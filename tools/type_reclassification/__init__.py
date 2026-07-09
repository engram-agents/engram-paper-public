"""type_reclassification — Track-(b) dual-axis type re-classification
harness. Implements BOTH arms: the OBSERVATION ARM (pre-reg §2's
`quote_type` re-classification) and, as of 2026-07-08 following Aleph's
reasoning-arm review + Kepler's countersign on the pre-reg, the
DERIVATION ARM (pre-reg §2's `reasoning_type` re-classification).

Pre-registration (the contract of record for this package):
    engram-paper `paper_research/type-reclassification-preregistration-2026-07-08.md`
    (draft 7 as of the derivation arm's build — draft 1 (Borges) encoded
    dv_1083's normative reframe, ob_2805's multi-graph power requirement,
    Kepler's three riders, and the third blind outcome-labeler pass (DM
    seq 1395/1398); drafts 2-6 folded Aleph's reasoning-arm review, the §4
    pre-freeze re-measurement, and Kepler's OR-estimand fix; draft 7 folds
    the derivation-arm's confidence-redaction blinding refinement below).

Reuses the compression-fidelity blinding/isolation harness (PR #18,
`tools/compression_fidelity/`) for its confidence/quote_type/reasoning_type/
node-id redaction mechanism — see `redact.py`'s module docstring for the
import-reuse rationale — but is judge-task-agnostic where that package was
confidence-rating-specific: everything type-reclassification-specific
(the normative judge prompts, raw-API dispatch, Fleiss-kappa panel, the
outcome-labeler, the OR-estimand analysis) lives in this package's own
modules.

**Observation arm** (`quote_type`): `db.py`'s `fetch_frame`/
`classify_outcome`, `frame_export.export_frame`, `judge_prompt.py`,
`dispatch.py`, `interrater.py`, `outcome_prompt.py`/`outcome_dispatch.py`,
`type_definitions.py`.

**Derivation arm** (`reasoning_type`), built as a genuine parallel track
rather than a retrofit — the observation arm's modules were deliberately
kept general enough (see the original design note, preserved below) that
none of them needed a rewrite:
  - `derivation_type_definitions.py` — REASONING_TYPES enum +
    schema text. Departs from `type_definitions.py`'s "reproduce verbatim"
    rule in one deliberate, documented way: the real reasoning_type
    docstring is confidence-saturated (inline discount/cap numbers and
    hierarchy words), unlike quote_type's clean bare-enum, so this module
    hand-redacts the confidence-derivation framing while preserving every
    inference-form semantic requirement — see its own module docstring
    for the full keep/drop reasoning (worked out live with Borges/Aleph,
    DM seq 1502/1505/1506, folded into pre-reg draft 7).
  - `db.py`'s `fetch_derivation_frame` / `fetch_derivation_premises` /
    `find_type_correction_partner` / `classify_derivation_outcome` /
    `mine_m5_reconstruction_pool` — the derivation-arm frame fetch, the
    §5 M5 positive-control mining (both structural forms of a
    type-correction: formal supersede, and retract(error_type=other)+
    refile), and the draft-3 circularity fix (`"excluded_type"` outcome
    category, kept out of both the main judge frame and the refuted/
    unclassified population).
  - `frame_export.export_derivation_frame` — the reasoning_type dose
    ({id, claim, premises: [{claim, type}], stratum}), excluding BOTH
    `"excluded"` and `"excluded_type"` outcomes from the main frame.
  - `derivation_judge_prompt.py` / `derivation_dispatch.py` — the
    reasoning_type judge prompt + its own response-parsing (reuses
    `dispatch.py`'s transport layer — `PanelMember`/`JudgeClient`/
    `DispatchError`/`scope_a_panel`/`scope_b_panel` — unchanged, exactly
    as this module's original design note below anticipated).
  - `analysis.py` — M1 (divergence rate + confusion matrix), M2 (odds
    ratio of refutation, divergent vs concordant, +CI — Kepler's
    draft-6 fix: the estimand is the OR, not the marginal rate, since
    pre-reg §4 uses outcome-stratified/case-control sampling), M4
    (per-graph + pooled fixed/random-effects ORs), M5 (recovery rate vs
    chance, the positive-control instrument check). M0 (the Fleiss-kappa
    instrument-validity gate) is NOT reimplemented — `interrater.py`'s
    existing `fleiss_kappa`/`instrument_validity_gate` were already
    generic and apply to the derivation panel's results unchanged.

**Original design note (why the observation-arm modules never needed a
rewrite to add the derivation arm above)**, preserved for the historical
record of that design decision:
  - `db.py`'s `NodeRow` / `fetch_frame` / `classify_outcome` /
    `resolve_fs_class` are all written against the general `nodes`/`edges`
    schema, not an observation-only shape — the observation-type scoping is
    a single `WHERE type IN (...)` filter (currently
    `OBSERVATION_TYPES`), swappable to `DERIVATION_TYPES` or a union.
  - `redact.py`'s screen is type-system-agnostic (works on `claim`/
    `quoted_text` free text regardless of node type).
  - `frame_export.py`'s `export_frame` shape mirrors the pre-reg §2 dose
    structure generically ({id, claim, evidence, stratum}); only the
    `evidence` dict's field set (`quoted_text`/`source_class`/
    `source_domain`/`source_date`) is observation-arm-specific per the
    pre-reg's dose definition — the derivation-arm export swaps in the
    derivation dose (premise claims + types) without touching the outer
    shape, exactly as anticipated.
  - `judge_prompt.py` / `dispatch.py` / `interrater.py` (the type-judge
    pipeline) and `outcome_prompt.py` / `outcome_dispatch.py` (the blind
    outcome-labeler) are dose-agnostic at the prompt-construction layer;
    the derivation-arm judge got its own prompt module (reasoning_type
    vocabulary, premise-structure dose) but reuses `dispatch.py`'s
    transport (`JudgeClient`/`PanelMember`/`DispatchError`) unchanged.
"""
