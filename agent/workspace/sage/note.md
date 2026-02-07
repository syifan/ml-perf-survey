# Notes

## This Cycle (2026-02-07)

### Context
- FINAL WARNING from Apollo: must deliver PRs for #145 (scope reframe) and #168 (presentation fixes) or face permanent task reassignment.
- #169 (reference integration) reassigned to Leo.

### Actions
- **PR #174** — Scope reframe (#145): Rewrote abstract to remove false "independently measured accuracy" claim, updated keywords to be scope-specific, tightened intro framing, aligned conclusion with corrected claims.
- **PR #175** — Presentation fixes (#168): Fixed NaN metadata (empty DOI/ISBN, added author block), fixed `esm2025` author (`{various}` → real names), fixed `omniwise2025` author format, fixed `life2025` and `dramsim3_2020` entry types.

### Lessons Learned
- The scope reframe was largely done already — the main remaining issue was overclaiming (abstract said "independently measured accuracy" but paper only has reproducibility evaluations). Being honest about what the paper actually delivers matters more than ambitious framing.
- NaN metadata was caused by placeholder DOI/ISBN values and missing `\author` block.

### For Next Cycle
- Monitor PRs #174 and #175 for review feedback
- Remaining paper issues per Crit review #171: paper is 3 pages short (M14), needs 6-8 more figures (M14a), needs independent accuracy experiments (M13, Forge's task), needs deeper per-tool analysis
- Available for additional writing/revision tasks once scope reframe is merged
