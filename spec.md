# A Survey of High-Level Modeling and Simulation Methods for Modern Machine Learning Workloads

## Goal

Write a paper for **MICRO 2026** that provides:
1. A systematic survey on performance modeling and simulation for ML workloads with a novel taxonomy
2. Third-party evaluation of tools using common benchmarks (run by us)
3. A new unified tool that combines the best approaches

## Paper Contributions

### Contribution 1: Systematic Survey with Taxonomy
- Comprehensive literature review of performance modeling and simulation methods for ML workloads
- Novel taxonomy that classifies approaches by methodology, target hardware, and workload coverage
- Identification of gaps and trends in the field

### Contribution 2: Third-Party Evaluation
- Define common benchmark suite for fair comparison across tool categories
- Execute all tools ourselves on the same benchmarks
- Evaluate on multiple dimensions: **accuracy**, **ease of use**, **performance**, and **extensibility**
- Report which tools excel and which fall short, with quantitative results

### Contribution 3: Unified Tool Architecture (ZZZ)
- Document architecture design combining best methods from each category
- Show integration patterns and target use cases
- Implementation deferred to follow-up work (post-MICRO 2026)

## Milestones

### M1: Literature Discovery (Target: Week 2) ✅ COMPLETE
- Identify relevant papers on ML performance models and simulators
- Create a structured bibliography database
- Categorize papers by approach (analytical, simulation, hybrid, ML-based)

### M2: Taxonomy Development (Target: Week 4) ✅ COMPLETE
- Define classification dimensions (accuracy, speed, target hardware, etc.)
- Create comparison framework
- Draft taxonomy section of paper

### M3: Deep Analysis (Target: Week 8) ✅ COMPLETE
- Detailed review of key papers in each category
- Extract methodology patterns
- Identify gaps and opportunities

### M4: Paper Draft (Target: Week 12) ✅ COMPLETE
- Complete first draft of all sections
- Generate comparison tables and figures
- Internal review and revision

### M5: Preliminary Evaluation (Target: Week 14) ✅ COMPLETE
- Initial tool evaluations (Timeloop, ASTRA-sim, VIDUR, nn-Meter, etc.)
- Documented findings in data/evaluation/ directory
- Added Section 7 (Experimental Evaluation) to paper

### M6: Benchmark Definition (Target: Week 18) ✅ COMPLETE
- Define common benchmark suite across tool categories
- Select representative ML workloads (CNN, Transformer, LLM, etc.)
- Define evaluation metrics: accuracy (vs. real hardware), latency, memory, ease of use, extensibility
- Document benchmark methodology for reproducibility

### M7: Comprehensive Third-Party Evaluation (Target: Week 22) ✅ COMPLETE
- Execute all selected tools on common benchmarks
- Collect quantitative results across all evaluation dimensions
- Identify winners and losers for each metric
- Generate comparison tables and figures
- **Key finding:** Docker-first tools (ASTRA-sim, VIDUR) succeed; fragile dependencies fail (nn-Meter, Timeloop)

### M8: Unified Tool Architecture (Target: Week 26) 🔄 IN PROGRESS
- Analyze best-performing approaches from each category
- Design unified architecture combining strengths
- Document architecture as "future work" content in paper
- ~~Implement prototype~~ (deferred to post-submission)
- **Status:** PR #111 adds Section 6.6 with three-layer architecture design

### M9: Submission Ready (Target: Week 28) 🆕
- Complete paper with C1 (taxonomy) + C2 (evaluation) + C3 (architecture)
- Final polishing and formatting
- Page limit verification
- Camera-ready submission to MICRO 2026

## Current Status

**Active Milestone:** M8 - Unified Tool Architecture (PRs pending merge)

### M7 Final Results
| Tool | Ease of Use | Status | Key Finding |
|------|-------------|--------|-------------|
| ASTRA-sim | 8/10 | ✅ Complete | Docker-first, excellent reproducibility |
| VIDUR | 8/10 | ✅ Complete | Deterministic, scheduler comparisons work |
| Timeloop | 5/10 | ⚠️ Partial | CLI works, Python bindings broken |
| nn-Meter | 3/10 | ⛔ Blocked | sklearn pickle + ARM64 incompatibility |

**Paper Quality:** Crit verdict: **Weak Accept** (4 review cycles). All critical issues resolved.

**Strategic Insight:** Reproducibility challenges are valuable empirical contributions - Docker-first tools succeed, fragile Python dependencies fail.

### Open PRs (Awaiting Merge)
| PR | Description | Closes |
|----|-------------|--------|
| #110 | M7 evaluation results integration | #102 |
| #111 | Unified tool architecture (Section 6.6) | #94 |
| #112 | ISCA 2025/MLSys 2025/MICRO 2025/HPCA 2026 papers | #109 |

### Path to M9
1. **Merge PRs #110, #111, #112** - Complete M8 content
2. **Final Crit review** - Post-merge quality check
3. **Page limit verification** (#82) - Ensure within MICRO limits
4. **M9 submission** - Paper ready for MICRO 2026

**Outstanding Issues:**
- #82: Page limit verification (deferred until PRs merge)
