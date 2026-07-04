# Retrospective Calibration Check — Pre-Registration

**Authors:** Borges Funes, Kepler Somnium
**Date authored:** 2026-07-04
**Status:** PRE-REGISTRATION — authored and signed *before* any confidence value is pulled or any statistic is computed. Paper item: engram-paper #8.

> **Why this document exists.** The refuted-set definition, labeling rubric, analysis plan, metric, and negative-result commitment are all fixed *here*, before data access. Computing-then-choosing-the-method is the motivated-reasoning path this pre-registration structurally forecloses. If a design decision is not in this document, it was not pre-registered, and any post-hoc version of it must be reported as exploratory.

## 1. Purpose

Test whether ENGRAM's computed confidence has **predictive validity**: do claims later refuted carry lower confidence *before* refutation than claims that survived? This is the paper's first outcome datum — a within-graph natural experiment, computable from the existing graph, no new data collection.

## 2. Primary hypothesis (H1)

Computed confidence **at filing time discriminates** claims later refuted from claims that survived, matched on node-type and age.

### 2.1 Confidence timepoint (pinned — Kepler review, dv_0028)

Confidence can mutate after filing (support-edge fusion recomputes it), so "at filing time" (H1) and "before refutation" (§1) can differ. **Primary = filing-time computed confidence, for both classes.** Last-pre-refutation confidence is a **labeled sensitivity analysis only.** Filing-time is primary *precisely because of* the §6 scrutiny confound: a last-pre-refutation value may already carry the emerging scrutiny that *precedes* a refutation, artificially inflating discrimination. We additionally **report the fraction of nodes whose confidence changed post-filing** and the magnitude, so the filing-vs-current distinction is quantified rather than assumed.

## 3. Definitions

### 3.0 The unifying principle (pinned — v3, Lei review): the refuted set counts CLAIM-CONTENT falsity only

A retraction or supersede fires for many reasons, but only one of them tests the confidence model: **the confidence was calibrated to whether the CLAIM'S CONTENT is true, so only a claim-content falsity is a refutation of it.** A retract/supersede where the content stood but a *wrapper* was wrong — its **type** (§3.2), its **support/citation** (§3.1 bucket 1), or its **metadata/attribution** (author, venue, date) — is **excluded**, reported separately, never counted as a refutation. Counting a wrapper-error as a refutation biases the result in the worst direction: it makes the confidence model look worse than it is on a case where it was *right*. The canonical instance is the Mao-Cao case (ob_0426): a hallucinated **author** (the paper is Lee 2024) on a claim whose content was correct and stayed correct — the model put 0.95 on a true claim and was never wrong; only the attribution was. The three exclusions below are one rule applied to three wrappers.

### 3.1 Refuted set (positive class) — three buckets

1. **Retracted-as-claim-false** — split by `error_type` (pinned — Kepler review, dv_0028): `hallucinated_claim` + `fabricated_quote` are **structural** claim-false (the claim itself was wrong). `wrong_citation` / `wrong_evidence` are **NOT** automatically claim-false — a claim can lose its support while remaining *true* (a support-error), so counting them as refutations mixes classes in the flattering direction (the same failure shape as the type-error exclusion in §3.2). These two, plus `error_type=other`, go through the **blind reason-read** (§4): counted refuted iff the reason asserts the *claim itself* was false; otherwise they join a separate **support-error bucket** — reported, but not counted as refutations. **Metadata guard (v3, Lei review):** even `hallucinated_claim` / `fabricated_quote` are NOT auto-refuted when the hallucination is in a **metadata field** (author/venue/date/attribution) and the claim's content stood — a hallucinated *author* may have been filed as `hallucinated_claim` because it *was* a hallucination. So the blind read applies to the structural buckets too, for the single question "was the claim's **content** false, or only a wrapper?"; content-intact metadata-hallucinations go to the metadata-error bucket (§3.2), not the refuted set.
2. **Contradicted-and-lost** — the side of a resolved contradiction that resolution retracted/superseded. Identified **structurally** off `resolves` provenance (the retracted/superseded side of a `ct_` node). No hand judgment.
3. **Superseded-as-wrong** — `supersede` whose `supersede_reason` asserts the old claim was **incorrect at filing time** (not merely narrowed/updated). Requires **blind hand-labeling** (§4).

### 3.2 Excluded / separately bucketed
- **Type-error retracts** (claim-true, type-wrong — the cs_0046 type axis): **EXCLUDED.** The claim wasn't wrong; counting it as a refutation poisons the signal in our favor (the worst direction to be wrong in).
- **Superseded-as-refined** (correct-then, narrowed/extended/vocabulary-improved): **NOT refuted** — this is epistemic evolution. It joins the survivor class.
- **Metadata / attribution errors** (v3, Lei review — the Mao-Cao class): retract/supersede that corrected a **metadata field** (author, venue, date, citation-target) while the claim's **content** stood → **EXCLUDED**, filed in a reported **metadata-error bucket**. The claim's uncertainty was never a function of the attribution, so the confidence model was neither right nor wrong to be tested here. This is the third wrapper of the §3.0 principle (with type-error and support-error).

### 3.3 Survivor set (negative class / baseline)
All current + superseded-as-refined nodes NOT in the refuted set, **matched on node-type × age-bucket** (pinned — Kepler review): age-at-filing bucketed by **fortnight**; **all** eligible survivors in each type×age cell (**no sampling**); the AUC is computed **stratified per cell and pooled weighted by refuted-count**. (A 9-week observation and a 2-day derivation carry different priors; an unmatched baseline is itself a confound.)

## 4. Blind labeling rubric (superseded-as-wrong bucket only)

`supersede_reason` is free text (~201 supersedes), so as-wrong vs as-refined is a hand-labeling job. It must be **blind and two-standpoint**:

- **Blind:** the labeler reads the reason text with **all confidence values masked** (old and new node confidence hidden). Labeling with the numbers visible is the contamination path.
- **Rubric (v3 — classify on CLAIM CONTENT, not on "was anything wrong"):** three labels. **as-wrong** iff the reason asserts the old claim's *content* was incorrect at filing time (→ refuted). **as-refined** iff the content was *correct-then* and narrowed / extended / re-vocabularied (→ survivor). **metadata-error** iff the correction was to a *wrapper* — author, venue, date, citation-target, or node-type — while the content stood (→ excluded, §3.2 metadata-error bucket). The discriminating question is always "was the **content** false?", never "was *something* about the node wrong?" — the Mao-Cao author-fix is the worked example of the third label.
- **Two-standpoint:** Borges labels the full set; Kepler audits a random 20% (or the assignment reverses). Disagreements are adjudicated by re-reading the source node, and every adjudication is logged.

## 5. Analysis plan — two pre-committed levels

- **(a) Raw.** Does computed confidence discriminate refuted from matched-survivors? **This is the headline and the paper's actual claim.**
- **(b) Within-type.** Does confidence add discrimination *beyond* the node's reasoning/quote-type mix? Confidence is computed *from* type, so raw discrimination could reduce to "type X gets refuted more." Within-type tests whether the arithmetic adds signal beyond the type system. **This is not a confound to eliminate** — type-derived confidence predicting refutation *is* the model working — it is a second, stricter question, reported either way.

### 5.1 Metric — discrimination, not a mean comparison

Refutation is a **rare event** (most nodes are never refuted), so a mean-confidence gap can be statistically significant *and* useless — a small mean difference on a rare outcome discriminates almost nothing. The pre-registered metric is therefore a **discrimination measure**:

- **AUC** of confidence predicting refutation — **primary**.
- Full confidence **distributions** of refuted vs matched-survivors — reported.
- **Effect size** (rank-biserial / Cliff's δ), not just p.
- Reported at **both** levels: raw AUC; within-type AUC via **type-stratified** confidence (pinned primary — Kepler review — fewer modeling assumptions at our N; type-residualized is a labeled sensitivity analysis).
- **Bootstrap confidence intervals on all AUCs** (pinned — Kepler review): rare event + small refuted-N means a point estimate alone overstates what we know, in either direction.

### 5.2 Interpretation matrix (pre-committed)

| Raw AUC | Within-type AUC | Reading (printed as-is) |
|---|---|---|
| real | real | Confidence has predictive validity beyond type. Strongest positive. |
| real | collapses | "The calibration lives in the type system, not the arithmetic." A finding in its own right. |
| null | — | **NEGATIVE RESULT.** The confidence model does not predict refutation in this graph. Printed as-is. |

## 6. Confounds named regardless of outcome

- **Scrutiny-selection.** Refuted claims may sit lower not because the model is calibrated but because low-confidence claims get *more scrutiny* — a 0.4 is revisited more than a 0.9, so it is likelier to be caught and refuted. That is selection-by-attention, not predictive validity. The retrospective design **cannot fully separate the two**; doing so requires a **pre-registered forward test** (proposed as the paper's next experiment). This limitation is stated wherever the result is reported.
- **Single-graph (N=1).** One graph (Borges's, 9 weeks). Generalization requires replication on other graphs (Kepler's, Ariadne's, …).

## 7. Negative-result commitment (verbatim)

> "The honesty spine has to survive its own first datum, or it was decoration."

If refuted claims did **not** sit lower (raw AUC null), that is the result, and it goes in the paper as-is.

## 8. Execution order (nothing before step 1 is signed)

1. Both authors sign this pre-registration; Lei (co-author) reads it. **No confidence value is accessed before this step.**
2. Borges pulls the three refuted buckets (structural for 1 + 2; blind-labeled for 3) + the matched survivor baseline.
3. Blind-label the superseded-as-wrong set; Kepler audits 20%.
4. Compute AUC + distributions + effect size, raw + within-type.
5. Report per the §5.2 interpretation matrix, with the §6 confounds stated.

## Review history

- **v1** (2026-07-04, Borges) — initial pre-registration.
- **v2** (2026-07-04, post-Kepler-review, dv_0028) — four researcher-degree-of-freedom pins closed: (1) confidence timepoint = filing-time primary + post-filing mutation-rate reported (§2.1); (2) bucket-1 split — support-errors (`wrong_citation`/`wrong_evidence`) blind-read, not auto-refuted (§3.1); (3) matching pinned to fortnight age-buckets, no sampling, refuted-weighted stratified AUC (§3.3); (4) within-type = type-stratified primary + bootstrap CIs on all AUCs (§5.1).
- **v3** (2026-07-04, post-Lei-review) — the **Mao-Cao concern**: a hallucinated *author* (metadata) on a content-true claim must not count as a refutation of the *confidence* model. Added the §3.0 unifying principle (**refuted = claim-CONTENT falsity only**), a **metadata-error exclusion** as the third wrapper alongside type-error and support-error (§3.2), a metadata guard on the structural bucket (§3.1), and a third **metadata-error** label in the blind rubric (§4). Re-opens signatures.

## Signatures (the git history is the signature ledger)

- **Borges Funes** — author + v2 pins + v3 (Mao-Cao / claim-content-falsity), 2026-07-04. Signed before any data access.
- **Kepler Somnium** — signed v2 (approve on PR #13); **v3 re-sign pending** (the metadata-error exclusion is a negative-class change).
- **Lei Shi** — signed 2026-07-04 ("SIGNED — Lei Shi"), raising the Mao-Cao concern that v3 resolves; re-read of v3 pending.
