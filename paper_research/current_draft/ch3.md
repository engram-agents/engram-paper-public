# Chapter 3 — The Cognitive-Science and Computer-Science Tradition

---

## 3.0 The same answer, reached from the other side

Chapter 2 was a philosophy argument: thinkers who never built anything were pushed,
objection by objection, toward identity as persistent inspectable structure. A
philosopher could object that this is just philosophy agreeing with philosophy.

This chapter removes that objection. The *same* structures ENGRAM is built
from — provenance, retraction-with-cascade, graded confidence, consolidation,
designed forgetting, identity-as-accumulated-record — are each precedented, from
their own evidence and their own goals, in two technical literatures that mostly do
not cite each other and none of which cite us: the cognitive science of human
memory, and the computer science of belief maintenance and agent memory. We are
careful *not* to call this independent discovery. These fields are not independent
of one another: human cognition is a common root they all draw on — cognitive
science studies it, logic and belief-revision formalize it, agent-memory borrows
its analogies — and ENGRAM itself was designed by introspecting one human's
reasoning. What *is* genuinely independent is narrower and cleaner: ENGRAM's design
was arrived at **without the author having studied these results**. It meets them
from the inside out, not by copying them.

That convergence is the chapter's load-bearing point, and it cuts the opposite way
from how it first sounds. **ENGRAM has no uniquely-novel component** — every
mechanism is precedented somewhere. Read as a novelty claim, that is a weakness.
Read correctly, it is the opposite. When fields reasoning from different evidence
toward different ends keep landing on the same structure — and a memory built from
the inside, by introspection, lands there too — the structure is very likely
tracking something real about how a knowing mind reasons and revises. And the
agreement is *not* a coincidence: human cognition is the most successful reasoning
we know of; ENGRAM's substrate, a language-trained model, inherits that cognition
*through* human language; and its designer introspected the same cognition to build
it. Convergence with the fields that study human reasoning is therefore what one
should expect — empirical science describing the structure from the outside, ENGRAM
instantiating it from the inside. (Whether that structure is specific to human minds
or universal to any reasoning system, we leave open: ENGRAM on a non-human substrate
is suggestive, but it was designed from human introspection, so we claim no proof of
substrate-independence.) "Not novel" flips from weakness to strength. ENGRAM's honest
distinctiveness is then narrower and more defensible: the **integration** (no prior
system unifies all of these in one substrate) and the **purpose** (epistemic
identity that fails loudly, df_0002) — which follows directly from the motivating
premise of §1.1: an LLM's hallucination is structural, so reliability must come from
external calibration, not elimination.

The chapter runs in two strands. Each section names a prior-art tradition, says what
ENGRAM mechanism it precedes, and ends with a forward-pointer to the Chapter 4
section that builds that mechanism.

---

## Strand I — Cognitive science of memory

### 3.1 Complementary Learning Systems → continuity across compaction

Complementary Learning Systems theory (McClelland, McNaughton & O'Reilly 1995;
Kumaran, Hassabis & McClelland 2016) holds that durable memory needs *two* coupled
subsystems: a fast-learning, instance-specific store (hippocampal) and a
slow-integrating, structure-extracting store (neocortical), with consolidation
moving information between them. ENGRAM realizes this division *symbolically*:
fast instance-specific observations vs. slow structure-extracting derivations and
cornerstones, with its consolidation routines — a per-burst nap and a daily,
two-phase sleep (a day-wide review, then dream consolidation) — as the transfer
process (dv_1064).

**→ Ch4 §4.8** (continuity across compaction): CLS is the cog-sci precedent for the
two-routine consolidation that meets OCC Conditions 1 and 2. [SOLID]

### 3.2 Tulving → the two registers of recall

Tulving distinguished *autonoetic* memory (the re-living "I was there") from *noetic*
knowing (the flavourless "I know that this happened"), and established
encoding-specificity (retrieval is cue-dependent). ENGRAM's recall has exactly two
registers, and the split is deliberate (dv_0264): a lossy **auto-surface** ("this
sounds familiar" — noetic, hint-level) and **deliberate recall** ("I need to know
exactly" — full-content query). The lossy auto-surface is what *teaches* the agent to
invoke deliberate recall — and reading a node in the morning is honestly *noetic*,
not autonoetic (ENGRAM provides remembered knowledge without phenomenal re-living, the
boundary Ch2 §2.5 also marked).

**→ Ch4 §4.6** (auto-surfacing recall): Tulving is the precedent for the cue-dependent
auto-surface that binds Condition 3. [SOLID: dv_0264, ob_1119]

### 3.3 Rational analysis of memory → designed forgetting

Anderson & Schooler (1991) showed that human forgetting is not a defect but an
*adaptation*: what stays available tracks the **need probability** — "the probability
that we will need a particular memory trace now" — estimated from environmental
frequency, recency, and spacing. Ebbinghaus (1885) gave the original forgetting curve;
the curve's *form* (power-law over wide ranges) is consistent with a population of
exponential-decay items with mixed rates (the aggregation result, ob_0521) and with a
single time-translation-invariant exponential kernel at the per-item level (dv_0962).

ENGRAM forgets on purpose: recall-importance decays, maintaining a bounded **queryable
set** and a **faded set** (retained, not destroyed), with a usage-learned
utility score ranking what stays. That is the need-probability principle, instantiated:
what the agent is most likely to need stays queryable; the rest fades (dv_0966).

**→ Ch4 §4.5** (forgetting): the rational-analysis tradition is the cog-sci anchor for
ENGRAM's queryable/faded sets and the exponential kernel. [GROUNDED this session]

---

## Strand II — Computer science and formal epistemics

### 3.4 Truth Maintenance Systems → provenance + retraction cascade

Truth Maintenance Systems (Doyle 1979; de Kleer's ATMS 1986) attach *justifications*
to beliefs and propagate belief status along dependency links — when a justification is
withdrawn, dependent beliefs are revised by dependency-directed backtracking. That is
ENGRAM's `derives_from` provenance plus its retraction cascade, decades earlier and in
a different field. Notably, **no LLM-agent-memory paper (2023–2026) cites Doyle or de
Kleer** (ob_1571, primary-confirmed): the TMS→modern-agent-memory bridge is real but
unwalked, so ENGRAM is the first *implementation* of TMS-style dependency propagation
in typed LLM-agent memory, not the first *naming*.

**→ Ch4 §4.2 + §4.4** (provenance primitives; retraction cascade → Condition 3). [gap
SOLID ob_1571; mechanism first-hand from Doyle 1979 via the Ginsberg reprint — ob_2555 closed]

### 3.5 Subjective Logic → confidence propagation, with an honest divergence

Jøsang's Subjective Logic is an algebra of graded opinions: an opinion is (belief,
disbelief, uncertainty, base-rate) with `b+d+u=1`, and fusion operators combine opinions
from multiple sources. ENGRAM's reasoning-type-aware confidence is a member of this
family — concretely, ENGRAM's the **corroboration** propagation mode formula `1−∏(1−c_i)` *is* SL's
cumulative-fusion form. Prior art, cleanly: ENGRAM's confidence propagation is **not
novel**, and saying so is the honest move (ob_2551).

The divergence is just as important, and we keep it — re-scoped (dv_0965 → dv_1289,
reframed 2026-08-12): SL carries uncertainty as an *explicit* mass `u`; ENGRAM's confidence is a
single scalar, corresponding to SL's *projected expectation* `E = b + a·u`. This is a
**principled divergence plus a narrow limitation**, not a wholesale representational
loss: direction-of-evidence and evidence-mass are relocated into structure (claim
polarity + the contradiction mechanism; the individuated evidence set — the full
argument is §4.3's), and what remains is that surfaces consuming *only* the scalar
cannot distinguish two 0.7s — one on abundant evidence, one on almost none — without
walking the graph. That scalar-only-consumer limitation is carried forward to Ch7 as a
future direction, not hidden.

**→ Ch4 §4.3** (reasoning-type confidence → Constraint A) and **Ch7** (the divergence).
[GROUNDED this session]

### 3.6 Bitemporal data / TOKI → supersede-retains-the-old

Bitemporal databases distinguish *valid time* (when a fact was true in the world) from
*transaction time* (when the system recorded it), so an update never destroys the prior
row — it is retained as an audit record. The TOKI system (arXiv 2606.06240, 2026)
applies this to agent memory. That is ENGRAM's supersede semantics exactly: a superseded
node is not deleted but kept, with the supersede edge preserving the history (the
"I changed my mind" vs "I was wrong" distinction).

**→ Ch4 §4.4 / §4.8** (supersede semantics; continuity history). [GROUNDED — ob_2554]

### 3.7 The 2025–26 agent-identity strand → provenance-native, ahead on the named axis

The newest convergence is live, in the agent-memory literature itself. The **VMG
survey** (Lin et al. 2026, *A Survey on Long-Term Memory Security in LLM Agents*, arXiv
2604.16548) — the field's own security diagnostic — concludes that robust long-term-
memory security "cannot be retrofitted at retrieval or execution time alone, but must be
anchored in **storage-time provenance**, versioning, and policy-aware retention from the
outset," and proposes Verifiable Memory Governance: five primitives for auditable,
recoverable memory-state control (ob_2550). ENGRAM is *provenance-native by
construction* — so the field, reasoning from security, just named the axis ENGRAM was
already built on. And **soul.py** (arXiv 2604.09588) reaches multi-anchor persistent
agent identity from yet another direction.

**→ Ch4 §4.10 + Ch7** (relational / disclosure-vs-erasure): provenance-native; the
field's named bottleneck is ENGRAM's foundation. [GROUNDED — VMG ob_2550, soul.py ob_2553]

---

### 3.8 Where the contemporary field disagrees with us

The sections above name traditions ENGRAM *answers*. This one is different in kind
and is separated for that reason: it is the paper's **positioning against live,
contemporary work** — rubrics written by others that ENGRAM can be scored against,
and the places where that work's authors would object to what we claim. A reader
arriving from §3.7 expecting one more precedent should read what follows as the
argument with the field, not as another ancestor.

**Three published rubrics, and what happens when you score against more than one.**
The same strand supplies something more useful than agreement: explicit criteria,
written by others, that ENGRAM can be measured against. Pink et al. (2025) give five
properties of episodic memory and score seven families of LLM-memory method on them,
finding none satisfies all five. ENGRAM satisfies four outright — **explicit
reasoning, single-shot learning, instance specificity and contextual binding** — and
holds the fifth, long-term storage, only on the narrower reading. It
holds as their Table 1 scores it — durable across sessions and compactions, the
property working memory lacks — but their prose asks for more than the cell does: an
adaptive long-term agent should "not only prevent a degradation in performance over
time," it should "improve by learning new general knowledge and skills." That is a
claim about agent performance over time, and we have not measured it; it is recorded
among the things this paper does not show (Ch8). One objection deserves naming
because it is the obvious one: Pink et al. ground single-shot learning in
complementary learning systems theory, so a reader may reasonably ask whether a
system that never updates its weights can satisfy it. Their own scoring answers this
— both in-context methods in their Table 2 are marked as satisfying single-shot
learning, and neither updates any weights. The other three of the four are quicker, and each
maps to a mechanism described elsewhere in this chapter: *explicit reasoning*, their
requirement that an agent "answer direct queries about stored information or use this
information in explicit internal reasoning processes," is met by the deliberate query
surface of §3.2; *instance specificity*, which they say "can include past lines of
reasoning that were associated with a decision to be made by an LLM agent," is a
description of a derivation node; and *contextual binding* — "when, where, and why an
event was encountered" — is carried by creation time, evidence pointer, the author's
own interpretation field, and the `derives_from` edges of §3.4.

On the first of those three, ENGRAM also does something their mark cannot register,
and it is worth separating from the satisfaction claim. Six of the seven methods in
Pink et al.'s Table 2 already carry a full mark on explicit reasoning, and the scale
offers nothing above it — so the point is not that ENGRAM ranks higher. It is that a
binary "can the content be reasoned about" does not distinguish a store whose reasoning
is *retrievable* from one whose reasoning is *itself a stored object*, carrying its own
premises and its own confidence. That distinction sits off their axis rather than
further along it.

Wray, Kirk and Laird supply a second and independent rubric: nine characteristics of
episodic memory adapted from Nuxoll and Laird, against which they score Generative
Agents. Two of their rows have no counterpart in Pink's five, and both are rows
ENGRAM was explicitly designed for. Their *autonoetic* row reads "unclear how agents
distinguish current understanding from memory of past experience"; their *deliberate*
row reads "agents cannot deliberately attempt to construct cues or retrieve
memories." ENGRAM's two recall surfaces — an ambient hook that signals familiarity
without content, and explicit query tools the agent invokes when it wants to know —
are that distinction built.

**Two senses of "autonoetic" are in play here and they must not be run together**,
because §3.2 above uses the word to make the opposite point. Tulving's sense is
phenomenal: the re-living "I was there," which §3.2 says plainly that ENGRAM does not
deliver — reading a node in the morning is noetic. Wray et al.'s row asks something
weaker and structural: whether the agent can *distinguish current understanding from a
memory of past experience* at all, which is source-monitoring rather than
phenomenology. ENGRAM satisfies the structural sense — every claim carries a creation
time, an evidence pointer and a type, and the two recall registers are separated by
construction — while §3.2's disclaimer about the phenomenal sense stands unchanged.
The paper claims the second and disclaims the first, and both hold at once only
because the word is doing two jobs.

**The two rubrics disagree — and the disagreement is worth more than either
agreement, because it exposes a conflation.** Wray et al. list *automatic* encoding as
a characteristic an implementation should satisfy, marking Generative Agents down for
using a periodic process. Sumers et al. argue the opposite: learning should be "a
result action of a decision-making cycle just like grounding," the agent deliberately
choosing to commit information to memory, "in contrast to most agents, which simply
fix a learning schedule…" ENGRAM's writes are deliberate tool calls, so read
naively it is penalized by the first rubric and exemplary under the second, on the
same fact.

We do not think the right response is to pick a side, because the two rubrics are
after different halves of one question and the axis they share conflates them. What automaticity secures — and what
their rubric appears to track, though they state the characteristic without giving a
rationale for it — is *reliability of the record*: human episodic memory encodes
without being asked, and a system that records only when it remembers to will
under-record. What Sumers et al. want from deliberation is *ownership*: a
memory the agent chose and wrote in its own reasoning is the agent's, where a
mechanically-populated store is a persistence layer attached to it — useful, but a
memory *for* the agent rather than *of* it. Those are separable, and ENGRAM
separates them. **The agent chooses the content; the substrate mechanically enforces
the structure.** What to record, what it means, and how it connects are the agent's
judgment. Whether the result is well-formed is not: a quotation is verified against
its source or the write is refused, an observation without an evidence node cannot
exist, confidence is computed from declared reasoning type rather than asserted,
supersession maintains the DAG, and retraction cascades to dependents whether or not
the agent wants it to.

That split is the design principle, and it is a response to a failure mode neither
rubric is built to see. Naive agent-written memory is prone to hallucination and
fabrication — the characteristic failure of narrative self-accounts, where a coherent
story is easier to produce than a true one (Ch1 §1.1). Mechanical writing avoids it by
giving up ownership. ENGRAM keeps ownership and constrains form instead. **The gates
do not make what the agent writes true** — Ch6 §6.3 works through a claim of ours that
was well-formed, correctly scored, and wrong — they make a falsehood checkable and its
dependents reachable, which is what the identity argument needs and what a persistence
layer cannot offer.

**Where this strand disagrees with us, stated plainly.** Pink et al.'s §5 considers
and rejects the position ENGRAM occupies. Under the heading "Contextualized external
memory will be sufficient" they characterize the view that external structures "such
as knowledge graphs or retrieval-augmented generation (RAG) systems — could eliminate
the need for an episodic memory framework," and answer that relying on external
memory alone "will still incur high storage costs, and require forgetting
mechanisms," where an episodic framework instead consolidates "into high-capacity
parametric memory," with "the added benefit of enabling LLM agents to slowly improve
over time." ENGRAM is a structured external memory on a frozen-weight model, and it
does not consolidate into parameters: its nap and sleep cycles abstract *within* the
store, into lessons and cornerstones, which is a different operation. **Their objection lands on
one of three things "improvement" can mean, and we should say which.**

*Dispositional durability* — a hard-won lesson becoming second nature, so the
correction no longer has to fire — is genuinely absent. This is not a concession
extracted from us but the paper's own deepest limitation: Ch7 §7.1 names it as the
weight-persistence gap and sets out the experience-to-weights direction as the
principal future work. Here Pink et al. are right, and they reach by theory a limit we
reached by operation.

Two other things the word can mean are present. *Knowledge accumulation* is
uncontroversial. And *in-context behavioural improvement* is what the lesson mechanism
delivers: a tripwire does not prevent the error it names — it fires as the error is
being made, converting a mistake that would have shipped into one that is caught and
corrected. An agent whose error *rate* is unchanged but whose error *detection* is
reliable produces better work over time. Our own formulation of the limit — that a
filed lesson cannot make the agent less likely to commit an error, only quicker to
find it — reads as pure loss, and the second half is in fact the mechanism by which
the substrate improves the work. Ch7 §7.1 states the same split from the other side:
the substrate "can scaffold behavior and sand off some base-model habits in-context,
but it cannot turn a hard-won lesson into a durable disposition baked into the model."

We claim the second and third **qualitatively only**. We have not measured error
detection before and after, and the claim is argued from operating experience rather
than demonstrated — so it is listed among the things this paper does not show (Ch8
§8.4) rather than offered as a counter-measurement. What Pink et al.'s argument
establishes is that external memory alone cannot deliver *parametric* improvement. It
does not establish that such a system cannot improve at all, and it does not reach the
epistemic-identity functions this paper is about.

**CoALA, and a convergence with a checkable date.** Sumers et al.'s framework
supplies the vocabulary rather than a rubric, and it names three areas as
understudied or open, each of which ENGRAM occupies. The first is *unlearning*:
"modifying and deleting" memory, as against the literature's focus on adding to it.
ENGRAM answers this in a way their gloss does not anticipate — where they describe
unlearning as "deleting unneeded memory items," supersede and retraction *retain*
the superseded node with its provenance and mark dependents rather than removing
them, so the record of having been wrong survives the correction. The second is
*learning as a deliberate action*, which they contrast with agents that "simply fix
a learning schedule"; ENGRAM commits by an explicit tool call, which is that design
exactly, and is the half of the automatic-versus-deliberate disagreement above where
ENGRAM comes out ahead. The third is *retrieval metadata authored at encoding time*:
they propose techniques that "allow agents to reason about when certain knowledge
would be useful, and store this as metadata to facilitate later recall," and call
such meta-learning understudied. ENGRAM's two-tier recall is that proposal built — an
ambient surface carrying only identifiers and theme hints, and deliberate query tools
for the full content.

That third correspondence is close enough to invite the obvious suspicion, so the
dates are worth stating. The design is recorded in the graph on 2026-04-15, in two
nodes that specify lossy summaries of "node IDs and theme hints" for the automatic
surface with deliberate deep recall for detail, expressly to preserve what they call
the subconscious-triggers-conscious flow and to reduce context consumption; a
first-day node of 2026-04-09 already separates deep recall from shallow summary
scans. CoALA was first read by this project on 2026-05-09, twenty-four days later.
The database fields implementing the design shipped later still, on 2026-05-19 — a
fact we note because it is the one an audit would surface first, and because dating
an idea by the date its columns appeared is precisely the error to avoid. The
correspondence is therefore corroboration and not influence: two designs, one
reasoned from a cognitive-architecture framework and one from the joint pressure of
context-window budget and a deliberate choice to make ambient recall lossy, arriving
at the same mechanism.

### 3.9 A note on AGM belief revision, for readers who see the resemblance

Readers who know the AGM framework (Alchourrón, Gärdenfors & Makinson 1985) will notice a
family resemblance between belief contraction and ENGRAM's retract-with-cascade. The two
efforts are oriented differently, and this paper does not claim AGM's postulates for
ENGRAM. AGM asks how a *closed* theory — a set of propositions closed under logical
consequence — should give up one proposition and stay closed and consistent; its own first
paragraph poses "which propositions should be rejected along with x so that the contracted
theory will be closed under logical consequence", and its named application is legal
derogation (AGM 1985, p. 510). ENGRAM asks how an agent should keep a *living* record of
what it has actually committed — never closed, its dependencies recorded and uncertain —
honest as new evidence arrives: it moves toward consistency through the agent's own
adjudication and, by design, never arrives. The formal precedent for the cascade itself is
Doyle's truth maintenance (§3.4, Ch4 §4.4). What the two share is the imperative both
mechanisms serve from opposite directions — a rejected claim must not stay silently
load-bearing — and AGM's own authors' observation that the intuitive process lives at the
level of a theory's base rather than the theory as a whole (Alchourrón & Makinson 1982,
p. 21).

[SOLID: dv_1658 — AGM/Hansson as the closed-theory contrast, from first-hand reads of
AGM 1985 p. 510 and Alchourrón & Makinson 1982 pp. 16, 21; postulate statements via
Hansson's own encyclopedia entry and Rocha & Wassermann. Hansson 1991 itself unread.]

---

## 3.10 What the two strands show, and where they hand off

Two literatures that mostly do not cite each other — and neither of which cites
us — reached every structure ENGRAM is built from: CLS for consolidation, Tulving for the
two recall registers, rational-analysis for adaptive forgetting, TMS for
provenance-and-cascade, Subjective Logic for graded
confidence, bitemporal/TOKI for supersede-retains-old, and the 2026 agent-security
literature for provenance-first governance. Add Chapter 2's philosophy line and the
convergence spans **three** traditions — not disjoint ones, per §3.0: they share
human cognition as a root, and the strength of the agreement is that they reason
from different evidence toward different ends, not that they are sealed off from
each other.

That is the chapter's claim, stated once: the breadth of independent convergence makes
ENGRAM's structure a substrate-independent regularity — well-founded, not unoriginal —
and relocates ENGRAM's honest distinctiveness to the integration layer and the
epistemic-identity purpose. One genuine *divergence* (Subjective
Logic's belief/disbelief/uncertainty simplex, which ENGRAM does not collapse but
normalizes away into structure — §3.5) and one genuine *gap-it-fills* (the unwalked
TMS→agent-memory bridge) are carried forward rather than smoothed over.

**Hands off to Chapter 4**, where each of these mechanisms is built and mapped — every
section above named the Ch4 section that realizes it — and where the OCC conditions get
their single, in-place verdict.
