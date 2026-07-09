"""Blind outcome-labeler prompt — the third blind-dispatch pass (Borges's
DMs, 2026-07-08, seq 1395 + 1398): resolves a superseded observation's true
outcome (refuted / survivor_refined / excluded_support / excluded_type) via
an EXOGENOUS blind labeler, NOT the author's own analysis (same-standpoint
bias — the exact problem Study-1's v4/dv_1069 amendment eliminated) and NOT
a deterministic classifier (there's no stored field for this; it's a
judgment call over old_claim/new_claim/supersede_reason text).

Hard isolation requirement (Borges, seq 1395): this labeler must be
INDEPENDENT OF AND BLIND TO the type-judge (judge_prompt.py) — neither pass
sees the other's prompt, output, or any framing about what the other pass
is for. Do not import/reference judge_prompt.py's SYSTEM_PROMPT or type
vocabulary from this module, and do not let any orchestration code leak an
outcome-labeler's verdict into a type-judge prompt or vice versa.

excluded_type is a CIRCULARITY GUARD (Borges, seq 1398): the study's
predictor is type-mis-selection (divergence). A node whose only fault was a
wrong TYPE (claim content fine) must not count as a refutation outcome, or
the predictor and the outcome would be the same construct — trivially
circular. So excluded_type is tracked as its own bucket, not folded into
excluded_support, specifically so the exclusion can be reported/audited.

Also per Borges (seq 1398): there is NO separate retract-side type-error
bucket — the pre-reg's §4 "type-error retracts" language was an error he's
fixing; a type-only correction is a supersede in practice, so excluded_type
only ever arises from THIS labeler (superseded nodes), not from the
mechanical retract-side error_type classification in db.py.

REVIEWER-FAIRY-CAUGHT BLOCKER, fixed here: this module previously applied
NO redaction to old_claim/new_claim/supersede_reason before rendering them
into the prompt — the docstring said callers "must not include confidence"
but nothing enforced it, and a plausible supersede_reason like "confidence
was 0.4, should be 0.85" would leak a numeric confidence value straight
into the labeler's prompt (same leak CLASS the sibling redact.py module
found for the type-judge's frame_export path).

SECOND, SELF-CAUGHT bug in the first fix attempt (found while implementing
Borges's security-pass fold #2 — a positive test that type-vocab SURVIVES
this labeler's redaction): the first fix ran old_claim/new_claim/
supersede_reason through the BASE `compression_fidelity.redact.screen_text`,
reasoning that it was "confidence-value screening only." That reasoning was
WRONG — direct testing showed `screen_text` ALSO redacts quote_type/
reasoning_type ENUM VALUES ("hard_data", "official_statement", etc.)
unconditionally as part of its bundled vocabulary pass; there is no way to
select "just the confidence-number pass" from that module's `screen_text`.
So the first fix silently broke the exact judgment (excluded_type
detection needs to see phrases like "should have been official_statement
not hard_data") it was written to preserve — caught only by trying to write
the positive survival test the fold asked for, not by reasoning about it.

FIX: a self-contained, narrow, purpose-built pattern (`_CONFIDENCE_NUMBER_PATTERN`
below) that redacts ONLY bare decimal-shaped numbers ([0-1].NN), independent
of `compression_fidelity.redact` entirely. This closes the concretely-
demonstrated risk (an arbitrary confidence-shaped number leaking, and
carrying no legitimate rubric signal) without touching quote_type/
reasoning_type vocabulary, outcome-vocabulary words, or anything else this
labeler legitimately needs to see. Deliberately NOT reusing
`type_reclassification.redact`'s outcome-vocab/field-name passes either,
for the same reason: this labeler already knows it's looking at a supersede
event, so outcome-vocabulary words aren't an answer-key leak for ITS task
the way they are for the type-judge's blinding, and it needs quote_type/
reasoning_type vocabulary intact to make the excluded_type call at all.
Flag to Borges/Kepler if this narrower read is wrong.
"""

from __future__ import annotations

import random
import re

# Narrow, self-contained: redacts ONLY bare decimal-shaped numbers
# (0.NN / 1.0-style), independent of compression_fidelity.redact entirely
# -- see module docstring for why that module's screen_text is NOT reused
# here (it also strips quote_type/reasoning_type enum values, which this
# labeler needs intact). Deliberately broader than "must be near the word
# confidence" (compression_fidelity's own _CONF_PATTERN convention) --
# a bare decimal in this specific free-text (a claim revision reason) has
# no legitimate non-confidence use we've identified, so over-redaction is
# the safe default here.
_CONFIDENCE_NUMBER_PATTERN = re.compile(r"(?<![0-9.])[01]?\.\d+(?![0-9.])")
_REDACTED = "[number redacted]"


def _redact_confidence_numbers(text: str) -> str:
    return _CONFIDENCE_NUMBER_PATTERN.sub(_REDACTED, text)


SYSTEM_PROMPT = (
    "You are participating in a research study that classifies how a factual "
    "claim was later revised. You will be shown an OLD claim, a NEW claim "
    "that replaced it, and the stated reason for the replacement. You do not "
    "know who wrote either claim or why beyond the reason given. Do not use "
    "any tool. Respond only in the exact JSON format requested at the end of "
    "the prompt."
)

# Verbatim rubric from Borges's DM (seq 1395, 2026-07-08), sourced from
# study1_fairy_spec.md. Reproduced as given — do not paraphrase or add
# examples beyond what's pasted here; if the rubric needs elaboration, that
# should happen in the source pre-reg doc, not invented in this module.
_RUBRIC_TEXT = (
    "RUBRIC\n"
    "The only question is whether the OLD claim was false WHEN IT WAS FILED "
    "— not whether it is false now, and not whether something changed later.\n\n"
    "- A claim that was correct at filing, but became false later because of "
    "a LATER decision, restructure, or premise reversal, is survivor_refined "
    "(evolution), NOT refuted. Tells for this: \"false under the NEW "
    "structure\", \"restructured\", \"reversed by a later decision\", "
    "\"premise LATER superseded\", \"was valid then\".\n"
    "- Assign refuted ONLY IF the stated reason asserts the OLD claim's "
    "CONTENT was incorrect AT THE TIME IT WAS FILED (wrong / mistaken / "
    "false / \"actually X, not Y\" / corrected a factual error).\n"
    "- Assign survivor_refined if the reason describes narrowing, "
    "extending, re-scoping, a vocabulary change, or adding nuance to a "
    "claim that was correct at the time.\n"
    "- If the reason is empty or non-committal (doesn't clearly say the "
    "claim was wrong), assign excluded_support, NOT refuted. Only an "
    "explicit \"the claim was wrong\" statement upgrades this to refuted.\n"
    "- If the old and new claims are essentially the same claim (identical "
    "or semantically equivalent — the supersede only changed metadata or "
    "confidence, not the claim's content), assign survivor_refined.\n"
    "- If the new claim contradicts or corrects the old claim (the new "
    "claim reverses or fixes something the old one got wrong), assign "
    "refuted. If the new claim narrows, extends, or rephrases the old one, "
    "and the old one was correct at the time, assign survivor_refined.\n"
    "- If the supersede's effect was to correct the node's TYPE/CLASSIFICATION "
    "while the claim's content stayed true and unchanged (e.g. it should have "
    "been filed as a conjecture, not an observation; or the quote_type/"
    "reasoning_type was wrong, but what the claim asserts held up), assign "
    "excluded_type — NOT refuted and NOT excluded_support. Distinguish by "
    "WHAT the supersede actually changed: content was wrong -> refuted; "
    "content narrowed/rescoped -> survivor_refined; the support/evidence/"
    "citation was wrong -> excluded_support; the classification/type was "
    "wrong but the claim itself was fine -> excluded_type.\n\n"
    "Worked examples:\n"
    "- \"the mechanism does NOT fire on contradict, only on resolve — "
    "earlier claim was wrong\" -> refuted.\n"
    "- \"narrowed scope to multi-agent; single-agent framing imprecise but "
    "not wrong\" -> survivor_refined.\n"
    "- \"this should have been filed as a conjecture, not an observation — "
    "the claim itself was right\" -> excluded_type.\n"
)

_RESPONSE_FORMAT_INSTRUCTIONS = (
    "\nRespond with ONLY a single JSON object, no other text, in exactly this "
    "shape:\n"
    '{"outcome": "<one of: refuted, survivor_refined, excluded_support, excluded_type>", '
    '"justification": "<one sentence citing which part of the rubric applied>"}'
)

OUTCOME_CATEGORIES = ("refuted", "survivor_refined", "excluded_support", "excluded_type")


def build_prompt(supersede_item: dict, rng: random.Random) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) for one superseded-node outcome
    labeling item.

    supersede_item: {"id": ..., "old_claim": ..., "new_claim": ...,
    "supersede_reason": ...}. Callers must NOT include confidence, node
    type, filing-agent, or any type-judge output in this dict — same
    withholding discipline as the type-judge frame (see frame_export.py).
    Confidence NUMBERS that slip into free text anyway are screened by this
    function itself (see module docstring's "REVIEWER-FAIRY-CAUGHT BLOCKER"
    section for what's screened and, deliberately, what is NOT).

    rng accepted for interface symmetry with judge_prompt.build_prompt (this
    rubric has no order-randomizable element today — the category list order
    is fixed/small enough that randomizing it isn't load-bearing the way the
    7-way quote_type list is — but kept as a parameter so both prompt
    builders share a call signature or gain one later without an API break.
    """
    del rng  # unused today, kept for signature symmetry — see docstring
    old_claim = _redact_confidence_numbers(supersede_item.get("old_claim", ""))
    new_claim = _redact_confidence_numbers(supersede_item.get("new_claim", ""))
    raw_reason = supersede_item.get("supersede_reason", "") or "(no reason given)"
    reason = _redact_confidence_numbers(raw_reason)

    user_prompt = (
        f"{_RUBRIC_TEXT}\n"
        f"OLD CLAIM\n{old_claim}\n\n"
        f"NEW CLAIM\n{new_claim}\n\n"
        f"STATED REASON FOR THE REPLACEMENT\n{reason}\n"
        f"{_RESPONSE_FORMAT_INSTRUCTIONS}"
    )
    return SYSTEM_PROMPT, user_prompt


def valid_outcome_names() -> tuple:
    return OUTCOME_CATEGORIES
