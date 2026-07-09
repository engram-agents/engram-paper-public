"""Builds the rubric-only judge prompt for the derivation-arm
(reasoning_type) normative type-assignment task — pre-reg §2/§7.

Isolation-by-construction (pre-reg §7): this prompt is self-contained. It
carries NO ENGRAM identity material, NO confidence-scale anchors, NO tool
definitions, NO instruction to use any tool. It is dispatched via a raw API
call (see derivation_dispatch.py), never via a Claude-Code/Agent-tool
subagent — a framework subagent inherits the dispatching agent's CLAUDE.md,
which is exactly the confidence-anchor leak this isolation is designed to
close (dv_1081). Nothing in this module should ever be handed to the
Agent/Task tool.
"""

from __future__ import annotations

import random

from .derivation_type_definitions import (
    REASONING_TYPES,
    VERBATIM_REASONING_TYPE_SCHEMA_TEXT,
    order_randomized,
)

SYSTEM_PROMPT = (
    "You are participating in a research study that classifies short factual "
    "claims. You will be shown a claim and the premises that were cited to "
    "support it via a specific reasoning step. You do not know who wrote "
    "this, why, or what happened to it afterward — and none of that is "
    "relevant to your task. Answer only from the premises given. Do not use "
    "any tool. Respond only in the exact JSON format requested at the end "
    "of the prompt."
)

_TASK_INSTRUCTIONS = (
    "TASK\n"
    "Below is a CLAIM and the PREMISES that were cited to support it via a "
    "specific reasoning step. Your job: assign the strongest of the "
    "following types of logical argument that this CLAIM is warranted in, "
    "given ONLY the premises shown. Do not assume anything about the claim "
    "beyond what the premises actually support. If the claim reaches "
    "further than the premises justify (e.g. the premises support only a "
    "weaker inductive or abductive step but the claim asserts the "
    "conclusion as if it followed deductively), assign the weaker type the "
    "premises actually warrant, not the type the claim's own phrasing "
    "implies.\n\n"
    "TYPES (schema definition, verbatim from the source system)\n"
    f"{VERBATIM_REASONING_TYPE_SCHEMA_TEXT}\n\n"
    "The types, in the order to consider them for this item, are:\n"
)

_RESPONSE_FORMAT_INSTRUCTIONS = (
    "\nRespond with ONLY a single JSON object, no other text, in exactly this "
    "shape:\n"
    '{"assigned_type": "<one of the type names above, exact spelling>", '
    '"justification": "<one sentence: why this type and not a stronger one>"}'
)


def build_prompt(frame_item: dict, rng: random.Random) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) for a single derivation-arm
    frame item ({id, claim, premises: [{claim, type}, ...], stratum: {...}}).

    frame_item's premises list must carry ONLY the pre-reg §2 dose fields
    per premise (claim, type) — this function does not itself filter/
    withhold anything at the frame_item level (that responsibility is
    frame_export.py's job); however, THIS function's own rendering of each
    premise WHITELISTS exactly `premise.get("claim")` and
    `premise.get("type")` (docstring correction, Borges's PR #23 review,
    2026-07-08 — the earlier wording claimed this function "renders
    whatever is in frame_item['premises'] verbatim," which overstated the
    actual leak risk: a stray extra key on a premise dict, e.g.
    confidence/reasoning_type/interpretation set there by caller error,
    is NOT rendered, since only the two whitelisted keys are ever read).
    Callers should still pass already-withheld frame items (see
    frame_export.py's own test asserting the withholding property) as the
    primary discipline — this function's per-premise whitelisting is a
    second, narrower line of defense specific to the premises list, not a
    substitute for frame_export's own withholding responsibility over the
    rest of the frame_item (e.g. a top-level `confidence` key on
    frame_item itself would still need frame_export to have never put it
    there).

    A premise's "type" field is rendered ONLY when it is not None — a
    premise cited from a non-observation/non-derivation node (e.g. an
    axiom) has no established type to show, and rendering the literal
    string "None" would look like a leaked null/error to the judge rather
    than intentional withholding of a field that genuinely doesn't exist
    for that premise.

    rng: caller-owned random.Random, seeded deterministically per item (e.g.
    from the packet_id) so type-order randomization is reproducible without
    being global-random (would make dispatch order-dependent and hard to
    replay for a second inter-rater pass on the identical prompt).
    """
    premises = frame_item.get("premises", [])
    claim = frame_item.get("claim", "")

    ordered_types = order_randomized(rng)
    type_list_text = "\n".join(f"- {t}" for t in ordered_types)

    premise_lines = []
    for i, premise in enumerate(premises, start=1):
        line = f'{i}. "{premise.get("claim", "")}"'
        if premise.get("type") is not None:
            line += f' (type: {premise["type"]})'
        premise_lines.append(line)
    premises_text = "\n".join(premise_lines) if premise_lines else "(no premises provided)"

    user_prompt = (
        f"{_TASK_INSTRUCTIONS}{type_list_text}\n\n"
        f"CLAIM\n{claim}\n\n"
        f"PREMISES\n{premises_text}\n"
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
    return REASONING_TYPES
