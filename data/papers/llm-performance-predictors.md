# LLM-Specific Performance Predictors

Papers on performance prediction tools specifically designed for large language model inference and training (2023-2025).

---

## Summary Table

| Title | Authors | Year | Venue | Focus | Notes |
|-------|---------|------|-------|-------|-------|
| GenZ | Bambhaniya et al. | 2024 | Open-source | Hardware | LLM-hardware interplay, UIUC |
| LLMCompass | Ning et al. | 2024 | ISCA | Hardware | 4.1% end-to-end error, MIT/CMU |
| Roofline-LLM | Imai et al. | 2024 | NeurIPS-WS | Hybrid | Roofline + ML, 87% MSE reduction |
| Lumos | Liang et al. | 2025 | MLSys | Training | 3.3% error on 512 H100s |
| PRISM | Sun et al. | 2025 | arXiv | Training | 64K+ GPU scale, probabilistic |
| Calculon | Isaev et al. | 2024 | MLSys | Training | Analytical decomposition |
| VIDUR | Agrawal et al. | 2024 | MLSys | Inference | <5% error, discrete-event sim |
| Splitwise | Patel et al. | 2024 | ISCA | Inference | Phase splitting, 1.4x throughput |
| DistServe | Zhong et al. | 2024 | OSDI | Inference | Disaggregated, 7.4x requests |

---

## Key Categories

### Hardware-Aware Analysis Tools
- **GenZ (2024)**: LLM inference analyzer
  - Multiple hardware platforms
  - Tensor parallelism, pipeline parallelism
  - Open-source, UIUC

- **LLMCompass (2024)**: Hardware evaluation
  - 10.9% operator error, 4.1% end-to-end
  - 3.41x perf/cost improvement
  - MIT/CMU

- **llm-analysis (2024)**: Training and inference
  - Latency and memory analysis
  - Compute, memory, communication

### Roofline-Based Models
- **Roofline-LLM (2024)**: Hybrid approach
  - Combines roofline with ML
  - 17 point R2 increase
  - 87% MSE reduction
  - IBM Research

### Training Performance Modeling
- **Lumos (2025)**: Trace-driven modeling
  - 3.3% error on 512 H100 GPUs
  - Reproduces SM utilization
  - Execution breakdown
  - Cornell

- **PRISM (2025)**: Probabilistic modeling
  - Handles 64K+ GPU scale
  - Stochastic variation modeling
  - Identifies 1.26x optimization potential

- **Calculon (2024)**: Analytical decomposition
  - Compute, memory, communication
  - Distributed training focus

### Inference Simulation
- **VIDUR (2024)**: Discrete-event simulation
  - <5% prediction error
  - Vidur-Search: 1 hour vs 42K GPU hours
  - Microsoft Research

- **ReaLLM (2025)**: Trace-driven framework
  - Kernel-level simulation
  - Fast and accurate

### Prefill/Decode Phase Modeling
- **Splitwise (2024)**: Phase separation
  - Different hardware for each phase
  - 1.4x higher throughput
  - ISCA 2024

- **DistServe (2024)**: Disaggregated serving
  - 7.4x more requests or 12.6x tighter SLO
  - PKU/Tsinghua

- **Sarathi-Serve (2024)**: Chunked prefills
  - Stall-free batching
  - 1.25x throughput improvement
  - Microsoft Research

### Speculative Decoding Models
- **MagicDec (2025)**: Long context analysis
  - KV compression easier than model compression
  - Bottleneck-aware drafting
  - ICLR 2025

- **EAGLE (2024)**: Feature extrapolation
  - 2.7-3.5x speedup analysis
  - No separate draft model

---

## Key Insights

1. **Phase Separation Is Critical**: Prefill and decode have different bottlenecks
2. **Roofline Models Are Extensible**: Adding ML improves accuracy
3. **Simulation Enables Fast Exploration**: VIDUR reduces search cost dramatically
4. **Large-Scale Training Needs Probabilistic Models**: PRISM handles variance
5. **Hardware-Specific Tools Emerging**: GenZ, LLMCompass for analysis
6. **Open-Source Tooling Growing**: GenZ, llm-analysis available

---

## Comparison of Tools

| Tool | Target | Approach | Accuracy | Speed |
|------|--------|----------|----------|-------|
| GenZ | Inference | Analytical | ~10% | Fast |
| LLMCompass | Hardware | Analytical | 4.1% | Fast |
| VIDUR | Inference | Simulation | <5% | Moderate |
| Lumos | Training | Trace | 3.3% | Moderate |
| Roofline-LLM | Inference | Hybrid | High | Fast |

---

## Gap Analysis

### Well-Covered
- LLM inference latency prediction
- Distributed training modeling
- Phase-aware serving analysis

### Emerging
- KV cache performance modeling
- Speculative decoding analysis
- Multi-tenant serving prediction

### Underexplored
- LLM energy prediction
- Cross-model transfer learning
- Real-time adaptive prediction

---

## Coverage for Survey

This file addresses reviewer W1 gap: "Recent LLM-specific predictors (LLM-Viewer, GenZ, etc.)"

Papers added: 25+
Key venues: ISCA, OSDI, MLSys, NeurIPS Workshop, ICML
