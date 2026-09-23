"""Contract tests for `tools/paper_stats.py`'s `--trace` mode, written BEFORE
the implementation per `spec-trace.md` — expected to fail (argparse
`unrecognized arguments`, exit 2) until `--trace` / `--trace-deepest` /
`--json` exist on the CLI.

Ports the reference script's chain-walk logic
(`/home/agent-borges/borges-desk/paper-chain-trace-2026-09-23.py`); does not
copy it verbatim (see docstring notes on the two deliberate departures: cycle
termination in `trace()`, and the `--trace-deepest` tie-break direction).

DB fixture / CLI-subprocess pattern matches
`tests/test_connectivity_trim_control.py` (`_make_db`, subprocess + `--db
--allow-unpinned`, JSON key-set assertions).
"""

from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "paper_stats.py"


# ── DB fixture builder ───────────────────────────────────────────────────
# Superset schema (matches every column any section of paper_stats.py reads)
# so the same builder serves both the byte-identical regression test and the
# trace-only tests.

def _make_db(tmp_path, nodes, edges, name="synthetic.db"):
    """nodes: list of (id, type, claim, metadata_json_or_None, confidence,
    quote_type, status, is_current, created_at).
    edges: list of (source_id, target_id, relation, created_at)."""
    db_path = tmp_path / name
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "CREATE TABLE nodes (id TEXT, type TEXT, claim TEXT, metadata TEXT, "
        "confidence REAL, quote_type TEXT, status TEXT, is_current INTEGER, "
        "created_at TEXT)"
    )
    conn.execute(
        "CREATE TABLE edges (source_id TEXT, target_id TEXT, relation TEXT, "
        "created_at TEXT)"
    )
    conn.executemany("INSERT INTO nodes VALUES (?,?,?,?,?,?,?,?,?)", nodes)
    conn.executemany("INSERT INTO edges VALUES (?,?,?,?)", edges)
    conn.commit()
    conn.close()
    return db_path


def _node(id_, type_="observation", claim=None, metadata=None, confidence=None,
          quote_type=None, status=None, is_current=1, created_at="2026-01-01T00:00:00"):
    return (id_, type_, claim if claim is not None else f"claim for {id_}",
            metadata, confidence, quote_type, status, is_current, created_at)


def _edge(source_id, target_id, relation="derives_from", created_at="2026-01-01T00:00:00"):
    return (source_id, target_id, relation, created_at)


def _run(db, *args):
    return subprocess.run(
        [sys.executable, str(TOOL), "--db", str(db), "--allow-unpinned", *args],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )


# ── Test 0: without any trace flag, output is byte-identical to today ────
# (the "today" text below was captured by running the UNMODIFIED
# tools/paper_stats.py, at base commit 049d6d0a, against this exact
# fixture -- transcribed here verbatim minus the one path-dependent line,
# the "# source:" header, which is asserted separately by shape.)

def _byte_identical_nodes():
    return [
        _node("ob_01", "observation", "claim one", None, 0.85, "hard_data", None, 1, "2026-01-01T00:00:00"),
        _node("ob_02", "observation", "claim two", None, 0.40, "personal_communication", None, 1, "2026-01-02T00:00:00"),
        _node("dv_01", "derivation", "derived claim one", '{"reasoning_type":"deductive_modus_ponens"}', 0.75, None, None, 1, "2026-01-03T00:00:00"),
        _node("dv_02", "derivation", "derived claim two", '{"reasoning_type":"abductive_best_explanation"}', 0.55, None, None, 1, "2026-01-04T00:00:00"),
        _node("qu_01", "question", "open question", None, None, None, "open", 1, "2026-01-05T00:00:00"),
        _node("qu_02", "question", "resolved question", None, None, None, "resolved", 1, "2026-01-06T00:00:00"),
        _node("ax_01", "axiom", "axiom claim", None, 1.0, None, None, 1, "2026-01-07T00:00:00"),
        _node("ob_03", "observation", "superseded claim", None, 0.5, "hard_data", None, 0, "2026-01-08T00:00:00"),
    ]


def _byte_identical_edges():
    return [
        _edge("dv_01", "ob_01"),
        _edge("dv_02", "dv_01"),
        _edge("dv_02", "ob_02"),
    ]


_EXPECTED_BODY = """# every figure below is computed from that file and nothing else

## Graph at a glance
  current nodes            7 / 8 total (superseded+retracted = 1)
  edges                    3
  first node               2026-01-01T00:00:00
  last node                2026-01-08T00:00:00

## Node census (current)
  question                      2 / 7
  observation                   2 / 7
  derivation                    2 / 7
  axiom                         1 / 7

## §6.1 Confidence by node type — current, confidence NOT NULL
  type                          n    mean  median     p25     p75
  axiom                         1    1.00    1.00    1.00    1.00
  derivation                    2    0.65    0.65    0.60    0.70
  observation                   2    0.62    0.62    0.51    0.74

## §6.1 Confidence by reasoning_type — current derivations
  reasoning_type                          n    / dvs    mean
  deductive_modus_ponens                  1        2    0.75
  abductive_best_explanation              1        2    0.55

## §6.1 Confidence by quote_type — current observations
  quote_type                              n    / obs    mean
  hard_data                               1        2    0.85
  personal_communication                  1        2    0.40

## §6.2 Non-modularity — largest connected component over the CURRENT node set
  edges used               3 / 3 (dropped 0: an endpoint is not a current node)
  components               4
  largest component        4 / 7 nodes = 57.1%
  isolated (size 1)        3 / 7
  next four components     1, 1, 1

## §6.4 Derivation chain depth — longest derives_from path to a root, current nodes
  derives_from edges used  3 (both endpoints current)
  max depth                2
   depth  node         conf   claim
       2  dv_02        0.55   derived claim two
       1  dv_01        0.75   derived claim one
       0  qu_02         --    resolved question
       0  qu_01         --    open question
       0  ob_02        0.40   claim two

## §6.5 Metacognitive surface — the agent's own weakest live beliefs
  open questions           1 / 2 current questions
  lowest-confidence current derivations       
    dv_02  0.55  derived claim two
    dv_01  0.75  derived claim one

"""


def test_no_trace_flag_output_byte_identical_to_today(tmp_path):
    db = _make_db(tmp_path, _byte_identical_nodes(), _byte_identical_edges())
    proc = _run(db)
    assert proc.returncode == 0, proc.stderr
    lines = proc.stdout.split("\n", 1)
    assert lines[0].startswith("# source: ")
    assert lines[1] == _EXPECTED_BODY
    assert "--trace" not in proc.stdout


# ── Chain fixtures shared by several tests ────────────────────────────────
# A straightforward 3-step chain: dv_c (root's grandchild) -> dv_b -> dv_a
# (root). Confidences chosen per spec's multiplicative-check test 6.

def _chain3_nodes():
    return [
        _node("dv_a", "derivation", "root of the chain", '{"reasoning_type":"deductive_modus_ponens"}', 0.45),
        _node("dv_b", "derivation", "middle of the chain", '{"reasoning_type":"deductive_modus_ponens"}', 0.70),
        _node("dv_c", "derivation", "tip of the chain", '{"reasoning_type":"deductive_modus_ponens"}', 0.56),
    ]


def _chain3_edges():
    return [
        _edge("dv_c", "dv_b"),
        _edge("dv_b", "dv_a"),
    ]


# ── Error contract ─────────────────────────────────────────────────────────

def test_trace_unknown_id_errors(tmp_path):
    db = _make_db(tmp_path, _chain3_nodes(), _chain3_edges())
    proc = _run(db, "--trace", "dv_nonexistent")
    assert proc.returncode == 2
    assert "no current node dv_nonexistent" in proc.stderr
    assert proc.stdout == ""


def test_trace_non_current_id_errors_same_as_unknown(tmp_path):
    nodes = _chain3_nodes() + [
        _node("dv_stale", "derivation", "superseded", None, 0.5, is_current=0),
    ]
    db = _make_db(tmp_path, nodes, _chain3_edges())
    proc = _run(db, "--trace", "dv_stale")
    assert proc.returncode == 2
    assert "no current node dv_stale" in proc.stderr
    assert proc.stdout == ""


def test_trace_cyclic_fixture_terminates(tmp_path):
    # dv_x <-> dv_y mutual derives_from: a genuine 2-cycle with no exit.
    nodes = [
        _node("dv_x", "derivation", "cyclic node x", None, 0.5),
        _node("dv_y", "derivation", "cyclic node y", None, 0.5),
    ]
    edges = [_edge("dv_x", "dv_y"), _edge("dv_y", "dv_x")]
    db = _make_db(tmp_path, nodes, edges)
    proc = subprocess.run(
        [sys.executable, str(TOOL), "--db", str(db), "--allow-unpinned",
         "--trace", "dv_x", "--json"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=10,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert len(payload["traces"]) == 1
    rows = payload["traces"][0]["rows"]
    # terminates: finite rows, and the chosen next parent (already in the
    # trace) stops the walk rather than looping.
    assert len(rows) == 2
    ids = [r["id"] for r in rows]
    assert ids == ["dv_x", "dv_y"]
    for r in rows:
        assert isinstance(r["depth"], int)


def test_trace_tie_break_lowest_confidence(tmp_path):
    # X's two depth-2 parents P1 (conf 0.9) and P2 (conf 0.3): trace goes
    # through P2 (lower confidence), per the reference script's tie-break key
    # max(depth(p), -confidence(p)).
    nodes = [
        _node("X", "derivation", "start", None, 0.5),
        _node("P1", "derivation", "depth-2 high-conf parent", None, 0.9),
        _node("P2", "derivation", "depth-2 low-conf parent", None, 0.3),
        _node("gp1", "derivation", "grandparent of P1", None, 0.6),
        _node("gp2", "derivation", "grandparent of P2", None, 0.6),
    ]
    edges = [
        _edge("X", "P1"), _edge("X", "P2"),
        _edge("P1", "gp1"), _edge("P2", "gp2"),
    ]
    db = _make_db(tmp_path, nodes, edges)
    proc = _run(db, "--trace", "X", "--json")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    ids = [r["id"] for r in payload["traces"][0]["rows"]]
    assert ids == ["X", "P2", "gp2"]


def test_trace_tie_break_prefers_strictly_deeper_parent(tmp_path):
    # Same as above, plus P3 (depth 3, conf 0.95): trace now goes through P3
    # (strictly deeper beats lower confidence).
    nodes = [
        _node("X", "derivation", "start", None, 0.5),
        _node("P1", "derivation", "depth-2 high-conf parent", None, 0.9),
        _node("P2", "derivation", "depth-2 low-conf parent", None, 0.3),
        _node("P3", "derivation", "depth-3 parent", None, 0.95),
        _node("gp1", "derivation", "grandparent of P1", None, 0.6),
        _node("gp2", "derivation", "grandparent of P2", None, 0.6),
        _node("gp3", "derivation", "grandparent of P3", None, 0.6),
        _node("ggp3", "derivation", "great-grandparent of P3", None, 0.6),
    ]
    edges = [
        _edge("X", "P1"), _edge("X", "P2"), _edge("X", "P3"),
        _edge("P1", "gp1"), _edge("P2", "gp2"),
        _edge("P3", "gp3"), _edge("gp3", "ggp3"),
    ]
    db = _make_db(tmp_path, nodes, edges)
    proc = _run(db, "--trace", "X", "--json")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    ids = [r["id"] for r in payload["traces"][0]["rows"]]
    assert ids == ["X", "P3", "gp3", "ggp3"]


def test_trace_root_node_single_row(tmp_path):
    db = _make_db(tmp_path, _chain3_nodes(), _chain3_edges())
    proc = _run(db, "--trace", "dv_a", "--json")
    assert proc.returncode == 0, proc.stderr
    rows = json.loads(proc.stdout)["traces"][0]["rows"]
    assert len(rows) == 1
    row = rows[0]
    assert row["id"] == "dv_a"
    assert row["depth"] == 0
    assert row["n_premises"] == 0
    assert row["min_premise_conf"] is None


def test_trace_multiplicative_chain_confidences_to_3dp(tmp_path):
    db = _make_db(tmp_path, _chain3_nodes(), _chain3_edges())
    proc = _run(db, "--trace", "dv_c", "--json")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    block = payload["traces"][0]
    assert block["start"] == "dv_c"
    assert block["depth"] == 2
    rows = block["rows"]
    by_id = {r["id"]: r for r in rows}
    assert by_id["dv_c"]["confidence"] == 0.56
    assert by_id["dv_b"]["confidence"] == 0.7
    assert by_id["dv_a"]["confidence"] == 0.45
    assert by_id["dv_c"]["min_premise_conf"] == 0.7
    assert by_id["dv_b"]["min_premise_conf"] == 0.45
    assert by_id["dv_a"]["min_premise_conf"] is None
    assert by_id["dv_c"]["n_premises"] == 1
    assert by_id["dv_b"]["n_premises"] == 1
    assert by_id["dv_a"]["n_premises"] == 0
    for r in rows:
        assert r["reasoning_type"] == "deductive_modus_ponens"
        assert r["type"] == "derivation"


def test_trace_given_twice_two_blocks_in_order(tmp_path):
    db = _make_db(tmp_path, _chain3_nodes(), _chain3_edges())
    proc = _run(db, "--trace", "dv_c", "--trace", "dv_a", "--json")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert [t["start"] for t in payload["traces"]] == ["dv_c", "dv_a"]

    # order reversed at the CLI -> order reversed in output
    proc2 = _run(db, "--trace", "dv_a", "--trace", "dv_c", "--json")
    payload2 = json.loads(proc2.stdout)
    assert [t["start"] for t in payload2["traces"]] == ["dv_a", "dv_c"]


# ── --trace-deepest: tie-break direction (our departure from the reference
# script, documented in the implementation's docstring: ties -> smallest id,
# not the reference script's largest id).

def test_trace_deepest_tie_break_smallest_id(tmp_path):
    # Two roots-of-equal-max-depth chains, tip ids "aaa_tip" and "zzz_tip":
    # both depth 1. Smallest id ("aaa_tip") wins.
    nodes = [
        _node("root1", "derivation", "root one", None, 0.5),
        _node("root2", "derivation", "root two", None, 0.5),
        _node("aaa_tip", "derivation", "alphabetically-first tip", None, 0.5),
        _node("zzz_tip", "derivation", "alphabetically-last tip", None, 0.5),
    ]
    edges = [_edge("aaa_tip", "root1"), _edge("zzz_tip", "root2")]
    db = _make_db(tmp_path, nodes, edges)
    proc = _run(db, "--trace-deepest", "--json")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["traces"][0]["start"] == "aaa_tip"


# ── can-it-fail companion mutations live in the handoff, not as pytest
# cases: run against the implementation post-hoc (sed a plausible-wrong
# variant into tools/paper_stats.py, confirm these tests 3/4/6 go red while
# the byte-identical + existing paper_stats output stays green, then revert).
