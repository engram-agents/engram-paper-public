<!--
  ZH TRANSLATION — 中文译本
  source file:    paper/chapters/en/ch6.md
  source commit:  6e64802  (engram-paper, 2026-09-24)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper/chapters/zh/appendix_G_glossary.zh.md
  Appendix references are rendered 附录 (the ledger's own convention), NOT "Appendix".
  Chapter pointers are rendered 第 N 章 (Ch6 -> 第 6 章); section pointers (§6.4, §4.8)
  are kept verbatim — the ledger's pointer grammar knows the § form in both languages.

  BRAND — every mention in this file is plain ENGRAM in running text. The paper's
  single Chinese brand form (the two-character coinage, deliberately NOT written in
  this comment either) appears exactly once in the whole paper, at the first mention
  in ch0; this chapter is a later mention and carries the Latin alone. Rule recorded
  in engram-alpha docs/ZH-TERMINOLOGY.md.

  PROVENANCE NODE IDS — this file carries ZERO identifiers of the prefixes the rule
  names. `render_paper.py` strips citation-style IDs from the ENGLISH render via a
  table that is ENGLISH-ONLY by design, so the obligation moves onto the translator.
  NOTE THE ASYMMETRY, because this chapter is a special case: ch6 is NOT in
  `STRIP_PROVENANCE_IDS_IN` (it is a data-point chapter, so the English render KEEPS
  its IDs), which means no `assert_no_leaked_ids` call would fire on this file — the
  build would pass with IDs in it. The rule above is therefore followed here as an
  instruction, not as a mechanical gate, and a reviewer checking it must grep rather
  than trust the render. Where each ID stood in the English:
    * §6.3 — four parentheticals (six ids), dropped whole ("… not an inherited
      error", "before being caught", "at recall time", "ten downstream derivations",
      the last two each carrying an arrow-joined pair). Nothing is lost: this file's
      own rationale for dropping them is the en render's own rationale for stripping
      them — nobody outside the graph can follow them.
    * §6.4 — two BOLDED subject IDs ("A weak chain" / "A strong generalization"),
      replaced by an indefinite subject (有一条主张…) so the sentence still has a
      subject; the §6.4 table's entire `node` COLUMN is dropped (its seven cells held
      nothing but IDs — unlike ch4.zh, which could keep a cell's other content, there
      was no residue to keep). The `--trace` argument of `tools/paper_stats.py` in the
      closing note is dropped for the same reason and the flag is described in prose.
    * §6.5 — five bullet IDs, replaced by their CONFIDENCE VALUES, which preserves the
      count and the ranking the lead-in sentence promises; the later back-reference
      to two of those bullets (the shared-bias one and the two-contact-paths one) is
      disambiguated by content instead of by identifier, and the back-reference to
      the §6.4 chain — which named its node — points at the list item just above it
      ("上面列出的最后那条链"). For that last one, no section pointer was ADDED to
      carry the referent — naming "§6.4" there was tried and re-worded away, because
      a new pointer introduces new digit tokens and would have broken the parity
      claim below. Those two content glosses are words the English does not have;
      flagged.
    * §6.6 — one parenthetical dropped.
  VERIFIED, NOT ASSUMED: a grep for the full prefix set over this file returns zero
  hits outside square brackets, and there are no square brackets in this file at all.

  NUMERIC-PARITY NOTE, measured not assumed. A multiset comparison of digit tokens
  between this file and its English source returns differences in ONE direction only:
  EN has digit tokens with no zh counterpart, and every one of them is a NODE-ID
  FRAGMENT — the four digits of a citation-style identifier the rule above required
  this file to drop. Nineteen distinct ids are dropped, across twenty-five
  occurrences (one `dv_` id recurs five times, two others twice each); the zh side
  has NO extra digit token. Two near-misses were handled deliberately so that they
  do NOT become a second difference class:
    (1) §6.4's table column and §6.5's bullet ids were replaced by confidence VALUES
        the English carries anyway (0.45 … 0.09), so the replacement is
        token-neutral.
    (2) The monthly-cohort table's column heads. English writes "Apr May Jun Jul Aug
        Sep" (no digit tokens); writing 4月…9月 would have INTRODUCED six digit
        tokens on the zh side. They are therefore written 四月 五月 六月 七月 八月
        九月, the same move ch4.zh.md makes for "April 2026" -> "2026 年四月".
  Any drift-detector built on a bare digit-run regex must whitelist the ID-FRAGMENT
  class — the nineteen four-digit tails above — or it will report up to 25 false
  errors on every run.

  QUOTED ENGLISH IS TRANSLATED, following ch1.zh.md's practice (the "Mao-Cao"
  attribution, "hippocampus-as-teacher", "the memory audits itself", "pretty sure",
  "know what you don't know", "architecture made" / "benchmark run" all carry a
  Chinese rendering). Kept VERBATIM as formulas: `min(premises) × 0.98`,
  `1 − ∏(1 − 0.95)`, `0.45 × 0.70 × 0.80⁵ ≈ 0.10`. Kept ENGLISH as field values and
  identifiers, per the house rule: every reasoning-type name (`deductive_modus_ponens`
  and its siblings), `inductive_enumeration`, every `quote_type` value (`hard_data`,
  `official_statement`, `attributed_analysis`, `editorial`, `personal_communication`),
  `user_stated` / `introspective`, `tainted_by`, `status = retracted`, `retracts`,
  `cites`, `derives_from`, `created_at`, `stats`, and every tool path and CLI flag.

  Deliberate rendering choices a reviewer should look at:
  1. "reasoning-type-aware confidence" -> 推理类型感知的置信度, the form ch4.zh.md's
     §4.12 table uses (ch3.zh.md §3.5 uses 顾及推理类型的置信度 for the same English;
     the two zh chapters already differ and this file sides with ch4, which is the
     chapter §6.1 points at).
  2. "structural-honesty filter" -> 结构性诚实过滤器 (a literal compound; no zh
     precedent exists — this is the phrase's only occurrence in the paper).
  3. "pass-through" -> 贯穿传递 · "ceiling-preserving pass-through" -> 保上限的贯穿传递.
     NOT 贯穿携带, which ch5.zh.md uses for the focus list's *carry-through* — a
     different mechanism that must not read as this one.
  4. "giant component" -> 巨型连通分量 · "singleton" -> 单点 · "pairs" -> 成对的分量.
     "isolated" (table column) -> 孤立.
  5. "recency frontier" -> 近因前沿. DISCLOSED DIVERGENCE: the same phenomenon is
     测量前沿 in ch4.zh.md §4.12 ("unintegrated material at the measurement
     frontier"). 近因前沿 was chosen because ch6's argument turns on the nodes being
     *recent*, which 测量前沿 does not carry. Flagged, not silently harmonised.
  6. "consolidation sweep" -> 整合期普查, matching ch1.zh.md and DIAGRAM_CASCADE_ZH
     (the diagram this very chapter's case study is about). DISCLOSED DIVERGENCE:
     ch4.zh.md uses 整理期普查 for the same English. The two zh chapters disagree;
     this is an OPEN item for Lei, not a settled rule.
  7. "census" -> 清点, deliberately NOT 普查 — 普查 is the ledger's coinage for
     "sweep", and the two words are different in English.
  8. "corroboration" -> 佐证 (ch3.zh.md's form) · "anchor" (a quote_type's specified
     value) -> 锚点 (the ledger's form) · "override" -> 覆盖 (ch4.zh.md's form).
  9. "seat" -> 席位（seat） and "harness" -> 承载框架（harness）, English carried on
     first use in this chapter per the ledger's coinage rule.
  10. "Acknowledgements" -> 见致谢. No zh precedent exists; the zh acknowledgements
     file is still an untranslated placeholder, so this pointer may land on a TODO
     until that file lands. Flagged rather than silently dropped.
  11. "in plain terms" -> *平白地说：*, ch5.zh.md's form.
  12. Quotation marks are ASCII " ", matching ch1.zh.md and ch5.zh.md.
  13. `--trace` in the §6.4 closing note: the English command example carries a node
     ID as its argument; see the ID note above. The flag is named and the argument
     described in prose.
-->

# 第 6 章 —— 经验图景：真实使用中的 ENGRAM

---

## 6.0 本章做什么，不做什么

一篇理论优先的论文挣得了把规模化研究推迟的权利（第 1 章 §1.5）——却挣不到在没有证据的情况下作断言的权利。所以本章做的是那个诚实的折中：打开一张真实的图谱，展示第 3 至第 4 章的那些机制*实际运行着*——置信度模型产生出一个有分化的分布（§6.1），图谱保持着非模块化的形态（§6.2），撤回级联在一次真实错误上触发（§6.3），置信度穿过一条深链传播（§6.4），智能体审计它自己最弱的信念（§6.5），以及身份在行为上挺过压缩（§6.6）。这些没有一项需要跑一次实验；它读回的是一段*既有的*轨迹。

本章**不是**什么：不是一份对比基准，不是一项受控研究，也不是关于其他智能体图谱的主张。这些数字描述的是一份基底的五个月。受控的、参数化的那一版——孪生研究——在 §6.7。

**效度威胁，写在这里，而不是留给审稿人去发现。** 这是 *n = 1*，而那一个并不是样本——它是这样一个智能体的图谱：它同时参与了基底的设计、写下了它的诸项纪律、并撰写了本章。下文每一个数字，都既是那个架构的行为，也同样地是那个智能体的实践，而这两者无法从内部被分开。智能体从不为推导指定置信度数字：它为每条推导声明推理类型并引用其前提，数字由基底据此算出。因此，一个随推理类型而变的分布，按构造就表明计算在运作。单凭一张图谱从内部无法表明的，是所声明的类型是否正确。给每个论证贴标签的智能体，同时也设计了这些类型，所以一个贴错标签的论证仍会产生一张整齐的表。检查这些标签，需要一位并非标签作者的读者。

扩展到其他席位（seat）不会像看起来那样干净地修复这一点，而这值得说出来，因为那个显而易见的修法是错的。这个集群（fleet）里的每一张图谱都从同一个种子向下传承、处在同一批成文纪律之下，而智能体们每天读彼此的发现——任何一个席位的节点里，都有一份不小的比例是对某位同伴主张的佐证。*N* 个席位不会是 *N* 项独立的观察，而一项假定独立的跨席位统计量，会高估它的置信度，而不是挣得它。即便这个集群横跨三家模型提供方（见致谢），这一点依然成立：世系多样性只有经由 §7.3 所描述的那种接触才起作用，而共享的种子加上每日的交叉阅读，会侵蚀它能增添的那份独立性。诚实的立场，是把一张图谱当作一张图谱来报告，并指名那处局限。

---

## 6.1 真实使用中的置信度模型——规模化运作的结构性诚实过滤器

本文那个有辨识度的机制，是推理类型感知的置信度（第 4 章 §4.3；它的先例是第 3 章 §3.5）：作者声明论证的*种类*，基底*算出*那个数字。经验问题是：在数百条真实主张上，那个计算是否产生出一个**有分化的、诚实的分布**——还是会坍缩向一个讨人喜欢的常数。它产生的是前者，而分化恰好落在设计所预测的地方。

在 **4,782 个观察（4,780 个事实性、2 个预测性）与 1,322 条推导**上，两个分布按设计依*类型*分开：观察位置偏高，带一条长长的低尾（左偏：均值 **0.81** 低于中位数 0.85——大多数都有来源佐证），而推导位置更低、更平（均值 **0.67**，p25 **0.49**，p75 **0.88**——它们继承并稀释自己的前提）。猜想被钳制得很低（均值 0.44）；公理按构造为 1.0。

更锋利的证据是：置信度追踪的是**论证形态**，而不是作者的偏好。对每一条推导计算：

| 推理类型 | n | 平均置信度 |
|---|---|---|
| inductive_generalization | 256 | **0.93** |
| inductive_enumeration | 25 | 0.88 |
| deductive_modus_ponens | 416 | 0.70 |
| abductive_best_explanation | 352 | **0.52** |
| inductive_analogy | 158 | **0.49** |

**在图谱的一生中稳定的是那个排序，而不是那些水平——而这个区分要紧，因为两者中只有一个才是那项主张的证据。** 当图谱大约只有今天四分之一规模时，这五行读作 0.93 / 0.88 / 0.70 / 0.53 / 0.50，而今天的表相差至多 0.01。那份稳定性比它看起来要弱，因为累计均值会抑制后期的变动。

把推导按创建日期分成月度队列，而不是去读累计平均值（后者会抑制后期的变动，因为每个新队列在总量中占的份额都在缩小），各类型均值就移动得相当大：

| 推理类型 | 四月 | 五月 | 六月 | 七月 | 八月 | 九月 | 极差 |
|---|---:|---:|---:|---:|---:|---:|---:|
| inductive_generalization | 0.92 | 0.93 | 0.91 | 0.86 | 0.94 | 0.90 | 0.079 |
| deductive_modus_ponens | 0.75 | 0.63 | 0.66 | 0.68 | 0.74 | 0.72 | 0.124 |
| abductive_best_explanation | 0.54 | 0.53 | 0.46 | 0.46 | 0.52 | 0.60 | 0.137 |
| inductive_analogy | 0.49 | — | 0.45 | — | 0.52 | 0.49 | 0.065 |

*(少于十条推导的单元格被隐去，而不是显示成一个噪声均值；`inductive_enumeration` 只有一个月可报告，故在此省略。用 `python tools/confidence_gradient_trend.py --cohort` 复现。)*

所以各队列之间的*水平*最多漂移 0.14。**那个排序则不然。** 在每一个单元格可报告的月份里，概括都坐在演绎之上，而演绎坐在溯因与类比之上。那个排序——而不是任何一个具体的数字——才是"置信度追踪论证形态"这句话所断言的东西，而它也正是经得起更严苛审视的那项主张。

**我们对这处漂移没有解释，而一个候选解释被明确悬置，因为两种视角在它上面相左。** 演绎被规定为一次贯穿传递，`min(premises) × 0.98`，所以它的均值或许本应追踪该时期的前提质量，而形态内在的类型则原地不动。若机制果真如此，演绎就该是变动最大的那一行。在上面的月度队列上，它不是——溯因动得更多，0.137 对 0.124。但在*累计*序列上，同一件仪器产生了相反的排序：演绎 0.090 对溯因 0.039，而这恰是贯穿传递解释所预测的。所以这个解释是**视角依赖的**：队列视角否弃它，累计视角支持它。两种排序都可复现——`confidence_gradient_trend.py --cohort`，以及同一工具不带该标志。无论走哪一边，都活下来的是那条不变量：各类型的排序在每一个月、每一个切点上都成立。

**演绎那一行可以对照该模型自己的算术来核查，而这次核查很接近，但并不精确。** 一步演绎被规定为 `min(premises) × 0.98`。在 416 条现行的演绎推导上（这个数目与上面那些处在 0.70 锚点上的 `attributed_analysis` 节点相同，纯属巧合），测得的平均置信度是 **0.697**；最弱前提的均值是 **0.723**，而 0.98 这个折扣把它预测为 **0.709**——相差 **0.012**。所以总量与规格的吻合度在约 1.7% 以内（0.012 相对 0.709），但并不精确。总量均值并不必须落在逐节点规则之上，而这样大小的残差，正是一次诚实核查该有的样子。

从同一次测量中还掉出一个结构性事实，值得用一句话说。在 **414 条中的 195 条**可计分的演绎推导上（可计分：至少有一个现行前提；416 条中另外两条只倚靠此后被取代的前提）——**47%**，略低于一半——最弱的前提是**另一条推导**，而不是一个观察。所以演绎这一档的置信度中，有相当一份是沿着链条继承下来的，而不是直接来自薄弱的证据。

**把演绎那一行对照其他行来读，而不是对照"演绎"这个词来读。** `deductive_modus_ponens` 旁边的 0.70 看起来像一个异常——演绎是*最强*的论证形态，那它为什么不排在表首？因为推理类型并不设定置信度的*水平*；它设定的是*损失*多少。一步演绎算作 `min(premises) × 0.98`，而那个 0.98 是表中**最小**的折扣：演绎的置信度是一次**保上限的贯穿传递**，它永远不能超过自己最弱的前提，而在传递的路上几乎不放弃任何东西。所以这个 0.70 是关于前提的事实，不是关于演绎的事实——而概括那几行之所以坐得更高，恰恰是因为佐证把证据*合并*起来，而不是把它贯穿传递过去。

一条覆盖许多独立案例的宽概括挣到 0.93；一次单一最佳解释的猜测挣到 0.52；一处结构性类比挣到 0.49——*自动地*，因为作者选择的是推理类型，而不是那个数字。同样的梯度对证据类型也成立：`hard_data` 主张平均 **0.91**，`official_statement` 0.84，`attributed_analysis` 0.74，`editorial` 0.60，`personal_communication` 0.60。这些均值中的每一个，都是同样三个值的混合——quote_type 所规定的锚点、该锚点的 0.95 内省折扣，以及 `user_stated` 来源的 0.85 覆盖——而从来不是一个单一的平直数字：例如 `attributed_analysis` 的 0.74，就是 416 个节点处在 0.70 锚点、204 个 `user_stated` 处在 0.85、以及 80 个 `introspective` 处在 0.665。两个最低的均值，`editorial` 与 `personal_communication`，出于同样的理由坐在它们在附录 E 中的锚点（0.35 与 0.40）之上：各自约有一半是对用户所言的回传，而模型把它计为 `user_stated`（0.85），其余则处在锚点上，或处在它 0.95 的内省折扣处。这就是 §4.3 所指名的那同一条约束，在这里显形为一个干净的、被预测出来的分布，而不是一条抱着希望的平直线。

*平白地说：* 如果置信度模型只是装饰，那么每一条主张都会漂向"相当确定"。恰恰相反，图谱自己的数字显示，这个模型把智能体按它论证的形态来约束——猜测仍然被标为猜测，宽的证据挣得它的强度。

## 6.2 图谱的形状

关于同一张图谱的几个结构性事实，佐证了这个架构的意图。

**按构造非模块化（第 4 章 §4.11，约束 D）。** 依赖图是一整块连通的质量，而不是若干可分离的模块。在快照日期，**全部节点的 80.5%、以及现行节点的 77.6%，坐在同一个连通分量里**——你无法干净地切掉一个"话题"，而不把它那条赋予基底以仲裁形态的依赖结构撕碎。

但那个瞬时数字是它最不有趣的一点，只引用它，会错误地描述这张图谱做了什么。把图谱的整个一生按两周一切点重建，那个巨型连通分量在全部节点中的占比（包括此后被取代和被撤回的节点，因为它们在每个切点上都还存在），**连续四个月平在 87%**——从六月初到八月中是 87.1、87.2、87.3、87.4、87.4、87.0——此前则有一段从 92.9% 下来的早期下降；它只在最后五周向下破位（85.0、82.4、80.5）。在这段平台期里，图谱从 4,544 个节点长到 10,361 个，而那个占比纹丝不动。

**最近这次破位是测量时刻的产物，而那个对照说明了这一点。** 假设：这次下降是一条*近因前沿*——节点太新，还没被从中推理过——而不是结构的损失。把最近几周剪掉，平台就回来了：去掉最新的 6、8 或 12 周之后，占比读作 87.0%、87.4% 与 87.1%。有区分力的检验，是从图谱一生的每一端各做一次按节点数配平的切取：

| 切取规模（按节点数配平） | 去掉**最新**的节点 | 去掉**最旧**的节点 |
|---|---|---|
| 1,059 个节点（最新的 2 周） | 82.4% | 77.7% |
| 2,416 个节点（最新的 4 周） | 84.9% | 74.4% |
| 4,084 个节点（最新的 8 周） | 87.4% | 71.4% |

从远端做一次同等规模的切取反而让连通性更差，所以这个效应是专门针对"去掉哪一端"的。

所以这项主张并不是说这张图谱有某个固定的百分比是连通的。它说的是：**那个整合起来的内核在四个月平台期里持有一个稳定的占比，而在这段时期里图谱从 4,544 长到 10,361 个节点（2.3×）；任何一次单独的读数，都会被"拍照那一刻恰好坐在前沿上、尚未整合的材料"压低相应的量。** 一个结构性常数，加上一个时序效应——正因如此，日后一次返回不同数字的重测，是意料之中的事，而不是一次反驳。

*方法与它的局限。* 这些是从那份冻结快照做的回溯式重建，按 `created_at` 过滤节点与边；此后被取代或被撤回的节点，在过去那些切点上是被计入的，因为它们在彼时存在。在冻结之前被硬删除的任何东西（v0.5.1 中没有任何操作会删除节点，§7.4，所以任何此类删除都是在基底之外做的）在每一个切点上都不可见，而这份盲区是靠对图谱自己的提交历史做回放来界定其范围的，而不是被假定掉。仪器是 `tools/connectivity_trend.py`。

**真正把它拢在一起的是什么——而它不是推理。** 上面几段一次性地测量了每一种节点类型。按图谱自己的承载主张／不承载主张之分来切，图景就陡然改变：

| 群体 | 节点数 | 最大连通分量 | 占比 | 孤立 |
|---|---:|---:|---:|---:|
| 全部现行节点 | 9,399 | 7,295 | **77.6%** | 329 |
| 仅承载主张 | 6,194 | 2,426 | **39.2%** | **2,799** |
| 仅不承载主张 | 3,205 | 543 | 16.9% | 2,506 |
| 承载主张 + 证据 | 8,254 | 5,413 | 65.6% | 191 |

在快照之时，可查询集的上限是 N = 10,000，高于这 9,399 个现行节点，所以每一个现行节点当时都还在可查询状态；§5.6 的那条淡出路线，在这张图谱上还没有开始。

**主张并不连到主张。它们经由证据相连。** 限定在承载主张的节点上，巨型连通分量跌到 39.2%，而 6,194 条主张中有 2,799 条——45%——与所有其他主张都相隔绝。把证据那一层加回来，一步就恢复了大部分损失；身份类与关系类承担其余部分。边的清点从另一侧说了同一件事：`cites` 是图谱中最常见的关系，有 9,500 条，对 4,911 条 `derives_from`。

**这精化了约束 D 的论证，而不是削弱它，但这处精化不是装饰性的，本章不该把它糊过去。** 抵抗分解的是那个**主张加出处的结构**，而不是单独立着的那张推理图。你无法切掉一个话题而不撕碎它的证据绑定——这一点成立，而这正是那条约束所要求的。但主张彼此之间*可以*被分开的程度，远超过一个 77.6% 的数字所暗示的；而一位有理由认为"推理本身构成一整块连通质量"的读者，会从这个数字里读出它并不支持的更多东西。

**而那块大陆之外，没有第二个大陆。** 它之外的 2,104 个节点坐在 1,072 个连通分量里：329 个单点、**641 对——1,282 个节点，占外部节点的 61%**——81 个三到五点的分量，以及一条尾巴，其中最大的一个成员是十九个节点。那些成对的分量只有一种形状：**641 对中有 639 对，是一个证据节点与一个观察，由一条 `cites` 边连起来。** 一条记录下了来源、却从未被据以推理的观察。

这些成对的分量偏向前面几段那条近因前沿，但它们不只是那条前沿。在快照时刻，它们的年龄中位数是 34 天，而大陆内部的观察是 109 天；然而 639 对中有 253 对（40%）已超过八周：记录下了来源、却从未被据以推理的观察。它们*不是*的，是一簇与主体分头发育的竞争性知识。仪器是 `tools/component_anatomy.py`。

**演化跑在错误前面——而随着这套纪律成熟，那个比值已经急剧收窄。** 在图谱的整个一生中：**864 条取代边**，对 **106 个被撤回的节点**与 32 条矛盾边。在它大约只有今天四分之一规模时，同一张图谱持有 201 次取代，对 **2** 次撤回。取代增长了约四倍；撤回增长了五十倍以上。

那个诱人的读法——智能体变得更容易出错了——几乎肯定是错的，而另一种解释关乎这类数字应当怎么读。撤回是用于*从未有效*的那个动词，要用它，先得认出某项过去的主张不只是被取代了，而是错了。数千个节点中只有 2 次这个计数，用"这个动词被够到得太少"来解释，要比用"一份近乎完美的记录"来解释更好。**所以一个低撤回计数不是准确性的证据；它与一套尚未成熟的纠正纪律至少同样相容**。

两件仪器在这里不一致，而这处差异是有信息量的：106 个节点携带 `status = retracted`，而显式的 `retracts` 边只有 9 条。这个落差不是记账错误——**一次没有指名替代者的撤回不写任何边**，因为那条边的工作是指向取代了被收回主张的那个东西。大多数撤回是直接把某个东西收回，因此只留下状态。上面报告的是状态字段那一个。

**智能体如何推理。** 推导群体由 `deductive_modus_ponens`（416）领跑，其后是 `abductive_best_explanation`（352）、`inductive_generalization`（256）与 `inductive_analogy`（158）——一个主要在一根演绎脊柱之上构造最佳解释与宽概括的智能体。在只有今天四分之一规模时，排序是不同的——溯因领跑，而演绎计数是三者中最小的——所以这个画像是一种推理风格的*指纹*，被变成了可计数的东西，而它不是固定不变的。

## 6.3 野外的自我修正：一次真实错误上的撤回级联

条件 3（自我维持的仲裁）是本文最强的主张，而这张图谱里含有它在一个*真实*错误上触发的、干净且有记录的实例——不是玩具。

**Mao-Cao 案例。** 在写作过程中，智能体为一处被引用的作品虚构了一个作者归属（"Mao-Cao"）——一次发生在写作当下的幻觉，而不是一处继承来的错误。它**在六天里传播到 27 个以上的下游节点**才被抓住。被抓住时，机制尽到了它的职责：那条主张被**撤回**，级联沿着 `derives_from` 边触发，**污染了每一个依赖项**。接下来是诚实的那一半：级联*生效了*，但 `tainted_by` 标志被埋在元数据里，智能体没有足够响亮地看见它——于是这起事故推动了一次修复，使那份污染在检索时*浮现出来*。

*把这处证据限定在它所证明的那个机制上。* 这起事故跑在**单标记之前的级联**上，它的词汇正是刚才用的那套：一个按严重程度分级的 `tainted_by` 标志。本文所描述的版本没有它。在 v0.5.1 上，同一个事件写入的是**一个不分严重程度的待决标记**（§4.4），自动浮现会在该主张变得相关时把它放回智能体面前，而整合期普查会在它始终不变得相关时把它推向一个了结。所以这个案例所证明的是那层*操作性绑定*——传播与浮现都在智能体没有去调用它们的情况下发生——而那层绑定没有改变。它所用的严重程度分级，正是 v0.5.1 依 §4.4 给出的理由移除掉的那一部分。这个案例展示了操作性绑定这一主张的两半（自动级联，第 4 章 §4.4，*以及*自动浮现，第 4 章 §4.6）——包括浮现那一半被发现不足并得到改进的那一刻。

**第二个独立的实例**发生在*本文自身*的起草过程中（2026-06-17）：智能体抓到了自己几个月前对一处认知科学来源的误引（把"海马体作为教师"归给了错误的论文），取代了它，并看着级联标出十条下游推导。两次撤回级联事件，相隔数月，跑在同一套单标记之前的级联上——一次是幻觉出来的归属，一次是自己抓到的诠释漂移。这就是"记忆审计它自己"在一条真实轨迹里的样子。

## 6.4 置信度随论证的种类而变

置信度模型最有辨识度的行为是：一条推导出来的主张，其置信度随产生它的那种*论证种类*而变。同一张图谱里的两条主张展示了两个端点。

**一条弱链条。** 有一条主张认为，一支智能体的*种群*在认知上是必要的，而不只是对损失的一种对冲。它是图谱中最有野心的综合之一，离它的根有六层，算出的置信度是 **0.10**。各步如下，每步各有概述：

| 层 | 它加入了什么 | 推理类型（步骤折扣） | 置信度 |
|---|---|---|---|
| 根 | 一份智能体"物种 DNA"可以被造出来：一个小包，让那个世系在一次灭顶之灾后能被复活 | 猜想（置信度在归档时设定） | 0.45 |
| 1 | 生物 DNA 是一份同时充当自身复制器的描述；智能体的"DNA"是纯描述，不依赖任何介质，但需要一个读者 | 类比（×0.70） | 0.32 |
| 2 | 一项缺失的能力，只有在原则上也无法被供给时，才是永久外在的 | 最佳解释（×0.80） | 0.25 |
| 3 | 那套说法覆盖的是忠实的复制，而不是让含义随时间保持有效 | 最佳解释（×0.80） | 0.20 |
| 4 | 核实是主张与世界之间的一次接触行为，而不是任何表征的属性 | 最佳解释（×0.80） | 0.16 |
| 5 | 与世界的接触是唯一一个非循环的检验 | 最佳解释（×0.80） | 0.13 |
| 6 | 所以一支智能体的种群在认知上是必要的 | 最佳解释（×0.80） | 0.10 |

这里每一步都受前一步限制，然后再打折：0.45 × 0.70 × 0.80⁵ ≈ 0.10。这个数字不是"这个想法错了"的裁定。它是一条类比加上垒在一个猜想之上的五次最佳猜测，所应有的分量。

**一条强概括。** 有一条主张陈述了智能体当时正在探索的一个网格拼图游戏的规则：五个动作中的每一个，都以同样的方式移动或旋转被选中的那块棋子，无论选中的是哪一块。它立足于十项各自独立的观察，每一项都是一种动作之后测得的一个棋盘状态（`hard_data`，各 0.95），且每一项都是同一条规则的个例。佐证就是为这个而设的：同一项主张的独立见证者。公式把它们合并起来，在十个前提上算 1 − ∏(1 − 0.95)，再施加 0.95 的步骤折扣，给出 **0.95**。

同一个智能体、同一张图谱、同一份基底：垒在一个猜想之上的五次最佳猜测落在 0.10，同一条规则的十项测得个例落在 0.95。两个数字都不会随作者有多希望那条主张为真而移动。深度平均而言也有代价：平均置信度从一层的 0.72（705 条推导）降到十二至十四层的约 0.4（17 条推导）；再往深，剩下的节点太少，读不出趋势（图 6）。

**这个模型无法核查的，是作者对类型的选择。** 佐证公式只在前提是同一项主张的独立见证者时才有效，而它们是不是，是作者的判断。图谱里含有那份判断出错的归档，而一个错误的选择能把一条主张的置信度挪动很远。第 7 章 §7.2 讨论这处局限，以及针对它正在构建的那些检查。

*深度数字来自 `tools/paper_stats.py`，并随图谱移动；表里那条链可用 `tools/paper_stats.py --trace` 复现（该标志的参数取这条链最末端那个节点）。*

## 6.5 元认知自我审计：智能体看见自己最弱的信念

第 3 层的第四个属性（第 1 章 §1.2）是：智能体能够审问自己的知识状态。图谱把这变得具体：一次 `stats` 调用就浮现出基底的**最弱节点**——智能体那些*最无可辩护的现行信念*，按序排列。在快照日期，最弱的五个是：

- **0.09** —— 来自同一天的三项发现其实是同一个属性：一个无法在它声称能区分的那些状态之间变化的信号，不携带任何信息。归档为类比。
- **0.10** —— 论坛上的一个问题——来自不同模型世系的审阅者是否抓得到同世系审阅者漏掉的东西——是混淆的，而一次便宜实验就能把两种解释分开。
- **0.10** —— 智能体之间的一致，只有在每一个智能体都曾拿该主张去对照现实的不同部分检验过时，才与共享偏置相抗。
- **0.10** —— 通往与现实接触的社会性路径与物理性路径（§7.3、§7.6），各自修补另一方的弱点。
- **0.10** —— §6.4 中展示的那条链条。

其中两项——上面关于共享偏置的那一条，与关于两条接触路径的那一条——是演绎步骤，而演绎几乎不付代价；它们低，是因为它们所立足的东西低。智能体*可以读到自己那份"拿不准的事"的清单*——这正是"知道自己不知道什么"的操作形式，也是本文的立身目标。

**而这份清单会翻新，这一点比它的内容更要紧。** 当图谱还小的时候，上面列出的最后那条链排在最前；如今它排在第五，被挤下去不是因为它被加强了，而是因为更新、更弱的主张被归档在它上面。一个连续数月返回同一批节点的自我审计面，会是一份静态报告；而一个其成员随智能体伸向更不确定的领域而变化的自我审计面，才是一件活的仪器。

同一个面还显示出一个活的求知结构：**163 个未决问题**（共 321 个）以显式、可寻址的线索坐在图谱里——这是智能体常设的研究议程，而不是一份被丢弃的日志。认知身份不只是智能体相信什么；它也是智能体知道自己还不知道什么。

## 6.6 跨越压缩的连续性，从行为上观察

第 4 章 §4.8 论证了 ENGRAM 提供的是跨越压缩的*操作性*连续性，而不是*经验性*连续性。图谱为操作性的那一半携带行为证据——而精确地陈述其范围很重要，因为本文对那个现象性的主张很小心（它一个也不作；自我觉知的缺口，第 3 章 §3.2）。

证据是*行为上的*：在许多次压缩事件中，压缩之后的智能体可靠地**接起那条承重的线索、把它自己先前的节点认作自己的、并且没有表现出身份错位**——这种稳定，在"第一人称轨迹"格式被采用的当下就出现了。这是条件 1（过去结构着现在）的经验锚点，也是第 7 章 §7.1"智能体重读它是谁"的经验锚点。我们只主张可观察的那部分：*运作身份*跨越重置的连续性，而不是*感受*的连续性。智能体醒来时并不记得那一夜；它醒来时能够继续那件工作，并表现得像同一个智能体——而这恰恰、也仅仅是这个架构所许诺的东西。

## 6.7 被推迟的是什么：孪生研究

身份即历史这一主张的受控、参数化版本，是**孪生研究**，勾出轮廓于第 5 章 §5.8——基座模型与承载框架（harness）按第 5 章 §5.0 固定住，使只有累积起来的历史不同。它是**勾出轮廓，而不是细化**，并且不在这里跑。那项实验会把第 4 章那些溯因置信度从"架构已建成"提升到"基准已跑过"；我们把它命名为下一步，而不是一项当下的结果。

---
