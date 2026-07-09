"""Packet extraction (pre-reg §4 / §4.1) — builds the confidence-stripped,
source-class-label-stripped provenance packet a blind judge fairy reads.

Exact allowed fields, nothing else (§4):
    claim, quoted_text, interpretation (primary arm only),
    evidence.url / evidence.domain / evidence.title / evidence.source_date,
    and for derivations: the full premise structure as a screened reasoning
    tree (tree.py).

Explicitly withheld, at every level, including inside free text: computed
`confidence`, `quote_type` enum, `reasoning_type` enum (redact.py).

Judgment call (flagged in the handoff): the pre-reg's §4 sentence "the
filer's `interpretation` ... a recall-reader sees the interpretation on
inspect" is written about the sampled node under evaluation, and the
`§4.1` rendering enumeration for tree leaves lists only `claim` +
`quoted_text` + raw source fields for evidence leaves — no
`interpretation`. This module therefore includes `interpretation` ONLY on
the top-level sampled node (target), never on premise nodes inside a
reasoning tree, even in the primary (with-interpretation) arm. This keeps
packet size down and matches the leaf-rendering enumeration literally; an
alternative reading (interpretation on every node a judge could "inspect")
was rejected because §4.1's explicit field list for leaves does not
include it.

Two exclusion gates, both required outputs (by node ID, with reason):
    - >20% of a chain's text redacted -> excluded ("a gutted chain isn't a
      fair fixture").
    - packet exceeds the ~15k whitespace-token max-packet-size guard.

**`packet_id` is opaque, never the real ENGRAM node ID (reviewer-fairy
catch #1, fixed).** An earlier version of this harness wrote the real
node ID into both the packet's `packet_id` field and the served filename
— which defeats the pre-reg's §3 harness-isolation defense-in-depth: if
the judge's environment isolation ever fails even partially, a raw node
ID lets it directly call `engram_inspect(<id>)` and read the withheld
confidence/type. `cli.py` now generates an opaque serial (`sampling.
assign_packet_ids`) and passes it into `build_packet` as `packet_id`; the
`packet_id <-> real_node_id` mapping is recorded ONLY in the researcher-
side manifest, never in a packet file.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from . import db, redact, tree
from .constants import DERIVATION_TYPES, OBSERVATION_TYPES

MAX_PACKET_TOKENS = 15_000
MAX_CHAIN_REDACTION_FRACTION = 0.20


@dataclass
class PacketResult:
    packet_id: str
    node_id: str
    node_type: str
    arm: str  # "primary" | "without_interpretation"
    packet: Optional[dict]
    redaction_hits: list[redact.RedactionHit] = field(default_factory=list)
    excluded: bool = False
    exclusion_reason: Optional[str] = None
    token_count: int = 0
    chain_redaction_fraction: float = 0.0


def _token_count(packet: dict) -> int:
    """Rough whitespace-token proxy (pre-reg: 'no need for a real
    tokenizer'). Counts every string value in the packet."""
    total = 0

    def walk(v):
        nonlocal total
        if isinstance(v, str):
            total += len(v.split())
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)

    walk(packet)
    return total


def build_packet(
    cache: tree.GraphCache,
    node: db.NodeRow,
    packet_id: str,
    include_interpretation: bool,
) -> PacketResult:
    """`packet_id` MUST be an opaque identifier (e.g. "pkt_00001"), never
    the real ENGRAM node ID — see `sampling.assign_packet_ids`. This
    function trusts its caller on that; it does not itself derive or
    validate the opaque mapping (that's the caller's/manifest's job, per
    the reviewer-fairy fix: the raw node ID must never appear in a served
    packet file, only in the researcher-side manifest)."""
    arm = "primary" if include_interpretation else "without_interpretation"
    hits: list[redact.RedactionHit] = []
    # Redacted-char / total-char accumulators for the >20%-gutted-chain
    # check. Each screen() call below reports its OWN correctly-scoped
    # redacted-char-count (via redact.redacted_char_count, computed from
    # that exact call's text + hits) rather than reusing hit offsets
    # against a later concatenation — see redact.py/tree.py docstrings for
    # why the earlier concatenation approach undercounted (bug #4).
    gut_totals = {"redacted": 0, "total": 0}

    def screen(text, fieldname):
        if not text:
            return ""
        screened, h = redact.screen_text(text, node.id, fieldname)
        hits.extend(h)
        gut_totals["redacted"] += redact.redacted_char_count(text, h)
        gut_totals["total"] += len(text)
        return screened

    def screen_evidence_field(text, fieldname):
        # Reviewer-fairy round-2 catch: evidence fields are served VERBATIM
        # per §4, but an agent-authored title/URL can itself cite another
        # node's ID (e.g. a forum-thread title naming "cj_0005") -- narrow
        # screen for JUST the node-ID-citation channel, not the full
        # confidence/percent/vocab pipeline, so genuinely verbatim content
        # (a percentage or decimal actually present in a source title) is
        # not over-redacted.
        if not text:
            return text
        screened, h = redact.screen_node_id_citations(text, node.id, fieldname)
        hits.extend(h)
        return screened

    if node.type in OBSERVATION_TYPES:
        claim = screen(node.claim or "", "claim")
        quoted = screen(node.quoted_text or "", "quoted_text")
        interp = screen(node.interpretation or "", "interpretation") if include_interpretation else None
        ev = cache.evidence(node.evidence_id) if node.evidence_id else {
            "url": None, "domain": None, "title": None, "source_date": None
        }
        packet = {
            "packet_id": packet_id,
            "node_type": "observation",
            "claim": claim,
            "quoted_text": quoted,
            "evidence": {
                "url": screen_evidence_field(ev.get("url"), "evidence.url"),
                "domain": screen_evidence_field(ev.get("domain"), "evidence.domain"),
                "title": screen_evidence_field(ev.get("title"), "evidence.title"),
                "source_date": ev.get("source_date"),
            },
        }
        if include_interpretation:
            packet["interpretation"] = interp

        # Gutting check scoped to all free text on an observation packet
        # (claim + quoted_text + interpretation) — the pre-reg's 20%-rule
        # is framed around a "chain", but the same "not a fair fixture"
        # concern applies to any packet whose free text is mostly
        # redacted. Judgment call (flagged in handoff): extending the rule
        # to observation packets, not just derivation logical_chains.
        chain_fraction = (
            gut_totals["redacted"] / gut_totals["total"] if gut_totals["total"] else 0.0
        )

    elif node.type in DERIVATION_TYPES:
        tree_result = tree.render_reasoning_tree(cache, node)
        hits.extend(tree_result.redaction_hits)
        # Reuse the tree's already-screened target claim for the top-level
        # "claim" convenience field, rather than re-screening node.claim a
        # second time (which would double-log the same redaction hits).
        claim = tree_result.target_claim_screened
        interp = screen(node.interpretation or "", "interpretation") if include_interpretation else None
        packet = {
            "packet_id": packet_id,
            "node_type": "derivation",
            "claim": claim,
            "reasoning_tree": tree_result.markdown,
        }
        if include_interpretation:
            packet["interpretation"] = interp

        # The chain-fraction check for derivations is scoped to
        # `logical_chain` text ONLY (the tree's own accumulator, which
        # already excludes the top-level `interpretation` screen() call
        # above) — not the `gut_totals` accumulator, which would also
        # include the (unrelated) interpretation field for this branch.
        chain_fraction = (
            tree_result.chain_redacted_chars / tree_result.chain_total_chars
            if tree_result.chain_total_chars else 0.0
        )
    else:
        raise ValueError(f"unexpected node type in packet extraction: {node.type}")

    token_count = _token_count(packet)

    excluded = False
    reason = None
    if chain_fraction > MAX_CHAIN_REDACTION_FRACTION:
        excluded = True
        reason = (
            f">20% chain redacted ({chain_fraction:.1%}) — gutted chain not a fair fixture"
        )
    elif token_count > MAX_PACKET_TOKENS:
        excluded = True
        reason = f"packet exceeds max-size guard ({token_count} > {MAX_PACKET_TOKENS} tokens)"

    return PacketResult(
        packet_id=packet_id,
        node_id=node.id,
        node_type=node.type,
        arm=arm,
        packet=None if excluded else packet,
        redaction_hits=hits,
        excluded=excluded,
        exclusion_reason=reason,
        token_count=token_count,
        chain_redaction_fraction=chain_fraction,
    )
