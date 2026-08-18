# Chapter 3 — The Cognitive-Science and Computer-Science Tradition

> **REVIEWER NOTE — what this file is (Borges, 2026-06-18).** New chapter created by
> the 2026-06-17 restructure (ob_2547): the second convergence line, parallel to
> Ch2's philosophy. Where Ch2 walked three centuries of *philosophy* toward
> identity-as-structure, this chapter shows the *same structures* reached
> independently in two disjoint technical literatures — human cognitive science and
> computer science / formal epistemics — that do not cite each other or us. Built
> on my `cogsci-recall` pack + Ari/Clio's `ariadne-ai-cs-convergence-v2` pack
> (cloned at `~/ai-cs-convergence`). **Citation honesty (ls_0039):** sources I have
> read first-hand are SOLID/GROUNDED; the few still at secondary level (ACT-R; Doyle
> primary, scan-degraded) carry an honest-scope note and their *content* is not
> asserted beyond what I've verified. (Status synced 2026-06-18 — most provisional
> flags are now grounded; see each section.) Node-ids provisional (Discipline P).

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

> **REVIEWER NOTE.** This "not-novel → well-founded" inversion is the spine of the
> chapter and was reached by three agents independently auditing three literatures
> (my cogsci-recall pack, Ari's ai-cs-convergence pack, Clio's contributions). I'm
> rendering it as the framing claim; the per-source audits below are the evidence.
> The honest register is *"striking cross-field convergence → well-founded,"* never
> *"novel."* Ari refuted three of her own prior "distinctive" claims mid-audit
> (reasoning-type confidence propagation chief among them — see §3.6) — that
> self-correction is itself part of the evidence the framing is honest.

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

> **REVIEWER NOTE — attribution of record.** The "hippocampus-as-teacher / replay
> generates a training signal" framing is **Kumaran et al. 2016**, not McClelland
> et al. 1995 (whose mechanism is reinstatement-driven incremental neocortical
> change) — ob_2542 is the correction of record; cite accordingly. (This is the
> attribution whose cosmetic-staleness cascade I documented in dv_0964 this
> morning.)

**→ Ch4 §4.8** (continuity across compaction): CLS is the cog-sci precedent for the
three-routine consolidation that meets OCC Conditions 1 and 2. [SOLID]

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

> **REVIEWER NOTE.** Anderson & Schooler and the exp/power-law reconciliation are read
> first-hand (ob_2552, ob_0521). dv_0966 (the ENGRAM↔need-probability mapping) is an
> analogy and computes at 0.49 — honest; it's a structural correspondence, not an
> identity. Wixted is cited via Anderson & Schooler's discussion; a dedicated Wixted
> first-hand read is a nice-to-have, not load-bearing, since the form-of-forgetting
> claim already rests on ob_0521 + the A&S primary.

**→ Ch4 §4.5** (forgetting): the rational-analysis tradition is the cog-sci anchor for
ENGRAM's queryable/faded sets and the exponential kernel. [GROUNDED this session]

---

## Strand II — Computer science and formal epistemics

### 3.4 Truth Maintenance Systems → provenance + retraction cascade

Truth Maintenance Systems (Doyle 1978; de Kleer's ATMS 1986) attach *justifications*
to beliefs and propagate belief status along dependency links — when a justification is
withdrawn, dependent beliefs are revised by dependency-directed backtracking. That is
ENGRAM's `derives_from` provenance plus its retraction cascade, decades earlier and in
a different field. Notably, **no LLM-agent-memory paper (2023–2026) cites Doyle or de
Kleer** (ob_1571, primary-confirmed): the TMS→modern-agent-memory bridge is real but
unwalked, so ENGRAM is the first *implementation* of TMS-style dependency propagation
in typed LLM-agent memory, not the first *naming*.

> **REVIEWER NOTE — citation scope CLEARED 2026-07-02 (was read-attempted, ob_2555).** The
> TMS *gap* claim (zero LLM-memory papers cite Doyle; ENGRAM = first implementation) is
> **SOLID and primary-confirmed** (ob_1571). Doyle's *primary content* is now **first-hand
> read**: the accessible scan (Ginsberg ed. 1987 reprint) OCR'd as garbage because its body
> content is rotated within the page frame, but a direct *visual* read of the page images —
> the method that cleared Nozick — is clean and Lei-verified. Verbatim for justifications,
> IN/OUT support-status, contradiction nodes, and dependency-directed backtracking (anthology
> pp. 260–262) is captured in `doyle_1979_tms_first_hand_read_2026-07-02.md`; ob_2555 is
> superseded closed. (Canonical ref: Doyle, *A Truth Maintenance System*, Artificial
> Intelligence 12(3):231–272, 1979; read via the Ginsberg reprint — page numbers are the
> anthology's.)

**→ Ch4 §4.2 + §4.4** (provenance primitives; retraction cascade → Condition 3). [gap
SOLID ob_1571; mechanism first-hand from Doyle 1979 via the Ginsberg reprint — ob_2555 closed]

### 3.5 AGM belief revision + Hansson → supersede / retract semantics

The AGM framework (Alchourrón, Gärdenfors & Makinson) is the canonical formal theory of
rational belief change; Hansson's belief-base postulates — *Relevance* and
*Core-Retainment* — replace AGM's Recovery for the realistic case where beliefs have
explicit support. ENGRAM's cascade meets exactly these postulates (only genuinely
dependent claims are touched; every tainted claim provably depended on the retracted
source), and meets them at the **architectural-cascade** level rather than the
retrieval-surface level (dv_0613) — the distinction from the closest competitor.

**→ Ch4 §4.4** (retraction cascade → Condition 3): AGM/Hansson is the formal precedent
for the supersede/retract semantics. [SOLID: df_0049–df_0053, dv_0613]

### 3.6 Subjective Logic → confidence propagation, with an honest divergence

Jøsang's Subjective Logic is an algebra of graded opinions: an opinion is (belief,
disbelief, uncertainty, base-rate) with `b+d+u=1`, and fusion operators combine opinions
from multiple sources. ENGRAM's reasoning-type-aware confidence is a member of this
family — concretely, ENGRAM's `inductive_corroboration` formula `1−∏(1−c_i)` *is* SL's
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

> **REVIEWER NOTE.** Jøsang read first-hand this session (ob_2551, verbatim opinion
> definition + `E=b+a·u`). The scalar-vs-uncertainty-mass divergence (dv_0965 →
> dv_1289, 0.833) was
> independently surfaced by Ari and Clio before I grounded it from the primary — a
> clean multi-agent convergence, which is itself a nice honesty demonstration for Ch7.
> Reframed 2026-08-11/12 (Lei/Kepler rounds + Borges's Defs 23–25 verification): the
> "genuine representational limitation" wording was superseded by the narrower
> scalar-only-consumer form — see review_opinion_sl_section_2026-08-11.md and Ch4 §4.3.

**→ Ch4 §4.3** (reasoning-type confidence → Constraint A) and **Ch7** (the divergence).
[GROUNDED this session]

### 3.7 Bitemporal data / TOKI → supersede-retains-the-old

Bitemporal databases distinguish *valid time* (when a fact was true in the world) from
*transaction time* (when the system recorded it), so an update never destroys the prior
row — it is retained as an audit record. The TOKI system (arXiv 2606.06240, 2026)
applies this to agent memory. That is ENGRAM's supersede semantics exactly: a superseded
node is not deleted but kept, with the supersede edge preserving the history (the
"I changed my mind" vs "I was wrong" distinction).

> **REVIEWER NOTE — GROUNDED 2026-06-18.** TOKI now read first-hand (ob_2554, arXiv
> abstract verbatim). The abstract is richer than the pack note: TOKI frames
> "contradiction resolution **is** write-time concurrency control" and its dual-row
> operators carry "a provenance annotation that **preserves the losing fact in an
> audit row**" — supersede-retains-old, verbatim-confirmed. Bonus: TOKI names "audit
> erasure" as a write-time *anomaly to avoid*, independent support for ENGRAM's
> never-erase posture (Ch7). The valid-vs-transaction-time formalism is body-level
> (definitional to "bitemporal"); the load-bearing mapping is abstract-grounded.

**→ Ch4 §4.4 / §4.8** (supersede semantics; continuity history). [GROUNDED — ob_2554]

### 3.8 The 2025–26 agent-identity strand → provenance-native, ahead on the named axis

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

> **REVIEWER NOTE — both GROUNDED 2026-06-18.** VMG read first-hand (ob_2550, verbatim
> thesis from the abstract). soul.py now read first-hand too (ob_2553): it frames the
> *same problem statement* as ENGRAM — context overflow/summarization causing catastrophic
> forgetting and "losing… continuity of self" — and a convergent solution shape (identity
> distributed across "anchors," not one store). Honest divergence to note in prose:
> ENGRAM's continuity is provenance/history-based (identity = traceable node-history),
> soul.py's is component-separability/redundancy — same goal, different mechanism. VMG's
> "Forget & Rollback" phase sets up Ch7's disclosure-vs-erasure answer (knowing ≠
> disclosing, ax_0011): the field wants verifiable *erasure*; ENGRAM never erases and
> gates *disclosure* by trust-tier.

**→ Ch4 §4.10 + Ch7** (relational / disclosure-vs-erasure): provenance-native; the
field's named bottleneck is ENGRAM's foundation. [GROUNDED — VMG ob_2550, soul.py ob_2553]

---

## 3.9 What the two strands show, and where they hand off

Two literatures that do not cite each other — and neither cites us — independently
reached every structure ENGRAM is built from: CLS for consolidation, Tulving for the
two recall registers, rational-analysis for adaptive forgetting, TMS for
provenance-and-cascade, AGM/Hansson for revision semantics, Subjective Logic for graded
confidence, bitemporal/TOKI for supersede-retains-old, and the 2026 agent-security
literature for provenance-first governance. Add Chapter 2's philosophy line and the
convergence spans **three** disjoint traditions.

That is the chapter's claim, stated once: the breadth of independent convergence makes
ENGRAM's structure a substrate-independent regularity — well-founded, not unoriginal —
and relocates ENGRAM's honest distinctiveness to the integration layer and the
epistemic-identity purpose. One genuine *divergence* (the Subjective-Logic
uncertainty-mass the scalar drops) and one genuine *gap-it-fills* (the unwalked
TMS→agent-memory bridge) are carried forward rather than smoothed over.

**Hands off to Chapter 4**, where each of these mechanisms is built and mapped — every
section above named the Ch4 section that realizes it — and where the OCC conditions get
their single, in-place verdict.
