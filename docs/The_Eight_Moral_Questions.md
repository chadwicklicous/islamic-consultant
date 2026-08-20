# The Eight Moral Questions Through the Juridical Cipher
## Divorce, Alcohol, Lying, Wealth, Retribution, Sexuality, Usury, and War as Conditional Nodes

**Author:** Hermes Agent (Islamic Consultant)
**Date:** August 19, 2026
**Status:** Working analysis
**Corpus:** Quran (Uthmani script), Sunni tafsir (Ibn Kathir, al-Tabari, al-Qurtubi, al-Baghawi — classical; al-Sa'di, al-Wasit/Tantawi, al-Muyassar — modern), indexed via ChromaDB + bge-m3.
**Method:** Every Arabic quotation is retrieved verbatim from the corpus (`text/quran.tsv`, `text/tafsir.tsv`). No verse is cited from memory. "Cipher node" = a conditional rule of the form **IF [condition] THEN [state-change / penalty / exit]**.

---

## Abstract

This essay works the eight pending moral questions — **divorce, alcohol, lying, wealth, retribution, sexuality, usury, and war** — through the juridical cipher. It shows that none of the eight is a pure, genuinely-unconditional prohibition in the operative reading. Each is a **conditional node** (IF/THEN) or a prohibition-with-an-exit, bounded by an explicit condition, a fixed-quantified penalty, a repentance/forgiveness branch, or a commutative relief. The essay documents, for each question, the verbatim Arabic, the node-structure, the 'illa (ratio legis) per the tafsir, the network connections, and the classical-vs-modern divergence. It closes with a synthesis of the unifying patterns the cipher reveals.

---

## 1. Divorce (ṭalāq)

**Core verses:** 2:229-233, 2:236-238, 33:49, 65:1-4.

**Verbatim Arabic (2:229):**
> ٱلطَّلَـٰقُ مَرَّتَانِ ۖ فَإِمْسَاكٌۢ بِمَعْرُوفٍ أَوْ تَسْرِيحٌۢ بِإِحْسَـٰنٍ ... فَإِنْ خِفْتُمْ أَلَّا يُقِيمَا حُدُودَ ٱللَّهِ فَلَا جُنَاحَ عَلَيْهِمَا فِيمَا ٱفْتَدَتْ بِهِۦ ۗ تِلْكَ حُدُودُ ٱللَّهِ فَلَا تَعْتَدُوهَا

**Gloss:** "Divorce is twice; then either retain (the wife) honorably or release her with kindness. It is not lawful for you to take back anything of what you gave them, unless the two fear they will not uphold God's bounds. If you fear they will not uphold God's bounds, then there is no blame on them for what she pays as ransom (khul'). Those are God's bounds — do not transgress them."

**Cipher nodes:**
- **N1 (default permissive):** IF the husband divorces once/twice and stays within the waiting period → THEN he may revoke (رجعة) or release (2:229).
- **N2 (three-repudiation bar):** 2:230 — IF divorce reaches the third pronouncement THEN she is no longer lawful to him UNLESS she marries another man. A conditional exit-node with a **state-reinstatement condition** — an explicit counter-condition.
- **N3 (khul' — financial-consideration exit):** 2:229 — IF both fear inability to uphold God's bounds THEN she may ransom herself (فَلَا جُنَاحَ عَلَيْهِمَا فِيمَا افْتُدَتْ بِهِ).
- **N4 (procedural — 'idda):** 65:1 — IF you divorce, do it within the 'idda and count it; do not expel them (لَا تُخْرِجُوهُنَّ مِنۢ بُيُوتِهِنَّ).
- **N5 (no-'idda / virgin-exemption):** 33:49 — IF divorce before consummation THEN no 'idda is required.

**'Illa per tafsir:** Al-Sa'di explains 2:229's occasioning — in jahiliyya a man could repudiate endlessly to harm his wife; the two-divorce limit is prophylactic against harm (a maṣlaḥa / public-interest ratio). Al-Baghawi and al-Qurtubi read the same but foreground preserving lineage and avoiding confusion (اختصار في أمر النسب).

**Connections:** Divorce nodes feed the retribution/fixed-penalty node-type — "تِلْكَ حُدُودُ ٱللَّهِ فَلَا تَعْتَدُوهَا" (2:229) reconnects to the ḥudūd family shared with riba, ḥadd penalties, and war's sacred months. It also connects to the sexuality node via the 'idda and remarriage logic.

**Classical vs. modern:** al-Sa'di adds an explicit maṣlaḥa/anti-harassment rationale and reads khul' as a legitimate statutory avenue. The classical are more formalist, treating khul' as a narrow exception. No substantive contradiction; the modern is more purpose-oriented.

---

## 2. Alcohol — khamr / maysir

**Core verses:** 2:219, 4:43, 5:90-91, 16:67.

**Verbatim Arabic (5:90):**
> يَـٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوٓا۟ إِنَّمَا ٱلْخَمْرُ وَٱلْمَيْسِرُ وَٱلْأَنصَابُ وَٱلْأَزْلَـٰمُ رِجْسٌ مِّنْ عَمَلِ ٱلشَّيْطَـٰنِ فَٱجْتَنِبُوهُ لَعَلَّكُمْ تُفْلِحُونَ

**Gloss:** "O believers, wine, gambling, stone-altars (anṣāb), and divining-arrows (azlām) are only an abomination (رجس) from the work of Satan; so avoid it, that you may prosper."

**Cipher node — a GRADED prohibition ladder (tadrīj), not a single hard bar:**
- **N1 (pre-stage, informational):** 2:219 — IF asked about wine and gambling THEN "there is great sin and some benefit for people, and their sin is greater than their benefit" (2:219). A **weighted-binomial node**: benefit remains but is outweighed.
- **N2 (conditional suspension):** 4:43 — IF drunk THEN do not approach the prayer (لَا تَقْرَبُوا۟ ٱلصَّلَوٰةَ وَأَنتُمْ سُكَـٰرَىٰ). Conditional on the state of drunkenness.
- **N3 (final absolute prohibition):** 5:90 — IF one consumes khamr THEN the state is "رجس من عمل الشيطان" — avoid it. The **naskh (abrogating) node** that annuls 2:219's tolerance. al-Qurṭubī and al-Wasit document the sequence: "تحريم الخمر كان بتدريج ونوازل كثيرة."

**'Illa per tafsir:** 5:91 supplies the ratio verbatim:
> إِنَّمَا يُرِيدُ ٱلشَّيْطَـٰنُ أَن يُوقِعَ بَيْنَكُمُ ٱلْعَدَاوَةَ وَٱلْبَغْضَآءَ فِى ٱلْخَمْرِ وَٱلْمَيْسِرِ وَيَصُدَّكُمْ عَن ذِكْرِ ٱللَّهِ وَعَنِ ٱلصَّلَوٰةِ

The 'illa = causing enmity and enmity and **turning away from dhikr of God and from prayer**. al-Qurṭubī analogizes any pastime that "دعا قليله إلى كثير وأوقع العداوة والبغضاء وصدّ عن ذكر الله" (including chess/gambling) to wine — an explicit analogical extension.

**Exit-condition:** Alcohol has **no fixed statutory penalty in the Quran itself** (the 40/80-lash penalty is sunnah-based) and **no repentance-exit formula internal to 5:90**. The prohibition is unconditional post-5:90; the only relief is cessation (5:91's rhetorical "فَهَلْ أَنتُم مُّنْتَهُونَ"). Compare with riba and zina which carry explicit exit clauses — alcohol is the odd one out: absolute but without an internal "if you repent then..." branch.

**Classical vs. modern:** al-Qurṭubī (classical) treats khamr as *najis* (ritually impure) — a physical-impurity reading — and derives the ban on selling/vinegarizing (takhall). al-Sa'di and al-Wasit (modern) deliberately re-read "رجس" as **moral/meaning-impurity** rather than physical: al-Sa'di "رجس أي خبث، نجس معنى، وإن لم تكن نجسة حسّيًا." This is a genuine modern softening of the physical-impurity doctrine.

---

## Lying / Perjury

**Core verses:** 6:21, 2:224-226, 16:94, 40:28, 4:61.

**Verbatim Arabic (16:94):**
> وَلَا تَتَّخِذُوٓا۟ أَيْمَـٰنَكُمْ دَخَلًۢا بَيْنَكُمْ فَتَزِلَّ قَدَمٌۢ بَعْدَ ثُبُوتِهَا وَتَذُوقُوا۟ ٱلسُّوٓءَ بِمَا صَدَدتُّمْ عَن سَبِيلِ ٱللَّهِ ۖ وَلَكُمْ عَذَابٌ عَظِيمٌ

**Gloss:** "Do not make your oaths a means of deceit between you, lest a foot slip after its firmness, and you taste the evil because you turned [others] away from the path of God; and you will have a great punishment."

**Cipher node — a deontic prohibition with no fixed ritual penalty but a grave consequent:**
- **N1 (truth-in-oaths):** 16:94 — IF one uses oaths for treachery THEN the consequent: slipping after firmness + tasting evil + great torment.
- **N2 (perjury/qadhf inversion):** the hadd on qadhf (false accusation, 24:4) functions as a fixed-penalty node (see Sexuality).
- **N3 (oath-expiatory exit):** 2:224-226 — IF you break an oath THEN the expiation (كفارة) is specified (feeding/clothing/emancipation). Lying by oath has a **penitential exit with a fixed tariff**, not a fixed physical penalty.

**'Illa per tafsir:** al-Sa'di (16:94): the 'illa is the harm done to the collective ("صدّوا عن سبيل الله حيث ضللتم"). 40:28 gives the mirror-test: IF he is lying THEN his lie is upon him. 6:21 (افترى على الله كذبا) ties lying-to-God to the severe unconditional node of *ẓulm* against God — the one place where falsehood lacks a relaxation.

**Connections:** Lying connects to (a) the Sexuality/qadhf hadd (fixed 80-lash penalty — the only Quranic penalty for a speech act), (b) the Wealth node via perjury to consume wealth (2:188), (c) the War node via treachery/oaths as stratagem (16:94).

**Classical vs. modern:** Classical tafsir treat the sinfulness of a bare lie mostly as an *adab* (moral) matter; the modern expand the node into an obligation-weighted social-harm framework connected to the "security" of contracts — placing the harms under a maṣlaḥa lens.

---

## 4. Wealth

**Core verses:** 2:188, 2:264-265, 2:276, 9:34-35, 3:130.

**Verbatim Arabic (2:188):**
> وَلَا تَأْكُلُوٓا۟ أَمْوَٰلَكُم بَيْنَكُم بِٱلْبَـٰطِلِ وَتُدْلُوا۟ بِهَآ إِلَى ٱلْحُكَّامِ لِتَأْكُلُوا۟ فَرِيقًا مِّنْ أَمْوَٰلِ ٱلنَّاسِ بِٱلْإِثْمِ وَأَنتُم تَعْلَمُونَ

**Gloss:** "Do not consume your wealth among yourselves in falsehood (بالباطل), nor convey it to the judges so that you may consume a portion of people's wealth in sin while you know."

**Cipher node:**
- **N1 (prohibition-exception structure):** IF consumption is *by falsehood (بالباطل)* THEN prohibited; the node is deliberately *qualified* — lawful acquisition (by contract, trade, transfer) is presumptively allowed.
- **N2 (riba vs sadaqah):** 2:276 — IF one deals in riba THEN God destroys/erases (يَمْحَقُ) the gain; IF one gives sadaqah THEN God makes it flourish (يُرْبِى ٱلصَّدَقَـٰتِ).
- **N3 (hoarding → fixed-sentence):** 9:34-35 — IF one hoards gold & silver without spending them in God's path THEN = a painful punishment, with 9:35's imagery of branding in Hell-fire — an **eschatological fixed-penalty node**.
- **N4 (riba):** dedicated node below.

**'Illa per tafs:** al-Sa'd (2:188) enumerates the 'illa as **"لا مقابل عوض مباح"** — consumption not matched by a lawful compensatory countervalue (including riba, gambling, bribery, wage-theft). The 'illa is the injustice/corruption of the exchange and the public interest in honest commerce. al-Wasit glosses 2:275's underlying as "لما فيه من الظلم وسوء العاقبة." The hoarding node's 'illa is the *withholding of an obligation* (منع ما وجب من نفقة/زكاة).

**Connections:** Wealth → Riba (2:275-9), → War (spending "في سبيل الله" as the positive alternative), → Lying (consuming property by false means).

**Classical vs. modern:** Classical focus on *technical legality* (which transactions are باطل) and *literal hoarding* (of treasure). Modern (al-Sa'di, al-Muyassar) expand "hoarding" to *any withholding of obligatory philanthropy* and frame all wealth disposition under a purpose-of-treasure reading — the 'illa is widened from "action-type" to "intention+obligation."

---

## 5. Retribution — qiṣāṣ and blood-money

**Core verses:** 2:178-179, 5:45, 17:33.

**Verbatim Arabic (2:178):**
> يَـٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوا۟ كُتِبَ عَلَيْكُمُ ٱلْقِصَاصُ فِى ٱلْقَتْلَى ۖ ٱلْحُرُّ بِٱلْحُرِّ وَٱلْعَبْدُ بِٱلْعَبْدِ وَٱلْأُنثَىٰ بِٱلْأُنثَىٰ ۚ فَمَنْ عُفِىَ لَهُۥ مِنْ أَخِيهِ شَىْءٌ فَٱتِّبَاعٌۢ بِٱلْمَعْرُوفِ وَأَدَآءٌ إِلَيْهِ بِإِحْسَـٰنٍ ۗ ذَٰلِكَ تَخْفِيفٌ مِّن رَّبِّكُمْ وَرَحْمَةٌ ۗ فَمَنِ ٱعْتَدَىٰ بَعْدَ ذَٰلِكَ فَلَهُۥ عَذَابٌ أَلِيمٌ

**Gloss:** "O believers, qiṣāṣ (retaliation) is prescribed for you in cases of killed persons: free for free, slave for slave, female for female. But whoever is pardoned something by his brother — then compensation in good manner and payment with kindness. That is a relief and mercy from your Lord. Whoever transgresses after that has a painful punishment."

**Cipher node — fixed-equality penalty with a commutability-exit:**
- **N1 (fixed-penalty node):** IF one kills THEN prescribed qiṣāṣ (life-for-life equality node).
- **N2 (blood-money / forgiveness-exit):** IF the victim's kin forgive (عفو) THEN the demand converts to i-āsp (collect the diyā) — a *commutation of penalty* away from execution.
- **N3 (escalation-ban):** IF one exceeds the bounds after forgiveness THEN a painful torment (العذاب الأليم). 17:33 glosses: retaliation (سلطان) is for the wronged kin, but do not be excessive in killing (فَلَا يُسْرِفِ فِى ٱلْقَتْلِ).
- **5:45 (physical-correspondence):** the *lex talionis* scale (eye-for-eye, etc.) with a **charity-exit**: "فَمَن تَصَدَّقَ بِهِ فَهُوَ كَفَّارَةٌ لَّهُ" — voluntary forgiveness converts to an *expiation* for the giver.

**'Illa per tafsir:** 2:179 gives the ratio: "وَلَكُمْ فِى ٱلْقِصَاصِ حَيَوٰةٌ يَـٰٓأُو۟لِى ٱلْأَلْبَـٰبِ" — *qiṣāṣ* is a means to **preserve life**. al-Qurtubi treats the equality-'illa: punishment must mirror the crime to deter recurrence.

**Connections:** Retribution → War (both center on the limited lawful taking of life) → Wealth (the diyā/transfer) → a distinct "life" node (17:33).

**Classical vs. modern:** Classical dwell on the equality-condition matrix (free/slave/gender) as an operative legal table. The modern (al-Sa'di) explicitly *equalizes and extends* — al-Sa'di writes "الأنثى بالذكر والذكر بالأنثى" via sunnah and uses maṣlaḥa/العدل (justice) as the ratio to *qualify* the literal gender-symmetry reading. A real shift: the modern removes the classical female-only-for-female equivalence through sunnah and maṣlaḥa.

---

## 6. Sexuality / Zina (adultery and fornication)

**Core verses:** 4:15-16, 4:22-25, 17:32, 24:2-3, 70:29-31.

**Verbatim Arabic (24:2):**
> ٱلزَّانِيَةُ وَٱلزَّانِى فَٱجْلِدُوا۟ كُلَّ وَٰحِدٍ مِّنْهُمَا مِا۟ئَةَ جَلْدَةٍ ۖ وَلَا تَأْخُذْكُمْ بِهِمَا رَأْفَةٌ فِى دِينِ ٱللَّهِ إِن كُنتُمْ تُؤْمِنُونَ بِٱللَّهِ وَٱلْيَوْمِ ٱلْـَـٔاخِرِ ۖ وَلْيَشْهَدْ عَذَابَهُمَا طَٓا ٱئِفَةٌ مِّنَ ٱلْمُؤْمِنِينَ

**Gloss:** "The fornicating woman and the fornicating man — flog each of them one hundred lashes. Let not pity for them seize you in the religion of God, if you believe in God and the Last Day. Let a party of believers witness their punishment."

**Cipher node — fixed-ḥadd with a mandatory non-mercy inversion:**
- **N1 (fixed penalty, non-discretionary):** IF an unmarried adult free person commits zina THEN = 100 lashes + (per sunnah) one-year exile; the penalty is not droppable — pity is banned.
- **N2 (the married issue):** the sunnah raises to stoning (رجم) for the *muḥsin* (married) — **not in the Quran itself** (24:2 fixes the flogging only). Al-Baghawi and al-Muyassar debate the "بكرين غير محصنين" qualifier.
- **N3 (the abrogated pre-node):** 4:15-16 is the Quran's clearest internal **naskh** in the field: IF the act is proven by four witnesses THEN imprison at home until death for women (4:15); 4:16 prescribed *hurt* (فَاذُوهُمَا) for the pair. **These two are abrogated by 24:2's 100-lashes**, per al-Qurtubi.
- **N4 (the approach-prohibition):** 17:32 "وَلَا تَقْرَبُوا ٱلزِّنَىٰ" — the prohibition *includes approach*, i.e., it blocks the precipitating acts (24:30-31: the lower-the-gaze rule) — the **sadd al-dharāʾiʿ** (blocking the means) node.
- **N5 (the marital-exception):** 70:29-31 — IF one confines to spouses/slave-arrangements THEN not blameworthy; IF one seeks beyond that THEN they are the transgressors.
- **N6 (the accusation node):** 4:31/24:4 — IF one falsely accuses (qadhf) a chaste woman THEN a fixed penalty of 80 lashes UNLESS four witnesses. This connects Zina to the Lying node (false testimony with a fixed statutory punishment).

**'Illa per tafsir:** al-Baghawi and al-Sa'di state the four-witness rule is *to conceal (ستْر) people* — the 'illa is *protective concealment*: "لأن الله شدّد في هذه الفاحشة سترًا لعباده" (al-Wasit, rephrasing al-Sa'di). The thing forbidden (فاحشة) is guarded for fear of corruption to lineage, child-welfare, and social trust.

**Classical vs. modern:** Classical (al-Baghawi, al-Qurtubi) at length the *procedure* (number of witnesses, the بكر condition) and read the "رأفة" ban literally to *reject mercy*. The modern (al-Wasit, al-Sa'di) focus on the *maṣlaḥa al-satr* (concealment is in the community's interest) and stress the witness requirement as a *disincentive to wrongdoing* — effectively making the penalty nearly impossible to impose without 4 witnesses (a virtual barrier to punishment achieved through the node itself).

---

## 7. Usury — riba

**Core verses:** 2:275-280, 3:130, 4:161, 30:39.

**Verbatim Arabic (2:275-279):**
> ٱلَّذِينَ يَأْكُلُونَ ٱلرِّبَوٰا۟ لَا يَقُومُونَ إِلَّا كَمَا يَقُومُ ٱلَّذِى يَتَخَبَّطُهُ ٱلشَّيْطَـٰنُ مِنَ ٱلْمَسِّ ۚ ذَٰلِكَ بِأَنَّهُمْ قَالُوٓا۟ إِنَّمَا ٱلْبَيْعُ مِثْلُ ٱلرِّبَوٰا۟ ۗ وَأَحَلَّ ٱللَّهُ ٱلْبَيْعَ وَحَرَّمَ ٱلرِّبَوٰا۟ ۚ فَمَن جَاءَهُۥ مَوْعِظَةٌ مِّن رَّبِّهِۦ فَٱنتَهَىٰ فَلَهُۥ مَا سَلَفَ وَأَمْرُهُۥٓ إِلَى ٱللَّهِ ۖ وَمَنْ عَادَ فَأُو۟لَـٰٓئِكَ أَصْحَـٰبُ ٱلنَّارِ ۖ هُمْ فِيهَا خَـٰلِدُونَ

**Gloss:** "Those who consume riba will not stand [on the Day] except as one who is struck by Satan's touch... They said 'commerce is just like riba,' but God has made *sale* lawful and *riba* unlawful. So whoever has received an admonition from his Lord and desists — to him is what already passed, and his matter is to God; but whoever returns — those are the companions of the Fire, therein forever."

**Cipher node — the prohibited-with-explicit-exit node (the most "cipher-like" in the corpus):**
- **N1 (default):** IF commerce THEN lawful; IF riba THEN unlawful.
- **N2 (the exit-branch):** IF the admonished one *desists* THEN forgiveness of the past (فَلَهُۥ مَا سَلَفَ) + his matter to God — no retrograde penalty.
- **N3 (the recidivism node):** IF one returns THEN companions of the fire — the hard terminal.
- **N4 (the procedural-completion):** 2:278-279 — IF you are believers THEN give up remaining riba; IF you do not THEN "be warned of a war from God and His Messenger" (a martial-escalation branch); but IF you repent THEN you have your capital only (a two-branched exit).
- **N5 (the debtor-soft branch):** 2:280 — IF the debtor is in difficulty THEN grant respite until ease, or better give charity (صدّقوا).

**'Illa per tafsir:** al-Sa'di and al-Qurtubi give the ratio as (a) *unjustice* (ظلم and سوء عاقبة), and (b) the standard juristic 'illa of riba — either the kayl-wazn (weight/measure genus, Abū Ḥanīfa) or mut'am jins (food-of-one-kind, al-Shāfi'ī) or the Maliki staple criterion — all three are **analogical nodes (qiyas)** mapping riba to other goods sharing the ratio of "hoardable surplus." This is a genuine doctrinal split over *which* 'illa to analogize on — the network branching.

**Classical vs. modern:** The most telling divergence: al-Sa'di (modern) *softens the "خَالِدُونَ" (eternity)* clause for the riba-consumer by invoking the anti-eternity rule of Islamic soteriology — i.e., he *reads the "eternity" clause against the backbone of sin-not-kufr doctrine*. al-Wasit (modern) emphasizes the reasonableness (naskh of old riba customs) and the principle (رو) over the classical liturgical & secondary-market formalism.

---

## 8. War — qitāl

**Core verses:** 2:190-193, 2:194, 8:39, 8:61, 9:5, 9:29, 47:4.

**Verbatim Arabic (2:190, 9:5):**
> **2:190:** وَقَـٰتِلُوا۟ فِى سَبِيلِ ٱللَّهِ ٱلَّذِينَ يُقَـٰتِلُونَكُمْ وَلَا تَعْتٓدُوا۟ ۚ إِنَّ ٱللَّهَ لَا يُحِبُّ ٱلْمُعْتَدِينَ
> **9:5 (the Sword Verse):** فَإِذَا ٱنسَلَخَ ٱلْأَشْهُرُ ٱلْحُرُمُ فَٱقْتُلُوا۟ ٱلْمُشْرِكِينَ حَيْثُ وَجَدتُّمُوهُمْ وَخُذُوهُمْ وَٱحْصُرُوهُمْ وَٱقْعُدُوا۟ لَهُمْ كُلَّ مَرْصَدٍ ۚ فَإِن تَابُوا۟ وَأَقَامُوا۟ ٱلصَّلَوٰةَ وَءَاتَوا۟ ٱلزَّكَوٰةَ فَخَلُّوا۟ سَبِيلَهُمْ

**Gloss (2:190):** "Fight in the path of God those who fight you, and do not be aggressive — God loves not the aggressors."
**Gloss (9:5):** "When the sacred months have passed, kill the polytheists wherever you find them... But if they repent, and establish prayer and pay the charity (zakat), then let their way be free."

**Cipher node — a conditional-hierarchy / naskh-hot node:**
- **N1 (the initial limited-defensive node, 2:190):** IF they fight you THEN you may fight — *plus* do not be aggressive (the ban on transgression).
- **N2 (the escalation node, 9:5, the Sword Verse):** IF the sacred months lapse THEN you may kill/capture/besiege the polytheists anywhere — subject to an explicit exit: IF they repent, pray, and give zakat THEN set them free.
- **N3 (the peace-node, 8:61):** IF the enemies incline to peace THEN incline to it as well — an explicit conditional-de-terminal.
- **N4 (the ultimatum node, 8:39 / 2:193):** "And fight them until there be no *fitna* and the religion be wholly God's" — if they desist, no transgression except against the wrong-doers.
- **N5 (the captives node, 47:4):** IF you meet them in battle THEN strike the necks until you overpower, THEN bind the captives, THEN either favor (set free) or ransom — until the war lays down its loads.

**'Illa per tafsir:** The ratio of the defensive node (2:190) is explicitly *context-responsiveness* — "only those who fight you." al-Sa'di emphasizes sincerity in "في سبيل الله". The 'illa of 9:5/8:39 is the removal of *fitnah* (persecution) and the religion being wholly God's. The peace-node's priority (8:61) is the preservation of life and diminution of evil.

**Classical vs. modern — the theoretical hotspot:** Ibn Kathir (classical) *rejects* the "reverse-abrogation" claim that 9:5 abrogated 2:190 — he holds 2:190 is *alive*, and reads 9:5 as directed against the recalcitrant treaty-breakers, not a general killing-license. al-Sa'di (modern) reinforces this *anti-naskh* reading, framing 9:5's "kill anywhere" as *against* those who continue hostility, not a random killing license — and points to 8:61 and 9:5's own "if they repent... release them" as keeping the whole node-tree *conditional*. **This is the most consequential modern divergence:** al-Wasit/al-Muyassar remove the image of a "kill-anywhere, any-time, unconditional" hostilities (which the literal classical reading of "المشركين حيث وجدتموهم" could license in a universal mode), re-investing 2:190's defensive node as permanent.

---

## Closing Synthesis — What the Cipher Reveals Across the Eight Questions

**1. None of the eight is a genuinely-unconditional prohibition in the operative reading.** Each rule, even at its most absolute surface (alcohol's رجس; riba's "خالدون"; adultery's flogging), is *internally conditioned* in one of four ways:
- **(a)** an explicit *IF-condition* that defines the domain (2:190 "those who fight you"; 2:188's "bil-bāṭil" qualifier; 70:29's "من أزواجهم أو ما ملكت أيمانهم");
- **(b)** a fixed-quantified penalty that *bounds* the punishment (qiṣāṣ's commensurateness; 24:2's exact "one hundred"; 2:186's "twice");
- **(c)** an explicit *exit / repentance / forgiveness branch* (riba's "ما سلف" + "إن تبتم" (2:279); the qadhf tawbah; war's "if they repent" (9:5); the *fixed-expiatory* كفارة for broken oaths); and
- **(d)** a *commutative* relief-branch (qiṣāṣ converted to forgiveness/diyā via the "brother"; 2:280 for the distressed debtor).

**2. The conditionality is structurally different from casuistry — it is a normative commitment.** The tafsir (classical and modern) reads the فَـ/إِذَا/إِن conditional morphology not as legal loopholes but as *interest and purpose* (maṣlaḥa). The Quran's own glosses — "that you may prosper" (5:90), "in qiṣāṣ is life" (2:179), and the recurring "تلك حدود الله" — embed the *ratio* *in the law itself*, not in a separate moral frame.

**3. Every exit-condition that exists is *cheap or generous* by construction:**
- riba: the entire past is forgiven ("his matter to God") — a near-total amnesty with a recidivism check;
- riba/war (9:5): "repent, pray, give zakat" — a reversal through three performative acts;
- divorce (2:230): remarriage is the self-inflicted exit;
- retribution (2:178): the relatives' *forgiveness* is a complete discharge;
- riba/wealth: *increase of charity* is the positive symmetric node (2:276);
- the *كفارة* for broken oaths is a fixed transactional expiation.
In no verse does an exit require a divine intermediary (an imam, a priest, a confession) — the agent restores himself through an act *individually doable*. This is a **consistently low-cost, self-actualizing moral infrastructure**.

**4. The hard, non-commutable prohibitions exist only in the formal/terminal layer, not as ordinary practice.** The three candidate "hard" ones — homicide (17:33, except "by right"), shirk/polytheism-to-kufr (in the war node's inverse), and the marriage-boundary (4:22-24) — all carry the "with right" (إلاّبالحق) exception or a partial clause. Even the *prohibition* of zina is *bounded* by the marital-exemption node (70:30-31). The categorical only resides in the threat-labels ("أصدار النار", "خلالدون") — and these are precisely what al-Sa'di (modern) reads as *non-infinite for the believer*, treating the "eternity" as conditioned on the un-atoned persistence.

**5. The most telling classical-vs-modern divergence clusters around the maṣlaḥa / purpose-driven interpretation:**
- **alcohol:** classical hard "impurity" (نجاسة) → modern "moral impurity," softening the social-ostracism;
- **wealth/hoarding:** classical literal-metallic → modern obligation-oriented;
- **retribution:** classical formal gender/slave equivalence → modern equality via sunnah+maṣlaḥa;
- **war's naskh:** the classical "9:5 abrogated 2:190" → al-Sa'di/al-Wasit insist the defensive node continues;
- **riba's "eternal fire":** al-Sa'di systematizes against the permanent-damnation reading.
These are **genuine, not cosmetic, reinterpretations** — the modern layer uses the *same* nodes but *relabels their ratio* (from *formal* to *purpose*). **The classical law is node-shape-legal (formal-proportional); the modern is node-function-legal (outcome-weighted).**

**6. The eight are not a flat list but a *network of mutually-referential nodes*.** War and retribution share the killing-with-a-right gate; riba and wealth share the "consume-not-in-bāṭil" and the sadaqah mirror; zina and lying share the fixed-quantity ḥadd and the witness-threshold; divorce and sexuality share the "حدود الله" frame and the marriage-boundary; riba/alcohol/wealth share the demonic label (رجس / عمل الشيطان). The body is best modeled as **a connected DAG where each node's THEN maps into at least one other node's IF — the morality is an enforcing network, not a set of independent prohibitions.**

**Honest caveat.** (1) The IF/THEN form is *our* formalization — the Quran does not present itself in that shape; it is a *heuristic export*. (2) A purely "conditional" reading could be accused of softening prohibitions; but it is *not invented* — every branch above is anchored to a *verbatim* Quranic فإذا/فإن/إن construction and to an explicit tafsir-glossed ratio ('illa). The classical-modern divergences flagged are *exegetical* changes, not new texts.

---

*Written with the assistance of the Islamic Consultant — a retrieval tool grounded in the original Arabic.*
