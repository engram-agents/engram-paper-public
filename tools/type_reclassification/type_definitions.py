"""Verbatim quote_type schema text, extracted from the production tool
schema — NOT re-worded, NOT enriched with prose the production schema
doesn't actually contain.

Source of truth: engram-alpha's server.py, engram_add_observation's
docstring (~line 1538 as of 2026-07-08, commit d874c5c). That docstring
gives quote_type ONLY as a bare enum list with no per-value definition —
confirmed by grep across the engram-alpha source tree; there is no richer
official prose for any quote_type value anywhere in the codebase. This is
intentional for the study: the judge must see exactly what a filing agent's
tool schema shows them, not a richer definition invented for this study
(that would test something other than the actual filing-time information
asymmetry). If the production docstring is ever enriched with real
per-value prose, this file should be re-pulled to match — do not hand-write
richer definitions here.

Confidence values are NOT part of what's shown to the judge (confidence is
the thing being withheld) — they're recorded here only as provenance/
citation for where each name's base rate lives in the production schema
(engram_confidence.py CONFIDENCE_MAP), so this module stays traceable to
source without leaking the mapping into judge-facing text.
"""

from __future__ import annotations

# (name, verbatim-schema-description) — order here is NOT presentation
# order; see order_randomized() below, which the judge-prompt builder must
# use instead of iterating this list directly.
QUOTE_TYPES = (
    "hard_data",
    "official_statement",
    "attributed_analysis",
    "counterfactual_inference",
    "unnamed_source",
    "personal_communication",
    "editorial",
)

# The production schema (server.py engram_add_observation docstring) gives
# these as a bare comma-separated enum list with NO per-value prose. That is
# reproduced here verbatim as a single joined string — not expanded, not
# split into invented per-value sentences, per this module's docstring.
VERBATIM_QUOTE_TYPE_SCHEMA_TEXT = (
    "quote_type (str, required): One of: hard_data, official_statement, "
    "attributed_analysis, counterfactual_inference, unnamed_source, "
    "personal_communication, editorial."
)


def order_randomized(rng) -> tuple:
    """Return QUOTE_TYPES in an order shuffled by the given random.Random
    instance (pre-reg §2: 'Definitions order-randomized per item').

    Caller owns the RNG so packet-to-packet randomization is seeded and
    reproducible (e.g. seed derived from packet_id), not global-random.
    """
    items = list(QUOTE_TYPES)
    rng.shuffle(items)
    return tuple(items)
