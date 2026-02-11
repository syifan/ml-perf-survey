#!/usr/bin/env python3
"""Run Timeloop on ResNet-50 first convolution layer and compare against analytical estimates.

This script:
1. Defines a ResNet-50 Conv1 workload (7x7, stride 2, 3->64 channels, 224x224 input)
2. Defines an Eyeriss-like accelerator architecture
3. Runs Timeloop via subprocess
4. Parses results (cycles, energy, utilization)
5. Computes analytical estimates and compares

Usage (inside Timeloop Docker container):
    python3 run_resnet50_conv.py --timeloop-bin /usr/local/bin/timeloop-mapper
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import yaml
from pathlib import Path


# ResNet-50 Conv1: 7x7 kernel, stride 2, 3 input channels, 64 output channels
# Input: 224x224x3, Output: 112x112x64
RESNET50_CONV1_PROBLEM = {
    "problem": {
        "shape": {
            "name": "Conv2D",
            "dimensions": ["N", "C", "M", "P", "Q", "R", "S"],
            "data-spaces": [
                {
                    "name": "Weights",
                    "projection": [
                        [["C"]],
                        [["M"]],
                        [["R"]],
                        [["S"]],
                    ],
                },
                {
                    "name": "Inputs",
                    "projection": [
                        [["N"]],
                        [["C"]],
                        [["R"], ["P"]],
                        [["S"], ["Q"]],
                    ],
                },
                {
                    "name": "Outputs",
                    "projection": [
                        [["N"]],
                        [["M"]],
                        [["P"]],
                        [["Q"]],
                    ],
                    "read-write": True,
                },
            ],
        },
        "instance": {
            "N": 1,
            "C": 3,
            "M": 64,
            "P": 112,
            "Q": 112,
            "R": 7,
            "S": 7,
            "Hstride": 2,
            "Wstride": 2,
        },
    }
}

# Simplified Eyeriss-like architecture (Row Stationary dataflow)
EYERISS_ARCH = {
    "architecture": {
        "version": "0.4",
        "nodes": [
            {
                "name": "system",
                "local": [
                    {
                        "name": "DRAM",
                        "class": "DRAM",
                        "attributes": {
                            "type": "LPDDR4",
                            "width": 64,
                            "block-size": 4,
                            "word-bits": 16,
                        },
                    }
                ],
                "subtree": [
                    {
                        "name": "chip",
                        "local": [
                            {
                                "name": "shared_glb",
                                "class": "smartbuffer_SRAM",
                                "attributes": {
                                    "depth": 16384,
                                    "width": 64,
                                    "block-size": 4,
                                    "word-bits": 16,
                                    "read_bandwidth": 16,
                                    "write_bandwidth": 16,
                                },
                            }
                        ],
                        "subtree": [
                            {
                                "name": "PE[0..167]",
                                "local": [
                                    {
                                        "name": "ifmap_spad",
                                        "class": "smartbuffer_SRAM",
                                        "attributes": {
                                            "depth": 12,
                                            "width": 16,
                                            "block-size": 1,
                                            "word-bits": 16,
                                        },
                                    },
                                    {
                                        "name": "weights_spad",
                                        "class": "smartbuffer_SRAM",
                                        "attributes": {
                                            "depth": 192,
                                            "width": 16,
                                            "block-size": 1,
                                            "word-bits": 16,
                                        },
                                    },
                                    {
                                        "name": "psum_spad",
                                        "class": "smartbuffer_SRAM",
                                        "attributes": {
                                            "depth": 16,
                                            "width": 16,
                                            "block-size": 1,
                                            "word-bits": 16,
                                        },
                                    },
                                    {
                                        "name": "mac",
                                        "class": "intmac",
                                        "attributes": {"datawidth": 16},
                                    },
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
    }
}

# Mapper configuration (use random search with timeout)
MAPPER_CONFIG = {
    "mapper": {
        "optimization-metrics": ["delay", "energy"],
        "timeout": 120,
        "victory-condition": 500,
        "algorithm": "random-pruned",
        "max-permutations-per-if-visit": 16,
        "num-threads": 4,
    }
}


def compute_analytical_estimates():
    """Compute analytical estimates for ResNet-50 Conv1 layer.

    ResNet-50 Conv1: 7x7 kernel, stride 2, 3->64 channels, 224x224 input
    Output: 112x112x64

    Total MACs = N * M * P * Q * C * R * S
               = 1 * 64 * 112 * 112 * 3 * 7 * 7 = 118,013,952
    """
    N, C, M, P, Q, R, S = 1, 3, 64, 112, 112, 7, 7
    total_macs = N * M * P * Q * C * R * S

    # Eyeriss has 168 PEs (14x12), each does 1 MAC/cycle at 200MHz
    num_pes = 168
    clock_freq_mhz = 200

    # Ideal cycles (100% utilization)
    ideal_cycles = total_macs / num_pes

    # Typical utilization for this layer shape ~50-75% due to mapping constraints
    # Conv1 is challenging because C=3 is very small
    estimated_utilization = 0.60
    estimated_cycles = ideal_cycles / estimated_utilization

    # Energy estimate: ~5500 fJ/MAC for Eyeriss (from published data)
    energy_per_mac_fj = 5500
    total_energy_uj = total_macs * energy_per_mac_fj / 1e9

    # Latency at 200MHz
    latency_ms = estimated_cycles / (clock_freq_mhz * 1e3)

    return {
        "total_macs": total_macs,
        "num_pes": num_pes,
        "ideal_cycles": round(ideal_cycles),
        "estimated_utilization": estimated_utilization,
        "estimated_cycles": round(estimated_cycles),
        "energy_per_mac_fj": energy_per_mac_fj,
        "total_energy_uj": round(total_energy_uj, 2),
        "estimated_latency_ms": round(latency_ms, 3),
    }


def write_configs(work_dir):
    """Write Timeloop configuration files to the working directory."""
    with open(os.path.join(work_dir, "problem.yaml"), "w") as f:
        yaml.dump(RESNET50_CONV1_PROBLEM, f, default_flow_style=False)

    with open(os.path.join(work_dir, "arch.yaml"), "w") as f:
        yaml.dump(EYERISS_ARCH, f, default_flow_style=False)

    with open(os.path.join(work_dir, "mapper.yaml"), "w") as f:
        yaml.dump(MAPPER_CONFIG, f, default_flow_style=False)


def run_timeloop(work_dir, timeloop_bin):
    """Run timeloop-mapper and return stdout."""
    cmd = [
        timeloop_bin,
        os.path.join(work_dir, "arch.yaml"),
        os.path.join(work_dir, "problem.yaml"),
        os.path.join(work_dir, "mapper.yaml"),
    ]
    print(f"Running: {' '.join(cmd)}")
    print(f"Working directory: {work_dir}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=work_dir,
        timeout=300,  # 5 minute timeout
    )

    print("STDOUT:")
    print(result.stdout[-3000:] if len(result.stdout) > 3000 else result.stdout)
    if result.returncode != 0:
        print("STDERR:")
        print(result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr)
    return result


def parse_timeloop_stats(work_dir):
    """Parse Timeloop output statistics."""
    stats = {}

    # Look for stats file
    stats_file = os.path.join(work_dir, "timeloop-mapper.stats.txt")
    if os.path.exists(stats_file):
        with open(stats_file) as f:
            content = f.read()
        stats["raw_stats"] = content[:5000]

        # Parse key metrics
        for line in content.split("\n"):
            line = line.strip()
            if "Cycles:" in line or "Total Cycles" in line:
                try:
                    val = int("".join(c for c in line.split(":")[-1] if c.isdigit()))
                    stats["total_cycles"] = val
                except ValueError:
                    pass
            elif "Energy:" in line or "Total Energy" in line:
                try:
                    val = float(line.split(":")[-1].strip().split()[0])
                    stats["total_energy"] = val
                except (ValueError, IndexError):
                    pass
            elif "Utilization" in line:
                try:
                    val = float(line.split(":")[-1].strip().rstrip("%")) / 100
                    stats["utilization"] = val
                except (ValueError, IndexError):
                    pass
            elif "GFLOPs" in line:
                try:
                    val = float(line.split(":")[-1].strip().split()[0])
                    stats["gflops"] = val
                except (ValueError, IndexError):
                    pass

    # Also check for XML/JSON output
    for ext in [".map.txt", ".map+stats.xml"]:
        map_file = os.path.join(work_dir, f"timeloop-mapper{ext}")
        if os.path.exists(map_file):
            with open(map_file) as f:
                stats[f"map_output_{ext}"] = f.read()[:3000]

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Run Timeloop on ResNet-50 Conv1 layer"
    )
    parser.add_argument(
        "--timeloop-bin",
        default="timeloop-mapper",
        help="Path to timeloop-mapper binary",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for results (default: data/evaluation/timeloop-results/)",
    )
    parser.add_argument(
        "--analytical-only",
        action="store_true",
        help="Only compute analytical estimates (no Timeloop run)",
    )
    args = parser.parse_args()

    # Determine output directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent.parent
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = repo_root / "data" / "evaluation" / "timeloop-results"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Timeloop ResNet-50 Conv1 Experiment")
    print("=" * 70)
    print()

    # Step 1: Analytical estimates
    print("=== Analytical Estimates ===")
    analytical = compute_analytical_estimates()
    for k, v in analytical.items():
        print(f"  {k}: {v}")
    print()

    if args.analytical_only:
        results = {
            "experiment": "timeloop_resnet50_conv1",
            "analytical_estimates": analytical,
            "timeloop_results": None,
            "note": "Analytical only mode - Timeloop not executed",
        }
        results_path = output_dir / "resnet50_conv1_results.json"
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {results_path}")
        return

    # Step 2: Run Timeloop
    with tempfile.TemporaryDirectory(prefix="timeloop_") as work_dir:
        print(f"=== Writing Configs to {work_dir} ===")
        write_configs(work_dir)

        print()
        print("=== Running Timeloop Mapper ===")
        result = run_timeloop(work_dir, args.timeloop_bin)

        print()
        print("=== Parsing Results ===")
        tl_stats = parse_timeloop_stats(work_dir)

        # Step 3: Compare
        print()
        print("=== Comparison: Timeloop vs Analytical ===")
        comparison = {}
        if "total_cycles" in tl_stats:
            ratio = tl_stats["total_cycles"] / analytical["estimated_cycles"]
            comparison["cycle_ratio_tl_over_analytical"] = round(ratio, 3)
            print(
                f"  Timeloop cycles: {tl_stats['total_cycles']}"
            )
            print(
                f"  Analytical est.: {analytical['estimated_cycles']}"
            )
            print(f"  Ratio (TL/Analytical): {ratio:.3f}")
        if "utilization" in tl_stats:
            print(
                f"  Timeloop utilization: {tl_stats['utilization']:.1%}"
            )
            print(
                f"  Analytical est.: {analytical['estimated_utilization']:.1%}"
            )

        # Save results
        results = {
            "experiment": "timeloop_resnet50_conv1",
            "workload": {
                "model": "ResNet-50",
                "layer": "Conv1",
                "dimensions": {"N": 1, "C": 3, "M": 64, "P": 112, "Q": 112, "R": 7, "S": 7},
                "stride": 2,
            },
            "architecture": "Eyeriss-like (168 PEs, 16-bit)",
            "analytical_estimates": analytical,
            "timeloop_results": tl_stats,
            "comparison": comparison,
            "timeloop_exit_code": result.returncode,
        }

        results_path = output_dir / "resnet50_conv1_results.json"
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to {results_path}")

        # Also save configs for reproducibility
        configs_dir = output_dir / "configs"
        configs_dir.mkdir(exist_ok=True)
        for cfg_name in ["problem.yaml", "arch.yaml", "mapper.yaml"]:
            src = os.path.join(work_dir, cfg_name)
            dst = configs_dir / cfg_name
            with open(src) as sf, open(dst, "w") as df:
                df.write(sf.read())
        print(f"Configs saved to {configs_dir}")


if __name__ == "__main__":
    main()
