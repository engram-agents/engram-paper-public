"""Contract tests for the keyed-citation pipeline in `tools/render_paper.py`
(`paper/references.yaml` + vendored CSL style + citeproc-py), written BEFORE the
implementation.

The contract (C1-C10) is stated by the PR1 spec, not inferred:

  C1  an unknown key anywhere in a chapter is a HARD error naming file and line
  C2  `[@a; @b]` renders both works in one parenthetical, APA order, two links
  C3  narrative `@key`, year-only `[-@key]` and a locator `[@key, p. 12]` render
  C4  every `#ref-<key>` link has a matching `id="ref-<key>"` anchor (whole render)
  C5  the generated bibliography is deterministic (byte-identical across renders)
  C6  every entry's `provenance` text appears verbatim in the generated bibliography
  C7  an entry missing author/title/issued AND lacking `metadata_incomplete` is a
      hard error; with `metadata_incomplete` it renders
  C8  an entry never cited is a WARNING line listing the key, not an error
  C9  text inside inline code or fenced code blocks is not parsed as a citation
  C10 three or more authors render with "et al." in-text (APA 7)

C1-C3 and C7-C10 use small fixtures; C4-C6 run against the real repo references.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

import pytest

from tools import render_paper as rp  # noqa: E402  (imports without the renderer deps)

try:
    import citeproc  # noqa: F401
    import yaml  # noqa: F401

    _MISSING_DEPS = None
except ImportError as _e:  # pragma: no cover - only without requirements.txt installed
    _MISSING_DEPS = str(_e)


@pytest.fixture(autouse=True)
def _renderer_dependencies_installed():
    """Fail LOUDLY, never skip: a skipped citation suite would read as green while
    testing nothing. The renderer deps are pinned in requirements.txt."""
    if _MISSING_DEPS is not None:
        pytest.fail(
            f"citation tests need citeproc-py and PyYAML ({_MISSING_DEPS}); "
            f"run `pip install -r requirements.txt`"
        )


REPO = Path(__file__).resolve().parents[1]

# --- fixtures ---------------------------------------------------------------------

FIXTURE_YAML = """\
references:
- id: aaron1999
  type: book
  author:
  - {family: Aaron, given: A. B.}
  issued: {date-parts: [[1999]]}
  title: Alpha book
  publisher: Alpha Press
- id: baker2001
  type: article-journal
  author:
  - {family: Baker, given: C. D.}
  issued: {date-parts: [[2001]]}
  title: Beta article
  container-title: Journal of Beta
  volume: '3'
  issue: '2'
  page: 10-20
- id: carter2005
  type: article-journal
  author:
  - {family: Carter, given: E.}
  - {family: Dunn, given: F.}
  - {family: Evans, given: G.}
  issued: {date-parts: [[2005]]}
  title: Gamma article
  container-title: Journal of Gamma
  volume: '1'
  page: 1-9
  provenance: |-
    Gamma provenance line one
    gamma provenance line two.
  metadata_incomplete: no issue number printed
- id: kahl2026a
  type: article
  author:
  - {family: Kahl, given: P.}
  issued: {date-parts: [[2026]]}
  title: First Kahl paper
- id: kahl2026b
  type: article
  author:
  - {family: Kahl, given: P.}
  issued: {date-parts: [[2026]]}
  title: Second Kahl paper
"""


def _ctx(yaml_text: str = FIXTURE_YAML, tmp_path: Path | None = None, lang: str = "en"):
    assert tmp_path is not None
    p = tmp_path / "references.yaml"
    p.write_text(yaml_text, encoding="utf-8")
    entries = rp.load_references(p)
    return rp.CitationContext(entries, rp.DEFAULT_CSL, lang=lang)


def _links(text: str) -> list[str]:
    return re.findall(r"\]\(#ref-([a-z0-9]+)\)", text)


def _make_tree(tmp_path: Path, chapter: str, refs: str = FIXTURE_YAML) -> None:
    """A minimal render tree under tmp_path (the renderer resolves paths relative
    to the working directory)."""
    (tmp_path / "paper").mkdir()
    (tmp_path / "paper" / "front-matter.md").write_text("# Title\n", encoding="utf-8")
    (tmp_path / "paper" / "acknowledgements.md").write_text("Thanks.\n", encoding="utf-8")
    (tmp_path / "paper" / "bibliography.md").write_text(
        "# Bibliography\n\nIntro paragraph.\n\n{{REFERENCES}}\n\n---\n\n## Data availability\n\nNone.\n",
        encoding="utf-8",
    )
    (tmp_path / "paper" / "references.yaml").write_text(refs, encoding="utf-8")
    d = tmp_path / "paper_research" / "current_draft"
    d.mkdir(parents=True)
    (d / "ch1.md").write_text(chapter, encoding="utf-8")


@pytest.fixture
def tree(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(rp, "BODY", ["ch1.md"])
    monkeypatch.setattr(rp, "INSERTS_BY_LANG", {"en": [], "zh": []})
    return tmp_path


def _render(tree: Path, chapter: str, refs: str = FIXTURE_YAML, extra=()):
    _make_tree(tree, chapter, refs)
    out = tree / "out.md"
    rc = rp.main(["--out", str(out), *extra])
    return rc, out.read_text(encoding="utf-8")


# --- C1 ---------------------------------------------------------------------------

def test_c1_unknown_key_is_hard_error_naming_file_and_line(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve("line one\nline two [@nosuchkey] here\n", "paper_research/current_draft/ch1.md")
    msg = str(e.value)
    assert "paper_research/current_draft/ch1.md:2" in msg
    assert "nosuchkey" in msg


def test_c1_unknown_narrative_key_is_hard_error(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve("a\nb\nAs @ghost2000 argues.\n", "ch2.md")
    assert "ch2.md:3" in str(e.value) and "ghost2000" in str(e.value)


def test_c1_unknown_key_in_one_group_member_fails_whole_group(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve("see [@aaron1999; @ghost2000]\n", "ch1.md")
    assert "ch1.md:1" in str(e.value)


def test_c1_end_to_end_exit_is_nonzero(tree):
    _make_tree(tree, "ok\n\nbad [@nope1999]\n")
    with pytest.raises(SystemExit) as e:
        rp.main(["--out", str(tree / "out.md")])
    assert e.value.code not in (0, None)
    assert "ch1.md:3" in str(e.value)
    assert not (tree / "out.md").exists(), "a failed render must not leave an output file"


def test_c1_malformed_group_is_hard_error_not_silent_skip(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve("x [@aaron1999 p. 3 and more] y\n", "ch1.md")
    assert "ch1.md:1" in str(e.value)


# --- C2 ---------------------------------------------------------------------------

def test_c2_group_renders_both_works_in_one_parenthetical_apa_order(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    expected = "([Aaron, 1999](#ref-aaron1999); [Baker, 2001](#ref-baker2001))"
    assert ctx.resolve("x [@aaron1999; @baker2001] y\n", "ch1.md") == f"x {expected} y\n"
    # source order reversed: APA order (alphabetical), not citation order
    assert ctx.resolve("x [@baker2001; @aaron1999] y\n", "ch1.md") == f"x {expected} y\n"


def test_c2_same_author_same_year_group_keeps_suffixes_and_two_links(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    out = ctx.resolve("[@kahl2026b; @kahl2026a]\n", "ch1.md")
    assert out == "([Kahl, 2026a](#ref-kahl2026a), [2026b](#ref-kahl2026b))\n"


def test_c2_year_suffix_comes_from_the_key_in_text_and_bibliography(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    assert ctx.resolve("[@kahl2026a]", "ch1.md") == "([Kahl, 2026a](#ref-kahl2026a))"
    bib = ctx.bibliography_markdown("en")
    assert re.search(r'ref-kahl2026b"></a>Kahl, P\. \(2026b\)\.', bib)


def test_c2_ambiguous_in_text_citations_are_a_hard_error(tmp_path):
    """Two works with the same author and year and no distinguishing suffix would
    print identical in-text citations; that must fail loudly, not link wrongly."""
    both_plain = FIXTURE_YAML.replace("id: kahl2026a", "id: kahl2026").replace(
        "id: kahl2026b", "id: kahl2026x"
    )
    # kahl2026 vs kahl2026x: suffix "x" disambiguates -> fine
    _ctx(both_plain, tmp_path)
    clash = FIXTURE_YAML.replace("id: kahl2026a", "id: kahl2026").replace("id: kahl2026b", "id: kahl2026")
    with pytest.raises(SystemExit) as e:
        _ctx(clash, tmp_path)
    assert "kahl2026" in str(e.value)


# --- C3 ---------------------------------------------------------------------------

def test_c3_narrative_year_only_and_locator(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    assert ctx.resolve("@aaron1999 argues.\n", "ch1.md") == "[Aaron (1999)](#ref-aaron1999) argues.\n"
    assert ctx.resolve("Aaron [-@aaron1999] argues.\n", "ch1.md") == "Aaron ([1999](#ref-aaron1999)) argues.\n"
    assert ctx.resolve("[@aaron1999, p. 12]\n", "ch1.md") == "([Aaron, 1999, p. 12](#ref-aaron1999))\n"


def test_c3_locator_forms_survive_verbatim(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    for loc in ("p. 12", "pp. 12–18", "ch. 4", "§ 2.3"):
        out = ctx.resolve(f"[@baker2001, {loc}]\n", "ch1.md")
        assert f"Baker, 2001, {loc}](#ref-baker2001)" in out, out


def test_c3_narrative_sentence_end_punctuation_is_not_part_of_the_key(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    assert ctx.resolve("so says @aaron1999.\n", "ch1.md") == "so says [Aaron (1999)](#ref-aaron1999).\n"


def test_c3_two_author_narrative_uses_and(tmp_path):
    y = FIXTURE_YAML.replace(
        "  - {family: Baker, given: C. D.}\n",
        "  - {family: Baker, given: C. D.}\n  - {family: Young, given: Z.}\n",
    )
    ctx = _ctx(y, tmp_path)
    assert ctx.resolve("@baker2001 said\n", "ch1.md") == "[Baker and Young (2001)](#ref-baker2001) said\n"
    assert ctx.resolve("[@baker2001]\n", "ch1.md") == "([Baker & Young, 2001](#ref-baker2001))\n"


# --- C4 / C5 / C6 (real repo references) -----------------------------------------

@pytest.fixture(scope="module")
def real_entries():
    return rp.load_references(REPO / "paper" / "references.yaml")


def _all_keys_text(entries) -> str:
    lines = []
    for e in entries:
        k = e["id"]
        lines += [f"[@{k}]", f"@{k} said", f"[-@{k}]", f"[@{k}, p. 3]"]
    lines.append("[" + "; ".join("@" + e["id"] for e in entries) + "]")
    return "\n\n".join(lines) + "\n"


def test_c4_every_link_has_an_anchor_in_the_generated_bibliography(real_entries):
    ctx = rp.CitationContext(real_entries, rp.DEFAULT_CSL, lang="en")
    body = ctx.resolve(_all_keys_text(real_entries), "synthetic.md")
    bib = ctx.bibliography_markdown("en")
    links = set(_links(body))
    anchors = set(re.findall(r'<a id="ref-([a-z0-9]+)"></a>', bib))
    assert links, "vacuous: synthetic text produced no links"
    assert links == {e["id"] for e in real_entries}, "every key must be linkable"
    assert links <= anchors
    assert anchors == {e["id"] for e in real_entries}


def test_c4_whole_real_render_links_all_anchored_en_and_zh(tmp_path, monkeypatch):
    monkeypatch.chdir(REPO)
    for lang in ("en", "zh"):
        out = tmp_path / f"{lang}.md"
        assert rp.main(["--lang", lang, "--out", str(out)]) == 0
        text = out.read_text(encoding="utf-8")
        anchors = set(re.findall(r'<a id="ref-([a-z0-9]+)"></a>', text))
        assert anchors, f"{lang} render carries no bibliography anchors"
        assert set(_links(text)) <= anchors


def test_c5_generated_bibliography_is_deterministic(real_entries):
    a = rp.CitationContext(real_entries, rp.DEFAULT_CSL, lang="en").bibliography_markdown("en")
    b = rp.CitationContext(real_entries, rp.DEFAULT_CSL, lang="en").bibliography_markdown("en")
    assert a == b and len(a) > 1000
    za = rp.CitationContext(real_entries, rp.DEFAULT_CSL, lang="zh").bibliography_markdown("zh")
    zb = rp.CitationContext(real_entries, rp.DEFAULT_CSL, lang="zh").bibliography_markdown("zh")
    assert za == zb


def test_c5_two_full_renders_are_byte_identical(tmp_path, monkeypatch):
    monkeypatch.chdir(REPO)
    one, two = tmp_path / "1.md", tmp_path / "2.md"
    rp.main(["--out", str(one)])
    rp.main(["--out", str(two)])
    assert one.read_bytes() == two.read_bytes() and one.stat().st_size > 1000


def test_c5_render_is_identical_across_processes_with_different_hash_seeds(tmp_path):
    """Two renders in ONE process share a hash seed, so they cannot expose an order that
    depends on str hashing (set/dict iteration). Separate processes with different
    PYTHONHASHSEED values can."""
    import os
    import subprocess

    outs = []
    for seed in ("1", "2"):
        out = tmp_path / f"seed{seed}.md"
        r = subprocess.run(
            [sys.executable, "tools/render_paper.py", "--out", str(out)],
            cwd=REPO, env={**os.environ, "PYTHONHASHSEED": seed}, capture_output=True, text=True,
        )
        assert r.returncode == 0, r.stderr
        outs.append(out.read_bytes())
    assert outs[0] == outs[1] and len(outs[0]) > 1000


UNCITED_ORDER_YAML = "references:\n" + "".join(
    f"- id: {k}\n  type: book\n  author:\n  - {{family: {f}, given: A.}}\n"
    f"  issued: {{date-parts: [[{y}]]}}\n  title: Book {f}\n  publisher: P\n"
    for k, f, y in (
        ("zeta2001", "Zeta", 2001), ("alpha2002", "Alpha", 2002), ("mu2003", "Mu", 2003),
        ("omega2004", "Omega", 2004), ("beta2005", "Beta", 2005), ("kappa2006", "Kappa", 2006),
    )
)

_UNCITED_SCRIPT = """\
import sys
from pathlib import Path
from tools import render_paper as rp
entries = rp.load_references(Path(sys.argv[1]))
ctx = rp.CitationContext(entries, rp.DEFAULT_CSL, lang="en")
ctx.resolve("Only [@mu2003] is cited.", "x.md")
print(", ".join(ctx.uncited()))
"""


def test_c5_uncited_key_order_is_stable_across_hash_seeds(tmp_path):
    """The WARNING line lists uncited keys; their order must not depend on str hashing.
    Uses a fixture with deliberately uncited entries, NOT the real paper (whose citation
    state decides whether any key is uncited at all). The warning text itself is built
    inline in main() from this list with a plain join, so the list is what is covered."""
    import os
    import subprocess

    refs = tmp_path / "references.yaml"
    refs.write_text(UNCITED_ORDER_YAML, encoding="utf-8")
    results = []
    for seed in ("0", "1", "2", "3", "4"):
        r = subprocess.run(
            [sys.executable, "-c", _UNCITED_SCRIPT, str(refs)],
            cwd=REPO, env={**os.environ, "PYTHONHASHSEED": seed, "PYTHONPATH": str(REPO)},
            capture_output=True, text=True,
        )
        assert r.returncode == 0, r.stderr
        results.append(r.stdout.strip())
    keys = results[0].split(", ")
    assert len(keys) >= 4 and "mu2003" not in keys, results[0]
    assert all(r == results[0] for r in results), results


def test_c6_every_provenance_text_appears_verbatim(real_entries):
    en = rp.CitationContext(real_entries, rp.DEFAULT_CSL, lang="en").bibliography_markdown("en")
    zh = rp.CitationContext(real_entries, rp.DEFAULT_CSL, lang="zh").bibliography_markdown("zh")
    with_prov = [e for e in real_entries if e.get("provenance")]
    assert len(with_prov) >= 15, "the real references must carry their provenance notes"
    for e in real_entries:
        if e.get("provenance"):
            assert e["provenance"] in en, e["id"]
            assert (e.get("provenance_zh") or e["provenance"]) in zh, e["id"]
        if e.get("metadata_incomplete"):
            assert "*[" + e["metadata_incomplete"] + "]*" in en, e["id"]
            assert "*[" + (e.get("metadata_incomplete_zh") or e["metadata_incomplete"]) + "]*" in zh, e["id"]


def test_c6_provenance_is_verbatim_for_fixture_and_precedes_the_note(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    bib = ctx.bibliography_markdown("en")
    assert "Gamma provenance line one\ngamma provenance line two." in bib
    assert bib.index("Gamma provenance line one") < bib.index("*[no issue number printed]*")


def test_same_author_same_year_entries_list_in_suffix_order_not_title_order(tmp_path):
    """citeproc-py breaks author+year ties by title; the suffix is the key's, so the
    printed order must follow it (2026a before 2026b) even when the titles say otherwise."""
    y = FIXTURE_YAML.replace("title: First Kahl paper", "title: Zeta paper").replace(
        "title: Second Kahl paper", "title: Alpha paper"
    )
    bib = _ctx(y, tmp_path).bibliography_markdown("en")
    assert bib.index("ref-kahl2026a") < bib.index("ref-kahl2026b")
    assert bib.index("Zeta paper") < bib.index("Alpha paper")


def test_bibliography_is_sorted_apa_order_and_anchored_per_entry(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    bib = ctx.bibliography_markdown("en")
    keys = re.findall(r'<a id="ref-([a-z0-9]+)"></a>', bib)
    assert keys == ["aaron1999", "baker2001", "carter2005", "kahl2026a", "kahl2026b"]


# --- C7 ---------------------------------------------------------------------------

@pytest.mark.parametrize("missing", ["author", "title", "issued"])
def test_c7_missing_core_field_without_metadata_incomplete_is_hard_error(tmp_path, missing):
    entry = {
        "author": "  author:\n  - {family: Zed, given: Z.}\n",
        "title": "  title: Zed work\n",
        "issued": "  issued: {date-parts: [[2000]]}\n",
    }
    body = "".join(v for k, v in entry.items() if k != missing)
    y = "references:\n- id: zed2000\n  type: book\n" + body
    p = tmp_path / "r.yaml"
    p.write_text(y, encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        rp.load_references(p)
    assert "zed2000" in str(e.value) and missing in str(e.value)


@pytest.mark.parametrize("missing", ["author", "title", "issued"])
def test_c7_with_metadata_incomplete_the_entry_renders(tmp_path, missing):
    entry = {
        "author": "  author:\n  - {family: Zed, given: Z.}\n",
        "title": "  title: Zed work\n",
        "issued": "  issued: {date-parts: [[2000]]}\n",
    }
    body = "".join(v for k, v in entry.items() if k != missing)
    y = "references:\n- id: zed2000\n  type: book\n" + body + "  metadata_incomplete: the source prints no " + missing + "\n"
    ctx = _ctx(y, tmp_path)
    bib = ctx.bibliography_markdown("en")
    assert 'id="ref-zed2000"' in bib
    assert f"*[the source prints no {missing}]*" in bib


def test_c7_unknown_field_and_duplicate_id_are_hard_errors(tmp_path):
    p = tmp_path / "r.yaml"
    p.write_text(FIXTURE_YAML.replace("title: Alpha book", "title: Alpha book\n  colour: red"), encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        rp.load_references(p)
    assert "colour" in str(e.value)
    p.write_text(FIXTURE_YAML.replace("id: baker2001", "id: aaron1999"), encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        rp.load_references(p)
    assert "aaron1999" in str(e.value)


# --- C8 ---------------------------------------------------------------------------

def test_c8_uncited_entry_is_a_warning_line_not_an_error(tree, capsys):
    rc, out = _render(tree, "Only [@aaron1999] is cited here.\n")
    assert rc == 0
    err = capsys.readouterr().err
    warn = [l for l in err.splitlines() if l.startswith("WARNING")]
    assert len(warn) == 1, err
    for k in ("baker2001", "carter2005", "kahl2026a", "kahl2026b"):
        assert k in warn[0]
    assert "aaron1999" not in warn[0]
    # the uncited entries are still printed in the bibliography
    assert 'id="ref-baker2001"' in out


def test_c8_no_warning_when_everything_is_cited(tree, capsys):
    rc, _ = _render(tree, "[@aaron1999; @baker2001; @carter2005; @kahl2026a; @kahl2026b]\n")
    assert rc == 0
    assert "WARNING" not in capsys.readouterr().err


# --- C9 ---------------------------------------------------------------------------

def test_c9_inline_code_and_fenced_blocks_are_not_citations(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    text = (
        "Write `[@ghost1999]` or ``@ghost2000 and [@x]`` to cite.\n\n"
        "```python\n@decorator\nx = [@ghost1999]\n```\n\n"
        "~~~\n[@ghost2001]\n~~~\n\n"
        "````md\n```\n[@ghost2002]\n```\n````\n"
    )
    assert ctx.resolve(text, "ch1.md") == text
    assert ctx.cited == set()


def test_c9_code_is_skipped_but_real_citations_around_it_still_resolve(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    out = ctx.resolve("`[@ghost1999]` then [@aaron1999] and\n\n```\n[@ghost1999]\n```\n", "ch1.md")
    assert "`[@ghost1999]`" in out and "([Aaron, 1999](#ref-aaron1999))" in out
    assert ctx.cited == {"aaron1999"}


def test_c9_escaped_and_email_at_signs_are_not_citations(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    text = r"literal \@ghost1999 and \[@ghost1999] and mail me@example.com and https://x.org/@ghost1999" + "\n"
    assert ctx.resolve(text, "ch1.md") == text


def test_c9_html_comments_are_not_citations(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    text = "<!-- translator note: [@ghost1999]\nand @ghost2000 -->\nbody\n"
    assert ctx.resolve(text, "ch1.md") == text


def test_c9_line_numbers_count_lines_inside_comments_and_code(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    text = "<!-- a\nb\nc -->\n```\nx\n```\n[@ghost1999]\n"
    with pytest.raises(SystemExit) as e:
        ctx.resolve(text, "ch1.md")
    assert "ch1.md:7" in str(e.value)


# --- C10 --------------------------------------------------------------------------

def test_c10_three_or_more_authors_render_et_al(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    assert ctx.resolve("[@carter2005]\n", "ch1.md") == "([Carter et al., 2005](#ref-carter2005))\n"
    assert ctx.resolve("@carter2005 found\n", "ch1.md") == "[Carter et al. (2005)](#ref-carter2005) found\n"


def test_c10_twelve_authors_in_the_real_references_render_et_al(real_entries):
    ctx = rp.CitationContext(real_entries, rp.DEFAULT_CSL, lang="en")
    assert ctx.resolve("[@wu2026]", "x.md") == "([Wu et al., 2026](#ref-wu2026))"
    assert ctx.resolve("[@alchourron1985]", "x.md") == "([Alchourrón et al., 1985](#ref-alchourron1985))"


# --- dependency / options / template ------------------------------------------------

def test_missing_citeproc_prints_a_clear_error_naming_the_package(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "citeproc", None)  # makes `import citeproc` raise ImportError
    p = tmp_path / "r.yaml"
    p.write_text(FIXTURE_YAML, encoding="utf-8")
    entries = rp.load_references(p)
    with pytest.raises(SystemExit) as e:
        rp.CitationContext(entries, rp.DEFAULT_CSL)
    assert "citeproc-py" in str(e.value)


def test_csl_option_selects_the_style_file_and_a_missing_one_is_an_error(tree, tmp_path):
    custom = tree / "mystyle.csl"
    shutil.copy(rp.DEFAULT_CSL, custom)
    rc, out = _render(tree, "[@aaron1999]\n", extra=("--csl", str(custom)))
    assert rc == 0 and "([Aaron, 1999](#ref-aaron1999))" in out
    with pytest.raises(SystemExit) as e:
        rp.main(["--out", str(tree / "o2.md"), "--csl", str(tree / "nope.csl")])
    assert "nope.csl" in str(e.value)


def test_template_without_the_references_token_is_a_hard_error(tree):
    _make_tree(tree, "text\n")
    (tree / "paper" / "bibliography.md").write_text("# Bibliography\n\nno token here\n", encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        rp.main(["--out", str(tree / "out.md")])
    assert "{{REFERENCES}}" in str(e.value)


def test_render_places_generated_entries_where_the_token_was(tree):
    rc, out = _render(tree, "text\n")
    assert rc == 0
    assert "{{REFERENCES}}" not in out
    i_intro, i_entry, i_tail = out.index("Intro paragraph."), out.index('<a id="ref-aaron1999">'), out.index("## Data availability")
    assert i_intro < i_entry < i_tail


# =====================================================================================
# Round 2 (PR #124 review round 1). Contract tests, written BEFORE the fixes.
#
#  B1  the order of works inside ONE in-text group equals the bibliography's order,
#      on every path that orders cited works (one shared ordering, not two)
#  S1  an inline code span cannot cross a block boundary (blank line, heading, list item)
#  S2  Pandoc prefix/suffix: [see @k], [see @k, p. 3], [@a, p. 3; also @b]; unsupported
#      shapes are hard errors naming file:line, never a silent mis-render
#  S3  [@k](url) is a hard error; _@k_ / *@k* render as an emphasised narrative citation
#  S4  tools/csl/README.md records the provenance of the vendored apa.csl
#  S5  the repo README documents how to cite in chapters
#  N1  APA 7 capitalises role labels in the reference list: (Ed.) (Eds.) (Trans.)
#  N2  {{REFERENCES}} sits on its own line in both bibliography templates
# =====================================================================================

# Titles sort OPPOSITE to suffix order: citeproc-py breaks author+year ties by title.
FLIPPED_YAML = FIXTURE_YAML.replace("title: First Kahl paper", "title: Zeta paper").replace(
    "title: Second Kahl paper", "title: Alpha paper"
)

KAHL_AB = "([Kahl, 2026a](#ref-kahl2026a), [2026b](#ref-kahl2026b))"


def _plain(s: str) -> str:
    """Link labels without the link targets: what a reader of the rendered paper sees."""
    return re.sub(r"\[([^\]]*)\]\(#ref-[a-z0-9]+\)", r"\1", s)


# --- B1 ---------------------------------------------------------------------------

def test_b1_in_text_same_author_group_follows_suffix_order_when_titles_sort_opposite(tmp_path):
    ctx = _ctx(FLIPPED_YAML, tmp_path)
    assert ctx.resolve("[@kahl2026a; @kahl2026b]", "ch1.md") == KAHL_AB
    assert ctx.resolve("[@kahl2026b; @kahl2026a]", "ch1.md") == KAHL_AB
    bib = ctx.bibliography_markdown("en")
    assert bib.index("ref-kahl2026a") < bib.index("ref-kahl2026b")


def test_b1_real_kahl_triple_prints_2026a_2026b_2026c_with_three_links(real_entries):
    ctx = rp.CitationContext(real_entries, rp.DEFAULT_CSL, lang="en")
    want = ("([Kahl, 2026a](#ref-kahl2026a), [2026b](#ref-kahl2026b), "
            "[2026c](#ref-kahl2026c))")
    assert ctx.resolve("[@kahl2026a; @kahl2026b; @kahl2026c]", "x.md") == want
    assert ctx.resolve("[@kahl2026c; @kahl2026b; @kahl2026a]", "x.md") == want
    assert _links(want) == ["kahl2026a", "kahl2026b", "kahl2026c"]


def test_b1_mixed_author_group_is_in_bibliography_order(tmp_path):
    ctx = _ctx(FLIPPED_YAML, tmp_path)
    out = ctx.resolve("[@kahl2026b; @baker2001; @kahl2026a; @aaron1999]", "ch1.md")
    assert _links(out) == ["aaron1999", "baker2001", "kahl2026a", "kahl2026b"]
    assert _plain(out) == "(Aaron, 1999; Baker, 2001; Kahl, 2026a, 2026b)"


def test_b1_group_with_locators_and_year_only_items_keeps_bibliography_order(tmp_path):
    ctx = _ctx(FLIPPED_YAML, tmp_path)
    out = ctx.resolve("[@kahl2026b, p. 4; @kahl2026a, p. 3]", "ch1.md")
    assert _links(out) == ["kahl2026a", "kahl2026b"]
    assert _plain(out) == "(Kahl, 2026a, p. 3, 2026b, p. 4)"
    out = ctx.resolve("[-@kahl2026b; @kahl2026a]", "ch1.md")
    assert _links(out) == ["kahl2026a", "kahl2026b"]
    # a year-only item suppresses its author, so it is its own `;` segment (as before)
    assert _plain(out) == "(Kahl, 2026a; 2026b)"


def _bib_order(ctx) -> list[str]:
    return re.findall(r'<a id="ref-([a-z0-9]+)"></a>', ctx.bibliography_markdown("en"))


def test_b1_order_is_the_bibliography_s_even_where_key_order_disagrees(tmp_path):
    """A key is an id, not a sort key: an entry keyed `zzz1999` whose author is Aaron is
    listed FIRST. In-text order must follow the bibliography, not the key strings."""
    y = FIXTURE_YAML.replace("id: aaron1999", "id: zzz1999").replace("id: baker2001", "id: aaa2001")
    ctx = _ctx(y, tmp_path)
    assert _bib_order(ctx)[:2] == ["zzz1999", "aaa2001"]
    out = ctx.resolve("[@aaa2001; @zzz1999]", "ch1.md")
    assert _links(out) == ["zzz1999", "aaa2001"]
    assert _plain(out) == "(Aaron, 1999; Baker, 2001)"


def test_b1_every_pair_and_the_whole_set_of_real_entries_follow_bibliography_order(real_entries):
    """The property, over the real references: for ANY group, in-text link order equals
    the bibliography's order, whatever order the author typed. Covers same-author,
    same-author-same-year and mixed-author groups, with and without locators."""
    ctx = rp.CitationContext(real_entries, rp.DEFAULT_CSL, lang="en")
    order = _bib_order(ctx)
    assert len(order) == len(real_entries) >= 20
    keys = list(reversed(order))
    whole = ctx.resolve("[" + "; ".join("@" + k for k in keys) + "]", "x.md")
    assert _links(whole) == order
    located = ctx.resolve("[" + "; ".join(f"@{k}, p. 1" for k in keys) + "]", "x.md")
    assert _links(located) == order
    for i, a in enumerate(order):
        for b in order[i + 1:]:
            assert _links(ctx.resolve(f"[@{b}; @{a}]", "x.md")) == [a, b], (a, b)
            assert _links(ctx.resolve(f"[@{b}, p. 2; @{a}, p. 1]", "x.md")) == [a, b], (a, b)


# --- S1 ---------------------------------------------------------------------------

def test_s1_stray_backtick_does_not_swallow_citations_in_later_paragraphs(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    text = "one stray ` backtick here\n\nsee [@aaron1999] now\n\nanother stray ` one\n"
    out = ctx.resolve(text, "ch1.md")
    assert "([Aaron, 1999](#ref-aaron1999))" in out
    assert ctx.cited == {"aaron1999"}


def test_s1_stray_backtick_in_a_heading_or_list_item_does_not_reach_the_next_block(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    out = ctx.resolve("- item with a stray ` tick\n- cites [@aaron1999] ok ` end\n", "ch1.md")
    assert "([Aaron, 1999](#ref-aaron1999))" in out
    ctx = _ctx(tmp_path=tmp_path)
    out = ctx.resolve("## heading with ` tick\n[@baker2001] text ` end\n", "ch1.md")
    assert "([Baker, 2001](#ref-baker2001))" in out


def test_s1_a_real_code_span_may_still_wrap_one_line_break(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    text = "code `[@ghost1999]\nstill code` and `[@ghost2000]` done\n"
    assert ctx.resolve(text, "ch1.md") == text


# S1 (round 3): the boundary set is exactly what interrupts a paragraph in CommonMark, so a
# multi-line code span that crosses a line CommonMark does NOT treat as a block start is a
# real code span, and a citation-shaped string inside it stays literal.

@pytest.mark.parametrize("middle", ["2. see [@aaron1999]", "| see [@aaron1999]", "10) see [@aaron1999]"])
def test_s1_code_span_crosses_lines_that_do_not_interrupt_a_paragraph(tmp_path, middle):
    ctx = _ctx(tmp_path=tmp_path)
    text = f"syntax `[@ghost1999]\n{middle}\nand more` done\n"
    assert ctx.resolve(text, "ch1.md") == text
    assert ctx.cited == set()


@pytest.mark.parametrize(
    "middle",
    ["- see [@aaron1999] x", "+ see [@aaron1999] x", "* see [@aaron1999] x", "1. see [@aaron1999] x",
     "1) see [@aaron1999] x", "> see [@aaron1999] x", "## see [@aaron1999] x", "---", "", ],
)
def test_s1_lines_that_do_interrupt_a_paragraph_still_end_a_code_span(tmp_path, middle):
    ctx = _ctx(tmp_path=tmp_path)
    text = f"stray ` tick\n{middle}\nand [@baker2001] more ` end\n"
    out = ctx.resolve(text, "ch1.md")
    assert "([Baker, 2001](#ref-baker2001))" in out


# --- S2 ---------------------------------------------------------------------------

def test_s2_prefix_and_suffix_render_inside_the_parentheses(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    assert ctx.resolve("[see @aaron1999]", "c.md") == "(see [Aaron, 1999](#ref-aaron1999))"
    assert ctx.resolve("[see @aaron1999, p. 3]", "c.md") == "(see [Aaron, 1999, p. 3](#ref-aaron1999))"
    out = ctx.resolve("[@aaron1999, p. 3; also @baker2001]", "c.md")
    assert out == "([Aaron, 1999, p. 3](#ref-aaron1999); also [Baker, 2001](#ref-baker2001))"
    assert _plain(out) == "(Aaron, 1999, p. 3; also Baker, 2001)"
    assert ctx.resolve("[see -@aaron1999]", "c.md") == "(see [1999](#ref-aaron1999))"
    assert ctx.resolve("[see also @aaron1999; @baker2001]", "c.md") == (
        "(see also [Aaron, 1999](#ref-aaron1999); [Baker, 2001](#ref-baker2001))")


def test_s2_prefixed_item_does_not_merge_into_the_same_author_run(tmp_path):
    ctx = _ctx(FLIPPED_YAML, tmp_path)
    out = ctx.resolve("[@kahl2026a; also @kahl2026b]", "c.md")
    assert _plain(out) == "(Kahl, 2026a; also Kahl, 2026b)"
    assert _links(out) == ["kahl2026a", "kahl2026b"]


@pytest.mark.parametrize("bad", [
    "[see @aaron1999 p. 3]",            # suffix without a comma
    "[see @aaron1999; and more text]",  # a part with no key
    "[@aaron1999, p. [3]]",             # nested brackets
    "[see @ghost1999]",                 # unknown key, with a prefix
    "[@aaron1999",                      # unclosed group
])
def test_s2_unsupported_forms_are_hard_errors_naming_file_and_line(tmp_path, bad):
    ctx = _ctx(tmp_path=tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve(f"fine line\n{bad} tail\n", "paper_research/current_draft/ch9.md")
    assert "paper_research/current_draft/ch9.md:2" in str(e.value)


# --- S3 ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad", ["[@aaron1999](http://example.org)", "[@aaron1999][ref]",
                                 "[see @aaron1999](http://example.org)"])
def test_s3_a_citation_followed_by_a_link_target_is_a_hard_error(tmp_path, bad):
    ctx = _ctx(tmp_path=tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve(f"one\n{bad}\n", "ch1.md")
    msg = str(e.value)
    assert "ch1.md:2" in msg and "link label" in msg


def test_s3_adjacent_citation_groups_are_not_mistaken_for_a_link(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    out = ctx.resolve("[@aaron1999][-@baker2001]", "ch1.md")
    assert out == "([Aaron, 1999](#ref-aaron1999))([2001](#ref-baker2001))"


@pytest.mark.parametrize("mark", ["_", "*", "**", "__"])
def test_s3_narrative_citation_inside_emphasis_is_an_emphasised_narrative_citation(tmp_path, mark):
    ctx = _ctx(tmp_path=tmp_path)
    out = ctx.resolve(f"as {mark}@aaron1999{mark} says\n", "ch1.md")
    assert out == f"as {mark}[Aaron (1999)](#ref-aaron1999){mark} says\n"


def test_s3_underscores_hanging_off_a_word_are_not_emphasis(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    text = "an identifier snake_@aaron1999 and my_name__@aaron1999 stay as written\n"
    assert ctx.resolve(text, "ch1.md") == text


def test_s3_emphasised_unknown_key_is_still_a_hard_error(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve("x\n_@ghost1999_\n", "ch1.md")
    assert "ch1.md:2" in str(e.value) and "ghost1999" in str(e.value)


# --- S4 / S5 / N2 (files) -----------------------------------------------------------

def test_s4_csl_readme_records_apa_csl_provenance_and_the_file_hash():
    import hashlib

    readme = (REPO / "tools" / "csl" / "README.md").read_text(encoding="utf-8")
    for needle in ("apa.csl", "2026-10-07", "https://", "citation-style-language/styles",
                   "Creative Commons Attribution-ShareAlike 3.0", "<updated>", "unmodified"):
        assert needle in readme, needle
    digest = hashlib.sha256((REPO / "tools" / "csl" / "apa.csl").read_bytes()).hexdigest()
    assert digest in readme, "README must pin the sha256 of the vendored file (a silent edit shows)"


def test_s5_readme_documents_citing_in_chapters():
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert "## Citing in chapters" in readme
    sect = readme.split("## Citing in chapters", 1)[1].split("\n## ", 1)[0]
    for needle in ("[@key]", "[@key, p. 12]", "[@a; @b]", "[see @key", "[-@key]", "paper/references.yaml",
                   "pip install -r requirements.txt", "unknown key", "never from memory"):
        assert needle in sect, needle


@pytest.mark.parametrize("name", ["bibliography.md", "bibliography.zh.md"])
def test_n2_references_token_is_on_its_own_line_in_the_templates(name):
    lines = (REPO / "paper" / name).read_text(encoding="utf-8").split("\n")
    assert lines.count(rp.REFERENCES_TOKEN) == 1
    assert not any(rp.REFERENCES_TOKEN in l and l.strip() != rp.REFERENCES_TOKEN for l in lines)


# --- N1 ---------------------------------------------------------------------------

ROLES_YAML = """\
references:
- id: doyle1979
  type: chapter
  author: [{family: Doyle, given: J.}]
  editor: [{family: Ginsberg, given: M. L.}]
  issued: {date-parts: [[1987]]}
  title: A truth maintenance system
  container-title: Readings in nonmonotonic reasoning
  page: 259-279
  publisher: Morgan Kaufmann
- id: pair2001
  type: chapter
  author: [{family: Pair, given: A.}]
  editor: [{family: One, given: B.}, {family: Two, given: C.}]
  issued: {date-parts: [[2001]]}
  title: Two editors
  container-title: A collection
  page: 1-9
  publisher: P
- id: ricoeur1992
  type: book
  author: [{family: Ricoeur, given: P.}]
  translator: [{family: Blamey, given: K.}]
  issued: {date-parts: [[1992]]}
  title: Oneself as another
  publisher: University of Chicago Press
- id: stiegler1998
  type: book
  author: [{family: Stiegler, given: B.}]
  translator: [{family: Beardsworth, given: R.}, {family: Collins, given: G.}]
  issued: {date-parts: [[1998]]}
  title: Technics and time
  publisher: Stanford University Press
"""


def test_n1_reference_list_capitalises_role_labels_like_apa_7(tmp_path):
    bib = _ctx(ROLES_YAML, tmp_path).bibliography_markdown("en")
    assert "In M. L. Ginsberg (Ed.)," in bib
    assert "In B. One & C. Two (Eds.)," in bib
    assert "(K. Blamey, Trans.)" in bib
    assert "(R. Beardsworth & G. Collins, Trans.)" in bib
    assert not re.search(r"\((?:[^()]*, )?(?:eds?|trans)\.\)", bib), bib


def test_n1_real_references_have_no_lower_case_role_labels_in_either_language(real_entries):
    for lang in ("en", "zh"):
        bib = rp.CitationContext(real_entries, rp.DEFAULT_CSL, lang=lang).bibliography_markdown(lang)
        assert "(Ed.)" in bib and "(K. Blamey, Trans.)" in bib
        assert not re.search(r"\((?:[^()]*, )?(?:eds?|trans)\.\)", bib)


def test_n1_provenance_text_is_not_touched_by_the_label_fix(tmp_path):
    y = ROLES_YAML.replace("  publisher: P\n", "  publisher: P\n  provenance: kept as written (ed.) and (trans.) here\n")
    ctx = _ctx(y, tmp_path)
    assert "kept as written (ed.) and (trans.) here" in ctx.bibliography_markdown("en")


# --- reference-definition label (round 3) ---------------------------------------------

@pytest.mark.parametrize("line", ["[@aaron1999]: http://example.com", "   [@aaron1999]: http://example.com",
                                   "[-@aaron1999]: http://example.com", "[see @aaron1999]: http://example.com"])
def test_a_citation_as_a_reference_definition_label_is_a_hard_error(tmp_path, line):
    ctx = _ctx(tmp_path=tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve(f"text\n\n{line}\n", "ch1.md")
    msg = str(e.value)
    assert msg.startswith("ch1.md:3:") and "reference-definition label" in msg


def test_a_citation_followed_by_a_colon_mid_line_or_in_code_is_not_a_definition(tmp_path):
    ctx = _ctx(tmp_path=tmp_path)
    out = ctx.resolve("as shown [@aaron1999]: and so on\n\n    x\n\n`[@ghost1999]: y`\n", "ch1.md")
    assert "([Aaron, 1999](#ref-aaron1999)): and so on" in out


# --- malformed-shape class guard (review of #124: a key-shaped `@` never renders as text) ---

FIXTURE_YAML_TV = FIXTURE_YAML + """\
- id: tulving1985
  type: article-journal
  author:
  - {family: Tulving, given: E.}
  issued: {date-parts: [[1985]]}
  title: Memory and consciousness
  container-title: Canadian Psychology
- id: semon1904
  type: book
  author:
  - {family: Semon, given: R.}
  issued: {date-parts: [[1904]]}
  title: Die Mneme
  publisher: Engelmann
"""


def _ctx_tv(tmp_path, lang="en"):
    return _ctx(FIXTURE_YAML_TV, tmp_path, lang=lang)


@pytest.mark.parametrize("src", [
    "[@tulving1985 @semon1904]",
    "[@tulving1985, @semon1904]",
    "[see @tulving1985 @semon1904]",
    "[see @tulving1985, also @semon1904]",
])
def test_r2_two_keys_in_one_item_is_a_hard_error_with_hint(tmp_path, src):
    ctx = _ctx_tv(tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve(f"first line\n\nA claim {src} here.\n", "ch1.md")
    msg = str(e.value)
    assert msg.startswith("ch1.md:3:") and "separate citations with ';'" in msg


def test_r2_the_semicolon_form_still_renders(tmp_path):
    ctx = _ctx_tv(tmp_path)
    out = ctx.resolve("[@tulving1985; @semon1904]", "ch1.md")
    assert _links(out) == ["semon1904", "tulving1985"] and "@" not in out


@pytest.mark.parametrize("src,expected", [
    ("如@tulving1985所述。", "如{N}所述。"),
    ("见@tulving1985，", "见{N}，"),
    ("（@tulving1985）", "（{N}）"),
    ("あ@tulving1985い", "あ{N}い"),
    ("한@tulving1985글", "한{N}글"),
    ("如@tulving1985。", "如{N}。"),
])
def test_r3_cjk_adjacent_narrative_citation_renders_without_inserting_spaces(tmp_path, src, expected):
    ctx = _ctx_tv(tmp_path)
    narrative = ctx.resolve("@tulving1985", "ch1.md")
    assert narrative.startswith("[Tulving (1985)]")
    assert ctx.resolve(src, "ch1.md") == expected.replace("{N}", narrative)


def test_r3_cjk_adjacent_equals_the_spaced_form_minus_the_spaces(tmp_path):
    ctx = _ctx_tv(tmp_path)
    spaced = ctx.resolve("如 @tulving1985 所述", "ch1.md")
    assert ctx.resolve("如@tulving1985所述", "ch1.md") == spaced.replace("如 ", "如").replace(" 所述", "所述")


def test_r3_cjk_adjacent_unknown_key_is_still_an_unknown_key_error(tmp_path):
    ctx = _ctx_tv(tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve("如@ghost1999所述", "ch1.md")
    assert "unknown citation key '@ghost1999'" in str(e.value)


@pytest.mark.parametrize("src", ["foo@tulving1985", "see foo@tulving1985 here", "é@tulving1985", "x1@tulving1985"])
def test_r3_latin_word_char_before_at_is_an_error_not_a_citation(tmp_path, src):
    ctx = _ctx_tv(tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve(src + "\n", "ch1.md")
    assert "@tulving1985" in str(e.value) and "ch1.md:1:" in str(e.value)


@pytest.mark.parametrize("src", ["@{tulving1985}", "[@{tulving1985}]", "as in @{tulving1985}.", "-@{tulving1985}"])
def test_r4_braced_pandoc_form_is_a_hard_error_naming_the_unbraced_form(tmp_path, src):
    ctx = _ctx_tv(tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve(f"line one\n{src}\n", "ch1.md")
    msg = str(e.value)
    assert msg.startswith("ch1.md:2:") and "tulving1985" in msg and "braced" in msg


@pytest.mark.parametrize("src", ["[@tulving1985 @semon1904]", "@{tulving1985}", "foo@tulving1985", "-@tulving1985x1",
                                  "word -@tulving1985 tail", "x[@a1999 junk @tulving1985]"])
def test_r1_sweep_no_key_shaped_token_survives_into_the_output(tmp_path, src):
    """Whatever the shape, resolve() either raises or leaves no unprotected key-shaped
    `@` token behind."""
    ctx = _ctx_tv(tmp_path)
    try:
        out = ctx.resolve(src + "\n", "ch1.md")
    except SystemExit:
        return
    assert not re.search(r"@\{?[a-z]+\d{4}[a-z]?", out), out


def test_r1_sweep_catches_a_shape_nobody_enumerated(tmp_path):
    ctx = _ctx_tv(tmp_path)
    for src in ("a-@tulving1985", "k=@tulving1985", "x:@tulving1985", "a.@tulving1985"):
        with pytest.raises(SystemExit) as e:
            ctx.resolve(f"p\n\n{src}\n", "ch1.md")
        assert "ch1.md:3:" in str(e.value) and "@tulving1985" in str(e.value), src


@pytest.mark.parametrize("text", [
    "mail me@example.com or me@smith2020.com now\n",
    "see https://x.org/@tulving1985 and http://medium.com/@user2020\n",
    "`engram_stats @ turn 82` and engram_stats @ turn 82 again\n",
    "escaped \\@tulving1985 and \\[@tulving1985] text\n",
    "```\n@tulving1985 {@x} @{tulving1985}\n```\n`@{tulving1985} foo@tulving1985`\n",
    "<!-- @tulving1985 @{tulving1985} -->\n",
    "an @ sign, a lone @, and @ turn 82 stay text\n",
])
def test_r1_sweep_does_not_fire_on_non_citation_at_signs(tmp_path, text):
    ctx = _ctx_tv(tmp_path)
    assert ctx.resolve(text, "ch1.md") == text


def test_r1_error_message_names_file_line_and_token(tmp_path):
    ctx = _ctx_tv(tmp_path)
    with pytest.raises(SystemExit) as e:
        ctx.resolve("a\nb\nfoo@semon1904 bar\n", "chX.md")
    assert str(e.value).startswith("chX.md:3:") and "'@semon1904'" in str(e.value)


def test_r1_end_to_end_malformed_shape_exits_nonzero(tree):
    with pytest.raises(SystemExit) as e:
        _render(tree, "Text [@aaron1999 @baker2001].\n")
    assert e.value.code not in (0, None)
