"""Contract tests for the stripped release of the paper's SSoT.

Written BEFORE `tools/strip_paper_snapshot.py` existed (contract-first, Lei's
2026-09-19 ruling). The spec is `2026-10-13-stripped-snapshot.md`; the cells
below are its C1-C9, plus C10 for the `_ssot.py` change and C11 (round 2) for the
total-order contract.

    C1  keep-list, exact            C6  timestamp precision flag
    C2  text columns emptied        C7  pinned input + release_meta
    C3  metadata, state-preserving  C8  determinism
    C4  no-text guarantee (by VALUE) C9  refusals come first
    C5  stats match (a) full-vs-stripped, (b) stripped-vs-golden
    C10 `_ssot.py` accepts the stripped file as a second declared artifact
    C11 every ORDER the instruments print is a TOTAL order: identical output whatever the
        planner statistics, the indexes, or the physical row order of the file

HOW TO READ THIS FILE.  The private full SSoT is read-only and lives outside
the repository.  Cells that need it SKIP with a reason when it is absent (CI,
every outside reader); everything else runs against a synthetic full-schema
fixture built here, or against the committed stripped release itself.

REGENERATING THE GOLDEN FILE (needs the private full SSoT):

    python tests/test_stripped_snapshot.py --regen-expected [--full PATH]

writes `data/expected_stats.json` from the FULL SSoT by exactly the commands
cell C5 runs on the stripped file.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import random
import re
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS = REPO_ROOT / "tools"
DATA = REPO_ROOT / "data"
STRIP_TOOL = TOOLS / "strip_paper_snapshot.py"
STRIPPED = DATA / "engram-paper-ssot-20260920T131330Z.stripped.db"
EXPECTED = DATA / "expected_stats.json"
FULL_DEFAULT = "/home/agent-borges/engram-paper/data/engram-paper-ssot-20260920T131330Z.db"
FULL = Path(os.environ.get("ENGRAM_PAPER_FULL_SSOT", FULL_DEFAULT))
CH6_TRACE_ID = "dv_0922"           # the worked chain ch6 §6.4 names

needs_full = pytest.mark.skipif(
    not FULL.exists(),
    reason=f"private full SSoT absent ({FULL}) - it is absent in CI and for every outside reader",
)

sys.path.insert(0, str(TOOLS))


def _load_tool(name: str):
    """Import tools/<name>.py lazily so a missing module fails ONE cell, not collection."""
    spec = importlib.util.spec_from_file_location(f"_under_test_{name}", TOOLS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with Path(p).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ─────────────────────────────────────────────────────────────────────────
# Independent oracles (deliberately NOT imported from the tool under test)
# ─────────────────────────────────────────────────────────────────────────

EXPECTED_NODE_COLS = {
    "id", "type", "created_at", "confidence", "is_current", "status", "quote_type",
    "source_type", "claim", "source_url", "metadata",
}
EXPECTED_EDGE_COLS = {"id", "source_id", "target_id", "relation", "created_at"}
EXPECTED_META_COLS = {"key", "value"}
EXPECTED_TABLES = {"nodes": EXPECTED_NODE_COLS, "edges": EXPECTED_EDGE_COLS,
                   "release_meta": EXPECTED_META_COLS}
EXPECTED_META_KEYS = {"source_sha256", "tool_commit", "time_precision", "command", "allow_unpinned"}
KEPT_MD_KEYS = ("reasoning_type", "derivation_mode", "source_class")
UNPARSEABLE = "<unparseable>"


def oracle_url_class(url, stype):
    """The rule evidence_provenance.ev_class implements, restated independently."""
    u = url or ""
    if u.endswith(".jsonl"):
        return "transcript"
    if stype == "conversation":
        return "transcript"
    if stype == "web_page":
        return "external"
    return "file"


def oracle_md_state(m):
    """How the tools' own code classifies a metadata cell: absent / unparseable / null / value."""
    if m is None:
        return ("null",)
    if m == "":
        return ("empty",)
    try:
        d = json.loads(m)
    except Exception:
        return ("unparseable",)
    if not isinstance(d, dict):
        return ("unparseable",)
    return ("value",) + tuple(sorted((k, repr(d[k])) for k in KEPT_MD_KEYS if k in d))


# ─────────────────────────────────────────────────────────────────────────
# Synthetic full-schema fixture
# ─────────────────────────────────────────────────────────────────────────

SECRET = "SECRETTEXT"      # every free-text cell in the fixture carries this marker

FULL_NODE_DDL = """
CREATE TABLE nodes (
    id TEXT PRIMARY KEY, type TEXT NOT NULL, claim TEXT, created_at TEXT NOT NULL,
    source_url TEXT, source_title TEXT, source_domain TEXT, content_snippet TEXT,
    evidence_id TEXT, quoted_text TEXT, interpretation TEXT, quote_type TEXT,
    status TEXT DEFAULT 'active', logical_chain TEXT, confidence REAL,
    confidence_history TEXT DEFAULT '[]', supersedes TEXT, superseded_by TEXT,
    is_current INTEGER DEFAULT 1, metadata TEXT DEFAULT '{}', embedding TEXT,
    source_type TEXT, recall_summary TEXT, recall_keywords TEXT, trigger_text TEXT
)"""
FULL_EDGE_DDL = """
CREATE TABLE edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT, source_id TEXT NOT NULL, target_id TEXT NOT NULL,
    relation TEXT NOT NULL, created_at TEXT NOT NULL, metadata TEXT,
    UNIQUE(source_id, target_id, relation)
)"""

_RT = ["inductive_generalization", "deductive_modus_ponens", "abductive_best_explanation",
       "inductive_analogy", "inductive_enumeration"]
_QT = ["hard_data", "official_statement", "attributed_analysis", "personal_communication",
       "editorial", None]
_SC = ["introspective", "external", "user_stated"]


def _ts(i: int, per_hour: float = 5.3) -> str:
    # a spread of full-precision timestamps across ~5 months, several per day
    from datetime import datetime, timedelta, timezone
    base = datetime(2026, 4, 9, 4, 8, 15, 121083, tzinfo=timezone.utc)
    return (base + timedelta(hours=per_hour * i)).isoformat()


def build_fixture_rows():
    nodes, edges = [], []

    def node(id_, type_, **kw):
        row = dict(id=id_, type=type_, claim=f"{SECRET} claim of {id_}", created_at=_ts(len(nodes)),
                   source_url=None, source_title=f"{SECRET} title", quoted_text=f"{SECRET} quote",
                   interpretation=f"{SECRET} interp", quote_type=None, status="active",
                   logical_chain=f"{SECRET} chain", confidence=None, supersedes=None,
                   superseded_by=None, is_current=1, metadata="{}", source_type=None,
                   recall_summary=f"{SECRET} summary", embedding=f"[0.1, 0.2, {SECRET}]")
        row.update(kw)
        nodes.append(row)

    ev = [
        ("ev_0001", "file:///home/someone/.claude/projects/-home-someone/abc.jsonl", None),
        ("ev_0002", "/home/someone/evidence-archive/sha256-deadbeef.jsonl", "file"),
        ("ev_0003", "https://example.com/secret/page?token=XYZ", "web_page"),
        ("ev_0004", "https://example.com/doc.pdf", "file"),
        ("ev_0005", "/home/someone/notes/private.md", "file"),
        ("ev_0006", "https://x.org/a.jsonl", "web_page"),          # .jsonl beats web_page
        ("ev_0007", "https://y.org/p", "conversation"),
        ("ev_0008", None, "conversation"),                          # NULL url, class from type
        ("ev_0009", "", "web_page"),                                # '' url stays ''
        ("ev_0010", None, None),
        ("ev_0011", "http://a.b/c", None),
        ("ev_0012", "https://gone.example/z", "web_page"),
        ("ev_0013", "https://pair.example/one", "web_page"),
        ("ev_0014", "/home/someone/pair/two.txt", "file"),
        ("ev_0015", "file:///x/y/z/pair3.jsonl", None),
    ]
    for id_, url, st in ev:
        node(id_, "evidence", source_url=url, source_type=st, is_current=0 if id_ == "ev_0012" else 1,
             metadata="{}")
    for i in range(1, 31):
        id_ = f"ob_{i:04d}"
        if i % 7 == 1:
            md = None
        elif i % 7 == 2:
            md = ""
        elif i % 7 == 3:
            md = "{bad json " + SECRET
        elif i % 7 == 4:
            md = "{}"
        else:
            md = json.dumps({"source_class": _SC[i % 3], "note": f"{SECRET} note"})
        node(id_, "observation_predictive" if i == 30 else "observation_factual",
             quote_type=_QT[i % len(_QT)], confidence=round(0.35 + (i % 13) * 0.05, 4),
             metadata=md, is_current=0 if i in (9, 10) else 1,
             status="retracted" if i == 9 else "active")
    for i in range(1, 41):
        id_ = f"dv_{i:04d}"
        rt = _RT[i % len(_RT)] if i <= 36 else _RT[1]
        md = json.dumps({"reasoning_type": rt, "warrant": f"{SECRET} warrant", "x": i})
        if i == 37:
            md = None
        elif i == 38:
            md = "{bad json " + SECRET
        elif i == 39:
            md = ""
        elif i == 40:
            md = json.dumps({"derivation_mode": "chain", "warrant": SECRET})
        node(id_, "derivation", confidence=None if i == 33 else round(0.4 + (i % 11) * 0.05, 4),
             metadata=md, is_current=0 if i in (35, 36) else 1,
             supersedes="dv_0035" if i == 37 else None, superseded_by="dv_0037" if i == 35 else None)
    for i, stt in enumerate(["open", "resolved", "answered", "partially_resolved", None, "open"], 1):
        node(f"qu_{i:04d}", "question", status=stt, confidence=None, metadata="{}")
    node("ls_0001", "lesson", metadata=json.dumps({"reasoning_type": "inductive_generalization"}))
    node("gl_0001", "goal", status="planned")
    node("df_0001", "definition")
    node("pn_0001", "person", metadata=json.dumps({"name": f"{SECRET} Name"}))

    def edge(s, t, rel, md=None):
        edges.append(dict(source_id=s, target_id=t, relation=rel,
                          created_at=_ts(len(edges), 3.1), metadata=md))

    for i in range(1, 37):
        edge(f"dv_{i:04d}", f"ob_{i % 20 + 1:04d}", "derives_from")
        if i > 1:
            edge(f"dv_{i:04d}", f"dv_{i - 1:04d}", "derives_from")
    edge("dv_0005", "dv_0005", "derives_from")                       # self loop
    edge("dv_0006", "dv_0035", "derives_from")                       # non-current premise
    for i in range(1, 21):
        edge(f"ob_{i:04d}", f"ev_{i % 8 + 1:04d}", "cites")
    for i in (21, 22, 23, 24):                                       # in the giant, never derived from
        edge(f"ob_{i:04d}", "ev_0001", "cites")
    edge("ob_0028", "ev_0013", "cites")                              # isolated (obs, evidence) pairs
    edge("ob_0029", "ev_0014", "cites")
    edge("ob_0030", "ev_0015", "cites")
    edge("dv_0037", "dv_0035", "supersedes", md=json.dumps({"why": f"{SECRET} why"}))
    edge("ls_0001", "ob_0001", "about")
    edge("qu_0001", "dv_0003", "about")
    edge("gl_0001", "dv_0001", "serves")
    edge("df_0001", "ob_0002", "about")
    edge("pn_0001", "ob_0003", "about")
    return nodes, edges


def make_full_fixture(path: Path) -> Path:
    nodes, edges = build_fixture_rows()
    con = sqlite3.connect(str(path))
    con.execute(FULL_NODE_DDL)
    con.execute(FULL_EDGE_DDL)
    con.execute("CREATE TABLE edit_history (id INTEGER PRIMARY KEY, node_id TEXT, note TEXT)")
    con.execute("INSERT INTO edit_history (node_id, note) VALUES ('ob_0001', ?)", (f"{SECRET} edit",))
    # The full file's indexes differ from the release's on purpose: no printed order may depend
    # on which indexes exist (cell C11), so full-vs-stripped equality also covers that.
    con.execute("CREATE INDEX idx_nodes_type ON nodes(type)")
    con.execute("CREATE INDEX idx_nodes_current ON nodes(is_current)")
    con.execute("CREATE INDEX idx_edges_source ON edges(source_id)")
    con.execute("CREATE INDEX idx_edges_target ON edges(target_id)")
    cols = list(nodes[0])
    con.executemany(
        f"INSERT INTO nodes ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
        [tuple(n[c] for c in cols) for n in nodes])
    ecols = list(edges[0])
    con.executemany(
        f"INSERT INTO edges ({','.join(ecols)}) VALUES ({','.join('?' * len(ecols))})",
        [tuple(e[c] for c in ecols) for e in edges])
    con.commit()
    con.close()
    return path


# ─────────────────────────────────────────────────────────────────────────
# Running the strip tool
# ─────────────────────────────────────────────────────────────────────────

def run_strip(src, out, *args, env_extra=None):
    env = dict(os.environ)
    env.update(env_extra or {})
    return subprocess.run(
        [sys.executable, str(STRIP_TOOL), "--src", str(src), "--out", str(out), *args],
        cwd=str(REPO_ROOT), capture_output=True, text=True, env=env)


def ro(path):
    return sqlite3.connect(f"file:{path}?mode=ro&immutable=1", uri=True)


@pytest.fixture(scope="module")
def synth_full(tmp_path_factory):
    return make_full_fixture(tmp_path_factory.mktemp("synth") / "full.db")


@pytest.fixture(scope="module")
def synth_day(tmp_path_factory, synth_full):
    out = tmp_path_factory.mktemp("synth_day") / "stripped.db"
    r = run_strip(synth_full, out, "--allow-unpinned", "--time-precision", "day")   # the option
    assert r.returncode == 0, r.stderr
    return out


@pytest.fixture(scope="module")
def synth_default(tmp_path_factory, synth_full):
    out = tmp_path_factory.mktemp("synth_default") / "stripped.db"
    r = run_strip(synth_full, out, "--allow-unpinned")           # NO precision flag: the default
    assert r.returncode == 0, r.stderr
    return out


@pytest.fixture(scope="module")
def synth_stored(tmp_path_factory, synth_full):
    out = tmp_path_factory.mktemp("synth_stored") / "stripped.db"
    r = run_strip(synth_full, out, "--allow-unpinned", "--time-precision", "stored")
    assert r.returncode == 0, r.stderr
    return out


@pytest.fixture(scope="module")
def synth_second(tmp_path_factory, synth_full):
    out = tmp_path_factory.mktemp("synth_second") / "stripped.db"
    r = run_strip(synth_full, out, "--allow-unpinned", "--time-precision", "second")
    assert r.returncode == 0, r.stderr
    return out


@pytest.fixture(params=["synthetic", "committed"])
def stripped_db(request, synth_default):
    """Cells C1-C4 hold for the tool's output on the fixture AND for the shipped file."""
    if request.param == "synthetic":
        return synth_default
    assert STRIPPED.exists(), f"the stripped release is not committed at {STRIPPED}"
    return STRIPPED


# ─────────────────────────────────────────────────────────────────────────
# C1  KEEP-LIST, exact
# ─────────────────────────────────────────────────────────────────────────

EXPECTED_INDEXES = {
    "idx_nodes_type": ("nodes", ["type"]),
    "idx_edges_source": ("edges", ["source_id"]),
    "idx_edges_target": ("edges", ["target_id"]),
}


def test_c1_tables_and_columns_are_exactly_the_keep_list(stripped_db):
    con = ro(stripped_db)
    objs = {(t, n) for t, n in con.execute(
        "SELECT type, name FROM sqlite_master WHERE name NOT LIKE 'sqlite_autoindex%'")}
    tables = {n for t, n in objs if t == "table"}
    assert tables == set(EXPECTED_TABLES), f"tables: {sorted(tables)}"
    for t, cols in EXPECTED_TABLES.items():
        got = {r[1] for r in con.execute(f"PRAGMA table_info({t})")}
        assert got == cols, f"{t}: extra={sorted(got - cols)} missing={sorted(cols - got)}"
    # no triggers / views / virtual tables; indexes are exactly the declared set
    assert {t for t, _ in objs} <= {"table", "index"}
    idx = {}
    for t, n in objs:
        if t == "index":
            tbl = con.execute("SELECT tbl_name FROM sqlite_master WHERE name=?", (n,)).fetchone()[0]
            idx[n] = (tbl, [r[2] for r in con.execute(f"PRAGMA index_info({n})")])
    assert idx == EXPECTED_INDEXES


def test_c1_rows_survive_one_to_one(synth_full, synth_day):
    f, s = ro(synth_full), ro(synth_day)
    assert s.execute("SELECT id FROM nodes ORDER BY rowid").fetchall() == \
        f.execute("SELECT id FROM nodes ORDER BY rowid").fetchall()
    assert s.execute("SELECT id, source_id, target_id, relation FROM edges ORDER BY id").fetchall() == \
        f.execute("SELECT id, source_id, target_id, relation FROM edges ORDER BY id").fetchall()
    for col in ("type", "confidence", "is_current", "status", "quote_type", "source_type"):
        assert s.execute(f"SELECT {col} FROM nodes ORDER BY rowid").fetchall() == \
            f.execute(f"SELECT {col} FROM nodes ORDER BY rowid").fetchall(), col


# ─────────────────────────────────────────────────────────────────────────
# C2  TEXT COLUMNS THE TOOLS SELECT: PRESENT BUT EMPTIED
# ─────────────────────────────────────────────────────────────────────────

def test_c2_claim_is_all_null(stripped_db):
    con = ro(stripped_db)
    assert con.execute("SELECT COUNT(*) FROM nodes WHERE claim IS NOT NULL").fetchone()[0] == 0
    assert con.execute("SELECT COUNT(*) FROM nodes").fetchone()[0] > 0


def test_c2_source_url_is_a_class_token_only(stripped_db):
    con = ro(stripped_db)
    toks = [r[0] for r in con.execute("SELECT source_url FROM nodes WHERE source_url IS NOT NULL")]
    bad = [t for t in toks if t != "" and not re.fullmatch(r"redacted:(transcript|external|file)", t)]
    assert not bad, f"{len(bad)} source_url cells are not a bare class token"


def test_c2_url_class_matches_the_rule_per_node(synth_full, synth_day):
    full = {i: (u, st) for i, u, st in ro(synth_full).execute(
        "SELECT id, source_url, source_type FROM nodes WHERE type='evidence'")}
    stripped = {i: (u, st) for i, u, st in ro(synth_day).execute(
        "SELECT id, source_url, source_type FROM nodes WHERE type='evidence'")}
    ep = _load_tool("evidence_provenance")
    assert set(full) == set(stripped)
    for i, (u, st) in full.items():
        want = oracle_url_class(u, st)
        assert ep.ev_class(*stripped[i]) == want, i          # the TOOL reads the token
        su = stripped[i][0]
        if u is None:
            assert su is None, i                             # NULL stays NULL
        elif u == "":
            assert su == "", i                               # '' stays ''
        else:
            assert su == f"redacted:{want}", i
        assert stripped[i][1] == st, i                       # source_type untouched


def test_c2_evidence_provenance_reads_the_token_and_still_reads_raw_urls():
    ep = _load_tool("evidence_provenance")
    assert ep.ev_class("redacted:transcript", None) == "transcript"
    assert ep.ev_class("redacted:external", "file") == "external"      # token beats source_type
    assert ep.ev_class("redacted:file", "conversation") == "file"
    with pytest.raises(ValueError):
        ep.ev_class("redacted:bogus", None)
    # raw-URL behaviour is unchanged
    assert ep.ev_class("x/y.jsonl", "web_page") == "transcript"
    assert ep.ev_class("https://a/b", "web_page") == "external"
    assert ep.ev_class(None, "conversation") == "transcript"
    assert ep.ev_class("/p/q.md", "file") == "file"


@needs_full
def test_c2_url_class_matches_the_rule_on_the_real_data():
    ep = _load_tool("evidence_provenance")
    full = {i: oracle_url_class(u, st) for i, u, st in ro(FULL).execute(
        "SELECT id, source_url, source_type FROM nodes WHERE type='evidence'")}
    got = {i: ep.ev_class(u, st) for i, u, st in ro(STRIPPED).execute(
        "SELECT id, source_url, source_type FROM nodes WHERE type='evidence'")}
    assert got == full and len(full) > 2000


# ─────────────────────────────────────────────────────────────────────────
# C3  METADATA: keep three keys, preserve STATE
# ─────────────────────────────────────────────────────────────────────────

def test_c3_metadata_state_is_preserved_per_node(synth_full, synth_day):
    full = dict(ro(synth_full).execute("SELECT id, metadata FROM nodes"))
    got = dict(ro(synth_day).execute("SELECT id, metadata FROM nodes"))
    assert set(full) == set(got)
    seen_states = set()
    for i, m in full.items():
        st = oracle_md_state(m)
        seen_states.add(st[0])
        assert oracle_md_state(got[i]) == st, (i, st, "stripped state differs")
        if m is None:
            assert got[i] is None, i
        elif m == "":
            assert got[i] == "", i
        elif st[0] == "unparseable":
            assert got[i] == UNPARSEABLE, i                  # the ONE fixed sentinel
        else:
            d = json.loads(m)
            kept = {k: d[k] for k in KEPT_MD_KEYS if k in d}
            assert got[i] == json.dumps(kept, sort_keys=True), i   # canonical, kept keys only
    assert {"null", "empty", "unparseable", "value"} <= seen_states   # the fixture covers every state


def test_c3_exact_canonical_forms(synth_day):
    con = ro(synth_day)
    md = dict(con.execute("SELECT id, metadata FROM nodes"))
    assert md["dv_0040"] == '{"derivation_mode": "chain"}'
    assert md["ob_0004"] == "{}"                              # '{}' stays '{}'
    assert md["dv_0001"] == '{"reasoning_type": "%s"}' % _RT[1]
    assert md["ob_0003"] == UNPARSEABLE
    assert md["dv_0038"] == UNPARSEABLE
    assert md["ob_0001"] is None and md["ob_0002"] == ""


@pytest.mark.parametrize("bad_metadata", ["[1, 2]", '"a string"', "null", "17"])
def test_c3_parseable_non_object_metadata_is_refused(tmp_path, bad_metadata):
    src = make_full_fixture(tmp_path / "f.db")
    c = sqlite3.connect(str(src))
    c.execute("UPDATE nodes SET metadata=? WHERE id='ob_0005'", (bad_metadata,))
    c.commit(); c.close()
    out = tmp_path / "o.db"
    r = run_strip(src, out, "--allow-unpinned")
    assert r.returncode != 0 and not out.exists()
    assert "metadata" in (r.stderr + r.stdout)


# ─────────────────────────────────────────────────────────────────────────
# C4  NO-TEXT GUARANTEE, by VALUE
# ─────────────────────────────────────────────────────────────────────────

_ID = re.compile(r"[a-z]{2}_[0-9]{4,}")
_TS = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}(T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2}))?")
_HEX64 = re.compile(r"[0-9a-f]{64}")
_COMMIT = re.compile(r"([0-9a-f]{40}(\+dirty)?|unknown)")


def vocabulary():
    """The closed vocabulary, built from the tool's own allowlists (which the cells above
    pin to the tools' code and to the real data)."""
    s = _load_tool("strip_paper_snapshot")
    plain = set()
    for name in ("NODE_TYPES", "RELATIONS", "QUOTE_TYPES", "STATUSES", "SOURCE_TYPES"):
        plain |= set(getattr(s, name))
    plain |= {f"{s.URL_PREFIX}{c}" for c in s.URL_CLASSES}
    plain |= {s.UNPARSEABLE, ""}
    plain |= set(s.TIME_PRECISIONS) | {"true", "false"}
    plain |= set(s.RELEASE_META_KEYS)
    md_vocab = {"reasoning_type": set(s.REASONING_TYPES), "derivation_mode": set(s.DERIVATION_MODES),
                "source_class": set(s.SOURCE_CLASSES)}
    commands = {s.generation_command(p, u) for p in s.TIME_PRECISIONS for u in (True, False)}
    return plain, md_vocab, commands


def leak_scan(db_path, vocab=None, precision=None):
    """Return a description (table.column, row key) of every TEXT cell whose VALUE is not
    an id, an ISO timestamp, a sha/commit stamp, or a member of the closed vocabulary.
    With `precision` given, a timestamp must have EXACTLY that mode's form (the tool's
    TS_FORMS); without it, any of the three forms passes.  The VALUE is deliberately not echoed."""
    plain, md_vocab, commands = vocab or vocabulary()
    ts_form = _TS if precision is None else _load_tool("strip_paper_snapshot").TS_FORMS[precision]
    con = ro(db_path)
    leaks = []
    node_ids = {r[0] for r in con.execute("SELECT id FROM nodes")}
    tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    for t in tables:
        cols = [r[1] for r in con.execute(f"PRAGMA table_info({t})")]
        for rowid, *vals in con.execute(f"SELECT rowid, {','.join(cols)} FROM {t}"):
            for col, v in zip(cols, vals):
                if v is None or isinstance(v, (int, float)):
                    continue
                where = f"{t}.{col} rowid={rowid}"
                if isinstance(v, bytes):
                    leaks.append(f"{where} (BLOB)")
                    continue
                if v in plain or v in commands:
                    continue
                if _ID.fullmatch(v) or ts_form.fullmatch(v) or _HEX64.fullmatch(v) or _COMMIT.fullmatch(v):
                    if col in ("source_id", "target_id") and v not in node_ids:
                        leaks.append(f"{where} (dangling id)")
                    continue
                if t == "nodes" and col == "metadata":
                    try:
                        d = json.loads(v)
                    except Exception:
                        d = None
                    if (isinstance(d, dict) and set(d) <= set(md_vocab)
                            and all(isinstance(x, str) and x in md_vocab[k] for k, x in d.items())
                            and json.dumps(d, sort_keys=True) == v):
                        continue
                leaks.append(where)
    return leaks


def test_c4_every_text_cell_is_id_timestamp_or_closed_vocabulary(stripped_db):
    mode = release_precision(stripped_db)
    leaks = leak_scan(stripped_db, precision=mode)
    assert not leaks, f"{len(leaks)} cell(s) carry a non-vocabulary value, first: {leaks[:5]}"


def test_c4_gate_can_fail_control(tmp_path, synth_day):
    """The leak gate must be able to FAIL: plant one claim string in a copy and see it red."""
    for col, rowid_sql, planted in [
        ("claim", "id='ob_0001'", "a real claim sentence about someone"),
        ("source_url", "id='ev_0003'", "https://example.com/secret"),
        ("metadata", "id='dv_0001'", '{"reasoning_type": "inductive_generalization", "warrant": "w"}'),
        ("status", "id='ob_0002'", "free text status"),
    ]:
        cp = tmp_path / f"leaky_{col}.db"
        shutil.copy(synth_day, cp)
        c = sqlite3.connect(str(cp))
        c.execute(f"UPDATE nodes SET {col}=? WHERE {rowid_sql}", (planted,))
        c.commit(); c.close()
        leaks = leak_scan(cp)
        assert len(leaks) == 1 and leaks[0].startswith(f"nodes.{col} "), (col, leaks)
    # an id-shaped value in the wrong place (dangling reference) is also caught
    cp = tmp_path / "dangling.db"
    shutil.copy(synth_day, cp)
    c = sqlite3.connect(str(cp)); c.execute("UPDATE edges SET target_id='zz_9999' WHERE id=1")
    c.commit(); c.close()
    assert any("dangling" in x for x in leak_scan(cp))
    # exact matching: a trailing newline must not smuggle a vocabulary word past the gate
    cp = tmp_path / "newline.db"
    shutil.copy(synth_day, cp)
    c = sqlite3.connect(str(cp)); c.execute("UPDATE nodes SET quote_type='hard_data\n' WHERE id='ob_0002'")
    c.commit(); c.close()
    assert leak_scan(cp)


def test_c4_no_fixture_text_survives_anywhere_in_the_file_bytes(synth_day):
    raw = Path(synth_day).read_bytes()
    for needle in (SECRET.encode(), b"someone", b"example.com", b"jsonl", b"deadbeef", b"warrant",
                   b"pair.example"):
        assert needle not in raw, needle


@needs_full
def test_c4_no_real_claim_text_survives_in_the_shipped_file_bytes():
    raw = STRIPPED.read_bytes()
    rng = random.Random(0)
    claims = [r[0] for r in ro(FULL).execute(
        "SELECT claim FROM nodes WHERE claim IS NOT NULL AND length(claim) > 40")]
    sample = rng.sample(claims, 400)
    hits = [i for i, c in enumerate(sample) if c[:30].encode() in raw]
    assert not hits
    urls = [r[0] for r in ro(FULL).execute("SELECT source_url FROM nodes WHERE source_url LIKE 'http%'")]
    assert not [u for u in urls[:300] if u.encode() in raw]


def test_c4_vocabulary_is_pinned_to_the_tools_and_the_real_data():
    plain, md_vocab, _ = vocabulary()
    s = _load_tool("strip_paper_snapshot")
    # code-side pins: values the tools themselves dispatch on must be admissible
    assert {"observation_factual", "observation_predictive", "derivation", "theory", "axiom",
            "conjecture", "evidence", "question"} <= set(s.NODE_TYPES)
    assert {"derives_from", "cites", "supersedes"} <= set(s.RELATIONS)
    assert {"resolved", "answered"} <= set(s.STATUSES)
    assert "deductive_modus_ponens" in md_vocab["reasoning_type"]
    assert md_vocab["source_class"] == {"introspective", "external", "user_stated"}
    assert md_vocab["derivation_mode"] == {"chain", "corroboration"}


@needs_full
def test_c4_every_real_value_is_inside_the_vocabulary():
    s = _load_tool("strip_paper_snapshot")
    con = ro(FULL)
    for col, vocab in (("type", s.NODE_TYPES), ("status", s.STATUSES), ("quote_type", s.QUOTE_TYPES),
                       ("source_type", s.SOURCE_TYPES)):
        vals = {r[0] for r in con.execute(f"SELECT DISTINCT {col} FROM nodes") if r[0] is not None}
        assert vals <= set(vocab), (col, sorted(vals - set(vocab)))
    rels = {r[0] for r in con.execute("SELECT DISTINCT relation FROM edges")}
    assert rels <= set(s.RELATIONS)


# ─────────────────────────────────────────────────────────────────────────
# C5  STATS MATCH
# ─────────────────────────────────────────────────────────────────────────
#
# EXCLUSIONS (every one is DISPLAY of claim text; no NUMBER is excluded - see
# test_c5_normalisers_exclude_claim_text_and_nothing_else):
#   * "# source: <path>"            - the database path differs by construction
#   * paper_stats section 6.4 rows  - trailing claim[:64] after depth/node/conf
#   * paper_stats section 6.5 rows  - trailing claim[:88] after node/conf
#   * paper_stats --trace text rows - trailing "| claim[:150]" after the numeric fields
#   * paper_stats --trace JSON      - the "claim" key of each row

R64 = re.compile(r"^\s+(\d+)\s+([a-z]{2}_\d+)\s+(\d\.\d\d|--)(?:\s{3}.*)?$")
R65 = re.compile(r"^    ([a-z]{2}_\d+)  (\d\.\d\d)  .*$")


def _drop_claim_key(o):
    if isinstance(o, dict):
        return {k: _drop_claim_key(v) for k, v in o.items() if k != "claim"}
    if isinstance(o, list):
        return [_drop_claim_key(v) for v in o]
    return o


def normalise(label: str, stdout: str):
    if label.endswith("_json"):
        return _drop_claim_key(json.loads(stdout))
    out, sect = [], ""
    for line in stdout.splitlines():
        if line.startswith("# source:"):
            continue
        if line.startswith("## "):
            sect = line
        if label.startswith("paper_stats") and "trace" in label and " | " in line:
            line = line.split(" | ", 1)[0]
        elif label == "paper_stats" and sect.startswith("## §6.4"):
            m = R64.match(line)
            if m:
                line = " ".join(m.groups())
        elif label == "paper_stats" and sect.startswith("## §6.5"):
            m = R65.match(line)
            if m:
                line = " ".join(m.groups())
        out.append(line)
    return out


def command_table(trace_id):
    return [
        ("paper_stats", "paper_stats.py", []),
        ("paper_stats_trace", "paper_stats.py", ["--trace", trace_id]),
        ("paper_stats_trace_json", "paper_stats.py", ["--trace", trace_id, "--json"]),
        ("paper_stats_trace_deepest", "paper_stats.py", ["--trace-deepest"]),
        ("paper_stats_trace_deepest_json", "paper_stats.py", ["--trace-deepest", "--json"]),
        ("component_anatomy", "component_anatomy.py", []),
        ("connectivity_trend", "connectivity_trend.py", []),
        ("connectivity_trend_trim_control_json", "connectivity_trend.py", ["--trim-control", "--json"]),
        ("confidence_gradient_trend", "confidence_gradient_trend.py", []),
        ("confidence_gradient_trend_cohort", "confidence_gradient_trend.py", ["--cohort"]),
        ("evidence_provenance", "evidence_provenance.py", []),
        ("modus_ponens_check", "modus_ponens_check.py", []),
    ]


def run_commands(db, trace_id, *, pinned: bool, tolerate_errors: bool = False):
    """{label: normalised output} for every tool command, one subprocess each.

    tolerate_errors (synthetic fixture only): a command that FAILS is recorded as its
    exception line, so "fails the same way on both files" is itself compared.  The one
    legitimate case is modus_ponens_check on a graph holding malformed metadata, where
    SQLite's json_extract raises - on the full file and, by design, on the stripped one."""
    res = {}
    for label, script, args in command_table(trace_id):
        argv = [sys.executable, str(TOOLS / script), "--db", str(db), *args]
        if not pinned:
            argv.append("--allow-unpinned")
        p = subprocess.run(argv, cwd=str(REPO_ROOT), capture_output=True, text=True)
        if p.returncode != 0 and tolerate_errors:
            res[label] = {"returncode": p.returncode, "error": p.stderr.strip().splitlines()[-1]}
            continue
        assert p.returncode == 0, f"{label} exited {p.returncode}: {p.stderr[-400:]}"
        res[label] = normalise(label, p.stdout)
    return res


def run_make_figures(db, only=None):
    """make_figures prints the numbers its plots carry.  matplotlib is not needed for
    those numbers, so it is stubbed: every figure function runs for real, only the
    drawing calls are absorbed.  Returns {fig_name: [lines]}.  `only`: a set of function
    names to run (the default runs all six)."""
    plt = mock.MagicMock()
    plt.subplots.side_effect = lambda *a, **k: (mock.MagicMock(), mock.MagicMock())
    mpl = mock.MagicMock()
    spec = importlib.util.spec_from_file_location("_under_test_make_figures", TOOLS / "make_figures.py")
    mod = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {"matplotlib": mpl, "matplotlib.pyplot": plt}):
        spec.loader.exec_module(mod)
    mod.plt = plt
    con = mod._ssot.connect(Path(db))
    out = {}
    scratch = Path(os.environ.get("TMPDIR", "/tmp"))
    for fn in (mod.fig_reasoning_type, mod.fig_node_type, mod.fig_quote_type,
               mod.fig_depth, mod.fig_growth, mod.fig_census):
        if only is None or fn.__name__ in only:
            out[fn.__name__] = fn(con, scratch).splitlines()
    return out


def run_all(db, trace_id, *, pinned, figures=True):
    res = run_commands(db, trace_id, pinned=pinned)
    if figures:
        res["make_figures"] = run_make_figures(db)
    return res


def test_c5_normalisers_exclude_claim_text_and_nothing_else():
    full = ("## §6.4 Derivation chain depth\n  derives_from edges used  5\n  max depth                12\n"
            "   depth  node         conf   claim\n"
            "      12  dv_0922       0.55   a claim with 77 numbers 0.99\n")
    strp = full.replace("a claim with 77 numbers 0.99", "")
    assert normalise("paper_stats", full) == normalise("paper_stats", strp)
    # but a changed NUMBER is never absorbed
    for changed in (full.replace("      12  dv_0922", "      11  dv_0922"),
                    full.replace("0.55", "0.56"), full.replace("max depth                12",
                                                                "max depth                13")):
        assert normalise("paper_stats", changed) != normalise("paper_stats", strp)
    f65 = "## §6.5 Metacognitive surface\n    dv_0007  0.12  some claim 42\n"
    assert normalise("paper_stats", f65) == normalise("paper_stats", f65.replace("some claim 42", ""))
    assert normalise("paper_stats", f65) != normalise("paper_stats", f65.replace("0.12", "0.13"))
    tr = "dv_0922   d=12 derivation    deductive_modus_ponens       conf=0.55 prem=2 minprem=0.6 | words 9\n"
    assert normalise("paper_stats_trace", tr) == normalise("paper_stats_trace", tr.replace("words 9", ""))
    assert normalise("paper_stats_trace", tr) != normalise("paper_stats_trace", tr.replace("prem=2", "prem=3"))
    js = json.dumps({"traces": [{"start": "dv_1", "depth": 3, "rows": [{"id": "dv_1", "claim": "x 1", "n": 2}]}]})
    js2 = json.dumps({"traces": [{"start": "dv_1", "depth": 3, "rows": [{"id": "dv_1", "claim": None, "n": 2}]}]})
    js3 = json.dumps({"traces": [{"start": "dv_1", "depth": 4, "rows": [{"id": "dv_1", "claim": None, "n": 2}]}]})
    assert normalise("x_json", js) == normalise("x_json", js2) != normalise("x_json", js3)


_ISO_TS = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2})(T[0-9]{2}:[0-9]{2}:[0-9]{2})(?:\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})")


def at_precision(o, precision: str):
    """Every ISO timestamp STRING inside `o` (a list of lines, a dict, a scalar), cut to `precision`:
    `stored` leaves it, `second` drops the fraction (offset kept, nothing rounded), `day` keeps the
    date.  Applied to BOTH sides of a comparison, so it equalises the fractional digits a release
    made at `precision` cannot carry and nothing else: it touches only text that is a complete ISO
    timestamp, never a number, and a timestamp that differs at or above `precision` still differs."""
    if isinstance(o, str):
        if precision == "stored":
            return o
        return _ISO_TS.sub(r"\1" if precision == "day" else r"\1\2\3", o)
    if isinstance(o, list):
        return [at_precision(v, precision) for v in o]
    if isinstance(o, dict):
        return {k: at_precision(v, precision) for k, v in o.items()}
    return o


def release_precision(db) -> str:
    """The precision a release says it was made at: its own release_meta stamp."""
    return dict(ro(db).execute("SELECT key, value FROM release_meta"))["time_precision"]


def test_c5_timestamp_normaliser_hides_the_fraction_and_nothing_else():
    """The golden file is the true output of the FULL snapshot (fractions and all).  The C5
    comparison cuts every ISO timestamp on BOTH sides to the release's precision (release_meta)
    before comparing, so the three lines that PRINT a timestamp compare at the precision the
    release carries.  This cell shows what that cannot hide: a number, or a timestamp that
    differs at or above that precision."""
    line = "  first node               2026-04-09T04:08:15.121083+00:00"
    whole = "  first node               2026-04-09T04:08:15+00:00"
    assert at_precision([line], "second") == at_precision([whole], "second")      # the fraction: hidden
    assert at_precision([line], "stored") != at_precision([whole], "stored")      # ...only at `second`
    for changed in (line.replace(":15.", ":16."),            # a changed whole second
                    line.replace("04:08:15", "04:09:15"),    # a changed minute
                    line.replace("2026-04-09", "2026-04-10"),
                    line.replace("+00:00", "+01:00")):       # a changed offset
        assert at_precision([changed], "second") != at_precision([whole], "second"), changed
    # a planted NUMERIC difference still fails, alone and beside a timestamp
    assert at_precision(["  pair observations 639 33.6 42.4% 253"], "second") != \
        at_precision(["  pair observations 639 33.7 42.4% 253"], "second")
    both = "age reference: 2026-09-20T13:12:41.385290+00:00 median 33.6"
    assert at_precision([both], "second") != at_precision([both.replace("33.6", "33.7")], "second")
    assert at_precision([both], "second") == at_precision([both.replace(".385290", ".000001")], "second")
    # the JSON shape (trim-control) and the day option
    js = {"control": [{"control_share_pct": 77.7, "at": "2026-09-20T13:12:41.385290+00:00"}]}
    assert at_precision(js, "second")["control"][0]["control_share_pct"] == 77.7
    assert at_precision(js, "second") != at_precision(
        {"control": [{"control_share_pct": 77.8, "at": "2026-09-20T13:12:41+00:00"}]}, "second")
    assert at_precision(["2026-09-20T13:12:41.5Z"], "day") == ["2026-09-20"]


@pytest.fixture(scope="module")
def synth_results(synth_full, synth_stored, synth_second, synth_day):
    kw = dict(pinned=False, tolerate_errors=True)
    full = run_commands(synth_full, "dv_0030", **kw)
    return full, {"stored": run_commands(synth_stored, "dv_0030", **kw),
                  "second": run_commands(synth_second, "dv_0030", **kw),
                  "day": run_commands(synth_day, "dv_0030", **kw)}


def test_c5_synthetic_fixture_stripped_equals_full_at_stored_precision(synth_results):
    full, strp = synth_results
    assert strp["stored"] == full


def test_c5_synthetic_fixture_nontrivial(synth_results):
    """Guard against a vacuous comparison: the fixture must exercise the unparseable and
    absent buckets, the evidence classes, and the anatomy pairs."""
    full, _ = synth_results
    ps = "\n".join(full["paper_stats"])
    assert "<unparseable>" in ps and "<absent>" in ps
    ep = "\n".join(full["evidence_provenance"])
    assert "(unparseable)" in ep and "transcript" in ep and "external" in ep
    assert any("pair observations" in x for x in full["component_anatomy"])
    # modus_ponens_check dies on malformed metadata (SQLite json_extract); it must die identically
    assert full["modus_ponens_check"]["error"].endswith("malformed JSON")


@pytest.fixture(scope="module")
def real_full_results():
    if not FULL.exists():
        pytest.skip(f"private full SSoT absent ({FULL})")
    return run_all(FULL, CH6_TRACE_ID, pinned=True)


@pytest.fixture(scope="module")
def real_stripped_results(tmp_path_factory, request):
    """The stripped file the tool produces from the real SSoT: with NO precision flag (the
    default, key "default") and with the explicit `day` option (key "day")."""
    if not FULL.exists():
        pytest.skip(f"private full SSoT absent ({FULL})")
    outs = {}
    for key, flags in (("default", ()), ("stored", ("--time-precision", "stored")),
                       ("second", ("--time-precision", "second")), ("day", ("--time-precision", "day"))):
        out = tmp_path_factory.mktemp(f"real_{key}") / "stripped.db"
        r = run_strip(FULL, out, *flags)
        assert r.returncode == 0, r.stderr
        outs[key] = run_all(out, CH6_TRACE_ID, pinned=False)
        if key == "default":
            assert dict(ro(out).execute("SELECT key, value FROM release_meta"))["time_precision"] == DEFAULT_PRECISION
    return outs


DEFAULT_PRECISION = "second"      # the tool's default and the committed release's precision (owner, 2026-10-13)
ALL_LABELS = [lbl for lbl, _, _ in command_table("x")] + ["make_figures"]

# C6 FINDING.  The owner ruled (2026-10-13) that the release carries whole-second timestamps, so the
# DEFAULT is `--time-precision second`.  Every NUMBER is reproduced there; the comparison cuts the
# timestamps on both sides to the release's precision (`at_precision`).  The `day` option still exists; at `--time-precision day` these reported numbers differ from the
# full SSoT's and nothing else does.  Each entry is (where, full-SSoT value, day-precision value);
# `where` is the output line index, or the dotted JSON path.  They are pinned EXACTLY so that
# (1) the explicit-day cell below is marked xfail(strict) only for these labels and (2) any NEW
# divergence goes red.
#
#   paper_stats            the two DISPLAYED span endpoints lose their time of day
#   component_anatomy Q3   ages are measured in days from fractional-second timestamps
#   connectivity_trend --trim-control
#                          the oldest-removed control sorts nodes by FULL created_at (its own
#                          docstring: day-truncating that key moves the 2-week reading from 77.7%
#                          to 76.7%); this is the number ch6 section 6.2 prints
DAY_DELTAS = {
    "paper_stats": [
        (5, "  first node               2026-04-09T04:08:15.121083+00:00",
            "  first node               2026-04-09"),
        (6, "  last node                2026-09-20T13:12:41.385290+00:00",
            "  last node                2026-09-20"),
    ],
    "component_anatomy": [
        (46, "  age reference (newest current created_at): 2026-09-20T13:12:41.385290+00:00",
             "  age reference (newest current created_at): 2026-09-20T00:00:00+00:00"),
        (48, "  pair observations                          639      33.6     42.4%     253     217",
             "  pair observations                          639      34.0     42.9%     253     215"),
        (49, "  giant observations (all)                 3,837     109.4     20.5%   2,503   2,279",
             "  giant observations (all)                 3,837     109.0     20.7%   2,503   2,278"),
        (50, "  giant obs on no derives_from edge        1,968      83.7     27.0%   1,140     982",
             "  giant obs on no derives_from edge        1,968      84.0     27.2%   1,140     981"),
        (52, "  P(pair obs younger than a giant obs)              = 0.696  (0.5 = no difference)",
             "  P(pair obs younger than a giant obs)              = 0.695  (0.5 = no difference)"),
        (53, "  P(pair obs younger than an unreasoned giant obs)  = 0.632",
             "  P(pair obs younger than an unreasoned giant obs)  = 0.631"),
    ],
    "connectivity_trend_trim_control_json": [
        ("control.2.control_lcc_all", 7225, 7130),
        ("control.2.control_share_pct", 77.7, 76.7),
        ("control.4.control_lcc_all", 5912, 5913),
        ("control.8.control_lcc_all", 4480, 4483),
    ],
}
DAY_REASON = ("C6: this number differs at the non-default `day` precision (see DAY_DELTAS); "
              "the release is not made at day precision")


@needs_full
@pytest.mark.parametrize("label", [pytest.param(lbl, id=lbl) for lbl in ALL_LABELS])
def test_c5a_full_vs_stripped_default_precision(real_full_results, real_stripped_results, label):
    """The tool run with NO precision flag reproduces every number, DAY_DELTAS labels included.
    Both sides are cut to the default's precision first (`at_precision`): the full SSoT's three
    printed endpoints carry fractions the whole-second release cannot."""
    assert real_stripped_results["default"][label] == at_precision(real_full_results[label], DEFAULT_PRECISION), label


@needs_full
@pytest.mark.parametrize("label", [
    pytest.param(lbl, id=lbl, marks=pytest.mark.xfail(strict=True, reason=DAY_REASON))
    if lbl in DAY_DELTAS else pytest.param(lbl, id=lbl) for lbl in ALL_LABELS])
def test_c5a_full_vs_stripped_day_precision(real_full_results, real_stripped_results, label):
    assert real_stripped_results["day"][label] == real_full_results[label], label


@needs_full
@pytest.mark.parametrize("label", [pytest.param(lbl, id=lbl) for lbl in ALL_LABELS])
def test_c5a_full_vs_stripped_stored_precision(real_full_results, real_stripped_results, label):
    """`stored` is the source byte-for-byte, so it reproduces every golden line."""
    assert real_stripped_results["stored"][label] == real_full_results[label], label


# Whole-second truncation (measured 2026-10-13, round 5).  Every NUMBER the instruments report
# is unchanged (the 77.7% control, the Q3 ages 33.6 / 109.4 days, all counts); the ONLY lines
# that differ RAW are three that PRINT a timestamp, which lose their fractional digits.  Pinned
# exactly so any new divergence goes red; the comparison cells normalise those digits away.
SECOND_DELTAS = {
    "paper_stats": [
        (5, "  first node               2026-04-09T04:08:15.121083+00:00",
            "  first node               2026-04-09T04:08:15+00:00"),
        (6, "  last node                2026-09-20T13:12:41.385290+00:00",
            "  last node                2026-09-20T13:12:41+00:00"),
    ],
    "component_anatomy": [
        (46, "  age reference (newest current created_at): 2026-09-20T13:12:41.385290+00:00",
             "  age reference (newest current created_at): 2026-09-20T13:12:41+00:00"),
    ],
}


@needs_full
@pytest.mark.parametrize("label", [pytest.param(lbl, id=lbl) for lbl in ALL_LABELS])
def test_c5a_full_vs_stripped_second_precision(real_full_results, real_stripped_results, label):
    """Every number is reproduced; timestamps on both sides are cut to whole seconds first."""
    assert real_stripped_results["second"][label] == at_precision(real_full_results[label], "second"), label


@needs_full
def test_c6_second_precision_divergence_is_exactly_the_known_set(real_full_results, real_stripped_results):
    got = {lbl: delta(real_full_results[lbl], real_stripped_results["second"][lbl]) for lbl in ALL_LABELS}
    got = {k: v for k, v in got.items() if v}
    assert got == {k: [tuple(x) for x in v] for k, v in SECOND_DELTAS.items()}


@needs_full
def test_c6_day_precision_divergence_is_exactly_the_known_set(real_full_results, real_stripped_results):
    """Pinned: the deltas of the explicit `day` option are EXACTLY DAY_DELTAS."""
    got = {lbl: delta(real_full_results[lbl], real_stripped_results["day"][lbl]) for lbl in ALL_LABELS}
    got = {k: v for k, v in got.items() if v}
    assert got == {k: [tuple(x) for x in v] for k, v in DAY_DELTAS.items()}


@needs_full
def test_c5_reported_number_sanity_on_the_real_data(real_full_results):
    """The comparison is not vacuous: ch6's own figures are in the compared output."""
    ps = "\n".join(real_full_results["paper_stats"])
    assert "9,399 / 10,361 total" in ps and "17,208" in ps
    assert real_full_results["paper_stats_trace_json"]["traces"][0]["start"] == CH6_TRACE_ID


@pytest.fixture(scope="module")
def golden():
    assert STRIPPED.exists(), "stripped release not committed"
    assert EXPECTED.exists(), "data/expected_stats.json not committed"
    return json.loads(EXPECTED.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def release_results(golden):
    """The committed release, with its sha256 pin verified end to end (no --allow-unpinned)."""
    return json.loads(json.dumps(run_all(STRIPPED, golden["trace_id"], pinned=True)))


def test_c5b_golden_covers_every_command(golden, release_results):
    assert set(golden["commands"]) == set(ALL_LABELS) == set(release_results)
    assert all(golden["commands"][k] for k in ALL_LABELS), "an empty golden entry compares nothing"


@pytest.mark.parametrize("label", [pytest.param(lbl, id=lbl) for lbl in ALL_LABELS])
def test_c5b_committed_stripped_reproduces_the_golden_numbers(golden, release_results, label):
    """ALWAYS RUNS (no private data needed): the shipped release must reproduce the paper's
    numbers recorded in data/expected_stats.json.  The golden file is the true output of the FULL
    snapshot and is not edited; every ISO timestamp string on BOTH sides is cut to the release's
    own precision (release_meta) first, so only the fractional digits the release cannot carry are
    equalised (cell test_c5_timestamp_normaliser_hides_the_fraction_and_nothing_else)."""
    p = release_precision(STRIPPED)
    assert release_results[label] == at_precision(golden["commands"][label], p), label


def test_c6_release_diverges_from_the_golden_nowhere(golden, release_results):
    """After the same normalisation, no line and no key differs."""
    p = release_precision(STRIPPED)
    got = {lbl: delta(at_precision(golden["commands"][lbl], p), release_results[lbl]) for lbl in ALL_LABELS}
    assert {k: v for k, v in got.items() if v} == {}


def test_c6_release_raw_divergence_from_the_golden_is_exactly_the_three_timestamp_lines(golden, release_results):
    """The RAW (un-normalised) difference between the release and the golden file is SECOND_DELTAS:
    three printed timestamps and nothing else, so the normaliser above is hiding exactly that."""
    assert release_precision(STRIPPED) == "second"
    got = {lbl: delta(golden["commands"][lbl], release_results[lbl]) for lbl in ALL_LABELS}
    assert {k: v for k, v in got.items() if v} == {k: [tuple(x) for x in v] for k, v in SECOND_DELTAS.items()}


def test_c5b_golden_file_is_bound_to_the_pinned_artifacts():
    ssot = _load_tool("_ssot")
    gold = json.loads(EXPECTED.read_text(encoding="utf-8"))
    shas = ssot.pinned_shas()
    assert gold["source_sha256"] == shas["engram-paper-ssot-20260920T131330Z.db"]
    assert gold["trace_id"] == CH6_TRACE_ID
    assert gold["commands"]["paper_stats"], "golden file is empty"


def _flatten(o, prefix=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _flatten(v, f"{prefix}{k}.")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _flatten(v, f"{prefix}{i}.")
    else:
        yield prefix.rstrip("."), o


def delta(reference, got):
    """[(where, reference value, got value)] for everything that differs.  Same shape required:
    a missing / extra line or key is reported as such, never absorbed."""
    if isinstance(reference, list) and all(isinstance(x, str) for x in reference + got):
        if len(reference) != len(got):
            return [("<line count>", len(reference), len(got))]
        return [(i, a, b) for i, (a, b) in enumerate(zip(reference, got)) if a != b]
    a, b = dict(_flatten(reference)), dict(_flatten(got))
    return [(k, a.get(k, "<missing>"), b.get(k, "<missing>")) for k in sorted(set(a) | set(b))
            if a.get(k, "<missing>") != b.get(k, "<missing>")]


def regenerate_expected(full: Path) -> dict:
    ssot = _load_tool("_ssot")
    return {
        "_what": "Golden output of every command in tests/test_stripped_snapshot.py (C5), run on the "
                 "FULL private SSoT.  The stripped release must reproduce it exactly.  Claim-text "
                 "display is excluded; no number is.  Regenerate: python tests/test_stripped_snapshot.py "
                 "--regen-expected",
        "schema": 1,
        "source_sha256": ssot.file_sha(Path(full)),
        "trace_id": CH6_TRACE_ID,
        "commands": json.loads(json.dumps(run_all(full, CH6_TRACE_ID, pinned=True))),
    }


# ─────────────────────────────────────────────────────────────────────────
# C6  TIMESTAMP PRECISION
# ─────────────────────────────────────────────────────────────────────────

def test_c6_default_precision_is_whole_seconds(synth_full, synth_default, synth_second):
    s, f = ro(synth_default), ro(synth_full)
    for t, key in (("nodes", "rowid"), ("edges", "id")):
        got = s.execute(f"SELECT created_at FROM {t} ORDER BY {key}").fetchall()
        assert got == ro(synth_second).execute(f"SELECT created_at FROM {t} ORDER BY {key}").fetchall()
        assert got and not any("." in r[0] for r in got)                  # no sub-second digit survives
        assert any("." in r[0] for r in f.execute(f"SELECT created_at FROM {t}"))   # the control: the source has them
    meta = dict(s.execute("SELECT key, value FROM release_meta"))
    assert meta["time_precision"] == DEFAULT_PRECISION == "second"
    assert f"--time-precision {DEFAULT_PRECISION}" in meta["command"]


def test_c6_day_option_truncates_nodes_and_edges(synth_full, synth_day):
    s, f = ro(synth_day), ro(synth_full)
    for t in ("nodes", "edges"):
        vals = [r[0] for r in s.execute(f"SELECT created_at FROM {t}")]
        assert vals and all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", v) for v in vals), t
        want = [r[0][:10] for r in f.execute(f"SELECT created_at FROM {t} ORDER BY {'rowid' if t == 'nodes' else 'id'}")]
        got = [r[0] for r in s.execute(f"SELECT created_at FROM {t} ORDER BY {'rowid' if t == 'nodes' else 'id'}")]
        assert got == want
    assert dict(s.execute("SELECT key, value FROM release_meta"))["time_precision"] == "day"


def test_c6_stored_precision_equals_the_source_byte_for_byte(synth_full, synth_stored):
    s, f = ro(synth_stored), ro(synth_full)
    assert s.execute("SELECT created_at FROM nodes ORDER BY rowid").fetchall() == \
        f.execute("SELECT created_at FROM nodes ORDER BY rowid").fetchall()
    assert s.execute("SELECT created_at FROM edges ORDER BY id").fetchall() == \
        f.execute("SELECT created_at FROM edges ORDER BY id").fetchall()
    assert any("." in r[0] for r in s.execute("SELECT created_at FROM nodes"))     # the fixture has fractions
    meta = dict(s.execute("SELECT key, value FROM release_meta"))
    assert meta["time_precision"] == "stored" and "--time-precision stored" in meta["command"]


_WHOLE_SECOND = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(Z|[+-][0-9]{2}:[0-9]{2})")


def test_c6_second_precision_drops_the_fraction_keeps_the_offset_and_truncates(synth_full, synth_second):
    s, f = ro(synth_second), ro(synth_full)
    for t, key in (("nodes", "rowid"), ("edges", "id")):
        got = [r[0] for r in s.execute(f"SELECT created_at FROM {t} ORDER BY {key}")]
        src = [r[0] for r in f.execute(f"SELECT created_at FROM {t} ORDER BY {key}")]
        assert got and any("." in x for x in src)                     # the control: the source HAS fractions
        assert all("." not in x and _WHOLE_SECOND.fullmatch(x) for x in got), t
        assert got == [re.sub(r"\.[0-9]+", "", x) for x in src], t        # offset kept, nothing rounded
    assert dict(s.execute("SELECT key, value FROM release_meta"))["time_precision"] == "second"


@pytest.mark.parametrize("src,want", [
    ("2026-01-01T00:00:59.999999+00:00", "2026-01-01T00:00:59+00:00"),   # truncates, never rounds up
    ("2026-12-31T23:59:59.999999+00:00", "2026-12-31T23:59:59+00:00"),
    ("2026-01-01T00:00:00.5Z", "2026-01-01T00:00:00Z"),
    ("2026-01-01T10:20:30.123456-05:30", "2026-01-01T10:20:30-05:30"),
    ("2026-01-01T10:20:30+00:00", "2026-01-01T10:20:30+00:00"),          # no fraction: unchanged
])
def test_c6_strip_time_second_truncates(src, want):
    tool = _load_tool("strip_paper_snapshot")
    assert tool.strip_time(src, "second") == want
    assert tool.strip_time(src, "stored") == src
    assert tool.strip_time(src, "day") == src[:10]


def test_c6_second_precision_end_to_end_on_a_planted_59_999999(tmp_path, synth_full):
    r, out, d = _hostile_run(tmp_path, synth_full,
                             "UPDATE nodes SET created_at='2026-01-01T00:00:59.999999+00:00' WHERE id='ob_0005'",
                             (), "--time-precision", "second")
    assert r.returncode == 0, r.stderr
    assert ro(out).execute("SELECT created_at FROM nodes WHERE id='ob_0005'").fetchone() == \
        ("2026-01-01T00:00:59+00:00",)


_FORMS_OK = {
    "stored": ["2026-01-01T00:00:59.999999+00:00", "2026-01-01T00:00:59+00:00", "2026-01-01T00:00:59.5Z"],
    "second": ["2026-01-01T00:00:59+00:00", "2026-01-01T00:00:59Z"],
    "day": ["2026-01-01"],
}
_FORMS_BAD = {
    "stored": ["2026-01-01", "2026-01-01T00:00:59", "2026-01-01T00:00:59+00:00\n", "2026-01-01T00:00:59.+00:00"],
    "second": ["2026-01-01", "2026-01-01T00:00:59.999999+00:00", "2026-01-01T00:00:59.5Z",
               "2026-01-01T00:00:59+00:00\n", "2026-01-01T00:00:59"],
    "day": ["2026-01-01T00:00:59+00:00", "2026-01-01T00:00:59.999999+00:00", "2026-01-01\n", "2026-01"],
}


@pytest.mark.parametrize("mode", ["stored", "second", "day"])
def test_c6_each_modes_timestamp_form_accepts_its_own_and_rejects_the_others(mode):
    tool = _load_tool("strip_paper_snapshot")
    pat = tool.TS_FORMS[mode]
    assert all(pat.fullmatch(x) for x in _FORMS_OK[mode]), mode
    assert not any(pat.fullmatch(x) for x in _FORMS_BAD[mode]), mode


def test_c6_leak_scan_is_mode_exact(synth_stored, synth_second, synth_day):
    """The leak gate at mode M accepts M's timestamps and flags the other modes' forms."""
    assert not leak_scan(synth_stored, precision="stored")
    assert not leak_scan(synth_second, precision="second")
    assert not leak_scan(synth_day, precision="day")
    assert leak_scan(synth_stored, precision="second")          # fractions are not allowed at second
    assert leak_scan(synth_stored, precision="day")
    assert leak_scan(synth_second, precision="day")


def test_c6_bad_precision_is_refused(tmp_path, synth_full):
    out = tmp_path / "o.db"
    r = run_strip(synth_full, out, "--allow-unpinned", "--time-precision", "hour")
    assert r.returncode != 0 and not out.exists()


# ─────────────────────────────────────────────────────────────────────────
# C7  PINNED INPUT + release_meta
# ─────────────────────────────────────────────────────────────────────────

def test_c7_unpinned_input_is_refused_without_the_flag(tmp_path, synth_full):
    out = tmp_path / "o.db"
    r = run_strip(synth_full, out)
    assert r.returncode != 0
    assert not out.exists() and list(tmp_path.iterdir()) == []
    assert "sha256" in (r.stderr + r.stdout).lower() or "mismatch" in (r.stderr + r.stdout).lower()


def test_c7_release_meta_is_stamped(tmp_path, synth_full, synth_day):
    meta = dict(ro(synth_day).execute("SELECT key, value FROM release_meta"))
    assert set(meta) == EXPECTED_META_KEYS
    assert meta["source_sha256"] == sha256_file(synth_full)
    assert meta["time_precision"] == "day"
    assert meta["allow_unpinned"] == "true"                  # stamped: this run bypassed the pin
    assert re.fullmatch(r"[0-9a-f]{40}(\+dirty)?|unknown", meta["tool_commit"])
    assert meta["command"].startswith("python tools/strip_paper_snapshot.py")
    assert "--allow-unpinned" in meta["command"] and "--time-precision day" in meta["command"]
    # the command records NO path (a path would leak the generating user's home directory)
    assert "/" not in meta["command"].replace("tools/strip_paper_snapshot.py", "")
    assert str(tmp_path) not in meta["command"]


def test_c7_committed_release_records_the_pinned_source():
    ssot = _load_tool("_ssot")
    meta = dict(ro(STRIPPED).execute("SELECT key, value FROM release_meta"))
    assert set(meta) == EXPECTED_META_KEYS
    assert meta["source_sha256"] == ssot.pinned_shas()["engram-paper-ssot-20260920T131330Z.db"]
    assert meta["allow_unpinned"] == "false"
    assert meta["time_precision"] == "second"
    assert "--time-precision second" in meta["command"]
    assert re.fullmatch(r"[0-9a-f]{40}", meta["tool_commit"])         # generated from a clean tree
    assert "--allow-unpinned" not in meta["command"]


@needs_full
def test_c7_pinned_real_input_is_accepted(tmp_path):
    out = tmp_path / "o.db"
    r = run_strip(FULL, out)
    assert r.returncode == 0, r.stderr
    assert dict(ro(out).execute("SELECT key, value FROM release_meta"))["allow_unpinned"] == "false"


# ─────────────────────────────────────────────────────────────────────────
# C8  DETERMINISM
# ─────────────────────────────────────────────────────────────────────────

def test_c8_two_runs_are_byte_identical_and_self_contained(tmp_path, synth_full):
    a, b = tmp_path / "a" / "x.db", tmp_path / "b" / "x.db"
    a.parent.mkdir(); b.parent.mkdir()
    assert run_strip(synth_full, a, "--allow-unpinned").returncode == 0
    assert run_strip(synth_full, b, "--allow-unpinned").returncode == 0
    assert a.read_bytes() == b.read_bytes()
    assert sorted(p.name for p in a.parent.iterdir()) == ["x.db"]          # no -wal/-shm/journal
    con = sqlite3.connect(str(a))
    assert con.execute("PRAGMA journal_mode").fetchone()[0] == "delete"
    assert con.execute("PRAGMA freelist_count").fetchone()[0] == 0          # VACUUMed
    assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"


def test_c8_committed_file_is_single_self_contained_and_recorded_in_the_manifest():
    ssot = _load_tool("_ssot")
    assert not list(DATA.glob("*.stripped.db-*")), "a -wal/-shm sidecar is next to the release"
    con = sqlite3.connect(f"file:{STRIPPED}?mode=ro&immutable=1", uri=True)
    assert con.execute("PRAGMA journal_mode").fetchone()[0] == "delete"
    assert con.execute("PRAGMA freelist_count").fetchone()[0] == 0
    assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    name = STRIPPED.name
    assert sha256_file(STRIPPED) == ssot.pinned_shas()[name]
    text = (DATA / "DATASET.md").read_text(encoding="utf-8")
    assert f"{STRIPPED.stat().st_size:,} bytes" in text


@needs_full
def test_c8_regeneration_from_the_real_ssot_reproduces_the_release(tmp_path):
    out = tmp_path / "regen.db"
    assert run_strip(FULL, out).returncode == 0
    a, b = ro(out), ro(STRIPPED)
    for t, order in (("nodes", "rowid"), ("edges", "id")):
        assert a.execute(f"SELECT * FROM {t} ORDER BY {order}").fetchall() == \
            b.execute(f"SELECT * FROM {t} ORDER BY {order}").fetchall(), t
    ma = dict(a.execute("SELECT key, value FROM release_meta"))
    mb = dict(b.execute("SELECT key, value FROM release_meta"))
    ma.pop("tool_commit"); mb.pop("tool_commit")      # the commit the tool ran at is, by nature, different
    assert ma == mb


# ─────────────────────────────────────────────────────────────────────────
# C9  REFUSALS FIRST
# ─────────────────────────────────────────────────────────────────────────

def _assert_refused(tmp_dir: Path, out: Path, r, needle: str, before):
    assert r.returncode != 0, "tool should have refused"
    msg = (r.stderr + r.stdout).lower()
    assert needle in msg, msg[-300:]
    after = sorted(p.name for p in tmp_dir.iterdir())
    assert after == before, f"refusal wrote something: {set(after) ^ set(before)}"


def test_c9_input_missing(tmp_path):
    out = tmp_path / "out" / "o.db"
    out.parent.mkdir()
    before = []
    r = run_strip(tmp_path / "nope.db", out, "--allow-unpinned")
    _assert_refused(out.parent, out, r, "no such", before)


def test_c9_output_exists_is_not_overwritten_without_force(tmp_path, synth_full):
    out = tmp_path / "o.db"
    out.write_bytes(b"precious")
    r = run_strip(synth_full, out, "--allow-unpinned")
    _assert_refused(tmp_path, out, r, "exists", ["o.db"])
    assert out.read_bytes() == b"precious"
    r2 = run_strip(synth_full, out, "--allow-unpinned", "--force")
    assert r2.returncode == 0 and out.read_bytes() != b"precious"
    assert sorted(p.name for p in tmp_path.iterdir()) == ["o.db"]


def test_c9_output_inside_another_repos_private_data_dir(tmp_path, synth_full):
    other = tmp_path / "other-repo"
    (other / ".git").mkdir(parents=True)
    (other / "data").mkdir()
    out = other / "data" / "stripped.db"
    r = run_strip(synth_full, out, "--allow-unpinned")
    _assert_refused(other / "data", out, r, "data", [])
    sub = other / "data" / "deeper"
    sub.mkdir()
    r = run_strip(synth_full, sub / "s.db", "--allow-unpinned")
    _assert_refused(sub, out, r, "data", [])
    # a non-data directory of the same foreign repo is not the private data dir
    ok = other / "elsewhere"
    ok.mkdir()
    assert run_strip(synth_full, ok / "s.db", "--allow-unpinned").returncode == 0


def test_c9_output_inside_a_live_engram_home(tmp_path, synth_full):
    home = tmp_path / "live"
    home.mkdir()
    r = run_strip(synth_full, home / "s.db", "--allow-unpinned", env_extra={"ENGRAM_HOME": str(home)})
    _assert_refused(home, home / "s.db", r, "live", [])


def test_c9_output_directory_missing(tmp_path, synth_full):
    r = run_strip(synth_full, tmp_path / "no" / "such" / "o.db", "--allow-unpinned")
    assert r.returncode == 2 and "REFUSED" in r.stderr and "does not exist" in r.stderr   # a refusal, not a crash
    assert sorted(p.name for p in tmp_path.iterdir()) == []


def test_c9_input_not_an_engram_store(tmp_path):
    notdb = tmp_path / "in" / "x.db"
    notdb.parent.mkdir()
    c = sqlite3.connect(str(notdb))
    c.execute("CREATE TABLE other (a TEXT)"); c.commit(); c.close()
    out = tmp_path / "out"
    out.mkdir()
    r = run_strip(notdb, out / "o.db", "--allow-unpinned")
    _assert_refused(out, out / "o.db", r, "nodes", [])
    garbage = tmp_path / "in" / "g.db"
    garbage.write_bytes(b"this is not sqlite at all" * 100)
    r = run_strip(garbage, out / "o.db", "--allow-unpinned")
    _assert_refused(out, out / "o.db", r, "not", [])


def test_c9_stripped_file_is_not_an_acceptable_input(tmp_path, synth_day):
    out = tmp_path / "o.db"
    r = run_strip(synth_day, out, "--allow-unpinned")
    # refused for ITS OWN reason, not incidentally by a later check (a stripped file whose
    # source_url cells are all NULL would otherwise be stripped a second time)
    assert r.returncode == 2 and "already a stripped release" in r.stderr and not out.exists()


def test_c9_out_of_vocabulary_value_is_refused_not_leaked(tmp_path):
    src = make_full_fixture(tmp_path / "f.db")
    c = sqlite3.connect(str(src))
    c.execute("UPDATE nodes SET status='a free text status' WHERE id='ob_0005'")
    c.commit(); c.close()
    out = tmp_path / "o.db"
    r = run_strip(src, out, "--allow-unpinned")
    assert r.returncode != 0 and not out.exists()
    assert "status" in (r.stderr + r.stdout)
    assert "a free text status" not in (r.stderr + r.stdout)       # the value is not echoed


def test_c9_non_numeric_confidence_is_refused(tmp_path):
    src = make_full_fixture(tmp_path / "f.db")
    c = sqlite3.connect(str(src))
    c.execute("UPDATE nodes SET confidence='smuggled words' WHERE id='ob_0005'")
    c.commit(); c.close()
    out = tmp_path / "o.db"
    r = run_strip(src, out, "--allow-unpinned")
    assert r.returncode != 0 and not out.exists()


# ─────────────────────────────────────────────────────────────────────────
# C9b  EVERY VALUE-REFUSAL PATH CAN FAIL (round 3)
# ─────────────────────────────────────────────────────────────────────────
# Round 2 left three privacy gates (id, timestamp, metadata value) with no cell that could
# fail: loosening `fullmatch` to `match`, or deleting the vocabulary check, kept the whole
# suite green. The class is "a refusal path with no cell that fails when the path is
# removed", so EVERY path in the tool that guards what may reach the output has a
# hostile-input cell here, fed through the tool's real entry point (a subprocess on a copy of
# the synthetic full store with ONE value planted). The cell ids name the path.
#
# Every refusal cell asserts the same things: exit status exactly 2 (a REFUSAL, not a
# crash), the word REFUSED, the named column/path in the message, no output file, nothing
# else written beside it, and the hostile value is not echoed. A trailing-newline variant
# rides with every pattern or membership gate, because `re.match` and `re.fullmatch` differ
# exactly there.

HOSTILE = "SMUGGLED"


def _hostile_run(tmp_path, synth_full, sql, params=(), *args, prepare=None):
    """Copy the clean fixture, plant ONE hostile value, run the real tool, return the facts."""
    in_dir, out_dir = tmp_path / "in", tmp_path / "out"
    in_dir.mkdir()
    out_dir.mkdir()
    src, out = in_dir / "f.db", out_dir / "o.db"
    shutil.copy(synth_full, src)
    c = sqlite3.connect(str(src))
    if prepare:
        c.executescript(prepare)
    if sql:
        c.execute(sql, params)
    c.commit()
    c.close()
    r = run_strip(src, out, "--allow-unpinned", *args)
    return r, out, out_dir


def _assert_value_refused(r, out, out_dir, needle):
    said = r.stderr + r.stdout
    assert r.returncode == 2, f"expected a refusal (exit 2), got {r.returncode}: {said[-300:]}"
    assert "REFUSED" in r.stderr, said[-300:]
    assert needle in said, said[-300:]
    assert not out.exists()
    assert list(out_dir.iterdir()) == [], "a refusal left files behind"
    assert HOSTILE not in said, "the hostile value was echoed"


def _with_newline_variants(valid):
    return [f"{valid} {HOSTILE}", f"{valid}\n", f"{valid} ", f" {valid}", f"{valid}\n{HOSTILE}"]


_NODE_VOCAB_CASES = []
for _col, _valid in (("type", "lesson"), ("status", "active"), ("quote_type", "hard_data"),
                     ("source_type", "file")):
    for _bad in (f"{HOSTILE} {_col}", _valid.upper(), *_with_newline_variants(_valid), "",
                 _valid.encode()):
        _NODE_VOCAB_CASES.append(pytest.param(_col, _bad, id=f"{_col}-{_bad!r}"))


@pytest.mark.parametrize("col,bad", _NODE_VOCAB_CASES)
def test_c9b_node_column_outside_its_closed_vocabulary_is_refused(tmp_path, synth_full, col, bad):
    r, out, d = _hostile_run(tmp_path, synth_full, f"UPDATE nodes SET {col}=? WHERE id='ob_0005'", (bad,))
    _assert_value_refused(r, out, d, f"nodes.{col}")


_ID_CASES = [f"ob_0005 {HOSTILE}", "ob_0005\n", "ob_0005 ", " ob_0005", f"ob_0005\n{HOSTILE}", "OB_0005",
             "ob_005", "ob0005", "ob_0005x", "", b"ob_0005"]


@pytest.mark.parametrize("bad", [pytest.param(b, id=repr(b)) for b in _ID_CASES])
def test_c9b_node_id_must_be_exactly_an_id(tmp_path, synth_full, bad):
    r, out, d = _hostile_run(tmp_path, synth_full, "UPDATE nodes SET id=? WHERE id='ob_0005'", (bad,))
    _assert_value_refused(r, out, d, "nodes.id")


@pytest.mark.parametrize("col", ["source_id", "target_id"])
@pytest.mark.parametrize("bad", [pytest.param(b, id=repr(b)) for b in _ID_CASES])
def test_c9b_edge_endpoint_must_be_exactly_an_id(tmp_path, synth_full, col, bad):
    r, out, d = _hostile_run(tmp_path, synth_full, f"UPDATE edges SET {col}=? WHERE id=1", (bad,))
    _assert_value_refused(r, out, d, f"edges.{col}")


@pytest.mark.parametrize("bad", [pytest.param(b, id=repr(b)) for b in
                                 (f"{HOSTILE} relation", "CITES", *_with_newline_variants("cites"), "",
                                  b"cites")])
def test_c9b_edge_relation_outside_its_closed_vocabulary_is_refused(tmp_path, synth_full, bad):
    r, out, d = _hostile_run(tmp_path, synth_full, "UPDATE edges SET relation=? WHERE id=1", (bad,))
    _assert_value_refused(r, out, d, "edges.relation")


@pytest.mark.parametrize("bad", [pytest.param(b, id=repr(b)) for b in ("SMUGGLED", 1.5, b"1")])
def test_c9b_edge_id_must_be_an_integer(tmp_path, synth_full, bad):
    # The real store declares edges.id INTEGER PRIMARY KEY (which cannot hold text); the tool
    # only requires the COLUMN to exist, so a source with a loosely typed id column is reachable.
    prep = ("ALTER TABLE edges RENAME TO edges_old;"
            "CREATE TABLE edges (id, source_id TEXT NOT NULL, target_id TEXT NOT NULL,"
            " relation TEXT NOT NULL, created_at TEXT NOT NULL);"
            "INSERT INTO edges SELECT id, source_id, target_id, relation, created_at FROM edges_old;"
            "DROP TABLE edges_old;")
    r, out, d = _hostile_run(tmp_path, synth_full, "UPDATE edges SET id=? WHERE rowid=1", (bad,),
                             prepare=prep)
    _assert_value_refused(r, out, d, "edges.id")


@pytest.mark.parametrize("col,bad", [
    ("confidence", HOSTILE), ("confidence", f"0.5 {HOSTILE}"), ("confidence", b"0.5"),
    ("is_current", HOSTILE), ("is_current", 1.5), ("is_current", b"1"),
    ("source_url", b"https://x.example/"), ("metadata", b"{}"),
], ids=lambda v: repr(v))
def test_c9b_mistyped_cells_are_refused(tmp_path, synth_full, col, bad):
    # The hostile text values carry SMUGGLED; the blob / float ones have no text to echo.
    r, out, d = _hostile_run(tmp_path, synth_full, f"UPDATE nodes SET {col}=? WHERE id='ob_0005'", (bad,))
    _assert_value_refused(r, out, d, f"nodes.{col}")


def test_c9b_booleans_are_not_numbers():
    """sqlite3 never returns a bool, so these three guards are reachable only through a
    stand-in connection; the cell calls the tool's own build_rows with one."""
    tool = _load_tool("strip_paper_snapshot")

    class _Con:
        def __init__(self, node, edge):
            self.node, self.edge = node, edge

        def execute(self, sql):
            return iter([self.node] if "FROM nodes" in sql else [self.edge])

    ts = "2026-01-01T00:00:00+00:00"
    good_node = ("ob_0001", "lesson", ts, 0.5, 1, "active", None, None, None, None)
    good_edge = (1, "ob_0001", "ob_0002", "cites", ts)
    tool.build_rows(_Con(good_node, good_edge), "day")                       # control: this shape passes
    for i, name in ((3, "nodes.confidence"), (4, "nodes.is_current")):
        bad = list(good_node)
        bad[i] = True
        with pytest.raises(tool.Refusal, match=re.escape(name)):
            tool.build_rows(_Con(tuple(bad), good_edge), "day")
    with pytest.raises(tool.Refusal, match=re.escape("edges.id")):
        tool.build_rows(_Con(good_node, (True,) + good_edge[1:]), "day")


_TS_CASES = [f"2026-01-01T00:00:00Z {HOSTILE}", "2026-01-01T00:00:00Z\n", "2026-01-01T00:00:00Z ",
             " 2026-01-01T00:00:00Z", f"2026-01-01T00:00:00+00:00\n{HOSTILE}",
             "2026-01-01T00:00:00+00:00\n", "2026-01-01", "2026-01-01 00:00:00", "2026-01-01T00:00:00",
             HOSTILE, "", b"2026-01-01T00:00:00Z"]


@pytest.mark.parametrize("precision", ["day", "second"])
@pytest.mark.parametrize("table,where", [("nodes", "id='ob_0005'"), ("edges", "id=1")])
@pytest.mark.parametrize("bad", [pytest.param(b, id=repr(b)) for b in _TS_CASES])
def test_c9b_created_at_must_be_exactly_an_iso_timestamp(tmp_path, synth_full, table, where, bad, precision):
    r, out, d = _hostile_run(tmp_path, synth_full, f"UPDATE {table} SET created_at=? WHERE {where}",
                             (bad,), "--time-precision", precision)
    _assert_value_refused(r, out, d, "created_at")


_MD_VALID = {"reasoning_type": "inductive_analogy", "derivation_mode": "chain",
             "source_class": "external"}
_MD_CASES = []
for _k, _valid in _MD_VALID.items():
    for _bad in (f"{HOSTILE} text", _valid.upper(), *_with_newline_variants(_valid), "", None, 5, True,
                 [_valid], {"x": _valid}):
        _MD_CASES.append(pytest.param(_k, _bad, id=f"{_k}-{_bad!r}"))


@pytest.mark.parametrize("key,bad", _MD_CASES)
def test_c9b_metadata_value_outside_its_closed_vocabulary_is_refused(tmp_path, synth_full, key, bad):
    md = json.dumps({key: bad})
    r, out, d = _hostile_run(tmp_path, synth_full, "UPDATE nodes SET metadata=? WHERE id='dv_0001'", (md,))
    _assert_value_refused(r, out, d, f"metadata key '{key}'")


@pytest.mark.parametrize("bad", ["redacted:file", f"redacted:{HOSTILE}", "redacted:"])
def test_c9b_a_source_url_that_already_carries_a_redaction_token_is_refused(tmp_path, synth_full, bad):
    r, out, d = _hostile_run(tmp_path, synth_full,
                             "UPDATE nodes SET source_url=? WHERE id='ev_0003'", (bad,))
    _assert_value_refused(r, out, d, "redaction token")


def test_c9b_positive_control_the_planted_boundary_values_are_accepted(tmp_path, synth_full):
    """The hostile cells plant values with exactly this mechanism. This cell plants the VALID
    neighbours (each one the vocabulary or pattern allows) and must succeed, so a refusal
    above is a judgement about the VALUE, not a side effect of the planting."""
    r, out, d = _hostile_run(
        tmp_path, synth_full,
        "UPDATE nodes SET id='ob_9999', type='lesson', status='active', quote_type='hard_data',"
        " source_type='file', created_at='2026-01-01T00:00:00Z',"
        " metadata='{\"reasoning_type\": \"inductive_analogy\", \"derivation_mode\": \"chain\","
        " \"source_class\": \"external\"}' WHERE id='ob_0005'")
    assert r.returncode == 0, r.stderr
    got = ro(out).execute("SELECT type, status, created_at FROM nodes WHERE id='ob_9999'").fetchone()
    assert got == ("lesson", "active", "2026-01-01T00:00:00Z")      # default precision: second


# ── the location / input / pin refusals that had no cell ────────────────────────────────

def test_c9b_output_path_is_a_directory(tmp_path, synth_full):
    out = tmp_path / "o.db"
    out.mkdir()
    r = run_strip(synth_full, out, "--allow-unpinned", "--force")
    assert r.returncode == 2 and "REFUSED" in r.stderr and "directory" in r.stderr
    assert out.is_dir() and list(out.iterdir()) == []


def test_c9b_input_inside_a_live_engram_home(tmp_path, synth_full):
    home = tmp_path / "live"
    home.mkdir()
    src = home / "f.db"
    shutil.copy(synth_full, src)
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    r = run_strip(src, out_dir / "o.db", "--allow-unpinned", env_extra={"ENGRAM_HOME": str(home)})
    assert r.returncode == 2 and "LIVE" in r.stderr
    assert list(out_dir.iterdir()) == []


@pytest.mark.parametrize("prep,needle", [
    ("ALTER TABLE nodes DROP COLUMN status;", "lacks columns"),
    ("ALTER TABLE nodes DROP COLUMN metadata;", "lacks columns"),
    ("ALTER TABLE edges DROP COLUMN created_at;", "lacks columns"),
    ("DROP TABLE edges;", "nodes/edges"),
])
def test_c9b_input_missing_a_required_table_or_column(tmp_path, synth_full, prep, needle):
    r, out, d = _hostile_run(tmp_path, synth_full, None, (), prepare=prep)
    _assert_value_refused(r, out, d, needle)


def test_c9b_no_pin_in_the_manifest_is_a_refusal_not_a_pass(tmp_path, synth_full, monkeypatch, capsys):
    tool = _load_tool("strip_paper_snapshot")
    monkeypatch.setattr(tool._ssot, "pinned_sha", lambda: None)
    out = tmp_path / "o.db"
    assert tool.main(["--src", str(synth_full), "--out", str(out)]) == 2
    assert "no sha256 pin" in capsys.readouterr().err
    assert not out.exists()


# ─────────────────────────────────────────────────────────────────────────
# C10  _ssot.py: the stripped file is a second DECLARED artifact
# ─────────────────────────────────────────────────────────────────────────

def test_c10_manifest_declares_exactly_two_readable_artifacts():
    ssot = _load_tool("_ssot")
    shas = ssot.pinned_shas()
    assert set(shas) == {"engram-paper-ssot-20260920T131330Z.db",
                         "engram-paper-ssot-20260920T131330Z.stripped.db"}
    assert shas["engram-paper-ssot-20260920T131330Z.db"] == \
        "adaa6a84828b761ab2e5bf269e1ea4d48366c7e713b73c0c0918bf5ce3fbef85"
    assert ssot.pinned_sha() == shas["engram-paper-ssot-20260920T131330Z.db"]   # unchanged contract


def test_c10_resolve_db_accepts_the_stripped_release_and_refuses_everything_else(tmp_path, synth_full):
    ssot = _load_tool("_ssot")
    assert ssot.resolve_db(str(STRIPPED)) == STRIPPED.resolve()
    with pytest.raises(SystemExit) as e:
        ssot.resolve_db(str(synth_full))
    assert "HASH MISMATCH" in str(e.value)
    # the 07-04 freeze is declared in the manifest too, but is NOT a readable artifact
    assert not any("2026-07-04" in k for k in ssot.pinned_shas())


def test_c10_default_resolution_prefers_the_full_ssot_but_falls_back_to_the_stripped(tmp_path, monkeypatch):
    ssot = _load_tool("_ssot")
    monkeypatch.setattr(ssot, "DATASET", tmp_path)
    (tmp_path / "engram-paper-ssot-20260920T131330Z.db").write_bytes(b"x")
    (tmp_path / "engram-paper-ssot-20260920T131330Z.stripped.db").write_bytes(b"y")
    assert ssot.resolve_db(None, allow_unpinned=True).name == "engram-paper-ssot-20260920T131330Z.db"
    (tmp_path / "engram-paper-ssot-20260920T131330Z.db").unlink()
    assert ssot.resolve_db(None, allow_unpinned=True).name.endswith(".stripped.db")


def test_c10_a_real_tool_runs_on_the_shipped_file_by_default_resolution():
    """An outside reader has only the stripped file: no --db, no --allow-unpinned."""
    if any(p for p in DATA.glob("engram-paper-ssot-*.db") if not p.name.endswith(".stripped.db")):
        pytest.skip("a full snapshot is present next to the release; default resolution prefers it")
    p = subprocess.run([sys.executable, str(TOOLS / "modus_ponens_check.py")], cwd=str(REPO_ROOT),
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert "current deductive_modus_ponens derivations: 416" in p.stdout


# ─────────────────────────────────────────────────────────────────────────
# C11  EVERY PRINTED ORDER IS A TOTAL ORDER (round 2)
# ─────────────────────────────────────────────────────────────────────────
#
# `ORDER BY count DESC` (and `Counter.most_common()`, and `sorted(key=len)`) leave TIED rows
# in whatever order the query plan happens to produce, and the plan depends on which indexes
# exist and on whether the file was ANALYZEd.  A reproducibility artifact must not depend on
# planner statistics, so every ordering the instruments print carries a natural secondary key.
# This cell is the guard: the SAME rows, presented to the planner differently, must print the
# SAME output.  Index choice in the release is therefore free.

PLANNER_TEMPTING_INDEXES = (
    "CREATE INDEX x_nodes_current ON nodes(is_current)",
    "CREATE INDEX x_nodes_current_type ON nodes(is_current, type)",
    "CREATE INDEX x_nodes_type_cur_conf ON nodes(type, is_current, confidence)",
    "CREATE INDEX x_nodes_quote ON nodes(quote_type)",
    "CREATE INDEX x_edges_relation ON edges(relation)",
    "CREATE INDEX x_edges_srt ON edges(source_id, relation, target_id)",
)


def physical_variant(src, dst, *, keep_indexes, extra_indexes=(), analyze=False, reverse=False):
    """Copy `src` (a release) to `dst` with the same rows and a different physical shape: its
    own indexes kept or dropped, extra indexes added, ANALYZE run, rows inserted in reverse."""
    s = ro(src)
    d = sqlite3.connect(str(dst))
    for (ddl,) in s.execute("SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL"):
        d.execute(ddl)
    nodes = s.execute("SELECT * FROM nodes ORDER BY rowid").fetchall()
    edges = s.execute("SELECT * FROM edges ORDER BY id").fetchall()
    if reverse:
        nodes.reverse()
        edges.reverse()
    d.executemany(f"INSERT INTO nodes VALUES ({','.join('?' * len(nodes[0]))})", nodes)
    d.executemany(f"INSERT INTO edges VALUES ({','.join('?' * len(edges[0]))})", edges)
    d.executemany("INSERT INTO release_meta VALUES (?, ?)", s.execute("SELECT * FROM release_meta").fetchall())
    if keep_indexes:
        for (ddl,) in s.execute("SELECT sql FROM sqlite_master WHERE type='index' AND sql IS NOT NULL"):
            d.execute(ddl)
    for ddl in extra_indexes:
        d.execute(ddl)
    if analyze:
        d.execute("ANALYZE")
    d.commit()
    d.close()
    return dst


VARIANTS = {
    "as_shipped":             dict(keep_indexes=True),
    "as_shipped_analyzed":    dict(keep_indexes=True, analyze=True),
    "no_indexes":             dict(keep_indexes=False),
    "tempting_indexes":       dict(keep_indexes=False, extra_indexes=PLANNER_TEMPTING_INDEXES),
    "tempting_analyzed":      dict(keep_indexes=True, extra_indexes=PLANNER_TEMPTING_INDEXES, analyze=True),
    "reversed_rows_analyzed": dict(keep_indexes=True, extra_indexes=PLANNER_TEMPTING_INDEXES,
                                   analyze=True, reverse=True),
}


def compared_outputs(db, synthetic):
    """The C5 commands' normalised outputs.  The synthetic fixture cannot run make_figures
    (it has no EXEMPLAR node) and holds malformed metadata, so errors are compared too."""
    if synthetic:
        return run_commands(db, "dv_0030", pinned=False, tolerate_errors=True)
    return json.loads(json.dumps(run_all(db, CH6_TRACE_ID, pinned=False)))


def test_c11_printed_order_is_independent_of_analyze_indexes_and_row_order(tmp_path, stripped_db):
    synthetic = stripped_db != STRIPPED
    outputs = {name: compared_outputs(physical_variant(stripped_db, tmp_path / f"{name}.db", **kw), synthetic)
               for name, kw in VARIANTS.items()}
    ref = outputs["as_shipped"]
    for name, got in outputs.items():
        diffs = {lbl: delta(ref[lbl], got[lbl]) for lbl in ref}
        diffs = {k: v[:3] for k, v in diffs.items() if v}
        assert not diffs, f"{name}: output depends on the physical file shape: {diffs}"


def test_c11_a_plain_analyze_of_the_release_changes_nothing(tmp_path, stripped_db):
    """The literal form of the owner's ruling: ANALYZE a temp copy of the file as it ships."""
    synthetic = stripped_db != STRIPPED
    before = compared_outputs(stripped_db, synthetic)
    cp = tmp_path / "analyzed.db"
    shutil.copy(stripped_db, cp)
    c = sqlite3.connect(str(cp))
    c.execute("ANALYZE")
    c.commit()
    c.close()
    assert compared_outputs(cp, synthetic) == before


def test_c11_ties_exist_in_the_release_so_the_cells_are_not_vacuous():
    """The release has tied census counts and tied reasoning-type counts; without ties the
    cells above would pass for any implementation."""
    con = ro(STRIPPED)
    counts = [r[0] for r in con.execute("SELECT COUNT(*) FROM nodes WHERE is_current=1 GROUP BY type")]
    assert len(counts) != len(set(counts))
    rts = {}
    for (m,) in con.execute("SELECT metadata FROM nodes WHERE type='derivation' AND is_current=1"):
        rt = "<absent>"
        if m:
            try:
                rt = json.loads(m).get("reasoning_type", "<absent>")
            except Exception:
                rt = "<unparseable>"
        rts[rt] = rts.get(rt, 0) + 1
    assert len(rts) != len(set(rts.values()))


def _tiny_graph(path, edges_in_order, conf_ob2=0.9):
    """A 4-node graph for the two tie-breaks that no file-shape variant of the release reaches."""
    con = sqlite3.connect(str(path))
    con.execute("CREATE TABLE nodes (id TEXT PRIMARY KEY, type TEXT NOT NULL, created_at TEXT NOT NULL,"
                " confidence REAL, is_current INTEGER, status TEXT, quote_type TEXT, source_type TEXT,"
                " claim TEXT, source_url TEXT, metadata TEXT)")
    con.execute("CREATE TABLE edges (id INTEGER PRIMARY KEY, source_id TEXT NOT NULL, target_id TEXT NOT NULL,"
                " relation TEXT NOT NULL, created_at TEXT NOT NULL)")      # no UNIQUE: rows scan in rowid order
    con.execute("CREATE TABLE release_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    mp = '{"reasoning_type": "deductive_modus_ponens"}'
    # dv_0001 has two premises of EQUAL confidence 0.6: ob_0001 (an observation), dv_0002 (a derivation)
    rows = [("dv_0001", "derivation", 0.5, mp), ("ob_0001", "observation_factual", 0.6, "{}"),
            ("dv_0002", "derivation", 0.6, mp), ("ob_0002", "observation_factual", conf_ob2, "{}")]
    con.executemany("INSERT INTO nodes (id, type, created_at, confidence, is_current, metadata)"
                    " VALUES (?, ?, '2026-09-01', ?, 1, ?)", rows)
    con.executemany("INSERT INTO edges (source_id, target_id, relation, created_at)"
                    " VALUES (?, ?, 'derives_from', '2026-09-01')", edges_in_order)
    con.commit()
    con.close()
    return path


def test_c11_equal_confidence_premises_resolve_by_id_not_by_edge_order(tmp_path):
    """modus_ponens_check: the weakest premise of a tie is the lowest id (dv_0002 < ob_0001), so
    the count of 'weakest premise is itself a derivation' cannot depend on edge storage order."""
    fwd = [("dv_0001", "ob_0001"), ("dv_0001", "dv_0002"), ("dv_0002", "ob_0002")]
    outs = []
    for i, edges in enumerate((fwd, [fwd[1], fwd[0], fwd[2]])):
        db = _tiny_graph(tmp_path / f"t{i}.db", edges)
        p = subprocess.run([sys.executable, str(TOOLS / "modus_ponens_check.py"), "--db", str(db),
                            "--allow-unpinned"], cwd=str(REPO_ROOT), capture_output=True, text=True)
        assert p.returncode == 0, p.stderr
        outs.append(normalise("modus_ponens_check", p.stdout))
    assert outs[0] == outs[1]
    assert any(x.endswith("weakest premise is itself a derivation: 1") for x in outs[0]), outs[0]


def test_c11_trace_chain_tie_resolves_by_id_not_by_edge_order(tmp_path):
    """paper_stats --trace: two parents equal in depth and confidence -> the lowest id."""
    results = []
    for i, edges in enumerate(([("dv_0001", "ob_0001"), ("dv_0001", "ob_0002")],
                               [("dv_0001", "ob_0002"), ("dv_0001", "ob_0001")])):
        db = _tiny_graph(tmp_path / f"c{i}.db", edges, conf_ob2=0.6)
        p = subprocess.run([sys.executable, str(TOOLS / "paper_stats.py"), "--db", str(db),
                            "--allow-unpinned", "--trace", "dv_0001", "--json"],
                           cwd=str(REPO_ROOT), capture_output=True, text=True)
        assert p.returncode == 0, p.stderr
        results.append([r["id"] for r in json.loads(p.stdout)["traces"][0]["rows"]])
    assert results[0] == results[1] == ["dv_0001", "ob_0001"]


def _tied_means_db(path, reverse):
    """Two reasoning types (5 derivations each) and two quote types (2 observations each),
    every confidence 0.5: each pair has EQUAL means, so only the tie-break orders it."""
    con = sqlite3.connect(str(path))
    con.execute("CREATE TABLE nodes (id TEXT PRIMARY KEY, type TEXT NOT NULL, created_at TEXT NOT NULL,"
                " confidence REAL, is_current INTEGER, status TEXT, quote_type TEXT, source_type TEXT,"
                " claim TEXT, source_url TEXT, metadata TEXT)")
    con.execute("CREATE TABLE edges (id INTEGER PRIMARY KEY, source_id TEXT NOT NULL, target_id TEXT NOT NULL,"
                " relation TEXT NOT NULL, created_at TEXT NOT NULL)")
    con.execute("CREATE TABLE release_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    rows = []
    for rt, base in (("inductive_analogy", 0), ("authority_expert", 5)):
        for i in range(5):
            rows.append((f"dv_{base + i + 1:04d}", "derivation", None,
                         json.dumps({"reasoning_type": rt})))
    for qt, base in (("hard_data", 0), ("editorial", 2)):
        for i in range(2):
            rows.append((f"ob_{base + i + 1:04d}", "observation_factual", qt, "{}"))
    if reverse:
        rows.reverse()
    con.executemany("INSERT INTO nodes (id, type, created_at, confidence, is_current, quote_type, metadata)"
                    " VALUES (?, ?, '2026-09-01', 0.5, 1, ?, ?)",
                    [(i, t, q, m) for i, t, q, m in rows])
    con.commit()
    con.close()
    return path


def test_c11_tied_means_sort_by_label_whatever_the_row_order(tmp_path):
    figs, stats = [], []
    for i, rev in enumerate((False, True)):
        db = _tied_means_db(tmp_path / f"m{i}.db", rev)
        figs.append(run_make_figures(db, only={"fig_reasoning_type", "fig_quote_type"}))
        p = subprocess.run([sys.executable, str(TOOLS / "paper_stats.py"), "--db", str(db), "--allow-unpinned"],
                           cwd=str(REPO_ROOT), capture_output=True, text=True)
        assert p.returncode == 0, p.stderr
        stats.append(normalise("paper_stats", p.stdout))
    assert figs[0] == figs[1] and stats[0] == stats[1]
    order = lambda lines, a, b: next(i for i, x in enumerate(lines) if a in x) < next(i for i, x in enumerate(lines) if b in x)
    assert order(figs[0]["fig_reasoning_type"], "authority_expert", "inductive_analogy")
    assert order(figs[0]["fig_quote_type"], "editorial", "hard_data")
    assert order(stats[0], "editorial", "hard_data")                       # paper_stats quote_type table
    assert order(stats[0], "authority_expert", "inductive_analogy")        # paper_stats reasoning_type table


def test_c11_evidence_provenance_ranking_breaks_ties_by_label():
    ep = _load_tool("evidence_provenance")
    from collections import Counter
    a, b = Counter(), Counter()
    for k in ("file", "external", "transcript"):
        a[k] += 4
    for k in ("transcript", "file", "external"):
        b[k] += 4
    assert ep.ranked(a) == ep.ranked(b) == [("external", 4), ("file", 4), ("transcript", 4)]
    assert ep.ranked(Counter({"x": 1, "y": 9, "z": 1})) == [("y", 9), ("x", 1), ("z", 1)]


# ─────────────────────────────────────────────────────────────────────────

def _main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--regen-expected", action="store_true")
    ap.add_argument("--full", default=str(FULL))
    a = ap.parse_args(argv)
    if not a.regen_expected:
        ap.error("nothing to do; run the tests with pytest")
    gold = regenerate_expected(Path(a.full))
    EXPECTED.write_text(json.dumps(gold, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {EXPECTED} ({EXPECTED.stat().st_size:,} bytes)")


if __name__ == "__main__":
    _main()
