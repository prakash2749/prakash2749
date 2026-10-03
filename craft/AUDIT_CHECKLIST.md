# Audit Checklist — *The Blood Code*

The instrument. Run per chapter, then per book.

**Thresholds:** no chapter below **7** on any metric. Book average **8+**. A chapter below 7 on cliffhanger gets rewritten. A chapter below 8 on voice distinction gets a metaphor-system pass.

A score is only useful if 7 and 8 mean different things, so every metric below has anchors. **Score against the anchor, not against how the chapter felt to write.**

---

## 1. The seven metrics

### 1 · Opening hook

| | |
|---|---|
| **10** | First line reframes something, threatens something, or lands a reveal. Unputdownable cold. |
| **8** | First line puts the reader mid-action or mid-tension. No orientation needed. |
| **7** | First line is concrete and specific but static — a place, a state. |
| **5** | Orientation, weather, waking up, or a recap of the previous chapter. |

**Fail markers:** the narrator wakes up · the chapter opens on a summary of where we are · the first sentence exceeds 14 words.

### 2 · Pacing

| | |
|---|---|
| **10** | Every paragraph earns its place. Cut nothing without losing something. |
| **8** | One soft paragraph. Everything else pulls. |
| **7** | A short stretch of exposition or blocking that could be compressed. |
| **5** | Recap, a conversation that restates known facts, or a travel sequence. |

**Fail markers:** any fact restated that the reader already has · an established duration repeated (*four years* twice in a chapter) · a scene whose plot function duplicates the previous scene's.

### 3 · Heat

Judged against the chapter's slot, not in absolute terms — a non-explicit chapter can score 10.

| | |
|---|---|
| **10** | Tension or explicit content exactly right for this point, and it advances plot or relationship. |
| **8** | Right level, plot function slightly soft. |
| **7** | Present but thin, or sits a beat behind where the book is. |
| **5** | Absent where the gap has run four chapters, or a scene that could be deleted with no consequence. |

**Gate:** tension by Ch. 3. First explicit scene by Ch. 8. No gap over four chapters. Eleven scenes per book.

### 4 · Cliffhanger ending

**Below 7 = automatic rewrite.**

| | |
|---|---|
| **10** | A revelation that reframes what was just read, or a new threat arriving in the last line. |
| **8** | A reversal, an unexpected action, or a line that shifts the power dynamic. |
| **7** | Unresolved and forward-leaning, quietly. *"Safe."* qualifies. |
| **5** | The narrator reflects on what happened, states a theme, or settles into a feeling. |

**Fail markers:** the narrator summarizes their own feelings · a settled emotional state · the final paragraph exceeds 10 words without a strong reason (52% target is ≤10 words, 27% at ≤5).

### 5 · Quotable line

| | |
|---|---|
| **10** | Standalone, under 15 words, devastating with zero context. Screenshot-ready. |
| **8** | Strong and standalone, but needs a beat of context. |
| **7** | A good line that only works in place. |
| **5** | Nothing. |

Not every chapter needs one — target **15–25 per book**, spread and unclustered. A 7 here is acceptable if the neighbors are 9s. Bank them in `QUOTABLES.md`.

### 6 · Voice distinction

**Below 8 = metaphor-system pass.** The highest bar in the rubric, because POV collapse is the number-one AI tell in dual POV.

| | |
|---|---|
| **10** | Swap test fails hard. The narrator's system is present as judgment, and the word carrying it never repeats enough to notice. |
| **8** | Swap test fails. System present. |
| **7** | Identifiable by content but not by cognition — you know it's Selene because she's in her apartment, not because of how she thinks. |
| **5** | A paragraph could be worn by another narrator unchanged. |

**Run it:** take two random narration paragraphs, put another narrator's name on them. Both must fail. Procedure in `series/VOICE_BIBLE.md` §5.

**Highest-risk zone: tender scenes.** Both characters vulnerable drifts toward a shared register. One anchor metaphor per page of tender content.

### 7 · Tense consistency

Binary. **10 or 0.**

First person, present tense, no drift. Past-tense verbs are legitimate only for genuinely prior events. One slipped sentence is a defect, not a 9.

```powershell
# candidate drift — narration past-tense verbs outside dialogue
$n = [regex]::Replace((Get-Content $file -Raw), '"[^"]*"', '')
([regex]::Matches($n, '(?i)\bI (was|had|felt|knew|said|walked|looked|thought)\b')) |
  ForEach-Object { $_.Value } | Group-Object | Sort-Object Count -Descending
```

Review each hit by hand — *I knew what he was* can be legitimate.

---

## 2. Mechanical flags

Pass/fail, not scored. Any flag blocks the chapter.

| Flag | Threshold | Source |
|---|---|---|
| Narration sentence mean | 8–14 words | `STYLE_GUIDE.md` §2 |
| Narration median | ≤12 | §2 |
| Narration ≤14 words | ≥65% | §2 |
| Any narration sentence >25 words | **zero** | §2 |
| Dialogue mean | ≤8 | §2 |
| Single-sentence paragraphs | ≥45% | §2 |
| Paragraphs >4 sentences | **zero** | §2 |
| Semicolons | **zero** | §2 |
| Narration question marks | 8–12 | §2 |
| Fragment runs | ~14, ≈69% sentence-plus-one | §4 |
| Parallel-echo triplets | ≤2 | §4 |
| Banned phrases | **zero** | `BANNED_PHRASES.md` |
| Cardinals per 10K | <30 | §6 |
| Number+measure per 10K | <5 | §6 |
| Bare digits per 10K | <2 | §6 |
| Spatial or social counting in a lead's head | **zero** | §6 |
| American English, incl. double-L | no British forms | §1 |

Scanners: `STYLE_GUIDE.md` §9 and `BANNED_PHRASES.md` §10.

---

## 3. Structural slop — read by hand

No regex catches these and they matter more than the phrase list.

- [ ] Both POVs distinct in tender scenes
- [ ] No emotional over-articulation — the narrator does not accurately diagnose their own psychology
- [ ] No feeling named right after it's shown
- [ ] Sex choreography lopsided, not turn-taking
- [ ] No consent negotiated in clinical language mid-scene
- [ ] Fragment rhythm not over-applied
- [ ] Not every chapter ends on a zinger (52%, not 100%)
- [ ] No abstract tricolons
- [ ] No metaphor explained after it's made
- [ ] No uniform eloquence — villains, young wolves, and functionaries have different ceilings
- [ ] No theme stated in dialogue (`THEMES.md` — the *never on the page* lines)
- [ ] **Cassian interstitials:** does it explain a strategy? Rewrite as a choice.

---

## 4. Per-chapter form

```
CH __  POV: ______  Words: ____ / target ____

  1 Opening hook        __/10
  2 Pacing              __/10
  3 Heat                __/10
  4 Cliffhanger         __/10   <7 = rewrite
  5 Quotable            __/10
  6 Voice distinction   __/10   <8 = metaphor pass
  7 Tense               __/10   binary

  Mechanical flags     PASS / FAIL  ______________________
  Structural slop      PASS / FAIL  ______________________
  Swap test            FAILS CORRECTLY / COLLAPSED
  Seed due?            ____________  two-level test: PASS / FAIL
  Heat row?            ____________  adjacency: __ axes matched (max 1)
  Canon touched?       ____________  logged in CANON_LEDGER: Y / N

  Verdict: SHIP / REWRITE ____________
```

---

## 5. Book-level gates

Run once the full draft exists. These are commercial, and each one is money.

**Opening**
- [ ] Hero present in the first 500 words
- [ ] Ch. 1's ending is the strongest in the first act — it's the Look Inside cliff
- [ ] First three chapters deliver every trope the blurb names

**Heat**
- [ ] Tension by Ch. 3 · first explicit by Ch. 8 · eleven scenes · no gap over four chapters
- [ ] No two consecutive scenes match on more than one axis (`HEAT_MAP.md` adjacency tables)
- [ ] At least one tender scene and one at maximum filth
- [ ] Every scene has a plot function that would be lost if it were cut

**Structure**
- [ ] 95,000–115,000 words · chapter median ~2,500 · explicit chapters 20–35% over
- [ ] Cliffhanger average 8+ · soft reflective endings under 25% of chapters
- [ ] Every chapter ≥7 on every metric

**Series**
- [ ] 15–25 quotables, spread not clustered
- [ ] Next couple seeded by Ch. 20, with 4–6 moments starting in Act 1
- [ ] Every seed passes the two-level test (`SEEDING_MATRIX.md` §10)
- [ ] No character comments on a seed
- [ ] Title appears in text — planted early as metaphor, paid late as transformation
- [ ] Epilogue does not close completely; last paragraph hooks the next book
- [ ] Back matter carries a real 1,000–1,500-word excerpt of the next book's Ch. 1

**Canon**
- [ ] Nothing contradicts `reference/source-bible-v1.md`
- [ ] All fourteen never-contradict rules hold (`CANON_LEDGER.md` §4)
- [ ] New facts logged with the chapter that locks them
- [ ] Every character in a sexual situation is an adult with their age in their sheet

**Book-level number census** — ceilings are measured across the whole book, not per chapter. Chapter spikes are expected; the book total is what's binding.

**Front matter** — author note naming content warnings plainly, no euphemism. Then playlist. Acknowledgments at the back.

---

## 6. Order of operations

Auditing in the wrong order wastes work — fixing prose in a chapter that gets restructured is throwing effort away.

1. **Canon** — contradictions invalidate everything downstream
2. **Structure** — word count, chapter shape, heat placement
3. **Cliffhangers** — rewrites happen here
4. **Voice** — swap test, metaphor passes
5. **Mechanical** — run the scanners
6. **Structural slop** — the hand read
7. **Quotables and seeds** — last, because they move without cost

---

## 7. What a failing chapter looks like

A worked example, so the rubric has a floor to point at.

```
CH 15  POV: Selene  Words: 2,610 / target 2,500

  1 Opening hook        6/10   opens on her making coffee and recapping Ch. 14
  2 Pacing              6/10   three paragraphs re-explaining the pact terms
  3 Heat                7/10   tension present, thin, no scene due
  4 Cliffhanger         4/10   ends "I didn't know what to think anymore."
  5 Quotable            5/10   none
  6 Voice distinction   6/10   no translation beat in 2,600 words
  7 Tense              10/10

  Mechanical flags     FAIL  narration mean 15.2 · 2 semicolons · 1 sentence at 31 words
  Structural slop      FAIL  feeling named twice · one abstract tricolon
  Swap test            COLLAPSED — para 3 wearable by Lucian unchanged
  Verdict: REWRITE
```

**Diagnosis, in order:** the cliffhanger fails (4) so the chapter's ending is rebuilt first. The voice score (6) triggers a metaphor pass — a chapter in Selene's head with no conversion in it isn't her chapter. Pacing and hook are both symptoms of the same cause: the chapter opens by recapping instead of starting. Mechanical flags get fixed last, because the sentences carrying them may not survive the restructure.
