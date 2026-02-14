# Final Critical Review: MICRO Program Committee Assessment

**Paper:** "A Survey of High-Level Modeling and Simulation Methods for Modern Machine Learning Workloads"
**Venue:** MICRO 2026 (59th IEEE/ACM International Symposium on Microarchitecture)
**Reviewer Role:** MICRO Program Committee Member (Final Assessment)
**Date:** 2026-02-14
**Paper State:** main branch (commit e02f6a9) + pending PR for VIDUR fix (branch paper-editor/fix-vidur-comparison-90)

---

## Overall Recommendation: **Weak Accept**

**Score: 6.0/10**

The paper has materially improved since the initial review cycle (up from 5.5/10). Key fixes include consistent tool counts, qualified Docker-first claims, expanded cross-cutting architectural insights, and reframed workload coverage as a temporal validation lag rather than bias. The abstract and contributions have been tightened. However, the paper's fundamental limitations remain: no hardware accuracy validation, compressed per-tool treatments, and an experimental section that evaluates reproducibility rather than producing new scientific data. The paper is at the Accept/Weak Accept boundary—publishable but not compelling for a top-tier MICRO slot.

---

## Paper Statistics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Pages (content) | 9 (Sections 1-9) | 10-11 | Below target |
| Pages (total with refs) | 12 (page 12 mostly blank) | 10.5-11 | Refs push to 12 |
| Figures | 10 | 8+ | PASS |
| Tables | 6 | — | Adequate |
| References | 92 | 80+ | PASS |
| Tools surveyed in depth | 22 | — | Consistent |
| Tools mentioned | 15+ additional | — | Consistent |

---

## 1. Has the Abstract/Evaluation Contradiction Been Resolved?

**Verdict: MOSTLY RESOLVED**

The previous reviews identified contradictions between the abstract's accuracy claims and the evaluation's inability to validate them. The current paper addresses this in several ways:

**Improvements:**
- The abstract now frames the contribution as "hands-on reproducibility evaluations" rather than accuracy validation (line 67)
- Section 7 opens with an explicit disclaimer: "No GPU hardware was available, so we **do not validate accuracy claims**" (PDF page 7, line 741-742)
- The evaluation table is retitled "Reproducibility evaluation results (not accuracy evaluation)" (Table 4 caption)
- Accuracy claims in Figures 5 and 6 now carry the caveat: "Self-reported accuracy vs. evaluation speed" and "values are not directly comparable across platforms or workload types"
- The contributions list (page 1) now includes "error composition analysis" as a distinct bullet, separating it from accuracy validation

**Remaining tension:**
- The abstract still says "hybrid approaches combining analytical structure with learned components achieve the best accuracy-speed trade-offs" — this is the paper's claim based on *reported* numbers, not its own validation. The qualifier "reported" or "as claimed in the literature" would resolve this.
- Figures 5 and 6 still plot all tools on the same MAPE axis despite measuring fundamentally different quantities (RTL error, hardware error, simulator-vs-simulator fidelity). The captions now caveat this, but the visual impression of direct comparability remains.

**Assessment:** The contradiction is no longer a structural flaw. The paper now consistently positions itself as a reproducibility study that reports others' accuracy claims with appropriate qualification. The remaining tensions are minor.

---

## 2. Does the Empirical Error Composition Data Strengthen the Contribution?

**Verdict: PARTIALLY — CONCEPTUALLY STRONG, EMPIRICALLY WEAK**

The error composition analysis (Section 8, Figure 9) is one of the paper's most interesting contributions:

**Strengths:**
- Figure 9 clearly illustrates how kernel-level errors (2-3%) accumulate through uncaptured inter-kernel overheads (launch latency, memory allocation, data movement, synchronization) to yield 5-12% model-level error
- The mathematical framing (σ_model ≈ σ_kernel · √N for uncorrelated, N · σ_kernel for correlated) identifies the key analytical question
- The observation that VIDUR sidesteps composition by profiling entire phases is a genuine architectural insight
- The contribution bullet in the introduction now highlights this explicitly

**Weaknesses:**
- **No empirical data supports the composition analysis.** The kernel-level error numbers in Figure 9 (Conv: 2.3%, Attn: 2.1%, FFN: 1.8%, Norm: 3.5%, Softmax: 2.0%) appear to be illustrative/hypothetical rather than measured. The paper doesn't state where these numbers come from.
- The paper doesn't determine whether real tool errors are correlated or uncorrelated — this is precisely the question a MICRO paper should answer empirically.
- No tool-chain experiment (e.g., running NeuSight kernel predictions and comparing their sum to an end-to-end measurement) is presented.

**Assessment:** The composition analysis is the paper's most promising intellectual contribution, but it remains conceptual rather than empirical. If the authors could run even one end-to-end composition experiment (possible without GPU hardware by using Timeloop or ASTRA-sim), it would substantially strengthen the paper.

---

## 3. Does the Paper Meet MICRO Acceptance Standards?

### 3.1 Technical Quality: 6/10 (up from 5/10)

**Improvements since initial review:**
- Cross-cutting themes (Section 5.5) now provides three structured architectural insights with mechanistic explanations
- NeuSight vs. AMALI comparison now explains *why* tile-based prediction outperforms memory hierarchy analysis (thread block scheduling granularity)
- MAESTRO vs. Timeloop distinction is precise (data-centric directives vs. loop-nest enumeration, sacrifice of per-PE utilization modeling)
- Accelerator tractability is grounded in architectural properties (deterministic dataflow, no dynamic scheduling)
- Tool counts are now consistent ("22 tools in depth with 15+ additional tools discussed")
- Docker-first claims are properly qualified with sample size limitations

**Persistent weaknesses:**
- **No hardware validation.** The paper reports others' numbers without independent verification. This is acknowledged but not mitigated.
- **Per-tool descriptions remain compressed.** Section 5 averages 3-5 sentences per tool. A reader still cannot understand *how* NeuSight's tile prediction works, *how* SimAI achieves 1.9% MAPE, or *what* VIDUR's execution model looks like without reading the original papers.
- **The accuracy comparison (Figures 5-6) conflates incommensurable metrics.** Timeloop's 5-10% (vs. RTL), Accel-Sim's 10-20% (IPC correlation vs. hardware), ArchGym's 0.61% (vs. simulator), and nn-Meter's <1% (unverifiable) are plotted as if comparable. The footnotes and caveats help but do not resolve the visual misleading.

### 3.2 Novelty and Significance: 6.5/10 (up from 6/10)

**Contributions ranked by novelty:**
1. **Reproducibility evaluation** (genuine, novel): No prior survey includes hands-on tool evaluation with a structured rubric. The nn-Meter failure (3/10, pickle serialization) is an important negative result. The Docker-first correlation finding is actionable.
2. **Workload coverage/temporal validation lag analysis** (well-quantified): The reframing from "CNN bias" to "temporal validation lag" is more accurate and provides a forward-looking perspective — the lag is closing for transformers but remains for MoE and diffusion.
3. **Cross-methodology architectural analysis** (improved): The insight that structural decomposition aligned to hardware execution boundaries consistently outperforms black-box approaches is now well-supported with specific examples.
4. **Error composition framework** (conceptually interesting): Identifies the right question but lacks empirical grounding.
5. **Taxonomy and coverage matrix** (useful but incremental): The Table 1 gap cells are actionable for researchers, but taxonomy is expected in any survey.

**Missing novelty:**
- No standardized evaluation framework is proposed (the previous comparative review suggested this as the most impactful addition)
- No new measurements or predictions are generated
- Future directions remain descriptive gaps rather than concrete research agendas

### 3.3 Scope and Comprehensiveness: 7/10 (unchanged)

**Strengths:**
- Broad platform coverage (accelerators, GPUs, distributed, edge, CPU)
- 2016-2026 timeframe captures CNN-to-LLM transition
- Related surveys section now covers foundational work (DianNao, Eyeriss, Paleo), SST, and proprietary tools
- The addition of a "Proprietary and vendor tools" paragraph acknowledges Nsight Compute and internal TPU models

**Weaknesses:**
- Edge/mobile coverage remains thin (3 tools, 6 lines of text) relative to deployment importance
- Compiler cost models (TVM, Ansor, TLP) get minimal treatment despite being heavily used
- Industry practices remain absent — how do NVIDIA/Google/Meta actually model performance?
- Coverage depth varies dramatically: accelerator modeling gets 1+ page with detailed mechanistic analysis; distributed training crams 15+ tools into 1 page

### 3.4 Presentation Quality: 7/10 (unchanged)

**Strengths:**
- 10 figures and 6 tables provide rich visual taxonomy
- Timeline (Figure 1), tool architecture (Figure 2), accuracy-speed scatter (Figure 5), and error composition (Figure 9) are effective
- Writing is clear and concise throughout
- Table annotations (*, †, ‡) flag unverifiable claims — excellent practice

**Weaknesses:**
- **Figure redundancy:** Figure 6 (accuracy bar chart) adds no information over Figure 5 (accuracy-speed scatter). Figure 7 (reproducibility bar chart) adds little over Table 4. Removing one would free ~0.5 pages for technical depth.
- **Dense multi-citation sentences** in Section 5.3 remain hard to parse (e.g., listing 6+ citations in one sentence)
- No architecture-level diagrams showing *how* specific tools model hardware (e.g., how Timeloop represents a PE array, how NeuSight decomposes a kernel into tiles)

### 3.5 Venue Fit: 5.5/10 (up from 5/10)

**Improvements:**
- Cross-cutting themes now engage with microarchitectural concepts (warp scheduling, memory coalescing, dataflow mapping)
- The "why accelerators are tractable vs. why GPUs are hard" analysis is the kind of architectural reasoning MICRO reviewers expect

**Persistent concerns:**
- **The evaluation is still not a MICRO "experimental evaluation."** It tests whether software installs work, not whether tools produce correct predictions. MICRO expects new data that advances understanding.
- **Survey papers have a higher bar at MICRO** than at journals (ACM Computing Surveys, IEEE CSUR). This paper's main experimental contribution (reproducibility scores, n=5) may not justify a MICRO slot over a systems paper.
- **Insufficient microarchitectural depth.** Key concepts are mentioned (warp scheduling, bank conflicts, coalescing, KV cache) but not analyzed in terms of how they create specific modeling challenges and how tools address them.

---

## 4. Issue-Specific Checks

### 4.1 VIDUR Evaluation Comparison (Issue #90)

A pending PR (branch `paper-editor/fix-vidur-comparison-90`) addresses the invalid vLLM vs. Sarathi comparison (200 vs. 50 requests). The fix:
- Equalizes request counts to 100 each
- Adds QPS row to Table 5
- Caveats that different arrival rates make latency values non-comparable
- Reframes the text to highlight scheduling model fidelity rather than controlled comparison

**Assessment:** This fix is appropriate and necessary. The current main branch still has the invalid comparison, which undermines the evaluation section. This PR should be merged before final assessment.

### 4.2 Abstract Accuracy Claims

The abstract states: "hybrid approaches combining analytical structure with learned components achieve the best accuracy-speed trade-offs" (line 66). This is the paper's conclusion from reported numbers, not independently validated. Adding "among surveyed tools" or "based on reported results" would fully resolve the remaining abstract tension.

### 4.3 Contributions List

The four contributions are now well-structured and substantiated:
1. Methodology-centric taxonomy with coverage matrix → Section 4 (strong)
2. Cross-methodology architectural analysis → Section 5.5 (improved, now substantive)
3. Reproducibility evaluation → Section 7 (genuine, novel)
4. Error composition analysis → Section 8 (conceptual, needs empirical grounding)

The second contribution has been significantly strengthened from the generic "systematic survey" to a specific "cross-methodology architectural analysis" that identifies hardware-aligned decomposition as a design principle. This is a real insight.

---

## 5. Comparison to Previous Reviews

| Dimension | Initial Review (5.5/10) | This Review (6.0/10) | Change |
|-----------|------------------------|---------------------|--------|
| Technical Quality | 5/10 | 6/10 | +1.0 |
| Novelty/Significance | 6/10 | 6.5/10 | +0.5 |
| Scope/Comprehensiveness | 6/10 | 7/10 | +1.0 |
| Presentation Quality | 7/10 | 7/10 | 0 |
| Venue Fit | 6/10 | 5.5/10 | -0.5 |

**Net movement: +0.5 points overall (5.5 → 6.0)**

The venue fit score decreased slightly because the comparative review against exemplar surveys (Sze et al., gem5, Wu & Xie) made clearer how far the paper falls from the top-tier standard in technical depth. However, technical quality and scope both improved from the architectural deepening and coverage fixes.

---

## 6. What Would Change the Recommendation

### To "Accept" (requires 2 of 3):

1. **Run one hardware validation experiment.** Even a single A100 running NeuSight kernel predictions against measured latency for 10 transformer operators would transform Section 7 from reproducibility-checking to genuine experimental contribution.

2. **Run one composition experiment.** Use Timeloop or ASTRA-sim (both work without GPU hardware) to measure whether kernel-level prediction errors are correlated or uncorrelated when composed to end-to-end latency. This would ground Figure 9's conceptual analysis with empirical data.

3. **Propose a standardized evaluation framework.** Define benchmark suites per subdomain, required disclosures (hardware, workload, batch size, precision), and recommended metrics. This would be the paper's signature contribution — the "MLPerf for prediction" that Section 8 identifies as missing.

### To "Strong Accept" (aspirational):

All three of the above, plus expanding Section 5 to provide per-tool mechanistic explanations at workshop/tutorial depth (likely requires journal-length format).

---

## 7. Summary

### Strengths
1. **Timely, well-organized survey** covering the full landscape of ML performance modeling (accelerators through distributed systems)
2. **Novel reproducibility evaluation** with actionable findings (Docker-first deployment, pickle serialization failure)
3. **Improved architectural insights** in cross-cutting themes — hardware-aligned decomposition as a design principle
4. **Well-quantified workload coverage analysis** reframed as temporal validation lag
5. **Honest self-assessment** of limitations (no GPU hardware, sample size caveats, metric incomparability)

### Weaknesses
1. **No independent accuracy validation** — fundamental limitation for a paper reporting accuracy numbers
2. **Per-tool descriptions remain too compressed** — 3-5 sentences per tool doesn't convey mechanisms
3. **Accuracy metrics across tools are incommensurable** but plotted on same axes
4. **Error composition analysis lacks empirical grounding** — the most promising contribution is purely conceptual
5. **Evaluation doesn't produce new scientific data** by MICRO standards
6. **VIDUR comparison invalid** on main branch (fix pending in PR)

### Final Verdict

The paper is a competent, well-organized survey with two genuine contributions (reproducibility evaluation, architectural design principle identification). It has improved meaningfully since the initial review cycle. However, it remains at the Weak Accept boundary because it lacks the experimental depth MICRO expects — it catalogs and qualifies others' work but produces limited new data or analysis. The paper would be a stronger fit for ACM Computing Surveys (where survey contributions are primary) than MICRO (where experimental novelty is expected), but it is publishable at MICRO given the practical importance of the topic and the actionable guidance it provides.

**Recommendation: Weak Accept (6.0/10)**

---

## Appendix: Specific Line-Level Issues

1. **Line 66 (abstract):** "hybrid approaches...achieve the best accuracy-speed trade-offs" — should say "among surveyed tools" or "based on reported results"
2. **Table 5 (VIDUR):** Still shows unequal request counts (200 vs 50) on main branch — fix pending in PR
3. **Figure 5 caption:** "approximate Pareto frontier" is good — but the frontier itself is misleading because it connects tools measured under different conditions
4. **Figure 9:** Kernel-level error numbers appear hypothetical — should be labeled as "illustrative" or sourced
5. **Section 5.3:** Dense citation listing (6+ refs in one sentence) reduces readability
6. **Section 5.4 (Edge):** 6 lines for 3 tools + 2 additional references is too compressed for a subdomain serving billions of devices
7. **Page 12:** Almost entirely blank (only 3 references) — suggests the paper could accommodate more content within page limits
