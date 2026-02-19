#!/usr/bin/env bash
# ASTRA-sim installation script for multi-GPU experiments
# ASTRA-sim is a distributed training simulator that models communication patterns.
# Requires: Docker (recommended) or build from source
set -euo pipefail

echo "=== ASTRA-sim Installation ==="
echo "ASTRA-sim models distributed training communication (AllReduce, AllGather, etc.)"
echo "It uses analytical network models, so GPU hardware is optional for simulation."
echo "However, running on an H100/A100 node validates the HGX topology modeling."
echo ""

# Check for GPU (optional but useful for topology validation)
if command -v nvidia-smi &>/dev/null; then
    echo "GPU detected (optional for ASTRA-sim, useful for topology validation):"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    echo ""
fi

# ============================================================
# Option 1: Docker (recommended)
# ============================================================
echo "=== Option 1: Docker (Recommended) ==="
if command -v docker &>/dev/null; then
    echo "Docker found."
    DOCKERFILE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../benchmarks/astra-sim" && pwd)"

    if [ -f "$DOCKERFILE_DIR/Dockerfile" ]; then
        echo "Building ASTRA-sim Docker image..."
        docker build -t astrasim-benchmarks "$DOCKERFILE_DIR" \
            2>&1 | tail -5
        echo ""
        echo "Docker image built: astrasim-benchmarks"
    else
        echo "Dockerfile not found at $DOCKERFILE_DIR. Building from scratch..."
        docker build -t astrasim-benchmarks -f - /tmp <<'DOCKERFILE'
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential git cmake gcc g++ \
    libboost-dev libboost-program-options-dev \
    openmpi-bin libopenmpi-dev \
    python3 python3-pip autoconf automake libtool pkg-config \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN git clone --depth 1 --branch v3.21.12 https://github.com/protocolbuffers/protobuf.git /tmp/protobuf && \
    cd /tmp/protobuf && git submodule update --init --recursive && \
    mkdir build && cd build && cmake ../cmake -DCMAKE_INSTALL_PREFIX=/usr/local -Dprotobuf_BUILD_TESTS=OFF && \
    make -j$(nproc) && make install && ldconfig && rm -rf /tmp/protobuf
RUN git clone --recurse-submodules https://github.com/astra-sim/astra-sim.git
WORKDIR /app/astra-sim
RUN ./build/astra_analytical/build.sh
RUN pip3 install protobuf pydot pyyaml
DOCKERFILE
    fi
    echo ""
    echo "To run: docker run --rm -v \$(pwd)/results:/results astrasim-benchmarks bash /app/run.sh"
else
    echo "Docker not found. Use Option 2 (build from source)."
fi

# ============================================================
# Option 2: Build from source
# ============================================================
echo ""
echo "=== Option 2: Build from source ==="
echo "Requirements: cmake, g++, protobuf, MPI"
echo ""
echo "  git clone --recurse-submodules https://github.com/astra-sim/astra-sim.git"
echo "  cd astra-sim"
echo "  ./build/astra_analytical/build.sh"
echo ""

echo "=== Installation Complete ==="
echo "Next: Run benchmarks with ./run_benchmarks.sh"
