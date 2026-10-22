#!/usr/bin/env python3
"""Render-oracle check: literal `*` left in the rendered text of the release Markdown.

A conformant CommonMark renderer leaves some emphasis as literal asterisks (a closing
`**` that follows punctuation and precedes a letter is not a closing delimiter, which
bites CJK text where no space follows the punctuation). Hand-rolled converters render
those spans as bold anyway, so a PDF can look right while the paper site shows `**`.

The ORACLE is markdown-it-py, `MarkdownIt('commonmark').enable('table')`. It is never
the PDF builder (tools/pdf_build): the builder's rules are what is in question.
If markdown-it-py cannot be imported the check exits non-zero. A missing oracle is
never a pass.

What counts: render each file, walk the inline text outside code spans, code blocks
and raw HTML. Any literal `*` is a finding (default-deny). Kinds:
  bold    a pair of consecutive `**` runs in one block (reported once, at the opener)
  single  any other `*` run (a lone `*`, an unpaired `**`, or a run of 3+)

Allowlist (data, ALLOWLIST below): a `*` is allowed only when the maximal run of
[A-Za-z0-9*] around it fully matches one of the patterns. `xK*2` and `K*23` are not
allowed.

Modes:
  default      passes iff findings equal the baseline exactly (tools/emphasis_findings_baseline.json):
               a new finding fails, and a baseline entry no longer found fails as stale.
  --gate-zero  fails on any finding (for a version whose source is fixed).
  --write-baseline  rewrite the baseline from the current findings, then exit 0.

Usage:  check_emphasis_render.py [files...] [--baseline PATH] [--gate-zero | --write-baseline]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_FILES = [
    REPO / "paper" / "release" / "engram-paper-v0.5.1.md",
    REPO / "paper" / "release" / "engram-paper-v0.5.1.zh.md",
]
DEFAULT_BASELINE = Path(__file__).resolve().parent / "emphasis_findings_baseline.json"

# Exact tokens only. Each entry: the pattern the maximal [A-Za-z0-9*] run must FULLY
# match (re.fullmatch), and why it is allowed.
ALLOWLIST = [
    {"pattern": r"K\*[2-6]", "reason": "AGM postulate names K*2-K*6"},
]

_WORD = re.compile(r"[A-Za-z0-9*]")
_CODE = "\x00"  # stands in for a code span / raw HTML inside a block's text
CONTEXT = 15


class OracleMissing(RuntimeError):
    pass


def load_oracle():
    try:
        from markdown_it import MarkdownIt
    except ImportError as e:
        raise OracleMissing(
            "oracle missing: markdown-it-py cannot be imported "
            f"({e}); install it (pip install 'markdown-it-py>=3,<4'). "
            "A missing oracle is never a pass.") from e
    return MarkdownIt("commonmark").enable("table")


def label_for(path) -> str:
    p = Path(path).resolve()
    try:
        return p.relative_to(REPO).as_posix()
    except ValueError:
        return p.as_posix()


def block_texts(md_text: str):
    """Yield the visible text of each rendered inline block (code spans masked)."""
    for tok in load_oracle().parse(md_text):
        if tok.type != "inline":
            continue
        parts = []
        for c in tok.children or []:
            if c.type == "text":
                parts.append(c.content)
            elif c.type in ("softbreak", "hardbreak"):
                parts.append("\n")
            elif c.type in ("code_inline", "html_inline"):
                parts.append(_CODE)
            # image alt text is an attribute, not visible text; open/close tags add none
        yield "".join(parts)


def _allowed(text: str, start: int, end: int) -> bool:
    lo, hi = start, end
    while lo > 0 and _WORD.match(text[lo - 1]):
        lo -= 1
    while hi < len(text) and _WORD.match(text[hi]):
        hi += 1
    token = text[lo:hi]
    return any(re.fullmatch(a["pattern"], token) for a in ALLOWLIST)


def _context(text: str, start: int, end: int) -> str:
    window = text[max(0, start - CONTEXT):end + CONTEXT]
    return window.replace("\n", " ").replace(_CODE, "`")


def scan(md_text: str, file_label: str):
    """Return (findings, allowed_count). A finding is {file, kind, context}."""
    findings, allowed = [], 0
    for text in block_texts(md_text):
        bold_open = None  # a `**` run waiting for its partner
        for m in re.finditer(r"\*+", text):
            if _allowed(text, m.start(), m.end()):
                allowed += 1
                continue
            if len(m.group()) == 2:
                if bold_open is None:
                    bold_open = m
                else:
                    findings.append({"file": file_label, "kind": "bold",
                                     "context": _context(text, bold_open.start(), bold_open.end())})
                    bold_open = None
                continue
            findings.append({"file": file_label, "kind": "single",
                             "context": _context(text, m.start(), m.end())})
        if bold_open is not None:  # unpaired `**`
            findings.append({"file": file_label, "kind": "single",
                             "context": _context(text, bold_open.start(), bold_open.end())})
    return findings, allowed


def _key(f):
    return (f["file"], f["kind"], f["context"])


def _fmt(f):
    return f"{f['file']} [{f['kind']}] ...{f['context']}..."


def check(paths, baseline_path, gate_zero=False):
    """Return (exit_code, report_lines)."""
    findings = []
    for p in paths:
        f, _ = scan(Path(p).read_text(encoding="utf-8"), label_for(p))
        findings.extend(f)
    lines = []
    if gate_zero:
        for f in findings:
            lines.append("finding: " + _fmt(f))
        lines.append(f"gate-zero: {len(findings)} finding(s)")
        return (1 if findings else 0), lines

    base = json.loads(Path(baseline_path).read_text(encoding="utf-8"))["findings"]
    have, want = Counter(map(_key, findings)), Counter(map(_key, base))
    new = have - want
    stale = want - have
    for k in sorted(new.elements()):
        lines.append("new finding: " + _fmt(dict(zip(("file", "kind", "context"), k))))
    for k in sorted(stale.elements()):
        lines.append("stale baseline entry (no longer found): "
                     + _fmt(dict(zip(("file", "kind", "context"), k))))
    lines.append(f"{len(findings)} finding(s), baseline {len(base)}: "
                 f"{sum(new.values())} new, {sum(stale.values())} stale")
    return (1 if (new or stale) else 0), lines


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--gate-zero", action="store_true")
    mode.add_argument("--write-baseline", action="store_true")
    args = ap.parse_args(argv)
    paths = [Path(f) for f in args.files] or DEFAULT_FILES
    try:
        load_oracle()
        if args.write_baseline:
            findings = []
            for p in paths:
                findings.extend(scan(Path(p).read_text(encoding="utf-8"), label_for(p))[0])
            Path(args.baseline).write_text(
                json.dumps({"oracle": "markdown-it-py MarkdownIt('commonmark').enable('table')",
                            "findings": findings}, ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8")
            print(f"wrote {len(findings)} finding(s) to {args.baseline}")
            return 0
        rc, lines = check(paths, args.baseline, args.gate_zero)
    except OracleMissing as e:
        print(str(e), file=sys.stderr)
        return 2
    print("\n".join(lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
