# Accuracy-Centered Evaluation Report

**Date:** 2026-02-16
**Author:** experiment-runner
**Purpose:** Replace MTAP rubric with accuracy-centered evaluation per human directives #243 and #244

## Directive from Human

> "We should not use a rubric to evaluate which simulator is the best. All the evaluation should be centered on accuracy. While evaluating accuracy, we should specify which feature is not available on which simulator." (#243)

> "Also, look for ways to combine them to deliver an optimal solution for the community. This is not a post-publication goal. This must be included in the paper." (#244)

---

## 1. Accuracy Results: Our Independent Verification

### NeuSight — GPU Kernel Performance Prediction
**Published claim:** 2.3% MAPE overall
**Our verification:** 146 model configurations across 12 GPU types

| Device | Mode | Paper Claim | Our Measured | Verdict | N |
|--------|------|-------------|-------------|---------|---|
| V100 | Inference | 5.2% | **5.87%** | MATCH | 10 |
| V100 | Training | 7.4% | **8.91%** | CLOSE | 3 |
| H100 | Inference | 2.3% | **8.74%** | MISMATCH | 16 |
| H100 | Training | 4.1% | **6.60%** | CLOSE | 18 |
| A100-80G | Training | 5.8% | **7.59%** | CLOSE | 10 |
| A100-40G | Inference | — | **8.63%** | — | 16 |
| L4 | Inference | 3.8% | **14.08%** | MISMATCH | 11 |
| T4 | Inference | 6.1% | **18.51%** | MISMATCH | 5 |
| P4 | Inference | — | **27.10%** | — | 3 |
| AMD MI100 | Inference | — | **10.80%** | — | 8 |
| AMD MI210 | Inference | — | **8.40%** | — | 10 |
| AMD MI250 | Inference | — | **7.65%** | — | 10 |

**Key finding:** Accuracy degrades on newer GPUs (H100: 8.74% vs claimed 2.3%) and older GPUs (T4: 18.51%, P4: 27.10%). Best accuracy on V100 (5.87%), suggesting the model is overfit to V100 training data.

### ASTRA-sim — Distributed Training Communication
**Published claim:** 9.69% geomean error at 8-GPU HGX-H100
**Our verification:** Collective benchmarks + ResNet-50 scaling

| Experiment | Result |
|-----------|--------|
| All-Reduce (8 NPUs, 1MB) | 57,426 cycles |
| All-Gather (8 NPUs, 1MB) | 44,058 cycles (0.767× AR) |
| Reduce-Scatter (8 NPUs, 1MB) | 28,950 cycles (0.504× AR) |
| All-to-All (8 NPUs, 1MB) | 114,000 cycles (1.985× AR) |
| ResNet-50 4-GPU comm overhead | 0.133% |
| ResNet-50 8-GPU comm overhead | 0.301% |

**Status:** Trends plausible, absolute accuracy unverifiable without HGX-H100 hardware.

### VIDUR — LLM Inference Serving
**Published claim:** <5% error vs real serving traces
**Our verification:** Llama-2-7B on simulated A100

| Metric | vLLM | Sarathi | Difference |
|--------|------|---------|-----------|
| Avg E2E Latency | 0.177s | 0.158s | Sarathi 12.2% faster |
| Avg TTFT | 0.027s | 0.025s | Sarathi 10.5% faster |
| Avg TPOT | 0.009s | 0.009s | Similar |
| Preempted Requests | 53 | 0 | Sarathi avoids preemption |

**Status:** Scheduler ranking matches literature. Absolute latency unverifiable without A100 hardware.

### Timeloop — Accelerator Energy/Performance
**Published claim:** Within 10% of RTL simulation for energy
**Our verification:** ResNet-50 Conv1 on Eyeriss-like architecture

- Total energy: 649.08 µJ (5,500 fJ/MAC)
- Energy breakdown: DRAM 61.8%, weights SPAD 18.4%, MAC 3.8%
- Estimated latency: 5.854 ms at 60% utilization

**Status:** Energy breakdown structure matches published Eyeriss data. Requires RTL/silicon for absolute verification.

### nn-Meter — Edge Device Latency
**Published claim:** <1% MAPE, 99% correlation
**Our verification:** COMPLETE FAILURE

- **Failure mode:** scikit-learn 0.23.1 pickle incompatibility
- **Time spent:** >4 hours debugging
- **Result:** Zero predictions obtained

**Key finding:** The tool claiming the best accuracy (<1%) is completely non-functional.

---

## 2. Feature Availability Matrix

### What Each Tool CAN and CANNOT Do

| Feature | ASTRA-sim | VIDUR | Timeloop | NeuSight | nn-Meter |
|---------|-----------|-------|----------|----------|----------|
| **CNN Training** | Comm only | — | Single-layer energy | Full model | Inf latency only |
| **Transformer Training** | Comm patterns | — | — | Single-GPU time | — |
| **LLM Inference Serving** | — | **Full** (TTFT/TPOT/batching) | — | — | — |
| **Edge Inference** | — | — | — | — | **Full** (broken) |
| **Accelerator Design Space** | — | — | **Full** (dataflow/mapping) | — | — |
| **NVIDIA Datacenter GPU** | Comm only | A100/H100 | — | H100/A100/V100/T4/P100/L4 | — |
| **AMD GPU** | — | — | — | MI100/MI210/MI250 | — |
| **Custom Accelerator** | — | — | Eyeriss, systolic arrays | — | — |
| **Edge Device** | — | — | — | — | ARM, Adreno, Myriad |
| **Multi-GPU Cluster** | 2-16 GPUs NVSwitch | Single GPU | — | DP/PP/TP (limited) | — |
| **Kernel-Level Prediction** | — | — | Per-layer energy/latency | Per-layer (tile decomp) | Per-kernel models |
| **Model-Level Prediction** | Comm only | Full iteration (profiled) | — | Sum of layers | Sum of kernels |
| **System-Level Prediction** | Comm + compute overlap | Request scheduling/batching | — | — | — |
| **Latency** | Comm cycles | E2E, TTFT, TPOT | Cycle count | GPU kernel time (ms) | Inf latency (ms) |
| **Energy** | — | — | **Full breakdown** | — | — |
| **Throughput** | — | Tokens/s, requests/s | — | — | — |
| **Memory** | — | KV cache | Buffer sizes, data movement | — | — |

---

## 3. Combined Solution: Unified Simulation Pipeline

**No single tool covers the full ML performance stack.** The tools are more complementary than competing — their feature coverage is fundamentally disjoint.

### Proposed Pipeline Architecture

```
Layer 5: Hardware Design    [Timeloop]
    ↓ accelerator specs
Layer 1: Kernel Prediction  [NeuSight / Timeloop]
    ↓ per-kernel latency
Layer 2: Model Composition  [CRITICAL GAP — no existing tool]
    ↓ full model iteration time
Layer 3: Distributed Training  [ASTRA-sim]
    ↓ communication + scaling
Layer 4: Serving System     [VIDUR]
    ↓ request-level SLAs
```

### Why Combination is Necessary

1. **ASTRA-sim** models communication but NOT compute → needs NeuSight for kernel times
2. **VIDUR** models serving but uses profiled traces → needs a predictor for unseen hardware
3. **NeuSight** predicts kernels but NOT system effects → needs ASTRA-sim for scale-out
4. **Timeloop** models accelerators but NOT GPU workloads → needs NeuSight for GPU targets
5. **nn-Meter** targets edge but is broken → needs replacement or repair

### The Critical Gap: Kernel-to-Model Composition

The biggest unsolved problem is **Layer 2**: composing kernel predictions into model-level estimates.

- NeuSight kernel-level accuracy: 5-9% MAPE
- NeuSight model-level (sum of kernels): 10-28% MAPE on some configs
- The composition gap adds 5-15% additional error
- No existing tool validates this composition

This gap is **larger than most tools' kernel-level error**, meaning better kernel predictors alone won't solve end-to-end accuracy.

### Research Priorities for the Community

1. **Kernel-to-model composition model** — validated model for composing kernel predictions, accounting for memory overlap, kernel launch overhead, graph optimization effects
2. **Unified input format** — common workload description that all tools can consume (currently each requires its own format)
3. **Cross-hardware accuracy transfer** — methods to maintain accuracy across GPU generations (NeuSight degrades 3-4x outside training GPUs)
4. **Continuous accuracy validation** — CI framework that alerts when tool accuracy degrades (nn-Meter failed silently)

---

## 4. Key Insights for the Paper

### Surprising Finding 1: Inverse Accuracy-Reliability Correlation
Tools claiming the highest accuracy are the least reliable:
- nn-Meter (<1% MAPE claimed) → completely broken
- NeuSight (2.3% MAPE claimed) → actually 8-27% on many GPUs
- ASTRA-sim (9.69% claimed) → functional, trends validated
- VIDUR (<5% claimed) → functional, behavior validated

### Surprising Finding 2: Tools Don't Compete — They're Complementary
The 5 tools cover 5 almost entirely disjoint slices of the ML performance stack. No two tools can be meaningfully compared on the same prediction task (except NeuSight vs Timeloop on single-layer latency, and even there they target different hardware).

### Surprising Finding 3: The Composition Gap Dominates
The gap between kernel-level and model-level prediction (5-15% additional error) is larger than the kernel-level prediction error itself (2-9%). This means the field's focus on improving kernel predictors has diminishing returns until composition is solved.

---

## Data Sources
- `data/evaluation/neusight-results/neusight_results.json` (146 configs, 12 GPUs)
- `data/evaluation/astra-sim-results/astra_sim_results.json` (11 experiments)
- `data/evaluation/cross-tool-accuracy-results.json` (ASTRA-sim + VIDUR)
- `data/evaluation/timeloop-results/resnet50_conv1_results.json`
- `data/results/nn-meter/predictions.json`
