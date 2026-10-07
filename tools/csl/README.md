# tools/csl: vendored citation styles

`render_paper.py` formats in-text citations and the bibliography with a CSL style
(`--csl <file>`; default `tools/csl/apa.csl`). Styles here are **vendored unmodified**.

## apa.csl (APA Style 7th edition)

| | |
|---|---|
| Upstream | https://github.com/citation-style-language/styles/blob/master/apa.csl (the CSL project's style repository; also served as http://www.zotero.org/styles/apa) |
| Retrieved | 2026-10-07 |
| Upstream revision | commit `3c6698d791a83016d699f50cbbea857f6ee3d2f8` of `citation-style-language/styles` (2026-10-02, "APA: \"[Data set]\", not \"[Dataset]\" (#8359)"), the newest commit that touches `apa.csl` as of the retrieval date |
| How the revision was pinned | the vendored file was compared byte for byte with `apa.csl` at that commit, fetched from `raw.githubusercontent.com` on 2026-10-07: identical. The three previous upstream revisions (`32078ede`, `a9c2eeec`, `b14d5c33`) differ in size and content, so this is the only candidate of those four that matches |
| Size and hash | 85,817 bytes; sha256 `3917def5fc951b104d64216c3373096042368b9704ba269ca83c14ebaba889fc` (a test pins this hash, so an edit to the file shows up as a failing test) |
| `<updated>` stamp | `2026-02-07T00:00:00+00:00`. This is upstream's own stamp, not ours: the file at the commit above carries it. (A review of this repo's first round reported that the copy served by zotero.org prints a different stamp, `2026-10-02T20:29:11+00:00`, with the same size and otherwise identical content; that value equals the commit time of the revision above, so the Zotero server appears to restamp when serving. I did not re-fetch zotero.org to confirm that.) |
| Authors | Brenton M. Wiernik, Andrew Dunning; contributor Jay Pfaffman (from the file's `<info>` block) |
| Licence | Creative Commons Attribution-ShareAlike 3.0 (http://creativecommons.org/licenses/by-sa/3.0/), as the file's own `<rights>` element states. Kept in the file unmodified. ShareAlike applies to the style file and adaptations of it, not to the paper text rendered with it |

**Do not edit `apa.csl`.** A needed behaviour change goes in `tools/render_paper.py`
(for example, role labels are capitalised there, because citeproc-py skips the style's
`text-case="title"` on labels), or in a new, separately named style file. To update the
style, replace the file with a newer upstream revision, then change this table (revision,
size, hash, retrieval date) in the same commit; the pinned-hash test will fail until you do.

## Adding another style

Add the `.csl` file here, add a row to this file in the same form (source URL, retrieval
date, upstream revision, hash, licence), and render with `--csl tools/csl/<name>.csl`.
Only author-date styles work today: the renderer splits each in-text citation into author
and year, and stops with an error naming the style if it cannot.
