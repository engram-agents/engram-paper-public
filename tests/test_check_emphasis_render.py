"""Contract tests for tools/check_emphasis_render.py, written before the code.

The check renders Markdown with a CONFORMANT CommonMark parser (markdown-it-py) and
reports every literal `*` left in the rendered text outside code. The oracle is never
the PDF builder: the builder's rules are exactly what is in question.

  (i)   real-tree baseline equality, both languages
  (ii)  planted `**中文。**它` gives exactly one bold finding
  (iii) planted K*7, xK*2, K*23 each give a finding; K*2–K*6 gives none
  (iv)  `**x**` inside a code span or a fence gives none
  (v)   stale baseline: a baseline entry no longer found FAILS and is named
  (vi)  oracle missing: non-zero exit and a message -- never a pass, never a skip
  plus: --gate-zero fails on any finding; default mode fails on a new finding.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import tools.check_emphasis_render as cer

REPO = Path(__file__).resolve().parents[1]
RELEASE = REPO / "paper" / "release"
EN = RELEASE / "engram-paper-v0.5.1.md"
ZH = RELEASE / "engram-paper-v0.5.1.zh.md"


def scan(text):
    findings, allowed = cer.scan(text, "fixture.md")
    return findings, allowed


def kinds(findings):
    return sorted(f["kind"] for f in findings)


# ------------------------------------------------------------------------- (i)
def test_real_tree_findings_equal_the_committed_baseline(capsys):
    rc = cer.main([])
    out = capsys.readouterr().out
    assert rc == 0, out


def test_real_tree_numbers_en_and_zh():
    en_findings, en_allowed = cer.scan(EN.read_text(encoding="utf-8"), "en")
    zh_findings, zh_allowed = cer.scan(ZH.read_text(encoding="utf-8"), "zh")
    assert en_findings == [] and en_allowed == 4
    assert zh_allowed == 4
    assert kinds(zh_findings) == ["bold"] * 7 + ["single"] * 16


# ------------------------------------------------------------------------ (ii)
def test_planted_chinese_bold_followed_by_text_is_one_bold_finding():
    findings, _ = scan("前文。**中文。**它继续。\n")
    assert kinds(findings) == ["bold"]
    f = findings[0]
    assert f["file"] == "fixture.md" and "中文" in f["context"]


# ----------------------------------------------------------------------- (iii)
def test_allowlisted_agm_names_give_no_finding():
    # The source escapes them (K\*2); unescaped, CommonMark reads K*2–K* as emphasis.
    findings, allowed = scan("The postulates K\\*2–K\\*6 hold.\n")
    assert findings == [] and allowed == 2


def test_k_star_outside_the_allowlist_each_give_a_finding():
    for bad in ("K*7", "xK*2", "K*23"):
        findings, allowed = scan("see " + bad.replace("*", "\\*") + " here\n")
        assert kinds(findings) == ["single"], bad
        assert allowed == 0, bad


# ------------------------------------------------------------------------ (iv)
def test_emphasis_markers_in_code_give_no_finding():
    assert scan("inline `**x**` and `*y*` here\n")[0] == []
    assert scan("```\n**x** and *y*\n```\n")[0] == []
    assert scan("~~~\n**x**\n~~~\n")[0] == []
    assert scan("    **indented code**\n")[0] == []


def test_conformant_emphasis_gives_no_finding():
    assert scan("*em* and **strong** and ***both***\n")[0] == []


# ------------------------------------------------------------------------- (v)
def write_baseline(path, findings):
    path.write_text(json.dumps({"findings": findings}, ensure_ascii=False), encoding="utf-8")


def test_stale_baseline_entry_fails_and_names_it(tmp_path, capsys):
    doc = tmp_path / "a.md"
    doc.write_text("one **中文。**它\n\ntwo K*7 end\n", encoding="utf-8")
    base = tmp_path / "base.json"
    findings, _ = cer.scan(doc.read_text(encoding="utf-8"), cer.label_for(doc))
    assert len(findings) == 2
    write_baseline(base, findings)
    assert cer.main([str(doc), "--baseline", str(base)]) == 0
    capsys.readouterr()

    doc.write_text("one **中文。**它\n", encoding="utf-8")  # K*7 source deleted
    rc = cer.main([str(doc), "--baseline", str(base)])
    out = capsys.readouterr().out
    assert rc != 0
    assert "stale" in out.lower() and "K*7" in out


def test_a_new_finding_fails_default_mode(tmp_path, capsys):
    doc = tmp_path / "a.md"
    doc.write_text("clean\n", encoding="utf-8")
    base = tmp_path / "base.json"
    write_baseline(base, [])
    assert cer.main([str(doc), "--baseline", str(base)]) == 0
    doc.write_text("clean **中文。**它\n", encoding="utf-8")
    capsys.readouterr()
    assert cer.main([str(doc), "--baseline", str(base)]) != 0
    assert "new finding" in capsys.readouterr().out.lower()


def test_gate_zero_fails_on_any_finding_even_if_baselined(tmp_path):
    doc = tmp_path / "a.md"
    doc.write_text("clean **中文。**它\n", encoding="utf-8")
    base = tmp_path / "base.json"
    findings, _ = cer.scan(doc.read_text(encoding="utf-8"), cer.label_for(doc))
    write_baseline(base, findings)
    assert cer.main([str(doc), "--baseline", str(base)]) == 0
    assert cer.main([str(doc), "--baseline", str(base), "--gate-zero"]) != 0


def test_gate_zero_passes_on_a_clean_file(tmp_path):
    doc = tmp_path / "a.md"
    doc.write_text("clean *em* and K*3\n", encoding="utf-8")
    assert cer.main([str(doc), "--gate-zero"]) == 0


# ------------------------------------------------------------------------ (vi)
def test_oracle_missing_exits_nonzero_with_a_message(monkeypatch, capsys):
    monkeypatch.setitem(sys.modules, "markdown_it", None)  # `import markdown_it` now raises
    rc = cer.main([str(EN), "--gate-zero"])
    captured = capsys.readouterr()
    assert rc != 0
    assert "oracle" in (captured.err + captured.out).lower()
    assert "markdown-it-py" in (captured.err + captured.out)


def test_markdown_it_is_a_declared_requirement():
    reqs = (REPO / "requirements.txt").read_text(encoding="utf-8")
    assert "markdown-it-py>=3,<4" in reqs


# ------------------------------------------------------------------- S2: image alt text
def test_a_literal_star_in_image_alt_text_is_a_finding():
    findings, _ = scan("![a * b](x.png)\n")
    assert kinds(findings) == ["single"]
    assert findings[0]["file"] == "fixture.md"


def test_conformant_emphasis_in_image_alt_text_gives_no_finding():
    assert scan("![a *b* and **c**](x.png)\n")[0] == []


def test_alt_text_is_scanned_as_its_own_block_never_fused_with_the_text_around_it():
    # Alt "x *" and the "*" after the image are two separate literal stars (2 findings).
    # Fused into one stream they would read "x ** tail": one unpaired `**` run, 1 finding.
    findings, _ = scan("![x *](i.png)* tail\n")
    assert kinds(findings) == ["single", "single"]


def test_a_bold_pair_split_across_alt_and_outer_text_is_not_a_bold_finding():
    # Fused, "**" in the alt and "**" after the image would pair into one `bold` finding.
    findings, _ = scan("![a **](i.png)** b\n")
    assert kinds(findings) == ["single", "single"]
