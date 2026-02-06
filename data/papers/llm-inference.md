# LLM Inference Performance Modeling Papers

Literature focused on LLM-specific performance models, serving systems, attention optimization, KV cache management, and scheduling (2022-2025).

## Summary Table

| Paper | Authors | Year | Venue | Focus | Key Contribution |
|-------|---------|------|-------|-------|------------------|
| vLLM/PagedAttention | Kwon et al. | 2023 | SOSP | Memory | PagedAttention for KV cache, 2-4x throughput |
| Orca | Yu et al. | 2022 | OSDI | Scheduling | Pioneered continuous/iteration-level batching |
| Llumnix | Sun et al. | 2024 | OSDI | Scheduling | Live migration, 10x tail latency improvement |
| DistServe | Zhong et al. | 2024 | OSDI | Architecture | Disaggregate prefill/decode, 7.4x more requests |
| Sarathi-Serve | Agrawal et al. | 2024 | OSDI | Scheduling | Chunked prefills, stall-free batching |
| Parrot | Lin et al. | 2024 | OSDI | Applications | Semantic variables for LLM app serving |
| Jenga | Various | 2025 | SOSP | Memory | Heterogeneous memory for KV cache |
| FlashInfer | Ye et al. | 2025 | MLSys | Attention | 29-69% ITL reduction, customizable kernels |
| VIDUR | Agrawal et al. | 2024 | MLSys | Simulation | LLM inference simulator, <5% error |
| FlashAttention | Dao et al. | 2022 | NeurIPS | Attention | IO-aware attention, linear memory |
| FlashAttention-2 | Dao | 2024 | ICLR | Attention | 2x speedup, 50-73% utilization on A100 |
| FlashAttention-3 | Shah et al. | 2024 | arXiv | Attention | 1.5-2x on H100, FP8 support, 85% util |
| Oaken | Park et al. | 2025 | ISCA | KV Cache | Online-offline hybrid quantization |
| ALISA | Various | 2024 | ISCA | KV Cache | Sparsity-aware KV caching |
| MorphKV | Various | 2025 | arXiv | KV Cache | Attention-based token selection, 50% savings |
| MagicDec | Various | 2025 | ICLR | Speculative | Bottleneck-aware drafting strategy |
| EAGLE-3 | Li et al. | 2024 | NeurIPS | Speculative | Lightweight prediction head, no draft model |
| MEDUSA | Cai et al. | 2024 | ICML | Speculative | Multiple decoding heads, 2.2-3.6x speedup |
| Roofline-LLM | Imai et al. | 2024 | NeurIPS-WS | Prediction | Roofline + ML, 87% MSE reduction |
| SpotServe | Various | 2024 | ASPLOS | Distributed | Serving on preemptible instances |
| SuperServe | Various | 2025 | NSDI | Scheduling | Fine-grained serving for variable workloads |

## Categorization by Focus Area

### 1. Foundational Serving Systems

- **vLLM/PagedAttention** (SOSP 2023) - Foundational work
  - PagedAttention inspired by OS virtual memory
  - Near-zero KV cache memory waste
  - Flexible sharing within and across requests
  - 2-4x throughput improvement over FasterTransformer/Orca

- **Orca** (OSDI 2022) - Continuous batching pioneer
  - Iteration-level scheduling (vs request-level)
  - Foundation for all modern LLM serving systems
  - Allows new requests to join batches mid-generation

### 2. Scheduling & Resource Management (OSDI/SOSP 2024-2025)

- **Llumnix** (OSDI 2024) - Dynamic scheduling
  - Live migration of requests across model instances
  - 10x tail latency improvement
  - 1.5x acceleration for high-priority requests
  - 36% cost savings at similar tail latency

- **DistServe** (OSDI 2024) - Disaggregated serving
  - Separate GPUs for prefill vs decode phases
  - Eliminates prefill-decode interference
  - 7.4x more requests OR 12.6x tighter SLO

- **Sarathi-Serve** (OSDI 2024) - Chunked prefills
  - Divides prefill into equal-sized chunks
  - Decode-maximal batching (prefill chunk + decode requests)
  - Stall-free execution
  - 1.25x throughput improvement

- **Jenga** (SOSP 2025) - Heterogeneous memory
  - Extends PagedAttention for heterogeneous memory
  - CXL, NVMe integration for KV cache

### 3. Attention Mechanism Optimization

- **FlashAttention** (NeurIPS 2022) - IO-aware attention
  - Memory linear in sequence length (vs quadratic)
  - 10-20x memory savings at long sequences
  - Exact attention (not approximate)

- **FlashAttention-2** (ICLR 2024) - Better parallelism
  - 2x speedup over FlashAttention
  - 50-73% theoretical max FLOPs on A100
  - 35% utilization on H100 (room for improvement)

- **FlashAttention-3** (2024) - Hopper optimization
  - 1.5-2x speedup on H100 GPUs
  - 75-85% utilization with BF16
  - FP8 support: 1.2-1.3 PFLOPs/s
  - 2.6x lower numerical error vs baseline FP8

- **FlashInfer** (MLSys 2025) - Customizable engine
  - 29-69% inter-token-latency reduction
  - 28-30% latency reduction for long-context
  - Customizable attention kernels

### 4. KV Cache Optimization

- **Oaken** (ISCA 2025) - Hybrid quantization
  - Online-offline hybrid approach
  - Data-agnostic outlier thresholds determined offline
  - Quantization loss mitigation technique

- **ALISA** (ISCA 2024) - Sparsity-aware
  - Layer-specific scheduling
  - Hierarchical KV cache management
  - Exploits attention sparsity patterns

- **MorphKV** (2025) - Adaptive selection
  - Fixed-size KV cache via attention patterns
  - Iteratively refines which tokens to keep
  - >50% memory savings

- **MIRAGE** (2025) - Multi-tenant optimization
  - Per-layer dynamic KV cache sizing
  - Automatic elastic adjustment
  - Optimized for multi-tenant serving

### 5. Speculative Decoding

- **MEDUSA** (ICML 2024) - Multiple heads
  - Parallel decoding heads attached to LLM
  - No separate draft model needed
  - 2.2-3.6x speedup without quality loss

- **EAGLE-3** (NeurIPS 2024) - Lightweight prediction
  - Autoregressive prediction head on internal layers
  - Eliminates separate draft model
  - Improved acceptance rates

- **MagicDec** (ICLR 2025) - Bottleneck-aware
  - KV compression > model compression for acceptance rate
  - More prominent in high batch/long context
  - General formulation for drafting strategy selection

- **EDD** (ACL 2025) - Effective draft decoder
  - LLM as encoder
  - Hidden state as soft prompt for drafts
  - Autoregressive draft generation

### 6. Performance Prediction & Cost Models

- **VIDUR** (MLSys 2024) - LLM inference simulation
  - Discrete-event simulation framework
  - <5% prediction error
  - Open-source, extensible
  - Models serving system behavior

- **Roofline-LLM** (NeurIPS-WS 2024) - Analytical + ML
  - Roofline model extended for LLM inference
  - Interpretable performance ceiling
  - 17 point R² increase over baselines
  - 87% MSE reduction

- **SOLA** (2024) - SLO optimization
  - Fine-grained iteration-level scheduling
  - Dynamic workload tuning
  - Explicit SLO modeling

- **ReaLLM** (2025) - Trace-driven prediction
  - Kernel-level simulation
  - More accurate than simple linear models
  - Addresses limitations of peak-FLOPS-based prediction

### 7. Distributed Inference

- **SpotServe** (ASPLOS 2024) - Preemptible instances
  - Graceful handling of spot instance preemption
  - Cost-effective LLM serving
  - State migration strategies

- **SuperServe** (NSDI 2025) - Variable workloads
  - Fine-grained inference serving
  - Handles unpredictable request patterns

- **PRISM** (2025) - Distributed training modeling
  - Probabilistic performance modeling
  - Scalable to large distributed systems

## Key Themes and Trends

### 1. Prefill-Decode Separation is Critical
- Prefill: compute-bound, parallel, high latency
- Decode: memory-bound, sequential, low latency per token
- DistServe, Sarathi-Serve exploit this for optimization

### 2. KV Cache is the Primary Memory Bottleneck
- Memory grows with batch size × sequence length
- PagedAttention reduced waste dramatically
- Further optimization via quantization, sparsity, compression

### 3. Attention Optimization is Foundational
- FlashAttention family achieves near-optimal utilization
- Memory complexity reduction enables longer contexts
- Hardware-specific optimization (A100 vs H100) matters

### 4. Speculative Decoding Matures
- Shift from separate draft models to integrated prediction
- MEDUSA, EAGLE-3 eliminate external draft model overhead
- Bottleneck-aware selection becoming standard

### 5. Simulation-Based Modeling Emerges
- VIDUR provides accurate LLM-specific simulation
- Enables serving system research without expensive GPU runs
- Trace-driven approaches improve prediction accuracy

### 6. SLO-Aware Systems Design
- Moving beyond throughput-only optimization
- Explicit latency constraints in scheduling
- Cost-latency tradeoff optimization

## Gap Analysis

### Well-Covered Areas
- Memory management and KV cache optimization
- Attention mechanism efficiency
- Single-node serving optimization
- Basic speculative decoding

### Areas Needing More Coverage
- Cross-datacenter LLM serving
- Heterogeneous accelerator serving (mixed GPU types)
- Energy-aware inference optimization
- Accuracy-latency tradeoff modeling
- Multi-modal LLM inference
- Edge/mobile LLM deployment performance models

## Venue Distribution

| Venue | Count | Focus |
|-------|-------|-------|
| OSDI | 4 | Serving systems |
| SOSP | 2 | Memory management |
| ISCA | 2 | Hardware/KV cache |
| MLSys | 3 | ML systems |
| ICML | 2 | Speculative decoding |
| ICLR | 2 | Attention, speculative |
| NeurIPS | 2 | Attention, prediction |
| ASPLOS | 1 | Distributed |
| NSDI | 1 | Scheduling |
| ACL | 2 | Speculative, KV cache |
| ATC | 1 | Latency-aware |

## Key Papers for Deep Analysis

1. **vLLM/PagedAttention** - Foundation for modern LLM serving
2. **VIDUR** - Essential for simulation-based research
3. **FlashAttention-3** - State-of-art attention efficiency
4. **DistServe** - Disaggregated architecture paradigm
5. **Roofline-LLM** - Bridges analytical and ML prediction

## References Summary

Total papers cataloged: 42
- Serving systems: 12
- Attention optimization: 4
- KV cache: 6
- Speculative decoding: 5
- Performance prediction: 5
- Distributed inference: 5
- Benchmarks/surveys: 5
