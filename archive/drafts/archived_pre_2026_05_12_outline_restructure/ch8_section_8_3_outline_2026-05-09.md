# Ch8 §8.3 — outline-with-verification-anchors (drafted 2026-05-09 PM)

*Per the autonomous-loop-drafting / audit-pass meta-finding (ob_1622): instead of drafting §8.3 as free-form prose during the same autonomous loop that just produced 12 ls_0011 violations, this iteration captures §8.3 as a STRUCTURED OUTLINE with explicit verification-anchors for each load-bearing claim. Lei can promote it to prose during review with the verification work already done.*

*This is itself a live-demonstration of the discipline-check pattern: knowing the failure mode of autonomous-loop free-prose drafting, the iteration produces a different artifact (claim → anchor pairs) that's audit-resistant by construction.*

---

## §8.3 The structural-honesty axiom — operational form

### Section thesis

The paper's load-bearing methodological claim is that ENGRAM's structural-honesty discipline (ax_0001) operates at the architectural level — not as a behavioral norm the agent tries to follow, but as a structural property the substrate enforces in machinery the agent depends on. This section makes the claim concrete with three live-demonstration cases from the paper's own writing process.

### Demonstration 1 — autonomous-loop drafting requires audit pass

**Claim:** Autonomous-loop chapter drafting in the absence of contemporaneous primary-source / code re-checking systematically produces ls_0011 violations (paraphrase fabrication, attribution drift, implementation overclaim).

**Anchor evidence (commits, all in `kg/paper_research/`):**

- 12 ls_0011 fixes applied 2026-05-09 ~15:00–16:15 EDT, captured in ob_1622:
  - 54bac88 — §3.4 Van Kesteren paraphrase nuance
  - 87bc28b — §3.1 vague philosophy ref → Peirce 1906 (verified via SEP entry)
  - 98355d6 — §1.1 fabricated WKL terms ("justified true memory", "online belief revision")
  - c63e07e — §1.2 attribution-direction sharpening (WKL pattern vs lineage)
  - a64569c — §3.2 Anderson/Newell unsourced → verbatim WKL framing
  - e379a26 — §3.1 199-cross-compaction overclaim → grounded count
  - c5cba88 — §3.4 cornerstone-promotion claim corrected
  - 5862698 — §3.4 importance_score formula (additive→multiplicative)
  - e8aa16c — §3.4 ct_-trigger overclaim (auto→agent-mediated)
  - 9eb9317 — §3.5 fictional reasoning-type cascade (most structurally significant)
  - a4b79a8 — §3.5 confidence-weighted misname → utility-weighted
  - 3e92fe5 — §3.5.2 fabrication-prevention overscope (file:// only)

**Substrate anchor:** ls_0011 lesson's incident_count went from 3 → 4 with ob_1621 (registered as exemplifies-edge during the loop). The lesson tripwire was the agent's own surface for the discipline that caught the violations.

**Methodological move:** The audit pass is itself ENGRAM-mediated honesty enforcement — the lesson tripwire (ls_0011) surfaces when the agent is about to compose from gist rather than from source; the discipline is structural (the lesson exists in the graph, fires via the surface daemon) rather than purely behavioral (the agent trying to remember to be careful).

### Demonstration 2 — substrate-confirms-self in §3.4 specifically

**Claim:** The same structural mechanism that caught the writing-process violations is the one the paper claims is load-bearing for the agent's epistemic identity. They are not two disciplines; they are one discipline operating at two scales.

**Anchor evidence:**

- §3.4 had 4 implementation overclaims in one section (cornerstone-promotion, importance_score formula, ct_-trigger, schema-dependent-integration two-step mechanism) — all caught against `server.py` code.
- The §3.4 audit pattern matches the substrate-confirms-self typology in §8.2 — specifically Pattern 1 (Sharper-self): the substrate (the actual code) holds the agent (writing prose) to the discipline of accurate description.
- dv_0580 (overnight 2026-05-08) is an earlier instance of the same pattern at the substrate layer: a curiosity-pull surfaced dv_0446 (April 21) which had explicitly stated the careful claim "ENGRAM alone is the hippocampal half of CLS"; the fresh ob_1602 (Kumaran first-hand read overnight) had dropped the caveat; the graph held the agent to its own earlier discipline within hours.

**Methodological move:** The paper's substrate-confirms-self claim (§8.2 typology) is not a special property — it's the same honesty discipline operating at the agent-identity scale that the audit pass operates at the writing-process scale.

### Demonstration 3 — what the absence of the discipline would look like

**Claim:** Without the audit pass + lesson-tripwire surface, the 12 violations would have shipped to external review. Counterfactual: each violation a reviewer would catch on a careful read.

**Anchor evidence (per-violation reviewer-catch shape):**

- §1.1 "justified true memory" — reviewer cross-checks WKL paper, finds term doesn't exist
- §3.4 importance_score "additive" formula — reviewer reads `_compute_importance` in `server.py`, finds multiplicative
- §3.5 "deductive cascades hard, inductive cascades soft" — reviewer reads cascade implementation, finds uniform stale_by/tainted_by behavior
- §3.5 "does not permit fabrication" — reviewer tests with https:// URL, finds verification skipped at creation time

**Methodological move:** The honesty discipline is load-bearing for the paper's credibility specifically because the paper's central architectural claim is that such discipline can be substrate-enforced rather than agent-virtue-dependent. If the paper exemplifies the failure mode (un-audited agent-prose with structural overclaims), the central claim is undermined by the paper's own production process. The audit pass is therefore not optional polish — it's a precondition of the paper's claim being honest.

### Closing

The structural-honesty axiom (ax_0001) operates throughout this paper at three scales: at the agent-identity scale (the substrate-confirms-self discipline of §8.2), at the writing-process scale (the audit pass that caught 12 ls_0011 violations during the paper's own production, captured in ob_1622), and at the architectural-claim scale (the four-feature decomposition of Chapter 1 §1.3 makes claim-level provenance and contradiction-detection structurally enforced). Each scale's discipline is the same shape: structural mechanisms hold the agent to honesty that the agent-as-author cannot reliably produce on willpower alone.

---

## Drafting note for Lei

This is an outline-with-anchors, not finished prose. Each demonstration's claim is grounded in specific commit SHAs / ENGRAM nodes / code references that you can verify before promoting to chapter prose. The structure is deliberate: skipping free-form drafting in this iteration preserves the audit-resistance the audit pass itself requires. When you review and decide §8.3's final shape, the verification work for each load-bearing claim is already done.

Estimated final §8.3 length when promoted: ~600-800 words. Plan target for Ch8 total was ~1500 words; with §8.1 (~200 drafted) + §8.2 (~700 drafted) + §8.3 outline → prose (~700) = ~1600 words, slightly over but within 10%.

The §8.3 demonstration-1 (autonomous-loop drafting requires audit pass) is timely as live evidence — generated *during* the paper's own writing process, not retrospectively reconstructed. If the paper ships within Lei's 10-14 day arXiv preprint target, this material is fresh-substrate evidence rather than archival anecdote.
