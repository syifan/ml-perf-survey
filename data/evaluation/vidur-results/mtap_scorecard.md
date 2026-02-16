# MTAP Scorecard: VIDUR

**Tool:** VIDUR (LLM Inference Simulator, Microsoft Research)
**Evaluation Date:** 2026-02-16
**Platform:** GitHub Actions (Ubuntu 22.04, 2-core x86_64, 7 GB RAM, no GPU)
**Evaluator:** Experiment-Runner (automated)

---

## Composite MTAP Score

**S(VIDUR) = 2.1 / 3.0 (70.0%)**

```
S(t) = 0.4*M + 0.2*M + 0.2*M + 0.1*M + 0.1*H
     = 0.4*2 + 0.2*2 + 0.2*2 + 0.1*2 + 0.1*3
     = 0.8 + 0.4 + 0.4 + 0.2 + 0.3
     = 2.1
```

| Dimension | Weight | Score | Label | Key Evidence |
|-----------|--------|-------|-------|--------------|
| D1: Prediction Fidelity | 40% | 2 | **M** | <5% self-reported; unverifiable without A100 |
| D2: Compositional Fidelity | 20% | 2 | **M** | ML predictor + DES; pre-profiled GPU dependency |
| D3: Generalization Robustness | 20% | 2 | **M** | 7 models; Python 3.10 fragility |
| D4: Deployment Viability | 10% | 2 | **M** | 5 min pip install; no Docker; version-sensitive |
| D5: Extensibility | 10% | 3 | **H** | 5 schedulers; config optimizer; profiling pipeline |

---

## D1: Prediction Fidelity (Score: M)

### Self-Reported Accuracy (Published)

| Metric | Claim | Source |
|--------|-------|--------|
| Error vs real traces | <5% | Agrawal et al., MLSys 2024 |
| Validated against | vLLM, TensorRT-LLM | Microsoft Research |

*Status: PLAUSIBLE but UNVERIFIED --- no A100 GPU available for ground-truth measurements.*

### Our Independent Measurements

**vLLM Scheduler (Llama-2-7B, A100, 200 requests, QPS=2.0):**

| Metric | Value |
|--------|-------|
| Avg E2E latency | 0.1767 s |
| Median E2E | 0.177 s |
| P90 E2E | 0.2609 s |
| P99 E2E | 0.3198 s |
| Avg TTFT | 0.0273 s |
| Avg TPOT | 0.009347 s |
| Requests preempted | 53 / 200 (26.5%) |

**Sarathi Scheduler (Llama-2-7B, A100, 50 requests, QPS=2.0):**

| Metric | Value |
|--------|-------|
| Avg E2E latency | 0.1575 s |
| Median E2E | 0.1563 s |
| P90 E2E | 0.2357 s |
| P99 E2E | 0.2697 s |
| Avg TTFT | 0.0247 s |
| Avg TPOT | 0.009034 s |
| Requests preempted | 0 / 50 (0%) |

**Scheduler Comparison:**

| Metric | vLLM | Sarathi | Difference |
|--------|------|---------|------------|
| Avg E2E | 0.1767 s | 0.1575 s | vLLM 12.19% slower |
| Avg TTFT | 0.0273 s | 0.0247 s | vLLM 10.53% slower |
| Avg TPOT | 0.009347 s | 0.009034 s | vLLM 3.46% slower |
| Preemption | 53 requests | 0 requests | Design difference |

### Scoring Rationale

Score = **M (Medium)** because:
- Published <5% error claim is plausible given Microsoft's production validation
- Scheduler ranking (Sarathi < vLLM latency) is consistent with published literature
- Preemption behavior matches algorithmic design exactly (PagedAttention vs chunked prefill)
- Cannot independently verify absolute latency accuracy without A100 hardware

---

## D2: Compositional Fidelity (Score: M)

### Composition Approach

VIDUR composes ML-predicted per-operator execution times with discrete-event scheduling simulation:

```
request_latency = sum(iteration_times) + scheduling_delay + preemption_time
iteration_time  = ML_predictor(batch_size, seq_len, model, device)
scheduling      = DES(arrival_pattern, scheduler_policy, memory_constraints)
```

### Pre-Profiled Data Dependency

| Component | Method | Hardware Required |
|-----------|--------|-------------------|
| Operator execution | GPU profiling | Yes (target GPU) |
| Network latency | Network profiling | Yes (target network) |
| Scheduling logic | Analytical DES | No |

### Scoring Rationale

Score = **M (Medium)** because:
- Successfully composes execution prediction + scheduling simulation into end-to-end metrics
- ML-based predictor trained on real GPU profiles (A100, H100, A40)
- Hidden dependency: new GPUs/models require physical hardware for profiling
- Composition gap cannot be measured (pre-profiled data bypasses kernel prediction)

---

## D3: Generalization Robustness (Score: M)

### Model Coverage

| Model | A100 | H100 | A40 | Tested |
|-------|------|------|-----|--------|
| Meta-Llama-3-8B | Yes | No | No | No |
| Meta-Llama-3-70B | Yes | No | No | No |
| Llama-2-7b-hf | Yes | Yes | Yes | **Yes** |
| Llama-2-70b-hf | Yes | Yes | Yes | No |
| CodeLlama-34b | Yes | Yes | Yes | No |
| internlm-20b | Yes | Yes | Yes | No |
| Qwen-72B | Yes | Yes | Yes | No |

### Temporal Stability

| Aspect | Status |
|--------|--------|
| Python 3.10 required | Yes (3.11+ breaks argparse) |
| Docker support | No |
| pip reproducible | Version-sensitive |
| scikit-learn dependency | Yes |
| wandb dependency | Yes (can disable) |

### Scoring Rationale

Score = **M (Medium)** because:
- 7 pre-profiled model architectures across 3 GPU types
- Only 1 model tested in our evaluation (Llama-2-7B)
- Python 3.10 hard requirement creates temporal fragility
- No Docker image for reproducible deployment
- Adding new models requires GPU hardware access

---

## D4: Deployment Viability (Score: M)

| Metric | Value |
|--------|-------|
| Time-to-first-prediction | ~5 min (pip install + run) |
| Docker support | **No** |
| Deterministic outputs | Yes (with fixed seed) |
| CI compatible | Partial (Python 3.10 setup required) |
| Failure modes | Python 3.11+ incompatible; wandb import |
| Platform support | Linux/macOS with Python 3.10 |

### Deployment Steps

1. Create Python 3.10 venv (~1 min)
2. `pip install -r requirements.txt` (~3 min)
3. `WANDB_MODE=disabled python -m vidur.main` (~1 min)

### Scoring Rationale

Score = **M (Medium)** because:
- Fast setup (5 min) but fragile (Python 3.10 only)
- No Docker image — pip-only installation
- Deterministic with fixed seed, but CI requires specific Python version management
- wandb dependency adds unnecessary friction (requires disabling)
- Excellent documentation partially compensates for deployment issues

---

## D5: Extensibility (Score: H)

| Extension Type | Method | Effort |
|---------------|--------|--------|
| New model | GPU profiling + config | Hours (GPU required) |
| New GPU | Hardware profiling pipeline | Hours (hardware required) |
| New scheduler | Subclass `replica_scheduler` | ~100-300 LOC |
| New workload | CSV trace file or synthetic config | Minutes |

### Built-in Schedulers

| Scheduler | Preemption | Chunked Prefill | Description |
|-----------|------------|-----------------|-------------|
| vLLM | Yes | No | PagedAttention |
| Orca | Yes | No | Iteration-level scheduling |
| Sarathi | No | Yes | Chunked prefill |
| LightLLM | No | No | Lightweight serving |
| FasterTransformer | No | No | NVIDIA implementation |

### Scoring Rationale

Score = **H (High)** because:
- 5 production scheduling algorithms implemented
- Config optimizer for automated hyperparameter search
- Rich output metrics (20+ request-level and system-level)
- Chrome trace visualization for debugging
- Documented profiling pipeline for new models/GPUs
- Microsoft-backed with Azure production use

---

## Experimental Evidence Summary

| Category | Count |
|----------|-------|
| Total experiments run | 2 |
| Successful | 2 |
| Failed | 0 |
| Schedulers tested | 2 (vLLM, Sarathi) |
| Models tested | 1 (Llama-2-7B) |
| Total requests simulated | 250 |
| Metrics collected | 6 (E2E, TTFT, TPOT, preemption, sched delay, throughput) |

---

## Limitations

1. **D1 unverified:** Self-reported <5% accuracy cannot be independently confirmed without A100 hardware
2. **Single model:** Only Llama-2-7B tested; no cross-architecture validation
3. **Two schedulers:** Only vLLM and Sarathi tested; Orca, LightLLM, FasterTransformer untested
4. **No Docker:** pip-only installation with Python 3.10 creates deployment fragility
5. **Synthetic workload:** Not tested with real Azure traces
6. **Single GPU config:** No multi-replica or pipeline-parallel testing

---

*Generated from `data/evaluation/cross-tool-accuracy-results.json` and `data/evaluation/vidur-evaluation.md`*
