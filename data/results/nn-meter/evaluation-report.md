# nn-Meter Evaluation Report

**Tool:** nn-Meter v2.0
**Evaluation Date:** 2026-02-07
**Evaluator:** Leo (Paper Analyst)

---

## Executive Summary

nn-Meter could not be successfully executed on the benchmark suite due to **critical reproducibility issues**. The tool has extensive dependency version constraints that are poorly documented and incompatible with modern Python environments.

**Status:** BLOCKED - Requires significant environment engineering to reproduce

---

## Setup Attempts

### Attempt 1: Native Python 3.14 Environment
- **Result:** FAILED
- **Issue:** scikit-learn pickle incompatibility
- The pretrained kernel predictors were serialized with sklearn 0.23.1
- sklearn 1.8.0 (latest) cannot deserialize these models
- sklearn 1.0.2 requires Python <=3.11

### Attempt 2: Docker with Python 3.10 + sklearn 1.7.2
- **Result:** FAILED
- **Issue:** numpy dtype incompatibility
- sklearn 1.7.2 still cannot load 0.23.1 pickles

### Attempt 3: Docker with Python 3.10 + sklearn 1.0.2
- **Result:** PARTIAL SUCCESS
- Predictors load with deprecation warnings
- **New Issue:** Requires onnx + onnx-simplifier for PyTorch model conversion

### Attempt 4: Docker with onnx 1.14.0
- **Result:** FAILED
- **Issue:** onnx-simplifier fails to build on aarch64
- Error: "'NoneType' object is not callable" during model conversion

---

## Compatibility Matrix

| Dependency | Required Version | Available | Status |
|------------|------------------|-----------|--------|
| Python | 3.10 | 3.14 (system) | Docker needed |
| scikit-learn | 1.0.x | 1.8.0 (latest) | Downgrade needed |
| numpy | 1.26.x | 2.4.2 (latest) | Downgrade needed |
| torch | 1.10.0/1.9.0/1.7.1 | 1.13.1+ (for aarch64) | Version mismatch |
| onnx | 1.10.0/1.9.0 | 1.14.0 | Version mismatch |
| onnx-simplifier | Required | Fails on aarch64 | Build failure |

---

## Ease of Use Assessment (Partial)

### Setup Complexity: 3/10 (Very Difficult)
- Requires Docker container with specific environment
- Multiple dependency version conflicts
- No documented compatibility matrix
- ~4+ hours to attempt setup, still unsuccessful

### Documentation Quality: 4/10 (Poor)
- README provides basic examples
- No version pinning requirements documented
- No troubleshooting for common errors
- Predictor models trained with undocumented sklearn version

### API Design: N/A (Could not test)

### Error Handling: 2/10 (Very Poor)
- Silent failures common
- Error messages do not suggest solutions
- Version compatibility errors are cryptic

---

## Key Findings for Survey Paper

### 1. Reproducibility Gap
nn-Meter exemplifies a common reproducibility issue in ML tooling:
- Pretrained models serialized with specific library versions
- No version pinning in package metadata
- Rapidly evolving Python ecosystem breaks compatibility

### 2. Platform Limitations
- Only tested on x86_64
- aarch64/ARM64 support limited (onnx-simplifier fails)
- No pre-built wheels for many dependencies

### 3. Dependency Hell
Full dependency chain requires:
```
Python 3.10
sklearn==1.0.2
numpy<2.0
onnx==1.10.0
onnx-simplifier (x86_64 only)
torch==1.10.0 (not available for aarch64)
```

---

## Recommendations

### For nn-Meter Maintainers
1. Provide Docker images with tested environments
2. Re-train predictors with newer sklearn or use portable format
3. Document exact version requirements
4. Provide fallback for missing onnx-simplifier

### For Survey Paper
1. Document this as a case study in reproducibility challenges
2. Ease of Use score: **3/10** (setup blocked evaluation)
3. Note that published accuracy claims cannot be verified
4. Recommend practitioners verify environment compatibility before adoption

---

## Artifacts

- Dockerfile: `scripts/benchmarks/nn-meter/Dockerfile`
- Evaluation script: `scripts/benchmarks/nn-meter/run_all.py`
- Raw results: `data/results/nn-meter/predictions.json`

---

*This evaluation demonstrates that tool reproducibility is a critical dimension for practical ML performance modeling. Even well-cited tools may be difficult to use outside their original development environment.*
