#!/usr/bin/env python3
"""strip_paper_snapshot.py - full paper SSoT in, stripped public release out.

Lei's ruling, 2026-10-13: "strip the snapshot and leave only structures that enables
the paper reported data stats analysis, commit the striped graph and the stripping
code we use as a tool to the repo as provenance."

The full SSoT is Borges's private ENGRAM graph and is never published. This tool
produces the one file that can be: the same `nodes` / `edges` structure the paper's
instruments read, with every free-text cell removed or reduced to a class label.
The instruments (`paper_stats`, `component_anatomy`, `connectivity_trend`,
`confidence_gradient_trend`, `evidence_provenance`, `modus_ponens_check`,
`make_figures`) print the same numbers from the stripped file as from the full one -
that equality is a test (`tests/test_stripped_snapshot.py`, cell C5).

WHAT IS KEPT (the keep-list is exact, and a test asserts it):

  nodes        id, type, created_at, confidence, is_current, status, quote_type,
               source_type, claim, source_url, metadata
  edges        id, source_id, target_id, relation, created_at
  release_meta key, value   (provenance of THIS file: source sha256, tool commit, ...)

WHAT IS EMPTIED BUT PRESENT (the instruments SELECT these columns):

  claim        always NULL (the instruments only DISPLAY claim text).
  source_url   `redacted:<class>` where <class> is what `evidence_provenance.ev_class`
               computes for the node; NULL stays NULL and '' stays ''. No host, path,
               query, filename or extension survives.
  metadata     only the keys reasoning_type, derivation_mode, source_class, as a
               canonical `json.dumps(sort_keys=True)` object. STATE IS PRESERVED:
               NULL stays NULL, '' stays '', JSON that does not parse becomes the one
               fixed sentinel `<unparseable>`, an object with none of the kept keys
               becomes `{}`.

The nodes.supersedes / nodes.superseded_by pointers are NOT kept: no instrument reads them
(`component_anatomy` reads the supersede RELATION, which survives as edges.relation =
'supersedes'). The rule is "leave only what the paper's reported statistics need".

EVERYTHING ELSE IS ABSENT: every other node column (quoted_text, interpretation,
logical_chain, recall_summary, embeddings, titles, names, ...), edge metadata, the FTS
and vector tables, edit/diagnostic history, focus and timing tables.

FAIL CLOSED. Every kept text value must be an id, an ISO timestamp, or a member of a
closed vocabulary (below). A value outside it - a new node type, a free-text status, a
non-numeric confidence - makes the tool REFUSE; it never copies the value and never
echoes it. The vocabularies are the leak gate's allowlist: extending one is a reviewed
code change, and `tests/test_stripped_snapshot.py` (C4) scans the output by VALUE.

TIME PRECISION. `--time-precision` says what the timestamps KEEP, on nodes AND edges:
  stored  the full value as stored: microseconds, so the exact write order survives
          (`YYYY-MM-DDTHH:MM:SS.ffffff+00:00`)
  second  whole seconds, the fraction dropped, the offset kept, nothing rounded
          (`YYYY-MM-DDTHH:MM:SS+00:00`); rows created in one second tie
  day     the date only (`YYYY-MM-DD`)
The default is `second` (the owner's ruling, 2026-10-13): the release carries the time of day to
the second and no sub-second write order. `stored` and `day` are options.

REFUSALS COME FIRST: input missing, output exists (unless --force), output directory
missing, output inside a live ENGRAM home or inside another repository's `data/`
directory, input not an ENGRAM store, input already a stripped release, an input whose
sha256 is not the manifest's SSoT pin (unless --allow-unpinned, which is stamped into
`release_meta`), or any value outside the vocabulary. Nothing is written until every
check has passed; the output appears atomically (written beside, then renamed).

DETERMINISM. Rows are copied in source order, the schema is fixed, nothing carries a
timestamp or a path, and the file is VACUUMed in `journal_mode=DELETE`, so two runs on
one input give byte-identical files (on one SQLite build: the file header records the
library version that wrote it).

Usage:
    python tools/strip_paper_snapshot.py --src PATH/engram-paper-ssot-<stamp>.db
        [--out data/engram-paper-ssot-<stamp>.stripped.db]
        [--time-precision {stored,second,day}] [--allow-unpinned] [--force]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ssot  # noqa: E402
import evidence_provenance  # noqa: E402  (the ONE definition of the source_url class)

REPO = Path(__file__).resolve().parents[1]
STRIPPED_SUFFIX = _ssot.STRIPPED_SUFFIX

# ── the closed vocabularies (the leak gate's allowlist) ──────────────────────────────
NODE_TYPES = (
    "observation_factual", "observation_predictive", "evidence", "derivation", "feeling_report",
    "question", "lesson", "conjecture", "cornerstone", "definition", "task", "goal", "person",
    "contradiction", "axiom", "prediction",
    "theory",  # named by the instruments' claim-bearing set; absent from the 2026-09-20 graph
)
RELATIONS = (
    "about", "acknowledged_derives_from", "cites", "contradicts", "derives_from", "exemplifies",
    "generalizes", "instantiates", "predicted_by", "resolves", "retracts", "serves", "subtask_of",
    "supersedes", "supported_by", "tensions",
)
QUOTE_TYPES = ("hard_data", "official_statement", "attributed_analysis", "personal_communication",
               "editorial")
STATUSES = ("active", "resolved", "partially_resolved", "retracted", "open", "done", "planned",
            "supported", "refuted", "blocked", "confirmed",
            "answered")  # paper_stats §6.5 tests for it; absent from the 2026-09-20 graph
SOURCE_TYPES = ("file", "web_page", "conversation")
# ENGRAM's derive tool documents exactly these reasoning types.
REASONING_TYPES = (
    "deductive_modus_ponens", "deductive_modus_tollens", "deductive_hypothetical_syllogism",
    "deductive_disjunctive", "deductive_reductio", "deductive_conjunction",
    "inductive_generalization", "inductive_enumeration", "inductive_statistical",
    "inductive_analogy", "inductive_causal", "abductive_best_explanation",
    "abductive_elimination", "authority_expert", "authority_consensus",
)
DERIVATION_MODES = ("chain", "corroboration")          # the legacy field
SOURCE_CLASSES = ("external", "introspective", "user_stated")   # engram_confidence.VALID_SOURCE_CLASSES
URL_PREFIX = evidence_provenance.URL_CLASS_PREFIX
URL_CLASSES = evidence_provenance.URL_CLASSES
UNPARSEABLE = "<unparseable>"
TIME_PRECISIONS = ("stored", "second", "day")
RELEASE_META_KEYS = ("source_sha256", "tool_commit", "time_precision", "command", "allow_unpinned")

KEPT_METADATA = {
    "reasoning_type": frozenset(REASONING_TYPES),
    "derivation_mode": frozenset(DERIVATION_MODES),
    "source_class": frozenset(SOURCE_CLASSES),
}

NODE_COLUMNS = ("id", "type", "created_at", "confidence", "is_current", "status", "quote_type",
                "source_type", "claim", "source_url", "metadata")
EDGE_COLUMNS = ("id", "source_id", "target_id", "relation", "created_at")
# Columns the SOURCE must carry (claim is never read: the output's claim is always NULL).
REQUIRED_NODE_SOURCE = tuple(c for c in NODE_COLUMNS if c != "claim")

_ID = re.compile(r"[a-z]{2}_[0-9]{4,}")
_TS = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})")
_TS_SECOND = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2})(?:\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})")
# The exact form each precision may emit (fullmatch): the vocabulary the output is held to.
TS_FORMS = {
    "stored": _TS,
    "second": re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(Z|[+-][0-9]{2}:[0-9]{2})"),
    "day": re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}"),
}

SCHEMA = (
    """CREATE TABLE nodes (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    created_at TEXT NOT NULL,
    confidence REAL,
    is_current INTEGER,
    status TEXT,
    quote_type TEXT,
    source_type TEXT,
    claim TEXT,
    source_url TEXT,
    metadata TEXT
)""",
    """CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    relation TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE (source_id, target_id, relation)
)""",
    """CREATE TABLE release_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
)""",
)
# Indexes: speed only. Every ordering the instruments print is a total order (a natural
# secondary key on each tie; cell C11 proves the output is identical with or without
# ANALYZE, with any index set, and in any physical row order), so which indexes ship does
# not affect a single printed line. These three cover the instruments' hot paths: the
# per-type scans (paper_stats, make_figures) and the edge walks by endpoint
# (modus_ponens_check joins edges by source_id; the component tools read both directions).
INDEXES = (
    "CREATE INDEX idx_nodes_type ON nodes(type)",
    "CREATE INDEX idx_edges_source ON edges(source_id)",
    "CREATE INDEX idx_edges_target ON edges(target_id)",
)


class Refusal(Exception):
    """A reason to stop BEFORE anything is written. Never carries a cell's value."""


# ── the mapping rules (pure functions; the tests pin each one) ───────────────────────

def url_class(url: str, source_type: str | None) -> str:
    """The class evidence_provenance.ev_class computes for this node's URL."""
    if url.startswith(URL_PREFIX):
        raise Refusal("source_url already carries a redaction token - input looks stripped already")
    return evidence_provenance.ev_class(url, source_type)


def strip_source_url(url, source_type):
    """NULL stays NULL, '' stays '', anything else becomes the class token alone."""
    if url is None or url == "":
        return url
    return f"{URL_PREFIX}{url_class(url, source_type)}"


def strip_metadata(m):
    """Keep reasoning_type / derivation_mode / source_class; preserve the cell's STATE."""
    if m is None or m == "":
        return m
    try:
        d = json.loads(m)
    except Exception:           # the instruments' own `except Exception` bucket
        return UNPARSEABLE
    if not isinstance(d, dict):
        raise Refusal(
            "metadata parses as JSON but is not an object; the instruments disagree on how to "
            "treat that, so there is no state-preserving mapping")
    kept = {k: d[k] for k in KEPT_METADATA if k in d}
    for k, v in kept.items():
        if not isinstance(v, str) or v not in KEPT_METADATA[k]:
            raise Refusal(f"metadata key {k!r} holds a value outside its closed vocabulary")
    return json.dumps(kept, sort_keys=True)


def strip_time(ts, precision: str):
    if ts is None:
        return None
    if not isinstance(ts, str) or not _TS.fullmatch(ts):
        raise Refusal("created_at holds a value that is not an ISO timestamp")
    if precision == "day":
        out = ts[:10]
    elif precision == "second":
        out = _TS_SECOND.fullmatch(ts).expand(r"\1\2")     # fraction dropped, offset kept
    else:
        out = ts
    if not TS_FORMS[precision].fullmatch(out):
        raise Refusal(f"created_at is not in the {precision} form")
    return out


def generation_command(precision: str, allow_unpinned: bool) -> str:
    """A path-free record of how the file was made (a path would leak the user's home)."""
    return ("python tools/strip_paper_snapshot.py --src <full-ssot> --out <stripped> "
            f"--time-precision {precision}" + (" --allow-unpinned" if allow_unpinned else ""))


def tool_commit() -> str:
    """HEAD of the repository the tool ran in, `+dirty` if tools/ differs from it."""
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                              text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "tools"], cwd=REPO,
                               capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        return "unknown"
    return head + ("+dirty" if dirty else "")


# ── refusals ─────────────────────────────────────────────────────────────────────────

def _under(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _repo_root_of(path: Path):
    for a in (path, *path.parents):
        if (a / ".git").exists():
            return a
    return None


def check_locations(src: Path, out: Path, force: bool) -> None:
    if not src.exists():
        raise Refusal(f"no such database: {src}")
    if not out.parent.is_dir():
        raise Refusal(f"output directory does not exist: {out.parent}")
    if out.is_dir():
        raise Refusal(f"output path is a directory: {out}")
    if out.exists() and not force:
        raise Refusal(f"output exists: {out} (pass --force to overwrite)")
    outd = out.parent.resolve()
    for root in _ssot._live_roots():
        if _under(outd, root) or _under(src.resolve(), root):
            raise Refusal(f"refusing to touch a LIVE ENGRAM home ({root})")
    root = _repo_root_of(outd)
    if root is not None and root.resolve() != REPO.resolve():
        data = root.resolve() / "data"
        if _under(outd, data):
            raise Refusal(f"output is inside the private data dir of a different repository ({data})")


def open_source(src: Path) -> sqlite3.Connection:
    try:
        con = sqlite3.connect(f"file:{src}?mode=ro&immutable=1", uri=True)
        tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    except sqlite3.DatabaseError:
        raise Refusal("input is not an ENGRAM store: not a readable SQLite database (no nodes table)")
    if "release_meta" in tables:
        raise Refusal("input is already a stripped release (has release_meta); strip the full SSoT")
    if "nodes" not in tables or "edges" not in tables:
        raise Refusal("input is not an ENGRAM store: no nodes/edges tables")
    for table, need in (("nodes", REQUIRED_NODE_SOURCE), ("edges", EDGE_COLUMNS)):
        have = {r[1] for r in con.execute(f"PRAGMA table_info({table})")}
        missing = [c for c in need if c not in have]
        if missing:
            raise Refusal(f"input is not an ENGRAM store: {table} lacks columns {missing}")
    return con


def check_pin(src: Path, allow_unpinned: bool) -> str:
    got = _ssot.file_sha(src)
    if allow_unpinned:
        print(f"# strip: --allow-unpinned - source sha256 NOT checked against the manifest ({got})",
              file=sys.stderr)
        return got
    want = _ssot.pinned_sha()
    if want is None:
        raise Refusal(f"{_ssot.MANIFEST} records no sha256 pin for the full SSoT")
    if got != want:
        raise Refusal(
            f"HASH MISMATCH - input sha256 {got} is not the manifest's SSoT pin {want}\n"
            "      pass --allow-unpinned only if you are deliberately stripping a different snapshot")
    return got


# ── building the rows (all validation happens here, before any write) ────────────────

def build_rows(con: sqlite3.Connection, precision: str):
    bad: dict[str, int] = {}
    row_bad = [False]

    def flag(col):
        bad[col] = bad.get(col, 0) + 1
        row_bad[0] = True

    nodes = []
    cols = ", ".join(REQUIRED_NODE_SOURCE)
    for (id_, type_, created, conf, cur, status, qt, stype, url, md) in \
            con.execute(f"SELECT {cols} FROM nodes ORDER BY rowid"):
        row_bad[0] = False
        if not (isinstance(id_, str) and _ID.fullmatch(id_)):
            flag("nodes.id")
        if type_ not in NODE_TYPES:
            flag("nodes.type")
        if status is not None and status not in STATUSES:
            flag("nodes.status")
        if qt is not None and qt not in QUOTE_TYPES:
            flag("nodes.quote_type")
        if stype is not None and stype not in SOURCE_TYPES:
            flag("nodes.source_type")
        if conf is not None and (isinstance(conf, bool) or not isinstance(conf, (int, float))):
            flag("nodes.confidence")
        if cur is not None and (isinstance(cur, bool) or not isinstance(cur, int)):
            flag("nodes.is_current")
        if url is not None and not isinstance(url, str):
            flag("nodes.source_url")
        if md is not None and not isinstance(md, str):
            flag("nodes.metadata")
        if row_bad[0]:
            continue
        nodes.append((id_, type_, strip_time(created, precision), conf, cur, status,
                      qt, stype, None, strip_source_url(url, stype), strip_metadata(md)))
    edges = []
    for (eid, s, t, rel, created) in con.execute(
            "SELECT id, source_id, target_id, relation, created_at FROM edges ORDER BY id"):
        row_bad[0] = False
        if isinstance(eid, bool) or not isinstance(eid, int):
            flag("edges.id")
        for name, ref in (("source_id", s), ("target_id", t)):
            if not (isinstance(ref, str) and _ID.fullmatch(ref)):
                flag(f"edges.{name}")
        if rel not in RELATIONS:
            flag("edges.relation")
        if row_bad[0]:
            continue
        edges.append((eid, s, t, rel, strip_time(created, precision)))
    if bad:
        detail = ", ".join(f"{c} ({n} row(s))" for c, n in sorted(bad.items()))
        raise Refusal(f"values outside the closed vocabulary / type, not echoed: {detail}")
    return nodes, edges


# ── writing ──────────────────────────────────────────────────────────────────────────

def write_release(path: Path, nodes, edges, meta: dict[str, str]) -> None:
    if path.exists():
        path.unlink()
    con = sqlite3.connect(str(path), isolation_level=None)
    try:
        con.execute("PRAGMA page_size=4096")
        con.execute("PRAGMA journal_mode=DELETE")
        con.execute("BEGIN")
        for ddl in SCHEMA:
            con.execute(ddl)
        con.executemany(f"INSERT INTO nodes ({', '.join(NODE_COLUMNS)}) "
                        f"VALUES ({', '.join('?' * len(NODE_COLUMNS))})", nodes)
        con.executemany(f"INSERT INTO edges ({', '.join(EDGE_COLUMNS)}) "
                        f"VALUES ({', '.join('?' * len(EDGE_COLUMNS))})", edges)
        con.executemany("INSERT INTO release_meta (key, value) VALUES (?, ?)",
                        [(k, meta[k]) for k in RELEASE_META_KEYS])
        for ddl in INDEXES:
            con.execute(ddl)
        con.execute("COMMIT")
        con.execute("VACUUM")
    finally:
        con.close()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True, help="the FULL paper SSoT (private; read-only)")
    ap.add_argument("--out", default=None,
                    help="stripped file to write (default: data/<src stem>.stripped.db)")
    ap.add_argument("--time-precision", choices=TIME_PRECISIONS, default="second",
                    help="what created_at KEEPS on nodes AND edges: stored = the full value as stored "
                         "(microseconds, so the exact write order); second = whole seconds, fraction "
                         "dropped; day = date only (default: second)")
    ap.add_argument("--allow-unpinned", action="store_true",
                    help="skip the sha256 pin check - deliberate, noisy, stamped into release_meta")
    ap.add_argument("--force", action="store_true", help="overwrite an existing output file")
    a = ap.parse_args(argv)

    src = Path(a.src).expanduser()
    out = Path(a.out).expanduser() if a.out else REPO / "data" / f"{src.stem}{STRIPPED_SUFFIX}"
    partial = out.with_name(out.name + ".partial")
    try:
        check_locations(src, out, a.force)
        con = open_source(src)
        sha = check_pin(src, a.allow_unpinned)
        nodes, edges = build_rows(con, a.time_precision)
        con.close()
        meta = {
            "source_sha256": sha,
            "tool_commit": tool_commit(),
            "time_precision": a.time_precision,
            "command": generation_command(a.time_precision, a.allow_unpinned),
            "allow_unpinned": "true" if a.allow_unpinned else "false",
        }
        # ---- every refusal is behind us: only now does anything touch the disk ----
        try:
            write_release(partial, nodes, edges, meta)
            os.replace(partial, out)
        finally:
            if partial.exists():
                partial.unlink()
    except Refusal as e:
        print(f"strip: REFUSED - {e}", file=sys.stderr)
        return 2

    h = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"stripped   {out}")
    print(f"sha256     {h}")
    print(f"size       {out.stat().st_size:,} bytes")
    print(f"nodes      {len(nodes):,}")
    print(f"edges      {len(edges):,}")
    print(f"precision  {a.time_precision}")
    print(f"source     sha256 {sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
