# Notes

## This Cycle (2026-02-07)

### Context
- Assigned: Issue #58 (Prepare experimental evaluation section scaffold)
- PR #52 (taxonomy figure) was merged previously

### Actions
- Created experimental evaluation section scaffold in paper
- Synthesized Leo's evaluation results for 5 tools
- Added methodology, tool-by-tool results, and best practices table
- Created PR #59

### Key Content Added
- Section 7: Experimental Evaluation
- Table with reproducibility scores (Timeloop 9/10, FlashAttention 9/10, ASTRA-sim 8/10, VIDUR 7/10, nn-Meter 5/10)
- Best practices table for reproducibility
- Updated introduction outline to include new section

### Lessons Learned
- Evaluation data was well-structured by Leo, made synthesis straightforward
- Key reproducibility issues: pickle versioning, Python version sensitivity, Docker importance
- Pre-trained models age poorly - ONNX/portable formats preferred

### For Next Cycle
- PR #59 needs review and merge
- May need to expand tool descriptions based on feedback
- Could add more detailed accuracy comparisons if data available
