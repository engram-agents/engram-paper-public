"""Panel orchestration + Fleiss' kappa instrument-validity gate — pre-reg §3.

Design choice (flagging per the build-pair-loop discipline, ax_0010): the
pre-reg names both "Fleiss kappa >= 0.60 across the panel" (>=3 judges) and
"two independent passes for inter-rater" as requirements, without fully
spelling out how the two combine. This module treats each (panel_member,
pass) pair as one independent rater for the Fleiss kappa computation — e.g.
a 3-member panel run for 2 passes yields 6 raters per item, which is a
standard way to stabilize a kappa estimate with a small panel and gives
each pass equal statistical weight. Per-rater per-pass results stay fully
tagged (lineage, model, pass_index) in the raw JudgeResult records, so an
analyst can also compute a narrower per-judge test-retest agreement
separately if that turns out to be the intended reading instead. Flag to
Borges/Kepler if this operationalization isn't what was intended — cheap to
change since the raw per-(rater,pass) data is preserved either way.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .dispatch import DispatchError, JudgeResult, PanelMember, dispatch_one


@dataclass
class ItemVerdict:
    packet_id: str
    votes: list  # list of assigned_type strings (None entries excluded), one per (rater, pass)
    n_expected_ratings: int  # panel_size * n_passes
    n_parse_failures: int
    majority_type: str | None
    is_concordant: bool  # majority_type reaches a strict majority of *valid* votes
    vote_counts: dict


def run_panel(
    panel: list,
    frame_items: list,
    n_passes: int = 2,
) -> list:
    """Dispatch every frame item to every panel member, for n_passes
    independent passes each. Returns a flat list of JudgeResult — one per
    (frame_item, panel_member, pass_index). A transport failure (DispatchError)
    on one call does not abort the run; it's recorded as a JudgeResult with
    assigned_type=None and parse_error set, so one dead judge/network blip
    doesn't lose the rest of the batch.
    """
    results = []
    for item in frame_items:
        for member in panel:
            for pass_index in range(n_passes):
                try:
                    results.append(dispatch_one(member, item, pass_index))
                except DispatchError as e:
                    results.append(JudgeResult(
                        packet_id=item.get("id", ""),
                        pass_index=pass_index,
                        lineage=member.lineage,
                        model=member.model,
                        assigned_type=None,
                        justification="",
                        raw_response="",
                        parse_error=f"dispatch failed: {e}",
                    ))
    return results


def summarize_item(packet_id: str, results_for_item: list, n_expected_ratings: int) -> ItemVerdict:
    """Reduce all (rater, pass) JudgeResults for ONE item into a verdict:
    majority type + whether that majority is a true majority (> half of
    valid votes) or just a plurality (panel is discordant — pre-reg §3
    'ambiguous' bucket, not eligible to score agent-divergence).
    """
    votes = [r.assigned_type for r in results_for_item if r.assigned_type is not None]
    n_parse_failures = sum(1 for r in results_for_item if r.assigned_type is None)
    vote_counts = dict(Counter(votes))

    if not votes:
        return ItemVerdict(
            packet_id=packet_id, votes=votes, n_expected_ratings=n_expected_ratings,
            n_parse_failures=n_parse_failures, majority_type=None, is_concordant=False,
            vote_counts=vote_counts,
        )

    top_type, top_count = Counter(votes).most_common(1)[0]
    is_concordant = top_count > len(votes) / 2  # strict majority, not plurality
    return ItemVerdict(
        packet_id=packet_id, votes=votes, n_expected_ratings=n_expected_ratings,
        n_parse_failures=n_parse_failures,
        majority_type=top_type if is_concordant else None,
        is_concordant=is_concordant, vote_counts=vote_counts,
    )


def summarize_all(all_results: list, n_expected_ratings: int) -> dict:
    """Group flat JudgeResults by packet_id and summarize each. Returns
    {packet_id: ItemVerdict}."""
    by_item: dict = {}
    for r in all_results:
        by_item.setdefault(r.packet_id, []).append(r)
    return {
        pid: summarize_item(pid, results, n_expected_ratings)
        for pid, results in by_item.items()
    }


def fleiss_kappa(ratings_by_item: dict, categories) -> float:
    """Standard Fleiss' kappa (Fleiss 1971) over N items x k categories.

    ratings_by_item: {item_id: [category_label, ...]} — one entry per
    (rater, pass) valid vote for that item. Every item MUST have the same
    number of raters (n) — Fleiss' kappa is undefined for a ragged rater
    count; items with a different vote count than the modal count are
    dropped from the kappa computation (with a warning-worthy count
    returned separately by the caller if desired — this function itself
    just computes on whatever's passed in, so filter to a consistent n
    before calling if your data has ragged counts from parse failures).
    categories: the fixed list of possible category labels (the 7
    quote_type names) — needed even for categories that got zero votes,
    since Fleiss' kappa's chance-agreement term depends on each category's
    overall marginal proportion across the whole sample.

    Returns NaN (float('nan')) if there are fewer than 2 items or fewer
    than 2 raters per item (kappa is undefined in those degenerate cases) —
    callers must check for NaN before treating this as a real gate value.
    """
    items = list(ratings_by_item.items())
    if len(items) < 2:
        return float("nan")

    n_raters_per_item = {len(v) for _, v in items}
    if len(n_raters_per_item) != 1:
        raise ValueError(
            f"fleiss_kappa requires every item to have the SAME rater count; "
            f"got counts {sorted(n_raters_per_item)}. Filter to a consistent "
            f"n before calling (e.g. drop items where parse failures made the "
            f"valid-vote count ragged)."
        )
    n = n_raters_per_item.pop()
    if n < 2:
        return float("nan")

    N = len(items)
    k = len(categories)
    cat_index = {c: i for i, c in enumerate(categories)}

    # n_ij: count of raters assigning category j to item i.
    counts_matrix = []
    for _, votes in items:
        row = [0] * k
        for v in votes:
            if v not in cat_index:
                raise ValueError(f"vote {v!r} is not in the provided categories list {categories}")
            row[cat_index[v]] += 1
        counts_matrix.append(row)

    # p_j: overall proportion of all assignments that were category j.
    total_assignments = N * n
    p_j = [sum(row[j] for row in counts_matrix) / total_assignments for j in range(k)]

    # P_i: per-item agreement — extent to which raters agree on item i.
    P_i = []
    for row in counts_matrix:
        agreement = sum(nij * (nij - 1) for nij in row)
        P_i.append(agreement / (n * (n - 1)))

    P_bar = sum(P_i) / N          # mean observed agreement
    P_e_bar = sum(p * p for p in p_j)  # expected agreement by chance

    if P_e_bar == 1.0:
        # Every rating fell in one category — no variance to explain;
        # kappa's denominator (1 - P_e_bar) is zero. Perfect agreement
        # trivially, not a meaningful reliability estimate either way.
        return float("nan")

    return (P_bar - P_e_bar) / (1 - P_e_bar)


KAPPA_INSTRUMENT_VALIDITY_FLOOR = 0.60  # pre-reg §3, committed pre-data


def instrument_validity_gate(kappa: float) -> bool:
    """True iff the panel clears the pre-registered Fleiss kappa floor.
    NaN (undefined kappa — too few items/raters) always fails the gate;
    an undefined instrument-validity measurement cannot pass a validity gate.
    """
    if kappa != kappa:  # NaN check without importing math, for a one-line gate
        return False
    return kappa >= KAPPA_INSTRUMENT_VALIDITY_FLOOR
