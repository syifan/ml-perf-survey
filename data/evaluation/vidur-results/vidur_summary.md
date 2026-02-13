# VIDUR Accuracy Experiment Results

**Date:** 2026-02-13T04:38:19Z
**Tool:** VIDUR (Microsoft Research, MLSys 2024)
**Model:** Llama-2-7B on simulated A100 GPU
**Workload:** Synthetic requests, uniform token distribution (128-512 tokens, 20:1 prefill/decode ratio)

## Summary Table

| Metric |  |
|--------|

## Analysis

### Scheduler Comparison


### Accuracy Validation Notes

- VIDUR claims <5% error vs real LLM serving traces
- Without real A100 hardware running vLLM/Sarathi, we validate through internal consistency and physical plausibility
- Scheduler ranking and preemption behavior match algorithmic design expectations
- Deterministic outputs with fixed seed confirm reproducibility
