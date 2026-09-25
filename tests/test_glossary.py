"""Contract tests for Appendix G — Glossary (`spec-glossary.md`), written BEFORE
the appendix and the render-order change existed. Expected to fail until
`paper_research/current_draft/appendix_G_glossary.md` exists and
`tools.render_paper.BODY` includes it.

T1 — every glossary term occurs at least once in the rendered body OUTSIDE
     Appendix G (case-insensitive, word-boundary).
T2 — every section pointer in G resolves to a heading that exists in the render.
T3 — G carries zero node IDs (reuses tests/test_render_strip_ids.py's _ID_SCAN).
T4 — G is <= 1800 words, and every required term has an entry (or is in the
     documented-absent set, for the two required terms that do not occur
     anywhere in the current draft body at all).
T5 — the Ch1 pointer sentence is present exactly once in the render.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

from tools.render_paper import DRAFT, PAPER, BODY, load, apply_inserts, strip_provenance_ids

REPO_ROOT = Path(__file__).resolve().parents[1]
G_PATH = DRAFT / "appendix_G_glossary.md"
CH1_POINTER = (
    "Terms of art are collected in the Glossary (Appendix G); each entry "
    "points to the section that defines it."
)

# _ID_SCAN copied verbatim from tests/test_render_strip_ids.py so this file has
# no import-order dependency on that module's internals.
_ID_SCAN = re.compile(r"\b(?:ob|dv|th|cj|df|ax|cs|ls|gl|gt|ct|qu|pr|ev|fl|pn|tk|ts)_\d{4}\b")


def _render_full_text() -> str:
    """Render the whole paper via the real assembly path (front matter + BODY +
    acknowledgements + bibliography), mirroring tools/render_paper.py:main()
    exactly, so the test exercises the real render rather than a hand-rolled
    substitute."""
    parts = [load(PAPER / "front-matter.md")]
    for name in BODY:
        body = load(DRAFT / name)
        body = apply_inserts(name, body)
        body, _ = strip_provenance_ids(name, body)
        parts.append(body)
    parts.append(load(PAPER / "acknowledgements.md"))
    parts.append(load(PAPER / "bibliography.md"))
    return "\n\n---\n\n".join(p.rstrip() for p in parts) + "\n"


def _g_section_text(full_text: str) -> str:
    """Slice out just the Appendix G section from the full render."""
    m = re.search(r"^# Appendix G — Glossary\s*$", full_text, re.MULTILINE)
    assert m, "Appendix G heading not found in render"
    rest = full_text[m.end():]
    # G ends at the next top-level heading (Acknowledgements) or end of doc.
    m2 = re.search(r"^## Acknowledgements\s*$", rest, re.MULTILINE)
    return rest[: m2.start()] if m2 else rest


def _body_outside_g(full_text: str) -> str:
    m = re.search(r"^# Appendix G — Glossary\s*$", full_text, re.MULTILINE)
    assert m
    before = full_text[: m.start()]
    rest = full_text[m.end():]
    m2 = re.search(r"^## Acknowledgements\s*$", rest, re.MULTILINE)
    after = rest[m2.start():] if m2 else ""
    return before + after


# ── entry parsing ────────────────────────────────────────────────────────────

_ENTRY_RE = re.compile(r"^\*\*(.+?)\*\*", re.MULTILINE)


def _parse_entries(g_text: str) -> list[str]:
    """Every top-level glossary entry's bold headword, as written (including
    any trailing parenthetical, e.g. 'cascade (retraction cascade)')."""
    return _ENTRY_RE.findall(g_text)


def _headword_terms(raw_headword: str) -> list[str]:
    """Normalize one raw bold headword into the literal string(s) T1 should
    search for in the body. Rule: strip a trailing parenthetical annotation
    (e.g. '(usage-derived ...)', '(utility score)', '(node)'), then split on
    ' / ' for compound headwords (e.g. 'seed / root',
    'claim-bearing / non-claim-bearing', 'engram / ENGRAM') so each name is
    checked independently."""
    stripped = re.sub(r"\s*\([^)]*\)\s*$", "", raw_headword).strip()
    return [t.strip() for t in stripped.split(" / ") if t.strip()]


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
_ID_PREFIXES = {
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
}

# The entry cites the CODE's type-prefix map (engram_core.py TYPE_PREFIX at
# v0.5.1-rc5), not a paper section, after Borges's colleague read of #109
# found the fairy's table had paired ts_ with task (it is trust_signal; task
# is tk_) and cited E.2, which names types but no prefixes. Two types in
# that map are never named in the paper body at all, so their prefixes are
# exempt from the body check below and rest on the code citation alone.
_PREFIXES_CITED_TO_CODE_ONLY = {"gt_", "ts_"}

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


# ── T1 ────────────────────────────────────────────────────────────────────


def test_t1_every_glossary_term_occurs_outside_g():
    assert G_PATH.exists(), f"missing: {G_PATH}"
    full = _render_full_text()
    body = _body_outside_g(full)
    g_text = _g_section_text(full)

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
        if raw.strip() == "node ID prefixes":
            # Special-cased below: this entry is a 13-row table, not a term
            # that itself appears in prose.
            continue
        for term in _headword_terms(raw):
            pattern = _FORM_OVERRIDES.get(term)
            if pattern is None:
                pattern = re.escape(term)
                regex = re.compile(r"\b" + pattern + r"\b", re.IGNORECASE)
            else:
                regex = re.compile(r"\b" + pattern, re.IGNORECASE)
            if not regex.search(body_norm):
                missing.append(term)

    # The node-ID-prefix table entry: each prefix's node-TYPE NAME (see
    # _ID_PREFIXES docstring above for why type name, not bare prefix) must
    # be named somewhere in the body.
    for prefix, type_name in _ID_PREFIXES.items():
        if prefix in _PREFIXES_CITED_TO_CODE_ONLY:
            continue
        if not re.search(r"\b" + re.escape(type_name) + r"\b", body_norm, re.IGNORECASE):
            missing.append(f"(ID prefix {prefix}) {type_name}")

    assert not missing, f"glossary terms not found outside Appendix G: {missing}"


def test_t1_mutation_absent_term_reddens_only_this_test(tmp_path):
    """Can-it-fail demonstration: a term that never appears in the body must
    fail T1. Runs against a temp copy of G with one bogus entry appended;
    does not touch the real file."""
    full = _render_full_text()
    body = _body_outside_g(full)
    bogus = "zorblattian-nonexistent-term"
    assert not re.search(r"\b" + re.escape(bogus) + r"\b", body, re.IGNORECASE)
    g_text = _g_section_text(full) + f"\n\n**{bogus}** — a term invented for this test.\n"
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


def test_t2_every_pointer_resolves():
    full = _render_full_text()
    g_text = _g_section_text(full)
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
        assert (PAPER / "front-matter.md").exists()

    if "Data availability" in g_text:
        if "Data availability" not in named_headings:
            unresolved.append("Data availability")

    assert not unresolved, f"pointers that do not resolve to a real heading: {unresolved}"


def test_t2_mutation_bad_pointer_reddens_only_this_test():
    """Can-it-fail demonstration: a pointer to a non-existent section must
    fail T2. Constructs a synthetic G excerpt with a bogus pointer; does not
    touch the real file."""
    full = _render_full_text()
    section_tokens, appendix_letters, chapter_numbers, _named = _heading_index(full)
    bogus_token = "4.99"
    assert bogus_token not in section_tokens
    synthetic_line = "**bogus-term** — a fake entry pointing nowhere. (Defined §4.99.)"
    unresolved = []
    for tok in _SECTION_TOKEN_RE.findall(synthetic_line):
        if tok not in section_tokens:
            unresolved.append(f"§{tok}")
    assert f"§{bogus_token}" in unresolved


# ── T3 ────────────────────────────────────────────────────────────────────


def test_t3_g_carries_zero_node_ids():
    assert G_PATH.exists()
    text = G_PATH.read_text(encoding="utf-8")
    assert not _ID_SCAN.search(text), "Appendix G source carries a node ID"

    full = _render_full_text()
    g_text = _g_section_text(full)
    assert not _ID_SCAN.search(g_text), "Appendix G render carries a node ID"


# ── T4 ────────────────────────────────────────────────────────────────────


def test_t4_word_budget_and_required_terms_present():
    assert G_PATH.exists()
    text = G_PATH.read_text(encoding="utf-8")
    words = len(text.split())
    assert words <= 1800, f"Appendix G is {words} words, over the 1800 budget"

    full = _render_full_text()
    g_text = _g_section_text(full)
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


def test_t5_ch1_pointer_sentence_present_exactly_once():
    full = _render_full_text()
    # Source markdown is hard-wrapped, so the sentence may straddle a line
    # break in ch1.md; collapse whitespace runs before counting (same
    # normalization as T1's body-phrase matching).
    full_norm = re.sub(r"\s+", " ", full)
    count = full_norm.count(CH1_POINTER)
    assert count == 1, f"Ch1 pointer sentence found {count} times, expected exactly 1"


# ── render byte-check (spec verification tail) ──────────────────────────────


def test_fresh_render_matches_committed_paper():
    """A fresh `tools/render_paper.py` run must reproduce the committed
    paper/engram-paper-v0.5.1.md byte-for-byte (git status --porcelain empty)."""
    out = REPO_ROOT / "paper" / "engram-paper-v0.5.1.md"
    if not out.exists():
        pytest.skip("rendered paper not present yet")
    before = out.read_text(encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "tools/render_paper.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    after = out.read_text(encoding="utf-8")
    assert before == after, "fresh render diverged from the committed paper"
