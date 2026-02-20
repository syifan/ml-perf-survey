# Roadmap — ML Performance Survey Paper

**Last updated:** 2026-02-19 by Athena (Cycle 13 — M10 complete, defining M11)
**Target venue:** MICRO 2026
**Current state:** Paper at 882 lines, 10 content pages (13 total w/ 3 ref pages). M10 complete: 7/7 quantitative criteria passed (Raj). Red team ran, all findings fixed (Leo). Human now requests comparative within-category evaluation and H100 results integration.

## Current Assessment

### What's Done (M1–M10)
- **M1-M4 complete**: Literature, taxonomy, deep analysis, paper draft
- **M5-M8 complete**: Fix rounds, evaluation restructuring, compression, hostile review
- **M9 complete**: GPU scripts, 10 tools evaluated (5 full + 5 deployment), benchmark suite (36 scenarios), multi-backend scripts
- **M10 complete**: Paper expanded to 10 content pages, 8 figures, 98 refs. 3-reviewer red team (Diana hostile, Felix paragraph, Maya comparative). All findings fixed. Raj verified 7/7 pass.
- **Paper metrics**: 882 lines, 10 content pages, 13 total PDF pages, 8 figures, 98 refs

### Key Findings Established
- Self-reported accuracy unreliable (NeuSight 2.3% claimed vs 5.87–27.10% measured)
- Composition gap (5–9% kernel → 10–28% model error) dominates total error
- nn-Meter fails due to dependency rot
- 50% of PerfSim-Survey-2026 scenarios lack tool support
- Tools are complementary, not competing (no two tools overlap in scope)

### New Human Directives (Open — drive M11)
- **#36**: "More tools need to be evaluated. Each category needs to have comparison or multiple tools. For NeuSight, we can compare Paleo, Path Forward, etc. For ASTRA-sim, we can compare with TrioSim."
- **#35**: "How is the H100 results used?" — H100 ground-truth data exists in scripts/gpu_experiments/results/ but paper line 123 still says "hardware we lack (e.g., H100 GPUs)". Must integrate.
- **#37**: "Let's remove the page limit for now. Write concisely, but ignore the limit." — Page constraint lifted.
- **#3** (partially open): Several items from human's original suggestion list remain relevant (evaluate all tools, Paleo/Path Forward missing, writing style consistency, supplementary materials).

### Previous Human Directives (Closed)
- **#198**: Deep insights + 50% eval weight ✅ MET
- **#243/#244**: Accuracy-centered eval ✅ DONE
- **#246**: NS-3 network sim discussion ✅ DONE
- **#250**: LLM-focused benchmark suite ✅ DONE
- **#258**: Hostile reviewer ✅ DONE
- **#25**: Multi-backend GPU scripts ✅ DONE
- **#21**: Page count ✅ DONE (M10)

## Remaining Milestones

### M10: Paper Expansion + Red Team Review ✅ COMPLETE
All 7/7 quantitative criteria passed. Paper at 10 content pages. Red team ran 3-reviewer protocol. All findings fixed and verified.

### M11: Comparative Tool Evaluation + H100 Integration (15 cycles) ← CURRENT

The human's core feedback is that the evaluation is too narrow: each category has at most one fully-evaluated tool, preventing within-category comparison. This must change. Additionally, H100 ground-truth results exist but aren't used.

**P0 tasks (blocking):**
1. **Within-category comparative evaluation**: Evaluate additional tools to enable head-to-head comparison:
   - **GPU kernel prediction**: NeuSight vs Paleo vs Path Forward approach. Attempt to run Paleo on the same workloads as NeuSight and compare accuracy.
   - **Distributed training**: ASTRA-sim vs TrioSim. Attempt to run TrioSim and compare with ASTRA-sim results.
   - **Other categories**: Identify which other categories can have a second tool evaluated. Prioritize feasible tools (those with Docker/working artifacts).
2. **Integrate H100 ground-truth results**: The human ran PerfSim-Survey-2026 on H100. Results are in scripts/gpu_experiments/results/. Remove "hardware we lack" claim. Use H100 data as ground-truth for validating tool predictions where applicable.
3. **Update paper evaluation sections**: Add comparison subsections showing head-to-head results within categories. Update cross-tool comparison table and findings.
4. **Literature search for newly-evaluated tools**: Ensure any newly-evaluated tools are properly cited and contextualized in the survey section.

**P1 tasks (important):**
5. **Update figures**: Add comparison charts (bar charts or tables) showing within-category accuracy comparisons.
6. **Remaining items from #3**: Fix writing style consistency, consider supplementary materials for detailed configs.

**Pass/fail for Apollo (M11):**
- At least 3 categories have 2+ tools evaluated with head-to-head comparison on same workloads
- H100 ground-truth data integrated into evaluation section; no "hardware we lack" claim remains
- Each new tool evaluation includes: setup effort, accuracy measurement, comparison with category peer
- No regression: existing content quality maintained (≥8 figures, ≥80 refs, no overclaims)
- All stated findings still supported by evidence

### M12: Final Red Team + Submission (8 cycles)
- Fresh 3-reviewer red team on updated paper
- Address findings
- Final verification and submission

## Lessons Learned

1. **Page count**: Use PDF analysis (pdfinfo), not line count. Distinguish content pages from reference pages.
2. **Verification scope**: Apollo criteria must be concrete and measurable. Subjective criteria cause endless fix rounds.
3. **Fix round discipline**: M7 burned 30 cycles; M9 had 4 verification passes. Set clear pass/fail and stick to it.
4. **Worker timeouts**: One task per worker per cycle. Keep tasks focused.
5. **Prototype gap**: Code was written but never discussed in paper — always ensure implementation work appears in manuscript.
6. **Compression danger**: M7's compression from 907→715 lines lost 3 pages of content. Don't compress below the page limit.
7. **Script portability**: Always test scripts on multiple GPU backends from the start.
8. **Evaluation breadth matters**: Reviewing 25 tools but only evaluating 5 leaves the paper vulnerable to "why didn't you evaluate X?" criticism. Within-category comparison is essential for a survey.

## Risk Assessment

- **Top risk (M11)**: Tool installation failures. Many tools have fragile dependencies (nn-Meter precedent). Budget cycles for failed attempts.
  - Mitigation: Attempt tool installs early. If a tool fails, document the failure (as with nn-Meter) and move on. Failed evaluations are still informative.
- **Top risk (M11)**: H100 results may not align with tool predictions, requiring narrative changes.
  - Mitigation: Be honest about discrepancies. They strengthen the paper's "self-reported accuracy is unreliable" finding.
- **Budget**: M11 allocated 15 cycles. If comparative evaluation takes >10 cycles, narrow scope to 2 categories instead of 3.
