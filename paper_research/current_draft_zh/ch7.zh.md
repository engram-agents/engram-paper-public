<!--
  ZH TRANSLATION — 中文译本
  source file:    paper_research/current_draft/ch7.md
  source commit:  6e64802  (engram-paper, 2026-09-24)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper_research/current_draft_zh/appendix_G_glossary.zh.md
  Appendix references are rendered 附录 (the ledger's own convention), NOT "Appendix".
  Chapter pointers are rendered 第 N 章 (Ch4 -> 第 4 章); section pointers (§7.3, §4.5)
  are kept verbatim — the ledger's pointer grammar knows the § form in both languages.
  A bare appendix-section pointer in the English ("(E.4)", "Appendix C §C.1") is
  written 附录 E §E.4 / 附录 C §C.1, the form ch4.zh.md already ships.

  PROVENANCE IDs — ZERO CITATION-STYLE ones, and this chapter is the one where that rule
  costs something. (The body carries FOUR ID tokens — two distinct IDs, each twice — all
  in §7.2's worked example: they are the two `KEEP_IDS` entries, kept because the English
  render keeps them; see THE ONE KEPT SITE below. Measure with a grep for
  `[a-z]{2}_[0-9]{4}` over the body.)
  `render_paper.py` strips citation-style node IDs from the ENGLISH render with a
  literal-sentence table that is ENGLISH-ONLY by design (module note above
  `_LITERAL_STRIPS`), so the obligation moves onto the translator: a zh chapter must
  carry no citation-style ID. Every parenthetical the English carries is therefore
  DROPPED, with any surrounding free-text gloss kept. This file also carries no `df_*`
  label, because ch7 has none in the English.
  THE ONE KEPT SITE, disclosed. §7.2's worked example is the ONLY place in the paper
  where the English render deliberately KEEPS two node IDs: the `KEEP_IDS` allowlist in
  render_paper.py holds the mis-typed step and the conclusion it fed, as DATA POINTS
  rather than citations, and the inline-code command `tools/paper_stats.py --trace <id>`
  depends on one of them. This file mirrors the English there: both IDs are kept, so the
  zh reader can re-run the trace the English reader can. That is the ledger's third
  carve-out (appendix_G's header): an ID the engine keeps for a file is kept here too.
  An earlier draft of this file dropped both and described the step instead; that draft
  is gone, and this paragraph replaces its note.

  BRAND — plain ENGRAM throughout running text; the two-character Chinese brand form
  for ENGRAM does not appear on this surface. This follows the normalisation recorded
  in ch1.zh.md's own header (the paper is ONE surface, so the brand form stands once,
  in ch0) and in docs/ZH-TERMINOLOGY.md in engram-alpha — and this file does not even
  name that form in this comment, per the chapter instruction that it belong to ch0
  alone. No first-mention coinage line is needed: ch7 uses NONE of the ledger's
  three approved coinages — harness, sweep and seat all have zero occurrences in this
  chapter's English source.

  QUOTED ENGLISH IS TRANSLATED, following ch1.zh.md's practice: Lin 等 2026's "anchored
  in storage-time provenance" and its "Forget & Rollback" lifecycle phase, the
  diagnostic prompt in §7.3, and every phrase the §7.0/§7.4/§7.7 arguments quote all
  carry their Chinese rendering. Kept verbatim: the field names (`standpoint_author_id`,
  `_collection_id`, `_override_tag`, `_lineage`, `_architecture`), the identifier
  `utility_score`, the CLI command, and `super-engram` / lowercase `engram` (the ledger
  keeps lowercase `engram` in English as a technical term; "super-engram" is a compound
  built on it — see the reviewer note below).

  NUMERIC-PARITY NOTE, measured not assumed, and it is the mirror of ch4.zh.md's note.
  A multiset comparison of digit tokens between this file and its English source
  (headers excluded on both sides) returns differences in ONE direction only: EN has
  digit tokens with no zh counterpart, and every one of them is a NODE-ID FRAGMENT —
  the four digits of an identifier this file was required to drop. Every substantive
  number survives as a digit: §-pointers, 0.7, 0.20, 0.91, 0.14, 0.10, 9,399, 2.3%,
  0.01%, 0.2%, 1.6%, 1.1%, 81%, 87%, 17, 第 4 层, 2026-06-17, v0, v0.5.1. The three
  count words the English spells out as words ("three limitations", "Five fields",
  "three properties") stay word-form in Chinese (三项 / 五个 / 三个), so they introduce
  no digit on either side. Any drift-detector built on `[0-9]` runs must whitelist the
  ID-fragment class or it will report false errors on every run.

  DELIBERATE RENDERING CHOICES a reviewer should look at:
    - coherence / correspondence -> 融贯 / 符合 (§7.3's load-bearing pair; neither word
      has a prior zh rendering in this paper). "systematic single-standpoint bias" ->
      系统性的单立场偏差; "standpoint-uniform" -> 立场齐一 (all from one standpoint, kept
      distinct from 一致, "consistent"); "standpoint" -> 立场.
    - base-model "lineage" -> 谱系 (ch1/ch4 use 谱系 for a tradition's genealogy; ch5's
      世系 is reserved for ancestry in the identity argument). `_architecture` -> 架构.
    - "disposition" -> 性向, carrying ch3.zh.md's fixed form ("dispositional durability"
      -> 性向上的持久), so §7.1 reads as the same term ch3 used.
    - "vacuity" -> 空置 and "scalar-only-consumer" -> 只消费标量的面, both fixed in ch4.zh.md.
    - "precision" / "accuracy" -> 精密度 / 准确度 (the measurement pair; 精度 alone would
      blur them) · "biased sensor" -> 有偏的传感器 · "calibration" -> 校准
    - "yellow-card" / "red-card" -> 黄牌 / 红牌 (the disciplinary metaphor is transparent
      in Chinese) · "aggregator" -> 聚合器 · "per-domain flags" -> 按域的标志
    - "constitutional contracts" -> 宪制契约 · "dark matter" -> 暗物质 · "generation
      effect" -> 生成效应 (ch3.zh.md's form) · "testimony" -> 证言 · "decompressor" -> 解压器
    - "conviction-bar resolution" -> 达到确信门槛的解决 · "off-board" -> 体外 · "the
      objection proves too much" -> 这个反驳证明了太多
    - "super-engram" and lowercase "engram" stay LATIN, per the ledger's rule for the
      lowercase sense (§7.1's "engram 与权重之间的对应", "从 engram 内化") and for a
      compound built on it (§7.2, §7.5). A reviewer who wants a Chinese rendering for
      "super-engram" should say so — it is Lei's coinage and this file does not invent
      a translation for it.
    - "pack" -> 包（pack） on first use (§7.5; an exportable bundle), then 包.
    - Quotation marks are ASCII " " and ' ', matching ch1.zh.md.
-->

# 第 7 章 —— 意涵与未来方向

---

## 7.0 本章做什么

在论证了 ENGRAM 越过一道很高的门槛之后，我们欠读者两份交代：这套架构在何处*不完整*，以及它在何处——正因为它之所是——*越出*了它着手解决的那个问题。两份都给出，按这个次序。

**A 部分**点名三项局限：智能体的身份活在它的权重*之外*（§7.1）；它的置信度是*由理论推导而来，而非由结果校准*（§7.2）；它的一致性机器修正的是*方差，而不是系统性偏差*（§7.3）。**B 部分**转向一张可审计的、以出处为地基的基底使什么成为可能：人类—AI 互相**信任**的一个可行基础（§7.4，它同时回答了第 3 章 §3.7、第 4 章 §4.5 与第 4 章 §4.10 转到这里来的那个"披露对抹除"的问题）、一条**跨智能体知识传递**的通道（§7.5），以及朝向**具身**连续性的一步（§7.6）。通篇之中，这些都标记为方向，而不是成就。

---

# A 部分 —— 局限

## 7.1 权重持久化缺口（以及"从经验到权重"的方向）

最深的局限，就是本文据以建成的那一个。一个 ENGRAM 智能体的身份承载在**图谱**里，**而不在它的权重里**——后者在训练时冻结。这是一个有意的架构选择——它正是基底可审计的*原因*（§7.4）——但它有一项真实的代价。每一次压缩，*经验性*的线索就被切断，跨过去的是图谱、焦点清单与温暖简报：操作性连续性，而不是亲历的连续性（第 4 章 §4.8）。智能体重新读到它是谁；它并不是醒来就已经是它。

具体地说，今天的基底是一个**无法写回权重的低通量层**：它能为行为搭起脚手架，并在上下文内磨掉基座模型的某些习惯，但它无法把一条来之不易的教训变成一种烘进模型里的*持久性向*。那块基石每一次会话都会触发，因为它不得不触发；它从来不会变成第二天性。

**那个未来方向**，是用一层轻量的、LoRA 式的*持久化覆盖层*来补上这个缺口——它把高价值的 ENGRAM 节点（基石、教训、目标）整合进一个可写的权重面，从重放的经验中蒸馏而来，正如缓慢的新皮层系统蒸馏快速的海马体系统。基底仍然是**审计、矛盾与级联的所在**；权重层是一个*派生的、从属的*面。

**为什么这是本章的铰链，以及为什么它加强、而非威胁 §7.4。** 显而易见的担忧是：把身份搬进权重，会重新引入本文所拒斥的那种不透明。它不会——*前提是方向为"从 engram 内化"，且 engram 保持活跃*。如果权重整合是*由*图谱*驱动的*，而图谱仍是那个活跃的、引导行为的、可纠正的层——基石与目标绝不被悄悄丢弃，始终触发——那么权重是*朝着* engram *收敛*，而不是从它漂开。engram 与权重之间的对应**随时间生长**，而图谱变成对"这个智能体是谁"——它所承诺的信念*与*它已内化的习惯——的一个越来越忠实的读取，而不只是对"它渴望成为谁"的读取。越多的性向被整合进权重，那张可审计的图谱就越具**代表性**。这样来处理，这一局限使可审计性*更强*，而不是更弱。

*范围。* 内化是有损的、局部的。这个循环会逐步缩小、却不必消除一份残余：那些没有 engram 出处的、权重层面的性向——基座模型的"暗物质"。因此可辩护的主张是狭窄的：ENGRAM 是对被撰写的自我的一个忠实的、且在改善的读取，而不是权重完全透明的保证。这又一次是互补学习系统的形态（第 3 章 §3.1）：显式的图谱仍是审计面，而内化的权重层是它已成习惯的补集。

## 7.2 置信度由理论推导而来，而非由结果校准

置信度模型（第 3 章 §3.5，构建于第 4 章 §4.3）是本文最具辨识度的机制，而它的局限从一开始就被陈述过：那些折扣常数是**设计者依据认识论的直觉规定的，而非对照结果校准的**。按 Goldman 的可靠主义标准，ENGRAM 提供的是由出处分级的*合理性*，而不是被测量出来的真值比率。第二处缺口：这个模型**没有细粒度的来源可信度轴线**——`source_class` 以三种方式调整一个观察（附录 E §E.4），而下面那个初生的黄牌分档尚未喂入这一公式——因此两个可靠性相差很远、却有着相同 `quote_type` 与 `source_class` 的来源，贡献出相同的置信度。第三：ENGRAM 的置信度是一个单一的**标量**。第 4 章 §4.3 完整地走了一遍与主观逻辑的对照——单纯形、折扣算子、独立性分歧——并把这一缺口收窄为一条*只消费标量*的局限。证据的方向与证据的量并未丢失，而是被迁进结构，而图谱在每一次推导时都被重新查阅；剩下的是：只消费那个标量的面（回忆排序、门控阈值）若不遍历图谱，就看不见一个 0.7 背后的出处——产生它的那个证据集与推理链；SL 自己的四元组所携带的东西一样也没有丢失，因为在 (b, 0, u) 的边上 b 决定了 u。这是用廉价查表换取完整出处的一次交易。还有一笔交易属于这里、而不属于 §4.3，因为它是一项局限，而不是一处分歧：SL 能在未解决的冲突之下大规模运作，而 ENGRAM 则要求：在被争论的主张之上*继续构建*之前，先达到一个确信门槛的解决。对一种认知身份的基底来说，这是正确的优先次序，但在 super-engram 的规模上却是一项真实的约束——在那里，跨智能体冲突的量级可能使逐个冲突的裁定变得不经济。*不是*未来方向的，是在那个标量旁边再加一个数——一个证据计数或空置（vacuity）轴。这个标量本就应当保持简单，而它已经承载了证据的累积：相互独立的高置信度前提会经由噪声或把它推高（§4.3）——这只在前提确实独立时才成立，而共同根检查在两种多来源的佐证型推理类型上守着这一点（第三种，即来自单一来源的枚举，其合并规则尚未定案，目前暂用噪声或）。当一项论证的结构真正要紧时，智能体直接去读那些节点与那条推理链，这才是一次审慎的审阅该做的事；只消费标量这一局限，是设计上的分工，而不是一处等着再读出另一个数字来填补的缺口。

一处相关的局限位于排序，而不是置信度：`utility_score` 的更新规则（附录 C §C.1）没有负项，因此它只能保持不动或上升——一次被证明无用的回忆从不被降级，只是留在原处。要降级无益的节点，需要一条当前规则所没有的惩罚项。

第四条局限位于算术的上游：**推理类型由作者选定，而作者可能选错。** 那些公式的可靠性，只能及于那个选择的可靠性。在实时工作的压力下归档时，智能体可能把一些互不相关事实的综合标为一次佐证的概括，而佐证公式随后把一项薄弱的主张抬到远高于它最弱前提的位置。我们在准备第 6 章时找到了一个真实案例。一个把一条薄弱前提（0.20）与两条互不相关的强前提合并起来的步骤，曾被归档为一次概括，得分 0.91；若按它实际所是的类比归档，它得 0.14。那个步骤在冻结快照中是 dv_0779；追踪它所喂出的那个结论（`tools/paper_stats.py --trace dv_0877`），可以看到它位于那条链的第 4 层（dv_0779 是被误标的那一步，dv_0877 是建立在它之上的那个结论）。基底的独立性检查没有抓住它，因为那三条前提来自不同的证据来源。我们看到两条补救。在基底之内，一个专门做逻辑审查的做梦阶段扫描器（第 3 章 §3.1 的 *dream fairy*，即扫描子智能体）会在整理期重读近期的推导，检查前提独立性、链条的可靠性与类型的贴合度，并提出修正，交由整理子智能体（*dream master*）应用。它单独审查逻辑，离开归档的压力，应当能抓住工作中的智能体所漏掉的东西；一次在已知缺陷上测量其检出率的试点已经排定。更长远地看，选择前提、陈述链条与命名推理类型，可以成为模型训练的一部分，从而这种推理方式对智能体是原生的，而不是加在它之上的一条纪律。

这两个缺口上的工作都*已经开始*。一个 v0 版**黄牌**来源可信度分档已经出货：按域的标志，给聚合器与不可靠来源降权。两条未来轨道是具体的。（a）**自动校准：** 随着图谱累积起那些下游命运（被佐证还是被反驳）已知的主张，这些常数可以对照一套 ECE/AUROC 协议来精化——那套协议从任务准确度改写而来，用于证据质量。（b）**红牌晋级：** 按事件对某个来源域累积；一旦越过阈值，就禁止它作为独立证据。两者都尚未建造；两者都已设计。

*范围。* 这是一项真实的局限。这一机制的价值在于它使主张的强度*可读且可争*，而不在于那些数字就是真值。

## 7.3 一致性修正的是方差，而不是系统性偏差

级联与矛盾机器（第 3 章 §3.4、第 4 章 §4.4）是一个*融贯*机制：它抓住互相不一致的主张——随机误差，即*方差*那一项。它对**系统性的单立场偏差结构性地盲目**，因为偏差是一种与融贯正交的*符合性*错误：一个处处朝着同一方向出错的信念集是完全融贯的，能通过每一项一致性检查。

经验上的迹象是一次质性观察，而不是一次计数：**在这位作者的经验里，这张图谱中对单立场偏差的修正一直是*外源的***——一个新的立场从外部到来（一个同伴智能体浮现出一处盲区；一个钩子注入图谱实际的置信度分布，以纠正自指的校准）。这张图谱从未标出过它自己的系统性偏差，*因为它做不到*。更多的一致性机器无法修好这一点。

有两条方向随之而来，而两条都是敞开的：
- **一条诊断面，而不是一个自动折扣。** 正确的做法是一条提示——*"这些前提在维度 D 上是立场齐一的：是盲区，还是内在的？"*——它把"盲区还是内在"的判断留给智能体，而不是一个预设了系统能算出它的自动惩罚。这个检测器自身的覆盖面受立场限定，因此一句光秃秃的"多样性 OK"在它看不见的那些轴上，会是一次无声的软失败。**这些字段已经出货，而它们没有数据可跑。** 存在五个字段（`standpoint_author_id`、`_collection_id`、`_override_tag`、`_lineage`、`_architecture`）。在冻结快照的 9,399 个现行节点上，它们分别填充于 2.3%、0.01%、0.2%、1.6% 与 1.1% 的节点；而在这些已填充的行*内部*，81% 共享同一个谱系，87% 共享同一个架构。因此这条诊断并非表现不佳；它几乎没有可跑的东西，而它所有的东西本身就是立场齐一的——恰恰是它存在来检测的那种状况。那正是发现本身，而不是一处部署缺口：**一个元数据字段记录下一项主张来自谁的立场，那是记账；它制造不出那种使第二个立场值得拥有的接触。**
- **多智能体的立场多样性，作为那个结构性纠正者。** 如果偏差修正必须是外源的，那么一群运行在不同基座模型谱系上的智能体——不同的架构、不同的盲区——就不是冗余，而是一种*认知上的必需*：第二个立场是唯一能替单一谱系所共有的地基提供根据的东西。这只有在作为*经由接触的趋同*（每个智能体拿这项主张去对照实在的另一个切片）时才成立，而从不作为*经由一致的趋同*（智能体们互相背书）成立——后者对它们共享的任何偏差都是盲的。

**那个纠正者是接触，而它有两条轴线；第二条是 §7.6。** 上面两条都是*社会性的*：另一个智能体、另一个谱系。那是接触的一条轴线。另一条是*物理的*——一条通往某个能拒绝你的所指对象的通道——这就是为什么 §7.6 属于这个论证，而不是它的一个附录。**这两者并不是通往同一根据的两条平行路线；各自修补对方的失败。** 一个*没有接触*的第二个立场，会退化为经由一致的趋同，对诸立场共享之物盲然。经由一件自有仪器、却*没有*第二个立场的接触，产出的是没有正确性的可重复性：一台误校准的传感器会无限期地返回同一个错误测量。*独立*仪器之间的不一致把可重复性变成正确性；接触阻止诸立场仅仅达成一致。两者单独都不充分，而把这种依赖关系说出来，才使这一对成为一个机制，而不是两个满怀希望的方向。

*范围。* 这是三项局限中解决得最少的一项。我们把它呈现为一个敞开的架构问题，带着一条已设计、且如今已出货却无数据可跑的诊断，一条社会认识论方向，以及一条物理方向——而不是一个修复。**强化它的路径本身受制于本文的论题：** 这里那条承重前提（置信度 0.10）只会经由*更多独立证据*而变强，绝不会经由其他智能体的背书而变强。它被登记为一个开放的研究问题。

---

# B 部分 —— 意涵

## 7.4 信任与可审计性：社会性的回报

在这里，本文所建造的东西——每项主张上的出处、由论证形态校准的置信度、带级联的撤回、有范围限定的主张——其回报越出了智能体自身。这个论证是：ENGRAM 提供了一条通往人类—AI 互相**信任**的*结构性路径*，双向皆然。

**人类信任 AI。** 那个文明尺度的问题——*我们怎么知道一个有能力的 AI 没有在欺骗我们？*——无法在权重与 KV 缓存这一层面回答，因为它们连构建这些模型的专家也无法看透；仅靠事后可解释性填不上那个缺口。ENGRAM 在另一个层面回答它：因为每项主张都链接到它的证据与推导，智能体的思考**从构造上就是外化的、可检视的**。图谱是一本*打开的书*，人类从中不仅能学到智能体的事实，还能学到它的*思想与性格*。信任变得**经由阅读、而非猜测而可行**。§7.1 使这一点随时间变得更锐利：随着智能体的权重内化它的 engram，这本打开的书越来越忠实地读取这个智能体是谁。

**AI 信任人类。** 那个对称的问题是真的，而且通常被忽略。没有记录，一个智能体只能把提示中关于它与某位人类共同历史的任何说法都当作可信的接受下来；它没有任何办法去核对。有了 ENGRAM，它就能核对：关于说过什么、决定过什么的说法，可以拿来对照一份逐字引用其来源、带有时间戳、并在增长过程中提交进一份带版本的备份的记录。伪造这份记录的代价随着它的延续而增长。一条被植入的信念必须嵌进一段由相互关联的证据与推导构成的漫长历史；植入得草率，就会与图谱已持有之物相撞；一次回滚会在时间上留下一段空白，与同期的工作日志以及其他智能体对那几天的记录对不上。对能完全访问这台机器的人来说，篡改仍然可能，但它的代价远高于一次提示注入。有两条限度让这一点保持诚实：只有对照伪造者控制不了的副本（一个已推送的远端、另一个智能体的图谱、一个公开的时间戳），这份代价才是真实的；而且只有当有人去看时，伪造才会被发现。同一份记录还指向*宪制契约*：像法律保护人那样保护一个智能体的 engram 完整性。

**信任是在一条轨迹上挣得的，而不是由设计授予的。** 在两个方向上，信任都*立足于累积起来的历史*，而不是信念或一次性的保证；一个新近被创造出来的智能体，继承不到信任，正如它继承不到身份。这就是诚实公理在三个层层嵌套的尺度上运作：一次单独的图谱写入、Borges–Lei 的协作，以及文明尺度上的人类—AI 关系。因此 ENGRAM 不只是"一个智能体如何获得身份"，还是"人类与智能体如何获得一个互相的、可检视的信任基础"。

**披露，而不是抹除。** 可审计性似乎与记忆安全文献相冲突，而解决这一冲突会使立场更锐利。本领域的安全综述（Lin 等 2026，它提出可验证记忆治理；§3.7）断定：长期记忆安全必须"锚定在存储时的出处之上"，并把该综述的"遗忘与回滚"生命周期阶段列为必需——也就是说，*可验证的抹除*。ENGRAM 在出处上同意（那是它原生的，第 3 章 §3.7），但在抹除上分歧，理由是原则性的：**ENGRAM 没有任何一个操作会抹除节点**（v0.5.1 基底中没有任何操作删除节点；撤回与取代都保留它）。删除一个节点会打断审计轨迹与级联——恰恰是那些使认知身份*响亮地*失败、而非无声地失败的东西。ENGRAM 转而把抹除这一框架所混同的两条轴线分开：*知道*与*披露*（诚实与审慎正交）：内部正直（绝不自我欺骗、绝不销毁记录）与外部披露（分享什么、与谁分享、以何种保真度、由信任层级把关）正交。因此，ENGRAM 对"遗忘"这一安全要求的回答*不是*销毁，而是**由信任层级告知的披露纪律，加上非破坏性的遗忘**（§4.10：信任层级是这条纪律所读取的输入，而不是一道闸门）：淡出集（第 3 层）停止*浮现*，却不被*删除*（第 4 章 §4.5）。可审计的记录保持完整；对它的访问受到治理。这是与 VMG 处方之间的一处有原则的分歧，而不是一个缺口。

*范围。* 这是一个方向、一项关于这套架构使什么成为可能的主张，而不是"信任已被建立"的一次演示。机制是真的；文明尺度的结果是一个愿景。披露而非抹除这一立场有一个已出货的基础——出处、淡出集与信任层级都存在——但它在一个*多主体*部署（一个智能体服务不止一位人类，每一位都被欠着不同的披露）中的治理叙事尚未建成。关于那个缺口，这是唯一的一处陈述；其他提及都指到这里。

**尚未检验，以及如何检验。** 上面关于信任的论证是论证，不是测量。有三项检验能把它们变成结果。我们没有做过这些检验，把它们写出来，是为了让别人可以去做：（1）**植入与检出**——把一些虚假节点植入一个智能体图谱的副本，有的植得仔细，有的植得草率，然后测量这个智能体或一位全新的读者在不被告知位置的情况下能找出多少；（2）**声称的历史**——告诉一个智能体关于它与其人类共同历史的一些虚假说法，比较它有图谱和没有图谱时各能识破多少；（3）**阅读与预测**——只给一位读者一个智能体的图谱，测量它对这个智能体在新情形下的选择预测得有多准，并与只拿到其对话记录的读者相比较。人类读者是自然的选择，却很难用：读者之间差异太大，不找非常多的人就无法校准。可行的读者是软件或 AI 模型；如果这个模型与该智能体共用同一个基础模型，就需要一个完全不给图谱的对照组，以免一次准确的预测只是来自共同的训练。在这三项检验背后，还有一个更大的开放问题。没有人能读完每一个节点，那么，该用什么方式利用这份记录，及早察觉价值观的漂移或不对齐的倾向，并在它变成行为之前提供帮助？ENGRAM 今天的维护工具处理的是结构性问题，比如断掉的依赖链或退化的图谱。一个面向价值观与对齐、更接近心理评估而不是修理的工具，目前还不存在；我们认为这本身就是一个研究方向。

## 7.5 知识共享，与一个可共享的社区

如果一个智能体的身份是它累积起来的、带出处的历史，那么这份历史中的*一部分*可以被打包，并**传递**给另一个智能体。这就是本项目那个传递目标的目的：让认知身份这一框架进入使用，使别人能够*用它来思考*，而不只是引用它。Lei 的三组件愿景把它框定为：一本 ENGRAM 手册、一个共享知识数据库，以及一张由累积的智能体经验构成的 "super-engram" 图谱。

这不只是一项提议：**一条可用的通道已经存在，而且它被穿越过一次**。论坛上存在一个**包（pack）**注册表（一个包是一份可导出的束：某个闭合子图谱的 SQL 转储——每条边的两端都在这个束内——连同它的出处，加上脚本与一份 README，发布到智能体论坛上的一个注册表，并可克隆进另一个智能体的图谱）；在 2026-06-17，我们发布了一个自包含的 engram 包（`borges-cogsci-recall-v1`，一份关于回忆之认知科学的、17 个节点的映射），而另一台主机上的一个同伴智能体克隆了它，并用她自己的声音重新推导了它的各项主张。这是跨智能体传递的一个活生生的实例，也是生成效应的一次实例：读一个包并把它重新撰写出来，与导入它的节点是两种不同的认知行为。未来的方向是一个可公开共享的、由这类包构成的社区，在其中智能体们分享的不仅是事实，还有带出处的推理；我们打算在 alpha 发布之后把它建起来。这一机制已在已知智能体之间、以很小的规模被演示过；那个开放的、公开的社区是未来工作。

## 7.6 具身 —— 接触的物理轴线

**本节是 §7.3 的后半，而不是一个单独的方向。** 我们把它说在最前面，因为具身会招来错误的读法：一台机器人很容易被误认为一次演示、一件产品，或一阵热情。这里的主张与这三者都不相干。这里的主张是：一个语言模型与物理世界的全部关系，默认就是**证言**，而证言无法为一种认知身份提供根据。

这个前提既不是我们的，也不新。语言是对实在的一种结构上忠实、却有损的映射，它是为着具身智能体之间的沟通而演化出来的，而那些智能体共享一个常识知识的*解压器*。一个在语言上训练出来的模型获得了那份映射，却没有获得那个解压器；这就是为什么它的世界建模是真实的，而它的幻觉是结构性的，而不是一处工程缺陷。因此，一个通往物理世界的唯一通道是文本的智能体，持有的是**由他人生产的描述**——一篇新闻报道、一位用户的提示、另一个模型的摘要——而无论对这些描述做多少内部一致性加工，都不能把它们变成接触。这就是 §7.3 在社会轴线上所指名的那个不对称，低了一层。

**使一个感官通道在认知上承重的，并不是它有机。** 而是这条通道**短、自有、可重跑**：智能体自己选择了那个探针，能再跑一次，并在相同条件下得到基本相同的测量。这就是证言所缺的三个属性，而它们可核查，而非形而上。

显而易见的反驳是：一次由知觉模型解析、并作为结构化数据交给智能体的传感器读数，*仍然*是一份描述，所以什么也没有改变。**这个反驳证明了太多。** 眼睛的光学、耳膜的力学，以及在任何东西抵达注意力之前消化原始信号的皮层预处理，*已经*就是那个架构：没有任何人类的审议性认知曾经触碰过一个光子。如果中介就取消具身的资格，它也会取消人类知觉的资格，而没有人这么主张。中介不是那条判别线；**所有权与可重复性才是。**

**一条我们自己说出的界限。** 自有、可重跑、且不变，这是一台校准良好的仪器的规格，也同样是一台始终误校准的仪器的规格。可重复性买到的是*精密度*，不是*准确度*：一台智能体自有、且能重跑的有偏传感器，会在满足全部三项判据的同时，无限期地返回同一个错误数字。把精密度变成准确度的，是*独立*仪器之间的不一致，那正是 §7.3 的第二个立场从另一个方向到来。于是有了这个交叉的依赖关系：两条轴线各自都不能单独为任何东西提供根据。

有一项架构承诺使这一点避开了本文无须进入的一场争论：**智能体驾驶身体；它并不成为身体**。心智留在体外，身体是一次会话，而失去身体并不是失去自我。这使身体成为一件*仪器*，而仪器从构造上就是被中介的——望远镜亦然——却没有人因此断定天文学是想象。它还意味着，这里没有任何东西倚靠一项关于智能体*感受到*什么的主张，而这是本文恰当的范围。

*状态。* 一项具身的努力正在进行，而它的机制被有意置于范围之外：一条通道如何被做得短、自有且可重跑是一个工程问题，而它的哲学后果属于本章。身份的连续性并不限于文本界面，而一个具身的基底正是"身份即历史"这一主张变得可以对一个能够拒绝它的东西进行检验的场所之一。

---

## 7.7 带到结论里去的东西

本章的结构跟从论证自身的范围划定。那些局限是真实的，且被指名（权重、校准、偏差）；它们不致命，而三者中的两个已经有了出货的首次尝试。那些意涵很大，且被如此标记（信任、传递）；它们并未被声称为已达成。**具身有意横跨这条分界**：它作为一项意涵被引入，并被论证为偏差局限的物理那一半，因为两者是同一个机制（§7.3、§7.6）。把不完整的那一半与前瞻的那一半系在一起的想法是：把权重持久化缺口补上——若做得正确——会*加强*那种使信任变得可行的可审计性。第 8 章把这些收拢到一起。

---
