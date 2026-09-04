#!/usr/bin/env python3
"""Append Ibn Sa'd's Tabaqat (historical, non-canonical) to the islamic_corpus index.

Each entry is stored with metadata that carries its CANONICAL GRADE, so the
consultant can distinguish canonical hadith from historical context reports:
  - source_class = 'historical'
  - grade        = 'da\\'if'   (non-canonical, weak-by-default)
  - weight       = 'context'

Usage:
  python ic_index_tabaqat.py [--query "..."] [--k N]
"""
import os, sys, json, time, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
TABAQAT_TSV = os.path.join(BASE, 'text', 'tabaqat.tsv')
CHROMA_DIR = os.path.join(BASE, 'chroma')
COLLECTION = 'islamic_corpus'

OLLAMA_URL = 'http://localhost:11434'
EMBED_MODEL = 'bge-m3'


def embed(texts):
    texts = [t[:6000] for t in texts]
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                f'{OLLAMA_URL}/api/embed',
                data=json.dumps({'model': EMBED_MODEL, 'input': texts}).encode(),
                headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read())
            return d['embeddings']
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


def load_entries():
    entries = []
    if not os.path.exists(TABAQAT_TSV):
        return entries
    with open(TABAQAT_TSV, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if '\t' not in line:
                continue
            cit, text = line.split('\t', 1)
            if text.strip():
                entries.append((cit.strip(), text.strip()))
    return entries


def grade_fields(citation):
    """Derive source_class / grade / weight from a citation tag."""
    low = citation.lower()
    if 'historical' in low or 'tabaqat' in low:
        return {'source_class': 'historical', 'grade': 'da\'if', 'weight': 'context'}
    if low.startswith('quran'):
        return {'source_class': 'canonical', 'grade': 'sahih', 'weight': 'canon'}
    # default
    return {'source_class': 'hadith', 'grade': 'sahih', 'weight': 'canon'}


def main():
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    col = client.get_or_create_collection(
        name=COLLECTION, metadata={'hnsw:space': 'cosine'})

    entries = load_entries()
    print(f"Loaded {len(entries)} tabaqat entries")

    BATCH = 32
    start_id = col.count()  # append after existing rows
    for i in range(0, len(entries), BATCH):
        batch = entries[i:i + BATCH]
        ids = [f"t{start_id + i + j}" for j in range(len(batch))]
        texts = [t for _, t in batch]
        cits = [c for c, _ in batch]
        vecs = embed(texts)
        meta = [{'citation': c, **grade_fields(c)} for c in cits]
        col.upsert(ids=ids, embeddings=vecs,
                   documents=texts, metadatas=meta)
        if (i // BATCH) % 5 == 0:
            print(f"  upserted {i + len(batch)}/{len(entries)}")
    print(f"Done. Collection total: {col.count()}")


if __name__ == '__main__':
    if '--query' in sys.argv:
        import chromadb
        q = sys.argv[sys.argv.index('--query') + 1]
        k = int(sys.argv[sys.argv.index('--k') + 1]) if '--k' in sys.argv else 5
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        col = client.get_collection(COLLECTION)
        vec = embed([q])[0]
        res = col.query(query_embeddings=[vec], n_results=k)
        for i, (doc, meta) in enumerate(zip(res['documents'][0], res['metadatas'][0])):
            print(f"\n[{meta['citation']}] [grade={meta.get('grade','?')}]")
            print(f"  {doc[:250]}")
    else:
        main()
