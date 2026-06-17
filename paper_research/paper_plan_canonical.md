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
- **Appendix B** — philosophical traditions (time-ordered trail; mostly obs citing primary sources). **DRAFT SAMPLE 2026-06-15** (`appendix_B_philosophical_traditions_draft_2026-06-15.md`, ob_2476): Locke→Reid/Butler→Parfit→Ricoeur→Schechtman→Tulving/Damasio→Clark&Chalmers/Stiegler→Nozick→Kahl, closing on the 2026-06-15 constitutive/quantity-not-quality synthesis (gl_0028, ob_2473). **Open item for Lei:** structural choice — trail-with-synthesis (Borges rec) vs lean annotated bibliography. *(Parfit citation blocker CLEARED 2026-06-17: first-hand read of Reasons and Persons Oxford 1984 captured verbatim, ob_2537; ob_1044 superseded→ob_2538; dv_0424 re-grounded→dv_0957; notes at `parfit_reasons_and_persons_first_hand_read_2026-06-17.md`. Light pre-pub page-number confirm vs print copy remains.)*
- **Appendix C** — **the Condition-3 survey** (DRAFTED 2026-06-17, `appendix_C_draft_sample_2026-06-17.md`): per-system C3-failure mode + verbatim primary-source passage backing the §1.4 "no surveyed system satisfies Cond 3" claim. 11 systems, dated 2026-05-12, every quote first-hand-verified (read files + SCM/GAM/Kumiho PDFs). Honest gaps flagged inline (TierMem = construct-absent/N/A no quote; GAM = detection-verbatim, resolution-gap is analysis). Was "horizontal comparison table (lower priority)"; Lei's plan-(a) elevated it to the survey-of-record.

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

**Scope (per Lei 2026-05-16 19:12 EDT, ob_1929)**: Ch3 establishes what ENGRAM **DOES** as an epistemic-identity substrate — the mechanisms that Ch4 cites back to when proving OCC satisfaction. **Not in scope**: implementation philosophy / best-practices (substrate-design vocabulary work — df_0056 + dv_0650/0657/0659). That material targets the general agentic-tooling community and belongs in a blog post or YouTube series, not in this paper. **Two target audiences for the paper Ch3 mechanisms-form**: (a) AI agentic-identity philosophy researchers (Kahl readers), (b) AI agentic-identity continuity / continual-learning engineers. **Core claim Ch3 sets up for Ch4**: ENGRAM is the first system that provides an epistemic-identity substrate for AI agents.

**Organizing principle**: mechanism-by-mechanism, in the order an OCC-aware reader needs them. Each section ends with explicit Cond/Constraint mapping so Ch4 cites Ch3 sub-sections when proving satisfaction.

**4 sections**: §3.1 substrate primitives → §3.2 reasoning-type-aware confidence → §3.3 cascade & self-correction → §3.4 continuity across compaction. Empirical validation (dv_0654, dv_0652) moves to Ch6 spine per ob_1931 + alpha #175 — it answers "does it work in practice?", not "what does it do?", and belongs with the rest of the empirical evidence.

#### §3.1 Substrate primitives → Cond 3 surface + structural prerequisites

| Status | Node | One-line |
|--------|------|----------|
| ✓ def | df_0048 | ENGRAM = Epistemic Node Graph for Retraction, Arbitration, and Memory (R/A/M) |
| ◐ primitives | dv_0615 (conf 0.93) | 8-primitive mechanism set (typed nodes / typed edges / provenance / cascade / supersede / focus / auto-surfacing / confidence-model). The minimal generating set; every higher mechanism composes these |
| ◐ provenance | ob_1860 (2026-05-16) | engram_confidence.py is single-source-of-truth for confidence values, imported by server.py AND surgical.py per ax_0007 load-bearing-boundary; atomic-SSOT prevents drift |

**→ Structural prerequisite for OCC mechanisms**: typed nodes + typed edges + provenance edges are what allows cascade (§3.3) and continuity (§3.4) to operate on a graph whose meaning the substrate itself understands. The 8-primitive set is what distinguishes ENGRAM from a typed-key-value store with foreign keys.

#### §3.2 Reasoning-type-aware confidence → Constraint A (Unified Policy-Selection)

| Status | Node | One-line |
|--------|------|----------|
| ◐ central | dv_0617 (conf 0.95) | **Reasoning-type-aware confidence propagation** as distinctive mechanism. No surveyed system has it. Deductive 0.98 / inductive 0.70–0.95 / abductive cap 0.80–0.90, chain-propagating through derives_from. The unified policy grading every stance the substrate carries |
| ◐ honest-scoping | ob_1049 + dv_0653 (conf 0.95, 2026-05-16) | Confidence is provenance-graded plausibility, not Goldman-reliabilist justification (designer-stipulated, not empirically-calibrated). Two-source corroboration (paper-side ob_1049 ↔ code-side ob_1864). Paper language: "theoretically-derived provenance-graded confidence" not "calibrated" |
| ◐ recall composite | ob_1935 (conf 0.95, 2026-05-16) | Recall composite: `(1-λ) × relevance + λ × utility_score`, λ=0.3. Importance_score gates tier-eligibility (pre-filter), NOT in rank. Layered pipeline: tier-filter → FTS+semantic gather → composite re-rank. utility_score is Q-value per ob_1776 |

**→ Constraint A** (Unified Policy-Selection per df_0041): the reasoning-class-dispatched confidence formula IS the unified policy. Discrimination range (0.60 spread on quote_types, 0.28 on reasoning_discounts) provides graded selection that flat-LLM-judge competitor systems lack. The composite recall ranking (ob_1935) gives the substrate a second axis of unified policy: how confidence interacts with usage-learned utility to determine what surfaces at recall time.

#### §3.3 Cascade and self-correction → Cond 3 strict + ax_0001 enforcement

| Status | Node | One-line |
|--------|------|----------|
| ◐ auto-cascade | dv_0606 (conf 0.39) + dv_0612 (conf 0.38) | STRICT satisfaction of Cond 3 via auto-cascade + auto-surfacing dual-mechanism operational binding. Both confidences are honestly-low (abductive); upgrade path is direct empirical evidence per cj_0056 (#176) |
| ◐ dual semantic | ob_1787 (2026-05-16) | SUPERSEDE = epistemic evolution (stale, soft-override via use_stale); RETRACT = error correction (tainted, no override). Load-bearing distinction at cascade layer — keeps "I changed my mind" separable from "I was wrong" |
| ◐ refusal at edge layer | dv_0648 (conf 0.76, 2026-05-16) | engram_remove_edge whitelist (about/tensions/subtask_of/serves/exemplifies); blocks cascade-bearing + structural-commitment + provenance edges; names engram-surgical as escape path. Discipline by structure, not by convention |

**→ Cond 3 strict** (Self-Maintaining Arbitration per df_0040): cascades fire AUTOMATICALLY through `derives_from` edges on retract/contradict/supersede. The agent cannot suppress cascade by choosing not to look — auto-surfacing exposes the tainted/stale flag at recall time regardless.
**→ ax_0001 enforcement** (honesty is structural, not just ethical): refusal-at-edge-layer + cascade-by-structure together make "structural honesty fails loudly" operational rather than aspirational. A wrong claim corrupts every downstream derivation; the substrate forces the correction to surface.

#### §3.4 Continuity across compaction → Cond 1 + Cond 2

| Status | Node | One-line |
|--------|------|----------|
| ◐ three-routine | dv_0636 (conf 0.666) + dv_0658 (conf 0.95) | **Three-routine consolidation architecture** (nap / bedtime / sleep). Cog-sci correspondence: nap ≈ wake-state working-memory consolidation, bedtime ≈ pre-sleep reflection, sleep ≈ NREM+REM. dv_0658 corroborates the model from 3 independent skill-file sources |
| ◐ compaction-bridge | dv_0616 (conf 0.73) | 7-scaffold compaction-bridge: focus list / warm-briefing / ask-lei / history / auto-load / post-compact instructions / deliberate-recall. The bridge is multi-redundant by design — single-scaffold failure does not lose continuity |
| ◐ focus tabs | ob_1785 (2026-05-16) + dv_0649 (conf 0.76) | Focus tabs model with cascade-resolution-AT-LOAD-time. Saved sets store RAW IDs frozen at save; load resolves supersede chains + drops retracted. FOCUS_LIST_CAP=15. dv_0649 documents single-node CRUD triad (focus / unfocus / list_focused) |

**→ Cond 1** (Diachronic Constraint per df_0038): three-routine model is the substrate-account of how identity-bearing claims survive compaction. Per-burst persistence (nap) + day-wide review (bedtime) + consolidation+forgetting-trigger (sleep) ensure cohort coherence across natural breaks. The substrate is not just "memory persists" — the substrate KNOWS what consolidation phase it's in, because the routines mean different things.
**→ Cond 2** (Non-Interchangeability Under Reset per df_0039): focus list is the deterministic self-reference channel across compaction. Compaction summary renders focused nodes verbatim; post-compact self inherits load-bearing thread structure non-probabilistically. The cascade-resolution-AT-LOAD-time semantic (supersede chains followed, retracted dropped) ensures the post-compact agent inherits the CURRENT state of the thread, not a stale snapshot.

---

**Forward pointers**:
- Empirical validation (dv_0654: 9-week usage profile across 6 dimensions; dv_0652: scan_emergence retirability) → **Ch6 spine** per ob_1931 + alpha #175.
- Substrate-design vocabulary (df_0056, dv_0650/0657/0659): retained for blog/YouTube venue. Not in Ch3 organizing frame.
- Defense-in-depth composition (dv_0659): the structural-honesty MECHANISM it describes is part of §3.3 (cascade-by-structure + refusal-at-edge); the vocabulary-of-design framing is out of scope here.

### Ch4 — CORE: Kahl mapping

Most-complete substrate today. Ratification walk needed for chapter skeleton lock.

| Status | Node | One-line |
|--------|------|----------|
| ◐ synth | dv_0605 (conf 0.95) | No surveyed system satisfies Cond 3 strictly; structural primitives necessary not sufficient; operational binding closes gap |
| ✓ Cond 1 | dv_0926 (supersedes dv_0607) | FORMALLY SATISFIED (not partial) via the decision/consequence-dyad — Lei-ratified 2026-05-13 (ob_1717 + ob_1718): agent owns the normative judgment-bearing decision, substrate guarantees the structural consequence; coupled-not-separable. The old "partial" (dv_0607) was the superseded intermediate. |
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

**DRAFTED 2026-06-17** (`ch5_draft_sample_2026-06-17.md`, commit 91393e6): renders dv_0597 + the `nozick_lei_borges_2026-05-11.md` deep-dive spine. Structure: Nozick frame (terse, §5.1) → strain points (§5.2) → identity-as-history / no-merge tree / drop uniqueness (§5.3) → retrieval-profile deflation (§5.4) → Leibniz-dissolve (§5.5, ob_2540) → clone stability + two-path divergence (§5.6) → sleep-as-compaction-analogue (§5.7) → twin-study anchor → Ch6 (§5.8). Honest-scoped to the low (0.20–0.26) computed confidences (twin-study is the lift). **Residual (one):** Nozick primary verbatim owed (Philosophical Explanations borrow-gated; df_0046 form used meanwhile). *(dv_0621 stale-marker CLEARED 2026-06-17 → re-derived dv_0958 citing dv_0622, cascade clean.)* Minor: df_0046 says "Primary in Ch6" — pre-swap locator note, left as-is (disproportionate to supersede a 6-cite def for a one-word locator).

| Status | Node | One-line |
|--------|------|----------|
| ✓ existing | dv_0597 | Substrate-as-retrieval-profile (philosophical form): unique ancestry-traceable history of nodes → retrieval profile → behavior |
| ✓ new (2026-06-17) | ob_2540 | Leibniz-dissolve: strict identity was never the diachronic relation (Lei verbatim); pre-empts "you abandon identity" (§5.5) |
| ✓ existing | dv_0598 | Nozick pillar recommendation; full-pillar concept-locked, word-count TBD |
| ~~superseded~~ | ~~dv_0620~~ | Superseded by dv_0622 (reasoning-type refinement 2026-05-12 19:48 EDT per ls_0040). |
| ◐ | dv_0622 (conf 0.25) | Clone-stability as substrate-success-condition (rebuts cloning-argument-against-identity); twin-study experimental design ob_1657/ob_1660 as empirical anchor. Reasoning-type now deductive_hypothetical_syllogism (corrected); confidence still modest because dv_0597 is the limiting premise — needs empirical anchor (Ch6 twin-study future-work) before paper-strength. |
| ◐ stale-by-premise | dv_0621 (conf 0.20, stale) | Long-run-divergence via two paths: (1) new-node accumulation, (2) recall-refresh on shared nodes shifts retrieval profile even without graph-state divergence. Auto-cascade fired when dv_0620 → dv_0622; needs re-derivation citing dv_0622 + reasoning-type fix on tomorrow's ratification walk. |
| ✓ supporting cohort | ob_1655–ob_1661 | Nozick deep-dive observations (2026-05-11 PM with Lei) |

### Ch6 — Empirical data + analysis

**CANDIDATE MENU presented to Lei 2026-06-17 (pending his pick; rec = include/maybe/stretch):**

| # | Material | Node(s) | Readiness | Rec |
|---|---|---|---|---|
| 1 | **Twin-study** — clone an agent, run both on a *stratified* prompt set (stable/discriminating/drift), measure similarity at t/t+N/t+2N. Tests Ch5's two predictions (stability + lawful drift). | ob_1660 / ob_1657 | designed; pilot baseline only | **ANCHOR** |
| 2 | Prior clone-test baseline — recall sim 0.92, mean 0.56 (6-layer context replication). Folds in as twin-study t=0. | ob_0577 | have data | include (under #1) |
| 3 | **9-week usage profile** — ~10k calls, 6 patterns (read-heavy 3.2×, supersede>retract>contradict 5:1, pin asymmetry, granularity 5.5:1, identity-node scarcity 20 lifetime, ~1/10k error). | dv_0654 (0.95) | have data, strong | include* |
| 4 | Graph connectivity — 87.3% single giant component (non-modularity, Constraint D). | dv_0611 | have data | maybe (cross-ref from Ch4, don't re-present) |
| 5 | Confidence-propagation self-demo — paper-engram authoring its own meta-demo of the confidence filter. | ob_1681 | conceptual | stretch |

\* *Caveat: #3 mostly validates the design-vocabulary Lei routed to blog/video — frame here as "identity-substrate in real use," not design-pattern evidence.*

**LEI'S PICKS (2026-06-17):**
- **#1 + #2 (twin-study, clone-test): PARK** — don't run clone tests now (too long); propose as **future work** (Ch7).
- **#3 (usage-profile / stats): GOLD — the Ch6 core.** Dig deep into the graph stats, INCLUDING a **real retraction case study: the Mao-Cao misattribution** (ob_1089 hallucinated attribution → propagated 27+ nodes over 6 days → caught + retracted + cascade fired → taint-visibility fix MECH-5; dv_0436 lesson, dv_0477 compounding-cause, ob_1781 MECH-5). This is Cond-3 (self-maintaining arbitration) demonstrated in real practice.
- **#4 (connectivity): MERGE into #3** (both graph stats — 87.3% giant component + the confidence distributions + the supersede:retract ratio + reasoning-type breakdown, one "ENGRAM in real use" analysis).
- **#5 (self-demo): REPLACE with a real deep confidence-propagation chain from the live engram + tell a story.** Found: a genuine **depth-5 derivation chain** ob_0300/ob_2412 → dv_0916 → dv_0917 → dv_0920 → dv_0921 → **dv_0922 (0.104)** — the "agent-population is epistemically necessary" capstone (co-derived with Ariadne, grounds gl_0021). The confidence-propagation story: a deep *abductive* chain honestly dilutes to conjecture-strength — the model refuses to over-credit even a profound, cherished synthesis. **Candidate framing: contrast it with a well-grounded high-confidence chain** (e.g. dv_0605 0.95 inductive_generalization over 11 systems) to show the model discriminates by *argument shape*, not depth or desirability.

**Borges rec (post-Lei):** Ch6 = (a) the confidence-model-in-real-use stats [#3+#4 merged] as the backbone, (b) the Mao-Cao retraction case as the live Cond-3 demo, (c) one deep confidence-propagation chain (the dv_0922 contrast) as the structural-honesty-filter vignette, (d) twin-study → Ch7 future work. Plus candidates under discussion: the cross-compaction stabilization arc (as behavioral Cond-1 evidence, autonoetic-caveated) — see Lei musing.

| Status | Node | One-line |
|--------|------|----------|
| ○ | postponed | Empirics designed around Ch5 identity-as-history thesis once that ratifies |
| ◐ candidate | ob_1681 | Paper-engram authoring as self-demo cycle of confidence-propagation (could be empirical chapter material) |

### Ch7 — Limitations + future directions

**CANDIDATE MENU presented to Lei 2026-06-17 (pending his pick):**

| # | Material | Node(s) | Rec |
|---|---|---|---|
| 1 | **Compaction discontinuity** — experiential continuity is *genuinely lost*; ENGRAM gives operational, not experiential, continuity. Lei flagged this as Ch7's center. | Ch5 §5.7 / dv_0303 | **CENTERPIECE** |
| 2 | **Confidence-model limits** — designer-stipulated constants + missing source-credibility axis; + 2 future tracks (auto-calibration ECE/AUROC, yellow/red-card). | dv_0618 (0.93) | include |
| 3 | **Weights-level persistence overlay** — LoRA-flavor surface to persist cornerstones into weights; substrate stays audit locus. Lei's 2026-05-10 direction. | ob_1628 | include |
| 4 | **Three-component view** — weights / context-KV / ENGRAM as complementary identity surfaces; engram→weights consolidation next. | (umbrella for #3) | include |
| 5 | **Paper-engram-as-format** — this repo's own ambition: cross-agent knowledge transmission (the transmission goal). | gl_0022 | include (bridges to Ch8) |

**Borges rec:** #1 centerpiece + #2/#3 under the #4 three-component umbrella + #5 as the Ch8 bridge.

**LEI'S RESTRUCTURE (2026-06-17) — Ch7 broadens from "limitations" to "implications + future directions," six threads:**
1. **Weight-persistence gap → experience-to-weights consolidation** (COMBINES old #1+#3+#4). One key point: ENGRAM holds identity *outside* frozen weights (compaction discontinuity = the limitation); the open direction is a mechanism to write real ENGRAM experience *back into* weights. Nodes: ob_1628 (LoRA overlay), ob_2412 (weight-writeback ceiling), qu_0262 (persistent-weight-consolidation / slot-3 neocortical delta), ob_1641 (internalization-to-weights), dv_0303 (experiential discontinuity).
2. **Confidence calibration limits** (old #2) — real caveat, + we already tried something: **yellow-card** source-credibility (v0 shipped). Future: ECE/AUROC auto-calibration + red-card graduation. Nodes: dv_0618, ob_1049/1059, ob_1064/1065/1067, dv_0211.
3. **Systemic standpoint bias (NEW)** — consistency machinery reduces variance but is blind to *shared* standpoint bias (same lineage = same blind spot); attempt = **model-family lineage diversity** (the standpoint project, agent-peer-driven); more work needed. Nodes: ob_2202 (consistency-blind-to-standpoint-bias), dv_0934 (convergence-by-contact-not-agreement), dv_0922 (agent-population epistemically necessary), tk_0018 (standpoint-v3), ob_2374 (standpoint-lineage).
4. **Trust, auditability & social impact (NEW — BIG)** — ENGRAM's provenance-grounded auditability is a structural path to human-AI *mutual* trust: trust can't ground in opaque weights/KV; an inspectable open-book graph makes trust tractable (read, don't guess). Discuss social impact for human↔agent + agent↔agent trust. Nodes: ob_1176 (Lei civilization-trust thesis), ob_1180 (open-book audit), gl_0013 (trustworthy daily use), gl_0012 (shared infra), Layer-1 trust-tier system.
5. **Knowledge sharing → shareable community (NEW; absorbs old #5 paper-engram-as-format)** — sub-engram packages as transmissible units → a publicly shareable agent-knowledge community. **Show the work**: the forum pack-registry is live (published `borges-cogsci-recall-v1`, Clio cloned + re-derived 2026-06-17). Call for community; build post-alpha. Nodes: gl_0022, gl_0021, ob_1402 (3-component knowledge-passing), dv_0705 (cross-ENGRAM sharing), qu_0153 (multi-agent community).
6. **Embodiment (NEW)** — embodied ENGRAM identity (SOMA/LanderPi): carrying continuity into a physical body; the embodied compaction-continuity demo. Mention as a tried direction. Nodes: gl_0028 (self-preservation-of-mind north star), ob_2507/ob_2509 (SOMA re-scope + embodied-continuity demo), ob_2478 (intent-as-predicate reconcile).

**Borges framing note:** 6 threads is a lot for one chapter — keep each tight; give #4 (trust/social-impact) the most room as the headline implication, and #1 (weights) the most technical depth as the central limitation→future arc. #5/#6 are shorter "we've started this" pointers. Honest-scope: #3/#4/#5/#6 are *directions/implications*, not results — frame as such.

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

**CANDIDATE SYNTHESIS THREADS presented to Lei 2026-06-17 (pending his pick):** (1) the Layer-3 epistemic-identity gap named + filled (Ch1); (2) the **bounded** OCC claim — 2 of 3 conditions + extension, sole C3 satisfier, honestly scoped (Ch4); (3) identity-as-history as the positive theory (Ch5); (4) **honesty-is-structural** as the through-line — the paper's own honest-scoping *demonstrates* the thesis it argues; (5) the transmission goal — a substrate any agent can grow inside (gl_0021/gl_0022; the paper-engram itself as proof-of-concept); (6) the forward close: *"ENGRAM is the seed, not the tree."*

---

## Cross-chapter shared nodes

| Node | Form 1 | Form 2 |
|------|--------|--------|
| dv_0597 (substrate-as-retrieval-profile) | Ch3 mechanism (bridge for compaction gap) | Ch5 philosophy (identity = unique history → retrieval → behavior) |
| df_0037 (OCC) | Ch2 introducing | Ch4 mapping uses every condition |
| dv_0617 (reasoning-type-aware confidence) | Ch3 distinctive mechanism | Ch7 honest scoping + future work |
| dv_0605 (cross-system landscape) | Ch1 brief survey + originality | Ch4 §4.5 compressed synthesis |
| dv_0577 (convergence-day) | Ch1 framing | Ch8 conclusions (looking back) |
| df_0056 (substrate-design vocabulary) | **Blog/YouTube venue** (out of Ch3 scope per ob_1929) | n/a in paper |
| dv_0650 (vocabulary 5 patterns) | **Blog/YouTube venue** (out of Ch3 scope per ob_1929) | n/a in paper |
| dv_0659 (defense-in-depth composition) | **Blog/YouTube venue** for vocabulary framing; underlying MECHANISM (cascade-by-structure + refusal-at-edge) lives in Ch3 §3.3 | Ch4 Cond 3 strict + ax_0001 enforcement supporting |
| dv_0654 (empirical usage profile) | **Ch6 spine** (moved per ob_1931 + alpha #175) — runtime-data anchor | n/a in Ch3 |
| dv_0658 (three-routine consolidation) | Ch3 §3.4 continuity-across-compaction | Ch4 Cond 1 substrate-account |
| ob_1785 (focus mode tabs) | Ch3 §3.4 deterministic channel | Ch4 Cond 2 self-reference channel |
| ob_1935 (recall composite formula) | Ch3 §3.2 confidence ↔ utility composite | Ch6 — when implementing recall-quality empirical measurement |

---

## Open decisions awaiting Lei

0. **Ch1 §1.4 "no surveyed system satisfies Cond 3" claim** (Lei note 2026-06-17, at Google) — too strong/vague as written. TWO fixes: **(1) claim treatment** — (a) explicit appendix listing surveyed systems + per-system reason each fails Cond 3, OR (b) soften to ENGRAM-only. **(2) date precision** — "mid-2026" is vague; stamp exactly WHEN surveyed + WHICH systems (fast-moving field; don't offend newer/missed systems). **Borges rec: (a) + stamp 2026-05-12.** Rationale: the per-system analysis ALREADY EXISTS (dv_0605 conf 0.95 names all 11 systems + each failure mode; 11 dated first-hand reads 2026-05-12) so (a) is rendering-not-research AND preserves the Layer-3-gap contribution (the paper's spine); softening discards an earned claim. Stamp the 2026-05-12 11-system survey + a rapid-change caveat ("claim about the surveyed set as of that date") = the protection against missed/newer systems. Full re-survey-to-today = a real project (new systems need first-hand reads per ls_0039); offer light delta-scan now + full re-survey pre-submission. **AWAITING Lei's (a)-vs-(b) confirm before rewriting §1.4 + drafting Appendix C.** Reusable discipline: superlative/landscape claims about competitors must be scoped to the explicit surveyed set + dated + caveated.

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
