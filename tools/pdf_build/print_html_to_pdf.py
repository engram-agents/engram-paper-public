"""Print a self-contained HTML file to an A4 PDF with Playwright's Chromium.

Usage:  print_html_to_pdf.py <absolute/path/to/in.html> <out.pdf>

Playwright is imported lazily inside main(), so importing this module needs neither
Playwright nor a browser.
"""
import sys


def main():
    from playwright.sync_api import sync_playwright
    src, out = sys.argv[1], sys.argv[2]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + src, wait_until="networkidle")
        pg.pdf(path=out, format="A4", print_background=True, margin={"top":"18mm","bottom":"18mm","left":"16mm","right":"16mm"},
               display_header_footer=True, header_template="<span></span>",
               footer_template='<div style="font-size:8pt;width:100%;text-align:center;color:#666"><span class="pageNumber"></span> / <span class="totalPages"></span></div>')
        b.close()
    print("wrote", out)


if __name__ == '__main__':
    main()
