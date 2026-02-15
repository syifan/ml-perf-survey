# Pre-Restructuring Critical Review: Evaluation Framework Assessment

**Issue:** #218
**Reviewer:** Critic (Red Team)
**Date:** 2026-02-15
**Paper version:** main branch (commit 6a8e34f)

---

## 1. How Weak Is the Current Evaluation Section?

**Verdict: Critically weak — disqualifying for MICRO.**

### Quantitative Assessment

| Metric | Current | MICRO Expectation | Gap |
|--------|---------|-------------------|-----|
| Evaluation lines | 98 / 946 (10.4%) | ≥400 / 946 (≥42%) | ~4x too small |
| Tools evaluated independently | 5 (repro only) | 5+ with accuracy verification | No accuracy data |
| Hardware used | Apple M2 Ultra (no GPU) | Target hardware (GPU/TPU/cluster) | Wrong platform entirely |
| Novel methodology contribution | None | Expected for survey papers at MICRO | Missing |
| Quantitative comparison across tools | None (self-reported only) | Common-benchmark comparison | Missing |
| Accuracy independently verified | 0 tools | ≥3 tools | 0/3 |

### What the Section Actually Contains (Lines 723–815)

The current Section 7 contains:
1. **Setup description** (5 lines): Lists 5 tools, M2 Ultra, Docker.
2. **Scope disclaimer** (6 lines): "No GPU hardware was available" — immediately undermines any evaluation credibility.
3. **VIDUR results** (Table 4): Simulation output for Llama-2-7B. This is a **tool demo**, not an evaluation. It shows VIDUR runs and produces numbers, but validates nothing — no comparison to ground truth, no accuracy assessment.
4. **Timeloop** (2 lines): "Docker CLI works, Python bindings don't." Pure reproducibility note.
5. **ASTRA-sim** (Table 5): Collective microbenchmarks and ResNet-50 scaling. Again, a tool demo. The "internal consistency" claim (Reduce-Scatter = half All-Reduce) validates the tool against its own expected behavior, not against real hardware.
6. **NeuSight** (2 lines): "Tile-based decomposition mirrors CUDA tiling." Observational, no data.
7. **nn-Meter** (3 lines): Failed to run — the only genuinely useful finding.
8. **Lessons** (8 lines): Three bullet points about Docker, reference outputs, and scale-limited evaluation.

**The entire section amounts to: "We installed 5 tools. 4 ran. 1 didn't. Here are some numbers the tools produced."** This is not evaluation. A MICRO reviewer would write: *"The authors merely demonstrate that some tools can be installed. No accuracy claims are verified, no tools are compared on common benchmarks, and the evaluation platform lacks the hardware the tools are designed for."*

### Comparison to What Peer Papers Do

Strong MICRO survey papers (e.g., Dudziak et al.'s NAS latency predictor comparison, or ArchGym's multi-objective evaluation) include:
- **Common benchmarks**: Same workloads run across all tools
- **Ground-truth comparison**: Tool predictions vs. measured hardware performance
- **Statistical rigor**: Error distributions, confidence intervals, not just MAPE
- **Scaling evaluation**: How accuracy degrades with scale
- **Failure mode analysis**: Systematic identification of where each tool breaks

The current paper has **none** of these.

---

## 2. Specific Methodological Gaps

### Gap 1: No Ground Truth
The paper reports self-reported accuracy numbers from each tool's own paper (Figure 4, Figure 5). This is antithetical to the paper's own stated contribution of "hands-on reproducibility evaluation." The abstract claims "hands-on evaluation" but the section only evaluates whether tools install, not whether they produce correct results.

### Gap 2: Incomparable Metrics Treated as Comparable
Section 6 correctly notes that cross-domain accuracy comparison is "methodologically unsound," then proceeds to plot all tools on the same axes (Figure 5: accuracy vs. speed). The paper acknowledges the flaw but still commits it visually. The domain-separated Figure 4 is better but still uses self-reported numbers.

### Gap 3: No Evaluation of Claimed Contributions
The abstract lists four contributions. The evaluation section validates **zero** of them:
- "Cross-cutting architectural design principle" — never tested empirically
- "Coverage matrix" — a table, not tested
- "Error composition analysis" — theoretical, never measured
- "Hands-on reproducibility evaluation" — this is the evaluation section itself, which is circular

### Gap 4: Single Platform, Wrong Platform
All evaluation runs on Apple M2 Ultra (ARM, no GPU). Every tool surveyed targets GPU/TPU/accelerator. Running GPU performance prediction tools without GPUs is like evaluating a car's fuel efficiency by pushing it downhill. The paper acknowledges this limitation but doesn't address it.

### Gap 5: No Usability or Extensibility Metrics
The spec calls for evaluating "accuracy, ease of use, performance, and extensibility." The paper evaluates reproducibility (a subset of ease-of-use) and nothing else. There is no time-to-setup metric, no API usability comparison, no extensibility evaluation (can users add new hardware models?).

### Gap 6: Statistical Weakness
No confidence intervals, no variance reporting, no statistical tests. VIDUR results (Table 4) report single-run averages with no indication of variability. ASTRA-sim results (Table 5) similarly lack statistical context.

---

## 3. What Would a 'Novel Evaluation Framework' Look Like for MICRO?

A novel evaluation framework must be **itself a contribution** — not just "we ran tools." It should define a reusable methodology that the community can adopt.

### Proposed Framework: Multi-Dimensional Tool Assessment Protocol (MTAP)

#### Dimension 1: Prediction Fidelity (weighted: 40%)
- **Absolute accuracy**: MAPE, RMSE vs. measured hardware latency on common benchmarks
- **Rank accuracy**: Spearman rank correlation (captures whether the tool correctly orders configurations, which is what matters for DSE)
- **Error distribution**: Report full error distribution, not just mean — a tool with 5% MAPE but 30% max error is worse for design than one with 8% MAPE and 12% max
- **Scaling behavior**: How does accuracy degrade as workload size, batch size, or device count increases?

#### Dimension 2: Compositional Fidelity (weighted: 20%)
This is the paper's unique angle — leverage the "error composition analysis" contribution:
- **Kernel-to-model composition**: Predict individual kernels, sum them, compare to measured end-to-end
- **Model-to-system composition**: Predict single-device, compose for multi-device, compare to measured distributed execution
- **Gap attribution**: How much of the end-to-end error comes from kernel prediction vs. inter-kernel overhead vs. communication modeling?

This dimension is **novel** — no prior survey measures compositional fidelity.

#### Dimension 3: Generalization Robustness (weighted: 20%)
- **Workload transfer**: Train/profile on CNNs, test on transformers (or vice versa)
- **Hardware transfer**: Profile on GPU-A, predict for GPU-B (Habitat's claimed capability)
- **Temporal stability**: Does the tool's accuracy hold across software stack versions? (motivated by nn-Meter failure)

#### Dimension 4: Practical Usability (weighted: 10%)
- **Time-to-first-prediction**: From git clone to first valid output
- **Deployment robustness**: Docker score, dependency freshness, platform compatibility
- **Documentation quality**: Can a grad student use it without contacting the authors?

#### Dimension 5: Extensibility (weighted: 10%)
- **New hardware support**: Effort to add a new GPU/accelerator model
- **New workload support**: Effort to evaluate a workload not in the training/profiling set
- **API design**: Programmatic interface vs. config-file-only

### Why This Framework Is Novel

1. **Compositional fidelity** (Dimension 2) has never been systematically measured across tools. This directly connects to the paper's error-composition contribution.
2. **Temporal stability** testing (Dimension 3c) is unique — no prior survey evaluates whether tools degrade over time.
3. **The framework itself is reusable** — future tool papers can evaluate against MTAP dimensions, establishing a community standard.

---

## 4. How to Structure Evaluation as 50% of Paper Weight

### Current Structure (946 lines)
```
Section 1: Introduction (101 lines) — 10.7%
Section 2: Survey Methodology (24 lines) — 2.5%
Section 3: Background (22 lines) — 2.3%
Section 4: Taxonomy (234 lines) — 24.7%
Section 5: Survey of Approaches (114 lines) — 12.1%
Section 6: Comparison and Analysis (153 lines) — 16.2%
Section 7: Evaluation (93 lines) — 9.8%
Section 8: Challenges (105 lines) — 11.1%
Section 9: Conclusion (17 lines) — 1.8%
Figures/tables/preamble: remainder
```

### Proposed Structure
```
Section 1: Introduction (~80 lines) — compress slightly
Section 2: Background and Survey Methodology (~40 lines) — merge, compress
Section 3: Taxonomy and Coverage (~150 lines) — compress from 234
Section 4: Survey of Approaches (~80 lines) — compress from 114
Section 5: Evaluation Framework (~100 lines) — NEW: define MTAP methodology
Section 6: Evaluation Results (~250 lines) — NEW: expanded results
Section 7: Analysis and Cross-Cutting Findings (~100 lines) — merge current Sec 6 findings
Section 8: Open Challenges (~80 lines) — compress
Section 9: Conclusion (~20 lines)
```

This gives evaluation (Sections 5-7) roughly 450 lines out of ~900 content lines = **50%**.

### What Must Be Compressed

1. **Taxonomy (Section 4)**: Cut from 234 to ~150 lines. The workload coverage table (Table 3) and associated discussion (~60 lines) can be compressed to a paragraph + reference to the table. Figure 3 (validation bias bar chart) can be removed — the information is in the table.

2. **Survey of Approaches (Section 5)**: Cut from 114 to ~80 lines. The per-tool descriptions are already reasonably compact. Cut the DNN accelerator subsection slightly (it's the most mature and least novel) and the edge device subsection (peripheral to MICRO audience).

3. **Comparison and Analysis (current Section 6)**: Merge the per-domain analysis and speed-accuracy tradeoff into the evaluation results section. The "fundamental incomparability" discussion is important and should be preserved, but the figures can be folded into the evaluation framework.

4. **Introduction**: Cut from 101 to ~80 lines. The contribution list can be made more concise now that evaluation is expanded.

### What Must Be Added

1. **Evaluation Framework Section** (~100 new lines): Define MTAP dimensions, explain why each matters, describe the protocol for each dimension.

2. **Expanded Results** (~200 new lines):
   - Common-benchmark results (even without GPU, can report tool output and compare inter-tool consistency)
   - Compositional fidelity measurements (if any tools provide kernel + model-level predictions)
   - Temporal stability data (nn-Meter failure is one data point; can test older versions of other tools)
   - Usability metrics (time-to-first-prediction for each tool)
   - Extensibility assessment (document what adding a new workload/hardware requires for each tool)

3. **Framework Validation** (~50 new lines): Does MTAP reveal insights that single-metric evaluation misses? This is where the "surprising and controversial" insights live.

---

## 5. Controversial / Surprising Insights the Framework Could Surface

The human requested "deep, surprising, controversial insights." Here are candidates that the evaluation framework could substantiate:

1. **"Reported accuracy is inversely correlated with practical usability."** nn-Meter reports <1% MAPE but can't even run. Tools with higher reported error (VIDUR at <5%, ASTRA-sim at 5-15%) are the only ones that work out of the box. If true, this challenges the field's accuracy-first evaluation culture.

2. **"No single tool can predict both kernel and system performance — and composition makes it worse."** The error composition analysis is theoretical in the current paper. Measuring it empirically would show that the field has no validated kernel-to-system pipeline — a surprising gap for a field that's been active for 10 years.

3. **"The most impactful design choice for a modeling tool is its deployment strategy, not its modeling methodology."** Docker-first vs. pickle serialization vs. compiled binary determines whether anyone can use the tool 2 years after publication. This is provocative because it suggests the ML/systems community should invest more in software engineering than modeling innovation.

4. **"Self-reported accuracy numbers are systematically optimistic."** If the paper can show even one tool whose independently-measured accuracy is significantly worse than reported, it undermines all self-reported numbers in the field. This is the most controversial possible finding.

---

## 6. Immediate Actionable Recommendations for Paper-Editor

### Priority 1: Kill the "No GPU" Disclaimer (requires actual work)
The sentence "No GPU hardware was available" on line 730 is a death sentence for the paper at MICRO. Options:
- **Best**: Get GPU access (GitHub Actions runners, cloud credits, university cluster) and run at least VIDUR and NeuSight with real predictions.
- **Acceptable**: Frame evaluation explicitly as a reproducibility + usability study, and make compositional fidelity (measurable without GPU) the novel dimension.
- **Unacceptable**: Keep current framing — MICRO reviewers will reject on this alone.

### Priority 2: Define the Evaluation Framework in the Paper Text
The framework must be described in ~100 lines of the paper itself, as a standalone contribution. Each dimension should be motivated by a gap in the current evaluation literature.

### Priority 3: Expand Results with Available Data
Even without GPU, the paper can report:
- Time-to-first-prediction for all 5 tools (measurable now)
- Dependency age and freshness for all tools (measurable now)
- Documentation quality assessment (measurable now)
- Tool output consistency (run same workload config through VIDUR/ASTRA-sim with different seeds, report variance)
- Compositional fidelity where tools overlap (e.g., if NeuSight predicts kernel latency and VIDUR uses kernel latency as input, compare)

### Priority 4: Compress Taxonomy and Survey Sections
Target: 150 lines for taxonomy (from 234), 80 lines for survey (from 114). This frees ~120 lines for evaluation content.

### Priority 5: Restructure Paper Order
Move evaluation to Sections 5-7. Current ordering (survey → comparison → evaluation → challenges) buries the paper's strongest potential contribution.

---

## 7. Overall Assessment

| Criterion | Score (1-10) | Notes |
|-----------|:---:|-------|
| Current evaluation quality | 2 | Barely passes as a tool demo; no evaluation content |
| Potential with proposed framework | 7 | MTAP + compositional fidelity could be strong contribution |
| Feasibility of 50% evaluation weight | 6 | Achievable if taxonomy/survey compressed and framework + available-data results expanded |
| Risk of staying at current state | 10 | Certain reject at MICRO — evaluation is the weakest section in the paper |
| Difficulty of proposed changes | 7 | Requires restructuring + new content, but framework design is ready |

**Bottom line:** The evaluation section is the single biggest barrier to acceptance. It must be completely rebuilt, not incrementally improved. The proposed MTAP framework provides a path to making evaluation a genuine contribution, but it requires compressing other sections significantly and committing to a reproducibility + usability + compositional evaluation approach that works without GPU access.
