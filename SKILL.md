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

- **Text corpus:** `C:\Users\philo\islamic-consultant\scripts\text\` — 7 TSV files, 113,776 entries, each `CITATION\tTEXT`
- **Vector index:** `C:\Users\philo\islamic-consultant\scripts\chroma\` — ChromaDB collection `islamic_corpus`, bge-m3 (1024-dim, multilingual)
- **Obsidian index:** `What Animates Man/Islamic Corpus/Index.md`

The corpus covers:
- **Quran** (114 surahs, 6,236 verses) — Arabic, Uthmani script
- **Hadith** (16 collections, 50,276 hadiths) — the Six Books (Bukhari, Muslim, Abu Dawud, Tirmidhi, Nasa'i, Ibn Majah) plus Muwatta Malik, Riyad as-Salihin, and more
- **Tafsir (interpretation)** (43,522 entries) — Arabic commentary on every verse from 7 authorities:
  - **Classical Sunni**: Ibn Kathir, al-Tabari, al-Qurtubi, al-Baghawi
  - **Modern Sunni**: al-Sa'di, al-Wasit (Tantawi), al-Muyassar
- **Sufi (mystical)** (1,831 entries) — Ghazali's *Ihya Ulum al-Din* ("Revival of the Religious Sciences"), the foundational Sufi text, in Arabic.
- **Sira (biography)** (2,491 entries) — Ibn Hisham's *Sira Nabawiyya* (Mustafa al-Saqqa edition), the foundational biography of the Prophet.
- **Tabaqat (biographical dictionary)** (8,550 entries) — Ibn Sa'd's *al-Tabaqat al-Kubra* (al-Khanji ed.), the earliest surviving biographical dictionary of the Prophet and his companions.
- **Akhbar Makka (history of Mecca)** (870 entries) — al-Azraqi's *Akhbar Makka wa-ma ja'a fiha min al-athar* (Malhas ed.), an early topographical history of Mecca (historical layer).

Each entry carries authority + layer metadata in its citation, e.g.
`Quran 4:3 | Ibn Kathir | classical-sunni` or `Ihya Ulum al-Din | كتاب العلم | sufi`.
This lets the consultant answer both "what does the Quran say" and "how does the
tradition interpret it" — the interpretive layer that directs how practitioners
read the text.

### Canonical-grade vocabulary (which sources are authoritative)

The consultant distinguishes **canonical** reports (authoritative for law and
belief) from **non-canonical** historical reports (context only). Every citation
carries a built-in grade via `ic_grades.py` and the index stores
`source_class` / `grade` / `weight` metadata:

- **Canonical** (صحيح / sahih) — the Quran itself, plus the *Kutub al-Sittah*:
  Bukhari, Muslim, Abu Dawud, Tirmidhi, Nasai, Ibn Majah, and recognized sahih
  works (Riyad as-Salihin, Muwatta Malik, Mishkat al-Masabih). Authoritative for
  both belief and legal practice. Citation suffix: `canonical:sahih`.
- **Historical** (تاريخي, weight `context`) — biographical/historical works like
  Ibn Hisham's *Sira* and Ibn Sa'd's *Tabaqat*. They give context to the
  Prophet's life but are **NOT** part of the canonical hadith corpus and often
  carry weak (*da'if*) chains. Useful for context; NOT authoritative for legal
  practice. Citation suffix: `historical:da'if`.
- **Commentary** (تفسير) / **Devotional** (تصوف) — tafsir and sufi layers.

**The hadith-science report grades** (from `ic_grades.py`):
| Arabic | Grade | Meaning |
|--------|-------|---------|
| صحيح | **sahih** | sound, authentic — meets the strictest criteria |
| حسن | **hasan** | good — reliable but slightly weaker |
| ضعيف | **da'if** | weak — a flaw in the chain or text |
| موضوع | **mawdu'** | fabricated — a forgery, rejected outright |

**The narrator grades** (*jarh wa ta'dil* — the transmitter-auditing science):
| Arabic | Grade | Meaning |
|--------|-------|---------|
| ثقة | **thiqah** | trustworthy — reliable |
| صدوق | **saduq** | truthful — mostly reliable |
| ضعيف | **da'if** | weak — unreliable |
| كذاب | **kadhdhab** | liar — a fabricator |

Use these to tell the user when a report sits on the **context** side of the
tradition (historical, weak, non-canonical) versus the **canon** side. This is
especially important when answering from the Sira or Tabaqat: those works narrate
the Prophet's life but are not the basis for law. See `ic_grades.py --help` /
`python ic_grades.py` for the full vocabulary reference.

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

### Epistemic standards (READ BEFORE ANSWERING)

Religious-studies material is full of difficulty-to-source tradition: rumors,
black myths, outright fabrications, polemical distortions, and revisionist
counter-claims. The user explicitly wants accuracy and awareness of limits over
confidence. Apply these rules to every answer:

1. **Separate exactly three registers, and label each:**
   - **Text** — something I retrieved verbatim from a corpus file with a citation.
   - **Sourced tradition** — a claim a work says the tradition holds (e.g.
     al-Azraqi "it is said the jinn gave allegiance"). Still cite the work.
   - **Hypothesis / general knowledge** — my inference or what I know from outside
     the corpus. ALWAYS label it as such ("my hypothesis is…", "this is general
     knowledge, not from the corpus"). Never deliver it in the voice of the text.

2. **Never counter a claim with an equally-unsourced counter-claim.** If I doubt a
   report, I may say "I cannot find it in the sources I have" (a statement of
   absence, backed by the search I actually ran) — but I must NOT substitute my own
   made-up reading as if it were the tradition. A hypothesis is welcome and can
   generate leads, but it must be flagged as a hypothesis, not asserted as fact.

3. **Absence ≠ non-existence.** "Not in my corpus" means exactly that. State which
   sources I checked. Do not upgrade a searching-failure into "this story is
   fake everywhere." If the report is attributed to a source I don't hold, say so
   explicitly and offer to go get that source (as with al-Azraqi). Actually go
   fetch it before making claims about it.

4. **Do not paraphrase a polemical or revisionist secondhand summary as the story
   itself.** If the user brings me a video/claim, separate (a) what I can verify in
   primary sources from (b) what I can only see in the secondhand retelling. Do not
   inherit the retelling's specifics (e.g. "they rode him all night") unless I find
   them in a primary text.

5. **A counter-reading is only legitimate if I have a text for it.** To say "the
   tradition reads X as jinn," I need a source that says so (e.g. al-Azraqi's
   "the jinn gave allegiance"). If I only *think* that's how it's read, label it a
   hypothesis.

6. **When genuinely uncertain, say "I don't know," then state the smallest true
   claim I can defend** and what would settle it. Confidence must scale with
   competence — never fill an evidential gap with assertive prose.

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
