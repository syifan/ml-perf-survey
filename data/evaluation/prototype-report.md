# Unified Tool Prototype — Evaluation Report

**Generated:** 2026-02-12
**Tools:** 5
**Workloads:** 5
**Total runs:** 13
**Pass/Fail:** 12/1

## Tool Overview

| Tool | Category | Metrics |
|------|----------|---------|
| timeloop | analytical | cycles, energy_uj, utilization, latency_ms |
| analytical | analytical | latency_ms, throughput_samples_s, arithmetic_intensity, memory_gb |
| astra-sim | simulation | total_cycles, communication_cycles, compute_cycles, gpu_count |
| neusight | ml-based | latency_ms, predicted_latency_ms, ape_pct |
| vidur | simulation | avg_e2e_time_s, p50_e2e_time_s, p99_e2e_time_s, avg_ttft_s, avg_tpot_s, throughput_tokens_per_s |

## Coverage Matrix

| Workload | timeloop | analytical | astra-sim | neusight | vidur |
|----------|---|---|---|---|---|
| bert-large-inference-a100 | PASS | PASS | — | PASS | — |
| gpt3-inference-h100 | — | PASS | — | — | FAIL |
| llama2-7b-serving-a100 | — | — | — | — | PASS |
| resnet50-inference-a100 | PASS | PASS | — | PASS | — |
| resnet50-training-h100-8gpu | PASS | PASS | PASS | PASS | — |

## Per-Workload Results

### bert-large-inference-a100
**Model:** BERT-large | **Task:** inference | **Hardware:** A100

| Metric | timeloop | analytical | neusight |
|--------|---|---|---|
| ape_pct | — | — | 4.4500 |
| arithmetic_intensity | — | 851.7600 | — |
| bottleneck | — | compute | — |
| compute_time_ms | — | 1.8564 | — |
| config | — | — | bert_large-inf-512-16 |
| cycles | 1,170,773 | — | — |
| device | — | — | NVIDIA_A100-PCIE-40GB |
| energy_uj | 649.0800 | — | — |
| latency_ms | 5.8540 | 1.8564 | 396.4750 |
| memory_gb | — | 0.6800 | — |
| memory_time_ms | — | 0.3335 | — |
| predicted_latency_ms | — | — | 414.1270 |
| source | — | — | precomputed_ci |
| throughput_samples_s | — | 538.6700 | — |
| utilization | 0.6000 | — | — |

### gpt3-inference-h100
**Model:** GPT-3 | **Task:** inference | **Hardware:** H100

| Metric | analytical | vidur |
|--------|---|---|
| arithmetic_intensity | 1,000.0000 | — |
| bottleneck | compute | — |
| compute_time_ms | 353.8928 | — |
| latency_ms | 353.8928 | — |
| memory_gb | 350.0000 | — |
| memory_time_ms | 104.4776 | — |
| throughput_samples_s | 2.8300 | — |

### llama2-7b-serving-a100
**Model:** Llama-2-7b | **Task:** serving | **Hardware:** A100

| Metric | vidur |
|--------|---|
| avg_decode_tokens | 15.2100 |
| avg_e2e_time_s | 0.1703 |
| avg_exec_time_s | 0.1601 |
| avg_prefill_tokens | 293.6700 |
| avg_sched_delay_s | 0.0022 |
| avg_tpot_s | 0.0093 |
| avg_ttft_s | 0.0266 |
| num_requests | 100 |
| p50_e2e_time_s | 0.1769 |
| p99_e2e_time_s | 0.3135 |
| scheduler | vllm |
| schedulers_available | ['vllm', 'sarathi', 'orca'] |
| source | precomputed |
| throughput_tokens_per_s | 98,531.4670 |

### resnet50-inference-a100
**Model:** ResNet-50 | **Task:** inference | **Hardware:** A100

| Metric | timeloop | analytical | neusight |
|--------|---|---|---|
| arithmetic_intensity | — | 160.1600 | — |
| bottleneck | — | compute | — |
| compute_time_ms | — | 0.0263 | — |
| cycles | 1,170,773 | — | — |
| device | — | — | A100 |
| energy_uj | 649.0800 | — | — |
| latency_ms | 5.8540 | 0.0263 | — |
| mean_ape_pct | — | — | 8.6300 |
| memory_gb | — | 0.0510 | — |
| memory_time_ms | — | 0.0251 | — |
| mode | — | — | inf |
| num_models | — | — | 16 |
| source | — | — | precomputed_ci_aggregate |
| throughput_samples_s | — | 38,048.7800 | — |
| utilization | 0.6000 | — | — |

### resnet50-training-h100-8gpu
**Model:** ResNet-50 | **Task:** training | **Hardware:** H100 x8

| Metric | timeloop | analytical | astra-sim | neusight |
|--------|---|---|---|---|
| arithmetic_intensity | — | 5,125.0000 | — | — |
| bottleneck | — | compute | — | — |
| communication_cycles | — | — | 3,307,886 | — |
| compute_cycles | — | — | 1,095,314,000 | — |
| compute_time_ms | — | 0.2653 | — | — |
| cycles | 1,170,773 | — | — | — |
| device | — | — | — | H100 |
| energy_uj | 649.0800 | — | — | — |
| gpu_count | — | — | 8 | — |
| latency_ms | 5.8540 | 0.2653 | — | — |
| mean_ape_pct | — | — | — | 6.6000 |
| memory_gb | — | 0.0510 | — | — |
| memory_time_ms | — | 0.0153 | — | — |
| mode | — | — | — | train |
| npus_in_result | — | — | 8 | — |
| num_models | — | — | — | 18 |
| source | — | — | precomputed_ci | precomputed_ci_aggregate |
| throughput_samples_s | — | 3,769.0500 | — | — |
| total_cycles | — | — | 1,098,621,886 | — |
| utilization | 0.6000 | — | — | — |

## Category Analysis

- **analytical:** timeloop, analytical
- **simulation:** astra-sim, vidur
- **ml-based:** neusight
