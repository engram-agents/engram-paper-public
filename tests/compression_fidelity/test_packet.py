"""Tests for tools/compression_fidelity/packet.py -- the packet-extraction
exclusion gates (pre-reg §4.1): >20% chain-redaction-fraction exclusion,
the ~15k-token max-packet-size guard, and opaque packet_id handling. Like
redact.py, this module had zero automated tests before this suite.

A lightweight fake cache (duck-typed against `tree.GraphCache`'s
`.node()` / `.evidence()` / `.premises` interface) avoids needing a real
sqlite DB for these packet-level unit tests -- `build_packet` and
`tree.render_reasoning_tree` only ever call these three members.
"""

from tools.compression_fidelity.db import NodeRow
from tools.compression_fidelity.packet import (
    MAX_CHAIN_REDACTION_FRACTION,
    MAX_PACKET_TOKENS,
    build_packet,
)


class FakeCache:
    def __init__(self, nodes, premises=None, evidence=None):
        self._nodes = nodes
        self.premises = premises or {}
        self._evidence = evidence or {}

    def node(self, node_id):
        return self._nodes.get(node_id)

    def evidence(self, evidence_id):
        return self._evidence.get(
            evidence_id, {"url": None, "domain": None, "title": None, "source_date": None}
        )


def _obs(id_, claim="a claim", quoted_text="a quote", interpretation="an interpretation",
         evidence_id=None):
    return NodeRow(
        id=id_, type="observation_factual", claim=claim, quoted_text=quoted_text,
        interpretation=interpretation, quote_type="hard_data", evidence_id=evidence_id,
        logical_chain=None, confidence=0.95, metadata={},
    )


def _deriv(id_, claim="a derived claim", logical_chain="because of the premises",
           interpretation="an interpretation"):
    return NodeRow(
        id=id_, type="derivation", claim=claim, quoted_text=None,
        interpretation=interpretation, quote_type=None, evidence_id=None,
        logical_chain=logical_chain, confidence=0.80,
        metadata={"reasoning_type": "deductive_modus_ponens"},
    )


# ── Observation packets ──────────────────────────────────────────────────


def test_observation_packet_builds_clean_when_no_redaction():
    node = _obs("ob_1")
    cache = FakeCache({"ob_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert not result.excluded
    assert result.packet is not None
    assert result.packet["packet_id"] == "pkt_00001"
    assert result.packet["node_type"] == "observation"
    assert result.packet["claim"] == "a claim"
    assert result.packet["interpretation"] == "an interpretation"


def test_observation_packet_without_interpretation_arm_omits_field():
    node = _obs("ob_1")
    cache = FakeCache({"ob_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=False)
    assert "interpretation" not in result.packet
    assert result.arm == "without_interpretation"


def test_observation_packet_excludes_real_node_id_from_packet():
    """packet_id must be opaque -- the real node ID must not appear
    anywhere in the packet dict (reviewer-fairy catch #1)."""
    node = _obs("ob_1")
    cache = FakeCache({"ob_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    import json
    serialized = json.dumps(result.packet)
    assert "ob_1" not in serialized


def test_observation_packet_evidence_fields_served_verbatim():
    node = _obs("ob_1", evidence_id="ev_1")
    cache = FakeCache(
        {"ob_1": node},
        evidence={"ev_1": {"url": "http://example.com", "domain": "example.com",
                            "title": "A Title", "source_date": "2026-01-01"}},
    )
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert result.packet["evidence"]["url"] == "http://example.com"
    assert result.packet["evidence"]["source_date"] == "2026-01-01"


def test_observation_packet_evidence_title_node_id_citation_screened():
    """Evidence fields are verbatim EXCEPT for the narrower node-ID-
    citation screen (a title that itself names another node's ID)."""
    node = _obs("ob_1", evidence_id="ev_1")
    cache = FakeCache(
        {"ob_1": node},
        evidence={"ev_1": {"url": None, "domain": None,
                            "title": "cj_0005 cross-lineage test", "source_date": None}},
    )
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert "cj_0005" not in result.packet["evidence"]["title"]


# ── Derivation packets ────────────────────────────────────────────────────


def test_derivation_packet_builds_clean_reasoning_tree():
    node = _deriv("dv_1")
    cache = FakeCache({"dv_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert not result.excluded
    assert result.packet["node_type"] == "derivation"
    assert "reasoning_tree" in result.packet
    assert "[TARGET]" in result.packet["reasoning_tree"]


def test_derivation_packet_reasoning_type_never_in_packet():
    node = _deriv("dv_1", logical_chain="derived via deductive_modus_ponens from evidence")
    cache = FakeCache({"dv_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    import json
    serialized = json.dumps(result.packet)
    assert "deductive_modus_ponens" not in serialized


# ── >20%-gutted-chain exclusion (§4.1) ────────────────────────────────────


def test_observation_excluded_when_over_20_percent_redacted():
    """A claim/quoted_text/interpretation dominated by confidence-leak
    vocabulary must exceed the 20% threshold and be excluded, packet=None."""
    node = _obs(
        "ob_1",
        claim="conf 0.95 attributed_analysis conf 0.95 attributed_analysis",
        quoted_text="short",
        interpretation="ok",
    )
    cache = FakeCache({"ob_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert result.excluded
    assert result.packet is None
    assert result.chain_redaction_fraction > MAX_CHAIN_REDACTION_FRACTION
    assert "20%" in result.exclusion_reason
    assert result.node_id == "ob_1"  # excluded items reported BY ID


def test_observation_not_excluded_when_under_20_percent_redacted():
    node = _obs(
        "ob_1",
        claim="a long claim with plenty of ordinary words and conf 0.95 buried once in it",
        quoted_text="another long quote with many ordinary words and no leaks at all here",
        interpretation="a long interpretation with many ordinary words and no leaks either",
    )
    cache = FakeCache({"ob_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert not result.excluded
    assert result.chain_redaction_fraction <= MAX_CHAIN_REDACTION_FRACTION


def test_derivation_excluded_when_logical_chain_over_20_percent_redacted():
    node = _deriv(
        "dv_1",
        claim="fine claim text with plenty of words",
        logical_chain="conf 0.95 attributed_analysis",  # entirely leak vocabulary
    )
    cache = FakeCache({"dv_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert result.excluded
    assert result.packet is None
    assert "20%" in result.exclusion_reason


def test_derivation_excluded_when_claim_gutted_but_logical_chain_clean():
    """Colleague-review-caught BLOCKER (Borges's breadth fairy, 2026-07-09):
    a derivation whose CLAIM (not logical_chain) is almost entirely
    confidence-leak vocabulary, with a clean logical_chain, MUST still be
    excluded. Before the fix, chain_redacted_chars only accumulated from
    logical_chain, so this exact case reported chain_fraction == 0.0 and
    reached the judge unexcluded -- a gutted packet the >20% rule exists
    to catch, silently passing straight through."""
    node = _deriv(
        "dv_1",
        claim="conf 0.95 attributed_analysis conf 0.95 attributed_analysis",
        logical_chain="a perfectly ordinary, entirely clean reasoning chain",
    )
    cache = FakeCache({"dv_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert result.excluded
    assert result.packet is None
    assert "20%" in result.exclusion_reason
    assert result.chain_redaction_fraction > 0.20


def test_derivation_chain_fraction_scoped_to_logical_chain_not_interpretation():
    """The derivation branch's chain_fraction must be computed ONLY from
    logical_chain text (tree.py's accumulator), NOT the top-level
    interpretation field -- even a heavily-redacted interpretation must
    not by itself trigger the >20%-chain exclusion."""
    node = _deriv(
        "dv_1",
        claim="a fine claim",
        logical_chain="a long clean logical chain with no leaks in it whatsoever at all",
        interpretation="conf 0.95 attributed_analysis conf 0.95",  # fully redacted
    )
    cache = FakeCache({"dv_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert not result.excluded


def test_exclusion_reason_reports_the_actual_fraction():
    node = _obs("ob_1", claim="conf 0.95", quoted_text="", interpretation="")
    cache = FakeCache({"ob_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert result.excluded
    assert "100.0%" in result.exclusion_reason


# ── 15k max-packet-token guard (§4.1) ─────────────────────────────────────


def test_packet_excluded_when_over_token_guard():
    huge_claim = " ".join(["word"] * (MAX_PACKET_TOKENS + 1))
    node = _obs("ob_1", claim=huge_claim, quoted_text="", interpretation="")
    cache = FakeCache({"ob_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert result.excluded
    assert result.packet is None
    assert "max-size guard" in result.exclusion_reason
    assert result.token_count > MAX_PACKET_TOKENS


def test_packet_not_excluded_when_under_token_guard():
    small_claim = " ".join(["word"] * 100)
    node = _obs("ob_1", claim=small_claim, quoted_text="", interpretation="")
    cache = FakeCache({"ob_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert not result.excluded
    assert result.token_count <= MAX_PACKET_TOKENS


def test_gutted_chain_check_takes_priority_over_token_guard():
    """When BOTH gates would fire, the >20%-gutted check is checked first
    (packet.py's if/elif order) -- verify the reported reason matches."""
    huge_leak_claim = " ".join(["conf 0.95"] * (MAX_PACKET_TOKENS // 2 + 10))
    node = _obs("ob_1", claim=huge_leak_claim, quoted_text="", interpretation="")
    cache = FakeCache({"ob_1": node})
    result = build_packet(cache, node, "pkt_00001", include_interpretation=True)
    assert result.excluded
    assert "20%" in result.exclusion_reason


# ── Reported-by-ID discipline ──────────────────────────────────────────────


def test_excluded_packet_result_still_carries_node_id_and_packet_id():
    """Both required outputs of an exclusion (§4.1: 'excluded and reported
    by ID') must survive on the result even when packet=None."""
    node = _obs("ob_1", claim="conf 0.95", quoted_text="", interpretation="")
    cache = FakeCache({"ob_1": node})
    result = build_packet(cache, node, "pkt_00042", include_interpretation=True)
    assert result.excluded
    assert result.node_id == "ob_1"
    assert result.packet_id == "pkt_00042"
    assert result.exclusion_reason is not None


# ── Unexpected node type ───────────────────────────────────────────────────


def test_unexpected_node_type_raises():
    node = NodeRow(
        id="ax_1", type="axiom", claim="an axiom", quoted_text=None,
        interpretation=None, quote_type=None, evidence_id=None,
        logical_chain=None, confidence=1.0, metadata={},
    )
    cache = FakeCache({"ax_1": node})
    try:
        build_packet(cache, node, "pkt_00001", include_interpretation=True)
        assert False, "expected ValueError for a non-observation/derivation node type"
    except ValueError:
        pass
