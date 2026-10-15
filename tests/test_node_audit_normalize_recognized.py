"""Contract tests for `studies/node-audit/normalize_recognized.py` (PROTOCOL.md Amendment 5,
the recognized.txt addendum: one pinned, single-output reshaping of a reader's recognized file).

Written BEFORE the implementation (contract-first). Clause numbers R1-R8 match the tool's module
docstring. SYNTHETIC data only: every input is built inside the test; no real recognized file,
packet, verdict or snapshot is ever read, and no node content appears here.

Synthetic ariadne-shaped fixture (44 physical lines):
  lines 1-7, 24-43   single-id lines (27); line 3 also carries LATE
  lines 8-23         multi-id lines (16): first id packet-shaped, later ids outside the packet;
                     line 8 also carries LATE
  line 44            six packet ids and the phrase "not mine" (dropped)
  => stripped 16, dropped [44], untouched 27, ids_out 43
"""
from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "studies" / "node-audit" / "normalize_recognized.py"


def _load():
    spec = importlib.util.spec_from_file_location("normalize_recognized", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["normalize_recognized"] = mod
    spec.loader.exec_module(mod)
    return mod


nr = _load()
arms = nr.arms  # the analyze_arms module the tool actually imports
ID_TOKEN, LATE_TOKEN = arms.ID_TOKEN, arms.LATE_TOKEN

PHRASE = "not mine"
STRIPPED_LINES = list(range(8, 24))
SINGLE_LINES = list(range(1, 8)) + list(range(24, 44))
LATE_SINGLE, LATE_MULTI = 3, 8


def _first(n):
    return f"dv_{n:04d}"


def _fixture_lines():
    out = []
    for n in range(1, 45):
        if n in SINGLE_LINES:
            s = f"{_first(n)} synthetic single {n}"
            if n == LATE_SINGLE:
                s += " LATE"
        elif n in STRIPPED_LINES:
            s = f"{_first(n)} synthetic note mentions {_first(5000 + n)} and ob_{n:04d} too"
            if n == LATE_MULTI:
                s += " LATE"
        else:
            s = " ".join(f"dv_{8000 + k:04d}" for k in range(1, 7)) + f" synthetic {PHRASE} here"
        out.append(s)
    return out


def _packet_ids():
    return {_first(n) for n in range(1, 44)} | {f"dv_{8000 + k:04d}" for k in range(1, 7)}


def _write(path, lines, ending="\n"):
    path.write_bytes("".join(s + ending for s in lines).encode())
    return path


def _run(args):
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True)


def _cli(tmp_path, lines, reader="ariadne", ending="\n"):
    src = _write(tmp_path / "in.txt", lines, ending)
    out = tmp_path / "out.txt"
    r = _run(["--in", str(src), "--out", str(out), "--reader", reader])
    return r, src, out


def _only_dir_is_input(tmp_path):
    return sorted(p.name for p in tmp_path.iterdir()) == ["in.txt"]


# ---------------------------------------------------------------- R1 pin
def test_r1_pin_constant():
    assert nr.EXPECTED == {
        "ariadne": {"stripped": 16, "dropped": [44], "untouched": 27, "ids_out": 43, "drop_phrase": "not mine"}
    }


def test_r1_other_reader_expectation_is_noop():
    e = nr.expected_for("someone")
    assert e["stripped"] == 0 and e["dropped"] == [] and e["drop_phrase"] is None


def test_r1_ids_come_from_analyze_arms_not_redefined():
    assert nr.ID_TOKEN is arms.ID_TOKEN and nr.LATE_TOKEN is arms.LATE_TOKEN


# ---------------------------------------------------------------- success path / R2 / R7
def test_success_path_output_lines(tmp_path):
    r, src, out = _cli(tmp_path, _fixture_lines())
    assert r.returncode == 0, r.stderr
    got = out.read_text().splitlines()
    assert len(got) == 43
    for n in STRIPPED_LINES:
        want = _first(n) + (" LATE" if n == LATE_MULTI else "")
        assert got[n - 1] == want
    assert all(len(ID_TOKEN.findall(g)) == 1 for g in got)
    assert not any(PHRASE in g for g in got)


def test_untouched_lines_byte_identical(tmp_path):
    r, src, out = _cli(tmp_path, _fixture_lines())
    assert r.returncode == 0, r.stderr
    orig = src.read_bytes().splitlines(keepends=True)
    got = out.read_bytes().splitlines(keepends=True)
    for n in SINGLE_LINES:
        assert got[n - 1] == orig[n - 1]


def test_late_preserved_on_stripped_line_and_untouched_line(tmp_path):
    r, _, out = _cli(tmp_path, _fixture_lines())
    got = out.read_text().splitlines()
    assert LATE_TOKEN.search(got[LATE_MULTI - 1]) and LATE_TOKEN.search(got[LATE_SINGLE - 1])
    assert sum(1 for g in got if LATE_TOKEN.search(g)) == 2


def test_stripped_line_keeps_original_line_ending(tmp_path):
    r, _, out = _cli(tmp_path, _fixture_lines(), ending="\r\n")
    assert r.returncode == 0, r.stderr
    assert all(l.endswith(b"\r\n") for l in out.read_bytes().splitlines(keepends=True))


def test_blank_and_comment_lines_pass_through_and_do_not_shift_nothing_counted(tmp_path):
    # Physical numbering: a leading comment shifts every data line by one, so the pin (line 44) no
    # longer points at the phrase line -> refused. Passing through blank/# lines is tested on a no-op file.
    r, _, out = _cli(tmp_path, ["# header"] + _fixture_lines())
    assert r.returncode != 0 and not out.exists()


# ---------------------------------------------------------------- R3 refusals
def test_phrase_missing_on_line_44_refused(tmp_path):
    lines = _fixture_lines()
    lines[43] = lines[43].replace(PHRASE, "mine")
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode != 0 and not out.exists()
    assert "line 44" in r.stderr
    assert _only_dir_is_input(tmp_path)


def test_phrase_case_insensitive_on_line_44(tmp_path):
    lines = _fixture_lines()
    lines[43] = lines[43].replace(PHRASE, "NOT Mine")
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode == 0, r.stderr


def test_phrase_present_on_another_line_refused(tmp_path):
    lines = _fixture_lines()
    lines[11] += " Not Mine"  # line 12, a stripped line
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode != 0 and not out.exists()
    assert "line 12" in r.stderr


def test_phrase_present_on_single_id_line_refused(tmp_path):
    lines = _fixture_lines()
    lines[0] += " not mine"
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode != 0 and not out.exists()
    assert "line 1" in r.stderr


def test_line_without_id_refused(tmp_path):
    lines = _fixture_lines()
    lines[29] = "synthetic text with no id at all"  # line 30
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode != 0 and not out.exists()
    assert "line 30" in r.stderr


def test_per_field_mismatch_with_right_ids_out_refused(tmp_path):
    # 15 stripped / 28 untouched keeps ids_out == 43 (and the dropped line right): only a per-field
    # check can see it.
    lines = _fixture_lines()
    lines[9] = f"{_first(10)} synthetic single 10"  # line 10 was multi-id
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode != 0 and not out.exists()
    assert "stripped" in r.stderr and "untouched" in r.stderr
    assert "expected 16, actual 15" in r.stderr and "expected 27, actual 28" in r.stderr
    assert "ids_out" not in r.stderr  # only the mismatched fields are named


def test_ids_out_mismatch_refused(tmp_path):
    lines = _fixture_lines()[:43]  # no line 44: dropped field and ids_out unchanged? dropped=[] vs [44]
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode != 0 and not out.exists()
    assert "dropped" in r.stderr


def test_extra_data_line_refused_on_ids_out(tmp_path):
    lines = _fixture_lines() + [f"dv_0900 extra"]
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode != 0 and not out.exists()
    assert "ids_out" in r.stderr


def test_duplicate_first_ids_refused(tmp_path):
    lines = _fixture_lines()
    lines[1] = lines[0]  # line 2 repeats line 1's id (counts stay right)
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode != 0 and not out.exists()
    assert "line 2" in r.stderr and "duplicate" in r.stderr


def test_every_offending_line_listed(tmp_path):
    lines = _fixture_lines()
    lines[0] += " not mine"
    lines[1] += " not mine"
    lines[29] = "no id here"
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode != 0 and not out.exists()
    for n in ("line 1:", "line 2:", "line 30:"):
        assert n in r.stderr


# ---------------------------------------------------------------- R4 no leakage
def test_refusal_leaks_no_id_and_no_line_text(tmp_path):
    lines = _fixture_lines()
    lines[0] += " not mine"
    lines[29] = "secretword free text, no id"
    lines[43] = lines[43].replace(PHRASE, "mine")
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode != 0 and not out.exists()
    assert r.stderr.startswith("REFUSED:")
    assert ID_TOKEN.search(r.stderr) is None
    assert "secretword" not in r.stderr and "synthetic" not in r.stderr
    assert r.stdout == ""


# ---------------------------------------------------------------- R5 safety
def test_out_exists_refused_and_untouched(tmp_path):
    src = _write(tmp_path / "in.txt", _fixture_lines())
    out = tmp_path / "out.txt"
    out.write_text("precious")
    r = _run(["--in", str(src), "--out", str(out), "--reader", "ariadne"])
    assert r.returncode != 0 and out.read_text() == "precious"


def test_out_same_file_as_in_refused(tmp_path):
    src = _write(tmp_path / "in.txt", _fixture_lines())
    before = src.read_bytes()
    r = _run(["--in", str(src), "--out", str(tmp_path / "." / "in.txt"), "--reader", "ariadne"])
    assert r.returncode != 0 and src.read_bytes() == before


def test_out_missing_dir_and_missing_input_refused(tmp_path):
    src = _write(tmp_path / "in.txt", _fixture_lines())
    assert _run(["--in", str(src), "--out", str(tmp_path / "nodir" / "o.txt"), "--reader", "ariadne"]).returncode != 0
    assert _run(["--in", str(tmp_path / "nope.txt"), "--out", str(tmp_path / "o.txt"), "--reader", "ariadne"]).returncode != 0
    assert not (tmp_path / "o.txt").exists()


# ---------------------------------------------------------------- no-op control
def test_noop_control_other_reader_byte_identical(tmp_path):
    lines = ["# header", "", "dv_0001 fine", "ob_0002 LATE", "  ", "dv_0003"]
    src = tmp_path / "in.txt"
    src.write_bytes(("\n".join(lines) + "\r\n\n").encode())
    out = tmp_path / "out.txt"
    r = _run(["--in", str(src), "--out", str(out), "--reader", "other"])
    assert r.returncode == 0, r.stderr
    assert hashlib.sha256(out.read_bytes()).hexdigest() == hashlib.sha256(src.read_bytes()).hexdigest()


def test_other_reader_multi_id_line_refused(tmp_path):
    r, _, out = _cli(tmp_path, ["dv_0001 and dv_0002"], reader="other")
    assert r.returncode != 0 and not out.exists()


def test_other_reader_phrase_not_special(tmp_path):
    r, _, out = _cli(tmp_path, ["dv_0001 not mine"], reader="other")
    assert r.returncode == 0, r.stderr


# ---------------------------------------------------------------- R6 determinism / R7 report
def test_two_runs_byte_identical(tmp_path):
    src = _write(tmp_path / "in.txt", _fixture_lines())
    o1, o2 = tmp_path / "o1.txt", tmp_path / "o2.txt"
    for o in (o1, o2):
        assert _run(["--in", str(src), "--out", str(o), "--reader", "ariadne"]).returncode == 0
    assert o1.read_bytes() == o2.read_bytes()


def test_report_lines(tmp_path):
    r, _, out = _cli(tmp_path, _fixture_lines())
    assert r.returncode == 0, r.stderr
    lines = r.stdout.strip().splitlines()
    assert lines[:4] == ["stripped: 16", "dropped: [44]", "untouched: 27", "ids_out: 43"]
    assert lines[4] == f"sha256 {hashlib.sha256(out.read_bytes()).hexdigest()} {out}"
    assert len(lines) == 5


# ---------------------------------------------------------------- R8 output parses
def test_output_parses_with_analyze_arms_and_late_survives(tmp_path):
    r, src, out = _cli(tmp_path, _fixture_lines())
    assert r.returncode == 0, r.stderr
    with __import__("pytest").raises(arms.RecognizedInvalid):
        arms.parse_recognized(src, _packet_ids())  # the input is what A2 refuses
    recognized, late = arms.parse_recognized(out, _packet_ids())
    assert recognized == {_first(n) for n in range(1, 44)}
    assert late == {_first(LATE_SINGLE), _first(LATE_MULTI)}


# ---------------------------------------------------------------- round 4: numbering parity with parse_recognized
SEPARATORS = ["\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", " ", " "]


def test_numbering_parity_with_str_splitlines_and_parse_recognized(tmp_path):
    src = _write(tmp_path / "in.txt", _fixture_lines())
    assert len(src.read_text().splitlines()) == len(src.read_bytes().splitlines()) == 44
    # the real parser numbers the multi-id lines exactly as this tool's pin numbers them
    try:
        arms.parse_recognized(src, _packet_ids())
    except arms.RecognizedInvalid as e:
        said = {int(x) for x in __import__("re").findall(r"line (\d+): more than one id", str(e))}
    assert said == set(STRIPPED_LINES) | {44}


def test_extra_separators_refused_each(tmp_path):
    for sep in SEPARATORS:
        lines = _fixture_lines()
        lines[4] = lines[4] + sep + "tail"  # line 5
        d = tmp_path / f"s{ord(sep):x}"
        d.mkdir()
        r, _, out = _cli(d, lines)
        assert r.returncode != 0, repr(sep)
        assert not out.exists()
        assert "line 5" in r.stderr
        assert ID_TOKEN.search(r.stderr) is None and "tail" not in r.stderr


def test_extra_separator_refused_for_other_reader_too(tmp_path):
    r, _, out = _cli(tmp_path, ["dv_0001 a\x0cb"], reader="other")
    assert r.returncode != 0 and not out.exists() and "line 1" in r.stderr


def test_utf8_non_separator_text_still_fine(tmp_path):
    lines = _fixture_lines()
    lines[4] += " café — dash"
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode == 0, r.stderr


# ---------------------------------------------------------------- round 4: LATE position
def _late_fixture(before, after_later):
    lines = _fixture_lines()
    lines[LATE_MULTI - 1] = f"{_first(LATE_MULTI)} synthetic note mentions {_first(5000 + LATE_MULTI)}"  # plain
    lines[11] = f"LATE {_first(12)} synthetic note mentions {_first(5012)}"  # line 12: LATE before the first id
    lines[12] = f"{_first(13)} synthetic note mentions {_first(5013)} LATE"  # line 13: LATE after a later id
    return lines


def test_late_before_first_id_kept(tmp_path):
    r, _, out = _cli(tmp_path, _late_fixture(True, True))
    assert r.returncode == 0, r.stderr
    assert out.read_text().splitlines()[11] == f"{_first(12)} LATE"


def test_late_after_a_later_id_kept(tmp_path):
    r, _, out = _cli(tmp_path, _late_fixture(True, True))
    assert r.returncode == 0, r.stderr
    assert out.read_text().splitlines()[12] == f"{_first(13)} LATE"


def test_late_substring_of_a_word_is_not_late(tmp_path):
    lines = _fixture_lines()
    lines[LATE_MULTI - 1] = f"{_first(LATE_MULTI)} note {_first(5008)} LATELY and PLATE"
    r, _, out = _cli(tmp_path, lines)
    assert r.returncode == 0, r.stderr
    assert out.read_text().splitlines()[LATE_MULTI - 1] == _first(LATE_MULTI)
