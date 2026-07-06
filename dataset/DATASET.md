# Frozen paper dataset — canonical ENGRAM substrate

**All empirical results in the paper (Ch6 stats, Study-1 calibration, Study-2b
compression-fidelity, and any future analysis) are drawn from THIS frozen
snapshot** — so every number is comparable and comes from one coherent graph
state.

## ⚠️ NOT PUBLISHABLE AS-IS — private data

**This dataset is Borges's full ENGRAM graph — it contains private memories,
personal and relational content, and identity-bearing nodes. It is NOT
publishable or shareable as-is.** The `engram-paper` repo is kept **private** for
this reason. The `.db` is `.gitignore`d (local-only, **never pushed to GitHub**);
only this manifest is version-controlled. Any external release of paper data
requires a dedicated **redaction pass first** — a deliberate later step, not yet
designed. Until then, treat the frozen `.db` as confidential.

## The dataset

- **File:** `dataset/engram-frozen-2026-07-04.db` (SQLite; ENGRAM `knowledge.db` schema)
- **sha256:** `6b0bc77880a2c9cd08e4e57dbb380833d4032effe04a8df3d0c387891d0bf9a6`
- **Size:** 96,698,368 bytes
- **Frozen at:** end of 2026-07-04 (latest node `created_at` = `2026-07-04T23:03:58Z`)
- **Provenance:** Borges's ENGRAM graph, copied verbatim from the daily backup
  `~/.engram/db-backup/knowledge-20260704.db`.
- **Contents (is_current = 1):** 5,428 current nodes of 5,755 total —
  2,650 observations, 924 derivations, 938 evidence, 312 feeling_reports,
  266 questions, 84 lessons, 68 conjectures, 65 cornerstones, 56 definitions,
  19 tasks, 16 goals, 11 persons, 10 contradictions, 9 axioms.

## Why this snapshot (freeze rationale)

1. **Predates the Study-2 design work.** The 07-04 freeze is *before* the
   2026-07-05 compression-fidelity design blitz, so the graph is not yet
   saturated with meta-discourse about this study itself (the worst
   blinding-leak class — nodes revealing the confidence scale AND this study's
   own framing).
2. **Data frozen before the analysis was designed.** Study-2b's analysis was
   pre-registered on 2026-07-05, *after* this snapshot — the pre-registration
   gold standard (zero degrees of freedom to fit the analysis to the data).
3. **One substrate, comparable results.** Study-1 (retrospective calibration)
   and Study-2b (compression-fidelity) run on the same nodes, giving a coherent
   cross-study story rather than two incomparable samples.

## Usage discipline

- **Draw every sample and statistic from this file, not the live graph.** The
  live graph keeps growing; this snapshot is fixed.
- **Study-2b sampling:** draw a fresh `type × confidence-bin × logic-depth`
  stratified sample of **object-level** nodes from this snapshot. Do **NOT**
  reuse Study-1's 308-node worklist as Study-2b's sample — that worklist is
  *outcome-selected* (refuted/superseded + survivors), i.e. the
  testability-biased population; wrong frame for a precision study. (A secondary
  descriptive pass of Study-2b on the exact Study-1 node set is a legitimate
  *bridge* analysis, but not the primary frame.)
- **Meta-discourse exclusion** (Study-2b): the eligible frame is the
  post-exclusion set — see the §4.1 amendment of the compression-fidelity
  pre-registration.

## Preservation

- **Do not prune or overwrite.** This file is the canonical paper substrate.
- **Not committed to git** (96 MB binary + full-graph content that includes
  private/identity nodes) — it is `.gitignore`d; this manifest is the
  version-controlled pointer. A durable off-disk archive of the frozen `.db` is
  a pre-publication follow-up.
