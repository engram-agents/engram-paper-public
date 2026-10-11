# reviews/

How the paper was checked. This is a record, separate from the paper itself.

| Path | What |
|---|---|
| `fresh-reader/` | Rounds in which a model with no project context read the full paper cold: persona, rubric, each round's report and its run manifest. The run tooling is in `../tools/fresh_reader/`. |
| `rounds/` | Peer review rounds between the authors (review, then response). |
| `lei-notes/` | The human author's chapter-by-chapter reading notes, kept as the record of his review. |

**Rules**
- One file (or file group) per round, with the reviewer and date in the name.
- A round's files are frozen once the round closes. Later rounds add new files; they do not edit old ones.
