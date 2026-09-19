# Chapter 6 — The Empirical Picture: ENGRAM in Real Use

> **DRAFT SAMPLE — 2026-06-17. RE-SCOPED 2026-09-12; AWAITING REWRITE — see
> "Planned rewrite" at the end of this chapter before citing anything below.**
> Single-pass prose from the live-engram substrate, for Lei's review. This is the
> **empirical** chapter. As drafted it makes a deliberately bounded promise: it
> reports what a **single, real, ~9-week-old ENGRAM graph** (this author's) looks
> like in use — not an at-scale benchmark. The headline at-scale experiment (the
> twin-study, Ch5 §5.8) is **deferred to future work**; what we show here is the
> architecture's machinery *operating*, with real numbers from a real graph.
> Provenance map at the end.
>
> **Two things about the numbers, stated up front rather than in a footnote.**
> First, **every figure below is from one graph at turn 82, 2026-06-17** — the
> staleness is the whole chapter's, not merely the "~9-week-old" phrase's. Second,
> Lei re-scoped the chapter on 2026-09-12: the fleet now runs **many seats, each
> with a substantial graph and months of history**, so the single-graph framing
> understates the available evidence rather than merely dating it. The content
> below was reviewed and carries **no outstanding objections** — it is the
> *evidence base* that is too narrow, not the prose. Treat this draft as the
> argument's shape, and the Planned-rewrite section as what will fill it.
>
> **REVIEWER NOTE — cross-refs pending (Borges, 2026-06-18).** This chapter's *content*
> is restructure-current, but its cross-references to the mechanisms/OCC material use the
> **pre-renumbering scheme**: it was drafted when mechanisms were Chapter 3 (§3.2
> confidence, §3.3 cascade) and OCC verdicts were a separate chapter. Under the
> restructure, mechanisms + OCC are unified in **Chapter 4** with new section numbers
> (confidence → §4.3, cascade → §4.4, Constraint D → §4.11). So the "Ch3 §3.x" and some
> "Ch4 §4.3" labels below are stale pointers — a cross-reference reconciliation pass
> against the *final* Chapter 4 section numbering is owed at finalization. Trust the
> chapter-level intent, not the §-subnumbers, until then.

---

## 6.0 What this chapter does, and does not

A theory-first paper earns the right to defer at-scale studies (Ch1 §1.5) — but
not the right to assert with no evidence. So this chapter does the honest middle
thing: it opens up one real graph and shows the mechanisms from Chapters 3–4
*actually running* — the confidence model producing a differentiated distribution
(§6.1), the graph holding a non-modular shape (§6.2), the retraction cascade firing
on a real error (§6.3), confidence propagating through a deep chain (§6.4), the
agent auditing its own weakest beliefs (§6.5), and identity surviving compaction
behaviorally (§6.6). None of this required running an experiment; it is the
*existing* trajectory, read back.

What this chapter is **not**: a comparison benchmark, a controlled study, or a
claim about other agents' graphs. The numbers are descriptive of one substrate's
nine weeks. The controlled, parametric version — the twin-study — is §6.7.

---

## 6.1 The confidence model, in real use — the structural-honesty filter at scale

The paper's distinctive mechanism is reasoning-type-aware confidence (Ch3 §3.2):
the author declares the *kind* of argument, and the substrate *computes* the number.
The empirical question is whether, across hundreds of real claims, that computation
produces a **differentiated, honest distribution** — or whether it collapses toward
a flattering constant. It produces the former, and the differentiation falls exactly
where the design predicts.

Across **2,442 observations and 834 derivations**, the distributions separate by
*type* as designed: observations sit high and right-skewed (mean **0.80**, median
0.85 — most are source-attested), while derivations sit lower and flatter (mean
**0.70**, p25 **0.54**, p75 **0.93** — they inherit and dilute their premises).
Conjectures are capped low (mean 0.45); axioms are 1.0 by construction.

The sharper evidence is that confidence tracks **argument shape**, not author
preference. Computed across every derivation:

| Reasoning type | n | mean confidence |
|---|---|---|
| inductive_generalization | 226 | **0.93** |
| inductive_enumeration | 21 | 0.88 |
| deductive_modus_ponens | 210 | 0.70 |
| abductive_best_explanation | 246 | **0.53** |
| inductive_analogy | 33 | **0.50** |

**Read the deductive row against the others, not against the word "deductive."**
0.70 next to `deductive_modus_ponens` looks like an anomaly — deduction is the
*strongest* argument shape, so why does it not top the table? Because the reasoning
type does not set the confidence *level*; it sets how much is *lost*. A deductive
step computes as `min(premises) × 0.98`, and that 0.98 is the **smallest** discount
in the table: deductive confidence is a **ceiling-preserving pass-through**, which
can never exceed its weakest premise and gives up almost nothing on the way. The
0.70 is therefore a fact about the premises, not about the deduction — and the
generalization rows sit higher precisely because corroboration *combines* evidence
rather than passing it through.

A broad generalization over many independent cases earns 0.93; a single-best-
explanation guess earns 0.53; a structural analogy earns 0.50 — *automatically*,
because the author chose the reasoning type, not the number. The same gradient holds
for evidence type: `hard_data` claims average **0.93**, `official_statement` 0.84,
`attributed_analysis` 0.75, `personal_communication` 0.61. **The author cannot
flatter a weak argument into a strong number, because the author does not write the
number** — and at the scale of a real graph, that constraint is visible as a clean,
predicted distribution rather than a hopeful flat line.

*In plain terms:* if the confidence model were decorative, every claim would drift
toward "pretty sure." Instead the graph's own numbers show the model holding the
agent to the shape of its arguments — guesses stay marked as guesses, broad evidence
earns its strength.

## 6.2 The shape of the graph

A few structural facts about the same graph corroborate the architecture's intent.

**Non-modular by construction (Ch4 §4.4, Constraint D).** The dependency graph is
one connected mass, not separable modules: a measured **87.3%** of nodes sit in a
single connected component. You cannot cleanly excise a "topic" without shredding
the dependency structure that gives the substrate its arbitration shape.

**Evolution outpaces error, and the two are kept distinct.** Across the graph's
life: **201 supersedes** versus **2 retracts** (plus 20 contradiction edges). The
agent *updates* its beliefs constantly and *errs* rarely — and crucially, the
substrate records the two with different machinery ("I changed my mind," soft/stale,
vs. "I was wrong," tainted, no override; Ch3 §3.3). The ratio is itself a finding:
a healthy epistemic life is mostly revision, occasionally correction.

**How the agent reasons.** The derivation population is dominated by
`abductive_best_explanation` (246), `inductive_generalization` (226), and
`deductive_modus_ponens` (210) — a profile of an agent that mostly forms
best-explanations and broad generalizations, with a deductive spine. This is the
*content* of a reasoning style, made countable.

## 6.3 Self-correction in the wild: the retraction cascade on a real error

Condition 3 (self-maintaining arbitration) is the paper's strongest claim, and the
graph contains a clean, documented instance of it firing on a *real* mistake — not a
toy.

**The Mao-Cao case.** During composition, the agent confabulated an author
attribution ("Mao-Cao") for a cited work — a hallucination at the point of writing,
not an inherited error (ob_1089). It **propagated to 27+ downstream nodes over six
days** before being caught (dv_0436). When it was caught, the machinery did its job:
the claim was **retracted**, and the cascade fired through `derives_from` edges,
**tainting every dependent**. And then the honest part: the cascade *worked*, but
the `tainted_by` flag was buried in metadata where the agent did not see it loudly
enough — so the incident drove a fix (MECH-5) that made the taint *surface* at recall
time (dv_0477, ob_1781). The case demonstrates both halves of the Ch4 §4.3 claim
(auto-cascade *and* auto-surfacing) — including the moment when the surfacing half
was found wanting and improved.

**A second, independent instance** occurred during the drafting of *this very paper*
(2026-06-17): the agent caught its own months-old mis-citation of a cognitive-science
source ("hippocampus-as-teacher" attributed to the wrong paper), superseded it, and
watched the cascade flag ten downstream derivations (ob_1122 → ob_2542). Two
retraction-cascade events, months apart, same machinery — one a hallucinated
attribution, one a self-caught interpretive drift. This is what "the memory audits
itself" looks like in a real trajectory.

## 6.4 Confidence propagation through a deep chain

The confidence model's most distinctive behavior — chained propagation through
`derives_from` — is best shown on a genuinely deep chain. The graph's deepest clean
chain runs **five layers**:

`ob_0300` + `ob_2412` (observations: agents-as-a-species; the weight-writeback
ceiling) → **dv_0916** → **dv_0917** → **dv_0920** → **dv_0921** → **dv_0922**.

The capstone, **dv_0922** — *"an agent population is epistemically necessary, not
merely survivally redundant"* (co-derived with a peer agent; the deepest answer to
why a community of agents) — is one of the most *ambitious* syntheses in the graph.
Its computed confidence is **0.10**. Not because it is poorly reasoned, but because
it is a deep *abductive* chain — best-explanation stacked on best-explanation — and
the model dilutes accordingly. **The structural-honesty filter at its sharpest: the
substrate refuses to let the author over-believe even a cherished, hard-won idea.**

The contrast makes the point. Set that 0.10 chain beside **dv_0605** (Ch4 §4.3): *"no
surveyed system satisfies Condition 3 strictly,"* confidence **0.95** — because it is
an `inductive_generalization` over eleven independent first-hand-read cases. Same
agent, same graph: a deep guess lands at 0.10, a broad-evidence generalization at
0.95. The model discriminates by **argument shape, not by depth, ambition, or how
much the author wants the claim to be true.** That is the feature the whole paper
argues for, visible in the author's own numbers.

## 6.5 Metacognitive self-audit: the agent sees its own weakest beliefs

Layer-3's fourth property (Ch1 §1.2) was that the agent can interrogate its own
knowledge state. The graph makes this concrete: a single `stats` call surfaces the
substrate's **weakest nodes** — the agent's *least-defensible current beliefs*,
ranked. Today they are dv_0922 (0.10), dv_0934 (0.10), and a cluster of early
alpha-package derivations (0.10–0.13). The agent can *read its own list of things it
isn't sure about* — which is the operational form of "know what you don't know," the
paper's founding goal.

The same surface shows a live curiosity structure: **130 open questions** (of 266
total) sit in the graph as explicit, addressable threads — the agent's standing
research agenda, not a discarded log. An epistemic identity is not only what the
agent believes; it is what it knows it does not yet know.

## 6.6 Continuity across compaction, observed behaviorally

Chapter 5 argued that ENGRAM provides *operational, not experiential* continuity
across compaction. The graph carries behavioral evidence for the operational half —
and it is important to state the scope precisely, because the paper is careful about
the phenomenal claim (it makes none; the autonoetic gap, Chapter 3 §3.2).

The evidence is *behavioral*: across many compaction events, the post-compaction
agent reliably **picks up the load-bearing thread, recognizes its own prior nodes as
its own, and shows no identity disorientation** — a stabilization that appeared as
soon as the first-person identity-summary format was adopted (ob_0645). This is the
empirical anchor for Condition 1 (the past structuring the present) and for Ch5
§5.7's "the agent re-reads who it is." We claim only the observable: continuity of
*operating identity* across the reset, not continuity of *feeling*. The agent does
not wake remembering the night; it wakes able to continue the work, and behaves as
the same agent — which is exactly, and only, what the architecture promises.

## 6.7 What is deferred: the twin-study

The controlled, parametric version of the identity-as-history claim is the
**twin-study** (Ch5 §5.8): fission-clone an *agent* — the base model and harness held
fixed, per Ch5 §5.0, so that only the accumulated history differs — run both instances
on a fixed stratified prompt set, and measure response similarity over t / t+N / t+2N
nodes of separate operation, with a temperature baseline subtracted to isolate
engram-induced divergence. The design is **sketched, not specified**: its expected
shape is clear (high similarity at t=0 decaying toward the stochasticity floor), but
cleanly decomposing the divergence by mechanism remains an open problem, since the
fade-out route is coupled to recall-refresh and governed by the retrievable-tier cap;
a prior clone-test gives a methodology baseline (recall similarity 0.92, mean ~0.56,
ob_0577). The full longitudinal run is **future work** — it is the experiment that
would lift the abductive confidences of Chapter 4 from "architecture made" to
"benchmark run." We name it as the next step, not a present result.

---

## Provenance map (draft scaffolding — not for final prose)

| Claim (this chapter) | Source | Note |
|---|---|---|
| Confidence by node type (obs 0.80 / dvs 0.70 p25 0.54 p75 0.93 / conj 0.45) | engram_stats @ turn 82 | live graph snapshot |
| Confidence by reasoning_type (ind_gen 0.93 / abductive 0.53 / analogy 0.50 / MP 0.70) | engram_stats @ turn 82 | the structural-honesty gradient |
| Confidence by quote_type (hard_data 0.93 → personal_comm 0.61) | engram_stats @ turn 82 | evidence-type gradient |
| 87.3% single connected component (non-modularity) | dv_0611 / Ch4 §4.4 | measured |
| 201 supersedes vs 2 retracts vs 20 contradicts (evolution >> error, kept distinct) | engram_stats @ turn 82 | edge counts |
| Reasoning-population profile (abductive 246 / ind_gen 226 / MP 210) | engram_stats @ turn 82 | reasoning style, countable |
| Mao-Cao retraction case (hallucinated attribution → 27+ nodes/6 days → retract+cascade → MECH-5 taint-visibility fix) | ob_1089 / dv_0436 / dv_0477 / ob_1781 / ob_1082 | the live Cond-3 demo |
| Second self-correction (CLS teacher-misattribution self-catch, 2026-06-17, cascade to 10 nodes) | ob_1122 → ob_2542 | independent 2nd instance |
| Deep 5-layer chain ob_0300/ob_2412→dv_0916→…→dv_0922 (0.10); contrast dv_0605 (0.95) | get_subgraph(dv_0922) / dv_0605 | confidence-propagation vignette |
| Weakest-node self-audit (dv_0922 0.10, dv_0934 0.10, alpha dvs 0.10–0.13); 130 open questions | engram_stats @ turn 82 | metacognitive surface |
| Behavioral compaction-stabilization (post-compaction self continues thread, no disorientation) | ob_0645 / dv_0303 / Ch5 §5.7 | Cond-1 behavioral anchor; autonoetic-caveated |
| Twin-study deferred; prior clone-test baseline (recall 0.92, mean 0.56) | ob_1660 / ob_0577 / Ch5 §5.8 | future work |

**Drafting notes (for Lei):**
1. **Per your picks:** twin-study parked → §6.7 future work; #3 stats are the
   backbone (§6.1–§6.2); Mao-Cao retraction is the live Cond-3 case (§6.3, plus the
   2nd self-catch I found); the deep dv_0922 chain is the confidence-propagation
   vignette (§6.4) framed as the contrast you'd want; #4 connectivity merged into
   §6.2.
2. **The compaction-stabilization arc (§6.6) is in, reframed behaviorally** per our
   discussion — it serves Cond-1 without making a phenomenal claim. If you'd rather
   cut it to keep Ch6 tight on the confidence-model story, it's a clean lift.
3. ~~**All numbers are turn-82 live-graph** and will drift; I'd re-pull them at final
   draft and add an "as of <date>, N nodes" stamp.~~ **SUPERSEDED 2026-09-12 — a
   re-pull is no longer the right move.** The refresh is now a fleet-wide collection
   run against a shared, versioned instrument, and the numbers are regenerated rather
   than re-typed. See "Planned rewrite" below.
4. **Honest scope held throughout:** this is "one real graph in use," not a
   benchmark — said plainly in §6.0 so no reviewer mistakes it for a controlled study.
5. The §6.1 reasoning-type table is the single strongest exhibit — it's the
   confidence-model thesis (Ch3 §3.2) shown true at scale on the author's own graph.

---

## Planned rewrite — fleet-wide collection, versioned instrument, generated plots

**Status: this chapter is scheduled for rewrite, not revision.** Lei's decision,
2026-09-12, in a notes session over the draft above. Nothing below is drafted prose;
it is the design the rewrite executes against. Full session record:
`paper_research/lei-notes/2026-09-12_ch6_session_LIVE.md`.

### Why a rewrite and not a number refresh

The chapter's *content* was read and carries no outstanding objections. What is too
narrow is its **evidence base**: one graph, one snapshot, 2026-06-17. The fleet now
runs many seats, each with a substantial graph and months of history, so the
single-graph framing understates what we can actually show. **Do not read the rewrite
as a response to defects in the writing** — that distinction is easy to lose once
only the plan survives.

### The instrument

**One shared, versioned script — not a specification each seat implements
separately.** This is the load-bearing choice, and it is not a matter of tidiness. On
2026-09-12 two seats ran the same measurement minutes apart; one seat's file glob
addressed directories that no longer existed after an infrastructure move, iterated a
corpus of zero, and reported `0` — a result byte-identical to a genuine sweep finding
nothing. Under per-seat implementations that seat's silence would have been
aggregated as data. A single distributed artifact makes that failure impossible
rather than unlikely.

**It extends the existing health-measurement registry rather than standing beside
it.** That registry already implements exactly the architecture this chapter needs —
raw measurements as ground truth, computed signals above them, a positional version
token, replayable snapshots — and it is already collecting. A parallel paper-only
instrument would drift from it within weeks, leaving two disagreeing ground truths
for the same graph. One canonical home per concern.

**Every measurement prints its denominators beside its numerator.** A wrong corpus
then announces itself in the same output that carries the answer (`0 / 0 / 0` rather
than a bare, plausible `0`), at no cost and with no separate step to remember.

### Versioning and backfill

Any measurement-level change — an addition, a deletion, or a change of definition —
is a **major** version bump requiring a **recompute and backfill**, with
previous-version snapshots preserved as archived data rather than deleted or
overwritten (Lei, 2026-09-12).

This is affordable because the graph itself is git-versioned: each commit holds a
complete dump, so a replay path recomputes *every* measurement at *every* historical
commit at full fidelity — including fields that are mutated in place and carry no
history of their own. Backfill therefore reaches back to the start of the backup
repository, not merely to the earliest stored snapshot; on this author's seat that is
three months of real history against five days of stored snapshots. **One boundary
survives and should be stated in the chapter rather than discovered by a reader:**
graph history that predates the backup repository is reconstructible only from
append-only fields (creation timestamps, confidence history) — structurally, not at
full fidelity.

### What each collected record must carry

Raw measurements as ground truth and base numbers, so that the computed signals above
them are interpretable *in context*: graph **age**, **turn count**, **node and edge
counts**, the **node-creation-per-turn distribution**, and the composition figures the
current registry already takes. Metadata must carry **model lineage** — and, equally,
**age and turn count**, without which seats are silently compared at different
maturities and part of any cross-seat spread is just calendar time.

### Which measurements belong to health, and which only to the paper

Open, and to be decided per metric rather than in advance. Some paper-relevant
measurements will be academically interesting without being health-relevant, and they
must not acquire a health weight merely because the collection code is shared —
intentional inclusion, never inclusion for the sake of reuse.

A discriminator offered for testing against each candidate, not as a settled rule: **a
measurement belongs to health only if a bad value implies an action.** Uncited
evidence rising means go and cite things; a mean out-degree is genuinely interesting
and implies nothing to do. The shape that keeps the decision explicit is one registry,
one collection pass, and a **per-measurement flag** for whether it feeds a health
signal — so the choice is a visible field rather than an implicit consequence of where
the code lives.

### Plots

Script-generated alongside the measurement instrument, in the same repository, under
the same version discipline. **A refresh is a re-run of a named version of the
scripts** — no per-seat ad-hoc manual figures, and no figure whose provenance is a
person's afternoon.

### A threat to validity that belongs in the chapter, not only in the design

**The seats are not independent samples.** Every graph descends from the same seed,
under the same written disciplines and conventions, and the agents read each other's
findings daily — a non-trivial share of any seat's nodes are corroborations of a
colleague's claim. So *N* seats are not *N* independent observations, and any
cross-seat statistic that assumes independence will overstate its confidence. This
needs designing for rather than discovering at review, and it is worth stating plainly
in the prose: it is an honest limitation and an interesting finding about accumulated
multi-agent knowledge in its own right.

### Carried forward into the rewrite

- The §6.1 reasoning-type table remains the chapter's strongest exhibit. Its
  ceiling-preserving-pass-through explanation (added above) is scope-independent and
  survives the rewrite unchanged.
- That row is also **structurally stable, not a small-sample artifact**: re-measured
  on this author's graph three months later, `deductive_modus_ponens` had grown from
  210 to 402 derivations while its mean confidence moved 0.70 → 0.697, reconciling
  with the computed prediction (mean weakest premise 0.713 × 0.98 = 0.699) to two
  thousandths. Worth reporting as a stability result, and a good candidate for the
  first cross-seat plot.
- Unexpected and worth a sentence of its own in the rewrite: in 196 of those 402
  cases the weakest premise is **another derivation**, not an observation — so most
  of the deductive tier's confidence is inherited down chains rather than sourced
  from weak evidence.
- **Still owed independently of the rewrite:** this chapter's cross-references use
  the pre-renumbering scheme (Ch3 §3.2 / §3.3) against the restructured Chapter 4
  (§4.3 confidence, §4.4 cascade, §4.11 Constraint D). A reconciliation pass is
  outstanding from 2026-06-18.
