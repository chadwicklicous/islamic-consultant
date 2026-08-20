#!/usr/bin/env python3
"""Build a concordance of the Quran's jurisprudential "node" structure.

Refined: token-based matching with clitic stripping, so a term matches only
as a whole word (with attached Arabic clitics), not as a substring inside a
longer word. This eliminates false positives like jizya (جزية) matching
jaza' (جزاء, "recompense") — they share letters but are different words.

Output: concordance/nodes.tsv  —  verse | particle/term | matched text
        concordance/term_verses.tsv  —  term | verse list
"""
import os, re, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
QURAN = os.path.join(BASE, 'text', 'quran.tsv')
OUT_DIR = os.path.join(BASE, 'concordance')
os.makedirs(OUT_DIR, exist_ok=True)

# Diacritic marks to strip
DIACRITICS = set()
for cp in range(0x064B, 0x065F + 1):
    DIACRITICS.add(chr(cp))
DIACRITICS.add('\u0670')  # superscript alef
DIACRITICS.add('\u0640')  # tatweel

def normalize(text):
    """Strip diacritics and normalize alef/ya variants. Keep ta marbuta (ة)
    distinct — do NOT convert it to ha, or feminine nouns break."""
    text = ''.join(c for c in text if c not in DIACRITICS)
    text = text.replace('\u0623', '\u0627').replace('\u0625', '\u0627')
    text = text.replace('\u0622', '\u0627').replace('\u0671', '\u0627')
    text = text.replace('\u0649', '\u064A')  # alef-maqsura -> ya
    return text

# Common Arabic clitics to strip (prefixes and suffixes)
PREFIXES = ['وال', 'فال', 'بال', 'كال', 'لل', 'ال', 'و', 'ف', 'ب', 'ل', 'ك', 'س', 'أ', 'ا']
SUFFIXES = ['هما', 'هم', 'هن', 'كما', 'كم', 'كن', 'ها', 'ه', 'ك', 'ي', 'نا']

def strip_clitics(token):
    """Strip common Arabic clitics from a token, returning the core word."""
    core = token
    # Strip prefixes (longest first)
    for p in PREFIXES:
        if core.startswith(p):
            core = core[len(p):]
            break
    # Strip suffixes (longest first)
    for s in SUFFIXES:
        if core.endswith(s) and len(core) > len(s) + 1:
            core = core[:-len(s)]
            break
    return core

def token_matches(token, term):
    """Check if a token matches a term (whole-word, with clitics stripped)."""
    core = strip_clitics(token)
    return core == term

# Conditional particles (normalized forms) — these are matched as substrings
# because they are grammatical particles, not content words.
PARTICLES = {
    'in (if)': 'ان',
    'fa (then)': 'ف',
    'hatta (until)': 'حتى',
    'illa (except)': 'الا',
    'idha (when)': 'اذا',
    'law (if-counterfactual)': 'لو',
    "la'alla (perhaps)": 'لعل',
}

# Node-connector terms (normalized) — matched as whole words via token matching
TERMS = {
    'ma malakat aymanukum (what your right hands possess)': 'ما ملكت ايمانكم',
    'fitnah (persecution/trial)': 'فتنة',
    'jizya (poll tax)': 'جزية',
    'amanah (trust)': 'امانة',
    'qital (fighting)': 'قتال',
    'qatl (killing)': 'قتل',
    'salam (peace)': 'سلام',
    'sulh (reconciliation)': 'صلح',
    'ahd (covenant/treaty)': 'عهد',
    'dhimma (protection)': 'ذمة',
    'tawba (repentance)': 'توبة',
    'rahma (mercy)': 'رحمة',
    'huda (guidance)': 'هدى',
    'tawfiq (enabling)': 'توفيق',
    'ruh (spirit)': 'روح',
    'nikah (marriage)': 'نكاح',
    'zawj (spouse)': 'زوج',
    'yatim (orphan)': 'يتيم',
    'armala (widow)': 'ارملة',
    'raqaba (slave/neck)': 'رقبة',
    'abd (servant/slave)': 'عبد',
    'hurr (free)': 'حر',
    'khalifa (vicegerent)': 'خليفة',
    'shirk (associating partners)': 'شرك',
    'iman (faith)': 'ايمان',
    'kufr (disbelief)': 'كفر',
    'zulm (oppression)': 'ظلم',
    'adl (justice)': 'عدل',
    'qisas (retaliation)': 'قصاص',
    'diyya (blood-money)': 'دية',
    'hadd (limit/punishment)': 'حد',
    'haram (forbidden)': 'حرام',
    'halal (lawful)': 'حلال',
    'fard (obligation)': 'فرض',
    'wajib (obligatory)': 'واجب',
    'sunnah (way/practice)': 'سنة',
    'sharia (law)': 'شريعة',
    'hukm (ruling)': 'حكم',
    'amr (command)': 'امر',
    'nahy (prohibition)': 'نهى',
    'talaq (divorce)': 'طلاق',
    'riba (usury/interest)': 'ربا',
    'zina (adultery/fornication)': 'زنا',
    'khamr (wine/intoxicant)': 'خمر',
    'mahr (dower)': 'مهر',
    'sadaqa (charity)': 'صدقة',
    'zakat (alms)': 'زكاة',
    'nisaa (women)': 'نساء',
    "mar'a (woman)": 'امراة',
    'kafir (unbeliever)': 'كافر',
    'ahl al-kitab (People of the Book)': 'اهل الكتاب',
    "mu'min (believer)": 'مومن',
    'muslim (one who submits)': 'مسلم',
    'shahid (witness)': 'شاهد',
    'hijab (veil/barrier)': 'حجاب',
    'awra (nakedness)': 'عورة',
    'qawwam (maintainer)': 'قوام',
    'daraba (strike)': 'ضرب',
    'nushuz (rebellion)': 'نشوز',
    'idda (waiting period)': 'عدة',
    'mahr (dower)': 'مهر',
    'mirath (inheritance)': 'ميراث',
    'wasiyya (bequest)': 'وصية',
    'shahada (testimony)': 'شهادة',
    'qawama (guardianship)': 'قوامة',
}


def main():
    with open(QURAN, encoding='utf-8') as f:
        lines = f.readlines()

    norm_lines = []
    for line in lines:
        if '\t' not in line:
            continue
        ref, text = line.rstrip('\n').split('\t', 1)
        norm_lines.append((ref, text, normalize(text)))

    matches = []
    for ref, text, norm in norm_lines:
        # Particles: substring match (grammatical particles)
        for pname, pform in PARTICLES.items():
            if pform in norm:
                matches.append((ref, f'PARTICLE:{pname}', text.strip()))
        # Terms: token-based whole-word match
        tokens = norm.split()
        for tname, tform in TERMS.items():
            nterm = normalize(tform)
            if any(token_matches(tok, nterm) for tok in tokens):
                matches.append((ref, f'TERM:{tname}', text.strip()))

    out = os.path.join(OUT_DIR, 'nodes.tsv')
    with open(out, 'w', encoding='utf-8') as f:
        for ref, kind, text in matches:
            f.write(f'{ref}\t{kind}\t{text}\n')

    from collections import Counter
    kinds = Counter(k for _, k, _ in matches)
    print(f"Total matches: {len(matches)}")
    print(f"Verses with matches: {len(set(r for r,_,_ in matches))}")
    print("\nMatch counts by particle/term:")
    for k, c in kinds.most_common():
        print(f"  {c:5d}  {k}")

    term_verses = {}
    for ref, kind, text in matches:
        if kind.startswith('TERM:'):
            term = kind[5:]
            term_verses.setdefault(term, set()).add(ref)
    out2 = os.path.join(OUT_DIR, 'term_verses.tsv')
    with open(out2, 'w', encoding='utf-8') as f:
        for term in sorted(term_verses):
            verses = sorted(term_verses[term], key=lambda r: (int(r.split()[1].split(':')[0]), int(r.split()[1].split(':')[1])))
            f.write(f'{term}\t{", ".join(verses)}\n')
    print(f"\nWrote {out}")
    print(f"Wrote {out2}")


if __name__ == '__main__':
    main()
