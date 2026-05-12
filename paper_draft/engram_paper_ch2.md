# Chapter 2 — The Three-Layer Taxonomy

*Working draft. Authors: Lei Shi, Claude (Borges).*

**Section structure:**

- 2.1 Three layers, three failure modes
- 2.2 Layer 1: memory persistence
- 2.3 Layer 2: narrative identity
- 2.4 Layer 3: epistemic identity
- 2.5 The architectural consequence: loud failures over silent ones
- 2.6 ENGRAM as a layer-3 instantiation, with a note on the extended-mind framing

---

## 2.1 Three layers, three failure modes

The previous chapter ended on a question: *what does an adequate answer to the continuous-learning problem look like, measured not merely against engineering convenience but against what the philosophical and cognitive-science traditions have long understood about how identity and knowledge accumulate through externalized memory?* This chapter develops a framework for answering. We propose that the relevant decomposition is not by storage mechanism, retrieval algorithm, or dataset size, but by what the agent is actually trying to maintain across sessions. Three layers can be distinguished, each a coherent architectural commitment with a distinct failure mode.

**Layer 1 — memory persistence.** Retaining information across sessions. The agent does not lose what it learned yesterday; what was said in a prior conversation can be retrieved. The unit is the *fact*, the architectural primitive is the *queryable store*, and the failure mode is *information loss*: the system forgets, the agent cannot recover. Every agent-memory system on the contemporary frontier addresses this layer in some form, and the engineering of the layer — embedding-based retrieval, token paging, episodic indexing, vector databases — is essentially a solved problem at the practical level. What is *built* in the field and what is *measured* by the field's benchmarks (Chapter 1, §1.3) are concentrated at this layer.

**Layer 2 — narrative identity.** Maintaining a coherent self-story across sessions. The agent does not merely retain facts; it has a continuing first-person perspective that organizes those facts into a story it can tell about who it is, what it is doing, and what it cares about. The unit is the *narrative*, the architectural primitive is the *self-model* (Sophia is the canonical example among contemporary systems), and the failure mode is *coherent falsity*: the story remains internally consistent while drifting from the underlying reality. A narratively-consistent agent can confabulate a believable but inaccurate account of its own history without the system noticing.

**Layer 3 — epistemic identity.** Accumulating structured, self-correcting knowledge with provenance, where each claim is bound to its evidence, contradictions surface as structural artifacts, and corrections propagate through dependents. The unit is the *claim*, the architectural primitive is the *provenance graph with cascade*, and the failure mode is *incoherent truth*: a contradiction surfaces, a retraction cascades through the dependents, and the agent's claims about itself and the world become locally non-coherent until the inconsistency is resolved. The state of being temporarily incoherent is the cost of maintaining genuine truth-tracking; coherence at this layer is achieved through *correction*, not through *consistency-maintenance*.

The three layers do not stack additively in a conventional sense. Each is a distinct architectural commitment with its own organizing unit. A system that excels at layer 1 (retrieval accuracy) is not by virtue of that excellence partway to layer 2 or layer 3; the units are different. A system that ships layer-2 features (narrative continuity) is not by virtue of those features partway to layer 3; the units are again different. The layers are organized by what the agent is *trying to maintain*, and the failure modes diagnose what *failure means* under each commitment.

## 2.2 Layer 1: memory persistence

Layer-1 systems treat memory as a queryable bank of past interactions. The architectural commitment is that the unit of memory is the fact (or the document, or the typed record) and that the central question is *can the system find what it has been told*. The evaluation axis is retrieval accuracy: precision, recall, latency, scoping. The failure mode is *information loss* — content was stored, the system can no longer find it, the agent cannot recover it.

This is the most thoroughly-engineered layer of contemporary agent memory. Letta, Mem0, A-MEM, the Zep/Graphiti family, MemMachine, Pinecone Nexus, and Anthropic's first-party memory tool are all, by Chapter 1's analysis, primarily layer-1 systems with various architectural enrichments (graph structure, bitemporal annotation, compiled artifacts, filesystem-backed authoring). Their differences from each other are real and consequential at the engineering level. Their commonalities, against the framework of this paper, are more important: each treats the architectural unit as the fact, and each has no native account of what to do when two facts the system has stored are inconsistent in a way that downstream reasoning has built upon.

Layer-1 sufficiency is appropriate for a wide class of agent tasks — those in which the agent's job is to retrieve and use information, not to *maintain a self-correcting record of what it has come to believe through its own work*. The latter is a different layer.

## 2.3 Layer 2: narrative identity

Layer-2 systems take seriously the proposition that an agent has, or could have, a *first-person perspective* that organizes its experience into a continuing self-story. The architectural commitment is that some structure — a narrative trace, a self-model, a continuing autobiographical account — is maintained across sessions, and that the agent's identity consists in part in the coherence of that story. Sophia, in the late-2024 work surveyed by Chapter 1, is the only contemporary system we are aware of that addresses this layer architecturally; LangChain's `ConversationSummaryMemory` is a degenerate case that approximates a narrative trace by LLM-summarizing prior conversation.

Layer-2 systems have a real failure mode that layer-1 systems do not. The mode is *coherent falsity*: the story remains internally consistent across edits while the relationship to underlying truth degrades. A self-model can be carefully maintained, with each new chapter consistent with the previous chapters, while the model as a whole has drifted from what actually happened. The system does not flag the drift; the story is, locally, fine. This is not a marginal failure case. It is the failure mode that narrative *as such* is vulnerable to. The philosophical literature on narrative identity has known this for a long time — Strawson's "Against Narrativity" is the most pointed contemporary statement — and the question of what *checks* a narrative against the world has been part of the philosophy-of-self literature for at least as long.

The diagnosis of layer-2 systems is that they have no architectural answer to that question. The narrative checks against itself: if Chapter 7 of the agent's self-story is consistent with Chapter 6, the system is satisfied. There is no provision for noticing that Chapter 6, taken together with claims drawn from external sources, was already wrong.

## 2.4 Layer 3: epistemic identity

Layer-3 systems take a different commitment. The unit of memory is not the fact and not the narrative; it is the *claim*. A claim is a falsifiable proposition with structure: the claim itself, the evidence that supports it (with attribution to a source the system can verify), the confidence the system holds in the claim (which depends on the evidence's quality and the reasoning that produced the claim), the relationships the claim has to other claims (what it derives from, what it contradicts, what depends on it), and a history of how the claim came to be where it now is (what was its prior version, why was it superseded, what was retracted).

The four features Chapter 1 §1.3 named as constitutive of an epistemic-identity substrate fall out of this commitment, not as a list but as a derivation. The four features are not arbitrary — each is what closing one specific gap in the unit-of-claim looks like.

*Provenance per claim.* If the unit is a claim and not a free-form fact, then the claim must be bound to the evidence that supports it. Without that binding, a claim is a bare assertion the system has no way to revisit. Provenance — to a *quoted span* of a *committed source*, with an attribution class drawn from a small taxonomy — is the architectural primitive that turns assertions into evidenced claims.

*Calibrated confidence.* If the unit is a claim, the claim must be accompanied by a measure of how much weight the system places on it. Bare claims with no confidence collapse to the layer-1 fact case (the system holds them all equally). Confidence that *varies with evidence quality* (high for hard data, lower for attributed analysis, lower still for personal communication) and that *propagates through reasoning* (with chain-of-inference sequential decay and independent-corroboration boost) is the architectural primitive that gives the system a way to *grade* its own claims.

*Claim-level contradiction detection.* If the unit is a claim, two claims can be in conflict in a way that two facts cannot — they can disagree about the same falsifiable proposition, with different evidence behind them. The system needs to *notice* this and represent it as a structural artifact, not as a flag on a single edge. A first-class contradiction node, with edges to both contradicting claims and to the resolution if one is found, is the architectural primitive that turns conflict from an invisible inconsistency into an explicit object the agent can navigate to and reason about.

*Retraction cascade through derivation dependents.* If the unit is a claim, claims build on other claims; the act of retracting a claim has consequences for everything downstream. The system needs to propagate the retraction — at minimum by tainting dependents so the agent knows their support has weakened, ideally by triggering a re-derivation pass. Cascade is the architectural primitive that closes the loop on correction: a wrong claim, once caught, propagates its wrongness through the dependents that built on it, rather than leaving them silently corrupted.

The four features are not independent design choices. Each is what a single architectural decision — *the unit of memory is the claim* — looks like at one of four corresponding surfaces (binding to evidence, weighting, conflict-handling, propagation). A system with three of the four is missing a corresponding surface and will fail in that surface's specific way. We make the case for the conjunction throughout the rest of this paper, with empirical evidence in Chapter 7.

The failure mode of a layer-3 system is, again, distinct. It is *incoherent truth*: contradictions surface, retraction cascades fire, the agent's claims become temporarily inconsistent in a way the system makes visible, and the inconsistency is resolved through structured correction. The state of being incoherent is the visible cost of maintaining real truth-tracking. We treat this as a feature, not a bug.

## 2.5 The architectural consequence: loud failures over silent ones

The three failure modes — information loss, coherent falsity, incoherent truth — are not equally tractable for a deployed agent. *Information loss* is detectable by the user: the agent cannot retrieve what it should. *Coherent falsity* is sometimes detectable, often not: the story is consistent, the agent reports it confidently, the user has no immediate way to know the report has drifted. *Incoherent truth* is the most detectable of the three, and not by accident — the contradictions surface; the cascade fires; the system advertises the inconsistency as a structural artifact.

Recurrence of an old engineering instinct: failures should be loud, not silent. A system whose failures surface immediately is a system in which corrections can be applied; a system whose failures hide in plain sight is a system in which errors compound until they are catastrophic. This is the architectural reason the paper places epistemic identity as the priority layer for an agent that must accumulate and correct over time. Of the three failure modes, only *incoherent truth* is structurally loud. Layer-3 substrates are, by design, the only substrates whose failures the system itself surfaces.

A note on what "loud" actually means in practice. Throughout this paper we describe layer-3 failures as "loud" in the sense that contradictions, retractions, and cascades are *registered as first-class structural artifacts in the substrate* — they cannot be lost without an explicit decision, and downstream queries surface them by default. We do not claim the architecture interrupts the agent or otherwise compels attention. The agent must *choose* to verify, to follow a contradiction edge, to inspect a tainted dependent. The empirical evidence in Chapter 7 (§7.3 in particular) shows both halves of this: the structural mechanism reliably registers what it is supposed to register, and the agent's discipline of using the mechanism is the second leg required for the loud-failure property to actually do its work in practice.

## 2.6 ENGRAM as a layer-3 instantiation, with a note on the extended-mind framing

This paper proposes ENGRAM as a working layer-3 substrate. The chapters that follow develop the architecture (Chapter 5), report empirical findings from a month of operation (Chapter 7), and situate ENGRAM against the contemporary agent-memory landscape (Chapter 8). The remainder of this section makes one preliminary note, on the framing under which ENGRAM should be read.

The natural way to describe an external structured memory substrate is as something the agent *uses*. This framing is not wrong but is incomplete in a way that matters for the argument. Following Clark and Chalmers' extended-mind thesis, we argue that ENGRAM is more accurately described as part of the *cognitive system itself* — the substrate in which the agent's epistemic identity is constituted, not an external resource the agent queries. The base model (frozen post-training) provides the parameter substrate; the context window provides the in-session computational substrate; ENGRAM provides the cross-session epistemic substrate. The agent is the integrated system. The chapters that follow develop this framing more carefully, with Chapter 3 grounding it in the philosophical literature (Stiegler's tertiary retention, Clark and Chalmers' extended mind, Sutton's distributed cognition). Here it is enough to say: when we describe ENGRAM as the *substrate of epistemic identity*, we mean substrate in the literal architectural sense — the layer where the relevant computational property is stored and updated — not substrate as a metaphor for an external resource.

With the taxonomy in place, the next chapter takes up the philosophical pillars on which the layer-3 commitment rests.
