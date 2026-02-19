# ASTRA-sim Distributed Training Experiments

## What This Does

Runs ASTRA-sim communication modeling for distributed LLM training scenarios from our paper (Section 4.2). ASTRA-sim simulates collective communication patterns (AllReduce, AllGather, ReduceScatter, All-to-All) using analytical network models on HGX-H100 topology.

ASTRA-sim models **communication overhead only**. It requires externally profiled per-layer compute times for end-to-end training time prediction.

## Paper Scenarios Covered

| Scenario | Description | ASTRA-sim Coverage |
|----------|-------------|-------------------|
| T1.1 | GPT-2 DP on 8xA100 | Supported (AllReduce communication) |
| T1.2 | Llama-2-7B DP on 8xH100 | Supported |
| T1.3 | Llama-2-13B DP on 8xA100 | Supported |
| T2.1 | Llama-2-13B TP on 4xA100 | Supported (intra-node AllReduce) |
| T2.2 | Llama-2-70B TP on 8xH100 | Supported |
| T3.1 | GPT-3 PP on 8xH100 | Supported (pipeline communication) |
| T3.2 | GPT-3 175B PP8+TP8 on 64xH100 | Supported |
| T4.3 | Sequence parallelism | Partial (communication only) |
| T4.4 | MoE expert parallelism | Partial (All-to-All only) |

Total: 7 supported + 2 partial = 9/28 scenarios (32% coverage, broadest training coverage).

## Hardware Requirements

- **GPU**: Optional (ASTRA-sim uses analytical network models)
- **Docker**: Recommended
- **RAM**: 16GB+
- **Disk**: 10GB free
- Running on an actual HGX-H100 node validates topology modeling accuracy

## How to Run

```bash
# 1. Install (Docker recommended)
./install.sh

# 2. Run benchmarks
./run_benchmarks.sh

# Or run directly in Docker:
docker run --rm -v $(pwd)/results:/results astrasim-benchmarks bash /scripts/run_benchmarks.sh
```

## Expected Runtime

- Collective microbenchmarks: ~5 minutes
- ResNet-50 scaling: ~10 minutes
- Total: ~15-20 minutes

## Expected Outputs

Results saved to `results/<timestamp>/`:

- `<collective>_<npus>npus_1MB.log` — Collective microbenchmark results
- `resnet50_dp<N>.log` — ResNet-50 data-parallel scaling
- `llm_communication_analysis.txt` — Communication pattern analysis

### Key Metrics (from paper Table 3)

| Collective | 8 NPUs, 1MB | Expected |
|-----------|-------------|----------|
| AllReduce | Ring | ~11.0 μs |
| AllGather | Ring | ~10.7 μs |
| ReduceScatter | Ring | ~10.7 μs |
| All-to-All | — | ~21.8 μs (1.985x AR) |

## Sending Results Back

```bash
tar czf astrasim_results.tar.gz results/
```
