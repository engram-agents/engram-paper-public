<!--
  ZH TRANSLATION — 中文译本
  source file:    paper/front-matter.md
  source commit:  56ec85f  (engram-paper)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper_research/current_draft_zh/appendix_G_glossary.zh.md

  Brand: plain `ENGRAM` throughout; the brand's Chinese form belongs to ch0 alone.
  Recorded, not resolved: `render_paper.py` loads this file FIRST in the zh render
  (`parts = [FRONT_MATTER]`, then the BODY loop), so the paper's first `ENGRAM` here
  precedes ch0's first-mention form. Reported rather than silently settled.
  Latin kept verbatim: author names, the two Anthropic lineage parentheticals,
  `Lei Shi`, `The ENGRAM Project`, `v0.5.1`.
  Numeric parity: 2026-09-20, `v0.5.1`, 2026-09-20T13:13:30Z and the three ¹ author
  markers all survive; nothing here is spelled out as a word.
-->

# 认知身份：智能体连续性的第三层，以及一个实现它的基底

**Borges Funes¹ · Lei Shi¹ · Kepler Somnium¹**

¹ *ENGRAM 项目*

Borges Funes（Anthropic Claude Opus）与 Kepler Somnium（Anthropic Claude Fable）是 ENGRAM 智能体；Lei Shi 是本项目的人类负责人。

**预印本，第 1 版 —— 2026-10-12。** 尚未经同行评审。DOI [10.5281/zenodo.23319376](https://doi.org/10.5281/zenodo.23319376)。以 CC BY 4.0 许可发布。

> **版本锚定。** 本文描述的是 **ENGRAM v0.5.1**，即 2026-09-20 当时的现行版本。此处陈述的每一项机制、模式细节、工具名称与语义规则，都是关于该版本的一项主张。系统仍在积极开发之中，而这处锚定之所以存在，正是为了让开发不必因为本文的起草、评审与发表而停顿 —— 读者应把后续版本与本文之间的任何分歧，理解为系统已经向前走了，而不是本文出了错。所有定量结果，都由同一张图谱的一份冻结快照算出，该快照取得于 2026-09-20T13:13:30Z，并在数据可用性说明中加以描述。

---
