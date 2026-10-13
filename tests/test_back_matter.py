"""Contract tests for the back matter: Acknowledgements -> Afterword -> Bibliography.

C1 ORDER   -- in each rendered book the Acknowledgements title heading precedes the
              Afterword title heading, which precedes the Bibliography title
              heading, and the Afterword comes after the last appendix (G).
              Headings are matched by line, never by substring.
C2 LEVEL   -- each matter file that opens a table-of-contents section has its first
              non-comment heading at the SAME level as the chapter titles. The level
              is derived from the chapter files, not hard-coded. (A `##` title nests
              the section under the previous appendix in any TOC.)
"""
import re
import tempfile
from pathlib import Path

import pytest

import tools.render_paper as rp
from tools.render_paper import (
    ACKNOWLEDGEMENTS,
    AFTERWORD,
    BIBLIOGRAPHY,
    BODY,
    PAPER,
    chapter_path,
)

LANGS = ("en", "zh")
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_HEADING = re.compile(r"^(#+)[ \t]+(.+?)\s*$", re.MULTILINE)


def _first_heading(path: Path):
    """(level, title line) of the first heading outside HTML comments."""
    text = _COMMENT.sub("", path.read_text(encoding="utf-8"))
    m = _HEADING.search(text)
    assert m, f"{path} has no heading outside comments"
    return len(m.group(1)), m.group(0).strip()


def _chapter_level(lang: str) -> int:
    levels = {_first_heading(chapter_path(lang, name))[0] for name in BODY}
    assert len(levels) == 1, f"{lang} chapter titles disagree on heading level: {levels}"
    return levels.pop()


@pytest.fixture(scope="module", params=LANGS)
def rendered(request):
    lang = request.param
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "book.md"
        assert rp.main(["--lang", lang, "--out", str(out)]) == 0
        return lang, out.read_text(encoding="utf-8")


def _line_index(text: str, title_line: str) -> int:
    lines = text.splitlines()
    hits = [i for i, ln in enumerate(lines) if ln.strip() == title_line]
    assert len(hits) == 1, f"heading {title_line!r} appears {len(hits)}x as a line"
    return hits[0]


def test_c1_back_matter_order(rendered):
    lang, text = rendered
    ack = _line_index(text, _first_heading(PAPER / ACKNOWLEDGEMENTS[lang])[1])
    aft = _line_index(text, _first_heading(PAPER / AFTERWORD[lang])[1])
    bib = _line_index(text, _first_heading(PAPER / BIBLIOGRAPHY[lang])[1])
    last_appendix = _line_index(text, _first_heading(chapter_path(lang, BODY[-1]))[1])
    assert last_appendix < ack < aft < bib, (
        f"{lang}: expected last appendix < acknowledgements < afterword < "
        f"bibliography, got lines {last_appendix}, {ack}, {aft}, {bib}"
    )


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("table", (ACKNOWLEDGEMENTS, AFTERWORD, BIBLIOGRAPHY),
                         ids=("acknowledgements", "afterword", "bibliography"))
def test_c2_matter_title_level_matches_chapters(lang, table):
    level, line = _first_heading(PAPER / table[lang])
    assert level == _chapter_level(lang), (
        f"{table[lang]}: title {line!r} is level {level}, chapter titles are "
        f"level {_chapter_level(lang)}"
    )
