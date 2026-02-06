# Emerging Topics in ML Performance Modeling

Literature search for emerging research areas that may expand the survey's scope.
Compiled by Maya (Literature Scout) for issue #38.

---

## 1. Foundation Models for Architecture and Hardware Design

LLMs and foundation models are increasingly being applied to hardware design and performance prediction tasks.

### Key Papers

| Paper | Venue | Year | Summary |
|-------|-------|------|---------|
| **LLMCompass** | ISCA | 2024 | Hardware evaluation framework for LLM inference with 10.9% operator error and 4.1% end-to-end error. Enables design space exploration achieving 3.41x performance/cost improvement over A100. |
| **ChipNeMo** | arXiv | 2024 | NVIDIA domain-adapted LLMs for chip design using domain-adaptive tokenization and continued pretraining. 5x model size reduction with similar performance on EDA scripting, chatbot, and bug analysis. |
| **GPT4AIGChip** | arXiv | 2024 | LLM-powered framework for AI accelerator design from natural language descriptions with automated prompt generation. |
| **LLM4HWDesign** | ICCAD | 2024 | Community dataset and benchmark for LLM-assisted hardware code generation covering synthesis, simulation, and verification. |

### Observations

- LLMCompass demonstrates that analytical frameworks can achieve <5% error for LLM inference prediction
- Domain adaptation (ChipNeMo) enables smaller models to match larger general-purpose LLMs on chip design tasks
- Current LLMs struggle with detailed hardware specifications but show promise for routine design tasks

---

## 2. AutoML and NAS Integration with Performance Models

Hardware-aware Neural Architecture Search (NAS) increasingly relies on accurate performance predictors.

### Key Papers

| Paper | Venue | Year | Summary |
|-------|-------|------|---------|
| **ESM** | DAC | 2025 | Framework for building effective surrogate models for HW-NAS with novel FCC encoding. 97.6% accuracy across GPUs, CPUs, and embedded devices. |
| **LitePred** | NSDI | 2024 | Transfer learning for latency prediction using VAE data sampler. 99.3% accuracy on 85 edge platforms with 50.6x profiling cost reduction. |
| **HELP** | NeurIPS | 2021 | Meta-learning for hardware-adaptive latency prediction with novel hardware embeddings. Achieves high accuracy with only 10 samples per new platform. |
| **Once-for-All (OFA)** | ICLR | 2020 | Progressive shrinking for hardware-aware deployment. Single supernet supports diverse platforms (Mobile, CPU, GPU, FPGA). |
| **On Latency Predictors** | MLSys | 2024 | Comprehensive study of NAS latency predictors showing 22.5% improvement with transfer learning. |
| **MicroNAS** | Scientific Reports | 2025 | NAS for time series on microcontrollers with memory and latency constraints. |

### Observations

- Transfer learning is key to reducing profiling cost while maintaining accuracy (LitePred, HELP)
- Surrogate models must balance accuracy with data collection efficiency
- Hardware embeddings enable generalization to unseen platforms with minimal samples

---

## 3. Uncertainty Quantification in Performance Prediction

Providing confidence intervals and calibrated predictions is critical for production deployment.

### Key Papers

| Paper | Venue | Year | Summary |
|-------|-------|------|---------|
| **PRISM** | arXiv | 2025 | Probabilistic performance modeling for distributed training at 64K+ GPU scale. Handles stochastic variation with 20.8% KS distance accuracy. Identifies 1.26x optimization potential. |
| **Conformal Prediction for CL** | ICML | 2025 | Model uncertainty quantification via conformal prediction in continual learning with asymptotic coverage guarantee. |
| **CP for NLP Survey** | TACL | 2024 | Survey of conformal prediction for NLP providing distribution-free guarantees for LLM uncertainty. |
| **Uncertainty in GNNs** | arXiv | 2024 | Survey on GNN uncertainty covering aleatoric and epistemic uncertainty estimation. |
| **Calibration Survey** | arXiv | 2024 | Survey of deep learning calibration methods including Top-versus-All post-hoc calibration. |
| **Bayesian UQ for RUL** | IJSAEM | 2024 | BNN for remaining useful life prediction with implicit uncertainty modeling. |
| **UQ for Engineering** | ML4CSE | 2024 | Survey of GP, ANN, PINN for uncertainty quantification in engineering systems. |

### Observations

- Conformal prediction offers distribution-free guarantees suitable for production ML
- At large scale (64K+ GPUs), stochastic variation becomes significant and must be modeled (PRISM)
- Bayesian methods provide principled uncertainty but face scalability challenges

---

## 4. Online Learning and Adaptive Performance Models

Models that adapt to deployment data and handle data drift are essential for production systems.

### Key Papers

| Paper | Venue | Year | Summary |
|-------|-------|------|---------|
| **DaCapo** | ISCA | 2024 | Hardware-algorithm co-design for continuous learning in video analytics. 6.5% higher accuracy than Ekya with 254x less power. Distinguished Artifact Award. |
| **Ekya** | NSDI | 2022 | Continuous learning on edge with Thief Scheduler for resource-accuracy tradeoff. Handles data drift with micro-profiling. 29% accuracy gain with 4x less GPU resources. |
| **Lumos** | MLSys | 2025 | Trace-driven performance modeling for LLM training. 3.3% error on 512 H100 GPUs. Reproduces execution breakdown and SM utilization without custom instrumentation. |
| **VIDUR** | MLSys | 2024 | Discrete-event simulation for LLM serving with <5% error. Vidur-Search finds optimal deployment config in 1 hour vs 42K GPU hours. |
| **CLONE (ATC)** | ATC | 2025 | MoE router for adaptive LoRA integration with DVFS for per-token energy optimization while meeting latency constraints. |
| **Drift Detection MLOps** | ResearchGate | 2024 | Comprehensive MLOps for drift detection using statistical process control and adaptive windowing. |
| **PELT Drift Detection** | ScienceDirect | 2025 | PELT algorithm for drift detection with selective model retraining in dynamic environments. |

### Observations

- Continuous learning systems (DaCapo, Ekya) address data drift in edge deployment
- Trace-driven approaches (Lumos, VIDUR) enable accurate prediction without expensive profiling
- Drift detection is critical: 75% of businesses report AI performance decline without monitoring
- Hardware-algorithm co-design yields significant efficiency gains (254x power reduction in DaCapo)

---

## Summary and Survey Integration

These emerging topics suggest several directions for expanding the survey:

1. **Foundation Models for Design**: LLMCompass and ChipNeMo represent a new paradigm where LLMs assist in hardware design and performance prediction, bridging the gap between natural language specifications and hardware implementations.

2. **Integrated AutoML/NAS**: Performance models are increasingly embedded within AutoML pipelines, requiring both accuracy and sample efficiency. Transfer learning and meta-learning are key enablers.

3. **Quantified Uncertainty**: Production deployment requires not just predictions but confidence intervals. Conformal prediction and probabilistic modeling (PRISM) address this need.

4. **Adaptive Systems**: Real-world deployment faces data drift and changing workloads. Online learning systems (DaCapo, Ekya) and drift detection are essential for maintaining model accuracy over time.

---

## Paper Count Summary

| Category | Papers |
|----------|--------|
| Foundation Models for Architecture | 4 |
| AutoML/NAS Integration | 6 |
| Uncertainty Quantification | 7 |
| Online Learning/Adaptive Models | 7 |
| **Total** | **24** |

---

*Generated: February 2026*
