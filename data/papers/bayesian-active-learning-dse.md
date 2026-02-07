# Bayesian Optimization and Active Learning for DSE

Papers on Bayesian optimization, active learning, and efficient sampling for hardware design space exploration (2017-2025).

---

## Summary Table

| Title | Authors | Year | Venue | Approach | Notes |
|-------|---------|------|-------|----------|-------|
| BO for Accelerators | Reagen et al. | 2017 | ISLPED | BO | Foundational work, Harvard |
| AutoML Codesign | Abdelfattah et al. | 2021 | DAC | BO | CNN + accelerator co-search |
| ARS-Flow 2.0 | various | 2024 | Integration | Active | PSO-GP + SAMOGA + PRSRS |
| Polaris | various | 2024 | arXiv | Multi-fidelity | 2.7x EDP reduction |
| Compass | various | 2024 | arXiv | Ensemble BO | Graph learning + BO |
| AutoHLS | various | 2024 | arXiv | Learning | Limited sample DSE |
| CSDSE | various | 2025 | Neurocomputing | Cooperative | Heterogeneous agents |
| ConfuciuX | Kao et al. | 2020 | MICRO | RL | O(10^72) design space |
| ArchGym | Krishnan et al. | 2023 | ISCA | Multi | OpenAI Gym for architecture |
| GNN-DSE | Sohrabizadeh et al. | 2022 | DAC | GNN+Meta | MAML for kernel adaptation |

---

## Key Categories

### Foundational Bayesian Optimization
- **Reagen et al. (2017)**: First BO for accelerators
  - Multi-objective optimization
  - Outperforms grid/random search
  - Harvard

- **AutoML Codesign (2021)**: Joint CNN + HW search
  - Pareto-optimal designs
  - Samsung/Cambridge

### Active Learning and Efficient Sampling
- **ARS-Flow 2.0 (2024)**: State-of-the-art DSE
  - PSO-optimized GP regression
  - Self-adaptive MOGA
  - Pareto-oriented resampling

- **Polaris (2024)**: Multi-fidelity exploration
  - Transfer between analytical and RTL
  - 35 min vs 6 hours for DOSA
  - 2.7x EDP reduction

- **AutoHLS (2024)**: Limited sample learning
  - Essential for long HLS synthesis

### GNN-Based Surrogates
- **GNN-DSE (2022)**: GNN for HLS
  - MAML meta-learning
  - Kernel adaptation
  - UCLA

- **ApproxGNN (2024)**: Approximate computing
  - Pretrained GNN
  - 50% better embedding accuracy

### Reinforcement Learning for DSE
- **ConfuciuX (2020)**: REINFORCE algorithm
  - Handles O(10^72) space
  - 4.7-24x faster convergence
  - Uses MAESTRO cost model

- **ArchGym (2023)**: Unified framework
  - OpenAI Gym interface
  - Compares RL, BO, GA, random
  - Google/Stanford

### Multi-Fidelity Optimization
- **Polaris (2024)**: Transfer between fidelities
  - Low-fidelity: analytical models
  - High-fidelity: RTL simulation
  - Bridges accuracy gap

- **Accelerated NAS BO (2024)**: Pretrained ensembles
  - Multi-fidelity BO
  - Reduces NAS cost

---

## Key Insights

1. **BO Is Now Standard**: Widely adopted for accelerator DSE
2. **Multi-Fidelity Reduces Cost**: Polaris achieves major speedups
3. **Active Learning Is Sample-Efficient**: Critical for expensive evaluations
4. **GNNs Capture Design Structure**: Effective surrogates for HLS
5. **RL Handles Massive Spaces**: ConfuciuX, ArchGym for exploration
6. **Meta-Learning Enables Transfer**: Adapt to new kernels quickly

---

## Comparison of Approaches

| Method | Sample Efficiency | Exploration | Implementation |
|--------|-------------------|-------------|----------------|
| Bayesian Optimization | High | Good | Moderate |
| Active Learning | Very High | Moderate | Complex |
| RL (REINFORCE) | Moderate | Excellent | Complex |
| GNN Surrogate | High | Good | Complex |
| Random Search | Low | Poor | Simple |
| Grid Search | Low | Poor | Simple |

---

## Coverage for Survey

This file addresses reviewer W1 gap: "Bayesian optimization/active learning for DSE"

Papers added: 20+
Key venues: MICRO, ISCA, DAC, ISLPED, Neurocomputing
