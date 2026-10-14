"""Contract tests for `studies/node-audit/analyze.py` (paper v2 workstream D).

Written BEFORE the implementation (contract-first). The contract is the one stated in the
tool's module docstring, clause numbers below match it. SYNTHETIC data only: every input
is built inside the test; no real verdict, packet, control file or snapshot is ever read.

Synthetic world (hand-computed expectations are written out beside each assertion):
  derivation strata: IG n=12, MP n=10, AN n=9;  observation strata: hard_data n=10, editorial n=3
  census populations: IG 100 / MP 60 / AN 40;  hard_data 80 / editorial 20
  analyst-prior node: dv_ig01
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
AUDIT = REPO / "studies" / "node-audit"
TOOL = AUDIT / "analyze.py"
VENDORED = AUDIT / "_v051_confidence.py"
VENDORED_SHA = "5ea367d8d15153e82b68d3fdf5f08ef12b5d5555be9326f5ee65e0a12ac260e0"
SEED = "synthetic-seed"
PRIOR = "dv_ig01"
READING_TRACKS = "confidence tracks correctness in this sample"
READING_NONE = "no evidence either way at this n"
READING_AGAINST = "confidence runs against correctness in this sample"


def _load():
    spec = importlib.util.spec_from_file_location("analyze", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["analyze"] = mod
    spec.loader.exec_module(mod)
    return mod


an = _load()

DER_CHECKS = ("type", "placement", "chain-overreach")
OBS_CHECKS = ("support-overreach", "quote_type", "source_class")


# ------------------------------------------------------------------ synthetic world
def ids(prefix, n, width=2):
    return [f"{prefix}{i:0{width}d}" for i in range(1, n + 1)]


IG, MP, AN = ids("dv_ig", 12), ids("dv_mp", 10), ids("dv_an", 9)
HD, ED = ids("ob_hd", 10), ids("ob_ed", 3, 1)
SAMPLED = {
    "derivation:inductive_generalization": IG,
    "derivation:deductive_modus_ponens": MP,
    "derivation:inductive_analogy": AN,
    "observation:hard_data": HD,
    "observation:editorial": ED,
}
ZEPH = ["dv_ig01", "dv_ig02", "dv_ig03", "dv_ig04", "dv_mp01", "dv_mp02", "ob_hd01", "ob_hd02"]
CTL_LOOSE = ["dv_cl1", "dv_cl2", "ob_cl1"]
CTL_TIGHT_PV = ["dv_ct1"]
CTL_TIGHT_FINAL = ["ob_ct1"]
CTL_ALL = CTL_LOOSE + CTL_TIGHT_PV + CTL_TIGHT_FINAL
NOTE = "SECRETNOTE-do-not-print"
DRAWN = {
    "seed": SEED,
    "allocation": {k: len(v) for k, v in SAMPLED.items()},
    "sampled": SAMPLED,
    "zephyr": ZEPH,
    "census": {
        "derivation_by_type": {"inductive_generalization": 100, "deductive_modus_ponens": 60,
                               "inductive_analogy": 40, "deductive_reductio": 0},
        "observation_factual_by_quote_type": {"hard_data": 80, "editorial": 20},
        "derivation_null_type": 4,
    },
}


def checks_for(node_id):
    return DER_CHECKS if node_id.startswith("dv_") else OBS_CHECKS


def row(node_id, cls, loose_check=None, proposed="deductive_modus_ponens"):
    """cls: T all tight; L one loose check (default the first); P first check cannot-judge,
    rest tight; C all cannot-judge."""
    names = checks_for(node_id)
    v = {c: "tight" for c in names}
    if cls == "L":
        v[loose_check or names[0]] = "loose"
    elif cls == "P":
        v[names[0]] = "cannot-judge"
    elif cls == "C":
        v = {c: "cannot-judge" for c in names}
    checks = {c: {"verdict": v[c], "reason": "r"} for c in names}
    if node_id.startswith("dv_"):
        checks["type"]["proposed_type"] = proposed if v["type"] == "loose" else None
    return {"id": node_id, "checks": checks}


def mira_spec():
    s = {i: ("T",) for i in IG + MP + AN + HD + ED}
    s["dv_ig01"] = ("L", "type", "deductive_modus_ponens")
    s["dv_ig02"] = ("L", "placement")
    s["dv_ig03"] = ("P",)
    s["dv_ig07"] = ("C",)
    s["dv_ig11"] = ("P",)
    s["dv_mp01"] = ("L", "type", "inductive_generalization")
    s["dv_mp03"] = ("P",)
    s["dv_an01"] = ("L", "type", "deductive_conjunction")  # not in the v0.5.1 table
    s["ob_hd01"] = ("L", "quote_type")
    s["ob_hd03"] = ("P",)
    s["ob_ed1"] = ("L", "support-overreach")
    s.update({"dv_cl1": ("L",), "dv_cl2": ("T",), "ob_cl1": ("L",),
              "dv_ct1": ("T",), "ob_ct1": ("P",)})
    return s


def zeph_spec():
    s = {i: ("T",) for i in ZEPH}
    s["dv_ig02"] = ("L", "placement")
    s["dv_mp01"] = ("L", "type", "deductive_modus_tollens")
    s["ob_hd01"] = ("P",)
    s.update({"dv_cl1": ("L",), "dv_cl2": ("L",), "ob_cl1": ("L",),
              "dv_ct1": ("T",), "ob_ct1": ("T",)})
    return s


def rows_from(spec):
    out = []
    for i, args in spec.items():
        cls = args[0]
        lc = args[1] if len(args) > 1 else None
        pt = args[2] if len(args) > 2 else "deductive_modus_ponens"
        out.append(row(i, cls, lc, pt))
    return out


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return path


def stored_conf():
    c = {i: 0.8 for i in IG + MP + AN + HD + ED}
    for i in IG + MP + AN:  # tight derivations: .9 except two
        c[i] = 0.9
    c.update({"dv_ig12": 0.5, "dv_mp10": 0.6})
    c.update({"dv_ig01": 0.931, "dv_ig02": 0.7, "dv_mp01": 0.588, "dv_an01": 0.5})
    c.update({"dv_ig03": 0.8, "dv_ig11": 0.8, "dv_ig07": 0.8, "dv_mp03": 0.8})
    for i in HD + ED:
        c[i] = 0.85
    c.update({"ob_ed2": 0.35, "ob_ed3": 0.35, "ob_hd01": 0.95, "ob_ed1": 0.35, "ob_hd03": 0.8})
    for i in CTL_ALL:
        c[i] = 0.999  # distinctive: any leak of a control into a join shows
    return c


def make_db(path):
    conf = stored_conf()
    declared = {}
    for i in IG:
        declared[i] = "inductive_generalization"
    for i in MP:
        declared[i] = "deductive_modus_ponens"
    for i in AN:
        declared[i] = "inductive_analogy"
    c = sqlite3.connect(path)
    c.executescript("CREATE TABLE nodes (id TEXT PRIMARY KEY, confidence REAL, metadata TEXT);"
                    "CREATE TABLE edges (id INTEGER PRIMARY KEY, source_id TEXT, target_id TEXT, relation TEXT);")
    for i, v in conf.items():
        md = json.dumps({"reasoning_type": declared[i]}) if i in declared else "{}"
        c.execute("INSERT INTO nodes VALUES (?,?,?)", (i, v, md))
    premises = {"pm1": 0.9, "pm2": 0.8, "pm3": 0.9, "pm4": 0.6, "pm8": 0.1, "pm9": 0.1}
    for i, v in premises.items():
        c.execute("INSERT INTO nodes VALUES (?,?,?)", (i, v, "{}"))
    edges = [("dv_ig01", "pm1", "derives_from"), ("dv_ig01", "pm2", "derives_from"),
             ("dv_ig01", "pm9", "acknowledged_derives_from"), ("dv_ig01", "pm8", "cites"),
             ("dv_mp01", "pm3", "derives_from"), ("dv_mp01", "pm4", "derives_from")]
    for s, t, r in edges:
        c.execute("INSERT INTO edges (source_id, target_id, relation) VALUES (?,?,?)", (s, t, r))
    c.commit()
    c.close()
    return path


def controls_obj():
    return {"known_loose": {i: NOTE for i in CTL_LOOSE},
            "known_tight_placement_verified": {i: NOTE for i in CTL_TIGHT_PV},
            "known_tight_final": CTL_TIGHT_FINAL,
            "other_key": {"ignored": NOTE}}


@pytest.fixture
def world(tmp_path):
    w = tmp_path / "w"
    w.mkdir()
    (w / "drawn.json").write_text(json.dumps(DRAWN))
    (w / "controls.json").write_text(json.dumps(controls_obj()))
    write_jsonl(w / "mira.jsonl", rows_from(mira_spec()))
    write_jsonl(w / "zephyr.jsonl", rows_from(zeph_spec()))
    make_db(w / "snap.db")
    return w


def args_for(w, out, prior=PRIOR):
    return ["--mira", str(w / "mira.jsonl"), "--zephyr", str(w / "zephyr.jsonl"),
            "--controls", str(w / "controls.json"), "--db", str(w / "snap.db"),
            "--drawn", str(w / "drawn.json"), "--prior-node", prior, "--seed", SEED,
            "--out", str(out)]


@pytest.fixture
def report(world, tmp_path):
    out = tmp_path / "out"
    an.main(args_for(world, out))
    return json.loads((out / "report.json").read_text())


def P(report, name="with_prior"):
    return report["passes"][name]


def expected_ids(drawn=DRAWN):
    sampled = {i for v in drawn["sampled"].values() for i in v}
    return sampled | set(CTL_ALL), set(drawn["zephyr"]) | set(CTL_ALL)


# ------------------------------------------------------------------ vendored file
def test_vendored_file_hash_is_the_pinned_v051_hash():
    assert hashlib.sha256(VENDORED.read_bytes()).hexdigest() == VENDORED_SHA
    assert an.VENDORED_SHA256 == VENDORED_SHA
    an.verify_vendored(VENDORED)  # does not raise


def test_vendored_hash_mismatch_is_refused(tmp_path):
    tampered = tmp_path / "_v051_confidence.py"
    tampered.write_bytes(VENDORED.read_bytes() + b"\n# edited\n")
    with pytest.raises(an.VendoredFileMismatch):
        an.verify_vendored(tampered)


# ------------------------------------------------------------------ 1 validation
def good_rows(who):
    return {r["id"]: r for r in rows_from(mira_spec() if who == "mira" else zeph_spec())}


def validate(tmp_path, rows, who="mira"):
    p = write_jsonl(tmp_path / "v.jsonl", rows)
    exp = expected_ids()[0 if who == "mira" else 1]
    return an.validate_verdicts(p, exp, who)


def test_validation_accepts_a_complete_file(tmp_path):
    out = validate(tmp_path, list(good_rows("mira").values()))
    assert set(out) == expected_ids()[0]


def test_validation_missing_id_named(tmp_path):
    g = good_rows("mira")
    del g["dv_mp05"]
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, list(g.values()))
    assert "dv_mp05" in str(e.value) and "missing" in str(e.value)


def test_validation_extra_id_named(tmp_path):
    rows = list(good_rows("mira").values()) + [row("dv_zz99", "T")]
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, rows)
    assert "dv_zz99" in str(e.value) and "unexpected" in str(e.value)


def test_validation_duplicate_id_named(tmp_path):
    rows = list(good_rows("mira").values()) + [row("dv_mp05", "T")]
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, rows)
    assert "dv_mp05" in str(e.value) and "duplicate" in str(e.value)


def test_validation_wrong_check_set_named(tmp_path):
    g = good_rows("mira")
    del g["dv_mp05"]["checks"]["placement"]
    g["ob_hd05"]["checks"]["bogus"] = {"verdict": "tight", "reason": "r"}
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, list(g.values()))
    assert "dv_mp05" in str(e.value) and "ob_hd05" in str(e.value) and "check set" in str(e.value)


def test_validation_observation_row_with_derivation_checks_named(tmp_path):
    g = good_rows("mira")
    g["ob_hd05"] = row("dv_mp05", "T") | {"id": "ob_hd05"}
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, list(g.values()))
    assert "ob_hd05" in str(e.value) and "check set" in str(e.value)


@pytest.mark.parametrize("bad", [None, "Tight", "ok", "", 3])
def test_validation_bad_verdict_value_named(tmp_path, bad):
    g = good_rows("mira")
    g["dv_mp05"]["checks"]["placement"]["verdict"] = bad
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, list(g.values()))
    assert "dv_mp05" in str(e.value) and "verdict value" in str(e.value)


def test_validation_missing_reason_named(tmp_path):
    g = good_rows("mira")
    del g["dv_mp05"]["checks"]["placement"]["reason"]
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, list(g.values()))
    assert "dv_mp05" in str(e.value) and "reason" in str(e.value)


def test_validation_proposed_type_null_when_type_loose(tmp_path):
    g = good_rows("mira")
    g["dv_ig01"]["checks"]["type"]["proposed_type"] = None
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, list(g.values()))
    assert "dv_ig01" in str(e.value) and "proposed_type" in str(e.value)


def test_validation_proposed_type_present_when_type_not_loose(tmp_path):
    g = good_rows("mira")
    g["dv_mp05"]["checks"]["type"]["proposed_type"] = "inductive_analogy"
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, list(g.values()))
    assert "dv_mp05" in str(e.value) and "proposed_type" in str(e.value)


def test_validation_unparseable_line_named(tmp_path):
    p = tmp_path / "v.jsonl"
    p.write_text("".join(json.dumps(r) + "\n" for r in good_rows("mira").values()) + "{not json\n")
    with pytest.raises(an.VerdictFileInvalid) as e:
        an.validate_verdicts(p, expected_ids()[0], "mira")
    assert "invalid JSON" in str(e.value) and "line" in str(e.value)


def test_validation_unknown_node_kind_named(tmp_path):
    exp = expected_ids()[0] | {"th_0001"}
    p = write_jsonl(tmp_path / "v.jsonl", list(good_rows("mira").values()) + [row("dv_mp05", "T") | {"id": "th_0001"}])
    with pytest.raises(an.VerdictFileInvalid) as e:
        an.validate_verdicts(p, exp, "mira")
    assert "th_0001" in str(e.value) and "unknown node kind" in str(e.value)


def test_validation_lists_every_offender_not_just_the_first(tmp_path):
    g = good_rows("mira")
    del g["dv_mp05"]
    g["dv_mp06"]["checks"]["placement"]["verdict"] = "nope"
    g["ob_hd07"]["checks"]["quote_type"]["verdict"] = None
    rows = list(g.values()) + [row("dv_zz98", "T")]
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, rows)
    msg = str(e.value)
    for needle in ("dv_mp05", "dv_mp06", "ob_hd07", "dv_zz98"):
        assert needle in msg


def test_validation_one_bad_row_among_good_still_refuses(tmp_path):
    """A single bad row is never skipped silently."""
    g = good_rows("mira")
    g["dv_ig05"]["checks"]["type"]["verdict"] = "unsure"
    with pytest.raises(an.VerdictFileInvalid):
        validate(tmp_path, list(g.values()))


def test_validation_zephyr_expects_overlap_plus_controls(tmp_path):
    out = validate(tmp_path, list(good_rows("zephyr").values()), who="zephyr")
    assert set(out) == set(ZEPH) | set(CTL_ALL)
    # a Mira-only id in Zephyr's file is an extra
    rows = list(good_rows("zephyr").values()) + [row("dv_ig09", "T")]
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, rows, who="zephyr")
    assert "dv_ig09" in str(e.value)


def test_validation_missing_control_is_missing(tmp_path):
    g = good_rows("mira")
    del g["dv_cl2"]
    with pytest.raises(an.VerdictFileInvalid) as e:
        validate(tmp_path, list(g.values()))
    assert "dv_cl2" in str(e.value)


def test_cli_invalid_file_exits_nonzero_and_names_every_offender(world, tmp_path):
    g = good_rows("mira")
    del g["dv_mp05"]
    g["ob_hd07"]["checks"]["quote_type"]["verdict"] = "bad"
    write_jsonl(world / "mira.jsonl", list(g.values()))
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, str(TOOL)] + args_for(world, out), capture_output=True, text=True)
    assert r.returncode != 0
    assert "VerdictFileInvalid" in r.stderr
    assert "dv_mp05" in r.stderr and "ob_hd07" in r.stderr
    assert not out.exists()


# ------------------------------------------------------------------ 2 node class
@pytest.mark.parametrize("verdicts,expected", [
    (["tight", "tight", "tight"], "tight"),
    (["tight", "loose", "tight"], "loose"),
    (["loose", "cannot-judge", "tight"], "loose"),
    (["loose", "cannot-judge", "cannot-judge"], "loose"),
    (["tight", "cannot-judge", "tight"], "partial"),
    (["tight", "cannot-judge", "cannot-judge"], "partial"),
    (["cannot-judge", "cannot-judge", "cannot-judge"], "cannot-judge"),
])
def test_node_class(verdicts, expected):
    checks = {f"c{i}": {"verdict": v, "reason": "r"} for i, v in enumerate(verdicts)}
    assert an.node_class(checks) == expected


# ------------------------------------------------------------------ 4 rates
def wilson(k, n, z=1.959963984540054):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def test_wilson_known_values():
    lo, hi = an.wilson(2, 12)
    elo, ehi = wilson(2, 12)
    assert (lo, hi) == pytest.approx((elo, ehi))
    assert an.wilson(0, 10)[0] == pytest.approx(0.0, abs=1e-12)
    assert an.wilson(10, 10)[1] == pytest.approx(1.0, abs=1e-12)


def test_stratum_bounds_count_partial_as_tight_low_and_loose_high(report):
    s = P(report)["derivation"]["strata"]["derivation:inductive_generalization"]
    assert (s["n"], s["loose"], s["partial"], s["cannot_judge"], s["tight"]) == (12, 2, 2, 1, 7)
    assert s["n_judgeable"] == 11  # the cannot-judge node leaves the denominator
    assert s["low"]["rate"] == pytest.approx(2 / 11)
    assert s["high"]["rate"] == pytest.approx(4 / 11)
    assert (s["low"]["ci_low"], s["low"]["ci_high"]) == pytest.approx(wilson(2, 11))
    assert (s["high"]["ci_low"], s["high"]["ci_high"]) == pytest.approx(wilson(4, 11))


def test_stratum_of_exactly_ten_reports_a_rate(report):
    s = P(report)["derivation"]["strata"]["derivation:deductive_modus_ponens"]
    assert s["n"] == 10 and (s["loose"], s["partial"]) == (1, 1)
    assert s["low"]["rate"] == pytest.approx(0.1) and s["high"]["rate"] == pytest.approx(0.2)


def test_stratum_below_ten_is_counts_only(report):
    for kind, name in (("derivation", "derivation:inductive_analogy"), ("observation", "observation:editorial")):
        s = P(report)[kind]["strata"][name]
        assert "low" not in s and "high" not in s and "rate" not in s
        assert s["n"] in (9, 3) and "loose" in s and "partial" in s and "cannot_judge" in s


def test_markdown_prints_no_rate_for_small_stratum(world, tmp_path):
    out = tmp_path / "out"
    an.main(args_for(world, out))
    md = (out / "report.md").read_text()
    line = [ln for ln in md.splitlines() if "inductive_analogy" in ln and "n=9" in ln]
    assert line, "stratum line with n=9 must be printed"
    assert "%" not in line[0] and "rate" not in line[0].lower().replace("counts only", "")
    assert "counts only" in line[0]


def test_population_weighted_rate_derivations(report):
    w = P(report)["derivation"]["weighted"]
    assert w["low"] == pytest.approx(0.5 * (2 / 11) + 0.3 * (1 / 10) + 0.2 * (1 / 9))
    assert w["high"] == pytest.approx(0.5 * (4 / 11) + 0.3 * (2 / 10) + 0.2 * (1 / 9))
    assert w["n_cannot_judge_excluded"] == 1  # dv_ig07, printed beside the rate
    assert w["weights"] == pytest.approx({"derivation:inductive_generalization": 0.5,
                                          "derivation:deductive_modus_ponens": 0.3,
                                          "derivation:inductive_analogy": 0.2})


def test_population_weighted_rate_observations(report):
    w = P(report)["observation"]["weighted"]
    assert w["low"] == pytest.approx(0.8 * 0.1 + 0.2 * (1 / 3))
    assert w["high"] == pytest.approx(0.8 * 0.2 + 0.2 * (1 / 3))


def test_weighted_rate_also_reported_over_rated_strata_only(report):
    w = P(report)["derivation"]["weighted"]["rated_strata_only"]
    assert w["low"] == pytest.approx((100 / 160) * (2 / 11) + (60 / 160) * 0.1)
    assert w["high"] == pytest.approx((100 / 160) * (4 / 11) + (60 / 160) * 0.2)
    assert w["n_cannot_judge_excluded"] == 1


def test_census_stratum_with_no_drawn_nodes_is_listed_not_hidden(report):
    w = P(report)["derivation"]["weighted"]
    assert "derivation:deductive_reductio" in w["strata_without_draw"]


def _nodes(**counts):
    """Synthetic stratum members with the given class counts (tight=, loose=, partial=, cj=)."""
    cls = {"tight": "tight", "loose": "loose", "partial": "partial", "cj": "cannot-judge"}
    return [{"class": cls[k]} for k, n in counts.items() for _ in range(n)]


def test_cannot_judge_leaves_the_denominator_of_the_stratum_bounds():
    """tight=2, loose=1, partial=1, cannot-judge=2: judgeable n is 4, so low 1/4 and high 2/4."""
    s = an.stratum_row(_nodes(tight=2, loose=1, partial=1, cj=2), min_n=1)
    assert (s["n"], s["n_judgeable"], s["cannot_judge"]) == (6, 4, 2)
    assert s["low"]["rate"] == pytest.approx(1 / 4)
    assert s["high"]["rate"] == pytest.approx(2 / 4)
    assert (s["low"]["ci_low"], s["low"]["ci_high"]) == pytest.approx(wilson(1, 4))
    assert (s["high"]["ci_low"], s["high"]["ci_high"]) == pytest.approx(wilson(2, 4))


def test_partial_nodes_stay_in_the_denominator():
    s = an.stratum_row(_nodes(tight=2, loose=1, partial=3), min_n=1)
    assert s["n_judgeable"] == 6
    assert s["low"]["rate"] == pytest.approx(1 / 6) and s["high"]["rate"] == pytest.approx(4 / 6)


def test_small_n_rule_applies_to_the_judgeable_n_not_the_drawn_n():
    # 12 drawn but only 7 judgeable: counts only, no rate, no interval
    s = an.stratum_row(_nodes(tight=5, loose=1, partial=1, cj=5))
    assert s["n"] == 12 and s["n_judgeable"] == 7 and "low" not in s and "high" not in s
    # 10 judgeable (plus 2 cannot-judge) reports a rate
    s = an.stratum_row(_nodes(tight=8, loose=1, partial=1, cj=2))
    assert s["n"] == 12 and s["n_judgeable"] == 10
    assert s["low"]["rate"] == pytest.approx(1 / 10)


def test_stratum_with_no_judgeable_node_has_no_rate_and_is_excluded_from_the_weights():
    s = an.stratum_row(_nodes(cj=3), min_n=1)
    assert s["n_judgeable"] == 0 and "low" not in s and "high" not in s
    rows = {"derivation:a": s, "derivation:b": an.stratum_row(_nodes(tight=3, loose=1), min_n=1)}
    w = an.weighted_rate(rows, {"derivation:a": 50, "derivation:b": 50}, "derivation")
    assert w["weights"] == {"derivation:b": 1.0}          # renormalised over strata that have a rate
    assert w["low"] == pytest.approx(1 / 4)
    assert w["n_cannot_judge_excluded"] == 3              # a's nodes are still counted beside the rate


def test_markdown_prints_the_cannot_judge_count_beside_each_rate(world, tmp_path):
    out = tmp_path / "out"
    an.main(args_for(world, out))
    md = (out / "report.md").read_text()
    line = [ln for ln in md.splitlines() if ln.startswith("- derivation:inductive_generalization: n=12")]
    assert line and "judgeable 11" in line[0] and "cannot-judge 1" in line[0]
    assert any("cannot-judge nodes excluded from the denominator: 1" in ln for ln in md.splitlines())


# ------------------------------------------------------------------ 3 controls
def test_controls_never_enter_a_rate(report):
    for st in P(report)["derivation"]["strata"].values():
        assert st["n"] == st["loose"] + st["partial"] + st["cannot_judge"] + st["tight"]
    n_d = sum(s["n"] for s in P(report)["derivation"]["strata"].values())
    n_o = sum(s["n"] for s in P(report)["observation"]["strata"].values())
    assert (n_d, n_o) == (31, 13)
    # a loose control with confidence .999 in the loose group would move the loose mean
    conf = P(report)["derivation"]["confidence"]
    assert conf["n_loose"] == 4 and conf["n_tight"] == 23
    assert conf["mean_loose"] == pytest.approx((0.931 + 0.7 + 0.588 + 0.5) / 4)


def test_controls_sensitivity_specificity_as_counts(report):
    m, z = report["controls"]["mira"], report["controls"]["zephyr"]
    assert (m["sensitivity"]["k"], m["sensitivity"]["n"]) == (2, 3)
    assert (m["specificity"]["k"], m["specificity"]["n"]) == (1, 2)
    assert (z["sensitivity"]["k"], z["sensitivity"]["n"]) == (3, 3)
    assert (z["specificity"]["k"], z["specificity"]["n"]) == (2, 2)
    assert m["sensitivity"]["text"] == "2/3" and m["specificity"]["text"] == "1/2"
    # classes among controls: Mira's missed loose control was classed tight; one tight control is partial
    assert m["known_loose_classes"] == {"loose": 2, "tight": 1, "partial": 0, "cannot-judge": 0}
    assert m["known_tight_classes"] == {"loose": 0, "tight": 1, "partial": 1, "cannot-judge": 0}


def test_controls_agreement_reported_separately(report):
    a = report["controls"]["agreement"]
    assert (a["n"], a["agree"]) == (5, 3)
    assert a["percent_agreement"] == pytest.approx(60.0)
    assert {d["id"] for d in a["disagreements"]} == {"dv_cl2", "ob_ct1"}


def test_control_ids_only_in_controls_section_and_notes_never(world, tmp_path):
    out = tmp_path / "out"
    an.main(args_for(world, out))
    rj = json.loads((out / "report.json").read_text())
    rest = dict(rj)
    controls = rest.pop("controls")
    blob = json.dumps(rest)
    for cid in CTL_ALL:
        assert cid not in blob, cid
        assert cid in json.dumps(controls)
    md = (out / "report.md").read_text()
    sections = md.split("\n## ")
    seen_in_controls = False
    for s in sections:
        head = s.splitlines()[0] if s.splitlines() else ""
        for cid in CTL_ALL:
            if head.lower().startswith("controls"):
                continue
            assert cid not in s, (cid, head)
        if head.lower().startswith("controls"):
            seen_in_controls = any(cid in s for cid in CTL_ALL)
    assert seen_in_controls
    assert NOTE not in md and NOTE not in (out / "report.json").read_text()


# ------------------------------------------------------------------ 5 IG + confusion
def test_inductive_generalization_rate_on_its_own(report):
    ig = P(report)["derivation"]["inductive_generalization"]
    assert (ig["n"], ig["loose"], ig["partial"], ig["cannot_judge"]) == (12, 2, 2, 1)
    assert ig["low"]["rate"] == pytest.approx(2 / 11) and ig["high"]["rate"] == pytest.approx(4 / 11)


def test_confusion_table_declared_by_proposed_over_loose_type(report):
    c = P(report)["derivation"]["confusion"]
    assert c == {"inductive_generalization": {"deductive_modus_ponens": 1},
                 "deductive_modus_ponens": {"inductive_generalization": 1},
                 "inductive_analogy": {"deductive_conjunction": 1}}


# ------------------------------------------------------------------ 6 confidence vs verdict
def auc_ref(tight, loose):
    wins = sum((t > l) + 0.5 * (t == l) for t in tight for l in loose)
    return wins / (len(tight) * len(loose))


def test_auc_function_counts_ties_half():
    assert an.auc([0.9, 0.5], [0.5, 0.1]) == pytest.approx(auc_ref([0.9, 0.5], [0.5, 0.1]))
    assert an.auc([0.9, 0.5], [0.5, 0.1]) == pytest.approx((1 + 1 + 0.5 + 1) / 4)


def test_auc_direction_is_tight_greater_than_loose():
    assert an.auc([0.9, 0.8], [0.2, 0.1]) == 1.0
    assert an.auc([0.2, 0.1], [0.9, 0.8]) == 0.0


def test_derivation_confidence_numbers(report):
    c = P(report)["derivation"]["confidence"]
    assert c["mean_tight"] == pytest.approx(20 / 23)
    assert c["auc"] == pytest.approx(65.5 / 92)
    assert (c["n_tight"], c["n_loose"], c["n_partial"], c["n_cannot_judge"]) == (23, 4, 3, 1)
    lo, hi = c["auc_ci"]
    assert 0.0 <= lo <= c["auc"] <= hi <= 1.0


def test_observation_confidence_numbers(report):
    c = P(report)["observation"]["confidence"]
    assert (c["n_tight"], c["n_loose"], c["n_partial"], c["n_cannot_judge"]) == (10, 2, 1, 0)
    assert c["mean_tight"] == pytest.approx(0.75) and c["mean_loose"] == pytest.approx(0.65)
    assert c["auc"] == pytest.approx(9 / 20)


@pytest.mark.parametrize("lo,hi,expected", [
    (0.55, 0.9, READING_TRACKS),
    (0.5000001, 0.6, READING_TRACKS),
    (0.5, 0.9, READING_NONE),      # lower bound == 0.5 includes 0.5
    (0.3, 0.7, READING_NONE),
    (0.1, 0.5, READING_NONE),      # upper bound == 0.5 includes 0.5
    (0.1, 0.4999999, READING_AGAINST),
    (0.0, 0.3, READING_AGAINST),
])
def test_reading_is_chosen_mechanically(lo, hi, expected):
    assert an.reading(lo, hi) == expected


def test_reading_strings_are_verbatim():
    assert (READING_TRACKS, READING_NONE, READING_AGAINST) == (
        an.READING_TRACKS, an.READING_NONE, an.READING_AGAINST)


def test_end_to_end_reading_direction_tracks_and_against():
    tight, loose = [0.9] * 12, [0.3] * 12
    r = an.auc_report(tight, loose, seed=SEED, label="x", n_boot=500)
    assert r["auc"] == 1.0 and r["reading"] == READING_TRACKS
    r = an.auc_report(loose, tight, seed=SEED, label="x", n_boot=500)
    assert r["auc"] == 0.0 and r["reading"] == READING_AGAINST


def test_end_to_end_reading_none_when_overlapping_small_n():
    r = an.auc_report([0.9, 0.3, 0.6], [0.7, 0.4, 0.8], seed=SEED, label="x", n_boot=500)
    assert r["reading"] == READING_NONE


def test_auc_not_computable_without_both_groups():
    r = an.auc_report([0.9, 0.8], [], seed=SEED, label="x", n_boot=100)
    assert r["auc"] is None and r["reading"].startswith("not computable")


def test_bootstrap_is_seeded_and_default_is_10000():
    assert an.N_BOOT == 10000
    a = an.auc_report([0.9, 0.3, 0.6, 0.5], [0.7, 0.4, 0.8], seed="s1", label="x", n_boot=300)
    b = an.auc_report([0.9, 0.3, 0.6, 0.5], [0.7, 0.4, 0.8], seed="s1", label="x", n_boot=300)
    c = an.auc_report([0.9, 0.3, 0.6, 0.5], [0.7, 0.4, 0.8], seed="s2", label="x", n_boot=300)
    assert a == b and a["auc_ci"] != c["auc_ci"]


def test_report_reading_is_printed_verbatim_in_markdown(world, tmp_path):
    out = tmp_path / "out"
    an.main(args_for(world, out))
    rj = json.loads((out / "report.json").read_text())
    md = (out / "report.md").read_text()
    for kind in ("derivation", "observation"):
        assert P(rj)[kind]["confidence"]["reading"] in md


# ------------------------------------------------------------------ 7 confidence deltas
def test_formula_uses_v051_tables():
    f = an.v051_confidence
    assert f("deductive_modus_ponens", [0.9, 0.8]) == pytest.approx(0.784)
    assert f("inductive_generalization", [0.9, 0.8]) == pytest.approx(0.931)
    assert f("abductive_best_explanation", [0.9, 0.8]) == pytest.approx(0.64)
    assert f("abductive_best_explanation", [1.0]) == pytest.approx(0.8)     # the cap binds
    assert f("authority_consensus", [0.5, 0.5]) == pytest.approx(0.735)     # corroboration class
    assert f("inductive_analogy", [0.9, 0.8]) == pytest.approx(0.56)
    assert f("deductive_conjunction", [0.9]) is None                        # not in the v0.5.1 table


def test_deltas_recomputed_under_proposed_type_with_own_premises(report):
    rows = {r["id"]: r for r in report["deltas"]["computed"]}
    assert set(rows) == {"dv_ig01", "dv_mp01"}
    # premises = derives_from UNION acknowledged_derives_from (.9, .8, .1); the `cites` edge is ignored
    r = rows["dv_ig01"]
    assert (r["declared_type"], r["proposed_type"]) == ("inductive_generalization", "deductive_modus_ponens")
    assert r["n_premises"] == 3
    assert r["stored"] == pytest.approx(0.931) and r["recomputed"] == pytest.approx(0.098)  # min .1 * .98
    assert r["delta"] == pytest.approx(0.098 - 0.931)
    r = rows["dv_mp01"]  # premises .9, .6 -> (1 - .1*.4) * .95 = .912
    assert r["recomputed"] == pytest.approx(0.912) and r["delta"] == pytest.approx(0.912 - 0.588)


def _delta_db(tmp_path, nodes, edges):
    p = tmp_path / "d.db"
    c = sqlite3.connect(p)
    c.executescript("CREATE TABLE nodes (id TEXT PRIMARY KEY, confidence REAL, metadata TEXT);"
                    "CREATE TABLE edges (id INTEGER PRIMARY KEY, source_id TEXT, target_id TEXT, relation TEXT);")
    for i, v in nodes.items():
        c.execute("INSERT INTO nodes VALUES (?,?,?)", (i, v, "{}"))
    for s_, t, r in edges:
        c.execute("INSERT INTO edges (source_id, target_id, relation) VALUES (?,?,?)", (s_, t, r))
    c.commit()
    c.close()
    return an.open_ro(p)


def _loose_type_node(node_id, declared, proposed):
    r = row(node_id, "L", "type", proposed)
    return {"id": node_id, "kind": "derivation", "declared": declared, "checks": r["checks"]}


def test_premise_set_is_derives_from_union_acknowledged_derives_from(tmp_path):
    """The stored value was computed from BOTH relations (the project's computed-from set, as
    tools/modus_ponens_check.py defines it), so the recompute must read both: a deductive
    recompute is the min over both, here the acknowledged premise (.5) binding over the
    derives_from one (.9)."""
    con = _delta_db(tmp_path, {"dv_x": 0.882, "p_df": 0.9, "p_ack": 0.5, "p_cite": 0.1},
                    [("dv_x", "p_df", "derives_from"), ("dv_x", "p_ack", "acknowledged_derives_from"),
                     ("dv_x", "p_cite", "cites")])
    assert sorted(an.db_premise_confidences(con, "dv_x")) == [0.5, 0.9]
    d = an.deltas_block(con, [_loose_type_node("dv_x", "inductive_generalization", "deductive_modus_ponens")])
    r = d["computed"][0]
    assert r["n_premises"] == 2
    assert r["recomputed"] == pytest.approx(0.49)          # min(.9, .5) * .98
    assert r["delta"] == pytest.approx(0.49 - 0.882)
    con.close()


def test_acknowledged_premise_alone_still_counts_and_a_shared_target_counts_once(tmp_path):
    con = _delta_db(tmp_path, {"dv_y": 0.9, "dv_z": 0.9, "p1": 0.6, "p2": 0.5},
                    [("dv_y", "p1", "acknowledged_derives_from"),
                     ("dv_z", "p2", "derives_from"), ("dv_z", "p2", "acknowledged_derives_from"),
                     ("dv_z", "dv_z", "derives_from")])  # self-loop never a premise
    assert an.db_premise_confidences(con, "dv_y") == [0.6]
    assert an.db_premise_confidences(con, "dv_z") == [0.5]
    # a corroboration type would double-count a target listed under both relations
    d = an.deltas_block(con, [_loose_type_node("dv_z", "deductive_modus_ponens", "inductive_generalization")])
    assert d["computed"][0]["recomputed"] == pytest.approx(0.475)   # (1 - .5) * .95, one premise
    con.close()


def test_unknown_proposed_type_is_listed_never_computed(report):
    nc = report["deltas"]["not_computed"]
    assert [r["id"] for r in nc] == ["dv_an01"]
    assert nc[0]["proposed_type"] == "deductive_conjunction"  # clause 13: pinned publishable name, rendered as itself
    assert "v0.5.1" in nc[0]["reason"]
    assert "dv_an01" not in {r["id"] for r in report["deltas"]["computed"]}


def test_delta_distribution(report):
    s = report["deltas"]["summary"]
    d1, d2 = 0.098 - 0.931, 0.912 - 0.588
    assert s["n"] == 2
    assert s["min"] == pytest.approx(min(d1, d2)) and s["max"] == pytest.approx(max(d1, d2))
    assert s["median"] == pytest.approx((d1 + d2) / 2)


# ------------------------------------------------------------------ 8 agreement
def test_agreement_on_node_class_with_partial_as_category(report):
    a = report["agreement"]
    assert a["n_overlap"] == 8 and a["n_agree"] == 5
    assert a["percent_agreement"] == pytest.approx(62.5)
    assert a["kappa_class"] == pytest.approx(0.4)          # po .625, pe 24/64
    assert a["kappa_tight_loose"] == pytest.approx(2 / 3)  # n=6, po 5/6, pe .5
    assert a["n_tight_loose_both"] == 6


def test_agreement_lists_every_disagreement(report):
    d = {x["id"]: (x["mira"], x["zephyr"]) for x in report["agreement"]["disagreements"]}
    assert d == {"dv_ig01": ("loose", "tight"), "dv_ig03": ("partial", "tight"),
                 "ob_hd01": ("loose", "partial")}


def test_agreement_excludes_controls(report):
    a = report["agreement"]
    assert a["n_overlap"] == 8
    assert not ({x["id"] for x in a["disagreements"]} & set(CTL_ALL))


def test_per_check_agreement(report):
    pc = report["agreement"]["per_check"]
    assert (pc["type"]["n"], pc["type"]["agree"]) == (6, 4)
    assert pc["type"]["percent_agreement"] == pytest.approx(100 * 4 / 6)
    assert (pc["support-overreach"]["n"], pc["support-overreach"]["agree"]) == (2, 1)


def test_kappa_undefined_is_none_not_an_error():
    assert an.cohens_kappa(["tight", "tight"], ["tight", "tight"]) is None
    assert an.cohens_kappa(["a", "b", "a", "b"], ["a", "b", "a", "b"]) == pytest.approx(1.0)


# ------------------------------------------------------------------ 9 cannot-judge
def test_cannot_judge_counts_per_check_and_per_class(report):
    cj = report["cannot_judge"]["mira"]
    assert cj["per_check"]["type"]["cannot-judge"] == 4          # ig03, ig11, mp03 partial + ig07
    assert cj["per_check"]["placement"]["cannot-judge"] == 1     # ig07
    assert cj["per_check"]["chain-overreach"]["cannot-judge"] == 1
    assert cj["per_check"]["support-overreach"]["cannot-judge"] == 1   # hd03
    assert cj["per_check"]["type"]["loose"] == 3
    assert cj["per_class"]["derivation"] == {"loose": 4, "tight": 23, "partial": 3, "cannot-judge": 1}
    assert cj["per_class"]["observation"] == {"loose": 2, "tight": 10, "partial": 1, "cannot-judge": 0}


def test_cannot_judge_never_folded_into_tight_or_loose(report):
    s = P(report)["derivation"]["strata"]["derivation:inductive_generalization"]
    assert s["cannot_judge"] == 1 and s["tight"] == 7 and s["loose"] == 2


# ------------------------------------------------------------------ 10 analyst-prior node
def test_every_rate_reported_with_and_without_prior_node(report):
    assert set(report["passes"]) == {"with_prior", "without_prior"}
    for name in ("with_prior", "without_prior"):
        p = report["passes"][name]
        for kind in ("derivation", "observation"):
            assert {"strata", "weighted", "confidence"} <= set(p[kind])
        assert {"inductive_generalization", "confusion"} <= set(p["derivation"])


def test_without_prior_drops_exactly_that_node(report):
    w = P(report, "without_prior")["derivation"]
    s = w["strata"]["derivation:inductive_generalization"]
    assert (s["n"], s["loose"], s["partial"], s["cannot_judge"], s["tight"]) == (11, 1, 2, 1, 7)
    assert s["n_judgeable"] == 10
    assert s["low"]["rate"] == pytest.approx(1 / 10) and s["high"]["rate"] == pytest.approx(3 / 10)
    assert w["confusion"] == {"deductive_modus_ponens": {"inductive_generalization": 1},
                              "inductive_analogy": {"deductive_conjunction": 1}}
    assert w["confidence"]["n_loose"] == 3
    assert w["confidence"]["auc"] == pytest.approx(65.5 / 69)
    # observations are untouched by a derivation prior
    assert P(report, "without_prior")["observation"]["strata"] == P(report)["observation"]["strata"]


def test_without_prior_small_stratum_rule_applies_to_the_reduced_n(world, tmp_path):
    out = tmp_path / "out"
    an.main(args_for(world, out, prior="dv_mp01"))
    rj = json.loads((out / "report.json").read_text())
    s = rj["passes"]["without_prior"]["derivation"]["strata"]["derivation:deductive_modus_ponens"]
    assert s["n"] == 9 and "low" not in s and "high" not in s
    assert "low" in rj["passes"]["with_prior"]["derivation"]["strata"]["derivation:deductive_modus_ponens"]


def test_prior_node_must_be_a_sampled_node(world, tmp_path):
    with pytest.raises(an.InputInvalid):
        an.main(args_for(world, tmp_path / "out", prior="dv_cl1"))
    with pytest.raises(an.InputInvalid):
        an.main(args_for(world, tmp_path / "out2", prior="dv_nope"))


# ------------------------------------------------------------------ 11 determinism
def test_byte_identical_outputs_same_inputs_same_seed(world, tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    an.main(args_for(world, a))
    an.main(args_for(world, b))
    for f in ("report.json", "report.md"):
        assert (a / f).read_bytes() == (b / f).read_bytes()


def _file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def test_report_carries_sha256_of_each_input_verdict_file(world, tmp_path):
    out = tmp_path / "out"
    an.main(args_for(world, out))
    rep = json.loads((out / "report.json").read_text())
    want = {"mira": _file_sha(world / "mira.jsonl"), "zephyr": _file_sha(world / "zephyr.jsonl")}
    assert want["mira"] != want["zephyr"]
    assert rep["meta"]["verdict_sha256"] == want
    md = (out / "report.md").read_text()
    assert want["mira"] in md and want["zephyr"] in md


def test_verdict_hash_changes_only_for_the_reader_whose_file_changed(world, tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    an.main(args_for(world, a))
    m = world / "mira.jsonl"
    raw = m.read_bytes()
    assert raw.count(b'"reason": "r"') > 0
    m.write_bytes(raw.replace(b'"reason": "r"', b'"reason": "s"', 1))  # one byte of one reason
    an.main(args_for(world, b))
    ha = json.loads((a / "report.json").read_text())["meta"]["verdict_sha256"]
    hb = json.loads((b / "report.json").read_text())["meta"]["verdict_sha256"]
    assert ha["mira"] != hb["mira"]
    assert ha["zephyr"] == hb["zephyr"]
    assert hb["mira"] == _file_sha(m)


def test_verdict_hash_is_of_file_bytes_not_of_validated_rows(world, tmp_path):
    # re-serialising the same rows (spacing) leaves the rows identical but the bytes different
    m = world / "mira.jsonl"
    rows = [json.loads(l) for l in m.read_text().splitlines()]
    m.write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in rows))
    out = tmp_path / "out"
    an.main(args_for(world, out))
    assert json.loads((out / "report.json").read_text())["meta"]["verdict_sha256"]["mira"] == _file_sha(m)


def test_different_seed_leaves_auc_point_estimate_and_strata_unchanged(world, tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    an.main(args_for(world, a))
    argv = args_for(world, b)
    argv[argv.index("--seed") + 1] = "another-seed"
    an.main(argv)
    ra, rb = (json.loads((d / "report.json").read_text()) for d in (a, b))
    assert P(ra)["derivation"]["confidence"]["auc"] == P(rb)["derivation"]["confidence"]["auc"]
    # (the seed-sensitivity of the interval itself is asserted in test_bootstrap_is_seeded_...;
    # at 2-4 loose nodes the interval ends here can coincide for any seed)
    for k in ("derivation", "observation"):
        assert P(ra)[k]["strata"] == P(rb)[k]["strata"]


# ------------------------------------------------------------------ 12 outputs
def test_out_inside_worktree_is_refused_and_nothing_written(world):
    out = REPO / "studies" / "node-audit" / "_analysis_out_test"
    with pytest.raises(an.OutputInsideWorktree):
        an.main(args_for(world, out))
    assert not out.exists()


def test_out_equal_to_worktree_root_is_refused(world):
    with pytest.raises(an.OutputInsideWorktree):
        an.main(args_for(world, REPO))


def test_out_outside_worktree_writes_exactly_the_report_and_the_public_export(world, tmp_path):
    out = tmp_path / "fresh" / "out"
    assert an.main(args_for(world, out)) == 0
    assert sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()) == [
        "public/verdicts-mira.public.jsonl", "public/verdicts-zephyr.public.jsonl",
        "report.json", "report.md"]


def test_cli_end_to_end_exit_zero(world, tmp_path):
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, str(TOOL)] + args_for(world, out), capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert (out / "report.json").exists() and (out / "report.md").exists()


def test_cli_out_inside_worktree_exits_nonzero(world):
    out = REPO / "studies" / "node-audit" / "_analysis_out_test"
    r = subprocess.run([sys.executable, str(TOOL)] + args_for(world, out), capture_output=True, text=True)
    assert r.returncode != 0 and "OutputInsideWorktree" in r.stderr
    assert not out.exists()


# ------------------------------------------------------------------ inputs
def test_db_is_opened_read_only(world, tmp_path):
    con = an.open_ro(world / "snap.db")
    with pytest.raises(sqlite3.OperationalError):
        con.execute("INSERT INTO nodes VALUES ('x', 1.0, '{}')")
    con.close()


def test_declared_type_in_db_must_match_the_stratum(world, tmp_path):
    c = sqlite3.connect(world / "snap.db")
    c.execute("UPDATE nodes SET metadata=? WHERE id='dv_ig05'", (json.dumps({"reasoning_type": "inductive_analogy"}),))
    c.commit()
    c.close()
    with pytest.raises(an.InputInvalid) as e:
        an.main(args_for(world, tmp_path / "out"))
    assert "dv_ig05" in str(e.value)


def test_missing_confidence_for_a_joined_node_is_refused(world, tmp_path):
    c = sqlite3.connect(world / "snap.db")
    c.execute("UPDATE nodes SET confidence=NULL WHERE id='dv_ig05'")
    c.commit()
    c.close()
    with pytest.raises(an.InputInvalid) as e:
        an.main(args_for(world, tmp_path / "out"))
    assert "dv_ig05" in str(e.value)


def test_a_control_that_is_also_sampled_is_refused(world, tmp_path):
    ctl = controls_obj()
    ctl["known_loose"]["dv_ig05"] = NOTE
    (world / "controls.json").write_text(json.dumps(ctl))
    with pytest.raises(an.InputInvalid) as e:
        an.main(args_for(world, tmp_path / "out"))
    assert "dv_ig05" in str(e.value)


def test_module_docstring_states_the_contract():
    doc = an.__doc__
    for needle in ("VerdictFileInvalid", "Wilson", "10 judgeable", "partial", "AUC", "v0.5.1", "byte-identical"):
        assert needle in doc


# ---- round 3: the "Free parameters" section (every number's choices visible in the report)
FREE_KEYS = ("small_stratum_rule", "rate_denominator", "partial_bounds", "interval", "population_weights",
             "auc", "reading_thresholds", "confidence_deltas", "readers")


def _free_md_section(md):
    lines = md.splitlines()
    i = lines.index("## Free parameters")
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("## ")), len(lines))
    return i, lines[i:j]


def test_free_parameters_section_in_md_directly_after_header_paragraph(world, tmp_path):
    out = tmp_path / "out"
    an.main(args_for(world, out))
    md = (out / "report.md").read_text()
    i, sec = _free_md_section(md)
    # title, blank, two header-paragraph lines, blank, then the section
    assert not any(ln.startswith("## ") for ln in md.splitlines()[:i])
    assert md.splitlines()[:2] == ["# Node audit analysis report", ""] and md.splitlines()[i - 1] == ""
    assert i == 5
    assert sum(1 for ln in sec if ln.startswith("- ")) == len(FREE_KEYS)  # one short line each


def test_free_parameters_keys_in_json_meta(report):
    fp = report["meta"]["free_parameters"]
    assert set(fp) == set(FREE_KEYS)
    assert all(isinstance(v, str) and v and "\n" not in v for v in fp.values())


def test_free_parameters_md_lines_are_the_json_values(world, tmp_path):
    out = tmp_path / "out"
    an.main(args_for(world, out))
    fp = json.loads((out / "report.json").read_text())["meta"]["free_parameters"]
    _, sec = _free_md_section((out / "report.md").read_text())
    for v in fp.values():
        assert f"- {v}" in sec


def test_free_parameters_state_the_actual_constants(report):
    fp = report["meta"]["free_parameters"]
    assert str(an.MIN_RATE_N) in fp["small_stratum_rule"]
    assert str(an.Z95) in fp["interval"]
    assert str(an.N_BOOT) in fp["auc"] and an.BOOT_SEED_FORMAT in fp["auc"] and SEED in fp["auc"]
    for r in (an.READING_TRACKS, an.READING_NONE, an.READING_AGAINST, an.READING_NA):
        assert r in fp["reading_thresholds"]
    assert "acknowledged_derives_from" in fp["confidence_deltas"] and "v0.5.1" in fp["confidence_deltas"]
    assert PRIOR in fp["readers"]


def test_free_parameters_values_are_read_from_the_constants_not_retyped(world, monkeypatch):
    monkeypatch.setattr(an, "MIN_RATE_N", 7)
    monkeypatch.setattr(an, "READING_NONE", "MUTATED-READING")
    monkeypatch.setattr(an, "Z95", 1.5)
    rep = an.run_analysis(world / "mira.jsonl", world / "zephyr.jsonl", world / "controls.json",
                          world / "snap.db", world / "drawn.json", PRIOR, SEED, n_boot=123)
    fp = rep["meta"]["free_parameters"]
    assert "7" in fp["small_stratum_rule"] and "10" not in fp["small_stratum_rule"]
    assert "MUTATED-READING" in fp["reading_thresholds"]
    assert "1.5" in fp["interval"]
    assert "123" in fp["auc"] and "10000" not in fp["auc"]


# ---- clauses 13-14: no content in any output; the public verdict export
PLACEHOLDER = "other (not a v0.5.1 type; text withheld)"  # literal on purpose: not read from the tool
FREE_PT = "SENTINEL_PT free text"
FREE_PT_Z = "SENTINEL_PT zephyr text"


def _sentinel_rows(spec, reader):
    rows = rows_from(spec)
    for r in rows:
        for name, c in r["checks"].items():
            c["reason"] = f"SENTINEL_REASON_{reader}_{r['id']}_{name}"
    return rows


@pytest.fixture
def sworld(tmp_path):
    """A world where every content source carries a distinctive SENTINEL."""
    w = tmp_path / "sw"
    w.mkdir()
    (w / "drawn.json").write_text(json.dumps(DRAWN))
    ctl = controls_obj()
    ctl["known_loose"] = {i: f"SENTINEL_NOTE_{i}" for i in CTL_LOOSE}
    ctl["known_tight_placement_verified"] = {i: f"SENTINEL_NOTE_{i}" for i in CTL_TIGHT_PV}
    ctl["other_key"] = {"ignored": "SENTINEL_NOTE_other"}
    (w / "controls.json").write_text(json.dumps(ctl))
    ms = mira_spec()
    ms["dv_an01"] = ("L", "type", FREE_PT)
    zs = zeph_spec()
    zs["dv_ig04"] = ("L", "type", FREE_PT_Z)
    write_jsonl(w / "mira.jsonl", _sentinel_rows(ms, "mira"))
    write_jsonl(w / "zephyr.jsonl", _sentinel_rows(zs, "zephyr"))
    make_db(w / "snap.db")
    c = sqlite3.connect(w / "snap.db")
    c.execute("ALTER TABLE nodes ADD COLUMN claim TEXT")
    for nid, md in c.execute("SELECT id, metadata FROM nodes").fetchall():
        m = json.loads(md)
        m["logical_chain"] = f"SENTINEL_CHAIN_{nid}"
        c.execute("UPDATE nodes SET claim=?, metadata=? WHERE id=?",
                  (f"SENTINEL_CLAIM_{nid}", json.dumps(m), nid))
    c.commit()
    c.close()
    return w


@pytest.fixture
def sout(sworld, tmp_path):
    out = tmp_path / "sout"
    an.main(args_for(sworld, out))
    return out


def _all_files(out):
    return sorted(p for p in out.rglob("*") if p.is_file())


def _public(out, who):
    text = (out / "public" / f"verdicts-{who}.public.jsonl").read_text()
    return text, [json.loads(line) for line in text.splitlines()]


def test_13_no_sentinel_in_any_output_file(sout):
    files = _all_files(sout)
    names = {p.relative_to(sout).as_posix() for p in files}
    assert {"report.json", "report.md", "public/verdicts-mira.public.jsonl",
            "public/verdicts-zephyr.public.jsonl"} <= names  # the walk is not vacuous
    for p in files:
        assert b"SENTINEL" not in p.read_bytes(), p.name


def test_13_free_text_proposed_type_is_the_fixed_placeholder_everywhere(sout):
    rj = json.loads((sout / "report.json").read_text())
    md = (sout / "report.md").read_text()
    assert rj["passes"]["with_prior"]["derivation"]["confusion"]["inductive_analogy"] == {PLACEHOLDER: 1}
    assert rj["passes"]["without_prior"]["derivation"]["confusion"]["inductive_analogy"] == {PLACEHOLDER: 1}
    nc = {r["id"]: r for r in rj["deltas"]["not_computed"]}
    assert nc["dv_an01"]["proposed_type"] == PLACEHOLDER
    assert f"inductive_analogy -> {PLACEHOLDER}: 1" in md
    assert f"- dv_an01: inductive_analogy -> {PLACEHOLDER}: NOT computed" in md
    _, mira = _public(sout, "mira")
    assert {r["id"]: r for r in mira}["dv_an01"]["checks"]["type"]["proposed_type"] == PLACEHOLDER
    _, zeph = _public(sout, "zephyr")
    assert {r["id"]: r for r in zeph}["dv_ig04"]["checks"]["type"]["proposed_type"] == PLACEHOLDER


def test_13_positive_control_real_v051_name_is_rendered_verbatim(sout):
    rj = json.loads((sout / "report.json").read_text())
    md = (sout / "report.md").read_text()
    conf = rj["passes"]["with_prior"]["derivation"]["confusion"]
    assert conf["deductive_modus_ponens"] == {"inductive_generalization": 1}
    assert conf["inductive_generalization"]["deductive_modus_ponens"] == 1
    assert "- deductive_modus_ponens -> inductive_generalization: 1" in md
    _, mira = _public(sout, "mira")
    assert {r["id"]: r for r in mira}["dv_mp01"]["checks"]["type"]["proposed_type"] == "inductive_generalization"
    _, zeph = _public(sout, "zephyr")
    assert {r["id"]: r for r in zeph}["dv_mp01"]["checks"]["type"]["proposed_type"] == "deductive_modus_tollens"


def test_13_every_v051_name_passes_through_and_nothing_else_does():
    assert an.public_type("deductive_modus_ponens") == "deductive_modus_ponens"
    for name in an._vendored().REASONING_CLASS:
        assert an.public_type(name) == name
    assert an.public_type("deductive_conjunction") == "deductive_conjunction"  # the one pinned post-v0.5.1 name
    for bad in (FREE_PT, "", " inductive_analogy", "Inductive_Analogy", "deductive_conjunction "):
        assert an.public_type(bad) == PLACEHOLDER


def test_13_publishable_set_is_v051_names_plus_exactly_deductive_conjunction():
    assert an.PUBLISHABLE_TYPE_NAMES == frozenset(an._vendored().REASONING_CLASS) | {"deductive_conjunction"}


def test_13_deductive_conjunction_is_rendered_verbatim_yet_still_not_computed(sworld, tmp_path):
    ms = mira_spec()
    ms["dv_an01"] = ("L", "type", "deductive_conjunction")
    write_jsonl(sworld / "mira.jsonl", _sentinel_rows(ms, "mira"))
    out = tmp_path / "dcout"
    an.main(args_for(sworld, out))
    rj = json.loads((out / "report.json").read_text())
    md = (out / "report.md").read_text()
    for wp in ("with_prior", "without_prior"):
        assert rj["passes"][wp]["derivation"]["confusion"]["inductive_analogy"] == {"deductive_conjunction": 1}
    nc = {r["id"]: r for r in rj["deltas"]["not_computed"]}
    assert nc["dv_an01"]["proposed_type"] == "deductive_conjunction"          # not-computed row, verbatim
    assert "dv_an01" not in {r["id"] for r in rj["deltas"]["computed"]}       # ...and still not computed
    assert "- dv_an01: inductive_analogy -> deductive_conjunction: NOT computed" in md
    assert "inductive_analogy -> deductive_conjunction: 1" in md
    _, mira = _public(out, "mira")
    assert {r["id"]: r for r in mira}["dv_an01"]["checks"]["type"]["proposed_type"] == "deductive_conjunction"
    for p in _all_files(out):
        assert b"SENTINEL" not in p.read_bytes(), p.name


def test_14_export_shape(sworld, sout):
    for who in ("mira", "zephyr"):
        text, rows = _public(sout, who)
        src = [json.loads(line) for line in (sworld / f"{who}.jsonl").read_text().splitlines()]
        assert len(rows) == len(src) and len(rows) > 0
        assert [r["id"] for r in rows] == sorted(r["id"] for r in src)
        by_src = {r["id"]: r for r in src}
        for r in rows:
            assert set(r) == {"id", "checks"}
            s = by_src[r["id"]]
            assert set(r["checks"]) == set(s["checks"])
            for name, c in r["checks"].items():
                assert c["verdict"] == s["checks"][name]["verdict"]
                extra = set(c) - {"verdict"}
                if name == "type" and s["checks"]["type"]["verdict"] == "loose":
                    assert extra == {"proposed_type"}
                else:
                    assert extra == set(), (r["id"], name)
        assert "reason" not in text
        assert text.endswith("\n") and not text.endswith("\n\n")
        for line, r in zip(text.splitlines(), rows):
            assert line == json.dumps(r, sort_keys=True, separators=(",", ":"))


def test_14_export_includes_controls_rows(sout):
    _, mira = _public(sout, "mira")
    assert set(CTL_ALL) <= {r["id"] for r in mira}


def test_14_export_is_byte_deterministic(sworld, tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    an.main(args_for(sworld, a))
    an.main(args_for(sworld, b))
    pa, pb = _all_files(a), _all_files(b)
    assert [p.relative_to(a) for p in pa] == [p.relative_to(b) for p in pb]
    for x, y in zip(pa, pb):
        assert x.read_bytes() == y.read_bytes()


def test_14_a_refused_input_writes_no_export(sworld, tmp_path):
    rows = [json.loads(line) for line in (sworld / "mira.jsonl").read_text().splitlines()]
    write_jsonl(sworld / "mira.jsonl", rows[:-1])  # one id missing
    out = tmp_path / "refused"
    with pytest.raises(an.VerdictFileInvalid):
        an.main(args_for(sworld, out))
    assert not out.exists()


def test_clauses_13_and_14_are_in_the_module_docstring():
    doc = an.__doc__
    assert "13. No content in any output" in doc and "14. Public verdict export" in doc
    assert "verdicts-mira.public.jsonl" in doc and "other (not a v0.5.1 type; text withheld)" in doc
