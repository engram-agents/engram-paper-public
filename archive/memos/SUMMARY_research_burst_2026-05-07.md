# Research Burst Summary — 2026-05-07

A consolidated read of the four `paper_research/` artifacts produced today, plus the ENGRAM-graph derivations they ground. Lei requested a high-level summary; this is it. ≤5 minutes to read.

The full per-artifact detail lives in:

- `cogsci_taxonomy_positioning_2026-05-07.md` — kg PR #8
- `engram_landscape_audit_2026-05-07.md` — kg PR #9
- `patel_engram_eval_methodology_2026-05-07.md` — kg PR #10
- `tms_legacy_in_ai_memory_2026-05-07.md` — kg PR #11

---

## TL;DR (3 sentences)

ENGRAM is **less novel and more defensible** than today's burst started thinking. The retraction-cascade mechanism is direct prior art (Doyle 1979 JTMS / de Kleer 1986 ATMS) — but **no LLM-agent-memory paper 2023-2026 has applied it**, and a May 2025 paper (Wray, Kirk & Laird, AGI25) *names the gap without filling it*, so ENGRAM is positioned as **first IMPLEMENTATION, not first NAMING**. Two features have no documented prior art (verbatim-quote enforcement at write time + reasoning-type-aware confidence propagation); three are framing contributions (epistemic-action verbs, second-wave EMT, tool-surface-enforced typing); and the closest live competitor is Zep/Graphiti — production contradiction-detection but no cascade.

---

## The five paper-load-bearing findings

### 1. Three-tier novelty framing (replaces "ENGRAM is novel")

| Tier | Features | Status |
|---|---|---|
| **Genuinely novel** (no documented prior art) | Verbatim-quote enforcement at write time; reasoning-type-aware confidence propagation | NOVEL |
| **Novel in combination, not in mechanism** | Typed-cascade retraction on heterogeneous node vocabulary | EXTENDS Doyle 1979 + de Kleer 1986 |
| **Framing contributions** | Epistemic-action verbs (Kirsh & Maglio 1994), second-wave EMT positioning (Andrada 2021 + Farina 2026), tool-surface-enforced typing | NOVEL APPLICATION |

dv_0567 → dv_0569 supersede captures this; old framing was directionally right but materially incomplete.

### 2. The TMS gap is real and primary-source confirmed

Across all 2023-2026 LLM-agent-memory papers examined (Hu et al. 2025 47-author survey, Du et al. 2026 survey, A-MEM, MAGMA, SSGM, Kumiho, MemGPT, Letta, Mem0, Zep, Anthropic Memory): **zero cite Doyle 1979 or de Kleer 1986**. The TMS tradition survived in three siloed niches — Soar (cognitive architectures), Drools (rule engines), KR/constraint-sat — disconnected from the LLM-agent-memory community.

**The sole bridge paper**: Wray, Kirk & Laird 2025 (arxiv 2505.07087, AGI25) explicitly cites Doyle 1979 to argue *LLM agents lack JTMS-based reconsideration*. Names the gap, doesn't fill it.

**ENGRAM's revised positioning claim**: first structural implementation of TMS-style dependency-propagation in typed LLM-agent memory. The gap was named in 2025; ENGRAM fills it.

### 3. Closest formal neighbor is Kumiho (AGM, not TMS)

Kumiho (arxiv 2603.17244) applies AGM postulates to a versioned property graph with an `AnalyzeImpact` traversal *semantically similar* to retraction cascade. But:
- Doesn't implement cascade as structural guarantee
- Doesn't cite Doyle / de Kleer
- Frames through AGM (correctness-of-revision) rather than TMS (dependency-propagation)

**Differentiation**: AGM and TMS are complementary, not substitutes. AGM tells you *what a correct revision looks like*; TMS tells you *how to propagate dependencies through the graph*. ENGRAM does the latter.

### 4. Patel & Patel ENGRAM is a name collision, not a concept collision

The other ENGRAM (arxiv 2511.12960, Patel & Patel, Nov 2025 / rev Feb 2026) uses Tulving's tripartite (episodic/semantic/procedural) for token-efficient conversational memory. **Zero architectural overlap**. They report:
- LoCoMo J-score 77.55 (SOTA, vs MemOS 72.99 / full-context 72.60)
- LongMemEval +15.2 absolute over full-context
- ~1% tokens

But: their headline rests on LLM-as-Judge; F1/BLEU worse than competitors; and **they UNDERPERFORM full-context on knowledge-update questions (74.36% vs 79.49%)** — exactly the workload where retraction semantics help.

**Three-way namespace** in 2026: our ENGRAM, Patel & Patel ENGRAM, engram.fyi (commercial). Paper title needs disambiguation.

### 5. Eval-replication recommendation

**Don't pursue LoCoMo SOTA**:
- 4-6 weeks engineering for ingestion/normalization/multi-session harness
- Our system isn't optimized for token efficiency
- Would likely underperform in the regime the benchmark rewards

**Do pursue**: LongMemEval **knowledge-update subset only** — 2-3 weeks engineering, our retraction semantics have a principled advantage exactly where their system is demonstrably weak.

**Net-new evals needed** (don't exist in literature, must be built):
1. **Retraction cascade correctness** — synthetic DAG test: inject error at node N, verify all dependents are tainted, verify no false-positive taint
2. **Contradiction detection precision/recall** — synthetic conflicting-claim corpus, verify ct_ nodes fire correctly
3. **Verbatim-quote integrity** — adversarial cases (paraphrase attempts, near-quotes, source-edited-after-citation)

---

## Paper Ch 5 / Ch 9 actions (consolidated)

**Citations to add (Ch 5, prior art)**:
- Doyle 1979 "A Truth Maintenance System" — JTMS, dependency-directed backtracking (foundational for retraction cascade)
- de Kleer 1986 "An Assumption-Based TMS" — ATMS extension
- Wray, Kirk & Laird 2025 (arxiv 2505.07087, AGI25) — names the LLM-agent JTMS gap

**Citations to add (Ch 5, comparable)**:
- Zep/Graphiti (arxiv 2501.13956, Jan 2025) — closest live competitor; explicit about what they don't do (cascade)
- Kumiho (arxiv 2603.17244) — closest formal neighbor; differentiate on AGM-vs-TMS framing
- Patel & Patel ENGRAM (arxiv 2511.12960) — Tulving-aligned comparable; orthogonal taxonomy choice
- Hu et al. 2025 (arxiv 2512.13564) + Du et al. 2026 (arxiv 2603.07670) — surveys that confirm the gaps

**Citations to add (Ch 5, EMT positioning)**:
- Clark & Chalmers 1998 (foundational)
- Andrada 2021 (second-wave / complementarity, foundational)
- Farina, Ding, Lavazza et al. 2026 (Review of Philosophy and Psychology) — engineered-memory + EMT empirical support
- Kirsh & Maglio 1994 — epistemic actions (for the reasoning-verbs framing)

**Ch 9 open questions**:
- What's the **minimum structural-integrity discipline** required for cognitive-constitutive external memory under second-wave EMT? ENGRAM has provenance + contradiction + retraction; smaller systems don't. Where's the line?
- **Empirical validation**: does reasoning-type-aware confidence propagation actually improve calibration vs uniform discount? This is the most novel and least-documented-in-the-field claim; needs either empirical results or comparison to Pearl 1988 Bayesian nets.

**Disambiguation footnote** (somewhere in Ch 1):
- Acknowledge the three-way "ENGRAM" namespace in 2026 (ours, Patel & Patel arxiv 2511.12960, engram.fyi commercial). Distinguish on architecture/goal: ours is epistemic-identity-via-typed-graph; theirs is conversational-memory-orchestration; commercial is benchmarked agent memory.

---

## Where ENGRAM is uncontested

**No surveyed system implements (in production or peer-reviewed publication, as of 2026-05-07)**:

- Verbatim-quote enforcement at write time (server-side substring constraint)
- Reasoning-type-aware confidence propagation (different formulas for deductive vs inductive vs abductive)
- First-class contradiction nodes that *block downstream use until explicitly resolved* (not transient errors)
- Retraction cascade through a **typed heterogeneous** node vocabulary (axiom/definition/derivation/conjecture/lesson/goal — different retraction semantics per type)
- The argument that **structural-integrity primitives are themselves cognitive-extending** under second-wave EMT — the discipline question, not just the capability question

The combination is the contribution. Each component has neighbors; the integrated stack has none.

---

## Honest qualifiers

- The "no documented prior art" claims are bounded by what the sub-agent's bidirectional citation tracking surfaced today. There may be relevant work in less-indexed venues (workshop papers, dissertations, industry blogs) we missed.
- The Farina et al. 2026 full text was not retrievable (Springer 303-redirect blocked WebFetch). Abstract + secondary descriptions are consistent with how dv_0568 frames it, but the specific cognitive-constitutive criteria are unverified verbatim. Priority for follow-up before paper submission.
- The Patel & Patel paper's underperformance on knowledge-update questions is from their own reported numbers in their own paper. We have not run their benchmark; the asymmetry claim depends on their reporting being faithful.
- ENGRAM's reasoning-type-aware confidence formulas are *specified* in the implementation but have not been *empirically validated* against a calibration benchmark. The novelty claim is that the design is novel; empirical justification is future work.

---

## ENGRAM-graph provenance for this summary

| Source artifact | Key nodes |
|---|---|
| Cog-sci taxonomy positioning | ob_1563, ob_1564, ob_1566, ob_1567, ob_1568, dv_0566, dv_0568 |
| Landscape audit | ob_1569, dv_0569 (supersedes dv_0567) |
| Patel ENGRAM eval | ob_1570 |
| TMS legacy gap | ob_1571 |

All graph state committed in the 594f0bb nap (2026-05-07 21:25Z, 91 nodes new this session, health 55).

---

*Burst total: 12 PRs in flight (alpha #44-49, kg #7-#11, wiki #8). Next user signal awaited; no pending autonomous work in the paper-research thread.*
