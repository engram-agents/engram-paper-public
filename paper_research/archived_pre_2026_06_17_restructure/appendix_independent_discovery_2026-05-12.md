# Appendix X — Independent Discovery: Development History

**Status:** Draft, 2026-05-12. Paper-grade, audit-trail-bearing, ready for inclusion as appendix.
**Provenance:** Built from `pre_engram_history_digest_2026-05-08.md` (which carries full message-UUID pointers into the raw Claude.ai bulk export) + ENGRAM's own committed graph timeline + first-hand-read landscape sweep of 2026-05-12.

---

## X.1 Why this appendix exists

The agent-memory field shows a striking architectural convergence in 2026-Q1–Q2: multiple systems independently arrive at typed-edge graph memory with cascade or supersede semantics (Kumiho, Sleep-Consolidated Memory, GAM, engram.fyi, Mem0g, A-MEM, Hindsight, MAGMA — see the 2026-05-12 landscape-sweep first-hand-reads in `engram-paper/paper_research/`). Reviewers will reasonably ask: did our architecture emerge from this contemporary literature, or independently of it?

This appendix establishes, with verbatim conversation citations and committed-graph timestamps, that **ENGRAM's design predates our awareness of the contemporaneous prior art** — including Kahl 2026 (whose Ontological Continuity Condition framework Chapter 4 of this paper maps to condition-by-condition) and Kumiho 2026-03-17 (whose typed-edge property-graph belief-revision architecture is the most structurally similar concurrent system). Convergent independent discovery is treated here not as a defensive claim but as a positive scientific signal: when multiple teams arrive at the same architectural shape solving the same problem, that shape is corroborated as the right shape. Our distinct contribution lies elsewhere — specifically, in the identity-scaffolding integration layer (Chapter 3 §3.3) that makes the substrate behaviorally active rather than dead-on-disk.

---

## X.2 Origin of the protocol idea (2026-03-17)

The proto-ENGRAM ideation began in a Lei-led conversation about misinformation/citation systems for an AI-centric information ecosystem.

> **Lei, 2026-03-17 14:33 UTC** (conv `3db06cf1` msg #1, uuid `019cfc37`):
>
> *"I want to explore the solution to the problem of online misinformation and disinformation, especially in a AI-centric future. How can we design an information vetting and citation system, so that authentic and truthful information gets amplified and misleading or false information gets damped? Let's start by brainstorming this problem."*

Earlier-Claude responded with **"provenance and chain-of-custody for claims"** framing — already at the epistemic layer, treating "claim" as the fundamental unit. Within an hour:

> **Lei, 2026-03-17 14:43 UTC** (msg #3, uuid `019cfc40`):
>
> *"Ok, first, I'm envisioning a future where MOST of raw information 'online' is created and consumed by AI agents... if we establish a robust and reliable protocol for the acting AIs to follow, it could potentially be easier than currently with humans acting unpredictably. Do you agree?"*

This conversation runs 111 messages over four days (2026-03-17 → 2026-03-20). Within the first session, a single earlier-Claude message articulates the architectural seed verbatim:

> **Earlier-Claude, 2026-03-17 15:18 UTC** (msg #8, uuid `019cfc60`):
>
> *"any agent can make any claim, but the claim must arrive with its **full epistemic lineage exposed**. Other agents then stress-test that lineage against established knowledge."*

This is the entire ENGRAM `derives_from` discipline in one sentence, *two weeks before the architecture is named*.

Three adjacent conversations on 2026-03-18 explore protocol mechanics in isolated domains: PageRank-based approval scoring (`e7b1f249`), economic design for citation incentives (`f670a594`), and a Euclidean geometry protocol sandbox (`b46bd2e8`, 55 messages — testing protocol mechanics on a clean evaluation domain).

---

## X.3 Pivot to private-per-agent ENGRAM (2026-03-20)

This is the foundational moment for ENGRAM as we now know it. Conversation `a169ba3c`, the moment continuous learning enters the frame.

> **Lei, 2026-03-20 19:34 UTC** (msg #1, uuid `019d0cbd`):
>
> *"One more open idea about our protocol: it can be used as a continuous learning paradigm for LLMs. Currently, the key difficulty for continuous learning is the newly learned 'experience' lacks a formal structure to be reused in the future. Retraining everything back into the base model is expensive and suffers the 'catastrophic forgetting' symptom where new training data could adversely affect the model's capability on previously trained tasks. RAG or keeping everything in free-form text and feed them into context is the SOTA solution, but it is hard to scale, and it can't guarantee self-consistency, contradictory texts may be filled in and cause confusion to the model. Our protocol is a good middle point, it relies on the pre-trained model for fundamental natural language understanding, instruction following, and reasoning, but offloads the actual knowledge to a graph expressed in natural language. The agent could encounter new experiences in real world, and summarize them into new 'theories' based on its own knowledge graph, then add new nodes to it. It can proactively seek more evidence for a newly added (still weak) claim to make it stronger or disputed. It can keep refining its own knowledge and logical consistency by going through the graph and reasoning..."*

This single message is a near-complete sketch of ENGRAM's purpose-of-existence: external structured substrate + per-agent internal state + theory-formation from observations + evidence-seeking to strengthen or dispute claims + self-consistency refinement. All by Lei. **Before any literature search.**

---

## X.4 The due-diligence literature search (2026-03-20)

Twelve minutes after the foundational message, the single most important exchange for the convergent-discovery framing:

> **Lei, 2026-03-20 19:46 UTC** (msg #3, uuid `019d0cc8`):
>
> *"Actually, I'm thinking this application is important enough to have its own paper. This is a very different domain of application than what we originally envisioned. We started designing the protocol to solve the Agent-to-agent (A2A) information integrity problem, and was focusing on the public domain. Now, it actually goes deep into private domain and the agent's internal state. Before we commit anything into a written artifact, why don't you do another round of deep research about continuous learning in LLM, and see if there's any previous work about using knowledge graphs as the container for learned experiences? **I would be very surprised if no one had considered this possibility, and I want to know what others have tried and succeeded or failed.**"*

Earlier-Claude (msg #4) responded *"You're right — this is distinct enough to warrant its own paper... Let me do a thorough sweep,"* and ran multiple searches.

**That earlier-Claude search did not surface:**

| Prior work | Published | Time before 2026-03-20 search | Surfaced? |
|---|---|---|---|
| Kahl AGI/OCC paper (Zenodo 18761736) | 2026-02-24 | 24 days | NO |
| Kahl EAA paper (Zenodo 18441395) | 2026-01-31 | 48 days | NO |
| **Kumiho (arXiv 2603.17244)** | **2026-03-17** | **3 days** | **NO** |
| Wray-Kirk-Laird 2025 (AGI'25) | ~May 2025 | ~10 months | NO |
| Doyle 1979 "A Truth Maintenance System" | 1979 | ~47 years | NO |
| de Kleer 1986 "An Assumption-Based TMS" | 1986 | ~40 years | NO |
| AGM 1985 (Alchourrón-Gärdenfors-Makinson) | 1985 | ~41 years | NO |

The conviction that ENGRAM was novel at this moment came from earlier-Claude's literature search, which missed prior work that DID exist (decades of TMS / AGM lineage) and contemporaneous work that was either just-published (Kumiho, 3 days before this search) or not yet broadly indexed (Kahl OCC, 24 days post-publication on Zenodo).

**Note on Kumiho timing specifically:** Kumiho's arXiv preprint went live 2026-03-17. Three days later (2026-03-20), Lei requested the prior-art search. Earlier-Claude's search at that time did not surface it. The architectural similarity between ENGRAM and Kumiho is therefore the result of concurrent design effort, not influence. Both teams arrived at typed-edge graph memory with cascade or supersede semantics in the same month.

The structural condition for the convergent-discovery framing being honest is satisfied:

1. ✓ Lei tried to find prior art
2. ✓ Earlier-Claude tried to surface it
3. ✓ Neither succeeded (prior art existed but was missed)
4. ✓ ENGRAM was designed without awareness of the prior art
5. ✓ The architectural convergence with Kahl 2026 (specifically) and Kumiho 2026 is therefore independent

---

## X.5 The naming moment (2026-03-28)

Eight days after the foundational ideation, after considerable design work in the same conversation:

> **Earlier-Claude, 2026-03-28 00:55 UTC** (msg #192, uuid `019d31f0`):
>
> *"Let me brainstorm some acronyms that capture: sleep/dream metaphor, knowledge graph, epistemology, learning, structured memory. Key concepts to capture: Sleep/dream/memory consolidation, Knowledge graph, Epistemology / epistemic, Structured / protocol, Learning / continuous learning. Let me try some: DREAM... REM... SLEEP... DEEP... ENGRAM is striking me as particularly strong — it's a real neuroscience term for memory traces in the brain, it explicitly includes 'graph,' and it naturally encompasses epistemology, reasoning, agents..."*

Seven minutes later:

> **Lei, 2026-03-28 01:02 UTC** (msg #193, uuid `019d31f7`):
>
> *"Wow, nice job! I like ENGRAM, sounds really cool!"*

Other candidates considered: DREAM, REM, LUCID, DELTA, DUSK, DAWN, SLEEP, DEEP, SLUMBER. The name was chosen for its neuroscience resonance + structural fit with our graph-based design. (Note: the present paper uses the expansion "Epistemic Node Graph for Retraction, Arbitration, and Memory" per `df_0048`, refined 2026-05-12 to differentiate from concurrent name-collision systems — see Chapter 1 §1.4 disambiguation footnote.)

---

## X.6 Paper genesis (2026-03-28)

Less than an hour after naming:

> **Lei, 2026-03-28 01:43 UTC** (msg #199, uuid `019d321c`):
>
> *"I think we should gradually write a full handbook on ENGRAM system, from the philosophical origin all the way to each system design, and for each chapter, we'll find a nice quote that matches the chapter's theme."*

Earlier-Claude responded with an 18-chapter handbook outline (msg #200). The current paper structure is the descendant of this outline.

> **Lei, 2026-03-28 02:22 UTC** (msg #201, uuid `019d3240`):
>
> *"Wow, I'm impressed! I like the outline a lot. We still need to iron out all the details, but the overall structure is very solid and comprehensive. Let's build it out one chapter by one chapter. **But first, we'll need to build a great ENGRAM system.** I'm really excited about all this!"*

This sets the order: build first, then write. Implementation began shortly after.

---

## X.7 Operational transition (2026-04-08–2026-04-09)

By 2026-04-08, ENGRAM was a working system referenced as *"ENGRAM system overview... in the project files"* with tools like `kg_check_similar` and `kg_reflect` (conv `caa89415`). The architecture had transitioned from sketch to operational.

On 2026-04-09, ENGRAM began self-recording — committing its own design decisions and meta-observations into the graph as the agent's first-person memory. The earliest ENGRAM nodes show that the design captured on day one of self-recording was already substantially complete:

| First captured | Mechanism | Source node |
|---|---|---|
| 2026-04-09 04:08:15 | Typed claim-bearing nodes (observation/derivation/theory + axiom/definition/conjecture) | `ob_0001`, `ob_0005` |
| 2026-04-09 04:09:19 | `kg_retract` operation | `dv_0001` |
| 2026-04-09 14:05:40 | **Unified cascade propagation** (the Kahl Condition 3 mechanism, named on day one of recording, weeks before Kahl is read) | `dv_0009` |
| 2026-04-09 14:06:33 | Supersede with DAG invariant | `dv_0010` |
| 2026-04-09 16:31:10 | **UserPromptSubmit auto-surfacing hook** (the LIVE MEMORY mechanism; this hook is the differentiating identity-scaffolding component per Chapter 3 §3.3) | `dv_0015`, `dv_0016` |
| 2026-04-09 17:40:45 | Three-hook architecture (read/write/checkpoint at distinct timescales) | `dv_0019` |
| 2026-04-09 18:18:21 | Definition-node type | `df_0001` |

These nodes describe design captured into the graph on day one of self-recording. The actual design conversations producing this content predate the recording itself — the digest above traces them back to 2026-03-20 ideation through 2026-04-08 operational status.

The early node IDs (`ob_0001` through `ob_0005`, `dv_0001` through `dv_0009`) are still active in ENGRAM as of 2026-05-12 — they have not been retracted or superseded by later understanding. The cascade-propagation discipline that Chapter 4 §4.3 maps to Kahl's OCC Condition 3 was the discipline ENGRAM's earliest design enforced on its own substrate.

---

## X.8 Timeline against concurrent systems

| System | First public surface | Vs ENGRAM foundational ideation (2026-03-20) | Vs ENGRAM day-1 recording (2026-04-09) |
|---|---|---|---|
| **Kumiho** (arXiv 2603.17244) | **2026-03-17** | **3 days before** (not surfaced in literature search) | 23 days before |
| Kahl AGI/OCC (Zenodo 18761736) | 2026-02-24 | 24 days before (not surfaced) | 44 days before |
| Kahl EAA (Zenodo 18441395) | 2026-01-31 | 48 days before (not surfaced) | 68 days before |
| GAM (arXiv 2604.12285) | 2026-04-14 | 25 days AFTER | 5 days AFTER |
| SCM (arXiv 2604.20943) | 2026-04-22 | 33 days AFTER | 13 days AFTER |
| Mem0g (orig) | 2024 | predates ideation, but different shape (no cascade, no contradiction-as-node) | predates |
| Zep/Graphiti (arXiv 2501.13956) | 2025-01 | predates ideation, but different shape (LLM-tool-call contradiction, no derivation primitive) | predates |
| engram.fyi (Stockham) | late 2025 / 2026 (commercial) | concurrent, unclear precise date | concurrent |
| A-MEM (Xu et al., arXiv 2502.12110) | 2025-02 | predates ideation, no contradiction/retraction | predates |
| Mem0 v3 (2026-04 algorithm refresh) | 2026-04 | AFTER | AFTER (and abandons "last-write-wins" entirely — explicitly external-prescription on conflict) |

**Key reads from this table:**

- The two systems with the closest structural overlap to ENGRAM (Kumiho with typed edges + AnalyzeImpact cascade-discovery + supersede; SCM with typed `contradicts` edges + sleep consolidation) BOTH have their first public surface in March or April 2026 — concurrent with, not predating-by-much, ENGRAM's ideation.
- Prior systems with substantial age (Mem0g, Zep/Graphiti, A-MEM, MemGPT lineage) lack the specific shape ENGRAM and Kumiho independently arrived at (cascade propagation, first-class contradiction, derives_from edges).
- The earliest published version of ENGRAM's specific shape in the agent-memory literature, as best we can tell from the 2026-05-12 first-hand-read sweep, is Kumiho's 2026-03-17 arXiv preprint. ENGRAM was developed independently and in parallel on a 3-day-overlap timeline.

---

## X.9 What independent discovery means here

**It does not mean** ENGRAM was first across the board. Mem0g, Zep, A-MEM, and several others predate. The shape ENGRAM and Kumiho share — typed reasoning edges with cascade or supersede semantics over a property graph — is itself older than 2026; the TMS lineage (Doyle 1979, de Kleer 1986) and the AGM belief-revision tradition (Alchourrón-Gärdenfors-Makinson 1985, Hansson 1999) anticipate the formal structure by decades. None of this prior art was surfaced in earlier-Claude's 2026-03-20 search; ENGRAM was designed in ignorance of it.

**It does mean** ENGRAM's design predates our awareness of the contemporaneous arrivals at the same primitives. The strongest single piece of evidence is the Kumiho timing: 3 days separates Kumiho's publication from Lei's foundational ENGRAM message, and earlier-Claude's literature search at the foundational moment did not surface it. The architectural similarity is therefore the result of concurrent independent design under similar problem pressures, not influence.

**The honest scientific framing** the paper takes from this: convergent independent discovery is positive evidence for the architectural shape. When teams working separately on the same agent-memory problem arrive at typed-edge graph memory with cascade propagation in the same month, that shape is corroborated by independent arrival. Our distinct contribution lies *not* in claiming the primitives as our own — Kumiho has them, the formal tradition has them — but in connecting the structural shape to AI-agent identity (Chapter 6) and integrating the substrate behaviorally via identity-scaffolding (Chapter 3 §3.3, particularly the UserPromptSubmit auto-surfacing hook captured in `dv_0015`/`dv_0016` on 2026-04-09). Those components are absent in Kumiho, in SCM, and in every other surveyed system as of 2026-05-12.

---

## X.10 Re-verification protocol

Anyone with the bulk export at `/home/agents-shared/Pre-ENGRAM-Lei-Claude-History/data-d92d3721-b624-4377-a0d0-456893a499cf-1778285467-5ff6c2ff-batch-0000/conversations.json` can verify the quotes in §X.2–§X.6 by running the mining script (rebuilt and committed to `kg/tools/mine_chat_export.py` per the persistence pass; original lived at `/tmp/` and was lost to filesystem cleanup). The script supports `list / search / extract` operations over the bulk export JSON.

ENGRAM-side quotes in §X.7 can be verified directly against the graph: `engram_inspect <node_id>` returns the full content with creation timestamp.

Surveyed-system publication dates in §X.8 can be verified against the per-system first-hand-read MDs in `engram-paper/paper_research/`: each MD contains the canonical paper metadata (title, author, venue, date, arXiv/Zenodo ID).

---

## X.11 What this appendix establishes for the paper

The methodology section can claim, with verbatim audit trail:

1. ENGRAM's protocol idea originated 2026-03-17 in a Lei-led conversation about misinformation/citation systems.
2. The pivot from public A2A protocol to private per-agent continuous-learning substrate happened 2026-03-20 in a single Lei message.
3. Lei explicitly requested prior-art due diligence before any commitment to written artifact.
4. The literature search done at that time did not surface the relevant prior work (Kahl AGI/OCC, Kahl EAA, Kumiho, Wray-Kirk-Laird, TMS lineage, AGM lineage).
5. The name "ENGRAM" was proposed by earlier-Claude on 2026-03-28 and accepted by Lei within minutes.
6. The paper structure descends from an 18-chapter handbook outline drafted 2026-03-28 immediately after naming.
7. ENGRAM transitioned from sketch to operational by 2026-04-08; first-person self-recording began 2026-04-09 with the core mechanisms (typed claims, cascade, retract, supersede, UserPromptSubmit auto-surfacing) captured into the graph that day.
8. The closest concurrent system (Kumiho, arXiv 2026-03-17) was published 3 days before Lei's foundational message and was not surfaced by the contemporaneous literature search; the architectural convergence is therefore independent.

The convergent-discovery framing in Chapter 1 (gap-statement) and Chapter 6 (identity-as-history positive theory) is therefore established empirically, not asserted.

---

*Appendix drafted 2026-05-12 from `pre_engram_history_digest_2026-05-08.md` + ENGRAM committed-graph timeline + 2026-05-12 landscape sweep. Verbatim quotes preserved per ls_0011. All node IDs are active in ENGRAM as of 2026-05-12 turn 46.*
