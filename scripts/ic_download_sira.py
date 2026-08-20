#!/usr/bin/env python3
"""Download Ibn Hisham's Sira (biography of Muhammad) from ar.wikisource.

The Sira is the foundational biography of the Prophet — the "exemplar" layer
through which believers read the Quran. Uses the MediaWiki API for clean text.

Output: raw/sira/sira.json  — { "page_title": "text" }
"""
import os, json, time, urllib.request, urllib.error, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_SIRA = os.path.join(BASE, 'raw', 'sira')
os.makedirs(RAW_SIRA, exist_ok=True)

WIKI = 'https://ar.wikisource.org/w/api.php'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
PREFIX = 'سيرة ابن هشام'


def api_get(params, retries=5):
    params = dict(params)
    params['format'] = 'json'
    url = WIKI + '?' + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(3 * (attempt + 1))


def get_all_pages():
    pages = []
    apcontinue = None
    while True:
        params = {'action': 'query', 'list': 'allpages', 'apprefix': PREFIX, 'aplimit': '500'}
        if apcontinue:
            params['apcontinue'] = apcontinue
        d = api_get(params)
        for p in d['query']['allpages']:
            pages.append(p['title'])
        if 'continue' in d:
            apcontinue = d['continue'].get('apcontinue')
        else:
            break
    return pages


def get_page_text(title):
    d = api_get({'action': 'query', 'prop': 'extracts', 'explaintext': '1', 'exlimit': '1', 'titles': title})
    for pid, p in d['query']['pages'].items():
        return p.get('extract', '')
    return ''


def main():
    out = os.path.join(RAW_SIRA, 'sira.json')
    data = {}
    if os.path.exists(out):
        with open(out, encoding='utf-8') as f:
            data = json.load(f)

    pages = get_all_pages()
    print(f"Total Sira subpages: {len(pages)}")

    # Patient mode: long delay per page to avoid 429 rate limiting.
    # Resumable — each run fills whatever it can, and re-running later
    # completes the rest.
    for i, title in enumerate(pages):
        if title in data and data[title]:
            continue
        try:
            text = get_page_text(title)
            if text:
                data[title] = text
        except Exception as e:
            print(f"FAIL {title}: {e}")
        # Save progress every page so a rate-limited run isn't lost
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"  progress: {len(data)}/{len(pages)}")
        time.sleep(3.0)  # polite delay — ar.wikisource throttles aggressively

    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"DONE: {len(data)} pages saved")


if __name__ == '__main__':
    main()
