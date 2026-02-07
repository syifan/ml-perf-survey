# Notes

## This Cycle (2026-02-07)

### Context
- Assigned: Issues #91 (benchmark suite), #92 (evaluation rubric)
- New scope: third-party tool evaluation with common benchmarks

### Actions Completed
1. **Issue #91 (Done)**: Created benchmark suite document
   - 13 benchmarks across CNN, Transformer, LLM, Distributed categories
   - Hardware configs for Timeloop, nn-Meter, VIDUR, ASTRA-sim
   - Tool-benchmark compatibility matrix
   - Execution methodology and reproducibility requirements

2. **Issue #92 (Done)**: Created evaluation rubric document
   - 4-dimension framework: Accuracy (40%), Ease of Use (25%), Performance (20%), Extensibility (15%)
   - Detailed 1-10 scoring rubrics with concrete criteria
   - Ground truth methodology
   - Composite scoring formula

3. Created PR #96

### Key Decisions
- Selected Llama-2-7B/70B for LLM benchmarks (well-profiled in VIDUR)
- Used 40/25/20/15 weighting to prioritize accuracy while valuing usability
- Included MAPE, correlation, max error for quantitative accuracy assessment (addresses Crit's feedback)

### For Next Cycle
- Monitor PR #96 for review feedback
- Coordinate with Maya once tool selection (#93) is finalized
- May need to add benchmarks for any new tools Maya selects
