#!/usr/bin/env python3
"""Islamic Consultant query interface with the Initiation Layer toggle.

For scholars who want the ORIGINAL Arabic text without bias or ideological
interpretation, with an OPTIONAL, toggleable layer showing how the initiated
(the tradition's own jurisprudential method) read the text.

Two modes (the design in deep-research/The_Initiation_Layer_Design.md):

  --mode text        (default) RAW retrieval only. Original Arabic + citation.
                     No interpretation, no gloss, no method. The ground truth.

  --mode initiated   RAW text + the INITIATION LAYER frame. Adds a clearly-
                     labeled methodological frame for each hit showing how the
                     tradition teaches the initiated to read it.

The initiation layer is ALWAYS labeled as the tradition's frame, never as the
text itself. The raw Arabic remains authoritative.

Usage:
  python ic_query.py --query "what does the quran say about wine" --k 5
  python ic_query.py --mode initiated --query "wine" --k 5
  python ic_query.py --frame naskh --query "alcohol"     # only the naskh frame

Frame flags (fine-grained toggles):
  --frame naskh      show the naskh (abrogation) time-index for the verses
  --frame asbab      show occasions of revelation where present in tafsir
  --frame qiyas      show the 'illa (ratio) and its analogical extensions
  --frame split      show where classical vs. modern tafsir diverge
  --frame network    show which node(s) / domains the verse connects to
With --mode initiated all five frames are shown. With --frame X only X shows.
"""

import os, sys, json, time, re, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
TXT = os.path.join(BASE, 'text')
CHROMA_DIR = os.path.join(BASE, 'chroma')
COLLECTION = 'islamic_corpus'
OLLAMA_URL = 'http://localhost:11434'
EMBED_MODEL = 'bge-m3'

# Which tafsir authorities count as classical vs. modern (for the --frame split)
CLASSICAL = ('al-Tabari', 'al-Qurtubi', 'al-Baghawi', 'Ibn Kathir')
MODERN = ('al-Sa\'di', 'al-Wasit', 'al-Muyassar')


def embed(texts):
    texts = [t[:6000] for t in texts]
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                f'{OLLAMA_URL}/api/embed',
                data=json.dumps({'model': EMBED_MODEL, 'input': texts}).encode(),
                headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())['embeddings']
        except urllib.error.HTTPError as e:
            if e.code == 400 and len(texts) > 1:
                mid = len(texts) // 2
                return embed(texts[:mid]) + embed(texts[mid:])
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def query(q, k=5):
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    col = client.get_collection(COLLECTION)
    vec = embed([q])[0]
    res = col.query(query_embeddings=[vec], n_results=k)
    return list(zip(res['metadatas'][0], res['documents'][0]))


def get_tafsir_for_verse(verse):
    """Grep tafsir.tsv for tafsir entries on a given verse citation, grouped by authority."""
    verse_clean = verse.split('|')[0].strip()  # e.g. 'Quran 5:90'
    results = []
    path = os.path.join(TXT, 'tafsir.tsv')
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if '\t' not in line:
                    continue
                cit, text = line.split('\t', 1)
                if cit.startswith(verse_clean + ' |'):
                    # cit like 'Quran 5:90 | al-Sa'di | modern-sunni'
                    parts = [p.strip() for p in cit.split('|')]
                    authority = parts[1] if len(parts) > 1 else '?'
                    results.append((authority, text.strip()))
    except FileNotFoundError:
        pass
    return results


def frame_naskh(tafsir_entries):
    """Naskh frame: does the tafsir record abrogation (ناسخ/منسوخ/نسخت) for this verse?"""
    naskh_terms = ['نسخ', 'منسوخ', 'ناسخ', 'نسخت']
    out = []
    for authority, text in tafsir_entries:
        if any(t in text for t in naskh_terms):
            # pull a short window around the first naskh mention
            idx = min([text.find(t) for t in naskh_terms if t in text] or [-1])
            snippet = text[max(0, idx-120):idx+220] if idx >= 0 else text[:220]
            out.append(f"  [{authority}] naskh noted: …{snippet}…")
    return out


def frame_asbab(tafsir_entries):
    """Asbab frame: does the tafsir record an occasion of revelation (سبب نزول)?"""
    out = []
    for authority, text in tafsir_entries:
        if 'سبب نزول' in text or 'نزلت' in text:
            idx = text.find('سبب نزول') if 'سبب نزول' in text else text.find('نزلت')
            snippet = text[max(0, idx-80):idx+280]
            out.append(f"  [{authority}] occasion: …{snippet}…")
    return out


def frame_qiyas(tafsir_entries):
    """Qiyas frame: does the recording extend the ruling by analogy (قياس)?"""
    out = []
    for authority, text in tafsir_entries:
        if 'قياس' in text or 'على القياس' in text or 'بمنزلة' in text:
            idx = min([text.find(x) for x in ['قياس', 'على القياس', 'بمنزلة'] if x in text] or [-1])
            snippet = text[max(0, idx-120):idx+240] if idx >= 0 else text[:240]
            out.append(f"  [{authority}] analogy: …{snippet}…")
    return out


def frame_split(tafsir_entries):
    """Split frame: where a classical and a modern authority read the verse differently."""
    classical = [(a, t) for a, t in tafsir_entries if any(c in a for c in CLASSICAL)]
    modern = [(a, t) for a, t in tafsir_entries if any(m in a for m in MODERN)]
    if classical and modern:
        c_auth = ', '.join(a for a, _ in classical[:2])
        m_auth = ', '.join(a for a, _ in modern[:2])
        return [f"  classical read ({c_auth}) vs modern read ({m_auth}) — see full tafsir "
                f"entries above for each authority's framing of the 'illa and ruling."]
    return []


def frame_network(citation):
    """Network frame: the node/domain this verse belongs to (from the node database knowledge)."""
    KNOWN = {
        'Quran 2:229': 'Divorce node (the two-divorce limit; khul\' exit)',
        'Quran 2:230': 'Divorce node (three-repudiation bar)',
        'Quran 2:219': 'Alcohol/gambling node (stepped prohibition: first informational stage)',
        'Quran 4:43': 'Alcohol node (second stage: no prayer while drunk)',
        'Quran 5:90': 'Alcohol/gambling node (final absolute prohibition)',
        'Quran 5:91': "Alcohol node — the 'illa (enmity + turning from prayer)",
        'Quran 16:94': 'Lying/perjury node (oaths as deceit)',
        'Quran 2:188': 'Wealth node (consuming by falsehood)',
        'Quran 2:178': 'Retribution node (qisas)',
        'Quran 5:45': 'Retribution node (lex talionis / physical correspondence)',
        'Quran 24:2': 'Sexuality node (fixed hadd for zina)',
        'Quran 24:4': 'Testimony/qadhf node (false accusation hadd)',
        'Quran 2:275': 'Usury node (riba — prohibited with explicit exit)',
        'Quran 2:279': 'Usury node (the two-branched exit: war-warning or repent)',
        'Quran 9:5': 'War node (the Sword Verse — conditional escalation)',
        'Quran 2:190': 'War node (the defensive trigger)',
        'Quran 8:61': 'War node (the peace-node)',
        'Quran 2:185': 'Worship node (fasting relief — Yusr)',
        'Quran 5:6': 'Worship node (tayammum)',
        'Quran 2:282': 'Testimony node (two men or a man + two women)',
        'Quran 5:106': 'Testimony node (non-Muslim witnesses in necessity)',
        'Quran 4:11': 'Inheritance node (fixed shares)',
        'Quran 4:176': 'Inheritance node (kalala)',
        'Quran 2:240': 'Inheritance node (widow\'s 1-year home)',
        'Quran 3:7': 'Hermeneutic node (muhkam/mutashabih — the clear/ambiguous master-rule)',
    }
    for k, v in KNOWN.items():
        if citation.startswith(k):
            return [f"  network: {v}"]
    return [f"  network: (node mapping for {citation} not in the current register)"]


def main():
    args = sys.argv[1:]
    if '--query' not in args:
        print(__doc__)
        return
    qi = args.index('--query')
    q = args[qi + 1] if qi + 1 < len(args) else ''
    k = int(args[args.index('--k') + 1]) if '--k' in args else 5

    # Determine the mode and frame toggles
    mode = 'text'
    if '--mode' in args:
        mode = args[args.index('--mode') + 1]
    frames = set()
    for flag in ('--frame naskh', '--frame asbab', '--frame qiyas', '--frame split', '--frame network'):
        name = flag.split()[-1]
        if flag in ' '.join(args):
            frames.add(name)
    if mode == 'initiated':
        frames = {'naskh', 'asbab', 'qiyas', 'split', 'network'}

    print(f"# {q}  (mode={mode})")
    print(f"  {k} hits from the {COLLECTION} corpus — original Arabic, verbatim\n")

    for meta, doc in query(q, k):
        citation = meta['citation']
        print(f"── [{citation}]")
        print(f"   {doc[:400]}")
        if frames:
            # Gather tafsir for this verse to feed the frames
            verse = citation.split('|')[0].strip()
            tafsir_entries = get_tafsir_for_verse(verse)
            print("   ── Initiation layer (the tradition's frame, not the text itself):")
            if 'network' in frames:
                for line in frame_network(citation):
                    print(line)
            if 'naskh' in frames:
                n = frame_naskh(tafsir_entries)
                if n:
                    print("   · naskh/abrogation:")
                    for line in n:
                        print(line)
            if 'asbab' in frames:
                a = frame_asbab(tafsir_entries)
                if a:
                    print("   · occasion of revelation:")
                    for line in a:
                        print(line)
            if 'qiyas' in frames:
                q = frame_qiyas(tafsir_entries)
                if q:
                    print("   · analogical extension:")
                    for line in q:
                        print(line)
            if 'split' in frames:
                s = frame_split(tafsir_entries)
                if s:
                    print("   · classical vs modern:")
                    for line in s:
                        print(line)
            if not (frame_naskh(tafsir_entries) or frame_asbab(tafsir_entries)
                    or frame_qiyas(tafsir_entries) or frame_split(tafsir_entries)):
                print("   · (no initiation frame found in tafsir for this verse — "
                      "text stands on its own)")
    print("\n  ⚠ The initiation layer shows how the tradition reads the text; it is not "
          "a substitute for the raw Arabic above. Both the naive-literal and the "
          "ideological misreadings are avoided by keeping text and frame separate.")


if __name__ == '__main__':
    main()
