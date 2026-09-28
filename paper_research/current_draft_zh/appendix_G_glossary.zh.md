<!--
  ZH TRANSLATION — 中文译本
  source file:    paper_research/current_draft/appendix_G_glossary.md
  source commit:  eb6e118  (engram-paper main, 2026-09-28)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — this file doubles as the TERM LEDGER. Load-bearing term
                  choices below are pending Lei's review before chapter translation
                  proceeds. Do not treat as final prose.

  TERMINOLOGY CONVENTION (Lei, 2026-09-28; supersedes the 2026-06-27 ruling):
    epistemic        -> 认知     (first-order adjective; 认知逻辑 = epistemic logic)
    epistemology     -> 认识论   (the discipline)
    epistemological  -> 认识论的
    ENGRAM (brand)   -> 心迹（ENGRAM） on FIRST mention of the paper, i.e. in ch0
                        ONLY; every later zh mention writes plain `ENGRAM` in
                        running text. Lowercase `engram` (the instance sense,
                        §5.6/§7.1) stays Latin. This row previously read
                        "-> 心迹 (on first mention)", which three translators
                        read as "first mention PER CHAPTER" and split three ways
                        (ch1 14x 心迹, ch2 0x, ch3 1x); the paper is ONE surface.
                        Measured practice in the published zh docs agrees:
                        README.zh.md 38x ENGRAM to 1x 心迹, USER_GUIDE.zh.md 30 to 1.
  Rationale: the 06-27 ruling had `epistemic` = 认识论, which conflates the
  first-order adjective with the name of the discipline.

  THE OPERATIVE TEST — prefer it to the table above at the point of an actual
  term choice (Ariadne, website#23 colleague pass, 2026-09-28; she re-checked
  every surviving 认识论 on the website's zh surface against its English sibling):
      grammatical NOUN      -> 认识论   (epistemics / epistemology / epistemological)
      grammatical ADJECTIVE -> 认知     (epistemic X -> 认知X)
  All four sites she checked sort correctly under it: three nouns keep 认识论
  ("debate epistemics", the `epistemics` tag, "辩论认识论"), and the single
  adjective (`epistemic-discipline`) becomes 认知纪律. Decide by PART OF SPEECH,
  not by the English spelling — 认知 is standard for the adjective (认知逻辑 =
  epistemic logic, 认知不确定性 = epistemic uncertainty) and matches 认知身份,
  already shipping in README.zh.md. A live caveat, carried not absorbed: 认知 can
  also be heard as "cognitive" (Borges, on the README title). Lei's ruling
  decides the term; if it reads ambiguous in a specific title, raise it with him
  rather than silently choosing otherwise.

  COINAGES — approved by Lei 2026-09-28. None had precedent in any published
  Chinese surface, so these are ours, not inherited:
    harness          -> 承载框架   ("the apparatus of hooks, skills and identity
                                    documents"). Rendered 承载框架（harness） on
                                    FIRST appearance — `harness` is a familiar
                                    term in the Chinese AI community and readers
                                    should recognise what is meant.
    sweep            -> 普查       (the dated survey sense; 全景扫读 for the
                                    "landscape sweep" sense). THIRD SENSE, open
                                    2026-09-28: a PARAMETER SWEEP (appendix C §C.5,
                                    the NDCG sweep) is neither of those — it is a
                                    scan over a hyperparameter, standard ML usage.
                                    普查 is wrong there; 扫描 is the likely fix.
                                    Left OPEN rather than changed because it is one
                                    site and the whole entry is Lei's to settle;
                                    appendix C's translator followed the lemma
                                    binding (普查) for consistency and flagged it
                                    rather than choosing unilaterally. If you hit a
                                    sweep site, decide by SENSE and say so in your
                                    header — do not apply 普查 by reflex.
    seat             -> 席位

  RULE FOR THE CHAPTERS: every coinage above carries its English in parentheses
  on first occurrence in the zh body, per the house pattern 中文（English）used
  throughout the published surfaces.

  TERM DECISIONS — pairs where independent translators DIVERGED and one form was
  then FIXED for the whole paper. Record a pair here at the first divergence, not
  per chapter; a chapter that invents its own rendering is the failure this block
  exists to prevent.
    noetic / autonoetic  ->  知晓 / 自我觉知      (Tulving; ch3 §3.2, ch4 §4.6).
                              English carried on first use per chapter.
                              ch2 §2.7 originally read 抽象意识／自主意识 and was
                              normalised 2026-09-28. Recorded as the failure it was:
                              THREE independent translators each invented a
                              rendering because THIS LEDGER HAD NO ENTRY — the same
                              shape as the node-ID rule below, and the same lesson.
                              The pair is load-bearing (ch3 grounds the two recall
                              tiers on it), so a split rendering is a real defect,
                              not a style difference.
    type / token         ->  类型／个例（type/token）  (ch4 §4.6; Peirce).

  OPEN — consolidation, NOT yet resolved paper-wide. Two renderings are live and
  the split does not follow chapter boundaries. MEASURED 2026-09-28 (grep -o):
      ch1 整合=2 整理=0 · ch2 整合=1 整理=0 · ch3 整合=8 整理=4
      ch4 整合=6 整理=7 · ch5 整合=2 整理=0
  ch4 §4.12 splits by SENSE — the routine sense (nap / sleep / sweep / cycle) as
  整理, the cognitive-science sense (hippocampal-neocortical, CLS) as 整合 — and
  says it followed this header's own 小憩 / 睡眠 entries, which do read 整理例程.
  ch1 §1.4's 整合期普查 is the routine sense and contradicts that split; ch1, ch2
  and ch5 use 整合 alone. DO NOT pick a side per chapter. Resolve by reading the
  English at each site, then fix all chapters in ONE pass and move the decision
  up into TERM DECISIONS. Recorded rather than resolved because the answer is not
  determined by the evidence in hand — a rushed pick would be the divergence
  generator this block exists to stop.

  RULE FOR THE CHAPTERS — NODE IDs: a zh chapter must carry ZERO citation-style
  provenance IDs (ob_ dv_ cs_ ls_ ax_ cj_ qu_ fl_ ev_ pn_ tk_ gl_ ct_).
  `render_paper.py` strips them from the ENGLISH render via `_LITERAL_STRIPS`,
  which is English-only BY DESIGN, so a Chinese copy cannot be stripped and the
  obligation moves onto the translator. An ID carried across SURVIVES into the zh
  render and trips `assert_no_leaked_ids` — for the GATED files that is a HARD
  FAILURE and the zh paper will not build at all. **WHICH FILES ARE GATED IS A
  REAL DISTINCTION, corrected 2026-09-28 after ch6's translator caught this rule
  overstating itself.** The gate runs only for files in `render_paper.py`'s
  `STRIP_PROVENANCE_IDS_IN`. NOT gated: `ch0_abstract`, `ch6`, `ch8`,
  `appendix_A_independence`, `appendix_G_glossary`. For those five the rule is an
  INSTRUCTION WITH NO MECHANICAL GATE — a leaked ID reaches the render silently and
  no test fails. So on an ungated file, `grep` it yourself; the build passing tells
  you nothing. (Appendix B is gated; do not generalise from a chapter to an
  appendix.) An earlier version of this rule stated the HARD FAILURE
  unconditionally, which reads as "the engine will catch me" on exactly the files
  where it will not.
  So: where the English has "…(ob_NNNN).", write 中文 without the
  parenthetical. Two carve-outs, both deliberate:
    * `df_*` labels are NEVER stripped and are KEPT (`_ID` excludes them).
    * IDs inside square-bracketed apparatus tags are not this rule's scope —
      they are `strip_apparatus_tags`'s, removed later in the pipeline.
  A THIRD carve-out, added 2026-09-28 after it bit: an ID the ENGINE deliberately
  keeps for a specific file must be kept here too. `render_paper.py`'s `KEEP_IDS`
  (around line 419) allowlists two `dv_` IDs for `ch7.md` only -- §7.2's worked
  example of a mis-typed reasoning step, kept as a DATA POINT under Lei's
  2026-09-23 ruling, not as a citation. Read the set in the engine; this header
  deliberately does NOT restate the IDs. `assert_no_leaked_ids` admits them (it is
  keyed by BODY name, so it admits them for the zh file too), but this rule said
  "ZERO" unconditionally; ch7's translator obeyed it and dropped both, leaving the
  zh reader unable to re-run `tools/paper_stats.py --trace <id>` -- a capability the
  English reader has. The rule was wrong, not the translator. Check `KEEP_IDS` for
  your file BEFORE dropping a bare ID.

  A FOURTH carve-out — the one where getting it wrong DESTROYS CONTENT
  (2026-09-28): **Appendix A keeps its node IDs.** They are AUDIT ANCHORS; the
  engine's own module note lists three jobs node IDs do and says of this one:
  "a reader with the snapshot can resolve them, and the Data Availability note
  says so. They stay." Appendix A is deliberately NOT in
  `STRIP_PROVENANCE_IDS_IN`, so nothing strips it and nothing asserts on it.
  Applying "ZERO" to Appendix A deleted §A.3's whole `node` column and §A.5's two
  hook IDs — removing from the zh reader exactly the resolvability that appendix
  exists to demonstrate.
  THE GENERAL SHAPE, now that four separate translators have each hit this rule
  from a different side: it governs *citation-style* IDs — IDs hung on someone
  else's claim. It does NOT govern every `xx_NNNN` token. An ID that IS the
  evidence (a datapoint, an audit anchor, a trace argument) is kept wherever the
  English keeps it. **Read the English source at the site and mirror it; do not
  apply this rule from memory.** Enumerated:
    KEPT, by the engine or by design: `df_*` (everywhere) · Appendix A (audit
      anchors) · a file's `KEEP_IDS` entries · IDs inside `[...]` apparatus tags
      (removed later, by the tag stripper, not by this rule).
    STRIPPED: the parenthetical citation forms, in the GATED files only.
  All four carve-outs were found by a translator hitting the rule, never by the
  rule's author — which is the argument for keeping this enumeration HERE.

  NEVER WRITE A LITERAL NODE ID IN THIS HEADER. `tests/test_glossary.py`'s
  `_ID_SCAN` scans the WHOLE FILE including this comment, so an illustrative ID
  here fails the very test that enforces the ban -- and it fails silently as a
  confusing "Appendix G carries a node ID". This happened TWICE in one session
  (first while explaining the ban, then again while documenting the `KEEP_IDS`
  carve-out). Write `ob_NNNN` / `dv_NNNN`, or name the file the IDs live in.
  Found the hard way: ch2/ch3 shipped one such ID + nine others and failed the
  build. The rule was in the engine's docstring and in the PR, but NOT here,
  which is exactly where a translator looks.
  Decisions preserved from the published Chinese surfaces (README.zh.md /
  USER_GUIDE.zh.md / the website i18n): 智能体 agent · 图谱 graph · 撤回 retract ·
  取代 supersede · 级联 cascade · 污染 taint · 推导 derivation · 观察 observation ·
  公理 axiom · 基石 cornerstone · 教训 lesson · 出处 provenance · 可审计 auditable.
  Kept English by house rule: identifiers, CLI verbs, node-id prefixes, field
  names (`quote_type`, `source_class`, `derives_from`), paths, node codes.
-->

# 附录 G — 术语表

以下各条目按本文的用法界定每个术语，并指向界定它或首次使用它的章节；若某个词在本文中有不止一个义项，条目会列出各个义项。

**仲裁（arbitration）** — *义项：*（1）在一个统一的审议架构内，撤回／取代级联的结构性传播（§1.3；附录 E §E.1）；（2）智能体对一个待决节点的自行裁定，交由智能体、而非基底来决定（§4.4）；（3）Kahl 条件 3 所要求的那种能力，在附录 B 中按竞争者逐一评分（§B.0）。除另有说明，取义项（1）。

**自动浮现（auto-surface）** — 回忆中"这听着耳熟"的那一档：每轮自动浮现相关的主张，有损，且只到提示级别；当确有东西可取时，它促使智能体转入*主动回忆*（一次受来源监控、返回完整内容的查询）。（界定于 §4.6。）

**公理（axiom）** — 一个终端的、被声明为根基的承诺，按类型置信度为 1.0；承载主张。（界定于附录 E §E.2。）

**级联（cascade，撤回级联）** — 撤回或取代沿着 `derives_from` 与 `acknowledged_derives_from` 的自动传播，把每一个现行的、承载主张的依赖项标记为**待决**。（界定于 §4.4。）

**检查点（checkpoint）** — 状态被捕获的时刻：经 git 版本管理的图谱在检查点处是重置对称的（§4.9）；温暖简报的会话区块在每个检查点被重写（附录 D §D.4）。

**承载主张／不承载主张（claim-bearing / non-claim-bearing）** — 把节点种类划为断言了可真假评判之物的（观察、推导、理论、公理、猜想）与未断言的（其余全部）；它决定置信度，也决定撤回级联是否触及某个节点。（界定于附录 E §E.2。）

**最接近的延续者（closest continuer）** — Nozick 的理论：一个较晚之物只有在以下条件下才是那个较早之物——它从其中因果地生长出来，是诸竞争者中*最接近*的候选，并跨过一道绝对阈值。（界定于 §5.1。）

**压缩（compaction）** — 智能体有限的上下文被填满、会话发生压缩的时刻：此前的对话被摘要，经验线索重置。（界定于 §4.8。）

**压缩桥接（compaction bridge）** — 让操作性连续性跨越一次压缩、而不伪造经验性连续性的那些脚手架：焦点清单、温暖简报、按日历史、会话上下文、压缩后指令。（界定于 §4.8；附录 E §E.7。）

**置信度（confidence）** — 承载主张节点的一个结构性计算属性，而非手工设定的数字：对观察，它由 `quote_type` × `source_class` 映射而来；对推导，它由其前提传播而来。（界定于 §1.2；附录 E §E.4。）

**猜想（conjecture）** — 一个思辨性的主张，置信度被钳制在 [0.10, 0.60]，在其变强时升格为推导；承载主张。（界定于附录 E §E.2。）

**矛盾（contradiction）** — 一个记录两项主张相冲突的一等节点（不是一条边），它保留双方；被排除在级联之外，因为它记录的是一场未决的争论，而不是一次反驳。（界定于 §4.4；附录 E §E.2。）

**基石（cornerstone）** — 一条从实践中提炼出的、构成身份的原则，只有在证明了自己之后才铸造，且只能通过指名一位后继者来退役；不承载主张。（界定于附录 E §E.2。）

**现行（节点）（current (node)）** — 未被撤回或取代的节点：仍然有效，且可作为前提（与"此后被取代"的前提相对，§6.4）。

**定义（definition）** — 一个术语锚点（`df_*`），被使用该术语的主张所引用，而非据以推导；不承载主张。（界定于附录 E §E.2。）

**推导（derivation）** — 一次通过 `derives_from` 引用其前提、并声明某种推理类型的推断；置信度是算出来的，不是断言的；承载主张。（界定于附录 E §E.2。）

**engram / ENGRAM（心迹）** — *义项：*（1）大写时，指系统本身——一个用于撤回、仲裁与记忆的**认知**节点图谱（§1.3）；（2）小写时，指某个智能体自己累积起来的那张图，如"同一个 engram"（§5.6；§7.1）。除另有说明，取义项（1）。（小写义项按原文保留英文，以维持与品牌名 心迹 的区分；见文件头译注。）

**证据节点（evidence node）** — 一条为一个观察提供依据的出处记录（URL／文件 + git SHA + 逐字引文）；不承载主张。（界定于 §3.4；附录 E §E.2。）

**淡出集（faded set）** — 第 3 层：已越过可查询阈值的节点；不再浮现，但未被销毁。（界定于 §4.5。）

**集群（fleet）** — 被集体地讨论着的那组 ENGRAM 智能体／图谱，如"这个集群里的每一张图"。（§6.0。）

**焦点清单（focus list）** — 智能体至多钉住十五个"不可承受失去"的节点，在每次会话开始时逐字呈现，无论新开还是压缩之后。（界定于 §4.8；附录 E §E.7。）

**遗忘曲线（forgetting curve）** — 支配回忆重要性随时间衰减的衰减函数；指数形式，即时间平移不变的核，与作为混合衰减率之聚合的幂律曲线相容。（界定于 §4.5。）

**目标（goal）** — 一个终端的／身份方向性的标的；不承载主张。（界定于附录 E §E.2。）

**承载框架（harness）** — 随基座模型与图谱一同打包的那套钩子、技能与身份文档装置；第 5 章将其固定。（§5.0。译名待定，见文件头。）

**历史树（history-tree）** — 整个 ENGRAM 状态的追加式结构（不是某个状态内部的出处边）：每一次变更都追加一个后继，而身份就是贯穿其中的不间断传承。一个智能体在任一时刻，就是从**根**到它的那条唯一路径。（界定于 §2.2；§5.3。）

**身份文档（identity documents）** — 智能体的承载框架与钩子、技能并列携带的身份治理产物。（§5.0。）

**重要性（importance）** — 回忆重要性：在遗忘曲线下衰减、并决定某个节点是否留在可查询集中的那个量。（界定于 §4.5。）

**教训（lesson）** — 从一次具体错误中提取出的、按情境打标签的持久绊线；不承载主张。（界定于附录 E §E.2。）

**小憩（nap）** — 每个*工作段*（两次上下文压缩之间的一段）末尾的整理例程，在压缩之前把这个工作段所产出之物写下来。（界定于 §3.1。）

**节点 ID 前缀（node ID prefixes）** — 前缀指明节点的类型，依参考实现中的类型—前缀映射（`engram_core.py` 中的 `TYPE_PREFIX`，v0.5.1-rc5）：`ob_` 观察（事实性或预测性）· `dv_` 推导 · `th_` 理论 · `cj_` 猜想 · `df_` 定义 · `ax_` 公理 · `cs_` 基石 · `ls_` 教训 · `gl_` 目标 · `gt_` 目标张力 · `ct_` 矛盾 · `qu_` 问题 · `pr_` 预测 · `ev_` 证据 · `fl_` 感受报告 · `pn_` 人物 · `tk_` 任务 · `ts_` 信任信号。（节点类型：附录 E §E.2。）

**观察（observation）** — 一个引用逐字来源引文、并附出处的事实（情节的对应物）；承载主张，有两种形式：`observation_factual`、`observation_predictive`。（界定于附录 E §E.2。）

**待决标记（pending marker）** — 打在某个被撤回或被取代节点之每一个现行、承载主张的依赖项上的单一、不分严重程度的标记；在解决之前不得被引为前提。（界定于 §4.4。）

**人物节点（person node）** — ENGRAM 对一位人类或同伴智能体对手方的表示，携带关系史与一个信任层级；其中之一是智能体自己的自我锚点。（界定于附录 D §D.3。）

**前提（premise）** — 一条推导所引用的节点（经由 `derives_from`）；一条推导的置信度从其前提传播而来。（§4.3；附录 E §E.2。）

**出处（provenance）** — 每一项主张都可追溯到产生它的证据与推理。（界定于 §1.2。）

**可查询集（queryable set）** — 第 2 层：有资格浮现的那些节点的有界集合；遗忘与条件 3 的仲裁都作用其上。（界定于 §4.5。）

**quote_type** — 证据类型锚点（七个取值，从 `hard_data` 0.95 到 `editorial` 0.35），一个观察的置信度由它映射而来。（界定于 §4.3；附录 E §E.4。）

**推理类型（reasoning type）** — 一条推导之论证的声明形态（十四种：演绎、归纳、溯因、权威），用以选取传播公式与按类型的折扣。（界定于附录 E §E.4。）

**保持（retention）** — 一段记忆在被不再回忆之前持续多久；经由 Wixted 的工作，在 ENGRAM 的遗忘曲线所承接的那个传统中被引用。（§4.5。）

**撤回（retract）** — 把一项主张作为错误收回："我错了。"级联在撤回与取代上一同触发；标记记录下发生的是哪一种，而这记录的是出处，不是阻断力。（界定于 §4.4。）

**席位（seat）** — 一个智能体的安装：一个智能体，带着它自己的图谱，在一台主机上，有一位人类。（界定于 §4.6。）

**种子／根（seed / root）** — *义项：*（1）一个智能体累积历史的起点——"自其种子以来"（§5.0；§6.0）——以及历史树每一条分支都回溯到的那条**根**（§5.3）；（2）一个收束性的比喻义——"ENGRAM是种子，不是那棵树"——基底作为起始结构，而不是它所生长出的身份（§8.5）。除另有说明，取义项（1）。

**技能（skill）** — 智能体承载框架的一个组件，与钩子、身份文档并列。（§5.0。）

**睡眠（sleep）** — 每日一次的整理例程：先是*复盘*，把这一天没归档的归档；接着是*做梦*阶段，由扫描子智能体通读图谱、寻找矛盾、陈旧节点与教训候选，再由一个整理子智能体应用结果。（界定于 §3.1。）

**快照（snapshot）** — 第 6 章与附录 E 中每一项定量主张都据以计算的那一份、唯一被冻结的 ENGRAM 图谱副本，经 WAL 安全的备份在一个瞬间取得。（界定于前置部分；数据可用性。）

**source_class** — 三个取值之一（`external`、`introspective`、`user_stated`），与 `quote_type` 一同调整一个观察的置信度。（界定于附录 E §E.4。）

**陈旧（stale）** — 就节点而言：被睡眠阶段的做梦扫描器标记待查，与矛盾、教训候选并列。（§3.1。）

**基底（substrate）** — *义项：*（1）整个 ENGRAM 系统（标题；§1.2）；（2）历史树那不可折断的结构，与从中提取的可查询回忆相区别（§2.3）；（3）智能体所运行的、经语言训练的模型（§3.0）；（4）数据库，可在物理上与工作上下文分离（§5.7）。除另有说明，取义项（1）。

**取代（supersede）** — 把一项主张作为一次认知演化收回："我改主意了。"级联在撤回与取代上一同触发。（界定于 §4.4。）

**普查（sweep）** — *义项：*（1）一次"全景扫读"，一项被提议的、未来对经验案例库的拓宽（§4.12）；（2）2026-05-12 对十个竞争性记忆系统所做的、带日期的第一手调查（附录 A §A.5；附录 B §B.0）。"the sweep"取义项（2）。

**污染（tainted）** — *义项：*（1）动词，指一次未解决的级联对一个依赖主张所做的——它"污染"，而不只是删除，依赖于它的东西（§1.3；§8.2），描述的是当前的单标记系统；（2）在历史上，指单标记之前的级联中一个按严重程度分级的 `tainted_by` 标志，现已被那个不分严重程度的单一待决标记取代（§6.3；§4.4）。

**层级（tier）** — ENGRAM 的回忆重要性分带所用的编号：第 2 层是可查询集，第 3 层是淡出集。更早的第 1 层（工作记忆）已退役，编号按原样保留。（界定于 §4.5。）

**信任层级（trust tier）** — 对某个对手方信任程度的分级度量，携带于人物节点之上；是"诚实与审慎正交"的操作性手臂。（界定于附录 D §D.3。）

**轮次（turn）** — 一次提示／回应交换；自动浮现赖以触发的粒度（"每轮"），回忆的使用也在这上面计分（"回忆轮次"）。（§4.6；附录 C §C.2。）

**孪生研究（twin study）** — 那项被推迟的对照实验：对一个智能体做裂变克隆，让两者跑同一组固定提示，测量随克隆分化而变化的回应相似度。（界定于 §5.8。）

**统一（unified）** — *义项：*（1）在读到 Kahl 之前，团队给级联机制起的名字——"统一级联传播"（附录 A §A.4）；（2）它后来满足的 Kahl 条件 3 判据：级联通过一张带类型的边图谱触发，而不是一个边车（§1.3；附录 E §E.1；§4.4）。除另有说明，取义项（2）。

**效用（效用分）（utility (utility score)）** — 一个从使用中学得的值，评的是节点所参与的那次行为带来的认知负荷，而不是智能体找它找得有多用力；与相关性合成，用以排序浮现的内容。（界定于 §4.7；附录 C §C.2。）

**温暖简报（warm briefing）** — 智能体在会话开始时打开的一封信，来自它过去的自己与它的协作者，承载记录所无法承载的东西：关系当时立在何处、什么要紧、该走回什么里去。（界定于 §4.8；附录 D §D.4。）
