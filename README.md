# engram-paper — ENGRAM foundational paper

The workspace for the ENGRAM foundational paper (Paper 1: epistemic identity +
ENGRAM-as-architecture). Two rendered artifacts, one source of truth:

1. **The paper-engram** — the argument structure as an ENGRAM dv-chain. Source of truth.
2. **The publishable prose article** — the human-readable artifact, rendered from the
   paper-engram + chapter drafts.

This repo was split from `engram-agents/kg-protocol-for-ai` (2026-05-12) so the paper
material can eventually be made public without leaking private workshop history.

## Start here (the current draft)

- **`paper_research/current_draft/`** — the current review set, on the **2026-06-17
  restructure** spine.
  - **`PAPER_REVIEW_2026-06-18.md`** — all chapters + appendices in one printable doc
    (read this for a full pen review).
  - `ch1.md … ch8.md` + `appendix_A..E` — the per-section files (edit these; the combined
    doc is generated).
- **`paper_research/paper_plan_canonical.md`** — the canonical plan (outline + chapter
  substrate + design-iteration history). Read first for paper context, alongside the draft.
- **`paper_research/restructure_chapter_plan_2026-06-17.md`** — the detailed per-chapter
  plan for the current restructure.

Everything older than the 2026-06-17 restructure lives under the `archived_*` folders
below — do not read those as the current paper.

## Frozen dataset (paper substrate)

**All empirical results in the paper are drawn from one frozen ENGRAM snapshot**,
so every number is comparable and comes from a coherent graph state:

- **`dataset/engram-frozen-2026-07-04.db`** — the canonical frozen graph
  (end of 2026-07-04, 5,428 current nodes; sha256
  `6b0bc778…d0bf9a6`). Predates the Study-2 design work and was frozen before the
  analysis was pre-registered (pre-registration gold standard).
- **`dataset/DATASET.md`** — the manifest: full integrity metadata, freeze
  rationale, and the usage discipline (draw every sample/statistic from this
  file, not the live graph). Read it before running any paper analysis.

The `.db` itself is `.gitignore`d (96 MB binary + private full-graph content);
`DATASET.md` is the version-controlled pointer.

## Layout

- **`paper_research/`** — the working substrate:
  - `current_draft/` — **the current draft** (see *Start here*).
  - `paper_plan_canonical.md`, `restructure_chapter_plan_2026-06-17.md` — current plans.
  - the research corpus — first-hand source reads, comparative scans, citation database
    (`citations.bib` + `citations.manifest`), working memos. The grounding the draft cites.
  - `archived_pre_2026_05_12_outline_restructure/` — pre-2026-05-12 chapter drafts.
  - `archived_pre_2026_06_17_restructure/` — drafts superseded by the 2026-06-17 restructure
    (the 06-14 chapter samples, the OCC-spine appendix, the May spine/proofreads).
- **`tools/`** — bibliography tooling (`bib_bootstrap.py`, `check_citations_consistency.py`).

## Status

Active draft. The full restructure draft (Ch1–8 + appendices A–E) is complete and on
`main` as of 2026-06-19. A pre-public-share scrub (provisional node-ID references, byline
cleanup) is a separate pass before any external sharing — node-ID citations in the drafts
are intentional-for-now and provisional (see `CLAUDE.md`, Discipline P).
