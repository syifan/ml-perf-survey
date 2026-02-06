# Deep Analysis: Simulation-Based Performance Models for ML Workloads

This document provides detailed analysis of simulation-based performance modeling frameworks for ML/DNN workloads.

---

## 1. ASTRA-sim (arXiv 2023, ISPASS 2020)

**Full Title:** ASTRA-sim: Enabling SW/HW Co-Design Exploration for Distributed DL Training Platforms

**Authors:** Won et al. (Georgia Tech, Meta, Intel, AMD)

### Core Methodology

ASTRA-sim is an **end-to-end distributed ML training simulator** that models the full stack: compute, memory, and network. It enables design space exploration for distributed training systems by simulating the interaction between collective communication, compute, and memory subsystems.

The framework uses a **modular architecture** separating:
1. **Workload Layer** - DNN model execution (Chakra execution traces)
2. **System Layer** - Collective communication algorithms, parallelism strategies
3. **Network Layer** - Topology simulation (analytical or NS-3/Garnet backend)

### Key Components

| Component | Description |
|-----------|-------------|
| **Chakra Execution Traces** | Standardized format for representing distributed workloads |
| **Collective Communication** | Ring, tree, halving-doubling all-reduce implementations |
| **Network Backends** | Analytical, NS-3, Garnet2.0 for different fidelity |
| **Parallelism Strategies** | Data parallel, model parallel, pipeline parallel |

### Performance Model

ASTRA-sim models performance through discrete-event simulation:

1. **Compute Time** - From execution traces or analytical model
   - Can inject real profiled compute times
   - Or use roofline-based analytical estimates

2. **Communication Time** - Network simulation
   - Collective decomposition into point-to-point messages
   - Network contention and congestion modeling
   - Support for hierarchical collectives (intra-node + inter-node)

3. **Memory Time** - Memory bandwidth constraints
   - Tensor movement between accelerators and memory
   - Offloading and prefetching effects

### Accuracy Claims

| Metric | Claim | Validation |
|--------|-------|------------|
| End-to-end training time | 5-15% error | Validated against real clusters |
| Communication breakdown | <10% error | Compared to NCCL traces |
| Scaling trends | Captures inflection points | Multi-GPU/node scaling |

### Input Requirements

| Requirement | Level |
|-------------|-------|
| Workload traces (Chakra) | Required |
| Network topology | Required |
| Collective algorithms | Required |
| Compute timing | Required (profiled or analytical) |
| Memory hierarchy | Optional (for detailed modeling) |

### Strengths

1. **End-to-end simulation** - Covers compute, memory, and network holistically
2. **Modular backends** - Trade off speed vs. accuracy with network backend choice
3. **Distributed focus** - Unlike Timeloop/MAESTRO, targets multi-device systems
4. **Open source** - Available at https://github.com/astra-sim/astra-sim
5. **Chakra traces** - Standardized workload representation enables reproducibility

### Limitations

1. **Trace-driven** - Requires upfront trace collection or generation
2. **Network-centric** - Compute modeling is coarse compared to Timeloop
3. **Simulation speed** - Slower than analytical models (but faster than cycle-accurate)
4. **Collective library** - Assumes specific collective implementations

### Reproducibility

**Level: Full**
- Code: https://github.com/astra-sim/astra-sim
- Traces: Chakra format with example traces
- Documentation: Extensive tutorials
- Community: Active development, industry adoption

---

## 2. GPGPU-Sim / Accel-Sim (Various, 2009-2021)

**Full Title:** GPGPU-Sim: A GPU Simulator / Accel-Sim: Enabling GPGPU Research

**Authors:** Bakhoda et al. (UBC) / Khairy et al. (Purdue)

### Core Methodology

**GPGPU-Sim** is a cycle-accurate GPU simulator that models NVIDIA GPU architectures. **Accel-Sim** extends it with trace-driven simulation and correlation with real hardware for modern GPUs (Turing, Ampere).

The simulator models:
1. **SIMT Core** - Warp scheduling, scoreboard, register file, operand collectors
2. **Memory System** - L1/L2 caches, memory partitions, DRAM controller
3. **Interconnect** - On-chip network between cores and memory

### Key Components

| Component | Description |
|-----------|-------------|
| **PTX/SASS Frontend** | Can run PTX directly or SASS traces |
| **Timing Model** | Cycle-accurate SIMT core simulation |
| **Memory Model** | Detailed cache hierarchy with MSHR, coalescing |
| **Power Model** | GPUWattch for power estimation |

### Simulation Modes

1. **Functional Simulation** - Fast execution, no timing
2. **Timing Simulation** - Cycle-accurate, ~1000x slowdown vs. real GPU
3. **Trace-Driven (Accel-Sim)** - Faster simulation from SASS traces

### Accuracy Claims

| GPU Generation | IPC Correlation | Notes |
|----------------|-----------------|-------|
| Fermi/Kepler | ~0.95 | Well-tuned configurations |
| Volta | ~0.97 | Accel-Sim tuned configs |
| Turing | ~0.90 | Tensor core modeling added |
| Ampere | ~0.85-0.90 | Active development |

Error for DNN workloads: **10-20%** on kernel execution time.

### Input Requirements

| Requirement | Level |
|-------------|-------|
| GPU configuration | Required (detailed arch params) |
| Application binary | Required (PTX or SASS) |
| CUDA runtime | Intercepted at runtime |
| Hardware validation | Recommended for tuning |

### Strengths

1. **Cycle-accurate** - Highest fidelity GPU simulation
2. **Widely adopted** - Most-cited GPU simulator in academia
3. **Microarchitecture details** - Models warp scheduling, bank conflicts, etc.
4. **Power modeling** - GPUWattch integration
5. **Open source** - Large community, active development

### Limitations

1. **Simulation speed** - Very slow (~1000x-10000x slowdown)
2. **Configuration effort** - Tuning for accuracy requires hardware access
3. **Functional correctness** - Some CUDA features not fully supported
4. **DNN library support** - cuDNN/cuBLAS require special handling

### Reproducibility

**Level: Full (with caveats)**
- Code: https://github.com/gpgpu-sim/gpgpu-sim_distribution
- Code: https://github.com/accel-sim/accel-sim-framework
- Configs: Available for multiple GPU generations
- Challenge: Accuracy depends on configuration tuning

---

## 3. gem5 + ML Extensions

**Full Title:** gem5: A Modular Platform for System Architecture Research

**Authors:** Binkert et al. (Multiple institutions)

### Core Methodology

**gem5** is a modular full-system simulator supporting multiple ISAs (x86, ARM, RISC-V). For ML workloads, gem5 can be used:

1. **CPU-based inference** - Full simulation of ML on CPU
2. **Accelerator modeling** - Custom accelerator integration (gem5-Aladdin, SMAUG)
3. **System studies** - Memory hierarchy, coherence for ML

### ML-Specific Extensions

| Extension | Focus | Approach |
|-----------|-------|----------|
| **gem5-Aladdin** | Accelerator DSE | Integrates Aladdin accelerator models |
| **SMAUG** | DNN accelerators | End-to-end DNN simulation |
| **gem5-GPU** | CPU-GPU systems | Heterogeneous system simulation |
| **gem5 + SST** | Large-scale | Parallel simulation with SST |

### Performance Model

gem5 provides multiple CPU models with different speed/accuracy trade-offs:

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| AtomicSimple | Fast | Low | Functional validation |
| TimingSimple | Medium | Medium | Memory studies |
| O3 (Out-of-Order) | Slow | High | Microarchitecture studies |
| KVM | Near-native | Functional only | Fast-forward |

### Accuracy Claims

For CPU-based ML inference:
- **Cycle accuracy:** Within 10-20% of real hardware (tuned O3 model)
- **Memory behavior:** Accurate cache miss rates, DRAM traffic
- **Power:** Can integrate with McPAT for power estimation

### Input Requirements

| Requirement | Level |
|-------------|-------|
| ISA specification | Required |
| CPU configuration | Required |
| Memory hierarchy | Required |
| Workload binary | Required (statically linked) |

### Strengths

1. **Full-system simulation** - OS, memory coherence, I/O
2. **Multiple ISAs** - x86, ARM, RISC-V support
3. **Extensibility** - Modular design for custom components
4. **Large community** - Academic standard for architecture research
5. **Parallel simulation** - dist-gem5 for large systems

### Limitations

1. **CPU-focused** - GPU/accelerator support less mature
2. **Simulation speed** - Slow for large ML models
3. **DNN library support** - Challenging to run optimized libraries
4. **Configuration complexity** - Steep learning curve

### Reproducibility

**Level: Full**
- Code: https://github.com/gem5/gem5
- Documentation: Extensive
- Community: Very active, annual workshops
- Configs: Many reference configurations available

---

## 4. VIDUR (MLSys 2024)

**Full Title:** VIDUR: A Large-Scale Simulation Framework For LLM Inference

**Authors:** Agrawal et al. (Microsoft Research)

### Core Methodology

VIDUR is a **discrete-event simulator** specifically designed for LLM inference serving. It simulates the entire serving stack:

1. **Request arrival** - Poisson or trace-driven arrival patterns
2. **Scheduler** - Various scheduling policies (FCFS, SJF, ORCA, etc.)
3. **Execution Engine** - Models prefill and decode phases
4. **Memory Management** - KV cache allocation, paging (PagedAttention)

### Key Components

| Component | Description |
|-----------|-------------|
| **Execution Model** | Separates prefill (compute-bound) and decode (memory-bound) |
| **KV Cache** | Models memory allocation, eviction, paging |
| **Batching** | Continuous batching, iteration-level scheduling |
| **Hardware Model** | GPU memory bandwidth, compute throughput |

### Performance Model

VIDUR models LLM inference through:

1. **Prefill Time** - Compute-bound, scales with prompt length
   - T_prefill = prompt_tokens * compute_per_token / compute_throughput

2. **Decode Time** - Memory-bound, per-token generation
   - T_decode = model_size / memory_bandwidth (per token)

3. **Scheduling Overhead** - Batching decisions, memory management

4. **Queuing Delays** - Request queuing under load

### Accuracy Claims

| Metric | Error | Validation Method |
|--------|-------|-------------------|
| Request latency | <5% | vs. vLLM measurements |
| Time-to-first-token | <5% | vs. production traces |
| Throughput | <5% | vs. real GPU serving |
| Queue lengths | <10% | vs. simulation ground truth |

### Input Requirements

| Requirement | Level |
|-------------|-------|
| Model architecture | Required (layer configs) |
| GPU specifications | Required (memory, bandwidth) |
| Request traces | Required (prompt/generation lengths) |
| Scheduling policy | Required |
| KV cache config | Required |

### Strengths

1. **LLM-specific** - Captures prefill/decode asymmetry
2. **Production-relevant** - Models real serving concerns (queuing, batching)
3. **Fast simulation** - Discrete-event, not cycle-accurate
4. **Scheduling focus** - Compare scheduler algorithms at scale
5. **Memory modeling** - KV cache paging, eviction

### Limitations

1. **Abstracted execution** - No microarchitecture modeling
2. **Single GPU focus** - Limited distributed inference support
3. **Operator-level** - Doesn't model kernel-level details
4. **Calibration required** - Needs profiled timing data

### Reproducibility

**Level: Full**
- Code: https://github.com/microsoft/vidur
- Documentation: Good examples
- Traces: Sample request traces included
- Configs: Multiple model/GPU configurations

---

## 5. TrioSim (ISCA 2025)

**Full Title:** TrioSim: A Multi-GPU Simulator for DNN Training and Inference

**Authors:** Various (Industry/Academia)

### Core Methodology

TrioSim extends GPU simulation to **multi-GPU systems** for DNN workloads. It models:

1. **Single GPU** - Built on GPGPU-Sim/Accel-Sim foundations
2. **Inter-GPU communication** - NVLink, PCIe modeling
3. **Collective operations** - NCCL-like all-reduce, all-gather
4. **Training workloads** - Forward, backward, gradient sync

### Key Components

| Component | Description |
|-----------|-------------|
| **GPU Cores** | Accel-Sim-based timing model |
| **Memory System** | HBM modeling with bandwidth constraints |
| **Interconnect** | NVLink topology simulation |
| **Collectives** | Ring/tree all-reduce implementations |

### Performance Model

TrioSim simulates multi-GPU training through:

1. **Compute Phase** - Per-GPU kernel execution (Accel-Sim)
2. **Communication Phase** - Collective operation simulation
3. **Overlap** - Compute-communication overlap modeling
4. **Synchronization** - Barrier and dependency tracking

### Accuracy Claims

| Configuration | Error vs. Real Hardware |
|---------------|-------------------------|
| 2-GPU training | ~15% |
| 4-GPU training | ~20% |
| 8-GPU training | ~25% |

### Input Requirements

| Requirement | Level |
|-------------|-------|
| GPU configuration | Required |
| Interconnect topology | Required |
| DNN model | Required (trace or description) |
| Parallelism strategy | Required |

### Strengths

1. **Multi-GPU** - Only simulator targeting multi-GPU DNN at scale
2. **Cycle-accurate cores** - High-fidelity GPU modeling
3. **Communication modeling** - NVLink, collective operations
4. **Training workloads** - Forward and backward pass

### Limitations

1. **Simulation speed** - Very slow for large systems
2. **Scalability** - Challenging beyond 8 GPUs
3. **Early stage** - Less mature than single-GPU simulators
4. **Collective accuracy** - NCCL behavior hard to replicate exactly

### Reproducibility

**Level: Partial**
- Code: Available (check paper for link)
- Documentation: Limited
- Configs: Basic multi-GPU setups

---

## 6. Comparative Analysis

### Simulation Approach Comparison

| Simulator | Target | Granularity | Speed | Accuracy |
|-----------|--------|-------------|-------|----------|
| GPGPU-Sim/Accel-Sim | Single GPU | Cycle-accurate | Very slow | 85-97% correlation |
| gem5 | CPU/System | Cycle-accurate | Slow | 80-90% |
| ASTRA-sim | Distributed | Event-driven | Medium | 85-95% |
| VIDUR | LLM Serving | Event-driven | Fast | 95%+ |
| TrioSim | Multi-GPU | Cycle-accurate | Very slow | 75-85% |

### Use Case Matrix

| Use Case | Best Simulator | Rationale |
|----------|----------------|-----------|
| Single GPU kernel optimization | GPGPU-Sim/Accel-Sim | Cycle-accurate details |
| Distributed training DSE | ASTRA-sim | Fast network exploration |
| LLM serving evaluation | VIDUR | Production-relevant metrics |
| Multi-GPU system design | TrioSim | Full-system fidelity |
| CPU inference | gem5 | Full-system, ISA support |

### Accuracy vs. Speed Trade-off

```
                    Accuracy
                       ^
                       |
    Cycle-Accurate ----+---- GPGPU-Sim
                       |         TrioSim
                       |              gem5
                       |
    Event-Driven  -----+------------ ASTRA-sim
                       |                  VIDUR
                       |
    Analytical    -----+----------------------- Timeloop
                       |                             MAESTRO
                       +---------------------------------> Speed
                       Slow                           Fast
```

### Common Simulation Challenges

All simulation-based approaches face:

1. **Scalability** - Simulation time grows with system size
2. **Calibration** - Requires real hardware for validation
3. **Library support** - Hard to simulate optimized CUDA/cuDNN
4. **Workload generation** - Trace collection or model creation
5. **Configuration space** - Many parameters to tune

---

## 7. Integration with Analytical and ML-Based Models

### Hybrid Approaches

Several frameworks combine simulation with other techniques:

| Framework | Simulation | Analytical | ML-Based |
|-----------|------------|------------|----------|
| **ArchGym** | Connects to simulators | - | RL for DSE |
| **TAO** | Microarch simulation | - | Transfer learning |
| **ASTRA-sim** | Network simulation | Compute estimation | - |
| **Timeloop** | - | Core model | Uses ML mapper |

### When to Use Simulation

**Use Simulation When:**
- Microarchitectural details matter (cache behavior, scheduling)
- Validating analytical model assumptions
- Exploring new architectures without hardware
- Debugging system-level issues

**Avoid Simulation When:**
- Rapid design space exploration needed
- Only high-level trends required
- Real hardware profiling is feasible
- Time budget is limited

---

## 8. Key Takeaways for Survey

### What Simulation Models Excel At

1. **Microarchitecture insights** - Details not captured by analytical models
2. **System-level interactions** - Memory hierarchy, network contention
3. **What-if analysis** - Explore configurations without hardware
4. **Debugging/validation** - Verify performance expectations

### Gaps Addressed by Other Approaches

| Gap | Analytical Approach | ML-Based Approach |
|-----|---------------------|-------------------|
| Speed | 1000x+ faster | Real-time prediction |
| Scalability | Handles large designs | Generalizes across workloads |
| Ease of use | Simpler setup | Data-driven |
| New architectures | Quick specification | Transfer learning |

### Evolution of Simulation for ML

```
Traditional HPC Simulation (pre-2010)
           |
           v
GPGPU-Sim for CUDA workloads (2009-2015)
           |
           v
DNN-specific extensions (2015-2020)
           |
           +--- Accel-Sim (improved correlation)
           |
           +--- ASTRA-sim (distributed focus)
           |
           +--- VIDUR (LLM serving)
           |
           v
Multi-GPU/Large-Scale (2020-present)
           |
           +--- TrioSim (multi-GPU training)
           |
           +--- Integration with ML-based models
```

### Recommendations for Survey

1. **Position simulation as validation tool** - Complements analytical/ML approaches
2. **Highlight ASTRA-sim for distributed** - Most practical for distributed training
3. **VIDUR for LLM serving** - Only targeted framework for serving
4. **Acknowledge speed limitations** - But emphasize unique insights

---

## 9. References

1. Won, W., et al. (2023). ASTRA-sim: Enabling SW/HW Co-Design Exploration for Distributed DL Training Platforms. arXiv.

2. Bakhoda, A., et al. (2009). Analyzing CUDA Workloads Using a Detailed GPU Simulator. ISPASS.

3. Khairy, M., et al. (2020). Accel-Sim: An Extensible Simulation Framework for Validated GPU Modeling. ISCA.

4. Binkert, N., et al. (2011). The gem5 Simulator. ACM SIGARCH Computer Architecture News.

5. Agrawal, A., et al. (2024). VIDUR: A Large-Scale Simulation Framework For LLM Inference. MLSys.

6. Various. (2025). TrioSim: A Multi-GPU Simulator for DNN Training and Inference. ISCA.

---

*Analysis by Leo | ML Performance Survey Project*
