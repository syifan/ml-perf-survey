#!/usr/bin/env bash
# Timeloop benchmark script
#
# Timeloop is an accelerator (NPU) energy/performance modeling tool.
# It evaluates architectures like Eyeriss, NOT GPU workloads.
# It has 0% LLM benchmark suite coverage (paper Table 6).
#
# We include Timeloop experiments for paper completeness (Section 4.5):
# - ResNet-50 Conv1 on Eyeriss-like architecture (168 PEs)
# - Energy breakdown by memory hierarchy level
# - Utilization analysis
#
# These experiments do NOT require GPU hardware.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="${RESULTS_DIR}/${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR"

echo "=== Timeloop Accelerator Benchmark Suite ==="
echo "Results directory: $OUTPUT_DIR"
echo ""
echo "NOTE: Timeloop models NPU accelerators, not GPU workloads."
echo "These experiments reproduce paper Section 4.5 findings."
echo ""

# ============================================================
# Option A: Run via Docker (recommended)
# ============================================================
run_docker() {
    echo "=== Running via Docker ==="

    # Build a custom image with our scripts
    DOCKER_IMG="timeloop-benchmarks"

    docker build -t "$DOCKER_IMG" -f - . <<'DOCKERFILE'
FROM timeloopaccelergy/timeloop-accelergy-pytorch:latest
WORKDIR /workspace
COPY ../../benchmarks/timeloop/run_resnet50_conv.py /workspace/run_resnet50_conv.py
RUN pip install pyyaml
DOCKERFILE

    docker run --rm \
        -v "$OUTPUT_DIR:/results" \
        "$DOCKER_IMG" \
        python3 /workspace/run_resnet50_conv.py --output-dir /results

    echo "Docker run complete. Results in $OUTPUT_DIR"
}

# ============================================================
# Option B: Run with local Timeloop installation
# ============================================================
run_local() {
    echo "=== Running with local Timeloop ==="

    TIMELOOP_SCRIPT="${SCRIPT_DIR}/../../benchmarks/timeloop/run_resnet50_conv.py"

    if [ ! -f "$TIMELOOP_SCRIPT" ]; then
        echo "ERROR: run_resnet50_conv.py not found at $TIMELOOP_SCRIPT"
        exit 1
    fi

    # Run the existing benchmark script
    python3 "$TIMELOOP_SCRIPT" --output-dir "$OUTPUT_DIR" \
        2>&1 | tee "$OUTPUT_DIR/timeloop_run.log"
}

# ============================================================
# Option C: Analytical estimates only (no Timeloop binary needed)
# ============================================================
run_analytical() {
    echo "=== Analytical Estimates Only (no Timeloop binary) ==="

    TIMELOOP_SCRIPT="${SCRIPT_DIR}/../../benchmarks/timeloop/run_resnet50_conv.py"

    python3 "$TIMELOOP_SCRIPT" --analytical-only --output-dir "$OUTPUT_DIR" \
        2>&1 | tee "$OUTPUT_DIR/analytical_only.log"
}

# ============================================================
# Main: Try Docker first, then local, then analytical
# ============================================================
if command -v docker &>/dev/null; then
    run_docker || {
        echo "Docker run failed. Trying local installation..."
        if command -v timeloop-mapper &>/dev/null; then
            run_local
        else
            echo "Timeloop not installed locally. Running analytical estimates only."
            run_analytical
        fi
    }
elif command -v timeloop-mapper &>/dev/null; then
    run_local
else
    echo "Neither Docker nor Timeloop found."
    echo "Running analytical estimates only."
    run_analytical
fi

echo ""
echo "=== Benchmark Complete ==="
echo "Results saved to: $OUTPUT_DIR"
echo ""
echo "=== Expected outputs for paper Section 4.5 ==="
echo "- ResNet-50 Conv1 energy breakdown (DRAM vs GLB vs PE)"
echo "- Utilization: ~50-75% for Conv1 (C=3 limits PE utilization)"
echo "- Energy: ~5500 fJ/MAC (Eyeriss published data)"
echo ""
echo "=== LLM Benchmark Coverage ==="
echo "Timeloop provides 0/28 LLM scenario coverage."
echo "It is an accelerator design-space exploration tool, not an LLM predictor."
