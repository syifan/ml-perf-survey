# VIDUR LLM Inference Serving Experiments

## What This Does

Runs VIDUR LLM inference serving simulations targeting paper scenarios (Section 4.3). VIDUR models prefill/decode phases, scheduling policies (vLLM, Sarathi-Serve, Orca), KV cache management, and preemption behavior.

VIDUR is a **simulator** — it does not require actual GPU inference. It uses pre-profiled execution traces to predict serving metrics (TTFT, TPOT, throughput).

## Paper Scenarios Covered

| Scenario | Description | VIDUR Coverage |
|----------|-------------|----------------|
| I1.1 | Llama-2-7B single-request inference | Supported |
| I1.2 | Llama-2-13B single-request inference | Supported |
| I2.1 | Llama-2-7B batched serving (vLLM) | Supported |
| I2.2 | Llama-2-13B batched serving (Sarathi) | Supported |
| I2.3 | Llama-2-7B batched serving (Orca) | Supported |
| I3.1 | KV cache with PagedAttention | Supported |
| I3.2 | KV cache optimization | Partial |
| I3.3 | Long-context KV cache | Partial |
| I5.x | Speculative decoding, prefix caching, etc. | Unsupported |

Total: 6 supported + 2 partial = 8/28 scenarios (29% coverage).

## Hardware Requirements

- **GPU**: Not strictly required (VIDUR is a simulator), but useful for validation
- **Docker**: Recommended
- **RAM**: 16GB+
- **Disk**: 5GB free

## How to Run

```bash
# 1. Install (Docker recommended)
./install.sh

# 2. Run all benchmarks
./run_benchmarks.sh
```

## Experiments Included

1. **Paper reproduction** (Table 4): Llama-2-7B on A100 with vLLM, Sarathi, Orca at QPS=2.0
2. **Higher QPS stress tests**: QPS=4.0 and QPS=8.0 (paper limitation noted at line 224)
3. **Llama-2-13B experiments**: Larger model serving with Sarathi and vLLM
4. **H100 experiments**: If VIDUR supports H100 device config

## Expected Runtime

- Per experiment: ~2-5 minutes
- Total (all experiments): ~30-45 minutes

## Expected Outputs

Each experiment produces:
- `request_metrics.csv` — Per-request TTFT, TPOT, total latency
- `batch_metrics.csv` — Per-batch size and processing time
- `run.log` — Full execution log

### Key Metrics (from paper Table 4)

| Experiment | Metric | Expected |
|-----------|--------|----------|
| Llama-2-7B vLLM QPS=2.0 | Mean TTFT | ~150-300ms |
| Llama-2-7B Sarathi QPS=2.0 | Preemptions | 0 |
| Sarathi vs vLLM | P99 latency | Sarathi lower |

## Sending Results Back

```bash
tar czf vidur_results.tar.gz results/
```
