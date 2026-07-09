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
