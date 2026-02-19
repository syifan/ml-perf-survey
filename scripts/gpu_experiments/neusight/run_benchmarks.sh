#!/usr/bin/env bash
# NeuSight GPU benchmarks targeting paper scenarios
#
# Paper scenarios covered by NeuSight (kernel-level predictions):
#   I1.1: Llama-2-7B single-request inference (H100/A100)
#   I1.2: Llama-2-13B single-request inference (A100)
#   I1.3: Llama-2-70B single-request inference (H100)
#   T1.1: GPT-2 data-parallel on 8xA100 (per-GPU kernel time)
#   T2.1: Llama-2-13B tensor-parallel on 4xA100 (per-GPU kernel time)
#
# NeuSight predicts per-GPU kernel latency using tile-based decomposition.
# It does NOT model communication overhead (AllReduce, pipeline bubbles).
# For distributed scenarios, NeuSight provides only the compute component.
#
# Models tested: GPT-2, GPT-3, Llama-2-7B/13B/70B, BERT, OPT, SwitchXL
# GPUs: H100, A100 (SXM4 and PCIe variants)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEUSIGHT_DIR="${NEUSIGHT_DIR:-/tmp/NeuSight}"
RESULTS_DIR="${SCRIPT_DIR}/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="${RESULTS_DIR}/${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR"

echo "=== NeuSight GPU Benchmark Suite ==="
echo "Results directory: $OUTPUT_DIR"
echo ""

# Detect GPU type
GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1 | xargs)
echo "Detected GPU: $GPU_NAME"
echo ""

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate neusight

cd "$NEUSIGHT_DIR"

# ============================================================
# Part 1: Validate NeuSight on artifact prediction/label pairs
# This reproduces the paper's accuracy analysis (Table in Section 4.1)
# ============================================================
echo "=== Part 1: Artifact-Based Accuracy Validation ==="
echo "Re-analyzing NeuSight's pre-computed prediction/label pairs..."

python3 "${SCRIPT_DIR}/../../benchmarks/neusight/run_neusight_prediction.py" \
    --output-dir "$OUTPUT_DIR/artifact_validation" \
    2>&1 | tee "$OUTPUT_DIR/artifact_validation.log"

echo ""

# ============================================================
# Part 2: Run NeuSight predictions on actual GPU hardware
# These are the key experiments that require H100/A100
# ============================================================
echo "=== Part 2: Live GPU Predictions ==="

# Define benchmark configurations matching paper scenarios
# Format: model_name mode sequence_length batch_size
BENCHMARKS=(
    # I1.1: Llama-2-7B single-request inference
    "llama2-7b inf 2048 1"
    "llama2-7b inf 4096 1"
    # I1.2: Llama-2-13B single-request inference
    "llama2-13b inf 2048 1"
    # I1.3: Llama-2-70B single-request inference
    "llama2-70b inf 2048 1"
    # T1.1: GPT-2 training (per-GPU kernel time for DP scenario)
    "gpt2-large train 1024 4"
    "gpt2-large train 1024 8"
    # GPT-3 variants
    "gpt3-2.7b inf 2048 1"
    "gpt3-2.7b train 2048 4"
    # BERT baselines (for cross-validation with paper Table 5)
    "bert-large inf 512 4"
    "bert-large inf 512 8"
    "bert-large inf 512 16"
    "bert-large train 512 4"
    # OPT models
    "opt-13b inf 2048 1"
    # SwitchXL (MoE architecture - higher variance expected per paper)
    "switchxl4 inf 512 1"
)

# NeuSight's prediction script (from their repo)
PREDICT_SCRIPT="scripts/asplos/predict.py"

if [ -f "$NEUSIGHT_DIR/$PREDICT_SCRIPT" ]; then
    for benchmark in "${BENCHMARKS[@]}"; do
        read -r model mode seqlen batch <<< "$benchmark"
        echo "--- Running: $model $mode seq=$seqlen batch=$batch ---"

        timeout 300 python3 "$NEUSIGHT_DIR/$PREDICT_SCRIPT" \
            --model "$model" \
            --mode "$mode" \
            --seq-len "$seqlen" \
            --batch-size "$batch" \
            --output "$OUTPUT_DIR/live_${model}_${mode}_${seqlen}_${batch}.json" \
            2>&1 | tee -a "$OUTPUT_DIR/live_predictions.log" || {
                echo "WARNING: $model $mode failed, continuing..."
                echo "{\"model\": \"$model\", \"mode\": \"$mode\", \"status\": \"FAILED\"}" \
                    > "$OUTPUT_DIR/live_${model}_${mode}_${seqlen}_${batch}.json"
            }
        echo ""
    done
else
    echo "WARNING: NeuSight predict.py not found at expected path."
    echo "Attempting alternative: running via NeuSight's main entry point..."

    # Try alternative invocation methods
    if [ -f "$NEUSIGHT_DIR/main.py" ]; then
        for benchmark in "${BENCHMARKS[@]}"; do
            read -r model mode seqlen batch <<< "$benchmark"
            echo "--- Running: $model $mode seq=$seqlen batch=$batch ---"
            timeout 300 python3 "$NEUSIGHT_DIR/main.py" \
                --model "$model" --mode "$mode" \
                --seq-len "$seqlen" --batch-size "$batch" \
                2>&1 | tee -a "$OUTPUT_DIR/live_predictions.log" || true
            echo ""
        done
    else
        echo "ERROR: Cannot find NeuSight entry point. Check repository structure."
        echo "Listing available scripts:"
        find "$NEUSIGHT_DIR" -name "*.py" -maxdepth 2 | head -20
        echo ""
        echo "You may need to adapt the invocation. See NeuSight README for usage."
    fi
fi

# ============================================================
# Part 3: Parallelism-specific experiments
# Paper Section 4.1: DP4/TP4/PP4 comparison on A100 with GPT-2-Large
# ============================================================
echo ""
echo "=== Part 3: Parallelism Strategy Comparison ==="
echo "GPT-2-Large on A100, batch=4: DP4 vs TP4 vs PP4"
echo "(NeuSight predicts per-GPU kernel time only; communication is NOT modeled)"

PARALLEL_CONFIGS=(
    "gpt2-large train 1024 4 dp4"
    "gpt2-large train 1024 4 tp4"
    "gpt2-large train 1024 4 pp4"
)

for config in "${PARALLEL_CONFIGS[@]}"; do
    read -r model mode seqlen batch parallel <<< "$config"
    echo "--- $parallel: $model $mode batch=$batch ---"

    if [ -f "$NEUSIGHT_DIR/$PREDICT_SCRIPT" ]; then
        timeout 300 python3 "$NEUSIGHT_DIR/$PREDICT_SCRIPT" \
            --model "$model" --mode "$mode" \
            --seq-len "$seqlen" --batch-size "$batch" \
            --parallel-strategy "$parallel" \
            --output "$OUTPUT_DIR/parallel_${model}_${parallel}.json" \
            2>&1 | tee -a "$OUTPUT_DIR/parallel_predictions.log" || {
                echo "WARNING: $parallel config failed"
            }
    else
        echo "SKIP: predict.py not available"
    fi
    echo ""
done

# ============================================================
# Part 4: Fusion comparison (paper finding: fused > unfused error)
# ============================================================
echo ""
echo "=== Part 4: Operator Fusion Comparison ==="
echo "Paper finding: H100 GPT-2-Large fused=19.37% vs unfused=6.80% at batch 8"

for fuse_mode in "fused" "unfused"; do
    echo "--- GPT-2-Large batch=8 $fuse_mode ---"
    if [ -f "$NEUSIGHT_DIR/$PREDICT_SCRIPT" ]; then
        timeout 300 python3 "$NEUSIGHT_DIR/$PREDICT_SCRIPT" \
            --model "gpt2-large" --mode "inf" \
            --seq-len 1024 --batch-size 8 \
            --fusion "$fuse_mode" \
            --output "$OUTPUT_DIR/fusion_gpt2large_${fuse_mode}.json" \
            2>&1 | tee -a "$OUTPUT_DIR/fusion_predictions.log" || true
    fi
done

# ============================================================
# Summary
# ============================================================
echo ""
echo "=== Benchmark Complete ==="
echo "Results saved to: $OUTPUT_DIR"
echo ""
echo "Files generated:"
ls -la "$OUTPUT_DIR"/ 2>/dev/null || true
echo ""
echo "GPU used: $GPU_NAME"
echo "Timestamp: $TIMESTAMP"
echo ""
echo "=== Expected outputs for paper Table 5 ==="
echo "- Per-model MAPE across GPU types (verify paper's 5.87-27.10% range)"
echo "- DP4/TP4/PP4 comparison (verify paper's 12.87%/8.40%/10.26% APE)"
echo "- Fused vs unfused error (verify paper's 19.37% vs 6.80%)"
echo ""
echo "Please send the results directory back for analysis."
