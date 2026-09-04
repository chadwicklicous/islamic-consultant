#!/usr/bin/env python3
"""Extract citation-tagged entries from Musnad Ahmad (OpenITI mARkdown).

Parses the OpenITI mARkdown of Ahmad ibn Hanbal's *Musnad* (Shu'ayb al-Arna'ut
critical edition, Mu'assasat al-Risala 1421/2001, Shamela_0025794) into
citation-tagged segments:

  "Musnad Ahmad | <section> | <hadith number>"

Structure conventions (OpenITI mARkdown) — same as ic_extract_sira.py:
  - #META# ... #META#Header#End#  -> metadata block (skip)
  - ### | <title>                  -> top-level section heading (companion)
  - ### || <title>                 -> subsection heading
  - ### ||| <title>                -> sub-subsection (individual companion)
  - # N - <text>                   -> numbered hadith start (continuous numbering
                                       across the whole Musnad, Arna'ut edition)
  - # <text> / ~~<text>            -> paragraph / continuation lines
  - PageV01P001                    -> page marker (strip EVERYWHERE)
  - ms0001                         -> manuscript marker (strip)

Output: text/musnad.tsv — one hadith per line:  CITATION\tTEXT
Classification: canonical (Musnad Ahmad is one of the great canonical musnads;
the Arna'ut edition grades each chain). Citation carries the hadith number so
individual hadiths (e.g. 3788) are directly addressable.
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw', 'musnad', 'ibn_hanbal_musnad.mARkdown')
TXT = os.path.join(BASE, 'text')
os.makedirs(TXT, exist_ok=True)

PAGE_RE = re.compile(r'PageV\d+P\d+')
MS_RE = re.compile(r'ms\d+')
HADITH_RE = re.compile(r'^#\s*(\d+)\s*-\s*(.*)$')


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


def parse_hadiths():
    """Yield (section_path, hadith_number, text) from the mARkdown."""
    sections = []  # stack of section titles
    current = None  # (number, [lines])
    in_meta = True

    def flush():
        nonlocal current
        if current:
            num, lines = current
            text = ' '.join(l for l in lines if l).strip()
            if text:
                yield (' | '.join(s for s in sections if s), num, text)
            current = None

    with open(RAW, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if in_meta:
                if line.strip() == '#META#Header#End#':
                    in_meta = False
                continue
            stripped = line.strip()
            if stripped.startswith('###'):
                # flush current hadith before switching section
                for item in flush():
                    yield item
                # heading depth: ### | -> level 1, ### || -> level 2, etc.
                m = re.match(r'^#+\s*(\|*)\s*(.*)$', stripped)
                depth = len(m.group(1)) if m else 1
                title = m.group(2).strip(' :') if m else ''
                # rebuild section stack to depth
                sections = sections[:depth]
                if title:
                    sections.append(title)
                continue
            m = HADITH_RE.match(stripped)
            if m:
                for item in flush():
                    yield item
                current = (int(m.group(1)), [clean_line(m.group(2))])
                continue
            cleaned = clean_line(line)
            if cleaned and current:
                current[1].append(cleaned)

    for item in flush():
        yield item


def main():
    total = 0
    with open(os.path.join(TXT, 'musnad.tsv'), 'w', encoding='utf-8') as out:
        for section, num, text in parse_hadiths():
            citation = f'Musnad Ahmad | {section} | {num}'
            out.write(f'{citation}\t{text}\n')
            total += 1
    print(f'Extracted {total} musnad hadiths')


if __name__ == '__main__':
    main()
