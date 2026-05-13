# Empirical Data — Scaffolds and Mechanisms Working in Practice

*Concrete instances where ENGRAM's substrate mechanisms have produced value that imagination at design time did not anticipate. Empirical record supporting `ax_0010` (Practice produces true knowledge; practice is the sole criterion for testing truth) and the broader epistemic-practice framing the paper makes.*

**Last updated:** 2026-05-13 (initial collection)
**Position in paper:** candidate material for Ch7 (limitations + future) or Ch8 (conclusions), and for methodology appendix demonstrating "the substrate validates itself by running."
**Related ENGRAM nodes:** `ax_0010` (axiom, filed 2026-05-13), `cs_0010` (cornerstone, 2026-05-13), `ax_0006` (friction-side specialization, 2026-04-15), `dv_0224` (original four-instance calibration record, 2026-04-15).

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
| Fairy multi-round | Real-bug-catching round-by-round | Partly (peace-of-mind) | Today's PR #12 (3 rounds) + PR #13 (2 rounds) |
| Lesson tripwires | Active in-flow firing, not retrospective | Partly | Today's cross-repo session |
| Dedup heuristic | Alarm-fatigue calibration | NO | ob_0474 friction-driven calibration |
| Supersede cascade | DAG-invariant respect | NO | ob_0475 friction-driven calibration |
| Quote verification | Encoding-robust comparison | NO | ob_0483 friction-driven calibration |
| DAG check | Operational-pragmatism for legacy | NO | ob_0485 friction-driven calibration |
| DAG_EXEMPT_RELATIONS | Schema-level partition | NO | dv_0495 friction-driven calibration |
| Supersede refactor | Tool-design decomposition | NO | dv_0501 friction-driven calibration |

**Across 9 instances spanning ~one month, the anticipation rate is zero or partial.** Imagination at design time did not name the load-bearing role that practice surfaces. This is the empirical base for `ax_0010` and the cross-cultural pragmatist claim.

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
