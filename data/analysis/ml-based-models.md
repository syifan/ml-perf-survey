# Deep Analysis: ML-Based Performance Models for DNN Workloads

This document provides detailed analysis of ML-based performance modeling approaches for DNN workloads, covering neural network surrogates, graph neural networks, transformer-based models, and transfer learning techniques.

---

## 1. Neural Network-Based Models (MLPs, CNNs, RNNs)

### 1.1 nn-Meter (MobiSys 2021) - Best Paper

**Full Title:** nn-Meter: Towards Accurate Latency Prediction of Deep-Learning Model Inference on Diverse Edge Devices

**Authors:** Zhang et al. (Microsoft Research)

#### Core Methodology

nn-Meter introduces a **kernel-level latency prediction** approach that achieves 99% accuracy on edge devices. The key insight is that end-to-end model latency can be decomposed into kernel latencies, where kernels are fused operator groups.

The framework consists of:
1. **Kernel Detection** - Automatically identifies how frameworks fuse operators
2. **Adaptive Data Sampler** - Efficiently collects training data for each kernel
3. **Kernel Predictor** - Separate MLP for each kernel type

#### Architecture

```
Input: DNN Computational Graph
           |
           v
    +---------------+
    | Kernel        |  Detects op fusion patterns
    | Detector      |  (conv-bn-relu -> single kernel)
    +---------------+
           |
           v
    +---------------+
    | Per-Kernel    |  MLP predictor per kernel type
    | Predictors    |  Features: shape, dtype, etc.
    +---------------+
           |
           v
    Sum of kernel latencies = Total latency
```

#### Training Data Requirements

| Aspect | Details |
|--------|---------|
| Data Collection | Automated profiling on target device |
| Sample Efficiency | ~1000 samples per kernel type |
| Adaptation Cost | Hours for new device |
| Transfer Approach | Adaptive sampling reduces data needs |

#### Accuracy Claims

| Device | Framework | Accuracy | Notes |
|--------|-----------|----------|-------|
| Pixel 4 (CPU) | TFLite | 99.0% | Avg error <1% |
| Pixel 4 (GPU) | TFLite | 98.5% | Mobile GPU |
| Intel VPU | OpenVINO | 97.8% | Myriad X |
| Cortex-A76 | NCNN | 98.2% | ARM CPU |

#### Strengths

1. **Kernel-level decomposition** - Captures framework fusion behavior
2. **Adaptive sampling** - Reduces data collection overhead
3. **Hardware-agnostic design** - Supports diverse edge devices
4. **Open source** - https://github.com/microsoft/nn-Meter
5. **Production-ready** - Used in Azure ML for hardware-aware NAS

#### Limitations

1. **Device-specific training** - Requires profiling on each target device
2. **Framework dependency** - Fusion patterns differ across frameworks
3. **Edge focus** - Less validated on datacenter GPUs
4. **Static shapes** - Assumes fixed input dimensions

#### Taxonomy Classification

- **Approach:** ML-Based (MLP ensemble)
- **Hardware:** Edge devices (mobile CPU/GPU, VPU)
- **Workloads:** General DNN
- **Target:** Latency
- **Input:** Graph-Only (after kernel detection)
- **Reproducibility:** Full

---

### 1.2 TVM/Ansor Cost Models (OSDI 2018/2020)

**Full Title:** TVM: An Automated End-to-End Optimizing Compiler for Deep Learning / Ansor: Generating High-Performance Tensor Programs for Deep Learning

**Authors:** Chen et al., Zheng et al. (OctoML, UC Berkeley)

#### Core Methodology

TVM's AutoTVM and Ansor use **learned cost models** to guide tensor program optimization. Instead of executing every candidate program, ML models predict performance to prune the search space.

**AutoTVM** uses XGBoost regression on hand-crafted features:
- Loop iteration counts, vectorization widths
- Memory access patterns, cache utilization estimates
- Hardware-specific features (thread block dimensions)

**Ansor** improves with:
- Hierarchical search (sketch generation → random annotation → evolutionary refinement)
- Feature extraction from program AST
- Multi-layer perceptron with 512-dimensional features

#### Performance Model Features

| Model | Features | ML Model |
|-------|----------|----------|
| AutoTVM | Loop vars, memory patterns | XGBoost |
| Ansor | Program AST features | MLP (2 hidden layers) |
| MetaSchedule | Probabilistic features | Gradient-boosted trees |

#### Training Data

- **Source:** Profiled execution times on target hardware
- **Size:** TenSet provides 52M records for reproducibility
- **Collection:** Online learning during autotuning

#### Accuracy Claims

| System | Error | Speedup vs. Baseline |
|--------|-------|----------------------|
| AutoTVM | ~20% MAPE | 1.2-2x over manual tuning |
| Ansor | ~15% MAPE | Up to 3.8x over AutoTVM |
| MetaSchedule | ~10% MAPE | Matches Ansor quality |

#### Strengths

1. **Integrated with compiler** - Direct impact on code generation
2. **Online learning** - Improves during search
3. **TenSet dataset** - Enables reproducible research
4. **Production deployment** - Used in Apache TVM

#### Limitations

1. **Search-time training** - Model trains during autotuning
2. **Hardware-specific** - Separate model per target
3. **Operator-level** - Doesn't predict end-to-end latency directly
4. **Tuning overhead** - Hours to days for large models

#### Taxonomy Classification

- **Approach:** ML-Based (XGBoost, MLP)
- **Hardware:** Multi (CPU, GPU, accelerators)
- **Workloads:** Tensor programs (operators)
- **Target:** Latency
- **Input:** Profiling-Based (during search)
- **Reproducibility:** Full (TenSet dataset)

---

### 1.3 LitePred (NSDI 2024)

**Full Title:** LitePred: Transferable and Scalable Latency Prediction for Hardware-Aware Neural Architecture Search

**Authors:** Feng et al. (MIT, Google)

#### Core Methodology

LitePred addresses cross-platform transfer learning using a **variational autoencoder (VAE)** based approach. Key innovations:

1. **Hardware Embedding** - Learns latent representation of hardware platforms
2. **Data Sampler** - VAE selects most informative samples for new platforms
3. **Shared Predictor** - Single model generalizes across 85+ platforms

#### Architecture

```
+------------------+     +------------------+
|  Architecture    |     |   Hardware       |
|  Encoder         |     |   Embedding      |
+------------------+     +------------------+
         |                        |
         v                        v
    +--------------------------------+
    |        Shared MLP              |
    |   (Architecture + Hardware)    |
    +--------------------------------+
                  |
                  v
            Latency Prediction
```

#### Transfer Learning Approach

| Step | Description | Data Required |
|------|-------------|---------------|
| 1. Pre-train | Train on source platforms | Full profiling data |
| 2. Embed | Learn hardware embedding | Platform characteristics |
| 3. Sample | VAE selects key samples | ~100 samples |
| 4. Fine-tune | Adapt to target | <1 hour profiling |

#### Accuracy Claims

| Setting | Platforms | Accuracy | Adaptation Cost |
|---------|-----------|----------|-----------------|
| Full | 85 edge devices | 99.3% | None (trained) |
| Transfer | New device | 98.5% | <1 hour |
| Zero-shot | New device | 92.1% | None |

#### Strengths

1. **Cross-platform transfer** - Single model covers 85 platforms
2. **Sample efficiency** - 100 samples for adaptation
3. **VAE-based sampling** - Intelligent data selection
4. **Scalable** - Handles diverse hardware landscape

#### Limitations

1. **Edge focus** - Not validated on datacenter GPUs
2. **CNN architectures** - Limited transformer evaluation
3. **Framework-specific** - Tied to specific inference runtimes

#### Taxonomy Classification

- **Approach:** ML-Based (VAE + MLP)
- **Hardware:** Edge devices (85 platforms)
- **Workloads:** CNN architectures
- **Target:** Latency
- **Input:** Transfer Learning
- **Reproducibility:** Partial

---

## 2. Graph Neural Network Approaches

### 2.1 HELP (NeurIPS 2021)

**Full Title:** Hardware-Adaptive Efficient Latency Prediction for NAS via Meta-Learning

**Authors:** Lee et al. (KAIST, Samsung)

#### Core Methodology

HELP formulates hardware latency prediction as a **meta-learning problem**. The key insight is that hardware platforms can be treated as "tasks" in meta-learning, enabling few-shot adaptation to new devices.

Components:
1. **Architecture Encoder** - GNN encodes neural architecture graph
2. **Hardware Encoder** - Learns hardware embedding from few samples
3. **Meta-Learner** - MAML-style adaptation across hardware tasks

#### Meta-Learning Formulation

```
Given:
- N source hardware platforms with profiled data
- New target platform with ~10 samples

Learn:
- Architecture embedding f(arch)
- Hardware embedding g(hw)
- Predictor h(f(arch), g(hw)) → latency
```

#### Architecture Encoding

HELP uses a **directed acyclic graph (DAG)** representation:
- Nodes: Operations (conv, relu, pool, etc.)
- Edges: Data dependencies
- GNN: Message passing to aggregate features

#### Accuracy Claims

| Adaptation Samples | Accuracy | vs. Full Training |
|-------------------|----------|-------------------|
| 10 samples | 93.2% | 15% gap |
| 50 samples | 96.8% | 3% gap |
| 100 samples | 98.1% | 1% gap |

#### Strengths

1. **Few-shot adaptation** - 10 samples for reasonable accuracy
2. **Meta-learning framework** - Principled transfer approach
3. **GNN architecture encoding** - Captures graph structure
4. **Open source** - Implementation available

#### Limitations

1. **CNN-focused** - Limited transformer support
2. **Meta-training cost** - Requires many source platforms
3. **Sample quality** - Assumes representative samples

#### Taxonomy Classification

- **Approach:** ML-Based (GNN + Meta-Learning)
- **Hardware:** Multi (via meta-learning)
- **Workloads:** CNN architectures (NAS search spaces)
- **Target:** Latency
- **Input:** Graph-Only + Few-shot profiling
- **Reproducibility:** Full

---

### 2.2 GNN-Based Compiler Cost Models

Several recent works apply GNNs to tensor program cost modeling:

#### CALO-GNN (OpenReview 2024)

**Approach:** GNN with **calibrated uncertainty** for tensor program latency.

Key contributions:
- Uncertainty quantification helps autotuner explore vs. exploit
- Calibrated confidence intervals on predictions
- Better sample efficiency in autotuning loop

#### TC-GNN (HPCA 2022)

**Full Title:** TC-GNN: Bridging Sparse GNN and Dense Tensor Core on GPU

**Approach:** GNN accelerated by Tensor Cores for computational graph optimization.

While primarily a system paper, TC-GNN demonstrates:
- GNN message passing maps to sparse-dense matrix ops
- 1.70x speedup over Deep Graph Library
- Enables faster graph-based cost model inference

#### GRAF (ICML 2024)

**Full Title:** Graph Features for Neural Architecture Search

**Key insight:** Simple graph features (degree distribution, clustering coefficient) can match complex learned embeddings for NAS performance prediction.

| Method | Accuracy | Training Cost |
|--------|----------|---------------|
| Zero-cost proxies | 0.65 correlation | None |
| GRAF features | 0.78 correlation | None |
| Learned GNN | 0.82 correlation | Hours |

Implication: Graph structure alone carries significant performance signal.

---

### 2.3 Comparison of GNN Architectures

| Model | Graph Encoding | Message Passing | Pooling |
|-------|---------------|-----------------|---------|
| HELP | Op-level DAG | 3-layer GNN | Global mean |
| CALO-GNN | Tensor program AST | Graph attention | Hierarchical |
| ApproxGNN | Hardware circuit graph | Pretrained GNN | Attention |

#### When to Use GNNs

**Advantages:**
- Natural fit for computational graphs
- Captures operator dependencies
- Enables transfer across architectures

**Disadvantages:**
- Training data requirements
- Inference overhead vs. MLP
- Graph construction preprocessing

---

## 3. Transformer-Based Models

### 3.1 Architecture Performance Prediction

Recent work explores transformers for performance prediction:

#### TLP (ASPLOS 2023)

**Full Title:** TLP: A Deep Learning-Based Cost Model for Tensor Program Tuning

**Approach:** Transformer encoder over program tokens.

Key components:
1. **Program Tokenization** - Convert tensor program to token sequence
2. **Positional Encoding** - Capture loop structure
3. **Transformer Encoder** - Self-attention over program tokens
4. **Regression Head** - Predict execution time

#### Accuracy vs. Prior Work

| Model | MAPE | Training Data |
|-------|------|---------------|
| XGBoost (AutoTVM) | 22.1% | 10K samples |
| MLP (Ansor) | 15.3% | 10K samples |
| TLP (Transformer) | 11.8% | 10K samples |

#### Self-Attention for Programs

The transformer captures:
- Long-range dependencies in nested loops
- Parallel vs. sequential structure
- Memory access patterns through positional encoding

### 3.2 LLM-Assisted Performance Modeling

Emerging approaches use large language models:

#### LLM for Code Analysis

Recent work (2024-2025) explores:
- Using code LLMs to extract performance features
- Zero-shot latency estimation from code descriptions
- Chain-of-thought reasoning about bottlenecks

Challenges:
- Hallucination in numerical predictions
- Limited hardware awareness
- Expensive inference for autotuning loops

---

## 4. Comparative Analysis

### 4.1 Accuracy Comparison

| Model | Best Accuracy | Target | Evaluation Scope |
|-------|---------------|--------|------------------|
| nn-Meter | 99.0% | Edge latency | 4 platforms, CNNs |
| LitePred | 99.3% | Edge latency | 85 platforms, CNNs |
| HELP | 98.1% | Multi-platform | Meta-learning, CNNs |
| Ansor | 85% (within 15% error) | GPU/CPU | Tensor programs |
| TLP | 88% (within 12% error) | GPU/CPU | Tensor programs |
| NeuSight | 97.7% | GPU | DNNs including LLMs |

### 4.2 Training Data Requirements

| Model | Pre-training Data | Per-Device Adaptation |
|-------|-------------------|----------------------|
| nn-Meter | None | ~1000 samples/kernel |
| LitePred | 85 platforms | ~100 samples |
| HELP | Multiple platforms | 10-100 samples |
| Ansor | None (online) | Grows during search |
| TLP | TenSet (52M) | None |

### 4.3 Generalization Capabilities

| Dimension | Best Approach | Notes |
|-----------|---------------|-------|
| New architectures | GNN-based | Graph structure generalizes |
| New hardware | LitePred, HELP | Transfer learning |
| New operators | TVM cost models | Online adaptation |
| Dynamic shapes | Limited coverage | Open research challenge |

### 4.4 Speed vs. Accuracy Trade-off

```
                    Accuracy
                       ^
                       |
    99% ---------------+---- nn-Meter, LitePred
                       |          (specialized)
                       |
    95% ---------------+-------- HELP, NeuSight
                       |             (general)
                       |
    90% ---------------+------------ TLP, Ansor
                       |                (compiler)
                       |
    85% ---------------+---------------- XGBoost
                       |                   (basic)
                       +---------------------------------> Generality
                       Narrow                         Broad
```

---

## 5. Key Themes and Trends

### 5.1 Kernel-Level Decomposition Emerges as Best Practice

nn-Meter demonstrated that decomposing models into kernels dramatically improves accuracy:
- Captures framework fusion behavior
- Enables compositional prediction
- Allows per-kernel specialization

This insight is now adopted by NeuSight (tile-based) and others.

### 5.2 Transfer Learning is Essential for Scalability

The explosion of edge devices (85+ in LitePred) makes per-device training impractical:
- Meta-learning (HELP) enables few-shot adaptation
- VAE sampling (LitePred) selects informative samples
- Pre-trained embeddings (TenSet) provide foundation

### 5.3 GNNs Capture Graph Structure Effectively

For neural architecture search and dataflow prediction:
- DAG representation is natural for DNNs
- Message passing aggregates operator features
- Enables cross-architecture transfer

But simple features (GRAF) can be surprisingly competitive.

### 5.4 Hybrid Approaches Dominate Recent Work

Pure ML models are giving way to hybrid analytical+ML:
- NeuSight combines roofline with neural networks
- ALCOP pre-trains with analytical model outputs
- Physics-informed approaches improve robustness

### 5.5 Uncertainty Quantification Gains Importance

For autotuning, knowing prediction confidence matters:
- CALO-GNN provides calibrated uncertainty
- Enables better exploration vs. exploitation
- Critical for sample-efficient optimization

---

## 6. Gaps and Open Challenges

### 6.1 Well-Addressed Areas

- **CNN latency on edge devices** - nn-Meter, LitePred achieve 99%+ accuracy
- **Tensor program tuning** - TVM/Ansor cost models enable fast autotuning
- **NAS predictor** - HELP, Multi-Predict enable hardware-aware search

### 6.2 Emerging Challenges

| Challenge | Current State | Needed |
|-----------|---------------|--------|
| LLM inference | VIDUR simulates | ML-based prediction |
| Dynamic shapes | Limited support | Shape-aware models |
| Distributed training | ASTRA-sim simulates | Fast surrogate models |
| Energy prediction | Fragmented | Unified energy models |

### 6.3 Underexplored Areas

1. **Uncertainty quantification** - Only CALO-GNN addresses systematically
2. **Continual learning** - Adapting to hardware/software evolution
3. **Multi-objective prediction** - Joint latency-energy-memory
4. **Sparse/dynamic models** - Activation sparsity, early exit

---

## 7. Reproducibility Assessment

### 7.1 Available Artifacts

| Model | Code | Data | Pre-trained |
|-------|------|------|-------------|
| nn-Meter | Yes | Partial | Yes |
| TVM/Ansor | Yes | TenSet | No |
| LitePred | Partial | No | No |
| HELP | Yes | Yes | Yes |
| TLP | Partial | TenSet | No |
| CALO-GNN | No | No | No |

### 7.2 Reproducibility Recommendations

For survey readers, most reproducible options:
1. **nn-Meter** - Full open source, Microsoft maintained
2. **TVM ecosystem** - Apache project, TenSet dataset
3. **HELP** - Complete code and experiments

---

## 8. Key Takeaways for Survey

### What ML-Based Models Excel At

1. **High accuracy for specialized domains** - 99%+ on edge devices
2. **Fast inference** - Real-time prediction for autotuning
3. **Cross-platform transfer** - Handle diverse hardware landscape
4. **Data-driven generalization** - Learn patterns beyond analytical models

### Gaps Addressed by Other Approaches

| Gap | Analytical Approach | Simulation Approach |
|-----|---------------------|---------------------|
| Interpretability | Closed-form equations | Execution traces |
| No training data | Hardware specs only | Run programs |
| New architectures | Parameter updates | Execution |
| Microarch details | Detailed models | Cycle-accurate |

### Evolution of ML-Based Performance Modeling

```
XGBoost on Features (2018)
        |
        v
MLP on Program Features (2020)
        |
        +--- nn-Meter (kernel-level)
        |
        +--- HELP (meta-learning)
        |
        v
GNN on Computational Graphs (2021-2022)
        |
        +--- CALO-GNN (uncertainty)
        |
        v
Transformers + Hybrid Approaches (2023-present)
        |
        +--- TLP (transformer encoder)
        |
        +--- NeuSight (physics-informed)
        |
        +--- LitePred (VAE transfer)
```

---

## 9. References

1. Zhang, L., et al. (2021). nn-Meter: Towards Accurate Latency Prediction of Deep-Learning Model Inference on Diverse Edge Devices. MobiSys.

2. Chen, T., et al. (2018). TVM: An Automated End-to-End Optimizing Compiler for Deep Learning. OSDI.

3. Zheng, L., et al. (2020). Ansor: Generating High-Performance Tensor Programs for Deep Learning. OSDI.

4. Lee, S., et al. (2021). Hardware-Adaptive Efficient Latency Prediction for NAS via Meta-Learning. NeurIPS.

5. Zheng, L., et al. (2021). TenSet: A Large-scale Program Performance Dataset for Learned Tensor Compilers. NeurIPS.

6. Feng, Y., et al. (2024). LitePred: Transferable and Scalable Latency Prediction for Hardware-Aware Neural Architecture Search. NSDI.

7. Zhai, J., et al. (2023). TLP: A Deep Learning-Based Cost Model for Tensor Program Tuning. ASPLOS.

8. Various. (2024). CALO-GNN: GNN Cost Model with Calibrated Uncertainty. OpenReview.

9. Yu, P., et al. (2025). NeuSight: Near-Instant Neural Network Inference via Tile-Based GPU Performance Prediction. ASPLOS.

10. Kadlecova, K., et al. (2024). GRAF: Graph Features for Neural Architecture Search. ICML.

---

*Analysis by Leo | ML Performance Survey Project*
