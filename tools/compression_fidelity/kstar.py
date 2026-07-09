"""K* computation (pre-reg §8.0 / §PIN v5-A, v6-A).

K* = the BIC-optimal K over K in [2,6] on the pooled FROZEN SAMPLE's
computed confidence values, via an exact deterministic 1-D clustering
method (the pre-reg pins `Ckmeans.1d.dp` — optimal 1-D k-means via dynamic
programming — as the reference algorithm, explicitly rejecting any
random-restart method since reproducibility without a seed is required).

**Package choice: `ckwrap` (wraps the actual R `Ckmeans.1d.dp`
implementation).** Two maintained candidates were checked on PyPI
(per Borges's leads):

    - `kmeans1d` — exact 1-D k-means via DP, C++ core, deterministic. Does
      NOT expose a built-in BIC K-selection — it clusters at a single,
      caller-supplied K only. Using it would mean hand-rolling the BIC
      comparison across K=2..6 as separate code, outside the "one audited
      code path" the pre-reg's §PIN v6-A wants for the K*-determination +
      clustering.
    - `ckwrap` — a Python wrapper around the actual R `Ckmeans.1d.dp`
      package (the literal pinned reference algorithm, not just an
      equivalent DP formulation). `ckwrap.ckmeans(x, k=(2, 6))` clusters
      AND selects the BIC-optimal K in one call when `k` is passed as a
      range — this is the "SAME algorithm's built-in ... BIC selection"
      the pre-reg asks for, in a single audited call.

`ckwrap` is used here. Exact package + version must still be pinned by
Borges/Kepler at freeze per the pre-reg (§8.0: "with the exact package +
version recorded at freeze") — this run recorded ckwrap==1.2.3 (see
requirements.txt). No random-restart method is used anywhere; the DP
method is deterministic given the input scores (order-independent), so no
seed is needed for this step.

**Degenerate-distribution rule (pre-reg §8.0):** if the sample has fewer
than K* distinct confidence values, K* is reduced to the distinct count
and the reduction is reported. `ckwrap.ckmeans` also hard-errors if
`max(k) >= n_distinct` ("Max 'k' must be smaller than the number of unique
'x' values") — this module pre-clamps the K-range's upper bound to
`min(6, n_distinct - 1)` before calling ckwrap, and separately reports the
degenerate-distribution reduction whenever the graph's real spread is
narrower than the requested [2,6] range, so the two concerns (ckwrap's
hard input constraint, and the pre-reg's degenerate-distribution rule) are
handled by one code path rather than two.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

try:
    import ckwrap
except ImportError as e:  # pragma: no cover - environment guard
    raise ImportError(
        "K* computation requires the 'ckwrap' package (pip install ckwrap). "
        "See kstar.py module docstring for why this package was chosen over "
        "the alternative (kmeans1d)."
    ) from e


@dataclass
class KStarResult:
    k_star: int
    k_requested_max: int  # the upper bound actually passed to ckwrap (post-clamp)
    degenerate_reduced: bool
    n_distinct_values: int
    n_samples: int
    centroids: list[float]  # ordered ascending, tier 1..K*
    tier_assignments: dict[str, int]  # node_id -> tier (1-indexed, ordered by centroid)
    bic: Optional[float] = None


def _extract_bic(result, k_star: int, k_min: int) -> Optional[float]:
    """`ckwrap`'s `result.BIC` is an array of BIC values, one per candidate K
    in the requested range (not a single scalar) — index it at the winning
    K's position. Falls back to None if the shape is unexpected (e.g. a
    single-K call, where ckwrap may not populate a comparison array)."""
    bic = getattr(result, "BIC", None)
    if bic is None:
        return None
    arr = np.atleast_1d(np.asarray(bic))
    idx = k_star - k_min
    if 0 <= idx < arr.size:
        return float(arr[idx])
    if arr.size == 1:
        return float(arr[0])
    return None


def compute_k_star(
    node_ids: list[str],
    scores: list[float],
    k_min: int = 2,
    k_max: int = 6,
) -> KStarResult:
    if len(node_ids) != len(scores):
        raise ValueError("node_ids and scores must be the same length")
    if not scores:
        raise ValueError("cannot compute K* on an empty sample")

    x = np.array(scores, dtype=float)
    n_distinct = len(set(round(s, 6) for s in scores))

    degenerate_reduced = False
    if n_distinct <= 1:
        # Cannot cluster at all — every sampled node in one tier.
        return KStarResult(
            k_star=max(n_distinct, 1),
            k_requested_max=k_max,
            degenerate_reduced=True,
            n_distinct_values=n_distinct,
            n_samples=len(scores),
            centroids=[float(x[0])] if n_distinct == 1 else [],
            tier_assignments={nid: 1 for nid in node_ids},
            bic=None,
        )

    effective_k_max = min(k_max, n_distinct - 1)
    degenerate_reduced = effective_k_max < k_max
    if effective_k_max < k_min:
        # Fewer distinct values than k_min allows a range at all — reduce
        # K* straight to the distinct count (pre-reg's degenerate rule).
        k_star = n_distinct
        result = ckwrap.ckmeans(x, k_star)
        centroids = sorted(float(c) for c in result.centers)
        order = np.argsort(result.centers)
        rank_of = {int(orig): rank + 1 for rank, orig in enumerate(order)}
        tiers = {nid: rank_of[int(lbl)] for nid, lbl in zip(node_ids, result.labels)}
        return KStarResult(
            k_star=k_star,
            k_requested_max=k_max,
            degenerate_reduced=True,
            n_distinct_values=n_distinct,
            n_samples=len(scores),
            centroids=centroids,
            tier_assignments=tiers,
            bic=_extract_bic(result, k_star=k_star, k_min=k_star),
        )

    result = ckwrap.ckmeans(x, (k_min, effective_k_max))
    k_star = int(result.k)
    if k_star > n_distinct:  # guard; should not trigger given the clamp above
        k_star = n_distinct
        degenerate_reduced = True

    order = np.argsort(result.centers)
    rank_of = {int(orig): rank + 1 for rank, orig in enumerate(order)}
    tiers = {nid: rank_of[int(lbl)] for nid, lbl in zip(node_ids, result.labels)}
    centroids = sorted(float(c) for c in result.centers)

    return KStarResult(
        k_star=k_star,
        k_requested_max=k_max,
        degenerate_reduced=degenerate_reduced,
        n_distinct_values=n_distinct,
        n_samples=len(scores),
        centroids=centroids,
        tier_assignments=tiers,
        bic=_extract_bic(result, k_star=k_star, k_min=k_min),
    )
