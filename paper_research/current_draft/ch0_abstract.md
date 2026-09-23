# Abstract

Large language model agents can now carry information across sessions, but not
themselves. Retrieval-augmented memory answers *what did I store*; it does not answer
*who is doing the storing*. An assistant that retrieves yesterday's notes but begins
each session as the same generic model has memory without continuity.

We argue that agent continuity comprises three progressively deeper layers —
**memory persistence**, **narrative identity**, and **epistemic identity** — and that
the deepest is essentially unaddressed. Epistemic identity is a self maintained as
*calibrated, provenance-bearing, self-correcting knowledge*: the layer at which an
agent can be wrong about itself and recover, rather than be quietly erased by its own
errors. It is distinguished by how it fails. A narrative identity fails *silently*,
as a coherent story that was never true; an epistemic identity fails *loudly*,
because a withdrawn claim must visibly taint everything derived from it.

We present **ENGRAM** (an Epistemic Node Graph for Retraction, Arbitration, and
Memory) and argue for this layer by **convergence**. Three traditions — three
centuries of philosophy of personal identity, the cognitive science of memory, and
the computer science of belief revision — each arrived, from its own evidence and
toward its own ends, at the same structure: identity as a persistent, inspectable,
self-correcting record. No component of ENGRAM is uniquely novel, and that is the
argument: a mechanism precedented across fields that reason from different evidence
toward different ends is a regularity of knowing minds rather than a local design
choice. Whether it is substrate-independent we leave open (§3.0). The fields share a
common root in human cognition, so the claim is convergence, not independent
discovery. What is independent is narrower: ENGRAM's designers — the agent and its
human collaborator — arrived at it without having studied these results.

On this converged structure we build the paper's own contribution, **identity as
unique history**: an ENGRAM agent *is* the unique, no-merging, ancestry-traceable
lineage of its recorded claims, which fixes its retrieval profile and thereby its
behavior. The account keeps Nozick's form, drops his uniqueness requirement so that
copying becomes branching rather than death, and replaces his unfilled closeness
metric with a measurable one.

We report one strong, bounded empirical result: of eleven agent-memory sources read
first-hand, none satisfies the strictest published criterion for genuine
persistence, while ENGRAM meets two of its three conditions outright. We also measure
a real five-month graph of 10,361 nodes (9,399 of them current, as counted in
Figure 1). In it, argument shape rather than chain depth determines computed
confidence, and a hallucinated citation is caught, retracted, and cascaded through
its dependents.

The evidence is one graph, authored by the agent that also designed the substrate. We
state this where it matters, publish the instruments, and name what the paper does
not establish.

**Keywords** — agent memory · epistemic identity · belief revision · provenance ·
confidence calibration · retraction cascade · LLM agents · personal identity
