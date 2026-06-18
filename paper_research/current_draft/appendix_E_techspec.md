# Appendix A — ENGRAM: A Concise Specification

> **DRAFT SAMPLE — 2026-06-17.** A compact reference for the substrate the paper
> argues about: the node types, edge types, the confidence model, the OCC
> definitions the mapping uses, and the consolidation routines. It restates, in one
> place and tersely, what Chapters 2–3 introduce in prose — so a reader can check a
> definition without re-reading a chapter. Nothing here is new; it is a glossary of
> the live substrate. Definition-node IDs are given for traceability.

---

## A.1 Name

**ENGRAM — an Epistemic Node Graph for Retraction, Arbitration, and Memory** (df_0048).
The three differentiating mechanisms are named in the acronym: *Retraction* (error
correction that cascades through derivation edges), *Arbitration* (the structural
propagation of that cascade within a unified deliberative architecture), and *Memory*
(the underlying substrate of typed claims, evidence, and derivations).

## A.2 Node types

A claim is never free text; it is a *kind*, and the kind determines how the substrate
treats it.

| Type | Role |
|---|---|
| **observation** | A fact, citing a verbatim source quote + provenance. The episode-analog. |
| **derivation** | An inference, citing its premises by `derives_from`, declaring its reasoning type; confidence is *computed*, not asserted. |
| **definition** | A term anchor (`df_*`); cited (not derived-from) by claims that use the term. |
| **conjecture** | A speculative claim, confidence-capped (~0.85); promoted to a derivation when it strengthens. |
| **contradiction** | A first-class node recording that two claims conflict (not an edge); preserves both sides. |
| **axiom** | A terminal, declared-fundamental commitment; confidence 1.0 by type. |
| **cornerstone** | An identity-forming principle distilled from practice; mint/retire is high-stakes-and-rare. |
| **lesson** | A durable, situation-tagged tripwire extracted from a specific mistake. |
| **goal** | A terminal/identity-direction aim. |
| **question** | An explicit open thread (the live research agenda). |
| **person** | A counterparty node (with trust-tier + `about` edges). |
| **feeling_report** | A self-report of an internal state, structured as *"I reported feeling X,"* never *"I felt X"* (no privileged access claim). |
| **evidence** | A provenance record (URL/file + git_sha + verbatim quote) backing observations. |
| **task** | A tracked unit of work with status + importance. |

**Identity scarcity is by design**: across a 9-week graph, lifetime identity-node
creation (cornerstones + axioms + goals + persons) numbered in the low dozens — the
substrate treats identity-shaping writes as sacred and rare.

## A.3 Edge types

Relationships are typed too; the substrate acts on different edges differently.

| Edge | Meaning | Cascade-bearing? |
|---|---|---|
| **derives_from** | premise → conclusion; the channel the self-correction cascade travels | **yes** |
| **cites** | references a definition/context without inferential dependency | no |
| **supersedes** | epistemic evolution: the new node replaces the old (soft/stale, override allowed) | yes |
| **contradicts** | records a conflict between two claims | yes (DAG-exempt) |
| **retracts** | error correction: the target was never valid (tainted, no override) | **yes** |
| **supported_by** | a cornerstone/lesson points to its exemplar evidence | no |
| **resolves** | a resolution node closes a contradiction/question | no |
| **exemplifies / instantiates / serves / about / subtask_of** | classification + relational edges (mostly DAG-exempt) | no |

`derives_from`, `supersedes`, `contradicts`, `retracts` are the cascade-bearing
edges — the structure on which arbitration operates. A whitelist blocks removal of
cascade-bearing and structural edges (Ch3 §3.3).

## A.4 The confidence model (computed, not annotated)

Confidence is a **computed property of the claim's structure**, not a hand-set number
(Ch3 §3.2). For an **observation** it maps from `quote_type` × `source_class`; for a
**derivation** it propagates from premises through a discount fixed by `reasoning_type`.

**Observation `quote_type` anchors** (median ≈ 0.85, right-skewed):
`hard_data` 0.95 · `official_statement` 0.85 · `attributed_analysis` 0.70 ·
`personal_communication` 0.40 · `editorial` 0.35. Adjustments: ×0.95 for
`source_class=introspective`; → 0.85 override for `user_stated`.

**Derivation `reasoning_type` propagation** (median ≈ 0.72, flatter):
`inductive_generalization` 0.92+ (broad independent support) · `deductive_modus_ponens`
≤ min-premise · `abductive_best_explanation` cap ~0.80–0.90 (tentative best fit) ·
`inductive_analogy` ~0.45 (structural similarity only). Chained derivations inherit
and dilute their premises.

**Other types:** conjectures cap ~0.85; lessons bimodal (battle-tested high / proposed
low); axioms 1.0. *(These constants are theoretically-derived provenance-graded
plausibility, designer-stipulated, not outcome-calibrated — Ch7 §7.2.)*

## A.5 Self-correction

- **Retract** = "I was wrong": target tainted, no override; cascade taints all
  `derives_from` dependents.
- **Supersede** = "I changed my mind": old node stale, soft-overridable (`use_stale`);
  the new node is current.
- **Cascade** fires automatically on retract/supersede/contradict, and the
  **per-turn auto-surfacing** hook returns tainted/stale state to the agent's view
  without an intentional reach-out (the two halves of *operational binding*, Ch4 §4.3).
- The eight load-bearing **primitives** (dv_0615): typed nodes, typed edges, provenance,
  cascade, supersede, focus mode, auto-surfacing, the confidence model — the minimal
  generating set every higher mechanism composes from.

## A.6 The OCC threshold (Kahl 2026), as the paper uses it

Definitions the mapping (Ch4) rests on:
- **OCC** = Ontological Continuity Condition (df_0037): 3 jointly-necessary conditions
  + 4 constraints.
- **Cond 1 — Diachronic Constraint** (df_0058) · **Cond 2 — Non-Interchangeability
  Under Reset** (df_0039) · **Cond 3 — Self-Maintaining Arbitration** (df_0040).
- **Constraints A–D** (df_0041–df_0044): unified policy-selection under uncertainty;
  not externally imposed; not trivially reset; not modularly decomposable.
- Supporting machinery: Peirce type/token (df_0047); Nozick closest-continuer (df_0046);
  AGM + Hansson Relevance/Core-Retainment (df_0049–df_0053); retrieval profile (df_0045);
  identity-tree node (df_0055).

## A.7 Continuity across compaction

- **Three-routine consolidation**: **nap** (per-burst persistence at compaction
  boundaries, df_0003) · **bedtime** (once-daily review) · **sleep** (consolidation +
  forgetting-curve advance + dream-style repair, df_0036) — mapping to wake / pre-sleep
  / NREM-REM phases.
- **Compaction-bridge scaffolds** (Ch3 §3.4): the **focus list** (small, fixed-size,
  rendered verbatim into the pre-compaction summary — the deterministic channel), the
  **warm-briefing** letter, per-day history logs, auto-loaded session-start context, and
  an explicit post-compaction instruction template. Multi-redundant by design.

---

**Drafting note (for Lei):** This is the concise spec-summary appendix you flagged as
missing (you started reading at B). It's a reference/glossary, not an argument — mostly
rendering the `df_*` and primitive nodes. Two scope questions: (1) is this the right
*altitude* (a one-page-ish reference), or do you want it fuller (a per-tool or
per-mechanism spec)? (2) the OCC definitions (A.6) restate Ch2's verbatim definitions in
brief — keep the cross-reference, or have A.6 carry the full verbatim text so the
appendix is self-contained? Easy either way.
