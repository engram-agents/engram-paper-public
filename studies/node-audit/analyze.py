#!/usr/bin/env python3
"""Pre-registered analysis for the independent node audit (paper v2, workstream D;
protocol: studies/node-audit/PROTOCOL.md, section "Analysis").

    analyze.py --mira PATH --zephyr PATH --controls PATH --db PATH --drawn PATH
               --prior-node ID --seed TEXT --out DIR

Built and tested on SYNTHETIC data before any verdict is read. Rates, AUC and deltas use
Mira's verdicts (the primary reader, all sampled nodes); Zephyr's file feeds the control
scores and the overlap agreement. Stdlib only.

CONTRACT (each clause is asserted by tests/test_node_audit_analyze.py)

 1. Validation, refuse loudly, never drop. Mira's file must hold exactly the sampled ids
    plus all controls; Zephyr's exactly the `zephyr` ids plus all controls. No duplicate,
    extra or missing id; each row carries exactly the check set its kind calls for
    (dv_ -> type, placement, chain-overreach; ob_ -> support-overreach, quote_type,
    source_class); every verdict in {tight, loose, cannot-judge}; every reason a string;
    `proposed_type` non-null iff `type` is loose. Any violation raises VerdictFileInvalid
    listing EVERY offending id with its reason, and the CLI exits non-zero. A row is
    never skipped silently.
 2. Node class: loose = any check loose; tight = every check tight; partial = at least one
    tight, at least one cannot-judge, no loose; cannot-judge = every check cannot-judge.
 3. Controls are excluded from every rate. Per reader: sensitivity = known-loose controls
    classed loose / known-loose; specificity = known-tight controls (placement_verified
    union final) classed tight / known-tight; reported as k/n with the class tallies
    (partial and cannot-judge counts). Control ids appear in the report ONLY in the
    "Controls" section (the reveal). The notes in the controls file are never read.
 4. Loose rates per stratum: low bound counts partial as tight, high bound counts partial
    as loose; Wilson 95% interval on each bound; partial and cannot-judge counts beside
    them. A node whose class is cannot-judge LEAVES THE DENOMINATOR of every loose rate,
    bound and weighted rate (it is never counted as not-loose) and its count is printed
    beside the rate; partial nodes stay in the denominator. The denominator is therefore
    the judgeable n = tight + loose + partial. A stratum with fewer than 10 judgeable
    nodes reports counts only: no rate, no interval. Population-weighted loose rate,
    separately for derivations and observations, weights = census population shares of
    the strata that have at least one judgeable node (renormalised over them; the strata
    without a draw, and those drawn but all cannot-judge, are listed), with the number of
    cannot-judge nodes excluded printed beside it; a second figure restricted to strata
    with at least 10 judgeable nodes is printed beside it.
 5. inductive_generalization loose rate on its own, plus a confusion table of declared
    type x proposed type over `loose:type` verdicts.
 6. Confidence vs verdict (confidences joined from the DB only here): mean confidence of
    tight vs loose nodes; AUC = P(conf(tight) > conf(loose)), ties 0.5; seeded
    percentile bootstrap 95% interval (N_BOOT = 10,000 resamples, tight and loose groups
    resampled separately), within derivations and within observations. Partial and
    cannot-judge are excluded, counts shown. The reading is chosen mechanically and
    printed verbatim: CI lower > 0.5 -> READING_TRACKS; CI contains 0.5 -> READING_NONE;
    CI upper < 0.5 -> READING_AGAINST.
 7. Confidence deltas (item 3b): for every `loose:type` verdict on a derivation, recompute
    its confidence under the reader's proposed type with the VENDORED v0.5.1 formula
    (_v051_confidence.py tables, verified by sha256 before use) and the node's own
    COMPUTED-FROM premise set, `derives_from` UNION `acknowledged_derives_from` targets,
    as tools/modus_ponens_check.py defines it (self-loops excluded, a target listed under
    both relations counted once, NULL-confidence targets excluded); delta = recomputed -
    stored, so the delta isolates the type effect: the stored value was computed from that
    same set. A
    proposed type outside the v0.5.1 table is listed as such, never computed. n/min/
    median/max and every row are reported.
 8. Agreement on the overlap ids (controls excluded; control agreement reported
    separately): percent agreement and Cohen's kappa on node class with partial as its own
    category; kappa on tight vs loose restricted to nodes both readers classed tight or
    loose; per-check percent agreement. Every disagreement is listed.
 9. cannot-judge counts per check and per node class are always reported, never folded
    into tight or loose.
10. Analyst-prior node (--prior-node, must be a sampled node): every rate in 4-6 is
    reported twice, with and without that node. The <10 rule applies to each pass's own n.
11. Determinism: same inputs plus seed give byte-identical report.json and report.md.
12. Outputs go to --out, which must resolve outside the git worktree that holds this
    script (OutputInsideWorktree otherwise, nothing written): report.json (all numbers)
    and report.md. Nothing is written into the repo.

The snapshot DB is opened read-only and used only for nodes.confidence,
json_extract(metadata,'$.reasoning_type') and edges(source_id, target_id, relation) with
relation in ('derives_from', 'acknowledged_derives_from').
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import random
import sqlite3
import statistics
import subprocess
import sys
from bisect import bisect_left, bisect_right
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDORED_PATH = HERE / "_v051_confidence.py"
VENDORED_SHA256 = "5ea367d8d15153e82b68d3fdf5f08ef12b5d5555be9326f5ee65e0a12ac260e0"

N_BOOT = 10000
MIN_RATE_N = 10
Z95 = 1.959963984540054
BOOT_SEED_FORMAT = "{seed}:boot:{label}"  # label = "<with_prior|without_prior>:<derivation|observation>"
VERDICTS = ("tight", "loose", "cannot-judge")
CLASSES = ("loose", "tight", "partial", "cannot-judge")
CHECKS = {
    "derivation": ("type", "placement", "chain-overreach"),
    "observation": ("support-overreach", "quote_type", "source_class"),
}
ALL_CHECKS = CHECKS["derivation"] + CHECKS["observation"]

READING_TRACKS = "confidence tracks correctness in this sample"
READING_NONE = "no evidence either way at this n"
READING_AGAINST = "confidence runs against correctness in this sample"
READING_NA = "not computable: needs at least one tight and one loose node"


# ------------------------------------------------------------------ errors
class AnalysisError(Exception):
    """A refusal with a name; the tool never improvises past one."""


class VerdictFileInvalid(AnalysisError):
    pass


class InputInvalid(AnalysisError):
    pass


class OutputInsideWorktree(AnalysisError):
    pass


class VendoredFileMismatch(AnalysisError):
    pass


# ------------------------------------------------------------------ vendored v0.5.1 formula
_VENDORED = None


def _sha256(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_vendored(path=VENDORED_PATH):
    got = _sha256(path)
    if got != VENDORED_SHA256:
        raise VendoredFileMismatch(f"{path}: sha256 {got} != pinned v0.5.1 {VENDORED_SHA256}")


def _vendored():
    global _VENDORED
    if _VENDORED is None:
        verify_vendored()
        spec = importlib.util.spec_from_file_location("_v051_confidence", VENDORED_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _VENDORED = mod
    return _VENDORED


def v051_confidence(reasoning_type, premise_confidences):
    """A derivation's confidence under `reasoning_type`, from the v0.5.1 tables.

    The vendored module holds the tables only (REASONING_CLASS, REASONING_DISCOUNT,
    ABDUCTIVE_CONFIDENCE_CAP); the per-class aggregation is not in it. This wrapper applies
    the aggregation exactly as v0.5.1's src/engram/tools/surgical.py does (lines 431-444) and
    as v0.5.1's src/engram/engram_core.py does (the derive path that computed the stored
    confidences; its per-class branches are identical to surgical.py's): corroboration class
    1-prod(1-c) times the discount; abductive min(c)*discount capped; every other class
    min(c)*discount; rounded to 3 places. Returns None for a type outside the v0.5.1 table.
    """
    m = _vendored()
    if reasoning_type not in m.REASONING_CLASS:
        return None
    confs = list(premise_confidences)
    if not confs:
        raise ValueError("no premise confidences")
    rclass, discount = m.REASONING_CLASS[reasoning_type], m.REASONING_DISCOUNT[reasoning_type]
    if rclass == "inductive_corroboration":
        product = 1.0
        for c in confs:
            product *= (1.0 - c)
        conf = (1.0 - product) * discount
    elif rclass == "abductive":
        conf = min(min(confs) * discount, m.ABDUCTIVE_CONFIDENCE_CAP.get(reasoning_type, 0.85))
    else:
        conf = min(confs) * discount
    return round(conf, 3)


# ------------------------------------------------------------------ small statistics
def wilson(k, n, z=Z95):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def auc(tight, loose):
    """P(conf(tight) > conf(loose)), ties counting 0.5."""
    ls = sorted(loose)
    wins = 0.0
    for t in tight:
        lt = bisect_left(ls, t)
        wins += lt + 0.5 * (bisect_right(ls, t) - lt)
    return wins / (len(tight) * len(ls))


def reading(ci_low, ci_high):
    if ci_low > 0.5:
        return READING_TRACKS
    if ci_high < 0.5:
        return READING_AGAINST
    return READING_NONE


def auc_report(tight, loose, seed, label, n_boot=N_BOOT):
    out = {"n_tight": len(tight), "n_loose": len(loose),
           "mean_tight": statistics.fmean(tight) if tight else None,
           "mean_loose": statistics.fmean(loose) if loose else None}
    if not tight or not loose:
        out.update(auc=None, auc_ci=None, reading=READING_NA)
        return out
    rng = random.Random(BOOT_SEED_FORMAT.format(seed=seed, label=label))
    boots = sorted(auc(rng.choices(tight, k=len(tight)), rng.choices(loose, k=len(loose)))
                   for _ in range(n_boot))
    lo, hi = boots[int(0.025 * n_boot)], boots[math.ceil(0.975 * n_boot) - 1]
    out.update(auc=auc(tight, loose), auc_ci=[lo, hi], reading=reading(lo, hi))
    return out


def cohens_kappa(a, b):
    """Cohen's kappa for two label lists; None where undefined (chance agreement is 1)."""
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in set(a) | set(b))
    if pe >= 1.0:
        return None
    return (po - pe) / (1 - pe)


# ------------------------------------------------------------------ nodes and classes
def kind_of(node_id):
    if node_id.startswith("dv_"):
        return "derivation"
    if node_id.startswith("ob_"):
        return "observation"
    return None


def node_class(checks):
    vs = [c["verdict"] for c in checks.values()]
    if "loose" in vs:
        return "loose"
    if all(v == "tight" for v in vs):
        return "tight"
    if all(v == "cannot-judge" for v in vs):
        return "cannot-judge"
    return "partial"


# ------------------------------------------------------------------ 1 validation
def validate_verdicts(path, expected_ids, reader):
    """Return {id: checks} for a verdict file that is exactly right; raise VerdictFileInvalid
    naming every offending id otherwise. No row is ever skipped."""
    expected = set(expected_ids)
    problems = []
    rows = {}
    seen = set()
    try:
        text = Path(path).read_text()
    except OSError as e:
        raise VerdictFileInvalid(f"{reader}: cannot read {path}: {e}") from None
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except ValueError as e:
            problems.append((f"line {lineno}", f"invalid JSON ({e})"))
            continue
        if not isinstance(obj, dict) or not isinstance(obj.get("id"), str) or not isinstance(obj.get("checks"), dict):
            problems.append((f"line {lineno}", "row must be an object with a string id and a checks object"))
            continue
        nid, checks = obj["id"], obj["checks"]
        if nid in seen:
            problems.append((nid, "duplicate id"))
        seen.add(nid)
        if nid not in expected:
            problems.append((nid, "unexpected id (not in the expected set)"))
        kind = kind_of(nid)
        if kind is None:
            problems.append((nid, "unknown node kind (id is neither dv_ nor ob_)"))
            continue
        want = CHECKS[kind]
        if set(checks) != set(want):
            problems.append((nid, f"check set {sorted(checks)} != {sorted(want)}"))
            continue
        row_ok = True
        for name in want:
            c = checks[name]
            if not isinstance(c, dict):
                problems.append((nid, f"check {name}: not an object"))
                row_ok = False
                continue
            if c.get("verdict") not in VERDICTS:
                problems.append((nid, f"check {name}: verdict value {c.get('verdict')!r} not in {list(VERDICTS)}"))
                row_ok = False
            if not isinstance(c.get("reason"), str):
                problems.append((nid, f"check {name}: reason missing or not a string"))
                row_ok = False
        if kind == "derivation" and isinstance(checks.get("type"), dict):
            t = checks["type"]
            pt = t.get("proposed_type")
            if t.get("verdict") == "loose" and not (isinstance(pt, str) and pt.strip()):
                problems.append((nid, "proposed_type must be a non-empty string when type is loose"))
                row_ok = False
            elif t.get("verdict") != "loose" and pt is not None:
                problems.append((nid, "proposed_type must be null unless type is loose"))
                row_ok = False
        if row_ok and nid not in rows:
            rows[nid] = checks
    for nid in sorted(expected - seen):
        problems.append((nid, "missing id"))
    if problems:
        body = "\n".join(f"  - {i}: {why}" for i, why in problems)
        raise VerdictFileInvalid(f"{reader} verdict file {path} is invalid ({len(problems)} problem(s)):\n{body}")
    return rows


# ------------------------------------------------------------------ inputs
def load_drawn(path):
    d = json.loads(Path(path).read_text())
    for k in ("seed", "allocation", "sampled", "zephyr", "census"):
        if k not in d:
            raise InputInvalid(f"drawn ids file lacks key {k!r}")
    for k in ("derivation_by_type", "observation_factual_by_quote_type"):
        if k not in d["census"]:
            raise InputInvalid(f"drawn ids census lacks key {k!r}")
    census_pop = {}
    for t, n in d["census"]["derivation_by_type"].items():
        census_pop[f"derivation:{t}"] = n
    for q, n in d["census"]["observation_factual_by_quote_type"].items():
        census_pop[f"observation:{q}"] = n
    stratum_of = {}
    for s, members in d["sampled"].items():
        if s not in census_pop:
            raise InputInvalid(f"sampled stratum {s!r} has no census population")
        for i in members:
            if kind_of(i) != s.split(":", 1)[0]:
                raise InputInvalid(f"{i} does not belong in stratum {s!r}")
            if i in stratum_of:
                raise InputInvalid(f"{i} is sampled in two strata")
            stratum_of[i] = s
    unknown = sorted(set(d["zephyr"]) - set(stratum_of))
    if unknown:
        raise InputInvalid(f"zephyr ids not in the sampled set: {unknown}")
    return d, census_pop, stratum_of


def load_controls(path, sampled_ids):
    c = json.loads(Path(path).read_text())
    for k in ("known_loose", "known_tight_placement_verified", "known_tight_final"):
        if k not in c:
            raise InputInvalid(f"controls file lacks key {k!r}")
    loose = sorted(c["known_loose"])  # keys only: the notes are never read
    tight = sorted(set(c["known_tight_placement_verified"]) | set(c["known_tight_final"]))
    both = sorted(set(loose) & set(tight))
    if both:
        raise InputInvalid(f"control ids listed as both known-loose and known-tight: {both}")
    leaked = sorted((set(loose) | set(tight)) & set(sampled_ids))
    if leaked:
        raise InputInvalid(f"control ids that are also sampled: {leaked}")
    return loose, tight


def open_ro(path):
    con = sqlite3.connect(f"file:{Path(path).resolve()}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def db_confidence(con, node_id):
    r = con.execute("SELECT confidence FROM nodes WHERE id=?", (node_id,)).fetchone()
    return None if r is None else r["confidence"]


def db_declared_type(con, node_id):
    r = con.execute("SELECT json_extract(metadata,'$.reasoning_type') AS rt FROM nodes WHERE id=?",
                    (node_id,)).fetchone()
    return None if r is None else r["rt"]


def db_premise_confidences(con, node_id):
    """Confidences of the COMPUTED-FROM premise set: targets of `derives_from` UNION
    `acknowledged_derives_from` edges (tools/modus_ponens_check.py's definition), each target
    once, the node itself and NULL-confidence targets excluded. The stored confidence was
    computed from this set, so a recompute under another type must read the same set for the
    delta to isolate the type effect."""
    return [r["confidence"] for r in con.execute(
        "SELECT DISTINCT n.id AS id, n.confidence AS confidence "
        "FROM edges e JOIN nodes n ON n.id = e.target_id "
        "WHERE e.source_id=? AND e.relation IN ('derives_from','acknowledged_derives_from') "
        "AND n.id <> ? AND n.confidence IS NOT NULL "
        "ORDER BY n.id", (node_id, node_id))]


# ------------------------------------------------------------------ analysis pieces
def stratum_row(nodes, min_n=None):
    """Counts for one stratum plus, when it has at least `min_n` (default MIN_RATE_N) JUDGEABLE
    nodes, the low/high loose bounds. `n` is the number drawn; the denominator of every rate is
    `n_judgeable` = tight + loose + partial: cannot-judge nodes leave it (never counted as
    not-loose), partial nodes stay in it."""
    min_n = MIN_RATE_N if min_n is None else min_n
    n = len(nodes)
    cnt = {c: sum(1 for x in nodes if x["class"] == c) for c in CLASSES}
    nj = cnt["tight"] + cnt["loose"] + cnt["partial"]
    row = {"n": n, "n_judgeable": nj, "loose": cnt["loose"], "partial": cnt["partial"],
           "cannot_judge": cnt["cannot-judge"], "tight": cnt["tight"]}
    if nj >= max(min_n, 1):
        for key, k in (("low", cnt["loose"]), ("high", cnt["loose"] + cnt["partial"])):
            lo, hi = wilson(k, nj)
            row[key] = {"rate": k / nj, "ci_low": lo, "ci_high": hi}
    return row


def weighted_rate(rows, census_pop, kind, min_n=1):
    """Weights = census shares of the strata with at least `min_n` JUDGEABLE nodes (and at least
    one), renormalised over them. Each stratum's rate has the judgeable n as denominator.
    `n_cannot_judge_excluded` = cannot-judge nodes left out of the denominators, over ALL
    strata of this kind, printed beside the rate."""
    kind_rows = {s: r for s, r in rows.items() if s.startswith(kind + ":")}
    excluded = sum(r["cannot_judge"] for r in kind_rows.values())
    used = {s: r for s, r in kind_rows.items() if r["n_judgeable"] >= max(min_n, 1) and census_pop.get(s, 0) > 0}
    total = sum(census_pop[s] for s in used)
    if not total:
        return {"low": None, "high": None, "weights": {}, "n_cannot_judge_excluded": excluded}
    w = {s: census_pop[s] / total for s in sorted(used)}
    return {"low": sum(w[s] * used[s]["loose"] / used[s]["n_judgeable"] for s in w),
            "high": sum(w[s] * (used[s]["loose"] + used[s]["partial"]) / used[s]["n_judgeable"] for s in w),
            "weights": w, "n_cannot_judge_excluded": excluded}


def analyze_pass(nodes, census_pop, strata_names, seed, label, n_boot):
    out = {}
    for kind in ("derivation", "observation"):
        kn = [x for x in nodes if x["kind"] == kind]
        rows = {s: stratum_row([x for x in kn if x["stratum"] == s])
                for s in strata_names if s.startswith(kind + ":")}
        weighted = weighted_rate(rows, census_pop, kind)
        weighted["rated_strata_only"] = weighted_rate(rows, census_pop, kind, MIN_RATE_N)
        weighted["strata_without_draw"] = {s: p for s, p in sorted(census_pop.items())
                                           if s.startswith(kind + ":") and rows.get(s, {"n": 0})["n"] == 0}
        weighted["strata_all_cannot_judge"] = {s: p for s, p in sorted(census_pop.items())
                                               if s.startswith(kind + ":") and rows.get(s, {"n": 0})["n"] > 0
                                               and rows[s]["n_judgeable"] == 0}
        tight = [x["conf"] for x in kn if x["class"] == "tight"]
        loose = [x["conf"] for x in kn if x["class"] == "loose"]
        conf = auc_report(tight, loose, seed, f"{label}:{kind}", n_boot)
        conf["n_partial"] = sum(1 for x in kn if x["class"] == "partial")
        conf["n_cannot_judge"] = sum(1 for x in kn if x["class"] == "cannot-judge")
        out[kind] = {"strata": rows, "weighted": weighted, "confidence": conf}
    ig = "derivation:inductive_generalization"
    out["derivation"]["inductive_generalization"] = out["derivation"]["strata"].get(ig, stratum_row([]))
    confusion = {}
    for x in nodes:
        if x["kind"] == "derivation" and x["checks"]["type"]["verdict"] == "loose":
            d = confusion.setdefault(x["declared"], {})
            p = x["checks"]["type"]["proposed_type"]
            d[p] = d.get(p, 0) + 1
    out["derivation"]["confusion"] = {a: dict(sorted(b.items())) for a, b in sorted(confusion.items())}
    return out


def cannot_judge_block(verdict_rows, node_ids):
    per_check = {c: {v: 0 for v in VERDICTS} for c in ALL_CHECKS}
    per_class = {k: {c: 0 for c in CLASSES} for k in CHECKS}
    for i in node_ids:
        checks = verdict_rows[i]
        for name, c in checks.items():
            per_check[name][c["verdict"]] += 1
        per_class[kind_of(i)][node_class(checks)] += 1
    return {"per_check": per_check, "per_class": per_class}


def agreement_block(ids, mclass, zclass):
    ids = sorted(ids)
    a, b = [mclass[i] for i in ids], [zclass[i] for i in ids]
    agree = sum(x == y for x, y in zip(a, b))
    return {"n": len(ids), "agree": agree,
            "percent_agreement": 100 * agree / len(ids) if ids else None,
            "kappa": cohens_kappa(a, b),
            "disagreements": [{"id": i, "mira": x, "zephyr": y} for i, x, y in zip(ids, a, b) if x != y]}


def overlap_agreement(ids, mrows, zrows):
    mc = {i: node_class(mrows[i]) for i in ids}
    zc = {i: node_class(zrows[i]) for i in ids}
    base = agreement_block(ids, mc, zc)
    both = [i for i in sorted(ids) if mc[i] in ("tight", "loose") and zc[i] in ("tight", "loose")]
    per_check = {}
    for name in ALL_CHECKS:
        kids = [i for i in sorted(ids) if name in mrows[i]]
        ag = sum(mrows[i][name]["verdict"] == zrows[i][name]["verdict"] for i in kids)
        per_check[name] = {"n": len(kids), "agree": ag,
                           "percent_agreement": 100 * ag / len(kids) if kids else None}
    return {"n_overlap": base["n"], "n_agree": base["agree"], "percent_agreement": base["percent_agreement"],
            "kappa_class": base["kappa"],
            "n_tight_loose_both": len(both),
            "kappa_tight_loose": cohens_kappa([mc[i] for i in both], [zc[i] for i in both]),
            "disagreements": base["disagreements"], "per_check": per_check}


def controls_block(loose, tight, mrows, zrows):
    out = {}
    for who, rows in (("mira", mrows), ("zephyr", zrows)):
        cl = {i: node_class(rows[i]) for i in loose + tight}
        tally = lambda ids: {c: sum(1 for i in ids if cl[i] == c) for c in CLASSES}  # noqa: E731
        k_s, k_p = sum(cl[i] == "loose" for i in loose), sum(cl[i] == "tight" for i in tight)
        out[who] = {"sensitivity": {"k": k_s, "n": len(loose), "text": f"{k_s}/{len(loose)}"},
                    "specificity": {"k": k_p, "n": len(tight), "text": f"{k_p}/{len(tight)}"},
                    "known_loose_classes": tally(loose), "known_tight_classes": tally(tight),
                    "per_control": dict(sorted(cl.items()))}
    mc = {i: out["mira"]["per_control"][i] for i in loose + tight}
    zc = {i: out["zephyr"]["per_control"][i] for i in loose + tight}
    out["agreement"] = agreement_block(loose + tight, mc, zc)
    return out


def deltas_block(con, nodes):
    computed, not_computed = [], []
    for x in nodes:
        if x["kind"] != "derivation" or x["checks"]["type"]["verdict"] != "loose":
            continue
        proposed = x["checks"]["type"]["proposed_type"]
        base = {"id": x["id"], "declared_type": x["declared"], "proposed_type": proposed}
        if proposed not in _vendored().REASONING_CLASS:
            not_computed.append(base | {"reason": "proposed_type is not in the v0.5.1 reasoning table"})
            continue
        premises = db_premise_confidences(con, x["id"])
        stored = db_confidence(con, x["id"])
        if not premises or stored is None:
            not_computed.append(base | {"reason": "no derives_from / acknowledged_derives_from premise with a stored confidence, or no stored confidence"})
            continue
        rec = v051_confidence(proposed, premises)
        computed.append(base | {"stored": stored, "recomputed": rec, "delta": rec - stored,
                                "n_premises": len(premises)})
    ds = [r["delta"] for r in computed]
    summary = ({"n": len(ds), "min": min(ds), "median": statistics.median(ds), "max": max(ds)}
               if ds else {"n": 0, "min": None, "median": None, "max": None})
    return {"computed": computed, "not_computed": not_computed, "summary": summary}


# ------------------------------------------------------------------ the whole analysis
def free_parameters(seed, prior_node, n_boot):
    """The choices every number in the report depends on, one short line each. Values are read
    from the module's constants and the run's arguments at call time, never retyped."""
    return {
        "small_stratum_rule": f"strata with fewer than {MIN_RATE_N} judgeable nodes report counts only (no rate, no interval)",
        "rate_denominator": "judgeable nodes = tight + loose + partial; cannot-judge nodes are excluded and counted beside each rate",
        "partial_bounds": "low bound counts partial as tight; high bound counts partial as loose",
        "interval": f"Wilson, z = {Z95}",
        "population_weights": "census population shares of each stratum, renormalised over strata with at least 1 judgeable node; "
                              "strata left out of the weights are listed under each weighted rate (no draw; no judgeable node)",
        "auc": f"P(conf(tight) > conf(loose)), ties count 0.5; bootstrap resamples the tight and loose groups separately, "
               f"{n_boot} resamples, percentile 95% interval, seed string {BOOT_SEED_FORMAT!r} with seed {seed!r}",
        "reading_thresholds": f"CI lower > 0.5: {READING_TRACKS!r}; CI contains 0.5: {READING_NONE!r}; "
                              f"CI upper < 0.5: {READING_AGAINST!r}; no tight or no loose node: {READING_NA!r}",
        "confidence_deltas": "premise set = derives_from + acknowledged_derives_from targets (tools/modus_ponens_check.py computed-from set); "
                             f"v0.5.1 formula from the vendored module (sha256 {VENDORED_SHA256}); computed once over all nodes",
        "readers": "rates and AUC use the primary reader's (Mira's) verdicts; Zephyr's feed controls and agreement only; "
                   f"analyst-prior node {prior_node} reported with and without",
    }


def run_analysis(mira, zephyr, controls, db, drawn, prior_node, seed, n_boot=N_BOOT):
    verify_vendored()
    d, census_pop, stratum_of = load_drawn(drawn)
    loose_ctl, tight_ctl = load_controls(controls, stratum_of)
    ctl = loose_ctl + tight_ctl
    if prior_node not in stratum_of:
        raise InputInvalid(f"--prior-node {prior_node!r} is not a sampled node")
    mrows = validate_verdicts(mira, set(stratum_of) | set(ctl), "mira")
    zrows = validate_verdicts(zephyr, set(d["zephyr"]) | set(ctl), "zephyr")

    con = open_ro(db)
    try:
        nodes, bad_conf, bad_decl = [], [], []
        for i in sorted(stratum_of):  # sampled ids only: controls never enter
            checks = mrows[i]
            x = {"id": i, "kind": kind_of(i), "stratum": stratum_of[i], "checks": checks,
                 "class": node_class(checks), "conf": None, "declared": None}
            if x["kind"] == "derivation":
                x["declared"] = db_declared_type(con, i)
                if x["declared"] != stratum_of[i].split(":", 1)[1]:
                    bad_decl.append(f"{i}: DB reasoning_type {x['declared']!r} != stratum {stratum_of[i]!r}")
            if x["class"] in ("tight", "loose"):
                x["conf"] = db_confidence(con, i)
                if x["conf"] is None:
                    bad_conf.append(i)
            nodes.append(x)
        if bad_decl or bad_conf:
            raise InputInvalid("; ".join(bad_decl + ([f"no stored confidence for joined nodes {bad_conf}"] if bad_conf else [])))
        strata_names = sorted(d["sampled"])
        passes = {
            "with_prior": analyze_pass(nodes, census_pop, strata_names, seed, "with_prior", n_boot),
            "without_prior": analyze_pass([x for x in nodes if x["id"] != prior_node], census_pop,
                                          strata_names, seed, "without_prior", n_boot),
        }
        deltas = deltas_block(con, nodes)
    finally:
        con.close()

    overlap = sorted(d["zephyr"])
    zeph_ids = sorted(zrows.keys() - set(ctl))
    report = {
        "meta": {"seed": seed, "prior_node": prior_node, "n_boot": n_boot, "min_rate_n": MIN_RATE_N,
                 "wilson_z": Z95, "vendored_sha256": VENDORED_SHA256,
                 "readings": {"tracks": READING_TRACKS, "none": READING_NONE, "against": READING_AGAINST},
                 "free_parameters": free_parameters(seed, prior_node, n_boot)},
        "validation": {"mira_rows": len(mrows), "zephyr_rows": len(zrows), "mira_sampled": len(stratum_of),
                       "zephyr_overlap": len(overlap), "controls": len(ctl)},
        "passes": passes,
        "deltas": deltas,
        "agreement": overlap_agreement(overlap, mrows, zrows),
        "cannot_judge": {"mira": cannot_judge_block(mrows, sorted(stratum_of)),
                         "zephyr": cannot_judge_block(zrows, zeph_ids)},
        "controls": controls_block(loose_ctl, tight_ctl, mrows, zrows),
    }
    return _round(report)


def _round(o):
    if isinstance(o, float):
        return round(o, 10)
    if isinstance(o, dict):
        return {k: _round(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_round(v) for v in o]
    return o


# ------------------------------------------------------------------ markdown
def pct(x):
    return "n/a" if x is None else f"{100 * x:.1f}%"


def num(x, nd=4):
    return "n/a" if x is None else f"{x:.{nd}f}"


def counts(r):
    return f"loose {r['loose']}, partial {r['partial']}, cannot-judge {r['cannot_judge']}, tight {r['tight']}"


def stratum_line(name, r):
    head = (f"- {name}: n={r['n']} (judgeable {r['n_judgeable']}; cannot-judge {r['cannot_judge']} "
            "left out of the denominator)")
    if "low" not in r:
        return f"{head}: counts only (fewer than {MIN_RATE_N} judgeable): {counts(r)}"
    lo, hi = r["low"], r["high"]
    return (f"{head}: low {pct(lo['rate'])} [Wilson {pct(lo['ci_low'])}, {pct(lo['ci_high'])}]; "
            f"high {pct(hi['rate'])} [Wilson {pct(hi['ci_low'])}, {pct(hi['ci_high'])}]; {counts(r)}")


def render_md(rep):
    L = []
    m = rep["meta"]
    L += ["# Node audit analysis report", "",
          f"Seed `{m['seed']}`; analyst-prior node `{m['prior_node']}`; bootstrap resamples {m['n_boot']}; "
          f"vendored v0.5.1 confidence module sha256 `{m['vendored_sha256']}`.",
          "Rates and confidence use the primary reader's (Mira's) verdicts on sampled nodes; controls are excluded from every rate.", "",
          "## Free parameters", ""]
    L += [f"- {v}" for v in m["free_parameters"].values()]
    L.append("")
    v = rep["validation"]
    L += ["## Validation", "",
          f"- Mira: {v['mira_rows']} rows ({v['mira_sampled']} sampled + {v['controls']} controls). "
          f"Zephyr: {v['zephyr_rows']} rows ({v['zephyr_overlap']} overlap + {v['controls']} controls). All rows valid; none dropped.", ""]
    L += ["## Cannot-judge counts (never folded into tight or loose)", ""]
    for who in ("mira", "zephyr"):
        cj = rep["cannot_judge"][who]
        L.append(f"### {who}")
        for k, cl in cj["per_class"].items():
            L.append(f"- {k} nodes by class: " + ", ".join(f"{c} {cl[c]}" for c in CLASSES))
        for name, vc in cj["per_check"].items():
            if sum(vc.values()):
                L.append(f"- check {name}: " + ", ".join(f"{x} {vc[x]}" for x in VERDICTS))
        L.append("")
    for pname, title in (("with_prior", "WITH the analyst-prior node"), ("without_prior", "WITHOUT the analyst-prior node")):
        p = rep["passes"][pname]
        L += [f"## Loose rates and confidence, {title}", ""]
        for kind in ("derivation", "observation"):
            k = p[kind]
            L += [f"### {kind}s: per-stratum loose rate", ""]
            L += [stratum_line(s, r) for s, r in k["strata"].items()]
            w = k["weighted"]
            L += ["", f"Population-weighted loose rate ({kind}s): low {pct(w['low'])}, high {pct(w['high'])} "
                      "(weights = census shares of strata with at least one judgeable node; no interval; "
                      f"cannot-judge nodes excluded from the denominator: {w['n_cannot_judge_excluded']}).",
                  f"Restricted to strata with at least {MIN_RATE_N} judgeable: low {pct(w['rated_strata_only']['low'])}, "
                  f"high {pct(w['rated_strata_only']['high'])}.",
                  "Strata with no drawn node (population shown): "
                  + (", ".join(f"{s} ({n})" for s, n in w["strata_without_draw"].items()) or "none"),
                  "Strata drawn but with no judgeable node (population shown): "
                  + (", ".join(f"{s} ({n})" for s, n in w["strata_all_cannot_judge"].items()) or "none"), ""]
            if kind == "derivation":
                L += ["inductive_generalization on its own:", stratum_line("derivation:inductive_generalization", k["inductive_generalization"]), "",
                      "Declared type x proposed type over `loose:type` verdicts:"]
                L += [f"- {a} -> {b}: {n}" for a, row in k["confusion"].items() for b, n in row.items()] or ["- none"]
                L.append("")
            c = k["confidence"]
            L += [f"### {kind}s: confidence vs verdict (small-n, exploratory)", "",
                  f"- tight n={c['n_tight']} mean {num(c['mean_tight'])}; loose n={c['n_loose']} mean {num(c['mean_loose'])}; "
                  f"excluded: partial {c['n_partial']}, cannot-judge {c['n_cannot_judge']}",
                  f"- AUC P(conf(tight) > conf(loose)): {num(c['auc'])}"
                  + (f", bootstrap 95% interval [{num(c['auc_ci'][0])}, {num(c['auc_ci'][1])}]" if c["auc_ci"] else ""),
                  f"- Reading: {c['reading']}", ""]
    d = rep["deltas"]
    s = d["summary"]
    L += ["## Confidence deltas (item 3b: v0.5.1 formula under the reader's proposed type)", "",
          f"n={s['n']}, min {num(s['min'])}, median {num(s['median'])}, max {num(s['max'])}", ""]
    L += [f"- {r['id']}: {r['declared_type']} -> {r['proposed_type']}: stored {num(r['stored'], 3)}, "
          f"recomputed {num(r['recomputed'], 3)}, delta {num(r['delta'])} ({r['n_premises']} premises)" for r in d["computed"]]
    L += [f"- {r['id']}: {r['declared_type']} -> {r['proposed_type']}: NOT computed ({r['reason']})" for r in d["not_computed"]]
    L.append("")
    a = rep["agreement"]
    L += ["## Agreement (overlap, controls excluded)", "",
          f"- node class (partial its own category): {a['n_agree']}/{a['n_overlap']} = {num(a['percent_agreement'], 1)}% agreement; kappa {num(a['kappa_class'])}",
          f"- tight vs loose, restricted to nodes both classed tight or loose (n={a['n_tight_loose_both']}): kappa {num(a['kappa_tight_loose'])}",
          "- per-check percent agreement:"]
    L += [f"  - {k}: {r['agree']}/{r['n']} = {num(r['percent_agreement'], 1)}%" for k, r in a["per_check"].items() if r["n"]]
    L += ["- disagreements (id: Mira / Zephyr):"]
    L += [f"  - {x['id']}: {x['mira']} / {x['zephyr']}" for x in a["disagreements"]] or ["  - none"]
    L.append("")
    c = rep["controls"]
    L += ["## Controls (revealed after both verdict sets were locked)", ""]
    for who in ("mira", "zephyr"):
        r = c[who]
        L += [f"### {who}", f"- sensitivity (known-loose classed loose): {r['sensitivity']['text']}",
              f"- specificity (known-tight classed tight): {r['specificity']['text']}",
              "- known-loose classes: " + ", ".join(f"{k} {r['known_loose_classes'][k]}" for k in CLASSES),
              "- known-tight classes: " + ", ".join(f"{k} {r['known_tight_classes'][k]}" for k in CLASSES),
              "- per control: " + ", ".join(f"{i} {k}" for i, k in r["per_control"].items()), ""]
    ca = c["agreement"]
    L += ["### Control agreement (separate from the overlap)",
          f"- {ca['agree']}/{ca['n']} = {num(ca['percent_agreement'], 1)}%; kappa {num(ca['kappa'])}",
          "- disagreements (id: Mira / Zephyr):"]
    L += [f"  - {x['id']}: {x['mira']} / {x['zephyr']}" for x in ca["disagreements"]] or ["  - none"]
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------ main
def repo_root():
    r = subprocess.run(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        return Path(r.stdout.strip()).resolve()
    for p in [HERE, *HERE.parents]:  # git unavailable: fail closed on the nearest .git
        if (p / ".git").exists():
            return p
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    for f in ("mira", "zephyr", "controls", "db", "drawn", "prior-node", "seed", "out"):
        ap.add_argument(f"--{f}", required=True)
    a = ap.parse_args(argv)

    out = Path(a.out).resolve()
    root = repo_root()
    if root is not None and (out == root or root in out.parents):
        raise OutputInsideWorktree(f"--out {out} is inside the git worktree {root}; the report must live outside it")
    rep = run_analysis(a.mira, a.zephyr, a.controls, a.db, a.drawn, a.prior_node, a.seed)
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(rep, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    (out / "report.md").write_text(render_md(rep))
    print(f"wrote {out / 'report.json'} and {out / 'report.md'}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AnalysisError as e:
        sys.exit(f"{type(e).__name__}: {e}")
