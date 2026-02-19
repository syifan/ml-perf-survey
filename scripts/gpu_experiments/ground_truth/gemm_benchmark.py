#!/usr/bin/env python3
"""Ground-truth GPU benchmark: Matrix Multiplication (GEMM).

Measures actual GPU execution time for matrix multiplications at sizes
representative of transformer model workloads (embedding projections,
attention QKV, FFN layers). Results serve as ground truth to compare
against performance prediction tool estimates.

Supports CUDA, ROCm, Apple MPS, and CPU backends.
"""

import argparse
import csv
import json
import os
import platform
import subprocess
import time
import torch

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


def get_device(requested="auto"):
    """Detect and return the best available compute device."""
    if requested in ("cuda", "auto") and torch.cuda.is_available():
        return torch.device("cuda"), "cuda"
    if requested in ("mps", "auto") and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps"), "mps"
    if requested in ("cpu", "auto"):
        return torch.device("cpu"), "cpu"
    raise ValueError(f"Requested backend '{requested}' not available")


def get_device_info(device, device_type):
    """Collect device hardware information."""
    info = {"device_type": device_type, "pytorch_version": torch.__version__}
    if device_type == "cuda":
        props = torch.cuda.get_device_properties(0)
        info.update({
            "gpu_name": props.name,
            "gpu_memory_gb": round(props.total_memory / (1024**3), 1),
            "cuda_version": torch.version.cuda,
            "gpu_count": torch.cuda.device_count(),
        })
    elif device_type == "mps":
        info.update({"gpu_name": "Apple GPU (MPS)", "gpu_count": 1})
        try:
            mem = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip()
            info["gpu_memory_gb"] = round(int(mem) / (1024**3), 1)
        except Exception:
            info["gpu_memory_gb"] = "unknown"
    else:
        info.update({"gpu_name": "CPU", "gpu_count": 0, "gpu_memory_gb": 0})
    return info


def sync_device(device_type):
    """Synchronize the device to ensure all operations are complete."""
    if device_type == "cuda":
        torch.cuda.synchronize()
    elif device_type == "mps":
        if hasattr(torch.mps, "synchronize"):
            torch.mps.synchronize()


def timed_iters(fn, device_type, warmup, iters):
    """Run warmup + timed iterations with proper synchronization."""
    for _ in range(warmup):
        fn()
    sync_device(device_type)
    times_ms = []
    for _ in range(iters):
        t0 = time.perf_counter()
        fn()
        sync_device(device_type)
        times_ms.append((time.perf_counter() - t0) * 1000.0)
    return times_ms


def benchmark_gemm(M, K, N, dtype, device, device_type, warmup=10, iters=100):
    """Run a single GEMM benchmark and return timing stats."""
    A = torch.randn(M, K, dtype=dtype, device=device)
    B = torch.randn(K, N, dtype=dtype, device=device)

    def fn():
        torch.mm(A, B)

    times_ms = timed_iters(fn, device_type, warmup, iters)
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
    parser.add_argument("--device", choices=["auto", "cuda", "mps", "cpu"], default="auto",
                        help="Compute backend: auto (default), cuda, mps, or cpu")
    # Single-config overrides (used by run_perfsim_survey_2026.sh)
    # Accepts one or more 'M,K,N' tokens, e.g. --sizes 2048,5120,256 2048,256,5120
    parser.add_argument("--sizes", nargs="+", default=None,
                        help="Override sizes as space-separated M,K,N tokens")
    args = parser.parse_args()

    dtype_map = {"fp16": torch.float16, "fp32": torch.float32, "bf16": torch.bfloat16}
    dtype = dtype_map[args.dtype]

    device, device_type = get_device(args.device)

    os.makedirs(args.output_dir, exist_ok=True)

    device_info = get_device_info(device, device_type)
    print(f"Device: {device_info['gpu_name']} (type={device_type})")
    if device_type == "cuda":
        print(f"CUDA: {device_info.get('cuda_version', 'N/A')}, PyTorch: {device_info['pytorch_version']}")
    else:
        print(f"PyTorch: {device_info['pytorch_version']}")
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
            r = benchmark_gemm(M, K, N, dtype, device=device, device_type=device_type,
                               warmup=args.warmup, iters=args.iters)
            results.append(r)
            print(f"{M:>6} {K:>6} {N:>6} | {r['median_ms']:>10.4f} {r['mean_ms']:>10.4f} {r['tflops']:>8.2f}")
        except RuntimeError as e:
            print(f"{M:>6} {K:>6} {N:>6} | SKIPPED ({e})")
        if device_type == "cuda":
            torch.cuda.empty_cache()

    # Save results
    output = {
        "benchmark": "gemm",
        "device_info": device_info,
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
