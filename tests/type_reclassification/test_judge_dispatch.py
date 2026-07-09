"""Tests for the type-judge prompt/dispatch/inter-rater machinery — all
against FakeJudgeClient (no live API dependency), per the study's freeze
discipline (synthetic fixtures only, no real-graph or live-API access
until sign-off)."""

import random

from tools.type_reclassification.dispatch import (
    AnthropicClient,
    DispatchError,
    FakeJudgeClient,
    PanelMember,
    dispatch_one,
    parse_judge_response,
    scope_b_panel,
)
from tools.type_reclassification.interrater import (
    KAPPA_INSTRUMENT_VALIDITY_FLOOR,
    fleiss_kappa,
    instrument_validity_gate,
    run_panel,
    summarize_all,
    summarize_item,
)
from tools.type_reclassification.judge_prompt import build_prompt, rng_for_item, valid_type_names


def _clean_frame_item(claim="Gold fell 9.6% this week.", quoted_text="Gold fell 9.6%."):
    return {
        "id": "ob_0001",
        "claim": claim,
        "evidence": {
            "quoted_text": quoted_text,
            "source_class": "external",
            "source_domain": "example.com",
            "source_date": "2026-01-01",
        },
        "stratum": {"outcome": "survived", "fs_class": "frozen"},
    }


# ── judge_prompt ────────────────────────────────────────────────────────


def test_build_prompt_contains_evidence_and_all_type_names():
    item = _clean_frame_item()
    system_prompt, user_prompt = build_prompt(item, random.Random(0))
    assert "do not use any tool" in system_prompt.lower()
    assert item["claim"] in user_prompt
    assert item["evidence"]["quoted_text"] in user_prompt
    for t in valid_type_names():
        assert t in user_prompt
    # Confidence VALUE / node id must never appear in the rendered prompt.
    # ("confidence" as a bare word is fine -- it never appears in this
    # prompt's static text at all, so this also incidentally checks that.)
    assert "confidence" not in user_prompt.lower()
    assert item["id"] not in user_prompt


def test_build_prompt_never_renders_stratum():
    """Borges's security-pass fold #1: build_prompt currently never touches
    frame_item["stratum"] at all -- true by construction (it isn't read),
    but that's an invariant a future derivation-arm edit could silently
    break without any test catching it. Make it a TESTED invariant: even
    when stratum carries the outcome (which frame_export.py must never let
    reach a real judge, but this test isn't relying on frame_export's own
    discipline -- it directly probes build_prompt), no stratum content
    leaks into the rendered prompt."""
    item = _clean_frame_item()
    item["stratum"] = {"outcome": "survived", "fs_class": "frozen"}
    _, user_prompt = build_prompt(item, random.Random(0))
    assert "stratum" not in user_prompt.lower()
    assert "survived" not in user_prompt.lower()
    assert "fs_class" not in user_prompt.lower()


def test_build_prompt_never_leaks_extra_evidence_fields():
    item = _clean_frame_item()
    item["evidence"]["interpretation"] = "the agent's own reach-justification, must not leak"
    item["evidence"]["quote_type"] = "hard_data"
    _, user_prompt = build_prompt(item, random.Random(0))
    # build_prompt only renders the 4 dose fields it explicitly knows about
    # (quoted_text/source_class/source_domain/source_date) -- confirm a
    # caller-mistake extra field does NOT get rendered just by being present
    # in the evidence dict (defense in depth on top of frame_export's own
    # withholding responsibility).
    assert "reach-justification" not in user_prompt
    # "quote_type" DOES legitimately appear in the verbatim schema-definition
    # block (pre-reg §2: judge sees the real tool-schema type definitions,
    # which are literally labeled "quote_type: One of: ..."). The leak this
    # test actually guards against is the CHOSEN value being labeled back to
    # the field name, i.e. a "quote_type: hard_data" pairing that reveals
    # what the agent picked for THIS item -- not the schema header itself.
    assert "quote_type: hard_data" not in user_prompt.lower()


def test_two_passes_use_different_type_order():
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


# ── dispatch ────────────────────────────────────────────────────────────


def test_fake_client_dispatch_and_parse_roundtrip():
    client = FakeJudgeClient(default_response='{"assigned_type": "hard_data", "justification": "measured event"}')
    member = PanelMember(client=client, model="fake-model", lineage="fake:lineage")
    item = _clean_frame_item()
    result = dispatch_one(member, item, pass_index=0)
    assert result.assigned_type == "hard_data"
    assert result.parse_error is None
    assert result.packet_id == item["id"]
    assert len(client.calls) == 1


def test_parse_judge_response_rejects_invalid_type():
    assigned, justification, err = parse_judge_response('{"assigned_type": "not_a_real_type", "justification": "x"}')
    assert assigned is None
    assert err is not None


def test_parse_judge_response_handles_code_fence_wrapping():
    raw = '```json\n{"assigned_type": "editorial", "justification": "opinion"}\n```'
    assigned, justification, err = parse_judge_response(raw)
    assert assigned == "editorial"
    assert err is None


def test_parse_judge_response_handles_garbage():
    assigned, justification, err = parse_judge_response("not json at all")
    assert assigned is None
    assert err is not None


def test_anthropic_client_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    client = AnthropicClient()
    try:
        client.dispatch("sys", "user", "claude-sonnet-5")
        assert False, "expected DispatchError"
    except DispatchError as e:
        assert "ANTHROPIC_API_KEY" in str(e)


def test_scope_b_panel_is_three_anthropic_seats():
    panel = scope_b_panel(client=FakeJudgeClient())
    assert len(panel) == 3
    assert all(m.lineage.startswith("anthropic:") for m in panel)
    assert len({m.model for m in panel}) == 3  # three distinct models


# ── interrater / Fleiss kappa ─────────────────────────────────────────


def test_run_panel_dispatches_every_item_to_every_member_every_pass():
    client = FakeJudgeClient(default_response='{"assigned_type": "hard_data", "justification": "x"}')
    panel = [
        PanelMember(client=client, model="m1", lineage="fake:a"),
        PanelMember(client=client, model="m2", lineage="fake:b"),
        PanelMember(client=client, model="m3", lineage="fake:c"),
    ]
    items = [_clean_frame_item(), {**_clean_frame_item(), "id": "ob_0002"}]
    results = run_panel(panel, items, n_passes=2)
    assert len(results) == len(items) * len(panel) * 2  # 2 items * 3 members * 2 passes = 12
    assert all(r.assigned_type == "hard_data" for r in results)


def test_run_panel_survives_a_dispatch_error():
    class FlakyClient:
        def __init__(self):
            self.n = 0

        def dispatch(self, system_prompt, user_prompt, model):
            self.n += 1
            if self.n == 1:
                raise DispatchError("simulated network failure")
            return '{"assigned_type": "hard_data", "justification": "x"}'

    panel = [PanelMember(client=FlakyClient(), model="m", lineage="fake:a")]
    results = run_panel(panel, [_clean_frame_item()], n_passes=2)
    assert len(results) == 2
    assert any(r.assigned_type is None and r.parse_error for r in results)
    assert any(r.assigned_type == "hard_data" for r in results)


def test_summarize_item_concordant_majority():
    from tools.type_reclassification.dispatch import JudgeResult

    results = [
        JudgeResult("ob_1", 0, "a", "m", "hard_data", "x", "{}"),
        JudgeResult("ob_1", 0, "b", "m", "hard_data", "x", "{}"),
        JudgeResult("ob_1", 1, "a", "m", "editorial", "x", "{}"),
    ]
    verdict = summarize_item("ob_1", results, n_expected_ratings=3)
    assert verdict.is_concordant is True
    assert verdict.majority_type == "hard_data"


def test_summarize_item_discordant_plurality_is_not_concordant():
    from tools.type_reclassification.dispatch import JudgeResult

    # 3 raters, 3 different answers -- no strict majority anywhere.
    results = [
        JudgeResult("ob_1", 0, "a", "m", "hard_data", "x", "{}"),
        JudgeResult("ob_1", 0, "b", "m", "editorial", "x", "{}"),
        JudgeResult("ob_1", 0, "c", "m", "unnamed_source", "x", "{}"),
    ]
    verdict = summarize_item("ob_1", results, n_expected_ratings=3)
    assert verdict.is_concordant is False
    assert verdict.majority_type is None


def test_summarize_all_groups_by_packet_id():
    from tools.type_reclassification.dispatch import JudgeResult

    results = [
        JudgeResult("ob_1", 0, "a", "m", "hard_data", "x", "{}"),
        JudgeResult("ob_2", 0, "a", "m", "editorial", "x", "{}"),
    ]
    grouped = summarize_all(results, n_expected_ratings=1)
    assert set(grouped.keys()) == {"ob_1", "ob_2"}


def test_fleiss_kappa_perfect_agreement_is_undefined_or_one():
    categories = valid_type_names()
    # 3 items, 4 raters each, all raters agree perfectly per item but items
    # differ from each other -- classic textbook near-perfect-agreement case.
    ratings = {
        "ob_1": ["hard_data"] * 4,
        "ob_2": ["editorial"] * 4,
        "ob_3": ["unnamed_source"] * 4,
    }
    kappa = fleiss_kappa(ratings, categories)
    # Perfect per-item agreement AND enough marginal variance across items
    # -> kappa should be at/near 1.0 (allow float tolerance).
    assert kappa == kappa  # not NaN
    assert kappa > 0.9


def test_fleiss_kappa_chance_level_agreement_is_near_zero():
    categories = ("hard_data", "editorial")
    # Each rater picks independently at random (fixed seed) -- with enough
    # items this converges toward the textbook chance-agreement case,
    # kappa near 0. (A small hand-rolled 2-2-split-every-item pattern is
    # NOT this case -- that's the maximum-disagreement configuration for 2
    # categories/4 raters and correctly produces a strongly negative kappa;
    # true independent-random assignment is what "chance level" means here.)
    rng = random.Random(20260708)
    ratings = {
        f"ob_{i}": [rng.choice(categories) for _ in range(4)]
        for i in range(200)
    }
    kappa = fleiss_kappa(ratings, categories)
    assert kappa == kappa
    assert abs(kappa) < 0.15


def test_fleiss_kappa_requires_consistent_rater_count():
    ratings = {"ob_1": ["hard_data", "hard_data"], "ob_2": ["hard_data"]}
    try:
        fleiss_kappa(ratings, ("hard_data",))
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_fleiss_kappa_too_few_items_is_nan():
    kappa = fleiss_kappa({"ob_1": ["hard_data", "editorial"]}, ("hard_data", "editorial"))
    assert kappa != kappa  # NaN


def test_instrument_validity_gate_floor():
    assert instrument_validity_gate(KAPPA_INSTRUMENT_VALIDITY_FLOOR) is True
    assert instrument_validity_gate(KAPPA_INSTRUMENT_VALIDITY_FLOOR - 0.01) is False
    assert instrument_validity_gate(float("nan")) is False
