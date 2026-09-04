#!/usr/bin/env python3
"""Extract citation-tagged entries from Ibn Hisham's Sira (OpenITI mARkdown).

Parses the OpenITI mARkdown of Ibn Hisham's Sira Nabawiyya (the standard
Mustafa al-Saqqa edition, Shamela0023833) into citation-tagged segments:

  "Sira Ibn Hisham | <section> | sira"

Structure conventions (OpenITI mARkdown):
  - #META# ... #META#Header#End#  -> metadata block (skip)
  - ### | <title>                  -> top-level section heading
  - ### || <title>                 -> subsection heading
  - # <text>                       -> paragraph line (strip leading '# ')
  - ~~<text>                       -> continuation line (strip leading '~~')
  - PageV01P001                    -> page marker (strip)

Output: text/sira.tsv  — one paragraph per line:  CITATION\tTEXT
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw', 'sira', 'ibn_hisham_sira.mARkdown')
TXT = os.path.join(BASE, 'text')
os.makedirs(TXT, exist_ok=True)

PAGE_RE = re.compile(r'PageV\d+P\d+')
MS_RE = re.compile(r'\bms\d+\b')


def clean_line(line):
    """Strip OpenITI line prefixes and page markers."""
    line = line.strip()
    if line.startswith('~~'):
        line = line[2:].strip()
    elif line.startswith('#'):
        line = line[1:].strip()
    line = PAGE_RE.sub('', line)
    line = MS_RE.sub('', line)
    return line


def parse_sections():
    """Yield (section_title, [paragraphs]) from the mARkdown."""
    sections = []  # list of (title, [paras])
    current_title = 'مقدمة'
    current_paras = []
    in_meta = True

    with open(RAW, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            # skip metadata block
            if in_meta:
                if line.strip() == '#META#Header#End#':
                    in_meta = False
                continue
            # section heading
            if line.startswith('### '):
                # flush previous
                if current_paras:
                    sections.append((current_title, current_paras))
                title = line[4:].strip()
                # normalize: strip leading | or || markers
                title = re.sub(r'^\|+\s*', '', title)
                title = title.strip(' :')
                current_title = title
                current_paras = []
                continue
            # content line
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
    with open(os.path.join(TXT, 'sira.tsv'), 'w', encoding='utf-8') as out:
        for title, paras in sections:
            for chunk in chunk_paras(paras):
                citation = f'Sira Ibn Hisham | {title} | sira'
                out.write(f'{citation}\t{chunk}\n')
                total += 1
    print(f'Extracted {total} sira entries from {len(sections)} sections')


if __name__ == '__main__':
    main()
