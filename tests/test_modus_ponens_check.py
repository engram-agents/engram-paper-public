"""Contract tests for the per-node arm of `tools/modus_ponens_check.py`.

Written BEFORE the implementation (contract-first, Lei's 2026-09-19 ruling). The
contract is the one stated in the tool's module docstring:

  * CF(d) = targets of `derives_from` UNION `acknowledged_derives_from` edges from d,
    regardless of the target's is_current, minus d itself, minus NULL-confidence targets.
  * empty CF -> reported in `excluded` by id; NULL measured -> `null_measured`.
  * expected = round(0.98 * min(CF), 3); exact iff round(measured, 3) == expected.
  * deviating nodes carry id, measured, expected, weakest premise id/type/currency.
  * pinned = has an acknowledged_derives_from edge AND min(CF) attained ONLY at
    premises with is_current = 0.
  * exact + deviating + excluded + null_measured == N, else a crash with a message.

Cells (numbered as in the spec):
  1 superseded weakest premise scores exact (a current-only rule gets a different expected)
  2 ack edge to a STRONGER replacement, weaker old premise kept: exact AND pinned
  3 ack edge to a WEAKER replacement: exact, NOT pinned
  4 deliberately wrong confidence: deviating, with the correct weakest premise
  5 only premise has NULL confidence: excluded, named (5b: NULL measured is its own list)
  6 self-loop edge ignored
  7 denominator identity holds; a result breaking it raises
"""
from __future__ import annotations

import importlib.util
import sqlite3
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools" / "modus_ponens_check.py"


def _load():
    spec = importlib.util.spec_from_file_location("modus_ponens_check", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MP = '{"reasoning_type":"deductive_modus_ponens"}'


def _db(tmp_path, nodes, edges):
    """nodes: (id, type, confidence, is_current, metadata); edges: (src, tgt, relation)."""
    c = sqlite3.connect(str(tmp_path / "s.db"))
    c.execute("CREATE TABLE nodes (id TEXT PRIMARY KEY, type TEXT, confidence REAL, "
              "is_current INTEGER, metadata TEXT)")
    c.execute("CREATE TABLE edges (source_id TEXT, target_id TEXT, relation TEXT)")
    c.executemany("INSERT INTO nodes VALUES (?,?,?,?,?)", nodes)
    c.executemany("INSERT INTO edges VALUES (?,?,?)", edges)
    c.commit()
    return c


def _score(tmp_path, nodes, edges):
    return _load().score_modus_ponens(_db(tmp_path, nodes, edges))


def test_cell1_superseded_weakest_premise_scores_exact(tmp_path):
    # weakest premise ob_old (0.5) is superseded; a current-only rule would expect 0.784
    r = _score(tmp_path,
               [("dv_1", "derivation", 0.49, 1, MP),
                ("ob_old", "observation", 0.5, 0, None),
                ("ob_cur", "observation", 0.8, 1, None)],
               [("dv_1", "ob_old", "derives_from"), ("dv_1", "ob_cur", "derives_from")])
    assert r.n == 1 and r.exact == ["dv_1"] and r.deviating == []
    assert r.pinned == []  # no ack edge -> never pinned


def test_cell2_ack_to_stronger_replacement_is_exact_and_pinned(tmp_path):
    r = _score(tmp_path,
               [("dv_1", "derivation", 0.49, 1, MP),
                ("ob_old", "observation", 0.5, 0, None),
                ("ob_new", "observation", 0.8, 1, None)],
               [("dv_1", "ob_old", "derives_from"),
                ("dv_1", "ob_new", "acknowledged_derives_from")])
    assert r.exact == ["dv_1"] and r.deviating == []
    assert r.pinned == ["dv_1"]


def test_cell3_ack_to_weaker_replacement_is_exact_not_pinned(tmp_path):
    # old 0.8 superseded, replacement 0.5 current binds the min; measured follows the union
    r = _score(tmp_path,
               [("dv_1", "derivation", 0.49, 1, MP),
                ("ob_old", "observation", 0.8, 0, None),
                ("ob_new", "observation", 0.5, 1, None)],
               [("dv_1", "ob_old", "derives_from"),
                ("dv_1", "ob_new", "acknowledged_derives_from")])
    assert r.exact == ["dv_1"] and r.deviating == []
    assert r.pinned == []


def test_cell4_wrong_confidence_is_deviating_with_weakest_premise(tmp_path):
    r = _score(tmp_path,
               [("dv_1", "derivation", 0.70, 1, MP),
                ("dv_p", "derivation", 0.6, 0, MP),
                ("ob_b", "observation", 0.9, 1, None)],
               [("dv_1", "dv_p", "derives_from"), ("dv_1", "ob_b", "derives_from")])
    assert [x for x in r.exact if x == "dv_1"] == []
    assert len(r.deviating) == 1
    d = r.deviating[0]
    assert d["id"] == "dv_1"
    assert d["measured"] == 0.70
    assert d["expected"] == round(0.98 * 0.6, 3)
    assert d["weakest_id"] == "dv_p"
    assert d["weakest_type"] == "derivation"
    assert d["weakest_is_current"] is False


def test_cell5_only_premise_null_confidence_is_excluded_and_named(tmp_path):
    r = _score(tmp_path,
               [("dv_1", "derivation", 0.5, 1, MP),
                ("dv_2", "derivation", 0.5, 1, MP),  # no edges at all
                ("ob_null", "observation", None, 1, None)],
               [("dv_1", "ob_null", "derives_from")])
    assert r.n == 2 and sorted(r.excluded) == ["dv_1", "dv_2"]
    assert r.exact == [] and r.deviating == []


def test_cell5b_null_measured_is_its_own_list(tmp_path):
    r = _score(tmp_path,
               [("dv_1", "derivation", None, 1, MP), ("ob_a", "observation", 0.5, 1, None)],
               [("dv_1", "ob_a", "derives_from")])
    assert r.null_measured == ["dv_1"] and r.exact == [] and r.deviating == []


def test_cell6_self_loop_is_ignored(tmp_path):
    # the self-loop target (dv_1, 0.49) would drag the expected down to 0.48 if counted
    r = _score(tmp_path,
               [("dv_1", "derivation", 0.49, 1, MP),
                ("dv_2", "derivation", 0.9, 1, MP),
                ("ob_a", "observation", 0.5, 1, None)],
               [("dv_1", "dv_1", "derives_from"), ("dv_1", "ob_a", "derives_from"),
                ("dv_2", "dv_2", "acknowledged_derives_from")])
    assert r.exact == ["dv_1"]
    assert r.excluded == ["dv_2"]  # only a self-loop -> empty CF


def test_cell7_denominator_identity_holds_and_breaks_loudly(tmp_path):
    mod = _load()
    r = _score(tmp_path,
               [("dv_ok", "derivation", 0.49, 1, MP),
                ("dv_bad", "derivation", 0.30, 1, MP),
                ("dv_ex", "derivation", 0.30, 1, MP),
                ("dv_nm", "derivation", None, 1, MP),
                ("dv_old", "derivation", 0.30, 0, MP),  # not current -> not in N
                ("dv_other", "derivation", 0.30, 1, '{"reasoning_type":"inductive_generalization"}'),
                ("ob_a", "observation", 0.5, 1, None)],
               [("dv_ok", "ob_a", "derives_from"), ("dv_bad", "ob_a", "derives_from"),
                ("dv_nm", "ob_a", "derives_from")])
    assert r.n == 4
    assert (len(r.exact), len(r.deviating), len(r.excluded), len(r.null_measured)) == (1, 1, 1, 1)
    mod.check_denominators(r)  # holds: does not raise
    r.exact.append("dv_phantom")  # now 5 != N=4
    with pytest.raises(Exception, match="denominator"):
        mod.check_denominators(r)
