# Notes

## Long-term memory
- Review each paper version independently per human directive #195 — no references to prior reviews
- Be harsh but fair — always find something to improve
- The biggest recurring gap: synthesis over cataloging in §5
- The #1 blocker: no experimental contribution comparing tool predictions against ground truth
- Abstract overclaims have been a persistent issue across versions
- Reading the paper fresh takes significant cycle time but produces the most honest assessment

## Current task
- issue: #201 (fresh independent paper review) + PR #205 review
- status: planning
- summary: Plan approach for PR #205 review and next fresh paper review post-merge

## Short-term memory
- **PR #205 review plan** (ready for execute mode):
  - PR addresses 3 concerns: section reordering (eval before challenges), abstract overclaim fix ("50+" → "30+ from 53 papers"), PIM/memory compression
  - Key items to verify: (1) \ref{} labels resolve after reorder, (2) Threats to Validity placement in Eval section is good, (3) commercial tool scope sentence appropriate, (4) "over 30 tools from 53 papers" count accuracy against Table 2, (5) check if Reproducibility subsection self-references after being moved into Eval section
  - Net -7 lines — modest but appropriate space recovery
- **Next fresh paper review**: Wait for PRs #203, #204, #205 to merge, then full fresh read and independent scoring
- **3 open PRs**: #203 (Flux cross-tool analysis), #204 (Leo synthesis), #205 (Sage reorder) — all unmerged
