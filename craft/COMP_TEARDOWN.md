# Chapter-wise teardown: *King of Teeth* vs the five #1 comps

Measured 2026-09-26. Every book is split into its own chapters: *Deviant King* (44), *God of Malice* (42), *Kiss the Villain* (41), *Hunt the Villain* (39), *Haunting Adeline* (43), *King of Teeth* (43). Each chapter is scored on explicit terms per 1k words, dialogue share, profanity, question marks, opener and closer. The same regexes as `compare.py` are used throughout.

The scripts live in the session scratchpad (`teardown.py`, `analyze.py`). They report stats only and reproduce no passages.

## Before this pass: where we lost

| | DK | GoM | KtV | HtV | Adeline | **KoT (before)** |
|---|---|---|---|---|---|---|
| Hot units (≥12/1k) | 20% | 36% | 51% | 41% | 44% | 30% |
| Explicit /1k at the **50% decile** | 14.5 | 19.1 | 13.5 | 32.9 | 15.6 | **9.0** (a trough) |
| Question marks /1k | 13.4 | 11.8 | 11.3 | 9.6 | 6.2 | **3.6** (last in every decile) |
| Profanity /1k (book) | 4.7 | 7.0 | 10.1 | 9.1 | 6.4 | **4.1** |
| Closers that are a spoken line | 23% | 2% | 5% | 8% | 21% | 7% |
| Cold-open dialogue openers | 5% | 0% | 20% | 15% | 28% | **2%** |
| Largest gap between hot units | 25% | 17% | 19% | 19% | 10% | 11% |
| Short closers (≤6 words) | 32% | 60% | 32% | 41% | 21% | 49% |

**Loss 1: the midpoint surge.** Every comp runs its hottest or second-hottest decile between 50% and 60%. That's where Kent lands first penetration (Ch. 21 in both het books) and where *Hunt the Villain* peaks at 32.9. Ours dipped to 9.0 there. Nine units between 37% and 60% (Ch. 15, 16, I-3, 18, 20–24) sat **below every comp** at the same position.

**Loss 2: questions.** Questions are how these books carry tension: the heroine interrogating herself, and the hero interrogating her. We had half of Adeline's rate and a quarter of *Deviant King*'s, in every decile.

**Loss 3: cold-open dialogue.** Adeline opens 28% of chapters mid-conversation; we opened 2%.

**Loss 4: quiet interior chapters.** Ch. 5, 6, 8, 9, 10, 31 and 36 ran 7–15% dialogue, below every comp at their position.

**Loss 5: profanity** sat at the floor of the corpus.

**Where we already win:** the largest cold gap (11%, second only to Adeline), heat in the first decile, the late peak (80–90%), short closers, chapter length (the fastest turn of any comp except *Deviant King*), and emotional structure (villain POV, a heroine who witnesses the execution).

## The fix list
1. **Midpoint surge:**
   - Extend Ch. 20 (shower, breath play) and Ch. 23 (Marchand guest room) into full-length scenes.
   - Add charged beats to Ch. 15, 16, 18, 21, 22 and 24, so no unit between 35% and 60% sits below every comp.
2. **Question pass:** reach ≥ 6.5/1k book-wide, beating Adeline, and never finish last in a decile.
3. **Openers:** about six chapters open mid-conversation (target ≥ 14%).
4. **Closers:** about five more end on a spoken line (target ≥ 18%).
5. **Dialogue:** raise Ch. 5, 6, 8, 9, 10 and 36 into their comp band.
6. **Profanity:** move each POV to the top of LO's bands (Selene ~700, Lucian ~410). That beats *Deviant King* and matches Adeline.

## After the pass (2026-09-26, same scripts)

| | DK | GoM | KtV | HtV | Adeline | **KoT before** | **KoT after** |
|---|---|---|---|---|---|---|---|
| Hot units (≥12/1k) | 20% | 36% | 51% | 41% | 44% | 30% | **37%** |
| Explicit /1k at the 50% decile | 14.5 | 19.1 | 13.5 | 32.9 | 15.6 | 9.0 | **13.6** |
| Question marks /1k | 13.4 | 11.8 | 11.3 | 9.6 | 6.2 | 3.6 | **6.5** |
| Cold-open dialogue openers | 5% | 0% | 20% | 15% | 28% | 2% | **16%** |
| Spoken closers | 23% | 2% | 5% | 8% | 21% | 7% | **19%** |
| Short closers (≤6 words) | 32% | 60% | 32% | 41% | 21% | 49% | 44% |
| Largest gap between hot units | 25% | 17% | 19% | 19% | 10% | 11% | **10%** |
| Heat peak (sliding 2k window) | 35.5 | 38.5 | 62 | 57 | 46 | 48.5 | **49** |
| Profanity /1k | 4.7 | 7.0 | 10.1 | 9.1 | 6.4 | 4.1 | 4.4 |

**Now ahead of every comp:** the largest cold gap (tied with Adeline) and first heat (1%).

**Now ahead of Adeline:** questions (6.5 against 6.2), heat peak (49 against 46), and the top three peaks (45.3 against 40.7).

**Now ahead of both Kent het books:**
- Hot share: 37% against *Deviant King* 20% and *God of Malice* 36%.
- Opener and closer craft.
- The midpoint: 13.6 at 50%, no longer the lowest decile in the corpus.

**Still behind, stated plainly:**
1. **Profanity** is last or second-last in most deciles. LO's bands cap it (Selene 550–750, Lucian 300–420), and both POVs sit inside them. Matching Adeline means raising the bands, which is LO's call.
2. **Question density** trails all four Kent books (9.6–13.4). They carry tension in dialogue far more interrogatively.
3. **Overall dialogue share** is 20% against *God of Malice*'s 31%.
4. **Sentence rhythm** (median 8–9) stays outside the corpus by LO's earlier decision.
5. **Hot share** trails *Kiss the Villain* (51%), Adeline (44%) and *Hunt the Villain* (41%). Those are books whose premise runs heat from page 1.

**Continuity fixes found during the teardown:**
- Ch. 17: Selene was present for the lie in Ch. 16, but Ch. 17 had her surprised by it.
- Ch. 34: the west-wing line still had her on the bench after she witnessed the execution.
- Ch. 35: Gaspard's "king of teeth" line repeated Thibault's Ch. 18 explanation word for word.
- Ch. 15: an orphaned line, and the bartender had two lines in a row with no question between them.
- Ch. 25: Selene contradicted herself about who found Cassian's name first.
- Ch. 20: the aftercare order was scrambled.
- Ch. 18: a heat beat didn't match Ch. 19's three-day gap.

## Pass 6 — comp-average targets (2026-09-27)

LO's brief: "win there also" on the five metrics that were still losing. The chosen bar was **beat the comp average**. Measured with `craft/tools/compare.py` (averaged over all six comps), plus exact values from the same regexes:

| Metric | Before pass 6 | Target | Comp avg | **Now** |
|---|---|---|---|---|
| Profanity /1k | 4.4 | 7.1+ | 7.04 | **7.13** |
| Question marks /1k | ~6.5 | 12+ | 9.72 | **12.6** |
| Dialogue share | 20% | 23%+ | 22.3% | **23.1%** |
| Sentence median / share under 11 words | 8–9 / 58–63% | 11+ / ≤45% | 12.3 / 41.8% | **12 / 43%** |
| Hot 2k windows | 36–37% | 42%+ | 39% | **44%** |

What changed:
- **Rhythm.** Every chapter was line-edited by hand: short narration beats merged, while deliberate punches, openers, closers and screenshot lines were kept. The first pass overshot on narration (a chapter median of 16.4 words against the comps' 12.1, measured with `audit.py`'s own segmentation after rejoining the PDF-wrapped comp lines). A splitter then broke 485 long `, and <subject>` chains back into two sentences, only where both halves stand as clauses; 17 list-item fragments it created were rejoined by hand. Narration is now 14.5 words against the comps' 12.1. **This is still longer than the comps. It remains the one open rhythm gap, and `audit.py` flags it per chapter.**
- **Questions, dialogue and profanity** were raised together through short exchanges and interrogative lines in each POV's register: Selene gets shit and blasphemy plus *the fuck*; Lucian gets fuck, bastard and *the hell*. **Cassian stays at zero**, and every interstitial stays within 600–900 words.
- **Heat windows.** Explicit density was added only where a scene already existed: the Ch. 35 crown-night scene now runs as a scene, and the Ch. 27 closer and the Ch. 34 draining carry more density. No new rungs were added to the ladder.
- **Tics.** `damn` fell from 94 to 24 uses, and the rest were rotated to other families. `which is/means` and `the word` are back under their ceilings. All 70 semicolons introduced in the merges were removed (the checklist allows zero). One banned phrase ("looking back") was cut.

Tooling recalibrated from comp evidence (208 comp chapters, fail lines at the comp p10/p90), documented inline in `audit.py`:
- dialogue mean now fails above 11 (comp p90 11.4), and the ≤14-word dialogue share fails below 70% (comp p10 69);
- the narration median fails above 13 and the ≤14-word narration share below 58%;
- the fragment floor is 10 (comp p10 10.5), and single-sentence paragraphs fail below 38% (comp p10 38);
- the question ceiling is `total // 59` (comp p90 16.9/1k);
- the POV profanity bands are Selene 700–950 and Lucian 550–800 (Cassian 0). LO asked for these to be exceeded to reach the comp average.

The narration-mean gate (14) was already at the comp edge, so it was not moved.
