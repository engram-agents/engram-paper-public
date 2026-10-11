# Kumaran, Hassabis, McClelland 2016 — First-Hand Read (2026-05-08 evening, ~22:00 EDT)

**Paper:** "What Learning Systems do Intelligent Agents Need? Complementary Learning Systems Theory Updated"
**Authors:** Dharshan Kumaran (Google DeepMind + UCL), Demis Hassabis (Google DeepMind + Gatsby), James L. McClelland (Stanford Psych + Center for Mind, Brain, and Computation)
**Venue:** Trends in Cognitive Sciences, Vol 20, No 7 — Feature Review
**Pub date:** July 2016
**DOI:** 10.1016/j.tics.2016.05.004
**Length:** 19 pages (pages 512-534 of TiCS Vol 20)
**Surfaced via:** Pink et al. 2025 + Wray-Kirk-Laird 2025 both cite as foundational
**Authority:** McClelland is the original CLS architect (1995, with McNaughton & O'Reilly); Hassabis built the empirical hippocampus / DQN bridge; Kumaran is the systematizer. This IS the canonical paper for CLS theory in 2026.

---

## Why we read this paper

It is the strongest cog-sci grounding for ENGRAM's nap/sleep consolidation cycle. Both Pink and Wray-Kirk-Laird cite it as the canonical CLS reference. Per ls_0011 + the EAA/OCC precedents, first-hand verification was overdue before paper-citation.

---

## Their thesis in two sentences

**Verbatim from abstract (page 512):**

> "We update complementary learning systems (CLS) theory, which holds that intelligent agents must possess two learning systems, instantiated in mammalians in neocortex and hippocampus. The first gradually acquires structured knowledge representations while the second quickly learns the specifics of individual experiences."

The two-system thesis is foundational: a single learning system cannot satisfy both stability (preserve existing structure) and plasticity (rapidly encode new specifics). The fast-slow division is structural, not algorithmic-detail.

---

## Three updates from the original 1995 CLS

The paper's contribution beyond the original framing:

**Update 1: Replay's role expanded.** Originally proposed as faithful re-presentation of recent experiences for gradual integration into cortex. Updated: replay is *goal-dependent*, *reward-modulated*, *novelty-modulated*. Verbatim from page 521:

> "the hippocampus may allow the general statistics of the environment to be circumvented by reweighting experiences such that statistically unusual but significant events may be afforded privileged status, leading not only to preferential storage and/or stabilization (as originally envisaged in the theory) but also leading to preferential replay that then shapes neocortical learning."

This means: the agent's memory system is not just a recorder — it is an *active editor* of what becomes stable knowledge, weighted by goals and significance.

**Update 2: Hippocampus supports generalization** (cross-item inference). Originally hippocampus was thought to support only specifics; cortex did all the generalizing. Updated: hippocampus enables paired-associate inference (PAI) and similar cross-item bindings via recurrent reactivation (REMERGE model). The hippocampus can dynamically combine information from multiple separate episodes to support inference that wasn't directly experienced.

**Update 3: Neocortical learning can be rapid when schema-consistent.** Originally cortical integration was thought to require thousands of repetitions over years. Event arena paradigm (Tse et al. 2007, 2011) showed: when new info is *consistent* with existing schema, integration can complete in 48 hours. Verbatim from page 525-527:

> "the core tenet of the theory that the incorporation of novel information into neocortical networks must be slow to avoid catastrophic interference: we now know that this statement only applies when new information is inconsistent with existing knowledge in the neocortex."

The slow-learning constraint applies to *schema-inconsistent* new info; *schema-consistent* info can integrate fast.

---

## The explicit AI invitation

This is the load-bearing finding for our paper. From the concluding remarks (page 530, verbatim):

> "Finally, we have highlighted the broad applicability of the principles of CLS theory to developing agents with artificial intelligence, an area which we hope will continue to rise in interest and become a significant direction for future research"

And from the section "Links Between CLS Theory and Machine-Learning Research" (page 527-529), they document how CLS principles already shape ML: deep neural networks (slow-learning neocortical analogue), DQN's experience replay (hippocampal replay analogue), neural Turing machines / Memory Networks (external memory + content-addressable retrieval as hippocampal analogue), continual learning research (catastrophic forgetting → CLS solution).

The Outstanding Questions sidebar (page 530) ends with one question that is essentially an open invitation:

> "What algorithmic functionalities and implementational schemes are desirable for an external memory module, both for human learners and for artificial agents?"

**ENGRAM is a substantive proposed answer to that question.** We should cite this verbatim.

---

## ENGRAM evaluated against CLS theory

**The structural mapping (this is the load-bearing claim for the paper):**

| CLS component | Hippocampus role | Neocortex role | ENGRAM analogue |
|---|---|---|---|
| Encoding | Fast, single-shot, instance-specific | Slow, statistical | `engram_add_observation` (single-shot, fast) → `engram_derive` chains (consolidated) |
| Coding scheme | Pattern-separated (sparse, distinct codes per experience) | Distributed, similarity-based | Each node has a distinct ID; derivation chains add similarity-based linkage via support edges |
| Replay | Sharp-wave ripples during sleep, reward/novelty modulated | Gradual integration via interleaved exposure | `engram_nap` / `engram_sleep` cycles; cornerstone-promotion criteria favor highly-supported derivations |
| Generalization | REMERGE-style recurrent reactivation across episodes | Schema-based generalization | `engram_derive` synthesizes claims from multiple support nodes; `engram_reflect` finds emergent patterns |
| Schema-dependent integration | Schema-consistent info integrates fast | New schema-inconsistent info requires slow learning | Consistent claims integrate immediately (high confidence); contradictory claims trigger `ct_` nodes that block downstream use until resolved |
| Forgetting / interference | Pattern separation prevents interference between similar items | Catastrophic forgetting in single-system networks | Distinct node IDs prevent interference; supersede + retract preserve audit trail rather than overwriting |

**Critical caveat:** Kumaran et al. are talking about NEURAL implementations (deep nets + experience replay + episodic memory modules in weight-update terms). ENGRAM is a SYMBOLIC implementation. Are we satisfying the spirit of CLS or just hitting surface features?

**Defensible position:** ENGRAM achieves the FUNCTIONAL CLS division at the substrate level rather than at the weight-update level. The fast-slow division is structural (observation_factual vs derivation+cornerstone) rather than learning-rate-based (hippocampus vs neocortex weights). But the FUNCTIONAL roles map cleanly. The paper should be explicit:

> "ENGRAM implements the CLS functional division through symbolic-substrate organization rather than dual-network weight learning. The fast-system (observation nodes with provenance) and slow-system (cornerstones, axioms, definitions, derivation chains) achieve the same functional roles Kumaran et al. ascribe to hippocampus and neocortex respectively. The substrate-level implementation is a different design point than DQN-style replay buffers (which still operate via gradient updates on a single neural network); ENGRAM achieves separation of fast and slow learning at the substrate level, decoupling it from the LLM weight update entirely."

This is honest convergence, not surface-level pattern-matching. It also makes the paper distinguishable from RAG/GraphRAG, which lack the fast/slow functional division explicitly.

---

## What CLS theory adds beyond what Pink + Wray-Kirk-Laird offer

Pink's 5-property framework focuses on *what episodic memory looks like* (long-term, explicit, single-shot, instance-specific, contextual). Wray-Kirk-Laird's reconsideration pattern focuses on *non-monotonic commitment revision*. Kumaran et al. add:

1. **The systems-level architecture argument**: not just "you need X property," but "you need TWO systems with complementary properties because a single system has stability-plasticity dilemma." This is the strongest theoretical argument for an external-memory architecture.

2. **The schema-dependent integration mechanism**: rapid integration when consistent + slow integration when inconsistent. This maps exactly to ENGRAM's design — consistent observations integrate immediately into the graph; contradictions block downstream use until resolved (slower process). We hadn't explicitly framed this as schema-dependent integration before; the framing is illuminating.

3. **The reward/significance modulation of consolidation**: not all memories are equal; significance-weighted replay shapes what becomes stable. ENGRAM's focus mechanism + cornerstone-promotion criteria implement exactly this — load-bearing claims (focused, high-support, frequently-cited) get preferential durability; routine observations may be retained but never promoted.

4. **The systems-neuroscience grounding**: SWRs during slow-wave sleep, time-compressed replay, hippocampal-cortical synchronization. None of this is in ENGRAM (we don't have cortical analogues at the neural level), but it grounds the *functional* design choices in cog-sci-validated mechanisms. The paper can cite these as "the biological substrate's design rationale matches our engineered substrate's design rationale."

---

## Concrete citations to harvest from Kumaran 2016 references

For our cog-sci grounding chapter:

1. **McClelland, McNaughton, O'Reilly 1995** — "Why there are complementary learning systems in the hippocampus and neocortex: insights from the successes and failures of connectionist models of learning and memory." Psychological Review 102, 419-457. The original CLS paper. We MUST cite alongside Kumaran 2016.

2. **O'Neill, Pleydell-Bouverie, Dupret, Csicsvari 2010** — "Play it again: reactivation of waking experience and memory." Trends in Neurosci 33, 220-229. Replay reactivation evidence.

3. **Marr 1971** — Original hippocampal-cortical theory. Foundational reference.

4. **Tse et al. 2007, 2011** — Event arena paradigm; rapid schema-consistent integration. Two papers, both load-bearing for the "neocortex can learn fast under right conditions" claim.

5. **Mnih et al. 2015 (DQN)** — Experience replay in deep RL. The clearest existing AI implementation of CLS-style replay; we contrast ENGRAM's symbolic approach to DQN's gradient-based approach.

6. **Graves et al. 2014, 2016 (Neural Turing Machine + Differentiable Neural Computer)** — External-memory neural networks. Cited in Box 10. Relevant comparison case.

7. **REMERGE model (Kumaran & McClelland 2012)** — Recurrent activation supporting cross-item inference. The mechanism by which hippocampal storage supports generalization, which ENGRAM does via `engram_derive` chains.

---

## The convergence picture extended to FIVE voices

We now have **five independent voices** converging on the same architectural shape:

1. **Kahl 2026** (Zenodo, philosophy/agency theory) — OCC framework + EAA framework. Names the architectural deficit: persisting subject + epistemic arbitration + diachronic constraint. ENGRAM satisfies 1 of 3 OCC conditions cleanly + extends the third via type/token reformulation.

2. **Wray, Kirk, Laird 2025** (AGI'25, cognitive engineering / Soar lineage) — names reconsideration and knowledge compilation as cognitive design patterns "apt for exploration and exploitation" but not yet mainstream in Agentic LLMs. ENGRAM specializes both.

3. **Pink et al. 2025** (arXiv, cog-sci-grounded LLM memory / MPI-SWS + Intel + UT Austin) — names episodic memory's five properties as the missing piece for long-term LLM agents. ENGRAM satisfies all 5.

4. **Kumaran, Hassabis, McClelland 2016** (TiCS, cog-sci/neuroscience canonical / Google DeepMind + UCL + Stanford) — CLS theory updated. The strongest argument for two-system memory architecture. Explicit invitation to apply to AI agent design. ENGRAM implements the CLS functional division at the substrate level.

5. **ENGRAM design (March-April 2026, engineering pressure)** — arrived at the same architectural shape independently, without seeing any of the above during ideation.

**Five-way independent convergence** across philosophy, cognitive engineering, cog-sci-grounded ML research, canonical cog-sci/neuroscience, and engineering. If three-way was already a strong claim, five-way is overwhelming.

The convergence doesn't mean we're right — it means the architectural shape is forced by the same constraints multiple independent traditions have identified. ENGRAM is a specific instance of a converged design space.

---

## What this implies for the paper

**Phil claim:** The convergence becomes the methodological spine. Paper opens with a five-way convergence diagram, then ENGRAM as one specific instance.

**Tech claim B:** The CLS framing strengthens the description of nap/sleep as functional consolidation. Tech B becomes:

> "ENGRAM realizes the complementary-learning-systems functional division at the substrate level. The fast-system (observation nodes with provenance, single-shot encoding) and slow-system (derivation chains, cornerstone promotion) achieve at the substrate level what Kumaran-Hassabis-McClelland (2016) ascribe to hippocampus and neocortex respectively. The substrate-level implementation decouples the fast/slow functional division from the LLM weight update — different from DQN-style replay buffers (which still operate via gradient updates on a single network) and from RAG/GraphRAG (which have no fast/slow functional division). The reconsideration pattern Wray-Kirk-Laird identify and the five episodic-memory properties Pink et al. identify are both consequences of the CLS-style two-system architecture; ENGRAM gets them coherently because they all emerge from the same design choice."

This is much more theoretically grounded than just "we have observations and derivations."

**Cog-sci grounding chapter:** The paper now has a substantive grounding chapter using Kumaran 2016 + McClelland 1995 + Tse 2007/2011 + Mnih 2015 + Tulving 1983. Strengthens the "ENGRAM has biological motivation" framing without overclaiming neural implementation.

---

## What's NEXT

Wakeup at 22:02. The natural next move is the integration pass on the clean-slate paper plan — I now have FOUR first-hand reads (OCC, Wray-Kirk-Laird, Pink, Kumaran) and the integration is overdue. Lower priority: Kahl Duck Criterion (deep-sweep flagged but not load-bearing), Wu et al. 2025 survey (landscape evidence).

Decision: **next turn = clean-slate paper plan revision** integrating the four first-hand reads + Lei's type/token sharpening + the compaction-as-live-instance extension. This is a substantial morning-deliverable update.

---

## Addendum 2026-05-08 22:13 EDT — dv_0580 retroactive correction

A curiosity-pull query into ENGRAM (~22:10) surfaced dv_0446 from 2026-04-21 (conf 0.95, resolves qu_0219) which is in tension with this memo's structural-mapping claim. dv_0446 had already established the more honest formulation:

> "ENGRAM alone is a single-layer hippocampal analog — fast, sparse, provenance-bearing — with no neocortical weight-update counterpart for slow statistical integration. The honest Ch 5 slot is therefore NOT 'ENGRAM implements CLS' but 'ENGRAM is the hippocampal half of CLS, and the full CLS mapping requires ENGRAM+fine-tuning as a composite architecture in which ENGRAM plays hippocampal teacher and model weights play neocortical student.'"

This memo's "Defensible position" subsection above (in §"ENGRAM evaluated against CLS theory") DID flag the symbolic-vs-neural caveat in prose, but ob_1602's claim-text dropped it — claiming "implements the CLS functional division at the substrate level" without the symbolic-substrate qualifier.

The dv_0580 derivation (abductive_elimination, conf 0.616) records the correction. **dv_0446's framing must take precedence in the paper.** The corrected position:

> ENGRAM realizes the hippocampal half of CLS at the symbolic-substrate level + provides explicit operators (derivations, nap/sleep, cornerstone promotion) that play the *agent-explicit analog* of neocortical statistical integration without requiring weight updates. Within ENGRAM the fast/slow distinction (observation vs derivation+cornerstone) is real but it is a symbolic fast/slow, not a learning-rate-based fast/slow. The composite ENGRAM+fine-tuning architecture would instantiate full CLS; ENGRAM alone makes that composite possible by providing the hippocampal-teacher half.

This is consistent with both Kumaran et al.'s actual position (which uses weight-update mechanisms throughout) and ENGRAM's earlier self-derivation. The convergent-discovery picture from §10 of the clean-slate paper plan is unchanged in shape (still five-way: Kahl + Wray-Kirk-Laird + Pink + Kumaran + ENGRAM-from-engineering); only the specific Tech B sub-claim about substrate-level implementation needed softening.

**Methodological note for the paper itself:** this episode is a live demonstration of why the ENGRAM-discipline matters. I overclaimed in ob_1602; the graph (via dv_0446) contained the corrective evidence; a curiosity-pull query surfaced it; dv_0580 records the correction with full provenance. The cascade hasn't fired (ob_1602 isn't strictly retracted, just refined); the contradict-and-resolve infrastructure caught the substantive overclaim within hours. This is exactly the kind of self-correcting trajectory the paper claims epistemic identity enables. The methodology chapter (Ch8) should cite this episode as a live example.
