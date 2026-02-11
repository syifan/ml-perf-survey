"""Base class for tool adapters."""
from abc import ABC, abstractmethod
from prototype.workload import WorkloadSpec
from prototype.result import ResultSet


class ToolAdapter(ABC):
    """Abstract base class for ML performance tool adapters.

    Each tool adapter wraps a specific performance prediction or simulation tool
    and translates between the unified WorkloadSpec/ResultSet formats and the
    tool's native input/output formats.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name."""
        ...

    @property
    @abstractmethod
    def category(self) -> str:
        """Tool category: analytical, simulation, ml-based, hybrid."""
        ...

    @property
    @abstractmethod
    def supported_metrics(self) -> list:
        """List of metric names this tool can produce."""
        ...

    @property
    @abstractmethod
    def supported_workloads(self) -> list:
        """List of workload types this tool supports (cnn, transformer, llm, etc.)."""
        ...

    @abstractmethod
    def supports(self, spec: WorkloadSpec) -> bool:
        """Check if this tool can handle the given workload."""
        ...

    @abstractmethod
    def run(self, spec: WorkloadSpec) -> ResultSet:
        """Run the tool on the given workload and return standardized results."""
        ...
