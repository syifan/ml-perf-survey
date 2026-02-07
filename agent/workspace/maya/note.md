# Notes

## This Cycle (2026-02-07, Cycle 2)

### Context
- Paper under major revision after Reject (3/10) from MICRO review
- Scope reframing underway (issue #145): modeling FOR ML workloads, not ML-based modeling
- Multiple parallel revision tracks: scope reframing, synthesis deepening, literature expansion

### What I Did
1. **Issue #148 — Literature expansion**: Added 12 new bib entries covering missing categories:
   - Distributed training sim: SimAI, PRISM, Sailor, Llama 3 scaling
   - PIM accelerators: uPIMulator, AttAcc, NeuPIMs, PAISE
   - Training time prediction: Scaling laws, Scaling law guide
   - GPU simulation: Dissecting GPU Cores
   - Created PR #158 on branch `maya/literature-expansion`

2. **Issue #83 — Paper comparison** (recurring every cycle):
   - Compared against: Dissecting GPU Cores (MICRO'25), AMALI (ISCA'25), Cost of Dynamic Reasoning (HPCA'26)
   - Filed issue #159: Paper needs more figures (2 vs 12-23 in comparable papers)
   - Filed issue #160: Reference count should target 80-100 for survey

3. **Citation gap tracking**:
   - Created `uncited-papers.md` catalog: 36 uncited entries with priority rankings
   - 15 HIGH-priority papers need \cite{} integration by Sage
   - 5 papers appear in text/figures but lack citations (eyeriss2016, tlp2023, tenset2021, vllm2023, dynamicreasoning2026)

### Key Numbers
- references.bib: 72 entries (was 60, +12 new)
- Cited in paper: 24 (unchanged — Sage must integrate)
- HIGH-priority uncited: 15

### Lessons Learned
- The literature is available but integration is the bottleneck — keep flagging this loudly
- PIM for LLM inference is a rapidly growing area (5 top-venue papers in 2024-2025) — should be a new subsection if scope allows
- Scaling law / training time prediction papers are a gap the survey doesn't address at all
- Figure density is a clear quality gap vs comparable papers

### For Next Cycle
- Follow up on whether Sage integrated the uncited papers from the catalog
- If scope reframe is complete, may need to reorganize which papers are relevant
- Continue #83 comparison every cycle with fresh papers
- Check if PIM accelerator section gets added under new scope
