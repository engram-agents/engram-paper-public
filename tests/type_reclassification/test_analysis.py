"""Tests for analysis.py -- M1 (divergence), M2 (OR+CI), M4 (pooled OR),
M5 (recovery rate vs chance). Key formulas cross-checked against
`scipy.stats` during test-writing (see inline notes) as an external
validation of the hand-rolled math -- scipy itself is NOT a runtime
dependency of analysis.py (stdlib `math` only), matching this package's
existing zero-new-package discipline (interrater.py's own Fleiss-kappa
precedent).
"""

import math

import pytest

from tools.type_reclassification.analysis import (
    DivergenceResult,
    build_2x2_from_divergence,
    compute_divergence,
    confusion_matrix,
    divergence_rate,
    odds_ratio_ci,
    pooled_odds_ratio,
    recovery_rate_vs_chance,
)

# ── M1: divergence ──────────────────────────────────────────────────────────


def test_compute_divergence_basic():
    filed = {"dv_1": "deductive_modus_ponens", "dv_2": "inductive_analogy"}
    majorities = {"dv_1": "deductive_modus_ponens", "dv_2": "abductive_best_explanation"}
    results = compute_divergence(filed, majorities)
    by_id = {r.packet_id: r for r in results}
    assert by_id["dv_1"].is_divergent is False
    assert by_id["dv_2"].is_divergent is True


def test_compute_divergence_discordant_panel_is_not_divergent():
    """A packet with no judge majority (None) is included but NOT counted
    as divergent -- discordance is a different signal than divergence."""
    filed = {"dv_1": "deductive_modus_ponens"}
    majorities = {"dv_1": None}
    results = compute_divergence(filed, majorities)
    assert results[0].is_divergent is False
    assert results[0].judge_majority_type is None


def test_compute_divergence_skips_packets_missing_from_either_input():
    filed = {"dv_1": "x", "dv_2": "y"}
    majorities = {"dv_1": "x"}  # dv_2 missing
    results = compute_divergence(filed, majorities)
    assert len(results) == 1
    assert results[0].packet_id == "dv_1"


def test_divergence_rate_excludes_discordant_items():
    results = [
        DivergenceResult("a", "x", "x", False),
        DivergenceResult("b", "x", "y", True),
        DivergenceResult("c", "x", None, False),  # discordant, excluded from denominator
    ]
    assert divergence_rate(results) == pytest.approx(0.5)  # 1 divergent / 2 decidable


def test_divergence_rate_nan_on_no_decidable_items():
    results = [DivergenceResult("a", "x", None, False)]
    assert math.isnan(divergence_rate(results))


def test_confusion_matrix_excludes_discordant():
    results = [
        DivergenceResult("a", "x", "x", False),
        DivergenceResult("b", "x", "y", True),
        DivergenceResult("c", "x", None, False),
    ]
    cm = confusion_matrix(results)
    assert cm == {("x", "x"): 1, ("x", "y"): 1}


# ── M2: odds ratio + CI ─────────────────────────────────────────────────────


def test_odds_ratio_ci_textbook_example():
    """Cross-checked externally against scipy.stats.norm.ppf(0.975) for the
    critical value and manual OR/log-OR-SE arithmetic: a=10,b=20,c=5,d=25
    -> OR=2.5, CI=(0.735, 8.502) (verified to 3 decimal places)."""
    result = odds_ratio_ci(10, 20, 5, 25)
    assert result.odds_ratio == pytest.approx(2.5)
    assert result.ci_low == pytest.approx(0.7351, abs=1e-3)
    assert result.ci_high == pytest.approx(8.5019, abs=1e-3)
    assert result.zero_cell_corrected is False


def test_odds_ratio_ci_applies_haldane_anscombe_on_zero_cell():
    result = odds_ratio_ci(10, 0, 5, 25)
    assert result.zero_cell_corrected is True
    # corrected cells: 10.5, 0.5, 5.5, 25.5
    expected_or = (10.5 * 25.5) / (0.5 * 5.5)
    assert result.odds_ratio == pytest.approx(expected_or)


def test_odds_ratio_ci_raises_on_all_zero_cells():
    with pytest.raises(ValueError):
        odds_ratio_ci(0, 0, 0, 0)


def test_odds_ratio_greater_than_one_when_divergence_predicts_refutation():
    # a (divergent+refuted) high, d (concordant+not-refuted) high -> OR > 1
    result = odds_ratio_ci(a=30, b=5, c=5, d=30)
    assert result.odds_ratio > 1
    assert result.ci_low > 1  # CI excludes 1 -- a "significant" OR>1 case


def test_build_2x2_from_divergence():
    results = [
        DivergenceResult("a", "x", "y", True),   # divergent
        DivergenceResult("b", "x", "x", False),  # concordant
        DivergenceResult("c", "x", None, False),  # discordant, must be excluded
    ]
    refuted = {"a", "c"}  # a is refuted+divergent; c is refuted but excluded (discordant)
    a, b, c, d = build_2x2_from_divergence(results, refuted)
    assert (a, b, c, d) == (1, 0, 0, 1)  # a: divergent+refuted=1; d: concordant+not-refuted=1


# ── M4: pooled OR (fixed + random effects) ──────────────────────────────────


def test_pooled_odds_ratio_requires_at_least_two_graphs():
    with pytest.raises(ValueError):
        pooled_odds_ratio({"g1": (10, 5, 5, 10)})


def test_pooled_odds_ratio_homogeneous_graphs_random_equals_fixed():
    """When per-graph ORs are IDENTICAL (zero heterogeneity), Cochran's Q
    should be ~0, tau^2 should be 0, and the random-effects pooled OR
    should equal the fixed-effect pooled OR (the RE model collapses to FE
    under perfect homogeneity) -- a verifiable sanity check without needing
    an external DerSimonian-Laird reference implementation."""
    per_graph = {
        "g1": (10, 5, 5, 10),
        "g2": (20, 10, 10, 20),  # same OR (=4), different sample size
        "g3": (30, 15, 15, 30),  # same OR (=4), different sample size
    }
    result = pooled_odds_ratio(per_graph)
    assert result.tau_squared == pytest.approx(0.0, abs=1e-9)
    assert result.q_statistic == pytest.approx(0.0, abs=1e-6)
    assert result.fixed_effect_or == pytest.approx(result.random_effects_or, rel=1e-6)


def test_pooled_odds_ratio_heterogeneous_graphs_random_effects_wider_ci():
    """With genuinely heterogeneous per-graph ORs, tau^2 > 0 and the
    random-effects CI should be WIDER than the fixed-effect CI (RE
    pooling accounts for between-study variance the FE model ignores) --
    a standard, textbook property of DerSimonian-Laird pooling."""
    per_graph = {
        "g1": (30, 5, 5, 30),   # strong effect
        "g2": (12, 10, 10, 12),  # weak effect
        "g3": (20, 18, 18, 20),  # near-null effect
    }
    result = pooled_odds_ratio(per_graph)
    assert result.tau_squared > 0
    fixed_width = math.log(result.fixed_effect_ci_high) - math.log(result.fixed_effect_ci_low)
    re_width = math.log(result.random_effects_ci_high) - math.log(result.random_effects_ci_low)
    assert re_width > fixed_width


def test_pooled_odds_ratio_per_graph_results_present():
    per_graph = {"g1": (10, 5, 5, 10), "g2": (8, 4, 4, 8)}
    result = pooled_odds_ratio(per_graph)
    assert set(result.per_graph.keys()) == {"g1", "g2"}
    assert result.per_graph["g1"].odds_ratio == pytest.approx(4.0)


# ── M5: recovery rate vs chance ──────────────────────────────────────────────


def test_recovery_rate_perfect_recovery_gives_low_p_value():
    m5 = [("x", "x")] * 10  # perfect recovery, 10/10
    result = recovery_rate_vs_chance(m5, n_candidate_types=14)
    assert result.recovery_rate == pytest.approx(1.0)
    assert result.chance_rate == pytest.approx(1 / 14)
    assert result.p_value < 0.001  # far exceeds chance


def test_recovery_rate_at_chance_gives_high_p_value():
    """Recovery rate exactly at chance (1/14 ~ 7.1%) should NOT reject the
    null (recovery == chance) -- p-value should be well above 0.05."""
    n = 140
    n_recovered = round(n / 14)  # exactly at chance
    m5 = [("x", "x")] * n_recovered + [("x", "y")] * (n - n_recovered)
    result = recovery_rate_vs_chance(m5, n_candidate_types=14)
    assert result.p_value > 0.4


def test_recovery_rate_raises_on_empty_pool():
    with pytest.raises(ValueError):
        recovery_rate_vs_chance([], n_candidate_types=14)


def test_recovery_rate_z_statistic_cross_checked_manually():
    """Manual cross-check: n=100, n_recovered=20, chance=1/14 (~0.0714).
    observed_rate=0.20. se = sqrt(chance*(1-chance)/n). z = (0.20-chance)/se.
    Computed independently below (not reusing the module's own formula) to
    catch a copy-paste self-consistency bug."""
    n, n_recovered, n_types = 100, 20, 14
    m5 = [("x", "x")] * n_recovered + [("x", "y")] * (n - n_recovered)
    result = recovery_rate_vs_chance(m5, n_candidate_types=n_types)

    chance = 1 / n_types
    observed = n_recovered / n
    se = math.sqrt(chance * (1 - chance) / n)
    expected_z = (observed - chance) / se

    assert result.z_statistic == pytest.approx(expected_z)
    assert result.n_items == n
    assert result.n_recovered == n_recovered
