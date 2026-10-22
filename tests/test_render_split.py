"""Per-chapter split of the paper render (`render_paper.py --split-dir`).

The site build wants one page per chapter and appendix, in both languages, from the
SAME assembler that makes the single-file release, so the site cannot drift from the
release text. These tests state the contract first:

  * the single-file outputs stay byte-identical to what the pre-split renderer made;
  * the split is on the assembler's PART boundaries, never on heading scans (Chapter 7
    has two inner H1s; zh Appendix G's H1 uses one dash where the others use two);
  * joining the pages, after undoing ONLY the documented split transforms, gives the
    single-file render back byte-for-byte;
  * every intra-book link resolves to an anchor on an existing page, every image link
    to an existing file;
  * every zh page states the translation note, except the afterword (Lei wrote it in
    Chinese), which says so instead;
  * the manifest records the pinned source commit and tag.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import tools.render_paper as rp

REPO = Path(__file__).resolve().parents[1]
BASE_SHA = "56aa5683"  # main before the split; the single-file outputs must not move
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


# ---- 1. one assembler, two outputs ----------------------------------------------

def test_single_file_is_byte_identical_to_the_pre_split_renderer(work, lang, single):
    new_out, new_stdout = single
    base_src = subprocess.run(
        ["git", "show", f"{BASE_SHA}:tools/render_paper.py"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8",
    )
    if base_src.returncode != 0:
        pytest.skip(f"base commit {BASE_SHA} not available in this clone")
    old_script = work / "render_paper_base.py"
    old_script.write_text(base_src.stdout, encoding="utf-8")
    csl = str(REPO / "tools" / "csl" / "apa.csl")
    # Same --out path for both, so the stdout `# rendered <path>` line is comparable.
    probe = work / "probe" / f"book.{lang}.md"
    old = _run(["--lang", lang, "--out", str(probe), "--csl", csl], script=old_script)
    assert old.returncode == 0, old.stderr
    old_bytes = probe.read_bytes()
    new = _run(["--lang", lang, "--out", str(probe)])
    assert new.returncode == 0, new.stderr
    assert len(old_bytes) > 100_000
    assert probe.read_bytes() == old_bytes
    assert new.stdout == old.stdout
    assert new.stderr == old.stderr
    assert new_out.read_bytes()  # the fixture's own render exists too


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
    assert set(m) == {"lang", "source_commit", "source_tag", "pages"}
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
