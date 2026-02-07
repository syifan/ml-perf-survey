# Comprehensive Comparison Tables for ML Performance Models

This document provides structured comparison tables for the survey paper, covering papers by target hardware, accuracy comparison, training cost comparison, and transfer learning approaches.

---

## 1. Papers by Target Hardware

### Table 1.1: Analytical Models by Hardware Target

| Paper | Year | Hardware Target | Technique | Accuracy | Key Contribution |
|-------|------|-----------------|-----------|----------|------------------|
| Eyeriss | 2016 | CNN Accelerator (ASIC) | Energy cost hierarchy | ~10% vs. silicon | Dataflow taxonomy, RS dataflow |
| Timeloop | 2019 | Spatial accelerators | Loop-nest analysis | 5-10% vs. RTL | Systematic design space exploration |
| MAESTRO | 2019 | DNN accelerators | Data-centric directives | 5-15% vs. RTL | Intuitive dataflow notation |
| Sparseloop | 2022 | Sparse accelerators | Extended loop-nest | 5-10% vs. RTL | Sparse tensor support |

### Table 1.2: Simulation-Based Models by Hardware Target

| Paper | Year | Hardware Target | Technique | Accuracy | Key Contribution |
|-------|------|-----------------|-----------|----------|------------------|
| GPGPU-Sim | 2009 | NVIDIA GPUs (Fermi-Kepler) | Cycle-accurate sim | 0.95 IPC correlation | GPU microarchitecture simulation |
| Accel-Sim | 2020 | NVIDIA GPUs (Volta-Ampere) | Trace-driven sim | 0.85-0.97 IPC corr | Modern GPU correlation |
| gem5 | 2011 | CPU (x86, ARM, RISC-V) | Full-system sim | 10-20% cycle error | Multi-ISA support |
| ASTRA-sim | 2023 | Distributed GPU clusters | Event-driven sim | 5-15% end-to-end | Distributed training DSE |
| VIDUR | 2024 | GPU (LLM serving) | Discrete-event sim | <5% latency error | LLM serving simulation |
| TrioSim | 2025 | Multi-GPU systems | Cycle-accurate sim | 15-25% error | Multi-GPU training |

### Table 1.3: ML-Based Models by Hardware Target

| Paper | Year | Hardware Target | Technique | Accuracy | Key Contribution |
|-------|------|-----------------|-----------|----------|------------------|
| nn-Meter | 2021 | Edge devices (mobile CPU/GPU/VPU) | MLP per kernel | 97.8-99.0% | Kernel-level decomposition |
| AutoTVM | 2018 | Multi (CPU, GPU, accelerators) | XGBoost regression | ~20% MAPE | Compiler cost model |
| Ansor | 2020 | Multi (CPU, GPU, accelerators) | MLP on AST features | ~15% MAPE | Hierarchical search |
| HELP | 2021 | Multi (via meta-learning) | GNN + meta-learning | 93.2-98.1% | Few-shot hardware adaptation |
| LitePred | 2024 | 85 edge platforms | VAE + MLP | 98.5-99.3% | Cross-platform transfer |
| TLP | 2023 | GPU/CPU | Transformer encoder | ~12% MAPE | Attention for programs |
| NeuSight | 2025 | GPU (including LLMs) | Roofline + neural | 97.7% | Tile-based prediction |

### Table 1.4: LLM Inference Systems by Focus Area

| Paper | Year | Hardware Target | Technique | Improvement | Key Contribution |
|-------|------|-----------------|-----------|-------------|------------------|
| Orca | 2022 | GPU | Continuous batching | 36.9x throughput | Iteration-level scheduling |
| vLLM | 2023 | NVIDIA GPUs | PagedAttention | 2-4x throughput | Virtual memory for KV cache |
| FlashAttention | 2022 | NVIDIA GPUs | IO-aware attention | 2-4x speed, 10-20x lower memory use | Linear memory attention |
| FlashAttention-2 | 2024 | A100 GPUs | Optimized parallelism | 2x vs. FA1 | 73% A100 utilization |
| FlashAttention-3 | 2024 | H100 GPUs | Warp specialization + FP8 | 1.5-2x vs. FA2 | 75-85% H100 utilization |
| DistServe | 2024 | Multi-GPU | Prefill-decode disaggregation | 7.4x request rate | Phase separation |
| Sarathi-Serve | 2024 | GPU | Chunked prefills | 25% throughput | Stall-free decode |
| MEDUSA | 2024 | GPU | Parallel decode heads | 2.2-3.6x speed | Draft-free speculation |

---

## 2. Accuracy Comparison

### Table 2.1: Accuracy by Modeling Approach

| Approach | Representative Paper | Accuracy Metric | Value | Validation Method |
|----------|---------------------|-----------------|-------|-------------------|
| Analytical | Timeloop | vs. RTL simulation | 5-10% error | Cycle-accurate RTL |
| Analytical | MAESTRO | vs. RTL simulation | 5-15% error | Cross-validation |
| Simulation | GPGPU-Sim | IPC correlation | 0.95 | Real GPU measurements |
| Simulation | Accel-Sim | IPC correlation | 0.85-0.97 | Modern GPU traces |
| Simulation | VIDUR | Latency error | <5% | vLLM measurements |
| ML-Based | nn-Meter | Latency accuracy | 97.8-99.0% | Edge device profiling |
| ML-Based | LitePred | Latency accuracy | 98.5-99.3% | 85 platform evaluation |
| ML-Based | HELP | Latency accuracy | 93.2-98.1% | Cross-hardware transfer |
| Hybrid | NeuSight | Latency accuracy | 97.7% | GPU profiling |
| Hybrid | Roofline-LLM | ΔR-squared vs. analytical | +17 points vs. pure analytical | LLM profiling |

### Table 2.2: Accuracy vs. Generality Trade-off

_Note: Accuracy column shows estimated (1 - error) or reported accuracy percentages for comparability across different metrics._

| Paper | Accuracy (est.) | Hardware Scope | Workload Scope | Generality Score |
|-------|-----------------|----------------|----------------|------------------|
| nn-Meter | 99.0% | 4 edge platforms | CNNs | Narrow |
| LitePred | 99.3% | 85 edge platforms | CNNs | Medium |
| HELP | 98.1% | Multi (meta-learned) | NAS search spaces | Medium |
| Ansor | ~85% (15% MAPE) | CPU, GPU, accelerators | Tensor programs | Broad |
| Timeloop | ~92.5% (7.5% avg error) | Spatial accelerators | DNN layers | Medium |
| ASTRA-sim | ~90% (10% avg error) | Distributed clusters | DL training | Narrow-Medium |

### Table 2.3: Accuracy by Workload Type

| Workload Type | Best Paper | Accuracy | Notes |
|---------------|------------|----------|-------|
| CNN inference (edge) | nn-Meter, LitePred | 99%+ | Kernel-level decomposition |
| CNN inference (GPU) | NeuSight | 97.7% | Tile-based prediction |
| Tensor programs | Ansor, TLP | 85-88% | Compiler integration |
| Distributed training | ASTRA-sim | 85-95% | Network-aware simulation |
| LLM inference | VIDUR | <5% error | Discrete-event simulation |
| LLM attention | FlashAttention-3 | 75-85% utilization | Hardware-optimal |

---

## 3. Training Cost Comparison

### Table 3.1: Training Data Requirements

| Paper | Pre-training Data | Per-Device Adaptation | Total Samples | Collection Method |
|-------|-------------------|----------------------|---------------|-------------------|
| nn-Meter | None | ~1000 samples/kernel type | 10K-50K | Automated profiling |
| LitePred | 85 platforms (full) | ~100 samples | 100-500 | VAE-guided sampling |
| HELP | Multiple platforms | 10-100 samples | 10-100 | Meta-learning |
| Ansor | None (online) | Grows during search | 1K-100K | Online profiling |
| TLP | TenSet (52M records) | None | 0 (per-device) | Pre-trained |
| Timeloop | None | None | 0 (analytical) | Analytical |
| ASTRA-sim | None | Trace collection | Varies | Trace profiling |

_Note: "Total Samples" refers to per-device adaptation samples only; pre-training data (e.g., TenSet) not included._

### Table 3.2: Training Time and Hardware

| Paper | Training Time | Hardware Needed | Pre-trained Available |
|-------|---------------|-----------------|----------------------|
| nn-Meter | Hours per device | Target device | Yes |
| LitePred | Hours (pre-training) + <1 hour (adapt) | GPU cluster | Partial |
| HELP | Hours (meta-training) + minutes (adapt) | GPU | Yes |
| Ansor | Grows during autotuning | Target hardware | No (online) |
| TLP | Hours on TenSet | GPU | Partial |
| AutoTVM | Grows during autotuning | Target hardware | No (online) |
| CALO-GNN | Hours | GPU | No |

### Table 3.3: Training Cost vs. Accuracy Trade-off

| Paper | Training Cost | Accuracy | Cost-Efficiency |
|-------|---------------|----------|-----------------|
| Timeloop | Zero (analytical) | 90-95% | Excellent |
| nn-Meter | Hours per device | 99% | Good (high accuracy) |
| HELP | Hours + minutes adapt | 98% | Excellent (transfer) |
| LitePred | Hours + <1 hour adapt | 99% | Excellent (scalable) |
| Ansor | Days (autotuning) | 85% | Moderate (online) |
| TLP | Hours (one-time) | 88% | Good (pre-trained) |

---

## 4. Transfer Learning Approaches

### Table 4.1: Cross-Hardware Transfer Methods

| Paper | Transfer Method | Source Platforms | Target Adaptation | Accuracy Loss |
|-------|-----------------|------------------|-------------------|---------------|
| LitePred | VAE + hardware embedding | 85 edge devices | ~100 samples, <1 hour | <1% |
| HELP | Meta-learning (MAML) | Multiple devices | 10-100 samples | 2-7% |
| nn-Meter | Per-device training | None (device-specific) | Full training | N/A |
| TAO | Transfer + active learning | GPU generations | Targeted samples | 5-10% |
| TenSet | Pre-trained features | Large-scale dataset | Fine-tuning optional | Varies |

### Table 4.2: Transfer Learning Accuracy by Sample Budget

| Paper | 10 Samples | 50 Samples | 100 Samples | Full Training |
|-------|------------|------------|-------------|---------------|
| HELP | 93.2% | 96.8% | 98.1% | 99%+ |
| LitePred | 92.1% (zero-shot) | 97% | 98.5% | 99.3% |
| TAO | 85% | 92% | 95% | 97% |
| Generic MLP | 60% | 75% | 85% | 97% |

### Table 4.3: Transfer Dimensions Covered

| Paper | Hardware Transfer | Workload Transfer | Framework Transfer | Model Size Transfer |
|-------|-------------------|-------------------|--------------------|--------------------|
| LitePred | Yes (85 platforms) | Limited (CNNs) | Framework-specific | Fixed architectures |
| HELP | Yes (meta-learned) | NAS spaces | Inference runtime | NAS architectures |
| nn-Meter | No (per-device) | General DNN | Multiple frameworks | General |
| TenSet | Implicit | Tensor programs | TVM only | General operators |
| NeuSight | GPU generations | DNNs + LLMs | Framework-agnostic | Scalable |

---

## 5. Summary Statistics

### Table 5.1: Papers by Category Count

| Category | Count | Key Examples |
|----------|-------|--------------|
| Analytical Models | 4 | Timeloop, MAESTRO, Eyeriss, Sparseloop |
| Simulation-Based | 6 | GPGPU-Sim, Accel-Sim, ASTRA-sim, VIDUR, gem5, TrioSim |
| ML-Based (MLP/Tree) | 5 | nn-Meter, AutoTVM, Ansor, LitePred, TLP |
| ML-Based (GNN) | 3 | HELP, CALO-GNN, GRAF |
| Hybrid | 3 | NeuSight, Roofline-LLM, ALCOP |
| LLM Serving Systems | 8 | vLLM, Orca, DistServe, Sarathi-Serve, FlashAttention (1-3), MEDUSA |
| KV Cache Optimization | 3 | Oaken, ALISA, MorphKV |
| Speculative Decoding | 3 | MEDUSA, EAGLE-3, MagicDec |

### Table 5.2: Reproducibility Assessment

| Paper | Code Available | Data/Traces | Pre-trained Models | Documentation |
|-------|----------------|-------------|--------------------| --------------|
| Timeloop | Yes (GitHub) | Examples | N/A | Extensive |
| MAESTRO | Yes (GitHub) | Examples | N/A | Good |
| GPGPU-Sim | Yes (GitHub) | Configs | N/A | Good |
| Accel-Sim | Yes (GitHub) | Traces | N/A | Good |
| nn-Meter | Yes (GitHub) | Partial | Yes | Good |
| TenSet | Yes | Yes (52M) | Partial | Good |
| HELP | Yes (GitHub) | Yes | Yes | Good |
| vLLM | Yes (GitHub) | N/A | N/A | Extensive |
| FlashAttention | Yes (GitHub) | N/A | N/A | Good |
| VIDUR | Yes (GitHub) | Sample traces | N/A | Good |

---

## CSV Format Tables for LaTeX

### CSV 5.1: Papers by Hardware Target

```csv
Paper,Year,Hardware,Technique,Accuracy,Key_Contribution
Timeloop,2019,Spatial accelerators,Loop-nest analysis,5-10% error,Design space exploration
MAESTRO,2019,DNN accelerators,Data-centric,5-15% error,Dataflow notation
GPGPU-Sim,2009,NVIDIA GPUs,Cycle-accurate,0.95 IPC,GPU simulation
Accel-Sim,2020,NVIDIA GPUs,Trace-driven,0.85-0.97 IPC,Modern GPU correlation
ASTRA-sim,2023,Distributed GPU,Event-driven,5-15% error,Distributed training
VIDUR,2024,GPU (LLM),Discrete-event,<5% error,LLM serving simulation
nn-Meter,2021,Edge devices,MLP per kernel,97.8-99.0%,Kernel decomposition
LitePred,2024,85 edge platforms,VAE+MLP,98.5-99.3%,Cross-platform transfer
HELP,2021,Multi (meta),GNN+meta-learning,93.2-98.1%,Few-shot adaptation
vLLM,2023,NVIDIA GPUs,PagedAttention,2-4x throughput,KV cache management
FlashAttention,2022,NVIDIA GPUs,IO-aware,2-4x speed,Linear memory
DistServe,2024,Multi-GPU,Disaggregation,7.4x rate,Phase separation
```

### CSV 5.2: Accuracy Comparison

```csv
Paper,Approach,Accuracy_Metric,Value,Validation
Timeloop,Analytical,vs RTL,5-10% error,RTL simulation
MAESTRO,Analytical,vs RTL,5-15% error,Cross-validation
GPGPU-Sim,Simulation,IPC correlation,0.95,Real GPU
Accel-Sim,Simulation,IPC correlation,0.85-0.97,GPU traces
VIDUR,Simulation,Latency error,<5%,vLLM measurements
nn-Meter,ML-Based,Accuracy,97.8-99.0%,Edge profiling
LitePred,ML-Based,Accuracy,98.5-99.3%,85 platforms
HELP,ML-Based,Accuracy,93.2-98.1%,Cross-hardware
NeuSight,Hybrid,Accuracy,97.7%,GPU profiling
```

### CSV 5.3: Training Cost Comparison

```csv
Paper,Pre-training,Per-Device,Total_Samples,Time
nn-Meter,None,1000/kernel,10K-50K,Hours/device
LitePred,85 platforms,100 samples,100-500,<1 hour adapt
HELP,Multiple platforms,10-100 samples,10-100,Minutes adapt
Ansor,None (online),Grows,1K-100K,During search
TLP,TenSet 52M,None,0,Pre-trained
Timeloop,None,None,0,Analytical
```

### CSV 5.4: Transfer Learning Approaches

```csv
Paper,Method,Source_Platforms,Adaptation_Cost,Accuracy_10,Accuracy_100
LitePred,VAE+embedding,85 edge,<1 hour,92.1%,98.5%
HELP,Meta-learning,Multiple,Minutes,93.2%,98.1%
TAO,Transfer+active,GPU gens,Hours,85%,95%
nn-Meter,None,Device-specific,Full training,N/A,99%
```

---

*Comparison tables by Leo | ML Performance Survey Project*
