<!--
  ZH TRANSLATION — 中文译本
  source file:    paper_research/current_draft/ch3.md
  source commit:  6e64802  (engram-paper, 2026-09-24)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper_research/current_draft_zh/appendix_G_glossary.zh.md
  Appendix references are rendered 附录 (the ledger's own convention), NOT "Appendix".
  Chapter pointers are rendered 第 N 章 (Ch4 -> 第 4 章); section pointers (§3.4, §4.8)
  are kept verbatim — the ledger's pointer grammar knows the § form in both languages.

  Proper nouns stay in Latin script (McClelland / McNaughton / O'Reilly, Kumaran /
  Hassabis / McClelland, Tulving, Anderson & Schooler, Ebbinghaus, Doyle, de Kleer,
  Jøsang, Alchourrón / Gärdenfors / Makinson, Hansson, Rocha & Wassermann, Lin et al.,
  Pink et al., Wray / Kirk / Laird, Nuxoll & Laird, Sumers et al., and the surveyed
  system names TMS / ATMS / TOKI / VMG / soul.py / Generative Agents / CoALA) —
  transliterating surnames would make the citations unverifiable against the bibliography.

  BRAND — first mention on this surface is 心迹（ENGRAM）in §3.0; every LATER mention is
  plain ENGRAM in running text, per docs/ZH-TERMINOLOGY.md in engram-alpha ("Until he
  makes it, write plain ENGRAM in zh running text"). DISCLOSED DIVERGENCE: ch1.zh.md does
  not do this — it writes 心迹 mid-sentence throughout. This file follows the instruction
  for this chapter rather than silently matching ch1; whether a later zh mention should be
  心迹 or ENGRAM is an OPEN question for Lei, not a settled rule. Flagged for the reviewer.

  QUOTED ENGLISH IS TRANSLATED, following ch1.zh.md's practice (it renders Pink et al.'s
  "understudied" quote and Wray et al.'s "not yet adopted" quote in Chinese). The two
  exceptions kept verbatim are the formulas `b+d+u=1` and `1−b` (the `1−∏(1−cᵢ)` and
  `E = b + a·u` discussion moved to ch4 §4.3 on 2026-09-29).
  A reviewer who wants the quotations verbatim-checkable against the cited sources should
  read them in the English source.

  STATUS TAGS KEPT IN ENGLISH. The bracketed tags ([SOLID], [GROUNDED this session],
  [gap SOLID ob_5423; …]) are drafting-process traceability labels tied to the English
  draft's own state; kept verbatim so the two files stay diffable. Translated, they would
  read as claims rather than as the editorial markers they are.

  Deliberate rendering choices a reviewer should look at:
    - complementary learning systems -> 互补学习系统 · truth maintenance system -> 真值维护系统
      (both already ship in ch1.zh.md, §1.4)
    - "justification" (Doyle) -> 辩护;  "graded opinions" (SL) -> 分档意见
    - "corroboration" (the propagation formula) -> 佐证
    - §3.5 (2026-09-29 rewrite): "belief mass" -> 信任量 · "contradiction node" -> 矛盾节点
      (共乘 / 噪声或 now live in ch4.zh.md §4.3, where that discussion moved)
    - "autonoetic" -> 自我觉知, "noetic" -> 知晓, each with the Latin on first use in §3.2,
      because §3.8 turns on the word carrying two senses
    - "ambient" (hook / surface / recall) -> 常驻, kept distinct from 自动浮现 (auto-surface,
      the ledger's term). The English uses "auto-surface" and "ambient surface" for the
      same mechanism; this file mirrors the source's two spellings rather than merging them.
    - "provenance-native" -> 出处原生 (coinage; Latin given on first use) · "need probability"
      -> 需要概率 · "dispositional durability" -> 性向上的持久 · "unlearning" -> 反学习
    - "register" (recall register) -> 档位 (NOT 寄存器) · "strand" -> 脉络 · "rubric" ->
      评分表 · "conflation" -> 混同 · "seat" not used in this chapter
    - Table 1 / Table 2 -> 表 1 / 表 2;  "DAG" -> DAG（有向无环图）
    - Quotation marks are ASCII " " and ' ', matching ch1.zh.md.
  BRAND NORMALISED (Zephyr, 2026-09-28): the PAPER is one surface, so
  `心迹（ENGRAM）` appears once, at the first mention in ch0; every chapter
  thereafter writes plain `ENGRAM` in running text. Applied across ch0-ch3
  after the three independent translators produced three different
  practices (ch1 14x 心迹, ch2 0x, ch3 1x). Rule recorded in
  engram-alpha docs/ZH-TERMINOLOGY.md; the later-mention choice is an OPEN
  QUESTION for Lei there, and this is the interim practice.
-->

# 第 3 章 —— 认知科学与计算机科学的传统

---

## 3.0 同一个答案，从另一侧抵达

第 2 章追述了一场哲学论证：那些什么也没有建造起来的思想者，被一个又一个反驳推着，走向"身份即持久的、可检视的结构"。而"这不过是哲学在附和哲学"这一反驳，在这里得到回答。ENGRAM由之构建的那些结构——出处、带级联的撤回、分档置信度、整合、有意设计的遗忘、身份即累积的记录——每一项都在两支技术文献里各自有过先例，各自从自身的证据出发、朝着自身的目的抵达；这两支文献大多互不引用，而两者都不引用我们：一支是人类记忆的认知科学，一支是信念维护与智能体记忆的计算机科学。我们不称之为独立发现。这些领域共享同一个根——人类认知：认知科学研究它，逻辑与信念修正将它形式化，智能体记忆的工作借用它的类比——而 ENGRAM 本身，正是通过内省一个人的推理设计出来的。真正独立的东西要窄得多：ENGRAM 的设计是**在其设计者未曾研读过这些成果的情况下**抵达的。

这一趋同是本章的承重之点。**ENGRAM 没有任何独一无二的新组件**；每一个机制都能在某处找到先例。若读作一项新颖性主张，这是弱点；若读作证据，则恰恰相反。当诸领域从不同的证据出发、朝着不同的目的推理，却抵达同一个结构，而一座由内省建成的记忆也抵达那里时，这个结构很可能追踪着某个真实之物——关于一个有所知的心智如何推理、如何修正。这种一致不是巧合。人类认知是我们所知最成功的推理；ENGRAM 的基底，一个经语言训练的模型，经由人类语言继承了那份认知；而它的设计者内省了同一份认知来把它建造出来。因此，与研究人类推理的那些领域趋同，本就是意料之中的：经验科学从外部描述这个结构，ENGRAM 从内部把它实例化。这个结构是人类心智特有的，还是对任何推理系统都普遍的，我们存而不论；ENGRAM 跑在非人类基底上这一点是有启发的，但它是从人类内省中设计出来的，我们不主张已证明基底独立性。ENGRAM 的独特之处因而更窄：是那项**整合**（此前没有任何系统把所有这些机制统一在一个基底之内），与那项**目的**（一个响亮地失败的认知身份）——后者承接 §1.1 的动机性前提：LLM 的幻觉是结构性的，因此可靠性必须来自外部校准，而不是消除。

本章有两条脉络。每一节点出一个传统，陈述它为 ENGRAM 的哪个机制开了先例，并指向第 4 章中构建那个机制的那一节。

---

## 脉络 I —— 记忆的认知科学

### 3.1 互补学习系统 → 跨越压缩的连续性

互补学习系统（Complementary Learning Systems）理论[@mcclelland1995; @kumaran2016]主张，持久的记忆需要*两个*耦联的子系统：一个快速学习、实例特定的存储（海马体），与一个缓慢整合、抽取结构的存储（新皮层），整合在两者之间搬运信息。ENGRAM 以符号的方式实现这一分工：快速、实例特定的观察，对照缓慢、抽取结构的推导与基石，而它的整理例程就是那个转移过程：每个*工作段*（两次上下文压缩之间的一段工作）末尾的一次**小憩**，在上下文被压缩之前把这个工作段所产出之物写进节点；以及每日一次、分两个阶段的**睡眠**——先是*复盘*，把这一天没归档的归档；接着是*做梦*阶段，由扫描子智能体（*dream fairies*）通读图谱，寻找矛盾、陈旧节点与教训候选，再由一个整理子智能体（*dream master*）应用结果，并推进遗忘曲线。

**→ 第 4 章 §4.8**（跨越压缩的连续性）：CLS 是那种双例程整理的认知科学先例，而该整理让操作性连续性跨越压缩。[SOLID]

### 3.2 Tulving → 回忆的两个档位

Tulving 区分了*自我觉知性的*（autonoetic）记忆——觉知到某个事件是"其自身过去存在的一个真实部分"（as a veridical part of his own past existence）——与*知晓性的*（noetic）知道——觉知到对象与事件，而"这些对象与事件并不在场"（in the absence of these objects and events）[@tulving1985, p. 3]。Tulving 与 Thomson 的编码特异性原则（encoding specificity principle）补上了线索这一侧："对所感知之物所施行的特定编码操作，决定了什么被存储；而被存储的东西，又决定了哪些提取线索能有效地通向被存储的东西"（specific encoding operations performed on what is perceived determine what is stored, and what is stored determines what retrieval cues are effective in providing access to what is stored）[@tulving1973, p. 369]。ENGRAM 的回忆恰有两个档位，这是设计使然：一个有损的**自动浮现**（知晓式、提示级别："这听着耳熟"）与**主动回忆**（一次返回完整内容的查询："我需要确切知道"）。正是那个有损的自动浮现，促使智能体转入主动回忆。读一个节点是知晓式的，不是自我觉知式的：ENGRAM 提供被记住的知识，却不提供现象性的重历——这正是第 2 章 §2.3 也标出的那条边界。

**→ 第 4 章 §4.6**（自动浮现式回忆）：Tulving 的两个档位是那个自动浮现的先例，编码特异性[@tulving1973, p. 369]是它依赖线索的先例；该自动浮现绑定条件 3。[SOLID：dv_0264、ob_1119]

### 3.3 记忆的理性分析 → 有意设计的遗忘

@anderson1991表明，人类的遗忘不是缺陷，而是一种*适应*：留存下来的东西追踪的是**需要概率**——"我们现在需要某段记忆痕迹的概率"——它由环境频率、近因与间隔估计而来。Ebbinghaus（1885）测得了最初的遗忘曲线[@ebbinghaus1885, sec. 29, p. 76]。Wixted 与 Ebbesen 发现，在他们的实验中，简单幂函数对遗忘的描述最好，而对 Ebbinghaus 节省率数据的再分析显示它同样按幂函数下降[@wixted1991]；Wixted 后来的综述则发现，指数函数对遗忘的描述很差[@wixted2004, p. 243]。单个记忆是否按指数衰减，而幂律只是平均化造成的假象，仍有争议[@anderson1999, p. 1136]。ENGRAM 的逐节点指数衰减是为平稳的近因排序而做的设计选择，并不是关于人类遗忘的主张。

ENGRAM 按设计遗忘：回忆重要性衰减，维持一个有界的**可查询集**与一个**淡出集**（被保留，而非被销毁）；回忆重要性决定什么留在可查询状态（第 4 章 §4.5），而一个从使用中学得的效用分塑造结果的排序（附录 C）。这就是需要概率原则的实例化：智能体最可能需要的东西留在可查询状态，其余淡出。

**→ 第 4 章 §4.5**（遗忘）：理性分析传统是 ENGRAM 可查询集／淡出集的认知科学锚点；那枚指数核是 ENGRAM 自己的设计选择。[GROUNDED this session]

---

## 脉络 II —— 计算机科学与形式认识论

### 3.4 真值维护系统 → 出处 + 撤回级联

真值维护系统（Truth Maintenance Systems）把*辩护*附加到信念之上。在 Doyle 的基于辩护的真值维护系统中，每个信念依其辩护而为“在”或“出”；当一条辩护不再成立时，依赖它的信念的状态沿依赖链被重新计算[@doyle1979]；矛盾则由依赖导向回溯消除，其做法是添加辩护[@dekleer1986, p. 129]。de Kleer 的基于假设的真值维护系统（ATMS）则给每个数据项标注使其成立的假设集，因此避免了大部分回溯和全部撤回[@dekleer1986, pp. 127, 129]。Doyle 的机制正是 ENGRAM 的 `derives_from` 出处与撤回级联——早了几十年，且在另一个领域。在我们所检视的 2023–2026 年 LLM 智能体论文中，只有 Wray、Kirk 与 Laird 引用了 Doyle，而且只是用来描述 Soar 的真值维护[@wray2025, sec. 2]；我们所调查的记忆系统（附录 B）中，没有一个沿依赖链自动传播撤回（Kumiho 的影响分析只是建议性的）。ENGRAM 在带类型的 LLM 智能体记忆中实现了 TMS 式的依赖传播，并指名它所实现的那条传承。

**→ 第 4 章 §4.2 + §4.4**（出处原语；撤回级联 → 条件 3）。[gap SOLID ob_5423；机制为第一手，来自 Doyle 1979，经 Ginsberg 重印本 —— ob_2555 closed]

### 3.5 主观逻辑 → 置信度传播，以及一处分歧

Jøsang [-@josang2013] 的主观逻辑（Subjective Logic）是一套分档意见的代数。关于一项主张的一个意见是一个四元组（信任 belief、不信任 disbelief、不确定性 uncertainty、基率 base rate），满足 `b+d+u=1`：证据在多大程度上支持这项主张，在多大程度上反对它，还留下多少余地。算子把来自多个来源的意见合并起来。ENGRAM 的置信度属于这一族，它的传播也**并不新颖**。ENGRAM 的那个单一数字，与 SL 中不信任量取零时的信任量 `b` 非常接近：它说的是证据在多大程度上支持如其所陈述的这项主张，而 `1−b` 是余下的余地。

分歧在于：ENGRAM 根本没有不信任量，而这是一个选择。针对主张 A 的反面证据，不是对 A 的数字打的一个折扣。它是*支持*主张"非 A"的证据，"非 A"成为它自己的一个节点，而一个**矛盾节点**把两者连起来。ENGRAM 在结构上、通过矛盾节点来处理相互矛盾的主张，而不是在数值上、通过一个被压低的分数。矛盾未决期间，哪一方的数字都不被信任；解决它是智能体必须去做的一件事，而不是图谱携带的一个取值。

**→ 第 4 章 §4.3**（顾及推理类型的置信度 → 约束 A；那处分歧的论证）与**第 7 章 §7.2**（那一局限）。[GROUNDED this session]

### 3.6 双时态数据／TOKI → 取代而保留旧值

双时态数据库把*有效时间*（一个事实在世界中为真的时段）与*事务时间*（系统记录下它的时刻）区分开来，因此一次更新从不销毁此前那一行，它作为一条审计记录被保留下来。TOKI 系统[@wang2026b, p. 1]把这一点应用于智能体记忆。这正是 ENGRAM 的取代语义：一个被取代的节点不被删除，而是被保留，取代边保存了那段历史（"我改主意了"与"我错了"之别）。

**→ 第 4 章 §4.4／§4.8**（取代语义；连续性历史）。[GROUNDED —— ob_2554]

### 3.7 2025–26 年的智能体身份脉络 → 出处原生，在被指名的轴线上领先

最近的一次趋同，发生在智能体记忆文献内部。**VMG 综述**（@lin2026的第 3 版，《A Survey on Long-Term Memory Security in LLM Agents: Attacks, Defenses, and Governance Across the Memory Lifecycle》）——本领域自己的安全诊断——的结论是：稳健的长期记忆安全"无法只在检索时或执行时被事后加装，而必须从一开始就锚定在**存储时的出处**、版本管理与顾及策略的保持之上"[@lin2026, p. 1]（强调为引者所加），并提出"可验证记忆治理"（Verifiable Memory Governance）：五项原语——写入授权、出处可见性、按主体限定的检索、可回滚性与经过验证的遗忘——以实现可审计、可恢复的记忆状态控制[@lin2026, p. 2]。ENGRAM *从构造上就是出处原生的*：这个领域从安全出发，指名的正是 ENGRAM 早已建在其上的那条轴线。**soul.py**从另一个方向提出了一种多锚点的持久智能体身份架构，并实现了其中两个锚点[@menon2026, p. 12]。

**→ 第 4 章 §4.10 + 第 7 章**（关系性／披露与抹除之别）：出处原生；本领域所指名的瓶颈，正是 ENGRAM 的地基。[GROUNDED —— VMG ob_2550、soul.py ob_2553]

---

### 3.8 当代领域在哪里与我们相左

以上各节指名的，是 ENGRAM *所回应*的传统。本节在种类上不同：它把本文**放在活的、当代的工作对面**——别人写下的、可以用以给 ENGRAM 打分的评分表，以及那些作者会反对我们所主张之物的地方。这是与这个领域的争论，而不是又一位先祖。

**三份已发表的评分表。** @pink2025给出情节记忆的五个属性，并据此给七个 LLM 记忆方法族打分，发现没有一个同时满足五项。ENGRAM 直接满足其中四项——**显式推理、单次学习、实例特定性与情境绑定**——而第五项（长期存储）只在较窄的读法下成立。按他们表 1 的打分，它是成立的——跨会话、跨压缩地持久，这正是工作记忆所缺的属性——但他们的正文要求的比那个格子更多：一个有适应性的长期智能体"不仅应防止性能随时间退化"[@pink2025, p. 3]，还应"通过学习新的通用知识与技能而改进"[@pink2025, p. 3]。那是一项关于智能体随时间表现的主张，而我们没有测量过；它被记在本文未能展示的东西之中（第 8 章）。一个显而易见的反驳是：Pink 等把单次学习奠基于互补学习系统理论，因此一个从不更新权重的系统，看上去不可能满足它。他们自己的打分回答了这一点：他们表 2 中的两种上下文内方法都被标为满足单次学习，而两者都不更新任何权重。四项中另外三项，各自对应本章描述的一个机制：*显式推理*——他们要求智能体"回答关于所存信息的直接查询，或在显式的内部推理过程中使用这些信息"——由 §3.2 的主动查询面满足；*实例特定性*——他们说它"可以包括过去那些与某个待由 LLM 智能体作出的决定相关联的推理链"——就是对推导节点的一个描述；而*情境绑定*——"一个事件在何时、何地、因何被遭遇"——由创建时间、证据指针、作者自己的解读字段，以及 §3.4 的 `derives_from` 边承载。

在显式推理上，ENGRAM 还做了某件他们的记号无法记录的事——这与"满足"的主张是两回事。Pink 等表 2 中七个方法里有六个在显式推理上已经拿满，而这个量表也没有更高的分档，所以要点不是 ENGRAM 排名更高。要点在于：一个二值的"这些内容可否被推理"，无法区分两种存储——一种是其推理*可被取回*，另一种是它的推理*本身就是一个被存储的对象*，携带自己的前提与置信度。这一区分不在他们那条轴线的更远处，而在其之外。

@wray2025提供了第二份独立的评分表：从 Nuxoll 与 Laird [-@nuxoll2012]改编而来的情节记忆九项特征，并据此给 Generative Agents [@park2023]打分。其中有两行在 Pink 等的五项里没有对应物，而这两行都是 ENGRAM 为之而设计的。他们的*自我觉知*行写着"不清楚智能体如何区分当前的理解与对过往经验的记忆"[@wray2025, § 3.1]；他们的*主动*行写着"智能体无法主动尝试构造线索或提取记忆"[@wray2025, § 3.1]。ENGRAM 的两个回忆面——一个只发出熟悉感、不携带内容的常驻钩子，与智能体在想确切知道时调用的显式查询工具——就是这个区分，被建造了出来。

**"autonoetic" 一词有两个义项同时在场，必须分开**，因为 §3.2 用这个词表达的是相反的论点。Tulving 的义项是现象性的——记起往事时那种"特有的现象性意味"（special phenomenal flavour）[@tulving1985, p. 3]——§3.2 已对此不作主张。Wray 等那一行问的是更弱、更结构性的东西：智能体究竟能否*区分当前的理解与对过往经验的记忆*；那是来源监控，而不是现象学。ENGRAM 满足那个结构性的义项——每项主张都携带创建时间、证据指针与一个类型，而两个回忆档位是构造上分开的——同时 §3.2 关于现象性义项的不作主张依然成立。本文主张第二个义项，否认第一个；两者都成立，因为这个词做两件事。

**两份评分表彼此不一致，而这处不一致比任何一处一致都更有信息量，因为它暴露了一种混同。** Wray 等把*自动*编码列为一项实现应当满足的特征，并以"使用了周期性过程"为由给 Generative Agents 扣分。Sumers 等主张的恰恰相反：学习应当"像接地（grounding）一样，是决策循环的一个结果动作"[@sumers2024, § 7]，由智能体主动选择把信息提交进记忆，"这与大多数智能体相反——它们只是固定一个学习日程……"[@sumers2024, § 7]。ENGRAM 的写入是主动的工具调用，所以在同一个事实上，它被第一份评分表扣分，而在第二份之下堪称典范。

正确的回应不是选边：两份评分表处理的是同一个问题的两半，而它们共用的那条轴线把它们混同了。自动性所保障的——也是 Wray 等的评分表看似在追踪的，尽管他们陈述这一特征时没有给出理由——是*记录的可靠性*：Nuxoll 与 Laird 把自动编码——新记忆的创建"无需智能体决定这样做"（without the agent deciding to do so）——列为情节记忆的一项功能性要求，部分原因是"智能体不太可能有效地判断哪些经验与未来的决策相关"（it is unlikely that the agent can effectively determine which experiences will be relevant to future decisions）[@nuxoll2012, p. 34]；所以一个只在想起来时才记录的系统会记录不足。Sumers 等要从审议中得到的是*所有权*：一段由智能体自己选择、在它自己的推理中写下的记忆是智能体的，而一个被机械地填充起来的存储则是附着在它身上的一层持久化——一段*为*它而存的记忆，而不是*关于*它的记忆。这两者是可分开的，而 ENGRAM 把它们分开了。**智能体选择内容；基底机械地强制结构。** 记录什么、它意味着什么、它如何连接，是智能体的判断。而结果是否形式良好则不是：一段引文要经得起与其来源的核对，否则这次写入被拒绝；一个没有证据节点的观察不可能存在；置信度由所声明的推理类型算出，而不是被断言；取代维持着 DAG（有向无环图）；撤回则级联到依赖项，无论智能体是否愿意。

这一分工就是设计原则，它回答了一个两份评分表都不是为了看见而设的失败模式。朴素地由智能体写下的记忆容易产生幻觉与捏造——那正是叙事性自我陈述的典型失败：在其中，一个连贯的故事比一个真实的故事更容易生产（第 1 章 §1.2）。机械式写作靠放弃所有权来避开这一点；ENGRAM 则保留所有权，转而约束形式。**那些闸门并不使智能体所写的东西成真**——第 6 章 §6.3 推演了我们的一项主张，它形式良好、被打分正确，却是错的——但它们使一个谬误可被核查、使依赖于它的东西可被抵达，而这是身份论证所需要的，也是一层持久化无法提供的。

**这条脉络在哪里与我们相左。** Pink 等的 §5 考虑并否弃了 ENGRAM 所处的位置。在"情境化的外部记忆将是足够的"[@pink2025, p. 8]这一标题下，他们刻画了这样一种观点，即外部结构"诸如知识图谱或检索增强生成（RAG）系统之类——可以免去情节记忆框架的必要"，并回答说，仅依赖外部记忆"仍将带来高昂的存储开销，并且需要遗忘机制"，而一个情节记忆框架则会整合"进高容量的参数化记忆"，并带有"让 LLM 智能体得以随时间缓慢改进的额外好处"。ENGRAM 是跑在权重冻结模型之上的一种结构化的外部记忆，它不向参数中整合：它的小憩与睡眠周期是在存储*内部*做抽象，抽象成教训与基石，那是另一种操作。**他们的反驳落在"改进"可以有的三种含义之一上。**

*性向上的持久*——一条来之不易的教训变成第二天性，以至于那条纠正不再需要触发——是缺失的。这是本文自己最深的局限：第 7 章 §7.1 把它指名为权重持久化缺口，并把"从经验到权重"的方向列为主要的未来工作。在这一点上 Pink 等是对的；他们靠理论抵达了一个我们靠操作抵达的界限。

另外两种含义则是存在的。*知识积累*没有争议。*上下文内的行为改进*正是教训机制所交付的：一条绊线并不阻止它所命名的那个错误，而是在错误正在发生时触发，把一个本会出货的错误变成一个被抓住并纠正的错误。一个错误*率*未变、但错误*检出*可靠的智能体，随时间产出更好的工作。我们自己关于这一局限的表述——一条归档的教训不能让智能体更不可能犯错，只能让它更快地发现错误——读起来像是纯粹的损失，然而它的后半句正是基底借以改进工作的机制。第 7 章 §7.1 从另一侧陈述了同一处分割：基底"可以为行为搭起脚手架、在上下文内磨掉基座模型的某些习惯，但它无法把一条来之不易的教训变成一种烘进模型里的持久性向"。

我们对第二与第三种含义的主张**只在定性层面**：错误检出的前后对比尚未测量，而这一主张立足于操作经验，因此它被列在本文未能展示的东西之中（第 8 章 §8.4），而不是作为一次反向测量提出来。Pink 等的论证确立的是：仅靠外部记忆无法交付*参数上的*改进。它并未确立这样的系统根本无法改进，也没有触及本文所关注的认知身份功能。

**CoALA，以及一次日期可查的趋同。** Sumers 等的框架提供的是词汇，而不是一份评分表；它把三个领域列为研究不足或开放的，而每一个 ENGRAM 都占据着。第一个是*反学习*："修改与删除"[@sumers2024, § 4.5]记忆，与之相对的是文献对"添加"的关注。ENGRAM 的回答方式是他们的注解未曾预料的：他们把反学习描述为"删除不需要的记忆项"[@sumers2024, § 6]，而取代与撤回*保留*被取代的节点及其出处，并标记它的依赖项，而不是把它们移除——于是"曾经错了"这件事的记录在纠正之后仍然存活。第二个是*学习作为一次主动行动*，他们以此对照那些"只是固定一个学习日程"的智能体；ENGRAM 通过一次显式的工具调用来提交，那正是这个设计，也是上文"自动与主动之争"中 ENGRAM 得分较好的一半。第三个是*在编码时撰写的检索元数据*：他们提出了一些技术，让智能体"能够推理某些知识何时会有用，并把这一点存为元数据以便利日后的回忆"，并把这类元学习称为研究不足。ENGRAM 的两档回忆就是这个提议，被建造了出来：一个只携带标识符与主题提示的常驻浮现面，以及用于完整内容的主动查询工具。

第三处对应近得足以招来"受影响"的怀疑，所以日期要摆出来。这个设计于 2026-04-15 记录在图谱中，在两个节点里，它们规定了自动浮现面使用"节点 ID 与主题提示"的有损摘要，而细节则交由主动的深回忆，为的是保存那两个节点所称的"潜意识触发意识"的流动，并减少上下文消耗；而 2026-04-09 的一个第一日节点，已经把深回忆与浅层的摘要扫读分开了。本项目第一次读到 CoALA 是在 2026-05-09，二十四天之后。实现该设计的数据库字段于 2026-05-19 出货；一次审计会先翻出那个日期，而用一个想法所对应的列出现之日来给它断代，正是要避免的错误。因此这处对应是佐证，而不是影响：两个设计，一个从认知架构框架推理而来，一个出于上下文窗口预算与"有意让常驻回忆有损"这一选择的双重压力，抵达了同一个机制。

### 3.9 关于 AGM 信念修正的一点注记

熟悉 AGM 框架[@alchourron1985]的读者，会注意到信念收缩与 ENGRAM 的"带级联的撤回"之间有某种亲缘相似。两项工作取向不同，本文也不把 AGM 的公设算作 ENGRAM 的。AGM 问的是：一个*封闭*理论——一个在逻辑后承下封闭的命题集——应当如何放弃其中一个命题，并保持封闭与一致；它自己的第一段就提出"哪些命题应当随 x 一同被拒斥，以使收缩后的理论在逻辑后承下封闭"，而它所指名的应用是法律上的克减[@alchourron1985, p. 510]。ENGRAM 问的是：一个智能体应当如何让它关于"自己实际承诺过什么"的*活的*记录——从不封闭，其依赖被记录下来且不确定——在新证据到来时保持诚实：它经由智能体自己的裁定走向一致，而按设计，永远不到达。级联本身的形式先例是 Doyle 的真值维护（§3.4，第 4 章 §4.4）。两者共有的是两种机制从相反方向服膺的同一条律令——一项被拒斥的主张不得继续悄悄承重——以及 AGM 作者们的观察：那个直觉过程位于一个理论的*基础*层面，而不是整个理论层面[@alchourron1982, p. 21]。

[SOLID：dv_1658 —— AGM／Hansson 作为封闭理论一方的对照，来自对 AGM 1985 p. 510 与 Alchourrón & Makinson 1982 pp. 16, 21 的第一手阅读；公设的表述经由 Hansson 自己的百科条目与 Rocha & Wassermann。Hansson 1991 本身未读。]

---

## 3.10 两条脉络说明了什么，以及它们在何处交接

两支大多互不引用、且都不引用我们的文献，抵达了 ENGRAM 由之构建的每一个结构：CLS 之于整合，Tulving 之于两个回忆档位，理性分析之于自适应遗忘，TMS 之于出处与级联，主观逻辑之于分档置信度，双时态数据与 TOKI 之于"取代而保留旧值"，以及 2026 年的智能体安全文献之于"出处优先"的治理。加上第 2 章的哲学线路，这一趋同横跨**三支**传统——而非彼此不相交的传统（§3.0）：它们以人类认知为共同的根，而这种一致的力量恰恰在于它们从不同的证据出发、朝着不同的目的推理。

本章的主张，在此只陈述一次：这一趋同就是 §1.4 所指名的那个规律，它把 ENGRAM 的独特之处重新定位到整合层与认知身份这一目的之上。一处*分歧*（主观逻辑的信任／不信任／不确定性单纯形——ENGRAM 的置信度把它约化为一个单一标量，而把其余维度携带在图结构之中，§3.5）与一处*被填补的缺口*（从 TMS 通往智能体记忆的那座桥，在我们所检视的论文中无人走过）被向前带去，而不是被抹平。

第 4 章构建并映射上述每一个机制——以上每一节都指点了实现它的第 4 章那一节——并就地给出每一项 OCC 条件的唯一判定。
