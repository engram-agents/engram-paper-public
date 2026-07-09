"""type_reclassification — Track-(b) dual-axis type re-classification
harness. Currently implements the OBSERVATION ARM only (pre-reg §2's
`quote_type` re-classification arm).

Pre-registration (the contract of record for this package):
    engram-paper `paper_research/type-reclassification-preregistration-2026-07-08.md`
    (draft 1, Borges, 2026-07-08 — encodes dv_1083's normative reframe,
    ob_2805's multi-graph power requirement, Kepler's three riders, and the
    third blind outcome-labeler pass, DM seq 1395/1398).

Reuses the compression-fidelity blinding/isolation harness (PR #18,
`tools/compression_fidelity/`) for its confidence/quote_type/reasoning_type/
node-id redaction mechanism — see `redact.py`'s module docstring for the
import-reuse rationale — but is judge-task-agnostic where that package was
confidence-rating-specific: everything type-reclassification-specific
(the normative judge prompt, raw-API dispatch, Fleiss-kappa panel, the
outcome-labeler) lives in this package's own modules.

**Scope: observation arm (quote_type) only.** The pre-reg's derivation arm
(reasoning_type re-classification) is explicitly on hold pending a separate
reviewer's (Aleph's) sign-off — nothing in this package implements it. Care
was taken not to hardcode "observation" so deeply that adding the derivation
arm later requires a rewrite:
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
    pre-reg's dose definition — a derivation-arm export would swap in the
    derivation dose (premise claims + types) without touching the outer
    shape.
  - `judge_prompt.py` / `dispatch.py` / `interrater.py` (the type-judge
    pipeline) and `outcome_prompt.py` / `outcome_dispatch.py` (the blind
    outcome-labeler) are dose-agnostic at the prompt-construction layer;
    a derivation-arm judge would need its own prompt module (reasoning_type
    vocabulary, premise-structure dose) but reuses `dispatch.py`'s
    transport (`JudgeClient`/`PanelMember`/`DispatchError`) unchanged.
"""
