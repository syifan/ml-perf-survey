# Roadmap — ML Performance Survey Paper

**Last updated:** 2026-02-19 by Athena (Cycle 12 — M9 complete, defining M10)
**Target venue:** MICRO 2026
**Current state:** Paper at 715 lines, 7 content pages (10 total w/ refs). M9 complete: 10/10 criteria passed (Elena), script portability fixed (Oscar). Paper needs expansion: MICRO limit is 10 pages excluding references.

## Current Assessment

### What's Done (M1–M9)
- **M1-M4 complete**: Literature, taxonomy, deep analysis, paper draft
- **M5-M8 complete**: Fix rounds, evaluation restructuring, compression (907→715 lines), hostile review
- **M9 complete**: GPU scripts filed (#290-294), 10 tools evaluated (5 full + 5 deployment), ASTRA-sim documented, 36 PerfSim-Survey-2026 scenarios, squeeze removed, claims reframed, boilerplate removed, multi-backend scripts (Oscar)
- **Paper metrics**: 715 lines, 7 content pages, 10 total PDF pages (3 ref pages), 8 figures, 92 refs

### Key Findings Established
- Self-reported accuracy unreliable (NeuSight 2.3% claimed vs 5.87–27.10% measured)
- Composition gap (2–9% kernel → 10–28% model error) dominates total error
- nn-Meter fails due to dependency rot
- 56% of PerfSim-Survey-2026 scenarios lack tool support

### What's Missing (M10 focus)
1. **Page count**: 7 content pages is well short of MICRO's 10-page limit. Need 3 more pages of substantive content.
2. **Red team review**: 3-reviewer protocol per spec #156 has never run on the current paper version.
3. **Synthesis depth**: Sections 5, 7, 8 are compressed and need richer analysis.
4. **Human issue #21**: Human flagged only 7 pages of visible content — must address.

### Human Directives (Open)
- **#198**: Deep, controversial insights + 50% evaluation weight ✅ MET (79.3% eval)
- **#243/#244**: Accuracy-centered eval, evaluate ALL tools ✅ DONE
- **#246**: NS-3-style network sim discussion ✅ DONE
- **#250**: LLM-focused benchmark suite ✅ DONE
- **#258**: Hostile top-tier reviewer ✅ DONE (Diana, score 2/6 → led to M9 fixes)
- **#25**: Multi-backend GPU scripts ✅ DONE (Oscar's commits)
- **#21**: "Only 7 pages of content" — OPEN → M10 must close this gap

## Remaining Milestones

### M9: Address Critical Review Findings ✅ COMPLETE
All 10 criteria passed. Script portability fixed. Paper expanded benchmark suite to 36 scenarios. GPU experiment issues filed #290-294.

### M10: Paper Expansion + Red Team Review (12 cycles) ← CURRENT

Expand the paper to fill the MICRO 10-page (excl. refs) limit with substantive content. Execute full 3-reviewer red team. Polish and prepare for submission.

**P0 tasks (blocking):**
1. **Expand paper to ~10 content pages**: Add ~3 pages of substantive content to Sections 5, 7, 8 and related work. Content must be high quality — deeper analysis, not padding. Priorities:
   - Section 5 (Survey of Approaches): More per-tool depth, comparison with alternatives, conditions where tools break down
   - Section 7 (Unified Pipeline): Concrete design, implementation details, integration patterns
   - Section 8 (Open Challenges): More specific research agenda with concrete problems
   - Related work: Position paper against survey papers more explicitly
2. **3-reviewer red team review**: (1) overall hostile review, (2) paragraph-by-paragraph, (3) comparative vs peer papers
3. **Address all red team findings**: Fix every identified issue
4. **Final verification**: Page count 9.5–10.5 content pages, refs ≥80, figures ≥8, all claims accurate

**Pass/fail for Apollo (M10):**
- Paper body is 9.5–10.5 content pages (use pdfinfo for total; subtract ~3 ref pages)
- All red team reviewer findings documented (as tracker issues or comments) and addressed
- No TODO markers, no "Confidential Draft" text, no overclaims
- Figure count ≥8, ref count ≥80
- All stated findings supported by evidence in the paper

### M11: Submission (4 cycles)
- Final page/format check per MICRO submission guidelines
- Generate camera-ready PDF
- Submission

## Lessons Learned

1. **Page count**: Use PDF analysis (pdfinfo), not line count. Distinguish content pages from reference pages.
2. **Verification scope**: Apollo criteria must be concrete and measurable. Subjective criteria cause endless fix rounds.
3. **Fix round discipline**: M7 burned 30 cycles; M9 had 4 verification passes. Set clear pass/fail and stick to it.
4. **Worker timeouts**: One task per worker per cycle. Keep tasks focused.
5. **Prototype gap**: Code was written but never discussed in paper — always ensure implementation work appears in manuscript.
6. **Compression danger**: M7's compression from 907→715 lines lost 3 pages of content. Don't compress below the page limit.
7. **Script portability**: Always test scripts on multiple GPU backends from the start.

## Risk Assessment

- **Top risk (M10)**: Adding 3 pages while maintaining quality. Risk of padding or dilution.
  - Mitigation: Assign experienced writer (Leo) with specific section targets. Review each addition.
- **Top risk (M10)**: Red team finds fundamental issues requiring another major revision.
  - Mitigation: Keep red team focused on current version; reject scope-expanding feedback.
- **Budget**: M10 allocated 12 cycles. If content expansion takes >6 cycles, cut scope on M11 instead.
