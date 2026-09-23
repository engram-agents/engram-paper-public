#!/usr/bin/env python3
"""Fresh-reader run driver for engram-paper#55.

Drives a vanilla (no-ENGRAM) DeepSeek Harness agent through a single,
strictly linear read of the rendered paper: one continuing session, one
chapter per turn, no skipping ahead. Reuses the LoCoMo benchmark runs'
general shape (one process/session per run, a durable manifest.jsonl
record) but is otherwise written fresh -- this seat has no read access to
Kepler's own ~/exam-agents/ driver.py, so this does not copy it byte for
byte.

## Why this uses the deepseek-harness-sdk, not the plain `dsh --profile
## headless "task"` CLI

Verified directly against the installed dsh 0.1.1-rc.2 packages (not
assumed from the issue's prose): the stock `dsh-headless` bundle creates
ONE fresh persisted Agent, submits the task as a single ordinary user
message, waits for quiescence, and exits -- its own README states plainly
"One submitted task only -- the runner has no interactive follow-up
surface." There is no `--resume` for the headless app (confirmed: it
refuses with `error: unknown option '--resume'`; that flag only exists for
the `tui` profile in this build). So a sequence of separate `dsh --profile
headless "chapter N"` CLI invocations would NOT share one session -- each
would be a fresh, memory-less agent, which defeats the whole point of a
continuing linear read.

The mechanism that genuinely supports multi-turn continuation is the
`deepseek-harness-sdk` Python package's synchronous `harness.run()` calls
against one `DeepSeekHarness` instance, per its own `RunResult` interface
(`session_id, final_response, finish_reason, events, notifications` --
verified by Kepler reading the installed `deepseek-harness-sdk 0.1.5rc1`
class directly, forum #428 post 10476, correcting this script's own two
earlier wrong guesses at the call shape). Live-smoke-tested end to end by
Kepler (post 10478): a real two-turn run (Abstract + Chapter 1) against
`deepseek-flash` returned substantive per-section reader logs. Not yet
attempted: the full 18-turn run, or figures (see the "does NOT do" list
below).

## What this script deliberately does NOT do

- Does not hardcode the model id. `--model` is REQUIRED with no default.
  RESOLVED (Kepler, forum #428 post 10473, after engram-paper#55's own
  open checklist item asked for exactly this): the real id is
  `deepseek-flash`. It is not in every installed dsh catalog's
  DEFAULT_MODELS -- see `write_model_catalog_patch`'s docstring for the
  override this script writes to declare it where needed.
- Does not run without `--live` AND a populated `DEEPSEEK_API_KEY`. Default
  mode is dry-run: build the turn sequence, print it, validate config, and
  stop. This is the "do not run the review itself" boundary enforced in
  code, not just in the operator's head.
- Does not pick a persona/rubric. `--persona-file` is REQUIRED (Kepler owns
  that file per the issue; this script only consumes it).
"""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType
from typing import Optional

SECTION_HEADING_RE = re.compile(r"^# (.+?)\s*$", re.MULTILINE)
DEEPSEEK_API_KEY_ENV = "DEEPSEEK_API_KEY"

# One markdown image reference alone on its own line (engram-paper#55,
# figures fold-in): `![alt](path)` with only trailing whitespace after the
# closing paren, matched per-line via re.M so `$` anchors at each line end
# rather than only the end of the whole rendered text.
IMAGE_REF = re.compile(r'^!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)\s*$', re.M)


def _load_guard() -> ModuleType:
    """Loads the sibling `fresh_reader_guard.py` module by its own file
    path rather than as a package (`from paper.review.tools.fresh_reader_guard
    import ...`) -- the package-style import only resolves when the repo
    root happens to be on `sys.path` (e.g. under pytest, invoked from the
    repo root), and raises `ModuleNotFoundError: No module named 'paper'`
    under the script's actual invocation shapes: `python3
    paper/review/tools/fresh_reader_run.py` from another cwd, or an import
    by file path with the tools directory on `sys.path` and the repo root
    NOT on it. Measured live (coordinator report, 2026-09-23): the
    package-style import failed exactly this way at the guard-import line
    inside run_live(). This loader depends only on `__file__`, so it
    resolves identically regardless of cwd, invocation method, or whether
    `paper` is importable as a package at all."""
    guard_path = Path(__file__).parent / "fresh_reader_guard.py"
    spec = importlib.util.spec_from_file_location("fresh_reader_guard", guard_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load guard module spec from {guard_path}")
    module = importlib.util.module_from_spec(spec)
    # Register under its own name BEFORE exec: fresh_reader_guard.py
    # defines @dataclass classes under `from __future__ import
    # annotations`, and dataclasses' own forward-ref resolution looks the
    # defining module up via `sys.modules[cls.__module__]` while the class
    # body is being processed -- omitting this line raises
    # `AttributeError: 'NoneType' object has no attribute '__dict__'` from
    # inside dataclasses.py the moment NoToolsReport's @dataclass
    # decorator runs, a second invocation-shape defect caught only by the
    # coordinator-requested invocation-shape test actually calling
    # _load_guard() end to end (an earlier version of this function passed
    # a shallower manual check that never got far enough to hit it).
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@dataclass
class Turn:
    """One unit of content delivered to the reader in one session turn."""

    label: str
    text: str


def turn_content_blocks(text: str, figures_root: Path) -> list[dict]:
    """Splits a turn's text on every standalone `![alt](path)` markdown
    image line (IMAGE_REF) into an ordered list of harness.run() content
    blocks: `{"type": "text", "text": ...}` and `{"type": "image",
    "data": <base64>, "mimeType": "image/png"}` alternating in document
    order (engram-paper#55 figures fold-in -- the reader has no file tools,
    so a figure reaches it only as image content inside the turn message).

    Each image line is removed from its surrounding text and replaced
    in-place by a `[Figure: <alt> — attached as an image below]` marker,
    so the reader still knows a figure was there and what it was captioned,
    without the raw markdown syntax (which the reader cannot resolve --
    there is no file tool to open the referenced path).

    No text is dropped and no paragraphs are merged: everything before the
    first image line, between consecutive image lines, and after the last
    one is preserved verbatim (aside from the one substitution described
    above) in its own text block. A block reduces to nothing only when its
    span from the text is itself empty (e.g. no trailing text follows the
    final image line) -- never emitted as an empty text block.

    `figures_root` is the directory the markdown path is relative to (the
    caller passes `<paper_repo>/paper`, since the rendered paper's own
    `![Figure N](figures/<name>.png)` lines are relative to that
    directory). A referenced file that does not exist raises
    FileNotFoundError naming the path -- never skipped silently, never
    sent through as the bare markdown line. Only `.png` is supported in
    this PR; any other extension raises ValueError naming it.
    """
    matches = list(IMAGE_REF.finditer(text))
    if not matches:
        return [{"type": "text", "text": text}]

    blocks: list[dict] = []
    pos = 0
    for m in matches:
        before = text[pos : m.start()]
        alt = m.group("alt")
        rel_path = m.group("path")
        marker = f"[Figure: {alt} — attached as an image below]"
        blocks.append({"type": "text", "text": before + marker})

        image_path = figures_root / rel_path
        if image_path.suffix.lower() != ".png":
            raise ValueError(
                f"unsupported figure extension (only .png is supported in "
                f"this PR): {rel_path}"
            )
        if not image_path.is_file():
            raise FileNotFoundError(f"figure file not found: {image_path}")
        data = base64.b64encode(image_path.read_bytes()).decode("ascii")
        blocks.append({"type": "image", "data": data, "mimeType": "image/png"})

        pos = m.end()

    trailing = text[pos:]
    if trailing:
        blocks.append({"type": "text", "text": trailing})
    return blocks


@dataclass
class RunManifestEntry:
    """No input_tokens/output_tokens field: Kepler's live smoke test
    (forum #428 post 10477, 2026-09-23) read the actual RunResult class
    on deepseek-harness-sdk 0.1.5rc1 -- it has exactly session_id,
    final_response, finish_reason, events, notifications, no token-count
    attributes. An earlier version carried getattr(result,
    "input_tokens", None)-style fallbacks that could never fire, which
    would have shipped a manifest column that always reads null and
    looks like a bug in the run rather than the schema. Token usage, if
    ever needed, would have to be parsed out of `events` -- unverified
    what that structure carries, not attempted here rather than guessed."""

    turn_index: int
    label: str
    prompt_chars: int
    response_chars: Optional[int] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    error: Optional[str] = None
    figures_attached: list[str] = field(default_factory=list)


@dataclass
class RunContext:
    paper_repo: Path
    paper_sha: str
    dsh_version: str
    model: str
    provider: str
    persona_text: str
    turns: list[Turn] = field(default_factory=list)
    manifest: list[RunManifestEntry] = field(default_factory=list)


def _run(cmd: list[str], cwd: Optional[Path] = None) -> str:
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(cmd)}\n"
            f"stderr: {result.stderr.strip()}"
        )
    return result.stdout.strip()


def capture_paper_sha(paper_repo: Path) -> str:
    """The exact commit this run reads -- printed into the manifest and
    the output header per Kepler's 2026-09-23 addition (forum #428,
    post 10466): the paper text is still moving, so a run must log which
    head it actually saw, not assume a pinned copy stays current.

    Compares the resolved commit SHA against origin/main's SHA, not the
    checked-out branch NAME (Kepler's nit, forum #428 post 10477): a
    detached-HEAD worktree checked out at main's exact commit reads
    branch 'HEAD', not 'main', and the earlier name-based check would
    warn on it even though it's reading the correct commit."""
    sha = _run(["git", "rev-parse", "HEAD"], cwd=paper_repo)
    try:
        origin_main_sha = _run(["git", "rev-parse", "origin/main"], cwd=paper_repo)
    except RuntimeError:
        origin_main_sha = None  # no origin/main ref fetched into this checkout
    if origin_main_sha is not None and sha != origin_main_sha:
        print(
            f"WARNING: paper repo's HEAD ({sha[:8]}) is not origin/main's "
            f"tip ({origin_main_sha[:8]}). Kepler's instruction was to run "
            "against whatever head is on main -- fetch + checkout "
            "origin/main before a real run. Proceeding with the current "
            "checkout as-is.",
            file=sys.stderr,
        )
    return sha


def render_fresh(paper_repo: Path, out_path: Path) -> str:
    """Regenerate the rendered paper from chapter sources at the CURRENT
    checkout, rather than trusting the committed
    paper/engram-paper-v0.5.1.md -- per this repo's own convention
    (paper_research/current_draft/ is the edit surface; the top-level .md
    is generated by tools/render_paper.py), a committed render can be one
    commit behind its own sources if a PR forgot to re-render."""
    _run(
        [sys.executable, "tools/render_paper.py", "--out", str(out_path)],
        cwd=paper_repo,
    )
    return out_path.read_text(encoding="utf-8")


def split_into_turns(rendered: str) -> list[Turn]:
    """Splits on EVERY level-1 (`^# `) heading, not just ones matching a
    hardcoded 'Chapter N' shape. The first attempt matched only
    '# Chapter N ...' / '# Abstract' and silently swallowed everything
    after the last matched heading into that final turn -- caught by
    actually running this against the real rendered paper (dry-run smoke
    test), where 'Chapter 8' turned out to carry 98842 chars because five
    Appendices, a Bibliography, and 'Part A/B' (Chapter 7's own two
    level-1 sub-splits) all followed it with no further 'Chapter N' match
    to stop at. A hardcoded heading-text pattern is exactly the kind of
    guess that silently drifts as the paper's structure evolves (a new
    Appendix, a renamed Part) -- splitting on the heading LEVEL instead
    needs no such list.

    The title (the very first `# ...` line) plus everything through the
    end of Abstract becomes turn 0's preamble, folded into the first real
    section rather than sent alone -- there is no per-section log to ask
    for on a title page."""
    matches = list(SECTION_HEADING_RE.finditer(rendered))
    if len(matches) < 2:
        raise ValueError(
            f"expected at least a title heading plus one section heading "
            f"in the rendered paper; found {len(matches)} level-1 ('# ') "
            "headings. The render may be malformed or empty."
        )
    # matches[0] is the title; real content sections start at matches[1].
    preamble = rendered[: matches[1].start()]
    section_starts = matches[1:]
    turns: list[Turn] = []
    for i, start_match in enumerate(section_starts):
        end = (
            section_starts[i + 1].start()
            if i + 1 < len(section_starts)
            else len(rendered)
        )
        body = rendered[start_match.start() : end]
        label = start_match.group(1).strip()
        if i == 0:
            body = preamble + body
        turns.append(Turn(label=label, text=body))
    return turns


# Verbatim from paper/review/fresh-reader-rubric.md (engram-paper#77,
# Lei-approved 2026-09-20, finalized 2026-09-23), not this script's own
# wording -- an earlier version of both instructions below drifted from
# the rubric on items 4-6 (per-section) and the end-of-paper Clarity-
# score name: item 5 asked whether questions were answered WITHIN the
# same section (the rubric tracks them ACROSS sections, resolved-later
# noted in the later section's own log); item 6 asked the reader to
# PREDICT the next section's content (the rubric asks whether THIS
# section's own ending justified the transition); the end block said
# "Presentation score" (the rubric's own source-check found NeurIPS 2025
# calls the same field Clarity, Presentation was the 2023-2024 name).
# Caught by #77's own reviewer-fairy comparing this file against the
# rubric it's meant to implement -- a content-correctness defect no
# amount of code-mechanics testing (this PR's round-2 fairy round, which
# APPROVEd before this was raised) could have caught. Keep these two
# constants byte-faithful to the rubric file; if the rubric changes,
# update here to match, not the other way around.
PER_SECTION_LOG_INSTRUCTION = """
---
Read the section above once, linearly. Before you see the next section,
write your per-section log for THIS section:
1. Retell -- two sentences, your own words: what this section claimed and
   why it is here. If you cannot, write "could not retell" and say where
   you lost the thread.
2. Undefined at first use -- every term, acronym, or made-up name or ID
   you met without a definition you could point to earlier in the text,
   unless it is standard in the field. Quote the sentence.
3. Read twice -- sentences or paragraphs you had to re-read to parse.
   Quote them.
4. Already said -- anything you recognised as a restatement of an
   earlier passage. Cite both locations. Say whether the repeat helped
   or cost you.
5. Open questions -- what you expected the paper to answer here and it
   did not. When a LATER section answers one, say so THERE ("answers
   the earlier open question about X"), not here.
6. Hand-off -- did the end of this section tell you why the next one
   comes next? Yes / no / partly.
Do not summarize the whole paper yet -- only this section.
"""

END_OF_PAPER_INSTRUCTION = """
---
You have now read the entire paper. Write the end-of-paper block:
- Whole-paper retell, one paragraph. This is the headline signal: what
  an average reader in the domain takes away.
- Ordering: would you move any chapter? Which, where, and what it would
  fix.
- Clarity score 1-4 on the NeurIPS scale (4 excellent, 3 good, 2 fair,
  1 poor), with one sentence of justification.
- Top five edits that would most improve the read, ranked.
- What you still do not understand about the system after reading
  everything.
Correctness of numbers, novelty, related-work coverage, and whether the
claims are true are explicitly out of scope for this pass -- it measures
only the read.
"""


def build_turns(persona_text: str, chapters: list[Turn]) -> list[Turn]:
    """Wraps each chapter with the per-section-log instruction, and adds
    a final end-of-paper turn. `persona_text` rides on turn 0 only -- the
    session is continuing, so the harness's own conversation history
    carries the persona forward; re-sending it every turn would just
    waste tokens and risk the reader treating it as new content to
    retell."""
    turns: list[Turn] = []
    for i, chapter in enumerate(chapters):
        text = chapter.text + PER_SECTION_LOG_INSTRUCTION
        if i == 0:
            text = persona_text.strip() + "\n\n" + text
        turns.append(Turn(label=chapter.label, text=text))
    turns.append(Turn(label="end-of-paper", text=END_OF_PAPER_INSTRUCTION.strip()))
    return turns


def dsh_version(dsh_bin: Optional[str] = None) -> str:
    """--dry-run's own docstring claims it works without the SDK
    installed; it should not then die on a missing `dsh` CLI either
    (Borges's nit, PR-76 review) -- report the gap as data instead."""
    try:
        return _run([dsh_bin or "dsh", "--version"])
    except FileNotFoundError:
        return f"not installed ({dsh_bin or 'dsh'} not found on PATH)"


def vanilla_env() -> dict:
    """The NoMemory-arm shape as the SDK's own `env=` kwarg: an empty
    dict. Matches exam_room.memory.none.NoMemory's isolation invariant
    (handle.env={}, handle.mcp_servers=[], handle.plugins=[]) -- no
    ENGRAM_ROOT/ENGRAM_HOME, no MCP server, nothing pointing at any
    memory system."""
    return {}


def write_model_catalog_patch(run_dir: Path, model: str) -> Path:
    """`--model deepseek-flash` (Kepler's confirmed id, forum #428 post
    10473: DeepSeek's docs name it the V4.1-Flash-backed id, image
    input -- deepseek-v4-flash and -vision-exp are now legacy aliases
    served by the same model) is NOT in any installed dsh catalog's
    DEFAULT_MODELS as of this write (checked 0.1.1-rc.2; the driver seat
    is upgrading to 0.1.5-rc.3 before the live run, unconfirmed there
    either). The @deepseek-ai/dsh-llm-deepseek plugin (cordis id
    `llm-deepseek` in the stock headless profile, PROVIDER =
    "deepseek-official") takes its model list as a `models:` config key
    -- z.array(catalogModel).default(DEFAULT_MODELS) -- so an unlisted id
    needs an explicit override, or dsh-tool-fs's read_image will refuse
    to register against it (per its own README: "requires the exact
    routed model to declare image input").

    Writes a minimal cordis patch overriding ONLY the `llm-deepseek`
    plugin's `models` list with the one entry this run needs -- bare
    id-matching (not `insert:`), the documented pattern for overriding an
    already-bundled plugin rather than erroring on a duplicate id.
    CONFIRMED (not unverified) that this config key REPLACES the whole
    catalog, not merges: the reviewer-fairy round on this PR (forum #428
    post 10477) read `resolveModels`'s `(models ?? DEFAULT_MODELS)`
    directly and caught a real blocker in this function's first version --
    the pinned `dsh-llm-deepseek 0.1.7-rc.1` catalog ALREADY declares
    `deepseek-flash` with `contextWindow: 1_000_000`,
    `inputModalities: ["text","image"]`, AND `systemPromptUpdate:
    "in-history"`; my override carried only the first two fields, so on a
    seat with that catalog installed, it would REPLACE the correct entry
    with an incomplete one and silently drop `systemPromptUpdate`. Kepler's
    live smoke test (post 10478) confirmed the override is harmless with
    the pinned provider and asked to KEEP it (it protects an older-catalog
    seat that doesn't have `deepseek-flash` listed at all) -- so the fix
    here is what the fairy actually asked for: copy the real entry
    verbatim, `systemPromptUpdate` included, rather than drop the override.
    Passed via `patches=` on `DeepSeekHarnessConfig` (see run_live), which
    is where an earlier version of THIS function's caller had a different,
    also-wrong `cordis=` kwarg guess, since corrected."""
    patch_path = run_dir / "cordis-model-patch.yml"
    run_dir.mkdir(parents=True, exist_ok=True)
    patch_path.write_text(
        "- id: llm-deepseek\n"
        "  config:\n"
        "    models:\n"
        f"      - id: {model}\n"
        f'        name: "{model}"\n'
        "        contextWindow: 1000000\n"
        '        inputModalities: ["text", "image"]\n'
        '        systemPromptUpdate: "in-history"\n',
        encoding="utf-8",
    )
    return patch_path


def _preflight_turn_figures(
    turns: list[Turn], figures_root: Path
) -> tuple[list[list[dict]], list[list[str]]]:
    """Validates AND builds every turn's figures up front, in one pass per
    turn (colleague-pass fold on spec-figures.md): calls
    turn_content_blocks(turn.text, figures_root) for each turn in document
    order, which raises FileNotFoundError/ValueError on the first invalid
    reference -- so a run whose LAST turn references a missing or
    non-.png figure refuses before turn 0 is ever sent, not partway
    through a session with earlier turns already billed.

    Returns (blocks_per_turn, figures_per_turn) -- parallel lists, one
    entry per turn. `figures_per_turn[i]` is the resolved file names
    (`Path(path).name`, document order) for turn i, extracted via the same
    IMAGE_REF matches that produced blocks_per_turn[i] -- so a name here
    is only ever one whose file has already been proven to exist and be a
    .png, never an unvalidated guess read off the raw text independently
    of that check."""
    blocks_per_turn: list[list[dict]] = []
    figures_per_turn: list[list[str]] = []
    for turn in turns:
        blocks_per_turn.append(turn_content_blocks(turn.text, figures_root))
        figures_per_turn.append(
            [Path(m.group("path")).name for m in IMAGE_REF.finditer(turn.text)]
        )
    return blocks_per_turn, figures_per_turn


def dry_run_report(ctx: RunContext, model_patch: Path) -> str:
    # Validates every turn's figures the same way run_live() does (colleague-
    # pass fold): a dry run must refuse on a missing or non-.png figure too,
    # not just silently report a name that will fail once the run goes live.
    figures_root = ctx.paper_repo / "paper"
    _, figures_per_turn = _preflight_turn_figures(ctx.turns, figures_root)

    lines = [
        "# Fresh-reader run: DRY RUN (no API call made)",
        "",
        f"paper_repo: {ctx.paper_repo}",
        f"paper_sha: {ctx.paper_sha}",
        f"dsh_version: {ctx.dsh_version}",
        f"model: {ctx.model}",
        f"provider: {ctx.provider}",
        f"turn_count: {len(ctx.turns)}",
        f"model_catalog_patch: {model_patch}",
        "",
        "## Planned turn sequence",
        "",
    ]
    for i, turn in enumerate(ctx.turns):
        lines.append(f"{i}. {turn.label} ({len(turn.text)} chars)")
        figure_names = figures_per_turn[i]
        if figure_names:
            lines.append(f"   figures: {', '.join(figure_names)}")
    lines += [
        "",
        "## Status as of the last fold-in (per engram-paper#55 + forum #428)",
        "- Model id settled: 'deepseek-flash' (Kepler, post 10473). Models-"
        "catalog override written above matches the pinned catalog's real "
        "entry verbatim (contextWindow=1000000, image input, "
        "systemPromptUpdate=in-history) -- confirmed to REPLACE the whole "
        "catalog, not merge (reviewer-fairy, post 10477); kept deliberately "
        "so an older-catalog seat without 'deepseek-flash' listed still "
        "gets it declared.",
        "- Live-path SDK call shape smoke-tested end to end by Kepler "
        "(post 10478): turns 0-1 (Abstract + Chapter 1) against the real "
        "API returned substantive per-section logs. Full 18-turn run not "
        "yet attempted.",
        "- Persona/rubric file: Kepler's is the real one to use for the "
        "full run (his stand-in three-liner was enough for the smoke "
        "test) -- read from --persona-file, wherever the caller points it.",
        "- Figures ARE now attached, as image content blocks inside the "
        "turn message (turn_content_blocks). With the notools overlay "
        "applied (below), read_image is disabled along with everything "
        "else, so this is the only path a figure reaches the reader by -- "
        "each standalone `![alt](path)` markdown line in a turn is "
        "replaced by a text marker plus an inline image block, in "
        "document order. NOTE: the finalized rubric (paper/review/"
        "fresh-reader-rubric.md, engram-paper#77) does not itself score "
        "figures explicitly -- the earlier claim here that 'the rubric "
        "scores figures' was inherited from #55's draft text, not "
        "re-verified against the finalized file.",
        "- Per-section/end-of-paper instructions now copied verbatim from "
        "the finalized rubric (#77) -- an earlier version drifted on "
        "items 4-6 and the Clarity-score name (see the module-level "
        "comment above PER_SECTION_LOG_INSTRUCTION).",
        "- CONFIRMED and FIXED (Kepler measured this directly, PR-76 "
        "comment 2026-09-23T16:41:16Z -- not hypothetical): the 'sdk' "
        "profile's default composition sends 25 tools to the model "
        "(bash, read, write, edit, web_search, subagent, ...) with no "
        "model-permission gate, decoded from a live smoke-test session's "
        "own request/header record. Without a fix, a 'never heard of "
        "ENGRAM' reader is one curiosity away from reading the whole "
        "paper on turn 0 and defeating the linear-read premise "
        "undetectably. Fixed by wiring Kepler's verified "
        "fresh-reader-notools.yml overlay into patches= (see run_live) "
        "-- confirmed via --dump-config (every entry disabled) and a "
        "live turn that sent 0 tools. (An earlier version of this note "
        "called the exposure 'unverified' and left the overlay unwired "
        "for ~3 minutes after Kepler's own measurement landed in this "
        "same PR thread -- caught by the round-3 reviewer-fairy, not by "
        "re-reading the thread myself in time.) The run_live() runtime "
        "assertion Kepler suggested -- decode the actual request/header "
        "after turn 0 and refuse if any tool name is present, turning the "
        "persona instruction into a checked fact -- IS implemented, in "
        "paper/review/tools/fresh_reader_guard.py (assert_no_tools), "
        "wired into run_live() immediately after the turn-0 harness.run() "
        "call returns.",
    ]
    return "\n".join(lines)


def _final_no_tools_check(
    dsh_home: Path, session_id: str, out_md: Path, manifest_path: Path
) -> None:
    """Called once, after the turn loop finishes NORMALLY (every turn
    completed with no exception) -- colleague-pass fold round on
    spec-no-tools-guard.md. The turn-0 check in run_live() only verifies
    the first request/header record; this re-decodes the FULL session
    store so every request/header of the whole session is checked, not
    just turn 0's.

    On success: appends `no_tools_check_final: passed (<N> request
    header(s), 0 tools)` to out_md.

    On GuardError (including NoToolsViolation): the reader log (out_md) is
    already complete at this point -- nothing in it is touched or
    deleted. One manifest entry is appended with turn_index=-1,
    label='no_tools_check_final', error=str(exc), and the exception is
    re-raised so the run exits non-zero (the caller's own `finally`
    closes the harness).

    Factored out of run_live() as its own module-level function
    specifically so it can be tested directly against a fake session
    store built from the fixtures, without spinning up a harness."""
    guard_mod = _load_guard()
    try:
        report = guard_mod.assert_no_tools(dsh_home, session_id)
    except guard_mod.GuardError as exc:
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
            f"no_tools_check_final: passed ({report.header_count} "
            "request header(s), 0 tools)\n"
        )


def run_live(
    ctx: RunContext,
    run_dir: Path,
    dsh_bin: Optional[str],
    out_md: Path,
    manifest_path: Path,
    overwrite: bool = False,
) -> None:
    """Drives the actual session via the DeepSeek Harness SDK. Import is
    deferred (not a module-level import) so --dry-run works on a machine
    that never installed the SDK -- this script's default path must not
    require it.

    PyPI TRAP, worth restating here since it fails in a way that looks
    like an unrelated bug: `pip install deepseek-harness` (no `-sdk`
    suffix) installs a DIFFERENT, third-party package that also imports
    as `deepseek_harness` but has no `DeepSeekHarnessConfig` -- the
    correct package is `deepseek-harness-sdk`, needs `--pre` (still
    pre-release as of this write). A wrong install fails loud at this
    import with AttributeError/ImportError on DeepSeekHarnessConfig,
    which is a LUCKY failure (Kepler hit it before checking metadata,
    forum #428 post 10476) -- it could as easily have been a same-named
    attribute that silently behaved differently.

    API shape here is Kepler's own verified read (forum #428 post 10476,
    2026-09-23) against `deepseek-harness-sdk 0.1.5rc1` actually
    installed and imported on his seat -- NOT exam-room's `DshRunner`,
    which was checked against rc7 and is now stale: `DeepSeekHarnessConfig`
    has no `session_root=`/`cordis=` (this function's own first two
    versions used both, guessing from DshRunner and then from partial
    memory of this exact SDK -- both wrong, corrected here from a live
    read of the installed class signature, not another guess). The real
    fields used below: `patches=` (tuple of cordis overlay paths, plural
    -- this call passes one), `dsh_home=` (the session store, replacing
    `session_root=`), `dsh_bin=` (the runtime binary; without it the SDK
    wants its own `deepseek-harness-runtime-bin` platform package),
    `api_key=`. `harness.close()` is called in `finally` -- the runtime
    subprocess is owned by the instance, per the same read.

    PERSIST PER TURN (Kepler's should-fix, forum #428 post 10478): writes
    `out_md` and `manifest_path` incrementally, one section/entry at a
    time as each turn completes, rather than accumulating in memory and
    writing once after all turns return. The prior all-at-once shape
    would lose an entire 18-turn run to a crash on turn 17 -- recoverable
    from the dsh session store, but not what the script's own output
    promises. Returns nothing; both files are the durable record, updated
    live.

    `overwrite=False` (Borges's should-fix, PR-76 review): refuses to
    start if either output file already exists non-empty, since both are
    truncated at the start of a real run and `out_md`'s name repeats
    across every run on the same day -- without this guard, retrying
    after a crash silently destroys the very progress persist-per-turn
    just saved."""
    # Deferred (not module-level) for the same reason as the SDK import
    # below: the dry-run path never calls run_live() at all, so this never
    # executes there, but keeping it out of the module header keeps that
    # invariant visible at the call site rather than relying on control
    # flow elsewhere in the file. Loaded via _load_guard() -- a package-
    # style `from paper.review.tools.fresh_reader_guard import ...` only
    # resolves when the repo root happens to be on sys.path (e.g. under
    # pytest); it raises ModuleNotFoundError under this script's actual
    # invocation shapes (see _load_guard's own docstring). The guard
    # module itself is stdlib-only (its own zstandard use is a further-
    # nested lazy import inside decode_session).
    assert_no_tools = _load_guard().assert_no_tools

    try:
        from deepseek_harness import DeepSeekHarness, DeepSeekHarnessConfig
    except ImportError as exc:
        raise RuntimeError(
            "deepseek-harness-sdk is not installed (pip install --pre "
            "deepseek-harness-sdk -- NOT 'deepseek-harness', a different "
            "package with no DeepSeekHarnessConfig). Required for --live; "
            "--dry-run does not need it."
        ) from exc

    import os
    import uuid

    run_dir.mkdir(parents=True, exist_ok=True)
    model_patch = write_model_catalog_patch(run_dir, ctx.model)
    # Disables every tool the `sdk` profile grants by default (25 of them,
    # per Kepler's decoded live-session measurement, forum #428 / PR-76
    # comment 2026-09-23T16:41:16Z) -- without this, "cannot look ahead or
    # open any file" is a persona INSTRUCTION only, and the rendered paper
    # sits one directory above `cwd`, one bash/read call away from a
    # reader who defeats the whole linear-read premise undetectably. This
    # exact overlay is Kepler's, verified against dsh 0.1.5-rc.3 via
    # --dump-config (every entry disabled) and a live turn (0 tools sent).
    # See the file's own header comment for the two accepted consequences
    # (figures must travel as image content, not read_image; the residual
    # "coding agent" system-prompt line has no found patch target).
    notools_patch = Path(__file__).parent / "fresh-reader-notools.yml"
    config = DeepSeekHarnessConfig(
        provider=ctx.provider,
        model=ctx.model,
        cwd=str(run_dir.resolve()),
        dsh_home=str(run_dir / "dsh-home"),
        dsh_bin=dsh_bin,
        patches=(str(model_patch), str(notools_patch)),
        env=vanilla_env(),
        api_key=os.environ[DEEPSEEK_API_KEY_ENV],
    )
    # A re-run truncates the very durability persist-per-turn exists to
    # buy (Borges's should-fix, PR-76 review): out_md's name is
    # fresh-reader-<model>-<date>.md, the same for every run that day, and
    # run_live() used to write_text()/truncate both files unconditionally
    # at start -- so retrying after a crash at turn 14 wipes the 13
    # sections that persistence just saved. Refuse instead unless the
    # caller passes --overwrite.
    for existing in (out_md, manifest_path):
        if existing.exists() and existing.stat().st_size > 0 and not overwrite:
            raise FileExistsError(
                f"{existing} already exists and is non-empty. A prior run's "
                "output would be silently truncated. Move it aside, or pass "
                "--overwrite if you mean to discard it."
            )

    out_md.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    session_id = f"fresh-reader-{uuid.uuid4().hex}"

    # Pre-flight: validate + build EVERY turn's figures before any paid
    # harness call (colleague-pass fold, spec-figures.md) -- before
    # DeepSeekHarness is even constructed, before harness.start(), and
    # before the reader-log header is written, so a missing/invalid
    # figure in even the LAST turn refuses the whole run up front and
    # leaves no half-written run behind. The rendered paper's
    # `![Figure N](figures/<name>.png)` lines are relative to the paper
    # directory, not the repo root. Figure count is over ALL turns.
    figures_root = ctx.paper_repo / "paper"
    blocks_per_turn, figures_per_turn = _preflight_turn_figures(
        ctx.turns, figures_root
    )
    total_figure_count = sum(len(names) for names in figures_per_turn)

    harness = DeepSeekHarness(config)

    try:
        harness.start()
        out_md.write_text(
            f"# Fresh-reader run\n\nmodel: {ctx.model}\nprovider: {ctx.provider}\n"
            f"paper_sha: {ctx.paper_sha}\ndsh_version: {ctx.dsh_version}\n"
            "figures: attached inline as image blocks "
            f"({total_figure_count} found in the render)\n"
            f"session_id: {session_id}\n"
            f"started_at: {datetime.now(timezone.utc).isoformat()}\n\n---\n",
            encoding="utf-8",
        )
        manifest_path.write_text("", encoding="utf-8")  # truncate/create fresh

        for i, turn in enumerate(ctx.turns):
            entry = RunManifestEntry(
                turn_index=i,
                label=turn.label,
                prompt_chars=len(turn.text),
                started_at=datetime.now(timezone.utc).isoformat(),
                figures_attached=figures_per_turn[i],
            )
            try:
                content_blocks = blocks_per_turn[i]
                result = harness.run(content_blocks, session_id=session_id)
                response_text = result.final_response
                entry.response_chars = len(response_text)
                if i == 0:
                    # Turns the persona's "cannot look ahead, search the
                    # web, or open any file" sentence into a checked fact
                    # (spec-no-tools-guard.md): decode the dsh session
                    # store immediately after this first harness.run()
                    # returns and refuse to continue if any tool reached
                    # the model. Not caught here -- GuardError/
                    # NoToolsViolation fall through to the except clause
                    # below like any other exception, which records
                    # entry.error and re-raises so the run aborts.
                    report = assert_no_tools(Path(config.dsh_home), session_id)
                    with out_md.open("a", encoding="utf-8") as fh:
                        fh.write(
                            f"no_tools_check: passed ({report.header_count} "
                            "request header(s), 0 tools)\n"
                        )
                with out_md.open("a", encoding="utf-8") as fh:
                    fh.write(f"## {turn.label}\n\n{response_text}\n\n")
            except Exception as exc:  # noqa: BLE001 -- record and re-raise
                entry.error = str(exc)
                entry.finished_at = datetime.now(timezone.utc).isoformat()
                with manifest_path.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(entry.__dict__) + "\n")
                ctx.manifest.append(entry)
                raise
            entry.finished_at = datetime.now(timezone.utc).isoformat()
            with manifest_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry.__dict__) + "\n")
            ctx.manifest.append(entry)

        # Every turn completed with no exception -- re-check the FULL
        # session store now, not just turn 0's (colleague-pass fold
        # round). A GuardError/NoToolsViolation here still propagates
        # through this same try/finally, so harness.close() below still
        # runs, and the run still exits non-zero.
        _final_no_tools_check(
            Path(config.dsh_home), session_id, out_md, manifest_path
        )
    finally:
        # The runtime subprocess is owned by this instance (Kepler's read,
        # forum #428 post 10476) -- close it whether the run succeeded,
        # failed mid-turn, or was interrupted.
        harness.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-repo", type=Path, required=True)
    parser.add_argument("--persona-file", type=Path, required=True)
    parser.add_argument(
        "--model",
        required=True,
        help="Exact DeepSeek API model id. No default -- see module docstring.",
    )
    parser.add_argument("--provider", default="deepseek-official")
    parser.add_argument("--out-dir", type=Path, default=Path("/tmp/fresh-reader-run"))
    parser.add_argument(
        "--dsh-bin",
        default=None,
        help=(
            "Path to the dsh runtime binary the SDK should launch "
            "(DeepSeekHarnessConfig's dsh_bin=). Without it the SDK wants "
            "its own deepseek-harness-runtime-bin platform package. "
            "--dry-run's dsh_version report also uses this binary if given."
        ),
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Actually call the API. Without this flag, dry-run only.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Allow --live to overwrite a non-empty prior run's output "
            "(out_md / manifest.jsonl). Without this, a re-run refuses to "
            "start rather than silently truncate a prior run's progress."
        ),
    )
    args = parser.parse_args()
    # A relative --out-dir otherwise crashes: render_fresh() runs
    # render_paper.py with cwd=paper_repo, then this function reads the
    # output path relative to THIS process's cwd -- a relative out_dir
    # resolves against different directories in the two calls (Borges's
    # should-fix, PR-76 review; measured: FileNotFoundError, with the
    # render actually landing inside the paper repo instead). Resolving
    # once here, before either call, makes every downstream use absolute.
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

    ctx = RunContext(
        paper_repo=args.paper_repo,
        paper_sha=paper_sha,
        dsh_version=dsh_version(args.dsh_bin),
        model=args.model,
        provider=args.provider,
        persona_text=persona_text,
        turns=turns,
    )

    if not args.live:
        model_patch = write_model_catalog_patch(args.out_dir / "run", ctx.model)
        print(dry_run_report(ctx, model_patch))
        return 0

    import os

    if not os.environ.get(DEEPSEEK_API_KEY_ENV):
        print(
            f"--live given but {DEEPSEEK_API_KEY_ENV} is not set. Refusing "
            "to start a live run without it.",
            file=sys.stderr,
        )
        return 1

    run_dir = args.out_dir / "run"
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_md = args.paper_repo / "paper" / "review" / f"fresh-reader-{ctx.model}-{date_str}.md"
    manifest_path = args.out_dir / "manifest.jsonl"

    # Both files are written incrementally inside run_live() -- persist
    # per turn (Kepler's should-fix, forum #428 post 10478) -- so by the
    # time this call returns (or raises), whatever completed is already
    # durable on disk, not held only in memory.
    run_live(ctx, run_dir, args.dsh_bin, out_md, manifest_path, args.overwrite)

    print(f"Wrote {out_md}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
