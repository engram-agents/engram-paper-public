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

Usage:  python3 tools/paper_stats.py [--db data/engram-paper-ssot-<stamp>.db]
        python3 tools/paper_stats.py --trace <node_id> [--trace <node_id> ...]
        python3 tools/paper_stats.py --trace-deepest [--json]

`--trace` / `--trace-deepest` print a per-step confidence chain instrument
instead of the full report above (Ch6 §6.4's worked-chain figures come from
this mode; see that section for the numbers themselves -- this script does
not embed them, since they are read off the pinned snapshot the parent's
colleague holds, not this seat's).

TRACE METHOD, ported from `/home/agent-borges/borges-desk/
paper-chain-trace-2026-09-23.py` (Borges's uncommitted desk script) --
faithfully for depth() and the per-step tie-break, with three DELIBERATE
DEPARTURES:

  1. `trace()` here tracks the ids already emitted and stops the walk the
     moment the chosen next-parent is already in that set, rather than
     looping forever. The reference script's own `trace()` has no such
     guard and enters an infinite loop on a genuine cycle (e.g. two nodes
     that are each other's sole `derives_from` parent) -- `depth()`'s
     memoized cycle guard prevents *depth* from diverging, but nothing in
     the reference `trace()` reuses that guard for the *walk* itself.
  2. `--trace-deepest`'s tie-break is documented here as LOWEST id among
     nodes at the max depth. The reference script's `sorted(..., reverse=True)`
     over `(depth, id)` tuples picks the HIGHEST id on a tie. Either is a
     defensible convention; this instrument picks lowest-id for
     determinism-toward-the-start-of-the-alphabet and states it here so a
     reader porting numbers between the two scripts knows to check which
     one produced a given trace.
  3. `n_premises` and `min_premise_conf` (in `_node_row`) count only
     NON-self-loop parents -- consistent with this module's own parents(n)
     definition below, which excludes self-loops. The reference script's
     `info()` computes both from `parents.get(n, [])` UNFILTERED, so on a
     node with a self-referencing `derives_from` edge plus one real parent
     the reference reports `n_premises=2` where this instrument reports 1.
     Deliberate, not an oversight: a self-loop is not a premise.

One more divergence worth naming though it is not a design choice, just a
difference in strictness: `_node_row` treats malformed `metadata` JSON as
`{}` (so `reasoning_type` reads as absent rather than the row erroring);
the reference script's `info()` calls `json.loads(r[2] or '{}')` directly
on the metadata column, with no try/except, and would raise on the same
malformed input.

Depth, parents and the per-step selection rule are otherwise unchanged from
the reference script:

  parents(n)  = target_ids of `derives_from` edges out of n, restricted to
                edges where BOTH endpoints are current nodes (is_current=1),
                excluding self-loops.
  depth(n)    = 0 if parents(n) is empty, else 1 + max(depth(p) for p in
                parents(n)); a node already on the current recursion path
                contributes 0 (memoized cycle guard -- terminates on a
                cyclic fixture, ported as-is from the reference script).
  trace(n)    = walk from n down, at each step choosing the parent p in
                parents(current) that maximizes (depth(p), -confidence(p))
                -- i.e. deepest parent first, ties broken by LOWEST
                confidence. This is the reference script's own key,
                unchanged.
"""
import argparse, glob, json, os, sqlite3, statistics, sys
from collections import Counter, defaultdict

import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import _ssot

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


def _build_graph(c):
    """(conf, parents) over current nodes, for --trace mode. Deliberately NOT
    shared with the §6.4 report section below, which builds its own
    equivalent inline (out of scope for this change -- see spec-trace.md;
    touching it would risk the byte-identical-output guarantee for a
    no-flag run). conf: id -> confidence|None, current nodes only. parents:
    id -> [id, ...], both endpoints current, self-loops excluded."""
    conf = {i: cf for i, cf in c.execute("SELECT id, confidence FROM nodes WHERE is_current=1")}
    parents = defaultdict(list)
    for s_, t_ in c.execute("SELECT source_id, target_id FROM edges WHERE relation='derives_from'"):
        if s_ in conf and t_ in conf and s_ != t_:
            parents[s_].append(t_)
    return conf, parents


def _make_depth_fn(parents):
    memo = {}
    def depth(n, seen=frozenset()):
        if n in memo: return memo[n]
        if n in seen: return 0                      # cycle guard
        ps = [p for p in parents.get(n, []) if p != n]
        d = 0 if not ps else 1 + max(depth(p, seen | {n}) for p in ps)
        memo[n] = d
        return d
    return depth


def _trace_chain(n, parents, conf, depth):
    """Walk from n down, deepest-parent-first (ties -> lowest confidence).
    Departure from the reference script: stops once the chosen next parent
    is already in this trace, instead of looping forever on a cycle."""
    out = []
    emitted = set()
    while True:
        out.append(n)
        emitted.add(n)
        ps = sorted(p for p in parents.get(n, []) if p != n)   # id order: the tie-break below
        if not ps:
            break
        # max() keeps the FIRST of equal keys, so with ps in id order a full tie (same depth,
        # same confidence) resolves to the lowest id - not to whichever edge the scan met first.
        nxt = max(ps, key=lambda p: (depth(p), -(conf.get(p) or 0)))
        if nxt in emitted:
            break                                    # cycle guard for the walk
        n = nxt
    return out


def _node_row(c, n, parents, conf, depth):
    r = c.execute("SELECT type, claim, metadata FROM nodes WHERE id=?", (n,)).fetchone()
    type_, claim, metadata = r
    md = {}
    if metadata:
        try: md = json.loads(metadata)
        except Exception: md = {}
    reasoning_type = md.get("reasoning_type") or md.get("derivation_mode")
    ps = [p for p in parents.get(n, []) if p != n]
    pc = [conf[p] for p in ps if conf.get(p) is not None]
    cv = conf.get(n)
    return {
        "id": n,
        "depth": depth(n),
        "type": type_,
        "reasoning_type": reasoning_type,
        "confidence": round(cv, 3) if cv is not None else None,
        "n_premises": len(ps),
        "min_premise_conf": round(min(pc), 3) if pc else None,
        "claim": (claim or "")[:150],
    }


def _deepest_start(conf, depth):
    """Max-depth current node; ties -> lowest id (see module docstring)."""
    max_d = max(depth(n) for n in conf)
    candidates = [n for n in conf if depth(n) == max_d]
    return min(candidates)


def _run_trace(c, starts, as_json):
    conf, parents = _build_graph(c)
    depth = _make_depth_fn(parents)

    # validate ALL requested ids before printing anything, so an invalid id
    # anywhere in the list produces nothing on stdout (error contract).
    for start in starts:
        if start not in conf:
            print(f"no current node {start}", file=sys.stderr)
            return 2

    blocks = []
    for start in starts:
        chain = _trace_chain(start, parents, conf, depth)
        rows = [_node_row(c, n, parents, conf, depth) for n in chain]
        blocks.append({"start": start, "depth": depth(start), "rows": rows})

    if as_json:
        print(json.dumps({"traces": blocks}))
    else:
        for b in blocks:
            print(f"==== {b['start']} depth={b['depth']}")
            for row in b["rows"]:
                cf = row["confidence"]
                mn = row["min_premise_conf"]
                print(
                    f"{row['id']:8} d={row['depth']:2} {str(row['type'])[:14]:14} "
                    f"{str(row['reasoning_type']):28} conf={cf} prem={row['n_premises']} "
                    f"minprem={mn} | {row['claim']}"
                )
    return 0


def main():
    ap = argparse.ArgumentParser()
    _ssot.add_db_arg(ap)
    ap.add_argument("--trace", action="append", default=[], metavar="NODE_ID",
                     help="print a per-step confidence chain from NODE_ID down to its roots; repeatable")
    ap.add_argument("--trace-deepest", action="store_true",
                     help="trace from the max-depth current node (ties -> lowest id)")
    ap.add_argument("--json", action="store_true",
                     help="with --trace/--trace-deepest, emit {\"traces\": [...]} instead of text")
    a = ap.parse_args()
    db = _ssot.resolve_db(a.db, allow_unpinned=a.allow_unpinned)
    c = _ssot.connect(db)

    if a.trace or a.trace_deepest:
        starts = list(a.trace)
        if a.trace_deepest:
            conf, _parents = _build_graph(c)
            depth = _make_depth_fn(_parents)
            starts.append(_deepest_start(conf, depth))
        sys.exit(_run_trace(c, starts, a.json))

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
    for t, n in c.execute("SELECT type,COUNT(*) FROM nodes WHERE is_current=1 GROUP BY 1 ORDER BY 2 DESC, 1"):
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
    for rt, vals in sorted(buckets.items(), key=lambda kv: (-len(kv[1]), str(kv[0]))):
        print(f"  {rt:<34}{len(vals):>7,}{dv_total:>9,}{statistics.fmean(vals):>8.2f}")
    print()

    print("## §6.1 Confidence by quote_type — current observations")
    ob_total = c.execute("SELECT COUNT(*) FROM nodes WHERE is_current=1 AND type LIKE 'observation%'").fetchone()[0]
    print(f"  {'quote_type':<34}{'n':>7}{'/ obs':>9}{'mean':>8}")
    for qt, n, mean in c.execute(
            "SELECT quote_type, COUNT(*), AVG(confidence) FROM nodes "
            "WHERE is_current=1 AND type LIKE 'observation%' AND quote_type IS NOT NULL "
            "AND confidence IS NOT NULL GROUP BY 1 ORDER BY 3 DESC, 1"):
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
