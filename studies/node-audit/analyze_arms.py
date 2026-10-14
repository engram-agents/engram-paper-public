#!/usr/bin/env python3
"""Pre-registered analysis of the two arms added by PROTOCOL.md Amendment 4: Arm A (the
author, Borges) and Arm B (Ariadne, a same-lineage non-author).

    analyze_arms.py --author-blind PATH --author-verdicts PATH --ariadne PATH
                    --ariadne-recognized PATH --mira PATH --zephyr PATH --controls PATH
                    --manifest PATH --packet PATH --db PATH --drawn PATH --filing-model PATH
                    --prior-node ID --seed TEXT --out DIR

Built and tested on SYNTHETIC data before any verdict is read. It IMPORTS analyze.py and reuses
its validation, node classes, kappa, Wilson interval, rate/AUC/delta/control helpers and its
public-export writer; analyze.py itself is unchanged (Amendment 4: it changes nothing in
analyze.py clauses 1-14). Stdlib only. `--manifest` is the private author-arm manifest,
{"control_mentions": {<sampled id>: [<control id>, ...]}, "n_sampled_nodes_mentioning_a_control": N};
`--packet` is the reader packet markdown (one `## Node i of n: <id>` block per node).

CONTRACT (each clause is asserted by tests/test_node_audit_analyze_arms.py)

 A1 Validation, refuse loudly, never drop; analyze.py clause-1 semantics. Ariadne's file: exactly
    the sampled ids plus all controls (as Mira's). The author's verdict file: exactly the sampled
    ids and NO control id. The blind file: rows {"id","blind_type","reason"} for exactly the
    sampled DERIVATION ids, each blind_type a name in analyze.PUBLISHABLE_TYPE_NAMES, each reason
    a string. The manifest: every key a sampled id, every listed value a control id, and the
    count equal to n_sampled_nodes_mentioning_a_control. The filing-model file must cover every
    sampled id, and the packet must hold exactly the sampled ids plus the controls. Any
    violation raises a named error listing EVERY offending item of that input file (a withheld
    value is never echoed: text that is not an id is named only by its position), the CLI exits
    non-zero, and nothing is written. Files are checked in turn, so a second bad file is reported
    after the first is fixed; each file has its own named error, as in analyze.py clause 1.
 A2 recognized.txt. Each non-empty line not starting with `#` must hold exactly one id-shaped
    token ((dv|ob)_\\d{4}, whole token); a line also holding the token LATE counts as late.
    RecognizedInvalid lists LINE NUMBERS ONLY, never line text or ids, for: zero ids, more than
    one id, an id outside the packet's ids, a duplicated id. The set may include control ids,
    which are COUNTED in the set comparison (A8) and NAMED only in the Controls section; the n of
    a set therefore includes its control ids, and the without-set passes drop sampled ids only.
 A3 Mention set: the ids of packet node blocks whose text matches (?i)ariadne|\\bari\\b. The report
    prints its n and the protocol's measured figure "41 of 211"; it does not assert equality.
    The matched text is never printed.
 A4 Blind-pass agreement (Arm A, the sampled derivations). Agree = blind_type equals the declared
    reasoning_type read from the DB as analyze.py reads it. k/n with a Wilson 95% interval
    overall, per stratum (drawn_ids.json) and per filing model (filing_model.json; nodes with
    hours_before > 24 are counted beside each model row as less_certain), plus a declared x
    blind confusion table. A group with fewer than 10 nodes reports counts only. Every figure
    is reported in four passes: all; without --prior-node; without the manifest's sampled ids;
    without both. The per-filing-model split is labelled `exploratory, not attribution`. Outputs
    that are not themselves pre-registered carry a status in json and md: the "without both" pass
    (here, in A6 and in A9) and A8's "without both sets" are `derived (combines pre-registered
    exclusions; not itself pre-registered)`; the Wilson intervals and the declared x blind table of
    the blind pass are `descriptive (not pre-registered)`. Passes the protocol names carry no
    status. The report opens with the five Amendment 4 reading rules, verbatim from PROTOCOL.md.
 A5 Self-naming. A blind-pass derivation names its own type if its claim or its logical chain
    (nodes.claim, nodes.logical_chain: the fields build_packet.py renders) contains its declared
    reasoning_type in underscore or space form, case-insensitive. Reported: the count, and the
    blind agreement re-computed without those nodes, in each A4 pass. The text is read for this
    boolean only and is never written anywhere.
 A6 Author agrees / disagrees. For each reader in {mira, ariadne, zephyr}, per check and summed,
    over the sampled nodes that reader judged: reader loose and author loose (author_agrees);
    reader loose and author tight (author_disagrees); reader loose and author cannot-judge
    (author_cannot_judge); the reverse cell, author loose and reader tight; and n_reader_loose,
    the denominator, which keeps the cannot-judge cell. Reported in the four A4 passes, with a
    per-filing-model split of every cell labelled `exploratory, not attribution`. Controls never
    enter (the author has no control rows).
 A7 Pairwise agreement on the sampled ids each pair shares: author-mira, author-ariadne,
    author-zephyr, ariadne-mira, ariadne-zephyr. Per pair: percent agreement and Cohen's kappa
    on node class (four categories, partial its own); kappa on tight vs loose restricted to
    nodes both classed tight or loose; per-check percent agreement and kappa. Agreement on the
    controls is a separate block, ariadne-mira and ariadne-zephyr only. Disagreement lists hold
    ids and labels only.
 A8 Ariadne's rates: analyze.py items 4-6 (loose rates per stratum with bounds and Wilson
    intervals, weighted rates, the inductive_generalization rate and confusion table, the
    confidence AUC and its reading) in five passes: all; without the prior node; without the
    recognized set; without the mention set; without both sets (their union). Her clause-7
    deltas on the full set only. A set comparison (recognized, mention, both, recognized-only,
    mention-only, late). Her controls: sensitivity and specificity as analyze.py clause 3.
 A9 The author's rates: analyze.py items 4-6 over the sampled ids in the four A4 passes. No
    controls, no sensitivity.
A10 No content in any output. No file under --out (the whole tree) contains any `reason` string
    from any verdict or blind file, any recognized.txt line text other than an id, any packet
    text, any DB claim or chain text, any controls-file note, or any proposed_type outside
    PUBLISHABLE_TYPE_NAMES (rendered as analyze.OTHER_TYPE). Control ids appear in the report
    only in its Controls section.
A11 Public export under out/public/: verdicts-ariadne.public.jsonl and verdicts-author.public.jsonl
    (exactly analyze.public_export_text, every row of the validated file, so Ariadne's include
    the control rows as Mira's do under analyze.py clause 14), and blind-author.public.jsonl,
    rows {"id","blind_type"} sorted by id, no reason. Byte-deterministic.
A12 meta.input_sha256 holds the sha256 of every input file (also printed in report_arms.md). The
    same inputs plus seed give byte-identical report_arms.json, report_arms.md and public
    files. Bootstrap seed labels are prefixed `arms:` so they never collide with analyze.py's.
A13 Writes are report_arms.json, report_arms.md and public/ under --out, which must resolve
    outside the git worktree holding this script (analyze.OutputInsideWorktree otherwise,
    nothing written).

The snapshot DB is opened read-only and used only for nodes.confidence, nodes.claim,
nodes.logical_chain, json_extract(metadata,'$.reasoning_type') and the edges analyze.py reads.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load_analyze():
    """Import analyze.py from this directory, reusing an already-imported copy of the same file
    so exception classes stay identical for any caller that imported it first."""
    target = HERE / "analyze.py"
    cached = sys.modules.get("analyze")
    if cached is not None and Path(getattr(cached, "__file__", None) or "").resolve() == target:
        return cached
    spec = importlib.util.spec_from_file_location("analyze", target)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


an = _load_analyze()

PASSES4 = ("all", "without_prior", "without_manifest", "without_both")
PASSES_ARIADNE = ("all", "without_prior", "without_recognized", "without_mention", "without_both_sets")
PROTOCOL_MENTION_FIGURE = "41 of 211"
SPLIT_LABEL = "exploratory, not attribution"
DERIVED_LABEL = "derived (combines pre-registered exclusions; not itself pre-registered)"
DESCRIPTIVE_LABEL = "descriptive (not pre-registered)"
# PROTOCOL.md Amendment 4, "Reading rules, fixed now": the five bullets, verbatim, printed at the top
# of report_arms.md. tests/test_node_audit_analyze_arms.py reads them back out of PROTOCOL.md itself.
READING_RULES = (
    "- **Author agrees** is read as an error made at filing time. The design cannot attribute it to a cause. "
    "Time pressure, an earlier model's habits, and the project's own changing practice over those months are all "
    "confounded, because in one author's transcripts each model occupied one continuous period. The per-model "
    "breakdown is reported, and it is not read as attribution.",
    "- **Author disagrees** is read as a standing disagreement between the author and that reader.",
    "- **Ariadne vs Mira and Zephyr** is read as a difference of lineage plus exposure, not of lineage alone. "
    "Being of the author's lineage and having read the author's posts arrive together in her.",
    "- **Ariadne vs the author** is read as an authorship difference within one lineage, with the same exposure "
    "caveat.",
    "- No result of these arms is read as showing which reader is right. Counts are reported beside every rate, "
    "and the small-stratum rule applies.",
)
INPUT_KEYS = ("author_blind", "author_verdicts", "ariadne", "ariadne_recognized", "mira", "zephyr",
              "controls", "manifest", "packet", "db", "drawn", "filing_model")
PAIRS = (("author", "mira"), ("author", "ariadne"), ("author", "zephyr"), ("ariadne", "mira"),
         ("ariadne", "zephyr"))
CELLS = ("author_agrees", "author_disagrees", "author_cannot_judge", "reverse_author_loose_reader_tight",
         "n_reader_loose")
LESS_CERTAIN_HOURS = 24

ID_TOKEN = re.compile(r"(?<![A-Za-z0-9_])(?:dv|ob)_\d{4}(?![A-Za-z0-9_])")
LATE_TOKEN = re.compile(r"(?<![A-Za-z0-9_])LATE(?![A-Za-z0-9_])")
NODE_HEADING = re.compile(r"^## Node \d+ of \d+: (\S+)[ \t]*$", re.M)
MENTION = re.compile(r"ariadne|\bari\b", re.I)


# ------------------------------------------------------------------ errors
class BlindFileInvalid(an.AnalysisError):
    pass


class ManifestInvalid(an.AnalysisError):
    pass


class RecognizedInvalid(an.AnalysisError):
    pass


def _refuse(exc, what, problems):
    body = "\n".join(f"  - {i}: {why}" for i, why in problems)
    raise exc(f"{what} is invalid ({len(problems)} problem(s)):\n{body}")


# ------------------------------------------------------------------ small input files
def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_text(path, exc, what):
    try:
        return Path(path).read_text()
    except (OSError, UnicodeDecodeError) as e:
        raise exc(f"{what}: cannot read the file ({type(e).__name__})") from None


def _read_json(path, exc, what):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError) as e:
        raise exc(f"{what}: cannot read as JSON ({type(e).__name__})") from None


def validate_blind(path, derivation_ids):
    """A1: {id: blind_type} for a blind file that is exactly right. Values are never echoed."""
    expected = set(derivation_ids)
    publishable = an.PUBLISHABLE_TYPE_NAMES
    text = _read_text(path, BlindFileInvalid, "blind file")
    rows, seen, problems = {}, set(), []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            problems.append((f"line {lineno}", "invalid JSON"))
            continue
        if not isinstance(obj, dict) or not isinstance(obj.get("id"), str):
            problems.append((f"line {lineno}", "row must be an object with a string id"))
            continue
        nid = obj["id"]
        if nid in seen:
            problems.append((nid, "duplicate id"))
        seen.add(nid)
        if nid not in expected:
            problems.append((nid, "unexpected id (not a sampled derivation)"))
        if set(obj) != {"id", "blind_type", "reason"}:
            problems.append((nid, f"keys {sorted(obj)} != ['blind_type', 'id', 'reason']"))
            continue
        ok = True
        if not (isinstance(obj["blind_type"], str) and obj["blind_type"] in publishable):
            problems.append((nid, "blind_type is not a name in PUBLISHABLE_TYPE_NAMES (value withheld)"))
            ok = False
        if not isinstance(obj["reason"], str):
            problems.append((nid, "reason is not a string"))
            ok = False
        if ok and nid in expected and nid not in rows:
            rows[nid] = obj["blind_type"]
    for nid in sorted(expected - seen):
        problems.append((nid, "missing id"))
    if problems:
        _refuse(BlindFileInvalid, "blind file", problems)
    return rows


def validate_manifest(path, sampled, controls):
    """A1: the set of sampled ids the manifest lists as mentioning a control."""
    m = _read_json(path, ManifestInvalid, "manifest")
    if not isinstance(m, dict) or not isinstance(m.get("control_mentions"), dict) \
            or "n_sampled_nodes_mentioning_a_control" not in m:
        raise ManifestInvalid("manifest must be an object with control_mentions and "
                              "n_sampled_nodes_mentioning_a_control")
    problems = []
    ctl, smp = set(controls), set(sampled)

    def named(x, where):
        """An id-shaped string is named; anything else is withheld (A1: a withheld value is never echoed)."""
        return x if isinstance(x, str) and ID_TOKEN.fullmatch(x) else f"<non-id text withheld, {where}>"

    for k, (nid, vals) in enumerate(m["control_mentions"].items(), 1):
        who = named(nid, f"key {k}")
        if nid not in smp:
            problems.append((who, "key is not a sampled id"))
        if not isinstance(vals, list) or not vals:
            problems.append((who, "value must be a non-empty list of control ids"))
            continue
        for j, v in enumerate(vals, 1):
            if not (isinstance(v, str) and v in ctl):
                problems.append((who, f"listed value {named(v, f'value {j}')} is not a control id"))
    declared, actual = m["n_sampled_nodes_mentioning_a_control"], len(m["control_mentions"])
    if type(declared) is not int or declared != actual:
        shown = repr(declared) if type(declared) is int else \
            f"<non-integer value withheld, type {type(declared).__name__}>"
        problems.append(("n_sampled_nodes_mentioning_a_control",
                         f"declares {shown} but control_mentions holds {actual} node(s)"))
    if problems:
        _refuse(ManifestInvalid, "manifest", problems)
    return set(m["control_mentions"])


def load_filing_model(path, sampled):
    """A1: {id: (filing_model, hours_before)} covering every sampled id."""
    f = _read_json(path, an.InputInvalid, "filing-model file")
    nodes = f.get("nodes") if isinstance(f, dict) else None
    if not isinstance(nodes, dict):
        raise an.InputInvalid("filing-model file lacks a `nodes` object")
    problems, out = [], {}
    for nid in sorted(sampled):
        r = nodes.get(nid)
        if r is None:
            problems.append((nid, "missing from the filing-model file"))
        elif not (isinstance(r, dict) and isinstance(r.get("filing_model"), str)
                  and isinstance(r.get("hours_before"), (int, float)) and not isinstance(r.get("hours_before"), bool)):
            problems.append((nid, "needs a string filing_model and a numeric hours_before"))
        else:
            out[nid] = (r["filing_model"], float(r["hours_before"]))
    if problems:
        _refuse(an.InputInvalid, "filing-model file", problems)
    return out


def parse_packet(text):
    """A3: {node id: block text}, a block running from its `## Node i of n: <id>` heading to the next."""
    heads = list(NODE_HEADING.finditer(text))
    if not heads:
        raise an.InputInvalid("packet holds no `## Node i of n: <id>` block")
    blocks, dupes = {}, []
    for k, h in enumerate(heads):
        end = heads[k + 1].start() if k + 1 < len(heads) else len(text)
        if h.group(1) in blocks:
            dupes.append(h.group(1))
        blocks[h.group(1)] = text[h.start():end]
    if dupes:
        raise an.InputInvalid(f"packet holds duplicate node blocks: {sorted(set(dupes))}")
    return blocks


def mention_set(blocks):
    return {nid for nid, block in blocks.items() if MENTION.search(block)}


def parse_recognized(path, packet_ids):
    """A2: (recognized ids, late ids). Refusals name line numbers only."""
    text = _read_text(path, RecognizedInvalid, "recognized file")
    first, late, problems = {}, set(), []
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        toks = ID_TOKEN.findall(s)
        if not toks:
            problems.append((f"line {n}", "no id"))
        elif len(toks) > 1:
            problems.append((f"line {n}", "more than one id"))
        elif toks[0] not in packet_ids:
            problems.append((f"line {n}", "id is not in the packet"))
        elif toks[0] in first:
            problems.append((f"line {n}", "duplicate of an earlier line's id"))
        else:
            first[toks[0]] = n
            if LATE_TOKEN.search(s):
                late.add(toks[0])
    if problems:
        raise RecognizedInvalid("recognized file is invalid ({} problem(s)); line numbers only, line text and ids "
                                "are never printed:\n".format(len(problems))
                                + "\n".join(f"  - {i}: {why}" for i, why in problems))
    return set(first), late


# ------------------------------------------------------------------ DB reads
def names_own_type(declared, claim, chain):
    """A5: does the claim or the logical chain contain the declared reasoning_type, in underscore
    or space form, case-insensitive? A boolean: the text is read here and goes nowhere else."""
    if not declared:
        return False
    low = declared.lower()
    text = f"{claim or ''}\n{chain or ''}".lower()
    return low in text or low.replace("_", " ") in text


def db_claim_chain(con, node_id):
    r = con.execute("SELECT claim, logical_chain FROM nodes WHERE id=?", (node_id,)).fetchone()
    return (None, None) if r is None else (r["claim"], r["logical_chain"])


# ------------------------------------------------------------------ small blocks
def group(k, n):
    """k of n with a Wilson interval, or counts only below the small-stratum threshold (A4)."""
    g = {"k": k, "n": n}
    if n >= an.MIN_RATE_N:
        lo, hi = an.wilson(k, n)
        g["rate"] = {"value": k / n, "ci_low": lo, "ci_high": hi}
    return g


def set_counts(s, controls):
    s = set(s)
    return {"n": len(s), "n_sampled": len(s - controls), "n_controls": len(s & controls)}


def blind_pass(nodes, derivation_strata):
    """A4 + A5 over the blind nodes of one pass."""
    agree = lambda xs: sum(1 for x in xs if x["agree"])  # noqa: E731
    by_stratum = {s: group(agree(xs), len(xs))
                  for s in derivation_strata for xs in [[x for x in nodes if x["stratum"] == s]]}
    by_model = {}
    for m in sorted({x["model"] for x in nodes}):
        xs = [x for x in nodes if x["model"] == m]
        by_model[m] = group(agree(xs), len(xs)) | {"less_certain": sum(1 for x in xs if x["hours"] > LESS_CERTAIN_HOURS)}
    confusion = {}
    for x in nodes:
        row = confusion.setdefault(x["declared"], {})
        row[x["blind"]] = row.get(x["blind"], 0) + 1
    rest = [x for x in nodes if not x["self_naming"]]
    return {"overall": group(agree(nodes), len(nodes)), "by_stratum": by_stratum,
            "by_filing_model": {"label": SPLIT_LABEL, "models": by_model},
            "confusion": {a: dict(sorted(b.items())) for a, b in sorted(confusion.items())},
            "status": {"wilson_intervals": DESCRIPTIVE_LABEL, "confusion": DESCRIPTIVE_LABEL},
            "self_naming": {"n_self_naming": len(nodes) - len(rest), "n": len(nodes),
                            "agreement_excluding": group(agree(rest), len(rest))}}


def _zero_cells():
    return {k: 0 for k in CELLS}


def author_vs_reader(author_rows, reader_rows, ids, model_of):
    """A6 over `ids` (sampled nodes the reader judged). Every reader-loose check lands in exactly one of
    three cells, so n_reader_loose keeps the author's cannot-judge cell in its denominator."""
    total, by_check, by_model = _zero_cells(), {c: _zero_cells() for c in an.ALL_CHECKS}, {}
    for i in ids:
        mcells = by_model.setdefault(model_of[i], _zero_cells())
        for name, rc in reader_rows[i].items():
            av, rv = author_rows[i][name]["verdict"], rc["verdict"]
            if rv == "loose":
                key = {"loose": "author_agrees", "tight": "author_disagrees",
                       "cannot-judge": "author_cannot_judge"}[av]
                hits = (key, "n_reader_loose")
            elif av == "loose" and rv == "tight":
                hits = ("reverse_author_loose_reader_tight",)
            else:
                continue
            for h in hits:
                total[h] += 1
                by_check[name][h] += 1
                mcells[h] += 1
    return {"total": total, "by_check": by_check,
            "by_filing_model": {"label": SPLIT_LABEL, "models": dict(sorted(by_model.items()))}}


def mark_derived(passes, name):
    """Label the one pass that is a union of two pre-registered exclusions. Only that pass is labelled:
    the registered passes carry no status, so nothing here claims a registration."""
    passes[name].setdefault("status", {})["pass"] = DERIVED_LABEL


def ariadne_controls(loose_ctl, tight_ctl, arows):
    """Clause 3's sensitivity/specificity block for Ariadne alone. analyze.controls_block compares two
    readers (Mira, Zephyr) and keys its per-reader block "mira"/"zephyr"; passing her rows as both and
    reading the "mira" key gives her block, and the self-comparison it also computes is discarded."""
    return an.controls_block(loose_ctl, tight_ctl, arows, arows)["mira"]


def class_agreement(ra, rb, ids, la, lb):
    ids = sorted(ids)
    ca, cb = [an.node_class(ra[i]) for i in ids], [an.node_class(rb[i]) for i in ids]
    agree = sum(x == y for x, y in zip(ca, cb))
    return {"n": len(ids), "n_agree": agree, "percent_agreement": 100 * agree / len(ids) if ids else None,
            "kappa": an.cohens_kappa(ca, cb),
            "disagreements": [{"id": i, la: x, lb: y} for i, x, y in zip(ids, ca, cb) if x != y]}


def pair_block(ra, rb, ids, la, lb):
    """A7 for one pair on the sampled ids they share."""
    ids = sorted(ids)
    classes = {i: (an.node_class(ra[i]), an.node_class(rb[i])) for i in ids}
    both = [i for i in ids if all(c in ("tight", "loose") for c in classes[i])]
    per_check = {}
    for name in an.ALL_CHECKS:
        kids = [i for i in ids if name in ra[i] and name in rb[i]]
        va, vb = [ra[i][name]["verdict"] for i in kids], [rb[i][name]["verdict"] for i in kids]
        ag = sum(x == y for x, y in zip(va, vb))
        per_check[name] = {"n": len(kids), "n_agree": ag,
                           "percent_agreement": 100 * ag / len(kids) if kids else None,
                           "kappa": an.cohens_kappa(va, vb)}
    return {"n_shared": len(ids), "class": class_agreement(ra, rb, ids, la, lb),
            "tight_loose": {"n": len(both), "kappa": an.cohens_kappa([classes[i][0] for i in both],
                                                                    [classes[i][1] for i in both])},
            "per_check": per_check}


# ------------------------------------------------------------------ the whole analysis
def build_nodes(con, rows, stratum_of, declared):
    """analyze.py's node dicts for one reader over the sampled ids (controls never enter)."""
    nodes, bad_conf = [], []
    for i in sorted(stratum_of):
        checks = rows[i]
        x = {"id": i, "kind": an.kind_of(i), "stratum": stratum_of[i], "checks": checks,
             "class": an.node_class(checks), "conf": None, "declared": declared.get(i)}
        if x["class"] in ("tight", "loose"):
            x["conf"] = an.db_confidence(con, i)
            if x["conf"] is None:
                bad_conf.append(i)
        nodes.append(x)
    return nodes, bad_conf


def analyze_arms(paths, prior_node, seed, n_boot):
    """Validate every input, then compute. Returns (report, {public file name: text}); raises before
    anything is written."""
    an.verify_vendored()
    d, census_pop, stratum_of = an.load_drawn(paths["drawn"])
    loose_ctl, tight_ctl = an.load_controls(paths["controls"], stratum_of)
    ctl = loose_ctl + tight_ctl
    ctl_set, sampled = set(ctl), set(stratum_of)
    if prior_node not in sampled:
        raise an.InputInvalid(f"--prior-node {prior_node!r} is not a sampled node")
    derivations = sorted(i for i in sampled if an.kind_of(i) == "derivation")

    # A1: every input, before any computation
    mrows = an.validate_verdicts(paths["mira"], sampled | ctl_set, "mira")
    zrows = an.validate_verdicts(paths["zephyr"], set(d["zephyr"]) | ctl_set, "zephyr")
    arows = an.validate_verdicts(paths["ariadne"], sampled | ctl_set, "ariadne")
    urows = an.validate_verdicts(paths["author_verdicts"], sampled, "author")
    blind = validate_blind(paths["author_blind"], derivations)
    manifest_ids = validate_manifest(paths["manifest"], sampled, ctl)
    filing = load_filing_model(paths["filing_model"], sampled)
    blocks = parse_packet(_read_text(paths["packet"], an.InputInvalid, "packet"))
    if set(blocks) != sampled | ctl_set:
        raise an.InputInvalid(f"packet node ids differ from the sampled ids plus controls: missing "
                              f"{sorted((sampled | ctl_set) - set(blocks))}, extra "
                              f"{sorted(set(blocks) - sampled - ctl_set)}")
    recognized, late = parse_recognized(paths["ariadne_recognized"], set(blocks))
    mention = mention_set(blocks)

    strata_names = sorted(d["sampled"])
    derivation_strata = [s for s in strata_names if s.startswith("derivation:")]
    model_of = {i: filing[i][0] for i in sampled}
    sample_ids = sorted(sampled)
    zeph_ids = sorted(d["zephyr"])
    excl4 = {"all": set(), "without_prior": {prior_node}, "without_manifest": set(manifest_ids),
             "without_both": {prior_node} | set(manifest_ids)}
    excl_ari = {"all": set(), "without_prior": {prior_node}, "without_recognized": set(recognized),
                "without_mention": set(mention), "without_both_sets": set(recognized) | set(mention)}

    try:
        con = an.open_ro(paths["db"])
        try:
            declared, bad_decl = {}, []
            blind_nodes = []
            for i in derivations:
                declared[i] = an.db_declared_type(con, i)
                if declared[i] != stratum_of[i].split(":", 1)[1]:
                    bad_decl.append(f"{i}: DB reasoning_type {declared[i]!r} != stratum {stratum_of[i]!r}")
                    continue
                claim, chain = db_claim_chain(con, i)
                blind_nodes.append({"id": i, "stratum": stratum_of[i], "declared": declared[i], "blind": blind[i],
                                    "agree": blind[i] == declared[i], "model": filing[i][0], "hours": filing[i][1],
                                    "self_naming": names_own_type(declared[i], claim, chain)})
            if bad_decl:
                raise an.InputInvalid("; ".join(bad_decl))
            ari_nodes, bad_a = build_nodes(con, arows, stratum_of, declared)
            aut_nodes, bad_u = build_nodes(con, urows, stratum_of, declared)
            if bad_a or bad_u:
                raise an.InputInvalid(f"no stored confidence for joined nodes {sorted(set(bad_a + bad_u))}")
            ari_passes = {p: an.analyze_pass([x for x in ari_nodes if x["id"] not in ex], census_pop, strata_names,
                                             seed, f"arms:ariadne:{p}", n_boot) for p, ex in excl_ari.items()}
            aut_passes = {p: an.analyze_pass([x for x in aut_nodes if x["id"] not in ex], census_pop, strata_names,
                                             seed, f"arms:author:{p}", n_boot) for p, ex in excl4.items()}
            deltas = an.deltas_block(con, ari_nodes)
        finally:
            con.close()
    except sqlite3.Error as e:
        raise an.InputInvalid(f"snapshot DB could not be read ({type(e).__name__}: {e})") from None

    readers = {"mira": (mrows, sample_ids), "ariadne": (arows, sample_ids), "zephyr": (zrows, zeph_ids)}
    avr = {who: {p: author_vs_reader(urows, rows, [i for i in ids if i not in ex], model_of)
                 for p, ex in excl4.items()} for who, (rows, ids) in readers.items()}
    allrows = {"author": urows, "ariadne": arows, "mira": mrows, "zephyr": zrows}
    ids_of = {"author": sample_ids, "ariadne": sample_ids, "mira": sample_ids, "zephyr": zeph_ids}
    pairs = {}
    for a, b in PAIRS:
        shared = sorted(set(ids_of[a]) & set(ids_of[b]))
        pairs[f"{a}_{b}"] = pair_block(allrows[a], allrows[b], shared, a, b)
    ari_ctl = ariadne_controls(loose_ctl, tight_ctl, arows)
    controls = {
        "ariadne": ari_ctl,
        "pairs": {f"ariadne_{b}": class_agreement(arows, allrows[b], ctl, "ariadne", b) for b in ("mira", "zephyr")},
        "recognized_control_ids": sorted(recognized & ctl_set),
        "mention_control_ids": sorted(mention & ctl_set),
    }
    both_sets = recognized & mention
    blind_passes = {p: blind_pass([x for x in blind_nodes if x["id"] not in ex], derivation_strata)
                    for p, ex in excl4.items()}
    for passes in (blind_passes, aut_passes, *avr.values()):
        mark_derived(passes, "without_both")
    mark_derived(ari_passes, "without_both_sets")
    report = {
        "meta": {"seed": seed, "prior_node": prior_node, "n_boot": n_boot, "min_rate_n": an.MIN_RATE_N,
                 "wilson_z": an.Z95, "vendored_sha256": an.VENDORED_SHA256,
                 "n_manifest_nodes": len(manifest_ids),
                 "input_sha256": {k: file_sha256(paths[k]) for k in INPUT_KEYS},
                 "passes": {"blind_author_readers": list(PASSES4), "ariadne": list(PASSES_ARIADNE)}},
        "validation": {"sampled": len(sampled), "blind_rows": len(blind), "author_rows": len(urows),
                       "ariadne_rows": len(arows), "mira_rows": len(mrows), "zephyr_rows": len(zrows),
                       "packet_nodes": len(blocks), "controls": len(ctl)},
        "mention_set": set_counts(mention, ctl_set) | {"n_packet_nodes": len(blocks),
                                                       "protocol_measured": PROTOCOL_MENTION_FIGURE},
        "blind": blind_passes,
        "author_vs_reader": avr,
        "pairs": pairs,
        "ariadne": {"passes": ari_passes, "deltas": deltas,
                    "sets": {"recognized": set_counts(recognized, ctl_set), "mention": set_counts(mention, ctl_set),
                             "both": set_counts(both_sets, ctl_set),
                             "recognized_only": set_counts(recognized - mention, ctl_set),
                             "mention_only": set_counts(mention - recognized, ctl_set),
                             "late": set_counts(late, ctl_set)}},
        "author": {"passes": aut_passes},
        "controls": controls,
    }
    public = {
        "verdicts-ariadne.public.jsonl": an.public_export_text(arows),
        "verdicts-author.public.jsonl": an.public_export_text(urows),
        "blind-author.public.jsonl": "".join(
            json.dumps({"id": i, "blind_type": blind[i]}, sort_keys=True, separators=(",", ":")) + "\n"
            for i in sorted(blind)),
    }
    return an._round(report), public


# ------------------------------------------------------------------ markdown
def fmt_group(g):
    s = f"{g['k']}/{g['n']}"
    if "rate" in g:
        r = g["rate"]
        s += f" = {an.pct(r['value'])} [Wilson {an.pct(r['ci_low'])}, {an.pct(r['ci_high'])}]"
    else:
        s += f" (counts only: fewer than {an.MIN_RATE_N})"
    return s + (f"; less certain (hours_before > {LESS_CERTAIN_HOURS}): {g['less_certain']}" if "less_certain" in g else "")


def fmt_cells(c):
    return (f"author agrees {c['author_agrees']}, author disagrees {c['author_disagrees']}, author cannot-judge "
            f"{c['author_cannot_judge']}, reverse (author loose, reader tight) {c['reverse_author_loose_reader_tight']}; "
            f"reader-loose total {c['n_reader_loose']}")


def status_lines(block):
    """The registration labels a pass block carries (none for the passes the protocol names)."""
    st = block.get("status", {})
    out = []
    if "pass" in st:
        out.append(f"- Status of this pass: {st['pass']}")
    if "wilson_intervals" in st:
        out.append(f"- Status of the Wilson intervals below: {st['wilson_intervals']}")
    if "confusion" in st:
        out.append(f"- Status of the declared -> blind table below: {st['confusion']}")
    return out + [""] if out else out


def render_rates(L, p, heading):
    for kind in ("derivation", "observation"):
        k = p[kind]
        L += [f"{heading} {kind}s: per-stratum loose rate", ""]
        L += [an.stratum_line(s, r) for s, r in k["strata"].items()]
        w = k["weighted"]
        L += ["", f"Population-weighted loose rate ({kind}s): low {an.pct(w['low'])}, high {an.pct(w['high'])} "
                  f"(cannot-judge nodes excluded from the denominator: {w['n_cannot_judge_excluded']}); restricted to "
                  f"strata with at least {an.MIN_RATE_N} judgeable: low {an.pct(w['rated_strata_only']['low'])}, "
                  f"high {an.pct(w['rated_strata_only']['high'])}.", ""]
        if kind == "derivation":
            L += ["inductive_generalization on its own:",
                  an.stratum_line("derivation:inductive_generalization", k["inductive_generalization"]), "",
                  "Declared type x proposed type over `loose:type` verdicts:"]
            L += [f"- {a} -> {b}: {n}" for a, row in k["confusion"].items() for b, n in row.items()] or ["- none"]
            L.append("")
        c = k["confidence"]
        L += [f"- {kind}s confidence: tight n={c['n_tight']} mean {an.num(c['mean_tight'])}; loose n={c['n_loose']} mean "
              f"{an.num(c['mean_loose'])}; excluded: partial {c['n_partial']}, cannot-judge {c['n_cannot_judge']}",
              f"- AUC P(conf(tight) > conf(loose)): {an.num(c['auc'])}"
              + (f", bootstrap 95% interval [{an.num(c['auc_ci'][0])}, {an.num(c['auc_ci'][1])}]" if c["auc_ci"] else ""),
              f"- Reading: {c['reading']}", ""]


def render_md(rep):
    L = []
    m = rep["meta"]
    L += ["# Node audit analysis report: Arm A (author) and Arm B (Ariadne)", "",
          "## Reading rules (PROTOCOL.md Amendment 4, \"Reading rules, fixed now\", verbatim)", "",
          *READING_RULES, "",
          f"Seed `{m['seed']}`; analyst-prior node `{m['prior_node']}`; bootstrap resamples {m['n_boot']}; small-stratum "
          f"rule: fewer than {m['min_rate_n']} nodes report counts only. Controls are excluded from every rate. "
          f"{m['n_manifest_nodes']} sampled nodes mention a control (the private manifest).", "",
          "Pass labels: a pass labelled \"derived\" is a union of two pre-registered exclusions and is not itself "
          "named in the protocol; items labelled \"descriptive\" are not pre-registered. Unlabelled passes are the "
          "ones the protocol names.", "",
          "## Input files (sha256)", ""]
    L += [f"- {k}: `{v}`" for k, v in m["input_sha256"].items()]
    v = rep["validation"]
    L += ["", "## Validation", "",
          f"- {v['sampled']} sampled nodes, {v['controls']} controls, {v['packet_nodes']} packet nodes. Rows: blind "
          f"{v['blind_rows']}, author {v['author_rows']}, ariadne {v['ariadne_rows']}, mira {v['mira_rows']}, "
          f"zephyr {v['zephyr_rows']}. All rows valid; none dropped.", ""]
    ms = rep["mention_set"]
    s = rep["ariadne"]["sets"]
    L += ["## Mention set and recognized set (counts only)", "",
          f"- Mention set (packet node blocks matching `ariadne|\\bari\\b`, case-insensitive): {ms['n']} of "
          f"{ms['n_packet_nodes']}; the protocol's measured figure is {ms['protocol_measured']} (not asserted here).",
          f"- recognized {s['recognized']['n']}, mention {s['mention']['n']}, both {s['both']['n']}, recognized-only "
          f"{s['recognized_only']['n']}, mention-only {s['mention_only']['n']}, late {s['late']['n']}; control ids "
          f"counted in recognized {s['recognized']['n_controls']}, mention {s['mention']['n_controls']}.", ""]
    L += ["## Arm A blind pass: agreement with the declared type, and self-naming", ""]
    for p in PASSES4:
        b = rep["blind"][p]
        L += [f"### pass: {p}", ""] + status_lines(b)
        L += [f"- overall: {fmt_group(b['overall'])}", "- per stratum:"]
        L += [f"  - {s_}: {fmt_group(g)}" for s_, g in b["by_stratum"].items()]
        L += [f"- per filing model ({b['by_filing_model']['label']}):"]
        L += [f"  - {mm}: {fmt_group(g)}" for mm, g in b["by_filing_model"]["models"].items()]
        L += ["- declared -> blind:"] + [f"  - {a} -> {c}: {n}" for a, row in b["confusion"].items() for c, n in row.items()]
        sn = b["self_naming"]
        L += [f"- self-naming (claim or chain contains the declared type): {sn['n_self_naming']} of {sn['n']}; "
              f"agreement without them: {fmt_group(sn['agreement_excluding'])}", ""]
    L += ["## Author agrees / disagrees, per reader", ""]
    for who in ("mira", "ariadne", "zephyr"):
        for p in PASSES4:
            a = rep["author_vs_reader"][who][p]
            L += [f"### {who}, pass: {p}", ""] + status_lines(a) + [f"- all checks: {fmt_cells(a['total'])}"]
            L += [f"- {c}: {fmt_cells(r)}" for c, r in a["by_check"].items()]
            L += [f"- per filing model ({a['by_filing_model']['label']}):"]
            L += [f"  - {mm}: {fmt_cells(r)}" for mm, r in a["by_filing_model"]["models"].items()]
            L.append("")
    L += ["## Pairwise agreement (shared sampled nodes)", ""]
    for name, b in rep["pairs"].items():
        c = b["class"]
        L += [f"### {name} (n={b['n_shared']})", "",
              f"- node class (partial its own category): {c['n_agree']}/{c['n']} = {an.num(c['percent_agreement'], 1)}%; "
              f"kappa {an.num(c['kappa'])}",
              f"- tight vs loose (n={b['tight_loose']['n']}): kappa {an.num(b['tight_loose']['kappa'])}",
              "- per check:"]
        L += [f"  - {k}: {r['n_agree']}/{r['n']} = {an.num(r['percent_agreement'], 1)}%; kappa {an.num(r['kappa'])}"
              for k, r in b["per_check"].items() if r["n"]]
        a, bb = name.split("_")
        L += [f"- disagreements (id: {a} / {bb}):"]
        L += [f"  - {x['id']}: {x[a]} / {x[bb]}" for x in c["disagreements"]] or ["  - none"]
        L.append("")
    L += ["## Ariadne's rates", ""]
    for p in PASSES_ARIADNE:
        L += [f"### pass: {p}", ""] + status_lines(rep["ariadne"]["passes"][p])
        render_rates(L, rep["ariadne"]["passes"][p], "####")
    d = rep["ariadne"]["deltas"]
    sm = d["summary"]
    L += ["### Confidence deltas (item 3b; full set only)", "",
          f"n={sm['n']}, min {an.num(sm['min'])}, median {an.num(sm['median'])}, max {an.num(sm['max'])}", ""]
    L += [f"- {r['id']}: {r['declared_type']} -> {r['proposed_type']}: stored {an.num(r['stored'], 3)}, recomputed "
          f"{an.num(r['recomputed'], 3)}, delta {an.num(r['delta'])} ({r['n_premises']} premises)" for r in d["computed"]]
    L += [f"- {r['id']}: {r['declared_type']} -> {r['proposed_type']}: NOT computed ({r['reason']})"
          for r in d["not_computed"]]
    L += ["", "## Author's rates", ""]
    for p in PASSES4:
        L += [f"### pass: {p}", ""] + status_lines(rep["author"]["passes"][p])
        render_rates(L, rep["author"]["passes"][p], "####")
    c = rep["controls"]
    a = c["ariadne"]
    L += ["## Controls (revealed after every reader had locked)", "", "### ariadne",
          f"- sensitivity (known-loose classed loose): {a['sensitivity']['text']}",
          f"- specificity (known-tight classed tight): {a['specificity']['text']}",
          "- known-loose classes: " + ", ".join(f"{k} {a['known_loose_classes'][k]}" for k in an.CLASSES),
          "- known-tight classes: " + ", ".join(f"{k} {a['known_tight_classes'][k]}" for k in an.CLASSES),
          "- per control: " + ", ".join(f"{i} {k}" for i, k in a["per_control"].items()),
          "- control ids in her recognized file: " + (", ".join(c["recognized_control_ids"]) or "none"),
          "- control ids in the mention set: " + (", ".join(c["mention_control_ids"]) or "none"), "",
          "### Control agreement (the author has no control rows)"]
    for name, b in c["pairs"].items():
        x, y = name.split("_")
        L += [f"- {name}: {b['n_agree']}/{b['n']} = {an.num(b['percent_agreement'], 1)}%; kappa {an.num(b['kappa'])}",
              f"  - disagreements (id: {x} / {y}):"]
        L += [f"    - {r['id']}: {r[x]} / {r[y]}" for r in b["disagreements"]] or ["    - none"]
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------ main
def main(argv=None, n_boot=an.N_BOOT):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    flags = {"author_blind": "--author-blind", "author_verdicts": "--author-verdicts", "ariadne": "--ariadne",
             "ariadne_recognized": "--ariadne-recognized", "mira": "--mira", "zephyr": "--zephyr",
             "controls": "--controls", "manifest": "--manifest", "packet": "--packet", "db": "--db",
             "drawn": "--drawn", "filing_model": "--filing-model"}
    for f in flags.values():
        ap.add_argument(f, required=True)
    for f in ("--prior-node", "--seed", "--out"):
        ap.add_argument(f, required=True)
    a = ap.parse_args(argv)

    out = Path(a.out).resolve()
    root = an.repo_root()
    if root is not None and (out == root or root in out.parents):
        raise an.OutputInsideWorktree(f"--out {out} is inside the git worktree {root}; the report must live outside it")
    paths = {k: getattr(a, k) for k in flags}
    rep, public = analyze_arms(paths, a.prior_node, a.seed, n_boot)
    out.mkdir(parents=True, exist_ok=True)
    (out / "report_arms.json").write_text(json.dumps(rep, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    (out / "report_arms.md").write_text(render_md(rep))
    (out / "public").mkdir(exist_ok=True)
    for name, text in public.items():
        (out / "public" / name).write_text(text)
    print(f"wrote {out / 'report_arms.json'}, {out / 'report_arms.md'} and {out / 'public'}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except an.AnalysisError as e:
        sys.exit(f"{type(e).__name__}: {e}")
