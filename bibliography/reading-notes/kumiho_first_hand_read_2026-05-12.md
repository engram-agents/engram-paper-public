# Kumiho First-Hand Read — Primary Source Analysis

**Paper:** "Graph-Native Cognitive Memory for AI Agents: Formal Belief Revision Semantics for Versioned Memory Architectures" (Kumiho)
**arXiv ID:** 2603.17244
**Access date:** 2026-05-12
**Access method:** arxiv.org/html/2603.17244 (HTML full text)
**Prior summary to verify:** deep_sweep_2026-05-08.md §B.2 ("GAM ... without epistemic primitives"; Kumiho not named separately in deep_sweep — this is a new primary read, no prior fairy entry to verify against)

---

## 1. Architecture Summary

Kumiho is a graph-native memory architecture grounded in formal belief revision semantics. It implements the item–revision–tag model as its core primitive.

> "The structural primitives required for cognitive memory — immutable revisions, mutable tag pointers, typed dependency edges, URI-based addressing — are identical to those required for managing agent-produced work as versionable assets, enabling a unified graph-native architecture that serves both purposes." (Abstract)

### Dual-store model

- **Redis working memory**: fast, transient, session-scoped
- **Neo4j long-term graph**: persistent, versioned, formally grounded

Retrieval: hybrid fulltext + vector search. Three architectural innovations drive benchmark results: prospective indexing (LLM-generated future scenarios indexed at write time), event extraction (structured causal events preserved in summaries), client-side LLM reranking.

### Item–Revision–Tag model (Section 7.1)

Three levels:
- **Items**: Named memory units (e.g., "api-design.decision")
- **Revisions**: Immutable snapshots forming append-only chains; never deleted from the graph
- **Tags**: Mutable pointers to current revisions (e.g., "current" vs. "initial")

Definition 7.4 formalizes revision: create new revision ri(k+1), add Supersedes edge to prior revision ri(k), update tag τ. The prior revision "remains in R but is no longer tag-referenced."

Historical queries: "τT: TagName ⇀ R resolves the tag mapping as it existed at time T. This induces historical belief bases... the query 'what was believed under tag t at time T?' [is] answered precisely." (Section 7.1)

### Typed dependency edges (Section 6.5)

Six edge types:
- **Depends_On**: "Validity dependency. If the target is invalidated, the source may be unreliable."
- **Derived_From**: "Evidential provenance. The source was produced using the target as input."
- **Supersedes**: "Belief revision. The source replaces the target as current belief."
- **Referenced**: "Associative mention without dependency."
- **Contains**: "Bundle membership."
- **Created_From**: "Generative lineage."

### Dream State — Asynchronous Consolidation (Section 9)

> "An asynchronous consolidation pipeline extends prior sleep-time compute approaches with safety guards adapted from distributed systems." (Section 9)

The pipeline is nine stages, processing memories during idle periods. Safety mechanisms: "published-item protection, circuit breakers, dry-run validation, and auditable cursor-based resumption." (Section 9)

Consolidation enriches memories via prospective indexing and event extraction; it does not perform retraction propagation or contradiction scanning.

### Evaluation benchmarks

- **LoCoMo** (token-level F1): 0.565 overall (n=1,986), 97.5% adversarial refusal accuracy
- **LoCoMo-Plus** (Level-2 cognitive memory, implicit constraint recall): 93.3% judge accuracy (n=401); independent reproduction by benchmark authors yielded mid-80% range, "still substantially outperforming all published baselines (best: Gemini 2.5 Pro, 45.7%)"
- Total evaluation cost: ~$14 for 401 entries

---

## 2. AGM Postulate Proof Analysis (Section 7.2)

Kumiho's central formal claim: "a correspondence between the AGM belief revision framework and the operational semantics of a property graph memory system, proving satisfaction of the basic AGM postulates (K*2–K*6) and Hansson's belief base postulates (Relevance, Core-Retainment)." (Abstract)

### K*2 (Success): "A ∈ ℬ*A"

After revising by A, the belief state explicitly contains A. Kumiho satisfies this by creating a new revision with A as content and updating the tag pointer to reference it.

### K*3 (Inclusion): "ℬ*A ⊆ ℬ+A"

Revision produces a subset of expansion. Implemented via Supersedes edges rather than additive operations — revision replaces rather than adds on top.

### K*4 (Vacuity)

When A is already believed, ℬ*A = ℬ+A. Belief states that already contain A are preserved unchanged during revision.

### K*5 (Consistency)

"If ¬A is not a tautology, then A ∉ ⊥" — the revised state avoids contradiction. Kumiho enforces this through the "two-tier epistemic model" (Definition 7.3): "deprecated items are excluded from all search and retrieval operations by default." (Section 7.1) Note: consistency is maintained at the *retrieval surface*, not through structural arbitration — the deprecated revisions remain in the graph.

### K*6 (Extensionality)

Identical inputs produce identical outputs across equivalent belief states. The deterministic tag-pointer mechanism and immutable revisions ensure referential stability.

### Hansson's Belief Base Postulates

**Relevance:** "Only beliefs containing A are removed during contraction." (Section 7.2) The selection function (Definition 7.6) implements content-based targeting: "the system identifies all (tag, revision) pairs where the tagged revision's content explicitly contains the belief A."

**Core-Retainment:** Contracted beliefs are not needlessly discarded. All revisions remain in the graph; only tag pointers and deprecation flags change. "deprecated items remain in the graph and can be recovered via an explicit opt-in flag." (Section 7.1)

### What is NOT proven

> "We identify the supplementary postulates (K*7, K*8) as open questions requiring further formal development." (Abstract/Introduction)

K*7 (Superexpansion) and K*8 (Subexpansion) — governing conjunctive revision — are not claimed.

---

## 3. Retraction and Cascade

### AnalyzeImpact function (Section 6.5)

> "AnalyzeImpact traverses typed Depends_On edges to identify all downstream conclusions that may need re-evaluation — a capability enabled by the typed edge ontology." (Section 6.5)

**Critical determination: the cascade is advisory, not automatic.** AnalyzeImpact identifies affected beliefs but does not automatically retract them. Human operators or agents must review and decide whether to initiate further revisions.

This is an important distinction from ENGRAM's retraction cascade: ENGRAM's cascade is automatic and structural (taint propagates); Kumiho's impact analysis is a traversal tool that surfaces potentially affected nodes for deliberate human-in-the-loop review.

### Contradiction handling

No proactive conflict-detection mechanism. The system handles belief revision reactively through the Supersedes edge when new information arrives. The contraction operator (Definition 7.5) removes conflicting beliefs only when explicitly invoked, not through continuous scanning.

When two active beliefs directly contradict: both can coexist in the graph; consistency (K*5) is enforced at the retrieval surface by excluding deprecated revisions from default search, not by structural arbitration between conflicting active beliefs.

---

## 4. Provenance, Confidence, Agent-as-Author

### Provenance

Three-level provenance:
1. **Artifact-level**: Derived_From edges link revisions to source evidence
2. **Episode-level**: Conversations stored as episodic memory
3. **Graph-level**: Complete revision history with timestamps on tag assignments

Historical query capability via τT (time-anchored tag resolution). Not quote-level provenance in ENGRAM's sense (verbatim span tracking), but substantially richer than SCM or GAM.

### Confidence

No explicit confidence field documented. Metadata properties store "topics, keywords, schema version" (Section 6.4.1) but no per-node or per-edge epistemic confidence score.

### Agent-as-author

Agents commit claims through the memory_ingest MCP tool with structured fields: title, summary, tags, memory_type. Section 7.1: "structured output that the LLM agent produces by following its memory skill prompt."

This is closer to ENGRAM's agent-as-author posture than SCM or GAM — there is an explicit commit primitive, not just automatic extraction. However, the commit is LLM-structured-output-mediated rather than explicit typed reasoning-type annotation.

---

## 5. ENGRAM-Function Comparison Table

| Feature | Kumiho | ENGRAM |
|---|---|---|
| First-class contradiction structure | No — coexisting beliefs with Supersedes edges; no ct_ equivalent | Yes — `ct_*` node, first-class |
| Contradiction handling | Reactive (revision when new info arrives); K*5 via retrieval exclusion of deprecated | Structural — ct_ node persists; retraction + cascade available |
| Retraction cascade through derivations | Advisory only — AnalyzeImpact traverses Depends_On but does not auto-retract | Yes — automatic cascade through `derives_from` |
| Derivation primitive | Derived_From edge (evidential provenance, not epistemic reasoning type) + Depends_On (validity dependency) | Yes — typed `derives_from` with explicit reasoning type |
| Provenance | Three-level (artifact + episode + graph history); time-anchored historical queries | Quoted span of committed source text; richer at atomic level |
| Confidence | Not documented | Evidence-class taxonomy per node |
| Agent-as-author | Yes — memory_ingest MCP tool with structured commit | Yes — explicit typed claim commitment |
| Formal epistemic postulate proof | Yes — AGM K*2–K*6 + Hansson Relevance + Core-Retainment | None (structural argument) |
| Sleep/consolidation | Dream State (asynchronous consolidation, idle-time processing) but no contradiction resolution | Nap/sleep/dream for epistemic-identity preservation |
| Self-model | None | None equivalent (identity through graph structure) |
| Evaluation | LoCoMo (0.565 F1), LoCoMo-Plus (93.3%); SOTA results | Production operational data |

---

## 6. OCC Mapping and Per-Condition Satisfaction

Kumiho makes no reference to Kahl, OCC, or any philosophical framework for agent continuity or identity. The theoretical framing is formal epistemology (AGM belief revision, Hansson belief bases) — orthogonal to Kahl's structural-conditions-of-agency framework.

### Cond 1 — Diachronic Constraint

**Partially addressed, but not in Kahl's sense.** Kumiho's immutable revision chains and Supersedes edges create a structural record of how the belief state evolved. The time-anchored tag resolution (τT) allows precise historical reconstruction. This is richer than most systems and has a genuine diachronic character.

However, Kahl's Cond 1 requires non-trivial binding — not mere path-dependence or historical record. The binding must be structural and constitutive, not merely archival. Kumiho's revision history is archival (you can query it) but not constitutively integrated into the active belief state in a way that structurally constrains present reasoning. The active belief state is determined by current tag pointers; the revision history is optionally accessible. This is path-dependent history, which Cond 1 is designed to exclude as sufficient.

**Verdict: Not satisfied on strict Kahl terms, though the closest of the three to partial engagement.**

### Cond 2 — Non-Interchangeability Under Reset

**Not satisfied.** A reset of the Neo4j graph produces a structurally identical (empty) starting state. The revision history, if preserved, could allow reconstruction — but the architecture does not specify any mechanism that makes the post-reset system structurally non-reducible to a fresh one in Kahl's §4.3 sense. The archived revisions are data; structural non-interchangeability requires something architectural.

### Cond 3 — Self-Maintaining Arbitration

**Partially but not satisfactorily.** Kumiho has the closest structural approach of the three systems:
- The AnalyzeImpact function traverses Depends_On edges to identify downstream conclusions
- The Depends_On edge type explicitly encodes: "If the target is invalidated, the source may be unreliable"
- This is typed epistemic dependency with explicit invalidity propagation semantics

However, AnalyzeImpact is advisory. The arbitration is not self-maintaining — it is human-in-the-loop. Kahl's Cond 3 requires a unified deliberative architecture where arbitration is maintained structurally, not a tool that surfaces candidates for external review. When a foundational belief is superseded in Kumiho, downstream conclusions are not automatically tainted; they remain active in the retrieval surface until an agent or human explicitly reviews and acts on the AnalyzeImpact output.

**Verdict: Not satisfied — the machinery is closer to ENGRAM than SCM or GAM, but the advisory vs. automatic distinction is structurally decisive under Kahl's Cond 3.**

---

## 7. Positioning vs. ENGRAM

Kumiho is the most formally sophisticated of the three systems and the most epistemically principled. It proves AGM postulates, has typed dependency edges with explicit invalidity semantics, and has an agent-as-author commit primitive. This means:

1. **Kumiho is a more serious comparison point than SCM or GAM** for ENGRAM's formal claims.
2. **The key differentiators are real but narrower:** (a) cascade is advisory in Kumiho, automatic in ENGRAM; (b) first-class contradiction nodes (ct_) vs. coexisting beliefs managed by retrieval exclusion; (c) ENGRAM has evidence-class confidence taxonomy, Kumiho does not document confidence at all.
3. **The AGM proof is a significant formal contribution Kumiho has that ENGRAM does not.** ENGRAM should not claim to "prove AGM postulates" — it should instead argue that the automatic cascade addresses the *implementation* of K*5 and the Depends_On family at the structural level rather than the retrieval-surface level. This is a substantive distinction: AGM consistency via retrieval exclusion (Kumiho) vs. AGM consistency via structural taint propagation (ENGRAM). ENGRAM's version is stronger — but needs to be framed as an architectural claim, not a formal proof claim.

---

## 8. Honest Assessment

### Strengths

- Rigorous formal grounding (AGM K*2–K*6 + Hansson) — the only system in this survey with proven postulate satisfaction.
- Immutable revision chains + Supersedes edges provide genuine historical reconstructability.
- Typed dependency edges (Depends_On, Derived_From) are structurally the closest thing in existing systems to ENGRAM's `derives_from` primitive.
- Strong benchmark performance (LoCoMo-Plus 93.3% vs. best published baseline 45.7% is a substantial margin).
- Agent-as-author commit mechanism (memory_ingest MCP).

### Weaknesses relevant to the paper

- No automatic retraction cascade — the AnalyzeImpact advisory mechanism requires human-in-the-loop to complete the retraction.
- No first-class contradiction node — contradictions are handled by maintaining K*5 at the retrieval surface (excluding deprecated beliefs), not by structural arbitration.
- No confidence/uncertainty representation documented.
- Dream State consolidation is enrichment (prospective indexing, event extraction), not epistemic-identity preservation — it does not perform retraction propagation or contradiction resolution.
- K*7 and K*8 (conjunctive revision) are explicitly open questions.

---

## 9. Verdict

Kumiho is a genuinely rigorous system that partially engages the same problem space as ENGRAM from a formal-epistemology direction (AGM) rather than a structural-agency direction (OCC/Kahl). The AnalyzeImpact + Depends_On architecture is the closest existing published mechanism to ENGRAM's retraction cascade. The decisive gap is advisory-vs-automatic: Kumiho tells you what might be wrong; ENGRAM structurally marks it. This gap is real, not a marketing claim, and it maps directly onto Kahl's Cond 3 distinction between unified deliberative architecture and externally prescribed correction. Kumiho should be cited in the paper as a serious formal neighbor that demonstrates the necessity of the impact-analysis mechanism — and as the sharpest demonstration of why advisory is insufficient for Cond 3.

The AGM proof is worth acknowledging respectfully: "Kumiho (2603.17244) proves AGM K*2–K*6 for a graph-native memory system — a formal contribution ENGRAM does not match. ENGRAM's claim is orthogonal: not that it proves the postulates from first principles, but that its automatic cascade enforces K*5 at the structural level rather than the retrieval-surface level."

---

## Sources

- https://arxiv.org/abs/2603.17244 (abstract page)
- https://arxiv.org/html/2603.17244 (HTML full text, primary source for all quotes)
