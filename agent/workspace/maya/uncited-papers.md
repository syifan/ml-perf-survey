# Uncited Papers in references.bib

## Status
- **Total bib entries:** 60
- **Cited in paper:** 24
- **Uncited:** 36

## Uncited Papers Organized by Section Relevance

### Section 2 (Background) — Traditional Modeling & Simulation Foundations
These should be cited to strengthen the background and show historical depth.

| Key | Title | Recommendation |
|-----|-------|---------------|
| `eyeriss2016` | Eyeriss: Spatial Architecture for Energy-Efficient Dataflow | **HIGH** — Already on timeline figure but not cited in text. Must cite. |
| `simpoint2002` | SimPoint: Automatic Simulation Point Selection | **MEDIUM** — Relevant to simulation acceleration discussion |
| `smarts2003` | SMARTS: Statistical Sampling for Simulation | **MEDIUM** — Foundational sampling technique |
| `looppoint2022` | LoopPoint: Multi-threaded Sampling | **MEDIUM** — Modern extension of sampling |
| `dramsim2_2011` | DRAMSim2: Cycle-accurate Memory Simulator | **LOW** — Only if memory modeling section expands |
| `dramsim3_2020` | DRAMsim3: Thermal-capable DRAM Simulator | **LOW** — Only if memory modeling section expands |
| `ramulator2015` | Ramulator: Fast DRAM Simulator | **LOW** — Only if memory modeling section expands |
| `ramulator2_2023` | Ramulator 2.0: Modular DRAM Simulator | **LOW** — Only if memory modeling section expands |
| `papi2000` | PAPI: Hardware Performance Counter API | **MEDIUM** — Relevant to HW counters input representation (Sec 3.3.2) |
| `likwid2010` | LIKWID: Lightweight Performance Tools | **LOW** — Supporting reference for counters |
| `astrasim2020` | ASTRA-SIM v1 (original) | **LOW** — Already cite v2 (astrasim2023) |

### Section 4 (Survey) — GPU and LLM Modeling
These directly strengthen the survey coverage.

| Key | Title | Recommendation |
|-----|-------|---------------|
| `tlp2023` | TLP: Deep Learning Cost Model for Tensor Programs | **HIGH** — Already on timeline figure, not cited in text |
| `tenset2021` | TenSet: Large-scale Dataset for Tensor Compilers | **HIGH** — Referenced in text ("52M records") but not cited |
| `vllm2023` | vLLM: PagedAttention for LLM Serving | **HIGH** — Referenced in text but not cited |
| `splitwise2024` | Splitwise: Phase-split LLM Inference (ISCA Best Paper) | **HIGH** — Directly relevant to LLM serving section |
| `sarathi2024` | Sarathi-Serve: LLM Inference Scheduling | **HIGH** — Referenced in evaluation section but not cited |
| `orca2022` | ORCA: Distributed Transformer Serving | **HIGH** — Referenced in evaluation section but not cited |
| `distserve2024` | DistServe: Disaggregated LLM Serving | **MEDIUM** — Relevant to distributed LLM section |
| `paleo2017` | Paleo: DNN Performance Model | **HIGH** — Seminal early work, should be cited in background |
| `medusa2024` | MEDUSA: Multi-head LLM Decoding | **LOW** — Optimization technique, tangential |
| `flashattention2022` | FlashAttention: IO-Aware Attention | **MEDIUM** — Relevant to GPU modeling of transformers |
| `rooflinellm2024` | Roofline-Driven LLM Performance Prediction | **HIGH** — Directly relevant hybrid approach |

### Section 4 (Survey) — Recent 2025-2026 Papers
New papers that should be integrated.

| Key | Title | Recommendation |
|-----|-------|---------------|
| `dynamicreasoning2026` | Cost of Dynamic Reasoning: AI Agents (HPCA 2026) | **HIGH** — Already on timeline, directly relevant |
| `life2025` | LIFE: Hardware-Agnostic LLM Inference Forecasting | **HIGH** — Directly relevant analytical model |
| `throttllem2025` | throttLL'eM: GPU Throttling for LLM Energy | **MEDIUM** — Energy-focused, supports energy gap discussion |
| `hermes2025` | HERMES: Multi-stage AI Inference Simulator | **HIGH** — Directly relevant simulation tool |
| `frontier2025` | Frontier: MoE/Disaggregated LLM Simulator | **HIGH** — Directly relevant to distributed section |
| `omniwise2025` | Omniwise: LLM-based GPU Kernel Prediction | **HIGH** — Novel LLM-for-prediction approach |
| `swizzleperf2025` | SwizzlePerf: LLM-based GPU Optimization | **MEDIUM** — LLM-guided optimization |
| `aqua2025` | AQUA: Network-Accelerated Memory for LLMs | **LOW** — Architecture paper, not modeling |
| `podattention2025` | POD-Attention: Prefill-Decode Overlap | **LOW** — Optimization, not modeling |
| `esm2025` | ESM: Surrogate Models for HW-Aware NAS | **HIGH** — Directly relevant surrogate model work |
| `synperf2025` | SynPerf: Synthesized GPU Kernel Performance | **MEDIUM** — Related but not core |
| `chakra2023` | Chakra: Standardized Execution Traces | **MEDIUM** — Relevant to distributed modeling |
| `echo2024` | Echo: Distributed Training Simulation | **MEDIUM** — Relevant to distributed section |
| `madmax2024` | MAD Max: Distributed Model Acceleration (ISCA) | **MEDIUM** — Relevant to distributed section |

## Summary: Priority Integration List

**Must cite (HIGH priority — 15 papers):**
1. `eyeriss2016` — In timeline but uncited
2. `tlp2023` — In timeline but uncited
3. `tenset2021` — Referenced in text but uncited
4. `vllm2023` — Referenced in text but uncited
5. `splitwise2024` — ISCA Best Paper, directly relevant
6. `sarathi2024` — Referenced in evaluation but uncited
7. `orca2022` — Referenced in evaluation but uncited
8. `paleo2017` — Seminal early DNN performance model
9. `rooflinellm2024` — Hybrid roofline+ML for LLMs
10. `dynamicreasoning2026` — In timeline, HPCA 2026
11. `life2025` — Hardware-agnostic LLM modeling
12. `hermes2025` — Multi-stage inference simulator
13. `frontier2025` — MoE inference simulator
14. `omniwise2025` — LLM-based kernel prediction
15. `esm2025` — Surrogate models for NAS
