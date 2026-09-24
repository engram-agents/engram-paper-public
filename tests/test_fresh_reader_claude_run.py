"""Contract tests for `paper.review.tools.fresh_reader_claude_run`, written
BEFORE the implementation per spec-fresh-reader-claude-runner.md §7 —
expected to fail with an ImportError until the module exists.

Uses the `tests/__init__.py` package so
`paper.review.tools.fresh_reader_claude_run` imports as an absolute package
regardless of pytest's invocation directory, matching the existing
`tests/test_fresh_reader_guard.py` / `tests/test_fresh_reader_figures.py`
convention. All tests here are unit tests on fixtures: no subprocess is
actually launched (dry-run tests monkeypatch `subprocess.run` to fail if
called), no network.
"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import pytest

from paper.review.tools.fresh_reader_claude_run import (
    LEAK_STRINGS,
    SYSTEM_PROMPT,
    JailViolation,
    _refuse_if_existing_output,
    assert_leak_strings_absent,
    build_argv,
    build_env,
    check_transcript,
    check_turn_output,
    find_transcript,
    to_claude_blocks,
)
import paper.review.tools.fresh_reader_claude_run as claude_run

PERSONA_FILE = (
    Path(__file__).parent.parent / "paper" / "review" / "fresh-reader-persona.md"
)

# A real 1x1 PNG so the dry-run test exercises real bytes, not a placeholder
# (matches the convention in tests/test_fresh_reader_figures.py).
_PNG_1PX = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgAAIAAAUAAen63NgAAAAASUVORK5CYII="
)


# ── 1. to_claude_blocks ──────────────────────────────────────────────────


def test_to_claude_blocks_text_passes_through_unchanged():
    blocks = [{"type": "text", "text": "hello reader"}]
    assert to_claude_blocks(blocks) == blocks


def test_to_claude_blocks_image_converts_to_source_shape():
    blocks = [{"type": "image", "data": "QUJD", "mimeType": "image/png"}]
    converted = to_claude_blocks(blocks)
    assert converted == [
        {
            "type": "image",
            "source": {"type": "base64", "media_type": "image/png", "data": "QUJD"},
        }
    ]


def test_to_claude_blocks_preserves_document_order():
    blocks = [
        {"type": "text", "text": "before"},
        {"type": "image", "data": "AAAA", "mimeType": "image/png"},
        {"type": "text", "text": "after"},
    ]
    converted = to_claude_blocks(blocks)
    assert [b["type"] for b in converted] == ["text", "image", "text"]
    assert converted[0]["text"] == "before"
    assert converted[2]["text"] == "after"
    assert converted[1]["source"]["media_type"] == "image/png"
    assert converted[1]["source"]["data"] == "AAAA"


# ── 2. argv builder ──────────────────────────────────────────────────────


def test_build_argv_turn0_carries_session_id_and_no_resume():
    argv = build_argv("claude", "claude-opus-5-5", "abc-123", is_first_turn=True)
    assert "--session-id" in argv
    assert argv[argv.index("--session-id") + 1] == "abc-123"
    assert "--resume" not in argv


def test_build_argv_turn1_carries_resume_and_no_session_id():
    argv = build_argv("claude", "claude-opus-5-5", "abc-123", is_first_turn=False)
    assert "--resume" in argv
    assert argv[argv.index("--resume") + 1] == "abc-123"
    assert "--session-id" not in argv


def test_build_argv_never_carries_both_session_id_and_resume():
    for is_first in (True, False):
        argv = build_argv("claude", "claude-opus-5-5", "abc-123", is_first_turn=is_first)
        assert not ("--session-id" in argv and "--resume" in argv)


def test_build_argv_tools_flag_followed_by_empty_string_element():
    argv = build_argv("claude", "claude-opus-5-5", "abc-123", is_first_turn=True)
    assert "--tools" in argv
    idx = argv.index("--tools")
    assert argv[idx + 1] == ""
    assert argv[idx + 1] is not None


def test_build_argv_carries_all_required_flags():
    argv = build_argv("claude", "claude-opus-5-5", "abc-123", is_first_turn=True)
    for flag in ("--strict-mcp-config", "--restricted", "--safe-mode", "--verbose"):
        assert flag in argv
    assert "--input-format" in argv
    assert argv[argv.index("--input-format") + 1] == "stream-json"
    assert "--output-format" in argv
    assert argv[argv.index("--output-format") + 1] == "stream-json"
    assert "--system-prompt" in argv
    assert argv[argv.index("--system-prompt") + 1] == SYSTEM_PROMPT
    assert "--model" in argv
    assert argv[argv.index("--model") + 1] == "claude-opus-5-5"


def test_build_argv_is_a_list_of_strings():
    argv = build_argv("claude", "claude-opus-5-5", "abc-123", is_first_turn=True)
    assert isinstance(argv, list)
    assert all(isinstance(a, str) for a in argv)
    assert argv[0] == "claude"
    assert argv[1] == "-p"


# ── 3. env builder ───────────────────────────────────────────────────────


def test_build_env_removes_anthropic_api_key_when_present():
    base = {"PATH": "/usr/bin", "ANTHROPIC_API_KEY": "sk-should-be-removed"}
    env = build_env(base)
    assert "ANTHROPIC_API_KEY" not in env
    assert env["PATH"] == "/usr/bin"


def test_build_env_is_a_noop_when_key_absent():
    base = {"PATH": "/usr/bin"}
    env = build_env(base)
    assert env == {"PATH": "/usr/bin"}


def test_build_env_does_not_mutate_the_input_dict():
    base = {"ANTHROPIC_API_KEY": "sk-test"}
    build_env(base)
    assert base == {"ANTHROPIC_API_KEY": "sk-test"}


# ── 4. check_turn_output ─────────────────────────────────────────────────


def _init_line(**overrides):
    base = {
        "type": "system",
        "subtype": "init",
        "cwd": "/out-dir/run/jail",
        "session_id": "sess-1",
        "tools": [],
        "mcp_servers": [],
        "model": "claude-opus-5-5",
        "permissionMode": "default",
        "apiKeySource": "none",
        "claude_code_version": "2.1.281",
    }
    base.update(overrides)
    return base


def _result_line(**overrides):
    base = {"type": "result", "is_error": False, "result": "A careful, linear reading."}
    base.update(overrides)
    return base


def test_check_turn_output_refuses_on_nonempty_tools():
    lines = [_init_line(tools=["Bash"]), _result_line()]
    with pytest.raises(JailViolation):
        check_turn_output(lines, "claude-opus-5-5")


def test_check_turn_output_refuses_on_nonempty_mcp_servers():
    lines = [_init_line(mcp_servers=["some-mcp-server"]), _result_line()]
    with pytest.raises(JailViolation):
        check_turn_output(lines, "claude-opus-5-5")


def test_check_turn_output_refuses_on_model_mismatch():
    lines = [_init_line(model="claude-sonnet-5"), _result_line()]
    with pytest.raises(JailViolation):
        check_turn_output(lines, "claude-opus-5-5")


def test_check_turn_output_refuses_on_is_error_true():
    lines = [_init_line(), _result_line(is_error=True)]
    with pytest.raises(JailViolation):
        check_turn_output(lines, "claude-opus-5-5")


def test_check_turn_output_refuses_on_missing_init():
    lines = [_result_line()]
    with pytest.raises(JailViolation):
        check_turn_output(lines, "claude-opus-5-5")


def test_check_turn_output_refuses_on_missing_result():
    lines = [_init_line()]
    with pytest.raises(JailViolation):
        check_turn_output(lines, "claude-opus-5-5")


def test_check_turn_output_refuses_on_empty_result_string():
    lines = [_init_line(), _result_line(result="")]
    with pytest.raises(JailViolation):
        check_turn_output(lines, "claude-opus-5-5")


def test_check_turn_output_refuses_on_non_string_result():
    lines = [_init_line(), _result_line(result=None)]
    with pytest.raises(JailViolation):
        check_turn_output(lines, "claude-opus-5-5")


def test_check_turn_output_passes_on_clean_fixture_and_returns_fields():
    lines = [_init_line(), _result_line(result="A thoughtful, linear reading response.")]
    report = check_turn_output(lines, "claude-opus-5-5")
    assert report.session_id == "sess-1"
    assert report.claude_code_version == "2.1.281"
    assert report.response_text == "A thoughtful, linear reading response."


# ── 5. check_transcript ──────────────────────────────────────────────────


def _write_jsonl(path: Path, lines: list) -> None:
    path.write_text(
        "\n".join(json.dumps(line) for line in lines) + "\n", encoding="utf-8"
    )


def test_check_transcript_refuses_on_assistant_tool_use_block(tmp_path):
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "assistant",
                "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {}}]},
            }
        ],
    )
    with pytest.raises(JailViolation):
        check_transcript(path)


def test_check_transcript_refuses_on_user_tool_result_block(tmp_path):
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "user",
                "message": {"content": [{"type": "tool_result", "content": "output"}]},
            }
        ],
    )
    with pytest.raises(JailViolation):
        check_transcript(path)


def test_check_transcript_passes_when_user_content_is_a_plain_string(tmp_path):
    """content 'when a list' is the qualifier — a plain-string user message
    (the ordinary shape) must not be scanned for a tool_result block type
    at all."""
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {"type": "user", "message": {"content": "plain text turn content"}},
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": "response text"}]},
            },
        ],
    )
    report = check_transcript(path)
    assert report.assistant_messages == 1
    assert report.tool_use_blocks == 0


def test_check_transcript_refuses_on_leak_string_in_assistant_text(tmp_path):
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "text", "text": "This reminds me of pn_0002's prior work."}
                    ]
                },
            }
        ],
    )
    with pytest.raises(JailViolation):
        check_transcript(path)


def test_check_transcript_passes_when_leak_string_only_in_top_level_cwd(tmp_path):
    # "agent-kepler" was dropped from LEAK_STRINGS entirely (addendum 2 --
    # it's path-shaped and every path field carries it). Use a remaining
    # leak string embedded in the path to prove the top-level `cwd`
    # forgiveness is still structurally in effect, independent of which
    # specific string it happens to shield.
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "system",
                "subtype": "init",
                "cwd": "/home/agent-kepler/cs_0015-jail-dir",
                "session_id": "sess-1",
            },
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": "Clean, no leaks here."}]},
            },
        ],
    )
    report = check_transcript(path)
    assert report.assistant_messages == 1
    assert report.tool_use_blocks == 0


def test_check_transcript_passes_when_leak_string_only_in_nested_snapshot_working_directory(
    tmp_path,
):
    """Addendum 2: the REAL transcript nesting is
    attachment.snapshot.workingDirectory, not attachment.workingDirectory --
    a fixture with the flat shape tests nothing that actually runs."""
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "attachment",
                "attachment": {
                    "type": "environment",
                    "snapshot": {
                        "workingDirectory": "/home/agent-kepler/self_lineage-jail-dir",
                        "isWorktree": False,
                        "isGitRepo": False,
                        "additionalWorkingDirectories": [],
                        "platform": "linux",
                        "shell": "bash",
                        "osVersion": "6.6.87.2",
                    },
                },
            },
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": "Clean, no leaks here."}]},
            },
        ],
    )
    report = check_transcript(path)
    assert report.assistant_messages == 1
    assert report.tool_use_blocks == 0


def test_check_transcript_passes_when_leak_string_only_in_snapshot_additional_working_dirs(
    tmp_path,
):
    """attachment.snapshot.additionalWorkingDirectories is the OTHER
    path-bearing field addendum 2 names -- also forgiven."""
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "attachment",
                "attachment": {
                    "type": "environment",
                    "snapshot": {
                        "workingDirectory": "/tmp/clean",
                        "additionalWorkingDirectories": [
                            "/home/agent-kepler/ask-Lei.md-adjacent-dir"
                        ],
                    },
                },
            },
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": "Clean, no leaks here."}]},
            },
        ],
    )
    report = check_transcript(path)
    assert report.assistant_messages == 1
    assert report.tool_use_blocks == 0


def test_check_transcript_refuses_when_leak_string_in_flat_attachment_working_directory(
    tmp_path,
):
    """The FLAT shape (attachment.workingDirectory, no `snapshot` nesting)
    does not exist in real transcripts, so nothing legitimate lands there --
    a leak string there must NOT be forgiven (addendum 2's regression test
    for the wrong-nesting defect that aborted the second live smoke)."""
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "attachment",
                "attachment": {
                    "type": "environment",
                    "workingDirectory": "/home/agent-kepler/cs_0015-jail-dir",
                },
            }
        ],
    )
    with pytest.raises(JailViolation):
        check_transcript(path)


def test_check_transcript_still_refuses_on_leak_in_other_snapshot_field(tmp_path):
    """workingDirectory and additionalWorkingDirectories are the ONLY
    forgiven sub-fields under attachment.snapshot — a leak string in any
    OTHER snapshot field, or elsewhere in the record, still fires."""
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "attachment",
                "attachment": {
                    "type": "environment",
                    "snapshot": {
                        "workingDirectory": "/tmp/clean",
                        "additionalWorkingDirectories": [],
                        "shell": "warm-briefing.md leaked into shell field",
                    },
                },
            }
        ],
    )
    with pytest.raises(JailViolation):
        check_transcript(path)


def test_check_transcript_passes_when_engram_appears_in_assistant_text(tmp_path):
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "text", "text": "ENGRAM is a claim-level knowledge graph."}
                    ]
                },
            }
        ],
    )
    report = check_transcript(path)
    assert report.assistant_messages == 1
    assert report.tool_use_blocks == 0


def test_check_transcript_passes_when_server_tool_use_in_usage_block(tmp_path):
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "assistant",
                "message": {
                    "content": [{"type": "text", "text": "Reading normally."}],
                    "usage": {"server_tool_use": 3, "input_tokens": 100},
                },
            }
        ],
    )
    report = check_transcript(path)
    assert report.assistant_messages == 1
    assert report.tool_use_blocks == 0


def test_check_transcript_passes_when_assistant_text_mentions_tool_use_as_prose(tmp_path):
    """A clean transcript whose assistant TEXT happens to contain the
    substring 'tool_use' in ordinary prose (not a block type) must still
    pass -- this is the discriminating fixture for the can-it-fail mutation
    'greps the raw line for the substring tool_use' (spec §7's can-it-fail
    item for test 5)."""
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "text",
                            "text": "The paper's appendix E describes the tool_use "
                            "field in its request schema.",
                        }
                    ]
                },
            }
        ],
    )
    report = check_transcript(path)
    assert report.assistant_messages == 1
    assert report.tool_use_blocks == 0


def test_check_transcript_counts_assistant_messages_across_multiple_lines(tmp_path):
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "one"}]}},
            {"type": "user", "message": {"content": "a follow-up prompt"}},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "two"}]}},
        ],
    )
    report = check_transcript(path)
    assert report.assistant_messages == 2


def test_check_transcript_blank_lines_are_ignored(tmp_path):
    path = tmp_path / "t.jsonl"
    path.write_text(
        '{"type": "assistant", "message": {"content": [{"type": "text", "text": "x"}]}}'
        "\n\n\n",
        encoding="utf-8",
    )
    report = check_transcript(path)
    assert report.assistant_messages == 1


# ── ADDENDUM 2: prompt_snapshot tools check ──────────────────────────────


def test_check_transcript_refuses_on_prompt_snapshot_nonempty_tools(tmp_path):
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "attachment",
                "attachment": {"type": "prompt_snapshot", "tools": ["Bash"]},
            }
        ],
    )
    with pytest.raises(JailViolation):
        check_transcript(path)


def test_check_transcript_passes_on_prompt_snapshot_empty_tools_and_counts(tmp_path):
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "attachment",
                "attachment": {"type": "prompt_snapshot", "tools": []},
            },
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": "clean"}]},
            },
        ],
    )
    report = check_transcript(path)
    assert report.prompt_snapshots_with_empty_tools == 1


def test_check_transcript_passes_on_prompt_snapshot_null_tools_and_does_not_count(tmp_path):
    """The FIRST prompt_snapshot of a turn carries no 'tools' key at all in
    real transcripts; null is the same not-a-violation shape (spec §10:
    'if tools is null/absent -> not a violation')."""
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "attachment",
                "attachment": {"type": "prompt_snapshot", "tools": None},
            }
        ],
    )
    report = check_transcript(path)
    assert report.prompt_snapshots_with_empty_tools == 0


def test_check_transcript_passes_on_prompt_snapshot_absent_tools_key(tmp_path):
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "attachment",
                "attachment": {"type": "prompt_snapshot"},
            }
        ],
    )
    report = check_transcript(path)
    assert report.prompt_snapshots_with_empty_tools == 0


def test_check_transcript_prompt_snapshots_with_empty_tools_count_is_exact(tmp_path):
    """Two turns' worth of the REAL observed shape: first snapshot per turn
    has no 'tools' key, second carries 'tools': [] -- count must be exactly
    the number of empty-list snapshots, not every prompt_snapshot line."""
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {"type": "attachment", "attachment": {"type": "prompt_snapshot"}},
            {"type": "attachment", "attachment": {"type": "prompt_snapshot", "tools": []}},
            {"type": "attachment", "attachment": {"type": "prompt_snapshot"}},
            {"type": "attachment", "attachment": {"type": "prompt_snapshot", "tools": []}},
        ],
    )
    report = check_transcript(path)
    assert report.prompt_snapshots_with_empty_tools == 2


def test_check_transcript_non_prompt_snapshot_attachment_not_counted(tmp_path):
    """An environment attachment (or any other attachment type) must not
    be mistaken for a prompt_snapshot and counted."""
    path = tmp_path / "t.jsonl"
    _write_jsonl(
        path,
        [
            {
                "type": "attachment",
                "attachment": {
                    "type": "environment",
                    "snapshot": {"workingDirectory": "/tmp/clean"},
                },
            }
        ],
    )
    report = check_transcript(path)
    assert report.prompt_snapshots_with_empty_tools == 0


# ── session-transcript locator ───────────────────────────────────────────


def test_find_transcript_exactly_one_match_returns_it(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    proj_dir = tmp_path / ".claude" / "projects" / "-some-mangled-cwd"
    proj_dir.mkdir(parents=True)
    expected = proj_dir / "sess-1.jsonl"
    expected.write_text("{}\n", encoding="utf-8")
    found = find_transcript("sess-1")
    assert found == expected


def test_find_transcript_zero_matches_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / ".claude" / "projects" / "-some-mangled-cwd").mkdir(parents=True)
    with pytest.raises(JailViolation):
        find_transcript("sess-missing")


def test_find_transcript_two_matches_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    d1 = tmp_path / ".claude" / "projects" / "-cwd-a"
    d2 = tmp_path / ".claude" / "projects" / "-cwd-b"
    d1.mkdir(parents=True)
    d2.mkdir(parents=True)
    (d1 / "sess-dup.jsonl").write_text("{}\n", encoding="utf-8")
    (d2 / "sess-dup.jsonl").write_text("{}\n", encoding="utf-8")
    with pytest.raises(JailViolation):
        find_transcript("sess-dup")


# ── 6. dry run over a tiny fake paper ────────────────────────────────────


def _write_png(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_PNG_1PX)


def test_dry_run_over_tiny_fake_paper_prints_plan_and_launches_nothing(
    tmp_path, monkeypatch, capsys
):
    paper_repo = tmp_path / "paper_repo"
    _write_png(paper_repo / "paper" / "figures" / "fig1.png")

    persona_file = tmp_path / "persona.md"
    persona_file.write_text("You are a careful, linear reader.\n", encoding="utf-8")

    # Two "# " content sections (Abstract, Chapter 1) plus the title line,
    # one figure line pointing at the 1x1 PNG above.
    rendered_text = (
        "# The Tiny Paper\n\n"
        "# Abstract\n\nA short abstract.\n\n"
        "# Chapter 1\n\n"
        "Some prose.\n\n"
        "![Fig 1](figures/fig1.png)\n\n"
        "More prose after the figure.\n"
    )

    monkeypatch.setattr(claude_run, "capture_paper_sha", lambda repo: "deadbeef1234")
    monkeypatch.setattr(
        claude_run, "render_fresh", lambda repo, out_path: rendered_text
    )

    def _fail_if_subprocess_called(*args, **kwargs):
        raise AssertionError("subprocess.run must not be called during a dry run")

    monkeypatch.setattr(claude_run.subprocess, "run", _fail_if_subprocess_called)

    out_dir = tmp_path / "fr-out-dry"
    argv = [
        "--paper-repo",
        str(paper_repo),
        "--persona-file",
        str(persona_file),
        "--model",
        "claude-opus-5-5",
        "--out-dir",
        str(out_dir),
    ]
    exit_code = claude_run.main(argv)
    assert exit_code == 0

    out = capsys.readouterr().out
    assert "deadbeef1234" in out
    assert "claude-opus-5-5" in out
    assert "Abstract" in out
    assert "Chapter 1" in out
    assert "fig1.png" in out
    # turn count is printed somewhere in the plan (Abstract, Chapter 1,
    # end-of-paper -> 3 turns)
    assert "3" in out
    # exact argv shown for turn 0 and turn 1, session id shown as <uuid>
    assert "<uuid>" in out
    assert "--session-id" in out
    assert "--resume" in out

    jail_dir = out_dir / "run" / "jail"
    assert jail_dir.is_dir()
    assert list(jail_dir.iterdir()) == []


# ── 7. existing-output refusal without --overwrite ───────────────────────


def test_refuse_if_existing_output_raises_without_overwrite(tmp_path):
    out_md = tmp_path / "out.md"
    manifest_path = tmp_path / "manifest.jsonl"
    out_md.write_text("prior run content", encoding="utf-8")
    with pytest.raises(FileExistsError):
        _refuse_if_existing_output(out_md, manifest_path, overwrite=False)


def test_refuse_if_existing_output_allows_with_overwrite(tmp_path):
    out_md = tmp_path / "out.md"
    manifest_path = tmp_path / "manifest.jsonl"
    out_md.write_text("prior run content", encoding="utf-8")
    manifest_path.write_text("prior manifest\n", encoding="utf-8")
    _refuse_if_existing_output(out_md, manifest_path, overwrite=True)  # no raise


def test_refuse_if_existing_output_allows_when_both_absent(tmp_path):
    out_md = tmp_path / "out.md"
    manifest_path = tmp_path / "manifest.jsonl"
    _refuse_if_existing_output(out_md, manifest_path, overwrite=False)  # no raise


def test_refuse_if_existing_output_allows_when_present_but_empty(tmp_path):
    out_md = tmp_path / "out.md"
    manifest_path = tmp_path / "manifest.jsonl"
    out_md.write_text("", encoding="utf-8")
    manifest_path.write_text("", encoding="utf-8")
    _refuse_if_existing_output(out_md, manifest_path, overwrite=False)  # no raise


def test_refuse_if_existing_output_checks_manifest_too(tmp_path):
    out_md = tmp_path / "out.md"
    manifest_path = tmp_path / "manifest.jsonl"
    manifest_path.write_text('{"turn_index": 0}\n', encoding="utf-8")
    with pytest.raises(FileExistsError):
        _refuse_if_existing_output(out_md, manifest_path, overwrite=False)


# ── §9 ADDENDUM: assert_leak_strings_absent (start-of-run self-check) ────


def test_assert_leak_strings_absent_refuses_when_leak_in_persona():
    persona_text = "You are a careful reader. Remember pn_0002's own history."
    rendered_text = "# Title\n\nClean paper text."
    with pytest.raises(JailViolation):
        assert_leak_strings_absent(persona_text, rendered_text)


def test_assert_leak_strings_absent_refuses_when_leak_in_render():
    persona_text = "You are a careful reader."
    rendered_text = "# Title\n\nSee ask-Lei.md for the operator's own queue."
    with pytest.raises(JailViolation):
        assert_leak_strings_absent(persona_text, rendered_text)


def test_assert_leak_strings_absent_passes_on_clean_texts():
    persona_text = "You are a careful reader with no special vocabulary."
    rendered_text = "# Title\n\nThe paper discusses ENGRAM, a knowledge graph system."
    assert_leak_strings_absent(persona_text, rendered_text)  # no raise


def test_assert_leak_strings_absent_names_the_first_leak_string_found():
    persona_text = "cs_0015 is mentioned here."
    rendered_text = "clean"
    with pytest.raises(JailViolation) as exc_info:
        assert_leak_strings_absent(persona_text, rendered_text)
    assert "cs_0015" in str(exc_info.value)


def test_assert_leak_strings_absent_checks_every_leak_string_at_least_once():
    """Regression coverage for the corrected LEAK_STRINGS constant itself --
    each string in the live list must actually trip the guard when present
    in either text, not just the one used above."""
    for leak in LEAK_STRINGS:
        with pytest.raises(JailViolation):
            assert_leak_strings_absent(f"persona text with {leak} inside", "clean render")
        with pytest.raises(JailViolation):
            assert_leak_strings_absent("clean persona", f"render text with {leak} inside")


def test_leak_strings_no_longer_carries_agent_kepler():
    """Addendum 2: 'agent-kepler' is dropped -- it is path-shaped, and every
    path field in a real transcript carries it (the scratchpad path itself
    contains '-home-agent-kepler-'), which is exactly what aborted the
    second live smoke. Eight markers remain."""
    assert "agent-kepler" not in LEAK_STRINGS
    assert len(LEAK_STRINGS) == 8


def test_assert_leak_strings_absent_regression_against_real_persona_file():
    """The regression test for the incident (spec §9): the LIVE
    LEAK_STRINGS constant, checked against the REAL
    paper/review/fresh-reader-persona.md file in this repo -- not a
    stand-in fixture. This is exactly what aborted the first live smoke
    (the OLD list matched the paper's own text); the corrected list must
    not."""
    assert PERSONA_FILE.is_file(), f"expected real persona file at {PERSONA_FILE}"
    persona_text = PERSONA_FILE.read_text(encoding="utf-8")
    assert_leak_strings_absent(persona_text, "clean render")  # no raise


# ── §9 ADDENDUM: check_turn_output failure message carries returncode/stderr


def test_check_turn_output_failure_message_includes_returncode_and_stderr():
    lines: list[dict] = []  # no init record at all
    with pytest.raises(JailViolation) as exc_info:
        check_turn_output(lines, "claude-opus-5-5", returncode=1, stderr="boom: traceback here")
    msg = str(exc_info.value)
    assert "1" in msg
    assert "boom: traceback here" in msg


def test_check_turn_output_failure_message_truncates_stderr_to_500_chars():
    lines: list[dict] = []
    long_stderr = "x" * 2000
    with pytest.raises(JailViolation) as exc_info:
        check_turn_output(lines, "claude-opus-5-5", returncode=2, stderr=long_stderr)
    msg = str(exc_info.value)
    assert "x" * 500 in msg
    assert "x" * 501 not in msg


def test_check_turn_output_still_works_without_returncode_or_stderr():
    """Backward-compatible: existing callers that don't pass these kwargs
    still get a clean JailViolation, and the success path is unaffected."""
    lines = [_init_line(), _result_line()]
    report = check_turn_output(lines, "claude-opus-5-5")
    assert report.response_text == "A careful, linear reading."


# ── reuse sanity: names come from fresh_reader_run.py, not restated ──────


def test_reuses_render_fresh_and_friends_from_fresh_reader_run():
    from paper.review.tools import fresh_reader_run as dsh_run

    # Same function objects' behaviour class -- not asserting identity
    # (our module loads fresh_reader_run.py via a SEPARATE file-path import,
    # per spec §1, so it is a different module object in sys.modules than
    # the package-imported one here; that is the documented, intentional
    # shape -- see the ambiguity note in the handoff). Assert instead that
    # our module's bound names are genuinely callables sourced from that
    # file, by checking the rubric text constants are byte-identical.
    assert claude_run.PER_SECTION_LOG_INSTRUCTION == dsh_run.PER_SECTION_LOG_INSTRUCTION
    assert claude_run.END_OF_PAPER_INSTRUCTION == dsh_run.END_OF_PAPER_INSTRUCTION
