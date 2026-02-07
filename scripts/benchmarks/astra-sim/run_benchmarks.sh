#!/bin/bash
# ASTRA-sim Benchmark Suite Runner
# For ML Performance Survey evaluation

set -e

SCRIPT_DIR=$(dirname "$(realpath "$0")")
RESULTS_DIR="${SCRIPT_DIR}/../../../data/results/astra-sim"
ASTRA_SIM_DIR="/app/astra-sim"

mkdir -p "${RESULTS_DIR}"

echo "=== ASTRA-sim Benchmark Suite ==="
echo "Running inside Docker container"
echo ""

# Build if needed
if [ ! -f "${ASTRA_SIM_DIR}/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware" ]; then
    echo "Building ASTRA-sim..."
    cd "${ASTRA_SIM_DIR}"
    ./build/astra_analytical/build.sh
fi

ASTRA_SIM_BIN="${ASTRA_SIM_DIR}/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware"
EXAMPLE_DIR="${ASTRA_SIM_DIR}/examples"
SYSTEM="${EXAMPLE_DIR}/system/native_collectives/HGX-H100-validated.json"
NETWORK="${EXAMPLE_DIR}/network/analytical/HGX-H100-validated.yml"
REMOTE_MEMORY="${EXAMPLE_DIR}/remote_memory/analytical/no_memory_expansion.json"

run_benchmark() {
    local collective=$1
    local npus=$2
    local size=$3

    WORKLOAD="${EXAMPLE_DIR}/workload/microbenchmarks/${collective}/${npus}npus_${size}/${collective}"

    if [ -f "${WORKLOAD}.et" ] || [ -f "${WORKLOAD}.0.et" ]; then
        echo "Running: ${collective} - ${npus} NPUs - ${size}"

        OUTPUT_FILE="${RESULTS_DIR}/${collective}_${npus}npus_${size}.log"

        "${ASTRA_SIM_BIN}" \
            --workload-configuration="${WORKLOAD}" \
            --system-configuration="${SYSTEM}" \
            --remote-memory-configuration="${REMOTE_MEMORY}" \
            --network-configuration="${NETWORK}" 2>&1 | tee "${OUTPUT_FILE}"

        echo "---"
    else
        echo "Skipping: ${collective} - ${npus} NPUs - ${size} (workload not found)"
    fi
}

echo "=== All-Reduce Benchmarks ==="
run_benchmark "all_reduce" "4" "1MB"
run_benchmark "all_reduce" "8" "1MB"
run_benchmark "all_reduce" "16" "1MB"

echo ""
echo "=== All-Gather Benchmarks ==="
run_benchmark "all_gather" "4" "1MB"
run_benchmark "all_gather" "8" "1MB"
run_benchmark "all_gather" "16" "1MB"

echo ""
echo "=== Reduce-Scatter Benchmarks ==="
run_benchmark "reduce_scatter" "4" "1MB"
run_benchmark "reduce_scatter" "8" "1MB"
run_benchmark "reduce_scatter" "16" "1MB"

echo ""
echo "=== All-to-All Benchmarks ==="
run_benchmark "all_to_all" "4" "1MB"
run_benchmark "all_to_all" "8" "1MB"
run_benchmark "all_to_all" "16" "1MB"

echo ""
echo "=== Benchmark Suite Complete ==="
echo "Results saved to: ${RESULTS_DIR}"
