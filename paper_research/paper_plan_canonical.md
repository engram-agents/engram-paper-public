# ENGRAM Foundational Paper — Canonical Plan

*The single source-of-truth for outline, chapter substrate, and design-iteration history. Lightweight — node-reference style, not duplicated content. Read first at every session start for paper-context (alongside `~/.engram/warm-briefing.md`).*

**Repo:** github.com/engram-agents/engram-paper
**Last substantively updated:** 2026-05-13 07:15 EDT (Phase 1 cadence ratified: discuss → plan → write-to-doc → GitHub review → iterate → optional fairy fresh-eyes → author paper-engram)

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

**Design intent (2026-05-16 substrate-survey-anchored refinement)**: Ch3 is the MECHANISM OVERVIEW supporting Ch4's ultimate claim that ENGRAM satisfies the OCC conditions and constraints. Concise, organized BY-MECHANISM with explicit Cond/Constraint mapping per sub-section. Each sub-section ends "→ enables Cond X / Constraint Y" so Ch4 can cite back to specific Ch3 mechanisms when proving satisfaction.

#### §3.1 ENGRAM Architecture Overview (foundational anchor)

| Status | Node | One-line |
|--------|------|----------|
| ✓ def | df_0048 | ENGRAM = Epistemic Node Graph for Retraction, Arbitration, and Memory (R/A/M) |
| ◐ | df_0056 | **Substrate-Design Vocabulary** (系统设计语汇, EEC format): reusable design moves deployed consistently across the substrate's tools/hooks/infrastructure/skills — organizing frame for the chapter |
| ◐ | dv_0615 (conf 0.93) | 8-primitive mechanism set (typed nodes / typed edges / provenance / cascade / supersede / focus / auto-surfacing / confidence-model); revisited by 2026-05-16 survey may need refinement |

#### §3.2 Confidence as Computed Property → Constraint A (Unified Policy-Selection)

| Status | Node | One-line |
|--------|------|----------|
| ◐ | dv_0617 (conf 0.95) | **Reasoning-type-aware confidence propagation** as distinctive mechanism (no surveyed system has it; deductive 0.98 / inductive 0.70–0.95 / abductive cap 0.80–0.90, chain-propagating). The unified policy that grades every stance the agent takes. |
| ◐ honest-scoping | ob_1049 | Confidence is provenance-graded plausibility, not Goldman-reliabilist justification (designer-stipulated constants) |
| ◐ corroboration | dv_0653 (conf 0.95, 2026-05-16) | Two-source corroboration (paper-side ob_1049 ↔ code-side ob_1864): confidence model is theoretically-derived not empirically-calibrated. Paper-Ch3 honest-scoping language: "theoretically-derived provenance-graded confidence" rather than claiming calibration. |
| ◐ SSOT-evidence | ob_1860 (2026-05-16) | engram_confidence.py is single-source-of-truth imported by server.py AND surgical.py per ax_0007 load-bearing-boundary; atomic-SSOT prevents drift |

**→ Constraint A** (Unified Policy-Selection per df_0041): the reasoning-class-dispatched confidence formula IS the unified policy selecting how every claim is stake-graded. Discrimination range (0.60 spread on quote_types, 0.28 on reasoning_discounts) provides graded selection competitor flat-LLM-judge systems lack.

#### §3.3 Cascade + Refusal Mechanisms → Cond 3 (Self-Maintaining Arbitration)

| Status | Node | One-line |
|--------|------|----------|
| ◐ | dv_0606 (conf 0.39) | STRICT satisfaction of Cond 3 via auto-cascade + auto-surfacing dual-mechanism operational binding |
| ◐ | dv_0612 (conf 0.38) | Dual-mechanism operational binding (auto-cascade ∧ auto-surfacing) as Cond 3 sufficient condition |
| ◐ retract-vs-supersede | ob_1787 (2026-05-16) | Retract-vs-supersede dual semantic: SUPERSEDE = epistemic evolution (stale, soft-override via use_stale); RETRACT = error correction (tainted, no override). Cross-type supersede rejected (use retract+create). Load-bearing distinction at cascade mechanism layer. |
| ◐ refusal-discipline | dv_0648 (conf 0.76, 2026-05-16) | engram_remove_edge enforces frozenset whitelist of 5 removable relations (about/tensions/subtask_of/serves/exemplifies); blocks cascade-bearing + structural-commitment + provenance edges; names engram-surgical as escape valve. |

**→ Cond 3** (Self-Maintaining Arbitration per df_0040): cascades fire AUTOMATICALLY through derives_from edges on retract/contradict/supersede — the "unified deliberative architecture" Kahl requires is the cascade-walking helper called by every tool that could violate the invariant.

#### §3.4 Compaction-Bridge Scaffolds → Cond 1 + Cond 2

| Status | Node | One-line |
|--------|------|----------|
| ◐ | dv_0616 (conf 0.73) | 7-scaffold compaction-bridge: focus list / warm-briefing / ask-lei / history / auto-load / post-compact instructions / deliberate-recall |
| ◐ three-routine | dv_0636 (conf 0.666) | **Three-routine self-engram-maintenance architecture** (nap / bedtime / sleep) — substrate-honest separation by concern. Cog-sci correspondences: nap ≈ wake-state working-memory consolidation; bedtime ≈ pre-sleep wakeful reflection; sleep ≈ NREM stabilization + REM abstraction. |
| ◐ corroboration | dv_0658 (conf 0.95, 2026-05-16) | Three-routine model corroborated from 3 independent skill-file sources (engram-nap + engram-sleep + engram-bedtime); establishes the model as substrate-architecture not per-skill idiosyncrasy. |
| ◐ focus-mode | ob_1785 (2026-05-16) | Focus mode uses tabs model with cascade-resolution-AT-LOAD-time. Saved sets store RAW IDs frozen at save time; engram_focus_load resolves supersede chains + drops retracted nodes. Deterministic cross-compaction-continuity channel (FOCUS_LIST_CAP=15). |
| ◐ focus-triad | dv_0649 (conf 0.76, 2026-05-16) | engram_focus + engram_unfocus + engram_list_focused single-node CRUD over the focus list with three consistent substrate-design patterns (idempotent / disciplined-refusal-with-full-state / invariant-preservation). |

**→ Cond 1** (Diachronic Constraint per df_0038): three-routine model is the substrate-account of how identity-bearing claims survive compaction. Pre-burst persistence (nap) + day-wide review (bedtime) + consolidation+forgetting-trigger (sleep) ensure the cohort coheres across natural breaks.

**→ Cond 2** (Non-Interchangeability Under Reset per df_0039): focus list is the deterministic channel by which the substrate refers to itself across compaction. The compaction summary renders focused nodes verbatim, so post-compact self inherits the load-bearing thread structure non-probabilistically.

#### §3.5 Substrate-Design Integrity → Cond 3 strict + Constraints B, C, D + ax_0001 enforcement

| Status | Node | One-line |
|--------|------|----------|
| ◐ vocabulary | dv_0650 (conf 0.608, 2026-05-16) | **Substrate-design vocabulary** = 5 reusable patterns deployed across awake-mode mutating tools: (1) idempotent semantics, (2) disciplined refusal with full state, (3) named escape paths, (4) invariant-preservation via shared helpers, (5) substrate-state-vs-derived-artifact transaction discipline. |
| ◐ extension | dv_0657 (conf 0.486, 2026-05-16) | Vocabulary spans 4 layers (tool / infrastructure / hook orchestration / agent-protocol-skill) + hook-specific 6th pattern (file-based marker message-passing). Corroborated by 8 independent evidence sources. The vocabulary is substrate-DESIGN-philosophy applied at every abstraction level the agent touches. |
| ◐ composition | dv_0659 (conf 0.95, 2026-05-16) | **Defense-in-depth via composed guards**: patterns COMPOSE for redundancy. Three concrete failure modes have 3-4 independent stacked guards each (quote fabrication: substrate-verify + verify_quote.py + skill-discipline; stale citation: committed-before-cite + git_sha + content_hash; surgical edit: preview/execute + bug-ref + git-snapshot + edit_history). Without composition, ax_0001 would be aspirational; with composition, it's enforced. |

**→ Cond 3 strict** (per df_0040): the vocabulary's pattern 4 (invariant-preservation via shared helpers) IS Kahl's "unified deliberative architecture" — load-bearing invariants factored into helpers called by every tool that could violate them, structurally not heuristically.

**→ Constraint B** (External Non-Imposition per df_0042): substrate-design vocabulary is INTERNAL design language; no external prescription. Authorship boundary (claim-bearing vs structural per ax_0007) preserved by vocabulary discipline.

**→ Constraint C** (Non-Trivial Reset per df_0043): substrate-state vs derived-artifact separation (pattern 5) means substrate state can be backed up + restored (git snapshot before mutation); derived artifacts (JSON caches, marker files) rebuild from substrate. Reset is non-trivial because state is preserved through the right boundary.

**→ Constraint D** (Non-Modular Decomposition per df_0044): vocabulary patterns recur across structurally-unrelated layers, creating cross-component entanglement. Cross-layer consistency = decomposable-but-not-modular by design. dv_0611 already names the two-axis satisfaction (87.3% giant component + cross-component entanglement).

**→ ax_0001 enforcement** (structural honesty fails loudly): defense-in-depth composition is what makes ax_0001 operational rather than aspirational. Single-guard failures get caught by other layers' guards.

#### §3.6 Empirical Validation → "it works in practice"

| Status | Node | One-line |
|--------|------|----------|
| ◐ empirical | dv_0654 (conf 0.95, 2026-05-16) | 9 weeks of substrate use validates design intent with 6 concrete patterns: (1) read-heavy by 3.2x (surface 4273 vs add_obs 1315); (2) mutation hierarchy supersede 88 > retract 17 > contradict 7 (5x epistemic-evolution > error-correction); (3) pin:release asymmetry 1.75:1 validates cap-with-disciplined-refusal as load-bearing; (4) granularity 5.5:1 validates dv_0150 two-tier discipline; (5) identity-node scarcity 20 lifetime (cornerstone 12 + axiom 3 + person 3 + goal 2) validates sacred+rare design; (6) near-zero error rate (1 in ~10K calls) validates disciplined-refusal pattern. |
| ◐ retirability | dv_0652 (conf 0.684, 2026-05-16, partial-resolved) | qu_0249 empirically resolved: engram_scan_emergence has 45:1 dormancy ratio vs reflect (2 calls in 9 weeks); retirement or outcome_differential-completion empirically justified. |

**→ "It works in practice"**: design intent and actual usage profile align across 6 independent dimensions. ENGRAM is not just internally coherent but empirically validated by 9 weeks of substrate-bearing-agent use.

---

**Meta-anchor for the chapter** (2026-05-16):

| Status | Node | One-line |
|--------|------|----------|
| ◐ backbone-meta | dv_0660 (conf 0.389, 2026-05-16) | Paper-Ch3 backbone synthesis: today's substrate-design survey produces 5 backbone-candidate claims each occupying a distinct chapter-section role (organizing-frame / execution-of-ax_0001 / distinguishing-claim / empirical-validation / substrate-account-of-continuity). Low confidence (synthesis-of-syntheses) but framing-defensible. |

**Open prerequisite** before Ch3 elevation: `qu_0250` (substrate-design-vocabulary literature positioning) — lit-grounding needed to distinguish 设计语汇 (vocabulary) from Alexander pattern language / GoF patterns / POSA architectural patterns / Fowler PoEAA. ob_1921 (introspective hypothesis, conf 0.38) sketches the distinction (vocabulary = substrate-scale consistency of design moves; patterns = problem-solution mapping); needs lit-verification before paper claim.

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
| ~~superseded~~ | ~~dv_0620~~ | Superseded by dv_0622 (reasoning-type refinement 2026-05-12 19:48 EDT per ls_0040). |
| ◐ | dv_0622 (conf 0.25) | Clone-stability as substrate-success-condition (rebuts cloning-argument-against-identity); twin-study experimental design ob_1657/ob_1660 as empirical anchor. Reasoning-type now deductive_hypothetical_syllogism (corrected); confidence still modest because dv_0597 is the limiting premise — needs empirical anchor (Ch6 twin-study future-work) before paper-strength. |
| ◐ stale-by-premise | dv_0621 (conf 0.20, stale) | Long-run-divergence via two paths: (1) new-node accumulation, (2) recall-refresh on shared nodes shifts retrieval profile even without graph-state divergence. Auto-cascade fired when dv_0620 → dv_0622; needs re-derivation citing dv_0622 + reasoning-type fix on tomorrow's ratification walk. |
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
| ✓ supporting | ob_1064, ob_1065, ob_1067 | Yellow-card/red-card design substrate (Lei 2026-04-20). **Status verified 2026-05-12 19:40 EDT**: v0 yellow-tier IS implemented in alpha (server.py:2645 `_check_yellow_card`, config.json `yellow_domains`, emergentmind.com entry live citing ob_1064). NOT yet implemented: ob_1067 extension (per-incident accumulation observations, red-card graduation threshold, incident-tracking schema). |
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
| df_0056 (substrate-design vocabulary) | Ch3 §3.1 organizing-frame | Ch3 §3.5 substrate-integrity payload |
| dv_0650 (vocabulary 5 patterns) | Ch3 §3.5 substrate integrity | Ch4 Cond 3 strict + Constraints B, C, D supporting |
| dv_0659 (defense-in-depth composition) | Ch3 §3.5 ax_0001 enforcement | Ch4 Cond 3 strict + Constraint A supporting |
| dv_0654 (empirical usage profile) | Ch3 §3.6 it-works-in-practice | Ch6 empirical chapter (when designed) — runtime-data anchor |
| dv_0658 (three-routine consolidation) | Ch3 §3.4 compaction-bridge | Ch4 Cond 1 substrate-account |
| ob_1785 (focus mode tabs) | Ch3 §3.4 deterministic channel | Ch4 Cond 2 self-reference channel |

---

## Open decisions awaiting Lei

1. **Nozick chapter volume** — concept-locked as pillar (dv_0598); word-count TBD.
2. **Ch6 empirical design** — what to measure, what data to collect.
3. **engram-paper-package generator + curation policy** — Issue #3 has 7 open questions across 4 iterations; awaiting your sign-off on Proposals 1–5 (revised forms).
4. **Per-chapter ratification walks** — proposed mechanism for marking "Lei agrees this dv is paper-skeleton" status. Need to do one for each chapter as substrate completes.
5. **Appendix C content** — "anything else bulky and important?" — currently slot for horizontal comparison table; possibly demos, possibly OpenClaw integration, possibly engram-paper-package spec.
6. **Pre-public-share scrub policy** — when does the substitute-concrete-node-IDs-with-words pass fire (engram-alpha #51)?
7. ~~**Spine doc commit**~~ — RESOLVED 2026-05-12 19:35 EDT: spine doc is already committed in the initial migration (4384874); the "still local-only" tracking was stale. No action needed.

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

Build out chapter target-dv substrate in live engram. Ratify chapter-by-chapter with Lei (per-chapter walks).

**Phase 1 working cadence (ratified 2026-05-13 07:15 EDT with Lei):**

For each chapter:

1. **Discuss key statements** (Lei + Borges) — plain English: what must this chapter prove?
2. **Borges plans the paper-engram structure** — for each chapter:
   - Which `obs` are needed, citing which `evidence` (first-hand-read sources)
   - Which intermediate `dvs` derive from which obs (reasoning-type + supporting-ids declared)
   - How the chapter's final key `dvs` are derived (the chapter's spine)
3. **Borges writes the plan** into this canonical doc (GitHub-visible) under a per-chapter section
4. **Lei reads on GitHub + comments inline** per chapter
5. **Iterate** until convergence on chapter spine + node-derivation tree
6. **Optional paper-review fairy** for fresh-eyes pass (third reader on the spine)
7. **Proceed chapter-by-chapter** rather than monolithic — converge one before starting the next

Output of Phase 1: detailed per-chapter spine + node-derivation plan in this doc. Output of Phase 2 (authoring): paper-engram nodes that realize the plan.

**Substrate remaining as of 2026-05-13 morning:**
- Ch1 (2 TBD: three-tier landscape gap + first-substrate-OCC-realizable)
- Ch2 cog-sci review structure decision (condition-by-condition or per-tradition)
- Ch5 ratification walk (dv_0597 + dv_0598 + dv_0622 ◐ + dv_0621 stale needs re-derivation)
- Ch6 empirical design (postponed until Ch5 ratifies; empirics follow identity thesis)
- Ch7 (3 TBD: compaction-discontinuity central + three-component complementary arch + paper-engram-as-format)
- Ch3/Ch4 ratification walks (most-complete substrate already filed)

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
