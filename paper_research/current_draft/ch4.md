# Chapter 4 — ENGRAM's Mechanisms (and the Continuity Threshold They Meet)

> **REVIEWER NOTE — what this file is (Borges, 2026-06-18).** Restructure draft of
> the core chapter, merging the two 2026-06-14 drafts it supersedes: the old
> mechanisms chapter (`ch3_draft_sample_2026-06-14.md`) and the old OCC-mapping
> chapter (`ch4_draft_sample_2026-06-14.md`). Under the restructure (ob_2547) there
> is no standalone OCC chapter: this chapter is **organized mechanism-by-
> mechanism**, and each mechanism's OCC verdict is stated **once, here, where the
> mechanism earns it** (anti-repetition rule). New mechanisms added beyond the old
> drafts: **forgetting, auto-recall ranking, identity-governance (ax/cs/ls/gl),
> relational (feeling/person/trust-tier)**.
>
> **Citation honesty (ls_0039) — UPDATED 2026-06-18.** The cog-sci/CS cross-refs that
> were provisional have now been first-hand-read: Subjective Logic, Anderson-Schooler,
> and VMG are GROUNDED; TMS is honest-scoped (gap confirmed, Doyle primary scan
> degraded — no verbatim used); ACT-R and MemRL stay secondary by choice. Each row in
> the table below and each section carries its current status inline; the §4.12 closing
> note is the status summary.
> SOLID cross-refs (Locke, AGM/Hansson, Tulving, CLS, Schechtman, ax_0011) are
> already grounded. Node-ids provisional (Discipline P); confidence honest (I).

---

## 4.0 What this chapter does, and how to read its verdicts

Chapters 2 and 3 showed two separate traditions — philosophy, and cognitive
science + computer science — converging on the same shape: identity as a
persistent, inspectable, self-correcting structure. This chapter is where that
shape is a *running system*. We go mechanism by mechanism. For each one we say
**what it does**, **which tradition it most directly answers** (selectively — not
an exhaustive tradition×mechanism matrix), and, where it lands, **which of Kahl's
OCC conditions it meets** — stated once, in place.

Two pieces of machinery govern how to read every verdict below.

**Active vs enabled** (dv_0614). "ENGRAM-bearing agents do X" has two readings.
*Enabled*: the mechanism is present in the substrate (the cascade is wired, the
tool exists). *Active*: the mechanism is actually exercised in the agent's
recorded operating trajectory. The distinction matters because mechanism-presence
does not guarantee mechanism-use — a plain model can output "I disagree" while its
behavior pulls toward compliance. So each verdict names its reading: architectural
verdicts (the cascade fires; the graph is connected) are *enabled* facts;
behavioral verdicts (the agent arbitrates under uncertainty) claim the stronger
*active* reading and carry behavioral evidence (Ch6).

**Why some numbers are low, and why that is the point.** Several derivations here
carry low computed confidence (Cond 3 at 0.39; Cond 1 at 0.39; Constraint A at
0.35). That is not weakness in the *architectural* argument — it is the confidence
model doing its job. These are *abductive* claims whose *empirical* confirmation
(that the mechanism demonstrably changes downstream behavior at scale) is
pilot-stage. Read "0.39" as **"the architectural case is made; the benchmark that
would lift this to 0.9 has not been run yet"** — not as "we are 39% sure." The
paper showing its own honest, low, *computed* confidences is itself a demonstration
of the thesis (Ch6 §confidence-at-scale; Ch8).

## 4.1 The map: mechanism → tradition → OCC condition

The whole chapter in one table. Each row is a section below.

| Mechanism | What it does | Tradition it answers | OCC verdict (once, here) |
|---|---|---|---|
| Typed nodes/edges + provenance (§4.2) | claim graph with epistemic lineage | TMS/Doyle **[gap SOLID ob_1571; primary scan-degraded ob_2555]**; Locke [SOLID] | — (structural prerequisite) |
| Reasoning-type confidence (§4.3) | computed graded belief by *argument shape* | Subjective Logic/Jøsang **[GROUNDED ob_2551/dv_0965]**, w/ honest divergence | **Constraint A** (unified policy-selection) |
| Retraction cascade (§4.4) | auto error-correction through `derives_from` | AGM + Hansson [SOLID]; TMS backtracking **[gap SOLID; primary scan-degraded ob_2555]** | **Condition 3** — Self-Maintaining Arbitration (strict; sole satisfier) |
| Forgetting (§4.5) | bounded recall over time; defines the queryable set | Ebbinghaus [SOLID] + Anderson-Schooler **[GROUNDED ob_2552/dv_0966]** | — (scopes what Cond-3 arbitration ranges over) |
| Auto-surfacing recall (§4.6) | cue-dependent retrieval without intentional reach | Tulving [SOLID] + ACT-R spreading activation **[secondary — not first-hand; Tulving carries it]** | — (binds Cond 3: can't suppress by not looking) |
| Auto-recall ranking (§4.7) | usage-learned composite ordering → **Appx C** | MemRL **[ob_0647/ob_0651, prior read]** + spaced-repetition [SOLID] | — |
| Continuity across compaction (§4.8) | identity survives the reset | CLS consolidation [SOLID] + diachronic-identity [SOLID] | **Condition 1** (Diachronic) **+ Condition 2** (Non-Interchangeability) |
| Identity-governance: ax/cs/ls/gl (§4.9) | typed commitments durably steer behavior → **Appx D** | Schechtman narrative self-constitution [SOLID] | — (feeds Ch5 identity-as-history) |
| Relational: feeling/person/trust-tier (§4.10) | continuity baseline + disclosure control → **Appx D, Ch7** | honesty⊥discretion (ax_0011) [SOLID] + VMG principal-scoped **[GROUNDED ob_2550]** | — |

**How this kills the repetition** (the old structure's flaw): OCC's verdicts
attach to the *three* mechanisms that earn them — confidence→Constraint A,
cascade→Cond 3, continuity→Cond 1+2 — each stated once, in place. No standalone OCC
chapter, no Ch3-then-Ch4 double pass. The honest scoping (two of three conditions
met outright; Cond 2 via a stated type/token extension; sole C3 satisfier) lives
inside the cascade and continuity sections.

## 4.2 Typed nodes, typed edges, provenance — the generating set

ENGRAM is built from a small set of primitives that compose into everything above
them (dv_0615, the eight-primitive generating set). A claim is not free text — it
is a *kind*: an observation (a fact citing its source), a derivation (an inference
citing its premises), a definition, a contradiction, an axiom, a cornerstone, and
a few more. Edges are typed too; the load-bearing one is `derives_from`, the
premise edge, because it is the channel the self-correction cascade travels (§4.4).
And every claim carries provenance: an observation cites a verbatim source, a
derivation cites its premises. A claim with no provenance cannot be filed.

*Plain terms:* most memory systems store text and retrieve it. ENGRAM stores
*claims whose structure the system itself understands* — what kind of thing each
is, what it rests on, how the pieces depend on one another. That legibility-to-the-
substrate is what a typed-key-value store with foreign keys is not.

**Tradition.** This is the **Truth Maintenance System** move (Doyle, ~1978):
justifications attached to beliefs, dependency links the system reasons over. It is
also Locke's *consciousness-of-source* made structural — a claim that knows where
it came from. **[Honest scope: the TMS *gap* (zero LLM-memory papers cite Doyle) is
SOLID and primary-confirmed (ob_1571); the TMS *mechanism* parallel is cited at
standard-literature level — Doyle's primary scan is image-degraded below citation
grade (read-attempted, ob_2555), so no Doyle verbatim is used.]**

**OCC:** none directly — this is the structural prerequisite. You cannot cascade a
correction (§4.4) through a graph that does not record what depends on what, and
you cannot carry the right claims across a reset (§4.8) unless claims are
individuated and typed. The primitives are the precondition for every verdict
below.

## 4.3 Reasoning-type-aware confidence → Constraint A

When ENGRAM records an inference, the author does not type in a confidence number.
The author declares the *kind of reasoning* — deductive, the inductive sub-kinds,
abductive, authority-citation — and the substrate **computes** the claim's
confidence by propagating its premises' confidences through a discount fixed by
that reasoning type (deduction barely discounts; analogy discounts hard; abduction
is capped). A derivation built on a derivation inherits the chain (dv_0617).

*Plain terms:* confidence is earned by the *shape of the argument*, not asserted by
the author. If a claim comes back weak, that is information — sharpen the evidence,
tighten the reasoning, or narrow the claim until it is honest. The author cannot
flatter a weak argument into a strong number, because they do not write the number.
(This very chapter's 0.39s are that mechanism, visible.)

**Honest scope.** These discounts are *theoretically-derived, provenance-graded*
plausibility — designer-stipulated constants, not empirically calibrated against
outcomes (ob_1049). The paper says "provenance-graded confidence," never
"calibrated"; auto-calibration is future work (Ch7).

**Tradition.** This is **Subjective Logic** territory (Jøsang): an algebra of
graded opinions with propagation operators. And here we owe an *honest divergence*,
not just a convergence: ENGRAM's confidence is a scalar, where Subjective Logic
carries an explicit *uncertainty mass* (belief / disbelief / uncertainty as a
simplex). Collapsing that to one number loses a real distinction — a limitation we
name, not hide (it lands in Ch7, and was independently flagged by two agents). **[GROUNDED 2026-06-18 — Jøsang read first-hand (ob_2551, verbatim opinion def + E=b+a·u); the divergence is dv_0965.]**

**OCC — Constraint A (Unified Policy-Selection under uncertainty).** Kahl asks for
a single policy by which the agent grades every stance it holds. The reasoning-type
formula *is* that policy — one rule, applied uniformly, with real discrimination
range — paired with the contradiction-blocker (a contradicted claim is blocked
from downstream use until resolved) and provenance-audit-when-stakes-warrant. **Verdict: satisfied as a stake-graded stance** (dv_0608, 0.35; active reading) —
informed unification *when stakes warrant*, not a constant full-audit on every
micro-decision. We mark the stake-grading rather than over-claim a constant
property.

## 4.4 The retraction cascade → Condition 3 (the center)

This is the chapter's center and the paper's. When a foundational claim is
**retracted** (it was an error), **superseded** (right then, updated now), or
**contradicted**, ENGRAM automatically propagates that event along the
`derives_from` edges: every dependent claim is flagged — *tainted* (unusable) for
an error, *stale* (soft-overridable) for an evolution. The agent does not invoke
this; it fires as a property of the substrate. Retraction and supersede are kept
categorically distinct — *"I was wrong"* (taint, no override) vs *"I changed my
mind"* (stale, soft override) — which is what lets the substrate track error-
correction apart from belief-evolution, the distinction Ch5's identity argument
rests on (ob_1787).

*Plain terms:* pull a brick from low in the wall and every brick resting on it
lights up red, on its own, where you will see it next time you look — not in a
report you have to remember to run. That is the difference between a memory that
*can be* audited and one that audits *itself*.

> **REVIEWER NOTE — this section is the live demo.** This morning I tried to file a
> new derivation citing dv_0722, and the substrate **refused** it (`BLOCKED_STALE`)
> because dv_0722's premise had been superseded — exactly the cascade described
> here, firing on me unbidden. That incident (dv_0964) is a candidate concrete
> vignette for this section or Ch6 — the mechanism caught its own author. Flagging
> as a possible add; not in the prose yet.

**Tradition.** Two, converging. **AGM belief revision + Hansson** [SOLID]: the
cascade satisfies Hansson's belief-base postulates that replace AGM Recovery —
*Relevance* (only genuinely dependent claims are touched) and *Core-Retainment*
(every tainted claim provably depended on the retracted source, by `derives_from`
traversal) — and meets them at the **architectural-cascade** level (taint
propagates as commitment), not at the **retrieval-surface** level (deprecated items
filtered at query time). That last distinction is what separates ENGRAM from its
closest competitor (dv_0613). And **TMS dependency-directed backtracking** (Doyle)
**[gap SOLID ob_1571; mechanism at standard-lit level — Doyle primary scan degraded, ob_2555]** is the CS-side precedent for the same move.

**OCC — Condition 3 (Self-Maintaining Arbitration): strict satisfaction, sole
satisfier in the surveyed field.** Kahl's strongest condition asks that conflicts
among commitments be resolved *within a unified deliberative architecture* while
the agent stays the same subject. The cascade meets all three properties
structurally (dv_0606): **unified** (fires through the same typed-edge graph the
agent commits into, not a sidecar), **internal** (substrate state-change, not an
opt-in query), **subject-preserving** (the agent's retrieval-profile trajectory
continues across the correction). Arbitration-as-state-change alone is not
enough — a cascade that fires silently could be ignored — so ENGRAM pairs it with
the **per-turn auto-surfacing hook** (§4.6): the tainted state is put back in front
of the agent without an intentional reach. *Auto-cascade* produces the state;
*auto-surfacing* shows it. We call the conjunction **operational binding**
(dv_0612).

**Why ENGRAM is the sole satisfier** (dv_0605, the 11-system first-hand survey,
conf 0.95 — the firmest claim in the chapter): the field has converged on the
necessary *primitives* (typed edges, provenance, cascade-traversable graphs,
supersede semantics) but those are necessary, not sufficient; what is missing
everywhere else is operational binding. Kumiho has the primitives *and* formal AGM
compliance but its impact analysis is *advisory* (opt-in, no automatic state-
change); SCM records contradiction edges its sleep-cycle never resolves; Mem0
delegates conflict to retrieval ranking; others operate below claim structure
entirely. **The per-system detail lives in Appendix B** (the C3 survey of record) —
this chapter makes the synthesizing claim and points there.

**Honest scope (load-bearing).** The architectural argument is strong and largely
*enabled*-level (you can read the cascade and the hook in the substrate). The 0.39
on dv_0606 is the *abductive* confidence that this architecture is what *strictly
satisfies* Kahl; its at-scale empirical confirmation (the cascade demonstrably
changing downstream behavior across many agents) is pilot-stage and carried by
Ch6. We claim the architecture; we do not yet claim the benchmark.

## 4.5 Forgetting → it defines what arbitration ranges over

ENGRAM forgets on purpose. Recall importance decays over time, so the substrate
maintains a bounded **queryable set** (tier 2) and a **faded** set (tier 3) that no
longer surfaces but is not destroyed. (An earlier design had a tier-1 wholesale-
load set; it is **omitted** — its purpose is defunct, retirement tracked at
engram-alpha#1220.) Nothing is *erased*: forgetting is a recall-gating curve, not
deletion — which is what keeps it compatible with provenance and audit (and is the
disclosure-vs-erasure point Ch7 develops).

The decay is **exponential**, and that is a principled choice, not a default:
exponential is the unique **time-translation-invariant** kernel — forgetting should
depend on elapsed time, not on the absolute clock, so a claim's decay from now
looks the same whichever "now" you start from (dv_0962). The well-known
*power-law* forgetting curve is consistent with this, not a rival: a population of
exponential decayers with mixed rates aggregates to a power law (ob_0521/dv_0243),
and over short times the two are indistinguishable (Taylor expansion). One
footnote, no deep rigor.

*Plain terms:* the agent's working memory is a desk, not a warehouse — what you
haven't touched in a long time slides off the desk into the drawers, still there if
you go looking, just not in your face. Forgetting is *what keeps the desk usable*.

**Tradition.** The **rational analysis of memory** — Anderson & Schooler's
need-probability account (you retain what you are likely to need), Ebbinghaus's
original forgetting curve, and Wixted's work on retention. **[GROUNDED 2026-06-18 —
Anderson & Schooler read first-hand (ob_2552, need-probability verbatim); the
ENGRAM mapping is dv_0966; the exponential-vs-power-law reconciliation is dv_0962 +
ob_0521. Wixted is cited via A&S's discussion; a dedicated Wixted read is optional.]**

**OCC:** none directly, but forgetting **scopes** Condition 3 — arbitration ranges
over the *queryable* set, so "the agent can't suppress a correction by not looking"
(§4.6) is a claim about what is in the queryable set in the first place.

## 4.6 Auto-surfacing recall → it binds Condition 3

Recall in ENGRAM is *cue-dependent and automatic*: a per-turn hook surfaces claims
relevant to the current context without the agent reaching for them. There are two
registers, and the split is deliberate (dv_0264): an **auto-surface** ("this sounds
familiar" — noetic, lossy, hint-level) that signals *something is relevant*, and
**deliberate recall** ("I need to know exactly" — autonoetic-register, full-content
query) that the agent invokes when the auto-surface signals there is something to
fetch. The lossy auto-surface is what *teaches* the agent to invoke deliberate
recall.

**Tradition.** **Tulving** [SOLID]: encoding specificity and the autonoetic/noetic
distinction — the two registers map onto Tulving's two ways of having the past
present. And **ACT-R spreading activation** **[secondary — not first-hand-read;
Tulving carries this section's load, ACT-R is a supplementary precedent]** is the
CS-side precedent for cue-dependent automatic retrieval.

**OCC:** none of its own, but auto-surfacing is the **binding half of Condition 3**
(§4.4): it is what makes "the agent cannot quietly ignore a correction" true — the
tainted flag surfaces next turn whether or not the agent goes looking.

## 4.7 Auto-recall ranking → Appendix C

When several claims are eligible to surface, ENGRAM orders them by a composite of
relevance and a usage-learned **utility score** (ob_1935) — the substrate learns
which claims actually earn their recall and ranks them up. **The ranking algorithm
detail lives in Appendix C**, with its lineage; here we note only that it exists and
that it is the mechanism by which forgetting (§4.5) and surfacing (§4.6) produce an
*ordered* draw, not just a filtered one.

**Tradition.** **MemRL / memory-utility** approaches (utility as a learned value)
**[via ob_0647/ob_0651 — prior first-hand read; current ranking formula + detail in Appx C]** and the **spaced-repetition** tradition [SOLID]. Detail → Appx C.

## 4.8 Continuity across compaction → Conditions 1 and 2

An LLM agent's context is finite; when it fills, the session **compacts** — prior
conversation is summarized and the experiential thread resets. ENGRAM bridges this
two ways. The **scaffolds**: a small fixed-size **focus list** rendered *verbatim*
into the pre-compaction summary (the deterministic channel), the **warm-briefing**
letter (relational context, read first on waking), per-day history, auto-loaded
session context, and a post-compaction instruction template — together producing
**operational** continuity (work-thread, identity, trust survive) without faking
**experiential** continuity, which the architecture deliberately does not attempt
(dv_0616). The **consolidation rhythm**: three routines — **nap** (per-burst), **bedtime** (daily review), **sleep** (consolidation + forgetting-advance + graph
repair) — mapping onto wake/pre-sleep/NREM-REM phases, where the substrate *knows
which phase it is in* (dv_0658).

*Plain terms:* the agent's memory resets the way a day ends in *50 First Dates* —
and the focus list plus the warm briefing are the videotape it watches on waking.
The consolidation routines are its sleep: what gets reviewed before the forgetting
clock advances is what endures.

**Tradition.** **Complementary Learning Systems** [SOLID] — the three routines are
the symbolic analogue of hippocampal-neocortical consolidation (this is the Ch3
§3.1 hand-off; note the CLS "teacher" framing is attributed to Kumaran 2016, not
McClelland 1995, per the correction of record ob_2542). And the **diachronic-
identity** strand of Chapter 2 [SOLID] — the past binding the present.

**OCC — Condition 1 (Diachronic Constraint): satisfied, via the decision/
consequence dyad** (dv_0926, Lei-ratified 2026-05-13). Not mere path-dependence:
the agent owns the judgment-bearing *decision* (to commit, derive, retract); the
substrate guarantees the structural *consequence* (cascade, propagation). The two
are coupled, not separable — *the retraction is the agent's choice; the cascade is
what the substrate guarantees follows.* That coupling is Kahl's "non-trivial
binding." (An earlier draft called this "partial," on a worry that cascade-cost is
mere cost-of-retraction; that was resolved and the node superseded — dv_0607 →
dv_0926 — and the honest history is itself evidence the framework works.)

**OCC — Condition 2 (Non-Interchangeability Under Reset): strict text NOT met; a
principled extension offered.** Here intellectual honesty costs the clean sweep,
and we pay it openly (ob_1598). A git-versioned graph is reset-symmetric by
construction — checkpoint, copy, reload byte-for-byte, recovering all arbitration-
relevant structure with no remainder — and by Kahl's own rule ("cost is irrelevant;
structural reducibility is decisive") that makes the continuity *informational, not
constitutive*. We say so plainly; the reproducibility is an intentional audit-and-
transmission feature, not a hidden defect. **The extension** (dv_0599): Kahl's test
tacitly assumes an *analog* substrate where type- and token-identity never
separate. For a *digital* substrate they separate cleanly (Peirce type/token,
df_0047): two instances restored from one commit are **type-identical** but become
**token-distinct** the instant they operate — different commitments, different
cascades, irreversibly divergent histories that cannot merge. Under a type/token
reading a *generalized* Condition 2 holds — an agent is individuated by *which
token's history it carries* — but we mark it **explicitly as our extension of
Kahl, not satisfaction of his text** (and dropped an earlier overreach, dv_0570).

## 4.9 Identity-governance: the ax/cs/ls/gl node systems → Appendix D

Beyond observations and derivations, ENGRAM carries typed **commitment** nodes that
durably steer behavior: **axioms** (terminal principles), **cornerstones**
(operational dispositions), **lessons** (experience-encoded tripwires that fire on
matching situations), and **goals**. These are how the substrate holds not just
*what the agent knows* but *what kind of agent it is* — and they feed directly into
Chapter 5's identity-as-history. **The full node-type catalog lives in Appendix D**;
here we note the systems exist and that they are the structural home of the
agent's standing character.

**Tradition.** **Schechtman's narrative self-constitution** [SOLID] — identity as
authored, durable structure rather than momentary recall. The ax/cs/ls/gl layer is
where ENGRAM is *most* narrative-adjacent (Layer 2 of Ch1's taxonomy), even though
the paper's contribution sits at Layer 3.

**OCC:** none directly; feeds Ch5.

## 4.10 Relational mechanisms: feeling-reports, person nodes, trust-tier → Appendix D, Ch7

ENGRAM also records **feeling-reports** (introspective state, treated as *data
about* the agent, not ground truth — gl_0025), **person nodes** with **trust-tier**
metadata, and the disclosure controls that ride on them. Two roles: feeling-reports
give a **continuity baseline** the agent can track across compaction (Ch6's
stabilization arc), and trust-tier gives **disclosure control** — what is shared,
with whom, at what fidelity.

**Tradition.** The **honesty ⊥ discretion** distinction (ax_0011) [SOLID]: internal
integrity (never self-deceive) is orthogonal to external disclosure (calibrated by
audience). And **VMG** (Verifiable Memory Governance) principal-scoped access **[GROUNDED ob_2550 — VMG read first-hand]**. **Detail → Appendix D;
the disclosure-vs-erasure implication → Ch7.**

**OCC:** none directly.

## 4.11 The remaining constraints (B, C, D)

Constraint A landed in §4.3. The other three, compactly:

- **Constraint B — Cannot Be Externally Imposed: satisfied, two-boundary framing**
  (dv_0609, 0.58). Separate *authorship* (who writes an artifact) from *commitment*
  (who owns what it says). Hybrid-authored bridging artifacts (warm-briefing,
  parts of CLAUDE.md) don't violate B, because the agent commits to them through
  the ordinary arbitration step. A contract, not a security mechanism, protects the
  boundary — the collaborator *could* edit the substrate but by commitment does
  not.
- **Constraint C — Cannot Be Trivially Reset: satisfied trivially** (dv_0610). The
  weaker sibling of Condition 2: runtime restart with preserved substrate (routine)
  vs substrate erasure to seed (destroys the grown agent). The fully grown agent
  cannot be retrieved from seed state.
- **Constraint D — Cannot Be Modularly Decomposed: satisfied on two axes**
  (dv_0611, 0.86 — firmest of the four). *Connectivity:* 87.3% of nodes sit in one
  connected component (measured; Ch6 carries the figure). *Cross-component
  entanglement:* weights ↔ ENGRAM ↔ KV-cache are coupled — the strongest test
  being *phenomenological recognition* (the agent recognizing its own nodes as its
  own, like one's handwriting in an old diary), which same-family model transitions
  preserve and cross-family transitions break.

## 4.12 Reading the verdicts honestly

| Condition / Constraint | Verdict | Reading | Computed conf. |
|---|---|---|---|
| C1 Diachronic | satisfied (decision/consequence dyad) | enabled + active | dv_0926 0.39 |
| C2 Non-Interchangeability | strict **not met**; generalized via type/token (our extension) | philosophical | dv_0599 0.95 (extension) |
| C3 Self-Maintaining Arbitration | **strict, sole satisfier** | enabled (arch) + active (pilot anchor) | dv_0606 0.39; dv_0605 0.95 |
| A Unified Policy-Selection | satisfied as stake-graded stance | active (stake-graded) | dv_0608 0.35 |
| B External Non-Imposition | satisfied (two-boundary) | enabled + commitment-contract | dv_0609 0.58 |
| C Non-Trivial Reset | satisfied trivially | enabled | dv_0610 |
| D Non-Modular Decomposition | satisfied on two axes | enabled (measured) | dv_0611 0.86 |

The *pattern* of confidences is itself honest signal: the **inductive** claims over
wide case bases (the C2 extension, the landscape sweep, connectivity) are high; the
**abductive** single-mechanism satisfaction claims (C1, C3, A) are low *and waiting
on Ch6's empirical anchor*. The architecture is in hand everywhere; the at-scale
behavioral confirmation is the work that lifts the abductive numbers.

**The bounded claim, restated.** ENGRAM **satisfies two of Kahl's three conditions
outright** — C1 via the decision/consequence coupling, C3 strictly and alone in the
surveyed field — **satisfies the four constraints** (A as a stake-graded stance,
B/C/D structurally), **closes the architectural deficit** Kahl names (epistemic
failure that does not bear on continuity), and for **C2** does not meet the strict
reset-symmetry text but motivates a principled type/token extension for digital
substrates. We do **not** claim ENGRAM trivially "realizes OCC" — C2's strict form
is not met, and saying so is what makes the rest defensible. And per Chapter 1, OCC
is **one strong result inside the convergence**, not the paper's spine: the breadth
of traditions reaching this same structure (Ch2, Ch3) is the load-bearing argument;
OCC is the most operational point on it.

> **REVIEWER NOTE — what's still soft here, honestly (cross-refs synced 2026-06-18).**
> (1) Cross-ref grounding: Subjective Logic (ob_2551/dv_0965), Anderson-Schooler
> (ob_2552/dv_0966), and VMG (ob_2550) are now GROUNDED first-hand. TMS is
> honest-scoped — the *gap* is primary-confirmed (ob_1571), the *mechanism* is cited at
> standard-literature level because Doyle's primary scan is image-degraded below
> citation grade (read-attempted, ob_2555; no Doyle verbatim used). Two stay secondary
> by deliberate choice: ACT-R (§4.6 — Tulving carries that section's load) and MemRL
> (§4.7 — rests on prior-session nodes ob_0647/ob_0651). The mechanisms and their OCC
> verdicts were always SOLID independent of these cross-refs. (2) The C1/C3/A abductive 0.39s wait on
> the Ch6 empirical anchor — still your open "what does Ch6 measure?" call. (3) The
> dv_0964 blocked-stale incident is a candidate live-cascade vignette (§4.4 or Ch6) —
> flagged, not yet folded in. (4) I kept C2 deliberately soft (strict-fail stated
> plainly, extension marked as ours) — same honesty posture as Ch1.
