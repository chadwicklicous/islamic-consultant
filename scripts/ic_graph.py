#!/usr/bin/env python3
"""Build a co-occurrence graph of the Quran's node-connector terms.

Two terms that appear in the SAME verse are linked — this reveals the
"packets" (clusters of interconnected nodes) in the jurisprudential network.

Also detects "conditional nodes": verses containing BOTH a conditional
particle (in/fa/hatta/illa/idha/law) AND a node-connector term — these are
the actual conditional bridges (IF [condition] THEN [state change]).

Output:
  concordance/cooccurrence.tsv  —  term1 | term2 | shared verse(s)
  concordance/conditional_nodes.tsv  —  verse | particle | term | text
"""
import os, re, unicodedata
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
QURAN = os.path.join(BASE, 'text', 'quran.tsv')
OUT_DIR = os.path.join(BASE, 'concordance')
os.makedirs(OUT_DIR, exist_ok=True)

DIACRITICS = set()
for cp in range(0x064B, 0x065F + 1):
    DIACRITICS.add(chr(cp))
DIACRITICS.add('\u0670')
DIACRITICS.add('\u0640')

def normalize(text):
    text = ''.join(c for c in text if c not in DIACRITICS)
    text = text.replace('\u0623', '\u0627').replace('\u0625', '\u0627')
    text = text.replace('\u0622', '\u0627').replace('\u0671', '\u0627')
    text = text.replace('\u0649', '\u064A')
    return text

PREFIXES = ['وال', 'فال', 'بال', 'كال', 'لل', 'ال', 'و', 'ف', 'ب', 'ل', 'ك', 'س', 'أ', 'ا']
SUFFIXES = ['هما', 'هم', 'هن', 'كما', 'كم', 'كن', 'ها', 'ه', 'ك', 'ي', 'نا']

def strip_clitics(token):
    core = token
    for p in PREFIXES:
        if core.startswith(p):
            core = core[len(p):]
            break
    for s in SUFFIXES:
        if core.endswith(s) and len(core) > len(s) + 1:
            core = core[:-len(s)]
            break
    return core

PARTICLES = {
    'in (if)': 'ان',
    'fa (then)': 'ف',
    'hatta (until)': 'حتى',
    'illa (except)': 'الا',
    'idha (when)': 'اذا',
    'law (if-counterfactual)': 'لو',
    "la'alla (perhaps)": 'لعل',
}

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
}


def main():
    with open(QURAN, encoding='utf-8') as f:
        lines = f.readlines()

    # For each verse, find which terms and particles it contains
    verse_terms = {}   # ref -> set of term names
    verse_particles = {}  # ref -> set of particle names
    verse_text = {}

    for line in lines:
        if '\t' not in line:
            continue
        ref, text = line.rstrip('\n').split('\t', 1)
        norm = normalize(text)
        tokens = norm.split()

        terms_here = set()
        for tname, tform in TERMS.items():
            nterm = normalize(tform)
            if any(strip_clitics(tok) == nterm for tok in tokens):
                terms_here.add(tname)

        particles_here = set()
        for pname, pform in PARTICLES.items():
            if pform in norm:
                particles_here.add(pname)

        if terms_here:
            verse_terms[ref] = terms_here
            verse_text[ref] = text.strip()
        if particles_here:
            verse_particles[ref] = particles_here

    # 1. Co-occurrence graph: terms sharing a verse
    cooccur = defaultdict(lambda: defaultdict(set))  # term1 -> term2 -> set of verses
    for ref, terms in verse_terms.items():
        terms = sorted(terms)
        for i in range(len(terms)):
            for j in range(i+1, len(terms)):
                cooccur[terms[i]][terms[j]].add(ref)
                cooccur[terms[j]][terms[i]].add(ref)

    out1 = os.path.join(OUT_DIR, 'cooccurrence.tsv')
    with open(out1, 'w', encoding='utf-8') as f:
        f.write('term1\tterm2\tshared_verses\n')
        seen = set()
        for t1 in sorted(cooccur):
            for t2 in sorted(cooccur[t1]):
                if (t2, t1) in seen:
                    continue
                seen.add((t1, t2))
                verses = sorted(cooccur[t1][t2])
                f.write(f'{t1}\t{t2}\t{", ".join(verses)}\n')

    # 2. Conditional nodes: verse has BOTH a particle AND a term
    out2 = os.path.join(OUT_DIR, 'conditional_nodes.tsv')
    with open(out2, 'w', encoding='utf-8') as f:
        f.write('verse\tparticle\tterm\ttext\n')
        for ref in sorted(verse_terms, key=lambda r: (int(r.split()[1].split(':')[0]), int(r.split()[1].split(':')[1]))):
            if ref in verse_particles:
                for p in sorted(verse_particles[ref]):
                    for t in sorted(verse_terms[ref]):
                        f.write(f'{ref}\t{p}\t{t}\t{verse_text[ref]}\n')

    # Summary
    print(f"Verses with terms: {len(verse_terms)}")
    print(f"Co-occurrence edges: {sum(len(v) for v in cooccur.values()) // 2}")
    print(f"Conditional nodes (verse+particle+term): {sum(len(verse_particles.get(r,[])) * len(verse_terms[r]) for r in verse_terms if r in verse_particles)}")
    print(f"\nWrote {out1}")
    print(f"Wrote {out2}")

    # Show the densest co-occurrences (the "packets")
    print("\n=== Densest co-occurrences (node packets) ===")
    edges = []
    for t1 in cooccur:
        for t2 in cooccur[t1]:
            if t1 < t2:
                edges.append((len(cooccur[t1][t2]), t1, t2))
    edges.sort(reverse=True)
    for count, t1, t2 in edges[:25]:
        print(f"  {count:3d} verses: {t1}  <->  {t2}")


if __name__ == '__main__':
    main()
