#!/usr/bin/env python3
"""Seeded stratified sampler and packet builder for the independent node audit
(paper v2, workstream D; protocol: D-audit-protocol.md).

    build_packet.py --db PATH --seed TEXT --out DIR --controls PATH
                    [--draw-only] [--author-arm] [--drawn-ids PATH] [--expect-sha256 HEX]

CONTRACT (each clause is asserted by tests/test_node_audit_sampler.py)

1. Population. Current derivations whose declared reasoning_type is in the v0.5.1
   table (14 types) are sampled. Current derivations with a NULL type, or a type
   outside the table, are census lines and never sampled. Observations: current
   `observation_factual` nodes, stratified by quote_type. `observation_predictive`
   is a census line, never sampled. EVERY CONTROL ID IS REMOVED FROM THE POPULATION
   before drawing.
2. Strata, deterministic from --seed. Each stratum is drawn with
   random.Random(seed + ":" + stratum) from its sorted candidate ids.
     * inductive_generalization: 50.
     * the other 13 types: 90 in total, allocated by the largest-remainder method in
       proportion to population, floor 2 for every type with >= 2 nodes, capped at the
       type's population; if the floors push the total over 90, the excess is taken
       one node at a time from the largest strata. A 1-node type has no floor.
     * observations: 60 by quote_type, same method.
   The allocation is computed on the census (pre-control-removal) populations so that
   drawn_ids.json reveals nothing about the controls; it is then capped at the number
   of non-control candidates actually available.
   Zephyr's overlap (50): 25 drawn from the drawn IG 50 plus 25 drawn from the other
   150 drawn nodes, seeded.
3. Controls (known_loose U known_tight_placement_verified U known_tight_final) are
   inserted into BOTH packets, at seeded positions, in exactly the format of sampled
   nodes. A control id is never a sampled id (asserted).
4. Packet content per node: id, type, claim; derivations: declared reasoning_type,
   logical_chain, every linked node's full text with its relation label; observations:
   quoted_text, interpretation, quote_type, source_class and the evidence node's
   source identity. Only whitelisted keys are ever read into a packet, and the
   assembled packet is asserted to hold no key named like confidence/importance/
   recall/utility and no non-string leaf value.
5. Outputs. --out must resolve outside the git worktree that holds this script
   (refused otherwise). It receives packet_mira.md, packet_zephyr.md,
   verdict_template.jsonl, TYPE_TABLE.md. drawn_ids.json (default: next to this
   script, committed) holds seed, allocation, sampled ids per stratum, Zephyr's 50 and
   the census, and no control id. --draw-only writes only drawn_ids.json.
6. Determinism. Same DB + seed + controls -> byte-identical drawn_ids.json. A
   different seed gives a different draw.

AUTHOR ARM (--author-arm; PROTOCOL.md Amendment 4, "Arm A, the author"). Same inputs as above.
Writes ONLY packet_author_blind.md, blind_template.jsonl, packet_author_verdict.md,
verdict_template_author.jsonl and TYPE_TABLE.md under --out, and no reader packet.
drawn_ids.json is written exactly as in the default mode. Refused together with --draw-only.
  A1 No control in either author packet. No control id appears anywhere in any author-mode
     output: not as a node, not in a linked-node heading, not in claim text. A control can be
     a premise of a sampled node, so this is a real possibility. The build REFUSES with
     AuthorPacketLeak, listing every (file, line, id), before any author file is written. It
     never drops or redacts a link: what to do about a leak is the analyst's decision.
  A2 Declared type withheld in the blind packet. No line of packet_author_blind.md starts with
     "- declared reasoning_type:" and blind_template.jsonl has no reasoning_type key. Reasoning
     words inside a node's own claim or chain text are content and are NOT redacted.
  A3 Blind set = exactly the derivations among the sampled ids (observations have no
     reasoning type; no control). Order: Mira's order, filtered to those derivations.
  A4 Verdict packet parity. packet_author_verdict.md holds all sampled ids and no control, in
     Mira's order (the random.Random(f"{seed}:order:mira") shuffle of sampled U controls)
     with the controls removed. Each node block equals its block in packet_mira.md except
     the "## Node i of n" numbering, here n = the sampled count.
  A5 Confidence withheld: the same assert_packet_clean covers author-mode nodes.
  A6 Deterministic: same inputs, byte-identical files.
  A7 The default mode's output is byte-unchanged by the author arm
     (tests/test_node_audit_author_packets.py holds golden hashes taken from the code
     before the arm was added).

The snapshot is opened read-only and its sha256 must match; a DB whose current
derivations have empty claim text (the stripped shape) is refused.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

SNAPSHOT_SHA256 = "adaa6a84828b761ab2e5bf269e1ea4d48366c7e713b73c0c0918bf5ce3fbef85"

IG = "inductive_generalization"
N_IG, N_OTHER, N_OBS, N_ZEPHYR, N_ZEPHYR_IG = 50, 90, 60, 50, 25
TYPE_FLOOR = 2

# v0.5.1 reasoning-type table (verbatim from the spec; deductive_conjunction postdates v0.5.1).
TYPE_TABLE = [
    ("deductive_modus_ponens", "If P then Q; P; therefore Q"),
    ("deductive_modus_tollens", "If P then Q; not Q; therefore not P"),
    ("deductive_hypothetical_syllogism", "If P→Q and Q→R; therefore P→R"),
    ("deductive_disjunctive", "P or Q; not P; therefore Q"),
    ("deductive_reductio", "Assume P; derive contradiction; therefore not P"),
    ("inductive_generalization", "Observed X in A,B,C → X generally true. REQUIRES 2+ distinct evidence sources."),
    ("inductive_enumeration", "Source S enumerates items I1,I2,...,In sharing property P → P has n instances (single authoritative source, structurally-independent items)"),
    ("inductive_statistical", "X% of A are B; this is A; therefore probably B"),
    ("inductive_analogy", "A~B in X,Y,Z; A has W; therefore B has W"),
    ("inductive_causal", "A precedes B + mechanism → A causes B"),
    ("abductive_best_explanation", "Observations → hypothesis that best explains them"),
    ("abductive_elimination", "Hypotheses H1,H2,H3; rule out H1,H2 → H3"),
    ("authority_expert", "Expert X says P → P is probably true"),
    ("authority_consensus", "Multiple independent sources agree → probably true"),
]
TYPES = [t for t, _ in TYPE_TABLE]
TYPE_TABLE_MD = "## Reasoning types (ENGRAM v0.5.1)\n\n" + "\n".join(f"- {t}: {d}" for t, d in TYPE_TABLE) + "\n"

# ---- packet whitelist: the ONLY keys ever read from a node row into a packet ----
NODE_FIELDS = {
    "derivation": ("id", "type", "claim", "reasoning_type", "logical_chain"),
    "observation": ("id", "type", "claim", "quoted_text", "interpretation", "quote_type", "source_class"),
}
LINK_FIELDS = ("id", "type", "claim", "quoted_text", "interpretation")
EVIDENCE_FIELDS = ("source_title", "source_url", "source_domain", "source_type")
FORBIDDEN_KEY = re.compile(r"confidence|importance|recall|utility", re.I)

RELATION_LABEL = {
    "derives_from": "premise",
    "acknowledged_derives_from": "acknowledged replacement (acknowledged_derives_from)",
    "cites": "context (cites)",
}
OMITTED_RELATIONS = ("supersedes", "retracts")

CHECKS = {
    "derivation": ("type", "placement", "chain-overreach"),
    "observation": ("support-overreach", "quote_type", "source_class"),
}


class AuditError(Exception):
    """A refusal with a name; the tool never improvises past one."""


class AuthorPacketLeak(AuditError):
    """A control id appears in an author-arm output (A1). Never silently dropped or redacted."""


class StrippedSnapshotError(AuditError):
    """The DB has no claim text on its current derivations (the data/*.stripped.db shape)."""


# ------------------------------------------------------------------ allocation
def allocate(pops: dict, total: int) -> dict:
    """Largest-remainder allocation of `total` over strata, floor TYPE_FLOOR for strata of
    >= 2 nodes, capped at population; excess is taken one at a time from the largest."""
    pops = {k: v for k, v in pops.items() if v > 0}
    if sum(pops.values()) <= total:
        return dict(pops)
    tot = sum(pops.values())
    exact = {k: total * v / tot for k, v in pops.items()}
    a = {k: int(exact[k]) for k in pops}
    left = total - sum(a.values())
    for k in sorted(pops, key=lambda k: (-(exact[k] - a[k]), k))[:left]:
        a[k] += 1
    lo = {k: (TYPE_FLOOR if pops[k] >= 2 else 0) for k in pops}
    lo = {k: min(lo[k], pops[k]) for k in pops}
    for k in a:
        a[k] = min(max(a[k], lo[k]), pops[k])
    while sum(a.values()) > total:
        k = max((k for k in a if a[k] > lo[k]), key=lambda k: (a[k], k), default=None)
        if k is None:
            break
        a[k] -= 1
    while sum(a.values()) < total:
        cand = [k for k in a if a[k] < pops[k]]
        if not cand:
            break
        k = max(cand, key=lambda k: (exact[k] - a[k], k))
        a[k] += 1
    return a


# ------------------------------------------------------------------ DB access
def _file_sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def open_ro(path) -> sqlite3.Connection:
    con = sqlite3.connect(f"file:{Path(path).resolve()}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


_SEL = ("SELECT *, json_extract(metadata,'$.reasoning_type') AS reasoning_type, "
        "json_extract(metadata,'$.source_class') AS source_class FROM nodes")


def fetch(con, node_id):
    r = con.execute(_SEL + " WHERE id=?", (node_id,)).fetchone()
    return dict(r) if r else None


def load_population(con):
    der, obs = {}, {}
    for r in con.execute("SELECT id, json_extract(metadata,'$.reasoning_type') AS rt FROM nodes "
                         "WHERE type='derivation' AND is_current=1 ORDER BY id"):
        der[r["id"]] = r["rt"]
    for r in con.execute("SELECT id, quote_type FROM nodes WHERE type='observation_factual' "
                         "AND is_current=1 ORDER BY id"):
        obs[r["id"]] = r["quote_type"] if r["quote_type"] is not None else "(null)"
    n_pred = con.execute("SELECT COUNT(*) FROM nodes WHERE type='observation_predictive' "
                         "AND is_current=1").fetchone()[0]
    return der, obs, n_pred


def refuse_if_stripped(con):
    n = con.execute("SELECT COUNT(*) FROM nodes WHERE type='derivation' AND is_current=1 "
                    "AND (claim IS NULL OR TRIM(claim)='')").fetchone()[0]
    if n:
        raise StrippedSnapshotError(
            f"{n} current derivations have empty claim text: this is a stripped snapshot, "
            "not the full one; the audit needs claim text")


def load_controls(path):
    c = json.loads(Path(path).read_text())
    loose = set(c.get("known_loose", {}))
    tight = set(c.get("known_tight_placement_verified", {})) | set(c.get("known_tight_final", []))
    if loose & tight:
        raise AuditError("a control id is listed as both known-loose and known-tight")
    return sorted(loose | tight)


# ------------------------------------------------------------------ drawing
def draw(seed, der, obs, n_pred, controls):
    ctl = set(controls)
    cen_der_type = {}
    for rt in der.values():
        if rt is not None:
            cen_der_type[rt] = cen_der_type.get(rt, 0) + 1
    cen_obs = {}
    for qt in obs.values():
        cen_obs[qt] = cen_obs.get(qt, 0) + 1
    census = {
        "derivation_current": len(der),
        "derivation_null_type": sum(1 for rt in der.values() if rt is None),
        "derivation_type_outside_table": {t: n for t, n in sorted(cen_der_type.items()) if t not in TYPES},
        "derivation_by_type": {t: cen_der_type.get(t, 0) for t in TYPES},
        "observation_factual_current": len(obs),
        "observation_factual_by_quote_type": dict(sorted(cen_obs.items())),
        "observation_predictive": n_pred,
    }
    alloc, sampled = {}, {}

    def stratum(name, ids, n):
        pool = sorted(i for i in ids if i not in ctl)
        n = min(n, len(pool))
        alloc[name] = n
        sampled[name] = sorted(random.Random(f"{seed}:{name}").sample(pool, n)) if n else []

    by_type = {t: sorted(i for i, rt in der.items() if rt == t) for t in TYPES}
    stratum(f"derivation:{IG}", by_type[IG], N_IG)
    others = {t: len(by_type[t]) for t in TYPES if t != IG}
    for t, n in allocate(others, N_OTHER).items():
        stratum(f"derivation:{t}", by_type[t], n)
    by_qt = {}
    for i, qt in obs.items():
        by_qt.setdefault(qt, []).append(i)
    for qt, n in allocate({q: len(v) for q, v in by_qt.items()}, N_OBS).items():
        stratum(f"observation:{qt}", by_qt[qt], n)
    allsampled = {i for v in sampled.values() for i in v}
    assert not (allsampled & ctl), "a control id was sampled"
    ig_ids = sorted(sampled[f"derivation:{IG}"])
    rest = sorted(allsampled - set(ig_ids))
    zeph = (random.Random(f"{seed}:zephyr:ig").sample(ig_ids, min(N_ZEPHYR_IG, len(ig_ids))) +
            random.Random(f"{seed}:zephyr:rest").sample(rest, min(N_ZEPHYR - N_ZEPHYR_IG, len(rest))))
    return census, alloc, sampled, sorted(zeph)


# ------------------------------------------------------------------ packet
def node_kind(row):
    if row["type"] == "derivation":
        return "derivation"
    if row["type"].startswith("observation"):
        return "observation"
    raise AuditError(f"node {row['id']} has type {row['type']!r}; only derivations and observations are auditable")


def build_node(con, node_id):
    row = fetch(con, node_id)
    if row is None:
        raise AuditError(f"node {node_id} is not in the snapshot")
    kind = node_kind(row)
    node = {k: row[k] for k in NODE_FIELDS[kind]}
    node["kind"] = kind
    if kind == "derivation":
        links = []
        for e in con.execute("SELECT target_id, relation FROM edges WHERE source_id=? ORDER BY relation, target_id",
                             (node_id,)):
            if e["relation"] in OMITTED_RELATIONS:
                continue
            t = fetch(con, e["target_id"])
            if t is None:
                continue
            link = {k: t[k] for k in LINK_FIELDS}
            link["relation"] = RELATION_LABEL.get(e["relation"], e["relation"])
            links.append(link)
        node["links"] = links
    else:
        ev = fetch(con, row["evidence_id"]) if row["evidence_id"] else None
        node["evidence"] = {k: (ev[k] if ev else None) for k in EVIDENCE_FIELDS}
    return node


def assert_packet_clean(obj, path="packet"):
    """No key named like a computed number, and no non-string leaf (a number cannot ride along)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if FORBIDDEN_KEY.search(str(k)):
                raise AuditError(f"forbidden key {k!r} at {path}")
            assert_packet_clean(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            assert_packet_clean(v, f"{path}[{i}]")
    elif obj is not None and not isinstance(obj, str):
        raise AuditError(f"non-string value {obj!r} at {path}")


def _q(text):
    return "\n".join("> " + ln for ln in (text if text is not None else "(none)").split("\n"))


def render_node(i, n, node, blind=False):
    """`blind=True` omits the declared-reasoning_type line and the blank line after it (A2)."""
    out = [f"## Node {i} of {n}: {node['id']}", "", f"- id: {node['id']}", f"- type: {node['type']}", "",
           "claim:", _q(node["claim"]), ""]
    if node["kind"] == "derivation":
        if not blind:
            out += [f"- declared reasoning_type: {node['reasoning_type'] or '(none declared)'}", ""]
        out += ["logical chain:", _q(node["logical_chain"]), ""]
        out.append(f"linked nodes ({len(node['links'])}):")
        for lk in node["links"]:
            out += ["", f"### {lk['relation']}: {lk['id']} ({lk['type']})", "claim:", _q(lk["claim"])]
            if lk["quoted_text"] is not None or lk["interpretation"] is not None:
                out += ["quoted_text:", _q(lk["quoted_text"]), "interpretation:", _q(lk["interpretation"])]
        out.append("")
    else:
        ev = node["evidence"]
        out += ["quoted_text:", _q(node["quoted_text"]), "", "interpretation:", _q(node["interpretation"]), "",
                f"- quote_type: {node['quote_type']}", f"- source_class: {node['source_class']}",
                f"- source_title: {ev['source_title']}", f"- source_url: {ev['source_url']}",
                f"- source_domain: {ev['source_domain']}", f"- source_type: {ev['source_type']}", ""]
    return "\n".join(out)


def template_line(node):
    checks = {c: {"verdict": None, "reason": None} for c in CHECKS[node["kind"]]}
    if node["kind"] == "derivation":
        checks["type"]["proposed_type"] = None
    return json.dumps({"id": node["id"], "checks": checks}, ensure_ascii=False)


HEADER = ("# Node audit packet\n\nFor each node below, give every check its own verdict: tight, loose or "
          "cannot-judge, plus one line of reasoning (derivations: type, placement, chain-overreach; "
          "observations: support-overreach, quote_type, source_class; when type is loose, give your "
          "proposed_type). Judge declared labels against the table below.\n\n")


def write_packets(con, seed, sampled_ids, zeph, controls, out):
    nodes = {i: build_node(con, i) for i in set(sampled_ids) | set(controls)}
    assert_packet_clean(list(nodes.values()))
    out.mkdir(parents=True, exist_ok=True)
    (out / "TYPE_TABLE.md").write_text(TYPE_TABLE_MD)
    for who, ids in (("mira", sorted(sampled_ids)), ("zephyr", sorted(zeph))):
        order = sorted(set(ids) | set(controls))
        random.Random(f"{seed}:order:{who}").shuffle(order)  # controls land at seeded positions
        body = "\n".join(render_node(k + 1, len(order), nodes[i]) for k, i in enumerate(order))
        (out / f"packet_{who}.md").write_text(HEADER + TYPE_TABLE_MD + "\n" + body)
        (out / ("verdict_template.jsonl" if who == "mira" else f"verdict_template_{who}.jsonl")).write_text(
            "\n".join(template_line(nodes[i]) for i in order) + "\n")


BLIND_HEADER = ("# Node audit packet: author blind pass\n\nFor each derivation, write the reasoning type you "
                "would file now, from the table below; the declared type is withheld. Fill in "
                "blind_template.jsonl (blind_type, reason).\n\n")
DECLARED_LINE = "- declared reasoning_type:"


def control_occurrences(name, text, controls):
    """Every (file name, 1-based line, control id) where a control id occurs as a whole token."""
    hits = []
    for cid in controls:
        pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(cid) + r"(?![A-Za-z0-9_])")
        for ln, line in enumerate(text.split("\n"), 1):
            hits += [(name, ln, cid)] * len(pat.findall(line))
    return sorted(hits)


def write_author_packets(con, seed, sampled_ids, controls, out):
    sampled = sorted(sampled_ids)
    nodes = {i: build_node(con, i) for i in sampled}
    assert_packet_clean(list(nodes.values()))
    order = sorted(set(sampled) | set(controls))
    random.Random(f"{seed}:order:mira").shuffle(order)
    order = [i for i in order if i in set(sampled)]  # Mira's order, controls removed
    blind_ids = [i for i in order if nodes[i]["kind"] == "derivation"]
    body_b = "\n".join(render_node(k + 1, len(blind_ids), nodes[i], blind=True) for k, i in enumerate(blind_ids))
    body_v = "\n".join(render_node(k + 1, len(order), nodes[i]) for k, i in enumerate(order))
    files = {
        "packet_author_blind.md": BLIND_HEADER + TYPE_TABLE_MD + "\n" + body_b,
        "blind_template.jsonl": "".join(
            json.dumps({"id": i, "blind_type": None, "reason": None}, ensure_ascii=False) + "\n"
            for i in blind_ids),
        "packet_author_verdict.md": HEADER + TYPE_TABLE_MD + "\n" + body_v,
        "verdict_template_author.jsonl": "\n".join(template_line(nodes[i]) for i in order) + "\n",
        "TYPE_TABLE.md": TYPE_TABLE_MD,
    }
    if (any(ln.startswith(DECLARED_LINE) for ln in files["packet_author_blind.md"].split("\n"))
            or "reasoning_type" in files["blind_template.jsonl"]):
        raise AuditError("the declared reasoning_type reached the blind packet")
    hits = [h for name, text in files.items() for h in control_occurrences(name, text, controls)]
    if hits:
        raise AuthorPacketLeak(
            f"{len(hits)} control-id occurrence(s) in author-arm output; nothing was written:\n" +
            "\n".join(f"  {name}:{ln}: {cid}" for name, ln, cid in hits))
    out.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (out / name).write_text(text)


# ------------------------------------------------------------------ main
def repo_root():
    here = Path(__file__).resolve().parent
    r = subprocess.run(["git", "-C", str(here), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(r.stdout.strip()).resolve() if r.returncode == 0 else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--db", required=True)
    ap.add_argument("--seed", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--controls", required=True)
    ap.add_argument("--draw-only", action="store_true")
    ap.add_argument("--author-arm", action="store_true",
                    help="write only the Arm A (author) blind and verdict packets")
    ap.add_argument("--drawn-ids", default=str(Path(__file__).resolve().parent / "drawn_ids.json"))
    ap.add_argument("--expect-sha256", default=SNAPSHOT_SHA256)
    a = ap.parse_args(argv)
    if a.author_arm and a.draw_only:
        raise AuditError("--author-arm cannot be combined with --draw-only (the arm writes packets)")

    out = Path(a.out).resolve()
    root = repo_root()
    if root is not None and (out == root or root in out.parents):
        raise AuditError(f"--out {out} is inside the git worktree {root}; packets are private and must live outside it")
    got = _file_sha256(a.db)
    if got != a.expect_sha256:
        raise AuditError(f"snapshot sha256 mismatch: got {got}, expected {a.expect_sha256}")
    con = open_ro(a.db)
    refuse_if_stripped(con)
    controls = load_controls(a.controls)
    der, obs, n_pred = load_population(con)
    for cid in controls:
        if con.execute("SELECT 1 FROM nodes WHERE id=?", (cid,)).fetchone() is None:
            raise AuditError(f"control id {cid} is not in the snapshot")
    census, alloc, sampled, zeph = draw(a.seed, der, obs, n_pred, controls)
    drawn = {"seed": a.seed, "snapshot_sha256": got, "census": census, "allocation": alloc,
             "sampled": sampled, "zephyr": zeph}
    Path(a.drawn_ids).write_text(json.dumps(drawn, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    if a.author_arm:
        write_author_packets(con, a.seed, [i for v in sampled.values() for i in v], controls, out)
    elif not a.draw_only:
        write_packets(con, a.seed, [i for v in sampled.values() for i in v], zeph, controls, out)
    print(f"allocation (seed {a.seed!r}):")
    for k, v in alloc.items():
        print(f"  {k}: {v}")
    print(f"drawn: {sum(alloc.values())}; zephyr: {len(zeph)}; controls removed/inserted: {len(controls)}")
    print("census:")
    for k, v in census.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AuditError as e:
        sys.exit(f"{type(e).__name__}: {e}")
