# KDP Upload Sheet — *Vow of Poison*

Everything to paste into kdp.amazon.com, field by field, in the order KDP asks for it. Mirrors Book 1's sheet (`books/book-1-king-of-teeth/KDP_UPLOAD.md`), which has the fuller explanations. Written 2026-09-26.

## Files

| Upload slot | File | Spec |
|---|---|---|
| Kindle eBook: manuscript | `Vow_of_Poison.epub` | EPUB3, reflowable, nav/TOC (46 entries: front matter, 34 chapters, 5 Cray interstitials, epilogue, Thank You, bonus scene *Drink*, *Son of Wolves* sneak peek) |
| Kindle eBook: cover | from your designer | 1600 × 2560 px, RGB JPG |
| Paperback: manuscript | `Vow_of_Poison.pdf` | 6 × 9 in, no bleed, **344 pages**, all fonts embedded |
| Paperback: cover | from your designer | Full-wrap print PDF (spec below) |

**After any manuscript edit:** run `python build_book.py` in this folder and check the page count. The spine changes if the page count does.

### Cover spec for your designer

- **Series look:** match *King of Teeth*'s type and layout so the two read as a set in the also-boughts. Same title font, same author-name placement, a different color key. Suggested key: poison green and bone white against black (Book 1 is blood red).
- **Imagery that fits the book:** a jar, salt, a red thread, a scarred hand, the new moon. Avoid a bare-chested model; the series brand is object-led.
- **Ebook:** 1600 × 2560 px, RGB, JPG, readable at thumbnail size.
- **Paperback full wrap:** trim 6 × 9 in, cream paper, **344 pages → spine 0.860 in**. Full size with 0.125 in bleed: **13.110 × 9.25 in**. Text 0.25 in inside the trim, spine text 0.0625 in clear of each fold. Leave 2 × 1.2 in clear at the bottom right of the back cover for the barcode.
- **Text on the cover must match KDP exactly:** *Vow of Poison*, *Aurelia Thorn*, and optionally *The Blood Code, Book Two*.
- **Licenses and AI:** ask the designer to confirm commercial licenses for fonts and images, and in writing whether any AI image tools were used.

---

## 1. Kindle eBook: Details

| Field | Enter |
|---|---|
| Language | English |
| Book Title | `Vow of Poison` |
| Subtitle | `A Dark Vampire Romance`, only if it's printed on the cover |
| Series | **The Blood Code**, Book **2** |
| Author | `Aurelia Thorn` |
| Description | HTML below |
| Primary audience: sexually explicit images or title | **No** |
| Reading age | **18+** |

### Description (HTML box, about 1,900 characters)

```html
<h4><b>He would give his name for her. She'd never let him.</b></h4>
<p>For a year, the King's enforcer has walked past the witch's gate every night and never once gone in.</p>
<p>Silas Roche reads ground for a living: who passed, how fast, what they were carrying. He can't read himself, and he can't finish a sentence about who he is. He's carried a writ of protection in his coat for three months without saying a word. Tonight he finally knocks.</p>
<p>Ondine Marchand brewed the poison that nearly killed his king. Her house is neutral ground between the vampires and the wolves, and her shelves hold half the city's debts. And a polite man in thin-soled shoes has just left an envelope under her mat.</p>
<p><b>Her grandmother signed a debt before Ondine was born. The collateral is Ondine's own name. It falls due at the new moon.</b></p>
<p>The broker will take a substitute: any name of equal weight, freely given. And he's looking at Silas when he says it.</p>
<p>Killing the broker only hands the paper to whatever he answers to. The only way out costs a name. And the witch has already decided whose.</p>
<p><i>Touch her again. Please.</i></p>
<p><b>Inside:</b></p>
<ul>
<li>A silent, scarred, possessive vampire who has wanted her for a year</li>
<li>A witch who saves herself, and pays for it</li>
<li>Touch her and die</li>
<li>A debt that can't be broken by violence, a new-moon deadline, and a villain who is always, always polite</li>
<li>Forced proximity: he moves into her guest room, the one with the lock on the inside</li>
<li>Blood drinking, a "knock twice" brake, and very explicit heat</li>
<li>Dual POV, plus chapters from the broker</li>
<li>Complete HEA, no cliffhanger (and a grave in the woods for Book 3)</li>
<li>Bonus scene: the first feeding, from his side</li>
</ul>
<p><i>Vow of Poison is Book Two of The Blood Code. It can be read as a standalone, and it's best after King of Teeth. For readers 18+: explicit sexual content, blood play, restraint, graphic violence, and dark themes. Full content list inside.</i></p>
```

### Keywords (7 boxes, 50 characters each). Every one is true of the book.

1. `witch romance vampire hero possessive protector`
2. `touch her and die obsessed hero he falls first`
3. `forced proximity forbidden love paranormal spicy`
4. `new orleans southern gothic dark fantasy romance`
5. `morally gray hero scarred tortured past redemption`
6. `debt collateral bargain deadline romantic suspense`
7. `dual pov explicit romance adult blood drinking`

### Categories (pick 3 in the category browser)

1. **Fiction › Romance › Paranormal › Vampires** (primary)
2. **Fiction › Romance › Paranormal › Witches & Wizards** (smaller shelf, easier ranking)
3. **Fiction › Fantasy › Paranormal & Urban**

Don't pick an Erotica category (see Book 1's sheet for why).

### AI disclosure (required, and answer it honestly)

- **Text: Yes.** The manuscript was drafted with an AI assistant. Choose the option that matches how much of it you rewrote yourself.
- **Images:** ask the designer, in writing.
- **Translations:** No.

The same copyright note as Book 1 applies: only your human authorship is protected.

---

## 2. Pricing and launch

| Item | Plan |
|---|---|
| List price | **$4.99 USD** (70% royalty band) |
| Pre-order | **Yes.** Open the pre-order the day *King of Teeth* launches, so Book 1's back-matter teaser can link straight to it. |
| Launch week | Keep Book 2 at $4.99 and drop **Book 1 to $0.99** for Book 2's launch week. Read-through is the engine: cheap Book 1 in, full-price Book 2 out. |
| KDP Select | Same choice as Book 1, so both are in Kindle Unlimited or neither is. |

## 3. After publishing

1. **Series page:** confirm both books appear on The Blood Code series page in order.
2. **A+ Content,** three modules: (1) the series banner with both covers; (2) the tagline plus three screenshot lines — *"Touch her again. Please."* · *"Knock twice if I'm wrong."* · *"I was a dog. Never yours."*; (3) "Start with Book One" with the *King of Teeth* cover.
3. **Book 1 back matter:** update the *King of Teeth* EPUB so its teaser page links to the Book 2 pre-order, then re-upload. The teaser text was already re-synced to this Chapter One on 2026-09-26.
