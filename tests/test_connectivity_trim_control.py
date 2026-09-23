"""Contract tests for `tools.connectivity_trend`'s `--trim-control` mode,
written BEFORE the implementation per `spec-trim-control.md` — they are
expected to fail with an ImportError/AttributeError until `trim_recency`,
`trim_oldest_matched` and `trim_control` exist.

Reuses Borges's re-derivation logic (`/home/agent-borges/borges-desk/
paper-trim-control-2026-09-23.py`) as the reference for what each arm
computes; does not copy its sweep loop.

Import style matches the existing `tests/test_render_apparatus.py`
convention: absolute `tools.connectivity_trend` import, relying on
`tests/__init__.py` making `tests` a package (pytest then inserts the repo
root — the parent of `tests/` — onto `sys.path`) and `tools/` being an
implicit namespace package (no `__init__.py`, same as `tools/render_paper.py`).
"""

from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from tools.connectivity_trend import trim_control, trim_oldest_matched, trim_recency

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "connectivity_trend.py"


# ── DB fixture builder ───────────────────────────────────────────────────

def _make_db(tmp_path, nodes, edges, name="synthetic.db"):
    """nodes: list of (id, created_at, is_current); edges: list of
    (source_id, target_id, created_at). created_at may be None for the
    null-exclusion test."""
    db_path = tmp_path / name
    conn = sqlite3.connect(str(db_path))
    conn.execute("CREATE TABLE nodes (id TEXT, created_at TEXT, is_current INTEGER)")
    conn.execute("CREATE TABLE edges (source_id TEXT, target_id TEXT, created_at TEXT)")
    conn.executemany("INSERT INTO nodes VALUES (?, ?, ?)", nodes)
    conn.executemany("INSERT INTO edges VALUES (?, ?, ?)", edges)
    conn.commit()
    conn.close()
    return db_path


# ── Test 1: window-edges share vs all-edges share DIFFER at a chosen cut ──
# The discriminating case named in the coordinator's amendment: one LATE
# edge between two EARLY (kept) nodes. Six kept nodes (n1..n6, dates
# 2026-01-01..06), two trimmed (n7, n8, dates 2026-01-15/16). cut =
# 2026-01-10.
#
# Window edges (created_at <= cut): n1-n2 (01-01), n3-n4 (01-02).
#   Components over {n1..n6}: {n1,n2}, {n3,n4}, {n5}, {n6} -> largest = 2.
# All edges also include n2-n3 (01-20, AFTER cut) which joins the two
# pairs into one component of size 4 -> largest = 4.
# So window share (2/6) and all-edges share (4/6) differ, as required.

def _t1_nodes():
    return [
        ("n1", "2026-01-01", 1),
        ("n2", "2026-01-02", 1),
        ("n3", "2026-01-03", 1),
        ("n4", "2026-01-04", 1),
        ("n5", "2026-01-05", 1),
        ("n6", "2026-01-06", 1),
        ("n7", "2026-01-15", 1),
        ("n8", "2026-01-16", 1),
    ]


def _t1_edges():
    return [
        ("n1", "n2", "2026-01-01"),
        ("n3", "n4", "2026-01-02"),
        ("n2", "n3", "2026-01-20"),  # late edge between two early (kept) nodes
    ]


def test_trim_recency_window_vs_all_differ():
    nodes = [(i, ca) for i, ca, _ in _t1_nodes()]
    edges = _t1_edges()
    kept, trimmed, lcc_window, lcc_all = trim_recency(nodes, edges, "2026-01-10")
    assert kept == 6
    assert trimmed == 2
    assert lcc_window == 2
    assert lcc_all == 4


# ── Test 2: trim_oldest_matched drops exactly k oldest (ties by id order) ─

def test_trim_oldest_matched_drops_k_oldest():
    # nA and nB share a created_at date; tie-break rule is ascending id, so
    # a nodes_sorted list built as sorted(nodes, key=lambda x: (date, id))
    # places nA before nB. Dropping k=1 oldest removes nA, keeps nB, nC.
    nodes_sorted = [
        ("nA", "2026-01-01"),
        ("nB", "2026-01-01"),
        ("nC", "2026-01-02"),
    ]
    edges = [("nB", "nC")]
    kept_count, lcc_all = trim_oldest_matched(nodes_sorted, edges, 1)
    assert kept_count == 2
    # remaining nodes {nB, nC} connected by the one edge -> largest component 2.
    assert lcc_all == 2


def test_trim_oldest_matched_ties_use_sorted_input_order():
    # Same tie, different sort input order (nB before nA in the list this
    # time) confirms trim_oldest_matched trusts nodes_sorted's own order —
    # it does not re-sort or re-break ties itself; the caller (trim_control)
    # is responsible for building nodes_sorted with the (created_at, id)
    # tie-break rule before calling.
    nodes_sorted = [
        ("nB", "2026-01-01"),
        ("nA", "2026-01-01"),
        ("nC", "2026-01-02"),
    ]
    edges = [("nA", "nC")]
    kept_count, lcc_all = trim_oldest_matched(nodes_sorted, edges, 1)
    assert kept_count == 2
    assert lcc_all == 2  # {nA, nC} kept this time, joined by the edge


# ── Test 3: trim_control's counts + same-k equality across arms ──────────

def _t3_nodes():
    # hi = 2026-03-01. 20 nodes spread one per day from 2026-02-10 through
    # 2026-03-01 (20 days), so at 1 week back (7 days) exactly 7 nodes are
    # newer than the cut, and at 2 weeks back exactly 14 are newer.
    nodes = []
    import datetime as _dt
    start = _dt.date(2026, 2, 10)
    for i in range(20):
        d = start + _dt.timedelta(days=i)
        nodes.append((f"m{i:02d}", d.strftime("%Y-%m-%d"), 1))
    return nodes


def _t3_edges(nodes):
    # A simple path so every lcc computation is well-defined and non-trivial.
    edges = []
    ids = [n[0] for n in nodes]
    for a, b in zip(ids, ids[1:]):
        edges.append((a, b, nodes[0][1]))  # all edges dated at the earliest node
    return edges


def test_trim_control_counts_and_matched_k(tmp_path):
    nodes = _t3_nodes()
    edges = _t3_edges(nodes)
    db = _make_db(tmp_path, nodes, edges)

    result = trim_control(db, recency_weeks=(1, 2), control_weeks=(1, 2))

    assert result["hi"] == "2026-03-01"

    # recency arm: 1 week back -> cut 2026-02-22, nodes newer than cut are
    # 2026-02-23..03-01 = 7 nodes trimmed, 13 kept.
    assert result["recency"][1]["cut"] == "2026-02-22"
    assert result["recency"][1]["trimmed"] == 7
    assert result["recency"][1]["kept"] == 13

    # 2 weeks back -> cut 2026-02-15, newer-than-cut = 02-16..03-01 = 14 nodes.
    assert result["recency"][2]["cut"] == "2026-02-15"
    assert result["recency"][2]["trimmed"] == 14
    assert result["recency"][2]["kept"] == 6

    # control arm: same k at the same week-cut, both arms trimmed/dropped
    # the identical count of nodes.
    for w in (1, 2):
        assert result["control"][w]["k"] == result["control"][w]["recency_trimmed"]
        assert result["control"][w]["recency_kept"] + result["control"][w]["k"] == 20
        assert result["control"][w]["control_kept"] + result["control"][w]["k"] == 20

    assert result["control"][1]["k"] == 7
    assert result["control"][2]["k"] == 14


# ── Test 8 (fold round, real-snapshot colleague pass): trim_control() must
# sort nodes_sorted by the FULL created_at timestamp, not by day-then-id.
# All real created_at values are full ISO timestamps; day-granularity
# truncation before the id tie-break means two nodes sharing a calendar day
# get ordered by id prefix instead of by actual time-of-day, which silently
# picks the wrong node to drop whenever a boundary day holds more than one
# node. This is the exact case: zz_id is EARLIER in real time (08:00) but
# sorts AFTER aa_id alphabetically; aa_id is LATER in real time (20:00) but
# sorts FIRST alphabetically — so a (date, id) key drops aa_id (the actually
# newest of the pair) instead of zz_id (the actually oldest).
#
# Exercises the real trim_control() code path (not a hand-built
# nodes_sorted) via a sentinel node newer than both, and an edge that only
# connects the sentinel to aa_id — so which of {aa_id, zz_id} survived the
# drop is observable through the resulting largest-component size, the same
# discriminator technique Test 1 uses (a late/early edge as an identity
# probe) rather than trim_control()'s dict exposing node identities
# directly. k=1 is engineered by the fractional-week cut below, so exactly
# one node (the oldest of the three by full timestamp) is dropped, leaving
# two kept — {aa_id, sentinel} if the sort is correct, {zz_id, sentinel} if
# it is the (date, id)-only bug.

def test_trim_control_sorts_by_full_timestamp_not_day_then_id(tmp_path):
    nodes = [
        # same calendar day, later-timed node's id sorts FIRST alphabetically
        ("zz_id", "2026-04-15T08:00:00", 1),  # earlier in real time
        ("aa_id", "2026-04-15T20:00:00", 1),  # later in real time
        ("sentinel", "2026-04-20T00:00:00", 1),  # newest of all three
    ]
    edges = [
        ("aa_id", "sentinel", "2026-04-20T00:00:00"),  # identity probe
    ]
    db = _make_db(tmp_path, nodes, edges)

    # cut = hi_date (2026-04-20) - 5 days, expressed as a fractional-week
    # control_weeks entry, so cut == "2026-04-15": exactly the calendar day
    # zz_id/aa_id share, so date > cut is False for both of them (k excludes
    # them) and True only for sentinel (k=1).
    result = trim_control(db, recency_weeks=(5 / 7,), control_weeks=(5 / 7,))

    w = 5 / 7
    assert result["hi"] == "2026-04-20"
    assert result["control"][w]["cut"] == "2026-04-15"
    assert result["control"][w]["k"] == 1
    assert result["control"][w]["control_kept"] == 2

    # correct (full-timestamp) sort drops zz_id (the true oldest), keeping
    # {aa_id, sentinel} -> the probe edge connects them -> largest component 2.
    # the (date, id)-only bug instead drops aa_id, keeping {zz_id, sentinel}
    # -> no edge between them -> largest component 1.
    assert result["control"][w]["control_lcc_all"] == 2


# ── Test 4: NULL created_at excluded on both nodes and edges ─────────────

def test_null_created_at_excluded(tmp_path):
    nodes = [
        ("n1", "2026-01-01", 1),
        ("n2", "2026-01-02", 1),
        ("n3", "2026-01-03", 1),
        ("nX", None, 1),  # excluded entirely
    ]
    edges = [
        ("n1", "n2", "2026-01-01"),
        ("n2", "n3", None),  # excluded entirely
    ]
    db = _make_db(tmp_path, nodes, edges)

    result = trim_control(db, recency_weeks=(0,), control_weeks=(0,))
    # hi is computed only over non-null created_at -> 2026-01-03, and total
    # node population for kept+trimmed is 3 (nX never counted).
    assert result["hi"] == "2026-01-03"
    assert result["recency"][0]["kept"] + result["recency"][0]["trimmed"] == 3
    # the n2-n3 edge (NULL created_at) must not connect anything: with only
    # the n1-n2 edge counted, the largest component at full kept (cut=hi)
    # is 2 (n1,n2), not 3.
    assert result["recency"][0]["lcc_all"] == 2
    assert result["recency"][0]["lcc_window"] == 2


# ── Test 5: CLI ───────────────────────────────────────────────────────────

def test_cli_trim_control_json(tmp_path):
    nodes = _t3_nodes()
    edges = _t3_edges(nodes)
    db = _make_db(tmp_path, nodes, edges)

    proc = subprocess.run(
        [sys.executable, str(TOOL), "--trim-control", "--json",
         "--db", str(db), "--allow-unpinned"],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert "hi" in payload
    assert "recency" in payload and "control" in payload
    for w_dict in (payload["recency"], payload["control"]):
        assert len(w_dict) > 0

    # Tightened per the colleague's request: assert the DOCUMENTED inner-dict
    # key names (trim_control()'s own docstring) for one recency entry and
    # one control entry, so a key rename reddens this test rather than
    # passing silently (the prior version only checked outer-dict presence
    # and non-emptiness). CLI runs trim_control(db) with its default
    # recency_weeks=(6, 8, 12) / control_weeks=(2, 4, 8); JSON serialises
    # the int week keys as strings.
    one_recency = next(iter(payload["recency"].values()))
    assert set(one_recency.keys()) == {
        "cut", "kept", "trimmed", "lcc_window", "lcc_all",
        "share_window_pct", "share_all_pct",
    }
    one_control = next(iter(payload["control"].values()))
    assert set(one_control.keys()) == {
        "cut", "k", "recency_kept", "recency_trimmed",
        "recency_lcc_window", "recency_lcc_all",
        "recency_share_window_pct", "recency_share_all_pct",
        "control_kept", "control_lcc_all", "control_share_pct",
    }


def test_cli_default_invocation_unchanged(tmp_path):
    nodes = _t3_nodes()
    edges = _t3_edges(nodes)
    db = _make_db(tmp_path, nodes, edges)

    proc = subprocess.run(
        [sys.executable, str(TOOL), "--db", str(db), "--allow-unpinned",
         "--step-days", "7"],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "source:" in proc.stdout
    assert "--trim-control" not in proc.stdout  # sanity: not silently routed
    # the default table header is present (trend()'s own column header)
    assert "date" in proc.stdout and "largest" in proc.stdout
