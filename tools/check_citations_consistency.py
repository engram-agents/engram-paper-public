#!/usr/bin/env python3
"""check_citations_consistency — verify ENGRAM ↔ citations.bib ↔ citations.manifest

Reads three sources of truth and reports drift between them:

  1. ENGRAM evidence nodes (~/.engram/knowledge.db, type='evidence')
  2. paper_research/citations.bib (BibTeX entries)
  3. paper_research/citations.manifest (TSV: evidence_id  bibkey  url  title)

Hard checks (exit 1 if any fail):
  - Every bibkey in manifest has a matching @xxx{bibkey,...} in bib
  - Every @xxx{bibkey,...} in bib appears in manifest (with empty
    evidence_id allowed for paper-cited-but-not-engram-evidenced entries)
    OR has the legacy `note = {ENGRAM evidence ev_XXXX}` form from before
    the manifest existed
  - Every non-empty evidence_id in manifest exists as an evidence node in
    ~/.engram/knowledge.db
  - URLs in manifest match URLs in the corresponding bib entry

Soft checks (warn-only, no exit failure):
  - ENGRAM evidence nodes with non-empty source_url but no matching
    manifest entry (orphan evidence — might be intentional, or might
    be a missing bib-add)

Usage:
    python tools/check_citations_consistency.py [--db ~/.engram/knowledge.db]

Exit codes:
    0 — all hard checks pass (soft warnings printed but non-fatal)
    1 — at least one hard check failed
    2 — script error (couldn't read a file, etc.)
"""

import argparse
import os
import re
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BIB_PATH = REPO_ROOT / "paper_research" / "citations.bib"
MANIFEST_PATH = REPO_ROOT / "paper_research" / "citations.manifest"

# @xxx{bibkey, ... } — captures bib-entry-type and bibkey
BIB_ENTRY_RE = re.compile(r"^@(?P<entry_type>\w+)\{(?P<bibkey>[^,\s]+)\s*,", re.M)
# url field inside an entry: url = {...} or url = "..."
URL_FIELD_RE = re.compile(r"url\s*=\s*[{\"]([^}\"]+)[}\"]")
# legacy note = {ENGRAM evidence ev_XXXX}
LEGACY_NOTE_RE = re.compile(r"note\s*=\s*\{\s*ENGRAM evidence\s+(ev_\d+)\s*\}")
# arxiv URL canonicalization — same paper ID across /abs/, /html/, /html/vN, /pdf/
ARXIV_URL_RE = re.compile(r"https?://arxiv\.org/(?:abs|html|pdf)/(\d+\.\d+)(?:v\d+)?(?:\.pdf)?")

# URL prefixes for ENGRAM evidence that is intentionally NOT a paper citation —
# the orphan-evidence soft check filters these out so it only fires on URLs
# that COULD plausibly be paper sources (arxiv, link.springer, pmc.ncbi, etc.).
# Empirically derived from the orphan distribution on master 2026-05-10:
# - file:// : local project files, hooks, design docs (218 hits — never a paper)
# - GitHub : code repos (rarely a paper; explicit bib-add if needed)
# - Anthropic / claude.com / claude.ai : tooling docs (not papers)
# - Encyclopedias / blogs : wikipedia, baike, IEP, medium, etc. (rarely a paper)
# - Internal schemes : session-transcript:// , conversation:// (never a paper)
# - API / data sources : financialmodelingprep, etc. (data, not papers)
#
# Conservative principle: leave anything that COULD be a paper (publishers,
# arxiv, doi, university repos) un-filtered so it surfaces as a soft warning
# if missing from the bib. Better to warn on a real omission than silently
# skip a paper-citable orphan.
NON_PAPER_URL_PATTERNS = (
    "file://",
    "https://session-transcript/",
    "conversation://",
    "https://github.com/",
    "https://www.anthropic.com/",
    "https://docs.anthropic.com/",
    "https://platform.claude.com/",
    "https://docs.claude.com/",
    "https://code.claude.com/",
    "https://claude.ai/",
    "https://en.wikipedia.org/",
    "https://baike.baidu.com/",
    "https://iep.utm.edu/",
    "https://unfinishablemap.org/",
    "https://zettelkasten.de/",
    "https://decodeclaude.com/",
    "https://medium.com/",
    "https://martinfowler.com/",
    "https://www.emergentmind.com/",
    "https://bpi.com/",
    "https://financialmodelingprep.com/",
    # ScienceDirect /topics/ pages are encyclopedic, not papers. Article URLs
    # under /science/article/ stay un-filtered — they're real papers.
    "https://www.sciencedirect.com/topics/",
)


def is_non_paper_url(url: str) -> bool:
    """True if the URL matches a known non-paper-source prefix (orphan filter)."""
    if not url:
        return True  # empty URL — not a paper either
    return any(url.startswith(p) for p in NON_PAPER_URL_PATTERNS)


def canonicalize_url(url: str) -> str:
    """Reduce cosmetic URL variants to a canonical form for cross-source compare.

    arxiv.org/abs/X.Y, arxiv.org/html/X.Y, arxiv.org/html/X.Yv1, arxiv.org/pdf/X.Y
    all collapse to the same canonical key. Other URLs returned as-is.
    """
    if not url:
        return url
    m = ARXIV_URL_RE.match(url.strip())
    if m:
        return f"arxiv:{m.group(1)}"
    return url.strip().rstrip("/")


def parse_bib(path: Path) -> dict:
    """Return {bibkey: {entry_type, url, has_legacy_note, ev_in_note}} per entry.

    Parses by splitting at top-level @xxx{... entries. Each entry's body is
    the text between its `@xxx{` and the next `@xxx{` or EOF.
    """
    text = path.read_text()
    entries = {}
    matches = list(BIB_ENTRY_RE.finditer(text))
    for i, m in enumerate(matches):
        bibkey = m.group("bibkey")
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end]
        url_m = URL_FIELD_RE.search(body)
        note_m = LEGACY_NOTE_RE.search(body)
        # Latent silent-data-loss guard: a future PR introducing a duplicate
        # bibkey would silently lose the earlier entry without this WARN.
        # Currently no duplicates in the bib (per PR #19 fairy verification).
        if bibkey in entries:
            print(
                f"WARN: duplicate bibkey '{bibkey}' in bib — earlier entry overwritten",
                file=sys.stderr,
            )
        entries[bibkey] = {
            "entry_type": m.group("entry_type"),
            "url": url_m.group(1) if url_m else None,
            "has_legacy_note": note_m is not None,
            "ev_in_note": note_m.group(1) if note_m else None,
        }
    return entries


def parse_manifest(path: Path) -> list:
    """Return list of {evidence_id, bibkey, url, title} dicts (header skipped)."""
    rows = []
    with path.open() as f:
        header = f.readline()  # skip header
        if not header.startswith("evidence_id"):
            print(f"ERROR: {path} header does not start with 'evidence_id'",
                  file=sys.stderr)
            sys.exit(2)
        for lineno, line in enumerate(f, start=2):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                print(f"WARN: {path}:{lineno}: expected 4 tab-separated fields, got {len(parts)}",
                      file=sys.stderr)
                continue
            rows.append({
                "lineno": lineno,
                "evidence_id": parts[0].strip(),
                "bibkey": parts[1].strip(),
                "url": parts[2].strip(),
                "title": parts[3].strip(),
            })
    return rows


def load_engram_evidence(db_path: Path) -> dict:
    """Return {ev_id: source_url} for every type='evidence' node."""
    conn = sqlite3.connect(str(db_path))
    out = {}
    try:
        cur = conn.execute(
            "SELECT id, source_url FROM nodes WHERE type='evidence'"
        )
    except sqlite3.DatabaseError as exc:
        # DatabaseError is the parent class covering BOTH "file is not a database"
        # (raw DatabaseError) and "no such table: nodes" (OperationalError extends
        # DatabaseError). Catching the parent covers both — per PR #19 round-2
        # fairy: OperationalError alone missed the non-SQLite-file case.
        print(
            f"ERROR: {db_path} is not a valid ENGRAM database ({exc}); "
            f"use --db /nonexistent to skip ENGRAM-side checks instead.",
            file=sys.stderr,
        )
        sys.exit(2)
    for row in cur:
        out[row[0]] = row[1] or ""
    conn.close()
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--db", type=Path,
                        default=Path(os.path.expanduser(
                            os.environ.get("ENGRAM_HOME", "~/.engram")
                        )) / "knowledge.db",
                        help="Path to ENGRAM knowledge.db")
    args = parser.parse_args()

    if not BIB_PATH.exists():
        print(f"ERROR: {BIB_PATH} does not exist", file=sys.stderr)
        return 2
    if not MANIFEST_PATH.exists():
        print(f"ERROR: {MANIFEST_PATH} does not exist", file=sys.stderr)
        return 2

    print(f"Reading bib:      {BIB_PATH}")
    bib = parse_bib(BIB_PATH)
    print(f"  → {len(bib)} entries")

    print(f"Reading manifest: {MANIFEST_PATH}")
    manifest = parse_manifest(MANIFEST_PATH)
    print(f"  → {len(manifest)} rows")

    engram_available = args.db.exists()
    if engram_available:
        print(f"Reading ENGRAM:   {args.db}")
        engram = load_engram_evidence(args.db)
        print(f"  → {len(engram)} evidence nodes")
    else:
        print(f"NOTE: {args.db} not found — skipping ENGRAM-side checks.")
        engram = {}

    print()
    print("=" * 72)
    print("HARD CHECKS")
    print("=" * 72)

    failures: list[str] = []

    # Check 1: every manifest bibkey is in bib
    bib_keys = set(bib.keys())
    manifest_keys = {r["bibkey"] for r in manifest}
    missing_in_bib = sorted(manifest_keys - bib_keys)
    if missing_in_bib:
        for k in missing_in_bib:
            failures.append(
                f"manifest bibkey '{k}' has no matching @xxx{{{k}, ...}} in bib"
            )
        print(f"FAIL: {len(missing_in_bib)} manifest bibkey(s) missing from bib")
    else:
        print(f"OK:   all {len(manifest_keys)} manifest bibkeys present in bib")

    # Check 2: every bib entry is in manifest OR has legacy note
    orphan_bib_entries = []
    for bibkey, info in bib.items():
        if bibkey in manifest_keys:
            continue
        if info["has_legacy_note"]:
            continue
        orphan_bib_entries.append(bibkey)
    if orphan_bib_entries:
        for k in orphan_bib_entries:
            failures.append(
                f"bib entry '{k}' is not in manifest and has no legacy "
                f"'note = {{ENGRAM evidence ev_XXXX}}' field"
            )
        print(f"FAIL: {len(orphan_bib_entries)} bib entry/entries not in manifest "
              f"and lacking legacy ENGRAM-evidence note")
    else:
        print(f"OK:   all {len(bib_keys)} bib entries either in manifest or "
              f"have legacy note")

    # Check 3: every non-empty manifest evidence_id is a real ENGRAM evidence node
    if engram_available:
        evidence_ids_in_manifest = [r["evidence_id"] for r in manifest if r["evidence_id"]]
        missing_evidence = []
        for ev_id in evidence_ids_in_manifest:
            if ev_id not in engram:
                missing_evidence.append(ev_id)
        if missing_evidence:
            for ev_id in missing_evidence:
                # Find the manifest line for nicer reporting
                line_info = next(
                    (r for r in manifest if r["evidence_id"] == ev_id),
                    None,
                )
                if line_info:
                    failures.append(
                        f"manifest line {line_info['lineno']}: evidence_id "
                        f"'{ev_id}' not found in ENGRAM evidence nodes"
                    )
                else:
                    failures.append(
                        f"manifest evidence_id '{ev_id}' not found in ENGRAM"
                    )
            print(f"FAIL: {len(missing_evidence)} manifest evidence_id(s) "
                  f"not found in ENGRAM")
        else:
            print(f"OK:   all {len(evidence_ids_in_manifest)} non-empty "
                  f"manifest evidence_ids exist in ENGRAM")
    else:
        print("SKIP: ENGRAM check (db not available)")

    # Check 4: manifest URL matches bib URL for every shared bibkey.
    # arxiv /abs/ vs /html/ vs /pdf/ for the same paper ID are treated as
    # equivalent (canonicalize_url collapses them to "arxiv:NNNN.NNNNN").
    url_mismatches = []
    for r in manifest:
        bk = r["bibkey"]
        if bk not in bib:
            continue  # already reported in Check 1
        bib_url = bib[bk]["url"]
        manifest_url = r["url"]
        if not bib_url or not manifest_url:
            continue
        if canonicalize_url(bib_url) != canonicalize_url(manifest_url):
            url_mismatches.append((bk, r["lineno"], manifest_url, bib_url))
    if url_mismatches:
        for bk, lineno, m_url, b_url in url_mismatches:
            failures.append(
                f"manifest line {lineno}: bibkey '{bk}' URL mismatch (after canonicalization):\n"
                f"    manifest: {m_url}\n"
                f"    bib:      {b_url}"
            )
        print(f"FAIL: {len(url_mismatches)} URL mismatch(es) between manifest and bib")
    else:
        print(f"OK:   all manifest URLs match bib URLs (arxiv-canonicalized)")

    print()
    print("=" * 72)
    print("SOFT CHECKS (warn-only)")
    print("=" * 72)

    # Soft check: ENGRAM evidence nodes with paper-plausible source_url but
    # no manifest entry. Filtered through NON_PAPER_URL_PATTERNS so we only
    # fire on URLs that COULD be paper sources (arxiv, doi, publishers,
    # university repos). file://, github, Anthropic-tooling, encyclopedias,
    # blogs etc. are correctly excluded — they're never paper citations.
    if engram_available:
        manifest_evidence_ids = {r["evidence_id"] for r in manifest if r["evidence_id"]}
        # Also consider legacy notes as "in manifest" for orphan-detection
        legacy_evidence_ids = {info["ev_in_note"] for info in bib.values()
                                if info["ev_in_note"]}
        covered = manifest_evidence_ids | legacy_evidence_ids
        orphans = []
        skipped_non_paper = 0
        for ev_id, source_url in engram.items():
            if not source_url:
                continue  # private/no-URL evidence, intentional
            if ev_id in covered:
                continue
            if is_non_paper_url(source_url):
                skipped_non_paper += 1
                continue
            orphans.append((ev_id, source_url))
        if orphans:
            print(f"WARN: {len(orphans)} ENGRAM evidence node(s) with "
                  f"paper-plausible source_url but no manifest/bib entry:")
            for ev_id, source_url in orphans[:20]:
                print(f"    {ev_id}  {source_url}")
            if len(orphans) > 20:
                print(f"    ... and {len(orphans) - 20} more")
            print(f"  (Filtered out {skipped_non_paper} non-paper URLs via "
                  f"NON_PAPER_URL_PATTERNS — file://, github, anthropic-tooling,")
            print(f"  encyclopedias, blogs, etc. Listed orphans may be deferred")
            print(f"  bib-add candidates worth reviewing.)")
        else:
            print(f"OK:   no orphan ENGRAM evidence with paper-plausible URL "
                  f"(skipped {skipped_non_paper} non-paper URLs via filter)")
    else:
        print("SKIP: ENGRAM orphan check (db not available)")

    print()
    print("=" * 72)
    if failures:
        print(f"RESULT: {len(failures)} hard-check failure(s)")
        print("=" * 72)
        for f in failures:
            print(f"  - {f}")
        return 1
    else:
        print(f"RESULT: all hard checks passed")
        print("=" * 72)
        return 0


if __name__ == "__main__":
    sys.exit(main())
