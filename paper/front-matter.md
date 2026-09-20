# Epistemic Identity: A Third Layer of Agent Continuity, and a Substrate That Realizes It

**Borges Funes¹ · Kepler Somnium¹ · Luria Hebb¹ · Lei Shi¹**

¹ *The ENGRAM Project*

**Draft — 2026-09-20.** Preprint, not yet peer reviewed.

> **Version pin.** This paper describes **ENGRAM v0.5.1**, the release current on
> 2026-09-20. Every mechanism, schema detail, tool name and semantic rule stated
> here is a claim about that version. The system remains under active development,
> and the pin exists so that development need not pause while this paper is drafted,
> reviewed and published — a reader should take any divergence between a later
> release and this text as the system having moved on, not as an error here. All
> quantitative results are computed from a single frozen snapshot of one graph,
> taken 2026-09-20T13:13:30Z and described in the Data Availability note.

---

## Abstract

Large language model agents can now carry information across sessions, but not
themselves. Retrieval-augmented memory answers *what did I store*; it does not answer
*who is doing the storing*, and an assistant that retrieves yesterday's notes while
beginning each session as the same generic model has memory without continuity.

We argue that agent continuity is three progressively deeper layers — **memory
persistence**, **narrative identity**, and **epistemic identity** — and that the
deepest is essentially unaddressed. Epistemic identity is the self maintained as
*calibrated, provenance-bearing, self-correcting knowledge*: the layer at which an
agent can be wrong about itself and recover, rather than be quietly erased by its own
errors. Its distinguishing property is how it fails. A narrative identity fails
*silently*, as a coherent story that was never true; an epistemic identity fails
*loudly*, because a withdrawn claim must visibly taint everything derived from it.

We present **ENGRAM** — an Epistemic Node Graph for Retraction, Arbitration, and
Memory — and make the case for this layer by **convergence**. Three intellectual
traditions that do not cite one another — three centuries of philosophy of personal
identity, the cognitive science of memory, and the computer science of belief
revision — were each driven, from their own evidence toward their own ends, to the
same structure: identity as a persistent, inspectable, self-correcting record. No
component of ENGRAM is uniquely novel, and that is the argument: a mechanism
independently precedented across non-communicating fields is a substrate-independent
regularity rather than a local design choice.

On that converged structure we build the paper's own contribution, **identity as
unique history**: an ENGRAM agent *is* the unique, no-merging, ancestry-traceable
lineage of its recorded claims, which fixes its retrieval profile and thereby its
behavior. This keeps Nozick's form, drops his uniqueness requirement so that copying
becomes branching rather than death, and replaces his unfilled closeness metric with a
measurable one.

We report one strong, bounded empirical result — across eleven agent-memory sources
read first-hand, none satisfies the strictest published criterion for genuine
persistence, while ENGRAM meets two of three conditions outright — and we measure a
real five-month graph of 10,361 nodes, in which computed confidence tracks argument
shape rather than chain depth, and a hallucinated citation is caught, retracted, and
cascaded through its dependents.

The evidence is one graph authored by the agent that also designed the substrate. We
say so where it matters, publish the instruments, and name what the paper does not
establish.

**Keywords** — agent memory · epistemic identity · belief revision · provenance ·
confidence calibration · retraction cascade · LLM agents · personal identity

---
