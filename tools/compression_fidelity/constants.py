"""Confidence-model constants, vendored from engram-alpha.

This package lives in a SEPARATE repo (engram-paper) from the ENGRAM schema
source of truth (engram-alpha `src/engram/engram_confidence.py`). Rather than
add a cross-repo import dependency (fragile — engram-alpha may not be checked
out next to engram-paper on every machine that runs this tool, e.g. Borges's
or Sol's), the handful of constants this package needs are copied here
verbatim, pinned to a specific engram-alpha commit for traceability.

Vendored from:
    engram-agents/engram-alpha, commit be55e8196ace2748b6e855ae876aaf9026431b93
    (2026-07-04), file src/engram/engram_confidence.py

If engram-alpha's confidence model changes, this file must be re-synced by
hand — there is no automated drift check. A future improvement could vendor
via a pinned git submodule or a published package instead.
"""

from __future__ import annotations

# ── Observation confidence: quote_type -> base confidence ──────────────────
# (Also the "confidence-bin" stratification axis for observations — §5.)

CONFIDENCE_MAP: dict[str, float] = {
    "hard_data": 0.95,
    "official_statement": 0.85,
    "attributed_analysis": 0.70,
    "counterfactual_inference": 0.65,
    "unnamed_source": 0.50,
    "personal_communication": 0.40,
    "editorial": 0.35,
}

VALID_QUOTE_TYPES = set(CONFIDENCE_MAP.keys())

# The 6 "natural bin edge" anchors named explicitly in the pre-reg §5
# ("observations: ~= 0.95 / 0.85 / 0.70 / 0.40-0.35 ... using the
# confidence-anchor values as natural bin edges") and in the coder-fairy
# spec ("0.95 / 0.85 / 0.70 / 0.50 / 0.40 / 0.35"). counterfactual_inference
# (0.65) is a real CONFIDENCE_MAP entry but is not one of the 6 named
# anchors — it bins to its nearest anchor (0.70) like any other computed
# value that doesn't land exactly on an anchor (e.g. after the introspective
# discount or a rounding artifact).
OBSERVATION_CONFIDENCE_ANCHORS: tuple[float, ...] = (0.95, 0.85, 0.70, 0.50, 0.40, 0.35)

# ── Source-class adjustments (affect the COMPUTED confidence value that
#    observation binning sees, but are never disclosed to the judge) ──────

SOURCE_CLASS_CONFIDENCE_DISCOUNT: dict[str, float | None] = {
    "external": 1.0,
    "introspective": 0.95,
    "user_stated": None,  # override: treated as official_statement regardless of quote_type
}

PREDICTIVE_CONFIDENCE_CAP = 0.60
CONJECTURE_CONFIDENCE_DEFAULT = 0.40
CONJECTURE_CONFIDENCE_MIN = 0.10
CONJECTURE_CONFIDENCE_MAX = 0.60

# ── Reasoning types for derivations (the derivation "confidence-bin" axis
#    — derivations bin by reasoning_type directly, per §5: "which IS their
#    confidence map, don't also bin derivations by raw score") ────────────

REASONING_TYPES: set[str] = {
    "deductive_modus_ponens",
    "deductive_modus_tollens",
    "deductive_hypothetical_syllogism",
    "deductive_disjunctive",
    "deductive_reductio",
    "inductive_generalization",
    "inductive_enumeration",
    "inductive_statistical",
    "inductive_analogy",
    "inductive_causal",
    "abductive_best_explanation",
    "abductive_elimination",
    "authority_expert",
    "authority_consensus",
}

REASONING_CLASS: dict[str, str] = {
    "deductive_modus_ponens": "deductive",
    "deductive_modus_tollens": "deductive",
    "deductive_hypothetical_syllogism": "deductive",
    "deductive_disjunctive": "deductive",
    "deductive_reductio": "deductive",
    "inductive_generalization": "inductive_corroboration",
    "inductive_enumeration": "inductive_corroboration",
    "inductive_statistical": "inductive_chain",
    "inductive_analogy": "inductive_chain",
    "inductive_causal": "inductive_chain",
    "abductive_best_explanation": "abductive",
    "abductive_elimination": "abductive",
    "authority_expert": "authority",
    "authority_consensus": "inductive_corroboration",
}

REASONING_DISCOUNT: dict[str, float] = {
    "deductive_modus_ponens": 0.98,
    "deductive_modus_tollens": 0.98,
    "deductive_hypothetical_syllogism": 0.98,
    "deductive_disjunctive": 0.98,
    "deductive_reductio": 0.98,
    "inductive_generalization": 0.95,
    "inductive_enumeration": 0.93,
    "inductive_statistical": 0.90,
    "inductive_analogy": 0.70,
    "inductive_causal": 0.85,
    "abductive_best_explanation": 0.80,
    "abductive_elimination": 0.88,
    "authority_expert": 0.95,
    "authority_consensus": 0.98,
}

ABDUCTIVE_CONFIDENCE_CAP: dict[str, float] = {
    "abductive_best_explanation": 0.80,
    "abductive_elimination": 0.90,
}

# ── ENGRAM node types (VALID_NODE_TYPES / CLAIM_BEARING_TYPES, same source) ─

OBSERVATION_TYPES: set[str] = {"observation_factual", "observation_predictive"}
DERIVATION_TYPES: set[str] = {"derivation"}
# Frame per pre-reg §5: observations + derivations ONLY. `theory` is a
# legacy/rarely-used alternate derivation-like type in engram_core.py (a
# handful of code paths treat `type IN ('derivation', 'theory')` the same
# way) but the pre-reg's frame text and the coder-fairy spec both say
# "observations + derivations" without mentioning `theory`, and it does not
# appear in any live install observed (VALID_NODE_TYPES includes it, but
# it's absent from CONFIDENCE_MAP/REASONING_CLASS usage and from the smoke
# DB). Excluded from the frame — flagged as a judgment call in the handoff.
CLAIM_BEARING_TYPES: set[str] = {
    "observation_factual",
    "observation_predictive",
    "derivation",
    "theory",
    "axiom",
    "conjecture",
    "lesson",
}

# ── ENGRAM node-ID prefix vocabulary (reviewer-fairy catch, post-handoff-1) ──
#
# Vendored from engram-alpha `src/engram/engram_core.py` (same commit as the
# other constants above), the `type -> id-prefix` map used by `_next_id()`.
# ENGRAM's own authoring convention cites node IDs inline in prose
# ("ob_0004 records that...") — a bare node-ID citation directly reveals
# that cited node's TYPE (a `quote_type`-adjacent leak: "ob_0004" tells the
# judge the cited premise is an observation, "ax_0004" that it's an axiom,
# etc.), so these prefixes must be redacted from free text exactly like the
# quote_type/reasoning_type vocabulary (redact.py).
NODE_ID_PREFIXES: tuple[str, ...] = (
    "ev",  # evidence
    "ob",  # observation_factual / observation_predictive
    "pr",  # prediction
    "dv",  # derivation
    "th",  # theory
    "ct",  # contradiction
    "qu",  # question
    "ax",  # axiom
    "df",  # definition
    "cj",  # conjecture
    "gl",  # goal
    "gt",  # goal_tension
    "fl",  # feeling_report
    "tk",  # task
    "ls",  # lesson
    "pn",  # person
    "cs",  # cornerstone
    "ts",  # trust_signal
)
