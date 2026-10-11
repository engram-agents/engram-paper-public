#!/usr/bin/env python3
"""bib_bootstrap.py — generate citations.bib from ENGRAM evidence nodes.

ONE-TIME bootstrap. Reads the live ENGRAM SQLite, finds every evidence node
with a citation-worthy URL (arxiv, DOI, .pdf, openreview, plato.stanford.edu,
ACL anthology), and emits a BibTeX file plus a manifest mapping each
evidence_id ↔ bibkey.

Going forward, new papers should be captured with `tools/bib_add.py <url>`
which both fetches metadata and writes the bib + ENGRAM evidence atomically.

Output:
    bibliography/citations.bib       — BibTeX file (paper-ready)
    bibliography/citations.manifest  — TSV: evidence_id, bibkey, url, title

Bibkey scheme:
    arxiv:1234.56789           → arxiv-1234.56789
    arxiv:abs/1234.56789       → arxiv-1234.56789
    arxiv html versions        → arxiv-1234.56789 (strip vN)
    SEP entries                → sep-{slug}
    DOIs                       → doi-{slug}
    Direct PDFs                → pdf-{evidence_id} (fallback; needs upgrade later)
    Other academic             → {evidence_id} (fallback)

Idempotent: running twice produces identical output.
"""

import os
import re
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path.home() / ".engram" / "knowledge.db"
REPO_ROOT = Path(__file__).resolve().parent.parent
BIB_OUT = REPO_ROOT / "bibliography" / "citations.bib"
MANIFEST_OUT = REPO_ROOT / "bibliography" / "citations.manifest"


# Patterns that mark a URL as academic / citation-worthy.
ACADEMIC_PATTERNS = (
    "arxiv.org",
    ".pdf",
    "doi.org",
    "openreview.net",
    "plato.stanford.edu",
    "aclanthology.org",
    "aclweb.org",
    "semanticscholar.org",
    "papers.nips.cc",
    "papers.neurips.cc",
    "proceedings.mlr.press",
)


def is_academic(url: str) -> bool:
    return any(p in url for p in ACADEMIC_PATTERNS)


_ARXIV_ID_RE = re.compile(r"arxiv\.org/(?:abs|html|pdf)/(\d{4}\.\d{4,5})", re.IGNORECASE)
_DOI_SLUG_RE = re.compile(r"doi\.org/(.+)$", re.IGNORECASE)
_SEP_SLUG_RE = re.compile(r"plato\.stanford\.edu/entries/([a-zA-Z0-9_-]+)", re.IGNORECASE)
_NONALNUM = re.compile(r"[^a-zA-Z0-9_-]")


def slugify(text: str, maxlen: int = 40) -> str:
    """Lower-case, replace non-alnum with hyphens, collapse repeats, trim."""
    s = _NONALNUM.sub("-", text.lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:maxlen]


def derive_bibkey(evidence_id: str, url: str) -> str:
    """Stable bibkey from URL when possible; falls back to evidence_id."""
    m = _ARXIV_ID_RE.search(url)
    if m:
        return f"arxiv-{m.group(1)}"
    m = _SEP_SLUG_RE.search(url)
    if m:
        return f"sep-{m.group(1)}"
    m = _DOI_SLUG_RE.search(url)
    if m:
        return f"doi-{slugify(m.group(1))}"
    if url.lower().endswith(".pdf"):
        return f"pdf-{evidence_id}"
    return evidence_id


def bibtex_escape(text: str) -> str:
    """BibTeX special chars + line-break safety."""
    if text is None:
        return ""
    # & % $ # _ { } need escaping; ~ and ^ too
    text = text.replace("\\", r"\textbackslash ")
    for ch in ("&", "%", "$", "#", "_"):
        text = text.replace(ch, f"\\{ch}")
    text = text.replace("{", r"\{").replace("}", r"\}")
    text = text.replace("\n", " ").replace("\r", " ")
    return text.strip()


def emit_entry(bibkey: str, url: str, title: str, source_date: str,
               domain: str, evidence_id: str) -> str:
    """Build one BibTeX entry. Conservative — uses @misc when type is uncertain."""
    title_esc = bibtex_escape(title)
    year = ""
    month = ""
    if source_date:
        # source_date may be 'YYYY-MM-DD', 'YYYY-MM', or 'YYYY'
        parts = source_date.split("-")
        if len(parts) >= 1 and parts[0].isdigit():
            year = parts[0]
        if len(parts) >= 2 and parts[1].isdigit():
            month_num = int(parts[1])
            if 1 <= month_num <= 12:
                month = ["jan", "feb", "mar", "apr", "may", "jun",
                         "jul", "aug", "sep", "oct", "nov", "dec"][month_num - 1]

    # Try to detect entry type from URL.
    if "arxiv.org" in url:
        entry_type = "@misc"  # arxiv papers — use eprint for the canonical handle
        m = _ARXIV_ID_RE.search(url)
        eprint_id = m.group(1) if m else ""
    elif "plato.stanford.edu" in url:
        entry_type = "@misc"
        eprint_id = ""
    elif url.lower().endswith(".pdf"):
        entry_type = "@misc"
        eprint_id = ""
    else:
        entry_type = "@misc"
        eprint_id = ""

    lines = [f"{entry_type}{{{bibkey},"]
    lines.append(f"  title        = {{{title_esc}}},")
    if year:
        lines.append(f"  year         = {{{year}}},")
    if month:
        lines.append(f"  month        = {month},")
    if eprint_id:
        lines.append(f"  eprint       = {{{eprint_id}}},")
        lines.append(f"  archivePrefix = {{arXiv}},")
    if domain:
        lines.append(f"  howpublished = {{{bibtex_escape(domain)}}},")
    lines.append(f"  url          = {{{url}}},")
    lines.append(f"  note         = {{ENGRAM evidence {evidence_id}}},")
    lines.append("}")
    return "\n".join(lines)


def main() -> int:
    if not DB_PATH.exists():
        print(f"ERROR: ENGRAM DB not found at {DB_PATH}", file=sys.stderr)
        return 2

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """SELECT id, source_url, source_title, source_date, source_domain
           FROM nodes
           WHERE type='evidence' AND is_current=1
           AND source_url IS NOT NULL AND source_url != ''
           ORDER BY id"""
    ).fetchall()

    academic = [r for r in rows if is_academic(r["source_url"])]
    print(f"Total evidence: {len(rows)} | academic-eligible: {len(academic)}")

    # First pass — assign bibkeys, dedupe identical bibkeys (different evidence
    # nodes citing same paper get the same bibkey, fine).
    seen_bibkeys: dict[str, list] = {}
    for r in academic:
        key = derive_bibkey(r["id"], r["source_url"])
        seen_bibkeys.setdefault(key, []).append(r)

    BIB_OUT.parent.mkdir(parents=True, exist_ok=True)
    bib_lines = [
        "% citations.bib — auto-generated by tools/bib_bootstrap.py",
        "% Source of truth: ENGRAM evidence nodes (~/.engram/knowledge.db).",
        "% Regenerate via tools/bib_bootstrap.py; for new papers prefer tools/bib_add.py.",
        "",
    ]
    manifest_lines = ["evidence_id\tbibkey\turl\ttitle"]

    written = 0
    for bibkey, ev_rows in sorted(seen_bibkeys.items()):
        # Pick the canonical evidence_id (lowest id) as the primary; keep all
        # in the manifest so we can audit duplicates.
        primary = min(ev_rows, key=lambda r: r["id"])
        bib_lines.append(emit_entry(
            bibkey=bibkey,
            url=primary["source_url"],
            title=primary["source_title"] or "",
            source_date=primary["source_date"] or "",
            domain=primary["source_domain"] or "",
            evidence_id=primary["id"],
        ))
        bib_lines.append("")
        written += 1
        for ev in ev_rows:
            title = (ev["source_title"] or "").replace("\t", " ")
            manifest_lines.append(f"{ev['id']}\t{bibkey}\t{ev['source_url']}\t{title}")

    BIB_OUT.write_text("\n".join(bib_lines))
    MANIFEST_OUT.write_text("\n".join(manifest_lines) + "\n")

    duplicates = sum(1 for k, v in seen_bibkeys.items() if len(v) > 1)
    print(f"Wrote {written} BibTeX entries → {BIB_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote {len(academic)} manifest rows → {MANIFEST_OUT.relative_to(REPO_ROOT)}")
    if duplicates:
        print(f"Note: {duplicates} bibkey(s) cover multiple evidence nodes "
              "(same paper cited from different ENGRAM nodes).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
