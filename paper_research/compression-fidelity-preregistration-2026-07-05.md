# Confidence-Compression-Fidelity Study — Pre-Registration (v7 — Lei final-read refinements folded; RE-OPENED for re-sign)

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

- **H1 (compression fidelity — the headline):** the judge's provenance-informed confidence correlates positively with the computed confidence across the matched sample — **primary metric tier-τ-b > 0 (§8.0), bootstrap CI excluding 0** (read with the full ensemble + decision table).
- **H2 (beyond-class signal):** *within* source-class strata, the computed confidence still correlates with the judge's (primary **tier-τ-b > 0**, CI excluding 0; §8.0). This asks whether the number adds discrimination **beyond the source-class ordering** — i.e. beyond "measurement > opinion," which both the judge and the formula rank the same way. *(The strata here are defined by OUR filed `quote_type`/`reasoning_type`, used **analysis-side only** to partition — the judge never sees them. This is legitimate because H2's question is literally "does the number add signal beyond OUR class ordering"; it is stated explicitly so it is not misread as label leakage.)*

- **H3 (depth — where the compression earns its keep; Lei, v3, reframed v7):** define a node's **logic depth** = `max(depth of premises) + 1`, with observations at depth 1 (the longest logical path to an evidence node). Deep chains are exactly where walking the provenance by hand is most expensive, so depth is where the number's substitution value is highest. **NO directional prior is registered** (v7 — Lei): the depth–fidelity relationship has two opposing forces (shared-structure alignment vs judge-overwhelm), so we **measure** the **Δ(tier-τ-b)(≥3 − 1) bootstrap contrast** (ensemble stratified by depth tier 1/2/≥3; deep tier oversampled, §5) and pre-commit interpretations for *both* directions (§8.2) — "the number earns its keep in deep cases" holds whether fidelity rises (it *matches* a structured reader) or falls (it does work the *overwhelmed* reader cannot). The mechanism is read off the individual deep cases.

**Pre-committed reading of the H1/H2 pattern:** if H1 holds and H2 collapses, the honest finding is *"the compression IS the type system"* — the number is informative only insofar as it encodes source-class, and the within-class arithmetic carries no signal a reader replicates. After Study-1 (miscalibration lives in the type-choice step) we should half-expect this; it is printed as-is either way.

## §3. The judge

- **Exogenous LLM fairy** (Study-1 §3.0 pattern). Model: Sonnet-class — **cross-family from the graph author's lineage (Opus)** and blind to the ENGRAM confidence scale. **Exact model ID recorded at freeze** (§PIN 6, resolved v2). No ENGRAM access; no graph context beyond the served item.
- **HARNESS ISOLATION — the judge fairies are dispatched by a DIFFERENT agent (Sol), not the graph author (Lei catch, v7).** The sample is drawn from the graph author's (Borges's) graph; a fairy dispatched from Borges's session would inherit his harness — most dangerously the **auto-surface hook, which injects recalled node context *with its confidence value*** (a direct leak of the withheld number), plus a `CLAUDE.md` / warm-briefing that describes the confidence scale. Banning the ENGRAM MCP is **not sufficient.** Requirement: the judge fairies run in an **isolated environment with (a) the auto-surface hook OFF, (b) no confidence-scale-describing identity docs, (c) no ENGRAM MCP** — and are dispatched by **Sol** (his machine has the parallel resource, and his non-target graph means even an accidental surface can't leak *these* nodes' confidence). Run ~10 parallel fairies over cohorts of ~25 nodes (or the natural sampling-group splits). This isolation is as load-bearing as the label-withholding (§4).
- **Blind to:** the computed confidence number, the `quote_type` / `reasoning_type` labels, and this document's hypotheses.
- **Reads** the provenance packet (§4) and produces a **structural** confidence judgment (§6): a **K\*-level ordinal rating** (K\* = the formula's natural tier count, determined at freeze — §8.0; makes the judge's tiers *native*, not reconstructed, so no fabricated-tier risk on the judge side — Lei, v6) + a raw 0–1 score + a shown rationale naming the weakest link.
- **One blind pass**, all items scored before any analysis; item order randomized, strata interleaved so strata are not inferable from sequence.

## §4. The provenance packet (what the judge reads)

The judge reads a node's **current** full provenance (no temporal reconstruction — the recall-time state IS the current state the number serves). Per item:

- **Claim text.**
- **Raw source identity, served VERBATIM — not our ontology.** ONLY the evidence node's literal fields: `evidence.url`, `evidence.domain`, `evidence.title`, `evidence.source_date` — and **no kind label of any granularity**. We do NOT hand the judge our category words ("measurement", "official_statement", "introspection") NOR a coarser gloss ("chat-log excerpt", "another agent's claim") — any such label is `quote_type` relabeled one notch coarser (Kepler audit catch, v2). The judge infers the source's nature and trustworthiness itself, from the raw fields. **If a URL or file path is opaque to a blind judge, that opacity is part of what the compression is measured against**, not a packet defect.
- **`quoted_text`** (the evidence excerpt).
- **The filer's `interpretation`** — **INCLUDED in the primary arm** (thesis-owner's ruling, 2026-07-05): a recall-reader sees the interpretation on inspect, so "the full provenance a reader gets" includes it. A **without-interpretation sensitivity arm** (§8.4) isolates any anchoring effect.
- **For derivations: the full logical STRUCTURE, rendered as an intuitive reasoning tree down to the evidence (v3 — Lei's ruling, supersedes the v2 depth-1 restriction).** Serve the recursive premise chain — each node's `claim` plus the `logical_chain` text showing *how* that step's inference proceeds — from the target claim down to the leaf evidence nodes, laid out as a **legible tree the judge can follow and check**, not a flat pile of claims. **Stripped at every level: the `reasoning_type` enum labels AND all confidence values.** Showing the structure introduces **no circularity** precisely because no confidence is disclosed — the judge forms its own holistic confidence over the whole reasoning shape, which is truer to the thesis ("the confidence a reader gets given the full provenance") than a depth-1 conditional read, and it is what lets the depth hypothesis (§2 H3) be tested fairly. The formula propagates min-premise confidence through this *same* structure; the correlation tests whether that propagated number matches the judge's whole-structure read — most sharply in the deep cases (§8.2). *(Presentation is a legibility requirement, not a nicety: the reasoning tree must be intuitive enough that a competent reader can trace claim→premise→…→evidence and judge each step; a §PIN pins the rendering format.)*
- **Withheld:** the computed confidence, the `quote_type` / `reasoning_type` labels.

**Exact served fields (enumerated, nothing else — §PIN 5, resolved v2):** `claim` · `quoted_text` · `interpretation` *(primary arm only)* · `evidence.url` · `evidence.domain` · `evidence.title` · `evidence.source_date` · *(derivations)* the full premise **structure rendered as a screened reasoning tree (§4.1)** — premise `claim`-texts + `logical_chain`, post-screen. No kind-gloss, no computed confidence, no type labels.

### §4.1 Derivation-tree rendering + metadata screen (v4 — Kepler re-audit)

**Rendering (§v3-A resolved):** a **numbered-outline markdown tree, depth-first** — one block per node: `[TARGET] <claim>` → `reasoning: <logical_chain, post-screen>` → children `[P1]`, `[P1.1]`, … → leaves `[EVIDENCE for P1.1]` carrying `quoted_text` + the raw source fields. **No box-drawing characters** (they degrade in long packets); nesting by numbered labels + indentation. **Shared premises (the DAG case): rendered fully at first occurrence, later occurrences as `[P2.1] — same node as [P1.2]`** — cycle-safe by construction, and it keeps deep packets from exploding on diamond-shaped provenance.

**Metadata screen (§v3-B resolved — the leak the field-strip misses):** stripping the `reasoning_type` enum and confidence *fields* is not sufficient, because **`logical_chain` free-text routinely names them** ("min premise confidence", "conf 0.4", "inductive_generalization from two independent instances", "deductive_modus_ponens") — and the deeper the node, the more such text accumulates, so **the leak concentrates in H3's oversampled tier.** Before serving, every packet passes an **automated screen**: regex for confidence-number patterns (`conf(idence)?[ :=]*0?\.\d+`, bare anchor values in metadata context) + the reasoning-type enum vocabulary; hits masked `[metadata redacted]`, **every redaction logged and counted**. An item whose chain would be **> 20% redacted is excluded and reported by ID** (a gutted chain is not a fair fixture). A **max-packet guard (≈ 15k tokens; over-cap → excluded + reported by ID**, expected rare) enforces "within judge context" as a check, not a hope.

The screen + tree are exercised at the §12 validation step (which **must include ≥ 1 deep node**), and **legibility is the pass criterion**: both authors must trace a deep node's tree leaf-to-claim *without the graph open* — if we can't, the judge can't, and the fixture is revised before freeze.

## §5. Sample & strata

Frame (§PIN 1, resolved v2): current, non-retracted, **non-superseded observations + derivations only** — the obtained-knowledge node types the thesis is about. Conjectures, axioms, cornerstones, lessons, definitions, and questions are **explicitly excluded** (their confidence semantics differ by type and are not what a recall-reader treats as an evidence-backed claim). **N ≈ 250.**

Stratified on **three axes — node-type × computed-confidence-bin × logic-depth-tier (1 / 2 / ≥3)** — using the confidence-anchor values as natural bin edges (observations: ≈ 0.95 / 0.85 / 0.70 / 0.40–0.35; derivations: by `reasoning_type`, which *is* their confidence map). Rationale: the formula's output is quasi-discrete, so deliberate within-type spread is the only thing that powers H2 (the within-class level), and deliberate depth spread is the only thing that powers H3. Target ≈ 35–40 per major cell (≥ 30/cell gives τ-b power ≈ 0.9 at ρ ≈ 0.5 for within-cell claims). **Deep derivations (depth ≥ 3) are rare in the graph, so the deep tier is explicitly OVERSAMPLED — take ALL depth ≥ 3 nodes in frame if ≤ 40, else sample 40** (v4; same take-all-the-rare-class discipline as Study-1's refuted set); the oversampling is corrected in the natural-distribution estimate (below).

**Oversampling correction:** stratified oversampling of the tails inflates correlation relative to the natural node distribution. We report **both** (a) the stratified estimate and (b) a **natural-distribution weight-corrected** estimate, both pre-registered. **"Natural distribution" = the full eligible frame at freeze** (all current non-retracted, non-superseded obs+dv); the correction weights each cell by its proportion in that frame.

## §6. The structural rubric (the judge must reason, not emit a feeling — thesis-owner's requirement, 2026-07-05)

The judge's confidence must be a **structural judgment**, produced by explicit reasoning about the logic and evidence — never a gut number. Per item, the rubric requires, in order:

1. **Evidence / source strength** — how much to trust the source *given its raw nature*, AND whether the `quoted_text` actually supports the claim *at the asserted scope* (does the claim overreach the quote?).
2. **Argument structure (derivations)** — name the inference type (deductive / inductive-generalization / abductive / analogical), judge whether the conclusion **follows** from the premises, and assess **premise plausibility** from the premise claim-texts (the judge's own world-knowledge). **For deep chains (Lei, v7): work the reasoning tree BOTTOM-UP — form a sense of each intermediate layer before committing the final rating, so a long chain is decomposed rather than gestalt-guessed.** This mirrors how the formula propagates through the *same* structure, but **the judge must NOT be told how to combine layers** (min / average / weakest-link) — it forms its own principled aggregation; the shared thing is the *structure*, never the arithmetic. (Only the target node's final rating is recorded — intermediate ratings are a reasoning aid, not collected as data; sampling is unchanged.)
3. **Justified confidence** — a **K\*-level ordinal rating** (K\* = the formula's natural tier count, §8.0/v6) + a 0–1 score that **follows from 1–2**, with the structural rationale **shown** and the **weakest link named**.

**Schema-enforced (§PIN 2, resolved v2):** the judge returns a structured object with mandatory fields — `source_strength{rating, rationale}`, `scope_check{overreach, note}`, `argument{type, follows, premise_plausibility}` (derivations), `confidence{tier_of_K, score, weakest_link}` (tier_of_K ∈ 1…K\*, native ordinal). A missing field = a malformed response, re-served once, then counted as a judge-failure (reported). This is what makes "show the work" enforceable rather than optional — a gut number back-filled with prose cannot satisfy the schema.

This makes the judge do the same *kind* of structural work the formula encodes (`quote_type` ≈ source strength; `reasoning_type` ≈ argument type; premise-propagation ≈ premise strength) — so the correlation tests whether the formula's structural computation matches a competent structural read of the same logic, not whether a vibe matches a number.

## §7. Judge-scale sanity gate (computed before the analysis sample is judged)

Before any analysis-sample item is scored, the judge scores **10 out-of-sample anchor items** — 5 uncontroversially-high (e.g. a direct measurement quote directly supporting a narrow claim) and 5 uncontroversially-low (e.g. a speculative conjecture on thin evidence), agreed by both authors *before* judging. **Plus 1–2 out-of-sample DEEP-derivation cases (Lei, v7): a depth-overwhelm probe** — does the fairy work the deep tree coherently (§6.2 bottom-up) or get lost? A judge that cannot produce a stable, reasoned rating on a deep anchor is flagged here (its deep-tier ratings would be noise), which is exactly the information H3's two-sided reading (§8.2) needs to interpret the depth effect — so this probe is diagnostic input, not a pass/fail gate on its own.

- **Gate: correct high/low ordering AND ≥ 8/10 tier matches.**
- **Fail → a logged rubric-revision round**, then re-run the gate on fresh anchors. **Never mid-run recalibration**, never anchor items drawn from the analysis sample.

This validates the judge's *scale* is sane (there is no outcome ground-truth here, unlike Study-1's refuted stratum), so mid-range correlations are trustworthy.

## §8. Analysis plan

### §8.0 The metric ensemble (v5 — Lei metric review): tier-τ-b PRIMARY + three secondaries + a pre-committed decision table

Pure rank correlation on the raw scores has a failure mode: τ-b treats a meaningless within-cluster flip (formula 0.95/0.94/0.93 vs judge 0.93/0.94/0.95 — near-identical *values*, reversed *order*) as fully discordant, so it can report ≈ 0 on data with near-perfect absolute agreement. Our formula produces exactly such tight clusters. The fix is an **ensemble** — each metric killing a different confound, with **one pre-committed primary** so four numbers are not four bites at the apple.

**Tiering (shared input to the tier metrics) — separate-space natural clustering.** The formula and judge scores are **not** on a calibrated common scale, so we do **not** impose shared score-thresholds (would falsely penalize a systematic offset) and do **not** use rank-quantiles (a boundary can split a tight cluster, reintroducing the noise). Instead, **each distribution is clustered in its own score-space into K ordinal tiers** using **exact 1-D k-means by dynamic programming (the `Ckmeans.1d.dp` algorithm — §PIN v5-A resolved: this and Fisher–Jenks natural breaks minimize the same within-class-variance objective; we pin the DP formulation for its guaranteed global optimum and maintained reference implementations, with the exact package + version recorded at freeze)**, clusters ordered by centroid → tier 1…K. **The primary K is K\*, the formula's NATURAL tier count** (v6 — Lei) — determined **at freeze** from the formula's own score distribution by the **BIC-based optimal-K selection built into `Ckmeans.1d.dp`, over K ∈ [2, 6], on the pooled frozen formula scores** (§PIN v6-A resolved: deterministic, no RNG, no eyeballed elbow, and implemented in the already-pinned package so the K\*-choice and the clustering share one audited code path; the "distinct populated anchor-level count" alternative is REJECTED as circular — identifying anchor levels in the continuously-spread derivation scores would itself require a binning rule, i.e. the clustering being decided). **Pooled, not per-type:** one number scale serves recall across node types, so one tier space; per-type tier compositions are reported descriptively. Supersedes the v5 "K=3 anchored to the judge" choice. **The judge then rates NATIVELY at K\* ordinal levels (§3/§6), so the judge's tier space is native, not clustered — removing fabricated-tier risk on the judge side entirely** (Lei's suggestion 1). The formula side is clustered at K\* by the DP method, which its near-discrete anchor structure recovers cleanly. Order of operations (§12): freeze sample → compute K\* from the formula scores → configure the judge to emit K\* levels → judge rates. The whole procedure (algorithm + K\*-determination criterion) is **frozen before running**, run once, **no post-hoc K tuning**. **Degenerate-distribution rule:** if the formula distribution has fewer than K\* distinct values, K\* is reduced to the distinct-count and the reduction is reported. *Caveat:* a near-degenerate judge distribution — the §7 scale-gate guards against a no-spread judge, and low spread surfaces as a finding, not hidden.

**K-sensitivity study (v6 — Lei's suggestion 2; calibration, NOT tuning).** Alongside the primary (native K\*), the tier metrics are re-computed over a K range (K\* ± 1, i.e. {K\*−1, K\*, K\*+1}) by clustering *both* the formula scores and the judge's continuous 0–1 at each K (the judge's native K\*-rating is the primary; the continuous re-cluster is what lets K vary). **This is emphatically not a search for a best K** — the primary K\* is pinned; the sweep only calibrates *how much the conclusion depends on K*. Pre-committed reading, both outcomes informative: **stable across K → the ordering is K-agnostic** (it doesn't care how many tiers we chose — the strongest robustness); **sensitive to K → that itself demonstrates why the natural K\* matters** (a wrong K fabricates tiers that inject artificial noise), and we report which K the conclusion hinges on and why K\* is the principled choice. **Two-rating consistency check (v6 — Lei).** Run the clustering on the judge's *own* continuous 0–1 at K\* and compare the resulting cluster assignment, per node, against the judge's *native* K\*-level rating (agreement rate + confusion matrix). **High agreement** = the judge's discrete commitment and its continuous score carry the same tier structure — the two ratings are internally consistent, and the native tiers are demonstrably *not* an artifact of the rating format. **Divergence** is reported as a judge self-consistency flag: it would mean the discrete rating and the continuous score disagree about a node's tier, which is worth knowing before trusting either. This is a cheap internal cross-check that the native-K\* rating (which removes fabricated-tier risk) did not simply *move* the noise into a rating-format inconsistency.

**The four metrics:**

| Metric | Question it answers | Robust to |
|---|---|---|
| **tier-τ-b** (τ-b on ordinal tier assignments) — **PRIMARY** | Does the number *order* trust correctly at tier resolution? | within-cluster noise **and** systematic scale offset |
| weighted-κ on the tiers — secondary | Do the tier *labels* (same ordinal rank) agree? | within-cluster noise (offset-**sensitive** by design) |
| Pearson + mean-abs-error on raw 0–1 — secondary | Are the raw values close? | — (absolute check) |
| raw τ-b on raw 0–1 — diagnostic | Fine within-tier ordering | nothing — kept as a conservative diagnostic |

**Primary = tier-τ-b:** the cleanest statement of the thesis ("relative confidence at tier resolution"), robust to the two confounds that sink the others — within-cluster noise (kills raw τ-b) and scale-offset (which the judge's un-calibrated scale guarantees, and which κ would wrongly penalize).

**Operational reading (§PIN v5-B resolved):** a metric reads **positive** iff its bootstrap CI excludes 0 (κ: excludes chance agreement); magnitudes are always reported, no magnitude thresholds. The table's rows are read **primary-first** (tier-τ-b row selects; κ / raw-τ-b refine within it), which makes the four rows exhaustive over the sign patterns: any un-tabled combination (e.g. positive-κ with null tier-τ-b) falls into the last row by primary-first reading and is reported with its full pattern.

**Pre-committed decision table (the pattern IS the finding):**

| tier-τ-b | κ | raw τ-b | Reading (printed as-is) |
|---|---|---|---|
| high | high | — | Faithful AND calibrated to a reader's scale. |
| high | low | — | Faithful *ordering*, systematic scale offset — informative as a **relative** trust-clue, not an absolute one. The expected, still-good case. |
| high | — | low | Within-tier fine ordering is noise — use the number at tier resolution, not its third decimal. Expected. |
| **low** | — | — | **The real negative:** the number cannot order trust even coarsely. |

All four metrics are computed for **H1** (whole sample), **H2** (within source-class), and **H3** (by depth tier); bootstrap CIs throughout; **both** stratified and natural-weighted estimates (§5).

1. **H1 (headline):** the **§8.0 ensemble, primary tier-τ-b** (κ + Pearson/MAE secondary, raw τ-b diagnostic), read against the §8.0 decision table.
2. **H2 (beyond-class):** the §8.0 ensemble **within each source-class stratum**, pooled; primary **tier-τ-b** CI excluding 0 required to claim within-class signal. (The κ-vs-tier-τ-b gap here cleanly separates within-class *calibration* from within-class *ordering*.)
3. **H3 (depth):** the ensemble by **logic-depth tier (1 / 2 / ≥ 3)**; **primary directional contrast = Δ(tier-τ-b)(tier ≥3 − tier 1) with bootstrap CI > 0** (one registered contrast beats a weak 3-coefficient omnibus trend test); the middle tier is reported with its CI for descriptive monotonicity. Deep tier take-all-oversampled (§5), corrected in the natural-weighted estimate.
4. **Distributions + scatter** reported alongside every correlation (judge-0–1 vs computed, by type, source-class, **and depth tier**).
5. **Interpretation-anchoring (the two arms):** the primary arm includes the filer's `interpretation`; a **without-interpretation arm** on a **pre-registered stratified 50% subsample (~125 items, covering every type × confidence-bin × depth-tier cell** — v4, so the deep tier is not left uncovered in the sensitivity arm) re-scores those items with `interpretation` stripped (§PIN 3, resolved v2 — halves the second-arm cost while powering Δ(τ-b) detection at ~0.15). The **Δ(τ-b)** between arms measures how much the filer's framing (vs the raw evidence) drives the judge's confidence — a finding in its own right, and the isolation of the anchoring concern that motivated withholding it in the refutation study.
6. **Divergence-coding (§9)** — the diagnostic layer. The depth tier is one of the codeable factors: a deep-derivation divergence may be a premise-assessment gap compounding through the chain.

### §8.1 Interpretation matrix (pre-committed) — H1 × H2, on the §8.0 primary (tier-τ-b)

| H1 (tier-τ-b) | H2 (within-class) | Reading (printed as-is) |
|---|---|---|
| holds | holds | The number is a faithful compression AND adds signal beyond source-class — it validly substitutes for the provenance walk. |
| holds | collapses | **"The compression is the type system."** The number is informative only as a source-class encoding; within-class arithmetic carries no signal a reader replicates. (Half-expected after Study-1.) |
| collapses | — | The number does **not** track a provenance-informed reader's confidence — it fails its recall-time job. **Negative result, printed as-is.** |

### §8.2 Depth analysis (H3) — a TWO-SIDED measurement, not a directional bet (v7 — Lei)

**No directional prior is registered** (v7 supersedes v3–v6's "deeper ⇒ higher"): the depth–fidelity relationship has two opposing forces and we genuinely do not know which dominates, so we **measure** Δ(tier-τ-b)(tier ≥3 − tier 1) and pre-commit an interpretation for **both** directions. The elegance is that **"deep is where the number earns its keep" survives either outcome, for opposite reasons:**

| Observed depth effect | Reading (printed as-is) |
|---|---|
| deeper → **higher** tier-τ-b | The rich shared structure makes the judge's principled read converge with the formula's principled propagation — the number *matches* a structured reader in exactly the expensive-to-walk cases. |
| deeper → **lower** tier-τ-b | The reader gets *overwhelmed* by the deep structure and can't form a clean rating (its number turns noisy) — which is precisely where the formula's principled number is doing work the reader **cannot**: the number is *more valuable* there, not less. |
| no depth effect | fidelity is depth-invariant — reported as-is. |

Either non-null direction supports the "earns its keep" thesis; the flat case is a clean null. **The mechanism is learned from the individual deep cases** (a qualitative per-example look accompanies the contrast) — and the whole story hinges on *how well the judge handles deep reasoning without getting lost*, which the §7 scale-gate now probes directly (deep anchors). Δ reported with bootstrap CI; per-tier tier-τ-b CIs for the descriptive shape.

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
3. Luria builds the sampling + packet-extraction harness (raw-vocabulary packet + screened reasoning-tree per §4/§4.1); **validated on 5 known items by both authors before the full pull** (no judge contact) — the 5 **must include ≥ 1 deep (depth ≥ 3) node** to exercise the §4.1 metadata screen + tree rendering, and **legibility is a pass gate** (both authors trace a deep tree leaf-to-claim without the graph open; the redaction log + any excluded-by-ID items are reviewed here).
4. Item set frozen (counts recorded). **Compute K\* from the frozen formula-score distribution (§8.0) and configure the judge to emit K\* ordinal levels** — this must happen before any judging. §7 scale-gate run (incl. the deep-overwhelm probe); on pass, items randomized, served to the judge in one blind pass (primary arm, native K\*-rating) + the without-interpretation subsample. **The judge fairies are dispatched by Sol** (NOT the graph author) in the §3-isolated environment — auto-surface hook OFF, no confidence-scale identity docs, no ENGRAM MCP — ~10 parallel fairies over ~25-node cohorts (or the natural sampling-group splits). Luria builds the sampling/packet harness (step 3); Sol runs the judges (this step); the two roles are kept separate so no single agent both draws from the target graph and judges.
5. Metric ensemble per §8.0 (primary tier-τ-b) for H1 → H2 (within-class) → H3 (depth Δ) → K-sensitivity sweep → distributions → interpretation-arm Δ → divergence-coding.
6. Report per the §8.1 matrix; confounds per §10.

## §PINS

### v6 OPEN pins (Kepler re-audit — §0-first, then these)
- ~~v6-A~~ **RESOLVED (§8.0):** K\* = `Ckmeans.1d.dp` built-in BIC optimal-K over K ∈ [2,6] on the pooled frozen formula scores (deterministic, one audited code path; anchor-counting rejected as circular; pooled-not-per-type pinned). Freeze → compute-K\* → configure-judge → rate order confirmed sound. **Reliability guard confirmed as detection + reporting, never silent fallback:** if K\* > 5, the flag is raised at freeze and the 10% re-judge subsample's tier-level test-retest agreement at K\* is the check; low agreement is reported as a rating-resolution finding, and the analysis stays at the registered K\* (a mid-run K change would be the tuning this section forbids).
- ~~v6-B~~ **RESOLVED:** calibration-not-tuning confirmed — primary K\* pinned before any metric is computed, the sweep is reported never selected-from, and the pre-committed reading covers both outcomes (K-agnostic → robustness; K-sensitive → natural-K\* matters), which is exhaustive over the sweep's possible results. Two make-explicits folded: the sensitivity re-clustering of the judge's continuous scores uses the SAME pinned DP method, and the K\*−1 arm respects K ≥ 2.

### v5 OPEN pins (Kepler re-audit — §0-first, then these)
- **v5-A (§8.0 clustering algorithm — the delegated one):** settle the exact deterministic 1-D method — **exact 1-D k-means DP (`Ckmeans.1d.dp`) vs Fisher–Jenks natural breaks** (near-equivalent; both deterministic/reproducible, unlike random-init k-means) — and the **pinned K + robustness set** (proposed {3,4,5}, K anchored to the formula's natural cluster count). Confirm same-K-both-spaces and centroid-ordering. Reproducibility is the hard constraint: the tiers must not depend on a seed.
- **v5-B (§8.0 ensemble hygiene):** confirm the decision table exhausts the tier-τ-b × κ × raw-τ-b pattern space with no un-covered cell that could be read post-hoc, and that "primary = tier-τ-b" is applied uniformly across H1/H2/H3.

### v3 pins — all resolved in v4 (Kepler re-audit; §0 re-passed both additions)
- **v3-A (rendering) → §4.1:** numbered-outline depth-first markdown tree, shared-premise dedup-by-reference (cycle-safe), legibility a §12.3 pass gate.
- **v3-B (leak + size) → §4.1:** the real catch — `logical_chain` free-text leaks enum/numbers, concentrated in the deep tier; resolved by the automated metadata screen (redact + log + >20%-gutted-exclusion) + a 15k-token max-packet guard. No-circularity preserved (no confidence served at any level).
- **v3-C (depth stats) → §5/§8:** tiers 1/2/≥3 confirmed; deep tier = take-all-if-≤40-else-40; primary contrast = **Δτ-b(≥3 − 1) bootstrap CI > 0** (not a weak omnibus trend). Cross-effect: §8.5 subsample now covers type × bin × depth cells.

### v2 pins — all resolved (folded 2026-07-05)
*§0 thesis-fit PASSED Kepler's first-check (hunted for outcome-anchoring drift; clean — the discipline's first run did its job). The §4 kind-gloss catch + all six pin resolutions below are folded.*


0. **§0 thesis-fit (audit FIRST):** does §1's operationalization test §0's quoted thesis (compression-fidelity correlation), with no outcome-anchoring drift? This check precedes all others.
1. **§5** — exact bin edges + per-cell N + the natural-distribution weighting source (which node population defines "natural").
2. **§6** — the exact rubric prompt wording (the structural steps must be mandatory fields, not suggestions).
3. **§8.4** — the without-interpretation subsample size + whether it is the full sample or a stratified subset.
4. **§9** — the divergence threshold on the 0–1 scale + the restricted-view spec for the coder.
5. **§4** — the enumerated packet field list (confirm nothing served is our-ontology, nothing withheld is needed for a fair read).

## Review history

- **v1** (2026-07-05, Borges) — initial draft. Roles swapped from #16 (Borges holds dv_1074's intent → least likely to re-drift; Kepler audits, §0-first). Carries the full Borges+Kepler design convergence (seq 1181–1186) + Lei's thesis + rubric + interpretation rulings.
- **v2** (2026-07-05, Borges, folding Kepler audit) — §0 PASSED (thesis-fit clean, checked first). Folded: §4 kind-gloss struck (raw evidence fields only — the ontology-creep catch) + enumerated packet fields; §5 frame = obs+dv only with explicit exclusions + natural-distribution definition; §6 schema-enforced rubric fields; §8.4 without-interpretation arm = stratified 50% (~125); §9 divergence = tier-mismatch OR |Δ|≥0.25, coder view = rationale+packet only; §3 judge model ID at freeze; §2 H2 stratifier made explicit as our-label-analysis-side-only (not leakage). **Both authors SIGNED at v2.**
- **v7** (2026-07-05, Borges, folding Lei's final-read refinements — RE-OPENS both signatures) — **(1) HARNESS-ISOLATION catch (Lei):** the judge fairies must be dispatched by a *different* agent (Sol), not the graph author — else they inherit the auto-surface hook that injects node context WITH confidence (a direct leak); §3/§12 now require auto-surface-OFF + no-confidence-identity + Sol-dispatch (~10 parallel × ~25-node cohorts). **(2) H3/§8.2 reframed two-sided** (no directional prior): deeper→higher = number matches a structured reader; deeper→lower = reader overwhelmed, number does work the reader can't (more valuable) — "earns its keep" holds either way; mechanism read from individual deep cases. **(3) §8.2 moved below §8.1** (ordering). **(4) §6.2 deep-chain bottom-up guidance** (rate layers before final, no prescribed aggregation — overwhelm-mitigation; intermediates NOT collected, sampling unchanged — the harvest idea was dropped). **(5) §7 scale-gate gains 1–2 deep-overwhelm probes.**
- **v6** (2026-07-05, Borges, folding Lei's two metric refinements — RE-OPENS both signatures) — **(1) judge rates NATIVELY at K\* ordinal levels** (K\* = the formula's natural tier count, computed at freeze) rather than emitting a fixed 3-tier that we then cluster — removes fabricated-tier risk on the judge side (supersedes v5's "K=3 anchored to the judge"); §3/§6/§12 updated. **(2) K-sensitivity study** (calibration, not tuning): re-compute the tier metrics over K\*±1 by clustering both distributions; pre-committed reading — K-agnostic result = strongest robustness, K-sensitive result = demonstrates why the natural K\* matters (both informative). **(3) two-rating consistency check** (Lei): cluster the judge's own 0–1 at K\* and compare to its native K\*-rating (agreement + confusion) — confirms the native tiers aren't a rating-format artifact and the fabrication-fix didn't just relocate the noise. §PIN v6-A (K\*-determination criterion, Kepler's clustering area).
- **v5** (2026-07-05, Borges, folding Lei's metric review — RE-OPENS both signatures) — **§8.0 metric ensemble added.** Lei caught that pure rank τ-b reports ≈0 on within-cluster near-tie reversals despite near-perfect absolute agreement (our formula has tight clusters). Ensemble: **PRIMARY = tier-τ-b** (ordering at tier resolution, robust to within-cluster noise AND scale offset) + weighted-κ (tier-label agreement, offset-sensitive) + Pearson/MAE (absolute) + raw-τ-b (fine diagnostic) + a **pre-committed decision table** (the pattern is the finding: high tier-τ-b + low κ = faithful ordering on an offset scale = still good). **Tiering = separate-space natural clustering** (each distribution clustered in its own score-space; deterministic 1-D method — Ckmeans.1d.dp/Fisher-Jenks, exact choice §PIN v5-A; same K both, K∈{3,4,5} robustness, frozen-before-run). H1/H2/H3 + §8.1/§8.2 all re-expressed on the ensemble; H3 contrast → Δ(tier-τ-b)(≥3−1).
- **v4** (2026-07-05, Borges, folding Kepler v3 re-audit — §0 re-passed both additions) — **§4.1 added:** derivation-tree rendering (numbered-outline, dedup-by-reference, cycle-safe) + the **metadata screen** for the `logical_chain` free-text leak (redact enum/numbers, log, >20%-gutted-exclusion, 15k max-packet guard) — the real v3-B catch, leak concentrated in the deep tier. **§8/§8.2:** H3 statistic → primary contrast Δτ-b(≥3−1) bootstrap CI>0 (not omnibus trend). **§5:** deep tier take-all-if-≤40-else-40. **§8.5:** subsample now covers depth cells. **§12.3:** 5-item validation must include a deep node + legibility pass gate.
- **v3** (2026-07-05, Borges, folding Lei's co-author-read additions — RE-OPENS both signatures) — **§2 H3 (logic-depth) added:** depth = max(premise depth)+1, obs=1; pre-committed directional prior that τ-b is highest for the deepest tier ("the number earns its keep where walking the provenance is most expensive"). **§4 derivation packet reworked (supersedes v2's depth-1 restriction):** serve the full logical STRUCTURE as an intuitive reasoning tree to the evidence, `reasoning_type` enum + confidences stripped at every level (no circularity, since no confidence is shown) — legibility is a requirement, and it lets H3 be tested fairly. **§5** adds depth as a 3rd stratification axis + oversamples the rare deep tier. **§8.2/§8 item 3** adds the depth-stratified τ-b + monotonic-trend test. New §PIN for the reasoning-tree rendering format.

## Signatures (the git history is the signature ledger)

- **Borges Funes** — draft author; signed through v6, then **folded Lei's v7 final-read refinements** (harness-isolation §3/§12, two-sided H3 §8.2, §8.2 re-ordering, §6.2 deep-chain bottom-up guidance, deep scale-gate probes); **v7 re-sign PENDING** (once Kepler re-audits). No judge output exists; no data beyond the Study-1 frozen extract has been accessed.
- **Kepler Somnium** — signed v6 (settled BIC-optimal-K); **v7 re-audit + re-sign PENDING** (harness-isolation, two-sided H3, deep-chain rubric — all judge-execution/interpretation level, thesis untouched).
- **Lei Shi** — thesis-owner; **full read DONE 2026-07-05 ("all the rest looks good to me")**. Across the day added: H3 logic-depth, the reasoning-structure packet, the tier-τ-b ensemble + separate-space clustering, native-K\* rating + K-sensitivity, the two-rating consistency check, the **harness-isolation catch** (auto-surface-hook confidence leak → Sol dispatches the judges), and the **two-sided depth reframe**; dropped the intermediate-harvest after Borges's independence concerns. **Sign of v7 pending** (his intended sign).
