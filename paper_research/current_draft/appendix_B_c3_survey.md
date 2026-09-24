# Appendix B — The Condition-3 Survey: Why No Surveyed System Self-Maintains Arbitration

## B.0 Scope, date, and method

**The survey.** Eleven sources — ten systems and one survey of the field — read
first-hand on **2026-05-12**: Pinecone Nexus,
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

**Synthesis.** Across the eleven sources, none satisfies Condition 3 strictly. The
conclusion is the conjunction of the verdicts above, so it holds exactly as far as each of
them does. The field has converged on the structural *primitives* C3 needs (typed
edges, provenance, cascade-traversable graphs, supersede semantics — Kumiho most
fully); what is missing everywhere is the **operational binding** that makes
arbitration automatic state-change. ENGRAM's contribution is that binding (Ch4
§4.4), not the primitives.

Section numbers inside *paper-verbatim* and *paper-claimed* tags refer to the
quoted paper's own sections, not to this paper's.

---

## B.1 The near-miss: a full revision engine, but advisory

### Kumiho (arXiv 2603.17244) — **(A) advisory / opt-in**
The strongest competitor in the survey: typed `Depends_On` edges, an `AnalyzeImpact`
traversal, and *self-claimed* AGM K\*2–K\*6 and Hansson belief-base compliance. The gap
is not belief revision — it is that the cascade **advises** rather than **acts**.

**The compliance claim is theirs, recorded at the fidelity we can vouch for.** The AGM
and Hansson properties above are Kumiho's own claims about Kumiho, and its paper makes
them in two parts — a formal part, "proving satisfaction of the basic AGM postulates
(K\*2–K\*6) and Hansson's belief base postulates (Relevance, Core-Retainment)", and an
implementation part, "Automated AGM compliance testing (49 scenarios, 7 postulates)
confirms 100% operational adherence to the claimed formal properties." That structure is
careful rather than confused: the proofs are offered for the semantics, the scenarios for
the running system. **We can vouch for neither half.** We have read their paper; we have
not worked through their proofs step by step, and we have no access to their
implementation to re-run anything — and 49 passing scenarios would in any case establish
that no counterexample was found in 49 cases, not that none exists. So we record the
compliance as *claimed* rather than as established and leave it unadjudicated: nothing in
this survey turns on it, because the contrast drawn here is about **where a correction
binds**, not about whose postulates are satisfied. (On why satisfaction is the wrong
relation for *this* paper to assert of itself, see Ch3 §3.9.)

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

## B.2 Detect-but-don't-resolve

### SCM — Sleep-Consolidated Memory (arXiv 2604.20943) — **(N) no resolution**
Has a `contradicts` edge predicate and a sleep cycle, but the resolution is
promised, not implemented: the same edges that §3.2 says are "flagged for
resolution" are used in §3.5 only as a **trigger metric**.

- *paper-verbatim* (§3.2): "when a user states a preference that contradicts a
  previously stored preference, the system records a contradicts edge and **flags
  the conflict for resolution during sleep**."
- *paper-verbatim* (§3.5): "Conflict density is the ratio of contradicts edges to
  total edges in the long-term memory graph: ρ(G) = |E_contradicts|/|E|."
- *paper-verbatim* (§3.5): the sleep cycle is "implementing three distinct offline
  processes" — NREM consolidation (Hebbian strengthening plus proportional
  downscaling), REM dreaming (random-walk sequence integration), and value-based
  forgetting — presented as a state machine (Figure 2) with "the full pseudocode
  given in Algorithm 1."
- *first-hand-read finding, from the paper alone:* **none of the three described
  phases acts on a `contradicts` edge.** The edges appear in the sleep cycle only
  inside the trigger metric ρ(G), and then persist. The finding is checkable at the
  level of the whole document: the string *resolution* occurs **twice** in the SCM
  paper — once in §3.2's promise quoted above, and once in future work, listing
  "contradictory information resolution" among capabilities harder evaluations
  should test. It occurs nowhere in §3.5, §3.6, or Algorithm 1. Because SCM
  publishes its sleep cycle's complete state machine and pseudocode, this absence is
  visible *in the paper's own account*, and needs no claim about SCM's code. SCM has
  the surface appearance of structural conflict handling without the substance: no
  arbitration outcome, no cascade, no downstream taint.

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

## B.3 Resolve-by-overwrite or by-someone-else (external delegation)

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

## B.4 No claim structure to cascade through

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

## B.5 The aspiration, and the genuine absence

### 2026 Memory survey — Du et al. (arXiv 2603.07670) — **(N) named, not solved**
A survey, not a system: it names contradiction-handling as something robust systems
*need*, citing no system that does it, and proposes only *external* fixes.

- *paper-verbatim* (§7.3): "Robust systems need temporal versioning (prefer the
  newest record), source attribution (user statement > agent inference),
  **contradiction detection (flag conflicts for resolution)**, and periodic
  consolidation..." — *normative* ("need"), not descriptive ("do").
- *paper-verbatim* (their §9.3): "Future systems need external validation... uncertainty
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

## B.6 Summary

| System | C3 failure mode | Verbatim available? |
|---|---|---|
| Kumiho | **Advisory / opt-in** (revision exists, not automatic) | yes (AnalyzeImpact, Depends_On "may be") |
| SCM | No resolution (aspirational flag, trigger-only) | yes (§3.2 vs §3.5) |
| GAM | Detect-only (no resolution prose) | partial — `contradict` edge yes; resolution-gap = analysis |
| Zep/Graphiti | Ephemeral, single-edge, no cascade | yes (§2.2.3) |
| Mem0 v3 | External delegation (retrieval ranking) | yes — cleanest in survey |
| MemMachine | External delegation (recency overwrite) | yes ("most recent state") |
| Pinecone Nexus | External/undocumented; read-only consumer | yes (list-item) + analysis |
| Letta | No claim structure (strings) | yes ("just strings") |
| Anthropic memory tool | No claim structure (manual coherence) | yes ("keep... coherent") |
| Memory survey 2026 | Named as aspiration, no implementation | yes (their §7.3, §9.3) |
| TierMem | Construct absent (C3 N/A) | **none — by honest design** |

Across the surveyed set, the pattern is uniform: the field has the *primitives*
(detection, typed edges, even Kumiho's self-claimed formal AGM compliance) but stops
short of **automatic arbitration as internal state-change**. What separates ENGRAM is
operational binding (Ch4 §4.4, dv_0606/dv_0612), and it has **three** parts, not two:
the cascade marks every affected node without being asked; auto-surfacing puts those
marks back in front of the agent without an intentional reach; and the **cascade
machine drives the marked region to adjudication during sleep** — walking the
frontier in dependency order until no pending marker remains, as a mandatory phase of
every consolidation cycle.

The third part is where the contrast with the closest competitor is sharpest, and it
is worth stating plainly because the two systems fail and succeed *at the same place
in the architecture*. SCM's sleep cycle is **triggered by** conflict density and does
not resolve conflicts; ENGRAM's sleep cycle is **where resolution happens**. Both
systems reached for the same biological analogy and put conflict handling in the
offline phase; only one of them closes the loop there.

One precision, since overclaiming here would repeat the very error this appendix
charges to others: ENGRAM's machine does not decide what is *true*. It finds what
needs deciding, orders the decisions so that none rests on a premise still awaiting
its own, computes what can be computed, and puts each remaining judgement to the
agent. The claim is that no affected node stays quietly unexamined — not that
arbitration happens without a mind.
