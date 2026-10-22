#!/usr/bin/env python3
"""Render a Mermaid diagram to standalone SVG using Playwright's Chromium.

Why not mermaid-cli: it pulls Puppeteer and its own Chromium (~150MB) and the
npx install timed out at 7 minutes on this seat. This seat already has
Playwright's Chromium and the ENGRAM venv's playwright bindings, so the only
thing actually needed is Mermaid's browser bundle — vendored beside this file.

Run with a python that has the playwright bindings:
    python mermaid_to_svg.py <in.mmd> <out.svg>

The bundle is NOT committed (3.5 MB). It is pinned: mermaid 11.17.2, sha256 below.
See README.md in this directory for how to fetch it. Playwright is imported lazily,
after the bundle check, so a missing bundle fails with a clear message first.
"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent / 'vendor' / 'mermaid.min.js'
BUNDLE_VERSION = '11.17.2'
BUNDLE_SHA256 = '581ed7d74bd9048d0e3a91363927d72ef22942d7722546b27f7cc29e35390eb8'
BUNDLE_URL = f'https://cdn.jsdelivr.net/npm/mermaid@{BUNDLE_VERSION}/dist/mermaid.min.js'


def check_bundle(path=BUNDLE):
    """Exit with a clear message unless `path` is the pinned mermaid bundle."""
    path = Path(path)
    if not path.is_file():
        raise SystemExit(f'mermaid bundle missing: {path}\n'
                         f'  expected mermaid {BUNDLE_VERSION}, sha256 {BUNDLE_SHA256}\n'
                         f'  fetch with: mkdir -p {path.parent} && curl -sSL -o {path} {BUNDLE_URL}')
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    if got != BUNDLE_SHA256:
        raise SystemExit(f'mermaid bundle sha256 mismatch: {path}\n'
                         f'  expected {BUNDLE_SHA256} (mermaid {BUNDLE_VERSION})\n'
                         f'  got      {got}\n'
                         f'  refetch with: curl -sSL -o {path} {BUNDLE_URL}')

HARNESS = """<!DOCTYPE html><html><head><meta charset="utf-8">
<script src="mermaid.min.js"></script>
<style>body{margin:0;background:transparent;font-family:"Source Sans Pro",Arial,sans-serif}</style>
</head><body><div id="out"></div><script>
window.__done = false; window.__err = null;
(async () => {
  try {
    mermaid.initialize({
      startOnLoad: false, theme: 'base', securityLevel: 'loose',
      flowchart: { htmlLabels: true, curve: 'basis', useMaxWidth: true },
      themeVariables: {
        fontFamily: '"Source Sans Pro", Arial, sans-serif', fontSize: '14px',
        primaryColor: '#f4f7fa', primaryTextColor: '#16181d',
        primaryBorderColor: '#2f4f7f', lineColor: '#5b6270',
        secondaryColor: '#eef1f5', tertiaryColor: '#fafbfc',
      },
    });
    const { svg } = await mermaid.render('theDiagram', window.__SRC);
    document.getElementById('out').innerHTML = svg;
    window.__svg = svg;
  } catch (e) { window.__err = String(e && e.message || e); }
  window.__done = true;
})();
</script></body></html>
"""


def render(code):
    check_bundle(BUNDLE)
    from playwright.sync_api import sync_playwright
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / 'mermaid.min.js').write_bytes(BUNDLE.read_bytes())
        (td / 'h.html').write_text(HARNESS, encoding='utf-8')
        with sync_playwright() as p:
            b = p.chromium.launch(args=['--no-sandbox', '--disable-dev-shm-usage'])
            pg = b.new_page(viewport={'width': 1400, 'height': 1200})
            pg.add_init_script('window.__SRC = ' + json.dumps(code) + ';')
            pg.goto((td / 'h.html').as_uri())
            pg.wait_for_function('window.__done === true', timeout=60000)
            err = pg.evaluate('window.__err')
            if err:
                b.close()
                raise SystemExit(f'mermaid render error: {err}')
            svg = pg.evaluate('window.__svg')
            b.close()
    return svg


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    svg = render(src.read_text(encoding='utf-8'))
    dst.write_text(svg, encoding='utf-8')
    print(f'{dst}  ({len(svg)} bytes)')


if __name__ == '__main__':
    main()
