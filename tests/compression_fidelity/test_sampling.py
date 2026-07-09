"""Tests for tools/compression_fidelity/sampling.py -- stratified sampling
(pre-reg §5). The module's own docstring calls its N~250/~35-40-per-cell
arithmetic "the single largest open interpretation" in the package; these
tests target the module's own resolution of that call as spec, not as
something to second-guess.
"""

from tools.compression_fidelity.db import NodeRow
from tools.compression_fidelity.sampling import (
    _cell_key_str,
    assign_packet_ids,
    build_cells,
    draw_stratified_sample,
)


def _obs(id_, confidence=0.95):
    return NodeRow(
        id=id_, type="observation_factual", claim=f"claim {id_}", quoted_text="q",
        interpretation="i", quote_type="hard_data", evidence_id=None,
        logical_chain=None, confidence=confidence, metadata={},
    )


def _deriv(id_, reasoning_type="deductive_modus_ponens"):
    return NodeRow(
        id=id_, type="derivation", claim=f"claim {id_}", quoted_text=None,
        interpretation="i", quote_type=None, evidence_id=None,
        logical_chain="chain", confidence=0.8, metadata={"reasoning_type": reasoning_type},
    )


# ── build_cells ────────────────────────────────────────────────────────────


def test_build_cells_buckets_observation_by_type_tier_confidence_bin():
    nodes = [_obs("ob_1", confidence=0.95)]
    depth_map = {"ob_1": 1}
    cells = build_cells(nodes, depth_map)
    assert ("observation", "1", "0.95") in cells
    assert cells[("observation", "1", "0.95")].node_ids == ["ob_1"]


def test_build_cells_buckets_derivation_by_type_tier_reasoning_type():
    nodes = [_deriv("dv_1", reasoning_type="inductive_causal")]
    depth_map = {"dv_1": 2}
    cells = build_cells(nodes, depth_map)
    assert ("derivation", "2", "inductive_causal") in cells


def test_build_cells_accumulates_multiple_nodes_in_same_cell():
    nodes = [_obs("ob_1", confidence=0.95), _obs("ob_2", confidence=0.95)]
    depth_map = {"ob_1": 1, "ob_2": 1}
    cells = build_cells(nodes, depth_map)
    assert set(cells[("observation", "1", "0.95")].node_ids) == {"ob_1", "ob_2"}


# ── draw_stratified_sample: reproducibility ──────────────────────────────


def test_same_seed_produces_identical_sample():
    nodes = [_obs(f"ob_{i}", confidence=0.95) for i in range(10)]
    depth_map = {n.id: 1 for n in nodes}
    r1 = draw_stratified_sample(nodes, depth_map, seed=42, per_cell_target=3)
    r2 = draw_stratified_sample(nodes, depth_map, seed=42, per_cell_target=3)
    assert r1.sampled_ids == r2.sampled_ids


def test_result_reports_the_seed_used():
    nodes = [_obs("ob_1")]
    depth_map = {"ob_1": 1}
    result = draw_stratified_sample(nodes, depth_map, seed=999)
    assert result.seed == 999


# ── deep-tier (>=3) take-all vs capped sampling ──────────────────────────


def test_deep_tier_reduced_when_frame_exceeds_cap():
    nodes = [_deriv(f"dv_{i}") for i in range(5)]
    depth_map = {n.id: 3 for n in nodes}  # all depth 3 -> tier ">=3"
    result = draw_stratified_sample(nodes, depth_map, seed=1, deep_tier_cap=3)
    assert result.deep_tier_frame_count == 5
    assert result.deep_tier_reduced is True
    assert result.deep_tier_sampled_count == 3


def test_deep_tier_take_all_when_under_cap():
    nodes = [_deriv(f"dv_{i}") for i in range(5)]
    depth_map = {n.id: 4 for n in nodes}  # depth 4 -> tier ">=3" too
    result = draw_stratified_sample(nodes, depth_map, seed=1, deep_tier_cap=10)
    assert result.deep_tier_frame_count == 5
    assert result.deep_tier_reduced is False
    assert result.deep_tier_sampled_count == 5


# ── per-cell target capping for non-deep slabs ────────────────────────────


def test_per_cell_target_caps_a_cell_over_target():
    nodes = [_obs(f"ob_{i}", confidence=0.95) for i in range(5)]
    depth_map = {n.id: 1 for n in nodes}
    result = draw_stratified_sample(nodes, depth_map, seed=1, per_cell_target=2)
    key = _cell_key_str("observation", "1", "0.95")
    assert result.frame_cell_counts[key] == 5
    assert result.sampled_cell_counts[key] == 2


def test_per_cell_take_all_when_under_target():
    nodes = [_obs(f"ob_{i}", confidence=0.95) for i in range(3)]
    depth_map = {n.id: 1 for n in nodes}
    result = draw_stratified_sample(nodes, depth_map, seed=1, per_cell_target=10)
    key = _cell_key_str("observation", "1", "0.95")
    assert result.sampled_cell_counts[key] == 3


def test_cell_key_string_format():
    assert _cell_key_str("observation", "1", "0.95") == "observation|1|0.95"


def test_sampled_ids_are_sorted_and_deduplicated():
    nodes = [_obs(f"ob_{i}", confidence=0.95) for i in range(5)]
    depth_map = {n.id: 1 for n in nodes}
    result = draw_stratified_sample(nodes, depth_map, seed=1, per_cell_target=10)
    assert result.sampled_ids == sorted(set(result.sampled_ids))


# ── without-interpretation subsample ──────────────────────────────────────


def test_without_interpretation_every_populated_cell_gets_a_representative():
    obs_nodes = [_obs(f"ob_{i}", confidence=0.95) for i in range(4)]
    dv_nodes = [_deriv(f"dv_{i}") for i in range(4)]
    nodes = obs_nodes + dv_nodes
    depth_map = {**{n.id: 1 for n in obs_nodes}, **{n.id: 2 for n in dv_nodes}}
    result = draw_stratified_sample(nodes, depth_map, seed=1, per_cell_target=10)
    without_interp = set(result.without_interpretation_ids)
    assert without_interp & {n.id for n in obs_nodes}
    assert without_interp & {n.id for n in dv_nodes}


def test_without_interpretation_target_is_max_1_round_n_over_2():
    """Verified directly against Python's actual round() behavior
    (banker's rounding) rather than hand-guessed: round(10/2)=5,
    round(1/2)=0 so max(1,0)=1, round(3/2)=2 so max(1,2)=2."""
    nodes = [_obs(f"ob_{i}", confidence=0.95) for i in range(10)]
    depth_map = {n.id: 1 for n in nodes}
    result = draw_stratified_sample(nodes, depth_map, seed=1, per_cell_target=10)
    assert len(result.without_interpretation_ids) == 5  # max(1, round(10/2))


def test_without_interpretation_single_item_cell_still_gets_one():
    nodes = [_obs("ob_1", confidence=0.95)]
    depth_map = {"ob_1": 1}
    result = draw_stratified_sample(nodes, depth_map, seed=1, per_cell_target=10)
    assert result.without_interpretation_ids == ["ob_1"]


# ── assign_packet_ids ──────────────────────────────────────────────────────


def test_assign_packet_ids_one_per_input_no_real_id_leaks_as_value():
    node_ids = [f"ob_{i}" for i in range(5)]
    mapping = assign_packet_ids(node_ids, seed=1)
    assert set(mapping.keys()) == set(node_ids)
    assert all(v.startswith("pkt_") for v in mapping.values())
    assert set(mapping.values()) not in (set(node_ids),)  # values are never real IDs
    for real_id in node_ids:
        assert real_id not in mapping.values()


def test_assign_packet_ids_reproducible_given_same_seed():
    node_ids = [f"ob_{i}" for i in range(10)]
    m1 = assign_packet_ids(node_ids, seed=7)
    m2 = assign_packet_ids(node_ids, seed=7)
    assert m1 == m2


def test_assign_packet_ids_different_seeds_differ():
    node_ids = [f"ob_{i}" for i in range(20)]
    m1 = assign_packet_ids(node_ids, seed=1)
    m2 = assign_packet_ids(node_ids, seed=2)
    assert m1 != m2  # non-deterministic-of-failure in principle, but overwhelmingly likely at n=20


def test_assign_packet_ids_zero_padding_width():
    node_ids = ["ob_1", "ob_2", "ob_3"]
    mapping = assign_packet_ids(node_ids, seed=1)
    assert all(len(v) == len("pkt_00001") for v in mapping.values())
