#!/usr/bin/env python3
"""Validate NeuSight GPU performance predictions against published accuracy claims.

NeuSight predicts GPU kernel latency using tile-based decomposition + MLP predictors.
Paper claims 97.7% accuracy (2.3% mean error) on NVIDIA GPUs (ASPLOS 2025).

Strategy: NeuSight requires CUDA at import time, so we cannot run predictions on
CPU-only CI runners. Instead, we independently validate accuracy by:
1. Reading NeuSight's pre-computed prediction JSONs from their artifact repo
2. Reading ground truth label JSONs (measured GPU latencies)
3. Computing Absolute Percentage Error (APE) independently
4. Comparing our computed errors against paper-claimed numbers

Usage:
    python3 run_neusight_prediction.py --output-dir data/evaluation/neusight-results/
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


NEUSIGHT_REPO = "https://github.com/sitar-lab/NeuSight.git"
NEUSIGHT_DIR = "/tmp/NeuSight"

# Map full device directory names to short names used in the paper
DEVICE_SHORT_NAMES = {
    "NVIDIA_H100_80GB_HBM3": "H100",
    "NVIDIA_A100_80GB_PCIe": "A100_80G_PCIe",
    "NVIDIA_A100-PCIE-40GB": "A100_40G_PCIe",
    "NVIDIA_A100-SXM4-40GB": "A100_SXM",
    "NVIDIA_L4": "L4",
    "Tesla_T4": "T4",
    "Tesla_V100-PCIE-32GB": "V100",
    "Tesla_P100-PCIE-16GB": "P100",
    "Tesla_P4": "P4",
}

# Paper-claimed accuracy from NeuSight Table 2 (ASPLOS 2025)
# Short device name -> { mode -> mean_MAPE_pct }
PAPER_CLAIMS = {
    "H100": {"inf": 2.3, "train": 4.1},
    "A100_80G_PCIe": {"inf": 3.1, "train": 5.8},
    "V100": {"inf": 5.2, "train": 7.4},
    "L4": {"inf": 3.8},
    "T4": {"inf": 6.1},
}


def clone_neusight():
    """Clone the NeuSight repository if not already present."""
    if os.path.exists(NEUSIGHT_DIR):
        print(f"NeuSight already cloned at {NEUSIGHT_DIR}")
        return True
    print(f"Cloning NeuSight from {NEUSIGHT_REPO}...")
    result = subprocess.run(
        ["git", "clone", "--depth", "1", NEUSIGHT_REPO, NEUSIGHT_DIR],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        print(f"Clone failed: {result.stderr}")
        return False
    print("Clone successful.")
    return True


def validate_from_json_files():
    """Validate NeuSight accuracy by comparing prediction JSONs vs label JSONs.

    For each device, enumerate all label JSON files, find the matching NeuSight
    prediction JSON, and compute APE from e2e_latency values.
    """
    label_base = os.path.join(NEUSIGHT_DIR, "scripts", "asplos", "label")
    pred_base = os.path.join(NEUSIGHT_DIR, "scripts", "asplos", "results", "prediction")

    # Results: short_device_name -> mode -> list of per-model entries
    results = {}
    detailed = []

    if not os.path.isdir(label_base) or not os.path.isdir(pred_base):
        print("  ERROR: label or prediction directory not found")
        return results, detailed

    for device_dir in sorted(os.listdir(label_base)):
        label_dir = os.path.join(label_base, device_dir)
        if not os.path.isdir(label_dir):
            continue

        short_name = DEVICE_SHORT_NAMES.get(device_dir, device_dir)
        pred_dir = os.path.join(pred_base, device_dir, "neusight")
        if not os.path.isdir(pred_dir):
            print(f"  {device_dir} ({short_name}): no neusight predictions, skipping")
            continue

        # Get set of available prediction JSONs
        pred_jsons = {f for f in os.listdir(pred_dir) if f.endswith(".json")}

        for label_fname in sorted(os.listdir(label_dir)):
            if not label_fname.endswith(".json"):
                continue

            # Check if matching prediction exists
            if label_fname not in pred_jsons:
                continue

            config_name = label_fname.replace(".json", "")

            # Determine mode from filename: "{model}-{mode}-{seqlen}-{batch}[-{option}].json"
            parts = config_name.split("-")
            if len(parts) < 3:
                continue
            mode = parts[-3] if len(parts) >= 4 else parts[1]
            # Mode is typically the second field: model_name-mode-seqlen-batch
            # model_name can contain underscores but not hyphens
            # Find "inf" or "train" in parts
            file_mode = None
            for p in parts:
                if p in ("inf", "train"):
                    file_mode = p
                    break
            if not file_mode:
                continue

            # Read both JSONs
            with open(os.path.join(label_dir, label_fname)) as f:
                label_data = json.load(f)
            with open(os.path.join(pred_dir, label_fname)) as f:
                pred_data = json.load(f)

            label_e2e = label_data.get("e2e_latency")
            pred_e2e = pred_data.get("e2e_latency")

            if label_e2e is None or pred_e2e is None:
                continue
            label_e2e = float(label_e2e)
            pred_e2e = float(pred_e2e)
            if label_e2e <= 0:
                continue

            ape = abs(pred_e2e - label_e2e) / label_e2e * 100

            entry = {
                "config": config_name,
                "device_full": device_dir,
                "device_short": short_name,
                "mode": file_mode,
                "actual_ms": round(label_e2e, 3),
                "predicted_ms": round(pred_e2e, 3),
                "ape_pct": round(ape, 2),
                "num_layers": label_data.get("num_layer", 1),
            }

            key = (short_name, file_mode)
            results.setdefault(key, []).append(entry)
            detailed.append(entry)

    return results, detailed


def inventory_prediction_data():
    """Inventory what prediction/label data exists in the repo."""
    pred_base = os.path.join(NEUSIGHT_DIR, "scripts", "asplos", "results", "prediction")
    label_base = os.path.join(NEUSIGHT_DIR, "scripts", "asplos", "label")

    inventory = {
        "devices_with_predictions": [],
        "devices_with_labels": [],
        "methods_available": set(),
        "model_configs_per_device": {},
    }

    if os.path.isdir(pred_base):
        for device in sorted(os.listdir(pred_base)):
            device_path = os.path.join(pred_base, device)
            if not os.path.isdir(device_path):
                continue
            inventory["devices_with_predictions"].append(device)
            methods = [m for m in os.listdir(device_path) if os.path.isdir(os.path.join(device_path, m))]
            inventory["methods_available"].update(methods)
            for method in methods:
                method_path = os.path.join(device_path, method)
                jsons = [f for f in os.listdir(method_path) if f.endswith(".json")]
                inventory["model_configs_per_device"].setdefault(device, {})[method] = len(jsons)

    if os.path.isdir(label_base):
        for device in sorted(os.listdir(label_base)):
            if os.path.isdir(os.path.join(label_base, device)):
                inventory["devices_with_labels"].append(device)

    inventory["methods_available"] = sorted(inventory["methods_available"])
    return inventory


def main():
    parser = argparse.ArgumentParser(description="Validate NeuSight prediction accuracy")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--skip-clone", action="store_true")
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent.parent
    output_dir = Path(args.output_dir) if args.output_dir else repo_root / "data" / "evaluation" / "neusight-results"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("NeuSight Prediction Accuracy Validation")
    print("=" * 70)
    print()
    print("Strategy: Compare prediction JSONs vs label JSONs from artifact repo")
    print("(NeuSight requires CUDA at import time; we validate pre-computed results)")
    print()

    # Step 1: Clone
    if not args.skip_clone:
        if not clone_neusight():
            results = {
                "experiment": "neusight_validation",
                "status": "FAILED",
                "error": "Could not clone NeuSight repository",
            }
            with open(output_dir / "neusight_results.json", "w") as f:
                json.dump(results, f, indent=2)
            sys.exit(1)

    # Step 2: Inventory
    print("=== Data Inventory ===")
    inventory = inventory_prediction_data()
    print(f"  Devices with predictions: {inventory['devices_with_predictions']}")
    print(f"  Devices with labels: {inventory['devices_with_labels']}")
    print(f"  Methods: {inventory['methods_available']}")
    for dev, methods in inventory["model_configs_per_device"].items():
        print(f"  {dev}: {methods}")

    # Step 3: Validate from JSON pairs
    print("\n=== Per-Model Validation (prediction JSON vs label JSON) ===")
    per_device_errors, detailed_entries = validate_from_json_files()

    # Summarize per device/mode
    per_device_summary = {}
    for (short_name, mode), entries in sorted(per_device_errors.items()):
        apes = [e["ape_pct"] for e in entries]
        mean_ape = sum(apes) / len(apes)
        key = f"{short_name}_{mode}"
        per_device_summary[key] = {
            "device": short_name,
            "mode": mode,
            "num_models": len(entries),
            "mean_ape_pct": round(mean_ape, 2),
            "min_ape_pct": round(min(apes), 2),
            "max_ape_pct": round(max(apes), 2),
            "per_model": entries,
        }
        paper_claim = PAPER_CLAIMS.get(short_name, {}).get(mode)
        claim_str = f" (paper claims {paper_claim}%)" if paper_claim else ""
        print(f"  {short_name} {mode}: mean APE = {mean_ape:.1f}%{claim_str} [{len(entries)} models]")

    # Step 4: Compare against paper claims
    print("\n=== Paper Claim Comparison ===")
    claim_comparisons = []
    for device, modes in PAPER_CLAIMS.items():
        for mode, claimed_error in modes.items():
            key = f"{device}_{mode}"
            computed = per_device_summary.get(key)
            if computed:
                diff = computed["mean_ape_pct"] - claimed_error
                verdict = "MATCH" if abs(diff) < 1.0 else ("CLOSE" if abs(diff) < 3.0 else "MISMATCH")
                comparison = {
                    "device": device,
                    "mode": mode,
                    "paper_claimed_error_pct": claimed_error,
                    "our_computed_error_pct": computed["mean_ape_pct"],
                    "difference_pct": round(diff, 2),
                    "verdict": verdict,
                    "num_models_tested": computed["num_models"],
                }
                claim_comparisons.append(comparison)
                print(f"  {device} {mode}: paper={claimed_error}%, ours={computed['mean_ape_pct']}% -> {verdict} (delta={diff:+.1f}%)")
            else:
                comparison = {
                    "device": device,
                    "mode": mode,
                    "paper_claimed_error_pct": claimed_error,
                    "our_computed_error_pct": None,
                    "verdict": "NO_DATA",
                }
                claim_comparisons.append(comparison)
                print(f"  {device} {mode}: paper={claimed_error}%, NO DATA")

    # Step 5: Compile results
    results = {
        "experiment": "neusight_validation",
        "tool": "NeuSight",
        "paper": "Forecasting GPU Performance for DL Training and Inference (ASPLOS 2025)",
        "repo": NEUSIGHT_REPO,
        "method": "json_pair_validation",
        "description": (
            "Independent validation of NeuSight accuracy claims by comparing "
            "prediction JSONs vs label JSONs from the artifact repository. "
            "For each device/model config, we read the e2e_latency from both "
            "the NeuSight prediction and the ground truth label, then compute "
            "APE independently."
        ),
        "status": "COMPLETED",
        "data_inventory": inventory,
        "claim_comparisons": claim_comparisons,
        "per_device_summary": per_device_summary,
        "total_configs_validated": len(detailed_entries),
    }

    results_path = output_dir / "neusight_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {results_path}")

    # Summary
    print("\n=== Final Summary ===")
    matches = sum(1 for c in claim_comparisons if c["verdict"] == "MATCH")
    close = sum(1 for c in claim_comparisons if c["verdict"] == "CLOSE")
    mismatches = sum(1 for c in claim_comparisons if c["verdict"] == "MISMATCH")
    no_data = sum(1 for c in claim_comparisons if c["verdict"] == "NO_DATA")
    print(f"  Total configs validated: {len(detailed_entries)}")
    print(f"  Claims verified: {matches} MATCH, {close} CLOSE, {mismatches} MISMATCH, {no_data} NO_DATA")


if __name__ == "__main__":
    main()
