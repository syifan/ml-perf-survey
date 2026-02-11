"""ResultSet: Standardized output format for performance predictions.

All tool adapters return results in this format, enabling cross-tool comparison.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ResultSet:
    """Standardized result from a performance prediction/simulation."""

    tool: str
    workload: str
    metrics: dict = field(default_factory=dict)
    # metrics can include: latency_ms, throughput_samples_s, energy_uj,
    # cycles, utilization, memory_gb, flops, communication_time_ms

    raw_output: Optional[str] = None
    exit_code: int = 0
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "tool": self.tool,
            "workload": self.workload,
            "metrics": self.metrics,
            "exit_code": self.exit_code,
            "error": self.error,
        }

    def print_summary(self):
        """Print a human-readable summary."""
        print(f"=== {self.tool} -> {self.workload} ===")
        if self.error:
            print(f"  ERROR: {self.error}")
            return
        for key, value in self.metrics.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")

    @staticmethod
    def print_comparison(results: list):
        """Print a comparison table across multiple results."""
        if not results:
            return

        # Collect all metric keys
        all_keys = set()
        for r in results:
            all_keys.update(r.metrics.keys())
        all_keys = sorted(all_keys)

        # Header
        tool_names = [r.tool for r in results]
        header = f"{'Metric':<30}" + "".join(f"{t:<20}" for t in tool_names)
        print(header)
        print("-" * len(header))

        # Rows
        for key in all_keys:
            row = f"{key:<30}"
            for r in results:
                val = r.metrics.get(key, "N/A")
                if isinstance(val, float):
                    row += f"{val:<20.4f}"
                else:
                    row += f"{str(val):<20}"
            print(row)
