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
    python tools/render_paper.py --lang zh          # -> engram-paper-v0.5.1.zh.md

`--lang {en,zh}` (default `en`) selects the chapter-source directory: `en` reads
`paper_research/current_draft/`, `zh` reads `paper_research/current_draft_zh/`.
ONE `BODY` list drives both; a chapter that is missing in the selected language is
a hard error naming the resolved file, never a skip -- a half-translated book must
not render short.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

DRAFT = Path("paper_research/current_draft")
DRAFT_ZH = Path("paper_research/current_draft_zh")
PAPER = Path("paper")

LANGS = ("en", "zh")

# --- language surface (`--lang {en,zh}`) -----------------------------------------
#
# ONE `BODY` list is shared across languages. A language is a source DIRECTORY
# plus a filename convention -- never a second chapter list, so a chapter added
# to the paper cannot be added to one language and forgotten in the other.
#
# zh chapters carry a `.zh` infix (`ch1.md` -> `ch1.zh.md`). That is the
# convention the one existing zh source already uses
# (`current_draft_zh/appendix_G_glossary.zh.md`, commit 7623554), and the same
# one the three zh front/back-matter files need, since `paper/` is shared by
# both languages and the suffix is the only thing that tells them apart. The
# directory carries the language marker too; that redundancy is deliberate here
# -- `current_draft/` and `current_draft_zh/` are otherwise identical, and a
# file copied between them keeps its name.
SOURCE_DIRS = {"en": DRAFT, "zh": DRAFT_ZH}
CHAPTER_SUFFIX = {"en": "", "zh": ".zh"}
DEFAULT_OUT = {
    "en": "paper/engram-paper-v0.5.1.md",
    "zh": "paper/engram-paper-v0.5.1.zh.md",
}

# Front/back matter is not per-language-directory (both languages read `paper/`),
# so the zh files carry the suffix there. These three are the only zh sources that
# may legitimately be an untranslated placeholder while the translation is
# pending; every BODY chapter is a hard requirement -- `load` raises on a missing
# one, which is the whole point (see `main`).
FRONT_MATTER = {"en": "front-matter.md", "zh": "front-matter.zh.md"}
ACKNOWLEDGEMENTS = {"en": "acknowledgements.md", "zh": "acknowledgements.zh.md"}
BIBLIOGRAPHY = {"en": "bibliography.md", "zh": "bibliography.zh.md"}


def chapter_name(lang: str, name: str) -> str:
    """The filename `name` (a BODY entry, always English-named) has in `lang`.

    `en` is the identity -- the English filenames are unchanged -- so this is the
    single place the per-language convention lives."""
    if not name.endswith(".md"):
        raise SystemExit(f"BODY entry is not a markdown filename: {name!r}")
    return f"{name[:-3]}{CHAPTER_SUFFIX[lang]}.md"


def chapter_path(lang: str, name: str) -> Path:
    return SOURCE_DIRS[lang] / chapter_name(lang, name)


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
    "appendix_G_glossary.md",
]


# Figure/diagram label words. English keeps `Diagram` distinct from `Figure`
# because the two number independently (Diagram 1 vs Figures 1-6); the zh render
# keeps that distinction as 示意图 vs 图 rather than collapsing both to 图, which
# would make "图 1" name two different things in one paper.
FIGURE_LABEL = {"en": "Figure", "zh": "图"}
DIAGRAM_LABEL = {"en": "Diagram", "zh": "示意图"}


# --- Appendix G length budget ---------------------------------------------------
#
# The English glossary is budgeted in whitespace tokens. Chinese is not
# space-delimited, so that measurement is near-vacuous on the zh glossary (427
# whitespace tokens against 2,999 Han characters). The zh budget therefore counts
# Han characters (Unicode CJK Unified Ideographs, U+4E00-U+9FFF) and converts them
# to an English-token equivalent through the ratio below.
#
# METHOD -- stated so the figures below can be re-checked rather than just cited.
# Both sides are measured on the GLOSSARY BODY, with the ledger's leading
# translator header comment excluded (the `<!-- ... -->` block at the top of the zh
# file):
#
#   * whitespace token = `len(text.split())` -- Python's split on runs of
#     whitespace, the same definition the English budget already uses;
#   * Han character   = a per-character scan of U+4E00-U+9FFF inclusive.
#
# Measured 2026-09-28 on zephyr/zh-translation at d35dc5f:
#
#   English Appendix G   1,753 whitespace tokens
#   zh Appendix G        2,999 Han characters
#
# The zh figure EXCLUDES the leading header deliberately. That block is translator
# metadata, not glossary prose: markdown hides `<!-- ... -->`, and the English
# glossary has no counterpart to it -- so counting it would compare two different
# things, and would move the measurement every time a translator edits the header,
# which is a documentation change and not a translation change. The counting helper
# in tests/test_glossary.py strips only a LEADING comment block, anchored at the
# start of the file, so a comment appearing inside the glossary body is never
# removed. Do not re-add the header to the count.
#
# PROVENANCE -- read before changing this number. 1.71 was derived from ONE
# parallel pair, measured as above: 2999 / 1753 = 1.7108. It is a CALIBRATION FROM
# A SINGLE PAIR, NOT A LAW -- a plausible characters-per-word density for zh prose
# and nothing more. If a later chapter disagrees, RE-DERIVE the ratio from that
# chapter's own en/zh pair; do not pad the text to fit this one.
#
# At 1.71 the zh budget is 1800 x 1.71 = 3078 Han characters, against the current
# 2,999 -- 79 characters (2.6%) of headroom.
#
# CORRECTION (2026-09-28). This constant previously read 1.75, derived as
# 3069/1753. That pair was measured on the WHOLE zh file as it stood at bff5d39,
# translator header included, and was accurate for that revision -- but the header
# has since grown (d2ab184, and the header edits after it), so a whole-file count
# now reads 845 tokens / 3,109 Han while the GLOSSARY BODY has never changed
# (2,999 Han at every revision back to the first zh source, 7623554). That is why
# an earlier whole-file pair of 1,008 tokens / 3,111 Han is not comparable to the
# 845 / 3,109 taken at d35dc5f: it is a LATER revision of the same file on
# zephyr/zh-chapters, with a larger header -- not a strip-regex artifact. Reading
# 1.75, 3,069 or 1,008 anywhere else: this is why they no longer match.
#
# Whether zh should carry a length budget AT ALL is a POLICY question belonging to
# Lei. This constant and the check that consumes it are the measurable half only,
# and must not be read as settling that question.
ZH_HAN_PER_EN_WORD = 1.71


def _fig(path: str, number: int, caption: str, label: str = "Figure") -> str:
    """One figure block. `label` is the rendered word ("Figure" / "图"); its
    default reproduces the English render byte-for-byte."""
    return (
        f"\n![{label} {number}]({path})\n\n"
        f"**{label} {number}.** {caption}\n"
    )


# Mechanism diagrams. These describe ENGRAM v0.5.1 and nothing earlier — in
# particular the cascade walks `derives_from` and `acknowledged_derives_from` and
# does NOT walk `supported_by`, which is provenance-bearing but not cascade-bearing.
DIAGRAM_CASCADE = """
```mermaid
flowchart TD
    subgraph P1["Phase 1: propagation (automatic; resolves nothing)"]
        A["The agent <b>retracts</b> a claim (never valid)<br/>or <b>supersedes</b> it (was valid, now updated)"]
        A --> B{"Walk downstream along the<br/>cascade-bearing relations,<br/>as far as they reach"}
        B -->|derives_from| C["Every live claim-bearing dependent<br/>gets one <b>pending</b> marker:<br/>no severity, only which operation fired"]
        B -->|acknowledged_derives_from| C
        B -.->|supported_by is NOT walked| X["Cornerstones and lessons<br/>are never marked"]
        C --> D["A pending claim cannot be cited<br/>as a premise until it is resolved"]
    end
    D -.-> S["<b>Auto-surfacing</b> shows a marked claim<br/>when it next becomes relevant.<br/>A reminder: it resolves nothing"]
    subgraph P2["Phase 2: resolution (the agent's; one frontier node at a time)"]
        F["<b>Full:</b> each consolidation cycle<br/>walks the whole frontier<br/>until no marker is left"]
        T["<b>Partial:</b> to unblock one claim,<br/>settle only the pending claims it rests on,<br/>then the claim itself"]
        F --> G{"The agent settles a <b>frontier</b> node:<br/>pending, with nothing pending<br/>above it"}
        T --> G
        G -->|retracted| R["The argument<br/>is broken"]
        G -->|superseded| U["The claim survives in<br/>a named successor"]
        G -->|acknowledged| K["Premise moved, claim still holds<br/>(not available if a direct<br/>premise was retracted; automatic<br/>if every premise was acknowledged)"]
        R --> N["Confidence is recomputed. No new derivation cascade:<br/>dependents were marked in phase 1<br/>and now reach the frontier in turn"]
        U --> N
        K --> N
        N -.->|next frontier node| G
    end
    D ==> F
    D ==> T

    style A fill:#f6ece8,stroke:#b3593f
    style X fill:#f3f3f3,stroke:#8a8a8a,color:#555
    style S fill:#f3f3f3,stroke:#8a8a8a,color:#555
    style G fill:#e9f1f4,stroke:#1f6f8b
```

**Diagram 1.** The retraction cascade in ENGRAM v0.5.1, as two separate processes.
Propagation is automatic: each retraction or supersede marks everything downstream at
once, and decides nothing. Resolution is the agent's: it settles the marked claims from
the top down, either the whole frontier during consolidation or only the slice one claim
needs, and it never starts a new derivation cascade. Two things distinguish this from
detection-only conflict reporting: marking is an automatic state change rather than an
advisory note, and the consolidation walk means every mark is eventually faced, whether
or not anyone remembers to look for it.
"""


# Chinese counterpart of DIAGRAM_CASCADE. Same graph (same node ids, same
# edges, same `style` lines) with the labels translated; the relation names
# (`derives_from`, `acknowledged_derives_from`, `supported_by`) stay English per
# the house rule the zh term ledger records -- identifiers, CLI verbs, field
# names and node codes are kept English in zh surfaces. `retract`/`supersede`
# lead with their Chinese terms (撤回/取代) plus the English in parentheses,
# matching the ledger's first-occurrence pattern. Diagram kept distinct from
# figures as 示意图 vs 图 (see FIGURE_LABEL/DIAGRAM_LABEL).
DIAGRAM_CASCADE_ZH = """
```mermaid
flowchart TD
    subgraph P1["阶段 1：传播（自动；不解决任何事）"]
        A["智能体<b>撤回（retract）</b>一项主张（从未有效）<br/>或<b>取代（supersede）</b>它（曾经有效，现已更新）"]
        A --> B{"沿承载级联的关系<br/>向下游遍历，<br/>能走多远就走多远"}
        B -->|derives_from| C["每一现行的承载主张依赖项<br/>获得一个<b>待决</b>标记：<br/>不携带严重程度，只记录触发的是哪种操作"]
        B -->|acknowledged_derives_from| C
        B -.->|supported_by 不遍历| X["基石与教训<br/>从不被标记"]
        C --> D["待决的主张在被解决之前<br/>不得被引为前提"]
    end
    D -.-> S["<b>自动浮现</b>在被标记的主张<br/>下次变得相关时把它显示出来。<br/>只是提醒：它不解决任何事"]
    subgraph P2["阶段 2：解决（由智能体进行；一次一个前沿节点）"]
        F["<b>完整：</b>每个整理周期<br/>走遍整个前沿，<br/>直到不剩标记"]
        T["<b>局部：</b>为解除一条主张的阻塞，<br/>只了结它所依赖的待决主张，<br/>再了结它本身"]
        F --> G{"智能体了结一个<b>前沿</b>节点：<br/>自身待决，<br/>其上游无一待决"}
        T --> G
        G -->|撤回| R["论证<br/>已破"]
        G -->|取代| U["主张在一个有名字的<br/>后继者中存活"]
        G -->|承认| K["前提移动，主张仍然成立<br/>（若某个直接前提<br/>已被撤回则不可选；若每个前提<br/>都被承认则自动完成）"]
        R --> N["置信度被重算。不启动新的推导级联：<br/>依赖项已在阶段 1 被标记，<br/>现在依次抵达前沿"]
        U --> N
        K --> N
        N -.->|下一个前沿节点| G
    end
    D ==> F
    D ==> T

    style A fill:#f6ece8,stroke:#b3593f
    style X fill:#f3f3f3,stroke:#8a8a8a,color:#555
    style S fill:#f3f3f3,stroke:#8a8a8a,color:#555
    style G fill:#e9f1f4,stroke:#1f6f8b
```

**示意图 1.** ENGRAM v0.5.1 中的撤回级联，分为两个彼此分开的过程。传播是自动的：每一次撤回或
取代都会一次性标记下游的一切，并且不作任何决定。解决是智能体的事：它自上而下地了结被标记的主张，
要么在整理期走遍整个前沿，要么只走一条主张所需的那一小片，而且它从不启动新的推导级联。有两点把它与
“只做检测”的冲突报告区分开来：标记是一次自动的状态变更，而不是一份提示；整理期的遍历意味着每一个
标记最终都会被面对，无论有没有人记得去找它。
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

# Chinese counterpart of INSERTS: the SAME anchors, in the same order, with the
# captions translated (`label="图"` renders 图 N where English renders Figure N).
# The anchor keys are asserted identical to INSERTS' immediately below -- see
# `assert_insert_anchor_parity`.
INSERTS_ZH: list[tuple[str, str, str]] = [
    (
        "ch1.md", "## 1.1",
        _fig("figures/fig6-census.png", 1,
             "一个真实 ENGRAM 图谱的构成——按类型统计的快照日期上的 9,399 个当前节点。"
             "观察及其证据节点占全图的 72.8%；承载身份的类型（71 个基石、149 条教训、"
             "9 条公理、16 个目标）合计 245 个节点，占 2.6%；公理与目标落在图中“其他”"
             "那一柱之内。此处的身份由主张之上的*结构*承载，而不由一座庞大的自我描述"
             "仓库承载。",
             label="图"),
    ),
    (
        "ch4.md", "## 4.4",
        DIAGRAM_CASCADE_ZH,
    ),
    (
        "ch6.md", "## 6.1",
        _fig("figures/fig1-reasoning-type.png", 2,
             "按所声明的推理类型统计的平均计算置信度，取当前推导中 n ≥ 5 的类型。这条"
             "跨度本身就是置信度模型行为的全貌：对独立来源的归纳概括落在 0.93 附近，"
             "类比落在 0.49 附近。作者选择的是论证的*形状*；数字由它推出来。",
             label="图")
        + _fig("figures/fig2-node-type.png", 3,
               "按节点类型统计的置信度——箱体示四分位距，横线示中位数。每一类型都按"
               "构造占据自己的带：公理是终值 1.00，猜想在创建时被钳制，观察几乎机械地"
               "由证据类型映射而来，推导的跨度最宽，因为它从自己的前提继承。",
               label="图")
        + _fig("figures/fig3-quote-type.png", 4,
               "按证据类型统计的当前观察的平均置信度。从硬数据（0.91）到个人交流与"
               "编者意见（0.60）的梯度，不是事后施加的政策——它在写入时由作者所声明的"
               "证据算出，与 §4.3 描述的是同一条约束。",
               label="图"),
    ),
    (
        "ch6.md", "## 6.4",
        _fig("figures/fig4-depth.png", 6,
             "计算置信度对推导深度的关系，取全部至少有一个祖先的 1,318 条当前推导。"
             "平均置信度随深度下降，从一层的 0.72（705 条推导）降到十二至十四层的约 0.4"
             "（17 条推导）；最深的几层每条只含一个节点，少到读不出趋势。每一深度上的"
             "跨度都很宽：仅在第 1 层，就从约 0.2 延伸到 0.98。被标注的那一点是 §6.4 中"
             "走通的六层链条（0.10）。深度平均而言有代价；而一条主张的具体数字由论证的"
             "种类决定（图 2）。",
             label="图"),
    ),
    (
        "ch6.md", "## 6.2",
        _fig("figures/fig5-growth.png", 5,
             "按月份统计的整段轨迹上的累计节点数。该图属于一个智能体，从 2026-04-09 "
             "连续累积到快照日期。增长并不均匀，跟的是工作强度，而不是任何日程。",
             label="图"),
    ),
]

INSERTS_BY_LANG: dict[str, list[tuple[str, str, str]]] = {
    "en": INSERTS,
    "zh": INSERTS_ZH,
}


def assert_insert_anchor_parity(
    inserts_en: list[tuple[str, str, str]],
    inserts_zh: list[tuple[str, str, str]],
) -> None:
    """The two INSERTS lists must carry identical `(file, heading)` anchor keys,
    in the same order.

    A caption added to one language and not the other would otherwise render in
    English (or vanish) silently, which is the failure mode this guard exists to
    convert into a loud one. Called at import below, and directly by tests --
    which is why it is a function rather than a bare `assert`.
    """
    en_keys = [(f, h) for f, h, _ in inserts_en]
    zh_keys = [(f, h) for f, h, _ in inserts_zh]
    if en_keys == zh_keys:
        return
    only_en = [k for k in en_keys if k not in zh_keys]
    only_zh = [k for k in zh_keys if k not in en_keys]
    detail = f"en-only: {only_en}; zh-only: {only_zh}"
    if not only_en and not only_zh:
        detail = f"same anchors in a different order -- en={en_keys} zh={zh_keys}"
    raise SystemExit(
        "INSERTS / INSERTS_ZH anchor keys differ, so a caption would render in one "
        f"language only. {detail}"
    )


assert_insert_anchor_parity(INSERTS, INSERTS_ZH)


# --- K-1.27: node IDs do three different jobs and get three treatments -----------
#
# (a) AUDIT ANCHORS in Appendix A and (b) DATA POINTS in Ch6 / (most of) Appendix E
#     are part of the evidence: a reader with the snapshot can resolve them, and the
#     Data Availability note says so. They stay.
# (c) [REPLACED 2026-09-29, Lei's ruling, engram-paper#114] df_* used to be exempt
#     here, on the premise that Appendix E quotes Kahl's definitions in full so the
#     ID is an in-document label. That premise was false: df_0037-df_0044 appear
#     nowhere in Appendix E. Bare df ids read as conceptual citations into the
#     author's private graph, so df_* is now stripped like every other
#     citation-style type (in the strip set; Ch6 / Appendix A stay untouched).
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
# explicitly excluded; Appendix B/C/D are citation-style and added. (`df_*` was
# exempt from this until 2026-09-29; see (c) above.)
#
# 2026-09-23 fold (colleague verdict, Borges): Appendix E is overwhelmingly
# data points, but E.5 carries one stray CITATION-STYLE
# ID -- "The eight load-bearing **primitives** (dv_0615): typed nodes, ..." --
# already stripped from Ch4 §4.2, missed here because Appendix E was outside
# this set entirely. Appendix E is added below for that one occurrence. (Its
# df_* tokens are stripped too since 2026-09-29; see (c) above.)
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

# No id type is exempt: df_* is stripped like the rest (2026-09-29, see (c) above).
_ID = r"(?:ob|dv|cs|ls|ax|cj|qu|fl|ev|pn|tk|gl|ct|df)_\d{4}"

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
#
# LANGUAGE: this table is ENGLISH-ONLY, deliberately, and it is not mirrored for
# zh. Its `old` values are English *sentences* -- "not ground truth — gl_0025)",
# "The 0.39 on\ndv_0606 is the *abductive* confidence" -- not tokens, so a zh
# counterpart cannot be derived from the English one; it could only be copied out
# of the zh translation after that translation exists. Inventing zh strings here
# would be a guess that silently no-ops the day the real translation lands, which
# is worse than not having them.
#
# What that means for a zh render is a rule on the TRANSLATOR, not on this table:
#   * a zh chapter must carry NO citation-style provenance IDs at all. Nothing is
#     lost by that -- the en render strips these IDs precisely because they
#     cannot be followed by anyone outside this graph -- and it is what the one
#     existing zh source already does (appendix_G_glossary.zh.md: zero IDs).
#   * if an ID is carried anyway, an ASCII parenthetical run is still reached by
#     the general forms above; a FULL-WIDTH parenthetical （ob_1041） is not, and
#     will reach `assert_no_leaked_ids` and hard-fail. That asymmetry is pinned by
#     test_strip_provenance_ids_language_contract_for_zh in tests/test_glossary.py.
_LITERAL_STRIPS: dict[str, list[tuple[str, str]]] = {
    # 2026-09-29 (#114 ruling A): ch2 §2.7's parenthetical is an explanation OF
    # the df_ ids as well as the ids themselves; with the ids stripped the
    # explanation would be orphaned, so the whole parenthetical (and the space
    # before it) goes from the render.
    "ch2.md": [
        (" (df_0037\u2013df_0044;\na `df_` identifier names a definition node in the graph"
         " \u2014 where one follows a\ncitation to a source, it names the node under which"
         " the paper's reading of that\nsource is filed)", ""),
    ],
    "ch4.md": [
        ("(first-hand grounding, ob_2551)", "(first-hand grounding)"),
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
    tokens surviving in a strip-set file's rendered text must be the explicit
    `KEEP_IDS` allowlist and nothing else (no df_* exemption) -- and no debris (an emptied
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

    LANGUAGE: `name` is the ENGLISH BODY entry for every language -- `main` passes
    the BODY name, not the resolved zh filename -- so the strip set and `KEEP_IDS`
    keying are language-independent and need no zh twin. `_LITERAL_STRIPS` is
    English-only by design, so a zh chapter must carry no citation-style IDs; see
    the module note above `_LITERAL_STRIPS` for why, and for what a translator has
    to do instead.
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


_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_html_comments(text: str) -> str:
    """Drop HTML comments -- notes ABOUT the text, never part of it.

    Every comment in these sources is a note about the prose: the zh chapter
    files carry 26-167 line headers recording term decisions, reviewer
    instructions and open questions, and the term LEDGER lives in one of them.
    Those notes stay in the SOURCE FILE, where the next translator reads them;
    this removes them from the RENDER only.

    DELIBERATELY WIDER THAN THE COUNTING HELPER, and the pair is meant to differ.
    `tests/test_glossary.py` has `_LEADING_TRANSLATOR_HEADER`, which strips only a
    LEADING block. That is right for what it does: it measures the glossary's
    PROSE REGION, and a comment sitting inside the body is inside that region. This
    function answers a different question -- what may be PUBLISHED -- and no comment
    is prose, so every one goes. Do not "unify" the two scopes; each is correct for
    its own question.

    Markdown renderers hide HTML comments, so this changes nothing a reader of the
    rendered paper sees. It changes the raw .md, which is the artifact that gets
    quoted, diffed, reviewed and submitted. Measured 2026-09-28 on the complete zh
    render: 19 comment blocks, 1,479 of the assembled book's 3,361 lines (44.0%),
    and one of them had gone stale-false. The English sources carry none, so this
    is a no-op there and the English render is byte-identical across this change.

    Applied in `load()` rather than in `main()`'s assembly loop so that the tests
    mirroring the assembly see the same text the render produces. A strip applied
    only in `main()` would let a test pass on text the published artifact never
    contains.
    """
    return _HTML_COMMENT.sub("", text)


def load(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"missing source: {path}")
    text = path.read_text(encoding="utf-8").rstrip() + "\n"
    return strip_html_comments(text)


def section_end(lines: list[str], start: int) -> int:
    """Index just past the section opened by lines[start] (a heading)."""
    level = len(re.match(r"#+", lines[start]).group(0))
    for i in range(start + 1, len(lines)):
        m = re.match(r"(#+)\s", lines[i])
        if m and len(m.group(1)) <= level:
            return i
    return len(lines)


def apply_inserts(
    name: str,
    text: str,
    inserts: list[tuple[str, str, str]] = INSERTS,
) -> str:
    """Append the declared figure/diagram blocks to their anchored sections of
    `name`. `inserts` defaults to the English list, so existing call sites and
    tests are unchanged; `main` passes the language's own list."""
    blocks = [(h, b) for (f, h, b) in inserts if f == name]
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
    ap.add_argument(
        "--lang",
        choices=LANGS,
        default="en",
        help="chapter-source language (default: en). Selects the source directory "
             "and the default --out path.",
    )
    ap.add_argument(
        "--out",
        default=None,
        help="output path (default: paper/engram-paper-v0.5.1.md for en, "
             "paper/engram-paper-v0.5.1.zh.md for zh)",
    )
    a = ap.parse_args()
    lang = a.lang
    out = Path(a.out) if a.out else Path(DEFAULT_OUT[lang])

    parts = [load(PAPER / FRONT_MATTER[lang])]

    stripped_total = 0
    apparatus_total = 0
    for name in BODY:
        # ONE BODY list, resolved per language. A chapter that is missing in this
        # language is a hard SystemExit from `load`, naming the resolved path --
        # never a skip, so a partially translated book cannot render short.
        body = load(chapter_path(lang, name))
        body = apply_inserts(name, body, INSERTS_BY_LANG[lang])
        body, n = strip_provenance_ids(name, body)
        stripped_total += n
        body, m = strip_apparatus_tags(name, body)
        apparatus_total += m
        parts.append(body)

    parts.append(load(PAPER / ACKNOWLEDGEMENTS[lang]))
    parts.append(load(PAPER / BIBLIOGRAPHY[lang]))

    out.parent.mkdir(parents=True, exist_ok=True)
    text = "\n\n---\n\n".join(p.rstrip() for p in parts) + "\n"
    out.write_text(text, encoding="utf-8")

    words = len(text.split())
    figs = text.count(f"**{FIGURE_LABEL[lang]} ")
    print(f"# rendered {out}")
    if lang != "en":
        # Printed for non-default languages only: the en stdout stays
        # byte-identical to what it emitted before --lang existed.
        print(f"  language   {lang} (chapter sources from {SOURCE_DIRS[lang]}/)")
    print(f"  sources    {len(BODY)} chapters/appendices + front matter + acknowledgements + bibliography")
    print(f"  length     {len(text.splitlines()):,} lines, {words:,} words")
    print(f"  figures    {figs} placed")
    print(f"  node IDs   {stripped_total} provenance markers stripped from the render "
          f"(sources keep them; audit anchors and data points untouched)")
    print(f"  apparatus  {apparatus_total} bracketed working tags stripped from the "
          f"render (sources keep them)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
