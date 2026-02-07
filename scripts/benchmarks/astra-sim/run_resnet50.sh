#!/bin/bash
# ASTRA-sim ResNet-50 Training Simulation
# For ML Performance Survey - Issue #170
set -e

ASTRA_SIM_DIR="/app/astra-sim"
RESULTS_DIR="/app/results"
WORKLOAD_DIR="/app/workloads"

mkdir -p "${RESULTS_DIR}" "${WORKLOAD_DIR}"

ASTRA_SIM_BIN="${ASTRA_SIM_DIR}/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware"
EXAMPLE_DIR="${ASTRA_SIM_DIR}/examples"
REMOTE_MEMORY="${EXAMPLE_DIR}/remote_memory/analytical/no_memory_expansion.json"

echo "=== ASTRA-sim ResNet-50 Training Simulation ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "ASTRA-sim version: $(cd ${ASTRA_SIM_DIR} && git rev-parse --short HEAD)"
echo ""

# --- Step 1: Locate ResNet-50 workload ---
RESNET_TXT="/app/Resnet50_DataParallel.txt"
echo "ResNet-50 workload: ${RESNET_TXT}"
echo "Contents preview:"
head -5 "${RESNET_TXT}"
echo "..."
echo "Total layers: $(tail -n +3 ${RESNET_TXT} | wc -l)"
echo ""

# --- Step 2: Generate Chakra ET traces ---
echo "=== Generating Chakra ET traces ==="

# Write Python trace generator inline
cat > /app/gen_traces.py << 'PYGEN'
#!/usr/bin/env python3
"""Convert ASTRA-sim v1.0 text workload to Chakra ET traces for v2.0."""
import sys
import os
import struct

# Add Chakra paths
for p in [
    "/app/astra-sim/extern/graph_frontend/chakra",
    "/app/astra-sim/extern/graph_frontend/chakra/src",
]:
    if os.path.exists(p):
        sys.path.insert(0, p)
        for sub in ["src", "schema", "schema/protobuf"]:
            sp = os.path.join(p, sub)
            if os.path.exists(sp):
                sys.path.insert(0, sp)

from chakra.schema.protobuf import et_def_pb2
from google.protobuf.internal.encoder import _EncodeVarint

def parse_v1_workload(filepath):
    """Parse ASTRA-sim v1.0 tab-delimited workload file.

    Format per line (tab-separated):
    name -1 fwd_comp NONE 0 inp_grad NONE 0 wt_grad ALLREDUCE comm_size delay
    """
    layers = []
    with open(filepath) as f:
        lines = [l.strip() for l in f if l.strip()]

    # First line: parallelization strategy (e.g., DATA)
    strategy = lines[0]
    num_layers = int(lines[1])

    for i in range(2, 2 + num_layers):
        parts = lines[i].split('\t')
        if len(parts) < 12:
            parts = lines[i].split()
        if len(parts) < 12:
            print(f"WARNING: Skipping malformed line {i}: {lines[i][:80]}")
            continue

        layers.append({
            'name': parts[0],
            'fwd_compute': int(parts[2]),    # forward compute (cycles)
            'inp_grad': int(parts[5]),        # input gradient compute
            'wt_grad': int(parts[8]),         # weight gradient compute
            'collective': parts[9],           # ALLREDUCE or NONE
            'comm_size': int(parts[10]),      # bytes
            'delay': int(parts[11]),          # delay cycles
        })

    return layers, strategy

def generate_et(layers, output_prefix, num_npus):
    """Generate Chakra ET protobuf traces."""
    for npu_id in range(num_npus):
        output_file = f"{output_prefix}.{npu_id}.et"
        with open(output_file, 'wb') as f:
            # Write GlobalMetadata
            meta = et_def_pb2.GlobalMetadata()
            meta.version = "0.0.4"
            meta_bytes = meta.SerializeToString()
            _EncodeVarint(f.write, len(meta_bytes))
            f.write(meta_bytes)

            node_id = 0
            prev_id = None

            for layer in layers:
                # Forward compute node
                fwd = et_def_pb2.Node()
                fwd.id = node_id
                fwd.name = f"{layer['name']}_fwd"
                fwd.type = et_def_pb2.COMP_NODE
                a = fwd.attr.add()
                a.name = "duration_micros"
                a.int64_val = layer['fwd_compute']
                if prev_id is not None:
                    fwd.data_deps.append(prev_id)
                prev_id = node_id
                node_id += 1
                _EncodeVarint(f.write, len(fwd.SerializeToString()))
                f.write(fwd.SerializeToString())

                # Backward input gradient
                bwd_i = et_def_pb2.Node()
                bwd_i.id = node_id
                bwd_i.name = f"{layer['name']}_bwd_inp"
                bwd_i.type = et_def_pb2.COMP_NODE
                a2 = bwd_i.attr.add()
                a2.name = "duration_micros"
                a2.int64_val = layer['inp_grad']
                bwd_i.data_deps.append(prev_id)
                prev_id = node_id
                node_id += 1
                _EncodeVarint(f.write, len(bwd_i.SerializeToString()))
                f.write(bwd_i.SerializeToString())

                # Backward weight gradient
                bwd_w = et_def_pb2.Node()
                bwd_w.id = node_id
                bwd_w.name = f"{layer['name']}_bwd_wt"
                bwd_w.type = et_def_pb2.COMP_NODE
                a3 = bwd_w.attr.add()
                a3.name = "duration_micros"
                a3.int64_val = layer['wt_grad']
                bwd_w.data_deps.append(prev_id)
                prev_id = node_id
                node_id += 1
                _EncodeVarint(f.write, len(bwd_w.SerializeToString()))
                f.write(bwd_w.SerializeToString())

                # Communication (all-reduce)
                if layer['collective'] == 'ALLREDUCE' and layer['comm_size'] > 0:
                    comm = et_def_pb2.Node()
                    comm.id = node_id
                    comm.name = f"{layer['name']}_allreduce"
                    comm.type = et_def_pb2.COMM_COLL_NODE
                    cs = comm.attr.add()
                    cs.name = "comm_size"
                    cs.int64_val = layer['comm_size']
                    ct = comm.attr.add()
                    ct.name = "comm_type"
                    ct.int64_val = int(et_def_pb2.ALL_REDUCE)
                    comm.data_deps.append(prev_id)
                    prev_id = node_id
                    node_id += 1
                    _EncodeVarint(f.write, len(comm.SerializeToString()))
                    f.write(comm.SerializeToString())

        print(f"  Generated {output_file} ({node_id} nodes)")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--num-npus', type=int, default=8)
    args = parser.parse_args()

    layers, strategy = parse_v1_workload(args.input)
    print(f"Parsed {len(layers)} layers, strategy: {strategy}")
    generate_et(layers, args.output, args.num_npus)
    print("Done!")
PYGEN

# Generate traces for different NPU counts
for npus in 4 8 16; do
    TRACE_PREFIX="${WORKLOAD_DIR}/Resnet50_DataParallel_${npus}npus"
    echo "Generating traces for ${npus} NPUs..."

    # Try chakra_converter first
    if command -v chakra_converter &> /dev/null; then
        chakra_converter Text \
            --input "${RESNET_TXT}" \
            --output "${TRACE_PREFIX}" \
            --num-npus "${npus}" \
            --num-passes 1 2>&1 && continue
    fi

    # Fallback to Python script
    python3 /app/gen_traces.py \
        --input "${RESNET_TXT}" \
        --output "${TRACE_PREFIX}" \
        --num-npus "${npus}" 2>&1
done

echo ""

# --- Step 3: Run simulations ---
echo "=== Running ASTRA-sim Simulations ==="

SYSTEM_H100="${EXAMPLE_DIR}/system/native_collectives/HGX-H100-validated.json"
NETWORK_H100="${EXAMPLE_DIR}/network/analytical/HGX-H100-validated.yml"

echo "System config: ${SYSTEM_H100}"
echo "Network config: ${NETWORK_H100}"
echo ""

run_sim() {
    local npus=$1
    local sys_cfg=$2
    local net_cfg=$3
    local label=$4

    local trace="${WORKLOAD_DIR}/Resnet50_DataParallel_${npus}npus"
    local outfile="${RESULTS_DIR}/resnet50_${label}_${npus}npus.log"

    if [ ! -f "${trace}.0.et" ]; then
        echo "SKIP: ${label} ${npus}NPUs - traces not found"
        return
    fi

    echo ">>> Running: ResNet-50 ${label} ${npus} NPUs"
    "${ASTRA_SIM_BIN}" \
        --workload-configuration="${trace}" \
        --system-configuration="${sys_cfg}" \
        --network-configuration="${net_cfg}" \
        --remote-memory-configuration="${REMOTE_MEMORY}" 2>&1 | tee "${outfile}"
    echo "<<< Saved: ${outfile}"
    echo ""
}

# Primary: HGX-H100 validated config
for npus in 4 8 16; do
    run_sim ${npus} "${SYSTEM_H100}" "${NETWORK_H100}" "hgx-h100-validated"
done

# Also run with input network configs if available
INPUTS_DIR="${ASTRA_SIM_DIR}/inputs"
if [ -d "${INPUTS_DIR}/network" ]; then
    for net_cfg in "${INPUTS_DIR}"/network/hgx_h100_*.yml; do
        [ ! -f "${net_cfg}" ] && continue
        cfg_name=$(basename "${net_cfg}" .yml)
        # Extract NPU count from YAML
        npus_from_cfg=$(python3 -c "
import yaml
with open('${net_cfg}') as f:
    d = yaml.safe_load(f)
if 'npus_count' in d:
    print(d['npus_count'][0] if isinstance(d['npus_count'], list) else d['npus_count'])
" 2>/dev/null || echo "")
        if [ -n "${npus_from_cfg}" ] && [ "${npus_from_cfg}" != "None" ]; then
            sys_cfg="${INPUTS_DIR}/system/Ring_AllReduce.json"
            [ ! -f "${sys_cfg}" ] && sys_cfg="${SYSTEM_H100}"
            run_sim ${npus_from_cfg} "${sys_cfg}" "${net_cfg}" "${cfg_name}"
        fi
    done
fi

# Microbenchmark validation runs
echo ""
echo "=== Microbenchmark Validation ==="
for npus in 4 8; do
    WORKLOAD="${EXAMPLE_DIR}/workload/microbenchmarks/all_reduce/${npus}npus_1MB/all_reduce"
    if [ -f "${WORKLOAD}.0.et" ] || [ -f "${WORKLOAD}.et" ]; then
        OUTFILE="${RESULTS_DIR}/microbench_all_reduce_${npus}npus_1MB.log"
        echo ">>> Running: all_reduce microbenchmark ${npus} NPUs 1MB"
        "${ASTRA_SIM_BIN}" \
            --workload-configuration="${WORKLOAD}" \
            --system-configuration="${SYSTEM_H100}" \
            --network-configuration="${NETWORK_H100}" \
            --remote-memory-configuration="${REMOTE_MEMORY}" 2>&1 | tee "${OUTFILE}"
        echo "<<< Saved: ${OUTFILE}"
        echo ""
    fi
done

echo ""
echo "========================================="
echo "=== ALL SIMULATIONS COMPLETE ==="
echo "========================================="
echo ""
ls -la "${RESULTS_DIR}/"
echo ""
echo "=== KEY METRICS ==="
for f in "${RESULTS_DIR}"/*.log; do
    [ ! -f "$f" ] && continue
    echo ""
    echo "--- $(basename $f) ---"
    grep -iE "(sys\[|total|time|cycle|latency|exposed|finish|tick)" "$f" | tail -20
done
