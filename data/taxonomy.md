# Paper Categorization Taxonomy

This taxonomy defines the classification scheme for categorizing ML performance modeling papers.

---

## 1. Modeling Approach

How the performance model generates predictions.

| Category | Description |
|----------|-------------|
| **Analytical** | Closed-form equations based on hardware/software parameters (e.g., roofline model) |
| **Simulation** | Cycle-accurate or functional simulation of hardware execution |
| **ML-Based** | Machine learning models trained on profiling data (regression, neural networks, etc.) |
| **Hybrid** | Combines multiple approaches (e.g., analytical model augmented with ML correction) |

---

## 2. Target Hardware

The hardware platform(s) the model predicts performance for.

| Category | Description |
|----------|-------------|
| **GPU** | NVIDIA, AMD, or other discrete GPUs |
| **TPU** | Google Tensor Processing Units |
| **CPU** | General-purpose processors |
| **NPU/Accelerators** | Custom DNN accelerators (e.g., Eyeriss, Simba, edge NPUs) |
| **Multi-Device** | Distributed systems, multi-GPU, or heterogeneous platforms |
| **FPGA** | Field-programmable gate arrays |

---

## 3. Target Workloads

The types of ML models/workloads the performance model covers.

| Category | Description |
|----------|-------------|
| **CNN** | Convolutional neural networks (ResNet, VGG, EfficientNet, etc.) |
| **Transformer** | Attention-based models (BERT, GPT, ViT, LLMs) |
| **RNN/LSTM** | Recurrent neural networks |
| **GNN** | Graph neural networks |
| **General DNN** | Operator-level or framework-agnostic modeling |
| **Specific Operators** | Focused on GEMM, convolution, attention, or other primitives |

---

## 4. Prediction Target

What performance metric(s) the model predicts.

| Category | Description |
|----------|-------------|
| **Latency** | End-to-end or per-layer execution time |
| **Throughput** | Samples/second, tokens/second, FLOPS achieved |
| **Energy** | Power consumption or energy per inference |
| **Memory** | Memory footprint, bandwidth utilization, or memory access patterns |
| **Multi-Objective** | Combines multiple targets (e.g., Pareto-optimal latency-energy) |

---

## 5. Accuracy Metrics

How prediction quality is evaluated.

| Metric | Description |
|--------|-------------|
| **MAPE** | Mean Absolute Percentage Error |
| **RMSE** | Root Mean Square Error |
| **Correlation** | Pearson or Spearman correlation coefficient |
| **Ranking Accuracy** | Ability to correctly rank configurations (e.g., Kendall's tau) |
| **Relative Error** | Median or percentile-based relative error |

---

## 6. Input Requirements

What information the model requires to make predictions.

| Category | Description |
|----------|-------------|
| **Graph-Only** | Only computational graph/operator sequence (no profiling) |
| **Static Analysis** | Requires model architecture + hardware specs |
| **Profiling-Based** | Requires runtime measurements (microbenchmarks, traces) |
| **Hardware Counters** | Requires access to performance counters |
| **Transfer Learning** | Trained on one platform, adapted to another |

---

## 7. Evaluation Scope

How comprehensive the model's evaluation is.

| Category | Description |
|----------|-------------|
| **Single Model** | Evaluated on one or few specific networks |
| **Model Family** | Evaluated across variants (e.g., ResNet-18 to ResNet-152) |
| **Cross-Architecture** | Evaluated on diverse model types (CNN + Transformer) |
| **Cross-Platform** | Evaluated on multiple hardware platforms |

---

## 8. Reproducibility

Availability of code, data, and documentation.

| Level | Description |
|-------|-------------|
| **Full** | Code + trained models + datasets publicly available |
| **Partial** | Code available but missing data or models |
| **None** | No public artifacts |

---

## Usage

When analyzing a paper, classify it along each dimension. Example:

```
Paper: "NeuralPredict: Fast DNN Performance Modeling"
- Modeling Approach: ML-Based
- Target Hardware: GPU
- Target Workloads: CNN, Transformer
- Prediction Target: Latency
- Accuracy Metrics: MAPE (8.5%), Correlation (0.97)
- Input Requirements: Graph-Only
- Evaluation Scope: Cross-Architecture
- Reproducibility: Partial (code available)
```
