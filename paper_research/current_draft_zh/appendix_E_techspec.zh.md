<!--
  ZH TRANSLATION — 中文译本
  source file:    paper_research/current_draft/appendix_E_techspec.md
  source commit:  df3b284  (engram-paper, 2026-09-25)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper_research/current_draft_zh/appendix_G_glossary.zh.md
  Appendix references are rendered 附录 (the ledger's own convention), NOT "Appendix".
  Section pointers (§E.2, §4.4, §7.2) are kept verbatim — the ledger's pointer grammar
  knows the § form in both languages. Chapter pointers are rendered 第 N 章 (Ch4 §4.3
  becomes 第 4 章 §4.3), matching ch4.zh.md and appendix_D.zh.md.

  NODE IDs — this file IS GATED. `appendix_E_techspec.md` is in render_paper.py's
  STRIP_PROVENANCE_IDS_IN, so `strip_provenance_ids` runs on it and
  `assert_no_leaked_ids` hard-fails the zh build on any surviving ID. The
  English source carries FOUR ID sites and the en render removes EVERY one of them (since
  #114 the `df_*` sites are stripped too; before it the render removed only the one `dv_`
  site), so the zh carries none and mirrors the en render site by site:
    * §E.1 `(df_NNNN)` — DROPPED (2026-09-29, #114: `df_*` is citation-style like the
      rest and is no longer exempted from the render strip).
    * §E.5 the primitives bullet, `(dv_NNNN)` — DROPPED with its parenthetical. This is
      the ONE citation-style ID the engine added Appendix E to the strip set for (its
      fold comment above STRIP_PROVENANCE_IDS_IN names this exact site); the en render
      prints "The eight load-bearing **primitives**: …". A zh copy cannot be reached by
      the English-only literal table, so dropping it here is the translator's half of
      the same operation. Nothing a reader loses: the en reader cannot follow it either.
    * §E.7, `nap` and `sleep` — `df_NNNN` twice, DROPPED (same reasoning as §E.1).
  (IDs in this header are written WITHOUT their four digits ON PURPOSE: this comment is
  part of the file the stripper reads, so a literal ID in the note would itself leak.)

  NO APPARATUS TAGS. The English source's only square brackets are the three numeric
  intervals `[0.10, 0.60]` (measured: a grep for `[` returns three lines, all of them an
  interval). None opens with a word `_APPARATUS_OPENERS` recognises, so
  `strip_apparatus_tags` is a no-op on this file in both languages and nothing can leave
  a stray English bracket in the zh body.

  BRAND — the paper is ONE surface, so `心迹（ENGRAM）` appears once, in ch0; this
  appendix writes plain `ENGRAM` in running text throughout, per the ledger header and
  engram-alpha docs/ZH-TERMINOLOGY.md.

  VERBATIM ENGLISH IS KEPT ENGLISH — the load-bearing call this appendix had to make.
  §E.6 quotes Kahl's three OCC conditions verbatim, and ch2.zh.md §2.5 tells the Chinese
  reader explicitly that the 逐字原文 lives HERE ("逐字原文见附录 E §E.6"). A translated
  quote would break that pointer and stop being the thing it is cited as. So every source
  quotation is reproduced BYTE-IDENTICAL to the English source, including its line
  wrapping, and the Chinese reading is carried OUTSIDE it, in a following paragraph
  （中文解说：…）. ASCII `"` marks a verbatim-English span; Chinese prose quotes also use
  ASCII `" "`, matching ch4.zh.md's declared convention (appendix_D.zh.md uses curly “ ”
  for the same purpose — a divergence, disclosed rather than silently harmonised).
    THE LINE DRAWN — source quotations stay English; this appendix's OWN analysis does
    not. The OCC condition NAMES in the §E.6 headings are the paper's own labels for
    Kahl's conditions, so they are translated 条件 1／2／3 with Kahl's English name carried
    in parentheses — this appendix is the standalone reference for the mapping, and the
    English name is the anchor a reader matches against Kahl's own paper. The Chinese
    condition names are taken from ch2.zh.md §2.5 (历时性约束 · 重置下的不可互换性 ·
    自我维持的仲裁) so the two surfaces cannot drift; §E.6's 中文解说 for condition 3 is
    byte-identical to appendix_B.zh.md's, which quotes the same sentence.

  TERMS THAT ARE GLOSSARY COUNTERPARTS — four ledger entries are DEFINED in this appendix,
  so the two files must not drift:
    axiom -> 公理 · cornerstone -> 基石 · lesson -> 教训 · goal -> 目标  (§E.2 table)
    claim-bearing / non-claim-bearing -> 承载主张／不承载主张 (§E.2) · pending marker ->
    待决标记 (§E.5) · focus list -> 焦点清单 (§E.7) · evidence node -> 证据节点 ·
    trust tier -> 信任层级 · provenance -> 出处 · derivation -> 推导 · observation -> 观察
  Other renderings fixed here or inherited from the ledger / ch4.zh.md: corroboration ->
  佐证 · weakest-link -> 最弱环节 · capped weakest-link -> 带封顶的最弱环节 (ch4.zh.md §4.3) ·
  reasoning type -> 推理类型 · discount -> 折扣 · premise -> 前提 · tripwire -> 绊线 ·
  disposition -> 性情 · mint / retire -> 铸造／退役 · consolidation (routine sense) -> 整理
  (ch4.zh.md §4.8's 整理节律; the ledger's 小憩／睡眠 entries both say 整理例程) ·
  compaction bridge -> 压缩桥接 · closest continuer -> 最接近的延续者 · history-tree ->
  历史树 · retrieval profile -> 检索画像 · type/token -> 类型／个例（type/token） · sidecar ->
  边车 · write path -> 写入路径。

  NUMERIC PARITY — measured, not assumed. A multiset comparison of digit tokens between
  this file and its English source returns differences in ONE direction only, and every
  one of them is a NODE-ID FRAGMENT: the four digits of each of the four IDs (three
  `df_`, one `dv_`) this file was required to drop — four digit tokens in all, measured
  on the bodies with this header excluded. The zh side introduces NO extra digit
  token — every digit in the English is carried as a digit here (0.95 · 0.85 · 0.70 ·
  0.65 · 0.50 · 0.40 · 0.35 · 0.60 · 0.80 · 0.90 · 0.98 · 1.0 · 164 · 23 · 10,361 · 131 ·
  75 · 11 · 28 · 17 · 1.26% · 3% · 450 · 2026b · every §/Ch pointer). English spells
  "six types", "three consequences", "six independent flags", "five or six a week",
  "three words", "fourteen types" as WORDS and so does Chinese (六种 / 三条后果 /
  六个标志 / 每周五到六个 / 三个词 / 十四种), so no digit crossed into or out of a word in
  either direction. Any drift-detector built on `[0-9]` runs must whitelist the
  ID-fragment class, or it will report four false errors per run.

  DELIBERATE RENDERING CHOICES a reviewer should look at:
  1. "an Epistemic Node Graph" -> 认知节点图谱, matching the README.zh.md title fix
     (认识论节点图谱 -> 认知节点图谱, engram-alpha #3203). 认知 is the ADJECTIVE form per
     the ledger's operative test; 认识论 is reserved for the noun.
  2. "named in the acronym" -> 写在这个名称之中. The English says the three mechanisms are
     named "in the acronym", but ENGRAM's letters spell none of them — they appear in the
     expansion. The zh does not reproduce the error and does not correct it either; see
     the note in the report.
  3. Condition headings carry Kahl's English name in parentheses (§E.6). See the verbatim
     note above.
  4. "unified / resolved / preserves S's continued status" (§E.6) -> 统一／解决／保全 S 的
     持续身份, the same words the ledger's 统一 entry and appendix_B.zh.md use.
  5. "reinforcing / limiting / ceilinged" (the three propagation modes) -> 强化型／限制型／
     有天花板的. A coinage; if it reads wrong, it reads wrong in all three §E.4 rows at once.
  6. "narrow set / wider set" (§E.2's identity-scarcity measurement) -> 窄集／更宽的集合,
     with "the two sets are not nested" -> 两个集合并非嵌套关系. The distinction is
     load-bearing (it is why the two percentages differ), so the two words are kept
     visibly paired.
  7. "warm-briefing letter" -> 温暖简报那封信 (the ledger's 温暖简报 entry), not a
     hyphenated Latin compound.

  ENGLISH AMBIGUITIES FOUND, NOT FIXED (reported rather than silently resolved):
    * §E.4's `d`-discount list names 0.80 for `abductive_best_explanation`, and the row
      above it gives that same type a CAP of 0.80. Reproduced as written.
    * §E.5 says "Two facts the other appendices lean on" and then lists one fact about the
      cascade plus one about `contradicts` — reproduced as written.
-->

# 附录 E —— ENGRAM：一份简明的规格说明

---

## E.1 名称

**ENGRAM——一个用于撤回、仲裁与记忆的认知节点图谱**。三个起区分作用的机制都写在这个名称之中：*撤回*（Retraction，沿推导边级联的错误修正）、*仲裁*（Arbitration，那次级联在一个统一的审议架构之内的结构性传播），以及*记忆*（Memory，带类型的主张、证据与推导所依托的那个基底）。

## E.2 节点类型

节点从来不是自由文本，而是一个*种类*；种类决定基底如何对待它。第一刀切的不是题材之别，而是**断言了可真假评判之物的节点与未断言的节点**之别——即承载主张／不承载主张这条划分；比起任何别的分类，它支配着基底更多的行为。

**承载主张（CB）**——六种：`observation_factual`、`observation_predictive`、`derivation`、`theory`、`axiom`、`conjecture`。**不承载主张（NCB）**——其余全部：定义、问题、目标、任务、教训、基石、感受报告、人物节点、证据、预测、矛盾。随之而来三条后果，而它们正是这条划分在一处声明、而不是由每个调用者各自推断的原因：

1. **置信度只对 CB 节点有意义。** 一条教训没有可供置信的真值；它是一种性情。写入路径——MCP 服务器暴露的那些节点创建工具，智能体的每一次写入都经由它们进入图谱——拒绝对一个 NCB 节点接受置信度；而每一个需要知道某条置信度谓词是否适用的调用者，都去问同一条规范谓词，而不是就地重新推导一遍那个成员资格判定。
2. **它决定自我纠正级联触及什么。** 这次遍历穿过承载主张的依赖项传播，并止步于身份层——基石与教训是 NCB，所以一条位于某条教训上游的撤回不会标记那条教训。这不是额外加装到级联上的一个特例；它是从这条划分里落出来的。
3. **NCB 是算出来的，绝不逐一枚举。** 它被定义为*图谱中实际存在的那些类型，减去 CB*——所以一个新的节点类型默认就是 NCB，而这个补集不可能与那条声明走岔。

`theory` 被声明为承载主张，目前没有实例；之所以列出它，是因为这条划分是关于种类的声明，而不是对恰好存在之物的清点。

| 类型 | CB？ | 角色 |
|---|---|---|
| **observation_factual** | CB | 一个事实，援引一条逐字来源引文 + 出处。情节的对应物。 |
| **observation_predictive** | CB | 一项带指名结算事件的前瞻性主张；在它尚未结算期间，置信度封顶于 0.60。 |
| **derivation** | CB | 一次推断，经由 `derives_from` 援引其前提，并声明其推理类型；置信度是*算出来的*，不是断言的。 |
| **definition** | ncb | 一个术语锚点（`df_*`）；被使用该术语的主张所引用（而非据以推导）。 |
| **conjecture** | CB | 一个思辨性的主张，置信度钳制在 [0.10, 0.60]（默认 0.40）；在它变强时升格为推导。 |
| **contradiction** | ncb | 一个记录两项主张相冲突的一等节点（不是一条边）；保留双方。 |
| **axiom** | CB | 一个终端的、被声明为根基的承诺；按类型置信度为 1.0。 |
| **cornerstone** | ncb | 一条从实践中提炼出的、构成身份的原则；铸造或退役一条都是罕见而审慎的：智能体只在一条原则于实践中证明了自己之后才铸造一条基石，且只经由一个指名其后继者的显式操作来退役。 |
| **lesson** | ncb | 一条从一次具体错误中提取出的、按情境打标签的持久绊线。 |
| **goal** | ncb | 一个终端的／身份方向性的标的。 |
| **question** | ncb | 一条显式的开放线索（那份活的科研议程）。 |
| **person** | ncb | 一个对手方节点（带信任层级 + `about` 边）。 |
| **feeling_report** | ncb | 一次对内部状态的自述，其构造是*"我报告感到 X"*，而绝不是*"我感到 X"*（不主张特权通道）。 |
| **theory** | CB | 一个被声明为承载主张的种类，在本图谱中没有实例（见上）。 |
| **evidence** | ncb | 一条为观察提供依据的出处记录（URL／文件 + git_sha + 逐字引文）。 |
| **task** | ncb | 一个被追踪的工作单元，带状态 + 重要性。 |
| **prediction** | ncb | 一项前瞻性主张的**结算追踪那一半**：归档一条指名了事件的 `observation_predictive`，同时也开启一个 `prediction` 节点（状态 `open`），由 `predicted_by` 链回。它自身不携带任何主张——主张由那条观察作出，而 prediction 节点追踪世界是否把它结算了。第二条指名同一事件的观察会链到那个既有的 prediction 上，而不是再开一个。 |

**身份稀缺是设计使然。** 在本文自己的图谱上测量，164 天（23 周）、10,361 个节点：**窄**集上终生的身份节点创建——基石、公理、目标与人物节点，不含教训——为 **131 个节点（75 个基石、11 条公理、28 个目标、17 个人物节点），占图谱的 1.26%**。（图 1 用的是**更宽的**集合，含教训，报告的数字在 3% 以下；它只计现行节点，且不含人物节点，所以两个集合并非嵌套关系；这里排除教训，是因为这条主张关乎*塑造身份*的写入，而一条教训是一道程序性的绊线——但两个数字描述的是同一张图谱，也都不算错：要比较它们，就必须把集合指名出来。）那是大约每周五到六个，而总写入速率接近 450。这条主张说的是那个比率，而不是那个计数：基底的构造方式让塑造身份的写入*相对于*普通知识保持罕见，而这一点在图谱增长时依然成立。*（这些数字是一张图谱在一个日期上的读数，会漂移；那个份额才是经久的陈述。）*

## E.3 边类型

关系也带类型；基底对不同的边区别对待。

每一种关系携带**六个彼此独立的标志**，而不是一个。把它们坍缩成单独一列"它是否承载级联"，会丢掉基底确实会据以行动的那些区分：

| 标志 | 它所支配的东西 |
|---|---|
| `cascade` | 级联遍历器沿这条边穿行 |
| `temporal_causal` | 目标必定先于源存在 |
| `dag` | 该关系必须保持无环，由一次真实的边遍历来检查 |
| `removable` | 该边创建之后可以被删除 |
| `addable_after_creation` | 该边可以被添加到既有的节点上 |
| `provenance` | 在解析一项主张的证据根时，这条边会被追溯到 |

| 边 | 含义 | 级联 | 时序 | 无环 | 可移除 | 可添加 | 出处 |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| **derives_from** | 前提 → 结论；级联借以穿行的通道 | ● | ● | ● | | | ● |
| **acknowledged_derives_from** | 一个已经认可了某次修正的节点，立在一条替代前提之上 | ● | | ● | | | ● |
| **cites** | 引用一个定义／上下文，不含推理依赖 | | ● | ● | | | ● |
| **supported_by** | 一条基石／教训指向它的范例证据 | | ● | ● | | | ● |
| **predicted_by** | 一个 prediction 节点 ← 作出该主张的那条观察 | | ● | ● | | | ● |
| **supersedes** | 认知演化：新节点替换旧节点 | | ● | ● | | | |
| **retracts** | 错误修正：目标从来不曾有效 | | ● | ● | | | |
| **subtask_of** | 任务分解 | | ● | ● | ● | ● | |
| **generalizes** | 一项更宽的主张把一项更窄的收摄于其下 | | | ● | ● | ● | |
| **contradicts** | 记录两项主张之间的一处冲突 | | | | | | |
| **resolves** | 一个解决节点闭合一处矛盾／一个问题 | | | | | | |
| **tensions** | 两个目标互相拉扯 | | | | ● | ● | |
| **exemplifies / instantiates / serves / about** | 分类性 + 关系性的边 | | | | ● | ● | |

**只有两种关系承载级联**：`derives_from` 与 `acknowledged_derives_from`。它们是遍历器所穿行的边。`supersedes` 与 `retracts` 是*启动*一次遍历、而自身不被遍历的事件——一个截然不同的角色，而把两者混为一谈是很容易的。`supported_by` 承载出处，所以一条位于某个基石范例上游的撤回是*可追溯*的，但不标记该基石。

**为什么 `dag` 与 `temporal_causal` 是两个分开的标志**——迫使它们分开的那个案例是 `acknowledged_derives_from`。一个已经认可的节点必然存在于它所最终落定的那条替代前提*之前*；认可这件事本身就是如此。所以这条边在创建时间上指向后方（`temporal_causal` 为假），却仍然必须保持无环（`dag` 为真）。那个诱人的捷径——*承载级联的关系之所以无环，是因为它们在时间上有序*——恰恰是那个抓不住这条边所能闭合的那个环的论证；无环性之所以由一次真实的边遍历来检查，而不是从时间顺序推断出来，原因就在这里。

`contradicts` 按设计不承载级联——归档一个矛盾不标记任何东西（见 E.5，那里重述了这一点与 `BLOCKED_CONTRADICTED` 前提守卫）。一条边只有在它的类型位于一张白名单上时才可被移除，那就是上文的 `removable` 列；承载级联的边与结构性的边不在其上。

## E.4 置信度模型（算出来的，不是标注的）

对观察与推导而言，置信度是**节点结构的一个计算属性**，而不是一个手工设定的数字（第 4 章 §4.3）；一条猜想的置信度由它的作者在归档时设定，钳制在 [0.10, 0.60]。它只存在于承载主张的节点上（E.2）。对一条**观察**，它由 `quote_type` × `source_class` 映射而来；对一条**推导**，它经由一个由 `reasoning_type` 选定的公式从前提传播而来。

**观察——`quote_type` 锚点。** 七个取值，降序：`hard_data` 0.95 · `official_statement` 0.85 · `attributed_analysis` 0.70 · `counterfactual_inference` 0.65（作为归属分析，再减去一项不可约的近似残差）· `unnamed_source` 0.50 · `personal_communication` 0.40 · `editorial` 0.35。调整：`source_class` 取三个取值之一——`external`（一份文档或一个第三方）、`introspective`（智能体自己此前的输出）或 `user_stated`（协作者自己所说）——所以下面两项调整绝不会落在同一个节点上：对 `source_class=introspective` ×0.95；`user_stated` 无论 quote type 为何都覆盖为 `official_statement`。一条前瞻性的观察在它的事件结算之前另被封顶于 0.60。

**推导——三条传播公式，而哪一条适用才是关键所在。** 推理类型并不只是缩放结果；它选定那次计算的*形态*，因为"许多彼此独立的证人"与"一条推断链"是不同的认知处境，绝不该按同一种方式计分。

| 模式 | 公式 | 推理类型 | 行为 |
|---|---|---|---|
| **佐证** | (1 − ∏(1−cᵢ)) × *d* | `inductive_generalization`、`inductive_enumeration`、`authority_consensus` | **强化型**——每增加一条独立前提都*抬高*置信度，而结果可以超过任何单条前提。**共同根独立性检查（§4.3）只在这三条中的两条上触发：`inductive_generalization` 与 `authority_consensus`。`inductive_enumeration` 在无护卫的情况下运行那条强化公式**，所以它的独立性是作者的判断，不会有任何警告到来。 |
| **最弱环节** | min(cᵢ) × *d* | 全部五种 `deductive_*`、`inductive_analogy`、`inductive_statistical`、`inductive_causal`、`authority_expert` | **限制型**——一条链不比它最弱的前提更强，再为那一步推理打折扣 |
| **带封顶的最弱环节** | min(min(cᵢ) × *d*, cap) | `abductive_best_explanation`（0.80）、`abductive_elimination`（0.90） | **有天花板的**——一个最佳解释*即便从完美的前提出发*也无法逼近确定性，因为替代项总是存在 |

*d* 是推理步骤本身按类型给出的折扣：演绎形式 0.98（保真，所以几乎免费）、`inductive_generalization` 0.95、`inductive_causal` 0.85、`abductive_best_explanation` 0.80、`inductive_analogy` 0.70——总共十四种（五种演绎——`deductive_modus_ponens`、`deductive_modus_tollens`、`deductive_hypothetical_syllogism`、`deductive_disjunctive`、`deductive_reductio`——五种归纳、两种溯因、两种权威），各有各的。

佐证公式是基底最强的工具，也是它最容易被误用的工具：**它只在真正独立的前提上成立。** 单一来源的两个侧面不是两个证人；把它们当作佐证来计分，就是从一件被数了两遍的证据里凭空制造置信度。基底在十四种推理类型中只对两种检查共同证据根，所以对其余各种，独立性是作者的判断，不会有任何警告到来。我们把这条公式与这个条件放在一起陈述，因为不带这个条件的公式是更危险的那一半。

**其余类型：** 猜想被钳制在 [0.10, 0.60]（默认 0.40）；公理按类型为 1.0。**不承载主张的节点完全不携带置信度**——一条教训或一条基石是一种性情，而不是一个命题，没有可供置信的真值（E.2）。*（这些常数是理论上导出、按出处分级的合理性，由设计者规定，而不是相对结果校准的——第 7 章 §7.2。）*

## E.5 自我纠正

自我纠正——撤回对取代、待决标记、每轮浮现钩子，以及整理期的前沿遍历——在第 4 章 §4.4 中完整给出，这里不再重复。另有两条其他附录所倚靠的事实：级联只穿行 `derives_from` 与 `acknowledged_derives_from`（E.3）；而一条 `contradicts` 边不级联——一个矛盾是一场活的争论，尚不是一次反驳——但任何援引了一条坐在未决矛盾之上的前提的新推导都默认被阻断（`BLOCKED_CONTRADICTED`），同时对刻意建在有争议一侧之上的智能体，有一个显式的、带审计戳的选择加入（`use_contested`）。

- 八个承重的**原语**：带类型节点、带类型边、出处、级联、取代、焦点模式（第 4 章 §4.8）、自动浮现，以及置信度模型——一切更高机制据以复合的那个最小生成集。

## E.6 OCC 阈值（Kahl 2026b），以及本文如何使用它

第 4 章的映射立足于 Kahl 的**本体论连续性条件**（Ontological Continuity Condition，OCC）；这里把各条条件完整给出，以便本附录脱离该章也能读。Kahl 自己的形式化陈述：*"A system S satisfies OCC if and only if the following three jointly necessary conditions obtain."*（中文解说：一个系统 S 满足 OCC，当且仅当下列三项共同必要的条件成立。）[@kahl2026b, p. 10]

**条件 1 —— 历时性约束（Diachronic Constraint）。**
> "Present deliberation within S is non-trivially constrained by S's past commitments,
> such that earlier commitments function as reasons structuring subsequent arbitration." [@kahl2026b, p. 10]

（中文解说：S 之内的当下审议，被 S 过去的承诺非平凡地约束着，以致较早的承诺作为理由，结构着后续的仲裁。）

注意它要求的是什么、不要求的是什么：不是系统*记得*它的过去，而是过去**约束**着当下的审议——什么都不改变的记忆不是历时性约束。

**条件 2 —— 重置下的不可互换性（Non-Interchangeability Under Reset）。**
> "Replacement of S by a functionally equivalent instance — including identical code and
> complete state snapshot — would constitute loss of the agent rather than substitution
> of an instance." [@kahl2026b, p. 10]

（中文解说：以一个个例功能等价的实例来替换 S——包括相同的代码与完整的状态快照——将构成该智能体的丧失，而不是一个实例的替换。）

这一条正是 ENGRAM 按其严格文本未能满足的：两个从同一份快照恢复出来的智能体，在恢复的那一刻*是*可互换的。第 4 章 §4.11 主张的是一处类型／个例的推广，而不是声称那种严格读法。

**条件 3 —— 自我维持的仲裁（Self-Maintaining Arbitration）。**
> "Conflicts among commitments are resolved within a unified deliberative architecture
> in a manner that preserves S's continued status as that subject." [@kahl2026b, p. 10]

（中文解说：诸承诺之间的冲突，在一个统一的审议架构之内得到解决，其方式保全 S 作为那个主体的持续身份。）

本文中心主张所系的那一条条件，也是附录 B 表明受调查系统中没有一个满足的那一条。三个词承着这个重量：**统一**（一个架构，而不是一个边车）、**解决**（而不只是检出），以及**保全 S 的持续身份**（智能体在修正之后与之前是同一个主体）。

**约束 A–D** 是防止平凡满足的护栏：不确定之下的统一策略选择；仲裁不被外部强加；系统不可被平凡重置；以及审议不可被模块化地分解而无剩余。否则，一个系统可以在字面上满足全部三项条件，而它的相容性却是由外部维持的，或是由一个可以被替换掉的模块维持的。

**映射另外使用的支撑装置**，各在首次引入之处界定：Peirce 的类型／个例之分（第 4 章 §4.11）；Nozick [-@nozick1981] 的最接近的延续者关系（第 2 章 §2.4）；检索画像（第 5 章 §5.4）；以及历史树（第 2 章 §2.2；第 5 章 §5.3）。AGM 信念修正只是为对照而提及，映射并未使用它（第 3 章 §3.9）。

## E.7 跨越压缩的连续性

- **双例程整理**（界定于第 3 章 §3.1）：**小憩**（压缩边界上按工作段的持久化）· **睡眠**（每日一次的复盘 + 整理 + 遗忘曲线推进 + 做梦式修复）——映射到清醒／NREM-REM 阶段。
- **压缩桥接脚手架**（第 3 章 §3.1）：**焦点清单**（小、固定大小，在每次会话开始时逐字呈现，无论新开还是压缩之后都一样——那条确定性的通道；见第 4 章 §4.8，那里载有这个机制，以及它为什么不是压缩前的摘要）、**温暖简报**那封信（它包含什么见附录 D §D.4，它的形态如何得来见附录 F）、按日历史日志、自动加载的会话开始上下文，以及一个显式的压缩后指令模板。按设计多重冗余。
