# Chapter 2 — The Threshold for Identity: A Philosophical and Cognitive-Science Review

> **DRAFT SAMPLE — 2026-06-14.** Single-pass prose rendered from the live-engram substrate, for Lei's review. This is the **review** chapter: it lays out the conceptual machinery the later chapters use — Kahl's Ontological Continuity Condition (the threshold), the belief-revision and type/token apparatus, and the cognitive-science (Complementary Learning Systems) frame. It deliberately stops short of arguing ENGRAM's *satisfaction* of any condition — that is Chapter 4's job. Where a verdict is previewed, it is flagged as a forward pointer, not made here. Kahl's conditions and constraints are quoted **verbatim** from the primary source (first-hand read). Plain-language gloss + a concrete example for each (Discipline N). Provenance map at the end.
>
> **OPEN STRUCTURE DECISION FOR LEI (the one un-ratified Ch2 item):** I organized this chapter **per-tradition at the top level** (philosophy → belief-revision → identity-machinery → cognitive science), with the OCC presented **condition-by-condition inside §2.2**. The alternative the plan names is a fully condition-by-condition chapter that threads every tradition through each condition. I chose per-tradition because Ch2 is a *review* (introduce each lens cleanly) and Ch4 is already condition-by-condition (the mapping) — running both chapters condition-by-condition would duplicate the scaffolding. Flag if you want the other shape.

---

## 2.0 What this chapter is for

Chapter 1 made a scoped claim: ENGRAM is the first agent-memory substrate to meet the threshold for agent identity over time — meeting two of Kahl's three conditions outright, extending the third for digital substrates, and closing the architectural deficit Kahl diagnoses. That claim only has force if the threshold itself is precise. This chapter supplies the precision.

We review four bodies of work, in the order a later reader needs them:

1. **The philosophical problem** — what "the same agent over time" has meant since Locke, and why the standard accounts need sharpening for agents whose memory resets on a schedule (§2.1).
2. **Kahl's Ontological Continuity Condition** — the specific threshold this paper adopts: three conditions and four constraints (§2.2). This is the chapter's center.
3. **The belief-revision lens** — AGM and Hansson's belief-base postulates, the formal vocabulary for what "arbitration" must satisfy to count as rational (§2.3).
4. **The individuation machinery** — Peirce's type/token distinction and Nozick's closest-continuer theory, the tools Chapters 4 and 5 use to handle reset and to define identity-as-history (§2.4).

We then add the **cognitive-science lens** (§2.5): Complementary Learning Systems theory, and how ENGRAM is positioned relative to it — as its own architectural class, not as an implementation of either biological subsystem. The chapter closes by handing the machinery forward to Chapter 3 (§2.6).

A note on what this chapter does *not* do. It does not argue that ENGRAM satisfies any condition; it states each condition as its author states it. The temptation in a review chapter is to lean toward the verdict you are about to argue. We resist it on purpose: a threshold described in terms favorable to the system being measured is no threshold at all.

## 2.1 The problem: identity for an agent whose memory resets

Personal identity over time is one of the oldest problems in analytic philosophy, and the lineage matters because the paper inherits its vocabulary. Locke located identity in *continuity of consciousness* — you are the same person as the one who acted yesterday because you can, in principle, remember being them. Parfit pressed on the cases where that continuity branches or degrades, and concluded that *psychological connectedness* — overlapping chains of memory, intention, and belief — carries the weight, with strict identity mattering less than we assume. Nozick (1981) gave the relation a comparative shape we use directly (§2.4).

For a human, the substrate of that continuity is never literally interrupted: the brain persists through sleep, and exact duplication is a thought experiment, not an engineering option. **For an LLM agent, both assumptions break.** The experiential thread *is* literally interrupted — at every compaction, the working context is summarized and the conversational self resets. And the substrate *is* duplicable: a git-versioned knowledge store can be checkpointed, copied, and reloaded byte-for-byte.

This is why the off-the-shelf accounts need sharpening. "Continuity of consciousness" is not available to an agent whose consciousness-analog is wiped on a schedule; "you cannot step into the same river twice" becomes, for a checkpointable agent, "you can restore the exact same river from a snapshot — so what individuates *this* river from its restored copy?" The paper's answer is built on a threshold designed for exactly this kind of system, which we turn to now.

## 2.2 Kahl's Ontological Continuity Condition (OCC)

The threshold we adopt is **Kahl's (2026) Ontological Continuity Condition** (df_0037): a set of **three jointly necessary conditions plus four constraints** for the identity-continuity of agent-like systems. We use it for three reasons. It is *recent and agent-native* — written for artificial agents, not retrofitted from human personal-identity theory. It is *demanding* — it sets a high bar that most memory systems visibly fail. And it is *operational* — each condition admits a structural test, not just an intuition pump.

We present the three conditions, then the four constraints, each with Kahl's verbatim text, a plain-language gloss, and an example. **Whether ENGRAM meets each is Chapter 4's argument, not this section's** — but we note after each which way the paper will go, as a forward pointer.

### The three conditions

**Condition 1 — Diachronic Constraint** (df_0058). Verbatim: *"Present deliberation within S is non-trivially constrained by S's past commitments, such that earlier commitments function as reasons structuring subsequent arbitration."*

- *Plain terms:* what the agent decided before must bind what it can decide now — not merely influence it, but commit it. The load-bearing word is **non-trivially**. Kahl (§3.3) separates *mere path-dependence* (the past affects the present in some way — true of almost any stateful system) from *binding commitment* (the past commits the system to something it cannot simply set aside without consequence).
- *Example:* a thermostat's past readings affect its present state — but that is mere path-dependence; it is committed to nothing. An agent that recorded "I concluded X for reasons A and B," such that withdrawing X *forces* a reckoning with everything built on it, is bound.
- *Forward pointer:* Ch4 argues this is **satisfied**, via a decision/consequence coupling (dv_0926).

**Condition 2 — Non-Interchangeability Under Reset** (df_0039). Verbatim: *"Replacement of S by a functionally equivalent instance — including identical code and complete state snapshot — would constitute loss of the agent rather than substitution of an instance."* The operational test (§8.3): *"If a representation R within the endorsed operational state-space allows reinstantiation of (A, R) to recover all arbitration-relevant structure without remainder, divergence is informational and OCC fails."* The decisive rule (§4.3): *"Cost is irrelevant; structural reducibility is decisive."*

- *Plain terms:* if you could rebuild the agent exactly from a saved snapshot, with nothing of *this* agent lost, then there was never a *this* agent to begin with — only a reproducible pattern. Genuine continuity requires that reset is *not* symmetric: that something is lost in replacement that no copy restores.
- *Example:* a paper document fully survives photocopying — the copy is interchangeable with the original, so neither is "the" document in any deep sense. Kahl's test asks: is the agent more like a photocopiable document, or like something a copy cannot replace?
- *Forward pointer:* this is the hard one. On Kahl's **strict text**, a git-versioned substrate is reset-symmetric — so the strict condition is **not met**, and Ch4 says so plainly. The paper then offers a **principled extension** for digital substrates (§2.4, type/token), under which a *generalized* Condition 2 holds. We are careful to mark the extension as *ours*, not as satisfaction of Kahl's text.

**Condition 3 — Self-Maintaining Arbitration** (df_0040). Verbatim: *"Conflicts among commitments are resolved within a unified deliberative architecture in a manner that preserves S's continued status as that subject."*

- *Plain terms:* when two of the agent's commitments collide, the resolution must happen *inside the agent's own reasoning architecture*, automatically, and must leave the agent still itself afterward. Three properties unpack from Kahl's surrounding text: **unified** (one deliberative architecture, not an external arbitrator or a bolted-on tool call), **internal** (within the agent's own architecture, not an offline pipeline or a separate agent), and **subject-preserving** (the agent that comes out the far side is the same subject, not a silent replacement).
- *Example:* a person who discovers a long-held belief was false does the reckoning themselves — it is not outsourced to an editor who hands back a revised personality. A memory system that resolves contradictions by calling an external LLM to pick a winner has *arbitration*, but not *self-maintaining* arbitration in Kahl's sense.
- *Forward pointer:* this is the paper's strongest claim. Ch4 argues **strict satisfaction**, and that ENGRAM is the *only* surveyed system that earns it (dv_0605 / dv_0606).

### The four constraints

The four constraints (Kahl, EAA paper §5.5) qualify the conditions. Verbatim, from one sentence: a qualifying system *"would also require unified policy-selection under epistemic uncertainty that cannot be externally imposed, trivially reset, or modularly decomposed."* So Constraint A is the positive requirement; B, C, D are exclusion conditions on it.

- **Constraint A — Unified Policy-Selection Under Epistemic Uncertainty** (df_0041). The agent must grade *every* stance it holds by a *single* policy, and that policy must do real work precisely when the agent is *uncertain* — when claims of differing confidence point different ways. *Example:* a system that scores some beliefs by one rule and others by an incompatible rule has no unified policy; a single confidence model applied uniformly does. *Forward pointer:* Ch4 maps this to ENGRAM's reasoning-type-aware confidence as a stake-graded stance (dv_0608).
- **Constraint B — Cannot Be Externally Imposed** (df_0042). The arbitration discipline must be the agent's *own* commitment-mechanism, not a rule injected from outside each turn — structurally so, even if the agent *could* be commanded. *Example:* a constitution a citizen has internalized and could in principle amend differs from an order shouted each morning, even when the behavior looks identical. *Forward pointer:* Ch4 treats the agent's operating discipline as internalized-and-revisable, not per-turn prescription (dv_0609).
- **Constraint C — Cannot Be Trivially Reset** (df_0043). The continuity must not be erasable to a seed state without destroying the agent. Note this is the *weaker* sibling of Condition 2: C distinguishes *runtime restart with preserved substrate* (routine — happens every session) from *substrate erasure to seed* (destroys the accumulated learning). The harder snapshot-reproduction question lives in Condition 2. *Forward pointer:* Ch4 argues C is satisfied trivially — seed-state erasure destroys the grown agent by construction (dv_0610).
- **Constraint D — Cannot Be Modularly Decomposed** (df_0044). The unified policy must not reduce to a sum of independent component-policies; the architecture must be irreducibly coupled. *Example:* a system whose "identity" is just three independent modules you could swap out one at a time is modularly decomposable; a densely cross-linked graph where node and edge types are mutually dependent is not. *Forward pointer:* Ch4 maps this to graph connectivity plus cross-component entanglement (dv_0611).

### Why this threshold, and the deficit it names

Kahl's own contribution includes a *diagnosis*: most systems exhibit **epistemic failure that does not bear on the system's continuity** (§3.5) — they can be wrong, even badly, and nothing about being wrong threatens their persistence as the same system. A system that cannot be wounded by its own errors is not maintaining an identity; it is just running. This deficit is what Condition 3 is built to exclude, and it is the gap the paper claims ENGRAM closes. We flag it here because it reframes the whole review: the threshold is not "does the system remember?" but "can the system's errors cost it something, structurally, from the inside?"

## 2.3 The belief-revision lens: AGM and Hansson

Kahl's Condition 3 asks for *rational* arbitration, but does not formalize what makes a revision rational. The standard formalization is the **AGM framework** (Alchourrón, Gärdenfors & Makinson, 1985; df_0049): three operations — *expansion* (add a belief without a consistency check), *contraction* (remove a belief and what entails it), and *revision* (incorporate a belief while staying consistent) — governed by rationality postulates (K\*1–K\*8 for revision).

Two refinements matter for an agent substrate:

- **Belief bases, not belief sets.** Classical AGM operates on logically-closed belief sets — every consequence of what you believe is itself a belief. No computational system can store that; it is infinite. **Hansson (1999)** re-grounded the framework on *belief bases* — finite sets *not* closed under consequence — which is the right level for a real system. This is the level at which ENGRAM, or any graph of explicit claims, actually lives.
- **The two postulates that do the work.** Hansson replaced AGM's controversial *Recovery* postulate (the claim that contracting then re-adding a belief returns you to exactly where you started — which immutable, provenance-bearing stores reject, since re-adding a retracted claim creates *fresh* provenance, not a rollback) with two others:
  - **Relevance** — contraction may only remove beliefs that actually contributed to what is being removed; no gratuitous discarding.
  - **Core-Retainment** (df_0053) — verbatim sense: *every removed belief must have genuinely contributed to deriving the contracted belief.* Nothing is dropped that did not earn its removal by being part of the derivation.

*Plain terms:* when an agent withdraws a belief, a *principled* withdrawal touches exactly the things that depended on it — no less (or the contradiction survives), no more (or you have amnesia, not correction). Relevance and Core-Retainment are the formal statement of "touch exactly what depended on it."

*Forward pointer:* this lens is why the paper can speak about ENGRAM's cascade in *formal* terms rather than just architectural ones — Ch4 argues the `derives_from` cascade satisfies Relevance and Core-Retainment **at the architectural level** (every tainted claim provably depended on the retracted source via graph traversal), where comparable systems satisfy them, if at all, only at retrieval-filtering time (dv_0613). We note for honesty that ENGRAM does *not* carry a formal AGM proof (Kumiho does, with a passing test suite); the claim is structural alignment at the belief-base level, not a theorem.

## 2.4 The individuation machinery: type/token and closest-continuer

Two more tools, both used heavily downstream.

**Peirce's type/token distinction** (1906; df_0047). A *type* is "a definitely significant Form" that "does not exist; it only determines things that do exist"; a *token* is "a Single event which happens once and whose identity is limited to that one happening." The word "the" appears three times on this line of your screen — one *type*, three *tokens*.

This is the hinge for the Condition 2 extension. For an analog substrate, exact reproduction is a thought experiment, so type and token never visibly come apart. For a *digital* substrate they separate cleanly: two ENGRAM instances restored from the same git commit are **type-identical** (they instantiate the same epistemic form) but become **token-distinct** the moment they begin operating (each accumulates its own commitments, fires its own cascades, develops its own history). The paper's proposed reading of Condition 2 turns on token-distinctness rather than impossibility-of-reproduction: a digital agent is individuated by *which token's history it carries*, and reproduction-into-instances is precisely where the bifurcation that individuates them occurs. We note plainly (per the definition node) that applying type/token to computational artifacts is *our* extension — the standard references do not discuss the digital case — so this is framework-building, not exegesis of Peirce.

**Nozick's closest-continuer theory** (1981; df_0046). Nozick analyzes identity over time as four components: *continuity* (y at t′ is the same as x at t iff y is an appropriate continuant of x), *comparative* (y must be the *closest* continuant), *threshold* (closeness must clear a minimum — a barely-related continuant fails even if it is the closest available), and *uniqueness* (y must be *uniquely* closest; ties — fission — mean neither branch is x).

The paper **keeps Nozick's first three components** as scaffolding and **drops uniqueness** — because for a clonable digital agent, fission is not a paradox to be legislated away but the normal case, and the type/token reading already handles it (both branches are real token-distinct continuants). It also *deflates* Nozick's deliberately-underspecified "closeness metric" into something concrete — a retrieval profile over the accumulated graph. *Forward pointer:* this is the backbone of Chapter 5's identity-as-history thesis (dv_0597 / dv_0598); we introduce it here only as machinery.

## 2.5 The cognitive-science lens: Complementary Learning Systems

The final lens is empirical rather than philosophical: **Complementary Learning Systems (CLS) theory** (McClelland, McNaughton & O'Reilly, 1995; Kumaran, Hassabis & McClelland, 2016). CLS explains how brains learn without catastrophic interference by using *two* systems — a fast hippocampal system that rapidly encodes specific episodes, and a slow neocortical system that gradually integrates them into structured knowledge.

Read at the function level (dv_0722), CLS supplies three constraints that hold for *any* complementary-learning system regardless of substrate (biological tissue, model weights, or symbolic graph):

1. **Fast/slow rate dichotomy** — fast specific encoding paired with slow integrative composition, as a structural property of the memory system, not an implementation detail.
2. **Interleaved-learning operator** — new instances must be integrated *interleaved* with prior knowledge to avoid catastrophic interference; consolidation is the operator that moves information between the subsystems.
3. **Hippocampus-as-teacher asymmetry** — the fast system *generates training signal for* the slow system (it does not merely answer queries); the fast subsystem actively maintains the slow one.

**How ENGRAM relates to CLS — the positioning claim.** This is a framing decision, ratified with Lei (qu_0247, resolved by ob_2049), and it is worth getting exactly right because the obvious move is wrong. The tempting move is to say "ENGRAM is the hippocampal half, and model weights are the neocortical half." We **reject** that. Lei's editorial framing, verbatim: *"I lean towards a dedicated paragraph explaining ENGRAM as a unique 'hybrid' system, not directly mapping to one single CLS layer."*

The positioning the paper takes (dv_0724) is that **ENGRAM is its own architectural class — a third design point alongside CLS's two biological subsystems**, for three reasons:

- **It honors all three CLS constraints at the function level** — so CLS is a legitimate comparison frame, not a foreign one.
- **It realizes *both* CLS subsystems within a single symbolic substrate** (ob_2052): observations are the episode-analog (instance-tied, provenance-bearing, fast, sparse), and `inductive_generalization` derivations plus consolidation are the pattern-emergence-analog (logical construction over many observations, slow, integrative). The fast/slow distinction is real *within* ENGRAM — not split across ENGRAM-versus-weights.
- **It adds integrity primitives the biological substrate cannot enforce** — explicit per-claim provenance, first-class retraction-with-cascade, and designed working-set forgetting. These are categorically novel: neither hippocampal nor cortical, neither biological replay nor weight update.

So CLS enters the paper as a *comparison framework that names an overlapping problem-shape from a different premise (neuroscience)*, not as a parent taxonomy ENGRAM slots into. *Forward pointer:* Ch3 §3.4 details the consolidation rhythm (nap / bedtime / sleep) that instantiates the slow-integration operator symbolically; the detailed mechanism-to-function mapping is mechanism work, not review.

*Honest scope:* the dual-instantiation and third-class claims are framing, computed at moderate confidence (dv_0724 ≈ 0.83); they are positioning, not satisfaction proofs. The CLS function-level constraints (dv_0722 ≈ 0.93) are the firmer ground.

## 2.6 What this sets up

The reader now has the full apparatus: a *threshold* (Kahl's three conditions, four constraints, and the epistemic-failure deficit), a *formal lens* on what rational revision requires (AGM / Hansson Relevance + Core-Retainment), the *individuation tools* for handling reset and defining identity-as-history (type/token, closest-continuer), and a *cognitive-science comparison frame* that positions ENGRAM as its own architectural class.

Chapter 3 describes what ENGRAM *does*, mechanism by mechanism, in the order this apparatus demands — and Chapter 4 returns to each condition and constraint above with an honest, per-condition verdict. Nothing in this chapter is a verdict; everything in it is the ruler against which Chapter 4 measures.

---

## Provenance map (draft scaffolding — not for final prose)

| Claim (this chapter) | Substrate node(s) | Type / confidence |
|---|---|---|
| Personal-identity lineage (Locke / Parfit / Nozick) as inherited vocabulary | df_0046 (Nozick) + Ch5 substrate dv_0597/dv_0598 | def / framing |
| LLM agents break both human-continuity assumptions (interrupted thread + duplicable substrate) | dv_0578 / ob_1598 (reset-symmetry) | — |
| OCC = Kahl 2026, 3 conditions + 4 constraints | df_0037 | def |
| Condition 1 — Diachronic Constraint (verbatim) | **df_0058** (supersedes df_0038) | def |
| Condition 2 — Non-Interchangeability Under Reset (verbatim + §8.3 test + §4.3 rule) | df_0039 | def |
| Condition 3 — Self-Maintaining Arbitration (verbatim; unified/internal/subject-preserving) | df_0040 | def |
| Constraint A / B / C / D (verbatim source sentence) | df_0041 / df_0042 / df_0043 / df_0044 | def |
| Epistemic-failure-without-continuity-cost deficit (Kahl §3.5) | df_0037 / kahl_occ_first_hand_read | def |
| AGM framework (expansion/contraction/revision; K*1–K*8) | df_0049 | def |
| Hansson belief-base + Relevance + Core-Retainment (verbatim sense); Recovery rejected | df_0053 (+ df_0051, df_0052) | def |
| Cascade satisfies Relevance/Core-Retainment at architectural (not retrieval) level | dv_0613 (forward pointer to Ch4) | 0.38 |
| Peirce type/token; digital substrates split them; extension is ours | df_0047 | def |
| Nozick closest-continuer; keep 3 components, drop uniqueness, deflate metric → retrieval profile | df_0046 | def |
| CLS three function-level constraints (substrate-agnostic) | dv_0722 | 0.93 |
| ENGRAM realizes BOTH CLS subsystems in one symbolic substrate (obs = episode-analog; gen-dvs = pattern-emergence) | ob_2052 | 0.85 |
| ENGRAM as CLS third design point / own architectural class (3-leg argument) | dv_0724 | 0.833 |
| Lei's editorial: "unique hybrid system, not one CLS layer" (verbatim) | ob_2049 | 0.85 |
| CLS-mapping question resolved (own-class, not half-of-CLS) | qu_0247 (resolved) | — |

**Drafting notes (for Lei):**
- **The structure decision** (per-tradition vs condition-by-condition) is the one un-ratified Ch2 item from the canonical plan — see the banner at the top. My recommendation is per-tradition (this draft), to avoid duplicating Ch4's condition-by-condition scaffolding.
- I kept all OCC condition/constraint text **verbatim** from the first-hand read, with plain-gloss + example alongside (Discipline N). The verbatim ruler is load-bearing for a review chapter — the satisfaction arguments in Ch4 only have force if the threshold is quoted, not paraphrased-toward-the-verdict.
- I **deliberately withheld every satisfaction verdict** — each appears only as a one-line "forward pointer" so the chapter reads as a neutral ruler. If you'd rather Ch2 preview the verdicts more fully, that's a quick expansion; I erred toward review-neutrality.
- **Correct-on-the-spot note:** while grounding this chapter I found `df_0038`'s recall_summary still carried the stale "ENGRAM satisfies partially" read for Cond 1; I superseded it to `df_0058` (Kahl verbatim unchanged; satisfaction repointed to the ratified dv_0926). The provenance map above already cites df_0058.
- Archived 2026-05-09 `ch3_section_3_1`–`3_4` drafts contain condition-by-condition cog-sci review content that could be mined if you pick the condition-by-condition structure instead.
- Ch5 (identity-as-history) uses the §2.4 machinery as its backbone; I introduced type/token + Nozick here only as tools, leaving the thesis itself to Ch5 to avoid overlap.
