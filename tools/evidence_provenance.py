#!/usr/bin/env python3
"""How much of this graph's knowledge is rooted in the agent's own experience?

Lei's questions, 2026-09-20:
  (1) Connectivity with only TRANSCRIPT evidence retained, beside ALL and
      CB+all-evidence — what do the chatlogs specifically contribute to gluing?
  (2) The ratio of claim-bearing nodes rooted in transcript evidence — how much
      held knowledge is first-hand experience versus external sources?

TWO INDEPENDENT AXES ARE REPORTED, deliberately, because they come from different
upstreams and can therefore check each other:

  AXIS 1  evidence source_url shape   — what KIND of artifact the claim cites
  AXIS 2  observation `source_class`  — what the AUTHOR declared the claim to be
                                        (introspective / external / user_stated)

Axis 1 is structural and cannot be mis-declared; axis 2 is hand-typed and could be.
If they disagree sharply that is a finding about the declaration discipline, not a
bug in either. They measure overlapping but non-identical things, so exact agreement
is NOT expected and would itself be suspicious.

TRANSCRIPT classification: any evidence whose source_url ends `.jsonl` — the session
transcripts, both raw `~/.claude/projects/…` paths and content-hashed snapshots under
`evidence-archive/`. Verified by sampling both shapes.
"""
import argparse, glob, json, os, sqlite3
from collections import defaultdict, Counter

import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import _ssot

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CB = {"observation_factual", "observation_predictive", "derivation", "theory", "axiom", "conjecture"}

URL_CLASS_PREFIX = "redacted:"
URL_CLASSES = ("transcript", "external", "file")

def ev_class(url, stype):
    u = url or ""
    # The stripped public release (tools/strip_paper_snapshot.py) replaces every source_url
    # with `redacted:<class>`, the class THIS function computed for the raw URL. Reading the
    # token back keeps the per-node class identical on the full and the stripped file.
    if u.startswith(URL_CLASS_PREFIX):
        cls = u[len(URL_CLASS_PREFIX):]
        if cls not in URL_CLASSES:
            raise ValueError(f"unknown redacted source_url class token: {cls!r}")
        return cls
    if u.endswith(".jsonl"): return "transcript"
    if stype == "conversation": return "transcript"
    if stype == "web_page": return "external"
    return "file"

def ranked(counter):
    """[(label, count)] by count descending, ties by label ascending. A TOTAL order:
    `Counter.most_common()` leaves tied labels in first-seen order, which is the order the
    database happened to return rows in - and that depends on the query plan."""
    return sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0])))

def lcc(ids, edges):
    adj = defaultdict(set); kept = 0
    for s, t in edges:
        if s in ids and t in ids: adj[s].add(t); adj[t].add(s); kept += 1
    seen, best, comps, iso = set(), 0, 0, 0
    for n in ids:
        if n in seen: continue
        comps += 1; st = [n]; seen.add(n); sz = 0
        while st:
            x = st.pop(); sz += 1
            for y in adj.get(x, ()):
                if y not in seen: seen.add(y); st.append(y)
        if sz == 1: iso += 1
        best = max(best, sz)
    return best, comps, iso, kept

def main():
    ap = argparse.ArgumentParser(); _ssot.add_db_arg(ap)
    a = ap.parse_args()
    db = _ssot.resolve_db(a.db, allow_unpinned=a.allow_unpinned)
    c = _ssot.connect(db)
    print(f"# source: {os.path.relpath(db, REPO)}\n")

    ntype, evcls = {}, {}
    for i, t, u, st in c.execute("SELECT id, type, source_url, source_type FROM nodes WHERE is_current=1"):
        ntype[i] = t
        if t == "evidence": evcls[i] = ev_class(u, st)
    edges = c.execute("SELECT source_id, target_id, relation FROM edges").fetchall()
    und = [(s, t) for s, t, _ in edges]

    evtot = len(evcls)
    print("## Evidence by artifact kind (AXIS 1 — structural)")
    for k, v in ranked(Counter(evcls.values())):
        print(f"  {k:<14}{v:>6} / {evtot}  = {100.0*v/evtot:5.1f}%")
    print()

    cb_ids = {i for i, t in ntype.items() if t in CB}
    arms = [
        ("ALL current nodes",           set(ntype)),
        ("CB only",                     cb_ids),
        ("CB + ALL evidence",           cb_ids | set(evcls)),
        ("CB + TRANSCRIPT evidence",    cb_ids | {i for i, k in evcls.items() if k == "transcript"}),
        ("CB + EXTERNAL evidence",      cb_ids | {i for i, k in evcls.items() if k == "external"}),
        ("CB + FILE evidence",          cb_ids | {i for i, k in evcls.items() if k == "file"}),
    ]
    print("## Q1 — connectivity with each evidence kind added back to the claim graph")
    print(f"  {'population':<30}{'nodes':>8}{'largest':>9}{'share':>8}{'comps':>7}{'isolated':>9}")
    for label, ids in arms:
        b, comps, iso, _ = lcc(ids, und)
        print(f"  {label:<30}{len(ids):>8,}{b:>9,}{100.0*b/len(ids):>7.1f}%{comps:>7,}{iso:>9,}")
    print()

    # Q2 — what fraction of claims root in transcript evidence
    cites = defaultdict(set)
    for s, t, r in edges:
        if r == "cites" and t in evcls: cites[s].add(t)
    obs = {i for i, t in ntype.items() if t.startswith("observation")}
    direct = Counter()
    for o in obs:
        ks = {evcls[e] for e in cites.get(o, ())}
        if not ks: direct["(cites no evidence)"] += 1
        elif ks == {"transcript"}: direct["transcript only"] += 1
        elif "transcript" in ks: direct["mixed incl. transcript"] += 1
        else: direct["no transcript"] += 1
    print("## Q2a — observations by the KIND of evidence they cite (AXIS 1)")
    for k, v in ranked(direct):
        print(f"  {k:<26}{v:>6} / {len(obs)}  = {100.0*v/len(obs):5.1f}%")
    print()

    sc = Counter()
    for i, m in c.execute("SELECT id, metadata FROM nodes WHERE is_current=1 AND type LIKE 'observation%'"):
        try: sc[json.loads(m).get("source_class", "(absent)") if m else "(null)"] += 1
        except Exception: sc["(unparseable)"] += 1
    tot = sum(sc.values())
    print("## Q2b — observations by DECLARED source_class (AXIS 2 — author-typed)")
    for k, v in ranked(sc):
        print(f"  {k:<26}{v:>6} / {tot}  = {100.0*v/tot:5.1f}%")
    print()
    print("## The two axes side by side — they measure different things; read the GAP, not a match.")
    tr = direct['transcript only'] + direct['mixed incl. transcript']
    print(f"  cites a transcript (structural)     {tr:>6} / {len(obs)} = {100.0*tr/len(obs):5.1f}%")
    print(f"  declared introspective (author)     {sc.get('introspective',0):>6} / {tot} = "
          f"{100.0*sc.get('introspective',0)/tot:5.1f}%")
    print(f"  declared introspective+user_stated  {sc.get('introspective',0)+sc.get('user_stated',0):>6} / {tot} = "
          f"{100.0*(sc.get('introspective',0)+sc.get('user_stated',0))/tot:5.1f}%")

if __name__ == "__main__":
    main()
