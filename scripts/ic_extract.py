#!/usr/bin/env python3
"""Extract citation-tagged verses/hadiths from Quran and Hadith JSON.

Output: text/<source>.tsv  — one entry per line:  CITATION\tTEXT

Quran:  "Quran 2:255"  (surah:ayah)
Hadith: "Sahih al-Bukhari 1"  (collection + hadith number)
"""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_QURAN = os.path.join(BASE, 'raw', 'quran')
RAW_HADITH = os.path.join(BASE, 'raw', 'hadith')
TXT = os.path.join(BASE, 'text')
os.makedirs(TXT, exist_ok=True)

# Collection code -> display name
COLLECTION_NAMES = {
    'bukhari': 'Sahih al-Bukhari',
    'muslim': 'Sahih Muslim',
    'abudawud': 'Sunan Abu Dawud',
    'tirmidhi': 'Jami at-Tirmidhi',
    'nasai': 'Sunan an-Nasai',
    'ibnmajah': 'Sunan Ibn Majah',
    'malik': 'Muwatta Malik',
    'riyadussalihin': 'Riyad as-Salihin',
    'adab': 'Al-Adab al-Mufrad',
    'bulugh': 'Bulugh al-Maram',
    'darimi': 'Sunan ad-Darimi',
    'forty': 'Forty Hadith (an-Nawawi)',
    'hisn': 'Hisn al-Muslim',
    'mishkat': 'Mishkat al-Masabih',
    'shamail': 'Shamail Muhammadiyah',
}


def extract_quran():
    """Extract verses from per-surah Quran files."""
    verses = []
    for fname in sorted(os.listdir(RAW_QURAN)):
        if not fname.endswith('.json'):
            continue
        path = os.path.join(RAW_QURAN, fname)
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        for v in data.get('verses', []):
            surah = v.get('surah')
            ayah = v.get('ayah')
            text = v.get('text_ar', '').strip()
            if text and surah and ayah:
                verses.append((f'Quran {surah}:{ayah}', text))
    return verses


def extract_hadith():
    """Extract hadiths from per-collection book files."""
    hadiths = []
    for fname in sorted(os.listdir(RAW_HADITH)):
        if not fname.endswith('.json'):
            continue
        # filename is like "bukhari__001_revelation.json"
        coll_code = fname.split('__')[0]
        coll_name = COLLECTION_NAMES.get(coll_code, coll_code)
        path = os.path.join(RAW_HADITH, fname)
        with open(path, encoding='utf-8-sig') as f:
            data = json.load(f)
        # data is a list of hadith objects
        if isinstance(data, dict):
            data = [data]
        for h in data:
            if not isinstance(h, dict):
                continue
            text = h.get('arabic', '').strip()
            if not text:
                continue
            # Build citation: collection + hadith number (from reference or id)
            ref = h.get('reference', '')
            # Try to extract the hadith number from the reference
            import re
            m = re.search(r'(\d+)', ref)
            num = m.group(1) if m else str(h.get('id', ''))
            hadiths.append((f'{coll_name} {num}', text))
    return hadiths


def main():
    quran = extract_quran()
    hadith = extract_hadith()

    with open(os.path.join(TXT, 'quran.tsv'), 'w', encoding='utf-8') as f:
        for cit, text in quran:
            f.write(f'{cit}\t{text}\n')

    with open(os.path.join(TXT, 'hadith.tsv'), 'w', encoding='utf-8') as f:
        for cit, text in hadith:
            f.write(f'{cit}\t{text}\n')

    print(f'Extracted {len(quran)} Quran verses + {len(hadith)} hadiths')


if __name__ == '__main__':
    main()
