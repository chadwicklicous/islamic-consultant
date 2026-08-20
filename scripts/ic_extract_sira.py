#!/usr/bin/env python3
"""Extract citation-tagged entries from Ibn Hisham's Sira (biography of Muhammad).

The Sira is the "exemplar" layer — how believers read the Quran through the
Prophet's life. Each page is chunked into paragraphs and tagged:
  "Sira Ibn Hisham | <section> | sira"

Output: text/sira.tsv  — one paragraph per line:  CITATION\tTEXT
"""
import os, json, re

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_SIRA = os.path.join(BASE, 'raw', 'sira')
TXT = os.path.join(BASE, 'text')
os.makedirs(TXT, exist_ok=True)

PREFIX = 'سيرة ابن هشام'


def section_name(title):
    """Extract the section name from a page title like 'سيرة ابن هشام/المجلد الأول/أصل العرب'."""
    parts = title.split('/')
    if len(parts) >= 3:
        return parts[2].strip()
    if len(parts) == 2:
        return parts[1].strip()
    return 'مقدمة'


def chunk_text(text, max_chars=1200):
    raw_paras = [p.strip() for p in re.split(r'\n+', text) if p.strip()]
    chunks = []
    current = ''
    for p in raw_paras:
        if len(current) + len(p) + 1 <= max_chars:
            current = (current + ' ' + p).strip()
        else:
            if current:
                chunks.append(current)
            current = p
    if current:
        chunks.append(current)
    return chunks


def main():
    with open(os.path.join(RAW_SIRA, 'sira.json'), encoding='utf-8') as f:
        data = json.load(f)

    total = 0
    with open(os.path.join(TXT, 'sira.tsv'), 'w', encoding='utf-8') as out:
        for title in sorted(data.keys()):
            text = data[title]
            if not text.strip():
                continue
            section = section_name(title)
            for chunk in chunk_text(text):
                citation = f'Sira Ibn Hisham | {section} | sira'
                out.write(f'{citation}\t{chunk}\n')
                total += 1
    print(f'Extracted {total} sira entries')


if __name__ == '__main__':
    main()
