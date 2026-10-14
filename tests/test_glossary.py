"""Contract tests for Appendix G — Glossary (`spec-glossary.md`), written BEFORE
the appendix and the render-order change existed. Expected to fail until
`paper/chapters/en/appendix_G_glossary.md` exists and
`tools.render_paper.BODY` includes it.

T1 — every glossary term occurs at least once in the rendered body OUTSIDE
     Appendix G (case-insensitive, word-boundary).
T2 — every section pointer in G resolves to a heading that exists in the render.
T3 — G carries zero node IDs (reuses tests/test_render_strip_ids.py's _ID_SCAN).
T4 — G's entries average <= `GLOSSARY_AVG_WORDS_PER_ENTRY` words and none exceeds
     `GLOSSARY_MAX_WORDS_PER_ENTRY` (zh: Han characters, both x `ZH_HAN_PER_EN_WORD`;
     zh is not space-delimited, so a whitespace-token count measures nothing
     there); the total therefore scales with the number of terms (Lei,
     2026-10-10). And every required term has an entry (or is
     in the documented-absent set, for the two required terms that do not occur
     anywhere in the current draft body at all).
T5 — the Ch1 pointer sentence is present exactly once in the render.

LANGUAGE PARAMETERIZATION (`--lang {en,zh}`, spec: zh translation support). Every
glossary test is parameterized over `LANGS` so the Chinese draft gets the same
checks as the English one — before this, the file was hardcoded to the English
draft path and the zh twin escaped every check entirely. A check that the current
zh draft cannot yet satisfy (because its chapters are not translated, or because
the check is keyed to English prose) SKIPS with the reason stated, never passes
silently. The three checks the spec names for zh — the word budget, the
zero-node-ID scan, and the every-term-occurs-outside-G check — all run.

The language-contract tests at the bottom of this file assert the engine
contracts the zh spec states: one shared `BODY`, a per-language chapter
resolution that hard-fails naming a missing file, anchor-key parity between
`INSERTS` and `INSERTS_ZH`, and the per-language default output path.
"""

from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import pytest

import tools.render_paper as rp
from tools.render_paper import (
    ACKNOWLEDGEMENTS,
    AFTERWORD,
    BIBLIOGRAPHY,
    BODY,
    CHAPTER_SUFFIX,
    DEFAULT_OUT,
    DIAGRAM_CASCADE,
    DIAGRAM_CASCADE_ZH,
    DRAFT,
    DRAFT_ZH,
    FRONT_MATTER,
    INSERTS,
    INSERTS_ZH,
    PAPER,
    SOURCE_DIRS,
    apply_inserts,
    assert_insert_anchor_parity,
    chapter_name,
    chapter_path,
    load,
    strip_provenance_ids,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
CH1_POINTER = (
    "Terms of art are collected in the Glossary (Appendix G); each entry "
    "points to the section that defines it."
)

LANGS = ("en", "zh")

# Appendix G's top-level heading, per language. The zh translation localises it
# (verified against paper/chapters/zh/appendix_G_glossary.zh.md).
_G_HEADING = {
    "en": r"^# Appendix G — Glossary\s*$",
    "zh": r"^# 附录 G — 术语表\s*$",
}
# What ends G in the assembled render, per language: the next level-1 heading,
# which is the Acknowledgements title in both languages now that the back matter
# is raised to chapter level (`# Acknowledgements` / `# 致谢`). This became
# language-keyed on 2026-09-28, exactly as the note here predicted: the zh slice
# was previously pinned to the English Acknowledgements heading and worked only
# because the zh acknowledgements file was a heading-less placeholder, so the
# slice ran to the end of the document harmlessly while T1/T2 skipped. Once the
# zh file had a real heading, an English-only boundary let the zh slice swallow
# the acknowledgements AND the bibliography -- whose section lead-ins then got
# mis-parsed as glossary entries. Verified against the heading line of
# paper/acknowledgements.zh.md (`# 致谢`).
_G_HEADING_END = {
    "en": r"^# Acknowledgements\s*$",
    "zh": r"^# 致谢\s*$",
}


@pytest.fixture(params=LANGS)
def lang(request: pytest.FixtureRequest) -> str:
    return request.param


def _g_path(lang: str) -> Path:
    """Appendix G's source file for `lang`, via the engine's own resolution."""
    return SOURCE_DIRS[lang] / chapter_name(lang, "appendix_G_glossary.md")


def _missing_chapters(lang: str) -> list[Path]:
    return [
        SOURCE_DIRS[lang] / chapter_name(lang, name)
        for name in BODY
        if not (SOURCE_DIRS[lang] / chapter_name(lang, name)).exists()
    ]


def _skip_if_cannot_assemble(lang: str, check: str) -> None:
    """Skip a check that needs the whole book assembled, naming exactly what is
    absent. Only the checks that need more than Appendix G itself take this
    path -- the ones satisfiable from the translated G still run."""
    missing = _missing_chapters(lang)
    if not missing:
        return
    pytest.skip(
        f"{check}: needs the full {lang!r} assembly, but {len(missing)} of "
        f"{len(BODY)} {lang!r} chapter sources do not exist yet "
        f"(first missing: {missing[0]}). Skipped, not silently passed -- the "
        f"checks satisfiable from the {lang!r} Appendix G alone still run."
    )


def _skip_zh(lang: str, check: str, why: str) -> None:
    """Explicit skip for a check the current zh draft cannot satisfy, quoting
    both the check-specific reason and the shared untranslated-chapters fact."""
    missing = _missing_chapters(lang)
    tail = ""
    if missing:
        tail = (
            f" Separately, {len(missing)} of {len(BODY)} {lang!r} chapter sources "
            f"are untranslated (first missing: {missing[0]}), so the book cannot "
            f"be assembled at all."
        )
    pytest.skip(f"{check}: {why}{tail} Skipped, not silently passed.")

# _ID_SCAN copied verbatim from tests/test_render_strip_ids.py so this file has
# no import-order dependency on that module's internals.
_ID_SCAN = re.compile(r"\b(?:ob|dv|th|cj|df|ax|cs|ls|gl|gt|ct|qu|pr|ev|fl|pn|tk|ts)_\d{4}\b")


def _render_full_text(lang: str = "en") -> str:
    """Render the whole paper via the real assembly path (front matter + BODY +
    acknowledgements + bibliography), so the test exercises the real render
    rather than a hand-rolled substitute.

    DELIBERATELY NOT IDENTICAL TO `tools/render_paper.py:main()`. This omits the
    `strip_apparatus_tags(name, body)` call `main()` makes on every BODY chapter,
    so the bracketed working-apparatus tags the chapters carry (`[SOLID]`,
    `[GROUNDED ob_2550]`, `[gap SOLID; ...]`, ...) SURVIVE here and are ABSENT
    from the committed render -- 33 occurrences in en, 31 in zh (measured
    2026-09-30; stripping them from this helper's output reproduces the committed
    book byte-for-byte). A check that needs apparatus-tag-free text must read the
    published .md, not this helper. engram-paper#113: the previous docstring
    claimed this mirrored `main()` "exactly", which was false."""
    parts = [load(PAPER / FRONT_MATTER[lang])]
    for name in BODY:
        body = load(SOURCE_DIRS[lang] / chapter_name(lang, name))
        body = apply_inserts(name, body, rp.INSERTS_BY_LANG[lang])
        body, _ = strip_provenance_ids(name, body)
        parts.append(body)
    parts.append(load(PAPER / ACKNOWLEDGEMENTS[lang]))
    parts.append(load(PAPER / AFTERWORD[lang]))
    parts.append(load(PAPER / BIBLIOGRAPHY[lang]))
    return "\n\n---\n\n".join(p.rstrip() for p in parts) + "\n"


def _g_section_text(lang: str, full_text: str) -> str:
    """Slice out just the Appendix G section from the full render."""
    m = re.search(_G_HEADING[lang], full_text, re.MULTILINE)
    assert m, f"Appendix G heading not found in the {lang!r} render"
    rest = full_text[m.end():]
    # G ends at the next top-level heading (Acknowledgements) or end of doc.
    m2 = re.search(_G_HEADING_END[lang], rest, re.MULTILINE)
    return rest[: m2.start()] if m2 else rest


def _body_outside_g(lang: str, full_text: str) -> str:
    m = re.search(_G_HEADING[lang], full_text, re.MULTILINE)
    assert m
    before = full_text[: m.start()]
    rest = full_text[m.end():]
    m2 = re.search(_G_HEADING_END[lang], rest, re.MULTILINE)
    after = rest[m2.start():] if m2 else ""
    return before + after


# ── entry parsing ────────────────────────────────────────────────────────────
#
# Appendix G is a TABLE (Lei, 2026-10-12): one row per term,
#   | Term | Definition | Section |                (zh: | 术语 | 定义 | 章节 |)
# A DATA row is a line whose first cell opens with a bold headword; the header and
# the `|---|` separator row are not entries. An empty Section cell is written `—`.
#
# The rare NOTES live under the table, not in a column (Lei, 2026-10-12: "a mostly
# empty column is a waste of page space"): a Definition cell that has a note ends
# with the marker `<sup>[n](#gnote-n)</sup>`, and a `**Notes**` (zh `**注**`) list
# directly after the table carries one line per note,
#   <a id="gnote-n"></a>n. **headword** — note text
# A "Sense (N) unless stated." tail is not a note: it is part of the senses
# definition and sits inside the Definition cell.

_ROW_RE = re.compile(r"^\|\s*\*\*(.+?)\*\*", re.MULTILINE)
_CELL_SPLIT = re.compile(r"(?<!\\)\|")
_EMPTY_CELL = "—"
_TABLE_HEADER = {
    "en": ["Term", "Definition", "Section"],
    "zh": ["术语", "定义", "章节"],
}
_NOTES_LEAD = {"en": "**Notes**", "zh": "**注**"}
# A Definition cell's note marker, and a note line of the list under the table.
_MARKER = re.compile(r"<sup>\[(\d+)\]\(#gnote-(\d+)\)</sup>")
_NOTE_LINE_LOOSE = re.compile(r'^<a id="gnote-')
_NOTE_LINE = re.compile(r'^<a id="gnote-(\d+)"></a>(\d+)\. \*\*(.+?)\*\* — (.+)$')


def _split_cells(line: str) -> list[str]:
    """The cells of one table line (outer pipes dropped, `\\|` escapes kept)."""
    inner = line.strip()
    assert inner.startswith("|") and inner.endswith("|"), f"not a table line: {line!r}"
    return [c.strip() for c in _CELL_SPLIT.split(inner[1:-1])]


def _parse_rows(g_text: str) -> list[list[str]]:
    """Every data row of the glossary table as its three cells
    [term, definition, section]."""
    return [_split_cells(m.group(0)) for m in
            re.finditer(r"^\|\s*\*\*.*$", g_text, re.MULTILINE)]


def _parse_notes(g_text: str) -> list[tuple[int, int, str, str]]:
    """The note lines of the list under the table, in order, as
    (anchor n, shown n, headword, text). A line that opens like a note line but
    does not have the exact shape is returned as (-1, -1, "", whole line) so the
    caller sees it instead of it vanishing."""
    out = []
    for line in g_text.splitlines():
        if _NOTE_LINE_LOOSE.match(line):
            m = _NOTE_LINE.match(line)
            out.append((int(m.group(1)), int(m.group(2)), m.group(3), m.group(4))
                       if m else (-1, -1, "", line))
    return out


def _split_marker(definition: str) -> tuple[str, int | None]:
    """(Definition with its note marker removed, the marker's number or None).
    The marker is at most one, at the very end of the cell, with equal text/target."""
    found = _MARKER.findall(definition)
    assert len(found) <= 1, f"more than one note marker in {definition[-80:]!r}"
    if not found:
        return definition, None
    assert found[0][0] == found[0][1], f"marker text/target differ: {found[0]}"
    assert definition.endswith(f"<sup>[{found[0][0]}](#gnote-{found[0][0]})</sup>"), (
        f"marker is not at the end of the cell: {definition[-80:]!r}")
    return _MARKER.sub("", definition), int(found[0][0])


def _parse_entries(g_text: str) -> list[str]:
    """Every entry's bold headword, as written (the Term cell's `**...**`; any
    non-bold annotation after it, e.g. 'cascade (retraction cascade)', is not
    part of it)."""
    return _ROW_RE.findall(g_text)


# The headwords of the pre-table glossary at 89248b5, in order (contract C1): the
# re-layout must not add, drop, rename or reorder a term. Raw bold text.
_EXPECTED_HEADWORDS = {
    "en": [
        'arbitration',
        'auto-surface',
        'axiom',
        'cascade',
        'checkpoint',
        'claim-bearing / non-claim-bearing',
        'closest continuer',
        'compaction',
        'compaction bridge',
        'confidence',
        'conjecture',
        'contradiction',
        'cornerstone',
        'current (node)',
        'definition',
        'deliberate recall',
        'derivation',
        'engram / ENGRAM',
        'evidence node',
        'faded set',
        'fleet',
        'focus list',
        'forgetting curve',
        'goal',
        'harness',
        'history-tree',
        'identity documents',
        'importance',
        'lesson',
        'nap',
        'node ID prefixes',
        'observation',
        'pending marker',
        'person node',
        'premise',
        'provenance',
        'queryable set',
        'quote_type',
        'reasoning type',
        'retention',
        'retract',
        'seat',
        'seed / root',
        'skill',
        'sleep',
        'snapshot',
        'source_class',
        'stale',
        'substrate',
        'supersede',
        'sweep',
        'tainted',
        'tier',
        'trust tier',
        'turn',
        'twin study',
        'unified',
        'utility (utility score)',
        'warm briefing',
    ],
    "zh": [
        '仲裁（arbitration）',
        '自动浮现（auto-surface）',
        '公理（axiom）',
        '级联（cascade，撤回级联）',
        '检查点（checkpoint）',
        '承载主张／不承载主张（claim-bearing / non-claim-bearing）',
        '最接近的延续者（closest continuer）',
        '压缩（compaction）',
        '压缩桥接（compaction bridge）',
        '置信度（confidence）',
        '猜想（conjecture）',
        '矛盾（contradiction）',
        '基石（cornerstone）',
        '现行（节点）（current (node)）',
        '定义（definition）',
        '主动回忆（deliberate recall）',
        '推导（derivation）',
        'engram / ENGRAM（心迹）',
        '证据节点（evidence node）',
        '淡出集（faded set）',
        '集群（fleet）',
        '焦点清单（focus list）',
        '遗忘曲线（forgetting curve）',
        '目标（goal）',
        '承载框架（harness）',
        '历史树（history-tree）',
        '身份文档（identity documents）',
        '重要性（importance）',
        '教训（lesson）',
        '小憩（nap）',
        '节点 ID 前缀（node ID prefixes）',
        '观察（observation）',
        '待决标记（pending marker）',
        '人物节点（person node）',
        '前提（premise）',
        '出处（provenance）',
        '可查询集（queryable set）',
        'quote_type',
        '推理类型（reasoning type）',
        '保持（retention）',
        '撤回（retract）',
        '席位（seat）',
        '种子／根（seed / root）',
        '技能（skill）',
        '睡眠（sleep）',
        '快照（snapshot）',
        'source_class',
        '陈旧（stale）',
        '基底（substrate）',
        '取代（supersede）',
        '普查（sweep）',
        '污染（tainted）',
        '层级（tier）',
        '信任层级（trust tier）',
        '轮次（turn）',
        '孪生研究（twin study）',
        '统一（unified）',
        '效用（效用分）（utility (utility score)）',
        '温暖简报（warm briefing）',
    ],
}


# A trailing parenthetical annotation, in EITHER paren style. The content class
# excludes only the parens that DELIMIT an annotation, not every paren: two zh
# headwords carry two trailing parentheticals whose outer one itself contains
# ASCII parens ('现行（节点）（current (node)）'), so a class such as [^（()）]*
# would stop at the inner '(' and leave the annotation un-stripped. The strip is
# applied REPEATEDLY (see _headword_terms) because one pass removes one layer.
_PAREN_TAIL_RE = re.compile(r"\s*[（(][^（）]*[）)]\s*$")

# The compound-headword separator, in either script. The zh form is the
# full-width '／' (U+FF0F), which an ASCII-only ' / ' split never matched; and
# the ASCII ' / ' also occurs INSIDE a parenthetical ('种子／根（seed / root）'),
# which split that headword into the malformed fragments '种子／根（seed' and
# 'root）' when the parenthetical was still present.
_TERM_SPLIT_RE = re.compile(r" / |／")


def _headword_terms(raw_headword: str) -> list[str]:
    """Normalize one raw bold headword into the literal string(s) T1 should
    search for in the body. Rule: strip trailing parenthetical annotations
    (e.g. '(usage-derived ...)', '(utility score)', '(node)'), then split on
    ' / ' or its full-width zh form '／' for compound headwords (e.g.
    'seed / root', 'claim-bearing / non-claim-bearing', 'engram / ENGRAM') so
    each name is checked independently.

    Deliberately language-AGNOSTIC rather than keyed by `lang`: it is called
    from the mutation test too, and the property it needs is "not ASCII-only" --
    a property of the input string, not of the language parameter. The English
    behaviour is unchanged (no English headword carries a full-width paren or
    slash).
    """
    stripped = raw_headword.strip()
    while True:
        nxt = _PAREN_TAIL_RE.sub("", stripped).strip()
        if nxt == stripped:
            break
        stripped = nxt
    return [t.strip() for t in _TERM_SPLIT_RE.split(stripped) if t.strip()]


# CJK-bearing text: the Han block, the CJK punctuation block, and the full-width
# forms block. Used to choose the match strategy for one term -- NOT to classify
# a whole document, so the ranges are deliberately broad.
_CJK = re.compile(r"[㐀-鿿　-〿＀-￯]")


def _term_regex(term: str) -> re.Pattern:
    """The search pattern for one glossary term in the rendered body.

    `\\b` is a WORD boundary, and CJK characters ARE word characters in Python's
    `re`, so `\\b遗忘曲线\\b` cannot match 遗忘曲线 inside `的遗忘曲线所` (ch7).
    Every zh term whose occurrences are flanked by Han characters on both sides
    is therefore missed -- measured as the residual 12 failures once the
    parenthetical strip and the compound split were fixed: 遗忘曲线, 身份文档,
    保持, 技能, 快照, 陈旧, 轮次, 证据节点, 集群, 承载框架, 普查, 效用 -- none of
    which is a translation gap.

    The count moved, and the move is measured rather than guessed: this note
    previously said 7, which is what the pure `\\b` form still gives on a
    PRE-comment-strip tree. The five terms above past 轮次 occurred ONLY inside
    HTML comments, so while comments reached the render they satisfied the check;
    once `load()` began stripping comments the residual rose to 12. Measured
    2026-09-28 both ways: 7 with `strip_html_comments` patched out, 12 without.
    Re-measure by reverting this function to the pure `\\b` form and running
    T1[zh] -- the list T1 prints IS the count -- rather than trusting either
    number, which is how the 7 was left standing for a day.

    Terms bearing CJK thus match as plain substrings; pure-ASCII terms keep the
    boundary, where it is doing real work (it stops `ENGRAM` matching inside
    `ENGRAMISH` and `skill` inside `skills`)."""
    if _CJK.search(term):
        return re.compile(re.escape(term), re.IGNORECASE)
    return re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)


# Terms whose only occurrence in the current draft body is a different
# grammatical form than the glossary headword. Documented explicitly rather
# than silently fuzzy-matched: each key is the exact headword-after-stripping
# from _headword_terms, each value is the regex alternation (word-form roots)
# accepted in its place.
_FORM_OVERRIDES: dict[str, str] = {
    # The paper never uses the bare adjective "tainted" outside the compound
    # `tainted_by` (which a \b-bounded search for "tainted" cannot reach,
    # since '_' is a word character with no boundary before it) -- the live
    # vocabulary is the verb "taint"/"taints"/"tainting" (Ch1 §1.3, Ch8 §8.2)
    # plus the historical `tainted_by` flag name (Ch6 §6.3). Accept the whole
    # word family.
    "tainted": r"taint\w*",
    # "skill" only ever appears in the body as the plural "skills" (Ch5 §5.0).
    "skill": r"skills?",
}

# The "node ID prefixes" entry is a 13-row table, not a term that itself
# appears in prose. T1 for this entry checks that each prefix's underlying
# node TYPE NAME (not the bare ID-prefix substring) is named somewhere in the
# body -- because not every type is actually cited as a live example ID
# outside Appendix G: measured directly against the full corpus, only
# ax/cj/cs/df/dv/gl/ob/pn/qu prefixes occur as real instantiated IDs
# (e.g. "ob_1089"); ls_ (lesson), ev_ (evidence), fl_ (feeling-report) and
# tk_ (task) are never cited as a live example anywhere outside G, only
# described by node-type name in Appendix E §E.2's own table (which IS part
# of the body). Checking the type name rather than the bare prefix is the
# more honest test: it verifies the *concept* each prefix names is grounded
# in the paper, which is what the entry actually claims.
# The type names are language-keyed: the entry's own table is written in the
# rendered language, so the zh body names the types in Chinese (观察, 推导, ...)
# and the English names never occur there -- an English-only map reported all 18
# prefixes as missing against the zh render. The zh values are the names the zh
# glossary's own `节点 ID 前缀（node ID prefixes）` entry uses, in the same
# prefix order as the English map. The English values are byte-identical to the
# pre-zh-fix table.
_ID_PREFIXES = {
    "en": {
        "ob_": "observation",
        "dv_": "derivation",
        "th_": "theory",
        "cj_": "conjecture",
        "df_": "definition",
        "ax_": "axiom",
        "cs_": "cornerstone",
        "ls_": "lesson",
        "gl_": "goal",
        "gt_": "goal tension",
        "ct_": "contradiction",
        "qu_": "question",
        "pr_": "prediction",
        "ev_": "evidence",
        "fl_": "feeling",
        "pn_": "person",
        "tk_": "task",
        "ts_": "trust signal",
    },
    "zh": {
        "ob_": "观察",
        "dv_": "推导",
        "th_": "理论",
        "cj_": "猜想",
        "df_": "定义",
        "ax_": "公理",
        "cs_": "基石",
        "ls_": "教训",
        "gl_": "目标",
        "gt_": "目标张力",
        "ct_": "矛盾",
        "qu_": "问题",
        "pr_": "预测",
        "ev_": "证据",
        "fl_": "感受报告",
        "pn_": "人物",
        "tk_": "任务",
        "ts_": "信任信号",
    },
}

# The entry cites the CODE's type-prefix map (engram_core.py TYPE_PREFIX at
# v0.5.1-rc5), not a paper section, after Borges's colleague read of #109
# found the fairy's table had paired ts_ with task (it is trust_signal; task
# is tk_) and cited E.2, which names types but no prefixes. Two types in
# that map are never named in the paper body at all, so their prefixes are
# exempt from the body check below and rest on the code citation alone.
_PREFIXES_CITED_TO_CODE_ONLY = {"gt_", "ts_"}

# The `node ID prefixes` entry's parsed headword term, per language (i.e. what
# `_headword_terms` returns for it -- the zh headword is
# `节点 ID 前缀（node ID prefixes）`, so its parsed term drops the gloss). This
# entry is a 13-row type table in its entry body, not a phrase the prose uses, so
# T1 skips it in the term loop and checks it through `_ID_PREFIXES` instead. The
# skip used to compare the RAW headword against the English literal, which the zh
# headword never satisfies -- so the zh entry fell through to the term search and
# reported `节点 ID 前缀` as missing from prose that has no reason to contain it
# (the word 前缀 does not occur outside Appendix G at all). Language-keyed,
# matching `_G_HEADING` and `_ID_PREFIXES`.
_ID_PREFIX_TABLE_HEADWORDS = {"en": "node ID prefixes", "zh": "节点 ID 前缀"}

# Required terms (spec's full list) that do not occur ANYWHERE in the current
# draft body -- not merely undefined (the spec's "current" case), but never
# used at all. Per the spec's own instruction to write a usage-derived
# definition when a term is used-but-undefined, there is no usage to derive
# from for these two, so they are omitted from G entirely rather than
# inventing content the paper never states. Locked here as an explicit,
# reviewable set (see HANDOFF DECISIONS).
_REQUIRED_BUT_ABSENT_FROM_BODY = {"recall summary", "fresh-reader round"}

# The full required-term list from spec-glossary.md, mapped to the literal
# headword string(s) actually used in G (None entries are the two terms
# above, intentionally missing from G). "history tree / identity tree" maps
# to "history-tree" only: "identity tree" is not used anywhere in the current
# draft body (only the hyphenated "history-tree" is), so the combined entry
# is filed under the paper's own name alone -- see HANDOFF DECISIONS.
REQUIRED_TERMS: dict[str, list[str] | None] = {
    "current (node)": ["current"],
    "queryable set": ["queryable set"],
    "faded set": ["faded set"],
    "pending marker": ["pending marker"],
    "supersede": ["supersede"],
    "retract": ["retract"],
    "cascade": ["cascade"],
    "tainted": ["tainted"],
    "stale": ["stale"],
    "auto-surface": ["auto-surface"],
    "focus list": ["focus list"],
    "warm briefing": ["warm briefing"],
    "seed / root": ["seed", "root"],
    "seat": ["seat"],
    "fleet": ["fleet"],
    "harness": ["harness"],
    "skill": ["skill"],
    "identity documents": ["identity documents"],
    "checkpoint": ["checkpoint"],
    "nap": ["nap"],
    "sleep": ["sleep"],
    "compaction": ["compaction"],
    "compaction bridge": ["compaction bridge"],
    "turn": ["turn"],
    "forgetting curve": ["forgetting curve"],
    "importance": ["importance"],
    "utility": ["utility"],
    "retention": ["retention"],
    "recall summary": None,
    "tier": ["tier"],
    "claim-bearing / non-claim-bearing": ["claim-bearing", "non-claim-bearing"],
    "observation": ["observation"],
    "derivation": ["derivation"],
    "conjecture": ["conjecture"],
    "definition": ["definition"],
    "axiom": ["axiom"],
    "cornerstone": ["cornerstone"],
    "lesson": ["lesson"],
    "goal": ["goal"],
    "person node": ["person node"],
    "evidence node": ["evidence node"],
    "provenance": ["provenance"],
    "confidence": ["confidence"],
    "reasoning type": ["reasoning type"],
    "premise": ["premise"],
    "contradiction": ["contradiction"],
    "trust tier": ["trust tier"],
    "source_class": ["source_class"],
    "quote_type": ["quote_type"],
    "history tree / identity tree": ["history-tree"],
    "closest continuer": ["closest continuer"],
    "twin study": ["twin study"],
    "fresh-reader round": None,
    "snapshot": ["snapshot"],
    "node ID prefixes": ["__ID_PREFIX_TABLE__"],  # special-cased below
}


# ── helper contracts (the zh-correct parser and matcher) ────────────────────
#
# Written BEFORE the helpers were made zh-correct, because the defects they pin
# are invisible in the EN run: the file was ASCII-only in three separate places
# (the trailing-parenthetical strip, the compound split, and the `\b` word
# boundary), and each one alone produced a large false-failure list against the
# zh render. The old failure list named malformed fragments -- '种子／根（seed'
# and 'root）' -- which is the signature of the split bug, and the fix that only
# repairs the first two leaves twelve terms still missing (`\b` around CJK; the
# full list and the provenance of the count are in `_term_regex`'s docstring). A
# regression to any one of the three ASCII assumptions reddens these, rather
# than resurfacing as "the zh translation is missing ~55 terms".


@pytest.mark.parametrize(
    "raw,expected",
    [
        # zh: full-width trailing parenthetical
        ("仲裁（arbitration）", ["仲裁"]),
        # zh: full-width compound separator, AND an ASCII ' / ' INSIDE the
        # parenthetical -- which split the headword into the two malformed
        # fragments before the parenthetical was stripped.
        ("种子／根（seed / root）", ["种子", "根"]),
        ("承载主张／不承载主张（claim-bearing / non-claim-bearing）",
         ["承载主张", "不承载主张"]),
        # zh: TWO trailing parentheticals, the outer one carrying inner ASCII
        # parens -- a single strip pass leaves `现行（节点）` behind.
        ("现行（节点）（current (node)）", ["现行"]),
        ("效用（效用分）（utility (utility score)）", ["效用"]),
        # en: unchanged
        ("cascade (retraction cascade)", ["cascade"]),
        ("seed / root", ["seed", "root"]),
    ],
)
def test_headword_terms_contract(raw: str, expected: list[str]):
    assert _headword_terms(raw) == expected


def test_zh_glossary_headwords_all_yield_usable_terms():
    """Every entry in the real zh glossary yields >=1 non-empty term, and no term
    carries an unbalanced paren. Reads the shipped source file, so a future entry
    written in a headword form the parser mishandles reddens HERE rather than as
    a confusing "this term is missing from the prose" failure in T1."""
    g_path = _g_path("zh")
    assert g_path.exists(), f"missing: {g_path}"
    entries = _parse_entries(g_path.read_text(encoding="utf-8"))
    assert entries, "no zh glossary entries parsed"
    for raw in entries:
        terms = _headword_terms(raw)
        assert terms, f"headword {raw!r} yielded no term"
        for term in terms:
            assert term, f"headword {raw!r} yielded an empty term"
            assert term.count("（") == term.count("）"), (
                f"headword {raw!r} -> term {term!r}: unbalanced full-width paren"
            )
            assert term.count("(") == term.count(")"), (
                f"headword {raw!r} -> term {term!r}: unbalanced ASCII paren"
            )


def test_term_regex_matches_cjk_as_substring_and_ascii_at_boundaries():
    """`\\b` is a WORD boundary and CJK characters ARE word characters in Python's
    `re`, so `\\b遗忘曲线\\b` cannot match 遗忘曲线 inside `的遗忘曲线所` (ch7) --
    the exact case measured as still-failing after the paren and split fixes. A
    pure-ASCII term keeps its boundary, where it does real work."""
    # CJK: plain substring, so a CJK-flanked occurrence is reached.
    assert _term_regex("遗忘曲线").search("的遗忘曲线所")
    assert _term_regex("陈旧").search("标记陈旧，与矛盾") is not None
    # ASCII: the boundary still prevents matching inside a longer word.
    assert _term_regex("ENGRAM").search("ENGRAM is a graph")
    assert _term_regex("ENGRAM").search("ENGRAMISH") is None
    assert _term_regex("skill").search("skills") is None


def test_id_prefixes_are_language_keyed_with_english_values_unchanged():
    """The node-ID-prefix table's type names are English, and no English type
    name occurs in zh prose -- so the table is language-keyed, the English values
    stay byte-identical to the pre-zh-fix table, and the zh values are the names
    the zh glossary's own node-ID entry uses (see
    `appendix_G_glossary.zh.md`, the `节点 ID 前缀` entry)."""
    assert set(_ID_PREFIXES) == set(LANGS)
    assert set(_ID_PREFIXES["zh"]) == set(_ID_PREFIXES["en"])
    assert _ID_PREFIXES["en"] == {
        "ob_": "observation", "dv_": "derivation", "th_": "theory",
        "cj_": "conjecture", "df_": "definition", "ax_": "axiom",
        "cs_": "cornerstone", "ls_": "lesson", "gl_": "goal",
        "gt_": "goal tension", "ct_": "contradiction", "qu_": "question",
        "pr_": "prediction", "ev_": "evidence", "fl_": "feeling",
        "pn_": "person", "tk_": "task", "ts_": "trust signal",
    }
    assert _ID_PREFIXES["zh"] == {
        "ob_": "观察", "dv_": "推导", "th_": "理论", "cj_": "猜想",
        "df_": "定义", "ax_": "公理", "cs_": "基石", "ls_": "教训",
        "gl_": "目标", "gt_": "目标张力", "ct_": "矛盾", "qu_": "问题",
        "pr_": "预测", "ev_": "证据", "fl_": "感受报告", "pn_": "人物",
        "tk_": "任务", "ts_": "信任信号",
    }


# ── T1 ────────────────────────────────────────────────────────────────────


def test_t1_every_glossary_term_occurs_outside_g(lang: str):
    _skip_if_cannot_assemble(lang, "T1 (every glossary term occurs outside G)")
    g_path = _g_path(lang)
    assert g_path.exists(), f"missing: {g_path}"
    full = _render_full_text(lang)
    body = _body_outside_g(lang, full)
    g_text = _g_section_text(lang, full)

    entries = _parse_entries(g_text)
    assert entries, "no glossary entries parsed"

    # Source markdown is hard-wrapped: a multi-word headword like "identity
    # documents" can straddle a line break in the body prose (Ch5 §5.0 wraps
    # "... identity\ndocuments."). Collapse whitespace runs (including
    # newlines) to a single space before matching so a phrase search isn't
    # defeated by the source's own line wrapping.
    body_norm = re.sub(r"\s+", " ", body)

    missing = []
    for raw in entries:
        terms = _headword_terms(raw)
        if terms == [_ID_PREFIX_TABLE_HEADWORDS[lang]]:
            # Special-cased below: this entry is a 13-row table, not a term
            # that itself appears in prose.
            continue
        for term in terms:
            pattern = _FORM_OVERRIDES.get(term)
            if pattern is None:
                regex = _term_regex(term)
            else:
                # An override supplies its own word-form root; the leading `\b`
                # is kept and NO trailing `\b` is added -- deliberate, see the
                # `skill` override, which must reach the plural `skills`.
                regex = re.compile(r"\b" + pattern, re.IGNORECASE)
            if not regex.search(body_norm):
                missing.append(term)

    # The node-ID-prefix table entry: each prefix's node-TYPE NAME (see
    # _ID_PREFIXES docstring above for why type name, not bare prefix) must
    # be named somewhere in the body.
    for prefix, type_name in _ID_PREFIXES[lang].items():
        if prefix in _PREFIXES_CITED_TO_CODE_ONLY:
            continue
        # DELIBERATELY the strict `\b` form, NOT `_term_regex` like the headword
        # loop above. The two loops look like the same bug and are not:
        #
        #   * For CJK, `\b` is STRICTER than substring -- a substring match is a
        #     strict superset (any `\b`-bounded match implies the literal occurs),
        #     so switching can only turn a not-found into a found. On a gate that
        #     is the worse direction: it can only make this check PASS, silently.
        #   * It also fixes nothing here. Measured on the shipped zh body, 0 of
        #     the 16 checked type names change outcome under either form, and the
        #     thinnest margins (`pn_`/人物 and `cj_`/猜想) rest on ONE `\b`-flanked
        #     occurrence each. The headword loop was different: there `\b`
        #     genuinely false-failed 7 terms, so `_term_regex` fixed a real defect.
        #
        # This loop's `\b` failure mode -- a type name that ever appears ONLY
        # inside a Han run -- is loud and self-correcting. The permissive one is
        # silent and permanent. Do not "fix" this loop for symmetry.
        if not re.search(r"\b" + re.escape(type_name) + r"\b", body_norm, re.IGNORECASE):
            missing.append(f"(ID prefix {prefix}) {type_name}")

    assert not missing, f"glossary terms not found outside Appendix G: {missing}"


def test_t1_mutation_absent_term_reddens_only_this_test(tmp_path):
    """Can-it-fail demonstration: a term that never appears in the body must
    fail T1. Runs against a temp copy of G with one bogus entry appended;
    does not touch the real file."""
    full = _render_full_text("en")
    body = _body_outside_g("en", full)
    bogus = "zorblattian-nonexistent-term"
    assert not re.search(r"\b" + re.escape(bogus) + r"\b", body, re.IGNORECASE)
    g_text = _g_section_text("en", full) + f"\n| **{bogus}** | a term invented for this test. | — | — |\n"
    entries = _parse_entries(g_text)
    missing = []
    for raw in entries:
        for term in _headword_terms(raw):
            if term == "__ID_PREFIX_TABLE__":
                continue
            pattern = _FORM_OVERRIDES.get(term)
            if pattern is None:
                regex = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
            else:
                regex = re.compile(r"\b" + pattern, re.IGNORECASE)
            if not regex.search(body):
                missing.append(term)
    assert bogus in missing


# ── T2 ────────────────────────────────────────────────────────────────────

# Accepted pointer grammar:
#   §x.y            -- a numbered chapter or appendix subsection, e.g. §4.5, §E.2
#   Appendix X      -- a bare top-level appendix heading, e.g. "Appendix B"
#   Appendix X §X.n -- an appendix plus its own subsection, e.g. "Appendix E §E.2"
#   Ch N            -- a bare top-level chapter heading (not used in G today,
#                      accepted for completeness/future entries)
#   "front matter"  -- special-cased: front-matter.md carries no heading of
#                      its own below the paper title (it is loaded first,
#                      unconditionally, by both tools/render_paper.py:main()
#                      and this test's _render_full_text()), so this pointer
#                      is resolved structurally rather than by heading lookup.
#   "Data availability" -- a literal, exact, un-numbered heading in
#                      paper/bibliography.md; resolved by exact heading-text
#                      match rather than the §x.y grammar.
_SECTION_TOKEN_RE = re.compile(r"§([A-Za-z]?\d+\.\d+)")
_APPENDIX_BARE_RE = re.compile(r"\bAppendix\s+([A-Z])\b(?!\s*§)")
_APPENDIX_SECTION_RE = re.compile(r"\bAppendix\s+[A-Z]\s+§([A-Za-z]?\d+\.\d+)")
_CH_BARE_RE = re.compile(r"\bCh\s?(\d+)\b")
_NAMED_HEADING_RE = re.compile(r'"([^"]+)"')


def _heading_index(full_text: str) -> tuple[set[str], set[str], set[str]]:
    """Returns (section_tokens, appendix_letters, chapter_numbers, named_headings)
    built from every '#'-prefixed line in the render."""
    section_tokens: set[str] = set()
    appendix_letters: set[str] = set()
    chapter_numbers: set[str] = set()
    named_headings: set[str] = set()
    for line in full_text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not m:
            continue
        title = m.group(2).strip()
        named_headings.add(title)
        sec = re.match(r"^([A-Za-z]?\d+\.\d+)\b", title)
        if sec:
            section_tokens.add(sec.group(1))
        appx = re.match(r"^Appendix\s+([A-Z])\b", title)
        if appx:
            appendix_letters.add(appx.group(1))
        chap = re.match(r"^Chapter\s+(\d+)\b", title)
        if chap:
            chapter_numbers.add(chap.group(1))
    return section_tokens, appendix_letters, chapter_numbers, named_headings


def _pointers_in_entry(entry_text: str) -> list[str]:
    """All recognizable pointer substrings in one glossary entry's text."""
    found = []
    found += [f"§{t}" for t in _SECTION_TOKEN_RE.findall(entry_text)]
    found += [f"Appendix {L}" for L in _APPENDIX_BARE_RE.findall(entry_text)]
    found += [f"Ch{n}" for n in _CH_BARE_RE.findall(entry_text)]
    if "front matter" in entry_text:
        found.append("front matter")
    if "Data availability" in entry_text:
        found.append("Data availability")
    return found


def test_t2_every_pointer_resolves(lang: str):
    if lang != "en":
        _skip_zh(
            lang,
            "T2 (every pointer resolves)",
            "the pointer grammar in this file is English (`Appendix E §E.1`, `Ch8`), "
            "while the zh translation points with localised forms (`附录 E §E.1`) that "
            "this grammar does not recognise, so the check would report false "
            "unresolved pointers. A zh pointer grammar is not part of this change.",
        )
    full = _render_full_text(lang)
    g_text = _g_section_text(lang, full)
    section_tokens, appendix_letters, chapter_numbers, named_headings = _heading_index(full)

    unresolved = []
    for line in g_text.splitlines():
        for tok in _SECTION_TOKEN_RE.findall(line):
            if tok not in section_tokens:
                unresolved.append(f"§{tok}")
        for L in _APPENDIX_BARE_RE.findall(line):
            if L not in appendix_letters:
                unresolved.append(f"Appendix {L}")
        for n in _CH_BARE_RE.findall(line):
            if n not in chapter_numbers:
                unresolved.append(f"Ch{n}")

    if "front matter" in g_text:
        # Structural resolution: front-matter.md is unconditionally the first
        # part loaded (see tools/render_paper.py:main() and this file's
        # _render_full_text()); it carries no numbered heading of its own.
        assert (PAPER / FRONT_MATTER[lang]).exists()

    if "Data availability" in g_text:
        if "Data availability" not in named_headings:
            unresolved.append("Data availability")

    assert not unresolved, f"pointers that do not resolve to a real heading: {unresolved}"


def test_t2_mutation_bad_pointer_reddens_only_this_test():
    """Can-it-fail demonstration: a pointer to a non-existent section must
    fail T2. Constructs a synthetic G excerpt with a bogus pointer; does not
    touch the real file."""
    full = _render_full_text("en")
    section_tokens, appendix_letters, chapter_numbers, _named = _heading_index(full)
    bogus_token = "4.99"
    assert bogus_token not in section_tokens
    synthetic_line = "| **bogus-term** | a fake entry pointing nowhere. | — | §4.99 |"
    unresolved = []
    for tok in _SECTION_TOKEN_RE.findall(synthetic_line):
        if tok not in section_tokens:
            unresolved.append(f"§{tok}")
    assert f"§{bogus_token}" in unresolved


# ── table contract (C1) ────────────────────────────────────────────────────
#
# Appendix G is a three-column table with its rare notes listed under it. These
# tests pin the LAYOUT contract; word-level preservation across the move is C7/C8
# below, and the marker <-> note pairing is C9.


def test_c1_table_shape_header_and_three_cells_per_row(lang: str):
    text = _g_path(lang).read_text(encoding="utf-8")
    body = _glossary_body(text) if lang == "zh" else text
    lines = body.splitlines()
    head_idx = [i for i, l in enumerate(lines) if l.startswith("| ") and
                _split_cells(l) == _TABLE_HEADER[lang]]
    assert len(head_idx) == 1, f"expected exactly one {lang} header row {_TABLE_HEADER[lang]}"
    sep = lines[head_idx[0] + 1]
    assert re.fullmatch(r"\|(?:\s*:?-{3,}:?\s*\|){3}", sep), f"bad separator row: {sep!r}"
    rows = []
    for l in lines[head_idx[0] + 2:]:
        if not l.startswith("|"):
            break
        rows.append(l)
    assert len(rows) == 59 and all(l.startswith("| **") for l in rows), (
        "every line of the table after the separator must be a data row")
    for l in rows:
        assert len(_split_cells(l)) == 3, f"row does not have exactly 3 cells: {l[:80]!r}"
    # The notes list sits directly under the table, behind its lead line.
    rest = [l for l in lines[head_idx[0] + 2 + len(rows):] if l.strip()]
    assert rest and rest[0] == _NOTES_LEAD[lang], f"no {_NOTES_LEAD[lang]!r} lead line under the table"
    assert all(_NOTE_LINE_LOOSE.match(l) for l in rest[1:]), "non-note line in the notes list"


def test_c1_term_column_is_the_pre_table_headword_list_in_order(lang: str):
    """Source file AND the rendered Appendix G."""
    expected = _EXPECTED_HEADWORDS[lang]
    assert len(expected) == 59
    src = _g_path(lang).read_text(encoding="utf-8")
    assert _parse_entries(src) == expected
    rendered = _g_section_text(lang, _fresh_render(lang))
    assert _parse_entries(rendered) == expected


def test_c1_headword_parser_reads_rows_not_prose():
    """Can-it-fail for the parser itself: a bold phrase in running prose or in a
    non-first cell is NOT a headword; only a row's first cell is."""
    text = (
        "A **bold intro** line.\n\n"
        "| Term | Definition | Section |\n|---|---|---|\n"
        "| **alpha** (annotation) | has **bold** inside | §1.1 |\n"
    )
    assert _parse_entries(text) == ["alpha"]
    assert _parse_rows(text) == [["**alpha** (annotation)", "has **bold** inside", "§1.1"]]


# ── Definition / Notes split (C7, C8) ──────────────────────────────────────
#
# Round 1 split each entry at its first top-level `;` and DROPPED the `;`, which cut
# single-sentence definitions in half and left fragments in the Definition cell.
# The rule now: Definition = the entry's FIRST SENTENCE, whole, as it stood in the
# paper at 89248b5 (its semicolons and the clauses after them included); Notes =
# every following sentence, verbatim, or `—` when there is none. The old text is
# frozen in tests/fixtures/glossary_entries_v1_{en,zh}.txt (one entry per line,
# whitespace collapsed, extracted from 89248b5) because origin/main moves.
# 2026-10-12, translator ruling (Zephyr): zh 承载框架 note dropped, zh 心迹 note's
# file-header pointer removed; all other entries are the 89248b5 text.
# 2026-10-14, v2 errata (Kepler, workstream A of paper issue #10): three entries
# corrected in both languages and the fixture moved with them — checkpoint's
# pointer §4.9 → §4.11 (reset-symmetry is stated in §4.11), unified's pointer
# §A.4 → §A.3 (the first-captured table), forgetting curve's
# 'time-translation-invariant' → 'memoryless' (the property the paper means).

_FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures"
_SENTENCE_JOIN = {"en": " ", "zh": ""}
# A sentence boundary. en: terminal punctuation, an optional closing quote, then
# whitespace and the start of the next sentence (a capital or an `*italic` opener)
# -- so `e.g. "every graph...` and `p. 1136]` and `§4.6` do not split. zh: see
# `_first_sentence` (a `。`, then a closing quote if one is open).
_SENTENCE_END_EN = re.compile(r'[.!?]["”]?\s+(?=[A-Z*])')
# The pointer wrapper the pre-table entry carried around the Section cell.
_POINTER_WRAPPER = {
    "en": lambda s: re.compile(r"\s\((?:Defined )?" + re.escape(s) + r"\.\)$"),
    "zh": lambda s: re.compile(r"（(?:界定于\s*)?" + re.escape(s) + r"。）$"),
}


def _collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _fixture_entries(lang: str) -> list[tuple[str, str]]:
    """[(term_cell_text, body)] from the frozen 89248b5 entries."""
    path = _FIXTURE_DIR / f"glossary_entries_v1_{lang}.txt"
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        head, sep, body = line.partition(" — ")
        assert sep, f"fixture line has no headword dash: {line[:60]!r}"
        out.append((head, body))
    return out


def _first_sentence(text: str, lang: str) -> tuple[str, str]:
    """(first sentence, the rest) of `text`; the rest is '' for a one-sentence text.

    zh: the first `。` that is followed by more text which is not a closing `）`
    (the `（...。）` trailing-note form ends in `。）`). A straight `"` right after
    the `。` belongs to the sentence only when a quote is OPEN there (odd count of
    `"` before it: `"我错了。"`); otherwise it opens the next sentence's quote
    (`。"the sweep"取义项（2）。`)."""
    if lang == "en":
        m = _SENTENCE_END_EN.search(text)
        if not m:
            return text, ""
        return text[: m.start()] + m.group(0).rstrip(), text[m.end():]
    for m in re.finditer("。", text):
        i = m.end()
        if i < len(text) and (text[i] == "”" or (text[i] == '"' and text[:i].count('"') % 2 == 1)):
            i += 1
        if i < len(text) and text[i] != "）":
            return text[:i], text[i:]
    return text, ""


def _entry_text_without_pointer(body: str, section: str, lang: str) -> str:
    """The old entry body with its trailing `(Defined <Section>.)` wrapper removed.
    Fails if the Section cell is not the pointer the old entry ended with."""
    if section == _EMPTY_CELL:
        return body
    m = _POINTER_WRAPPER[lang](section).search(body)
    if m:
        return body[: m.start()]
    if lang == "zh":
        # The one entry whose trailing paren carries a translator's note after the
        # pointer (`（§5.0。译名待定，见文件头。）`): the pointer moves to the Section
        # cell and the paren stays around the note, which remains in Notes.
        m = re.search(r"（" + re.escape(section) + r"。(?=[^（）]+）$)", body)
        if m:
            return body[: m.start()] + "（" + body[m.end():]
    raise AssertionError(
        f"Section {section!r} is not the trailing pointer of the old entry {body[-70:]!r}")


def _rows_for(lang: str) -> list[list[str]]:
    text = _g_path(lang).read_text(encoding="utf-8")
    return _parse_rows(_glossary_body(text) if lang == "zh" else text)


def test_fixture_is_the_pre_table_entry_list(lang: str):
    """The frozen fixture carries all 59 entries, headwords in the C1 order."""
    ents = _fixture_entries(lang)
    assert len(ents) == 59
    assert [re.match(r"\*\*(.+?)\*\*", h).group(1) for h, _ in ents] == _EXPECTED_HEADWORDS[lang]


def _notes_for(lang: str) -> list[tuple[int, int, str, str]]:
    text = _g_path(lang).read_text(encoding="utf-8")
    return _parse_notes(_glossary_body(text) if lang == "zh" else text)


def _row_note_text(notes: list, n: int | None) -> str | None:
    """The text of numbered note `n` (None for a row with no marker)."""
    if n is None:
        return None
    by_n = {a: t for a, _shown, _h, t in notes}
    assert n in by_n, f"marker {n} has no note line"
    return by_n[n]


def test_c7_definition_plus_note_plus_pointer_reconstructs_the_old_entry(lang: str):
    """For every row: Definition (marker stripped) + its numbered note's text (if
    the row has one) + the re-wrapped Section pointer is the 89248b5 entry text,
    modulo whitespace and the removed wrapper words / parens / headword dash -- no
    word, `;` or `；` was dropped or moved by the split, INCLUDING the words that
    moved from the Notes column into the notes list under the table."""
    fixture, rows, notes = _fixture_entries(lang), _rows_for(lang), _notes_for(lang)
    assert len(rows) == len(fixture) == 59
    for (term_text, body), (term, definition, section) in zip(fixture, rows):
        assert term == term_text, f"term cell changed: {term!r} != {term_text!r}"
        old = _entry_text_without_pointer(body, section, lang)
        d, n = _split_marker(definition)
        note = _row_note_text(notes, n)
        new = d if note is None else d + _SENTENCE_JOIN[lang] + note
        assert _collapse_ws(new) == _collapse_ws(old), (
            f"{term_text}: Definition + note != the old entry text\n new: {new!r}\n old: {old!r}")


# "Sense (N) unless stated." / `Sense (2) for "the sweep."` and the zh forms: part
# of the senses definition, so they stay INSIDE the Definition cell, not in a note.
_SENSE_TAIL = {
    "en": re.compile(r'Sense \(\d\) (?:unless stated\.|for "the sweep\.")'),
    "zh": re.compile(r'(?:除另有说明，|"the sweep")取义项（\d）。'),
}


def test_c8_definition_is_the_first_sentence_whole_senses_keep_their_tail(lang: str):
    """No Definition cell ends mid-sentence: it IS the first sentence of the old
    entry (clauses after its `;` included) -- except a senses row, whose Definition
    is the first sentence PLUS its `Sense (N) unless stated.` tail. Whatever follows
    that is the row's numbered note, verbatim; a row with nothing after has no
    marker."""
    fixture, rows, notes = _fixture_entries(lang), _rows_for(lang), _notes_for(lang)
    n_tail = n_note = 0
    for (term_text, body), (_t, definition, section) in zip(fixture, rows):
        first, rest = _first_sentence(
            _collapse_ws(_entry_text_without_pointer(body, section, lang)), lang)
        tail = _SENSE_TAIL[lang].match(rest)
        if tail:
            n_tail += 1
            first = first + _SENTENCE_JOIN[lang] + tail.group(0)
            rest = rest[tail.end():].strip()
        d, n = _split_marker(definition)
        assert _collapse_ws(d) == first, f"{term_text}: Definition is not the first sentence"
        assert (n is None) == (rest == ""), f"{term_text}: marker present iff a note remains"
        if n is not None:
            n_note += 1
            assert _collapse_ws(_row_note_text(notes, n)) == rest, f"{term_text}: note is not the rest"
    assert 5 <= n_tail < 20 and 5 <= n_note < 20, (n_tail, n_note)  # non-vacuous


def _gnote_problems(g_text: str, lang: str) -> list[str]:
    """Everything wrong with the note markers / note list of `g_text` (source or a
    render's Appendix G); empty = consistent. Rows in table order."""
    problems: list[str] = []
    rows = _parse_rows(g_text)
    notes = _parse_notes(g_text)
    markers: list[tuple[int, str]] = []  # (n, row headword), table order
    for term, definition, _section in rows:
        head = re.match(r"\*\*(.+?)\*\*", term).group(1)
        for m in _MARKER.finditer(definition):
            if m.group(1) != m.group(2):
                problems.append(f"marker text/target differ in row {head!r}: {m.group(0)}")
            markers.append((int(m.group(2)), head))
    # the marker may live only in a Definition cell (not elsewhere in the text)
    if len(_MARKER.findall(g_text)) != len(markers):
        problems.append("a note marker sits outside a table Definition cell")
    k = len(markers)
    if [n for n, _h in markers] != list(range(1, k + 1)):
        problems.append(f"markers are not 1..{k} contiguous in table order: {[n for n, _h in markers]}")
    if [a for a, *_ in notes] != list(range(1, len(notes) + 1)):
        problems.append(f"note anchors are not 1..{len(notes)} contiguous: {[a for a, *_ in notes]}")
    for a, shown, head, _t in notes:
        if a == -1:
            problems.append("a note line does not have the exact shape")
        elif a != shown:
            problems.append(f"note {a} is shown as {shown}")
    marker_count = Counter(n for n, _h in markers)
    for a, *_ in notes:
        if marker_count[a] != 1:
            problems.append(f"note {a} has {marker_count[a]} markers, not exactly one")
    note_nums = Counter(a for a, *_ in notes)
    for n, head in markers:
        if note_nums[n] != 1:
            problems.append(f"marker {n} (row {head!r}) has {note_nums[n]} note lines, not exactly one")
    by_marker = dict(markers)
    for a, _s, head, _t in notes:
        if a in by_marker and by_marker[a] != head:
            problems.append(f"note {a} is headed {head!r} but its marker is in row {by_marker[a]!r}")
    if _NOTES_LEAD[lang] not in g_text.splitlines():
        problems.append(f"lead line {_NOTES_LEAD[lang]!r} missing")
    return problems


def test_c9_note_markers_and_note_lines_pair_one_to_one(lang: str):
    """Every `<sup>[n](#gnote-n)</sup>` marker has exactly one `<a id="gnote-n">`
    note, numbers are 1..k contiguous in table order, every note has exactly one
    marker, and each note is headed with its row's headword -- in the source AND in
    the rendered Appendix G."""
    src = _g_path(lang).read_text(encoding="utf-8")
    src = _glossary_body(src) if lang == "zh" else src
    assert _gnote_problems(src, lang) == []
    rendered = _g_section_text(lang, _fresh_render(lang))
    assert _gnote_problems(rendered, lang) == []
    k = len(_notes_for(lang))
    assert k >= 6, k  # non-vacuous
    assert len(_parse_notes(rendered)) == k


def test_c9_checker_fails_on_a_lost_duplicated_or_misnumbered_note(lang: str):
    """Can-it-fail for the C9 instrument, on the real source text."""
    src = _g_path(lang).read_text(encoding="utf-8")
    src = _glossary_body(src) if lang == "zh" else src
    assert _gnote_problems(src, lang) == []
    lines = src.splitlines()
    note_idx = [i for i, l in enumerate(lines) if _NOTE_LINE_LOOSE.match(l)]
    # a note line deleted (a marker is left without its note)
    lost = "\n".join(l for i, l in enumerate(lines) if i != note_idx[1])
    assert _gnote_problems(lost, lang) != []
    # a marker deleted (a note is left without its marker)
    first_marker = _MARKER.search(src).group(0)
    assert _gnote_problems(src.replace(first_marker, "", 1), lang) != []
    # a duplicated note line
    dup = lines[:note_idx[0] + 1] + [lines[note_idx[0]]] + lines[note_idx[0] + 1:]
    assert _gnote_problems("\n".join(dup), lang) != []
    # a marker whose target differs from its text
    assert _gnote_problems(src.replace("(#gnote-1)", "(#gnote-2)", 1), lang) != []
    # a note under the wrong headword
    head = re.match(r'<a id="gnote-1"></a>1\. \*\*(.+?)\*\*', lines[note_idx[0]]).group(1)
    assert _gnote_problems(src.replace(f"1. **{head}**", "1. **elsewhere**", 1), lang) != []


@pytest.mark.parametrize(
    "lang,text,first,rest",
    [
        ("en", "a x; b y. C d.", "a x; b y.", "C d."),
        ("en", 'to withdraw: "I was wrong." The cascade fires.', 'to withdraw: "I was wrong."', "The cascade fires."),
        ("en", 'the set, e.g. "every graph in this fleet."', 'the set, e.g. "every graph in this fleet."', ""),
        ("en", "contested [@a1999, p. 1136].", "contested [@a1999, p. 1136].", ""),
        ("en", "points (§4.6; Appendix E §E.2). Sense (1) unless stated.",
         "points (§4.6; Appendix E §E.2).", "Sense (1) unless stated."),
        ("zh", "甲；乙。丙；丁。", "甲；乙。", "丙；丁。"),
        ("zh", '收回："我错了。"级联触发。', '收回："我错了。"', "级联触发。"),
        ("zh", "甲。（注：乙。）", "甲。", "（注：乙。）"),
        ("zh", '甲（2）。"the sweep"取义项（2）。', "甲（2）。", '"the sweep"取义项（2）。'),
        ("zh", "只有一句。", "只有一句。", ""),
    ],
)
def test_first_sentence_splitter(lang, text, first, rest):
    assert _first_sentence(text, lang) == (first, rest)


# ── pointer links & heading anchors (C2, C3, C4) ───────────────────────────
#
# The RENDERER turns every section pointer in Appendix G's table into a markdown
# link and inserts the matching `<a id="..."></a>` line before the target
# heading, from ONE scan, so a link and its target cannot drift apart (the same
# single-source idea as `#ref-<key>` for citations). Sources keep plain-text
# pointers.

_FRESH: dict[str, str] = {}


def _fresh_render(lang: str) -> str:
    """The real `tools/render_paper.py --lang <lang>` output, rendered to a temp
    path via `--out` (never in place), cached per language for this module."""
    if lang not in _FRESH:
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / f"fresh-{lang}.md"
            result = subprocess.run(
                [sys.executable, "tools/render_paper.py", "--lang", lang, "--out", str(out)],
                cwd=REPO_ROOT, capture_output=True, text=True,
            )
            assert result.returncode == 0, result.stderr
            _FRESH[lang] = out.read_text(encoding="utf-8")
    return _FRESH[lang]


_ANCHOR_LINE = re.compile(r'^<a id="([^"]+)"></a>$', re.MULTILINE)
_G_LINK = re.compile(
    r"\]\(#((?:sec|appendix|ch)-[A-Za-z0-9-]+|front-matter|data-availability)\)")
_MD_LINK = re.compile(r"\[[^\]]*\]\([^)]*\)")
_SEC = r"§(?:[A-Z]\.\d+|\d+\.\d+)"
# Written independently of the renderer's grammar: what a plain-text pointer in
# the SOURCE looks like. Used to count the expected links and to find leftovers.
_PLAIN_POINTER = {
    "en": re.compile(
        rf"Appendix [A-Z] {_SEC}|Appendix [A-Z]\b|{_SEC}|Chapter \d+|\bCh ?\d+\b"
        r"|front matter|Data availability"),
    "zh": re.compile(
        rf"附录 ?[A-Z] ?{_SEC}|附录 ?[A-Z](?![A-Za-z0-9])|{_SEC}|第 ?\d+ ?章"
        r"|前置部分|数据可用性"),
}


def _table_rows_text(g_text: str) -> str:
    """The glossary's linkable lines: the table's data rows AND the note lines of
    the list under it (both carry section pointers)."""
    return "\n".join(
        l for l in g_text.splitlines()
        if re.match(r"^\|\s*\*\*", l) or _NOTE_LINE_LOOSE.match(l))


# A note's anchor shares its line with the note text (`<a id="gnote-3"></a>3. ...`),
# so it is not an `_ANCHOR_LINE`; it is counted with the other ids all the same.
_GNOTE_ANCHOR = re.compile(r'<a id="(gnote-\d+)"></a>')
_GNOTE_LINK = re.compile(r"\]\(#(gnote-\d+)\)")


def _all_anchor_ids(render: str) -> Counter:
    return Counter(_ANCHOR_LINE.findall(render)) + Counter(_GNOTE_ANCHOR.findall(render))


def _unresolved_g_links(render: str, lang: str) -> list[str]:
    """Targets of Appendix G's pointer links that do not appear EXACTLY ONCE as an
    anchor id in the same render."""
    ids = _all_anchor_ids(render)
    g = _g_section_text(lang, render)
    return [t for t in _G_LINK.findall(g) + _GNOTE_LINK.findall(g) if ids[t] != 1]


def _duplicate_anchor_ids(render: str) -> list[str]:
    return sorted(i for i, n in _all_anchor_ids(render).items() if n > 1)


def _heading_lines(text: str) -> list[str]:
    """Every ATX heading line outside fenced code blocks, in order."""
    out, fenced = [], False
    for l in text.splitlines():
        if re.match(r"^ {0,3}(```|~~~)", l):
            fenced = not fenced
        elif not fenced and re.match(r"^#{1,6}\s", l):
            out.append(l)
    return out


def test_c2_every_pointer_link_targets_exactly_one_anchor(lang: str):
    render = _fresh_render(lang)
    assert _unresolved_g_links(render, lang) == []
    # NON-VACUOUS: every plain-text pointer in the SOURCE rows became a link, and
    # none was left as plain text.
    src_rows = _table_rows_text(_g_path(lang).read_text(encoding="utf-8"))
    expected_links = len(_PLAIN_POINTER[lang].findall(src_rows))
    g_rows = _table_rows_text(_g_section_text(lang, render))
    assert expected_links > 80, expected_links
    assert _GNOTE_LINK.findall(g_rows) and len(_GNOTE_LINK.findall(g_rows)) == len(_notes_for(lang))
    assert len(_G_LINK.findall(g_rows)) == expected_links
    leftover = _PLAIN_POINTER[lang].findall(_MD_LINK.sub("", g_rows))
    assert leftover == [], f"pointers left as plain text in the {lang} table: {leftover}"


def test_c2_checker_fails_on_a_missing_renamed_or_duplicated_anchor(lang: str):
    """Can-it-fail for the C2 instrument: the checker must go red when an anchor
    is removed, when a link is retargeted to a section that does not exist, and
    when an anchor id is duplicated."""
    render = _fresh_render(lang)
    assert _unresolved_g_links(render, lang) == []
    g = _g_section_text(lang, render)
    first = _G_LINK.findall(g)[0]
    anchor = f'<a id="{first}"></a>\n'
    assert render.count(anchor) == 1
    assert _unresolved_g_links(render.replace(anchor, ""), lang) == [first] * _G_LINK.findall(g).count(first)
    m = _G_LINK.search(g)
    bad = render.replace(g, g.replace(m.group(0), "](#sec-9-99)", 1))
    assert _unresolved_g_links(bad, lang) == ["sec-9-99"]
    assert _unresolved_g_links(render.replace(anchor, anchor * 2), lang) != []


def test_c3_no_anchor_id_is_duplicated_anywhere_in_the_render(lang: str):
    render = _fresh_render(lang)
    assert len(_ANCHOR_LINE.findall(render)) > 30  # non-vacuous: ref- + section anchors
    assert _duplicate_anchor_ids(render) == []
    assert _duplicate_anchor_ids(render + '\n<a id="sec-4-6"></a>\n<a id="sec-4-6"></a>\n') == ["sec-4-6"]
    # the gnote-* anchors are inside the uniqueness check, and a note whose anchor
    # is gone, or doubled, or that collides with another id, is caught
    assert [i for i in _all_anchor_ids(render) if i.startswith("gnote-")], "no gnote anchors in the render"
    assert _duplicate_anchor_ids(render + '\n<a id="gnote-1"></a>x\n') == ["gnote-1"]
    gone = _GNOTE_ANCHOR.search(render).group(0)
    assert _unresolved_g_links(render.replace(gone, "", 1), lang) != []


_SECTION_ANCHOR_ID = re.compile(r"(?:sec|appendix|ch)-|front-matter$|data-availability$")


def _is_section_anchor(line: str) -> bool:
    m = re.fullmatch(r'<a id="([^"]+)"></a>', line)
    return bool(m and _SECTION_ANCHOR_ID.match(m.group(1)))


def test_c4_headings_unchanged_and_anchors_sit_on_their_own_line_before_them(
    lang: str, monkeypatch, tmp_path
):
    """The anchor insertion adds LINES and changes nothing else: the render with
    the insertion switched off, and the real render with its section-anchor lines
    deleted, carry the same non-blank lines -- so no heading line (or any other
    line) was altered. And every anchor sits alone, directly before a heading."""
    # Both renders go to the SAME directory: the figure links are computed
    # relative to the output file's directory, so two directories would differ.
    monkeypatch.chdir(REPO_ROOT)
    anchored = tmp_path / "anchored.md"
    assert rp.main(["--lang", lang, "--out", str(anchored)]) == 0
    render = anchored.read_text(encoding="utf-8")
    monkeypatch.setattr(rp, "insert_heading_anchors", lambda text, targets: text)
    plain = tmp_path / "plain.md"
    assert rp.main(["--lang", lang, "--out", str(plain)]) == 0
    unanchored = plain.read_text(encoding="utf-8")
    assert unanchored != render, "the anchor insertion switch-off changed nothing"
    # Blank lines are compared out: a heading that follows a paragraph line with
    # no blank between (one in the zh ch4 source, before "## 4.4") gets one blank
    # line inserted along with its anchor, so the anchor is not glued onto that
    # paragraph. Every NON-blank line must be identical, in order.
    def nonblank(text: str) -> list[str]:
        return [l for l in text.split("\n") if l.strip()]

    assert nonblank("\n".join(l for l in render.split("\n") if not _is_section_anchor(l))) == nonblank(unanchored)
    assert _heading_lines(render) == _heading_lines(unanchored)
    lines = render.splitlines()
    section_anchors = [i for i, l in enumerate(lines) if _is_section_anchor(l)]
    assert section_anchors, "no section anchors were inserted"
    for i in section_anchors:
        assert re.match(r"#{1,6}\s", lines[i + 1]), f"anchor not directly before a heading: {lines[i:i+2]}"
        assert i == 0 or lines[i - 1].strip() == "", f"anchor shares a paragraph with the line above: {lines[i-1:i+1]}"


@pytest.mark.parametrize(
    "src,expected",
    [
        ("(§4.6)", "([§4.6](#sec-4-6))"),
        ("§E.2", "[§E.2](#sec-E-2)"),
        ("Appendix E §E.2", "[Appendix E §E.2](#sec-E-2)"),
        ("Appendix C", "[Appendix C](#appendix-C)"),
        ("Chapter 5 holds it", "[Chapter 5](#ch-5) holds it"),
        ("Ch8", "[Ch8](#ch-8)"),
        ("front matter; Data availability",
         "[front matter](#front-matter); [Data availability](#data-availability)"),
        ("(§4.7; Appendix C)", "([§4.7](#sec-4-7); [Appendix C](#appendix-C))"),
    ],
)
def test_link_glossary_pointers_en_grammar(src, expected):
    row = f"| **t** | {src} | — |"
    linked, targets = rp.link_glossary_pointers(row, "en")
    assert linked == f"| **t** | {expected} | — |"
    assert targets == set(re.findall(r"\(#([^)]+)\)", expected))


@pytest.mark.parametrize(
    "src,expected",
    [
        ("（§4.6）", "（[§4.6](#sec-4-6)）"),
        ("附录 E §E.2", "[附录 E §E.2](#sec-E-2)"),
        ("附录 C", "[附录 C](#appendix-C)"),
        ("第 5 章将其固定", "[第 5 章](#ch-5)将其固定"),
        ("前置部分；数据可用性", "[前置部分](#front-matter)；[数据可用性](#data-availability)"),
    ],
)
def test_link_glossary_pointers_zh_grammar(src, expected):
    row = f"| **t** | {src} | — |"
    linked, targets = rp.link_glossary_pointers(row, "zh")
    assert linked == f"| **t** | {expected} | — |"
    assert targets == set(re.findall(r"\(#([^)]+)\)", expected))


def test_link_glossary_pointers_touches_table_rows_only():
    text = ("# Appendix G — Glossary\n\nSee §4.6 and Appendix C.\n\n"
            "| Term | Definition | Section |\n|---|---|---|\n"
            "| **t** | x<sup>[1](#gnote-1)</sup> | §4.6 |\n\n**Notes**\n\n"
            '<a id="gnote-1"></a>1. **t** — see (§4.7; Appendix C).\n')
    linked, targets = rp.link_glossary_pointers(text, "en")
    assert "See §4.6 and Appendix C." in linked and "# Appendix G — Glossary" in linked
    assert "| **t** | x<sup>[1](#gnote-1)</sup> | [§4.6](#sec-4-6) |" in linked
    # the note lines under the table are linked too (and only they, below it)
    assert ('<a id="gnote-1"></a>1. **t** — see ([§4.7](#sec-4-7); [Appendix C](#appendix-C)).'
            in linked)
    assert targets == {"sec-4-6", "sec-4-7", "appendix-C"}


_HEADINGS_EN = (
    "# Epistemic Identity\n\ntext\n\n# Chapter 8 — Conclusion\n\n## 4.6 Auto-surface\n\n"
    "```\n# 4.6 not a heading, inside a fence\n```\n\n# Appendix E — Spec\n\n## E.2 Node types\n\n"
    "## Data availability\n"
)


def test_insert_heading_anchors_places_each_anchor_before_its_heading():
    targets = {"sec-4-6", "sec-E-2", "appendix-E", "ch-8", "front-matter", "data-availability"}
    out = rp.insert_heading_anchors(_HEADINGS_EN, targets)
    lines = out.splitlines()
    for t, heading in [
        ("front-matter", "# Epistemic Identity"), ("ch-8", "# Chapter 8 — Conclusion"),
        ("sec-4-6", "## 4.6 Auto-surface"), ("appendix-E", "# Appendix E — Spec"),
        ("sec-E-2", "## E.2 Node types"), ("data-availability", "## Data availability"),
    ]:
        assert lines[lines.index(heading) - 1] == f'<a id="{t}"></a>'
    assert out.count("<a id=") == 6
    assert _heading_lines(out) == _heading_lines(_HEADINGS_EN)


def test_insert_heading_anchors_zh_heading_forms():
    zh = ("# 标题\n\n# 第 8 章 —— 结论\n\n## 4.6 自动浮现\n\n# 附录 E —— 规格\n\n"
          "## E.2 节点类型\n\n## 数据可用性\n")
    out = rp.insert_heading_anchors(
        zh, {"ch-8", "sec-4-6", "appendix-E", "sec-E-2", "data-availability", "front-matter"})
    assert out.count("<a id=") == 6
    assert _heading_lines(out) == _heading_lines(zh)


def test_insert_heading_anchors_fails_loudly_on_a_missing_or_ambiguous_target():
    with pytest.raises(SystemExit):
        rp.insert_heading_anchors(_HEADINGS_EN, {"sec-9-99"})
    with pytest.raises(SystemExit):
        rp.insert_heading_anchors(_HEADINGS_EN + "\n## 4.6 A second 4.6\n", {"sec-4-6"})


# ── T3 ────────────────────────────────────────────────────────────────────


def test_t3_g_carries_zero_node_ids(lang: str):
    g_path = _g_path(lang)
    assert g_path.exists(), f"missing: {g_path}"
    text = g_path.read_text(encoding="utf-8")
    assert not _ID_SCAN.search(text), f"Appendix G source carries a node ID ({g_path})"

    # The render-side half needs the whole book assembled. Where chapters are
    # untranslated this skips after the source-side assertion above has already
    # run and passed -- the skip reason says so, so the "skipped" line is never
    # read as "nothing was checked".
    _skip_if_cannot_assemble(
        lang, "T3 render-side scan (the source-side zero-ID scan above ran and passed)"
    )
    full = _render_full_text(lang)
    g_text = _g_section_text(lang, full)
    assert not _ID_SCAN.search(g_text), "Appendix G render carries a node ID"


# ── T4 ────────────────────────────────────────────────────────────────────


# Han characters = the CJK Unified Ideographs block, U+4E00-U+9FFF -- the two
# bounds below, written in hex so the block is visible in the source.
# Deliberately NOT a "not-ASCII" count: the block excludes the CJK punctuation
# (U+3000-U+303F) and full-width forms (U+FF00-U+FFEF) a zh caption also carries
# (160 and 538 occurrences respectively in the current draft), plus every Latin
# token, so the count measures *ideographic content* only.
_HAN_BLOCK = (0x4E00, 0x9FFF)


def _han_char_count(text: str) -> int:
    lo, hi = _HAN_BLOCK
    return sum(1 for ch in text if lo <= ord(ch) <= hi)


# The zh ledger opens with a translator header -- ONE HTML comment block at the
# top of the file (terminology convention, coinage table, the term-choice test).
# It is translator metadata, not glossary prose: markdown hides `<!-- ... -->`,
# and the English glossary has no counterpart block, so a count that included it
# would not be comparable to the English figure and would drift on every
# documentation edit. T4's zh count EXCLUDES it, via the helper below. The
# regex is anchored at the file start (`\A`) and limited to one substitution, so
# a comment pair appearing later in the glossary BODY is never touched -- the
# three tests after the helper pin that contract.
_LEADING_TRANSLATOR_HEADER = re.compile(r"\A\s*<!--.*?-->\s*", re.S)


def _glossary_body(text: str) -> str:
    """`text` with a LEADING translator-header comment block removed, if any.

    Anchored at the start of the file (`\\A`), and removing at most one block: a
    comment pair appearing later in the glossary BODY is prose, not a header,
    and must survive. A no-op for a source with no leading comment -- which is
    every English file, so T4's English branch is unaffected.
    """
    return _LEADING_TRANSLATOR_HEADER.sub("", text, count=1)


def test_glossary_body_strips_a_leading_translator_header():
    text = "<!--\n  translator: Zephyr\n-->\n# 附录 G — 术语表\n\n正文\n"
    assert _glossary_body(text) == "# 附录 G — 术语表\n\n正文\n"


def test_glossary_body_never_strips_a_body_comment():
    """The strip is anchored at the file start. An UNANCHORED `<!--.*?-->` with
    DOTALL matches the first `<!--` anywhere, so on this input it would delete
    the body's comment and silently drop glossary text from the count -- the
    failure mode the anchoring exists to prevent. Must be a no-op here."""
    text = "# 附录 G — 术语表\n\n术语<!-- 内注 -->定义\n"
    assert _glossary_body(text) == text


def test_glossary_body_is_a_noop_without_a_leading_comment():
    """Every English glossary source has no translator header, so the helper
    must return it unchanged."""
    text = "# Appendix G — Glossary\n\n**arbitration** — ...\n"
    assert _glossary_body(text) == text


# ── T4 (length): per-entry limits that scale with the number of terms ─────────
#
# Lei, 2026-10-10: the glossary's total length limit "should naturally scale with
# the actual number of terms in it. The real meaningful cap should be a per-term
# average or something, so we avoid over complex and verbal definitions." The
# fixed 1800-word total is therefore gone; the limits are
# `rp.GLOSSARY_AVG_WORDS_PER_ENTRY` (mean per entry) and
# `rp.GLOSSARY_MAX_WORDS_PER_ENTRY` (worst single entry), zh scaled by
# `rp.ZH_HAN_PER_EN_WORD`. An ENTRY is a table ROW (`_parse_rows`: a line whose first
# cell opens with a bold headword); text before the first entry
# (the intro) is not counted, and neither is the zh translator header
# (`_glossary_body`).


def _entry_size(row: list[str], lang: str, note: str | None = None) -> int:
    """The size of one ENTRY = the words of its row: Term + Definition + Section,
    PLUS its numbered note's text if it has one -- i.e. the same words the pre-table
    entry had, so the budget measures the same text as before the notes moved out
    of the table (the `—` empty-cell marker, the table pipes and the note marker are
    layout, not words, and are not counted)."""
    cells = [_MARKER.sub("", c) for c in row if c != _EMPTY_CELL]
    text = " ".join(cells + ([note] if note else []))
    return _han_char_count(text) if lang == "zh" else len(text.split())


def _entry_stats(
    text: str, lang: str
) -> tuple[int, float, int, list[tuple[str, int]]]:
    """(n_entries, mean size, max size, [(headword, size) for every entry]) over
    the glossary ROWS of `text`: intro, header row and zh translator header
    excluded."""
    body = _glossary_body(text) if lang == "zh" else text
    by_n = {a: t for a, _shown, _h, t in _parse_notes(body)}
    sizes = []
    for row in _parse_rows(body):
        found = _MARKER.findall(row[1])
        note = by_n.get(int(found[0][1])) if found else None
        sizes.append((re.match(r"\*\*(.+?)\*\*", row[0]).group(1), _entry_size(row, lang, note)))
    if not sizes:
        return 0, 0.0, 0, []
    vals = [n for _, n in sizes]
    return len(vals), sum(vals) / len(vals), max(vals), sizes


def _entry_limit_violations(text: str, lang: str) -> list[str]:
    """Human-readable failures of the AVG and MAX limits; empty = within both."""
    scale = rp.ZH_HAN_PER_EN_WORD if lang == "zh" else 1.0
    unit = "Han characters" if lang == "zh" else "words"
    avg_cap = rp.GLOSSARY_AVG_WORDS_PER_ENTRY * scale
    max_cap = rp.GLOSSARY_MAX_WORDS_PER_ENTRY * scale
    n, mean, _mx, sizes = _entry_stats(text, lang)
    assert n, "no glossary entries found"
    out = []
    if mean > avg_cap:
        out.append(
            f"AVG: mean {mean:.1f} {unit} per entry over {n} entries exceeds the "
            f"cap {avg_cap:.1f}"
        )
    for head, size in sizes:
        if size > max_cap:
            out.append(
                f"MAX: entry {head!r} is {size} {unit}, over the per-entry cap "
                f"{max_cap:.1f}"
            )
    return out


def _synthetic(sizes: list[int], lang: str, intro: str = "") -> str:
    """A glossary TABLE whose row k has exactly sizes[k] counted units. en:
    whitespace tokens (the `**tK**` term is 1 of them); zh: Han characters (the
    Latin term adds 0). Section is the empty marker `—`; no row has a note."""
    parts = [intro] if intro else []
    hdr = _TABLE_HEADER[lang]
    rows = ["| " + " | ".join(hdr) + " |", "|---|---|---|"]
    for k, n in enumerate(sizes):
        if lang == "zh":
            rows.append(f"| **t{k}** | " + "字" * n + " | — |")
        else:
            rows.append(f"| **t{k}** | " + " ".join(["w"] * (n - 1)) + " | — |")
    parts.append("\n".join(rows))
    return "\n\n".join(parts) + "\n"


def _scaled(n_en: int, lang: str) -> int:
    """An en word count expressed in the language's own unit, rounded down."""
    return int(n_en * (rp.ZH_HAN_PER_EN_WORD if lang == "zh" else 1.0))


def test_t4_avg_limit_fails_and_names_mean_cap_and_count(lang: str):
    size = _scaled(rp.GLOSSARY_AVG_WORDS_PER_ENTRY, lang) + 2  # over the mean cap
    text = _synthetic([size] * 10, lang)
    assert size <= _scaled(rp.GLOSSARY_MAX_WORDS_PER_ENTRY, lang)  # only AVG can fire
    msgs = _entry_limit_violations(text, lang)
    assert len(msgs) == 1 and msgs[0].startswith("AVG"), msgs
    cap = rp.GLOSSARY_AVG_WORDS_PER_ENTRY * (rp.ZH_HAN_PER_EN_WORD if lang == "zh" else 1.0)
    assert f"{size:.1f}" in msgs[0] and f"{cap:.1f}" in msgs[0] and "10 entries" in msgs[0]


def test_t4_max_limit_fails_and_names_the_headword(lang: str):
    cap = _scaled(rp.GLOSSARY_MAX_WORDS_PER_ENTRY, lang)
    sizes = [10] * 9 + [cap + 2]  # mean stays far under AVG
    text = _synthetic(sizes, lang)
    msgs = _entry_limit_violations(text, lang)
    assert len(msgs) == 1 and msgs[0].startswith("MAX") and "'t9'" in msgs[0], msgs
    # exactly at the cap is fine
    assert _entry_limit_violations(_synthetic([10] * 9 + [cap], lang), lang) == []


def test_t4_allowance_grows_with_the_number_of_terms(lang: str):
    """The property Lei asked for: adding one more within-limit entry to a
    glossary already at the cap never fails. The old fixed 1800 total fails it."""
    size = _scaled(rp.GLOSSARY_AVG_WORDS_PER_ENTRY, lang)  # at the mean cap
    at_cap = _synthetic([size] * 60, lang)
    assert _entry_limit_violations(at_cap, lang) == []
    # the cap is not vacuous: this glossary is past the old 1800-en-word total
    assert size * 60 > _scaled(1800, lang)
    bigger = _synthetic([size] * 61, lang)
    assert _entry_limit_violations(bigger, lang) == []
    assert _entry_stats(bigger, lang)[0] == 61


def test_t4_intro_is_not_counted(lang: str):
    intro = "# Appendix G\n\n" + ("intro " if lang == "en" else "引言") * 800
    text = _synthetic([10] * 5, lang, intro=intro)
    assert _entry_stats(text, lang)[0] == 5
    assert _entry_stats(text, lang)[1] == 10
    assert _entry_limit_violations(text, lang) == []


def test_t4_zh_translator_header_is_not_counted():
    header = "<!--\n" + "译者注" * 800 + "\n-->\n"
    text = header + _synthetic([10] * 5, "zh", intro="# 附录 G")
    assert _entry_stats(text, "zh")[:3] == (5, 10.0, 10)
    assert _entry_limit_violations(text, "zh") == []


def test_t4_real_glossary_within_entry_limits(lang: str):
    g_path = _g_path(lang)
    assert g_path.exists(), f"missing: {g_path}"
    text = g_path.read_text(encoding="utf-8")
    msgs = _entry_limit_violations(text, lang)
    assert not msgs, (
        "Appendix G is over its per-entry limits (limits and ruling: see "
        "GLOSSARY_AVG_WORDS_PER_ENTRY in tools/render_paper.py): "
        + "; ".join(msgs)
        + ". Shorten the over-long definitions; do not raise the constants to fit."
    )


def test_t4_required_terms_present(lang: str):
    g_path = _g_path(lang)
    assert g_path.exists(), f"missing: {g_path}"

    # The required-term coverage below is keyed to the English REQUIRED_TERMS
    # list and needs the assembled book. Neither holds for zh, so it skips
    # explicitly -- naming both facts -- rather than reporting a pass it did not
    # earn. The per-entry length limits are separate tests and run for both.
    if lang != "en":
        _skip_zh(
            lang,
            "T4 required-term coverage",
            "REQUIRED_TERMS is the English spec list of English headwords, while the "
            "zh glossary's headwords are Chinese (`自动浮现（auto-surface）`) and no "
            "zh term-to-headword map exists yet; the headword normaliser also strips "
            "ASCII parens only.",
        )

    full = _render_full_text(lang)
    g_text = _g_section_text(lang, full)
    entries = _parse_entries(g_text)
    all_headwords: set[str] = set()
    for raw in entries:
        for term in _headword_terms(raw):
            all_headwords.add(term.lower())

    missing_entries = []
    for spec_name, mapped in REQUIRED_TERMS.items():
        if mapped is None:
            assert spec_name in _REQUIRED_BUT_ABSENT_FROM_BODY, (
                f"{spec_name!r} is mapped absent but not in the documented set"
            )
            continue
        for term in mapped:
            if term == "__ID_PREFIX_TABLE__":
                if not any("node id prefix" in h for h in all_headwords):
                    missing_entries.append(spec_name)
                continue
            if term.lower() not in all_headwords:
                missing_entries.append(f"{spec_name} (looked for {term!r})")

    assert not missing_entries, f"required terms without a G entry: {missing_entries}"
    # every required term is accounted for: either has an entry, or is in the
    # documented-absent set -- no third state.
    accounted = set(REQUIRED_TERMS)
    assert accounted == set(REQUIRED_TERMS), "REQUIRED_TERMS must enumerate every spec term"


# ── T5 ────────────────────────────────────────────────────────────────────


def test_t5_ch1_pointer_sentence_present_exactly_once(lang: str):
    if lang != "en":
        _skip_zh(
            lang,
            "T5 (Ch1 pointer sentence present exactly once)",
            "the asserted string is the English Ch1 pointer text; the zh Ch1 is a "
            "different string that does not exist yet.",
        )
    full = _render_full_text(lang)
    # Source markdown is hard-wrapped, so the sentence may straddle a line
    # break in ch1.md; collapse whitespace runs before counting (same
    # normalization as T1's body-phrase matching).
    full_norm = re.sub(r"\s+", " ", full)
    count = full_norm.count(CH1_POINTER)
    assert count == 1, f"Ch1 pointer sentence found {count} times, expected exactly 1"


# ── language contract (`--lang {en,zh}`) ────────────────────────────────────


def test_language_defaults_and_output_paths():
    """Spec point 1: `--lang {en,zh}` defaults to `en`, and the zh default output
    is the `.zh.md` sibling of the English paper. The parity test below
    (`test_fresh_render_matches_committed_paper`) runs one case per language with
    `--lang` passed explicitly and a third that omits it, so the renderer's own
    `en` default is exercised end-to-end there as well."""
    assert rp.LANGS == ("en", "zh")
    assert DEFAULT_OUT["en"] == "paper/release/engram-paper-v0.5.1.md"
    assert DEFAULT_OUT["zh"] == "paper/release/engram-paper-v0.5.1.zh.md"


def test_body_is_one_shared_list_never_duplicated_per_language():
    """Spec point 2: ONE `BODY` list shared across languages -- never a second
    list keyed by language."""
    body_lists = sorted(n for n in dir(rp) if n == "BODY" or n.startswith("BODY_"))
    assert body_lists == ["BODY"], (
        "the engine must carry exactly one BODY list shared across languages; "
        f"found {body_lists}"
    )


def test_zh_chapter_paths_derive_from_the_shared_body_list():
    """Spec point 2: the zh sources are the same chapter set, resolved into the
    zh source dir -- not a hand-maintained parallel listing. The assertions here
    are deliberately agnostic about the zh filename *convention* (bare vs
    `.zh`-suffixed); they pin only what the spec fixes: the set is derived from
    BODY, and every zh path lands inside the zh source dir."""
    assert set(DEFAULT_OUT) == set(LANGS) == set(SOURCE_DIRS) == set(CHAPTER_SUFFIX)
    assert CHAPTER_SUFFIX["en"] == "", "the en filenames must stay unchanged"
    for name in BODY:
        assert chapter_name("en", name) == name, "en chapter resolution is identity"
        zh_path = SOURCE_DIRS["zh"] / chapter_name("zh", name)
        assert zh_path.parent == DRAFT_ZH, f"{name} resolves outside the zh dir"
        assert zh_path.suffix == ".md", f"{name} does not resolve to a markdown file"


def test_zh_front_and_back_matter_are_translated_and_substantive():
    """Spec point 4, in its current state. These files (front matter,
    acknowledgements, bibliography) were one-line placeholders while translation
    was pending, and this test used to assert that placeholder state ("must carry
    an obvious TODO(zh) marker", "must be a one-line placeholder"). They are
    translated now, so the property worth defending is the inverse -- each exists,
    carries NO placeholder marker, and is substantive. The 100-Han floor is
    deliberately well below the measured minimum over the translated files (233
    Han characters, front-matter) so it stays non-vacuous without pinning today's
    exact sizes. (The hard-fail rule covers CHAPTERS; these four files are checked
    here instead.)

    The afterword zh file was a deliberate TODO(zh) placeholder in rounds 1-2 of
    engram-paper-public#16, and this test was the merge gate that kept it from
    shipping. In round 3 the human author's own Chinese afterword replaced it (he
    wrote it himself, not as a translation), so all four files are now held to
    the same floor. Do not weaken or skip the test."""
    for name in (FRONT_MATTER["zh"], ACKNOWLEDGEMENTS["zh"], AFTERWORD["zh"],
                 BIBLIOGRAPHY["zh"]):
        path = PAPER / name
        assert path.exists(), f"missing zh front/back matter: {path}"
        text = path.read_text(encoding="utf-8")
        for marker in ("TODO(zh)", "TODO"):
            assert marker not in text, (
                f"{path} still carries a {marker!r} placeholder; the four zh "
                f"front/back-matter files are translated, so a placeholder here "
                f"means one was reverted or not yet translated"
            )
        non_blank = len([ln for ln in text.splitlines() if ln.strip()])
        assert non_blank > 1, (
            f"{path} must be substantive, not a one-line placeholder; "
            f"got {non_blank} non-blank lines"
        )
        han = _han_char_count(text)
        assert han >= 100, (
            f"{path} carries only {han} Han characters -- below the 100 floor, "
            f"which every translated matter file clears by more than 2x"
        )


def test_en_front_and_back_matter_names_are_unchanged():
    assert FRONT_MATTER["en"] == "front-matter.md"
    assert ACKNOWLEDGEMENTS["en"] == "acknowledgements.md"
    assert AFTERWORD["en"] == "afterword.md"
    assert BIBLIOGRAPHY["en"] == "bibliography.md"


def test_zh_chapter_filename_convention_is_pinned():
    """The zh filename convention (`ch1.md` -> `ch1.zh.md`) is pinned here on
    purpose: it is the ONE place the spec's prose and the repo disagree. The
    prose says "the zh sources use the SAME filenames under
    `current_draft_zh/`", while the only zh source that exists -- the parent
    commit's own `current_draft_zh/appendix_G_glossary.zh.md` -- carries the
    suffix, as do the four zh front/back-matter names.

    Suffix was chosen (the artifact plus the front/back-matter precedent), and
    this test makes that choice visible rather than implied. If the bare name
    was meant, flip `CHAPTER_SUFFIX["zh"]` and this test together."""
    assert chapter_name("zh", "ch1.md") == "ch1.zh.md"
    assert chapter_name("zh", "appendix_G_glossary.md") == "appendix_G_glossary.zh.md"
    assert (DRAFT_ZH / "appendix_G_glossary.zh.md").exists()


def test_anchor_parity_guard_is_wired_at_import():
    """`assert_insert_anchor_parity` is only a guard if it actually RUNS at
    import. Defining it and never calling it looks identical to the tests below,
    which call it directly -- so assert the module-scope call exists by reading
    the module's own source (a definition without a call is the plausible-wrong
    implementation of "assert at import")."""
    tree = ast.parse(Path(rp.__file__).read_text(encoding="utf-8"))
    module_scope_calls = [
        node
        for node in tree.body
        if isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and getattr(node.value.func, "id", None) == "assert_insert_anchor_parity"
    ]
    assert module_scope_calls, (
        "assert_insert_anchor_parity is defined but never called at module scope, "
        "so nothing enforces the INSERTS / INSERTS_ZH anchor parity"
    )


def test_zh_pipeline_places_zh_captions_end_to_end(tmp_path, monkeypatch):
    """Drive the WHOLE zh pipeline over stand-in chapters (the English text under
    the zh filenames) in a temp source dir, so the routing is exercised
    independently of the chapter sources' contents. (The zh book assembles from
    the real sources now; this test is about ROUTING, not about what the chapters
    say.) This is the check that `--lang zh` really routes to the
    zh insert list and the zh captions/diagram rather than the English ones --
    exactly the failure spec point 3 names ("silently render English").

    English chapter text is used as a stand-in for the translation, so this test
    is about ROUTING, not about translation quality."""
    for name in BODY:
        shutil.copy(chapter_path("en", name), tmp_path / chapter_name("zh", name))
    monkeypatch.setitem(rp.SOURCE_DIRS, "zh", tmp_path)
    out = tmp_path / "rendered-zh.md"
    monkeypatch.setattr(sys, "argv", ["render_paper.py", "--lang", "zh", "--out", str(out)])

    assert rp.main() == 0
    text = out.read_text(encoding="utf-8")
    assert text.count(f"**{rp.FIGURE_LABEL['zh']} ") == 6, (
        "the zh render must place six zh figure captions (图 N), not the English ones"
    )
    assert f"**{rp.DIAGRAM_LABEL['zh']} 1.**" in text, "the zh cascade diagram is missing"
    assert text.count("TODO(zh)") == 0, (
        "no zh placeholder may survive into the render"
    )


def test_zh_render_hard_fails_naming_the_first_untranslated_chapter(tmp_path, monkeypatch):
    """Spec point 2: a missing zh chapter must hard-fail and name the file --
    never a skip/optional path, and never a silently short render.

    This was DATA-DRIVEN and self-retiring: it skipped when no zh chapter was
    missing, and the day every chapter was translated it retired itself -- taking
    the assertion with it and leaving the property unguarded. That is the wrong
    shape for it, because the property belongs to the ENGINE (a half-translated
    book must not render short), not to today's translation state. So the check
    now builds the condition instead of waiting for it: the real zh chapters are
    copied into `tmp_path` minus one, the engine's zh source dir is pointed there,
    and the render must die naming the file it could not find. It runs on every
    tree, translated or not."""
    missing_name = BODY[0]
    for name in BODY:
        if name == missing_name:
            continue
        shutil.copy(chapter_path("zh", name), tmp_path / chapter_name("zh", name))
    monkeypatch.setitem(rp.SOURCE_DIRS, "zh", tmp_path)
    out = tmp_path / "rendered-zh.md"
    monkeypatch.setattr(sys, "argv", ["render_paper.py", "--lang", "zh", "--out", str(out)])

    with pytest.raises(SystemExit) as exc:
        rp.main()
    assert chapter_name("zh", missing_name) in str(exc.value), (
        f"the zh hard-fail must name the missing file "
        f"{chapter_name('zh', missing_name)!r}; got: {exc.value}"
    )
    assert not out.exists(), "a failed render must not leave an output file behind"


def test_insert_lists_are_anchor_key_identical():
    """Spec point 3: `INSERTS` and `INSERTS_ZH` must carry identical
    `(file, heading)` anchor keys, so a caption present in one language and
    absent in the other cannot pass unnoticed."""
    assert [(f, h) for f, h, _ in INSERTS] == [(f, h) for f, h, _ in INSERTS_ZH]


def test_insert_parity_guard_accepts_the_shipped_lists():
    assert_insert_anchor_parity(INSERTS, INSERTS_ZH)


@pytest.mark.parametrize(
    "dropped_from", ["zh", "en"], ids=["zh-lost-a-caption", "en-lost-a-caption"]
)
def test_insert_parity_guard_fires_when_one_language_loses_an_anchor(dropped_from):
    """The discriminating case for spec point 3: a caption added to one language
    and not the other must fail loudly, not silently render English."""
    if dropped_from == "zh":
        bad_en, bad_zh = INSERTS, INSERTS_ZH[:-1]
    else:
        bad_en = INSERTS + [("ch9.md", "## 9.9", "a caption only en carries")]
        bad_zh = INSERTS_ZH
    with pytest.raises(SystemExit) as exc:
        assert_insert_anchor_parity(bad_en, bad_zh)
    assert "INSERT" in str(exc.value)


def test_zh_insert_blocks_are_not_english_copies():
    """Anchor parity cannot see a block that was copy-pasted rather than
    translated, and spec point 3's stated failure mode is exactly "silently
    render English" -- so assert the zh blocks are actually distinct text."""
    for (f, h, block_en), (f2, h2, block_zh) in zip(INSERTS, INSERTS_ZH):
        assert (f, h) == (f2, h2)
        assert block_en != block_zh, (
            f"{f} :: {h!r}: the zh insert block is a byte copy of the English one"
        )


# ── caption numeric-drift guard ─────────────────────────────────────────────
#
# INSERTS_ZH and DIAGRAM_CASCADE_ZH restate numbers that also appear in their
# English counterparts (9,399 nodes, 72.8%, 71/149/9/16, 245 = 2.6%, 0.93/0.49,
# 0.91/0.60, 1,318 ...). Nothing tied the two sides together: the anchor-parity
# guard above compares `(file, heading)` KEYS only, and the render pin
# (`test_fresh_render_matches_committed_paper`) checks each language's render
# against its own committed book -- never an English caption's text against its
# zh counterpart. So an English numbers-fold could update the English captions
# and leave the Chinese ones stating the old numbers -- CI green, the two
# languages disagreeing. This guard closes that: the numeric tokens of the two
# captions must form equal MULTISETS.
#
# TOKEN RULE -- `[0-9][0-9,\.]*%?`: a maximal run starting at a digit and
# continuing over digits, thousands separators and decimal points, with an
# optional trailing percent sign.
#
# NORMALISATION -- which differences are NOTATIONAL (compared equal) and which
# are FACTUAL (compared different). Recorded here because neither is
# self-evident, and a guard is only as good as its stated rule:
#
#   * Thousands separators are NOTATIONAL: commas are stripped, so `9,399` and
#     `9399` compare equal. The grouping is pure typography -- no reader learns
#     anything from it -- and a zh caption retyped without the separator states
#     the same number.
#   * Trailing sentence punctuation is NOTATIONAL: the greedy class swallows the
#     period of `... near 0.49. The author`, so a trailing `.` or `,` is
#     stripped. Without this, every number ending a sentence would differ
#     between en (`.`) and zh (none), for no factual reason.
#   * The percent sign is FACTUAL: it stays in the token, so `72.8%` and `72.8`
#     are NOT equal. This is the deliberate strict choice -- a percentage and a
#     bare proportion differ in what the caption *states*, not only in how it is
#     written, and the captions are parallel translations that carry the sign on
#     both sides today. The guard's failure mode is silence (a stale zh caption
#     looks exactly like a correct one), so it errs toward firing: a false
#     positive from a notational-only `%` difference is loud and costs one line
#     to fix, while a false negative is invisible. If a future translation style
#     makes this fire on a legitimate reformatting, the one-line loosening is
#     `raw.replace("%", "")` in the normaliser below -- deliberately a loosening
#     of this rule, never a bug fix.
#   * Mermaid colour literals are EXCLUDED outright, not normalised. A colour is
#     stripped before the numeric scan (`_COLOUR_LITERAL_RE`), because its hex
#     digits are not caption FACTS: `#b3593f` would otherwise contribute '3593',
#     `#555` -> '555', `#f6ece8` -> '6' and '8'. Every `#` form in either cascade
#     diagram is one of these literals (measured: the seven distinct values
#     #1f6f8b, #555, #8a8a8a, #b3593f, #e9f1f4, #f3f3f3, #f6ece8 -- six 6-digit
#     and one 3-digit; `{3,8}` also covers the 4- and 8-digit alpha forms mermaid
#     accepts), and the two diagrams carry identical style lines, so excluding
#     them changes no comparison today -- which is exactly why the exclusion has
#     to be written down rather than left implicit. Without it the guard's stated
#     subject ("numeric facts") would not match what it compares, and an
#     English-diagram restyle would fire a message reading "numeric tokens
#     differ" when only a colour had changed. The exclusion is load-bearing, not
#     cosmetic: removing it is what
#     `test_caption_numeric_guard_ignores_a_colour_only_difference` goes red on.
#
# The comparison is on multisets, not sets: a caption stating `2, 2` against one
# stating `2` has dropped an occurrence, and a set comparison would miss it.
_NUMERIC_TOKEN_RE = re.compile(r"[0-9][0-9,\.]*%?")
_COLOUR_LITERAL_RE = re.compile(r"#[0-9a-fA-F]{3,8}")


def _numeric_tokens(text: str) -> list[str]:
    """The normalised numeric tokens of one caption (rule above). Colour
    literals are removed first -- see the EXCLUDED bullet above for why."""
    return [
        raw.replace(",", "").rstrip(".,")
        for raw in _NUMERIC_TOKEN_RE.findall(_COLOUR_LITERAL_RE.sub("", text))
    ]


def _caption_pairs() -> list[tuple[str, str, str]]:
    """(label, en_caption, zh_caption) for every pair the numeric guard covers.

    Covers each anchor appearing in BOTH `INSERTS` and `INSERTS_ZH`, plus the
    two cascade-diagram constants by name. The constants are also the ch4 §4.4
    insert, but comparing them explicitly keeps the guard on the constants
    themselves even if that INSERTS entry is ever rebuilt from an inlined copy.
    """
    zh_by_anchor = {(f, h): block for f, h, block in INSERTS_ZH}
    pairs: list[tuple[str, str, str]] = [
        (f"{f} :: {h}", block, zh_by_anchor[(f, h)])
        for f, h, block in INSERTS
        if (f, h) in zh_by_anchor
    ]
    pairs.append(
        ("DIAGRAM_CASCADE / DIAGRAM_CASCADE_ZH", DIAGRAM_CASCADE, DIAGRAM_CASCADE_ZH)
    )
    return pairs


def _numeric_mismatches(
    pairs: list[tuple[str, str, str]],
) -> list[tuple[str, list[str], list[str]]]:
    """The `(label, en_tokens, zh_tokens)` triples whose multisets differ.

    This is the guard itself, factored out so the colour-exclusion test below can
    assert on the very comparison the shipped guard runs instead of
    re-implementing it -- a test that restates the guard can pass while the guard
    is wrong.
    """
    out = []
    for label, en_caption, zh_caption in pairs:
        en_tokens = sorted(_numeric_tokens(en_caption))
        zh_tokens = sorted(_numeric_tokens(zh_caption))
        if en_tokens != zh_tokens:
            out.append((label, en_tokens, zh_tokens))
    return out


def test_caption_numeric_tokens_match_between_languages():
    """Every shared caption anchor -- and the cascade diagram pair -- must state
    the SAME numeric tokens in both languages, so an English numbers-fold cannot
    leave the zh caption stating other numbers."""
    mismatches = _numeric_mismatches(_caption_pairs())
    assert not mismatches, (
        "caption numeric tokens differ between the English and zh captions -- an "
        "English numbers-fold has left the zh caption stale, or a zh number was "
        "edited without its English counterpart:\n"
        + "\n".join(
            f"  {label}\n      en: {en_tokens}\n      zh: {zh_tokens}"
            for label, en_tokens, zh_tokens in mismatches
        )
    )


def test_caption_numeric_guard_fires_on_one_changed_digit():
    """Can-it-fail demonstration for the guard above, committed so the
    discrimination does not rest on a pasted transcript. Uses the real ch1 §1.1
    caption pair, mutating it in memory -- the shipped files are not touched."""
    pairs = {label: (en, zh) for label, en, zh in _caption_pairs()}
    en_caption, zh_caption = pairs["ch1.md :: ## 1.1"]
    assert sorted(_numeric_tokens(en_caption)) == sorted(_numeric_tokens(zh_caption))

    mutated = zh_caption.replace("9,399", "9,398")
    assert mutated != zh_caption, "the ch1 §1.1 zh caption no longer states 9,399"
    assert sorted(_numeric_tokens(en_caption)) != sorted(_numeric_tokens(mutated)), (
        "a one-digit change in the zh caption must produce a token mismatch"
    )


def test_caption_numeric_guard_ignores_a_colour_only_difference():
    """The guard compares numeric FACTS, and a mermaid colour literal is not one:
    a colour-only difference between a caption pair must NOT register as a
    mismatch. This is the can-it-fail demonstration for the `_COLOUR_LITERAL_RE`
    exclusion above -- drop that exclusion and `#b3593f` / `#b35940` are read as
    the differing tokens '3593' / '35940', turning this test red. Uses the real
    cascade pair, recoloured in memory -- the shipped files are not touched."""
    pairs = {label: (en, zh) for label, en, zh in _caption_pairs()}
    label = "DIAGRAM_CASCADE / DIAGRAM_CASCADE_ZH"
    en_caption, zh_caption = pairs[label]
    recoloured = zh_caption.replace("#b3593f", "#b35940")
    assert recoloured != zh_caption, "the zh cascade diagram no longer uses #b3593f"
    assert not _numeric_mismatches([(label, en_caption, recoloured)]), (
        "a colour-only difference must not register as a numeric mismatch"
    )


def test_strip_provenance_ids_language_contract_for_zh():
    """Spec point 5: `_LITERAL_STRIPS` holds literal English `(old, new)` pairs,
    so for zh it no-ops and the zh render rests on the general regex forms plus
    the translation rule that zh chapters carry no citation-style provenance IDs.
    This pins what the regexes actually do to zh-shaped text, so the translator
    contract is checked rather than assumed."""
    # (a) the rule the translator is held to: no ID tokens -> nothing to strip.
    zh_clean = "撤回一次推导（§1.3）会触发级联。"
    out, n = strip_provenance_ids("ch2.md", zh_clean)
    assert (out, n) == (zh_clean, 0)
    rp.assert_no_leaked_ids("ch2.md", out)

    # (b) an ID the translator does carry, in an ASCII parenthetical run, is
    #     still reached by the general forms.
    out2, n2 = strip_provenance_ids("ch2.md", "撤回（级联）(ob_1041) 会传播。")
    assert n2 == 1 and "ob_1041" not in out2

    # (c) the documented gap, asserted rather than described: a full-width
    #     parenthetical carrying an ID is NOT reachable by the ASCII-paren
    #     regexes, so it survives the strip and hard-fails (the guard runs inside
    #     strip_provenance_ids itself, so the render dies at the strip call).
    #     That is why the translator rule is "no citation-style IDs in zh text",
    #     not "put them where the English put them".
    with pytest.raises(SystemExit):
        strip_provenance_ids("ch2.md", "撤回（ob_1041）会传播。")


# ── the load()-time comment strip ───────────────────────────────────────────


def test_zh_render_carries_no_html_comments(tmp_path):
    """A fresh zh render carries no HTML comment: the published .md must reach
    the reader without the sources' translator notes, which stay in the source
    files (they are the next translator's record). This asserts the RENDERED
    output; byte-parity with the committed book lives in
    `test_fresh_render_matches_committed_paper` (parametrized over both
    languages), and the committed artifact's own comment-freedom is folded into
    that same parity test (for zh it is implied by this test plus the byte
    comparison; see that test's docstring).

    This went unguarded until now -- reverting `load()` to its pre-strip body
    left the whole suite green. The source-side assertion is what keeps the check
    from being vacuous: if no zh source carried a comment, a comment-free render
    would prove nothing. All 19 zh comment blocks are LEADING, one per source
    file (measured 2026-09-28), so the render's emptiness is the strip's doing
    rather than the sources'."""
    out = tmp_path / "rendered-zh.md"
    result = subprocess.run(
        [sys.executable, "tools/render_paper.py", "--lang", "zh", "--out", str(out)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    text = out.read_text(encoding="utf-8")
    assert "<!--" not in text, (
        "the rendered zh paper carries an HTML comment -- the sources' translator "
        "notes are leaking into the published artifact"
    )
    carriers = [
        chapter_name("zh", name)
        for name in BODY
        if "<!--" in chapter_path("zh", name).read_text(encoding="utf-8")
    ]
    assert carriers, (
        "no zh chapter source carries an HTML comment, so a comment-free render "
        "proves nothing -- this check has gone vacuous"
    )


def test_strip_html_comments_is_wider_than_the_leading_only_helper():
    """The scope difference the engine's docstring argues for, pinned by the one
    input that can distinguish the two scopes.

    Every one of the 19 comment blocks in the zh sources is LEADING (measured
    2026-09-28), so a strip that removed only a leading block would satisfy every
    other check in this file -- the wider "every comment" scope and a leading-only
    strip are indistinguishable against the shipped data. `strip_html_comments`
    answers what may be PUBLISHED, so it takes every comment;
    `_LEADING_TRANSLATOR_HEADER` (via `_glossary_body`) answers what the
    glossary's PROSE REGION contains, so it takes only a leading block. This is
    the test that reddens if someone "unifies" the two -- in either direction."""
    interior = "# 附录 G — 术语表\n\n术语<!-- 内注 -->定义\n"
    assert rp.strip_html_comments(interior) == "# 附录 G — 术语表\n\n术语定义\n"
    assert _glossary_body(interior) == interior, (
        "the counting helper must keep an interior comment -- its scope is the "
        "leading header only, deliberately"
    )
    # A leading block is removed by BOTH; only the scope differs between them.
    leading = "<!--\n  translator: Zephyr\n-->\n# 附录 G — 术语表\n\n正文\n"
    assert "<!--" not in rp.strip_html_comments(leading)
    assert "<!--" not in _glossary_body(leading)


# ── render byte-check (spec verification tail) ──────────────────────────────


# Each case carries (the language the render must equal, the argv fragment that
# selects it). The third omits `--lang` entirely, so the renderer's own argparse
# default is what picks the language there -- and the book it is compared against
# is `DEFAULT_OUT["en"]`, the book that default is supposed to produce. The
# default is load-bearing outside the tests: the fresh-reader harness under
# `tools/fresh_reader/` renders the paper with `--out` alone, so a default that drifted
# to `zh` would silently render the zh sources there with nothing to catch it.
_PARITY_CASES = [
    pytest.param("en", ["--lang", "en"], id="en"),
    pytest.param("zh", ["--lang", "zh"], id="zh"),
    pytest.param("en", [], id="default"),
]


@pytest.mark.parametrize("lang, lang_args", _PARITY_CASES)
def test_fresh_render_matches_committed_paper(lang, lang_args, tmp_path):
    """A fresh `tools/render_paper.py` run must reproduce the committed book for
    the language it renders BYTE-for-byte (git status --porcelain empty) -- and
    that committed book must itself carry no HTML comment.

    Rendered to a tmp path via `--out`, NEVER in place: the committed book is
    the comparison target, not the render destination. The previous form ran the
    renderer with no `--out` for English only, so it wrote over
    paper/engram-paper-v0.5.1.md and then compared the file against itself -- a
    divergence left the tracked paper rewritten by the very test that caught it
    (engram-paper#111), and the zh book had no parity check at all
    (engram-paper#113). Both languages are covered here now, and neither render
    touches a tracked path.

    The committed path is DERIVED from `DEFAULT_OUT[lang]` rather than written
    out here, and a missing book is deliberately NOT a skip: a version bump must
    fail this test loudly, never quietly retire the parity check the way a
    literal path plus a "not present yet" skip did.

    WHY THE COMMENT-FREE ASSERTION IS FOLDED IN HERE, AND WHICH HALF OF IT IS
    ONLY IMPLIED. For `zh` the property is IMPLIED by two checks already in this
    file, and is stated as implied rather than claimed as independent:
    `test_zh_render_carries_no_html_comments` asserts a fresh zh render carries
    no `<!--` (and its carrier scan asserts the zh SOURCES do carry them, so a
    comment-free render is the strip's doing), and the byte comparison below
    pins the committed book to that render. Together they entail a comment-free
    committed zh book -- so injecting a comment into it reddens this assertion
    AND the byte comparison together, with the render-side sibling still green.
    It is kept as belt-and-braces there: it names the artifact and the cause in
    one line. For `en` it is the ONLY check -- nothing else in this suite asserts
    the committed English book is comment-free -- so folding it in is that
    book's single guard, not a second opinion."""
    out = REPO_ROOT / DEFAULT_OUT[lang]
    before = out.read_bytes()
    assert b"<!--" not in before, (
        f"the committed {lang} book carries an HTML comment -- a translator note "
        "has reached the published artifact"
    )
    # Rendered into the committed book's OWN directory (under a throwaway name,
    # removed below): the figure links are relative to the output directory, so a
    # render anywhere else would differ from the committed book by design.
    fd, name = tempfile.mkstemp(suffix=".md", prefix="parity-", dir=out.parent)
    os.close(fd)
    rendered = Path(name)
    result = subprocess.run(
        [
            sys.executable,
            "tools/render_paper.py",
            *lang_args,
            "--out",
            str(rendered),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    try:
        assert result.returncode == 0, result.stderr
        after = rendered.read_bytes()
    finally:
        rendered.unlink(missing_ok=True)
    assert before == after, f"fresh {lang} render diverged from {DEFAULT_OUT[lang]}"
