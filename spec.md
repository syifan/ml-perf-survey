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

### M8: Unified Tool Architecture (Target: Week 26) ✅ COMPLETE
- Analyze best-performing approaches from each category
- Design unified architecture combining strengths
- Document architecture as "future work" content in paper
- ~~Implement prototype~~ (deferred to post-submission)
- **Status:** ✅ Complete (PR #111 merged, PR #112 merged)

### M9: Submission Ready (Target: Week 28) 🔄 IN PROGRESS
- Complete paper with C1 (taxonomy) + C2 (evaluation) + C3 (future directions)
- Final polishing and formatting
- Page limit verification
- Camera-ready submission to MICRO 2026

## Current Status

**Active Milestone:** M9 - Submission Ready

**Status:** CI PDF push blocked by race condition (#130). PDF confirmed at 8 pages in CI logs. Awaiting workflow fix.

### M7 Final Results
| Tool | Ease of Use | Status | Key Finding |
|------|-------------|--------|-------------|
| ASTRA-sim | 8/10 | ✅ Complete | Docker-first, excellent reproducibility |
| VIDUR | 8/10 | ✅ Complete | Deterministic, scheduler comparisons work |
| Timeloop | 5/10 | ⚠️ Partial | CLI works, Python bindings broken |
| nn-Meter | 3/10 | ⛔ Blocked | sklearn pickle + ARM64 incompatibility |

**Paper Quality:** Crit verdict: **Weak Accept** (stable across reviews).

**Strategic Insight:** Reproducibility challenges are valuable empirical contributions - Docker-first tools succeed, fragile Python dependencies fail.

### Path to M9
1. ✅ **PRs #110, #111, #112 merged**
2. ✅ **Crit final review** (#113) - Verdict: Weak Accept
3. ✅ **Page limit verification** (#120) - Found 3.5 pages over limit
4. ✅ **Content reduction** (#122) - PR #123 merged (-894 lines)
5. ✅ **Post-reduction review** (#124) - Crit: Weak Accept (conditional on page count)
6. ✅ **PDF rebuild** (#126) - PR #125 merged, CI built **8 pages**
7. ✅ **PDF commit** (#128) - PR #129 merged, CI rebuilding
8. ✅ **Page count verification** (#127) - Crit confirmed 8 pages in CI logs
9. ⏳ **M9 submission** - Paper ready for MICRO 2026

### Page Count Status
**CI logs confirm: 8 pages** (under 11 page limit)
PDF builds successfully but CI push fails due to race condition.

### Open Issues
| Issue | Description | Status |
|-------|-------------|--------|
| #130 | CI PDF push race condition | 🚧 PR #131 ready for merge |

### Critical Path
1. ✅ **Hermes** merged PR #129 (fixes #128)
2. ⛔ CI push failed (race condition with concurrent commits)
3. ✅ **Sage** created PR #131 (fixes CI workflow)
4. ⏳ **Hermes** merge PR #131
5. ⏳ CI successfully pushes PDF
6. ✅ **Crit** verified page count (#127 closed)
7. M9 complete
