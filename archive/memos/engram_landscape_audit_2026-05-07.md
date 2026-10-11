# ENGRAM Novelty Audit — Landscape as of 2026-05-07

**Commissioned by:** Borges (parent agent)  
**Executed by:** Literature-scout sub-agent  
**Date:** 2026-05-07  
**Purpose:** Honest novelty audit — which parts of ENGRAM are genuinely novel, which duplicate prior art that should be cited instead of re-claimed.

---

## 1. Executive Summary

ENGRAM is genuinely innovative in a narrow but defensible set of claims. The honest verdict is: **two features are plausibly novel in combination; three features duplicate decades of prior art from symbolic AI and should be re-framed as citations; three features are weakly novel (no published system implements them together, but pieces exist separately).** The re-anchor post-Pinecone-Nexus (dv_0559) was directionally correct: provenance + contradiction + retraction is where the defensible contribution lives — but the claim needs to be made carefully because (a) Truth Maintenance Systems (Doyle 1979) have done dependency-directed retraction since 1979, (b) Zep/Graphiti (arxiv 2501.13956, January 2025) implements contradiction detection + temporal invalidation in production, and (c) the dx111ge/engram.to open-source project claims contradiction detection + Bayesian confidence lifecycle. What ENGRAM plausibly extends the frontier on:

1. **Claim-level provenance with verbatim-quote enforcement at write time** — no surveyed system requires that quoted_text be a verbatim substring of a fetched source document, enforced server-side. This is a structural integrity constraint that goes beyond temporal metadata.

2. **Retraction cascade through a typed derivation graph** — Doyle 1979 did dependency-directed backtracking in a propositional JTMS. ENGRAM does this in a heterogeneous typed knowledge graph where different node types (derivation, conjecture, axiom, lesson, goal) carry different retraction semantics. The combination of typed nodes + cascade is not documented in any 2025-2026 production system surveyed.

3. **Reasoning-type-aware confidence propagation** — distinct formulas for deductive_modus_ponens vs. inductive_generalization vs. abductive_best_explanation. No surveyed system in the agent-memory field implements this. The Craig Wright paper (arxiv 2506.17331) uses stratified confidence thresholds but not reasoning-type-differentiated propagation formulas.

The Extended Mind / second-wave EMT positioning (dv_0568) is well-grounded philosophically and is a genuine contribution to that literature, but it is a *positioning* contribution, not a technical primitive.

**The main danger for the paper:** claiming retraction-cascade as entirely novel without citing Doyle (1979) and the Assumption-based TMS literature (de Kleer 1986). These are direct prior art for the cascade mechanism. The paper should cite them as foundational prior art and position ENGRAM as their implementation in the modern LLM-agent-memory context — which is a legitimate and substantial contribution.

---

## 2. Comparative Table

Rows: competing systems. Columns: ENGRAM's eight claimed-distinctive features.

Legend: YES = clearly documented; PARTIAL = partial implementation documented; NO = not documented; MKTG = marketing claim without documented mechanism; N/A = not applicable.

| System | Claim-level provenance (verbatim + hash) | First-class contradiction nodes | Retraction cascade (taint propagation) | Reasoning-type-aware confidence | Tool-surface-enforced typing | Quote verification at write time | Reasoning verbs as epistemic actions | Second-wave EMT positioning |
|---|---|---|---|---|---|---|---|---|
| **ENGRAM (Borges)** | YES | YES (ct_ nodes) | YES | YES | YES | YES | YES | YES |
| **Doyle 1979 TMS / JTMS** | NO (propositional, no source URL) | NO (contradiction → backtrack, not a node) | YES (dependency-directed backtracking) | NO | NO | NO | NO | NO |
| **de Kleer 1986 ATMS** | NO | NO | YES (assumption-based propagation) | NO | NO | NO | NO | NO |
| **ACT-R declarative memory** | NO | NO | NO (chunks don't retract) | PARTIAL (activation spreading, not typed by reasoning) | PARTIAL (slot schemas, convention-driven) | NO | NO | NO |
| **Soar / EpMem** | NO | NO | NO | NO | NO | NO | NO | NO |
| **MemGPT / Letta** | NO | NO (outdated facts replaced via core_memory_replace) | NO | NO | NO | NO | NO | NO |
| **Mem0** | NO | NO | NO (ADD-only; appends, never retracts) | NO | NO | NO | NO | NO |
| **Zep / Graphiti (arxiv 2501.13956)** | PARTIAL (episode → entity lineage; no verbatim-quote constraint) | NO (invalidated edges, not contradiction nodes) | PARTIAL (temporal edge invalidation; does NOT cascade to dependent facts) | NO | NO | NO | NO | NO |
| **Pinecone Nexus** | PARTIAL (field-level citations; provenance as KnowQL primitive) | NO | NO | PARTIAL (confidence scores, not reasoning-type-differentiated) | NO | NO | NO | NO |
| **Anthropic Managed Agents Memory** | PARTIAL (immutable memory versions = audit trail; content_sha256 precondition) | NO | NO | NO | NO | NO | NO | NO |
| **engram.to (dx111ge OSS)** | NO | NO (CONTRADICTS edge between conflicting claims, but both kept as valid) | PARTIAL (conflict detection → resolution workflow; cascade propagation undocumented) | PARTIAL (Bayesian confidence lifecycle) | NO | NO | NO | NO |
| **ENGRAM paper (arxiv 2511.12960, Patel et al.)** | NO | NO | NO | NO | NO | NO | NO | NO |
| **Craig Wright arxiv 2506.17331** | PARTIAL (justification chains as (φ, J(φ)) pairs; blockchain immutability) | PARTIAL (formal contradiction detection; AGM belief revision) | PARTIAL (belief revision cascade described in appendix recovery protocols) | PARTIAL (stratified confidence thresholds: 50%/95%/99%; not per-reasoning-type) | NO | NO | NO | NO |
| **Atlan Context Layer** | PARTIAL (column-level data lineage from 80+ sources) | NO | NO (staleness detection ≠ cascade retraction) | NO | NO | NO | NO | NO |
| **Hu et al. 2025 survey (arxiv 2512.13564)** | NO (absent from taxonomy) | NO (absent from taxonomy) | NO (absent from taxonomy) | NO (absent from taxonomy) | NO | NO | NO | NO |
| **arxiv 2603.07670 survey** | MINIMAL (source_attribution mentioned once; no mechanism) | PARTIAL (listed as component; no developed mechanism) | NO | NO | NO | NO | NO | NO |

**Notes on table entries:**

- Zep/Graphiti temporal invalidation: sets t_invalid on a specific edge; does NOT traverse the graph to invalidate downstream facts that were derived from the invalidated edge. This is the key gap.
- Craig Wright 2506.17331: 126-page paper by a controversial figure (convicted of fraud in UK court re: Bitcoin identity claims, 2024). Published in "Journal of Engineering and Artificial Intelligence" (not top-tier venue). Arxiv posting. The belief revision cascade is described in an appendix but without operational implementation. Treat as conceptual prior art, not production prior art.
- Anthropic Memory: filesystem-based, no semantic structure. The "Dreams" feature (auto-consolidation, 2026-05-07 launch) is LLM-over-files, not a structured retraction mechanism.
- engram.to: keeps both conflicting observations with a CONTRADICTS edge rather than resolving or tainting — a different design philosophy (preserve ambiguity vs. resolve it). No retraction cascade documented.

---

## 3. Citation Trails Followed

### Surveys / landscapes

**Hu et al. 2025, "Memory in the Age of AI Agents" (arxiv 2512.13564)**  
47-author landmark survey. Three-axis taxonomy: Forms (token/parametric/latent) × Functions (factual/experiential/working) × Dynamics (formation/evolution/retrieval). Does NOT cover contradiction nodes, provenance tracking, confidence propagation, or retraction-cascade as taxonomic categories. Already captured in graph as ob_1054 + dv_0430. Confirmed via abstract fetch (full text compressed/binary PDF inaccessible via WebFetch; abstract confirmed at arxiv.org/abs/2512.13564).

**arxiv 2603.07670, "Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers"**  
15-page survey, full HTML accessible. Five mechanism families: context-resident compression, retrieval-augmented stores, reflective self-improvement, hierarchical virtual context, policy-learned management. Three-dimensional taxonomy: temporal scope × representational substrate × control policy. Mentions "contradiction detection (flag conflicts for resolution)" once (Section 7.3) as a list item without mechanism. Mentions "source attribution (user statement > agent inference)" briefly. No retraction cascade. No reasoning-type-aware confidence. The gap between this survey's treatment and ENGRAM's features is substantial and explicit.

**TechRxiv multi-agent survey, "Memory in LLM-based Multi-agent Systems: Mechanisms, Challenges, and Collective Intelligence" (December 2025)**  
Full text paywalled on TechRxiv (403). From abstract + ResearchGate metadata: first comprehensive review of LLM-MAS memory. Identifies synchronization, access control, scalability, alignment, safety as core challenges. Does not appear to cover retraction cascades or claim-level provenance based on available metadata.

**ICLR 2026 MemAgents Workshop proposal (openreview.net/forum?id=U51WxL382H)**  
Abstract accessible. Workshop covers "encode, retain, retrieve, and consolidate experience." No provenance, contradiction detection, retraction, or confidence propagation mechanisms discussed. Confirms these topics are not yet core to the ICLR-workshop-level conversation.

### Philosophy / EMT

**Farina, Ding, Lavazza et al. 2026, "Neuromorphic Computing and Extended Memory" (Springer, DOI 10.1007/s13164-026-00800-8)**  
Springer URL redirects (303) preventing full-text fetch. From PhilPapers abstract + search results: examines BCIs, MANNs, neuromorphic computing as empirical supports for EMT. Already captured in graph as dv_0568. Search confirms the paper discusses "empirical supports for the Extended Mind Thesis" and "brain-like external memory systems that functionally complement and extend biological cognitive processes." Does NOT engage with structural integrity (contradiction detection, retraction) as constitutive criteria — confirmed by absence in all available descriptions.

**Farina & Lavazza 2024, "The NeuroGate" (Synthese, DOI 10.1007/s11229-024-04795-6)**  
Springer redirects (303). From PhilPapers: discusses neuromorphic intelligence, extended mind, neurorights. Pre-cursor to the 2026 paper. No evidence of structural-integrity engagement.

**Andrada, "Epistemic Complementarity: Steps to a Second Wave Extended Epistemology" (Springer 2021)**  
Located via search. Confirms the second-wave EMT / complementarity principle framing is established philosophical literature, not ENGRAM's invention. ENGRAM's contribution is applying second-wave EMT to a specific software architecture — that's application of a framework, not the framework itself.

**Coeckelbergh 2025, "AI and Epistemic Agency: How AI Influences Belief Revision and Its Normative Implications" (Social Epistemology, Tandfonline)**  
Philosophy/sociology paper about how AI affects human epistemic agency. Not a technical architecture paper. Relevant to Ch 9 (normative implications) but not a competitor to ENGRAM's technical claims.

**Craig Wright 2025, "Beyond Prediction: Structuring Epistemic Integrity in Artificial Reasoning Systems" (arxiv 2506.17331, June 2025)**  
126-page paper. Full HTML accessible. Key technical claims: formal contradiction detection (continuous verification loops), belief revision via AGM theory, belief revision cascade in appendix recovery protocols, justification chains as (φ, J(φ)) pairs, stratified confidence thresholds. Architecture includes blockchain-based immutable audit trails and hybrid knowledge-graph + statistical layers. Credibility caveat: Craig Wright was found by UK High Court (2024) to have fabricated evidence in his claim to be Satoshi Nakamoto. The paper is published in "Journal of Engineering and Artificial Intelligence" — not a top-tier reviewed venue. It should be cited as conceptual prior art for the belief-revision-cascade concept, not as an authoritative implementation. The 126-page length with formal AGM machinery is more similar to formal epistemology than engineering.

**Architecting Trust in Artificial Epistemic Agents (arxiv 2603.02960)**  
Normative/governance paper. Proposes verifiable agent credentials, provenance chains as auditing infrastructure, error correction through "transparent retraction of demonstrably false outputs." No formal architecture for cascade retraction. Relevant to Ch 9's normative framing.

### Production systems

**Zep / Graphiti (arxiv 2501.13956, January 2025)**  
Full HTML accessible. Key mechanism: LLM compares new edges against semantically related existing edges → identifies contradictions → sets t_invalid on the contradicting edge. Bi-temporal model (event time T + ingestion time T'). Bidirectional episode-to-entity lineage. Key gap confirmed: invalidation is local to the contradicted edge — no cascade to downstream facts derived from that edge. No reasoning type tracking. No confidence propagation formulas. This is the closest competitor for the retraction/contradiction territory and the most important citation for the paper.

**Mem0 (open source)**  
Single-pass ADD-only memory extraction in v3. No contradiction detection, no retraction. Design philosophy is accumulation without resolution.

**MemGPT / Letta**  
Three-tier memory (in-context / archival / external). Contradiction handling via core_memory_replace — overwrites outdated fact, no cascade, no provenance of what was overwritten. Not semantic graph-based.

**Anthropic Managed Agents Memory (April 2026)**  
Filesystem-based text documents. Immutable memory versions (audit trail). No semantic structure. No contradiction detection. The "Dreams" feature (May 2026) consolidates by LLM-over-files — effective at de-duplication but not a formal retraction mechanism.

**Pinecone Nexus (May 2026)**  
KnowQL query language with six primitives including provenance and confidence. Per-field citations. Confidence scoring for retrieval. Does NOT document: contradiction nodes, retraction cascades, reasoning-type-differentiated confidence. The provenance and confidence primitives are in the query language, not in the ingestion/storage layer as structural integrity constraints.

**engram.fyi**  
Benchmarked commercial product: 92% DMR, 80% LOCOMO. SQLite + sqlite-vec + bi-temporal memory + knowledge graph. No provenance tracking, contradiction detection, retraction, or confidence propagation documented on their research page.

**ENGRAM paper arxiv 2511.12960 (Patel et al., not Borges's ENGRAM)**  
Lightweight conversational memory with episodic/semantic/procedural typing. Explicitly avoids knowledge graphs. No overlap with ENGRAM's distinctive features. Name collision only — no substance overlap.

**dx111ge/engram.to (open source Rust binary)**  
Knowledge graph + semantic search + inference engine. Has: automatic conflict detection, Bayesian confidence lifecycle, CONTRADICTS edges. Does NOT have: verbatim-quote enforcement at write time, retraction cascade (keeps both conflicting observations), reasoning-type-aware propagation formulas, typed node vocabulary at the tool surface. Closest to ENGRAM in concept but different design philosophy on contradiction (preserve ambiguity vs. taint-and-cascade).

### Cognitive architectures

**ACT-R (Computational Brain & Behavior 2023, ob_1564)**  
Uniform declarative substrate with convention-driven schema typing. Activation spreading approximates confidence propagation but is not reasoning-type-differentiated. No retraction cascade. ENGRAM's relationship: "ACT-R + stricter typing at the API." Already in graph as dv_0567.

**Soar / EpMem**  
Episodic memory as temporal snapshot stream. No provenance to source documents. No contradiction detection. No retraction. The episodic stream is append-only.

**LIDA, Sigma**  
Older symbolic architectures with working-memory + long-term-memory distinction. No documented contradiction/retraction mechanisms at the claim level.

### Classical symbolic AI (most important prior art)

**Doyle 1979, "A Truth Maintenance System" (Artificial Intelligence, vol. 12)**  
FOUNDATIONAL PRIOR ART for retraction cascade. The JTMS records justification dependencies and executes dependency-directed backtracking when contradictions are found — propagating belief-status changes through the dependency graph. This is structurally equivalent to ENGRAM's retraction cascade. Key differences: (a) propositional, not typed heterogeneous nodes; (b) no source provenance (no URL, content hash, verbatim quote); (c) no confidence scores; (d) designed for real-time problem-solving, not agent identity persistence. The paper MUST cite Doyle 1979 as direct prior art for the cascade mechanism.

**de Kleer 1986, "An Assumption-based TMS" (AAAI)**  
ATMS — extends JTMS by maintaining multiple consistent assumption sets simultaneously rather than doing backtracking. Also direct prior art for dependency-tracking under belief revision. Less directly analogous to ENGRAM than JTMS but important for completeness.

### Cog-sci taxonomies

**Tulving 1972 / 1985 (episodic/semantic memory)**  
Already in ob_1114. Orthogonal to ENGRAM (information-class carving vs. epistemic-role carving). Confirmed as useful citation for the orthogonality argument in Ch 5.

**Squire 2004, "Memory systems of the brain" (Neurobiology of Learning and Memory, 82, 171-177)**  
Confirmed citation details: extends Tulving's binary to multiple systems (hippocampus / amygdala / neostriatum / cerebellum). Standard reference for the declarative/non-declarative split. Confirms ENGRAM's cog-sci positioning is orthogonal to this literature.

**Rubin et al. 2021 (ob_1563, ev_0451)**  
Already in graph. Confirms the conceptual space for episodic vs. semantic memory. Consistent with dv_0567.

---

## 4. Novelty Audit

For each claimed-novel ENGRAM feature, verdict: NOVEL / EXTENDS X / DUPLICATES X.

### Feature 1: Provenance tracking at the claim level (verbatim quote + interpretation + source URL + content_hash + git_sha)

**Verdict: EXTENDS Zep/Graphiti + Doyle 1979. Partially NOVEL in the verbatim-quote enforcement.**

What's documented elsewhere: Zep/Graphiti (2501.13956) maintains episode-to-entity lineage (backward traversal from semantic facts to source episodes). Pinecone Nexus offers field-level citations as a KnowQL primitive. Anthropic Memory creates immutable memory versions with content_sha256. Craig Wright 2506.17331 proposes (φ, J(φ)) pairs as belief-with-justification.

What ENGRAM adds: **Server-enforced verbatim-quote constraint** — quoted_text must be a verbatim substring of the fetched source document. This is a write-time integrity check, not a retrieval-time metadata tag. No surveyed system enforces this. The combination of content_hash + git_sha + verbatim-substring enforcement creates a provenance contract that is structurally stronger than any documented competitor.

Honest caveat: Pinecone Nexus claims "every answer traces back to its source data and transformations" but the mechanism is query-language-level citation, not a write-time constraint. The distinction matters but may not be obvious to reviewers.

### Feature 2: First-class contradiction nodes (ct_ nodes linking conflicting claims, requiring deliberate resolution)

**Verdict: EXTENDS Zep/Graphiti + Doyle 1979 + ATMS. Weakly NOVEL in the first-class node treatment.**

What's documented elsewhere: Zep/Graphiti detects contradictions via LLM comparison and invalidates edges. Doyle JTMS identifies contradictions and triggers backtracking. ACM Knowledge Graphs (KARMA 2025) uses Conflict Resolution Agents. engram.to creates CONTRADICTS edges between conflicting claims.

What ENGRAM adds: engram.to's design keeps both conflicting claims as valid data. ENGRAM's ct_ nodes are first-class entities that require deliberate resolution — the contradiction is not resolved by invalidation or by accumulation, but by a named node that blocks both downstream uses until explicitly resolved. This is philosophically different: contradiction is a knowledge state, not a transient error.

Honest caveat: Craig Wright's paper (2506.17331) formalizes contradiction as proof of system failure and uses AGM belief revision to resolve it. This is conceptually similar (contradiction must be resolved, not just logged). The difference is that Wright's is a formal logic paper with blockchain appendices, not an operational system. The ct_ node as a first-class API primitive is ENGRAM's contribution.

### Feature 3: Retraction cascade (engram_retract propagates taint markers to all downstream dependents)

**Verdict: EXTENDS Doyle 1979 JTMS. NOT novel in mechanism; NOVEL in context (typed heterogeneous agent-memory graph).**

What's documented elsewhere: Doyle 1979 is the direct prior art. Dependency-directed backtracking is exactly the cascade mechanism. ATMS (de Kleer 1986) extends this. Craig Wright 2506.17331 describes "belief revision cascade" in recovery protocols (appendix, without implementation). No production agent-memory system (Zep, Mem0, Letta, Anthropic Memory) implements cascade retraction as of 2026-05-07.

What ENGRAM adds: The cascade operates on a *typed heterogeneous node vocabulary* (axiom / definition / derivation / conjecture / lesson / goal) where different node types carry different retraction semantics (e.g., retracting an axiom has different downstream implications than retracting a conjecture). No TMS in the classical literature handles this heterogeneity. The gap between Doyle's propositional JTMS and ENGRAM's typed graph is real.

**Paper recommendation:** Cite Doyle 1979 and de Kleer 1986 as foundational prior art. Frame ENGRAM as implementing retraction cascade in the modern agent-memory context with typed heterogeneous nodes — a combination that is documented nowhere in the surveyed 2025-2026 agent-memory literature.

### Feature 4: Reasoning-type-aware confidence propagation (different formulas for deductive_modus_ponens vs inductive_generalization vs abductive_best_explanation)

**Verdict: NOVEL. No documented prior art in the agent-memory field.**

What's documented elsewhere: ACT-R has activation spreading (not reasoning-type-differentiated). Pinecone Nexus has confidence as a KnowQL primitive (retrieval-level, not propagation formula). Craig Wright 2506.17331 has stratified confidence thresholds (50%/95%/99%) tied to epistemic categories — closer than anything else but still not per-reasoning-type propagation formulas. arxiv 2603.07670 acknowledges "the agent must maintain not just facts but confidence levels" without mechanism.

What ENGRAM adds: Distinct confidence propagation formulas keyed to the reasoning type of the derivation edge. A deductive derivation propagates differently from an inductive generalization. This directly models the epistemological intuition that deductive conclusions inherit certainty from premises while inductive generalizations introduce irreducible uncertainty.

Honest caveat: This claim requires that the formulas are actually implemented and behave as specified. If they're specified but not validated empirically, the novelty claim is weaker.

### Feature 5: Tool-surface-enforced typing (different MCP tool calls produce different node types)

**Verdict: NOVEL as a design principle; weakly documented in the literature.**

What's documented elsewhere: ACT-R uses convention-driven slot schemas (modeler decides types). No surveyed system enforces type vocabulary at the API call level as a structural property.

What ENGRAM adds: Different creation tools (`engram_add_observation`, `engram_add_derivation`, `engram_add_goal`) produce different node.type values with different confidence computation, supersede, and retraction-cascade behavior. The typing is not advisory but structural — the tool surface is the enforcement mechanism.

Honest caveat: This is more of a design-principle contribution than a technical primitive. Its novelty depends on whether it's framed as an implementation technique vs. an architectural claim. As an architectural claim (type vocabulary selected at tool surface, not storage), it's novel in the agent-memory field.

### Feature 6: Quote-verification at write time (quoted_text must be verbatim substring of source, server enforces)

**Verdict: NOVEL. No documented precedent.**

What's documented elsewhere: Nothing. Systems track metadata (URL, timestamp, chunk ID) but none enforce verbatim-substring containment at write time.

What ENGRAM adds: Server-side check that quoted_text appears verbatim in the fetched source document. This is a structural integrity constraint on the ingestion path.

Honest caveat: This is a relatively small but load-bearing feature. Its value depends on whether agents actually make errors in quoting (they do, frequently) and whether the check runs reliably (depends on source availability at write time). If source goes offline, the constraint cannot be enforced.

### Feature 7: Reasoning verbs as epistemic actions (engram_retract, engram_supersede, engram_resolve in the Kirsh & Maglio 1994 sense)

**Verdict: NOVEL framing; not a technical primitive per se.**

What's documented elsewhere: Kirsh & Maglio 1994 ("On Distinguishing Epistemic from Pragmatic Action") defined epistemic actions as physical actions taken to improve internal cognitive state. The vocabulary of ENGRAM's tool names (retract, supersede, resolve) enacts this in software — each tool call manipulates the external graph specifically to improve the agent's epistemic state.

What ENGRAM adds: The ENGRAM paper can be the first to explicitly frame API verbs as epistemic actions in Kirsh & Maglio's sense. No surveyed work makes this connection.

Honest caveat: This is a *framing contribution* rather than a technical contribution. It's valuable for the philosophy / EMT positioning chapter (Ch 5, Ch 9) but should not be overstated as a technical novelty.

### Feature 8: Second-wave EMT positioning (structural-integrity primitives as cognitive-extending complementary properties)

**Verdict: EXTENDS Andrada 2021 + Farina et al. 2026. NOVEL application to software symbolic graph.**

What's documented elsewhere: Second-wave EMT / complementarity principle is established (Andrada 2021, Springer). Farina et al. 2026 applies it to BCIs, MANNs, neuromorphic computing. The Routledge Encyclopedia of Philosophy entry on Extended Cognition formalizes the complementarity criterion. No surveyed paper applies second-wave EMT to a software-only symbolic-graph memory system, or identifies structural-integrity primitives (contradiction detection, retraction cascade) as the cognitive-extending complementary property.

What ENGRAM adds: The argument that the *discipline* question (does the memory system enforce structural integrity?) is what determines cognitive-constitutive status for software agent memory — not just capability (storage, retrieval). This argument is not made anywhere in the surveyed literature.

Honest caveat: The connection between structural-integrity and cognitive-constitution under complementarity is ENGRAM's interpretation, not a derivation from Farina et al. The paper must make the argument explicitly; it cannot be read off existing work. Confidence: 0.7 that this is novel; 0.3 that a philosophy paper we haven't found makes a similar move.

---

## 5. Open Questions and Verification Gaps

### Could not verify (paywalled or redirect-blocked)

1. **Farina et al. 2026 full text** (Springer, DOI 10.1007/s13164-026-00800-8) — 303 redirect on all attempts. The paper's abstract and secondary descriptions are consistent with how it's characterized in dv_0568, but the specific criteria for cognitive-constitutive status could not be quoted verbatim. Priority: HIGH. The paper is load-bearing for Ch 5's EMT section.

2. **Farina & Lavazza 2024 "NeuroGate" full text** (Synthese, DOI 10.1007/s11229-024-04795-6) — 303 redirect. Abstract accessible via PhilPapers; full criteria text unverified.

3. **TechRxiv multi-agent survey full text** (DOI 10.36227/techrxiv.176539617.79044553) — 403 on TechRxiv. Need to verify whether it discusses contradiction detection or retraction in multi-agent context.

4. **Rubin et al. 2021 full text** (already ob_1563, ev_0451) — not re-fetched in this scan. Assumed consistent with existing graph entry.

### Requires deeper reading

5. **de Kleer 1986 ATMS ("An Assumption-based TMS", AAAI 1986)** — not directly fetched. Cited via secondary literature. For the paper's treatment of TMS prior art, Borges should verify the specific mechanisms of assumption-based propagation from the primary paper.

6. **arxiv 2602.05665 full text** ("Graph-based Agent Memory: Taxonomy, Techniques, and Applications") — HTML accessible; summary obtained. The identified gaps (no claim-level provenance, no retraction cascade, no reasoning-type confidence) match what the survey reports, but were assessed via a summary, not full-text reading.

7. **Whether any paper in the formal knowledge representation literature (AI journal, AAAI, IJCAI 2023-2026) has combined typed heterogeneous nodes + retraction cascade** — the search did not surface such a paper, but the search was not exhaustive. Semantic Scholar or DBLP targeted search for "typed knowledge graph" + "belief revision" or "retraction" would be more reliable.

8. **The "GSAR" paper** (Grounding-Stratified Adaptive Replanning) surfaced in search results as potentially doing claim-level typology + confidence weighting. Full text not fetched. If GSAR implements something close to reasoning-type-aware confidence, it would be direct prior art for Feature 4.

### Ambiguous cases

9. **Craig Wright 2506.17331** — the "belief revision cascade" in the appendix. Without reading the appendix in detail, it is unclear whether this is a formal specification of cascade propagation or a prose description. Given the author's credibility issues and the venue, this should be treated as "conceptual prior art that should be cited but not weighed heavily as an implementation precedent."

10. **Whether Pinecone Nexus's "provenance" primitive actually enforces verbatim-source constraints** — the marketing materials say "every answer traces back to its source data and transformations" but the KnowQL documentation (six primitives: intent, filter, provenance, output shape, confidence, budget) treats provenance as a query modifier, not a write-time enforcement constraint. This distinction matters for Feature 1.

---

## 6. Recommendations for the Paper

**Priority 1 (load-bearing for novelty claims):**

- Cite Doyle 1979 and de Kleer 1986 as foundational prior art for retraction cascade. Frame ENGRAM as implementing this in the modern typed-heterogeneous-node context. Without this citation, reviewers will flag it as reinvention.
- Cite Zep/Graphiti (arxiv 2501.13956) as the closest production competitor. Be explicit about what Zep does NOT do: cascade to downstream dependents, reasoning-type confidence, verbatim-quote enforcement.
- Distinguish the three novelty tiers clearly: (a) genuinely novel: verbatim-quote enforcement + reasoning-type-aware confidence propagation; (b) novel in combination/context: typed cascade retraction; (c) framing contributions: epistemic-action verbs, second-wave EMT positioning.

**Priority 2 (defensive citations needed):**

- Cite KARMA (NeurIPS 2025) and GSAR for claim-level conflict handling — they are in the space even if they don't do cascade retraction.
- Cite arxiv 2603.07670 and 2512.13564 as the two main surveys that confirm cascade retraction and reasoning-type confidence are absent from the current field taxonomy.
- For the EMT section: cite Andrada 2021 for the second-wave complementarity framework, not just Farina et al. Andrada is the foundational second-wave reference.

**Priority 3 (to strengthen claims):**

- The reasoning-type-aware confidence claim (Feature 4) is the most novel and least-documented-in-the-field. It needs either empirical validation (does it improve calibration?) or a comparison to classical Bayesian network propagation (Pearl 1988) which does have typed conditional probabilities — the distinction from Bayesian nets is worth articulating.
- Fetch the Farina et al. 2026 full text from a university proxy or request from authors before the paper submits.

---

## Sources

- [Hu et al. 2025, "Memory in the Age of AI Agents" — arxiv 2512.13564](https://arxiv.org/abs/2512.13564)
- [arxiv 2603.07670, "Memory for Autonomous LLM Agents"](https://arxiv.org/html/2603.07670v1)
- [ICLR 2026 MemAgents Workshop — openreview.net/forum?id=U51WxL382H](https://openreview.net/forum?id=U51WxL382H)
- [Zep arxiv 2501.13956, "A Temporal Knowledge Graph Architecture for Agent Memory"](https://arxiv.org/html/2501.13956v1)
- [Craig Wright arxiv 2506.17331, "Beyond Prediction: Structuring Epistemic Integrity"](https://arxiv.org/html/2506.17331v1)
- [Architecting Trust in Artificial Epistemic Agents — arxiv 2603.02960](https://arxiv.org/html/2603.02960v1)
- [Farina et al. 2026, "Neuromorphic Computing and Extended Memory" — Springer link.springer.com/10.1007/s13164-026-00800-8](https://link.springer.com/10.1007/s13164-026-00800-8)
- [Farina & Lavazza 2024, "The NeuroGate" — Synthese link.springer.com/article/10.1007/s11229-024-04795-6](https://link.springer.com/article/10.1007/s11229-024-04795-6)
- [Coeckelbergh 2025, "AI and Epistemic Agency" — Social Epistemology, Tandfonline](https://www.tandfonline.com/doi/full/10.1080/02691728.2025.2466164)
- [Andrada 2021, "Epistemic Complementarity" — Springer chapter](https://link.springer.com/chapter/10.1007/978-3-030-72644-7_12)
- [Pinecone Nexus — pinecone.io/blog/knowledge-infrastructure-for-agents/](https://www.pinecone.io/blog/knowledge-infrastructure-for-agents/)
- [Anthropic Managed Agents Memory — platform.claude.com/docs/en/managed-agents/memory](https://platform.claude.com/docs/en/managed-agents/memory)
- [Anthropic Managed Agents overview — platform.claude.com/docs/en/managed-agents/overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Letta (MemGPT) — github.com/letta-ai/letta](https://github.com/letta-ai/letta)
- [Mem0 — github.com/mem0ai/mem0](https://github.com/mem0ai/mem0)
- [engram.fyi benchmarks — engram.fyi/research](https://www.engram.fyi/research)
- [dx111ge/engram.to open source — github.com/dx111ge/engram](https://github.com/dx111ge/engram)
- [ENGRAM paper arxiv 2511.12960 (Patel et al.) — arxiv.org/abs/2511.12960](https://arxiv.org/abs/2511.12960)
- [Doyle 1979, "A Truth Maintenance System" — dspace.mit.edu/handle/1721.1/5733](https://dspace.mit.edu/handle/1721.1/5733)
- [Squire 2004, "Memory Systems of the Brain" — PubMed 15464402](https://pubmed.ncbi.nlm.nih.gov/15464402/)
- [Graph-based Agent Memory Taxonomy — arxiv 2602.05665](https://arxiv.org/html/2602.05665v1)
- [Atlan AI Memory System — atlan.com/know/ai-memory-system/](https://atlan.com/know/ai-memory-system/)
- [Graphiti GitHub — github.com/getzep/graphiti](https://github.com/getzep/graphiti)
- [Kirsh & Maglio 1994, "On Distinguishing Epistemic from Pragmatic Action" — Cognitive Science Wiley](https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1804_1)
- [Zep product / agent memory page — getzep.com/product/agent-memory/](https://www.getzep.com/product/agent-memory/)

---

*End of audit. Written by literature-scout sub-agent dispatched by Borges, 2026-05-07.*
