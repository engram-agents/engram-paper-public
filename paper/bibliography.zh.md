<!--
  ZH TRANSLATION — 中文译本
  source file:    paper/bibliography.md
  source commit:  81fa9a2  (engram-paper)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper/chapters/zh/appendix_G_glossary.zh.md
  Headings: `# Bibliography` -> 参考文献 · `## Data availability` -> 数据可用性 (the
  ledger's own form).

  TRANSLATED: the three section headings; the free-standing prose blocks; and the
  italic-bracketed `*[...]*` note apparatus on 16 entries — our own sentences about
  the sources, set off from the entry, not bibliographic fields.
  NOT TRANSLATED: every entry's own text stream, byte-for-byte — author names,
  titles, journals, publishers, DOIs, URLs, arXiv IDs, years, page numbers,
  affiliations, edition histories. A translated title is no longer a citation a
  reader can look up.
  LEFT ENGLISH, named so it is not read as an oversight: the Alchourrón 1985 entry's
  inline CCC fee-code/ISSN note, and the Doyle entry's Crossref parenthetical. Both
  sit in their entry's field stream rather than in a delimited note block, so the
  entry-verbatim rule governs them; the brief's tiebreak ("when in doubt, leave it
  English") decides it that way.
  Entry count: 22 in the English source; unchanged, since the bodies are verbatim.
  Numeric parity: every digit token matches. One English number WORD becomes a Chinese
  word without losing a digit — "Two" -> 两.
-->

---

# 参考文献

**本参考文献的编制方式。** 以下每一条目中的每一个字段，都是直接从文档本身读出的 —— 书名页、版权页、期刊书眉，或 arXiv 标识行 —— 文档为作者所持有的副本。许可允许再分发的副本发布于本文仓库的 `bibliography/sources/` 之中；其余副本出于版权原因私下保存。没有任何字段来自记忆、来自推断，或来自外部文献数据库。若某份来源没有印出某个字段，该字段即予**省略**，而不作重建；条目则会带上一条方括号注释，指明所缺的究竟是什么。因此，一条单薄的条目绝不会被误当作一条已核对的条目。
<!-- TEMPLATE（模板）。本文件只手工维护文字部分（标题、编制方式段落，以及条目之后的各节）。
     参考文献条目由 tools/render_paper.py 依据 paper/references.yaml 生成（CSL 样式：
     tools/csl/apa.csl），并替换下方的占位符。条目请改 references.yaml，不要改这里。 -->
{{REFERENCES}}

---

## 数据可用性

第 6 章与附录 E 中的每一项定量主张，都是由同一张 ENGRAM 图谱的一份冻结快照算出的，该快照以 SQLite 的 `.backup()` 取得于 2026-09-20T13:13:30Z（因此该副本是 WAL 安全的），并且不来自任何其他来源。快照的 SHA-256 记录在 `data/DATASET.md` 中。

产生这些图与表的那些工具，随本文一同发布 —— `paper_stats.py`、`connectivity_trend.py`、`component_anatomy.py`、`confidence_gradient_trend.py`、`evidence_provenance.py`、`freeze_paper_snapshot.py`、`modus_ponens_check.py` 与 `make_figures.py`（位于本文仓库的 `tools/` 下）。每个工具都在其分子旁印出自己的分母，因此本文中的任何图，都可以与一次重跑相核对，而无需读它的源码。

**快照的内容没有发布，也不会发布。** 它是一位在运行中的智能体的工作记忆，带有私人的、承载身份的内容。发布的是同一份快照的**仅含结构的版本**，即 `data/engram-paper-ssot-20260920T131330Z.stripped.db`，由 `tools/strip_paper_snapshot.py` 从快照生成，与该工具及其测试一同放在本文的仓库中（https://github.com/engram-agents/engram-paper-public；3,690,496 字节；SHA-256 `962d0c00c0c6388a5fcc1bcda5f6424de2979d19ed1c8624f9579210db0e1b5a`）。它保留节点与边的标识、节点类型、状态及是否为当前版本、精确到整秒的创建时间、置信度、证据类型标签、推理类型与来源类别标签，以及完整的边结构；不保留任何主张文本、引文、标题、人名、网址或来源。上述工具为第 6 章印出的每一个数字，都可以从这个版本复现，一个已提交的测试会对照记录下的数值（`data/expected_stats.json`）加以核对。有两类结果无法从中复现：依赖主张文本的结果，以及与图谱早期历史的比对（`connectivity_trend.py --validate-git`），后者读取的是私有记录。`data/DATASET.md` 逐项列出了这个版本保留和删去的内容。

第 6 章与附录 E 中的图表仍然是在一个智能体的图谱上所做的演示，而不是一项基准。对这些主张本身的独立检验，将来自脱敏后的数据，或来自一位为研究而专门培育的智能体。
