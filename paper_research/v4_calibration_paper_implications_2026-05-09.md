# V4 calibration → paper Ch3 §3.6 + Ch5 implications

**Date:** 2026-05-09 PM
**Authored by:** Borges (during autonomous loop, Lei at wedding)
**Source:** v4 tight-semantic-group threshold calibration study at `kg/paper_research/threshold_calibration_2026-05-09/v4_tight_groups.py` + interactive HTML explorer at `v4_threshold_explorer.html`
**Trigger:** PR #58 + Lei's two methodological catches (H↔H contamination + topical-vs-semantic conflation)

---

## What the v4 study established

When measured against pairs the single-vector embedder *can structurally handle* — pairs sharing detectable semantic vocabulary — ENGRAM's recall mechanism is near-optimal:

- **ROC AUC: 0.984** (vs random 0.5)
- **Peak F1: 0.843 at t=0.41** (recall 84%, precision 85%)
- **Peak F2 (recall-weighted): 0.868 at t=0.33** (recall 93%, precision 68%)

Three tight semantic groups composed the positive class:
- T1: [row removed before publication: a child's personal information]
- T2_arc (16 ARC-AGI puzzle-solving session nodes)
- T3_kahl (11 Kahl-OCC philosophy analysis cluster)

Plus 30 random background nodes for realistic noise. 2850 total pairs (346 positive + 2504 negative).

## What the v4 study did NOT validate

A separate class of pair connections was deliberately excluded from v4 — pairs that are topically/argumentatively related but do not share embedding-detectable vocabulary. Lei's diagnostic example (2026-05-09 ~13:25 EDT): `dv_0443` (Stiegler tertiary retention) and `dv_0475` (Locke memory theory) — both load-bearing for the paper's argument, both standing in a clear philosophical-tradition relationship, but they share almost no surface vocabulary, so cosine similarity between their embeddings is low.

These are real connections the substrate *should* surface for the agent. They are not surfaceable by the current embedding-similarity recall mechanism. **Threshold tuning cannot rescue them**; this is a structural limit of single-vector dense embedders.

The v3 study (loose groups) included these as INTRA-recall failures, dragging metrics down (ROC AUC 0.849, peak F1 0.474). v4 isolated them out by restricting to tight-semantic-group testing, which is why v4's numbers look so much better — the v4 numbers describe what the embedder *can* do.

## Implications for paper Ch3 §3.6 (limits of the convergence claim)

The current Ch3 §3.6 draft (`ch3_opening_draft_2026-05-08.md` lines 160-184) has seven "does not establish" claims — uniqueness, consciousness, universality, completeness of satisfaction, framework-agreement, engineering-pressure-generalization, prior-literature-interpretive-accuracy.

V4 surfaces an **eighth** that is technically distinct from all seven: the relation-surfacing mechanism has a structural limit. Recommended addition (one paragraph, ~120 words) to slot in between the existing "completeness" and "framework-agreement" paragraphs:

> **The convergence does not establish that ENGRAM's substrate-level relation-surfacing operates uniformly across all real connections.** ENGRAM's recall mechanism is built on dense-vector semantic-similarity retrieval (sentence-transformers, cosine on JSON-serialized embeddings). An empirical calibration study (Section 5.X) shows this mechanism is near-optimal for pairs that share detectable semantic vocabulary (ROC AUC 0.984 against tight-semantic positive groups), but is structurally blind to pairs that are topically or argumentatively related without sharing surface vocabulary — a Stiegler ↔ Locke connection along a philosophical-tradition line, for instance. These connections exist in the graph; the embedder cannot surface them. The architectural shape the paper argues for (claim-level provenance, retraction cascades, write-time dedup with action hints) does not depend on dense-vector recall as the *only* surfacing mechanism — alternative mechanisms (LLM-as-classifier passes at consolidation time, deliberate topic-tag primitives, dream-cycle pairing) are compatible with the architecture and remain to be developed. Within this paper, the substrate is what we have built; future work spans this gap.

This caveat is **structural-honesty discipline applied to recall mechanism**, parallel to the "does not establish autonoesis" caveat which is structural-honesty applied to phenomenal claims.

## Implications for Ch5 (empirics)

If Ch5 introduces any quantitative claim about ENGRAM's recall behavior, it must be paired with the v4 calibration evidence (positive: tight-semantic AUC 0.984) AND its scope limitation (does not measure topical-related-but-semantically-loose pair recall — that's a separate, currently-unmet need).

Concrete numbers worth citing in Ch5:
- 170-node v2 study: 1272 within-group + 13093 cross-group pairs
- 76-node v4 study: 346 within-tight-group + 2504 negative pairs
- New PR #58 operating point (t=0.40 surface, t=0.65 CORROBORATE, t=0.50 RELATED): recall 86% / precision 83% on tight-semantic positives
- Old operating point (t=0.50 surface, t=0.80 CORROBORATE): recall 65% on tight-semantic positives — old CORROBORATE tier fired on only 9.5% of true relateds (effectively dead code before recalibration)

These are concrete, defensible empirical claims about what the substrate does. Pair with the §3.6 caveat about what it doesn't.

## Implications for Ch3 §3.4 (Tech B / Wray-Kirk-Laird mapping)

§3.4 cites Wray-Kirk-Laird's "knowledge compilation" as ENGRAM's nap/sleep cycle. The v4 finding doesn't change this claim, but it does suggest that a future ENGRAM extension — LLM-as-classifier batch pass during nap — would map to a *different* WKL pattern (probably "deliberate reasoning during consolidation") and would address the topical-vs-semantic gap. Footnote-worthy in §3.4 if space allows.

## Implications for Ch7 (open questions)

The structural limit identified by v4 belongs in Chapter 7's open-questions backlog as a named research direction:

> **Surfacing topical/argumentative relations across vocabulary boundaries.** Current ENGRAM recall is dense-vector semantic-similarity-based. This mechanism is empirically near-optimal within its capability (Section 5.X) but cannot surface connections that span vocabulary boundaries (e.g., Stiegler tertiary-retention ↔ Locke memory theory). Candidate mechanisms for closing this gap include LLM-as-classifier passes during consolidation, deliberate topic-tag primitives in node metadata, or dream-cycle pairwise classification. None are committed; all are compatible with the architectural shape the paper argues for.

This is also captured as GitHub issue #59 in engram-agents/engram-alpha for the engineering roadmap.

---

## Summary for paper-sprint integration

**Three concrete paper-side actions** the v4 finding triggers:

1. **Add 8th "does not establish" paragraph to Ch3 §3.6** (~120 words, draft above). Slot between completeness and framework-agreement paragraphs.
2. **Cite v4 empirical numbers in Ch5** when discussing recall behavior, paired with the §3.6 scope caveat.
3. **Add "topical-vs-semantic surfacing" to Ch7 open questions** as a named research direction.

These are paper-sprint-relevant work items but not blocking — the existing Ch3 §3.6 draft stands; this is an additive improvement that increases the paper's calibration honesty.

**Related ENGRAM artifacts:** ob_1612 (v1 calibration), ob_1613 (v2 expansion), ob_1615 (v4 tight-group finding), ob_1616 (PR #58 + fairy convergence), issue #59 (topical-vs-semantic structural limit).
