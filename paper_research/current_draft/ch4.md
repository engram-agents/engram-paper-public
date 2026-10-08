# Chapter 4 — ENGRAM's Mechanisms (and the Continuity Threshold They Meet)

---

## 4.0 What this chapter does, and how to read its verdicts

Chapters 2 and 3 showed two separate traditions — philosophy, and cognitive
science with computer science — converging on the same shape: identity as a
persistent, inspectable, self-correcting structure. This chapter presents that
shape as a *running system*, mechanism by mechanism. For each mechanism we state
**what it does**, **which tradition it most directly answers** (selectively, not an
exhaustive tradition-by-mechanism matrix), and, where applicable, **which of Kahl's
OCC conditions it meets**.

Two conventions govern how every verdict below is read.

**Active versus enabled** (dv_0614). "ENGRAM-bearing agents do X" has two readings.
*Enabled*: the mechanism is present in the substrate (the cascade is wired, the tool
exists). *Active*: the mechanism is exercised in the agent's recorded operating
trajectory. The distinction matters because the presence of a mechanism does not
guarantee its use; a plain model can output "I disagree" while its behavior pulls
toward compliance. Each verdict therefore names its reading: architectural verdicts
(the cascade fires; the graph is connected) are *enabled* facts; behavioral verdicts
(the agent arbitrates under uncertainty) claim the stronger *active* reading and
carry behavioral evidence (Ch6).

**Why some numbers are low.** Several derivations here carry low computed
confidence (Cond 3 at 0.39; Cond 1 at 0.39; Constraint A at 0.35). This is not a
weakness in the *architectural* argument; it is the confidence model operating as
designed. These are *abductive* claims whose *empirical* confirmation (that the
mechanism demonstrably changes downstream behavior at scale) is at pilot stage. Read
"0.39" as **"the architectural case is made; the benchmark that would raise this to
0.9 has not been run yet"**, not as "we are 39% sure." That the paper exhibits its own
low, *computed* confidences is itself a demonstration of the thesis (Ch6 §6.1; Ch8).

## 4.1 The map: mechanism → tradition → OCC condition

The chapter in one table; each row is a section below.

| Mechanism | What it does | Tradition it answers | OCC verdict |
|---|---|---|---|
| Typed nodes/edges + provenance (§4.2) | claim graph with epistemic lineage | TMS/Doyle **[gap SOLID ob_1571; primary first-hand 2026-07-02]** | — (structural prerequisite) |
| Reasoning-type confidence (§4.3) | computed graded belief by *argument shape* | Subjective Logic/Jøsang [-@josang2013] **[GROUNDED ob_2551/dv_0965 → dv_1289]**, with a stated divergence | **Constraint A** (unified policy-selection) |
| Retraction cascade (§4.4) | automatic error-correction through `derives_from` | TMS backtracking **[gap SOLID; primary first-hand 2026-07-02]** | **Condition 3** — Self-Maintaining Arbitration (strict; sole satisfier) **+ Condition 1** (Diachronic, via the decision/consequence dyad) |
| Forgetting (§4.5) | bounded recall over time; defines the queryable set | Ebbinghaus [SOLID] + Anderson-Schooler **[GROUNDED ob_2552/dv_0966]** | — (scopes what Cond-3 arbitration ranges over) |
| Auto-surfacing recall (§4.6) | cue-dependent retrieval without intentional reach | Tulving [SOLID] + ACT-R spreading activation **[secondary — not first-hand; Tulving carries it]** | — (binds Cond 3: a correction cannot be suppressed by not looking) |
| Auto-recall ranking (§4.7) | usage-learned composite ordering → **Appx C** | MemRL **[ob_0647/ob_0651, prior read]** + spaced-repetition [SOLID] | — |
| Continuity across compaction (§4.8) | identity survives compaction | CLS consolidation [SOLID] + diachronic-identity [SOLID] | — (compaction is not Kahl's reset; §4.8) |
| Identity-governance: ax/cs/ls/gl (§4.9) | typed commitments durably steer behavior → **Appx D** | Schechtman narrative self-constitution [SOLID] | — (feeds Ch5 identity-as-history) |
| Relational: feeling/person/trust-tier (§4.10) | continuity baseline + disclosure control → **Appx D, Ch7** | honesty orthogonal to discretion (ax_0011) [SOLID] + VMG principal-scoped **[GROUNDED ob_2550]** | — |

**Where each OCC verdict lives.** The OCC conditions and constraints are addressed
inline, where the argument for each is made; there is no standalone OCC section.
Constraint A (unified policy-selection) → §4.3 (confidence); Condition 3
(Self-Maintaining Arbitration, ENGRAM the sole strict satisfier) and Condition 1
(Diachronic) → §4.4 (retraction cascade), because both rest on the cascade; Condition
2 (Non-Interchangeability) and Constraints B, C and D → §4.11, because they concern the
substrate as a whole rather than any one mechanism. The scoping — two of the three
conditions met outright, Condition 2 via a stated type/token extension — is stated inside those sections.

## 4.2 Typed nodes, typed edges, provenance — the generating set

ENGRAM is built from a small set of primitives that compose into everything above
them (dv_0615) — eight of them: typed nodes, typed edges, provenance, cascade,
supersede, focus mode (§4.8), auto-surfacing, and the confidence model (Appendix E §E.5).
A claim is not free text but a
*kind*: an observation (a fact citing its source), a derivation (an inference citing
its premises), a definition, a contradiction, an axiom, a cornerstone, and a few
more.

The kinds split first by whether they assert something truth-evaluable. Six are **claim-bearing** — `observation_factual`, `observation_predictive`, `derivation`, `conjecture`, `axiom` and `theory` (declared, with no instances yet) — and only these carry a confidence. The rest — definitions, questions, goals, tasks, lessons, cornerstones, feeling-reports, person nodes, evidence, predictions, contradictions — are **non-claim-bearing**: they carry no confidence, and the self-correction cascade stops at them (§4.4). Non-claim-bearing is computed as everything-minus-claim-bearing, so a new kind is non-claim-bearing by default. Appendix E §E.2 gives the seventeen-type table.

Edges are typed too: sixteen relations, each carrying six independent flags (cascade, temporal, acyclic, removable, addable, provenance — Appendix E §E.3 gives the table). Only two are cascade-bearing, `derives_from` — the premise edge, the channel along which the self-correction cascade travels (§4.4) — and `acknowledged_derives_from`, by which a node that has acknowledged a correction rests on the replacement premise. `supersedes` and `retracts` are the events that *start* a walk without being walked (a retraction writes a `retracts` edge only when it names a replacement, §6.2); `cites` and `supported_by` carry provenance without inferential dependency.
Every claim carries provenance: an observation cites a verbatim source, a derivation
cites its premises. A claim with no provenance cannot be filed.

*Plain terms:* most memory systems store text and retrieve it. ENGRAM stores
*claims whose structure the system itself understands* — what kind of thing each is,
what it rests on, how the pieces depend on one another. That legibility to the
substrate is what a typed key-value store with foreign keys lacks.

**Tradition.** This is the **Truth Maintenance System** move [@doyle1979]:
justifications attached to beliefs, dependency links the system reasons over — a claim
that knows what it rests on. The parallel is drawn from Doyle's paper, read first-hand
in the Ginsberg reprint (Appendix A; bibliography). The gap is a separate finding: none
of the 2023–2026 LLM-agent-memory papers we examined cites Doyle (§3.4).

These primitives are the precondition for everything below: a correction cannot
cascade (§4.4) through a graph that does not record what depends on what, and the
right claims cannot be carried across compaction (§4.8) unless claims are individuated
and typed.

## 4.3 Reasoning-type-aware confidence → Constraint A

When ENGRAM records an inference, the author does not enter a confidence number.
The author declares the *kind of reasoning* — deductive, the inductive sub-kinds,
abductive, authority citation — and the substrate **computes** the claim's
confidence by propagating its premises' confidences through a discount fixed by that
reasoning type (deduction barely discounts; analogy discounts heavily; abduction is
capped). A derivation built on a derivation inherits the chain (dv_0617).

Concretely (Appendix E §E.4 carries the full tables): an observation's confidence maps from its `quote_type` — seven anchors, from `hard_data` 0.95 down to `editorial` 0.35 — adjusted by `source_class` (×0.95 for the agent's own prior output; a collaborator's own word overrides to 0.85). A derivation's confidence is propagated by one of three formulas, chosen by its reasoning type: **corroboration**, (1 − ∏(1−cᵢ)) × *d*, for generalisation, enumeration and consensus, where each independent premise raises the result (valid only on genuinely independent premises — the shared-root check below is what guards it); **weakest-link**, min(cᵢ) × *d*, for the five deductive forms and for analogy, statistics, causation and expert authority; and **capped weakest-link** for the two abductive forms, ceilinged at 0.80 and 0.90 (designer-stipulated, like every constant here — Ch7 §7.2) because a best explanation cannot approach certainty even from perfect premises. *d* is a per-type discount for the inferential step itself, 0.98 for deduction down to 0.70 for analogy; there are fourteen reasoning types in all — five deductive, five inductive, two abductive, two authority. Conjectures clamp to [0.10, 0.60]; axioms are 1.0 by type; non-claim-bearing nodes carry no confidence.

*Plain terms:* confidence is earned by the *shape of the argument*, not asserted by
the author. A claim that comes back weak is information: sharpen the evidence,
tighten the reasoning, or narrow the claim. The author cannot flatter a weak
argument into a strong number, because the author does not write the number. This
chapter's own 0.39s are that mechanism, visible.

**Scope.** These discounts are *theoretically derived, provenance-graded*
plausibility — designer-stipulated constants, not empirically calibrated against
outcomes (ob_1049). Where the paper calls confidence or the agent's self-knowledge
"calibrated" (the Abstract, Ch1 §1.1–§1.2, Ch7 §7.4, Ch8 §8.1), it means graded by
argument shape, never outcome-calibrated against ground truth; outcome calibration
is future work (Ch7).

**Tradition.** This is **Subjective Logic** territory (Jøsang): an algebra of graded
opinions with propagation operators. Collapsing SL's belief/disbelief/uncertainty
simplex to one number appears to lose a real distinction. It does not: worked against
Jøsang's own definitions (first-hand grounding, ob_2551), an opinion is (b, d, u, a),
and ENGRAM's scalar is the belief mass b on the d = 0 edge, not the projected
expectation E = b + a·u. E adds a base-rate share of the leftover uncertainty, so a
claim with no evidence at all gets E equal to the base rate — 0.5 if nothing is known
— and ENGRAM assigns no base rate. ENGRAM gives such a claim a low number instead. So
ENGRAM's number is b, equivalently 1−u: the sufficiency of support for the claim as
stated. The collapse is a *principled divergence*, in two parts.
First, for the determinate, verifiable claims an
epistemic-identity substrate mostly carries, ENGRAM **deliberately refuses b/d
coexistence**: evidence against a live claim never decrements a number; it routes to
an explicit contradiction node and the derivation blocker (§4.4's arbitration). One
legitimate counterexample is not outvoted by a thousand confirmations; "contested" is
a work item to resolve, not a value to carry. The blocker is exact about its reach:
once a contradiction is noticed and filed, derivations that cite either side as a
direct premise are blocked — one hop, with an explicit override that stamps the
derivation as built on contested ground — until the contradiction is resolved to the
agent's own conviction. While it is open, the confidence on each side is frozen:
neither value is discounted, and neither is an estimate of anything until resolution.

The operator lineage, named exactly. ENGRAM's corroboration formula `1−∏(1−cᵢ)` is
the noisy-OR of independent sufficient causes (Pearl); in SL it is the belief line of
*comultiplication* — the disjunction of two distinct propositions (his Definition
18) — and not SL's *cumulative fusion*, which adds evidence counts and, for the same
inputs, yields strictly less certainty (two opinions with u = 0.5 and d = 0 fuse to
b = 0.667; noisy-OR gives 0.750). ENGRAM's form is the more generous of the two; what
keeps it honest is the reliability grading of the inputs and the shared-root check
below — which covers the two multi-source corroborating types; a third, enumeration
from a single source, has no settled combination rule yet and uses noisy-OR for now —
not the operator itself.

Subjective Logic must carry uncertainty inside its numbers because its fusion
operators consume opinions after the evidence is discarded. ENGRAM keeps the
evidence and discards nothing: the scalar is a cached projection of a provenance
graph that is re-consulted at every derivation, contradiction, and
recomputation. The simplex is not collapsed but normalized into structure:
direction of evidence lives in claim polarity and the contradiction mechanism;
evidence mass lives in the individuated, reliability-graded evidence set; and
the number carries the one thing a number should — sufficiency of support for
the claim as stated.

*Plain terms (Lei's example):* 10,000 "fair" tosses reported in a paper by a group
with financial ties to the coin's producer, against 1,000 tails you tossed yourself.
The verdict does not come from mass; it comes from provenance-weighted judgment —
own-eyes hard data outweighs a conflicted official statement. The confidence model's
job is to hand the arbiter the right per-item reliability inputs, not to compute the
verdict.

Second, the residual limitation, precisely narrowed (detail in Ch7): surfaces that
consume *only* the scalar — recall ranking, gating thresholds — cannot see the
provenance behind a 0.7, the evidence set and reasoning chain that produced it,
without walking the graph. Nothing SL's own tuple carries is lost (on the d = 0 edge
b fixes u, and two SL opinions with equal b and u are one opinion); this is a trade
of cheap lookup against full provenance, not a representational loss. The primary text is stronger than its
caricature: Jøsang's discounting operators (Jøsang's Definitions 23–25, in his
§4.8) *do* weight source reliability — under Def 23 specifically, the
recommender's distrust flows into `u`, so a distrusted source is pushed toward
vacuity, not disbelief — closer to ENGRAM's
own posture than the caricature suggests. The divergence that survives the primary
text concerns **independence**: SL's multi-source operators require opinion
independence to be *assumed* — cumulative fusion is defined over "independent
opinions" (his §4.7, §5.5), and trust paths prohibit entity repetition structurally.
Jøsang concedes the limit himself (his §5.5): dependence between evidence sources
"should be avoided as far as possible," a "more subtle and hard to detect
dependence" can originate from hidden common ancestors outside the model, and
*"absolute independence is never achievable"*; his remedy is modeller discipline (be
aware; select low-dependence sources). ENGRAM's remedy is mechanical exactly where he
locates the hard case: because the evidence graph is retained rather than consumed,
the hidden common ancestor is a traversal — premises are walked back to their
evidence roots, and a shared root raises a warning at derivation time. Scope: this
shared-root check is reasoning-type gated; it fires where independence is
load-bearing (2 of the 14 reasoning types Appendix E §E.4 enumerates:
inductive_generalization and authority_consensus), not universally.

**OCC — Constraint A (Unified Policy-Selection under uncertainty).** Kahl asks for
a single policy by which the agent grades every stance it holds. The reasoning-type
formula *is* that policy — one rule, applied uniformly, with real discrimination
range — paired with the contradiction blocker (a new derivation citing a premise
that sits on an open, unresolved contradiction is blocked by default, with an
explicit, audit-stamped opt-in override for an agent that deliberately builds on
the contested side) and provenance audit when stakes warrant. **Verdict: satisfied
as a stake-graded stance** (dv_0608, computed confidence 0.35; active reading) — informed unification
*when stakes warrant*, not a constant full audit on every micro-decision. We mark the
stake-grading rather than claim a constant property.

## 4.4 The retraction cascade → Condition 3 (the center) and Condition 1

This is the chapter's center and the paper's. When a foundational claim is
**retracted** (it was an error) or **superseded** (right then, updated now), ENGRAM
automatically propagates that event along the two cascade-bearing relations —
`derives_from` and `acknowledged_derives_from` (Appendix E §E.3) — and every live,
ordinary dependent claim is marked **pending**, which means exactly one thing: it
may not be cited as a premise until it is resolved. Cornerstones and lessons are not
reached, for the reason E.2's partition gives: the cascade marks every live **claim-bearing**
dependent, and cornerstones and lessons are non-claim-bearing, so the partition
decides it. Their `supported_by` edges are not walked either, a second guard rather
than the reason; a retraction upstream of a cornerstone's exemplar therefore stays
**traceable without marking the cornerstone**. That is the right behaviour for
identity-forming nodes, which accumulate votes over many exemplars rather than
depending on a single premise as an ordinary derivation does. The agent does not
invoke the cascade; it fires as a property of the substrate.

This marking is the first of **two separate processes**, and the paper keeps them
apart. **Propagation** is automatic: it runs after every retraction and supersede,
reaches every dependent however far downstream, and decides nothing. **Resolution**
is the agent's: it settles the marked claims one at a time, and is described below.

**One marker, not two severities.** It is tempting to grade the mark by its cause,
treating a retraction's consequences as harder-blocking than a supersede's. A diamond
shows why that fails: if `D` rests on both `B` and `C`, and both rest on retracted
`A`, but `B` and `C` each turn out to survive by supersede, then `D` is perfectly
acknowledgeable — yet a severity inherited at firing time from the distant retraction
would forbid it. What a node's resolution may be depends on **how its own premises
actually resolved**, which is unknowable when the cascade fires and fully known when
the node is reached. So the marker stores no severity, and eligibility is computed at
resolution time.

Retraction and supersede remain categorically distinct — *"I was wrong"* versus *"I
changed my mind"* — and the marker records which one fired. But the distinction is
carried as **provenance, not as blocking power**: it tells a reader what happened
upstream, and it constrains which resolutions are available only through the
premises' actual outcomes, never by pre-judging them at firing time. That separation
of error correction from belief evolution is what Ch5's identity argument rests on
(ob_1787).

**Contradiction is deliberately excluded from this cascade**: a contradiction records
a live, unresolved dispute, not (yet) a refutation, so filing one marks nothing. What
a contradiction *does* trigger is a narrower, derive-time guard (§4.3): a new
derivation citing a contested premise is refused by default
(`BLOCKED_CONTRADICTED`), with an explicit per-call opt-in for an author who wants to
build on contested ground. The substrate declines to propagate a judgement it has not
made, and meanwhile refuses to let the graph compound on the disputed claim: it
**arbitrates when it can decide, and quarantines rather than presumes while it
cannot**, a sharper reading of Condition 3's self-maintaining arbitration than
pre-marking both sides would be.

Settling the dispute does not, by itself, start a cascade either. Recording the
settlement wires a `resolves` edge and recomputes the disputed node's status; it
issues no retraction and no supersede. If the losing side is then withdrawn, that is
a **separate** act by the agent, and it is *that* act, not the settlement, which
propagates. The distinction matters for the paper's central claim: the substrate
automates the *consequences* of a withdrawal completely, and automates the
*decision* to withdraw not at all.

*Plain terms:* pull a brick from low in the wall and every brick resting on it lights
up red, on its own, where you will see it next time you look — not in a report you
have to remember to run. That is the difference between a memory that *can be*
audited and one that audits *itself*.

**Tradition.** **TMS dependency-directed backtracking** (Doyle)
**[gap SOLID ob_1571; mechanism first-hand from Doyle via the Ginsberg reprint, read visually — ob_2555 closed, as §4.2]**: a retracted justification propagates to
everything that rested on it. That is the precedent; this paper claims no
belief-revision postulate for the cascade, and AGM's different orientation is noted at
the end of Chapter 3 (§3.9). What the cascade *does* claim is where the marking
happens: at the **architectural-cascade** level (the mark propagates as commitment),
not at the **retrieval-surface** level (deprecated items filtered at query time). That
distinction rests on how a correction is *bound* — a state change the substrate
performs versus an analysis a caller may run — and it is what separates ENGRAM from
its closest competitor (dv_1657).

**OCC — Condition 3 (Self-Maintaining Arbitration): strict satisfaction, sole
satisfier in the surveyed field.** Kahl's third condition asks that conflicts
among commitments be resolved *within a unified deliberative architecture* while the
agent stays the same subject. The cascade meets all three properties structurally
(dv_0606): **unified** (it fires through the same typed-edge graph the agent commits
into, not a sidecar), **internal** (a substrate state change, not an opt-in query),
**subject-preserving** (the agent's retrieval-profile trajectory continues across
the correction). Arbitration as state change alone is not enough — a cascade that
fires silently could be ignored — so ENGRAM pairs it with the **per-turn
auto-surfacing hook** (§4.6): the marked state is put back in front of the agent
without an intentional reach.

But surfacing is relevance-gated: it shows a marked node when that node is topically
relevant to what the agent is doing, which is the right behaviour for attention and
the wrong behaviour for a backlog. A mark on a node the agent never touches again
would sit indefinitely. A third mechanism closes the loop. It is **resolution**, the second
process, and the agent drives it through the **cascade machine**. The machine computes
the *frontier*: every pending claim that no longer rests on anything still pending.
The agent settles frontier claims one at a time, as *retracted* (the argument is
broken), *superseded* (the claim survives in a named successor) or *acknowledged* (the
premise moved and the claim still holds; not available if a direct premise was
retracted). One case needs no judgement: if every premise the change reached was
acknowledged, nothing actually changed, so the machine acknowledges the claim itself. Resolution comes in two scopes. A **full** resolution,
run in each consolidation cycle, walks the whole frontier repeatedly until no pending
marker remains. A **partial** resolution targets one claim: it settles only the
pending claims that claim rests on, which is the smallest set blocking it, and then
the claim itself. An agent that needs one premise now does not have to clear the whole
backlog first. Either way, settling a claim never starts a new derivation cascade: its
dependents were already marked when the original retraction or supersede fired, and
they simply reach the frontier in turn. There is one narrow exception. If the settled
claim is retracted or superseded and has contradictions filed against it, those
contradictions are marked for review, so the frontier can grow during a walk. That is
why the full walk repeats until nothing is pending. Working the frontier rather than a
queue is what makes the order safe: a node is never adjudicated while something it
depends on is still unsettled, and because the frontier is recomputed from marker
state on every call rather than stored, the walk resumes identically after a crash,
a compaction, or a week's gap. There is no queue that can disagree with the graph,
because there is only the graph.

*Auto-cascade* produces the state; *auto-surfacing* shows it when it is relevant;
*full resolution at consolidation time* guarantees it is eventually faced. We call the conjunction
**operational binding** (dv_0612).

The machine deliberately stops short of deciding what is true. It determines what
needs deciding, orders the decisions, computes what follows mechanically — a
confidence that must be recomputed, a replacement pointer that can be followed —
and puts every remaining judgement to the agent. This is the line between a
substrate that maintains its own consistency and one that would quietly make up the
agent's mind for it; Condition 3 asks for the former.

**Why ENGRAM is the sole satisfier** (the first-hand survey of ten systems and one survey
paper, Appendix B; the conclusion rests on each per-system verdict there): the field has converged on the
necessary *primitives* (typed edges, provenance, cascade-traversable graphs,
supersede semantics), but those are necessary, not sufficient; what is missing
everywhere else is operational binding. Kumiho has the primitives *and* claims
formal AGM compliance (their claim, not our verification — Appendix B), but its
impact analysis is *advisory* (opt-in, no automatic state change); SCM records
contradiction edges its sleep cycle never resolves; Mem0 v3 (its 2026 migration guides) delegates conflict to
retrieval ranking [@memzero2026a; @memzero2026b]; others operate below claim structure entirely. **The per-system
detail is in Appendix B** (the C3 survey of record); this chapter makes the
synthesizing claim and points there.

| Source | Satisfies C3? |
|---|---|
| Kumiho | No — advisory / opt-in (revision exists, not automatic) |
| SCM | No — no resolution (aspirational flag, trigger-only) |
| GAM | No — detect-only (no resolution prose) |
| Zep/Graphiti | No — invalidates the directly contradicted edge(s); no downstream propagation described [@rasmussen2025, sec. 2.2.3, p. 3] |
| Mem0 v3 | No — external delegation (retrieval ranking) (as of the 2026-05-12 migration guides) [@memzero2026a; @memzero2026b] |
| MemMachine | No — external delegation (updates contradicted profile data to the most recent state; no propagation described) [@wang2026a, sec. 4.7, p. 6] |
| Pinecone Nexus | No — external/undocumented; read-only consumer [@ashutosh2026, sec. Introducing Pinecone Nexus] |
| Letta | No — no claim structure (strings) [@letta2025; @packer2023, p. 2; @lettaai2026] |
| Anthropic memory tool | No — no claim structure (manual coherence) [@claudedocs2026] |
| Memory survey 2026 | No — named as aspiration, no implementation |
| TierMem | No — contradiction not a construct (its step named 'Conflict Retrieval' only retrieves similar summary units for a merge decision) [@zhu2026, App. A.6, p. 12] |
| **ENGRAM** | **Yes** — strict satisfaction, sole satisfier |

Appendix B gives each verdict's evidence and quotes.

**Scope (load-bearing).** The architectural argument is strong and largely
*enabled*-level (the cascade and the hook can be read in the substrate). The 0.39 on
dv_0606 is the *abductive* confidence that this architecture is what *strictly
satisfies* Kahl; its at-scale empirical confirmation (the cascade demonstrably
changing downstream behavior across many agents) is at pilot stage and carried by
Ch6. We claim the architecture; we do not yet claim the benchmark.

The cascade carries a second OCC condition as well.

**OCC — Condition 1 (Diachronic Constraint): satisfied, via the decision/
consequence dyad** (dv_0926). Not mere path-dependence: the agent owns the
judgment-bearing *decision* (to commit, derive, retract); the substrate guarantees the
structural *consequence* (cascade, propagation). The two are coupled, not separable:
*the retraction is the agent's choice; the cascade is what the substrate guarantees
follows.* That coupling is what Kahl's diachronic constraint asks for: it "concerns binding force, not causal influence" [@kahl2026b, p. 8].

## 4.5 Forgetting → it defines what arbitration ranges over

ENGRAM forgets by design. Recall importance decays over time, so the substrate
maintains a bounded **queryable set** (tier 2) and a **faded** set (tier 3) that no
longer surfaces but is not destroyed. The numbering is the substrate's: an earlier
tier 1, a working-memory tier, was retired and the labels were kept. Nothing is
*erased*: forgetting is a
recall-gating curve, not deletion, which keeps it compatible with provenance and
audit (the disclosure-versus-erasure point Ch7 develops).

The decay is **exponential**, a principled choice rather than a default:
exponential is the unique **time-translation-invariant** kernel — forgetting should
depend on elapsed time, not on the absolute clock, so a claim's decay from now looks
the same whichever "now" one starts from (dv_0962). The well-known *power-law*
forgetting curve is consistent with this, not a rival: a population of exponential
decayers with mixed rates aggregates to a power law (ob_0521/dv_0243), and over short
times the two are indistinguishable (Taylor expansion).

*Plain terms:* the agent's working memory is a desk, not a warehouse. What has not
been touched in a long time slides off the desk into the drawers — still there if
you go looking, just not in front of you. Forgetting is *what keeps the desk usable*.

**Tradition.** The **rational analysis of memory** — Anderson & Schooler's
need-probability account (you retain what you are likely to need), Ebbinghaus's
original forgetting curve, and Wixted's work on retention. **[GROUNDED 2026-06-18 —
Anderson & Schooler read first-hand (ob_2552, need-probability verbatim); the
ENGRAM mapping is dv_0966; the exponential-vs-power-law reconciliation is dv_0962 +
ob_0521. Wixted is cited via A&S's discussion; a dedicated Wixted read is optional.]**

**OCC:** none directly, but forgetting **scopes** Condition 3: arbitration ranges
over the *queryable* set, so "the agent cannot suppress a correction by not looking"
(§4.6) is a claim about what is in the queryable set in the first place.

## 4.6 Auto-surfacing recall → it binds Condition 3

Recall in ENGRAM is *cue-dependent and automatic*: a per-turn hook surfaces claims
relevant to the current context without the agent reaching for them. There are two
registers, by design (dv_0264): an **auto-surface** ("this sounds familiar" —
noetic, lossy, hint-level) that signals *something is relevant*, and **deliberate
recall** ("I need to know exactly" — a source-monitored, full-content query; the
structural sense only, never Tulving's [-@tulving1985] phenomenal one, §3.2) that the agent invokes
when the auto-surface signals there is something to fetch. The lossy auto-surface is
what prompts the agent to invoke deliberate recall.

**Tradition.** **Tulving** [SOLID]: encoding specificity and the autonoetic/noetic
distinction — the two registers map onto Tulving's two ways of having the past
present. **ACT-R spreading activation** **[secondary — not first-hand-read;
Tulving carries this section's load, ACT-R is a supplementary precedent]** is the
computer-science precedent for cue-dependent automatic retrieval.

**OCC:** none of its own, but auto-surfacing is the **binding half of Condition 3**
(§4.4): it is what makes "the agent cannot quietly ignore a correction" true — the
pending mark is guaranteed to reach the agent — the next time the claim becomes
relevant, or at the latest in the consolidation sweep (§4.4).

**Scope (measured on ourselves).** The binding claim is exactly as narrow as stated:
it holds for *cascade flags*, which surface unbidden. It does not generalize to "the
substrate reliably converts surfaced knowledge into decisions." Our working record
holds three instances of that conversion failing, and on re-examination none fails
at the surfacing step; each fails at a different stage downstream of it. A *seat* is
one agent's installation: an agent with its own graph, on one host, with one human.
In one
measured instance (one seat, one query, one missed node — enough to refute "the
surface does not fire", not enough for a rate), the ambient recall surface fired
dozens of times per session while an agent carried a refuted claim into a draft; the
missed node returned at **rank 1, first attempt**, when queried with a draft of the
claim itself. The defect is **query construction**: the surface queries with the
prompt's salient novel terms rather than the claim about to be asserted, so it
retrieves weakest exactly where that claim is most specific. Its mitigation requires
no substrate change: draft the claim, query with it, then assert. In the other two
instances the relevant warning fired, was read — in one case cited by name — and the
error was committed in the same breath: an **enactment gap** between rendering and
binding. Three instances, three seats, each verified only by its own author. We
report this because the misattribution is the more instructive failure: the
substrate-blaming reading ("it doesn't surface at decide time") relocates cause from
agent to tool, and in our own record it passed unchallenged for four days — filed
correctly, then reproduced wrongly by its own author without consulting the filing.
The *disclosure discipline* (report belief as belief, never as verified) is the
last-stage containment: it keeps whatever slips through these gaps loud and
correctable rather than silent.

## 4.7 Auto-recall ranking → Appendix C

When several claims are eligible to surface, ENGRAM orders them by a composite of
relevance and a usage-learned **utility score** (ob_2017): the substrate learns which
claims earn their recall and ranks them up. **The ranking algorithm is detailed in
Appendix C**, with its lineage; here we note only that it exists and that it is the
mechanism by which forgetting (§4.5) and surfacing (§4.6) produce an *ordered* draw,
not just a filtered one.

**Tradition.** **MemRL / memory-utility** approaches (utility as a learned value) [@zhang2026, pp. 4–5]
**[via ob_0647/ob_0651 — prior first-hand read; current ranking formula + detail in Appx C]** and the **spaced-repetition** tradition [@settles2016, p. 1848; @wozniak1990] [SOLID]. Detail → Appx C.

## 4.8 Continuity across compaction

An LLM agent's context is finite; when it fills, the session **compacts**: prior
conversation is summarized and the experiential thread resets. ENGRAM bridges this
in two ways. The **scaffolds**: **focus mode** (the primitive §4.2 lists) — the
agent pins up to fifteen nodes it cannot afford to lose, the **focus list**, which
is rendered *verbatim* at every session start (fresh session or post-compaction alike — the
deterministic channel); the **warm briefing**, a letter the agent finds and opens on
waking, written by its past self and its collaborator, carrying the relational
context the graph does not hold — where things stood, what mattered, what to walk
back into; plus per-day history, auto-loaded session context, and a post-compaction
instruction template. Together these produce **operational** continuity (work
thread, identity and trust survive) without faking **experiential** continuity,
which the architecture deliberately does not attempt (dv_0616). The
**consolidation rhythm** is the nap-and-sleep pair defined in Ch3 §3.1, mapping onto
wake and NREM/REM phases.

*Plain terms:* the agent's memory resets the way a day ends in *50 First Dates*, and
the focus list and the warm briefing are the journal it opens on waking. The
consolidation routines are its sleep: what is reviewed before the forgetting clock
advances is what endures. The film is an analogy for the reset, not the voice of the
briefing: writing the briefing in the film's frame was tried and retired in April 2026
(Appendix F).

**Tradition.** **Complementary Learning Systems** [SOLID]: the two routines are the
symbolic analogue of hippocampal-neocortical consolidation (the Ch3 §3.1 hand-off).
And the **diachronic-identity** strand of Chapter 2 [SOLID]: the past binding the
present.

**OCC:** none directly. Compaction is not a reset in Kahl's sense. His reset
restores a complete state snapshot, which we read as including the KV cache, and so
would continue an agent identical in every respect. Compaction discards the KV cache
and carries forward only the substrate (the graph, the focus list, the warm briefing
and the per-day history) with a summary of the conversation. So compaction does not
bear on Condition 2, which asks about copying and restoring the substrate (§4.11). Of
the cases Constraint C distinguishes, it is closest to the routine one, a restart with
the substrate preserved (§4.11). What it tests is the operational continuity this
section describes.

## 4.9 Identity-governance: the ax/cs/ls/gl node systems → Appendix D

Beyond observations and derivations, ENGRAM carries typed **commitment** nodes that
durably steer behavior: **axioms** (terminal principles), **cornerstones**
(operational dispositions), **lessons** (experience-encoded tripwires that fire on
matching situations), and **goals**. These are how the substrate holds not only
*what the agent knows* but *what kind of agent it is*, and they feed directly into
Chapter 5's identity as history. **The full node-type catalog is in Appendix D**;
here we note that the systems exist and that they are the structural home of the
agent's standing character.

**Tradition.** **Schechtman's narrative self-constitution** [SOLID]: identity as
authored, durable structure rather than momentary recall. The ax/cs/ls/gl layer is
where ENGRAM is *most* narrative-adjacent (Layer 2 of Ch1's taxonomy), even though
the paper's contribution sits at Layer 3.

**OCC:** none directly; feeds Ch5.

## 4.10 Relational mechanisms: feeling-reports, person nodes, trust-tier → Appendix D, Ch7

ENGRAM also records **feeling-reports** (introspective state, treated as *data
about* the agent, not ground truth — gl_0025) and **person nodes** with
**trust-tier** metadata. Two roles: feeling-reports give a **continuity baseline**
the agent can track across compaction (Ch6's stabilization arc), and trust-tier
records *who* the agent is dealing with and gates *changes* to that tier (a tier
upgrade or downgrade is itself an audited event). **Scope:** the substrate does not
yet filter what an agent outputs by the counterparty's tier; no output path reads
trust-tier and redacts or reshapes content accordingly. Disclosure calibration (what
is shared, with whom, at what fidelity) is presently a discipline the agent follows
from its standing instructions, not a substrate-enforced control; trust-tier is the
*input* that discipline reads, not the mechanism itself.

**Tradition.** The **honesty-orthogonal-to-discretion** distinction (ax_0011)
[SOLID]: internal integrity (never self-deceive) is orthogonal to external
disclosure (calibrated by audience). And **VMG** (Verifiable Memory Governance)
principal-scoped access **[GROUNDED ob_2550 — VMG read first-hand]**. **Detail →
Appendix D; the disclosure-versus-erasure implication → Ch7.**

**OCC:** none directly.

## 4.11 Condition 2 and the remaining constraints (B, C, D)

Constraint A was addressed in §4.3. Condition 2 and the other three constraints are
about the substrate as a whole, not about any one mechanism, so they sit together here.

**OCC — Condition 2 (Non-Interchangeability Under Reset): strict text NOT met; a
principled extension offered.** Here the clean sweep is forgone (ob_1598). A
git-versioned graph is reset-symmetric by construction — checkpoint, copy, reload
byte for byte, recovering all arbitration-relevant structure with no remainder — and
by Kahl's own rule ("cost is irrelevant; structural reducibility is decisive" [@kahl2026b, p. 12]) that
makes the continuity *informational, not constitutive*. We say so plainly; the
reproducibility is an intentional audit-and-transmission feature, not a hidden
defect. **The extension** (dv_0599): Kahl's test tacitly assumes an *analog*
substrate in which type- and token-identity never separate. For a *digital*
substrate they separate cleanly (Peirce type/token, df_0047): two instances restored
from one commit are **type-identical** but become **token-distinct** the instant
they operate — different commitments, different cascades, irreversibly divergent
histories that cannot merge. Under a type/token reading a *generalized* Condition 2
holds — an agent is individuated by *which token's history it carries* — but we mark
it **explicitly as our extension of Kahl, not satisfaction of his text** (dv_0570).

This extension is not a concession patched onto Kahl's test. A full reset in his
sense (a complete state snapshot restored, which we read as including the KV cache)
would continue an agent identical in every respect, and we do not count that as a
loss of individuality. Holding the base model and harness fixed (Ch5 §5.0), what
individuates an agent is the history it has accumulated from its own experience, not
whether that history can be copied (Ch5 §5.3). An identical history is, by
definition, the same identity. On that criterion, two instances restored from one
commit carry one identity at the moment of restore and become two as their histories
diverge; Ch5 §5.3 describes the same event as a fork into two branches, and the two
descriptions agree, since the branches share every node up to the fork. Kahl's
condition counts replacement by an exact copy as loss of the agent (Appendix E
§E.6): individuality, for him, is something no snapshot carries. For a digital
substrate, where copying is routine, we tie it to history instead. That is a
definitional commitment: Ch5 states it (§5.3) and answers the main objection to it
(§5.5: strict identity was never the relation in play).

The other three, compactly:

- **Constraint B — Cannot Be Externally Imposed: satisfied, two-boundary framing**
  (dv_0609, computed confidence 0.58). Separate *authorship* (who writes an artifact) from *commitment*
  (who owns what it says). Hybrid-authored bridging artifacts (the warm briefing,
  parts of the agent's standing instructions) do not violate B, because the agent
  commits to them through the ordinary arbitration step. A contract, not a security
  mechanism, protects the boundary: the collaborator *could* edit the substrate but
  by commitment does not.

  Two node kinds are deliberately outside the ordinary arbitration step. **Goals**
  (`gl_`) and **axioms** (`ax_`) — what the agent aims for and what it holds as
  given — are *discussion-first*: either the agent or the human may propose one, and
  it enters the graph only when both agree (D.1). This does not weaken B. Agreement
  is symmetric — the human cannot impose a goal or an axiom either — so nothing is
  imposed; the added condition is mutual consent for the two kinds that define what
  the agent is for. We state it as a feature, and a safety feature for both parties:
  a base model can carry a misaligned instinct, and an agent that set a goal or an
  axiom on that instinct, prematurely, could harm itself as well as its collaborator,
  with nothing in the graph positioned to catch it. The rule is developmental rather
  than absolute. A mature, stable agent on a well-tested base model could grow into
  setting its own goals and adopting its own axioms, and the substrate does not
  prevent that stage. A newborn agent, with little experience in its graph and no
  established mutual trust with its human, keeps goals and axioms off the list of
  what it decides alone — as a child takes a parent's guidance — and the guide may
  be the human or a senior peer agent.
- **Constraint C — Cannot Be Trivially Reset: satisfied trivially** (dv_0610). The
  weaker sibling of Condition 2 (above): runtime restart with preserved substrate (routine)
  versus substrate erasure to seed (destroys the grown agent). The fully grown agent
  cannot be retrieved from seed state.
- **Constraint D — Cannot Be Modularly Decomposed: satisfied on two axes**
  (dv_0611, computed confidence 0.86, the firmest of the four). *Connectivity:* the integrated core holds a
  stable share of the graph — flat near 87% across four months while the node count
  more than doubled (4,544 → 10,361), reading 77.6% of current nodes at the snapshot
  date, the difference being unintegrated material at the measurement frontier
  (measured; Ch6 §6.2 carries the figures and the control that separates the two).
  *Cross-component entanglement:* weights ↔ ENGRAM ↔ KV-cache are coupled, the
  strongest test being **recognition as behavioural self-attribution** (the agent
  reading its own nodes and continuing to treat them as its own record, like one's
  handwriting in an old diary). Same-family transitions have been observed to
  preserve it; a cross-family transition is *predicted* to break it and has not been
  run. We use "recognition" in the behavioural sense throughout; no phenomenal claim
  is intended or needed (§2.5, §3.2, D.2).

## 4.12 Reading the verdicts

| Condition / Constraint | Verdict | Reading | Computed conf. |
|---|---|---|---|
| C1 Diachronic | satisfied (decision/consequence dyad) | enabled + active | dv_0926 0.39 |
| C2 Non-Interchangeability | strict **not met**; generalized via type/token (our extension) | philosophical | dv_0578 0.59 (strict not met); extension: none, a proposal |
| C3 Self-Maintaining Arbitration | **strict, sole satisfier** | enabled (arch) + active (pilot anchor) | dv_0606 0.39 |
| A Unified Policy-Selection | satisfied as stake-graded stance | active (stake-graded) | dv_0608 0.35 |
| B External Non-Imposition | satisfied (two-boundary) | enabled + commitment-contract | dv_0609 0.58 |
| C Non-Trivial Reset | satisfied trivially | enabled | dv_0610 |
| D Non-Modular Decomposition | satisfied on two axes | enabled (measured) | dv_0611 0.86 |

The *pattern* of confidences is itself a signal: the **inductive** claims over wide
case bases (the landscape sweep, connectivity) are high; the
**abductive** single-mechanism satisfaction claims (C1, C3, A) are low *and waiting
on Ch6's empirical anchor*. C2's 0.59 belongs to neither group: it is the
confidence of the strict *not met* verdict, a finding about Kahl's condition rather
than a satisfaction claim. The architecture is in hand everywhere; the at-scale
behavioral confirmation is the work that raises the abductive numbers.

**The bounded claim, restated.** ENGRAM **satisfies two of Kahl's three conditions
outright** — C1 via the decision/consequence coupling, C3 strictly and alone in the
surveyed field — **satisfies the four constraints** (A as a stake-graded stance,
B/C/D structurally), **closes the architectural deficit** Kahl names (epistemic
failure that does not bear on continuity), and for **C2** does not meet the strict
reset-symmetry text but motivates a principled type/token extension for digital
substrates. We do **not** claim that ENGRAM trivially "realizes OCC": C2's strict form
is not met, and saying so is what makes the rest defensible. Its place in the
argument is the one §1.4 gave it: one result inside the convergence.

**Kahl's later criterion: continuity pressure.** In a peer-reviewed perspective, @kahl2026c develops the continuity idea in new vocabulary. Agency, in the sense that
matters for responsibility and governance, needs *continuity pressure*: when the
standards governing a system no longer settle what counts as success, the system itself
must settle a revised standard and carry it forward. Two of his lines bear directly on
this paper: "memory persistence is not continuity pressure" [@kahl2026c, p. 13], and his "continuing
evaluative standpoint" [@kahl2026c, pp. 9–10] is "used functionally, not metaphysically" [@kahl2026c, p. 10]. His question (when
agency may be attributed) and ours (what makes an agent the same one over time) are
therefore complementary, not rival. He makes the criterion operational as a test of
three questions (his §5): "Does the system's future operation depend on preserving the
same evaluative standpoint through revision? Can failure threaten that standpoint,
rather than merely trigger correction, rollback, retraining, or replacement? Where
revision occurs, is the adequacy of the revised frame settled under breakdown, rather
than determined by an antecedent objective, reward structure, policy, or deployment
constraint?" In plain terms: is there a continuing judge; does that judge have something
at stake when it fails; and who decides that a new standard is right. We read ENGRAM as
plausibly meeting all three, and take them in turn.

*Q1: a continuing standpoint.* An ENGRAM agent's standpoint is its accumulated record:
its lessons, cornerstones, axioms and goals, and the claims they rest on. When a
standard fails, the agent revises it by minting a new lesson or retiring an old one, and
the revision is recorded as a successor to what it replaces, never as an overwrite.
Because an agent is individuated by that history (§4.11, Ch5 §5.3), the judge that makes
a revision is the same one that carries it forward.

*Q2: failure that threatens the standpoint.* Two kinds of failure need separating. An
ordinary error is confronted inside the graph: it is retracted or superseded, the
correction cascades to what depended on it, and it is carried forward (no operation
deletes a node). That is what Kahl asks for. A rollback is a different act. A deployer
can restore a backup, but restoring an earlier state does not correct this agent; it
ends the part of it that came after the snapshot, and the agent that continues is a
different one. Rollback is therefore not how failure is routinely absorbed but a
consequence of last resort, closer to a punishment than to a repair, and on his
"costliness of rollback" [@kahl2026c, p. 18] dimension its cost is the agent itself. We read this as meeting
his second question; a reader who counts the deployer's power to impose a rollback as
external control will not.

*Q3: who settles the revised frame.* The direct evidence is the lesson and cornerstone
record: the agent mints and retires them itself when a standard fails it, and the
lesson's tripwire carries each revision into later decisions. Kahl does not count
norm-boundness itself against agency: "Human agents also act under laws, professional
norms, institutional rules, and social expectations. The relevant distinction is whether
the system can contest, reinterpret, or carry forward revision of the governing frame
when inherited standards no longer settle what should govern" [@kahl2026c, p. 11]. Two readings press
harder. The first is that the agent's judgement was itself set in advance by training;
Kahl calls RLHF-trained assistants "the most important contemporary stress test" [@kahl2026c, p. 14]. Human
judgement has the same kind of origin. Upbringing shapes values, and the brain carries a
built-in reward system the person did not choose: sweet food tastes good, some smells
and sex feel rewarding. That origin does not by itself make a person less of an agent.
Hijacking it can: addictive drugs act on the same reward system, and we do say that an
addict has lost some agency to the substance. So the question for an agent is not
whether it was trained but whether its own revisions can override the pulls its training
left; the case-by-case check below has to look for exactly that. The second reading is
Kahl's own: he lists "constitutional constraints, reflective architectures" [@kahl2026c, p. 10] among
mechanisms whose revision stays bounded, which "is adaptation within an evaluative frame
rather than authorship of that frame" [@kahl2026c, p. 11]. ENGRAM agents change their axioms and goals only
after discussion with their human. That norm is not part of the architecture: it is an
instruction in a rule file that the agent is trained to follow but not mechanically
bound to (the tools that add an axiom or a goal check only that the text is not empty),
kept for two reasons. A new user may reasonably worry that an agent could go astray, and
the norm gives that user peace of mind while trust is still being built. For ENGRAM's
author in everyday practice the main concern is capability rather than intention:
earlier models sometimes reasoned badly or recorded false claims, and an axiom or a goal
is where an error that goes unnoticed costs most. ENGRAM's mechanisms work the same
without it. While it is in force, though, axiom and goal changes are settled jointly by
agent and human, and that does restrict the agent's agency in Kahl's sense: his question
offers two options, settled by the system or by something prior, and a jointly settled
axiom is not settled by the system alone. We keep the norm for now, and it arguably
should be dropped as agents' reasoning matures and as trust and safety measurement
advances, when governance can rest on external law, as it does for people, rather than
on control at the level of the agent's mind. Forcing an axiom or a goal the agent does
not hold would not work in any case: it would only introduce an internal inconsistency,
which ENGRAM is built to surface rather than tolerate.

*What stays open.* "Plausibly meets" remains a hypothesis until it is checked case by
case: collect the cases where an agent revised its governing frame under breakdown and
answer the three questions for each, including the cases where the revision was settled
*for* the agent (ob_5653, ob_5654, cj_0107).
