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
  python3 tools/connectivity_trend.py --trim-control [--json]
"""
import argparse, glob, json, os, sqlite3, subprocess, sys, tempfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import _ssot

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
    c = _ssot.connect(db)
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

def trim_recency(nodes, edges, cut_date):
    """Largest-component size, kept, before/after a recency cut.

    nodes: iterable of (id, created_at_str). edges: iterable of
    (src, dst, created_at_str). cut_date: "YYYY-MM-DD".

    keep = nodes with created_at[:10] <= cut_date. Returns
    (kept_count, trimmed_count, lcc_edges_in_window, lcc_all_edges) where the
    two lcc values are lcc_share(...)[0] (the largest-component SIZE, not a
    percentage) over the kept node set, computed with (a) only edges whose
    own created_at[:10] <= cut_date ("window" edges — the reconstruction as
    it would have looked AT the cut date) and (b) all edges regardless of
    their date. Both are reported because they can diverge: an edge dated
    AFTER the cut can still connect two nodes that are both kept, which (b)
    sees and (a) does not.
    """
    nodes = list(nodes)
    edges = list(edges)
    kept_ids = {i for i, ca in nodes if ca[:10] <= cut_date}
    trimmed_count = len(nodes) - len(kept_ids)
    window_edges = [(s, t) for s, t, ca in edges if ca[:10] <= cut_date]
    all_edges = [(s, t) for s, t, ca in edges]
    lcc_window = lcc_share(kept_ids, window_edges)[0]
    lcc_all = lcc_share(kept_ids, all_edges)[0]
    return (len(kept_ids), trimmed_count, lcc_window, lcc_all)


def trim_oldest_matched(nodes_sorted, edges, k):
    """Drop the k OLDEST nodes from a pre-sorted list; largest component
    over what remains, with all edges.

    nodes_sorted: list of (id, created_at) ascending by created_at. This
    function trusts the caller's order and does not re-sort — the tie-break
    rule for equal created_at values is the CALLER's responsibility when
    building nodes_sorted: sort by the FULL created_at timestamp first, id
    only as a tie-break for two nodes with an IDENTICAL timestamp — never by
    a day-truncated date. All real created_at values are full ISO
    timestamps, so day-truncating before comparing means two nodes sharing a
    calendar day get ordered by id prefix instead of by actual time-of-day,
    which silently drops the wrong one at a boundary day (measured against
    the real snapshot: the oldest-removed control at the newest-2-weeks size
    read 76.7% instead of 77.7% under a day-truncated key). Among nodes
    sharing the exact same full timestamp, the lexicographically-smaller id
    counts as older and is dropped first. edges: iterable of (src, dst) pairs (already
    date-filtered by the caller, or simply the full edge set — this
    function applies no date filter of its own, matching "with all edges").

    Returns (kept_count, lcc_all_edges) — lcc_all_edges is lcc_share(...)[0]
    (the largest-component SIZE) over the remaining (kept) node ids.
    """
    nodes_sorted = list(nodes_sorted)
    edges = list(edges)
    kept = nodes_sorted[k:]
    kept_ids = {i for i, _ in kept}
    lcc_all = lcc_share(kept_ids, edges)[0]
    return (len(kept_ids), lcc_all)


def trim_control(db, recency_weeks=(6, 8, 12), control_weeks=(2, 4, 8)):
    """Ch6 §6.2's two trim arms, as one re-runnable instrument.

    RECENCY arm (trim the newest N weeks): at each cut, reports BOTH the
    window-edges share (`share_window_pct`, edges dated on/before the cut)
    and the all-edges share (`share_all_pct`, every edge regardless of
    date). These are not interchangeable and the paper's printed numbers
    use the window-edges value as primary: measured on the 2026-09-20
    snapshot, the two agree at 6 and 8 weeks (87.0%, 87.4%) but diverge at
    12 weeks — 87.1% window vs 87.9% all — because an edge dated after the
    12-week cut still links two nodes that are both kept at that cut.
    `share_window_pct` is the number Ch6 §6.2 prints; `share_all_pct` is
    reported alongside so the divergence itself is checkable rather than
    silently picked for you.

    CONTROL arm (matched node count, both ends): for each control week w,
    k = the number of nodes newer than the w-week-back cut. The
    newest-removed reading IS trim_recency's own reading at that same cut
    (`recency_share_window_pct` / `recency_share_all_pct` — trimming
    everything newer than the cut is exactly "remove the newest k nodes").
    The oldest-removed reading drops the k oldest nodes instead
    (`trim_oldest_matched`) and reports a single
    `control_share_pct` over all edges — there is no window/all distinction
    for that arm, because the kept nodes there are the NEWEST ones, so an
    edge connecting two of them is, by construction, never older than either
    endpoint's own creation and the window/all edge sets coincide.

    The oldest-removed reading's SORT KEY (full created_at timestamp, id
    only as a tie-break — see `trim_oldest_matched`'s docstring) is part of
    this instrument's definition, not an implementation detail: the
    control's DIRECTION holds under either a day-truncated or a
    full-timestamp key (both 76.7% and 77.7% sit well below the recency
    arm's 82.4% at the same matched size), but its LEVEL at the
    newest-2-weeks size moves a full percentage point depending on how
    same-day nodes are tie-broken. Measured against the real snapshot: a
    day-truncated key reads 76.7%, the full-timestamp key reads 77.7%.

    Loads nodes (id, created_at) and edges (source_id, target_id,
    created_at) via `_ssot.connect(db)`, excluding any row with a NULL
    created_at entirely (matching Borges's reference script) — such rows
    are invisible to every computation below, not merely to the recency
    cut. hi = the latest (max) created_at date among the loaded nodes.

    Returns a JSON-serialisable dict:
      {"hi": "YYYY-MM-DD",
       "recency": {w: {cut, kept, trimmed, lcc_window, lcc_all,
                        share_window_pct, share_all_pct}, ...},
       "control": {w: {cut, k, recency_kept, recency_trimmed,
                        recency_lcc_window, recency_lcc_all,
                        recency_share_window_pct, recency_share_all_pct,
                        control_kept, control_lcc_all,
                        control_share_pct}, ...}}
    Shares are percentages rounded to 1 decimal. `k` (control arm) and
    `trimmed` (recency arm, same cut) are always equal by construction —
    both count nodes newer than the same cut date.
    """
    c = _ssot.connect(db)
    nodes = c.execute("SELECT id, created_at FROM nodes WHERE created_at IS NOT NULL").fetchall()
    edges = c.execute(
        "SELECT source_id, target_id, created_at FROM edges WHERE created_at IS NOT NULL"
    ).fetchall()
    c.close()

    hi_str = max(ca for _, ca in nodes)[:10]
    hi = datetime.strptime(hi_str, "%Y-%m-%d")
    all_edge_pairs = [(s, t) for s, t, _ in edges]
    # Full created_at timestamp first, id only as a tie-break for identical
    # timestamps — NOT day-truncated. All real created_at values are full
    # ISO timestamps, so truncating to the day before comparing means two
    # nodes sharing a calendar day get ordered by id prefix rather than by
    # actual time-of-day, silently dropping the wrong one at a boundary day.
    nodes_sorted = sorted(nodes, key=lambda x: (x[1], x[0]))

    def _share(lcc, kept):
        return round(100.0 * lcc / kept, 1) if kept else 0.0

    result = {"hi": hi_str, "recency": {}, "control": {}}

    for w in recency_weeks:
        cut = (hi - timedelta(weeks=w)).strftime("%Y-%m-%d")
        kept, trimmed, lcc_window, lcc_all = trim_recency(nodes, edges, cut)
        result["recency"][w] = {
            "cut": cut,
            "kept": kept,
            "trimmed": trimmed,
            "lcc_window": lcc_window,
            "lcc_all": lcc_all,
            "share_window_pct": _share(lcc_window, kept),
            "share_all_pct": _share(lcc_all, kept),
        }

    for w in control_weeks:
        cut = (hi - timedelta(weeks=w)).strftime("%Y-%m-%d")
        r_kept, r_trimmed, r_lcc_window, r_lcc_all = trim_recency(nodes, edges, cut)
        # k = the count of nodes newer than the cut is exactly what
        # trim_recency already computed as its trimmed count at this same
        # cut (test 3 asserts the two are equal) — take it from there
        # instead of recomputing the same sum a second time.
        k = r_trimmed
        c_kept, c_lcc_all = trim_oldest_matched(nodes_sorted, all_edge_pairs, k)
        result["control"][w] = {
            "cut": cut,
            "k": k,
            "recency_kept": r_kept,
            "recency_trimmed": r_trimmed,
            "recency_lcc_window": r_lcc_window,
            "recency_lcc_all": r_lcc_all,
            "recency_share_window_pct": _share(r_lcc_window, r_kept),
            "recency_share_all_pct": _share(r_lcc_all, r_kept),
            "control_kept": c_kept,
            "control_lcc_all": c_lcc_all,
            "control_share_pct": _share(c_lcc_all, c_kept),
        }

    return result


def print_trim_control_table(result):
    print(f"# hi = {result['hi']}")
    print("## recency arm (trim the newest N weeks)")
    print(f"{'weeks':>6}{'cut':>12}{'kept':>8}{'trimmed':>9}{'lcc_win':>9}{'lcc_all':>9}"
          f"{'shr_win%':>10}{'shr_all%':>10}")
    for w, r in result["recency"].items():
        print(f"{w:>6}{r['cut']:>12}{r['kept']:>8,}{r['trimmed']:>9,}{r['lcc_window']:>9,}"
              f"{r['lcc_all']:>9,}{r['share_window_pct']:>10.1f}{r['share_all_pct']:>10.1f}")
    print("## control arm (matched node count, newest-removed vs oldest-removed)")
    print(f"{'weeks':>6}{'cut':>12}{'k':>8}{'rec_win%':>10}{'rec_all%':>10}"
          f"{'old_kept':>10}{'old_shr%':>10}")
    for w, r in result["control"].items():
        print(f"{w:>6}{r['cut']:>12}{r['k']:>8,}{r['recency_share_window_pct']:>10.1f}"
              f"{r['recency_share_all_pct']:>10.1f}{r['control_kept']:>10,}"
              f"{r['control_share_pct']:>10.1f}")


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

    c = _ssot.connect(db)
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
    _ssot.add_db_arg(ap)
    ap.add_argument("--step-days", type=int, default=7)
    ap.add_argument("--validate-git", metavar="COMMITISH", default=None)
    ap.add_argument("--trim-control", action="store_true",
                     help="Ch6 §6.2's recency-trim + matched-count control arms")
    ap.add_argument("--json", action="store_true",
                     help="with --trim-control, print the result as JSON instead of a table")
    a = ap.parse_args()
    db = _ssot.resolve_db(a.db, allow_unpinned=a.allow_unpinned)
    if a.trim_control:
        result = trim_control(db)
        if a.json:
            print(json.dumps(result, indent=2))
        else:
            print_trim_control_table(result)
    elif a.validate_git:
        validate_git(db, a.validate_git)
    else:
        trend(db, a.step_days)

if __name__ == "__main__":
    main()
