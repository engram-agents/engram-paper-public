"""Read-only, multi-graph access to ENGRAM `knowledge.db` SQLite files, for
the Track-(b) observation-arm harness.

Schema source of truth: engram-alpha `src/engram/engram_core.py` (`nodes`,
`edges` tables — same schema on every install per engram-alpha's CLAUDE.md).
This module only ever SELECTs; it never writes to any target graph, and
`connect()` opens every DB in SQLite's `mode=ro` URI immutable mode (same
discipline as `tools/compression_fidelity/db.py`).

**Multi-graph is required, not optional** (pre-reg §4: "Population =
multi-graph, REQUIRED not optional" — the reasoning_type arm needs it for
power, and observation-arm S2 generality needs it too). `NodeRow.graph_id`
is a caller-supplied label per DB file (e.g. the filename stem, or an
explicit label the caller chooses) — the DB file itself has no notion of
its own graph identity, so this is plumbed in at `fetch_frame_multi`'s
`db_paths: dict[str, str]` (graph_id -> db_path) call boundary.

**Scope: observation-type nodes only** (`observation_factual`,
`observation_predictive`) — `OBSERVATION_TYPES`, vendored via
`tools.compression_fidelity.constants` (same-repo sibling-package import;
see `redact.py`'s module docstring for why this is NOT the same fragility
concern that made `compression_fidelity/constants.py` vendor-not-import
ACROSS repos). Derivation nodes are explicitly out of scope for this
package — the reasoning_type arm is on hold (see package `__init__.py`).

Unlike `compression_fidelity/db.py`'s `fetch_frame` (which filters to
`is_current=1 AND status != 'retracted'`), THIS `fetch_frame` deliberately
fetches ALL observation-type nodes regardless of status/is_current —
`classify_outcome` needs to see retracted, superseded, and currently-active
nodes alike to assign the outcome stratum (refuted / excluded / survived /
unclassified); pre-filtering any of those out here would make certain
outcome branches unreachable.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from typing import Optional

from tools.compression_fidelity.constants import OBSERVATION_TYPES

# ---------------------------------------------------------------------------
# fs_class proxy fallback — ported from engram-alpha `src/engram/
# engram_core.py`'s `_node_fs_class()` (~line 4819) and its `_FS_PROXY_MAP`
# (~line 4812). Cited verbatim below; kept in sync by hand (no automated
# drift check — same caveat as compression_fidelity/constants.py's vendoring
# note).
#
# _node_fs_class's real signature returns (fs_class, source) so callers can
# distinguish a native-field measurement from a Phase-1 proxy guess and label
# it honestly in surfaced text. This package only needs the fs_class VALUE
# (for the `stratum.fs_class` field — a researcher-side stratification axis,
# never shown to the judge), so `resolve_fs_class` below returns just the
# string; the source/proxy distinction is dropped as unneeded for this use,
# not because it doesn't matter in general.
# ---------------------------------------------------------------------------

_FS_PROXY_MAP = {
    "hard_data": "re-executable",
    "editorial": "frozen",
    "personal_communication": "frozen",
}


def resolve_fs_class(row: "NodeRow") -> str:
    """Port of `_node_fs_class`'s Phase-1/Phase-2 fallback logic
    (engram_core.py ~line 4819-4843): if the native `fs_class` column is
    already `"re-executable"` or `"frozen"`, use it; otherwise derive a
    proxy from `quote_type` via `_FS_PROXY_MAP`; otherwise `"unknown"`.
    """
    if row.fs_class in ("re-executable", "frozen"):
        return row.fs_class
    if not row.quote_type:
        return "unknown"
    return _FS_PROXY_MAP.get(row.quote_type, "unknown")


def connect(db_path: str) -> sqlite3.Connection:
    """Open a target knowledge.db read-only (URI mode, immutable)."""
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


@dataclass
class NodeRow:
    id: str
    graph_id: str
    type: str
    claim: Optional[str]
    quoted_text: Optional[str]
    interpretation: Optional[str]
    quote_type: Optional[str]
    evidence_id: Optional[str]
    confidence: Optional[float]
    metadata: dict = field(default_factory=dict)
    is_current: int = 1
    status: Optional[str] = None
    superseded_by: Optional[str] = None
    supersedes: Optional[str] = None
    fs_class: Optional[str] = None
    standpoint_author_id: Optional[str] = None
    source_domain: Optional[str] = None
    source_date: Optional[str] = None
    # Filled by `fetch_frame` (needs a live `conn` to walk contradiction/
    # supersede edges) — `frame_export.export_frame` reads this precomputed
    # value rather than recomputing it (it takes no `conn`). `None` until
    # `fetch_frame`/`classify_outcome` has run; hand-built test fixtures
    # that skip `fetch_frame` must set this explicitly.
    outcome: Optional[str] = None

    @property
    def source_class(self) -> Optional[str]:
        """`source_class` lives in `metadata` (NOT a top-level `nodes`
        column) — confirmed against `engram_observation.py`'s
        `_add_observation_impl`, which stores
        `{"source_class": source_class, "quote_verified": ...}` into
        `obs_metadata` (~line 1090) rather than a dedicated column."""
        return self.metadata.get("source_class")


def _row_to_node(row: sqlite3.Row, graph_id: str) -> NodeRow:
    meta_raw = row["metadata"]
    try:
        meta = json.loads(meta_raw) if meta_raw else {}
    except (TypeError, ValueError):
        meta = {}
    if not isinstance(meta, dict):
        # Nit caught in review: meta_raw could be the *literal string*
        # "null" -- valid JSON, parses successfully to Python None (not
        # {}), so the `if meta_raw else {}` guard above doesn't catch it
        # (a non-empty string is truthy). Would otherwise crash downstream
        # `.get(...)` calls (classify_outcome, NodeRow.source_class) with
        # AttributeError instead of leaking anything -- low-probability in
        # practice (ENGRAM always writes '{}' as the column default) but
        # cheap to close.
        meta = {}
    return NodeRow(
        id=row["id"],
        graph_id=graph_id,
        type=row["type"],
        claim=row["claim"],
        quoted_text=row["quoted_text"],
        interpretation=row["interpretation"],
        quote_type=row["quote_type"],
        evidence_id=row["evidence_id"],
        confidence=row["confidence"],
        metadata=meta,
        is_current=row["is_current"],
        status=row["status"],
        superseded_by=row["superseded_by"],
        supersedes=row["supersedes"],
        fs_class=row["fs_class"],
        standpoint_author_id=row["standpoint_author_id"],
        source_domain=row["source_domain"],
        source_date=row["source_date"],
    )


# source_domain/source_date are "Evidence-specific" columns in the real
# schema (engram_core.py's CREATE TABLE comment groups them under
# "-- Evidence-specific") — populated on the EVIDENCE node (ev_*), not the
# observation node itself. Confirmed against engram_observation.py: an
# observation row only carries `evidence_id`; source_domain/source_date are
# read back via a join/lookup on that referenced evidence node (mirrors
# compression_fidelity/db.py's separate `fetch_evidence_fields` helper — here
# folded into a single LEFT JOIN so `fetch_frame` can stamp them onto each
# NodeRow directly).
NODE_COLUMNS = (
    "n.id, n.type, n.claim, n.quoted_text, n.interpretation, n.quote_type, "
    "n.evidence_id, n.confidence, n.metadata, n.is_current, n.status, "
    "n.superseded_by, n.supersedes, n.fs_class, n.standpoint_author_id, "
    "ev.source_domain AS source_domain, ev.source_date AS source_date"
)


def fetch_frame(conn: sqlite3.Connection, graph_id: str) -> list[NodeRow]:
    """All observation-type nodes in `conn`'s DB (any status/is_current),
    stamped with `graph_id` and a precomputed `.outcome` (via
    `classify_outcome`, which needs `conn` to walk contradiction/supersede
    edges — see `NodeRow.outcome`'s docstring for why this is precomputed
    here rather than lazily in `frame_export`).
    """
    types = tuple(OBSERVATION_TYPES)
    placeholders = ",".join("?" * len(types))
    cur = conn.execute(
        f"""SELECT {NODE_COLUMNS} FROM nodes n
            LEFT JOIN nodes ev ON n.evidence_id = ev.id
            WHERE n.type IN ({placeholders})""",
        types,
    )
    rows = [_row_to_node(r, graph_id) for r in cur.fetchall()]
    for row in rows:
        row.outcome = classify_outcome(row, conn)
    return rows


def fetch_frame_multi(db_paths: dict[str, str]) -> list[NodeRow]:
    """Open each `(graph_id, db_path)` pair read-only, fetch its observation
    frame, and concatenate. Each DB's connection is opened and closed within
    this call — no connection is kept open past a given DB's `fetch_frame`
    call (mirrors `_run_db_one_time_setup`'s per-call-scoped-connection
    discipline; nothing here is shared/global state across graphs).
    """
    all_rows: list[NodeRow] = []
    for graph_id, db_path in db_paths.items():
        conn = connect(db_path)
        try:
            all_rows.extend(fetch_frame(conn, graph_id))
        finally:
            conn.close()
    return all_rows


# ---------------------------------------------------------------------------
# Outcome classification (pre-reg §4's refuted-set boundary + the
# coder-fairy spec's stratum rubric).
# ---------------------------------------------------------------------------

# error_types that EXCLUDE a retracted node from the frame entirely (pre-reg
# §4: "duplicate (housekeeping — claim wasn't wrong), wrong_citation
# (provenance error — claim may be fine)").
_EXCLUDED_ERROR_TYPES = {"duplicate", "wrong_citation"}

# error_types that mark a retracted node as calibration-relevant "refuted"
# (pre-reg §4 INCLUDE list, minus the contradiction/supersede structural
# cases handled separately below).
_REFUTED_ERROR_TYPES = {"hallucinated_claim", "wrong_evidence", "fabricated_quote", "other"}


def classify_outcome(row: NodeRow, conn: sqlite3.Connection) -> str:
    """Classify `row` into one of "refuted" / "survived" / "excluded" /
    "unclassified", per the coder-fairy spec's rubric (pre-reg §4's
    refuted-set boundary). Order matters — each branch below is checked in
    the same priority order the spec enumerates:

      1. retracted + error_type in EXCLUDE list -> "excluded"
      2. retracted + error_type in INCLUDE list -> "refuted"
      3. superseded_by is not None (and not retracted) -> "unclassified"
         (deliberate open design question — superseded-as-wrong vs
         superseded-as-refined needs a rubric not yet written; NEVER
         silently folded into refuted/survived)
      4. contradicted-and-lost (structural, via a resolved/partially_resolved
         contradiction) -> "refuted", or "unclassified" if the "who won"
         determination is structurally ambiguous (see `_contradicted_and_lost`)
      5. otherwise -> "survived"
    """
    meta = row.metadata or {}
    error_type = meta.get("error_type")

    if row.status == "retracted":
        if error_type in _EXCLUDED_ERROR_TYPES:
            return "excluded"
        if error_type in _REFUTED_ERROR_TYPES:
            return "refuted"
        # Retracted but with an error_type outside both named lists (e.g.
        # a malformed/legacy row with no error_type at all, or a future
        # VALID_ERROR_TYPES addition this module hasn't been updated for).
        # Reviewer-fairy-caught fix: this used to default to "refuted" on
        # the reasoning that "a retraction IS itself evidence the claim was
        # wrong" -- but that asserts refuted from ABSENCE of positive
        # evidence, which contradicts the discipline this same function
        # applies correctly everywhere else (never guess refuted; tag
        # unclassified instead). Confirmed NOT hypothetical: engram-alpha's
        # own edit-history backfill code explicitly handles error_type
        # being None on legacy retracted rows, so an old/legacy retraction
        # with no error_type recorded is a real possibility in exactly the
        # multi-graph, cross-agent, possibly-old-snapshot population §4
        # requires -- and silently counting it as "refuted" would
        # contaminate the study's core dependent variable.
        return "unclassified"

    if row.superseded_by is not None:
        return "unclassified"

    lost = _contradicted_and_lost(row, conn)
    if lost is not None:
        return lost  # "refuted" or "unclassified"

    return "survived"


def _derives_from_or_is(conn: sqlite3.Connection, source_id: str, target_id: str) -> bool:
    """True if `source_id == target_id`, OR there is a direct
    `derives_from`/`supported_by` edge FROM `source_id` TO `target_id`
    (i.e. `source_id`'s node cites/derives from `target_id`'s claim as a
    supporting premise).

    **One-hop only** — does NOT walk a multi-step derivation chain (a
    resolver that derives from an intermediate node which in turn derives
    from `target_id` two-plus hops away is NOT detected here). This is a
    deliberate conservative choice (favors "ambiguous" over a false-positive
    "who won" call), not an oversight — flagged explicitly in the handoff as
    the piece most worth a closer look.
    """
    if source_id == target_id:
        return True
    row = conn.execute(
        "SELECT 1 FROM edges WHERE source_id = ? AND target_id = ? "
        "AND relation IN ('derives_from', 'supported_by') LIMIT 1",
        (source_id, target_id),
    ).fetchone()
    return row is not None


def _contradicted_and_lost(row: NodeRow, conn: sqlite3.Connection) -> Optional[str]:
    """Returns "refuted" if `row` structurally lost a resolved contradiction,
    "unclassified" if the "who won" determination cannot be made from the
    schema for at least one disputing contradiction, or `None` if `row` is
    not the target of any resolved/partially_resolved contradiction at all
    (i.e. this check has no signal — the caller falls through to
    "survived").

    **THE JUDGMENT-CALL PIECE (flagged per the coder-fairy spec's explicit
    ask for close review):**

    A contradiction node (`ct`) has exactly two `contradicts` edges (source
    = ct, target = each disputed node — confirmed against
    `engram_derive.py`'s `_contradict_impl`, which always wires exactly
    `node_id_a` and `node_id_b`). Once resolved, `ct.resolved_by` names the
    argmax-confidence current resolver wired via a `resolves` edge
    (`_resolve_impl`, engram_revision.py) — but `resolved_by` is a SEPARATE
    node, not one of the two `contradicts` targets by construction (the #229
    "pure-wire" design deliberately encourages composing a fresh resolving
    derivation that CITES the winning side as a premise, rather than
    resolving directly with one of the two disputed nodes — see
    `_resolve_impl`'s docstring on why "forcing callers to compose the
    resolving derivation explicitly ... makes citing roots the natural
    pattern"). So "who won" is NOT a stored fact anywhere — it has to be
    inferred from whether the resolver is, or derives from, one of the two
    disputed sides:

      - `resolved_by == row.id` (this node itself resolved the dispute) ->
        this node WON -> no refutation signal from this ct.
      - `resolved_by` derives_from/is `row.id` directly (one-hop) -> this
        node's side WON (the resolver cited THIS node as a premise) -> no
        refutation signal from this ct.
      - `resolved_by` derives_from/is the SIBLING side (the other
        `contradicts` target of the same ct) -> the sibling WON -> `row`
        LOST -> "refuted".
      - Neither: the resolver is a structurally-independent node with no
        one-hop derivation link to EITHER disputed side. The schema gives
        no further signal to determine who won. **AMBIGUOUS** -> tagged
        "unclassified" rather than guessed, per the spec's explicit
        instruction to flag rather than silently guess here.

    If multiple resolved contradictions dispute the same node, "refuted"
    takes priority over "unclassified" (a clear structural loss anywhere is
    more informative than an ambiguous result elsewhere) over `None`.
    """
    node_id = row.id
    cts = conn.execute(
        """SELECT DISTINCT ct.id AS ct_id, ct.resolved_by AS resolved_by
           FROM edges e
           JOIN nodes ct ON ct.id = e.source_id
           WHERE e.target_id = ? AND e.relation = 'contradicts'
             AND ct.type = 'contradiction'
             AND ct.status IN ('resolved', 'partially_resolved')""",
        (node_id,),
    ).fetchall()
    if not cts:
        return None

    signals: list[str] = []
    for ct in cts:
        resolved_by = ct["resolved_by"]
        if resolved_by is None:
            # resolved/partially_resolved but resolved_by unset -- a data
            # anomaly (real `_resolve_impl` always stamps resolved_by
            # alongside status in the same UPDATE). No signal from this ct.
            continue
        if _derives_from_or_is(conn, resolved_by, node_id):
            # this node itself won (self-resolver, or the resolver derives
            # from this node's claim).
            continue

        siblings = conn.execute(
            "SELECT target_id FROM edges WHERE source_id = ? AND relation = 'contradicts' AND target_id != ?",
            (ct["ct_id"], node_id),
        ).fetchall()
        sibling_ids = [s["target_id"] for s in siblings]

        if any(_derives_from_or_is(conn, resolved_by, sib) for sib in sibling_ids):
            signals.append("refuted")
        else:
            signals.append("unclassified")

    if "refuted" in signals:
        return "refuted"
    if "unclassified" in signals:
        return "unclassified"
    return None
