"""Reasoning-tree rendering (pre-reg §4.1): numbered-outline, depth-first
markdown. One block per node:

    [TARGET] <claim>
    reasoning: <logical_chain, post-screen>
        [P1] <claim>
        reasoning: <logical_chain, post-screen>
            [P1.1] ...
        [P2] <claim>
        ...
        [EVIDENCE for P1.1] <claim>
        quoted_text: "..."
        source: {url, domain, title, source_date}

No box-drawing characters — indentation + numbering only (ASCII-safe).

Shared premises (the DAG case): rendered FULLY at first occurrence; later
occurrences become a back-reference: `[P2.1] -- same node as [P1.2]`
(load-bearing per the pre-reg — keeps diamond-shaped provenance from
exploding packet size, and is cycle-safe by construction since a node is
only ever expanded once).

Leaf handling: a premise that is NOT itself a derivation is a leaf.
    - Observation premise -> `[EVIDENCE for <label>]`, carrying its own
      `claim` + `quoted_text` + raw evidence fields (source_url/domain/
      title/source_date). No `interpretation` (see packet.py docstring for
      why interpretation is target-only, a judgment call flagged there).
    - Non-observation, non-derivation premise (axiom / conjecture / lesson
      cited directly as a supporting id — confirmed present in the smoke
      graph) has no quoted_text/evidence_id. This case is NOT covered by
      the pre-reg's leaf-rendering example (which only describes
      "[EVIDENCE for ...]" leaves backed by quoted_text). Judgment call
      (flagged in the handoff): rendered as a generic `[SUPPORT for
      <label>]` leaf carrying just its own `claim` text, so the tree stays
      legible and complete rather than silently dropping the premise or
      forcing it into the evidence-leaf shape it doesn't have the fields
      for.
    - A `derives_from` edge pointing at a node ID not found in the DB
      (shouldn't happen in a consistent graph, but handled defensively) is
      rendered WITHOUT the raw node ID (just "-- premise not found") — an
      earlier version of this module interpolated the raw `pid` into this
      message, which leaked an un-redacted node ID the same way node-ID
      citations in prose do (reviewer-fairy catch #2b).

Every claim/quoted_text/interpretation/logical_chain field touched here is
run through `redact.screen_text` before rendering, and every redaction hit
is collected and returned to the caller (packet.py aggregates it into the
redaction log and the >20%-gutted-chain exclusion check).

**Redaction-fraction accounting (reviewer-fairy catch #4, fixed):** each
node's text is screened via its OWN `redact.screen_text` call, which
returns hit offsets LOCAL to that single node's text. An earlier version
of this module concatenated every node's raw chain text into one string
and then re-checked the (locally-scoped) hit offsets against that
concatenation — a provable undercount whenever two different premises'
local offsets happened to overlap (e.g. two independent 9-char and 15-char
redactions in different premises, 24 true redacted chars, could report as
few as 15 depending on offset collision). This module now accumulates
`chain_redacted_chars` / `chain_total_chars` per screen() call via
`redact.redacted_char_count` (which is always scoped correctly, since it's
computed from the SAME call's original text + hits) and exposes the
accumulated totals directly — the caller never reconstructs a fraction
from a concatenated string + hits collected across multiple calls.

**Gutted-fraction SCOPE (colleague-review catch, Borges's breadth fairy,
2026-07-09): `chain_redacted_chars`/`chain_total_chars` accumulate from
EVERY tree-rendered field, not just `logical_chain`.** An earlier version
of this module set `is_chain=True` only on the `logical_chain` screen()
call — a derivation's own `claim` (target + every derivation premise), an
observation premise's `claim`/`quoted_text`, and a non-obs/non-deriv
premise's `claim` (the `[SUPPORT for ...]` leaf) were all screened but
never counted toward the fraction. Two real consequences: (1) a
derivation whose `claim`/premise-`claim`s/`quoted_text` are almost
entirely confidence-leak vocabulary with a clean `logical_chain` reached
the judge UNEXCLUDED — `chain_fraction` reported near-0.0 while the
served `reasoning_tree` markdown was mostly `[metadata redacted]`, the
exact "not a fair fixture" scenario the >20% rule exists to prevent; (2)
per the 2026-07-09 draft-10 governance call (forum #238), this
gutted-fraction check IS now the meta-discourse GATE for the WHOLE
Study-2b/track-b family — under-scoping it meant a heavily-meta
derivation (a claim ABOUT confidence-scoring, with a clean chain) could
pass the gate uncaught, exactly the circular-scoring case the gate is
supposed to close. Fixed by threading `is_chain=True` through every
screen() call inside `render_node` (claim at line ~149, claim+quoted_text
at ~169-170, the SUPPORT-leaf claim at ~196) so the fraction is
tree-WIDE, matching how `packet.py`'s observation branch already scopes
its own gutted-check broadly (claim+quoted_text+interpretation) — the
derivation branch was the one surface that had silently narrowed.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import db, redact
from .constants import DERIVATION_TYPES, OBSERVATION_TYPES


@dataclass
class TreeResult:
    markdown: str
    redaction_hits: list[redact.RedactionHit] = field(default_factory=list)
    node_ids_rendered: list[str] = field(default_factory=list)
    # the TARGET node's own screened claim text — exposed so callers (e.g.
    # packet.py's top-level "claim" field) can reuse it instead of
    # re-screening the same text a second time (which would double-log the
    # same redaction hits).
    target_claim_screened: str = ""
    # Accumulated redacted-char-count / total-char-count across EVERY
    # tree-rendered field (claim, logical_chain, quoted_text -- not just
    # logical_chain, per the colleague-review fix) — the correctly-scoped,
    # tree-WIDE input to the >20%-gutted-chain exclusion check. See module
    # docstring re bug #4 (offset-scoping) and the 2026-07-09 gutted-scope
    # fix (which fields count toward the fraction at all).
    chain_redacted_chars: int = 0
    chain_total_chars: int = 0


class GraphCache:
    """Precomputed lookup tables shared across all tree renders in one run
    — avoids an N+1 query per premise (this DB read layer is read-only
    SQLite; caching here is a plain performance concern, not a correctness
    one, since the target graph is not mutated during a run)."""

    def __init__(self, conn):
        self.conn = conn
        self.premises = db.fetch_all_derives_from(conn)
        self._node_cache: dict[str, db.NodeRow | None] = {}
        self._evidence_cache: dict[str, dict] = {}

    def node(self, node_id: str) -> db.NodeRow | None:
        if node_id not in self._node_cache:
            self._node_cache[node_id] = db.fetch_node(self.conn, node_id)
        return self._node_cache[node_id]

    def evidence(self, evidence_id: str) -> dict:
        if evidence_id not in self._evidence_cache:
            self._evidence_cache[evidence_id] = db.fetch_evidence_fields(
                self.conn, evidence_id
            )
        return self._evidence_cache[evidence_id]


def render_reasoning_tree(cache: GraphCache, target: db.NodeRow) -> TreeResult:
    lines: list[str] = []
    hits: list[redact.RedactionHit] = []
    rendered: dict[str, str] = {}  # node_id -> label of first occurrence
    node_order: list[str] = []
    captured: dict[str, str] = {}
    chain_totals = {"redacted": 0, "total": 0}

    def screen(text, node_id, fieldname, *, is_chain=False):
        if not text:
            return ""
        screened, h = redact.screen_text(text, node_id, fieldname)
        hits.extend(h)
        if is_chain:
            chain_totals["redacted"] += redact.redacted_char_count(text, h)
            chain_totals["total"] += len(text)
        return screened

    def indent(depth: int) -> str:
        return "    " * depth

    def render_node(node: db.NodeRow, label: str, depth: int, is_target: bool) -> None:
        if node.id in rendered:
            lines.append(f"{indent(depth)}[{label}] -- same node as [{rendered[node.id]}]")
            return
        rendered[node.id] = label
        node_order.append(node.id)

        own_label = "TARGET" if is_target else label
        prefix = f"[{own_label}]"

        if node.type in DERIVATION_TYPES:
            claim = screen(node.claim or "", node.id, "claim", is_chain=True)
            reasoning = screen(node.logical_chain or "", node.id, "logical_chain", is_chain=True)
            lines.append(f"{indent(depth)}{prefix} {claim}")
            lines.append(f"{indent(depth)}reasoning: {reasoning}")
            if is_target:
                captured["claim"] = claim

            for i, pid in enumerate(cache.premises.get(node.id, []), start=1):
                child = cache.node(pid)
                child_label = f"{label}.{i}" if not is_target else f"P{i}"
                if child is None:
                    # Defensive case (dangling derives_from edge). Do NOT
                    # interpolate the raw `pid` here — that would leak an
                    # un-redacted node ID the same way inline citations do
                    # (reviewer-fairy catch #2b).
                    lines.append(f"{indent(depth + 1)}[{child_label}] -- premise not found")
                    continue
                render_node(child, child_label, depth + 1, is_target=False)

        elif node.type in OBSERVATION_TYPES:
            claim = screen(node.claim or "", node.id, "claim", is_chain=True)
            quoted = screen(node.quoted_text or "", node.id, "quoted_text", is_chain=True)
            ev = cache.evidence(node.evidence_id) if node.evidence_id else {}
            # Reviewer-fairy round-2 catch: evidence fields are served
            # VERBATIM per §4, but an agent-authored title/URL can itself
            # cite another node's ID -- narrow node-ID-only screen (not the
            # full pipeline) so genuinely verbatim content isn't
            # over-redacted. See redact.screen_node_id_citations docstring.
            def screen_ev(text, fieldname):
                if not text:
                    return text
                screened, h = redact.screen_node_id_citations(text, node.id, fieldname)
                hits.extend(h)
                return screened

            ev_url = screen_ev(ev.get("url"), "evidence.url")
            ev_domain = screen_ev(ev.get("domain"), "evidence.domain")
            ev_title = screen_ev(ev.get("title"), "evidence.title")
            lines.append(f"{indent(depth)}[EVIDENCE for {own_label}] {claim}")
            lines.append(f'{indent(depth)}quoted_text: "{quoted}"')
            lines.append(
                f"{indent(depth)}source: url={ev_url!r} domain={ev_domain!r} "
                f"title={ev_title!r} source_date={ev.get('source_date')!r}"
            )
        else:
            # axiom / conjecture / lesson / other non-obs/dv premise cited
            # directly — no quoted_text/evidence to show (see docstring).
            claim = screen(node.claim or "", node.id, "claim", is_chain=True)
            lines.append(f"{indent(depth)}[SUPPORT for {own_label}] {claim}")

    render_node(target, "TARGET", 0, is_target=True)

    return TreeResult(
        markdown="\n".join(lines),
        redaction_hits=hits,
        node_ids_rendered=node_order,
        target_claim_screened=captured.get("claim", ""),
        chain_redacted_chars=chain_totals["redacted"],
        chain_total_chars=chain_totals["total"],
    )
