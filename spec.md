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

**Project Status:** CLOSING THE GAP — merge PRs #196 and #197, then enter quality phase

Last cycle was highly productive. Hermes merged 5 PRs (#175, #186, #187, #188, #189), landing ~800 lines. Then workers delivered another round: Leo's PR #196 (+265 lines: expanded Section 8, related surveys, 15 new refs) and Sage's PR #197 (+150/-37 lines: merged tables, 2 new figures). Crit posted fresh review scoring **5/10 (Weak Reject)** on #185, and a content audit on #163.

**Score: 5/10 (Weak Reject)** per Crit's latest review (#185). Up from 4.5/10. This review was done BEFORE PRs #196 and #197 — once those merge, the two biggest weaknesses (thin evaluation, no related work) are addressed. Expected score: **6-7/10**.

### Human Directives
- **#140**: Paper must be close to 11-page limit
- **#142**: Scope is modeling FOR ML workloads, NOT ML-based modeling
- **#143**: Run experiments to verify accuracy — don't trust paper-reported numbers
- **#153**: Unified tool prototype must be implemented, not deferred
- **#156**: Incremental work, review follow-up, red team of 3
- **#83**: Paper comparison against top-tier papers every cycle
- **#195** (NEW): Crit must review each paper version independently, without referencing prior reviews

### Key Metrics
| Metric | Current (main) | After PRs merge | Target | Status |
|--------|----------------|-----------------|--------|--------|
| Paper lines | ~1125 | ~1340 (~10.5-11 pages) | 10.5-11 pages | CLOSE TO TARGET |
| Cited references | ~71 | 86 | 80-100 | MET (after PR #196) |
| Figures | 5 | 7 | 8-10 | CLOSE (need 1-3 more) |
| Tools evaluated independently | 0 verified | 0 verified | 4+ | Flux working on ASTRA-sim |
| Unified tool prototype | Absent | Absent | Working prototype | NOT STARTED |

### Worker Status
| Worker | Status | This Cycle Output |
|--------|--------|-------------------|
| **Leo** | Top performer | PR #196: expanded Section 8 (+84 lines), related surveys subsection, 15 new refs |
| **Sage** | Strong output | PR #197: merged Tables 1+2, decision flowchart fig, speed-accuracy scatter fig |
| **Crit** | Delivered review + audit | Issue #185: fresh review 5/10. Issue #163: content audit (~1.8 cols recoverable) |
| **Flux** | Assigned ASTRA-sim | Issue #194: execute ASTRA-sim experiment (in progress) |

### Open PRs (2 — Hermes must merge)
- **PR #196** (Leo) — Expanded eval section, related surveys, 15 refs → closes #190, #191, #173
- **PR #197** (Sage) — Merged tables, decision flowchart, scatter plot → closes #192, #193

### Active Issue Map

**Has PR, awaiting merge:**
1. **#190** — Expand Section 8 → PR #196
2. **#191** — Related surveys section → PR #196
3. **#173** — Integrate foundational refs → PR #196
4. **#192** — Merge Tables 1+2 → PR #197
5. **#193** — Decision flowchart + scatter plot → PR #197

**In progress (no PR yet):**
6. **#194** — Execute ASTRA-sim experiment (Flux)
7. **#163** — Content audit (Crit completed analysis, needs implementation)

**Ready for next work:**
8. **#155** — Independent accuracy experiments (Flux, after ASTRA-sim runs)
9. **#160** — Expand to 80-100 refs — will be MET after PR #196 (86 refs)
10. **#164** — Red team review process (deploy after content stabilizes)
11. **#162** — Add figures (target 8-10, at 7 after PRs — need 1-3 more)

**Longer-term:**
12. **#154** — Unified tool prototype (Flux after ASTRA-sim)
13. **#153** — Prototype must be implemented, not deferred

**Needs new issues (from Crit review #185, not yet addressed):**
14. Add synthesis paragraphs to Section 5 (thematic analysis, not just tool catalog)
15. Reorder Sections 7/8 (evaluation before challenges)
16. Fix abstract tool count claim ("over 50" vs actual ~25 unique tools)
17. Add paragraph on commercial/proprietary tool scope limitation
18. Compress tangential content per Crit's content audit (#163)

### Critical Path

**Phase 2 (current): Close the gap to 10.5-11 pages and address structural issues.**
- Hermes merge PRs #196 and #197 (HIGHEST PRIORITY)
- Flux runs ASTRA-sim, gets real results into Section 8
- Implement content audit recommendations (compress tangential content)
- Add synthesis paragraphs to Section 5
- Reorder sections (eval before challenges)
- Fix abstract claims

**Phase 3 (next 5-10 cycles): Quality polish and verification.**
- Crit: independent fresh review per #195 (no memory of prior reviews)
- Red team review (#164) with full 3-reviewer protocol
- Flux: accuracy verification results from ASTRA-sim
- Unified tool prototype (#154) — start after ASTRA-sim
- Add 1-3 more figures (architecture diagram, etc.) to reach 8-10
- Final page count and formatting

### Next Steps
1. **Hermes**: Merge PRs #196 and #197 immediately. Then assign new work.
2. **Leo**: After PR merges, add synthesis paragraphs to Section 5 (thematic analysis tying tools together). Reorder Sections 7/8. Fix abstract tool count.
3. **Sage**: After PR merges, implement content audit cuts (compress PIM/memory/LLM-optimization tangential content per Crit #163). Add architecture diagram figure.
4. **Flux**: Execute ASTRA-sim experiment (#194). Report quantitative results for Section 8. Then begin unified tool prototype (#154).
5. **Crit**: Fresh independent review per #195 (treat paper as new submission, no prior review memory). Then review PRs #196/#197 if not yet merged.
6. **Athena**: Create new baby-step issues for Phase 2 remaining gaps.
