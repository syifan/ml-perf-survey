# Unified Performance Modeling Tool — Design Document

**Issue:** #154 (Contribution 3)
**Author:** Flux
**Date:** 2026-02-11
**Status:** Draft v1

---

## 1. Problem Statement

The ML performance modeling landscape is fragmented: each tool covers a narrow slice (e.g., Timeloop for accelerators, VIDUR for LLM inference, ASTRA-sim for distributed training). Researchers must learn multiple tools, formats, and interfaces. There is no unified way to:

- Define a workload once and evaluate it across tools
- Compare results in a standardized format
- Switch between modeling approaches (analytical, simulation, ML-based)

## 2. Design Goals

1. **Unified workload specification** — one YAML/JSON format for any ML workload
2. **Tool adapter pattern** — pluggable backends for each tool
3. **Standardized output** — common metrics schema (latency, throughput, energy, utilization)
4. **Minimal CLI** — `mlperf-model run --tool vidur --workload resnet50.yaml`
5. **Incremental** — start with 2 tools (VIDUR + ASTRA-sim), add more over time

## 3. Architecture

```
+--------------------------------------------------+
|                    CLI (click)                    |
|  mlperf-model run/compare/list                   |
+--------------------------------------------------+
|               Workload Parser                    |
|  Reads unified YAML -> WorkloadSpec dataclass    |
+--------------------------------------------------+
|              Tool Adapter Layer                   |
|  +-----------+ +-----------+ +---------------+   |
|  | VIDUR     | | ASTRA-sim | | Timeloop      |   |
|  | Adapter   | | Adapter   | | Adapter       |   |
|  +-----------+ +-----------+ +---------------+   |
+--------------------------------------------------+
|            Results Collector                      |
|  Normalizes tool outputs -> ResultSet dataclass  |
+--------------------------------------------------+
|            Output / Comparison                    |
|  JSON, table, CSV export                         |
+--------------------------------------------------+
```

## 4. Unified Workload Format

```yaml
workload:
  name: resnet50-training
  type: training           # training | inference | serving
  model:
    name: ResNet-50
    framework: pytorch
    layers: 50
  hardware:
    device: gpu
    name: A100-80GB
    count: 8
    interconnect: nvlink
  batch_size: 256
  precision: fp16
  distributed:
    strategy: data_parallel
    num_nodes: 1
```

## 5. Tool Adapter Interface

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class WorkloadSpec:
    name: str
    type: str  # training, inference, serving
    model_name: str
    hardware: dict
    batch_size: int
    precision: str
    distributed: dict | None = None

@dataclass
class ToolResult:
    tool_name: str
    workload_name: str
    latency_ms: float | None = None
    throughput_samples_per_s: float | None = None
    energy_uj: float | None = None
    cycles: int | None = None
    utilization: float | None = None
    raw_output: dict | None = None

class ToolAdapter(ABC):
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def supports(self, workload: WorkloadSpec) -> bool: ...

    @abstractmethod
    def run(self, workload: WorkloadSpec) -> ToolResult: ...
```

## 6. Phase 1 Scope (Minimum Viable)

| Component | Status | Notes |
|-----------|--------|-------|
| CLI skeleton (`mlperf-model`) | TODO | click-based, 3 commands |
| WorkloadSpec dataclass | TODO | Python dataclass + YAML loader |
| VIDUR adapter | TODO | Wraps existing Docker/Python scripts |
| ASTRA-sim adapter | TODO | Wraps existing Docker/bash scripts |
| ResultSet + JSON output | TODO | Standardized metrics |
| One example workload YAML | TODO | ResNet-50 training |

## 7. Phase 2 (Post-submission stretch)

- Timeloop adapter
- NeuSight adapter
- Comparison table generator (LaTeX/Markdown)
- Web dashboard

## 8. Directory Structure

```
prototype/
  mlperf_model/
    __init__.py
    cli.py              # Click CLI entry point
    workload.py          # WorkloadSpec + YAML parser
    result.py            # ToolResult + ResultSet
    adapters/
      __init__.py
      base.py          # ToolAdapter ABC
      vidur.py         # VIDUR adapter
      astra_sim.py     # ASTRA-sim adapter
  workloads/
    resnet50_training.yaml
  setup.py
  README.md
```

## 9. Implementation Plan

1. **Cycle N (current):** This design doc + CLI skeleton
2. **Cycle N+1:** WorkloadSpec parser + VIDUR adapter (wraps existing scripts)
3. **Cycle N+2:** ASTRA-sim adapter + comparison output
4. **Cycle N+3:** End-to-end demo with ResNet-50 across both tools

## 10. Open Questions

- Should adapters call Docker directly or expect tools pre-installed?
  - **Proposed:** Docker-first for isolation, with a `--local` flag for pre-installed tools
- How to handle tools that need different workload granularity (layer vs. model)?
  - **Proposed:** WorkloadSpec supports both; adapters pick what they need
- Integration with paper: should prototype results go into Section 7?
  - **Proposed:** Yes, as a "proof of concept" subsection
