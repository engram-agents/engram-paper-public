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


# ------------------------------------------------------------------ S1: --require-mermaid
# Without the flag a missing bundle or renderer degrades to source blocks and exits 0
# (pinned byte-for-byte by the A3 cells). WITH the flag any of: missing bundle,
# hash-mismatched bundle, unavailable renderer, a diagram that fails to render, must exit
# non-zero naming the cause, and leave no output file.
MERMAID_MD = "# T\n\n```mermaid\ngraph TD; A-->B\n```\n"
STUB_OK = ('import sys\n'
           'def check_bundle(path=None):\n    pass\n'
           'if __name__ == "__main__":\n'
           '    open(sys.argv[2], "w").write("<svg width=\\"10\\"></svg>")\n')
STUB_FAIL = ('import sys\n'
             'def check_bundle(path=None):\n    pass\n'
             'if __name__ == "__main__":\n'
             '    sys.stderr.write("boom"); sys.exit(3)\n')


def run_strict(tmp_path, monkeypatch, renderer_dir=None, interpreter=sys.executable, flag=True):
    src = tmp_path / "in.md"
    src.write_text(MERMAID_MD, encoding="utf-8")
    dst = tmp_path / "out.html"
    if renderer_dir is not None:
        monkeypatch.setattr(p2h, "_RENDERER", renderer_dir / "mermaid_to_svg.py")
    monkeypatch.setattr(p2h, "_VENV_PY", Path(interpreter))
    argv = ["x", str(src), str(dst), "--mermaid-cache", str(tmp_path / "cache")]
    monkeypatch.setattr(sys, "argv", argv + (["--require-mermaid"] if flag else []))
    return dst


def renderer_copy(tmp_path, bundle_bytes=None):
    """A copy of the real mermaid_to_svg.py in tmp, so BUNDLE resolves to tmp/vendor."""
    d = tmp_path / "renderer"
    d.mkdir()
    (d / "mermaid_to_svg.py").write_text(
        (REPO / "tools/pdf_build/mermaid_to_svg.py").read_text(encoding="utf-8"), encoding="utf-8")
    if bundle_bytes is not None:
        (d / "vendor").mkdir()
        (d / "vendor" / "mermaid.min.js").write_bytes(bundle_bytes)
    return d


def test_require_mermaid_with_a_missing_bundle_exits_nonzero_and_writes_nothing(tmp_path, monkeypatch):
    dst = run_strict(tmp_path, monkeypatch, renderer_dir=renderer_copy(tmp_path))
    with pytest.raises(SystemExit) as e:
        p2h.main()
    assert e.value.code not in (0, None)
    assert "bundle missing" in str(e.value)
    assert not dst.exists()


def test_require_mermaid_with_a_mismatched_bundle_exits_nonzero_and_writes_nothing(tmp_path, monkeypatch):
    dst = run_strict(tmp_path, monkeypatch, renderer_dir=renderer_copy(tmp_path, b"not mermaid"))
    with pytest.raises(SystemExit) as e:
        p2h.main()
    assert e.value.code not in (0, None)
    assert "sha256 mismatch" in str(e.value)
    assert not dst.exists()


def test_require_mermaid_with_an_unavailable_renderer_exits_nonzero_and_writes_nothing(tmp_path, monkeypatch):
    dst = run_strict(tmp_path, monkeypatch, renderer_dir=renderer_copy(tmp_path, b"x"),
                     interpreter="/nonexistent/python")
    with pytest.raises(SystemExit) as e:
        p2h.main()
    assert e.value.code not in (0, None)
    assert "renderer unavailable" in str(e.value)
    assert not dst.exists()


def test_require_mermaid_with_a_diagram_that_fails_to_render_exits_nonzero_and_removes_output(tmp_path, monkeypatch):
    d = tmp_path / "stub"
    d.mkdir()
    (d / "mermaid_to_svg.py").write_text(STUB_FAIL, encoding="utf-8")
    dst = run_strict(tmp_path, monkeypatch, renderer_dir=d)
    dst.write_text("stale output from an earlier run", encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        p2h.main()
    assert e.value.code not in (0, None)
    assert "failed to render" in str(e.value) and "boom" in str(e.value)
    assert not dst.exists()


def test_require_mermaid_succeeds_when_the_renderer_works(tmp_path, monkeypatch):
    d = tmp_path / "stub"
    d.mkdir()
    (d / "mermaid_to_svg.py").write_text(STUB_OK, encoding="utf-8")
    dst = run_strict(tmp_path, monkeypatch, renderer_dir=d)
    p2h.main()
    out = dst.read_text(encoding="utf-8")
    assert 'figure class="diagram"' in out and "mermaid-svg" in out


def test_without_the_flag_a_missing_renderer_still_falls_back_and_exits_zero(tmp_path, monkeypatch):
    dst = run_strict(tmp_path, monkeypatch, interpreter="/nonexistent/python", flag=False)
    p2h.main()
    out = dst.read_text(encoding="utf-8")
    assert "<pre><code>graph TD" in out and 'figure class="diagram"' not in out


# ------------------------------------------------- R1-R3: the strict path trusts nothing
import hashlib as _hashlib  # noqa: E402

DIAGRAM = "graph TD; A-->B"


def stub_writing(tmp_path, svg_literal):
    """A stub renderer whose check_bundle passes and which writes `svg_literal` as the SVG."""
    d = tmp_path / "stub"
    d.mkdir()
    (d / "mermaid_to_svg.py").write_text(
        'import sys\n'
        'def check_bundle(path=None):\n    pass\n'
        'if __name__ == "__main__":\n'
        f'    open(sys.argv[2], "wb").write({svg_literal!r})\n', encoding="utf-8")
    return d


INVALID_SVGS = [
    pytest.param(b"", id="empty"),
    pytest.param(b"garbage, not xml", id="garbage"),
    pytest.param(b"<svg width='10'", id="svg-prefix-but-truncated"),
    pytest.param(b"<html><body/></html>", id="well-formed-but-not-svg-root"),
]


@pytest.mark.parametrize("bad", INVALID_SVGS)
def test_require_mermaid_rejects_an_invalid_rendered_svg(bad, tmp_path, monkeypatch):
    dst = run_strict(tmp_path, monkeypatch, renderer_dir=stub_writing(tmp_path, bad))
    with pytest.raises(SystemExit) as e:
        p2h.main()
    assert e.value.code not in (0, None)
    assert "invalid SVG" in str(e.value)
    assert not dst.exists()


def test_require_mermaid_accepts_a_namespaced_svg_with_an_xml_prolog(tmp_path, monkeypatch):
    good = b'<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" width="5"><g/></svg>'
    dst = run_strict(tmp_path, monkeypatch, renderer_dir=stub_writing(tmp_path, good))
    p2h.main()
    assert 'class="mermaid-svg"' in dst.read_text(encoding="utf-8")


def seed_cache(tmp_path, content: bytes):
    cache = tmp_path / "cache"
    cache.mkdir()
    key = _hashlib.sha1(DIAGRAM.encode("utf-8")).hexdigest()[:16]
    (cache / f"mermaid-{key}.svg").write_bytes(content)


@pytest.mark.parametrize("bad", INVALID_SVGS)
def test_require_mermaid_does_not_trust_an_invalid_cached_svg(bad, tmp_path, monkeypatch):
    # Cache validation (not bundle-keyed): every hit is parsed like a fresh render.
    seed_cache(tmp_path, bad)
    dst = run_strict(tmp_path, monkeypatch, renderer_dir=stub_writing(tmp_path, b"<svg/>"))
    with pytest.raises(SystemExit) as e:
        p2h.main()
    assert e.value.code not in (0, None)
    assert "invalid SVG" in str(e.value) and "cache" in str(e.value)
    assert not dst.exists()


def test_without_the_flag_a_garbage_cached_svg_is_still_inlined_unchanged(tmp_path, monkeypatch):
    seed_cache(tmp_path, b"garbage, not xml")
    dst = run_strict(tmp_path, monkeypatch, flag=False)
    p2h.main()
    assert '<figure class="diagram">garbage, not xml</figure>' in dst.read_text(encoding="utf-8")


def test_any_exception_in_a_require_mermaid_run_removes_the_output(tmp_path, monkeypatch):
    d = tmp_path / "stub"
    d.mkdir()
    (d / "mermaid_to_svg.py").write_text(
        'def check_bundle(path=None):\n    raise ValueError("unexpected")\n', encoding="utf-8")
    dst = run_strict(tmp_path, monkeypatch, renderer_dir=d)
    dst.write_text("stale output from an earlier run", encoding="utf-8")
    with pytest.raises(ValueError):
        p2h.main()
    assert not dst.exists()


# ------------------------------------------- round 5: argparse; the output can never be the input
def run_argv(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["x", *map(str, args)])


def test_flag_first_invocation_never_deletes_the_input(tmp_path, monkeypatch):
    # Positional sys.argv parsing made `--require-mermaid in.md out.html` read dst = in.md,
    # and the strict-failure cleanup then deleted the INPUT.
    src = tmp_path / "in.md"
    src.write_text(MERMAID_MD, encoding="utf-8")
    before = src.read_bytes()
    dst = tmp_path / "out.html"
    monkeypatch.setattr(p2h, "_RENDERER", renderer_copy(tmp_path) / "mermaid_to_svg.py")  # no bundle
    monkeypatch.setattr(p2h, "_VENV_PY", Path(sys.executable))
    run_argv(monkeypatch, "--require-mermaid", src, dst, "--mermaid-cache", tmp_path / "cache")
    with pytest.raises(SystemExit) as e:
        p2h.main()
    assert e.value.code not in (0, None) and "bundle missing" in str(e.value)
    assert src.read_bytes() == before
    assert not dst.exists()


def test_output_equal_to_input_is_refused_and_the_input_is_untouched(tmp_path, monkeypatch):
    src = tmp_path / "in.html"  # even with an .html name, same file is refused
    src.write_text("<p>precious</p>", encoding="utf-8")
    before = src.read_bytes()
    for out in (src, tmp_path / "." / "in.html"):
        run_argv(monkeypatch, src, out, "--require-mermaid")
        with pytest.raises(SystemExit) as e:
            p2h.main()
        assert e.value.code not in (0, None) and "same file" in str(e.value)
        assert src.read_bytes() == before


def test_output_equal_to_input_through_a_symlink_is_refused(tmp_path, monkeypatch):
    src = tmp_path / "in.html"
    src.write_text("<p>precious</p>", encoding="utf-8")
    link = tmp_path / "link.html"
    link.symlink_to(src)
    run_argv(monkeypatch, src, link)
    with pytest.raises(SystemExit) as e:
        p2h.main()
    assert "same file" in str(e.value)
    assert src.read_text(encoding="utf-8") == "<p>precious</p>"


@pytest.mark.parametrize("name", ["out.md", "out", "out.txt", "out.html.bak"])
def test_output_that_is_not_html_is_refused_and_nothing_is_written(name, tmp_path, monkeypatch):
    src = tmp_path / "in.md"
    src.write_text("# T\n", encoding="utf-8")
    run_argv(monkeypatch, src, tmp_path / name)
    with pytest.raises(SystemExit) as e:
        p2h.main()
    assert e.value.code not in (0, None) and ".html" in str(e.value)
    assert not (tmp_path / name).exists()


def test_flags_after_the_positionals_and_between_them_still_work(tmp_path, monkeypatch):
    src = tmp_path / "in.md"
    src.write_text("# T\n", encoding="utf-8")
    dst = tmp_path / "out.html"
    run_argv(monkeypatch, src, dst, "--banner", "BANNER-ONE", "--mermaid-cache", tmp_path / "c")
    p2h.main()
    assert "BANNER-ONE" in dst.read_text(encoding="utf-8")
    dst2 = tmp_path / "out2.HTM"
    run_argv(monkeypatch, src, "--banner", "BANNER-TWO", dst2)
    p2h.main()
    assert "BANNER-TWO" in dst2.read_text(encoding="utf-8")


def test_a_stale_output_at_the_declared_path_is_still_removed_on_strict_failure(tmp_path, monkeypatch):
    src = tmp_path / "in.md"
    src.write_text(MERMAID_MD, encoding="utf-8")
    dst = tmp_path / "out.html"
    dst.write_text("an older good-looking build", encoding="utf-8")
    monkeypatch.setattr(p2h, "_RENDERER", renderer_copy(tmp_path) / "mermaid_to_svg.py")
    run_argv(monkeypatch, src, dst, "--require-mermaid")
    with pytest.raises(SystemExit):
        p2h.main()
    assert not dst.exists() and src.exists()


# ---------------------------------- round 5: the same guard on the other two scripts' outputs
import tools.pdf_build.print_html_to_pdf as h2p  # noqa: E402


def test_mermaid_to_svg_refuses_output_equal_to_input_before_rendering(tmp_path, monkeypatch):
    mmd = tmp_path / "d.svg"  # even with an .svg name, the same file is refused
    mmd.write_text("graph TD; A-->B", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["x", str(mmd), str(mmd)])
    with pytest.raises(SystemExit) as e:
        m2s.main()
    assert "same file" in str(e.value)
    assert mmd.read_text(encoding="utf-8") == "graph TD; A-->B"


def test_mermaid_to_svg_refuses_a_non_svg_output_before_rendering(tmp_path, monkeypatch):
    mmd = tmp_path / "d.mmd"
    mmd.write_text("graph TD; A-->B", encoding="utf-8")
    out = tmp_path / "out.txt"
    monkeypatch.setattr(sys, "argv", ["x", str(mmd), str(out)])
    with pytest.raises(SystemExit) as e:
        m2s.main()
    assert ".svg" in str(e.value) and not out.exists()


def test_print_html_to_pdf_refuses_output_equal_to_input(tmp_path, monkeypatch):
    f = tmp_path / "in.pdf"
    f.write_bytes(b"precious")
    monkeypatch.setattr(sys, "argv", ["x", str(f), str(f)])
    with pytest.raises(SystemExit) as e:
        h2p.main()
    assert "same file" in str(e.value) and f.read_bytes() == b"precious"


def test_print_html_to_pdf_refuses_a_non_pdf_output(tmp_path, monkeypatch):
    html_in = tmp_path / "in.html"
    html_in.write_text("<p>x</p>", encoding="utf-8")
    out = tmp_path / "out.html"
    monkeypatch.setattr(sys, "argv", ["x", str(html_in), str(out)])
    with pytest.raises(SystemExit) as e:
        h2p.main()
    assert ".pdf" in str(e.value) and not out.exists()
