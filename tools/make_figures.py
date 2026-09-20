#!/usr/bin/env python3
"""make_figures.py — every figure in the ENGRAM paper, generated from the SSoT snapshot.

Same contract as the other instruments in this directory: each figure is computed
from the frozen database and nothing else, and each prints its own numbers to
stdout beside the file it writes, so a reader can check the plot against the prose
without opening the image.

Usage:
    python tools/make_figures.py --db dataset/<snapshot>.db --out paper/figures
"""

from __future__ import annotations

import argparse
import collections
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _ssot
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# One restrained palette across every figure; greys carry structure, one accent
# colour carries the claim under discussion.
INK = "#1b1b1b"
MUTED = "#8a8a8a"
GRID = "#e2e2e2"
ACCENT = "#1f6f8b"
WARM = "#b3593f"

# The derivation Ch6 §6.4 names as its worked example. The figure annotates THIS
# node, so a drift between plot and prose fails loudly instead of silently.
EXEMPLAR = "dv_0922"

plt.rcParams.update(
    {
        "figure.dpi": 160,
        "savefig.dpi": 160,
        "savefig.bbox": "tight",
        "font.size": 9,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "axes.titlesize": 10,
        "axes.titleweight": "bold",
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def _style(ax, xlabel=None, ylabel=None, title=None):
    if title:
        ax.set_title(title, loc="left", pad=10)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(axis="x", color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)


def fig_reasoning_type(con, out: Path) -> str:
    """The argument-shape claim: confidence tracks HOW a claim is argued."""
    # reasoning_type is not a column — it lives in the JSON metadata blob,
    # same as tools/paper_stats.py reads it.
    buckets = collections.defaultdict(list)
    for meta, conf in con.execute(
        "SELECT metadata, confidence FROM nodes "
        "WHERE type='derivation' AND is_current=1 AND confidence IS NOT NULL"
    ):
        rt = "(absent)"
        if meta:
            try:
                rt = json.loads(meta).get("reasoning_type", "(absent)")
            except Exception:
                pass
        buckets[rt].append(conf)

    rows = sorted(
        ((k, len(v), sum(v) / len(v)) for k, v in buckets.items() if len(v) >= 5),
        key=lambda r: r[2],
    )
    labels = [r[0].replace("_", " ") for r in rows]
    means = [r[2] for r in rows]
    ns = [r[1] for r in rows]

    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    colours = [ACCENT if m >= 0.80 else (WARM if m <= 0.55 else MUTED) for m in means]
    ax.barh(labels, means, color=colours, height=0.68)
    for y, (m, n) in enumerate(zip(means, ns)):
        ax.text(m + 0.012, y, f"{m:.2f}  (n={n:,})", va="center", fontsize=8, color=INK)
    ax.set_xlim(0, 1.0)
    _style(ax, xlabel="mean computed confidence", title="Confidence is set by argument shape, not by depth")
    fig.savefig(out / "fig1-reasoning-type.png")
    plt.close(fig)

    lines = [f"fig1  {r[0]:<34} n={r[1]:>5,}  mean={r[2]:.3f}" for r in rows]
    return "\n".join(lines)


def fig_node_type(con, out: Path) -> str:
    """Confidence by node type, with the interquartile range drawn."""
    rows = list(
        con.execute(
            """
            SELECT type, confidence FROM nodes
            WHERE is_current = 1 AND confidence IS NOT NULL
              AND type IN ('axiom','observation_factual','derivation','conjecture')
            """
        )
    )
    by = collections.defaultdict(list)
    for t, c in rows:
        by[t].append(c)

    order = ["conjecture", "derivation", "observation_factual", "axiom"]
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    data = [sorted(by[t]) for t in order]
    bp = ax.boxplot(
        data, vert=False, widths=0.55, patch_artist=True, showfliers=False,
        medianprops=dict(color=INK, linewidth=1.4),
        whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED),
        boxprops=dict(facecolor="#eef3f6", edgecolor=MUTED),
    )
    bp["boxes"][order.index("axiom")].set_facecolor("#e6eef2")
    ax.set_yticklabels([f"{t.replace('_',' ')}\n(n={len(by[t]):,})" for t in order])
    ax.set_xlim(0, 1.02)
    _style(ax, xlabel="computed confidence", title="Each node type occupies its own band")
    fig.savefig(out / "fig2-node-type.png")
    plt.close(fig)

    lines = []
    for t in order:
        v = sorted(by[t])
        med = v[len(v) // 2]
        lines.append(f"fig2  {t:<22} n={len(v):>5,}  median={med:.2f}  min={v[0]:.2f}  max={v[-1]:.2f}")
    return "\n".join(lines)


def fig_quote_type(con, out: Path) -> str:
    """Observation confidence is a near-mechanical map from evidence type."""
    rows = list(
        con.execute(
            """
            SELECT quote_type, COUNT(*) n, AVG(confidence) mean
            FROM nodes
            WHERE type LIKE 'observation%' AND is_current = 1
              AND confidence IS NOT NULL AND quote_type IS NOT NULL
            GROUP BY quote_type ORDER BY mean
            """
        )
    )
    labels = [r[0].replace("_", " ") for r in rows]
    means = [r[2] for r in rows]
    ns = [r[1] for r in rows]

    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    ax.barh(labels, means, color=[ACCENT if m >= 0.85 else MUTED for m in means], height=0.62)
    for y, (m, n) in enumerate(zip(means, ns)):
        ax.text(m + 0.012, y, f"{m:.2f}  (n={n:,})", va="center", fontsize=8, color=INK)
    ax.set_xlim(0, 1.0)
    _style(ax, xlabel="mean computed confidence", title="Evidence type sets an observation's ceiling")
    fig.savefig(out / "fig3-quote-type.png")
    plt.close(fig)
    return "\n".join(f"fig3  {r[0]:<26} n={r[1]:>5,}  mean={r[2]:.3f}" for r in rows)


def _depths(con):
    """Longest derives_from path to a root, per current node."""
    cur = {r[0] for r in con.execute("SELECT id FROM nodes WHERE is_current = 1")}
    parents = collections.defaultdict(list)
    for s, t in con.execute("SELECT source_id, target_id FROM edges WHERE relation = 'derives_from'"):
        if s in cur and t in cur:
            parents[s].append(t)

    memo: dict[str, int] = {}

    def depth(n, stack=frozenset()):
        if n in memo:
            return memo[n]
        if n in stack or n not in parents:
            return 0
        d = 1 + max(depth(p, stack | {n}) for p in parents[n])
        memo[n] = d
        return d

    sys.setrecursionlimit(10000)
    return {n: depth(n) for n in parents}


def fig_depth_inversion(con, out: Path) -> str:
    """The inversion: depth does not predict confidence."""
    d = _depths(con)
    conf = dict(
        con.execute(
            "SELECT id, confidence FROM nodes WHERE type='derivation' AND is_current=1 AND confidence IS NOT NULL"
        )
    )
    pts = [(d[n], conf[n]) for n in d if n in conf and d[n] > 0]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.scatter(xs, ys, s=9, alpha=0.20, color=MUTED, linewidths=0)

    by_depth = collections.defaultdict(list)
    for x, y in pts:
        by_depth[x].append(y)
    ds = sorted(by_depth)
    ax.plot(ds, [sum(by_depth[k]) / len(by_depth[k]) for k in ds], color=ACCENT, linewidth=1.8, label="mean at depth")

    deepest = max(pts, key=lambda p: p[0])
    ax.scatter([deepest[0]], [deepest[1]], s=54, color=ACCENT, zorder=5, edgecolor="white", linewidth=1.1)
    ax.annotate(
        f"deepest chain\ndepth {deepest[0]}, conf {deepest[1]:.2f}",
        xy=deepest, xytext=(deepest[0] - 4.6, deepest[1] + 0.20), fontsize=8, color=INK,
        arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8),
    )

    # Annotate the node the PROSE names, never an auto-picked extremum: an
    # auto-pick silently drifts away from the text as the graph grows, and the
    # figure then illustrates a different claim than the one beside it.
    if EXEMPLAR in d and EXEMPLAR in conf:
        low = (d[EXEMPLAR], conf[EXEMPLAR])
    else:  # fail loud rather than quietly illustrating something else
        raise SystemExit(f"exemplar {EXEMPLAR} absent from the snapshot — update EXEMPLAR or the prose")
    ax.scatter([low[0]], [low[1]], s=54, color=WARM, zorder=5, edgecolor="white", linewidth=1.1)
    ax.annotate(
        f"an ambitious synthesis\ndepth {low[0]}, conf {low[1]:.2f}",
        xy=low, xytext=(low[0] + 1.2, low[1] + 0.26), fontsize=8, color=INK,
        arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8),
    )

    ax.set_ylim(0, 1.0)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    _style(ax, xlabel="derivation depth (longest path to a root)", ylabel="computed confidence",
           title="Depth is not the variable")
    fig.savefig(out / "fig4-depth-inversion.png")
    plt.close(fig)

    return (f"fig4  derivations with depth>0: {len(pts):,}   max depth={deepest[0]} at conf={deepest[1]:.2f}\n"
            f"fig4  exemplar {EXEMPLAR}: depth={low[0]} conf={low[1]:.2f}")


def fig_growth(con, out: Path) -> str:
    """Graph growth and the current/superseded split over the trajectory."""
    rows = list(
        con.execute(
            "SELECT substr(created_at,1,7) m, COUNT(*) n, SUM(is_current) cur FROM nodes GROUP BY m ORDER BY m"
        )
    )
    months = [r[0] for r in rows]
    cum = 0
    cum_series = []
    for r in rows:
        cum += r[1]
        cum_series.append(cum)

    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(months, cum_series, color=ACCENT, linewidth=2.0, marker="o", markersize=4)
    for x, y in zip(months, cum_series):
        ax.annotate(f"{y:,}", (x, y), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=7.5, color=INK)
    ax.set_ylim(0, max(cum_series) * 1.18)
    _style(ax, ylabel="cumulative nodes", title="One graph, one agent, five months")
    ax.grid(axis="y", color=GRID, linewidth=0.7)
    fig.savefig(out / "fig5-growth.png")
    plt.close(fig)
    return "\n".join(f"fig5  {m}  new={r[1]:>5,}  cumulative={c:>6,}" for m, r, c in zip(months, rows, cum_series))


def fig_census(con, out: Path) -> str:
    """What the graph is made of."""
    rows = list(
        con.execute(
            "SELECT type, COUNT(*) n FROM nodes WHERE is_current=1 GROUP BY type ORDER BY n DESC"
        )
    )
    top = rows[:9]
    other = sum(r[1] for r in rows[9:])
    labels = [r[0].replace("_", " ") for r in top] + ([f"other ({len(rows)-9} types)"] if other else [])
    vals = [r[1] for r in top] + ([other] if other else [])

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    colours = [ACCENT if i == 0 else MUTED for i in range(len(vals))]
    ax.barh(labels[::-1], vals[::-1], color=colours[::-1], height=0.66)
    total = sum(r[1] for r in rows)
    for y, v in enumerate(vals[::-1]):
        ax.text(v + total * 0.006, y, f"{v:,}  ({v/total*100:.1f}%)", va="center", fontsize=8, color=INK)
    ax.set_xlim(0, max(vals) * 1.22)
    _style(ax, xlabel="current nodes", title=f"Node census — {total:,} current nodes")
    fig.savefig(out / "fig6-census.png")
    plt.close(fig)
    return "\n".join(f"fig6  {r[0]:<24} {r[1]:>5,}  {r[1]/total*100:5.1f}%" for r in rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    _ssot.add_db_arg(ap)
    ap.add_argument("--out", default="paper/figures")
    a = ap.parse_args()
    db = _ssot.resolve_db(a.db, allow_unpinned=a.allow_unpinned)
    pin_note = ("pin NOT verified (--allow-unpinned)" if a.allow_unpinned
                else "sha256 pin verified against dataset/DATASET.md")

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    con = _ssot.connect(db)

    print(f"# source: {db}")
    print(f"# {pin_note}")
    print("# every figure below is computed from that file and nothing else\n")
    for fn in (fig_reasoning_type, fig_node_type, fig_quote_type,
               fig_depth_inversion, fig_growth, fig_census):
        print(fn(con, out))
        print()
    print(f"# wrote {len(list(out.glob('*.png')))} figures to {out}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
