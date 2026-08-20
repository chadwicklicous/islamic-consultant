---
name: islamic-consultant
description: "Answer Quran and Hadith questions from the original Arabic."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [islam, quran, hadith, arabic, exegesis, vector-search]
    category: research
---

# Islamic Consultant

Answer questions about the Quran and the Hadith **from the original Arabic**, with exact citations (surah:ayah for the Quran, collection + number for hadiths), not from a translation or the model's recollection.

## When to Use

- User asks a question about a Quranic verse, a hadith, an Islamic concept, or a ruling
- User wants a verse/hadith located, an Arabic word examined, or a citation verified
- User is doing study, exegesis, or writing and needs the original Arabic with a precise reference

## The Corpus (already built)

- **Text corpus:** `C:\Users\philo\islamic-consultant\scripts\text\` — 4 TSV files, 101,865 entries, each `CITATION\tTEXT`
- **Vector index:** `C:\Users\philo\islamic-consultant\scripts\chroma\` — ChromaDB collection `islamic_corpus`, bge-m3 (1024-dim, multilingual)
- **Obsidian index:** `What Animates Man/Islamic Corpus/Index.md`

The corpus covers:
- **Quran** (114 surahs, 6,236 verses) — Arabic, Uthmani script
- **Hadith** (16 collections, 50,276 hadiths) — the Six Books (Bukhari, Muslim, Abu Dawud, Tirmidhi, Nasa'i, Ibn Majah) plus Muwatta Malik, Riyad as-Salihin, and more
- **Tafsir (interpretation)** (43,522 entries) — Arabic commentary on every verse from 7 authorities:
  - **Classical Sunni**: Ibn Kathir, al-Tabari, al-Qurtubi, al-Baghawi
  - **Modern Sunni**: al-Sa'di, al-Wasit (Tantawi), al-Muyassar
- **Sufi (mystical)** (1,831 entries) — Ghazali's *Ihya Ulum al-Din* ("Revival of the Religious Sciences"), the foundational Sufi text, in Arabic.

Each entry carries authority + layer metadata in its citation, e.g.
`Quran 4:3 | Ibn Kathir | classical-sunni` or `Ihya Ulum al-Din | كتاب العلم | sufi`.
This lets the consultant answer both "what does the Quran say" and "how does the
tradition interpret it" — the interpretive layer that directs how practitioners
read the text.

### Not yet included (deferred)

The following are **not** in the corpus because clean Arabic sources are not
freely available. Users may add them manually if they have access to a digital
edition:
- **Shia**: Nahj al-Balagha (sayings of Ali), Ja'fari fiqh
- **Sufi**: Ibn Arabi's *Futuhat al-Makkiyya*

These are noted so the consultant is honest about coverage rather than silently
omitting major interpretive traditions.

## Query Workflow

### 1. Semantic retrieval

```bash
cd /c/Users/philo/islamic-consultant/scripts
python ic_index.py --query "<question, in Arabic or English>" --k 5
```

bge-m3 is multilingual, so English queries match Arabic text. Returns the top-k
entries with exact citations. For a broader sweep, use `--k 10`.

### 2. Read the actual text

The query returns the verse/hadith text. Read it carefully. If you need the full
text (the query truncates to 300 chars), grep the TSV:

```bash
grep -F "Quran 2:255" /c/Users/philo/islamic-consultant/scripts/text/quran.tsv
```

### 3. Answer from the source

- Quote the **original Arabic** verse/hadith.
- Give the **exact citation** (e.g. `Quran 2:255`, `Sahih al-Bukhari 1`).
- Explain the passage in the user's language, but anchor every claim in the quoted text.
- Note the original Arabic word where relevant (e.g. *rahmah* "mercy", *iman* "faith").
- **For interpretive questions**, retrieve the tafsir layer too — query for the
  verse and note which authority's reading you're presenting (e.g. Ibn Kathir vs
  al-Sa'di). The citation encodes the authority and layer, so you can distinguish
  the classical Sunni reading from the modern one.

## The Initiation Layer (toggleable)

For scholars who want the **original Arabic text without bias or ideological
interpretation**, the consultant has a second, optional query mode that shows how
the tradition itself teaches the initiated to read the text. It is **off by
default** — the raw text always stands alone. Use `ic_query.py` for this:

```bash
cd /c/Users/philo/islamic-consultant/scripts

# Mode A — TEXT (default): raw retrieval only, original Arabic + citation, nothing else
python ic_query.py --query "wine" --k 5

# Mode B — TEXT + INITIATION LAYER: adds a clearly-labeled frame showing how the
# tradition reads the text (naskh state, occasion of revelation, 'illa/qiyas
# extension, classical-vs-modern split, and network rank), each grounded in tafsir
python ic_query.py --mode initiated --query "wine" --k 5

# Fine-grained toggles (show only one frame at a time)
python ic_query.py --frame naskh --query "wine"
python ic_query.py --frame asbab --query "wine"
python ic_query.py --frame qiyas --query "wine"
python ic_query.py --frame split --query "wine"
python ic_query.py --frame network --query "wine"
```

**What the initiation layer is (and isn't):**
- It is the **tradition's own reading key** — the discipline the initiated are
  taught (*usul al-fiqh*): which verse abrogates which (naskh), the occasion of
  revelation (asbab al-nuzul), the ratio that lets a ruling extend by analogy
  ('illa / qiyas), and where classical vs. modern tafsir diverge.
- It is **always labeled** as the tradition's frame, never as the text itself.
- It **never replaces the raw Arabic** — Mode A (text) is the authoritative
  baseline; the layer is an optional window into how the initiated read it.
- It avoids **both** failure modes: naive literalism (treating every verse as a
  time-flat command) and ideological projection (reading modern values in).

**Design reference:** `deep-research/The_Initiation_Layer_Design.md`

## Citation format

| Form | Meaning |
|------|---------|
| `Quran 2:255` | surah:ayah (the Throne Verse) |
| `Sahih al-Bukhari 1` | collection + hadith number |
| `Quran 4:3 \| Ibn Kathir \| classical-sunni` | tafsir entry: verse + authority + layer |
| `Ihya Ulum al-Din \| كتاب العلم \| sufi` | sufi entry: work + book + layer |

## Pitfalls

- **Don't answer from memory or from a translation.** Always retrieve and quote the original Arabic. The whole point is citation-grounded answers in the original language.
- **The index build is resumable.** If `ic_index.py` dies partway, re-run it — it resumes from the last indexed count.
- **Ollama must be running** for embeddings (`ollama serve`). Model: `bge-m3` (multilingual — required for Arabic).
- **Long entries** are truncated to 6000 chars before embedding.
- **Hadith numbering** is per-collection (IDs reset per book), so always cite the collection name alongside the number.

## Verification

1. Run a query and confirm it returns entries with valid citations.
2. Grep the TSV to confirm the full text matches the citation.
3. Answer a test question and confirm every claim is anchored in a quoted Arabic verse/hadith.
