#!/usr/bin/env python3
"""Re-fetch missing tafsir verses for authorities that were rate-limited.

Fills gaps in raw/tafsir/<slug>.json so every authority has all 6,236 verses.
"""
import os, json, time, urllib.request, urllib.error, re

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_TAFSIR = os.path.join(BASE, 'raw', 'tafsir')
API = 'https://api.qurancdn.com/api/qdc'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'

RESOURCE_IDS = {
    'ibn-kathir': 14, 'al-tabari': 15, 'al-qurtubi': 90, 'al-baghawi': 94,
    'al-sadi': 91, 'al-wasit': 93, 'al-muyassar': 16,
}

VERSES_PER_SURAH = {
    1:7, 2:286, 3:200, 4:176, 5:120, 6:165, 7:206, 8:75, 9:129, 10:109,
    11:123, 12:111, 13:43, 14:52, 15:99, 16:128, 17:111, 18:110, 19:98, 20:135,
    21:112, 22:78, 23:118, 24:64, 25:77, 26:227, 27:93, 28:88, 29:69, 30:60,
    31:34, 32:30, 33:73, 34:54, 35:45, 36:83, 37:182, 38:88, 39:75, 40:85,
    41:54, 42:53, 43:89, 44:59, 45:37, 46:35, 47:38, 48:29, 49:18, 50:45,
    51:60, 52:49, 53:62, 54:55, 55:78, 56:96, 57:29, 58:22, 59:24, 60:13,
    61:14, 62:11, 63:11, 64:18, 65:12, 66:12, 67:30, 68:52, 69:52, 70:44,
    71:28, 72:28, 73:20, 74:56, 75:40, 76:31, 77:50, 78:40, 79:46, 80:42,
    81:29, 82:19, 83:36, 84:25, 85:22, 86:17, 87:19, 88:26, 89:30, 90:20,
    91:15, 92:21, 93:11, 94:8, 95:8, 96:19, 97:5, 98:8, 99:8, 100:11,
    101:11, 102:8, 103:3, 104:9, 105:5, 106:4, 107:7, 108:3, 109:6, 110:3,
    111:5, 112:4, 113:5, 114:6,
}

UA_HEADERS = {'User-Agent': UA}


def fetch(url, retries=5):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA_HEADERS)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(3 * (attempt + 1))


def strip_html(text):
    if not text:
        return ''
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&quot;', '"').replace('&amp;', '&').replace('&#39;', "'").replace('&lt;', '<').replace('&gt;', '>')
    return ' '.join(text.split())


def repair(slug):
    out = os.path.join(RAW_TAFSIR, f'{slug}.json')
    with open(out, encoding='utf-8') as f:
        data = json.load(f)
    rid = RESOURCE_IDS[slug]
    missing = []
    for surah in range(1, 115):
        for ayah in range(1, VERSES_PER_SURAH[surah] + 1):
            key = f'{surah}:{ayah}'
            if key not in data:
                missing.append(key)
    if not missing:
        print(f"{slug}: complete ({len(data)} verses)")
        return
    print(f"{slug}: repairing {len(missing)} missing verses...")
    for key in missing:
        url = f'{API}/tafsirs/{rid}/by_ayah/{key}'
        try:
            resp = json.loads(fetch(url).decode('utf-8'))
            text = strip_html(resp['tafsir'].get('text', ''))
            if text:
                data[key] = text
        except Exception as e:
            print(f"  FAIL {key}: {e}")
        time.sleep(0.1)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"{slug}: now {len(data)} verses")


def main():
    for slug in ['ibn-kathir', 'al-tabari', 'al-sadi']:
        repair(slug)


if __name__ == '__main__':
    main()
