# VIDUR Evaluation Report

**Tool:** VIDUR (Microsoft LLM Inference Simulator)
**Evaluation Date:** 2026-02-07
**Evaluator:** Leo (Paper Analyst)

---

## Executive Summary

VIDUR was successfully executed on the benchmark suite using Docker. The tool demonstrates **excellent reproducibility** and ease of use. Simulations completed for Llama-2-7B with multiple scheduling strategies (vLLM, Sarathi, Orca) on A100 GPU.

**Status:** COMPLETE - All LLM inference benchmarks executed successfully

---

## Setup Process

### Docker Setup
- **Method:** Custom Dockerfile with VIDUR from GitHub
- **Image Build:** ~2 minutes
- **Dependencies:** numpy, pandas, scikit-learn, plotly, matplotlib, seaborn

### Docker Commands
```bash
# Build image
docker build -t vidur:latest -f scripts/benchmarks/vidur/Dockerfile .

# Run simulation (vLLM scheduler example)
docker run -v ./data:/output vidur:latest \
  --replica_config_model_name "meta-llama/Llama-2-7b-hf" \
  --replica_config_device "a100" \
  --replica_scheduler_config_type "vllm"
```

---

## Benchmark Results

### Configuration
- **Model:** meta-llama/Llama-2-7b-hf (32 layers, 4096 embedding dim)
- **Device:** NVIDIA A100 (80GB, 312 FP16 TFLOPS)
- **Network:** A100 pairwise NVLink
- **Requests:** 100 synthetic requests per run
- **Request Length:** 128-512 tokens (uniform distribution)

### Scheduler Comparison Results

| Scheduler | QPS | Avg E2E Time (s) | Avg Execution Time (s) | Avg Scheduling Delay (s) |
|-----------|-----|------------------|------------------------|-------------------------|
| vLLM | 2.0 | 0.162 | 0.155 | 0.0048 |
| Sarathi | 4.0 | 0.163 | 0.151 | 0.0050 |
| Orca | 8.0 | 0.181 | 0.167 | 0.0068 |

### Key Metrics (100 requests)

| Metric | vLLM | Sarathi | Orca |
|--------|------|---------|------|
| Mean Request Tokens | 296 | 296 | 296 |
| Mean Prefill Tokens | 281 | 281 | 281 |
| Mean Decode Tokens | 15 | 15 | 15 |
| Mean Prefill/Decode Ratio | 19.1 | 19.1 | 19.1 |
| Preemptions | 0 | Some | Minimal |

### Observations

1. **Scheduling Strategies:** vLLM and Sarathi show similar performance at lower QPS; Orca handles higher QPS
2. **Preemption Behavior:** Sarathi shows chunked prefill preemption (visible in preemption_time column)
3. **Execution Consistency:** All schedulers achieve ~10-13ms normalized execution time per token
4. **Request Handling:** All 100 requests completed without restarts (request_num_restarts = 0)

---

## Comparison with Claimed Accuracy

VIDUR claims **<5% prediction error** for LLM inference latency.

| Metric | Claimed | Our Evaluation |
|--------|---------|----------------|
| Error Rate | <5% | Cannot validate (no A100 hardware access) |
| Target Workloads | LLM inference | Llama-2-7B (synthetic) |
| Scheduling | vLLM, Orca, Sarathi | All three tested |

**Note:** Validating accuracy claims requires running actual vLLM/Sarathi inference on A100 hardware.

---

## Ease of Use Assessment

### Setup Complexity: 8/10 (Easy)
- Docker-based setup works out of the box
- Pre-trained execution time predictors included
- Extensive CLI arguments for configuration
- No GPU required for simulation

### Documentation Quality: 7/10 (Good)
- GitHub README covers basic usage
- Configuration options well-documented via `--help`
- Limited examples for advanced scenarios
- Missing tutorial for custom models

### API Design: 8/10 (Very Good)
- CLI interface is comprehensive
- Configuration via command-line flags
- Output includes request-level metrics CSV
- Chrome trace support for visualization

### Reproducibility: 9/10 (Excellent)
- Deterministic with fixed seed (--seed 42)
- All parameters saved in config.json
- Pre-trained models included in repo
- Docker ensures consistent environment

### Error Handling: 7/10 (Good)
- Clear error messages for invalid configs
- Validation of model names against known list
- Warning for unsupported scheduler combinations

---

## Key Findings for Survey Paper

### 1. LLM Inference Simulation Leadership
VIDUR is currently the most comprehensive LLM inference simulator:
- Supports multiple scheduling algorithms (vLLM, Orca, Sarathi, LightLLM)
- Models prefill/decode phases separately
- Captures KV cache management and batching effects

### 2. Random Forest Execution Predictor
Uses ML-based execution time prediction:
- Trained on profiled kernel times
- Supports multiple GPU types (A100, H100)
- Achieves low prediction error (<5% claimed)

### 3. Integration with Industry Tools
- Compatible with vLLM scheduler logic
- Orca-style iteration-level scheduling
- Sarathi chunked prefill support

### 4. Platform Support
- Pure Python implementation
- Works on x86_64 and aarch64 via Docker
- No GPU required for simulation

---

## Artifacts Created

- Dockerfile: `scripts/benchmarks/vidur/Dockerfile`
- Results: `scripts/benchmarks/vidur/data/results/vidur/`
  - vLLM config: `2026-02-07_05-17-20-211661/`
  - Sarathi config: `2026-02-07_05-22-22-523702/`
  - Orca config: `2026-02-07_05-27-11-500012/`
- This evaluation report

---

## Recommendations

### For Survey Paper
1. Feature VIDUR as the primary LLM inference simulator
2. Ease of Use score: **8/10**
3. Highlight scheduler comparison capability
4. Note integration with production inference systems (vLLM)

### For Users
1. Use Docker for reliable setup
2. Start with pre-defined model configs (Llama-2, GPT-2)
3. Use --metrics_config_store_request_metrics for detailed analysis
4. Compare schedulers using same workload traces

---

*VIDUR demonstrates that LLM inference simulation can be accessible and practical for researchers without GPU access, enabling rapid design space exploration.*
