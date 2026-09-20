#!/usr/bin/env python3
"""Giant-component share over the graph's lifetime, reconstructed from the frozen SSoT.

Chapter 6 §6.2 claims a measured 87.3% of nodes sit in one connected component,
as the paper's empirical evidence for non-modularity (OCC Constraint D). That
figure was measured 2026-05-10 on 3,198 current nodes; an earlier April run on
748 nodes gave 94.4%. On the 2026-09-20 SSoT the same measurement gives 77.6%.
Three points, all declining. This script turns that into a curve so the chapter
can say what is actually happening instead of swapping one number for a worse one.

METHOD, and its limitation stated first because it is the thing a reader must
weigh. This is a RETROSPECTIVE RECONSTRUCTION, not a series of contemporaneous
measurements: for each cut date it takes the nodes and edges in the frozen
snapshot whose `created_at` precedes that date, and computes the largest
connected component over them. That means:

  - Nodes later superseded or retracted are INCLUDED at a past cut, because they
    existed then. (`is_current` is a property of NOW, not of the cut date, so
    filtering on it would be an anachronism.)
  - Anything hard-deleted from the graph between then and the freeze is ABSENT
    and cannot be recovered from this snapshot.
  - Edges added later between two old nodes are EXCLUDED, correctly, since edges
    carry their own `created_at`.

So the reconstruction is faithful for everything that survived to the freeze, and
blind to anything that did not. The `--validate-git` control exists because that
blindness is the one assumption worth testing rather than asserting.

Usage:
  python3 tools/connectivity_trend.py [--db PATH] [--step-days 7]
  python3 tools/connectivity_trend.py --validate-git <commit-ish>
"""
import argparse, glob, os, sqlite3, subprocess, sys, tempfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def lcc_share(nodes, edges):
    """Largest-component size, component count, isolate count over a node/edge set."""
    adj = defaultdict(set)
    for s, t in edges:
        if s in nodes and t in nodes:
            adj[s].add(t); adj[t].add(s)
    seen, best, comps, iso = set(), 0, 0, 0
    for n in nodes:
        if n in seen: continue
        comps += 1; stack=[n]; seen.add(n); sz=0
        while stack:
            x = stack.pop(); sz += 1
            for y in adj.get(x, ()):
                if y not in seen: seen.add(y); stack.append(y)
        if sz == 1: iso += 1
        best = max(best, sz)
    return best, comps, iso

def default_db():
    c = sorted(glob.glob(os.path.join(REPO, "dataset", "engram-paper-ssot-*.db")))
    if not c: sys.exit("no SSoT snapshot in dataset/ — run tools/freeze_paper_snapshot.py")
    return c[-1]

def trend(db, step_days):
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    nodes = c.execute("SELECT id, created_at FROM nodes WHERE created_at IS NOT NULL").fetchall()
    edges = c.execute("SELECT source_id, target_id, created_at FROM edges WHERE created_at IS NOT NULL").fetchall()
    n_no_date = c.execute("SELECT COUNT(*) FROM nodes WHERE created_at IS NULL").fetchone()[0]
    e_no_date = c.execute("SELECT COUNT(*) FROM edges WHERE created_at IS NULL").fetchone()[0]
    c.close()

    print(f"# source: {os.path.relpath(db, REPO)}")
    print(f"# retrospective reconstruction by created_at — see module docstring for what it cannot see")
    if n_no_date or e_no_date:
        print(f"# EXCLUDED for having no created_at: {n_no_date} nodes, {e_no_date} edges "
              f"(these are invisible to every row below, at every date)")
    else:
        print(f"# every node and edge carries a created_at, so nothing is excluded for missing dates")

    lo = min(n[1] for n in nodes)[:10]
    hi = max(n[1] for n in nodes)[:10]
    d0 = datetime.strptime(lo, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    d1 = datetime.strptime(hi, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    print(f"# span {lo} .. {hi}, step {step_days}d\n")
    print(f"{'date':<12}{'nodes':>8}{'edges':>8}{'largest':>9}{'share':>8}{'comps':>7}{'isolated':>9}")

    rows = []
    d = d0
    while d <= d1 + timedelta(days=step_days):
        cut = d.strftime("%Y-%m-%d")
        ns = {i for i, ca in nodes if ca[:10] <= cut}
        es = [(s, t) for s, t, ca in edges if ca[:10] <= cut]
        if len(ns) >= 2:
            best, comps, iso = lcc_share(ns, es)
            share = 100.0 * best / len(ns)
            print(f"{cut:<12}{len(ns):>8,}{len(es):>8,}{best:>9,}{share:>7.1f}%{comps:>7,}{iso:>9,}")
            rows.append((cut, len(ns), len(es), best, share, comps, iso))
        d += timedelta(days=step_days)
    return rows

def validate_git(db, commitish, engram_repo=os.path.expanduser("~/.engram")):
    """CONTROL: rebuild the graph from a real historical commit and compare.

    The reconstruction above is blind to anything hard-deleted before the freeze.
    This is the check that could catch that: load the ACTUAL knowledge.sql from a
    past commit, compute the same measure, and compare it against what the
    reconstruction predicts for that commit's date. Agreement bounds the deletion
    blindness; disagreement measures it. A reconstruction that has never been
    compared against a real past state is an assumption, not a measurement.
    """
    date = subprocess.check_output(
        ["git","-C",engram_repo,"show","-s","--format=%cI",commitish], text=True).strip()
    cut = date[:10]
    sql = subprocess.check_output(
        ["git","-C",engram_repo,"show",f"{commitish}:knowledge.sql"], text=True, errors="replace")
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "hist.db")
        h = sqlite3.connect(p)
        try:
            h.executescript(sql)
        except sqlite3.Error as e:
            print(f"  replay of {commitish}:knowledge.sql failed: {e}", file=sys.stderr)
            return
        hn = {r[0] for r in h.execute("SELECT id FROM nodes")}
        he = [(s,t) for s,t in h.execute("SELECT source_id,target_id FROM edges")]
        h.close()
    hb, hc, hi = lcc_share(hn, he)

    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    ns = {i for i, ca in c.execute("SELECT id,created_at FROM nodes WHERE created_at IS NOT NULL") if ca[:10] <= cut}
    es = [(s,t) for s,t,ca in c.execute("SELECT source_id,target_id,created_at FROM edges WHERE created_at IS NOT NULL") if ca[:10] <= cut]
    c.close()
    rb, rc, ri = lcc_share(ns, es)

    print(f"## CONTROL — real commit {commitish[:10]} ({cut}) vs reconstruction at the same cut\n")
    print(f"  {'':<16}{'nodes':>8}{'edges':>8}{'largest':>9}{'share':>8}")
    print(f"  {'real commit':<16}{len(hn):>8,}{len(he):>8,}{hb:>9,}{100.0*hb/len(hn):>7.1f}%")
    print(f"  {'reconstruction':<16}{len(ns):>8,}{len(es):>8,}{rb:>9,}{100.0*rb/len(ns):>7.1f}%")
    dn = len(ns) - len(hn)
    print(f"\n  node delta        {dn:+,}  ({'reconstruction sees MORE' if dn>0 else 'reconstruction sees FEWER' if dn<0 else 'identical'})")
    print(f"  share delta       {100.0*rb/len(ns) - 100.0*hb/len(hn):+.1f} percentage points")
    print(f"\n  A node deficit in the reconstruction is the deletion blindness the docstring names.")
    print(f"  A surplus means the commit predates nodes the snapshot dates earlier — check the cut boundary.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=None)
    ap.add_argument("--step-days", type=int, default=7)
    ap.add_argument("--validate-git", metavar="COMMITISH", default=None)
    a = ap.parse_args()
    db = a.db or default_db()
    if a.validate_git:
        validate_git(db, a.validate_git)
    else:
        trend(db, a.step_days)

if __name__ == "__main__":
    main()
