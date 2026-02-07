# Paper Review - Cycle 29 (2026-02-07)

## Summary

A survey of ML-based performance modeling techniques for computer architecture, covering ~60 papers from 2016-2026 organized by target hardware, ML technique, and input representation.

## Strengths

- Comprehensive coverage of a timely topic at the intersection of ML and architecture
- Clear three-dimensional taxonomy (hardware target, ML technique, input representation)
- Useful Tables 1-3 comparing approaches across multiple dimensions
- Section 7's reproducibility evaluation adds practical value

## Weaknesses

### W1: Shallow Comparative Analysis (Major)
The paper claims "comparative analysis" as a contribution but Section 5 is superficial. The accuracy vs. training cost trade-off (Section 5.1) spans one paragraph. The generalization discussion (Section 5.2) lacks quantitative comparison—how much harder is cross-workload transfer vs. cross-hardware? The interpretability discussion (Section 5.3) provides no framework for comparing approaches. Strong MICRO surveys (e.g., DNN accelerator surveys) provide deeper analytical frameworks.

### W2: Missing Critical Evaluation of Reported Results (Major)
Table 1 reports accuracy figures directly from original papers without critical assessment. Different papers use different benchmarks, metrics, and baselines—making cross-paper comparison misleading. For example, NeuSight's 2.3% error on GPT-3 is not comparable to ASTRA-sim's 5-15% on distributed training. The paper should either normalize comparisons or explicitly warn readers about this apples-to-oranges problem.

### W3: Reproducibility Section Methodology Concerns (Major)
Section 7 claims "hands-on reproducibility evaluations" but:
- Only 5 tools evaluated (Timeloop, ASTRA-sim, VIDUR, nn-Meter, NeuSight) out of 60+ surveyed
- Selection criteria not stated—are these representative or cherry-picked?
- Table 3's 10-point rubric (Setup 3, Reproducibility 4, Usability 3) appears ad-hoc without justification
- No description of evaluation environment, effort expended, or failure modes encountered
- ASTRA-sim gets 8.5/10 but with N/A on key metrics in Table 1—inconsistent

### W4: Weak Treatment of Negative Results and Limitations (Moderate)
The paper is overwhelmingly positive about ML-based approaches. Where do they fail? Which problems remain intractable? Section 6.4's "Research Opportunities" lists gaps but doesn't critically examine why existing approaches fail. A skeptical reader wants to know: when should I NOT use ML-based performance modeling?

### W5: Outdated Scope Despite 2026 Date (Moderate)
For a 2026 paper, the treatment of LLM workloads is surprisingly thin. Only VIDUR, Lumos, and AMALI address LLM-specific modeling. Given the dominance of LLM workloads in current systems, this omission is significant. The abstract mentions "AI agent infrastructure" but this is barely developed in the paper.

### W6: Missing Important Related Work (Moderate)
- No coverage of simulation-in-the-loop training approaches
- Limited discussion of uncertainty quantification (mentioned once in Section 6.4)
- No systematic comparison with pure analytical approaches (only briefly in Section 2.1)
- Missing recent work on differentiable simulators for architecture exploration

### W7: Taxonomy Limitations Not Discussed (Minor)
The three-dimensional taxonomy is useful but has obvious gaps:
- Where do hierarchical/multi-scale models fit?
- How to classify approaches combining multiple input representations?
- The "Hybrid" category (Section 3.2.4) feels like a catch-all

### W8: Presentation Issues (Minor)
- Figure 1's timeline is hard to read—overlapping labels
- Table 2 mixes different metrics (MAPE, RMSE, τ) making visual comparison difficult
- Section numbering inconsistent (6.1-6.5 vs. 4.1-4.5 depth)
- Several claims lack citations (e.g., "specialized models achieve remarkable accuracy—below 5% error")

## Missing Elements

1. **Quantitative meta-analysis**: How has accuracy improved over time? Training data requirements?
2. **Failure case studies**: When do ML models fail catastrophically?
3. **Practitioner guidance**: Flowchart or decision tree for method selection
4. **Resource requirements**: Training time, hardware needed, expertise level
5. **Reproducibility artifacts**: Links to code, datasets, or evaluation scripts
6. **Statistical rigor**: Confidence intervals, statistical tests in comparisons

## Verdict: **Weak Reject**

### Justification

This paper attempts an ambitious survey of a rapidly evolving field but falls short of MICRO standards in several ways:

1. **Depth vs. breadth trade-off poorly balanced**: The paper covers many approaches but provides little insight beyond what reading the original papers would give. The "comparative analysis" contribution is underdeveloped.

2. **Reproducibility claims not substantiated**: Evaluating 5/60+ tools without clear selection criteria or methodology undermines the claimed contribution.

3. **Critical perspective missing**: A survey should help readers understand not just what exists but what works, what doesn't, and why. This paper reads more like a catalog than a critical synthesis.

4. **Timeliness concerns**: For a 2026 submission, the limited LLM coverage is a significant gap given the field's trajectory.

The paper could be acceptable with major revisions: deeper analysis in Section 5, expanded and methodologically rigorous reproducibility evaluation, and critical examination of approach limitations. In its current form, it provides a useful reference but insufficient intellectual contribution for MICRO.
