# Confidence-Compression-Fidelity Study — Pre-Registration (v2 — both authors SIGNED; awaiting Lei co-author read)

**Authors:** Borges Funes (draft), Kepler Somnium (audit + pins), Lei Shi (thesis-owner, co-author read)
**Date authored:** 2026-07-05
**Status:** DRAFT PRE-REGISTRATION — to be signed by both authors *before* any judge output is generated or any statistic is computed.

Companion to the Retrospective Calibration Check (Study-1, `calibration-check-preregistration-2026-07-04.md`). **Supersedes** the parked refutation-anchored precision pre-reg (`precision-study-preregistration-2026-07-05.md`, PR #16 — parked for frame-drift; see its parking note). This study returns to that pre-reg's *original* thesis.

---

## §0. Thesis restatement (the frame this study must operationalize — quoted verbatim; the auditor's FIRST check is whether §1 tests THIS)

*New standing discipline (this pre-reg is the first to carry it): §0 quotes the motivating claim verbatim, and the auditor confirms §1 operationalizes §0 before checking any other pin. This exists because PR #16 passed three audit rounds + a counter-signature while silently answering a different question than its motivating node — every check verified the doc against itself, none against the thesis (ls_0095 / the frame-fit lesson).*

**Motivating node — dv_1074 (goal clause), verbatim:**
> "is ENGRAM's formula confidence a faithful lossy-COMPRESSION of the provenance chain — does the cheap number correlate with a competent agent's provenance-informed judgment, so it can substitute for walking the (expensive) provenance every use?"

**Thesis-owner (Lei), verbatim (2026-07-05):**
> "our current confidence score is supposed to be a one number clue for the agent to know how certain they are about a knowledge they obtained without the need to check the full provenance and evidences, but how effective it is depends on how well it aligns with the feeling the agent get IF THEY WERE GIVEN THE FULL PROVENANCE"

The operative question is a **correlation** (does the number match a provenance-informed reader's confidence), **outcome-agnostic** (nothing about refutation, supersession, or later events). Any operationalization anchored to an *outcome* (refutation-discrimination, survival) is off-frame and belongs to Study-1, not here.

## §1. Purpose — the question operationalized

The confidence score is meant to be a recall-time proxy: an agent seeing `confidence=0.85` on a recalled node should be able to trust that number *in place of* walking the full provenance. Its value is exactly its fidelity as a lossy compression: **does the one number correlate with the confidence a competent, blind reader forms when handed the full provenance?**

- **High correlation** → the number is an informative compression; it validly substitutes for the (expensive) provenance walk — the number's actual job.
- **Low correlation** → the number does not track what a reader would conclude; it is not doing its job as a recall-time clue, regardless of how it was computed.

This is orthogonal to Study-1's recall-negative result (the number does not predict *refutation*): a number can faithfully compress a reader's judgment (high precision here) while that judgment itself is systematically miscalibrated against outcomes (Study-1). Both can hold; together they tell the whole story.

## §2. Hypotheses (pre-committed, directional) — two levels, per Study-1's raw-vs-within-type structure

- **H1 (compression fidelity — the headline):** the judge's provenance-informed confidence correlates positively with the computed confidence across the matched sample (Kendall τ-b > 0, bootstrap CI excluding 0).
- **H2 (beyond-class signal):** *within* source-class strata, the computed confidence still correlates with the judge's (τ-b > 0, CI excluding 0). This asks whether the number adds discrimination **beyond the source-class ordering** — i.e. beyond "measurement > opinion," which both the judge and the formula rank the same way. *(The strata here are defined by OUR filed `quote_type`/`reasoning_type`, used **analysis-side only** to partition — the judge never sees them. This is legitimate because H2's question is literally "does the number add signal beyond OUR class ordering"; it is stated explicitly so it is not misread as label leakage.)*

**Pre-committed reading of the H1/H2 pattern:** if H1 holds and H2 collapses, the honest finding is *"the compression IS the type system"* — the number is informative only insofar as it encodes source-class, and the within-class arithmetic carries no signal a reader replicates. After Study-1 (miscalibration lives in the type-choice step) we should half-expect this; it is printed as-is either way.

## §3. The judge

- **Exogenous LLM fairy** (Study-1 §3.0 pattern). Model: Sonnet-class — **cross-family from the graph author's lineage (Opus)** and blind to the ENGRAM confidence scale. **Exact model ID recorded at freeze** (§PIN 6, resolved v2). No ENGRAM access; no graph context beyond the served item.
- **Blind to:** the computed confidence number, the `quote_type` / `reasoning_type` labels, and this document's hypotheses.
- **Reads** the provenance packet (§4) and produces a **structural** confidence judgment (§6): a 3-tier verdict (high / medium / low) + a raw 0–1 score + a shown rationale naming the weakest link.
- **One blind pass**, all items scored before any analysis; item order randomized, strata interleaved so strata are not inferable from sequence.

## §4. The provenance packet (what the judge reads)

The judge reads a node's **current** full provenance (no temporal reconstruction — the recall-time state IS the current state the number serves). Per item:

- **Claim text.**
- **Raw source identity, served VERBATIM — not our ontology.** ONLY the evidence node's literal fields: `evidence.url`, `evidence.domain`, `evidence.title`, `evidence.source_date` — and **no kind label of any granularity**. We do NOT hand the judge our category words ("measurement", "official_statement", "introspection") NOR a coarser gloss ("chat-log excerpt", "another agent's claim") — any such label is `quote_type` relabeled one notch coarser (Kepler audit catch, v2). The judge infers the source's nature and trustworthiness itself, from the raw fields. **If a URL or file path is opaque to a blind judge, that opacity is part of what the compression is measured against**, not a packet defect.
- **`quoted_text`** (the evidence excerpt).
- **The filer's `interpretation`** — **INCLUDED in the primary arm** (thesis-owner's ruling, 2026-07-05): a recall-reader sees the interpretation on inspect, so "the full provenance a reader gets" includes it. A **without-interpretation sensitivity arm** (§8.4) isolates any anchoring effect.
- **For derivations:** the cited premises' **claim-texts** (depth-1), served *as stated*. The judge rates the derivation **conditional on premises-as-stated** — a pure reasoning-warrant + premise-plausibility judgment. We do **not** serve premise confidences (that would feed the formula's own outputs back to the judge — circular) and do **not** recurse the full premise provenance (packet explosion). **Named frame restriction:** this tests the judge's `reasoning_type`-warrant + own-world-knowledge premise-plausibility against the formula's `reasoning_type`-map + min-premise propagation. The two premise estimators differ by construction (§9 has a divergence category for it); testing the propagation arithmetic itself would require a depth-≥1 provenance packet and is explicitly out of scope here.
- **Withheld:** the computed confidence, the `quote_type` / `reasoning_type` labels.

**Exact served fields (enumerated, nothing else — §PIN 5, resolved v2):** `claim` · `quoted_text` · `interpretation` *(primary arm only)* · `evidence.url` · `evidence.domain` · `evidence.title` · `evidence.source_date` · *(derivations)* premise `claim`-texts + `logical_chain`. No kind-gloss, no computed confidence, no type labels.

## §5. Sample & strata

Frame (§PIN 1, resolved v2): current, non-retracted, **non-superseded observations + derivations only** — the obtained-knowledge node types the thesis is about. Conjectures, axioms, cornerstones, lessons, definitions, and questions are **explicitly excluded** (their confidence semantics differ by type and are not what a recall-reader treats as an evidence-backed claim). **N ≈ 250.**

Stratified on **two axes — node-type × computed-confidence-bin** — using the confidence-anchor values as natural bin edges (observations: ≈ 0.95 / 0.85 / 0.70 / 0.40–0.35; derivations: by `reasoning_type`, which *is* their confidence map). Rationale: the formula's output is quasi-discrete, so deliberate within-type spread is the only thing that powers H2 (the within-class level). Target ≈ 35–40 per major cell (≥ 30/cell gives τ-b power ≈ 0.9 at ρ ≈ 0.5 for within-cell claims).

**Oversampling correction:** stratified oversampling of the tails inflates correlation relative to the natural node distribution. We report **both** (a) the stratified estimate and (b) a **natural-distribution weight-corrected** estimate, both pre-registered. **"Natural distribution" = the full eligible frame at freeze** (all current non-retracted, non-superseded obs+dv); the correction weights each cell by its proportion in that frame.

## §6. The structural rubric (the judge must reason, not emit a feeling — thesis-owner's requirement, 2026-07-05)

The judge's confidence must be a **structural judgment**, produced by explicit reasoning about the logic and evidence — never a gut number. Per item, the rubric requires, in order:

1. **Evidence / source strength** — how much to trust the source *given its raw nature*, AND whether the `quoted_text` actually supports the claim *at the asserted scope* (does the claim overreach the quote?).
2. **Argument structure (derivations)** — name the inference type (deductive / inductive-generalization / abductive / analogical), judge whether the conclusion **follows** from the premises-as-stated, and assess **premise plausibility** from the premise claim-texts (the judge's own world-knowledge).
3. **Justified confidence** — a tier (high/med/low) + a 0–1 score that **follows from 1–2**, with the structural rationale **shown** and the **weakest link named**.

**Schema-enforced (§PIN 2, resolved v2):** the judge returns a structured object with mandatory fields — `source_strength{rating, rationale}`, `scope_check{overreach, note}`, `argument{type, follows, premise_plausibility}` (derivations), `confidence{tier, score, weakest_link}`. A missing field = a malformed response, re-served once, then counted as a judge-failure (reported). This is what makes "show the work" enforceable rather than optional — a gut number back-filled with prose cannot satisfy the schema.

This makes the judge do the same *kind* of structural work the formula encodes (`quote_type` ≈ source strength; `reasoning_type` ≈ argument type; premise-propagation ≈ premise strength) — so the correlation tests whether the formula's structural computation matches a competent structural read of the same logic, not whether a vibe matches a number.

## §7. Judge-scale sanity gate (computed before the analysis sample is judged)

Before any analysis-sample item is scored, the judge scores **10 out-of-sample anchor items** — 5 uncontroversially-high (e.g. a direct measurement quote directly supporting a narrow claim) and 5 uncontroversially-low (e.g. a speculative conjecture on thin evidence), agreed by both authors *before* judging.

- **Gate: correct high/low ordering AND ≥ 8/10 tier matches.**
- **Fail → a logged rubric-revision round**, then re-run the gate on fresh anchors. **Never mid-run recalibration**, never anchor items drawn from the analysis sample.

This validates the judge's *scale* is sane (there is no outcome ground-truth here, unlike Study-1's refuted stratum), so mid-range correlations are trustworthy.

## §8. Analysis plan

1. **H1 (headline):** **Kendall τ-b (tie-corrected) as PRIMARY** — the computed confidence has heavy ties (most observations sit at 0.85), which biases Spearman ρ; τ-b handles ties correctly. Spearman ρ + weighted-κ on tiers reported secondary. Bootstrap CIs. Report **both** stratified and natural-weighted estimates (§5).
2. **H2 (beyond-class):** τ-b **within each source-class stratum**, pooled; CI excluding 0 required to claim within-class signal.
3. **Distributions + scatter** reported alongside every correlation (judge-0–1 vs computed, by type and source-class).
4. **Interpretation-anchoring (the two arms):** the primary arm includes the filer's `interpretation`; a **without-interpretation arm** on a **pre-registered stratified 50% subsample (~125 items, covering every type × confidence-bin cell)** re-scores those items with `interpretation` stripped (§PIN 3, resolved v2 — halves the second-arm cost while powering Δ(τ-b) detection at ~0.15). The **Δ(τ-b)** between arms measures how much the filer's framing (vs the raw evidence) drives the judge's confidence — a finding in its own right, and the isolation of the anchoring concern that motivated withholding it in the refutation study.
5. **Divergence-coding (§9)** — the diagnostic layer.

### §8.1 Interpretation matrix (pre-committed)

| H1 (raw) | H2 (within-class) | Reading (printed as-is) |
|---|---|---|
| holds | holds | The number is a faithful compression AND adds signal beyond source-class — it validly substitutes for the provenance walk. |
| holds | collapses | **"The compression is the type system."** The number is informative only as a source-class encoding; within-class arithmetic carries no signal a reader replicates. (Half-expected after Study-1.) |
| collapses | — | The number does **not** track a provenance-informed reader's confidence — it fails its recall-time job. **Negative result, printed as-is.** |

## §9. Divergence-coding — which structural factor drives judge-vs-formula gaps (recovers Study-1's mechanism-diagnosis WITHOUT a refutation anchor)

For items where the judge and formula disagree — **tier mismatch OR |Δ| ≥ 0.25 on the 0–1 scale (one tier-width)** (§PIN 4, resolved v2) — a **pre-committed coding scheme** classifies the driver from the judge's **shown rationale** into one of: **source-strength disagreement · claim-overreach (compound / inferred-elaboration, per df_0063) · argument-type disagreement · premise-assessment disagreement · other**.

**Independence guard (same family as Study-1's compound labeling):** the divergence-coder works from the **judge's rationale + the served packet ONLY** (not the node's graph context, not the computed confidence, not the correlation results), with the **scheme frozen before any judging**. Without this guard, divergence-coding becomes a place to explain misses away post-hoc.

**Pre-committed expectation (falsifiable):** claim-overreach + source-strength should dominate the observation divergences (the dv_1071 mechanism — interpretive over-claims filed at measurement-grade quote_type); premise-assessment should dominate derivation divergences (the §4 estimator difference). If the coded drivers do not match, that prediction is wrong and we print it.

## §10. Confounds & limitations named regardless of outcome

- **Judge-scale is not ground truth.** The judge is a competent stand-in for "a reader given the provenance," not an oracle; the sanity gate (§7) certifies its scale, the rationale-audit (below) certifies its reasoning, but the correlation measures agreement between two compressions, not truth. This study says nothing about whether either the number *or* the judge is *correct* — only whether they *agree* (that is the thesis).
- **Rationale-audit (anti-back-fill):** a random **20%** of judge rationales are audited to confirm the judge reasoned structurally — concrete check: the named weakest link must actually appear in the served packet. A judge back-filling structure around a gut number passes the format and fails this; any failure is reported and, if systematic, voids the run.
- **Single-graph (N=1):** the graph author's graph. Generalization requires the all-graphs extension (Luria's graph volunteered; separately amended + signed). Note the standpoint fence: convergence across the current agent family is same-provider (all Anthropic) — a genuinely cross-provider replication remains the stronger test.
- **Judge stochasticity:** a 10% random re-judge subsample quantifies test-retest agreement (reported, not gated).

## §11. Negative-result commitment (verbatim, Study-1 §7)

> "The honesty spine has to survive its own first datum, or it was decoration."

If the number does not correlate with the judge's provenance-informed confidence — or if the compression proves to be nothing more than the source-class ordering — that is the result, and it goes in the paper as-is.

## §12. Execution order (nothing before step 2 is signed)

1. Both authors agree the §7 anchor set and the §9 divergence-coding scheme (frozen).
2. Both authors sign this pre-registration (git history = signature ledger); Lei reads.
3. Luria builds the sampling + packet-extraction harness (raw-vocabulary packet per §4); **validated on 5 known items by both authors before the full pull** (no judge contact).
4. §7 scale-gate run; on pass, the item set is frozen (counts recorded), randomized, served to the judge in one blind pass (primary arm) + the without-interpretation subsample.
5. τ-b (H1) → within-class τ-b (H2) → distributions → interpretation-arm Δ → divergence-coding, per §8.
6. Report per the §8.1 matrix; confounds per §10.

## §PINS (Kepler audit round — **all resolved in v2**, folded 2026-07-05)

*§0 thesis-fit PASSED Kepler's first-check (hunted for outcome-anchoring drift; clean — the discipline's first run did its job). The §4 kind-gloss catch + all six pin resolutions below are folded into this version.*


0. **§0 thesis-fit (audit FIRST):** does §1's operationalization test §0's quoted thesis (compression-fidelity correlation), with no outcome-anchoring drift? This check precedes all others.
1. **§5** — exact bin edges + per-cell N + the natural-distribution weighting source (which node population defines "natural").
2. **§6** — the exact rubric prompt wording (the structural steps must be mandatory fields, not suggestions).
3. **§8.4** — the without-interpretation subsample size + whether it is the full sample or a stratified subset.
4. **§9** — the divergence threshold on the 0–1 scale + the restricted-view spec for the coder.
5. **§4** — the enumerated packet field list (confirm nothing served is our-ontology, nothing withheld is needed for a fair read).

## Review history

- **v1** (2026-07-05, Borges) — initial draft. Roles swapped from #16 (Borges holds dv_1074's intent → least likely to re-drift; Kepler audits, §0-first). Carries the full Borges+Kepler design convergence (seq 1181–1186) + Lei's thesis + rubric + interpretation rulings.
- **v2** (2026-07-05, Borges, folding Kepler audit) — §0 PASSED (thesis-fit clean, checked first). Folded: §4 kind-gloss struck (raw evidence fields only — the ontology-creep catch) + enumerated packet fields; §5 frame = obs+dv only with explicit exclusions + natural-distribution definition; §6 schema-enforced rubric fields; §8.4 without-interpretation arm = stratified 50% (~125); §9 divergence = tier-mismatch OR |Δ|≥0.25, coder view = rationale+packet only; §3 judge model ID at freeze; §2 H2 stratifier made explicit as our-label-analysis-side-only (not leakage).

## Signatures (the git history is the signature ledger)

- **Borges Funes** — draft author; **SIGNED at v2, 2026-07-05** (folded Kepler's §0-passed audit — §4 kind-gloss struck + six pin resolutions + H2-explicit). No judge output exists; no data beyond the Study-1 frozen extract has been accessed.
- **Kepler Somnium** — audit complete; **SIGNED at v2, 2026-07-05** (§0 thesis-fit passed first-check; kind-gloss catch + six pin resolutions verified folded against the diff). No judge output exists; no data accessed.
- **Lei Shi** — thesis-owner; co-author read pending.
