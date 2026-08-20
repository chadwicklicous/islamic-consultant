#!/usr/bin/env python3
"""Extract citation-tagged entries from Ghazali's Ihya (Sufi layer).

The Ihya is prose organized as books (كتاب) with chapters (الباب/الفصل).
We chunk each page into paragraphs and tag each with:
  "Ihya Ulum al-Din | <book> | sufi"

Output: text/sufi.tsv  — one paragraph per line:  CITATION\tTEXT
"""
import os, json, re

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_SUFI = os.path.join(BASE, 'raw', 'sufi')
TXT = os.path.join(BASE, 'text')
os.makedirs(TXT, exist_ok=True)

PREFIX = 'إحياء علوم الدين'


def book_name(title):
    """Extract the book name from a page title like 'إحياء علوم الدين/كتاب العلم/الباب الأول'."""
    parts = title.split('/')
    if len(parts) >= 2:
        book = parts[1].replace('كتاب ', '').strip()
        return book
    return 'مقدمة'


def chunk_text(text, max_chars=1200):
    """Split text into paragraphs, merging short ones up to max_chars."""
    # Split on newlines / sentence boundaries
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
    with open(os.path.join(RAW_SUFI, 'ihya.json'), encoding='utf-8') as f:
        data = json.load(f)

    total = 0
    with open(os.path.join(TXT, 'sufi.tsv'), 'w', encoding='utf-8') as out:
        for title in sorted(data.keys()):
            text = data[title]
            if not text.strip():
                continue
            book = book_name(title)
            for chunk in chunk_text(text):
                citation = f'Ihya Ulum al-Din | {book} | sufi'
                out.write(f'{citation}\t{chunk}\n')
                total += 1
    print(f'Extracted {total} sufi entries')


if __name__ == '__main__':
    main()
