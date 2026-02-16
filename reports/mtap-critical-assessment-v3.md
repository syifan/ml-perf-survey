# MTAP Critical Assessment v3 — Post-Expansion Review

**Reviewer:** Critical Red Team Reviewer
**Date:** 2026-02-16
**Paper version:** Commit 81e1ba4 (branch `paper-editor/expand-mtap-methodology-232`)
**Prior assessments:** v1 (Weak Reject, 3.5/6), v2 (Weak Accept, 3.9/6)

---

## Executive Summary

The paper has improved meaningfully since v2. The most significant additions are: (1) explicit scoring rubrics in Table `scoring-rubrics`, (2) a defined threshold function replacing the undefined `f()`, (3) S(t) composite scores in the results table, (4) weight sensitivity analysis, and (5) a candid MTAP Limitations subsection. These changes address 4 of 5 Priority 1/2 items from v2.

**Updated verdict: Weak Accept (4.2/6)**

The paper now makes a credible case that MTAP is a novel evaluation framework contribution, primarily through the combination of D2 (compositional fidelity metric) and the explicit rubric-based scoring protocol. However, residual issues prevent a stronger recommendation.

---

## V2 Issue Tracker: What Was Fixed

| # | V2 Issue | Status | Assessment |
|---|----------|--------|------------|
| 1 | Scoring rubrics undefined | **FIXED** | Table `scoring-rubrics` provides H/M/L/F thresholds for all 5 dimensions. D1 has MAPE+ρ_s thresholds; D2-D5 have binary/threshold criteria. |
| 2 | f() undefined | **FIXED** | Replaced with `d_1(t) = min(g_MAPE(...), g_ρ(...))` — a concrete min-of-thresholds function. Clear and reproducible. |
| 3 | γ never measured | **ACKNOWLEDGED** | Limitations §6.5 explicitly states D2 "cannot be measured end-to-end with current tools" and justifies retaining it as "aspirational." Honest framing, though the contribution claim is weakened. |
| 4 | S(t) not in Table 4 | **FIXED** | Table `mtap-results` now includes S(t) column with computed scores. |
| 5 | No weight sensitivity | **FIXED** | Three weight schemes (default, uniform, deployment-heavy) compared in §7.6. All preserve ordinal rankings. |

**Net: 4 of 5 issues resolved. The remaining issue (γ unmeasured) is now honestly acknowledged rather than hidden.**

---

## Detailed Review by MICRO Criteria

### 1. Technical Quality (Score: 3.5/5)

**Strengths:**
- The threshold-based D1 scoring function is now well-defined and reproducible. The `min(g_MAPE, g_ρ)` formulation is elegant — it prevents a tool from gaming one metric while ignoring another.
- The M-cap for unverified self-reported accuracy is intellectually honest and methodologically sound. This is the kind of principled design choice reviewers appreciate.
- Sensitivity analysis, while simple (3 weight schemes), demonstrates robustness of qualitative findings.
- The failure mode taxonomy (F1-F4) is useful and correctly separates engineering failures from fundamental limitations.

**Weaknesses:**
- **D2 rubric is circular.** The rubric defines H as "Validated multi-level composition with γ < 0.10" but the paper acknowledges no tool can produce this measurement. So the D2 rubric's top score is currently unachievable — it defines a scale where only M or below is possible given current tooling. This isn't necessarily wrong, but it means D2 functions more as a theoretical benchmark than an evaluation dimension.
- **D2 scoring inconsistency.** VIDUR gets H (3) on D2 in Table `mtap-results`, but per the rubric, H requires "Validated multi-level composition with γ < 0.10." VIDUR doesn't do multi-level composition — it profiles at the phase level, which is explicitly described as "sidestepping composition." VIDUR's D2 score should arguably be M (2) ("Single-level prediction with documented scope") or even N/A. This is a concrete scoring inconsistency that undermines the rubric's claim of inter-rater reliability.
- **D1 rubric has an ambiguity.** M (2) is defined as "MAPE < 15% OR self-reported < 5% without independent verification." The OR means a tool with MAPE = 14% AND no independent verification gets M, but so does a tool with self-reported < 5% without verification. The distinction seems to be that M is a catch-all bucket. The thresholds should use AND more precisely.
- **No inter-rater reliability test.** The paper claims Table `scoring-rubrics` ensures "two independent evaluators would assign the same scores." This is an empirical claim that is never tested. Even a simple exercise — having a second author independently score one tool — would strengthen this claim.

### 2. Novelty/Significance (Score: 3.5/5)

**Strengths:**
- The "Relationship to existing evaluation approaches" paragraph (new in this version) clearly differentiates MTAP from MLPerf, SPEC, TPC, and artifact evaluation. The key insight — that prediction raises challenges absent from measurement (compositional error, generalization to unseen hardware, temporal stability) — is well-articulated and correct.
- The compositional fidelity concept (D2) remains genuinely novel. Even though γ cannot be measured today, formally defining the metric and establishing its importance is a legitimate intellectual contribution. The paper now correctly frames this as "aspirational."
- The finding that deployment methodology > accuracy for usability is valuable and actionable.

**Weaknesses:**
- **The novelty claim rests heavily on one dimension (D2) that admits it can't deliver.** The paper positions MTAP's novelty as combining "standard metrics (D1, D3-D5) with the novel composition gap metric (D2)." If D2 is aspirational, then MTAP's concrete contribution is: standard metrics + formal rubrics + one interesting finding (Docker > accuracy). That's useful but not a strong novel methodology contribution.
- **Survey-level analysis vs. evaluation methodology.** A MICRO reviewer might argue that the real contributions are the empirical findings (3 cross-cutting results in §7.6), not the framework that organized them. MTAP is arguably the vehicle, not the destination. The paper has improved its case that MTAP is independently valuable (via rubrics and reproducibility), but this tension remains.

### 3. Scope/Comprehensiveness (Score: 3.5/5)

**Strengths:**
- 22 tools, 53 papers, clear inclusion/exclusion criteria.
- The taxonomy matrix (Table 1) with explicit research gaps is well-constructed.
- Coverage of proprietary tools, compiler cost models, and capacity planning tools shows breadth.

**Weaknesses:**
- **N=5 evaluated tools is acknowledged but still limiting.** The paper honestly calls this "case-study-level" but a MICRO reviewer will note that evaluating 5 of 22 surveyed tools (23%) limits the framework's demonstrated utility. At minimum, SimAI, AMALI, and Habitat (mentioned in Threats to Validity) should be included to strengthen the evaluation.
- **No Contribution 3 (unified tool).** The spec requires a "working prototype" of a unified tool combining best approaches. The paper mentions this only as future work. This is a spec compliance issue, not a paper quality issue, but a MICRO reviewer expecting C3 would be disappointed.

### 4. Presentation Quality (Score: 4/5)

**Strengths:**
- Writing is clear, concise, and well-organized.
- 7 figures and 6 tables provide good visual support (up from earlier versions).
- The MTAP framework figure (Fig 4) is informative.
- The limitations subsection shows intellectual maturity.

**Weaknesses:**
- **Table `scoring-rubrics` is dense.** Cramming all 5 dimensions into one table makes it hard to read. Consider splitting into two tables or using a landscape layout.
- **The D2 section (§7.2) is more qualitative discussion than evaluation.** It reads as "here's why we can't measure composition" rather than presenting data. Contrast with D4 (Table `deployment`) which presents clear quantitative results.

### 5. Venue Fit (Score: 4/5)

**Strengths:**
- MICRO is the right venue for a survey spanning accelerator design, GPU modeling, and distributed training.
- The architectural insight (hardware-aligned decomposition) is a contribution MICRO readers care about.
- MTAP is designed for the computer architecture community's needs.

**Weaknesses:**
- The paper reads more as a systems/MLSys survey than a pure architecture paper. MICRO reviewers may push back on the edge device and distributed serving coverage as tangential to microarchitecture.

---

## Remaining Issues (Prioritized)

### Priority 1: Must Fix Before Submission

**P1.1: VIDUR D2 scoring inconsistency.** VIDUR receives H (3) on D2 but does not perform multi-level composition. Per the paper's own rubric (Table `scoring-rubrics`), H requires "Validated multi-level composition with γ < 0.10." VIDUR profiles at the phase level, which §7.2 describes as "sidestepping composition." This should be M (2) at most ("Single-level prediction with documented scope"), or a new rubric row should be added for "validated single-level prediction that avoids composition entirely." This inconsistency would be caught by any attentive reviewer.

**Impact:** If VIDUR D2 drops from H (3) to M (2), S(VIDUR) = 0.4×2 + 0.2×2 + 0.2×1 + 0.1×3 + 0.1×2 = 1.9 (down from 2.1). This changes the tool ranking: ASTRA-sim (2.2) > Timeloop (2.1) > VIDUR (1.9) > NeuSight (1.6). The sensitivity analysis must be re-run.

**P1.2: D1 rubric OR/AND ambiguity.** The M (2) row uses OR in a way that conflates two different situations. Suggest restructuring as:
- M (2): "MAPE < 15% with independent verification, OR self-reported MAPE < 5% without independent verification (capped at M)"
- This makes explicit that self-reported accuracy caps at M, which is already stated in the text but not cleanly in the rubric.

### Priority 2: Should Fix

**P2.1: Add one empirical D2 data point.** Even a single composition measurement would transform D2 from purely aspirational to empirically grounded. For example: sum NeuSight's per-kernel predictions for ResNet-50 and compare to a measured end-to-end latency (even from a published paper). This gives one γ value and demonstrates the protocol is executable.

**P2.2: Inter-rater reliability.** Have a second person independently score one tool using the rubrics. Report agreement/disagreement. This is a low-effort validation that dramatically strengthens the "reusable community standard" claim.

### Priority 3: Nice to Have

**P3.1: Expand to N≥7 tools.** Adding SimAI and Habitat would strengthen the evaluation's representativeness.

**P3.2: Add explicit D2 rubric category for "validated single-level prediction."** Currently the rubric doesn't cleanly map to tools that deliberately avoid composition (VIDUR). A category like "Validated prediction at chosen abstraction level, composition not attempted" (score M) would better capture reality.

---

## Score Breakdown

| Criterion | Score | Comment |
|-----------|-------|---------|
| Technical Quality | 3.5/5 | D2 scoring inconsistency is a concrete flaw |
| Novelty/Significance | 3.5/5 | D2 aspirational but valuable; rest is standard |
| Scope/Comprehensiveness | 3.5/5 | N=5 tools evaluated; no C3 |
| Presentation | 4.0/5 | Clean writing, good figures |
| Venue Fit | 4.0/5 | MICRO appropriate |
| **Overall** | **4.2/6** | **Weak Accept** |

---

## Comparison to v2 Assessment

| Metric | v1 | v2 | v3 |
|--------|----|----|-----|
| Score | 3.5/6 | 3.9/6 | 4.2/6 |
| Verdict | Weak Reject | Weak Accept | Weak Accept (stronger) |
| Scoring rubrics | Absent | Absent | Present, mostly correct |
| f() defined | No | No | Yes (min-of-thresholds) |
| S(t) in table | No | No | Yes |
| Sensitivity analysis | No | No | Yes (3 schemes) |
| Limitations section | No | No | Yes |
| γ measured | No | No | No (acknowledged aspirational) |
| D2 scoring consistent | N/A | N/A | No (VIDUR inconsistency) |

---

## Bottom Line

The paper improved from "conceptually interesting but methodologically incomplete" (v2) to "methodologically sound with specific correctible flaws" (v3). The scoring rubrics, threshold function, and limitations section represent genuine intellectual progress. The VIDUR D2 scoring inconsistency (P1.1) is the most important issue to fix — it's a factual error that undermines the rubric's credibility. If P1.1 and P1.2 are fixed, and ideally P2.1 (one empirical γ measurement), the paper moves solidly into Accept territory.

A MICRO PC member would say: "The MTAP framework is now well-defined enough to be a reusable contribution. The scoring rubrics and formal protocol are the right level of rigor. The empirical findings (deployment > accuracy, composition gap) are valuable. Fix the VIDUR D2 scoring error and clarify the D1 rubric, and this is an accept."
