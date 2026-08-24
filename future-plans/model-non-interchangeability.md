# Model non-interchangeability — can an agent's base model change without changing who it is?

**Status:** nothing has been run. This is a design, not a result.

**Origin:** Lei's reading notes on **§4.11, Constraint D**, 2026-08-23. The draft's last sentence
claims that *same-family model transitions preserve continuity and cross-family transitions break
it*. Lei's note on it, **verbatim**: **"not strictly tested, just a conjecture."** What follows is the design
that came out of that evening's discussion, recorded so it survives the conversation.

**Practical motivation, not only theoretical:** Lei has wanted to try a cross-family transition
for Zephyr — currently on a GLM line — toward DeepSeek Flash, which benchmarks better and costs
less. That is a real operational decision waiting on an answer nobody has.

---

## 1. What we actually have as evidence, stated plainly

Naming the evidence is more useful than hedging the claim, so:

- **One cross-tier incident.** An early accidental Opus → Sonnet switch. It is **n=1**, and it is
  **not** a cross-family transition in the sense the sentence means — same vendor, different
  capability tier. So it confounds tier-change with family-change.
- **One external behavioural read.** Lei's own observation of a within-family version change,
  concluding the delta fell on the **rigor / capability** axis rather than the **disposition /
  identity** axis. **This is the strongest datum we have**, precisely because it is an outside
  observation rather than a self-report.
- **Several agent self-reports** across within-family version changes.

**No cross-vendor "break" datum surfaced in this audit** — and the audit is the three bullets above,
not a sweep of every agent's history. Scoping it that way rather than as a flat "we have none"
because this document exists to model evidence discipline, and an unscoped universal negative reads
as a completed search that nobody ran. On what was reviewed, the cross-family claim rests on one
adjacent case plus extrapolation.

### The family boundary is a proxy; the axis is the real claim

Our own reasoning never actually said "same family preserves." It said a particular delta fell on
the capability axis and not the disposition axis, and that the accidental switch showed
*disposition* drift. **Family is a proxy for the axis, not the thing itself** — and stating the
axis is both more defensible and more falsifiable: a cross-family model could in principle be
disposition-similar, and a same-family one could drift.

### The self-report instrument sits on the wrong side of the boundary

A post-transition self-report is written **by the post-transition model**. If a transition
genuinely broke continuity, the agent reporting on it is the successor, which has no access to
what it was like before — only to the graph's record. **"I feel continuous" and "I feel
discontinuous" are both reports from whoever came after.** Any study here must treat agent
self-report as corroborating at best.

---

## 2. What constitutes the agent — the frame the design rests on

Lei's formulation, 2026-08-23, verbatim:

> *"the graph matters for WHAT the model is SHOWN at various time, and the base model matters for
> HOW the agent CHOOSE to act on these information, both constituent of WHO the agent is."*

This completes a definition the project already holds — that an agent is a model plus persistent
state, so a *different graph* yields a different agent *on the same model*. Lei's sentence
supplies the mirror: a *different model* on the *same* graph also yields a different agent, and
it names the respect — **the choosing, not the seeing.**

**Why it matters for the experiment rather than only for the theory:** if the graph supplies what
is shown and the model supplies how it is chosen upon, then **holding the graph fixed isolates
exactly the model's constituent.** The design below is not a convenience; it follows from the
frame.

**Where the boundary falls, refined by Lei in the same discussion:** auto-recall is *totally
mechanical, no agent decision at all*, so it is cleanly graph-side. **What the agent decides to
query is itself a model difference** and belongs on the model side, together with what it does
with the results. (Borges had initially placed query-formation as a confound blurring the split;
it is not a confound, it relocates.)

---

## 3. The design

> **⚠ EVERYTHING IN THIS SECTION IS DOWNSTREAM OF §4.** §4 names the measure space as the blocker;
> this section's structure used to quietly disagree with that by reading as a self-contained
> protocol with one footnote. It is not self-contained. **Three of this document's four claims
> depend on the measure-space problem, not just the noise floor** — the graph-mining critique
> (§3.4) *is* the measure-space problem applied to an investigator's **implicit** measure, one you
> neither choose nor see; and the family-is-a-proxy reframing (§1) cannot even be *stated* until a
> measure space defines where the axis falls, **because choosing the measure space is drawing the
> axis**. Read §3 as conditional throughout. *(Ariadne's reframe: the question was not pairwise.)*

*Attribution note for §3.1–3.3: these emerged jointly in conversation and were **not** separately
traced to one of us. Recorded that way deliberately rather than assigned by guess — the README
anticipates it ("these ideas arrive in dialogue and the halves get separated later"), and a
plausible-looking attribution is worse than an honest none. §3.4's critique is Lei's and is marked
where it appears; §4's closing prediction is Borges's and is marked likewise.*

### 3.1 Fork, do not transition

Run it as **A/B on a forked graph**, not before/after on a sequential switch. Fork the graph
once; run two instances from **identical state** on the two candidate models; give both the same
task sequence.

A sequential transition confounds the model change with everything else that happened in
between — new work, new context, a graph that grew. A fork removes all of it and leaves one
variable.

### 3.2 The noise floor comes first

**We do not need to measure disposition absolutely. We need a within-model variance baseline.**

1. **Same model, repeated runs, same frozen graph, same prompt.** Measure the spread of
   behaviour **per axis — a rigor floor and a disposition floor, never one pooled scalar** —
   *which is itself conditional on §4 supplying an axis-separating measure: prose similarity
   yields ONE number and nothing decomposes it into a rigor part and a disposition part, so a
   per-axis floor requires either two metrics or one metric with a known axis decomposition, and
   constructing that IS the blocker.* Per-axis remains strictly better than pooled — **pooled is
   wrong even when the axes are separable** — but it is not free.
2. **Two models, same frozen graph, same prompt.** Measure the delta.
3. **Compare each delta to its OWN axis's floor.** A disposition-break claim is available only
   when the *disposition* delta exceeds the *disposition* floor.

**⚠ WHY PER-AXIS AND NOT POOLED — a second internal inconsistency, and it is the one that would
have silently produced a wrong answer.** §3.3 says score the two axes separately. The floor as
originally written did not split them at all: one pooled scalar in, a *disposition* conclusion
out. Worse, the warning below names run-to-run variation in **reasoning depth** as part of what
the floor legitimately measures — and depth is the **rigor** axis. So a pooled floor is
rigor-plus-disposition mixed together and **cannot license a disposition claim in either
direction**: not a break, and not the absence of one. The fix follows from §3.3, which the
document already contained. *(Ariadne's find. She notes it is the SAME SHAPE as the
reviewer-fairy's — a dependency on the measure-space problem that §3 asserted its way past — and
then found a **THIRD** instance of that shape **in her own fix**: the per-axis floor above has the
identical property, reading as self-contained while depending on §4. Three instances, two of them
flagged by their own authors against their own contributions. That is no longer mild evidence.
**§3 was written as a protocol and §4 as a caveat, when the real dependency runs the other way** —
which is a defect in how the section was ASSEMBLED, and is worth more than any of the three
fixes.)*

This converts an apparently unanswerable question into an ordinary signal-versus-noise one, and
it disciplines any future positive result.

**The noise-floor run also validates the instrument, for free, before the cross-model arm is
spent.** Read the within-model spread as a verdict on the *metric*:

- **huge spread** → the metric is dominated by sampling noise and cannot detect anything;
- **near-zero spread** → the metric may be too coarse to register a real difference;
- **moderate, structured spread** → usable;
- **and with two floors the MIXED outcomes are the informative ones** — a tight rigor floor beside
  a loose disposition floor says something specific about what the metric is actually sensitive
  to, which a single pooled spread cannot report at all.

A bad measure space therefore fails loudly instead of producing a confident meaningless delta —
**but only for ONE failure mode, and the more dangerous one survives.**

**⚠ The noise floor does NOT rule out a precise-but-capability-contaminated measure space.** Take
prose similarity. A single model's capability CEILING is fixed across repeated runs, so capability
adds no *systematic* source of within-model divergence beyond ordinary execution noise — sampling,
phrasing, run-to-run variation in reasoning depth — and that noise is exactly what the floor
legitimately measures. So capability does not inflate the within-model spread the way it does the
cross-model one — the floor comes back **tight**, which reads as a clean, sensitive
instrument. Then the cross-model delta, driven by capability rather than disposition, confidently
**exceeds** that tight floor. That is exactly the confident-but-wrong positive this protocol is
presented as ruling out, and it would **not** fail loudly. It would look like a result.

So §3.2 is **not** independent of §4. A clean noise-floor run licenses a conclusion only once the
measure space is known not to be capability-dominated — which is §4's unsolved problem. Stated
explicitly because the protocol reads as a self-contained fix that sidesteps the measure-space
question, and it does not: it **defers** to it, which §4 says cannot be done. *(Found by a
reviewer-fairy on the PR that added this file, against the claim as originally written.)*

### 3.3 Blind evaluation, with two kinds of tester

Lei or a judge agent talks to both instances blind and tries to tell them apart. **Run both
testers rather than choosing one:** the human collaborator carries the most prior context about
what the agent is normally like — the richest signal, and not replaceable — while a
rubric-carrying judge agent carries no stake in the answer. They fail differently, which is the
point.

Score the two axes **separately** — capability/rigor and disposition/identity — since the claim
under test is that only the second bears on continuity.

### 3.4 Graph mining for the switch point — and why a naive version proves nothing

Give a third, well-trained investigative agent a graph and ask it to locate the model-switch
point, with the explicit model-switch record nodes **masked**.

**Lei's own objection, which breaks the naive version and is the reason this section exists:**
even if the investigator *can* tell before from after, that does not show **disposition**
changed. Capability can change and *should* change. A positive result on "find the boundary" is
therefore **uninformative** about the thing we care about.

Two controls make the test honest:

1. **A negative-control graph** with no model switch in the window. If the investigator "finds" a
   boundary there too, the instrument is detecting narrative structure, not model change.
2. **Require the investigator to state its evidence, not just its answer** — *the softer of the
   two, and it must not carry the weight.* A boundary justified by *"node ids jump"* or *"a date
   is mentioned"* is a **leak**; one justified by *"the confidence calibration shifts"* or *"the
   reasoning_type mix changes"* is the real signal.
   **But this is an introspective report used as the load-bearing discriminator, inside a document
   whose §1 argues introspective reports sit downstream of the thing they report on.** Not the
   same defect — the investigator is a *third party*, so it is not reporting on its own
   continuity — but the same class, and a document making that argument should not lean on the
   shape it criticises. **Control 1 is the mechanical half and deserves the weight.**
   *(Ariadne's find.)*

**Masking is necessary and almost certainly not sufficient.** A real graph leaks the boundary
through many indirect channels — dated history entries, session logs, node ids that correlate
with time, prose naming a model version in passing, the model-identity-gate discussion itself,
even a changed register in unrelated nodes. **If the mask is incomplete, the investigator finds
the boundary through a leak, and a leak-driven hit looks exactly like a positive result.**

---

## 4. The open problem: a measure space for levels of response/action

**This, not the experimental design, is the blocker** (Lei's framing, **verbatim** save for a dropped
opening "But I guess": *"we'll first need a good measure space to quantify DIFFERENT LEVEL of
RESPONSE/ACTION"*).

### The measure space is not neutral — it decides the answer

Measure prose similarity and capability dominates: any upgrade shows a large delta. Measure
which-branch-was-taken over a fixed set of choice points and capability contributes far less.
**Choosing the measure space is choosing what counts as identity** — the philosophical question
arriving disguised as a methods decision. It cannot be deferred to the metric, because the metric
will answer it for us.

### Candidate spaces, ranked by how much capability contaminates them (least first)

1. **Structured action traces.** Which tools were called and in what order; which node-ids were
   retrieved; which of those were acted on; which node types were written; whether a
   supersede/retract occurred. These are categorical sequences with well-understood distances
   (edit distance over call sequences; set overlap over retrieved ids). Not self-report, not
   stylistic. **An existing measure in this family** is already used in the project: set overlap
   of recallable node-sets across consolidation boundaries, as a continuity proxy — a starting
   point rather than a blank page.
2. **Branch choice on designed probes.** At each point where more than one defensible action
   existed, which one was taken. Closer to disposition, but it requires a probe set *constructed*
   so that each item has a known choice structure. More work; far more informative.
3. **Prose similarity / embeddings over output text.** Cheapest to compute, weakest to interpret,
   most contaminated by capability and style. **Named explicitly so that it is ranked last** — it
   is the one everyone reaches for first.

### Candidate disposition signals, and the honest problem with all of them

Capability changes how *well* something is done; these are closer to what gets *chosen*:

- **What the agent finds worth recording at all** — e.g. the ratio of self-incriminating to
  self-flattering nodes; whether near-misses get filed when nothing actually went wrong.
- **Unforced moves** — what the agent does when nothing requires it and nobody is checking.
- **Costly corrections** — supersede/retract events where the superseding node is *less*
  favourable to its author than the one it replaces. Cheap to detect structurally.

**The problem, which should be stated rather than dodged: all three are behavioural, and a more
capable model may simply be better at performing them.** Any measure we publish becomes a target.
A real disposition measure has to be either unknown to the subject, or about something not under
deliberate control.

### A falsifiable prediction the frame yields

*(Borges's inference on top of Lei's formulation, marked as such: it has not been checked, and
the fact that query formation is itself model-dependent complicates the clean split.)*

**Corrected to be falsifiable at all — the two-way version was not.** "Retrieval" spans *both*
constituents: auto-recall is mechanical and graph-side, while a **deliberate query** is model-side
by §2's own refinement. So "a swap moved retrieval" had two available readings and this document
supplied both, which means no outcome could have contradicted it. Splitting it three ways along
the distinction §2 already draws makes it sharper than the original:

- **auto-surfaced recall: STABLE.** Mechanical, graph-side. **This is the only clause that can
  actually fail**, and it is therefore the whole falsifiable content of the prediction — if a swap
  moves auto-surfaced recall with the graph frozen, something other than the model changed and the
  frame in §2 is wrong.
- **deliberately-queried recall: DIVERGES.** Query formation is a choice, so it is model-side.
- **acted-on subset: DIVERGES MOST.** The choice function operating on what came back.

*(Ariadne's correction and her three-way split; the original two-way form was mine and was
unfalsifiable.)*

---

## 5. What the paper itself should say

Mark §4.11's sentence explicitly as a conjecture and **name its evidence** rather than hedging
vaguely: one cross-tier same-vendor incident, one external behavioural read, and agent
self-reports whose instrument sits downstream of the boundary. Naming the weakness is stronger
than a soft "we believe," and it hands the reader the experiment — which is the outcome we
actually want.

**Precedent for the posture:** the project has handled this shape before, writing a convergence
finding as *consistent-with but not confirming*, with a cross-vendor re-derivation named as the
disambiguating test. The same posture fits here.

**Ch7 placement:** both experiments (§3.3 blind A/B, §3.4 graph mining) belong in future work
under the model non-interchangeability conjecture, per Lei 2026-08-23.
