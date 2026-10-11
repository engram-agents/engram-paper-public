#!/usr/bin/env python3
"""Freeze a date-time-stamped copy of a live ENGRAM graph as the paper's data SSoT.

Lei's ruling, 2026-09-20: one graph is the paper's evidence base, frozen at a
stamped moment, and every real-graph number in the paper is refreshed against it
unless the text clearly states otherwise. This script is the instrument that
makes the freeze, checked in so the act of freezing is as reproducible as the
numbers drawn from it.

WHY Connection.backup() AND NOT `cp`: the live DB runs in WAL mode with a hot
-wal and -shm beside it. A plain copy of the .db alone captures the main file
without the committed-but-uncheckpointed WAL contents -- a torn, silently
wrong snapshot that opens fine. `Connection.backup()` is the sqlite3 module's
page-level hot copy and folds the WAL view in. It is also the same call
ENGRAM's own backup and snapshot-worker paths use, so this is the tested route
rather than a second one invented here.

NOTHING IS STRIPPED. ENGRAM's `engram_backup.dump_stripped` drops embeddings and
derived indices, which is right for a git-tracked backup and wrong for a paper
SSoT: a stripped snapshot cannot answer a later question that needs embeddings,
and the whole point of a frozen SSoT is that it stays answerable.

Usage:  python3 tools/freeze_paper_snapshot.py [--src PATH] [--dest-dir PATH]
"""
import argparse, hashlib, os, sqlite3, sys
from datetime import datetime, timezone

def sha256(path, buf=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(buf), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.expanduser("~/.engram/knowledge.db"))
    ap.add_argument("--dest-dir", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))
    a = ap.parse_args()

    if not os.path.exists(a.src):
        sys.exit(f"source DB not found: {a.src}")
    os.makedirs(a.dest_dir, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = os.path.join(a.dest_dir, f"engram-paper-ssot-{stamp}.db")
    if os.path.exists(dest):
        sys.exit(f"refusing to overwrite existing snapshot: {dest}")

    src = sqlite3.connect(f"file:{a.src}?mode=ro", uri=True)
    try:
        bk = sqlite3.connect(dest)
        try:
            src.backup(bk)          # WAL-safe consistent hot copy
        finally:
            bk.close()
    finally:
        src.close()

    # --- census, denominators printed beside numerators -----------------
    c = sqlite3.connect(f"file:{dest}?mode=ro", uri=True)
    total = c.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
    current = c.execute("SELECT COUNT(*) FROM nodes WHERE is_current=1").fetchone()[0]
    by_type = c.execute(
        "SELECT type, COUNT(*) FROM nodes WHERE is_current=1 GROUP BY type ORDER BY COUNT(*) DESC"
    ).fetchall()
    edges = c.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    latest = c.execute("SELECT MAX(created_at) FROM nodes").fetchone()[0]
    earliest = c.execute("SELECT MIN(created_at) FROM nodes").fetchone()[0]
    c.close()

    size = os.path.getsize(dest)
    print(f"SNAPSHOT   {dest}")
    print(f"frozen_at  {stamp}  (UTC, from the clock at freeze time)")
    print(f"sha256     {sha256(dest)}")
    print(f"size       {size:,} bytes")
    print(f"source     {a.src}")
    print()
    print(f"nodes      {current:,} current of {total:,} total")
    print(f"edges      {edges:,}")
    print(f"span       {earliest}  ..  {latest}")
    print()
    print("current nodes by type (numerator / denominator = current total):")
    for t, n in by_type:
        print(f"  {t:<24} {n:>6,} / {current:,}")

if __name__ == "__main__":
    main()
