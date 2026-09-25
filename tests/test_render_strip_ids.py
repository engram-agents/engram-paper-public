"""Contract tests for the render-side citation-ID strip (Lei's 2026-09-23 ruling,
`spec-strip.md`) — written BEFORE the implementation change. Expected to fail until
`tools.render_paper` grows the extended `STRIP_PROVENANCE_IDS_IN` set and the new
forms B-G described in the spec.

Node IDs used as DATA POINTS (a real node cited as a worked example: Chapter 6,
Appendix A, most of Appendix E) stay in the render. CITATION-STYLE IDs (an ID
standing in for a citation, in ch1-5/ch7, Appendix B/C/D, and one stray occurrence
in Appendix E — 2026-09-23 fold, Borges) are removed from the render only — the
source chapters keep every ID as provenance. `df_*` labels are never stripped.

Appendix F (added 2026-09-24, Lei's appendix-f-lucy spec) is a tenth strip-set
file, not a new category: its design-history text was moved verbatim OUT OF
Appendix D, so it carries the same citation-style `(ob_0645)` that was already
stripped while that text lived in D.4, and it inherits D's strip-set membership
rather than being independently classified.

Every REAL-string example below was grepped directly from
`paper_research/current_draft/*.md` at base commit 049d6d0a (see spec §2) — none
are invented. Line/file citations are given in comments so a source edit that
removes the phrase is easy to re-locate.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tools.render_paper import DRAFT, strip_provenance_ids

DRAFT_FILES = [
    "ch0_abstract.md", "ch1.md", "ch2.md", "ch3.md", "ch4.md",
    "ch5.md", "ch6.md", "ch7.md", "ch8.md",
    "appendix_A_independence.md", "appendix_B_c3_survey.md",
    "appendix_C_autorecall_ranking.md", "appendix_D_relational_identity.md",
    "appendix_E_techspec.md",
]

_ID_SCAN = re.compile(r"\b(?:ob|dv|cj|ax|cs|ls|gl|df|pn|qu|ev|fl|ts)_\d{4}\b")

# The 2026-09-23 ruling fixed nine files; 2026-09-24 adds a tenth,
# appendix_F_lucy.md, split out of Appendix D on that date (see module
# docstring) -- it inherits D's stripping rather than being independently
# classified as citation-style vs data-point.
NEW_STRIP_FILES = {
    "ch1.md", "ch2.md", "ch3.md", "ch4.md", "ch5.md", "ch7.md",
    "appendix_B_c3_survey.md", "appendix_C_autorecall_ranking.md",
    "appendix_D_relational_identity.md", "appendix_E_techspec.md",
    "appendix_F_lucy.md",
}


# ── 0. The strip set itself, and the two files that must carry zero IDs ─────


def test_strip_set_is_the_spec_nine_plus_appendix_f():
    from tools.render_paper import STRIP_PROVENANCE_IDS_IN

    assert STRIP_PROVENANCE_IDS_IN == NEW_STRIP_FILES


@pytest.mark.parametrize("name", ["ch0_abstract.md", "ch8.md", "appendix_G_glossary.md"])
def test_ch0_and_ch8_carry_no_ids(name):
    """Spec §2 step 1: only add these to the strip set if they actually carry
    IDs. Measured empirically at base commit: neither does. appendix_G_glossary.md
    (spec-glossary.md) is added under the same rule: G must carry zero node IDs
    of any kind, and since it is deliberately NOT added to
    STRIP_PROVENANCE_IDS_IN, a stray ID in G must fail this check loudly rather
    than being silently stripped by the renderer."""
    path = DRAFT / name
    if not path.exists():
        pytest.skip(f"source moved: {path}")
    text = path.read_text(encoding="utf-8")
    assert not _ID_SCAN.search(text), (
        f"{name} carries an ID after all — add it to STRIP_PROVENANCE_IDS_IN"
    )


# ── A. (ID), (ID SEP ID ...) → paren removed entirely ───────────────────────

FORM_A = [
    # ch2.md:27 "the substrate... (ob_2544)"
    ("(ob_2544)", ""),
    # ch7.md:83 "one resting on abundant evidence and one on almost none (dv_0965 → dv_1289)."
    (" (dv_0965 → dv_1289).", "."),
    # ch7.md:94-95 "unreliable sources (ob_1064–\nob_1067)."
    (" (ob_1064–\nob_1067).", "."),
    # ch7.md:176 "The argument (ob_1176–ob_1183, dv_0486) is that"
    (" (ob_1176–ob_1183, dv_0486) is", " is"),
    # appendix_C:67 "an additive blend\n(ob_2017):\n\n```"
    ("an additive blend\n(ob_2017):\n\n```", "an additive blend:\n\n```"),
]


@pytest.mark.parametrize("text_in,expected", FORM_A)
def test_form_a_full_paren_removed(text_in, expected):
    text, n = strip_provenance_ids("ch2.md", text_in)
    assert text == expected
    assert n >= 1


def test_form_a_colon_after_paren_kept():
    # ch4.md:373 / appendix_C:67: "(ob_2017):" -> ":"
    text, n = strip_provenance_ids("ch4.md", "utility score (ob_2017): the substrate")
    assert text == "utility score: the substrate"
    assert n == 1


def test_form_a_appendix_e_stray_citation_stripped():
    # appendix_E_techspec.md:208 (2026-09-23 fold, Borges): the same
    # dv_0615 "eight load-bearing primitives" citation already stripped
    # from Ch4 §4.2, missed on the first pass because Appendix E was
    # entirely outside the strip set.
    text_in = (
        "- The eight load-bearing **primitives** (dv_0615): typed nodes, "
        "typed edges, provenance,"
    )
    text, n = strip_provenance_ids("appendix_E_techspec.md", text_in)
    assert text == (
        "- The eight load-bearing **primitives**: typed nodes, "
        "typed edges, provenance,"
    )
    assert n == 1


def test_form_a_appendix_e_real_line_present_in_real_source():
    """Guards against silent no-op: if a source edit removes or rewords the
    line, this fails loudly instead of the added strip-set membership
    quietly matching nothing."""
    path = DRAFT / "appendix_E_techspec.md"
    if not path.exists():
        pytest.skip(f"source moved: {path}")
    text = path.read_text(encoding="utf-8")
    assert "The eight load-bearing **primitives** (dv_0615):" in text


# ── B. (... SEP ID) / (... SEP ID/ID) → trailing IDs + separator dropped ───

FORM_B = [
    # appendix_B_c3_survey.md:260
    ("operational binding (Ch4 §4.4, dv_0606/dv_0612), and",
     "operational binding (Ch4 §4.4), and"),
    # ch5.md:94
    ("*history* (Lei's history-tree view; ob_1657, dv_0597).",
     "*history* (Lei's history-tree view).")  ,
    # ch3.md:86
    ("exponential-decay items with mixed rates (the aggregation result, ob_0521) and with a",
     "exponential-decay items with mixed rates (the aggregation result) and with a"),
]


@pytest.mark.parametrize("text_in,expected", FORM_B)
def test_form_b_trailing_ids_dropped(text_in, expected):
    text, n = strip_provenance_ids("ch5.md", text_in)
    assert text == expected
    assert n >= 1


# ── C. (ID SEP words...) → keep the words, strip only the leading ID(s) ────

FORM_C = [
    # ch4.md:63
    ("as a stake-graded stance** (dv_0615, the eight-primitive generating set) — informed",
     "as a stake-graded stance** (the eight-primitive generating set) — informed"),
    # ch4.md:165
    ("as a stake-graded stance** (dv_0608, 0.35; active reading) — informed unification",
     "as a stake-graded stance** (0.35; active reading) — informed unification"),
    # SYNTHETIC (was ch1.md:165-166 at base commit 049d6d0a; #88 rewrote the
    # sentence and ch1.md no longer carries any node ID at all, so no real
    # instance of a newline-wrapped leading ID run remains anywhere in the
    # strip set to replace this with -- kept as a fixture purely to cover
    # the leading-run-spans-a-newline case, which no other Form C entry
    # exercises).
    ("verbatim failure passage (dv_0605,\nconf 0.95). The claim",
     "verbatim failure passage (conf 0.95). The claim"),
    # appendix_D:29-30 (em dash separator; note the source uses U+2014, not the
    # U+2013 the spec's SEP list literally names -- see handoff)
    ("honesty-is-structural (ax_0001/ax_0002 — epistemic identity fails *loudly*,\n"
     "  the friction of verification *is* the system working); practice",
     "honesty-is-structural (epistemic identity fails *loudly*,\n"
     "  the friction of verification *is* the system working); practice"),
    # appendix_D:71 (em dash + newline: the newline right after the dash IS
    # consumed, unlike the ax_0011 case below where the newline is INSIDE the
    # kept words)
    ("a truth claim** (gl_0025 —\ncurious about one's own reports, not credulous):",
     "a truth claim** (curious about one's own reports, not credulous):"),
    # ch7.md:213
    ("*knowing* and *disclosing* (ax_0011, honesty orthogonal to\ndiscretion): internal",
     "*knowing* and *disclosing* (honesty orthogonal to\ndiscretion): internal"),
    # appendix_D:31 (em dash; newline INSIDE the kept words is preserved as-is)
    ("honesty is **orthogonal to** discretion (ax_0011 — internal\n"
     "  integrity is independent of external disclosure — the basis for §D.3 and\n"
     "  Ch7's disclosure-vs-erasure).",
     "honesty is **orthogonal to** discretion (internal\n"
     "  integrity is independent of external disclosure — the basis for §D.3 and\n"
     "  Ch7's disclosure-vs-erasure)."),
]


@pytest.mark.parametrize("text_in,expected", FORM_C)
def test_form_c_leading_id_stripped_words_kept(text_in, expected):
    text, n = strip_provenance_ids("appendix_D_relational_identity.md", text_in)
    assert text == expected
    assert n >= 1


def test_form_c_leading_and_trailing_combine():
    # ch5.md:207-209: dv_0621 leads, ob_0034 trails, the middle (with its own
    # internal newline, preserved as-is) survives untouched.
    text_in = (
        "different priority — divergence **without a single new node** "
        "(dv_0621; backed\n  by the importance-inflation mechanism, ob_0034)."
    )
    expected = (
        "different priority — divergence **without a single new node** "
        "(backed\n  by the importance-inflation mechanism)."
    )
    text, n = strip_provenance_ids("ch5.md", text_in)
    assert text == expected
    assert n == 2


# ── D. (ID context) → remove the whole paren ────────────────────────────────


def test_form_d_id_context_paren_removed():
    # ch5.md:75-76
    text_in = "Lei's intuition pump\n(ob_1657 context): clone a mind into two"
    text, n = strip_provenance_ids("ch5.md", text_in)
    assert text == "Lei's intuition pump: clone a mind into two"
    assert n == 1


# ── E. bare token after a dash or word — literal-substitution table ────────


def test_form_e_word_before_id():
    # ch4.md:110
    text_in = "own definitions (E = b + a·u, first-hand ob_2551) it is instead"
    text, n = strip_provenance_ids("ch4.md", text_in)
    assert text == "own definitions (E = b + a·u, first-hand) it is instead"
    assert n == 1


def test_form_e_dash_before_id():
    # ch4.md:454-455
    text_in = (
        "about* the agent, not ground truth — gl_0025) and **person nodes**"
    )
    text, n = strip_provenance_ids("ch4.md", text_in)
    assert text == "about* the agent, not ground truth) and **person nodes**"
    assert n == 1


def test_form_e_id_followed_by_more_words():
    # appendix_D:90-92 -- the ID is trailed by MORE words ("in this graph")
    # before the closing paren, not sitting at the absolute end; this is why
    # E cannot be a simple "SEP RUN $" regex and needs the literal table.
    text_in = (
        "**self-anchor** (the\n`is_self` node — pn_0004 in this graph), "
        "the default target"
    )
    text, n = strip_provenance_ids("appendix_D_relational_identity.md", text_in)
    assert text == (
        "**self-anchor** (the\n`is_self` node), the default target"
    )
    assert n == 1


@pytest.mark.parametrize(
    "name,old_snippet",
    [
        ("ch4.md", "(E = b + a·u, first-hand ob_2551)"),
        ("ch4.md", "not ground truth — gl_0025)"),
        ("appendix_D_relational_identity.md", "`is_self` node — pn_0004 in this graph)"),
    ],
)
def test_form_e_literal_old_string_present_in_real_source(name, old_snippet):
    """Guards against silent no-op: if a source edit removes the exact phrase,
    this fails loudly instead of the literal table quietly matching nothing."""
    path = DRAFT / name
    if not path.exists():
        pytest.skip(f"source moved: {path}")
    text = path.read_text(encoding="utf-8")
    assert old_snippet in text, f"{name} no longer contains {old_snippet!r}"


# ── F. sentence-subject — literal-substitution table ────────────────────────


def test_form_f_sentence_subject():
    # ch4.md:288-289
    text_in = "*enabled*-level. The 0.39 on\ndv_0606 is the *abductive* confidence"
    text, n = strip_provenance_ids("ch4.md", text_in)
    assert text == "*enabled*-level. The 0.39 is the *abductive* confidence"
    assert n == 1


def test_form_f_literal_old_string_present_in_real_source():
    path = DRAFT / "ch4.md"
    if not path.exists():
        pytest.skip(f"source moved: {path}")
    text = path.read_text(encoding="utf-8")
    assert "The 0.39 on\ndv_0606 is the *abductive* confidence" in text


# ── G. table cells (ch4 §4.12 "Reading the verdicts", "Computed conf." col) ─

FORM_G_ROWS = [
    ("| C1 Diachronic | satisfied (decision/consequence dyad) | enabled + active | dv_0926 0.39 |",
     "| C1 Diachronic | satisfied (decision/consequence dyad) | enabled + active | 0.39 |"),
    ("| C2 Non-Interchangeability | strict **not met**; generalized via type/token (our extension) | philosophical | dv_0599 0.95 (extension) |",
     "| C2 Non-Interchangeability | strict **not met**; generalized via type/token (our extension) | philosophical | 0.95 (extension) |"),
    # #88 dropped the dv_0605 half of this cell (App B's synthesis node no
    # longer exists as a bare citation) -- was "dv_0606 0.39; dv_0605 0.95".
    ("| C3 Self-Maintaining Arbitration | **strict, sole satisfier** | enabled (arch) + active (pilot anchor) | dv_0606 0.39 |",
     "| C3 Self-Maintaining Arbitration | **strict, sole satisfier** | enabled (arch) + active (pilot anchor) | 0.39 |"),
    ("| A Unified Policy-Selection | satisfied as stake-graded stance | active (stake-graded) | dv_0608 0.35 |",
     "| A Unified Policy-Selection | satisfied as stake-graded stance | active (stake-graded) | 0.35 |"),
    ("| B External Non-Imposition | satisfied (two-boundary) | enabled + commitment-contract | dv_0609 0.58 |",
     "| B External Non-Imposition | satisfied (two-boundary) | enabled + commitment-contract | 0.58 |"),
    ("| C Non-Trivial Reset | satisfied trivially | enabled | dv_0610 |",
     "| C Non-Trivial Reset | satisfied trivially | enabled | — |"),
    ("| D Non-Modular Decomposition | satisfied on two axes | enabled (measured) | dv_0611 0.86 |",
     "| D Non-Modular Decomposition | satisfied on two axes | enabled (measured) | 0.86 |"),
]


@pytest.mark.parametrize("row_in,expected", FORM_G_ROWS)
def test_form_g_table_cells(row_in, expected):
    text, n = strip_provenance_ids("ch4.md", row_in)
    assert text == expected
    assert n >= 1


def test_form_g_c_row_no_confidence_uses_em_dash():
    """The C row states no confidence -- the bare ID with nothing else in the
    cell strips to an em dash, not an empty cell."""
    text, n = strip_provenance_ids(
        "ch4.md", "| C Non-Trivial Reset | satisfied trivially | enabled | dv_0610 |"
    )
    assert "—" in text
    assert "dv_0610" not in text


def test_form_g_only_touches_strip_set_files():
    row = "| C1 Diachronic | satisfied | enabled | dv_0926 0.39 |"
    text, n = strip_provenance_ids("ch6.md", row)
    assert text == row
    assert n == 0


def test_form_g_bracketed_cell_left_for_apparatus_stripper():
    """A cell whose ID sits inside a bracketed apparatus tag (not a bare
    'Computed conf.'-style token) is left for strip_apparatus_tags, not G."""
    row = (
        "| Auto-recall ranking (§4.7) | usage-learned composite ordering "
        "→ **Appx C** | MemRL **[ob_0647/ob_0651, prior read]** + "
        "spaced-repetition [SOLID] | — |"
    )
    text, n = strip_provenance_ids("ch4.md", row)
    assert "ob_0647" in text
    assert "ob_0651" in text


def test_form_g_real_table_rows_present_in_source():
    path = DRAFT / "ch4.md"
    if not path.exists():
        pytest.skip(f"source moved: {path}")
    text = path.read_text(encoding="utf-8")
    for row_in, _ in FORM_G_ROWS:
        assert row_in in text, f"ch4.md no longer contains {row_in!r}"


# ── Residue assertion: only df_* + the ch7.md KEEP_IDS data points remain ──


def test_residue_only_df_and_keep_ids():
    """Mirrors the real render pipeline (`main()`): provenance-ID stripping
    runs, THEN apparatus-tag stripping -- an ID still sitting inside a
    bracketed apparatus tag (e.g. ch3.md's "[SOLID: dv_0264, ob_1119]") is
    not yet a leak at the strip_provenance_ids stage alone.

    #84 added a real data-point example to ch7.md (dv_0779 bare in prose,
    dv_0877 inside an inline-code command example) -- both are KEEP_IDS
    entries now that App B's dv_0605 citation (the previous sole entry) no
    longer exists in the sources at all (#88). No exact count is pinned for
    either -- only that each survives at least once -- because a future
    source edit that duplicates or slightly rewords the sentence should not
    fail this test over the count."""
    from tools.render_paper import KEEP_IDS, strip_apparatus_tags, strip_provenance_ids

    keep_id_hits: dict[tuple[str, str], int] = {k: 0 for k in KEEP_IDS}
    for name in sorted(NEW_STRIP_FILES):
        path = DRAFT / name
        if not path.exists():
            pytest.skip(f"source moved: {path}")
        text = path.read_text(encoding="utf-8")
        stripped, _ = strip_provenance_ids(name, text)
        stripped, _ = strip_apparatus_tags(name, stripped)
        for m in _ID_SCAN.finditer(stripped):
            tok = m.group(0)
            if tok.startswith("df_"):
                continue
            if (name, tok) in KEEP_IDS:
                keep_id_hits[(name, tok)] += 1
                continue
            line_no = stripped.count("\n", 0, m.start()) + 1
            pytest.fail(f"unstripped ID leaked into render: {name}:{line_no} {tok!r}")
    for key, count in keep_id_hits.items():
        assert count >= 1, f"allow-listed {key} never appeared in the stripped output"


def test_ch7_data_point_ids_survive_the_strip():
    """#84's worked data-point sentence in ch7.md §7.2 ("The step is dv_0779
    in the frozen snapshot; tracing the conclusion it fed,
    `tools/paper_stats.py --trace dv_0877`, shows it at layer 4 of that
    chain") must come through the
    render untouched -- dv_0779 sits bare in prose and dv_0877 sits inside
    an inline-code command example, neither of which any of forms A-G ever
    matches, so both rely purely on the KEEP_IDS allowlist rather than on
    the strip logic leaving them alone by construction."""
    text_in = (
        "is dv_0779 in the frozen snapshot; tracing the conclusion it fed,\n"
        "`tools/paper_stats.py --trace dv_0877`, shows it at layer 4"
    )
    text, n = strip_provenance_ids("ch7.md", text_in)
    assert text == text_in
    assert n == 0
    assert "dv_0779" in text
    assert "dv_0877" in text


def test_ch7_data_point_sentence_present_in_real_source():
    """Guards against silent no-op / a stale KEEP_IDS entry: if a source edit
    removes or rewords this sentence, this fails loudly instead of the
    allowlist entries quietly matching nothing (or, worse, matching an
    unrelated dv_0779/dv_0877 mention elsewhere)."""
    path = DRAFT / "ch7.md"
    if not path.exists():
        pytest.skip(f"source moved: {path}")
    text = path.read_text(encoding="utf-8")
    assert (
        "is dv_0779 in the frozen snapshot; tracing the conclusion it fed,\n"
        "`tools/paper_stats.py --trace dv_0877`, shows it at layer 4"
    ) in text


def test_runtime_residue_check_raises_on_leak(monkeypatch):
    """The runtime guard (item 3) must raise, not just the test-time check."""
    import tools.render_paper as rp

    with pytest.raises(SystemExit):
        rp.assert_no_leaked_ids("ch2.md", "an id survived the strip (ob_9999)")


# ── Debris assertion (item 4) ────────────────────────────────────────────────

DEBRIS_PATTERNS = ["( ", "(,", "(;", ", )", "; )", "–)", "→)", "()", "( —"]


def test_no_debris_across_real_strip_set_files():
    for name in sorted(NEW_STRIP_FILES):
        path = DRAFT / name
        if not path.exists():
            pytest.skip(f"source moved: {path}")
        before = path.read_text(encoding="utf-8")
        after, _ = strip_provenance_ids(name, before)
        for pat in DEBRIS_PATTERNS:
            assert pat not in after, f"{name}: debris {pat!r} found after strip"
        # no double space introduced AT a strip site: compare line-by-line
        before_lines = before.split("\n")
        after_lines = after.split("\n")
        # line counts can differ (newline-consuming strips) so this is a
        # weaker global check: no line in `after` has "  " unless an
        # identical-looking line (ignoring IDs) existed in `before`.
        for line in after_lines:
            if "  " in line:
                assert any(
                    "  " in bl for bl in before_lines
                ), f"{name}: double space introduced: {line!r}"


def test_runtime_debris_check_raises():
    import tools.render_paper as rp

    with pytest.raises(SystemExit):
        rp.assert_no_leaked_ids("ch2.md", "left a gap ( ) here")


# ── Idempotent ────────────────────────────────────────────────────────────


@pytest.mark.parametrize("name", sorted(NEW_STRIP_FILES))
def test_idempotent_over_real_sources(name):
    path = DRAFT / name
    if not path.exists():
        pytest.skip(f"source moved: {path}")
    text = path.read_text(encoding="utf-8")
    once, _ = strip_provenance_ids(name, text)
    twice, n2 = strip_provenance_ids(name, once)
    assert once == twice
    assert n2 == 0
