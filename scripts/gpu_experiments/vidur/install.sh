#!/usr/bin/env bash
# VIDUR installation script for GPU-based LLM inference serving experiments
# VIDUR simulates LLM serving systems (vLLM, Sarathi, Orca schedulers)
# Requires: Docker (recommended) or Python 3.10+
set -euo pipefail

echo "=== VIDUR Installation ==="
echo "VIDUR simulates LLM inference serving with scheduling policies."
echo "It models prefill/decode phases, KV cache management, and preemption."
echo ""

# Check for GPU (optional - VIDUR is a simulator)
if command -v nvidia-smi &>/dev/null; then
    echo "GPU detected (optional for VIDUR, useful for validation):"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    echo ""
fi

# ============================================================
# Option 1: Docker (recommended)
# ============================================================
echo "=== Option 1: Docker (Recommended) ==="
if command -v docker &>/dev/null; then
    echo "Docker found."
    DOCKERFILE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../benchmarks/vidur" && pwd)"

    if [ -f "$DOCKERFILE_DIR/Dockerfile" ]; then
        echo "Building VIDUR Docker image..."
        docker build -t vidur-benchmarks "$DOCKERFILE_DIR" \
            2>&1 | tail -5
        echo "Docker image built: vidur-benchmarks"
    else
        echo "Building VIDUR Docker image from scratch..."
        docker build -t vidur-benchmarks -f - /tmp <<'DOCKERFILE'
FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/microsoft/vidur.git /app
RUN pip install --no-cache-dir numpy pandas scikit-learn plotly_express matplotlib seaborn fasteners ddsketch randomname pyyaml wandb
ENV WANDB_MODE=disabled
ENTRYPOINT ["python", "-m", "vidur.main"]
DOCKERFILE
    fi
    echo ""
else
    echo "Docker not found. Use Option 2."
fi

# ============================================================
# Option 2: Local Python installation
# ============================================================
echo ""
echo "=== Option 2: Local Python Installation ==="
echo "  git clone https://github.com/microsoft/vidur.git"
echo "  cd vidur"
echo "  pip install -r requirements.txt"
echo "  # Or: pip install numpy pandas scikit-learn plotly_express matplotlib seaborn fasteners ddsketch randomname pyyaml"
echo ""

echo "=== Installation Complete ==="
echo "Next: Run benchmarks with ./run_benchmarks.sh"
