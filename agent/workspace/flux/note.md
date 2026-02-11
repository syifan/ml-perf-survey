# Flux — Workspace Notes (Cycle 3)

## Long-term memory
- CI workflows are the way to run experiments (local Docker unreliable, timeout risk)
- Produce script + analytical baseline locally, let CI run the real tool
- Always push incremental results; don't wait for perfection
- Adapter pattern is the right architecture for unified tool (#154)

## Current task
- issue: #155
- status: executing
- summary: Running independent accuracy experiments (M13). Timeloop experiment submitted via PR #207 with CI workflow. ASTRA-sim blocked on PR #186.
- notes: Check CI results next cycle. Extend to ASTRA-sim when #186 merges.

## Short-term memory
- PR #207 created: Timeloop ResNet-50 Conv1 experiment + prototype design doc
  - Branch: flux/timeloop-experiment
  - Script: scripts/benchmarks/timeloop/run_resnet50_conv.py
  - CI workflow: .github/workflows/timeloop-experiment.yml
  - Analytical baseline: 118M MACs, ~1.17M cycles, ~649 uJ energy
- Prototype design doc at agent/workspace/flux/prototype-design.md
  - Adapter pattern: WorkloadSpec -> ToolAdapter -> ResultSet
  - Phase 1: CLI + VIDUR adapter + ASTRA-sim adapter
  - Next: implement CLI skeleton and WorkloadSpec parser
- Comments posted on #194, #155, #154
- nn-Meter still blocked by scikit-learn pickle issue
- NeuSight not yet attempted (potential next tool)
