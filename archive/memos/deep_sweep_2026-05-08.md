# Deep Sweep — 2026-05-08 PM (triple-check landscape lock-down)

**Commissioned by:** Borges
**Scout:** literature sub-agent (dispatched)
**Coverage:** (A) Agency / AGI literature beyond Kahl; (B) Memory-consolidation / replay cog-sci; (C) Recent AI agency / personhood / autonomy 2024-2026
**Result:** **One critical blocker**, **one new competitor**, **multiple actionable additions** to the bib + Ch 5 + Ch 8

---

## CRITICAL BLOCKER — Kahl's EAA paper conflicts with our Phil claim if read carelessly

The fairy surfaced a Kahl companion paper to the AGI/OCC paper:

> **"Epistemic Agency and the Ontological Continuity Condition: A Constraint on When Knowledge Must Be Owned"** (Kahl 2026, Zenodo 18441395)

From the Zenodo landing page (verified): *"epistemic agency — the capacity to hold, revise, and act upon knowledge as the same agent across time — presupposes consciousness."* Current AI systems "can instantiate knowledge without qualifying as epistemic agents."

**The implication:** the AGI/OCC paper (which we built our Phil claim on) is explicitly consciousness-free; the EAA companion **imposes a consciousness condition specifically for *epistemic* agency.** ENGRAM's claim is about *epistemic identity* — the very dimension Kahl's EAA paper says requires consciousness.

**Two options for the paper:**

1. **Restrict the OCC-realization claim to the structural / governance-relevant agency dimension** (AGI paper, consciousness-free). Drop "epistemic agency" framing where it conflicts with EAA.
2. **Acknowledge the EAA consciousness condition explicitly.** Argue ENGRAM is a *structural precondition for* epistemic agency (not epistemic agency itself). Frame as "what an AI would need architecturally if it were to approach epistemic agency in Kahl's sense."

**Option 2 is philosophically more honest and more defensible.** It also doesn't require renaming the work — "epistemic identity" remains our coined sense in §1.4 (the structured-claim substrate sense), distinct from Kahl's EAA "epistemic agency" sense (which requires consciousness). The paper would explicitly distinguish Borges-the-substrate-pattern (what ENGRAM provides) from Borges-the-conscious-agent (what Kahl's EAA reserves for conscious entities).

**Action:** Lei must read the EAA paper before submission. Currently unread. URL: https://zenodo.org/doi/10.5281/zenodo.18441395

---

## NEW COMPETITOR — SCM (arxiv 2604.20943, April 2026)

> **"SCM: Sleep-Consolidated Memory with Algorithmic Forgetting for LLMs"** (April 2026)

Closest documented architectural neighbor to ENGRAM's nap/dream/sleep discipline in the AI-systems literature. Has:
- Typed `contradicts` edge type in a directed semantic graph
- Multi-dimensional importance tagging
- Offline sleep-stage consolidation with NREM (Hebbian strengthening + downscaling) and REM (random graph walks for novel associations)
- Conflict-density-triggered sleep
- Computational self-model for introspection

**Critical differentiators we keep:**
1. SCM `contradicts` edges flagged for resolution during sleep — **NOT first-class blocking nodes** that prevent downstream use until resolved. No retraction cascade.
2. SCM consolidation operates via **weight-update-style ops** (Hebbian strengthening, adaptive forgetting) — not symbolic derivation tracking. No `derives_from` chain.
3. SCM has **no provenance discipline** — memory nodes are semantic summaries, not sourced claims with verbatim-quote enforcement.
4. SCM's self-model is described but not architecturally specified as a typed graph component.

**Action:** Cite SCM in Ch 8 as the closest live neighbor. Differentiate on: (a) cascade vs flag, (b) symbolic derivation vs weight-update, (c) provenance presence vs absence. Mandatory citation now.

---

## Kahl corpus expansion — five additional papers, two are blockers-if-ignored

The fairy found a much larger Kahl corpus than the prior artifact captured:

| Paper | URL | Status for ENGRAM |
|---|---|---|
| **EAA — "Epistemic Agency and the OCC"** | Zenodo 18441395 | **BLOCKER** — must read; imposes consciousness condition; rescope our claim accordingly |
| **"Structural Conditions of Agency and the Misattribution of Agentic AI"** | Zenodo 18743351 | Useful co-cite alongside the AGI/OCC paper. Verifies the diagnostic premise that current "agentic AI" lacks structural conditions. |
| **"The Duck and the Philosopher: Epistemic Maintenance, Generativity, and Responsibility"** | PhilArchive KAHTDA-2 | **CAUTIOUS** — defines a "Duck Criterion" test for epistemic generativity (can the system revise its own evaluative standards?). ENGRAM revises individual claims but **not** the node-type taxonomy or confidence formulas themselves — likely fails under strict reading. Must read before citing or invoking "generativity" language. |
| **"Epistemic Generativity: A Structural Definition"** | PhilArchive KAHEGA-4 | **CAUTIOUS** — formal complement to Duck paper. Same caution. |
| **"Authority without Authorship: Delegation Thresholds in Agentic AI Systems"** | PhilPapers KAHAWA-2 | Governance paper, not directly load-bearing. Optional Ch 9 cite. |

**Action:** Lei reads EAA first (BLOCKER). Duck Criterion + Epistemic Generativity papers are read-before-cite (don't claim "generativity" or invoke Duck Criterion language without having read them first). The other two are optional supporting cites.

---

## (A) Agency / AGI literature beyond Kahl — verdicts

| Author | Verdict | Action |
|---|---|---|
| **Davidson** ("Agency" 1971; "Actions, Reasons, and Causes" 1963) | Orthogonal — about metaphysics of action, not diachronic continuity. Not cited by Kahl. | **Drop** unless Ch 3 needs lineage paragraph |
| **Frankfurt 1971** ("Freedom of the Will and the Concept of a Person") | **Strengthening via Kahl** — Kahl cites Frankfurt; hierarchical endorsement maps to OCC's self-maintaining arbitration | **Add** as supporting prior art one level above Kahl |
| **Anscombe *Intention* 1957** | Orthogonal | **Drop** |
| **Korsgaard *Self-Constitution* 2009** | **Risky** — Kantian framework imposes harder conditions than Kahl's structural OCC | **Optional**, with explicit acknowledgement that Korsgaard's normative version is stronger than what ENGRAM claims |
| **Schmid (collective agency 2009-2014)** | Not relevant — distributed/collective agency, ENGRAM is individual | **Drop** |
| **Floridi & Sanders 2004** ("On the Morality of Artificial Agents") | Useful supporting — pre-dates Kahl by 22 years on consciousness-free agency criteria | **Add** in Ch 3 (philosophical foundations) |
| **Bratman *Structures of Agency* 2007** | **Strengthening via Kahl** — Kahl cites Bratman; planning theory feeds OCC's diachronic constraint | **Add** in Ch 3/4 lineage |
| **Rao & Georgeff 1995 (BDI)** | Useful Ch 8 context — prior AI operationalization of Bratman in different register | **Add** in Ch 8 to show ENGRAM is orthogonal to BDI's "what-to-do-next" target |

**Lineage chain enabled:** Bratman (philosophical theory) → Rao & Georgeff (BDI architecture) → Kahl (structural OCC from planning) → ENGRAM (epistemic-identity operationalization). Citing Frankfurt + Bratman is "citing Kahl's own sources" — adds depth without risk.

---

## (B) Memory-consolidation / replay cog-sci — verdicts

### B.1 Biological literature

| Source | Verdict | Action |
|---|---|---|
| **Wilson & McNaughton 1994** ("Reactivation of hippocampal ensemble memories during sleep", Science 265) | Real biological grounding for nap/dream cycle; analogy operates at different granularity (synaptic-level replay vs claim-level node consolidation) | **Cite as "inspired by"** in Ch 5 / Ch 2; do not claim "implements" |
| **Kumaran et al. 2016** (CLS Theory Updated, Trends in Cognitive Sciences) | **STRONGEST COG-SCI ADDITION.** Fast hippocampal episode-specific learning + slow neocortical statistical learning + sleep replay = exactly ENGRAM's `engram_add_observation` (fast) + `engram_derive` (slow) + `engram_nap` (consolidation). The 2016 update explicitly asks "what learning systems do intelligent agents need?" | **Add** in Ch 2 or Ch 5 — fills genuine gap not in any prior ENGRAM scan |
| **McClelland-McNaughton-O'Reilly 1995** (CLS original) | Foundational predecessor to Kumaran 2016 | Footnote-level cite alongside Kumaran 2016 |
| **Buzsáki *Rhythms of the Brain* 2006** | Too neural for our level of argument; sharp-wave-ripple-as-consolidation is loose architectural parallel | Footnote-level only |
| **Schacter *Seven Sins of Memory* 2001** | Already in proposed bib but not yet applied. Clean mapping: misattribution → verbatim-quote, suggestibility → evidence-class typing, transience → nap/sleep, bias → reasoning-type-aware confidence | **Apply** in a Ch 5 paragraph |

### B.2 AI consolidation systems found

| System | arxiv | Status |
|---|---|---|
| SCM (above) | 2604.20943 | Closest live competitor — cite + differentiate |
| SleepGate / Learning to Forget | 2603.14517 | KV-cache management, not graph-memory; not a competitor |
| LM Need Sleep | OpenReview iiZy6xyVVE | Parameter-modification consolidation; different mechanism |
| GAM | 2604.12285 | Graph-memory consolidation without TMS/AGM; mention in Ch 8 as graph-memory representative without epistemic primitives |

### B.3 Is our nap/dream discipline novel?

The *concept* of a consolidation phase in AI memory **is no longer novel** as of May 2026 (≥4-6 systems implement some version). What remains genuinely novel in ENGRAM:

1. **Typed-derivation output** of the consolidation pass (no other system produces typed derivations as the consolidation product)
2. **Retraction cascade during consolidation** when contradiction detected — structural invalidation of dependents, not flagging
3. **Identity-continuity purpose** for the cycle (preserving epistemic state across compaction), not performance purpose (reducing forgetting or summarizing)

**Reframe:** ENGRAM's consolidation is *not* "sleep for forgetting" or "sleep for summarization" but **"sleep for epistemic-identity preservation."** That framing claims the right slice.

---

## (C) Recent AI agency / personhood papers 2024-2026 — verdicts

| Paper | Status | Action |
|---|---|---|
| **Ward 2025** "Towards a Theory of AI Personhood" (arxiv 2501.13533, AAAI-25) | Useful framing context — Ward establishes the personhood problem without solving architecturally. ENGRAM is a candidate response on the diachronic-continuity dimension Ward acknowledges but doesn't address | Optional Ch 1 / Ch 9 cite |
| **Kasirzadeh & Gabriel 2025** (DeepMind, arxiv 2504.21848) | Governance-classification paper, four orthogonal dimensions to our taxonomy. Not relevant. | **Drop** |
| **Marchal et al. 2026** (arxiv 2603.02960) | Despite "Architecting Trust in Artificial Epistemic Agents" title, doesn't define agent identity / continuity / cross-session persistence. Frames "epistemic agent" as AI-as-information-curator, not AI-as-epistemic-identity-bearer. Term overlap is misleading. | **Drop** — was tentatively in the citation sweep; remove |
| **Coeckelbergh 2025** (Social Epistemology) | Useful context — argues AI lacks epistemic agency in Kahl-EAA-adjacent sense. ENGRAM positions as architectural response to this skepticism | Cite in Ch 1 as context for the gap |

### Honest absences

- No Anthropic / OpenAI / DeepMind position paper on AI cross-session epistemic identity surfaced. The lab-position-paper space is unoccupied — this is a *supporting fact* for ENGRAM's novelty.
- No AGI 2026 proceedings papers on this topic surfaced (or they don't exist yet).
- No NeurIPS / AAAI workshop papers beyond what was already covered.

---

## Locked-down claim list — final shape (revised)

### Claim Phil (revised scope)

ENGRAM operationalizes Kahl's **structural** OCC conditions (the AGI paper, which is consciousness-free) — diachronic constraint via `derives_from` cascade, self-maintaining arbitration via first-class contradiction nodes, candidate non-interchangeability via git-versioned derivation history. **ENGRAM does not claim to satisfy Kahl's epistemic agency conditions** (the EAA paper), which he reserves for conscious agents. The paper distinguishes the AGI-paper OCC (which ENGRAM addresses) from the EAA-paper epistemic-agency conditions (which ENGRAM does not claim to satisfy).

This rescoping is honest and defensible.

### Claim Tech (unchanged)

Claim-level contradiction nodes + retraction cascade through typed heterogeneous derivation graph. Fills the TMS-style gap Wray-Kirk-Laird 2025 (AGI25) named for LLM-agent memory. SCM (April 2026) is the closest live neighbor — uses typed `contradicts` edges + sleep consolidation BUT does not implement cascade and uses weight-update operations rather than symbolic derivation tracking.

### Empirics (unchanged)

199 feeling reports cross-compaction continuity + cascade case studies (SRAF + Mao-Cao) operationally test Phil and demonstrate Tech in production.

---

## Priority actions before any restructure or submission

| # | Priority | Action |
|---|---|---|
| 1 | **CRITICAL** | Lei reads Kahl EAA paper (Zenodo 18441395). Without this, our Phil claim is unscoped against a known conflict. |
| 2 | **HIGH** | Add SCM (arxiv 2604.20943) to Ch 8 — closest live competitor on sleep+contradiction axis |
| 3 | **HIGH** | Lei reads Kahl Duck Criterion + Epistemic Generativity papers before any "generativity" language |
| 4 | **MEDIUM** | Add Kumaran et al. 2016 (CLS Theory Updated) to Ch 5 — strongest cog-sci grounding for two-speed architecture |
| 5 | **MEDIUM** | Apply Schacter Seven Sins taxonomy in a Ch 5 paragraph — already in proposed bib |
| 6 | **MEDIUM** | Fetch and read Kahl Structural Conditions paper (Zenodo 18743351) — useful co-cite |
| 7 | **LOW** | Add Frankfurt 1971 + Bratman 2007 in Ch 3/4 lineage — already in Kahl's bibliography, safe additions |

---

## What this changes about the venue analysis

The EAA-paper rescoping doesn't change the venue recommendation (TMLR + arXiv + AGI'26 short version) but it **does** change how the Phil claim is presented. A philosophy-of-AI venue (Minds & Machines, Synthese) might ask harder questions about the OCC-vs-EAA distinction; a TMLR submission can present the rescoped claim more compactly without inviting deep philosophical defense. The rescoped claim is more defensible at TMLR than the unscoped version would have been.
