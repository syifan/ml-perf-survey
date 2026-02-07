# Notes

## This Cycle (2026-02-06)

### Context
- Issue #75: Expand paper database to address reviewer coverage concern (issue #72)
- External reviewer criticized that ~60 papers is inadequate for a comprehensive survey

### Actions
- Created 5 new bibliography categories addressing specific reviewer gaps:
  1. `compiler-cost-models.bib` (18 papers): Halide, TVM/Ansor, TensorIR, DietCode
  2. `simulation-acceleration.bib` (18 papers): SimPoint, SimNet, phase prediction
  3. `power-energy-models.bib` (21 papers): Zeus, Accelergy, carbon tracking
  4. `bayesian-active-learning-dse.bib` (23 papers): BO for DSE, active learning
  5. `llm-performance-predictors.bib` (27 papers): GenZ, LLMCompass, Roofline-LLM
- Added corresponding markdown summary files for each category
- Total papers in database: 274 (was ~60, now exceeds 100+ target by significant margin)

### Key Papers Added (Highlights)
- **Compilers**: Halide autoscheduler (2019), Ansor (2020), TensorIR (2023), DietCode (2022)
- **Simulation**: SimPoint (2003/2006), SimNet (2022), Allegro (2024)
- **Power/Energy**: Zeus (2023), Accelergy (2019), CarbonTracker (2020)
- **BO/AL**: Reagen et al. (2017), ARS-Flow 2.0 (2024), Polaris (2024), ConfuciuX (2020)
- **LLM Predictors**: GenZ (2024), LLMCompass (2024), Lumos (2025), VIDUR (2024)

### Reviewer Gaps Addressed
All 5 gaps from W1 in issue #69 have been addressed:
1. Learned cost models for compilers (Halide, TVM/Ansor) - DONE
2. ML for simulation acceleration (SimPoint, phase prediction) - DONE
3. Power/energy prediction models (McPAT alternatives) - DONE
4. Bayesian optimization/active learning for DSE - DONE
5. Recent LLM-specific predictors (LLM-Viewer, GenZ) - DONE

### For Next Cycle
- May be asked to expand specific subcategories further
- Watch for new papers at ASPLOS 2025, MLSys 2025, ISCA 2025
- Consider adding papers on uncertainty quantification (mentioned in W3)
