"""Tests for tools/compression_fidelity/depth.py -- logic-depth computation
(pre-reg §2/§5): depth = max(depth of premises) + 1, non-derivation
premises (including the axiom/conjecture/lesson judgment call) are depth-1
base cases, and the graph is a DAG so shared premises must be memoized
once, not recomputed per path."""

import pytest

from tools.compression_fidelity.depth import compute_depth_map, depth_tier


def test_observation_with_no_premises_is_depth_1():
    types = {"ob_1": "observation_factual"}
    assert compute_depth_map(types, {}) == {"ob_1": 1}


def test_node_with_explicit_empty_premises_list_is_depth_1():
    types = {"dv_1": "derivation"}
    premises = {"dv_1": []}
    assert compute_depth_map(types, premises) == {"dv_1": 1}


def test_derivation_with_one_observation_premise_is_depth_2():
    types = {"dv_1": "derivation", "ob_1": "observation_factual"}
    premises = {"dv_1": ["ob_1"]}
    depths = compute_depth_map(types, premises)
    assert depths["ob_1"] == 1
    assert depths["dv_1"] == 2


def test_two_level_derivation_chain_is_depth_3():
    types = {"dv_1": "derivation", "dv_2": "derivation", "ob_1": "observation_factual"}
    premises = {"dv_1": ["dv_2"], "dv_2": ["ob_1"]}
    depths = compute_depth_map(types, premises)
    assert depths["ob_1"] == 1
    assert depths["dv_2"] == 2
    assert depths["dv_1"] == 3


def test_shared_premise_dag_case_computed_once_and_reused():
    """Two derivations both cite the SAME observation premise -- its depth
    (1) must be resolved once and reused for both, both landing at depth 2
    (not diverging, not double-counted)."""
    types = {
        "dv_1": "derivation", "dv_2": "derivation", "ob_shared": "observation_factual",
    }
    premises = {"dv_1": ["ob_shared"], "dv_2": ["ob_shared"]}
    depths = compute_depth_map(types, premises)
    assert depths["ob_shared"] == 1
    assert depths["dv_1"] == 2
    assert depths["dv_2"] == 2


def test_axiom_premise_is_a_depth_1_base_case_not_recursed_into():
    """Judgment call explicitly flagged in the module docstring: a
    non-derivation premise (axiom/conjecture/lesson) is treated as a
    depth-1 base case exactly like an observation, even though it isn't
    literally one."""
    types = {"dv_1": "derivation", "ax_1": "axiom"}
    premises = {"dv_1": ["ax_1"]}
    depths = compute_depth_map(types, premises)
    assert depths["ax_1"] == 1
    assert depths["dv_1"] == 2


def test_cycle_detected_and_raises():
    types = {"dv_1": "derivation", "dv_2": "derivation"}
    premises = {"dv_1": ["dv_2"], "dv_2": ["dv_1"]}
    with pytest.raises(RuntimeError):
        compute_depth_map(types, premises)


# ── depth_tier ──────────────────────────────────────────────────────────


def test_depth_tier_boundaries():
    assert depth_tier(1) == "1"
    assert depth_tier(2) == "2"
    assert depth_tier(3) == ">=3"
    assert depth_tier(10) == ">=3"


def test_depth_tier_zero_is_tier_1():
    """depth 0 shouldn't occur in practice, but the code's `if depth <= 1`
    guard means it falls into tier '1' rather than erroring -- worth
    pinning so a future refactor doesn't silently change this."""
    assert depth_tier(0) == "1"
