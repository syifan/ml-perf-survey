"""Analytical adapter: roofline-model based performance estimation.

This adapter provides quick analytical estimates without external tools.
It serves as a baseline for comparison against more sophisticated tools.
"""
from prototype.adapters.base import ToolAdapter
from prototype.workload import WorkloadSpec
from prototype.result import ResultSet


# Approximate peak FLOPS (FP16) and memory bandwidth for common GPUs
GPU_SPECS = {
    "A100": {"peak_tflops": 312, "mem_bw_gb_s": 2039, "mem_gb": 80},
    "H100": {"peak_tflops": 989, "mem_bw_gb_s": 3350, "mem_gb": 80},
    "V100": {"peak_tflops": 125, "mem_bw_gb_s": 900, "mem_gb": 32},
    "T4":   {"peak_tflops": 65,  "mem_bw_gb_s": 300, "mem_gb": 16},
    "L4":   {"peak_tflops": 121, "mem_bw_gb_s": 300, "mem_gb": 24},
}

# Approximate FLOP counts for common models (FP16, inference, batch=1)
MODEL_FLOPS = {
    "ResNet-50":  {"flops": 8.2e9,   "params": 25.6e6},
    "BERT-base":  {"flops": 22.5e9,  "params": 110e6},
    "BERT-large": {"flops": 72.4e9,  "params": 340e6},
    "GPT-2":      {"flops": 35.4e9,  "params": 1.5e9},
    "GPT-3":      {"flops": 350e12,  "params": 175e9},
}


class AnalyticalAdapter(ToolAdapter):
    """Roofline-model based analytical performance estimator."""

    @property
    def name(self) -> str:
        return "analytical"

    @property
    def category(self) -> str:
        return "analytical"

    @property
    def supported_metrics(self) -> list:
        return ["latency_ms", "throughput_samples_s", "arithmetic_intensity", "memory_gb"]

    @property
    def supported_workloads(self) -> list:
        return ["cnn", "transformer", "llm"]

    def supports(self, spec: WorkloadSpec) -> bool:
        model_name = spec.model.get("name", "")
        device = spec.hardware.get("device", "")
        return model_name in MODEL_FLOPS and device in GPU_SPECS

    def run(self, spec: WorkloadSpec) -> ResultSet:
        model_name = spec.model.get("name", "")
        device = spec.hardware.get("device", "")

        if model_name not in MODEL_FLOPS:
            return ResultSet(
                tool=self.name, workload=spec.name,
                error=f"Unknown model: {model_name}",
                exit_code=1,
            )
        if device not in GPU_SPECS:
            return ResultSet(
                tool=self.name, workload=spec.name,
                error=f"Unknown device: {device}",
                exit_code=1,
            )

        model = MODEL_FLOPS[model_name]
        gpu = GPU_SPECS[device]

        flops = model["flops"] * spec.batch_size
        param_bytes = model["params"] * 2  # FP16

        # Arithmetic intensity (FLOP/byte)
        ai = flops / param_bytes

        # Roofline: min(compute bound, memory bound)
        compute_time_ms = (flops / (gpu["peak_tflops"] * 1e12)) * 1000
        memory_time_ms = (param_bytes / (gpu["mem_bw_gb_s"] * 1e9)) * 1000
        latency_ms = max(compute_time_ms, memory_time_ms)

        throughput = 1000.0 / latency_ms if latency_ms > 0 else 0

        return ResultSet(
            tool=self.name,
            workload=spec.name,
            metrics={
                "latency_ms": round(latency_ms, 4),
                "throughput_samples_s": round(throughput, 2),
                "arithmetic_intensity": round(ai, 2),
                "memory_gb": round(param_bytes / 1e9, 3),
                "compute_time_ms": round(compute_time_ms, 4),
                "memory_time_ms": round(memory_time_ms, 4),
                "bottleneck": "compute" if compute_time_ms > memory_time_ms else "memory",
            },
        )
