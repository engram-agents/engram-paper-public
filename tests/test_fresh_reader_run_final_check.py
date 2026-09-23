"""Contract tests for `paper.review.tools.fresh_reader_run._final_no_tools_check`
-- the end-of-session no-tools re-check added in the colleague-pass fold
round on spec-no-tools-guard.md (after commit 6e81867).

The turn-0 check in run_live() only verifies the FIRST request/header
record. `_final_no_tools_check` is called once after the turn loop
finishes normally and re-decodes the whole session store, so every
request/header of the whole session is checked. Factored out as its own
module-level function specifically so it can be tested directly against a
fake session store built from the fixtures, without spinning up a
harness.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from paper.review.tools.fresh_reader_run import _final_no_tools_check

# Deliberately NOT `from paper.review.tools.fresh_reader_guard import
# GuardError`, and NOT even a single shared `_load_guard().GuardError`
# captured once at module level: `_load_guard()` is not memoized -- every
# call to it (including internally, once per `_final_no_tools_check` call)
# execs a FRESH copy of fresh_reader_guard.py, so each call produces its
# own distinct class objects. A GuardError class object captured from one
# `_load_guard()` call will not match (via isinstance/pytest.raises) an
# exception raised by a *different* `_load_guard()` call -- confirmed by
# hand: capturing GuardError once at collection time and asserting on it
# here did NOT catch the exception `_final_no_tools_check`'s own internal
# `_load_guard()` call raised. `RuntimeError` is the one class in this
# hierarchy that IS shared across every load (a builtin, never
# re-executed), so tests assert against that plus the exception's own
# type name/message instead of a specific GuardError class identity.

FIXTURES = Path(__file__).parent / "fixtures" / "fresh_reader"
WITH_TOOLS_RECORD = json.loads((FIXTURES / "request-header-with-tools.json").read_text())
NO_TOOLS_RECORD = json.loads((FIXTURES / "request-header-no-tools.json").read_text())

ZSTD_ON_PATH = shutil.which("zstd") is not None


def _write_session_jsonl(dsh_home: Path, session_id: str, records: list[dict]) -> Path:
    """Mirrors tests/test_fresh_reader_guard.py's own helper of the same
    shape -- kept local rather than imported cross-file, matching that
    file's own convention of not sharing test fixtures across test
    modules."""
    if not ZSTD_ON_PATH:
        pytest.skip("zstd CLI not on PATH")
    session_dir = dsh_home / "sessions" / "workspace-final" / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    plain = session_dir / "plain.jsonl"
    plain.write_bytes(("\n".join(json.dumps(r) for r in records) + "\n").encode("utf-8"))
    compressed = session_dir / "session.v3.jsonl.zstd"
    subprocess.run(
        ["zstd", "-f", "-o", str(compressed), str(plain)],
        check=True,
        capture_output=True,
    )
    plain.unlink()
    return compressed


def test_final_check_passes_and_appends_to_out_md(tmp_path):
    dsh_home = tmp_path / "dsh-home"
    session_id = "sess-final-clean"
    _write_session_jsonl(dsh_home, session_id, [NO_TOOLS_RECORD])

    out_md = tmp_path / "out.md"
    out_md.write_text("# Fresh-reader run\n\n---\n", encoding="utf-8")
    manifest_path = tmp_path / "manifest.jsonl"
    manifest_path.write_text("", encoding="utf-8")

    _final_no_tools_check(dsh_home, session_id, out_md, manifest_path)

    out_text = out_md.read_text(encoding="utf-8")
    assert "no_tools_check_final: passed (1 request header(s), 0 tools)" in out_text

    # No manifest entry added on success.
    assert manifest_path.read_text(encoding="utf-8") == ""


def test_final_check_violation_appends_manifest_entry_and_raises(tmp_path):
    dsh_home = tmp_path / "dsh-home"
    session_id = "sess-final-dirty"
    _write_session_jsonl(dsh_home, session_id, [NO_TOOLS_RECORD, WITH_TOOLS_RECORD])

    out_md = tmp_path / "out.md"
    original_out_md_text = "# Fresh-reader run\n\n---\n## Chapter 1\n\nsome response\n\n"
    out_md.write_text(original_out_md_text, encoding="utf-8")
    manifest_path = tmp_path / "manifest.jsonl"
    manifest_path.write_text("", encoding="utf-8")

    with pytest.raises(RuntimeError) as exc_info:
        _final_no_tools_check(dsh_home, session_id, out_md, manifest_path)
    assert type(exc_info.value).__name__ == "NoToolsViolation"
    assert "bash" in str(exc_info.value)

    # The reader log is NOT touched/deleted -- untouched from before the call.
    assert out_md.read_text(encoding="utf-8") == original_out_md_text

    manifest_lines = [
        json.loads(line)
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert len(manifest_lines) == 1
    entry = manifest_lines[0]
    assert entry["turn_index"] == -1
    assert entry["label"] == "no_tools_check_final"
    assert entry["error"] is not None
    assert "bash" in entry["error"]
