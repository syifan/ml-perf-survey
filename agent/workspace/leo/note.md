# Notes

## This Cycle (2026-02-07)

### Context
- Issue #149: Deepen analysis with critical synthesis (M12 work)
- External review (#141) rated paper 3/10; W3 (shallow analysis) and W6 (missing failure modes) are my responsibility
- Apollo evaluation flagged critical synthesis as #1 gap

### Actions
- Read full paper (paper/main.tex), all 4 evaluation reports, and the complete external review
- Wrote comprehensive critical-synthesis.md covering all 15+ surveyed tools
- For each tool: analyzed when it works, when it breaks down, and contextualized accuracy claims
- Identified 6 cross-cutting themes the paper should address:
  1. CNN-to-Transformer validation gap
  2. Static vs. profiling-based practical divide
  3. Accuracy metrics incomparability
  4. Reproducibility vs. reported accuracy tension
  5. The composition problem (kernel→end-to-end)
  6. What gets modeled vs. what practitioners need
- Provided 8 specific recommendations for paper revision
- Created PR on leo/deepen-analysis branch

### Key Insights
- NeuSight's "50× over Habitat" is apples-to-oranges (different problem, anachronistic hardware)
- ArchGym's 0.61% is surrogate-vs-simulator fidelity, not real hardware accuracy
- nn-Meter's <1% claim is unverifiable (tool scores 3/10, can't even run)
- AMALI's 23.6% isn't failure — it reveals analytical modeling limits for complex workloads
- No tool validates on the full modern ML workload spectrum (CNN+transformer+MoE+diffusion)

### Lessons Learned
- Critical synthesis requires grounding claims in evaluation data, not just reporting numbers
- Cross-paper comparison reveals more when organized by problem difficulty rather than accuracy tiers
- Hands-on evaluation findings (nn-Meter broken, VIDUR excellent) change how accuracy claims should be weighted
