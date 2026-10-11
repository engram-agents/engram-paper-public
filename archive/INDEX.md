# archive/INDEX.md

One row per item. "Replaced by" names the current material; "Landed in" is the commit where it took over. All items were moved here on 2026-10-11 by the repository reorganisation, which keeps each file's history (`git log --follow`).

| Item | What it was | Dates | Why retired | Replaced by | Landed in |
|---|---|---|---|---|---|
| `drafts/archived_pre_2026_05_12_outline_restructure/` (23 files) | Chapter prose written before the 2026-05-12 outline restructure | to 2026-05-12 | Restructure: the paper was re-planned from its argument structure first | The restructured plan, then the current chapters (`paper/chapters/`) | `b99b094` (archived), `dfb99d8` (chapters in place) |
| `drafts/archived_pre_2026_06_17_restructure/` (9 files) | Drafts and samples superseded by the 2026-06-17 restructure | 2026-05 to 2026-06-14 | Superseded by the restructured draft | The assembled restructure draft, now `paper/chapters/` | `e2b3f36` (archived), `dec8b85` (draft assembled) |
| `drafts/PAPER_REVIEW_2026-06-18.md`, `drafts/PAPER_REVIEW_2026-08-11.md` | Combined print sets of the draft, made for full read-throughs | 2026-06-18, 2026-08-11 | Generated snapshots of drafts that have since changed | `paper/release/` (the rendered paper) | `dfb99d8` |
| `drafts/review_opinion_sl_section_2026-08-11.md` | A review opinion on one section of the 2026-08-11 draft | 2026-08-11 | The section was revised | The current chapter text | — |
| `plans/paper_plan_canonical.md` | The paper plan: outline, chapter substrate, design history | 2026-05-12 to 2026-06-18 | Executed: the plan became the paper | `paper/chapters/` and this repository's README | the reorganisation commit |
| `plans/restructure_chapter_plan_2026-06-17.md` | The per-chapter plan for the 2026-06-17 restructure | 2026-06-17 | Executed | `paper/chapters/` | `dec8b85` |
| `plans/benchmark_plan_2026-08-17.md` | Survey of benchmarks that could test the system's claims, and how to run them | 2026-08-17 | Research for later work, not used by this paper | — (see `future-plans/`) | — |
| `memos/` (26 files) | Working memos from the drafting period: landscape scans and addenda, citation and deep sweeps, argument memos, proofreads, positioning notes, empirical inventories, venue analysis, an assembly-round harvest | 2026-05-05 to 2026-09-20 | Working material; what survived is in the chapters, the bibliography and the reading notes | `paper/chapters/`, `bibliography/` | — |
| `experiments/threshold_calibration_2026-05-09/` | Early similarity-threshold calibration for the memory engine | 2026-05-09 | Engine-development experiment; its outcome lives in the engine, not in this paper | — | — |
| `experiments/nli_polarity_bakeoff_2026-05-10/` | Bake-off of contradiction-detection models for the memory engine | 2026-05-10 | Engine-development experiment, as above | — | — |
| `experiments/mine_pre_engram.py` | Scanner used once to extract the pre-ENGRAM conversation excerpts | 2026-05-08 | One-off extraction; its output is kept | `bibliography/sources/pre_engram_history_digest_2026-05-08.md` | the reorganisation commit |
