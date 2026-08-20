#!/usr/bin/env python3
"""Convert the Islamic corpus TSV files to PDFs with proper Arabic RTL rendering.

Uses Playwright + headless Chromium to render HTML (which handles Arabic
shaping and RTL correctly) to PDF. Each file is paginated; large files are
split into multiple PDF parts to keep each under 200MB.

Output: pdf/<name>.pdf  (or pdf/<name>_part1.pdf, _part2.pdf, ... for large files)
"""
import os, html, math, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))
TEXT_DIR = os.path.join(BASE, 'text')
PDF_DIR = os.path.join(BASE, 'pdf')
os.makedirs(PDF_DIR, exist_ok=True)

# Max entries per PDF part (tune to keep each PDF under 200MB)
# Rough: each entry ~2KB rendered; 200MB / 2KB = ~100k entries, but be safe.
MAX_ENTRIES_PER_PART = 20000

FILES = [
    ('quran.tsv', 'Quran'),
    ('hadith.tsv', 'Hadith'),
    ('tafsir.tsv', 'Tafsir'),
    ('sufi.tsv', 'Sufi (Ghazali Ihya)'),
]


def build_html(title, entries):
    """Build an HTML document with RTL Arabic text from (citation, text) entries."""
    rows = []
    for cit, text in entries:
        rows.append(
            f'<div class="entry"><span class="cit">{html.escape(cit)}</span>'
            f'<span class="txt">{html.escape(text)}</span></div>'
        )
    body = '\n'.join(rows)
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<style>
  @page {{ size: A4; margin: 1.5cm; }}
  body {{ font-family: 'Amiri', 'Scheherazade New', 'Traditional Arabic', serif;
         direction: rtl; text-align: right; font-size: 12pt; line-height: 1.6; }}
  h1 {{ text-align: center; font-size: 20pt; margin-bottom: 0.5cm; }}
  .entry {{ margin-bottom: 0.4cm; padding-bottom: 0.3cm; border-bottom: 1px solid #ddd; }}
  .cit {{ display: block; font-weight: bold; color: #333; font-size: 10pt; margin-bottom: 2px; }}
  .txt {{ display: block; }}
</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
{body}
</body>
</html>"""


def write_pdf(html_content, out_path):
    """Render HTML to PDF via Playwright + Chromium."""
    import asyncio
    from playwright.sync_api import sync_playwright

    # Write HTML to temp file
    tmp_html = os.path.join(PDF_DIR, '_tmp.html')
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('file://' + tmp_html.replace('\\', '/'))
        page.pdf(path=out_path, format='A4', print_background=True)
        browser.close()

    os.remove(tmp_html)


def main():
    for fname, label in FILES:
        path = os.path.join(TEXT_DIR, fname)
        if not os.path.exists(path):
            print(f"SKIP {fname} (not found)")
            continue

        # Read entries
        entries = []
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if '\t' not in line:
                    continue
                cit, text = line.split('\t', 1)
                if text.strip():
                    entries.append((cit.strip(), text.strip()))

        print(f"{fname}: {len(entries)} entries")

        # Split into parts
        n_parts = max(1, math.ceil(len(entries) / MAX_ENTRIES_PER_PART))
        for part in range(n_parts):
            start = part * MAX_ENTRIES_PER_PART
            end = min((part + 1) * MAX_ENTRIES_PER_PART, len(entries))
            part_entries = entries[start:end]

            if n_parts == 1:
                out = os.path.join(PDF_DIR, fname.replace('.tsv', '.pdf'))
                title = f"{label} — {len(entries)} entries"
            else:
                out = os.path.join(PDF_DIR, fname.replace('.tsv', f'_part{part+1}.pdf'))
                title = f"{label} (part {part+1}/{n_parts}) — {len(part_entries)} entries"

            print(f"  rendering part {part+1}/{n_parts} ({len(part_entries)} entries) -> {os.path.basename(out)}")
            html_content = build_html(title, part_entries)
            write_pdf(html_content, out)
            print(f"    done: {os.path.getsize(out)/1e6:.1f} MB")


if __name__ == '__main__':
    main()
