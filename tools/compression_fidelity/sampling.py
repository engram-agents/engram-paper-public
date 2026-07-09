"""Stratified sampling (pre-reg §5).

Three stratification axes: node-type x confidence-bin/reasoning_type x
logic-depth-tier. In practice the axes are NOT a free cross-product —
observations are always depth-tier 1 (no premises -> depth 1, by
definition), and derivations are always depth-tier 2 or ">=3" (a
derivation always has >=1 premise, so its depth is always >= 2). The
frame is therefore naturally partitioned into three disjoint slabs:

    (observation, tier 1)   — sub-stratified by confidence-bin
    (derivation,  tier 2)   — sub-stratified by reasoning_type
    (derivation,  tier >=3) — the OVERSAMPLED deep tier (its own rule)

**Judgment call — the "N ~ 250 / ~35-40 per major cell" arithmetic (flagged
prominently in the handoff; this is the single largest open interpretation
in this module).** The pre-reg leaves the exact relationship between the
overall N~250 target and the finest stratification cell's ~35-40 target
underspecified for a graph with many populated bins/reasoning_types (a
literal per-finest-cell target of 35-40 summed across e.g. 6 observation
confidence bins ALONE already approaches 250, before any derivation cells
are counted). This module resolves it as follows, and the choice should be
confirmed by Borges/Kepler before the real run against Borges's graph:

    - the deep tier (derivation, >=3) is handled FIRST and separately, per
      its own explicit rule: take all if frame count <= 40, else a seeded
      random sample of 40 (regardless of reasoning_type sub-composition —
      the spec's oversampling rule is stated at the tier level, not
      sub-stratified further for the actual draw).
    - the two remaining slabs -- (observation, 1) and (derivation, 2) --
      are each sub-stratified at their FINEST populated cell (confidence-
      bin for observations, reasoning_type for derivations), targeting
      PER_CELL_TARGET (38, the midpoint of "35-40") nodes per cell, capped
      by availability ("where the frame supports it"). No cross-slab
      budget reallocation is performed — this is a straightforward
      per-cell cap, not a fixed total-N allocator, so the realized total
      is whatever the graph's actual bin population yields near, not a
      hard 250. On the local smoke-test graph this produces ~281, ~12%
      over the informal N~250 anchor — close enough to validate this
      reading, but not proof it is the pre-reg authors' intended
      arithmetic for Borges's graph (which will have a different bin
      population).

All random sub-sampling uses a single seeded `random.Random(seed)` instance
(recorded in the manifest) — no unseeded/random-restart method anywhere in
this module (reproducibility is a pinned requirement, pre-reg §5/§PIN
v5-A).
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

from . import binning, db, depth as depthmod
from .constants import DERIVATION_TYPES, OBSERVATION_TYPES

PER_CELL_TARGET = 38  # midpoint of the pre-reg's "~35-40 per major cell"
DEEP_TIER_CAP = 40
DEFAULT_SEED = 20260705  # pre-reg registration date, recorded in the manifest


@dataclass
class CellFrame:
    node_type: str  # "observation" | "derivation"
    depth_tier: str  # "1" | "2" | ">=3"
    subcategory: str  # confidence-bin (obs) or reasoning_type (deriv)
    node_ids: list[str] = field(default_factory=list)

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.node_type, self.depth_tier, self.subcategory)


@dataclass
class SamplingResult:
    seed: int
    sampled_ids: list[str]  # the frozen sample, deterministic order
    deep_tier_frame_count: int
    deep_tier_sampled_count: int
    deep_tier_reduced: bool  # True if frame > cap (i.e. we sub-sampled, not took-all)
    frame_cell_counts: dict[str, int]  # "type|tier|subcat" -> frame count
    sampled_cell_counts: dict[str, int]  # same key -> sampled count
    without_interpretation_ids: list[str]  # ~50% stratified subsample of sampled_ids


def _cell_key_str(node_type: str, tier: str, subcat: str) -> str:
    return f"{node_type}|{tier}|{subcat}"


def build_cells(
    frame_nodes: list[db.NodeRow], depth_map: dict[str, int]
) -> dict[tuple[str, str, str], CellFrame]:
    cells: dict[tuple[str, str, str], CellFrame] = {}
    for node in frame_nodes:
        node_type = "observation" if node.type in OBSERVATION_TYPES else "derivation"
        tier = depthmod.depth_tier(depth_map[node.id])
        subcat = binning.bin_key(node)
        key = (node_type, tier, subcat)
        if key not in cells:
            cells[key] = CellFrame(node_type, tier, subcat)
        cells[key].node_ids.append(node.id)
    return cells


def draw_stratified_sample(
    frame_nodes: list[db.NodeRow],
    depth_map: dict[str, int],
    seed: int = DEFAULT_SEED,
    per_cell_target: int = PER_CELL_TARGET,
    deep_tier_cap: int = DEEP_TIER_CAP,
) -> SamplingResult:
    rng = random.Random(seed)
    cells = build_cells(frame_nodes, depth_map)

    frame_cell_counts = {
        _cell_key_str(*key): len(cell.node_ids) for key, cell in cells.items()
    }

    sampled_ids: list[str] = []
    sampled_cell_counts: dict[str, int] = {}

    # 1. Deep tier (derivation, ">=3") — take all if <= cap, else seeded
    #    random sample of `deep_tier_cap`. Combined across all reasoning_type
    #    subcategories at this tier (the spec's rule is tier-level).
    deep_ids: list[str] = []
    for key, cell in cells.items():
        if key[0] == "derivation" and key[1] == ">=3":
            deep_ids.extend(cell.node_ids)
    deep_ids = sorted(deep_ids)  # deterministic pre-shuffle order
    deep_frame_count = len(deep_ids)
    deep_reduced = deep_frame_count > deep_tier_cap
    if deep_reduced:
        deep_sample = rng.sample(deep_ids, deep_tier_cap)
    else:
        deep_sample = list(deep_ids)
    sampled_ids.extend(deep_sample)
    # record sampled counts per (derivation, >=3, subcategory) for the
    # natural-distribution manifest, even though the draw itself wasn't
    # sub-stratified by subcategory.
    deep_sample_set = set(deep_sample)
    for key, cell in cells.items():
        if key[0] == "derivation" and key[1] == ">=3":
            sampled_cell_counts[_cell_key_str(*key)] = len(
                [n for n in cell.node_ids if n in deep_sample_set]
            )

    # 2. Remaining slabs: (observation, "1") and (derivation, "2"), each
    #    sub-stratified at the finest populated cell, target
    #    `per_cell_target`, capped by availability.
    for key, cell in cells.items():
        if key[1] == ">=3":
            continue  # handled above
        ids = sorted(cell.node_ids)
        if len(ids) <= per_cell_target:
            chosen = ids
        else:
            chosen = rng.sample(ids, per_cell_target)
        sampled_ids.extend(chosen)
        sampled_cell_counts[_cell_key_str(*key)] = len(chosen)

    sampled_ids = sorted(set(sampled_ids))  # deterministic final order

    without_interp_ids = _draw_without_interpretation_subsample(
        sampled_ids, cells, rng
    )

    return SamplingResult(
        seed=seed,
        sampled_ids=sampled_ids,
        deep_tier_frame_count=deep_frame_count,
        deep_tier_sampled_count=len(deep_sample),
        deep_tier_reduced=deep_reduced,
        frame_cell_counts=frame_cell_counts,
        sampled_cell_counts=sampled_cell_counts,
        without_interpretation_ids=without_interp_ids,
    )


def _draw_without_interpretation_subsample(
    sampled_ids: list[str],
    cells: dict[tuple[str, str, str], CellFrame],
    rng: random.Random,
) -> list[str]:
    """Pre-registered stratified 50% subsample (~125 of ~250), covering
    every populated type x confidence-bin x depth-tier cell (pre-reg §8/§5,
    the "interpretation-anchoring" sensitivity arm).

    Stratified by the same finest-cell key as the primary sample. Within
    each cell of the FROZEN SAMPLE (not the frame), take round(n/2),
    floored at 1 whenever the cell has >= 1 sampled item — so "every cell"
    means every populated cell gets at least one representative in the
    subsample, not that it's excluded for being small. (Docstring/code
    mismatch fixed per reviewer-fairy low-effort note: an earlier version
    of this docstring additionally claimed ">= 2 if the cell has >= 2",
    which `max(1, round(n/2))` does not guarantee for n=2 -- round(1.0)=1.
    The pre-reg's "covering every cell" requirement only asks for
    non-empty representation, not a specific per-cell floor beyond that,
    so the CODE's actual `max(1, round(n/2))` behavior is kept as-is and
    the docstring corrected to match it, rather than changing the sample
    composition to match the stronger claim.)"""
    sampled_set = set(sampled_ids)
    by_cell: dict[tuple[str, str, str], list[str]] = {}
    for key, cell in cells.items():
        members = sorted(n for n in cell.node_ids if n in sampled_set)
        if members:
            by_cell[key] = members

    chosen: list[str] = []
    for key, members in by_cell.items():
        n = len(members)
        target = max(1, round(n / 2)) if n >= 1 else 0
        target = min(target, n)
        chosen.extend(rng.sample(members, target))
    return sorted(set(chosen))


def assign_packet_ids(node_ids: list[str], seed: int) -> dict[str, str]:
    """Opaque, deterministic packet-ID assignment (reviewer-fairy catch
    #1, fixed).

    An earlier version of this harness used the real ENGRAM node ID as
    both the packet's `packet_id` field AND the served filename — a
    directly-observable leak that defeats the pre-reg's §3
    harness-isolation defense-in-depth (a raw node ID lets a
    partially-unisolated judge fairy call `engram_inspect(<id>)` and read
    the withheld confidence/type straight from the graph).

    This assigns a serial `pkt_NNNNN` label to each sampled node, in a
    seeded-shuffled order (not sorted node-ID order) so the packet-ID
    SEQUENCE itself doesn't correlate with sampling/cell order. Uses a
    dedicated `random.Random(seed)` instance (same seed as the sampling
    draw, but a fresh generator — this function doesn't consume or depend
    on the sampling RNG's state, so it's callable independently and
    reproducibly from just `(node_ids, seed)`).

    The returned `{node_id: packet_id}` mapping belongs ONLY in the
    researcher-side manifest — never in a served packet file. Packet files
    carry `packet_id` alone; the reverse mapping back to the real node ID
    is deliberately not derivable from a packet file itself.
    """
    ids = sorted(node_ids)  # deterministic input order before shuffling
    rng = random.Random(seed)
    rng.shuffle(ids)
    width = max(5, len(str(len(ids))))
    return {nid: f"pkt_{i + 1:0{width}d}" for i, nid in enumerate(ids)}
