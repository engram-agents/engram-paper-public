"""Contract tests for `studies/node-audit/analyze_arms.py` (PROTOCOL.md Amendment 4: Arm A,
the author, and Arm B, Ariadne).

Written BEFORE the implementation (contract-first). Clause numbers A1-A13 match the tool's
module docstring. SYNTHETIC data only: every input is built inside the test; no real
verdict, packet, control file, manifest or snapshot is ever read.

Synthetic world (every expectation below is hand-computed from these definitions):
  derivation strata: IG n=12 (dv_0101-0112), MP n=10 (dv_0201-0210), AN n=6 (dv_0301-0306)
  observation strata: HD n=8 (ob_0101-0108), ED n=4 (ob_0201-0204)
  census populations: IG 100 / MP 60 / AN 40; HD 80 / ED 20
  controls: dv_0901 dv_0902 ob_0901 (known loose), dv_0903 ob_0902 (known tight)
  analyst-prior node: dv_0101;  manifest nodes: dv_0102, dv_0203, ob_0101
  Zephyr's overlap: dv_0101-0104, dv_0201, dv_0202, ob_0101, ob_0102

Blind pass (28 derivations), 8 disagree with the declared type:
  IG: dv_0102 dv_0105 -> inductive_enumeration, dv_0110 -> inductive_statistical  (9/12 agree)
  MP: dv_0203 dv_0207 -> deductive_hypothetical_syllogism                        (8/10)
  AN: dv_0302 dv_0304 dv_0306 -> inductive_causal                                (3/6)
Filing models: IG 0101-04 4-6, 0105-08 4-7, 0109-12 5; MP 0201-05 4-6, 0206-10 4-8;
  AN 0301-03 4-7, 0304-06 4-8; HD 0101-04 4-6, 0105-08 4-8; ED all 5.
  hours_before > 24: dv_0105 (30.0), dv_0206 (25.5), ob_0203 (100.0); dv_0304 is exactly 24.0.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
AUDIT = REPO / "studies" / "node-audit"
TOOL = AUDIT / "analyze_arms.py"
ANALYZE = AUDIT / "analyze.py"
SEED = "arms-synthetic-seed"
PRIOR = "dv_0101"
N_BOOT = 200
PLACEHOLDER = "other (not a v0.5.1 type; text withheld)"  # literal on purpose: not read from the tool


def _load():
    spec = importlib.util.spec_from_file_location("analyze_arms", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["analyze_arms"] = mod
    spec.loader.exec_module(mod)
    return mod


arms = _load()
an = arms.an  # the analyze module the tool actually imports (exception classes must match)

PASSES4 = ("all", "without_prior", "without_manifest", "without_both")
PASSES_ARI = ("all", "without_prior", "without_recognized", "without_mention", "without_both_sets")
DER_CHECKS = ("type", "placement", "chain-overreach")
OBS_CHECKS = ("support-overreach", "quote_type", "source_class")


# ------------------------------------------------------------------ synthetic world
def ids(prefix, lo, hi):
    return [f"{prefix}{i:04d}" for i in range(lo, hi + 1)]


IG, MP, AN = ids("dv_", 101, 112), ids("dv_", 201, 210), ids("dv_", 301, 306)
HD, ED = ids("ob_", 101, 108), ids("ob_", 201, 204)
SAMPLED_BY_STRATUM = {
    "derivation:inductive_generalization": IG,
    "derivation:deductive_modus_ponens": MP,
    "derivation:inductive_analogy": AN,
    "observation:hard_data": HD,
    "observation:editorial": ED,
}
DERIVATIONS = IG + MP + AN
SAMPLED = DERIVATIONS + HD + ED
ZEPH = ["dv_0101", "dv_0102", "dv_0103", "dv_0104", "dv_0201", "dv_0202", "ob_0101", "ob_0102"]
CTL_LOOSE = ["dv_0901", "dv_0902", "ob_0901"]
CTL_TIGHT_PV = ["dv_0903"]
CTL_TIGHT_FINAL = ["ob_0902"]
CTL_ALL = CTL_LOOSE + CTL_TIGHT_PV + CTL_TIGHT_FINAL
MANIFEST_IDS = ["dv_0102", "dv_0203", "ob_0101"]
DECLARED = {**{i: "inductive_generalization" for i in IG}, **{i: "deductive_modus_ponens" for i in MP},
            **{i: "inductive_analogy" for i in AN}}
STRATUM_OF = {i: s for s, v in SAMPLED_BY_STRATUM.items() for i in v}
DRAWN = {
    "seed": "drawn-seed",
    "allocation": {k: len(v) for k, v in SAMPLED_BY_STRATUM.items()},
    "sampled": SAMPLED_BY_STRATUM,
    "zephyr": ZEPH,
    "census": {
        "derivation_by_type": {"inductive_generalization": 100, "deductive_modus_ponens": 60,
                               "inductive_analogy": 40},
        "observation_factual_by_quote_type": {"hard_data": 80, "editorial": 20},
    },
}

BLIND_DISAGREE = {"dv_0102": "inductive_enumeration", "dv_0105": "inductive_enumeration",
                  "dv_0110": "inductive_statistical", "dv_0203": "deductive_hypothetical_syllogism",
                  "dv_0207": "deductive_hypothetical_syllogism", "dv_0302": "inductive_causal",
                  "dv_0304": "inductive_causal", "dv_0306": "inductive_causal"}

M46, M47, M48, M5 = "claude-opus-4-6", "claude-opus-4-7", "claude-opus-4-8", "claude-opus-5"
MODEL_OF = {}
for _ids, _m in ((IG[0:4], M46), (IG[4:8], M47), (IG[8:12], M5), (MP[0:5], M46), (MP[5:10], M48),
                 (AN[0:3], M47), (AN[3:6], M48), (HD[0:4], M46), (HD[4:8], M48), (ED, M5)):
    for _i in _ids:
        MODEL_OF[_i] = _m
HOURS = {"dv_0105": 30.0, "dv_0206": 25.5, "dv_0304": 24.0, "ob_0203": 100.0}

# DB text: every claim/chain carries SENTINEL; a few name their own declared type.
CLAIM_EXTRA = {"dv_0103": "this is Inductive_Generalization at work",      # underscore form, mixed case
               "dv_0302": "an inductive_analogy of the cases",             # underscore form
               "dv_0201": "unlike inductive_generalization, this is exact",  # another type: non-match
               "dv_0108": "an inductive generalisation of the cases"}      # near miss spelling: non-match
CHAIN_EXTRA = {"dv_0104": "an inductive generalization of cases",          # space form, in the chain only
               "dv_0205": "so, by Deductive Modus Ponens, it follows"}      # space form, mixed case
SELF_NAMING = {"dv_0103", "dv_0302", "dv_0104", "dv_0205"}

PACKET_EXTRA = {"dv_0105": "Ariadne wrote this note", "dv_0110": "see ariadne's earlier post",
                "ob_0102": "Ari said so", "dv_0902": "ARIADNE", "dv_0106": "Aria, variables and Mario"}
MENTION = {"dv_0105", "dv_0110", "ob_0102", "dv_0902"}
RECOGNIZED = {"dv_0101", "dv_0105", "dv_0201", "dv_0903"}
LATE = {"dv_0201"}
RECOGNIZED_TEXT = (
    "# recognized.txt SENTINEL_REC header comment dv_0777\n"
    "dv_0101 SENTINEL_REC recognised this one\n"
    "\n"
    "dv_0105 SENTINEL_REC she is named in it\n"
    "dv_0201 LATE SENTINEL_REC added after judging\n"
    "dv_0903 SENTINEL_REC she half-remembered this\n")


def vrows(who, node_ids, over):
    """Verdict rows: every check tight unless `over[id][check]` says otherwise; a (verdict,
    proposed_type) tuple sets a loose type. Every reason carries SENTINEL."""
    out = []
    for nid in node_ids:
        names = DER_CHECKS if nid.startswith("dv_") else OBS_CHECKS
        o = over.get(nid, {})
        checks = {}
        for c in names:
            v = o.get(c, "tight")
            prop = None
            if isinstance(v, tuple):
                v, prop = v
            checks[c] = {"verdict": v, "reason": f"SENTINEL_REASON_{who}_{nid}_{c}"}
            if c == "type":
                checks[c]["proposed_type"] = prop
        out.append({"id": nid, "checks": checks})
    return out


MIRA_OVER = {
    "dv_0101": {"type": ("loose", "deductive_modus_ponens"), "placement": "loose"},
    "dv_0102": {"placement": "loose"}, "dv_0201": {"placement": "loose"},
    "dv_0301": {"type": ("loose", "SENTINEL_PT_MIRA free text")}, "dv_0110": {"type": ("loose", "inductive_statistical")},
    "ob_0101": {"quote_type": "loose"}, "ob_0201": {"support-overreach": "loose"},
    "ob_0102": {"source_class": "loose"},
    "dv_0901": {"placement": "loose"}, "dv_0902": {"placement": "loose"}, "ob_0901": {"quote_type": "loose"},
}
AUTHOR_OVER = {
    "dv_0101": {"type": ("loose", "SENTINEL_PT free text"), "placement": "cannot-judge"},
    "dv_0102": {"placement": "loose"}, "dv_0201": {"chain-overreach": "loose"},
    "dv_0301": {"type": "cannot-judge"}, "dv_0105": {"placement": "loose"},
    "ob_0101": {"quote_type": "loose"}, "ob_0201": {"support-overreach": "cannot-judge"},
}
ARIADNE_OVER = {
    "dv_0101": {"type": ("loose", "inductive_enumeration")},
    "dv_0105": {"placement": "loose", "type": ("loose", "SENTINEL_PT_ARIADNE free text")},
    "ob_0101": {"quote_type": "loose"},
    "dv_0901": {"placement": "loose"}, "ob_0901": {"support-overreach": "loose"},
}
ZEPH_OVER = {
    "dv_0101": {"type": ("loose", "SENTINEL_PT_ZEPH free text")}, "ob_0101": {"quote_type": "loose"},
    "dv_0201": {"chain-overreach": "loose"},
    "dv_0901": {"placement": "loose"}, "dv_0902": {"placement": "loose"},
}


def write_jsonl(path, rows):
    Path(path).write_text("".join(json.dumps(r) + "\n" for r in rows))
    return path


def blind_rows(over=None):
    over = over or {}
    return [{"id": i, "blind_type": BLIND_DISAGREE.get(i, DECLARED[i]),
             "reason": f"SENTINEL_REASON_BLIND_{i}"} | over.get(i, {}) for i in DERIVATIONS]


def packet_text(extra=None, node_ids=None):
    extra = PACKET_EXTRA if extra is None else extra
    order = list(node_ids if node_ids is not None else SAMPLED + CTL_ALL)
    random.Random(7).shuffle(order)
    parts = ["# Node audit packet\n\nSENTINEL_PACKET header\n"]
    for k, i in enumerate(order, 1):
        parts.append(f"## Node {k} of {len(order)}: {i}\n\n- id: {i}\n\nclaim:\n> SENTINEL_PACKET claim of {i}"
                     f" {extra.get(i, '')}\n")
    return "\n".join(parts)


def make_db(path):
    c = sqlite3.connect(path)
    c.executescript(
        "CREATE TABLE nodes (id TEXT PRIMARY KEY, type TEXT, confidence REAL, metadata TEXT, claim TEXT,"
        " logical_chain TEXT);"
        "CREATE TABLE edges (id INTEGER PRIMARY KEY, source_id TEXT, target_id TEXT, relation TEXT);")
    loose_low = {"dv_0101", "dv_0102", "dv_0105", "dv_0201", "ob_0101", "ob_0102"}
    for i in SAMPLED + CTL_ALL:
        md = json.dumps({"reasoning_type": DECLARED[i]}) if i in DECLARED else "{}"
        conf = 0.931 if i == "dv_0101" else (0.6 if i in loose_low else 0.85)
        c.execute("INSERT INTO nodes VALUES (?,?,?,?,?,?)",
                  (i, "derivation" if i.startswith("dv_") else "observation_factual", conf, md,
                   f"SENTINEL_CLAIM_{i} {CLAIM_EXTRA.get(i, '')}", f"SENTINEL_CHAIN_{i} {CHAIN_EXTRA.get(i, '')}"))
    for i, v in {"pm1": 0.9, "pm2": 0.8}.items():
        c.execute("INSERT INTO nodes VALUES (?,?,?,?,?,?)", (i, "observation_factual", v, "{}", "SENTINEL_PM", ""))
    for t in ("pm1", "pm2"):
        c.execute("INSERT INTO edges (source_id, target_id, relation) VALUES ('dv_0101', ?, 'derives_from')", (t,))
    c.commit()
    c.close()
    return path


def controls_obj():
    return {"known_loose": {i: "SENTINEL_NOTE_" + i for i in CTL_LOOSE},
            "known_tight_placement_verified": {i: "SENTINEL_NOTE_" + i for i in CTL_TIGHT_PV},
            "known_tight_final": CTL_TIGHT_FINAL, "other_key": {"ignored": "SENTINEL_NOTE_other"}}


def manifest_obj():
    return {"control_mentions": {"dv_0102": ["dv_0901"], "dv_0203": ["dv_0902", "dv_0903"], "ob_0101": ["ob_0901"]},
            "n_sampled_nodes_mentioning_a_control": 3}


def filing_obj():
    return {"n": len(SAMPLED), "rule": "synthetic",
            "nodes": {i: {"filing_model": MODEL_OF[i], "hours_before": HOURS.get(i, 0.0)} for i in SAMPLED}}


FILES = {"author_blind": "author_blind.jsonl", "author_verdicts": "author_verdicts.jsonl",
         "ariadne": "ariadne.jsonl", "ariadne_recognized": "recognized.txt", "mira": "mira.jsonl",
         "zephyr": "zephyr.jsonl", "controls": "controls.json", "manifest": "manifest.json",
         "packet": "packet.md", "db": "snap.db", "drawn": "drawn.json", "filing_model": "filing_model.json"}


@pytest.fixture
def world(tmp_path):
    w = tmp_path / "w"
    w.mkdir()
    write_jsonl(w / FILES["author_blind"], blind_rows())
    write_jsonl(w / FILES["author_verdicts"], vrows("author", SAMPLED, AUTHOR_OVER))
    write_jsonl(w / FILES["ariadne"], vrows("ariadne", SAMPLED + CTL_ALL, ARIADNE_OVER))
    (w / FILES["ariadne_recognized"]).write_text(RECOGNIZED_TEXT)
    write_jsonl(w / FILES["mira"], vrows("mira", SAMPLED + CTL_ALL, MIRA_OVER))
    write_jsonl(w / FILES["zephyr"], vrows("zephyr", ZEPH + CTL_ALL, ZEPH_OVER))
    (w / FILES["controls"]).write_text(json.dumps(controls_obj()))
    (w / FILES["manifest"]).write_text(json.dumps(manifest_obj()))
    (w / FILES["packet"]).write_text(packet_text())
    make_db(w / FILES["db"])
    (w / FILES["drawn"]).write_text(json.dumps(DRAWN))
    (w / FILES["filing_model"]).write_text(json.dumps(filing_obj()))
    return w


FLAGS = {"author_blind": "--author-blind", "author_verdicts": "--author-verdicts", "ariadne": "--ariadne",
         "ariadne_recognized": "--ariadne-recognized", "mira": "--mira", "zephyr": "--zephyr",
         "controls": "--controls", "manifest": "--manifest", "packet": "--packet", "db": "--db",
         "drawn": "--drawn", "filing_model": "--filing-model"}


def args_for(w, out, prior=PRIOR):
    a = []
    for k, f in FLAGS.items():
        a += [f, str(w / FILES[k])]
    return a + ["--prior-node", prior, "--seed", SEED, "--out", str(out)]


def run(w, out, **kw):
    return arms.main(args_for(w, out, **kw), n_boot=N_BOOT)


def load_report(out):
    return json.loads((Path(out) / "report_arms.json").read_text())


@pytest.fixture
def out(world, tmp_path):
    o = tmp_path / "out"
    run(world, o)
    return o


@pytest.fixture
def rep(out):
    return load_report(out)


def all_files(out):
    return sorted(p for p in Path(out).rglob("*") if p.is_file())


def read_lines(path):
    return [json.loads(x) for x in Path(path).read_text().splitlines()]


# ------------------------------------------------------------------ analyze.py untouched
# sha256 of studies/node-audit/analyze.py as it stands on main at 392a0b7
# (`git show 392a0b7:studies/node-audit/analyze.py | sha256sum`). A literal, so a COMMITTED edit
# fails here too; comparing to `git show HEAD:` only ever caught uncommitted ones (Amendment 4:
# analyze.py clauses 1-14 do not change).
ANALYZE_PY_SHA256_AT_392A0B7 = "675116a487da292ed4931b400b3b2e5e8c674751928ae954bbea4b3034b9e95b"


def test_analyze_py_is_byte_unchanged_since_392a0b7():
    assert hashlib.sha256(ANALYZE.read_bytes()).hexdigest() == ANALYZE_PY_SHA256_AT_392A0B7


def test_clauses_a1_to_a13_are_in_the_module_docstring():
    doc = arms.__doc__
    for n in range(1, 14):
        assert re.search(rf"^ *A{n}\b", doc, re.M), f"A{n} missing from the module docstring"


def test_every_flag_is_required(world, tmp_path):
    for flag in list(FLAGS.values()) + ["--prior-node", "--seed", "--out"]:
        a = args_for(world, tmp_path / "o")
        k = a.index(flag)
        del a[k:k + 2]
        with pytest.raises(SystemExit) as e:
            arms.main(a, n_boot=N_BOOT)
        assert e.value.code == 2, flag


# ------------------------------------------------------------------ A1 validation
def refused(world, tmp_path, exc):
    o = tmp_path / "refused"
    with pytest.raises(exc) as e:
        run(world, o)
    assert not o.exists(), "a refusal must write nothing"
    return str(e.value)


def test_a1_control_row_in_author_verdicts_is_refused_by_name(world, tmp_path):
    rows = vrows("author", SAMPLED, AUTHOR_OVER) + vrows("author", ["dv_0901", "ob_0902"], {})
    write_jsonl(world / FILES["author_verdicts"], rows)
    msg = refused(world, tmp_path, an.VerdictFileInvalid)
    assert "dv_0901" in msg and "ob_0902" in msg and "author" in msg


def test_a1_author_verdicts_missing_extra_duplicate_all_listed(world, tmp_path):
    rows = [r for r in vrows("author", SAMPLED, AUTHOR_OVER) if r["id"] not in ("dv_0103", "ob_0104")]
    rows += vrows("author", ["dv_9999", "dv_0102"], {})  # an extra id and a duplicate
    write_jsonl(world / FILES["author_verdicts"], rows)
    msg = refused(world, tmp_path, an.VerdictFileInvalid)
    for needle in ("dv_0103", "ob_0104", "dv_9999", "dv_0102"):
        assert needle in msg


def test_a1_ariadne_file_must_hold_every_control(world, tmp_path):
    write_jsonl(world / FILES["ariadne"], vrows("ariadne", SAMPLED + CTL_ALL[:-2], ARIADNE_OVER))
    msg = refused(world, tmp_path, an.VerdictFileInvalid)
    assert CTL_ALL[-1] in msg and CTL_ALL[-2] in msg and "missing" in msg


def test_a1_blind_file_every_offender_listed_and_values_not_echoed(world, tmp_path):
    rows = [r for r in blind_rows() if r["id"] != "dv_0103"]                       # missing
    rows += [{"id": "ob_0101", "blind_type": "inductive_analogy", "reason": "r"},   # an observation
             {"id": "dv_9999", "blind_type": "inductive_analogy", "reason": "r"}]   # not sampled
    by = {r["id"]: r for r in rows}
    by["dv_0104"]["blind_type"] = "not_a_type_SENTINEL_FREE"                        # not publishable
    by["dv_0105"]["reason"] = 5                                                     # reason not a string
    del by["dv_0106"]["reason"]                                                     # key missing
    rows.append(dict(by["dv_0107"]))                                                # duplicate
    write_jsonl(world / FILES["author_blind"], rows)
    msg = refused(world, tmp_path, arms.BlindFileInvalid)
    for needle in ("dv_0103", "ob_0101", "dv_9999", "dv_0104", "dv_0105", "dv_0106", "dv_0107"):
        assert needle in msg, needle
    assert "SENTINEL" not in msg, "a refusal must not echo a withheld value"


def test_a1_blind_file_that_is_valid_passes(world, tmp_path):
    rows = arms.validate_blind(world / FILES["author_blind"], DERIVATIONS)
    assert set(rows) == set(DERIVATIONS) and rows["dv_0102"] == "inductive_enumeration"


def test_a1_manifest_every_offender_listed(world, tmp_path):
    bad = {"control_mentions": {"dv_9998": ["dv_0901"], "dv_0102": ["dv_0101", "dv_0901"]},
           "n_sampled_nodes_mentioning_a_control": 5}
    (world / FILES["manifest"]).write_text(json.dumps(bad))
    msg = refused(world, tmp_path, arms.ManifestInvalid)
    assert "dv_9998" in msg and "dv_0101" in msg          # a non-sampled key; a non-control value
    assert "n_sampled_nodes_mentioning_a_control" in msg  # the count check names its field


def test_a1_manifest_names_ids_but_never_echoes_text_that_is_not_an_id(world, tmp_path):
    bad = {"control_mentions": {"dv_0102": ["SENTINEL_FREE not an id"], "SENTINEL_KEY not an id": ["dv_0901"]},
           "n_sampled_nodes_mentioning_a_control": 2}
    (world / FILES["manifest"]).write_text(json.dumps(bad))
    msg = refused(world, tmp_path, arms.ManifestInvalid)
    assert "SENTINEL" not in msg and "withheld" in msg
    assert "dv_0102" in msg                                # an id-shaped key is still named


def test_a1_filing_model_must_cover_every_sampled_id(world, tmp_path):
    f = filing_obj()
    del f["nodes"]["dv_0103"], f["nodes"]["ob_0104"]
    (world / FILES["filing_model"]).write_text(json.dumps(f))
    msg = refused(world, tmp_path, an.InputInvalid)
    assert "dv_0103" in msg and "ob_0104" in msg


def test_a1_packet_must_hold_exactly_the_sampled_ids_and_controls(world, tmp_path):
    (world / FILES["packet"]).write_text(packet_text(node_ids=[i for i in SAMPLED + CTL_ALL if i != "dv_0103"]))
    msg = refused(world, tmp_path, an.InputInvalid)
    assert "dv_0103" in msg


# ------------------------------------------------------------------ A2 recognized.txt
def parse_rec(tmp_path, text):
    p = tmp_path / "rec.txt"
    p.write_text(text)
    return arms.parse_recognized(p, set(SAMPLED + CTL_ALL))


def test_a2_valid_file_comments_blanks_late_and_controls(tmp_path):
    rec, late = parse_rec(tmp_path, RECOGNIZED_TEXT)
    assert rec == RECOGNIZED and late == LATE   # the commented-out id and the blank line contribute nothing


def test_a2_refusal_lists_every_bad_line_number_and_never_line_text(tmp_path):
    text = ("dv_0101 SENTINEL_REC ok\n"                  # 1 ok
            "\n"                                          # 2 blank
            "SENTINEL_REC no id here\n"                   # 3 zero ids
            "dv_0102 dv_0103 SENTINEL_REC two ids\n"      # 4 two ids
            "dv_7777 SENTINEL_REC not in the packet\n"    # 5 outside the packet
            "dv_0101 SENTINEL_REC again\n"                # 6 duplicate of line 1
            "# comment dv_0102 dv_0103\n"                 # 7 comment: ignored
            "ob_0104\n")                                  # 8 ok
    with pytest.raises(arms.RecognizedInvalid) as e:
        parse_rec(tmp_path, text)
    msg = str(e.value)
    for n in (3, 4, 5, 6):
        assert f"line {n}" in msg, n
    for n in (1, 2, 7, 8):
        assert f"line {n}:" not in msg and f"line {n} " not in msg, n
    assert "SENTINEL_REC" not in msg and "dv_" not in msg and "ob_" not in msg, "no line text, no id"


def test_a2_refusal_through_the_cli_writes_nothing(world, tmp_path):
    (world / FILES["ariadne_recognized"]).write_text("dv_0101\nthis line has no id SENTINEL_REC\n")
    msg = refused(world, tmp_path, arms.RecognizedInvalid)
    assert "line 2" in msg and "SENTINEL_REC" not in msg


def test_a2_id_shape_is_whole_token(tmp_path):
    with pytest.raises(arms.RecognizedInvalid):
        parse_rec(tmp_path, "dv_01011 an id-shaped token that is not an id\n")
    rec, _ = parse_rec(tmp_path, "see dv_0101, and nothing else.\n")
    assert rec == {"dv_0101"}


# ------------------------------------------------------------------ A3 mention set
def test_a3_mention_set_is_case_insensitive_and_word_bounded():
    blocks = arms.parse_packet(packet_text())
    assert set(blocks) == set(SAMPLED + CTL_ALL)
    assert arms.mention_set(blocks) == MENTION   # Ariadne, ariadne, Ari, ARIADNE; not Aria/variables/Mario


def test_a3_report_prints_n_and_the_protocol_figure_without_asserting_equality(rep, out):
    m = rep["mention_set"]
    assert m["n"] == 4 and m["n_packet_nodes"] == 45 and m["protocol_measured"] == "41 of 211"
    assert m["n_controls"] == 1
    md = (out / "report_arms.md").read_text()
    assert "4 of 45" in md and "41 of 211" in md


# ------------------------------------------------------------------ A4 blind-pass agreement
def grp(rep, pass_name, *path):
    d = rep["blind"][pass_name]
    for p in path:
        d = d[p]
    return d


def test_a4_four_passes_change_the_counts_by_exactly_the_excluded_nodes(rep):
    # all 20/28; without dv_0101 (agrees) 19/27; without dv_0102, dv_0203 (both disagree) 20/26; both 19/25
    got = {p: (grp(rep, p, "overall")["k"], grp(rep, p, "overall")["n"]) for p in PASSES4}
    assert got == {"all": (20, 28), "without_prior": (19, 27), "without_manifest": (20, 26),
                   "without_both": (19, 25)}


def test_a4_overall_rate_has_a_wilson_interval(rep):
    o = grp(rep, "all", "overall")
    lo, hi = an.wilson(20, 28)
    assert o["rate"]["value"] == pytest.approx(20 / 28) and o["rate"]["ci_low"] == pytest.approx(lo)
    assert o["rate"]["ci_high"] == pytest.approx(hi)


def test_a4_per_stratum_counts_and_the_lt10_rule_inside_a_pass(rep):
    ig = "derivation:inductive_generalization"
    mp, aN = "derivation:deductive_modus_ponens", "derivation:inductive_analogy"
    exp = {  # (k, n) per pass
        ig: {"all": (9, 12), "without_prior": (8, 11), "without_manifest": (9, 11), "without_both": (8, 10)},
        mp: {"all": (8, 10), "without_prior": (8, 10), "without_manifest": (8, 9), "without_both": (8, 9)},
        aN: {p: (3, 6) for p in PASSES4}}
    for s, per in exp.items():
        for p, (k, n) in per.items():
            g = grp(rep, p, "by_stratum", s)
            assert (g["k"], g["n"]) == (k, n), (s, p)
            assert ("rate" in g) == (n >= 10), (s, p)       # the <10 rule: counts only, no rate, no interval
    assert grp(rep, "all", "by_stratum", ig)["rate"]["value"] == pytest.approx(9 / 12)
    assert "rate" in grp(rep, "all", "by_stratum", mp) and "rate" not in grp(rep, "without_manifest", "by_stratum", mp)


def test_a4_per_filing_model_with_less_certain_counts(rep):
    exp = {M46: (7, 9, 0), M47: (5, 7, 1), M48: (5, 8, 1), M5: (3, 4, 0)}   # dv_0304 is exactly 24.0: not "less certain"
    for m, (k, n, less) in exp.items():
        g = grp(rep, "all", "by_filing_model", "models", m)
        assert (g["k"], g["n"], g["less_certain"]) == (k, n, less), m
        assert "rate" not in g                                              # every model has < 10 nodes
    g = grp(rep, "without_prior", "by_filing_model", "models", M46)
    assert (g["k"], g["n"]) == (6, 8)                                       # dv_0101 (agrees) is gone


def test_a4_confusion_table_declared_by_blind(rep):
    exp_all = {"inductive_generalization": {"inductive_generalization": 9, "inductive_enumeration": 2,
                                            "inductive_statistical": 1},
               "deductive_modus_ponens": {"deductive_modus_ponens": 8, "deductive_hypothetical_syllogism": 2},
               "inductive_analogy": {"inductive_analogy": 3, "inductive_causal": 3}}
    assert grp(rep, "all", "confusion") == exp_all
    both = grp(rep, "without_both", "confusion")
    assert both["inductive_generalization"] == {"inductive_generalization": 8, "inductive_enumeration": 1,
                                                "inductive_statistical": 1}
    assert both["deductive_modus_ponens"] == {"deductive_modus_ponens": 8, "deductive_hypothetical_syllogism": 1}


def test_a4_prior_node_exclusion_reaches_every_blind_pass(rep):
    # a plausible-wrong build forgets the prior node in the blind passes only
    assert grp(rep, "without_prior", "overall")["n"] == 27 and grp(rep, "without_both", "overall")["n"] == 25


# ------------------------------------------------------------------ A5 self-naming
@pytest.mark.parametrize("declared,claim,chain,want", [
    ("inductive_generalization", "an inductive_generalization of x", "", True),        # underscore form
    ("inductive_generalization", "an inductive generalization of x", "", True),        # space form
    ("inductive_generalization", "an INDUCTIVE_Generalization", "", True),             # case-insensitive
    ("inductive_generalization", "nothing here", "so, inductive generalization", True),  # chain only
    ("inductive_generalization", "an inductive generalisation", "deductive_modus_ponens", False),
    ("inductive_generalization", "inductive-generalization", "inductive  generalization", False),
    ("inductive_generalization", None, None, False),
])
def test_a5_names_own_type(declared, claim, chain, want):
    assert arms.names_own_type(declared, claim, chain) is want


def test_a5_counts_among_the_blind_derivations_and_recomputes_agreement(rep):
    # dv_0103, dv_0104, dv_0205 agree; dv_0302 disagrees. dv_0201 names another type and dv_0108
    # spells it differently: neither counts.
    exp = {"all": (4, 17, 24), "without_prior": (4, 16, 23), "without_manifest": (4, 17, 22),
           "without_both": (4, 16, 21)}
    for p, (cnt, k, n) in exp.items():
        s = grp(rep, p, "self_naming")
        assert s["n_self_naming"] == cnt, p
        assert (s["agreement_excluding"]["k"], s["agreement_excluding"]["n"]) == (k, n), p


def test_a5_claim_and_chain_are_read_for_the_boolean_only(out):
    for p in all_files(out):
        t = p.read_bytes()
        assert b"Inductive_Generalization at work" not in t and b"Deductive Modus Ponens" not in t


# ------------------------------------------------------------------ A6 author agrees / disagrees
CELL_KEYS = ("author_agrees", "author_disagrees", "author_cannot_judge",
             "reverse_author_loose_reader_tight", "n_reader_loose")


def cells(d):
    return tuple(d[k] for k in CELL_KEYS)


def avr(rep, reader, pass_name="all"):
    return rep["author_vs_reader"][reader][pass_name]


def test_a6_mira_every_cell_nonzero_with_hand_computed_counts(rep):
    a = avr(rep, "mira")
    assert cells(a["total"]) == (3, 3, 3, 2, 9)
    assert cells(a["by_check"]["type"]) == (1, 1, 1, 0, 3)
    assert cells(a["by_check"]["placement"]) == (1, 1, 1, 1, 3)
    assert cells(a["by_check"]["chain-overreach"]) == (0, 0, 0, 1, 0)
    assert cells(a["by_check"]["quote_type"]) == (1, 0, 0, 0, 1)
    assert cells(a["by_check"]["source_class"]) == (0, 1, 0, 0, 1)
    assert cells(a["by_check"]["support-overreach"]) == (0, 0, 1, 0, 1)
    assert all(v > 0 for v in cells(a["total"]))


def test_a6_the_denominator_keeps_the_cannot_judge_cell(rep):
    a = avr(rep, "mira")["total"]
    assert a["n_reader_loose"] == a["author_agrees"] + a["author_disagrees"] + a["author_cannot_judge"]
    assert a["author_cannot_judge"] == 3


def test_a6_ariadne_and_zephyr(rep):
    # dv_0105 adds a free-text `type` loose where the author is tight: one author-disagrees, one more reader-loose
    assert cells(avr(rep, "ariadne")["total"]) == (3, 1, 0, 2, 4)
    assert cells(avr(rep, "zephyr")["total"]) == (3, 0, 0, 1, 3)   # Zephyr judged 8 sampled nodes


def test_a6_four_passes_change_the_counts_by_exactly_the_excluded_nodes(rep):
    assert cells(avr(rep, "mira", "all")["total"]) == (3, 3, 3, 2, 9)
    assert cells(avr(rep, "mira", "without_prior")["total"]) == (2, 3, 2, 2, 7)      # dv_0101: type agree, placement cj
    assert cells(avr(rep, "mira", "without_manifest")["total"]) == (1, 3, 3, 2, 7)   # dv_0102, ob_0101: agrees
    assert cells(avr(rep, "mira", "without_both")["total"]) == (0, 3, 2, 2, 5)


def test_a6_filing_model_split_is_labelled_exploratory(rep, out):
    split = avr(rep, "mira")["by_filing_model"]
    assert split["label"] == "exploratory, not attribution"
    m = split["models"]
    assert (m[M46]["author_agrees"], m[M46]["n_reader_loose"]) == (3, 6)
    assert (m[M47]["author_agrees"], m[M47]["n_reader_loose"]) == (0, 1)
    assert (m[M5]["author_agrees"], m[M5]["n_reader_loose"]) == (0, 2)
    assert (m[M48]["author_agrees"], m[M48]["n_reader_loose"]) == (0, 0)
    assert "exploratory, not attribution" in (out / "report_arms.md").read_text()


def test_a6_controls_never_enter(rep):
    # the author file has no control rows; a control leaking into the tallies would add loose cells
    assert avr(rep, "mira")["total"]["n_reader_loose"] == 9   # Mira marks 3 controls loose


def test_a6_md_prints_every_check_even_when_all_its_cells_are_zero(out):
    md = (out / "report_arms.md").read_text()
    section = md.split("### zephyr, pass: all")[1].split("###")[0]
    for c in DER_CHECKS + OBS_CHECKS:                     # Zephyr has no source_class cell: still printed
        assert f"- {c}:" in section, c


# ------------------------------------------------------------------ reading rules and registration labels
DERIVED = "derived (combines pre-registered exclusions; not itself pre-registered)"
DESCRIPTIVE = "descriptive (not pre-registered)"
EXPLORATORY = "exploratory, not attribution"
PROTOCOL = AUDIT / "PROTOCOL.md"


def protocol_reading_rules():
    """The bullets under PROTOCOL.md's `*Reading rules, fixed now.*`, read from the file itself."""
    lines = PROTOCOL.read_text().splitlines()
    rules = []
    for ln in lines[lines.index("*Reading rules, fixed now.*") + 1:]:
        if not ln.startswith("- "):
            break
        rules.append(ln)
    return rules


def test_reading_rules_are_printed_verbatim_at_the_top_of_the_md(out):
    rules = protocol_reading_rules()
    assert len(rules) == 5, "Amendment 4 fixes five reading rules"
    top = (out / "report_arms.md").read_text().split("## Input files")[0]
    pos = [top.find(r) for r in rules]
    assert -1 not in pos, [r[:30] for r, p in zip(rules, pos) if p == -1]
    assert pos == sorted(pos)


def test_blind_per_filing_model_split_is_labelled_exploratory_in_json_and_md(rep, out):
    for p in PASSES4:
        assert grp(rep, p, "by_filing_model")["label"] == EXPLORATORY, p
    md = (out / "report_arms.md").read_text()
    blind = md.split("## Arm A blind pass")[1].split("## Author agrees")[0]
    assert blind.count(f"- per filing model ({EXPLORATORY}):") == 4


def test_combined_passes_are_marked_derived_and_the_registered_ones_are_not(rep):
    for p in PASSES4:
        want = DERIVED if p == "without_both" else None
        blocks = [rep["blind"][p], rep["author"]["passes"][p]] + [rep["author_vs_reader"][w][p]
                                                                  for w in ("mira", "ariadne", "zephyr")]
        for b in blocks:
            assert b.get("status", {}).get("pass") == want, p
    for p in PASSES_ARI:
        want = DERIVED if p == "without_both_sets" else None
        assert rep["ariadne"]["passes"][p].get("status", {}).get("pass") == want, p


def test_blind_wilson_intervals_and_confusion_are_marked_descriptive(rep):
    for p in PASSES4:
        st = rep["blind"][p]["status"]
        assert st["wilson_intervals"] == DESCRIPTIVE and st["confusion"] == DESCRIPTIVE, p


def test_registration_labels_appear_in_the_md(out):
    md = (out / "report_arms.md").read_text()
    assert md.count(DERIVED) == 6      # blind, author, three readers' author-vs-reader, Ariadne's both-sets
    blind = md.split("## Arm A blind pass")[1].split("## Author agrees")[0]
    assert blind.count(DESCRIPTIVE) == 8   # intervals and the confusion table, in each of the four passes
    assert blind.count(DERIVED) == 1


# ------------------------------------------------------------------ A7 pairwise agreement
def pair(rep, name):
    return rep["pairs"][name]


def test_a7_pairs_and_sizes(rep):
    assert {k: v["n_shared"] for k, v in rep["pairs"].items()} == {
        "author_mira": 40, "author_ariadne": 40, "author_zephyr": 8, "ariadne_mira": 40, "ariadne_zephyr": 8}


def test_a7_kappa_on_a_hand_computed_pair(rep):
    # author vs ariadne, 40 nodes. author: 5 loose, 2 partial, 33 tight; ariadne: 3 loose, 37 tight.
    # agree 36/40 = 90%; pe = (5*3 + 33*37)/1600 = 0.7725; kappa = 0.1275/0.2275 = 51/91.
    c = pair(rep, "author_ariadne")["class"]
    assert c["n"] == 40 and c["n_agree"] == 36 and c["percent_agreement"] == pytest.approx(90.0)
    assert c["kappa"] == pytest.approx(51 / 91)
    assert {(d["id"], d["author"], d["ariadne"]) for d in c["disagreements"]} == {
        ("dv_0102", "loose", "tight"), ("dv_0201", "loose", "tight"),
        ("dv_0301", "partial", "tight"), ("ob_0201", "partial", "tight")}
    # tight vs loose only: the 2 partial nodes leave; 38 remain, 36 agree; pe = (5*3 + 33*35)/38^2
    tl = pair(rep, "author_ariadne")["tight_loose"]
    assert tl["n"] == 38 and tl["kappa"] == pytest.approx(99 / 137)


def test_a7_per_check_percent_and_kappa(rep):
    pc = pair(rep, "author_ariadne")["per_check"]
    assert (pc["type"]["n"], pc["type"]["n_agree"]) == (28, 26)           # dv_0301 (cannot-judge/tight), dv_0105 (tight/loose)
    assert pc["type"]["percent_agreement"] == pytest.approx(100 * 26 / 28)
    assert (pc["placement"]["n"], pc["placement"]["n_agree"]) == (28, 26)   # dv_0101 and dv_0102 differ
    assert "kappa" in pc["placement"]
    assert set(pc) == set(DER_CHECKS + OBS_CHECKS)


def test_a7_disagreement_lists_hold_ids_and_labels_only(rep):
    for blk in rep["pairs"].values():
        for d in blk["class"]["disagreements"]:
            assert set(d) <= {"id", "author", "ariadne", "mira", "zephyr"}


def test_a7_controls_agreement_is_ariadne_pairs_only_and_separate(rep):
    c = rep["controls"]["pairs"]
    assert set(c) == {"ariadne_mira", "ariadne_zephyr"}
    am = c["ariadne_mira"]
    assert am["n"] == 5 and am["n_agree"] == 4
    assert am["disagreements"] == [{"id": "dv_0902", "ariadne": "tight", "mira": "loose"}]
    az = c["ariadne_zephyr"]
    assert az["n"] == 5 and az["n_agree"] == 3
    assert {d["id"] for d in az["disagreements"]} == {"dv_0902", "ob_0901"}


# ------------------------------------------------------------------ A8 Ariadne's rates
def ari(rep, p, kind, stratum):
    return rep["ariadne"]["passes"][p][kind]["strata"][stratum]


def test_a8_rates_in_the_five_passes(rep):
    ig = "derivation:inductive_generalization"
    exp = {"all": (12, 2), "without_prior": (11, 1), "without_recognized": (10, 0),
           "without_mention": (10, 1), "without_both_sets": (9, 0)}
    for p, (n, loose) in exp.items():
        r = ari(rep, p, "derivation", ig)
        assert (r["n"], r["loose"]) == (n, loose), p
        assert ("low" in r) == (n >= 10), p                    # the <10 rule inside a pass
    assert ari(rep, "all", "derivation", ig)["low"]["rate"] == pytest.approx(2 / 12)
    mp = "derivation:deductive_modus_ponens"
    assert ari(rep, "all", "derivation", mp)["n"] == 10 and "low" in ari(rep, "all", "derivation", mp)
    assert ari(rep, "without_recognized", "derivation", mp)["n"] == 9    # dv_0201 recognized
    assert "low" not in ari(rep, "without_recognized", "derivation", mp)
    assert ari(rep, "without_mention", "observation", "observation:hard_data")["n"] == 7   # ob_0102 mentions her


def test_a8_inductive_generalization_confusion_confidence_and_reading(rep):
    k = rep["ariadne"]["passes"]["all"]["derivation"]
    assert k["inductive_generalization"]["loose"] == 2
    assert k["confusion"] == {"inductive_generalization": {"inductive_enumeration": 1, PLACEHOLDER: 1}}
    c = k["confidence"]
    assert (c["n_tight"], c["n_loose"]) == (26, 2) and c["reading"] and "auc" in c
    assert rep["ariadne"]["passes"]["all"]["observation"]["confidence"]["n_loose"] == 1


def test_a8_deltas_use_the_full_set_only(rep):
    d = rep["ariadne"]["deltas"]
    assert d["summary"]["n"] == 1 and [r["id"] for r in d["computed"]] == ["dv_0101"]
    assert "deltas" not in rep["ariadne"]["passes"]["without_prior"]


def test_a8_set_comparison(rep):
    s = rep["ariadne"]["sets"]
    assert (s["recognized"]["n"], s["recognized"]["n_controls"]) == (4, 1)
    assert (s["mention"]["n"], s["mention"]["n_controls"]) == (4, 1)
    assert s["both"]["n"] == 1 and s["recognized_only"]["n"] == 3 and s["mention_only"]["n"] == 3
    assert s["late"]["n"] == 1


def test_a8_ariadne_controls_sensitivity_and_specificity(rep):
    c = rep["controls"]["ariadne"]
    assert c["sensitivity"]["text"] == "2/3" and c["specificity"]["text"] == "2/2"


# ------------------------------------------------------------------ A9 author's rates
def test_a9_author_rates_in_the_four_passes_and_no_controls(rep):
    ig, mp = "derivation:inductive_generalization", "derivation:deductive_modus_ponens"
    p = rep["author"]["passes"]
    exp_ig = {"all": (12, 3), "without_prior": (11, 2), "without_manifest": (11, 2), "without_both": (10, 1)}
    for name, (n, loose) in exp_ig.items():
        r = p[name]["derivation"]["strata"][ig]
        assert (r["n"], r["loose"]) == (n, loose), name
        assert ("low" in r) == (n >= 10), name
    assert p["all"]["derivation"]["strata"][mp]["loose"] == 1 and "low" in p["all"]["derivation"]["strata"][mp]
    assert p["without_manifest"]["derivation"]["strata"][mp]["n"] == 9
    assert "sensitivity" not in json.dumps(rep["author"])
    c = p["all"]["derivation"]["confidence"]
    assert (c["n_tight"], c["n_loose"], c["n_partial"]) == (23, 4, 1)


def test_a9_free_text_proposed_type_is_the_placeholder(rep):
    assert rep["author"]["passes"]["all"]["derivation"]["confusion"] == {
        "inductive_generalization": {PLACEHOLDER: 1}}
    assert rep["author"]["passes"]["without_prior"]["derivation"]["confusion"] == {}


# ------------------------------------------------------------------ A10 no content in any output
def test_a10_no_sentinel_anywhere_in_the_tree(out):
    files = all_files(out)
    names = {p.relative_to(out).as_posix() for p in files}
    assert {"report_arms.json", "report_arms.md", "public/verdicts-ariadne.public.jsonl",
            "public/verdicts-author.public.jsonl", "public/blind-author.public.jsonl"} <= names  # not vacuous
    for p in files:
        assert b"SENTINEL" not in p.read_bytes(), p.name


def test_a10_recognized_line_text_and_packet_text_never_appear(out):
    for p in all_files(out):
        t = p.read_bytes()
        for needle in (b"recognised this one", b"she is named in it", b"added after judging", b"half-remembered",
                       b"Ariadne wrote this note", b"see ariadne", b"Ari said so", b"Aria, variables"):
            assert needle not in t, (p.name, needle)


def test_a10_positive_controls_a_v051_name_and_a_blind_type_appear_verbatim(rep, out):
    assert rep["ariadne"]["passes"]["all"]["derivation"]["confusion"]["inductive_generalization"] == {
        "inductive_enumeration": 1, PLACEHOLDER: 1}
    ariadne = {r["id"]: r for r in read_lines(out / "public" / "verdicts-ariadne.public.jsonl")}
    assert ariadne["dv_0101"]["checks"]["type"]["proposed_type"] == "inductive_enumeration"
    assert ariadne["dv_0105"]["checks"]["type"]["proposed_type"] == PLACEHOLDER   # her free-text one is withheld
    blind = {r["id"]: r for r in read_lines(out / "public" / "blind-author.public.jsonl")}
    assert blind["dv_0102"]["blind_type"] == "inductive_enumeration"
    author = {r["id"]: r for r in read_lines(out / "public" / "verdicts-author.public.jsonl")}
    assert author["dv_0101"]["checks"]["type"]["proposed_type"] == PLACEHOLDER   # the free-text one is withheld
    md = (out / "report_arms.md").read_text()
    assert "inductive_generalization -> inductive_enumeration" in md


def test_a10_control_ids_appear_only_in_the_controls_section(rep, out):
    body = json.dumps({k: v for k, v in rep.items() if k != "controls"})
    md = (out / "report_arms.md").read_text()
    head, sep, tail = md.partition("## Controls")
    assert sep, "the markdown report has a Controls section"
    for cid in CTL_ALL:
        assert cid not in body, cid
        assert cid not in head, cid
    assert all(cid in tail for cid in ("dv_0901", "dv_0903", "ob_0902"))             # the section is not empty
    assert rep["controls"]["recognized_control_ids"] == ["dv_0903"]
    assert rep["controls"]["mention_control_ids"] == ["dv_0902"]
    for cid in ("dv_0901", "dv_0902"):                                                # manifest values stay private
        assert cid not in head


# ------------------------------------------------------------------ A11 public export
def test_a11_ariadne_and_author_exports_are_analyze_public_export_text(world, out):
    ctl = set(CTL_ALL)
    ar = an.validate_verdicts(world / FILES["ariadne"], set(SAMPLED) | ctl, "ariadne")
    au = an.validate_verdicts(world / FILES["author_verdicts"], set(SAMPLED), "author")
    assert (out / "public" / "verdicts-ariadne.public.jsonl").read_text() == an.public_export_text(ar)
    assert (out / "public" / "verdicts-author.public.jsonl").read_text() == an.public_export_text(au)
    assert {r["id"] for r in read_lines(out / "public" / "verdicts-ariadne.public.jsonl")} >= ctl  # clause-14 precedent
    assert not ({r["id"] for r in read_lines(out / "public" / "verdicts-author.public.jsonl")} & ctl)


def test_a11_blind_export_has_id_and_blind_type_only_sorted_and_deterministic(out):
    text = (out / "public" / "blind-author.public.jsonl").read_text()
    rows = [json.loads(x) for x in text.splitlines()]
    assert [r["id"] for r in rows] == sorted(DERIVATIONS) and len(rows) == 28
    assert all(set(r) == {"id", "blind_type"} for r in rows)
    assert "reason" not in text and text.endswith("\n") and not text.endswith("\n\n")
    assert rows[1] == {"id": "dv_0102", "blind_type": "inductive_enumeration"}
    for line, r in zip(text.splitlines(), rows):
        assert line == json.dumps(r, sort_keys=True, separators=(",", ":"))


# ------------------------------------------------------------------ A12 hashes and determinism
def test_a12_input_sha256_covers_every_input_file(world, rep, out):
    h = rep["meta"]["input_sha256"]
    assert set(h) == set(FILES)
    for k, name in FILES.items():
        assert h[k] == hashlib.sha256((world / name).read_bytes()).hexdigest(), k
    md = (out / "report_arms.md").read_text()
    for v in h.values():
        assert v in md


def test_a12_same_inputs_and_seed_give_byte_identical_outputs(world, tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    run(world, a)
    run(world, b)
    pa, pb = all_files(a), all_files(b)
    assert [p.relative_to(a) for p in pa] == [p.relative_to(b) for p in pb] and len(pa) == 5
    for x, y in zip(pa, pb):
        assert x.read_bytes() == y.read_bytes(), x.name


def test_a12_bootstrap_labels_are_prefixed_arms(world, tmp_path, monkeypatch):
    seen = []
    real = an.auc_report

    def spy(tight, loose, seed, label, n_boot=an.N_BOOT):
        seen.append(label)
        return real(tight, loose, seed, label, n_boot)

    monkeypatch.setattr(an, "auc_report", spy)
    run(world, tmp_path / "o")
    assert len(seen) == (5 + 4) * 2                       # Ariadne's five passes, the author's four, two kinds each
    assert all(s.startswith("arms:") for s in seen), seen
    assert len(set(seen)) == len(seen)


# ------------------------------------------------------------------ A13 outputs outside the worktree
def test_a13_out_inside_the_worktree_is_refused_and_nothing_is_written(world):
    o = REPO / "_arms_out_must_not_exist"
    try:
        with pytest.raises(an.OutputInsideWorktree):
            run(world, o)
        assert not o.exists()
    finally:
        if o.exists():  # pragma: no cover - only if the guard fails
            import shutil
            shutil.rmtree(o)


def test_a13_a_refused_run_through_the_command_line_exits_nonzero_and_writes_nothing(world, tmp_path):
    write_jsonl(world / FILES["author_verdicts"], vrows("author", SAMPLED + ["dv_0901"], AUTHOR_OVER))
    o = tmp_path / "cli_out"
    r = subprocess.run([sys.executable, str(TOOL)] + args_for(world, o), capture_output=True, text=True)
    assert r.returncode != 0 and "VerdictFileInvalid" in r.stderr
    assert not o.exists()


def test_a13_writes_exactly_the_report_and_public_files(out):
    assert {p.relative_to(out).as_posix() for p in all_files(out)} == {
        "report_arms.json", "report_arms.md", "public/verdicts-ariadne.public.jsonl",
        "public/verdicts-author.public.jsonl", "public/blind-author.public.jsonl"}
