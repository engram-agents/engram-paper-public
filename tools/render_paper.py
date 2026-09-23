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
             "the identity-bearing types (cornerstones, lessons, axioms, goals) are together "
             "under 3%. Identity here is carried by the *structure* over the claims, not by "
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
               "the author declares, and the author cannot raise it by wanting the claim more."),
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
# (a) AUDIT ANCHORS in Appendix A and (b) DATA POINTS in Ch6 / Appendix E are part of
#     the evidence: a reader with the snapshot can resolve them, and the Data
#     Availability note says so. They stay.
# (c) STRUCTURAL references to Kahl's definitions (df_*) stay: Appendix E quotes those
#     definitions in full, so the ID is a label, not a pointer out of the document.
# (d) PROVENANCE MARKERS on argument sentences in Ch2-5 and Ch7 — a bare "(dv_1055)"
#     hung on a claim — read as citations and cannot be followed by anyone outside
#     this graph. Those are stripped FROM THE RENDER ONLY. The chapter sources keep
#     them: they are the SSoT's own provenance, and Ch8 §8.2's honesty argument
#     depends on their existing.
#
# Reversible in one line when a redacted dataset ships.
STRIP_PROVENANCE_IDS_IN = {
    "ch2.md", "ch3.md", "ch4.md", "ch5.md", "ch7.md",
}
# Never stripped anywhere: df_* (definition labels quoted in full in Appendix E).
_ID = r"(?:ob|dv|cs|ls|ax|cj|qu|fl|ev|pn|tk|gl|ct)_\d{4}"
_PAREN_ONLY = re.compile(r"\s*\((?:" + _ID + r")(?:\s*(?:,|;|/|and)\s*(?:" + _ID + r"))*\)")
_TRAILING_IN_PAREN = re.compile(r",\s*(?:" + _ID + r")(?:\s*(?:,|;|and)\s*(?:" + _ID + r"))*(?=\))")


def strip_provenance_ids(name: str, text: str) -> tuple[str, int]:
    """Remove bare parenthetical node-ID provenance markers from the RENDER."""
    if name not in STRIP_PROVENANCE_IDS_IN:
        return text, 0
    before = text
    text = _TRAILING_IN_PAREN.sub("", text)   # "(... , dv_1234)" -> "(...)"
    text = _PAREN_ONLY.sub("", text)          # "claim (dv_1234)" -> "claim"
    n = len(re.findall(_ID, before)) - len(re.findall(_ID, text))
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

    parts.append(load(PAPER / "bibliography.md"))

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    text = "\n\n---\n\n".join(p.rstrip() for p in parts) + "\n"
    out.write_text(text, encoding="utf-8")

    words = len(text.split())
    figs = text.count("**Figure ")
    print(f"# rendered {out}")
    print(f"  sources    {len(BODY)} chapters/appendices + front matter + bibliography")
    print(f"  length     {len(text.splitlines()):,} lines, {words:,} words")
    print(f"  figures    {figs} placed")
    print(f"  node IDs   {stripped_total} provenance markers stripped from the render "
          f"(sources keep them; audit anchors, data points and df_* labels untouched)")
    print(f"  apparatus  {apparatus_total} bracketed working tags stripped from the "
          f"render (sources keep them)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
