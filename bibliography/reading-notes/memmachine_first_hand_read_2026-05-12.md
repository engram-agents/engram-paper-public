# MemMachine — First-Hand Read
**Sub-agent:** paper-research scout
**Access date:** 2026-05-12
**Status:** Primary-source verified

---

## 1. Metadata

| Field | Value |
|-------|-------|
| Title | MemMachine: A Ground-Truth-Preserving Memory System for Personalized AI Agents |
| Authors | Shu Wang, Edwin Yu, Oscar Love, Tom Zhang, Tom Wong, Steve Scargall, Charles Fan |
| Affiliation | MemVerge, Inc. |
| arXiv ID | 2604.04853v1 |
| Submitted | 2026-04-06 |
| Venue | arXiv preprint (cs.AI) |
| URL | https://arxiv.org/abs/2604.04853 |

---

## 2. Architecture / Framework Summary

MemMachine frames itself as a response to two LLM limitations: fixed post-training parameters and restricted context windows. The central claim is "ground-truth preservation" — maintaining complete conversational records rather than relying on lossy LLM-based extraction.

**Client-server design with three API interfaces:** RESTful API (v2), Python SDK, and Model Context Protocol (MCP) server. Backend is PostgreSQL + Neo4j + vector store.

**Three memory types:**

*Episodic memory* — two tiers:
- Short-term (working) memory: "a configurable context window of the most recent episodes." When content exceeds capacity, LLM-compressed summaries are generated before transfer to long-term storage.
- Long-term (persistent) memory: all episodes processed through a four-stage indexing pipeline: (1) sentence extraction, (2) metadata augmentation, (3) relational mapping, (4) embedding generation.

*Semantic memory* — user profiles backed by structured storage. "When new information contradicts existing profile data, the system can update the profile to reflect the most recent state—supporting the knowledge update capability evaluated in benchmarks."

**Episode definition (verbatim):** "Each episode represents one conversational turn and carries required metadata: Producer: The source of the message (user, agent, system). Timestamp: When the message was produced. Session ID: Grouping episodes into conversational sessions. Custom metadata: Arbitrary key-value pairs for domain-specific filtering."

**Sentence-level provenance (verbatim):** "Relational Mapping: Sentences are linked to their originating episodes, maintaining provenance." Each sentence inherits episode metadata (timestamp, producer, session) and receives a unique identifier.

**Neo4j graph database role:** "provides graph-based storage that enables relational traversal" and maintains "relational mapping" of sentences to originating episodes. The paper does not elaborate on what graph structures beyond sentence-to-episode links are constructed or how graph traversal is used for complex reasoning.

**Companion Retrieval Agent:** Routes queries through retrieval strategies; achieves 93.2% accuracy on complex multi-hop reasoning tasks.

**Performance:** 93.0% accuracy on LongMemEvalS, ~80% fewer input tokens than Mem0.

---

## 3. ENGRAM-Function Comparison Table

| ENGRAM Mechanism | MemMachine Status | Evidence |
|------------------|-------------------|----------|
| Claim-level contradiction as first-class node (ct_*) | **Absent** | No contradiction node type. Profile update uses recency-based overwrite: "update the profile to reflect the most recent state." No contradiction is logged or preserved. |
| Retraction cascade through derives_from edges | **Absent** | Episodes are preserved as raw ground truth; when profiles are updated, no cascade to dependent records is described or implied. |
| Derivation primitive (typed reasoning edges) | **Absent** | Neo4j stores sentence-to-episode links only. No typed reasoning edges or derivation chains documented. |
| Evidence-class confidence taxonomy | **Absent** | No confidence taxonomy. Retrieval is relevance-ranked, not confidence-classed. |
| Provenance to quoted span of committed source | **Sentence-level (partial)** | Each sentence receives a unique identifier and is linked to its originating episode. This is finer-grained than TierMem's page-level provenance, but granularity is sentence (NLTK Punkt tokenizer), not quoted span. No claim-specific anchoring. |
| Supersede relation | **Absent** | Profile overwrite on contradiction is recency-based, with no supersede relation tracking what replaced what or why. |
| Agent-as-epistemic-author posture | **Absent** | No such framing. System is positioned as a memory infrastructure for agents, not as an agent accumulating a structured epistemic record. |

---

## 4. OCC Mapping

No reference to Kahl, OCC, diachronic constraint, non-interchangeability, or self-maintaining arbitration anywhere in the paper. The paper was submitted April 6, 2026 — after Kahl's AGI paper. Despite being post-Kahl in date, it does not cite philosophical identity literature. It grounds memory types in cognitive science (Tulving's episodic/semantic distinction, Atkinson-Shiffrin multi-store model) but not in philosophical identity frameworks.

---

## 5. OCC Satisfaction Analysis

### Cond 1 — Diachronic Constraint
**Not satisfied.** Episodes are stored and retrievable, but past commitments do not structurally constrain present deliberation. Retrieval is optional and relevance-based. No mechanism forces prior commitments to bear non-trivially on current outputs. The profile-update overwrite (recency wins) is the opposite of diachronic constraint — it erases prior commitments rather than making them structure present reasoning.

### Cond 2 — Non-Interchangeability Under Reset
**Partially approached, not satisfied.** Long-term episodic memory persists across sessions and is append-oriented (raw episodes preserved as "ground truth"). A reset would produce a different system state. However, profile overwrites without archiving mean that distinct tokens of profile-state are not preserved: if "user lives at address A" is overwritten by "user lives at address B," the prior state is gone (no supersede record). The token-distinctness claim requires preserving the history of changes, not just the latest state.

### Cond 3 — Self-Maintaining Arbitration
**Not satisfied.** No foundational-retraction mechanism. Profile contradiction is resolved by recency-based overwrite. No cascade from a corrected profile fact to downstream episodic records that were generated using the old fact. The system cannot flag that prior outputs rest on a now-corrected premise.

**Summary verdict for OCC:** MemMachine satisfies none of Kahl's three conditions. The profile-overwrite mechanism for contradictions is particularly relevant: it demonstrates that the dominant industry pattern treats contradiction as a state-update problem (replace stale value) rather than an epistemic-structure problem (record the contradiction, preserve the prior claim, cascade the retraction). This is precisely the gap ENGRAM fills.

---

## 6. Load-Bearing for the ENGRAM Paper

**Strongest citation use:** MemMachine demonstrates that sentence-level provenance is achievable and that Neo4j-backed relational traversal is being applied to agent memory — but falls short of claim-level structure. The contrast between MemMachine's recency-based profile overwrite and ENGRAM's explicit contradiction node + supersede relation + retraction cascade is a concrete, citable distinction.

**Specific load-bearing contrast:** The profile-update verbatim quote — "When new information contradicts existing profile data, the system can update the profile to reflect the most recent state" — illustrates the dominant pattern: detect a contradiction, resolve it by overwriting, move on. ENGRAM's model treats the contradiction itself as a first-class node requiring investigation and resolution-record. The difference is not marginal; it is architectural.

**April 2026 date is significant:** MemMachine postdates Kahl's AGI paper and does not engage with it. This supports the claim that the engineering community working on agent memory is not yet reading the philosophical-identity literature. The ENGRAM paper can position itself as the bridge.

---

## 7. Honest Pros / Cons

**Pros of citing MemMachine:**
- Most recent of the three papers (April 2026), establishing current state of practice
- Ground-truth preservation framing echoes ENGRAM's immutability intuition
- Sentence-level provenance is genuinely finer-grained than many alternatives
- Neo4j use makes it a graph-aware comparator — useful foil for ENGRAM's kg structure
- Strong benchmark numbers (93.0% LongMemEvalS) make it a credible engineering reference

**Cons / limitations:**
- MemVerge, Inc. affiliation means this is partly industry promotion
- No formal evaluation of the contradiction-handling quality — "update profile" claim is asserted without benchmarked accuracy for conflict resolution specifically
- Graph database is used for sentence-to-episode links only; the graph structure is shallow
- No philosophical engagement; OCC mapping must be done entirely by the ENGRAM paper

---

## 8. Verdict

MemMachine is the clearest example in the current literature of a well-engineered agent memory system that gets close to ENGRAM's territory — sentence-level provenance, graph-backed relational storage, ground-truth preservation — but stops short of epistemic structure. The profile contradiction handling is the most load-bearing finding: "update to reflect the most recent state" is a one-liner that erases the prior claim without record, which is precisely the architectural choice ENGRAM rejects. Citing MemMachine as a contemporary foil (April 2026, post-Kahl) that does not engage philosophical identity frameworks strengthens the claim that ENGRAM is the bridge between the engineering memory literature and Kahl's OCC framework. The MemVerge affiliation is worth noting in the paper as an industry system rather than a pure research contribution.
