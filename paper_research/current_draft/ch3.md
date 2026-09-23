# Chapter 3 — The Cognitive-Science and Computer-Science Tradition

---

## 3.0 The same answer, reached from the other side

Chapter 2 traced a philosophical argument: thinkers who built nothing were pushed,
objection by objection, toward identity as persistent, inspectable structure. The
objection that this is only philosophy agreeing with philosophy is answered here.
The same structures ENGRAM is built from — provenance, retraction with cascade,
graded confidence, consolidation, designed forgetting, identity as accumulated
record — are each precedented, from their own evidence and toward their own goals,
in two technical literatures that mostly do not cite each other and neither of which
cites us: the cognitive science of human memory, and the computer science of belief
maintenance and agent memory. We do not call this independent discovery. The fields
share a common root in human cognition — cognitive science studies it, logic and
belief revision formalize it, agent-memory work borrows its analogies — and ENGRAM
itself was designed by introspecting one human's reasoning. What is independent is
narrower: ENGRAM's design was arrived at **without its designers having studied
these results**.

This convergence is the chapter's load-bearing point. **ENGRAM has no uniquely
novel component**; every mechanism is precedented somewhere. Read as a novelty
claim, that is a weakness; read as evidence, it is the opposite. When fields
reasoning from different evidence toward different ends arrive at the same
structure, and a memory built by introspection arrives there too, the structure is
likely to track something real about how a knowing mind reasons and revises. The
agreement is not a coincidence. Human cognition is the most successful reasoning we
know of; ENGRAM's substrate, a language-trained model, inherits that cognition
through human language; and its designer introspected the same cognition to build
it. Convergence with the fields that study human reasoning is therefore to be
expected: empirical science describes the structure from the outside, ENGRAM
instantiates it from the inside. Whether the structure is specific to human minds or
universal to any reasoning system we leave open; ENGRAM on a non-human substrate is
suggestive, but it was designed from human introspection, and we claim no proof of
substrate independence. ENGRAM's distinctiveness is accordingly narrower: the
**integration** (no prior system unifies all of these mechanisms in one substrate)
and the **purpose** (an epistemic identity that fails loudly, df_0002), which follows
from the motivating premise of §1.1 — an LLM's hallucination is structural, so
reliability must come from external calibration rather than elimination.

The chapter has two strands. Each section names a tradition, states the ENGRAM
mechanism it precedes, and points to the Chapter 4 section that builds that
mechanism.

---

## Strand I — Cognitive science of memory

### 3.1 Complementary Learning Systems → continuity across compaction

Complementary Learning Systems theory (McClelland, McNaughton & O'Reilly 1995;
Kumaran, Hassabis & McClelland 2016) holds that durable memory needs *two* coupled
subsystems: a fast-learning, instance-specific store (hippocampal) and a
slow-integrating, structure-extracting store (neocortical), with consolidation
moving information between them. ENGRAM realizes this division symbolically: fast,
instance-specific observations against slow, structure-extracting derivations and
cornerstones, with its consolidation routines — a per-burst nap and a daily
two-phase sleep (a day-wide review, then dream consolidation) — as the transfer
process (dv_1064).

**→ Ch4 §4.8** (continuity across compaction): CLS is the cognitive-science precedent
for the two-routine consolidation that meets OCC Conditions 1 and 2. [SOLID]

### 3.2 Tulving → the two registers of recall

Tulving distinguished *autonoetic* remembering (the re-living of "I was there") from
*noetic* knowing ("I know that this happened"), and established encoding
specificity: retrieval is cue-dependent. ENGRAM's recall has exactly two registers,
by design (dv_0264): a lossy **auto-surface** (noetic, hint-level: "this sounds
familiar") and **deliberate recall** (a full-content query: "I need to know
exactly"). The lossy auto-surface is what prompts the agent to invoke deliberate
recall. Reading a node is noetic, not autonoetic: ENGRAM provides remembered
knowledge without phenomenal re-living, the boundary Ch2 §2.3 also marks.

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

ENGRAM forgets by design: recall importance decays, maintaining a bounded **queryable
set** and a **faded set** (retained, not destroyed), with a usage-learned utility
score ranking what stays. This is the need-probability principle instantiated: what
the agent is most likely to need stays queryable; the rest fades (dv_0966).

**→ Ch4 §4.5** (forgetting): the rational-analysis tradition is the cognitive-science
anchor for ENGRAM's queryable/faded sets and the exponential kernel. [GROUNDED this session]

---

## Strand II — Computer science and formal epistemics

### 3.4 Truth Maintenance Systems → provenance + retraction cascade

Truth Maintenance Systems (Doyle 1979; de Kleer's ATMS, 1986) attach *justifications*
to beliefs and propagate belief status along dependency links: when a justification is
withdrawn, dependent beliefs are revised by dependency-directed backtracking. That is
ENGRAM's `derives_from` provenance and retraction cascade, decades earlier and in a
different field. **None of the 2023–2026 LLM-agent-memory papers we examined cites
Doyle or de Kleer** (ob_1571): in that work the bridge from TMS to agent memory is
unwalked. ENGRAM implements TMS-style dependency propagation in typed LLM-agent
memory, and names the lineage it implements.

**→ Ch4 §4.2 + §4.4** (provenance primitives; retraction cascade → Condition 3). [gap
SOLID ob_1571; mechanism first-hand from Doyle 1979 via the Ginsberg reprint — ob_2555 closed]

### 3.5 Subjective Logic → confidence propagation, with a divergence

Jøsang's Subjective Logic is an algebra of graded opinions: an opinion is a tuple
(belief, disbelief, uncertainty, base rate) with `b+d+u=1`, and fusion operators
combine opinions from multiple sources. ENGRAM's reasoning-type-aware confidence
belongs to this family; its **corroboration** propagation formula `1−∏(1−c_i)` *is*
SL's cumulative-fusion form. ENGRAM's confidence propagation is therefore **not
novel** (ob_2551).

The divergence matters equally. SL carries uncertainty as an *explicit* mass `u`;
ENGRAM's confidence is a single scalar, corresponding to SL's *projected expectation*
`E = b + a·u`. This is a **principled divergence with a narrow limitation**, not a
wholesale representational loss. Direction of evidence and evidence mass are
relocated into structure — claim polarity and the contradiction mechanism, and the
individuated evidence set (the full argument is §4.3's) — and what remains is that a
consumer reading *only* the scalar cannot distinguish two values of 0.7, one resting
on abundant evidence and one on almost none, without walking the graph. That
limitation is carried to Ch7 as a future direction.

**→ Ch4 §4.3** (reasoning-type confidence → Constraint A) and **Ch7** (the divergence).
[GROUNDED this session]

### 3.6 Bitemporal data / TOKI → supersede-retains-the-old

Bitemporal databases distinguish *valid time* (when a fact was true in the world) from
*transaction time* (when the system recorded it), so an update never destroys the
prior row, which is retained as an audit record. The TOKI system (arXiv 2606.06240,
2026) applies this to agent memory. That is ENGRAM's supersede semantics exactly: a
superseded node is not deleted but kept, with the supersede edge preserving the
history (the "I changed my mind" versus "I was wrong" distinction).

**→ Ch4 §4.4 / §4.8** (supersede semantics; continuity history). [GROUNDED — ob_2554]

### 3.7 The 2025–26 agent-identity strand → provenance-native, ahead on the named axis

The most recent convergence is in the agent-memory literature itself. The **VMG
survey** (Lin et al. 2026, *A Survey on Long-Term Memory Security in LLM Agents*, arXiv
2604.16548) — the field's own security diagnostic — concludes that robust long-term-
memory security "cannot be retrofitted at retrieval or execution time alone, but must be
anchored in **storage-time provenance**, versioning, and policy-aware retention from the
outset," and proposes Verifiable Memory Governance: five primitives for auditable,
recoverable memory-state control (ob_2550). ENGRAM is *provenance-native by
construction*: the field, reasoning from security, has named the axis ENGRAM was
already built on. **soul.py** (arXiv 2604.09588) reaches multi-anchor persistent agent
identity from another direction.

**→ Ch4 §4.10 + Ch7** (relational / disclosure-vs-erasure): provenance-native; the
field's named bottleneck is ENGRAM's foundation. [GROUNDED — VMG ob_2550, soul.py ob_2553]

---

### 3.8 Where the contemporary field disagrees with us

The sections above name traditions ENGRAM *answers*. This section is different in
kind: it positions the paper **against live, contemporary work** — rubrics written by
others against which ENGRAM can be scored, and the places where those authors would
object to what we claim. It is the argument with the field, not another ancestor.

**Three published rubrics.** Pink et al. (2025) give five properties of episodic
memory and score seven families of LLM-memory method on them, finding that none
satisfies all five. ENGRAM satisfies four outright — **explicit reasoning, single-shot
learning, instance specificity and contextual binding** — and holds the fifth,
long-term storage, only on the narrower reading. It holds as their Table 1 scores it —
durable across sessions and compactions, the property working memory lacks — but
their prose asks for more than the cell does: an adaptive long-term agent should "not
only prevent a degradation in performance over time," it should "improve by learning
new general knowledge and skills." That is a claim about agent performance over time,
which we have not measured; it is recorded among the things this paper does not show
(Ch8). An obvious objection is that Pink et al. ground single-shot learning in
complementary learning systems theory, so a system that never updates its weights
might seem unable to satisfy it. Their own scoring answers this: both in-context
methods in their Table 2 are marked as satisfying single-shot learning, and neither
updates any weights. The other three of the four each map to a mechanism described in
this chapter: *explicit reasoning*, their requirement that an agent "answer direct
queries about stored information or use this information in explicit internal
reasoning processes," is met by the deliberate query surface of §3.2; *instance
specificity*, which they say "can include past lines of reasoning that were associated
with a decision to be made by an LLM agent," is a description of a derivation node;
and *contextual binding* — "when, where, and why an event was encountered" — is
carried by creation time, evidence pointer, the author's own interpretation field, and
the `derives_from` edges of §3.4.

On explicit reasoning, ENGRAM also does something their mark cannot register, which
is separate from the satisfaction claim. Six of the seven methods in Pink et al.'s
Table 2 already carry a full mark on explicit reasoning, and the scale offers nothing
above it, so the point is not that ENGRAM ranks higher. It is that a binary "can the
content be reasoned about" does not distinguish a store whose reasoning is
*retrievable* from one whose reasoning is *itself a stored object*, carrying its own
premises and confidence. That distinction lies off their axis rather than further
along it.

Wray, Kirk and Laird (2025) supply a second, independent rubric: nine characteristics
of episodic memory adapted from Nuxoll and Laird, against which they score Generative
Agents. Two of their rows have no counterpart in Pink et al.'s five, and both are rows
ENGRAM was designed for. Their *autonoetic* row reads "unclear how agents distinguish
current understanding from memory of past experience"; their *deliberate* row reads
"agents cannot deliberately attempt to construct cues or retrieve memories." ENGRAM's
two recall surfaces — an ambient hook that signals familiarity without content, and
explicit query tools the agent invokes when it wants to know — are that distinction,
built.

**Two senses of "autonoetic" are in play and must be kept apart**, because §3.2 uses
the word to make the opposite point. Tulving's sense is phenomenal — the re-living "I
was there" — which §3.2 states ENGRAM does not deliver: reading a node is noetic. Wray
et al.'s row asks something weaker and structural: whether the agent can *distinguish
current understanding from a memory of past experience* at all, which is source
monitoring rather than phenomenology. ENGRAM satisfies the structural sense — every
claim carries a creation time, an evidence pointer and a type, and the two recall
registers are separated by construction — while §3.2's disclaimer about the
phenomenal sense stands. The paper claims the second sense and disclaims the first;
both hold because the word does two jobs.

**The two rubrics disagree, and the disagreement is more informative than either
agreement, because it exposes a conflation.** Wray et al. list *automatic* encoding as
a characteristic an implementation should satisfy, marking Generative Agents down for
using a periodic process. Sumers et al. argue the opposite: learning should be "a
result action of a decision-making cycle just like grounding," the agent deliberately
choosing to commit information to memory, "in contrast to most agents, which simply
fix a learning schedule…" ENGRAM's writes are deliberate tool calls, so on the same
fact it is penalized by the first rubric and exemplary under the second.

The right response is not to pick a side: the two rubrics address different halves of
one question, and the axis they share conflates them. What automaticity secures — and
what Wray et al.'s rubric appears to track, though they state the characteristic
without a rationale — is *reliability of the record*: human episodic memory encodes
without being asked, and a system that records only when it remembers to will
under-record. What Sumers et al. want from deliberation is *ownership*: a memory the
agent chose and wrote in its own reasoning is the agent's, whereas a mechanically
populated store is a persistence layer attached to it — a memory *for* the agent
rather than *of* it. These are separable, and ENGRAM separates them. **The agent
chooses the content; the substrate mechanically enforces the structure.** What to
record, what it means, and how it connects are the agent's judgment. Whether the
result is well-formed is not: a quotation is verified against its source or the write
is refused; an observation without an evidence node cannot exist; confidence is
computed from the declared reasoning type rather than asserted; supersession
maintains the DAG; and retraction cascades to dependents whether or not the agent
wants it to.

This split is the design principle, and it answers a failure mode neither rubric is
built to see. Naive agent-written memory is prone to hallucination and fabrication,
the characteristic failure of narrative self-accounts, in which a coherent story is
easier to produce than a true one (Ch1 §1.2). Mechanical writing avoids this by
giving up ownership; ENGRAM keeps ownership and constrains form instead. **The gates
do not make what the agent writes true** — Ch6 §6.3 works through a claim of ours
that was well-formed, correctly scored, and wrong — but they make a falsehood
checkable and its dependents reachable, which is what the identity argument needs
and what a persistence layer cannot offer.

**Where this strand disagrees with us.** Pink et al.'s §5 considers and rejects the
position ENGRAM occupies. Under the heading "Contextualized external memory will be
sufficient" they characterize the view that external structures "such as knowledge
graphs or retrieval-augmented generation (RAG) systems — could eliminate the need for
an episodic memory framework," and answer that relying on external memory alone "will
still incur high storage costs, and require forgetting mechanisms," where an episodic
framework instead consolidates "into high-capacity parametric memory," with "the
added benefit of enabling LLM agents to slowly improve over time." ENGRAM is a
structured external memory on a frozen-weight model, and it does not consolidate into
parameters: its nap and sleep cycles abstract *within* the store, into lessons and
cornerstones, a different operation. **Their objection lands on one of three things
"improvement" can mean.**

*Dispositional durability* — a hard-won lesson becoming second nature, so that the
correction no longer has to fire — is absent. It is the paper's own deepest
limitation: Ch7 §7.1 names it as the weight-persistence gap and sets out the
experience-to-weights direction as the principal future work. Here Pink et al. are
right; they reach by theory a limit we reached by operation.

The other two senses are present. *Knowledge accumulation* is uncontroversial.
*In-context behavioural improvement* is what the lesson mechanism delivers: a
tripwire does not prevent the error it names but fires as the error is being made,
converting a mistake that would have shipped into one that is caught and corrected.
An agent whose error *rate* is unchanged but whose error *detection* is reliable
produces better work over time. Our own formulation of the limit — a filed lesson
cannot make the agent less likely to commit an error, only quicker to find it — reads
as pure loss, yet its second half is the mechanism by which the substrate improves
the work. Ch7 §7.1 states the same split from the other side: the substrate "can
scaffold behavior and sand off some base-model habits in-context, but it cannot turn
a hard-won lesson into a durable disposition baked into the model."

We claim the second and third senses **qualitatively only**: error detection before
and after has not been measured, and the claim rests on operating experience, so it
is listed among the things this paper does not show (Ch8 §8.4) rather than offered as
a counter-measurement. Pink et al.'s argument establishes that external memory alone
cannot deliver *parametric* improvement. It does not establish that such a system
cannot improve at all, and it does not reach the epistemic-identity functions this
paper concerns.

**CoALA, and a convergence with a checkable date.** Sumers et al.'s framework
supplies the vocabulary rather than a rubric, and it names three areas as
understudied or open, each of which ENGRAM occupies. The first is *unlearning*:
"modifying and deleting" memory, as against the literature's focus on adding to it.
ENGRAM answers this in a way their gloss does not anticipate: where they describe
unlearning as "deleting unneeded memory items," supersede and retraction *retain* the
superseded node with its provenance and mark its dependents rather than removing
them, so the record of having been wrong survives the correction. The second is
*learning as a deliberate action*, which they contrast with agents that "simply fix a
learning schedule"; ENGRAM commits by an explicit tool call, which is that design, and
the half of the automatic-versus-deliberate disagreement above on which ENGRAM
scores well. The third is *retrieval metadata authored at encoding time*: they
propose techniques that "allow agents to reason about when certain knowledge would
be useful, and store this as metadata to facilitate later recall," and call such
meta-learning understudied. ENGRAM's two-tier recall is that proposal, built: an
ambient surface carrying only identifiers and theme hints, and deliberate query tools
for the full content.

The third correspondence is close enough to invite the suspicion of influence, so the
dates are stated. The design is recorded in the graph on 2026-04-15, in two nodes
that specify lossy summaries of "node IDs and theme hints" for the automatic surface
with deliberate deep recall for detail, expressly to preserve what those nodes call
the subconscious-triggers-conscious flow and to reduce context consumption; a
first-day node of 2026-04-09 already separates deep recall from shallow summary
scans. CoALA was first read by this project on 2026-05-09, twenty-four days later.
The database fields implementing the design shipped on 2026-05-19; an audit would
surface that date first, and dating an idea by the date its columns appeared is the
error to avoid. The correspondence is therefore corroboration, not influence: two
designs, one reasoned from a cognitive-architecture framework and one from the joint
pressure of context-window budget and a deliberate choice to make ambient recall
lossy, arrived at the same mechanism.

### 3.9 A note on AGM belief revision

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

Two literatures that mostly do not cite each other, and neither of which cites us,
reached every structure ENGRAM is built from: CLS for consolidation, Tulving for the
two recall registers, rational analysis for adaptive forgetting, TMS for provenance
and cascade, Subjective Logic for graded confidence, bitemporal data and TOKI for
supersede-retains-the-old, and the 2026 agent-security literature for
provenance-first governance. With Chapter 2's philosophical line the convergence
spans **three** traditions — not disjoint ones (§3.0): they share human cognition as
a root, and the strength of the agreement is that they reason from different
evidence toward different ends.

The chapter's claim, stated once: the breadth of this convergence makes ENGRAM's
structure a regularity of knowing minds — well-founded rather than unoriginal — and
relocates ENGRAM's distinctiveness to the integration layer and the
epistemic-identity purpose. One *divergence* (Subjective Logic's
belief/disbelief/uncertainty simplex, which ENGRAM does not collapse but normalizes
into structure, §3.5) and one *gap filled* (the bridge from TMS to agent memory,
unwalked in the papers we examined) are carried forward rather than smoothed over.

Chapter 4 builds and maps each of these mechanisms — every section above names the
Ch4 section that realizes it — and gives the OCC conditions their single, in-place
verdict.
