# Style Guide — *The Blood Code*

The register, turned into numbers a draft can be measured against.

**Authority:** `.claude/CLAUDE.md` is the source of every figure here and wins any conflict. This file is the working instrument — the same rules with the measuring built in.

The single most-violated instruction in the whole project is prose register. Assume drift until measured.

---

## 1. Fixed settings

| Setting | Value |
|---|---|
| Person and tense | First person, **present tense** |
| POV | Alternating. Book 1: Lucian · Selene · Cassian (interstitials) |
| Spelling | **American English.** Not just -ize/-or — also the double-L class (*traveled*, *canceled*, *modeled*, *signaled*) and idiom |
| Book length | **95,000–115,000** (widened 2026-09-25: scenes run at Adeline length, tic cuts pay for it — Book 1 landed at ~100k) |
| Chapter baseline | **Median ~2,500 words.** Range 2,000–3,200 |
| Explicit chapters | 20–35% over baseline → **3,000–3,400** |
| Cassian interstitials | 600–900, deliberately short |

**Idiom trap.** *Deviant King* is British — 160 British spellings, zero American, and Kent says so in her author note. Take rhythm, structure, and fragment technique from it. Never take spelling or idiom. *Mum*, *arse*, *grey*, *realise*, *fortnight*, *queue* for a line, *looking round* — all live in that book, all wrong for ours.

---

## 2. Sentence and paragraph targets

Measured across three Kent epubs. These are the real numbers, not approximations.

| Metric | Target | Fail condition |
|---|---|---|
| Narration mean | **~12 words** (comp median 12.1) | over 14 |
| Narration median | **~11 words** | over 13 |
| Narration ≤14 words | **~66%** | under 58% |
| Dialogue mean | **~9 words** (comp 9.3) | over 11 |
| Dialogue median | **5 words** | — |
| Dialogue ≤14 words | **~80%** | under 70% |
| Paragraphs of 1–3 sentences | **93%** | under 88% |
| Paragraphs of exactly 1 sentence | **~56%** | under 38% |
| Narration sentences ≤4 words | **~18%** | under 10% |
| Semicolons | **zero** | any |
| Question marks (total) | **book ≥12/1k** (LO's pass-6 target; comp avg 9.7) | zero in a chapter, or over ~17/1k |

*Recalibrated 2026-09-27* against 208 comp chapters (Kent ×4 and *Haunting Adeline*), measured with `audit.py`'s own segmentation after rejoining the PDF-wrapped lines. Fail lines sit at the comp 10th/90th percentile. The earlier figures came from three Kent epubs, and several of them were stricter than the comps' own median. **Book-level rhythm target (LO, pass 6): whole-book sentence median 11+ and at most 45% under 11 words** (measured by `compare.py`). Book 1 sits at 12 / 43%. Narration still runs longer than the comps (14.5 against 12.1), so shorten narration before lengthening anything else.

**One idea per sentence.** *X, because Y, which means Z* is three sentences. No sentence should need two commas to stay upright. Past ~20 words, break it or cut it.

**Zero question marks in a POV chapter is a failure, not restraint.** A chapter with no self-interrogation is under-pressured. But most of Kent's question marks live in *spoken dialogue* — the interior rate is the 219–291 figure, measured on narration only.

---

## 3. Sex scenes get no extra sentence length

This was wrong in an earlier draft of the project rules and it is the easiest mistake to make.

Measured: narration inside explicit scenes averages **11.8 words** against **10.9** outside. That is 1.08x — nothing. Across ~267,000 words there are exactly **four** narration sentences of 45+ words inside a sex scene, and only one is physical action.

**The 8–14 rule applies to sex exactly as everywhere else.** Momentum comes from short sentences stacking and from fragments. Never from comma-chaining.

What *does* change is chapter length: explicit-carrying chapters run 14–36% longer. Never pad a fast hook chapter to hit a number, and never cut a scene to hit one either.

---

## 4. The fragment engine

The real signature, and the most over-applied technique when a model has been told about it.

**The base unit is a full sentence followed by ONE short fragment.** Measured across 2,535 fragment runs:

| Shape | Share |
|---|---|
| sentence + **1** fragment | **69%** |
| sentence + 2 fragments | 19% |
| sentence + 3 fragments | 6% |
| longer | 6% |

**~14 runs per chapter**, across roughly 50 paragraphs. **86% cross a paragraph break** — each fragment is its own paragraph. The white space carries as much as the words.

> He has a key to a door he has no business opening.
>
> Nobody gave it to him.

**The parallel-echo triplet is a subset, not the rule.** *"Everything about him is black. Black mind. Black heart."* Hand-audited: only about a third of two-fragment runs genuinely echo the anchor, which is roughly **2 per chapter**. Expect whole chapters with none. A model will reach for it every paragraph — don't.

---

## 5. Chapter endings

| Metric | Measured | Our floor |
|---|---|---|
| Final paragraph ≤10 words | **52%** | at least 45% |
| Final paragraph ≤5 words | **27%** | at least 20% |
| Ends on spoken dialogue | 23% | keep under 30% |
| Ends on a question | **4%** | keep under 8% |

"End on a threat" and "end on a question" are **minority moves**, not the technique. The reliable rule is **brevity plus non-resolution**: never summarize what just happened, never land on a settled feeling.

Qualifying endings, none of them loud: *"Safe."* · *"Not at all."* · *"A shadow looms over my bed."* · *"I turn in the opposite direction and run."*

Commercial floor on top of this: every ending scores ≥7/10 on *would a reader swipe at 2 a.m.* Soft reflective endings stay under 25% of chapters. Chapter 1's ending is the most important in the book — it's the Look Inside cliff.

---

## 6. Numbers — precision is the wrong register

Per 10,000 words. Kent's actual rates, then our ceilings.

| Class | Kent | Huang | **Our ceiling** |
|---|---|---|---|
| Cardinal numbers | 19.6 | 32.4 | **under 30** |
| Number + measure (*six feet*, *two steps*) | 3.2 | 7.6 | **under 5** |
| Number + duration (*four years*) | 5.9 | 9.6 | **under 8** |
| Bare digits | 0.5 | 4.4 | **under 2** |
| Feet / inches / yards | — | — | **~5 in the whole book** |

For reference, a first drafted chapter on a previous project came in at **259 cardinals and 57 measure-phrases per 10,000 — 13x and 18x Kent.** That is a model signature, not a style.

**Kent's numbers are vagueness devices.** Across 480,000 words the measure slot is almost entirely vague time: *a second* (the dominant form by a distance), *a minute*, *a step*, *five minutes*, *ten minutes*. Genuinely precise physical measurement barely exists — about six precise distances in four books.

So the fix is not "fewer numbers." It's **swap precision for vagueness.**

- *a second* means briefly. *a step* means barely moved. *five minutes* means a little while.
- Precision is a cold register and this genre runs on sensation. *"Close enough to feel him breathe"* puts the reader in the body. *"Nine feet away"* puts them in a floor plan.
- A number invites verification, and checking is leaving the scene.
- First person present tense **cannot plausibly measure.** A woman mid-adrenaline does not know it is nine feet. She knows he is *there*.

**Numbers that belong:** ages (the age gap is the trope), money and debt, hard deadlines, injuries and body counts, and one or two obsessive repetitions where the counting *is* the characterization. Everything else: cut the number, keep the sensation.

Judge incidental numbers ruthlessly and let the load-bearing ones cost what they cost. Chapter-level spikes are expected — the chapter carrying a debt reveal runs hot. Ceilings are measured **across the whole book**, not per chapter.

### The deeper trap

Handing a narrator a "cognitive system" makes a model execute it as literal measurement — told *doors*, it builds a floor plan instead of a man. Worse, on a previous project both narrators started quantifying: hers social (*nineteen people told me*), his spatial (*nine feet*). Different units, **identical cognitive move**. That is the exact voice collapse the system rule exists to prevent.

**Varying the units is not varying the voice.** A cognitive system surfaces as *judgment*, not measurement:

> ❌ He's nine feet from the door and I'm four.
> ✅ He put himself between me and the only way out. He thinks I didn't notice.

**Related:** stop restating established durations. *Four years* ran twelve times in 3,400 words on a previous draft. Once the reader has the fact, trust it. That repetition is a model reinforcing its own context, not a character insisting.

---

## 7. Sex vocabulary — the ratio is the rule

Crude by default. Not a whitelist, a ratio.

*cock* appears **493** times across four books; *his length* appears **7**. That's **70:1** crude to euphemism. Soft words are legitimate at roughly **1–2% frequency** and never as a *substitute* for the crude one. *core* is fine — 27 genuine anatomical uses.

**Density varies enormously by book.** *Deviant King*: 9 *cock* in 94K. *Kiss the Villain*: 227 in 128K. **Aim at the Kiss the Villain / Hunt the Villain end** — roughly 17–18 per 10,000, so ~165 across a 95,000-word book.

*cunt* is not universal in her work: **0** in *Deviant King*, **0** in *Hunt the Villain*, **16** in *Kiss the Villain*, **37** in *God of Malice*. For this manuscript: live, deliberate, roughly 15–35 across the book.

**Clinical specificity alongside the crude vocabulary.** Shape, size comparison, curvature, texture (*veiny*, *smooth*), specific physical responses (*balls draw up tight*). The reader should be able to visualize exactly. **No phonetic moans** — measured across five bestsellers, nobody spells them out (CLAUDE.md §5c). Sound is carried by named verbs (*pant, sob, whimper, groan, gasp*) and by what the sound does to her throat.

**Profanity by POV (per 100k):** Selene 700–950 (fuck, shit, blasphemy — funny, modern). Lucian 550–800 (fuck, bastard — menacing). Cassian 0. Raised 2026-09-27 at LO's request so the book beats the comp average (704; Book 1 is now 713). *damn* ≤30 book-wide. Dialogue dirtier than narration. The rate stays flat between sex chapters and plot chapters. `audit.py --book` checks all of it.

Range soft to filthy and match the beat. When it's filthy, don't hold back. When it's tender, stay tender.

---

## 8. Diction floor

**Applies to POV narrators, not to everyone.** In Lucian's, Selene's, and Cassian's narration, a word that wouldn't survive in a bar needs justifying. Watch the formal adverbs: *entirely*, *considerably*, *genuinely*, *precisely*. Stacked intensifiers (*entirely flatly*, *entirely unrepentant*) are always drift — cut the adverb, keep the adjective.

**But formal diction is a characterization tool, not a defect.** Cassian is 690 and sounds it. That formality is most of why he's frightening, and sanding it off would cost the book its villain. Same for a word doing motif work across characters — if three people use the same word to describe what a life is worth, that's a theme, not a tic. Check whether a repeated word is doing work before cutting it.

Cut connective throat-clearing: *which is why*, *in a way that*, *the thing about X is*, *which meant*. State the thing.

Concrete over abstract. One image, then move on — no extended metaphor, and never explain the metaphor after making it.

---

## 9. Measuring a draft

Run from the project root against any drafted chapter.

```powershell
# Narration vs dialogue sentence length, paragraph shape, semicolons
$f = "books\book-1-king-of-teeth\drafts\ch01.md"
$t = Get-Content $f -Raw

# strip dialogue to measure narration alone
$narr = [regex]::Replace($t, '"[^"]*"', '')
$sent = [regex]::Split($narr, '(?<=[.!?])\s+') | Where-Object { $_.Trim().Length -gt 0 }
$wc = $sent | ForEach-Object { ($_ -split '\s+').Count }
"narration mean   : {0:N1}  (target 11, fail >14)" -f ($wc | Measure-Object -Average).Average
"narration median : {0}     (target 10)" -f ($wc | Sort-Object)[[int]($wc.Count/2)]
"pct <=14 words   : {0:N0}%  (target 71)" -f (100 * ($wc | Where-Object {$_ -le 14}).Count / $wc.Count)
"pct <=4 words    : {0:N0}%  (target ~21)" -f (100 * ($wc | Where-Object {$_ -le 4}).Count / $wc.Count)

$para = $t -split "(\r?\n){2,}" | Where-Object { $_.Trim().Length -gt 0 }
$ps = $para | ForEach-Object { ([regex]::Matches($_, '[.!?]("|\s|$)')).Count }
"pct 1-sentence paras: {0:N0}%  (target 48-54)" -f (100 * ($ps | Where-Object {$_ -eq 1}).Count / $ps.Count)
"semicolons          : {0}      (target 0)" -f ([regex]::Matches($t, ';')).Count
"question marks      : {0}      (target 8-12 per chapter)" -f ([regex]::Matches($narr, '\?')).Count
```

```powershell
# Number census — the model signature to watch
$words = ($t -split '\s+').Count
$card  = ([regex]::Matches($t, '(?i)\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|hundred|thousand)\b')).Count
$meas  = ([regex]::Matches($t, '(?i)\b\w+\s+(feet|foot|inches|inch|yards|yard|steps|step|seconds|second|minutes|minute)\b')).Count
$digit = ([regex]::Matches($t, '\b\d+\b')).Count
"per 10K - cardinals: {0:N1} (ceiling 30)" -f (10000 * $card / $words)
"per 10K - measures : {0:N1} (ceiling 5)"  -f (10000 * $meas / $words)
"per 10K - digits   : {0:N1} (ceiling 2)"  -f (10000 * $digit / $words)
```

Slop scanning lives in `BANNED_PHRASES.md`, which carries its own grep block.

---

## 10. Failure gallery

Each pair is the same beat, drafted wrong and then fixed. All three Book 1 narrators appear.

**Comma-chaining in a sex scene.**

> ❌ He pushes into me slowly, watching my face the whole time, and I can feel every inch of him as my body adjusts to the stretch, which is when he finally lets himself make a sound.
>
> ✅ He pushes in slow. Watching my face.
>
> I feel all of him. Every inch, and my body giving way around it.
>
> Then he makes a sound.

**Naming the feeling after showing it.**

> ❌ My hands are shaking against the table. I'm terrified of him.
>
> ✅ My hands are shaking against the table.

**Measurement instead of judgment.**

> ❌ Nine feet of hallway between us and he crosses it in half a second.
>
> ✅ He's across the hall before I finish the thought. Nobody taught him to wait in one.

**Emotional over-articulation.**

> ❌ I realize my grief has curdled into something closer to rage, and that I've been aiming it at the wolves because aiming it at myself would be unbearable.
>
> ✅ The wolves did this.
>
> I need that to stay true.

**The villain as professor.**

> ❌ "Your father's Code was a rhetorical instrument designed to render our species legible to a population that outnumbers us, and it has cost us four centuries of—"
>
> ✅ "Your father taught a room full of predators to apologize for their mouths."
>
> He asks about my hand. He always asks about my hand.

**Over-applied fragments.**

> ❌ He watches me. Quiet. Still. Deciding. The way a man decides.
>
> ✅ He watches me.
>
> Deciding.

**Abstract tricolon.**

> ❌ It was rage, and grief, and something like love.
>
> ✅ I want to put my hand through the window.

**Restating an established duration.**

> ❌ Four years. Four years I've had this ledger, and in four years I never opened it.
>
> ✅ I've had it since they died and I never opened it.

---

## 11. Pre-ship checklist

Per chapter, in order:

1. Narration mean 8–14, median ≤12, ~71% under 14 words.
2. Dialogue mean under 8. If a spoken line reads like a written sentence, clip it.
3. 45%+ single-sentence paragraphs; 88%+ at 1–3 sentences.
4. ~14 fragment runs, ~69% of them sentence-plus-one. At most ~2 parallel echoes.
5. Final paragraph ≤10 words, non-resolving. Cliffhanger ≥7/10.
6. 8–12 narration question marks.
7. Zero semicolons.
8. Number census under every ceiling. No spatial or social counting in either lead's head.
9. Zero banned phrases (`BANNED_PHRASES.md`).
10. Swap test fails on two random paragraphs (`series/VOICE_BIBLE.md`).
11. American English, including the double-L class.
12. Present tense throughout — no drift into past.
