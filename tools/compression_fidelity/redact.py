"""The metadata screen (pre-reg §4.1 / §4): confidence values, `quote_type`
and `reasoning_type` enum vocabulary must not appear ANYWHERE in a served
packet, including inside free text (`claim`, `quoted_text`, `interpretation`,
`logical_chain`).

Seven redaction passes, applied to every free-text field of every node
rendered into a packet:

1. **Conf-prefixed decimal numbers** — `conf(idence|ident)?[ :=~≈]*[01]?\\.\\d+`
   (e.g. "conf 0.95", "confidence: 0.4", "conf~0.70").
2. **Vocabulary hits** — the literal `quote_type` and `reasoning_type` enum
   words (flexible separators: `_`, `-`, or space all match, case-
   insensitive), e.g. "attributed-analysis", "deductive_modus_ponens",
   "Inductive Generalization" — PLUS the confidence-system's named Python
   constants (`CONJECTURE_CONFIDENCE_DEFAULT`, `REASONING_DISCOUNT`, etc.
   — see judgment-call note below).
3. **Proximity bare-decimals** — a bare `0.XX` / `1.0` number that is NOT
   already consumed by pass 1, but sits within a short window of a pass-1
   or pass-2 hit (or a bare "conf"/"confidence"/"confident" mention), gets
   redacted too. This is the pre-reg's "bare anchor values in metadata
   context" clause — real graph text does exactly this ("...ceiling
   (0.70)" right after "attributed-analysis", or "min(0.70, 0.95, 0.95) =
   0.70" a sentence after an earlier "conf 0.70" mention in the same chain).
4. **Known-constant bare-decimals (unconditional, no proximity gate)** — a
   bare number whose value, rounded to 3 decimals, exactly matches one of
   the confidence-system's known constants (every `CONFIDENCE_MAP`,
   `REASONING_DISCOUNT`, `ABDUCTIVE_CONFIDENCE_CAP`, predictive/conjecture
   bound, or introspective-discount-derived value) is redacted regardless
   of what's nearby. Added after the initial smoke test surfaced two real
   misses passes 1-3 didn't catch: "already discounted x0.95" (no "conf"
   word, no quote_type/reasoning_type word nearby — just the bare
   introspective-discount value) and "F-S ... = 0.15 ...
   CONJECTURE_CONFIDENCE_DEFAULT (0.40)" (a node discussing ENGRAM's own
   confidence constants by name).
5. **Node-ID citations** — a bare ENGRAM node ID (`ob_0004`, `dv_0021`,
   `ax_0007`, ...) directly names that cited node's TYPE — a
   `quote_type`-adjacent leak the reviewer-fairy pass caught (174/276
   primary packets, 3163 citations, in the first delivered version of this
   harness). ENGRAM's own authoring convention cites node IDs inline in
   `logical_chain`/`interpretation`/`claim` prose ("ob_0004 records
   that..."), so this is common, not an edge case. Matched against the
   full node-ID prefix vocabulary (`constants.NODE_ID_PREFIXES`), not just
   a subset — a partial prefix list would silently under-redact whichever
   type it omitted.
6. **Conf-percent phrasing** — "95% confident", "conf ~ 95%", "confidence
   is about 95 percent" — added because passes 1-4 all require a literal
   `.` + digits and never matched percentage or "X percent" phrasing
   (reviewer-fairy catch #3). Two directional patterns (conf-word-then-
   percent, percent-then-conf-word) since natural prose uses both orders.
7. **Proximity bare-percent** — mirrors pass 3 for percentage form: a bare
   `NN%` / `NN percent` not already consumed, within the same proximity
   window of a conf-word or vocab hit.

**Residual gap, deliberately NOT implemented (flagged for Borges/Kepler,
not silently left out):** spelled-out confidence phrasing ("point nine
five", "nine five percent confident") has no pattern here. A reliable
spelled-out-number lexicon is materially harder to get right (number-word
grammar, false-positive risk against ordinary spelled-out numbers in
unrelated context) and was not attempted. If ENGRAM authoring practice
ever produces spelled-out confidence mentions in `logical_chain`/
`interpretation` text, they will leak through this screen undetected.
Recommend a targeted grep-based audit of the served packets for this
phrasing before the real study run, rather than trusting this gap is
empty by construction.

**A second residual gap, discussed and deliberately left open (Borges,
2026-07-08):** a bare-INTEGER confidence near a conf-word with no decimal
point and no percent unit ("confidence 90", "conf around 90") is not
caught by any pass here -- pass 1 requires `[01]?\\.\\d+` (a decimal), the
bare-decimal passes (3/4) require a decimal point too, and the percent
passes (6/7) require `%`/"percent". Deliberately not patched: ENGRAM's
schema always stores/renders confidence as a 0-1 float (written "0.90")
or a percentage ("90%"), never a bare 0-100 integer, so this form is
believed absent from the real target corpus. More importantly, ADDING an
unconditioned bare-integer-near-conf-word pattern would carry a much
HIGHER false-positive cost than the leak risk it closes -- ordinary prose
routinely puts small integers near "confident"/"confidence" for unrelated
reasons ("confident 2026 will be a good year", "confidence grew over 3
years") in a way percentages and decimals essentially never do. If a
future audit of the real corpus finds this form actually occurring,
revisit with a narrower, more context-specific pattern rather than a
blanket bare-integer match.

**A DEEPER residual gap, found by direct verification against a real
graph, not just theorized (post-round-2-fix, Luria's own pass): a graph
that discusses ENGRAM's own confidence/calibration system extensively in
free-form prose leaks confidence-adjacent numbers with NO bounded regex
list able to catch all of them.** Two concrete instances fixed here
(underscore-broken word-boundary on "mean_conf=0.XX"-style identifiers;
missing plural "confidences"), but a further scan turned up a
qualitatively different, NOT further pattern-patched, class:

- Bare parenthetical confidence citations with no trigger word at all —
  "(0.937): Kant constitutive Class B..." (an inline "(conf): claim"
  citation convention some ENGRAM authoring uses) leaks the actual
  confidence value with nothing regex-matchable nearby to anchor on.
- Sentence-form confidence statements without an anchor word — "the
  server computed 0.95", "correlated corroborating frameworks ≈ 0.82" —
  natural language can express "here is a confidence-shaped number" in
  effectively unbounded ways that never use "conf"/"confidence" at all.
- Non-confidence numeric axes ENGRAM discusses alongside confidence in
  its own design discourse — Falsification-Sensitivity ("F-S=0.15",
  "F-S ≈ 0.90") is a DIFFERENT metric from the withheld `confidence`
  field, so its bare mentions are arguably out of scope for this
  screen's specific mandate, but they demonstrate the same underlying
  problem: this graph's content is unusually self-referential about its
  own scoring systems, and any fixed vocabulary/pattern list will always
  be one design-discussion node behind.

This is NOT a "one more regex pass" problem — it's a structural property
of a graph whose content is substantially ABOUT the thing being withheld.
**Recommendation for Borges/Kepler, not attempted here:** consider
whether nodes whose `claim`/`logical_chain` is itself meta-discourse
about ENGRAM's confidence/calibration machinery should be excluded from
the sampling frame entirely (they're a different kind of "meta" node
than an ordinary object-level claim, and are also the hardest to blind
by construction) — rather than relying on redaction alone to make them
safe to serve. Flagging this explicitly rather than claiming the
redaction screen is complete; it demonstrably is not, for this class.

Judgment calls (flagged in the handoff, all extensions beyond the
pre-reg's literal wording, all erring toward MORE redaction — the
fail-safe direction for a hard invariant the pre-reg calls out as a "hard
test assertion"):

  (a) Pass 2 also matches the confidence-system's constant NAMES (e.g.
      `CONJECTURE_CONFIDENCE_DEFAULT`), not just the `quote_type` /
      `reasoning_type` enum vocabulary the pre-reg names explicitly.
  (b) Pass 4 drops the proximity requirement entirely for values that
      EXACTLY match a known confidence constant. **Explicit limitation
      (reviewer-fairy catch, flagged for §10):** this means "served
      VERBATIM" is not strictly true for a `quoted_text` that happens to
      contain one of these ~15 common values for an UNRELATED reason —
      e.g. a Pearson correlation "r=0.70", a dollar amount "$0.85
      million", a probability estimate "p=0.95" in someone else's quoted
      words. This is an intentional precision-for-recall trade (an actual
      confidence leak is worse than an over-redacted unrelated number,
      and the >20%-gutted-chain exclusion catches the worst cases) but it
      is a real, not hypothetical, verbatim-quotation compromise that
      Borges/Kepler should weigh explicitly, not discover later.
  (c) Pass 6 does NOT add an unconditional (non-proximity-gated) bare
      percent match the way pass 4 does for decimals — bare percentages
      ("50% of respondents...") are far more common in ordinary prose
      than bare decimals matching a confidence anchor, so an
      unconditional match would over-redact heavily. Percent-form
      redaction is proximity-gated only (passes 6-7).

Redactions are logged (node id, field, original span text, category) —
the log ships alongside the packets per the pre-reg/spec, not discarded.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .constants import (
    ABDUCTIVE_CONFIDENCE_CAP,
    CONFIDENCE_MAP,
    CONJECTURE_CONFIDENCE_DEFAULT,
    CONJECTURE_CONFIDENCE_MAX,
    CONJECTURE_CONFIDENCE_MIN,
    NODE_ID_PREFIXES,
    PREDICTIVE_CONFIDENCE_CAP,
    REASONING_DISCOUNT,
    REASONING_TYPES,
    SOURCE_CLASS_CONFIDENCE_DISCOUNT,
)

REDACTED_TOKEN = "[metadata redacted]"

# "confident"/"confidences" (plural) included alongside "conf"/"confidence"
# — natural prose uses all these forms ("I am 95% confident", "average
# confidences 0.774/0.690/..."), and a plain `conf(?:idence)?\b`
# word-boundary pattern matches neither "confident" nor plural
# "confidences" (the trailing boundary fails mid-word). Found via direct
# verification: "average confidences 0.774/0.690/..." leaked both bare
# values unredacted because "confidences" never registered as an anchor.
_CONF_WORD = r"conf(?:idences?|ident)?"

# Left boundary for _CONF_WORD: a plain `\b` REQUIRES the preceding char to
# be a non-word char, which FAILS to match "conf" when it's preceded by an
# underscore (e.g. "mean_conf=0.690", "avg_conf" — snake_case identifier
# style, common in ENGRAM's own health-report/diagnostic prose). Found via
# direct verification against a real graph after the round-2 fix: several
# "identifier_conf=0.XX" values leaked completely unredacted because `_` is
# a word character, so no `\b` exists between "_" and "c". A negative
# lookbehind that only excludes an actual LETTER (not `_`/digit) fixes this
# without introducing new false positives — the trailing `\b` (unchanged)
# already prevents "conf" from matching as a prefix inside "confirmed" /
# "configuration" / "confetti", so widening only the LEFT side is safe.
_CONF_LEFT = r"(?<![a-zA-Z])"

_CONF_PATTERN = re.compile(
    rf"{_CONF_LEFT}{_CONF_WORD}\b[ :=~≈_]{{0,4}}[01]?\.\d+",
    re.IGNORECASE,
)

_BARE_DECIMAL_PATTERN = re.compile(r"(?<![0-9.])[01]?\.\d+(?![0-9.])")

_BARE_CONF_WORD_PATTERN = re.compile(rf"{_CONF_LEFT}{_CONF_WORD}\b", re.IGNORECASE)

# Proximity window (characters) for the bare-decimal/percent-near-a-
# withheld-word rule.
_PROXIMITY_WINDOW = 120

_PERCENT_UNIT = r"(?:%|percent)"

# Reviewer-fairy catch (2026-07-08, 3rd round -- the pass-7 fix's own
# review): the digit component `\d{1,3}` cannot span a decimal point, so a
# genuinely fractional percentage (e.g. "90.25%" -- exactly the
# introspective-discount-product form this module's own docstring already
# flags as realistic: hard_data 0.95 x 0.95 = 0.9025 = "90.25%") was never
# matched as ONE clean span by ANY of the three percent patterns below.
# Pass 6 could still accidentally grab just the post-decimal digits ("25%")
# when a conf-word sat within its ~15-char window, but that's a partial,
# incorrect match that leaves "90." fully visible -- reconstructable
# alongside the redacted "[metadata redacted]" fragment. Fixed by widening
# the digit component to optionally include a decimal fraction; used
# everywhere a percent NUMBER is matched (all three patterns share this
# fragment now, not just the pass-7 one this review targeted, since the
# same gap existed in all of them).
_PERCENT_NUMBER = r"\d{1,3}(?:\.\d+)?"

# Conf-word ... NN% / NN percent (either order — natural prose uses both:
# "confidence is about 95 percent" vs "95% confident").
_CONF_PERCENT_FORWARD = re.compile(
    rf"{_CONF_LEFT}{_CONF_WORD}\b.{{0,15}}?{_PERCENT_NUMBER}\s*{_PERCENT_UNIT}",
    re.IGNORECASE | re.DOTALL,
)
_CONF_PERCENT_BACKWARD = re.compile(
    rf"{_PERCENT_NUMBER}\s*{_PERCENT_UNIT}.{{0,15}}?{_CONF_LEFT}{_CONF_WORD}\b",
    re.IGNORECASE | re.DOTALL,
)

# New-test-suite catch (2026-07-08, first pytest run this module ever had):
# a trailing `\b` right after `{_PERCENT_UNIT}` is broken for the "%" symbol
# form. `%` is a non-word character, so `\b` requires the NEXT character to
# be a word character -- but a percent sign in real prose is essentially
# ALWAYS followed by whitespace or punctuation (also non-word), meaning
# `\b` after "%" almost never matches. Concretely: `\d{1,3}\s*%\b` matches
# "40%" only when immediately followed by a letter/digit with no space
# (e.g. the pathological "40%word"), which never occurs in real ENGRAM
# prose -- so this pattern was SILENTLY DEAD for the overwhelmingly common
# "NN%" form and only ever matched the word form "NN percent" (where the
# trailing `\b` after the letter "t" behaves normally). This is a genuine,
# live confidence-leak vector in the shipped screen: a bare percentage near
# a confidence anchor (e.g. "conf... 40%" separated by more than pass 6's
# adjacency window) silently escaped pass 7 entirely. Fixed with a
# unit-specific trailing check: `%` uses a negative lookahead for a
# following word character (a percent sign is not itself a word char, so
# only an immediately-adjacent alnum, never whitespace/punctuation, would
# be a real false-positive risk); "percent" keeps its normal `\b`.
_PERCENT_UNIT_TRAILING = r"(?:%(?!\w)|percent\b)"

_BARE_PERCENT_PATTERN = re.compile(
    rf"(?<![0-9.]){_PERCENT_NUMBER}\s*{_PERCENT_UNIT_TRAILING}", re.IGNORECASE
)

# Node-ID citations (e.g. "ob_0004", "dv_0021") — directly reveal the cited
# node's TYPE, a quote_type-adjacent leak. Built from the FULL node-ID
# prefix vocabulary (constants.NODE_ID_PREFIXES), not a subset.
_NODE_ID_PATTERN = re.compile(
    r"\b(?:" + "|".join(NODE_ID_PREFIXES) + r")_\d{2,6}\b",
    re.IGNORECASE,
)

# The confidence-system constant NAMES (not just enum values) — pass 2 also
# redacts these when they appear in free text (judgment call (a) above).
_CONSTANT_NAMES = (
    "CONFIDENCE_MAP",
    "REASONING_CLASS",
    "REASONING_DISCOUNT",
    "REASONING_TYPES",
    "ABDUCTIVE_CONFIDENCE_CAP",
    "PREDICTIVE_CONFIDENCE_CAP",
    "CONJECTURE_CONFIDENCE_DEFAULT",
    "CONJECTURE_CONFIDENCE_MIN",
    "CONJECTURE_CONFIDENCE_MAX",
    "SOURCE_CLASS_CONFIDENCE_DISCOUNT",
)


def _known_constant_values() -> set:
    """Every numeric value the confidence system can produce, rounded to 3
    decimals — the "known anchor values" pass-4 matches unconditionally."""
    vals = set(CONFIDENCE_MAP.values())
    vals |= set(REASONING_DISCOUNT.values())
    vals |= set(ABDUCTIVE_CONFIDENCE_CAP.values())
    vals |= {PREDICTIVE_CONFIDENCE_CAP, CONJECTURE_CONFIDENCE_DEFAULT,
             CONJECTURE_CONFIDENCE_MIN, CONJECTURE_CONFIDENCE_MAX, 1.0}
    # introspective-discount-derived products (e.g. hard_data x 0.95 = 0.9025)
    introspective = SOURCE_CLASS_CONFIDENCE_DISCOUNT.get("introspective")
    if introspective:
        vals |= {round(v * introspective, 3) for v in CONFIDENCE_MAP.values()}
    return {round(v, 3) for v in vals}


_KNOWN_CONSTANT_VALUES = _known_constant_values()


def _vocab_pattern() -> re.Pattern:
    words = sorted(
        set(CONFIDENCE_MAP.keys()) | REASONING_TYPES | set(_CONSTANT_NAMES),
        key=len,
        reverse=True,
    )
    # allow '_', '-', or ' ' interchangeably between sub-words. re.escape()
    # does not escape '_' (not a regex metacharacter), so replace the plain
    # underscore after escaping, not the escaped form.
    alternatives = [re.escape(w).replace("_", "[-_ ]+") for w in words]
    pattern = r"\b(?:" + "|".join(alternatives) + r")\b"
    return re.compile(pattern, re.IGNORECASE)


_VOCAB_PATTERN = _vocab_pattern()


@dataclass
class RedactionHit:
    node_id: str
    field: str
    category: str
    # one of: "conf_number" | "vocab" | "proximity_bare_decimal" |
    # "known_constant_bare_decimal" | "node_id_citation" |
    # "conf_percent" | "proximity_bare_percent"
    matched_text: str
    start: int
    end: int


def _merge_spans(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
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


def screen_node_id_citations(text: str, node_id: str, field: str) -> tuple[str, list[RedactionHit]]:
    """Screen ONLY for embedded ENGRAM node-ID citations (e.g. "ob_0004") --
    none of the confidence-number / percent / vocab / bare-decimal passes.

    Reviewer-fairy round-2 catch: `evidence.url/domain/title/source_date`
    are served verbatim per the pre-reg's §4 mandate (the judge must see
    the RAW source identity, not our relabeled gloss of it) -- but that
    mandate is about not relabeling source KIND, not about tolerating
    ENGRAM's own node-ID citations bleeding through an agent-authored
    title (e.g. a forum-thread title like "...cj_0005 cross-lineage test,
    Mira raw reply via Borges" directly names a conjecture node). Running
    the FULL `screen_text` pipeline on these fields would over-redact
    genuinely verbatim content (a percentage or decimal that is actually
    IN a source title/URL is not a confidence-system leak); only the
    node-ID-citation channel is the ENGRAM-internal leak that needs
    narrowing here. Same merge/replace mechanics as `screen_text`, restricted
    to `_NODE_ID_PATTERN`.
    """
    if not text:
        return text, []

    hits: list[RedactionHit] = []
    spans: list[tuple[int, int]] = []

    for m in _NODE_ID_PATTERN.finditer(text):
        spans.append((m.start(), m.end()))
        hits.append(RedactionHit(node_id, field, "node_id_citation", m.group(0), m.start(), m.end()))

    if not hits:
        return text, []

    merged = _merge_spans(spans)
    out = []
    last = 0
    for s, e in merged:
        out.append(text[last:s])
        out.append(REDACTED_TOKEN)
        last = e
    out.append(text[last:])
    return "".join(out), hits


def screen_text(text: str, node_id: str, field: str) -> tuple[str, list[RedactionHit]]:
    """Screen one free-text field. Returns (screened_text, hits).

    `hits[i].start`/`.end` are offsets LOCAL to `text` (this call's input),
    NOT offsets into any larger concatenation a caller may build from
    multiple `screen_text` calls. Callers that need a redacted-character
    COUNT across multiple calls must accumulate `redacted_char_count(text,
    hits)` per call — never re-run span logic against a concatenated
    string using hits from different calls (this was bug #4 in the first
    delivered version: `redaction_fraction` was called with locally-scoped
    hits against a globally-concatenated string, silently undercounting
    whenever two premises' texts had overlapping local offsets).
    """
    if not text:
        return text, []

    hits: list[RedactionHit] = []
    spans: list[tuple[int, int]] = []

    for m in _CONF_PATTERN.finditer(text):
        spans.append((m.start(), m.end()))
        hits.append(RedactionHit(node_id, field, "conf_number", m.group(0), m.start(), m.end()))

    for pat in (_CONF_PERCENT_FORWARD, _CONF_PERCENT_BACKWARD):
        for m in pat.finditer(text):
            spans.append((m.start(), m.end()))
            hits.append(RedactionHit(node_id, field, "conf_percent", m.group(0), m.start(), m.end()))

    for m in _NODE_ID_PATTERN.finditer(text):
        spans.append((m.start(), m.end()))
        hits.append(RedactionHit(node_id, field, "node_id_citation", m.group(0), m.start(), m.end()))

    for m in _VOCAB_PATTERN.finditer(text):
        spans.append((m.start(), m.end()))
        hits.append(RedactionHit(node_id, field, "vocab", m.group(0), m.start(), m.end()))

    # Anchor positions for the proximity rules: every "conf"/"confidence"/
    # "confident" mention (bare or already-consumed by pass 1) plus every
    # vocab hit.
    anchor_positions: list[int] = [m.start() for m in _BARE_CONF_WORD_PATTERN.finditer(text)]
    anchor_positions += [h.start for h in hits if h.category == "vocab"]

    def already_consumed(s: int, e: int) -> bool:
        merged = _merge_spans(spans)
        return any(cs <= s and e <= ce for cs, ce in merged)

    for m in _BARE_DECIMAL_PATTERN.finditer(text):
        s, e = m.start(), m.end()
        if already_consumed(s, e):
            continue
        try:
            value = round(float(m.group(0)), 3)
        except ValueError:
            value = None

        if value is not None and value in _KNOWN_CONSTANT_VALUES:
            spans.append((s, e))
            hits.append(
                RedactionHit(node_id, field, "known_constant_bare_decimal", m.group(0), s, e)
            )
        elif any(abs(s - a) <= _PROXIMITY_WINDOW for a in anchor_positions):
            spans.append((s, e))
            hits.append(
                RedactionHit(node_id, field, "proximity_bare_decimal", m.group(0), s, e)
            )

    for m in _BARE_PERCENT_PATTERN.finditer(text):
        s, e = m.start(), m.end()
        if already_consumed(s, e):
            continue
        if any(abs(s - a) <= _PROXIMITY_WINDOW for a in anchor_positions):
            spans.append((s, e))
            hits.append(
                RedactionHit(node_id, field, "proximity_bare_percent", m.group(0), s, e)
            )

    if not hits:
        return text, []

    merged = _merge_spans(spans)
    out = []
    last = 0
    for s, e in merged:
        out.append(text[last:s])
        out.append(REDACTED_TOKEN)
        last = e
    out.append(text[last:])
    return "".join(out), hits


def redacted_char_count(original: str, hits: list[RedactionHit]) -> int:
    """Count of `original`'s characters covered by `hits` (merged,
    non-overlapping). `hits` MUST be the hits returned by the single
    `screen_text(original, ...)` call that produced them — never hits
    accumulated from a different text (see `screen_text`'s docstring)."""
    if not original or not hits:
        return 0
    spans = _merge_spans([(h.start, h.end) for h in hits])
    return sum(e - s for s, e in spans)


def redaction_fraction(original: str, hits: list[RedactionHit]) -> float:
    """Fraction of `original`'s characters covered by redaction spans.
    Same single-call-provenance requirement as `redacted_char_count` — this
    is a convenience wrapper for the common single-field case, not a
    general aggregator across multiple screened fields/nodes. Callers
    aggregating across multiple `screen_text` calls (e.g. a whole
    reasoning tree's worth of `logical_chain` fields) must sum
    `redacted_char_count(...)` and `len(text)` per call instead — see
    `tree.py`'s `chain_redacted_chars`/`chain_total_chars` accumulators."""
    if not original:
        return 0.0
    return redacted_char_count(original, hits) / len(original)
