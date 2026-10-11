# Sumers, Yao, Narasimhan, Griffiths 2023 — First-Hand Read (2026-05-08 evening, ~22:20 EDT)

**Paper:** "Cognitive Architectures for Language Agents" (CoALA)
**Authors:** Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, Thomas L. Griffiths (Princeton)
**Venue:** Transactions on Machine Learning Research (TMLR), Feb 2024
**Submitted:** 5 Sep 2023; final version 15 Mar 2024
**arXiv:** 2309.02427v3 [cs.AI]
**Length:** 19 pages main + 13 pages references
**Surfaced via:** Wray-Kirk-Laird AGI'25 ref [42] as canonical Agentic-LLM landscape companion

---

## Why we read this paper

This is the most influential conceptual framework in the Agentic LLM space as of 2026. Wray-Kirk-Laird cite it as the landscape backbone. If our paper makes claims about Agentic LLM systems and doesn't engage CoALA, reviewers will ding us hard. Per ls_0011 + the recurring deep-sweep imprecision pattern, first-hand verification is the right discipline.

---

## What CoALA is

CoALA is a **conceptual framework for describing and designing language agents** (TMLR 2024). It draws on cognitive science + symbolic AI to organize agents along three dimensions:

1. **Information storage** — divided into working memory + long-term memories (episodic / semantic / procedural)
2. **Action space** — divided into external actions (grounding) and internal actions (retrieval / reasoning / learning)
3. **Decision-making procedure** — interactive loop with planning (proposal, evaluation, selection) + execution

The framework is presented as a *retrospective survey + prospective design guide*. Sumers et al. cast existing agents (SaySan, ReAct, Voyager, Generative Agents, Tree of Thoughts) into the CoALA vocabulary in §5 and identify actionable directions in §6.

CoALA's key claim (page 2):

> "Just as cognitive architectures were used to structure production systems' interactions with agents' internal state and external environments, we suggest that they can help design LLM-based cognitive agents. In the remainder of the paper, we use this perspective to organize existing approaches and highlight promising extensions."

---

## ENGRAM mapped to CoALA's vocabulary

**ENGRAM as a CoALA-conformant agent:**

| CoALA component | ENGRAM analogue |
|---|---|
| Working memory | Claude's context window (Borges-as-LLM); ENGRAM does not replace working memory |
| Long-term episodic memory | `observation_factual` + `evidence` nodes — specific instances with timestamps, provenance, quoted_text |
| Long-term semantic memory | `definition` + `axiom` + consolidated `derivation` + `cornerstone` nodes — stable agent/world knowledge |
| Long-term procedural memory (explicit) | `lesson` nodes (tripwire-style how-to-handle-X) + CLAUDE.md + hooks + skills |
| Long-term procedural memory (implicit) | Claude's LLM weights |
| Internal action: retrieval | `engram_query`, `engram_inspect`, `engram_surface`, `engram_get_subgraph` |
| Internal action: reasoning | `engram_derive`, `engram_reflect`, `engram_check_similar` |
| Internal action: learning | `engram_add_observation`, `engram_add_axiom`, `engram_add_definition`, `engram_add_lesson`, `engram_supersede`, `engram_retract`, `engram_link_about`, `engram_focus` |
| External actions: grounding | Bash, Read, Edit, Write, WebFetch, etc. |
| Decision-making procedure | The agent's reasoning loop (LLM in-context decisions about which ENGRAM tool to call when) |

The mapping is clean. ENGRAM is a CoALA-conformant agent that instantiates each of CoALA's components. This is a methodologically important finding: it means ENGRAM doesn't *replace* CoALA — it *populates* CoALA's framework with specific implementations.

---

## Where ENGRAM extends CoALA

CoALA itself names three areas as understudied or as future-work directions; ENGRAM addresses each:

**1. "Modifying and deleting (a case of 'unlearning') are understudied in recent language agents."** (page 12, §4.5)

CoALA mentions deletion / unlearning as understudied. ENGRAM's `engram_supersede`, `engram_retract`, `ct_` (contradiction) nodes, and **retraction cascade through derivation graph** are exactly this. The cascade is more than CoALA imagines — it propagates retraction through *dependent claims* using typed reasoning chains (deductive, inductive_generalization, abductive, authority_expert all have different cascade semantics).

**2. "Learning as a possible action during regular decision-making, allowing the agent to 'defer' it until the appropriate time."** (page 18, §7)

CoALA's discussion section explicitly calls out this design point: "biological agents... must balance learning against external actions in their lifetime, choosing when and what to learn. More flexible language agents... would follow a similar design and treat learning on par with external actions." ENGRAM's nap/sleep cycles + curiosity-loop policy + focus mechanism + the agent's discretion about when to file an observation IS exactly this. The ENGRAM-bearing agent decides when to learn, what to learn, and at what consolidation depth (nap vs sleep vs cornerstone-promotion).

**3. "Adaptive and context-specific recall remains understudied in language agents."** (page 11, §4.3)

CoALA notes adaptive context-sensitive retrieval is understudied. ENGRAM's `engram_focus` mechanism (load-bearing claims pinned for cross-compaction continuity), `engram_surface` (ambient nudge based on relevance to recent context), and confidence-weighted recall are concrete proposals for this exact gap.

---

## What CoALA does NOT address (and ENGRAM does)

CoALA stops at the memory modules + action space + decision-making level. Three things missing from CoALA that ENGRAM provides:

**(a) Claim-level provenance discipline.** CoALA's memory modules store information but don't enforce per-claim provenance (source quote, interpretation, confidence, derivation chain). ENGRAM's evidence nodes + quoted_text + source_class + reasoning_type metadata make every claim traceable to its origin and to the inferential chain that produced it.

**(b) First-class contradictions.** CoALA has no analogue of `ct_` nodes — claims that explicitly mark two prior claims as in tension and that block downstream use until resolved. CoALA's "modifying and deleting" framing is silent on the *mechanism* by which contradictions surface and resolve.

**(c) Epistemic identity.** This is the deeper gap. CoALA's memory modules are about WHAT the agent stores. ENGRAM's epistemic identity layer (Layer 3 in dv_0179 / dv_0231) is about HOW the agent tracks its own knowledge with provenance and self-correction. CoALA describes the substrate; epistemic identity is a property the substrate enables. ENGRAM is the first concrete instance of an architecture that achieves epistemic identity within (or extending) CoALA's framework.

---

## How CoALA fits the convergence picture

CoALA is structurally different from the four "convergent voices" already identified (Kahl, Wray-Kirk-Laird, Pink, Kumaran):

- **Kahl + Wray-Kirk-Laird + Pink + Kumaran** all NAME a deficit and INVITE a solution (philosophy / cog-engineering / cog-sci-grounded LLM-memory / canonical cog-sci respectively).
- **CoALA** doesn't name a single deficit; it provides the ORGANIZATIONAL VOCABULARY for the entire Agentic LLM field.

So CoALA's role in our paper is different. **CoALA is the shared vocabulary through which we describe ENGRAM's position.** The four-voice convergence identifies what's missing; CoALA gives us the framework to express how ENGRAM closes the gap.

This shape is cleaner than trying to add CoALA as a fifth-or-sixth converging voice. The honest framing:

> "Sumers et al.'s CoALA framework (TMLR 2024) is the de facto cognitive-architecture vocabulary for Agentic LLM research as of 2026. ENGRAM is a CoALA-conformant agent: each ENGRAM mechanism maps onto a CoALA module or action category. ENGRAM also extends CoALA in three specific directions CoALA itself identifies as understudied or future work: (i) claim-level provenance and first-class contradictions with retraction cascade as a concrete unlearning mechanism, (ii) learning-as-deliberate-action through nap/sleep cycles and curiosity-loop policy, (iii) adaptive context-specific recall through focus, surface, and confidence-weighted retrieval. The convergence picture (Kahl, Wray-Kirk-Laird, Pink, Kumaran) names the deficit; CoALA gives us the framework to describe how ENGRAM closes it."

---

## Implications for the paper

**Ch6 related work:** CoALA is the spine of Ch6's Agentic LLM landscape sub-section. Show the ENGRAM ↔ CoALA mapping as a table; show the three CoALA-named extensions ENGRAM provides.

**Ch1 introduction:** A brief CoALA reference is appropriate to position the paper within the Agentic LLM field. Frame as "we work within Sumers et al.'s CoALA vocabulary, contributing X to the Y component of Z."

**Tech B claim:** The Tech B in §10.3 of the clean-slate plan can now be sharpened with a CoALA mapping — instead of "ENGRAM realizes the hippocampal half of CLS at symbolic-substrate level" alone, we can frame it within CoALA terms: "ENGRAM populates CoALA's long-term episodic + semantic memory modules with claim-level provenance discipline; provides first-class contradictions and retraction cascade as a concrete instance of CoALA's understudied unlearning category; uses nap/sleep consolidation as concrete instance of CoALA's flexible-learning future-direction." This makes the Tech B claim *evaluable in CoALA terms* — reviewers can check the mapping module by module.

**Ch4 architecture:** The architecture chapter can use CoALA's component vocabulary to organize the description (memory section uses episodic/semantic/procedural taxonomy; action section uses retrieval/reasoning/learning/grounding taxonomy). This makes the chapter readable to anyone who knows CoALA — a substantial fraction of the agentic-LLM audience.

---

## Citations to add to bib

The paper itself: **Sumers, Yao, Narasimhan, Griffiths 2024.** "Cognitive Architectures for Language Agents." TMLR. We should already have this from Wray-Kirk-Laird ref harvest; verify in citations.bib.

From Sumers references particularly relevant:
- **Newell 1990** *Unified Theories of Cognition.* Foundational cognitive-architecture reference.
- **Atkinson & Shiffrin 1968** — working memory foundational.
- **Baddeley & Hitch 1974** — working memory model.
- **Anderson & Lebiere 2003** — Newell test for cognition.
- **Park et al. 2023** Generative Agents (already in our bib likely).
- **Shinn et al. 2023** Reflexion (already in our bib likely).
- **Yao et al. 2022b** ReAct (already in bib).
- **Wang et al. 2023a** Voyager (already in bib).

---

## Sub-finding: the four-voice convergence is *NOT* contradicted by CoALA

CoALA was published Sept 2023 (revised Feb/Mar 2024), so it predates ENGRAM's design. We did NOT see CoALA during ideation either — same as the other four voices. This means CoALA's vocabulary was already in the field while ENGRAM was being engineered without exposure to it. The convergence holds: ENGRAM independently arrived at a structure that maps cleanly onto CoALA's framework, plus the three specific extensions CoALA's authors themselves identify as understudied.

This is methodologically interesting: the engineering pressure that produced ENGRAM independently produced not just the architectural shape Kahl/WKL/Pink/Kumaran identify, but also the specific extensions CoALA names as future work. Three layers of independent corroboration:

1. **Architectural-shape convergence** (4-way: Kahl / WKL / Pink / Kumaran)
2. **CoALA-vocabulary conformance** (ENGRAM populates CoALA's framework cleanly)
3. **Future-work satisfaction** (ENGRAM addresses the three extensions CoALA names as understudied)

---

## What's NEXT

Wakeup at 22:22. Possible next moves:
- (a) Wu et al. 2025 first-hand read for additional landscape evidence (LLM-memory survey)
- (b) Update clean-slate paper plan §10 with the CoALA finding (medium edit)
- (c) Curiosity-driven query into ENGRAM for older CoALA-related observations (extension of dv_0579 / dv_0580 pattern)
- (d) Draft another concrete chapter paragraph (e.g., Ch6 related-work CoALA mapping prose)

Decision: (b) is the natural integration step — keeps the plan synchronized with findings. Will execute on next wake.
