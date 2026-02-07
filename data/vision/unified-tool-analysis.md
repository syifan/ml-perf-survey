# Feasibility Analysis: Unified ML Performance Modeling Tool

This document analyzes the feasibility of combining ML performance modeling approaches into a unified tool for the research community.

---

## Executive Summary

A unified ML performance modeling tool is **technically feasible** but would require significant engineering effort. The key insight is that existing tools share common abstractions (workload representations, hardware models, prediction interfaces) that could be unified. However, the heterogeneity of target hardware and modeling approaches suggests a **modular architecture** rather than a monolithic tool.

**Recommendation:** Develop a unified framework with pluggable backends, starting with Timeloop (analytical) + VIDUR (LLM simulation) + nn-Meter (ML-based edge) integration.

---

## 1. Interface Comparison Across Top Approaches

### 1.1 Input Interfaces

| Tool | Workload Input | Hardware Input | Configuration |
|------|---------------|----------------|---------------|
| **Timeloop** | Layer shapes (YAML) | Architecture spec (YAML) | Mapping constraints |
| **nn-Meter** | ONNX/TFLite model | Device name (predefined) | Minimal |
| **ASTRA-sim** | Chakra traces (JSON) | Topology config | Parallelism strategy |
| **VIDUR** | Request traces | GPU config | Scheduling policy |
| **FlashAttention** | Tensor dimensions | Implicit (CUDA) | Head/seq params |

### 1.2 Output Interfaces

| Tool | Primary Output | Secondary Outputs | Format |
|------|----------------|-------------------|--------|
| **Timeloop** | Latency, Energy | Utilization, data movement | YAML/CSV |
| **nn-Meter** | Latency (ms) | Per-kernel breakdown | Python dict |
| **ASTRA-sim** | Training time | Communication breakdown | CSV/JSON |
| **VIDUR** | Request latency, throughput | Queue lengths, memory | CSV/JSON |
| **FlashAttention** | Execution time | Memory usage | Python |

### 1.3 Common Abstractions

| Abstraction | Timeloop | nn-Meter | ASTRA-sim | VIDUR |
|-------------|----------|----------|-----------|-------|
| **Layer/Op representation** | Yes | Yes | Yes | Partial |
| **Hardware parameters** | Detailed | Implicit | Moderate | Moderate |
| **Memory hierarchy** | Explicit | Implicit | Explicit | Partial |
| **Dataflow/schedule** | Explicit | Implicit | Explicit | Explicit |

---

## 2. Complementary Strengths

### 2.1 Coverage Matrix

| Capability | Analytical | ML-Based | Simulation | Gap |
|------------|------------|----------|------------|-----|
| **Single accelerator DSE** | Timeloop | - | GPGPU-Sim | Covered |
| **Edge latency** | - | nn-Meter | - | Covered |
| **Distributed training** | - | - | ASTRA-sim | Covered |
| **LLM inference** | - | - | VIDUR | Covered |
| **Attention optimization** | Partial | - | - | FlashAttention |
| **Energy prediction** | Timeloop | - | GPUWattch | Covered |
| **Cross-platform transfer** | - | LitePred/HELP | - | Partial |

### 2.2 Synergy Opportunities

| Combination | Value Proposition |
|-------------|-------------------|
| **Timeloop + ASTRA-sim** | Single-chip + distributed modeling |
| **nn-Meter + LitePred** | Edge prediction + cross-platform transfer |
| **VIDUR + FlashAttention** | LLM system + kernel-level optimization |
| **Analytical + ML** | Physics-informed ML models (hybrid) |

### 2.3 Integration Benefits

1. **Unified workload representation** - Convert once, model everywhere
2. **Consistent hardware specs** - Single source of truth for GPU/accelerator params
3. **Composable predictions** - Combine single-device with distributed modeling
4. **Shared datasets** - Centralized profiling data management

---

## 3. Implementation Complexity Analysis

### 3.1 Engineering Effort Estimates

| Component | Effort (Person-Months) | Complexity | Dependencies |
|-----------|------------------------|------------|--------------|
| **Unified workload format** | 3-6 | Medium | ONNX, Chakra |
| **Hardware abstraction layer** | 4-8 | High | All backends |
| **Backend adapters** | 2-4 per tool | Medium | Each tool's API |
| **Query/prediction API** | 2-4 | Low | Standard |
| **Results aggregation** | 1-2 | Low | Visualization |
| **Documentation** | 2-4 | Medium | All components |
| **Testing/validation** | 4-8 | High | Ground truth data |

**Total estimate:** ~28-54 person-months for MVP (2-3 developers over 14-18 months)

### 3.2 Technical Challenges

| Challenge | Difficulty | Mitigation |
|-----------|------------|------------|
| **Heterogeneous inputs** | High | Use ONNX as canonical format |
| **Different abstractions** | High | Adapter pattern with lossy conversion |
| **Accuracy calibration** | Medium | Per-backend validation |
| **Version management** | Medium | Pin versions, containerization |
| **Performance overhead** | Low | Lazy loading, caching |

### 3.3 Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Upstream tool changes | High | Medium | Version pinning, adapters |
| Accuracy degradation | Medium | High | Per-backend validation |
| Adoption resistance | Medium | High | Community involvement |
| Maintenance burden | High | Medium | Modular architecture |

---

## 4. Proposed Unified API Design

### 4.1 High-Level Architecture

```
+------------------+     +-------------------+     +------------------+
|   Workload       |     |   Hardware        |     |   Query          |
|   Specification  |     |   Specification   |     |   Configuration  |
+------------------+     +-------------------+     +------------------+
         |                        |                        |
         v                        v                        v
+----------------------------------------------------------------------+
|                        Unified API Layer                              |
|  - Workload parsing (ONNX, PyTorch, traces)                          |
|  - Hardware database (GPU, accelerator, edge device specs)            |
|  - Query routing (which backend for which query?)                     |
+----------------------------------------------------------------------+
         |                        |                        |
         v                        v                        v
+----------------+    +------------------+    +------------------+
| Timeloop       |    | nn-Meter         |    | VIDUR            |
| Adapter        |    | Adapter          |    | Adapter          |
+----------------+    +------------------+    +------------------+
         |                        |                        |
         v                        v                        v
+----------------------------------------------------------------------+
|                        Results Aggregation                            |
|  - Unified output format                                              |
|  - Visualization                                                      |
|  - Uncertainty quantification                                         |
+----------------------------------------------------------------------+
```

### 4.2 Core API Interfaces

```python
# Note: Pseudocode for illustration; production code would use @dataclass or Pydantic

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple, Literal

# Workload specification
class Workload:
    @classmethod
    def from_onnx(cls, path: str) -> "Workload": ...
    @classmethod
    def from_pytorch(cls, model, input_shape) -> "Workload": ...
    @classmethod
    def from_traces(cls, chakra_path: str) -> "Workload": ...

    def get_layers(self) -> List[Layer]: ...
    def get_graph(self) -> nx.DiGraph: ...

# Hardware specification
class Hardware:
    @classmethod
    def from_name(cls, name: str) -> "Hardware": ...  # e.g., "A100", "Pixel-7"
    @classmethod
    def from_spec(cls, spec: dict) -> "Hardware": ...

    def get_compute_capability(self) -> ComputeSpec: ...
    def get_memory_hierarchy(self) -> MemorySpec: ...

# Prediction query
@dataclass
class PredictionQuery:
    workload: Workload
    hardware: Hardware
    target: Literal["latency", "energy", "throughput"]
    scenario: Literal["inference", "training", "serving"]
    batch_size: int = 1

# Prediction result
@dataclass
class PredictionResult:
    value: float
    unit: str
    confidence: Optional[Tuple[float, float]]  # 95% CI
    breakdown: Optional[Dict[str, float]]  # Per-layer/component
    backend_used: str
    metadata: Dict[str, Any]

# Unified predictor
class UnifiedPredictor:
    def predict(self, query: PredictionQuery) -> PredictionResult:
        backend = self._select_backend(query)
        return backend.predict(query)

    def _select_backend(self, query: PredictionQuery) -> Backend:
        # Route to appropriate backend based on query type
        if query.scenario == "serving" and is_llm(query.workload):
            return self.vidur_backend
        elif is_edge_device(query.hardware):
            return self.nn_meter_backend
        elif query.target == "energy":
            return self.timeloop_backend
        else:
            # Default fallback to Timeloop for general DNN workloads
            return self.timeloop_backend
```

### 4.3 Example Usage

```python
from unified_perf import Workload, Hardware, PredictionQuery, UnifiedPredictor

# Load workload
workload = Workload.from_onnx("resnet50.onnx")

# Specify hardware
hardware = Hardware.from_name("A100-80GB")

# Create query
query = PredictionQuery(
    workload=workload,
    hardware=hardware,
    target="latency",
    scenario="inference",
    batch_size=32
)

# Get prediction
predictor = UnifiedPredictor()
result = predictor.predict(query)

print(f"Predicted latency: {result.value:.2f} {result.unit}")
print(f"Backend used: {result.backend_used}")
print(f"Confidence interval: {result.confidence}")
```

---

## 5. Integration Challenges

### 5.1 Workload Representation Mapping

| Source Format | Target: Timeloop | Target: nn-Meter | Target: VIDUR |
|---------------|------------------|------------------|---------------|
| **ONNX** | Layer extraction | Direct support | Layer → trace |
| **PyTorch** | Via ONNX export | Via ONNX export | Via profiling |
| **Chakra** | Layer extraction | Not applicable | Trace format |
| **TFLite** | Layer extraction | Direct support | Not applicable |

**Key challenge:** ONNX provides operator-level info; Timeloop needs loop nests; VIDUR needs request traces.

**Solution:** Multi-level representation with adapters at each level.

### 5.2 Hardware Specification Alignment

| Specification | Timeloop | nn-Meter | VIDUR | ASTRA-sim |
|---------------|----------|----------|-------|-----------|
| **Compute (TFLOPs)** | Explicit | Implicit | Explicit | Explicit |
| **Memory BW (TB/s)** | Explicit | Implicit | Explicit | Explicit |
| **Memory Size (GB)** | Explicit | Implicit | Explicit | Explicit |
| **PE Count** | Explicit | N/A | N/A | N/A |
| **Interconnect** | N/A | N/A | N/A | Explicit |

**Key challenge:** Different tools need different levels of hardware detail.

**Solution:** Hierarchical hardware spec with detail levels (minimal → detailed).

### 5.3 Accuracy Reconciliation

Different backends may give different predictions for the same query.

**Approach:**
1. **Single backend:** Use most appropriate backend for query type
2. **Ensemble:** Average predictions with confidence weighting
3. **Hierarchical:** Use simulation to calibrate analytical/ML models

---

## 6. Recommended Approach

### 6.1 Phased Implementation

#### Phase 1: Unified Data Layer (3 months)

- Implement ONNX-based workload representation
- Create hardware database with common GPU/accelerator specs
- Define unified output format

**Deliverable:** Unified data layer package

#### Phase 2: Core Backends (6 months)

- Integrate Timeloop adapter (analytical, accelerator DSE)
- Integrate nn-Meter adapter (ML-based, edge latency)
- Integrate VIDUR adapter (simulation, LLM serving)

**Deliverable:** Three working backends with unified API

#### Phase 3: Advanced Features (3 months)

- Add ASTRA-sim adapter (distributed training)
- Implement ensemble/hierarchical prediction
- Add uncertainty quantification

**Deliverable:** Full unified predictor with advanced features

#### Phase 4: Community Release (2 months)

- Documentation and tutorials
- Benchmark suite
- CI/CD and packaging

**Deliverable:** Public release

### 6.2 MVP Feature Set

| Feature | Priority | Justification |
|---------|----------|---------------|
| ONNX workload input | P0 | Standard format |
| GPU hardware specs | P0 | Primary target |
| Latency prediction | P0 | Most common query |
| Timeloop backend | P0 | Foundational analytical |
| VIDUR backend | P0 | LLM is key use case |
| nn-Meter backend | P1 | Edge coverage |
| Energy prediction | P1 | Common need |
| Training scenario | P1 | Not just inference |
| Uncertainty | P2 | Nice to have |
| Ensemble | P2 | Advanced feature |

### 6.3 Success Criteria

| Metric | Target |
|--------|--------|
| Prediction accuracy | Within 2x of native tool |
| Setup time | < 10 minutes |
| Query latency | < 5 seconds for typical query |
| Hardware coverage | GPU (NVIDIA), Edge (mobile), Accelerator |
| Workload coverage | CNNs, Transformers, LLMs |

---

## 7. Value Proposition

### 7.1 For Researchers

- **Single interface** - Learn one API, access multiple tools
- **Reproducibility** - Consistent workload/hardware representations
- **Comparison** - Easy to compare modeling approaches
- **Extensibility** - Add new backends without changing user code

### 7.2 For Practitioners

- **Quick estimation** - Fast approximate predictions
- **Hardware selection** - Compare devices without profiling
- **Capacity planning** - Unified interface for system design
- **Cost modeling** - Foundation for deployment cost estimation

### 7.3 For Tool Developers

- **Adoption** - Reach users through unified interface
- **Benchmarking** - Standard comparison framework
- **Collaboration** - Common format enables data sharing

---

## 8. Alternatives Considered

### 8.1 Wrapper-Only Approach

- **Description:** Thin wrappers around existing tools, no unified format
- **Pros:** Lower effort, respects native formats
- **Cons:** Users still need to understand each tool, limited interoperability
- **Verdict:** Insufficient integration for value proposition

### 8.2 Single Model Approach

- **Description:** Train one ML model on all tool outputs
- **Pros:** Single prediction interface, learned integration
- **Cons:** Black box, loses interpretability, needs extensive training data
- **Verdict:** Could be added as optional ensemble layer

### 8.3 Fork/Rewrite Approach

- **Description:** Fork all tools into unified codebase
- **Pros:** Full control, deep integration
- **Cons:** Massive effort, loses upstream improvements, maintenance burden
- **Verdict:** Not practical given resources

---

## 9. Conclusion

A unified ML performance modeling tool is feasible and valuable. The recommended approach is:

1. **Modular architecture** with pluggable backends
2. **Phased implementation** starting with MVP (Timeloop + VIDUR + nn-Meter)
3. **Unified data layer** based on ONNX + hardware database
4. **Community-focused** design for extensibility

**Estimated total effort:** ~28-54 person-months (14-18 months with 2-3 developers)

**Key success factors:**
- Community buy-in from tool maintainers
- Clear value proposition for end users
- Sustainable maintenance model

---

## Appendix: Existing Integration Efforts

### ArchGym

- **Scope:** Connects to simulators for RL-based DSE
- **Relevant:** Architecture exploration focus
- **Gap:** Not focused on prediction accuracy

### Apache TVM

- **Scope:** Compiler with built-in cost models
- **Relevant:** Unified compilation framework
- **Gap:** Compiler-focused, not prediction-focused

### MLCommons

- **Scope:** Standardized ML benchmarks
- **Relevant:** Common workload definitions
- **Gap:** Benchmarking, not prediction

---

*Analysis by Leo | ML Performance Survey Project*
