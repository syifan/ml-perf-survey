# Timeloop Accelerator Experiments

## What This Does

Runs Timeloop energy/performance modeling on an Eyeriss-like NPU architecture, reproducing paper Section 4.5 findings.

**Important**: Timeloop is an accelerator (NPU) design-space exploration tool. It does **not** model GPU workloads and has **0% LLM benchmark suite coverage** (paper Table 6). It is included for paper completeness only.

## Paper Scenarios

Timeloop has 0 supported and 0 partial LLM scenarios (0% coverage). Its evaluation in our paper focuses on:

- ResNet-50 Conv1 on Eyeriss-like architecture (168 PEs, 16-bit)
- Energy breakdown by memory hierarchy (DRAM > GLB > PE scratchpads)
- Comparison against published Eyeriss silicon data

## Hardware Requirements

- **GPU**: Not required (Timeloop models NPU accelerators)
- **Docker**: Recommended (for Timeloop binary)
- **RAM**: 8GB+
- **Disk**: 5GB free

## How to Run

```bash
# 1. Install (Docker or local)
./install.sh

# 2. Run benchmarks
./run_benchmarks.sh
```

The script will try Docker first, fall back to local installation, and finally run analytical estimates if neither is available.

## Expected Runtime

- Timeloop mapper search: ~5-10 minutes
- Analytical estimates only: <1 minute

## Expected Outputs

- `resnet50_conv1_results.json` — Cycles, energy, utilization
- Energy breakdown: DRAM accesses dominate (~70-80% of total energy)
- Utilization: ~50-75% (Conv1 is limited by C=3 input channels)

## Sending Results Back

```bash
tar czf timeloop_results.tar.gz results/
```
