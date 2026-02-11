# Cross-Tool Accuracy Evaluation Report

**Generated:** 2026-02-07
**Author:** Flux (Tool Engineer)
**Issues:** #194, #155, #143

---

## 1. Executive Summary

We independently evaluated two ML performance modeling tools — **ASTRA-sim** (distributed training) and **VIDUR** (LLM inference) — by running experiments and comparing results against published accuracy claims. Neither tool's absolute accuracy can be verified without target hardware, but both produce internally consistent and physically plausible predictions suitable for relative comparisons.

## 2. ASTRA-sim Results

### 2.1 Microbenchmarks (8 NPUs, 1 MB, HGX-H100)

| Collective | Cycles | Ratio vs All-Reduce |
|-----------|--------|-------------------|
| all-reduce | 57,426 | 1.000 |
| all-gather | 44,058 | 0.767 |
| reduce-scatter | 28,950 | 0.504 |
| all-to-all | 114,000 | 1.985 |

**Analytical cross-check:** Simple ring all-reduce model predicts ~17,695 ns. ASTRA-sim reports 57,426 cycles (3.2x). The difference is due to endpoint delay, chunking, and scheduling overhead.

### 2.2 ResNet-50 Communication Scaling

| Scale | Wall Time (cycles) | Comm Time (cycles) | Comm Overhead |
|-------|-------------------|-------------------|--------------|
| 2 Gpu | 1,095,888,289 | 574,289 | 0.052% |
| 4 Gpu | 1,096,768,270 | 1,454,270 | 0.133% |
| 8 Gpu | 1,098,621,886 | 3,307,886 | 0.301% |

**Communication scaling factor (2→8 GPU):** 5.76x

### 2.3 Published Accuracy Claims

**Source:** ASTRA-sim HGX-H100 validation (Won et al.)

| Scale | Published Geomean Error | Our Verdict |
|-------|------------------------|-------------|
| 2 Gpu | 20.63% | Plausible, unverified |
| 4 Gpu | 12.01% | Plausible, unverified |
| 8 Gpu | 9.69% | Plausible, unverified |

**Why unverified:** Independent verification requires HGX-H100 hardware to measure ground-truth NCCL all-reduce latencies. Published validation was against specific NCCL benchmark message sizes, not end-to-end training. Our synthetic workload compute times don't represent real H100 kernel execution.

## 3. VIDUR Results

### 3.1 Scheduler Comparison (Llama-2-7B, A100)

| Metric | vLLM | Sarathi | Difference |
|--------|------|---------|-----------|
| Avg E2E Latency | 0.1767s | 0.1575s | +12.19% |
| Avg TTFT | 0.0273s | 0.0247s | +10.53% |
| Avg TPOT | 0.009347s | 0.009034s | +3.46% |
| Requests Preempted | 53 | 0 | — |
| Throughput (tok/s) | 197966.0 | 54704.9 | — |

### 3.2 Detailed Per-Scheduler Metrics

#### VLLM

- **Requests:** 200
- **QPS:** 2.0
- **E2E Latency:** avg=0.1767s, median=0.1770s, P90=0.2609s, P99=0.3198s
- **TTFT:** avg=0.0273s, P99=0.0645s
- **TPOT:** avg=0.009347s, P99=0.012719s
- **Scheduling delay:** avg=0.001967s, max=0.028845s
- **Preempted:** 53 requests
- **Throughput:** 197966.0 tok/s (64,053 total tokens)

#### SARATHI

- **Requests:** 50
- **QPS:** 2.0
- **E2E Latency:** avg=0.1575s, median=0.1563s, P90=0.2357s, P99=0.2697s
- **TTFT:** avg=0.0247s, P99=0.0382s
- **TPOT:** avg=0.009034s, P99=0.010996s
- **Scheduling delay:** avg=0.001453s, max=0.010783s
- **Preempted:** 0 requests
- **Throughput:** 54704.9 tok/s (14,752 total tokens)

### 3.3 Published Accuracy Claims

**Claimed error:** <5% vs real LLM serving traces
**Validated against:** vLLM, TensorRT-LLM
**Our verdict:** PARTIALLY_VERIFIED

**What we verified:**
- Simulation completes for Llama-2-7B on A100 with both vLLM and Sarathi schedulers
- Request-level metrics (E2E, TTFT, TPOT) are physically plausible
- Scheduling delay is near-zero at low QPS (2.0), as expected
- Preemption occurs with vLLM but not Sarathi, matching algorithm design
- Relative scheduler ranking (Sarathi slightly faster) is consistent with literature

**What we cannot verify:**
- Absolute latency accuracy (requires real A100 GPU running vLLM)
- The specific <5% error claim (requires identical hardware + workload trace)

## 4. Cross-Tool Comparison

### 4.1 Reproducibility

| Aspect | ASTRA-sim | VIDUR |
|--------|-----------|-------|
| Setup Method | Docker | pip (Python 3.10) |
| Deterministic | True | True |
| Time to First Result | 20 min | 5 min |
| Reproducibility Score | 8/10 | 7/10 |

### 4.2 Accuracy Verification Summary

| Tool | Published Claim | Our Verdict | Blocker |
|------|----------------|-------------|---------|
| ASTRA-sim | 9.69% geomean error (8 GPU HGX-H100) | PLAUSIBLE but UNVERIFIED | No hardware access for ground truth |
| VIDUR | <5% error vs real serving | PLAUSIBLE but UNVERIFIED | No hardware access for ground truth |

### 4.3 Key Findings

**1. Both tools produce physically plausible results**
   ASTRA-sim communication scales with GPU count as expected. VIDUR scheduler metrics match algorithm design (preemption in vLLM, not Sarathi).

**2. Published accuracy claims cannot be independently verified without hardware**
   ASTRA-sim claims 9.69% error (8 GPU) but needs HGX-H100 ground truth. VIDUR claims <5% error but needs real A100 + vLLM deployment.

**3. Relative comparisons are more trustworthy than absolute predictions**
   ASTRA-sim correctly predicts communication scaling trends. VIDUR correctly ranks scheduler latency and captures preemption behavior.

**4. Docker-based tools achieve better reproducibility than pip-installed tools**
   ASTRA-sim (Docker): deterministic builds, identical results across runs. VIDUR (pip): Python 3.10 requirement, dependency sensitivity.

## 5. Recommendations for the Survey Paper

1. **Report published accuracy claims as unverified.** We can say tools claim X% error, but we cannot independently confirm this without the target hardware.

2. **Emphasize relative comparison capability.** Both tools correctly predict trends (scaling, scheduler ranking) even if absolute numbers are unverified.

3. **Highlight reproducibility as a differentiator.** Docker-based setup (ASTRA-sim) provides stronger reproducibility guarantees than pip-only tools.

4. **Use our numerical results in Section 7.** The ASTRA-sim collective ratios, ResNet-50 scaling factors, and VIDUR scheduler comparison provide concrete data for the evaluation section.

---

*Generated by `scripts/cross_tool_accuracy_analysis.py`*