"""Tests for derivation_type_definitions.py -- the confidence-redaction
discipline is the load-bearing safety property of this module (see its own
module docstring for the design discussion this encodes)."""

import random
import re

from tools.type_reclassification.derivation_type_definitions import (
    REASONING_TYPES,
    VERBATIM_REASONING_TYPE_SCHEMA_TEXT,
    order_randomized,
)

_NUMBER_PATTERN = re.compile(r"(?<![0-9.])[01]?\.\d+(?![0-9.])")


def test_no_confidence_numbers_leak():
    assert not _NUMBER_PATTERN.search(VERBATIM_REASONING_TYPE_SCHEMA_TEXT)


def test_no_hierarchy_confidence_words_leak():
    """The widened redaction target Borges asked for: numbers AND the
    mechanism/hierarchy words that rank types by confidence-derivation."""
    text_lower = VERBATIM_REASONING_TYPE_SCHEMA_TEXT.lower()
    for banned in ("discount", "cap ", "capped", "weakest legitimate form"):
        assert banned not in text_lower, f"{banned!r} leaked into the schema text"


def test_semantic_requirement_phrases_survive():
    """The inference-form semantics Borges named as the must-keep KEEP
    examples must still be present -- this is not a blanket strip."""
    for keep_phrase in (
        "corroborative, multi-source",
        "truth-preserving",
        "evidence strengthens but never proves",
        "best explanation, alternatives may exist",
        "trust transfer",
    ):
        assert keep_phrase in VERBATIM_REASONING_TYPE_SCHEMA_TEXT


def test_all_reasoning_type_names_present_in_schema_text():
    for t in REASONING_TYPES:
        assert t in VERBATIM_REASONING_TYPE_SCHEMA_TEXT


def test_reasoning_types_count_matches_production_enum():
    """Sanity floor against future drift: engram-alpha's REASONING_TYPES
    set (engram_confidence.py) has 14 members as of this module's
    authoring (2026-07-08) -- if that enum grows/shrinks, this module's
    hand-vendored tuple needs a matching update, and this test is the
    tripwire (not an automated cross-repo check, same vendoring caveat as
    compression_fidelity/constants.py)."""
    assert len(REASONING_TYPES) == 14
    assert len(set(REASONING_TYPES)) == 14  # no duplicates


def test_order_randomized_is_deterministic_per_seed():
    a = order_randomized(random.Random(42))
    b = order_randomized(random.Random(42))
    assert a == b
    assert set(a) == set(REASONING_TYPES)


def test_order_randomized_differs_across_seeds():
    a = order_randomized(random.Random(1))
    b = order_randomized(random.Random(2))
    assert a != b
