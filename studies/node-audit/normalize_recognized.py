#!/usr/bin/env python3
"""normalize_recognized.py: PROTOCOL.md Amendment 5, the `recognized.txt` addendum.

`analyze_arms.py` clause A2 wants exactly one id per data line. One reader locked a recognized file
before that rule existed. This tool makes a COPY under one mapping, chosen by Kepler and pinned
below: keep the first id of each multi-id line (a `LATE` token is kept with it) and drop the line
that declares itself "not mine". The input is never modified; `analyze_arms.py` is not either.

    python normalize_recognized.py --in PATH --out PATH --reader NAME

Contract (tests/test_node_audit_normalize_recognized.py):

R1  Pinned expectation. EXPECTED holds, per reader, the stripped / dropped / untouched / ids_out
    counts and the drop phrase. Any other reader expects stripped 0, dropped [] and no phrase (a
    no-op): its multi-id lines are refused, nothing is silently reshaped.
R2  Per data line (non-blank, not starting with `#`, numbered by physical line, 1-based):
    - a line number in `dropped`: the drop phrase must be PRESENT (case-insensitive substring); the
      line is removed;
    - every other data line: when the reader has a drop phrase, it must be ABSENT;
    - 0 ID_TOKEN matches -> refuse; exactly 1 -> written byte-for-byte (untouched); more than 1 ->
      rewritten as the FIRST id, plus ` LATE` if LATE_TOKEN matched anywhere on the original line,
      plus the original line ending.
    Blank and `#` lines pass through byte-for-byte and are not counted.
R3  Before ANY write: stripped, dropped, untouched and ids_out (the number of output data lines)
    must each equal the pin exactly, per field (a total-only check is a defect), and no two output
    lines may share a first id. Otherwise refuse.
R4  A refusal names LINE NUMBERS and the failed field only, never line text and never an id; every
    offending line is listed; exit 1, `REFUSED:` on stderr; nothing is written (temp file in the
    output directory, os.replace only after every assertion passed).
R5  Safety: refuse when --out exists, is the same file as --in, its directory is missing, or --in
    is missing.
R6  Deterministic: the same input gives byte-identical output.
R7  Report: `stripped:`, `dropped:`, `untouched:`, `ids_out:` lines, then `sha256 <hex> <out>`.
R8  The output parses with analyze_arms.parse_recognized and LATE ids survive.

ID_TOKEN and LATE_TOKEN are imported from analyze_arms.py, never re-defined here.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load_arms():
    """Import analyze_arms.py from this directory, reusing an already-imported copy of the same
    file (the pattern analyze_arms.py uses for analyze.py)."""
    target = HERE / "analyze_arms.py"
    cached = sys.modules.get("analyze_arms")
    if cached is not None and Path(getattr(cached, "__file__", None) or "").resolve() == target:
        return cached
    spec = importlib.util.spec_from_file_location("analyze_arms", target)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["analyze_arms"] = mod
    spec.loader.exec_module(mod)
    return mod


arms = _load_arms()
ID_TOKEN = arms.ID_TOKEN
LATE_TOKEN = arms.LATE_TOKEN

# Amendment 5 addendum: a measurement with a pre-stated answer, not an open transform.
EXPECTED = {
    "ariadne": {"stripped": 16, "dropped": [44], "untouched": 27, "ids_out": 43, "drop_phrase": "not mine"},
}
FIELDS = ("stripped", "dropped", "untouched", "ids_out")


class NormalizeRefused(Exception):
    """Raised for every refusal; messages carry line numbers and field names only."""


def expected_for(reader):
    if reader in EXPECTED:
        e = dict(EXPECTED[reader])
        e["dropped"] = list(e["dropped"])
        return e
    # No-op: nothing stripped, nothing dropped; untouched / ids_out are not pinned.
    return {"stripped": 0, "dropped": [], "untouched": None, "ids_out": None, "drop_phrase": None}


def _split_ending(line):
    for ending in (b"\r\n", b"\n", b"\r"):
        if line.endswith(ending):
            return line[: -len(ending)], ending
    return line, b""


def transform(lines, exp):
    """Apply the mapping to raw lines (bytes, endings included).

    Returns (out_lines, actual, problems). `problems` are (sortkey, text) pairs naming line numbers
    and fields only. When it is non-empty the caller must not write anything."""
    out, problems = [], []
    actual = {"stripped": 0, "dropped": [], "untouched": 0, "ids_out": 0}
    phrase = exp["drop_phrase"].lower() if exp["drop_phrase"] else None
    drop_lines = set(exp["dropped"])
    seen_first = set()
    for n, raw in enumerate(lines, 1):
        body, ending = _split_ending(raw)
        try:
            text = body.decode("utf-8")
        except UnicodeDecodeError:
            problems.append((n, f"line {n}: not readable as UTF-8"))
            out.append(raw)
            continue
        s = text.strip()
        if not s or s.startswith("#"):
            out.append(raw)
            continue
        has_phrase = phrase is not None and phrase in text.lower()
        if n in drop_lines:
            if not has_phrase:
                problems.append((n, f"line {n}: drop phrase absent on a line to be dropped"))
            actual["dropped"].append(n)
            continue
        if phrase is not None and has_phrase:
            problems.append((n, f"line {n}: drop phrase present on a line not to be dropped"))
        toks = ID_TOKEN.findall(text)
        if not toks:
            problems.append((n, f"line {n}: no id"))
            out.append(raw)
            continue
        if len(toks) == 1:
            actual["untouched"] += 1
            new = raw
        else:
            actual["stripped"] += 1
            late = " LATE" if LATE_TOKEN.search(text) else ""
            new = (toks[0] + late).encode("utf-8") + ending
        if toks[0] in seen_first:
            problems.append((n, f"line {n}: duplicate first id"))
        seen_first.add(toks[0])
        actual["ids_out"] += 1
        out.append(new)
    for f in FIELDS:  # R3: per field, never a total
        if exp[f] is not None and exp[f] != actual[f]:
            problems.append((10**9, f"field {f}: expected {exp[f]}, actual {actual[f]}"))
    problems.sort(key=lambda p: p[0])
    return out, actual, problems


def normalize(src, out, reader):
    """Build the normalized copy and write it atomically. Returns (actual counts, sha256 hex).
    Raises NormalizeRefused (nothing written) on any refusal."""
    src, out = Path(src), Path(out)
    if not src.is_file():
        raise NormalizeRefused("--in is not a readable file")
    if src.resolve() == out.resolve() or (out.exists() and os.path.samefile(src, out)):
        raise NormalizeRefused("--out is the same file as --in; the locked input is never overwritten")
    if os.path.lexists(out):
        raise NormalizeRefused("--out already exists; refusing to overwrite")
    if not out.resolve().parent.is_dir():
        raise NormalizeRefused("--out directory does not exist")

    exp = expected_for(reader)
    new_lines, actual, problems = transform(src.read_bytes().splitlines(keepends=True), exp)
    if problems:
        body = "\n".join(f"  - {text}" for _, text in problems)
        raise NormalizeRefused(f"{len(problems)} problem(s); nothing written:\n{body}")

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
    return actual, hashlib.sha256(data).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Amendment 5 addendum: normalize a recognized.txt copy.")
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--reader", required=True)
    args = ap.parse_args(argv)
    try:
        actual, digest = normalize(args.src, args.out, args.reader)
    except NormalizeRefused as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1
    for f in FIELDS:
        print(f"{f}: {actual[f]}")
    print(f"sha256 {digest} {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
