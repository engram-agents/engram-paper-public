"""Contract tests for `paper.review.tools.fresh_reader_guard`, written BEFORE
the implementation per spec-no-tools-guard.md — expected to fail with an
ImportError until the module exists.

Uses the `tests/__init__.py` package so `paper.review.tools.fresh_reader_guard`
imports as an absolute package regardless of pytest's invocation directory,
matching the existing `tests/test_render_apparatus.py` convention.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from paper.review.tools.fresh_reader_guard import (
    GuardError,
    NoToolsViolation,
    assert_no_tools,
    decode_session,
    find_session_file,
    header_tool_names,
)

FIXTURES = Path(__file__).parent / "fixtures" / "fresh_reader"
WITH_TOOLS_RECORD = json.loads((FIXTURES / "request-header-with-tools.json").read_text())
NO_TOOLS_RECORD = json.loads((FIXTURES / "request-header-no-tools.json").read_text())

ZSTD_ON_PATH = shutil.which("zstd") is not None


# ── find_session_file ────────────────────────────────────────────────────


def _make_session_dir(dsh_home: Path, subdir: str, session_id: str) -> Path:
    session_dir = dsh_home / "sessions" / subdir / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    session_file = session_dir / "session.v3.jsonl.zstd"
    session_file.write_bytes(b"placeholder")
    return session_file


def test_find_session_file_exactly_one_match(tmp_path):
    dsh_home = tmp_path / "dsh-home"
    expected = _make_session_dir(dsh_home, "workspace-abc", "sess-1")
    found = find_session_file(dsh_home, "sess-1")
    assert found == expected


def test_find_session_file_zero_matches_raises(tmp_path):
    dsh_home = tmp_path / "dsh-home"
    (dsh_home / "sessions").mkdir(parents=True)
    with pytest.raises(GuardError) as exc_info:
        find_session_file(dsh_home, "sess-missing")
    msg = str(exc_info.value)
    assert str(dsh_home) in msg
    assert "sess-missing" in msg


def test_find_session_file_two_matches_raises_and_lists_both(tmp_path):
    dsh_home = tmp_path / "dsh-home"
    first = _make_session_dir(dsh_home, "workspace-a", "sess-dup")
    second = _make_session_dir(dsh_home, "workspace-b", "sess-dup")
    with pytest.raises(GuardError) as exc_info:
        find_session_file(dsh_home, "sess-dup")
    msg = str(exc_info.value)
    assert str(first) in msg
    assert str(second) in msg


# ── decode_session ───────────────────────────────────────────────────────


@pytest.mark.skipif(not ZSTD_ON_PATH, reason="zstd CLI not on PATH")
def test_decode_session_via_cli(tmp_path):
    payload = b'{"type": "session"}\n{"type": "user/message"}\n'
    src = tmp_path / "plain.jsonl"
    src.write_bytes(payload)
    compressed = tmp_path / "session.v3.jsonl.zstd"
    subprocess.run(
        ["zstd", "-f", "-o", str(compressed), str(src)],
        check=True,
        capture_output=True,
    )
    decoded = decode_session(compressed)
    assert decoded == payload


def test_decode_session_via_zstandard_module(tmp_path, monkeypatch):
    pytest.importorskip("zstandard")
    import zstandard

    payload = b'{"type": "session"}\n'
    compressed_path = tmp_path / "session.v3.jsonl.zstd"
    cctx = zstandard.ZstdCompressor()
    compressed_path.write_bytes(cctx.compress(payload))
    decoded = decode_session(compressed_path)
    assert decoded == payload


def test_decode_session_no_decoder_available_raises(tmp_path, monkeypatch):
    import paper.review.tools.fresh_reader_guard as guard_mod

    monkeypatch.setattr(guard_mod, "_import_zstandard", lambda: None)
    monkeypatch.setattr(shutil, "which", lambda name: None)

    bogus = tmp_path / "session.v3.jsonl.zstd"
    bogus.write_bytes(b"irrelevant")
    with pytest.raises(GuardError, match="no zstd decoder"):
        decode_session(bogus)


# ── header_tool_names ────────────────────────────────────────────────────


def _build_jsonl(*records: dict, blank_lines: bool = False) -> bytes:
    lines = []
    for i, rec in enumerate(records):
        lines.append(json.dumps(rec))
        if blank_lines and i == 0:
            lines.append("")
    return ("\n".join(lines) + "\n").encode("utf-8")


def test_header_tool_names_with_tools():
    filler_session = {"type": "session"}
    filler_msg = {"type": "user/message"}
    jsonl = _build_jsonl(filler_session, WITH_TOOLS_RECORD, filler_msg)
    result = header_tool_names(jsonl)
    assert len(result) == 1
    assert len(result[0]) == 25
    assert "bash" in result[0]
    assert "read" in result[0]
    assert "web_search" in result[0]
    assert "write" in result[0]


def test_header_tool_names_no_tools_key_yields_empty_list():
    jsonl = _build_jsonl({"type": "session"}, NO_TOOLS_RECORD)
    result = header_tool_names(jsonl)
    assert result == [[]]


def test_header_tool_names_empty_tools_list_yields_empty_list():
    rec = {
        "type": "request/header",
        "data": {"header": {"tools": []}},
    }
    jsonl = _build_jsonl(rec)
    result = header_tool_names(jsonl)
    assert result == [[]]


def test_header_tool_names_blank_lines_ignored():
    jsonl = _build_jsonl({"type": "session"}, NO_TOOLS_RECORD, blank_lines=True)
    result = header_tool_names(jsonl)
    assert result == [[]]


def test_header_tool_names_non_json_line_raises():
    jsonl = b'{"type": "session"}\nnot json at all\n' + _build_jsonl(NO_TOOLS_RECORD)
    with pytest.raises(GuardError):
        header_tool_names(jsonl)


def test_header_tool_names_zero_header_records_raises():
    jsonl = _build_jsonl({"type": "session"}, {"type": "user/message"})
    with pytest.raises(GuardError, match="no request/header record"):
        header_tool_names(jsonl)


def test_header_tool_names_multiple_headers_in_order():
    jsonl = _build_jsonl(NO_TOOLS_RECORD, WITH_TOOLS_RECORD)
    result = header_tool_names(jsonl)
    assert len(result) == 2
    assert result[0] == []
    assert len(result[1]) == 25


def test_header_tool_names_missing_data_raises_guard_error():
    """A request/header record with no 'data' key at all must raise
    GuardError (naming the record's seq), not a bare KeyError."""
    rec = {"type": "request/header", "seq": 42}
    jsonl = _build_jsonl(rec)
    with pytest.raises(GuardError) as exc_info:
        header_tool_names(jsonl)
    assert "42" in str(exc_info.value)


def test_header_tool_names_missing_header_raises_guard_error():
    """A request/header record whose 'data' lacks a 'header' key must
    raise GuardError (naming the record's seq), not a bare KeyError."""
    rec = {"type": "request/header", "seq": 43, "data": {}}
    jsonl = _build_jsonl(rec)
    with pytest.raises(GuardError) as exc_info:
        header_tool_names(jsonl)
    assert "43" in str(exc_info.value)


def test_header_tool_names_tools_not_a_list_raises_guard_error():
    """A request/header record whose 'tools' is not a list (e.g. a string,
    or a dict) must raise GuardError (naming the record's seq), not a bare
    TypeError from iterating a non-iterable-of-dicts shape."""
    rec = {
        "type": "request/header",
        "seq": 44,
        "data": {"header": {"tools": "not-a-list"}},
    }
    jsonl = _build_jsonl(rec)
    with pytest.raises(GuardError) as exc_info:
        header_tool_names(jsonl)
    assert "44" in str(exc_info.value)


def test_header_tool_names_missing_data_no_seq_falls_back_to_index():
    """When the offending record has no 'seq' either, the GuardError still
    names something locating the record -- its line index in the input."""
    rec = {"type": "request/header"}  # no seq, no data
    jsonl = _build_jsonl({"type": "session"}, rec)
    with pytest.raises(GuardError) as exc_info:
        header_tool_names(jsonl)
    # line index 1 (0-based) is where the offending record sits
    assert "1" in str(exc_info.value)


def test_header_tool_names_tool_entry_not_a_dict_raises_guard_error():
    """A tools list containing a non-dict entry (e.g. a bare string) must
    raise GuardError naming the record (seq/line-index) and the entry's
    position -- not a bare TypeError from `entry["name"]`."""
    rec = {
        "type": "request/header",
        "seq": 55,
        "data": {"header": {"tools": [{"name": "bash"}, "not-a-dict"]}},
    }
    jsonl = _build_jsonl(rec)
    with pytest.raises(GuardError) as exc_info:
        header_tool_names(jsonl)
    msg = str(exc_info.value)
    assert "55" in msg
    assert "1" in msg  # position 1 (0-based) is the offending entry


def test_header_tool_names_tool_entry_missing_name_raises_guard_error():
    """A tools list entry that IS a dict but lacks 'name' must also raise
    GuardError naming the record and the entry's position -- not a bare
    KeyError from `entry["name"]`."""
    rec = {
        "type": "request/header",
        "seq": 56,
        "data": {"header": {"tools": [{"description": "no name here"}]}},
    }
    jsonl = _build_jsonl(rec)
    with pytest.raises(GuardError) as exc_info:
        header_tool_names(jsonl)
    msg = str(exc_info.value)
    assert "56" in msg
    assert "0" in msg  # position 0 (0-based) is the offending entry


# ── assert_no_tools ──────────────────────────────────────────────────────


def _write_session_jsonl(dsh_home: Path, session_id: str, jsonl_bytes: bytes) -> Path:
    if not ZSTD_ON_PATH:
        pytest.skip("zstd CLI not on PATH")
    session_dir = dsh_home / "sessions" / "workspace-x" / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    plain = session_dir / "plain.jsonl"
    plain.write_bytes(jsonl_bytes)
    compressed = session_dir / "session.v3.jsonl.zstd"
    subprocess.run(
        ["zstd", "-f", "-o", str(compressed), str(plain)],
        check=True,
        capture_output=True,
    )
    plain.unlink()
    return compressed


def test_assert_no_tools_passes_when_clean(tmp_path):
    dsh_home = tmp_path / "dsh-home"
    jsonl = _build_jsonl({"type": "session"}, NO_TOOLS_RECORD)
    _write_session_jsonl(dsh_home, "sess-clean", jsonl)
    report = assert_no_tools(dsh_home, "sess-clean")
    assert report.header_count == 1
    assert report.tool_names_per_header == [[]]


def test_assert_no_tools_raises_violation_with_sorted_union(tmp_path):
    dsh_home = tmp_path / "dsh-home"
    jsonl = _build_jsonl(NO_TOOLS_RECORD, WITH_TOOLS_RECORD)
    _write_session_jsonl(dsh_home, "sess-dirty", jsonl)
    with pytest.raises(NoToolsViolation) as exc_info:
        assert_no_tools(dsh_home, "sess-dirty")
    exc = exc_info.value
    assert "bash" in exc.tool_names
    assert "read" in exc.tool_names
    assert "write" in exc.tool_names
    assert "web_search" in exc.tool_names
    assert exc.tool_names == sorted(exc.tool_names)
    assert "bash" in str(exc)


def test_assert_no_tools_is_a_guard_error_subclass():
    assert issubclass(NoToolsViolation, GuardError)
