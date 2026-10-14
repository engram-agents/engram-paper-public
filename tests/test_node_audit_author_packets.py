"""Contract tests for the `--author-arm` mode of `studies/node-audit/build_packet.py`
(Amendment 4, Arm A). Written BEFORE the implementation (contract-first). Synthetic data only.

  A1 no control id is ever a JUDGED node (heading or template row id): AuthorPacketLeak, every occurrence listed
  A1b any other mention of a control (premise link, claim text) is recorded per sampled id in
     author_arm_manifest.json; the build proceeds and nothing is redacted
  A2 declared type withheld in the blind packet (and no reasoning_type key in its template)
  A3 blind set = the derivations among the sampled, in Mira's filtered order
  A4 verdict packet = the 200 sampled, each block equal to its block in packet_mira.md
     (heading aside), in Mira's order with the controls removed
  A5 confidence withheld (same forbidden-key assertion)
  A6 deterministic: same inputs, byte-identical files
  A7 only the six author files are written; default-mode output (the five --out files and
     drawn_ids.json) is byte-unchanged (golden hashes taken from the UNMODIFIED code on the same
     synthetic fixture)
  Attribution is from known structure (per-node blocks), never from re-parsing rendered headings
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sqlite3
from pathlib import Path

import pytest

from tests.test_node_audit_sampler import (CONF, IMPORTANCE, UTIL, bp, ids_in_packet, make_db, sha)

SEED = "author-seed"
# not linked from anything in the fixture (dv_0001 links ob_0001, dv_9999, df_0001)
CTL = {"known_loose": {"dv_0002": "n", "dv_0003": "n"}, "known_tight_placement_verified": {"ob_0002": "n"},
       "known_tight_final": ["dv_0004"]}
CTL_IDS = {"dv_0002", "dv_0003", "ob_0002", "dv_0004"}
AUTHOR_FILES = {"packet_author_blind.md", "blind_template.jsonl", "packet_author_verdict.md",
                "verdict_template_author.jsonl", "TYPE_TABLE.md", "author_arm_manifest.json"}


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


# drawn_ids.json is also a default-mode output (written outside --out). Its golden is taken from the
# same pre-change code (5257134) on the same fixture. It embeds the fixture DB's own file hash, which
# depends on the sqlite library version, so that one value is masked before hashing and checked apart.
GOLDEN_DRAWN_IDS = "b4ebf9fc8ab9657344ccc2078156864a69ea3961ba5ec03bb2dcb6796adad6d6"


def test_a7_default_mode_byte_unchanged(tmp_path, db):
    out, drawn = run(tmp_path, db, seed="gold-seed", author=False)
    assert {p.name for p in out.iterdir()} == set(GOLDEN)
    for name, want in GOLDEN.items():
        assert hashlib.sha256((out / name).read_bytes()).hexdigest() == want, name
    text = drawn.read_text()
    assert f'"snapshot_sha256": "{sha(db)}"' in text
    masked = re.sub(r'"snapshot_sha256": "[0-9a-f]{64}"', '"snapshot_sha256": "<db>"', text)
    assert hashlib.sha256(masked.encode()).hexdigest() == GOLDEN_DRAWN_IDS, "drawn_ids.json"


# ---------------------------------------------------------------- A1
def _mention_db(tmp_path):
    """Every node sampled; ob_0001 is a control, a premise of dv_0001, and also linked from dv_0002."""
    small = make_db(tmp_path / "small.db", der={"inductive_generalization": 3}, obs={"hard_data": 3})
    c = sqlite3.connect(small)
    c.execute("INSERT INTO edges(source_id,target_id,relation) VALUES ('dv_0002','ob_0001','derives_from')")
    c.commit()
    c.close()
    return small


MENTION_CTL = {"known_loose": {"ob_0001": "n"}, "known_tight_placement_verified": {}}


def test_a1_no_control_is_a_judged_node_in_the_normal_build(tmp_path, db):
    out, _ = run(tmp_path, db)
    for name in ("packet_author_blind.md", "packet_author_verdict.md"):
        assert not set(ids_in_packet((out / name).read_text())) & CTL_IDS, name
    for name in ("blind_template.jsonl", "verdict_template_author.jsonl"):
        ids = {json.loads(x)["id"] for x in (out / name).read_text().splitlines()}
        assert not ids & CTL_IDS, name


def test_a1_control_as_judged_node_refuses_and_lists_every_occurrence(tmp_path):
    small = make_db(tmp_path / "small.db", der={"inductive_generalization": 3}, obs={"hard_data": 3})
    con = bp.open_ro(small)
    sampled = ["dv_0001", "dv_0002", "dv_0003", "ob_0001", "ob_0002"]
    out = tmp_path / "out"
    with pytest.raises(bp.AuthorPacketLeak) as ei:
        bp.write_author_packets(con, SEED, sampled, ["dv_0002", "ob_0001"], out)
    msg = str(ei.value)
    assert isinstance(ei.value, bp.AuditError)
    for where in ("packet_author_blind.md", "packet_author_verdict.md", "blind_template.jsonl",
                  "verdict_template_author.jsonl"):
        assert re.search(rf"{where}:\d+: dv_0002", msg), where
    assert re.search(r"packet_author_verdict.md:\d+: ob_0001", msg)
    assert re.search(r"verdict_template_author.jsonl:\d+: ob_0001", msg)
    assert not out.exists() or not any(out.iterdir())  # nothing written


def test_a1b_link_to_control_builds_and_is_in_manifest_under_the_right_sampled_id(tmp_path):
    small = _mention_db(tmp_path)
    out, _ = run(tmp_path, small, controls=MENTION_CTL)
    man = json.loads((out / "author_arm_manifest.json").read_text())
    assert man == {"control_mentions": {"dv_0001": ["ob_0001"], "dv_0002": ["ob_0001"]},
                   "n_sampled_nodes_mentioning_a_control": 2}
    v = (out / "packet_author_verdict.md").read_text()
    assert "ob_0001" in v  # mention stays in the text, unredacted
    assert "ob_0001" not in ids_in_packet(v)  # and the control is still not a judged node


def test_a1b_mention_in_claim_text_attributed_to_the_containing_node(tmp_path):
    small = make_db(tmp_path / "small.db", der={"inductive_generalization": 3}, obs={"hard_data": 3})
    c = sqlite3.connect(small)
    c.execute("UPDATE nodes SET claim = claim || ' (see also ob_0001 here)' WHERE id='dv_0003'")
    c.commit()
    c.close()
    out, _ = run(tmp_path, small, controls=MENTION_CTL)
    man = json.loads((out / "author_arm_manifest.json").read_text())
    assert man["control_mentions"] == {"dv_0001": ["ob_0001"], "dv_0003": ["ob_0001"]}
    assert man["n_sampled_nodes_mentioning_a_control"] == 2


def test_a1b_manifest_with_no_mentions_is_empty_and_deterministic(tmp_path, db):
    a, _ = run(tmp_path, db, out="a")
    b, _ = run(tmp_path, db, out="b", drawn="b.json")
    assert json.loads((a / "author_arm_manifest.json").read_text()) == {
        "control_mentions": {}, "n_sampled_nodes_mentioning_a_control": 0}
    assert (a / "author_arm_manifest.json").read_bytes() == (b / "author_arm_manifest.json").read_bytes()


def test_a1_id_boundary_is_not_a_prefix_match(tmp_path):
    # control dv_0002 must not trip on a longer id such as dv_00021 or xdv_0002 appearing in text,
    # but must trip on a heading, a bare mention and a quoted one
    text = "dv_00021 xdv_0002\n### premise: dv_0002 (derivation)\nsee dv_0002.\n> 'dv_0002'"
    hits = bp.control_occurrences("f.md", text, ["dv_0002"])
    assert [(f, ln, cid) for f, ln, cid in hits] == [("f.md", 2, "dv_0002"), ("f.md", 3, "dv_0002"),
                                                      ("f.md", 4, "dv_0002")]
    # the docstring's exact rule: not preceded/followed by [A-Za-z0-9_]; "-" is a boundary; case-sensitive
    hits = bp.control_occurrences("f.md", "dv_0002-x\nDV_0002\ndv_0002_x\n_dv_0002", ["dv_0002"])
    assert hits == [("f.md", 1, "dv_0002")]


def _forged_db(tmp_path, title, domain="example.org", claim_mention=False):
    """3 IG derivations + 3 observations; ob_0002 gets its own evidence node whose source_title /
    source_domain (the unquoted render fields) carry the given text. ob_0003 is the control."""
    small = make_db(tmp_path / "forged.db", der={"inductive_generalization": 3}, obs={"hard_data": 3})
    c = sqlite3.connect(small)
    c.execute("INSERT INTO nodes(id,type,claim,is_current,metadata,source_url,source_title,source_domain,"
              "source_type) VALUES ('ev_0002','evidence','ev',1,'{}','https://example.org/b',?,?,'web')",
              (title, domain))
    c.execute("UPDATE nodes SET evidence_id='ev_0002' WHERE id='ob_0002'")
    if claim_mention:
        c.execute("UPDATE nodes SET claim = claim || ' (see ob_0003)' WHERE id='dv_0003'")
    c.commit()
    c.close()
    return small


FORGE_CTL = {"known_loose": {"ob_0003": "n"}, "known_tight_placement_verified": {}}


def test_a1_heading_shaped_field_cannot_forge_a_judged_node_refusal(tmp_path):
    # a source_title carrying a newline plus a heading naming the CONTROL: the build must not refuse,
    # and the mention is attributed to the observation whose field holds it
    small = _forged_db(tmp_path, "T\n## Node 1 of 9: ob_0003\nmentions ob_0003 here")
    out, _ = run(tmp_path, small, controls=FORGE_CTL)
    man = json.loads((out / "author_arm_manifest.json").read_text())
    assert man == {"control_mentions": {"ob_0002": ["ob_0003"]}, "n_sampled_nodes_mentioning_a_control": 1}
    tpl = {json.loads(x)["id"] for x in (out / "verdict_template_author.jsonl").read_text().splitlines()}
    assert "ob_0003" not in tpl


def test_a1b_heading_shaped_field_naming_another_sampled_id_does_not_move_mentions(tmp_path):
    # the forged heading names a different SAMPLED node (ob_0001); a later mention in the same block
    # (source_domain) and a genuine mention in another node must stay attributed to their own nodes
    small = _forged_db(tmp_path, "T\n## Node 1 of 9: ob_0001", domain="ob_0003.example.org ob_0003",
                       claim_mention=True)
    out, _ = run(tmp_path, small, controls=FORGE_CTL)
    man = json.loads((out / "author_arm_manifest.json").read_text())
    assert man["control_mentions"] == {"dv_0003": ["ob_0003"], "ob_0002": ["ob_0003"]}
    assert man["n_sampled_nodes_mentioning_a_control"] == 2


def test_a1_judged_control_line_numbers_point_at_its_own_heading(tmp_path):
    small = make_db(tmp_path / "small.db", der={"inductive_generalization": 3}, obs={"hard_data": 3})
    con = bp.open_ro(small)
    with pytest.raises(bp.AuthorPacketLeak) as ei:
        bp.write_author_packets(con, SEED, ["dv_0001", "dv_0002", "ob_0001"], ["dv_0002"], tmp_path / "o")
    msg = str(ei.value)
    # rebuild the verdict packet without the control to learn what a block looks like, then locate the
    # control's block in a build that includes it: its reported heading line must hold its heading
    nodes = {i: bp.build_node(con, i) for i in ("dv_0001", "dv_0002", "ob_0001")}
    order = sorted(nodes)
    random.Random(f"{SEED}:order:mira").shuffle(order)
    text = bp.HEADER + bp.TYPE_TABLE_MD + "\n" + "\n".join(
        bp.render_node(k + 1, 3, nodes[i]) for k, i in enumerate(order))
    lines = text.split("\n")
    reported = [int(m.group(1)) for m in re.finditer(r"packet_author_verdict.md:(\d+): dv_0002", msg)]
    assert reported
    heading = next(n for n, ln in enumerate(lines, 1) if re.match(r"## Node \d+ of 3: dv_0002$", ln))
    assert heading in reported
    assert all("dv_0002" in lines[n - 1] for n in reported)


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


def test_a2_runtime_guard_refuses_when_the_blind_render_emits_the_declared_line(tmp_path, db, monkeypatch):
    real = bp.render_node
    monkeypatch.setattr(bp, "render_node", lambda i, n, node, blind=False: real(i, n, node))  # ignores blind
    with pytest.raises(bp.AuditError, match="declared reasoning_type reached the blind packet"):
        run(tmp_path, db)
    out = tmp_path / "out"
    assert not out.exists() or not any(out.iterdir())  # nothing written


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
