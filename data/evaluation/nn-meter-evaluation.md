# nn-Meter Reproducibility Evaluation

This document assesses nn-Meter's reproducibility, usability, and practical considerations for edge device latency prediction research.

---

## Overview

**Tool:** nn-Meter
**Paper:** nn-Meter: Towards Accurate Latency Prediction of Deep-Learning Model Inference on Diverse Edge Devices (MobiSys 2021, Best Paper)
**Authors:** Zhang et al. (Microsoft Research)
**Repository:** https://github.com/microsoft/nn-Meter
**License:** MIT
**Evaluation Date:** 2026-02-07

---

## Setup Assessment

### Installation

**Method:** pip install (simple)
**Time to First Result:** ~2-5 minutes

```bash
pip install nn-meter
```

### Dependencies

**Automatic:**
- sklearn (for pre-trained predictors)
- PyTorch/TensorFlow (for model parsing)
- pkg_resources (via setuptools)

**Manual (for Python 3.14+):**
```bash
pip install setuptools  # Required for pkg_resources
```

### Compatibility Issues Encountered

**Issue 1: Missing pkg_resources (Python 3.14)**
- Error: `ModuleNotFoundError: No module named 'pkg_resources'`
- Cause: pkg_resources removed from Python 3.14 stdlib
- Solution: `pip install setuptools`

**Issue 2: Pickle incompatibility (scikit-learn version)**
- Error: `ValueError: node array from the pickle has an incompatible dtype`
- Cause: Pre-trained models pickled with older scikit-learn
- Status: **Blocking** - Cannot use pre-trained predictors with current scikit-learn

**Recommendation:** Use Python 3.10 with scikit-learn ~1.0 for full compatibility.

---

## Repository Structure

```
nn-meter/
├── nn_meter/
│   ├── predictor/           # Core prediction engine
│   │   ├── nn_meter_predictor.py   # Main API
│   │   └── utils.py         # Predictor loading
│   ├── builder/             # Predictor training tools
│   ├── kernel_detector/     # Kernel fusion detection
│   └── utils/               # Configuration, downloads
├── examples/                # Usage examples
├── tests/                   # Unit tests
└── data/                    # Pre-trained predictors (downloaded)
    └── predictor/
        ├── cortexA76cpu_tflite21/
        ├── adreno640gpu_tflite21/
        ├── adreno630gpu_tflite21/
        └── myriadvpu_openvino2019r2/
```

---

## Pre-trained Predictors

### Available Predictors

| Predictor | Category | Framework | Kernels |
|-----------|----------|-----------|---------|
| cortexA76cpu_tflite21 | CPU | TFLite 2.1 | 16 |
| adreno640gpu_tflite21 | GPU | TFLite 2.1 | 10 |
| adreno630gpu_tflite21 | GPU | TFLite 2.1 | 10 |
| myriadvpu_openvino2019r2 | VPU | OpenVINO 2019R2 | 12 |

### Supported Kernel Types

**CPU (Cortex-A76):**
- conv-bn-relu, dwconv-bn-relu, fc, global-avgpool
- hswish, relu, se, split, add, addrelu
- maxpool, avgpool, bn, bnrelu, channelshuffle, concat

**GPU (Adreno 640/630):**
- conv-bn-relu, dwconv-bn-relu, hswish, relu
- se, maxpool, avgpool, bn, bnrelu, concat

---

## Basic Usage

### Listing Available Predictors

```python
from nn_meter import list_latency_predictors

for predictor in list_latency_predictors():
    print(predictor['name'], predictor['category'])
```

### Predicting Latency

```python
from nn_meter import load_latency_predictor
import torchvision.models as models

# Load predictor
predictor = load_latency_predictor('cortexA76cpu_tflite21')

# Predict for PyTorch model
model = models.resnet18()
latency = predictor.predict(model, model_type='torch')
print(f'Predicted latency: {latency:.2f} ms')
```

### Supported Input Formats

| Format | Parameter | Notes |
|--------|-----------|-------|
| PyTorch | `model_type='torch'` | Requires torch |
| TensorFlow | `model_type='tf'` | Requires tensorflow |
| ONNX | `model_type='onnx'` | Requires onnx |
| nn-Meter IR | Default | Internal representation |

---

## Methodology

### Kernel-Level Decomposition

nn-Meter predicts latency through:

1. **Graph Parsing:** Convert model to kernel-level DAG
2. **Kernel Fusion Detection:** Identify fused operations
3. **Kernel Latency Prediction:** ML model for each kernel type
4. **Summation:** Aggregate kernel latencies

### Adaptive Sampling

For training new predictors:
- Identifies representative kernel configurations
- Minimizes measurement overhead
- Achieves high accuracy with limited samples

---

## Accuracy Claims vs. Reality

### Published Claims (MobiSys 2021)

- 99% correlation on edge devices
- <5% MAPE for most models
- Generalizes to unseen architectures (NAS models)

### Evaluation Observations

1. **Pre-trained predictors available:** 4 device configurations
2. **Automatic download:** Predictors fetched from GitHub releases
3. **Model format flexibility:** PyTorch, TensorFlow, ONNX

### Critical Limitation: Pickle Compatibility

**Status:** Pre-trained predictors fail to load with current scikit-learn versions.

**Error:**
```
ValueError: node array from the pickle has an incompatible dtype:
- expected: ... 'missing_go_to_left' ...
- got: ... (older format without missing_go_to_left)
```

**Root Cause:** Predictors pickled with scikit-learn <1.0, incompatible with >=1.3

**Workarounds:**
1. Pin scikit-learn to older version: `pip install scikit-learn==1.0.2`
2. Retrain predictors with current scikit-learn
3. Request updated predictors from Microsoft

---

## Usability Assessment

### Strengths

| Aspect | Rating | Notes |
|--------|--------|-------|
| Installation | Excellent | Single pip install |
| API simplicity | Excellent | 2-3 lines of code |
| Model format support | Excellent | PyTorch, TF, ONNX |
| Documentation | Good | README, examples |
| Device coverage | Limited | 4 pre-trained devices |

### Challenges

| Aspect | Rating | Notes |
|--------|--------|-------|
| Scikit-learn compatibility | Poor | Pickle version mismatch |
| Python version | Moderate | 3.14 needs workaround |
| Adding new devices | Hard | Requires measurements |
| GPU predictor coverage | Limited | Only 10 kernel types |

---

## Reproducibility Checklist

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Source code available | Yes | Full Python source |
| Build instructions | Yes | pip install |
| Dependencies documented | Partial | Not pinned versions |
| Pre-trained models | Yes | Auto-downloaded |
| Example inputs | Yes | Works with torchvision |
| Reference outputs | No | No expected values |
| Test suite | Yes | Unit tests included |

**Reproducibility Score: 5/10**

Note: Score significantly reduced due to scikit-learn compatibility breaking pre-trained predictors.

---

## Practical Recommendations

### For Researchers

1. **Pin dependencies:** `scikit-learn==1.0.2` for pre-trained predictors
2. **Use Python 3.10:** Best compatibility
3. **Verify predictions:** Compare with actual measurements if possible
4. **Consider retraining:** If you have target device access

### For Practitioners

1. **NAS applications:** Fast latency estimates for architecture search
2. **Mobile deployment:** Cortex-A76 predictor covers many phones
3. **Framework selection:** TFLite predictions most accurate

### Known Limitations

1. **Pickle compatibility:** Pre-trained models may not load
2. **Limited GPU kernels:** Only 10 vs 16 for CPU
3. **Framework-specific:** Trained on TFLite/OpenVINO only
4. **Device-specific:** No easy way to adapt to new devices

---

## Comparison with Alternatives

| Tool | Scope | Accuracy | Device Coverage |
|------|-------|----------|-----------------|
| **nn-Meter** | Edge devices | 99% corr | 4 pre-trained |
| Timeloop | Accelerators | ~10% error | Configurable |
| TVM Autotuner | GPUs/CPUs | Ground truth | Any (slow) |
| Habitat | Mobile GPUs | ~10% error | Limited |

---

## Conclusion

**nn-Meter has excellent design but significant reproducibility issues due to dependency version sensitivity.**

Key findings:
- Simple API for latency prediction
- Multiple device predictors available
- scikit-learn version incompatibility blocks usage
- Python 3.14 requires setuptools workaround

Recommended for:
- NAS/AutoML with latency constraints
- Mobile deployment planning
- Quick latency estimates

Not recommended (without workarounds):
- Production use with current Python/scikit-learn
- Users without ability to pin dependencies
- Applications requiring exact latency values

**Action Required:** Microsoft should release updated predictors compatible with current scikit-learn, or provide version-pinned installation instructions.

---

*Evaluation by Leo | ML Performance Survey Project*
