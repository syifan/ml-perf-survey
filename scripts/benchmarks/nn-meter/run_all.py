#!/usr/bin/env python3
"""
nn-Meter benchmark evaluation script for ML Performance Survey.

Runs nn-meter predictions on CNN and Transformer benchmarks.
"""

import time
import json
from datetime import datetime
import torch
import torchvision.models as models
from nn_meter import load_latency_predictor

# Benchmark configurations
BENCHMARKS = {
    "CNN-1": {
        "model": "resnet50",
        "input_shape": (1, 3, 224, 224),
        "description": "ResNet-50 inference"
    },
    "CNN-2": {
        "model": "vgg16",
        "input_shape": (1, 3, 224, 224),
        "description": "VGG-16 inference"
    },
    "CNN-3": {
        "model": "mobilenet_v2",
        "input_shape": (1, 3, 224, 224),
        "description": "MobileNet-V2 inference"
    },
}

PREDICTORS = [
    "cortexA76cpu_tflite21",
    "adreno640gpu_tflite21",
]


def get_model(model_name):
    """Get PyTorch model by name."""
    if model_name == "resnet50":
        return models.resnet50(weights=None)
    elif model_name == "vgg16":
        return models.vgg16(weights=None)
    elif model_name == "mobilenet_v2":
        return models.mobilenet_v2(weights=None)
    else:
        raise ValueError(f"Unknown model: {model_name}")


def run_benchmark():
    """Run all benchmarks with all predictors."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "tool": "nn-meter",
        "version": "2.0",
        "predictions": [],
        "setup_notes": [],
        "issues_encountered": []
    }

    # Record setup time
    setup_start = time.time()

    for predictor_name in PREDICTORS:
        print(f"\nLoading predictor: {predictor_name}")
        try:
            predictor = load_latency_predictor(predictor_name)
            load_time = time.time() - setup_start
            print(f"  Predictor loaded in {load_time:.2f}s")
        except Exception as e:
            results["issues_encountered"].append(f"Failed to load {predictor_name}: {str(e)}")
            continue

        for bench_id, bench_config in BENCHMARKS.items():
            print(f"\n  Running {bench_id}: {bench_config['description']}")

            try:
                # Get model
                model = get_model(bench_config["model"])
                model.eval()

                # Run prediction (time it)
                pred_start = time.time()
                latency = predictor.predict(model, model_type="torch")
                pred_time = time.time() - pred_start

                result = {
                    "benchmark": bench_id,
                    "predictor": predictor_name,
                    "model": bench_config["model"],
                    "input_shape": bench_config["input_shape"],
                    "predicted_latency_ms": latency,
                    "prediction_time_s": pred_time,
                    "status": "success"
                }

                print(f"    Predicted latency: {latency:.2f} ms")
                print(f"    Prediction time: {pred_time:.3f}s")

            except Exception as e:
                result = {
                    "benchmark": bench_id,
                    "predictor": predictor_name,
                    "model": bench_config["model"],
                    "status": "error",
                    "error": str(e)
                }
                print(f"    ERROR: {str(e)}")
                results["issues_encountered"].append(f"{bench_id}/{predictor_name}: {str(e)}")

            results["predictions"].append(result)

    # Add setup notes
    results["setup_notes"] = [
        "Installed via pip install nn-meter",
        "Required setuptools for pkg_resources",
        "PyTorch CPU version used for model loading",
        "Predictors downloaded automatically on first use"
    ]

    return results


def main():
    print("=" * 60)
    print("nn-Meter Benchmark Evaluation")
    print("ML Performance Survey Project")
    print("=" * 60)

    results = run_benchmark()

    # Save results
    output_path = "/output/predictions.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n\nResults saved to: {output_path}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    successful = [p for p in results["predictions"] if p["status"] == "success"]
    failed = [p for p in results["predictions"] if p["status"] != "success"]

    print(f"Successful predictions: {len(successful)}")
    print(f"Failed predictions: {len(failed)}")

    if successful:
        print("\nPredictions:")
        for p in successful:
            print(f"  {p['benchmark']} ({p['predictor']}): {p['predicted_latency_ms']:.2f} ms")

    if results["issues_encountered"]:
        print("\nIssues:")
        for issue in results["issues_encountered"]:
            print(f"  - {issue}")


if __name__ == "__main__":
    main()
