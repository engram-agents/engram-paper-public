"""Tests for tools/compression_fidelity/db.py -- the pre-reg §PIN1 frame
filter (`fetch_frame`: current, non-retracted, non-superseded observations
+ derivations ONLY) plus the other read helpers. Exercised against a real
synthetic SQLite DB (fixtures.py) so the actual SQL runs, not a mock.
"""

from tools.compression_fidelity.db import (
    connect,
    fetch_all_derives_from,
    fetch_all_node_types,
    fetch_evidence_fields,
    fetch_frame,
    fetch_node,
)
from tests.compression_fidelity.fixtures import build_synthetic_db


def _node(id_, type_, **overrides):
    row = {"id": id_, "type": type_, "claim": f"claim for {id_}"}
    row.update(overrides)
    return row


def _with_conn(tmp_path, rows, edges, fn):
    db_path = build_synthetic_db(tmp_path, rows, edges=edges)
    conn = connect(db_path)
    try:
        return fn(conn)
    finally:
        conn.close()


# ── §PIN1: fetch_frame's node-type filter ────────────────────────────────


def test_frame_includes_observation_factual_and_predictive(tmp_path):
    rows = [
        _node("ob_1", "observation_factual"),
        _node("ob_2", "observation_predictive"),
    ]
    frame = _with_conn(tmp_path, rows, None, fetch_frame)
    assert {n.id for n in frame} == {"ob_1", "ob_2"}


def test_frame_includes_derivation(tmp_path):
    rows = [_node("dv_1", "derivation")]
    frame = _with_conn(tmp_path, rows, None, fetch_frame)
    assert {n.id for n in frame} == {"dv_1"}


def test_frame_excludes_conjecture_axiom_cornerstone_lesson_definition_question(tmp_path):
    rows = [
        _node("ob_1", "observation_factual"),
        _node("cj_1", "conjecture"),
        _node("ax_1", "axiom"),
        _node("cs_1", "cornerstone"),
        _node("ls_1", "lesson"),
        _node("df_1", "definition"),
        _node("qu_1", "question"),
    ]
    frame = _with_conn(tmp_path, rows, None, fetch_frame)
    assert {n.id for n in frame} == {"ob_1"}


def test_frame_excludes_theory_judgment_call(tmp_path):
    """constants.py's DERIVATION_TYPES = {"derivation"} only -- `theory` is
    explicitly excluded per the module's own judgment-call note, even
    though engram-alpha's schema technically allows it."""
    rows = [_node("ob_1", "observation_factual"), _node("th_1", "theory")]
    frame = _with_conn(tmp_path, rows, None, fetch_frame)
    assert {n.id for n in frame} == {"ob_1"}


def test_frame_excludes_non_current_is_current_zero(tmp_path):
    """is_current=0 marks a superseded node -- excluded per §PIN1's
    'non-superseded' clause (a supersede flips the OLD node's is_current
    to 0)."""
    rows = [
        _node("ob_1", "observation_factual", is_current=1),
        _node("ob_2", "observation_factual", is_current=0),
    ]
    frame = _with_conn(tmp_path, rows, None, fetch_frame)
    assert {n.id for n in frame} == {"ob_1"}


def test_frame_excludes_retracted_status(tmp_path):
    rows = [
        _node("ob_1", "observation_factual", status="active"),
        _node("ob_2", "observation_factual", status="retracted"),
        _node("ob_3", "observation_factual", status=None),
    ]
    frame = _with_conn(tmp_path, rows, None, fetch_frame)
    ids = {n.id for n in frame}
    assert "ob_2" not in ids
    assert {"ob_1", "ob_3"} <= ids


def test_frame_empty_when_no_eligible_nodes(tmp_path):
    rows = [_node("cj_1", "conjecture")]
    frame = _with_conn(tmp_path, rows, None, fetch_frame)
    assert frame == []


# ── fetch_node / fetch_evidence_fields ────────────────────────────────────


def test_fetch_node_returns_the_node(tmp_path):
    rows = [_node("ob_1", "observation_factual", claim="specific claim text")]
    node = _with_conn(tmp_path, rows, None, lambda c: fetch_node(c, "ob_1"))
    assert node is not None
    assert node.claim == "specific claim text"


def test_fetch_node_missing_returns_none(tmp_path):
    rows = [_node("ob_1", "observation_factual")]
    node = _with_conn(tmp_path, rows, None, lambda c: fetch_node(c, "ob_does_not_exist"))
    assert node is None


def test_node_row_reasoning_type_property_reads_metadata(tmp_path):
    rows = [_node("dv_1", "derivation", metadata={"reasoning_type": "inductive_causal"})]
    node = _with_conn(tmp_path, rows, None, lambda c: fetch_node(c, "dv_1"))
    assert node.reasoning_type == "inductive_causal"


def test_node_row_reasoning_type_none_when_absent(tmp_path):
    rows = [_node("ob_1", "observation_factual")]
    node = _with_conn(tmp_path, rows, None, lambda c: fetch_node(c, "ob_1"))
    assert node.reasoning_type is None


def test_fetch_evidence_fields_returns_source_fields(tmp_path):
    rows = [
        _node("ev_1", "evidence", source_url="http://x.com", source_domain="x.com",
              source_title="X Title", source_date="2026-01-01"),
    ]
    ev = _with_conn(tmp_path, rows, None, lambda c: fetch_evidence_fields(c, "ev_1"))
    assert ev == {
        "url": "http://x.com", "domain": "x.com",
        "title": "X Title", "source_date": "2026-01-01",
    }


def test_fetch_evidence_fields_missing_id_returns_all_none(tmp_path):
    rows = [_node("ob_1", "observation_factual")]
    ev = _with_conn(tmp_path, rows, None, lambda c: fetch_evidence_fields(c, "ev_missing"))
    assert ev == {"url": None, "domain": None, "title": None, "source_date": None}


# ── fetch_all_derives_from / fetch_all_node_types ─────────────────────────


def test_fetch_all_derives_from_groups_by_source_in_edge_order(tmp_path):
    rows = [
        _node("dv_1", "derivation"),
        _node("ob_1", "observation_factual"),
        _node("ob_2", "observation_factual"),
    ]
    edges = [("dv_1", "ob_1", "derives_from"), ("dv_1", "ob_2", "derives_from")]
    premises = _with_conn(tmp_path, rows, edges, fetch_all_derives_from)
    assert premises == {"dv_1": ["ob_1", "ob_2"]}


def test_fetch_all_derives_from_ignores_other_relations(tmp_path):
    rows = [_node("dv_1", "derivation"), _node("ob_1", "observation_factual")]
    edges = [("dv_1", "ob_1", "contradicts")]
    premises = _with_conn(tmp_path, rows, edges, fetch_all_derives_from)
    assert premises == {}


def test_fetch_all_node_types_covers_frame_excluded_types_too(tmp_path):
    """Used to resolve premise types OUTSIDE the sampling frame (e.g. an
    axiom cited as a premise) -- must include every node, not just
    frame-eligible ones."""
    rows = [_node("ob_1", "observation_factual"), _node("ax_1", "axiom")]
    types = _with_conn(tmp_path, rows, None, fetch_all_node_types)
    assert types == {"ob_1": "observation_factual", "ax_1": "axiom"}
