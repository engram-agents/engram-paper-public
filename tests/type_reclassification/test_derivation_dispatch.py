"""Tests for the derivation-arm judge dispatch machinery -- mirrors the
`# ── dispatch ──` section of `tests/type_reclassification/
test_judge_dispatch.py` (the observation-arm equivalent), all against
FakeJudgeClient (no live API dependency), per the study's freeze discipline
(synthetic fixtures only, no real-graph or live-API access until sign-off).
"""

from tools.type_reclassification.derivation_dispatch import (
    DerivationJudgeResult,
    dispatch_derivation_one,
    parse_derivation_judge_response,
)
from tools.type_reclassification.dispatch import FakeJudgeClient, PanelMember


def _clean_frame_item():
    return {
        "id": "dv_0001",
        "claim": "Therefore all observed swans are white.",
        "premises": [
            {"claim": "Swan #1 observed at the lake was white.", "type": "hard_data"},
            {"claim": "Swan #2 observed at the lake was white.", "type": "hard_data"},
        ],
        "stratum": {"outcome": "survived", "fs_class": "frozen"},
    }


def test_fake_client_dispatch_and_parse_roundtrip():
    client = FakeJudgeClient(
        default_response='{"assigned_type": "inductive_generalization", "justification": "corroborative, multi-source"}'
    )
    member = PanelMember(client=client, model="fake-model", lineage="fake:lineage")
    item = _clean_frame_item()
    result = dispatch_derivation_one(member, item, pass_index=0)
    assert isinstance(result, DerivationJudgeResult)
    assert result.assigned_type == "inductive_generalization"
    assert result.parse_error is None
    assert result.packet_id == item["id"]
    assert len(client.calls) == 1


def test_parse_derivation_judge_response_rejects_invalid_type():
    assigned, justification, err = parse_derivation_judge_response(
        '{"assigned_type": "not_a_real_type", "justification": "x"}'
    )
    assert assigned is None
    assert err is not None


def test_parse_derivation_judge_response_rejects_observation_arm_vocabulary():
    """Reviewer-fairy suggestion: a value valid in the OBSERVATION arm's
    quote_type vocabulary (e.g. 'hard_data') must be REJECTED here -- this
    is the live enforcement that derivation_dispatch.py validates against
    its OWN valid_type_names() and not a copy-paste-from-template import of
    the observation arm's judge_prompt.valid_type_names(). 'not_a_real_type'
    alone (the test above) can't catch that specific bug, since it's invalid
    in BOTH vocabularies."""
    assigned, justification, err = parse_derivation_judge_response(
        '{"assigned_type": "hard_data", "justification": "x"}'
    )
    assert assigned is None
    assert err is not None


def test_parse_derivation_judge_response_handles_code_fence_wrapping():
    raw = '```json\n{"assigned_type": "abductive_best_explanation", "justification": "best fit"}\n```'
    assigned, justification, err = parse_derivation_judge_response(raw)
    assert assigned == "abductive_best_explanation"
    assert err is None


def test_parse_derivation_judge_response_handles_garbage():
    assigned, justification, err = parse_derivation_judge_response("not json at all")
    assert assigned is None
    assert err is not None
