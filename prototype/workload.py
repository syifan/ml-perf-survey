"""WorkloadSpec: Unified workload description format.

A WorkloadSpec describes an ML workload in a tool-agnostic way.
Each tool adapter translates it into tool-specific input formats.

Example YAML:
    name: resnet50-training
    model_type: cnn
    model:
      name: ResNet-50
      layers: 50
      parameters: 25.6e6
    task: training
    batch_size: 32
    hardware:
      device: A100
      count: 8
      interconnect: NVLink
    dataset:
      name: ImageNet
      input_shape: [3, 224, 224]
"""
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class WorkloadSpec:
    """Unified workload specification."""

    name: str
    model_type: str  # cnn, transformer, llm, etc.
    model: dict = field(default_factory=dict)
    task: str = "inference"  # training, inference, serving
    batch_size: int = 1
    hardware: dict = field(default_factory=dict)
    dataset: dict = field(default_factory=dict)
    extra: dict = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str) -> "WorkloadSpec":
        """Load a workload spec from a YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(
            name=data["name"],
            model_type=data["model_type"],
            model=data.get("model", {}),
            task=data.get("task", "inference"),
            batch_size=data.get("batch_size", 1),
            hardware=data.get("hardware", {}),
            dataset=data.get("dataset", {}),
            extra=data.get("extra", {}),
        )

    @classmethod
    def from_dict(cls, data: dict) -> "WorkloadSpec":
        """Create from a dictionary."""
        return cls(
            name=data["name"],
            model_type=data["model_type"],
            model=data.get("model", {}),
            task=data.get("task", "inference"),
            batch_size=data.get("batch_size", 1),
            hardware=data.get("hardware", {}),
            dataset=data.get("dataset", {}),
            extra=data.get("extra", {}),
        )

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "name": self.name,
            "model_type": self.model_type,
            "model": self.model,
            "task": self.task,
            "batch_size": self.batch_size,
            "hardware": self.hardware,
            "dataset": self.dataset,
            "extra": self.extra,
        }
