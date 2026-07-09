"""Tests for tools/type_reclassification/frame_export.py.

The withholding test (`test_exported_frame_never_contains_withheld_fields`)
is the LOAD-BEARING safety test for this whole module -- a real leak here
would invalidate the study.
"""

from __future__ import annotations

import json

import pytest

from tools.type_reclassification import db, fixtures, frame_export


def _fetch_rows(tmp_path):
    path = fixtures.build_synthetic_db(tmp_path, fixtures.default_fixture_rows())
    conn = db.connect(path)
    try:
        return db.fetch_frame(conn, "graph_a")
    finally:
        conn.close()


def test_excluded_rows_never_enter_the_exported_frame(tmp_path):
    rows = _fetch_rows(tmp_path)
    frame = frame_export.export_frame(rows)
    exported_ids = {item["id"] for item in frame}
    assert "ob_fx_excluded_duplicate" not in exported_ids
    assert "ob_fx_excluded_wrong_citation" not in exported_ids
    # every non-excluded fixture row IS present
    all_ids = {row.id for row in rows}
    excluded_ids = {row.id for row in rows if row.outcome == "excluded"}
    assert exported_ids == all_ids - excluded_ids


def test_unclassified_rows_are_included_and_tagged(tmp_path):
    rows = _fetch_rows(tmp_path)
    frame = frame_export.export_frame(rows)
    by_id = {item["id"]: item for item in frame}
    for node_id in ("ob_fx_superseded", "ob_fx_contra_ambig_e", "ob_fx_contra_ambig_f"):
        assert node_id in by_id, f"{node_id} must appear in the exported frame"
        assert by_id[node_id]["stratum"]["outcome"] == "unclassified"


def test_frame_shape_is_flat_dv_1081(tmp_path):
    rows = _fetch_rows(tmp_path)
    frame = frame_export.export_frame(rows)
    assert frame, "fixture set must produce at least one exported item"
    for item in frame:
        assert set(item.keys()) == {"id", "claim", "evidence", "stratum"}
        assert set(item["evidence"].keys()) == {
            "quoted_text", "source_class", "source_domain", "source_date",
        }
        assert set(item["stratum"].keys()) == {"outcome", "fs_class"}


def test_export_frame_raises_on_unset_outcome():
    row = db.NodeRow(
        id="ob_x", graph_id="g", type="observation_factual", claim="x",
        quoted_text="x", interpretation=None, quote_type="hard_data",
        evidence_id=None, confidence=0.9,
    )
    assert row.outcome is None
    with pytest.raises(ValueError):
        frame_export.export_frame([row])


def test_exported_frame_never_contains_withheld_fields(tmp_path):
    """The load-bearing safety test: serialize the WHOLE exported frame to
    JSON and grep the whole string -- not just top-level keys -- for any of
    the withheld substrings, per pre-reg §2."""
    rows = _fetch_rows(tmp_path)
    frame = frame_export.export_frame(rows)
    serialized = json.dumps(frame)

    forbidden_substrings = [
        "quote_type",
        "confidence",
        "interpretation",
        "standpoint_author_id",
    ]
    for forbidden in forbidden_substrings:
        assert forbidden not in serialized, (
            f"withheld field/substring {forbidden!r} leaked into the "
            f"exported frame JSON"
        )

    # No raw agent-id-shaped string (pn_\d+, or a namespaced author id) may
    # appear anywhere in the serialized output either.
    import re
    author_id_leak = re.search(r"\bpn_\d+\b", serialized)
    assert author_id_leak is None, (
        f"a pn_* author-id-shaped string leaked: {author_id_leak.group(0)!r}"
    )

    # None of the fixture's own quote_type ENUM VALUES may appear anywhere,
    # even inside claim/quoted_text free text (redact.py's vocabulary pass).
    for enum_value in ("hard_data", "attributed_analysis", "editorial"):
        assert enum_value not in serialized, (
            f"quote_type enum value {enum_value!r} leaked into the frame"
        )

    # No node's own `outcome` state should be discoverable from anywhere
    # OTHER than the dedicated stratum.outcome field -- i.e. every
    # occurrence of an outcome-vocabulary word in the serialized JSON must
    # trace back to a `"outcome": "..."` key or an `"id"` value (ids are
    # explicitly allowed to remain verbatim per the pre-reg -- and this
    # fixture set deliberately uses DESCRIPTIVE ids like
    # "ob_fx_superseded" for readability, which is a test-authoring
    # convenience, not a real leak; production ids are opaque serials like
    # "ob_0004"), not to leaked FREE TEXT (claim/quoted_text).
    # (A crude but effective check: strip every `"id": "..."`,
    # `"outcome": "<value>"`, and `"fs_class": "<value>"` substring, then
    # confirm no outcome-vocabulary word remains in the rest of the string.)
    stripped = re.sub(r'"id":\s*"[^"]*"', "", serialized)
    stripped = re.sub(r'"outcome":\s*"[^"]*"', "", stripped)
    stripped = re.sub(r'"fs_class":\s*"[^"]*"', "", stripped)
    for outcome_word in ("retracted", "superseded", "refuted", "resolved", "contradicted"):
        assert outcome_word not in stripped, (
            f"outcome-vocabulary word {outcome_word!r} leaked outside of "
            f"the dedicated stratum/id fields"
        )


def test_outcome_vocab_in_free_text_is_actually_redacted_through_export(tmp_path):
    """A direct, non-trivial exercise of the redact-integration path (not
    just the belt-and-suspenders check above): a claim whose FREE TEXT
    happens to mention outcome-vocabulary words must have them scrubbed by
    the time it reaches the exported frame."""
    row = db.NodeRow(
        id="ob_z", graph_id="g", type="observation_factual",
        claim="This claim was later retracted after a contradiction was resolved.",
        quoted_text="The original source said the finding was superseded.",
        interpretation=None, quote_type="attributed_analysis",
        evidence_id=None, confidence=0.7, outcome="survived",
    )
    frame = frame_export.export_frame([row])
    item = frame[0]
    for outcome_word in ("retracted", "contradiction", "resolved", "superseded"):
        assert outcome_word not in item["claim"]
        assert outcome_word not in item["evidence"]["quoted_text"]


def test_source_class_read_from_metadata_not_a_column(tmp_path):
    """Confirm source_class (stored in metadata, not a top-level column per
    _add_observation_impl's `obs_metadata = {"source_class": ...}`) round-
    trips correctly through NodeRow -> export_frame."""
    row = db.NodeRow(
        id="ob_y", graph_id="g", type="observation_factual", claim="y",
        quoted_text="y", interpretation=None, quote_type="hard_data",
        evidence_id=None, confidence=0.9,
        metadata={"source_class": "introspective"},
        outcome="survived",
    )
    frame = frame_export.export_frame([row])
    assert frame[0]["evidence"]["source_class"] == "introspective"


# ── export_derivation_frame (derivation arm) ──────────────────────────────


def _derivation_row(node_id, outcome, premises=None, claim=None, **kwargs):
    if premises is None:
        premises = [
            {"claim": "Swan #1 observed at the lake was white.", "type": "hard_data"},
            {"claim": "Swan #2 observed at the lake was white.", "type": None},
        ]
    if claim is None:
        claim = f"Claim for {node_id}."
    row = db.NodeRow(
        id=node_id, graph_id="g", type="derivation", claim=claim,
        quoted_text=None, interpretation=None, quote_type=None,
        evidence_id=None, confidence=0.75,
        outcome=outcome,
        **kwargs,
    )
    row.premises = premises
    return row


def test_excluded_and_excluded_type_rows_never_enter_the_derivation_frame():
    """The one behavior genuinely different from the observation arm: BOTH
    "excluded" and "excluded_type" outcomes must be kept out of the normal
    judge-facing frame. "excluded_type" rows are type-correction cases that
    belong to the separate M5 reconstruction pool
    (`db.mine_m5_reconstruction_pool`) -- letting one leak into this frame
    would hand the judge a case whose ground truth is the study's own
    predictor (type mis-selection), which is exactly the circularity the
    "excluded_type" bucket exists to prevent (see `db.py`'s
    `classify_derivation_outcome` docstring)."""
    rows = [
        _derivation_row("dv_excluded", "excluded"),
        _derivation_row("dv_excluded_type", "excluded_type"),
        _derivation_row("dv_survived", "survived"),
    ]
    frame = frame_export.export_derivation_frame(rows)
    exported_ids = {item["id"] for item in frame}
    assert "dv_excluded" not in exported_ids
    assert "dv_excluded_type" not in exported_ids
    assert exported_ids == {"dv_survived"}


def test_unclassified_derivation_rows_are_included_and_tagged():
    rows = [
        _derivation_row("dv_unclassified", "unclassified"),
        _derivation_row("dv_survived", "survived"),
    ]
    frame = frame_export.export_derivation_frame(rows)
    by_id = {item["id"]: item for item in frame}
    assert "dv_unclassified" in by_id
    assert by_id["dv_unclassified"]["stratum"]["outcome"] == "unclassified"


def test_derivation_frame_shape_is_flat():
    rows = [_derivation_row("dv_survived", "survived")]
    frame = frame_export.export_derivation_frame(rows)
    assert frame, "fixture set must produce at least one exported item"
    for item in frame:
        assert set(item.keys()) == {"id", "claim", "premises", "stratum"}
        assert set(item["stratum"].keys()) == {"outcome", "fs_class"}
        for premise in item["premises"]:
            assert set(premise.keys()) == {"claim", "type"}


def test_export_derivation_frame_raises_on_unset_outcome():
    row = db.NodeRow(
        id="dv_x", graph_id="g", type="derivation", claim="x",
        quoted_text=None, interpretation=None, quote_type=None,
        evidence_id=None, confidence=0.75,
    )
    row.premises = [{"claim": "premise", "type": "hard_data"}]
    assert row.outcome is None
    with pytest.raises(ValueError):
        frame_export.export_derivation_frame([row])


def test_exported_derivation_frame_never_contains_withheld_fields():
    """The load-bearing safety test for the derivation arm: serialize the
    WHOLE exported frame to JSON and grep the whole string -- not just
    top-level keys -- for any of the withheld substrings, per pre-reg §2.
    `reasoning_type` (the node's own filed answer key) is the derivation
    arm's equivalent of the observation arm's withheld `quote_type`."""
    rows = [
        _derivation_row(
            "dv_survived", "survived",
            metadata={"reasoning_type": "inductive_generalization", "standpoint_author_id": "pn_0002"},
        ),
    ]
    frame = frame_export.export_derivation_frame(rows)
    serialized = json.dumps(frame)

    forbidden_substrings = [
        "reasoning_type",
        "confidence",
        "interpretation",
        "standpoint_author_id",
    ]
    for forbidden in forbidden_substrings:
        assert forbidden not in serialized, (
            f"withheld field/substring {forbidden!r} leaked into the "
            f"exported derivation frame JSON"
        )

    import re
    author_id_leak = re.search(r"\bpn_\d+\b", serialized)
    assert author_id_leak is None, (
        f"a pn_* author-id-shaped string leaked: {author_id_leak.group(0)!r}"
    )

    # None of the REASONING_TYPES enum values may appear anywhere, even
    # inside claim/premise-claim free text.
    for enum_value in ("inductive_generalization", "abductive_best_explanation", "deductive_modus_ponens"):
        assert enum_value not in serialized, (
            f"reasoning_type enum value {enum_value!r} leaked into the frame"
        )


def test_premise_claim_is_actually_redacted_through_export():
    """A direct, non-trivial exercise of the redact-integration path
    (mirrors `test_outcome_vocab_in_free_text_is_actually_redacted_through_export`
    for the observation arm): a premise claim whose FREE TEXT happens to
    mention outcome-vocabulary words, or a confidence-shaped number, must
    have them scrubbed by the time it reaches the exported frame."""
    row = _derivation_row(
        "dv_z", "survived",
        claim="Therefore the conclusion is warranted.",
        premises=[
            {
                "claim": "This premise was later retracted after a contradiction was resolved, confidence 0.85.",
                "type": "hard_data",
            },
        ],
    )
    frame = frame_export.export_derivation_frame([row])
    item = frame[0]
    premise_claim = item["premises"][0]["claim"]
    for outcome_word in ("retracted", "contradiction", "resolved"):
        assert outcome_word not in premise_claim
    assert "0.85" not in premise_claim


# ---------------------------------------------------------------------------
# export_m5_frame -- code-enforced M5 withholding (Borges's PR #23 suggestion:
# M5's withholding was previously a caller-contract in a docstring only)
# ---------------------------------------------------------------------------


def _m5_pool_item(node_id="dv_old", claim="the claim", premises=None, ground_truth_type="deductive_modus_ponens"):
    return {
        "pre_correction_packet": {
            "id": node_id,
            "claim": claim,
            "premises": premises or [],
        },
        "ground_truth_type": ground_truth_type,
    }


def test_export_m5_frame_preserves_ground_truth_type_for_scoring():
    """ground_truth_type is researcher-only scoring metadata (mirrors
    stratum's exact role) -- it MUST survive the export so
    analysis.recovery_rate_vs_chance can use it, but callers dispatching
    to the judge must not forward it (see the function's own docstring)."""
    pool = [_m5_pool_item(ground_truth_type="abductive_best_explanation")]
    frame = frame_export.export_m5_frame(pool)
    assert frame[0]["ground_truth_type"] == "abductive_best_explanation"


def test_export_m5_frame_withholds_field_names_not_the_ground_truth_value():
    """The bare field-name words (confidence, interpretation,
    standpoint_author_id, and the literal word "reasoning_type") must never
    appear -- but ground_truth_type's own VALUE (a type name) legitimately
    appears, since carrying it is the whole point of this function."""
    pool = [_m5_pool_item(ground_truth_type="inductive_generalization")]
    frame = frame_export.export_m5_frame(pool)
    serialized = json.dumps(frame)

    for forbidden in ("confidence", "interpretation", "standpoint_author_id"):
        assert forbidden not in serialized
    # The bare FIELD NAME "reasoning_type" must not appear even though a
    # type NAME (which happens to be a reasoning_type value) legitimately does.
    assert '"reasoning_type"' not in serialized
    assert "inductive_generalization" in serialized  # the value itself is expected


def test_export_m5_frame_shape_is_flat():
    pool = [_m5_pool_item(premises=[{"claim": "a premise", "type": "hard_data"}])]
    frame = frame_export.export_m5_frame(pool)
    item = frame[0]
    assert set(item.keys()) == {"id", "claim", "premises", "ground_truth_type"}
    assert item["premises"] == [{"claim": "a premise", "type": "hard_data"}]


def test_export_m5_frame_claim_is_actually_redacted():
    pool = [_m5_pool_item(claim="This claim mentions confidence 0.85 directly.")]
    frame = frame_export.export_m5_frame(pool)
    assert "0.85" not in frame[0]["claim"]


def test_export_m5_frame_premise_claim_is_actually_redacted():
    pool = [_m5_pool_item(premises=[
        {"claim": "This premise was later retracted, confidence 0.40.", "type": "hard_data"},
    ])]
    frame = frame_export.export_m5_frame(pool)
    premise_claim = frame[0]["premises"][0]["claim"]
    assert "retracted" not in premise_claim
    assert "0.40" not in premise_claim


def test_export_m5_frame_empty_pool_returns_empty_list():
    assert frame_export.export_m5_frame([]) == []
