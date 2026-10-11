# engram-paper

The paper *ENGRAM* (v0.5.1), and the record of how it was made: its sources, its reviews, the
tools that produced every number and figure, and the material it grew out of.

## Start here

- **Read the paper:** [`paper/release/engram-paper-v0.5.1.md`](paper/release/engram-paper-v0.5.1.md)
  (Chinese: [`engram-paper-v0.5.1.zh.md`](paper/release/engram-paper-v0.5.1.zh.md)). Generated; never edited by hand.
- **Edit the paper:** the chapter sources are in [`paper/chapters/`](paper/chapters/). See [`paper/README.md`](paper/README.md).

## Places

| Place | What it holds |
|---|---|
| [`paper/`](paper/) | The current paper, and nothing else: chapter sources (en, zh), figures, front matter, the rendered release. |
| [`bibliography/`](bibliography/) | What the citations rest on: the citation database, first-hand source copies, and a reading note per source. |
| [`reviews/`](reviews/) | How the paper was checked: fresh-reader rounds, peer review rounds, the human author's chapter notes. |
| [`studies/`](studies/) | Preregistered studies this paper does not cite, kept live for later work. |
| [`tools/`](tools/) | Every script that makes a number, a figure or the render. |
| [`tests/`](tests/) | Checks that the render, citations, glossary and statistics tooling hold. |
| [`data/`](data/) | The pointer to the frozen graph snapshot all of the paper's numbers come from. |
| [`archive/`](archive/) | Everything superseded, frozen, with an index of what each item was and what replaced it. |
| [`future-plans/`](future-plans/) | Directions beyond this paper. |

Each place has its own README stating what belongs there, how it is named, what is generated
versus edited by hand, and how to regenerate what is generated.

## Two rules for the whole repository

1. **Only `paper/` is the paper.** Anything else may be cited by it or may have shaped it, but is not it.
2. **Nothing is deleted; it is archived.** Superseded material moves to `archive/` with an index row.
   One exception: generated files (such as compiled caches) may leave the tree; the history keeps them.

## History and provenance

This repository is published with its development history, so every claim in the paper can be
traced to the work that produced it. Files were moved with `git mv`, so `git log --follow <path>`
follows a file across the reorganisation of 2026-10-11.

**One rewrite, made before publication.** Before this repository was made public, its history was
rewritten once to remove the human author's child's information. Two early engine-development
experiment folders, whose inputs were built from her events, were removed from every commit; three
table rows in two archived memos were replaced with a marker line. The rule applied: remove a file
when the private content is what the file is; redact the line when it is a string inside a file that
otherwise stands on its own. Nothing else was changed, and no commit was dropped (229 commits before
and after). Each commit's author and date are unchanged; one author's several git identities were
unified under one address. What was removed is recorded in [`archive/INDEX.md`](archive/INDEX.md).

**Commit hashes.** The rewrite gave every commit a new hash. `archive/INDEX.md` cites the new ones.
Hashes quoted inside archived documents, reviews and manifests refer to the pre-publication history
and do not resolve here.

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

## Build and test

```
pip install pytest -r requirements.txt -r tools/compression_fidelity/requirements.txt
python tools/render_paper.py            # writes paper/release/engram-paper-v0.5.1.md
python tools/render_paper.py --lang zh  # writes paper/release/engram-paper-v0.5.1.zh.md
python -m pytest -q tests
```

The agent working conventions for this repository are in [`CLAUDE.md`](CLAUDE.md).
