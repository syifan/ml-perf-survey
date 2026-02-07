# Selected Papers for Experimental Evaluation

This document identifies key papers and tools from our literature survey for experimental evaluation. Selection is based on: open-source availability, reproducibility, impact, and coverage across different modeling approaches.

---

## Selection Summary

| # | Paper/Tool | Category | Repository | Hardware Req |
|---|------------|----------|------------|--------------|
| 1 | Timeloop | Analytical | NVlabs/timeloop | CPU only |
| 2 | nn-Meter | ML-Based | microsoft/nn-Meter | Edge devices |
| 3 | ASTRA-sim | Simulation | astra-sim/astra-sim | CPU only |
| 4 | VIDUR | LLM Simulation | microsoft/vidur | CPU only |
| 5 | NeuSight | ML-Based | microsoft/neusight | NVIDIA GPU |

---

## 1. Timeloop (Analytical)

**Paper:** Timeloop: A Systematic Approach to DNN Accelerator Evaluation (ISPASS 2019)

**Authors:** Parashar et al. (NVIDIA, MIT)

### Why Selected

- **Foundational:** Most-cited analytical framework for DNN accelerator modeling
- **Industry adoption:** Used in 100+ papers, maintained by NVIDIA
- **Comprehensive:** Models energy, latency, and area for spatial architectures
- **Well-documented:** Extensive tutorials and examples

### Repository

- **URL:** https://github.com/NVlabs/timeloop
- **License:** BSD 3-Clause
- **Last Updated:** Active development (2024)
- **Stars:** 400+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full source code |
| Documentation | Excellent | Tutorials, examples, wiki |
| Dependencies | Standard | C++, Python, Accelergy for energy |
| Pre-built configs | Yes | Multiple accelerator examples |
| Docker support | Yes | Available |

### Evaluation Plan

1. **Setup:** Install via Docker or source
2. **Workloads:** Run on ResNet-50, BERT, MobileNet layers
3. **Metrics:** Compare predicted vs. published accuracy claims (5-10% error)
4. **Time:** Measure exploration speed (mappings/second)

### Hardware Requirements

- **Minimum:** Linux, 8GB RAM, multi-core CPU
- **Recommended:** 16GB RAM for large design spaces
- **GPU:** Not required

---

## 2. nn-Meter (ML-Based Edge Latency)

**Paper:** nn-Meter: Towards Accurate Latency Prediction of Deep-Learning Model Inference on Diverse Edge Devices (MobiSys 2021, Best Paper)

**Authors:** Zhang et al. (Microsoft Research)

### Why Selected

- **State-of-the-art accuracy:** 99% on edge devices
- **Practical impact:** Used in Azure ML for hardware-aware NAS
- **Novel approach:** Kernel-level decomposition with adaptive sampling
- **Well-maintained:** Active development by Microsoft

### Repository

- **URL:** https://github.com/microsoft/nn-Meter
- **License:** MIT
- **Last Updated:** 2024
- **Stars:** 700+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full framework + predictors |
| Documentation | Good | README, examples |
| Pre-trained models | Yes | Multiple edge devices |
| Dependencies | Standard | Python, PyTorch/TensorFlow |
| Test datasets | Partial | Some NAS benchmarks |

### Evaluation Plan

1. **Setup:** pip install nn-meter
2. **Workloads:** Predict latency for NAS-Bench models
3. **Validation:** Compare predictions vs. actual measurements on available device
4. **Metrics:** MAPE, correlation with ground truth

### Hardware Requirements

- **Minimum:** Python environment, any modern CPU
- **For validation:** Access to edge device (Pixel phone, Raspberry Pi, or Intel VPU)
- **Note:** Pre-trained predictors available; training new predictors requires target device

---

## 3. ASTRA-sim (Distributed Training Simulation)

**Paper:** ASTRA-sim: Enabling SW/HW Co-Design Exploration for Distributed DL Training Platforms (ISPASS 2020, arXiv 2023)

**Authors:** Won et al. (Georgia Tech, Meta, Intel, AMD)

### Why Selected

- **Unique capability:** Only framework for end-to-end distributed training simulation
- **Industry backing:** Developed with Meta, Intel, AMD
- **Practical scope:** Models compute, memory, and network interactions
- **Active development:** Continuous updates for modern workloads

### Repository

- **URL:** https://github.com/astra-sim/astra-sim
- **License:** MIT
- **Last Updated:** Active (2024)
- **Stars:** 200+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full simulator |
| Documentation | Good | Tutorials, Chakra trace format |
| Example traces | Yes | Sample distributed workloads |
| Network backends | Multiple | Analytical, NS-3, Garnet |
| Dependencies | Moderate | C++, Python, optional NS-3 |

### Evaluation Plan

1. **Setup:** Build from source (CMake)
2. **Workloads:** Run example Chakra traces (GPT-like, ResNet)
3. **Configurations:** Test 2/4/8 GPU setups
4. **Metrics:** Compare scaling efficiency predictions vs. claimed accuracy (5-15% error)

### Hardware Requirements

- **Minimum:** Linux, 16GB RAM, multi-core CPU
- **Recommended:** 32GB RAM for large simulations
- **GPU:** Not required (simulation only)

---

## 4. VIDUR (LLM Inference Simulation)

**Paper:** VIDUR: A Large-Scale Simulation Framework for LLM Inference (MLSys 2024)

**Authors:** Agrawal et al. (Microsoft Research)

### Why Selected

- **Novel contribution:** First comprehensive LLM inference simulator
- **High accuracy:** <5% error on real traces
- **Practical use:** Enables capacity planning without GPU clusters
- **Recent and relevant:** Addresses emerging LLM serving challenges

### Repository

- **URL:** https://github.com/microsoft/vidur
- **License:** MIT
- **Last Updated:** 2024
- **Stars:** 100+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full simulator |
| Documentation | Good | README, examples |
| Sample traces | Yes | Request arrival patterns |
| Serving policies | Multiple | Various scheduling algorithms |
| Dependencies | Standard | Python |

### Evaluation Plan

1. **Setup:** pip install or clone repo
2. **Workloads:** Simulate LLaMA-7B/13B serving with sample traces
3. **Configurations:** Test different scheduling policies (vLLM, Orca-style)
4. **Metrics:** Compare predicted latency/throughput vs. claimed accuracy

### Hardware Requirements

- **Minimum:** Python environment, 8GB RAM
- **Recommended:** 16GB RAM for large trace simulations
- **GPU:** Not required (simulation only)

---

## 5. NeuSight (ML-Based GPU Performance Prediction)

**Paper:** NeuSight: GPU Performance Forecasting via Tile-Based Execution Analysis (ASPLOS 2025)

**Authors:** Lee, Phanishayee, Mahajan (Microsoft Research)

### Why Selected

- **State-of-the-art accuracy:** 97.7% on GPU performance prediction
- **Novel approach:** Tile-based decomposition matching GPU execution model
- **ML-based predictor:** Core topic of survey (unlike optimization kernels)
- **Modern workloads:** Validated on LLMs including GPT-3

### Repository

- **URL:** https://github.com/microsoft/neusight (expected)
- **License:** MIT (typical for Microsoft Research)
- **Last Updated:** 2025
- **Stars:** New release

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Expected | Microsoft Research track record |
| Documentation | Good | Paper provides methodology details |
| Pre-trained models | Expected | For common GPU architectures |
| Dependencies | Standard | Python, PyTorch, CUDA |
| Validation | GPU required | Need GPU for calibration |

### Evaluation Plan

1. **Setup:** Clone repo, install dependencies
2. **Workloads:** Predict latency for ResNet, BERT, GPT models
3. **Validation:** Compare predictions vs. actual GPU execution
4. **Metrics:** MAPE, correlation with ground truth

### Hardware Requirements

- **Minimum:** NVIDIA GPU (Volta or newer)
- **Recommended:** A100 or H100 for full validation
- **For prediction only:** CPU sufficient after calibration

---

## Evaluation Priority and Schedule

### Phase 1: CPU-Only Tools (Week 1-2)

These require no GPU and can be evaluated immediately:

1. **Timeloop** - Analytical modeling validation
2. **ASTRA-sim** - Distributed training simulation
3. **VIDUR** - LLM inference simulation

### Phase 2: Edge/GPU Tools (Week 3-4)

These require specific hardware:

4. **nn-Meter** - Edge latency prediction (needs edge device for validation)
5. **NeuSight** - GPU performance prediction (needs NVIDIA GPU for calibration)

---

## Evaluation Metrics Framework

### Accuracy Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| MAPE | Mean Absolute Percentage Error | <10% |
| Correlation | Spearman rank correlation | >0.9 |
| R-squared | Variance explained | >0.8 |

### Usability Metrics

| Metric | Description |
|--------|-------------|
| Setup time | Time from clone to first run |
| Documentation quality | Completeness and clarity |
| Dependency complexity | Number and obscurity of dependencies |

### Performance Metrics

| Metric | Description |
|--------|-------------|
| Prediction speed | Evaluations per second |
| Scalability | Performance on large design spaces |
| Memory footprint | RAM requirements |

---

## Alternatives Considered (Not Selected)

### GPGPU-Sim/Accel-Sim

- **Reason:** Very slow simulation (1000x+ slowdown), complex setup
- **Alternative:** Use for deep-dive validation if needed

### MAESTRO

- **Reason:** Less active development than Timeloop, similar capability
- **Alternative:** Could evaluate as supplementary

### TVM/Ansor

- **Reason:** Requires GPU for meaningful evaluation, complex autotuning
- **Alternative:** Could demonstrate cost model component

### gem5

- **Reason:** CPU-focused, ML extensions less mature
- **Alternative:** Include if evaluating CPU inference

---

## Expected Outcomes

1. **Validation of accuracy claims** - Verify published error rates
2. **Usability assessment** - Document setup complexity
3. **Comparison table** - Side-by-side tool comparison
4. **Recommendations** - Guide for practitioners on tool selection
5. **Gaps identification** - What's missing from current tools

---

*Document by Leo | ML Performance Survey Project*
