"""Track-(b) observation-arm redaction: an outcome-vocabulary + author-id
screen LAYERED ON TOP of `tools.compression_fidelity.redact`'s existing
confidence/quote_type/reasoning_type/node-id-citation screen.

**Import-reuse decision (flagged per the coder-fairy spec's "note which you
chose and why").** This module IMPORTS `compression_fidelity.redact.screen_text`
(plus its `RedactionHit` dataclass and `REDACTED_TOKEN` constant) rather than
copy-pasting the whole seven-pass implementation. Both packages live in the
SAME repo (engram-paper) — the cross-REPO fragility concern that made
`compression_fidelity/constants.py` choose vendoring-over-import (engram-alpha
vs engram-paper: a different repo that may not be checked out alongside on
every machine, per that file's own docstring) does not apply to a same-repo
sibling-package import. Reuse also means the confidence/quote_type/
reasoning_type/node-id withholding disciplines never drift out of sync
between whatever future arms/harnesses this repo grows.

`_merge_spans` is NOT imported (it's a `_`-prefixed, i.e. private, symbol in
the base module) — reimplemented locally instead (it's a small, generic,
self-contained span-merge utility; the fragile-cross-package-coupling risk
the spec calls out to weigh is about depending on another package's PRIVATE
internals, not its public `screen_text`/`RedactionHit`/`REDACTED_TOKEN`
surface).

**quote_type screening is already covered for ENUM VALUES — confirmed, not
duplicated here.** `compression_fidelity.redact._VOCAB_PATTERN` is built
from `CONFIDENCE_MAP.keys()` (== `VALID_QUOTE_TYPES`, `constants.py`) union
`REASONING_TYPES` union the confidence-constant names — so quote_type enum
VALUES (`hard_data`, `attributed_analysis`, etc.) are already withheld by
the base `screen_text()` call this module wraps on every invocation. No
separate enum-value pass is added here.

**A THIRD, NOT explicitly spec'd pass was added after direct testing
surfaced a real gap (flagged prominently, not silently expanded):** the
base module screens quote_type/reasoning_type ENUM VALUES, but NOT the
literal FIELD-NAME WORDS "quote_type" / "reasoning_type" /
"standpoint_author_id" themselves. This package's own withholding test
(`test_exported_frame_never_contains_withheld_fields`) caught this directly
— a fixture claim reading "...overrides the quote_type proxy" leaked the
bare word "quote_type" verbatim, because `screen_text("...quote_type...",
...)` on the UNMODIFIED base module returns the text UNCHANGED (confirmed:
`compression_fidelity.redact.screen_text` has no pattern that matches these
literal identifiers as bare words — only their enum-value/constant-name
forms). This is a genuine, not hypothetical, leak class in the same spirit
as the base module's own documented residual gaps (its "spelled-out
confidence phrasing" and "self-referential ENGRAM discourse" sections) —
see `_FIELD_NAME_PATTERN` below. Adding this pass is technically outside
the two passes the coder-fairy spec explicitly authorized (outcome
vocabulary + author-id), so it is called out here and in the handoff for
the parent to keep or revert; it was added rather than silently left as a
known-gap because pre-reg §2 names `quote_type`/`reasoning_type`/
`standpoint_author_id` explicitly as fields that must NEVER appear, and a
bare mention of the field NAME (as opposed to its value) is a strictly
narrower but still real instance of the same invariant.
"""

from __future__ import annotations

import re

from tools.compression_fidelity.redact import (
    REDACTED_TOKEN,
    RedactionHit,
    screen_text as _base_screen_text,
)

# ---------------------------------------------------------------------------
# Outcome vocabulary — resolution/retraction-status words that, if they leak
# into free text (claim / quoted_text), tell the judge the node's OUTCOME
# (explicitly withheld per pre-reg §2: "not... the outcome"). Five word
# families (retract / supersede / refute / resolve / contradict), each with
# its FULL surface-form set (base, 3rd-person, past, gerund, nominalization)
# — a prior version of this list covered these inconsistently (missing every
# gerund plus the bare base forms of "resolve"/"contradict") and a
# reviewer-fairy caught it leaking via direct regex probing, not just
# doc-inspection: "resolve"/"contradict" are literally ENGRAM's own
# edge-relation names, so an agent's claim/quoted_text discussing its own
# graph mechanics is a real, plausible leak vector, not a corner case.
#
# JUDGMENT CALL (flagged): deliberately does NOT include this package's own
# internal stratum labels "survived" / "excluded" / "unclassified".
# "survived" is ordinary English (would over-redact claim text far more
# aggressively than the ENGRAM-specific words above); "excluded" and
# "unclassified" are THIS harness's own analysis vocabulary, not something a
# filing agent would plausibly write into `claim`/`quoted_text` prose about
# the object-level world. If Borges/Kepler want the full outcome-label set
# screened symmetrically, this is the list to extend.
# ---------------------------------------------------------------------------

_OUTCOME_WORDS = (
    # retract family
    "retracted",
    "retraction",
    "retract",
    "retracts",
    "retracting",
    # supersede family
    "superseded",
    "supersedes",
    "supersede",
    "superseding",
    # refute family
    "refuted",
    "refutation",
    "refute",
    "refutes",
    "refuting",
    # resolve family (these are also ENGRAM's own edge-relation names —
    # exactly the kind of self-referential-discourse phrasing an agent's
    # claim/quoted_text is plausibly to contain, per the base module's own
    # documented residual-gap section; reviewer-fairy-caught omission,
    # confirmed leaking via direct regex probing before this fix)
    "resolved",
    "resolution",
    "resolve",
    "resolves",
    "resolving",
    "unresolved",
    "partially resolved",
    "partially_resolved",
    # contradict family
    "contradicted",
    "contradiction",
    "contradict",
    "contradicts",
    "contradicting",
)

_OUTCOME_VOCAB_PATTERN = re.compile(
    r"\b(?:"
    + "|".join(
        re.escape(w).replace(r"\ ", "[-_ ]+")
        for w in sorted(_OUTCOME_WORDS, key=len, reverse=True)
    )
    + r")\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Author-id pattern — mirrors engram_observation.py's `_STABLE_ID_RE`
# (~line 116: `^pn_\d+$|^[a-z][a-z0-9-]*:.+$`), the canonical
# standpoint_author_id ID-shape convention (an in-graph `pn_*` person node,
# OR a namespaced external-author string like `orcid:...` / `doi-author:...`
# / `domain:handle`). `_STABLE_ID_RE` is anchored (`^...$`) for whole-field
# validation; this pattern drops the anchors (word-boundaried instead) to
# find an author-id-SHAPED SUBSTRING embedded in free text.
#
# KNOWN OVER-REDACTION RISK (flagged — same fail-safe direction as
# compression_fidelity/redact.py's own documented judgment calls, e.g. its
# pass-4 "known_constant_bare_decimal" precision-for-recall tradeoff): the
# namespaced-id half of this pattern (`[a-z][a-z0-9-]*:\S+`) ALSO matches
# ordinary URL-scheme prefixes embedded in prose (e.g. "http://...",
# "doi:10.1234/..." used as an ordinary citation, not a standpoint_author_id
# leak). This errs toward MORE redaction of claim/quoted_text — the
# fail-safe direction for a hard withholding invariant — but is a real, not
# hypothetical, over-redaction compromise for any `quoted_text` that
# legitimately contains a bare URL or DOI citation.
# ---------------------------------------------------------------------------

_AUTHOR_ID_PATTERN = re.compile(
    r"\bpn_\d+\b|\b[a-z][a-z0-9-]*:[^\s,;)\]]+",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Field-NAME mention pattern (see module docstring's "THIRD, NOT explicitly
# spec'd pass" note) — the literal withheld FIELD NAMES themselves
# (`quote_type`, `reasoning_type`, `standpoint_author_id`), separator-
# flexible (`_`/`-`/space all match, case-insensitive) like the base
# module's own `_vocab_pattern` convention.
# ---------------------------------------------------------------------------

_FIELD_NAME_WORDS = ("quote_type", "reasoning_type", "standpoint_author_id")

_FIELD_NAME_PATTERN = re.compile(
    r"\b(?:" + "|".join(re.escape(w).replace("_", "[-_ ]+") for w in _FIELD_NAME_WORDS) + r")\b",
    re.IGNORECASE,
)


def _merge_spans(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Same merge-spans logic as `compression_fidelity.redact._merge_spans`
    — duplicated locally rather than importing a private (`_`-prefixed)
    symbol across packages (see module docstring's import-reuse note)."""
    if not spans:
        return []
    spans = sorted(spans)
    merged = [spans[0]]
    for start, end in spans[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def _extra_hits(text: str, node_id: str, field: str) -> list[RedactionHit]:
    hits: list[RedactionHit] = []
    for m in _OUTCOME_VOCAB_PATTERN.finditer(text):
        hits.append(RedactionHit(node_id, field, "outcome_vocab", m.group(0), m.start(), m.end()))
    for m in _AUTHOR_ID_PATTERN.finditer(text):
        hits.append(RedactionHit(node_id, field, "author_id", m.group(0), m.start(), m.end()))
    for m in _FIELD_NAME_PATTERN.finditer(text):
        hits.append(RedactionHit(node_id, field, "field_name_mention", m.group(0), m.start(), m.end()))
    return hits


def screen_text(text: str, node_id: str, field: str) -> tuple[str, list[RedactionHit]]:
    """Screen one free-text field: the full `compression_fidelity`
    confidence/quote_type/reasoning_type/node-id screen, PLUS this module's
    outcome-vocabulary + author-id passes.

    All hit offsets are local to `text` (this call's ORIGINAL input) — the
    new passes are run against `text` directly, never against the
    already-partially-redacted output of the base screen, so merging the
    base module's hits with this module's new hits and replacing spans in
    ONE pass over the original `text` never double-redacts or drifts
    offsets (the exact trap `compression_fidelity.redact.screen_text`'s own
    docstring warns never to fall into: "never re-run span logic against a
    concatenated/modified string using hits from a different text").
    """
    if not text:
        return text, []

    _, base_hits = _base_screen_text(text, node_id, field)
    extra_hits = _extra_hits(text, node_id, field)

    all_hits = list(base_hits) + extra_hits
    if not all_hits:
        return text, []

    spans = [(h.start, h.end) for h in all_hits]
    merged = _merge_spans(spans)
    out = []
    last = 0
    for s, e in merged:
        out.append(text[last:s])
        out.append(REDACTED_TOKEN)
        last = e
    out.append(text[last:])
    return "".join(out), all_hits
