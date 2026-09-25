#!/usr/bin/env python3
"""render_paper.py — assemble the chapter sources into one publishable draft.

The chapter and appendix files are FROZEN as of the holistic-read phase: this
renderer never edits them. Everything the rendered paper adds beyond their text —
front matter, abstract, figure placement, mechanism diagrams, bibliography — lives
here or in `paper/`, so the assembled artifact can be regenerated at any time and
the per-chapter sources remain the single source of their own prose.

Figure and diagram placement is declared in INSERTS below, keyed on a heading in a
named source file. An insert whose anchor is not found is a hard error rather than a
silent omission — a figure that quietly fails to appear is the failure mode this
whole phase exists to catch.

Usage:
    python tools/render_paper.py --out paper/engram-paper-v0.5.1.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

DRAFT = Path("paper_research/current_draft")
PAPER = Path("paper")

# Assembly order. The rendered paper is exactly this, in exactly this sequence.
BODY = [
    "ch0_abstract.md",
    "ch1.md", "ch2.md", "ch3.md", "ch4.md",
    "ch5.md", "ch6.md", "ch7.md", "ch8.md",
    "appendix_A_independence.md",
    "appendix_B_c3_survey.md",
    "appendix_C_autorecall_ranking.md",
    "appendix_D_relational_identity.md",
    "appendix_E_techspec.md",
    "appendix_F_lucy.md",
]


def _fig(path: str, number: int, caption: str) -> str:
    return (
        f"\n![Figure {number}]({path})\n\n"
        f"**Figure {number}.** {caption}\n"
    )


# Mechanism diagrams. These describe ENGRAM v0.5.1 and nothing earlier — in
# particular the cascade walks `derives_from` and `acknowledged_derives_from` and
# does NOT walk `supported_by`, which is provenance-bearing but not cascade-bearing.
DIAGRAM_CASCADE = """
```mermaid
flowchart TD
    A["A claim is withdrawn<br/><b>retract</b> (never valid) or<br/><b>supersede</b> (was valid, now updated)"]
    A --> B{"Walk the two<br/>cascade-bearing relations"}
    B -->|derives_from| C["Every live dependent claim<br/>is marked <b>pending</b>"]
    B -->|acknowledged_derives_from| C
    B -.->|supported_by is NOT walked| X["Cornerstones and lessons<br/>are never marked:<br/>non-claim-bearing, and their<br/>exemplar edges are not traversed"]
    C --> D["Pending markers carry<br/>no severity — the substrate<br/>does not pre-judge the damage"]
    D --> E["<b>Auto-surfacing:</b> a marked claim<br/>is put back in front of the agent<br/>when it next becomes relevant"]
    D --> F["<b>Consolidation sweep:</b> every marked claim<br/>is driven to a decision even if it<br/>never becomes relevant"]
    E --> G{"Agent adjudicates<br/>at the frontier"}
    F --> G
    G -->|acknowledged| H["Premise moved,<br/>conclusion still holds"]
    G -->|superseded| I["Replaced by a<br/>named successor"]
    G -->|retracted| J["Withdrawn in turn —<br/>cascade continues downstream"]
    J --> B

    style A fill:#f6ece8,stroke:#b3593f
    style X fill:#f3f3f3,stroke:#8a8a8a,color:#555
    style G fill:#e9f1f4,stroke:#1f6f8b
```

**Diagram 1.** The retraction cascade in ENGRAM v0.5.1. Two things distinguish it
from detection-only conflict reporting. First, marking is *automatic state change*
rather than an advisory note the agent may consult. Second, the pairing of
auto-surfacing with a consolidation-time sweep means a marked claim is resolved
whether or not anyone remembers to look for it — detection without that binding
leaves the correction optional.
"""


# (source file, heading prefix to anchor on, block to append at the end of that section)
INSERTS: list[tuple[str, str, str]] = [
    (
        "ch1.md", "## 1.1",
        _fig("figures/fig6-census.png", 1,
             "What one real ENGRAM graph is made of — 9,399 current nodes at the snapshot "
             "date, by type. Observations and their evidence nodes are 72.8% of the graph; "
             "the identity-bearing types (71 cornerstones, 149 lessons, 9 axioms, 16 goals) "
             "are together 245 nodes, 2.6%; axioms and goals sit inside the chart's 'other' bar. "
             "Identity here is carried by the *structure* over the claims, not by "
             "a large store of self-description."),
    ),
    (
        "ch4.md", "## 4.4",
        DIAGRAM_CASCADE,
    ),
    (
        "ch6.md", "## 6.1",
        _fig("figures/fig1-reasoning-type.png", 2,
             "Mean computed confidence by declared reasoning type, current derivations, "
             "types with n ≥ 5. The spread is the confidence model's whole behaviour in one "
             "view: an inductive generalization over independent sources lands near 0.93, an "
             "analogy near 0.49. The author selects the *shape* of the argument; the number "
             "follows from it.")
        + _fig("figures/fig2-node-type.png", 3,
               "Confidence by node type — box shows the interquartile range, line the median. "
               "Each type occupies its own band by construction: axioms are terminal at 1.00, "
               "conjectures are clamped at creation, observations map near-mechanically from "
               "evidence type, and derivations span the widest range because they inherit from "
               "their premises.")
        + _fig("figures/fig3-quote-type.png", 4,
               "Mean confidence of current observations by evidence type. The gradient from "
               "hard data (0.91) to personal communication and editorial (0.60) is not a "
               "policy applied after the fact — it is computed at write time from the evidence "
               "the author declares, the same constraint §4.3 describes."),
    ),
    (
        "ch6.md", "## 6.4",
        _fig("figures/fig4-depth.png", 6,
             "Computed confidence against derivation depth, for all 1,318 current derivations "
             "with at least one ancestor. Mean confidence falls with depth, from 0.72 at one "
             "layer (705 derivations) to about 0.4 at twelve to fourteen layers (17 "
             "derivations); the deepest layers hold one node each, too few to read a trend. "
             "The spread at every depth is wide: at depth 1 alone it runs from about 0.2 to "
             "0.98. The annotated point is the six-layer chain worked through in §6.4 (0.10). "
             "Depth costs something on average; the kind of argument sets an individual "
             "claim's number (Figure 2)."),
    ),
    (
        "ch6.md", "## 6.2",
        _fig("figures/fig5-growth.png", 5,
             "Cumulative node count across the trajectory, by month. The graph is one agent's, "
             "accumulated continuously from 2026-04-09 to the snapshot date. Growth is uneven "
             "and tracks working intensity rather than any schedule."),
    ),
]


# --- K-1.27: node IDs do three different jobs and get three treatments -----------
#
# (a) AUDIT ANCHORS in Appendix A and (b) DATA POINTS in Ch6 / (most of) Appendix E
#     are part of the evidence: a reader with the snapshot can resolve them, and the
#     Data Availability note says so. They stay.
# (c) STRUCTURAL references to Kahl's definitions (df_*) stay: Appendix E quotes those
#     definitions in full, so the ID is a label, not a pointer out of the document.
# (d) PROVENANCE MARKERS on argument sentences in Ch2-5 and Ch7 — a bare "(dv_1055)"
#     hung on a claim — read as citations and cannot be followed by anyone outside
#     this graph. Those are stripped FROM THE RENDER ONLY. The chapter sources keep
#     them: they are the SSoT's own provenance, and Ch8 §8.2's honesty argument
#     depends on their existing.
#
# Reversible in one line when a redacted dataset ships.
#
# 2026-09-23 (Lei's ruling): extended to every chapter/appendix whose IDs are
# CITATION-STYLE (standing in for a citation) rather than DATA POINTS (a real
# node used as a worked example). Ch6 and Appendix A are data points and are
# explicitly excluded; Appendix B/C/D are citation-style and added. `df_*`
# (Kahl's definitions, quoted in full in Appendix E) are never stripped
# anywhere, in or out of this set.
#
# 2026-09-23 fold (colleague verdict, Borges): Appendix E is overwhelmingly
# data points (and its df_* labels), but E.5 carries one stray CITATION-STYLE
# ID -- "The eight load-bearing **primitives** (dv_0615): typed nodes, ..." --
# already stripped from Ch4 §4.2, missed here because Appendix E was outside
# this set entirely. Appendix E is added below for that one occurrence; its
# df_* tokens are never touched (see (c) above), and it carries no other
# non-df ID for the strip forms to reach.
#
# 2026-09-24 (Lei's spec, appendix-f-lucy PR): Appendix F is a NEW tenth
# entry, not a widening of the "Appendix E fold" reasoning above -- every
# sentence of F's design-history text was moved verbatim OUT OF Appendix D,
# which is already in this set (the "won, on three grounds" ->
# "won on two grounds ... agency and engagement ... and a third" edit is the one designated
# fix; everything else, including the citation-style `(ob_0645)`, carried
# over unchanged). Appendix F inherits Appendix D's stripping so that move
# is not also a render-behaviour change: without this entry, `(ob_0645)`
# would newly render un-stripped in Appendix F even though it was always
# stripped from that same text while it lived in D.4.
STRIP_PROVENANCE_IDS_IN = {
    "ch1.md", "ch2.md", "ch3.md", "ch4.md", "ch5.md", "ch7.md",
    "appendix_B_c3_survey.md", "appendix_C_autorecall_ranking.md",
    "appendix_D_relational_identity.md", "appendix_E_techspec.md",
    "appendix_F_lucy.md",
}

# Data points stated in Lei's required form are deliberately KEPT inside a
# strip-set file even though their file is otherwise stripped. Each survives
# untouched because the ID sits BARE in the prose (or inside an inline code
# span), never inside one of the recognized citation forms A-G -- this set
# exists purely as the post-strip residue allowlist (see
# `assert_no_leaked_ids`), not as an input to the stripping itself.
#
# ch7.md's "The step is dv_0779 in the frozen snapshot; `tools/paper_stats.py
# --trace dv_0877` shows it in place, layer 4 of the chain it inflated" (added
# by #84, under Lei's 2026-09-23 ruling) names a real node used as a worked
# example of a mis-typed reasoning step -- a data point, not a citation hung
# on someone else's claim -- so both dv_0779 (bare in prose) and dv_0877
# (inside the inline-code command example) stay.
KEEP_IDS: set[tuple[str, str]] = {
    ("ch7.md", "dv_0779"),
    ("ch7.md", "dv_0877"),
}

# Never stripped anywhere: df_* (definition labels quoted in full in Appendix E).
_ID = r"(?:ob|dv|cs|ls|ax|cj|qu|fl|ev|pn|tk|gl|ct)_\d{4}"

# Separators that JOIN two IDs together into one run (ranges, arrows, lists).
# `\s*` on both sides is deliberate and covers newlines: several parens wrap
# across a line break in the source (e.g. ch1 "(dv_0605,\nconf 0.95)" and ch7
# "(ob_1064–\nob_1067)").
_JOIN_SEP = r"(?:\s*(?:,|;|/|and\b|–|—|→)\s*)"
# Separator that may introduce a LEADING run of IDs, i.e. before free-text
# words (form C): same set as _JOIN_SEP, since a leading "(ax_0001/ax_0002 —
# epistemic identity fails ...)" uses an em dash exactly like a list join.
_LEAD_SEP = _JOIN_SEP
# Separator that may introduce a TRAILING run of IDs at the very end of a
# parenthetical (form B) — deliberately narrower than _JOIN_SEP/_LEAD_SEP:
# no dash/arrow here. A dash before a single trailing ID reads as free-text
# annotation ("... not ground truth — gl_0025)") rather than a list
# separator, and — unlike the leading case — a trailing dash can be followed
# by MORE words before the closing paren (appendix_D's "is_self` node —
# pn_0004 in this graph)"), which a plain "SEP RUN $" regex cannot express
# safely. Those are form E and are handled by the literal-substitution table
# below, applied before these regexes ever run.
_TRAIL_SEP = r"(?:\s*(?:,|;|/|and\b)\s*)"

_RUN = _ID + r"(?:" + _JOIN_SEP + _ID + r")*"
_FULL_RUN_PAREN = re.compile(r"\s*\((?:" + _RUN + r")\)", re.DOTALL)
_LEADING_RUN = re.compile(r"\A(?:" + _RUN + r")(?:" + _LEAD_SEP + r")", re.DOTALL)
_TRAILING_RUN = re.compile(r"(?:" + _TRAIL_SEP + r")(?:" + _RUN + r")\Z", re.DOTALL)
_PAREN_SPAN = re.compile(r"\(([^()]*)\)", re.DOTALL)

# Form D: "(ID context)" -- an incidental annotation, not a citation with
# content worth keeping ("context" carries no information on its own). The
# entire parenthetical (plus its leading whitespace, matching the same
# `\s*` convention as the full-run case) is removed.
_CONTEXT_PAREN = re.compile(r"\s*\(" + _ID + r"\s+context\)")

# Forms E and F: a bare ID trailing a dash/word, or naming a sentence subject,
# where the surrounding free text can continue past the ID before the natural
# stopping point (so no bounded regex expresses the cut safely). Applied as
# plain literal substitutions, BEFORE the regexes above, keyed by source file.
# Each `old` is asserted present in its real source by
# `test_form_e_literal_old_string_present_in_real_source` /
# `test_form_f_literal_old_string_present_in_real_source` in
# tests/test_render_strip_ids.py, so a source edit that removes the phrase
# fails loudly instead of the substitution silently no-op'ing.
_LITERAL_STRIPS: dict[str, list[tuple[str, str]]] = {
    "ch4.md": [
        ("(E = b + a·u, first-hand ob_2551)", "(E = b + a·u, first-hand)"),
        ("not ground truth — gl_0025)", "not ground truth)"),
        ("The 0.39 on\ndv_0606 is the *abductive* confidence",
         "The 0.39 is the *abductive* confidence"),
    ],
    "appendix_D_relational_identity.md": [
        ("`is_self` node — pn_0004 in this graph)", "`is_self` node)"),
    ],
}

# Form G: table cells in the ch4 §4.12 "Reading the verdicts" table's
# "Computed conf." column carry BARE ID tokens with no surrounding parens at
# all ("dv_0926 0.39", not "(dv_0926 0.39)") -- outside the reach of every
# paren-based form above. Applied to any markdown table row (a line whose
# stripped form starts with "|") in a strip-set file; a cell containing "["
# is left untouched (that is apparatus-tag territory, e.g. ch4's
# "[GROUNDED ob_2550]" cells, handled by strip_apparatus_tags separately).
_TABLE_ROW = re.compile(r"^([ \t]*\|.*)$", re.MULTILINE)
_WS_RUN = re.compile(r"\s+")


def _strip_table_row_ids(row: str) -> tuple[str, int]:
    cells = row.split("|")
    n = 0
    out_cells = []
    for cell in cells:
        if "[" in cell or not re.search(_ID, cell):
            out_cells.append(cell)
            continue
        stripped_cell, cell_n = re.subn(_ID, "", cell)
        n += cell_n
        stripped_cell = _WS_RUN.sub(" ", stripped_cell).strip()
        out_cells.append(" " + (stripped_cell or "—") + " ")
    return "|".join(out_cells), n


def _strip_table_cells(text: str) -> tuple[str, int]:
    total = 0

    def repl(m: re.Match) -> str:
        nonlocal total
        row = m.group(1)
        if not row.lstrip().startswith("|"):
            return row
        new_row, n = _strip_table_row_ids(row)
        total += n
        return new_row

    text = _TABLE_ROW.sub(repl, text)
    return text, total


def _strip_paren_forms(text: str) -> str:
    # Form A: the entire parenthetical is nothing but an ID run.
    text = _FULL_RUN_PAREN.sub("", text)

    # Forms B/C on every remaining "(...)" span (non-nested): strip a leading
    # run of IDs (keeping any free-text words that follow), then a trailing
    # run of IDs (keeping any free-text words that precede). Either, both, or
    # neither may apply to a given span.
    def repl(m: re.Match) -> str:
        content = m.group(1)
        if not re.search(_ID, content):
            return m.group(0)
        new_content = content
        lead = _LEADING_RUN.match(new_content)
        if lead:
            new_content = new_content[lead.end():]
        trail = _TRAILING_RUN.search(new_content)
        if trail:
            new_content = new_content[: trail.start()]
        if not re.search(_ID, new_content):
            if new_content.strip() == "":
                return ""
            return "(" + new_content + ")"
        return m.group(0)

    return _PAREN_SPAN.sub(repl, text)


_BRACKET_SPAN = re.compile(r"\[[^\]]*\]", re.DOTALL)


def assert_no_leaked_ids(name: str, text: str) -> None:
    """Runtime guard (item 3/4 of spec-strip.md): after stripping, the only ID
    tokens surviving in a strip-set file's rendered text must be `df_*` labels
    plus the explicit `KEEP_IDS` allowlist -- and no debris (an emptied
    parenthetical, a stray separator) may remain either. Raises with
    file:line so a future source edit that adds a new unstripped form cannot
    silently leak an ID (or a stripped-open paren) into the render.

    An ID still inside a square-bracketed apparatus tag (e.g. "[SOLID:
    dv_0264, ob_1119]") is NOT a leak from this function's own scope: those
    are `strip_apparatus_tags`'s responsibility and are removed later in the
    render pipeline (`main()` runs provenance-ID stripping first, apparatus
    stripping second) -- so bracketed spans are excluded from this scan.
    """
    bracketed = [(m.start(), m.end()) for m in _BRACKET_SPAN.finditer(text)]

    def _in_bracket(pos: int) -> bool:
        return any(s <= pos < e for s, e in bracketed)

    for m in re.finditer(_ID, text):
        if _in_bracket(m.start()):
            continue
        tok = m.group(0)
        if tok.startswith("df_"):
            continue
        if (name, tok) in KEEP_IDS:
            continue
        line_no = text.count("\n", 0, m.start()) + 1
        raise SystemExit(f"{name}:{line_no}: unstripped ID leaked into render: {tok!r}")

    debris = ["( ", "(,", "(;", ", )", "; )", "–)", "→)", "()", "( —"]
    for pat in debris:
        idx = text.find(pat)
        while idx != -1:
            if not _in_bracket(idx):
                line_no = text.count("\n", 0, idx) + 1
                raise SystemExit(f"{name}:{line_no}: strip debris {pat!r} left in render")
            idx = text.find(pat, idx + 1)


def strip_provenance_ids(name: str, text: str) -> tuple[str, int]:
    """Remove citation-style node-ID provenance markers from the RENDER.

    Node IDs used as DATA POINTS (a real node cited as a worked example) are
    never touched -- either because their file is not in
    `STRIP_PROVENANCE_IDS_IN` at all (Ch6, Appendix A), or, within a
    strip-set file (including Appendix E, which is overwhelmingly data
    points but is in this set for one stray citation-style ID -- see the
    2026-09-23 fold comment above `STRIP_PROVENANCE_IDS_IN`), because the ID
    sits bare in the prose rather than inside one of the recognized citation
    forms (see `KEEP_IDS`).
    """
    if name not in STRIP_PROVENANCE_IDS_IN:
        return text, 0
    before = text

    # Forms E/F: literal substitutions, applied first (see _LITERAL_STRIPS).
    for old, new in _LITERAL_STRIPS.get(name, []):
        text = text.replace(old, new)

    # Form D: "(ID context)" -- whole paren removed.
    text = _CONTEXT_PAREN.sub("", text)

    # Forms A/B/C: full-run parens, then leading/trailing runs within a
    # parenthetical that also carries free-text content.
    text = _strip_paren_forms(text)

    # Form G: bare ID tokens in markdown table cells.
    text, _ = _strip_table_cells(text)

    n = len(re.findall(_ID, before)) - len(re.findall(_ID, text))
    assert_no_leaked_ids(name, text)
    return text, n


# --- apparatus-tag stripping: working notes bracketed onto argument sentences ----
#
# A bracketed span like `[SOLID]`, `[GROUNDED ob_2551/dv_0965]`, or
# `**[gap SOLID ob_1571; primary first-hand 2026-07-02]**` is grounding/verification
# apparatus the AUTHOR needed while writing — not something the READER needs. The
# chapter sources keep these; the RENDER does not. Unlike `strip_provenance_ids`
# above (bare parenthetical node-ID citations), these are square-bracketed, often
# bold-wrapped, and sometimes span multiple lines — a line-based strip would miss
# them, so the tag's content is matched with a character class that spans newlines.
_APPARATUS_OPENERS = (
    r"(?:SOLID|GROUNDED|gap\s+SOLID|Honest\s+scope|via\s+ob_|ob_\d{4}|secondary)"
)

# Two shapes, tried in order at every match position (alternation commits to the
# first that succeeds, so listing the more specific ISOLATED shape first is what
# makes it win whenever both could apply):
#
#   ISOLATED — the tag is the only non-whitespace content of its own paragraph
#   (bounded on each side by a blank line, a single line break, or the start/end
#   of the text). Both the leading and trailing boundary are captured so the
#   replacement can be computed explicitly (see _apparatus_repl): two genuine
#   blank lines collapse to exactly one, a single line break on either side
#   survives as the paragraph separator, and a text-start/end edge contributes
#   nothing (no spurious leading/trailing break is introduced).
#
#   INLINE — the tag sits inside a line alongside other content. Only the
#   whitespace immediately before the tag is removed (at most one newline, so a
#   blank line further back is never touched); whatever follows the tag —
#   including punctuation with no space, per the "punctuation is kept and
#   re-attached" rule — is left exactly as it was.
_APPARATUS_TAG = re.compile(
    r"(?P<iso_pre>\A|\n\n|\n)[ \t]*(?P<iso_bold>\*\*)?"
    r"\[\s*" + _APPARATUS_OPENERS + r"[^\]]*\](?(iso_bold)\*\*)[ \t]*"
    r"(?P<iso_post>\n\n|\n|\Z)"
    r"|"
    r"(?P<inl_pre>[ \t]*(?:\n[ \t]*)?)(?P<inl_bold>\*\*)?"
    r"\[\s*" + _APPARATUS_OPENERS + r"[^\]]*\](?(inl_bold)\*\*)"
)


def _apparatus_repl(m: re.Match) -> str:
    if m.group("iso_pre") is not None:
        # `\A` and `\Z` are zero-width, so a matched anchor (text edge) comes
        # back as the empty string, not the pattern's own escape text.
        pre, post = m.group("iso_pre"), m.group("iso_post")
        at_start, at_end = pre == "", post == ""
        if pre == "\n\n" and post == "\n\n":
            return "\n\n"           # two genuine blank lines -> exactly one
        if pre == "\n\n":
            return "" if at_end else "\n\n"
        if post == "\n\n":
            return "" if at_start else "\n\n"
        if at_start or at_end:
            return ""               # nothing to separate from/into at a text edge
        return "\n"                 # ordinary single line break on both sides
    return ""                       # INLINE: preceding whitespace + tag, nothing kept


def strip_apparatus_tags(name: str, text: str) -> tuple[str, int]:
    """Remove bracketed working-apparatus tags from the RENDER (sources keep them).

    Applies to all BODY files — unlike `strip_provenance_ids`, apparatus tags are
    not scoped to a subset of chapters; `name` is accepted for signature symmetry
    with the sibling function and for future scoping if it's ever needed.
    """
    return _APPARATUS_TAG.subn(_apparatus_repl, text)


def load(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"missing source: {path}")
    return path.read_text(encoding="utf-8").rstrip() + "\n"


def section_end(lines: list[str], start: int) -> int:
    """Index just past the section opened by lines[start] (a heading)."""
    level = len(re.match(r"#+", lines[start]).group(0))
    for i in range(start + 1, len(lines)):
        m = re.match(r"(#+)\s", lines[i])
        if m and len(m.group(1)) <= level:
            return i
    return len(lines)


def apply_inserts(name: str, text: str) -> str:
    blocks = [(h, b) for (f, h, b) in INSERTS if f == name]
    if not blocks:
        return text
    lines = text.split("\n")
    # Insert from the bottom up so earlier indices stay valid.
    located = []
    for heading, block in blocks:
        idx = next((i for i, l in enumerate(lines) if l.startswith(heading)), None)
        if idx is None:
            raise SystemExit(f"anchor not found: {name} :: {heading!r}")
        located.append((section_end(lines, idx), block))
    for at, block in sorted(located, key=lambda t: -t[0]):
        lines[at:at] = ["", block.rstrip(), ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="paper/engram-paper-v0.5.1.md")
    a = ap.parse_args()

    parts = [load(PAPER / "front-matter.md")]

    stripped_total = 0
    apparatus_total = 0
    for name in BODY:
        body = load(DRAFT / name)
        body = apply_inserts(name, body)
        body, n = strip_provenance_ids(name, body)
        stripped_total += n
        body, m = strip_apparatus_tags(name, body)
        apparatus_total += m
        parts.append(body)

    parts.append(load(PAPER / "acknowledgements.md"))
    parts.append(load(PAPER / "bibliography.md"))

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    text = "\n\n---\n\n".join(p.rstrip() for p in parts) + "\n"
    out.write_text(text, encoding="utf-8")

    words = len(text.split())
    figs = text.count("**Figure ")
    print(f"# rendered {out}")
    print(f"  sources    {len(BODY)} chapters/appendices + front matter + acknowledgements + bibliography")
    print(f"  length     {len(text.splitlines()):,} lines, {words:,} words")
    print(f"  figures    {figs} placed")
    print(f"  node IDs   {stripped_total} provenance markers stripped from the render "
          f"(sources keep them; audit anchors, data points and df_* labels untouched)")
    print(f"  apparatus  {apparatus_total} bracketed working tags stripped from the "
          f"render (sources keep them)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
