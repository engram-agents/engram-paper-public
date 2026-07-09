"""Tests for the derivation-arm (reasoning_type) judge prompt — mirrors the
`# ── judge_prompt ──` section of `tests/type_reclassification/
test_judge_dispatch.py` (the observation-arm equivalent), against
FakeJudgeClient-free pure prompt-construction (no dispatch needed here)."""

import random

from tools.type_reclassification.derivation_judge_prompt import (
    build_prompt,
    rng_for_item,
    valid_type_names,
)


def _clean_frame_item(
    claim="Therefore all observed swans are white.",
    premises=None,
):
    if premises is None:
        premises = [
            {"claim": "Swan #1 observed at the lake was white.", "type": "hard_data"},
            {"claim": "Swan #2 observed at the lake was white.", "type": "hard_data"},
        ]
    return {
        "id": "dv_0001",
        "claim": claim,
        "premises": premises,
        "stratum": {"outcome": "survived", "fs_class": "frozen"},
    }


# ── derivation_judge_prompt ────────────────────────────────────────────────


def test_build_prompt_contains_claim_premises_and_all_type_names():
    item = _clean_frame_item()
    system_prompt, user_prompt = build_prompt(item, random.Random(0))
    assert "do not use any tool" in system_prompt.lower()
    assert item["claim"] in user_prompt
    for premise in item["premises"]:
        assert premise["claim"] in user_prompt
    for t in valid_type_names():
        assert t in user_prompt
    # Confidence VALUE / node id must never appear in the rendered prompt.
    assert "confidence" not in user_prompt.lower()
    assert item["id"] not in user_prompt
    # Reviewer-fairy suggestion: the bare field name "reasoning_type" (the
    # withheld field this whole arm exists to classify) must never appear
    # literally -- only the TYPE NAMES themselves (already asserted above)
    # should be visible, never the field-name word.
    assert "reasoning_type" not in user_prompt.lower()


def test_build_prompt_never_renders_stratum():
    """Mirrors the observation-arm's equivalent invariant test: even when
    stratum carries the outcome (which frame_export.py must never let reach
    a real judge, but this test isn't relying on frame_export's own
    discipline -- it directly probes build_prompt), no stratum content
    leaks into the rendered prompt."""
    item = _clean_frame_item()
    item["stratum"] = {"outcome": "survived", "fs_class": "frozen"}
    _, user_prompt = build_prompt(item, random.Random(0))
    assert "stratum" not in user_prompt.lower()
    assert "survived" not in user_prompt.lower()
    assert "fs_class" not in user_prompt.lower()


def test_build_prompt_never_leaks_extra_premise_fields():
    item = _clean_frame_item()
    item["premises"][0]["interpretation"] = "the agent's own reach-justification, must not leak"
    item["premises"][0]["confidence"] = 0.95
    _, user_prompt = build_prompt(item, random.Random(0))
    # build_prompt only renders the 2 dose fields it explicitly knows about
    # per premise (claim/type) -- confirm a caller-mistake extra field does
    # NOT get rendered just by being present in the premise dict (defense
    # in depth on top of frame_export's own withholding responsibility).
    assert "reach-justification" not in user_prompt
    assert "0.95" not in user_prompt


def test_premise_with_none_type_never_renders_literal_none():
    """This arm's dose includes premise `type` fields (unlike the
    observation arm), so a premise with type: None must be rendered WITHOUT
    a type annotation at all -- never the literal string "None", which
    would look like a leaked null/error to the judge rather than
    intentional withholding of a field that genuinely doesn't exist for
    that premise (e.g. an axiom cited as a premise)."""
    item = _clean_frame_item(
        premises=[
            {"claim": "An axiom cited as a premise.", "type": None},
            {"claim": "An observed fact.", "type": "hard_data"},
        ]
    )
    _, user_prompt = build_prompt(item, random.Random(0))
    assert "None" not in user_prompt
    assert "an axiom cited as a premise" in user_prompt.lower()
    assert "an observed fact" in user_prompt.lower()


def test_two_passes_use_different_type_order():
    """Mirrors the observation arm's equivalent test. NOTE: only the TYPE
    list is order-randomized per pass (mirroring `order_randomized`'s
    contract exactly) -- premise order is NOT independently randomized here.
    db.py's `fetch_derivation_premises` docstring is explicit that premise
    order carries no study meaning and is stabilized (sorted by id) purely
    for deterministic fixture comparisons, not because the pre-reg treats
    order as a presentation variable worth per-pass reshuffling the way
    type order is. So this test (like the observation arm's) only exercises
    type-order variation across passes."""
    item = _clean_frame_item()
    rng_pass0 = rng_for_item(item, pass_index=0)
    rng_pass1 = rng_for_item(item, pass_index=1)
    _, prompt0 = build_prompt(item, rng_pass0)
    _, prompt1 = build_prompt(item, rng_pass1)
    assert prompt0 != prompt1  # different order-randomization seed per pass


def test_same_pass_index_is_deterministic():
    item = _clean_frame_item()
    _, prompt_a = build_prompt(item, rng_for_item(item, pass_index=0))
    _, prompt_b = build_prompt(item, rng_for_item(item, pass_index=0))
    assert prompt_a == prompt_b
