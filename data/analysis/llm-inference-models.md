# Deep Analysis: LLM Inference Performance Models

This document provides detailed analysis of performance modeling approaches specific to Large Language Model (LLM) inference, covering serving systems, attention optimization, KV cache management, speculative decoding, and performance prediction.

---

## 1. Foundational Serving Systems

### 1.1 vLLM/PagedAttention (SOSP 2023)

**Full Title:** Efficient Memory Management for Large Language Model Serving with PagedAttention

**Authors:** Kwon et al. (UC Berkeley)

#### Core Methodology

PagedAttention revolutionized LLM serving by applying OS virtual memory concepts to KV cache management. The key insight is that KV cache memory can be managed in non-contiguous blocks, eliminating the waste from pre-allocation.

The system consists of:
1. **Block-based KV Cache** - Fixed-size blocks hold key-value pairs for token sequences
2. **Block Table** - Maps logical blocks to physical blocks (like page tables)
3. **Dynamic Allocation** - Blocks allocated on-demand during generation
4. **Flexible Sharing** - Copy-on-write semantics for parallel sampling

#### Architecture

```
Input: Token IDs + Sampling Parameters
              |
              v
    +-------------------+
    | Block Manager     |  Allocates physical blocks
    | (Virtual Memory)  |  on-demand from pool
    +-------------------+
              |
              v
    +-------------------+
    | Block Table       |  Logical → Physical mapping
    | (Per Request)     |  Copy-on-write for sharing
    +-------------------+
              |
              v
    +-------------------+
    | PagedAttention    |  Fetches KV from scattered
    | Kernel            |  physical blocks
    +-------------------+
```

#### Performance Model Implications

| Aspect | Traditional | PagedAttention | Impact |
|--------|-------------|----------------|--------|
| Memory Waste | 60-80% | <4% | Near-optimal utilization |
| Max Batch Size | Limited by worst-case | Dynamic | 2-4x more concurrent requests |
| Memory Complexity | O(max_seq_len × batch) | O(actual_tokens) | Proportional to usage |
| Sharing Overhead | Full copy | CoW (metadata only) | Enables parallel sampling |

#### Accuracy Claims

| Metric | Improvement | Baseline |
|--------|-------------|----------|
| Throughput | 2-4x | FasterTransformer |
| Throughput | 2.2x | Orca |
| Memory Waste | <4% | 60-80% baseline |
| Sharing Efficiency | Near-zero overhead | Full copy |

#### Strengths

1. **Foundational contribution** - Now standard in LLM serving
2. **Minimal memory waste** - Near-optimal utilization
3. **Flexible sharing** - Enables beam search, parallel sampling efficiently
4. **Open source** - https://github.com/vllm-project/vllm
5. **Production adoption** - Used by major providers

#### Limitations

1. **Block granularity** - Small internal fragmentation remains
2. **Single-node focus** - Original design for single GPU
3. **Homogeneous memory** - Assumes uniform GPU memory
4. **Kernel overhead** - Non-contiguous access has some cost

#### Taxonomy Classification

- **Approach:** System Design (memory management)
- **Hardware:** GPU (NVIDIA)
- **Workloads:** LLM inference
- **Target:** Throughput, Memory
- **Input:** Runtime (dynamic allocation)
- **Reproducibility:** Full

---

### 1.2 Orca (OSDI 2022)

**Full Title:** Orca: A Distributed Serving System for Transformer-Based Generative Models

**Authors:** Yu et al. (Seoul National University, FriendliAI)

#### Core Methodology

Orca introduced **continuous batching** (iteration-level scheduling), the foundation for all modern LLM serving. The key insight is that request-level batching wastes compute due to variable generation lengths.

Key innovations:
1. **Iteration-Level Scheduling** - Batching decisions at each decoding step
2. **Selective Batching** - Only batch similar-phase requests
3. **Continuous Joining** - New requests join mid-batch

#### Traditional vs. Continuous Batching

```
Traditional (Request-Level):
[Req A: ████████████████████]  ← Long generation
[Req B: ████----]               ← Finishes early, GPU idle
[Req C: ██████████----]         ← Medium length

Continuous (Iteration-Level):
[Req A: ████|D joins|█████████|E joins|████]
[Req B: ████|done→D starts here        ]
[Req C: ██████████|done→E starts here  ]
```

#### Performance Model Implications

| Dimension | Traditional | Continuous | Impact |
|-----------|-------------|------------|--------|
| GPU Utilization | Variable (gaps) | Consistent | Higher throughput |
| Latency Variance | High (head-of-line) | Lower | Better SLO compliance |
| Memory Management | Static | Dynamic | More flexible |
| Batch Size | Fixed | Variable | Adaptive |

#### Accuracy Claims

| Metric | Improvement | Notes |
|--------|-------------|-------|
| Throughput | 36.9x | vs. static batching |
| GPU Utilization | Near 100% | During serving |
| Latency | Lower variance | vs. request-level |

#### Strengths

1. **Paradigm shift** - Redefined LLM serving
2. **Foundational** - All modern systems build on this
3. **Simple insight** - Iteration-level batching
4. **High impact** - Enabled practical LLM deployment

#### Limitations

1. **Prefill-decode interference** - Mixed phases in batch
2. **Memory management** - Static allocation (pre-PagedAttention)
3. **Single model** - Not multi-model serving

#### Taxonomy Classification

- **Approach:** System Design (scheduling)
- **Hardware:** GPU
- **Workloads:** LLM inference
- **Target:** Throughput, Latency
- **Input:** Runtime
- **Reproducibility:** Partial (proprietary)

---

## 2. Advanced Scheduling & Resource Management

### 2.1 DistServe (OSDI 2024)

**Full Title:** DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving

**Authors:** Zhong et al. (Peking University)

#### Core Methodology

DistServe introduces **prefill-decode disaggregation**, assigning separate GPU resources to each phase. The key insight is that prefill (compute-bound) and decode (memory-bound) have fundamentally different characteristics.

Components:
1. **Prefill Pool** - GPUs optimized for compute-intensive parallel processing
2. **Decode Pool** - GPUs optimized for memory-intensive sequential generation
3. **KV Transfer** - Efficient migration of KV cache between pools
4. **Placement Algorithm** - Optimizes GPU assignment for SLO targets

#### Phase Characteristics

| Phase | Compute | Memory | Parallelism | Optimization |
|-------|---------|--------|-------------|--------------|
| Prefill | High (O(n²)) | Moderate | High (all tokens parallel) | Maximize compute |
| Decode | Low (O(n)) | High (KV read) | Low (one token) | Maximize bandwidth |

#### Architecture

```
                    Request Arrival
                          |
                          v
                 +----------------+
                 | Router/Scheduler|
                 +----------------+
                    /          \
                   v            v
    +----------------+     +----------------+
    | Prefill Pool   |     | Decode Pool    |
    | (Compute-opt)  |     | (Memory-opt)   |
    +----------------+     +----------------+
            |                     ^
            | KV Cache Transfer   |
            +---------------------+
```

#### Performance Model

The key performance insight is the interference model:

```
Traditional (Colocated):
  Decode Latency = f(batch_size, prefill_interference)

DistServe:
  Decode Latency = f(batch_size) only
  → Predictable, optimizable
```

#### Accuracy Claims

| Metric | Improvement | Baseline |
|--------|-------------|----------|
| Request Rate | 7.4x | vLLM (same SLO) |
| SLO Tightness | 12.6x | vLLM (same rate) |
| Goodput | 4.4x | Colocated serving |

#### Strengths

1. **Eliminates interference** - Predictable per-phase performance
2. **Flexible resource allocation** - Scale phases independently
3. **SLO-aware** - Explicit optimization for latency targets
4. **Production-ready** - Deployed at scale

#### Limitations

1. **KV transfer overhead** - Network/interconnect requirement
2. **Resource efficiency** - May underutilize during low load
3. **Complexity** - More components to manage
4. **Minimum scale** - Needs sufficient request volume

#### Taxonomy Classification

- **Approach:** System Design (disaggregation)
- **Hardware:** Multi-GPU
- **Workloads:** LLM inference
- **Target:** Throughput, Latency (goodput)
- **Input:** Workload characteristics
- **Reproducibility:** Full

---

### 2.2 Sarathi-Serve (OSDI 2024)

**Full Title:** Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve

**Authors:** Agrawal et al. (Microsoft Research, Georgia Tech)

#### Core Methodology

Sarathi-Serve introduces **chunked prefills** to eliminate decode stalls without full disaggregation. The key insight is that prefills can be split into fixed-size chunks that integrate smoothly with decode batches.

Key innovations:
1. **Chunked Prefills** - Break prefill into uniform chunks
2. **Decode-Maximal Batching** - Prioritize decode requests in batches
3. **Stall-Free Execution** - No decode waiting for prefill completion

#### Chunking Strategy

```
Traditional:
  Prefill[1000 tokens] → Decode batch stalls

Sarathi-Serve:
  Prefill[chunk1: 256] + Decode batch
  Prefill[chunk2: 256] + Decode batch
  Prefill[chunk3: 256] + Decode batch
  Prefill[chunk4: 232] + Decode batch
  → No stalls, uniform iterations
```

#### Performance Model

The batch composition determines latency:

```
Iteration Time = max(
  Prefill_chunk_time,
  Decode_batch_time
)

With chunking:
  Prefill_chunk_time ≈ Decode_batch_time
  → Balanced, predictable
```

#### Accuracy Claims

| Metric | Value | Notes |
|--------|-------|-------|
| Throughput | +25% | vs. vLLM |
| Decode Stalls | 0 | vs. variable in baseline |
| TTFT Variance | Lower | Predictable chunking |

#### Strengths

1. **Simpler than disaggregation** - Single-node compatible
2. **Stall-free** - Guaranteed decode progress
3. **Predictable** - Uniform iteration times
4. **Complementary** - Works with PagedAttention

#### Limitations

1. **Chunk size tuning** - Requires configuration
2. **TTFT increase** - Chunking delays first token
3. **Request mixing** - Still some phase interference

#### Taxonomy Classification

- **Approach:** System Design (scheduling)
- **Hardware:** GPU
- **Workloads:** LLM inference
- **Target:** Throughput, Latency variance
- **Input:** Configuration
- **Reproducibility:** Full

---

### 2.3 Llumnix (OSDI 2024)

**Full Title:** Llumnix: Dynamic Scheduling for Large Language Model Serving

**Authors:** Sun et al. (SJTU, Alibaba)

#### Core Methodology

Llumnix enables **live request migration** across model instances for dynamic load balancing. The key insight is that KV cache can be migrated mid-generation to rebalance load.

Components:
1. **Request Manager** - Tracks request locations and states
2. **Migration Engine** - Transfers KV cache between instances
3. **Scheduler** - Decides when/where to migrate
4. **Priority Support** - Fast-track high-priority requests

#### Migration Strategy

```
Instance A (Overloaded)      Instance B (Underloaded)
[Req 1: generating...]       [Req 5: generating...]
[Req 2: generating...]       [Req 6: idle]
[Req 3: generating...]   →   [Req 3: migrated!]
[Req 4: generating...]
```

#### Performance Model

Migration cost vs. benefit:

```
Migration Overhead = KV_size / bandwidth + setup_cost
Benefit = Reduced queueing delay at destination

Migrate if: Expected_latency_reduction > Migration_overhead
```

#### Accuracy Claims

| Metric | Improvement | Baseline |
|--------|-------------|----------|
| Tail Latency (P99) | 10x reduction | Static placement |
| High-Priority Latency | 1.5x faster | No priority |
| Cost Savings | 36% | Same tail latency |

#### Strengths

1. **Dynamic adaptation** - Responds to load changes
2. **Priority support** - Differentiated service levels
3. **Live migration** - No request restart
4. **Cost-effective** - Better resource utilization

#### Limitations

1. **Migration overhead** - Bandwidth consumption
2. **Coordination complexity** - Distributed state
3. **Minimum scale** - Needs multiple instances

#### Taxonomy Classification

- **Approach:** System Design (scheduling, migration)
- **Hardware:** Multi-GPU
- **Workloads:** LLM inference
- **Target:** Tail latency, Fairness
- **Input:** Runtime load
- **Reproducibility:** Partial

---

## 3. Attention Mechanism Optimization

### 3.1 FlashAttention (NeurIPS 2022)

**Full Title:** FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

**Authors:** Dao et al. (Stanford)

#### Core Methodology

FlashAttention achieves **IO-aware attention** by restructuring the attention computation to minimize HBM (High Bandwidth Memory) accesses. The key insight is that attention is memory-bound, not compute-bound.

Core algorithm:
1. **Tiling** - Process attention in small blocks that fit in SRAM
2. **Kernel Fusion** - Combine softmax and matmul in one kernel
3. **Recomputation** - Recompute during backward pass vs. storing activations
4. **Online Softmax** - Compute softmax incrementally across tiles

#### IO Complexity Analysis

```
Standard Attention:
  Q, K, V reads: 3 × N × d
  S = QK^T write/read: N²  ← Quadratic!
  P = softmax(S): N²
  O = PV: N × d
  Total HBM: O(N² + Nd)

FlashAttention:
  Process in tiles, never materialize full N² matrix
  Total HBM: O(Nd) ← Linear!
```

#### Performance Model

The speedup comes from reduced memory traffic:

| Sequence Length | Standard (GB) | Flash (GB) | Speedup |
|-----------------|---------------|------------|---------|
| 1K | 0.01 | 0.001 | 2x |
| 4K | 0.13 | 0.004 | 3x |
| 16K | 2.0 | 0.016 | 7x |
| 64K | 32 | 0.064 | 15x+ |

#### Accuracy Claims

| Metric | Value | Notes |
|--------|-------|-------|
| Memory | 10-20x reduction | Long sequences |
| Speed | 2-4x | GPT-2, BERT |
| Exactness | Bit-identical | No approximation |

#### Strengths

1. **Exact attention** - No accuracy loss
2. **Linear memory** - Enables long contexts
3. **Widely adopted** - Standard in LLM frameworks
4. **Open source** - https://github.com/Dao-AILab/flash-attention

#### Limitations

1. **Hardware-specific** - CUDA implementation
2. **Non-causal variants** - Different optimizations needed
3. **Custom backward** - Requires special handling

#### Taxonomy Classification

- **Approach:** Algorithmic (IO-aware)
- **Hardware:** GPU (NVIDIA)
- **Workloads:** Attention computation
- **Target:** Memory, Speed
- **Input:** Algorithm design
- **Reproducibility:** Full

---

### 3.2 FlashAttention-2 (ICLR 2024)

**Full Title:** FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning

**Authors:** Dao (Princeton)

#### Core Methodology

FlashAttention-2 improves upon v1 with:
1. **Better parallelization** - Parallelize over sequence length, not just batch
2. **Reduced non-matmul FLOPs** - Fewer operations outside tensor cores
3. **Improved work partitioning** - Better load balancing across warps

#### Key Optimizations

```
FlashAttention-1:
  - Parallelize over batch and heads
  - Sequential over sequence blocks

FlashAttention-2:
  - Additional parallelism over sequence
  - Within-warp reduction for softmax
  - Reduced shared memory bank conflicts
```

#### Accuracy Claims

| Hardware | FlashAttention-2 | FlashAttention-1 | Improvement |
|----------|------------------|------------------|-------------|
| A100 FLOPs | 50-73% of peak | 25-40% | 2x |
| H100 FLOPs | 35% of peak | - | Baseline for FA3 |

#### Strengths

1. **Near-optimal A100 utilization** - 73% theoretical max
2. **Drop-in replacement** - API compatible with v1
3. **Cumulative gains** - Compounds with other optimizations

#### Limitations

1. **H100 underutilization** - Only 35%, room for improvement
2. **Hopper features unused** - No TMA, FP8, warp specialization

#### Taxonomy Classification

- **Approach:** Algorithmic (optimized parallelism)
- **Hardware:** GPU (A100, H100)
- **Workloads:** Attention computation
- **Target:** Speed
- **Input:** Hardware-aware design
- **Reproducibility:** Full

---

### 3.3 FlashAttention-3 (2024)

**Full Title:** FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision

**Authors:** Shah et al. (Together AI, Meta)

#### Core Methodology

FlashAttention-3 exploits **Hopper architecture features**:
1. **Warp Specialization** - Producer (load) and consumer (compute) warps
2. **Asynchronous Execution** - Overlap memory and compute via TMA
3. **FP8 Support** - Lower precision with higher throughput
4. **Incoherent Processing** - Handles numerical edge cases

#### Hopper Optimizations

```
Ampere (A100):
  Load → Compute → Store (Sequential)

Hopper (H100):
  Producer Warp: Load[i+1] → Load[i+2] → ...
  Consumer Warp:         Compute[i] → Compute[i+1] → ...
  (Overlapped via TMA and pipeline)
```

#### Performance Model

| Precision | H100 Throughput | Utilization |
|-----------|-----------------|-------------|
| BF16 | 740 TFLOPs/s | 75% |
| FP16 | 840 TFLOPs/s | 85% |
| FP8 | 1.2-1.3 PFLOPs/s | 75% (FP8 peak) |

#### Accuracy Claims

| Metric | Value | Notes |
|--------|-------|-------|
| Speedup (BF16) | 1.5-2.0x | vs. FlashAttention-2 |
| H100 Utilization | 75-85% | vs. 35% for FA2 |
| FP8 Error | 2.6x lower | vs. baseline FP8 |

#### Strengths

1. **Hopper-optimized** - Exploits latest hardware
2. **FP8 support** - Lower precision, higher throughput
3. **Near-peak utilization** - 75-85% of H100
4. **Accuracy preserved** - Incoherent processing for FP8

#### Limitations

1. **H100 only** - Requires Hopper architecture
2. **Complexity** - Warp specialization is intricate
3. **Framework integration** - Needs adoption

#### Taxonomy Classification

- **Approach:** Algorithmic (hardware-specific)
- **Hardware:** GPU (H100 Hopper)
- **Workloads:** Attention computation
- **Target:** Speed, Utilization
- **Input:** Hardware-aware design
- **Reproducibility:** Partial

---

### 3.4 FlashInfer (MLSys 2025)

**Full Title:** FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving

**Authors:** Ye et al. (CMU, UW)

#### Core Methodology

FlashInfer provides a **customizable attention kernel generation** framework. Unlike fixed FlashAttention kernels, it generates optimized kernels for diverse serving scenarios.

Key features:
1. **JIT Compilation** - Generates kernels for specific configurations
2. **Composable Primitives** - Mix attention variants
3. **Batch Flexibility** - Handles ragged batches efficiently
4. **Prefix Sharing** - Optimized for common prefix scenarios

#### Flexibility Dimensions

| Dimension | FlashInfer Support |
|-----------|-------------------|
| Head dimensions | 32-512 |
| Page sizes | Variable |
| Attention patterns | Causal, sliding window, block-sparse |
| Precision | FP16, BF16, FP8 |
| Layouts | Various KV cache layouts |

#### Accuracy Claims

| Metric | Improvement | Baseline |
|--------|-------------|----------|
| Inter-token latency | 29-69% reduction | FlashAttention |
| Long-context latency | 28-30% reduction | Standard kernels |
| Kernel coverage | 100s of variants | Fixed kernels |

#### Strengths

1. **Customizable** - JIT for specific configurations
2. **Serving-optimized** - Handles real-world patterns
3. **Prefix sharing** - Common in applications
4. **Open source** - https://github.com/flashinfer-ai/flashinfer

#### Limitations

1. **JIT overhead** - Compilation time for new configurations
2. **Complexity** - More parameters to tune
3. **Less mature** - Newer than FlashAttention

#### Taxonomy Classification

- **Approach:** Algorithmic (JIT generation)
- **Hardware:** GPU
- **Workloads:** LLM inference attention
- **Target:** Latency
- **Input:** Configuration-specific
- **Reproducibility:** Full

---

## 4. KV Cache Optimization

### 4.1 Oaken (ISCA 2025)

**Full Title:** Oaken: Online-Offline Hybrid Quantization for KV Cache Compression

**Authors:** Park et al.

#### Core Methodology

Oaken combines **offline calibration** with **online quantization** for KV cache compression. The key insight is that outlier patterns are predictable across inputs.

Components:
1. **Offline Analysis** - Identify outlier thresholds per layer/head
2. **Online Quantization** - Apply calibrated thresholds at runtime
3. **Loss Mitigation** - Techniques to preserve accuracy

#### Quantization Strategy

```
Offline Phase:
  - Profile on calibration set
  - Determine per-channel scales and zero-points
  - Identify outlier thresholds

Online Phase:
  - Quantize KV to INT4/INT8
  - Store outliers in FP16 sparse format
  - Dequantize during attention
```

#### Accuracy Claims

| Metric | Value | Notes |
|--------|-------|-------|
| Compression | 4-8x | KV cache size |
| Accuracy Loss | <1% | On downstream tasks |
| Latency Impact | Minimal | Efficient kernels |

#### Strengths

1. **Hybrid approach** - Combines offline and online advantages
2. **Accuracy preservation** - Careful outlier handling
3. **Practical** - Works with existing serving systems

#### Limitations

1. **Calibration cost** - Offline profiling needed
2. **Model-specific** - Thresholds vary per model

#### Taxonomy Classification

- **Approach:** Compression (quantization)
- **Hardware:** GPU
- **Workloads:** LLM inference
- **Target:** Memory
- **Input:** Calibration + runtime
- **Reproducibility:** Partial

---

### 4.2 ALISA (ISCA 2024)

**Full Title:** ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching

**Authors:** Various

#### Core Methodology

ALISA exploits **attention sparsity patterns** for KV cache management. The key insight is that different layers have different sparsity characteristics.

Key innovations:
1. **Layer-specific scheduling** - Different strategies per layer
2. **Hierarchical caching** - Multi-level KV storage
3. **Sparsity-aware eviction** - Keep important tokens

#### Sparsity Analysis

```
Layer Type:
  - Early layers: Dense attention, keep all KV
  - Middle layers: Moderate sparsity, selective keep
  - Late layers: Sparse attention, aggressive eviction

Token Importance:
  - Compute importance scores from attention patterns
  - Evict low-importance tokens from cache
  - Recompute if needed
```

#### Accuracy Claims

| Metric | Value | Notes |
|--------|-------|-------|
| Memory Reduction | 2-4x | Layer-dependent |
| Accuracy | <1% degradation | Task-dependent |
| Speedup | 1.3-1.5x | From reduced memory |

#### Strengths

1. **Sparsity exploitation** - Leverages attention patterns
2. **Layer-aware** - Different strategies per layer
3. **Hierarchical** - Multi-level caching

#### Limitations

1. **Dynamic patterns** - Sparsity varies with input
2. **Accuracy risk** - Eviction can hurt quality
3. **Model-dependent** - Patterns differ across models

#### Taxonomy Classification

- **Approach:** Compression (sparsity)
- **Hardware:** GPU
- **Workloads:** LLM inference
- **Target:** Memory
- **Input:** Attention patterns
- **Reproducibility:** Partial

---

### 4.3 MorphKV (2025)

**Full Title:** MorphKV: Adaptive KV Cache Compression via Dynamic Token Selection

**Authors:** Various

#### Core Methodology

MorphKV uses **attention-based token selection** to maintain a fixed-size KV cache. The key insight is that token importance can be computed efficiently and refined iteratively.

Algorithm:
1. **Initial Fill** - Keep all tokens until cache full
2. **Score Computation** - Use recent attention patterns
3. **Iterative Refinement** - Update importance scores each step
4. **Eviction** - Remove lowest-scored tokens

#### Fixed-Size Strategy

```
Cache Capacity: C tokens

When |cache| > C:
  1. Compute importance: score[t] = Σ attention[t] over recent tokens
  2. Sort by importance
  3. Evict lowest C - budget tokens
  4. Continue generation
```

#### Accuracy Claims

| Metric | Value | Notes |
|--------|-------|-------|
| Memory Savings | 50%+ | Fixed cache size |
| Accuracy | Comparable | To full cache on most tasks |
| Long-context | Enables | Previously OOM sequences |

#### Strengths

1. **Fixed memory budget** - Predictable resource usage
2. **Adaptive** - Importance updates over time
3. **Simple implementation** - Attention-based scores

#### Limitations

1. **Task sensitivity** - Some tasks need all tokens
2. **Eviction risk** - Important tokens may be evicted
3. **Scoring overhead** - Adds computation

#### Taxonomy Classification

- **Approach:** Compression (selection)
- **Hardware:** GPU
- **Workloads:** LLM inference
- **Target:** Memory
- **Input:** Attention patterns
- **Reproducibility:** Partial

---

## 5. Speculative Decoding

### 5.1 MEDUSA (ICML 2024)

**Full Title:** MEDUSA: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads

**Authors:** Cai et al. (Princeton, Together AI)

#### Core Methodology

MEDUSA attaches **multiple parallel prediction heads** to an LLM for speculative decoding without a separate draft model. Each head predicts a different future token position.

Architecture:
```
LLM Hidden State
       |
       +---→ [Head 0] → Token t+1 prediction
       +---→ [Head 1] → Token t+2 prediction
       +---→ [Head 2] → Token t+3 prediction
       +---→ [Head 3] → Token t+4 prediction

Tree-based verification:
  Construct tree of candidate sequences
  Single forward pass verifies all
  Accept longest matching prefix
```

#### Training

| Aspect | Details |
|--------|---------|
| Head Architecture | Single linear layer per head |
| Training Data | Same as LLM or fine-tuning set |
| Training Cost | Hours (vs. days for draft model) |
| Frozen Base | LLM weights unchanged |

#### Acceptance Strategy

MEDUSA uses tree attention for efficient verification:
1. Generate candidate tree from all head combinations
2. Single forward pass scores entire tree
3. Accept longest prefix matching true distribution
4. Rejection sampling for final token

#### Accuracy Claims

| Model | Speedup | Heads | Notes |
|-------|---------|-------|-------|
| Vicuna-7B | 2.2x | 4 | Greedy decoding |
| Vicuna-13B | 2.4x | 4 | Greedy decoding |
| Vicuna-33B | 2.8x | 5 | Greedy decoding |
| Sampling | 2.2-3.6x | 4 | With rejection |

#### Strengths

1. **No draft model** - Eliminates separate model overhead
2. **Lightweight heads** - Single linear layer each
3. **Easy training** - Hours, not days
4. **Tree verification** - Efficient batch scoring

#### Limitations

1. **Head training** - Still requires training
2. **Model-specific** - Heads tied to base model
3. **Memory overhead** - Additional parameters

#### Taxonomy Classification

- **Approach:** Speculative (integrated heads)
- **Hardware:** GPU
- **Workloads:** LLM inference
- **Target:** Latency, Throughput
- **Input:** Trained heads
- **Reproducibility:** Full

---

### 5.2 EAGLE-3 (NeurIPS 2024)

**Full Title:** EAGLE-3: Lossless Acceleration of LLM Inference via Training-Free Token Tree Verification

**Authors:** Li et al.

#### Core Methodology

EAGLE-3 uses a **lightweight autoregressive head** on internal LLM layers for draft generation. The key insight is that hidden states contain sufficient information for multi-step prediction.

Architecture:
```
LLM Layers:
  [Layer 1] → [Layer 2] → ... → [Layer K] → [Layer K+1] → ... → [Layer N]
                                     ↓
                              EAGLE Predictor
                                     ↓
                              Draft: t+1, t+2, t+3, ...
```

#### Draft Generation

| Step | Description |
|------|-------------|
| 1 | Extract hidden state from intermediate layer |
| 2 | Feed to lightweight predictor |
| 3 | Autoregressively generate draft tokens |
| 4 | Verify with full model |

#### Accuracy Claims

| Metric | Value | Notes |
|--------|-------|-------|
| Acceptance Rate | 70-80% | Higher than separate draft |
| Speedup | 2-3x | Typical tasks |
| Lossless | Yes | Exact output distribution |

#### Strengths

1. **Training-free verification** - Standard verification
2. **High acceptance** - Good draft quality from hidden states
3. **Single model** - No separate draft model weights

#### Limitations

1. **Predictor training** - Still needs trained head
2. **Layer selection** - Which layer to extract from matters

#### Taxonomy Classification

- **Approach:** Speculative (hidden-state based)
- **Hardware:** GPU
- **Workloads:** LLM inference
- **Target:** Latency
- **Input:** Trained predictor
- **Reproducibility:** Partial

---

### 5.3 MagicDec (ICLR 2025)

**Full Title:** MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context Generation with Speculative Decoding

**Authors:** Various

#### Core Methodology

MagicDec provides a **bottleneck-aware drafting strategy** that adapts to whether the system is compute-bound or memory-bound. The key insight is that optimal speculation depth depends on the current bottleneck.

Analysis framework:
```
Compute-bound (small batch, short context):
  → More aggressive speculation
  → Higher draft length acceptable

Memory-bound (large batch, long context):
  → Conservative speculation
  → KV compression > model compression for acceptance
```

#### Strategy Selection

| Scenario | Batch | Context | Strategy |
|----------|-------|---------|----------|
| Interactive | Small | Varies | Long drafts |
| Batched | Large | Short | Medium drafts |
| Long-context | Any | Long | Conservative + KV compression |

#### Accuracy Claims

| Metric | Value | Notes |
|--------|-------|-------|
| Latency Reduction | 50%+ | Long-context batched |
| Strategy | Adaptive | Bottleneck-aware |

#### Strengths

1. **Bottleneck-aware** - Adapts to conditions
2. **Unified framework** - Covers multiple scenarios
3. **Actionable guidance** - When to speculate aggressively

#### Limitations

1. **Complexity** - Needs bottleneck detection
2. **Dynamic workloads** - Adaptation latency

#### Taxonomy Classification

- **Approach:** Speculative (adaptive)
- **Hardware:** GPU
- **Workloads:** LLM inference
- **Target:** Latency, Throughput
- **Input:** Runtime characteristics
- **Reproducibility:** Partial

---

## 6. Performance Prediction & Simulation

### 6.1 VIDUR (MLSys 2024)

**Full Title:** VIDUR: A Large-Scale Simulation Framework for LLM Inference

**Authors:** Agrawal et al. (Microsoft Research)

#### Core Methodology

VIDUR provides a **discrete-event simulation framework** specifically designed for LLM inference. The key contribution is accurate modeling of serving system behavior without GPU execution.

Components:
1. **Request Generator** - Synthetic or trace-driven arrivals
2. **Execution Simulator** - Models GPU execution timing
3. **Memory Simulator** - Tracks KV cache allocation
4. **Scheduling Simulator** - Replicates serving system policies

#### Simulation Architecture

```
Workload Trace              System Configuration
      |                            |
      v                            v
+------------+              +---------------+
| Request    |              | Hardware      |
| Generator  |              | Model         |
+------------+              +---------------+
      |                            |
      +------------+---------------+
                   |
                   v
           +---------------+
           | Discrete-Event|
           | Simulator     |
           +---------------+
                   |
                   v
           Metrics: Latency, Throughput, Memory
```

#### Modeling Approach

| Component | Modeling Method | Accuracy |
|-----------|-----------------|----------|
| Prefill latency | Analytical + profiling | <5% error |
| Decode latency | Memory-bound model | <3% error |
| KV cache | Exact tracking | Exact |
| Scheduling | Policy replication | Faithful |

#### Accuracy Claims

| Metric | Error | Notes |
|--------|-------|-------|
| Overall | <5% | End-to-end |
| Prefill | <5% | Per-phase |
| Decode | <3% | Per-phase |
| Memory | Exact | KV tracking |

#### Use Cases

1. **Capacity planning** - How many GPUs for target SLO?
2. **Policy evaluation** - Compare scheduling algorithms
3. **Research** - Test ideas without GPU cluster
4. **Cost estimation** - Serving cost prediction

#### Strengths

1. **High accuracy** - <5% error on real traces
2. **LLM-specific** - Models prefill/decode phases
3. **Open source** - https://github.com/microsoft/vidur
4. **Extensible** - Add new hardware/policies

#### Limitations

1. **Profiling required** - Need kernel measurements
2. **Single-node focus** - Limited distributed modeling
3. **Static models** - Doesn't model dynamic batching complexity fully

#### Taxonomy Classification

- **Approach:** Simulation-Based
- **Hardware:** GPU (configurable)
- **Workloads:** LLM inference
- **Target:** Latency, Throughput, Memory
- **Input:** Workload traces + profiles
- **Reproducibility:** Full

---

### 6.2 Roofline-LLM (NeurIPS-WS 2024)

**Full Title:** Roofline-LLM: Interpretable Performance Prediction for LLM Inference

**Authors:** Imai et al.

#### Core Methodology

Roofline-LLM extends the **roofline model** for LLM inference with ML augmentation. The key insight is combining analytical understanding with learned corrections.

Hybrid approach:
```
Traditional Roofline:
  Performance = min(Peak_FLOPs, Memory_BW × Arithmetic_Intensity)

Roofline-LLM:
  Performance = Roofline_Base + ML_Correction(features)

Features:
  - Model config (layers, heads, dims)
  - Sequence lengths
  - Batch size
  - Hardware specs
```

#### Performance Model

| Phase | Roofline Analysis |
|-------|-------------------|
| Prefill | Often compute-bound (high arithmetic intensity) |
| Decode | Memory-bound (low arithmetic intensity per token) |
| Attention | Varies with sequence length |

#### ML Augmentation

The learned component captures:
- Kernel launch overheads
- Memory access patterns
- Non-ideal utilization factors
- Cache effects

#### Accuracy Claims

| Metric | Value | vs. Baseline |
|--------|-------|--------------|
| R² | +17 points | vs. pure analytical |
| MSE | 87% reduction | vs. pure ML |
| Interpretability | High | Roofline provides ceiling |

#### Strengths

1. **Interpretable** - Roofline provides understanding
2. **Hybrid** - Combines analytical and ML
3. **Performance ceiling** - Identifies optimization headroom
4. **Generalizable** - Roofline applies across hardware

#### Limitations

1. **Training data** - Needs profiling for ML component
2. **Feature engineering** - Requires domain knowledge
3. **Coarse granularity** - Phase-level, not kernel-level

#### Taxonomy Classification

- **Approach:** Hybrid (Analytical + ML)
- **Hardware:** GPU
- **Workloads:** LLM inference
- **Target:** Latency
- **Input:** Model config + profiling
- **Reproducibility:** Partial

---

### 6.3 ReaLLM (2025)

**Full Title:** ReaLLM: Realistic LLM Inference Performance Prediction

**Authors:** Various

#### Core Methodology

ReaLLM provides **kernel-level simulation** for more accurate prediction than simple analytical models. The key insight is that kernel-level detail matters for LLM inference prediction.

Approach:
1. **Kernel Profiling** - Measure individual CUDA kernels
2. **Execution Graph** - Model kernel dependencies
3. **Memory Tracking** - Track allocation/deallocation
4. **Composition** - Sum kernel times for total

#### Accuracy Claims

| Metric | ReaLLM | Simple Analytical |
|--------|--------|-------------------|
| Prefill Error | <5% | 15-20% |
| Decode Error | <3% | 10-15% |
| End-to-end | <5% | 15-20% |

#### Strengths

1. **Kernel-level accuracy** - Captures real behavior
2. **Memory modeling** - Tracks actual allocation
3. **Composable** - Build up from primitives

#### Limitations

1. **Profiling cost** - Needs kernel measurements
2. **Hardware-specific** - Profiles per hardware

#### Taxonomy Classification

- **Approach:** Simulation (kernel-level)
- **Hardware:** GPU
- **Workloads:** LLM inference
- **Target:** Latency
- **Input:** Kernel profiles
- **Reproducibility:** Partial

---

## 7. Distributed Inference

### 7.1 SpotServe (ASPLOS 2024)

**Full Title:** SpotServe: Serving Generative Large Language Models on Preemptible Instances

**Authors:** Various

#### Core Methodology

SpotServe enables **cost-effective LLM serving** on preemptible cloud instances. The key challenge is handling preemption gracefully.

Components:
1. **State Management** - Checkpoint KV cache and model state
2. **Preemption Handling** - Migrate on eviction notice
3. **Instance Selection** - Balance cost and availability
4. **Request Routing** - Handle instance churn

#### Cost Model

```
On-demand cost: $C_on per hour
Spot cost: $C_spot per hour (typically 3-10x cheaper)
Preemption probability: p per hour

Expected cost = C_spot + p × migration_overhead

Break-even when: C_spot + p × overhead < C_on
```

#### Accuracy Claims

| Metric | Value | Notes |
|--------|-------|-------|
| Cost Savings | 50-70% | vs. on-demand |
| Availability | 99%+ | With redundancy |
| Latency Impact | <10% | During stable periods |

#### Strengths

1. **Cost reduction** - Significant savings
2. **Graceful degradation** - Handles preemption
3. **Practical** - Real cloud deployments

#### Limitations

1. **Preemption risk** - Latency spikes possible
2. **Complexity** - State management overhead
3. **Availability zones** - Need multiple for reliability

#### Taxonomy Classification

- **Approach:** System Design (distributed, cost-aware)
- **Hardware:** Cloud GPU
- **Workloads:** LLM inference
- **Target:** Cost, Availability
- **Input:** Cloud pricing, preemption patterns
- **Reproducibility:** Partial

---

### 7.2 SuperServe (NSDI 2025)

**Full Title:** SuperServe: Fine-Grained Inference Serving for Large Language Models

**Authors:** Various

#### Core Methodology

SuperServe provides **fine-grained resource allocation** for variable workloads. The key insight is that request patterns vary significantly, requiring adaptive resource management.

Features:
1. **Request Classification** - Categorize by expected length/complexity
2. **Dynamic Scaling** - Adjust resources based on load
3. **Priority Queuing** - Differentiated service levels

#### Accuracy Claims

| Metric | Improvement | Baseline |
|--------|-------------|----------|
| Resource Utilization | +30% | Fixed allocation |
| Tail Latency | -40% | Static batching |

#### Strengths

1. **Adaptive** - Responds to workload changes
2. **Fine-grained** - Per-request decisions
3. **Priority support** - SLO differentiation

#### Limitations

1. **Prediction accuracy** - Request classification quality
2. **Overhead** - Classification and routing cost

#### Taxonomy Classification

- **Approach:** System Design (scheduling)
- **Hardware:** Multi-GPU
- **Workloads:** LLM inference
- **Target:** Latency, Utilization
- **Input:** Workload patterns
- **Reproducibility:** Partial

---

## 8. Comparative Analysis

### 8.1 Serving Systems Comparison

| System | Key Innovation | Throughput | Latency | Memory |
|--------|----------------|------------|---------|--------|
| vLLM | PagedAttention | 2-4x | Same | 96%+ util |
| Orca | Continuous batching | 36x | Lower | Baseline |
| DistServe | Disaggregation | 7.4x | Predictable | Same |
| Sarathi-Serve | Chunked prefills | 1.25x | Stall-free | Same |
| Llumnix | Live migration | Same | 10x P99 | Same |

### 8.2 Attention Optimization Comparison

| Method | Memory | Speed | Hardware | Accuracy |
|--------|--------|-------|----------|----------|
| FlashAttention | O(N) | 2-4x | NVIDIA | Exact |
| FlashAttention-2 | O(N) | 2x more | A100 opt | Exact |
| FlashAttention-3 | O(N) | 1.5-2x more | H100 opt | Exact/FP8 |
| FlashInfer | O(N) | Custom | NVIDIA | Exact |

### 8.3 KV Cache Optimization Comparison

| Method | Compression | Accuracy | Approach |
|--------|-------------|----------|----------|
| Oaken | 4-8x | <1% loss | Quantization |
| ALISA | 2-4x | <1% loss | Sparsity |
| MorphKV | 50%+ | Varies | Selection |

### 8.4 Speculative Decoding Comparison

| Method | Speedup | Draft Overhead | Training |
|--------|---------|----------------|----------|
| MEDUSA | 2.2-3.6x | Linear heads | Hours |
| EAGLE-3 | 2-3x | Predictor head | Hours |
| MagicDec | Varies | Adaptive | None (strategy) |

### 8.5 Performance Prediction Comparison

| Model | Error | Approach | Training Data |
|-------|-------|----------|---------------|
| VIDUR | <5% | Simulation | Kernel profiles |
| Roofline-LLM | ~13% | Hybrid | Profiling + config |
| ReaLLM | <5% | Kernel-level | Kernel profiles |

---

## 9. Key Themes and Trends

### 9.1 Prefill-Decode Separation is Fundamental

All modern LLM serving systems recognize the distinct characteristics:
- **Prefill**: Compute-bound, parallelizable, variable duration
- **Decode**: Memory-bound, sequential, predictable per-token

This leads to disaggregation (DistServe), chunking (Sarathi), and phase-aware scheduling.

### 9.2 Memory Management is Critical

KV cache dominates memory usage and determines batch capacity:
- PagedAttention reduced waste from 60-80% to <4%
- Quantization (Oaken) provides 4-8x compression
- Sparsity (ALISA) and selection (MorphKV) offer alternatives
- Memory is often the binding constraint for serving

### 9.3 Attention Optimization Continues

FlashAttention family drives efficiency:
- Linear memory enables long contexts
- Hardware-specific optimization (A100→H100) matters
- Near-peak utilization (75-85%) now achievable
- FP8 support enables further throughput gains

### 9.4 Speculative Decoding Matures

Evolution from separate draft models to integrated approaches:
- MEDUSA: Parallel heads, lightweight training
- EAGLE: Hidden-state based prediction
- MagicDec: Bottleneck-aware strategy selection
- Trend: Eliminate external draft model overhead

### 9.5 Simulation-Based Research Emerges

VIDUR enables LLM serving research without expensive GPU runs:
- <5% accuracy enables meaningful research
- Capacity planning without provisioning
- Policy comparison at scale

### 9.6 SLO-Aware Design Becomes Standard

Moving beyond throughput-only optimization:
- DistServe: Goodput (throughput meeting SLO)
- Llumnix: Priority and tail latency
- SuperServe: Differentiated service levels

---

## 10. Gaps and Open Challenges

### 10.1 Well-Covered Areas

- **Single-node serving optimization** - vLLM, Sarathi mature
- **Attention efficiency** - FlashAttention-3 near-optimal
- **Basic speculative decoding** - MEDUSA, EAGLE work well
- **KV cache management** - Multiple compression approaches

### 10.2 Emerging Challenges

| Challenge | Current State | Needed |
|-----------|---------------|--------|
| Multi-datacenter serving | Limited | Geo-distributed optimization |
| Heterogeneous GPUs | Some support | Unified serving across GPU types |
| Multi-modal LLMs | Nascent | Vision+language serving |
| Energy efficiency | Not addressed | Power-aware serving |
| Accuracy-latency tradeoff | Per-technique | Unified framework |

### 10.3 Underexplored Areas

1. **Edge/mobile LLM inference** - On-device serving optimization
2. **Mixture-of-experts serving** - Efficient MoE inference
3. **Long-context optimization** - Beyond 100K tokens efficiently
4. **Cost modeling** - Unified cost-latency-accuracy framework
5. **Failure handling** - Graceful degradation under faults

---

## 11. Key Takeaways for Survey

### What LLM Inference Performance Models Excel At

1. **Serving system simulation** - VIDUR enables research without GPUs
2. **Attention optimization** - FlashAttention family provides near-optimal kernels
3. **Memory management** - PagedAttention solves KV cache waste
4. **Speculative decoding** - 2-3x speedups with minimal overhead

### Unique Characteristics of LLM Inference

| Aspect | Traditional DNN | LLM Inference |
|--------|-----------------|---------------|
| Memory growth | Static | Dynamic (KV cache) |
| Compute pattern | Uniform | Prefill vs. decode phases |
| Batching | Standard | Continuous/iteration-level |
| Generation | Single forward | Autoregressive |

### Evolution of LLM Inference Optimization

```
Static Batching (2020)
        |
        v
Continuous Batching [Orca] (2022)
        |
        v
Memory Optimization [vLLM] (2023)
        |
        +--- Attention: FlashAttention → FA2 → FA3
        |
        +--- Scheduling: Sarathi, DistServe, Llumnix
        |
        +--- Speculation: MEDUSA, EAGLE
        |
        v
Integrated Systems (2024-2025)
        |
        +--- Simulation: VIDUR
        |
        +--- KV Optimization: Oaken, ALISA, MorphKV
        |
        +--- Adaptive: MagicDec, SuperServe
```

---

## 12. References

1. Kwon, W., et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention. SOSP.

2. Yu, G., et al. (2022). Orca: A Distributed Serving System for Transformer-Based Generative Models. OSDI.

3. Zhong, Y., et al. (2024). DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving. OSDI.

4. Agrawal, A., et al. (2024). Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve. OSDI.

5. Sun, B., et al. (2024). Llumnix: Dynamic Scheduling for Large Language Model Serving. OSDI.

6. Dao, T., et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. NeurIPS.

7. Dao, T. (2024). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. ICLR.

8. Shah, J., et al. (2024). FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision. arXiv.

9. Ye, Z., et al. (2025). FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving. MLSys.

10. Cai, T., et al. (2024). MEDUSA: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads. ICML.

11. Li, Y., et al. (2024). EAGLE-3: Lossless Acceleration of LLM Inference via Training-Free Token Tree Verification. NeurIPS.

12. Agrawal, A., et al. (2024). VIDUR: A Large-Scale Simulation Framework for LLM Inference. MLSys.

13. Imai, T., et al. (2024). Roofline-LLM: Interpretable Performance Prediction for LLM Inference. NeurIPS Workshop.

14. Park, J., et al. (2025). Oaken: Online-Offline Hybrid Quantization for KV Cache Compression. ISCA.

15. Various. (2024). ALISA: Accelerating Large Language Model Inference via Sparsity-Aware KV Caching. ISCA.

16. Various. (2025). MorphKV: Adaptive KV Cache Compression via Dynamic Token Selection. arXiv.

17. Various. (2025). MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context Generation with Speculative Decoding. ICLR.

18. Various. (2024). SpotServe: Serving Generative Large Language Models on Preemptible Instances. ASPLOS.

19. Various. (2025). SuperServe: Fine-Grained Inference Serving for Large Language Models. NSDI.

---

*Analysis by Leo | ML Performance Survey Project*
