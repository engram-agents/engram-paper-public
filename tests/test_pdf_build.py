"""Contract tests for tools/pdf_build (the DOI-PDF builder), written before the code.

The builder turns the single-file release Markdown into print HTML and then a PDF. The
DOI PDFs (Zenodo 23319376) were built by a converter that lived only on a desk; these
cells pin the committed copy to that converter's behaviour:

  A3  byte identity: the committed converter's HTML for both release files equals the
      desk converter's (borges-desk a693ae5d), pinned by golden sha256s below.
  A4  inline emphasis is importable with no side effects, and does what the PDF shows.
      These cells pin what the DOI PDF shows, NOT a claim the rules are correct in
      general (a conformant CommonMark parser disagrees on some of them; that gap is
      what tools/check_emphasis_render.py measures).
  A5  paragraph joining (the paper site depends on it): lines are stripped and joined
      with ONE space before inline(); an indented list continuation is appended with
      one space.
  A6  print_html_to_pdf imports Playwright lazily, so the suite needs no browser.
  A2  mermaid_to_svg refuses a missing or wrong bundle with a clear message.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
RELEASE = REPO / "paper" / "release"

import tools.pdf_build.paper_to_print_html as p2h  # noqa: E402
import tools.pdf_build.mermaid_to_svg as m2s  # noqa: E402

# --------------------------------------------------------------------------- A3
# Golden sha256s of the HTML the DESK converter (borges-desk a693ae5d,
# tools/paper_to_print_html.py) writes for the two release files AS THEY STAND AT THE
# TIME OF WRITING (paper/release/engram-paper-v0.5.1{,.zh}.md at the branch base
# e06e076). Made once: that desk module was loaded, its `_VENV_PY` pointed at a path
# that does not exist (mermaid renderer unavailable), and its own main() was run with
# `--mermaid-cache <empty dir>` and no banner. Both files hold 2 mermaid blocks; in this
# mode they fall back to the <pre><code> source block, so 0 rendered diagrams.
# These hashes are tied to the release text: when the release files change in the next
# paper version, regenerate them from the desk converter the same way (or retire the
# cell) -- a red here after a text edit is the pin doing its job, not a builder bug.
GOLDEN_HTML_SHA256 = {
    "en": "acfa55d3cdbe8fc0bdd2d90edf21e551dec1d176dc9596bbb1ecda6638b2e4d2",
    "zh": "9ce94821ba00c4506345a6164c9d4f38e784f8a0b36841645b689e3543175b34",
}
RELEASE_FILES = {
    "en": RELEASE / "engram-paper-v0.5.1.md",
    "zh": RELEASE / "engram-paper-v0.5.1.zh.md",
}


def build_html_without_mermaid(mod, src: Path, dst: Path, cache: Path, monkeypatch) -> bytes:
    """Run the module's own main() with the mermaid renderer unavailable."""
    monkeypatch.setattr(mod, "_VENV_PY", Path("/nonexistent/python"))
    monkeypatch.setattr(sys, "argv", ["x", str(src), str(dst), "--mermaid-cache", str(cache)])
    mod.main()
    return dst.read_bytes()


@pytest.mark.parametrize("lang", ["en", "zh"])
def test_committed_converter_html_is_byte_identical_to_the_desk_version(lang, tmp_path, monkeypatch):
    html_bytes = build_html_without_mermaid(
        p2h, RELEASE_FILES[lang], tmp_path / f"{lang}.html", tmp_path / "cache", monkeypatch)
    assert len(html_bytes) > 500_000, "output suspiciously small; the comparison would be vacuous"
    assert b'figure class="diagram"' not in html_bytes, "mermaid must be disabled in this mode"
    assert hashlib.sha256(html_bytes).hexdigest() == GOLDEN_HTML_SHA256[lang]


# --------------------------------------------------------------------------- A4
def test_inline_is_importable_without_side_effects(tmp_path):
    code = (
        "import sys, os; sys.path.insert(0, %r); os.chdir(%r)\n"
        "import tools.pdf_build.paper_to_print_html as m\n"
        "assert callable(m.inline)\n"
        "assert not os.listdir('.'), os.listdir('.')\n"
        "assert 'playwright' not in sys.modules\n"
    ) % (str(REPO), str(tmp_path))
    r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_a_bold_span_of_chinese_text_becomes_strong():
    out = p2h.inline("**诚实是结构性的，而不是愿望性的。**它")
    assert out == "<strong>诚实是结构性的，而不是愿望性的。</strong>它"


def test_agm_postulate_names_stay_literal():
    assert p2h.inline("K*2–K*6") == "K*2–K*6"


def test_two_italics_paragraph_gives_exactly_two_em():
    text = ("*《机器学习研究汇刊》*（Transactions on Machine Learning Research）"
            "我们本会*带着*它来设计")
    out = p2h.inline(text)
    assert re.findall(r"<em>(.*?)</em>", out) == ["《机器学习研究汇刊》", "带着"]


def test_emphasis_markers_inside_a_code_span_stay_code():
    assert p2h.inline("see `**x**` here") == "see <code>**x**</code> here"


def test_a_backslash_escaped_star_stays_literal_and_does_not_pair():
    out = p2h.inline(r"\*a *b*")
    assert out == "*a <em>b</em>"


# --------------------------------------------------------------------------- A5
def test_a_bold_span_crossing_a_line_break_is_bolded():
    html_out = p2h.convert("**bold\ncrossing** end", Path("."))
    assert html_out == "<p><strong>bold crossing</strong> end</p>"


def test_paragraph_lines_are_stripped_and_joined_with_one_space():
    assert p2h.convert("one  \n   two\nthree", Path(".")) == "<p>one two three</p>"


def test_an_indented_list_continuation_is_appended_with_one_space():
    html_out = p2h.convert("- a **b\n    c** d", Path("."))
    assert html_out == "<ul><li>a <strong>b c</strong> d</li></ul>"


# --------------------------------------------------------------------------- A6
def test_print_html_to_pdf_import_does_not_import_playwright():
    code = (
        "import sys; sys.path.insert(0, %r)\n"
        "import tools.pdf_build.print_html_to_pdf as m\n"
        "assert callable(m.main)\n"
        "assert 'playwright' not in sys.modules, 'playwright imported eagerly'\n"
    ) % str(REPO)
    r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


# --------------------------------------------------------------------------- A2
def test_the_default_interpreter_is_not_the_desk_venv():
    assert "/.engram/venv/" not in str(p2h._VENV_PY)


def test_mermaid_bundle_missing_fails_with_a_clear_message(tmp_path):
    with pytest.raises(SystemExit) as e:
        m2s.check_bundle(tmp_path / "nope.js")
    msg = str(e.value)
    assert "missing" in msg and "11.17.2" in msg and m2s.BUNDLE_SHA256 in msg


def test_mermaid_bundle_with_wrong_sha256_fails_naming_both_hashes(tmp_path):
    bad = tmp_path / "mermaid.min.js"
    bad.write_bytes(b"not mermaid")
    with pytest.raises(SystemExit) as e:
        m2s.check_bundle(bad)
    msg = str(e.value)
    assert "sha256" in msg and m2s.BUNDLE_SHA256 in msg
    assert hashlib.sha256(b"not mermaid").hexdigest() in msg


def test_mermaid_bundle_with_the_pinned_sha256_passes(tmp_path, monkeypatch):
    good = tmp_path / "mermaid.min.js"
    good.write_bytes(b"stand-in")
    monkeypatch.setattr(m2s, "BUNDLE_SHA256", hashlib.sha256(b"stand-in").hexdigest())
    m2s.check_bundle(good)  # no raise


def test_the_pinned_bundle_sha256_is_the_one_in_the_spec():
    assert m2s.BUNDLE_SHA256 == "581ed7d74bd9048d0e3a91363927d72ef22942d7722546b27f7cc29e35390eb8"
