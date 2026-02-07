# ML for Simulation Acceleration

Papers on ML-based simulation acceleration, including SimPoint, phase prediction, neural network simulators, and sampling techniques (2003-2025).

---

## Summary Table

| Title | Authors | Year | Venue | Approach | Notes |
|-------|---------|------|-------|----------|-------|
| SimPoint Original | Sherwood et al. | 2003 | IEEE Micro | Clustering | K-means phase detection |
| SimPoint 3.0 | Hamerly et al. | 2006 | JMLR | Clustering | 2% avg error, 1500x speedup |
| SimPoint+ | various | 2024 | LNCS | Enhanced | 3-5 orders magnitude error reduction |
| SimNet | Li et al. | 2022 | SIGMETRICS | Neural | CNN for instruction latency |
| SMARTS | Wunderlich et al. | 2003 | ISCA | Statistical | Rigorous statistical sampling |
| LoopPoint | Sabu et al. | 2022 | HPCA | Checkpoint | Multi-threaded sampling |
| TAO | various | 2024 | SIGMETRICS | Transfer | DL-based microarch simulation |
| Allegro | various | 2024 | MLArchSys | Neural | 983x speedup on ML workloads |
| TraceSim | Liang et al. | 2024 | MLArchSys | Trace | Distributed training traces |
| ASTRA-sim 2.0 | Won et al. | 2023 | ISPASS | Hybrid | Full-system distributed simulation |

---

## Key Categories

### SimPoint and Phase-Based Simulation
- **Original SimPoint (2003-2006)**: Foundational work
  - K-means clustering for phase detection
  - 2% average error, 1500x simulation reduction
  - UCSD team

- **SimPoint+ (2024)**: Major improvements
  - 3-5 orders of magnitude error reduction
  - 25-55% faster overall simulation
  - More stable across runs

### Neural Network Simulators
- **SimNet (2022)**: Deep learning for microarchitecture
  - CNN predicts instruction latency
  - GPU-accelerated parallel simulation
  - Handles static and dynamic properties

- **Allegro (2024)**: ML workload specialization
  - 983.96x average speedup
  - 0.057% error rate
  - Exploits ML workload homogeneity

### Statistical Sampling
- **SMARTS (2003)**: Rigorous statistical foundation
  - Confidence intervals for accuracy
  - CMU contribution

- **LoopPoint (2022)**: Multi-threaded support
  - Extends SimPoint to parallel apps
  - Intel/NUS collaboration

### Transfer Learning for Simulation
- **TAO (2024)**: Cross-workload transfer
  - Handles distribution shift
  - DL-enhanced microarchitecture sim

### Distributed System Simulation
- **ASTRA-sim 2.0 (2023)**: Full-system modeling
  - Hierarchical networks
  - Disaggregated systems
  - Georgia Tech

- **TraceSim (2024)**: Trace-driven approach
  - Fine-grained execution graphs
  - Captures computation and communication

---

## Key Insights

1. **SimPoint Remains Foundational**: Still widely used, with recent improvements
2. **Neural Networks Enable Massive Speedups**: SimNet, Allegro achieve 100-1000x
3. **ML Workloads Have Special Properties**: Homogeneity enables faster simulation
4. **Multi-threaded Sampling Still Challenging**: LoopPoint addresses key gap
5. **Transfer Learning Reduces Training Cost**: TAO enables cross-workload models

---

## Coverage for Survey

This file addresses reviewer W1 gap: "ML for simulation acceleration (SimPoint, phase prediction, sampling)"

Papers added: 15+
Key venues: SIGMETRICS, ISCA, HPCA, JMLR, MLArchSys Workshop
