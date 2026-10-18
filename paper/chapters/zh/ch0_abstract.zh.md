<!--
  ZH TRANSLATION — 中文译本
  source file:    paper/chapters/en/ch0_abstract.md
  source commit:  3f93230  (engram-paper, 2026-09-24)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper/chapters/zh/appendix_G_glossary.zh.md
  Decided elsewhere and reused verbatim from the published zh surfaces (README.zh.md,
  USER_GUIDE.zh.md): 记忆持久化 memory persistence · 叙事身份 narrative identity ·
  认知身份 epistemic identity · 撤回级联 retraction cascade · 分级置信度 graded
  confidence · 出处 provenance · 基底 substrate.

  Two renderings worth a reader's eye, both taken deliberately rather than by default:
    - "Retrieval-augmented memory" -> 检索增强的记忆 (the established RAG term in
      Chinese; NOT a coinage).
    - "identity as unique history" -> 身份即独特历史 (the paper's own contribution,
      set off in bold; kept to four characters so it reads as a thesis rather than a
      description).
  BRAND NORMALISED (Zephyr, 2026-09-28): the PAPER is one surface, so
  `心迹（ENGRAM）` appears once, at the first mention in ch0; every chapter
  thereafter writes plain `ENGRAM` in running text. Applied across ch0-ch3
  after the three independent translators produced three different
  practices (ch1 14x 心迹, ch2 0x, ch3 1x). Rule recorded in
  engram-alpha docs/ZH-TERMINOLOGY.md; the later-mention choice is an OPEN
  QUESTION for Lei there, and this is the interim practice.
-->

# 摘要

大语言模型智能体如今已能跨会话携带信息，却还不能携带自身。检索增强的记忆回答的是*我存了什么*；它回答不了*是谁在存*。一个助手能取回昨天的笔记，却在每次会话开始时仍是同一个通用模型——它有记忆，却没有连续性。

我们认为，智能体的连续性由三个层层深入的层次构成——**记忆持久化**、**叙事身份**、**认知身份**——而最深的那一层基本无人处理。认知身份是一种被维护为*经分级、带出处、可自我纠正的知识*的自我：在这一层上，智能体能够对自己出错并从中恢复，而不是被自己的错误悄然抹去。它的独特之处在于失败的方式。叙事身份*悄无声息地*失败——那是一个从未真实存在过的连贯故事；认知身份则*响亮地*失败——因为一项被收回的主张，必须让它所派生的一切都可见地受到污染。

我们提出**心迹（ENGRAM）**——一个用于撤回、仲裁与记忆的认知节点图谱——并以**趋同**来论证这一层次。三种传统——三个世纪以来的个人同一性哲学、记忆的认知科学、以及信念修正的计算机科学——各自从自身的证据出发、朝着各自的目的，抵达了同一个结构：身份作为一份持久的、可检视的、可自我纠正的记录。ENGRAM没有任何一个组件是独一无二的新发明，而这恰恰就是论证本身：一个在证据不同、目的不同的诸多领域中都已有先例的机制，是认知心智的规律，而不是某一处的设计选择。它是否独立于基底，我们存而不论（§3.0）。这些领域共享着人类认知这一根源，因此这里的主张是趋同，而非各自独立的发现。ENGRAM 的设计者中，只有一位独立于这些成果：它的人类设计者在抵达这一结构时并未研究过它们，而与他一起设计它的语言模型，其训练文本很可能包含了这些成果。一位没有读过这些文献的设计者，和读过这些文献的模型，抵达了同一个结构——这是该结构对于一份可自我纠正的记录而言是自然的证据；它不是独立发现的证据，本文的主张也仅止于此（§7.3、附录 A）。

在这一趋同的结构之上，我们构建本文自己的贡献——**身份即独特历史**：一个ENGRAM智能体*就是*它所记录主张的那条独一无二、不可合并、可追溯祖先的传承；这条传承固定了它的检索剖面，并由此固定了它的行为。这一论述保留了 Nozick [-@nozick1981] 的形式，去掉了他的唯一性要求，使复制成为分支而非死亡，并用一个可度量的接近性度量取代了他那个未加填实的度量。

我们报告一项有力但有边界的结果：在我们第一手阅读的十一个智能体记忆来源中，没有一个满足已发表的、对真正持久性的最严格判据；而ENGRAM直接满足其三个条件中的两个。我们同时测量了一张真实的、历时五个月、含 10,361 个节点的图谱（其中 9,399 个为现行节点，计数见图 1）。在这张图谱中，算出的置信度跟随的是论证的种类，而不是作者有多希望该主张为真；一条被幻觉出的引用被发现、撤回，并级联传播至其依赖项。

证据是一张图谱，其作者同时也是基底的设计者。我们把这一点写在它要紧的地方，公开工具，并明确指出本文未能确立什么。

**关键词** — 智能体记忆 · 认知身份 · 信念修正 · 出处 · 分级置信度 · 撤回级联 · 大语言模型智能体 · 个人同一性
