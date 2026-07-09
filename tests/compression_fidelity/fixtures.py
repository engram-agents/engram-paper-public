"""Synthetic knowledge.db builder for compression_fidelity tests -- mirrors
the real ENGRAM schema (engram-alpha `src/engram/engram_core.py`) closely
enough to exercise db.py's SQL against SQLite directly, without needing a
real graph or a cross-repo import dependency (see constants.py's own
vendoring-not-importing rationale)."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

_SCHEMA = """
CREATE TABLE nodes (
    id              TEXT PRIMARY KEY,
    type            TEXT NOT NULL,
    claim           TEXT,
    created_at      TEXT NOT NULL,
    source_url      TEXT,
    source_title    TEXT,
    source_domain   TEXT,
    source_date     TEXT,
    evidence_id     TEXT,
    quoted_text     TEXT,
    interpretation  TEXT,
    quote_type      TEXT,
    logical_chain   TEXT,
    confidence      REAL,
    supersedes      TEXT,
    superseded_by   TEXT,
    is_current      INTEGER DEFAULT 1,
    status          TEXT,
    metadata        TEXT DEFAULT '{}'
);

CREATE TABLE edges (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id   TEXT NOT NULL,
    target_id   TEXT NOT NULL,
    relation    TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
"""


def build_synthetic_db(tmp_path: Path, rows: list[dict], edges: list[tuple[str, str, str]] | None = None) -> str:
    """`rows`: list of dicts with at least id/type; other fields default
    sensibly. `edges`: list of (source_id, target_id, relation) tuples."""
    db_path = str(tmp_path / "synthetic.db")
    conn = sqlite3.connect(db_path)
    conn.executescript(_SCHEMA)
    for i, row in enumerate(rows):
        metadata = row.get("metadata", {})
        conn.execute(
            """INSERT INTO nodes
               (id, type, claim, created_at, source_url, source_title,
                source_domain, source_date, evidence_id, quoted_text,
                interpretation, quote_type, logical_chain, confidence,
                supersedes, superseded_by, is_current, status, metadata)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                row["id"], row["type"], row.get("claim"),
                row.get("created_at", f"2026-01-01T00:00:0{i % 10}Z"),
                row.get("source_url"), row.get("source_title"),
                row.get("source_domain"), row.get("source_date"),
                row.get("evidence_id"), row.get("quoted_text"),
                row.get("interpretation"), row.get("quote_type"),
                row.get("logical_chain"), row.get("confidence"),
                row.get("supersedes"), row.get("superseded_by"),
                row.get("is_current", 1), row.get("status"),
                json.dumps(metadata),
            ),
        )
    for source_id, target_id, relation in (edges or []):
        conn.execute(
            "INSERT INTO edges (source_id, target_id, relation, created_at) VALUES (?,?,?,?)",
            (source_id, target_id, relation, "2026-01-01T00:00:00Z"),
        )
    conn.commit()
    conn.close()
    return db_path
