"""Tests for tools/compression_fidelity/tree.py -- reasoning-tree rendering
(pre-reg §4.1). Uses a lightweight duck-typed fake cache (same pattern as
test_packet.py's FakeCache) rather than a real DB.
"""

from tools.compression_fidelity.db import NodeRow
from tools.compression_fidelity.tree import render_reasoning_tree


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


def _obs(id_, claim="an observation claim", quoted_text="a quote", evidence_id=None):
    return NodeRow(
        id=id_, type="observation_factual", claim=claim, quoted_text=quoted_text,
        interpretation="i", quote_type="hard_data", evidence_id=evidence_id,
        logical_chain=None, confidence=0.95, metadata={},
    )


def _deriv(id_, claim="a derived claim", logical_chain="because of the premises", interpretation="i"):
    return NodeRow(
        id=id_, type="derivation", claim=claim, quoted_text=None,
        interpretation=interpretation, quote_type=None, evidence_id=None,
        logical_chain=logical_chain, confidence=0.8,
        metadata={"reasoning_type": "deductive_modus_ponens"},
    )


def _axiom(id_, claim="an axiom claim"):
    return NodeRow(
        id=id_, type="axiom", claim=claim, quoted_text=None,
        interpretation=None, quote_type=None, evidence_id=None,
        logical_chain=None, confidence=1.0, metadata={},
    )


def test_target_with_one_observation_premise():
    target = _deriv("dv_1")
    ob = _obs("ob_1")
    cache = FakeCache({"dv_1": target, "ob_1": ob}, premises={"dv_1": ["ob_1"]})
    result = render_reasoning_tree(cache, target)
    assert "[TARGET]" in result.markdown
    assert "[EVIDENCE for P1]" in result.markdown
    assert result.node_ids_rendered == ["dv_1", "ob_1"]


def test_two_level_derivation_chain_nests_by_indentation():
    target = _deriv("dv_1", claim="top claim")
    mid = _deriv("dv_2", claim="mid claim")
    leaf = _obs("ob_1", claim="leaf claim")
    cache = FakeCache(
        {"dv_1": target, "dv_2": mid, "ob_1": leaf},
        premises={"dv_1": ["dv_2"], "dv_2": ["ob_1"]},
    )
    result = render_reasoning_tree(cache, target)
    lines = result.markdown.split("\n")
    # target at depth 0 (no leading indent), mid-premise indented once,
    # leaf-of-mid indented twice.
    target_line = next(l for l in lines if "top claim" in l)
    mid_line = next(l for l in lines if "mid claim" in l)
    leaf_line = next(l for l in lines if "leaf claim" in l)
    assert not target_line.startswith(" ")
    assert mid_line.startswith("    ") and not mid_line.startswith("        ")
    assert leaf_line.startswith("        ")


def test_shared_premise_dag_renders_full_once_then_back_reference():
    """Load-bearing per the module docstring: a premise cited from two
    different paths must be fully expanded only at its FIRST occurrence;
    later occurrences become a back-reference, and the claim text must
    appear in the markdown exactly once."""
    target = _deriv("dv_1")
    shared = _obs("ob_shared", claim="a uniquely identifiable shared claim text")
    other = _deriv("dv_2", claim="a second premise that also cites the shared node")
    cache = FakeCache(
        {"dv_1": target, "dv_2": other, "ob_shared": shared},
        premises={"dv_1": ["ob_shared", "dv_2"], "dv_2": ["ob_shared"]},
    )
    result = render_reasoning_tree(cache, target)
    assert result.markdown.count("a uniquely identifiable shared claim text") == 1
    assert "same node as" in result.markdown


def test_dangling_premise_renders_without_leaking_raw_node_id():
    """Reviewer-fairy catch #2b (documented in the module docstring): a
    derives_from edge to a missing node must render 'premise not found'
    WITHOUT interpolating the raw dangling node ID."""
    target = _deriv("dv_1")
    cache = FakeCache({"dv_1": target}, premises={"dv_1": ["ob_missing_xyz"]})
    result = render_reasoning_tree(cache, target)
    assert "premise not found" in result.markdown
    assert "ob_missing_xyz" not in result.markdown


def test_non_observation_non_derivation_premise_renders_as_support_leaf():
    target = _deriv("dv_1")
    ax = _axiom("ax_1", claim="an axiom claim")
    cache = FakeCache({"dv_1": target, "ax_1": ax}, premises={"dv_1": ["ax_1"]})
    result = render_reasoning_tree(cache, target)
    assert "[SUPPORT for P1]" in result.markdown
    assert "an axiom claim" in result.markdown
    # no evidence/quoted_text lines for a non-observation leaf
    assert "quoted_text:" not in result.markdown


def test_reasoning_type_and_confidence_never_leak_into_rendered_tree():
    target = _deriv(
        "dv_1", logical_chain="derived via deductive_modus_ponens, conf 0.90"
    )
    cache = FakeCache({"dv_1": target})
    result = render_reasoning_tree(cache, target)
    assert "deductive_modus_ponens" not in result.markdown
    assert "0.90" not in result.markdown


def test_chain_accumulator_counts_claim_too_not_just_logical_chain():
    """Colleague-review-caught gap (Borges's breadth fairy, 2026-07-09):
    chain_redacted_chars/chain_total_chars must accumulate from EVERY
    tree-rendered field (claim, logical_chain, quoted_text), not just
    logical_chain -- otherwise a derivation whose CLAIM (not chain) is
    almost entirely leak vocabulary reports chain_redacted_chars == 0 and
    silently escapes the >20%-gutted exclusion gate. Verified via a
    leaky-claim/clean-chain node: BOTH fields' redactions must now count."""
    leaky_claim_clean_chain = _deriv(
        "dv_1",
        claim="conf 0.95 attributed_analysis conf 0.95 attributed_analysis",
        logical_chain="a perfectly ordinary reasoning chain with no leaks",
    )
    cache1 = FakeCache({"dv_1": leaky_claim_clean_chain})
    result1 = render_reasoning_tree(cache1, leaky_claim_clean_chain)
    assert result1.chain_redacted_chars > 0  # the leaky CLAIM must now count
    assert result1.chain_total_chars == (
        len(leaky_claim_clean_chain.claim) + len(leaky_claim_clean_chain.logical_chain)
    )

    clean_claim_leaky_chain = _deriv(
        "dv_2",
        claim="a perfectly ordinary claim with no leaks",
        logical_chain="conf 0.95 attributed_analysis conf 0.95 attributed_analysis",
    )
    cache2 = FakeCache({"dv_2": clean_claim_leaky_chain})
    result2 = render_reasoning_tree(cache2, clean_claim_leaky_chain)
    assert result2.chain_redacted_chars > 0  # the leaky CHAIN still counts too
    assert result2.chain_total_chars == (
        len(clean_claim_leaky_chain.claim) + len(clean_claim_leaky_chain.logical_chain)
    )


def test_chain_accumulator_counts_observation_premise_claim_and_quoted_text():
    """The same gutted-scope gap, but for an observation premise: its
    claim AND quoted_text must both count toward the tree-wide fraction,
    not just a derivation's own claim/logical_chain."""
    target = _deriv("dv_1", claim="a clean target claim", logical_chain="a clean chain")
    leaky_ob = _obs(
        "ob_1",
        claim="conf 0.95 attributed_analysis",
        quoted_text="conf 0.95 attributed_analysis",
    )
    cache = FakeCache({"dv_1": target, "ob_1": leaky_ob}, premises={"dv_1": ["ob_1"]})
    result = render_reasoning_tree(cache, target)
    assert result.chain_redacted_chars > 0
    expected_total = (
        len(target.claim) + len(target.logical_chain)
        + len(leaky_ob.claim) + len(leaky_ob.quoted_text)
    )
    assert result.chain_total_chars == expected_total


def test_target_claim_screened_is_the_targets_own_claim_not_a_premise():
    target = _deriv("dv_1", claim="the target's own claim")
    premise = _deriv("dv_2", claim="a premise's claim, not the target's")
    cache = FakeCache({"dv_1": target, "dv_2": premise}, premises={"dv_1": ["dv_2"]})
    result = render_reasoning_tree(cache, target)
    assert result.target_claim_screened == "the target's own claim"


def test_evidence_leaf_carries_quoted_text_and_source_fields():
    target = _deriv("dv_1")
    ob = _obs("ob_1", claim="obs claim", quoted_text="the actual quote", evidence_id="ev_1")
    cache = FakeCache(
        {"dv_1": target, "ob_1": ob},
        premises={"dv_1": ["ob_1"]},
        evidence={"ev_1": {"url": "http://x.com", "domain": "x.com",
                            "title": "T", "source_date": "2026-01-01"}},
    )
    result = render_reasoning_tree(cache, target)
    assert "the actual quote" in result.markdown
    assert "http://x.com" in result.markdown


def test_evidence_title_node_id_citation_is_screened():
    target = _deriv("dv_1")
    ob = _obs("ob_1", evidence_id="ev_1")
    cache = FakeCache(
        {"dv_1": target, "ob_1": ob},
        premises={"dv_1": ["ob_1"]},
        evidence={"ev_1": {"url": None, "domain": None,
                            "title": "cj_0005 cross-lineage test", "source_date": None}},
    )
    result = render_reasoning_tree(cache, target)
    assert "cj_0005" not in result.markdown


def test_premise_interpretation_never_leaks_into_tree():
    """Reviewer-fairy suggestion (2026-07-08): packet.py/tree.py's own
    documented judgment call is that `interpretation` is rendered ONLY on
    the top-level TARGET node, never on premise nodes inside a reasoning
    tree -- but no test pinned this with a distinguishing marker (the
    fixtures' generic interpretation="i" wouldn't catch a regression even
    if one were added naively, since "i" is too short/common to notice
    missing). A unique marker string makes a future accidental
    `screen(premise.interpretation, ...)` call inside render_node fail
    loudly here instead of silently leaking."""
    target = _deriv("dv_1", interpretation="TARGET_INTERP_UNIQUE_MARKER_XYZ")
    premise = _deriv("dv_2", interpretation="PREMISE_INTERP_SHOULD_NEVER_LEAK_ABC123")
    cache = FakeCache({"dv_1": target, "dv_2": premise}, premises={"dv_1": ["dv_2"]})
    result = render_reasoning_tree(cache, target)
    assert "PREMISE_INTERP_SHOULD_NEVER_LEAK_ABC123" not in result.markdown
    # target's own interpretation is ALSO never rendered by tree.py itself
    # (packet.py handles interpretation separately at the top level) --
    # confirms tree.py truly never touches interpretation for any node.
    assert "TARGET_INTERP_UNIQUE_MARKER_XYZ" not in result.markdown
