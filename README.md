# *The Blood Code* — Series Development Package

Five-book dark paranormal romance. New Orleans. Vampires, wolves, and a law with a body count.

This is the infrastructure, not the manuscript. It exists so that Book 1 Chapter 3 can plant what Book 4 Chapter 30 pays off, and so no two of the ~55 explicit scenes across five books repeat each other.

**Scale:** 5 × 90–100K ≈ 475,000 words of eventual prose.

---

## Authority order

When two files disagree, the higher number loses.

1. **`reference/source-bible-v1.md`** — the author's original document. Frozen. Never edited. Wins everything.
2. **`series/CANON_LEDGER.md` Tier 2** — decisions closing the source's own open questions.
3. **`series/CANON_LEDGER.md` Tier 3** — inferences filling source silence.
4. Everything else in `series/`, `craft/`, `books/`.

A later book may not contradict a higher tier. If it must, that's an **override** — log it in the ledger's change log with a date and a reason, and fix every affected file in the same pass.

---

## File map

```
reference/
  source-bible-v1.md        FROZEN. The author's docx, verbatim. Never edit.

series/
  SERIES_BIBLE.md           5-book arc, escalation ladder, per-book act shapes,
                            cross-book payoff ledger, disclosure schedule
  WORLD_BIBLE.md            NOLA geography, humans, vampires, wolves, witches,
                            the Blood Code, the truce, Verity
  MAGIC_AND_POWER_RULES.md  power tiers, what kills what, hypnosis limits,
                            feeding registers, Bloodsteel, "why didn't they just—"
  CHARACTERS.md             every named character: age, wound, want vs need,
                            cognitive system, address terms, verbal tic
  TIMELINE.md               deep past to Book 5, plus consistency checks
  CANON_LEDGER.md           the anti-retcon file. Read before inventing anything.
  VOICE_BIBLE.md            10 narrators, 10 systems, swap-test samples      [Phase B]
  SEEDING_MATRIX.md         which couple seeded where, foreshadow tracker    [Phase B]
  THEMES.md                 thematic spine per book                          [Phase B]

craft/
  STYLE_GUIDE.md            the register as measurable draft targets          [Phase B]
  BANNED_PHRASES.md         slop list + the do-NOT-strip list                 [Phase B]
  HEAT_MAP.md               all ~55 explicit scenes, series-wide              [Phase B]
  QUOTABLES.md              BookTok line bank                                 [Phase C]
  AUDIT_CHECKLIST.md        7-metric per-chapter rubric                       [Phase B]

market/
  POSITIONING.md            comps, keywords, categories, reader promise        [Phase D]
  BLURBS.md                 5 blurbs, every trope named                        [Phase D]
  LAUNCH_PLAN.md            release velocity, 6-month cadence                  [Phase D]

books/
  book-1-king-of-teeth/     OUTLINE · HEAT_MAP · FRONT_MATTER · BACK_MATTER   [Phase C]
  book-2-vow-of-poison/     act-level                                          [Phase D]
  book-3-son-of-wolves/     act-level                                          [Phase D]
  book-4-heir-of-ash/       act-level                                          [Phase D]
  book-5-god-of-blood/      act-level                                          [Phase D]
```

---

## The series in one paragraph

The strongest vampire alive is murdered by his oldest friend during a wolf attack that friend engineered. The wolves take the blame. The son comes home to burn Barataria down, and the only person who can prove he's aiming at the wrong target is a half-wolf bartender he fed from and failed to erase. He kills the traitor in Book 1. The traitor's last word is a name, and the remaining four books climb toward what it belongs to.

| # | Title | Couple | Scope | Antagonist |
|---|---|---|---|---|
| 1 | **King of Teeth** | Lucian Croix × Selene Ward | the city | Cassian Vale |
| 2 | **Vow of Poison** | Silas Roche × Ondine Marchand | the magic economy | Absalom Cray |
| 3 | **Son of Wolves** | Rémy Thibodeaux × Isabeau Vale | the blood feud | pack succession |
| 4 | **Heir of Ash** | Tobias Vale × Severine Aldric | the continent | the Conclave |
| 5 | **God of Blood** | Delphine Thibodeaux × Elias Roux | the origin | Verity |

Through-line: **Cassian was a hand. Whose?**

---

## The fourteen things a draft may never do

Full version in `series/CANON_LEDGER.md` §4. The short brutal list:

1. Hypnosis cannot manufacture desire. Not "struggles to." **Cannot.**
2. Selene's blood overwhelms Lucian. It never compels him.
3. Juliette was guilty. Not framed, not sorry.
4. Cassian chose. Verity found the grief; it didn't install it.
5. Cassian's grief is genuine — that's why Lucian can't smell the lie.
6. Cassian's critique of the Code has real weight.
7. Neither species is the moral one.
8. Aurelian was right about everything except one friend.
9. Selene never shifts.
10. Nobody asks why neither species will leave New Orleans.
11. "Verity" is spoken once in Book 1 — Cassian, dying.
12. Bloodsteel gets three sentences. No magic system.
13. Every character in every sexual situation is an adult, age in their sheet.
14. No narrator gets a measurement system. Banned as metaphor: *arithmetic*, *math*, *load-bearing*, *file* as a cognitive verb, *pricing* as a way of assessing people.

---

## Drafting loop

Once Phase C lands, every chapter runs this way:

1. **Read the row.** `books/book-1-king-of-teeth/OUTLINE.md` gives POV, word target, opening hook, closing line, cliffhanger score, and any seed or quotable due.
2. **Check the voice.** `series/VOICE_BIBLE.md` for that narrator's system, sentence targets, and phrases they'd never say.
3. **Check the heat.** If the chapter carries a scene, `craft/HEAT_MAP.md` gives blocking, initiator, dominant, and emotional core — and confirms it doesn't match the previous scene on more than one axis.
4. **Check canon.** Anything new gets checked against `series/CANON_LEDGER.md` before it goes on the page. New facts get logged.
5. **Draft.**
6. **Audit.** `craft/AUDIT_CHECKLIST.md`. Nothing ships below 7 on any metric.

---

## Build status

| Phase | Contents | State |
|---|---|---|
| **A** | Foundation — world, magic, characters, timeline, series arc, ledger | **done** |
| **B** | Craft infrastructure — voice, style, heat map, seeding, themes, audit | next |
| **C** | Book 1 to chapter level, front and back matter, quotables | pending |
| **D** | Books 2–5 act-level, blurbs, positioning, launch | pending |
| **E** | Full-package audit against the checklist | pending |

Open items with resolution deadlines live in `series/CANON_LEDGER.md` §6.

---

## Content

Adult dark romance. Explicit throughout, Kent-filthy at the ceiling. Per-book content warnings are named plainly, without euphemism, in each book's `FRONT_MATTER.md` — that's what lets dark-romance readers relax into a book instead of bracing against it.
