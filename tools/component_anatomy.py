#!/usr/bin/env python3
"""What holds the graph together, and what is outside the main continent.

Lei's questions, 2026-09-20:
  (1) Does the claim-bearing / non-claim-bearing split change the giant-component
      share? I.e. what role do NCB nodes play in GLUING the CB knowledge together?
  (2) What are the nodes OUTSIDE the main continent doing — a long tail of tiny
      clusters, or a secondary island big enough to be worth bridging?

CB set is read from engram_core.CLAIM_BEARING_TYPES rather than re-enumerated here
(the repo's own "derive from the classification, never re-enumerate it" rule).
NOTE a real name collision in the source: engram_revision.py defines a DIFFERENT
`CLAIM_BEARING_TYPES = frozenset({"axiom"})`. engram_core's is the canonical one.

Every arm prints its denominator.
"""
import argparse, glob, os, sqlite3, sys
from collections import defaultdict, Counter

import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import _ssot

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CB = {"observation_factual", "observation_predictive", "derivation", "theory", "axiom", "conjecture"}

def components(ids, edges):
    adj = defaultdict(set)
    kept = 0
    for s, t in edges:
        if s in ids and t in ids:
            adj[s].add(t); adj[t].add(s); kept += 1
    seen, comps = set(), []
    for n in sorted(ids):
        if n in seen: continue
        stack, members = [n], []
        seen.add(n)
        while stack:
            x = stack.pop(); members.append(x)
            for y in adj.get(x, ()):
                if y not in seen: seen.add(y); stack.append(y)
        comps.append(members)
    comps.sort(key=lambda m: (-len(m), min(m)))
    return comps, kept

def main():
    ap = argparse.ArgumentParser(); _ssot.add_db_arg(ap)
    a = ap.parse_args()
    db = _ssot.resolve_db(a.db, allow_unpinned=a.allow_unpinned)
    c = _ssot.connect(db)
    ntype = {i: t for i, t in c.execute("SELECT id, type FROM nodes WHERE is_current=1")}
    edges = c.execute("SELECT source_id, target_id FROM edges").fetchall()
    print(f"# source: {os.path.relpath(db, REPO)}\n")

    print("## Q1 — does the CB/NCB split change the giant-component share?\n")
    print(f"  {'population':<34}{'nodes':>8}{'edges':>8}{'largest':>9}{'share':>8}{'comps':>7}{'isolated':>9}")
    arms = [
        ("ALL current nodes",            set(ntype)),
        ("CB only (claim-bearing)",      {i for i, t in ntype.items() if t in CB}),
        ("NCB only",                     {i for i, t in ntype.items() if t not in CB}),
        ("CB + evidence only",           {i for i, t in ntype.items() if t in CB or t == "evidence"}),
        ("ALL minus evidence",           {i for i, t in ntype.items() if t != "evidence"}),
    ]
    for label, ids in arms:
        comps, kept = components(ids, edges)
        iso = sum(1 for m in comps if len(m) == 1)
        print(f"  {label:<34}{len(ids):>8,}{kept:>8,}{len(comps[0]):>9,}"
              f"{100.0*len(comps[0])/len(ids):>7.1f}%{len(comps):>7,}{iso:>9,}")

    print("\n## Q2 — anatomy of everything outside the main continent (ALL current nodes)\n")
    comps, _ = components(set(ntype), edges)
    giant, rest = comps[0], comps[1:]
    outside = sum(len(m) for m in rest)
    print(f"  giant component        {len(giant):,} / {len(ntype):,}")
    print(f"  outside it             {outside:,} nodes in {len(rest):,} components\n")
    buckets = [(1,1,"singletons"),(2,2,"pairs"),(3,5,"3-5"),(6,10,"6-10"),
               (11,25,"11-25"),(26,50,"26-50"),(51,100,"51-100"),(101,10**9,"101+")]
    print(f"  {'size':<14}{'comps':>7}{'nodes':>9}{'% of outside':>14}")
    for lo, hi, lab in buckets:
        sel = [m for m in rest if lo <= len(m) <= hi]
        n = sum(len(m) for m in sel)
        if sel:
            print(f"  {lab:<14}{len(sel):>7,}{n:>9,}{100.0*n/outside:>13.1f}%")
    print(f"\n  largest NON-giant components (is there a secondary island worth bridging?):")
    for m in rest[:6]:
        types = sorted(Counter(ntype[x] for x in m).items(), key=lambda kv: (-kv[1], kv[0]))[:3]
        print(f"    {len(m):>4} nodes  " + ", ".join(f"{t}:{k}" for t, k in types))
    print(f"\n  what is OUTSIDE, by node type (numerator / that type's total):")
    out_ids = {x for m in rest for x in m}
    tot = Counter(ntype.values())
    for t, n in sorted(Counter(ntype[x] for x in out_ids).items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"    {t:<24}{n:>6,} / {tot[t]:<6,} = {100.0*n/tot[t]:5.1f}% of that type")

    q3_pair_age(c, ntype, giant, rest)


def q3_pair_age(c, ntype, giant, rest):
    """Lei's question, 2026-10-12: are the evidence+observation pairs the recency
    frontier, i.e. clearly fresher than observations inside the continent?

    Age = days before the snapshot's newest current created_at. Compared against
    every observation in the giant component, and against the giant's observations
    that sit on no derives_from edge (recorded but never reasoned from), so that
    "recent" and "unreasoned" are not read as one property.
    """
    from datetime import datetime, timezone
    OBS = {"observation_factual", "observation_predictive"}

    def ts(s):
        d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)

    ctime = {i: ts(s) for i, s in c.execute("SELECT id, created_at FROM nodes WHERE is_current=1")}
    ref = max(ctime.values())
    rel = c.execute("SELECT source_id, target_id, relation FROM edges").fetchall()
    in_df = {x for s, t, r in rel if r == "derives_from" for x in (s, t)}
    pair_obs = []
    for m in rest:
        if len(m) == 2 and sorted(ntype[x] in OBS for x in m) == [False, True] \
                and any(ntype[x] == "evidence" for x in m):
            pair_obs.append(next(x for x in m if ntype[x] in OBS))
    giant_obs = [x for x in giant if ntype[x] in OBS]
    giant_unreasoned = [x for x in giant_obs if x not in in_df]

    def ages(ids):
        return sorted((ref - ctime[x]).total_seconds() / 86400 for x in ids)

    def median(v):
        n = len(v)
        return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2

    def p_younger(x, y):  # P(random x younger than random y), ties count half
        ys, below, eq = sorted(y), 0, 0
        import bisect
        for v in x:
            lo, hi = bisect.bisect_left(ys, v), bisect.bisect_right(ys, v)
            below += len(ys) - hi
            eq += hi - lo
        return (below + 0.5 * eq) / (len(x) * len(y))

    print(f"\n## Q3 — are the evidence+observation pairs the recency frontier?\n")
    print(f"  age reference (newest current created_at): {ref.isoformat()}")
    print(f"  {'population':<40}{'n':>6}{'median d':>10}{'newest 4w':>11}{'>8w':>8}{'>12w':>8}")
    A = ages(pair_obs)
    for label, v in (("pair observations", A),
                     ("giant observations (all)", ages(giant_obs)),
                     ("giant obs on no derives_from edge", ages(giant_unreasoned))):
        n = len(v)
        f = lambda pred: sum(1 for d in v if pred(d))
        print(f"  {label:<40}{n:>6,}{median(v):>10.1f}{f(lambda d: d <= 28)/n:>10.1%}"
              f"{f(lambda d: d > 56):>8,}{f(lambda d: d > 84):>8,}")
    print(f"\n  P(pair obs younger than a giant obs)              = {p_younger(A, ages(giant_obs)):.3f}  (0.5 = no difference)")
    print(f"  P(pair obs younger than an unreasoned giant obs)  = {p_younger(A, ages(giant_unreasoned)):.3f}")
    sup = {x for s, t, r in rel if r == "supersedes" for x in (s, t)}
    k = sum(1 for x in pair_obs if x in sup)
    print(f"\n  control: pair obs on a supersedes edge = {k} / {len(pair_obs)}"
          f" (fresh created_at over older content; biases the pairs toward looking younger)")
    by_m = Counter(ctime[x].strftime("%Y-%m") for x in pair_obs)
    by_g = Counter(ctime[x].strftime("%Y-%m") for x in giant_obs)
    print(f"\n  pair share of each month's observations:")
    for mth in sorted(set(by_m) | set(by_g)):
        print(f"    {mth}  {by_m[mth]:>4} / {by_m[mth] + by_g[mth]:>5}  = {by_m[mth]/(by_m[mth] + by_g[mth]):5.1%}")

if __name__ == "__main__":
    main()
