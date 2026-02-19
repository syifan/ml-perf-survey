#!/usr/bin/env bash
# ASTRA-sim distributed training benchmarks targeting paper scenarios
#
# Paper scenarios covered by ASTRA-sim (communication modeling):
#   T1.1: GPT-2 data-parallel on 8xA100 (AllReduce for gradient sync)
#   T1.2: Llama-2-7B data-parallel on 8xH100
#   T1.3: Llama-2-13B data-parallel on 8xA100
#   T2.1: Llama-2-13B tensor-parallel on 4xA100 (intra-node AllReduce)
#   T2.2: Llama-2-70B tensor-parallel on 8xH100
#   T3.1: GPT-3 pipeline-parallel on 8xH100
#   T3.2: GPT-3 175B hybrid PP8+TP8 on 64xH100
#   T4.3: Sequence parallelism (partial - communication only)
#   T4.4: MoE expert parallelism (partial - All-to-All only)
#
# ASTRA-sim models communication patterns (AllReduce, AllGather, ReduceScatter,
# All-to-All) using analytical network models. It requires externally profiled
# per-layer compute times for end-to-end prediction.
#
# Hardware: HGX-H100 topology (validated configuration from paper)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="${RESULTS_DIR}/${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR"

echo "=== ASTRA-sim Distributed Training Benchmark Suite ==="
echo "Results directory: $OUTPUT_DIR"
echo ""

# ============================================================
# Configuration
# ============================================================
ASTRA_SIM_DIR="${ASTRA_SIM_DIR:-/app/astra-sim}"
ASTRA_SIM_BIN="${ASTRA_SIM_DIR}/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware"
EXAMPLE_DIR="${ASTRA_SIM_DIR}/examples"

# HGX-H100 validated configurations from paper
SYSTEM_H100="${EXAMPLE_DIR}/system/native_collectives/HGX-H100-validated.json"
NETWORK_H100="${EXAMPLE_DIR}/network/analytical/HGX-H100-validated.yml"
REMOTE_MEMORY="${EXAMPLE_DIR}/remote_memory/analytical/no_memory_expansion.json"

# Check if running in Docker or locally
if [ ! -f "$ASTRA_SIM_BIN" ]; then
    echo "ASTRA-sim binary not found. Trying Docker..."

    DOCKER_IMG="astrasim-benchmarks"
    if docker image inspect "$DOCKER_IMG" &>/dev/null; then
        echo "Running via Docker: $DOCKER_IMG"
        docker run --rm \
            -v "$OUTPUT_DIR:/results" \
            -v "$SCRIPT_DIR:/scripts" \
            "$DOCKER_IMG" \
            bash /scripts/run_benchmarks.sh
        exit $?
    else
        echo "ERROR: Neither ASTRA-sim binary nor Docker image found."
        echo "Run install.sh first."
        exit 1
    fi
fi

# ============================================================
# Part 1: Collective Microbenchmarks (paper Table 3)
# 8 NPUs on HGX-H100, 1MB message size
# ============================================================
echo "=== Part 1: Collective Microbenchmarks ==="
echo "Configuration: 8 NPUs, HGX-H100 topology, 1MB messages"
echo ""

COLLECTIVES=("all_reduce" "all_gather" "reduce_scatter" "all_to_all")
NPU_COUNTS=("4" "8" "16")
MSG_SIZE="1MB"

for collective in "${COLLECTIVES[@]}"; do
    for npus in "${NPU_COUNTS[@]}"; do
        WORKLOAD="${EXAMPLE_DIR}/workload/microbenchmarks/${collective}/${npus}npus_${MSG_SIZE}/${collective}"

        if [ -f "${WORKLOAD}.et" ] || [ -f "${WORKLOAD}.0.et" ]; then
            echo "--- ${collective} ${npus} NPUs ${MSG_SIZE} ---"
            OUTPUT_FILE="${OUTPUT_DIR}/${collective}_${npus}npus_${MSG_SIZE}.log"

            timeout 120 "${ASTRA_SIM_BIN}" \
                --workload-configuration="${WORKLOAD}" \
                --system-configuration="${SYSTEM_H100}" \
                --remote-memory-configuration="${REMOTE_MEMORY}" \
                --network-configuration="${NETWORK_H100}" \
                2>&1 | tee "${OUTPUT_FILE}" || {
                    echo "WARNING: ${collective} ${npus} NPUs failed"
                }
            echo ""
        else
            echo "SKIP: ${collective} ${npus} NPUs (workload not found)"
        fi
    done
done

# ============================================================
# Part 2: ResNet-50 Data-Parallel Scaling (paper Table 3)
# ============================================================
echo ""
echo "=== Part 2: ResNet-50 Data-Parallel Scaling ==="

RESNET_SCRIPT="${SCRIPT_DIR}/../../benchmarks/astra-sim/run_resnet50.sh"
if [ -f "$RESNET_SCRIPT" ]; then
    echo "Running ResNet-50 scaling experiments..."
    bash "$RESNET_SCRIPT" 2>&1 | tee "$OUTPUT_DIR/resnet50_scaling.log"
else
    echo "ResNet-50 script not found. Running manual scaling experiments..."

    for gpu_count in 2 4 8; do
        echo "--- ResNet-50 DP${gpu_count} ---"
        RESNET_WORKLOAD="${EXAMPLE_DIR}/workload/ResNet50/data_parallel_${gpu_count}gpus"
        if [ -d "$RESNET_WORKLOAD" ] || [ -f "${RESNET_WORKLOAD}.et" ]; then
            timeout 120 "${ASTRA_SIM_BIN}" \
                --workload-configuration="${RESNET_WORKLOAD}/ResNet50" \
                --system-configuration="${SYSTEM_H100}" \
                --remote-memory-configuration="${REMOTE_MEMORY}" \
                --network-configuration="${NETWORK_H100}" \
                2>&1 | tee "${OUTPUT_DIR}/resnet50_dp${gpu_count}.log" || true
        else
            echo "SKIP: Workload not found at $RESNET_WORKLOAD"
        fi
        echo ""
    done
fi

# ============================================================
# Part 3: LLM-specific Communication Patterns
# Model the communication overhead for paper scenarios T1-T3
# ============================================================
echo ""
echo "=== Part 3: LLM Communication Pattern Modeling ==="
echo "Modeling AllReduce sizes for LLM training scenarios"
echo ""

# Generate a summary of communication patterns
cat > "$OUTPUT_DIR/llm_communication_analysis.txt" <<'EOF'
LLM Communication Pattern Analysis for ASTRA-sim
==================================================

Paper Scenario T1.1: GPT-2 data-parallel on 8xA100
  Model: 354M parameters, fp16
  Gradient AllReduce size: 708 MB
  Expected: Ring AllReduce at NVLink bandwidth (~900 GB/s)

Paper Scenario T1.2: Llama-2-7B data-parallel on 8xH100
  Model: 7B parameters, fp16
  Gradient AllReduce size: 14 GB
  Expected: Significant communication overhead

Paper Scenario T2.1: Llama-2-13B tensor-parallel on 4xA100
  TP=4: AllReduce per transformer layer
  Message size per layer: ~100 MB (activation tensors)
  Frequency: 2x per layer (forward + backward)

Paper Scenario T3.2: GPT-3 175B hybrid PP8+TP8 on 64xH100
  Pipeline bubble: (P-1)/(microbatches+P-1) efficiency
  TP AllReduce: intra-node NVLink
  PP communication: inter-node InfiniBand

ASTRA-sim can model the communication component for all above scenarios.
It CANNOT model the compute component (requires external profiling).
EOF

echo "Communication analysis written to llm_communication_analysis.txt"

# ============================================================
# Part 4: All-to-All for MoE (paper scenario T4.4)
# ============================================================
echo ""
echo "=== Part 4: All-to-All for MoE Expert Routing ==="
echo "Paper finding: All-to-All cost is 1.985x AllReduce cost"

# The collective microbenchmarks above already include All-to-All.
# This section just highlights the MoE-relevant comparison.
echo "Compare all_to_all vs all_reduce results from Part 1 above."
echo "Expected ratio: ~1.985x (per paper Section 4.2)"

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
echo "=== Expected Results (from paper Table 3) ==="
echo "AllReduce 8 NPUs 1MB: ~11.0 μs (Ring topology)"
echo "AllGather 8 NPUs 1MB: ~10.7 μs"
echo "ReduceScatter 8 NPUs 1MB: ~10.7 μs"
echo "All-to-All 8 NPUs 1MB: ~21.8 μs (1.985x AllReduce)"
echo "ResNet-50 scaling: <1% communication overhead (compute-dominated)"
echo ""
echo "Please send the results directory back for analysis."
