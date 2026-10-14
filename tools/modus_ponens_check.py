#!/usr/bin/env python3
"""Reproduction script for §6.1's modus-ponens figures.

A modus-ponens step is specified as `min(premises) x 0.98`. This script reproduces
the two numbers §6.1 checks that specification against, plus the structural fact
about weakest-premise provenance that §6.1 reports alongside them.

WHAT "SCORABLE" MEANS, stated because it is the one filtering choice the figures
depend on: a `deductive_modus_ponens` derivation is scorable only if at least one of
its `derives_from` premises is CURRENT and carries a non-null confidence (self-loops
excluded). A derivation whose premises rest entirely on since-superseded nodes is
excluded, not scored at 0 or dropped silently — its id is printed. On the frozen
SSoT this excludes exactly two of the 416 current modus-ponens derivations.

Five arms, in order:
  1. count of current `deductive_modus_ponens` derivations (reasoning_type read via
     `json_extract(metadata,'$.reasoning_type')`)
  2. mean MEASURED confidence over that set
  3. scorable count (current premises with non-null confidence, self-loops excluded)
  4. mean WEAKEST premise confidence over the scorable set, and what 0.98x that
     predicts
  5. how many scorable derivations have a derivation (not an observation) as their
     weakest premise

Excluded (non-scorable) derivation ids are printed, never silently dropped.

These five arms are the "v1 figures": they score each derivation against its CURRENT
`derives_from` premises only, and compare two population MEANS taken over different sets
(416 measured vs 414 scorable). They are kept, unchanged, for comparison.

PER-NODE ARM (v2): computed against the COMPUTED-FROM premise set
------------------------------------------------------------------
A mean of 0.98 x min equals 0.98 x the mean of min, so a residual gap between two means
means individual nodes deviate - and the v1 gap is mostly the instrument. A confidence is
computed from the premises the derivation had when it was last calculated: those include
premises later superseded, plus any replacement wired in by an `acknowledged_derives_from`
edge at an acknowledge step. Under the pinned engine version (v0.5.1) an acknowledge-step
recompute took the minimum over BOTH the old superseded premise and its replacement (a
known engine bug, since fixed), so the faithful computed-from set is the UNION.

Contract (tests/test_modus_ponens_check.py asserts each clause). For each CURRENT
derivation d with reasoning_type 'deductive_modus_ponens':
  1. CF(d) = targets of `derives_from` edges from d  UNION  targets of
     `acknowledged_derives_from` edges from d, REGARDLESS of the target's is_current,
     excluding d itself and excluding targets whose confidence is NULL.
  2. Empty CF -> d is listed in `excluded` by id; never scored, never silently dropped.
  3. expected(d) = round(0.98 * min(CF), 3). d is EXACT iff round(measured, 3) == expected.
     A NULL measured confidence -> its own `null_measured` list.
  4. DEVIATING nodes are printed with id, measured, expected, and the weakest premise's id,
     type and currency.
  5. PINNED-BY-SUPERSEDED-PREMISE: d has at least one `acknowledged_derives_from` edge AND
     min(CF) is attained ONLY at premise(s) with is_current = 0. Reported, not counted as
     deviations: they match the computed rule.
  6. Denominators are explicit: N, exact, deviating, excluded, null_measured are printed,
     and exact + deviating + excluded + null_measured == N is enforced in code
     (`check_denominators`): a mismatch is a crash with a message, never a print.
"""
import argparse, json, os, statistics, sys
from dataclasses import dataclass, field

import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import _ssot

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def print_v1_arms(c):
    """The five v1 arms, unchanged: current `derives_from` premises only."""
    # (1)/(2) current deductive_modus_ponens derivations + mean measured confidence
    rows = c.execute(
        "SELECT id, confidence FROM nodes "
        "WHERE type='derivation' AND is_current=1 "
        "AND json_extract(metadata,'$.reasoning_type')='deductive_modus_ponens'"
    ).fetchall()
    n_mp = len(rows)
    measured = [conf for _, conf in rows if conf is not None]
    mean_measured = statistics.fmean(measured) if measured else float("nan")

    print(f"\ncurrent deductive_modus_ponens derivations: {n_mp}")
    print(f"mean measured confidence: {mean_measured:.3f}")

    # (3)/(4)/(5) scorable set: at least one CURRENT, non-null-confidence,
    # non-self-loop premise via derives_from; weakest premise per derivation.
    scorable = 0
    weakest_vals = []
    weakest_is_derivation = 0
    excluded_ids = []
    for did, _dconf in rows:
        prem = c.execute(
            "SELECT n.id, n.type, n.confidence, n.is_current "
            "FROM edges e JOIN nodes n ON n.id = e.target_id "
            "WHERE e.source_id=? AND e.relation='derives_from'",
            (did,),
        ).fetchall()
        candidates = [
            (pid, ptype, pconf)
            for pid, ptype, pconf, pcur in prem
            if pcur == 1 and pconf is not None and pid != did
        ]
        if not candidates:
            excluded_ids.append(did)
            continue
        scorable += 1
        # weakest premise; a tie in confidence resolves to the lowest premise id, so which
        # premise "is" the weakest (and whether it is a derivation) never depends on the
        # order the join happened to return the rows in
        _wid, wtype, wconf = min(candidates, key=lambda x: (x[2], x[0]))
        weakest_vals.append(wconf)
        if wtype == "derivation":
            weakest_is_derivation += 1

    mean_weakest = statistics.fmean(weakest_vals) if weakest_vals else float("nan")
    predicted = mean_weakest * 0.98

    print(f"\nscorable (>=1 current, non-null-confidence, non-self-loop premise): {scorable}")
    print(f"mean weakest premise confidence: {mean_weakest:.3f}")
    print(f"predicted (mean weakest x 0.98): {predicted:.3f}")
    print(f"scorable derivations whose weakest premise is itself a derivation: "
          f"{weakest_is_derivation}")

    print(f"\nexcluded (not scorable — no current, confidence-bearing, non-self-loop "
          f"premise): {len(excluded_ids)} — {', '.join(sorted(excluded_ids))}")


@dataclass
class MPResult:
    """Per-node result. Lists hold ids, except `deviating` (dicts)."""
    n: int = 0
    exact: list = field(default_factory=list)
    deviating: list = field(default_factory=list)
    excluded: list = field(default_factory=list)
    null_measured: list = field(default_factory=list)
    pinned: list = field(default_factory=list)


def score_modus_ponens(c):
    """Score every current deductive_modus_ponens derivation against CF(d). See module docstring."""
    rows = c.execute(
        "SELECT id, confidence FROM nodes "
        "WHERE type='derivation' AND is_current=1 "
        "AND json_extract(metadata,'$.reasoning_type')='deductive_modus_ponens' "
        "ORDER BY id"
    ).fetchall()
    res = MPResult(n=len(rows))
    for did, dconf in rows:
        edges = c.execute(
            "SELECT e.target_id, e.relation, n.type, n.confidence, n.is_current "
            "FROM edges e JOIN nodes n ON n.id = e.target_id "
            "WHERE e.source_id=? AND e.relation IN ('derives_from','acknowledged_derives_from')",
            (did,),
        ).fetchall()
        has_ack = any(rel == "acknowledged_derives_from" for _t, rel, *_ in edges)
        cf = {}  # premise id -> (conf, type, is_current); union dedupes by id
        for pid, _rel, ptype, pconf, pcur in edges:
            if pid != did and pconf is not None:
                cf[pid] = (pconf, ptype, pcur == 1)
        if not cf:
            res.excluded.append(did)
            continue
        if dconf is None:
            res.null_measured.append(did)
            continue
        low = min(v[0] for v in cf.values())
        expected = round(0.98 * low, 3)
        if round(dconf, 3) == expected:
            res.exact.append(did)
            at_min = [v for v in cf.values() if v[0] == low]
            if has_ack and not any(v[2] for v in at_min):
                res.pinned.append(did)
        else:
            # weakest premise: ties resolve to the lowest premise id (as in v1)
            wid = min((pid for pid, v in cf.items() if v[0] == low))
            res.deviating.append({"id": did, "measured": dconf, "expected": expected,
                                  "weakest_id": wid, "weakest_type": cf[wid][1],
                                  "weakest_is_current": cf[wid][2]})
    return res


def check_denominators(res):
    """exact + deviating + excluded + null_measured must equal N, else crash."""
    total = (len(res.exact) + len(res.deviating) + len(res.excluded)
             + len(res.null_measured))
    if total != res.n:
        raise AssertionError(
            f"denominator identity broken: exact {len(res.exact)} + deviating "
            f"{len(res.deviating)} + excluded {len(res.excluded)} + null_measured "
            f"{len(res.null_measured)} = {total} != N {res.n}")


def print_per_node_arm(res):
    check_denominators(res)
    print("\n# per-node arm (v2): scored against the computed-from set "
          "(derives_from UNION acknowledged_derives_from, any is_current, "
          "self and NULL-confidence excluded)")
    print(f"N (current deductive_modus_ponens derivations): {res.n}")
    print(f"exact (round(measured,3) == round(0.98 x min(CF),3)): {len(res.exact)}")
    print(f"deviating: {len(res.deviating)}")
    for d in res.deviating:
        print(f"  {d['id']}: measured {d['measured']:.3f} expected {d['expected']:.3f}; "
              f"weakest premise {d['weakest_id']} ({d['weakest_type']}, "
              f"{'current' if d['weakest_is_current'] else 'superseded'})")
    print(f"excluded (empty computed-from set): {len(res.excluded)}"
          + (f" — {', '.join(sorted(res.excluded))}" if res.excluded else ""))
    print(f"NULL measured confidence: {len(res.null_measured)}"
          + (f" — {', '.join(sorted(res.null_measured))}" if res.null_measured else ""))
    print(f"denominator check: {len(res.exact)} + {len(res.deviating)} + "
          f"{len(res.excluded)} + {len(res.null_measured)} = "
          f"{len(res.exact) + len(res.deviating) + len(res.excluded) + len(res.null_measured)}"
          f" == N {res.n}")
    print(f"\npinned by a superseded premise (has an acknowledged_derives_from edge and "
          f"min(CF) attained only at is_current=0 premises; exact under the computed "
          f"rule, not deviations): {len(res.pinned)}"
          + (f" — {', '.join(sorted(res.pinned))}" if res.pinned else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    _ssot.add_db_arg(ap)
    a = ap.parse_args()
    db = _ssot.resolve_db(a.db, allow_unpinned=a.allow_unpinned)
    c = _ssot.connect(db)

    print(f"# source: {os.path.relpath(db, REPO)}")
    print("\n# v1 figures (current premises only; kept for comparison)")
    print_v1_arms(c)
    print_per_node_arm(score_modus_ponens(c))


if __name__ == "__main__":
    main()
