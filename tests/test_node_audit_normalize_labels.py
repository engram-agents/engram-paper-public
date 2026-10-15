"""Contract tests for `studies/node-audit/normalize_labels.py` (PROTOCOL.md Amendment 5: the
single pinned label normalization for one reader file).

Written BEFORE the implementation (contract-first). Clause numbers N1-N9 match the tool's module
docstring. SYNTHETIC data only: every input is built inside the test; no real verdict, packet,
snapshot or manifest is ever read, and no node content appears here.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "studies" / "node-audit" / "normalize_labels.py"


def _load():
    spec = importlib.util.spec_from_file_location("normalize_labels", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["normalize_labels"] = mod
    spec.loader.exec_module(mod)
    return mod


nl = _load()
an = nl.an  # the analyze module the tool actually imports

DERIV = ("type", "placement", "chain-overreach")
OBS = ("support-overreach", "quote_type", "source_class")


def _row(nid, verdicts, reasons=None, proposed=None):
    kind = DERIV if nid.startswith("dv_") else OBS
    checks = {}
    for name, v in zip(kind, verdicts):
        checks[name] = {"verdict": v, "reason": (reasons or {}).get(name, f"r-{name}")}
    if nid.startswith("dv_"):
        checks["type"]["proposed_type"] = proposed
    return {"id": nid, "checks": checks}


def _zephyr_rows(t=10, p=13, c=14):
    """14 derivation rows: row i is loose in chain if i<c, placement if i<p, type if i<t; the
    loose labels are written in the prefixed form. Plus two tight observation rows."""
    rows = []
    for i in range(14):
        vt = "loose:type" if i < t else "tight"
        vp = "loose:placement" if i < p else "tight"
        vc = "loose:chain-overreach" if i < c else "tight"
        rows.append(_row(f"dv_{i:04d}", (vt, vp, vc), proposed="some_type" if i < t else None))
    rows.append(_row("ob_0001", ("tight", "tight", "tight")))
    rows.append(_row("ob_0002", ("tight", "tight", "tight")))
    return rows


def _write(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return path


def _ids(rows):
    return [r["id"] for r in rows]


def _run(args):
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True)


def _cli(tmp_path, rows, reader="zephyr", name="in.jsonl"):
    src = _write(tmp_path / name, rows)
    out = tmp_path / "out.jsonl"
    r = _run(["--in", str(src), "--out", str(out), "--reader", reader])
    return r, src, out


def _normalized_expected(rows):
    exp = json.loads(json.dumps(rows))
    for r in exp:
        for c in r["checks"].values():
            if isinstance(c["verdict"], str) and c["verdict"].startswith("loose:"):
                c["verdict"] = "loose"
    return exp


# ---------------------------------------------------------------- N1 pinned expected delta
def test_n1_expected_delta_constant_is_pinned():
    assert nl.EXPECTED_DELTA == {"zephyr": {"type": 10, "placement": 13, "chain-overreach": 14}}


def test_n1_exact_delta_succeeds(tmp_path):
    r, _, out = _cli(tmp_path, _zephyr_rows())
    assert r.returncode == 0, r.stderr
    assert out.exists()


def test_n1_delta_9_13_14_refused_no_out(tmp_path):
    r, _, out = _cli(tmp_path, _zephyr_rows(t=9))
    assert r.returncode != 0
    assert not out.exists()
    assert "expected" in r.stderr and "actual" in r.stderr
    assert "type" in r.stderr and "10" in r.stderr and "9" in r.stderr


def test_n1_delta_too_many_refused(tmp_path):
    r, _, out = _cli(tmp_path, _zephyr_rows(p=14))
    assert r.returncode != 0 and not out.exists()


def test_n1_right_total_wrong_split_refused(tmp_path):
    # 37 changed cells, the pinned total, but split 13/10/14 instead of 10/13/14: the pin is per check.
    rows = _zephyr_rows(t=13, p=10, c=14)
    r, _, out = _cli(tmp_path, rows)
    assert sum(1 for x in rows for c in x["checks"].values() if c["verdict"].startswith("loose:")) == 37
    assert r.returncode != 0
    assert not out.exists()
    assert "type: expected 10, actual 13" in r.stderr
    assert "placement: expected 13, actual 10" in r.stderr
    assert "chain-overreach: expected 14, actual 14" in r.stderr  # the full table is shown
    assert "mismatch in ['type', 'placement']" in r.stderr


def test_n1_non_zephyr_with_a_single_loose_type_refused(tmp_path):
    rows = [_row("dv_0001", ("loose:type", "tight", "tight"), proposed="x")]
    r, _, out = _cli(tmp_path, rows, reader="mira")
    assert r.returncode != 0
    assert not out.exists()


def test_n1_zephyr_with_no_loose_labels_refused(tmp_path):
    r, _, out = _cli(tmp_path, [_row("dv_0001", ("tight", "tight", "tight"))], reader="zephyr")
    assert r.returncode != 0 and not out.exists()


def test_n1_unknown_reader_expects_empty_delta():
    assert nl.expected_delta_for("someone-else") == {}


# ---------------------------------------------------------------- N2 mapping
def test_n2_mismatched_prefix_refused_names_cell_no_out(tmp_path):
    rows = _zephyr_rows()
    rows[3]["checks"]["type"]["verdict"] = "loose:placement"
    r, _, out = _cli(tmp_path, rows)
    assert r.returncode != 0
    assert not out.exists()
    assert "dv_0003" in r.stderr and "type" in r.stderr and "loose:placement" in r.stderr


def test_n2_unknown_check_refused_no_out(tmp_path):
    rows = _zephyr_rows()
    rows[5]["checks"]["placement"]["verdict"] = "loose:typo"
    r, _, out = _cli(tmp_path, rows)
    assert r.returncode != 0
    assert not out.exists()
    assert "dv_0005" in r.stderr and "loose:typo" in r.stderr


def test_n2_known_check_of_other_kind_still_refused(tmp_path):
    # `loose:quote_type` is in ALL_CHECKS but is not the enclosing key -> mismatched prefix.
    rows = _zephyr_rows()
    rows[0]["checks"]["type"]["verdict"] = "loose:quote_type"
    r, _, out = _cli(tmp_path, rows)
    assert r.returncode != 0 and not out.exists()


def test_n2_reason_and_proposed_type_untouched(tmp_path):
    rows = _zephyr_rows()
    rows[0]["checks"]["type"]["reason"] = "says loose:type in prose, café"
    rows[0]["checks"]["type"]["proposed_type"] = "loose:type"  # not a verdict; must not change
    r, _, out = _cli(tmp_path, rows)
    assert r.returncode == 0, r.stderr
    got = [json.loads(x) for x in out.read_text().splitlines()]
    assert got[0]["checks"]["type"]["reason"] == "says loose:type in prose, café"
    assert got[0]["checks"]["type"]["proposed_type"] == "loose:type"
    assert got == _normalized_expected(rows)


def test_n2_other_values_unchanged_in_memory():
    rows = [
        _row("dv_0001", ("tight", "cannot-judge", "loose")),
        _row("ob_0001", ("loose:support-overreach", "tight", "tight")),
    ]
    lines = [(json.dumps(r) + "\n").encode() for r in rows]
    new_lines, counts, problems = nl.normalize_lines(lines)
    assert problems == []
    assert counts == {"support-overreach": 1}
    assert json.loads(new_lines[0]) == rows[0]
    assert json.loads(new_lines[1])["checks"]["support-overreach"]["verdict"] == "loose"


# ---------------------------------------------------------------- N3 refuse loudly, never partially
def test_n3_every_offender_named(tmp_path):
    rows = _zephyr_rows()
    rows[1]["checks"]["type"]["verdict"] = "loose:placement"
    rows[2]["checks"]["chain-overreach"]["verdict"] = "loose:typo"
    rows[4]["checks"]["placement"]["verdict"] = "loose:type"
    r, _, out = _cli(tmp_path, rows)
    assert r.returncode != 0 and not out.exists()
    for needle in ("dv_0001", "dv_0002", "dv_0004", "loose:placement", "loose:typo", "loose:type"):
        assert needle in r.stderr
    assert sorted(p.name for p in tmp_path.iterdir()) == ["in.jsonl"]  # no out, no temp file left


def test_n3_unparseable_line_refused(tmp_path):
    src = tmp_path / "in.jsonl"
    src.write_text(json.dumps(_zephyr_rows()[0]) + "\n{not json\n")
    out = tmp_path / "out.jsonl"
    r = _run(["--in", str(src), "--out", str(out), "--reader", "zephyr"])
    assert r.returncode != 0 and not out.exists()
    assert "line 2" in r.stderr


# ---------------------------------------------------------------- N4 byte fidelity
def test_n4_unchanged_lines_byte_for_byte_changed_reserialized(tmp_path):
    rows = _zephyr_rows()
    lines = []
    for i, r in enumerate(rows):
        s = json.dumps(r) if i % 2 else json.dumps(r, separators=(",", ":"))
        lines.append(s)
    # odd formatting on tight observation rows (never changed): spacing, escapes, CRLF
    lines[-2] = '{"id":"ob_0001",  "checks": ' + json.dumps(rows[-2]["checks"]) + "}"
    lines[-1] = json.dumps(rows[-1], ensure_ascii=True).replace('"r-source_class"', '"r-source_class\\u00e9"')
    ends = ["\n"] * len(lines)
    ends[-1] = "\r\n"
    src = tmp_path / "in.jsonl"
    src.write_bytes("".join(l + e for l, e in zip(lines, ends)).encode())
    out = tmp_path / "out.jsonl"
    r = _run(["--in", str(src), "--out", str(out), "--reader", "zephyr"])
    assert r.returncode == 0, r.stderr
    got = out.read_bytes().splitlines(keepends=True)
    orig = src.read_bytes().splitlines(keepends=True)
    assert len(got) == len(orig)
    for g, o, row in zip(got, orig, rows):
        changed = any(c["verdict"].startswith("loose:") for c in row["checks"].values())
        if not changed:
            assert g == o
        else:
            assert g.endswith(b"\n") and not g.endswith(b"\r\n")
            assert g == (json.dumps(json.loads(g), ensure_ascii=False) + "\n").encode()
    assert [json.loads(g) for g in got] == _normalized_expected([json.loads(o) for o in orig])
    assert _ids([json.loads(g) for g in got]) == _ids(rows)


def test_n4_changed_line_keeps_crlf(tmp_path):
    rows = _zephyr_rows()
    src = tmp_path / "in.jsonl"
    src.write_bytes("".join(json.dumps(r) + "\r\n" for r in rows).encode())
    out = tmp_path / "out.jsonl"
    assert _run(["--in", str(src), "--out", str(out), "--reader", "zephyr"]).returncode == 0
    assert all(l.endswith(b"\r\n") for l in out.read_bytes().splitlines(keepends=True))


def test_n4_non_ascii_not_escaped_on_changed_line(tmp_path):
    rows = _zephyr_rows()
    rows[0]["checks"]["type"]["reason"] = "café"
    src = tmp_path / "in.jsonl"
    src.write_bytes("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode())
    out = tmp_path / "out.jsonl"
    assert _run(["--in", str(src), "--out", str(out), "--reader", "zephyr"]).returncode == 0
    assert "café".encode() in out.read_bytes().splitlines()[0]


# ---------------------------------------------------------------- N5 no-op control
def test_n5_no_loose_prefix_file_byte_identical_for_other_reader(tmp_path):
    rows = [
        _row("dv_0001", ("tight", "loose", "cannot-judge"), proposed="x"),
        _row("ob_0001", ("tight", "tight", "loose")),
    ]
    src = tmp_path / "in.jsonl"
    src.write_bytes(
        (json.dumps(rows[0]) + "\n" + json.dumps(rows[1], separators=(",", ":"), ensure_ascii=True) + "\r\n\n").encode()
    )
    out = tmp_path / "out.jsonl"
    r = _run(["--in", str(src), "--out", str(out), "--reader", "mira"])
    assert r.returncode == 0, r.stderr
    assert hashlib.sha256(out.read_bytes()).hexdigest() == hashlib.sha256(src.read_bytes()).hexdigest()


# ---------------------------------------------------------------- N6 determinism
def test_n6_two_runs_byte_identical(tmp_path):
    src = _write(tmp_path / "in.jsonl", _zephyr_rows())
    o1, o2 = tmp_path / "o1.jsonl", tmp_path / "o2.jsonl"
    for o in (o1, o2):
        assert _run(["--in", str(src), "--out", str(o), "--reader", "zephyr"]).returncode == 0
    assert o1.read_bytes() == o2.read_bytes()


# ---------------------------------------------------------------- N7 output validates
def test_n7_output_passes_validator_input_does_not(tmp_path):
    rows = _zephyr_rows()
    ids = _ids(rows)
    src = _write(tmp_path / "in.jsonl", rows)
    out = tmp_path / "out.jsonl"
    with pytest.raises(an.VerdictFileInvalid):
        an.validate_verdicts(src, ids, "zephyr")
    assert _run(["--in", str(src), "--out", str(out), "--reader", "zephyr"]).returncode == 0
    got = an.validate_verdicts(out, ids, "zephyr")
    assert sorted(got) == sorted(ids)
    assert got["dv_0000"]["type"]["verdict"] == "loose"


def test_n7_check_names_come_from_analyze_not_relisted():
    assert tuple(nl.ALL_CHECKS) == tuple(an.ALL_CHECKS)
    assert tuple(nl.VERDICTS) == tuple(an.VERDICTS)


# ---------------------------------------------------------------- N8 safety
def test_n8_out_exists_refused_and_untouched(tmp_path):
    src = _write(tmp_path / "in.jsonl", _zephyr_rows())
    out = tmp_path / "out.jsonl"
    out.write_text("precious")
    r = _run(["--in", str(src), "--out", str(out), "--reader", "zephyr"])
    assert r.returncode != 0
    assert out.read_text() == "precious"


def test_n8_out_same_file_as_in_refused(tmp_path):
    src = _write(tmp_path / "in.jsonl", _zephyr_rows())
    before = src.read_bytes()
    r = _run(["--in", str(src), "--out", str(tmp_path / "." / "in.jsonl"), "--reader", "zephyr"])
    assert r.returncode != 0
    assert src.read_bytes() == before


def test_n8_out_symlink_to_in_refused(tmp_path):
    src = _write(tmp_path / "in.jsonl", _zephyr_rows())
    link = tmp_path / "link.jsonl"
    link.symlink_to(src)
    before = src.read_bytes()
    r = _run(["--in", str(src), "--out", str(link), "--reader", "zephyr"])
    assert r.returncode != 0
    assert src.read_bytes() == before


# ---------------------------------------------------------------- N9 report
def test_n9_report_lines(tmp_path):
    r, _, out = _cli(tmp_path, _zephyr_rows())
    assert r.returncode == 0, r.stderr
    lines = r.stdout.strip().splitlines()
    assert len(lines) == len(an.ALL_CHECKS) + 1
    counts = {ln.split()[0].rstrip(":"): ln.split()[-1] for ln in lines[:-1]}
    assert counts["type"] == "10" and counts["placement"] == "13" and counts["chain-overreach"] == "14"
    assert counts["quote_type"] == "0"
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    assert lines[-1] == f"sha256 {digest} {out}"
