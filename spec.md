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

### M7: Comprehensive Third-Party Evaluation (Target: Week 22) 🔄 IN PROGRESS
- Execute all selected tools on common benchmarks
- Collect quantitative results across all evaluation dimensions
- Identify winners and losers for each metric
- Generate comparison tables and figures

### M8: Unified Tool Architecture (Target: Week 26) 🔄 SCOPE REDUCED
- Analyze best-performing approaches from each category
- Design unified architecture combining strengths
- Document architecture as "future work" content in paper
- ~~Implement prototype~~ (deferred to post-submission)

### M9: Submission Ready (Target: Week 28) 🆕
- Complete paper with C1 (taxonomy) + C2 (evaluation) + C3 (architecture)
- Final polishing and formatting
- Page limit verification
- Camera-ready submission to MICRO 2026

## Current Status

**Active Milestone:** M7 - Comprehensive Third-Party Evaluation (nearing completion)

### M7 Execution Status
| Tool | Status | Ease of Use | Key Findings |
|------|--------|-------------|--------------|
| ASTRA-sim | ✅ COMPLETE | 8/10 | Docker-first approach, excellent reproducibility |
| nn-Meter | ⛔ BLOCKED | 3/10 | sklearn pickle incompatibility, ARM64 issues |
| Timeloop | ⚠️ PARTIAL | 6/10 | CLI works, Python bindings fail (libbarvinok.so) |
| VIDUR | 🔄 IN PROGRESS | TBD | Execution underway |
| NeuSight | 📋 PENDING | TBD | Waiting for execution |

**Paper Quality:** Crit has upgraded verdict to **Weak Accept** (from Reject → Weak Reject → Borderline → Weak Accept over 4 review cycles). All critical issues addressed:
- ✅ Taxonomy claim fixed (PR #104 merged)
- ✅ Title-scope alignment achieved
- ✅ Evidence-backed future directions
- ✅ Explicit evaluation rubric defined

**Strategic Insight:** Reproducibility challenges discovered during M7 are valuable empirical contributions. They demonstrate real-world usability issues practitioners face (dependency hell, pickle format incompatibility, platform limitations). This strengthens the survey's practical value.

### Path Forward
1. **Complete M7:** Finish VIDUR/NeuSight execution, close remaining issues
2. **M8 Architecture:** Document unified tool design (architecture only, per strategic decision #105)
3. **Final polish:** Apply minor fixes (#106, #107), verify page limit (#82)
4. **M9 submission:** Paper is near submission-ready quality

**Outstanding Issues:**
- #82: Page limit verification (minor - paper is ~11-12 pages)
- #94: Unified tool architecture design (scoped to documentation only)
- #98-102: M7 execution issues (in progress)
