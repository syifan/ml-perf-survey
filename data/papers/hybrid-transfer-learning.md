# Hybrid and Transfer Learning Approaches for Performance Modeling

Papers focused on hybrid analytical+ML models, transfer learning, few-shot learning, and domain adaptation for cross-hardware performance prediction (2020-2025).

---

## Summary Table

| Title | Authors | Year | Venue | Approach | Notes |
|-------|---------|------|-------|----------|-------|
| SynPerf | various | 2025 | arXiv | Hybrid | Analytical pipeline + MLP, 6.1% kernel error |
| HELP | Lee et al. | 2021 | NeurIPS | Meta-Learning | 10-sample hardware adaptation, open source |
| Multi-Predict | Akhauri et al. | 2023 | AutoML | Few-Shot | Multi-task, multi-HW, zero-cost proxy encoding |
| nn-Meter | Zhang et al. | 2021 | MobiSys | Transfer | Kernel-level, 85 edge platforms |
| TenSet | Zheng et al. | 2021 | NeurIPS | Dataset | 52M records, 10x speedup with pre-training |
| GRAF | Kadlecova et al. | 2024 | ICML | Graph Features | Outperforms zero-cost proxies |
| ArchGym | Krishnan et al. | 2023 | ISCA | ML-DSE | Hyperparameter lottery, 0.61% RMSE proxy |
| ApproxPilot | various | 2024 | arXiv | GNN-DSE | Physical-aware PPA prediction |
| MASE | various | 2024 | TODAES | Full-Stack | Quantization + FPGA, 24% accuracy gain |

---

## Categorization by Focus Area

### 1. Hybrid Analytical + ML Models

Approaches that combine physics-based/analytical models with machine learning.

- **SynPerf** (2025) - State-of-the-art hybrid GPU prediction
  - Decomposes kernels into pipeline demands (analytical)
  - MLP captures cross-pipeline interactions (ML)
  - 6.1% kernel error, 8.5% end-to-end error
  - Guides Triton kernel optimization with 1.7x speedup

- **Apollo** (2022) - JIT fusion with hybrid optimization
  - Combines graph-level grouping with operator-level loop fusion
  - 1.86x over TensorFlow, 1.37x over XLA on single GPU
  - 19.7% improvement on domain-specific accelerators

- **MetaTune** (2021) - Meta-learning cost model
  - Encodes convolution kernels as structurally similar graphs
  - Predicts optimization parameters for unseen operations
  - Accelerates tensor program autotuning

- **FTuner** (2024) - Dynamic shape tensor tuning
  - Uses uKernel abstraction instead of large design space
  - Avoids expensive cost model training
  - Targets dynamic shape workloads

### 2. Meta-Learning for Hardware Adaptation

Few-shot approaches that quickly adapt to new hardware.

- **HELP** (2021) - NeurIPS Spotlight
  - Formulates hardware prediction as meta-learning problem
  - Novel hardware embeddings represent devices as black-box functions
  - Achieves good predictions with just 10 measurement samples
  - Open source implementation available

- **Multi-Predict** (2023) - Multi-task few-shot
  - Enables multi-task, multi-search-space, multi-HW adaptation
  - Search-space independent encoding via zero-cost proxies
  - Leverages transfer learning for sample efficiency

- **ArchGym** (2023) - ML-aided DSE gymnasium
  - Open-source framework for architecture exploration
  - Discovers "hyperparameter lottery" phenomenon
  - Proxy cost model: 0.61% RMSE, 2000x simulation speedup
  - Supports memory controllers, DNN accelerators, AR/VR SoCs

### 3. Transfer Learning for Cross-Platform Prediction

Methods that transfer knowledge between hardware platforms.

- **nn-Meter** (2021) - Edge device predictor
  - Kernel-level prediction via automatic kernel detection
  - Adaptive sampling for efficient data collection
  - Supports mobile CPU, GPU, Intel VPU
  - Microsoft open source, used widely for HW-aware NAS

- **TenSet** (2021) - Large-scale dataset
  - 52 million program performance records
  - Covers Intel/AMD/ARM CPUs and NVIDIA GPUs
  - Pre-trained cost models achieve 10x speedup
  - Standard benchmark for cost model research

- **Cross-Feature Transfer** (2024) - Joint feature learning
  - Learns joint NN-hardware feature space
  - GNN-based latency querying with multi-headed prediction
  - Enables transfer to unseen target hardware

- **CNN Latency Heterogeneous** (2024) - Mobile framework
  - Operation-wise framework for cross-device prediction
  - Addresses hardware heterogeneity challenges
  - Handles diverse ML framework optimizations

### 4. Few-Shot Learning for New Hardware

Zero-shot and few-shot approaches for unseen configurations.

- **DCP** (2024) - Dataflow optimization
  - Zero-shot and few-shot unseen hardware settings
  - Fine-tunes neural predictor with minimal samples
  - Propagation-based dataflow learning

- **BRP-NAS** (2020) - GCN-based predictor
  - Graph convolutional network for accuracy/latency prediction
  - Released LatBench dataset across desktop/embedded/mobile
  - Binary relation modeling with iterative data selection

- **GRAF** (2024) - Neural graph features
  - Simple graph properties as strong performance predictors
  - Outperforms zero-cost proxies at fraction of cost
  - Fast, interpretable NAS performance prediction
  - ICML 2024

### 5. GNN-Based Design Space Exploration

Graph neural networks for accelerator design automation.

- **ApproxPilot** (2024) - Approximation framework
  - GNN captures physical connections of arithmetic units
  - Predicts PPA and accuracy jointly
  - Critical path embedding enhances prediction quality
  - Outperforms SOTA approximation frameworks

- **ApproxGNN** (2024) - Pretrained GNN for DSE
  - Targets approximate computing accelerators
  - 50% better embedding accuracy than alternatives
  - 30-54% improvement over statistical ML approaches

- **GNNBuilder** (2023) - Automated accelerator generation
  - End-to-end GNN accelerator framework
  - Accurate performance models enable fast DSE
  - Generic across GNN workloads

- **Meta-DSE-GNN** (2022) - Meta-learning for GNN-DSE
  - Meta-learning improves GNN-based design automation
  - DAC 2022 publication

### 6. Full-Stack Optimization Frameworks

Comprehensive frameworks spanning algorithm to hardware.

- **MASE** (2024) - ML Accelerator System Exploration
  - Quantization search, QAT, FPGA generation
  - Supports mixed-precision MX formats
  - 24% accuracy improvement at 3% energy overhead
  - First fine-grain multi-precision MX for LLM accelerators

- **AutoScaleDSE** (2024) - HLS transfer learning
  - Transfer learning for design space exploration
  - Mixed-sharing multi-domain model
  - Outperforms single-domain approaches

### 7. Distributed Training Performance Models

Models for multi-GPU and distributed settings.

- **FlexFlow** (2022) - Parallelization strategies
  - Execution simulator for strategy evaluation
  - SOAP dimensions: Sample, Operator, Attribute, Parameter
  - Automatic strategy discovery

- **FlexFlow Serve** (2024) - LLM serving
  - Distributed LLM inference optimization
  - 1.3-2.0x speedup (single-node)
  - 1.4-2.4x speedup (multi-node)

---

## Key Themes and Trends

### 1. Hybrid Models Achieve Best Accuracy
- SynPerf demonstrates hybrid analytical+ML achieves SOTA accuracy
- Analytical components provide interpretability and physics grounding
- ML components capture complex interactions and residual errors

### 2. Meta-Learning Enables Rapid Hardware Adaptation
- HELP shows 10-sample adaptation is feasible
- Critical for reducing deployment cost to new hardware
- Hardware embeddings as black-box function representations

### 3. Transfer Learning Reduces Data Requirements
- TenSet enables pre-training with cross-platform generalization
- nn-Meter's kernel-level approach transfers across device types
- Critical for scaling to diverse edge hardware landscape

### 4. GNN Emerges as Key Architecture for DSE
- Graph structure naturally represents accelerator designs
- Physical connections captured in GNN message passing
- Enables joint optimization of multiple objectives

### 5. Few-Shot Critical for Emerging Hardware
- New accelerators (RISC-V, PIM, custom ASICs) lack training data
- Zero-shot and few-shot approaches essential
- GRAF shows simple features can be surprisingly effective

---

## Relationship to Existing Paper Categories

### Extends ML-Based Models
- SynPerf improves on NeuSight with analytical foundation
- HELP/Multi-Predict generalize LitePred's transfer approach
- GRAF provides alternative to learned encodings

### Connects to Analytical Models
- Hybrid approaches bridge analytical and ML literature
- SynPerf combines roofline-like analysis with neural networks
- MetaTune brings meta-learning to compiler cost models

### Enables Cross-Platform Evaluation
- These methods critical for fair cross-hardware comparison
- TenSet provides standard benchmark for cost model evaluation
- ArchGym enables reproducible DSE experiments

---

## Taxonomy Classification

| Paper | Approach | Hardware | Workloads | Target | Input |
|-------|----------|----------|-----------|--------|-------|
| SynPerf | Hybrid | GPU | General DNN | Latency | Static |
| HELP | ML-Based | Multi | CNN | Latency | Graph-Only |
| Multi-Predict | ML-Based | Multi | CNN | Latency/Accuracy | Graph-Only |
| nn-Meter | ML-Based | Edge | General DNN | Latency | Static |
| TenSet | Dataset | Multi | Tensor Programs | Latency | Profiling |
| GRAF | ML-Based | N/A | CNN | Accuracy | Graph-Only |
| ArchGym | ML-Based | Accelerators | DNN | Multi-Objective | Profiling |
| MASE | Hybrid | FPGA | Transformer/LLM | Multi-Objective | Static |

---

## Papers for Deep Analysis (High Priority)

1. **SynPerf** - Latest hybrid approach with production impact
2. **HELP** - Foundational meta-learning work, well-cited
3. **TenSet** - Standard dataset enabling reproducibility
4. **ArchGym** - Comprehensive framework with hyperparameter lottery insight
5. **GRAF** - Simple but effective, challenges complex encodings

---

## Gap Analysis

### Well-Covered
- Cross-hardware CNN latency prediction
- NAS predictor transfer learning
- Tensor compiler cost models

### Emerging Areas
- LLM-specific transfer learning
- Hybrid models for distributed training
- Few-shot for emerging accelerators (PIM, neuromorphic)

### Underexplored
- Domain adaptation between workload types
- Continual learning for evolving hardware
- Uncertainty-aware transfer predictions

---

## Notes

- Priority given to peer-reviewed venues (NeurIPS, ICML, ISCA, MLSys, MobiSys)
- Open source implementations noted where available
- Papers bridge analytical and ML-based categories in existing taxonomy
