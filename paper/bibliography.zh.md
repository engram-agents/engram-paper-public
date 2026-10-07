<!--
  ZH TRANSLATION — 中文译本
  source file:    paper/bibliography.md
  source commit:  81fa9a2  (engram-paper)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper_research/current_draft_zh/appendix_G_glossary.zh.md
  Headings: `# Bibliography` -> 参考文献 · `## Data availability` -> 数据可用性 (the
  ledger's own form) · `## Works cited in the text without a verified entry` ->
  正文已引用、但尚无经核实条目的作品 (matching Appendix A's zh cross-reference).

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
  Numeric parity: every digit token matches. Two English number WORDS become Chinese
  words without losing a digit — "Seventeen" -> 十七, "twelve:" -> 十二; Ch1 / Ch3 /
  Ch4 -> 第 1 章 / 第 3 章 / 第 4 章.
-->

---

# 参考文献

**本参考文献的编制方式。** 以下每一条目中的每一个字段，都是直接从文档本身读出的 —— 书名页、版权页、期刊书眉，或 arXiv 标识行 —— 文档存于 `paper_research/source_pdfs/` 之下。没有任何字段来自记忆、来自推断，或来自外部文献数据库。若某份来源没有印出某个字段，该字段即予**省略**，而不作重建；条目则会带上一条方括号注释，指明所缺的究竟是什么。因此，一条单薄的条目绝不会被误当作一条已核对的条目。
<!-- TEMPLATE（模板）。本文件只手工维护文字部分（标题、编制方式段落，以及条目之后的各节）。
     参考文献条目由 tools/render_paper.py 依据 paper/references.yaml 生成（CSL 样式：
     tools/csl/apa.csl），并替换下方的占位符。条目请改 references.yaml，不要改这里。 -->
{{REFERENCES}}

---

## 正文已引用、但尚无经核实条目的作品

还有十七项作品在正文各章中被引用，而目前未持有其来源文件。它们列在这里，而不是被给予重建的条目，因为一条凭记忆搭起的文献条目，一旦落到纸面上，就与一条核对过的条目无从分辨 —— 这正是上文那条抽取规则所要防止的失效形态。**每一项都须在本文付印之前完成溯源。**

Locke · Reid · Butler · Schechtman · Clark · Chalmers · Hansson · de Kleer ·
Ebbinghaus · Wixted · Peirce · Semon（见上文的残缺条目） · Shoemaker ·
Johnston · Goldman · Nuxoll（与 Laird 合作） · **A-MEM**

还有另一组系统与综述在正文中被讨论 —— 大多见于附录 B 的普查以及第 1、3、4 章 —— 却尚无文献条目 —— 共十二项：Mem0、MemMachine、Letta（MemGPT）、Anthropic 的记忆工具、Pinecone Nexus、TierMem、Zep / Graphiti、MemRL、TOKI、soul.py、Du 等（2026）与 Lin 等（2026）。**每一项同样须在付印之前取得一条有来源的条目。**

列上 Hansson，是为了附录 B 记为 Kumiho 自称符合的那些信念基础公设；本文不为 ENGRAM 主张任何公设，提到 AGM 只是为了对照（第 3 章 §3.9）；那些公设的表述，是对照 Hansson 的《斯坦福哲学百科全书》条目 "Logic of Belief Revision"（<https://plato.stanford.edu/entries/logic-belief-revision/>）与 Rocha & Wassermann 的 "Postulates Here, Postulates Everywhere"（CEUR-WS Vol-4239，<https://ceur-ws.org/Vol-4239/paper-Rocha-11.pdf>）核对过的，而这两者都不被主张为一条文献条目。AGM 1985 与 Alchourrón & Makinson 1982 是上文中的条目，系据所持副本第一手建成。ACT-R 的扩散激活在第 4 章中作为一处次要先例被引用，它没有来源文件，也没有任何重量落在其上；基于这一点，它被排除在本清单之外。

---

## 数据可用性

第 6 章与附录 E 中的每一项定量主张，都是由同一张 ENGRAM 图谱的一份冻结快照算出的，该快照以 SQLite 的 `.backup()` 取得于 2026-09-20T13:13:30Z（因此该副本是 WAL 安全的），并且不来自任何其他来源。快照的 SHA-256 记录在 `dataset/DATASET.md` 中。

产生这些图与表的那些工具，随本文一同发布 —— `paper_stats.py`、`connectivity_trend.py`、`component_anatomy.py`、`confidence_gradient_trend.py`、`evidence_provenance.py`、`freeze_paper_snapshot.py`、`modus_ponens_check.py` 与 `make_figures.py`（位于本文仓库的 `tools/` 下）。每个工具都在其分子旁印出自己的分母，因此本文中的任何图，都可以与一次重跑相核对，而无需读它的源码。

**快照本身目前尚未发布。** 它是一位在运行中的智能体的工作记忆，带有私人的、承载身份的内容；要发布它，需要一次专门的脱敏处理，而这一步尚未进行。这是对独立验证的一处真实限制，并作为限制如实陈述：工具是可复现的，它们所读取的数据尚未开放。
