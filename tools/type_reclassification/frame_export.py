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
