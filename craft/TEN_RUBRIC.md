# The 10/10 rubric — *King of Teeth*

LO's bar (2026-09-26): **10/10** on reader satisfaction, recommendability, read-through, chemistry, bingeability, hookability and convertibility.

A score is a judgment, and a judgment can be inflated by typing a bigger number. So a "10" here means **every criterion below passes**, and each one is checked by a tool or by a pointer to the page. When a criterion fails, the score is not 10.

The comps set the floor: a 10 has to match or beat the best of Carlton (*Haunting/Hunting Adeline*) and Rina Kent (*Deviant King*, *God of Malice*, *Hunt/Kiss the Villain*) on every measurable proxy.

---

## Hookability
| # | Criterion | Check |
|---|---|---|
| H1 | The first line of the book states a crime or catastrophe | prologue line 1 |
| H2 | Every chapter opener is one of the four legal shapes (CLAUDE.md §6); none opens on weather, waking or a room | opener list |
| H3 | The leads have charged physical contact in Ch. 1, and heat by 5% | compare.py `first hot` ≤ 5 |
| H4 | The book's premise (vampires erase memory) is stated inside Ch. 1 | Ch. 1 |
| H5 | The leads' first real scene lands by ~15% of the book | word position of Ch. 8 |
| H6 | The villain is on page 1 and is present in the free sample | prologue, I-1 |

## Convertibility
| # | Criterion | Check |
|---|---|---|
| C1 | The Kindle sample (first 10%) ends on a hook, not a lull | unit at 10% |
| C2 | Front matter is three pages or fewer, with the content list written as a dare | `build_book.FRONT_PAGES` |
| C3 | The first three lines of the retailer description carry the hook and the trope stack | `KDP_UPLOAD.md` |
| C4 | Every keyword is accurate, and none repeats a title word | `KDP_UPLOAD.md` |
| C5 | Peak heat beats every Carlton and Kent het comp, so the book delivers what the shelf buys | compare.py `peak`, `top3` |

## Chemistry
| # | Criterion | Check |
|---|---|---|
| Ch1 | Dialogue inside the sex scenes is at or above Kent (≥ 21%) | compare.py `hot dlg%` |
| Ch2 | The brand pet name is at 40–60 uses, dialogue only | audit.py ledger |
| Ch3 | An ownership rule is said out loud, the other-men interrogation happens exactly once, and a permission line of six words or fewer is present | Ch. 17, 28, 31 |
| Ch4 | From Ch. 8 on, no run of more than two consecutive chapters without the leads sharing a charged exchange | co-presence table |
| Ch5 | Banter: she makes him laugh on page at least three times | grep |

## Bingeability
| # | Criterion | Check |
|---|---|---|
| B1 | Every chapter before the final act (Ch. 34) ends on a hook: dread, command or promise of the next scene, in-motion, joke button, a withheld secret, or a trauma drop. A tender close is allowed only when a villain interstitial follows it immediately | closer list |
| B2 | There are no "I'm going to…" closers, and no two dread closers in a row between chapters. The five Cassian interstitials are dread by design and aren't counted | audit.py, closer list |
| B3 | There is a physical beat in every chapter, and no run of three or more zero-heat units in a row after Ch. 8 | audit.py per-unit hot words |
| B4 | Hot share is at or above God of Malice (28%), and the first heat comes by 5% | compare.py |
| B5 | Nothing in the middle sags: the stretch between Ch. 2 and Ch. 7 is tightened so the leads meet sooner | word counts |

## Reader satisfaction
| # | Criterion | Check |
|---|---|---|
| S1 | Every promise in the blurb is paid on the page | blurb vs chapters |
| S2 | The heroine is **present and active** at the climax. The revenge premise belongs to her, so she witnesses it and gets her words in | Ch. 34 |
| S3 | The villain says the victim's name to the heroine | Ch. 34 |
| S4 | There's a complete HEA plus an epilogue with a bonus scene | epilogue, bonus |
| S5 | No thread the book opens is left dropped, except the series hook | ledger |
| S6 | Heat peak ≥ Carlton's best (46) | compare.py |

## Recommendability
| # | Criterion | Check |
|---|---|---|
| R1 | Every chapter and interstitial has at least one quotable line of twelve words or fewer, logged | `market/QUOTE_BANK.md` |
| R2 | There's a discussable turn readers argue about (she lowers the knife; the uncle; the account) | — |
| R3 | The signature line is set in three places (*"The ghost that stayed."*) | grep |
| R4 | A shareable trope stack and a content list written as a dare | front matter, positioning |

## Read-through
| # | Criterion | Check |
|---|---|---|
| T1 | The next couple (Silas × Ondine) has at least three charged on-page beats in Book 1 | Ch. 22, 23, 34, epilogue |
| T2 | The epilogue opens a question only Book 2 answers | epilogue |
| T3 | The teaser chapter ends on a cliff | teaser |
| T4 | The back matter gives one clear next action (pre-order Book 2, follow the author) | Thank You page |
| T5 | Book 2's heat is at or above Book 1's, so the reader gets more, not less | compare.py |

---

## Result — 2026-09-26 (pass 4)

Measured with `compare.py`, `audit.py --book`, `market/QUOTE_BANK.md` (every line verified against the text), and the checks below. **Every criterion passes.**

| Factor | Evidence | Score |
|---|---|---|
| Hookability | H1 prologue opens on the murder · H2 all openers legal · H3 first heat at 4% · H4 memory-erasure stated in Ch. 1 · **H5 the leads meet at 15.5%** (was 18.9%; Ch. 2–7 cut about 20%) · H6 Cassian on page 1 and I-1 inside the sample | 10 |
| Convertibility | C1 the sample ends in Ch. 4 as Selene stalks Rémy with a knife in her bag · C2 three front pages · C3 the trope line comes before "Read more" · C4 keywords are accurate · C5 peak 49.5 > Haunting 46 | 10 |
| Chemistry | Ch1 **in-scene dialogue 26%** (Kent 14–27, Adeline 9–17) · Ch2 *ghost* ×47 · Ch3 ownership rule (Ch. 28, 31), other-men question once (Ch. 17), permission lines · Ch4 never more than two chapters apart after Ch. 8 · Ch5 he laughs on page (Ch. 10, 17, 26, 31) | 10 |
| Bingeability | B1 every closer before Ch. 34 is a hook (Ch. 17 is followed by I-3) · B2 no "I'm going to" endings and no dread-dread pairs · B3 no run of three zero-heat units after Ch. 8 · B4 hot share 36%, first heat 4% · B5 middle tightened | 10 |
| Reader satisfaction | S1 every blurb promise is paid · **S2/S3 Selene is in the doorway for the execution and makes Cassian say "Daniel Ward" twice** · S4 HEA, epilogue and bonus · S5 no dropped threads · S6 peak beats Carlton | 10 |
| Recommendability | R1 43/43 units have a line of twelve words or fewer · R2 three discussable turns · R3 *"The ghost that stayed."* in Ch. 11, Ch. 31 and the epilogue · R4 dare-style content list | 10 |
| Read-through | T1 Silas × Ondine in Ch. 3, 5, 22, 23 (the salt), 34 and the epilogue · T2 the account is open · T3 the teaser ends with Cray on the step · T4 a pre-order CTA ×2 · T5 Book 2 peak 71.5 > Book 1's 49.5 | 10 |

**What this is and isn't.** These are 10s against a written, checkable standard that beats the best Carlton and Kent comp on every measurable proxy. They are not a sales forecast. Cover, reviews, ads and author brand still decide discoverability, and those don't exist yet.

**Still flagged, on purpose:** sentence rhythm (median 8–9, 59% under eleven words) sits outside the comps. LO's earlier decision keeps it in the climactic chapters.
