"""Derivation-arm analysis — M0-M5, pre-reg §4/§5/draft-6.

M0 (Fleiss-kappa instrument-validity gate) is NOT reimplemented here — it's
`interrater.fleiss_kappa` / `interrater.instrument_validity_gate`, already
generic over `(ratings_by_item, categories)` and directly reusable for the
derivation-arm panel's own results (call them with the derivation panel's
votes + `derivation_type_definitions.REASONING_TYPES`).

M1-M5 are new, self-contained, stdlib-only (`math` only — no scipy/
statsmodels dependency) statistics, matching this package's existing
zero-new-package-requirement discipline (`dispatch.py`'s own module
docstring: "zero new package requirements to install before it can be
exercised end-to-end" — `interrater.fleiss_kappa` already set this
precedent by hand-implementing kappa rather than importing a stats
library). Every formula below is a standard, textbook one (Wald log-OR CI,
Haldane-Anscombe zero-cell correction, DerSimonian-Laird random-effects
pooling, a one-sample proportion z-test) — verified against `scipy.stats`
during test-writing as an external cross-check (not a runtime dependency;
see `tests/type_reclassification/test_analysis.py`'s own cross-check
notes), not invented ad hoc.

**M2's estimand is the ODDS RATIO, not the risk ratio or the marginal
rate** (Kepler's draft-6 fix, DM/PR#20 comment, 2026-07-08): pre-reg §4 uses
outcome-stratified (case-control) sampling, which identifies the OR, not
the marginal probability of refutation — the OR's direction-symmetry is
also what dissolves H1(cohort-framed)/H0(case-control-framed) into one
estimand. M2 = OR of refutation, divergent-judge-verdict vs
concordant-judge-verdict, pre-committed direction OR > 1 (divergence
predicts refutation).
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Optional

# ---------------------------------------------------------------------------
# M1 — divergence rate + confusion matrix
# ---------------------------------------------------------------------------


@dataclass
class DivergenceResult:
    packet_id: str
    filed_type: str  # the agent's own reasoning_type at filing time
    judge_majority_type: Optional[str]  # None if the panel had no majority (discordant)
    is_divergent: bool  # judge_majority_type is not None and != filed_type


def compute_divergence(
    filed_types: dict,  # packet_id -> agent's filed reasoning_type
    judge_majorities: dict,  # packet_id -> ItemVerdict.majority_type (may be None)
) -> list:
    """One DivergenceResult per packet_id present in BOTH inputs. A packet
    with no judge majority (panel discordant on that item) is included with
    `is_divergent=False` and `judge_majority_type=None` -- a discordant
    panel is NOT evidence of divergence from the filed type (it's evidence
    the panel itself couldn't agree), so it must not silently count toward
    the divergent bucket. Callers computing M2's 2x2 table should exclude
    these (`judge_majority_type is None`) from BOTH the divergent and
    concordant cells, not fold them into concordant by default.
    """
    results = []
    for packet_id, filed_type in filed_types.items():
        if packet_id not in judge_majorities:
            continue
        majority = judge_majorities[packet_id]
        divergent = majority is not None and majority != filed_type
        results.append(DivergenceResult(
            packet_id=packet_id,
            filed_type=filed_type,
            judge_majority_type=majority,
            is_divergent=divergent,
        ))
    return results


def divergence_rate(results: list) -> float:
    """Fraction of DECIDABLE items (judge_majority_type is not None) that
    are divergent. Returns float('nan') if there are zero decidable items
    (avoids a ZeroDivisionError silently becoming a crash deep in a
    pipeline; NaN propagates visibly instead)."""
    decidable = [r for r in results if r.judge_majority_type is not None]
    if not decidable:
        return float("nan")
    return sum(1 for r in decidable if r.is_divergent) / len(decidable)


def confusion_matrix(results: list) -> dict:
    """{(filed_type, judge_majority_type): count} over decidable items only
    (judge_majority_type is not None) -- same discordant-item exclusion as
    `divergence_rate`, for the same reason (a discordant panel has no
    "judge type" to tabulate)."""
    counts = Counter(
        (r.filed_type, r.judge_majority_type)
        for r in results
        if r.judge_majority_type is not None
    )
    return dict(counts)


# ---------------------------------------------------------------------------
# M2 — odds ratio of refutation, divergent vs concordant, + Wald CI
# ---------------------------------------------------------------------------

_Z_95 = 1.959963984540054  # scipy.stats.norm.ppf(0.975), hardcoded (stdlib
# math has no inverse-normal-CDF; this is the standard two-sided 95% Wald
# critical value, the same constant every textbook OR-CI formula uses)


@dataclass
class OddsRatioResult:
    a: int  # divergent AND refuted
    b: int  # divergent AND not-refuted
    c: int  # concordant AND refuted
    d: int  # concordant AND not-refuted
    odds_ratio: float
    log_or: float
    ci_low: float
    ci_high: float
    zero_cell_corrected: bool  # True if Haldane-Anscombe +0.5 was applied


def odds_ratio_ci(a: int, b: int, c: int, d: int, z: float = _Z_95) -> OddsRatioResult:
    """Odds ratio (a*d)/(b*c) + Wald log-OR confidence interval, with the
    Haldane-Anscombe correction (+0.5 to all four cells) applied WHENEVER
    any cell is zero -- the standard fix for the otherwise-undefined
    OR/log(0) that a single empty cell produces, applied uniformly (not
    only to the zero cell) per the correction's own textbook definition.

    Raises ValueError if a+b+c+d == 0 (no data at all -- distinct from "one
    cell is zero," which the correction handles; zero TOTAL data has no
    meaningful OR to correct toward).
    """
    if a + b + c + d == 0:
        raise ValueError("odds_ratio_ci: all four cells are zero -- no data to compute an OR from.")

    corrected = any(cell == 0 for cell in (a, b, c, d))
    if corrected:
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5

    or_val = (a * d) / (b * c)
    log_or = math.log(or_val)
    se_log_or = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    ci_low = math.exp(log_or - z * se_log_or)
    ci_high = math.exp(log_or + z * se_log_or)

    return OddsRatioResult(
        a=a, b=b, c=c, d=d,
        odds_ratio=or_val, log_or=log_or,
        ci_low=ci_low, ci_high=ci_high,
        zero_cell_corrected=corrected,
    )


def build_2x2_from_divergence(results: list, refuted_packet_ids: set) -> tuple:
    """Build the M2 2x2 table (a, b, c, d) from `compute_divergence`'s
    output + the set of packet_ids whose outcome stratum is "refuted".
    Excludes discordant items (judge_majority_type is None) from the
    table entirely -- see `divergence_rate`'s docstring for why.
    """
    a = b = c = d = 0
    for r in results:
        if r.judge_majority_type is None:
            continue
        refuted = r.packet_id in refuted_packet_ids
        if r.is_divergent:
            if refuted:
                a += 1
            else:
                b += 1
        else:
            if refuted:
                c += 1
            else:
                d += 1
    return a, b, c, d


# ---------------------------------------------------------------------------
# M4 — per-graph ORs + pooled (fixed-effect and random-effects) OR
# ---------------------------------------------------------------------------


@dataclass
class PooledOddsRatioResult:
    per_graph: dict  # graph_id -> OddsRatioResult
    fixed_effect_or: float
    fixed_effect_ci_low: float
    fixed_effect_ci_high: float
    random_effects_or: float
    random_effects_ci_low: float
    random_effects_ci_high: float
    tau_squared: float  # between-graph heterogeneity variance (DerSimonian-Laird)
    q_statistic: float  # Cochran's Q (heterogeneity test statistic)


def pooled_odds_ratio(per_graph_2x2: dict, z: float = _Z_95) -> PooledOddsRatioResult:
    """Inverse-variance-weighted fixed-effect pooling, plus
    DerSimonian-Laird random-effects pooling (the standard two-estimator
    pair reported together so a reader can see how much the pooled
    estimate depends on the homogeneity assumption).

    per_graph_2x2: {graph_id: (a, b, c, d)}. Each graph's own OR+CI is
    computed via `odds_ratio_ci` (with its own zero-cell correction,
    independent per graph). Requires at least 2 graphs (pre-reg §4:
    "Population = multi-graph, REQUIRED not optional") -- raises
    ValueError with 0 or 1 graph, since a "pooled" estimate over a single
    study is a category error, not just an edge case to silently degrade.
    """
    if len(per_graph_2x2) < 2:
        raise ValueError(
            f"pooled_odds_ratio requires >=2 graphs (pre-reg §4's multi-graph "
            f"requirement) -- got {len(per_graph_2x2)}."
        )

    per_graph: dict = {}
    log_ors: list = []
    variances: list = []
    for graph_id, (a, b, c, d) in per_graph_2x2.items():
        result = odds_ratio_ci(a, b, c, d, z=z)
        per_graph[graph_id] = result
        log_ors.append(result.log_or)
        # variance of log-OR = sum of 1/cell (same corrected cells the
        # per-graph result already applied) -- reuse the corrected a/b/c/d
        # stored on the result object, not the caller's raw (possibly
        # zero-containing) inputs, so the variance is internally consistent
        # with the log_or it's paired with.
        variances.append(1 / result.a + 1 / result.b + 1 / result.c + 1 / result.d)

    weights_fixed = [1 / v for v in variances]
    sum_w_fixed = sum(weights_fixed)
    pooled_log_or_fixed = sum(w * lo for w, lo in zip(weights_fixed, log_ors)) / sum_w_fixed
    se_pooled_fixed = math.sqrt(1 / sum_w_fixed)

    # Cochran's Q (heterogeneity statistic), computed against the FIXED
    # pooled estimate (the standard DerSimonian-Laird recipe).
    q_statistic = sum(w * (lo - pooled_log_or_fixed) ** 2 for w, lo in zip(weights_fixed, log_ors))
    k = len(log_ors)
    df = k - 1
    sum_w = sum(weights_fixed)
    sum_w_sq = sum(w * w for w in weights_fixed)
    denom = sum_w - (sum_w_sq / sum_w)
    # tau^2 clamped at 0 (DerSimonian-Laird's own convention -- a Q below
    # its expected value under homogeneity yields a negative raw estimate,
    # which has no meaningful interpretation as a variance).
    tau_squared = max(0.0, (q_statistic - df) / denom) if denom > 0 else 0.0

    weights_re = [1 / (v + tau_squared) for v in variances]
    sum_w_re = sum(weights_re)
    pooled_log_or_re = sum(w * lo for w, lo in zip(weights_re, log_ors)) / sum_w_re
    se_pooled_re = math.sqrt(1 / sum_w_re)

    return PooledOddsRatioResult(
        per_graph=per_graph,
        fixed_effect_or=math.exp(pooled_log_or_fixed),
        fixed_effect_ci_low=math.exp(pooled_log_or_fixed - z * se_pooled_fixed),
        fixed_effect_ci_high=math.exp(pooled_log_or_fixed + z * se_pooled_fixed),
        random_effects_or=math.exp(pooled_log_or_re),
        random_effects_ci_low=math.exp(pooled_log_or_re - z * se_pooled_re),
        random_effects_ci_high=math.exp(pooled_log_or_re + z * se_pooled_re),
        tau_squared=tau_squared,
        q_statistic=q_statistic,
    )


# ---------------------------------------------------------------------------
# M5 — recovery rate vs chance (positive-control instrument check, §5)
# ---------------------------------------------------------------------------


@dataclass
class RecoveryRateResult:
    n_items: int
    n_recovered: int  # judge's assigned_type == ground_truth_type
    recovery_rate: float
    chance_rate: float  # 1 / n_candidate_types
    z_statistic: float
    p_value: float  # one-sided (pre-committed direction: recovery > chance)


def _normal_cdf(x: float) -> float:
    """Standard normal CDF via `math.erf` -- stdlib-only, no scipy
    dependency (same discipline as the rest of this module)."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def recovery_rate_vs_chance(
    m5_results: list,  # list of (judge_assigned_type, ground_truth_type) tuples
    n_candidate_types: int,
) -> RecoveryRateResult:
    """One-sample proportion z-test: does the panel recover the agent's own
    post-correction reasoning_type at a rate exceeding chance
    (1/n_candidate_types)? Pre-committed direction (pre-reg §5): recovery
    rate > chance, one-sided p-value.

    Raises ValueError on an empty `m5_results` list -- an M5 gate computed
    from zero items is not a null result, it's a missing-pool error (the
    excluded_type mining found nothing, which itself needs surfacing
    loudly, not a silent NaN p-value).
    """
    if not m5_results:
        raise ValueError(
            "recovery_rate_vs_chance: m5_results is empty -- the M5 pool "
            "mining found no type-correction cases. Surface this loudly; "
            "do not silently report a vacuous recovery rate."
        )

    n = len(m5_results)
    n_recovered = sum(1 for judge_type, truth_type in m5_results if judge_type == truth_type)
    observed_rate = n_recovered / n
    chance = 1 / n_candidate_types

    se = math.sqrt(chance * (1 - chance) / n)
    z = (observed_rate - chance) / se if se > 0 else float("inf")
    p_value = 1 - _normal_cdf(z)  # one-sided: P(rate > chance)

    return RecoveryRateResult(
        n_items=n,
        n_recovered=n_recovered,
        recovery_rate=observed_rate,
        chance_rate=chance,
        z_statistic=z,
        p_value=p_value,
    )
