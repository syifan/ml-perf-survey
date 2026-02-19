#!/usr/bin/env python3
"""Ground-truth GPU benchmark: Full Transformer Forward Pass.

Measures actual GPU execution time for complete transformer decoder
blocks (attention + FFN + layernorm) and stacked layers representing
full model forward passes. Results serve as ground truth for
prediction tool comparison.
"""

import argparse
import csv
import json
import os
import time
import torch
import torch.cuda
import torch.nn as nn

# Transformer configs: (num_layers, hidden_dim, num_heads, intermediate_dim,
#                        seq_len, batch_size, label)
DEFAULT_CONFIGS = [
    # Single transformer block
    (1, 4096, 32, 11008, 512, 1, "7B-1layer-seq512"),
    (1, 4096, 32, 11008, 1024, 1, "7B-1layer-seq1024"),
    (1, 4096, 32, 11008, 2048, 1, "7B-1layer-seq2048"),
    (1, 5120, 40, 13824, 1024, 1, "13B-1layer-seq1024"),
    # Stacked layers (partial model)
    (4, 4096, 32, 11008, 512, 1, "7B-4layers-seq512"),
    (8, 4096, 32, 11008, 512, 1, "7B-8layers-seq512"),
    (4, 5120, 40, 13824, 512, 1, "13B-4layers-seq512"),
    # Decode (single token)
    (1, 4096, 32, 11008, 1, 1, "7B-1layer-decode-b1"),
    (1, 4096, 32, 11008, 1, 8, "7B-1layer-decode-b8"),
    (4, 4096, 32, 11008, 1, 1, "7B-4layers-decode-b1"),
    (4, 4096, 32, 11008, 1, 8, "7B-4layers-decode-b8"),
    # Batched prefill
    (1, 4096, 32, 11008, 512, 4, "7B-1layer-seq512-b4"),
]


class TransformerBlock(nn.Module):
    """Standard transformer decoder block (pre-norm, LLaMA-style)."""
    def __init__(self, hidden_dim, num_heads, intermediate_dim, dtype):
        super().__init__()
        self.attn_norm = nn.RMSNorm(hidden_dim).to(dtype)
        self.ffn_norm = nn.RMSNorm(hidden_dim).to(dtype)
        self.attn = nn.MultiheadAttention(
            hidden_dim, num_heads, batch_first=True, dtype=dtype
        )
        self.gate_proj = nn.Linear(hidden_dim, intermediate_dim, bias=False, dtype=dtype)
        self.up_proj = nn.Linear(hidden_dim, intermediate_dim, bias=False, dtype=dtype)
        self.down_proj = nn.Linear(intermediate_dim, hidden_dim, bias=False, dtype=dtype)
        self.act = nn.SiLU()

    def forward(self, x, attn_mask=None):
        # Self-attention with residual
        h = self.attn_norm(x)
        h, _ = self.attn(h, h, h, attn_mask=attn_mask, need_weights=False)
        x = x + h
        # FFN with residual
        h = self.ffn_norm(x)
        h = self.down_proj(self.act(self.gate_proj(h)) * self.up_proj(h))
        return x + h


class StackedTransformer(nn.Module):
    """Stack of transformer decoder blocks."""
    def __init__(self, num_layers, hidden_dim, num_heads, intermediate_dim, dtype):
        super().__init__()
        self.layers = nn.ModuleList([
            TransformerBlock(hidden_dim, num_heads, intermediate_dim, dtype)
            for _ in range(num_layers)
        ])

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x


def benchmark_forward(num_layers, hidden_dim, num_heads, intermediate_dim,
                      seq_len, batch_size, dtype, warmup=10, iters=50):
    """Run forward pass benchmark and return timing stats."""
    model = StackedTransformer(
        num_layers, hidden_dim, num_heads, intermediate_dim, dtype
    ).cuda().eval()

    x = torch.randn(batch_size, seq_len, hidden_dim, dtype=dtype, device="cuda")

    # Count parameters
    num_params = sum(p.numel() for p in model.parameters())

    with torch.no_grad():
        # Warmup
        for _ in range(warmup):
            model(x)
        torch.cuda.synchronize()

        # Timed iterations
        start_events = [torch.cuda.Event(enable_timing=True) for _ in range(iters)]
        end_events = [torch.cuda.Event(enable_timing=True) for _ in range(iters)]

        for i in range(iters):
            start_events[i].record()
            model(x)
            end_events[i].record()

        torch.cuda.synchronize()

    times_ms = [s.elapsed_time(e) for s, e in zip(start_events, end_events)]
    times_ms.sort()
    median_ms = times_ms[len(times_ms) // 2]

    mem_allocated_mb = torch.cuda.max_memory_allocated() / (1024**2)
    torch.cuda.reset_peak_memory_stats()

    # Tokens per second
    total_tokens = batch_size * seq_len
    tokens_per_sec = total_tokens / (median_ms / 1000) if median_ms > 0 else 0

    return {
        "num_layers": num_layers,
        "hidden_dim": hidden_dim,
        "num_heads": num_heads,
        "intermediate_dim": intermediate_dim,
        "seq_len": seq_len,
        "batch_size": batch_size,
        "num_params_M": round(num_params / 1e6, 1),
        "dtype": str(dtype),
        "median_ms": round(median_ms, 4),
        "mean_ms": round(sum(times_ms) / len(times_ms), 4),
        "min_ms": round(times_ms[0], 4),
        "max_ms": round(times_ms[-1], 4),
        "p95_ms": round(times_ms[int(0.95 * len(times_ms))], 4),
        "tokens_per_sec": round(tokens_per_sec, 1),
        "peak_mem_mb": round(mem_allocated_mb, 1),
        "iters": iters,
    }


def get_gpu_info():
    props = torch.cuda.get_device_properties(0)
    return {
        "gpu_name": props.name,
        "gpu_memory_gb": round(props.total_memory / (1024**3), 1),
        "cuda_version": torch.version.cuda,
        "pytorch_version": torch.__version__,
        "gpu_count": torch.cuda.device_count(),
    }


def main():
    parser = argparse.ArgumentParser(description="Forward pass ground-truth benchmark")
    parser.add_argument("--dtype", choices=["fp16", "fp32", "bf16"], default="fp16")
    parser.add_argument("--iters", type=int, default=50)
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--output-dir", default="results")
    # Single-config overrides (used by run_perfsim_survey_2026.sh)
    parser.add_argument("--hidden-dim", type=int, default=None)
    parser.add_argument("--num-heads", type=int, default=None)
    parser.add_argument("--num-layers", type=int, default=None)
    parser.add_argument("--seq-len", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--intermediate-dim", type=int, default=None)
    args = parser.parse_args()

    dtype_map = {"fp16": torch.float16, "fp32": torch.float32, "bf16": torch.bfloat16}
    dtype = dtype_map[args.dtype]

    os.makedirs(args.output_dir, exist_ok=True)

    gpu_info = get_gpu_info()
    print(f"GPU: {gpu_info['gpu_name']} ({gpu_info['gpu_memory_gb']} GB)")
    print(f"CUDA: {gpu_info['cuda_version']}, PyTorch: {gpu_info['pytorch_version']}")
    print(f"Dtype: {args.dtype}, Iterations: {args.iters}")
    print("-" * 100)
    print(f"{'Label':<24} {'Layers':>6} {'Params':>8} {'Seq':>5} | "
          f"{'Median(ms)':>10} {'Tok/s':>10} {'Mem(MB)':>8}")
    print("-" * 100)

    # If single-config args provided, run one benchmark; otherwise use DEFAULT_CONFIGS
    if args.hidden_dim is not None:
        num_layers = args.num_layers if args.num_layers is not None else 1
        hidden = args.hidden_dim
        heads = args.num_heads if args.num_heads is not None else 32
        # Default intermediate_dim to ~2.7x hidden if not provided (LLaMA ratio)
        inter = args.intermediate_dim if args.intermediate_dim is not None else int(hidden * 2.6875)
        seq = args.seq_len if args.seq_len is not None else 2048
        batch = args.batch_size if args.batch_size is not None else 1
        label = f"custom-h{hidden}-l{num_layers}-s{seq}-b{batch}"
        configs = [(num_layers, hidden, heads, inter, seq, batch, label)]
    else:
        configs = DEFAULT_CONFIGS

    results = []
    for num_layers, hidden, heads, inter, seq, batch, label in configs:
        try:
            r = benchmark_forward(num_layers, hidden, heads, inter, seq, batch, dtype,
                                  warmup=args.warmup, iters=args.iters)
            r["label"] = label
            results.append(r)
            print(f"{label:<24} {num_layers:>6} {r['num_params_M']:>7.1f}M {seq:>5} | "
                  f"{r['median_ms']:>10.4f} {r['tokens_per_sec']:>10.1f} {r['peak_mem_mb']:>8.1f}")
        except RuntimeError as e:
            print(f"{label:<24} | SKIPPED ({e})")
        torch.cuda.empty_cache()

    output = {
        "benchmark": "forward_pass",
        "gpu_info": gpu_info,
        "config": {"dtype": args.dtype, "iters": args.iters, "warmup": args.warmup},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "results": results,
    }

    json_path = os.path.join(args.output_dir, f"forward_pass_{args.dtype}.json")
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)

    csv_path = os.path.join(args.output_dir, f"forward_pass_{args.dtype}.csv")
    if results:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    print(f"\nResults saved to {json_path} and {csv_path}")


if __name__ == "__main__":
    main()
