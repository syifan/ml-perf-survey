#!/usr/bin/env bash
# NeuSight installation script for GPU hardware (H100/A100)
# Requires: NVIDIA GPU with CUDA 12.x, Python 3.10+, conda
set -euo pipefail

echo "=== NeuSight GPU Installation ==="
echo "Hardware: Requires NVIDIA GPU (H100/A100) with CUDA 12.x"
echo ""

# Check for NVIDIA GPU
if ! command -v nvidia-smi &>/dev/null; then
    echo "ERROR: nvidia-smi not found. NVIDIA GPU driver required."
    exit 1
fi
echo "GPU detected:"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo ""

# Check CUDA version
CUDA_VER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -1)
echo "NVIDIA Driver: $CUDA_VER"

# Clone NeuSight
NEUSIGHT_DIR="${NEUSIGHT_DIR:-/tmp/NeuSight}"
if [ -d "$NEUSIGHT_DIR" ]; then
    echo "NeuSight already cloned at $NEUSIGHT_DIR"
else
    echo "Cloning NeuSight..."
    git clone --depth 1 https://github.com/sitar-lab/NeuSight.git "$NEUSIGHT_DIR"
fi

# Create conda environment
echo ""
echo "Setting up conda environment..."
if conda env list | grep -q "neusight"; then
    echo "Conda env 'neusight' already exists"
else
    conda create -n neusight python=3.10 -y
fi

echo ""
echo "Installing NeuSight dependencies..."
eval "$(conda shell.bash hook)"
conda activate neusight

cd "$NEUSIGHT_DIR"
pip install -r requirements.txt 2>/dev/null || {
    # Fallback: install known dependencies
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
    pip install numpy pandas scipy scikit-learn onnx onnxruntime
}

echo ""
echo "=== Installation Complete ==="
echo "NeuSight directory: $NEUSIGHT_DIR"
echo "Conda environment: neusight"
echo ""
echo "Next: Run benchmarks with ./run_benchmarks.sh"
