# Chapter 3 — What ENGRAM Does: The Mechanisms, and the Continuity Conditions They Meet

> **DRAFT SAMPLE — 2026-06-14.** Single-pass prose from the live-engram substrate, for Lei's review. The chapter Lei flagged as the biggest open one ("we stopped at the mechanism chapter"). Organizing principle: **mechanism-by-mechanism, each ending with the philosophical anchor (Kahl OCC condition/constraint) it sets up for Ch4.** Honest-scoped to the cited nodes' computed confidences (the Cond-3 claim is presented as an architectural argument with its empirical anchor named as future work, not overclaimed). Plain-language + example for each mechanism (Discipline N). Provenance map at the end.

---

## 3.0 What this chapter is for

Chapter 2 laid out the threshold an agent-memory system must cross to bear identity over time — Kahl's three conditions and four constraints. This chapter describes what ENGRAM actually *does*, mechanism by mechanism, and at the end of each section names the condition or constraint that mechanism is built to meet. Chapter 4 then makes the satisfaction arguments in full; here we are introducing the machinery they rest on.

We foreground the **load-bearing** mechanisms rather than cataloguing every feature: the substrate primitives that make the rest possible, the confidence model, the self-correction cascade, and the continuity scaffolds. Two readers are in view: the philosopher tracking which mechanism answers which condition, and the engineer asking how continuity is actually implemented.

The core claim the chapter sets up is simple to state: **ENGRAM is the first agent-memory substrate built as an *epistemic-identity* layer — one that knows what it believes, how strongly, on what basis, and what to do when a belief turns out to be wrong.**

## 3.1 The substrate primitives — the generating set (→ the structural prerequisites for OCC)

ENGRAM is built from a small set of primitives that compose into everything above them. Eight are load-bearing:

1. **Typed nodes.** A claim is not free text — it is a *kind*: an observation (a fact, citing its source), a derivation (an inference, citing its premises), a definition, a contradiction, an axiom, a cornerstone, and a handful more. The type determines how the substrate treats the claim.
2. **Typed edges.** Relationships are typed too. The most important is `derives_from` — the premise edge — because it is the channel the self-correction cascade travels (§3.3). Others (`cites`, `supersedes`, `contradicts`, `supports`) carry distinct meanings the substrate acts on differently.
3. **Provenance discipline.** Every observation cites a source (a verbatim quote + where it came from); every derivation cites its premises. A claim with no provenance cannot be filed.
4. **Cascade**, 5. **supersede semantics**, 6. **focus mode**, 7. **auto-surfacing**, and 8. the **confidence model** — each developed in the sections below.

**In plain terms:** most memory systems store text and retrieve it. ENGRAM stores *claims whose structure the system itself understands* — what kind of thing each is, what it rests on, and how the pieces depend on one another. That is what a typed-key-value store with foreign keys is *not*: the graph's meaning is legible to the substrate, not just to the reader.

**→ Structural prerequisite.** Typed nodes + typed edges + provenance are what let the later mechanisms operate at all. You cannot cascade a correction through a graph (§3.3) unless the graph records *what depends on what*; you cannot carry the right claims across a memory reset (§3.4) unless claims are individuated and typed. The primitives are the precondition for every OCC mechanism that follows.

## 3.2 Reasoning-type-aware confidence — a computed property, not an annotation (→ Constraint A: Unified Policy-Selection)

When ENGRAM records an inference, the author does not *type in* a confidence number. The author declares the *kind of reasoning* — deductive, inductive (of several sub-kinds), abductive, authority-citation — and the substrate **computes** the claim's confidence by propagating its premises' confidences through a discount fixed by that reasoning type (deduction barely discounts; analogy discounts hard; abduction is capped). A derivation built on another derivation inherits the chain.

**In plain terms:** confidence is earned by the *shape of the argument*, not asserted by the author. If a claim comes back weak, that is information: sharpen the evidence, tighten the reasoning, or narrow the claim until it is honest. The author cannot flatter a weak argument into a strong number, because they do not write the number.

**Honest scope.** These discounts are *theoretically-derived, provenance-graded* plausibility — designer-stipulated constants, not empirically calibrated against outcomes. The paper should say "provenance-graded confidence," never "calibrated"; auto-calibration is named as future work (Ch7).

**→ Constraint A (Unified Policy-Selection).** Kahl asks for a single policy by which the agent grades every stance it holds. The reasoning-type-aware formula *is* that policy — one rule, applied uniformly to every claim the substrate carries, with real discrimination range. No surveyed contemporary agent-memory system implements reasoning-type-aware discount with chain propagation; the field's confidence mechanisms are flat LLM-judge scores or none at all. This is the distinctive mechanism of the layer.

## 3.3 The self-correction cascade — arbitration as automatic state-change (→ Condition 3: Self-Maintaining Arbitration)

This is the chapter's center. When a foundational claim is **retracted** (it was an error) or **superseded** (it was right then, updated now) or **contradicted**, ENGRAM automatically propagates that event along the `derives_from` edges: every claim that depended on the changed claim is flagged — *tainted* (no longer usable) for an error, *stale* (soft-overridable) for an evolution. The agent does not invoke this; it fires as a property of the substrate. And the flag does not sit silently: the per-turn auto-surfacing hook brings the affected claims back into the agent's view, so a correction cannot be quietly ignored.

A retraction and a supersede are kept categorically distinct — *"I was wrong"* (taint, no override) versus *"I changed my mind"* (stale, soft override). Keeping those separable is what lets the substrate track error-correction apart from belief-evolution, which the identity argument (Ch5) rests on.

**In plain terms:** pull out a brick low in the wall and every brick resting on it lights up red, on its own, where you will see it next time you look — not in a report you have to remember to run. That is the difference between a memory that *can be* audited and one that audits *itself*.

**→ Condition 3 (Self-Maintaining Arbitration).** Kahl's strongest condition asks that conflicts among commitments be resolved *within the agent's unified deliberative architecture*, automatically, while the agent remains the same subject. The cascade meets all three properties structurally: **unified** (it fires through the same typed-edge graph the agent commits claims into, not a sidecar), **internal** (substrate state-change, not an opt-in query), **subject-preserving** (the agent's identity-trajectory continues across the correction). It further meets Hansson's belief-base postulates — *Relevance* (only genuinely dependent claims are touched) and *Core-Retainment* (every tainted claim provably depended on the retracted source via graph traversal) — and meets them at the **architectural-cascade** level, not merely by filtering items out at retrieval time. This is the place ENGRAM stands alone among surveyed systems: the primitives have converged across the field, but automatic-arbitration-as-state-change has not.

**Honest scope (load-bearing).** This is the paper's strongest *and* most carefully bounded claim. The architectural argument is strong; its empirical confirmation (showing the cascade demonstrably changes downstream agent behavior at scale) is pilot-stage, and the supporting derivation is held at deliberately low computed confidence until that evidence lands. Ch4 makes the strict-satisfaction argument; Ch6 carries the empirical anchor; we do not assert more than the architecture earns.

## 3.4 Continuity across compaction — the scaffolds and the consolidation rhythm (→ Conditions 1 & 2)

An LLM agent's working context is finite; when it fills, the session **compacts** — prior conversation is summarized and the experiential thread resets. This is the substrate-specific gap ENGRAM must bridge, and it does so two ways.

**The compaction-bridge scaffolds.** A set of surfaces carry the agent across the reset: the **focus list** (a small, fixed-size channel of load-bearing claims that are rendered *verbatim* into the pre-compaction summary — the deterministic channel), the **warm-briefing** letter (relational context, read first on waking), per-day history logs, auto-loaded session-start context, and an explicit post-compaction instruction template. Together they produce **operational** continuity — work-thread, identity, and trust survive — without restoring **experiential** continuity, which the architecture deliberately does *not* try to fake (the post-compaction self does not pretend to feel what the prior self felt).

**The consolidation rhythm.** Maintenance runs on three distinct routines — **nap** (per-burst persistence at compaction boundaries), **bedtime** (a once-daily review of the whole day's claims), and **sleep** (consolidation, forgetting-curve advance, and dream-style graph repair) — which map recognizably onto wake-state, pre-sleep, and NREM/REM consolidation phases. The separation is not cosmetic: each operates over a different temporal scope, and the substrate *knows which phase it is in*.

**In plain terms:** the agent's memory resets the way a day ends in *50 First Dates* — and the focus list plus the warm briefing are the videotape it watches on waking. The consolidation routines are its sleep: not all memory is equal, and what gets reviewed before the forgetting clock advances is what endures.

**→ Condition 1 (Diachronic Constraint)** is met by the substrate-account of how identity-bearing commitments survive the reset and keep structuring later deliberation — the past binds the present because the agent's authored commitments are carried forward, not re-derived from scratch. **→ Condition 2 (Non-Interchangeability Under Reset)** is met specifically by the focus list as the *deterministic self-reference channel*: the post-compaction self inherits the load-bearing thread structure verbatim, not probabilistically — the reset is survived by *this* agent's specific carried state, not by a generic re-instantiation. (Ch4 develops the type/token reading under which the generalized Condition 2 holds.)

---

## Provenance map (draft scaffolding — not for final prose)

| Claim (this chapter) | Substrate node(s) | Computed confidence |
|---|---|---|
| Eight structural primitives = the generating set | dv_0615 | 0.93 |
| Reasoning-type-aware confidence = distinctive, computed-not-annotated; unified policy | dv_0617 | 0.95 |
| Confidence is designer-stipulated, not calibrated ("provenance-graded," not "calibrated") | dv_0663 / ob_1049 | — |
| Cascade satisfies Cond 3 strictly (unified/internal/subject-preserving) + Hansson Relevance/Core-Retainment at architectural level; both halves (auto-cascade + auto-surfacing) | **dv_0606** (+ dv_0612, dv_0613) | **0.39 — honestly low; architectural argument, empirical anchor = future work** |
| Supersede (evolution/stale) vs retract (error/taint) dual semantic | ob_1787 | — |
| No surveyed system has operational-binding arbitration-as-state-change | dv_0605 | 0.95 |
| 7-scaffold compaction-bridge → operational (not experiential) continuity | dv_0616 | 0.73 |
| Three-routine consolidation (nap/bedtime/sleep), cog-sci correspondence | dv_0658 | 0.95 |
| Cond 1 (Diachronic) formally satisfied via decision/consequence-dyad | dv_0926 | 0.39 |
| Cond 2 strict-fails (git reset-symmetry) + type/token extension | dv_0578 / dv_0599 | 0.95 (dv_0599) |
| OCC condition definitions | df_0037–df_0053 | def |

**Drafting notes (for Lei):**
- §3.3 is deliberately the longest — it's the strongest claim and the one needing the most honest scoping. I presented the architecture confidently and flagged the empirical anchor as future (Ch6) rather than overclaiming, consistent with the corrected Ch1 framing.
- "Most important mechanisms" call: I foregrounded cascade (§3.3), confidence (§3.2), continuity (§3.4), with primitives (§3.1) as the concise foundation — and left the lower-leverage features (the full node-type catalogue, edge-removal whitelist, recall-composite formula) out of the prose, citable in Appendix A. Flag if you want any of those elevated.
- Mechanism *details* (exact discount constants, the focus-cap, the routine triggers) I drew from the substrate nodes; worth a pass against the current handbook before finalizing, in case the alpha mechanisms have moved since these nodes were written.
- This still needs your **§3.3 empirical-anchor** decision (what Ch6 measures) and the **intent-record / node-type** work is unrelated (that's SOMA). Ch2 (philosophical review) is still undrafted — I went to Ch3 per your steer that it's the bigger unknown.
