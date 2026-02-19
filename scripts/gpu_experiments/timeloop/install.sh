#!/usr/bin/env bash
# Timeloop installation script
# Timeloop targets NPU/accelerator architectures (Eyeriss-like), NOT GPU compute.
# No GPU required for Timeloop itself, but we include it for completeness
# since our paper evaluates it alongside GPU tools.
set -euo pipefail

echo "=== Timeloop Installation ==="
echo "Note: Timeloop is an accelerator (NPU) modeling tool."
echo "It does NOT require a GPU to run, but is included for paper completeness."
echo ""

# Option 1: Docker (recommended)
echo "=== Option 1: Docker (Recommended) ==="
if command -v docker &>/dev/null; then
    echo "Docker found. Pulling Timeloop image..."
    docker pull timeloopaccelergy/timeloop-accelergy-pytorch:latest || {
        echo "WARNING: Could not pull official image. Building from source..."
    }
    echo ""
    echo "To run via Docker:"
    echo "  docker run --rm -v \$(pwd)/results:/results timeloopaccelergy/timeloop-accelergy-pytorch:latest"
    echo ""
else
    echo "Docker not found. Install Docker or use Option 2."
fi

# Option 2: Install from source
echo "=== Option 2: Install from source ==="
echo "If Docker is not available:"
echo ""
echo "  # Install dependencies"
echo "  sudo apt-get install -y build-essential cmake libboost-all-dev libyaml-cpp-dev"
echo "  pip install timeloop-python accelergy"
echo ""
echo "  # Or build from GitHub:"
echo "  git clone https://github.com/NVlabs/timeloop.git"
echo "  cd timeloop && mkdir build && cd build && cmake .. && make -j\$(nproc)"
echo ""

# Check if Timeloop is already available
if command -v timeloop-mapper &>/dev/null; then
    echo "timeloop-mapper found in PATH:"
    which timeloop-mapper
elif command -v timeloop-model &>/dev/null; then
    echo "timeloop-model found in PATH:"
    which timeloop-model
else
    echo "Timeloop not found in PATH. Use Docker or install from source."
fi

echo ""
echo "=== Installation Notes ==="
echo "Timeloop evaluates accelerator (NPU) energy/performance, not GPU workloads."
echo "Our paper uses it to model ResNet-50 Conv1 on an Eyeriss-like architecture."
echo "For LLM benchmark scenarios, Timeloop has 0% coverage (Table 6 in paper)."
