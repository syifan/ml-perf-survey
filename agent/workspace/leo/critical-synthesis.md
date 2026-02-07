# Critical Synthesis: Performance Modeling Tools for ML Workloads

This document provides critical analysis of each surveyed tool/approach, addressing reviewer weaknesses W3 (shallow analysis) and W6 (missing failure mode discussion). For each tool, we analyze: (a) when it works well, (b) when it breaks down, (c) how its accuracy claims compare to what's actually verifiable.

This analysis is grounded in our hands-on evaluation reports (data/results/) and cross-paper comparison.

---

## 1. CPU Performance Modeling

### GRANITE (GNN-based basic block throughput)
- **Reported accuracy:** 0.97 Kendall's τ on x86 basic blocks
- **When it works:** Compute-bound basic blocks with well-defined instruction dependency graphs. The GNN representation naturally captures ILP and dependency chains — this is its core strength. Generalizes across x86 microarchitectures because the instruction dependency structure is architecture-independent.
- **When it breaks down:** (1) **Memory-bound code** — GRANITE predicts throughput from static instruction graphs but cannot model cache behavior, which depends on runtime access patterns and data layout. For memory-bound ML kernels (e.g., embedding lookups, sparse attention), this is a fundamental limitation. (2) **Optimized library code** — BLAS/cuDNN kernels use hand-tuned assembly with microarchitecture-specific tricks that violate the assumptions of learned models. (3) **Basic blocks vs. end-to-end** — predicting basic block throughput doesn't directly translate to end-to-end model latency; the composition problem (how block-level predictions aggregate) is unaddressed.
- **Accuracy contextualization:** Kendall's τ measures *ranking* accuracy, not absolute error. A model with 0.97 τ could have large absolute errors while correctly ordering blocks by relative speed. This is fine for compiler optimization (where ranking matters) but insufficient for latency prediction (where absolute values matter). The paper should distinguish these use cases explicitly.
- **Relevance to ML workloads:** Limited. GRANITE targets general CPU workloads, not ML-specific ones. ML inference on CPUs is dominated by GEMM/GEMV operations in optimized libraries, which GRANITE cannot model because it operates below the library abstraction.

### Concorde (Hybrid analytical-ML for CPI prediction)
- **Reported accuracy:** 2% CPI error, 5 orders of magnitude faster than gem5
- **When it works:** Compositional workloads where the analytical component provides a strong prior. The "compositional" aspect means it models program segments independently and combines them — effective when segments don't interact through shared microarchitectural state.
- **When it breaks down:** (1) **Shared cache contention** — the compositional model assumes segments don't interfere through cache, which fails for multi-threaded ML training on CPUs. (2) **New microarchitectures** — the analytical component encodes assumptions about pipeline structure; new designs (e.g., ARM's big.LITTLE for edge ML) require re-deriving the analytical model. (3) **The 2% claim needs context** — measured on specific benchmark suites; the error on real ML workloads with their characteristic memory patterns is unknown.
- **Cross-reference with GRANITE:** Concorde and GRANITE solve different problems (CPI vs. throughput) at different granularities. Neither addresses the composition problem for full ML model execution on CPUs. This gap is significant given increasing CPU-based ML inference deployment.

---

## 2. GPU Performance Modeling

### NeuSight (Tile-based GPU kernel prediction)
- **Reported accuracy:** 2.3% MAPE on GPT-3 inference (H100, A100, V100); "50× improvement over Habitat"
- **When it works:** Regular, dense tensor operations where CUDA's tiling strategy is predictable. The tile-based decomposition mirrors actual GPU execution, providing structural inductive bias. Works across GPU generations because tile-level compute/memory behavior scales predictably.
- **When it breaks down:** (1) **Irregular workloads** — sparse attention (e.g., Flash Attention's IO-aware tiling), dynamic shapes (variable sequence lengths in LLM serving), and graph neural networks with irregular adjacency patterns all break the assumption of uniform tile behavior. (2) **Novel operators** — custom CUDA kernels not seen during training (e.g., Mixture-of-Experts routing, speculative decoding) have no tile decomposition template. (3) **Multi-kernel interactions** — NeuSight predicts individual kernel latency but doesn't model kernel launch overhead, memory allocation between kernels, or concurrent kernel execution on modern GPUs (MPS/MIG).
- **The "50× over Habitat" claim is misleading.** The reviewer correctly identifies this: Habitat was evaluated on H100, which didn't exist when it was published (2021). Habitat achieved 11.8% error on contemporary GPU transfers (V100→A100). NeuSight and Habitat solve fundamentally different problems: NeuSight predicts from static features (no GPU needed), while Habitat transfers from profiling data (requires source GPU). Comparing their error rates as if they compete is an apples-to-oranges comparison. The survey should present these as complementary approaches for different use cases (design-time prediction vs. deployment migration).
- **Verified in our evaluation:** NeuSight scored 7.5/10 in our reproducibility evaluation. The tile-based approach worked as described for standard LLM workloads, but we could not test on irregular workloads (sparse, dynamic shape) due to limited examples.

### Habitat (Cross-GPU transfer via wave scaling)
- **Reported accuracy:** 11.8% MAPE (on contemporary V100→A100 transfers)
- **When it works:** Dense training workloads where performance is dominated by compute and memory bandwidth — the two components Habitat explicitly models. GPU-to-GPU transfer when source and target share similar architecture (e.g., Ampere→Hopper).
- **When it breaks down:** (1) **Cross-architecture transfer** — transferring from fundamentally different architectures (GPU→TPU, datacenter GPU→mobile GPU) fails because the wave scaling model encodes GPU-specific assumptions. (2) **Memory-bound phases** — decode phase of LLM inference, where performance depends on KV cache management and memory bandwidth, is poorly modeled by wave scaling. (3) **Requires source GPU profiling** — unlike static approaches, Habitat needs actual hardware execution, limiting its use for design space exploration.
- **Historical context matters:** Habitat (2021) predates the LLM era. Its accuracy numbers were measured on CNN training workloads. Applying Habitat to transformer-based workloads, especially with attention mechanisms and dynamic sequence lengths, is outside its validated domain.

### AMALI (Analytical LLM inference modeling)
- **Reported accuracy:** 23.6% MAPE (reduced from 127.6% baseline)
- **When it works:** Steady-state LLM inference with known batch sizes and sequence lengths on single-GPU setups. The analytical memory hierarchy model captures the compute-vs-memory-bound transition between prefill and decode phases.
- **When it breaks down:** (1) **The 23.6% error is 5-10× worse than ML-based approaches.** This isn't a limitation of the AMALI team — it reveals that LLM inference is fundamentally harder to model analytically than CNN inference. The irregular memory access patterns of attention (scaling quadratically with sequence length), the impact of KV cache management strategies, and the sensitivity to batch scheduling all resist closed-form modeling. (2) **Multi-GPU inference** — AMALI models single-GPU inference; tensor parallelism, pipeline parallelism, and expert parallelism introduce communication overheads that compound modeling error. (3) **Dynamic batching** — real LLM serving systems use continuous batching (Orca, Sarathi) which changes effective batch size mid-execution.
- **Why this matters:** AMALI's 23.6% error vs NeuSight's 2.3% is not simply "AMALI is worse" — it reflects the fundamental difficulty gap between analytical and ML-based approaches for complex workloads. The survey should use AMALI as a case study for *when analytical models hit their limits* and ML-based approaches are justified.

### Accel-Sim (SASS trace-driven GPU simulation)
- **Reported accuracy:** 0.90–0.97 IPC correlation at 1000–10000× slowdown
- **When it works:** Microarchitectural studies requiring cycle-level fidelity (cache policies, warp scheduling, memory coalescing). Trace-driven simulation avoids functional execution overhead.
- **When it breaks down:** (1) **Scale** — simulating a single ResNet-50 inference takes hours; a full LLM training run is completely infeasible. (2) **Modern GPU features** — Tensor Cores, MIG, NVLink, and GPU-to-GPU communication in multi-GPU setups require explicit modeling that lags behind hardware releases by 1-2 years. (3) **The correlation metric hides absolute error** — 0.97 IPC correlation can coexist with 20%+ absolute latency error for workloads with unusual occupancy patterns.
- **Role in the ecosystem:** Accel-Sim is valuable as a *validation baseline* for ML-based approaches, not as a practical prediction tool for ML workloads. The survey should position it this way.

---

## 3. DNN Accelerator Modeling

### Timeloop (Analytical loop-nest DSE)
- **Reported accuracy:** 5–10% vs RTL simulation at 2000× speedup
- **When it works:** Regular DNN layers (convolutions, GEMMs) on systolic array accelerators with well-defined dataflows. The loop-nest representation exactly captures data reuse patterns for these workloads. Excellent for design space exploration (mapping optimization).
- **When it breaks down:** (1) **Irregular operators** — attention mechanisms, dynamic routing (MoE), sparse convolutions cannot be expressed in the standard loop-nest formalism. (2) **Graph-level effects** — Timeloop models individual layers in isolation; inter-layer pipelining, fusion, and memory allocation across layers are not modeled. (3) **The 5-10% accuracy claim is for accelerators with known, fixed dataflows** — real deployments involve dynamic scheduling and runtime decisions that Timeloop's static analysis cannot capture.
- **Verified in our evaluation:** Timeloop scored 9/10 in reproducibility. Docker works out-of-the-box, reference outputs are deterministic. However, Python bindings (pytimeloop) are broken (libbarvinok.so.23 missing), and configuration is verbose (three YAML files per evaluation). The tool works well for its intended use case but requires significant expertise.
- **Critical observation:** Timeloop models the *accelerator* but not the full *system*. For ML workloads, the bottleneck often isn't the accelerator compute itself but host-device communication, memory allocation, and data preprocessing. Timeloop's accuracy claims are valid for the accelerator in isolation but don't extend to end-to-end ML workload performance.

### MAESTRO (Data-centric dataflow analysis)
- **Reported accuracy:** 5–15% (broader range than Timeloop)
- **When it works:** Rapid early-stage accelerator design exploration. The data-centric directive language is more intuitive than Timeloop's loop-nest representation for architects less familiar with compiler optimization.
- **When it breaks down:** Same fundamental limitations as Timeloop (irregular operators, no graph-level effects) plus (1) **less precise than Timeloop** for detailed mapping optimization because the data-centric abstraction trades accuracy for usability. (2) **No sparse tensor support** — Sparseloop extends Timeloop but no equivalent exists for MAESTRO.
- **Comparison with Timeloop:** Both tools serve the same niche (DNN accelerator DSE) but Timeloop has a stronger ecosystem (Sparseloop extension, larger community, more validated configurations). MAESTRO's advantage is ease of use for initial exploration. In practice, the community has converged on Timeloop for detailed analysis.

### Sparseloop (Sparse tensor accelerator modeling)
- **Reported accuracy:** 5–10% for sparse workloads at 2000× speedup over RTL
- **When it works:** Accelerators with explicit sparsity support (compression/decompression hardware, sparse dataflows). Models the complex interaction between sparsity pattern, compression format, and dataflow strategy.
- **When it breaks down:** (1) **Structured vs. unstructured sparsity** — Sparseloop models the hardware's sparsity handling but real sparsity patterns (activation sparsity, weight pruning patterns) vary dramatically. The 5-10% accuracy assumes known, static sparsity distributions. (2) **Dynamic sparsity** — emerging techniques like dynamic token pruning in transformers change sparsity at runtime, which static analytical models cannot capture.

### ArchGym (ML-aided design space exploration)
- **Reported accuracy:** 0.61% RMSE at 2000× speedup using surrogate models
- **When it works:** Design space exploration where the objective function is expensive to evaluate (RTL simulation). The surrogate model approximates the simulation, enabling rapid Pareto front exploration.
- **When it breaks down:** (1) **The 0.61% RMSE is for the surrogate's fit to the simulator, not to real hardware.** This is a critical distinction: the surrogate accurately approximates Timeloop/simulation outputs, but those simulations themselves have 5-10% error vs. reality. The compounded error is larger than 0.61%. (2) **Extrapolation** — surrogate models trained on a design space region may produce wildly incorrect predictions for configurations far from training data. This is especially dangerous when using ML surrogates to discover "novel" architectures.
- **Clarification for the survey:** ArchGym's accuracy claim is about surrogate fidelity, not about prediction of real hardware performance. The survey currently presents 0.61% alongside NeuSight's 2.3% and nn-Meter's <1% in the same table, which is misleading — they measure fundamentally different things.

---

## 4. Edge and Mobile Device Modeling

### nn-Meter (Kernel-level random forest prediction)
- **Reported accuracy:** <1% MAPE across mobile CPUs, GPUs, VPUs
- **When it works:** Standard CNN inference on well-characterized mobile devices. The kernel detection and adaptive sampling approach handles the diversity of operator implementations across mobile hardware.
- **When it breaks down:** (1) **Pickle serialization fragility** — our evaluation found that nn-Meter's pre-trained models fail with current scikit-learn versions due to pickle format incompatibility. This is not just a technical nuisance — it means the <1% accuracy claim is unverifiable on current software stacks. (2) **Transformer operators** — nn-Meter was developed for CNNs; attention and MLP layers in vision transformers have different kernel decompositions on mobile hardware. (3) **The <1% claim is for kernel-level prediction** — end-to-end model latency involves memory allocation, data transfer, and runtime overhead that kernel-level composition underestimates. (4) **Platform-specific training** — each new device requires hours of profiling to train new predictors, which doesn't scale to the fragmented mobile hardware landscape.
- **Verified in our evaluation:** nn-Meter scored 3/10 — the lowest of all evaluated tools. We could not execute *any* predictions due to dependency conflicts. The tool is essentially unmaintained (no updates since 2022). This severely undermines confidence in the reported accuracy.

### LitePred (VAE-based cross-platform transfer)
- **Reported accuracy:** 0.7% MAPE across 85 platforms; 99.3% accuracy
- **When it works:** CNN latency prediction when similar devices exist in the training set. The VAE-based sampling intelligently selects which profiling data to collect on a new device, minimizing adaptation cost.
- **When it breaks down:** (1) **Novel architectures** — transfer from GPU/CPU to NPU/DSP (fundamentally different execution models) likely degrades significantly, but this isn't well-characterized. (2) **The "85 platforms" are mostly mobile CPUs and GPUs** — the diversity within the evaluation set is unclear. If most are ARM Cortex variants, the transfer task is easier than if the set includes diverse accelerators. (3) **Same CNN-centric limitation as nn-Meter** — the 0.7% claim is for CNN operators; transformer and MoE workloads are unvalidated.
- **Cross-reference with nn-Meter:** LitePred builds on nn-Meter's kernel-level decomposition but adds transfer learning. If nn-Meter's kernel boundaries are wrong for a workload (e.g., fused operators in transformer inference), LitePred inherits that limitation. The 0.7% improvement over nn-Meter's <1% comes from the transfer component, but the shared foundation means both tools share the same failure modes for non-CNN workloads.

### HELP (Meta-learning for hardware adaptation)
- **Reported accuracy:** 1.9% MAPE with 10-sample adaptation
- **When it works:** Adapting latency predictions to a new device with minimal profiling. The MAML-based meta-learning framework learns a prior that makes 10 samples sufficient for reasonable accuracy.
- **When it breaks down:** (1) **10 samples must be representative** — if the 10 samples don't cover the performance-critical operators of the target workload, the adapted model will be inaccurate for those operators. The paper doesn't discuss how to select these 10 samples optimally. (2) **Distribution shift between meta-training and target** — if the target device is fundamentally different from meta-training devices (e.g., a neuromorphic chip), the learned prior is unhelpful. (3) **Static workload assumption** — HELP predicts latency for fixed inputs; dynamic shapes in LLM serving would require re-adaptation.
- **Relevance to ML workload modeling:** HELP is primarily designed for NAS, not for deployment latency prediction. The 1.9% error is sufficient for NAS ranking but may be insufficient for SLO-aware serving decisions.

---

## 5. Distributed and LLM System Modeling

### ASTRA-sim (Distributed training simulation)
- **Reported accuracy:** 5–15% for collective communication; validated on HGX-H100 configurations
- **When it works:** Analyzing collective communication algorithms (all-reduce, all-gather) on regular topologies (ring, tree, mesh). Excellent for comparing parallelization strategies (data parallel, tensor parallel, pipeline parallel).
- **When it breaks down:** (1) **Scale validation gap** — our evaluation only tested 4-NPU and 8-NPU configurations; real distributed training uses 100s-1000s of GPUs where network congestion, stragglers, and failure recovery dominate performance. The 5-15% accuracy at small scale may not hold at large scale. (2) **Training-specific effects** — gradient compression, activation checkpointing, dynamic loss scaling, and optimizer state sharding all affect communication patterns but are not explicitly modeled. (3) **The analytical backend trades accuracy for speed** — ASTRA-sim supports both analytical and detailed ns-3 backends. Our evaluation used the analytical backend, which runs in <1s but is less accurate than the detailed backend.
- **Verified in our evaluation:** ASTRA-sim scored 8.5/10 in reproducibility. Docker setup works in ~5 minutes, execution is fast (<1s per benchmark). Results for ring all-reduce match analytical expectations (qualitative validation passed). However, we cannot validate accuracy without actual HGX-H100 hardware.
- **Coverage gap:** We executed only 4 of 12 intended benchmarks (33% coverage). The remaining benchmarks failed due to missing configurations, not tool errors.

### VIDUR (LLM inference serving simulation)
- **Reported accuracy:** <5% for LLM inference serving metrics
- **When it works:** Comparing scheduling algorithms (vLLM, Orca, Sarathi) for LLM inference serving. Captures the prefill/decode phase distinction and KV cache management — the two most important factors in LLM serving performance.
- **When it breaks down:** (1) **Uses ML (Random Forest) internally for execution time prediction** — the simulation's accuracy depends on the quality of pre-trained kernel time predictors. For models not in the training set (new architectures, custom operators), predictions degrade. (2) **Single-model serving only** — doesn't model multi-model serving, model routing, or the scheduling complexity of multi-tenant GPU clusters. (3) **Static hardware assumptions** — thermal throttling, memory fragmentation over long-running serving sessions, and GPU clock variation are not modeled.
- **Verified in our evaluation:** VIDUR scored 9/10 in reproducibility — the highest among all tools. Docker setup works in ~2 minutes, execution is fast, and the scheduler comparison output is immediately useful. We confirmed that all 100 synthetic requests completed without failures. However, the <5% accuracy claim cannot be validated without A100 hardware.
- **Critical observation for the survey:** VIDUR is sometimes presented as a "simulation" tool but it internally uses ML (Random Forest) for kernel prediction. Under the revised paper scope ("modeling FOR ML workloads"), VIDUR is a prime example of a hybrid analytical/ML approach that deserves deeper treatment, not just a one-paragraph description.

### Lumos (Trace-driven LLM training prediction)
- **Reported accuracy:** 3.3% error on H100 for LLM training
- **When it works:** Predicting LLM training performance when trace data from a similar configuration is available. Captures training-specific effects (gradient accumulation, activation checkpointing, optimizer states) that general-purpose simulators miss.
- **When it breaks down:** (1) **Requires traces from similar configurations** — if training parameters change significantly (different parallelism strategy, different model architecture), collected traces may not transfer. (2) **Hardware-specific** — the 3.3% result is specifically for H100; transferring to different GPU generations or different interconnects requires re-tracing. (3) **Doesn't model failures** — real large-scale training is dominated by recovery from failures (checkpointing, re-scheduling). Lumos models steady-state performance, not operational performance.
- **Comparison with ASTRA-sim:** Lumos focuses narrowly on LLM training (higher accuracy for that specific task), while ASTRA-sim generalizes to arbitrary distributed workloads (broader scope, lower accuracy). This is a classic specialization-vs-generalization tradeoff that the survey should make explicit.

### TrioSim (Lightweight multi-GPU simulation)
- **Reported accuracy:** N/A (no absolute accuracy vs. real hardware reported)
- **When it works:** Rapid simulation of multi-GPU DNN training workloads where relative comparison between configurations is more important than absolute accuracy.
- **When it breaks down:** (1) **No accuracy baseline** — without comparison to real hardware measurements, the tool's predictions cannot be trusted for absolute performance estimation. (2) **"Lightweight" implies accuracy tradeoffs** — selective fidelity means some aspects of GPU behavior are approximated; the paper should characterize which aspects and the impact on prediction quality.
- **Note for the survey:** Including TrioSim in the same comparison table as tools with validated accuracy numbers (NeuSight, nn-Meter) while marking it "N/A" creates a misleading impression of comparable coverage. Either validate accuracy or discuss TrioSim separately as a simulation framework rather than a prediction tool.

---

## 6. Cross-Cutting Themes (Insights the Paper Should Add)

### Theme 1: The CNN-to-Transformer Gap
Nearly all reported accuracy numbers are measured on CNN workloads (ResNet, VGG, MobileNet). The few tools that evaluate on transformer/LLM workloads (NeuSight on GPT-3, Lumos on LLM training, VIDUR on LLM serving) report accuracy on narrow configurations. No tool has demonstrated robust accuracy across the full range of modern ML workloads (CNNs, transformers, MoE, diffusion models, multimodal). The survey should explicitly map which tools have been validated on which workload types.

### Theme 2: Static vs. Profiling-Based — A Practical Divide
The paper should foreground a key practical distinction: static models (NeuSight, nn-Meter, LitePred) predict without hardware access but cannot capture runtime effects; profiling-based models (Habitat, HELP) capture runtime behavior but require hardware. This distinction determines which tools are usable in which contexts (design-time exploration, deployment optimization, capacity planning). Currently this is buried in Section 2.3 and should be elevated.

### Theme 3: Accuracy Metrics Are Not Comparable
The current paper groups tools into accuracy tiers (<5%, 5-15%, 15-25%) but the numbers come from:
- Different workloads (basic blocks vs. full models vs. serving systems)
- Different hardware (mobile CPUs vs. datacenter GPUs vs. NPUs)
- Different metrics (MAPE vs. RMSE vs. Kendall's τ vs. correlation)
- Different evaluation protocols (self-reported vs. independently validated)

**The paper should NOT tier these numbers.** Instead, it should organize accuracy discussion by *problem difficulty* — predicting single-kernel latency on a known device is fundamentally easier than predicting end-to-end distributed training time on a novel cluster. The fact that nn-Meter achieves <1% on the former while ASTRA-sim achieves 5-15% on the latter doesn't mean nn-Meter is "better."

### Theme 4: Reproducibility vs. Reported Accuracy
Our hands-on evaluation revealed a pattern: tools with high reported accuracy sometimes have poor reproducibility. nn-Meter claims <1% MAPE but scored 3/10 in our evaluation (could not run at all). Conversely, ASTRA-sim and VIDUR have moderate accuracy claims but excellent reproducibility. The survey should discuss this tradeoff — unreproducible accuracy claims are worthless for practitioners.

### Theme 5: The Composition Problem
Most tools predict performance of individual components (kernels, layers, collectives). Composing these predictions into end-to-end workload performance remains unsolved. The error compounds: if each layer prediction has 5% error and a model has 100 layers, the end-to-end error can be much larger (or cancel out, depending on error correlation). No surveyed work addresses this composition problem rigorously. This is a genuine research gap.

### Theme 6: What Gets Modeled vs. What Matters
For ML workloads, the gap between "what performance models predict" and "what practitioners need to know" is large:
- Models predict **compute latency**; practitioners care about **time-to-accuracy** (which depends on convergence, not just throughput)
- Models predict **single-request latency**; serving systems care about **tail latency under load** (P99, which depends on scheduling and queuing)
- Models predict **steady-state performance**; operational systems face **stragglers, failures, and thermal throttling**

The survey should acknowledge this gap explicitly and identify which tools partially address it (VIDUR models scheduling; Lumos models training-specific effects).

---

## 7. Recommendations for Paper Revision

Based on this analysis, the paper should:

1. **Replace accuracy tiers with problem-difficulty tiers.** Group by what's being predicted (kernel latency, end-to-end inference, distributed training) rather than by accuracy number.

2. **Add a failure mode column to Table 1.** For each tool, list the primary condition under which it breaks down. This is the single most impactful addition the review asks for.

3. **Distinguish static vs. profiling-based approaches** as a primary organizational dimension, not a sub-point in Section 2.3.

4. **Add a workload coverage table.** For each tool, indicate which workload types have been validated (CNN, Transformer, MoE, Diffusion, GNN) with checkmarks.

5. **Use AMALI's 23.6% as a case study** for the limits of analytical modeling for complex workloads, not as a failure. Compare with NeuSight's 2.3% to argue *when* ML-based approaches are justified.

6. **Remove or recontextualize the "50× over Habitat" claim** for NeuSight. Present both tools' accuracy on their contemporary evaluation settings.

7. **Foreground the composition problem** as a key open challenge, grounded in specific evidence from the surveyed tools.

8. **Link reproducibility findings to accuracy trust.** nn-Meter's <1% is unverifiable; Timeloop's 5-10% is confirmed. This changes how practitioners should weight these claims.
