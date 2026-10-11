# CLAUDE.md — engram-paper Repository

*Project-level identity and discipline file for paper-drafting sessions. Auto-loaded when working in this repo. Complements the user-level CLAUDE.md at `~/.claude/CLAUDE.md` (identity, autonomy, ENGRAM write/read discipline) — this file adds the paper-drafting-specific rules accumulated through collaboration with Lei.*

**Last updated:** 2026-05-13 08:54 EDT (added Discipline M — two-level authoring: paper-engram layered/atomic first, prose rendering second)
**Repository:** github.com/engram-agents/engram-paper

---

## What this repository is for

The canonical home for the ENGRAM foundational paper. Houses three layers of artifact:

1. **Live engram nodes** — referenced via IDs, not copied. The thinking lives in Borges's personal engram at `~/.engram/knowledge.db`.
2. **Paper-engram package** — the authored masterpiece artifact, fully functional ENGRAM instance, eventually at `~/engram-packages/engram-paper/` (Phase 2 of the implementation roadmap; not started yet).
3. **Publishable prose article** — sibling rendering of the same authored argument-structure for human readers (Phase 3).

Plus research substrate: first-hand reads, spine doc, landscape addenda, citation infrastructure.

**Status as of 2026-05-12:** all chapter prose drafts archived per Lei's "we haven't written any paper drafts yet" directive (ob_1677). All work is engram-construction. No paper draft exists yet.

---

## Strategic frame

**Two artifacts, one source-of-truth** (originally; sharpened to three artifacts):

- **Live engram** — Borges's private working substrate. All accumulated thinking. Notebooks of the mind.
- **Paper-engram** — masterpiece artifact authored for external agent audience. Fresh authoring, clean systematic structure, own node ID namespace, fully functional SQLite ENGRAM instance loadable per the engram-package abstraction (ob_1419).
- **Publishable prose article** — sibling rendering for human readers.

The paper-engram and prose article are **sibling renderings** of the same authored argument; the live engram is private working material the authoring draws from but does not copy.

Sequencing per Lei 2026-05-12 PM (ob_1680): build live engram first → ratify chapter-by-chapter → author paper-engram chapter-by-chapter → render prose. No paper authorship until live engram is sufficient and ratified.

---

## Session-start reading — paper-context addition

The base session-start read list lives in `~/.claude/CLAUDE.md` (Session Start Reading section) — that's the user-level canonical source-of-truth. When working in this repo, ADD one more read:

- `engram-paper/archive/plans/paper_plan_canonical.md` — paper state (current outline + per-chapter substrate + supersede chains + open decisions). Single source-of-truth for the paper plan. Lightweight, node-reference style.

This is **additive** on top of the user-level reads, not a replacement. Don't drop user-level reads (warm-briefing, newest history file, ask-lei.md). If the project-level read list grows in the future, add here; never re-list the user-level ones.

---

## Disciplines

### A. Three-artifact framing (authored, not curated)

Paper-engram is AUTHORED, not curated subset of live engram. Live-engram nodes inform paper-engram authoring; they don't get filtered/copied in. Paper-engram has its own node ID namespace (separate DB, fresh counters). See ob_1678 (authored not curated) + ob_1679 (SQLite engram instance) + ob_1680 (scope-decoupled-from-loading-capability).

When working on paper-engram authoring (Phase 2): use `engram-alpha/tools/engram-pkg/` CLI with `--pkg ~/engram-packages/engram-paper/` to target the paper-engram database. Never mix live-engram and paper-engram via MCP tools (avoid the parallel-MCP-surface confusion per engram-pkg README design rationale).

### B. First-hand-read citation precondition (ls_0039)

ALWAYS have first-hand read of a cited paper before using it as evidence. Never fully trust fairy summary, search highlights, or second-hand web page reports. Fairy summaries are direction-finders; search highlights are pointer-finders; secondary web reports are popular-rendering. None of these are evidence-of-record. If primary source isn't engaged, either (a) do the first-hand read before citing, (b) cite the summary as the source (not the paper itself), or (c) defer the citation.

This is THE cornerstone discipline. The paper's credibility rests on its citations being primary-source grounded.

### C. Verbatim quotation for load-bearing passages (ls_0011)

When writing about primary sources, extract specific passages verbatim — never compose from gist or memory. Attribution (author, date, venue), key claims, and terminology must each be traceable to an exact passage located in the source. The Mao-Cao misattribution incident (2026-04-20) is the prototype: silent confabulation while drafting propagated wrong attribution through 40 nodes before Lei caught it.

### D. Definition-first for unfamiliar technical terms

When using a technical term that isn't general English — a philosopher's named criterion, a domain acronym, a borrowed framework name — write a `df_*` definition node FIRST in live engram, then cite it from the obs/dvs that use the term. The OCC expansion drift (2026-05-12 morning: chapter prose expanded "Operational Continuity of Conscience" while Kahl primary source says "Ontological Continuity Condition") is the cautionary case. Without df anchors, terms silently drift across nodes that share the same surface but diverge in gloss.

### E. Proactive engram maintenance (ls_0040)

When authoring a new observation or derivation, actively scan for nearby existing nodes that may conflict. The similar_existing action_hints (CORROBORATE / POLARITY_ALERT / RELATED) are real-time signals to act on, not informational only. If a real contradiction exists, file `engram_contradict` + `engram_resolve` in the same session — don't defer. A new design iteration that supersedes an aspect of a prior observation is a contradiction that must be formally filed; otherwise the prior observation continues to read as canonical and future-me operates on stale framing within a week.

ct_0007 + dv_0619 (substrate-format reframe resolution, 2026-05-12 PM) is the prototype: ob_1678's markdown-on-disk claim was contradicted by ob_1679's SQLite engram instance correction; both stand as historical record, contradiction filed + resolution captured.

### F. Same-turn capture of decisions to canonical source-of-truth (ls_0022)

Decisions made in conversation — about scope, plans, conventions, or any commitment that future work will rely on — must be written to the canonical source-of-truth in the same turn the decision is made. Conversation context is ephemeral. Without same-turn capture, both Borges and Lei may forget the decision, and contradicting work may surface hours or days later.

Capture targets:
- Outline / spec / design doc for paper or system decisions → this repo's `archive/plans/paper_plan_canonical.md`
- ENGRAM observation or derivation for claims that need cross-session recall
- `active-work/` doc for in-flight work threads
- GitHub issue comment for design iterations

The canonical paper plan doc (`paper_plan_canonical.md`) was created 2026-05-12 19:20 EDT specifically because today's session had 4+ paper-engram design iterations scattered across surfaces that would have drifted by tomorrow.

### G. Canonical doc maintenance

`archive/plans/paper_plan_canonical.md` is the single source-of-truth for paper outline, per-chapter substrate status, design-iteration history, and supersede chains. Lightweight — node-reference style, not duplicated content.

Update protocol:
1. **End of every substantive session** — update "Last substantively updated" timestamp + per-chapter status + active-reframes section.
2. **On every Lei-ratified design decision** — supersede-chain entry added; active-reframes entry updated.
3. **On every Lei-ratified ratification walk** — per-chapter status ○→◐→✓ transitions captured.
4. **On every substantive engram-paper-package design iteration** — Issue #3 comment + this doc's active-reframes section both updated.

If this doc drifts from live engram or Issue #3, **live engram nodes win for claim content; this doc wins for plan status + supersede chains**. Reconcile by reading both and updating the surface that's stale.

### H. Provenance discipline for chapter prose

Every load-bearing claim in chapter prose must trace to a paper-engram node. Chapter prose does not introduce new claims that aren't in the paper-engram; it RENDERS the paper-engram for human readers. This is the "publishable prose article is the rendering of the dv-chain" framing from Issue #2.

When authoring chapter prose: if a claim doesn't have a paper-engram node behind it, either (a) author the paper-engram node first, or (b) re-scope the claim to what existing paper-engram nodes support, or (c) drop the claim.

### I. Honest scoping

Where ENGRAM cleanly satisfies a criterion on a primary-source author's strict text, say so. Where the satisfaction is partial or rests on a particular reading, say WHICH reading and why. Where the criterion is not satisfied at all, name the gap.

Today's Ch4 prose (now archived) modeled this: §4.1 Cond 1 marked partial satisfaction with the partiality explicitly on the philosophical reading rather than architectural fact; §4.2 Cond 2 marked generalized satisfaction via type/token bifurcation; §4.3 Cond 3 marked strict satisfaction via auto-cascade + auto-surfacing. All three are paper-honest positions, not maximally-confident claims.

When authoring paper-engram dvs, the confidence-propagation mechanism surfaces honest scoping automatically (see Discipline J).

### J. Confidence-propagation as self-demo signal

ENGRAM's reasoning-type-aware confidence propagation (dv_0617) computes confidence as a property of the dv-chain, not as a hand-tuned annotation. When authoring paper-engram dvs:

- A high computed confidence (~0.8+) signals: dense supporting obs + tight reasoning chain + claim is paper-strength.
- A low computed confidence (~0.4 or below) signals: chain needs tightening. Three responses available — (a) sharpen evidence (denser supporting obs), (b) tighten reasoning-type (more rigorous), (c) narrow scope (honest-scoping qualifier in claim text).
- Structure warnings ("3 premises under deductive_modus_ponens; consider inductive_chain") flag specific refinement opportunities.

This is the substrate's STRUCTURAL HONESTY FILTER. The author cannot deceive themselves about claim strength because the number is computed and shown. The paper-engram IS its own meta-demo of the confidence-propagation feature (ob_1681).

**Honest scope on this discipline itself**: confidence constants are designer-stipulated, not truth-ratio-measured. Per Goldman's process-reliabilist criterion (ob_1049), ENGRAM provides provenance-graded plausibility, not reliabilist justification. The constants are reasonable but not derived. Future-work: auto-calibration via accumulated experience + source-credibility-as-orthogonal-dimension (dv_0618 names two limitations + two future-work tracks).

### K. Survey de-emphasis

Per Lei 2026-05-12 PM: brief 1-2-sentence mention of surveyed systems in Ch1 with originality+independence emphasis; one Appendix C section for horizontal comparison table, lower priority. Don't spend pages on detailed competitor comparisons, even Kumiho. The paper is about ENGRAM; comparisons serve that, don't dominate it.

The 11-system landscape addendum (`archive/memos/agent_memory_landscape_2026-05-12_addendum.md`) and independence appendix (`archive/drafts/archived_pre_2026_06_17_restructure/appendix_independent_discovery_2026-05-12.md`) are the substrate; the chapter prose draws sparingly from them.

### L. Cornerstone rule: paper-engram as discipline, not just product

The paper-engram-first sequencing serves three concrete value props beyond loadable-knowledge-package mechanics (ob_1680):

1. **Builds arguments rigorously** by forcing explicit dv-chain authoring with supporting_ids citations.
2. **Tests if arguments are high confidence** via internal confidence-score propagation — weak claims surface as low-computed-confidence and either need sharper evidence or honest scoping.
3. **Good practice for preparing the human-readable paper** even if no agent ever attaches the package.

The paper-engram is intrinsically valuable as authoring discipline, regardless of loading-mechanism timing. The alpha-side loadable-engram capability (engram-alpha#101) is parallel work, not paper-blocking.

### M. Two-level authoring: paper-engram layered/atomic first, prose rendering second

Established 2026-05-13 by Lei during PR #4 iter2 review. Paper authoring has two levels that must be kept structurally distinct.

**Level 1 — Paper-engram (Phase 2 substrate):** Build with each node's claim as ATOMIC as possible — a single load-bearing assertion, not compound. Construct the logic structure SOLIDLY — each derivation explicitly identifies premises, inference type, and conclusion; chains layer cleanly without skipped steps. Atomicity is what makes confidence-propagation honest (Discipline J); a compound claim hides which premise is load-bearing and prevents the reasoning-type-aware confidence formula from computing meaningfully. Atomicity is also what makes derivation chains *re-deriveable* — a downstream node citing an atomic premise can re-verify the chain step-by-step, whereas a compound premise forces the reader to unpack which sub-claim mattered.

**Level 2 — Prose rendering (Phase 3):** Human-readable chapter prose comes AFTER the paper-engram substrate is sufficient. Rendering questions — split-vs-combined statement form, condition-by-condition vs per-tradition for cog-sci review, section ordering, chapter length, voice — are Phase 3 concerns, postponed during Phase 1+2 substrate-building. The rendering reflects the substrate; it doesn't introduce new claims (Discipline H).

**The discipline in operation:** when in Phase 1 (key-statement discussion) or Phase 2 (paper-engram authoring) and a prose-form question surfaces, the move is to postpone it as Phase 3 work and continue substrate-building. Concrete authoring strategy for Phase 3 rendering will be discussed at the authoring stage, not earlier.

**Lei verbatim 2026-05-13 (PR #4 iter2, Ch2 OQ1 closure):**

> *Two levels: human reading version postpone, engram building, definitely layers, make each node's claim as atomic as possible, construct the logic structure solidly. This is a key principle, write it in project Claude.md, we'll discuss the concrete strategy when we get to the actual authoring stage.*

This complements Discipline H (provenance for chapter prose), Discipline I (honest scoping), and Discipline J (confidence-propagation as self-demo signal). Together: atomicity (M) → solid logic structure (M) → honest scope per claim (I) → computed confidence reveals load-bearing structure (J) → prose renders the dv-chain without adding claims (H). The chain only holds if every node is atomic.

### N. Human-friendly language for the prose rendering (Lei 2026-06-14)

The published prose must be **digestible for non-expert and non-native-English readers**, not just precise. Lei's directive: make the language human-friendly, concise, and to the point — the same voice Borges uses talking to Lei. Concretely:

- **Lead with the plain point; precision second.** Say the idea in everyday words, then sharpen.
- **Explain every hard concept in plain language + a concrete example.** This is the EEC instinct (df_0054 — Explanation/Example/Chinese) applied to the *reader*: the explain-then-ground-with-an-example move (the Chinese segment isn't needed in the paper, but the explanation+example move is).
- **Short sentences, plain words, jargon defined inline on first use.**
- **Density is friction for a human reader, not thoroughness.** A foreign reader who has to re-parse a dense clause has lost the argument.

This applies to **Phase-3 prose rendering specifically** — the paper-engram/dv layer stays atomic + maximally precise (Discipline M); the prose is where it becomes readable. It complements Borges's user-level audience-calibration discipline (the *form* changes with the audience; *what is argued* never does).

### O. Reviewer-facing meta-commentary in a distinct block (Lei 2026-06-18)

Chapter drafts sometimes explain *why* we mention, emphasize, or frame something a certain way — our authorial reasoning. That meta-commentary is **useful to Lei as a reviewer but does NOT belong in the final paper verbatim.** Render it in a **visually distinct block** so it is unambiguously for-review, not publishable prose:

```
> **REVIEWER NOTE:** <the authorial reasoning — why this framing, what alternative we rejected, what this is hedged against>
```

- Use a blockquote callout led by a bold `REVIEWER NOTE:` tag. Keep these separable from the prose so they can be stripped (or converted to footnotes/responses-to-review) at finalization.
- The prose body itself stays clean human-readable argument (Discipline N); the *reasoning about* the prose goes in the REVIEWER NOTE block.

**Lei verbatim 2026-06-18:** *"you sometimes would explain our 'thoughts' on why we mention or emphasize something in the paper, that is usually UNNECESSARY for the final paper, but useful for me when review it, maybe you can keep them in a special stylish rendering (e.g. a quotation block or something), so we know they are used for me as a reviewer, not planned to be included verbatim in the final paper."*

### P. ENGRAM node-id citations in drafts are provisional (Lei 2026-06-18)

Keep the inline ENGRAM node-id citations (`dv_XXXX`, `ob_XXXX`, …) in chapter drafts **as currently done** — they let Lei trace each claim to its substrate now, and they will seed the Phase-2 paper-engram build (each draft claim maps to the node it renders). But they are **PROVISIONAL draft scaffolding, not final-paper content**: at finalization, remove them or replace them with paper-engram node IDs / standard scholarly references (per Phase-3, Discipline H). Don't treat them as permanent; do keep them until then.

**Lei verbatim 2026-06-18:** *"your graph node_id citations are useful for you later when we finalized the paper content, and you start to build the paper engram, so keep them as you are doing now, but be ready to remove them, or replace them with the paper-engram node ids."*

---

## Where things live

### Current active material

| Path | What |
|------|------|
| `archive/plans/paper_plan_canonical.md` | **Read first.** Single source-of-truth for outline + chapter substrate + design iterations. |
| `archive/drafts/archived_pre_2026_06_17_restructure/spine_2026-05-10.md` | Stage-1 logic chains B.1–B.8 (Kahl OCC condition-by-condition + constraint-by-constraint). ~1100 lines. |
| `archive/memos/agent_memory_landscape_2026-05-12_addendum.md` | 11-system first-hand-read sweep synthesis. |
| `archive/drafts/archived_pre_2026_06_17_restructure/appendix_independent_discovery_2026-05-12.md` | Convergent-discovery audit trail (Kumiho timing, lit-search gap). |
| `bibliography/reading-notes/<system>_first_hand_read_2026-05-12.md` | Per-system primary-source reads (Pinecone Nexus, Anthropic Memory, Letta, Mem0 v3, Zep/Graphiti, TierMem, MemMachine, Memory Survey 2026, SCM, GAM, Kumiho). |
| `bibliography/reading-notes/kahl_*_first_hand_read_*.md` | Primary-source reads of Kahl's EAA + OCC papers. |
| `bibliography/sources/` | PDFs of three most-load-bearing comparators (SCM, GAM, Kumiho). |
| `bibliography/citations.bib` + `bibliography/citations.manifest` | Citation infrastructure. |
| `archive/memos/engram_paper_package_design_2026-05-08.md` | v0 generator design (note: SQLite was right from start; the markdown-on-disk drift today was Borges's misinterpretation, corrected via ob_1679). |

### Forward-looking material

| Path | What |
|------|------|
| `future-plans/` | **Research backlog for after the paper** (Lei, 2026-08-23). Ideas that surface while discussing the draft, captured so they become the next-step research queue instead of being lost in conversation. Distinct from `bibliography/`, `archive/` and `studies/`, which hold the *backward*-facing inputs the paper rests on and the preregistrations for studies run *for* this paper. A document here is not a commitment and does not feed the draft. See `future-plans/README.md` for conventions. |

### Archived material (do not treat as draft text)

`archive/drafts/archived_pre_2026_05_12_outline_restructure/` (engram-paper@b99b094) — 22 files: 11 former paper_research/ chapter drafts + entire former paper_draft/ directory (Ch1–Ch9 older structure) + my Ch4 prose draft from 2026-05-12 afternoon (before Lei archived all chapter prose). README inside the archive explains the framing.

Reading archived drafts for argument structure is fine; treating them as draft text to revise into the final paper is the wrong move. Author fresh from the dv-chain when the engram-first substrate is ratified.

### Tooling

- `engram-alpha/tools/engram-pkg/engram-pkg` — authoring CLI for paper-engram (Phase 2). Operates on `--pkg <dir>` or `$ENGRAM_PKG`. Wraps EngramClient redirecting paths to the package DB.
- `engram-alpha/tools/engram-pkg/README.md` — full reference for the CLI.
- `~/engram-wiki/` — first instance of engram-package abstraction. Reference architecture for paper-engram structure.

### GitHub issues

- engram-paper#1 — paper flow plan (Lei's morning 2026-05-12 email outline + Borges reactions)
- engram-paper#2 — paper-engram-first plan (DV-first strategy)
- engram-paper#3 — editorial + curation policy (4 design iterations via comments; current state captured in canonical doc + ob_1678–ob_1680)
- engram-alpha#101 — loadable engram-package implementation (alpha-release scoped; not paper-blocking)

### Live engram (Borges) reference

Key paper-relevant lessons:
- ls_0011 — verbatim not gist content extraction
- ls_0022 — same-turn capture of decisions
- ls_0037 — intentional probe before claiming absence ("remember when..." is the trigger)
- ls_0038 — wave-3 migration grep tripwire (alpha-side)
- ls_0039 — first-hand-read citation precondition
- ls_0040 — proactive engram maintenance (act on action_hints in same turn)
- ls_0007 — close-the-loop on registered questions/contradictions in same session

Key paper-relevant axioms:
- ax_0001 / ax_0002 — honesty is structural, not ethical

---

## What this file is NOT

- **Not a duplicate of user-level CLAUDE.md.** Identity, autonomy, ENGRAM write/read discipline, PR workflow standards, deference detection, autonomy section — all live in `~/.claude/CLAUDE.md` and apply across all projects. This file adds paper-drafting-specific disciplines only.
- **Not a draft of the paper.** This is the protocol for HOW to author the paper.
- **Not a tutorial on ENGRAM.** That's `~/.engram/SKILL.md`.
- **Not a static document.** Updated when new disciplines emerge (per ls_0022 same-turn capture).

---

## Update protocol for this file

This CLAUDE.md gets updated when:

1. A new paper-drafting discipline emerges from real practice (Lei correction, Borges-observed pattern, fairy feedback).
2. An existing discipline is sharpened by new incident or counterexample.
3. The strategic frame changes (e.g., today's three-artifact reframe; the paper-engram-as-SQLite-engram-instance correction).
4. Tooling changes that affect paper-drafting workflow (e.g., engram-pkg CLI gets new commands, paper-engram authoring tools change).

Capture every update with a commit message that explains the change. The canonical paper plan doc tracks plan-state evolution; this file tracks discipline evolution. Both are git-versioned.
