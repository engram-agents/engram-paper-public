"""reasoning_type enum + judge-facing schema text for the derivation arm
(pre-reg §2 reasoning_type re-classification), analogous to
`type_definitions.py`'s quote_type module for the observation arm.

**Confidence-redacted, NOT verbatim** — the one deliberate departure from
`type_definitions.py`'s "reproduce the production docstring verbatim, never
enrich" discipline, and why:

Source of truth: engram-alpha `src/engram/engram_derive.py`'s
`_derive_impl` docstring (as of 2026-07-08, commit ae13c50) — the actual
prose a filing agent sees when choosing a `reasoning_type`. Unlike
`quote_type`'s production docstring (a bare enum list, nothing to redact),
`reasoning_type`'s docstring is saturated with per-type CONFIDENCE
information inline: numeric discounts ("discount 0.98"), caps
("cap 0.80"), and hierarchy/ranking words ("weakest legitimate form").
Reproducing this text truly verbatim would hand the judge the exact
downstream-confidence anchor pre-reg §2 withholds (dv_1081) — a strictly
worse leak than quote_type's clean-enum case, since here the leak sits
INSIDE the very schema text the judge must be shown to do the task at all.

**Design discussion (Borges, DM seq 1502/1505/1506, 2026-07-08; folded
into the pre-reg as draft 7, a blinding-strengthening amendment, FYI not
re-countersign):**

    The judge needs each type's INFERENCE-FORM semantics (what deductive /
    inductive_generalization / abductive / analogy MEAN as forms of
    inference). It must NOT see the CONFIDENCE-DERIVATION framing — numbers
    AND the mechanism/hierarchy words ("discount", "cap", "weakest
    legitimate form"). Those are the same downstream-confidence anchor
    Aleph flagged, just without the digits.

    KEEP (semantic requirement — e.g. "corroborative, multi-source" is the
    actual REQUIREMENT distinguishing inductive_generalization, and exactly
    what the judge needs to assess whether the agent's choice was
    warranted): descriptive prose about what the inference form IS or
    requires.

    DROP (confidence-derivation / hierarchy — ranks types by how much they
    should be trusted, not what they ARE): every numeric discount/cap value,
    and words like "discount", "cap", "weakest legitimate form".

This module applies that rule BY HAND against the real docstring text
below (not a generic regex over the whole schema — the failure mode a
blind regex risks is dropping semantic tokens entangled in the same
parenthetical as a confidence number, e.g. incorrectly stripping
"corroborative, multi-source" along with "0.95" from
"inductive_generalization (0.95, corroborative, multi-source)"). Every
redaction below is a deliberate, itemized decision — see the inline
comments on `_REASONING_TYPE_DEFINITIONS_TEXT` for the per-phrase
KEEP/DROP call, so a reviewer can audit each one against the source
docstring rather than trusting the regex to have gotten it right.
"""

from __future__ import annotations

# Enum values — engram-alpha `src/engram/engram_confidence.py`'s
# `REASONING_TYPES` set, reproduced as an ORDERED tuple (the set itself has
# no meaningful order; this module's own grouping below, by inference
# class, is the presentation order before `order_randomized` shuffles it).
REASONING_TYPES = (
    "deductive_modus_ponens",
    "deductive_modus_tollens",
    "deductive_hypothetical_syllogism",
    "deductive_disjunctive",
    "deductive_reductio",
    "inductive_generalization",
    "inductive_enumeration",
    "inductive_statistical",
    "inductive_analogy",
    "inductive_causal",
    "abductive_best_explanation",
    "abductive_elimination",
    "authority_expert",
    "authority_consensus",
)

# Confidence-redacted schema text, hand-verified against `_derive_impl`'s
# real docstring (engram-alpha engram_derive.py, ~lines 120-141 as of
# ae13c50). Each redaction decision below, phrase by phrase:
#
#   "Deductive (discount 0.98 -- truth-preserving)"
#     DROP "discount 0.98" (confidence-derivation number); KEEP
#     "truth-preserving" (semantic -- an actual property of deductive
#     inference: if premises are true, conclusion MUST be true).
#
#   "Inductive (discount 0.70-0.95 -- evidence strengthens but never
#   proves)"
#     DROP the discount range; KEEP "evidence strengthens but never
#     proves" (semantic -- what inductive inference IS).
#
#   "inductive_generalization (0.95, corroborative, multi-source)"
#     DROP "0.95"; KEEP "corroborative, multi-source" (semantic
#     REQUIREMENT distinguishing this type -- Borges's own example of what
#     must survive).
#
#   "inductive_enumeration (0.93, corroborative, single authoritative
#   source that enumerates structurally-independent items -- use when one
#   SEP/textbook entry decomposes a property into n distinct instances)"
#     DROP "0.93"; KEEP everything else (all semantic -- describes WHEN to
#     use this type).
#
#   "inductive_statistical (0.90), inductive_causal (0.85)"
#     DROP both parens entirely -- pure confidence numbers, no semantic
#     content in either.
#
#   "inductive_analogy (0.70, weakest legitimate form)"
#     DROP the whole paren -- "weakest legitimate form" is HIERARCHY/
#     ranking language (Borges's explicit DROP example), not a semantic
#     description of what analogy-based inference IS.
#
#   "Abductive (capped -- best explanation, alternatives may exist)"
#     DROP "capped" (hierarchy/mechanism word, same class as "discount");
#     KEEP "best explanation, alternatives may exist" (semantic -- what
#     abductive inference IS).
#
#   "abductive_best_explanation (cap 0.80), abductive_elimination (cap
#   0.90)"
#     DROP both parens entirely -- pure confidence-derivation, no semantic
#     content.
#
#   "Authority (trust transfer)"
#     No confidence info present -- kept unchanged (semantic: this IS what
#     authority-based reasoning is).
#
#   "authority_expert (0.95), authority_consensus (0.98, corroborative,
#   multi-source)"
#     DROP "0.95" paren entirely (pure confidence); for authority_consensus
#     DROP "0.98" but KEEP "corroborative, multi-source" (same semantic
#     requirement as inductive_generalization).
VERBATIM_REASONING_TYPE_SCHEMA_TEXT = (
    "Deductive (truth-preserving):\n"
    "  deductive_modus_ponens, deductive_modus_tollens,\n"
    "  deductive_hypothetical_syllogism, deductive_disjunctive, deductive_reductio\n"
    "\n"
    "Inductive (evidence strengthens but never proves):\n"
    "  inductive_generalization (corroborative, multi-source),\n"
    "  inductive_enumeration (corroborative, single authoritative source\n"
    "    that enumerates structurally-independent items — use when one SEP/textbook\n"
    "    entry decomposes a property into n distinct instances),\n"
    "  inductive_statistical, inductive_causal,\n"
    "  inductive_analogy\n"
    "\n"
    "Abductive (best explanation, alternatives may exist):\n"
    "  abductive_best_explanation, abductive_elimination\n"
    "\n"
    "Authority (trust transfer):\n"
    "  authority_expert, authority_consensus (corroborative, multi-source)"
)


def order_randomized(rng) -> tuple:
    """Return REASONING_TYPES in an order shuffled by the given
    random.Random instance (mirrors `type_definitions.order_randomized`
    exactly — pre-reg §2's per-item order-randomization applies to both
    arms)."""
    items = list(REASONING_TYPES)
    rng.shuffle(items)
    return tuple(items)
