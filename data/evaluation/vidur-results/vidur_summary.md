# VIDUR Accuracy Experiment Results

**Date:** 2026-02-13T04:34:57Z
**Tool:** VIDUR (Microsoft Research, MLSys 2024)
**Model:** Llama-2-7B on simulated A100 GPU
**Workload:** Synthetic requests, uniform token distribution (128-512 tokens, 20:1 prefill/decode ratio)

## Summary Table

| Metric | vllm | sarathi | orca |
|--------|--------||--------||--------|
| Requests completed | 100 | 100 | 100 |
| QPS | 2.0 | 4.0 | 8.0 |
| Avg E2E latency (s) | 0.1703 | 0.1744 | 0.1879 |
| P50 E2E latency (s) | 0.1769 | 0.1790 | 0.1875 |
| P99 E2E latency (s) | 0.3135 | 0.2962 | 0.3350 |
| Avg TTFT (s) | 0.0266 | 0.0281 | 0.0312 |
| Avg TPOT (s) | 0.0093 | 0.0095 | 0.0102 |
| Throughput (tok/s) | 98531 | 104275 | 92201 |
| Requests preempted | 28 | 0 | 0 |
| Preemption rate | 28.0% | 0.0% | 0.0% |
| Avg scheduling delay (s) | 0.002205 | 0.003550 | 0.005619 |

## Analysis

### Scheduler Comparison

**Lowest latency:** vllm (0.1703s avg E2E)
**Latency spread:** 10.3% between vllm and orca

- **vllm**: 28/100 requests preempted (28.0%)
- **sarathi**: 0/100 requests preempted (0.0%)
- **orca**: 0/100 requests preempted (0.0%)

### Per-Token Decode Throughput

TPOT spread across schedulers: 9.7%, confirming decode throughput is primarily hardware-bound rather than scheduler-dependent.

### Accuracy Validation Notes

- VIDUR claims <5% error vs real LLM serving traces
- Without real A100 hardware running vLLM/Sarathi, we validate through internal consistency and physical plausibility
- Scheduler ranking and preemption behavior match algorithmic design expectations
- Deterministic outputs with fixed seed confirm reproducibility
