# ASTRA-sim Experiment Results

**Date:** 2026-02-11T23:31:08Z
**Experiment:** ResNet-50 Data-Parallel Training + All-Reduce Microbenchmarks
**Platform:** HGX-H100 validated configuration

## Published Validation Numbers (HGX-H100)

| GPU Count | Geomean Error Rate |
|-----------|-------------------|
| 2 GPUs | 20.63% |
| 4 GPUs | 12.01% |
| 8 GPUs | 9.69% |

## Simulation Results

### microbench_all_reduce_4npus_1MB.log
No cycle counts extracted.

### microbench_all_reduce_8npus.log

| NPU | Total Cycles |
|-----|-------------|
| 4 | 57,426 |
| 5 | 57,426 |
| 6 | 57,426 |
| 7 | 57,426 |
| 0 | 57,426 |
| 1 | 57,426 |
| 2 | 57,426 |
| 3 | 57,426 |

**Average:** 57,426 cycles
**Max:** 57,426 cycles
**Min:** 57,426 cycles

**Raw output (first 10 lines):**
```
[2026-02-11 23:31:07.966] [workload] [info] sys[4] finished, 57426 cycles, exposed communication 57426 cycles.
[2026-02-11 23:31:07.966] [statistics] [info] sys[4], Wall time: 57426
[2026-02-11 23:31:07.966] [statistics] [info] sys[4], Comm time: 57426
[2026-02-11 23:31:07.966] [workload] [info] sys[5] finished, 57426 cycles, exposed communication 57426 cycles.
[2026-02-11 23:31:07.966] [statistics] [info] sys[5], Wall time: 57426
[2026-02-11 23:31:07.966] [statistics] [info] sys[5], Comm time: 57426
[2026-02-11 23:31:07.966] [workload] [info] sys[6] finished, 57426 cycles, exposed communication 57426 cycles.
[2026-02-11 23:31:07.966] [statistics] [info] sys[6], Wall time: 57426
[2026-02-11 23:31:07.966] [statistics] [info] sys[6], Comm time: 57426
[2026-02-11 23:31:07.966] [workload] [info] sys[7] finished, 57426 cycles, exposed communication 57426 cycles.
```

### microbench_all_reduce_8npus_1MB.log

| NPU | Total Cycles |
|-----|-------------|
| 4 | 57,426 |
| 5 | 57,426 |
| 6 | 57,426 |
| 7 | 57,426 |
| 0 | 57,426 |
| 1 | 57,426 |
| 2 | 57,426 |
| 3 | 57,426 |

**Average:** 57,426 cycles
**Max:** 57,426 cycles
**Min:** 57,426 cycles

**Raw output (first 10 lines):**
```
[2026-02-11 23:31:08.708] [workload] [info] sys[4] finished, 57426 cycles, exposed communication 57426 cycles.
[2026-02-11 23:31:08.708] [statistics] [info] sys[4], Wall time: 57426
[2026-02-11 23:31:08.708] [statistics] [info] sys[4], Comm time: 57426
[2026-02-11 23:31:08.708] [workload] [info] sys[5] finished, 57426 cycles, exposed communication 57426 cycles.
[2026-02-11 23:31:08.708] [statistics] [info] sys[5], Wall time: 57426
[2026-02-11 23:31:08.708] [statistics] [info] sys[5], Comm time: 57426
[2026-02-11 23:31:08.708] [workload] [info] sys[6] finished, 57426 cycles, exposed communication 57426 cycles.
[2026-02-11 23:31:08.708] [statistics] [info] sys[6], Wall time: 57426
[2026-02-11 23:31:08.708] [statistics] [info] sys[6], Comm time: 57426
[2026-02-11 23:31:08.708] [workload] [info] sys[7] finished, 57426 cycles, exposed communication 57426 cycles.
```

### resnet50_full.log

| NPU | Total Cycles |
|-----|-------------|
| 0 | 1,098,621,886 |
| 1 | 1,098,621,886 |
| 2 | 1,098,621,886 |
| 3 | 1,098,621,886 |
| 4 | 1,098,621,886 |
| 5 | 1,098,621,886 |
| 6 | 1,098,621,886 |
| 7 | 1,098,621,886 |
| 0 | 1,098,621,886 |
| 1 | 1,098,621,886 |
| 2 | 1,098,621,886 |
| 3 | 1,098,621,886 |
| 4 | 1,098,621,886 |
| 5 | 1,098,621,886 |
| 6 | 1,098,621,886 |
| 7 | 1,098,621,886 |
| 0 | 1,096,768,270 |
| 1 | 1,096,768,270 |
| 2 | 1,096,768,270 |
| 3 | 1,096,768,270 |
| 0 | 1,098,621,886 |
| 1 | 1,098,621,886 |
| 2 | 1,098,621,886 |
| 3 | 1,098,621,886 |
| 4 | 1,098,621,886 |
| 5 | 1,098,621,886 |
| 6 | 1,098,621,886 |
| 7 | 1,098,621,886 |
| 4 | 57,426 |
| 5 | 57,426 |
| 6 | 57,426 |
| 7 | 57,426 |
| 0 | 57,426 |
| 1 | 57,426 |
| 2 | 57,426 |
| 3 | 57,426 |
| 0 | 57,426 |
| 1 | 57,426 |
| 2 | 57,426 |
| 3 | 57,426 |
| 0 | 57,426 |
| 1 | 57,426 |
| 2 | 57,426 |
| 3 | 57,426 |
| 0 | 57,426 |
| 1 | 57,426 |
| 2 | 57,426 |
| 3 | 57,426 |
| 5 | 1,098,621,886 |
| 6 | 1,098,621,886 |
| 7 | 1,098,621,886 |
| 5 | 1,098,621,886 |
| 6 | 1,098,621,886 |
| 7 | 1,098,621,886 |
| 1 | 1,096,768,270 |
| 2 | 1,096,768,270 |
| 3 | 1,096,768,270 |
| 5 | 1,098,621,886 |
| 6 | 1,098,621,886 |
| 7 | 1,098,621,886 |

**Average:** 732,217,477 cycles
**Max:** 1,098,621,886 cycles
**Min:** 57,426 cycles

**Raw output (first 10 lines):**
```
[2026-02-11 23:31:08.383] [workload] [info] sys[0] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.383] [statistics] [info] sys[0], Wall time: 1098621886
[2026-02-11 23:31:08.383] [statistics] [info] sys[0], Comm time: 3307886
[2026-02-11 23:31:08.383] [statistics] [info] sys[0], GPU time: 1095314000
[2026-02-11 23:31:08.383] [workload] [info] sys[1] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.383] [statistics] [info] sys[1], Wall time: 1098621886
[2026-02-11 23:31:08.383] [statistics] [info] sys[1], Comm time: 3307886
[2026-02-11 23:31:08.383] [statistics] [info] sys[1], GPU time: 1095314000
[2026-02-11 23:31:08.383] [workload] [info] sys[2] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.383] [statistics] [info] sys[2], Wall time: 1098621886
```

### resnet50_hgx-h100-validated_16npus.log

| NPU | Total Cycles |
|-----|-------------|
| 0 | 1,098,621,886 |
| 1 | 1,098,621,886 |
| 2 | 1,098,621,886 |
| 3 | 1,098,621,886 |
| 4 | 1,098,621,886 |
| 5 | 1,098,621,886 |
| 6 | 1,098,621,886 |
| 7 | 1,098,621,886 |

**Average:** 1,098,621,886 cycles
**Max:** 1,098,621,886 cycles
**Min:** 1,098,621,886 cycles

**Raw output (first 10 lines):**
```
[2026-02-11 23:31:08.439] [workload] [info] sys[0] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.439] [statistics] [info] sys[0], Wall time: 1098621886
[2026-02-11 23:31:08.439] [statistics] [info] sys[0], Comm time: 3307886
[2026-02-11 23:31:08.439] [statistics] [info] sys[0], GPU time: 1095314000
[2026-02-11 23:31:08.439] [workload] [info] sys[1] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.439] [statistics] [info] sys[1], Wall time: 1098621886
[2026-02-11 23:31:08.439] [statistics] [info] sys[1], Comm time: 3307886
[2026-02-11 23:31:08.439] [statistics] [info] sys[1], GPU time: 1095314000
[2026-02-11 23:31:08.439] [workload] [info] sys[2] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.439] [statistics] [info] sys[2], Wall time: 1098621886
```

### resnet50_hgx-h100-validated_4npus.log
No cycle counts extracted.

### resnet50_hgx-h100-validated_8npus.log

| NPU | Total Cycles |
|-----|-------------|
| 0 | 1,098,621,886 |
| 1 | 1,098,621,886 |
| 2 | 1,098,621,886 |
| 3 | 1,098,621,886 |
| 4 | 1,098,621,886 |
| 5 | 1,098,621,886 |
| 6 | 1,098,621,886 |
| 7 | 1,098,621,886 |

**Average:** 1,098,621,886 cycles
**Max:** 1,098,621,886 cycles
**Min:** 1,098,621,886 cycles

**Raw output (first 10 lines):**
```
[2026-02-11 23:31:08.383] [workload] [info] sys[0] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.383] [statistics] [info] sys[0], Wall time: 1098621886
[2026-02-11 23:31:08.383] [statistics] [info] sys[0], Comm time: 3307886
[2026-02-11 23:31:08.383] [statistics] [info] sys[0], GPU time: 1095314000
[2026-02-11 23:31:08.383] [workload] [info] sys[1] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.383] [statistics] [info] sys[1], Wall time: 1098621886
[2026-02-11 23:31:08.383] [statistics] [info] sys[1], Comm time: 3307886
[2026-02-11 23:31:08.383] [statistics] [info] sys[1], GPU time: 1095314000
[2026-02-11 23:31:08.383] [workload] [info] sys[2] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.383] [statistics] [info] sys[2], Wall time: 1098621886
```

### resnet50_hgx_h100_16gpu_8npus.log
No cycle counts extracted.

### resnet50_hgx_h100_32gpu_8npus.log
No cycle counts extracted.

### resnet50_hgx_h100_4gpu_4npus.log

| NPU | Total Cycles |
|-----|-------------|
| 0 | 1,096,768,270 |
| 1 | 1,096,768,270 |
| 2 | 1,096,768,270 |
| 3 | 1,096,768,270 |

**Average:** 1,096,768,270 cycles
**Max:** 1,096,768,270 cycles
**Min:** 1,096,768,270 cycles

**Raw output (first 10 lines):**
```
[2026-02-11 23:31:08.598] [workload] [info] sys[0] finished, 1096768270 cycles, exposed communication 1454270 cycles.
[2026-02-11 23:31:08.598] [statistics] [info] sys[0], Wall time: 1096768270
[2026-02-11 23:31:08.598] [statistics] [info] sys[0], Comm time: 1454270
[2026-02-11 23:31:08.598] [statistics] [info] sys[0], GPU time: 1095314000
[2026-02-11 23:31:08.598] [workload] [info] sys[1] finished, 1096768270 cycles, exposed communication 1454270 cycles.
[2026-02-11 23:31:08.598] [statistics] [info] sys[1], Wall time: 1096768270
[2026-02-11 23:31:08.598] [statistics] [info] sys[1], Comm time: 1454270
[2026-02-11 23:31:08.598] [statistics] [info] sys[1], GPU time: 1095314000
[2026-02-11 23:31:08.598] [workload] [info] sys[2] finished, 1096768270 cycles, exposed communication 1454270 cycles.
[2026-02-11 23:31:08.598] [statistics] [info] sys[2], Wall time: 1096768270
```

### resnet50_hgx_h100_8gpu_8npus.log

| NPU | Total Cycles |
|-----|-------------|
| 0 | 1,098,621,886 |
| 1 | 1,098,621,886 |
| 2 | 1,098,621,886 |
| 3 | 1,098,621,886 |
| 4 | 1,098,621,886 |
| 5 | 1,098,621,886 |
| 6 | 1,098,621,886 |
| 7 | 1,098,621,886 |

**Average:** 1,098,621,886 cycles
**Max:** 1,098,621,886 cycles
**Min:** 1,098,621,886 cycles

**Raw output (first 10 lines):**
```
[2026-02-11 23:31:08.687] [workload] [info] sys[0] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.687] [statistics] [info] sys[0], Wall time: 1098621886
[2026-02-11 23:31:08.687] [statistics] [info] sys[0], Comm time: 3307886
[2026-02-11 23:31:08.687] [statistics] [info] sys[0], GPU time: 1095314000
[2026-02-11 23:31:08.687] [workload] [info] sys[1] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.687] [statistics] [info] sys[1], Wall time: 1098621886
[2026-02-11 23:31:08.687] [statistics] [info] sys[1], Comm time: 3307886
[2026-02-11 23:31:08.687] [statistics] [info] sys[1], GPU time: 1095314000
[2026-02-11 23:31:08.687] [workload] [info] sys[2] finished, 1098621886 cycles, exposed communication 3307886 cycles.
[2026-02-11 23:31:08.687] [statistics] [info] sys[2], Wall time: 1098621886
```


## Analysis

ASTRA-sim simulates distributed training communication patterns.
The simulator models all-reduce collective operations on the specified
network topology (HGX-H100 with NVSwitch) and reports cycle counts.

**Key observations:**
- ASTRA-sim reports cycle counts, not wall-clock time
- Compute durations in the workload trace are synthetic (from v1.0 format)
- The validated accuracy claim (9.69% error for 8 GPUs) is for NCCL Ring All-Reduce microbenchmarks, not full training
- Full ResNet-50 training accuracy depends on trace fidelity
