"""Logic-depth computation (pre-reg §2/§5): depth = max(depth of premises) + 1,
observations = depth 1 (no premises).

The graph is a DAG (§5: "don't assume a tree — a derivation can cite the
same premise as a sibling"), so depth is computed with memoization across
the WHOLE graph, not per-sample — a shared premise's depth is resolved once
and reused everywhere it's cited.

Judgment call (flagged in the handoff): the pre-reg only defines depth for
observations (1, base case) and derivations (recursive). A derivation's
`derives_from` premises are not always observations or derivations — axioms,
conjectures, and lessons are valid MECH-5 supporting-id types too (confirmed
present in the smoke-test graph). This module treats ANY non-derivation
premise as a depth-1 base case (the same treatment as an observation) rather
than restricting the base case to `type == observation`. This is the
natural generalization of "observations = depth 1 (no premises)" to "a node
we do not recurse into is depth 1" and keeps depth defined for every node
that can appear as a premise, without inventing a different rule for a case
the pre-reg does not address.
"""

from __future__ import annotations

import sys

from .constants import DERIVATION_TYPES


def compute_depth_map(
    node_types: dict[str, str],
    premises: dict[str, list[str]],
) -> dict[str, int]:
    """Return {node_id: depth} for every node reachable as a key in
    `node_types`. Only nodes of a DERIVATION type recurse into their
    premises; every other node type is a depth-1 base case.
    """
    memo: dict[str, int] = {}
    # Iterative post-order to avoid Python recursion-limit issues on long
    # chains; a visiting set catches an accidental cycle (should never
    # happen in a DAG, but fails loudly rather than looping forever).
    def resolve(start: str) -> int:
        if start in memo:
            return memo[start]
        stack = [(start, False)]
        visiting: set[str] = set()
        while stack:
            node_id, processed = stack.pop()
            if node_id in memo:
                continue
            ntype = node_types.get(node_id)
            prems = premises.get(node_id, []) if ntype in DERIVATION_TYPES else []
            if not prems:
                memo[node_id] = 1
                continue
            if processed:
                if any(p not in memo for p in prems):
                    raise RuntimeError(
                        f"depth cycle detected involving node {node_id!r} "
                        "(derives_from graph is not a DAG)"
                    )
                memo[node_id] = 1 + max(memo[p] for p in prems)
                visiting.discard(node_id)
                continue
            if node_id in visiting:
                raise RuntimeError(
                    f"depth cycle detected involving node {node_id!r} "
                    "(derives_from graph is not a DAG)"
                )
            visiting.add(node_id)
            stack.append((node_id, True))
            for p in prems:
                if p not in memo:
                    stack.append((p, False))
        return memo[start]

    for nid in list(node_types.keys()):
        if nid not in memo:
            resolve(nid)
    return memo


def depth_tier(depth: int) -> str:
    """1 / 2 / '>=3' per pre-reg §5."""
    if depth <= 1:
        return "1"
    if depth == 2:
        return "2"
    return ">=3"
