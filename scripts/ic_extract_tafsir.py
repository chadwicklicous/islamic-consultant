#!/usr/bin/env python3
"""Extract citation-tagged tafsir entries from the downloaded tafsir JSON.

Each entry becomes a line in text/tafsir.tsv:
  CITATION\tTEXT
where CITATION encodes the verse + authority + layer so the vector store can
filter by authority.

Citation format:
  "Quran 4:3 | Ibn Kathir | classical-sunni"
  "Quran 4:3 | al-Sa'di | modern-sunni"
"""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_TAFSIR = os.path.join(BASE, 'raw', 'tafsir')
TXT = os.path.join(BASE, 'text')
os.makedirs(TXT, exist_ok=True)

# slug -> (authority, layer)
AUTHORITY_META = {
    'ibn-kathir': ('Ibn Kathir', 'classical-sunni'),
    'al-tabari': ('al-Tabari', 'classical-sunni'),
    'al-qurtubi': ('al-Qurtubi', 'classical-sunni'),
    'al-baghawi': ('al-Baghawi', 'classical-sunni'),
    'al-sadi': ('al-Sa\'di', 'modern-sunni'),
    'al-wasit': ('al-Wasit (Tantawi)', 'modern-sunni'),
    'al-muyassar': ('al-Muyassar', 'modern-sunni'),
}


def main():
    total = 0
    with open(os.path.join(TXT, 'tafsir.tsv'), 'w', encoding='utf-8') as out:
        for slug in sorted(os.listdir(RAW_TAFSIR)):
            if not slug.endswith('.json'):
                continue
            path = os.path.join(RAW_TAFSIR, slug)
            authority, layer = AUTHORITY_META.get(slug.replace('.json', ''), (slug, 'unknown'))
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
            for verse_key, text in sorted(data.items()):
                if text.strip():
                    citation = f'Quran {verse_key} | {authority} | {layer}'
                    out.write(f'{citation}\t{text}\n')
                    total += 1
    print(f'Extracted {total} tafsir entries')


if __name__ == '__main__':
    main()
