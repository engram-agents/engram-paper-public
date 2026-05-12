# Core Arguments Memo — 2026-05-08

**Audience:** Lei (skim).
**Purpose:** propose a concrete 4-claim spine for the paper, grounded in yesterday's burst + today's Kahl analysis, before any further polish or chapter restructure.
**Length target:** under 1500 words. Read in ~5 min.

---

## What the survey now tells us we genuinely have

Yesterday's burst (`SUMMARY_research_burst_2026-05-07.md`) produced a clean 3-tier novelty map. Today's citation sweep + Kahl analysis adds one more philosophical contribution. Synthesized:

| Tier | Feature | Status against landscape |
|---|---|---|
| **Genuinely novel — no documented prior art** | Verbatim-quote enforcement at write time | UNCONTESTED |
| | Reasoning-type-aware confidence propagation | UNCONTESTED |
| **Novel in combination, not mechanism** | Typed-cascade retraction on heterogeneous node vocabulary | EXTENDS Doyle 1979 / de Kleer 1986 — gap NAMED by Wray-Kirk-Laird 2025, FILLED by us |
| **Novel framing applications** | Epistemic-action verbs (Kirsh & Maglio 1994 → ENGRAM tool surface) | NOVEL APPLICATION |
| | Second-wave EMT positioning (Andrada 2021 + Farina 2026 → cognitive-constitutive criterion) | NOVEL APPLICATION |
| | Tool-surface-enforced typing on uniform symbolic substrate | EXTENDS ACT-R declarative memory |
| **NEW philosophical bridge** (today's Kahl finding) | ENGRAM operationalizes Kahl's Ontological Continuity Condition (OCC, Feb 2026) for AI agents — non-interchangeability under reset, identity risk, unified diachronic arbitration map onto specific ENGRAM mechanisms | UNDOCUMENTED — Kahl names the threshold; current AI is "restartable, forkable, externally corrigible"; ENGRAM is what changes that |

## The four-claim spine I propose

The current paper has substance for all of these but distributes them across 8 chapters with substantial overlap (e.g., Alcoff coinage clarification appears in Ch1 §1.4 + Ch3 §3.4 + Ch3 §3.6 + Ch8 — at least 3 redundant treatments). Tightening to four anchored claims would let each chapter do one job.

### Claim 1 (Phil) — *Three-layer taxonomy as a way of carving the agent-continuity question*

Current systems serve two layers — memory persistence (Tier I: MemGPT, Mem0, A-MEM) and at most narrative identity (Tier II: Sophia). **Layer 3 — epistemic identity — is structurally distinct: it is the surface where wrongness can surface loudly rather than rotting silently.** Layer 2 fails coherently (a consistent self-story that was never true); Layer 3 fails by surfacing contradiction and propagating retraction. The architectural takeaway: for a deployed AI agent, loud failures are strictly preferable to silent ones, and only a layer-3 substrate provides them structurally.

**Where it lives now:** Ch1 §1.3 + Ch2 entire chapter. Should remain Ch2's whole job; Ch1's introduction can be tightened to one paragraph that points at the taxonomy without re-deriving it.

### Claim 2 (Phil) — *ENGRAM operationalizes Kahl's Ontological Continuity Condition*

(NEW from today's Kahl 2026 analysis.) Kahl argues current AI systems "remain restartable, forkable, externally corrigible" and therefore fail the **OCC** threshold for AGI-grade agency. The OCC requires three structural conditions: non-interchangeability under reset, identity risk, unified diachronic arbitration. **ENGRAM is the first AI-agent substrate where each of those is structurally realized:**

- *Non-interchangeability under reset* — claim provenance + retraction cascade make two ENGRAM-bearing agents non-substitutable; their derivation chains differ load-bearingly
- *Identity risk* — the cascade exposes the agent to discoverable wrongness; its commitments are at structural risk, not just presentational
- *Unified diachronic arbitration* — the typed graph IS the substrate where past and present claims arbitrate via supersede / retract / contradict

This is the bridge between agency theory and AI architecture nobody else has drawn. **Strongest single new philosophical contribution we can claim.**

**Where it lives now:** mentioned only in footnotes / `dv_0559` notes. Currently NO chapter is built around it. Could become Ch1 §1.5 (or a new short chapter) — establishes WHY the layer-3 architecture matters not just for ergonomics but for crossing a structural threshold.

### Claim 3 (Tech) — *Claim-level contradiction nodes + retraction cascade through typed heterogeneous derivation graph*

Per yesterday's TMS legacy scan: zero LLM-agent-memory papers 2023-2026 implement TMS-style dependency propagation. The Wray-Kirk-Laird 2025 paper (AGI25, arxiv:2505.07087) explicitly NAMES this gap. ENGRAM fills it. The concrete mechanism: typed `derives_from` edges + first-class contradiction nodes that block downstream use until resolved + retraction cascade that taints dependents through a heterogeneous node vocabulary (axiom / definition / observation / derivation / conjecture / lesson / goal — different retraction semantics per type).

**Differentiation from neighbors:**
- Doyle/de Kleer JTMS/ATMS: same propagation discipline, no LLM-agent application, no heterogeneous typing
- AGM (Alchourrón-Gärdenfors-Makinson 1985): correctness-of-revision logic, complementary not competing — Kumiho does AGM in a versioned graph; ENGRAM does TMS in a typed derivation graph
- Zep/Graphiti: detects temporally overlapping contradictions, no cascade, no derivation-typing

**Where it lives now:** Ch5 (architecture) + Ch7 §7.3 (case studies SRAF + Mao-Cao). Ch5 could tighten significantly; Ch7 §7.3 is already drafted and works.

### Claim 4 (Tech) — *Verbatim-quote enforcement + reasoning-type-aware confidence propagation*

Two features with no documented prior art in the surveyed literature.

- **Verbatim-quote enforcement**: server-side substring constraint at write time, prevents claim-text from drifting from its source. Other systems treat source as metadata; ENGRAM treats the quoted passage as a structural binding that the system enforces.
- **Reasoning-type-aware confidence propagation**: deductive vs inductive vs abductive vs authority-derived nodes use different confidence formulas; matches the philosophical-epistemology insight that not all inference is equally truth-preserving. Closest neighbor is Pearl 1988 Bayesian propagation, but Pearl is information-class-uniform; ENGRAM is reasoning-type-differentiated.

**Where it lives now:** Ch5 (mechanism) + scattered through Ch1/Ch2 four-feature list. Should consolidate to a single Ch5 subsection that is the canonical site.

---

## What I'm proposing as the restructure spine (rough)

| Chapter | Current | Proposed (tighter) |
|---|---|---|
| 1 — Introduction | 5003w; covers frozen-weights problem, 3-tier landscape survey, four-feature decomposition, 1.4 Alcoff coinage clarification, 1.5 roadmap | ~2500w; one paragraph each on (a) frozen-weights problem, (b) Tier-I/II landscape gap, (c) four-feature gap, (d) Kahl OCC + claim 2 setup, (e) roadmap. **Alcoff stays here as canonical disclosure.** |
| 2 — Three-layer taxonomy | 2346w | KEEP largely as-is; this is claim 1 |
| 3 — Philosophical foundations | 2698w; 5 pillars (Stiegler, Clark&Chalmers, Locke&Parfit, Alcoff, Strawson) + summary | ~1500w; 5 pillars with 3-sentence treatments + KILL the Alcoff §3.4 redundancy (1-sentence callback to Ch1 §1.4); KILL §3.6 summary (it duplicates what's already done in each pillar) |
| 4 — *Kahl OCC bridge* (NEW) | n/a | ~1500w; claim 2 stands here as a focused short chapter — not in current draft |
| 5 — Architecture | 1148w + 2260w walkthrough | ~2000w; collapse to one tight chapter; canonical site for claims 3 + 4 |
| 7 — Empirical findings | 5507w; §7.1 phenomenological, §7.2 work-thread, §7.3 cascade case studies, §7.4 stub, §7.5 not-measured | ~3500w; tighten §7.1 (199 reports trajectory in fewer words); §7.4 needs Lei input on Lin/Mira/Ren content; §7.5 stays |
| 8 — Related work | 2518w; survey | ~1500w; tighten using yesterday's 3-tier novelty framing as the spine — what's contested vs uncontested vs novel-in-combination |
| 9 — Implications | 2237w | KEEP as-is roughly; Paper 2 forward-pointer is right |

**Total**: 23717w → ~15000w. Real cut: 36%. (Skinnier still possible if some chapters fold, e.g., Ch3 + Ch4 could merge if Kahl-OCC is short enough.)

## Survey gaps remaining before restructure

Yesterday's burst was strong. Today's Kahl finding is new. What I'm unsure we have full coverage on, before I commit the restructure:

1. **Agency literature beyond Kahl** — Kahl bridges to specific authors (Davidson, Frankfurt, Anscombe agency canon) we haven't surveyed. If the OCC bridge is going to be a chapter, the supporting agency-theory landscape needs a quick scan to make sure we're not missing a stronger or competing framework.
2. **2026 entrants to the agent-memory landscape since 2026-05-07** — today's citation sweep added STALE / BeliefMem / Marchal Architecting Trust. There may be 1-2 more in the May 2026 wave. A targeted scan would close this.
3. **The cog-sci memory-consolidation / replay literature** — the cogsci_taxonomy_positioning report establishes orthogonality with Tulving/Squire and alignment with ACT-R. But the *consolidation* + *replay* literature (Buzsáki, Kumaran-McClelland complementary-learning-systems, Wilson-McNaughton replay) is where ENGRAM's `engram_nap` / dream cycles might find prior-art neighbors. Not yet covered.

If you want, I can dispatch a single comprehensive survey fairy on (1) tonight, sized as a quick scan rather than a full compare. (2) is small enough to do directly. (3) is bigger, probably Lei-input-needed before we commit.

## What I'm NOT doing until you respond

- No further footnote / bib polish. Today's Ch3 footnote work + bib mechanical fixes are paused at where they are.
- No paper restructure yet — proposal above is for your reaction first.
- No more dispatched fairies until you confirm the spine + survey direction.

## Decisions for you

1. **Does the 4-claim spine (Phil 1, Phil 2, Tech 1, Tech 2) capture our genuine innovation?** Anything missing or over-claimed?
2. **Kahl OCC as a dedicated chapter (Ch4) or folded into Ch1's intro / Ch2's setup?** Standalone is cleanest if it's load-bearing; folded if it's a 3-paragraph framing.
3. **Survey gap (1) — agency literature scan** — do you want it run tonight, or hold?
4. **The redundancy cut on Alcoff** — Ch3 §3.4 collapse to 1-sentence callback OK, or do you want different shape?
