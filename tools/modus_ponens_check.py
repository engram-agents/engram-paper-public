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
"""
import argparse, json, os, statistics, sys

import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import _ssot

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    _ssot.add_db_arg(ap)
    a = ap.parse_args()
    db = _ssot.resolve_db(a.db, allow_unpinned=a.allow_unpinned)
    c = _ssot.connect(db)

    print(f"# source: {os.path.relpath(db, REPO)}")

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


if __name__ == "__main__":
    main()
