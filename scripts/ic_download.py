#!/usr/bin/env python3
"""Download the Quran (Arabic) and Hadith collections (Arabic).

Sources:
  - Quran: CheeseWithSauce/TheHolyQuranJSONFormat (per-surah files, Uthmani script)
  - Hadith: CheeseWithSauce/HadithsJSONFormat (16 collections, Arabic + grading)

Output:
  raw/quran/*.json    (114 surah files)
  raw/hadith/*.json   (per-collection book files)

Resumable: skips files already downloaded.
"""
import os, time, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_QURAN = os.path.join(BASE, 'raw', 'quran')
RAW_HADITH = os.path.join(BASE, 'raw', 'hadith')
os.makedirs(RAW_QURAN, exist_ok=True)
os.makedirs(RAW_HADITH, exist_ok=True)

QURAN_BASE = 'https://raw.githubusercontent.com/CheeseWithSauce/TheHolyQuranJSONFormat/main/surahs'
HADITH_BASE = 'https://raw.githubusercontent.com/CheeseWithSauce/HadithsJSONFormat/main/Sunnah'

# Hadith collections (the Six Books + Muwatta Malik + extras)
HADITH_COLLECTIONS = [
    'bukhari', 'muslim', 'abudawud', 'tirmidhi', 'nasai', 'ibnmajah',
    'malik', 'riyadussalihin', 'adab', 'bulugh', 'darimi', 'forty',
    'hisn', 'mishkat', 'shamail',
]

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'


def fetch(url, retries=4):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(2 * (attempt + 1))


def download_quran():
    ok, fail = 0, 0
    for n in range(1, 115):
        fname = f'{n:03d}.json'
        out = os.path.join(RAW_QURAN, fname)
        if os.path.exists(out) and os.path.getsize(out) > 100:
            ok += 1
            continue
        url = f'{QURAN_BASE}/{fname}'
        try:
            data = fetch(url)
            with open(out, 'wb') as f:
                f.write(data)
            ok += 1
        except Exception as e:
            fail += 1
            print(f"FAIL quran {fname}: {e}")
        time.sleep(0.05)
    print(f"Quran: ok={ok}, fail={fail}, total=114")
    return ok, fail


def download_hadith():
    ok, fail = 0, 0
    import subprocess, tempfile, shutil

    tmp = tempfile.mkdtemp(prefix='hadith_tree_')
    try:
        subprocess.run(
            ['git', 'clone', '--depth', '1',
             'https://github.com/CheeseWithSauce/HadithsJSONFormat.git', tmp],
            check=True, capture_output=True, timeout=180)
        for coll in HADITH_COLLECTIONS:
            coll_dir = os.path.join(tmp, 'Sunnah', coll)
            if not os.path.isdir(coll_dir):
                print(f"SKIP collection {coll} (not found)")
                continue
            for fname in sorted(os.listdir(coll_dir)):
                if not fname.endswith('.json'):
                    continue
                out = os.path.join(RAW_HADITH, f'{coll}__{fname}')
                if os.path.exists(out) and os.path.getsize(out) > 100:
                    ok += 1
                    continue
                shutil.copy2(os.path.join(coll_dir, fname), out)
                ok += 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"Hadith: ok={ok}, fail={fail}")
    return ok, fail


def main():
    q_ok, q_fail = download_quran()
    h_ok, h_fail = download_hadith()
    print(f"DONE: quran ok={q_ok} fail={q_fail}; hadith ok={h_ok} fail={h_fail}")


if __name__ == '__main__':
    main()
