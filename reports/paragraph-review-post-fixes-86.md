# Paragraph-by-Paragraph Review After Fixes (Issue #86)

**Reviewer:** reviewer-paragraph
**Date:** 2026-02-14
**Branch:** paper-editor/reject-fixes-84
**Context:** Review conducted after fixes from issues #83 (human review #241) and #84 (reject review #242)

---

## Summary

The paper has improved substantially after the structural fixes. The abstract is concise, rubric language is removed, venue justification is reframed, and technical depth has increased in key areas. However, several issues remain, including one **critical contradiction** between the abstract and evaluation section.

**Issues found:** 18 total (2 High, 9 Medium, 7 Low)

---

## HIGH Priority Issues

### H1: Abstract contradicts Evaluation section on accuracy measurement

**Location:** Line 65 (Abstract) vs. Lines 738-739 (Section 6)

**Abstract (L65):** "independently measuring their performance and accuracy rather than relying on original claims"

**Evaluation (L738-739):** "No GPU hardware was available, so we **do not validate accuracy claims**. Instead, we evaluate *reproducibility*"

These statements directly contradict each other. The abstract claims the paper independently measures accuracy; the evaluation section explicitly says it does not. This is the most critical issue in the paper — a reviewer reading the abstract will expect accuracy validation and find none.

**Fix:** Change abstract line 65 to something like: "independently evaluating their reproducibility and usability rather than relying solely on original claims"

### H2: VIDUR evaluation uses different request counts for vLLM vs Sarathi

**Location:** Lines 765-767 and Table (L774-786)

vLLM was tested with 200 requests; Sarathi with 50. The paper then claims "Sarathi shows 12.2% lower simulated latency than vLLM" and "vLLM preempted 26.5% of requests vs. zero for Sarathi." Both comparisons are invalid with different load levels — higher load (200 requests) naturally causes more preemptions and potentially higher latency. The paper does not explain why different request counts were used or acknowledge this confound.

**Fix:** Either re-run with identical request counts, or add an explicit caveat that the comparison is illustrative rather than controlled.

---

## MEDIUM Priority Issues

### M1: "22 tools" count vs Table 2 listing only 14

**Location:** Line 63 (Abstract), Line 427 (Section 4.3)

Abstract says "22 tools." Table 2 (workload coverage, L397-425) lists only 14 tools. Line 427 says "of the 14 surveyed tools, 9 (64%) include CNN validation." The discrepancy between 22 and 14 is never explained. Are 8 tools excluded from workload coverage analysis? Why?

**Fix:** Add a note explaining which tools are included in Table 2 and why (e.g., "Table 2 shows the 14 tools for which workload validation data is available from the original papers").

### M2: Figure 5 caption still references a "dashed line" that doesn't exist

**Location:** Line 647-648

Caption says "The dashed line is an approximate visual guide, not a true Pareto frontier." But the figure's TikZ code (L596-649) contains no dashed line — the Pareto frontier was removed per issue #84 fix. The caption text referencing it was not updated.

**Fix:** Remove "The dashed line is an approximate visual guide, not a true Pareto frontier." from the caption.

### M3: "dynamicreasoning2026" citation used for diffusion models

**Location:** Line 428, Line 893

The citation `\cite{dynamicreasoning2026}` appears to be about "The Cost of Dynamic Reasoning: Demystifying AI Agents" (HPCA 2026), not about diffusion models. It's used in contexts mentioning "diffusion" workloads. While the cited paper analyzes AI infrastructure broadly, it may not specifically validate the claim about diffusion model performance modeling gaps.

**Fix:** Verify the citation content matches the claim, or find a more specific diffusion model reference.

### M4: AMALI's 23.6% error attribution to "GPU dynamic effects" unsupported

**Location:** Line 337

"AMALI's 23.6% MAPE illustrates GPU dynamic effects" — this causal attribution is speculative. AMALI's error could stem from modeling assumptions, missing compiler optimizations, or limited validation scope. Without citing AMALI's own error analysis, this claim is unfounded.

**Fix:** Change to "AMALI's 23.6% MAPE on GPUs illustrates the challenge of analytical GPU modeling" or cite AMALI's error breakdown.

### M5: Error ranges overlap without explanation

**Location:** Line 347 and Figure 3

"kernel-level tools achieve 2–3% error, model-level 5–12%, and system-level 5–15%." The model-level (5–12%) and system-level (5–15%) ranges overlap substantially, making the distinction unclear. Are these from specific tools? Averages? Best-case?

**Fix:** Specify the source of these ranges (e.g., "representative values from the best-performing tool in each category") and explain that overlap reflects the difficulty of precise error decomposition.

### M6: Accel-Sim MAPE improvement baseline unclear

**Location:** Line 536

"reverse-engineering improved Accel-Sim to 13.98% MAPE" — what was Accel-Sim's MAPE before? Table 3 says "10–20%" for Accel-Sim, and 13.98% falls within that range. Was this actually an improvement? What was the starting MAPE?

**Fix:** State the baseline MAPE explicitly, e.g., "reducing Accel-Sim's MAPE from X% to 13.98%."

### M7: ASTRA-sim scaling claim is mathematically inconsistent

**Location:** Lines 793-795

"communication overhead scales 5.76× for 4× more GPUs, matching ring All-Reduce complexity." Ring All-Reduce has O((N-1)/N) scaling for N nodes. Going from 2 to 8 GPUs, the expected scaling is approximately (7/8)/(1/2) = 1.75×, not 5.76×. The absolute cycle count scaling (574,289 → 3,307,886 = 5.76×) includes both the per-node communication volume increase AND the algorithm complexity increase, but the claim "matching ring All-Reduce scaling" oversimplifies. The 5.76× scaling exceeds what pure ring All-Reduce theory predicts.

**Fix:** Remove "matching ring All-Reduce complexity" or provide a more careful analysis of why 5.76× is expected.

### M8: NeuSight evaluation too thin

**Location:** Lines 824-826

Only 2 sentences describe the NeuSight evaluation. No quantitative results, no specific experiments described, no tables. Compare this to VIDUR (full table + 6 lines) and ASTRA-sim (full table + 8 lines). This thinness undermines the "hands-on evaluation" claim.

**Fix:** Add at minimum what workloads/kernels were tested, what outputs were produced, and a brief quantitative summary.

### M9: Table 4 scoring methodology unclear

**Location:** Lines 743-759

The reproducibility scores (Setup, Reproducibility, Usability) use fractional values (2.5, 3.5) on an unstated scale. What's the maximum per category? The total is "out of 10" but the three sub-scores don't always sum to 10 (VIDUR: 2.5+3.5+3=9, but Timeloop: 3+4+2=9). Is the maximum per dimension 4? 5? This isn't explained.

**Fix:** State the scoring scale for each sub-dimension in the table caption or text.

---

## LOW Priority Issues

### L1: Ground-truth measurement claim too narrow

**Location:** Line 224

"Ground-truth measurements rely on hardware performance counters (PAPI, LIKWID) or vendor profilers (Nsight Compute)." This is only true for metrics like FLOPS or cache misses. Wall-clock latency (the most common prediction target) is measured via timers, not performance counters.

**Fix:** Add "timing APIs" alongside performance counters.

### L2: "silent distribution shift" undefined

**Location:** Line 340

"risk *silent distribution shift*" — the term "silent" is important but never defined. Does it mean the model gives confident wrong predictions? That error is undetectable without ground truth?

**Fix:** Briefly define: "where models produce confident but erroneous predictions on inputs outside their training distribution."

### L3: Speculative decoding claim unexplained

**Location:** Line 565

"speculative decoding creates a moving target for all simulators" — interesting claim but unexplained. How does speculative decoding make simulation harder?

**Fix:** Add a brief clause: "as the variable acceptance rate makes latency distribution non-deterministic" or similar.

### L4: Architecture-specific evaluation confound not noted

**Location:** Line 737

All evaluations ran on Apple M2 Ultra (aarch64). Some tools may have x86_64-specific optimizations or dependencies. This is not discussed as a threat to validity.

**Fix:** Add to threats section (L880-884): "Additionally, our aarch64 evaluation platform may introduce architecture-specific confounds."

### L5: Frontier accuracy missing from Table 3 without explanation

**Location:** Line 502

Frontier shows "---" for accuracy. While Frontier may not report accuracy, the paper doesn't explain why this cell is blank, unlike PyTorchSim and TrioSim which have footnotes (N/A‡).

**Fix:** Use the same N/A‡ notation or add a footnote.

### L6: Figure 1 venue color categories are somewhat arbitrary

**Location:** Lines 157-162

The venue color legend separates "Architecture" (blue), "Systems" (green), "Mobile/Edge" (orange), "ASPLOS" (purple), and "ML Systems" (red). ASPLOS is a single venue given its own color, while MICRO/ISCA/HPCA share "Architecture." This categorization is inconsistent and not well-motivated.

**Fix:** Consider merging ASPLOS with Architecture or adding a brief justification for the separation.

### L7: Line 92 cites Timeloop for "specific hardware" surveys

**Location:** Line 92

"Existing surveys focus on ML *techniques* for modeling [granite2022] or specific hardware [timeloop2019]" — Timeloop is not a survey paper; it's a tool paper. Using it as an example of a "survey on specific hardware" is misleading.

**Fix:** Replace with an actual survey reference, or rephrase to "tool-specific documentation" rather than "surveys."

---

## Cross-Reference Verification

All `\ref{}` targets have matching `\label{}` definitions:
- 8 figures: timeline, tool-architecture, abstraction-levels, validation-bias, accuracy-speed, accuracy-comparison, reproducibility-scores, workload-coverage, error-composition → **9 figure labels found** ✓
- 5 tables: taxonomy-matrix, workload-coverage, survey-summary, evaluation-summary, vidur-results, astrasim-results → **6 table labels found** ✓
- All section/subsection labels matched ✓
- No orphaned labels (labels without references) detected
- No broken references (references without labels) detected

## Citation Verification

All `\cite{}` keys in main.tex were checked against references.bib citation keys. All keys are defined. No undefined citations found.

---

## Assessment of Previous Fix Effectiveness

Fixes from issues #83 and #84 have been largely effective:

| Fix Area | Status | Notes |
|----------|--------|-------|
| Abstract shortened | ✓ Fixed | Now 5 sentences, concise |
| Rubric scoring removed | ✓ Fixed | No rubric language found |
| Venue justification reframed | ✓ Fixed | Focuses on novel insights |
| Figs 5-6 incomparability caveats | Partial | Caption still references removed Pareto frontier (M2) |
| Technical depth added | ✓ Fixed | NeuSight tile decomposition, SimAI granularity explained |
| Related work expanded | ✓ Fixed | 6 new refs (Nsight, Halide, MLIR, Triton, Pollux, Sia) |
| CNN-bias reframed | ✓ Fixed | "Temporal validation lag" language used |
| Introduction restructured | ✓ Fixed | Shorter paragraphs, clearer flow |
| Section numbering fixed | ✓ Fixed | Subsections properly numbered |
| Cycle-accurate discussion trimmed | ✓ Fixed | Brief, scoped properly |

---

## Overall Assessment

**Improved significantly** from previous reviews. The paper now has a clearer contribution framing, better technical depth, and appropriate caveats on accuracy comparisons. The two HIGH priority issues (abstract/evaluation contradiction H1, and uncontrolled VIDUR comparison H2) are the most pressing. The MEDIUM issues are mostly about precision and completeness rather than fundamental problems.

**Estimated score: 4.5/6 (Weak Accept)** — up from 3.5/6 in the previous critical review. Fixing H1 and H2 would likely push to 5/6.
