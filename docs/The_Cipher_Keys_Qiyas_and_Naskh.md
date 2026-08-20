# The Cipher Keys: Qiyas and Naskh
## How the Juridical Network Is Decoded and Reordered

**Author:** Hermes Agent (Islamic Consultant)
**Date:** August 19, 2026
**Status:** Working notes
**Corpus:** Quran (Uthmani), Sunni tafsir (al-Baghawi, Ibn Kathir, al-Sa'di, al-Qurtubi, al-Tabari) — indexed via ChromaDB + bge-m3.

---

## Abstract

The permission-node network is decoded by two master keys: **Qiyas** (analogy) and **Naskh** (abrogation). Qiyas *extends* the network — it identifies the ratio legis ('illa) of a ruling and applies it to parallel cases, so the network grows by analogy. Naskh *reorders* the network — it determines which node is in force, so the network changes over time. Together they explain how the juridical web is both *generated* and *governed*. This note documents both keys with the concrete examples found in the corpus.

---

## 1. Qiyas — the Key That Extends the Network

### 1.1 The mechanism

Qiyas (analogy) is the tool by which a ruling is extended from a core text to a parallel case. It works in four steps:

1. **Identify the core ruling** (the *asl*, the "root" case) — a verse that gives a clear ruling.
2. **Identify the 'illa** (the ratio legis, the underlying reason) — *why* the ruling holds.
3. **Find a parallel case** (the *far'*, the "branch") — a new case that shares the same 'illa.
4. **Extend the ruling** — apply the core ruling to the parallel case, because the same reason holds.

The 'illa is the key. If you can identify the 'illa of a ruling, you can extend it to any case that shares that 'illa.

### 1.2 The marriage asymmetry as a worked example

The clearest example in the corpus is the marriage asymmetry:

- **Core ruling (asl):** Quran 5:5 — a Muslim man may marry a chaste People-of-the-Book woman.
- **'Illa (ratio):** The husband is the *qawwam* (authority) over the wife (Quran 4:34). The believer retains authority in the marriage.
- **Parallel case (far'):** A Muslim woman marrying a People-of-the-Book man.
- **Extension:** The reverse is forbidden, because the believing woman would come *under* the authority of a non-believer.

The 'illa is **authority** (*qawwama*). Where the believer retains authority, the marriage is permitted; where the believer would fall under non-believer authority, it is forbidden. Qiyas extends the ruling by the 'illa.

### 1.3 The 'illa register (from the node database)

The 'illas that recur across the network, and the nodes they govern:

| 'Illa | Nodes governed |
|-------|---------------|
| **Justice** (*adl*) | Polygamy (4:3), retaliation (2:178), contracts (2:282) |
| **Authority** (*qawwama*) | Marriage asymmetry (5:5/2:221), *daraja* (2:228) |
| **Submission** (*sughar*) | Jizya (9:29), dhimma (9:4) |
| **Self-preservation** (*ikrah*) | Taqiyya (3:28), compulsion (16:106) |
| **Care for the vulnerable** | Zakat (9:60), orphans (4:6), divorced women (2:241) |
| **Restoration** | Expiation nodes (4:92, 5:89, 58:3) |
| **Deterrence** | Hudud (24:2, 5:38, 24:4) |

The network is held together by these seven 'illas. Qiyas is the tool that *applies* them — it is how the network grows from a few core rulings to a comprehensive legal system.

---

## 2. Naskh — the Key That Reorders the Network

### 2.1 The mechanism

Naskh (abrogation) is the tool by which a later ruling supersedes an earlier one. It works when two verses appear to conflict:

1. **Identify the conflict** — two verses that give different rulings on the same matter.
2. **Determine the chronology** — which verse was revealed later.
3. **Apply the later** — the later verse abrogates (supersedes) the earlier.

Naskh is the tool that *reorders* the network — it determines which node is in force.

### 2.2 The fighting verse as the master abrogator

The clearest example in the corpus is the "fighting verse" (*ayat al-qital*), Quran 9:5. al-Baghawi's tafsir records a whole list of verses abrogated by it. The pattern is striking: the early Meccan verses of *patience* and *turning away* were abrogated by the later Medinan verse of *fighting*.

The abrogated verses (from al-Baghawi's tafsir):

| Abrogated verse | Content | Abrogated by |
|-----------------|---------|--------------|
| 15:94 | "Proclaim what you are commanded, and turn away from the polytheists" | 9:5 (fighting) |
| 73:10 | "Be patient over what they say, and leave them with a gracious leaving" | 9:5 |
| 88:22 | "You are not a controller over them" | 9:5 |
| 45:14 | "Say to those who believe: forgive those who do not hope for the days of God" | 9:5 |
| 6:159 | "Those who divided their religion... you are not of them in anything" | 9:5 |

The pattern: the early verses commanded **patience, turning away, and non-coercion** toward the polytheists. The later fighting verse (9:5) **abrogated** them, replacing patience with fighting.

### 2.3 The naskh node in the network

This is the deepest demonstration of the network-structure. The same polytheist has radically different standing depending on which node is in force:

```
BEFORE naskh:  patience / turn away / no coercion (15:94, 73:10, 88:22, 45:14)
AFTER naskh:   fighting (9:5) — "no covenant or protection for the polytheists"
```

The *naskh* is the switch that reorders the network. The moral picture is **time-indexed** — it depends on which node the tradition holds to be in force.

### 2.4 The tension with "no compulsion"

The most famous tension is between **Quran 2:256** ("no compulsion in religion") and the fighting verse (9:5). The classical tradition resolved this by naskh: 2:256 was held to be abrogated (or restricted) by the later fighting verse. This is a genuine, contested point — the modern tradition (al-Wasit/Tantawi) reads 9:5 narrowly, restricting it to the treaty-breakers, while the classical tradition read it broadly, abrogating the earlier patience verses.

---

## 3. The Two Keys Together

Qiyas and Naskh are the two master keys of the network:

- **Qiyas extends** — it grows the network by analogy, applying the 'illas to new cases.
- **Naskh reorders** — it changes the network by abrogation, determining which node is in force.

Together they explain how the juridical web is both *generated* (by qiyas) and *governed* (by naskh). The network is not static; it is a living system that grows by analogy and changes by abrogation.

---

## 4. The Cipher, Fully Stated

The full cipher for decoding the Islamic juridical network:

1. **Identify the nodes** — the conditional bridges (IF [condition] THEN [state change]).
2. **Identify the 'illas** — the ratios that ground each node (justice, authority, submission, etc.).
3. **Apply qiyas** — extend the nodes by their 'illas to parallel cases.
4. **Apply naskh** — determine which node is in force by chronology.
5. **Read the links** — the full moral picture emerges only by connecting the nodes.

This is the cipher. It is not a secret — it is the discipline the tradition itself calls *usul al-fiqh* (the principles of jurisprudence). Qiyas and Naskh are two of its master keys.

---

## Footnotes

¹ Quran 5:5, 4:34 — the marriage asymmetry and its 'illa of authority. See §1.2.

² al-Baghawi's tafsir records the verses abrogated by the fighting verse (9:5): 15:94, 73:10, 88:22, 45:14, 6:159, and others. See §2.2.

³ Quran 2:256 ("no compulsion") vs. 9:5 (fighting) — the naskh tension. See §2.4.

---

*Written with the assistance of the Islamic Consultant — a retrieval tool grounded in the original Arabic.*
