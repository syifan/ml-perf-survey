"""Timeloop adapter: wraps Timeloop for DNN accelerator performance modeling."""
import json
import subprocess
import tempfile
from pathlib import Path

from prototype.adapters.base import ToolAdapter
from prototype.workload import WorkloadSpec
from prototype.result import ResultSet


class TimeloopAdapter(ToolAdapter):
    """Adapter for Timeloop analytical DNN accelerator modeling tool."""

    @property
    def name(self) -> str:
        return "timeloop"

    @property
    def category(self) -> str:
        return "analytical"

    @property
    def supported_metrics(self) -> list:
        return ["cycles", "energy_uj", "utilization", "latency_ms"]

    @property
    def supported_workloads(self) -> list:
        return ["cnn", "transformer"]

    def supports(self, spec: WorkloadSpec) -> bool:
        return spec.model_type in self.supported_workloads

    def run(self, spec: WorkloadSpec) -> ResultSet:
        """Run Timeloop on the workload.

        Currently delegates to the existing run_resnet50_conv.py script.
        Future: generate Timeloop configs dynamically from WorkloadSpec.
        """
        script_path = (
            Path(__file__).parent.parent.parent
            / "scripts"
            / "benchmarks"
            / "timeloop"
            / "run_resnet50_conv.py"
        )

        if not script_path.exists():
            return ResultSet(
                tool=self.name,
                workload=spec.name,
                error=f"Timeloop script not found at {script_path}",
                exit_code=1,
            )

        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ["python3", str(script_path), "--analytical-only", "--output-dir", tmpdir],
                capture_output=True,
                text=True,
                timeout=60,
            )

            results_file = Path(tmpdir) / "resnet50_conv1_results.json"
            if results_file.exists():
                with open(results_file) as f:
                    data = json.load(f)
                analytical = data.get("analytical_estimates", {})
                return ResultSet(
                    tool=self.name,
                    workload=spec.name,
                    metrics={
                        "cycles": analytical.get("estimated_cycles", 0),
                        "energy_uj": analytical.get("total_energy_uj", 0),
                        "utilization": analytical.get("estimated_utilization", 0),
                        "latency_ms": analytical.get("estimated_latency_ms", 0),
                    },
                    raw_output=result.stdout,
                    exit_code=result.returncode,
                )

            return ResultSet(
                tool=self.name,
                workload=spec.name,
                error="No results produced",
                raw_output=result.stderr,
                exit_code=result.returncode,
            )
