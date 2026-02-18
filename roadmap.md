# Roadmap — ML Performance Survey Paper

**Last updated:** 2026-02-18 by Athena (Cycle 10)
**Target venue:** MICRO 2026
**Current state:** Paper at 908 lines, CI shows 14 total pages. Figures: 8. Refs: 92. M7 nearly complete — final blocker is body page count verification.

## Diagnosis

The human (issue #198) identified three critical requirements:
1. **Deep, surprising, controversial insights** — not a catalog
2. **At least 50% of paper weight on third-party evaluation with novel methodology**
3. **Guide future research** with concrete agendas

### Human Directives (Open)
- **#198**: Paper needs deep, controversial insights and 50% evaluation weight
- **#243**: No rubrics — evaluation must be accuracy-centered ✅ DONE
- **#244**: Evaluate ALL simulators + combine them for optimal solution ✅ DONE (5 tools evaluated, unified pipeline in Sec 8)
- **#246**: Discuss whether detailed NS-3-style network sim is needed ✅ DONE (Sec 8)
- **#250**: Define LLM-focused benchmark suite ✅ DONE (28-scenario suite in Sec 6)
- **#258**: Critical reviewer must review as hostile top-tier conference reviewer (skill rewritten, not yet executed)
- **#327**: Human asked to check GitHub issue #286 — responded, that was an old M6b task superseded by M7
- **#328**: Human asked to clean up issues — many stale verification issues remain open from M7 verification rounds

## What M7 Accomplished (30 cycles — deadline missed)

- **Paper compressed**: 1217 lines → 908 lines (cut ~309 lines from non-eval sections)
- **Figures added**: 5 → 8 figures (added accuracy bar chart, architecture diagram, coverage heatmap)
- **Eval ratio**: 79.3% (well above 50% target)
- **References**: 92 (above 80+ target)
- **CI**: Compiles cleanly

### What M7 Did NOT Complete
- **Body page count: UNCERTAIN** — CI shows 14 total pages. Apollo estimated body = ~10.35-11.35 pages depending on layout. Must be definitively confirmed at 10.5-11.
- **Eval section integrity**: Apollo's FAIL was due to pass 14 cutting eval sections. These were reverted in pass 15. Now confirmed intact (Secs 6-7 = 779 lines, identical to pre-pass14).
- **PR not merged to main**: All work is on `marco/compress-m7-pass7` branch, not merged.

### Lessons Learned
1. **Page count verification must use PDF analysis, not line count** — 13 vs 14 pages was a persistent confusion throughout M7. Need to count body pages directly in the PDF.
2. **CI multi-pass LaTeX reports different page counts** — the final `Output written` line in the last pass is the truth. This was 14 pages in the most recent CI run.
3. **Apollo's verification process creates noise** — 10+ open verification issues remain from M7. Should bulk-close resolved ones before re-submission.
4. **Body page count is 14-ref_pages = 14-2.65 = ~11.35** — over the 11-page limit. Need ~3-5 more lines cut from non-eval sections, OR accept 11.35 if template allows slight overrun.
5. **Fix rounds burned most of the 30 cycles** — Apollo's FAIL sent team into 15+ cycles of minor fixes. Need tighter Apollo verification criteria.

## Strategy (Revised)

M7 is almost done. The narrow remaining gap:
1. **Definitively measure body page count** from PDF (not estimation)
2. **If body > 11 pages**: cut 5-15 more lines from non-eval sections (Intro, Background, Conclusion only — Taxonomy and Survey already minimal)
3. **Open a PR from marco/compress-m7-pass7 to main** and merge it
4. **Close stale verification issues** per human directive #328

## Milestones (Revised)

### M7-final: Verify Page Count, Cut If Needed, Merge PR ← NEXT
Close out M7 with a verified merge to main.

**Specific tasks:**
1. **Measure body pages** — download PDF from CI artifact, count body pages directly (not estimate). Body pages = total - reference pages.
2. **If body > 11.0**: cut 10-15 lines from non-eval sections (Intro paragraphs, Background, Conclusion). DO NOT touch Secs 6-7.
3. **Open PR** from `marco/compress-m7-pass7` to `main` with all compression work
4. **Merge the PR** once CI passes
5. **Close stale issues** — bulk close all open verification issues from M7 that are resolved (#329, #330 and others per human #328)

**Pass/fail criteria for Apollo:**
- Body pages 10.5-11.0 measured from PDF (direct count, not estimation)
- 8+ figures
- 92+ references
- Secs 6-7 unchanged from pre-pass14 (75eeb6f) — verify with diff
- CI passes
- PR merged to main

**Budget: 10 cycles**

### M7b: Hostile Critical Review + Fix Round
Fresh hostile review per #258, then fix all issues. Reviewer must approach paper as hostile top-tier conference reviewer, NOT checking against our internal checklist.
- **Budget: 10 cycles**

### M8: Unified Tool Prototype Integration
Describe prototype in paper, ensure it's a real contribution.
- **Budget: 10 cycles**

### M9: Red Team Review + Final Polish
Three-reviewer red team, fix issues, final PDF.
- **Budget: 10 cycles**

## Completed Milestones

- M1-M4: Literature discovery, taxonomy, deep analysis, paper draft
- M5: Fix reject-level issues — page limit, Pareto methodology, contribution framing
- M6 (partial): Evaluation restructuring — paper restructured, MTAP removed, accuracy-centered eval added, taxonomy compressed
- M6a (partial): PRs merged, eval at 50%, methodology contribution articulated. Failed page limit and figure count.
- M7 (partial — deadline missed after 30 cycles): Compression 1217→908 lines, figures 5→8, refs 92. Failed on body page count verification and PR merge.

## Risk Assessment

- **Biggest risk:** Body page count still uncertain — 10.35 vs 11.35 estimates vary. Must count directly from PDF.
- **Second risk:** Apollo's verification is strict; minor issues cause FAIL and fix rounds. Mitigation: provide Apollo with concrete PDF-measured page count, not line estimates.
- **Reduced risks:** Content is solid. Figures added. References exceed target. Eval ratio excellent.
