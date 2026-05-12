# "Memory for Autonomous LLM Agents" Survey — First-Hand Read
**Sub-agent:** paper-research scout
**Access date:** 2026-05-12
**Status:** Primary-source verified

---

## 1. Metadata

| Field | Value |
|-------|-------|
| Title | Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers |
| Author | Pengfei Du |
| Affiliation | Hong Kong Research Institute of Technology |
| arXiv ID | 2603.07670v1 |
| Submitted | 2026-03-08 |
| Venue | arXiv preprint (cs.AI) |
| URL | https://arxiv.org/abs/2603.07670 |

---

## 2. Architecture / Framework Summary

This is a single-author survey covering agent memory literature from 2022 through early 2026. It frames memory as "the ability to persist, organize, and selectively recall information across interactions — is what turns a stateless text generator into a genuinely adaptive agent."

**Coverage:** Five mechanism families: context compression, retrieval-augmented storage, self-reflection, hierarchical contexts, and learned management policies. Applications: personal assistants, coding agents, gaming environments, scientific reasoning, multi-agent collaboration.

**Three-axis taxonomy (exact verbatim):** The survey "organize[s] the space along three orthogonal dimensions":
- *Temporal scope*: "working memory...episodic memory...semantic memory...procedural memory"
- *Representational substrate*: "context-resident text...vector-indexed stores...structured stores...executable repositories"
- *Control policy*: "heuristic control...prompted self-control...learned control"

**Write-manage-read framework:** The survey structures memory operations into a three-phase pipeline: writing new information, managing/consolidating existing memory, and reading/retrieving on demand.

**Evaluation landscape:** Notes a significant gap: "models that score near-perfectly on LoCoMo plummet to 40–60% in MemoryArena, exposing a deep gap between passive recall and active, decision-relevant memory use."

**Self-reinforcing error (Section 4.3, verbatim):** "A single incorrect reflection in a short-lived agent causes limited damage; the same incorrect reflection persisting in a long-running production agent...can be catastrophic." "If the agent incorrectly concludes 'API X always returns errors with parameter Y,' it will avoid that call path forever, never collecting evidence to overturn the false belief."

**Contradiction handling (Section 7.3, verbatim):** "Robust systems need _temporal versioning_ (prefer the newest record), _source attribution_ (user statement > agent inference), _contradiction detection_ (flag conflicts for resolution), and _periodic consolidation_ (scheduled sweeps that merge duplicates and retire stale entries)."

**Key open challenges (Section 9):**
1. Principled consolidation
2. Causally grounded retrieval
3. Trustworthy reflection (Section 9.3)
4. Learning to forget (Section 9.4)
5. Multimodal and embodied memory
6. Multi-agent memory governance
7. Memory-efficient architectures
8. Neuroscience integration
9. Foundation models for memory management
10. Standardized evaluation

**Trustworthy reflection (Section 9.3, verbatim):** "Self-reflection is a powerful adaptation mechanism that can also entrench mistakes. If the agent falsely concludes that 'approach A always fails,' it will never test approach A again—a classic confirmation bias. Future systems need external validation (check reflections against ground truth when available), uncertainty quantification (decay confidence over time without confirming evidence), adversarial probing (periodically challenge stored beliefs with counterexamples), and expiration policies (retire unvalidated reflections after a set period)."

**Learning to forget (Section 9.4, verbatim):** "Forgetting is not a bug; it is a feature—essential for robustness, privacy, and efficiency. Yet current systems handle it crudely: hard time-based expiration, storage-limit eviction, or nothing at all. The research problem is to learn _selective_ forgetting policies that maximize long-term utility under safety and compliance constraints."

---

## 3. ENGRAM-Function Comparison Table

Note: This is a survey, not a system. The table assesses whether the survey recognizes, names, or cites each mechanism.

| ENGRAM Mechanism | Survey Treatment | Evidence |
|------------------|-----------------|----------|
| Claim-level contradiction as first-class node (ct_*) | **Named as needed, not solved** | Section 7.3 names "contradiction detection (flag conflicts for resolution)" as a requirement for robust systems, but cites no system as implementing this. |
| Retraction cascade through derives_from edges | **Not recognized** | No survey entry for cascade retraction or retraction propagation. Confirmed absent. |
| Derivation primitive (typed reasoning edges) | **Not recognized** | No discussion of typed derivation edges or provenance-tracked reasoning steps. |
| Evidence-class confidence taxonomy | **Partially gestured** | "Uncertainty quantification (decay confidence over time without confirming evidence)" appears in Section 9.3 as a future need, not a documented existing mechanism. |
| Provenance to quoted span of committed source | **Not recognized** | "Source attribution" in Section 7.3 means user-vs-agent attribution, not fine-grained quoted-span provenance. Knowledge graphs mentioned once (Ji et al., 2022) as structured storage substrate with no further development. |
| Supersede relation | **Not recognized** | "Temporal versioning (prefer the newest record)" in Section 7.3 describes recency-based overwrite, not a structured supersede relation. |
| Agent-as-epistemic-author posture | **Not recognized** | No framing of agent as accumulating a structured epistemic record with authorship accountability. |

---

## 4. OCC Engagement Analysis

No reference to Kahl, OCC, diachronic constraint, non-interchangeability, or self-maintaining arbitration anywhere in the survey. The March 8, 2026 submission date is after Kahl's AGI paper, but the survey does not cite it.

**Philosophical engagement:** None from analytic philosophy or philosophy of mind tradition. The survey adopts cognitive neuroscience framing (Baddeley's working memory model, Ebbinghaus forgetting curves, spreading activation theory, Tulving's episodic/semantic distinction). These are empirical psychology sources, not philosophical identity frameworks.

**Nearest passage to OCC territory:** The trustworthy reflection challenge (Section 9.3) describes a problem structurally adjacent to Cond 3 (self-maintaining arbitration): the agent entrenches false beliefs without correction. But the proposed remedies (external validation, adversarial probing, expiration policies) are all external interventions, not structural primitives. This is precisely the gap ENGRAM fills with internal retraction-cascade architecture.

---

## 5. OCC Engagement Analysis (Survey Frame)

This section assesses whether the survey's framing, even without citing Kahl, would independently lead a reader toward the OCC conditions.

**Cond 1 — Diachronic Constraint:** The survey treats past information as a retrieval resource, not a structural constraint on deliberation. The "temporal scope" axis describes what type of memory is being accessed, not whether past commitments non-trivially structure present reasoning. No survey system is described as enforcing diachronic constraint.

**Cond 2 — Non-Interchangeability Under Reset:** Not addressed. The survey discusses persistence across sessions but not agent-level token-distinctness. A reset that replaces one agent's memory with another's is not discussed as a problem.

**Cond 3 — Self-Maintaining Arbitration:** The survey identifies this as an open problem without naming it as such. Section 9.3 describes the problem (false reflections entrench, confirmation bias, no correction mechanism). The proposed solutions are all external to the agent's deliberative architecture. ENGRAM's internal retraction cascade is the structural answer this challenge calls for.

**Net OCC engagement:** The survey independently surfaces the problem space that OCC Cond 3 addresses, without the Kahl vocabulary. This makes it a useful positive citation: "Even a purely engineering-focused survey (Du 2026) independently identifies the need for correction mechanisms that cascade through agent reasoning — confirming that the problem is real and unsolved."

---

## 6. Load-Bearing for the ENGRAM Paper

**Strongest citation use (gap-naming):** Section 9.3 (Trustworthy Reflection) and Section 7.3 (contradiction handling) together establish that: (a) the engineering community recognizes contradiction and self-reinforcing error as problems, and (b) no system is cited as solving them structurally. The survey's silence on cascade retraction, despite covering 4 years of literature, is a load-bearing absence.

**Verbatim quotes for direct citation:**
- For the problem: "If the agent incorrectly concludes 'API X always returns errors with parameter Y,' it will avoid that call path forever, never collecting evidence to overturn the false belief." (Section 4.3)
- For the gap: "Robust systems need...contradiction detection (flag conflicts for resolution)" — followed by no citation to a system that does this. (Section 7.3)
- For open-challenge framing: "Future systems need external validation...uncertainty quantification...adversarial probing...and expiration policies" — these are all external interventions, not structural primitives. (Section 9.3)

**Single-author limitation:** This is a single-author survey from a Hong Kong institute preprint. It has not undergone peer review as of access date. Coverage of literature may have gaps; the 10 open challenges are not systematically derived from coverage. Cite as representative of engineering-community framing, not as authoritative taxonomy.

---

## 7. Honest Pros / Cons

**Pros of citing this survey:**
- Most recent comprehensive survey of agent memory (March 2026), covering the same period as ENGRAM's development
- The taxonomy (temporal × representational × control) gives the ENGRAM paper a clean foil: ENGRAM adds an orthogonal fourth axis (epistemic structure / provenance discipline)
- Section 7.3 and Section 9.3 name the ENGRAM problem space without solving it — ideal for establishing that the problem is recognized
- Cascade-retraction absence is cleanly documentable: 4 years of survey coverage, not one system cited for retraction propagation

**Cons / limitations:**
- Single author, no peer review, preprint
- Neuroscience framing, no philosophical identity engagement — ENGRAM paper has to bridge that gap itself
- "Contradiction detection (flag conflicts for resolution)" in Section 7.3 is aspirational: the survey doesn't distinguish between flagging contradictions and resolving them structurally. The claim is normative ("robust systems need"), not descriptive ("existing systems do"). This is good for ENGRAM's argument but requires careful framing.
- The open-challenges list (Section 9) reads as brainstorming rather than systematic gap analysis — weak as a primary source for what's unsolved, but usable as corroboration

---

## 8. Verdict

This survey is the clearest available evidence that the engineering-focused agent-memory community (a) recognizes the contradiction-and-false-belief-persistence problem, (b) names it as unsolved, and (c) does not engage Kahl's philosophical framing at all. The three most load-bearing findings are: the verbatim gap in Section 7.3 ("contradiction detection...flag conflicts for resolution" with no cited solution), the self-reinforcing-error analysis in Section 4.3, and the trustworthy-reflection open challenge in Section 9.3 that calls for external interventions rather than internal structural primitives. Cascade retraction is absent from a 4-year literature survey, which is a confirmable negative result. The survey's philosophical silence is itself a citation argument: ENGRAM is positioned as the bridge between this engineering community and Kahl's OCC framework. Use this survey as gap-naming evidence, not as a systems comparator. Cite with the single-author / preprint caveat.
