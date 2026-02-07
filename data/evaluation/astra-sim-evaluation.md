# ASTRA-sim Reproducibility Evaluation

This document assesses ASTRA-sim's reproducibility, usability, and practical considerations for distributed ML training simulation research.

---

## Overview

**Tool:** ASTRA-sim
**Paper:** ASTRA-sim: Enabling SW/HW Co-Design Exploration for Distributed DL Training Platforms (ISPASS 2020)
**Authors:** Won et al. (Georgia Tech, Meta, Intel, AMD)
**Repository:** https://github.com/astra-sim/astra-sim
**License:** MIT
**Evaluation Date:** 2026-02-07

---

## Setup Assessment

### Installation Options

| Method | Complexity | Time to First Result | Recommended For |
|--------|------------|---------------------|-----------------|
| Docker | Moderate | ~20-30 minutes | New users, reproducibility |
| Native (Linux) | High | 1-2 hours | Development, advanced use |
| Native (macOS) | Not Supported | N/A | Use Docker |

### Docker Setup (Recommended)

**Dockerfile provided:** Yes, with Ubuntu 22.04 base

**Key Dependencies Installed:**
- gcc, g++, clang-format
- CMake, make
- Boost libraries
- OpenMPI
- Python 3.11 with venv
- Protobuf (compiled from source for compatibility)
- Abseil (for Protobuf)

**Notes:**
- Docker image includes all dependencies pre-configured
- Protobuf compiled from source for proper CMake integration
- Environment variable `PROTOBUF_FROM_SOURCE=True` enables advanced CMake features

### Native Installation (Linux Only)

**Required Dependencies:**
1. Build tools: gcc, g++, cmake (>= 3.22), make
2. Libraries: libboost-dev, libboost-program-options-dev
3. OpenMPI: openmpi-bin, openmpi-doc, libopenmpi-dev
4. Protobuf: protoc (for Chakra trace compilation)
5. Python packages: numpy, sympy, graphviz, pandas

**Build Process:**
```bash
cd astra-sim
./build/astra_analytical/build.sh
```

**Build Targets:**
- `all` (default): Both congestion-aware and unaware
- `congestion_unaware`: Faster, simpler model
- `congestion_aware`: More accurate, includes network congestion

---

## Repository Structure

```
astra-sim/
├── astra-sim/           # Core simulator source (C++)
│   ├── system/          # System layer (scheduling, collectives)
│   ├── workload/        # Workload handling (Chakra traces)
│   └── common/          # Shared utilities
├── build/
│   └── astra_analytical/  # Analytical backend build scripts
├── examples/
│   ├── workload/        # Microbenchmark Chakra traces
│   │   └── microbenchmarks/
│   │       ├── all_reduce/    # 4, 8, 16 NPU configs
│   │       ├── all_gather/
│   │       ├── reduce_scatter/
│   │       └── all_to_all/
│   ├── system/          # System configuration examples
│   │   ├── native_collectives/   # Built-in algorithms
│   │   └── custom_collectives/   # User-defined
│   ├── network/         # Network topology configs
│   │   └── analytical/  # HGX-H100, DGX-V100, TPU-v3
│   └── run_scripts/     # Example execution scripts
├── inputs/
│   ├── network/         # Pre-defined network configs
│   │   ├── hgx_h100_*.yml    # 2, 4, 8, 16, 32 GPU
│   │   ├── dgx_v100_*.yml    # 4, 8 GPU
│   │   └── tpu_v3_*.yml      # Ring and 2D torus
│   └── system/          # System layer configs
├── extern/
│   ├── graph_frontend/chakra/   # Chakra trace format
│   ├── network_backend/         # Network simulators
│   │   ├── analytical/          # Fast analytical model
│   │   ├── ns-3/                # Detailed NS-3
│   │   └── csg-htsim/           # HTSim backend
│   └── remote_memory_backend/   # Memory expansion
└── tests/               # Regression tests
```

---

## Pre-defined Configurations

### Network Topologies

| Configuration | NPUs | Topology | Bandwidth | Latency |
|--------------|------|----------|-----------|---------|
| HGX-H100 8GPU | 8 | Switch | 400 GB/s | 936.25 ns |
| HGX-H100 16GPU | 16 | Switch | 400 GB/s | - |
| HGX-H100 32GPU | 32 | Switch | 400 GB/s | - |
| DGX-V100 8GPU | 8 | - | - | - |
| TPU-v3 32 Ring | 32 | Ring | - | - |
| TPU-v3 32 2D Torus | 32 | 2D Torus | - | - |

### Collective Implementations

System configuration supports:
- `all-reduce-implementation`: ring, tree, etc.
- `all-gather-implementation`: ring, etc.
- `reduce-scatter-implementation`: ring, etc.
- `all-to-all-implementation`: ring, etc.
- `collective-optimization`: localBWAware, etc.

### Example Configuration (HGX-H100 Validated)

**System Config:**
```json
{
    "scheduling-policy": "LIFO",
    "endpoint-delay": 10,
    "active-chunks-per-dimension": 2,
    "preferred-dataset-splits": 4,
    "all-reduce-implementation": ["ring"],
    "collective-optimization": "localBWAware",
    "local-mem-bw": 3350
}
```

**Network Config:**
```yaml
topology: [ Switch ]
npus_count: [ 8 ]
bandwidth: [ 400.0 ]  # GB/s
latency: [ 936.25 ]   # ns
```

---

## Workload Input Format

ASTRA-sim uses **Chakra Execution Traces** (ET) for workload specification.

### Microbenchmark Examples

Pre-included 1MB collective operation traces:
- `all_reduce/{4,8,16}npus_1MB/`
- `all_gather/{4,8,16}npus_1MB/`
- `reduce_scatter/{4,8,16}npus_1MB/`
- `all_to_all/{4,8,16}npus_1MB/`

Each configuration includes per-NPU trace files (e.g., `all_reduce.0.et` through `all_reduce.7.et` for 8 NPUs).

### Generating Custom Workloads

For realistic workloads (compute + communication):
1. Use [STG (Symbolic Tensor Graph)](https://github.com/astra-sim/symbolic_tensor_graph) for synthetic generation
2. Use Chakra for collecting traces from real systems

---

## Running Simulations

### Basic Execution

```bash
# Run example with analytical network backend
./examples/run_scripts/analytical/congestion_aware/HGX-H100-validated.sh
```

### Command Line Interface

```bash
./AstraSim_Analytical_Congestion_Aware \
    --workload-configuration=<path-to-chakra-traces> \
    --system-configuration=<system-config.json> \
    --network-configuration=<network-config.yml> \
    --remote-memory-configuration=<memory-config.json>
```

---

## Network Backends

| Backend | Fidelity | Speed | Use Case |
|---------|----------|-------|----------|
| Analytical | Low-Medium | Very Fast | Design exploration |
| NS-3 | High | Slow | Accurate validation |
| HTSim | High | Medium | Large-scale systems |

The analytical backend is recommended for most use cases due to speed advantages.

---

## Accuracy Claims vs. Reality

### Published Claims

- 5-15% error vs. real hardware measurements
- Validated against HGX-H100 and HPE ProLiant systems
- TPU-v3 validation available

### Evaluation Observations

1. **Validated configurations provided:** HGX-H100-validated examples included
2. **Multiple network backends:** Can trade accuracy for speed
3. **Industry backing:** Meta, Intel, AMD involvement suggests production use

### Limitations Noted

1. **Chakra trace dependency:** Requires trace generation infrastructure
2. **Linux only:** macOS/Windows require Docker
3. **Protobuf version sensitivity:** Dockerfile compiles from source for compatibility

---

## Usability Assessment

### Strengths

| Aspect | Rating | Notes |
|--------|--------|-------|
| Documentation | Good | Wiki, tutorials available |
| Example coverage | Excellent | Multiple HW configs, collectives |
| Network flexibility | Excellent | 3 backend options |
| HW coverage | Excellent | H100, V100, TPU-v3 |
| Community | Active | Georgia Tech, industry partners |

### Challenges

| Aspect | Rating | Notes |
|--------|--------|-------|
| Installation | Moderate | Docker recommended |
| Workload generation | Moderate | Chakra trace format learning curve |
| macOS/Windows support | Poor | Docker only |
| Build complexity | High | Multiple submodules, Protobuf |

---

## Reproducibility Checklist

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Source code available | Yes | Full C++ source |
| Build instructions | Yes | Makefile, CMake |
| Dependencies documented | Yes | Dockerfile shows all |
| Pre-built containers | Partial | Dockerfile provided, no pre-built image |
| Example inputs | Yes | Microbenchmarks, network configs |
| Reference outputs | Partial | Validated configs, no reference numbers |
| Test suite | Yes | Regression tests included |

**Reproducibility Score: 8/10**

---

## Practical Recommendations

### For Researchers

1. **Use Docker** - Avoids dependency issues, especially Protobuf
2. **Start with analytical backend** - Fast iteration on design ideas
3. **Use validated configs** - HGX-H100 provides known-good baseline
4. **Learn Chakra format** - Essential for custom workloads

### For Practitioners

1. **Capacity planning** - Simulate before hardware purchase
2. **Scaling studies** - Test 2/4/8/16/32 GPU configurations
3. **Collective algorithm selection** - Compare ring vs. tree vs. custom
4. **Network topology optimization** - Test ring, switch, 2D torus

### Known Limitations

1. **No GPU modeling** - Pure simulation, no actual GPU execution
2. **Trace-based only** - Requires upfront workload characterization
3. **Linux-focused** - Cross-platform requires Docker
4. **Build complexity** - Many submodules and dependencies

---

## Comparison with Alternatives

| Tool | Focus | Fidelity | Speed |
|------|-------|----------|-------|
| **ASTRA-sim** | Distributed training | Medium-High | Fast |
| Timeloop | Single accelerator | High | Fast |
| GPGPU-Sim | GPU kernels | Very High | Very Slow |
| SimAI | Distributed inference | Medium | Fast |

---

## Conclusion

**ASTRA-sim is a capable tool for distributed ML training simulation with good reproducibility.**

Key findings:
- Docker provides reliable, reproducible setup
- Validated configurations for major GPU systems
- Flexible network backend options
- Active development and industry backing

Recommended for:
- Distributed training research
- HW/SW co-design exploration
- Network topology optimization
- Collective algorithm development

Not recommended for:
- Single-GPU workload modeling (use Timeloop)
- Real-time profiling (simulation only)
- Windows/macOS without Docker

---

*Evaluation by Leo | ML Performance Survey Project*
