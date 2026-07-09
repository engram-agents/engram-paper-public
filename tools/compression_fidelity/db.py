"""Read-only access to an ENGRAM `knowledge.db` SQLite file.

Schema source of truth: engram-alpha `src/engram/engram_core.py` (`nodes`,
`edges`, `edit_history` tables — same schema on every install per CLAUDE.md).
This module only ever SELECTs; it never writes to the target graph.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from typing import Optional

from .constants import DERIVATION_TYPES, OBSERVATION_TYPES


def connect(db_path: str) -> sqlite3.Connection:
    """Open the target knowledge.db read-only (URI mode, immutable)."""
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


@dataclass
class NodeRow:
    id: str
    type: str
    claim: Optional[str]
    quoted_text: Optional[str]
    interpretation: Optional[str]
    quote_type: Optional[str]
    evidence_id: Optional[str]
    logical_chain: Optional[str]
    confidence: Optional[float]
    metadata: dict = field(default_factory=dict)
    is_current: int = 1
    status: Optional[str] = None

    @property
    def reasoning_type(self) -> Optional[str]:
        return self.metadata.get("reasoning_type")


def _row_to_node(row: sqlite3.Row) -> NodeRow:
    meta_raw = row["metadata"]
    try:
        meta = json.loads(meta_raw) if meta_raw else {}
    except (TypeError, ValueError):
        meta = {}
    return NodeRow(
        id=row["id"],
        type=row["type"],
        claim=row["claim"],
        quoted_text=row["quoted_text"],
        interpretation=row["interpretation"],
        quote_type=row["quote_type"],
        evidence_id=row["evidence_id"],
        logical_chain=row["logical_chain"],
        confidence=row["confidence"],
        metadata=meta,
        is_current=row["is_current"],
        status=row["status"],
    )


NODE_COLUMNS = (
    "id, type, claim, quoted_text, interpretation, quote_type, evidence_id, "
    "logical_chain, confidence, metadata, is_current, status"
)


def fetch_frame(conn: sqlite3.Connection) -> list[NodeRow]:
    """Current, non-retracted observation + derivation nodes (pre-reg §5).

    `is_current = 1` already excludes superseded nodes (a supersede flips
    the OLD node's is_current to 0 — verified against engram_core.py), so
    this single filter satisfies both the "current" and "non-superseded"
    clauses of the pre-reg's frame definition. Conjectures, axioms,
    cornerstones, lessons, definitions, questions are excluded by the type
    filter alone.
    """
    types = tuple(OBSERVATION_TYPES | DERIVATION_TYPES)
    placeholders = ",".join("?" * len(types))
    cur = conn.execute(
        f"""SELECT {NODE_COLUMNS} FROM nodes
            WHERE is_current = 1
              AND (status IS NULL OR status != 'retracted')
              AND type IN ({placeholders})""",
        types,
    )
    return [_row_to_node(r) for r in cur.fetchall()]


def fetch_node(conn: sqlite3.Connection, node_id: str) -> Optional[NodeRow]:
    cur = conn.execute(f"SELECT {NODE_COLUMNS} FROM nodes WHERE id = ?", (node_id,))
    row = cur.fetchone()
    return _row_to_node(row) if row else None


def fetch_evidence_fields(conn: sqlite3.Connection, evidence_id: str) -> dict:
    """Raw, un-relabeled evidence-node fields (pre-reg §4: served verbatim)."""
    cur = conn.execute(
        "SELECT source_url, source_domain, source_title, source_date "
        "FROM nodes WHERE id = ?",
        (evidence_id,),
    )
    row = cur.fetchone()
    if not row:
        return {"url": None, "domain": None, "title": None, "source_date": None}
    return {
        "url": row["source_url"],
        "domain": row["source_domain"],
        "title": row["source_title"],
        "source_date": row["source_date"],
    }


def fetch_all_derives_from(conn: sqlite3.Connection) -> dict[str, list[str]]:
    """source_id -> [target_id, ...] for every `derives_from` edge, in the
    order the edges were created (rowid order — deterministic, matches the
    order premises were cited in `engram_derive`)."""
    cur = conn.execute(
        "SELECT source_id, target_id FROM edges "
        "WHERE relation = 'derives_from' ORDER BY id"
    )
    premises: dict[str, list[str]] = {}
    for row in cur.fetchall():
        premises.setdefault(row["source_id"], []).append(row["target_id"])
    return premises


def fetch_all_node_types(conn: sqlite3.Connection) -> dict[str, str]:
    """id -> type for every node in the graph (used by depth computation to
    resolve premise types that fall outside the sampling frame, e.g. an
    axiom or conjecture cited as a premise)."""
    cur = conn.execute("SELECT id, type FROM nodes")
    return {row["id"]: row["type"] for row in cur.fetchall()}
