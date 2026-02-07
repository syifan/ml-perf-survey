# Timeloop Evaluation Report (Preliminary)

**Tool:** Timeloop (via Docker infrastructure)
**Evaluation Date:** 2026-02-07
**Evaluator:** Leo (Paper Analyst)

---

## Executive Summary

Timeloop evaluation partially completed. Docker infrastructure image exists but has Python binding issues. Native timeloop binaries work but require complex configuration setup.

**Status:** PARTIALLY BLOCKED - Python bindings fail, native CLI requires additional work

---

## Setup Process

### Docker Image
- **Image:** `timeloopaccelergy/accelergy-timeloop-infrastructure:latest`
- **Size:** ~2GB
- **Pull time:** ~2 minutes

### Test Results

#### Python Wrapper (pytimeloop)
- **Status:** FAILED
- **Error:** `ImportError: libbarvinok.so.23: cannot open shared object file`
- The Python timeloop frontend cannot load required shared libraries

#### Native CLI Binaries
- **Status:** AVAILABLE
- `timeloop-model` and `timeloop-mapper` binaries exist
- Require YAML configuration files for architecture, problem, and mapping

---

## Configuration Requirements

Timeloop requires three types of YAML configurations:
1. **Architecture** (`arch.yaml`): Hardware description (PE array, memory hierarchy)
2. **Problem** (`problem.yaml`): Workload dimensions (conv params, batch size)
3. **Mapping** (`mapping.yaml`): Loop nest and data movement schedule

Example architecture found: Eyeriss-like (14x12 PE array, 65nm)

---

## Benchmark Compatibility

| Benchmark | Timeloop Support | Notes |
|-----------|------------------|-------|
| CNN-1 (ResNet-50) | Yes | Conv layers need individual configs |
| CNN-2 (VGG-16) | Yes | Conv layers available in examples |
| CNN-3 (MobileNet-V2) | Yes | Depthwise separable needs special handling |
| XFMR-1 (BERT) | Partial | Attention as GEMM |
| LLM/Distributed | No | Single accelerator only |

---

## Next Steps

To complete evaluation:
1. Fix Docker Python binding issue (or use native CLI)
2. Create problem YAML files for benchmark CNN layers
3. Run timeloop-mapper on each layer
4. Collect latency/energy estimates
5. Compare to published Eyeriss results for validation

---

## Preliminary Assessment

### Setup Complexity: 5/10 (Moderate)
- Docker image provides most dependencies
- Python wrapper broken, CLI requires learning curve
- Configuration format is powerful but verbose

### Documentation: 7/10 (Good)
- Tutorials available in accelergy-timeloop-infrastructure
- Academic papers provide architecture details
- API reference less complete

### Platform Support
- Docker required for reproducible setup
- x86_64 primary target
- aarch64 may have issues (shared library not found)

---

## Artifacts

- Example configs: `/tmp/timeloop-exercises/workspace/example_designs/`
- Eyeriss architecture: `eyeriss_like/arch.yaml`
- Layer shapes: `layer_shapes/resnet18/`, `layer_shapes/vgg16/`

---

*Full evaluation requires resolving Docker Python binding issue or switching to CLI-based evaluation.*
