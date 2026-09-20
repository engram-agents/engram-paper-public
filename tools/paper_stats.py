#!/usr/bin/env python3
"""Regenerate every live-graph number Chapter 6 reports, from the frozen paper SSoT.

Lei's ruling, 2026-09-20: the instruments that produce the paper's numbers are
checked in, so a reader can see exactly how each figure was generated. This is
that instrument for Chapter 6. Run it, and the output IS the chapter's numeric
content -- no figure in ch6 should exist that this script cannot reproduce.

DISCIPLINE, taken from ch6's own planned-rewrite section: every measurement
prints its DENOMINATOR beside its numerator. A wrong corpus then announces
itself in the same output that carries the answer (`0 / 0`) instead of arriving
as a bare, plausible number.

Usage:  python3 tools/paper_stats.py [--db dataset/engram-paper-ssot-<stamp>.db]
"""
import argparse, glob, json, os, sqlite3, statistics, sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def pct(nom, den):
    return f"{100.0*nom/den:.1f}%" if den else "n/a (denominator 0)"

def quantiles(vals):
    v = sorted(vals)
    if not v:
        return {}
    def q(p):
        if len(v) == 1: return v[0]
        i = p * (len(v) - 1); lo = int(i); hi = min(lo + 1, len(v) - 1)
        return v[lo] + (v[hi] - v[lo]) * (i - lo)
    return {"n": len(v), "mean": statistics.fmean(v), "median": q(0.5),
            "p25": q(0.25), "p75": q(0.75), "min": v[0], "max": v[-1]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=None)
    a = ap.parse_args()
    db = a.db
    if db is None:
        cands = sorted(glob.glob(os.path.join(REPO, "dataset", "engram-paper-ssot-*.db")))
        if not cands:
            sys.exit("no SSoT snapshot found in dataset/ — run tools/freeze_paper_snapshot.py first")
        if len(cands) > 1:
            print(f"# NOTE: {len(cands)} SSoT snapshots present; using the newest. "
                  f"The paper's SSoT is named in dataset/DATASET.md — check they agree.", file=sys.stderr)
        db = cands[-1]
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    print(f"# source: {os.path.relpath(db, REPO)}")
    print(f"# every figure below is computed from that file and nothing else\n")

    total = c.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
    cur   = c.execute("SELECT COUNT(*) FROM nodes WHERE is_current=1").fetchone()[0]
    lo, hi = c.execute("SELECT MIN(created_at), MAX(created_at) FROM nodes").fetchone()
    print("## Graph at a glance")
    print(f"  current nodes            {cur:,} / {total:,} total (superseded+retracted = {total-cur:,})")
    print(f"  edges                    {c.execute('SELECT COUNT(*) FROM edges').fetchone()[0]:,}")
    print(f"  first node               {lo}")
    print(f"  last node                {hi}\n")

    print("## Node census (current)")
    for t, n in c.execute("SELECT type,COUNT(*) FROM nodes WHERE is_current=1 GROUP BY 1 ORDER BY 2 DESC"):
        print(f"  {t:<24} {n:>6,} / {cur:,}")
    print()

    print("## §6.1 Confidence by node type — current, confidence NOT NULL")
    print(f"  {'type':<24}{'n':>7}{'mean':>8}{'median':>8}{'p25':>8}{'p75':>8}")
    for t, in c.execute("SELECT DISTINCT type FROM nodes WHERE is_current=1 AND confidence IS NOT NULL ORDER BY 1"):
        vals = [r[0] for r in c.execute(
            "SELECT confidence FROM nodes WHERE is_current=1 AND type=? AND confidence IS NOT NULL", (t,))]
        s = quantiles(vals)
        if s: print(f"  {t:<24}{s['n']:>7,}{s['mean']:>8.2f}{s['median']:>8.2f}{s['p25']:>8.2f}{s['p75']:>8.2f}")
    print()

    print("## §6.1 Confidence by reasoning_type — current derivations")
    buckets = defaultdict(list)
    dv_total = 0
    for m, conf in c.execute(
            "SELECT metadata, confidence FROM nodes WHERE type='derivation' AND is_current=1"):
        dv_total += 1
        rt = "<absent>"
        if m:
            try: rt = json.loads(m).get("reasoning_type", "<absent>")
            except Exception: rt = "<unparseable>"
        if conf is not None: buckets[rt].append(conf)
    print(f"  {'reasoning_type':<34}{'n':>7}{'/ dvs':>9}{'mean':>8}")
    for rt, vals in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        print(f"  {rt:<34}{len(vals):>7,}{dv_total:>9,}{statistics.fmean(vals):>8.2f}")
    print()

    print("## §6.1 Confidence by quote_type — current observations")
    ob_total = c.execute("SELECT COUNT(*) FROM nodes WHERE is_current=1 AND type LIKE 'observation%'").fetchone()[0]
    print(f"  {'quote_type':<34}{'n':>7}{'/ obs':>9}{'mean':>8}")
    for qt, n, mean in c.execute(
            "SELECT quote_type, COUNT(*), AVG(confidence) FROM nodes "
            "WHERE is_current=1 AND type LIKE 'observation%' AND quote_type IS NOT NULL "
            "AND confidence IS NOT NULL GROUP BY 1 ORDER BY 3 DESC"):
        print(f"  {qt:<34}{n:>7,}{ob_total:>9,}{mean:>8.2f}")
    print()

    print("## §6.2 Non-modularity — largest connected component over the CURRENT node set")
    cur_ids = {r[0] for r in c.execute("SELECT id FROM nodes WHERE is_current=1")}
    adj = defaultdict(set); kept = dropped = 0
    for s, t in c.execute("SELECT source_id, target_id FROM edges"):
        if s in cur_ids and t in cur_ids:
            adj[s].add(t); adj[t].add(s); kept += 1
        else:
            dropped += 1
    seen, sizes = set(), []
    for n in cur_ids:
        if n in seen: continue
        stack, comp = [n], 0
        seen.add(n)
        while stack:
            x = stack.pop(); comp += 1
            for y in adj.get(x, ()):
                if y not in seen: seen.add(y); stack.append(y)
        sizes.append(comp)
    sizes.sort(reverse=True)
    print(f"  edges used               {kept:,} / {kept+dropped:,} (dropped {dropped:,}: an endpoint is not a current node)")
    print(f"  components               {len(sizes):,}")
    print(f"  largest component        {sizes[0]:,} / {len(cur_ids):,} nodes = {pct(sizes[0], len(cur_ids))}")
    print(f"  isolated (size 1)        {sum(1 for s in sizes if s==1):,} / {len(cur_ids):,}")
    print(f"  next four components     {', '.join(str(s) for s in sizes[1:5]) or '(none)'}\n")

    print("## §6.4 Derivation chain depth — longest derives_from path to a root, current nodes")
    from collections import deque
    conf = {i: cf for i, cf in c.execute("SELECT id, confidence FROM nodes WHERE is_current=1")}
    parents = defaultdict(list)
    n_edges = 0
    for s_, t_ in c.execute("SELECT source_id, target_id FROM edges WHERE relation='derives_from'"):
        if s_ in conf and t_ in conf:
            parents[s_].append(t_); n_edges += 1
    memo = {}
    def depth(n, seen=frozenset()):
        if n in memo: return memo[n]
        if n in seen: return 0                      # cycle guard
        ps = [p for p in parents.get(n, []) if p != n]
        d = 0 if not ps else 1 + max(depth(p, seen | {n}) for p in ps)
        memo[n] = d
        return d
    ranked = sorted(((depth(n), n) for n in conf), reverse=True)
    print(f"  derives_from edges used  {n_edges:,} (both endpoints current)")
    print(f"  max depth                {ranked[0][0]}")
    print(f"  {'depth':>6}  {'node':<10}{'conf':>7}   claim")
    for d, n in ranked[:5]:
        cl = (c.execute("SELECT claim FROM nodes WHERE id=?", (n,)).fetchone()[0] or "")[:64]
        cv = conf[n]
        print(f"  {d:>6}  {n:<10}{(f'{cv:.2f}' if cv is not None else '  -- '):>7}   {cl}")
    print()

    print("## §6.5 Metacognitive surface — the agent's own weakest live beliefs")
    open_q = c.execute("SELECT COUNT(*) FROM nodes WHERE is_current=1 AND type='question' AND (status IS NULL OR status NOT IN ('resolved','answered'))").fetchone()[0]
    all_q  = c.execute("SELECT COUNT(*) FROM nodes WHERE is_current=1 AND type='question'").fetchone()[0]
    print(f"  open questions           {open_q:,} / {all_q:,} current questions")
    print(f"  {'lowest-confidence current derivations':<44}")
    for nid, conf, claim in c.execute(
            "SELECT id, confidence, claim FROM nodes WHERE is_current=1 AND type='derivation' "
            "AND confidence IS NOT NULL ORDER BY confidence ASC, id ASC LIMIT 5"):
        print(f"    {nid}  {conf:.2f}  {(claim or '')[:88]}")
    print()

if __name__ == "__main__":
    main()
