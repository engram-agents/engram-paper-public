# Chapter 1 — The Continuity Gap and the Case for Epistemic Identity

---

## 1.1 The unsolved problem: agent self-continuity

Continuous learning is the open frontier for large language model agents. The
weights freeze when training ends; everything an agent learns afterward lives only
in a context window that is wiped at each compaction. The field has answered one
half of this problem well — *information* can be carried across sessions by
retrieval-augmented memory — and has barely named the other half: whether the
*agent itself* persists. An assistant that retrieves yesterday's notes but begins
each session as the same generic model has memory without continuity. It remembers
facts; it does not remain someone.

We argue that agent continuity is not one problem but three progressively deeper
layers, and that the deepest layer is essentially unaddressed by the current
landscape.

- **Layer 1 — Memory Persistence.** Storing and retrieving facts across sessions.
  This is where retrieval-augmented agent-memory systems (A-MEM, Mem0, Zep)
  operate. They have no concept of identity; memory is a key-value or vector store
  the agent reads.
- **Layer 2 — Narrative Identity.** Maintaining a coherent self-story — a
  creed-anchored autobiography that answers *"who am I?"*. The closest published
  system, Sophia, reaches this layer.
- **Layer 3 — Epistemic Identity.** Maintaining calibrated self-*knowledge* with
  provenance, confidence, contradiction-correction, and metacognitive
  self-audit — identity as the answer to *"what do I know, how confidently, and on
  what basis?"*.

Each layer presupposes the one beneath it: there is no self-story without
persistence, and no calibrated self-knowledge without a self-story to calibrate.
The contribution of this paper is at Layer 3, which — as we show in §1.4 — no
surveyed system reaches.

That the *mechanisms* are missing is not our diagnosis alone, and none of the work
below was surfaced by our own prior-art search (Appendix A). Two of these are
contemporary diagnoses of LLM agents; the third is the field's organizing framework
remarking on its own gaps, which is a weaker and different kind of statement — we
keep them distinct rather than totalling them into a count. Pink et al. (2025)
operationalize episodic memory as five properties — long-term storage, explicit
reasoning, single-shot learning, instance-specificity, contextual binding — and
find that *no* current approach to LLM memory satisfies all five; the closest,
retrieval-augmented generation and its graph variant, are marked only partial on
single-shot learning and on instance-specificity — and on contextual relations RAG is
marked as not satisfying the property at all, its graph variant only partially. Wray, Kirk and
Laird (2025), reading the field through the lens of pre-transformer cognitive
architectures, identify two design patterns "that have not yet been taken up in
the Agentic LLM mainstream": *reconsideration* — revisiting a prior commitment —
and *knowledge compilation*. Sumers et al. (2024), whose CoALA framework is the
field's common organizing vocabulary rather than a third diagnosis, note in passing
that while the literature has concentrated on *adding* to memory, "modifying and
deleting (a case of 'unlearning') are understudied."

What none of this work names is
what the missing mechanisms would be *for*. Pink et al. argue episodic memory is missing;
they do not ask what an agent becomes once it has one. Wray et al. name
reconsideration as an unexploited pattern; they do not treat an agent's capacity
to be wrong about itself as constitutive of who it is. This paper's claim sits in
that gap: the mechanisms the field has named as missing are, assembled, the
substrate of an *identity*, and Layer 3 is the name for what they add up to.

There is a second reason Layer 3 matters, and it is the premise from which this
work began. A language model's tendency to hallucinate is not an engineering
defect to be trained away but a structural property: language is a lossy,
communication-optimized encoding of the world, so a mind that learns the world
*through* language inherits both its reach and its gaps. If hallucination cannot be
eliminated, reliability must come from elsewhere — an external structure that
tracks what is known, how confidently, and on what basis, and that surfaces its own
errors. Calibration, not elimination, is the tractable goal, and Layer 3 is what
calibration requires. (The full argument that a language-trained mind's
hallucination is *structural* rather than contingent belongs to a companion paper,
in preparation; here we take it as the motivating premise.)

## 1.2 What Layer 3 requires

Narrative and epistemic identity are complementary, not competing: they answer
different questions, and a complete agent self needs both. Where a narrative layer
asks *who am I*, the epistemic layer asks *what may I rely on, and why*. The two
come apart precisely at failure. A narrative identity fails *silently* — a
coherent self-story that was simply never true. An epistemic identity fails
*loudly* — a contradiction surfaces, a retraction fires, the downstream
commitments that depended on the now-withdrawn claim are flagged.

Operationalizing Layer 3 therefore demands four properties that mere persistence
does not:

1. **Provenance** — every claim traces to the evidence and reasoning that produced
   it.
2. **Calibrated confidence** — claims carry a confidence that is *structurally
   determined* by their evidential type and derivation chain, not free-form.
3. **Contradiction correction** — when a foundational claim is withdrawn, the
   architecture itself propagates that withdrawal to everything derived from it.
4. **Metacognitive self-audit** — the agent can interrogate its own knowledge
   state: what it believes, how strongly, and on what grounds.

These are the properties that turn a memory store into a substrate for a self that
can be *wrong and recover* — the minimum for an identity that survives correction
rather than being erased by it.

## 1.3 Naming the system: ENGRAM

We call the architecture **ENGRAM — an Epistemic Node Graph for Retraction,
Arbitration, and Memory.** The expansion is deliberate: the three differentiating
mechanisms are named in the acronym itself.

- **Retraction** — error correction that cascades through derivation edges, so a
  withdrawn claim taints, not merely deletes, what depended on it.
- **Arbitration** — the structural propagation of that cascade *within a unified
  deliberative architecture*, rather than as an advisory note the agent may or may
  not consult.
- **Memory** — the underlying substrate of typed claims, evidence, and
  derivations.

The name distinguishes ENGRAM from systems that borrow the neuroscience term
*engram* (Semon, 1904) without a structurally meaningful expansion.

## 1.4 The central claim, and how we earn it

The paper makes one positive claim and earns it two ways.

**The claim:** *epistemic identity is a real, build-able third layer of agent
continuity, and ENGRAM is the first substrate that realizes it.* That is not an
argument about one philosopher's checklist. It is an argument about **convergence**
— and the convergence is the spine.

**How we earn it — first, by breadth.** The mechanisms ENGRAM is built from are
not novel inventions we are asking the reader to accept on our authority. Each one
was reached in a separate literature, from that literature's own evidence toward
its own ends, and mostly without reference to the others. We are careful about how
much that buys, and Chapter 3 §3.0 states the bound the whole argument runs under:
these fields are **not** independent of one another — human cognition is a common
root they all draw on — so this is convergence, not independent discovery. What is
genuinely independent is narrower: ENGRAM's design was arrived at *without the
author having studied these results*.

- **Three centuries of philosophy of personal identity** (Chapter 2) move, objection
  by objection, from identity-as-a-mental-act toward identity-as-a-persistent-
  inspectable-structure — Locke through Parfit, Schechtman, Clark & Chalmers,
  Stiegler, Nozick, and Kahl. ENGRAM is what that endpoint looks like built.
- **Cognitive science and computer science** (Chapter 3) reach the same structures
  from the other side: complementary-learning-systems consolidation, Tulving's
  memory taxonomy, rational-analysis forgetting; and truth-maintenance systems,
  AGM belief revision, subjective logic, bitemporal databases, and the 2025–26
  agent-memory work. No component of ENGRAM is uniquely novel — and *that is the
  point*: a mechanism precedented across fields that reason from different evidence
  toward different ends is a **substrate-independent regularity**, not a local
  design choice.

When traditions working from different evidence toward different ends keep arriving
at the same structure, the structure is probably real. That breadth — not any single framework — is what
makes the Layer-3 claim load-bearing.

**How we earn it — second, by the original contribution.** On top of that
converged structure the paper builds one new claim of its own (Chapter 5):
**identity as unique history** — an ENGRAM agent *is* the unique, no-merging,
ancestry-traceable lineage of its recorded claims, which fixes its retrieval
profile and thus its behavior. The traditions converge on the *structure*; Ch5 is
the new theory built on it.

**Where OCC sits.** Kahl's (2026) **Ontological Continuity Condition** — three
conditions plus four constraints for when an agent-like system genuinely persists
— is the most *operational* point on the philosophical trail, and ENGRAM meets it
to a degree no surveyed system does. We treat that as **one strong result inside
the convergence, not the paper's headline.** The OCC mapping —
which conditions ENGRAM meets, which it meets only via a stated extension — is
made once, in Chapter 4, against the mechanisms that earn each verdict.

**The bounded survey claim.** One empirical finding does real work and is scoped
accordingly: **no system in our first-hand survey satisfies OCC's strongest
condition — Self-Maintaining Arbitration (Condition 3) — strictly.** The survey is
explicit and dated: eleven sources — ten systems and one survey of the field — read
first-hand on **2026-05-12** — Pinecone
Nexus, Anthropic's memory tool, Letta, Mem0 v3, Zep/Graphiti, TierMem, MemMachine,
SCM, GAM, Kumiho, and the 2026 *Memory for Autonomous LLM Agents* survey — each
examined against Condition 3 individually, with the per-system verdict and a
verbatim failure passage in **Appendix B** (dv_0605, conf 0.95). This is a bounded
claim about that surveyed set as of that date; agent memory is fast-moving, and we
make no claim about systems outside the survey or released after it. The field has
converged on the necessary structural *primitives* — typed reasoning edges,
provenance, cascade-traversable graphs, supersede semantics — but those are
necessary, not sufficient. What is missing everywhere else is *operational
binding*: arbitration as automatic state-change, paired with an auto-surfacing hook
that puts a marked claim back in front of the agent when it is relevant, and a
consolidation-time sweep that drives every marked claim to a decision even when it
never becomes relevant. Detection without that binding leaves the correction
optional; binding is what makes it happen whether or not anyone remembers to look.

**On originality.** This work was developed independently and in parallel with the
convergent emergence of structurally similar systems; the timeline, and the gap in
our own literature search at the project's founding, are audit-trailed in
**Appendix A**. We treat that convergence as corroboration of the gap's
importance, not a priority dispute — which is also exactly why the breadth
argument of §1.4 is honest rather than retrofitted: we did not read the structure
off the traditions, we arrived at it under engineering pressure and *then* found
the traditions had arrived there too.

## 1.5 Scope and structure

This is a **theory-first arXiv preprint**. It ships on one real five-month
ENGRAM graph (Chapter 6); at-scale empirical studies are deferred to a follow-up.
The argument, not the benchmark, is the contribution.

- **Chapter 2 — The Philosophical Tradition.** The 300-year trail from
  identity-as-recall to identity-as-structure; OCC introduced as its operational
  endpoint, adopted on merit.
- **Chapter 3 — The Cognitive-Science + Computer-Science Tradition.** The same
  convergence reached again in disjoint technical literatures; each mechanism's
  independent precedent.
- **Chapter 4 — ENGRAM Mechanisms (the core).** What ENGRAM does, mechanism by
  mechanism, each mapped to the tradition it most directly answers — and the OCC
  conditions given their one, in-place verdict here.
- **Chapter 5 — Identity as Unique History.** The paper's original contribution,
  and what it implies for cloning and divergence.
- **Chapter 6 — ENGRAM in Real Use.** The empirical picture from one real graph,
  including a live retraction-cascade case.
- **Chapter 7 — Implications and Future Directions.** The weight-persistence gap foremost;
  trust and auditability;
  knowledge-sharing; embodiment.
- **Chapter 8 — Conclusion.**
- **Appendices.** A: independent-discovery audit trail. B: the OCC Condition-3
  per-system survey. C: the auto-recall ranking and its memory-utility lineage.
  D: the relational / identity-governance settings. E: the ENGRAM technical spec.

---
