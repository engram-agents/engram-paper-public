"""Tests for tools/type_reclassification/db.py: outcome classification (every
branch), fs_class proxy fallback, and multi-graph frame merging.
"""

from __future__ import annotations

from tools.type_reclassification import db, fixtures


def _build_frame(tmp_path, graph_id="graph_a"):
    path = fixtures.build_synthetic_db(str(tmp_path), fixtures.default_fixture_rows())
    conn = db.connect(path)
    try:
        rows = db.fetch_frame(conn, graph_id)
    finally:
        conn.close()
    return {row.id: row for row in rows}


# ---------------------------------------------------------------------------
# classify_outcome: every branch
# ---------------------------------------------------------------------------

def test_refuted_branch_all_include_error_types(tmp_path):
    by_id = _build_frame(tmp_path)
    for suffix in ("hallucinated", "wrong_evidence", "fabricated", "other"):
        node_id = f"ob_fx_refuted_{suffix}"
        assert by_id[node_id].outcome == "refuted", node_id


def test_excluded_branch_duplicate_and_wrong_citation(tmp_path):
    by_id = _build_frame(tmp_path)
    assert by_id["ob_fx_excluded_duplicate"].outcome == "excluded"
    assert by_id["ob_fx_excluded_wrong_citation"].outcome == "excluded"


def test_contradicted_and_lost_clean_case(tmp_path):
    """A loses to B; B itself is the resolver."""
    by_id = _build_frame(tmp_path)
    assert by_id["ob_fx_contra_loser_a"].outcome == "refuted"
    assert by_id["ob_fx_contra_winner_b"].outcome == "survived"


def test_contradicted_and_lost_derived_from_case(tmp_path):
    """J loses to K; the resolver is a separate derivation that derives_from K."""
    by_id = _build_frame(tmp_path)
    assert by_id["ob_fx_contra_loser_j"].outcome == "refuted"
    assert by_id["ob_fx_contra_winner_k"].outcome == "survived"


def test_contradicted_and_lost_ambiguous_case(tmp_path):
    """E vs F resolved by an independent node G with no derivation link to
    either side -- the schema gives no way to say who won; both sides must
    land on "unclassified", NEVER silently "refuted" or "survived"."""
    by_id = _build_frame(tmp_path)
    assert by_id["ob_fx_contra_ambig_e"].outcome == "unclassified"
    assert by_id["ob_fx_contra_ambig_f"].outcome == "unclassified"
    # G itself is the resolver -- it won (or at least didn't lose).
    assert by_id["ob_fx_contra_ambig_resolver_g"].outcome == "survived"


def test_superseded_is_unclassified_not_refuted_or_survived(tmp_path):
    by_id = _build_frame(tmp_path)
    assert by_id["ob_fx_superseded"].outcome == "unclassified"
    # its current successor is a plain, unrelated node -- survived.
    assert by_id["ob_fx_superseded_successor"].outcome == "survived"


def test_survived_default_branch(tmp_path):
    by_id = _build_frame(tmp_path)
    assert by_id["ob_fx_survived_plain"].outcome == "survived"
    assert by_id["ob_fx_survived_fsclass_override"].outcome == "survived"
    assert by_id["ob_fx_survived_predictive"].outcome == "survived"


def test_unclassified_never_leaks_into_refuted_or_survived_counts(tmp_path):
    """Every 'unclassified' row must remain distinctly tagged -- never
    silently counted alongside refuted/survived."""
    by_id = _build_frame(tmp_path)
    unclassified_ids = {
        node_id for node_id, row in by_id.items() if row.outcome == "unclassified"
    }
    assert unclassified_ids == {
        "ob_fx_superseded",
        "ob_fx_contra_ambig_e",
        "ob_fx_contra_ambig_f",
    }
    for node_id in unclassified_ids:
        assert by_id[node_id].outcome not in ("refuted", "survived")


# ---------------------------------------------------------------------------
# fs_class proxy fallback (ported from engram_core._node_fs_class)
# ---------------------------------------------------------------------------

def test_fs_class_proxy_fallback_from_quote_type(tmp_path):
    by_id = _build_frame(tmp_path)
    row = by_id["ob_fx_survived_plain"]
    assert row.fs_class is None
    assert row.quote_type == "hard_data"
    assert db.resolve_fs_class(row) == "re-executable"


def test_fs_class_native_field_wins_over_proxy(tmp_path):
    by_id = _build_frame(tmp_path)
    row = by_id["ob_fx_survived_fsclass_override"]
    assert row.fs_class == "re-executable"
    # quote_type is 'editorial' -- proxy alone would say 'frozen' -- the
    # native field must win.
    assert row.quote_type == "editorial"
    assert db.resolve_fs_class(row) == "re-executable"


def test_fs_class_unknown_when_neither_field_nor_proxy_known(tmp_path):
    by_id = _build_frame(tmp_path)
    row = by_id["ob_fx_contra_winner_b"]  # default quote_type=attributed_analysis, no fs_class
    assert row.fs_class is None
    assert db.resolve_fs_class(row) == "unknown"


# ---------------------------------------------------------------------------
# Multi-graph merging
# ---------------------------------------------------------------------------

def test_fetch_frame_multi_merges_and_tags_graph_id(tmp_path):
    path_a = fixtures.build_synthetic_db(
        str(tmp_path / "a.db"), fixtures.default_fixture_rows()
    )
    path_b = fixtures.build_synthetic_db(
        str(tmp_path / "b.db"), fixtures.secondary_graph_fixture_rows()
    )
    rows = db.fetch_frame_multi({"graph_a": path_a, "graph_b": path_b})

    graph_ids_seen = {row.graph_id for row in rows}
    assert graph_ids_seen == {"graph_a", "graph_b"}

    # graph B's node-only-in-B is present.
    b_only = [r for r in rows if r.id == "ob_fx_graph_b_only"]
    assert len(b_only) == 1
    assert b_only[0].graph_id == "graph_b"

    # id-collision safety: 'ob_0001' exists in BOTH graphs with different
    # claims -- fetch_frame_multi must preserve both as distinct NodeRows,
    # not collide/deduplicate them.
    collided = [r for r in rows if r.id == "ob_0001"]
    assert len(collided) == 2
    claims_by_graph = {r.graph_id: r.claim for r in collided}
    assert claims_by_graph == {
        "graph_a": "Graph-A's version of ob_0001.",
        "graph_b": "Graph-B's version of ob_0001.",
    }


def test_retracted_with_unknown_error_type_is_unclassified_not_refuted(tmp_path):
    """Regression test for a reviewer-fairy-caught blocker: a retracted node
    whose error_type is missing/None or outside both named lists (a
    malformed row, or a legacy retraction filed before error_type existed --
    confirmed a real possibility via engram-alpha's own edit-history
    backfill code, which explicitly handles error_type=None on old retracted
    rows) must NOT default to "refuted" -- that asserts refuted from ABSENCE
    of positive evidence, contaminating the study's core dependent variable.
    It must fall to "unclassified", same discipline as the superseded and
    contradiction-ambiguous branches."""
    rows = [
        {
            "id": "ob_legacy_no_error_type",
            "type": "observation_factual",
            "claim": "A legacy retracted claim with no error_type recorded.",
            "status": "retracted",
            "is_current": 0,
            "metadata": {},  # no error_type key at all
        },
        {
            "id": "ob_malformed_unknown_error_type",
            "type": "observation_factual",
            "claim": "A retracted claim with an error_type outside both named lists.",
            "status": "retracted",
            "is_current": 0,
            "metadata": {"error_type": "some_future_error_type_not_yet_named"},
        },
    ]
    path = fixtures.build_synthetic_db(str(tmp_path), rows)
    conn = db.connect(path)
    try:
        by_id = {row.id: row for row in db.fetch_frame(conn, "graph_a")}
    finally:
        conn.close()
    assert by_id["ob_legacy_no_error_type"].outcome == "unclassified"
    assert by_id["ob_malformed_unknown_error_type"].outcome == "unclassified"
