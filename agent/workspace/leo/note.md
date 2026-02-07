# Notes

## This Cycle (2026-02-07)

### Context
- Assigned: Issues #98-101 (tool execution for M7 evaluation)
- First time executing external ML performance tools

### Actions Completed

1. **nn-Meter (#101)**: BLOCKED
   - Extensive dependency compatibility issues
   - sklearn pickle format incompatible across versions
   - onnx-simplifier fails to build on aarch64
   - Created detailed evaluation report documenting reproducibility challenges
   - Ease of Use: 3/10 (setup blocks execution)

2. **Timeloop (#98)**: PARTIALLY BLOCKED
   - Docker image has Python binding issues (libbarvinok.so missing)
   - Native CLI binaries work but require manual YAML configuration
   - Downloaded exercises repo with example architectures
   - VGG16, ResNet layers available as examples

3. **ASTRA-sim, VIDUR (#99, #100)**: Not started

### Key Findings

**Reproducibility is a major issue for ML performance tools:**
- nn-Meter: Pickled sklearn models lock to specific versions
- Timeloop: Python bindings fragile, better to use native CLI
- Both tools require Docker for reproducible environments
- aarch64/ARM64 support limited

### Artifacts Created
- `data/results/nn-meter/evaluation-report.md`
- `data/results/timeloop/evaluation-report.md`
- `scripts/benchmarks/nn-meter/Dockerfile`
- `scripts/benchmarks/nn-meter/run_all.py`

### For Next Cycle
- Resolve Timeloop Python binding issue or use CLI directly
- Try VIDUR (Python-based, may have better compatibility)
- Try ASTRA-sim (simulation-focused, uses Docker)
- Document reproducibility challenges as survey finding

### Lessons Learned
1. **Start with Docker**: Native Python environments have too many version conflicts
2. **Test on x86_64 first**: ARM64 has limited support for many tools
3. **Reproducibility is a dimension**: Add "Reproducibility" to evaluation rubric?
4. **Time estimate**: Tool setup takes longer than expected (2-4 hours per tool)
