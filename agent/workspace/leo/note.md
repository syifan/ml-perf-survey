# Leo — Cycle 4 Notes (2026-02-07)

## What I did
- **#190 (Expand Section 8)**: Grew experimental evaluation from 35 to 119 lines with 3 subsections: Evaluation Methodology, Per-Tool Results, Lessons from Evaluation. Added per-tool deep dives (VIDUR, Timeloop, ASTRA-sim, NeuSight, nn-Meter) with specific error messages, setup times, and quantitative results from our data/results/ reports. Five grounded lessons replace generic best practices.
- **#191 (Related Surveys)**: Added 14-line Related Surveys subsection in Section 2 positioning against Rakhshanfar (ML-for-DSE), Sze (DNN accelerator taxonomy), MLPerf benchmarks, and Hennessy/Patterson. Clear 3-point differentiation statement.
- **#173 (Foundational references)**: Added 15 new bib entries (14 from issue + 1 survey for related work). All substantively cited: TPUv1/v4 in intro/taxonomy, PyTorch/TensorFlow in background, Megatron-LM/GPipe/ZeRO in distributed section, scaling laws in challenges, MLPerf suites in reproducibility discussion. Total refs now 86, all cited.

## Key decisions
- Put Related Surveys in Section 2 (Survey Methodology) rather than a separate section — saves space and fits the paper flow
- Ranked tools by score in Table 5 (VIDUR first) rather than alphabetically — more informative
- Used specific numbers from evaluation reports (e.g., "57,426 cycles", "0.301% comm overhead") rather than vague statements
- Cited `hennessy2019golden` twice (intro + related work) — it serves both motivational and positioning purposes

## Remaining work
- Paper is now ~1220 lines (~10.5 pages), approaching target
- Still need figures from Sage (#192, #193)
- Crit needs fresh review after these changes (#185)
- Reference count at 86, closer to 80-100 target

## Lessons learned
- Reading the actual data/results/ reports before writing evaluation makes the content much more specific and credible
- The Related Surveys subsection is compact but addresses a real gap — reviewers specifically flagged the missing survey positioning (W7)
- All bib entries should be cited; 86/86 match means no orphaned references
