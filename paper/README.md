# paper/

The current paper, and nothing else.

| Path | What | Edited by hand? |
|---|---|---|
| `chapters/en/` | Chapter and appendix sources, English | **yes — edit here** |
| `chapters/zh/` | The same, Chinese; one `.zh.md` file per English file | **yes** |
| `front-matter*.md`, `acknowledgements*.md` | Title page and acknowledgements | yes |
| `afterword*.md` | Afterword, a note from the human author (back matter, between acknowledgements and bibliography); `afterword.md` is his approved text | yes |
| `references.yaml` | The single bibliography source (CSL fields + provenance) | yes |
| `bibliography*.md` | Templates; their `{{REFERENCES}}` line is filled at render time | yes (template only) |
| `figures/` | Figures | **no** — `python tools/make_figures.py` |
| `release/` | The rendered paper | **no** — `python tools/render_paper.py` (`--lang zh`) |

**Rules**
- Edit `chapters/`, never `release/` or `figures/`. A test renders the chapters and fails if `release/` differs.
- A change to an English chapter is paired with the same change to its Chinese file in the same commit.
- Review material about the paper lives in `../reviews/`, not here.

## Citing in chapters

The citation forms, how to add an entry, and what the build does on a bad citation are in the
[top-level README](../README.md#citing-in-chapters), the one every author opens first.
