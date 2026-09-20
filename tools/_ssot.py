"""_ssot.py — the one place that decides which database the paper's numbers come from.

Every analysis and plotting tool in this directory resolves its database through
`resolve_db()`. The rule it enforces, mechanically rather than by convention:

    A paper number is computed from the PINNED frozen snapshot, never from a live
    ENGRAM graph.

This matters because the live graph moves under you. Ch6 §6.4 already carries a
note that an earlier reading described the graph's deepest derivation chain as five
layers, true of a graph a quarter the size — a number that was correct when written
and silently false a few months later. A frozen, hash-pinned snapshot is what makes
a figure re-runnable by a reviewer and what makes "this number is wrong" a
checkable claim rather than an argument about when it was measured.

Three refusals, each loud:

1. **A live graph.** Any path under `~/.engram/` (or `$ENGRAM_HOME`) is refused
   outright. `freeze_paper_snapshot.py` is the one legitimate reader of the live
   graph and does not use this module.
2. **A hash mismatch.** The snapshot's SHA-256 must equal the one recorded in
   `dataset/DATASET.md`. A snapshot that has been regenerated, truncated or
   swapped fails here instead of silently producing different numbers.
3. **A missing pin.** If `DATASET.md` records no hash, we refuse rather than
   proceed unverified — an unpinned run is exactly the state this module exists
   to make impossible.

`--allow-unpinned` exists as a deliberate, noisy escape for the case where the
snapshot is being deliberately replaced. It prints what it is doing.
"""

from __future__ import annotations

import hashlib
import os
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATASET = REPO / "dataset"
MANIFEST = DATASET / "DATASET.md"

_SHA_RE = re.compile(r"\*\*sha256:\*\*\s*`([0-9a-f]{64})`")


def _live_roots() -> list[Path]:
    roots = [Path(os.environ.get("ENGRAM_HOME", "~/.engram")).expanduser()]
    roots.append(Path("~/.engram").expanduser())
    return [r.resolve() for r in roots if r.exists()]


def pinned_sha() -> str | None:
    """The SHA-256 the manifest declares for the paper's SSoT snapshot."""
    if not MANIFEST.exists():
        return None
    m = _SHA_RE.search(MANIFEST.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_db(explicit: str | None = None, *, allow_unpinned: bool = False) -> Path:
    """Return the database every paper number must be computed from.

    Refuses a live graph, a hash mismatch, or an absent pin. Raises SystemExit with
    a message naming the reason — never falls back silently.
    """
    if explicit:
        db = Path(explicit).expanduser().resolve()
        if not db.exists():
            raise SystemExit(f"SSoT: no such database: {db}")
    else:
        cands = sorted(DATASET.glob("engram-paper-ssot-*.db"))
        if not cands:
            raise SystemExit(
                "SSoT: no frozen snapshot in dataset/ — run tools/freeze_paper_snapshot.py first"
            )
        if len(cands) > 1:
            print(
                f"# SSoT: {len(cands)} snapshots present; using the newest ({cands[-1].name}). "
                "Retire the others or pass --db explicitly.",
                file=sys.stderr,
            )
        db = cands[-1].resolve()

    # (1) never a live graph
    for root in _live_roots():
        if root in db.parents or db == root:
            raise SystemExit(
                f"SSoT: refusing to read a LIVE ENGRAM graph ({db}).\n"
                "      Paper numbers are computed from the frozen snapshot in dataset/ only.\n"
                "      To make a new snapshot, use tools/freeze_paper_snapshot.py."
            )

    # (2)/(3) the pin
    want = pinned_sha()
    if allow_unpinned:
        print(f"# SSoT: --allow-unpinned — hash NOT verified for {db.name}", file=sys.stderr)
        return db
    if want is None:
        raise SystemExit(
            f"SSoT: {MANIFEST} records no sha256 pin, so {db.name} cannot be verified.\n"
            "      Record the hash in the manifest, or pass --allow-unpinned deliberately."
        )
    got = file_sha(db)
    if got != want:
        raise SystemExit(
            f"SSoT: HASH MISMATCH for {db.name}\n"
            f"      manifest: {want}\n"
            f"      actual:   {got}\n"
            "      The snapshot is not the one the paper's numbers were computed from.\n"
            "      Either restore it, or re-freeze and update dataset/DATASET.md."
        )
    return db


def add_db_arg(ap) -> None:
    """Standard --db / --allow-unpinned pair for every analysis tool."""
    ap.add_argument("--db", default=None,
                    help="frozen snapshot to read (default: the pinned one in dataset/)")
    ap.add_argument("--allow-unpinned", action="store_true",
                    help="skip the SHA-256 pin check — deliberate and noisy")


def connect(db: Path):
    """Open the pinned snapshot read-only, in a way that works for a READER.

    `mode=ro` is not sufficient. A snapshot taken from a WAL database still
    carries WAL mode in its header, so SQLite wants to create//touch the `-shm`
    and `-wal` side files next to it — and in a directory the reader cannot
    write, every read fails with "attempt to write a readonly database". The
    tools therefore worked for the directory's owner and for nobody else, which
    made this repo's reproducibility claim true only for the author.

    `immutable=1` tells SQLite the file cannot change underneath it, so it skips
    the side files entirely. That assumption is not a hope here: `resolve_db()`
    has already verified the file's SHA-256 against the manifest pin.

    Found by Kepler on 2026-09-20, reviewing the paper: all five instruments
    exited 1 on a hash-verified, readable file until he wrapped them.
    """
    return sqlite3.connect(f"file:{db}?mode=ro&immutable=1", uri=True)
