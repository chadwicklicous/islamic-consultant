# Islamic Consultant

A citation-grounded consultant for the **Quran and the Hadith from the original
Arabic**. Builds a semantic-search index over the Quran (Uthmani script), 16 major
Hadith collections, the classical/modern Sunni tafsir (interpretation) tradition,
and Ghazali's *Ihya Ulum al-Din* — and answers questions **from the original Arabic
with exact citations** (surah:ayah for the Quran, collection + number for hadiths),
not from a translation or a model's recollection.

Includes the **Initiation Layer** — a scholar-facing toggle that shows how the
tradition itself teaches the initiated to read the text, while keeping the raw
Arabic authoritative.

## What it does

1. Downloads and extracts the corpus in the original Arabic:
   - **Quran** (114 surahs, 6,236 verses) — Uthmani script
   - **Hadith** (16 collections, 50,276 hadiths) — the Six Books (Bukhari, Muslim,
     Abu Dawud, Tirmidhi, Nasa'i, Ibn Majah), Muwatta Malik, Riyad as-Salihin, and more
   - **Tafsir** (43,522 entries) — Arabic commentary on every verse from 7 authorities:
     classical (Ibn Kathir, al-Tabari, al-Qurtubi, al-Baghawi) and modern (al-Sa'di,
     al-Wasit/Tantawi, al-Muyassar)
   - **Sufi** (1,831 entries) — Ghazali's *Ihya Ulum al-Din*
2. Builds a ChromaDB vector index (bge-m3, 1024-dim, multilingual) for semantic search.
3. Answers questions by retrieving the relevant Arabic passages with exact citations.

## Two ways to use it

### For non-technical users (recommended): let your AI agent do the work

If you use **Hermes Agent** (or a similar AI agent), you don't need to run any
commands. Just:

1. Install the skill:
   ```bash
   hermes skills install https://raw.githubusercontent.com/chadwicklicous/islamic-consultant/main/SKILL.md
   ```
   (or copy this repo's `SKILL.md` + `scripts/` into your agent's skills folder)
2. Say: *"Set up the Islamic consultant."*

Your agent reads the skill, installs the dependencies, downloads the corpus, builds
the index, and verifies it — all autonomously. Then you ask questions in plain
English and it answers from the original Arabic with exact citations.

### For technical users: run it directly

The pipeline is standalone Python. See the Quick start below.

## Requirements

- **Python 3.9+** (stdlib only for the pipeline; `chromadb` for the index)
- **ChromaDB** — `pip install "chromadb==1.5.9"` (in `requirements.txt`). Runs embedded.
- **Ollama** — the embedding provider (free, local, no API key). Pull the `bge-m3`
  model with `ollama pull bge-m3` (multilingual — required for Arabic).
- **Hermes Agent** (optional) — to use the bundled `islamic-consultant` skill.

## Quick start

```bash
# 1. Install dependencies
pip install "chromadb==1.5.9"

# 2. Pull the embedding model
ollama pull bge-m3

# 3. Build the corpus (downloads the Quran, hadith, tafsir, sufi)
cd scripts
python ic_download.py          # Quran + hadith
python ic_download_tafsir.py   # 7 tafsir authorities
python ic_download_sufi.py     # Ghazali's Ihya
python ic_extract.py && python ic_extract_tafsir.py && python ic_extract_sufi.py

# 4. Build the vector index (embeds ~102k entries; resumable)
python ic_index.py

# 5. Query — raw Arabic text
python ic_index.py --query "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ" --k 5
# or in English (bge-m3 is multilingual)
python ic_index.py --query "the Throne Verse" --k 5
```

## The Initiation Layer (scholar tool)

For scholars who want the **original Arabic without bias or ideological
interpretation**, the consultant has a second, optional query mode. It is **off by
default** — the raw text always stands alone.

```bash
cd scripts

# Mode A — TEXT (default): raw retrieval only, original Arabic + citation
python ic_query.py --query "wine" --k 5

# Mode B — TEXT + INITIATION LAYER: adds the tradition's reading frame
# (naskh state, occasion of revelation, 'illa/qiyas extension, classical-vs-modern
# split, network rank), each grounded in the tafsir — always labeled, never replacing
# the raw text
python ic_query.py --mode initiated --query "wine" --k 5

# Fine-grained toggles
python ic_query.py --frame naskh --query "wine"
python ic_query.py --frame asbab --query "wine"
python ic_query.py --frame qiyas --query "wine"
python ic_query.py --frame split --query "wine"
python ic_query.py --frame network --query "wine"
```

The initiation layer is the **tradition's own reading key** — the discipline the
initiated are taught (*usul al-fiqh*): which verse abrogates which (naskh), the
occasion of revelation (asbab al-nuzul), the ratio that lets a ruling extend by
analogy ('illa / qiyas), and where classical vs. modern tafsir diverge. It avoids
**both** failure modes: naive literalism (treating every verse as a time-flat
command) and ideological projection (reading modern values in). The design rationale
is in `docs/The_Initiation_Layer_Design.md`.

## Research notes (in `docs/`)

The consultant was built in support of a comparative-theology research project.
The analytical notes that emerged are included:

- **The Juridical Cipher** — understanding Islam through its jurisprudential
  methodology: a network of conditional permissions (IF [condition] THEN [state change]).
- **The Cipher Keys: Qiyas and Naskh** — the two master keys that decode and reorder the network.
- **Cipher Exploration — Additional Qiyas and Naskh** — 5 stepped-revelation (naskh) chains,
  qiyas extensions, and the modern tafsir's narrowing of classical readings.
- **The Eight Moral Questions** — divorce, alcohol, lying, wealth, retribution,
  sexuality, usury, and war worked through the cipher.
- **The Permission Node Database** — a catalog of the conditional legal nodes, with the 'illa register.
- **The Initiation Layer Design** — the design for the scholar-facing toggle.

## Citation format

| Form | Meaning |
|------|---------|
| `Quran 2:255` | surah:ayah (the Throne Verse) |
| `Sahih al-Bukhari 1` | collection + hadith number |
| `Quran 4:3 \| Ibn Kathir \| classical-sunni` | tafsir entry: verse + authority + layer |
| `Ihya Ulum al-Din \| كتاب العلم \| sufi` | sufi entry: work + book + layer |

## License

MIT. The Quranic text and tafsir/hadith sources are from public/open collections
(free Arabic corpora); this repository does not distribute the large corpus — the
scripts build it from the public sources.

---

*The Islamic Consultant is a research aid. It retrieves and cites the texts; the
interpretation and judgment remain with the reader.*
