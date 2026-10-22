"""Per-chapter split of the paper render (`render_paper.py --split-dir`).

The site build wants one page per chapter and appendix, in both languages, from the
SAME assembler that makes the single-file release, so the site cannot drift from the
release text. These tests state the contract first:

  * the single-file outputs are the committed release files (checked by rendering in
    place and `git diff --quiet paper/release`; the one-shot proof that the refactor
    left them byte-identical to 56aa5683 is recorded in the PR body, not kept here);
  * the split is on the assembler's PART boundaries, never on heading scans (Chapter 7
    has two inner H1s; zh Appendix G's H1 uses one dash where the others use two);
  * joining the pages, after undoing ONLY the documented split transforms, gives the
    single-file render back byte-for-byte;
  * every intra-book link resolves to an anchor on an existing page, every image link
    to an existing file;
  * every zh page states the translation note, except the afterword (Lei wrote it in
    Chinese), which says so instead;
  * the manifest records the pinned source commit, tag and whether the tree was dirty.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

import tools.render_paper as rp

REPO = Path(__file__).resolve().parents[1]
LANGS = ("en", "zh")

EXPECTED_SLUGS = [
    "front-matter", "abstract",
    "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8",
    "appendix-a", "appendix-b", "appendix-c", "appendix-d",
    "appendix-e", "appendix-f", "appendix-g",
    "acknowledgements", "afterword", "bibliography",
]

SEP = "\n\n---\n\n"
ANCHOR = re.compile(r'<a id="([^"]+)"></a>')
INTRA_LINK = re.compile(r"\]\(#([^)\s]+)\)")
CROSS_LINK = re.compile(r"\]\(([a-z0-9-]+)\.html#([^)\s]+)\)")
IMAGE_LINK = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def _run(args: list[str], script: Path | None = None) -> subprocess.CompletedProcess:
    script = script or (REPO / "tools" / "render_paper.py")
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8",
    )


@pytest.fixture(scope="module")
def work(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("split")


@pytest.fixture(scope="module", params=LANGS)
def lang(request) -> str:
    return request.param


@pytest.fixture(scope="module")
def single(work, lang):
    """The single-file render with the NEW code, and its stdout."""
    out = work / "single" / f"book.{lang}.md"
    r = _run(["--lang", lang, "--out", str(out)])
    assert r.returncode == 0, r.stderr
    return out, r.stdout


@pytest.fixture(scope="module")
def split(work, lang):
    d = work / "pages"
    r = _run(["--lang", lang, "--split-dir", str(d)])
    assert r.returncode == 0, r.stderr
    return d / lang


def _pages(split_dir: Path) -> dict[str, str]:
    return {s: (split_dir / f"{s}.md").read_text(encoding="utf-8") for s in EXPECTED_SLUGS}


# ---- 2. the page set ------------------------------------------------------------

def test_slug_table_is_fixed_and_matches_body():
    assert rp.PART_SLUGS == EXPECTED_SLUGS
    assert len(rp.PART_SLUGS) == len(rp.BODY) + 4


def test_twenty_pages_in_reading_order_per_language(split):
    files = sorted(p.name for p in split.iterdir())
    assert files == sorted([f"{s}.md" for s in EXPECTED_SLUGS] + ["manifest.json"])
    manifest = json.loads((split / "manifest.json").read_text(encoding="utf-8"))
    assert [p["slug"] for p in manifest["pages"]] == EXPECTED_SLUGS
    assert [p["order"] for p in manifest["pages"]] == list(range(1, 21))


def test_slugs_identical_across_languages(work):
    seen = []
    for lg in LANGS:
        r = _run(["--lang", lg, "--split-dir", str(work / "xl")])
        assert r.returncode == 0, r.stderr
        m = json.loads((work / "xl" / lg / "manifest.json").read_text(encoding="utf-8"))
        seen.append([p["slug"] for p in m["pages"]])
    assert seen[0] == seen[1] == EXPECTED_SLUGS


def _h1s(text: str) -> list[str]:
    out, fenced = [], False
    for line in text.split("\n"):
        if re.match(r"^ {0,3}(```|~~~)", line):
            fenced = not fenced
        elif not fenced and re.match(r"^# ", line):
            out.append(line)
    return out


def test_split_is_on_part_boundaries_not_heading_scans(split, lang):
    pages = _pages(split)
    ch7 = _h1s(pages["ch7"])
    assert len(ch7) == 3, ch7  # the chapter title + "Part A" + "Part B", all on ONE page
    part_a = "# Part A — Limitations" if lang == "en" else "# A 部分 —— 局限"
    part_b = "# Part B — Implications" if lang == "en" else "# B 部分 —— 意涵"
    assert part_a in ch7 and part_b in ch7
    for slug, text in pages.items():
        if slug != "ch7":
            assert len(_h1s(text)) == 1, (slug, _h1s(text))
    if lang == "zh":
        # zh Appendix G's H1 has a single dash where the other zh H1s have a double one
        assert _h1s(pages["appendix-g"]) == ["# 附录 G — 术语表"]
        assert "# 附录 F —— " in pages["appendix-f"]


# ---- 3. the fidelity invariant --------------------------------------------------

def _undo_split_transforms(slug: str, text: str, lang: str, page_dir: Path,
                           single_dir: Path) -> str:
    # (a) the zh page note
    if lang == "zh":
        note = rp.zh_page_note(slug)
        assert text.count("\n\n" + note) == 1, f"{slug}: page note not found exactly once"
        text = text.replace("\n\n" + note, "", 1)
    # (b) cross-page link targets -> same-book fragments
    text = CROSS_LINK.sub(lambda m: f"](#{m.group(2)})", text)

    # (c) figure path prefix: relative-to-page -> relative-to-the-single-file's directory
    def fig(m: re.Match) -> str:
        target = (page_dir / m.group(1)).resolve()
        rel = os.path.relpath(target, start=single_dir.resolve())
        return m.group(0).replace(m.group(1), rel.replace(os.sep, "/"))
    return IMAGE_LINK.sub(fig, text)


def test_joined_pages_reproduce_the_single_file_byte_for_byte(split, single, lang):
    """Join-after-undo equals the single file.

    The undo accepts ANY slug in a cross-page link (`CROSS_LINK` is `[a-z0-9-]+`), so
    this test alone cannot tell a link pointed at the RIGHT page from one pointed at a
    wrong one. It discriminates only together with
    `test_every_link_resolves_to_an_anchor_on_an_existing_page`, which checks that each
    link's page owns the anchor (owner == page). Neither is a stand-alone control.

    The zh-note undo also assumes the real sources' first heading is followed by a
    blank line (`add_zh_page_note` is not injective otherwise); the undo asserts the
    note is found exactly once, so a source that broke this fails here.
    """
    book, _ = single
    pages = _pages(split)
    undone = [
        _undo_split_transforms(s, pages[s], lang, split, book.parent)
        for s in EXPECTED_SLUGS
    ]
    joined = SEP.join(p.rstrip() for p in undone) + "\n"
    expected = book.read_text(encoding="utf-8")
    assert len(expected) > 100_000
    assert joined == expected


# ---- 4. anchors and links -------------------------------------------------------

def test_every_anchor_lands_on_exactly_one_page(split):
    owner: dict[str, str] = {}
    for slug, text in _pages(split).items():
        ids = ANCHOR.findall(text)
        assert len(ids) == len(set(ids)), f"{slug}: duplicate anchor on one page"
        for i in ids:
            assert i not in owner, f"anchor {i!r} on both {owner[i]} and {slug}"
            owner[i] = slug
    assert len(owner) > 100
    assert owner["front-matter"] == "front-matter"
    assert owner["ch-5"] == "ch5" and owner["ch-6"] == "ch6"
    assert owner["appendix-E"] == "appendix-e"
    assert owner["ref-pearl1988"] == "bibliography"


def test_every_link_resolves_to_an_anchor_on_an_existing_page(split):
    pages = _pages(split)
    owner = {i: s for s, t in pages.items() for i in ANCHOR.findall(t)}
    n_same = n_cross = 0
    for slug, text in pages.items():
        for target in INTRA_LINK.findall(text):
            assert owner.get(target) == slug, (
                f"{slug}: bare link #{target} but its anchor lives on {owner.get(target)!r}")
            n_same += 1
        for page, target in CROSS_LINK.findall(text):
            assert (split / f"{page}.md").is_file(), f"{slug}: link to missing page {page}"
            assert page != slug, f"{slug}: cross-page link to itself"
            assert owner.get(target) == page, f"{slug}: #{target} is not on {page}"
            n_cross += 1
    assert n_same > 0 and n_cross > 100  # citations into the bibliography dominate


def test_citation_links_point_at_the_bibliography_page(split):
    ch1 = (split / "ch1.md").read_text(encoding="utf-8")
    assert re.search(r"\]\(bibliography\.html#ref-[a-z0-9]+\)", ch1)
    assert "](#ref-" not in ch1


def test_link_extension_is_configurable(work, lang):
    d = work / "ext-md"
    r = _run(["--lang", lang, "--split-dir", str(d), "--split-link-ext", ".md"])
    assert r.returncode == 0, r.stderr
    ch1 = (d / lang / "ch1.md").read_text(encoding="utf-8")
    assert re.search(r"\]\(bibliography\.md#ref-", ch1)
    assert ".html#" not in ch1


def test_rewrite_leaves_same_page_links_and_errors_on_a_dangling_one():
    pages = [("a", '<a id="x"></a>\n# A\n\n[to x](#x) [to y](#y)\n'),
             ("b", '<a id="y"></a>\n# B\n')]
    out = rp.rewrite_cross_page_links(pages, ".html")
    assert "[to x](#x)" in out[0] and "[to y](b.html#y)" in out[0]
    with pytest.raises(SystemExit):
        rp.rewrite_cross_page_links([("a", "[dead](#nowhere)\n")], ".html")


# ---- 5. figures and diagrams ----------------------------------------------------

def test_image_links_resolve_on_the_filesystem(split):
    n = 0
    for slug, text in _pages(split).items():
        for link in IMAGE_LINK.findall(text):
            assert "\\" not in link
            assert (split / link).resolve().is_file(), f"{slug}: {link} does not resolve"
            n += 1
    assert n == 6


def test_mermaid_diagrams_and_images_land_in_the_right_pages(split):
    pages = _pages(split)
    mermaid = {s: len(re.findall(r"^```mermaid$", t, re.M)) for s, t in pages.items()}
    assert sum(mermaid.values()) == 2
    assert mermaid["ch4"] == 2
    images = {s: len(IMAGE_LINK.findall(t)) for s, t in pages.items()}
    assert sum(images.values()) == 6
    assert images["ch1"] == 1 and images["ch6"] == 5


# ---- 6. the zh translator note --------------------------------------------------

def test_every_zh_page_but_the_afterword_states_the_translation_note(work):
    d = work / "zhnote"
    assert _run(["--lang", "zh", "--split-dir", str(d)]).returncode == 0
    for slug in EXPECTED_SLUGS:
        text = (d / "zh" / f"{slug}.md").read_text(encoding="utf-8")
        lines = text.split("\n")
        h = next(i for i, l in enumerate(lines) if re.match(r"^#{1,6}\s", l))
        note = rp.zh_page_note(slug)
        assert lines[h + 1] == "" and lines[h + 2] == note, slug
        assert note.startswith("> ") and "\n" not in note
        if slug == rp.AFTERWORD_SLUG:
            assert "Lei Shi" in note and "中文写成" in note
            for name in rp.ZH_TRANSLATORS:
                assert name not in note
        else:
            assert note == rp.ZH_TRANSLATION_NOTE
            for name in rp.ZH_TRANSLATORS:
                assert name in note


def test_afterword_exception_is_a_named_case():
    assert rp.AFTERWORD_SLUG == "afterword"
    assert rp.zh_page_note("afterword") == rp.ZH_AFTERWORD_NOTE
    assert rp.ZH_AFTERWORD_NOTE != rp.ZH_TRANSLATION_NOTE
    for slug in EXPECTED_SLUGS:
        if slug != "afterword":
            assert rp.zh_page_note(slug) == rp.ZH_TRANSLATION_NOTE


def test_english_pages_carry_no_note(work):
    d = work / "ennote"
    assert _run(["--lang", "en", "--split-dir", str(d)]).returncode == 0
    for slug in EXPECTED_SLUGS:
        lines = (d / "en" / f"{slug}.md").read_text(encoding="utf-8").split("\n")
        h = next(i for i, l in enumerate(lines) if re.match(r"^#{1,6}\s", l))
        assert not lines[h + 2].startswith(">"), slug
        assert not any(rp.ZH_TRANSLATION_NOTE in l or rp.ZH_AFTERWORD_NOTE in l for l in lines)


def test_translator_names_match_the_approved_front_matter_note():
    fm = (REPO / "paper" / "front-matter.zh.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*译文说明：\*\*.*", fm)
    assert m, "front-matter.zh.md lost its approved translation note"
    for name in rp.ZH_TRANSLATORS:
        assert name in m.group(0)
    assert "以英文版为准" in m.group(0) and "以英文版为准" in rp.ZH_TRANSLATION_NOTE
    # and the afterword exception the same note states
    assert "后记" in m.group(0) and "Lei Shi 本人以中文写成" in m.group(0)


# ---- 7. the manifest ------------------------------------------------------------

def test_manifest_records_commit_tag_and_titles(split, lang):
    m = json.loads((split / "manifest.json").read_text(encoding="utf-8"))
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                          text=True).stdout.strip()
    assert m["lang"] == lang
    assert m["source_commit"] == head and re.fullmatch(r"[0-9a-f]{40}", head)
    tag = subprocess.run(["git", "describe", "--tags", "--exact-match"], cwd=REPO,
                         capture_output=True, text=True)
    assert m["source_tag"] == (tag.stdout.strip() if tag.returncode == 0 else None)
    assert set(m) == {"lang", "source_commit", "source_tag", "dirty",
                      "renderer_commit", "renderer_dirty", "pages"}
    assert re.fullmatch(r"[0-9a-f]{40}", m["renderer_commit"])
    assert isinstance(m["renderer_dirty"], bool)
    assert isinstance(m["dirty"], bool)
    for p in m["pages"]:
        assert set(p) == {"order", "slug", "file", "title"}
        assert p["file"] == f"{p['slug']}.md"
        assert "<a" not in p["title"] and p["title"].strip() == p["title"] and p["title"]
    titles = {p["slug"]: p["title"] for p in m["pages"]}
    expected = ("Chapter 7 — Implications and Future Directions" if lang == "en"
                else "第 7 章 —— 意涵与未来方向")
    assert titles["ch7"] == expected


def test_source_provenance_tag_present_absent_and_null_is_not_refused(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}

    def git(*a):
        return subprocess.run(["git", *a], cwd=repo, env=env, check=True,
                              capture_output=True, text=True).stdout.strip()
    git("init", "-q")
    (repo / "f").write_text("1")
    git("add", "f")
    git("commit", "-q", "-m", "one")
    commit, tag = rp.source_provenance(repo)
    assert commit == git("rev-parse", "HEAD") and tag is None  # untagged: null, no refusal
    git("tag", "v1.0")
    assert rp.source_provenance(repo) == (commit, "v1.0")
    (repo / "f").write_text("2")
    git("commit", "-qam", "two")
    commit2, tag2 = rp.source_provenance(repo)
    assert commit2 != commit and tag2 is None  # HEAD past the tag is not "exactly tagged"


def _scratch_repo(tmp_path: Path):
    repo = tmp_path / "r"
    repo.mkdir()
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}

    def git(*a):
        return subprocess.run(["git", *a], cwd=repo, env=env, check=True,
                              capture_output=True, text=True).stdout.strip()
    return repo, git


def test_missing_git_binary_is_a_clean_exit_naming_git(monkeypatch, tmp_path):
    def boom(*a, **k):
        raise FileNotFoundError(2, "No such file or directory", "git")
    monkeypatch.setattr(rp.subprocess, "run", boom)
    for fn in (rp.source_provenance, rp.source_dirty):
        with pytest.raises(SystemExit) as e:
            fn(tmp_path)
        assert "git" in str(e.value) and "not found" in str(e.value).lower(), fn.__name__


def test_provenance_outside_a_git_checkout_is_refused(tmp_path, monkeypatch):
    plain = tmp_path / "not-a-repo"
    plain.mkdir()
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    with pytest.raises(SystemExit) as e:
        rp.source_provenance(plain)
    assert "cannot read the source commit" in str(e.value)


def test_split_dir_help_says_it_needs_a_git_checkout():
    r = _run(["--help"])
    assert r.returncode == 0
    flat = " ".join(r.stdout.split())
    assert "--split-dir SPLIT_DIR" in flat
    assert "must run in a git checkout" in flat


def _commit_repo(path: Path, rel: str) -> str:
    """A scratch repo at `path` with one committed file `rel`; returns HEAD."""
    path.mkdir(parents=True)
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}

    def git(*a):
        return subprocess.run(["git", *a], cwd=path, env=env, check=True,
                              capture_output=True, text=True).stdout.strip()
    git("init", "-q")
    (path / rel).parent.mkdir(parents=True, exist_ok=True)
    (path / rel).write_text(path.name)
    git("add", ".")
    git("commit", "-q", "-m", path.name)
    return git("rev-parse", "HEAD")


def _one_part_asm():
    from types import SimpleNamespace
    return SimpleNamespace(parts=[SimpleNamespace(slug="ch1", text="# Chapter 1\n\nbody\n")])


def test_renderer_provenance_comes_from_the_renderer_file_not_the_cwd(tmp_path, monkeypatch):
    content = tmp_path / "content"
    renderer = tmp_path / "renderer"
    content_head = _commit_repo(content, "paper/f")
    renderer_head = _commit_repo(renderer, "tools/render_paper.py")
    assert content_head != renderer_head
    monkeypatch.chdir(content)
    monkeypatch.setattr(rp, "__file__", str(renderer / "tools" / "render_paper.py"))
    pages = rp.write_split(_one_part_asm(), "en", tmp_path / "out", ".html")
    m = json.loads((pages / "manifest.json").read_text(encoding="utf-8"))
    assert m["source_commit"] == content_head
    assert m["renderer_commit"] == renderer_head
    assert m["renderer_dirty"] is False and m["dirty"] is False
    rfile = renderer / "tools" / "render_paper.py"
    rfile.write_text("edited")          # dirtiness is the tool's, read from its own repo
    assert rp.renderer_provenance(rfile) == (renderer_head, True)
    rfile.write_text("renderer")
    (renderer / "elsewhere").write_text("x")          # outside tools/: not dirty
    assert rp.renderer_provenance(rfile) == (renderer_head, False)


def test_renderer_outside_git_records_null_null_without_error(tmp_path, monkeypatch):
    content = tmp_path / "content"
    _commit_repo(content, "paper/f")
    loose = tmp_path / "loose" / "tools"
    loose.mkdir(parents=True)
    (loose / "render_paper.py").write_text("x")
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path / "loose"))
    assert rp.renderer_provenance(loose / "render_paper.py") == (None, None)
    monkeypatch.chdir(content)
    monkeypatch.setattr(rp, "__file__", str(loose / "render_paper.py"))
    pages = rp.write_split(_one_part_asm(), "en", tmp_path / "out", ".html")
    m = json.loads((pages / "manifest.json").read_text(encoding="utf-8"))
    assert m["renderer_commit"] is None and m["renderer_dirty"] is None
    assert re.fullmatch(r"[0-9a-f]{40}", m["source_commit"])


def test_dirty_flag_tracks_paper_and_tools_only(tmp_path):
    repo, git = _scratch_repo(tmp_path)
    git("init", "-q")
    for d in ("paper", "tools", "other"):
        (repo / d).mkdir()
        (repo / d / "f").write_text("1")
    git("add", ".")
    git("commit", "-q", "-m", "one")
    assert rp.source_dirty(repo) is False
    (repo / "other" / "f").write_text("2")          # outside paper/ and tools/
    (repo / "other" / "new").write_text("x")
    assert rp.source_dirty(repo) is False
    (repo / "paper" / "f").write_text("2")           # tracked edit
    assert rp.source_dirty(repo) is True
    git("checkout", "--", "paper/f")
    assert rp.source_dirty(repo) is False
    (repo / "tools" / "untracked").write_text("x")   # untracked counts
    assert rp.source_dirty(repo) is True


# ---- 8. residual link shapes, code exclusion, zh note placement, front-matter fence ---

# (cell id, sample, shape name the error must carry). The cells after the first three
# are the round-3 widening: each was silently kept by the round-2 regexes.
_RESIDUAL = [
    ("title-form", '[t](#x "a title")', "title-form link"),
    ("refdef", "[x]: #x", "reference definition"),
    ("href-quoted", '<a href="#x">t</a>', "raw href"),
    ("href-unquoted", "<a href=#x>t</a>", "raw href"),
    ("angle-dest", "[t](<#x>)", "angle-bracket link"),
    ("refdef-angle", "[x]: <#x>", "reference definition"),
    ("refdef-quote", "> [x]: #x", "reference definition"),
    ("refdef-quote-deep", "> > [x]: #x", "reference definition"),
    ("paren-title", "[t](#x (t))", "title-form link"),
    ("trailing-space", "[t](#x )", "title-form link"),
]
_RESIDUAL_IDS = [c[0] for c in _RESIDUAL]

# Shapes that must stay clean: the handled shape and external look-alikes.
_NOT_RESIDUAL = [
    "[t](#x)",
    "[x]: https://example.com/#frag",
    '<a href="https://example.com/#a">t</a>',
    "the href attribute is a word, and href=https://example.com/",
    '[t](https://example.com/#x "t")',
    "> quoted [t](#x) link",
]


def _pages_with(body: str):
    return [("a", '<a id="x"></a>\n# A\n\n' + body + "\n"),
            ("b", '<a id="y"></a>\n# B\n')]


@pytest.mark.parametrize("cell", _RESIDUAL, ids=_RESIDUAL_IDS)
def test_residual_link_shape_outside_code_is_a_hard_error(cell):
    _, sample, name = cell
    with pytest.raises(SystemExit) as e:
        rp.rewrite_cross_page_links(_pages_with(sample), ".html")
    msg = str(e.value)
    assert msg.startswith("a:") and name in msg


@pytest.mark.parametrize("cell", _RESIDUAL, ids=_RESIDUAL_IDS)
def test_residual_link_shape_inside_code_is_not_an_error(cell):
    _, sample, name = cell
    bodies = [f"```\n{sample}\n```"]
    if name != "reference definition":   # see the comment below: a definition starts its line
        bodies.insert(0, f"text `{sample}` more")
    for body in bodies:
        pages = _pages_with(body)
        out = rp.rewrite_cross_page_links(pages, ".html")
        assert [o.rstrip("\n") for o in out] == [t.rstrip("\n") for _, t in pages]


@pytest.mark.parametrize("sample", _NOT_RESIDUAL)
def test_non_residual_shapes_are_not_flagged(sample):
    rp.check_residual_link_shapes(_pages_with(sample))


# A reference definition cannot sit inside an inline code span (it must start its
# line), so there is no inline-span cell for it; the fenced-block cell above covers it.


def test_rewrite_skips_inline_code_and_fenced_blocks_byte_for_byte():
    a_body = ('<a id="here"></a>\n# A\n\n'
              "plain [p](#ref-x) then `[c](#ref-x)` inline\n\n"
              "```\n[f](#ref-x)\n```\n")
    pages = [("a", a_body), ("bib", '<a id="ref-x"></a>\n# Bib\n')]
    out = rp.rewrite_cross_page_links(pages, ".html")
    assert out[0] == a_body.replace("plain [p](#ref-x)", "plain [p](bib.html#ref-x)")
    assert "`[c](#ref-x)`" in out[0] and "```\n[f](#ref-x)\n```" in out[0]


def test_zh_note_after_a_heading_followed_directly_by_a_table_stays_a_separate_block():
    table = "| a | b |\n|---|---|\n| 1 | 2 |"
    out = rp.add_zh_page_note("ch1", "# T\n" + table + "\n")
    note = rp.zh_page_note("ch1")
    assert out == "# T\n\n" + note + "\n\n" + table + "\n"
    lines = out.split("\n")
    n = lines.index(note)
    assert lines[n - 1] == "" and lines[n + 1] == "" and lines[n + 2] == "| a | b |"


def test_zh_note_with_blank_line_list_paragraph_and_heading_only():
    note = rp.zh_page_note("ch1")
    assert rp.add_zh_page_note("ch1", "# T\n\nbody\n") == f"# T\n\n{note}\n\nbody\n"
    for nxt in ("- item", "para"):
        assert rp.add_zh_page_note("ch1", "# T\n" + nxt) == f"# T\n\n{note}\n\n{nxt}"
    assert rp.add_zh_page_note("ch1", "# T") == f"# T\n\n{note}"
    assert rp.zh_page_note("afterword") in rp.add_zh_page_note("afterword", "# T\nx")


def test_zh_note_undo_inverts_the_insertion_when_a_blank_follows_the_heading():
    for slug in ("ch1", "afterword"):
        src = "# T\n\nbody text\n\n| a |\n"
        out = rp.add_zh_page_note(slug, src)
        assert out.replace("\n\n" + rp.zh_page_note(slug), "", 1) == src


def test_zh_note_insertion_is_not_injective_on_a_blank_after_the_heading():
    # Documents the non-injectivity the fidelity test's undo accepts: a heading directly
    # followed by content and a heading, blank line, content give the same page.
    for slug in ("ch1", "afterword"):
        assert (rp.add_zh_page_note(slug, "# T\nX")
                == rp.add_zh_page_note(slug, "# T\n\nX"))


def test_front_matter_anchor_skips_a_part_whose_only_hash_line_is_in_a_fence():
    texts = ["```\n# not a heading\n```\n\nprose", "# Real title\n\nbody"]
    out = rp.insert_heading_anchors_in_parts(texts, {"front-matter"})
    assert "<a id=" not in out[0]
    assert out[1].startswith('<a id="front-matter"></a>\n# Real title')
