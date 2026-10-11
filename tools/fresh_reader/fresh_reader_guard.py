"""Run-time no-tools guard for the fresh-reader run (engram-paper, part of #55).

The fresh-reader persona tells the model it "cannot look ahead, search the
web, or open any file" -- that has been true only because the
`fresh-reader-notools.yml` overlay is passed via `patches=` in
`fresh_reader_run.run_live()`; nothing checked it at run time. This module
turns the persona's sentence into a checked fact: after the first turn,
decode the dsh session store and refuse to continue if any tool reached the
model.

stdlib only (plus the OPTIONAL `zstandard` module, imported lazily -- its
absence is not a hard dependency, since the `zstd` CLI is an accepted
fallback; see `decode_session`).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


class GuardError(RuntimeError):
    """Could not verify the no-tools invariant. Always a refusal, never a
    pass -- raised for every failure mode short of a clean, fully-decoded
    confirmation (missing session file, ambiguous session file, no decoder
    available, malformed JSONL, no request/header record)."""


class NoToolsViolation(GuardError):
    """Verified, and tools WERE present in at least one request/header
    record. `tool_names` is the sorted union across every header that
    carried tools."""

    def __init__(self, tool_names: list[str]):
        self.tool_names = tool_names
        super().__init__(
            "fresh-reader session sent tool(s) to the model despite the "
            "no-tools overlay: " + ", ".join(tool_names)
        )


@dataclass
class NoToolsReport:
    session_file: Path
    header_count: int
    tool_names_per_header: list[list[str]]


def find_session_file(dsh_home: Path, session_id: str) -> Path:
    """The store lives at `<dsh_home>/sessions/<any one dir>/<session_id>/
    session.v3.jsonl.zstd`. Exactly one match -> return it. Zero or two-or-
    more matches -> GuardError (never pick one silently)."""
    pattern = f"sessions/*/{session_id}/session.v3.jsonl.zstd"
    matches = sorted(dsh_home.glob(pattern))
    if len(matches) == 0:
        raise GuardError(
            f"no session file found under {dsh_home} for session_id "
            f"{session_id!r} (looked for {dsh_home / pattern})"
        )
    if len(matches) > 1:
        listed = "\n  ".join(str(m) for m in matches)
        raise GuardError(
            f"ambiguous session file for session_id {session_id!r} under "
            f"{dsh_home}: {len(matches)} matches found, refusing to pick "
            f"one:\n  {listed}"
        )
    return matches[0]


def _import_zstandard():
    """Isolated so tests can monkeypatch this one function to simulate the
    module being unimportable, without touching real import machinery."""
    try:
        import zstandard  # type: ignore
    except ImportError:
        return None
    return zstandard


def decode_session(path: Path) -> bytes:
    """Use the `zstandard` module if importable; else the `zstd` CLI
    (`zstd -dc <path>`), checking its exit status; if neither is available
    -> GuardError. Absence of a decoder is a refusal, not a pass."""
    zstandard = _import_zstandard()
    if zstandard is not None:
        cctx = zstandard.ZstdDecompressor()
        with path.open("rb") as fh:
            return cctx.decompress(fh.read())

    zstd_bin = shutil.which("zstd")
    if zstd_bin is not None:
        result = subprocess.run(
            [zstd_bin, "-dc", str(path)],
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            raise GuardError(
                f"zstd CLI failed decoding {path} (exit {result.returncode}): "
                f"{result.stderr.decode('utf-8', errors='replace').strip()}"
            )
        return result.stdout

    raise GuardError("cannot verify: no zstd decoder")


def header_tool_names(jsonl_bytes: bytes) -> list[list[str]]:
    """Input is the decoded JSONL (one JSON object per line; blank lines
    ignored; a non-JSON line -> GuardError, not silently skipped). Selects
    records with `"type" == "request/header"`. For each, tool names are
    `[t["name"] for t in rec["data"]["header"].get("tools", [])]`. A header
    with no `tools` key, or `"tools": []`, both yield `[]`. Zero header
    records -> GuardError.

    A request/header record that is missing `data`, missing `data.header`,
    or whose `tools` is not a list, also raises GuardError -- naming the
    record's `seq` field when present, else its 0-based line index in the
    input -- rather than letting a bare KeyError/TypeError escape from a
    malformed record."""
    result: list[list[str]] = []
    for idx, raw_line in enumerate(jsonl_bytes.decode("utf-8").splitlines()):
        line = raw_line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            raise GuardError(
                f"non-JSON line in decoded session store: {line!r} ({exc})"
            ) from exc
        if rec.get("type") != "request/header":
            continue
        record_ref = f"seq={rec['seq']!r}" if "seq" in rec else f"line-index={idx}"
        if "data" not in rec:
            raise GuardError(
                f"request/header record ({record_ref}) missing 'data': {rec!r}"
            )
        data = rec["data"]
        if "header" not in data:
            raise GuardError(
                f"request/header record ({record_ref}) missing 'data.header': {rec!r}"
            )
        header = data["header"]
        tools = header.get("tools", [])
        if not isinstance(tools, list):
            raise GuardError(
                f"request/header record ({record_ref}) has a non-list 'tools' "
                f"({type(tools).__name__}): {tools!r}"
            )
        names: list[str] = []
        for pos, entry in enumerate(tools):
            if not isinstance(entry, dict) or "name" not in entry:
                raise GuardError(
                    f"request/header record ({record_ref}) has a malformed "
                    f"tool entry at position {pos}: {entry!r}"
                )
            names.append(entry["name"])
        result.append(names)

    if not result:
        raise GuardError("no request/header record found in decoded session store")

    return result


def assert_no_tools(dsh_home: Path, session_id: str) -> NoToolsReport:
    """Composes find_session_file + decode_session + header_tool_names. If
    ANY header's list is non-empty -> NoToolsViolation whose `tool_names`
    is the sorted union, and whose message lists them. Otherwise returns
    the report."""
    session_file = find_session_file(dsh_home, session_id)
    jsonl_bytes = decode_session(session_file)
    tool_names_per_header = header_tool_names(jsonl_bytes)

    union: set[str] = set()
    for names in tool_names_per_header:
        union.update(names)
    if union:
        raise NoToolsViolation(sorted(union))

    return NoToolsReport(
        session_file=session_file,
        header_count=len(tool_names_per_header),
        tool_names_per_header=tool_names_per_header,
    )
