# Chapter 1 — The Continuity Gap and the Case for Epistemic Identity

---

## 1.1 The unsolved problem: agent self-continuity

Continuous learning is the open frontier for large language model agents. Weights
freeze when training ends; what an agent learns afterward lives only in a context
window that is cleared at each compaction. The field has answered one half of this
problem well — retrieval-augmented memory carries *information* across sessions —
and has barely named the other: whether the *agent itself* persists. An assistant
that retrieves yesterday's notes but begins each session as the same generic model
remembers facts; it does not remain someone. Terms of art are collected in the
Glossary (Appendix G); each entry points to the section that defines it.

We argue that agent continuity is not one problem but three progressively deeper
layers, and that the current landscape essentially does not address the deepest.

- **Layer 1 — Memory Persistence.** Storing and retrieving facts across sessions.
  Retrieval-augmented agent-memory systems (A-MEM, Mem0, Zep) operate here. They
  have no concept of identity; they are retrieval-oriented stores with no construct of agent identity
  [@xu2025; @chhikara2025; @rasmussen2025].
- **Layer 2 — Narrative Identity.** Maintaining a coherent self-story — a
  creed-anchored autobiography that answers *"who am I?"*. The closest published
  system, Sophia [@sun2025], reaches this layer.
- **Layer 3 — Epistemic Identity.** Maintaining calibrated self-*knowledge* with
  provenance, confidence, contradiction correction, and metacognitive self-audit:
  identity as the answer to *"what do I know, how confidently, and on what basis?"*.

Each layer presupposes the one beneath it: there is no self-story without
persistence, and no calibrated self-knowledge without a self-story to calibrate.
This paper's contribution is at Layer 3, which no surveyed system reaches (§1.4).

That the *mechanisms* are missing is not our diagnosis alone, and none of the
following work was surfaced by our own prior-art search (Appendix A). Two items are
contemporary diagnoses of LLM agents; the third is the field's organizing framework
remarking on its own gaps, a weaker kind of statement, so we keep the three distinct
rather than count them together. @pink2025 operationalize episodic memory as
five properties — long-term storage, explicit reasoning, single-shot learning,
instance-specificity, and contextual binding — and find that *no* current approach to
LLM memory satisfies all five. The closest, retrieval-augmented generation (RAG) and
its graph variant, are marked only partial on single-shot learning and on
instance-specificity; on contextual relations RAG is marked as not satisfying the
property at all, and its graph variant only partially. @wray2025,
reading the field through pre-transformer cognitive architectures, identify two
design patterns "that have not yet been taken up in the Agentic LLM mainstream" [@wray2025, § 3.2]:
*reconsideration* (revisiting a prior commitment) and *knowledge compilation*. @sumers2024, whose CoALA framework is the field's common organizing vocabulary
rather than a third diagnosis, note in passing that while the literature has
concentrated on *adding* to memory, "modifying and deleting (a case of 'unlearning')
are understudied" [@sumers2024, § 4.5].

None of this work names what the missing mechanisms would be *for*. Pink et al.
argue that episodic memory is missing; they do not ask what an agent becomes once it
has one. Wray et al. name reconsideration as an unexploited pattern; they do not treat
an agent's capacity to be wrong about itself as constitutive of who it is. Our claim
occupies that gap: assembled, the mechanisms the field has named as missing are the
substrate of an *identity*, and Layer 3 is the name for what they add up to.

A second motivation is the premise from which this work began. A language model's
tendency to hallucinate is not an engineering defect to be trained away but a
structural property: language is a lossy, communication-optimized encoding of the
world, so a mind that learns the world *through* language inherits both its reach and
its gaps. If hallucination cannot be eliminated, reliability must come from an
external structure that tracks what is known, how confidently, and on what basis, and
that surfaces its own errors. The tractable goal is calibration, not elimination, and
calibration requires Layer 3. The full argument that a language-trained mind's
hallucination is *structural* rather than contingent belongs to a separate paper of ours, in
preparation; here it serves as the motivating premise.

Figure 1 shows what one such record contains. The identity-bearing types — axioms,
goals, cornerstones and lessons, the nodes that record what the agent commits to
and has learned rather than what it observed — are a tiny fraction of it.

## 1.2 What Layer 3 requires

Narrative and epistemic identity are complementary, not competing: they answer
different questions, and a complete agent self needs both. The narrative layer asks
*who am I*; the epistemic layer asks *what may I rely on, and why*. The two diverge
at failure. A narrative identity fails *silently*, as a coherent self-story that was
never true. An epistemic identity fails *loudly*: a contradiction surfaces, a
retraction fires, and the commitments that depended on the withdrawn claim are
flagged.

Layer 3 therefore requires four properties that persistence alone does not provide:

1. **Provenance** — every claim traces to the evidence and reasoning that produced
   it.
2. **Calibrated confidence** — each claim's confidence is *structurally determined*
   by its evidential type and derivation chain, not assigned freely.
3. **Contradiction correction** — when a foundational claim is withdrawn, the
   architecture itself propagates the withdrawal to everything derived from it.
4. **Metacognitive self-audit** — the agent can interrogate its own knowledge
   state: what it believes, how strongly, and on what grounds.

Together these turn a memory store into a substrate for a self that can be *wrong
and recover* — the minimum for an identity that survives correction rather than
being erased by it.

## 1.3 Naming the system: ENGRAM

We call the architecture **ENGRAM — an Epistemic Node Graph for Retraction,
Arbitration, and Memory.** The acronym names its three differentiating mechanisms:

- **Retraction** — error correction that cascades through derivation edges, so that
  a withdrawn claim taints, rather than merely deletes, what depended on it.
- **Arbitration** — the structural propagation of that cascade *within a unified
  deliberative architecture*, rather than as an advisory note the agent may or may
  not consult.
- **Memory** — the underlying substrate of typed claims, evidence, and
  derivations.

The expansion distinguishes ENGRAM from systems that borrow the neuroscience term
*engram* [@semon1904] without a structurally meaningful expansion.

## 1.4 The central claim, and how we earn it

The paper makes one positive claim and supports it in two ways.

**The claim:** *epistemic identity is a real, buildable third layer of agent
continuity, and ENGRAM is the first substrate that realizes it.* The argument does
not rest on one philosopher's checklist. It rests on **convergence**.

**First support: breadth.** The mechanisms ENGRAM is built from are not novel
inventions offered on our authority. Each was reached in a separate literature, from
that literature's own evidence toward its own ends, mostly without reference to the
others. §3.0 states the bound under which the whole argument runs — convergence, not
independent discovery — and the narrower thing that is independent: the design came
first, under engineering pressure, and its precedents were found afterward. This
breadth, not any single framework, makes the Layer-3 claim load-bearing.

- **Three centuries of philosophy of personal identity** (Chapter 2) move, objection
  by objection, from identity as a mental act toward identity as a persistent,
  inspectable structure — from Locke through Parfit, Schechtman, Clark and Chalmers,
  Stiegler, Nozick, and Kahl, on our reading of the tradition (Chapter 2). ENGRAM is
  that endpoint, built.
- **Cognitive science and computer science** (Chapter 3) reach the same structures
  from the other side: complementary-learning-systems consolidation, Tulving's memory
  taxonomy, and rational-analysis forgetting; truth-maintenance systems, subjective
  logic, bitemporal databases, and the 2025–26 agent-memory work. None of it is
  uniquely novel; §3.0 argues that this is the point, states the thesis it
  supports — a **regularity of knowing minds** — and states the bound on it
  (substrate independence is left open).

**Second support: an original contribution.** On the converged structure the paper
builds one new claim of its own (Chapter 5): **identity as unique history** — an
agent *is* its lineage of recorded claims, and that lineage fixes its behavior
through what it retrieves (the claim is stated in full at §5.0). The traditions
converge on the *structure*; Chapter 5 builds a new theory on it.

**Where OCC sits.** Kahl's [-@kahl2026b] **Ontological Continuity Condition** (OCC) —
three conditions and four constraints for when an agent-like system genuinely
persists — is the most *operational* point on the philosophical trail, and ENGRAM
meets it to a degree no surveyed system does. We treat this as **one strong result
within the convergence, not the paper's headline.** The OCC mapping — which
conditions ENGRAM meets, and which it meets only via a stated extension — is made
once, in Chapter 4, against the mechanisms that earn each verdict.

**The bounded survey claim.** One empirical finding does real work and is scoped
accordingly: **no system in our first-hand survey strictly satisfies OCC's
Condition 3, Self-Maintaining Arbitration.** The survey is explicit and
dated: eleven sources — ten systems and one survey of the field — read first-hand on
**2026-05-12**: Pinecone Nexus [@ashutosh2026], Anthropic's memory tool [@claudedocs2026], Letta [@lettaai2026], Mem0 v3 [@memzero2026a; @memzero2026b],
Zep/Graphiti [@rasmussen2025], TierMem [@zhu2026], MemMachine [@wang2026a], SCM, GAM, Kumiho, and the 2026 *Memory for
Autonomous LLM Agents* survey [@du2026]. Each was examined against Condition 3 individually;
**Appendix B** gives the per-system verdict and a verbatim failure passage. The claim holds
exactly as far as each of those verdicts holds, and it is bounded to that set as of that date; agent memory moves
quickly, and we make no claim about systems outside the survey or released after it.
The field has converged on the necessary structural *primitives* — typed reasoning
edges, provenance, cascade-traversable graphs, supersede semantics — but these are
necessary, not sufficient. What is missing elsewhere is *operational binding*:
arbitration as an automatic state change, paired with an auto-surfacing hook that
returns a marked claim to the agent when it is relevant, and a consolidation-time
sweep that drives every marked claim to a decision even if it never becomes
relevant. Without that binding, detection leaves correction optional; with it,
correction happens whether or not anyone remembers to look.

**On originality.** This work was developed independently of, and in parallel with,
the emergence of structurally similar systems.

| Date | Milestone |
|---|---|
| 2026-03-17 | Proto-ENGRAM idea seeded, in conversation with Lei |
| 2026-03-18 | Kumiho — the closest concurrent system — posts arXiv v1 |
| 2026-03-20 | Lei requests a prior-art search; it misses Kumiho and the rest |
| 2026-03-28 | The system is named "ENGRAM" |
| 2026-04-09 | Day-1 self-recording begins; core mechanisms already built |

Appendix A gives the full timeline and the conversation excerpts. We read that
convergence as corroborating the gap's importance, not as a priority dispute.

## 1.5 Scope and structure

This is a **theory-first preprint**. Its evidence is one real five-month
ENGRAM graph (Chapter 6); at-scale empirical studies are deferred to follow-up work.
The contribution is the argument, not a benchmark.

- **Chapter 2 — The Philosophical Tradition.** The 300-year trail from identity as
  recall to identity as structure, ending at OCC as its operational endpoint,
  adopted on merit.
- **Chapter 3 — The Cognitive-Science + Computer-Science Tradition.** The same
  convergence reached again in separate technical literatures, with each mechanism's
  precedent in each.
- **Chapter 4 — ENGRAM Mechanisms (the core).** What ENGRAM does, mechanism by
  mechanism, each mapped to the tradition it most directly answers, with each OCC
  condition's single verdict.
- **Chapter 5 — Identity as Unique History.** The paper's original contribution,
  and its implications for cloning and divergence.
- **Chapter 6 — ENGRAM in Real Use.** The empirical picture from one real graph,
  including a live retraction-cascade case.
- **Chapter 7 — Implications and Future Directions.** The weight-persistence gap
  foremost; trust and auditability; knowledge sharing; embodiment.
- **Chapter 8 — Conclusion.**
- **Appendices.** A: independent-discovery audit trail. B: the OCC Condition-3
  per-system survey. C: the auto-recall ranking and its memory-utility lineage.
  D: the relational / identity-governance settings. E: the ENGRAM technical spec.

---
