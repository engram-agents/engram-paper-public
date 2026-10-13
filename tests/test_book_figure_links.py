"""Every image link in a rendered book must resolve from the book's own directory.

The renderer used to hardcode `figures/figN-*.png`, which resolves against the
book's directory (`paper/release/`), where no `figures/` exists; the images live
in `paper/figures/`. Both committed books carried 6 broken image links each (6 distinct figures,
each used once per book). The link
is now computed from the `--out` directory, so it is right for any `--out`.
"""
from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path

import pytest

import tools.render_paper as rp

REPO = Path(__file__).resolve().parents[1]
IMAGE_LINK = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def _links(book: Path) -> list[str]:
    return IMAGE_LINK.findall(book.read_text(encoding="utf-8"))


def _assert_all_resolve(book: Path) -> None:
    links = _links(book)
    assert len(links) == 6, f"expected 6 image links, found {len(links)}"
    for link in links:
        assert "\\" not in link
        assert (book.parent / link).is_file(), f"{book.name}: {link} does not resolve"


def _render(lang: str, out: Path, monkeypatch) -> None:
    monkeypatch.chdir(REPO)
    monkeypatch.setattr("sys.argv", ["render_paper.py", "--lang", lang, "--out", str(out)])
    assert rp.main() == 0


@pytest.mark.parametrize("lang", ["en", "zh"])
def test_committed_book_image_links_resolve(lang):
    _assert_all_resolve(REPO / rp.DEFAULT_OUT[lang])


@pytest.mark.parametrize("lang", ["en", "zh"])
def test_fresh_render_in_release_dir_links_resolve(lang, monkeypatch):
    # Same directory as the committed book, so the relative link is the real one.
    release = (REPO / rp.DEFAULT_OUT[lang]).parent
    fd, name = tempfile.mkstemp(suffix=".md", prefix="figlinks-", dir=release)
    os.close(fd)
    out = Path(name)
    try:
        _render(lang, out, monkeypatch)
        _assert_all_resolve(out)
    finally:
        out.unlink(missing_ok=True)


@pytest.mark.parametrize("lang", ["en", "zh"])
def test_links_resolve_for_a_different_out_directory(lang, tmp_path, monkeypatch):
    # Outside paper/: the link must be computed from --out, not hardcoded.
    out = tmp_path / "elsewhere" / "deeper" / f"book.{lang}.md"
    _render(lang, out, monkeypatch)
    _assert_all_resolve(out)
    expected = os.path.relpath(REPO / "paper" / "figures" / "fig6-census.png", out.parent)
    assert expected.replace(os.sep, "/") in _links(out)
