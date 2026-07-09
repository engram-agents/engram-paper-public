"""Raw-API judge dispatch for the derivation-arm (reasoning_type)
normative type-assignment task — pre-reg §7 isolation-by-construction.

Deliberately does NOT duplicate `PanelMember`/`JudgeClient`/`DispatchError`/
`AnthropicClient`/`FakeJudgeClient` — those are pure HTTP-transport
plumbing, generic across doses, and import cleanly from `.dispatch`. Only
the response-parsing/validation logic is dose-specific (it needs
`derivation_judge_prompt.valid_type_names()` instead of
`judge_prompt.valid_type_names()`), so that piece gets its own function
here rather than parameterizing `dispatch.py` itself — mirrors
`outcome_dispatch.py`'s own precedent for this exact shape of "share
transport, not prompt/response logic" split.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from .dispatch import DispatchError, JudgeClient, PanelMember  # noqa: F401  (re-exported for callers)
from .derivation_judge_prompt import build_prompt, rng_for_item, valid_type_names


@dataclass
class DerivationJudgeResult:
    packet_id: str
    pass_index: int
    lineage: str
    model: str
    assigned_type: str | None  # None if unparseable — see parse errors below
    justification: str
    raw_response: str
    parse_error: str | None = None


def parse_derivation_judge_response(raw_text: str) -> tuple[str | None, str, str | None]:
    """Parse a judge's raw text response into (assigned_type, justification,
    parse_error). assigned_type is None and parse_error is set (not raised)
    on any failure — a single judge's malformed response must not crash a
    panel run; it becomes a recorded parse failure the analysis stage can
    account for (and, per pre-reg §3, an item with too many parse failures
    to reach a majority is itself evidence for the panel-discordant bucket).

    Mirrors `dispatch.parse_judge_response` exactly, except validation is
    against the DERIVATION arm's `valid_type_names()` (reasoning_type
    vocabulary), not the observation arm's quote_type vocabulary.
    """
    text = raw_text.strip()
    # Judges sometimes wrap JSON in a code fence despite instructions not to.
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip()
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        return None, "", f"not valid JSON: {e}"
    if not isinstance(obj, dict):
        return None, "", f"response JSON is not an object: {obj!r}"
    assigned = obj.get("assigned_type")
    justification = obj.get("justification", "")
    if assigned not in valid_type_names():
        return None, justification, (
            f"assigned_type {assigned!r} is not one of the valid reasoning_type names"
        )
    return assigned, justification, None


def dispatch_derivation_one(
    member: PanelMember, frame_item: dict, pass_index: int
) -> DerivationJudgeResult:
    """Dispatch a single derivation-arm frame item to a single panel member
    for one pass. Never raises on a judge-response problem (see
    parse_derivation_judge_response) — only raises DispatchError on a
    transport failure, which the caller (the inter-rater orchestrator) is
    expected to catch per-call so one dead judge doesn't kill an entire
    panel batch.
    """
    rng = rng_for_item(frame_item, pass_index)
    system_prompt, user_prompt = build_prompt(frame_item, rng)
    raw = member.client.dispatch(system_prompt, user_prompt, member.model)
    assigned_type, justification, parse_error = parse_derivation_judge_response(raw)
    return DerivationJudgeResult(
        packet_id=frame_item.get("id", ""),
        pass_index=pass_index,
        lineage=member.lineage,
        model=member.model,
        assigned_type=assigned_type,
        justification=justification,
        raw_response=raw,
        parse_error=parse_error,
    )
