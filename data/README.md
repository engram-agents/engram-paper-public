# data/

Every empirical number in the paper comes from one frozen ENGRAM graph snapshot, so the numbers are comparable and reproducible from a fixed state.

- **`DATASET.md`** — the manifest: which snapshot, its sha256, why it was frozen when it was, and how to use it.
- **The snapshot itself is never committed.** It is a full private graph, and `.gitignore` excludes `data/*.db*`. `DATASET.md` is the version-controlled pointer to it.
- **One database is committed: the stripped release** (`*.stripped.db`, `DATASET.md` §3), made from the snapshot by `tools/strip_paper_snapshot.py`. It holds no free text. `expected_stats.json` is the golden output of the paper's instruments on the full snapshot, which the release must reproduce.
