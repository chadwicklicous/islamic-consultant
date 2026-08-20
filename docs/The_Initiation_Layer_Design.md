# The Initiation Layer
## Design for the "Methodological Hermeneutic" Toggle in the Islamic Consultant

**Status:** Design document
**Date:** August 19, 2026
**Goal:** Make the consultant a tool for scholars to get the **original Arabic text without bias or ideological interpretation** — while providing an *optional, toggleable* layer that teaches the non-initiated how the initiated actually read the text (the tradition's own jurisprudential method, *usul al-fiqh*).

---

## 1. The Problem Being Solved

A scholar using a raw Quran/Hadith corpus sees individual verses. But the tradition does **not** read verses as flat, isolated commands. It reads them through a learned method — the conditional-node network, decoded by *qiyas* (analogy), *naskh* (abrogation), *asbab al-nuzul* (occasions of revelation), and the *muhkam/mutashabih* (clear/ambiguous) distinction.

Two failure modes to avoid:
1. **Naive literalism** — treating every verse as an unconditional, time-flat command. (The outsider's error.)
2. **Ideological projection** — reading modern values into the text. (The apologist's error.)

Both are *bias*. The text, read on its own, is conditional, time-indexed, and analogically-structured. The initiation layer exists to surface the **tradition's own reading key** — so the scholar sees exactly how the initiated learn to read it — without ever *replacing* the raw text.

**The principle:** the raw Arabic is always the ground truth. The initiation layer is a *frame*, clearly marked as the tradition's interpretive method, toggleable on/off.

---

## 2. The Two-Mode Design

The consultant runs in two modes, with a toggle:

### Mode A — TEXT (default, always available)
> Pure retrieval. Return the original Arabic + citation, nothing more. No interpretation, no gloss, no method.

Example query: *"what does the Quran say about wine?"*
- **Mode A output:** quotes 2:219, 4:43, 5:90, 16:67 in Arabic, with citations. Nothing else.

### Mode B — TEXT + INITIATION LAYER (toggle ON)
> Retrieval + the tradition's reading key. Returns the raw text PLUS a clearly-labeled frame showing how the tradition teaches the initiated to read it — the naskh sequence, the asbab, the qiyas-extension, the classical vs. modern tafsir split.

The initiation layer is the **interface layer between the text and the tradition's method.** It is not a substitute for the text; it is the *key* the tradition hands to the initiated.

---

## 3. The Layer as a Toggle — Technical Shape

Each retrieval returns, in addition to the raw Arabic, a structured **methodological frame** when the toggle is ON. The frame has up to five fields, each grounded in the actual corpus:

| Field | What it shows | Source in corpus |
|-------|---------------|------------------|
| **1. Naskh state** | Is this verse superseded, or does it supersede? Time-index. | tafsir naskh mentions (777 in corpus) |
| **2. Asbab al-nuzul** | Occasion of revelation — the historical trigger | tafsir "سبب نزول" (343 mentions) |
| **3. Qiyas 'illa** | The ratio that lets it extend to parallel cases | node database 'illa register |
| **4. Classical vs. modern** | Where Ibn Kathir/al-Tabari read it one way, al-Sa'di/al-Wasit another | the 7 tafsir authorities |
| **5. Rank in network** | What node(s) it connects to; which domain | node database + network map |

The frame is **always labeled**: "Tradition's framing — not the text itself." The user can toggle the whole layer, or per-field.

---

## 4. The "How the Initiated Are Taught" Content

The core insight: the tradition teaches a *method*, not a list. The initiation layer surfaces five things the tradition itself considers essential for the non-initiated to learn, each grounded in the corpus's own tafsir data:

### 4.1 The Chronological Key (Naskh)
The tradition reads the Quran as a **time-indexed** text. The same theme can have a Meccan (early, often patient/non-coercive) and a Medinan (later, often juridical) phase. The layer shows the *sequence* — which verse came earlier, which later, which supersedes.

- **Example:** the wine verses. 2:20 (Meccan, "great sin and benefit") → 4:43 (Medinan, "do not approach prayer drunk") → 5:90 (final, "avoid it"). The layer shows the *stepped* prohibition — the tradition's own record of progressive revelation.

### 4.2 The Occasion (Asbab al-Nuzul)
The tradition always teaches *why* a verse came down. The layer surfaces the occasion — e.g., the divorce-verse occasions, the war-verse occasion at Badr/after treaty-breach. The non-initiated reader sees the historical trigger, not just the abstract rule.

### 4.3 The Clear vs. the Ambiguous (Muhkam / Mutashabih)
Quran 3:7 itself divides the text: "verses firmly-constructed are the mother of the Book, and others are similar-ones; those in whose hearts is deviation follow the ambiguous, seeking discord and seeking its interpretation." The layer teaches the tradition's rule: **ambiguous verses are resolved by the clear ones, not by the reader's whim.** This is the master-method against ideological projection.

### 4.4 The Extension by Analogy (Qiyas)
The tradition reads each ruling not in isolation but as extendable by its 'illa. The layer shows how a ruling connects to its parallels — e.g., the marriage-asymmetry 'illa of authority extending the marriage rule.

### 4.5 The Honest Divergence — Classical vs. Modern
The layer shows where the classical tafsir (Ibn Kathir, al-Tabari, al-Qurtubi) and the modern (al-Sa'di, al-Wasit/Tantawi) diverge. This is the *non-ideological* core: it does not choose sides, it surfaces the divergence honestly so the scholar sees the interpretive range within the tradition itself.

---

## 5. Toggle Mechanics (Design)

The toggle lives in the tool's config and query surface:

```
--mode text            # raw retrieval only (default)
--mode initiated       # text + full initiation layer
--frame naskh          # only the naskh frame
--frame asbab          # only the occasions
--frame qiyas          # only the analogy extensions
--frame split          # only the classical/modern divergence
```

On by default? **No.** Default to `--mode text` (the honest baseline). The initiation layer is an explicit, optional act of the scholar. This preserves the tool's promise: original text without bias, with the frame available for those who want to see how the tradition teaches it.

---

## 6. What the Initiation Layer is NOT

To keep the tool honest, the layer must *not* become:
- **An apology** — it does not justify; it shows the tradition's own method and its internal divergences.
- **An ideology** — it does not flatten the classical/modern split into one "correct" reading; it shows both honestly.
- **A substitute** — the raw Arabic remains the authoritative ground; the frame never overrides the text.

The layer is a *window into the tradition's teaching* — the scholar's tool to see how the text is read by those who read it canonically, while the text itself stays raw and unmediated.

---

## 7. Relation to the Cipher Work

The initiation layer is the **deliverable form** of the Cipher Keys work. The cipher (qiyas + naskh) is the method; the initiation layer is the tool that *presents* that method to the scholar on demand. The Cipher Keys paper becomes the "how," the initiation layer the "tool."

This is why the Cipher Keys chapter becomes part of the packaged consultant: it is the *manual* that explains the initiation layer's five frames to the human reader.
