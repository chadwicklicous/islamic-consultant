#!/usr/bin/env python3
"""Append the Sufi (Ghazali Ihya) layer to the islamic_corpus index.

Uses distinct IDs (s{idx}) and upsert, so re-running is safe.

Usage:
  python ic_index_sufi.py            # append sufi entries
  python ic_index_sufi.py --query "..." --k 5
"""
import os, sys, json, time, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
SUFI_TSV = os.path.join(BASE, 'text', 'sufi.tsv')
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
    if not os.path.exists(SUFI_TSV):
        return entries
    with open(SUFI_TSV, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if '\t' not in line:
                continue
            cit, text = line.split('\t', 1)
            if text.strip():
                entries.append((cit.strip(), text.strip()))
    return entries


def main():
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    col = client.get_or_create_collection(
        name=COLLECTION,
        metadata={'hnsw:space': 'cosine'})

    entries = load_entries()
    print(f"Loaded {len(entries)} sufi entries")

    BATCH = 32
    for i in range(0, len(entries), BATCH):
        batch = entries[i:i+BATCH]
        ids = [f"s{i+j}" for j in range(len(batch))]
        texts = [t for _, t in batch]
        cits = [c for c, _ in batch]
        vecs = embed(texts)
        col.upsert(ids=ids, embeddings=vecs,
                   documents=texts,
                   metadatas=[{'citation': c} for c in cits])
        if (i // BATCH) % 5 == 0:
            print(f"  upserted {i+len(batch)}/{len(entries)}")
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
            print(f"\n[{meta['citation']}]\n  {doc[:250]}")
    else:
        main()
