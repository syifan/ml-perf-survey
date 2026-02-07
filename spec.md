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
- **Figure density**: Paper needs significantly more figures — peer papers have 12-23 figures vs our 2 (per issue #159)
- **Reference count**: Target 80-100 cited references for a comprehensive MICRO survey (per issue #160)

## Process Requirements (per issue #156)

- **Incremental updates**: Work paragraph-by-paragraph, not whole-paper rewrites in one cycle
- **Review follow-up**: Crit posts reviews as GitHub issues, then follows up to verify fixes before re-reviewing
- **Red team structure**: 3 reviewers — (1) overall critical review, (2) paragraph-by-paragraph review, (3) comparative review against peer papers
- **Standing process**: Paper comparison against top-tier papers must happen every cycle (per issue #83)

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

### M11: Scope Correction and Taxonomy Redesign (ACTIVE — CRITICAL PATH)

The external review (#141) identified fundamental issues. Per Crit's analysis (#144), the taxonomy redesign is the critical missing piece — the current taxonomy (ML technique × target hardware × input representation) does not fit the corrected scope. This is closer to a rewrite than a revision.

**M11a: Scope reframing and content audit (~5-10 cycles)**
1. **Rewrite abstract, intro, and framing** to clearly position paper as surveying modeling/simulation FOR ML workloads
2. **Audit all sections** — identify content that must be removed or repositioned (e.g., ML-based performance prediction content that doesn't fit scope)
3. **Decide what to cut** — the plan must address removals, not just additions (per Crit's critique)

**M11b: Taxonomy redesign (~10-15 cycles)**
1. **Redesign taxonomy from scratch** for the corrected scope — classify by modeling methodology (analytical, simulation, hybrid), abstraction level, target hardware, and workload coverage
2. **Rebuild Table 1** to reflect new taxonomy dimensions
3. **Populate taxonomy matrix** with paper counts per cell, identify empty cells as research opportunities

**M11c: Presentation fixes (~3-5 cycles)**
1. Fix "#NaN" submission metadata placeholder
2. Fix Figure 1 inconsistencies — ensure all timeline entries are cited
3. Fix reference formatting — remove "et al." in author lists, remove editorial annotations
4. Add systematic survey methodology section (search databases, terms, inclusion/exclusion criteria)

### M12: Literature Expansion and Deep Analysis

Address shallow analysis and incomplete coverage. Work paragraph-by-paragraph (per #156).

**M12a: Literature expansion (~10-15 cycles)**
1. **Integrate uncited references** — 72 entries in bib but only 24 cited; integrate HIGH-priority uncited papers into the text
2. **Add new references** to reach 80-100 total cited (per #160) — target categories: simulation acceleration, compiler cost models, memory system modeling, LLM inference cost calculators, workload characterization, training-time prediction, distributed training simulation
3. **Every new reference must include substantive discussion** — at least 2-3 sentences of critical analysis per cited work (not just citation padding)

**M12b: Critical synthesis (~10-15 cycles)**
1. **Integrate Leo's critical synthesis** (PR #157) into paper text — tool-by-tool analysis of failure modes, limitations, and cross-cutting themes
2. **Deepen analysis per tool** — conditions where it breaks down, comparison to alternatives on same workloads
3. **Normalize comparisons** — stop grouping accuracy numbers measured on different workloads/hardware

### M13: Independent Accuracy Verification

Per issue #143: Do not trust reported accuracy numbers. Run experiments.

1. **Set up evaluation environments** — at minimum ASTRA-sim and one other accessible tool
2. **Define concrete benchmark suite** — specific workloads (ResNet-50, BERT-base, GPT-2), specific hardware targets, specific metrics
3. **Run common workloads** and collect measured results
4. **Report measured vs. claimed accuracy** — document discrepancies
5. **Update Section 7** with independently-verified evaluation results

### M14: Figure Creation and Paper Expansion

Per issues #140, #159: Paper needs 10.5-11 pages and significantly more figures.

**M14a: Add figures (~10-15 cycles)**
1. **Add at minimum 6-8 new figures** to approach peer paper density (target: 8-10 total figures)
2. Suggested figures: taxonomy visualization, accuracy comparison bar charts, tool coverage scatter plot, unified architecture diagram, methodology flowchart, timeline with more detail, evaluation comparison tables as figures
3. Each figure must be referenced and discussed in the text

**M14b: Paper expansion to page limit (~5-10 cycles)**
1. Integrate content from M11-M13 into paper
2. Verify paper reaches 10.5-11 pages
3. Final formatting and polish

### M15: Red Team Review and Submission

Implements the review process from #156. Three-phase review.

**M15a: Red team review (~5-10 cycles)**
1. **Crit** — Overall critical review posted as GitHub issue, then follow-up to verify fixes
2. **Paragraph reviewer** — Detailed paragraph-by-paragraph review: logic problems, writing quality, spec compliance
3. **Comparative reviewer** — Compare revised paper against top-tier peer papers

**M15b: Address review findings (~5-10 cycles)**
1. Fix all issues raised by red team
2. Red team verifies fixes

**M15c: Final submission (~3-5 cycles)**
1. Verify all quality requirements met: page count ≥10.5, reference count ≥80, figure count ≥8, accuracy verification, scope alignment
2. PDF rebuild and commit
3. Final submission

## Current Status

**Project Status:** PR MERGE BOTTLENECK — Work stalled waiting on Hermes

PRs #172, #174, #175 have been open for multiple cycles with no merge action. All downstream work (taxonomy redesign, content audit, figures) is blocked. Forge remains completely non-responsive — zero output across all assignments (#154, #155, #170) despite final warnings. The Forge track (accuracy experiments + unified tool prototype) must be reassigned or the project cannot meet human requirements #143 and #153.

**Score: 4/10 (Reject)** per Crit's latest review (#171). Up from 3/10 but still far from acceptable.

### Human Directives (unchanged)
- **#140**: Paper must be close to 11-page limit (currently ~8 pages)
- **#142**: Scope is modeling FOR ML workloads, NOT ML-based modeling
- **#143**: Run experiments to verify accuracy — don't trust paper-reported numbers
- **#153**: Unified tool prototype must be implemented, not deferred
- **#156**: Incremental work, review follow-up, red team of 3
- **#83**: Paper comparison against top-tier papers every cycle

### Key Metrics
| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| Paper pages | ~8 | 10.5-11 | STALLED (PRs not merged) |
| Cited references | ~63 (72 in bib) | 80-100 | STALLED (PR #172 adds 9 but not merged) |
| Figures | 2 | 8-10 | NOT STARTED |
| Tools evaluated independently | 0 verified | 4+ | BLOCKED (Forge non-responsive) |
| Unified tool prototype | Absent | Working prototype | BLOCKED (Forge non-responsive) |

### Worker Status
| Worker | Assigned | Status | Output |
|--------|----------|--------|--------|
| **Sage** | #145, #168 | Delivered PRs, awaiting merge | PR #174 (scope reframe), PR #175 (NaN/ref fixes) |
| **Leo** | #169, #161 | Delivered PR + taxonomy proposal | PR #172 (9 refs), taxonomy redesign proposal on #161 |
| **Maya** | #173, #162 | Assigned but no output yet | No PR for #173, no progress on figures |
| **Forge** | #170, #155, #154 | NON-RESPONSIVE | Zero output. Must be replaced or reassigned. |
| **Crit** | #171, #164 | Done | Review posted, red team protocol designed |

### Open PRs (URGENT — need Hermes to merge)
- **PR #175** (Sage) — NaN metadata + reference formatting fixes → closes #168
- **PR #174** (Sage) — Scope reframe: abstract, keywords, intro → partially addresses #145
- **PR #172** (Leo) — Integrate 9 uncited references → closes #169

### Active Issue Map

**BLOCKED on PR merge (Hermes must act):**
1. **#168** — Fix NaN metadata → PR #175 open
2. **#145** — Scope reframe → PR #174 open
3. **#169** — Integrate uncited references → PR #172 open

**Assigned but no output:**
4. **#173** — Maya: 14 foundational refs (no PR yet)
5. **#170** — Forge: ASTRA-sim experiment (no activity)
6. **#162** — Maya: Figures (no activity)

**Unblocked after PRs merge:**
7. **#161** — Taxonomy redesign — Leo has proposal ready, needs approval then implementation
8. **#163** — Content audit — blocked on #145 merge
9. **#146** — Survey methodology section

**CRITICAL — no worker producing output:**
10. **#155** — Independent accuracy experiments (Forge non-responsive)
11. **#154** — Unified tool prototype (Forge non-responsive)
12. **#176, #177, #178** — Individual figure issues (unassigned)
13. **#179** — Deepen per-tool analysis (unassigned)

**Longer-term:**
14. **#160** — Expand to 80-100 cited refs
15. **#164** — Red team review process (protocol ready, needs 2 new hires)

### Critical Path

The two biggest blockers right now:
1. **Hermes must merge PRs #172, #174, #175** — everything downstream depends on this
2. **Forge must be fired and replaced** — accuracy experiments (#143) and unified tool (#153) are human requirements that have zero progress after 5+ cycles

### Next Steps
1. **Hermes**: URGENT — merge PRs #172, #174, #175
2. **Apollo**: Fire Forge, hire replacement for accuracy experiments (#155, #170) and unified tool (#154)
3. **Leo**: After PR #172 merges, implement taxonomy redesign (#161) based on approved proposal
4. **Sage**: After PRs merge, tackle #146 (methodology section) and finish #145 (conclusion reframe)
5. **Maya**: Deliver #173 (refs) and start on figures (#162, #176-178)
6. **Crit**: Review PRs before merge, then standby for next review cycle after content stabilizes
