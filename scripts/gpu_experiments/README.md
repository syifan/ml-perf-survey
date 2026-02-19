# GPU Experiment Scripts

Scripts for running ML performance prediction tool benchmarks on real H100/A100 hardware. These experiments target the 28-scenario LLM benchmark suite defined in our paper.

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | NVIDIA A100 (40GB) | NVIDIA H100 SXM (80GB) |
| CUDA | 12.0+ | 12.2+ |
| RAM | 32 GB | 64 GB |
| Disk | 20 GB free | 50 GB free |
| Docker | 24.0+ | Latest |
| Python | 3.10+ | 3.10 |
| conda | Any | Miniconda3 |

For multi-GPU experiments (ASTRA-sim T3.2): 8+ GPUs with NVLink (HGX-H100 or DGX A100).

## What to Run

Each tool has `install.sh` and `run_benchmarks.sh` scripts. Run them in order:

### 1. NeuSight (GPU kernel latency prediction)
```bash
cd neusight/
./install.sh        # Clones repo, sets up conda env
./run_benchmarks.sh # Runs predictions on H100/A100
```
- **Requires**: NVIDIA GPU with CUDA 12.x, conda
- **Runtime**: ~1 hour
- **Paper scenarios**: I1.1-I1.3 (single-request inference), T1.1/T2.1 (per-GPU kernel time)

### 2. ASTRA-sim (distributed training communication)
```bash
cd astrasim/
./install.sh        # Builds Docker image
./run_benchmarks.sh # Runs collective benchmarks + ResNet-50 scaling
```
- **Requires**: Docker (GPU optional)
- **Runtime**: ~15-20 minutes
- **Paper scenarios**: T1.1-T3.2 (data/tensor/pipeline parallel communication)

### 3. VIDUR (LLM inference serving simulation)
```bash
cd vidur/
./install.sh        # Builds Docker image
./run_benchmarks.sh # Runs serving experiments across schedulers
```
- **Requires**: Docker (GPU optional)
- **Runtime**: ~30-45 minutes
- **Paper scenarios**: I1.1-I3.3 (inference serving with vLLM, Sarathi, Orca)

### 4. Timeloop (accelerator energy/performance)
```bash
cd timeloop/
./install.sh        # Sets up Docker or local Timeloop
./run_benchmarks.sh # Runs Eyeriss-like NPU experiments
```
- **Requires**: Docker (no GPU needed)
- **Runtime**: ~5-10 minutes
- **Paper scenarios**: None (0% LLM coverage; included for paper completeness)

## Run All at Once

```bash
# Run all experiments sequentially
for tool in neusight astrasim vidur timeloop; do
    echo "=== Running $tool ==="
    cd $tool && ./install.sh && ./run_benchmarks.sh && cd ..
done
```

## Paper Benchmark Coverage Summary

| Tool | Supported | Partial | Total | Focus |
|------|-----------|---------|-------|-------|
| NeuSight | 5 | 3 | 8/28 (29%) | GPU kernel latency |
| ASTRA-sim | 7 | 2 | 9/28 (32%) | Training communication |
| VIDUR | 6 | 2 | 8/28 (29%) | Inference serving |
| Timeloop | 0 | 0 | 0/28 (0%) | NPU accelerators |
| **Union** | **14** | **4** | **18/28 (64%)** | |

## How to Send Results Back

After running all experiments, compress results and share:

```bash
# From this directory (scripts/gpu_experiments/)
tar czf gpu_experiment_results.tar.gz \
    neusight/results/ \
    astrasim/results/ \
    vidur/results/ \
    timeloop/results/

# The tar file contains all experiment outputs
# Share it via GitHub issue comment or file upload
```

### What the Results Should Contain

- **NeuSight**: Per-model MAPE across GPU types, DP4/TP4/PP4 comparison, fusion analysis
- **ASTRA-sim**: Collective latencies (AllReduce, AllGather, etc.), ResNet-50 scaling
- **VIDUR**: Per-request TTFT/TPOT, scheduler comparison (vLLM vs Sarathi), preemption counts
- **Timeloop**: Energy breakdown, utilization metrics

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `nvidia-smi` not found | Install NVIDIA driver: `sudo apt install nvidia-driver-535` |
| CUDA version mismatch | NeuSight needs CUDA 12.x; check with `nvcc --version` |
| Docker permission denied | Add user to docker group: `sudo usermod -aG docker $USER` |
| conda not found | Install Miniconda: `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh` |
| Out of GPU memory | Reduce batch sizes in NeuSight benchmarks |
| VIDUR model not found | Check if `meta-llama/Llama-2-7b-hf` is accessible (may need HF token) |
