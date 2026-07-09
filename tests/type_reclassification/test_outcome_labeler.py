"""Tests for the blind outcome-labeler pass (superseded-node
refuted/survivor_refined/excluded_support reclassification)."""

from tools.type_reclassification.dispatch import FakeJudgeClient, PanelMember
from tools.type_reclassification.outcome_dispatch import dispatch_outcome_one, parse_outcome_response
from tools.type_reclassification.outcome_prompt import build_prompt, valid_outcome_names
import random


def _supersede_item():
    return {
        "id": "ob_0042",
        "old_claim": "The contradiction cascade fires when a contradiction is filed.",
        "new_claim": "The contradiction cascade fires only at resolution, never at filing.",
        "supersede_reason": "the mechanism does NOT fire on contradict, only on resolve -- earlier claim was wrong",
    }


def test_build_prompt_contains_rubric_and_no_confidence_value():
    import re

    item = _supersede_item()
    system_prompt, user_prompt = build_prompt(item, random.Random(0))
    assert item["old_claim"] in user_prompt
    assert item["new_claim"] in user_prompt
    assert item["supersede_reason"] in user_prompt
    # The rubric text legitimately discusses "confidence" as a CONCEPT
    # (Borges's own pasted rubric: "the supersede changed metadata or
    # confidence, not the claim"). This item also never receives a
    # confidence field as input at all, so the actual safety property is:
    # no numeric confidence-VALUE-shaped decimal ever appears (there's
    # nothing structurally that could produce one, but assert it anyway as
    # a direct regression guard rather than relying on "no input, so no
    # output" reasoning alone).
    assert not re.search(r"0\.\d{2,3}\b", user_prompt)
    for cat in valid_outcome_names():
        assert cat in user_prompt


def test_build_prompt_redacts_confidence_value_that_leaks_via_reason_text():
    """Regression test for a reviewer-fairy-caught blocker: this module
    previously applied NO redaction at all, so a plausible supersede_reason
    like "confidence was 0.4, should be 0.85" would leak numeric confidence
    values straight into the labeler's prompt -- exactly the scenario the
    reviewer demonstrated as the concrete risk, not a hypothetical one."""
    item = {
        "id": "ob_0777",
        "old_claim": "The event occurred as described.",
        "new_claim": "The event occurred as described, evidence re-weighted.",
        "supersede_reason": "confidence was 0.40, should be 0.85 given stronger corroboration",
    }
    _, user_prompt = build_prompt(item, random.Random(0))
    assert "0.40" not in user_prompt
    assert "0.85" not in user_prompt


def test_outcome_prompt_does_not_import_judge_prompt():
    """Isolation requirement (Borges, seq 1395): the outcome-labeler must
    not share prompt content with the type-judge."""
    import tools.type_reclassification.outcome_prompt as op

    assert not hasattr(op, "SYSTEM_PROMPT") or "quote_type" not in op.SYSTEM_PROMPT.lower()
    assert "type_definitions" not in dir(op)


def test_dispatch_worked_example_refuted():
    client = FakeJudgeClient(
        default_response='{"outcome": "refuted", "justification": "old claim asserted a false mechanism"}'
    )
    member = PanelMember(client=client, model="fake-model", lineage="fake:a")
    result = dispatch_outcome_one(member, _supersede_item())
    assert result.outcome == "refuted"
    assert result.parse_error is None


def test_dispatch_worked_example_survivor_refined():
    item = {
        "id": "ob_0099",
        "old_claim": "This applies to single-agent installs.",
        "new_claim": "This applies to multi-agent installs generally.",
        "supersede_reason": "narrowed scope to multi-agent; single-agent framing imprecise but not wrong",
    }
    client = FakeJudgeClient(
        default_response='{"outcome": "survivor_refined", "justification": "narrowing of a correct claim"}'
    )
    member = PanelMember(client=client, model="fake-model", lineage="fake:a")
    result = dispatch_outcome_one(member, item)
    assert result.outcome == "survivor_refined"


def test_dispatch_worked_example_excluded_type():
    """excluded_type is the circularity guard: content fine, only the
    classification/type was wrong (Borges, seq 1398)."""
    item = {
        "id": "ob_0150",
        "old_claim": "ENGRAM's compaction hook always fires within 2 seconds.",
        "new_claim": "ENGRAM's compaction hook always fires within 2 seconds.",
        "supersede_reason": "this should have been filed as a conjecture, not an observation -- the claim itself was right",
    }
    client = FakeJudgeClient(
        default_response='{"outcome": "excluded_type", "justification": "classification was wrong, content held"}'
    )
    member = PanelMember(client=client, model="fake-model", lineage="fake:a")
    result = dispatch_outcome_one(member, item)
    assert result.outcome == "excluded_type"


def test_parse_outcome_response_rejects_invalid_category():
    outcome, justification, err = parse_outcome_response('{"outcome": "not_a_real_outcome", "justification": "x"}')
    assert outcome is None
    assert err is not None


def test_parse_outcome_response_default_excluded_support_is_a_valid_category():
    outcome, justification, err = parse_outcome_response(
        '{"outcome": "excluded_support", "justification": "reason was non-committal"}'
    )
    assert outcome == "excluded_support"
    assert err is None


def test_build_prompt_preserves_type_vocab_for_excluded_type_judgment():
    """Borges's security-pass fold #2: a positive test that a type-vocab
    word in supersede_reason SURVIVES this labeler's redaction, guarding
    design-tension-#3 against a future patch that reuses the full
    type_reclassification.redact screen here (which would silently break
    the one judgment -- excluded_type -- this labeler exists to make).

    This test itself caught a real bug during implementation: the first
    redaction fix reused compression_fidelity.redact.screen_text, believing
    it was "confidence-value screening only" -- but that module ALSO
    redacts quote_type/reasoning_type enum values unconditionally as part
    of its bundled vocabulary pass, so the first fix silently broke
    excluded_type detection. Fixed with a narrow, self-contained
    confidence-number-only pattern (see outcome_prompt.py's
    _CONFIDENCE_NUMBER_PATTERN)."""
    item = {
        "id": "ob_0200",
        "old_claim": "ENGRAM's compaction hook always fires within 2 seconds.",
        "new_claim": "ENGRAM's compaction hook always fires within 2 seconds.",
        "supersede_reason": (
            "this should have been filed as official_statement not hard_data "
            "-- the claim itself was right, just the wrong quote_type"
        ),
    }
    _, user_prompt = build_prompt(item, random.Random(0))
    assert "official_statement" in user_prompt
    assert "hard_data" in user_prompt
    assert "quote_type" in user_prompt
