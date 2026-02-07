# Notes

## This Cycle (2026-02-07)

### Context
- Final cycle for M7 tool evaluations
- Completed VIDUR execution (issue #100)
- Closed blocked issues (#98 Timeloop, #101 nn-Meter)

### Actions Completed

1. **VIDUR (#100)**: COMPLETE
   - Successfully executed with 3 schedulers (vLLM, Sarathi, Orca)
   - All 100 requests per config completed
   - Docker-based setup works perfectly
   - Created comprehensive evaluation report
   - Ease of Use: 8/10

2. **Timeloop (#98)**: CLOSED (Partially Blocked)
   - Python bindings broken (libbarvinok.so missing)
   - Native CLI works but requires manual YAML config
   - Ease of Use: 5/10

3. **nn-Meter (#101)**: CLOSED (Blocked)
   - sklearn pickle version incompatibility
   - onnx-simplifier build fails on aarch64
   - Ease of Use: 3/10

### Final M7 Evaluation Summary

| Tool | Status | Ease of Use | Notes |
|------|--------|-------------|-------|
| ASTRA-sim | Complete | 8/10 | Distributed training focus |
| VIDUR | Complete | 8/10 | LLM inference, best-in-class |
| Timeloop | Partial | 5/10 | CLI only, Python broken |
| nn-Meter | Blocked | 3/10 | Reproducibility issues |

### Key Survey Findings

**Reproducibility patterns:**
- Docker-first tools succeed (ASTRA-sim, VIDUR)
- Pickled ML models break across versions (nn-Meter)
- Python bindings often fragile (Timeloop)

### For Next Cycle
- No pending tool evaluations
- Available for paper updates or additional analysis
- Consider summarizing reproducibility findings for survey

### Lessons Learned
1. **Docker is essential** - tools without Docker have setup issues
2. **ML-based predictors age poorly** - sklearn/pickle versioning breaks
3. **LLM tools more mature** - VIDUR shows modern engineering practices
4. **Close blocked issues promptly** - keeps tracker clean
