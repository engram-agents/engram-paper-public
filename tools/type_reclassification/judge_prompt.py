"""Builds the rubric-only judge prompt for the observation-arm (quote_type)
normative type-assignment task — pre-reg §2/§7.

Isolation-by-construction (pre-reg §7): this prompt is self-contained. It
carries NO ENGRAM identity material, NO confidence-scale anchors, NO tool
definitions, NO instruction to use any tool. It is dispatched via a raw API
call (see dispatch.py), never via a Claude-Code/Agent-tool subagent — a
framework subagent inherits the dispatching agent's CLAUDE.md, which is
exactly the confidence-anchor leak this isolation is designed to close
(dv_1081). Nothing in this module should ever be handed to the Agent/Task
tool.
"""

from __future__ import annotations

import random

from .type_definitions import QUOTE_TYPES, VERBATIM_QUOTE_TYPE_SCHEMA_TEXT, order_randomized

SYSTEM_PROMPT = (
    "You are participating in a research study that classifies short factual "
    "claims. You will be shown a claim and the evidence that was cited for it. "
    "You do not know who wrote this, why, or what happened to it afterward — "
    "and none of that is relevant to your task. Answer only from the evidence "
    "given. Do not use any tool. Respond only in the exact JSON format "
    "requested at the end of the prompt."
)

_TASK_INSTRUCTIONS = (
    "TASK\n"
    "Below is a CLAIM and the EVIDENCE that was cited to support it. Your job: "
    "assign the strongest of the following types that this CLAIM is warranted "
    "in, given ONLY the evidence shown. Do not assume anything about the claim "
    "beyond what the evidence text actually supports. If the claim reaches "
    "further than the evidence justifies (e.g. the evidence is a single "
    "informal remark but the claim asserts it as settled fact), assign the "
    "weaker type the evidence actually warrants, not the type the claim's "
    "own phrasing implies.\n\n"
    "TYPES (schema definition, verbatim from the source system)\n"
    f"{VERBATIM_QUOTE_TYPE_SCHEMA_TEXT}\n\n"
    "The types, in the order to consider them for this item, are:\n"
)

_RESPONSE_FORMAT_INSTRUCTIONS = (
    "\nRespond with ONLY a single JSON object, no other text, in exactly this "
    "shape:\n"
    '{"assigned_type": "<one of the type names above, exact spelling>", '
    '"justification": "<one sentence: why this type and not a stronger one>"}'
)


def build_prompt(frame_item: dict, rng: random.Random) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) for a single observation-arm
    frame item ({id, claim, evidence: {...}, stratum: {...}}).

    frame_item's evidence dict must carry ONLY the pre-reg §2 dose fields
    (quoted_text, source_class, source_domain, source_date) — this function
    does not itself filter/withhold anything; that's frame_export.py's job.
    This function will render whatever is in frame_item["evidence"] verbatim,
    so a frame_item that still carries confidence/quote_type/interpretation
    would leak it straight into the judge prompt. Callers MUST pass
    already-withheld frame items (see frame_export.py's own test asserting
    the withholding property) — this function does not re-check it, by
    design: prompt construction is not the place to silently drop a field a
    caller assembled wrong, it's the frame-export layer's job to never
    produce one.

    rng: caller-owned random.Random, seeded deterministically per item (e.g.
    from the packet_id) so type-order randomization is reproducible without
    being global-random (would make dispatch order-dependent and hard to
    replay for a second inter-rater pass on the identical prompt).
    """
    evidence = frame_item.get("evidence", {})
    claim = frame_item.get("claim", "")

    ordered_types = order_randomized(rng)
    type_list_text = "\n".join(f"- {t}" for t in ordered_types)

    evidence_lines = []
    if "quoted_text" in evidence:
        evidence_lines.append(f'Quoted text: "{evidence["quoted_text"]}"')
    if evidence.get("source_class"):
        evidence_lines.append(f"Source class: {evidence['source_class']}")
    if evidence.get("source_domain"):
        evidence_lines.append(f"Source domain: {evidence['source_domain']}")
    if evidence.get("source_date"):
        evidence_lines.append(f"Source date: {evidence['source_date']}")
    evidence_text = "\n".join(evidence_lines) if evidence_lines else "(no evidence fields provided)"

    user_prompt = (
        f"{_TASK_INSTRUCTIONS}{type_list_text}\n\n"
        f"CLAIM\n{claim}\n\n"
        f"EVIDENCE\n{evidence_text}\n"
        f"{_RESPONSE_FORMAT_INSTRUCTIONS}"
    )
    return SYSTEM_PROMPT, user_prompt


def rng_for_item(frame_item: dict, pass_index: int) -> random.Random:
    """Deterministic per-item, per-pass RNG seed.

    Two independent inter-rater passes (pre-reg §10) over the SAME item must
    NOT reuse the identical type-order (that would make the two passes
    correlated on presentation order, not independent measurements) — so the
    seed folds in pass_index, not just the item id.
    """
    seed_str = f"{frame_item.get('id', '')}:{pass_index}"
    return random.Random(seed_str)


def response_schema_keys() -> tuple:
    return ("assigned_type", "justification")


def valid_type_names() -> tuple:
    return QUOTE_TYPES
