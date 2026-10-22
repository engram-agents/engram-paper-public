#!/usr/bin/env python3
"""Render the ENGRAM paper's single-file Markdown into a self-contained,
print-ready A4 HTML document.

Why a hand-rolled converter: no markdown library is installed on this seat, and
the render uses a small, stable subset (headings, tables, blockquotes, fenced
code, lists, images, inline emphasis). Figures are inlined as data URIs so the
output is ONE file that prints correctly from any machine with no asset paths.

Mermaid blocks are rendered to SVG at BUILD time (via mermaid_to_svg.py) and inlined,
rather than left to a CDN script at view time: the output must print correctly
offline, and a client-side renderer that has not finished laying out when the
print dialog opens silently produces a blank box. Rendered SVGs are cached by
content hash, so an unchanged diagram costs nothing on a rebuild.

Usage:  paper_to_print_html.py <input.md> <output.html> [--banner "text"]
                               [--mermaid-cache <dir>] [--require-mermaid]

--require-mermaid is the strict path: a missing or hash-mismatched mermaid bundle, an
unavailable renderer, or any diagram that fails to render exits non-zero naming the
cause and leaves no output file. Without it those cases fall back to the source block
and exit 0.
"""
import base64
import hashlib
import html
import mimetypes
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------- inline

_INLINE = [
    (re.compile(r'`([^`]+)`'),                lambda m: f'<code>{html.escape(m.group(1))}</code>'),
    (re.compile(r'\*\*\*(.+?)\*\*\*'),        r'<strong><em>\1</em></strong>'),
    (re.compile(r'\*\*(.+?)\*\*'),            r'<strong>\1</strong>'),
    (re.compile(r'(?<![A-Za-z0-9_*])\*([^*\n]+)\*(?![A-Za-z0-9_*])'), r'<em>\1</em>'),  # ASCII word chars only, so emphasis next to CJK text still converts
    (re.compile(r'~~(.+?)~~'),                r'<del>\1</del>'),
    (re.compile(r'\[([^\]]+)\]\(([^)]+)\)'),  r'<a href="\2">\1</a>'),
]


def inline(text):
    """Escape, then apply inline markup. Code spans are protected first."""
    spans = []

    def stash(m):
        spans.append(html.escape(m.group(1)))
        return f'\x00{len(spans) - 1}\x00'

    text = re.sub(r'`([^`]+)`', stash, text)
    # Bare anchor targets the book writes for cross-references (<a id="sec-1-2"></a>)
    # are HTML, not text: pass them through instead of escaping them into visible tags.
    anchors = []
    def keep_anchor(m):
        anchors.append(m.group(0))
        return f'\x02{len(anchors) - 1}\x02'
    text = re.sub(r'<a id="[^"<>]+"></a>|</?(?:sup|sub)>', keep_anchor, text)
    # Markdown backslash escapes (\* \_ \[ ...) are literal characters: protect them
    # before emphasis runs, or an escaped `\*` pairs with a later real `*` as italics.
    text = re.sub(r'\\([\\`*_{}\[\]()#+\-.!|])', lambda m: f'\x01{ord(m.group(1))}\x01', text)
    text = html.escape(text)
    for pat, rep in _INLINE[1:]:
        text = pat.sub(rep, text)
    text = re.sub(r'\x01(\d+)\x01', lambda m: html.escape(chr(int(m.group(1)))), text)
    text = re.sub(r'\x02(\d+)\x02', lambda m: anchors[int(m.group(1))], text)
    return re.sub(r'\x00(\d+)\x00', lambda m: f'<code>{spans[int(m.group(1))]}</code>', text)


def img_tag(alt, src, base):
    """Inline the image as a data URI so the HTML is self-contained."""
    p = (base / src).resolve()
    if p.is_file():
        mime = mimetypes.guess_type(p.name)[0] or 'image/png'
        b64 = base64.b64encode(p.read_bytes()).decode('ascii')
        return (f'<figure><img src="data:{mime};base64,{b64}" alt="{html.escape(alt)}">'
                f'<figcaption>{html.escape(alt)}</figcaption></figure>')
    return f'<p class="missing-figure">[missing figure: {html.escape(src)}]</p>'


# ---------------------------------------------------------------- mermaid

# Rendering runs out-of-process in a Python that has the playwright bindings;
# mermaid-cli's npx install timed out at 7 minutes and would have pulled a second
# Chromium. See mermaid_to_svg.py. The interpreter is this one by default; set
# PDF_BUILD_PYTHON to point at another (e.g. a venv that has playwright). A path that
# does not exist disables the mermaid step: diagrams fall back to their source block.
_RENDERER = Path(__file__).resolve().parent / 'mermaid_to_svg.py'
_VENV_PY = Path(os.environ.get('PDF_BUILD_PYTHON') or sys.executable)


class MermaidRequired(Exception):
    """Raised, under --require-mermaid, instead of falling back to a source block."""


def _check_svg(raw, source):
    """Raise MermaidRequired unless `raw` (bytes) is an XML document with an <svg> root.

    A real XML parse, not a prefix check: an empty, truncated or non-SVG file must not
    count as a rendered diagram. `source` names where the bytes came from.
    """
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        raise MermaidRequired(f'invalid SVG from {source}: not well-formed XML ({e})') from None
    if root.tag.rpartition('}')[2] != 'svg':
        raise MermaidRequired(f'invalid SVG from {source}: root element is <{root.tag}>, not <svg>')


def render_mermaid(code, cache_dir, strict=False):
    """Return inline SVG for a mermaid block, or None if it cannot be rendered.

    Cached by content hash: an unchanged diagram never re-renders, a changed one
    always does. None is a real outcome, not an error — the caller falls back to
    showing the source, which is what the block did before. With strict=True
    (--require-mermaid) every None outcome raises MermaidRequired instead.
    """
    if cache_dir is None:
        if strict:
            raise MermaidRequired('no mermaid cache directory given')
        return None
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(code.encode('utf-8')).hexdigest()[:16]
    svg_path = cache_dir / f'mermaid-{key}.svg'

    if not svg_path.is_file():
        if not (_VENV_PY.is_file() and _RENDERER.is_file()):
            if strict:
                raise MermaidRequired(f'mermaid renderer unavailable ({_VENV_PY} / {_RENDERER})')
            print(f'  mermaid: renderer unavailable ({_VENV_PY} / {_RENDERER}) — '
                  f'falling back to source block', file=sys.stderr)
            return None
        with tempfile.TemporaryDirectory() as td:
            mmd = Path(td) / 'd.mmd'
            mmd.write_text(code + '\n', encoding='utf-8')
            try:
                subprocess.run([str(_VENV_PY), str(_RENDERER), str(mmd), str(svg_path)],
                               check=True, capture_output=True, timeout=300)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                detail = getattr(e, 'stderr', b'') or b''
                if strict:
                    raise MermaidRequired(
                        f'mermaid diagram failed to render ({type(e).__name__}): '
                        f'{detail.decode("utf-8", "replace").strip()[-300:]}') from e
                print(f'  mermaid render failed ({type(e).__name__}): '
                      f'{detail.decode("utf-8", "replace").strip()[-300:]}\n'
                      f'  falling back to source block', file=sys.stderr)
                return None
        if not svg_path.is_file():
            if strict:
                raise MermaidRequired('mermaid diagram failed to render: renderer wrote no SVG')
            return None

    if strict:
        # Never trust the cache unvalidated: a hit is checked exactly like a fresh render
        # (the cache is keyed by diagram text only, so a corrupt file would be reused forever).
        _check_svg(svg_path.read_bytes(), f'the mermaid cache file {svg_path}')
    svg = svg_path.read_text(encoding='utf-8')
    # Strip the XML prolog/DOCTYPE so the SVG can sit inline in HTML.
    svg = re.sub(r'<\?xml[^>]*\?>\s*', '', svg)
    svg = re.sub(r'<!DOCTYPE[^>]*>\s*', '', svg)
    # mermaid emits a fixed pixel width; let it scale to the text column instead.
    svg = re.sub(r'(<svg\b[^>]*?)\swidth="[\d.]+(?:px)?"', r'\1', svg, count=1)
    svg = re.sub(r'(<svg\b[^>]*?)\sheight="[\d.]+(?:px)?"', r'\1', svg, count=1)
    svg = svg.replace('<svg ', '<svg class="mermaid-svg" ', 1)
    return f'<figure class="diagram">{svg}</figure>'


# ---------------------------------------------------------------- block

def convert(md, base, mermaid_cache=None, strict=False):
    out, lines, i = [], md.split('\n'), 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # fenced code
        if line.startswith('```') or line.startswith('~~~'):
            fence = line[:3]
            i += 1
            buf = []
            while i < n and not lines[i].startswith(fence):
                buf.append(lines[i]); i += 1
            i += 1
            lang = line[3:].strip().lower()
            code = '\n'.join(buf)
            if lang == 'mermaid':
                fig = render_mermaid(code, mermaid_cache, strict)
                if fig:
                    out.append(fig)
                    continue
            out.append('<pre><code>' + html.escape(code) + '</code></pre>')
            continue

        # image on its own line
        m = re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)', line.strip())
        if m:
            out.append(img_tag(m.group(1), m.group(2), base)); i += 1
            continue

        # heading
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            lvl = len(m.group(1))
            out.append(f'<h{lvl}>{inline(m.group(2).strip())}</h{lvl}>')
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r'\s*([-*_])\s*(\1\s*){2,}', line):
            out.append('<hr>'); i += 1
            continue

        # table: header row, separator row, body
        if (line.lstrip().startswith('|') and i + 1 < n
                and re.fullmatch(r'\s*\|[\s:|-]+\|\s*', lines[i + 1])):
            def cells(row):
                return [c.strip() for c in row.strip().strip('|').split('|')]
            head = cells(line)
            i += 2
            body = []
            while i < n and lines[i].lstrip().startswith('|'):
                body.append(cells(lines[i])); i += 1
            t = ['<table><thead><tr>']
            t += [f'<th>{inline(c)}</th>' for c in head]
            t.append('</tr></thead><tbody>')
            for row in body:
                t.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in row) + '</tr>')
            t.append('</tbody></table>')
            out.append(''.join(t))
            continue

        # blockquote (consume the whole run, recurse on its contents)
        if line.lstrip().startswith('>'):
            buf = []
            while i < n and (lines[i].lstrip().startswith('>') or
                             (lines[i].strip() and buf and not lines[i].lstrip().startswith(('#', '|', '-', '*')))):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            out.append('<blockquote>' + convert('\n'.join(buf), base, mermaid_cache, strict) + '</blockquote>')
            continue

        # lists
        m = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)$', line)
        if m:
            ordered = not m.group(2) in ('-', '*', '+')
            tag = 'ol' if ordered else 'ul'
            items = []
            while i < n:
                mm = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)$', lines[i])
                if not mm:
                    # continuation line of the current item
                    if items and lines[i].strip() and lines[i].startswith((' ', '\t')):
                        items[-1] += ' ' + lines[i].strip(); i += 1
                        continue
                    break
                items.append(mm.group(3)); i += 1
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
            continue

        # blank
        if not line.strip():
            i += 1
            continue

        # paragraph
        buf = []
        while i < n and lines[i].strip() and not re.match(
                r'^(#{1,6}\s|>|\s*([-*+]|\d+\.)\s|\||```|~~~|!\[)', lines[i]):
            buf.append(lines[i].strip()); i += 1
        if buf:
            out.append(f'<p>{inline(" ".join(buf))}</p>')

    return '\n'.join(out)


CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
:root { --ink:#16181d; --muted:#5b6270; --rule:#d6dae1; --accent:#2f4f7f; --bg:#fff; }
* { box-sizing: border-box; }
body {
  font-family: "Source Serif Pro", Georgia, "Times New Roman", "DejaVu Serif", "Noto Sans SC Clean", serif;
  font-size: 10.5pt; line-height: 1.52; color: var(--ink); background: var(--bg);
  max-width: 44em; margin: 0 auto; padding: 2.5em 1.5em 4em; hyphens: auto;
}
h1,h2,h3,h4,h5,h6 {
  font-family: "Source Sans Pro", "Helvetica Neue", Arial, "DejaVu Sans", "Noto Sans SC Clean", sans-serif;
  color: var(--accent); line-height: 1.25; break-after: avoid; page-break-after: avoid;
  margin: 1.6em 0 .5em;
}
h1 { font-size: 19pt; margin-top: 2.2em; border-bottom: 2px solid var(--rule); padding-bottom: .3em; }
h1:first-of-type { margin-top: 0; }
h2 { font-size: 14.5pt; margin-top: 1.9em; }
h3 { font-size: 12pt; }
h4 { font-size: 10.8pt; color: var(--ink); }
p { margin: 0 0 .75em; text-align: justify; }
a { color: var(--accent); text-decoration: none; word-break: break-word; }
strong { font-weight: 650; }
code {
  font-family: "SF Mono", "DejaVu Sans Mono", Menlo, "DejaVu Sans Mono", "Noto Sans SC Clean", monospace;
  font-size: .87em; background: #f2f4f7; padding: .08em .3em; border-radius: 3px;
}
pre {
  background: #f7f8fa; border: 1px solid var(--rule); border-left: 3px solid var(--accent);
  padding: .7em .9em; overflow-x: auto; font-size: 8.8pt; line-height: 1.42;
  break-inside: avoid; page-break-inside: avoid;
}
pre code { background: none; padding: 0; font-size: inherit; }
blockquote {
  margin: 1em 0; padding: .5em 0 .5em 1em; border-left: 3px solid var(--rule);
  color: var(--muted); break-inside: avoid;
}
blockquote p { text-align: left; }
table {
  border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 9pt;
  break-inside: avoid; page-break-inside: avoid;
}
th, td { border: 1px solid var(--rule); padding: .34em .5em; text-align: left; vertical-align: top; }
th { background: #eef1f5; font-family: "Source Sans Pro", Arial, "DejaVu Sans", "Noto Sans SC Clean", sans-serif; font-weight: 600; }
tbody tr:nth-child(even) { background: #fafbfc; }
ul, ol { margin: 0 0 .8em; padding-left: 1.5em; }
li { margin-bottom: .28em; }
hr { border: none; border-top: 1px solid var(--rule); margin: 1.8em 0; }
figure { margin: 1.3em 0; text-align: center; break-inside: avoid; page-break-inside: avoid; }
figure.diagram { margin: 1.5em 0 1em; }
/* A tall diagram must fit ONE page or it is silently clipped at the page
   break, losing its bottom row. A4 printable height is ~259mm; cap below it. */
svg.mermaid-svg {
  max-width: 100%; max-height: 232mm; width: auto; height: auto;
  display: block; margin: 0 auto;
}
/* Mermaid labels are HTML in foreignObject, so they inherit body justification
   and come out with stretched word gaps. Override inside the diagram only. */
svg.mermaid-svg foreignObject div,
svg.mermaid-svg foreignObject span,
svg.mermaid-svg foreignObject p { text-align: center !important; }
/* CJK in diagram labels must reach the CJK font by name, not system fallback: the fallback path writes Kangxi-radical code points into the PDF text layer. */
svg.mermaid-svg text, svg.mermaid-svg tspan, svg.mermaid-svg foreignObject, svg.mermaid-svg foreignObject * { font-family: "trebuchet ms", verdana, arial, "DejaVu Sans", "Noto Sans SC Clean", sans-serif !important; }
figure img { max-width: 100%; height: auto; border: 1px solid var(--rule); }
figcaption {
  font-family: "Source Sans Pro", Arial, "DejaVu Sans", "Noto Sans SC Clean", sans-serif; font-size: 8.8pt;
  color: var(--muted); margin-top: .45em;
}
.missing-figure { color: #b00; font-style: italic; }
.banner {
  font-family: "Source Sans Pro", Arial, "DejaVu Sans", "Noto Sans SC Clean", sans-serif; font-size: 9pt; line-height: 1.5;
  background: #fff8e6; border: 1px solid #e3cf9a; border-left: 4px solid #c9a227;
  padding: .8em 1em; margin: 0 0 2em; color: #4a3c10; break-inside: avoid;
}
.banner strong { color: #3a2f08; }
@media print {
  body { max-width: none; padding: 0; font-size: 10pt; }
  .banner { background: #fff; }
  a { color: var(--ink); }
}
"""


def _require_mermaid_ready():
    """--require-mermaid preflight: renderer, interpreter and pinned bundle must be usable."""
    import importlib.util
    if not (_VENV_PY.is_file() and _RENDERER.is_file()):
        raise MermaidRequired(f'mermaid renderer unavailable ({_VENV_PY} / {_RENDERER})')
    spec = importlib.util.spec_from_file_location('_mermaid_to_svg_preflight', _RENDERER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        mod.check_bundle()
    except SystemExit as e:  # check_bundle exits with the message naming the cause
        raise MermaidRequired(str(e.code)) from None


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    strict = '--require-mermaid' in sys.argv
    banner = ''
    if '--banner' in sys.argv:
        banner = f'<div class="banner">{sys.argv[sys.argv.index("--banner") + 1]}</div>'
    cache = Path(sys.argv[sys.argv.index('--mermaid-cache') + 1]) \
        if '--mermaid-cache' in sys.argv else dst.parent / '.diagram-cache'
    done = False
    try:
        try:
            if strict:
                _require_mermaid_ready()
            body = convert(src.read_text(encoding='utf-8'), src.parent, cache, strict)
        except MermaidRequired as e:
            raise SystemExit(f'--require-mermaid: {e}')
        title = 'ENGRAM — Epistemic Identity'
        dst.write_text(
            f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title}</title>\n<style>{CSS}</style>\n</head>\n<body>\n'
            f'{banner}\n{body}\n</body>\n</html>\n', encoding='utf-8')
        done = True
    finally:
        if strict and not done:
            dst.unlink(missing_ok=True)  # any failure: never leave a stale or partial output
    print(f'{dst}  ({dst.stat().st_size / 1024:.0f} KB)')


if __name__ == '__main__':
    main()
