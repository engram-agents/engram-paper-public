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

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CB = {"observation_factual", "observation_predictive", "derivation", "theory", "axiom", "conjecture"}

def components(ids, edges):
    adj = defaultdict(set)
    kept = 0
    for s, t in edges:
        if s in ids and t in ids:
            adj[s].add(t); adj[t].add(s); kept += 1
    seen, comps = set(), []
    for n in ids:
        if n in seen: continue
        stack, members = [n], []
        seen.add(n)
        while stack:
            x = stack.pop(); members.append(x)
            for y in adj.get(x, ()):
                if y not in seen: seen.add(y); stack.append(y)
        comps.append(members)
    comps.sort(key=len, reverse=True)
    return comps, kept

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--db", default=None)
    a = ap.parse_args()
    db = a.db or sorted(glob.glob(os.path.join(REPO, "dataset", "engram-paper-ssot-*.db")))[-1]
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
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
        types = Counter(ntype[x] for x in m).most_common(3)
        print(f"    {len(m):>4} nodes  " + ", ".join(f"{t}:{k}" for t, k in types))
    print(f"\n  what is OUTSIDE, by node type (numerator / that type's total):")
    out_ids = {x for m in rest for x in m}
    tot = Counter(ntype.values())
    for t, n in Counter(ntype[x] for x in out_ids).most_common():
        print(f"    {t:<24}{n:>6,} / {tot[t]:<6,} = {100.0*n/tot[t]:5.1f}% of that type")

if __name__ == "__main__":
    main()
