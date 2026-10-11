<!--
  ZH TRANSLATION — 中文译本
  source file:    paper_research/current_draft/appendix_B_c3_survey.md
  source commit:  6e64802  (engram-paper, 2026-09-28)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper_research/current_draft_zh/appendix_G_glossary.zh.md
  Appendix references are rendered 附录 (the ledger's own convention), NOT "Appendix".
  Section pointers (§B.0, §3.5, §4.4) are kept verbatim — the ledger's pointer grammar
  knows the § form in both languages.

  VERBATIM FAILURE QUOTES ARE KEPT IN ENGLISH — the decision this appendix had to make,
  and the one place its translation can do real damage. The per-system `*paper-verbatim*`
  lines are EVIDENCE: each is the sentence that shows why that system fails Condition 3,
  and a translated quote is no longer the thing it is cited as. So every source quotation
  stays BYTE-IDENTICAL to the English source, and the Chinese reading is carried OUTSIDE
  the quotation, in a full-width parenthetical that follows it: （中文解说：…）. ASCII
  `"` is the visual marker for a verbatim-English span; Chinese prose quotes use curly “ ”.
    THE LINE DRAWN — source quotations stay English; the survey's OWN analysis does not.
    `*first-hand-read finding:*`, `*honest scope:*` and `*first-hand-read note:*` blocks are
    our prose about the source, not quotations from it. The appendix says so itself (§B.2
    GAM: "We cite this as analysis, not as a quote"), and the §B.6 table's "Verbatim
    available?" column marks the same split — GAM reads "resolution-gap = analysis". Those
    blocks are therefore TRANSLATED. The English labels themselves (`*paper-verbatim*`,
    `*first-hand-read finding:*`) are kept verbatim as drafting markers, the way ch3.zh.md
    and ch4.zh.md keep their bracketed tags. Kahl's Condition-3 definition in §B.0 is a
    source quotation and is kept in English for the same reason.
    NOTE the consequence for a reviewer: this file reads partly in English by design, and
    the English half is the half to check against the cited sources.

  NO PROVENANCE NODE IDS. This file carries ZERO `ob_`/`dv_`/… identifiers in its body,
  per the rule stated in render_paper.py above `_LITERAL_STRIPS`: a zh chapter must carry
  NO citation-style provenance IDs at all, and `_LITERAL_STRIPS` is English-only by
  design, so the obligation is the translator's. Three IDs stood in the English source:
    * the `df_` label after Kahl's Condition 3 in §B.0 — DROPPED (2026-09-29, #114: `df_*`
      is citation-style like the rest and is no longer exempted from the render strip).
    * two `dv_` IDs in §B.6 — DROPPED with their parenthetical, the same class of
      citation-style provenance as ch4.zh.md drops. (Written here WITHOUT their four
      digits ON PURPOSE: this header is part of the file the stripper reads, so a literal
      ID in the note above would itself trip `assert_no_leaked_ids` — which is exactly
      what happened on the first draft of this file.)
  This file has NO bracketed apparatus tags (the English source has none — its only two
  square-bracketed spans are an inline elision inside a GAM finding, and the TierMem
  tiering aside, both rendered here as ordinary full-width parentheticals). So
  `strip_apparatus_tags` is a no-op on this file and nothing can leave a stray English
  bracket behind in the body — the two square brackets that remain anywhere in the file
  are both inside THIS header comment, matching ch3.zh.md / ch4.zh.md, whose headers
  carry the same kind of bracketed example.

  BRAND — the paper is ONE surface, so `心迹（ENGRAM）` appears once, in ch0; this appendix
  writes plain `ENGRAM` in running text throughout, per the ledger header and
  docs/ZH-TERMINOLOGY.md.

  Proper nouns stay in Latin script — this appendix is a per-system survey, so the system
  names ARE the content: Kumiho, SCM (Sleep-Consolidated Memory), GAM (Hierarchical
  Graph-based Agentic Memory), Zep / Graphiti, Mem0 v3, MemMachine, Pinecone Nexus,
  Letta / MemGPT, Anthropic Claude memory tool, TierMem, and the 2026 *Memory for
  Autonomous LLM Agents* survey (Du). Author surnames stay Latin (Kahl, Hansson,
  Du); so do the standing names AGM, NREM, REM, Hebbian, and the identifiers
  `Depends_On`, `AnalyzeImpact`, `contradicts`, `contradict`, `memory_rethink`,
  `core_memory_replace`, UPDATE, C3.

  DELIBERATE RENDERING CHOICES a reviewer should look at:
  1. `survey` -> 调查 (the ledger's own entry for the dated first-hand sweep already
     describes it as "带日期的第一手调查"), NOT 普查. The ledger binds 普查 to the English
     lemma `sweep` — and this appendix never writes "sweep" anywhere. ch4.zh.md's own §4.12
     table already ships 调查 for "survey" and names this appendix as "作为记录的 C3 调查",
     so the two surfaces agree.
  2. "Memory survey 2026" -> `Memory survey 2026` (kept English) in the §B.6 table and in
     the §B.5 heading, because ch4.zh.md's §4.12 table already renders the same system that
     way and the ledger forbids a chapter inventing its own rendering. The §B.0 list keeps
     the paper title in English italics as *Memory for Autonomous LLM Agents*.
  3. "Appendix E.1" in §B.2's GAM bullet refers to **GAM's own** appendix, not ours — and
     this paper's 附录 E is the techspec, so a bare 附录 E.1 there would actively mislead.
     It is rendered 源论文的附录 E.1. The `§` pointers in the same bullets are left bare
     (unlike the appendix number, a §3.5 or §9.3 cannot be confused with our numbering
     without also ignoring §B.0's standing note, which this file translates).
  4. "One precision" (§B.6's closing note) -> 一处精确化, and the §B.0 forward reference to
     it uses the same words.
  5. `consolidation cycle` -> 整理周期 (routine sense, per the ledger's 小憩 / 睡眠 entries),
     NOT 整合周期 — this file takes no side on the header's still-OPEN 整合/整理 split
     beyond using the routine sense where the English means the routine.
  6. `sweep` does occur once in this file's own prose, in §B.6's "consolidation cycle"
     sense — rendered 普查 only where the English word is sweep. It is not used here.

  NUMERIC-PARITY NOTE, measured not assumed. A multiset comparison of digit tokens between
  this file and its English source returns differences in ONE direction only, and every one
  of them is a NODE-ID FRAGMENT: the four digits of each of the three IDs this file was
  required to drop — the `df_` label in §B.0 and the two `dv_` IDs whose parenthetical
  §B.6 required this file to drop (§4.4's operational-binding citation). Three digit
  tokens in all, measured on the bodies with this header excluded.
  The zh side introduces NO extra digit token — every number in the English is carried as a
  digit here, including the ones Chinese could have written as words (十一项来源 / 十个系统 /
  四种不合格的方式 / 两次 / 三部分 / 两半 — these spell out words that are ALSO words in
  English, so neither side gains a digit token). Any drift-detector built on `[0-9]` runs
  must whitelist the ID-fragment class, or it will report three false errors per run.
-->

# 附录 B —— 条件 3 调查：为什么受调查的系统中没有一个自我维持仲裁

## B.0 范围、日期与方法

**这份调查。** 十一项来源——十个系统，外加一篇对本领域的综述——于 **2026-05-12** 第一手读完：Pinecone Nexus[@ashutosh2026]、Anthropic 的 memory tool[@claudedocs2026]、Letta（MemGPT）[@lettaai2026; @packer2023]、Mem0 v3[@memzero2026a; @memzero2026b]、Zep/Graphiti[@rasmussen2025]、TierMem[@zhu2026]、MemMachine[@wang2026a]、SCM、GAM、Kumiho，以及 2026 年的 *Memory for Autonomous LLM Agents* 调查[@du2026]。这是一条**关于该受调查集合、以该日期为界的受限主张。** 智能体记忆是一个快速变动的领域；我们对调查之外的、或调查之后发布的系统不作主张。较新的或遗漏的系统，恰恰是这条主张被限定范围、标注日期并逐一列出、而非普遍化的原因。

**那条标尺。** Kahl 的**条件 3——自我维持的仲裁**，逐字："Conflicts among commitments are resolved within a unified deliberative architecture in a manner that preserves S's continued status as that subject."（中文解说：诸承诺之间的冲突，在一个统一的审议架构之内得到解决，其方式保全 S 作为那个主体的持续身份。）[@kahl2026b, p. 10]就操作性而言，一个系统只有在它**把自身所存储诸主张之间的矛盾作为一次内部状态变更来自动解决**时，才算满足 C3（下文"一处精确化"那条注解说明了"解决"意味着什么、不意味着什么）——级联依构造而传播，而受影响的主张不依赖任何有意的触及就浮现到智能体面前。四种不合格的方式：

- **（N）无解决** —— 矛盾作为一个构造缺位，或虽被检出却从不被解决（那些边／标志持续存在）。
- **（A）咨询性／选择加入** —— 存在一个解决机制，但必须被显式调用，而且它只建议、不撤回。
- **（X）外部委托** —— 解决被交给检索排序、近因规则或应用代码，处在审议架构之外。
- **（S）无主张结构** —— 系统在文本块上运作，没有任何可供级联穿行的东西。

**诚实定界的注解。** 当某个系统的 C3 失败是由一项*正面*的设计选择所显示时（委托给检索、按近因覆盖、只建议不撤回），我们逐字引用它。当来源记录了检出、却对解决保持沉默（GAM）时，没有句子可引——我们如实说明这一点，并把判定建立在有记录可查的缺位之上，而不是一句编造出来的引文上。

**综合。** 在全部十一项来源中，没有一个严格满足条件 3；其中一项，TierMem，没有可供仲裁的矛盾构造（§B.5）。这个结论是以上诸判定的合取，因此它的成立范围，恰好与其中每一项的成立范围一样远。本领域已经在 C3 所需要的那些结构性*原语*上趋同（带类型的边、出处、可级联遍历的图谱、取代语义——以 Kumiho 最为完整）；各处所缺的，是那个使仲裁成为自动状态变更的**操作性绑定**。ENGRAM 的贡献是那个绑定（第 4 章 §4.4），而不是那些原语。

*paper-verbatim* 与 *paper-claimed* 标记之内的章节号，指的是被引论文自己的章节，而不是本文的章节。

---

## B.1 一次险失：一台完整的修订引擎，却是咨询性的

### Kumiho（arXiv 2603.17244）—— **（A）咨询性／选择加入**
本次调查中最强的竞争者：带类型的 `Depends_On` 边、一次 `AnalyzeImpact` 遍历，以及*自称的* AGM K\*2–K\*6 与 Hansson 信念库符合性。缺口不在于信念修订——而在于这次级联**建议**，而不是**行动**。

**那项符合性主张是他们的，我们按其能被我们担保的保真度记录。** 上文那些 AGM 与 Hansson 性质，是 Kumiho 关于 Kumiho 自己的主张，而它的论文分两部分提出它们——一个形式化部分，"proving satisfaction of the basic AGM postulates (K\*2–K\*6) and Hansson's belief base postulates (Relevance, Core-Retainment)"（中文解说：证明对基本 AGM 公设与 Hansson 信念库公设（Relevance、Core-Retainment）的满足）[@park2026, p. 1]，以及一个实现部分，"Automated AGM compliance testing (49 scenarios, 7 postulates) confirms 100% operational adherence to the claimed formal properties."（中文解说：自动化 AGM 符合性测试确认对所声称形式化性质的运行符合度。）[@park2026, p. 2]这个结构是审慎的，而不是混乱的：证明是为语义提供的，场景是为运行中的系统提供的。**这两半我们都担保不了。** 我们读过他们的论文；我们没有逐步演算他们的证明，也无从接触他们的实现来重跑任何东西——而 49 个通过的场景无论如何只能确立"在 49 个案例中没有找到反例"，而不是"不存在反例"。所以我们把这项符合性记为*自称的*，而不是已确立的，并把它搁置不予裁定：本次调查中没有任何东西取决于它，因为这里所画的对照关乎**一处更正从哪里开始约束**，而不关乎谁的诸公设被满足。（关于为什么"满足"是*本文*不应就自身加以主张的那种关系，见第 3 章 §3.9。）

- *paper-verbatim*（§6.5）："AnalyzeImpact traverses typed Depends_On edges to identify all downstream conclusions that **may need re-evaluation**—a capability enabled by the typed edge ontology that flat file systems cannot express."（中文解说：AnalyzeImpact 遍历带类型的 Depends_On 边，找出所有**可能需要重新评估**的下游结论——这是带类型边本体论所支撑的能力，扁平文件系统无法表达。）
- *paper-verbatim*（边定义）："**Depends_On**: Validity dependency. If the target is invalidated, the source **may be** unreliable."（中文解说：Depends_On：有效性依赖。若目标被作废，源**可能**不可靠。）括号里那个情态词 *may be* 正是咨询性的破绽——它不是 *is invalidated*。
- *paper-verbatim*（§7.1，一致性强制）："deprecated items are excluded from all search and retrieval operations by default"（中文解说：被弃用的条目默认被排除在全部搜索与检索操作之外）——也就是说，一致性是在**检索面**上维持的，而不是通过对承诺的结构性仲裁。
- *first-hand-read finding:* 这次级联是咨询性的，而不是自动的——`AnalyzeImpact` *identifies*（识别出）受影响的信念，但并不撤回它们；必须由人或智能体来审阅并决定是否修订。**把这个缺口表述为"咨询性对自动性"，而不是"没有信念修订"**——Kumiho 拥有那套修订机制；它扣住的是自动的那一层绑定。

---

## B.2 检出而不解决

### SCM —— Sleep-Consolidated Memory（arXiv 2604.20943）—— **（N）无解决**
拥有一个 `contradicts` 边谓词和一个睡眠周期，但那个解决是被许诺的，而不是被实现的：§3.2 说被"flagged for resolution"（标记以待解决）的那些边，在 §3.5 中只被当作一个**触发指标**来用。

- *paper-verbatim*（§3.2）："when a user states a preference that contradicts a previously stored preference, the system records a contradicts edge and **flags the conflict for resolution during sleep**."（中文解说：当用户陈述一项与此前存储的偏好相矛盾的偏好时，系统记录一条 contradicts 边，并**把该冲突标记为在睡眠期间解决**。）
- *paper-verbatim*（§3.5）："Conflict density is the ratio of contradicts edges to total edges in the long-term memory graph: ρ(G) = |E_contradicts|/|E|."（中文解说：冲突密度是长期记忆图谱中 contradicts 边与全部边数之比。）
- *paper-verbatim*（§3.5）：睡眠周期"implementing three distinct offline processes"（中文解说：实现三种不同的离线过程）—— NREM 巩固（Hebbian 增强加按比例降尺度）、REM 做梦（随机游走序列整合），以及基于价值的遗忘——以一台状态机（Figure 2）呈现，并附"the full pseudocode given in Algorithm 1."（中文解说：给出了完整伪代码。）
- *first-hand-read finding, from the paper alone:* **所述三个阶段中没有任何一个作用于一条 `contradicts` 边。** 这些边在睡眠周期中只出现在那个触发指标 ρ(G) 之内，然后就持续存在。这个发现在整篇文档的层面可核验：字符串 *resolution* 在 SCM 论文中出现**两次**——一次在上文所引 §3.2 的许诺中，一次在未来工作里，把"contradictory information resolution"列在更严苛的评估应当检验的能力之中。它不出现在 §3.5、§3.6 或 Algorithm 1 中的任何一处。因为 SCM 公布了它睡眠周期的完整状态机与伪代码，这个缺位*在该论文自己的叙述之内*就可见，无需对 SCM 的代码作任何主张。SCM 拥有结构性冲突处理的外表，却没有其实质：没有仲裁结果，没有级联，没有下游污染。

### GAM —— Hierarchical Graph-based Agentic Memory（arXiv 2604.12285）—— **（N）仅检出**
在巩固时赋予一条 `contradict` 边，但两个相冲突的节点都持续存在，没有任何东西进行仲裁；冲突是被*时序*管理的，而不是被解决的。

- *paper-verbatim*（源论文的附录 E.1，关系评分提示词）："**contradict**: one memory contradicts the other (asymmetric)"（中文解说：contradict：一条记忆与另一条相矛盾（非对称））——检出作为一种带类型的关系而存在。
- *honest scope:* **没有一句论文原话陈述 GAM 不解决**——C3 的失败是由一条仅检出的边的*存在*，加上任何解决性文字的*缺位*共同显示的。第一手阅读发现：两个节点都留在记忆里；检索排序隐含地偏袒置信度更高的信息，但没有任何冲突解决机制被记录。没有仲裁，没有自动撤回，没有级联。我们把它作为分析引用，而不是作为引文。

### Zep / Graphiti[@rasmussen2025] —— **（N）矛盾不持久保存，无级联**
矛盾是摄取期间做出的一次 LLM 分类，它使被直接矛盾的那些边作废；没有任何矛盾节点持续存在，而实体边不能引用其他边，因此没有任何可供级联穿行的东西。

- *paper-verbatim*（§2.2.3）："The system employs an LLM to compare new edges against semantically related existing edges to identify potential contradictions. When the system identifies temporally overlapping contradictions, it invalidates the affected edges by setting their t_invalid to the t_valid of the invalidating edge."（中文解说：系统用一个 LLM 把新边与此前语义相关的既有边作比较，以找出潜在矛盾。当系统识别出时间上重叠的矛盾时，它把受影响边的 t_invalid 设为那条作废边的 t_valid，从而使其作废。）
- *first-hand-read finding:* 作废只作用于被直接矛盾的那些边，且只由*新到达的*情节触发；一个智能体无法检视自己的信念、找到一处矛盾，并传播一次撤回。这次矛盾"not persisted as a node, not persisted as an edge type, and not queryable after ingestion"（中文解说：不作为节点持续存在，不作为边类型持续存在，且摄取之后不可查询）。

---

## B.3 靠覆盖、或靠别人来解决（外部委托）

### Mem0 v3（docs.mem0.ai migration guide，截至 2026-05-12）[@memzero2026a] —— **（X）外部委托**
本次调查中最清楚的外部委托证据。v3 是只增的；矛盾共存，并在读取时被理清。

- *paper-verbatim*："Retrieval handles ranking — the most relevant, current information surfaces first."（中文解说：检索负责排序——最相关、最新的信息最先浮现。）[@memzero2026a, step 4 Tip, Internet Archive snapshot of 2026-05-14]
- *first-hand-read finding:* 冲突解决被委托给检索时的排序，并最终委托给应用代码——这"恰恰是 Kahl 的条件 3 所排除的：外部规定，而不是自我维持的仲裁。"

### MemMachine[@wang2026a] —— **（X）最新状态更新**
系统把被矛盾的画像数据更新为最新状态；没有矛盾记录，也没有从旧事实级联到建立在它之上的那些情节记录。

- *paper-verbatim*："When new information contradicts existing profile data, the system can **update the profile to reflect the most recent state**—supporting the knowledge update capability evaluated in benchmarks such as LongMemEval [7]."（中文解说：当新信息与既有画像数据相矛盾时，系统可以**更新画像以反映最新状态**——这支撑了诸如 LongMemEval [7] 之类的基准中所评估的知识更新能力。）[@wang2026a, sec. 4.7, p. 6]（强调为引者所加）
- *first-hand-read finding:* 当新信息与画像事实矛盾时，画像被更新为最新状态——没有一等矛盾节点，也没有从一处被更正的画像事实，级联到使用旧事实生成的那些情节记录。

### Pinecone Nexus（Pinecone 架构博客）[@ashutosh2026] —— **（X）／（N），且是只读消费者**
"Deterministic conflict resolution"（确定性冲突解决）只出现一次，是知识编译一侧的一个无文档的功能清单条目；而消费端的智能体根本没有承诺图谱。

- *paper-verbatim*（功能枚举）："...Typed fields. Per-field citations with confidence levels. **Deterministic conflict resolution.** Output shaped exactly as the agent specified..."（中文解说：……带类型的字段。按字段的引用并附置信度。**确定性冲突解决。** 输出完全按智能体所指定的形态……）[@ashutosh2026, sec. Introducing Pinecone Nexus]（强调为引者所加）—— 第一手阅读注记：这是"the only location in the primary sources where 'deterministic conflict resolution' appears... a list item in a feature enumeration, with no further elaboration. The mechanism is not defined anywhere in the primary sources."（中文解说：一线来源中唯一出现"确定性冲突解决"的地方……一个功能枚举里的清单条目，再无进一步展开。该机制在一线来源中任何地方都没有被定义。）
- *first-hand-read finding:* 从消费端智能体的视角看，Nexus 里根本没有任何仲裁架构。智能体查询并接收结果；它不维护承诺图谱，也不检测所接收的内容何时与此前的承诺相矛盾。

---

## B.4 没有可供级联穿行的主张结构

### Letta / MemGPT（GitHub + letta.com 文档）[@lettaai2026; @letta2025] —— **（S）文本块**
记忆块就是字符串；编辑在原位覆盖；没有推导图谱。

- *paper-verbatim*（letta.com/blog/memory-blocks）："memory block values are just strings."（中文解说：记忆块的值就是字符串。）[@letta2025] *paper-verbatim*（GitHub `base.py`）："The `memory_rethink` command allows you to completely rewrite the contents of a memory block."（中文解说：`memory_rethink` 命令允许你完全重写一个记忆块的内容。）[@lettaai2026]
- *first-hand-read finding:* Letta 没有推导图谱，没有下游承诺的概念，也没有撤回原语。当 `core_memory_replace` 覆盖一项根基性的主张时，下游没有任何东西被标记。

### Anthropic Claude memory tool（platform.claude.com 文档）[@claudedocs2026] —— **（S）手工维持一致性**
扁平的、自由形态的文本文件；一致性被委托给智能体每个会话的人工努力。

- *paper-verbatim*："Note: when editing your memory folder, always try to keep its content up-to-date, **coherent** and organized. You can rename or delete files that are no longer relevant. Do not create new files unless necessary."（中文解说：注意：编辑你的 memory 文件夹时，始终尽量让内容保持最新、**连贯**且有组织。你可以重命名或删除不再相关的文件。除非必要，不要创建新文件。）[@claudedocs2026, sec. Prompting guidance]（强调为引者所加）—— 这是开发者注入的一条*指令*，要求手工维持一致性，而不是一个结构性机制。
- *first-hand-read finding:* 没有任何机制用来检测一个记忆文件何时与另一个记忆文件相矛盾。也没有任何机制用来找出哪些结论依赖于一项被撤回的前提。

---

## B.5 那份愿望，与真正的缺位

### Memory survey 2026 —— Du[@du2026] —— **（N）被指认，未被解决**
它是一篇综述，而不是一个系统：它把矛盾处理指名为稳健系统*需要*的东西，却没有引用任何一个做到了这一点的系统，并且只提出*外部的*修补。

- *paper-verbatim*（§7.3）："Robust systems need temporal versioning (prefer the newest record), source attribution (user statement > agent inference), **contradiction detection (flag conflicts for resolution)**, and periodic consolidation..."（中文解说：稳健系统需要时间版本管理（偏好最新记录）、来源归属（用户陈述 > 智能体推断）、**矛盾检出（把冲突标记出来以待解决）**，以及周期性巩固……）[@du2026, sec. 7.3, p. 9]（强调为引者所加）—— 这是*规范性的*（"need"／需要），而不是描述性的（"do"／做到了）。
- *paper-verbatim*（他们的 §9.3）："Future systems need external validation... uncertainty quantification... adversarial probing... and expiration policies"（中文解说：未来的系统需要外部验证……不确定性量化……对抗性探测……以及过期策略）—— 所提出的修补全是**外部**干预，而不是结构性原语。这篇综述指出了 C3 问题，却引用了零个解决方案。

### TierMem[@zhu2026] —— **（N）矛盾不是构造，无级联**
TierMem 的写回有一个名为 Conflict Retrieval 的步骤，但它只检索与新事实最相似的既有摘要单元；随后一个 LLM 记忆管理器在 SKIP（该事实已被蕴含）、UPDATE（为一条含糊的条目补充细节；合并后的文本继承出处）与 ADD（一个不同的事件）之中选择（该页称管理器输出“四种动作之一”，但只列出这三种）。所列步骤中没有任何一步检出或解决矛盾，也没有任何东西标记或回访下游的主张[@zhu2026, App. A.6, p. 12]。第一手阅读发现：没有任何根基性撤回的标记机制存在。当一份第 1 层摘要被 UPDATE 时（此处所说的分层是 TierMem 自己的分层，与第 4 章 §4.5 的分层无关），没有级联通往依赖它的摘要，也没有级联通往旧内容的下游用途。判定：C3 未被满足——在所描述的步骤中，矛盾作为构造是缺位的；"conflict"一词所指称的是一个检索步骤。

---

## B.6 小结

| 系统 | C3 失败模式 | 有逐字引文可用？ |
|---|---|---|
| Kumiho | **咨询性／选择加入**（修订存在，但不自动） | 有（AnalyzeImpact、Depends_On 的 "may be"） |
| SCM | 无解决（愿望性的标志，仅触发） | 有（§3.2 对 §3.5） |
| GAM | 仅检出（无解决性文字） | 部分——`contradict` 边有；解决缺口＝分析 |
| Zep/Graphiti | 使被直接矛盾的边作废；无级联 | 有（§2.2.3） |
| Mem0 v3 | 外部委托（检索排序） | 有——本次调查中最清楚的 |
| MemMachine | 外部委托（最新状态更新） | 有（"most recent state"） |
| Pinecone Nexus | 外部／无文档；只读消费者 | 有（清单条目）+ 分析 |
| Letta | 无主张结构（字符串） | 有（"just strings"） |
| Anthropic memory tool | 无主张结构（手工维持一致性） | 有（"keep... coherent"） |
| Memory survey 2026 | 被指名为愿望，无实现 | 有（他们的 §7.3、§9.3） |
| TierMem | 矛盾不是构造；无级联 | 无引文 |

在受调查的整个集合上，模式是一致的：本领域拥有那些*原语*（检出、带类型的边，甚至 Kumiho 自称的形式化 AGM 符合性），却止步于**作为内部状态变更的自动仲裁**之前。把 ENGRAM 区分开来的，是操作性绑定（第 4 章 §4.4），而它由**三**部分组成，不是两部分：级联不经请求就标记每一个受影响的节点；自动浮现把这些标记放回智能体面前，不依赖任何有意的触及；而**级联机在睡眠期间把被标记的那片区域推向裁定**——按依赖顺序走那条前沿，直到不剩任何待决标记，作为每一个整理周期的强制阶段。

第三部分，正是与那个最接近的竞争者对照最鲜明的地方，而它值得直白地说出来，因为这两个系统*在架构中的同一个位置*上失败与成功。SCM 的睡眠周期是被冲突密度**触发的**，且不解决冲突；ENGRAM 的睡眠周期则**是解决发生的地方**。两个系统都伸手去够同一个生物学类比，都把冲突处理放进离线阶段；但只有其中一个在那里合上了这个环。

一处精确化，因为在这里过度主张，恰恰会重犯这个附录指控别人的那个错误：ENGRAM 这台机器并不判定什么是*真*。它找出什么需要被决定，给这些决定排序，使其中没有任何一个依赖着仍未落定的前提，把能算的算出来，并把每一个剩下的判断交给智能体。这条主张是：没有任何受影响的节点会安静地不被检视——而不是：仲裁在没有心智参与的情况下发生。
