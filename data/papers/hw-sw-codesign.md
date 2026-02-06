# Hardware-Software Co-Design for ML Performance Models

Papers focused on neural architecture search with hardware-aware predictors, AutoML systems with performance modeling, hardware design optimization using ML, and co-design of DNN accelerators and workloads (2020-2025).

---

## Summary Table

| Title | Authors | Year | Venue | Approach | Notes |
|-------|---------|------|-------|----------|-------|
| NAAS | Lin et al. | 2021 | DAC | Co-Search | NN + accelerator + mapping co-optimization |
| HASCO | Xiao et al. | 2021 | ISCA | Co-Design | Tensor syntax tree IR, Bayesian optimization |
| CODEBench | Jha Lab | 2023 | TECS | Benchmark | BOSHCODE surrogate for CNN-accelerator pairs |
| ConfuciuX | Kao et al. | 2020 | MICRO | RL-DSE | REINFORCE for hardware resource assignment |
| MCUNetV2 | Lin et al. | 2021 | NeurIPS | Tiny ML | Patch-based inference, 71.8% ImageNet on MCU |
| AutoDNNchip | Tu et al. | 2020 | FPGA | Automation | Chip predictor + builder for FPGA/ASIC |
| Timeloop | Parashar et al. | 2019 | ISPASS | Analytical | Systematic DNN accelerator evaluation |
| MAESTRO | Kwon et al. | 2019 | MICRO | Analytical | Data-centric dataflow cost model |
| HAO | Jain et al. | 2021 | FCCM | Co-Design | Integer programming for FPGA NAS |
| Energon | Zhou et al. | 2022 | TCAD | Co-Design | Dynamic sparse attention accelerator |
| HADAS | UC Irvine | 2023 | DATE | Dynamic NAS | Joint backbone + DVFS optimization |
| Gemmini | Genc et al. | 2021 | DAC | Generator | Systolic array accelerator generator |
| On Latency Predictors | MLSys | 2024 | MLSys | Predictor | End-to-end training strategy, 5.8x speedup |
| GNN-DSE | UCLA | 2022 | DAC | GNN-DSE | Meta-learning for HLS design prediction |
| Zeus | You et al. | 2023 | NSDI | Energy | GPU energy optimization for DNN training |

---

## Categorization by Focus Area

### 1. Joint Neural Architecture and Accelerator Search

Approaches that simultaneously optimize neural network architecture and hardware accelerator design.

- **NAAS** (2021) - Neural Accelerator Architecture Search
  - Holistically searches NN architecture, accelerator architecture, and compiler mapping
  - Two-level optimization with indexing, ordering, and sizing
  - 4.4x EDP reduction vs. Eyeriss with 2.7% accuracy improvement
  - Encodes non-numerical parameters (loop order, parallel dimension) numerically
  - MIT HAN Lab, published at DAC 2021

- **HASCO** (2021) - Hardware-Software Co-Design for Tensor Computation
  - Uses tensor syntax trees as unified IR for HW/SW co-design
  - Multi-objective Bayesian optimization for hardware exploration
  - Q-learning and heuristics for software optimization
  - 1.25-1.44x latency reduction vs. separate HW/SW design
  - ISCA 2021, PKU/UCLA

- **CODEBench** (2023) - Neural Architecture and Accelerator Co-Design Framework
  - Combines CNNBench (accuracy) + AccelBench (hardware performance)
  - BOSHCODE: surrogate model predicting CNN-accelerator pair performance
  - Hierarchical search with neural network surrogate and active learning
  - 1.4% higher accuracy, 59.1% lower latency, 60.8% lower energy
  - ACM TECS 2023, Princeton/Stanford

- **HAO** (2021) - Hardware-Aware Neural Architecture Optimization
  - Integer programming prunes design space under hardware constraints
  - Directly outputs optimal accelerator config for FPGA mapping
  - 72.5% ImageNet accuracy at 50 FPS, 60-135% faster than prior work
  - FCCM 2021

### 2. ML-Based Design Space Exploration

Using machine learning to accelerate hardware design space exploration.

- **ConfuciuX** (2020) - Autonomous Hardware Resource Assignment
  - REINFORCE RL for DNN accelerator resource allocation
  - Handles O(10^72) design space for MobileNet configurations
  - 4.7-24x faster convergence than Bayesian/GA/SA approaches
  - Uses MAESTRO cost model for reward estimation
  - MICRO 2020, Georgia Tech

- **GNN-DSE** (2022) - GNN-Based Accelerator Design Automation
  - GNN as surrogate for High-Level Synthesis tools
  - Meta-learning (MAML) for new kernel adaptation
  - Addresses domain shift between training and test kernels
  - DAC 2022, UCLA

- **Gemmini** (2021) - Systolic Array Generator
  - Open-source, full-stack DNN accelerator generator
  - Generates wide design space from flexible template
  - Up to 2,670x speedup over CPU baselines
  - Fabricated accelerators with comparable commercial performance
  - DAC 2021, UC Berkeley

### 3. Analytical Cost Models for Accelerators

Deterministic models for rapid accelerator performance estimation.

- **Timeloop** (2019) - Systematic DNN Accelerator Evaluation
  - Unified representation of architecture and implementation attributes
  - Automatic mapspace construction and optimal mapping search
  - Deterministic model for throughput, access counts, energy
  - Supports diverse memory technologies (SRAM, DRAM, HBM)
  - Integrated with Accelergy for energy estimation
  - ISPASS 2019, NVIDIA/MIT

- **MAESTRO** (2019) - Data-Centric Dataflow Analysis
  - Models accelerator efficiency via spatio-temporal reuse and occupancy
  - Data-centric directives for specifying dataflow space
  - Rapid estimation: latency, energy, throughput (20+ metrics)
  - Used by ConfuciuX and other DSE frameworks
  - MICRO 2019 (Top Picks 2020), Georgia Tech

- **AutoDNNchip** (2020) - Automated DNN Chip Predictor/Builder
  - Chip Predictor: energy, throughput, latency, area estimation
  - Chip Builder: automatic RTL generation with optimized dataflows
  - Two-stage DSE: coarse exploration → pipeline optimization
  - <10% prediction error, up to 3.86x improvement over expert designs
  - FPGA 2020, Rice/UIUC

### 4. Tiny ML and Edge Deployment

Co-design for memory-constrained microcontroller and edge devices.

- **MCUNetV2** (2021) - Memory-Efficient Patch-Based Inference
  - Patch-by-patch scheduling for memory-constrained MCUs
  - Network redistribution shifts FLOPs to later stages
  - 4-8x peak memory reduction with patch-based inference
  - 71.8% ImageNet accuracy under 32kB SRAM
  - Enables object detection on tiny devices (16.9% higher mAP)
  - NeurIPS 2021, MIT HAN Lab

- **HADAS** (2023) - Hardware-Aware Dynamic NAS
  - Joint optimization: backbone, early exits, DVFS
  - Nested genetic algorithms for DyNN search
  - Up to 57% energy gains with accuracy retention
  - Compatible with existing NAS frameworks
  - DATE 2023, UC Irvine

### 5. Transformer and Attention Accelerators

Co-design approaches for transformer model acceleration.

- **Energon** (2022) - Dynamic Sparse Attention Accelerator
  - Mix-Precision Multi-Round Filtering (MP-MRF) algorithm
  - Filtering Unit + Attention Unit architecture
  - 168x speedup vs. CPU, 8.7x vs. V100 GPU
  - 10^4x energy reduction vs. CPU
  - IEEE TCAD 2022

### 6. Energy-Aware Training and Inference

Performance models for energy optimization.

- **Zeus** (2023) - GPU Energy Optimization for DNN Training
  - Automatic batch size and power limit optimization
  - 15.3-75.8% energy reduction, up to 60.6% time reduction
  - Energy-optimal batch size: 3.4-65.0% energy savings
  - Integrated with PyTorch
  - NSDI 2023, University of Michigan

### 7. Hardware-Aware Latency Prediction

Specialized predictors for hardware-aware NAS.

- **On Latency Predictors for NAS** (2024) - MLSys
  - End-to-end predictor training strategy
  - Studies architecture, sample selection, device representation, encoding
  - 22.5% average improvement, up to 87.6% on hard tasks
  - 5.8x wall-clock speedup for hardware-aware NAS
  - Automated device set design for evaluation
  - MLSys 2024

---

## Key Themes and Trends

### 1. Integration of Search Spaces
- NAAS, HASCO, CODEBench demonstrate benefits of joint optimization
- Separate optimization leaves performance on the table
- Co-search requires unified representation (tensor syntax trees, encoding schemes)

### 2. Cost Models as Optimization Enablers
- MAESTRO/Timeloop provide fast, accurate feedback for DSE
- AutoDNNchip achieves <10% error for chip prediction
- Enables exploring O(10^72) design spaces efficiently

### 3. Learning-Based Surrogates
- GNN-DSE shows meta-learning improves generalization to new kernels
- BOSHCODE demonstrates neural surrogates with uncertainty quantification
- Critical for reducing HLS simulation overhead

### 4. Memory as Primary Constraint for Edge
- MCUNetV2 shows patch-based inference unlocks tiny devices
- Co-design of inference schedule and architecture essential
- Memory redistribution complements architecture search

### 5. Dynamic Adaptation
- HADAS optimizes jointly with DVFS for runtime adaptation
- Energon dynamically identifies sparse patterns
- Static models insufficient for variable workloads

---

## Relationship to Existing Paper Categories

### Extends ML-Based Models
- GNN-DSE/BOSHCODE use ML for hardware performance prediction
- Connects to LitePred, NeuSight transfer learning approaches
- Meta-learning bridges training/deployment domain gaps

### Connects to Analytical Models
- Timeloop/MAESTRO provide analytical foundations for DSE
- AutoDNNchip combines analytical prediction with automation
- Hybrid approaches (analytical structure + learned residuals)

### Enables Hardware-Aware NAS
- Latency predictors essential for efficient architecture search
- MCUNetV2 demonstrates co-design benefits for extreme constraints
- CODEBench provides reproducible benchmarking

---

## Taxonomy Classification

| Paper | Approach | Hardware | Workloads | Target | Input |
|-------|----------|----------|-----------|--------|-------|
| NAAS | ML-Based | Accelerator | CNN | Multi-Objective | Static |
| HASCO | Hybrid | Accelerator | Tensor | Latency | Static |
| CODEBench | ML-Based | Accelerator | CNN | Multi-Objective | Static |
| ConfuciuX | ML-Based | Accelerator | DNN | Multi-Objective | Profiling |
| MCUNetV2 | Hybrid | MCU | CNN | Memory/Latency | Static |
| AutoDNNchip | ML-Based | FPGA/ASIC | DNN | Multi-Objective | Static |
| Timeloop | Analytical | Accelerator | DNN | Multi-Objective | Static |
| MAESTRO | Analytical | Accelerator | DNN | Multi-Objective | Static |
| Energon | Hybrid | Accelerator | Transformer | Latency/Energy | Static |
| Zeus | ML-Based | GPU | DNN Training | Energy | Profiling |

---

## Papers for Deep Analysis (High Priority)

1. **NAAS** - Pioneering joint NN/accelerator/mapping co-search
2. **CODEBench** - Comprehensive framework with BOSHCODE surrogate
3. **Timeloop/MAESTRO** - Foundational analytical models used widely
4. **MCUNetV2** - Breakthrough for extreme edge deployment
5. **ConfuciuX** - RL-based DSE with practical impact

---

## Gap Analysis

### Well-Covered
- CNN accelerator co-design
- FPGA-based automation
- Analytical cost models for spatial architectures

### Emerging Areas
- LLM accelerator co-design
- Transformer-specific optimization (Energon)
- Energy-aware training (Zeus)

### Underexplored
- Co-design for emerging memory technologies (PIM, ReRAM)
- Multi-tenant accelerator optimization
- Continual learning for evolving hardware

---

## Notes

- Priority given to peer-reviewed venues (ISCA, MICRO, DAC, MLSys, NeurIPS)
- Open source implementations noted where available
- Papers bridge analytical and ML-based categories
- Focus on 2020-2025 per issue requirements

