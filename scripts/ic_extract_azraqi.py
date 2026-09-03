#!/usr/bin/env python3
"""Extract citation-tagged entries from al-Azraqi's Akhbar Makka (OpenITI mARkdown).

Parses the OpenITI mARkdown of al-Azraqi's *Akhbar Makka wa-ma ja'a fiha min
al-athar* (Rushdi al-Salih Malhas ed., Shamela_0009621 / #0249.IbnCabdAllahAzraqi.AkhbarMakka)
into citation-tagged segments:

  "Akhbar Makka | <section> | historical:da'if"

Structure conventions (OpenITI mARkdown) — same as ic_extract_sira.py:
  - #META# ... #META#Header#End#  -> metadata block (skip)
  - ### | <title>                  -> top-level section heading
  - # <text>                       -> paragraph line (strip leading '# ')
  - ~~<text>                       -> continuation line (strip leading '~~')
  - PageV01P001                    -> page marker (strip EVERYWHERE, not just standalone)

Output: text/azraqi.tsv — one chunk per line:  CITATION\tTEXT
Classification: historical (da'if source-class), like the Sira and Tabaqat
layers — context for the Prophet's and Mecca's history, NOT a canonical hadith
corpus. Carry the same 'historical:da'if' suffix for source-class consistency.
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw', 'makka', 'azraqi.mARkdown')
TXT = os.path.join(BASE, 'text')
os.makedirs(TXT, exist_ok=True)

PAGE_RE = re.compile(r'PageV\d+P\d+')
MS_RE = re.compile(r'\bms\d+\b')
TITLEBAR_RE = re.compile(r'^#+ *')


def clean_line(line):
    """Strip OpenITI line prefixes and page/marker tokens."""
    line = line.strip()
    if line.startswith('~~'):
        line = line[2:].strip()
    elif line.startswith('#'):
        line = line[1:].strip()
    line = PAGE_RE.sub('', line)
    line = MS_RE.sub('', line)
    return line.strip()


def parse_sections():
    """Yield (section_title, [paragraphs]) from the mARkdown."""
    sections = []
    current_title = 'مقدمة'
    current_paras = []
    in_meta = True

    with open(RAW, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if in_meta:
                if line.strip() == '#META#Header#End#':
                    in_meta = False
                continue
            if line.strip().startswith('###'):
                # flush previous section
                if current_paras:
                    sections.append((current_title, current_paras))
                title = line.strip()
                title = TITLEBAR_RE.sub('', title)
                title = re.sub(r'^\|+\s*', '', title).strip(' :')
                current_title = title
                current_paras = []
                continue
            cleaned = clean_line(line)
            if cleaned:
                current_paras.append(cleaned)

    if current_paras:
        sections.append((current_title, current_paras))
    return sections


def chunk_paras(paras, max_chars=1200):
    """Group paragraphs into chunks <= max_chars."""
    chunks = []
    current = ''
    for p in paras:
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
    sections = parse_sections()
    total = 0
    with open(os.path.join(TXT, 'azraqi.tsv'), 'w', encoding='utf-8') as out:
        for title, paras in sections:
            for chunk in chunk_paras(paras):
                citation = f'Akhbar Makka | {title} | historical:da\'if'
                out.write(f'{citation}\t{chunk}\n')
                total += 1
    print(f'Extracted {total} akhbar-makka entries from {len(sections)} sections')


if __name__ == '__main__':
    main()
