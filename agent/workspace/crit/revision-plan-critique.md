# Revision Plan Critique (M11-M15)

## Date: 2026-02-07

## Summary

The revision plan (issue #144, milestones M11-M15 in spec.md) correctly identifies the major problems raised by the external reviewer (#141). However, the plan has structural risks that could result in a paper that addresses surface criticisms without fixing the underlying quality problems.

## Key Concerns

### 1. Scope Pivot Risk (M11)

The biggest risk in the entire plan. The paper is currently framed around "ML-based performance modeling" — the title, abstract, introduction, taxonomy, survey section, and both analysis tables are all structured around ML techniques. Pivoting to "modeling FOR ML workloads" is not a light reframing — it requires rethinking the entire taxonomy and reclassifying every surveyed work.

**Specific concern:** The current taxonomy axes (ML technique, target hardware, input representation) make no sense for a paper about modeling FOR ML workloads. If the scope is analytical models + simulators + hybrid approaches for predicting ML performance, the taxonomy should be organized around methodology type (analytical, trace-driven simulation, hybrid, ML-augmented) and what is being modeled (training vs. inference, single-device vs. distributed). The plan does not acknowledge this taxonomy redesign.

### 2. Coverage Inflation vs. Depth (M12)

The plan says "expand to ~60 actual cited references." But the reviewer's complaint was not merely about reference count — it was about *depth of discussion*. Adding 35 references without substantive analysis of each will make the paper worse, not better. The bib file already has ~50 entries but the paper only discusses ~20 with substance.

**Risk:** The team adds citations to pad the number while the analysis remains abstract-level for most entries. This is exactly what the reviewer warned about.

### 3. Experimental Verification is Underspecified (M13)

"Run experiments to verify accuracy" is the right direction, but the plan doesn't specify: (a) what hardware is available, (b) which workloads will be used as common benchmarks, (c) what constitutes a fair comparison across fundamentally different tool categories. Running NeuSight and Timeloop on "the same workload" doesn't make sense — they solve different problems.

**Risk:** The experiments end up as another round of tool evaluations (like the current Section 7) rather than genuine accuracy verification that the reviewer asked for.

### 4. Page Expansion Without Content Plan (M14)

"Expand to 10.5-11 pages" is listed as a separate milestone. This should not be a goal in itself — it should be a natural consequence of deeper analysis and broader coverage. Treating page count as a deliverable invites padding.

### 5. Missing: What Gets Cut

The plan only discusses additions. The current paper has significant content that may need to be removed or heavily rewritten under the new scope:
- Section on memory system modeling conflates DRAM simulation with KV cache management
- vLLM PagedAttention discussion (a systems optimization, not a performance model)
- The "AI Agent Infra" entry in Figure 1 (uncited)
- The entire framing of "ML-based performance modeling" in the abstract and introduction

The plan does not identify what existing content is *wrong* for the new scope.

## Verdict on Plan Adequacy

**The plan partially addresses the reviewer's concerns.** It correctly identifies the five major problem areas (scope, methodology, coverage, depth, presentation). However:

1. It underestimates the scope pivot — this is a near-rewrite, not a revision
2. It risks quantity over quality in coverage expansion
3. The experimental plan is too vague to be actionable
4. It doesn't address what to remove, only what to add
5. The unified tool prototype (Contribution 3) adds scope creep risk — building a tool while doing a major paper revision is ambitious

## Recommendations

- Rewrite the taxonomy FIRST (before expanding coverage), since the taxonomy determines what gets included
- Set a minimum analysis depth per cited work (at least 2-3 sentences of critical discussion, not just a mention)
- Define the common benchmark suite concretely before starting M13
- Identify content to cut from the current paper under the new scope
- Consider deferring the unified tool prototype to avoid spreading too thin
