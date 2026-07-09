"""frame_export.py — pre-reg §2 observation-arm judge-facing frame builder
(the "dv_1081" shape).

Produces the exact frame the pre-reg registers for the observation arm:

    {"id": ..., "claim": <redacted>, "evidence": {"quoted_text": <redacted>,
     "source_class": ..., "source_domain": ..., "source_date": ...},
     "stratum": {"outcome": ..., "fs_class": ...}}

— a FLAT structure, no nested confidence/type/outcome keys anywhere (the
ABSENCE of the key is the safety property per the task spec, not a null
placeholder someone could forget to check).

**WITHHELD, must never appear anywhere in the exported dict** (pre-reg §2):
`quote_type` (the node's own filed type — the answer key), `confidence`
(any numeric value or `confidence_history`), the node's own
`interpretation` field (the "framing leak"), `standpoint_author_id` (the
filing agent's identity). See
`tests/type_reclassification/test_frame_export.py`'s withholding test —
the load-bearing safety test for this whole module.

**Note on `stratum.outcome` NOT being a withholding violation.** Pre-reg
§2's withholding list governs the DOSE shown to the blinded JUDGE.
`stratum` is frozen-frame ANALYSIS metadata — this harness's own
outcome-classification result, carried alongside the frame for the
RESEARCHER's stratified sampling (pre-reg §4/§5) — not part of the judge's
dose (`evidence`). This module's scope ends at producing the frame; whoever
builds the judge-dispatch step (explicitly out of THIS package's scope, per
the task spec's "What NOT to do") must serve only `id`+`claim`+`evidence` to
the judge and must NOT forward `stratum` — flagged here so that boundary is
explicit for whoever builds the dispatch step next.
"""

from __future__ import annotations

from .db import NodeRow, resolve_fs_class
from .redact import screen_text


def export_frame(rows: list[NodeRow]) -> list[dict]:
    """Build the pre-reg §2 observation-arm frame from already-classified
    `NodeRow`s.

    **Precondition: `row.outcome` must already be set** (via `fetch_frame` /
    `fetch_frame_multi`, or set manually on a hand-built test fixture) —
    this function takes no `conn` and cannot compute `classify_outcome`
    itself. A row with `outcome is None` raises `ValueError` rather than
    silently defaulting to any stratum (silently guessing an outcome is
    exactly the failure mode this package's design is trying to avoid).

    Excludes any row whose outcome is `"excluded"` (pre-reg §4 EXCLUDE list
    — `duplicate` / `wrong_citation` retractions never enter the judge
    corpus at all). Rows with outcome `"unclassified"` (superseded-but-not-
    retracted, or a structurally-ambiguous contradiction loss) ARE included,
    tagged as such — they must never silently collapse into `"refuted"` or
    `"survived"`.
    """
    out: list[dict] = []
    for row in rows:
        if row.outcome is None:
            raise ValueError(
                f"NodeRow {row.id!r} has no outcome set -- export_frame requires "
                "classify_outcome() to have already run (via fetch_frame / "
                "fetch_frame_multi, or set manually on a test fixture). "
                "export_frame takes no `conn` and cannot compute it itself."
            )
        if row.outcome == "excluded":
            continue

        redacted_claim, _ = screen_text(row.claim or "", row.id, "claim")
        redacted_quote, _ = screen_text(row.quoted_text or "", row.id, "quoted_text")

        out.append({
            "id": row.id,
            "claim": redacted_claim,
            "evidence": {
                "quoted_text": redacted_quote,
                "source_class": row.source_class,
                "source_domain": row.source_domain,
                "source_date": row.source_date,
            },
            "stratum": {
                "outcome": row.outcome,
                "fs_class": resolve_fs_class(row),
            },
        })
    return out


def export_derivation_frame(rows: list[NodeRow]) -> list[dict]:
    """Build the pre-reg §2 derivation-arm frame from already-classified
    `NodeRow`s (mirrors `export_frame`'s structure/docstring discipline
    exactly, for the reasoning_type dose instead of quote_type's).

    **Precondition: `row.outcome` must already be set** (via
    `fetch_derivation_frame` / `fetch_derivation_frame_multi`, or set
    manually on a hand-built test fixture) — this function takes no `conn`
    and cannot compute `classify_derivation_outcome` itself. A row with
    `outcome is None` raises `ValueError` rather than silently defaulting to
    any stratum (silently guessing an outcome is exactly the failure mode
    this package's design is trying to avoid).

    Excludes any row whose outcome is `"excluded"` OR `"excluded_type"`
    (pre-reg §4 EXCLUDE list, plus the derivation-arm's own circularity fix
    — see `db.py`'s `classify_derivation_outcome` and
    `mine_m5_reconstruction_pool` docstrings). `"excluded_type"` rows are a
    TYPE-CORRECTION case (a retracted/superseded derivation whose
    correction changed its reasoning_type) and go through the SEPARATE M5
    reconstruction path (`mine_m5_reconstruction_pool`), never the normal
    judge frame — letting one leak into this frame would hand the judge a
    case whose ground truth is the study's own predictor (type
    mis-selection), contaminating the measurement the same way `"excluded"`
    duplicate/wrong_citation rows would contaminate the observation arm.
    Rows with outcome `"unclassified"` (superseded-but-not-a-type-
    correction, or a structurally-ambiguous contradiction loss) ARE
    included, tagged as such — they must never silently collapse into
    `"refuted"` or `"survived"`.

    **WITHHELD, must never appear anywhere in the exported dict** (pre-reg
    §2): `reasoning_type` (the node's own filed answer — the answer key),
    `confidence` (any numeric value or `confidence_history`), the node's
    own `interpretation` field (the "framing leak"), `standpoint_author_id`
    (the filing agent's identity). These are all excluded by construction —
    this function only ever copies `id`/`claim`/`premises`/`stratum`
    fields off each row — but see
    `tests/type_reclassification/test_frame_export.py`'s withholding test
    for the derivation arm, the load-bearing safety test for this function.
    A premise's own `type` field IS visible dose (per the pre-reg — the
    premise's established type is part of the visible premise->conclusion
    structure the judge is shown), but its `claim` text is still redaction-
    screened for the same free-text-leak reasons `quoted_text` is redacted
    above.
    """
    out: list[dict] = []
    for row in rows:
        if row.outcome is None:
            raise ValueError(
                f"NodeRow {row.id!r} has no outcome set -- export_derivation_frame "
                "requires classify_derivation_outcome() to have already run (via "
                "fetch_derivation_frame / fetch_derivation_frame_multi, or set "
                "manually on a test fixture). export_derivation_frame takes no "
                "`conn` and cannot compute it itself."
            )
        if row.outcome in ("excluded", "excluded_type"):
            continue

        redacted_claim, _ = screen_text(row.claim or "", row.id, "claim")
        redacted_premises = []
        for premise in row.premises:
            redacted_premise_claim, _ = screen_text(premise.get("claim") or "", row.id, "premise_claim")
            redacted_premises.append({"claim": redacted_premise_claim, "type": premise.get("type")})

        out.append({
            "id": row.id,
            "claim": redacted_claim,
            "premises": redacted_premises,
            "stratum": {
                "outcome": row.outcome,
                "fs_class": resolve_fs_class(row),
            },
        })
    return out


def export_m5_frame(pool: list[dict]) -> list[dict]:
    """Build the pre-reg §5 M5 positive-control frame from
    `db.mine_m5_reconstruction_pool`'s output.

    Added per Borges's PR #23 colleague-review suggestion: M5's withholding
    was previously a caller-CONTRACT stated only in
    `mine_m5_reconstruction_pool`'s docstring ("callers building the actual
    M5 dispatch packets must run this pool through the same withholding
    path") -- exactly the kind of gap that gets forgotten once a later PR
    (the dispatch wiring) actually calls it. This function makes the
    withholding CODE-ENFORCED and TESTED, mirroring `export_frame`/
    `export_derivation_frame` exactly, instead of leaving it as a
    docstring-only promise.

    Input shape (per pool item): `{"pre_correction_packet": {"id", "claim",
    "premises"}, "ground_truth_type": <str>}`.

    Output shape (per item): `{"id", "claim": <redacted>, "premises":
    [{"claim": <redacted>, "type": ...}, ...], "ground_truth_type": <str>}`.

    **`ground_truth_type` is researcher-only scoring metadata, NEVER part of
    the judge's dose** -- mirrors `stratum`'s exact role in `export_frame`/
    `export_derivation_frame` (see those docstrings' "NOT a withholding
    violation" notes): it rides alongside the frame item for the
    RESEARCHER's own M5 recovery-rate scoring (`analysis.recovery_rate_vs_chance`),
    but whoever dispatches M5 items to the judge (`derivation_dispatch.py`'s
    `dispatch_derivation_one`, reused unchanged for M5 -- it only ever reads
    `id`/`claim`/`premises` off a frame_item, per `derivation_judge_prompt.
    build_prompt`'s own docstring) must pass only `id`/`claim`/`premises`
    to `build_prompt`, never the whole dict with `ground_truth_type`
    attached. Same caller discipline as `stratum`, now at least given a
    withholding-tested `claim`/premise-`claim` redaction pass rather than
    relying on the caller to redact it themselves from scratch.

    `id` withholding note: unlike `export_frame`/`export_derivation_frame`
    (whose `id` is a live graph node id, already excluded from `build_prompt`'s
    rendered text but otherwise unremarkable), an M5 item's `id` is the
    RETRACTED/SUPERSEDED node's own id -- confirming that's fine to carry
    here (same as the other two frames; `build_prompt` never renders `id`
    into prompt text either way).
    """
    out: list[dict] = []
    for item in pool:
        packet = item["pre_correction_packet"]
        redacted_claim, _ = screen_text(packet.get("claim") or "", packet.get("id", ""), "claim")
        redacted_premises = []
        for premise in packet.get("premises", []):
            redacted_premise_claim, _ = screen_text(
                premise.get("claim") or "", packet.get("id", ""), "premise_claim"
            )
            redacted_premises.append({"claim": redacted_premise_claim, "type": premise.get("type")})

        out.append({
            "id": packet.get("id"),
            "claim": redacted_claim,
            "premises": redacted_premises,
            "ground_truth_type": item["ground_truth_type"],
        })
    return out
