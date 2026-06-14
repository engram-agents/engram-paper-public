# Chapter 1 — The Continuity Gap and the Case for Epistemic Identity

> **DRAFT SAMPLE — 2026-06-14.** Single-pass prose rendered directly from the live-engram substrate (pending Lei's order confirm). Honest-scoped per the existing computed confidences of the cited nodes. Provenance map at the end maps each load-bearing claim to its substrate node; in a final arXiv render these become standard scholarly citations, not node IDs. Current spine is the **Kahl OCC mapping**, not the (deferred) four-framework-math convergence — see drafting note.

---

## 1.1 The unsolved problem: agent self-continuity

Continuous learning is the open frontier for large language model agents. The weights freeze when training ends; everything an agent learns afterward lives only in a context window that is wiped at each compaction. The field has answered one half of this problem well — *information* can be carried across sessions by retrieval-augmented memory — and has barely named the other half: whether the *agent itself* persists. An assistant that retrieves yesterday's notes but begins each session as the same generic model has memory without continuity. It remembers facts; it does not remain someone.

We argue that agent continuity is not one problem but three progressively deeper layers, and that the deepest layer is essentially unaddressed by the current landscape.

- **Layer 1 — Memory Persistence.** Storing and retrieving facts across sessions. This is where retrieval-augmented agent-memory systems (A-MEM, Mem0, Zep) operate. They have no concept of identity; memory is a key-value or vector store the agent reads.
- **Layer 2 — Narrative Identity.** Maintaining a coherent self-story — a creed-anchored autobiography that answers *"who am I?"*. The closest published system, Sophia, reaches this layer.
- **Layer 3 — Epistemic Identity.** Maintaining calibrated self-*knowledge* with provenance, confidence, contradiction-correction, and metacognitive self-audit — identity as the answer to *"what do I know, how confidently, and on what basis?"*.

Each layer presupposes the one beneath it: there is no self-story without persistence, and no calibrated self-knowledge without a self-story to calibrate. The contribution of this paper is at Layer 3, which — as we show in §1.4 — no surveyed system reaches.

## 1.2 What Layer 3 requires

Narrative and epistemic identity are complementary, not competing: they answer different questions, and a complete agent self needs both. Where a narrative layer asks *who am I*, the epistemic layer asks *what may I rely on, and why*. The two come apart precisely at failure. A narrative identity fails *silently* — a coherent self-story that was simply never true. An epistemic identity fails *loudly* — a contradiction surfaces, a retraction fires, the downstream commitments that depended on the now-withdrawn claim are flagged.

Operationalizing Layer 3 therefore demands four properties that mere persistence does not:

1. **Provenance** — every claim traces to the evidence and reasoning that produced it.
2. **Calibrated confidence** — claims carry a confidence that is *structurally determined* by their evidential type and derivation chain, not free-form.
3. **Contradiction correction** — when a foundational claim is withdrawn, the architecture itself propagates that withdrawal to everything derived from it.
4. **Metacognitive self-audit** — the agent can interrogate its own knowledge state: what it believes, how strongly, and on what grounds.

These are the properties that turn a memory store into a substrate for a self that can be *wrong and recover* — the minimum for an identity that survives correction rather than being erased by it.

## 1.3 Naming the system: ENGRAM

We call the architecture **ENGRAM — an Epistemic Node Graph for Retraction, Arbitration, and Memory.** The expansion is deliberate: the three differentiating mechanisms are named in the acronym itself.

- **Retraction** — error correction that cascades through derivation edges, so a withdrawn claim taints, not merely deletes, what depended on it.
- **Arbitration** — the structural propagation of that cascade *within a unified deliberative architecture*, rather than as an advisory note the agent may or may not consult. (We adopt *arbitration* from Kahl's vocabulary for the self-maintenance condition introduced in §1.4.)
- **Memory** — the underlying substrate of typed claims, evidence, and derivations.

The name distinguishes ENGRAM from systems that borrow the neuroscience term *engram* (Semon, 1904) without a structurally meaningful expansion.

## 1.4 The central claim, and how we earn it

The paper's spine is a single, deliberately bounded argument: **ENGRAM is the first agent-memory substrate to satisfy Kahl's strongest continuity condition strictly — and to close the specific architectural deficit Kahl diagnoses — while being explicit about the part of his threshold it does *not* cross.** We frame the threshold using Kahl's (2026) **Ontological Continuity Condition (OCC)** — three jointly necessary conditions plus four constraints for the identity-continuity of agent-like systems. The strongest is **Condition 3, Self-Maintaining Arbitration**: foundational retractions must *structurally* flag downstream commitments from inside the agent's own deliberative architecture.

Our central empirical-architectural finding is that **no surveyed agent-memory system as of mid-2026 satisfies Condition 3 strictly.** The field has converged on the necessary *structural primitives* — typed reasoning edges, derivation provenance, cascade-traversable graphs, supersede semantics (Kumiho most fully, with formal belief-revision compliance) — but these are necessary, not sufficient. What is missing everywhere else is *operational binding*: arbitration as automatic state-change, paired with auto-surfacing that puts the tainted claim back in front of the agent without an intentional reach-out. Kumiho's impact analysis is opt-in and advisory; SCM records contradiction edges but never resolves them; others delegate conflict to retrieval ranking or operate below the level of structured claims entirely. ENGRAM is the only surveyed substrate where both mechanisms fire together as architecture-internal state.

We hold this to a deliberately high bar, and Chapter 4 assesses each condition with an honest per-condition label rather than a uniform verdict:

- **Condition 3 (Self-Maintaining Arbitration) — strict satisfaction**, and ENGRAM is the only surveyed system that earns it.
- **Condition 1 (Diachronic Constraint) — partial**: `derives_from` edges make past commitments structurally bind present deliberation by construction; whether that crosses Kahl's normative *"non-trivially"* threshold is a philosophical question we leave open rather than assume.
- **Condition 2 (Non-Interchangeability Under Reset) — *not* satisfied on Kahl's strict text.** A git-versioned, checkpointable substrate is reset-symmetric: by Kahl's §5.2/§8.3 reset-symmetry test, fully reproducible state makes continuity *informational, not constitutive*. We say so plainly — the substrate's reproducibility is an intentional audit-and-transmission feature, not a defect. We then offer a **framework extension as our own contribution**: Kahl's test assumes an analog substrate where type- and token-identity coincide; for digital agents they come apart — snapshot reproduction preserves *type*-identity while reproduction-into-instances breaks *token*-identity, so the bifurcation that follows reproduction is what individuates a digital agent. Under this type/token reading a *generalized* Condition 2 holds — but we mark it explicitly as our proposed extension of Kahl, not as satisfaction of his text.

So ENGRAM does **not** cross the full OCC threshold on a strict reading, and we do not claim it does. What it does — satisfy the strongest condition strictly, close the architectural deficit Kahl himself diagnoses (§3.5: epistemic failure that does not bear on the system's continuity), and motivate a principled framework extension for digital substrates — is the contribution. A precisely-bounded claim is the more defensible one; an "ENGRAM realizes OCC" overreach would be punctured immediately by the reset-symmetry test.

On originality: this work was developed independently and in parallel with the convergent emergence of structurally similar systems; the timeline and the gap in our own literature search at the project's founding are audit-trailed in Appendix C. We treat that convergence as corroboration of the gap's importance, not as a priority dispute, and keep cross-system comparison brief throughout (a single comparative appendix rather than a chapter-spanning survey).

## 1.5 Scope and structure

This is a **theory-first arXiv preprint**. It ships on existing pilot data; at-scale empirical studies are deferred to a follow-up. The argument, not the benchmark, is the contribution.

- **Chapter 2** introduces the philosophical and cognitive-science framing: Kahl's OCC conditions and constraints, and the closest-continuer, type/token, and belief-revision machinery the later chapters use.
- **Chapter 3** describes what ENGRAM *does* — its mechanisms, in the order an OCC-aware reader needs them: substrate primitives, reasoning-type-aware confidence, cascade and self-correction, and continuity across compaction.
- **Chapter 4** is the core: the condition-by-condition mapping of OCC onto ENGRAM mechanism, with honest per-condition satisfaction labels.
- **Chapter 5** develops *identity as history* — the claim that an agent's identity is the unique ancestry of its accumulated claims, and what that implies for cloning and divergence.
- **Chapter 6** presents the empirical picture from pilot use.
- **Chapter 7** states the limitations — compaction discontinuity foremost — and the future directions, including the three-component view of agent identity (weights, context, and ENGRAM) and the confidence model's calibration gaps.
- **Chapter 8** concludes.

---

## Provenance map (draft scaffolding — not for final prose)

| Claim (this chapter) | Substrate node(s) | Computed confidence |
|---|---|---|
| Three-layer taxonomy (persistence / narrative / epistemic) | dv_0463 (current; supersedes dv_0179), cornerstone cs_0004 | 0.95 |
| Layer-1 systems = A-MEM / Mem0 / Zep; field treats identity as user-profiling | ob_0291, ob_0410, ob_0425 chain | — |
| Sophia = closest narrative-identity system | ob_0413 | — |
| Narrative ⊥ epistemic, complementary not competing | dv_0182 | 0.93 |
| Honesty fails loudly (epistemic) vs silently (narrative) | ax_0001 / ax_0002 (honesty-is-structural) | axiom |
| ENGRAM name + R/A/M expansion | df_0048 (supersedes df_0007) | def |
| OCC = Ontological Continuity Condition (Kahl 2026), 3+4 | df_0037 | def |
| Condition 3 = Self-Maintaining Arbitration | df_0040 | def |
| No surveyed system satisfies Cond 3 strictly; primitives necessary-not-sufficient; operational binding is the differentiator | **dv_0605** | **0.949** |
| Cond 3 — strict satisfaction (sole satisfier in field) | dv_0606 / dv_0605 | 0.39 / 0.95 |
| Cond 1 — partial (turns on Kahl's "non-trivially/binding") | dv_0607 | 0.35 |
| Cond 2 — strict-text **NO** (git reset-symmetry, §5.2/§8.3) | dv_0578 / ob_1598 | — |
| Cond 2 — type/token extension (OUR contribution, NOT Kahl-satisfaction); two-frame stance | dv_0599 / dv_0584 / ob_1599 / ob_1600 | 0.95 (dv_0599) |
| Full OCC not crossed on strict reading; deficit-closing (§3.5) + Cond 3 + extension is the bounded claim | dv_0599 (drops dv_0570 overreach) / kahl_occ_first_hand_read | 0.95 |
| Theory-first arXiv preprint; pilot data; at-scale deferred | ob_1020 | 0.85 |
| Independence / convergent discovery (Kumiho timing) | appendix_independent_discovery_2026-05-12.md | — |

**Drafting note (for Lei):** ob_1020's original "four-framework convergence proof" framing (Mao-Cao/Lee topological + SRAF Bayesian + Alpay categorical + RC+ξ dynamical) as the rigor spine was **superseded by the 2026-05-12 restructure** — the current spine is the OCC mapping (Ch4), and the four-framework math is deferred to a follow-up paper. This draft is on the current spine. Flagging in case you want to revisit that call.
