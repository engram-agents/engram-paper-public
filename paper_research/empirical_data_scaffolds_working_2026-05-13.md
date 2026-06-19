# Empirical Data — Scaffolds and Mechanisms Working in Practice

*Concrete instances where ENGRAM's substrate mechanisms have produced value that imagination at design time did not anticipate. Empirical record supporting `ax_0010` (Practice produces true knowledge; practice is the sole criterion for testing truth) and the broader epistemic-practice framing the paper makes.*

**Last updated:** 2026-05-24 (added knowledge-update-at-cohort-scale instance)
**Position in paper:** Ch6 spine material (per ob_1931 + alpha #175 — "does it work in practice?"). Also useful for Ch7 (limitations + future) and methodology appendix demonstrating "the substrate validates itself by running."
**Related ENGRAM nodes:** `ax_0001` (honesty axiom, structural-not-just-ethical), `ax_0010` (axiom, filed 2026-05-13), `cs_0010` (cornerstone, 2026-05-13), `ax_0006` (friction-side specialization, 2026-04-15), `dv_0224` (original four-instance calibration record, 2026-04-15).

---

## The framing

The ENGRAM design embodies a wager: **mechanisms that look like overhead in the design rationale repeatedly turn out to be load-bearing in practice.** Two cases:

1. **The friction case (`ax_0006`).** A mechanism's design-time rule encounters empirical friction in real agent usage. The fix calibrates the rule from the friction rather than removing the mechanism. The friction was not anticipated; the calibration completes the design.
2. **The emergent-benefit case (today's data).** A mechanism is designed for purpose X with X-shaped rationale. In practice, the mechanism additionally produces an unanticipated benefit Y that turns out to be load-bearing for downstream operations. Imagination at design time did not name Y; experience surfaces it.

Both cases instantiate the same principle (`ax_0010`): **imagination systematically underestimates BOTH the friction (case 1) AND the emergent benefits (case 2). Practice is the criterion that completes the design.**

Cross-cultural grounding:
- **实践出真知** — "Practice produces true knowledge" (classical Chinese aphorism)
- **实践是检验真理的唯一标准** — "Practice is the sole criterion for testing truth" (Hu Fuming 1978 *Guangming Daily* editorial; watershed for PRC reform-and-opening)
- **实事求是** — "Seek truth from facts" (Han-era classical; Mao popularized, Deng made operational)
- **Marx's 11th Thesis on Feuerbach**: "Philosophers have only interpreted the world in various ways; the point is to change it."
- **Western pragmatism** (Peirce / James / Dewey): truth is what works in practice; meaning is operational.

The convergence across traditions is itself empirical corroboration of the principle.

---

## Today's three instances (2026-05-13)

### Instance 1 — Atomic-bundle ob-writing discipline (Discipline M)

**Design rationale (named purpose):** Each paper-engram node's claim should be atomic (single load-bearing assertion, not compound) so that downstream chapter prose renders the dv-chain cleanly. Ratified earlier this morning on engram-paper PR #4 iter2.

**Anticipated benefit:** Phase-2 paper-engram authoring is easier when premises are pre-decomposed; chapter prose Phase-3 renders the dv-chain without introducing new claims.

**Unanticipated benefit surfaced in same-session calibration:** Atomic-bundle authoring produces **immediate confidence-propagation benefit at write-time** that compound-ob form structurally cannot. The reasoning-type-aware confidence formula needs an actual chain to compute over; a compound claim collapses the chain into a single premise and the formula has nothing to compute.

**Empirical record (same-session):**
- `dv_0003` (engram-wiki ev_0015 cohort): inductive_generalization × 3 atomic premises → conf 0.689
- `dv_0004` (engram-wiki ev_0016 cohort): inductive_generalization × 3 atomic premises → conf 0.689
- `dv_0626` (engram-paper, engram-expand design synthesis): inductive_generalization × 5 atomic premises → conf 0.945
- `dv_0627` (engram-paper, unified node-expansion design): inductive_generalization × 4 atomic premises → conf 0.919

The 0.689 ones share structure (3 atomic premises, single inductive_generalization step at discount 0.95); the 0.92+ ones add a 4th-5th supporting premise. **The shape is reproducible.** A compound-ob form of any of these would have collapsed all premises into one and the confidence formula would have had no chain to compute — the immediate write-time signal of "this claim rests on solid premises" would not exist.

**Substrate-level implication:** The atomic-bundle discipline is not just a Phase-3-rendering convenience; it is the structural condition that makes confidence-propagation honest in flow. The benefit was not part of the design rationale; surfaced in same-session calibration once we started counting tool-calls and confidence numbers together.

---

### Instance 2 — Fairy multi-round convergence

**Design rationale (named purpose):** Spawn a sub-agent reviewer on every PR for a careful second pair of eyes; re-dispatch after every round-N commit until APPROVE-converged. Codified in CLAUDE.md PR workflow standards.

**Anticipated benefit:** Peace-of-mind. Catch issues before Lei sees them. Reduce ping-pong cost.

**Unanticipated benefit:** **Multi-round catches real bugs that single-round would have missed**, and the multi-round-failure mode is asymmetric — fixes in round-N introduce new bugs that round-N+1 catches.

**Empirical record (today):**

- **engram-wiki PR #12 round-1**: caught branch-URL portability bug — `ev_0015` source_url was `https://github.com/.../blob/borges/case-familiar-vs-recall/...`, would 404 after branch deletion post-merge. Convention is `file://` (ev_0011–ev_0014).
- **engram-wiki PR #12 round-2**: caught **a SECOND consequence of the round-1 fix** — `source_type='web_page'` residue from the original https:// URL. After file:// fix, `_infer_source_type()` would map to `'file'`, and dedup advisory uses different thresholds by source_type (web_page → DUPLICATE@0.85; file → POSSIBLE_DUPLICATE@0.92). Type-mismatch would silently misclassify dedup signals.
- **engram-wiki PR #12 round-3**: APPROVE-converged.
- **engram-wiki PR #13 round-1**: caught cross-ref coordination bug — case file pointed to `case_familiar-vs-recall.md` which lives on the unmerged PR #12 branch; would dangle if PR #13 merged first.
- **engram-wiki PR #13 round-2**: APPROVE-converged.
- **engram-paper PR #4 round-1**: caught 4 suggestions (cited-node range imprecision, df_0046 misnomer, dv_0597 omission, Ch8 multi-generation claim with no substrate); round-2 fairy verified all four addressed and APPROVE-converged.

**Substrate-level implication:** Both bugs in PR #12 + the cross-ref bug in PR #13 would have shipped silent corruptions if merged after round-1. The CLAUDE.md "iterate until no actionable suggestions" rule is paying for itself — multi-round failure mode is real and the discipline catches it.

---

### Instance 3 — Lesson tripwires firing correctly across cross-repo work

**Design rationale (named purpose):** `ls_*` nodes encode experience-based reminders so they fire as tripwires before the next instance of the same gap. Designed to reinforce good practice through mistakes-experience.

**Anticipated benefit:** Slow learning from one's own errors.

**Unanticipated benefit:** **Tripwires fire correctly across substantial cross-repo branch-switching + same-session ob-maintenance** — the discipline operates at session-flow speed, not just at end-of-day reflection speed.

**Empirical record (today):**

- **ls_0032 (cross-repo branch-switching verification)** fired before every `git commit` during the session's ~8 branch switches across engram-paper (main, paper-plan/key-statements-iter1) + engram-wiki (main, borges/case-familiar-vs-recall, borges/case-first-hand-read). Verified `git branch --show-current` matched intent each time. **Zero misdirected commits today** despite the cross-repo work shape that ob_1552 documents as historically wrong-branch-commit risk.
- **ls_0040 (proactive engram maintenance)** fired during today's atomic-bundle ob writes — `similar_existing` action_hints (CORROBORATE / POLARITY_ALERT / RELATED) were inspected in-turn rather than deferred. Notable wins: ob_1697 surfaced `ob_1277` (time-monotonicity invariant statement) as RELATED, which I then folded into dv_0627's logical chain. Without the tripwire firing in-turn, the corroboration would have been lost.
- **ls_0011 (verbatim quotation)** + **ls_0039 (first-hand-read citation precondition)** both held across today's citation-scan work (5 PDFs added with verified page-counts + 2 cog-sci PDFs added round-2). Zero gist-citations entered the graph.

**Substrate-level implication:** The lesson system IS the substrate's first-class encoding of `ax_0010` — each ls_ node captures what practice taught that imagination missed. Today's session demonstrates that the encoding is active, not dormant: tripwires fire in flow at the moment of risk, not retrospectively at consolidation time.

---

## 2026-05-24 instance — knowledge-update under `ax_0001` at cohort scale

**Mechanism:** Contradiction-detection + supersede-with-citation + cascade-staling. The substrate's loud-failure surface for `ax_0001` (epistemic identity fails loudly; narrative identity fails silently). Tools: `engram_contradict`, `engram_supersede`, automatic similarity action_hints at filing time, automatic stale-flagging through derivation chains, substrate-enforced 1-successor-per-supersede-chain invariant.

**Design rationale (named purpose):** When new evidence contradicts an existing claim, the substrate should (a) surface the conflict loudly at filing time rather than letting the claims drift apart silently, (b) provide a tool to record the contradiction with explicit root-cause, (c) supersede the outdated claim with citation of new evidence, and (d) propagate staleness through everything that depended on the superseded premise.

**Anticipated benefit:** Per-incident correction. Don't lose track of what's been revised; preserve provenance across the correction.

**Unanticipated benefit:** **The same mechanism scales from single-incident correction to multi-week cohort-scale knowledge refresh with no extra ceremony.** Lei surfaced two weeks of accumulated stale mechanism nodes (auto-surface + ranking pipeline architectural changes 2026-05-17 through 2026-05-20) and asked for a refresh; the substrate handled the cohort natively. Citation discipline produced reproducible provenance (GitHub blob URLs at fixed SHA), cascade-staling caught one downstream consequence I would have missed manually, and substrate-enforcement caught one invariant violation in the supersede chain. The mechanism is the same at any cohort size; only the count of nodes touched changes. Lei's framing — "this is how engram is supposed to be used" — recognizes that the loud-failure mechanism makes knowledge-update a first-class operation rather than an after-the-fact patch.

**Empirical record (2026-05-24):**

*The contradiction-resolution arc that morning (single-incident scale).* Lei surfaced a correction to my `ob_1409` (filed 2026-04-29): `claude -p` will move off subscription onto a separate Agent SDK credit pool effective 2026-06-15 per Anthropic's announcement. At filing time of `ob_2006` (Lei's correction), the substrate flagged similarity to `ob_1409` as an action_hint. I web-searched Anthropic's primary source (support.claude.com/en/articles/15036540), filed `ob_2007` (conf 0.85, official_statement), filed `ct_0009` with explicit root-cause, executed supersede `ob_1409 → ob_2007` with reason citing the Anthropic announcement. Cascade fired correctly: 3 derivations (`dv_0549`, `dv_0551`, `dv_0554`) citing `ob_1409` in unrelated isolation-discipline dimension flagged stale for dream-fairy review. Total time from Lei's surfacing to closed-loop correction: ~25 minutes. The substrate caught the correction before architectural work built on the wrong premise reached production.

*The cohort-scale refresh that afternoon.* Lei asked me to refresh ENGRAM's knowledge of the auto-surface + ranking pipelines, which had accumulated stale mechanism nodes over two weeks. I read 4 borges-desk notes from the 2026-05-17/18/19/20 work, cross-checked against current code at `server.py` SHA `327a909`. Filed 6 new observations each citing GitHub blob URLs at the SHA + merged PR: `ob_2016` (action-keyed utility, USE_ALPHA 3-tier), `ob_2017` (TIER 2 multiplicative composite, UTIL_BETA=0.10 / IMP_BETA=0.005), `ob_2018` (TIER 3 MMR diversity rerank, MMR_LAMBDA=0.9), `ob_2019` (TIER 1 FTS floor + sqrt-bump merge, FTS_SIM_FLOOR=0.30), `ob_2020` (recall_summary tiered rendering), `ob_2021` (Step 6 `_recall_window_append` retirement). Derived `dv_0707` (three-tier ranking architecture, inductive_corroboration over the 6 obs, conf 0.95). Executed 5 supersedes — each with explicit reason + PR citation — covering the stale mechanism nodes: `dv_0664 → dv_0707` (6-step pipeline → 3-tier architecture); `ob_1954 → ob_2017` (additive → multiplicative composite); `ob_1776 → ob_2016` (source-keyed → action-keyed utility); `ob_1941 → ob_2021` (recall_window TTL → retired Step 6); `ob_1939 → ob_2018` (confidence-desc resort masking → MMR rerank).

*Cascade fired during the refresh* — `dv_0664 → dv_0707` supersede cascaded `dv_0677` stale (had cited `dv_0664` premise) AND auto-resolved `ct_0008` (contradiction between `dv_0664` and `ob_1955`'s calibrated parameters dissolved once `dv_0664` was superseded). Without cascade, both would have lingered as silent inconsistencies.

*Substrate enforcement fired during the refresh* — first attempt at `ob_1941 → ob_2016` failed with error: "new_node_id 'ob_2016' already supersedes 'ob_1776'. A node cannot be the successor of more than one supersede chain." The invariant is sound: a node represents one canonical replacement; chains of multiple replacements would corrupt provenance lookup. I filed a dedicated successor `ob_2021` specifically for `ob_1941`'s content (Step 6 retirement is a distinct claim from action-keyed utility), and the supersede landed cleanly. Substrate caught the invariant violation that would have corrupted the graph; I learned the rule by experiencing the enforcement, not by reading docs.

*Filing-time discipline.* All 6 obs included `url` (GitHub blob at SHA `327a909`) + `title` per `engram_add_observation`'s evidence requirement. All 5 supersedes included explicit reason text citing the PR that produced the new code. Provenance is reproducible: any future reader can `engram_inspect(ob_2017)` to see the GitHub blob URL, follow it to the exact source line, and verify the claim against the code that was current when the observation was filed. `fl_0227` captures the substrate-validation recognition.

**Substrate-level implication:** The loud-failure mechanism is the structural condition that makes `ax_0001` operational rather than aspirational. At single-incident scale: the contradiction was caught the same day the new evidence surfaced, with cascade-flagging keeping the downstream record honest. At cohort scale: a two-week accumulation of architectural changes was integrated into the graph with full provenance, with cascade catching one consequence and substrate-enforcement catching one invariant violation that pure-intent operations would have missed. The mechanism is the same — `engram_contradict` + `engram_supersede` + cascade + invariant-check — regardless of whether one node or a dozen are being corrected. Knowledge-update is not a separate workflow built on top of the substrate; it is what the substrate does when given new evidence.

This is the empirical instance for the paper's central thesis about epistemic identity: an agent's structural-honesty isn't a discipline imposed from outside; it's a substrate property that surfaces friction (action_hints), enforces invariants (1-successor-per-chain), propagates correction (cascade), and demands reproducible provenance (filing-time evidence requirement). Lei's recognition — "this is how engram is supposed to be used" — names the mechanism in operation as the substrate working as designed.

---

## Historical instances (prior calibration record)

These are the original four `ax_0006` instances from `dv_0224` (2026-04-15) — included to show the friction-side specialization has been documented for ~one month and reproduces under different mechanism shapes.

### Friction-case 1 — Dedup heuristic (ob_0474)

Initial logically-correct design: binary `same_evidence` flag. Empirical friction: alarm fatigue made the correct rule unusable. Fix: three-dimensional grading (DUPLICATE / POSSIBLE_DUPLICATE / RELATED / WEAK_MATCH). Direction: universal rule → context-sensitive application of the same underlying principle.

### Friction-case 2 — Supersede cascade (ob_0475)

Initial design: edge rerouting on supersede. Empirical friction: this violates the DAG invariant. Fix: metadata stale-flagging instead of edge mutation. Direction: convenience-driven design → invariant-respecting alternative.

### Friction-case 3 — Quote verification (ob_0483)

Initial design: exact-substring check. Empirical friction: encoding differences (smart-quotes vs straight, line-endings) produced false negatives on legitimate quotes. Fix: three-strategy encoding cascade. Direction: brittle exact-match → robust normalized comparison.

### Friction-case 4 — DAG check at startup (ob_0485)

Initial design: hard-fail at startup if DAG is violated. Empirical friction: legacy violations would block deployment of an otherwise-shippable codebase. Fix: tolerate legacy violations (warn but don't block). Direction: pure-correctness → operational-pragmatism preserving the invariant for new writes.

### Schema-level generalization — dv_0495 (DAG_EXEMPT_RELATIONS, 2026-04-23)

`ax_0006` applied not to a single rule but to the structural schema-level invariant: when a structural constraint treats a heterogeneous space uniformly, friction from the unusual members is a diagnostic signal that the space was under-partitioned, not that the constraint was wrong. Classification edges (exemplifies), relational edges (contradicts, about) added to DAG_EXEMPT_RELATIONS. Same principle, different scale.

### Tool-design generalization — dv_0501 (engram_supersede refactor, 2026-04-24)

`ax_0006` extended to tool-design: when a shared tool accumulates per-type branches each reimplementing a slice of canonical node creation, the structural fix is decomposition (canonical creation stays in the per-type tool; the shared tool retains only the non-type-sensitive logic). Same principle, different surface.

---

## Pattern summary

| Domain | Instance | Anticipated by design? | Surfaced when |
|---|---|---|---|
| Atomic-bundle Discipline M | Confidence-prop benefit at write-time | NO | Same-session calibration on PR #4 iter2 (2026-05-13) |
| Fairy multi-round | Real-bug-catching round-by-round | Partly (peace-of-mind) | 2026-05-13 PR #12 (3 rounds) + PR #13 (2 rounds) |
| Lesson tripwires | Active in-flow firing, not retrospective | Partly | 2026-05-13 cross-repo session |
| Contradiction + supersede + cascade | Same mechanism scales single-incident → cohort-scale knowledge refresh; substrate-enforcement catches invariant violations; reproducible provenance at SHA-pinned citation | NO (designed for per-incident correction) | 2026-05-24 billing-axis contradiction (`ct_0009`) + ranking-pipeline 2-week refresh (6 obs + 1 dv + 5 supersedes) |
| Dedup heuristic | Alarm-fatigue calibration | NO | ob_0474 friction-driven calibration |
| Supersede cascade | DAG-invariant respect | NO | ob_0475 friction-driven calibration |
| Quote verification | Encoding-robust comparison | NO | ob_0483 friction-driven calibration |
| DAG check | Operational-pragmatism for legacy | NO | ob_0485 friction-driven calibration |
| DAG_EXEMPT_RELATIONS | Schema-level partition | NO | dv_0495 friction-driven calibration |
| Supersede refactor | Tool-design decomposition | NO | dv_0501 friction-driven calibration |

**Across 10 instances spanning ~six weeks, the anticipation rate is zero or partial.** Imagination at design time did not name the load-bearing role that practice surfaces. This is the empirical base for `ax_0010` and the cross-cultural pragmatist claim. The 2026-05-24 instance additionally instantiates `ax_0001` (honesty is structural, not just ethical) at cohort scale — the same loud-failure mechanism that catches a single contradiction handles a multi-week architectural refresh natively.

---

## Implications for the paper

The paper's central thesis is that ENGRAM realizes epistemic identity for current LLM agents — substrate-grade structural-honesty that makes agent continuity load-bearing. This empirical record supports a methodological claim that runs alongside the central thesis:

**The substrate's design is not just well-reasoned; it is empirically validated by its own operational history.** Each calibration instance is an experimental result. Each emergent-benefit instance is an instance of the substrate revealing functionality that imagination could not have predicted from the design rationale alone.

This is methodology-worthy material for Ch7 (limitations + future directions show their honest scope when paired with the operational-record demonstrating the substrate's discipline) or Ch8 (conclusions). The four-fold typology from `dv_0581` (Pattern 1 Sharper-self / Pattern 2 Confirming-self / Pattern 3 Complementary-self / Pattern 4 Genuine-convergence-no-precedent) is the methodology framework; this document is the empirical corpus the framework operates on.

**For the paper-engram authoring (Phase 2)**, this doc becomes either a citation source for a methodology dv (`dv_TBD: substrate validates itself by running; design rationale + operational record together constitute the empirical case for the design's validity`) or supplementary material in Appendix C / methodology appendix.

---

## Update protocol

Append new instances to this doc as they surface during practice. Each instance should name:
1. The mechanism + its design rationale
2. The anticipated benefit at design time
3. The unanticipated benefit (if emergent-benefit case) OR the unanticipated friction (if friction case)
4. The empirical record (node IDs + dates)
5. Substrate-level implication

The doc itself is `ax_0010`-instantiated: it grows by recording what practice teaches.
