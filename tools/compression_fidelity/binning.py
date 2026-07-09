"""Confidence-bin / reasoning_type binning (pre-reg §5, stratification axis 2).

Observations bin to the NEAREST of the 6 named confidence anchors, using
the node's actual COMPUTED confidence (not its raw `quote_type`) — this
correctly buckets `user_stated`-overridden and `introspective`-discounted
observations by what they actually compute to, not by their nominal
quote_type (e.g. a `personal_communication` observation with
`source_class=user_stated` computes to 0.85, the official_statement
anchor, and bins there — confirmed against the smoke-test graph, where
several such nodes exist).

Derivations bin by their `reasoning_type` directly (read from `metadata`)
— "which IS their confidence map, don't also bin derivations by raw
score" (spec).
"""

from __future__ import annotations

from typing import Optional

from . import db
from .constants import DERIVATION_TYPES, OBSERVATION_CONFIDENCE_ANCHORS


def observation_confidence_bin(node: db.NodeRow) -> Optional[float]:
    if node.confidence is None:
        return None
    return min(OBSERVATION_CONFIDENCE_ANCHORS, key=lambda a: abs(a - node.confidence))


def derivation_reasoning_bin(node: db.NodeRow) -> str:
    return node.reasoning_type or "UNKNOWN"


def bin_key(node: db.NodeRow) -> str:
    """The stratification sub-key (confidence-bin for observations,
    reasoning_type for derivations) rendered as a stable string."""
    if node.type in DERIVATION_TYPES:
        return derivation_reasoning_bin(node)
    b = observation_confidence_bin(node)
    return f"{b:.2f}" if b is not None else "UNKNOWN"
