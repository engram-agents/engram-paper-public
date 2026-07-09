"""Tests for tools/compression_fidelity/binning.py -- pre-reg §5's second
stratification axis (confidence-bin for observations, reasoning_type for
derivations)."""

from tools.compression_fidelity.binning import (
    bin_key,
    derivation_reasoning_bin,
    observation_confidence_bin,
)
from tools.compression_fidelity.db import NodeRow


def _obs(confidence):
    return NodeRow(
        id="ob_1", type="observation_factual", claim="c", quoted_text="q",
        interpretation="i", quote_type="hard_data", evidence_id=None,
        logical_chain=None, confidence=confidence, metadata={},
    )


def _deriv(reasoning_type=None):
    meta = {"reasoning_type": reasoning_type} if reasoning_type else {}
    return NodeRow(
        id="dv_1", type="derivation", claim="c", quoted_text=None,
        interpretation="i", quote_type=None, evidence_id=None,
        logical_chain="chain", confidence=0.8, metadata=meta,
    )


# ── observation_confidence_bin ───────────────────────────────────────────


def test_bins_to_exact_anchor_match():
    assert observation_confidence_bin(_obs(0.95)) == 0.95
    assert observation_confidence_bin(_obs(0.35)) == 0.35


def test_bins_to_nearest_anchor():
    assert observation_confidence_bin(_obs(0.72)) == 0.70


def test_tie_breaks_to_the_first_anchor_in_declared_order():
    """0.60 is equidistant from 0.70 and 0.50 (both anchors 0.10 away).
    Python's min(key=...) returns the FIRST minimal element in iteration
    order, and OBSERVATION_CONFIDENCE_ANCHORS = (0.95, 0.85, 0.70, 0.50,
    0.40, 0.35) lists 0.70 before 0.50 -- verified directly against the
    real anchors tuple before writing this assertion."""
    assert observation_confidence_bin(_obs(0.60)) == 0.70


def test_none_confidence_returns_none():
    assert observation_confidence_bin(_obs(None)) is None


# ── derivation_reasoning_bin ──────────────────────────────────────────────


def test_returns_reasoning_type_when_set():
    assert derivation_reasoning_bin(_deriv("inductive_causal")) == "inductive_causal"


def test_returns_unknown_when_absent():
    assert derivation_reasoning_bin(_deriv(None)) == "UNKNOWN"


# ── bin_key ────────────────────────────────────────────────────────────────


def test_bin_key_derivation_returns_raw_reasoning_type_string():
    assert bin_key(_deriv("abductive_best_explanation")) == "abductive_best_explanation"


def test_bin_key_observation_formats_as_two_decimal_string():
    assert bin_key(_obs(0.70)) == "0.70"


def test_bin_key_observation_none_confidence_is_unknown_string():
    """Distinct from observation_confidence_bin's raw `None` return --
    bin_key's ternary converts that to the literal string 'UNKNOWN' so it
    behaves consistently as a stratification-cell key alongside
    derivation_reasoning_bin's 'UNKNOWN'."""
    assert bin_key(_obs(None)) == "UNKNOWN"
