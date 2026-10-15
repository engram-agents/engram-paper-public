#!/usr/bin/env python3
"""normalize_labels.py: PROTOCOL.md Amendment 5, the one pinned label normalization.

One reader's locked verdict file writes some loose verdicts as `loose:<check>` where the analysis
expects `loose`. This tool makes a COPY in which a verdict whose value is exactly `loose:` followed
by the name of the check it sits in becomes `loose`. The input file is never modified. Nothing else
is touched. The copy then goes through `analyze.validate_verdicts` like any other verdict file.

    python normalize_labels.py --in PATH --out PATH --reader NAME

Contract (tests/test_node_audit_normalize_labels.py, one or more tests per clause):

N1  Pinned expected delta. EXPECTED_DELTA fixes, per reader, how many cells change in each check.
    Any reader not listed expects zero changes. After the mapping is computed in memory, the
    per-check count of changed cells must EQUAL the reader's expected delta exactly (a missing key
    is 0); otherwise refuse, stating expected vs actual per check. This runs before anything is
    written.
N2  Mapping. For each row, for each check key under `checks`: if `verdict` is a str starting with
    `loose:`, let s be the remainder. s not in ALL_CHECKS -> refuse (unknown check name). s != the
    enclosing check key -> refuse (mismatched prefix). Otherwise the verdict becomes `loose`. No
    other field or value is altered.
N3  Refuse loudly, never partially. A refusal names EVERY offending cell (id, check, value), exits
    non-zero and writes NO output file: the output is built fully in memory, written to a temp file
    in the output directory, and moved into place with os.replace only after every assertion passed.
N4  Byte fidelity. A line with no changed cell is written byte-for-byte as read, line ending
    included. A changed line is re-serialized with json.dumps(obj, ensure_ascii=False) plus the
    original line ending.
N5  No-op control. A file with no `loose:` values, with a reader whose expected delta is empty,
    comes out byte-identical.
N6  Determinism. The same input always yields byte-identical output.
N7  The output validates: check and verdict names are read from analyze.py (never re-listed here).
N8  Safety. Refuse when --out exists (symlinks included) or resolves to the same file as --in.
N9  Report. On success print one line per check with its changed count, then `sha256 <hex> <out>`.

Stdlib only, plus analyze.py from this directory.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load_analyze():
    """Import analyze.py from this directory, reusing an already-imported copy of the same file
    (same loader as analyze_arms.py) so exception classes stay identical for any caller."""
    target = HERE / "analyze.py"
    cached = sys.modules.get("analyze")
    if cached is not None and Path(getattr(cached, "__file__", None) or "").resolve() == target:
        return cached
    spec = importlib.util.spec_from_file_location("analyze", target)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


an = _load_analyze()
ALL_CHECKS = an.ALL_CHECKS
VERDICTS = an.VERDICTS

LOOSE = "loose"
PREFIX = LOOSE + ":"
assert LOOSE in VERDICTS

# Amendment 5, rider 1: a measurement with a pre-stated answer, not an open transform.
EXPECTED_DELTA = {"zephyr": {"type": 10, "placement": 13, "chain-overreach": 14}}


class NormalizeRefused(Exception):
    """Raised for every refusal; the message names everything the user must see."""


def expected_delta_for(reader):
    return dict(EXPECTED_DELTA.get(reader, {}))


def _split_ending(line):
    for ending in (b"\r\n", b"\n", b"\r"):
        if line.endswith(ending):
            return line[: -len(ending)], ending
    return line, b""


def normalize_lines(lines):
    """Map `loose:<own check>` -> `loose` over raw lines (bytes, line endings included).

    Returns (new_lines, counts, problems). `counts` holds only checks with at least one change.
    `problems` lists every offending cell or unreadable line; when it is non-empty the caller
    must not write anything. Lines with no changed cell are returned as the very same bytes."""
    new_lines, counts, problems = [], {}, []
    for lineno, raw in enumerate(lines, 1):
        body, ending = _split_ending(raw)
        if not body.strip():
            new_lines.append(raw)
            continue
        try:
            obj = json.loads(body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as e:
            problems.append(f"line {lineno}: not readable as JSON ({e})")
            new_lines.append(raw)
            continue
        changed = False
        checks = obj.get("checks") if isinstance(obj, dict) else None
        if isinstance(checks, dict):
            for name, cell in checks.items():
                v = cell.get("verdict") if isinstance(cell, dict) else None
                if not (isinstance(v, str) and v.startswith(PREFIX)):
                    continue
                rest = v[len(PREFIX):]
                where = f"{obj.get('id')!r} check {name}: value {v!r}"
                if rest not in ALL_CHECKS:
                    problems.append(f"{where}: unknown check name {rest!r}")
                elif rest != name:
                    problems.append(f"{where}: mismatched prefix (sits in check {name!r})")
                else:
                    cell["verdict"] = LOOSE
                    counts[name] = counts.get(name, 0) + 1
                    changed = True
        if changed:
            new_lines.append(json.dumps(obj, ensure_ascii=False).encode("utf-8") + ending)
        else:
            new_lines.append(raw)
    return new_lines, counts, problems


def _assert_delta(reader, counts):
    expected = expected_delta_for(reader)
    names = list(ALL_CHECKS) + sorted(set(expected) | set(counts) - set(ALL_CHECKS))
    bad = [n for n in names if expected.get(n, 0) != counts.get(n, 0)]
    if bad:
        rows = "\n".join(
            f"  - {n}: expected {expected.get(n, 0)}, actual {counts.get(n, 0)}" for n in names
        )
        raise NormalizeRefused(
            f"reader {reader!r}: changed-cell counts differ from the pinned expected delta "
            f"(mismatch in {bad}):\n{rows}"
        )


def normalize(src, out, reader):
    """Build the normalized copy and write it atomically. Returns (counts, sha256 hex).
    Raises NormalizeRefused (nothing written) on any refusal."""
    src, out = Path(src), Path(out)
    if not src.is_file():
        raise NormalizeRefused(f"--in {src} is not a readable file")
    if src.resolve() == out.resolve() or (out.exists() and os.path.samefile(src, out)):
        raise NormalizeRefused(f"--out {out} is the same file as --in; the locked input is never overwritten")
    if os.path.lexists(out):
        raise NormalizeRefused(f"--out {out} already exists; refusing to overwrite")
    if not out.resolve().parent.is_dir():
        raise NormalizeRefused(f"--out directory {out.resolve().parent} does not exist")

    new_lines, counts, problems = normalize_lines(src.read_bytes().splitlines(keepends=True))
    if problems:
        body = "\n".join(f"  - {p}" for p in problems)
        raise NormalizeRefused(f"{len(problems)} offending cell(s)/line(s); nothing written:\n{body}")
    _assert_delta(reader, counts)  # N1: before anything is written

    data = b"".join(new_lines)
    fd, tmp = tempfile.mkstemp(dir=str(out.resolve().parent), prefix=".normalize-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, out)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return counts, hashlib.sha256(data).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Amendment 5: normalize `loose:<check>` labels on a copy.")
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--reader", required=True)
    args = ap.parse_args(argv)
    try:
        counts, digest = normalize(args.src, args.out, args.reader)
    except NormalizeRefused as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1
    for name in ALL_CHECKS:
        print(f"{name}: {counts.get(name, 0)}")
    print(f"sha256 {digest} {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
