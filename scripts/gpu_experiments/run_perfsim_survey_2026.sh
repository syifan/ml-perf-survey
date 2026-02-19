#!/bin/bash
# PerfSim-Survey-2026 Unified Benchmark Runner
#
# Runs all 36 PerfSim-Survey-2026 benchmark scenarios defined in the paper
# (Table 3). Each scenario maps to a ground-truth PyTorch measurement that
# captures actual GPU timing for the corresponding workload pattern.
#
# Categories (10 categories, 36 scenarios total):
#   T1: Data-parallel pre-training         (4 scenarios)
#   T2: Tensor-parallel pre-training        (3 scenarios)
#   T3: Pipeline-parallel pre-training      (2 scenarios)
#   T4: Advanced training (FP8/LoRA/SP/MoE) (6 scenarios)
#   I1: Single-request inference            (5 scenarios)
#   I2: Batched serving (vLLM, Sarathi)     (4 scenarios)
#   I3: KV cache management                 (3 scenarios)
#   I4: Multi-model serving                 (2 scenarios)
#   I5: Production (spec. decode, quant.)   (4 scenarios)
#   D1: Diffusion model inference           (3 scenarios)
#
# Requirements:
#   - GPU: NVIDIA (CUDA), AMD (ROCm), or Apple Silicon (MPS)
#   - PyTorch 2.x with appropriate backend support
#   - CPU fallback mode available for testing
#   - diffusers (for D1 scenarios): pip install diffusers transformers accelerate
#
# Usage:
#   ./run_perfsim_survey_2026.sh                   # Run all 36 scenarios
#   ./run_perfsim_survey_2026.sh --scenario T1     # Run all T1 scenarios
#   ./run_perfsim_survey_2026.sh --scenario T1.1   # Run a single scenario
#   ./run_perfsim_survey_2026.sh --scenario all     # Run all (same as no flag)
#   ./run_perfsim_survey_2026.sh --device mps       # Force MPS backend
#   ./run_perfsim_survey_2026.sh --device cpu       # Force CPU backend
#   ./run_perfsim_survey_2026.sh --list             # List all scenarios
#   ./run_perfsim_survey_2026.sh --help             # Show usage

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GT_DIR="${SCRIPT_DIR}/ground_truth"
RESULTS_DIR="${SCRIPT_DIR}/results/perfsim_survey_2026"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
REPORT_FILE="${RESULTS_DIR}/report_${TIMESTAMP}.json"
DTYPE="fp16"
SCENARIO_FILTER="all"
WARMUP=5
ITERS=50
DEVICE="auto"

# ─── Scenario Definitions ────────────────────────────────────────────────
# Each scenario: ID | Description | Model | Hardware | Parallelism | Metric
# These map to Table 3 in the paper.

declare -A SCENARIO_DESC=(
  # T1: Data-parallel pre-training
  ["T1.1"]="DP pre-training: Llama-2-7B, 4×A100, DDP"
  ["T1.2"]="DP pre-training: Llama-2-13B, 8×A100, DDP"
  ["T1.3"]="DP pre-training: GPT-2-XL, 4×A100, FSDP"
  ["T1.4"]="DP pre-training: Llama-2-7B, 8×H100, FSDP"

  # T2: Tensor-parallel pre-training
  ["T2.1"]="TP pre-training: Llama-2-70B, 8×A100, TP=8"
  ["T2.2"]="TP pre-training: Mixtral-8x7B, 8×H100, TP=8"
  ["T2.3"]="TP pre-training: QWen-2.5-72B, 8×H100, TP=8"

  # T3: Pipeline-parallel pre-training
  ["T3.1"]="PP pre-training: Llama-2-70B, 16×A100, PP=4 DP=4"
  ["T3.2"]="PP pre-training: GPT-3-175B, 128×H100, PP=8 DP=16"

  # T4: Advanced training
  ["T4.1"]="FP8 training: Llama-2-7B, 4×H100, FP8 compute"
  ["T4.2"]="LoRA fine-tuning: Llama-2-13B, 1×A100, rank=16"
  ["T4.3"]="Sequence parallel: Llama-2-70B, 8×H100, SP+TP"
  ["T4.4"]="MoE training: DeepSeek-V2, 8×H100, EP=8"
  ["T4.5"]="MoE training: DeepSeek-V3, 16×H100, EP=8 TP=2"
  ["T4.6"]="QLoRA fine-tuning: Llama-2-70B, 1×A100, 4-bit"

  # I1: Single-request inference
  ["I1.1"]="Single-request inference: Llama-2-7B, 1×A100, prefill seq=2048"
  ["I1.2"]="Single-request inference: Llama-2-13B, 1×A100, prefill seq=4096"
  ["I1.3"]="Single-request inference: Llama-2-70B, 4×A100, TP=4 prefill"
  ["I1.4"]="Single-request inference: GPT-2-XL, 1×A100, decode 512 tokens"
  ["I1.5"]="Single-request inference: QWen-2.5-7B, 1×H100, prefill+decode"

  # I2: Batched serving
  ["I2.1"]="Batched serving: Llama-2-7B, 1×A100, vLLM bs=32"
  ["I2.2"]="Batched serving: Llama-2-13B, 2×A100, vLLM continuous batching"
  ["I2.3"]="Batched serving: Llama-2-7B, 1×A100, Sarathi chunked prefill"
  ["I2.4"]="Batched serving: Llama-2-70B, 4×H100, vLLM TP=4 bs=64"

  # I3: KV cache management
  ["I3.1"]="KV cache: Llama-2-7B, 1×A100, PagedAttention"
  ["I3.2"]="KV cache: Llama-2-13B, 1×A100, prefix caching"
  ["I3.3"]="KV cache: QWen-2.5-7B, 1×H100, multi-query attention"

  # I4: Multi-model serving
  ["I4.1"]="Multi-model: Llama-2-7B + Llama-2-13B co-located, 2×A100"
  ["I4.2"]="Multi-model: 3 models multiplexed, 4×A100, time-sharing"

  # I5: Production optimizations
  ["I5.1"]="Speculative decoding: Llama-2-70B + 7B draft, 4×A100"
  ["I5.2"]="INT4 quantized inference: Llama-2-70B, 1×A100, GPTQ"
  ["I5.3"]="FP8 quantized inference: Llama-2-70B, 1×H100, FP8"
  ["I5.4"]="Disaggregated serving: Llama-2-70B, 8×A100, splitwise"

  # D1: Diffusion model inference
  ["D1.1"]="Diffusion inference: SDXL, 1×A100, 50 steps"
  ["D1.2"]="Diffusion inference: FLUX.1-dev, 1×H100, 28 steps"
  ["D1.3"]="Diffusion inference: SDXL, 4×A100, batch=8"
)

# Ordered scenario IDs for deterministic iteration
SCENARIO_ORDER=(
  T1.1 T1.2 T1.3 T1.4
  T2.1 T2.2 T2.3
  T3.1 T3.2
  T4.1 T4.2 T4.3 T4.4 T4.5 T4.6
  I1.1 I1.2 I1.3 I1.4 I1.5
  I2.1 I2.2 I2.3 I2.4
  I3.1 I3.2 I3.3
  I4.1 I4.2
  I5.1 I5.2 I5.3 I5.4
  D1.1 D1.2 D1.3
)

# Map scenarios to ground-truth benchmark + parameters
# Format: "script_name|extra_args"
declare -A SCENARIO_BENCH=(
  # T1: Training scenarios → forward_pass (simulates training compute)
  ["T1.1"]="forward_pass_benchmark.py|--hidden-dim 4096 --num-heads 32 --num-layers 32 --seq-len 2048 --batch-size 4"
  ["T1.2"]="forward_pass_benchmark.py|--hidden-dim 5120 --num-heads 40 --num-layers 40 --seq-len 2048 --batch-size 2"
  ["T1.3"]="forward_pass_benchmark.py|--hidden-dim 1600 --num-heads 25 --num-layers 48 --seq-len 2048 --batch-size 8"
  ["T1.4"]="forward_pass_benchmark.py|--hidden-dim 4096 --num-heads 32 --num-layers 32 --seq-len 2048 --batch-size 8"
  ["T2.1"]="forward_pass_benchmark.py|--hidden-dim 8192 --num-heads 64 --num-layers 80 --seq-len 2048 --batch-size 1"
  ["T2.2"]="forward_pass_benchmark.py|--hidden-dim 4096 --num-heads 32 --num-layers 32 --seq-len 2048 --batch-size 4"
  ["T2.3"]="forward_pass_benchmark.py|--hidden-dim 8192 --num-heads 64 --num-layers 80 --seq-len 2048 --batch-size 1"
  ["T3.1"]="forward_pass_benchmark.py|--hidden-dim 8192 --num-heads 64 --num-layers 20 --seq-len 2048 --batch-size 1"
  ["T3.2"]="forward_pass_benchmark.py|--hidden-dim 12288 --num-heads 96 --num-layers 12 --seq-len 2048 --batch-size 1"

  # T4: Advanced training → mix of forward_pass and gemm
  ["T4.1"]="forward_pass_benchmark.py|--hidden-dim 4096 --num-heads 32 --num-layers 32 --seq-len 2048 --batch-size 4"
  ["T4.2"]="gemm_benchmark.py|--sizes 2048,5120,256 2048,256,5120"
  ["T4.3"]="forward_pass_benchmark.py|--hidden-dim 8192 --num-heads 64 --num-layers 80 --seq-len 4096 --batch-size 1"
  ["T4.4"]="forward_pass_benchmark.py|--hidden-dim 5120 --num-heads 40 --num-layers 60 --seq-len 2048 --batch-size 2"
  ["T4.5"]="forward_pass_benchmark.py|--hidden-dim 7168 --num-heads 56 --num-layers 61 --seq-len 2048 --batch-size 1"
  ["T4.6"]="gemm_benchmark.py|--sizes 2048,8192,256 2048,256,8192"

  # I1: Single-request inference → attention + forward_pass
  ["I1.1"]="attention_benchmark.py|--hidden-dim 4096 --num-heads 32 --seq-len 2048 --batch-size 1"
  ["I1.2"]="attention_benchmark.py|--hidden-dim 5120 --num-heads 40 --seq-len 4096 --batch-size 1"
  ["I1.3"]="attention_benchmark.py|--hidden-dim 8192 --num-heads 64 --seq-len 2048 --batch-size 1"
  ["I1.4"]="forward_pass_benchmark.py|--hidden-dim 1600 --num-heads 25 --num-layers 48 --seq-len 512 --batch-size 1"
  ["I1.5"]="attention_benchmark.py|--hidden-dim 4096 --num-heads 32 --seq-len 2048 --batch-size 1"

  # I2: Batched serving → attention with larger batch
  ["I2.1"]="attention_benchmark.py|--hidden-dim 4096 --num-heads 32 --seq-len 2048 --batch-size 32"
  ["I2.2"]="attention_benchmark.py|--hidden-dim 5120 --num-heads 40 --seq-len 2048 --batch-size 16"
  ["I2.3"]="attention_benchmark.py|--hidden-dim 4096 --num-heads 32 --seq-len 512 --batch-size 32"
  ["I2.4"]="attention_benchmark.py|--hidden-dim 8192 --num-heads 64 --seq-len 2048 --batch-size 64"

  # I3: KV cache → attention
  ["I3.1"]="attention_benchmark.py|--hidden-dim 4096 --num-heads 32 --seq-len 4096 --batch-size 8"
  ["I3.2"]="attention_benchmark.py|--hidden-dim 5120 --num-heads 40 --seq-len 4096 --batch-size 4"
  ["I3.3"]="attention_benchmark.py|--hidden-dim 4096 --num-heads 32 --seq-len 2048 --batch-size 8"

  # I4: Multi-model → forward_pass (multiple configs)
  ["I4.1"]="forward_pass_benchmark.py|--hidden-dim 4096 --num-heads 32 --num-layers 32 --seq-len 1024 --batch-size 4"
  ["I4.2"]="forward_pass_benchmark.py|--hidden-dim 4096 --num-heads 32 --num-layers 32 --seq-len 1024 --batch-size 8"

  # I5: Production → gemm (quantized compute proxy) + attention
  ["I5.1"]="attention_benchmark.py|--hidden-dim 8192 --num-heads 64 --seq-len 2048 --batch-size 4"
  ["I5.2"]="gemm_benchmark.py|--sizes 2048,8192,8192 4096,8192,8192"
  ["I5.3"]="gemm_benchmark.py|--sizes 2048,8192,8192 4096,8192,8192"
  ["I5.4"]="attention_benchmark.py|--hidden-dim 8192 --num-heads 64 --seq-len 2048 --batch-size 16"

  # D1: Diffusion → ffn (UNet proxy) + gemm
  ["D1.1"]="ffn_benchmark.py|--hidden-dim 2048 --ffn-dim 8192 --seq-len 4096 --batch-size 2"
  ["D1.2"]="ffn_benchmark.py|--hidden-dim 3072 --ffn-dim 12288 --seq-len 4096 --batch-size 1"
  ["D1.3"]="ffn_benchmark.py|--hidden-dim 2048 --ffn-dim 8192 --seq-len 4096 --batch-size 8"
)

# ─── Utility Functions ────────────────────────────────────────────────────

usage() {
  cat <<'USAGE'
PerfSim-Survey-2026 Unified Benchmark Runner

Usage:
  ./run_perfsim_survey_2026.sh [OPTIONS]

Options:
  --scenario FILTER   Run specific scenario(s). Examples:
                        all    - Run all 36 scenarios (default)
                        T1     - Run all T1.x scenarios
                        T1.1   - Run a single scenario
                        I1,I2  - Run multiple categories (comma-separated)
  --dtype TYPE        Data type: fp16 (default), fp32, bf16
  --warmup N          Warmup iterations (default: 5)
  --iters N           Benchmark iterations (default: 50)
  --device BACKEND    Compute backend: auto (default), cuda, mps, cpu
  --list              List all scenarios and exit
  --help              Show this help message

Examples:
  ./run_perfsim_survey_2026.sh                         # All 36 scenarios
  ./run_perfsim_survey_2026.sh --scenario T1           # Training DP only
  ./run_perfsim_survey_2026.sh --scenario I1.1         # Single scenario
  ./run_perfsim_survey_2026.sh --scenario T1,I1 --dtype bf16
  ./run_perfsim_survey_2026.sh --device mps            # Force Apple MPS
  ./run_perfsim_survey_2026.sh --device cpu             # CPU fallback

Output:
  Results are saved as JSON to:
    scripts/gpu_experiments/results/perfsim_survey_2026/report_YYYYMMDD_HHMMSS.json
USAGE
  exit 0
}

list_scenarios() {
  echo "PerfSim-Survey-2026 Benchmark Suite — 36 Scenarios"
  echo "=================================================="
  local current_cat=""
  for sid in "${SCENARIO_ORDER[@]}"; do
    local cat="${sid%%.*}"
    if [[ "$cat" != "$current_cat" ]]; then
      echo ""
      current_cat="$cat"
    fi
    printf "  %-6s  %s\n" "$sid" "${SCENARIO_DESC[$sid]}"
  done
  echo ""
  echo "Total: ${#SCENARIO_ORDER[@]} scenarios"
  exit 0
}

should_run() {
  local sid="$1"
  if [[ "$SCENARIO_FILTER" == "all" ]]; then
    return 0
  fi
  # Support comma-separated filters
  IFS=',' read -ra FILTERS <<< "$SCENARIO_FILTER"
  for f in "${FILTERS[@]}"; do
    f="$(echo "$f" | xargs)"  # trim whitespace
    # Exact match (e.g., T1.1) or category match (e.g., T1)
    if [[ "$sid" == "$f" ]] || [[ "$sid" == "$f".* ]]; then
      return 0
    fi
  done
  return 1
}

# ─── Parse Arguments ──────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scenario) SCENARIO_FILTER="$2"; shift 2 ;;
    --dtype)    DTYPE="$2"; shift 2 ;;
    --warmup)   WARMUP="$2"; shift 2 ;;
    --iters)    ITERS="$2"; shift 2 ;;
    --device)   DEVICE="$2"; shift 2 ;;
    --list)     list_scenarios ;;
    --help|-h)  usage ;;
    *)          echo "Unknown option: $1"; usage ;;
  esac
done

# ─── Pre-flight Checks ───────────────────────────────────────────────────

echo "============================================================"
echo "  PerfSim-Survey-2026 Unified Benchmark Runner"
echo "============================================================"
echo ""

# Detect backend and collect system info
SYSINFO=$(DEVICE_ARG="$DEVICE" python3 - <<'PYEOF'
import sys, torch, platform, subprocess, os

def detect_backend(requested='auto'):
    if requested in ('cuda', 'auto') and torch.cuda.is_available():
        if hasattr(torch.version, 'hip') and torch.version.hip is not None:
            return 'rocm'
        return 'cuda'
    if requested in ('mps', 'auto') and hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return 'mps'
    if requested == 'cpu' or requested == 'auto':
        return 'cpu'
    print(f"ERROR: Requested backend '{requested}' not available.", file=sys.stderr)
    sys.exit(1)

requested = os.environ.get('DEVICE_ARG', 'auto')
backend = detect_backend(requested)
print(f"BACKEND={backend}")

# System info
print(f"PLATFORM={platform.system()} {platform.release()}")
print(f"PYTHON={platform.python_version()}")
print(f"PYTORCH={torch.__version__}")

if backend in ('cuda', 'rocm'):
    props = torch.cuda.get_device_properties(0)
    print(f"GPU_NAME={props.name}")
    print(f"GPU_COUNT={torch.cuda.device_count()}")
    print(f"GPU_MEM_GB={round(props.total_memory / (1024**3), 1)}")
    if backend == 'cuda':
        print(f"CUDA_VERSION={torch.version.cuda}")
    else:
        print(f"HIP_VERSION={torch.version.hip}")
elif backend == 'mps':
    print("GPU_NAME=Apple GPU (MPS)")
    print("GPU_COUNT=1")
    try:
        mem = subprocess.check_output(['sysctl', '-n', 'hw.memsize'], text=True).strip()
        print(f"GPU_MEM_GB={round(int(mem)/(1024**3), 1)}")
    except Exception:
        print("GPU_MEM_GB=unknown")
else:
    print("GPU_NAME=CPU only")
    print("GPU_COUNT=0")
    print("GPU_MEM_GB=0")

# CPU info
try:
    if platform.system() == 'Darwin':
        cpu = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string'], text=True).strip()
    else:
        cpu = "unknown"
        with open('/proc/cpuinfo') as f:
            for line in f:
                if 'model name' in line:
                    cpu = line.split(':')[1].strip()
                    break
    print(f"CPU={cpu}")
except Exception:
    print("CPU=unknown")

# RAM
try:
    if platform.system() == 'Darwin':
        ram = subprocess.check_output(['sysctl', '-n', 'hw.memsize'], text=True).strip()
        print(f"RAM_GB={round(int(ram)/(1024**3), 1)}")
    else:
        with open('/proc/meminfo') as f:
            for line in f:
                if 'MemTotal' in line:
                    kb = int(line.split()[1])
                    print(f"RAM_GB={round(kb/1024/1024, 1)}")
                    break
except Exception:
    print("RAM_GB=unknown")
PYEOF
)

# Parse KEY=VALUE lines into shell variables
BACKEND=""
GPU_NAME=""
GPU_COUNT=""
GPU_MEM_GB=""
CUDA_VERSION=""
HIP_VERSION=""
PLATFORM_INFO=""
PYTHON_VER=""
PYTORCH_VER=""
CPU_INFO=""
RAM_GB=""

while IFS='=' read -r key val; do
  case "$key" in
    BACKEND)      BACKEND="$val" ;;
    GPU_NAME)     GPU_NAME="$val" ;;
    GPU_COUNT)    GPU_COUNT="$val" ;;
    GPU_MEM_GB)   GPU_MEM_GB="$val" ;;
    CUDA_VERSION) CUDA_VERSION="$val" ;;
    HIP_VERSION)  HIP_VERSION="$val" ;;
    PLATFORM)     PLATFORM_INFO="$val" ;;
    PYTHON)       PYTHON_VER="$val" ;;
    PYTORCH)      PYTORCH_VER="$val" ;;
    CPU)          CPU_INFO="$val" ;;
    RAM_GB)       RAM_GB="$val" ;;
  esac
done <<< "$SYSINFO"

# Map backend to --device arg for Python scripts
if [[ "$BACKEND" == "rocm" ]]; then
  DEVICE_ARG="cuda"  # ROCm uses cuda device in PyTorch
else
  DEVICE_ARG="$BACKEND"
fi

echo "Backend:     $BACKEND"
echo "Device:      $GPU_NAME"
if [[ "$BACKEND" == "cuda" ]]; then
  echo "CUDA:        $CUDA_VERSION"
elif [[ "$BACKEND" == "rocm" ]]; then
  echo "HIP/ROCm:    $HIP_VERSION"
fi
echo "GPU Count:   $GPU_COUNT"
echo "GPU Memory:  ${GPU_MEM_GB} GB"
echo "CPU:         $CPU_INFO"
echo "RAM:         ${RAM_GB} GB"
echo "Platform:    $PLATFORM_INFO"
echo "Python:      $PYTHON_VER"
echo "PyTorch:     $PYTORCH_VER"
echo ""

if [[ "$BACKEND" == "cpu" ]]; then
  echo "WARNING: No GPU detected. Running in CPU fallback mode (slow)."
  echo ""
fi

echo "Data type:   $DTYPE"
echo "Filter:      $SCENARIO_FILTER"
echo "Warmup:      $WARMUP iterations"
echo "Iterations:  $ITERS iterations"

mkdir -p "$RESULTS_DIR"

# Count scenarios to run
RUN_COUNT=0
for sid in "${SCENARIO_ORDER[@]}"; do
  if should_run "$sid"; then
    RUN_COUNT=$((RUN_COUNT + 1))
  fi
done
echo "Scenarios:   $RUN_COUNT of ${#SCENARIO_ORDER[@]}"
echo "Report:      $REPORT_FILE"
echo ""

if [[ $RUN_COUNT -eq 0 ]]; then
  echo "ERROR: No scenarios match filter '$SCENARIO_FILTER'."
  echo "Use --list to see available scenarios."
  exit 1
fi

# ─── Run Benchmarks ──────────────────────────────────────────────────────

# Initialize JSON report with system info
python3 -c "
import json, datetime
report = {
    'suite': 'PerfSim-Survey-2026',
    'timestamp': datetime.datetime.now().isoformat(),
    'backend': '$BACKEND',
    'gpu': '$GPU_NAME',
    'gpu_count': '$GPU_COUNT',
    'gpu_memory_gb': '$GPU_MEM_GB',
    'cuda_version': '$CUDA_VERSION',
    'hip_version': '$HIP_VERSION',
    'pytorch_version': '$PYTORCH_VER',
    'python_version': '$PYTHON_VER',
    'platform': '$PLATFORM_INFO',
    'cpu': '$CPU_INFO',
    'ram_gb': '$RAM_GB',
    'dtype': '$DTYPE',
    'warmup': $WARMUP,
    'iterations': $ITERS,
    'scenarios': {}
}
with open('$REPORT_FILE', 'w') as f:
    json.dump(report, f, indent=2)
"

PASSED=0
FAILED=0
SKIPPED=0

for sid in "${SCENARIO_ORDER[@]}"; do
  if ! should_run "$sid"; then
    continue
  fi

  desc="${SCENARIO_DESC[$sid]}"
  bench_entry="${SCENARIO_BENCH[$sid]}"
  script="${bench_entry%%|*}"
  extra_args="${bench_entry#*|}"

  echo "------------------------------------------------------------"
  echo "  [$sid] $desc"
  echo "------------------------------------------------------------"

  SCENARIO_OUT="${RESULTS_DIR}/${sid}"
  mkdir -p "$SCENARIO_OUT"

  # Build command with --device flag
  CMD="python3 ${GT_DIR}/${script} --dtype ${DTYPE} --output-dir ${SCENARIO_OUT} --device ${DEVICE_ARG}"
  if [[ -n "$extra_args" ]]; then
    CMD="$CMD $extra_args"
  fi

  echo "  CMD: $CMD"
  echo ""

  START_TIME=$(date +%s)
  if timeout 600 bash -c "$CMD" 2>&1 | tee "${SCENARIO_OUT}/stdout.log"; then
    STATUS="pass"
    PASSED=$((PASSED + 1))
    echo "  -> [$sid] PASS"
  else
    EXIT_CODE=$?
    if [[ $EXIT_CODE -eq 124 ]]; then
      STATUS="timeout"
      echo "  -> [$sid] TIMEOUT (>600s)"
    else
      STATUS="fail"
      echo "  -> [$sid] FAIL (exit $EXIT_CODE)"
    fi
    FAILED=$((FAILED + 1))
  fi
  END_TIME=$(date +%s)
  ELAPSED=$((END_TIME - START_TIME))

  # Update JSON report with this scenario's result
  python3 -c "
import json, glob, os

with open('$REPORT_FILE', 'r') as f:
    report = json.load(f)

# Try to find any JSON result files produced by the benchmark
result_files = glob.glob('${SCENARIO_OUT}/*.json')
bench_results = {}
for rf in result_files:
    if os.path.basename(rf) != 'stdout.log':
        with open(rf, 'r') as f2:
            try:
                bench_results[os.path.basename(rf)] = json.load(f2)
            except json.JSONDecodeError:
                pass

report['scenarios']['$sid'] = {
    'description': '$desc',
    'status': '$STATUS',
    'elapsed_seconds': $ELAPSED,
    'script': '$script',
    'results': bench_results
}

with open('$REPORT_FILE', 'w') as f:
    json.dump(report, f, indent=2)
"
  echo ""
done

# ─── Summary ──────────────────────────────────────────────────────────────

echo "============================================================"
echo "  Summary"
echo "============================================================"
echo ""
echo "  Backend:  $BACKEND"
echo "  Device:   $GPU_NAME"
echo "  Passed:  $PASSED"
echo "  Failed:  $FAILED"
echo "  Total:   $RUN_COUNT"
echo ""
echo "  Report:  $REPORT_FILE"
echo ""

# Print quick scenario status table
echo "  Scenario Results:"
for sid in "${SCENARIO_ORDER[@]}"; do
  if should_run "$sid"; then
    python3 -c "
import json
with open('$REPORT_FILE') as f:
    r = json.load(f)
s = r['scenarios'].get('$sid', {})
status = s.get('status', 'skipped')
elapsed = s.get('elapsed_seconds', 0)
icon = '✓' if status == 'pass' else '✗' if status in ('fail','timeout') else '?'
print(f'    {icon} $sid  ({elapsed}s)  {status}')
"
  fi
done

echo ""
echo "============================================================"

if [[ $FAILED -gt 0 ]]; then
  echo "WARNING: $FAILED scenario(s) failed. Check logs in $RESULTS_DIR/"
  exit 1
else
  echo "All $PASSED scenarios completed successfully."
fi
