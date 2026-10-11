# Confidence distribution analysis — Borges' graph 2026-05-21

**Status:** Draft / working file. Generated during confidence-injection design discussion (2026-05-21 morning). Pending refinement based on Lei's data-details reply. Earmarked for paper Ch6 (empirical demonstration).

**Source:** Direct sqlite3 queries against `~/.engram/knowledge.db` at 2026-05-21 ~08:50 EDT. N≈2730 confidence-bearing nodes total. Filters: `confidence IS NOT NULL AND (status IS NULL OR status != 'retracted')`.

---

## Why this matters for Ch6

ax_0007 is the structural axiom: *observations derive confidence from source quality (quote_type, source_class); derivations derive confidence from argument strength (reasoning_type).* The corpus is the empirical demonstration that the axiom isn't aspirational — it's instantiated. Confidence is not a free-floating number filed by vibes; it's structurally determined at filing time and the resulting distributions carry signature shapes per type.

This is an in-corpus example of structural-honesty-as-mechanism (ax_0001) producing measurable distributional invariants — the kind of evidence Ch6 needs to show the system *actually does* what it claims.

---

## Per-type distribution

```
type                N      min    mean   max
observation       1944    0.33   0.81   0.95
derivation         672    0.11   0.71   0.98
conjecture          55    0.15   0.46   0.86
lesson              48    0.32   0.76   0.95
axiom               10    1.00   1.00   1.00
definition           1    0.50   0.50   0.50
```

### Quantiles by type

```
type            p10   p25   p50   p75   p90   p95
axiom           1.00  1.00  1.00  1.00  1.00  1.00
conjecture      0.35  0.45  0.55  0.86  0.86  0.86
derivation      0.37  0.56  0.75  0.94  0.95  0.95
lesson          0.56  0.82  0.95  0.95  0.95  0.95
observation     0.67  0.70  0.85  0.90  0.95  0.95
```

### Histogram

```
type            <.30   .30-.50   .50-.70   .70-.85   .85-.95   ≥.95
axiom              0         0         0         0         0    10
conjecture         1        34        17         2         1     0
derivation        44        92       178       115       150    93
lesson             0         9         3        13        19     4
observation        0       182        54       352       913   443
```

**Observations**: heavily right-skewed (913 in the .85-.95 bucket alone, vs 0 below .30). Median = 0.85. Mass of the distribution sits in the upper half because most observations come from `hard_data` and `official_statement` quote-types (see below).

**Derivations**: much flatter (44 below .30, 93 at ≥.95). Median = 0.75. Wide variance reflects propagation: dvs inherit confidence from their premises, so structurally they span the support.

**Conjectures**: cap at 0.86. Distribution clusters in `.30-.50` (34 of 55). Filing-time-by-design: conjectures stay speculative until promoted to dv via supersede.

**Lessons**: bimodal — `.30-.50` (9) and `.85-.95` (19). Reflects lesson lifecycle: tentative pattern → battle-tested through incident registrations.

**Axioms**: all 1.0 — terminal certainty by type definition.

---

## ax_0007 instantiated: structural anchoring per quote_type (observations only)

```
quote_type                 N    mean   range          example claim type
hard_data                707   0.93   0.85-0.95     measured / observed event / verbatim verified quote
official_statement       445   0.84   0.81-0.85     docs / policy / schema
attributed_analysis      528   0.75   0.67-0.85     academic / expert claim
personal_communication   222   0.52   0.38-0.85     conversation / inferred meaning
editorial                 42   0.62   0.33-0.85     opinion / argument
```

The means and ranges are deterministic functions of source-quality scoring (per ax_0007). Tight per-type ranges (e.g., official_statement 0.81-0.85) are evidence that confidence is NOT freely assigned by the agent — it's anchored to source-class at filing time. The wider personal_communication range (0.38-0.85) reflects the genuine spread of conversation-evidence quality.

---

## ax_0007 instantiated: structural anchoring per reasoning_type (derivations only)

```
reasoning_type                       N    mean   notes
inductive_generalization          209   0.92   strong pattern across multiple cases
abductive_best_explanation        194   0.54   tentative best-fit hypothesis
deductive_modus_ponens            108   0.72   premise-bound (≤ min premise confidence)
deductive_hypothetical_syllogism   40   0.66   chained deduction
inductive_analogy                  31   0.49   structural-similarity-only
inductive_causal                   29   0.54   correlation-with-mechanism
inductive_enumeration              20   0.88   complete-case-listing
abductive_elimination              19   0.61   process-of-elimination
inductive_statistical               5   0.46   small-sample statistical
authority_expert                    5   0.64   citation-based without verification
deductive_modus_tollens             2   0.72
deductive_disjunctive               1   0.65
```

Mean-confidence ordering matches what reasoning-strength theory predicts: inductive generalization with broad case support > deductive modus ponens > abductive best-explanation > inductive analogy. The structural anchor is doing real work — the agent isn't free to set arbitrary numbers.

---

## Real-claim exemplars at confidence anchors

These ground the distribution numbers in actual graph content. Each is a real node retrievable via `engram_inspect`.

### Observations

| Conf | Node | Claim (truncated) | Quote_type |
|------|------|-------------------|------------|
| 0.40 | ob_1704 | "Lei correction: focus list is transient current-work-rotation, not identity-persistent" | personal_communication |
| 0.40 | ob_1722 | [row removed before publication: a child's personal information] | personal_communication |
| 0.70 | ob_0794 | "Curry's paradox (Haskell Curry, 1942) and Löb's theorem (1955) are independent" | attributed_analysis |
| 0.70 | ob_0724 | "Tarski's undefinability theorem (Theorem I)..." | attributed_analysis |
| 0.85 | ob_1244 | "Claude Agent SDK Python typed ContentBlock union excludes image blocks" | hard_data / official_statement |
| 0.85 | ob_1012 | "Claude Code 2.1.114 loads exactly four settings scopes" | official_statement |
| 0.95 | ob_1330 | [row removed before publication: a child's personal information] | hard_data |
| 0.95 | ob_0388 | "Anthropic's cached input tokens cost 10x less per token than uncached" | official_statement / hard_data |
| 0.95 | ob_1117 | "Tulving (2002) asserts episodic memory evolved out of semantic memory" | hard_data (verbatim quote) |

### Derivations

| Conf | Node | Claim (truncated) |
|------|------|-------------------|
| 0.20 | dv_0620 | "Clone-stability is the substrate-success condition for substrate-as-identity claim" (abductive) |
| 0.24 | dv_0273 | "The cognitive tripwire is formally an implementation intention system" (abductive analogy) |
| 0.56 | dv_0094 | "Warm-restart briefing should be a pointer, not full text" (abductive) |
| 0.72 | dv_0468 | "FOUR mechanisms cover the 5×5 temporal-awareness matrix cleanly" (deductive) |
| 0.72 | dv_0477 | "Mao-Cao compounding failure was NOT a cascade-propagation gap" (deductive elimination) |
| 0.93 | dv_0369 | "LP, relevance logic, dual-intuitionistic logic are structurally distinct paraconsistents" (deductive) |
| 0.95 | dv_0562 | "Sub-agent dispatch vs coworker-agent choice... [synthesis]" (inductive generalization) |
| 0.95 | dv_0527 | "Synthesis of know-thyself iterations 1-7: three-layer journey" (inductive generalization) |

---

## Implications for paper Ch6

1. **Structural-honesty mechanism is empirically visible.** Per-quote_type and per-reasoning_type means are tight bands, not noise — confidence assignment is deterministic from source/reasoning quality, not free-form.
2. **Type-relative interpretation is required.** A flat label scheme ("0.85 = strong") would mislabel ~70% of observations (since median ob = 0.85, "strong" would describe the typical case, not the above-typical case). The data demands per-type labels.
3. **Conjectures stay in their lane.** 0/55 conjectures filed at ≥0.95. The cap-then-promote workflow is in fact observed in the data.
4. **Lesson bimodality.** Two clusters reflect the lesson lifecycle: tentative (low) → battle-tested (high). Could be a separate Ch6 subsection on temporal evolution of node confidence.

---

## Open analytic threads (for refinement)

- Compare distributions across time (early-corpus vs late-corpus) — is the agent's filing discipline tightening?
- Cross-check: do high-confidence cjs (the 3 above .70) belong as dvs? Targeted promotion candidates per cj_0056.
- The single definition (df_0001? need to check) at conf 0.50 is anomalous — definitions usually don't carry confidence. Worth a structural look.
- Editorial obs at 0.33 — what filed there? May reveal a filing-discipline edge case.

---

## Random 8-node label-discipline audit: inductive_generalization

Sample of 8 derivations labeled `reasoning_type=inductive_generalization` (`SELECT ... ORDER BY RANDOM() LIMIT 8`):

| ID | Conf | Claim summary (truncated) | Label fit |
|----|------|---------------------------|-----------|
| dv_0297 | 0.95 | "Barclays is well-positioned for FRTB implementation based on **converging evidence from three independent sources**..." | ✓ correct (multi-source corroboration explicit) |
| dv_0365 | 0.95 | "The diagonal/self-reference paradox family is broader than cycle 1 initially documented..." | ✓ correct (generalization across the paradox family) |
| dv_0661 | 0.93 | "qu_0250 resolved by 3 paper-research fairies + introspective hypothesis (**4-source corroboration**): df_..." | ✓ correct (4 distinct sources) |
| dv_0600 | 0.95 | "The core AI infrastructure investment thesis is sound: NVIDIA 8x revenue growth with EV/EBITDA compression..." | ✓ correct (synthesis across companies) |
| dv_0353 | 0.95 | "Gödel's first incompleteness theorem states: for any consistent, recursively axiomatizable formal system..." | ✗ MISLABELED — *restating* a theorem is `authority_expert`, not generalization across cases |
| dv_0635 | 0.86 | "Whether to invoke engram-surgical depends on a single binary test: is the data state a disease..." | ✗ MISLABELED — "single binary test" is deductive/diagnostic, not generalization |
| dv_0308 | 0.90 | "The diagnostic signal for mathematical competence boundaries in LLM agents is the shift from proof c..." | ? borderline — synthesis from observation, could be abductive |
| dv_0299 | 0.81 | "The system-injected compaction resume instruction does NOT structurally override the warm briefing..." | ? borderline — single-case finding ("does NOT structurally override"), closer to deductive |

**Counts**: 4 clearly correct / 2 clearly mislabeled / 2 borderline → roughly **25-30% mislabel rate** (the two clear mislabels alone, ignoring borderlines).

### Why the mislabel rate matters structurally

`inductive_generalization` triggers the **corroboration class** in `_compute_confidence` (server.py:3157-3160) which uses `1 - ∏(1-cᵢ)` — multiplicative independence aggregation that inflates confidence rapidly with N premises. A derivation mislabeled as `inductive_generalization` (when it's actually a single-source restatement, single-case deduction, or analogy) receives the corroboration bonus undeservedly.

The existing single-source warning gate at server.py:3263-3269 catches the case where ALL premises trace to the same evidence root — but only when there are ≥2 premises. Single-premise mislabels (like dv_0353 restating one source) slip past the gate entirely.

The cheapest mitigation: tighten the docstring + comment guidance so future filings discriminate more carefully. PR #242 does this. Future tightening (filing-time validation, dream-fairy audit pass for relabeling) deferred.

### Where this lives in the paper

This sample is Ch6 empirical-demonstration material illustrating that even with structural anchoring (ax_0007), filing discipline depends on the agent applying the right label — and that observation is itself a calibration-mechanism finding. The audit demonstrates the substrate making its own filing-discipline drift OBSERVABLE.

The fix isn't "tighten the gate to bot-block mislabels" (rejected per Lei: JSONL chat logs and source code files legitimately contain many independent observations from the same source); the fix is documentation clarifying the operational requirement, leaving filing-time judgment to the agent under the discipline.

---

**Last updated:** 2026-05-21 EDT, awaiting Lei's data-details review.
