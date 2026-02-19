#!/usr/bin/env python3
"""Ground-truth GPU benchmark: Matrix Multiplication (GEMM).

Measures actual GPU execution time for matrix multiplications at sizes
representative of transformer model workloads (embedding projections,
attention QKV, FFN layers). Results serve as ground truth to compare
against performance prediction tool estimates.
"""

import argparse
import csv
import json
import os
import time
import torch
import torch.cuda

# GEMM sizes representative of transformer workloads:
# (M, K, N) — corresponding to output_rows x inner_dim x output_cols
DEFAULT_SIZES = [
    # Attention QKV projections (batch*seq, hidden, 3*hidden)
    (1024, 4096, 12288),   # ~7B model, seq=1024
    (2048, 4096, 12288),   # ~7B model, seq=2048
    (1024, 5120, 15360),   # ~13B model, seq=1024
    # FFN layers (batch*seq, hidden, 4*hidden)
    (1024, 4096, 16384),   # ~7B FFN up-projection
    (2048, 4096, 16384),   # ~7B FFN up-projection, longer seq
    (1024, 5120, 20480),   # ~13B FFN up-projection
    # Small GEMMs (single-token decode, batch=1)
    (1, 4096, 12288),      # Single token, 7B QKV
    (1, 4096, 16384),      # Single token, 7B FFN
    (32, 4096, 12288),     # Small batch decode
    # Large GEMMs
    (4096, 4096, 4096),    # Square large
    (8192, 4096, 4096),    # Rectangular large
]


def benchmark_gemm(M, K, N, dtype, warmup=10, iters=100):
    """Run a single GEMM benchmark and return timing stats."""
    A = torch.randn(M, K, dtype=dtype, device="cuda")
    B = torch.randn(K, N, dtype=dtype, device="cuda")

    # Warmup
    for _ in range(warmup):
        torch.mm(A, B)
    torch.cuda.synchronize()

    # Timed iterations
    start_events = [torch.cuda.Event(enable_timing=True) for _ in range(iters)]
    end_events = [torch.cuda.Event(enable_timing=True) for _ in range(iters)]

    for i in range(iters):
        start_events[i].record()
        torch.mm(A, B)
        end_events[i].record()

    torch.cuda.synchronize()

    times_ms = [s.elapsed_time(e) for s, e in zip(start_events, end_events)]
    times_ms.sort()

    # Compute TFLOPS: GEMM does 2*M*N*K FLOPs
    flops = 2 * M * N * K
    median_ms = times_ms[len(times_ms) // 2]
    tflops = flops / (median_ms / 1000) / 1e12

    return {
        "M": M,
        "K": K,
        "N": N,
        "dtype": str(dtype),
        "median_ms": round(median_ms, 4),
        "mean_ms": round(sum(times_ms) / len(times_ms), 4),
        "min_ms": round(times_ms[0], 4),
        "max_ms": round(times_ms[-1], 4),
        "p95_ms": round(times_ms[int(0.95 * len(times_ms))], 4),
        "tflops": round(tflops, 2),
        "iters": iters,
    }


def get_gpu_info():
    """Collect GPU hardware information."""
    props = torch.cuda.get_device_properties(0)
    return {
        "gpu_name": props.name,
        "gpu_memory_gb": round(props.total_memory / (1024**3), 1),
        "cuda_version": torch.version.cuda,
        "pytorch_version": torch.__version__,
        "gpu_count": torch.cuda.device_count(),
    }


def main():
    parser = argparse.ArgumentParser(description="GEMM ground-truth benchmark")
    parser.add_argument("--dtype", choices=["fp16", "fp32", "bf16"], default="fp16",
                        help="Data type for matrix operations")
    parser.add_argument("--iters", type=int, default=100,
                        help="Number of timed iterations per size")
    parser.add_argument("--warmup", type=int, default=10,
                        help="Number of warmup iterations")
    parser.add_argument("--output-dir", default="results",
                        help="Directory for output files")
    # Single-config overrides (used by run_perfsim_survey_2026.sh)
    # Accepts one or more 'M,K,N' tokens, e.g. --sizes 2048,5120,256 2048,256,5120
    parser.add_argument("--sizes", nargs="+", default=None,
                        help="Override sizes as space-separated M,K,N tokens")
    args = parser.parse_args()

    dtype_map = {"fp16": torch.float16, "fp32": torch.float32, "bf16": torch.bfloat16}
    dtype = dtype_map[args.dtype]

    os.makedirs(args.output_dir, exist_ok=True)

    gpu_info = get_gpu_info()
    print(f"GPU: {gpu_info['gpu_name']} ({gpu_info['gpu_memory_gb']} GB)")
    print(f"CUDA: {gpu_info['cuda_version']}, PyTorch: {gpu_info['pytorch_version']}")
    print(f"Dtype: {args.dtype}, Iterations: {args.iters}")
    print("-" * 80)
    print(f"{'M':>6} {'K':>6} {'N':>6} | {'Median(ms)':>10} {'Mean(ms)':>10} {'TFLOPS':>8}")
    print("-" * 80)

    # If --sizes provided, parse them; otherwise fall back to DEFAULT_SIZES
    if args.sizes is not None:
        sizes = []
        for token in args.sizes:
            parts = token.split(",")
            if len(parts) != 3:
                parser.error(f"--sizes token '{token}' must be in M,K,N format")
            sizes.append(tuple(int(p) for p in parts))
    else:
        sizes = DEFAULT_SIZES

    results = []
    for M, K, N in sizes:
        try:
            r = benchmark_gemm(M, K, N, dtype, warmup=args.warmup, iters=args.iters)
            results.append(r)
            print(f"{M:>6} {K:>6} {N:>6} | {r['median_ms']:>10.4f} {r['mean_ms']:>10.4f} {r['tflops']:>8.2f}")
        except RuntimeError as e:
            print(f"{M:>6} {K:>6} {N:>6} | SKIPPED ({e})")
        torch.cuda.empty_cache()

    # Save results
    output = {
        "benchmark": "gemm",
        "gpu_info": gpu_info,
        "config": {"dtype": args.dtype, "iters": args.iters, "warmup": args.warmup},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "results": results,
    }

    json_path = os.path.join(args.output_dir, f"gemm_{args.dtype}.json")
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)

    csv_path = os.path.join(args.output_dir, f"gemm_{args.dtype}.csv")
    if results:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    print(f"\nResults saved to {json_path} and {csv_path}")


if __name__ == "__main__":
    main()
