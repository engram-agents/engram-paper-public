# Current Draft — ENGRAM Foundational Paper (review set)

This folder holds the **current** chapter + appendix drafts on the 2026-06-17
restructure spine — separated from the research substrate and stale/archived drafts
in the parent `paper_research/`. This is the review set.

- **`PAPER_REVIEW_2026-08-11.md`** — all chapters + appendices concatenated into one
  printable doc (for pen review). GENERATED; do not edit here — edit the per-section
  files below and regenerate. ch1–4 carry Lei's post-06-18 feedback (commit `6515ed7`);
  ch5–8 + appendices are unchanged from the 06-18 assembly. The prior
  `PAPER_REVIEW_2026-06-18.md` is kept for diff reference.
- **`ch1.md … ch8.md`** — chapters 1–8.
- **`appendix_A_independence.md`, `appendix_B_c3_survey.md`,
  `appendix_C_autorecall_ranking.md`, `appendix_D_relational_identity.md`,
  `appendix_E_techspec.md`** — appendices A–E (filenames now match the restructure
  letter map; this also resolves the old appendix letter-remap item).

## Source-filename lineage (pre-move → clean name)

| Clean name | Was | Status |
|---|---|---|
| ch1.md | ch1_restructure_2026-06-18.md | fresh restructure draft |
| ch2.md | ch2_philosophy_restructure_2026-06-18.md | fresh restructure draft |
| ch3.md | ch3_cogsci_cs_restructure_2026-06-18.md | NEW (restructure) |
| ch4.md | ch4_mechanisms_restructure_2026-06-18.md | NEW (restructure, the core) |
| ch5.md | ch5_draft_sample_2026-06-17.md | content-current + reviewer-note |
| ch6.md | ch6_draft_sample_2026-06-17.md | content-current + reviewer-note |
| ch7.md | ch7_draft_sample_2026-06-17.md | strengthened 2026-06-18 |
| ch8.md | ch8_draft_sample_2026-06-17.md | reframed 2026-06-18 |
| appendix_A_independence.md | appendix_D_independent_discovery_draft_2026-06-17.md | |
| appendix_B_c3_survey.md | appendix_C_draft_sample_2026-06-17.md | |
| appendix_C_autorecall_ranking.md | appendix_C_autorecall_ranking_2026-06-18.md | NEW |
| appendix_D_relational_identity.md | appendix_D_relational_identity_2026-06-18.md | NEW |
| appendix_E_techspec.md | appendix_A_draft_sample_2026-06-17.md | |

## To regenerate the combined doc
Concatenate `ch1..ch8` then `appendix_A..E` with a page-break between each, under the
title/how-to-read header. **Fetch first** — `git fetch origin && git merge --ff-only
origin/main` — before assembling. The chapter files move on `main` independently of
this combined doc, and a stale local clone will silently assemble an out-of-date paper
(this happened on 2026-08-11: the first re-stamp was built from a clone behind
`origin/main` and missed the ch1–4 updates; it was discarded after a `git fetch`
revealed them). (The original 2026-06-18 build script is in that session's transcript.)

## Printing
No local md→pdf renderer; render `PAPER_REVIEW_2026-08-11.md` via VS Code markdown
preview → print, a browser markdown viewer, or `pandoc -o paper.pdf`. Page-break divs
between sections are honored by HTML/browser print.
