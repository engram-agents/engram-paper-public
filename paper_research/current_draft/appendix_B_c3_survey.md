# Appendix C — The Condition-3 Survey: Why No Surveyed System Self-Maintains Arbitration

> **DRAFT SAMPLE — 2026-06-17.** Supplemental material backing the Chapter 1 §1.4
> claim that *no system in our first-hand survey satisfies Kahl's Condition 3
> strictly.* This appendix makes that claim auditable: it lists every surveyed
> system, names its specific failure mode, and gives a **verbatim passage** from
> the primary source (or, where the failure is one of genuine *absence*, says so
> plainly rather than manufacturing a quote). Every quote below was verified
> first-hand against the source — the arXiv papers, vendor docs, or the committed
> 2026-05-12 first-hand-read notes; the three most load-bearing (SCM, GAM, Kumiho)
> were re-confirmed against the source PDFs.

## C.0 Scope, date, and method

**The survey.** Eleven systems, read first-hand on **2026-05-12**: Pinecone Nexus,
Anthropic's memory tool, Letta (MemGPT), Mem0 v3, Zep/Graphiti, TierMem,
MemMachine, SCM, GAM, Kumiho, and the 2026 *Memory for Autonomous LLM Agents*
survey (Du et al.). This is a **bounded claim about that surveyed set as of that
date.** Agent memory is a fast-moving field; we make no claim about systems
outside the survey or released after it. Newer or missed systems are exactly why
the claim is scoped, dated, and listed rather than universal.

**The bar.** Kahl's **Condition 3 — Self-Maintaining Arbitration** (df_0040),
verbatim: *"Conflicts among commitments are resolved within a unified deliberative
architecture in a manner that preserves S's continued status as that subject."*
In operational terms a system meets C3 only if it **automatically resolves
contradictions among its own stored claims as an internal state-change** — the
cascade propagates by construction and the affected claims surface to the agent
without an intentional reach-out. Four ways to fall short:

- **(N) No resolution** — contradictions are absent as a construct, or detected
  but never resolved (the edges/flags persist).
- **(A) Advisory / opt-in** — a resolution mechanism exists but must be explicitly
  invoked, and it recommends rather than retracts.
- **(X) External delegation** — resolution is handed to retrieval ranking, recency
  rules, or application code, outside the deliberative architecture.
- **(S) No claim structure** — the system operates on text blocks with nothing to
  cascade through.

**Honest-scoping note.** Where a system's C3 failure is shown by a *positive*
design choice (delegate to retrieval, overwrite by recency, advise-don't-retract),
we quote it verbatim. Where the failure is *absence* of the construct entirely
(TierMem), or where the source documents detection but is silent on resolution
(GAM), there is no sentence to quote — we say so and rest the verdict on the
documented absence, not an invented quote.

**Synthesis node:** dv_0605 (conf 0.95, inductive_generalization over the 11
systems). The field has converged on the structural *primitives* C3 needs (typed
edges, provenance, cascade-traversable graphs, supersede semantics — Kumiho most
fully); what is missing everywhere is the **operational binding** that makes
arbitration automatic state-change. ENGRAM's contribution is that binding (Ch3
§3.3, Ch4 §4.3), not the primitives.

---

## C.1 The near-miss: a full revision engine, but advisory

### Kumiho (arXiv 2603.17244) — **(A) advisory / opt-in**
The strongest competitor in the survey: typed `Depends_On` edges, an `AnalyzeImpact`
traversal, and *proven AGM K\*2–K\*6 + Hansson compliance*. The gap is not belief
revision — it is that the cascade **advises** rather than **acts**.

- *paper-verbatim* (§6.5): "AnalyzeImpact traverses typed Depends_On edges to
  identify all downstream conclusions that **may need re-evaluation**—a capability
  enabled by the typed edge ontology that flat file systems cannot express."
- *paper-verbatim* (edge definition): "**Depends_On**: Validity dependency. If the
  target is invalidated, the source **may be** unreliable." (The modal *may be* is
  the advisory tell — not *is invalidated*.)
- *paper-verbatim* (§7.1, consistency enforcement): "deprecated items are excluded
  from all search and retrieval operations by default" — i.e. consistency is held
  at the **retrieval surface**, not by structural arbitration of commitments.
- *first-hand-read finding:* the cascade is advisory, not automatic — `AnalyzeImpact`
  *identifies* affected beliefs but does not retract them; a human or agent must
  review and decide whether to revise. **Frame the gap as advisory-vs-automatic,
  not as "no belief revision"** — Kumiho has the revision machinery; it withholds
  the automatic binding.

---

## C.2 Detect-but-don't-resolve

### SCM — Sleep-Consolidated Memory (arXiv 2604.20943) — **(N) no resolution**
Has a `contradicts` edge predicate and a sleep cycle, but the resolution is
promised, not implemented: the same edges that §3.2 says are "flagged for
resolution" are used in §3.6 only as a **trigger metric**.

- *paper-verbatim* (§3.2): "when a user states a preference that contradicts a
  previously stored preference, the system records a contradicts edge and **flags
  the conflict for resolution during sleep**."
- *paper-verbatim* (§3.6): "Conflict density is the ratio of contradicts edges to
  total edges in the long-term memory graph: ρ(G) = |E_contradicts|/|E|."
- *first-hand-read finding:* the sleep cycle (NREM/REM phases) contains **no
  resolution logic** — the "flagged for resolution during sleep" language is
  aspirational; the `contradicts` edges feed the density trigger ρ(G) and then
  persist. SCM has the *surface appearance* of structural conflict handling without
  the substance: no arbitration outcome, no cascade, no downstream taint.

### GAM — Hierarchical Graph-based Agentic Memory (arXiv 2604.12285) — **(N) detect-only**
Assigns a `contradict` edge at consolidation, but both conflicting nodes persist
and nothing arbitrates; conflict is managed by *timing*, not resolution.

- *paper-verbatim* (Appendix E.1, the relation-scoring prompt): "**contradict**: one
  memory contradicts the other (asymmetric)" — detection exists as a typed relation.
- *honest scope:* **there is no paper sentence stating GAM does not resolve** — the
  C3 failure is shown by the *presence* of a detect-only edge plus the *absence* of
  any resolution prose. First-hand-read finding: "both nodes remain in the [memory];
  retrieval ranking implicitly favors higher-confidence information, but no conflict
  resolution mechanism is documented. There is no arbitration, no automatic
  retraction, no cascade." We cite this as analysis, not as a quote.

### Zep / Graphiti (arXiv 2501.13956) — **(N) ephemeral, no cascade**
Contradiction is an ephemeral LLM classification during ingestion that invalidates
the single directly-contradicted edge; no contradiction node persists, and
entity-edges cannot reference other edges, so there is nothing to cascade through.

- *paper-verbatim* (§2.2.3): "The system employs an LLM to compare new edges against
  semantically related existing edges to identify potential contradictions. When the
  system identifies temporally overlapping contradictions, it invalidates the
  affected edges by setting their t_invalid to the t_valid of the invalidating edge."
- *first-hand-read finding:* invalidation is single-edge-only and triggered only by
  *new arriving* episodes; an agent cannot inspect its own beliefs, find a
  contradiction, and propagate a retraction. The contradiction is "not persisted as
  a node, not persisted as an edge type, and not queryable after ingestion."

---

## C.3 Resolve-by-overwrite or by-someone-else (external delegation)

### Mem0 v3 (docs.mem0.ai migration guide) — **(X) external delegation**
The single cleanest external-delegation statement in the survey. v3 is add-only;
contradictions coexist and are sorted out at read time.

- *paper-verbatim:* "**Contradictions are resolved at retrieval time through ranking
  rather than at write time.**"
- *paper-verbatim:* "Retrieval handles ranking — the most relevant, current
  information surfaces first."
- *first-hand-read finding:* conflict resolution is delegated to retrieval-time
  ranking and ultimately to application code — "exactly what Kahl's Cond 3 rules
  out: external prescription rather than self-maintaining arbitration."

### MemMachine (arXiv 2604.04853) — **(X) recency overwrite**
Profile contradictions are resolved by last-write-wins; no contradiction record, no
cascade to episodic records built on the old fact.

- *paper-verbatim:* "When new information contradicts existing profile data, the
  system can **update the profile to reflect the most recent state**—supporting the
  knowledge update capability evaluated in benchmarks."
- *first-hand-read finding:* "detect a contradiction, resolve it by overwriting, move
  on" — no first-class contradiction node, no cascade from a corrected profile fact
  to the episodic records generated using the old one.

### Pinecone Nexus (Pinecone architecture posts) — **(X)/(N), and read-only consumer**
"Deterministic conflict resolution" appears once, as an undocumented feature
list-item operating on the knowledge-compilation side; the consuming agent has no
commitment graph at all.

- *paper-verbatim* (feature enumeration): "...Typed fields. Per-field citations with
  confidence levels. **Deterministic conflict resolution.** Output shaped exactly as
  the agent specified..." — first-hand-read note: this is "the only location in the
  primary sources where 'deterministic conflict resolution' appears... a list item
  in a feature enumeration, with no further elaboration. The mechanism is not defined
  anywhere in the primary sources."
- *first-hand-read finding:* "There is no arbitration architecture in Nexus at all
  from the consuming agent's perspective. The agent queries and receives results; it
  does not maintain a commitment graph, does not detect when received content
  contradicts prior commitments."

---

## C.4 No claim structure to cascade through

### Letta / MemGPT (GitHub + letta.com docs) — **(S) text blocks**
Memory blocks are strings; edits overwrite in place; no derivation graph.

- *paper-verbatim* (letta.com/blog/memory-blocks): "memory block values are just
  strings." *paper-verbatim* (GitHub `base.py`): "The `memory_rethink` command allows
  you to completely rewrite the contents of a memory block."
- *first-hand-read finding:* "Letta has no derivation graph, no concept of downstream
  commitments, and no retraction primitive. When `core_memory_replace` overwrites a
  foundational claim, nothing downstream is flagged."

### Anthropic Claude memory tool (platform.claude.com docs) — **(S) manual coherence**
Flat free-form text files; coherence is delegated to the agent's manual effort each
session.

- *paper-verbatim:* "Note: when editing your memory folder, always try to keep its
  content up-to-date, **coherent** and organized. You can rename or delete files that
  are no longer relevant." — developer-injected *instruction* to maintain coherence by
  hand, not a structural mechanism.
- *first-hand-read finding:* "There is no mechanism for detecting when a memory file
  contradicts another memory file. There is no mechanism for identifying which
  conclusions depended on a retracted premise."

---

## C.5 The aspiration, and the genuine absence

### 2026 Memory survey — Du et al. (arXiv 2603.07670) — **(N) named, not solved**
A survey, not a system: it names contradiction-handling as something robust systems
*need*, citing no system that does it, and proposes only *external* fixes.

- *paper-verbatim* (§7.3): "Robust systems need temporal versioning (prefer the
  newest record), source attribution (user statement > agent inference),
  **contradiction detection (flag conflicts for resolution)**, and periodic
  consolidation..." — *normative* ("need"), not descriptive ("do").
- *paper-verbatim* (§9.3): "Future systems need external validation... uncertainty
  quantification... adversarial probing... and expiration policies" — the proposed
  fixes are all **external** interventions, not structural primitives. The survey
  names the C3 problem and cites zero solutions.

### TierMem — **(N) construct absent** *(no quote — by honest design)*
The C3 failure here is genuine **absence**: the paper never uses "conflict,"
"contradiction," or "inconsistency" as architectural primitives. **There is no
sentence to quote**, and we do not manufacture one. First-hand-read finding: "No
foundational-retraction-flagging mechanism exists. When a Tier-1 summary is UPDATEd,
there is no cascade to dependent summaries or downstream uses of the old content."
The paper does not specify whether UPDATE preserves or overwrites the prior entry —
we report that as *not documented* rather than asserting overwrite. Verdict: C3 is
**not applicable** — the architecture has no conflict construct to arbitrate.

---

## C.6 Summary

| System | C3 failure mode | Verbatim available? |
|---|---|---|
| Kumiho | **Advisory / opt-in** (revision exists, not automatic) | yes (AnalyzeImpact, Depends_On "may be") |
| SCM | No resolution (aspirational flag, trigger-only) | yes (§3.2 vs §3.6) |
| GAM | Detect-only (no resolution prose) | partial — `contradict` edge yes; resolution-gap = analysis |
| Zep/Graphiti | Ephemeral, single-edge, no cascade | yes (§2.2.3) |
| Mem0 v3 | External delegation (retrieval ranking) | yes — cleanest in survey |
| MemMachine | External delegation (recency overwrite) | yes ("most recent state") |
| Pinecone Nexus | External/undocumented; read-only consumer | yes (list-item) + analysis |
| Letta | No claim structure (strings) | yes ("just strings") |
| Anthropic memory tool | No claim structure (manual coherence) | yes ("keep... coherent") |
| Memory survey 2026 | Named as aspiration, no implementation | yes (§7.3, §9.3) |
| TierMem | Construct absent (C3 N/A) | **none — by honest design** |

Across the surveyed set, the pattern is uniform: the field has the *primitives*
(detection, typed edges, even formal AGM compliance in Kumiho) but stops short of
**automatic arbitration as internal state-change**. The single line that separates
ENGRAM is operational binding — auto-cascade paired with auto-surfacing (Ch3 §3.3,
dv_0606/dv_0612) — which no surveyed system, including the closest competitor,
provides.

---

**Drafting notes (for Lei):**
1. **Every quote verified first-hand** (read files + the SCM/GAM/Kumiho PDFs,
   whitespace-normalized). The two honest gaps are flagged inline, not papered over:
   **TierMem** has no quote (C3 construct absent — verdict "N/A"), and **GAM**'s
   no-resolution claim is analysis, not a paper sentence (detection *is*
   paper-verbatim).
2. **Ordering** is by narrative (closest competitor → detect-only → delegate →
   text-level → aspiration/absence), not survey order — flag if you'd rather it be
   alphabetical or grouped strictly by the four failure-mode codes.
3. **Kumiho framing** is deliberately careful: it *proves* AGM K\*2–K\*6, so the gap
   is advisory-vs-automatic, never "no belief revision." Overstating Kumiho's
   weakness is the one place this appendix could lose credibility, so it's hedged.
4. **One verification residual:** a few quotes are from vendor docs/blogs (Mem0,
   Pinecone, Anthropic, Letta) captured in the 2026-05-12 read files; the arXiv ones
   (SCM, GAM, Zep, MemMachine, Kumiho, survey) are paper-stable. Before publication,
   re-pull the vendor-doc URLs to confirm they haven't changed (docs drift); the
   arXiv quotes are fixed.
