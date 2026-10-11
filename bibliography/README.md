# bibliography/

What the paper's citations rest on.

| Path | What | Edited by hand? |
|---|---|---|
| `../paper/references.yaml` | The bibliography the paper renders from (the single source for citations) | yes |
| `citations.bib`, `citations.manifest` | The citation database built while drafting, and its manifest | `tools/bib_bootstrap.py` generates the `.bib`; `tools/check_citations_consistency.py` checks the three agree |
| `sourcing-journal.md` | Log of how each source was found and checked | yes, append-only |
| `sources/` | First-hand copies of sources (PDFs, text extractions, forum captures) | no — snapshots, never edited |
| `reading-notes/` | One note per source read first-hand, with verbatim passages | yes |

**Rules**
- **Snapshots, not links.** A source is kept as a copy so a citation stays checkable if the original moves.
- **Only openly licensed copies are committed.** Sources whose licence does not allow redistribution are listed in `.gitignore` and cited instead.
- **Read before citing.** Every attributed claim in the paper is cited from a source someone read first-hand, and the reading note holds the passage.
- Reading notes are named `<source>_first_hand_read_<date>.md` (or `_verification_` for a targeted check). Older notes keep their original names.
