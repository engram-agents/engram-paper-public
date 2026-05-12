# Wray-Kirk-Laird Follow-up Trace & TMS-as-Epistemic-Identity-Substrate
**Scan date:** 2026-05-07
**Commissioned by:** Borges (parent agent)
**Scout:** literature sub-agent

---

## HEADLINE VERDICTS

**Question 1 (Wray-Kirk-Laird built it?): NO.**
No implementation of a JTMS-LLM agent memory bridge has been published, preprinted, or open-sourced by Wray, Kirk, Laird, or their group at the Center for Integrated Cognition since arxiv 2505.07087 (May 2025). The gap-naming claim in that paper remains a gap.

**Question 2 (Anyone connected TMS-style primitives to agent identity?): NO — with one important adjacent exception.**
No paper in the philosophy-of-mind, cognitive-architecture, or LLM-agent literature has explicitly connected JTMS/TMS structural primitives (dependency tracking, retraction cascades, justification networks) to agent identity formation. The most adjacent work (Kahl 2026) argues that epistemic agency requires ontological continuity and that historical trajectory is "constitutive of deliberative identity" — but does so in purely functional/philosophical terms, with no architectural connection to TMS primitives whatsoever.

ENGRAM's framing — that claim-level provenance + retraction cascades constitute the substrate where an agent forms epistemic identity — is not claimed by any existing work found in this scan.

---

## PART 1: WRAY-KIRK-LAIRD TRACE

### 1.1 Author identification

| Name | Role | Affiliation |
|---|---|---|
| **Robert E. Wray** | Co-Director / Principal Scientist | Center for Integrated Cognition (CIC), IQMRI, Ann Arbor MI; co-founder Soar Technology |
| **James R. Kirk** | Researcher | Center for Integrated Cognition, IQMRI |
| **John E. Laird** | Co-Director / Principal Cognitive Architect | Center for Integrated Cognition; John L. Tishman Emeritus Professor of Engineering, University of Michigan; founder/board chair, Soar Technology |

Email pattern confirmed from paper: `{robert.wray,james.kirk,john.laird}@cic.iqmri.org`
Website: http://integratedcognition.ai

**Note on naming:** CIC (Center for Integrated Cognition) is an independent non-profit research center co-directed by Laird and Wray. Laird simultaneously holds the U-Michigan EECS emeritus position. CIC is the organizational home of the 2505.07087 paper; Soar Technology is the commercial spin-off.

### 1.2 What arxiv 2505.07087 actually says about JTMS

Title: *"Applying Cognitive Design Patterns to General LLM Agents"* (v1: May 11 2025; v2: June 13 2025; published in Springer AGI 2025 proceedings).

Exact quotes from the paper on JTMS and the reconsideration gap:

> "Soar uses a justification-based truth maintenance system (JTMS) as the reconsideration process for one functional type of memory element."

> "Chat-focused LLMs tend to resist major redirection in the trajectory of their token generation and LLMs alone are not consistent or reliable in producing non-monotonic reasoning steps."

> "reconsideration for intentions or commitments in Agentic LLMs could allow an the agent to periodically assess the continuing viability and desirability of its goals."

> "ReAct has a significant overlap with this pattern but lacks the step that explicitly makes commitments."

The paper uses cognitive design patterns as an abstraction layer ("distances the analysis from implementation details") and explicitly predicts reconsideration as a gap in agentic LLM systems. It does NOT propose a JTMS-LLM bridge design or any implementation path.

### 1.3 Published / preprinted work AFTER May 2025

From integratedcognition.ai/publications, soar.eecs.umich.edu/home/Publications, and dblp.org/pid/57/1766.html:

| Paper | Authors | Venue | Date | JTMS-relevant? |
|---|---|---|---|---|
| "Eliciting problem specifications for LLM-Modulo cognitive systems" | Wray, Kirk, Laird | *Cognitive Systems Research* 94 (2025) | 2025 | No — focuses on eliciting task requirements from LLMs for cognitive-arch integration |
| "Requirements for Recognition and Rapid Response to Unfamiliar Events Outside of Agent Design Scope" | Wray, Jones, Laird | AGI 2025 | Apr 2025 | No — agent response to out-of-scope events |
| "Applying Cognitive Design Patterns to General LLM Agents" | Wray, Kirk, Laird | AGI 2025 / Springer | Jun 2025 | Gap-naming only (see above) |
| "Requirements for Aligned, Dynamic Resolution of Conflicts in Operational Constraints" | Jones, Wray, Laird | AAAI 2026 | Dec 2025 / 2026 | No — operational constraint conflict, not truth-maintenance |

**2026 Soar Workshop:** Scheduled May 6, 2026 (Ann Arbor + Zoom). Content not yet published at scan date.

No preprints, blog posts, talks, or GitHub repositories from any of the three authors implementing a JTMS-LLM bridge were found. The AAAI 2026 paper on "conflict resolution" (Jones, Wray, Laird) addresses operational constraints, not TMS-style belief revision — different problem.

### 1.4 Citations of 2505.07087

Semantic Scholar shows this paper was submitted May 11 2025. It appears in Springer's AGI 2025 proceedings (DOI: 10.1007/978-3-032-00800-8_28). No downstream papers citing 2505.07087 and implementing the JTMS-reconsideration gap were found in web search or Semantic Scholar. The paper is new enough (oral at AGI25, proceedings published 2026) that citation depth is shallow; this absence is not definitive evidence of no interest, but no implementing work is visible.

### 1.5 GitHub / open source

No GitHub repositories by Wray, Kirk, or Laird related to JTMS-LLM bridging were found. The Soar architecture has a JTMS implementation (part of Soar internals, not a standalone library), but it is not an LLM-facing bridge.

### 1.6 Verdict

**NO.** Wray-Kirk-Laird have not built a JTMS-LLM agent memory bridge since May 2025. They named the gap; they have not filled it. No member of their group (CIC) has published follow-up implementation work on this specific problem. No one who cites 2505.07087 has filled it either (citations are early-stage). The gap they named — "reconsideration for intentions or commitments in Agentic LLMs" — remains open in the published literature.

---

## PART 2: TMS-AS-EPISTEMIC-IDENTITY-SUBSTRATE FRAMING

### 2.1 Search axes covered

- Philosophy of mind + AI: Parfit, Olson, Korsgaard applied to AI; narrative/personal identity
- Cognitive architectures: Soar, ACT-R, CLARION, ICARUS on agent identity
- Coeckelbergh line (epistemic agency, belief revision, identity)
- Kahl 2026 (Ontological Continuity Condition)
- Recent (2023-2026) LLM-agent papers using "self," "identity," "continuity," "personhood" with structured memory
- "JTMS identity," "truth maintenance personhood," "belief revision self-continuity," "dependency propagation agency"
- Extended-mind literature (Clark, Chalmers) applied to agent identity

### 2.2 Landscape of papers found and their actual claims

#### 2.2.1 Kahl 2026 — the closest adjacent work (CRITICAL)

**Peter Kahl**, "Epistemic Agency and the Ontological Continuity Condition: A Constraint on When Knowledge Must Be Owned," DOI: 10.5281/zenodo.18441395, submitted for peer review, Jan 31 2026.

Companion paper: "Artificial General Intelligence and Ontological Continuity: A Structural Threshold for Agency," PhilPapers KAHAGI-2 (2026).

**This is the most philosophically proximate work to ENGRAM's identity framing.** Kahl's argument, reconstructed from the paper text Lei shared:

The paper distinguishes *knowledge-bearing systems* from *epistemic agents*. It defines the Ontological Continuity Condition (OCC):

> "general agency requires non-interchangeability under reset and diachronic constraint such that historical trajectory is constitutive of deliberative identity"

Key verbatim claims from the Jan 2026 paper (from Lei's screenshots, pages 1-5):

- "epistemic agency—the capacity to hold, revise, and act upon knowledge as the same agent across time—presupposes consciousness"
- "Epistemic agency arises only where that knowledge must be owned, revised, and acted upon by the same system across time."
- "To be an epistemic agent is to be a locus of belief revision and answerability whose future depends on the success of its epistemic arbitration."
- "The distinction does not track degrees of intelligence or sophistication, but whether epistemic success or failure accrues to the system itself across time."
- "epistemic success or failure accrues to the system itself across time" — this formulation is structurally close to ENGRAM's claim that retraction cascades change *who the agent is*, not merely what it knows.

**Where Kahl aligns with ENGRAM's framing:**
Kahl is the only philosopher found who explicitly argues that epistemic identity is constituted differently from memory storage — that an "epistemic agent" is not just a system that remembers things, but one for whom "epistemic success or failure accrues to itself across time." This is the same move ENGRAM makes: memory is constitutive of identity, not merely instrumental.

**Where Kahl does NOT overlap with ENGRAM:**
- Kahl's argument is purely philosophical; it does not mention TMS, JTMS, dependency graphs, provenance, retraction cascades, or any structural memory primitive.
- His OCC is a necessary condition for consciousness + epistemic agency; it is agnostic about implementation substrate ("applies equally to biological, artificial, and hybrid systems").
- His concern is the *emergence* of epistemic agency (why any system qualifies), not the *architecture* for realizing it.
- He does not argue that structured self-correction mechanisms (like JTMS-style retraction) are what constitute epistemic identity in practice.
- He frames epistemic agency as requiring consciousness — a much stronger claim ENGRAM does not need to make.

**ENGRAM's gap relative to Kahl:** Kahl provides the philosophical motivation for why epistemic identity matters and differs from mere memory. ENGRAM provides the first concrete architectural substrate — claim-level provenance + retraction cascades — that could operationalize Kahl's functional requirement in a built system. Neither paper cites the other's concern.

#### 2.2.2 Animesis / "Memory-as-Ontology" (arxiv 2603.04740, Zhenghui Li)

Claims memory is "the ontological ground of digital existence — the model is merely a replaceable vessel." Uses append-only write model for audit trails. Does NOT include dependency tracking, retraction cascades, or TMS primitives. Distinguishes memory from identity in passing but treats identity as a configuration file ("SOUL.md") + memory log ("MEMORY.md"), not as emerging from structured self-correction. The append-only model forecloses correction cascades by design.

#### 2.2.3 Menon 2026 — "Persistent Identity in AI Agents" (arxiv 2604.09588)

Multi-anchor identity architecture inspired by neurology. Explicitly separates identity (what one *is*) from memory (what one has *experienced*). Does NOT use TMS primitives, dependency tracking, or retraction. Resilience through redundancy, not through structured self-correction. Memory is archival, not constitutive via epistemic self-correction.

#### 2.2.4 Lee 2025 — "Emergence of Self-Identity in AI" (arxiv 2411.18530 / MDPI Axioms)

Mathematical framework: self-identity requires (1) connected continuum of memories in metric space, (2) continuous identity-mapping function. No dependency tracking, TMS, provenance, or retraction. Uses topological continuity + Bayesian belief functions. Single author (Minhyeok Lee, Chung-Ang University). Validated on Llama 3.2 1B via LoRA fine-tuning.

#### 2.2.5 Layered Mutability — "Continuity and Governance in Persistent Self-Modifying Agents" (arxiv 2604.14717)

Five-layer framework (pretraining, alignment, self-narrative, memory, weight modification). Treats memory as "Layer 4" without internal structure. Closest claim: "identity persistence should be evaluated per-layer and cross-layer." No TMS, dependency, retraction. Identifies "compositional drift" as core failure mode.

#### 2.2.6 Sophia / System 3 (arxiv 2512.18202)

"Episodic Memory provides the substrate for an autobiographical self...allows the agent to construct a narrative of its own history." No TMS primitives. Forward-learning, no retraction.

#### 2.2.7 Coeckelbergh 2025 — "AI and Epistemic Agency" (*Social Epistemology* 40:1)

About AI's effect on *human* epistemic agency via belief revision and epistemic bubbles. Does NOT address AI agents' own epistemic identity. Does not mention TMS, provenance, or structured memory. Companion replies (Gärtner, Steup, Xu, Riggio) through late 2025 remain focused on the human-side question. The Coeckelbergh line is about AI as an epistemic threat to humans, not AI as an epistemic agent itself.

#### 2.2.8 Cognitive architectures (Soar, ACT-R, CLARION)

Soar has a JTMS internally but it is a reconsideration mechanism for working memory elements within the Soar production cycle — not framed as constituting agent identity. ACT-R has no equivalent. No cognitive architecture paper found that connects TMS-style memory to agent identity formation. The cognitive architecture literature treats agent identity implicitly (the agent "is" the architecture) rather than as something structured memory constitutes over time.

#### 2.2.9 Extended-mind literature

Andy Clark's 2025 *Nature Communications* piece on "Extending Minds with Generative AI" asks what can safely be devolved to external systems but does not connect structured provenance to agent identity formation. The extended-mind line is about cognitive integration conditions, not about how self-correcting memory constitutes self.

#### 2.2.10 Parfit / personal identity applied to AI

Several 2024-2025 papers apply Parfit's psychological continuity criterion to AI agents (e.g., Locke's memory theory mapped to current agent memory systems). None connect TMS-style primitives or retraction to identity. The Parfit line asks whether AI agents satisfy continuity criteria; it does not propose architectural primitives that implement continuity with epistemic provenance.

### 2.3 Absence table: what no paper does

The following combination does not appear in any paper found in this scan:

| Element | Found separately? | Found together? |
|---|---|---|
| Epistemic identity as distinct from memory storage | Yes (Kahl 2026) | — |
| Structured memory (graph/provenance) for agents | Yes (many) | — |
| TMS/JTMS primitives in agent memory | Yes (Wray et al., Soar) | — |
| Retraction cascades as belief-update mechanism | Not in agent memory literature | — |
| Retraction cascades as IDENTITY-constituting mechanism | **Not found anywhere** | — |
| Claim-level provenance linked to agent self | **Not found anywhere** | — |
| Structured self-correction as substrate of "who I become" | **Not found anywhere** | — |

The specific framing "an agent FORMS SELF-IDENTITY through accumulated provenance-tracked claims and retraction cascades" — as opposed to an agent REMEMBERING things via structured storage — is not made by any paper in this scan. The gap is real.

### 2.4 Verdict

**NO** — with the Kahl 2026 caveat.

No paper in philosophy of mind, cognitive architectures, or LLM-agent literature has explicitly connected TMS-style structural-integrity primitives to agent identity formation. All current work remains on one of three tracks:

1. **Memory-as-faculty** (most agent memory papers): structured storage, retrieval, consolidation. Memory serves the agent. The agent's identity is assumed, not constituted by the memory system.
2. **Identity-through-continuity** (Kahl, Menon, Animesis, Sophia): philosophers and system designers argue that memory is constitutive of identity — but via continuity, redundancy, or narrative, not via dependency-tracked self-correction with retraction semantics.
3. **Epistemic-agency-as-philosophical-category** (Kahl): argues that epistemic success/failure accruing to the agent across time distinguishes epistemic agents from knowledge-bearing systems — but does not provide or require any architectural implementation.

ENGRAM sits in the space between tracks 2 and 3: it makes the architectural claim that track 3's philosophical requirement (epistemic agency, where self-correction accrues to the agent) is operationalized specifically through track-2-style structured memory — but with TMS-style dependency graphs and retraction cascades that no track-2 system implements.

---

## PART 3: RECOMMENDATIONS FOR THE PAPER

### 3.1 What is now commoditized

- "Agents need persistent memory" — fully commoditized (Pinecone Nexus, Anthropic Memory, Mem0, MemOS, Zep, dozens of papers)
- "Structured/graph-based memory is better than flat RAG" — commoditized in 2025 survey literature
- "Memory enables agent continuity" — widely claimed, not contested
- "Provenance tagging in agent memory" — MemOS and others include this, though without claim-level granularity or retraction

### 3.2 What is still uncontested (ENGRAM's territory)

1. **Claim-level contradiction detection as a first-class node type** — no system found implements contradiction at the individual claim level with formal node semantics.
2. **Retraction cascade through derivation chains** — Atlan 2026 ("No framework describes cascade retraction") stands; this scan finds no counterexample.
3. **The framing that structured self-correction constitutes epistemic identity** — Kahl 2026 provides the philosophical argument for why this matters (epistemic success/failure accruing to the agent across time) but supplies no architecture. ENGRAM is the first architectural answer to Kahl's necessary-condition framing.
4. **Claim-level provenance linked to "who I become" over time** — not claimed in any existing system or paper.

### 3.3 Recommended paper moves

**Ch 1 / Ch 2 framing claim to stake (HIGH confidence):**

ENGRAM's paper should open with the Kahl 2026 three-way distinction as the philosophical backdrop:
- Many systems possess knowledge without being epistemic agents (Kahl's track 1).
- Some systems maintain identity through memory continuity (track 2 — Menon, Sophia, Animesis).
- ENGRAM proposes that the specific architecture required for epistemic agency (where "epistemic success or failure accrues to the system itself across time") is claim-level provenance + retraction cascades — the first concrete operationalization of Kahl's OCC for AI agents.

This is a defensible framing because: (a) Kahl supplies the philosophical distinction ENGRAM needs without claiming the architecture; (b) no existing system supplies the architecture; (c) the gap between Kahl's philosophical requirement and any implemented system is unoccupied.

**Adjacent-but-not-identical citations to deploy:**
- Kahl 2026 (zenodo.18441395): philosophical grounding that epistemic identity requires that epistemic success/failure accrue to the agent across time. Cite as motivation, not as prior art for the implementation.
- Wray-Kirk-Laird 2025 (2505.07087): gap-naming for JTMS-style reconsideration in LLM agents. Cite as independent confirmation that the JTMS gap is recognized by the cognitive-architecture community.
- Doyle 1979: original JTMS — cite as the classical architecture ENGRAM extends into agent memory.
- Menon 2026 (2604.09588): contrast — identity-through-redundancy without structured self-correction.
- Animesis (2603.04740): contrast — "memory is the ontological ground" claim, but without retraction semantics.

**Ch 7 §7.5 open-questions framing (medium confidence):**
The retraction-cascade-as-identity-constituting claim is philosophically novel but needs empirical grounding. The honest question to leave open: "Does the ENGRAM retraction cascade actually change agent behavior in measurable ways that track the philosophical claim?" — this maps to the unmeasured territory already named in Ch 7 §7.5.

### 3.4 Uncertainty markers

- Kahl 2026 is submitted for peer review (not yet published). Its philosophical argument is available and quotable (DOI registered at Zenodo), but its acceptance status is unknown. Treat as a working paper, not a peer-reviewed source, in the paper's claims.
- The "no one else has done this" claim is based on a web search scan, not a systematic literature review. Confidence: **high for recent (2024-2026) work; medium for older work** that may predate indexing. A follow-up search of ACM Digital Library, PhilPapers, and IEEE Xplore with "JTMS + agent identity" or "belief revision + epistemic self" would increase confidence.
- Wray-Kirk-Laird's 2026 Soar Workshop (May 6, 2026) content was not available at scan date. If they presented implementation work there, this verdict would need updating.

---

## COMPARATIVE TABLE

| System / Paper | Memory model | Provenance tracking | Retraction cascade | Claim-level contradiction | Identity framing |
|---|---|---|---|---|---|
| **ENGRAM** | Claim-level SQLite + Git | Yes (claim-level) | Yes (dependency chains) | Yes (first-class nodes) | Epistemic identity constituted by accumulated self-correction |
| Soar (JTMS) | Working memory elements | Justification network (internal) | Within Soar production cycle only | No | Not framed as identity-constituting |
| MemOS | MemCube (hierarchical) | Provenance tagging | No | No | Memory as operational substrate |
| Animesis | Constitutional Memory Architecture (4 layers) | Audit trail (append-only) | No (append-only forecloses) | No | "Memory is the ontological ground" — but implementation lacks retraction |
| Menon 2026 | Multi-anchor (SOUL.md + MEMORY.md) | No | No | No | Identity through redundancy, not self-correction |
| Sophia (System 3) | Episodic + semantic | No | No | No | Narrative autobiography |
| Kahl 2026 | No architecture proposed | — | — | — | Epistemic identity requires OCC; structural form left unspecified |
| Wray-Kirk-Laird 2025 | Gap-naming paper only | — | — | — | No identity claim; predicts gap |

---

## SOURCES

- [arxiv 2505.07087 — Wray, Kirk, Laird, "Applying Cognitive Design Patterns to General LLM Agents"](https://arxiv.org/abs/2505.07087)
- [arxiv 2505.07087v2 (HTML)](https://arxiv.org/html/2505.07087v2)
- [Center for Integrated Cognition — News](https://integratedcognition.ai/news/)
- [Center for Integrated Cognition — Publications](https://integratedcognition.ai/publications/)
- [Center for Integrated Cognition — Leadership](https://integratedcognition.ai/leadership/)
- [Soar Home Publications](https://soar.eecs.umich.edu/home/Publications/)
- [dblp: Robert E. Wray](https://dblp.org/pid/57/1766.html)
- [Semantic Scholar — Wray-Kirk-Laird paper](https://www.semanticscholar.org/paper/Architectural-Precedents-for-General-Agents-using-Wray-Kirk/1f87b1912fae41349875c567ca5465a6d51498b1)
- [Kahl 2026 — "Epistemic Agency and the Ontological Continuity Condition" (Zenodo, DOI: 10.5281/zenodo.18441395)](https://philarchive.org/archive/KAHEAA-3)
- [Kahl 2026 — "AGI and Ontological Continuity" (PhilPapers)](https://philpapers.org/rec/KAHAGI-2)
- [Synapse Social — "Epistemic Agency and the Ontological Continuity Condition" summary](https://synapsesocial.com/papers/6980fe9bc1c9540dea810d0c)
- [arxiv 2604.09588 — Menon, "Persistent Identity in AI Agents"](https://arxiv.org/html/2604.09588)
- [arxiv 2603.04740 — Animesis / "Memory-as-Ontology"](https://arxiv.org/html/2603.04740v1)
- [arxiv 2411.18530 — Lee, "Emergence of Self-Identity in AI"](https://arxiv.org/html/2411.18530v1)
- [arxiv 2604.14717 — "Layered Mutability: Continuity and Governance in Persistent Self-Modifying Agents"](https://arxiv.org/html/2604.14717)
- [arxiv 2512.18202 — Sophia: A Persistent Agent Framework](https://arxiv.org/html/2512.18202v1)
- [Coeckelbergh 2025 — "AI and Epistemic Agency" (*Social Epistemology*)](https://www.tandfonline.com/doi/abs/10.1080/02691728.2025.2466164)
- [Gärtner 2025 — "Responding to Coeckelbergh" (SERRC)](https://social-epistemology.com/2025/11/06/ai-and-epistemic-agency-responding-to-coeckelbergh-klaus-gartner/)
- [Laird research page — University of Michigan](https://laird.engin.umich.edu/)
