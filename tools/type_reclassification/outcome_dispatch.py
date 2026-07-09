"""Dispatch + response parsing for the blind outcome-labeler pass.

Deliberately does NOT import anything from judge_prompt.py (the type-judge
prompt module) — isolation requirement (Borges, seq 1395): the outcome-
labeler must be independent of and blind to the type-judge, so this module
only shares the low-level transport (dispatch.py's JudgeClient/PanelMember/
DispatchError — pure HTTP plumbing, no prompt content) with the type-judge
path, never any prompt text, vocabulary, or per-item result.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass

from .dispatch import PanelMember
from .outcome_prompt import build_prompt, valid_outcome_names


@dataclass
class OutcomeResult:
    packet_id: str
    lineage: str
    model: str
    outcome: str | None  # None if unparseable
    justification: str
    raw_response: str
    parse_error: str | None = None


def parse_outcome_response(raw_text: str) -> tuple:
    """Mirrors dispatch.parse_judge_response but for the outcome vocabulary
    (refuted / survivor_refined / excluded_support) instead of quote_type
    names. Kept as a separate function (not a shared generic parser) so the
    two response schemas can diverge independently without one change
    silently affecting the other pass.
    """
    text = raw_text.strip()
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
    outcome = obj.get("outcome")
    justification = obj.get("justification", "")
    if outcome not in valid_outcome_names():
        return None, justification, f"outcome {outcome!r} is not one of {valid_outcome_names()}"
    return outcome, justification, None


def dispatch_outcome_one(member: PanelMember, supersede_item: dict, seed_suffix: str = "") -> OutcomeResult:
    """Dispatch one supersede_item to one panel member for outcome labeling.

    seed_suffix lets a caller vary the (currently-unused) rng deterministically
    per call if this prompt ever gains an order-randomizable element (see
    outcome_prompt.build_prompt's docstring) without changing this
    function's signature.
    """
    rng = random.Random(f"{supersede_item.get('id', '')}:{seed_suffix}")
    system_prompt, user_prompt = build_prompt(supersede_item, rng)
    raw = member.client.dispatch(system_prompt, user_prompt, member.model)
    outcome, justification, parse_error = parse_outcome_response(raw)
    return OutcomeResult(
        packet_id=supersede_item.get("id", ""),
        lineage=member.lineage,
        model=member.model,
        outcome=outcome,
        justification=justification,
        raw_response=raw,
        parse_error=parse_error,
    )
