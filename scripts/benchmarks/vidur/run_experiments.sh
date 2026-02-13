#!/usr/bin/env bash
# Run VIDUR experiments across multiple schedulers for accuracy evaluation.
# Usage: run_experiments.sh <output_dir>
set -euo pipefail

OUTPUT_DIR="${1:-/app/results}"
mkdir -p "$OUTPUT_DIR"

MODEL="meta-llama/Llama-2-7b-hf"
DEVICE="a100"
NETWORK="a100_pairwise_nvlink"
NUM_REQUESTS=200
QPS=2.0
SEED=42

# Schedulers to evaluate
SCHEDULERS=("vllm" "sarathi" "orca")

for SCHEDULER in "${SCHEDULERS[@]}"; do
    echo "============================================="
    echo "Running VIDUR with scheduler: $SCHEDULER"
    echo "  Model: $MODEL, Device: $DEVICE"
    echo "  Requests: $NUM_REQUESTS, QPS: $QPS"
    echo "============================================="

    SCHED_OUT="$OUTPUT_DIR/$SCHEDULER"
    mkdir -p "$SCHED_OUT"

    EXTRA_ARGS=""
    if [ "$SCHEDULER" = "sarathi" ]; then
        EXTRA_ARGS="--replica_scheduler_chunk_size 512"
    fi

    python -m vidur.main \
        --replica_config_model_name "$MODEL" \
        --replica_config_device "$DEVICE" \
        --replica_config_network_device "$NETWORK" \
        --replica_scheduler_provider "$SCHEDULER" \
        --request_generator_provider synthetic \
        --synthetic_request_generator_num_requests "$NUM_REQUESTS" \
        --poisson_request_interval_generator_qps "$QPS" \
        --uniform_request_length_generator_min_tokens 128 \
        --uniform_request_length_generator_max_tokens 512 \
        --uniform_request_length_generator_prefill_to_decode_ratio 20.0 \
        --seed "$SEED" \
        --metrics_store_request_metrics \
        --metrics_store_batch_metrics \
        --metrics_store_utilization_metrics \
        --metrics_output_dir "$SCHED_OUT" \
        $EXTRA_ARGS \
        2>&1 | tee "$SCHED_OUT/run.log" || {
            echo "WARNING: $SCHEDULER run failed, continuing..."
            echo "FAILED" > "$SCHED_OUT/status.txt"
            continue
        }

    echo "COMPLETED" > "$SCHED_OUT/status.txt"
    echo "Scheduler $SCHEDULER completed successfully"
    echo ""
done

echo "All experiments complete. Results in $OUTPUT_DIR"
ls -la "$OUTPUT_DIR"/*/
