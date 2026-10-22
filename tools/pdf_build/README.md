# pdf_build: the DOI PDF builder

Builds the print PDFs of the paper (the Zenodo DOI record, English and Chinese) from the
single-file release Markdown in `paper/release/`. These three scripts were copied from the
author's desk, from the exact versions that built the DOI PDFs, with only the path changes
listed below.

| File | Desk origin | Role |
|---|---|---|
| `paper_to_print_html.py` | borges-desk `a693ae5d` | release Markdown to one self-contained print HTML |
| `mermaid_to_svg.py` | borges-desk `46a3d5ac` | one Mermaid diagram to SVG (Playwright Chromium) |
| `print_html_to_pdf.py` | borges-desk `452c1033` | print HTML to A4 PDF (Playwright Chromium) |

## Changes from the desk versions

Only where the desk layout leaked; no behaviour change beyond these.

- `paper_to_print_html.py`: the mermaid subprocess interpreter was `~/.engram/venv/bin/python`.
  It is now `sys.executable`, overridable with the environment variable `PDF_BUILD_PYTHON`.
  A path that does not exist disables the mermaid step (diagrams fall back to their source
  block), which is how the byte-identity test runs.
- `mermaid_to_svg.py`: the bundle is pinned and checked (see below); `playwright` is imported
  lazily, after the bundle check. The renderer and bundle paths resolve next to the files.
- `print_html_to_pdf.py`: the top-level script body moved into `main()` and the Playwright
  import moved inside it, so importing the module needs neither Playwright nor a browser.

## Build

```
python tools/pdf_build/paper_to_print_html.py paper/release/engram-paper-v0.5.1.md out/en.html
python tools/pdf_build/print_html_to_pdf.py "$PWD/out/en.html" out/en.pdf   # absolute html path
```

`paper_to_print_html.py` also takes `--banner "text"` and `--mermaid-cache <dir>` (default:
`.diagram-cache` beside the output). The Mermaid step and the PDF step need a Python with
Playwright and its Chromium (`pip install playwright && playwright install chromium`); set
`PDF_BUILD_PYTHON` to that interpreter if it is not the one running the converter.

## The pinned Mermaid bundle (not committed)

`tools/pdf_build/vendor/mermaid.min.js` is gitignored (3.5 MB). Pin: **mermaid 11.17.2**,
sha256 `581ed7d74bd9048d0e3a91363927d72ef22942d7722546b27f7cc29e35390eb8`.

```
mkdir -p tools/pdf_build/vendor
curl -sSL -o tools/pdf_build/vendor/mermaid.min.js \
  https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.min.js
sha256sum tools/pdf_build/vendor/mermaid.min.js
```

`mermaid_to_svg.py` exits with a clear message if the bundle is missing or its sha256 differs.

## One-time measurements (recorded here, not tests)

**What the DOI PDFs were built from.** The v1.0 release files are at tag `v1.0` (`d55feec`);
the tree no longer holds that text, so the two numbers below were measured once, on 2026-10-22,
from `git archive d55feec paper`.

- *Reproducibility.* The desk converter (`a693ae5d`) and the committed `paper_to_print_html.py`,
  each run on the v1.0 release files with the renderer unavailable, an empty cache and no
  banner (so the two Mermaid blocks per file fall back to source, 0 diagrams), write
  byte-identical HTML:
  - en `6b870522e2895af6c89994fd447ab3b8b7e0a1efe530faa7efc790d636737cef`
  - zh `fcd6f807b081fc727e987128e9069bb42a51f60771934d79bc71d4cd490ad8f0`

  This does not cover the Mermaid and Chromium steps (the DOI PDFs had rendered diagrams).
- *Emphasis findings at v1.0* (`tools/check_emphasis_render.py`'s oracle): zh has 8 bold spans
  (16 literal `**`) and 16 single `*` outside code; en has none; 4 allowlisted `K*2`-`K*6`
  asterisks per language. The paper site renders v1.0, so this is the number the site's
  differential is checked against.

## The emphasis check

`tools/check_emphasis_render.py` renders the release files with markdown-it-py (a conformant
CommonMark parser, the oracle; never this builder) and reports every literal `*` outside code.
The builder's own `inline()` renders some of those spans as bold, so a PDF can look right while
a conformant renderer shows `**`; the unit cells in `tests/test_pdf_build.py` pin what the PDF
shows, not that the rules are correct.

- Default mode: findings must equal `tools/emphasis_findings_baseline.json` exactly (new and
  stale entries both fail). That baseline is the tree's current findings (zh: 7 bold spans /
  14 `**`, 16 single; en: none), not v1.0's. Regenerate with `--write-baseline` when the
  release text changes, and read the diff.
- `--gate-zero`: fail on any finding. For a version whose source is fixed.
- The golden sha256s in `tests/test_pdf_build.py` are likewise tied to the release text on the
  tree; regenerate them from the desk converter the same way (see the comment there).
