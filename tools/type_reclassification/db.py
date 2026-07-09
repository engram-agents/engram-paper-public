"""Read-only, multi-graph access to ENGRAM `knowledge.db` SQLite files, for
the Track-(b) dual-axis (observation + derivation arm) type-reclassification
harness.

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

**Scope: both observation- and derivation-type nodes** (`observation_factual`,
`observation_predictive`, `derivation`) — `OBSERVATION_TYPES`/`DERIVATION_TYPES`,
vendored via `tools.compression_fidelity.constants` (same-repo sibling-package
import; see `redact.py`'s module docstring for why this is NOT the same
fragility concern that made `compression_fidelity/constants.py` vendor-not-import
ACROSS repos). The derivation-arm functions below (`fetch_derivation_frame`,
`fetch_derivation_premises`, `find_type_correction_partner`,
`classify_derivation_outcome`) were added once the reasoning_type arm's
design intent + Aleph's review landed (2026-07-08) — see package
`__init__.py`'s note on how the observation-arm code was deliberately kept
general enough not to need a rewrite for this.

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

from tools.compression_fidelity.constants import DERIVATION_TYPES, OBSERVATION_TYPES

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
    # Derivation-arm fields (gh-derivation-arm handoff, 2026-07-08). Both
    # None/empty for observation-type rows; filled for derivation-type rows
    # by `fetch_derivation_frame` (premises needs a live `conn` to walk
    # `derives_from` edges, same reasoning `outcome` above already applies).
    premises: list = field(default_factory=list)

    @property
    def reasoning_type(self) -> Optional[str]:
        """`reasoning_type` lives in `metadata` (NOT a top-level `nodes`
        column) — confirmed against engram-alpha's `engram_core.py`
        `_create_derivation`, which stores
        `derive_meta = {"reasoning_type": reasoning_type, "reasoning_class": rclass}`
        into the node's `metadata` JSON, mirroring `source_class`'s own
        metadata-not-column storage (see `NodeRow.source_class` above)."""
        return self.metadata.get("reasoning_type")

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


# ---------------------------------------------------------------------------
# Derivation-arm functions (reasoning_type re-classification, §2/§4/§5 M5).
# ---------------------------------------------------------------------------

def fetch_derivation_premises(conn: sqlite3.Connection, derivation_id: str) -> list[dict]:
    """Return the visible premise structure for a derivation: each premise's
    `claim` + its own established `type` (the premise's `quote_type` if it's
    an observation, or its own `reasoning_type` if it's itself a derivation
    citing a prior derivation) -- pre-reg §2's "premise `type` IS shown, it's
    part of the visible premise->conclusion structure" requirement.

    Walks `derives_from`/`supported_by` edges FROM `derivation_id` (the
    convention `_create_derivation` writes them in, confirmed against
    engram-alpha's `engram_core.py` -- `INSERT INTO edges (source_id,
    target_id, relation, ...) VALUES (?, ?, 'derives_from', ...)` per
    supporting_id, source_id = the new derivation). Order is NOT guaranteed
    (SQLite gives no ordering guarantee absent ORDER BY, and the pre-reg's
    dose has no notion of premise order) -- sorted by target `id` for
    deterministic test/fixture comparisons only, not because order carries
    study meaning.

    A premise node that is itself neither an observation nor a derivation
    (e.g. an axiom/conjecture/theory cited as a premise -- CLAIM_BEARING_TYPES
    in engram-alpha includes these) gets `type: None` -- there is no
    quote_type/reasoning_type to show for those, and the dose must not
    invent one.
    """
    rows = conn.execute(
        """SELECT p.id, p.type AS node_type, p.claim, p.quote_type, p.metadata
           FROM edges e
           JOIN nodes p ON p.id = e.target_id
           WHERE e.source_id = ? AND e.relation IN ('derives_from', 'supported_by')
           ORDER BY p.id""",
        (derivation_id,),
    ).fetchall()

    premises: list[dict] = []
    for r in rows:
        node_type = r["node_type"]
        premise_type: Optional[str] = None
        if node_type in OBSERVATION_TYPES:
            premise_type = r["quote_type"]
        elif node_type in DERIVATION_TYPES:
            try:
                meta = json.loads(r["metadata"]) if r["metadata"] else {}
            except (TypeError, ValueError):
                meta = {}
            if isinstance(meta, dict):
                premise_type = meta.get("reasoning_type")
        premises.append({"claim": r["claim"], "type": premise_type})
    return premises


def fetch_derivation_frame(conn: sqlite3.Connection, graph_id: str) -> list[NodeRow]:
    """All derivation-type nodes in `conn`'s DB (any status/is_current),
    stamped with `graph_id`, `.premises` (via `fetch_derivation_premises`),
    and a precomputed `.outcome` (via `classify_derivation_outcome`).
    Mirrors `fetch_frame`'s observation-arm shape and rationale exactly --
    see that function's docstring for why ALL statuses are fetched (not
    pre-filtered to is_current=1) rather than duplicating the explanation.
    """
    types = tuple(DERIVATION_TYPES)
    placeholders = ",".join("?" * len(types))
    cur = conn.execute(
        f"""SELECT {NODE_COLUMNS} FROM nodes n
            LEFT JOIN nodes ev ON n.evidence_id = ev.id
            WHERE n.type IN ({placeholders})""",
        types,
    )
    rows = [_row_to_node(r, graph_id) for r in cur.fetchall()]
    for row in rows:
        row.premises = fetch_derivation_premises(conn, row.id)
        row.outcome = classify_derivation_outcome(row, conn)
    return rows


def fetch_derivation_frame_multi(db_paths: dict[str, str]) -> list[NodeRow]:
    """Multi-graph derivation frame -- mirrors `fetch_frame_multi` exactly."""
    all_rows: list[NodeRow] = []
    for graph_id, db_path in db_paths.items():
        conn = connect(db_path)
        try:
            all_rows.extend(fetch_derivation_frame(conn, graph_id))
        finally:
            conn.close()
    return all_rows


@dataclass
class TypeCorrectionSearch:
    """Tri-state result of `find_type_correction_partner` -- distinguishes
    "definitely not a type correction" from "can't tell" (colleague-review
    -caught gap, Borges, 2026-07-08: the prior boolean/Optional-only
    signature silently folded these two into one "no match" outcome, which
    could let an UNASSESSABLE node land in the scored refuted/INCLUDE
    population as if it had been assessed-and-found-clean).

    partner: the matched correction partner, or None if none found.
    indeterminate: True if a same-claim candidate existed but its
        reasoning_type (or `row`'s own) is None, so a type-change
        comparison could not be made at all. When True, `partner` is
        always None -- an indeterminate candidate is never returned as a
        confirmed match (that would be guessing the comparison came out
        "different").
    """
    partner: Optional[NodeRow] = None
    indeterminate: bool = False


def find_type_correction_partner(conn: sqlite3.Connection, row: NodeRow) -> TypeCorrectionSearch:
    """Find `row`'s type-correction PARTNER node, if one exists -- the
    reconstruction step for both the outcome-labeler's circularity fix
    (§4/draft-3) and the M5 positive-control pool (§5).

    Type-errors surface in TWO structural forms (Borges's handoff, 2026-07-08,
    both must be mined -- a supersede-only miner silently undercounts):

    Form (a) -- FORMAL SUPERSEDE: `row.superseded_by` is set, and the
    superseding node has the SAME claim text but a DIFFERENT reasoning_type.
    Structurally linked via the `superseded_by` FK -- no ambiguity.

    Form (b) -- RETRACT(error_type=other) + REFILE: `row` is retracted with
    error_type == "other", and a LATER derivation in the SAME graph exists
    with the SAME claim text but a DIFFERENT reasoning_type. There is no FK
    linking a retraction to its refile (unlike supersede) -- ENGRAM's schema
    has no "refiled_by" concept, so this is a claim-text + created_at
    heuristic, not a structural guarantee. Deliberately conservative:
    EXACT claim-text match only (no fuzzy/normalized matching), and if
    MULTIPLE later same-claim candidates exist, the EARLIEST one is taken
    (the first refile attempt, not a later unrelated coincidence) --
    favors returning no-match over a false-positive partner pairing, same
    "ambiguous > wrong" discipline as `_contradicted_and_lost` above.

    Returns `TypeCorrectionSearch(partner=None, indeterminate=False)` if
    `row` is not itself a candidate (not superseded, not a
    retracted-with-error_type=other derivation) OR no same-claim candidate
    is found at all, OR the only candidate partner(s) have the SAME
    reasoning_type as `row` (a supersede/refile that did NOT change the
    type is not a type correction -- e.g. a pure content refinement, out
    of scope here). Returns `indeterminate=True` if a same-claim candidate
    exists but either its or `row`'s own `reasoning_type` is None (a
    type-change comparison literally cannot be made) -- see
    `classify_derivation_outcome`'s handling of this case.
    """
    if row.type not in DERIVATION_TYPES:
        return TypeCorrectionSearch()

    # #1715-shaped bug caught by reviewer-fairy review (2026-07-08): these
    # two checks were originally `if/elif`, making Form (a) and Form (b)
    # MUTUALLY EXCLUSIVE. A real, reproducible circularity leak: a
    # derivation can be BOTH superseded (by a same-reasoning_type content
    # refinement -- NOT itself a type correction) AND SEPARATELY retracted
    # later with error_type="other" (engram-alpha's `_retract_impl` never
    # checks `superseded_by`/`is_current` before retracting -- confirmed
    # against engram_revision.py). With `elif`, the `if row.superseded_by`
    # branch wins, finds no type change on the supersede partner, and the
    # function returns None -- even when a genuine Form (b) refile (same
    # claim, different reasoning_type, filed later) exists elsewhere in the
    # graph. Both checks now run independently and their candidates are
    # unioned (Form (a) first -- the more certain structural match --
    # then Form (b)'s heuristic match), so a Form (a) non-match no longer
    # suppresses a real Form (b) match.
    candidates: list[sqlite3.Row] = []

    if row.superseded_by is not None:
        cur = conn.execute(
            f"SELECT {NODE_COLUMNS} FROM nodes n "
            f"LEFT JOIN nodes ev ON n.evidence_id = ev.id WHERE n.id = ?",
            (row.superseded_by,),
        )
        r = cur.fetchone()
        if r is not None:
            candidates.append(r)

    if row.status == "retracted" and (row.metadata or {}).get("error_type") == "other":
        # Colleague-review-caught gap (Borges, 2026-07-08): the docstring
        # says "a LATER derivation" but the query had no created_at bound
        # at all -- only an ORDER BY, which sorts candidates but doesn't
        # EXCLUDE earlier ones. An earlier same-claim-diff-type node (e.g.
        # a prior draft this derivation itself superseded/refiled FROM)
        # could be silently picked as the "correction partner," which for
        # M5 specifically would mis-pair pre_correction_packet (should be
        # the retracted row) against the WRONG ground_truth_type -- silent
        # because it requires a multi-version claim history to trigger, no
        # crash, just a wrong number in the study's own positive-control
        # instrument. row's own created_at is fetched here (NodeRow/
        # NODE_COLUMNS don't carry it -- both are shared with the
        # observation arm's already-reviewed code, so this stays a scoped
        # local lookup rather than widening that shared surface).
        row_created_at = conn.execute(
            "SELECT created_at FROM nodes WHERE id = ?", (row.id,)
        ).fetchone()
        if row_created_at is not None:
            cur = conn.execute(
                f"SELECT {NODE_COLUMNS} FROM nodes n "
                f"LEFT JOIN nodes ev ON n.evidence_id = ev.id "
                f"WHERE n.type IN ({','.join('?' * len(DERIVATION_TYPES))}) "
                f"AND n.id != ? AND n.claim = ? AND n.created_at > ? "
                f"ORDER BY n.created_at ASC",
                (*DERIVATION_TYPES, row.id, row.claim, row_created_at["created_at"]),
            )
            candidates.extend(cur.fetchall())

    saw_indeterminate = False
    for cand_row in candidates:
        cand = _row_to_node(cand_row, row.graph_id)
        if cand.claim != row.claim:
            continue  # form (a) safety check: supersede target must match too
        if cand.reasoning_type is None or row.reasoning_type is None:
            # Colleague-review-caught gap (Borges, 2026-07-08): a same-claim
            # candidate exists, but the type-change comparison literally
            # cannot be made (one side's reasoning_type is unknown --
            # legacy/backfilled derivations, typically). The OLD code
            # silently treated this the same as "compared, found no
            # change" (both falsy-short-circuit the `and` chain), which
            # would let an unassessable node enter the scored population
            # as if it had been cleanly assessed. Track it and keep
            # scanning other candidates -- a LATER candidate in the same
            # list might still resolve definitively.
            saw_indeterminate = True
            continue
        if cand.reasoning_type != row.reasoning_type:
            return TypeCorrectionSearch(partner=cand)
    return TypeCorrectionSearch(indeterminate=saw_indeterminate)


def classify_derivation_outcome(row: NodeRow, conn: sqlite3.Connection) -> str:
    """Derivation-arm outcome classification -- mirrors `classify_outcome`'s
    rubric exactly EXCEPT for the type-error circularity fix (§4 draft-3):
    a retracted-or-superseded derivation whose correction is a TYPE change
    (same claim, different reasoning_type -- see `find_type_correction_partner`)
    is tagged "excluded_type", NOT "refuted"/"unclassified". Type-errors are
    the study's own predictor (type mis-selection); letting them leak into
    the refuted/unclassified outcome population would make the predictor
    and the outcome the same construct -- circular (Borges, seq 1398).

    Order (checked in this priority, same discipline as `classify_outcome`):
      1. retracted + error_type in EXCLUDE list -> "excluded"
      2. retracted OR superseded + a type-correction partner exists ->
         "excluded_type"
      2b. retracted OR superseded + a same-claim candidate exists but the
         type-change comparison is INDETERMINATE (either side's
         reasoning_type is None -- colleague-review-caught gap, Borges,
         2026-07-08) -> "unclassified", NEVER "refuted"/"excluded_type".
         "Can't tell if this was a type correction" must never be silently
         treated as "assessed and clean" (which would let it enter the
         scored refuted/INCLUDE population) NOR as a confirmed correction
         (which would enter M5 with an unreliable ground truth) -- the
         SAME open-question-deferral principle classify_outcome already
         applies to a superseded-with-unwritten-rubric observation.
      3. retracted + error_type in INCLUDE list -> "refuted"
      4. superseded_by is not None (no type-correction partner found) ->
         "unclassified" (same open-question deferral as classify_outcome)
      5. contradicted-and-lost (reused verbatim from classify_outcome's own
         helper -- the structural-loss logic is type-system-agnostic)
      6. otherwise -> "survived"
    """
    meta = row.metadata or {}
    error_type = meta.get("error_type")

    if row.status == "retracted":
        if error_type in _EXCLUDED_ERROR_TYPES:
            return "excluded"
        search = find_type_correction_partner(conn, row)
        if search.partner is not None:
            return "excluded_type"
        if search.indeterminate:
            return "unclassified"
        if error_type in _REFUTED_ERROR_TYPES:
            return "refuted"
        return "unclassified"

    if row.superseded_by is not None:
        search = find_type_correction_partner(conn, row)
        if search.partner is not None:
            return "excluded_type"
        return "unclassified"

    lost = _contradicted_and_lost(row, conn)
    if lost is not None:
        return lost

    return "survived"


def mine_m5_reconstruction_pool(conn: sqlite3.Connection, graph_id: str) -> list[dict]:
    """Build the M5 positive-control pool (§5): every derivation classified
    as "excluded_type" by `classify_derivation_outcome`, reconstructed into
    a {pre_correction_packet, ground_truth_type} pair.

    pre_correction_packet is the SAME shape a normal derivation-arm frame
    item would have ({id, claim, premises}) built from the RETRACTED/
    SUPERSEDED node's OWN premises (its pre-correction state -- the panel
    re-judges what reasoning_type the ORIGINAL claim+premises warranted,
    blind to the fact a correction ever happened). ground_truth_type is the
    partner node's reasoning_type -- the agent's own refiled/superseding
    choice, used only for scoring (recovery rate vs chance), never shown to
    the judge.

    Does NOT redact/export-shape the packet (no confidence/interpretation/
    node-id withholding applied here) -- that is frame_export.py's job,
    same division of responsibility as the observation arm's `fetch_frame`
    (raw fetch) vs `export_frame` (judge-facing shaping). Callers building
    the actual M5 dispatch packets must run this pool through the same
    withholding path as a normal derivation frame item.
    """
    frame = fetch_derivation_frame(conn, graph_id)
    pool: list[dict] = []
    for row in frame:
        if row.outcome != "excluded_type":
            continue
        search = find_type_correction_partner(conn, row)
        if search.partner is None:
            # row.outcome == "excluded_type" was set by
            # classify_derivation_outcome finding a CONFIRMED partner --
            # an indeterminate-only result never sets that outcome (see
            # its docstring), so reaching here with no partner is a
            # genuine defensive no-op, not a live path.
            continue
        pool.append({
            "pre_correction_packet": {
                "id": row.id,
                "claim": row.claim,
                "premises": row.premises,
            },
            "ground_truth_type": search.partner.reasoning_type,
        })
    return pool
