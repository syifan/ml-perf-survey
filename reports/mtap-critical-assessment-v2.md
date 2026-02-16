# Critical Assessment v2: MTAP Evaluation Framework — Post-Enhancement Review

**Reviewer:** Critical Red Team Reviewer
**Date:** 2026-02-16
**Issue:** #226
**Scope:** Re-assessment after paper-editor/enhanced-mtap-222 changes + VIDUR/Timeloop/ASTRA-sim scorecards

---

## Changes Since v1 Assessment

The paper has been updated with several improvements responding to the initial critical review:

| My Priority 1 Fix | Status | Comment |
|---|---|---|
| Define scoring rubrics (H/M/L/F thresholds) | **NOT ADDRESSED** | Paper now defines `d_i ∈ {0,1,2,3}` but still no thresholds for what MAPE/metric maps to each score |
| Measure γ empirically | **PARTIALLY** | γ is now formally defined (`γ = |T̂_model - Σ T̂_k| / Σ T̂_k`) but never computed — scorecards say "Cannot be measured" or "Not applicable" |
| Compute and report S(t) with sensitivity analysis | **PARTIALLY** | S(t) computed in scorecard JSONs (VIDUR: 2.1/3.0, Timeloop: 2.0/3.0, ASTRA-sim: 2.2/3.0) but NOT reported in paper Table 4. No sensitivity analysis on weights. |

| My Priority 2 Fix | Status | Comment |
|---|---|---|
| Define f() or drop formal notation for D1 | **WORSENED** | Paper now adds `d_1(t) = f(MAPE, ρ_s, max|ε|)` but still never defines f(). This adds formalism without substance. |
| Add MTAP limitations subsection | **NOT ADDRESSED** | Only "Threats to Validity" exists, which mentions MTAP weight subjectivity in passing |
| Sensitivity analysis on weights | **NOT ADDRESSED** | No analysis showing findings are robust to weight changes |

---

## What Improved (Positive)

### 1. Formal Composite Scoring (Good)
The addition of `S(t) = Σ w_i · d_i(t)` with `d_i ∈ {0,1,2,3}` is a genuine improvement. The mapping {Fail=0, Low=1, Medium=2, High=3} provides a concrete scoring scale. The weight justification paragraph is adequate — not strong, but at least present.

### 2. Experimental Design Matrix (Good)
Table with tools × workloads × MTAP dimensions is a significant improvement. It shows which tool-workload combinations are evaluated and for which dimensions. This makes the evaluation more systematic and the scope explicit.

### 3. Failure Mode Taxonomy (Good)
The F1-F4 classification (Build failure, Runtime failure, Silent inaccuracy, Scope mismatch) is a useful contribution that other papers could adopt. It correctly distinguishes engineering problems from fundamental limitations.

### 4. Statistical Validation Protocol (Good)
Verifying bit-identical outputs for deterministic tools and <1% inter-run variance for stochastic tools demonstrates basic rigor.

### 5. MTAP Scorecards (Good Data, Not in Paper)
The JSON scorecards for VIDUR, Timeloop, and ASTRA-sim contain detailed quantitative data. However, this data is only in supplementary files — the paper text does not report S(t) scores.

---

## What Remains Problematic (Critical Issues)

### Issue 1: Scoring Rubrics Still Undefined (CRITICAL)

The paper still does not define what quantitative metrics earn each grade. For D1:
- What MAPE threshold separates High (3) from Medium (2)?
- Is 5% MAPE always "Medium"? What about 4.9%?
- The scorecard files show VIDUR (self-reported <5%) gets M=2, and Timeloop (5-10%) also gets M=2. Why are these the same score?
- NeuSight (2.3%) gets H=3 while VIDUR (<5%) gets M=2. What justifies this? The paper says "we do not rank tools across incomparable domains" but then assigns the same letter grade scale.

**Impact:** Two reviewers applying MTAP to the same tool could assign different scores. This is fatal for a "reusable community standard."

**Fix:** Add a table like:
| D1 Score | Criteria |
|---|---|
| H (3) | MAPE < 3% AND hardware-validated AND rank correlation > 0.95 |
| M (2) | MAPE < 10% OR self-reported < 5% without independent verification |
| L (1) | MAPE < 25% OR only validated on limited workloads |
| F (0) | No working prediction OR MAPE > 25% |

### Issue 2: f() Still Undefined (Getting Worse)

The paper now writes:
> `d_1(t) = f(MAPE(t,W,h), ρ_s(t,W,h), max_w |ε_{t,w}|)`

This is worse than before. The paper introduces a formal function `f()` that maps three metrics to {0,1,2,3} but never specifies the mapping. A MICRO reviewer would immediately ask: "What is f()? Is it a threshold function? A weighted combination? How do you combine MAPE, Spearman correlation, and max error into a single ordinal score?"

Adding undefined mathematical notation to disguise subjective judgment is a red flag. Either define f() concretely or remove the notation and honestly state that scores reflect expert assessment.

### Issue 3: γ Defined But Never Measured (Central Problem Remains)

The formal definition is good: `γ = |T̂_model - Σ T̂_k| / Σ T̂_k`. But the scorecards reveal:
- VIDUR: "Cannot be measured — no kernel-level prediction to compare against"
- Timeloop: "Not applicable — operates at single-layer granularity"
- ASTRA-sim: Likely similar (takes pre-profiled compute times as input)

**The paper's "novel" dimension (D2) has a well-defined metric that cannot be measured for any of the five evaluated tools.** This is the survey's most fundamental weakness. The paper honestly acknowledges this in Section 6.2, but that doesn't resolve the problem — it just means the paper's claimed novel contribution (compositional fidelity measurement) is aspirational rather than realized.

**Possible fix:** Use NeuSight's kernel predictions. Sum the predicted latencies for all kernels in ResNet-18 and compare to a measured end-to-end forward pass time from published data. Even a single γ measurement would transform this from theory to evidence.

### Issue 4: S(t) Not in Paper Text

The scorecards compute S(t) = 2.1 (VIDUR), 2.0 (Timeloop), 2.2 (ASTRA-sim). Table 4 in the paper shows only H/M/L/F letter grades. The paper defines S(t) formally in Section 6 but never uses it. This undermines the formal scoring framework — why define a composite score if you don't report it?

**Fix:** Add a column to Table 4 with numeric S(t) scores, or add a ranking discussion.

### Issue 5: No Sensitivity Analysis

Weights (40/20/20/10/10) are asserted but their impact is not analyzed. Would VIDUR still rank highest if D4 were weighted at 30%? Would the "deployment > accuracy" finding hold under different weight schemes? Without this analysis, the findings are contingent on arbitrary weights.

### Issue 6: N=5 Tools, N=3 with Scorecards

Only 3 tools (VIDUR, Timeloop, ASTRA-sim) have structured scorecards. NeuSight and nn-Meter have qualitative assessments only. For a paper claiming to introduce a "reusable community standard," having only 3 complete data points is thin. The sample is too small for any statistical claims.

---

## Updated Overall Assessment

### Improved, But Core Weaknesses Persist

The paper-editor's additions (experimental design matrix, failure taxonomy, statistical validation, formal scoring) are all good incremental improvements. The paper is noticeably better than v1.

However, the three issues I flagged as Priority 1 remain essentially unaddressed:
1. Scoring rubrics → still undefined
2. γ measurement → still zero empirical data points
3. S(t) reporting → computed in JSONs but not in paper

### Updated Scoring

| Criterion | v1 Score | v2 Score | Notes |
|---|---|---|---|
| Technical Quality | 3/6 | 3.5/6 | Better evaluation design, but core rigor gaps persist |
| Novelty/Significance | 3/6 | 3.5/6 | γ definition helps, but unmeasured novelty isn't novel |
| Scope/Comprehensiveness | 4/6 | 4/6 | No change — 22 tools surveyed, 5 evaluated |
| Presentation Quality | 4/6 | 4.5/6 | Experimental design matrix and failure taxonomy improve structure |
| Venue Fit | 4/6 | 4/6 | No change |

**Overall: Weak Accept (3.9/6)**, improved from Weak Reject (3.5/6).

The paper is now closer to the acceptance bar but still has the fundamental problem that its claimed novel contribution (compositional fidelity measurement via MTAP) is never actually demonstrated empirically.

---

## Remaining Priority Fixes (Ordered)

### Must-Do (Before Submission)
1. **Define scoring rubrics** with explicit thresholds for all 5 dimensions
2. **Either measure γ or downgrade the D2 contribution claim** — don't claim to measure something you can't measure
3. **Report S(t) numerically in Table 4** — use the data already in the scorecard JSONs
4. **Define f() or remove the formal notation** — undefined math is worse than no math

### Should-Do
5. **Weight sensitivity analysis** — show findings hold under ±10% weight perturbations
6. **Add explicit MTAP limitations paragraph** in Section 6 or 7
7. **Complete NeuSight and nn-Meter scorecards** — even partial data is better than none

---

## Bottom Line

The paper has improved from "a reasonable organizational framework" to "a structured evaluation methodology with good supporting infrastructure but incomplete empirical backing." The gap between what MTAP claims to do (measure compositional fidelity) and what it actually does (classify tools on subjective ordinal scales) remains the paper's central vulnerability. A MICRO reviewer would say: "The framework design is sound; the execution is incomplete."
