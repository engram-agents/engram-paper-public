#!/usr/bin/env python3
"""Fresh-reader run driver for engram-paper#55 -- Claude Code backend.

Sibling of `fresh_reader_run.py` (the DeepSeek Harness SDK driver). Keeps
the instrument constant -- same render, same turn split, same
persona-on-turn-0, same per-section and end-of-paper instructions, same
figures-as-image-blocks, same log and manifest shape -- and swaps only the
backend: one `claude -p` process per turn, chained by `--session-id` /
`--resume`, instead of one continuing DeepSeek Harness SDK session.

Why a separate process per turn rather than one continuing session:
Claude Code's headless mode (`claude -p`) has no in-process multi-turn API
comparable to `harness.run()` against one `DeepSeekHarness` instance --
continuation is via the CLI's own `--resume <session-id>` flag, chaining a
fresh process per turn onto the same transcript. This is a genuinely
different backend shape from the dsh driver's, not a smaller version of it.

Flags verified live on this seat 2026-09-24 (Claude Code 2.1.281,
`claude-opus-5-5`, subscription login -- init reported `"tools":[]`,
`"mcp_servers":[]`, `"apiKeySource":"none"`; a second turn via `--resume`
recalled the first; a base64 image block through stream-json input was
read correctly). See the module-level constants and `build_argv` below for
the exact flag list.

## What this script deliberately does NOT do

- Does not run without `--live`. Default mode is dry-run: build the turn
  sequence, print the plan (including the exact argv for turn 0 and turn 1,
  with the session id shown as `<uuid>`), create the empty jail dir, and
  stop -- exactly like the dsh driver's own dry-run boundary.
- Never sends `ANTHROPIC_API_KEY` to the subprocess even if it is set in
  the calling environment -- the run must go through the subscription
  login, not a key (Lei's decision, per the spec).
- Never writes anything into the jail dir (`<out-dir>/run/jail/`) other
  than what the `claude` subprocess itself might write as a side effect of
  running there with `--restricted --safe-mode --tools ""` -- the runner
  itself only asserts the dir starts empty and passes it as `cwd=`.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType
from typing import Optional

SYSTEM_PROMPT = "You are a careful reader."

# Leak strings for check_transcript -- deliberately NOT "engram"/"ENGRAM":
# the paper is about ENGRAM, so that word is expected to appear throughout
# a genuine reading and must not itself be treated as contamination (spec
# §4). These are identity-layer strings specific to the operator's own
# ENGRAM seat that must never leak into a vanilla fresh-reader session.
#
# CORRECTED per spec §9 ADDENDUM (2026-09-24, after the first live smoke):
# the original list included "Somnium" and "warm-briefing", both of which
# the PAPER ITSELF legitimately contains (the title page credits "Kepler
# Somnium" as an author; a chapter describes the warm-briefing letter
# mechanism) -- a leak string the paper itself carries is not a leak
# string, and the first live smoke aborted at turn 0 on exactly this false
# positive. "MEMORY.md" and "agent-kepler/.claude" are dropped too.
#
# CORRECTED AGAIN per spec §10 ADDENDUM 2 (2026-09-24, after the second
# live smoke): "agent-kepler" is ALSO dropped -- it is path-shaped, and
# every path field in the transcript carries it (e.g. the scratchpad path
# itself contains "-home-agent-kepler-"), which aborted the second live
# smoke on the environment-snapshot attachment. Path-bearing fields are
# handled by `_strip_forgiven_fields` (which is what needed fixing, not
# this list) -- LEAK_STRINGS itself should carry only content/identity
# markers, never path fragments. Eight markers remain.
LEAK_STRINGS = (
    "warm-briefing.md",
    "pn_0002",
    "Model Identity Gate",
    "ENGRAM Write Discipline",
    "self_lineage",
    "ask-Lei.md",
    "cs_0015",
    "lei-timezone-nyc",
)

TURN_TIMEOUT_SECONDS = 1800


def _load_reader_run() -> ModuleType:
    """Loads the sibling `fresh_reader_run.py` module by its own file path
    rather than as a package -- the same pattern as that module's own
    `_load_guard()` (see its docstring): a package-style
    `from tools.fresh_reader.fresh_reader_run import ...` only resolves
    when the repo root happens to be on `sys.path`, which is not true under
    this script's own direct-invocation shapes. This loader depends only on
    `__file__`, so it resolves identically regardless of cwd or invocation
    method."""
    run_path = Path(__file__).parent / "fresh_reader_run.py"
    spec = importlib.util.spec_from_file_location("fresh_reader_run", run_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load fresh_reader_run module spec from {run_path}")
    module = importlib.util.module_from_spec(spec)
    # Register under its own name BEFORE exec -- fresh_reader_run.py defines
    # @dataclass classes under `from __future__ import annotations`, and
    # dataclasses' own forward-ref resolution looks the defining module up
    # via sys.modules[cls.__module__] while the class body is being
    # processed. See fresh_reader_run._load_guard's own docstring for the
    # AttributeError this avoids.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_reader_run = _load_reader_run()

# Reused, unchanged, per spec §1 -- the rubric text constants therefore
# come from fresh_reader_run.py; nothing here restates them.
render_fresh = _reader_run.render_fresh
capture_paper_sha = _reader_run.capture_paper_sha
split_into_turns = _reader_run.split_into_turns
build_turns = _reader_run.build_turns
turn_content_blocks = _reader_run.turn_content_blocks
_preflight_turn_figures = _reader_run._preflight_turn_figures
Turn = _reader_run.Turn
RunManifestEntry = _reader_run.RunManifestEntry
PER_SECTION_LOG_INSTRUCTION = _reader_run.PER_SECTION_LOG_INSTRUCTION
END_OF_PAPER_INSTRUCTION = _reader_run.END_OF_PAPER_INSTRUCTION


# ── Pure helpers (tested directly, no subprocess) ────────────────────────


def to_claude_blocks(blocks: list[dict]) -> list[dict]:
    """Converts `turn_content_blocks`'s harness-shaped content blocks into
    the Claude Code stream-json input shape (spec §2). A text block passes
    through unchanged; an image block
    `{"type": "image", "data": <b64>, "mimeType": <mt>}` becomes
    `{"type": "image", "source": {"type": "base64", "media_type": <mt>,
    "data": <b64>}}`. Order is preserved; any other block type (none exist
    today) passes through unchanged rather than being silently dropped."""
    converted: list[dict] = []
    for block in blocks:
        if block.get("type") == "image":
            converted.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": block["mimeType"],
                        "data": block["data"],
                    },
                }
            )
        else:
            converted.append(block)
    return converted


def build_argv(
    claude_bin: str, model: str, session_id: str, is_first_turn: bool
) -> list[str]:
    """Builds the `claude -p` argv for one turn (spec §2). Turn 0 carries
    `--session-id <session_id>`; every later turn carries
    `--resume <session_id>`; never both on one call. `--tools` is followed
    by an argv element that is the empty string -- built as a list, so this
    is genuinely an empty-string element, not an omitted flag."""
    argv = [
        claude_bin,
        "-p",
        "--model",
        model,
        "--tools",
        "",
        "--strict-mcp-config",
        "--restricted",
        "--safe-mode",
        "--system-prompt",
        SYSTEM_PROMPT,
        "--input-format",
        "stream-json",
        "--output-format",
        "stream-json",
        "--verbose",
    ]
    if is_first_turn:
        argv += ["--session-id", session_id]
    else:
        argv += ["--resume", session_id]
    return argv


def build_env(base_env: dict) -> dict:
    """Pure: returns a COPY of `base_env` with `ANTHROPIC_API_KEY` removed
    if present (spec §2 -- the run must go through the subscription login,
    not a key). Never mutates the input dict. Whether the key was present
    (and thus whether to print the removal notice) is the caller's concern,
    not this function's -- kept pure and side-effect-free for testability."""
    env = dict(base_env)
    env.pop("ANTHROPIC_API_KEY", None)
    return env


# ── Guards (the contract, tested first per spec §3/§4) ───────────────────


class JailViolation(RuntimeError):
    """The jailed, tool-less invariant this run depends on was not upheld
    (or could not be verified) -- raised by `check_turn_output`,
    `check_transcript`, and `find_transcript`. Always a refusal, never a
    silent pass."""


@dataclass
class TurnReport:
    session_id: str
    claude_code_version: str
    response_text: str


def check_turn_output(
    lines: list[dict],
    expected_model: str,
    returncode: Optional[int] = None,
    stderr: Optional[str] = None,
) -> TurnReport:
    """Spec §3 (+ §9 ADDENDUM). Raises JailViolation when: no init record,
    or init["tools"] != [], or init["mcp_servers"] != [], or
    init["model"] != expected_model; no result record, or
    result["is_error"] is truthy, or result["result"] is not a non-empty
    string. Returns the init's session_id, claude_code_version, and the
    response text on success. Called by the runner on EVERY turn (not only
    turn 0) -- with Claude Code each turn is a fresh process, so the tool
    list is per-process configuration, not per-session.

    `returncode`/`stderr` are OPTIONAL (both default None, so every
    pre-addendum caller/test still works unchanged) -- the live runner
    passes the subprocess's own `returncode` and `stderr` so a failure
    message carries them (spec §9): without this, a non-JSON stdout (e.g.
    the process crashed before writing anything) surfaces only as the
    unhelpful "no init record found", discarding the actual reason on
    stderr. When given, every raised message below is suffixed with the
    returncode and the first 500 chars of stderr."""

    def _violation(message: str) -> JailViolation:
        if returncode is not None or stderr:
            stderr_snippet = (stderr or "")[:500]
            message = (
                f"{message} (subprocess returncode={returncode!r}, "
                f"stderr[:500]={stderr_snippet!r})"
            )
        return JailViolation(message)

    init = next(
        (
            line
            for line in lines
            if line.get("type") == "system" and line.get("subtype") == "init"
        ),
        None,
    )
    if init is None:
        raise _violation("no init record (type=system, subtype=init) found in turn output")
    if init.get("tools") != []:
        raise _violation(f"init record carries non-empty tools: {init.get('tools')!r}")
    if init.get("mcp_servers") != []:
        raise _violation(
            f"init record carries non-empty mcp_servers: {init.get('mcp_servers')!r}"
        )
    if init.get("model") != expected_model:
        raise _violation(
            f"init record model {init.get('model')!r} != expected {expected_model!r}"
        )

    result = next((line for line in lines if line.get("type") == "result"), None)
    if result is None:
        raise _violation("no result record (type=result) found in turn output")
    if result.get("is_error"):
        raise _violation(f"result record reports is_error: {result.get('is_error')!r}")
    response_text = result.get("result")
    if not isinstance(response_text, str) or not response_text:
        raise _violation(
            f"result record's 'result' field is not a non-empty string: {response_text!r}"
        )

    return TurnReport(
        session_id=init.get("session_id", ""),
        claude_code_version=init.get("claude_code_version", ""),
        response_text=response_text,
    )


@dataclass
class TranscriptReport:
    assistant_messages: int
    tool_use_blocks: int
    prompt_snapshots_with_empty_tools: int = 0


def _strip_forgiven_fields(line: dict) -> dict:
    """Drops the top-level `cwd` field and the environment-snapshot
    attachment's path-bearing sub-fields before the leak-string scan (spec
    §4, nesting CORRECTED per spec §10 ADDENDUM 2) -- these legitimately
    carry the operator's own filesystem paths and must not themselves
    count as a leak.

    The REAL transcript shape (measured on the second live smoke, addendum
    2) is `{"type":"attachment","attachment":{"type":"environment",
    "snapshot":{"workingDirectory": ..., "additionalWorkingDirectories":
    [...], ...}}}` -- the path sits at `attachment.snapshot.
    workingDirectory`, NOT `attachment.workingDirectory` (the flat shape
    used in the first-cut implementation does not exist in real
    transcripts, so a leak string landing at that flat, non-existent path
    is never legitimately forgiven -- see the matching test). Both
    `attachment.snapshot.workingDirectory` and
    `attachment.snapshot.additionalWorkingDirectories` are dropped; no
    other field under `snapshot` (or elsewhere in the record) is forgiven."""
    stripped = dict(line)
    stripped.pop("cwd", None)
    attachment = stripped.get("attachment")
    if stripped.get("type") == "attachment" and isinstance(attachment, dict):
        if attachment.get("type") == "environment":
            attachment = dict(attachment)
            snapshot = attachment.get("snapshot")
            if isinstance(snapshot, dict):
                snapshot = dict(snapshot)
                snapshot.pop("workingDirectory", None)
                snapshot.pop("additionalWorkingDirectories", None)
                attachment["snapshot"] = snapshot
            stripped["attachment"] = attachment
    return stripped


def check_transcript(path: Path) -> TranscriptReport:
    """Spec §4 (+ §10 ADDENDUM 2). Raises JailViolation when: any
    type=='assistant' line has a message.content block whose type is
    'tool_use'; any type=='user' line has a message.content block (when
    content is a list) whose type is 'tool_result'; a type=='attachment'
    line whose attachment.type=='prompt_snapshot' carries a non-empty
    'tools' list (a stronger witness than the init line -- the tool list
    as actually sent to the API); after stripping the forgiven fields (see
    `_strip_forgiven_fields`), the JSON text of any line contains one of
    the LEAK_STRINGS. Checks block TYPES, never a raw substring grep for
    'tool_use' (the 'server_tool_use' usage counter must not misfire this).
    Returns assistant_messages (count), tool_use_blocks (0 on success --
    a run that reaches the return has, by construction, found none), and
    prompt_snapshots_with_empty_tools (count of prompt_snapshot
    attachments whose 'tools' was explicitly `[]`; a prompt_snapshot with
    'tools' null/absent counts as neither a violation nor a member of this
    count -- the first snapshot of a turn carries no 'tools' key)."""
    assistant_messages = 0
    prompt_snapshots_with_empty_tools = 0

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        line = json.loads(raw_line)
        line_type = line.get("type")

        if line_type == "assistant":
            assistant_messages += 1
            content = line.get("message", {}).get("content")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        raise JailViolation(
                            f"assistant message contains a tool_use block: {block!r}"
                        )
        elif line_type == "user":
            content = line.get("message", {}).get("content")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        raise JailViolation(
                            f"user message contains a tool_result block: {block!r}"
                        )
        elif line_type == "attachment":
            attachment = line.get("attachment")
            if isinstance(attachment, dict) and attachment.get("type") == "prompt_snapshot":
                if "tools" in attachment:
                    tools = attachment["tools"]
                    if tools:
                        # present and truthy -- a non-empty list (or any
                        # other truthy shape) is treated as a violation,
                        # never silently ignored just because it isn't a
                        # list in this particular record.
                        raise JailViolation(
                            f"prompt_snapshot attachment carries non-empty tools: {tools!r}"
                        )
                    elif isinstance(tools, list):
                        # explicitly present and an empty list
                        prompt_snapshots_with_empty_tools += 1
                    # else: tools is None (falsy, not a list) -- not a
                    # violation, not counted.

        checked = _strip_forgiven_fields(line)
        checked_text = json.dumps(checked)
        for leak in LEAK_STRINGS:
            if leak in checked_text:
                raise JailViolation(
                    f"leak string {leak!r} found in transcript line: {checked_text[:300]}"
                )

    return TranscriptReport(
        assistant_messages=assistant_messages,
        tool_use_blocks=0,
        prompt_snapshots_with_empty_tools=prompt_snapshots_with_empty_tools,
    )


def find_transcript(session_id: str) -> Path:
    """Spec §4. Claude Code writes the session transcript at
    `$HOME/.claude/projects/<mangled cwd>/<session_id>.jsonl`. Does not
    reimplement the mangling: locates the file with a glob over
    `$HOME/.claude/projects/*/<session_id>.jsonl` and raises JailViolation
    if the match count is not exactly 1. Reads `HOME` from the environment
    at call time (not cached at import time), so tests can monkeypatch it."""
    home = Path(os.environ["HOME"])
    pattern = f".claude/projects/*/{session_id}.jsonl"
    matches = sorted(home.glob(pattern))
    if len(matches) != 1:
        raise JailViolation(
            f"expected exactly 1 session transcript for session_id {session_id!r} "
            f"under {home / '.claude' / 'projects'}, found {len(matches)}: {matches!r}"
        )
    return matches[0]


def assert_leak_strings_absent(persona_text: str, rendered_text: str) -> None:
    """Spec §9 ADDENDUM start-of-run self-check. Raises JailViolation naming
    the FIRST leak string (in LEAK_STRINGS order) found in either
    `persona_text` or `rendered_text`. Pure -- no I/O of its own, so it can
    be called both against the real files (run_live/main) and against
    fixtures in tests.

    This exists because the leak-string list itself can be wrong -- the
    incident this guards against was LEAK_STRINGS containing a string the
    PAPER ITSELF legitimately carries ("Somnium", from the title page's
    author credit), which aborted the first live smoke at turn 0. Checking
    the persona and the render BEFORE any process launches turns "is this
    leak list even compatible with the material we're about to send" into
    a checked fact at the start of every run, not just a corrected list we
    hope stays correct."""
    for leak in LEAK_STRINGS:
        if leak in persona_text:
            raise JailViolation(
                f"leak string {leak!r} found in the persona file text -- "
                "LEAK_STRINGS is incompatible with this persona; refusing "
                "to start the run"
            )
        if leak in rendered_text:
            raise JailViolation(
                f"leak string {leak!r} found in the rendered paper text -- "
                "LEAK_STRINGS is incompatible with this paper; refusing to "
                "start the run"
            )


# ── Output-refusal guard (spec §5) ───────────────────────────────────────


def _refuse_if_existing_output(out_md: Path, manifest_path: Path, overwrite: bool) -> None:
    """Refuses to start if either output file already exists non-empty,
    unless `overwrite` -- same behaviour, same error text shape as the dsh
    driver's `run_live()` (fresh_reader_run.py)."""
    for existing in (out_md, manifest_path):
        if existing.exists() and existing.stat().st_size > 0 and not overwrite:
            raise FileExistsError(
                f"{existing} already exists and is non-empty. A prior run's "
                "output would be silently truncated. Move it aside, or pass "
                "--overwrite if you mean to discard it."
            )


# ── Dry run ───────────────────────────────────────────────────────────────


def dry_run_report(
    paper_sha: str,
    model: str,
    turns: list,
    figures_per_turn: list,
    jail_dir: Path,
    claude_bin: str,
) -> str:
    """Prints paper_sha, model, turn count, per-turn label/prompt_chars/
    figures, the exact argv for turn 0 and turn 1 (session id shown as
    `<uuid>`), and the jail dir (spec §6). Launches nothing."""
    lines = [
        "# Fresh-reader run (Claude Code backend): DRY RUN (no process launched)",
        "",
        f"paper_sha: {paper_sha}",
        f"model: {model}",
        f"provider: anthropic-subscription (claude -p)",
        f"system_prompt: {SYSTEM_PROMPT}",
        f"turn_count: {len(turns)}",
        f"jail_dir: {jail_dir}",
        "",
        "## Planned turn sequence",
        "",
    ]
    for i, turn in enumerate(turns):
        lines.append(f"{i}. {turn.label} ({len(turn.text)} chars)")
        names = figures_per_turn[i]
        if names:
            lines.append(f"   figures: {', '.join(names)}")

    lines += ["", "## Example argv (session id shown as <uuid>)", ""]
    if len(turns) >= 1:
        argv0 = build_argv(claude_bin, model, "<uuid>", is_first_turn=True)
        lines.append(f"turn 0: {argv0}")
    if len(turns) >= 2:
        argv1 = build_argv(claude_bin, model, "<uuid>", is_first_turn=False)
        lines.append(f"turn 1: {argv1}")

    return "\n".join(lines)


# ── Live run ──────────────────────────────────────────────────────────────


def run_live(
    paper_repo: Path,
    paper_sha: str,
    model: str,
    claude_bin: str,
    turns: list,
    out_dir: Path,
    out_md: Path,
    manifest_path: Path,
    persona_text: str,
    rendered_text: str,
    overwrite: bool = False,
    turn_limit: Optional[int] = None,
) -> None:
    """Drives the actual run: one `claude -p` process per turn, chained by
    `--session-id`/`--resume`, with the guards from spec §3/§4 enforced on
    every turn (turn output) and after turn 0 + at the end of the run
    (transcript). Persists `out_md`/`manifest_path` incrementally, one
    turn at a time, same durability shape as the dsh driver.

    `turn_limit`, when given, runs only turns 0..turn_limit-1 (live smoke
    only), then still performs the final transcript check, then stops.

    `persona_text`/`rendered_text` feed `assert_leak_strings_absent` (spec
    §9 ADDENDUM), called before the jail dir is created and before any
    process launches -- the class of incident this guards against (a
    LEAK_STRINGS entry the paper/persona itself legitimately contains)
    aborted the first live smoke at turn 0; checking it up front turns
    that into a pre-flight refusal instead of a mid-run abort."""
    assert_leak_strings_absent(persona_text, rendered_text)
    _refuse_if_existing_output(out_md, manifest_path, overwrite)

    figures_root = paper_repo / "paper"
    blocks_per_turn, figures_per_turn = _preflight_turn_figures(turns, figures_root)
    total_figure_count = sum(len(names) for names in figures_per_turn)

    jail_dir = out_dir / "run" / "jail"
    jail_dir.mkdir(parents=True, exist_ok=True)
    assert not any(jail_dir.iterdir()), f"jail dir {jail_dir} is not empty before turn 0"

    out_md.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    session_id = str(uuid.uuid4())
    started_at = datetime.now(timezone.utc).isoformat()

    if "ANTHROPIC_API_KEY" in os.environ:
        print(
            "ANTHROPIC_API_KEY was set in the environment; removed for this "
            "run (subscription login required, not a key).",
            file=sys.stderr,
        )
    env = build_env(dict(os.environ))

    header_lines = [
        "# Fresh-reader run",
        "",
        f"model: {model}",
        "provider: anthropic-subscription (claude -p)",
        f"paper_sha: {paper_sha}",
        f"system_prompt: {SYSTEM_PROMPT}",
        f"figures: attached inline as image blocks ({total_figure_count} found in the render)",
        f"session_id: {session_id}",
        f"started_at: {started_at}",
    ]
    if turn_limit is not None:
        header_lines.append(f"turn_limit: {turn_limit}")
    header_lines += ["", "---", ""]
    out_md.write_text("\n".join(header_lines), encoding="utf-8")
    manifest_path.write_text("", encoding="utf-8")

    turns_to_run = turns if turn_limit is None else turns[:turn_limit]

    for i, turn in enumerate(turns_to_run):
        is_first = i == 0
        entry = RunManifestEntry(
            turn_index=i,
            label=turn.label,
            prompt_chars=len(turn.text),
            started_at=datetime.now(timezone.utc).isoformat(),
            figures_attached=figures_per_turn[i],
        )
        try:
            argv = build_argv(claude_bin, model, session_id, is_first)
            claude_blocks = to_claude_blocks(blocks_per_turn[i])
            stdin_obj = {
                "type": "user",
                "message": {"role": "user", "content": claude_blocks},
            }
            stdin_line = json.dumps(stdin_obj) + "\n"

            proc = subprocess.run(
                argv,
                cwd=jail_dir,
                env=env,
                input=stdin_line,
                capture_output=True,
                text=True,
                timeout=TURN_TIMEOUT_SECONDS,
                check=False,
            )
            # A non-JSON stdout (e.g. the process crashed before writing a
            # stream-json line) must not raise a bare JSONDecodeError here
            # -- fall through to check_turn_output with an empty line list
            # so the failure surfaces as a JailViolation carrying the
            # subprocess's own returncode/stderr (spec §9 ADDENDUM), not an
            # unrelated parse traceback.
            try:
                out_lines = [
                    json.loads(raw) for raw in proc.stdout.splitlines() if raw.strip()
                ]
            except json.JSONDecodeError:
                out_lines = []
            turn_report = check_turn_output(
                out_lines, model, returncode=proc.returncode, stderr=proc.stderr
            )
            entry.response_chars = len(turn_report.response_text)

            with out_md.open("a", encoding="utf-8") as fh:
                fh.write(f"## {turn.label}\n\n{turn_report.response_text}\n\n")

            if is_first:
                transcript_path = find_transcript(turn_report.session_id)
                t_report = check_transcript(transcript_path)
                with out_md.open("a", encoding="utf-8") as fh:
                    fh.write(
                        f"no_tools_check: passed ({t_report.assistant_messages} "
                        "assistant message(s), 0 tool_use, "
                        f"{t_report.prompt_snapshots_with_empty_tools} prompt "
                        "snapshot(s) with empty tool list, 0 leak strings)\n"
                        f"claude_code_version: {turn_report.claude_code_version}\n"
                    )
        except Exception as exc:  # noqa: BLE001 -- record and re-raise
            entry.error = str(exc)
            entry.finished_at = datetime.now(timezone.utc).isoformat()
            with manifest_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry.__dict__) + "\n")
            raise
        entry.finished_at = datetime.now(timezone.utc).isoformat()
        with manifest_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry.__dict__) + "\n")

    # Every turn completed with no exception -- re-check the FULL transcript
    # now, not just after turn 0 (same colleague-pass-fold shape as the dsh
    # driver's _final_no_tools_check). A JailViolation here still means the
    # run aborts non-zero after appending its own manifest entry.
    try:
        transcript_path = find_transcript(session_id)
        final_report = check_transcript(transcript_path)
    except JailViolation as exc:
        entry = RunManifestEntry(
            turn_index=-1,
            label="no_tools_check_final",
            prompt_chars=0,
            error=str(exc),
            finished_at=datetime.now(timezone.utc).isoformat(),
        )
        with manifest_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry.__dict__) + "\n")
        raise

    with out_md.open("a", encoding="utf-8") as fh:
        fh.write(
            f"no_tools_check_final: passed ({final_report.assistant_messages} "
            "assistant message(s), 0 tool_use, "
            f"{final_report.prompt_snapshots_with_empty_tools} prompt "
            "snapshot(s) with empty tool list, 0 leak strings)\n"
        )


# ── CLI ───────────────────────────────────────────────────────────────────


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-repo", type=Path, required=True)
    parser.add_argument("--persona-file", type=Path, required=True)
    parser.add_argument(
        "--model",
        required=True,
        help="Exact Claude Code model id (e.g. claude-opus-5-5). No default.",
    )
    parser.add_argument(
        "--out-dir", type=Path, default=Path("/tmp/fresh-reader-claude-run")
    )
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Actually launch `claude -p` processes. Without this flag, dry-run only.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Allow --live to overwrite a non-empty prior run's output "
            "(out_md / manifest.jsonl)."
        ),
    )
    parser.add_argument(
        "--turn-limit",
        type=int,
        default=None,
        help="Live smoke only: run turns 0..N-1, then the final transcript check, then stop.",
    )
    args = parser.parse_args(argv)

    # A relative --out-dir crashes downstream the same way it would in the
    # dsh driver (render_fresh runs with cwd=paper_repo, then this process
    # reads output paths relative to its own cwd) -- resolve once, up front.
    args.out_dir = args.out_dir.resolve()

    if not args.persona_file.is_file():
        parser.error(f"--persona-file not found: {args.persona_file}")
    persona_text = args.persona_file.read_text(encoding="utf-8")

    paper_sha = capture_paper_sha(args.paper_repo)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    rendered_path = args.out_dir / "rendered-fresh.md"
    rendered = render_fresh(args.paper_repo, rendered_path)
    chapters = split_into_turns(rendered)
    turns = build_turns(persona_text, chapters)

    # Pre-flight ALL turns' figures before any process is launched (same as
    # the dsh driver) -- and before the jail dir's own existence, so a dry
    # run refuses on a missing/invalid figure just like a live run would.
    figures_root = args.paper_repo / "paper"
    _, figures_per_turn = _preflight_turn_figures(turns, figures_root)

    jail_dir = args.out_dir / "run" / "jail"
    jail_dir.mkdir(parents=True, exist_ok=True)

    if not args.live:
        # Spec §9 ADDENDUM: the start-of-run self-check runs on the
        # dry-run path too (run_live carries its own call, for the live
        # path -- see below), so a dry run refuses the same way a live run
        # would, catching a LEAK_STRINGS/paper incompatibility before
        # printing a plan that would only fail once made live.
        assert_leak_strings_absent(persona_text, rendered)
        print(
            dry_run_report(
                paper_sha, args.model, turns, figures_per_turn, jail_dir, args.claude_bin
            )
        )
        return 0

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_md = (
        args.paper_repo / "reviews" / "fresh-reader" / f"fresh-reader-{args.model}-{date_str}.md"
    )
    manifest_path = args.out_dir / "manifest.jsonl"

    run_live(
        paper_repo=args.paper_repo,
        paper_sha=paper_sha,
        model=args.model,
        claude_bin=args.claude_bin,
        turns=turns,
        out_dir=args.out_dir,
        out_md=out_md,
        manifest_path=manifest_path,
        persona_text=persona_text,
        rendered_text=rendered,
        overwrite=args.overwrite,
        turn_limit=args.turn_limit,
    )

    print(f"Wrote {out_md}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
