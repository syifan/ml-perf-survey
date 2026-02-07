# A Survey of High-Level Modeling and Simulation Methods for Modern Machine Learning Workloads

## Goal

Write a paper for **MICRO 2026** that provides:
1. A systematic survey on high-level performance modeling and simulation for ML workloads with a novel taxonomy
2. Third-party evaluation of tools using common benchmarks (run by us), with independently verified accuracy numbers
3. A new unified tool that combines the best approaches

**Scope clarification (per issue #142):** This paper surveys high-level modeling and simulation methods FOR machine learning workloads — NOT machine learning-based performance modeling techniques. The focus is on tools and methods (analytical models, simulators, hybrid approaches) that predict/model performance of ML workloads, not on using ML to build performance models.

## Paper Contributions

### Contribution 1: Systematic Survey with Taxonomy
- Comprehensive literature review of performance modeling and simulation methods for ML workloads
- Novel taxonomy that classifies approaches by methodology, target hardware, and workload coverage
- **Systematic methodology**: documented search terms, databases, inclusion/exclusion criteria
- Identification of gaps and trends in the field

### Contribution 2: Third-Party Evaluation
- Define common benchmark suite for fair comparison across tool categories
- Execute all tools ourselves on the same benchmarks
- **Run our own accuracy experiments** — do NOT trust accuracy numbers from papers (per issue #143)
- Evaluate on multiple dimensions: **accuracy**, **ease of use**, **performance**, and **extensibility**
- Report which tools excel and which fall short, with quantitative results

### Contribution 3: Unified Tool Architecture (ZZZ)
- Document architecture design combining best methods from each category
- Show integration patterns and target use cases
- **Implement working prototype** (per issue #153 — this is an important contribution, not deferred)

## Quality Requirements

- **Page count**: Paper must be close to the page limit (11 pages), no more than half a page short (per issue #140)
- **Accuracy claims**: All accuracy numbers must be independently verified by running experiments, not just cited from papers (per issue #143)
- **Scope**: Survey is about modeling/simulation FOR ML workloads, NOT ML-based modeling (per issue #142)

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
- **Implement prototype** (reinstated per issue #153 — important contribution, assigned to Forge)

### M9: First Submission Draft (Target: Week 28) ✅ COMPLETE
- First complete draft with C1 + C2 + C3
- 8 pages, PDF committed
- **Review verdict: Reject (3/10)** — major revisions needed

### M10: Pre-Submission Polish (v1) ✅ COMPLETE
- Fixed paper count claim, added missing related work, added threats to validity

---

### M11: Scope Correction and Methodology (ACTIVE)

The external review (#141) identified fundamental issues. This milestone addresses the most critical structural problems.

**Key issues to fix:**
1. **Scope alignment** — Reframe paper to clearly survey high-level modeling/simulation FOR ML workloads (not ML-based modeling). Remove or reposition content about ML-based performance prediction that doesn't fit scope
2. **Systematic methodology section** — Add description of search databases, search terms, inclusion/exclusion criteria, and paper selection process
3. **Fix coverage claim** — Align "over 60 papers" claim with actual reference count, or expand references to match
4. **Fix Figure 1 inconsistencies** — Ensure all works in timeline figure are cited in references
5. **Fix reference formatting** — Remove "et al." in author lists, remove editorial annotations from bibliography entries
6. **Fix submission metadata** — Remove "#NaN" placeholder

### M12: Deepen Analysis and Expand Coverage

Address the review's criticism that analysis is shallow and coverage is incomplete.

1. **Expand to ~60 actual cited references** — Add missing categories: simulation acceleration, compiler cost models, memory system modeling tools, LLM inference cost calculators, workload characterization tools
2. **Deepen analysis per tool** — For each surveyed tool, discuss: conditions where it breaks down, limitations, failure modes, comparison to alternatives on same workloads
3. **Strengthen taxonomy** — Populate matrix with paper counts per cell, identify empty cells as research opportunities, analyze why certain combinations work
4. **Normalize comparisons** — Stop grouping accuracy numbers measured on different workloads/hardware. Either run common benchmarks or explicitly discuss incomparability

### M13: Independent Accuracy Verification

Per issue #143: Do not trust reported accuracy numbers. Run experiments.

1. **Expand evaluation suite** — Add more tools to hands-on evaluation (GRANITE, HELP, LitePred, NeuSight if accessible)
2. **Run common workloads** — Execute multiple tools on same workloads (e.g., ResNet-50, GPT-2 inference) for normalized comparison
3. **Report measured vs. claimed accuracy** — Document discrepancies between paper-reported and independently-measured results
4. **Update Section 7** with expanded, independently-verified evaluation results

### M14: Paper Expansion to Page Limit

Per issue #140: Paper must be close to 11-page limit (currently 8 pages).

1. **Expand paper to 10.5-11 pages** using content from M11-M13
2. **Add systematic methodology section** (~0.5 page)
3. **Expand survey coverage** with deeper analysis (~1-2 pages)
4. **Expand evaluation section** with new experimental results (~0.5-1 page)
5. **Add notation table/glossary** for cross-community accessibility
6. Final formatting and polish

### M15: Final Review and Submission

1. **Internal review** — Crit provides fresh review of revised paper
2. **Address remaining reviewer concerns** from #141
3. **Verify all quality requirements met**: page count, accuracy verification, scope alignment
4. **PDF rebuild and commit**
5. **Final submission**

## Current Status

**Project Status:** 🔄 **MAJOR REVISION IN PROGRESS**

The paper received a Reject (3/10) from external review (#141). Combined with human directives (#140, #142, #143), a significant revision is required before submission.

### Critical Review Summary (Issue #141)
| Dimension | Assessment |
|-----------|-----------|
| Coverage & Completeness | Poor — 24 refs cited vs 60+ claimed |
| Methodology | Absent — no systematic selection criteria |
| Analytical Depth | Weak — restates claims without synthesis |
| Taxonomy | Superficial — no quantitative gap analysis |
| Reproducibility Section | Good — structured rubric, useful findings |
| Presentation | Below standard — placeholder metadata, uncited figures |

### Human Directives
- **#140**: Paper must be close to 11-page limit (currently 8 pages, 3 pages short)
- **#142**: Scope is modeling FOR ML workloads, NOT ML-based modeling
- **#143**: Run experiments to verify accuracy — don't trust paper-reported numbers

### Next Steps
- M11: Fix scope, add methodology, fix presentation issues
- M12: Expand coverage and deepen analysis
- M13: Run independent accuracy experiments
- M14: Expand paper to page limit
- M15: Final review and submission
