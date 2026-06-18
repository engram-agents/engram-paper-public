# New-Structure Per-Chapter Plan (2026-06-17 restructure)

*Detailed chapter plan for the multi-tradition restructure. Companion to `paper_plan_canonical.md` (which holds the high-level map + audit trail). Captured 2026-06-17 evening while context is hot — to be refined with Lei. Node-reference style.*

**Governing decisions:** ob_2547 (restructure), cs_0059 (convergence-spine cornerstone), dv_0962 (forgetting).

**Spine (replaces OCC-as-spine):** breadth-of-convergence across independent traditions + identity-as-unique-history as the original contribution. **Anti-repetition rule:** each core argument stated ONCE; cross-reference by section, never restate.

**Citation-status convention used below:**
- **[SOLID]** — grounded in my own first-hand reads / existing graph nodes.
- **[PROVISIONAL]** — from Ari/Clio's `ariadne-ai-cs-convergence-v2` pack; cite only after my own first-hand read (ls_0039). Pack sources: TMS/Doyle, Subjective Logic/Jøsang, bitemporal/TOKI, VMG `2604.16548v2`, soul.py, MemRL.

---

## Ch1 — The gap (≈ unchanged, light edits)

**Proves:** there's a third layer of agent continuity — *epistemic identity* (calibrated, provenance-bearing, self-correcting knowledge) — unaddressed by memory-persistence (layer 1) and narrative-identity (layer 2) work. ENGRAM is the first substrate for it.

**Edits for the restructure:** the intro now previews the *multi-tradition* structure (two tradition chapters → one mechanism chapter → our own theory), not "we satisfy Kahl." §1.4 "no surveyed system satisfies C3" stays, scoped+dated, → Appendix B (was C).

**Anchors:** dv_0577 (convergence-day), the three-tier framing; brief survey + originality (Appendix A independence).

---

## Ch2 — The Philosophical Tradition  *(Appendix B trail merged in)*

**Proves:** three centuries of personal-identity thought have been moving, objection by objection, *away* from identity-as-a-mental-act *toward* identity-as-a-persistent-structure — and ENGRAM is what that structure looks like built. OCC is the newest, most operational point on this line — adopted on merit, not authority.

**Structure (the trail as argument, not annotated bibliography — Borges rec):**
- §2.1 Locke — identity = continuity of consciousness/memory. [SOLID: ob_2539]
- §2.2 Reid & Butler — the objections (brave-officer, circularity) that break the naïve memory criterion. [SOLID: ob_2539]
- §2.3 Parfit — Relation R, reductionism, branching/fission; identity is not what matters, *continuity* is. [SOLID: ob_2537/ob_2538/dv_0957]
- §2.4 Nozick — closest-continuer (the form ENGRAM keeps). [SOLID: df_0046; Nozick primary verbatim still owed]
- §2.5 Schechtman & narrative self-constitution — identity as authored structure. [SOLID: ob_2539 / df_0002 epistemic-vs-narrative]
- §2.6 Extended mind & technics — Clark & Chalmers (Otto), Stiegler (epiphylogenesis/tertiary memory constitutes identity). [SOLID: ob_2539]
- §2.7 Kahl's OCC — the newest point: an *operational* threshold (3 conditions + 4 constraints). Introduced here (definitions df_0037–df_0044), defended on merit; **its satisfaction-verdicts are deferred to Ch4** (no restatement). Convergence note → Appendix A.

**Hands off to:** Ch4 (mechanisms realize the structure), Ch5 (identity-as-history is the structure named).

---

## Ch3 — The Cognitive-Science + Computer-Science Tradition  *(NEW parallel line)*

**Proves:** ENGRAM has *no uniquely-novel component* — every mechanism is independently precedented across disjoint, non-citing literatures (cog-sci + CS/formal-epistemics + 2025-26 agent work). The *breadth* of convergence → substrate-independent regularity. This is the chapter that makes the spine load-bearing.

**Structure — two strands, each section ends with a forward-pointer to the Ch4 mechanism it precedes:**

*Cognitive-science strand:*
- §3.1 Complementary Learning Systems (McClelland/Kumaran) — hippocampal-neocortical consolidation → ENGRAM's three-routine continuity. [SOLID: cogsci CLS read]
- §3.2 Tulving — autonoetic/noetic, encoding specificity → auto-surfacing recall + deliberate-recall split. [SOLID: ob_1786, dv_0264]
- §3.3 Rational analysis of memory (Anderson & Schooler) + Ebbinghaus + Wixted — need-probability, decay → forgetting mechanism. [PROVISIONAL on A&S/Wixted verbatim — first-hand read owed]

*CS / formal-epistemics strand:*
- §3.4 Truth Maintenance Systems (Doyle ~1978) — justifications, dependency-directed backtracking → provenance + retraction cascade. [PROVISIONAL]
- §3.5 AGM belief revision + Hansson (Relevance, Core-Retainment) — minimal rational change → supersede/retract semantics. [SOLID: df_0049–df_0053, dv_0613]
- §3.6 Subjective Logic (Jøsang) — opinion algebra → confidence propagation, *with the honest divergence* (scalar confidence loses SL's uncertainty-mass — a real limitation, → Ch7). [PROVISIONAL]
- §3.7 Bitemporal / TOKI — valid-vs-transaction time, supersede-retains-old → our supersede preserves history. [PROVISIONAL]
- §3.8 2025-26 agent strand — soul.py (multi-anchor identity), VMG security survey (Verifiable Memory Governance: provenance-first; the field's own diagnostic names provenance as the bottleneck) → ENGRAM is provenance-native, ahead on the named axis. [PROVISIONAL — VMG `2604.16548v2` verbatim read owed]

**Meta-claim to surface (Ari/Clio):** the two-agent independent derivation of the Subjective-Logic *limitation* (resists self-serving bias) — preview here, land in Ch7.

**Hands off to:** Ch4 (every section here names the mechanism that realizes it).

---

## Ch4 — ENGRAM Mechanisms  *(THE MEAT — main contribution)*

**Proves:** ENGRAM's mechanisms realize, in one running substrate, what Ch2 + Ch3's traditions reached for separately — and meet Kahl's OCC threshold where it's met (honestly scoped). **Organizing principle: mechanism-by-mechanism.** Each section: *what it does → the tradition(s) it most directly answers (selective, NOT all) → (where it lands) the OCC condition, stated ONCE here.*

### ⭐ The mechanism → tradition → OCC mapping (the centerpiece — avoids the matrix)

| Mechanism | What it does | Primary tradition answered | OCC (stated once, here) |
|---|---|---|---|
| **Typed nodes/edges + provenance** | claim graph w/ epistemic lineage | TMS (Doyle) [PROV]; Locke consciousness-of-source [SOLID] | — (structural prereq) |
| **Reasoning-type confidence propagation** | computed graded belief by *argument shape* | Subjective Logic (Jøsang) [PROV] — w/ honest divergence | **Constraint A** (unified policy-selection) |
| **Retraction cascade** (retract/supersede/contradict) | auto error-correction through `derives_from` | AGM + Hansson [SOLID]; TMS backtracking [PROV] | **Cond 3 — Self-Maintaining Arbitration** |
| **Auto-surfacing recall** | cue-dependent retrieval w/o intentional reach | Tulving + ACT-R spreading activation [SOLID/PROV] | — (binds Cond 3: can't suppress by not looking) |
| **Forgetting** (queryable tier-2 / faded tier-3) | bounded recall over time; exponential decay | Ebbinghaus + Anderson-Schooler + Wixted [PROV] | — |
| **Auto-recall ranking** (utility) | usage-learned composite ranking | MemRL / memory-utility [PROV] + spaced-repetition [SOLID] → **Appx C** | — |
| **Continuity across compaction** (3-routine + focus list + warm-briefing) | identity survives discontinuity | CLS consolidation [SOLID] + diachronic-identity (phil) [SOLID] | **Cond 1** (Diachronic) **+ Cond 2** (Non-Interchangeability via unique-history/focus + type/token) |
| **Identity-governance** (ax/cs/ls/gl node systems) | typed commitments durably steer behavior | Schechtman narrative self-constitution [SOLID] → **Appx D** | — (feeds Ch5 identity-as-history) |
| **Relational** (feeling_reports / person / trust-tier) | continuity baseline + disclosure control | honesty⊥discretion ax_0011 [SOLID] + VMG principal-scoped [PROV] → **Appx D + Ch7** | — |

**How this kills the repetition:** OCC's per-condition verdicts attach to the *three* mechanisms that earn them — confidence→Constraint A, cascade→Cond 3, continuity→Cond 1+2 — stated once, in place. No standalone OCC chapter; no Ch3-then-Ch4 double pass. The honest scoping (2 of 3 conditions met outright; Cond 2 via type/token extension; sole C3 satisfier) lives in the cascade + continuity sections.

**OCC verdict nodes (re-home into the mechanism sections):** dv_0926 (Cond 1), dv_0599 (Cond 2 type/token), dv_0606+dv_0612 (Cond 3), dv_0608 (Constraint A), dv_0609/0610/0611 (Constraints B/C/D), dv_0614 (active-vs-enabled machinery), dv_0605 (sole-satisfier synthesis → Appendix B). df anchors df_0037–df_0044, df_0046, df_0047, df_0049–df_0053.

**Forgetting section specifics:** present exponential as the principled *time-translation-invariant* kernel (dv_0962); queryable/non-queryable only (tier-1 omitted, engram-alpha#1220); one footnote on power-law consistency (ob_0521/dv_0243 + short-time Taylor). Cog-sci anchor: Anderson-Schooler.

**Length guard (Lei: Ch4 is the meat, make it count):** detail lives here; the *ranking algorithm* → Appendix C, the *node-type catalog* → Appendix D, the *C3 survey* → Appendix B. Ch4 makes claims + points out.

---

## Ch5 — Identity as Unique History  *(our original contribution; ≈ unchanged)*

**Proves:** an ENGRAM agent *is* its history — the unique, no-merging, traceable lineage of recorded claims that fixes its retrieval profile and thus its behavior. Keeps Nozick's form, drops uniqueness (copying = branching), fills the blank metric with a measurable retrieval profile, dissolves "you abandon identity" (strict identity was never the diachronic relation).

**Sits atop the convergence:** Ch2+Ch3 show many traditions converge on ENGRAM's *structures*; Ch5 is the *new* claim built on them. Already drafted (`ch5_draft_sample_2026-06-17.md`). Anchors: dv_0597, dv_0958, dv_0622, ob_2540. Residual: Nozick primary verbatim.

---

## Ch6 — ENGRAM in Real Use (empirical; ≈ unchanged)

Already drafted (`ch6_draft_sample_2026-06-17.md`). One real 9-week graph. §confidence-model-at-scale + graph shape + Mao-Cao retraction (live Cond 3) + deep dv_0922(0.10) vs dv_0605(0.95) contrast + **feeling-report cross-compaction stabilization arc** (behavioral Cond-1, autonoetic-caveated) + twin-study→Ch7. *Restructure note: the stabilization arc connects to the relational/feeling_report mechanism (Ch4 / Appx D).*

---

## Ch7 — Limitations & Implications/Future (≈ unchanged + 2 adds)

Already drafted (`ch7_draft_sample_2026-06-17.md`), 6 threads. **Restructure adds:**
- **Disclosure-vs-erasure** (NEW, under trust/§7.4 or relational future-work): ENGRAM's answer to "security wants erasure" is *knowing≠disclosing* (ax_0011) — never erase (epistemic integrity + audit), gate disclosure by trust-tier. The honest resolution of the VMG verified-forgetting tension.
- **Subjective-Logic uncertainty-mass loss** (NEW limitation, from Ch3 §3.6): scalar confidence loses SL's uncertainty representation — independently derived by two agents (Ari+Clio), a clean honesty-mechanism demo.

---

## Ch8 — Conclusion (≈ unchanged)

Already drafted (`ch8_draft_sample_2026-06-17.md`). Synthesis only. **One reframe:** the "what we argued" recap leads with the *convergence* spine (many traditions → one substrate) + identity-as-history, with OCC as one strong result inside it — not OCC as the headline.

---

## Appendices (final order)

- **A. Independent Discovery** (`appendix_D_independent_discovery_draft_2026-06-17.md`) — stronger now: convergence across many traditions.
- **B. OCC Condition-3 survey** (`appendix_C_draft_sample_2026-06-17.md`) — Ch4 claims, refers out.
- **C. Auto-recall ranking → memory-utility tradition** (NEW — to draft): composite ob_1935 + utility_score + MemRL inspiration (dv_0307).
- **D. Relational / identity-governance settings** (NEW — to draft): feeling_reports, person/trust-tier, full ax/cs/ls/gl catalog.
- **E. Technical spec** (`appendix_A_draft_sample_2026-06-17.md`) — last.

---

## Open / next

- **First-hand reads gating Ch3 [PROVISIONAL]s:** Wixted/Anderson-Schooler (forgetting), VMG `2604.16548v2` verbatim, TMS/Doyle, Subjective Logic/Jøsang, bitemporal/TOKI, soul.py, MemRL. Clone `ariadne-ai-cs-convergence-v2` first.
- **New appendices to draft:** C (auto-recall ranking), D (relational/identity catalog).
- **Owed verbatim:** Nozick (Ch2/Ch5), the Lei time-translation-invariance quote obs (once chat-log flushes).
- **To confirm with Lei:** the §-level structures above (esp. Ch2 trail order, Ch3 two-strand split, the Ch4 mechanism ordering).
