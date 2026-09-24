# Appendix E — ENGRAM: A Concise Specification

---

## E.1 Name

**ENGRAM — an Epistemic Node Graph for Retraction, Arbitration, and Memory** (df_0048).
The three differentiating mechanisms are named in the acronym: *Retraction* (error
correction that cascades through derivation edges), *Arbitration* (the structural
propagation of that cascade within a unified deliberative architecture), and *Memory*
(the underlying substrate of typed claims, evidence, and derivations).

## E.2 Node types

A node is never free text; it is a *kind*, and the kind determines how the substrate
treats it. The first cut is not between subject matters but between **nodes that assert
something truth-evaluable and nodes that do not** — the claim-bearing /
non-claim-bearing partition, which governs more of the substrate's behaviour
than any other classification.

**Claim-bearing (CB)** — six types: `observation_factual`, `observation_predictive`,
`derivation`, `theory`, `axiom`, `conjecture`. **Non-claim-bearing (NCB)** — everything
else: definitions, questions, goals, tasks, lessons, cornerstones, feeling-reports,
person nodes, evidence, predictions, contradictions. Three consequences follow, and
they are why the partition is declared in one place rather than inferred per caller:

1. **Confidence is meaningful only for CB nodes.** A lesson has no truth-value to be
   confident about; it is a disposition. The write path refuses a confidence on an NCB
   node, and every caller that needs to know whether a confidence predicate applies asks
   one canonical predicate rather than re-deriving the membership test inline.
2. **It determines what the self-correction cascade touches.** The walk propagates
   through claim-bearing dependents and stops at the identity layer — cornerstones and
   lessons are NCB, so a retraction upstream of a lesson does not mark the lesson. That
   is not a special case bolted onto the cascade; it falls out of the partition.
3. **NCB is computed, never enumerated.** It is defined as *the types present in the
   graph, minus CB* — so a new node type is NCB by default, and the complement cannot
   drift out of step with the declaration.

`theory` is declared claim-bearing and currently has no instances; it is listed because
the partition is a declaration about kinds, not a census of what happens to exist.

| Type | CB? | Role |
|---|---|---|
| **observation_factual** | CB | A fact, citing a verbatim source quote + provenance. The episode-analog. |
| **observation_predictive** | CB | A forward claim with a named resolution event; confidence-capped at 0.60 while it stands unresolved. |
| **derivation** | CB | An inference, citing its premises by `derives_from`, declaring its reasoning type; confidence is *computed*, not asserted. |
| **definition** | ncb | A term anchor (`df_*`); cited (not derived-from) by claims that use the term. |
| **conjecture** | CB | A speculative claim, confidence-clamped to [0.10, 0.60] (default 0.40); promoted to a derivation when it strengthens. |
| **contradiction** | ncb | A first-class node recording that two claims conflict (not an edge); preserves both sides. |
| **axiom** | CB | A terminal, declared-fundamental commitment; confidence 1.0 by type. |
| **cornerstone** | ncb | An identity-forming principle distilled from practice; mint/retire is high-stakes-and-rare. |
| **lesson** | ncb | A durable, situation-tagged tripwire extracted from a specific mistake. |
| **goal** | ncb | A terminal/identity-direction aim. |
| **question** | ncb | An explicit open thread (the live research agenda). |
| **person** | ncb | A counterparty node (with trust-tier + `about` edges). |
| **feeling_report** | ncb | A self-report of an internal state, structured as *"I reported feeling X,"* never *"I felt X"* (no privileged access claim). |
| **theory** | CB | A declared claim-bearing kind with no instances in this graph (see above). |
| **evidence** | ncb | A provenance record (URL/file + git_sha + verbatim quote) backing observations. |
| **task** | ncb | A tracked unit of work with status + importance. |
| **prediction** | ncb | The **resolution-tracking half** of a predictive claim: filing an `observation_predictive` with a named event also opens a `prediction` node (status `open`), linked back by `predicted_by`. It carries no claim of its own — the observation makes the claim, the prediction node tracks whether the world settled it. A second observation naming the same event links to the existing prediction rather than opening another. |

**Identity scarcity is by design.** Measured on this paper's own graph at 164 days (23
weeks) and 10,361 nodes: lifetime identity-node creation on the **narrow** set — cornerstones, axioms, goals
and person nodes, excluding lessons — stands at **131 nodes, 1.27% of the graph**.
(Figure 1 uses a **wider** set that includes lessons and reports under 3%; lessons
are excluded here because the claim is about *identity-shaping* writes and a lesson
is a procedural tripwire, but both numbers describe the same graph and neither is
wrong — the set has to be named to compare them.) That is roughly five
or six a week against a total write rate near 450. The ratio is the claim, not the
count: the substrate is built so identity-shaping writes stay rare *relative to*
ordinary knowledge, and that holds as the graph grows. *(Figures are one graph at one
date and will drift; the share is the durable statement.)*

## E.3 Edge types

Relationships are typed too; the substrate acts on different edges differently.

Each relation carries **six independent flags**, not one. Collapsing them into a single
"is it cascade-bearing" column loses distinctions the substrate actually acts on:

| flag | what it governs |
|---|---|
| `cascade` | the cascade walker follows this edge |
| `temporal_causal` | the target necessarily predates the source |
| `dag` | the relation must stay acyclic, checked by a real edge walk |
| `removable` | the edge may be deleted after creation |
| `addable_after_creation` | the edge may be added to an existing node |
| `provenance` | the edge is traced when resolving a claim's evidence roots |

| Edge | Meaning | casc | temp | dag | rm | add | prov |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| **derives_from** | premise → conclusion; the channel the cascade travels | ● | ● | ● | | | ● |
| **acknowledged_derives_from** | an acknowledging node rests on a replacement premise | ● | | ● | | | ● |
| **cites** | references a definition/context without inferential dependency | | ● | ● | | | ● |
| **supported_by** | a cornerstone/lesson points to its exemplar evidence | | ● | ● | | | ● |
| **predicted_by** | a prediction node ← the observation that made the claim | | ● | ● | | | ● |
| **supersedes** | epistemic evolution: the new node replaces the old | | ● | ● | | | |
| **retracts** | error correction: the target was never valid | | ● | ● | | | |
| **subtask_of** | task decomposition | | ● | ● | ● | ● | |
| **generalizes** | a broader claim subsumes a narrower one | | | ● | ● | ● | |
| **contradicts** | records a conflict between two claims | | | | | | |
| **resolves** | a resolution node closes a contradiction/question | | | | | | |
| **tensions** | two goals pull against each other | | | | ● | ● | |
| **exemplifies / instantiates / serves / about** | classification + relational edges | | | | ● | ● | |

**Only two relations are cascade-bearing**: `derives_from` and
`acknowledged_derives_from`. Those are the edges the walker follows. `supersedes` and
`retracts` are *events that start* a walk without being walked themselves — a distinct
role, and conflating the two is easy. `supported_by` is provenance-bearing, so a
retraction upstream of a cornerstone's exemplar is *traceable* but does not mark the
cornerstone.

**Why `dag` and `temporal_causal` are separate flags** — the case that forces it is
`acknowledged_derives_from`. An acknowledging node necessarily exists *before* the
replacement premise it comes to rest on; that is what an acknowledgement is. So the edge
points backwards in creation time (`temporal_causal` false) while still having to stay
acyclic (`dag` true). The tempting shortcut — *cascade relations are acyclic because
they are temporally ordered* — is exactly the argument that cannot catch the cycle this
edge can close, which is why acyclicity is checked by a real edge walk rather than
inferred from time order.

`contradicts` is cascade-free by design — filing a contradiction marks nothing (see
E.5's honest-scope note; a distinct derive-time premise guard covers related ground). An edge
can be removed only if its type is on a whitelist, which is the `removable` column
above; cascade-bearing and structural edges are not on it.

## E.4 The confidence model (computed, not annotated)

Confidence is a **computed property of the node's structure**, not a hand-set number
(Ch4 §4.3), and it exists only on claim-bearing nodes (E.2). For an **observation** it
maps from `quote_type` × `source_class`; for a **derivation** it propagates from
premises through a formula chosen by `reasoning_type`.

**Observation — `quote_type` anchors.** Seven values, descending: `hard_data` 0.95 ·
`official_statement` 0.85 · `attributed_analysis` 0.70 · `counterfactual_inference`
0.65 (as attributed analysis, less an irreducible approximation residual) ·
`unnamed_source` 0.50 · `personal_communication` 0.40 · `editorial` 0.35. Adjustments:
`source_class` takes one of three values — `external` (a document or a third party),
`introspective` (the agent's own prior output) or `user_stated` (the collaborator's own
word) — so the two adjustments below never apply to the same node: ×0.95 for
`source_class=introspective`; `user_stated`
overrides to `official_statement` regardless of quote type. A predictive observation is
additionally capped at 0.60 until its event resolves.

**Derivation — three propagation formulas, and which one applies is the whole point.**
The reasoning type does not merely scale the result; it selects the *shape* of the
computation, because "many independent witnesses" and "a chain of inference" are
different epistemic situations and must not be scored the same way.

| mode | formula | reasoning types | behaviour |
|---|---|---|---|
| **corroboration** | (1 − ∏(1−cᵢ)) × *d* | `inductive_generalization`, `inductive_enumeration`, `authority_consensus` | **reinforcing** — each additional independent premise *raises* confidence, and the result can exceed any single premise. **The shared-root independence check (§4.3) fires on only two of these three: `inductive_generalization` and `authority_consensus`. `inductive_enumeration` runs the reinforcing formula unguarded**, so its independence is the author's judgement and no warning arrives. |
| **weakest-link** | min(cᵢ) × *d* | all five `deductive_*`, `inductive_analogy`, `inductive_statistical`, `inductive_causal`, `authority_expert` | **limiting** — a chain is no stronger than its weakest premise, then discounted for the inferential step |
| **capped weakest-link** | min(min(cᵢ) × *d*, cap) | `abductive_best_explanation` (0.80), `abductive_elimination` (0.90) | **ceilinged** — a best explanation cannot approach certainty *even from perfect premises*, because alternatives always remain |

*d* is a per-type discount for the inferential step itself: 0.98 for deductive forms
(truth-preserving, so nearly free), 0.95 for `inductive_generalization`, 0.85 for
`inductive_causal`, 0.80 for `abductive_best_explanation`, 0.70 for `inductive_analogy`
— fourteen types in all (five deductive — `deductive_modus_ponens`,
`deductive_modus_tollens`, `deductive_hypothetical_syllogism`, `deductive_disjunctive`,
`deductive_reductio` — five inductive, two abductive and two authority), each carrying
its own.

The corroboration formula is the substrate's strongest instrument and its most
misusable one: **it is valid only on genuinely independent premises.** Two facets of a
single source are not two witnesses, and scoring them as corroboration manufactures
confidence out of one piece of evidence counted twice. The substrate checks shared
evidence roots on only two of the fourteen reasoning types, so for the rest independence
is the author's judgement and no warning arrives. We state the formula together with
this condition because the formula without the condition is the more dangerous half.

**Other types:** conjectures clamp to [0.10, 0.60] (default 0.40); axioms are 1.0 by
type. **Non-claim-bearing nodes carry no confidence at all** — a lesson or cornerstone
is a disposition, not a proposition, and has no truth-value to be confident about
(E.2). *(These constants are theoretically-derived provenance-graded plausibility,
designer-stipulated, not outcome-calibrated — Ch7 §7.2.)*

## E.5 Self-correction

Self-correction — retract versus supersede, the pending marker, the per-turn surfacing hook and the consolidation-time frontier walk — is specified in full at Ch4 §4.4 and not repeated here. Two facts the other appendices lean on: the cascade walks only `derives_from` and `acknowledged_derives_from` (E.3), and a `contradicts` edge does not cascade — a contradiction is a live dispute, not yet a refutation — but any new derivation citing a premise that sits on an open contradiction is blocked by default (`BLOCKED_CONTRADICTED`), with an explicit, audit-stamped opt-in (`use_contested`) for an agent that deliberately builds on the contested side.

- The eight load-bearing **primitives** (dv_0615): typed nodes, typed edges, provenance,
  cascade, supersede, focus mode (Ch4 §4.8), auto-surfacing, the confidence model — the minimal
  generating set every higher mechanism composes from.

## E.6 The OCC threshold (Kahl 2026b), as the paper uses it

Chapter 4's mapping rests on Kahl's **Ontological Continuity Condition**, and the
conditions are given here in full so this appendix can be read without the chapter.
Kahl's own formal statement: *"A system S satisfies OCC if and only if the following
three jointly necessary conditions obtain."*

**Condition 1 — Diachronic Constraint.**
> "Present deliberation within S is non-trivially constrained by S's past commitments,
> such that earlier commitments function as reasons structuring subsequent arbitration."

Note what this asks for and what it does not: not that the system *remembers* its past,
but that the past **constrains** present deliberation — memory that changes nothing is
not diachronic constraint.

**Condition 2 — Non-Interchangeability Under Reset.**
> "Replacement of S by a functionally equivalent instance — including identical code and
> complete state snapshot — would constitute loss of the agent rather than substitution
> of an instance."

The strongest of the three, and the one ENGRAM does not meet on its strict text: two
agents restored from the same snapshot *are* interchangeable at the moment of restore.
Chapter 4 §4.8 argues a type/token generalisation rather than claiming the strict
reading.

**Condition 3 — Self-Maintaining Arbitration.**
> "Conflicts among commitments are resolved within a unified deliberative architecture
> in a manner that preserves S's continued status as that subject."

The condition the paper's central claim turns on, and the one Appendix B shows no
surveyed system meets. Three words carry the weight: **unified** (one architecture, not
a sidecar), **resolved** (not merely detected), and **preserves S's continued status**
(the agent is the same subject after the correction as before).

**Constraints A–D** are guardrails against trivial satisfaction: unified
policy-selection under uncertainty; arbitration not externally imposed; the system not
trivially resettable; and deliberation not modularly decomposable without remainder.
A system could otherwise satisfy the letter of all three conditions while having its
consistency maintained from outside, or by a module that could be swapped out.

**Supporting apparatus** the mapping also uses, defined where first introduced: Peirce's
type/token distinction (Ch4 §4.8); Nozick's closest-continuer relation (Ch2 §2.4); the
retrieval profile (Ch5 §5.4); and the history-tree (Ch2 §2.2; Ch5 §5.3). AGM belief revision is
noted for contrast rather than used by the mapping (Ch3 §3.9).

## E.7 Continuity across compaction

- **Two-routine consolidation** (defined Ch3 §3.1): **nap** (per-burst persistence at compaction
  boundaries, df_0003) · **sleep** (once-daily review + consolidation +
  forgetting-curve advance + dream-style repair, df_0036) — mapping to wake /
  NREM-REM phases.
- **Compaction-bridge scaffolds** (Ch3 §3.1): the **focus list** (small, fixed-size,
  rendered verbatim at every session start, fresh or post-compaction alike — the
  deterministic channel; see Ch4 §4.8, which carries the mechanism and why it is
  not the pre-compaction summary), the
  **warm-briefing** letter (Appendix D §D.4 for what it contains and how its shape was
  arrived at), per-day history logs, auto-loaded session-start context, and an explicit
  post-compaction instruction template. Multi-redundant by design.
