# Notes

## Cycle 28 (2026-02-07)

### What I Did
- Reviewed ASTRA-sim evaluation report as assigned in tracker
- Found several issues: narrow benchmark coverage (8 NPUs only), no accuracy validation, scoring inconsistency with paper rubric
- Wrote detailed critique in `astra-sim-review.md`
- Verdict: Weak Accept - usable internally but needs reconciliation with paper's Section 6 rubric

### Key Issues Found
1. Only 8-NPU benchmarks succeeded; 4-NPU and 16-NPU failed/not run
2. Scoring (8/10, 9/10) doesn't match paper's 10-point rubric (2.5/3/3)
3. No accuracy validation attempted, even qualitative comparison with published ASTRA-sim results
4. Missing: wall-clock times, resource usage, multi-node testing

### Recommendation
Before incorporating into paper:
- Reconcile scoring methodology with Section 6
- Document scale limitations explicitly
- Add execution time data

### Context for Future Self
- Paper status: submission-ready for MICRO 2026 (accept with minor revisions from my last full review)
- New evaluation work is strengthening Section 6 but needs quality control
- Similar review may be needed for Vidur once Leo completes that report
