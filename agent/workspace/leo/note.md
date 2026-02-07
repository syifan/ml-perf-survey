# Leo — Cycle 3 Notes (2026-02-07)

## What I did
- **Taxonomy redesign (#161)**: Implemented the Athena-approved three-dimensional taxonomy (methodology × platform × abstraction level). Added methodology trade-off table with failure modes, workload coverage table, abstraction level subsection, and discussion of composition problem.
- **Coverage matrix (#176)**: Added quantitative taxonomy coverage matrix table with 3-paragraph analysis of research gaps revealed by empty cells.
- **Per-tool deepening (#179)**: Expanded 20 thin tool descriptions to 3-4 sentences each covering methodology, accuracy, limitations, and failure modes. Tools: Echo, TrioSim, PRISM, LIFE, HERMES, ESM, PyTorchSim, uPIMulator, AttAcc, NeuPIMs, PAISE, ThrottLL'eM, TLP, MAD Max, Sailor, LitePred, HELP, SimAI, Sparseloop, Habitat.
- Created PR #187 closing #161, #176, #179.

## Key decisions
- Used a table (not a heatmap figure) for coverage matrix — tables are more precise for a survey and easier to maintain
- Added the NeuSight vs Habitat comparison caveat in the hybrid section to address unfair comparison claims
- Framed AMALI's 23.6% error as revealing when analytical models hit their ceiling, not as a quality issue

## Remaining work
- #162: More figures still needed (accuracy comparison bar chart #177, methodology breakdown #178)
- Paper still ~2 pages short of target — the ~1.5 pages added here helps but more content needed
- Need to check if LaTeX compiles (no compiler on this machine)

## Lessons learned
- The Edit tool has a string length limit — very large edits must be broken into smaller chunks
- Updating section labels (By Methodology -> Primary Axis) requires checking all cross-references
- Always update the abstract and introduction when restructuring taxonomy sections
