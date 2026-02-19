#!/usr/bin/env bash
# VIDUR LLM inference serving benchmarks targeting paper scenarios
#
# Paper scenarios covered by VIDUR:
#   I1.1: Llama-2-7B single-request inference latency (A100)
#   I1.2: Llama-2-13B single-request inference latency
#   I2.1: Llama-2-7B batched serving under vLLM (A100)
#   I2.2: Llama-2-13B batched serving under Sarathi-Serve
#   I2.3: Llama-2-7B batched serving under Orca
#   I3.1: Llama-2-7B with PagedAttention KV cache
#   I3.2: KV cache optimization under PagedAttention (partial)
#   I3.3: Long-context KV cache (Llama-2-7B, 8K context) (partial)
#
# VIDUR models prefill/decode phases, scheduler policies, preemption,
# and KV cache management. It does NOT model speculative decoding,
# prefix caching, quantized inference, or disaggregated serving (I5).
#
# Hardware: Simulated A100 (can also simulate H100)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="${RESULTS_DIR}/${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR"

echo "=== VIDUR LLM Inference Serving Benchmark Suite ==="
echo "Results directory: $OUTPUT_DIR"
echo ""

# ============================================================
# Configuration
# ============================================================
DOCKER_IMG="vidur-benchmarks"
NUM_REQUESTS=200
SEED=42

# Check if running in Docker or locally
USE_DOCKER=false
if docker image inspect "$DOCKER_IMG" &>/dev/null 2>&1; then
    USE_DOCKER=true
fi

run_vidur() {
    local description="$1"
    shift
    local output_name="$1"
    shift
    local args=("$@")

    echo "--- $description ---"
    local exp_dir="$OUTPUT_DIR/$output_name"
    mkdir -p "$exp_dir"

    if $USE_DOCKER; then
        timeout 300 docker run --rm \
            -v "$exp_dir:/results" \
            -e WANDB_MODE=disabled \
            "$DOCKER_IMG" \
            "${args[@]}" \
            --metrics_store_request_metrics \
            --metrics_store_batch_metrics \
            --metrics_store_utilization_metrics \
            --metrics_output_dir /results \
            --seed "$SEED" \
            2>&1 | tee "$exp_dir/run.log" || {
                echo "WARNING: $description failed"
                echo "FAILED" > "$exp_dir/status.txt"
                return 1
            }
    else
        timeout 300 python -m vidur.main \
            "${args[@]}" \
            --metrics_store_request_metrics \
            --metrics_store_batch_metrics \
            --metrics_store_utilization_metrics \
            --metrics_output_dir "$exp_dir" \
            --seed "$SEED" \
            2>&1 | tee "$exp_dir/run.log" || {
                echo "WARNING: $description failed"
                echo "FAILED" > "$exp_dir/status.txt"
                return 1
            }
    fi

    echo "COMPLETED" > "$exp_dir/status.txt"
    echo ""
}

# ============================================================
# Part 1: Paper reproduction - Llama-2-7B on A100
# Matches paper Table 4 (Section 4.3)
# ============================================================
echo "=== Part 1: Llama-2-7B on A100 (Paper Table 4) ==="
echo ""

# I2.1: vLLM scheduler
run_vidur "I2.1: Llama-2-7B vLLM on A100 (QPS=2.0)" \
    "llama2_7b_vllm_a100_qps2" \
    --replica_config_model_name "meta-llama/Llama-2-7b-hf" \
    --replica_config_device "a100" \
    --replica_config_network_device "a100_pairwise_nvlink" \
    --replica_scheduler_provider "vllm" \
    --request_generator_provider synthetic \
    --synthetic_request_generator_num_requests "$NUM_REQUESTS" \
    --poisson_request_interval_generator_qps 2.0 \
    --uniform_request_length_generator_min_tokens 128 \
    --uniform_request_length_generator_max_tokens 512 \
    --uniform_request_length_generator_prefill_to_decode_ratio 20.0

# I2.2: Sarathi-Serve scheduler (with chunked prefill)
run_vidur "I2.2: Llama-2-7B Sarathi on A100 (QPS=2.0)" \
    "llama2_7b_sarathi_a100_qps2" \
    --replica_config_model_name "meta-llama/Llama-2-7b-hf" \
    --replica_config_device "a100" \
    --replica_config_network_device "a100_pairwise_nvlink" \
    --replica_scheduler_provider "sarathi" \
    --replica_scheduler_chunk_size 512 \
    --request_generator_provider synthetic \
    --synthetic_request_generator_num_requests "$NUM_REQUESTS" \
    --poisson_request_interval_generator_qps 2.0 \
    --uniform_request_length_generator_min_tokens 128 \
    --uniform_request_length_generator_max_tokens 512 \
    --uniform_request_length_generator_prefill_to_decode_ratio 20.0

# I2.3: Orca scheduler
run_vidur "I2.3: Llama-2-7B Orca on A100 (QPS=2.0)" \
    "llama2_7b_orca_a100_qps2" \
    --replica_config_model_name "meta-llama/Llama-2-7b-hf" \
    --replica_config_device "a100" \
    --replica_config_network_device "a100_pairwise_nvlink" \
    --replica_scheduler_provider "orca" \
    --request_generator_provider synthetic \
    --synthetic_request_generator_num_requests "$NUM_REQUESTS" \
    --poisson_request_interval_generator_qps 2.0 \
    --uniform_request_length_generator_min_tokens 128 \
    --uniform_request_length_generator_max_tokens 512 \
    --uniform_request_length_generator_prefill_to_decode_ratio 20.0

# ============================================================
# Part 2: Higher QPS stress tests
# Paper notes: QPS 2.0 may not expose scheduling limitations
# ============================================================
echo "=== Part 2: Higher QPS Stress Tests ==="
echo ""

for qps in 4.0 8.0; do
    run_vidur "Llama-2-7B vLLM QPS=$qps" \
        "llama2_7b_vllm_a100_qps${qps//./_}" \
        --replica_config_model_name "meta-llama/Llama-2-7b-hf" \
        --replica_config_device "a100" \
        --replica_config_network_device "a100_pairwise_nvlink" \
        --replica_scheduler_provider "vllm" \
        --request_generator_provider synthetic \
        --synthetic_request_generator_num_requests "$NUM_REQUESTS" \
        --poisson_request_interval_generator_qps "$qps" \
        --uniform_request_length_generator_min_tokens 128 \
        --uniform_request_length_generator_max_tokens 512 \
        --uniform_request_length_generator_prefill_to_decode_ratio 20.0

    run_vidur "Llama-2-7B Sarathi QPS=$qps" \
        "llama2_7b_sarathi_a100_qps${qps//./_}" \
        --replica_config_model_name "meta-llama/Llama-2-7b-hf" \
        --replica_config_device "a100" \
        --replica_config_network_device "a100_pairwise_nvlink" \
        --replica_scheduler_provider "sarathi" \
        --replica_scheduler_chunk_size 512 \
        --request_generator_provider synthetic \
        --synthetic_request_generator_num_requests "$NUM_REQUESTS" \
        --poisson_request_interval_generator_qps "$qps" \
        --uniform_request_length_generator_min_tokens 128 \
        --uniform_request_length_generator_max_tokens 512 \
        --uniform_request_length_generator_prefill_to_decode_ratio 20.0
done

# ============================================================
# Part 3: Llama-2-13B experiments (I2.2 in paper)
# ============================================================
echo "=== Part 3: Llama-2-13B Serving Experiments ==="
echo ""

run_vidur "I2.2: Llama-2-13B Sarathi on A100 (QPS=2.0)" \
    "llama2_13b_sarathi_a100_qps2" \
    --replica_config_model_name "meta-llama/Llama-2-13b-hf" \
    --replica_config_device "a100" \
    --replica_config_network_device "a100_pairwise_nvlink" \
    --replica_scheduler_provider "sarathi" \
    --replica_scheduler_chunk_size 512 \
    --request_generator_provider synthetic \
    --synthetic_request_generator_num_requests "$NUM_REQUESTS" \
    --poisson_request_interval_generator_qps 2.0 \
    --uniform_request_length_generator_min_tokens 128 \
    --uniform_request_length_generator_max_tokens 512 \
    --uniform_request_length_generator_prefill_to_decode_ratio 20.0

run_vidur "Llama-2-13B vLLM on A100 (QPS=2.0)" \
    "llama2_13b_vllm_a100_qps2" \
    --replica_config_model_name "meta-llama/Llama-2-13b-hf" \
    --replica_config_device "a100" \
    --replica_config_network_device "a100_pairwise_nvlink" \
    --replica_scheduler_provider "vllm" \
    --request_generator_provider synthetic \
    --synthetic_request_generator_num_requests "$NUM_REQUESTS" \
    --poisson_request_interval_generator_qps 2.0 \
    --uniform_request_length_generator_min_tokens 128 \
    --uniform_request_length_generator_max_tokens 512 \
    --uniform_request_length_generator_prefill_to_decode_ratio 20.0

# ============================================================
# Part 4: H100 experiments (if device config available)
# ============================================================
echo "=== Part 4: H100 Device Experiments ==="
echo ""

run_vidur "Llama-2-7B vLLM on H100 (QPS=2.0)" \
    "llama2_7b_vllm_h100_qps2" \
    --replica_config_model_name "meta-llama/Llama-2-7b-hf" \
    --replica_config_device "h100" \
    --replica_config_network_device "h100_pairwise_nvlink" \
    --replica_scheduler_provider "vllm" \
    --request_generator_provider synthetic \
    --synthetic_request_generator_num_requests "$NUM_REQUESTS" \
    --poisson_request_interval_generator_qps 2.0 \
    --uniform_request_length_generator_min_tokens 128 \
    --uniform_request_length_generator_max_tokens 512 \
    --uniform_request_length_generator_prefill_to_decode_ratio 20.0 || {
    echo "NOTE: H100 device config may not be available in VIDUR. A100 results above are primary."
}

# ============================================================
# Part 5: Parse results
# ============================================================
echo ""
echo "=== Parsing Results ==="

ANALYZE_SCRIPT="${SCRIPT_DIR}/../../benchmarks/vidur/analyze_results.py"
if [ -f "$ANALYZE_SCRIPT" ]; then
    for exp_dir in "$OUTPUT_DIR"/*/; do
        if [ -f "$exp_dir/status.txt" ] && grep -q "COMPLETED" "$exp_dir/status.txt"; then
            exp_name=$(basename "$exp_dir")
            echo "--- Analyzing: $exp_name ---"
            python3 "$ANALYZE_SCRIPT" --results-dir "$exp_dir" \
                2>&1 | tee "$exp_dir/analysis.log" || true
        fi
    done
fi

# ============================================================
# Summary
# ============================================================
echo ""
echo "=== Benchmark Complete ==="
echo "Results saved to: $OUTPUT_DIR"
echo ""
echo "Experiment status:"
for exp_dir in "$OUTPUT_DIR"/*/; do
    exp_name=$(basename "$exp_dir")
    if [ -f "$exp_dir/status.txt" ]; then
        status=$(cat "$exp_dir/status.txt")
        echo "  $exp_name: $status"
    fi
done
echo ""
echo "=== Expected Results (from paper Table 4) ==="
echo "Llama-2-7B vLLM A100 QPS=2.0:"
echo "  - Mean TTFT: ~150-300ms"
echo "  - Mean TPOT: ~30-60ms"
echo "  - P99 TTFT: higher (preemption effects)"
echo ""
echo "Llama-2-7B Sarathi A100 QPS=2.0:"
echo "  - Lower P99 latency (chunked prefill reduces head-of-line blocking)"
echo "  - Zero preemptions expected"
echo ""
echo "Key comparison: Sarathi vs vLLM preemption behavior"
echo "Paper finding: Sarathi achieves zero preemptions, lower P99 latency"
echo ""
echo "Please send the results directory back for analysis."
