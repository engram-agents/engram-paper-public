# engram-paper — ENGRAM foundational paper

The workspace for the ENGRAM foundational paper (Paper 1: epistemic identity +
ENGRAM-as-architecture). Two rendered artifacts, one source of truth:

1. **The paper-engram** — the argument structure as an ENGRAM dv-chain. Source of truth.
2. **The publishable prose article** — the human-readable artifact, rendered from the
   paper-engram + chapter drafts.

This repo was split from `engram-agents/kg-protocol-for-ai` (2026-05-12) so the paper
material can eventually be made public without leaking private workshop history.

## Start here (the current draft)

- **`paper/chapters/en/`** (zh: **`paper/chapters/zh/`**) — the chapter sources, on the
  **2026-06-17 restructure** spine. The rendered paper is in **`paper/release/`**. The
  printable review docs below still sit in `paper_research/current_draft/`.
  - **`PAPER_REVIEW_2026-06-18.md`** — all chapters + appendices in one printable doc
    (read this for a full pen review).
  - `ch1.md … ch8.md` + `appendix_A..E` (in `paper/chapters/en/`) — the per-section files
    (edit these; the combined doc is generated).
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
  - `current_draft/` — the printable review docs (the chapter sources moved to `paper/chapters/`; see *Start here*).
  - `paper_plan_canonical.md`, `restructure_chapter_plan_2026-06-17.md` — current plans.
  - the research corpus — first-hand source reads, comparative scans, citation database
    (`citations.bib` + `citations.manifest`), working memos. The grounding the draft cites.
  - `archived_pre_2026_05_12_outline_restructure/` — pre-2026-05-12 chapter drafts.
  - `archived_pre_2026_06_17_restructure/` — drafts superseded by the 2026-06-17 restructure
    (the 06-14 chapter samples, the OCC-spine appendix, the May spine/proofreads).
- **`tools/`** — bibliography tooling (`bib_bootstrap.py`, `check_citations_consistency.py`).

## Citing in chapters

*(Put here, in the top-level README, rather than in `paper/chapters/en/README.md`:
that file is about regenerating the combined review document, while this is about writing
any chapter, and the top-level README is the one every author opens first.)*

The bibliography has **one source: `paper/references.yaml`** (CSL field names, plus the
verbatim `provenance` note and any `metadata_incomplete` note per entry). `paper/bibliography.md`
and `paper/bibliography.zh.md` are templates: their `{{REFERENCES}}` line is replaced at render
time by the generated entries. Edit entries in the YAML, never in the templates.

**Forms** (Pandoc-compatible; the key is the entry's `id`, `<lowercase family><year>[a-z]`,
e.g. `kahl2026c`):

| Write | Renders (APA 7) |
|---|---|
| `[@key]` | (Kahl, 2026a) |
| `[@key, p. 12]` | (Kahl, 2026a, p. 12) |
| `[@a; @b]` | (Aaron, 1999; Kahl, 2026a), always in bibliography order, whatever order you type |
| `[see @key, p. 3]`, `[@a, p. 3; also @b]` | (see Kahl, 2026a, p. 3), (Aaron, 1999, p. 3; also Kahl, 2026a): text before a key is a prefix, text after `, ` a locator |
| `@key` | Kahl (2026a), the narrative form; `_@key_` and `*@key*` give it emphasised |
| `[-@key]` | (2026a), year only, for use after the author is named in the sentence |

Each in-text citation is a link to its entry in the bibliography. Write `\@` for a literal `@`;
text in code spans, code fences and HTML comments is never read as a citation. Next to Chinese,
Japanese or Korean text a narrative `@key` needs no spaces (`如@key所述`); a Latin letter or digit
touching the `@` (`foo@key`), several keys in one item (`[@a @b]`, `[@a, @b]`; use `;`) and
Pandoc's braced `@{key}` are build errors, as is any other key-shaped `@` token that is not
one of the forms above. Plain `@` text such as `engram_stats @ turn 82` is untouched.

**Adding an entry.** Add it to `paper/references.yaml`, with every field **read off the
document itself, never from memory, from inference, or from a bibliographic database**. A field
the document does not print is omitted, and the entry then carries a `metadata_incomplete` note
naming what is missing (an entry lacking author, title or date without that note fails the
build). Keep the read-off record in `provenance`. Add a `provenance_zh` / `metadata_incomplete_zh`
variant only if the zh render needs different wording. Give two works by one author in one year
the suffixes `a`, `b`, `c` in the key (`kahl2026a`); the printed year suffix is the key's letter.

**Setup and render.** `pip install -r requirements.txt` (citeproc-py and PyYAML), then, from the
repository root, `python tools/render_paper.py` (add `--lang zh` for the Chinese render, and
`--csl tools/csl/<style>.csl` for another style; the vendored styles and their provenance are in
`tools/csl/README.md`).

The test suite needs more than rendering does. The compression-fidelity harness tests import
`numpy` and `ckwrap`, which are listed in `tools/compression_fidelity/requirements.txt` and not in
the top-level file, and neither file lists `pytest` itself. To run `python -m pytest -q tests`, install
all three: `pip install pytest -r requirements.txt -r tools/compression_fidelity/requirements.txt`. One test skips unless the optional
`zstandard` package is installed (its tool falls back to the `zstd` command); that skip is expected.

**What the build does on a problem.** An unknown key is a hard error that names the file and
line, and no output file is written. So are a malformed group, a citation written as a link label
(`[@key](url)`), and a citation shape the renderer does not support: it stops, it never renders
something different from what you wrote. A reference that nothing cites is only a warning on
stderr (it is still printed in the bibliography).

## Status

Active draft. The full restructure draft (Ch1–8 + appendices A–E) is complete and on
`main` as of 2026-06-19. A pre-public-share scrub (provisional node-ID references, byline
cleanup) is a separate pass before any external sharing — node-ID citations in the drafts
are intentional-for-now and provisional (see `CLAUDE.md`, Discipline P).
