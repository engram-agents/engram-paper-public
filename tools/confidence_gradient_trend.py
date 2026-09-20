#!/usr/bin/env python3
"""Mean confidence per reasoning type over the graph's lifetime.

Lei's question, 2026-09-20: for §6.1, is it worth keeping both data points "or even
more like historical curves?" This produces the curve, so the answer can be made on
the data rather than on taste.

§6.1's claim is that the confidence model tracks ARGUMENT SHAPE rather than author
preference, and its strongest evidence is that the per-reasoning-type gradient held
to within 0.01 while the underlying counts more than doubled and reshuffled. Two
points support that weakly; a flat line across five months supports it properly, and
— this is the part a two-point reading cannot give — a WOBBLE would be visible.

⚠ WHAT THIS RECONSTRUCTS, AND THE BOUND THAT MATTERS. For each cut date it takes
nodes CREATED before that date and averages their CURRENT confidence. That is NOT
"the mean confidence as it stood on that date": a node's confidence can be
recomputed after creation (supersede, cascade, re-derivation), and this instrument
sees only today's value. So the series answers "how does the gradient look across
cohorts of nodes grouped by creation date", not "what would this table have printed
in June". The distinction is real and the chapter must not blur it — the claim it
supports is about the model's behaviour across cohorts, which is what §6.1 argues
anyway.

Superseded nodes are INCLUDED at cuts after their creation, because they existed and
were scored then; excluding them would silently select for claims that survived.
"""
import argparse, glob, json, os, sqlite3, statistics, sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import _ssot

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    ap = argparse.ArgumentParser()
    _ssot.add_db_arg(ap)
    ap.add_argument("--step-days", type=int, default=14)
    ap.add_argument("--cohort", action="store_true",
                    help="group by CALENDAR MONTH of creation instead of cumulative cuts — the view §6.1's monthly table reports")
    ap.add_argument("--min-n", type=int, default=10, help="suppress a cell below this count")
    a = ap.parse_args()
    db = _ssot.resolve_db(a.db, allow_unpinned=a.allow_unpinned)
    c = _ssot.connect(db)

    rows = []
    for ca, m, conf in c.execute(
            "SELECT created_at, metadata, confidence FROM nodes "
            "WHERE type='derivation' AND created_at IS NOT NULL AND confidence IS NOT NULL"):
        rt = None
        if m:
            try: rt = json.loads(m).get("reasoning_type")
            except Exception: pass
        if rt: rows.append((ca[:10], rt, conf))

    print(f"# source: {os.path.relpath(db, REPO)}")
    print(f"# cohorts by creation date, CURRENT confidence — see docstring for what that is not")
    print(f"# cells with n < {a.min_n} are shown as '-' rather than a noisy mean\n")

    TRACK = ["inductive_generalization", "inductive_enumeration", "deductive_modus_ponens",
             "abductive_best_explanation", "inductive_analogy"]
    lo = min(r[0] for r in rows); hi = max(r[0] for r in rows)
    d = datetime.strptime(lo, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    end = datetime.strptime(hi, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    if a.cohort:
        # MONTHLY COHORTS — each row is the derivations CREATED in that month, not a
        # cumulative prefix. This is the view §6.1's monthly table reports, and it is
        # a different measurement from the cumulative one below: a cumulative cut damps
        # late movement because each new month is a shrinking fraction of the total.
        # The two can order the per-type SPREADS differently, so never quote a spread
        # without saying which view produced it.
        months = sorted({r[0][:7] for r in rows})
        hdr = f"{'month':<9}{'n(dv)':>7}" + "".join(f"{t.split('_')[-1][:9]:>11}" for t in TRACK)
        print(hdr); print("-" * len(hdr))
        spread = {t: [] for t in TRACK}
        for mo in months:
            sel = [r for r in rows if r[0][:7] == mo]
            line = f"{mo:<9}{len(sel):>7,}"
            for t in TRACK:
                vals = [conf for _, rt, conf in sel if rt == t]
                if len(vals) >= a.min_n:
                    line += f"{statistics.fmean(vals):>11.2f}"; spread[t].append(statistics.fmean(vals))
                else:
                    line += f"{'-':>11}"
            print(line)
        print("\n# per-type spread ACROSS MONTHLY COHORTS (reportable cells only):")
        for t in TRACK:
            v = spread[t]
            if len(v) >= 2:
                print(f"  {t:<30} min {min(v):.3f}  max {max(v):.3f}  "
                      f"range {max(v)-min(v):.3f}  over {len(v)} months")
        return

    hdr = f"{'date':<12}{'n(dv)':>7}" + "".join(f"{t.split('_')[-1][:9]:>11}" for t in TRACK)
    print(hdr); print("-" * len(hdr))
    while d <= end + timedelta(days=a.step_days):
        cut = d.strftime("%Y-%m-%d")
        sel = [r for r in rows if r[0] <= cut]
        if sel:
            line = f"{cut:<12}{len(sel):>7,}"
            for t in TRACK:
                vals = [conf for _, rt, conf in sel if rt == t]
                line += f"{statistics.fmean(vals):>11.2f}" if len(vals) >= a.min_n else f"{'-':>11}"
            print(line)
        d += timedelta(days=a.step_days)

    print("\n# per-type spread across all cuts where the cell was reportable:")
    for t in TRACK:
        series = []
        d = datetime.strptime(lo, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        while d <= end + timedelta(days=a.step_days):
            cut = d.strftime("%Y-%m-%d")
            vals = [conf for ca, rt, conf in rows if rt == t and ca <= cut]
            if len(vals) >= a.min_n: series.append(statistics.fmean(vals))
            d += timedelta(days=a.step_days)
        if series:
            print(f"  {t:<32} min {min(series):.3f}  max {max(series):.3f}  "
                  f"range {max(series)-min(series):.3f}  over {len(series)} cuts")

if __name__ == "__main__":
    main()
