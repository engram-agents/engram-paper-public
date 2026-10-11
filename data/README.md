# data/

Every empirical number in the paper comes from one frozen ENGRAM graph snapshot, so the numbers are comparable and reproducible from a fixed state.

- **`DATASET.md`** — the manifest: which snapshot, its sha256, why it was frozen when it was, and how to use it.
- **The snapshot itself is never committed.** It is a full private graph, and `.gitignore` excludes `data/*.db*`. `DATASET.md` is the version-controlled pointer to it.
