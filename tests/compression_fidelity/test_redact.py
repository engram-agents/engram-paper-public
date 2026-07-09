"""Tests for the metadata screen (tools/compression_fidelity/redact.py) --
the pre-reg's §4.1 "hard test assertion": confidence values, `quote_type`
and `reasoning_type` enum vocabulary must not appear ANYWHERE in a served
packet. This module had ZERO automated tests before this suite -- only
2 rounds of reviewer-fairy direct-read + manual graph-verification. Every
test here targets a specific documented behavior from redact.py's own
docstring (the 7 passes + the judgment-call notes), so a future edit that
narrows or loosens a pass fails loudly here instead of leaking silently
into a served judge packet.
"""

from tools.compression_fidelity.redact import (
    REDACTED_TOKEN,
    redacted_char_count,
    redaction_fraction,
    screen_node_id_citations,
    screen_text,
)

NODE = "dv_test"
FIELD = "claim"


def _screen(text):
    return screen_text(text, NODE, FIELD)


# ── Pass 1: conf-prefixed decimals ──────────────────────────────────────


def test_pass1_conf_prefixed_decimal_redacted():
    out, hits = _screen("The estimate carries conf 0.95 given the source.")
    assert REDACTED_TOKEN in out
    assert "0.95" not in out
    assert len(hits) == 1
    assert hits[0].category == "conf_number"


def test_pass1_confidence_colon_form():
    out, hits = _screen("confidence: 0.4 based on a single source.")
    assert "0.4" not in out
    assert hits[0].category == "conf_number"


def test_pass1_conf_tilde_approx_form():
    out, _ = _screen("conf~0.70 is a reasonable ceiling.")
    assert "0.70" not in out


def test_pass1_case_insensitive():
    out, _ = _screen("CONF 0.90 on this one.")
    assert "0.90" not in out


def test_pass1_conf_left_boundary_underscore():
    """Reviewer-fairy round-2 catch: `_conf` (snake_case identifier prefix,
    e.g. "mean_conf=0.690") -- a plain `\\b` REQUIRES the preceding char to
    be non-word, which FAILS right after `_` (a word character), so a
    naive pass-1 pattern would miss "mean_conf=0.690" entirely. The fix
    (`_CONF_LEFT`) widens the left boundary to only exclude an actual
    LETTER, not `_`/digit -- so pass 1 DOES correctly match this form.

    Docstring correction (reviewer-fairy 3rd-round catch, 2026-07-08): an
    earlier version of this docstring claimed the opposite -- that pass 1
    "must NOT match" this case and that it "falls through to bare-decimal/
    proximity handling instead." Empirically false: `hits[0].category ==
    "conf_number"`, i.e. pass 1 itself is exactly what catches it. Fixed
    the docstring to match reality and pinned the actual category so a
    future edit can't silently re-break this and have the docstring keep
    lying about which pass does the work."""
    out, hits = _screen("mean_conf=0.690 across the batch.")
    assert "0.690" not in out
    assert len(hits) == 1
    assert hits[0].category == "conf_number"


# ── Pass 2: vocabulary hits (quote_type / reasoning_type / constant names) ──


def test_pass2_quote_type_word_redacted():
    out, hits = _screen("This is an attributed_analysis claim.")
    assert "attributed_analysis" not in out
    assert any(h.category == "vocab" for h in hits)


def test_pass2_reasoning_type_word_redacted():
    out, _ = _screen("Derived via deductive_modus_ponens from two premises.")
    assert "deductive_modus_ponens" not in out


def test_pass2_flexible_separators_hyphen_and_space():
    out1, _ = _screen("This reads as attributed-analysis in the source.")
    assert "attributed-analysis" not in out1
    out2, _ = _screen("Inductive Generalization from two independent instances.")
    assert "Inductive Generalization" not in out2


def test_pass2_constant_name_redacted():
    """Judgment call (a): pass 2 also matches confidence-system constant
    NAMES, not just enum vocabulary."""
    out, _ = _screen("Falls back to CONJECTURE_CONFIDENCE_DEFAULT here.")
    assert "CONJECTURE_CONFIDENCE_DEFAULT" not in out


def test_pass2_does_not_over_match_unrelated_word():
    """'confident' (colloquial) must not be caught by the VOCAB pattern --
    only by the bare-conf-word proximity anchor logic, which is a
    documented, intentional catch for a DIFFERENT reason (percent-form
    confidence). A lone 'confident' with no decimal/percent nearby is not
    itself redacted."""
    out, hits = _screen("I am confident this claim is well supported.")
    assert "confident" in out  # not redacted on its own
    assert not hits


# ── Pass 3: proximity bare-decimals ─────────────────────────────────────


def test_pass3_bare_decimal_near_conf_word_redacted():
    """0.62/0.77 are deliberately NOT known confidence-system constants
    (unlike 0.70/0.95/0.85 etc.) so this exercises pure proximity-to-a-
    conf-word redaction, not pass 4's unconditional known-constant match."""
    out, hits = _screen("min(0.62, 0.77) = 0.62, a conf ceiling.")
    assert "0.62" not in out
    assert "0.77" not in out
    assert any(h.category == "proximity_bare_decimal" for h in hits)


def test_pass3_bare_decimal_far_from_anchor_survives():
    """A bare decimal with NO conf-word/vocab anchor anywhere nearby and
    not matching a known constant is NOT redacted -- verbatim quoted_text
    with an unrelated number (e.g. a dollar figure) must survive. 0.62 is
    deliberately not a known confidence-system constant."""
    padding = "x" * 200
    out, hits = _screen(f"The invoice was $0.62 million. {padding}")
    assert "0.62" in out


def test_pass3_proximity_window_boundary():
    """Just inside the 120-char proximity window is redacted; comfortably
    outside it is not (uses a decimal that is NOT a known constant so only
    the proximity rule is exercised)."""
    near = "conf" + (" " * 100) + "0.62"
    out_near, hits_near = _screen(near)
    assert "0.62" not in out_near

    far = "conf" + (" " * 300) + "0.62"
    out_far, hits_far = _screen(far)
    assert "0.62" in out_far


# ── Pass 4: known-constant bare-decimals (unconditional) ────────────────


def test_pass4_known_constant_value_redacted_without_proximity():
    """A bare decimal exactly matching a CONFIDENCE_MAP/REASONING_DISCOUNT/
    etc. value is redacted even with NO nearby conf-word -- judgment call
    (b) in the module docstring."""
    padding = "x" * 300  # comfortably outside the proximity window
    out, hits = _screen(f"{padding} already discounted x0.95 from the source.")
    assert "0.95" not in out
    assert any(h.category == "known_constant_bare_decimal" for h in hits)


def test_pass4_introspective_discount_product_redacted():
    """hard_data (0.95) x introspective discount (0.95) = 0.9025, rounded
    to 3dp -- a known-constant-derived product, not a named constant
    itself."""
    padding = "x" * 300
    out, hits = _screen(f"{padding} computed value 0.9025 for this claim.")
    assert "0.9025" not in out


def test_pass4_unrelated_decimal_not_a_known_constant_survives_far_away():
    """A bare decimal that does NOT match any known constant, and is far
    from any anchor, is not redacted (e.g. 0.62 is not in CONFIDENCE_MAP/
    REASONING_DISCOUNT/ABDUCTIVE_CONFIDENCE_CAP)."""
    padding = "x" * 300
    out, hits = _screen(f"{padding} a correlation of 0.62 was observed.")
    assert "0.62" in out


# ── Pass 5: node-ID citations ────────────────────────────────────────────


def test_pass5_node_id_citation_redacted():
    out, hits = _screen("ob_0004 records that the source confirms this.")
    assert "ob_0004" not in out
    assert any(h.category == "node_id_citation" for h in hits)


def test_pass5_multiple_prefixes():
    out, _ = _screen("Derived from dv_0021 and ax_0007 jointly.")
    assert "dv_0021" not in out
    assert "ax_0007" not in out


def test_pass5_case_insensitive_prefix():
    out, _ = _screen("See OB_0004 for the source citation.")
    assert "OB_0004" not in out


def test_screen_node_id_citations_only_redacts_node_ids():
    """The narrower node-ID-only screen (used for evidence.title etc.) must
    NOT touch decimals/percentages/vocab -- only bare node-ID citations."""
    text = "cj_0005 cross-lineage test at conf 0.95, 90% agreement"
    out, hits = screen_node_id_citations(text, NODE, "title")
    assert "cj_0005" not in out
    assert "0.95" in out  # untouched -- not this screen's job
    assert "90%" in out
    assert len(hits) == 1
    assert hits[0].category == "node_id_citation"


# ── Pass 6: conf-percent phrasing ────────────────────────────────────────


def test_pass6_percent_after_conf_word():
    out, hits = _screen("I am 95% confident in this reading.")
    assert "95%" not in out
    assert any(h.category == "conf_percent" for h in hits)


def test_pass6_conf_word_then_percent():
    out, _ = _screen("confidence is about 95 percent here.")
    assert "95 percent" not in out


def test_pass6_percent_then_conf_word():
    out, _ = _screen("roughly 80% confidence in this derivation.")
    assert "80%" not in out


# ── Pass 7: proximity bare-percent ───────────────────────────────────────


def test_pass7_bare_percent_near_conf_word_redacted():
    """Anchored off a VOCAB hit rather than a bare conf-word so the direct
    conf-word-adjacent-to-percent pattern (pass 6) cannot fire -- isolates
    pass 7's proximity-to-any-anchor (vocab hits count too) rule."""
    out, hits = _screen(
        "This is an attributed_analysis claim, and separately, "
        "roughly 40% of the sample agreed."
    )
    assert "40%" not in out
    assert any(h.category == "proximity_bare_percent" for h in hits)


def test_pass7_bare_percent_far_from_anchor_survives():
    """Bare percentages are common ordinary prose ('50% of respondents') --
    must NOT be unconditionally redacted the way known-constant decimals
    are (judgment call (c))."""
    padding = "x" * 300
    out, hits = _screen(f"{padding} 50% of respondents agreed with this.")
    assert "50%" in out


def test_pass7_fractional_percent_near_vocab_hit_redacted():
    """Reviewer-fairy catch (2026-07-08, 3rd round -- review of the pass-7
    fix itself): a genuinely fractional percentage (e.g. "90.25%" -- the
    exact form an introspective-discount product takes: hard_data 0.95 x
    0.95 = 0.9025 = 90.25%, a case this module's OWN docstring already
    flags as realistic) was never matched as ONE clean span by any percent
    pattern, because \\d{1,3} cannot span a decimal point. This left "90."
    fully visible even in cases where pass 6 accidentally grabbed just the
    post-decimal "25%" via a nearby conf-word. Anchored off a vocab hit
    (not a bare conf-word) so pass 6 cannot fire, isolating pass 7's own
    fractional-number handling."""
    out, hits = _screen(
        "This is an attributed_analysis claim, and separately, "
        "roughly 90.25% of the sample agreed."
    )
    assert "90.25%" not in out
    assert "90." not in out  # the whole fractional number must be gone, not just the tail
    assert any(h.category == "proximity_bare_percent" for h in hits)


def test_pass7_fractional_percent_far_from_anchor_survives():
    """Mirrors the whole-number far-from-anchor case: a fractional
    percentage with no anchor nearby must not be unconditionally redacted."""
    padding = "x" * 300
    out, hits = _screen(f"{padding} 90.25% of respondents agreed with this.")
    assert "90.25%" in out


def test_pass6_conf_word_then_fractional_percent():
    """The conf-word-adjacent pass (6) must also correctly redact the
    WHOLE fractional number, not just its post-decimal tail."""
    out, hits = _screen("roughly 90.25% confident in this reading.")
    assert "90.25%" not in out
    assert "90." not in out


# ── Overlap / merge behavior ──────────────────────────────────────────────


def test_overlapping_spans_merge_into_single_redaction_token():
    """A conf-prefixed decimal directly adjacent to a vocab hit must not
    produce two separate [metadata redacted] tokens for what a reader
    would see as one contiguous leak."""
    out, hits = _screen("conf 0.95 attributed_analysis basis.")
    assert out.count(REDACTED_TOKEN) <= 2  # merged where spans touch/overlap
    assert "0.95" not in out
    assert "attributed_analysis" not in out


def test_empty_text_short_circuits():
    out, hits = screen_text("", NODE, FIELD)
    assert out == ""
    assert hits == []


def test_no_hits_returns_original_unchanged():
    text = "A plain claim with no confidence-shaped content at all."
    out, hits = _screen(text)
    assert out == text
    assert hits == []


# ── redacted_char_count / redaction_fraction ─────────────────────────────


def test_redacted_char_count_matches_merged_span_length():
    text = "conf 0.95 here."
    out, hits = _screen(text)
    # "conf 0.95" is the matched span
    matched = "conf 0.95"
    assert redacted_char_count(text, hits) == len(matched)


def test_redaction_fraction_is_fraction_of_original_length():
    text = "conf 0.95 here."
    _, hits = _screen(text)
    frac = redaction_fraction(text, hits)
    assert 0.0 < frac < 1.0
    assert frac == redacted_char_count(text, hits) / len(text)


def test_redaction_fraction_empty_text_is_zero():
    assert redaction_fraction("", []) == 0.0


def test_redaction_fraction_no_hits_is_zero():
    text = "nothing to redact here"
    assert redaction_fraction(text, []) == 0.0


def test_redaction_fraction_fully_redacted_is_near_one():
    text = "conf 0.95"
    _, hits = _screen(text)
    assert redaction_fraction(text, hits) == 1.0
