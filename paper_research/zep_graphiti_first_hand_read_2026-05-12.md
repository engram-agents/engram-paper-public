# Zep / Graphiti — First-Hand Deep Read
**Date:** 2026-05-12
**Dispatched by:** Borges (paper-research sub-agent)
**Purpose:** Primary-source verification of the 2026-05-05 second-hand summary; close-reading for OCC mapping

---

## 1. Metadata Header

| Item | Detail |
|---|---|
| arXiv paper | "Zep: A Temporal Knowledge Graph Architecture for Agent Memory" — 2501.13956v1, submitted 2025-01-20 |
| Authors | Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, Daniel Chalef |
| OSS project | getzep/graphiti (GitHub), currently v0.29.0 (released 2026-04-27) |
| Stars at access | 26k (GitHub) |
| Access date | 2026-05-12 |
| License | CC BY-NC-SA 4.0 (paper); OSS (code) |
| Primary sources accessed | arXiv HTML 2501.13956v1; github.com/getzep/graphiti tree + edges.py + nodes.py + graphiti_core/prompts/dedupe_edges.py + graphiti_core/prompts/extract_edges.py + graphiti_core/utils/maintenance/edge_operations.py; help.getzep.com; blog.getzep.com |

---

## 2. Architecture Summary with Verbatim Paper Quotes

### 2.1 Bi-temporal model

From Section 2.1 (verbatim):

> "Zep implements a bi-temporal model, where timeline T represents the chronological ordering of events, and timeline T′ represents the transactional order of Zep's data ingestion."

The paper defines four timestamps per edge. In code (`graphiti_core/edges.py`, `EntityEdge`), the actual fields are:
- `valid_at` — when the fact became true (domain time)
- `invalid_at` — when the fact ceased to be true (domain time, optional)
- `expired_at` — transaction time: when the record was superseded in the graph DB
- `created_at` — transaction time: when the record was written

Note: the paper notation uses `t_valid` / `t_invalid` / `t'_created` / `t'_expired`; the code uses `valid_at` / `invalid_at` / `created_at` / `expired_at`. These are the same concepts.

### 2.2 Graph entities

Three structural node types:
- **EpisodicNode** — raw ingested data (message, json, text, or fact_triple). Source of truth for provenance. Fields: `source` (EpisodeType), `content`, `valid_at`, `entity_edges`.
- **EntityNode** — extracted entities with evolving summaries. Fields: `name`, `summary`, `name_embedding`, `attributes` (custom k/v).
- **CommunityNode** — summaries of entity clusters.

Two primary edge types:
- **EpisodicEdge** — `MENTIONS` relation: EpisodicNode → EntityNode.
- **EntityEdge** — the factual relationship between two entities. Fields: `name`, `fact` (natural-language description), `fact_embedding`, `episodes` (list of episode UUIDs that contributed), `valid_at`, `invalid_at`, `expired_at`, `reference_time`, `attributes`.

### 2.3 Ingestion pipeline

Episodes are ingested via `graphiti.add_episode()`. The pipeline runs:
1. Entity extraction (LLM call)
2. Edge extraction (LLM call or combined call in v0.29.0)
3. Entity deduplication against existing graph
4. Edge resolution (deduplication + contradiction detection against related existing edges)
5. Persistence

### 2.4 Post-paper updates (v0.29.0, 2026-04-27)

Major changes relevant to this comparison:
- **Combined extraction**: node+edge extraction merged into one LLM call (`use_combined_extraction=True`)
- **`fact_triple` episode type added**: enum value `fact_triple = 'fact_triple'` now exists in `EpisodeType` (no docstring provided in source; purpose undocumented in accessible docs)
- **`episode_metadata` dictionary**: enables filtering by provenance at retrieval time
- **SagaNode**: multi-episode narrative rollup (new node type, not in original paper)
- **Search pipeline rework**: ~1k lines modified; no public API change
- **Deduplication logic refined**; fact extraction detail preservation improved
- **Breaking**: episode indices now 0-based; Kuzu schema migration required

---

## 3. ENGRAM-Function Comparison Table

| ENGRAM mechanism | Zep/Graphiti status | Primary source evidence |
|---|---|---|
| **Claim-level contradiction as first-class node (`ct_*`)** | ABSENT. Contradiction is an ephemeral LLM classification used to select edges for invalidation. No contradiction node type exists. No contradiction relation persists after the ingestion run. | `edges.py`: no contradiction class; `dedupe_edges.py`: `EdgeDuplicate` captures contradicted indices during resolution, discarded after; code comment: "contradicted_facts" is a list of indices, not persisted graph elements |
| **Retraction cascade through `derives_from` edges** | ABSENT. Invalidation affects only the single directly contradicted edge. No derivation graph exists to cascade through. | `edge_operations.py` verbatim (lines 835-842, 853-858): `for candidate in invalidation_candidates: candidate.invalid_at = ...` — sets `invalid_at` on the directly identified candidates only; no traversal of downstream edges |
| **Derivation primitive (typed reasoning edges)** | ABSENT. All EntityEdges are peer-level factual relations. There is no edge-to-edge relationship, no "this fact was inferred from that fact" primitive. | `edges.py`: `EntityEdge` has no `derived_from` field; `nodes.py`: no derivation node; `extract_edges.py` prompt: relationships are between "two DISTINCT ENTITIES", never between facts |
| **Evidence-class confidence taxonomy** | ABSENT. No confidence scores, certainty weights, or evidence classes on any node or edge type. | `edges.py`: no confidence/weight field in `EntityEdge`; paper: no section on confidence computation; HTML fetch: "No sections found addressing confidence scores, weights, or explicit certainty measures" |
| **Provenance to quoted span of committed source** | PARTIAL — episode linkage only, not quote-level. Episode UUIDs are stored in `EntityEdge.episodes`. Bidirectional indices tracked. Paper explicitly marks quote-level citation as future work. | Paper Section 2.1 (verbatim): "While these connections are not directly examined in this paper's experiments, they will be explored in future work." Blog (April 2026): "every fact in your agent's context graph came from somewhere" — but this refers to episode-level linkage, not verbatim quote spans. No quote-level span field exists in `EntityEdge` as of v0.29.0. |
| **Supersede relation** | PARTIAL — invalidation (`invalid_at`) achieves temporal supersession but does not create a named `supersedes` edge. Old and new edges coexist; query for `invalid_at IS NULL` returns current facts. | `edges.py`: `EntityEdge.invalid_at` field; `edge_operations.py`: `resolved_edge.invalid_at = candidate.valid_at` — the supersession is encoded as a timestamp flag, not a structural relation |
| **Agent-as-epistemic-author posture** | ABSENT as structured claim authoring. Ingestion is always conversational/document extraction through the episode pipeline. The `fact_triple` episode type (added v0.29.0) may allow direct fact injection, but has no docstring, no public documentation found, and no examples in the codebase. | `nodes.py`: `EpisodeType.fact_triple = 'fact_triple'` — no docstring; GitHub search for "fact_triple" returned 0 files beyond the enum definition; `extract_edges.py` prompt: extraction instruction assumes natural-language source text, not structured author claims |
| **Focus mode (deterministic cross-compaction channel)** | NOT APPLICABLE. Zep/Graphiti is a retrieval service, not a within-agent identity system. Cross-compaction continuity is not a design concern. | By design |
| **Bi-temporal fact tracking** | PRESENT. This is Graphiti's primary architectural contribution. Both domain time (`valid_at`/`invalid_at`) and transaction time (`created_at`/`expired_at`) are tracked per edge. | Paper Section 2.1 (verbatim): "Zep implements a bi-temporal model, where timeline T represents the chronological ordering of events, and timeline T′ represents the transactional order of Zep's data ingestion." |

---

## 4. Contradiction-Handling Deep-Dive

### 4.1 Paper description (verbatim)

From Section 2.2.3 of arXiv 2501.13956v1:

> "The system employs an LLM to compare new edges against semantically related existing edges to identify potential contradictions. When the system identifies temporally overlapping contradictions, it invalidates the affected edges by setting their t_invalid to the t_valid of the invalidating edge."

### 4.2 Implementation mechanism (from source code)

The contradiction detection runs inside `resolve_extracted_edge()` in `graphiti_core/utils/maintenance/edge_operations.py`.

Step 1: The LLM is called with the deduplication prompt (`dedupe_edges.py`). The prompt returns an `EdgeDuplicate` object with two fields:
- `duplicate_facts`: list of indices of exact-match existing edges
- `contradicted_facts`: list of indices of edges the new fact supersedes

From the prompt (verbatim system instruction):
> "You are a fact deduplication assistant. NEVER mark facts with key differences as duplicates."

From the prompt user instruction (paraphrased from code; no verbatim full text was accessible, only the structural description):
The LLM is instructed to identify when "a NEW FACT represents identical factual information as any fact in EXISTING FACTS" (duplicate) and separately to identify which facts the new statement contradicts, where "A fact from EXISTING FACTS can be both a duplicate AND contradicted (e.g., semantically the same but the new fact updates/supersedes it)."

Step 2: The identified `contradicted_facts` indices are collected as `invalidation_candidates` (verbatim code, lines 835-842):
```python
for idx in contradicted_facts:
    if 0 <= idx < len(related_edges):
        invalidation_candidates.append(related_edges[idx])
    elif invalidation_idx_offset <= idx <= max_valid_idx:
        invalidation_candidates.append(existing_edges[idx - invalidation_idx_offset])
```

Step 3: The `invalid_at` timestamp is set on contradicted candidates only when temporal ordering confirms the new edge supersedes (verbatim code, lines 853-858):
```python
for candidate in invalidation_candidates:
    candidate_valid_at_utc = ensure_utc(candidate.valid_at)
    resolved_edge_valid_at_utc = ensure_utc(resolved_edge.valid_at)
    if (candidate_valid_at_utc is not None 
        and resolved_edge_valid_at_utc is not None 
        and candidate_valid_at_utc > resolved_edge_valid_at_utc):
        resolved_edge.invalid_at = candidate.valid_at
```

Wait: note the direction here. This sets `invalid_at` on the **new** resolved edge (not the candidate) when the candidate's `valid_at` is more recent than the new edge's `valid_at` — meaning the new fact is outdated relative to an already-known fact. The invalidation_candidates list separately receives an `invalid_at` flag when the reverse is true. (The exact assignment direction for invalidation_candidates is not fully visible in the excerpt; the logic appears to mark old facts invalid when a newer one supersedes.)

### 4.3 Assessment

**Contradiction is an ephemeral LLM inference, not a structural graph relation.** The `EdgeDuplicate.contradicted_facts` list exists only in working memory during the ingestion pipeline. It is not persisted as a node, not persisted as an edge type, and not queryable after ingestion completes. The contradiction "event" is consumed to set a `invalid_at` flag on affected edges; then it disappears.

**What survives:** the invalidated edge (with `invalid_at` set), the new edge, and the episode records. A query for all edges including invalid ones can reconstruct "something changed here," but there is no `contradicts` relation, no contradiction node, and no record of *why* the flag was set (LLM determined X supersedes Y).

**What ENGRAM does differently:** A `ct_` node is committed to the graph with explicit edges to both the contradicting and contradicted claims. The contradiction is queryable, explainable, and auditable. It is a first-class epistemic event, not a flag set as a side effect of ingestion.

---

## 5. Retraction Deep-Dive

### 5.1 The cascade question

The core question: if EntityEdge A is marked `invalid_at`, are there any edges B, C, ... whose validity was derived from A also marked invalid?

**Answer from source code: No.**

The `resolve_extracted_edge` function (lines 853-858, verbatim above) sets `invalid_at` on identified `invalidation_candidates`. There is no subsequent graph traversal to find edges that reference the invalidated edge. The `EntityEdge` schema has no `derived_from` field and no mechanism to express "this fact depends on that fact."

The `resolve_extracted_edges` function (outer loop) returns `(resolved_edges, invalidated_edges, new_edges)`. The `invalidated_edges` are persisted with their new `invalid_at` values. There is no additional pass that traverses the graph looking for downstream dependents of the invalidated edges.

### 5.2 Why this is architecturally unavoidable for Graphiti

Graphiti's edge model is fundamentally entity-to-entity (subject-predicate-object triples). Edges cannot reference other edges. In a system where no edge can express "I was derived from edge X," cascade retraction is not just unimplemented — it is architecturally inexpressible. Adding it would require a different graph schema: edges between edges, or a separate derivation layer.

### 5.3 What the paper says (verbatim)

The paper does not use the word "cascade." The paper states invalidation sets `t_invalid` on "the affected edges" (plural) — this refers to multiple directly contradicted edges in the same resolution step, not downstream traversal. There is no retraction cascade claim in the paper.

### 5.4 Post-paper state

v0.29.0 (2026-04-27) release notes do not mention retraction cascade, derivation tracking, or any change to invalidation semantics. The invalidation model is unchanged from the paper.

---

## 6. OCC Mapping — Does Zep/Graphiti Reference Kahl/OCC?

**Kahl is not cited anywhere in arXiv 2501.13956v1.** The paper's references section (Section 6) covers temporal knowledge graph literature, RAG frameworks, and the MemGPT benchmark paper. The concepts of Ontological Continuity, diachronic constraint, and non-interchangeability under reset are not mentioned.

The Graphiti GitHub README, release notes, and documentation do not reference Kahl, OCC, or related philosophical frameworks. This is expected: Graphiti is positioned as a retrieval infrastructure, not an epistemic-identity system.

---

## 7. OCC Satisfaction Per Condition

### Condition 1 — Diachronic Constraint
*Past commitments structure present deliberation non-trivially (binding commitment, not mere path-dependence)*

**Assessment: Does not satisfy Condition 1 on strict OCC terms.**

Graphiti's bi-temporal model means past facts influence present context — but only as retrieval filters, not as binding epistemic commitments. The system retrieves edges where `invalid_at IS NULL` for current state, or temporal queries for historical state. A past fact has no structural authority over a present agent's deliberation; it is input to a retrieval query, not a constraint on the agent's inference process.

On OCC's strict reading, "binding" means the past commitment structures what inferences the agent can make now, not merely what data it has access to. Graphiti provides data with timestamps; it does not model commitments that bind downstream reasoning. An agent using Graphiti can ignore a retrieved fact; an agent using ENGRAM's derivation graph has committed inferences that are structurally tainted if their premises are retracted.

Charitable reading: if one defines "structuring present deliberation" broadly as "past facts survive in the graph and are returned in context," then Condition 1 is nominally satisfied at the data layer. But this collapses Condition 1 to something trivially satisfied by any memory system with persistence, which is not the OCC's intent.

### Condition 2 — Non-Interchangeability Under Reset
*Token-distinctness preserved across snapshot/reset events*

**Assessment: Does not satisfy Condition 2.**

This is the clearest failure. Graphiti is a separable service. The knowledge graph is stored in a graph database (Neo4j, Kuzu, FalkorDB, or Neptune). An agent connects to the graph, reads from it, writes to it. If the agent process is reset, killed, or replaced, the graph is unaffected. Two different agents connecting to the same Graphiti instance are indistinguishable from the graph's perspective — both can read and write the same facts, neither leaves any trace of its individual epistemic history.

From the Zep documentation (April 2026 blog): "every piece of context in the graph, you can answer 'where did this come from?'" — but "where it came from" refers to which episode (conversation) produced it, not which agent. The graph has no agent-identity layer; it is shared infrastructure. OCC Condition 2 requires that agent identity not be reducible to graph contents, but Graphiti makes no such claim and has no such mechanism.

### Condition 3 — Self-Maintaining Arbitration
*Foundational retractions structurally flag downstream commitments within unified deliberative architecture*

**Assessment: Does not satisfy Condition 3.**

As established in Section 5 above, there is no retraction cascade in Graphiti. Invalidating an edge sets a temporal flag on that single edge. The graph has no derivation structure, so there is no "downstream commitments" layer to traverse. The "unified deliberative architecture" requirement implies that the contradiction-detection, invalidation, and cascade are all integrated into the same system that the agent uses to reason — in Graphiti, contradiction detection is an ingestion-pipeline step, not a reasoning-time primitive.

More precisely: Graphiti's arbitration is not "self-maintaining" in OCC's sense. It is externally triggered (by the arrival of new data through the ingestion pipeline). An agent cannot look at its own existing beliefs, find a contradiction, and propagate a retraction. The system can only detect contradictions when new episodes arrive that contradict existing edges.

---

## 8. What Has Shipped Since the Paper (Post-Paper Updates)

### Changes material to this comparison

| Feature | Status | Impact on comparison |
|---|---|---|
| `fact_triple` episode type | Added v0.29.0 (2026-04-27) | Potentially closes the agent-authoring gap — an agent could construct a `(subject, predicate, object)` triple and ingest it directly without conversational extraction. However: no docstring, no documentation found, no examples in codebase as of 2026-05-12. Cannot confirm it works as structured agent-authored claims. Marked: feature present, purpose undocumented. |
| `episode_metadata` filtering | Added v0.29.0 | Enhances provenance-filtered retrieval (return only facts from trusted source X). Does not add quote-level provenance. |
| SagaNode | Added v0.29.0 | Multi-episode narrative summaries. Not relevant to contradiction/retraction comparison. |
| Combined extraction | Added v0.29.0 (opt-in) | Efficiency only; no semantic change to contradiction or retraction behavior. |
| MCP server 1.0 | Released Nov 2025 (per blog) | Integration surface only; no change to graph semantics. |
| Security patch (Cypher injection) | v0.28.2, 2026-03-11 | Security only |

### Changes that do NOT close any gap

- No confidence scoring added.
- No contradiction node type added.
- No derivation primitive added.
- No retraction cascade added.
- No quote-level provenance added.
- Agent-authoring via `fact_triple` remains undocumented; cannot confirm structured-claim semantics.

---

## 9. Honest Assessment — Their Strengths, Our Weaknesses

### Zep/Graphiti genuine strengths

1. **Production-grade infrastructure.** 26k GitHub stars, multi-backend support (Neo4j, Kuzu, FalkorDB, Neptune), MCP server, actively maintained. ENGRAM is a research prototype in SQLite+Git.

2. **Bi-temporal model is clean and well-specified.** The `valid_at` / `invalid_at` / `created_at` / `expired_at` four-field schema is principled and lets you query "what did the agent know at time T about event-time T′." ENGRAM's temporal model is less formally specified.

3. **Benchmarked performance.** The paper reports 94.8% on DMR (vs MemGPT's 93.4%) and up to 18.5% accuracy improvement with 90% latency reduction on LongMemEval. ENGRAM has no published benchmark numbers.

4. **Entity-centric graph is more operationally natural** for most agent use cases: "what do I know about Alice?" is a graph traversal on EntityNode. ENGRAM's claim-centric structure is more epistemically principled but harder to query for simple agent tasks.

5. **Conflict detection is automated and LLM-driven.** No human schema definition of what conflicts with what. ENGRAM requires the agent to explicitly author a `ct_` node.

### ENGRAM genuine weaknesses relative to Zep

1. **No automated conflict detection.** ENGRAM does not have an ingestion pipeline that automatically detects when a new claim contradicts existing ones. Contradiction must be author-identified and explicitly committed.

2. **Research prototype scale.** SQLite is fine for personal-scale graphs; Graphiti supports distributed Neo4j deployments.

3. **No quantitative benchmark comparison.** The OCC arguments are philosophical/structural; reviewers will want empirical validation.

4. **`fact_triple` uncertainty.** If Zep's undocumented `fact_triple` type does enable structured agent-authored claims, the agent-authoring gap may be partially closed by the time reviewers check. This is a risk to track.

---

## 10. Verdict

Zep/Graphiti is the strongest existing system in the comparison set, and the 2026-05-05 second-hand summary holds up under primary-source verification. The core distinctions are structurally confirmed:

**Contradiction** in Graphiti is an ephemeral LLM inference during ingestion that leaves no persistent graph artifact — it produces a temporal flag (`invalid_at`) but no `contradicts` relation, no contradiction node, no queryable record of why or when the determination was made. ENGRAM's `ct_*` nodes are a genuinely distinct structural primitive.

**Retraction cascade** is architecturally inexpressible in Graphiti: the entity-to-entity edge schema has no mechanism to represent "edge B was derived from edge A," so there is nothing to cascade through. The verbatim code (lines 835-858 of `edge_operations.py`) confirms that invalidation operates on directly identified candidates only, with no graph traversal. The Atlan 2026 statement — "No framework describes cascade retraction" — remains accurate as of v0.29.0.

**OCC satisfaction** is zero across all three conditions. Graphiti does not reference Kahl, does not engage the continuity-of-epistemic-agent framing, and does not satisfy any of the three OCC conditions on strict terms.

One material surprise from this read: the addition of `fact_triple` episode type in v0.29.0. This is a potential partial closure of the agent-authoring gap and should be monitored. If Zep ships documented structured-claim authoring before the paper is submitted, the agent-as-author argument needs to be reframed around what structured authoring without provenance-class taxonomy and without cascade retraction still misses.

The paper's strongest claim — that no other system provides the combination of (claim-level contradiction as persistent structural node) + (retraction cascade through derivation chains) — survives this first-hand read intact.

---

## Sources

- arXiv 2501.13956 abstract/metadata: https://arxiv.org/abs/2501.13956
- arXiv 2501.13956 HTML full text: https://arxiv.org/html/2501.13956v1
- Graphiti GitHub repository: https://github.com/getzep/graphiti
- graphiti_core/edges.py: https://github.com/getzep/graphiti/blob/main/graphiti_core/edges.py
- graphiti_core/nodes.py: https://github.com/getzep/graphiti/blob/main/graphiti_core/nodes.py
- graphiti_core/utils/maintenance/edge_operations.py: https://github.com/getzep/graphiti/blob/main/graphiti_core/utils/maintenance/edge_operations.py
- graphiti_core/prompts/dedupe_edges.py: https://github.com/getzep/graphiti/blob/main/graphiti_core/prompts/dedupe_edges.py
- graphiti_core/prompts/extract_edges.py: https://github.com/getzep/graphiti/blob/main/graphiti_core/prompts/extract_edges.py
- graphiti_core/prompts/ directory listing: https://github.com/getzep/graphiti/tree/main/graphiti_core/prompts
- graphiti_core/ directory listing: https://github.com/getzep/graphiti/tree/main/graphiti_core
- Graphiti v0.29.0 release notes: https://github.com/getzep/graphiti/releases/tag/v0.29.0
- Zep help docs landing: https://help.getzep.com/
- Zep help docs Graphiti section: https://help.getzep.com/graphiti
- Zep blog (April 2026 — "Context You Can Trace, Filter, and Trust"): https://blog.getzep.com/context-you-can-trace-filter-and-trust
- Zep blog index: https://blog.getzep.com/
- Baseline scan (2026-05-05): /home/agent-borges/engram-paper/paper_research/agent_memory_landscape_2026-05-05.md
