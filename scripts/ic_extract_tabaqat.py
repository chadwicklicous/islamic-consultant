#!/usr/bin/env python3
"""Extract citation-tagged entries from Ibn Sa'd's Tabaqat al-Kubra (OpenITI).

al-Tabaqat al-Kubra is Ibn Sa'd's foundational biographical dictionary of the
Prophet and his companions — a HISTORICAL source, NOT part of the canonical
hadith corpus (the Kutub al-Sittah). It gives context to the life of Muhammad
but is not authoritative for legal practice, and its chains are often da'if
(weak) by the canonical standard.

Each entry is tagged with the source class 'historical' and grade 'da'if'
(weight='context') via ic_grades.py, so the consultant can tell it apart from
canonical hadith.

Structure conventions (OpenITI mARkdown):
  - #META# ... #META#Header#End#  -> metadata block (skip)
  - ### $ <name>                  -> individual person entry
  - ### | <title>                 -> top-level narrative section
  - ### || <title>                -> subsection
  - # <text>                      -> paragraph line (strip leading '# ')
  - ~~<text>                      -> continuation line (strip leading '~~')
  - PageV\d+P\d+                  -> page marker (strip)
  - ms\d+                         -> manuscript marker (strip)

Output: text/tabaqat.tsv — one paragraph per line:  CITATION\tTEXT
Citation format preserves the grade:
  "Ibn Sa'd Tabaqat | <section/person> | historical:da'if"
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw', 'sira', 'ibn_sad_tabaqat.mARkdown')
TXT = os.path.join(BASE, 'text')
os.makedirs(TXT, exist_ok=True)

PAGE_RE = re.compile(r'PageV\d+P\d+')
MS_RE = re.compile(r'\bms\d+\b')
SRC_TAG = 'historical:da\'if'  # non-canonical, weak-by-default


def clean_line(line):
    line = line.strip()
    if line.startswith('~~'):
        line = line[2:].strip()
    elif line.startswith('#'):
        line = line[1:].strip()
    line = PAGE_RE.sub('', line)
    line = MS_RE.sub('', line)
    return line.strip()


def parse_entries():
    """Yield (citation_label, [paragraphs]) walking the mARkdown.

    Citation label is the current section (### |) or person (### $) heading.
    """
    entries = []
    current_label = 'مقدمة'
    current_paras = []
    in_meta = True

    with open(RAW, encoding='utf-8-sig') as f:
        for line in f:
            line = line.rstrip('\n')
            if in_meta:
                if '#META#Header#End#' in line:
                    in_meta = False
                continue
            if line.startswith('###'):
                if current_paras:
                    entries.append((current_label, current_paras))
                # heading text after ### $  (strip ms/PageV markers too)
                label = line[5:].strip()
                label = PAGE_RE.sub('', label)
                label = MS_RE.sub('', label)
                label = re.sub(r'^\$\s*|\|\s*|\|\|\s*|\|\|\|\s*', '', label)
                label = label.strip(' -').strip()
                current_label = label if label else 'مقدمة'
                current_paras = []
                continue
            if line.startswith('|PARATEXT|'):
                continue
            cleaned = clean_line(line)
            if cleaned:
                current_paras.append(cleaned)

    if current_paras:
        entries.append((current_label, current_paras))
    return entries


def chunk_paras(paras, max_chars=1400):
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
    entries = parse_entries()
    total = 0
    out_path = os.path.join(TXT, 'tabaqat.tsv')
    with open(out_path, 'w', encoding='utf-8') as out:
        for label, paras in entries:
            label_clean = label.split(' - ')[-1] if label else 'مقدمة'
            for chunk in chunk_paras(paras):
                citation = f'Ibn Sa\'d Tabaqat | {label_clean} | {SRC_TAG}'
                out.write(f'{citation}\t{chunk}\n')
                total += 1
    print(f'Extracted {total} tabaqat entries from {len(entries)} sections')


if __name__ == '__main__':
    main()
