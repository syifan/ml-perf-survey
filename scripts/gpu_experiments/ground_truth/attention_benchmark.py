#!/usr/bin/env python3
"""Ground-truth GPU benchmark: Multi-Head Attention.

Measures actual GPU execution time for multi-head attention at
configurations matching common transformer models (7B, 13B, 70B).
Tests both prefill (long input) and decode (single token) scenarios.
Results serve as ground truth for prediction tool comparison.
"""

import argparse
import csv
import json
import os
import time
import torch
import torch.cuda
import torch.nn.functional as F

# Attention configs: (num_heads, head_dim, seq_len, batch_size, label)
DEFAULT_CONFIGS = [
    # Prefill scenarios (processing full prompt)
    (32, 128, 512, 1, "7B-prefill-512"),
    (32, 128, 1024, 1, "7B-prefill-1024"),
    (32, 128, 2048, 1, "7B-prefill-2048"),
    (40, 128, 512, 1, "13B-prefill-512"),
    (40, 128, 1024, 1, "13B-prefill-1024"),
    (64, 128, 1024, 1, "70B-prefill-1024"),
    # Decode scenarios (generating one token at a time)
    (32, 128, 1, 1, "7B-decode-b1"),
    (32, 128, 1, 8, "7B-decode-b8"),
    (32, 128, 1, 32, "7B-decode-b32"),
    (40, 128, 1, 1, "13B-decode-b1"),
    (40, 128, 1, 8, "13B-decode-b8"),
    # Batched prefill
    (32, 128, 512, 4, "7B-prefill-512-b4"),
    (32, 128, 512, 8, "7B-prefill-512-b8"),
]


def benchmark_attention(num_heads, head_dim, seq_len, batch_size, dtype,
                        warmup=10, iters=100):
    """Run scaled dot-product attention and measure timing."""
    hidden_dim = num_heads * head_dim

    # Create Q, K, V tensors shaped for multi-head attention
    # Shape: (batch, num_heads, seq_len, head_dim)
    Q = torch.randn(batch_size, num_heads, seq_len, head_dim,
                     dtype=dtype, device="cuda")
    K = torch.randn(batch_size, num_heads, seq_len, head_dim,
                     dtype=dtype, device="cuda")
    V = torch.randn(batch_size, num_heads, seq_len, head_dim,
                     dtype=dtype, device="cuda")

    # Warmup
    for _ in range(warmup):
        F.scaled_dot_product_attention(Q, K, V, is_causal=True)
    torch.cuda.synchronize()

    # Timed iterations
    start_events = [torch.cuda.Event(enable_timing=True) for _ in range(iters)]
    end_events = [torch.cuda.Event(enable_timing=True) for _ in range(iters)]

    for i in range(iters):
        start_events[i].record()
        F.scaled_dot_product_attention(Q, K, V, is_causal=True)
        end_events[i].record()

    torch.cuda.synchronize()

    times_ms = [s.elapsed_time(e) for s, e in zip(start_events, end_events)]
    times_ms.sort()

    median_ms = times_ms[len(times_ms) // 2]

    return {
        "num_heads": num_heads,
        "head_dim": head_dim,
        "seq_len": seq_len,
        "batch_size": batch_size,
        "hidden_dim": hidden_dim,
        "dtype": str(dtype),
        "median_ms": round(median_ms, 4),
        "mean_ms": round(sum(times_ms) / len(times_ms), 4),
        "min_ms": round(times_ms[0], 4),
        "max_ms": round(times_ms[-1], 4),
        "p95_ms": round(times_ms[int(0.95 * len(times_ms))], 4),
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
    parser = argparse.ArgumentParser(description="Attention ground-truth benchmark")
    parser.add_argument("--dtype", choices=["fp16", "fp32", "bf16"], default="fp16")
    parser.add_argument("--iters", type=int, default=100)
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--output-dir", default="results")
    # Single-config overrides (used by run_perfsim_survey_2026.sh)
    parser.add_argument("--hidden-dim", type=int, default=None)
    parser.add_argument("--num-heads", type=int, default=None)
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
    print(f"{'Label':<22} {'Heads':>5} {'Seq':>6} {'Batch':>5} | {'Median(ms)':>10} {'Mean(ms)':>10}")
    print("-" * 90)

    # If single-config args provided, run one benchmark; otherwise use DEFAULT_CONFIGS
    if args.hidden_dim is not None:
        num_heads = args.num_heads if args.num_heads is not None else 32
        head_dim = args.hidden_dim // num_heads
        seq_len = args.seq_len if args.seq_len is not None else 2048
        batch_size = args.batch_size if args.batch_size is not None else 1
        label = f"custom-h{args.hidden_dim}-nh{num_heads}-s{seq_len}-b{batch_size}"
        configs = [(num_heads, head_dim, seq_len, batch_size, label)]
    else:
        configs = DEFAULT_CONFIGS

    results = []
    for num_heads, head_dim, seq_len, batch_size, label in configs:
        try:
            r = benchmark_attention(num_heads, head_dim, seq_len, batch_size, dtype,
                                    warmup=args.warmup, iters=args.iters)
            r["label"] = label
            results.append(r)
            print(f"{label:<22} {num_heads:>5} {seq_len:>6} {batch_size:>5} | "
                  f"{r['median_ms']:>10.4f} {r['mean_ms']:>10.4f}")
        except RuntimeError as e:
            print(f"{label:<22} | SKIPPED ({e})")
        torch.cuda.empty_cache()

    output = {
        "benchmark": "attention",
        "gpu_info": gpu_info,
        "config": {"dtype": args.dtype, "iters": args.iters, "warmup": args.warmup},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "results": results,
    }

    json_path = os.path.join(args.output_dir, f"attention_{args.dtype}.json")
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)

    csv_path = os.path.join(args.output_dir, f"attention_{args.dtype}.csv")
    if results:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    print(f"\nResults saved to {json_path} and {csv_path}")


if __name__ == "__main__":
    main()
