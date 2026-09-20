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
               "hard data (0.92) to personal communication and editorial (0.60) is not a "
               "policy applied after the fact — it is computed at write time from the evidence "
               "the author declares, and the author cannot raise it by wanting the claim more."),
    ),
    (
        "ch6.md", "## 6.4",
        _fig("figures/fig4-depth-inversion.png", 5,
             "Computed confidence against derivation depth, for all 1,318 current derivations "
             "with at least one ancestor. Mean confidence **does** fall with depth, from 0.72 "
             "at one layer to 0.32 at sixteen — so depth is not irrelevant. But it does not "
             "*determine* the value, and two things on this plot show why. The spread at every "
             "depth is enormous: at depth 1 alone the range runs from about 0.10 to 0.98. And "
             "the ordering inverts — the graph's deepest chain (16 layers) carries 0.32 while "
             "the annotated synthesis six layers down carries 0.10, a third of the value at "
             "less than half the depth. A model that diluted by distance could not produce "
             "that pair. Argument shape is what separates them (Figure 2)."),
    ),
    (
        "ch6.md", "## 6.2",
        _fig("figures/fig5-growth.png", 6,
             "Cumulative node count across the trajectory, by month. The graph is one agent's, "
             "accumulated continuously from 2026-04-09 to the snapshot date. Growth is uneven "
             "and tracks working intensity rather than any schedule."),
    ),
]


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

    for name in BODY:
        body = load(DRAFT / name)
        body = apply_inserts(name, body)
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
