"""Tests for tools/compression_fidelity/kstar.py -- K* computation
(pre-reg §8.0/§PIN v5-A, v6-A). `ckwrap` is a real, installed dependency
here (not mocked) -- these tests exercise the actual clustering call.
Every expected value below was verified by running the real code first,
not hand-guessed against the DP algorithm's internals.
"""

import pytest

from tools.compression_fidelity.kstar import compute_k_star


def test_two_well_separated_clusters():
    node_ids = [f"n{i}" for i in range(6)]
    scores = [0.1, 0.15, 0.2, 0.8, 0.85, 0.9]
    result = compute_k_star(node_ids, scores)
    assert result.k_star == 2
    assert len(result.centroids) == result.k_star
    assert result.centroids == sorted(result.centroids)


def test_tier_assignments_ordered_by_ascending_centroid():
    """The lower-value cluster must be tier 1, the higher-value cluster
    tier 2 -- not raw ckwrap label order, which need not match ascending
    centroid order without the rank_of remapping."""
    node_ids = ["low_a", "low_b", "low_c", "high_a", "high_b", "high_c"]
    scores = [0.1, 0.15, 0.2, 0.8, 0.85, 0.9]
    result = compute_k_star(node_ids, scores)
    assert result.tier_assignments["low_a"] < result.tier_assignments["high_a"]
    assert result.tier_assignments["low_a"] == 1
    assert result.tier_assignments["high_a"] == 2


def test_mismatched_lengths_raises_value_error():
    with pytest.raises(ValueError):
        compute_k_star(["a"], [0.1, 0.2])


def test_empty_scores_raises_value_error():
    with pytest.raises(ValueError):
        compute_k_star([], [])


def test_degenerate_all_identical_scores():
    result = compute_k_star(["a", "b", "c"], [0.5, 0.5, 0.5])
    assert result.k_star == 1
    assert result.degenerate_reduced is True
    assert result.centroids == [0.5]
    assert result.tier_assignments == {"a": 1, "b": 1, "c": 1}
    assert result.bic is None


def test_degenerate_two_distinct_values_below_k_min_range():
    """n_distinct=2 means effective_k_max = min(6, 2-1) = 1, which is
    < k_min (2) -- hits the 'reduce K* straight to distinct count' branch.
    Verified directly: k_star=2, degenerate_reduced=True."""
    node_ids = ["a", "b", "c", "d", "e", "f"]
    scores = [0.3, 0.3, 0.3, 0.9, 0.9, 0.9]
    result = compute_k_star(node_ids, scores)
    assert result.k_star == 2
    assert result.degenerate_reduced is True
    assert result.n_distinct_values == 2
    assert result.k_requested_max == 6


def test_n_samples_and_n_distinct_values_reported_correctly():
    node_ids = ["a", "b", "c", "d", "e", "f"]
    scores = [0.1, 0.1, 0.5, 0.5, 0.9, 0.95]  # 4 distinct values, 6 samples
    result = compute_k_star(node_ids, scores)
    assert result.n_samples == 6
    assert result.n_distinct_values == 4


def test_k_requested_max_reports_the_original_request_not_the_clamp():
    node_ids = [f"n{i}" for i in range(6)]
    scores = [0.1, 0.15, 0.2, 0.8, 0.85, 0.9]
    result = compute_k_star(node_ids, scores, k_max=6)
    assert result.k_requested_max == 6
