#!/usr/bin/env python3
"""Canonical-grade vocabulary for the Islamic consultant.

Muslims do not treat all hadith and historical reports as equally authoritative.
The tradition grades reports on a spectrum of reliability, and the consultant now
carries that grading so it can distinguish canonical law-bearing hadith from
historical reports that give context but are not canonical for those who practice
the faith.

This vocabulary is applied to every citation in the consultant as a `grade` tag.
Two dimensions are tracked:

1. The **hadith science grade** (reliability of the report itself).
2. The **source class** (whether the work is a canonical hadith collection, a
   historical/biographical work, or a jurisprudential work).

The Arabic narrator grades are:
  ثقة (thiqah)     — trustworthy, reliable
  صدوق (saduq)     — truthful, mostly reliable
  ضعيف (da'if)     — weak, unreliable
  كذاب (kadhdhab)  — liar, a fabricator

The hadith report grades are:
  صحيح (sahih)     — sound, authentic
  حسن (hasan)      — good, reliable but slightly weaker
  ضعيف (da'if)     — weak
  موضوع (mawdu')   — fabricated

The source classes are:
  canonical       — one of the Kutub al-Sittah (Bukhari, Muslim, Abu Dawud,
                    Tirmidhi, Nasai, Ibn Majah) or a recognized sahih work
  historical      — biographical/historical works (Ibn Hisham's Sira,
                    Ibn Sa'd's Tabaqat, al-Azraqi's Akhbar Makka) that record
                    the Prophet's life but are NOT part of the canonical hadith
                    corpus. These give context but are not authoritative for
                    legal practice.
  tafsir          — Quranic commentary
  sufi            — devotional/mystical works
"""

# ---------------------------------------------------------------------------
# The grading vocabulary
# ---------------------------------------------------------------------------

# Narrator grades (jarh wa ta'dil) — reliability of a transmitter
NARRATOR_GRADES = {
    "thiqah":   {"en": "trustworthy", "ar": "ثقة",    "def": "reliable"},
    "saduq":    {"en": "truthful",    "ar": "صدوق",   "def": "mostly reliable"},
    "da'if":    {"en": "weak",        "ar": "ضعيف",   "def": "unreliable"},
    "kadhdhab": {"en": "liar",        "ar": "كذاب",   "def": "a fabricator"},
}

# Hadith report grades — authenticity of the report itself
REPORT_GRADES = {
    "sahih":   {"en": "sound",   "ar": "صحيح", "def": "authentic, meets the strictest criteria"},
    "hasan":   {"en": "good",    "ar": "حسن",  "def": "reliable but slightly weaker than sahih"},
    "da'if":   {"en": "weak",    "ar": "ضعيف", "def": "a flaw in the chain or text"},
    "mawdu'":  {"en": "fabricated", "ar": "موضوع", "def": "a forgery, rejected outright"},
}

# Source classes — where a report comes from
SOURCE_CLASSES = {
    "canonical": {
        "en": "canonical", "ar": "معتبر",
        "def": ("One of the Kutub al-Sittah (Bukhari, Muslim, Abu Dawud, Tirmidhi, "
                "Nasai, Ibn Majah) or a recognized sahih collection. Authoritative "
                "for both belief and legal practice."),
        "examples": ["Sahih al-Bukhari", "Sahih Muslim", "Sunan Abu Dawud",
                     "Jami at-Tirmidhi", "Sunan an-Nasai", "Sunan Ibn Majah",
                     "Riyad as-Salihin", "Muwatta Malik", "Mishkat al-Masabih"],
        "weight": "canon",
    },
    "historical": {
        "en": "historical", "ar": "تاريخي",
        "def": ("Biographical/historical works that record the Prophet's life and "
                "give context to the revelation, but are NOT part of the canonical "
                "hadith corpus. They may contain weak (da'if) chains. Useful for "
                "context; NOT authoritative for legal practice."),
        "examples": ["Sira Ibn Hisham", "Ibn Sa'd Tabaqat (al-Tabaqat al-Kubra)",
                     "al-Azraqi Akhbar Makka"],
        "weight": "context",
    },
    "tafsir": {
        "en": "commentary", "ar": "تفسير",
        "def": "Quranic commentary/exegesis.",
        "examples": ["Ibn Kathir", "al-Tabari", "al-Qurtubi", "al-Baghawi"],
        "weight": "context",
    },
    "sufi": {
        "en": "devotional", "ar": "تصوف",
        "def": "Devotional/mystical works.",
        "examples": ["Ihya Ulum al-Din"],
        "weight": "context",
    },
}

# A report can be canonical but weak (a hadith in Bukhari is sahih, but a hadith
# in a biographical work may be da'if). The `grade` field carries the report
# grade; the `source_class` field carries where it comes from.

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SOURCE_CLASS_BY_FILE = {
    "hadith.tsv": "canonical",
    "sira.tsv": "historical",
    "tabaqat.tsv": "historical",
    "quran.tsv": "canonical",      # the Quran itself is canonical revelation
    "tafsir.tsv": "tafsir",
    "sufi.tsv": "sufi",
}


def source_class_for(file_or_citation):
    """Return the source_class for a text file or a citation string."""
    if "/" in file_or_citation or ".tsv" in file_or_citation:
        fname = file_or_citation.split("/")[-1]
        for key, cls in SOURCE_CLASS_BY_FILE.items():
            if fname == key:
                return cls
        return "historical"  # default for biographical corpora
    # citation string like "Sira Ibn Hisham | X | sira"
    low = file_or_citation.lower()
    if "bukhari" in low or "muslim" in low or "abu dawud" in low \
       or "tirmidhi" in low or "nasai" in low or "ibn majah" in low \
       or "riyad" in low or "muwatta" in low or "mishkat" in low:
        return "canonical"
    if low.startswith("sira") or "tabaqat" in low:
        return "historical"
    if low.startswith("quran"):
        return "canonical"
    if "quran " in low and "|" in file_or_citation:
        return "tafsir"
    return "context"


def grade_for(citation):
    """Return a report-grade hint for a citation.

    This is a heuristic label that the extractors attach; it does NOT replace
    formal hadith-science grading, but it flags on which side of the canon a
    report sits. The most reliable reports are in the canonical collections
    (assumed sahih unless known weak); historical/biographical works are
    explicitly marked da'if-by-default because their chains were not audited
    to the canonical standard.
    """
    cls = source_class_for(citation)
    if cls == "canonical":
        return "sahih"       # in a canonical collection; assume sound
    if cls == "historical":
        return "da'if"       # biographical works contain weak chains; flag as non-canonical
    return "context"         # tafsir/sufi


# ---------------------------------------------------------------------------
# CLI summary
# ---------------------------------------------------------------------------

def describe():
    """Print the vocabulary as a reference table."""
    lines = ["CANONICAL-GRADE VOCABULARY", "=" * 40]
    lines.append("\nHadith report grades:")
    for k, v in REPORT_GRADES.items():
        lines.append(f"  {v['ar']} ({k}) - {v['en']}: {v['def']}")
    lines.append("\nNarrator grades (jarh wa ta'dil):")
    for k, v in NARRATOR_GRADES.items():
        lines.append(f"  {v['ar']} ({k}) - {v['en']}: {v['def']}")
    lines.append("\nSource classes:")
    for k, v in SOURCE_CLASSES.items():
        lines.append(f"  {v['ar']} ({k}) - {v['en']}: {v['def']}")
    lines.append("\nBy file:")
    for f, cls in SOURCE_CLASS_BY_FILE.items():
        lines.append(f"  {f} -> {cls}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(describe())
