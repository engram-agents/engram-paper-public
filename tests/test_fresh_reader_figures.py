"""Contract tests for `paper.review.tools.fresh_reader_run.turn_content_blocks`
(+ its wiring into `run_live`/`dry_run_report`/`RunManifestEntry`), written
BEFORE the implementation per spec-figures.md — expected to fail with an
ImportError/AttributeError until the function/fields exist.

Uses the `tests/__init__.py` package so `paper.review.tools.fresh_reader_run`
imports as an absolute package regardless of pytest's invocation directory,
matching the existing `tests/test_fresh_reader_guard.py` /
`tests/test_render_apparatus.py` convention.
"""

from __future__ import annotations

import base64
import sys
import types
from pathlib import Path

import pytest

from paper.review.tools.fresh_reader_run import (
    IMAGE_REF,
    RunContext,
    RunManifestEntry,
    Turn,
    dry_run_report,
    run_live,
    turn_content_blocks,
)

# A real 1x1 PNG so tests exercise real base64/bytes, not a placeholder.
_PNG_1PX = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgAAIAAAUAAen63NgAAAAASUVORK5CYII="
)


def _write_png(root: Path, rel: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(_PNG_1PX)
    return p


# ── IMAGE_REF regex ─────────────────────────────────────────────────────


def test_image_ref_matches_bare_line():
    m = IMAGE_REF.search("![Figure 1](figures/fig1.png)")
    assert m is not None
    assert m.group("alt") == "Figure 1"
    assert m.group("path") == "figures/fig1.png"


def test_image_ref_does_not_match_inline_with_trailing_text():
    # Contract requires "one markdown image on its own line" -- trailing
    # non-whitespace after the closing paren must NOT match.
    assert IMAGE_REF.search("See ![Figure 1](figures/fig1.png) above.") is None


# ── 1. No image line ─────────────────────────────────────────────────────


def test_no_image_line_returns_single_byte_identical_text_block(tmp_path):
    text = "# Chapter 1\n\nSome plain prose with no figures at all.\n"
    blocks = turn_content_blocks(text, tmp_path)
    assert blocks == [{"type": "text", "text": text}]


# ── 2. One image line ─────────────────────────────────────────────────────


def test_one_image_line_middle_three_blocks_in_order(tmp_path):
    _write_png(tmp_path, "figures/fig1.png")
    text = (
        "Intro paragraph before the figure.\n\n"
        "![Figure 1](figures/fig1.png)\n\n"
        "Paragraph after the figure."
    )
    blocks = turn_content_blocks(text, tmp_path)
    assert len(blocks) == 3
    assert blocks[0]["type"] == "text"
    assert "Intro paragraph before the figure." in blocks[0]["text"]
    # the image markdown line itself must be gone, replaced by the marker
    assert "![Figure 1]" not in blocks[0]["text"]
    assert "[Figure: Figure 1 — attached as an image below]" in blocks[0]["text"]
    assert blocks[1] == {
        "type": "image",
        "data": base64.b64encode(_PNG_1PX).decode("ascii"),
        "mimeType": "image/png",
    }
    assert blocks[2]["type"] == "text"
    assert blocks[2]["text"] == "\nParagraph after the figure."


def test_one_image_line_at_end_omits_trailing_text_block(tmp_path):
    _write_png(tmp_path, "figures/fig1.png")
    text = "Some lead-in text.\n\n![Figure 1](figures/fig1.png)"
    blocks = turn_content_blocks(text, tmp_path)
    assert len(blocks) == 2
    assert blocks[0]["type"] == "text"
    assert blocks[1]["type"] == "image"
    # never an empty trailing text block
    assert not any(b["type"] == "text" and b["text"] == "" for b in blocks)


def test_no_surrounding_text_is_dropped_and_paragraphs_not_merged(tmp_path):
    _write_png(tmp_path, "figures/fig1.png")
    before = "Paragraph A.\n\nParagraph B."
    after = "Paragraph C.\n\nParagraph D."
    text = f"{before}\n\n![Figure 1](figures/fig1.png)\n\n{after}"
    blocks = turn_content_blocks(text, tmp_path)
    assert "Paragraph A." in blocks[0]["text"]
    assert "Paragraph B." in blocks[0]["text"]
    assert "Paragraph C." in blocks[-1]["text"]
    assert "Paragraph D." in blocks[-1]["text"]
    # paragraphs not merged: the blank-line separation must survive
    assert "\n\n" in blocks[0]["text"]
    assert "\n\n" in blocks[-1]["text"]


# ── 3. Two or more image lines ────────────────────────────────────────────


def test_six_figures_alternating_blocks_in_document_order(tmp_path):
    """The spec's own six-figure case, built from a synthetic render (does
    not depend on the real paper)."""
    names = [
        "fig1-reasoning-type.png",
        "fig2-node-type.png",
        "fig3-quote-type.png",
        "fig4-depth-inversion.png",
        "fig5-growth.png",
        "fig6-census.png",
    ]
    for n in names:
        _write_png(tmp_path, f"figures/{n}")

    parts = ["Opening prose for the chapter."]
    for i, n in enumerate(names):
        parts.append(f"![Fig {i + 1} alt text](figures/{n})")
        parts.append(f"Prose paragraph number {i + 1} after that figure.")
    text = "\n\n".join(parts)

    blocks = turn_content_blocks(text, tmp_path)

    image_blocks = [b for b in blocks if b["type"] == "image"]
    text_blocks = [b for b in blocks if b["type"] == "text"]
    assert len(image_blocks) == 6
    # 6 images => 7 text blocks if none are dropped (leading + between each
    # pair + trailing), since neither the first nor the last line is an
    # image line in this synthetic render.
    assert len(text_blocks) == 7

    # alternating, document order: text, image, text, image, ..., text
    types_seen = [b["type"] for b in blocks]
    assert types_seen == ["text", "image"] * 6 + ["text"]

    expected_bytes = base64.b64encode(_PNG_1PX).decode("ascii")
    for img in image_blocks:
        assert img["data"] == expected_bytes
        assert img["mimeType"] == "image/png"

    # no markdown image syntax leaks into any text block
    for tb in text_blocks:
        assert "![" not in tb["text"]
    # every alt marker line shows up, in order, across the text blocks
    joined_text = "".join(tb["text"] for tb in text_blocks)
    for i in range(6):
        assert f"[Figure: Fig {i + 1} alt text — attached as an image below]" in joined_text


# ── 4. Missing file ────────────────────────────────────────────────────────


def test_missing_figure_file_raises_file_not_found_naming_path(tmp_path):
    text = "Some text.\n\n![Figure 1](figures/does-not-exist.png)\n\nMore text."
    with pytest.raises(FileNotFoundError) as exc_info:
        turn_content_blocks(text, tmp_path)
    msg = str(exc_info.value)
    assert "does-not-exist.png" in msg


def test_missing_figure_file_never_sent_as_bare_text(tmp_path):
    text = "![Figure 1](figures/nope.png)"
    with pytest.raises(FileNotFoundError):
        turn_content_blocks(text, tmp_path)


# ── 5. Non-.png extension ──────────────────────────────────────────────────


def test_non_png_extension_raises_value_error_naming_it(tmp_path):
    jpg = tmp_path / "figures" / "fig1.jpg"
    jpg.parent.mkdir(parents=True, exist_ok=True)
    jpg.write_bytes(_PNG_1PX)
    text = "![Figure 1](figures/fig1.jpg)"
    with pytest.raises(ValueError) as exc_info:
        turn_content_blocks(text, tmp_path)
    msg = str(exc_info.value)
    assert "fig1.jpg" in msg or ".jpg" in msg


# ── 6. mimeType / base64 encoding exactness ────────────────────────────────


def test_data_is_standard_base64_no_prefix_no_newlines(tmp_path):
    _write_png(tmp_path, "figures/fig1.png")
    text = "![Figure 1](figures/fig1.png)"
    blocks = turn_content_blocks(text, tmp_path)
    image_block = next(b for b in blocks if b["type"] == "image")
    data = image_block["data"]
    assert not data.startswith("data:")
    assert "\n" not in data
    assert base64.b64decode(data) == _PNG_1PX
    assert image_block["mimeType"] == "image/png"


# ── 8. RunManifestEntry.figures_attached ───────────────────────────────────


def test_manifest_entry_figures_attached_defaults_to_empty_list():
    entry = RunManifestEntry(turn_index=0, label="Abstract", prompt_chars=10)
    assert entry.figures_attached == []


def test_manifest_entry_figures_attached_accepts_names():
    entry = RunManifestEntry(
        turn_index=1, label="Ch1", prompt_chars=10, figures_attached=["fig1.png"]
    )
    assert entry.figures_attached == ["fig1.png"]


# ── 10. dry_run_report lists figure names per turn ─────────────────────────


def test_dry_run_report_lists_figures_per_turn(tmp_path):
    # dry_run_report now validates figures too (colleague-pass fold), so
    # both referenced files must genuinely exist under
    # <paper_repo>/paper/figures/.
    _write_png(tmp_path, "paper/figures/a.png")
    _write_png(tmp_path, "paper/figures/b.png")
    turns = [
        Turn(label="Abstract", text="No figures here."),
        Turn(
            label="Chapter 1",
            text="prose\n\n![Fig A](figures/a.png)\n\nmore prose\n\n"
            "![Fig B](figures/b.png)\n\ntail",
        ),
    ]
    ctx = RunContext(
        paper_repo=tmp_path,
        paper_sha="deadbeef",
        dsh_version="1.0",
        model="deepseek-flash",
        provider="deepseek-official",
        persona_text="persona",
        turns=turns,
    )
    report = dry_run_report(ctx, tmp_path / "patch.yml")
    # figure file names attached to Chapter 1 appear in the report
    assert "a.png" in report
    assert "b.png" in report
    # the stale "figures are not attached" status line is gone
    assert "Figures are not yet attached" not in report


# ── 7 & 9. run_live wiring: content blocks + header count-before-turn-0 ────


class _FakeResult:
    def __init__(self, text: str) -> None:
        self.final_response = text


class _FakeHarness:
    all_run_contents = []
    last_session_id = None

    def __init__(self, config):
        self.config = config
        _FakeHarness.all_run_contents = []

    def start(self):
        pass

    def run(self, content, session_id=None):
        _FakeHarness.all_run_contents.append(content)
        _FakeHarness.last_session_id = session_id
        return _FakeResult("ok")

    def close(self):
        pass


class _FakeConfig:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.dsh_home = kwargs.get("dsh_home")


class _FakeGuardReport:
    header_count = 1


class _FakeGuardModule:
    @staticmethod
    def assert_no_tools(dsh_home, session_id):
        return _FakeGuardReport()


def test_run_live_sends_content_blocks_not_bare_string(tmp_path, monkeypatch):
    """figures_root is computed INSIDE run_live() as ctx.paper_repo / "paper"
    (spec item 7) -- not passed as a parameter. So the PNG must live under
    <ctx.paper_repo>/paper/figures/, matching the real repo layout."""
    import paper.review.tools.fresh_reader_run as run_module

    paper_repo = tmp_path / "paper_repo"
    _write_png(paper_repo, "paper/figures/a.png")

    fake_sdk = types.SimpleNamespace(
        DeepSeekHarness=_FakeHarness, DeepSeekHarnessConfig=_FakeConfig
    )
    monkeypatch.setitem(sys.modules, "deepseek_harness", fake_sdk)
    monkeypatch.setattr(run_module, "_load_guard", lambda: _FakeGuardModule)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")

    turns = [
        Turn(
            label="Abstract",
            text="intro\n\n![Fig A](figures/a.png)\n\ntail",
        ),
        Turn(label="end-of-paper", text="wrap up"),
    ]
    ctx = RunContext(
        paper_repo=paper_repo,
        paper_sha="deadbeef",
        dsh_version="1.0",
        model="deepseek-flash",
        provider="deepseek-official",
        persona_text="persona",
        turns=turns,
    )

    out_md = tmp_path / "out.md"
    manifest_path = tmp_path / "manifest.jsonl"
    run_module.run_live(
        ctx,
        run_dir=tmp_path / "run",
        dsh_bin=None,
        out_md=out_md,
        manifest_path=manifest_path,
        overwrite=True,
    )

    # harness.run() was called with a list of content blocks, not a bare
    # str -- for turn 0, which carries the image line.
    turn0_content = _FakeHarness.all_run_contents[0]
    assert isinstance(turn0_content, list)
    assert any(b.get("type") == "image" for b in turn0_content)

    header = out_md.read_text(encoding="utf-8")
    # header count is over ALL turns, computed before turn 0
    assert "figures: attached inline as image blocks (1 found in the render)" in header


def test_run_live_header_figure_count_zero_when_no_figures(tmp_path, monkeypatch):
    import paper.review.tools.fresh_reader_run as run_module

    paper_repo = tmp_path / "paper_repo"
    (paper_repo / "paper").mkdir(parents=True, exist_ok=True)

    fake_sdk = types.SimpleNamespace(
        DeepSeekHarness=_FakeHarness, DeepSeekHarnessConfig=_FakeConfig
    )
    monkeypatch.setitem(sys.modules, "deepseek_harness", fake_sdk)
    monkeypatch.setattr(run_module, "_load_guard", lambda: _FakeGuardModule)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")

    turns = [Turn(label="Abstract", text="no figures at all")]
    ctx = RunContext(
        paper_repo=paper_repo,
        paper_sha="deadbeef",
        dsh_version="1.0",
        model="deepseek-flash",
        provider="deepseek-official",
        persona_text="persona",
        turns=turns,
    )

    out_md = tmp_path / "out2.md"
    manifest_path = tmp_path / "manifest2.jsonl"
    run_module.run_live(
        ctx,
        run_dir=tmp_path / "run2",
        dsh_bin=None,
        out_md=out_md,
        manifest_path=manifest_path,
        overwrite=True,
    )
    header = out_md.read_text(encoding="utf-8")
    assert "figures: attached inline as image blocks (0 found in the render)" in header


# ── Colleague-pass fold: pre-flight every turn's figures before the first
#    paid turn ─────────────────────────────────────────────────────────────


class _FakeHarnessCounting:
    """Class-level (not instance-level) counters, deliberately -- so the
    assertion `start_count == 0 and run_count == 0` holds true even when
    run_live() never gets far enough to construct a DeepSeekHarness
    instance at all (the pre-flight case under test raises before
    construction)."""

    start_count = 0
    run_count = 0

    def __init__(self, config):
        self.config = config

    def start(self):
        _FakeHarnessCounting.start_count += 1

    def run(self, content, session_id=None):
        _FakeHarnessCounting.run_count += 1
        return _FakeResult("ok")

    def close(self):
        pass


def test_run_live_preflights_all_turns_before_any_paid_call(tmp_path, monkeypatch):
    """A synthetic render whose LAST turn references a missing figure must
    raise FileNotFoundError before harness.start() and before any
    harness.run() -- the whole run refuses up front, not partway through
    a live session with earlier turns already billed."""
    import paper.review.tools.fresh_reader_run as run_module

    paper_repo = tmp_path / "paper_repo"
    (paper_repo / "paper").mkdir(parents=True, exist_ok=True)

    _FakeHarnessCounting.start_count = 0
    _FakeHarnessCounting.run_count = 0
    fake_sdk = types.SimpleNamespace(
        DeepSeekHarness=_FakeHarnessCounting, DeepSeekHarnessConfig=_FakeConfig
    )
    monkeypatch.setitem(sys.modules, "deepseek_harness", fake_sdk)
    monkeypatch.setattr(run_module, "_load_guard", lambda: _FakeGuardModule)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")

    turns = [
        Turn(label="Abstract", text="no figures in this turn at all"),
        Turn(label="Chapter 1", text="still no figures in this one either"),
        Turn(
            label="end-of-paper",
            text="wrap up\n\n![Fig Z](figures/missing.png)",
        ),
    ]
    ctx = RunContext(
        paper_repo=paper_repo,
        paper_sha="deadbeef",
        dsh_version="1.0",
        model="deepseek-flash",
        provider="deepseek-official",
        persona_text="persona",
        turns=turns,
    )

    out_md = tmp_path / "out.md"
    manifest_path = tmp_path / "manifest.jsonl"
    with pytest.raises(FileNotFoundError) as exc_info:
        run_module.run_live(
            ctx,
            run_dir=tmp_path / "run",
            dsh_bin=None,
            out_md=out_md,
            manifest_path=manifest_path,
            overwrite=True,
        )
    assert "missing.png" in str(exc_info.value)

    assert _FakeHarnessCounting.start_count == 0
    assert _FakeHarnessCounting.run_count == 0
    # no half-written reader log -- the refusal must leave nothing behind
    assert not out_md.exists()


def test_dry_run_report_raises_on_missing_figure_in_last_turn(tmp_path):
    """The same synthetic case makes the dry run raise too -- a dry run
    must refuse on a missing or non-PNG figure, not just report it."""
    paper_repo = tmp_path / "paper_repo"
    (paper_repo / "paper").mkdir(parents=True, exist_ok=True)

    turns = [
        Turn(label="Abstract", text="no figures in this turn at all"),
        Turn(
            label="end-of-paper",
            text="wrap up\n\n![Fig Z](figures/missing.png)",
        ),
    ]
    ctx = RunContext(
        paper_repo=paper_repo,
        paper_sha="deadbeef",
        dsh_version="1.0",
        model="deepseek-flash",
        provider="deepseek-official",
        persona_text="persona",
        turns=turns,
    )
    with pytest.raises(FileNotFoundError) as exc_info:
        dry_run_report(ctx, tmp_path / "patch.yml")
    assert "missing.png" in str(exc_info.value)


def test_dry_run_report_raises_on_non_png_extension(tmp_path):
    paper_repo = tmp_path / "paper_repo"
    jpg = paper_repo / "paper" / "figures" / "fig1.jpg"
    jpg.parent.mkdir(parents=True, exist_ok=True)
    jpg.write_bytes(_PNG_1PX)

    turns = [Turn(label="Chapter 1", text="![Fig A](figures/fig1.jpg)")]
    ctx = RunContext(
        paper_repo=paper_repo,
        paper_sha="deadbeef",
        dsh_version="1.0",
        model="deepseek-flash",
        provider="deepseek-official",
        persona_text="persona",
        turns=turns,
    )
    with pytest.raises(ValueError):
        dry_run_report(ctx, tmp_path / "patch.yml")
