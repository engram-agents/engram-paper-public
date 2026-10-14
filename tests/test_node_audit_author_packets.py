"""Contract tests for the `--author-arm` mode of `studies/node-audit/build_packet.py`
(Amendment 4, Arm A). Written BEFORE the implementation (contract-first). Synthetic data only.

  A1 no control id anywhere in any author-mode output file; a sampled node that links to a
     control makes the build REFUSE with AuthorPacketLeak listing every occurrence
  A2 declared type withheld in the blind packet (and no reasoning_type key in its template)
  A3 blind set = the derivations among the sampled, in Mira's filtered order
  A4 verdict packet = the 200 sampled, each block equal to its block in packet_mira.md
     (heading aside), in Mira's order with the controls removed
  A5 confidence withheld (same forbidden-key assertion)
  A6 deterministic: same inputs, byte-identical files
  A7 only the five author files are written; default-mode output is byte-unchanged
     (golden hashes taken from the UNMODIFIED code on the same synthetic fixture)
"""
from __future__ import annotations

import hashlib
import json
import random
import re
from pathlib import Path

import pytest

from tests.test_node_audit_sampler import (CONF, IMPORTANCE, UTIL, bp, ids_in_packet, make_db, sha)

SEED = "author-seed"
# not linked from anything in the fixture (dv_0001 links ob_0001, dv_9999, df_0001)
CTL = {"known_loose": {"dv_0002": "n", "dv_0003": "n"}, "known_tight_placement_verified": {"ob_0002": "n"},
       "known_tight_final": ["dv_0004"]}
CTL_IDS = {"dv_0002", "dv_0003", "ob_0002", "dv_0004"}
AUTHOR_FILES = {"packet_author_blind.md", "blind_template.jsonl", "packet_author_verdict.md",
                "verdict_template_author.jsonl", "TYPE_TABLE.md"}


def run(tmp, db, controls=CTL, seed=SEED, author=True, out="out", drawn="drawn_ids.json"):
    ctl = Path(tmp) / "controls.json"
    ctl.write_text(json.dumps(controls))
    outdir = Path(tmp) / out
    argv = ["--db", str(db), "--seed", seed, "--out", str(outdir), "--controls", str(ctl),
            "--drawn-ids", str(Path(tmp) / drawn), "--expect-sha256", sha(db)]
    if author:
        argv.append("--author-arm")
    bp.main(argv)
    return outdir, Path(tmp) / drawn


@pytest.fixture()
def db(tmp_path):
    return make_db(tmp_path / "full.db")


def blocks(text):
    """node id -> block text with the `## Node i of n: ` heading's numbering removed."""
    parts = re.split(r"(?m)^(?=## Node \d+ of \d+: )", text)
    res = {}
    for p in parts:
        m = re.match(r"## Node \d+ of \d+: (\S+)\n", p)
        if m:
            res[m.group(1)] = p[m.end():]
    return res


def mira_order(sampled, controls, seed=SEED):
    order = sorted(set(sampled) | set(controls))
    random.Random(f"{seed}:order:mira").shuffle(order)
    return [i for i in order if i in set(sampled)]


# ---------------------------------------------------------------- A7
def test_a7_only_author_files_written(tmp_path, db):
    out, _ = run(tmp_path, db)
    assert {p.name for p in out.iterdir()} == AUTHOR_FILES


# golden sha256s of the DEFAULT-mode outputs, taken from the unmodified build_packet.py
# (seed "gold-seed", the make_db fixture, controls dv_0002/dv_0003/ob_0002/dv_0004)
GOLDEN = {
    "TYPE_TABLE.md": "c6f7e94d03779b57952931f41215ca5b8ee55a996b258c5bd9b7ad4685f54aaf",
    "packet_mira.md": "06b7c6f4e311ffec09b365ec702cffa5ae843cd2de094e0ea413499da987b895",
    "packet_zephyr.md": "991ea1e2860bc68d19ed7d5b5d91d3fabf3f79f6ea4b1c88d93fe45dfaf9071e",
    "verdict_template.jsonl": "d2291fe521a138d424c7439af94c96cd59e80468bb528f1f721fe1d3bcbefa15",
    "verdict_template_zephyr.jsonl": "21678c46e7a3fc9ea7cc764b162bd2b99d875f550a829856176106237eec6d07",
}


def test_a7_default_mode_byte_unchanged(tmp_path, db):
    out, _ = run(tmp_path, db, seed="gold-seed", author=False)
    assert {p.name for p in out.iterdir()} == set(GOLDEN)
    for name, want in GOLDEN.items():
        assert hashlib.sha256((out / name).read_bytes()).hexdigest() == want, name


# ---------------------------------------------------------------- A1
def test_a1_no_control_id_in_any_author_file(tmp_path, db):
    out, _ = run(tmp_path, db)
    for p in out.iterdir():
        text = p.read_text()
        for cid in CTL_IDS:
            assert not re.search(rf"(?<![A-Za-z0-9_]){cid}(?![A-Za-z0-9_])", text), (p.name, cid)


def test_a1_link_to_control_refuses_with_named_error(tmp_path):
    # tiny population: every node is sampled, so dv_0001 is sampled and its premise ob_0001 is a control
    small = make_db(tmp_path / "small.db", der={"inductive_generalization": 3}, obs={"hard_data": 3})
    ctl = {"known_loose": {"ob_0001": "n"}, "known_tight_placement_verified": {}}
    with pytest.raises(bp.AuthorPacketLeak) as ei:
        run(tmp_path, small, controls=ctl)
    msg = str(ei.value)
    assert "ob_0001" in msg and "packet_author_blind.md" in msg and "packet_author_verdict.md" in msg
    assert isinstance(ei.value, bp.AuditError)
    # refused before writing any author packet
    assert not (tmp_path / "out" / "packet_author_verdict.md").exists()
    assert not (tmp_path / "out" / "packet_author_blind.md").exists()


def test_a1_leak_lists_every_occurrence(tmp_path):
    small = make_db(tmp_path / "small.db", der={"inductive_generalization": 3}, obs={"hard_data": 3})
    c = __import__("sqlite3").connect(small)
    c.execute("INSERT INTO edges(source_id,target_id,relation) VALUES ('dv_0002','ob_0001','derives_from')")
    c.commit()
    c.close()
    ctl = {"known_loose": {"ob_0001": "n"}, "known_tight_placement_verified": {}}
    with pytest.raises(bp.AuthorPacketLeak) as ei:
        run(tmp_path, small, controls=ctl)
    # two sampled derivations link it; blind + verdict file each -> 4 occurrences
    assert str(ei.value).count("ob_0001") >= 4


def test_a1_id_boundary_is_not_a_prefix_match(tmp_path):
    # control dv_0002 must not trip on a longer id such as dv_00021 or xdv_0002 appearing in text,
    # but must trip on a heading, a bare mention and a quoted one
    text = "dv_00021 xdv_0002\n### premise: dv_0002 (derivation)\nsee dv_0002.\n> 'dv_0002'"
    hits = bp.control_occurrences("f.md", text, ["dv_0002"])
    assert [(f, ln, cid) for f, ln, cid in hits] == [("f.md", 2, "dv_0002"), ("f.md", 3, "dv_0002"),
                                                      ("f.md", 4, "dv_0002")]


# ---------------------------------------------------------------- A2 / A3
def test_a2_declared_type_withheld(tmp_path, db):
    out, _ = run(tmp_path, db)
    blind = (out / "packet_author_blind.md").read_text()
    assert not any(ln.startswith("- declared reasoning_type:") for ln in blind.splitlines())
    assert "declared reasoning_type" not in blind
    assert "reasoning_type" not in (out / "blind_template.jsonl").read_text()
    for ln in (out / "blind_template.jsonl").read_text().splitlines():
        assert json.loads(ln).keys() == {"id", "blind_type", "reason"}
    assert bp.TYPE_TABLE_MD in blind  # the table is shown
    assert "declared type is withheld" in blind


def test_a2_blind_block_is_render_node_minus_declared_line(tmp_path, db):
    out, _ = run(tmp_path, db)
    con = bp.open_ro(db)
    blind = (out / "packet_author_blind.md").read_text()
    got = blocks(blind)
    n = len(got)
    for k, nid in enumerate(ids_in_packet(blind)):
        full = bp.render_node(k + 1, n, bp.build_node(con, nid))
        want = re.sub(r"- declared reasoning_type: .*\n\n", "", full, count=1)
        assert want != full
        assert blocks(want)[nid].rstrip("\n") == got[nid].rstrip("\n")


def test_a3_blind_set_is_sampled_derivations_in_mira_order(tmp_path, db):
    out, drawn = run(tmp_path, db)
    d = json.loads(drawn.read_text())
    sampled = [i for v in d["sampled"].values() for i in v]
    ders = {i for i in sampled if i.startswith("dv_")}
    ids = ids_in_packet((out / "packet_author_blind.md").read_text())
    assert len(ids) == len(set(ids)) == len(ders) == 140
    assert set(ids) == ders
    assert not (set(ids) & CTL_IDS) and not any(i.startswith("ob_") for i in ids)
    assert ids == [i for i in mira_order(sampled, CTL_IDS) if i in ders]
    tpl = [json.loads(x) for x in (out / "blind_template.jsonl").read_text().splitlines()]
    assert tpl == [{"id": i, "blind_type": None, "reason": None} for i in ids]
    assert f"of {len(ids)}:" in (out / "packet_author_blind.md").read_text()


# ---------------------------------------------------------------- A4
def test_a4_verdict_parity_with_mira_packet(tmp_path, db):
    a_out, drawn = run(tmp_path, db, out="a")
    m_out, _ = run(tmp_path, db, author=False, out="m", drawn="m.json")
    d = json.loads(drawn.read_text())
    sampled = [i for v in d["sampled"].values() for i in v]
    av = (a_out / "packet_author_verdict.md").read_text()
    ids = ids_in_packet(av)
    assert len(ids) == 200 and set(ids) == set(sampled) and not (set(ids) & CTL_IDS)
    assert ids == mira_order(sampled, CTL_IDS)
    mira = blocks((m_out / "packet_mira.md").read_text())
    ab = blocks(av)
    for i in ids:
        assert ab[i] == mira[i], i
    assert all(f" of 200: " in ln for ln in re.findall(r"(?m)^## Node .*$", av))
    assert av.startswith(bp.HEADER + bp.TYPE_TABLE_MD)
    tpl = (a_out / "verdict_template_author.jsonl").read_text().splitlines()
    con = bp.open_ro(db)
    assert tpl == [bp.template_line(bp.build_node(con, i)) for i in ids]
    assert (a_out / "TYPE_TABLE.md").read_text() == bp.TYPE_TABLE_MD


# ---------------------------------------------------------------- A5
def test_a5_confidence_withheld(tmp_path, db):
    out, _ = run(tmp_path, db)
    for p in out.iterdir():
        text = p.read_text()
        for needle in (CONF, UTIL, IMPORTANCE):
            assert needle not in text, (p.name, needle)
        assert not re.search(r"(confidence|importance|recall_|utility)", text, flags=re.I), p.name


def test_a5_forbidden_key_check_runs_in_author_mode(tmp_path, db, monkeypatch):
    seen = []
    real = bp.assert_packet_clean
    monkeypatch.setattr(bp, "assert_packet_clean", lambda o, *a: (None if a else seen.append(len(o)), real(o, *a))[1])
    run(tmp_path, db)
    assert seen and seen[0] >= 200


# ---------------------------------------------------------------- A6
def test_a6_deterministic(tmp_path, db):
    a, _ = run(tmp_path, db, out="a")
    b, _ = run(tmp_path, db, out="b", drawn="b.json")
    assert {p.name for p in a.iterdir()} == {p.name for p in b.iterdir()}
    for p in a.iterdir():
        assert p.read_bytes() == (b / p.name).read_bytes(), p.name


# ---------------------------------------------------------------- misc
def test_out_inside_worktree_refused_in_author_mode(tmp_path, db):
    from tests.test_node_audit_sampler import REPO
    ctl = tmp_path / "controls.json"
    ctl.write_text(json.dumps(CTL))
    with pytest.raises(bp.AuditError, match="worktree"):
        bp.main(["--db", str(db), "--seed", SEED, "--out", str(REPO / "pk"), "--controls", str(ctl),
                 "--drawn-ids", str(tmp_path / "d.json"), "--expect-sha256", sha(db), "--author-arm"])
    assert not (REPO / "pk").exists()


def test_author_arm_with_draw_only_refused(tmp_path, db):
    ctl = tmp_path / "controls.json"
    ctl.write_text(json.dumps(CTL))
    with pytest.raises(bp.AuditError, match="draw-only"):
        bp.main(["--db", str(db), "--seed", SEED, "--out", str(tmp_path / "o"), "--controls", str(ctl),
                 "--drawn-ids", str(tmp_path / "d.json"), "--expect-sha256", sha(db), "--author-arm",
                 "--draw-only"])
