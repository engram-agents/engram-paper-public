"""End-to-end integration test for the compression_fidelity pipeline
(cli.run): synthetic DB -> sampling -> packet extraction -> K* -> output
files. Exercises the REAL pipeline wiring, not individual units -- this is
the test that would have caught a wiring-level mistake (e.g. a real node
ID accidentally reaching a served packet file) that no single module's
unit tests could see on their own.
"""

import json

from tools.compression_fidelity.cli import run
from tests.compression_fidelity.fixtures import build_synthetic_db


def _obs(id_, claim, quoted_text="a quote", confidence=0.95, quote_type="hard_data",
         evidence_id=None, **overrides):
    row = {
        "id": id_, "type": "observation_factual", "claim": claim,
        "quoted_text": quoted_text, "interpretation": "an interpretation",
        "quote_type": quote_type, "confidence": confidence, "evidence_id": evidence_id,
    }
    row.update(overrides)
    return row


def _deriv(id_, claim, logical_chain="because of the premises", reasoning_type="deductive_modus_ponens",
           confidence=0.8, **overrides):
    row = {
        "id": id_, "type": "derivation", "claim": claim,
        "interpretation": "an interpretation", "logical_chain": logical_chain,
        "confidence": confidence, "metadata": {"reasoning_type": reasoning_type},
    }
    row.update(overrides)
    return row


def _build_realistic_graph(tmp_path):
    """A small but structurally realistic graph: several observations at
    varied confidence, a 2-level derivation chain, a shared premise cited
    by two derivations, one observation whose text is mostly confidence-
    leak vocabulary (must be excluded), and one excluded/non-current node
    that must NEVER appear in the frame at all."""
    rows = [
        _obs("ob_0001", "The sky is blue.", confidence=0.95, evidence_id="ev_0001"),
        _obs("ob_0002", "Water boils at 100C at sea level.", confidence=0.85, evidence_id="ev_0001"),
        _obs("ob_0003", "The shared premise both derivations cite.", confidence=0.70, evidence_id="ev_0001"),
        _deriv("dv_0001", "A conclusion drawn from ob_0003.", reasoning_type="deductive_modus_ponens"),
        _deriv("dv_0002", "Another conclusion, also drawn from ob_0003.", reasoning_type="inductive_causal"),
        _deriv(
            "dv_0003", "A conclusion built on dv_0001.",
            logical_chain="chained from the prior derivation", reasoning_type="abductive_best_explanation",
        ),
        # This one must be excluded by the >20%-gutted-chain gate.
        _obs(
            "ob_gutted", "conf 0.95 attributed_analysis conf 0.95 attributed_analysis",
            quoted_text="", interpretation="",
        ),
        # Must never appear in the frame at all (excluded node types / states).
        {"id": "cj_0001", "type": "conjecture", "claim": "a conjecture, out of frame"},
        _obs("ob_superseded", "a superseded observation", is_current=0),
        _obs("ob_retracted", "a retracted observation", status="retracted"),
    ]
    edges = [
        ("dv_0001", "ob_0003", "derives_from"),
        ("dv_0002", "ob_0003", "derives_from"),
        ("dv_0003", "dv_0001", "derives_from"),
    ]
    return build_synthetic_db(tmp_path, rows, edges=edges)


def test_pipeline_produces_expected_output_structure(tmp_path):
    db_path = _build_realistic_graph(tmp_path)
    out_dir = tmp_path / "out"
    manifest = run(db_path, str(out_dir), seed=1, per_cell_target=10, deep_tier_cap=10)

    assert (out_dir / "manifest.json").exists()
    assert (out_dir / "exclusions.json").exists()
    assert (out_dir / "redaction_log.jsonl").exists()
    assert (out_dir / "packets" / "primary").is_dir()
    assert (out_dir / "packets" / "without_interpretation").is_dir()

    on_disk_manifest = json.loads((out_dir / "manifest.json").read_text())
    assert on_disk_manifest["seed"] == 1
    assert manifest["seed"] == 1


def test_frame_excludes_conjecture_superseded_and_retracted_nodes(tmp_path):
    db_path = _build_realistic_graph(tmp_path)
    out_dir = tmp_path / "out"
    manifest = run(db_path, str(out_dir), seed=1, per_cell_target=10, deep_tier_cap=10)

    # 4 real observations (ob_0001, ob_0002, ob_0003, ob_gutted) + 3 derivations
    # (dv_0001, dv_0002, dv_0003) = 7 in frame; cj_0001/ob_superseded/ob_retracted excluded.
    assert manifest["frame_totals"]["observation"] == 4
    assert manifest["frame_totals"]["derivation"] == 3
    assert manifest["frame_totals"]["total"] == 7


def test_gutted_node_is_excluded_and_reported_by_id(tmp_path):
    db_path = _build_realistic_graph(tmp_path)
    out_dir = tmp_path / "out"
    manifest = run(db_path, str(out_dir), seed=1, per_cell_target=10, deep_tier_cap=10)

    exclusions_on_disk = json.loads((out_dir / "exclusions.json").read_text())
    excluded_ids = {e["node_id"] for e in exclusions_on_disk}
    assert "ob_gutted" in excluded_ids
    entry = next(e for e in exclusions_on_disk if e["node_id"] == "ob_gutted")
    assert "20%" in entry["reason"]
    assert entry["arm"] == "primary"


def test_no_real_node_id_appears_in_any_served_packet_file(tmp_path):
    """The load-bearing isolation invariant (reviewer-fairy catch #1): a
    real ENGRAM node ID must NEVER appear inside a served packets/*/*.json
    file -- only the opaque packet_id."""
    db_path = _build_realistic_graph(tmp_path)
    out_dir = tmp_path / "out"
    manifest = run(db_path, str(out_dir), seed=1, per_cell_target=10, deep_tier_cap=10)

    real_node_ids = [
        nid for nid in manifest["packet_id_map"].keys() if nid != "ob_gutted"
    ]
    for packets_dir in ("primary", "without_interpretation"):
        for pkt_file in (out_dir / "packets" / packets_dir).glob("*.json"):
            content = pkt_file.read_text()
            for real_id in real_node_ids:
                assert real_id not in content, f"{real_id} leaked into {pkt_file}"


def test_reasoning_type_and_confidence_never_appear_in_any_served_packet(tmp_path):
    db_path = _build_realistic_graph(tmp_path)
    out_dir = tmp_path / "out"
    run(db_path, str(out_dir), seed=1, per_cell_target=10, deep_tier_cap=10)

    for packets_dir in ("primary", "without_interpretation"):
        for pkt_file in (out_dir / "packets" / packets_dir).glob("*.json"):
            content = pkt_file.read_text()
            for forbidden in ("reasoning_type", "quote_type", "confidence",
                               "deductive_modus_ponens", "inductive_causal",
                               "abductive_best_explanation", "attributed_analysis"):
                assert forbidden not in content, f"{forbidden!r} leaked into {pkt_file}"


def test_packet_id_map_is_researcher_side_only_in_manifest(tmp_path):
    """packet_id_map (the real_id <-> packet_id link) must exist in
    manifest.json (researcher-side) but nowhere else served."""
    db_path = _build_realistic_graph(tmp_path)
    out_dir = tmp_path / "out"
    manifest = run(db_path, str(out_dir), seed=1, per_cell_target=10, deep_tier_cap=10)
    assert "packet_id_map" in manifest
    assert len(manifest["packet_id_map"]) > 0


def test_shared_premise_derivations_both_reference_the_common_node(tmp_path):
    """dv_0001 and dv_0002 both cite ob_0003 -- both must successfully build a
    packet whose reasoning_tree references the shared premise (verifies
    the pipeline wiring end-to-end, not just tree.py in isolation)."""
    db_path = _build_realistic_graph(tmp_path)
    out_dir = tmp_path / "out"
    manifest = run(db_path, str(out_dir), seed=1, per_cell_target=10, deep_tier_cap=10)

    dv1_pkt_id = manifest["packet_id_map"]["dv_0001"]
    dv2_pkt_id = manifest["packet_id_map"]["dv_0002"]
    dv1_content = (out_dir / "packets" / "primary" / f"{dv1_pkt_id}.json").read_text()
    dv2_content = (out_dir / "packets" / "primary" / f"{dv2_pkt_id}.json").read_text()
    assert "shared premise both derivations cite" in dv1_content
    assert "shared premise both derivations cite" in dv2_content


def test_reproducible_given_same_seed(tmp_path):
    db_path = _build_realistic_graph(tmp_path)
    out1 = tmp_path / "out1"
    out2 = tmp_path / "out2"
    m1 = run(db_path, str(out1), seed=5, per_cell_target=10, deep_tier_cap=10)
    m2 = run(db_path, str(out2), seed=5, per_cell_target=10, deep_tier_cap=10)

    # generated_at legitimately differs; compare everything else.
    m1_stable = {k: v for k, v in m1.items() if k != "generated_at"}
    m2_stable = {k: v for k, v in m2.items() if k != "generated_at"}
    assert m1_stable == m2_stable


def test_k_star_computed_over_scored_ids_excludes_gutted_node(tmp_path):
    """ob_gutted is excluded from the primary arm -- its confidence must
    NOT be pooled into the K* computation."""
    db_path = _build_realistic_graph(tmp_path)
    out_dir = tmp_path / "out"
    manifest = run(db_path, str(out_dir), seed=1, per_cell_target=10, deep_tier_cap=10)
    assert "ob_gutted" not in manifest["k_star"]["tier_assignments"]
    assert manifest["k_star"]["n_samples"] == manifest["sample_totals"]["total"] - 1


def test_node_excluded_only_from_without_interpretation_arm_still_counts_in_k_star(tmp_path):
    """Reviewer-fairy suggestion (2026-07-08): cli.py's own comment
    documents that a node excluded ONLY from the without-interpretation
    arm (not the primary arm) still counts toward the K* pool -- it's
    still served via its primary packet, just not in that one sensitivity
    arm. Verified numerically before writing this fixture: a SHORT,
    heavily-leaky claim/quoted_text alongside a LONG, clean interpretation
    passes the primary arm's chain-fraction gate (interpretation dilutes
    the ratio) but fails the without-interpretation arm's gate on its own
    (no interpretation left to dilute it)."""
    rows = [
        _obs(
            "ob_0010",
            "conf 0.95 attributed_analysis",
            quoted_text="conf 0.95 attributed_analysis",
            interpretation="a" * 300,
        ),
    ]
    db_path = build_synthetic_db(tmp_path, rows)
    out_dir = tmp_path / "out"
    manifest = run(db_path, str(out_dir), seed=1, per_cell_target=10, deep_tier_cap=10)

    exclusions = json.loads((out_dir / "exclusions.json").read_text())
    excluded_arms = {e["node_id"]: e["arm"] for e in exclusions}
    assert excluded_arms.get("ob_0010") == "without_interpretation"
    # excluded from the sensitivity arm but NOT the primary arm -> still
    # scored in K*.
    assert "ob_0010" in manifest["k_star"]["tier_assignments"]
