"""Contract tests for `studies/node-audit/build_packet.py` (paper v2 workstream D).

Written BEFORE the implementation (contract-first). The contract is the one stated in
the tool's module docstring. Cells (numbered as in the spec):

  1 strata counts exact: floor 2, 1-node type, excess redistribution, cap
  2 determinism: same seed -> identical drawn_ids.json; other seed -> other draw
  3 a control id in the population is never drawn, and appears in both packets
  4 no confidence / numeric field in a packet (and the assertion itself fires)
  5 --out inside the git worktree is refused
  6 a stripped DB (empty derivation claims) is refused
  7 Zephyr's 50 are a subset of Mira's 200, 25 of them from the IG stratum
  8 drawn_ids.json carries no control id
Extra (not in the spec's eight): 9 snapshot-hash mismatch is refused; 10 packet content.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sqlite3
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "studies" / "node-audit" / "build_packet.py"
SEED = "test-seed"


def _load():
    spec = importlib.util.spec_from_file_location("build_packet", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bp = _load()

CONF = "0.8731"  # distinctive numbers that must never reach a packet
UTIL = "0.4417"
IMPORTANCE = "0.6209"

COLS = """id TEXT PRIMARY KEY, type TEXT, claim TEXT, logical_chain TEXT, quoted_text TEXT,
 interpretation TEXT, quote_type TEXT, evidence_id TEXT, is_current INTEGER, metadata TEXT,
 source_url TEXT, source_title TEXT, source_domain TEXT, source_type TEXT,
 confidence REAL, confidence_history TEXT, importance_base REAL, importance_score REAL,
 recall_count INTEGER, utility_score REAL"""

# fixture populations (see test_1 for the hand-computed allocation)
DER = {"inductive_generalization": 60, "abductive_best_explanation": 200,
       "inductive_analogy": 30, "deductive_modus_ponens": 3, "authority_expert": 1}
OBS = {"hard_data": 100, "editorial": 3, "personal_communication": 1}


def make_db(path, der=DER, obs=OBS, claim_prefix="claim", untyped=0, predictive=0):
    c = sqlite3.connect(path)
    c.executescript(f"CREATE TABLE nodes ({COLS});"
                    "CREATE TABLE edges (id INTEGER PRIMARY KEY, source_id TEXT, target_id TEXT, relation TEXT);")

    def ins(i, typ, claim, cur=1, meta=None, **kw):
        row = dict(id=i, type=typ, claim=claim, logical_chain=kw.get("lc"), quoted_text=kw.get("q"),
                   interpretation=kw.get("interp"), quote_type=kw.get("qt"), evidence_id=kw.get("ev"),
                   is_current=cur, metadata=json.dumps(meta or {}), source_url=kw.get("url"),
                   source_title=kw.get("title"), source_domain=kw.get("dom"), source_type=kw.get("st"),
                   confidence=float(CONF), confidence_history=f"[{CONF}]", importance_base=float(IMPORTANCE),
                   importance_score=float(IMPORTANCE), recall_count=7, utility_score=float(UTIL))
        c.execute(f"INSERT INTO nodes VALUES ({','.join('?' * len(row))})", list(row.values()))

    ins("ev_0001", "evidence", "ev", title="A Title", url="https://example.org/a", dom="example.org", st="web")
    n = 0
    for rt, k in der.items():
        for j in range(k):
            n += 1
            ins(f"dv_{n:04d}", "derivation", f"{claim_prefix} {rt} {j}", meta={"reasoning_type": rt},
                lc=f"chain for {n}")
    for j in range(untyped):
        n += 1
        ins(f"dv_{n:04d}", "derivation", f"{claim_prefix} untyped {j}", meta={})
    m = 0
    for qt, k in obs.items():
        for j in range(k):
            m += 1
            ins(f"ob_{m:04d}", "observation_factual", f"obs {qt} {j}", qt=qt, ev="ev_0001",
                q=f"quote {m}", interp=f"interp {m}", meta={"source_class": "web"})
    for j in range(predictive):
        m += 1
        ins(f"ob_{m:04d}", "observation_predictive", f"pred {j}", qt="editorial")
    # a non-current derivation and linked nodes for the first derivation
    ins("dv_9999", "derivation", "old superseded", cur=0, meta={"reasoning_type": "inductive_analogy"})
    ins("df_0001", "definition", "a definition text")
    for tgt, rel in [("ob_0001", "derives_from"), ("dv_9999", "acknowledged_derives_from"),
                     ("df_0001", "cites"), ("df_0001", "about"), ("dv_9999", "supersedes")]:
        c.execute("INSERT INTO edges(source_id,target_id,relation) VALUES ('dv_0001',?,?)", (tgt, rel))
    c.commit()
    c.close()
    return path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(tmp, db, seed=SEED, controls=None, draw_only=False, out="out", drawn="drawn_ids.json",
        expect=None):
    ctl = Path(tmp) / "controls.json"
    if controls is not None:
        ctl.write_text(json.dumps(controls))
    outdir = Path(out) if Path(out).is_absolute() else Path(tmp) / out
    argv = ["--db", str(db), "--seed", seed, "--out", str(outdir), "--controls", str(ctl),
            "--drawn-ids", str(Path(tmp) / drawn), "--expect-sha256", expect or sha(db)]
    if draw_only:
        argv.append("--draw-only")
    bp.main(argv)
    return outdir, Path(tmp) / drawn


@pytest.fixture()
def db(tmp_path):
    return make_db(tmp_path / "full.db")


NO_CONTROLS = {"known_loose": {}, "known_tight_placement_verified": {}}


def ids_in_packet(text):
    return re.findall(r"^## Node \d+ of \d+: (\S+)$", text, flags=re.M)


# ---------------------------------------------------------------- cell 1
def test_1_strata_counts_exact(tmp_path, db):
    _, drawn = run(tmp_path, db, controls=NO_CONTROLS, draw_only=True)
    d = json.loads(drawn.read_text())
    alloc = d["allocation"]
    # IG: 50 of 60
    assert alloc["derivation:inductive_generalization"] == 50
    # other types, total 90 over pops 200/30/3/1 (=234):
    # exact 76.92/11.54/1.15/0.38 -> largest remainder 77/12/1/0 -> floor 2 on the 3-node type
    # (sum 91) -> 1 excess taken from the LARGEST stratum (77 -> 76). The 1-node type has no floor.
    assert alloc["derivation:abductive_best_explanation"] == 76
    assert alloc["derivation:inductive_analogy"] == 12
    assert alloc["derivation:deductive_modus_ponens"] == 2
    assert alloc["derivation:authority_expert"] == 0
    assert sum(v for k, v in alloc.items() if k.startswith("derivation:") and "inductive_generalization" not in k) == 90
    # observations, 60 over 100/3/1: exact 57.69/1.73/0.58 -> LR 58/2/0
    assert alloc["observation:hard_data"] == 58
    assert alloc["observation:editorial"] == 2
    assert alloc["observation:personal_communication"] == 0
    # and the ids drawn match the allocation, all from the right stratum
    for k, v in alloc.items():
        assert len(d["sampled"][k]) == v
    assert sum(len(v) for v in d["sampled"].values()) == 200
    # NULL-type derivations are a census line, never sampled
    assert "untyped" not in json.dumps(d["sampled"])


def test_1b_allocate_cap_and_deficit():
    # cap: a stratum can never exceed its population; deficit is redistributed
    assert bp.allocate({"a": 1, "b": 2}, 10) == {"a": 1, "b": 2}
    assert bp.allocate({"a": 5, "b": 5}, 4) == {"a": 2, "b": 2}
    assert sum(bp.allocate({"a": 100, "b": 100, "c": 2}, 90).values()) == 90
    assert bp.allocate({"a": 100, "b": 100, "c": 2}, 90)["c"] == 2  # floor


def test_1c_census_lines(tmp_path):
    db = make_db(tmp_path / "c.db", untyped=2, predictive=3)
    _, drawn = run(tmp_path, db, controls=NO_CONTROLS, draw_only=True)
    cen = json.loads(drawn.read_text())["census"]
    assert cen["derivation_current"] == 60 + 200 + 30 + 3 + 1 + 2
    assert cen["derivation_null_type"] == 2
    assert cen["observation_predictive"] == 3
    assert cen["derivation_by_type"]["inductive_generalization"] == 60
    assert cen["observation_factual_by_quote_type"]["hard_data"] == 100


# ---------------------------------------------------------------- cell 2
def test_2_determinism(tmp_path, db):
    _, d1 = run(tmp_path, db, controls=NO_CONTROLS, draw_only=True, drawn="a.json")
    _, d2 = run(tmp_path, db, controls=NO_CONTROLS, draw_only=True, drawn="b.json")
    assert d1.read_bytes() == d2.read_bytes()
    _, d3 = run(tmp_path, db, seed="other-seed", controls=NO_CONTROLS, draw_only=True, drawn="c.json")
    assert json.loads(d1.read_text())["sampled"] != json.loads(d3.read_text())["sampled"]


# ---------------------------------------------------------------- cell 3
def test_3_controls_excluded_and_in_both_packets(tmp_path, db):
    # five IG derivations + one observation as controls; sweep seeds so a missing exclusion
    # cannot hide behind the luck of one draw (50 of 60 IG would draw a given node 5/6 of the time)
    ctl = {"known_loose": {"dv_0001": "n1", "dv_0002": "n2", "dv_0003": "n3"},
           "known_tight_placement_verified": {"dv_0004": "n4", "dv_0005": "n5"},
           "known_tight_final": ["ob_0001"]}
    cids = {"dv_0001", "dv_0002", "dv_0003", "dv_0004", "dv_0005", "ob_0001"}
    for seed in ["s1", "s2", "s3", "s4", "s5", "s6"]:
        _, drawn = run(tmp_path, db, seed=seed, controls=ctl, draw_only=True, drawn=f"{seed}.json")
        d = json.loads(drawn.read_text())
        sampled = {i for v in d["sampled"].values() for i in v}
        assert not (sampled & cids), seed
    out, _ = run(tmp_path, db, seed="s1", controls=ctl)
    mira = ids_in_packet((out / "packet_mira.md").read_text())
    zeph = ids_in_packet((out / "packet_zephyr.md").read_text())
    assert cids <= set(mira) and cids <= set(zeph)
    assert len(mira) == 200 + 6 and len(zeph) == 50 + 6
    assert len(set(mira)) == len(mira)
    # indistinguishable: no packet text marks a control
    for name in ("packet_mira.md", "packet_zephyr.md", "verdict_template.jsonl"):
        assert "control" not in (out / name).read_text().lower()
    # the control notes are never written anywhere
    for p in list(out.iterdir()) + [tmp_path / "s1.json"]:
        assert not re.search(r"\bn[1-5]\b", p.read_text()) or p.name.startswith("packet_")


def test_3b_control_missing_from_db_is_refused(tmp_path, db):
    ctl = {"known_loose": {"dv_NOPE": "x"}, "known_tight_placement_verified": {}}
    with pytest.raises(bp.AuditError, match="control"):
        run(tmp_path, db, controls=ctl, draw_only=True)


# ---------------------------------------------------------------- cell 4
def test_4_no_confidence_or_numeric_field_in_packet(tmp_path, db):
    out, _ = run(tmp_path, db, controls={"known_loose": {"dv_0001": "x"},
                                         "known_tight_placement_verified": {"ob_0002": "y"}})
    for name in ("packet_mira.md", "packet_zephyr.md", "verdict_template.jsonl", "TYPE_TABLE.md"):
        text = (out / name).read_text()
        for needle in (CONF, UTIL, IMPORTANCE):
            assert needle not in text, (name, needle)
        assert not re.search(r"(confidence|importance|recall_|utility)", text, flags=re.I), name


def test_4b_assertion_fires_on_forbidden_key_or_number():
    with pytest.raises(bp.AuditError):
        bp.assert_packet_clean([{"id": "x", "confidence": "0.5"}])
    with pytest.raises(bp.AuditError):
        bp.assert_packet_clean([{"id": "x", "links": [{"id": "y", "importance_score": "1"}]}])
    with pytest.raises(bp.AuditError):
        bp.assert_packet_clean([{"id": "x", "claim": 0.9}])
    bp.assert_packet_clean([{"id": "x", "claim": "talks about confidence in prose", "links": []}])


# ---------------------------------------------------------------- cell 5
def test_5_out_inside_worktree_refused(tmp_path, db):
    with pytest.raises(bp.AuditError, match="worktree"):
        run(tmp_path, db, controls=NO_CONTROLS, draw_only=True, out=str(REPO / "studies" / "node-audit" / "pk"))
    with pytest.raises(bp.AuditError, match="worktree"):
        run(tmp_path, db, controls=NO_CONTROLS, out=str(REPO / "pk"))
    assert not (REPO / "pk").exists()


# ---------------------------------------------------------------- cell 6
def test_6_stripped_db_refused(tmp_path):
    db = make_db(tmp_path / "stripped.db")
    c = sqlite3.connect(db)
    c.execute("UPDATE nodes SET claim='' WHERE type='derivation'")
    c.commit()
    c.close()
    with pytest.raises(bp.StrippedSnapshotError):
        run(tmp_path, db, controls=NO_CONTROLS, draw_only=True)


# ---------------------------------------------------------------- cell 7
def test_7_zephyr_subset_with_25_ig(tmp_path, db):
    ctl = {"known_loose": {"dv_0001": "x"}, "known_tight_placement_verified": {}}
    out, drawn = run(tmp_path, db, controls=ctl)
    d = json.loads(drawn.read_text())
    z = d["zephyr"]
    assert len(z) == 50 and len(set(z)) == 50
    ig = set(d["sampled"]["derivation:inductive_generalization"])
    assert len(set(z) & ig) == 25
    mira = set(ids_in_packet((out / "packet_mira.md").read_text()))
    zeph = set(ids_in_packet((out / "packet_zephyr.md").read_text()))
    assert set(z) <= mira
    assert zeph - {"dv_0001"} == set(z)
    # the 25 others come from the remaining 150 drawn, never from the IG 50
    rest = {i for k, v in d["sampled"].items() if "inductive_generalization" not in k for i in v}
    assert len(set(z) & rest) == 25


# ---------------------------------------------------------------- cell 8
def test_8_drawn_ids_has_no_control_id(tmp_path, db):
    ctl = {"known_loose": {"dv_0001": "x"}, "known_tight_placement_verified": {"ob_0005": "y"},
           "known_tight_final": ["dv_0262"]}
    _, drawn = run(tmp_path, db, controls=ctl, draw_only=True)
    text = drawn.read_text()
    for cid in ("dv_0001", "ob_0005", "dv_0262"):
        assert f'"{cid}"' not in text and cid not in text
    # and draw-only writes only the drawn file
    assert not (tmp_path / "out").exists()


# ---------------------------------------------------------------- extras
def test_9_hash_mismatch_refused(tmp_path, db):
    with pytest.raises(bp.AuditError, match="sha256"):
        run(tmp_path, db, controls=NO_CONTROLS, draw_only=True, expect="0" * 64)


def test_10_packet_content(tmp_path, db):
    out, _ = run(tmp_path, db, controls={"known_loose": {"dv_0001": "x"}, "known_tight_placement_verified": {},
                                         "known_tight_final": ["ob_0001"]})
    text = (out / "packet_mira.md").read_text()
    # type table verbatim at top
    table = (out / "TYPE_TABLE.md").read_text()
    assert "inductive_generalization: Observed X in A,B,C" in table and "deductive_conjunction" not in table
    assert table.strip() in text and text.index(table.strip()) < text.index("## Node 1 of")
    # dv_0001 carries relation-labelled links; supersedes omitted; acknowledged labelled
    sec = text.split("## Node ", 1)
    node = [s for s in text.split("\n## Node ") if ": dv_0001\n" in s][0]
    assert "acknowledged_derives_from" in node and "premise" in node and "context" in node
    assert "old superseded" in node and "a definition text" in node and "about" in node
    assert "supersedes" not in node
    # observation carries source identity
    onode = [s for s in text.split("\n## Node ") if ": ob_0002\n" in s][0]
    assert "A Title" in onode and "https://example.org/a" in onode and "example.org" in onode
    # template: one line per packet node, in order, all check fields null
    lines = [json.loads(x) for x in (out / "verdict_template.jsonl").read_text().splitlines()]
    assert [x["id"] for x in lines] == ids_in_packet(text)
    d = [x for x in lines if x["id"] == "dv_0001"][0]
    assert set(d["checks"]) == {"type", "placement", "chain-overreach"}
    assert d["checks"]["type"] == {"verdict": None, "reason": None, "proposed_type": None}
    assert d["checks"]["placement"] == {"verdict": None, "reason": None}
    o = [x for x in lines if x["id"] == "ob_0002"][0]
    assert set(o["checks"]) == {"support-overreach", "quote_type", "source_class"}
