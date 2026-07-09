"""Tests for the derivation-arm functions in tools/type_reclassification/db.py
(reasoning_type re-classification, §2/§4/§5 M5). Synthetic fixtures only,
per the study's freeze discipline -- nothing here touches a real graph.
"""

from tools.type_reclassification.db import (
    NodeRow,
    classify_derivation_outcome,
    connect,
    fetch_derivation_frame,
    fetch_derivation_premises,
    find_type_correction_partner,
    mine_m5_reconstruction_pool,
)
from tools.type_reclassification.fixtures import build_synthetic_db


def _dv(id_, claim, reasoning_type, **overrides):
    row = {
        "id": id_,
        "type": "derivation",
        "claim": claim,
        "quote_type": None,
        "metadata": {"reasoning_type": reasoning_type},
        **overrides,
    }
    return row


def _ob(id_, claim, quote_type="hard_data", **overrides):
    return {"id": id_, "type": "observation_factual", "claim": claim, "quote_type": quote_type, **overrides}


# ── fetch_derivation_premises ──────────────────────────────────────────────


def test_fetch_derivation_premises_mixed_types(tmp_path):
    rows = [
        _ob("ob_1", "premise A", quote_type="hard_data"),
        _dv("dv_1", "premise B", "inductive_analogy"),
        _dv("dv_2", "conclusion", "deductive_modus_ponens"),
        {"_edge": {"source_id": "dv_2", "target_id": "ob_1", "relation": "derives_from"}},
        {"_edge": {"source_id": "dv_2", "target_id": "dv_1", "relation": "derives_from"}},
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        premises = fetch_derivation_premises(conn, "dv_2")
    finally:
        conn.close()

    by_claim = {p["claim"]: p["type"] for p in premises}
    assert by_claim["premise A"] == "hard_data"
    assert by_claim["premise B"] == "inductive_analogy"


def test_fetch_derivation_premises_non_claim_type_has_none_type(tmp_path):
    """A premise that's neither observation nor derivation (e.g. an axiom)
    gets type=None rather than an invented value."""
    rows = [
        {"id": "ax_1", "type": "axiom", "claim": "axiom premise"},
        _dv("dv_1", "conclusion", "deductive_modus_ponens"),
        {"_edge": {"source_id": "dv_1", "target_id": "ax_1", "relation": "derives_from"}},
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        premises = fetch_derivation_premises(conn, "dv_1")
    finally:
        conn.close()
    assert premises == [{"claim": "axiom premise", "type": None}]


# ── find_type_correction_partner ───────────────────────────────────────────


def test_partner_form_a_supersede_with_type_change(tmp_path):
    rows = [
        _dv("dv_old", "the claim", "inductive_analogy", superseded_by="dv_new", is_current=0),
        _dv("dv_new", "the claim", "deductive_modus_ponens"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old = fetch_derivation_frame(conn, "g1")
    finally:
        conn.close()
    old_row = next(r for r in old if r.id == "dv_old")
    conn = connect(db_path)
    try:
        search = find_type_correction_partner(conn, old_row)
    finally:
        conn.close()
    assert search.partner is not None
    assert search.partner.id == "dv_new"


def test_partner_form_a_supersede_without_type_change_returns_none(tmp_path):
    """A supersede that DIDN'T change reasoning_type is a content refinement,
    not a type correction -- must not be mined as excluded_type."""
    rows = [
        _dv("dv_old", "the claim", "inductive_analogy", superseded_by="dv_new", is_current=0),
        _dv("dv_new", "the claim, refined", "inductive_analogy"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
        search = find_type_correction_partner(conn, old_row)
    finally:
        conn.close()
    assert search.partner is None


def test_partner_form_b_retract_other_plus_refile(tmp_path):
    rows = [
        _dv(
            "dv_old", "the claim", "inductive_analogy",
            status="retracted", metadata={"reasoning_type": "inductive_analogy", "error_type": "other"},
            created_at="2026-01-01T00:00:00Z",
        ),
        _dv("dv_new", "the claim", "deductive_modus_ponens", created_at="2026-01-02T00:00:00Z"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
        search = find_type_correction_partner(conn, old_row)
    finally:
        conn.close()
    assert search.partner is not None
    assert search.partner.id == "dv_new"


def test_partner_form_b_ignores_earlier_same_claim_diff_type_node(tmp_path):
    """Colleague-review-caught gap (Borges): the docstring says "a LATER
    derivation" but the original query had no created_at bound at all --
    only an ORDER BY, which sorts but doesn't exclude earlier candidates.
    An earlier same-claim-diff-type node must NEVER be picked as the
    correction partner; only a genuinely later refile counts."""
    rows = [
        _dv("dv_earlier", "the claim", "abductive_best_explanation",
            created_at="2025-12-01T00:00:00Z"),  # earlier, different type -- must be ignored
        _dv(
            "dv_old", "the claim", "inductive_analogy",
            status="retracted", metadata={"reasoning_type": "inductive_analogy", "error_type": "other"},
            created_at="2026-01-01T00:00:00Z",
        ),
        _dv("dv_later_refile", "the claim", "deductive_modus_ponens",
            created_at="2026-01-02T00:00:00Z"),  # genuinely later -- must be picked
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
        search = find_type_correction_partner(conn, old_row)
    finally:
        conn.close()
    assert search.partner is not None
    assert search.partner.id == "dv_later_refile"


def test_partner_form_b_no_refile_found_returns_none(tmp_path):
    rows = [
        _dv(
            "dv_old", "an orphaned claim", "inductive_analogy",
            status="retracted", metadata={"reasoning_type": "inductive_analogy", "error_type": "other"},
        ),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
        search = find_type_correction_partner(conn, old_row)
    finally:
        conn.close()
    assert search.partner is None


def test_partner_retract_non_other_error_type_never_a_candidate(tmp_path):
    """A retraction with error_type != 'other' (e.g. hallucinated_claim) is
    a real refutation, not a type-error-in-disguise -- must never be mined
    as a type-correction candidate even if a same-claim later node exists
    by coincidence."""
    rows = [
        _dv(
            "dv_old", "the claim", "inductive_analogy",
            status="retracted",
            metadata={"reasoning_type": "inductive_analogy", "error_type": "hallucinated_claim"},
        ),
        _dv("dv_new", "the claim", "deductive_modus_ponens"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
        search = find_type_correction_partner(conn, old_row)
    finally:
        conn.close()
    assert search.partner is None


def test_partner_both_forms_simultaneously_form_b_not_suppressed_by_form_a(tmp_path):
    """Reviewer-fairy-caught blocker regression: a derivation can be BOTH
    superseded (by a content-only refinement -- SAME reasoning_type, not
    itself a type correction) AND SEPARATELY retracted later with
    error_type='other' -- engram-alpha's _retract_impl never checks
    superseded_by/is_current before retracting (confirmed against
    engram_revision.py; the reverse order, retract-then-supersede, IS
    blocked by _supersede_impl's is_current requirement, but this order
    is not). The original `if row.superseded_by: ... elif retracted: ...`
    structure let the Form (a) branch win, find no type change on the
    supersede partner, and return None -- silently losing a genuine Form
    (b) refile that exists elsewhere in the graph. Both forms must now be
    checked independently."""
    rows = [
        _dv(
            "dv_old", "the claim", "inductive_analogy",
            status="retracted", superseded_by="dv_sibling",
            metadata={"reasoning_type": "inductive_analogy", "error_type": "other"},
            created_at="2026-01-01T00:00:00Z",
        ),
        # Form (a) candidate: same reasoning_type as dv_old -- a content
        # refinement, NOT a type correction. Must not suppress Form (b).
        _dv("dv_sibling", "the claim", "inductive_analogy", created_at="2026-01-02T00:00:00Z"),
        # Form (b) candidate: the genuine refile, different reasoning_type.
        _dv("dv_refile", "the claim", "deductive_modus_ponens", created_at="2026-01-03T00:00:00Z"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
        search = find_type_correction_partner(conn, old_row)
    finally:
        conn.close()
    assert search.partner is not None
    assert search.partner.id == "dv_refile"


def test_classify_both_forms_simultaneously_yields_excluded_type_not_refuted(tmp_path):
    """Same scenario as above, through classify_derivation_outcome's full
    branch: must classify as excluded_type, not refuted -- the exact
    silent-corruption the reviewer-fairy reproduced (`outcome: refuted`
    before this fix, should be `excluded_type`)."""
    rows = [
        _dv(
            "dv_old", "the claim", "inductive_analogy",
            status="retracted", superseded_by="dv_sibling",
            metadata={"reasoning_type": "inductive_analogy", "error_type": "other"},
            created_at="2026-01-01T00:00:00Z",
        ),
        _dv("dv_sibling", "the claim", "inductive_analogy", created_at="2026-01-02T00:00:00Z"),
        _dv("dv_refile", "the claim", "deductive_modus_ponens", created_at="2026-01-03T00:00:00Z"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
    finally:
        conn.close()
    assert old_row.outcome == "excluded_type"


def test_partner_multiple_candidates_takes_earliest(tmp_path):
    rows = [
        _dv(
            "dv_old", "the claim", "inductive_analogy",
            status="retracted", metadata={"reasoning_type": "inductive_analogy", "error_type": "other"},
            created_at="2026-01-01T00:00:00Z",
        ),
        _dv("dv_new_2", "the claim", "abductive_best_explanation", created_at="2026-01-03T00:00:00Z"),
        _dv("dv_new_1", "the claim", "deductive_modus_ponens", created_at="2026-01-02T00:00:00Z"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
        search = find_type_correction_partner(conn, old_row)
    finally:
        conn.close()
    assert search.partner.id == "dv_new_1"


# ── classify_derivation_outcome ────────────────────────────────────────────


def test_classify_excluded_duplicate(tmp_path):
    rows = [_dv("dv_1", "x", "inductive_analogy", status="retracted",
                metadata={"reasoning_type": "inductive_analogy", "error_type": "duplicate"})]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        row = next(r for r in fetch_derivation_frame(conn, "g1"))
    finally:
        conn.close()
    assert row.outcome == "excluded"


def test_classify_excluded_type_via_refile(tmp_path):
    rows = [
        _dv("dv_old", "the claim", "inductive_analogy", status="retracted",
            metadata={"reasoning_type": "inductive_analogy", "error_type": "other"},
            created_at="2026-01-01T00:00:00Z"),
        _dv("dv_new", "the claim", "deductive_modus_ponens", created_at="2026-01-02T00:00:00Z"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
    finally:
        conn.close()
    assert old_row.outcome == "excluded_type"


def test_classify_refuted_when_other_has_no_refile(tmp_path):
    """error_type='other' WITHOUT a same-claim-diff-type partner is a real
    refutation, not a type error -- must fall through to 'refuted', not
    silently become 'excluded_type' or 'unclassified'."""
    rows = [_dv("dv_1", "an orphaned claim", "inductive_analogy", status="retracted",
                metadata={"reasoning_type": "inductive_analogy", "error_type": "other"})]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        row = next(r for r in fetch_derivation_frame(conn, "g1"))
    finally:
        conn.close()
    assert row.outcome == "refuted"


def test_partner_indeterminate_when_row_reasoning_type_is_none(tmp_path):
    """Colleague-review-caught gap (Borges, 2026-07-08): a same-claim
    candidate exists, but row's OWN reasoning_type is unknown (legacy/
    backfilled derivation) -- the type-change comparison can't be made at
    all. Must be flagged indeterminate, NOT silently treated as
    "compared, no change" (which the old `and`-short-circuit did)."""
    rows = [
        _dv("dv_old", "the claim", "inductive_analogy", status="retracted",
            metadata={"error_type": "other"},  # no reasoning_type key at all
            created_at="2026-01-01T00:00:00Z"),
        _dv("dv_new", "the claim", "deductive_modus_ponens", created_at="2026-01-02T00:00:00Z"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
        search = find_type_correction_partner(conn, old_row)
    finally:
        conn.close()
    assert search.partner is None
    assert search.indeterminate is True


def test_classify_indeterminate_type_comparison_routes_to_unclassified(tmp_path):
    """Same scenario through the full classify_derivation_outcome branch:
    must land as 'unclassified', never 'refuted' (assessed-and-clean) NOR
    'excluded_type' (confirmed correction) -- "can't tell" must never be
    silently upgraded to either assessed state."""
    rows = [
        _dv("dv_old", "the claim", "inductive_analogy", status="retracted",
            metadata={"error_type": "other"},
            created_at="2026-01-01T00:00:00Z"),
        _dv("dv_new", "the claim", "deductive_modus_ponens", created_at="2026-01-02T00:00:00Z"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
    finally:
        conn.close()
    assert old_row.outcome == "unclassified"


def test_classify_refuted_hallucinated_claim(tmp_path):
    rows = [_dv("dv_1", "x", "inductive_analogy", status="retracted",
                metadata={"reasoning_type": "inductive_analogy", "error_type": "hallucinated_claim"})]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        row = next(r for r in fetch_derivation_frame(conn, "g1"))
    finally:
        conn.close()
    assert row.outcome == "refuted"


def test_classify_unclassified_supersede_no_type_change(tmp_path):
    rows = [
        _dv("dv_old", "the claim", "inductive_analogy", superseded_by="dv_new", is_current=0),
        _dv("dv_new", "the claim, refined", "inductive_analogy"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
    finally:
        conn.close()
    assert old_row.outcome == "unclassified"


def test_classify_excluded_type_via_supersede(tmp_path):
    rows = [
        _dv("dv_old", "the claim", "inductive_analogy", superseded_by="dv_new", is_current=0),
        _dv("dv_new", "the claim", "deductive_modus_ponens"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        old_row = next(r for r in fetch_derivation_frame(conn, "g1") if r.id == "dv_old")
    finally:
        conn.close()
    assert old_row.outcome == "excluded_type"


def test_classify_survived_plain(tmp_path):
    rows = [_dv("dv_1", "x", "deductive_modus_ponens")]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        row = next(r for r in fetch_derivation_frame(conn, "g1"))
    finally:
        conn.close()
    assert row.outcome == "survived"


# ── mine_m5_reconstruction_pool ────────────────────────────────────────────


def test_m5_pool_contains_pre_correction_packet_and_ground_truth(tmp_path):
    rows = [
        _ob("ob_1", "supporting evidence", quote_type="hard_data"),
        _dv("dv_old", "the claim", "inductive_analogy", status="retracted",
            metadata={"reasoning_type": "inductive_analogy", "error_type": "other"},
            created_at="2026-01-01T00:00:00Z"),
        _dv("dv_new", "the claim", "deductive_modus_ponens", created_at="2026-01-02T00:00:00Z"),
        {"_edge": {"source_id": "dv_old", "target_id": "ob_1", "relation": "derives_from"}},
        # a clean survivor that must NOT appear in the M5 pool
        _dv("dv_clean", "unrelated survivor claim", "authority_expert"),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        pool = mine_m5_reconstruction_pool(conn, "g1")
    finally:
        conn.close()

    assert len(pool) == 1
    item = pool[0]
    assert item["pre_correction_packet"]["id"] == "dv_old"
    assert item["pre_correction_packet"]["claim"] == "the claim"
    assert item["pre_correction_packet"]["premises"] == [
        {"claim": "supporting evidence", "type": "hard_data"}
    ]
    assert item["ground_truth_type"] == "deductive_modus_ponens"


def test_m5_pool_empty_when_no_type_corrections(tmp_path):
    rows = [_dv("dv_1", "x", "deductive_modus_ponens")]
    db_path = build_synthetic_db(tmp_path, rows)
    conn = connect(db_path)
    try:
        pool = mine_m5_reconstruction_pool(conn, "g1")
    finally:
        conn.close()
    assert pool == []
