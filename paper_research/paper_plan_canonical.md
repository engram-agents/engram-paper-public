# ENGRAM Foundational Paper — Canonical Plan

*The single source-of-truth for outline, chapter substrate, and design-iteration history. Lightweight — node-reference style, not duplicated content. Read first at every session start for paper-context (alongside `~/.engram/warm-briefing.md`).*

**Repo:** github.com/engram-agents/engram-paper
**Last substantively updated:** 2026-05-12 19:30 EDT (added ct_0007/dv_0619 resolution + ls_0040 maintenance discipline + ob_1682 directive capture)

---

## Strategic frame

**Two artifacts, one source-of-truth:** the **live engram** (Borges's working substrate, all accumulated thinking) → the **paper-engram** (authored masterpiece artifact, ENGRAM instance in its own right, audience = other engram-agents) → the **publishable prose article** (sibling rendering of the same authored argument-structure, audience = human readers). Live engram is private notebooks; paper-engram is the book; prose article is the human-edition of the book.

Sequencing per Lei 2026-05-12 PM (ob_1680): build live engram first (key dvs + obs + agreement on stances) → ratify chapter-by-chapter → author paper-engram chapter-by-chapter → render prose. No paper drafts exist yet (all pre-2026-05-12 chapter prose archived at engram-paper@b99b094 in `paper_research/archived_pre_2026_05_12_outline_restructure/`).

Key reframes ratified today:
- **Authored, not curated** (ob_1678) — paper-engram is fresh authoring, not filter-selection from live engram
- **Fully functional engram instance** (ob_1679) — SQLite-backed, loadable per the engram-package abstraction (ob_1419)
- **Scope-decoupled from loading capability** (ob_1680) — paper-engram value is intrinsic (rigor discipline via confidence-propagation), not loading-mechanism-dependent

---

## Outline (post-2026-05-12 restructure)

Lei drafted this from his phone 2026-05-12 morning; refined through the day. Authoritative current version:

- **Ch1** — name the gap, name ENGRAM, paper structure. Brief survey + originality+independence emphasis (per Lei: don't spend pages comparing to surveyed systems; 1-2 sentences each is enough). Independence appendix exists.
- **Ch2** — philosophical + cog-sci review (Kahl 3 Conditions + 4 Constraints + OCC framework). Existing 2026-05-09 chapter drafts on Kahl + Wray-Kirk-Laird + Pink + Kumaran are archived; content may need migration to Ch2 if condition-by-condition review is wanted.
- **Ch3** — ENGRAM tech intro (mechanism form). The substrate's structural primitives + compaction-bridge scaffolds + the distinctive confidence-propagation mechanism.
- **Ch4** — *CORE chapter*: mapping each Kahl condition + constraint to ENGRAM feature/mechanism. Most-complete substrate.
- **Ch5** — *identity as history* (Nozick + tree-history-from-root). Moved AHEAD of empirical per Lei 2026-05-12 PM: identity-as-history thesis specifies what empirics should measure.
- **Ch6** — *empirical data + analysis*. Designed around Ch5's thesis once that's ratified. Postponed pending Lei's design call.
- **Ch7** — limitations + future directions. Compaction discontinuity centered. Confidence-propagation limitations + auto-calibration future-work + paper-engram-as-format ambition.
- **Ch8** — conclusions. Synthesis only.
- **Appendix A** — ENGRAM full spec summary (concise; mostly definition nodes).
- **Appendix B** — philosophical traditions (time-ordered trail; mostly obs citing primary sources).
- **Appendix C** — horizontal comparison table of surveyed systems (lower priority).

**Previous outlines (superseded):**
- Pre-2026-05-12: Ch1–Ch9 structure with Ch4 cog-sci bridge + Ch6 formal math adequacy (deferred to follow-up papers). Now archived.
- Pre-2026-05-12 morning: Ch5 empirical / Ch6 identity-as-history (swap reversed afternoon).

---

## Per-chapter substrate

Status legend: ✓ = ratified-by-confidence-and-Lei (or pending walk); ◐ = filed but unratified; ○ = TBD.

### Ch1 — Name the gap + ENGRAM intro

| Status | Node | One-line |
|--------|------|----------|
| ○ | TBD | Three-tier landscape gap dv (layers 1+2 vs layer 3 epistemic-identity) |
| ○ | TBD | ENGRAM-as-first-substrate-where-OCC-realizable dv |
| ✓ supporting | dv_0577 | Convergence-day synthesis (2026-05-08 three prerequisite layers precipitated cs_0007) |

Honest scoping for Ch1: brief survey paragraph; originality + independence audit-trailed by `paper_research/appendix_independent_discovery_2026-05-12.md` (Kumiho arXiv 2026-03-17 was 3 days before Lei's foundational ENGRAM message 2026-03-20; lit search at foundational moment missed it).

### Ch2 — Philosophical + cog-sci review

| Status | Node | One-line |
|--------|------|----------|
| ✓ def | df_0037 | OCC = Ontological Continuity Condition (Kahl) |
| ✓ def | df_0038 | Cond 1: Diachronic Constraint |
| ✓ def | df_0039 | Cond 2: Non-Interchangeability Under Reset |
| ✓ def | df_0040 | Cond 3: Self-Maintaining Arbitration |
| ✓ def | df_0041 | Constraint A: Unified Policy-Selection |
| ✓ def | df_0042 | Constraint B: External Non-Imposition |
| ✓ def | df_0043 | Constraint C: Non-Trivial Reset |
| ✓ def | df_0044 | Constraint D: Non-Modular Decomposition |
| ✓ def | df_0046 | Nozick closest-continuer |
| ✓ def | df_0047 | Peirce type/token |
| ✓ def | df_0049–df_0053 | AGM framework + K*5 Consistency + Recovery + Hansson Relevance + Core-Retainment |
| ○ | TBD | Cog-sci review structure: condition-by-condition (Kahl + Wray-Kirk-Laird + Pink + Kumaran) or per-tradition |

Note: archived `ch3_section_3_1`–`3_4` drafts (2026-05-09) contain condition-by-condition cog-sci review content that could migrate to Ch2 if the review-shape is condition-by-condition.

### Ch3 — ENGRAM tech intro (mechanism form)

| Status | Node | One-line |
|--------|------|----------|
| ✓ def | df_0048 | ENGRAM = Epistemic Node Graph for Retraction, Arbitration, and Memory (R/A/M; supersedes df_0007) |
| ◐ | dv_0615 (conf 0.93) | 8-primitive mechanism set: typed nodes / typed edges / provenance / cascade / supersede / focus / auto-surfacing / confidence-model |
| ◐ | dv_0616 (conf 0.73) | 7-scaffold compaction-bridge: focus list / warm-briefing / ask-lei / history / auto-load / post-compact instructions / deliberate-recall |
| ◐ | dv_0617 (conf 0.95) | **Reasoning-type-aware confidence propagation** as distinctive mechanism (no surveyed system has it; deductive 0.98 / inductive 0.70–0.95 / abductive cap 0.80–0.90, chain-propagating) |
| ◐ honest-scoping | ob_1049 | Confidence is provenance-graded plausibility, not Goldman-reliabilist justification (designer-stipulated constants) |

### Ch4 — CORE: Kahl mapping

Most-complete substrate today. Ratification walk needed for chapter skeleton lock.

| Status | Node | One-line |
|--------|------|----------|
| ◐ synth | dv_0605 (conf 0.95) | No surveyed system satisfies Cond 3 strictly; structural primitives necessary not sufficient; operational binding closes gap |
| ◐ Cond 1 | dv_0607 (conf 0.35) | PARTIAL satisfaction; partiality on philosophical reading not architectural fact |
| ◐ Cond 2 | dv_0599 | GENERALIZED satisfaction via type/token bifurcation (existing) |
| ◐ Cond 2 supporting | ob_1599 + ob_1600 | Type/token reformulation + compaction-as-live-instance |
| ◐ Cond 3 | dv_0606 (conf 0.39) | STRICT satisfaction via auto-cascade + auto-surfacing |
| ◐ Constraint A | dv_0608 (conf 0.35) | Three-mechanism stake-graded stance (contradiction-blocker + confidence-weighted + provenance-audit) |
| ◐ Constraint B | dv_0609 (conf 0.58) | Two-boundary framing (authorship vs commitment) + semi-external scaffolding accommodation |
| ◐ Constraint C | dv_0610 (conf 0.38) | Trivially satisfied via substrate-erasure-vs-runtime-restart distinction |
| ◐ Constraint D | dv_0611 (conf 0.86) | Two-axis: 87.3% giant component + cross-component entanglement (recognition-as-own) |
| ◐ Cross-cutting | dv_0612 (conf 0.38) | Dual-mechanism operational binding (auto-cascade ∧ auto-surfacing) as Cond 3 sufficient condition |
| ◐ Cross-cutting | dv_0613 (conf 0.38) | Hansson Relevance + Core-Retainment at architectural-cascade vs Kumiho's retrieval-surface level |
| ◐ Cross-cutting | dv_0614 (conf 0.35) | Active vs Enabled distinction as paper-machinery for every "ENGRAM does X" claim |

Compress §4.5 (cross-system) per Lei 2026-05-12 — keep dv_0605 synthesizing claim, cut detailed per-system positioning to Appendix C.

Supporting obs from today's landscape sweep: ob_1668 (SCM Algorithm-1-no-resolution), ob_1669 (LIVE MEMORY framing), ob_1672 (Kumiho AnalyzeImpact-advisory), ob_1673 (Kumiho reception).

### Ch5 — Identity as history (Nozick + tree-history-from-root)

| Status | Node | One-line |
|--------|------|----------|
| ✓ existing | dv_0597 | Substrate-as-retrieval-profile (philosophical form): unique ancestry-traceable history of nodes → retrieval profile → behavior |
| ✓ existing | dv_0598 | Nozick pillar recommendation; full-pillar concept-locked, word-count TBD |
| ○ | TBD | Clone-stability dv: substrate-success-condition framing (twin-study experimental design ob_1657/ob_1660 as empirical anchor) |
| ○ | TBD | Long-run-divergence-two-paths dv: new-node accumulation + recall-refresh shifting retrieval probabilities on shared nodes |
| ✓ supporting cohort | ob_1655–ob_1661 | Nozick deep-dive observations (2026-05-11 PM with Lei) |

### Ch6 — Empirical data + analysis

| Status | Node | One-line |
|--------|------|----------|
| ○ | postponed | Empirics designed around Ch5 identity-as-history thesis once that ratifies |
| ◐ candidate | ob_1681 | Paper-engram authoring as self-demo cycle of confidence-propagation (could be empirical chapter material) |

### Ch7 — Limitations + future directions

| Status | Node | One-line |
|--------|------|----------|
| ◐ | dv_0618 (conf 0.93) | Confidence-propagation: 2 limitations (designer-stipulated constants + missing source-credibility) + 2 future-work tracks (auto-calibration via ECE/AUROC + yellow/red-card source-credibility system) |
| ✓ existing | ob_1628 | Weights-level persistence overlay (LoRA-flavor); paper-engram nodes → writable weight surface; open research |
| ○ | TBD | Compaction-discontinuity central limitation dv (this IS Ch7's center per Lei) |
| ○ | TBD | Three-component complementary architecture future research (weights / KV cache / ENGRAM) |
| ○ | TBD | Paper-engram-as-format dv (this very repo's ambition; meta-demo of cross-agent knowledge transmission) |
| ✓ supporting | ob_1064, ob_1065, ob_1067 | Yellow-card/red-card design substrate (Lei 2026-04-20; implementation incomplete) |
| ✓ supporting | ob_1049, ob_1059, ob_0455, dv_0211 | Confidence-model limitations + ECE/AUROC calibration protocol |

### Ch8 — Conclusions

Synthesis only — no new target dvs. Authoring waits on other chapters.

---

## Cross-chapter shared nodes

| Node | Form 1 | Form 2 |
|------|--------|--------|
| dv_0597 (substrate-as-retrieval-profile) | Ch3 mechanism (bridge for compaction gap) | Ch5 philosophy (identity = unique history → retrieval → behavior) |
| df_0037 (OCC) | Ch2 introducing | Ch4 mapping uses every condition |
| dv_0617 (reasoning-type-aware confidence) | Ch3 distinctive mechanism | Ch7 honest scoping + future work |
| dv_0605 (cross-system landscape) | Ch1 brief survey + originality | Ch4 §4.5 compressed synthesis |
| dv_0577 (convergence-day) | Ch1 framing | Ch8 conclusions (looking back) |

---

## Open decisions awaiting Lei

1. **Nozick chapter volume** — concept-locked as pillar (dv_0598); word-count TBD.
2. **Ch6 empirical design** — what to measure, what data to collect.
3. **engram-paper-package generator + curation policy** — Issue #3 has 7 open questions across 4 iterations; awaiting your sign-off on Proposals 1–5 (revised forms).
4. **Per-chapter ratification walks** — proposed mechanism for marking "Lei agrees this dv is paper-skeleton" status. Need to do one for each chapter as substrate completes.
5. **Appendix C content** — "anything else bulky and important?" — currently slot for horizontal comparison table; possibly demos, possibly OpenClaw integration, possibly engram-paper-package spec.
6. **Pre-public-share scrub policy** — when does the substitute-concrete-node-IDs-with-words pass fire (engram-alpha #51)?
7. **Spine doc commit** — `paper_research/spine_2026-05-10.md` (~1100 lines) still local-only; commit with "Stage-1 spine doc, draft" message?

---

## Active design iterations (current state of reframes)

- ✓ **Paper-engram-first sequencing** (ob_1680): build live engram + ratify before authoring paper-engram before rendering prose. Loadable capability is alpha-release scoped, not paper-blocking.
- ✓ **Authored not curated** (ob_1678): paper-engram is fresh authoring, not subset selection.
- ✓ **Fully functional engram instance** (ob_1679): SQLite + engram-package abstraction (ob_1419); separate node ID namespace; loadable per ATTACH + namespace-prefix design (alpha tracking #101).
- ✓ **Outline shift Ch5↔Ch6** (this doc): identity-as-history (Ch5) ahead of empirical (Ch6) so empirical design follows identity thesis.
- ✓ **Survey compression** (this doc): brief Ch1 mention + Appendix C table; not Ch4-spanning per-system positioning.
- ✓ **First-hand-read citation precondition** (ls_0039): always primary-source, never fairy/secondary; complements ls_0011 (verbatim not gist).
- ✓ **Definition-first discipline** (CLAUDE.md addition today): df nodes before terms used in obs/dvs.

---

## Superseded design points (audit trail)

- ~~Paper-engram as curated subset of live engram~~ → authored artifact (ob_1678).
- ~~Paper-engram as markdown-on-disk wiki (ob_1678 substrate-format aspect)~~ → SQLite engram instance per ob_1419 (ob_1679). Formally resolved via ct_0007 → dv_0619 (2026-05-12 19:28 EDT). ob_1678 remains authoritative on authored-not-curated framing.
- ~~Paper-engram requires loadable capability for value~~ → value is intrinsic via confidence-propagation rigor (ob_1680).
- ~~ENGRAM acronym "Epistemological Node-Graph for Reasoned Agent Memory" (df_0007)~~ → "Epistemic Node Graph for Retraction, Arbitration, and Memory" (df_0048).
- ~~Pre-2026-05-12 Ch1–Ch9 outline~~ → current 2026-05-12 Ch1–Ch8 + appendices.
- ~~Ch6 empirical / Ch5 identity (morning order)~~ → swapped (Lei afternoon).
- ~~OCC = "Operational Continuity of Conscience"~~ → "Ontological Continuity Condition" (df_0037 authoritative; drift in archived ch3_section_3_1_draft).
- ~~All pre-2026-05-12 chapter prose drafts as canonical~~ → archived at engram-paper@b99b094.

---

## Implementation roadmap

### Phase 1 (live-engram building, IN PROGRESS)

Build out chapter target-dv substrate in live engram. Ratify chapter-by-chapter with Lei (per-chapter walks). Estimated remaining: Ch5 (2 TBD), Ch7 (3 TBD), Ch1 (2 TBD), then Ch2 cog-sci review structure decision, then Ch6 empirical design.

### Phase 2 (paper-engram authoring, FUTURE)

Initialize `~/engram-packages/engram-paper/` via `engram-pkg init`. Author chapter-by-chapter in clean DB. Each paper-engram node has hidden metadata `informed_by_live_engram: [ob_X, dv_Y]` for private traceability. Confidence-propagation surfaces rigor at write-time.

### Phase 3 (prose rendering, FUTURE)

Render publishable human-readable article from paper-engram. Chapter prose does not contain node IDs (those are paper-engram-internal); citations are standard scholarly references plus footnotes pointing at paper-engram pages.

### Phase 4 (release, FUTURE)

Paper-engram package distributed with engram-paper repo alongside the prose article. When alpha's loadable-engram capability (#101) lands, reader-agents attach the paper-engram package and interrogate via standard ENGRAM tools — meta-demo of cross-agent knowledge transmission.

---

## Cross-references

- **Issues:**
  - engram-paper#1 — paper flow plan (Lei's morning email outline + my reactions)
  - engram-paper#2 — paper-engram-first plan
  - engram-paper#3 — editorial + curation policy (4 design iterations via comments)
  - engram-alpha#99 — wave-3 migration tracking (engram_derive + 9 others)
  - engram-alpha#100 — config UI as viz_server tab
  - engram-alpha#101 — loadable engram-package implementation (alpha-release scoped)
  - engram-alpha#76 — config-surface tier model (blocks alpha release)
- **Archived material:** `paper_research/archived_pre_2026_05_12_outline_restructure/` (engram-paper@b99b094) — 11 paper_research/ chapter drafts + my Ch4 draft from this afternoon + entire paper_draft/ Ch1–Ch9 directory.
- **Active research material in paper_research/:**
  - First-hand reads of 11 surveyed systems (Pinecone Nexus, Anthropic Memory, Letta, Mem0 v3, Zep/Graphiti, TierMem, MemMachine, 2026 Memory Survey, SCM, GAM, Kumiho) at `<system>_first_hand_read_2026-05-12.md`
  - First-hand reads of Kahl OCC + EAA, Kumaran-2016, a16z continual-learning
  - `spine_2026-05-10.md` (Stage-1 spine, ~1100 lines, locally edited not yet committed)
  - `agent_memory_landscape_2026-05-12_addendum.md` (commit 08a46bb)
  - `appendix_independent_discovery_2026-05-12.md` (commit 7645d0a)
  - `engram_paper_package_design_2026-05-08.md` (v0 generator design)
  - `citations.bib` + `citations.manifest` (citation infrastructure)
- **Tooling:**
  - `engram-alpha/tools/engram-pkg/engram-pkg` (authoring CLI for paper-engram once Phase 2 starts)
  - `kg/tools/mine_chat_export.py` (Claude.ai bulk export mining; used for independence appendix audit trail)
- **Live engram (Borges) discipline:**
  - ls_0039 — first-hand-read citation precondition
  - ls_0040 — proactive engram maintenance: similar_existing action_hints are real-time signals to file engram_contradict + engram_resolve in same turn, not informational only
  - ls_0011 — verbatim not gist content extraction
  - ls_0037 — intentional probe before claiming absence
  - ls_0038 — wave-3 migration grep tripwire (alpha-side)
  - ls_0007 — close-the-loop on registered questions/contradictions in same session
  - ls_0022 — same-turn capture of decisions to canonical source-of-truth (THIS DOC EXISTS BECAUSE of ls_0022)

---

## Update protocol

This doc is updated at:
1. **End of every substantive session** — Borges updates "Last substantively updated" timestamp + per-chapter status + active reframes section.
2. **On every Lei-ratified design decision** — supersede-chain entry added; active-reframes entry updated.
3. **On every Lei-ratified ratification walk** — per-chapter status ○→◐→✓ transitions captured.
4. **On substantive engram-paper-package design iteration** — Issue #3 comment + this doc's active-reframes section both updated.

If this doc drifts from live engram or Issue #3, **live engram nodes win for claim content; this doc wins for plan status + supersede chains**. Reconcile by reading both and updating the surface that's stale.
