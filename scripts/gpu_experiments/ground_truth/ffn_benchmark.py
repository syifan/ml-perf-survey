#!/usr/bin/env python3
"""Ground-truth GPU benchmark: Feed-Forward Network (FFN) layers.

Measures actual GPU execution time for transformer FFN blocks
(two linear projections with activation) at configurations matching
common LLMs. Results serve as ground truth for prediction tool comparison.
"""

import argparse
import csv
import json
import os
import time
import torch
import torch.cuda
import torch.nn as nn

# FFN configs: (hidden_dim, intermediate_dim, seq_len, batch_size, activation, label)
DEFAULT_CONFIGS = [
    # Standard FFN: hidden -> 4*hidden -> hidden with SiLU (LLaMA-style)
    (4096, 11008, 1024, 1, "silu", "7B-seq1024"),
    (4096, 11008, 2048, 1, "silu", "7B-seq2048"),
    (4096, 11008, 512, 4, "silu", "7B-seq512-b4"),
    (5120, 13824, 1024, 1, "silu", "13B-seq1024"),
    (5120, 13824, 2048, 1, "silu", "13B-seq2048"),
    (8192, 28672, 1024, 1, "silu", "70B-seq1024"),
    # Single-token decode (small M, large K/N)
    (4096, 11008, 1, 1, "silu", "7B-decode-b1"),
    (4096, 11008, 1, 8, "silu", "7B-decode-b8"),
    (4096, 11008, 1, 32, "silu", "7B-decode-b32"),
    (5120, 13824, 1, 1, "silu", "13B-decode-b1"),
    # GPT-style FFN with GELU
    (4096, 16384, 1024, 1, "gelu", "GPT-7B-seq1024"),
    (4096, 16384, 2048, 1, "gelu", "GPT-7B-seq2048"),
]


class LLaMAFFN(nn.Module):
    """LLaMA-style FFN with gate projection and SiLU activation."""
    def __init__(self, hidden_dim, intermediate_dim, dtype):
        super().__init__()
        self.gate_proj = nn.Linear(hidden_dim, intermediate_dim, bias=False).to(dtype)
        self.up_proj = nn.Linear(hidden_dim, intermediate_dim, bias=False).to(dtype)
        self.down_proj = nn.Linear(intermediate_dim, hidden_dim, bias=False).to(dtype)
        self.act = nn.SiLU()

    def forward(self, x):
        return self.down_proj(self.act(self.gate_proj(x)) * self.up_proj(x))


class GPTFFN(nn.Module):
    """GPT-style FFN with GELU activation."""
    def __init__(self, hidden_dim, intermediate_dim, dtype):
        super().__init__()
        self.fc1 = nn.Linear(hidden_dim, intermediate_dim, bias=True).to(dtype)
        self.fc2 = nn.Linear(intermediate_dim, hidden_dim, bias=True).to(dtype)
        self.act = nn.GELU()

    def forward(self, x):
        return self.fc2(self.act(self.fc1(x)))


def benchmark_ffn(hidden_dim, intermediate_dim, seq_len, batch_size,
                  activation, dtype, warmup=10, iters=100):
    """Run FFN benchmark and return timing stats."""
    if activation == "silu":
        model = LLaMAFFN(hidden_dim, intermediate_dim, dtype).cuda().eval()
    else:
        model = GPTFFN(hidden_dim, intermediate_dim, dtype).cuda().eval()

    x = torch.randn(batch_size, seq_len, hidden_dim, dtype=dtype, device="cuda")

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

    # Memory info
    mem_allocated_mb = torch.cuda.max_memory_allocated() / (1024**2)
    torch.cuda.reset_peak_memory_stats()

    return {
        "hidden_dim": hidden_dim,
        "intermediate_dim": intermediate_dim,
        "seq_len": seq_len,
        "batch_size": batch_size,
        "activation": activation,
        "dtype": str(dtype),
        "median_ms": round(median_ms, 4),
        "mean_ms": round(sum(times_ms) / len(times_ms), 4),
        "min_ms": round(times_ms[0], 4),
        "max_ms": round(times_ms[-1], 4),
        "p95_ms": round(times_ms[int(0.95 * len(times_ms))], 4),
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
    parser = argparse.ArgumentParser(description="FFN ground-truth benchmark")
    parser.add_argument("--dtype", choices=["fp16", "fp32", "bf16"], default="fp16")
    parser.add_argument("--iters", type=int, default=100)
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--output-dir", default="results")
    # Single-config overrides (used by run_perfsim_survey_2026.sh)
    parser.add_argument("--hidden-dim", type=int, default=None)
    parser.add_argument("--ffn-dim", type=int, default=None)
    parser.add_argument("--seq-len", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    args = parser.parse_args()

    dtype_map = {"fp16": torch.float16, "fp32": torch.float32, "bf16": torch.bfloat16}
    dtype = dtype_map[args.dtype]

    os.makedirs(args.output_dir, exist_ok=True)

    gpu_info = get_gpu_info()
    print(f"GPU: {gpu_info['gpu_name']} ({gpu_info['gpu_memory_gb']} GB)")
    print(f"CUDA: {gpu_info['cuda_version']}, PyTorch: {gpu_info['pytorch_version']}")
    print(f"Dtype: {args.dtype}, Iterations: {args.iters}")
    print("-" * 90)
    print(f"{'Label':<22} {'Hidden':>6} {'Inter':>6} {'Seq':>5} | {'Median(ms)':>10} {'Mem(MB)':>8}")
    print("-" * 90)

    # If single-config args provided, run one benchmark; otherwise use DEFAULT_CONFIGS
    if args.hidden_dim is not None:
        hidden_dim = args.hidden_dim
        inter_dim = args.ffn_dim if args.ffn_dim is not None else hidden_dim * 4
        seq_len = args.seq_len if args.seq_len is not None else 2048
        batch_size = args.batch_size if args.batch_size is not None else 1
        label = f"custom-h{hidden_dim}-i{inter_dim}-s{seq_len}-b{batch_size}"
        configs = [(hidden_dim, inter_dim, seq_len, batch_size, "silu", label)]
    else:
        configs = DEFAULT_CONFIGS

    results = []
    for hidden_dim, inter_dim, seq_len, batch_size, act, label in configs:
        try:
            r = benchmark_ffn(hidden_dim, inter_dim, seq_len, batch_size, act, dtype,
                              warmup=args.warmup, iters=args.iters)
            r["label"] = label
            results.append(r)
            print(f"{label:<22} {hidden_dim:>6} {inter_dim:>6} {seq_len:>5} | "
                  f"{r['median_ms']:>10.4f} {r['peak_mem_mb']:>8.1f}")
        except RuntimeError as e:
            print(f"{label:<22} | SKIPPED ({e})")
        torch.cuda.empty_cache()

    output = {
        "benchmark": "ffn",
        "gpu_info": gpu_info,
        "config": {"dtype": args.dtype, "iters": args.iters, "warmup": args.warmup},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "results": results,
    }

    json_path = os.path.join(args.output_dir, f"ffn_{args.dtype}.json")
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)

    csv_path = os.path.join(args.output_dir, f"ffn_{args.dtype}.csv")
    if results:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    print(f"\nResults saved to {json_path} and {csv_path}")


if __name__ == "__main__":
    main()
