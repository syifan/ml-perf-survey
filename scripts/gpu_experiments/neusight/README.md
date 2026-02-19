# NeuSight GPU Experiments

## What This Does

Runs NeuSight kernel-level latency predictions on real H100/A100 hardware, targeting the benchmark scenarios from our paper (Section 4.1).

NeuSight predicts per-GPU kernel execution time using tile-based decomposition + MLP predictors. It does **not** model communication overhead (AllReduce, pipeline bubbles), so distributed scenarios only get the compute component.

## Paper Scenarios Covered

| Scenario | Description | NeuSight Coverage |
|----------|-------------|-------------------|
| I1.1 | Llama-2-7B single-request inference | Supported (kernel latency) |
| I1.2 | Llama-2-13B single-request inference | Supported (kernel latency) |
| I1.3 | Llama-2-70B single-request inference | Supported (kernel latency) |
| T1.1 | GPT-2 DP on 8xA100 | Partial (per-GPU kernel only) |
| T2.1 | Llama-2-13B TP on 4xA100 | Partial (per-GPU kernel only) |

Additional models tested: GPT-3-2.7B, BERT-Large, OPT-13B, SwitchXL4 (MoE).

## Hardware Requirements

- **GPU**: NVIDIA H100-SXM or A100-SXM4 (80GB preferred)
- **CUDA**: 12.x
- **RAM**: 32GB+
- **Disk**: 10GB free
- **Software**: conda, Python 3.10+

## How to Run

```bash
# 1. Install dependencies
./install.sh

# 2. Run benchmarks
./run_benchmarks.sh
```

## Expected Runtime

- Artifact validation: ~5 minutes
- Live GPU predictions: ~30-60 minutes (depends on GPU)
- Total: ~1 hour

## Expected Outputs

Results are saved to `results/<timestamp>/`:

- `artifact_validation/` — Re-analysis of NeuSight's pre-computed prediction/label pairs
- `live_*.json` — Per-model predictions on your actual GPU
- `parallel_*.json` — DP4/TP4/PP4 comparison (GPT-2-Large on A100)
- `fusion_*.json` — Fused vs unfused operator comparison

### Key Metrics to Verify (from paper Table 5)

| Device | Paper MAPE (inf) | Paper MAPE (train) |
|--------|------------------|--------------------|
| H100 | 9.43% | 15.61% |
| A100-SXM | 8.12% | — |
| V100 | 5.87% | 8.91% |

Parallelism comparison (A100, GPT-2-Large, batch=4):
- DP4: 12.87% APE
- TP4: 8.40% APE
- PP4: 10.26% APE

## Sending Results Back

Compress and send the entire results directory:
```bash
tar czf neusight_results.tar.gz results/
```
