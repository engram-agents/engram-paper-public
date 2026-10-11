# tools/

Every script that produces something in the paper. Run them from the repository root.

| Tool | Produces |
|---|---|
| `render_paper.py` | `paper/release/*.md` — assembles the chapter sources into the publishable paper (`--lang zh` for Chinese) |
| `make_figures.py` | `paper/figures/*` — every figure, from the frozen snapshot |
| `paper_stats.py` | Every live-graph number Chapter 6 reports, from the frozen snapshot |
| `modus_ponens_check.py` | §6.1's modus-ponens figures |
| `connectivity_trend.py` | Giant-component share over the graph's lifetime |
| `confidence_gradient_trend.py` | Mean confidence per reasoning type over the graph's lifetime |
| `component_anatomy.py` | What holds the graph together, and what lies outside the main component |
| `evidence_provenance.py` | How much of the graph's knowledge is rooted in the agent's own experience |
| `freeze_paper_snapshot.py` | Freezes a dated copy of a live graph as the paper's data source (see `data/`) |
| `_ssot.py` | The one place that decides which database the numbers come from |
| `bib_bootstrap.py`, `check_citations_consistency.py` | Build and check `bibliography/citations.bib` |
| `csl/` | Citation styles used by the render (provenance in `csl/README.md`) |
| `fresh_reader/` | Runs the cold-reader review rounds recorded in `reviews/fresh-reader/` |
| `compression_fidelity/`, `type_reclassification/` | Harnesses for the two studies in `studies/` |

**Rule:** a number or figure in the paper is produced by a tool here, from the frozen snapshot. Never type one in by hand.
