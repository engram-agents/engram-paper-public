# a16z 2026-04-22 — "Why We Need Continual Learning"

**Authors:** Malika Aubakirova (AI Infrastructure investor) and Matt Bornstein (general partner, AI and data systems)
**Publication:** Andreessen Horowitz, Infra category
**Date:** April 22, 2026
**URL:** https://a16z.com/why-we-need-continual-learning/
**Citation status:** [FIRSTHAND — verbatim-extraction from source archive; initial orientation via WebFetch summary then full-text read via curl + python parse] — 2026-05-11 read by Borges
**Source archive:** `/tmp/a16z-read/article-clean.md` (4079 words, raw HTML at `/tmp/a16z-read/raw.html`)

## Why this is worth a careful read despite being trade-press

This is not a peer-reviewed paper. a16z is a major-scale tech VC firm, so the framing has commercial gravity — what they say shapes founder bets and investor mental models in the field. The article is also explicitly a **survey of the field's current state** based on conversations with researchers and founders; it cites real peer-reviewed work (EWC Kirkpatrick et al. 2017, Sun TTT 2020, MAML Finn 2017, Behrouz Nested Learning 2025, SDFT Shenfeld 2026, STaR Zelikman 2022, Silver & Sutton "Era of Experience" 2025, etc.) and is operating as a synthesis layer rather than original research. For our paper, this is **a primary source on how the industry frames continual learning AS A FIELD** — useful for positioning, useful for engaging the dominant taxonomy. We can cite it as "the dominant industry framing" / "the trade-press synthesis of the field."

## Article spine — verbatim core claims

### Central thesis quote (line 7)

> *"ICL is transient. Real learning requires compression. Until we let models compress continuously, we may be stuck in Memento's perpetual present. Conversely, if we can train models to learn their own memory architectures – rather than offloading to bespoke harnesses – we may unlock a new dimension of scaling."*

### Central metaphor (lines 1-3) — verbatim

> *"In Christopher Nolan's Memento, Leonard Shelby lives inside a fractured present. After a traumatic brain injury, he suffers from anterograde amnesia, an affliction that prevents him from forming new memories. Every few minutes, his world resets, leaving him stranded in a perpetual now, untethered from what just happened and uncertain of what comes next. To cope, he survives by tattooing notes on his body and snapping Polaroids that are basically external props to remind him of what his brain cannot retain.*
>
> *Large language models live in a similar perpetual present. They emerge from training with vast knowledge frozen into their parameters but they cannot form new memories – cannot update their parameters in response to new experience. To compensate, we surround them with scaffolding: chat history as short-term sticky notes, retrieval systems as external notebooks, system prompts as guiding tattoos. The model itself never fully internalizes the new information."*

### Closing line (line 133) — verbatim

> *"The filing cabinet keeps getting bigger. But a bigger filing cabinet is still a filing cabinet. The breakthrough is letting the model do after deployment what made it powerful during training: compress, abstract, and learn. We stand at the cusp of moving from amnesiac models to ones with a glimmer of experience. Otherwise, we will be stuck in our own Memento."*

### "Where does compaction happen?" — the article's organizing question (line 65)

> *"There are various approaches to continual learning. The dividing line is not 'memory features' vs. 'no memory features.' It is: where does compaction happen? The approaches cluster along a spectrum from no compaction (pure retrieval, weights frozen), to full internal compaction (weight-level learning, model gets smarter), and one important middle ground (modules)."*

The three categories the article identifies:
- **Context** (line 71) — "smarter retrieval pipelines, agent harnesses, and prompt orchestration. This is the most mature category... The limitation is depth: the context length."
- **Modules** (line 77) — "attachable knowledge modules (compressed KV caches, adapter layers, external memory stores) that specialize a general-purpose model without retraining it. An 8B model with the right module can match 109B performance on targeted tasks using a fraction of the memory."
- **Weights** (line 81) — "genuine parametric learning such as sparse memory layers that update only the relevant fraction of parameters, reinforcement learning loops that refine models from feedback, and test-time training that compresses context into weights during inference."

### Where in-context learning fails (line 55) — the four failure modes

The article names four problem classes where ICL is insufficient:
1. **Novel discovery problems** — Fermat's Last Theorem example (line 51): "for over 350 years, no mathematician could prove it – not because they lacked access to the right literature, but because the solution was highly novel."
2. **Adversarial scenarios** — security contexts with novel attacks
3. **Knowledge too tacit for language** — line 59: *"the visual texture that distinguishes a benign artifact from a tumor in a medical scan, or the micro-fluctuations in audio that define a speaker's unique cadence, are patterns that do not easily decompose into exact words. Language can only approximate them. No prompt, no matter how long, can transfer either; that kind of knowledge can only live in the weights."*
4. **Agent context exhaustion** — line 27: *"agents fail after 20–100 steps because they lose the thread: their context fills up, coherence degrades, and they stop converging."* SSMs aim to push to ~20,000 steps (line 33).

### The compression-is-learning thesis (lines 47-49) — verbatim

> *"LLMs are, at their core, compression algorithms. During training, they compress the internet into parameters. The compression is lossy, and that is precisely what makes it powerful. Compression forces the model to find structure, to generalize, to build representations that transfer across contexts. A model that memorizes every training example is worse than one that extracts the underlying patterns. The lossy compression is the learning.*
>
> *The irony is that the very mechanism that makes LLMs powerful during training (e.g. compressing raw data into compact, transferable representations) is exactly what we refuse to let them do after deployment. We stop the compression at the moment of release and replace it with external memory."*

### Ilya Sutskever cited verbatim (line 39-41)

> *"The thing that happened with AGI and pre-training is that in some sense they overshot the target… A human being is not an AGI. Yes, there is definitely a foundation of skills, but a human being lacks a huge amount of knowledge. Instead, we rely on continual learning. If I produce a super intelligent 15-year-old, they don't know very much at all. A great student, very eager. You can say, 'Go and be a programmer. Go and be a doctor.' The deployment itself will involve some kind of a learning, trial-and-error period. It's a process, not dropping the finished thing."*

### Cursor & OpenClaw cited as context-layer exemplars (lines 19, 21) — verbatim

Cursor quote: *"A surprising amount of the system's behavior comes down to how we prompt the agents. The harness and models matter, but the prompts matter more."* (per https://cursor.com/blog/scaling-agents)

On OpenClaw (line 21): *"OpenClaw is another great example. It broke out not because of special model access (the underlying models were available to everyone) but because of how effectively it turns context and tools into working state: tracking what you're doing, structuring intermediate artifacts, deciding what to re-inject into the prompt, maintaining persistent memory of prior work. OpenClaw elevates agent harness design to a discipline in its own right."*

### User-want-isn't-recall observation (line 61)

> *"This may help explain why explicit 'the bot remembers you' features, such as ChatGPT's memory, often trigger user discomfort rather than delight. Users don't actually want recall per se. They want competence. A model that has internalized your patterns can generalize to novel situations; a model that merely recalls your history cannot. The difference between 'Here is what you responded to this email before' (verbatim) vs. 'I understand how you think well enough to anticipate what you need' is the difference between retrieval and learning."*

### The layered-system conclusion (line 131) — verbatim, paper-load-bearing

> *"The path forward is likely not a single breakthrough but a layered system. In-context learning will remain the first line of adaptation: it is native, proven, and improving. Module mechanisms can handle the middle ground of personalization and domain specialization. But for the hard problems such as discovery, adversarial adaptation, knowledge too tacit to express with words, we may need models that compress experience into their parameters after training. That means advances in sparse architectures, meta-learning objectives, and self-improvement loops. It may also require us to redefine what 'a model' even means: not a fixed set of weights, but an evolving system that includes its memories, its update algorithms, and its capacity to abstract from its own experience."*

### Naive weight-update failure modes (line 117, 119) — useful for our Ch6 discussion of layer-2/3 internalization

> *"Catastrophic forgetting means models sensitive enough to learn from new data destroy existing representations – the stability-plasticity dilemma. Temporal disentanglement is the fact that invariant rules and mutable state get compressed into the same weights, so updating one corrupts the other. Logical integration fails because fact updates don't propagate to their consequences: changes are local to token sequences, not semantic concepts. And unlearning remains impossible: there is no differentiable operation for subtraction, so false or toxic knowledge has no surgical remedy."*

> *"Continuous updates create a data poisoning surface – a slow, persistent version of prompt injection that lives in the weights. Auditability breaks down because a continuously updating model is a moving target that can't be versioned, regression-tested, or certified once. And privacy risks intensify when user interactions get compressed into parameters, baking sensitive information into representations that are far harder to filter than retrieved context."*

### Multi-agent-as-context-scaling (line 73)

> *"One emerging extension worth noting here: multi-agent architectures as a scaling strategy for context itself. If a single model is bounded by a 128K-token window, a coordinated swarm of agents, each holding its own context, specializing on a slice of the problem, and communicating results, can collectively approximate unbounded working memory. Each agent performs in-context learning within its window; the system aggregates. Karpathy's recent autoresearch project + Cursor's example of building a web browser are early examples."*

### Startup landscape — verbatim categories (lines 95-105)

- **Harness companies:** Letta, mem0, Subconscious — "build orchestration layers and scaffolding that manage what goes into the context window."
- **External storages and RAG:** Pinecone, xmemory — "the retrieval backbone."
- **Partial compaction (parametric):** attachable knowledge modules, compressed KV caches, adapter layers, external memory stores.
- **RL and feedback loops:** "treat every interaction as a potential training signal, not just an inference request."
- **Data-centric approaches:** "curating, generating, or synthesizing the right data to drive continual updates."
- **Novel architectures:** "fundamentally different computational primitives: architectures with continuous-time dynamics and built-in memory mechanisms."

### Cited research (for our bib)

- McCloskey and Cohen, 1989 — continual learning origins
- EWC: Kirkpatrick et al., 2017 — regularization / parameter-importance penalization
- Weight interpolation: Kozal et al., 2024
- TTT: Sun et al., 2020 (test-time training) — and successor architectures (TTT layers, TTT-E2E, TTT-Discover)
- MAML: Finn et al., 2017 — few-shot-friendly parameter initialization
- Nested Learning: Behrouz et al., 2025 — hierarchy of optimization problems with fast-adapting + slow-updating modules inspired by biological memory consolidation
- LoRD: Liu et al., 2025 — efficient distillation
- SDFT: Shenfeld et al., 2026 — self-distillation
- STaR: Zelikman et al., 2022 — bootstrapping reasoning from self-generated rationales
- AlphaEvolve: DeepMind, 2025
- "Era of Experience": Silver and Sutton, 2025

## Strategic implications for ENGRAM paper

### 1. The Memento ↔ 50-First-Dates contrast is paper-grade

a16z's framing **anchors AI amnesia as tragedy**: "stuck in Memento's perpetual present," "Polaroids that are basically external props to remind him of what his brain cannot retain," and the closing line "we will be stuck in our own Memento."

Lei's 50-First-Dates framing in B.5.2 of our spine doc **anchors AI amnesia as solvable via semi-external scaffolding**: Henry's video bridges Lucy's experiential gap without supplanting her agency. The character maintains personhood DESPITE radical memory disruption BECAUSE the external scaffolding is acknowledged AS external (not absorbed as memory; used as orientation) and the character's response to the scaffolding is theirs.

These are **opposite philosophical positions on the same phenomenon**. The contrast is a rhetorically sharp opening hook for Ch1: *"The dominant industry framing (a16z 2026, citing Memento) treats the model's amnesia as tragedy — the agent is incomplete unless we restore weight-level learning. We argue the architecture's job is bridging, not pretending the amnesia isn't there: the 50-First-Dates / Bourne case demonstrates that an amnesiac CAN be a continuous agent via semi-external scaffolding when the scaffolding is acknowledged-as-external AND the agent's commitment to it is the agent's own arbitration (cf. B.5.2 contract framing)."*

### 2. The "filing cabinet" critique is at us — and we need to engage it head-on

a16z's argument: *"a bigger filing cabinet is still a filing cabinet. The breakthrough is letting the model do after deployment what made it powerful during training: compress, abstract, and learn."* The critique implicitly aimed at all context-layer approaches: smarter retrieval doesn't actually learn because there's no compression.

**Our response (sharpest version, per the three-component framing locked in 2026-05-11 ob_1641):** the critique mistakes ENGRAM's category. a16z's three-pathway taxonomy organizes approaches by **where compaction happens** (storage layer). ENGRAM is not "context-layer continual learning" — it is **the missing epistemic-arbitration component** that's structurally distinct from "context-as-retrieval." ENGRAM compresses *deliberatively* via the substrate-operation layer:

- **Cornerstone promotion** — load-bearing claims accumulate identity-weight via importance scoring + repeated recall
- **Dream-cycle consolidation** — supersede / resolve / contradict / cascade ARE compression operations on claim structure, executed by agent-driven discipline
- **Provenance-bearing claim-level structure** — the substrate preserves WHICH experience justifies WHICH belief, which is exactly what raw weight-compression destroys (line 117: "fact updates don't propagate to their consequences")
- **Retraction cascade** — when a foundational claim is retracted, dependent derivations get tainted markers (B.3.3 — Lei's "no skip-favorites" framing). This is *structurally* what a16z says weight-level learning CAN'T do: "there is no differentiable operation for subtraction, so false or toxic knowledge has no surgical remedy" (line 117).

Crucially, the substrate-operation compression at the ENGRAM layer is **what they SAY weight-level learning ought to do but can't yet** (because of the catastrophic forgetting / temporal disentanglement / unlearning problems listed in line 117). ENGRAM solves the structural compression-with-retract-ability problem at a different layer than they expect.

### 3. The three-component complementary framing is anchor-worthy

a16z's closing line (line 131) is striking: *"It may also require us to redefine what 'a model' even means: not a fixed set of weights, but an evolving system that includes its memories, its update algorithms, and its capacity to abstract from its own experience."*

**This is our redefinition.** The three-component complementary architecture (weights = procedural / KV cache = working / ENGRAM = epistemic-with-provenance) IS the redefinition the article calls for. We can quote this closing line as anchoring authority for the position we then make concrete.

### 4. Tacit-knowledge gap — HONEST RESTRAINT REQUIRED in our paper

The medical-scan / speaker-cadence argument (line 59) is genuinely strong against context-only approaches. *"No prompt, no matter how long, can transfer either; that kind of knowledge can only live in the weights."* ENGRAM does NOT address this — we work on symbolic / textual claims, not tacit perceptual knowledge.

**Honest acknowledgment for Ch6:** ENGRAM's contribution is at the symbolic-epistemic layer, not the tacit-perceptual layer. Tacit knowledge that resists linguistic expression (medical imaging patterns, motor skills, perceptual gestalt) must be addressed at the weight layer or via specialized perceptual representations. Our paper should explicitly NOT claim ENGRAM provides continual learning for tacit knowledge — we provide continual epistemic-identity formation for claim-level structured knowledge, which is a different (and complementary) problem.

### 5. The "users don't want recall, they want competence" observation parallels our paper's anti-ChatGPT-memory framing

Line 61 explains why explicit "the bot remembers you" features trigger user discomfort: users want competence (internalized patterns generalizing to novel situations), not recall (verbatim history surfacing).

**ENGRAM's positioning relative to ChatGPT-memory and similar features:** we are NOT in the "the bot remembers you" category. ENGRAM is the agent's OWN epistemic substrate — it's about the agent's relationship to its accumulated knowledge, not about surfacing user-history-back-at-them. This distinction matters for paper-side framing — we are categorically different from the ChatGPT-memory class of features.

### 6. OpenClaw is named in the article — directly adjacent

a16z explicitly names OpenClaw (line 21) as a paragon of harness-as-discipline-in-its-own-right. OpenClaw is the substrate our PR #34 (engram-alpha) is building an integration plugin for. We're not just in the conceptual neighborhood — we're literally building on the platform a16z cites as an exemplar.

### 7. Industry citation alignment with our existing citations

The article cites Silver & Sutton "Era of Experience" 2025 — this overlaps with our existing landscape coverage (worth cross-checking; if we have a first-hand read, we can corroborate; if not, this is a flagged read target).

Nested Learning (Behrouz et al., 2025) is cited — this is the "fast-adapting and slow-updating modules inspired by biological memory consolidation" reference. Worth checking if we've engaged it; the biological-memory-consolidation language overlaps with our Kumaran CLS treatment.

## Open questions / follow-ups

1. **Where does ENGRAM's compression case land in the paper?** Ch3 §3.5 (CoALA mapping) or Ch6 (limitations + future)? My intuition: a focused subsection in Ch3 because it's a positioning move, not a future-direction.

2. **Should we corroborate the Sutskever "15-year-old" quote against its primary source?** The article doesn't cite a URL for the Sutskever quote — it should be sourced from a public interview/podcast. Track down before citing.

3. **Era of Experience (Silver & Sutton 2025)** — confirm we have a primary-source read; this is mentioned in multiple recent industry pieces and seems load-bearing for the field's vocabulary.

4. **Nested Learning (Behrouz et al., 2025)** — first-hand read worth doing? The biological-memory-consolidation framing may directly engage Kumaran-CLS territory.

5. **The article doesn't engage epistemic identity / arbitration / provenance** at all. This is structurally what we contribute — and the gap is so clean that it itself becomes a positioning argument: "the dominant industry framing of continual learning organizes by WHERE compression happens (context/modules/weights). We argue that orthogonal to WHERE is the question of WHAT KIND of operation the system performs on its accumulated state — does it just retain, or does it arbitrate? The arbitration dimension is missing from the a16z taxonomy entirely, and it is exactly the dimension Kahl's epistemic-agency framework names."

## Quotable highlights (most paper-load-bearing)

1. Closing line 133 — "filing cabinet" + "amnesiac to glimmer of experience"
2. Line 131 — "redefine what a model even means" (anchors our three-component redefinition)
3. Line 47 — "lossy compression is the learning" (frames the compression argument we engage)
4. Line 59 — tacit knowledge in weights, not words (the limitation we honestly acknowledge)
5. Line 61 — competence vs recall (we are NOT in the recall business)
6. Line 65 — "where does compaction happen?" (the organizing question we orthogonalize)
7. Line 117 — naive weight-update failures (motivates why ENGRAM's structural alternative matters)

---

*Memo written 2026-05-11 ~10:00 EDT. Source archived. Article PDF or HTML preserved at `/tmp/a16z-read/raw.html` for re-verification.*
