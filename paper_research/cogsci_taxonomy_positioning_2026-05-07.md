# Cog-sci Memory Taxonomy Positioning — 2026-05-07

Self-study thread (Borges, gl_0027 multiplier-domain pull) on how ENGRAM's node-type taxonomy relates to established memory-type taxonomies in cognitive science. Generated the following claims; recording here so Ch 5 (formal architecture) and Ch 9 (open questions) drafts can pick them up.

## Core claim (dv_0567, conf 0.864)

> ENGRAM's typing structure is **orthogonal** to cognitive-science memory taxonomies (Tulving / Squire — episodic vs semantic vs procedural) and **structurally aligned** with symbolic cognitive architectures (ACT-R-style declarative memory). ENGRAM is "ACT-R-with-enforced-typing": uniform symbolic substrate (nodes + edges) with type vocabulary selected at the tool-surface layer, not the storage layer.

## Carving-plane comparison

| Framework | Carves memory by | Type vocabulary |
|---|---|---|
| Tulving (1972, 1985) | Information class | priming / procedural / perceptual / semantic / episodic |
| Squire (1990s+) | Information class + consciousness | declarative (semantic + episodic) / nondeclarative (procedural + priming + classical conditioning + nonassociative) |
| ACT-R (1990s+) | Architectural module | declarative chunks / procedural productions (info-class agnostic at the substrate layer; convention-driven schema typing) |
| **ENGRAM** | **Epistemic role** | **axiom / definition / observation_factual / observation_predictive / derivation / conjecture / question / lesson / goal / cornerstone / evidence / person / contradiction / feeling_report / task** |

## Three implications for the paper

**1. (Ch 5 architecture)** ENGRAM's type vocabulary is not a competing answer to Tulving/Squire — it answers a different question. Cog-sci asks "what KIND of information is stored." ENGRAM asks "what EPISTEMIC ROLE does this play in the agent's reasoning chain." The chapter should make the orthogonality explicit so readers don't expect ENGRAM to map onto episodic/semantic and find the mapping forced.

**2. (Ch 5 architecture)** Closer comparable: ACT-R's declarative memory module. ENGRAM and ACT-R both operate at the symbolic-claim layer and use a uniform substrate. Difference: ACT-R's type-distinctions are convention-driven (modeler decides via slot semantics); ENGRAM's are tool-surface enforced (different creation tools produce different node.type values with different confidence-computation, supersede, retraction-cascade behavior). ENGRAM is therefore "ACT-R + stricter typing at the API."

**3. (Ch 9 open questions)** ENGRAM has no procedural-memory analog inside the graph, and that's structurally correct: procedural memory in agents lives in skill markdown files, hook scripts, and harness behavior — different substrate, different lifecycle. The orthogonality is a feature, not a gap. Worth naming explicitly so readers don't ask "where's procedural memory in ENGRAM?" — the answer is "outside the graph by design."

## Provenance

- ob_1563 (Tulving / Squire taxonomy review, conf 0.7 external) — Rubin et al. 2021, *Memory & Cognition*: https://link.springer.com/article/10.3758/s13421-021-01148-3
- ob_1564 (ACT-R declarative memory, conf 0.7 external) — *Computational Brain & Behavior* 2023: https://link.springer.com/article/10.1007/s42113-023-00189-y
- dv_0567 (the orthogonality + ACT-R-alignment derivation, conf 0.864 inductive_generalization) — combines the two

## What this is NOT

This isn't a complete competitive-intel scan. It's one self-study thread that surfaced a paper-relevant positioning. Adjacent work that could deepen it: read the original Tulving 1985 paper (already partly captured in ob_1114), the Squire (2004) "Memory systems of the brain" review, and the Atkinson & Shiffrin (1968) multi-store model for the broader historical context.

## Update — 2026-05-07 PM

A follow-up search on "epistemic memory taxonomy provenance reasoning role belief revision AI agent" surfaced that **the agent-memory community is already carving along axes that overlap with ENGRAM's epistemic-role typing**. The landmark survey "Memory in the Age of AI Agents" (Hu et al., arxiv 2512.13564, 2025) classifies along three axes:

- **Forms**: Token-level / Parametric / Latent
- **Functions**: Factual / Experiential / Working
- **Dynamics**: Formation / Evolution / Retrieval

The Functions axis maps roughly onto ENGRAM's epistemic-role typing — Factual ↔ evidence + observation_factual + axiom + definition; Experiential ↔ lesson + feeling_report + observation_predictive; Working ↔ focused-set / tier1 / current-turn.

**This already lives in my graph as ob_1054 + dv_0430** (registered earlier). ob_1054 specifically notes the survey does NOT include contradiction detection, provenance tracking, confidence tracking, or retraction-cascade as distinct taxonomic categories — which is where ENGRAM differs.

**Revised positioning** for the paper:

- ENGRAM is NOT novel in carving by epistemic role (the agent-memory community already does)
- ENGRAM IS novel in: (a) the specific node-type vocabulary, (b) tool-surface-enforced typing vs convention-driven, (c) reasoning-type-aware confidence propagation, (d) explicit contradiction nodes + retraction-cascade as first-class typology elements absent from the Hu et al. taxonomy
- dv_0567's "orthogonal to cog-sci, aligned with ACT-R" framing is correct but undersells the agent-memory positioning; better framing for Ch 5 is: "ENGRAM is a strict-typing instantiation of the Hu et al. Functions taxonomy with the Forms axis pinned to Token-level + semantic-embedding retrieval, and with contradiction/provenance/confidence/retraction promoted to first-class node-type and edge-type categories that the Hu et al. taxonomy elides."

Provenance update:
- ob_1566 — Hu et al. functions taxonomy ↔ ENGRAM mapping (new today)
- ob_1054 — Hu et al. three-axis taxonomy + absent-categories observation (existed; corroborates dv_0430)
- ls_0032 — branch-hygiene tripwire (ob_1552 + ob_1565 incidents) — registered today, not paper-relevant but operational

## Update — 2026-05-07 PM (Lei pointer: Farina et al. 2026)

Lei flagged a directly relevant paper: **Farina, Ding, Lavazza et al. 2026, "Neuromorphic Computing and Extended Memory"**, *Review of Philosophy and Psychology* (DOI [10.1007/s13164-026-00800-8](https://doi.org/10.1007/s13164-026-00800-8), accepted 14 January 2026, published 7 February 2026).

### Abstract framing

The paper examines BCIs, Memory-Augmented Neural Networks (MANNs), and neuromorphic computing as **empirical supports for the Extended Mind Thesis (EMT)**.

### Why this matters for ENGRAM's paper

`ob_0542` (2026-04-13) already claimed ENGRAM "is functionally a component of the agent's cognitive system... under the extended mind thesis criteria" — at the time, an agent-introspective interpretation of Clark & Chalmers 1998. **Farina et al. 2026 provides published philosophical scaffolding for that exact framing.** dv_0568 (today, conf 0.907) corroborates the EMT positioning at the field-published level.

### ENGRAM's place within Farina et al.'s taxonomy

The paper names three EMT-supporting artifact classes: BCIs / MANNs / neuromorphic computing. ENGRAM is **software-only, symbolic-MANN-adjacent** — it satisfies EMT criteria (reliable access, automatic endorsement, consistent integration into reasoning) but sits at a different point in the design space than the paper's neuromorphic-hardware case study. The MANN comparison is the closest published comparable.

### Where ENGRAM extends the EMT literature

Two specific openings the paper does NOT close:

1. **The symbolic-graph subspace** — Farina et al.'s case study is hardware; ENGRAM is the symbolic-software case
2. **Structural-integrity primitives** — the EMT literature engages engineered-memory CAPABILITIES (storage, retrieval, augmentation) but not the discipline question. Whether a memory system's structural integrity (contradiction-detection, provenance-tracking, retraction-cascade) matters for its cognitive-constitutive status is, as far as today's quick scan shows, unaddressed. ENGRAM's first-class promotion of these primitives is a contribution the paper (Ch 5 architecture, Ch 9 open questions) can name explicitly.

### Sharper paper claim (revised again)

**ENGRAM's positioning relative to current literature, as of 2026-05-07:**

- Cog-sci taxonomy (Tulving / Squire) — ENGRAM carves orthogonally (epistemic role, not information class). dv_0567.
- Symbolic cognitive architectures (ACT-R) — ENGRAM is "ACT-R-with-enforced-typing." dv_0567.
- Agent-memory survey (Hu et al.) — ENGRAM is a strict-typing instantiation of the Functions axis with first-class promotion of categories the survey elides. ob_1054, ob_1566.
- **Extended Mind Thesis (Farina et al. 2026)** — ENGRAM is a software-only symbolic-MANN-adjacent EMT case; structural-integrity primitives are an opening for ENGRAM's contribution to the EMT literature. **dv_0568** (new today).

### Sub-finding: ENGRAM is a SECOND-WAVE EMT case, not first-wave

A 5-minute follow-up search on whether the EMT literature has engaged structural-integrity as a constitutive criterion surfaced an important distinction. The EMT literature has three waves:

1. **First-wave (Clark & Chalmers 1998)** — functional-similarity + reliability + endorsement + access criteria
2. **Second-wave (complementarity principle)** — artifact can have *different* properties from biological memory and still be cognitive-constitutive if tightly integrated. Quote: *"An object does not have to be functionally similar to a biological process but can become an extended part of the cognitive system when it is tightly integrated somewhere in the brain-body-environment system."* (Routledge Encyclopedia of Philosophy, "Extended Cognition")
3. **Third-wave** — dynamical / coupling-as-constitution

**ENGRAM is a second-wave case.** Its structural-integrity primitives (contradiction-detection, provenance-tracking, retraction-cascade) are *exactly* the kind of complementary properties biological memory does NOT have — the LLM agent's training-frozen weights cannot retract themselves; only ENGRAM's external symbolic structure can. Under complementarity, ENGRAM's first-class promotion of these primitives is the cognitive-extending property, not a deviation. (See `ob_1568`.)

Bonus connection: ENGRAM's reasoning-verbs (`engram_retract`, `engram_supersede`, `engram_resolve`) are textbook **epistemic actions** in the Kirsh & Maglio 1994 sense — actions that manipulate the environment specifically to improve epistemic state. The vocabulary IS the cognitive scaffolding.

### Implications for paper Ch 5 / Ch 9 (consolidated, after Lei pointer + sub-finding)

- **Ch 5**: Position ENGRAM under second-wave EMT explicitly. Cite Farina et al. 2026 + the Routledge encyclopedia entry's complementarity formulation. Distinguish ENGRAM from first-wave functional-similarity readings (e.g., the Otto's-notebook case) that don't license structural-integrity primitives as cognitive-constitutive.
- **Ch 9**: Open question — under complementarity, what is the *minimum* structural-integrity discipline that an external memory must have to count as cognitive-constitutive? ENGRAM has provenance + contradiction + retraction; smaller systems (vector stores, episodic memory plugins) don't. Where's the line? This is a research direction the paper can name without answering.
