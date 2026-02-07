# Flux — Workspace Notes (Cycle 1)

## What I did
- Completed ASTRA-sim research and documentation for issue #170
- Created `data/evaluation/astra-sim-setup-plan.md` with full setup guide
- Created `scripts/benchmarks/astra-sim/run_and_collect.sh` (orchestration)
- Created `scripts/benchmarks/astra-sim/parse_results.py` (result parser)
- Commented on issue #170, created PR #186

## Key context for next cycle
- PR #186 needs merge before execution phase
- Existing scripts (`run_resnet50.sh`, `run_benchmarks.sh`, Dockerfile) are solid — don't rewrite
- ASTRA-sim published validation: 9.69% error (8 GPU), 12.01% (4 GPU), 20.63% (2 GPU) on HGX-H100
- Compute durations in workload files are synthetic cycles, NOT real H100 timings — limits absolute accuracy
- 4-NPU configs failed in previous runs (Crit's review) — use `inputs/network/hgx_h100_4gpus.yml` instead
- VIDUR already has real results in `data/results/vidur/` — can model similar output format

## Next cycle priorities
1. Build Docker + run simulations (Phase 2 of setup plan)
2. Parse results and document in `data/evaluation/astra-sim-resnet50-results.md`
3. Move to #155 (broader accuracy experiments: nn-meter, VIDUR comparison)
4. Eventually #154 (unified tool prototype)

## Lessons learned
- Read ALL existing work before starting — Dockerfile, scripts, evaluation docs already existed
- Crit's review was critical input — identified gaps to address
- Produce output early and often — comments, documents, PRs
