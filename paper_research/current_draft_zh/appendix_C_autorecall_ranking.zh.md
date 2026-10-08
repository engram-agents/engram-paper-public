<!--
  ZH TRANSLATION — 中文译本
  source file:    paper_research/current_draft/appendix_C_autorecall_ranking.md
  source commit:  6e64802  (engram-paper, 2026-09-28)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper_research/current_draft_zh/appendix_G_glossary.zh.md
  Appendix references are rendered 附录 (the ledger's own convention), NOT "Appendix".
  Chapter pointers are rendered 第 N 章 (Ch4 -> 第 4 章, Ch7 -> 第 7 章); section
  pointers (§4.5, §7.2) are kept verbatim — the ledger's pointer grammar knows the §
  form in both languages.

  NO PROVENANCE NODE IDS — this file IS in render_paper.py's STRIP_PROVENANCE_IDS_IN, so
  a citation-style ID carried across trips `assert_no_leaked_ids` and HARD-FAILS the
  build. (Worse than in an ungated file: a full-width parenthetical is not even reached
  by the stripper's ASCII forms, so it can only fail.) The English source carries SIX
  citation-style IDs, every one of them parenthetical, and all SIX are DROPPED here with
  their parenthetical:
    * FOUR `ob_` IDs — §C.1 (twice: the MemRL prior-read pair), §C.3 (the composite
      amplifier), §C.5 (the NDCG tuning result).
    * TWO `dv_` IDs — §C.2 (the utility_score definition), §C.3 (the `_search_nodes`
      pipeline).
  None of the six is a data point of the kind `KEEP_IDS` protects (ch7's trace example);
  every one is a citation hung on someone else's claim, which is exactly what the en
  render already strips — so nothing is lost to the zh reader. NO `df_*` label appears
  in this appendix. (Written WITHOUT their digits ON PURPOSE: this header is part of the
  file the stripper reads, so a literal ID in the note above would itself trip
  `assert_no_leaked_ids` — the same trap appendix B's header documents for itself.)

  NUMERIC PARITY — every digit token survives except the four digits of each of the six
  dropped IDs above (six EN-only tokens, measured on the bodies with this header
  excluded; the zh side adds none); no number is spelled as a word here.
  The two formulas are reproduced BYTE-IDENTICAL, including the code block's leading
  alignment (line 2's `×` sits under line 1's `×`, so the three-factor product reads
  unambiguously as one product and not as a sum — the appendix's whole point is that
  these are multipliers, so the grouping IS the claim):
      composite = relevance × (1 + UTIL_BETA × utility_score)
                            × (1 + IMP_BETA × normalized_importance)
  The inline rules `Q_new = Q_old + α(1 − Q_old)`, `(1−α)^t` and `(1−λ)·relevance +
  λ·utility` are likewise verbatim, as is the α column (0.15 / 0.10 / 0.05). CONSTANTS
  THE MS CARRIES: 2026 · 2026-05-19 · 0.15 · 0.10 · 0.05 · UTIL_BETA = 0.10 ·
  IMP_BETA = 0.005 · MMR_LAMBDA = 0.9 · UTILITY_LAMBDA = 0.3 · Q=1 → 1.10× ·
  ≈0.05 NDCG · §4.5 · §7.2 · §4.7 · tiers 2／3 · stage 2.

  COINAGES — first use in this file carries the English, per the ledger's rule:
    harness -> 承载框架（harness）. FIRST occurrence is §C.5's "harness-calibrated";
      the later use (the recall-measurement harness) writes plain 承载框架.
    sweep   -> 普查, per the ledger. ONE SENSE STRETCH, flagged rather than silently
      resolved: §C.5's "NDCG sweep" is a PARAMETER scan (a tuning search over constant
      values), which is neither sense the ledger's entry names (the dated first-hand
      survey; the "landscape sweep"). The ledger binds 普查 to the English lemma `sweep`
      uniformly and every other sweep-site in this paper reads 普查, so the binding is
      followed here — but a reviewer may prefer 扫描 at this one site, and that is a
      ledger decision, not this translator's.

  DELIBERATE RENDERING CHOICES a reviewer should look at:
  1. `utility_score` stays a Latin identifier everywhere, §C.2's heading included (field
     name; house rule). The PROSE sense is 效用分, matching ch4.zh.md §4.7 ("一个从使用
     中学得的效用分") and the ledger's 效用（效用分）entry.
  2. "engaged with" -> 被互动, and "engagement proxy" / "engagement actions" ->
     互动代理指标 / 互动行为 — one stem for one English stem, so §C.2's middle band and
     §C.5's second qualification stay visibly the same concept.
  3. §C.3's three stage names are kept as 中文（English）labels — 汇聚（Gather）／
     合成重排（Composite re-rank）／多样性（Diversity） — because they are code-path stage
     names a reader may want to match against `_search_nodes`.
  4. `stop-hook` -> 停止钩子（stop-hook） at its single occurrence.
  5. Every CLI verb in the α table (`derive`, `inspect`, `focus_load`, …) stays Latin
     per the house rule on identifiers; the table's other two columns are translated.
  6. §C.5's "Honest scope" is translated (it is a section heading here, not one of
     appendix B's `*honest scope:*` drafting markers) -> 诚实的范围.

  ENGLISH ODDITIES FOUND — recorded, NOT fixed (the task asks for them):
   a. §C.3: "let each amplifier scale from 0 to a bounded gain." An amplifier of the
      form (1 + β·x) scales from **1**, not from 0 — read literally, a zero-utility node
      would be multiplied by zero and vanish. The sentence only works if "scale from 0"
      means the BOOST above 1, which the next clause ("a 1.10× boost") does support. So
      it is resolvable, but the two readings differ on whether a zero-utility node
      survives the product at all.
   b. §C.3: the bounded-gain demonstration is given for the utility amplifier only
      (Q = 1 -> 1.10×). `normalized_importance`'s range is never stated anywhere in this
      appendix, so `(1 + 0.005 × normalized_importance)` has NO stated bound — the
      plural "each amplifier" outruns its evidence by one.
   c. §C.5: the constants were tuned "by an NDCG sweep", but NDCG is defined against
      relevance judgments and the appendix never says what the ground truth for that
      sweep was. It is the appendix's one measurement claim and its instrument is
      unnamed.
   d. §C.3: MMR_LAMBDA = 0.9. Under the usual MMR form (λ·sim(d,q) − (1−λ)·max
      sim(d, selected)), λ = 0.9 puts only 10% of the weight on diversity, which sits a
      little awkwardly beside "trims near-duplicates". Not a contradiction — it still
      trims — but the constant reads as a weak-diversification setting. The convention
      is not stated, so this is flagged, not asserted.
   e. §C.2: pinning (`focus`) is in the 0.10 band ("or pinned") while `unfocus`, its
      inverse, is in the 0.05 "loose touch" band. Defensible (choosing vs releasing),
      but the asymmetry goes unremarked in the prose.

  RANKS vs SCORES — checked as asked, since this appendix is a ranking one:
   * The α table's three bands are ordered 0.15 > 0.10 > 0.05 top-to-bottom, and every
     cross-reference agrees with it: "top band" = 0.15 ("no retrieval verb at all"),
     the middle band = 0.10 (`inspect`), the "loose touch" band = 0.05.
   * "`inspect` … sits in the middle band, below `derive`" — `derive` is in the 0.15 row,
     `inspect` in the 0.10 row. FOLLOWS.
   * The two convergence statements agree with each other: `Q_new = Q_old + α(1 − Q_old)`
     is a fixed-step EMA toward Q = 1 whose error is (1−α)^t — exactly §C.1's stated
     decay — and Q ≤ 1 at every step, which is what makes §C.1's "non-decreasing" true.
   * The 1.10× boost follows from the formula at Q = 1 with UTIL_BETA = 0.10. FOLLOWS.
   * §C.5's "0.10, 0.005 and 0.9" maps onto "UTIL_BETA, IMP_BETA, and MMR_LAMBDA" in
     that order. FOLLOWS.

  BRAND — the paper is ONE surface, so 心迹（ENGRAM） appears once, in ch0; this appendix
  writes plain `ENGRAM` in running text throughout, per the ledger header and
  docs/ZH-TERMINOLOGY.md.

  Proper nouns stay in Latin script — MemRL, and the author surname Lei. So do the
  identifiers `utility_score`, `_search_nodes`, `UTIL_BETA`, `IMP_BETA`, `MMR_LAMBDA`,
  `UTILITY_LAMBDA`, `normalized_importance`, `Q_new`, `Q_old`, `Q`, `α`, `λ`, `EMA`,
  `FTS`, `MMR`, `NDCG`, and the CLI verbs in the α table.
-->

# 附录 C —— 自动回忆排序与记忆效用传统

---

## C.1 记忆效用传统

2026 年的一脉工作——以 **MemRL**[@zhang2026, p. 1]为典范——把强化学习用在模型的**记忆检索**上，而不是用在它的权重上：它把检索当作一个动作、把下游的有用性当作奖励，从而学出*哪些存储下来的记忆值得浮现*，并按一个学得的 **Q 值**给记忆排序。它的吸引力在于：它让基座模型保持冻结——不微调，因此没有灾难性遗忘——却仍在*什么会被回忆起来*这一层面上随时间改进。具体地说，MemRL 把一个 EMA 学得的 Q 值与语义相似度经一个加权分数合成，其中 Q 误差按 `(1−α)^t` 衰减[@zhang2026, pp. 4–5, 13]。

ENGRAM 属于这一传统。每个节点都带一个 `utility_score`——一个按同一条指数规则更新的学得值，`Q_new = Q_old + α(1 − Q_old)`——而排序把那个学得的值与语义相关性合成，而不是只按相关性排序。不同之处在奖励：MemRL 从任务结果中学，而 ENGRAM 从**智能体拿到该节点之后对它做了什么**中学——这个信号基底可以直接观察到，并且可以无歧义地归因。这条规则没有负项：一次被证明无用的回忆会让该节点的效用停在原处，所以 `utility_score` 是非递减的。要把无用的节点降级，需要一个当前规则所没有的惩罚项；我们把它列为一项局限（§7.2）。

## C.2 ENGRAM 的 `utility_score` —— 一个学得的值，按它所挣得的那次行为来评定

ENGRAM 的 `utility_score` 是 Q 值的对应物，而它评定的是**一个节点所参与的那次行为的认知负荷**——而不是智能体找它找得有多用力。学习率 α 以行为为键，分三档：

| α | 行为 | 该档的含义 |
|---|---|---|
| **0.15** | `derive`、`supersede`、`contradict`、`resolve`、`register_exemplar` | 该节点参与了一次**认知行为**——它成为前提、驱动了一次修订，或锚定了一条教训 |
| **0.10** | `inspect`、`subgraph`、`mention`、`focus`、`history`、`citation` | 该节点**被互动**——被仔细阅读、被遍历、在推理中被指名，或被钉住 |
| **0.05** | `focus_load`、`unfocus` | **松散接触**——该节点是随一个集合一起移动的，而不是被选中的 |

当一个节点经由多条路径被触达时，*取最大 α 者胜*。

注意最高档里没有的是什么：**一个检索动词都没有。** 其中每一个都是智能体在*拿到*一个节点之后*对它做*的某件事。这张表测量的不是花在"找"上的注意；它测量的是"找"产出了什么。`inspect`——读一个节点最刻意的方式——落在中间档、低于 `derive`，因为仔细阅读与随后在其上建造是两种不同的成就。

**有两条独立的路径授予得分**，而第二条比它看起来更重要。第一条是引用：在一个新推导中把一个节点指名为前提。第二条是一个停止钩子（stop-hook），它扫描智能体自己每一轮，并给其中**被提及**的任何节点记上 α = 0.10 的得分。仅有第一条路径是最初的设计，而它被证明太窄：它漏掉了散文式提及、行内引用，以及那种明显受某个节点启发、却没有正式引用它的推理。一个塑造了论证却未被引用其中的节点，仍然是有用的，而基底现在看得见这一点。

这就是*访问频次*（一个向量存储能追踪的东西）与*认知有用性*（要求知道那次回忆随后做了什么）之间的差别——正是这一区分，把 ENGRAM 的排序放进记忆效用传统，而不是朴素检索的那个传统。

## C.3 合成排序 —— 三层流水线上的乘法放大器

生产环境中的回忆跑一条**三阶段**的 `_search_nodes` 流水线：

1. **汇聚（Gather）** —— FTS 与语义嵌入的合并产出候选节点，各带一个基础**相关性**分。
2. **合成重排（Composite re-rank）** —— 本附录所讲的那个阶段。
3. **多样性（Diversity）** —— 一趟 MMR（最大边际相关性）过滤（MMR_LAMBDA = 0.9）裁掉近重复项，使浮现出来的集合不至于是同一条主张的九种改写。

合成（第 2 阶段）用的是**乘法放大器**，而不是加法混合：

```
composite = relevance × (1 + UTIL_BETA × utility_score)
                      × (1 + IMP_BETA × normalized_importance)
```

在当前的生产环境中取 `UTIL_BETA = 0.10`、`IMP_BETA = 0.005`。设计理由（Lei，2026-05-19）就是那个吃重的论点：**相关性是基础的主题信号；效用与重要性是正交维度上的*放大器*，不是地位等同的加数。** 一个加法混合 `(1−λ)·relevance + λ·utility`（已退役的形式，UTILITY_LAMBDA = 0.3）需要小心的 λ 调参，以免效用把相关性*淹没*；乘法放大器保全相关性的主导地位，并让每个放大器从 0 缩放到一个有界增益（一个效用拉满的节点，Q=1，得到 1.10× 的提升）。重要性放大器是**稳态的（homeostatic）**——`normalized_importance` 锚定在当前的可查询最小重要性上，所以这个公式随图谱增长而自适应，而不是使用一个固定标度。

## C.4 重要性、遗忘与间隔重复

还有两个信号与排序相互作用。**重要性**把关*层级资格*——按遗忘机制（第 4 章 §4.5），它是一个预过滤器，决定什么才够格进入可查询集（第 2 层）而不是淡出集（第 3 层）——随后作为第二个放大器进入合成式。而回忆本身*强化*一个节点（回忆计数／回忆轮次这两个信号），所以一个持续证明自己有用的节点，既被保留得更久，也被排得更高：这就是**测试效应**的形态，其中检索不是一次只读事件，而是强化那条痕迹[@roediger2006, p. 249]。结果是一个在三条耦合轴上自适应的回忆面——主题相关性、学得的有用性，以及衰减中的重要性——而不是一次静态的相似度排序。

## C.5 诚实的范围

两条诚实的限定，两者都与本文的姿态一致：

- **这些常数是经承载框架（harness）校准的，不是从第一性原理推出的。** UTIL_BETA、IMP_BETA 与 MMR_LAMBDA 是在一个本地回忆测量承载框架上、经一次 NDCG 普查调出的，那次普查把它们定为 0.10、0.005 和 0.9，并比未调参的取值多得了 ≈0.05 NDCG。它们*被测量为排序良好*，这比置信度模型的常数（第 7 章 §7.2——那些常数*没有*经过结果校准）立足更稳——一处有用的内部对照。
- **奖励信号是一个互动代理指标，而不是真正的结果：** 效用是从 C.2 所列的那些互动行为（引用是其中之一）中学得的，而这些行为没有一项核实被回忆的那个节点是对的。一个更完整、基于结果的奖励（下游主张是否挺过了矛盾？）是一个未来方向，与置信度自动校准这条线索（第 7 章 §7.2）相连续。

**→ 第 4 章 §4.7** 提出主张；本附录是细节。
