# Agent-Memory Landscape — 2026-05-12 First-Hand-Read Addendum

**Companion to:** `agent_memory_landscape_2026-05-05.md` (the original second-hand scan).
**Built from:** the 11-system first-hand-read sweep dispatched 2026-05-12 morning, with results in `<system>_first_hand_read_2026-05-12.md` per system. Source PDFs for SCM/GAM/Kumiho committed at `source_pdfs/`.
**Purpose:** Where the 5-12 first-hand reads materially change or sharpen claims in the 5-05 scan. Original is preserved for historical record; this addendum is the canonical state as of 2026-05-12.

---

## Cross-cutting headline

**No surveyed AI-agent-memory system satisfies Kahl OCC Condition 3 (`df_0040` Self-Maintaining Arbitration) strictly.** Synthesized in `dv_0605` (confidence 0.949, inductive_generalization across 11 systems). The structural primitives Cond 3 requires (typed reasoning edges, cascade infrastructure, supersede semantics) have converged across the field — Kumiho most prominently has every primitive ENGRAM has — but no surveyed system makes arbitration automatic state-change within the unified deliberative architecture. The differentiating layer is operational binding (auto-cascade + auto-surfacing), not structural infrastructure. Identity-scaffolding (Ch3 §3.3) is the sufficient condition that closes the necessary-but-not-sufficient gap.

---

## Per-system updates from the 5-12 reads

### Kumiho (UPGRADED from absent to most-serious-competitor)

5-05 scan didn't surface Kumiho. The 5-12 first-hand-read of arXiv 2603.17244 (March 17 2026, Young Bin Park, Kumiho Inc., 56 pages) elevates it to the **most-serious-competitor** in the surveyed field.

- **Structural primitives**: 6 typed edges (DEPENDS_ON, DERIVED_FROM, SUPERSEDES, REFERENCED, CONTAINS, CREATED_FROM), URI-based addressing (`kref://project/space/item.kind?r=N`), immutable revisions with mutable tag pointers, AnalyzeImpact for dependency-cascade discovery.
- **Formal grounding**: AGM K*2–K*6 + Hansson Relevance + Core-Retainment compliance proven; 49-scenario automated test suite 100% pass rate; principled rejection of Recovery postulate grounded in immutable versioning.
- **Empirics**: LoCoMo 0.447 four-category F1 (highest reported); LoCoMo-Plus 93.3% (vs Gemini 2.5 Pro 45.7% — 47.6pp improvement).
- **Productization**: open-source SDKs (Python/C++/Dart/MCP), commercial cloud at kumiho.io, official Claude Code plugin via `.claude-plugin/plugin.json`, web dashboard + desktop asset browser.
- **CRITICAL DIFFERENTIATOR** (`ob_1672`): cascade is ADVISORY not automatic. `AnalyzeImpact` discovers downstream dependents but the agent or human must explicitly invoke + decide per-dependent. Fails Kahl Cond 3 strict reading. ENGRAM's auto-cascade fires structurally; Kumiho's requires opt-in query.
- **Identity engagement**: governance-level only (ISACA 2025, IBM Agent Decision Records). No personal-identity philosophy (no Kahl, Nozick, Parfit).
- **Reception** (`ob_1673`): arXiv-only, not peer-reviewed; 5 org followers, 28 stars main repo; one third-party blog (Ranjan Kumar); not cited in major 2026 surveys. Active development; serious productization investment.

**Net for ENGRAM paper**: Kumiho proves the structural primitives independently (independent convergent discovery — see `appendix_independent_discovery_2026-05-12.md` for timeline). Our distinctive contribution is the operational binding (auto-cascade + auto-surfacing) plus the identity-scaffolding integration layer.

### SCM — Sleep-Consolidated Memory (UPGRADED from "closest live competitor" to "architecturally incomplete by own paper description")

5-05 scan: fairy-generated note flagged SCM as architecturally closest neighbor. The 5-12 first-hand-read of arXiv 2604.20943 (April 2026, Saish Shinde, Clyrai IP Studio, 19 pages) **sharpens this to architectural incompleteness**.

- **Structural primitives**: typed `contradicts` edges, sleep consolidation (NREM/REM), conflict-density-triggered sleep, multi-dim importance scoring, self-model node.
- **CRITICAL FINDING** (`ob_1668`, hard_data conf 0.95): **Algorithm 1 (page 18) contains ZERO references to processing existing `contradicts` edges**. NREM strengthens via Hebbian plasticity; REM filters new walks that would contradict facts; forgetting prunes low-score concepts. None of these resolve stored `contradicts` edges. The paper §3.2 phrase "flagged for resolution during sleep" is aspirational — *the sleep cycle implementation contains no resolution logic.* Contradicts edges persist indefinitely.
- **Code/product**: NOT publicly available. Page 16 verbatim: *"The source code for SCM is not publicly available at this time. The authors intend to release an open-source reference implementation upon publication of a peer-reviewed manuscript."* Single author, ~3K LOC Python, internal 8-test benchmark only.
- **Identity engagement**: Self-Model node exists but explicitly disclaims consciousness/identity. Cites Metzinger 2003 but no engagement with Kahl/Nozick/Parfit.

**Net**: SCM is the strongest evidence that the field has reached the *diagnostic shape* (typed contradiction + sleep trigger) but not the *resolution shape*. The gap is the implementation, not the design intent.

### GAM — Hierarchical Graph-based Agentic Memory (correction to 5-05 scan)

5-05 scan: flagged GAM as "no detection mechanism" — **this characterization was wrong**.

- **CORRECTION**: GAM does have `contradict` edge type. Appendix E.1's Semantic Relation & Edge Weighting Prompt explicitly lists six relations: support / contradict / coreference / causal / semantic / unrelated. LLM judges + assigns confidence 0-1.
- **Updated characterization**: detection WITHOUT resolution, not "no detection." Once a `contradict` edge is created during consolidation, nothing in the paper addresses it downstream. No retraction. No cascade. The edge persists indefinitely.
- **Productization**: NO code release. Pure academic publication (13 authors, Zhejiang/UIC/Rutgers/MBZUAI/McGill, Chinese + US NSF funded).
- **Identity engagement**: NONE (pure memory management; "agent" = LLM doing dialogue).
- **Scaling concern**: Table 10 shows F1 drops 0.65 → 0.48 as sessions grow 3 → 27.

### Mem0 (MAJOR ARCHITECTURE SHIFT — 5-05 characterization invalidated)

5-05 scan: "last-write-wins overwrite" — **accurate for v2, WRONG for current v3**.

- **v3 (2026-04 algorithm refresh) is ADD-only**: no UPDATE, no DELETE. Both old and new memories survive as unrelated vector store records. Conflict resolution is **explicitly delegated to retrieval ranking + application code**.
- This makes Mem0 v3 a *cleaner OCC foil* than v2 — explicit external prescription, exactly what Cond 3 rules out as "arbitration external to the unified deliberative architecture."
- **Performance**: 91.6 LoCoMo / 93.4 LongMemEval. Strong retrieval baseline; use these numbers to establish that retrieval quality and epistemic identity are orthogonal.
- **Identity engagement**: NONE. Identifies cross-session identity as open engineering problem.

### Anthropic Claude Memory Tool (UNDERSTATED in 5-05 scan)

5-05 scan: simple filesystem-as-memory framing — **understated capability**.

- **Managed Agents memory store** (distinct surface from Messages API tool) has: `memstore_*` IDs, API-level CRUD, **immutable memory versions** with `memver_*` IDs and 30-day retention, `redact` endpoint for compliance workflows, optimistic concurrency via `content_sha256` preconditions.
- Two distinct surfaces: Messages API `memory_20250818` (self-hosted, no built-in versioning) vs Managed Agents memory stores (full immutable version history). **Paper references should specify which surface.**
- **Still no claim structure**, no contradiction detection, no derivation graph, no cascade. All three OCC conditions still fail. But the infrastructure gap vs ENGRAM is narrower than 5-05 implied.

### Zep / Graphiti (sharpened with source-code-level evidence)

5-05 scan was directionally correct; 5-12 first-hand read sharpens to **source-code-citable** claims.

- **Cascade absence is now source-code-verifiable**: `invalidation_candidates` is populated by iterating LLM-identified edge indices, then `invalid_at` is set on those candidates only. There is NO graph traversal, NO recursive step, NO `derived_from` lookup. Confirmed in primary code, not just paper claim.
- **Contradiction is MORE ephemeral than 5-05 said**: integer indices in working memory during a single ingestion call. `EdgeDuplicate.contradicted_facts` list is **never persisted to the graph**. The only trace is the `invalid_at` timestamp on the flagged edge — which doesn't record why.
- **`fact_triple` episode type (v0.29.0, April 2026, undocumented)**: was added to the enum. May be a mechanism for direct agent-authored fact injection — bypassing conversational extraction. No docstring, no public documentation. 5-05 "fully absent agent-authoring" needs caveat: "absent as documented structured-claim authoring; undocumented `fact_triple` type may partially close this gap."
- **Provenance discipline**: episode-level (improved) ≠ quote-level (still "future work").

### Pinecone Nexus (5-05 over-attributed; correction)

5-05 scan: described "deterministic conflict resolution" as launch material — **weaker than implied**.

- "Deterministic conflict resolution" appears ONCE in the architecture deep-dive blog as a feature-list item with zero mechanism elaboration. NOT in the main announcement. Citation should point at the specific architecture blog post if used.
- **NEW (missed by 5-05)**: Pinecone Nexus has a versioning claim — "Every artifact is versioned" — in the architecture post. **No documented API access surface** for the versioning; described as internal auditability feature.
- Agent is read-only consumer; offline curation by separate "Context Compiler" agent (Cond 3 unsatisfiable by design — arbitration is external to consuming agent).

### TierMem (refinement)

5-05 scan: "no retraction" — refined to **"UPDATE behavior is underdocumented"**.

- Primary source confirms no retraction cascade. But the fate of the old Tier-1 entry after UPDATE is simply not specified in the paper. The 5-05 "overwrites" characterization is stronger than the paper supports.
- Correct characterization: "not documented" rather than "definitively overwrites."

### MemMachine (sharper non-engagement evidence)

- Postdates Kahl AGI paper (2026-04 submission vs Kahl 2026-02-24) and STILL ignores him entirely. Strong dated-evidence of the engineering-memory community not yet reading the philosophical-identity literature.
- Profile contradiction handling: "update to reflect the most recent state" — the exact architectural choice ENGRAM rejects.

### Memory Survey 2026 (refined framing)

- §7.3 contradiction-handling is **NORMATIVE not descriptive**: "Robust systems need contradiction detection" stated as aspiration with no cited implementation.
- This is **stronger evidence for ENGRAM's novelty** than a gap-naming survey citing partial solutions would be: the survey covers 4 years of literature and names the contradiction-detection-resolution-cascade space as unfilled.
- No paper across surveyed corpus cites cascade retraction.
- None of three sources (TierMem, MemMachine, survey) cite Kahl despite postdating his publications.

---

## What this addendum establishes

- **dv_0605** (the synthesizing Ch4 cornerstone) is grounded in the per-system observations above.
- **The "no surveyed system satisfies Cond 3 strictly" claim** is empirically defended with per-system primary-source quotes, not asserted.
- **Kumiho is the strongest competitor**; differentiation is on operational binding + identity-scaffolding, not structural primitives.
- **Convergent independent discovery** is the right framing (see `appendix_independent_discovery_2026-05-12.md`): the structural primitives converged independently across ENGRAM, Kumiho, SCM, GAM, engram.fyi within a few months in 2026-Q1–Q2. That convergence corroborates the shape; our contribution lies in the integration layer.

## Cross-references

- Per-system FHRs: `<system>_first_hand_read_2026-05-12.md`
- Source PDFs: `source_pdfs/`
- Independence appendix: `appendix_independent_discovery_2026-05-12.md`
- Synthesizing dv: `dv_0605` (ENGRAM)
- Identity-scaffolding observations: `ob_1668` (SCM), `ob_1669` (LIVE MEMORY framing from Lei), `ob_1672` (Kumiho), `ob_1673` (Kumiho reception)
- OCC definitions: `df_0037` (overall), `df_0038`–`df_0044` (Conditions + Constraints)
