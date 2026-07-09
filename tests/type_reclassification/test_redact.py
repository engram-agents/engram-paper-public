"""Tests for tools/type_reclassification/redact.py: the outcome-vocabulary
+ author-id passes layered on top of compression_fidelity.redact's existing
confidence/quote_type/reasoning_type/node-id screen.
"""

from __future__ import annotations

from tools.compression_fidelity.redact import REDACTED_TOKEN
from tools.type_reclassification import redact


def test_outcome_vocab_redacted():
    text = "The node was later retracted; the contradiction was resolved."
    out, hits = redact.screen_text(text, "ob_0001", "claim")
    assert "retracted" not in out
    assert "contradiction" not in out
    assert "resolved" not in out
    categories = {h.category for h in hits}
    assert "outcome_vocab" in categories


def test_outcome_vocab_variants_all_scrubbed():
    text = (
        "supersedes, superseded, refuted, refutation, unresolved, "
        "partially resolved, partially_resolved, contradicts"
    )
    out, hits = redact.screen_text(text, "ob_0002", "claim")
    for word in (
        "supersedes", "superseded", "refuted", "refutation", "unresolved",
        "partially resolved", "partially_resolved", "contradicts",
    ):
        assert word not in out
    assert any(h.category == "outcome_vocab" for h in hits)


def test_outcome_vocab_gerund_and_base_forms_scrubbed():
    """Regression test for a reviewer-fairy-caught leak: the prior word list
    covered each family's surface forms inconsistently -- every gerund
    (resolving/superseding/contradicting/retracting/refuting) and the bare
    base forms of "resolve"/"contradict" leaked entirely, verified by
    direct regex probing (not just doc-reading) against exactly these
    sentences. This test is deliberately NOT limited to words already
    hardcoded in _OUTCOME_WORDS (the prior test's failure mode: it can only
    catch what it already enumerates) -- these are natural-sounding
    sentences an agent's claim/quoted_text might plausibly contain, chosen
    to probe forms outside the original list."""
    probes = (
        "The team is resolving the dispute now.",
        "This is superseding an earlier draft.",
        "The panel is contradicting itself here.",
        "We are retracting this claim informally.",
        "The finding refutes the earlier hypothesis directly.",
        "A resolve step closes the dispute.",
        "This claim does not contradict anything else.",
    )
    for i, text in enumerate(probes):
        out, hits = redact.screen_text(text, f"ob_probe_{i}", "claim")
        assert REDACTED_TOKEN in out, (
            f"leak: {text!r} was not redacted at all -> {out!r}"
        )
        categories = {h.category for h in hits}
        assert "outcome_vocab" in categories, (
            f"leak: {text!r} redacted something, but not via outcome_vocab -> {hits!r}"
        )


def test_author_id_pn_form_redacted():
    text = "Filed by pn_0002 during the session."
    out, hits = redact.screen_text(text, "ob_0003", "claim")
    assert "pn_0002" not in out
    assert any(h.category == "author_id" for h in hits)


def test_author_id_namespaced_form_redacted():
    text = "The author (orcid:0000-0002-1825-0097) wrote this."
    out, hits = redact.screen_text(text, "ob_0004", "claim")
    assert "orcid:0000-0002-1825-0097" not in out
    assert any(h.category == "author_id" for h in hits)


def test_field_name_mention_redacted():
    """Discovered gap (see redact.py module docstring): the base
    compression_fidelity screen catches quote_type/reasoning_type ENUM
    VALUES but not the literal FIELD-NAME WORDS themselves."""
    text = "This overrides the quote_type proxy and the reasoning_type default."
    out, hits = redact.screen_text(text, "ob_0009", "claim")
    assert "quote_type" not in out
    assert "reasoning_type" not in out
    assert any(h.category == "field_name_mention" for h in hits)


def test_base_confidence_and_quote_type_screen_still_applies():
    """Confirm the underlying compression_fidelity screen (confidence
    numbers + quote_type/reasoning_type vocabulary) is not bypassed by
    this module's wrapper."""
    text = "conf 0.95 -- this is hard_data evidence, cited as ob_0004."
    out, hits = redact.screen_text(text, "ob_0005", "claim")
    assert "0.95" not in out
    assert "hard_data" not in out
    assert "ob_0004" not in out
    categories = {h.category for h in hits}
    assert "conf_number" in categories
    assert "vocab" in categories
    assert "node_id_citation" in categories


def test_no_hits_returns_original_text_unchanged():
    text = "A perfectly ordinary claim about the world."
    out, hits = redact.screen_text(text, "ob_0006", "claim")
    assert out == text
    assert hits == []


def test_empty_text_short_circuits():
    out, hits = redact.screen_text("", "ob_0007", "claim")
    assert out == ""
    assert hits == []


def test_combined_pass_merges_overlapping_spans_correctly():
    """A hit from the base screen adjacent to a hit from this module's new
    passes must merge into a single non-overlapping redaction, not corrupt
    the surrounding text."""
    text = "conf 0.95 and the claim was later retracted (pn_0002)."
    out, hits = redact.screen_text(text, "ob_0008", "claim")
    assert "0.95" not in out
    assert "retracted" not in out
    assert "pn_0002" not in out
    assert out.count(REDACTED_TOKEN) >= 2
    # Text on either side of the redactions must survive intact.
    assert out.startswith(REDACTED_TOKEN)
    assert out.endswith(".")
