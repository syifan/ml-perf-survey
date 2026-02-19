#!/usr/bin/env python3
"""Ground-truth GPU benchmark: Feed-Forward Network (FFN) layers.

Measures actual GPU execution time for transformer FFN blocks
(two linear projections with activation) at configurations matching
common LLMs. Results serve as ground truth for prediction tool comparison.

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
                  activation, dtype, device, device_type, warmup=10, iters=100):
    """Run FFN benchmark and return timing stats."""
    if activation == "silu":
        model = LLaMAFFN(hidden_dim, intermediate_dim, dtype).to(device).eval()
    else:
        model = GPTFFN(hidden_dim, intermediate_dim, dtype).to(device).eval()

    x = torch.randn(batch_size, seq_len, hidden_dim, dtype=dtype, device=device)

    with torch.no_grad():
        def fn():
            model(x)

        times_ms = timed_iters(fn, device_type, warmup, iters)

    times_ms.sort()
    median_ms = times_ms[len(times_ms) // 2]

    # Memory info (CUDA only)
    if device_type == "cuda":
        mem_allocated_mb = torch.cuda.max_memory_allocated() / (1024**2)
        torch.cuda.reset_peak_memory_stats()
    else:
        mem_allocated_mb = 0

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


def main():
    parser = argparse.ArgumentParser(description="FFN ground-truth benchmark")
    parser.add_argument("--dtype", choices=["fp16", "fp32", "bf16"], default="fp16")
    parser.add_argument("--iters", type=int, default=100)
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--device", choices=["auto", "cuda", "mps", "cpu"], default="auto",
                        help="Compute backend: auto (default), cuda, mps, or cpu")
    # Single-config overrides (used by run_perfsim_survey_2026.sh)
    parser.add_argument("--hidden-dim", type=int, default=None)
    parser.add_argument("--ffn-dim", type=int, default=None)
    parser.add_argument("--seq-len", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
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
                              device=device, device_type=device_type,
                              warmup=args.warmup, iters=args.iters)
            r["label"] = label
            results.append(r)
            print(f"{label:<22} {hidden_dim:>6} {inter_dim:>6} {seq_len:>5} | "
                  f"{r['median_ms']:>10.4f} {r['peak_mem_mb']:>8.1f}")
        except RuntimeError as e:
            print(f"{label:<22} | SKIPPED ({e})")
        if device_type == "cuda":
            torch.cuda.empty_cache()

    output = {
        "benchmark": "ffn",
        "device_info": device_info,
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
