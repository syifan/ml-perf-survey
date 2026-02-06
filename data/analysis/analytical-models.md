# Deep Analysis: Analytical Performance Models for DNN Accelerators

This document provides detailed analysis of foundational analytical performance modeling frameworks for DNN accelerators.

---

## 1. Timeloop (ISPASS 2019)

**Full Title:** Timeloop: A Systematic Approach to DNN Accelerator Evaluation

**Authors:** Parashar, Rhu, Mukkara, Puglielli, Venkatesan, Khailany, Emer, Keckler (NVIDIA, MIT)

### Core Methodology

Timeloop is an analytical framework for exploring the design space of DNN accelerators. It decouples the specification of:
1. **Architecture** - Hardware resources (PEs, memory hierarchy, interconnects)
2. **Mapping** - How computations and data are scheduled onto hardware
3. **Problem** - The DNN workload (layer shapes, tensor dimensions)

The framework uses a **loop-nest representation** where each level of the memory hierarchy corresponds to a loop in a nested loop program. This abstraction enables systematic enumeration of valid mappings.

### Key Components

| Component | Description |
|-----------|-------------|
| **Architecture Specification** | YAML-based description of memory levels, sizes, bandwidth, energy per access |
| **Mapspace** | The space of all valid mappings for a given architecture-problem pair |
| **Mapper** | Exhaustive/heuristic search through mapspace |
| **Model** | Analytical equations computing latency, energy, utilization |

### Performance Model

The analytical model computes:

1. **Data Reuse Analysis** - For each tensor (weights, inputs, outputs) at each memory level, compute:
   - Working set size
   - Number of accesses
   - Temporal and spatial reuse factors

2. **Latency Estimation**
   - Compute cycles = Total MACs / (PEs × utilization)
   - Memory stalls based on bandwidth constraints

3. **Energy Estimation**
   - Energy = Σ (accesses_i × energy_per_access_i) for each memory level
   - Includes compute energy (MAC operations)

### Accuracy Claims

- **Validation against RTL:** Within 5-10% of cycle-accurate simulation for regular workloads
- **Speed:** 2000x faster than cycle-accurate simulation
- **Scope:** Primarily targets systolic array and spatial architectures

### Input Requirements

| Requirement | Level |
|-------------|-------|
| Architecture specification | Required (detailed YAML) |
| Layer dimensions | Required |
| Dataflow/mapping | Searched or specified |
| Runtime profiling | Not required |

### Strengths

1. **Systematic design space exploration** - Can evaluate millions of mappings
2. **Decoupled specification** - Architecture, mapping, and problem are independent
3. **Open source** - Widely adopted in academia (GitHub: NVlabs/timeloop)
4. **Extensible** - Supports custom architectures and constraints
5. **Energy-aware** - Models both compute and memory energy

### Limitations

1. **Regular workloads only** - Original Timeloop assumes dense tensors
2. **Idealized memory model** - Assumes perfect memory scheduling
3. **No dynamic effects** - Does not model runtime variations, contention
4. **Architecture expertise required** - Detailed specs needed
5. **Limited to single accelerator** - No distributed/multi-chip modeling

### Reproducibility

**Level: Full**
- Code: https://github.com/NVlabs/timeloop
- Documentation: Extensive tutorials and examples
- Community: Active development, used in 100+ papers

---

## 2. MAESTRO (MICRO 2019)

**Full Title:** MAESTRO: A Data-Centric Approach to Understand Reuse, Performance, and Hardware Cost of DNN Mappings

**Authors:** Kwon, Chatarasi, Sarber, Prasad, Patel, Krishna (Georgia Tech)

### Core Methodology

MAESTRO takes a **data-centric** perspective on DNN accelerator modeling. Instead of loop-nest transformations, it models performance through **data reuse analysis** using a compact **dataflow directives** notation.

The key insight is that different dataflows (row stationary, weight stationary, output stationary) can be uniformly described by specifying how data tiles are distributed spatially and temporally.

### Key Components

| Component | Description |
|-----------|-------------|
| **MAESTRO DSL** | Domain-specific language for describing dataflows |
| **Data Reuse Analysis** | Compute reuse factors for each tensor type |
| **Cost Model** | Analytical equations for latency, energy, area |
| **Design Space Exploration** | Automated search for optimal configurations |

### Dataflow Representation

MAESTRO uses **mapping directives** to describe dataflows:

```
Dataflow {
  TemporalMap(K, K) C;    // Map input channels temporally
  SpatialMap(Y, 1) R;     // Map output rows spatially
  TemporalMap(X, X) S;    // Map output columns temporally
  ...
}
```

This representation is more intuitive than loop-nest notation and directly captures data movement patterns.

### Performance Model

1. **Reuse Distance Analysis** - Compute how often each data element is reused
2. **Traffic Analysis** - Calculate bytes transferred at each memory level
3. **Latency Model**
   - L = max(compute_cycles, memory_cycles)
   - Accounts for compute-memory overlap
4. **Energy Model**
   - E = Σ (traffic_i × energy_per_byte_i) + compute_energy

### Accuracy Claims

- **Validation:** Matches RTL simulation within 5-15% for regular CNNs
- **Speed:** Orders of magnitude faster than simulation
- **Comparison:** Results correlate with Timeloop outputs

### Input Requirements

| Requirement | Level |
|-------------|-------|
| Architecture parameters | Required (PE count, buffer sizes) |
| Layer dimensions | Required |
| Dataflow directive | Required (or use templates) |
| Runtime profiling | Not required |

### Strengths

1. **Intuitive dataflow notation** - Easier to understand than loop-nests
2. **Data-centric analysis** - Directly reasons about data movement
3. **Fast exploration** - Analytical model enables rapid DSE
4. **Open source** - Available for research use
5. **Layer fusion support** - Can model fused operators

### Limitations

1. **Dense workloads** - Original version does not handle sparsity
2. **Coarse-grained modeling** - Some microarchitectural details abstracted
3. **Limited memory hierarchy** - Simpler than real accelerators
4. **No network modeling** - Single accelerator focus

### Comparison with Timeloop

| Aspect | Timeloop | MAESTRO |
|--------|----------|---------|
| Representation | Loop-nest | Data-centric directives |
| Granularity | More detailed | More abstract |
| Ease of use | Steeper learning curve | More intuitive |
| Extensibility | Highly extensible | Moderate |
| Sparse support | Via Sparseloop | Limited |

### Reproducibility

**Level: Full**
- Code: https://github.com/maestro-project/maestro
- Documentation: Available with examples
- Community: Active academic use

---

## 3. Eyeriss (ISCA 2016)

**Full Title:** Eyeriss: A Spatial Architecture for Energy-Efficient Dataflow for Convolutional Neural Networks

**Authors:** Chen, Emer, Sze (MIT)

### Core Methodology

Eyeriss introduces the **row stationary (RS)** dataflow for CNN accelerators. While primarily a hardware architecture paper, it establishes foundational analytical modeling concepts for understanding energy efficiency in DNN accelerators.

The paper provides an **energy cost taxonomy** that has become standard for comparing DNN accelerator dataflows.

### Key Contributions

1. **Row Stationary Dataflow** - Maximizes data reuse by keeping filter rows stationary in local registers
2. **Energy Cost Hierarchy** - Quantifies energy for different memory access types
3. **Dataflow Comparison Framework** - Methodology for comparing accelerator efficiency

### Energy Cost Model

Eyeriss establishes the following energy hierarchy (45nm):

| Operation | Energy (pJ) | Relative Cost |
|-----------|-------------|---------------|
| MAC operation | 1 | 1x |
| Register file access | 1 | 1x |
| PE array access | 2 | 2x |
| Global buffer access | 6 | 6x |
| DRAM access | 200 | 200x |

Key insight: **DRAM access costs 200x more than a MAC operation**, making memory hierarchy design critical.

### Dataflow Classification

Eyeriss categorizes dataflows by which tensor type is kept stationary:

| Dataflow | Stationary Data | Best For |
|----------|-----------------|----------|
| Weight Stationary | Weights | Large batch inference |
| Output Stationary | Partial sums | Depthwise convolutions |
| Row Stationary | Filter rows | General CNNs |
| No Local Reuse | None | Memory-bound workloads |

### Analytical Insights

The paper derives analytical expressions for:

1. **Global buffer accesses** per layer
2. **DRAM accesses** for each dataflow
3. **Energy breakdown** by operation type

These become the foundation for later tools like Timeloop and MAESTRO.

### Accuracy Claims

- **Silicon validation:** Measured on 65nm ASIC
- **Energy prediction:** Within 10% of chip measurements
- **Performance:** 35 fps on AlexNet at 278mW

### Strengths

1. **Foundational work** - Established vocabulary for DNN accelerator analysis
2. **Energy hierarchy** - Quantified the cost of data movement
3. **Dataflow taxonomy** - Systematic comparison framework
4. **Silicon-validated** - Real chip measurements

### Limitations

1. **CNN-focused** - Designed for convolutional layers
2. **Fixed architecture** - Analysis tied to specific design
3. **Dense only** - No sparsity support
4. **Single-chip** - No distributed modeling

### Reproducibility

**Level: Partial**
- No public simulator (concepts integrated into Timeloop)
- Chip design principles well documented
- Energy numbers widely cited

---

## 4. Comparative Analysis

### Methodology Comparison

| Aspect | Eyeriss | Timeloop | MAESTRO |
|--------|---------|----------|---------|
| Year | 2016 | 2019 | 2019 |
| Primary Focus | Architecture | DSE Framework | Cost Modeling |
| Representation | Dataflow taxonomy | Loop-nest | Data-centric |
| Scope | Single CNN accelerator | General spatial accelerators | General dataflows |
| Energy Model | Empirical hierarchy | Parameterized model | Analytical |
| Validation | Silicon measurements | RTL simulation | Cross-validation |

### Evolution of Analytical Modeling

```
Eyeriss (2016)                    MAESTRO (2019)
    │                                   │
    │ Established energy               │ Data-centric
    │ hierarchy and                    │ representation
    │ dataflow taxonomy                │
    │                                   │
    └──────────────┬───────────────────┘
                   │
                   ▼
             Timeloop (2019)
                   │
    Unified loop-nest framework
    combining architecture,
    mapping, and workload
                   │
                   ▼
            Sparseloop (2022)
                   │
    Extended to sparse tensors
    with compression formats
```

### Accuracy vs. Speed Trade-off

| Tool | Typical Error | Speed vs. RTL Sim | Use Case |
|------|---------------|-------------------|----------|
| Eyeriss model | ~10% | 1000x+ | Single design analysis |
| Timeloop | 5-10% | 2000x | Design space exploration |
| MAESTRO | 5-15% | 1000x+ | Rapid dataflow comparison |

### Common Assumptions and Limitations

All three analytical frameworks share certain assumptions:

1. **Deterministic execution** - No modeling of runtime variability
2. **Perfect memory scheduling** - Assumes ideal memory controller
3. **Regular workloads** - Limited support for dynamic shapes
4. **Single accelerator** - No distributed system modeling
5. **Layer-by-layer** - Limited fusion/scheduling across layers

---

## 5. Key Takeaways for Survey

### What Analytical Models Excel At

1. **Rapid design space exploration** - Evaluate millions of configurations
2. **Energy-efficiency analysis** - Accurate memory energy modeling
3. **Dataflow optimization** - Finding optimal data reuse patterns
4. **Hardware-software co-design** - Joint optimization of arch + mapping

### Gaps Addressed by Other Approaches

| Gap | ML-Based Approach | Simulation Approach |
|-----|-------------------|---------------------|
| Dynamic runtime effects | Learn from profiling data | Model contention, scheduling |
| Irregular/sparse workloads | Data-driven generalization | Detailed sparse execution |
| Cross-platform prediction | Transfer learning | Platform-specific simulation |
| End-to-end system modeling | Holistic regression | Full-system simulation |

### Papers Building on These Foundations

| Paper | Year | Extension |
|-------|------|-----------|
| Sparseloop | 2022 | Sparse tensor support for Timeloop |
| Interstellar | 2020 | Auto-mapper for Timeloop |
| CoSA | 2021 | Constrained optimization for mappings |
| dMazeRunner | 2020 | Multi-layer scheduling |
| GAMMA | 2022 | GNN-based mapping search |

---

## 6. References

1. Chen, Y.-H., Emer, J., & Sze, V. (2016). Eyeriss: A Spatial Architecture for Energy-Efficient Dataflow for Convolutional Neural Networks. ISCA.

2. Parashar, A., et al. (2019). Timeloop: A Systematic Approach to DNN Accelerator Evaluation. ISPASS.

3. Kwon, H., et al. (2019). MAESTRO: A Data-Centric Approach to Understand Reuse, Performance, and Hardware Cost of DNN Mappings. MICRO.

4. Wu, Y.-N., Sze, V., & Emer, J. (2022). Sparseloop: An Analytical Approach to Sparse Tensor Accelerator Modeling. MICRO.

---

*Analysis by Leo | ML Performance Survey Project*
