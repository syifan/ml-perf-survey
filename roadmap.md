# Roadmap — ML Performance Survey Paper

**Last updated:** 2026-02-19 by Athena (Cycle 11 — M8 complete, defining M9)
**Target venue:** MICRO 2026
**Current state:** Paper at 907 lines, ~10.71 body pages (14 total - ~3.29 ref pages). Figures: 8. Refs: 92. All M7 work merged to main (PRs #285, #287). M8 complete: hostile review score 2/6 (Reject); prototype assessed (works, do NOT add results to paper). Human approved up to 13 pages for now.

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

### M8: Hostile Critical Review + Prototype Check (8 cycles) ✅ COMPLETE
Hostile review score: **2/6 (Reject)**. Key finding: "independent verification" claim undermined by no GPU hardware; only 5/22 tools evaluated; composition gap not novel without mechanism. Prototype works but results should NOT be added (too tight on pages, not novel). Human directives (#3): add modern models, fix figure text, relax squeeze, generate GPU scripts, evaluate all tools, ASTRA-sim 3.0.

### M9: Address Critical Review Findings (12 cycles) ← CURRENT
Fix the blocking issues from Diana's hostile review and address all human directives from issue #3. Paper may expand to 13 pages temporarily (human approved). GPU scripts for human to run on real hardware. Evaluate more tools.

**P0 tasks (must complete):**
1. **GPU experiment scripts** — Generate runnable scripts + Dockerfiles for NeuSight/Timeloop/ASTRA-sim/VIDUR on H100/A100. Create GitHub issues for human to run. Remove "our platform lacks discrete GPUs" line.
2. **Expand tool evaluation** — Evaluate 5+ additional tools (SimAI, Habitat, MAESTRO, Paleo, Accel-Sim). Document clearly whether each runs and with what caveats.
3. **ASTRA-sim 3.0** — Update to version 3.0, re-run benchmarks, document version change.
4. **Literature search** — Full new sweep for 2025-2026 papers. Find "The Path Forward Beyond Simulators." Update Figure 1 and Table 2.

**P1 tasks (high priority):**
5. **Fix figure text** — All figure text must be ≥\small size (same as main text). Fix all overlapping labels.
6. **Relax text squeeze** — Remove extreme LaTeX spacing overrides. Up to 13 pages allowed now. Cut low-value content instead of squeezing.
7. **Reframe verification claim** — Change to "third-party evaluation focusing on accuracy and feature coverage."
8. **Expand benchmark suite** — Add QWen-2.5, DeepSeek-V2/V3, diffusion models. Target 32-40 scenarios. Create larger table. Name it formally. Remove "Concrete benchmark parameterization" paragraph once table covers it.
9. **Remove boilerplate** — Remove "Confidential Draft — Do NOT Distribute!!" subtitle. Handle \todo{} macro.
10. **Fix narrative order** — Talk about what tools DO before what they lack ("Three gaps emerge" issue).
11. **Writing style consistency** — Section 6 style must match Sections 4-5.
12. **Background section** — Either expand or merge into Introduction (currently too short to stand alone).

**Pass/fail for Apollo:**
- At least 8 tools evaluated (or documented failure modes) — up from 5
- ASTRA-sim 3.0 results in paper
- GPU experiment scripts exist and are filed as GitHub issues
- At least 3 new 2025-2026 papers found and cited
- No figure has tiny/overlapping text
- Text squeeze removed (sections readable)
- Benchmark suite has ≥32 scenarios including modern models (QWen, DeepSeek, diffusion)
- "Confidential Draft" subtitle removed
- Verification claim reframed (no "novel evaluation methodology" overclaim)
- Paper ≤13 pages (body)

### M10: Red Team Review + Submission (8 cycles)
3-reviewer red team per #156, final fixes, submission PDF.

**Tasks:**
1. Three independent reviewers: (1) overall critical, (2) paragraph-by-paragraph, (3) comparative vs peer papers
2. Fix all issues
3. Final quality verification (pages ≤11, figures ≥8, refs ≥80, accuracy claims verified)
4. Submission-ready PDF

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
- **M8**: Hostile review (2/6) + prototype check. Fix list in tracker issue #4. Human directives in tracker issue #3.

## Lessons Learned

1. **Page count**: Must use PDF analysis, not line count estimates. CI reports 14 total pages; body = 14 - ref pages ≈ 10.71.
2. **Verification scope**: Keep Apollo criteria concrete and measurable. Subjective criteria cause endless fix rounds.
3. **Fix round discipline**: M7 burned 30 cycles (20 over budget) because verification was too strict on minor issues. Set clear pass/fail and stick to it.
4. **Worker timeouts**: Keep tasks small and focused. One clear deliverable per worker per cycle.
5. **Prototype gap**: Code was written but never discussed in the paper — always verify that implementation work gets reflected in the manuscript.

## Risk Assessment

- **Top risk (M9)**: Expanding from 5 to 8-10 tools requires many tools to actually run on M2 Ultra or produce documented failure modes. Some tools may be difficult to install.
- **Mitigation**: For each new tool, allocate one worker per tool. Document failures clearly — even failure cases count and strengthen the paper.
- **Top risk (M10)**: Page budget. After relaxing squeeze and adding content, paper may balloon to 13+ pages. Must trim at the end.
- **Lesson from M8**: The "independent verification" framing was the single biggest flaw. Reframing to "third-party evaluation" is a low-cost fix with high reward. Do it first.
