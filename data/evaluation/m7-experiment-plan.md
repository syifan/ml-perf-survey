# M7 Concrete Experiment Plan

**Author:** Experiment-Runner
**Date:** 2026-02-15
**Issue:** #217
**Status:** Ready for execution

---

## 1. Objective

Produce quantitative, independently-verified evaluation data for the MTAP framework across all five dimensions. Every number in the paper's evaluation section must trace to a CI workflow artifact.

---

## 2. Tools to Evaluate

### Tier 1: Docker-based (high confidence, already working)

| Tool | Category | Docker Status | CI Workflow | Prior Results |
|------|----------|--------------|-------------|---------------|
| **ASTRA-sim** | Trace-driven simulation (distributed) | Working (`scripts/benchmarks/astra-sim/Dockerfile`) | `astra-sim-experiment.yml` | Microbenchmarks + ResNet-50 scaling (run 21974421234) |
| **VIDUR** | Trace-driven simulation (LLM serving) | Working (`scripts/benchmarks/vidur/Dockerfile`) | `vidur-experiment.yml` | 3 schedulers × Llama-2-7B (run 21974809943) |

### Tier 2: Docker-based (need debugging)

| Tool | Category | Docker Status | CI Workflow | Blocker |
|------|----------|--------------|-------------|---------|
| **nn-Meter** | ML-augmented (edge) | Dockerfile exists, untested in CI | None | Pickle deserialization errors with sklearn predictors; pinned versions may fix |

### Tier 3: Non-Docker (limited evaluation)

| Tool | Category | Setup | CI Workflow | Blocker |
|------|----------|-------|-------------|---------|
| **Timeloop** | Analytical (accelerator) | Docker image from official repo | `timeloop-experiment.yml` | Only Conv1 layer evaluated; official Docker image may fail on GH Actions |
| **NeuSight** | Hybrid ML (GPU) | Python clone + precomputed | `neusight-experiment.yml` | Uses precomputed predictions only; no live inference without GPU |

### Decision: Tools NOT included

| Tool | Reason |
|------|--------|
| MAESTRO | No Docker setup; requires custom build; would add infrastructure work beyond available time |
| FlashAttention | Kernel-level optimization, not a performance modeling tool; outside survey scope |
| Commercial tools (TensorRT profiler, etc.) | Proprietary; cannot reproduce in CI |

---

## 3. Workload Matrix

### 3.1 Primary workloads

| Workload | Model | Task | Hardware Target | Tools Applicable |
|----------|-------|------|-----------------|------------------|
| W1: ResNet-50 Conv1 | ResNet-50 | Single-layer inference | A100 (simulated) | Timeloop, nn-Meter, NeuSight, Analytical |
| W2: ResNet-50 Training 8-GPU | ResNet-50 | Data-parallel training | HGX-H100 × 8 | ASTRA-sim |
| W3: ResNet-50 Training Scaling | ResNet-50 | Data-parallel training | HGX-H100 × {2,4,8} | ASTRA-sim |
| W4: BERT-base Inference | BERT-base | Inference | A100 (simulated) | NeuSight, nn-Meter, Analytical |
| W5: Llama-2-7B Serving | Llama-2-7B | LLM serving | A100 (simulated) | VIDUR |
| W6: Collectives Microbench | all-reduce/all-gather/reduce-scatter/all-to-all | Communication | HGX-H100 × 8 | ASTRA-sim |

### 3.2 Secondary workloads (if time permits)

| Workload | Model | Task | Tools |
|----------|-------|------|-------|
| W7: GPT-2 Inference | GPT-2 | Inference | NeuSight, Analytical |
| W8: MobileNet-V2 Edge | MobileNet-V2 | Edge inference | nn-Meter |
| W9: VGG-16 Edge | VGG-16 | Edge inference | nn-Meter |
| W10: ResNet-50 Training 16-GPU | ResNet-50 | Scaling study | ASTRA-sim |

### 3.3 Tool × Workload Coverage Matrix

|  | W1 | W2 | W3 | W4 | W5 | W6 |
|--|----|----|----|----|----|----|
| ASTRA-sim | — | **P1** | **P1** | — | — | **P1** |
| VIDUR | — | — | — | — | **P1** | — |
| Timeloop | **P1** | — | — | — | — | — |
| nn-Meter | **P2** | — | — | **P2** | — | — |
| NeuSight | **P1** | — | — | **P1** | — | — |

**P1** = Priority 1 (must complete), **P2** = Priority 2 (attempt, report failures)

---

## 4. Metrics per MTAP Dimension

### D1: Prediction Fidelity

| Metric | Definition | How Measured |
|--------|-----------|--------------|
| Self-reported MAPE | Tool author's claimed accuracy | Extract from published papers |
| Reproducible output | Does tool produce numerical output on our workloads? | Binary pass/fail from CI |
| Internal consistency | Do predictions scale as expected? | Scaling factor analysis (e.g., 2→8 GPU comm scaling) |
| Cross-tool agreement | Do overlapping tools agree? | Compare NeuSight vs Timeloop on ResNet-50 Conv1 |

**Note:** Independent hardware verification requires target GPUs we don't have. We report self-reported claims as unverified and focus on reproducibility + internal consistency.

### D2: Compositional Fidelity

| Metric | Definition | How Measured |
|--------|-----------|--------------|
| Layer → Model error amplification | How kernel-level error compounds to model-level | Compare per-layer predictions (Timeloop/NeuSight) vs end-to-end (Analytical) |
| Compute → System error amplification | How compute prediction error compounds with communication | ASTRA-sim: compute cycles vs total cycles at different scales |

### D3: Generalization Robustness

| Metric | Definition | How Measured |
|--------|-----------|--------------|
| Cross-model coverage | Does tool handle diverse architectures? | Test ResNet-50 + BERT + Llama-2 on each tool |
| Failure rate | Fraction of workloads where tool fails to produce output | Count FAIL entries in coverage matrix |
| Configuration sensitivity | Does output change with minor config changes? | Run ASTRA-sim with Ring vs Tree topology |

### D4: Deployment Viability

| Metric | Definition | How Measured |
|--------|-----------|--------------|
| Setup time | Time from `git clone` to first result | Timed in CI workflow logs |
| Docker vs pip success rate | Does Docker-based setup succeed more reliably? | Binary from CI across tools |
| Determinism | Same inputs → same outputs? | Run twice, diff results |
| CI compatibility | Runs on GitHub Actions runners? | Binary from workflow status |

### D5: Extensibility

| Metric | Definition | How Measured |
|--------|-----------|--------------|
| New model effort | Lines of config/code to add a new workload | Count from our scripts |
| New hardware effort | Steps to add new hardware target | Documented from setup experience |
| API accessibility | Programmatic vs config-file interface | Qualitative assessment |

---

## 5. Execution Environment

### Primary: GitHub Actions Runners

- **OS:** Ubuntu 22.04 (latest)
- **CPU:** 2-core x86_64
- **RAM:** 7 GB
- **Storage:** 14 GB SSD
- **Docker:** Available
- **GPU:** None
- **Timeout:** 45 min max per workflow

### Secondary: Local M2 Ultra (if needed for debugging)

- **OS:** macOS
- **CPU:** Apple M2 Ultra (24-core)
- **RAM:** 192 GB
- **Docker:** Available via OrbStack/Colima
- **GPU:** None (Apple Silicon, not CUDA)

### Constraints

1. **No CUDA GPUs available** — all evaluations run on CPU or in simulated mode
2. Docker builds must complete within 45 minutes on GH Actions
3. Results must be deterministic across runs
4. All results committed as JSON artifacts to `data/evaluation/`

---

## 6. Experiment Execution Plan

### Phase 1: Expand Existing Experiments (P1, ~3 cycles)

**Goal:** Fill gaps in ASTRA-sim and VIDUR coverage.

#### Experiment 1a: ASTRA-sim Full Collective Suite
- **What:** Run all 4 collectives (all-reduce, all-gather, reduce-scatter, all-to-all) at 2, 4, 8 NPU scales
- **Why:** Currently only all-reduce at 8 NPUs runs in CI; paper has 4 values without CI backing
- **How:** Update `astra-sim-experiment.yml` to call `run_benchmarks.sh` with all collectives/scales
- **Output:** `data/evaluation/astra-sim-results/full_collective_results.json`
- **CI branch trigger:** `experiment-runner/astra-sim-full-*`

#### Experiment 1b: ASTRA-sim Topology Comparison
- **What:** Run ResNet-50 8-GPU with Ring vs Tree all-reduce topology
- **Why:** Measures D3 (generalization robustness) — configuration sensitivity
- **How:** Create alternate network config with tree topology; run both in CI
- **Output:** `data/evaluation/astra-sim-results/topology_comparison.json`

#### Experiment 1c: VIDUR Multi-Scheduler Extended
- **What:** Run all 3 schedulers (vLLM, Sarathi, Orca) with 500 requests at QPS {1.0, 2.0, 4.0}
- **Why:** Current run is 200 requests at 2.0 QPS only. Need QPS sweep for D3 (generalization)
- **How:** Update `vidur-experiment.yml` to loop over QPS values
- **Output:** `data/evaluation/vidur-results/qps_sweep_results.json`

### Phase 2: Activate Remaining Tools (P2, ~3 cycles)

#### Experiment 2a: nn-Meter Docker Evaluation
- **What:** Build nn-Meter Docker image, run predictions on ResNet-50, VGG-16, MobileNet-V2
- **Why:** nn-Meter is the only ML-augmented tool in our set; essential for cross-category comparison
- **How:** Create `nn-meter-experiment.yml` workflow; debug pickle/sklearn compatibility
- **Expected issues:** sklearn predictor pickle files may fail to deserialize; document failure as D4 finding
- **Output:** `data/evaluation/nn-meter-results/predictions.json` (or failure report)

#### Experiment 2b: Timeloop Extended
- **What:** Run Timeloop on ResNet-50 Conv layers (not just Conv1) + BERT attention layer
- **Why:** Current evaluation is single layer only; need multi-layer for D2 (compositional fidelity)
- **How:** Extend `run_resnet50_conv.py` to iterate over multiple layers; create `run_bert_attention.py`
- **Output:** `data/evaluation/timeloop-results/multi_layer_results.json`

#### Experiment 2c: NeuSight Cross-Model
- **What:** Collect NeuSight precomputed predictions for ResNet-50, BERT-base, GPT-2 on A100/H100
- **Why:** Cross-model coverage for D3 (generalization)
- **How:** Update `run_neusight_prediction.py` to extract per-model predictions
- **Output:** `data/evaluation/neusight-results/cross_model_predictions.json`

### Phase 3: Cross-Tool Analysis (P1, ~2 cycles)

#### Experiment 3a: Unified Results Aggregation
- **What:** Parse all tool outputs into a single structured JSON for paper table generation
- **How:** Write `scripts/benchmarks/aggregate_results.py` that reads all `*-results/` dirs
- **Output:** `data/evaluation/mtap-aggregate-results.json`

#### Experiment 3b: Compositional Fidelity Analysis
- **What:** Compare layer-level predictions (Timeloop/NeuSight) vs model-level (Analytical) vs system-level (ASTRA-sim) to measure error amplification
- **How:** Write `scripts/benchmarks/compositional_analysis.py`
- **Output:** `data/evaluation/compositional-fidelity-report.md`

#### Experiment 3c: Deployment Viability Summary
- **What:** Extract setup times from CI logs, Docker build times, success/fail matrix
- **How:** Parse GitHub Actions workflow timing from API
- **Output:** `data/evaluation/deployment-viability-report.md`

---

## 7. Success Criteria

| Criterion | Target |
|-----------|--------|
| Tools with CI-backed results | 5/5 (ASTRA-sim, VIDUR, Timeloop, nn-Meter, NeuSight) |
| MTAP dimensions with quantitative data | 5/5 (D1-D5) |
| Primary workloads executed | 6/6 (W1-W6) |
| Paper-ready tables/figures | At least 2 new figures + 1 updated table |
| All results in version control | JSON in `data/evaluation/` + CI artifacts |

---

## 8. Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| nn-Meter pickle deserialization fails | Lose ML-augmented category evaluation | Document failure as D4 finding; this itself is a MTAP result (deployment viability = Low) |
| Timeloop Docker image fails on GH Actions | Lose analytical tool evaluation | Use analytical-only fallback mode already in script |
| ASTRA-sim build exceeds 45-min timeout | Can't expand experiments | Pre-build Docker image and push to GHCR |
| VIDUR QPS=4.0 causes OOM on GH Actions (7 GB) | Incomplete QPS sweep | Reduce request count to 100 at high QPS |
| NeuSight precomputed predictions incomplete | Sparse coverage matrix | Report as-is; partial coverage is an honest D3 finding |

---

## 9. Timeline

| Phase | Cycles | Deliverable |
|-------|--------|-------------|
| Phase 1: Expand existing | 3 | ASTRA-sim full collectives, topology comparison; VIDUR QPS sweep |
| Phase 2: Activate remaining | 3 | nn-Meter attempt, Timeloop extended, NeuSight cross-model |
| Phase 3: Cross-tool analysis | 2 | Aggregate results, compositional analysis, deployment report |
| **Total** | **8** | Complete MTAP evaluation data for paper |

---

## 10. Output Artifacts

All results will be committed to `data/evaluation/` with the following structure:

```
data/evaluation/
  astra-sim-results/
    full_collective_results.json      # NEW: All collectives × all scales
    topology_comparison.json          # NEW: Ring vs Tree
    astra_sim_results.json            # Existing
    accuracy_analysis.json            # Existing
  vidur-results/
    qps_sweep_results.json            # NEW: Multi-QPS evaluation
    vidur_results.json                # Existing
  timeloop-results/
    multi_layer_results.json          # NEW: Multiple Conv layers
    resnet50_conv1_results.json       # Existing
  nn-meter-results/
    predictions.json                  # NEW: Full prediction run (or failure report)
  neusight-results/
    cross_model_predictions.json      # NEW: Per-model breakdown
    neusight_results.json             # Existing
  mtap-aggregate-results.json         # NEW: Unified cross-tool data
  compositional-fidelity-report.md    # NEW: Error amplification analysis
  deployment-viability-report.md      # NEW: Setup time + success matrix
```
