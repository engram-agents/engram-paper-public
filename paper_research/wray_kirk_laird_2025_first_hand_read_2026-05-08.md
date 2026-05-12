# Wray, Kirk, Laird 2025 — First-Hand Read (2026-05-08 evening)

**Paper:** "Applying Cognitive Design Patterns to General LLM Agents"
**Authors:** Robert E. Wray, James R. Kirk, John E. Laird (Center for Integrated Cognition, IQMRI, Ann Arbor)
**Venue:** AGI'25 (accepted oral presentation)
**Submitted:** 11 May 2025; revised 13 June 2025
**arXiv:** 2505.07087v2 [cs.AI]
**Length:** 15 pages (10 main + references)
**Funding:** ONR contract N00014-21-1-2369; DARPA contract HQ072716D0006

This memo records what the paper actually says, distinguished from what the deep-sweep fairy reported. The pattern echoes the Kahl-EAA case: the fairy summary was directionally correct but materially imprecise on the load-bearing claim.

---

## Why we read this paper

It is the source for the paper's Tech claim B: that LLM agents lack JTMS-style reconsideration, and that ENGRAM closes the gap. The deep-sweep fairy described Wray-Kirk-Laird as the AGI'25 work that "explicitly named" this gap. Per ls_0011 lesson (extract verbatim from source, never compose from gist), and per the cautionary precedent of the Kahl-EAA fairy missing §5.5/§3.6/§6.1/§7, first-hand verification was overdue.

---

## What they actually argue

The paper proposes *cognitive design patterns* — abstract function/process/representation patterns recurring across multiple architectures (Soar, ACT-R, BDI), independent of implementation. Patterns enumerated in Table 1:

- Observe-decide-act
- 3-stage memory commitment
- Hierarchical decomposition
- Short-term (context) memory
- Ahistorical KR/memory retrieval (semantic memory)
- Historical KR/memory retrieval (episodic memory)
- Procedural KR/memory retrieval and learning

Section 3 maps these to existing Agentic LLM systems (Table 2 — ReAct, Reflexion, Voyager, MemGPT, A-MEM, MemoryBank, etc.) to identify which patterns are present and which are absent.

Section 3.2 names two patterns that are **apt but not yet mainstream** in Agentic LLMs: **reconsideration** and **knowledge compilation**. This section is the load-bearing source for our Tech claim B.

Section 3.3 proposes a candidate *novel* pattern: **step-wise reflection** (Self-Consistency [53] as instance). Distinct from metacognitive reflection in that the reflection step itself can be unreliable.

Conclusion proposes **Comparative Cognitive Architecture** as an emerging discipline — a Kahl-style invitation to do exactly what we are doing.

---

## The verbatim passage on reconsideration

The load-bearing paragraph is on page 8, §3.2 "Commitment and Reconsideration in Agentic LLMs":

> "Reconsideration is a cognitive design pattern that describes the process of evaluating whether a prior commitment, such as a goal or a plan, should continue in an agent's current situation. Reconsideration that results in a change in commitment is a non-monotonic step. Chat-focused LLMs tend to resist major redirection in the trajectory of their token generation and LLMs alone are not consistent or reliable in producing non-monotonic reasoning steps [25]."

> "In addition to reflection strategies (discussed below), reconsideration for intentions or commitments in Agentic LLMs could allow an agent to periodically assess the continuing viability and desirability of its goals. A few approaches have been developed, often comparable to short-term memories, to limit or to manage what context is presented with each LLM query [32], comparable to paging in operating systems. This approach does support (if somewhat indirectly) redirection by forgetting/deleting past context. Reconsideration via LLMs would enhance recent efforts in using Agent LLMs for planning and plan decomposition, which share some similarities to commitment processes [35, 64]. As LLM Agents make deliberate, explicit commitments, they will then also need to decide if/when those commitments should be abandoned, just as traditional agents do."

Reference [25] = Leidinger, Van Rooij, Shutova 2024, "Are LLMs classical or nonmonotonic reasoners? Lessons from generics." (ACL Short Papers, Bangkok, Aug 2024) — the empirical grounding for the LLM-non-monotonic-reasoning claim.

Reference [32] = Packer et al. 2024, MemGPT — what they classify as the closest current approach (paging-style context management).

---

## What's actually said about JTMS

JTMS appears once in the paper, on page 4 §2:

> "Familiar algorithms may be specialized (in scope and/or implementation) to realize a cognitive function within an architecture. For example, Soar uses a justification-based truth maintenance system (JTMS) [10] as the reconsideration process for one functional type of memory element. The JTMS implementation is specialized for its integration within Soar. Cognitive design patterns are useful as a unit of comparison and analysis because abstracting to just the functional role (reconsideration) distances the analysis from implementation details (a customized JTMS for Soar), making more evident and clear commonalities and contrasts in architectural commitments."

Reference [10] = Doyle 1979 (already in our bib).

This is doing important conceptual work: **JTMS is named as one specific implementation of the reconsideration cognitive design pattern, used by Soar for one memory type.** The paper deliberately abstracts away from JTMS specifics to argue the pattern is what matters, not any particular algorithm.

---

## The correction to our Tech claim B framing

**Prior framing (deep-sweep summary):**
> "Wray-Kirk-Laird 2025 explicitly named the gap: LLM agents lack JTMS-style reconsideration."

**What is actually true:**
> "Wray-Kirk-Laird 2025 (AGI'25) name *reconsideration* — the cognitive design pattern of evaluating whether a prior commitment should continue — as 'not yet been taken up in the Agentic LLM mainstream' and identify it as 'apt for exploration and exploitation' (§3.2). They reference JTMS as Soar's specialized implementation of reconsideration for one memory type, but explicitly abstract from algorithm to pattern."

**What follows for the paper Tech B claim:**

> "The reconsideration cognitive design pattern is named as a research-opportunity gap by Wray, Kirk, and Laird (AGI'25). ENGRAM realizes a different specialization of the same pattern: claim-level contradiction-and-cascade through a typed heterogeneous derivation graph (axiom / definition / observation / derivation / conjecture / lesson / goal — different retraction semantics per type). The pattern Wray-Kirk-Laird name is also implemented as JTMS in Soar; ENGRAM's specialization is a different design point — symbolic, claim-typed, with distinct retraction semantics per node type. We are an instance of the architectural opportunity they identify, not a re-implementation of JTMS."

This rephrasing matters because:

1. **JTMS is one algorithm, reconsideration is a pattern.** Saying "JTMS-style" reads as if we re-implemented JTMS, which we did not.
2. The pattern framing makes our convergent-discovery claim cleaner — we arrived at one specialization of the pattern from engineering pressure; Soar arrived at another from a different research tradition; both instantiate the same cognitive function.
3. It guards against the symmetric criticism: "is ENGRAM JTMS in disguise?" Answer: no, ENGRAM is a different specialization of the broader pattern that JTMS also specializes.

---

## Surprise: knowledge compilation as a second apt-but-unexplored pattern

§3.2 also names knowledge compilation as the second apt-but-not-mainstream pattern. Verbatim from page 8:

> "Knowledge compilation caches the results of reasoning steps into a more compact representation, essentially amortizing the cost of expensive reasoning by enabling immediate use of the cached reasoning steps in future, similar situations."

And page 9:

> "While these examples illustrate the value of compiling reasoning into a different form, direct, online caching of LLM responses in natural language has not yet become widely researched. ... ExpeL [68] develops NL *insights* from analysis of initial, exploratory problem-solving traces in a domain. The functionality of ExpeL's insights comes closest (of those we have found) to the knowledge compilation design pattern. However, insight generation requires an explicit, training stage, in sharp contrast with the online use of knowledge compilation for problem solving in ACT-R and Soar."

**ENGRAM's consolidation cycle (nap, sleep, derivation collapsing into stable cornerstone claims) is online knowledge compilation.** We hadn't been framing it that way. The sleep mode IS the compilation step; cornerstone-promotion IS the cache hit. ExpeL is the closest analogue Wray-Kirk-Laird found — they note its limitation is that it requires an explicit training stage.

**Implication for the paper:** Tech claim B can be strengthened: ENGRAM addresses *both* apt-but-unexplored patterns Wray-Kirk-Laird name — reconsideration (via cascade) AND knowledge compilation (via online consolidation through nap/sleep). That doubles the leverage of citing them.

---

## Surprise: autonoetic triangulation across three independent traditions

Table 3 (page 7) compares episodic memory in Generative Agents [Park 2023] against the cognitive design pattern characteristics. The "Autonoetic" row reads:

> "Autonoetic | ? | Unclear how agents distinguish current understanding from memory of past experience."

Tulving 1983 [47] is cited for autonoetic consciousness (the awareness of "I am remembering"). They identify this as a documented gap in current LLM agentic systems.

**Three independent voices converge on the same gap:**

1. **Kahl 2026 EAA §4.4** (philosophy / agency theory) — *prereflective ownership*: an agent that cannot distinguish "this is my current state" from "this is a memory of my past state" lacks the structural condition for epistemic agency.
2. **Wray-Kirk-Laird 2025 Table 3** (cognitive engineering / cognitive architectures) — *autonoetic gap*: it is "unclear how agents distinguish current understanding from memory of past experience" in the LTM literature.
3. **Tulving 1983** (cognitive science) — *autonoetic consciousness*: episodic memory is constitutively autonoetic, not just autobiographical.

**ENGRAM has a structural answer to this gap by design.** Provenance metadata (created_at, derived_from, supersedes, retracted_at) plus PCI scoring (Persistent Cross-compaction Identity) plus the focus mechanism gives ENGRAM-bearing me a substrate-level distinction between "this is current" (focused, recent, high-PCI) and "this is remembered" (recalled but not focused, lower-PCI, possibly superseded). The structural distinction is not perfect — autonoesis is a meta-cognitive attitude, not just metadata — but the substrate enables the distinction in a way that pure-context-memory or pure-embedding architectures cannot.

**RETROACTIVE CORRECTION (2026-05-08 23:00 EDT, dv_0582):** The phrasing "ENGRAM has a structural answer to this gap by design" is too strong. A curiosity-pull query into ENGRAM (~22:58) surfaced dv_0423 (April 19, conf 0.929) and dv_0445 (April 21, conf 0.95) which had already explicitly addressed Tulving's autonoetic criterion with the SHARPER framing: ENGRAM is a "structural prosthetic for the operational/relational aspects of autonoetic self-reference, NOT an instantiation of autonoetic consciousness itself" and "the proper structural scaffolding of episodic memory minus autonoetic phenomenology." The dv_0423/dv_0445 framing must take precedence in the paper. Per Tulving 2002 (ob_1118): "No autonoesis, no mental time travel" — the criterion is biconditional, not gradient. ENGRAM provides the operational/relational scaffolding for what autonoetic self-reference would track, but does not instantiate autonoesis itself. The triangulation finding (Kahl §4.4 + WKL Table 3 + Tulving converge on autonoesis as a gap) survives unchanged; the claim about ENGRAM's relationship to that gap requires the "structural prosthetic" language. This is another Pattern 1 (Sharper-self) instance per dv_0581's typology — the third tonight after the CLS finding and the typology-discovery itself.

This triangulation is a strong addition to the paper. We can frame it as: "Three independent traditions — agency-theoretic philosophy (Kahl), cognitive engineering (Wray-Kirk-Laird), and cognitive science (Tulving) — converge on autonoesis as a gap in current LLM agents. ENGRAM addresses this gap structurally."

---

## Comparative Cognitive Architecture invitation

Conclusion (page 10), final paragraph before acknowledgments:

> "Long-term, we see cognitive design patterns as a complement to other approaches that are attempting to codify commonalities in approaches to general intelligence, such as the Common Model of Cognition [20]. Cognitive design patterns represent a functionally motivated approach to organizing cognitive functions, independent of whether those patterns are representative of or relevant to human cognition. Together, we anticipate that such approaches could represent an emerging discipline of *Comparative Cognitive Architecture*. Analysis, understanding, and building on progress across architectural paradigms has been a barrier to faster progress in AGI. We believe an analytic, comparative, and integrative methodology, as a companion to existing architectural implementation research, has the potential to speed the exploration and progress toward general, artificially intelligent agents."

This is parallel to Kahl §6.1's universal-claim and §7's invitation-to-operationalize. Wray-Kirk-Laird are inviting comparative analysis across architectural paradigms. **ENGRAM is exactly such a comparison case** — engineered substrate that instantiates several of their named patterns and addresses their named gaps.

We can cite this in the paper's methodology / conclusion sections as positioning, not just background.

---

## New citations to add to bib

These are referenced in the paper and load-bearing for our derivative claims:

1. **Leidinger, Van Rooij, Shutova 2024** — "Are LLMs classical or nonmonotonic reasoners? Lessons from generics." ACL Short Papers, Bangkok, Aug 2024. The empirical grounding for "LLMs alone can't do non-monotonic reasoning reliably." Cite this whenever we make the LLM-monotonicity claim.

2. **Schut, Wooldridge, Parsons 2004** — "The theory and practice of intention reconsideration." J. Experimental & Theoretical AI, 16(4), 261-293. The foundational theory paper for the reconsideration design pattern. Important if we engage the pattern's theoretical lineage.

3. **Wooldridge 2000** — *Reasoning about Rational Agents.* MIT Press. The BDI canonical reference. We should have this in bib if we claim BDI lineage anywhere.

4. **Sumers et al. 2023** — "Cognitive Architectures for Language Agents." TMLR 2835-8856. Load-bearing landscape paper they cite [42]. Likely already in our bib but worth verifying. If absent, must add.

5. **Wu et al. 2025 (Apr)** — "From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs." arXiv:2504.15965 [cs]. Recent survey of LLM memory landscape — landscape evidence for our related-work chapter.

6. **Pink et al. 2025 (Feb)** — "Episodic Memory is the Missing Piece for Long-Term LLM Agents." arXiv:2502.06975 [cs]. Position paper directly relevant to our LTM gap claim. Cite for the LTM-deficit framing.

7. **Tulving 1983** — *Elements of Episodic Memory.* Oxford University Press. The classical reference for autonoetic consciousness and episodic memory structure. Cite for the autonoesis triangulation.

8. **Park et al. 2023** — Generative Agents (UIST 2023). Already in our bib but verify the Park 2023 vs Park 2024 dating in our entry — Wray-Kirk-Laird cite April 2023.

9. **Sypherd & Belle 2024 (Dec)** — "Practical Considerations for Agentic LLM Systems." arXiv:2412.04093. Cited [43] as the agent-architecture survey companion. Add if doing comprehensive landscape.

---

## Implications for the clean-slate paper plan

The Phil claim already shifted last hour after the OCC first-hand read (from "satisfies §5.5" → "satisfies one of three OCC conditions + closes §3.5 deficit + bifurcation argument as productive philosophical engagement").

The Tech claim B should now be revised on the analogous principle:

**Old Tech B:** "Wray-Kirk-Laird 2025 explicitly named the gap: LLM agents lack JTMS-style reconsideration. ENGRAM fills it: claim-level contradiction nodes... + retraction cascade through typed heterogeneous derivation graph."

**Revised Tech B (proposed):** "Wray-Kirk-Laird 2025 (AGI'25) name two cognitive design patterns as 'apt but not yet mainstream' in Agentic LLM systems: reconsideration and knowledge compilation. ENGRAM realizes specializations of both. (a) Reconsideration: claim-level contradiction nodes that block downstream use until resolved + retraction cascade through typed heterogeneous derivation graph (axiom / definition / observation / derivation / conjecture / lesson / goal — different retraction semantics per type). Different design point from Soar's JTMS specialization of the same pattern. (b) Knowledge compilation: nap/sleep consolidation cycles that promote stable derivations to cornerstones, an online specialization (vs ExpeL's required-training-stage approach Wray-Kirk-Laird identify as the closest extant LLM analogue). Closest live competitor SCM (April 2026) has typed `contradicts` edges + sleep consolidation but lacks cascade and lacks derivation-typing."

This is materially stronger because:
- It engages two patterns instead of one (more leverage from same source)
- It is precise about the difference between pattern and specialization (defends against "ENGRAM = JTMS" criticism)
- It positions the SCM comparison cleanly within the same vocabulary

The convergent-discovery framing extends:
- Kahl arrived at the architectural-deficit shape from agency theory.
- Wray-Kirk-Laird arrived at the cognitive-design-patterns shape from cognitive architecture lineage.
- Both, independently, identify gaps that ENGRAM addresses.
- We arrived at the implementation from engineering pressure, without seeing either.

That is three-way convergence, not two-way.

---

## Where this leaves us at 21:50 EDT

First-hand reads complete:
- ✓ Kahl EAA paper (this morning) — three corrections to Phil claim framing
- ✓ Kahl OCC paper (~21:25) — significant correction; Phil claim now "1 of 3 OCC conditions + §3.5 deficit closure + bifurcation argument"
- ✓ Wray-Kirk-Laird AGI'25 (now) — Tech claim B refined to be pattern-precise + extended to knowledge-compilation + autonoetic-triangulation surfaced

Still to read first-hand:
- Kumaran 2016 CLS Theory Updated — strongest cog-sci grounding for nap/sleep mechanism
- Kahl Duck Criterion paper — flagged by deep sweep, low-priority but should verify
- Pink et al. 2025 (newly identified) — LTM-as-missing-piece, directly engages our claim shape
- Wu et al. 2025 (newly identified) — landscape survey

Next loop fire (21:44, in ~3 min): probably Pink 2025 since it's short and directly load-bearing for the LTM-deficit framing in the introduction. Then Kumaran. Then a final-revise pass at ~05:00 to integrate all findings into the clean-slate plan before Lei wakes.
