#!/usr/bin/env python3
"""Download Ghazali's Ihya Ulum al-Din (Sufi) from ar.wikisource.

Uses the MediaWiki API to fetch clean plain-text extracts of each subpage.
The full work is 105 subpages (books + their chapters/babs).

Output: raw/sufi/ihya.json  — { "page_title": "text" }

Resumable: skips pages already fetched.
"""
import os, json, time, urllib.request, urllib.error, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_SUFI = os.path.join(BASE, 'raw', 'sufi')
os.makedirs(RAW_SUFI, exist_ok=True)

WIKI = 'https://ar.wikisource.org/w/api.php'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
PREFIX = 'إحياء علوم الدين'


def api_get(params, retries=4):
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
            time.sleep(2 * (attempt + 1))


def get_all_pages():
    """Get all subpage titles under the Ihya prefix."""
    pages = []
    apcontinue = None
    while True:
        params = {
            'action': 'query', 'list': 'allpages',
            'apprefix': PREFIX, 'aplimit': '500',
        }
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
    """Get clean plain-text extract of a page."""
    d = api_get({
        'action': 'query', 'prop': 'extracts',
        'explaintext': '1', 'exlimit': '1',
        'titles': title,
    })
    pages = d['query']['pages']
    for pid, p in pages.items():
        return p.get('extract', '')
    return ''


def main():
    out = os.path.join(RAW_SUFI, 'ihya.json')
    data = {}
    if os.path.exists(out):
        with open(out, encoding='utf-8') as f:
            data = json.load(f)

    pages = get_all_pages()
    print(f"Total Ihya subpages: {len(pages)}")

    for i, title in enumerate(pages):
        if title in data and data[title]:
            continue
        try:
            text = get_page_text(title)
            if text:
                data[title] = text
        except Exception as e:
            print(f"FAIL {title}: {e}")
        if (i + 1) % 20 == 0:
            with open(out, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
            print(f"  saved {len(data)}/{len(pages)}")
        time.sleep(0.1)

    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"DONE: {len(data)} pages saved")


if __name__ == '__main__':
    main()
