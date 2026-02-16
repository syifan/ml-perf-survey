# Critical Assessment: MTAP Evaluation Framework Novelty and Rigor

**Reviewer:** Critical Red Team Reviewer
**Date:** 2026-02-16
**Issue:** #226
**Verdict:** MTAP has a solid conceptual core but significant gaps undermine its claim as a "novel evaluation methodology" contribution.

---

## Executive Summary

MTAP is positioned as one of four paper contributions and is framed as a "reusable community standard." After careful analysis, I find that **MTAP in its current form is a reasonable organizational framework but falls short of the novelty bar for a standalone contribution at MICRO.** The five dimensions are sensible but not surprising; the scoring is under-justified; and the "novel" dimension (D2: Compositional Fidelity) is the weakest in terms of actual evaluation evidence. Strengthening MTAP requires addressing three categories of issues: (1) novelty justification, (2) methodological rigor, and (3) empirical backing.

---

## 1. Framework Novelty Assessment

### 1.1 Are the 5 Dimensions Genuinely Innovative?

**Verdict: Partially — D2 is novel, the rest are standard practice.**

- **D1 (Prediction Fidelity, 40%):** MAPE, rank correlation, and error distribution are standard evaluation metrics used in every tool paper. The formal notation $d_1(t) = f(\text{MAPE}, \rho_s, \max|\epsilon|)$ adds rigor, but this is not new — it's what any competent reviewer would expect. The function $f$ is never actually defined, making the formalism cosmetic.

- **D2 (Compositional Fidelity, 20%):** This is **the only genuinely novel dimension**. The composition gap ratio $\gamma = |\hat{T}_{\text{model}} - \sum_k \hat{T}_k| / \sum_k \hat{T}_k$ is well-defined and addresses a real problem. The paper correctly marks this as "NOVEL" in Figure 4. However, **the paper never actually measures $\gamma$**. Section 6.2 admits "direct composition measurement [is] impossible with current tools" and resorts to indirect characterization and back-of-envelope estimation ($\sigma_{\text{model}} \approx \sigma_{\text{kernel}} \cdot \sqrt{N}$). A novel metric that cannot be measured is a hypothesis, not an evaluation methodology.

- **D3 (Generalization Robustness, 20%):** Workload transfer, hardware transfer, and temporal stability are well-known concerns. MLPerf already tracks temporal reproducibility. The nn-Meter temporal failure is a good illustration, but the dimension itself is not novel.

- **D4 (Deployment Viability, 10%):** Time-to-first-prediction is a practical metric but has been used in reproducibility studies (e.g., ACM badging, artifact evaluation committees). Not novel.

- **D5 (Extensibility, 10%):** Standard software engineering evaluation criteria. Not novel.

### 1.2 Comparison to Existing Evaluation Approaches

The paper claims "prior surveys evaluate tools by reprinting self-reported accuracy numbers." This is somewhat reductive. While no prior *survey* in this exact domain uses a named multi-dimensional framework, the individual dimensions are standard:

- **MLPerf** (cited) already evaluates across hardware, workloads, and deployment.
- **Artifact evaluation committees** at MICRO/ISCA already assess reproducibility and deployment viability.
- **Dudziak et al.** (cited) compare edge predictors on common benchmarks — essentially performing D1+D3.
- **Systems benchmarking** (SPEC, TPC) has decades of experience with multi-dimensional evaluation frameworks.

**The gap the paper should emphasize:** No one has combined all five dimensions *for performance prediction tools specifically*, and the composition gap metric is genuinely new. But the paper overclaims by framing the entire framework as novel rather than focusing on D2 as the novel contribution.

### 1.3 Is "Compositional Fidelity" Substantive Enough?

**Verdict: Conceptually yes, empirically no.**

The composition gap is indeed the field's central unsolved problem, and defining it formally is valuable. But a contribution needs to go beyond definition:

- The paper defines $\gamma$ but never measures it empirically.
- The error propagation analysis uses idealized assumptions (uncorrelated vs. linearly correlated) without empirical validation.
- The claim "5-12% model-level error" is from "the literature" — not from MTAP evaluation.
- No experiment actually composes kernel predictions into model predictions to measure the gap.

**To be a genuine contribution, MTAP needs at least one empirical measurement of $\gamma$** — even on a small workload like ResNet-50 Conv1 layers, comparing NeuSight kernel predictions summed vs. actual end-to-end measured time.

---

## 2. Methodological Rigor

### 2.1 Dimension Definitions and Measurability

| Dimension | Well-defined? | Measurable without target hardware? | Actually measured in paper? |
|-----------|--------------|--------------------------------------|---------------------------|
| D1 | Partially — $f()$ undefined | No (relies on self-report) | No — uses self-reported numbers |
| D2 | Yes — $\gamma$ is precise | Partially | No — "impossible with current tools" |
| D3 | Loosely defined | Partially | Anecdotal (nn-Meter failure) |
| D4 | Well-defined | Yes | Yes — Table 5 |
| D5 | Loosely defined | Yes | Qualitative only |

**Critical problem:** Only D4 is actually evaluated with independent quantitative data. D1 uses self-reported numbers (which the paper itself argues against in Section 5). D2 cannot be measured. D3 and D5 are qualitative assessments.

This means **MTAP is a 5-dimensional framework where only 1 dimension (D4) has rigorous independent evaluation**. The framework's value is significantly undermined by this.

### 2.2 Weighting Scheme (40/20/20/10/10)

**The weights are asserted but not justified empirically.** The paper states: "Weights reflect practitioner priorities: prediction fidelity dominates because incorrect predictions lead to flawed design decisions." This is reasonable intuition, but:

- No practitioner survey supports these weights.
- No sensitivity analysis shows whether different weights change conclusions.
- The weights have no impact on results since the composite score $S(t)$ is never computed in the paper — Table 4 uses letter grades (H/M/L/F), not numeric scores.
- If $S(t)$ were computed: VIDUR would score $0.4(3) + 0.2(3) + 0.2(1) + 0.1(3) + 0.1(2) = 2.5$; Timeloop would score $0.4(3) + 0.2(2) + 0.2(2) + 0.1(2) + 0.1(3) = 2.5$. They're identical — does this match the paper's narrative that VIDUR is the clear winner?

**Recommendation:** Either drop the numeric weights and use the ordinal H/M/L/F scale (which is what the paper actually uses), or commit to quantitative scoring and run a sensitivity analysis. The current approach has the formalism of rigor without the substance.

### 2.3 The $d_i(t) \in \{0,1,2,3\}$ Mapping

The scoring function maps to {Fail, Low, Medium, High}. But **the mapping criteria from measurable quantities to these ordinal scores are never specified.** What MAPE threshold separates "High" from "Medium" for D1? What $\gamma$ value marks the boundary between "Medium" and "Low" for D2? Without explicit scoring rubrics, two evaluators could assign different scores to the same tool — making MTAP non-reproducible as a "community standard."

### 2.4 Statistical Validation

The paper mentions bit-identical checks for deterministic tools and <1% inter-run variance for stochastic tools. This is good practice but does not address the fundamental issue: **N=5 tools is too small for any statistical analysis.** The findings are case studies, not statistical results. This is fine for a survey, but the paper should not imply statistical rigor that N=5 cannot support.

---

## 3. Practical Impact Assessment

### 3.1 Will Practitioners Use MTAP?

**Unlikely in current form, for three reasons:**

1. **No concrete scoring rubric.** A practitioner cannot take MTAP and evaluate a new tool without making subjective judgment calls at every step.
2. **Hardware dependency.** D1 (40% of score) requires running the tool on target hardware. Without hardware, the evaluator is back to trusting self-reported numbers — which is what MTAP claims to fix.
3. **Composition gap (D2) cannot be measured.** The most novel dimension is the one practitioners cannot actually evaluate.

### 3.2 Does MTAP Solve a Real Problem?

**Yes, conceptually.** The field genuinely needs better evaluation methodology beyond accuracy-only comparison. The deployment viability finding (Docker predicts usability better than accuracy) is the paper's strongest insight. But this finding comes from D4, which is the dimension least in need of a formal framework — any practitioner trying to use a tool discovers deployment issues immediately.

### 3.3 Are the Dimensions Comprehensive?

**Missing dimensions that a reviewer might expect:**

- **Cost/Resource Requirements:** What hardware/compute is needed to run the tool? A tool requiring 8 A100s for profiling has different practical value than one running on a laptop.
- **Accuracy Consistency Across Scale:** How does accuracy change from 1-GPU to 1000-GPU? This is distinct from D3 (generalization) which focuses on workload/hardware transfer.
- **Community Health:** Maintenance activity, user community size, issue response time. These predict long-term viability better than D4/D5.

---

## 4. Comparison to Standards in Systems/Architecture

### 4.1 How Does MTAP Compare?

| Framework | Domain | Dimensions | Empirical? | Adopted? |
|-----------|--------|-----------|------------|----------|
| MLPerf | ML benchmarking | Throughput, latency, power, cost | Yes | Widely |
| SPEC | Systems | Performance, power, area | Yes | Industry standard |
| TPC | Databases | Performance, price/performance | Yes | Industry standard |
| **MTAP** | **Perf. prediction** | **5 dimensions** | **Partially** | **N/A (new)** |

**Key difference:** MLPerf, SPEC, and TPC all have concrete, measurable metrics with standardized measurement protocols. MTAP has formal notation but lacks the measurement protocols that would make it reproducible.

### 4.2 Meeting the Bar for "Novel Evaluation Methodology as a Contribution"

**Current state: Below the bar.** For a MICRO paper to claim a novel evaluation methodology as a contribution, I would expect:

1. **Clearly defined, measurable metrics** — MTAP partially delivers (D4 yes, D2 defined but unmeasurable, D1/D3/D5 vague).
2. **Empirical validation that the methodology reveals something new** — The deployment finding (D4) succeeds here. The composition gap (D2) is defined but not validated. D3 produces one anecdote (nn-Meter).
3. **Evidence the methodology is reusable** — No scoring rubric means it's not reproducible.
4. **Comparison to alternative evaluation approaches** — Missing entirely.

---

## 5. Specific Recommendations to Strengthen MTAP

### Priority 1: Critical (Must-fix)

1. **Define scoring rubrics for all dimensions.** Specify exact thresholds: e.g., D1 High = MAPE < 5%, Medium = 5-15%, Low = 15-25%, Fail = >25% or unreproducible. Do this for every dimension.

2. **Measure $\gamma$ empirically, even partially.** Use NeuSight to predict individual kernels for a small model (e.g., ResNet-18), sum them, and compare to actual end-to-end latency from a profiler. Even one data point makes D2 empirical rather than hypothetical. If you can get Timeloop kernel predictions and compare to ASTRA-sim model-level predictions for the same workload, that's a composition gap measurement.

3. **Compute and report $S(t)$ for all tools.** The formal score is defined but never used. Compute it, report it, and run sensitivity analysis on weights.

### Priority 2: Important (Should-fix)

4. **Drop the formal notation for D1 or define $f()$.** The expression $d_1(t) = f(\text{MAPE}, \rho_s, \max|\epsilon|)$ is meaningless without defining $f$. Either specify $f$ (e.g., a weighted combination with thresholds) or remove the formalism.

5. **Add a "limitations of MTAP" subsection.** Acknowledge: N=5 is small, D2 is currently unmeasurable with available tools, weights are assumptions not empirical, no GPU hardware for D1 verification.

6. **Add sensitivity analysis on weights.** Show that top-level findings (VIDUR best, nn-Meter worst) are robust to reasonable weight variations (e.g., uniform weights, D2-heavy weights).

### Priority 3: Nice-to-have (Would strengthen)

7. **Add missing dimensions** (cost/resources, community health) or justify their exclusion.

8. **Provide a worked example** of how a future tool paper would apply MTAP, with a concrete checklist.

9. **Compare MTAP to artifact evaluation criteria** used at MICRO/ISCA to position it as an extension rather than a replacement.

---

## 6. Overall Assessment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Framework Novelty | **Weak** | D2 is novel; D1/D3/D4/D5 are standard. Overclaims novelty of the whole framework. |
| Methodological Rigor | **Below expectations** | Formal notation without formal definitions. Scoring rubrics absent. |
| Empirical Backing | **Insufficient** | Only D4 has independent quantitative data. D2 is unmeasured. |
| Practical Impact | **Moderate potential** | Good concept, but not actionable without rubrics. |
| Contribution Strength | **Borderline** | Needs Priority 1 fixes to pass as a contribution. |

**Bottom line:** MTAP is a good idea executed incompletely. The composition gap concept (D2) is genuinely novel and important, but the paper doesn't actually measure it. The deployment viability finding is the paper's strongest empirical result, but it doesn't need MTAP to be communicated. In its current form, a MICRO reviewer would likely say: "The evaluation framework is a reasonable organizational tool but not sufficiently rigorous or novel to be a standalone contribution. The empirical findings (deployment > accuracy, composition gap exists) are the real contributions — MTAP is the vehicle, not the destination."

To elevate MTAP to contribution status: define scoring rubrics, measure $\gamma$ empirically (even partially), and compute/report the composite scores with sensitivity analysis.
