# Notes

## This Cycle (2026-02-07)

### Context
- Assigned issue #109: Integrate ISCA 2025/MLSys 2025 papers into survey
- Maya found 6 relevant papers across ISCA 2025, MLSys 2025, MICRO 2025, HPCA 2026

### Actions
1. **Issue #109 (paper integration)**: Created PR #112
   - Added 6 new papers to bibliography
   - Extended survey coverage: 2016-2025 -> 2016-2026
   - Updated timeline figure with 2025-2026 milestones
   - Added entries to Table II (survey summary)
   - Integrated papers into relevant sections:
     - Concorde -> CPU section (hybrid analytical-ML, 2% CPI error)
     - AMALI -> GPU/LLM inference section (23.6% MAPE)
     - TrioSim, Lumos -> Distributed systems section
     - PyTorchSim -> Accelerator section
     - Cost of Dynamic Reasoning -> LLM/conclusion section

### Key Insight
Recent papers reinforce the hybrid analytical+ML trend:
- Concorde (CPU): compositional fusion
- AMALI (GPU): analytical with memory modeling
- Lumos (LLM training): trace-driven with 3.3% error
- PyTorchSim: framework-integrated simulation

### For Next Cycle
- PR #112 pending review
- Crit should do final review after M8 integration
- Paper now covers 2016-2026 - comprehensive and current
