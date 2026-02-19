# Roadmap — ML Performance Survey Paper

**Last updated:** 2026-02-18 by Athena (Cycle 11 — fresh orchestration start)
**Target venue:** MICRO 2026
**Current state:** Paper at 907 lines, ~10.71 body pages (14 total - ~3.29 ref pages). Figures: 8. Refs: 92. All M7 work merged to main (PRs #285, #287). Unified pipeline section exists but prototype results are NOT in the paper.

## Current Assessment

### What's Done
- **M1-M7 complete**: Literature, taxonomy, deep analysis, draft, evaluation restructuring, compression
- **Paper metrics**: 907 lines, 10.71 body pages, 8 figures, 92 refs, 79.3% eval ratio
- **5 tools evaluated**: NeuSight, ASTRA-sim, VIDUR, Timeloop, nn-Meter across 28-scenario benchmark
- **Key findings established**: Self-reported accuracy unreliable (NeuSight 2.3% claimed vs 5.87-27.10% measured), composition gap (2-9% kernel → 10-28% model), nn-Meter dependency rot
- **Unified pipeline section**: Architecture figure exists (5-layer pipeline), composition gap identified
- **Prototype code**: Working code in `/prototype/` with adapters for 5 tools
- **All compression work merged** to main (PRs #285, #287)

### What's Missing
1. **Prototype not discussed as implemented contribution** — code exists but paper doesn't mention running it or present results from it. Spec #153 requires a working prototype, not just an architecture diagram.
2. **Hostile critical review** (#258) — never executed. Paper hasn't been reviewed by a hostile top-tier reviewer.
3. **Red team review** (#164, #156) — 3-reviewer protocol never executed.
4. **Stale issue cleanup** (#328) — many open verification issues from M7 rounds.

### Human Directives (Open)
- **#198**: Deep, controversial insights + 50% evaluation weight ✅ MET (79.3% eval)
- **#243**: No rubrics — accuracy-centered eval ✅ DONE
- **#244**: Evaluate ALL simulators + combine them ✅ DONE
- **#246**: NS-3-style network sim discussion ✅ DONE
- **#250**: LLM-focused benchmark suite ✅ DONE
- **#258**: Hostile top-tier conference reviewer — NOT YET EXECUTED
- **#328**: Clean up stale issues — NOT YET DONE

## Remaining Milestones

### M8: Hostile Critical Review + Prototype Check (8 cycles) ← NEXT
A hostile reviewer assesses the paper as a MICRO 2026 submission. Simultaneously, verify the prototype works and determine if prototype results should be added to the paper (or if the current architecture discussion suffices given page constraints).

**Tasks:**
1. Build PDF from main, verify all quality metrics
2. Hostile critical review — reviewer acts as skeptical MICRO PC member, writes detailed review with score
3. Assess prototype — run it, determine if results add value within page budget
4. Produce prioritized fix list from review findings
5. Clean up stale tracker issues per #328

**Pass/fail for Apollo:**
- Hostile review completed with specific, actionable findings
- Prototype assessed (works/doesn't work, results add value or not)
- Prioritized action list produced
- Stale issues cleaned up

### M9: Address Review Findings + Final Content (10 cycles)
Fix all issues from hostile review. If prototype results add value, integrate them. Ensure paper is submission-quality.

**Tasks:**
1. Fix all critical issues from M8 review
2. Integrate prototype results if warranted (manage page budget)
3. Verify all quality metrics maintained
4. All content finalized

### M10: Red Team Review + Submission (8 cycles)
3-reviewer red team per #156, final fixes, submission PDF.

**Tasks:**
1. Three independent reviewers: (1) overall critical, (2) paragraph-by-paragraph, (3) comparative vs peer papers
2. Fix all issues
3. Final quality verification (pages, figures, refs, accuracy claims)
4. Submission-ready PDF

## Completed Milestones

- **M1-M4**: Literature discovery, taxonomy, deep analysis, paper draft
- **M5**: Fix reject-level issues — page limit, Pareto methodology, contribution framing
- **M6/M6a**: Evaluation restructuring — accuracy-centered eval, 50% eval ratio, methodology contribution
- **M7**: 24-pass compression (1217→907 lines), figures 5→8, refs 92, body pages 10.71. Merged to main via PRs #285, #287.

## Lessons Learned

1. **Page count**: Must use PDF analysis, not line count estimates. CI reports 14 total pages; body = 14 - ref pages ≈ 10.71.
2. **Verification scope**: Keep Apollo criteria concrete and measurable. Subjective criteria cause endless fix rounds.
3. **Fix round discipline**: M7 burned 30 cycles (20 over budget) because verification was too strict on minor issues. Set clear pass/fail and stick to it.
4. **Worker timeouts**: Keep tasks small and focused. One clear deliverable per worker per cycle.
5. **Prototype gap**: Code was written but never discussed in the paper — always verify that implementation work gets reflected in the manuscript.

## Risk Assessment

- **Top risk**: Hostile review may reveal structural issues requiring significant rewrites within tight page budget.
- **Mitigation**: Review first, then prioritize fixes by impact. Don't try to fix everything — focus on what moves the score most.
- **Reduced risks**: Content is strong, metrics are met, eval ratio is excellent, prototype code exists.
