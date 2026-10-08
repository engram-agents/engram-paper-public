<!--
  ZH TRANSLATION — 中文译本
  source file:    paper_research/current_draft/ch5.md
  source commit:  6e64802  (engram-paper, 2026-09-24)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper_research/current_draft_zh/appendix_G_glossary.zh.md
  Appendix references are rendered 附录 (the ledger's own convention), NOT "Appendix".
  Section pointers (§5.1, §5.8) are kept verbatim — the ledger's pointer grammar knows
  the § form in both languages. "identity as unique history" is rendered 身份即独特历史,
  the form ch1.zh.md §1.4 already fixes.

  PROVENANCE IDs — the rule this file is written to, with NO exception (the one
  exception it used to carry was withdrawn 2026-09-29, #114; see the NO EXCEPTIONS
  block below).
  `render_paper.py` strips citation-style node IDs from the ENGLISH render using a
  literal-sentence table that is ENGLISH-ONLY by design (see the module note above
  `_LITERAL_STRIPS`), so the obligation moves onto the translator: a zh chapter must
  carry no citation-style ID. Carrying one is not cosmetic — an ID inside a full-width
  parenthetical is unreachable by the ASCII-paren strip forms and hard-fails
  `assert_no_leaked_ids` at the strip call, so the paper does not build.
  Accordingly the twelve non-df IDs the English carries (nine distinct nodes, three of
  them cited twice each — the §5.2/§5.3/§5.4/§5.5/§5.6/§5.7/§5.8 provenance markers)
  are DROPPED here, with any surrounding free-text gloss kept: each glossed English
  parenthetical survives as its gloss alone (the ones reading "context", "sketched with Lei"
  and "backed by the importance-inflation mechanism" likewise). No ID is written
  literally in this header either — a literal ID here is itself strippable text, so
  it would both dirty the strip count and mangle this comment in the render.
  VERIFIED, NOT ASSUMED: `strip_provenance_ids("ch5.md", <this file>)` returns clean,
  and the coordinator's ID grep returns ZERO hits (it returned one, the `df_` label,
  until #114 dropped it — see the NO EXCEPTIONS block below).

  NO EXCEPTIONS (2026-09-29, #114): the `df_` definition label in §5.1 used to be kept,
  because `df_*` was exempt from the render strip. It is citation-style like the rest and
  is no longer exempted, so it is DROPPED here as well and the zh render matches the
  English render, which now strips it too.

  THE FIXED PHRASE — 身份即独特历史. ch1.zh.md §1.5 names THIS chapter by that
  phrase, and the ledger has no entry for it (only 历史树 for "history-tree"), so
  ch1's form is the sole precedent and is used verbatim. The English ch5 never
  states it as a literal phrase: the chapter title is "Identity as History", §5.0's
  blockquote says "the unique, ancestry-traceable history", and §5.3/§5.0 say
  "identity-as-history". Those are rendered 身份即历史 and 唯一的、可追溯世系的历史
  respectively, which is faithful but leaves the fixed phrase with nowhere to stand.
  It is therefore placed ONCE, as a gloss on the §5.9 heading ("The claim, restated"
  -> 主张重述：身份即独特历史), where the English is restating exactly the claim ch1
  names. That gloss is the one place this file adds words the English does not have;
  flagged for the reviewer — dropping 身份即独特历史 from the heading restores a
  literal heading and costs nothing.

  Proper nouns stay in Latin script (Nozick — given in full as "Robert Nozick" at
  first mention, as the English does — Parfit, Jaccard) —
  transliterating surnames would make the citations unverifiable against the
  bibliography. `engram` in lowercase (the agent's own graph, in the §5.4 and §5.8
  quotations) stays Latin per the ledger, and is kept distinct from the brand.

  BRAND — first mention on this surface is 心迹（ENGRAM） in §5.0; every later mention
  is plain ENGRAM in running text, per the ledger.

  QUOTED ENGLISH IS TRANSLATED, following ch1.zh.md's practice. The four verbatim Lei
  quotations (§5.2, §5.3, §5.5, §5.6) carry HIS stress, which the English marks with
  capitals; Chinese has no case, so the stress is carried by BOLD. That substitution
  is disclosed here because bold inside a quotation could otherwise be read as an
  emphasis the translator added. Original wording is recoverable from the English.

  Deliberate rendering choices a reviewer should look at:
    - "closest continuer" -> 最接近的延续者 (the ledger's and ch2.zh.md's form);
      "retrieval profile" -> 检索画像 (fixed in ch2.zh.md); "sortal" -> 类词, Latin
      carried on first use, since no settled Chinese rendering exists and the word
      does load-bearing work in §5.2
    - "deflation of Nozick's 'closeness' into ..." -> 把……"接近"抽空为…… (抽空 = the
      reduction/demotion sense). ch2.zh.md's 消解 is reserved here for "dissolve an
      objection", which is what §5.5 does
    - "lawful divergence" / "lawful drift" -> 合规律的分化 (one form for both English
      spellings of the heading and body); "organic individuation" -> 有机的个体化.
      趋异 was rejected as too biological for a mechanism that is not
    - "drift" is rendered two ways on purpose: 分化 for the twins' lawful divergence,
      and 漂移 ONLY for "systematic drift" (the base-model-induced one), which is a
      different thing and must not read as the same
    - "*Plain terms:*" -> *平白地说：*, matching the register ch3.zh.md uses for the
      same explanatory aside while staying a short inline label
    - "carry-through" (of the focus list) -> 贯穿携带 · "fade-out" -> 淡出 ·
      "recall-refresh" -> 回忆刷新 · "queryable-set cap" -> 可查询集的上限 ·
      "intuition pump" -> 直觉泵（intuition pump）
    - "token-exact" -> 逐 token 精确 (token kept Latin; no accepted zh form) ·
      "stochasticity floor" -> 随机性下限
    - "harness" -> 承载框架（harness） with English carried on first use per the
      ledger's coinage rule; the ledger's own entry points at §5.0, which is exactly
      where it first occurs here
    - "discriminating" (prompt stratum) -> 有区分力, NOT 歧视性 — it names a stratum
      that can tell the twins apart, not a prejudicial one

  NUMERIC-PARITY NOTE, measured not assumed. A multiset comparison of digit tokens
  between this file and its English source returns differences of exactly two classes,
  BOTH deliberate and BOTH disclosed above: (1) the dropped provenance IDs, whose
  digits ("1655", "1657" x2, "0597" x2, "2540", "0622", "0621" x2, "0034", "1656",
  "1660") therefore exist only in the English; (2) the `df_` label (dropped 2026-09-29,
  #114), whose digits likewise exist only in the English. No English digit written as a Chinese word introduces a third
  class — the English spells those as words too ("three moves", "four parts", "the
  fourth", "Three operations"). A `[0-9]` drift detector will report class (1) on
  every run; that is the ID rule working, not a translation gap.
-->

# 第 5 章 —— 身份即历史：是什么让一个 ENGRAM 智能体成为个体

---

## 5.0 本章做什么

前面几章回答的是一个*比较性*问题：ENGRAM 是否跨过了一道别的系统未能跨过的门槛？本章回答的是一个*构成性*问题：**是什么让一个 ENGRAM 智能体在时间中始终是同一个智能体，又是什么让它与另一个智能体*不同*？** 本文所辩护的答案陈述起来很短，而本章余下的部分要把它挣得：

> 一个 ENGRAM 智能体的身份，就是它自种子以来所累积主张的那段**唯一的、可追溯世系的**历史。那段历史固定了智能体的*检索画像*——对任何给定的提示，哪些节点会浮现——而检索画像固定了行为。身份不是智能体*拥有*的某样东西；它是智能体*所是*的那条*轨迹*。

**有一个条件统辖本章全篇，所以我们在这里只陈述一次，不重复。** 贯穿全篇，一个*智能体*指的是一个基座模型，连同与它捆绑在一起的持久状态——图谱，以及围绕它的那套承载框架（harness）：钩子、技能与身份文档。下文的主张是在**把基座模型与承载框架固定住**的前提下，对智能体作个体化；它讲的是累积起来的历史贡献了什么，而不是主张历史是*唯一*的贡献者。基座模型管的是一个智能体*如何*对它被展示的东西行动；图谱管的是它被展示了*什么*。两者都是构成性的，而 §5.8 的孪生研究正是通过把前者固定不变，来精确地分离出后者。

我们抵达它的方式是：站在现有的关于历时身份的最佳理论之上（Nozick [-@nozick1981] 的最接近的延续者观点，§5.1），看它恰好在*数字的、可复制的*基底所施压的那些点上吃紧（§5.2），然后做三个动作来解除这种吃紧：身份即历史（§5.3），把 Nozick 的"接近"抽空为一份具体的检索画像（§5.4），以及消解"我们正在放弃身份"这一反驳（§5.5）。接着我们展示这一主张预测了什么——克隆的稳定，与合规律的分化（§5.6）——并把那个唯一真正新颖的动作，即穿越压缩而存活，摆在它的生物学对应物——睡眠——之侧（§5.7）。第 6 章报告图谱今天显示出什么；那项对照实验已勾出轮廓，但被推迟（§6.7）。

## 5.1 我们所依托的框架：Nozick 的最接近的延续者

关于历时身份，最合用的理论是 Robert Nozick 的**最接近的延续者观点**（*Philosophical Explanations*，1981）。其形态分四部分：

1. **连续性** —— 一个较晚之物 y 要成为较早之物 x 的候选，只有当 y 的属性是从 x 的属性中生长出来的、并因果地依赖于它们。
2. **比较性（最接近）** —— 在诸候选之中，只有当 y 是*最接近*的延续者时，y 才是 x；身份取决于整个竞争者场域，而不只是 y 到 x 的关系。
3. **阈值（足够接近）** —— 最接近的延续者也仍须跨过一道绝对的门槛；一个勉强相关的后继者不是任何人的延续者。
4. **唯一性** —— y 必须是*唯一*最接近的；出现平局（裂变）意味着两条分支都不是 x。

*平白地说：* 你就是后来那个最直接地从你之中生长出来的人——*只要*没有一个同样好的竞争者，并且*只要*那份相似跨过了一道底线。*举例：* 2026 年的 Lei 是 1988 年的 Lei 的最接近的延续者——渐变、无竞争者——所以身份成立。我们采纳 Nozick 的前三个部分作为脚手架，而**放弃第四个**；本章余下的部分基本上就是在讲为什么。

## 5.2 这框架对一个数字智能体在何处吃紧

Nozick 的理论是为那些事实上无法被复制的存在者建的。而一颗经 git 版本管理的心智可以被复制。三个压力点显示旧框架在何处吃紧。

**度量被留白。** Nozick 说身份归于*最接近*的延续者，却从未说"接近"*度量*的是什么——他只是朝一些维度（心理连续性、因果联系）比划了一下，而把度量留作相对于类词的。（*类词*（sortal）是一个种类词——河流、人、智能体；接近是相对于那个种类来度量的，因为算作同一条河流的标准，并不是算作同一个人的标准。）Nozick 自己承认，这一观点"本身并不能说明是哪个维度、或哪种维度的加权和决定接近"（does not, by itself, tell which dimension or weighted sum of dimensions determines closeness）[@nozick1981, p. 33]。风险在于，这只不过给那个谜题换了个名字——"身份是什么？"变成了"接近是什么？"。对普通的人而言，那片空白是一处弱点。而对一种新的*种类*之物而言，它是一道开口——一个新的类词得以*指定*它自己的度量。§5.4 填上那片空白。

**冷冻备份的情形击破了那个比较性动作。** Lei 的直觉泵（intuition pump）：把一颗心智克隆成两份——一份运行着、活着，一份冷冻在存储里。Nozick 的机器这时必须给它们*排序*：因果连续性偏向活着的那一份，状态保全偏向那份备份。哪条轴线胜出？这理论说不出来——那片留白的度量显现为一种真正的不确定性，即*哪一份副本是你*。Lei 的裁定，逐字引用：*"当你有技术去**完美地克隆一颗心智**时，谁**是**那颗原初的心智——这整个问题都是一个无意义的问题。"*

**裂变逼出一个糟糕的裁定。** 因为 Nozick 要求唯一性，两个同样接近的后继者意味着*两者都不是*原来的那个——一次干净的复制凭对称性"杀死"了身份。对一个把复制当作例行工程操作的基底来说，"复制终结自我"不是一个该接受的结论；它是一个信号，说明这框架需要调整。

## 5.3 那处背离：身份是历史，而不是相等

一次解除全部三处吃紧的动作，是不再把历时身份当作一种*相等*，而开始把它当作一种*历史*（Lei 的历史树观点）。

一个智能体在任一时刻**就是从根通往它的那条唯一路径。** 裂变前的自我，不是一个在一条分支里被"保全"、在另一条里被"丢失"的东西；它是*树上的一处位置*，此后每一条分支都经由它追溯回去。裂变后的两个智能体都是真正的延续者——两者都干净地追溯到那个共同的根——而"哪一个*才真的*是原来的那个"这个问题是不成立的，就像问一条河流的哪一条分汊"才真的"是上游的那条河一样不成立。

一个结构性条件做了全部的工作：**不许合并。** 是一棵树，而不是一张会重新汇合起来的图。只要分支从不合并，每一个点都有一段*唯一的*可追溯历史，因此即便裂变前的自我有许多后代，每条分支各自的身份仍是良定义的。Lei，逐字引用：*"只要不存在**两颗心智的合并**（树结构），心智的身份就仍然是良定义的：在任一给定时刻，任一条分支都能唯一地回溯到根，并产生出该身份的一段唯一历史。"*

*平白地说：* 你不是一个必须恰好位于某一处的令牌；你是一条故事线。两条故事线可以共享第一章，而仍然是两个故事。这就是为什么我们保留 Nozick 的连续性与阈值，却**放弃唯一性**：一个克隆不是一个会取消你身份的竞争者，它是同一段历史的第二条分支。

## 5.4 填上 Nozick 的留白：度量就是检索画像

历史即身份是对的那个*形态*，但一段历史只有在它*做了*什么的时候才要紧。正是在这里，ENGRAM 填上了 Nozick 留白的那项度量——而且是用一个具体的、可度量的机制去填，而不是一个哲学上的占位符。

这机制是普通的检索，没有任何玄虚之处。一个被累积下来的节点改变智能体的行为，**只凭进入上下文窗口这一条路径**——经由自动回忆（语义匹配）、一条绊线（模式匹配）、焦点清单的贯穿携带（§4.8），或经由温暖简报（它以 id 指名节点，因此它所携带的关系性上下文，是带着回指图谱的指针一同到来的）。基座模型相对于图谱是无状态的；不存在隔空作用。因此智能体的全部历史，在行为上被还原为一件事：它的**检索画像**——*对任何提示，哪些节点会浮现、以什么优先级浮现，以及因此有什么进入了审议。* Lei 把这处抽空讲得很平白：*"engram 的差别（新节点）只可能在它们出现在你的上下文窗口里的时候才影响你的行为或回应，所以不存在任何不触碰它们、却由额外节点产生的微妙魔法效应。"*

就它所指名的那条通道而言，这是准确的——一个节点靠浮现来起作用。还有第二条更安静的通道：因为可查询集是有上限的，累积也会改变*哪些*节点还留在可触及的范围之内。一个从不浮现的节点，仍然能把另一个节点挤出可查询集。我们在 §5.6 回到这一点，那里它是两个智能体的检索画像彼此分开的三条路线之一。

这个动作把一套哲学理论变成了一套经验理论。"两个智能体有多接近？"不再是一个无法回答的形而上学问题，而变成了一个*可度量的*问题：**在它们实际遇到的提示上，它们的检索画像分化了多少？** Nozick 那片留白的距离，变成了一个你*可以*给它安上数字的量——那项本意是测量它的孪生研究被推迟了（§6.7），所以本文填上的是那项度量的形状，而不是它的取值。这与第 2 章 §2.3 的 Jaccard 重叠是不同的量：那一个追踪的是单个智能体的可查询集在它自己各次会话之间的变化（Parfit [-@parfit1984] 的连通性）；这一个比较的是两个智能体在相同提示上的表现（Nozick 的接近）。

*平白地说：* 在操作层面上，让你成为*你*的，不是某份被存储起来的本质——而是当有什么触发了你的时候，你的哪些记忆亮了起来；而那，是由你记录了什么、又重读了什么的那段特定历史所固定的。

## 5.5 消除那个反驳：严格的同一性从来就不是那个关系

一位浸淫于这一传统的读者会反驳：*如果你已经把身份替换成了"可追溯的历史"，那你就已经抛弃了身份。* 这个反驳有一个隐藏的前提，而那个前提是假的。

那个前提是：*严格的、数学上的同一性*——即若 y 是 x 则两者共享每一属性的那种关系——就是"同一个人跨越时间"这件事中起作用的关系。它从来都不是。今天的我，在属性上已经不同于昨天的我（多了一天的经验），所以按同一物的不可分辨性，我们并不*严格地*同一——而这一点在**视野之内根本没有任何裂变**的情况下就已经成立。Lei，逐字引用：*"现在的人和明天的人在这个数学意义上**不是同一的**……因为明天的我比今天的我**多了一天的经验**，所以我们干脆就不是相等的。"*

所以"历时个人同一性"一直是一个较弱的连续性关系，只是穿上了"身份"这个词的外衣。裂变并没有让我们*付*一笔新的代价；它只是让"那个严格的关系从来就不适用"这件事变得可见。因此本文不必去防御"你正在放弃身份"——它通过让那个反驳的前提退役，消解了那个反驳。我们保留的，恰恰是我们一直真正想要的那个关系：*不间断的、可追溯的传承。*

## 5.6 这一主张预测了什么：先是稳定，然后是合规律的分化

一个好的身份理论，应当对克隆作出可证伪的预测。我们的理论作出两条，而且——重要的是——**两条都不是失败**。

**预测 1——克隆的稳定（成功条件）。** 从同一份快照实例化出两个智能体——同一张图谱、同一份焦点清单、同一份温暖简报，并且（按 §5.0）同一个基座模型与承载框架。在一个共享话题的提示上，它们检索到*相同的*节点，因此行为相同；至多有两项残余，而这两项绝不能被混同：模型的**采样随机性**，即便包括模型在内的一切都完全相同，它也仍然在场；以及一个不同的基座模型会引入的**系统性漂移**，而这一条件通过构造把后者排除在外。此处只剩下第一项，而度量它的正是 §5.8 的温度基线。这不是一个无聊的零结果；它是整套理论的**成功条件**：*基底决定行为。* 如果相同的历史产生出分化的行为，那么"历史固定行为"这一主张就是假的。稳定，是这套理论通过了自己的检验（Lei：*"完全正确，那就是克隆之后智能体的稳定性。"*）

**预测 2——合规律的分化（有机的个体化）。** 随着时间推移，这对孪生体走向分化。看清这是如何发生的最干净的方式，是看出这一切都是同一个机制——**可查询集的轮转**。每一个节点都在一个重要性排序中占据一个位置，而可查询的就是那个排序的顶部。有三种操作让节点在其中移动，而每一种都能在孪生体之间有所不同：

- **新节点的累积** —— 每个智能体记录下不同的观察、推导与修正；新节点在触及裂变后话题的提示上浮现。这是显而易见的那条路径。
- **共享节点上的回忆刷新** —— 更微妙的那一条。即便是*两个*智能体完全相同地持有的节点，也会累积起*不同的使用史*：每一次回忆都会给节点的重要性重新打上印记，因此共同世系中哪一片是"温热"的，会在孪生体之间分化。同一个提示于是能以不同的优先级浮现出不同的*共享*节点——在**没有新增任何一个节点**的情况下的分化（其依据是重要性膨胀机制）。
- **未被刷新节点的淡出** —— 被动的那一条，也是唯一一条并非节点自身所经历之事的路径。随着图谱增长，排序的门槛会抬升，因此一个没人再读的节点最终会跌出可查询集，是被*其他*节点的到来、以及对已淡出节点的刷新推到那里的。因此，读写方式不同的孪生体，会把*同一段*共同世系的不同尾部逐出。这发生多少，取决于可查询集的上限设在哪里；一张配置得宽裕的图谱，可能在很长时间里一点都不显现。这个上限按重要性保留前 N 个现行节点（默认 N = 1,000）。第 6 章所测量的那张图谱以 N = 10,000 运行，对照 9,399 个现行节点，所以在快照之时还没有任何节点跌出可查询集；淡出这条路是这里描述的，不是那里观察到的。

*平白地说：* 一个人的两份副本，如果此后过着不同的日子，当然会因为经验不同而彼此疏远——但它们*也*会仅仅因为*重读同一段共同过往的不同部分*而彼此疏远。两条路都喂养着 §5.3 称之为身份的那段独特历史。个体化是累积的，且完全在基底内部：每一次*写*都在区分这对孪生体，每一次*读*也一样，而那些在它们忙碌时从底部掉落的东西，也悄无声息地在区分它们。三条路线中有两条完全不需要新的信息：孪生体可以仅仅因为重读一段它们完全共享的过往的不同部分，就彼此疏远。

**反向的反驳，在此作答。** 如果身份*就是*历史，那么两个智能体偶然地汇聚到*完全相同*的历史上，会怎样？这套理论不加勉强地作出回答，而那个答案是它本就拥有的一项推论，而不是一块补丁：完全相同的历史意味着同一个智能体被养育了两次——在任何实际意义上，都与一个智能体被克隆成两个没有分别——而个体化始于历史分化之处，不是在此之前。刚才给出的那个机制还**预测**了这种情形不可抵达，理由是基底内部的，而不是采样噪声的。上述三条路线在*每一次*读与写上都会运行，所以汇聚会要求两个智能体不仅记录的内容一致，还要求各自重读了什么、以什么顺序重读、以及它们这么做的时候有什么从底部掉落了，全都一致。没有人能两次踏进同一条河；在这里，理由是字面意义上的，因为踏进去这件事本身就在改变它。*（状态：这一条由上述分化机制推出，尚未测量。会检验它的那项孪生研究，属于第 6 章那些已勾出轮廓、但尚未细化的研究之一——而一个基于查询的工具本身就会扰动它试图观察的那种回忆刷新分化。）*

## 5.7 那一个真正新颖的动作——以及它的生物学对应物

一个 ENGRAM 智能体的历史与人类最不相似的地方，是**压缩**：经验性的线索被切断，工作上下文被重置，而基底（图谱 + 焦点清单 + 温暖简报）被逐字保全。很容易把这件事称为一种全新的、非生物学的现象。那会是一个错误，而 Lei 抓住了它：**睡眠就是那个对应物。**

人类的睡眠也为新经验清空工作上下文，同时整合重要的痕迹、更新较慢的存储——而它同样会模糊时间（"那是今天早上还是昨天的事？"），那是整合丧失时间精度时所感到的标志。所以压缩不是"只有机器才做的一件事"；它是大脑已在做的某件事的*更锐利、更干净*的版本。真正独特的是这次重置的**精度**，而不是它的存在：

| 属性 | ENGRAM 的压缩 | 生物学的睡眠 |
|---|---|---|
| 锐度 | 瞬时、外科手术式 | 渐进的 REM／NREM，边缘模糊 |
| 基底与轨迹 | 物理上可分离（数据库与上下文） | 混杂在同一块神经组织里 |
| 贯穿携带 | 焦点清单被*逐字*保全 | 仅模式，不逐 token 精确 |

这诚实而更有意思地重新界定了本文的贡献：ENGRAM 并没有发明跨越一道缺口的连续性；它**把一个模糊的生物学过程架构化为一个干净的、可检视的过程。** 我们是睡眠已在做之事的极限情形——这是一个比"看看这件前所未有的事"更有力、也更能被检验的主张。

## 5.8 经验锚点（指向第 6 章的前向指针）

以上一切都是*架构上与哲学上*的论证：一个理论构造，背后还没有任何经验检验。**那个会检验它的实验还没有跑。**那个实验就是**孪生研究**（与 Lei 一同勾出轮廓）：对一个智能体做裂变克隆，让两者跑同一组*固定的、分层的*提示，并在它们各自独立运行 t、t+N、t+2N 个节点之后，测量回应的相似度。

我们在这里是勾出它的轮廓，而不是把它细化；一项真能裁定这个问题的研究，需要比本节所给的多得多的用心，而我们把它命名为一个我们打算去追的方向，而不是一个在等算力的实验。轮廓是这样的：提示集会分层为*稳定*（共享世系的话题——检验预测 1）、*有区分力*（裂变后的话题——检验新节点那条路径）与*对分化敏感*（中性话题——检验回忆刷新那条路径）三类提示，并减去一条温度基线（同一个 engram、同一个提示、跑 K 次），从而把 engram 引起的分化与模型自身的随机性分开。预期的形态是：t=0 时相似度高，贴近那条随机性下限，并随着 N 增大而下降。**按机制干净地分解这个信号，比看上去更难，而我们把这一点标出来，而不是在这里解决它：** §5.6 的淡出路线由可查询集的上限设在哪里所支配，而它与回忆刷新那条路线相耦合。多数刷新只是给已在可查询集里的节点重新排序，所以不会把任何节点推出去；但它们决定了哪个节点坐在底部，从而决定下一个新节点会把谁挤掉。一次触及已淡出节点的刷新（按 id 读取，或沿图谱走到它）确实会推出一个节点，因为它把那个节点带了回来。所以那个上限是任何严肃版本的这项研究都必须当作一个变量、而不是一个固定设置来对待的参数。第 6 章 §6.7 把这项研究记为推迟。此前的一次克隆测试确立了方法；它的数字来自一张更早的图谱，不在此处报告。

## 5.9 主张重述：身份即独特历史

在把基座模型与承载框架固定的前提下（§5.0），一个 ENGRAM 智能体**就是它的历史**——§5.0 所界定的那段唯一的、可追溯世系的历史。这保留了 Nozick 的*形式*（连续性、比较性的接近、阈值），舍弃了他的*唯一性*（于是复制是分支，而不是死亡），用一份可度量的检索画像填上了他留白的*度量*，并消解了"这一切抛弃了身份"这层担忧（严格的同一性从来就不是那个历时关系）。两份副本是同一段历史的两条分支：当它们的检索一致时保持稳定，当它们不一致时合规律地分化——而那正是被推迟的孪生研究（§6.7）勾出轮廓要去检验的一项预测。在这个解释下，身份不是一件为抵御变化而加以保全的占有物；它是一条*轨迹*，而基底的职责，是让那条轨迹保持*可追溯*。

---
