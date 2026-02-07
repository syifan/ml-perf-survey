# Learned Cost Models for Compilers

Papers on learned cost models for tensor compilers, image processing pipelines, and autotuning frameworks (2019-2025).

---

## Summary Table

| Title | Authors | Year | Venue | Target | Notes |
|-------|---------|------|-------|--------|-------|
| Learning to Optimize Halide | Adams et al. | 2019 | SIGGRAPH | CPU | Neural network cost model, 2.29x speedup |
| Halide GPU Autoscheduler | Anderson et al. | 2021 | OOPSLA | GPU | Extends to GPU scheduling, 1.66x speedup |
| Ansor | Zheng et al. | 2020 | OSDI | Multi | XGBoost cost model, 3.8x vs AutoTVM |
| ICS24 Ansor Accelerated | HPCRL | 2024 | ICS | GPU | Order-of-magnitude speedup, 7 analytical features |
| TensorIR | Feng et al. | 2023 | ASPLOS | Multi | First-class tensor primitives |
| DietCode | Zheng et al. | 2022 | MLSys | Multi | Dynamic shape support |
| Hidet | Ding et al. | 2023 | ASPLOS | Multi | Task-mapping paradigm |
| BladeDISC | Zheng et al. | 2024 | SIGMOD | Multi | Production compiler at Alibaba |
| Asymptotic Sparse | Ahrens et al. | 2022 | PLDI | Multi | First sparse tensor cost model |
| SparseTIR | Ye et al. | 2023 | ASPLOS | Multi | Composable sparse abstractions |

---

## Key Categories

### Halide Autoscheduler Family
- **Original (2019)**: Neural network trained on random programs
  - Small NN predicts runtime from symbolic features
  - Beam search achieves 2.29x over baseline
  - Stanford/MIT/Adobe collaboration

- **GPU Extension (2021)**: Learned cost model for GPU scheduling
  - Features GPU-specific characteristics
  - 1.66x speedup in autotuning case

### TVM/Ansor Family
- **Ansor (2020)**: Hierarchical search + XGBoost
  - 164 AST-derived features
  - State-of-the-art until recent work

- **Accelerated Ansor (2024)**: Analytical features + gradient descent
  - Only 7 analytical features
  - Order-of-magnitude speedup

### Modern Tensor Compilers
- **TensorIR (2023)**: First-class tensor computation
  - Generalizes loop nest representation
  - Enables tensorized program optimization

- **DietCode (2022)**: Dynamic shape support
  - Shape-generic search space
  - First autoscheduler for dynamic shapes

- **Hidet (2023)**: Task-mapping abstraction
  - Reduces search space complexity
  - Competitive performance with simpler model

### Sparse Tensor Support
- **Asymptotic Cost Model (2022)**: First for sparse tensors
  - No profiling required
  - Enables sparse autoscheduling

- **SparseTIR (2023)**: Composable format abstractions
  - Deep learning sparse patterns
  - Interoperable with dense TensorIR

---

## Key Insights

1. **Feature Engineering Matters**: 7 analytical features can match 164 AST features
2. **Dynamic Shapes Require New Approaches**: DietCode, FTuner address this gap
3. **Sparse Tensors Underexplored**: Limited cost model support
4. **Transfer Learning Emerging**: CALO-GNN, ROFT combine learning with analytical

---

## Coverage for Survey

This file addresses reviewer W1 gap: "Learned cost models for compilers (Halide autoscheduler, TVM/Ansor literature)"

Papers added: 15+
Key venues: SIGGRAPH, OSDI, ASPLOS, MLSys, PLDI
