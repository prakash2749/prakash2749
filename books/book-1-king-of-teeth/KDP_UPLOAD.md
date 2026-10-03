# KDP Upload Sheet — *King of Teeth*

Everything to paste into kdp.amazon.com, field by field, in the order KDP asks for it. Written 2026-09-25.

## Files

| Upload slot | File | Spec |
|---|---|---|
| Kindle eBook: manuscript | `King_of_Teeth.epub` | EPUB3, reflowable, nav/TOC, all XHTML parses clean. No cover inside; KDP takes it separately. |
| ARC / BookFunnel copy (not for KDP) | `King_of_Teeth_ARC.epub` | Same book with the cover embedded. Passes EPUBCheck 5.4 with 0 errors and 0 warnings, like the KDP file. |
| Kindle eBook: cover | `cover/King_of_Teeth_ebook_cover.jpg` (designer; see the resolution note below) | 1600 × 2560 px (1.6:1), RGB JPG, under 50 MB. See the designer spec below. |
| Paperback: manuscript | `King_of_Teeth.pdf` | 6 × 9 in, no bleed, **408 pages**, all fonts embedded (Crimson Text + Cormorant Garamond, SIL OFL), mirrored margins: 0.85 in gutter, 0.62 in outside |
| Paperback: cover | `cover/King_of_Teeth_Paperback_408pp_Cream_6x9.pdf` | Designer's full wrap: 13.27 × 9.25 in, 1.02 in spine, CMYK, matches the 408 pp interior. |

**After any manuscript edit:** run `python build_book.py`, then check the PDF page count. If it changed, the spine width changes and the designer has to adjust the paperback cover.

### Cover spec for your designer (send them this)

- **Ebook:** 1600 × 2560 px, RGB, JPG. It has to read at thumbnail size: title large, author name legible.
- **Paperback full wrap:** trim 6 × 9 in, cream paper, **408 pages → spine 1.02 in**. Full size with 0.125 in bleed on all sides: **13.27 × 9.25 in**. Keep text 0.25 in inside the trim edges, and spine text 0.0625 in clear of each fold.
- **Barcode:** leave a 2 × 1.2 in area clear at the bottom right of the back cover. KDP prints the barcode there.
- **Text on the cover must match KDP exactly:** title *King of Teeth*, author *Aurelia Thorn*, and the subtitle *A Dark Vampire Romance* if you use that field. Leave the subtitle field blank if it isn't on the cover.
- **Back cover copy:** the short blurb in `market/BLURBS.md`.
- **Fonts and images:** ask the designer to confirm commercial licenses for both. If the designer uses AI image tools, you have to disclose that to KDP (see AI disclosure below).
- Ask for the print PDF *after* the interior is final, or confirm the page count with the designer, because the spine depends on it.

**Before you upload:**
1. Open the EPUB in **Kindle Previewer 3** (Amazon's free tool) and check the phone and Paperwhite views.
2. In the paperback flow, check that **Launch Previewer** comes back with no errors.

---

## 1. Kindle eBook: Details

| Field | Enter |
|---|---|
| Language | English |
| Book Title | `King of Teeth` |
| Subtitle | `A Dark Vampire Romance`, only if the designer prints it on the cover. Otherwise leave it blank. |
| Series | Create **The Blood Code**, Book **1** |
| Edition number | leave blank |
| Author | `Aurelia Thorn` (must match the cover exactly) |
| Contributors | none |
| Description | paste the HTML below |
| Publishing rights | *I own the copyright and I hold the necessary publishing rights* |
| Primary audience: sexually explicit images or title | **No**. The text is explicit; the title and images aren't. |
| Reading age | Minimum **18+** |

### Description (paste into the HTML-enabled box: ~1,800 characters, under the 4,000 limit)

```html
<h4><b>Every woman he feeds on forgets him. She's the one who stayed.</b></h4>
<p><i>Vampire king × half-wolf bartender. A blood pact, a murdered king, and a monster nobody has ever remembered, until her.</i></p>
<p>The King of New Orleans is dead, murdered in his own council chamber on the night the wolves came through the windows. His son, Lucian Croix, has come home to take the city back, and he won't take the crown until he has a killer.</p>
<p>Selene Ward pours drinks on Frenchmen Street. She's half wolf, she can't shift, and she has spent four years planning to kill the Alpha's son who murdered her parents. She has everything she needs except a way across the water.</p>
<p><b>Then a vampire drinks from her in a back hallway, tries to take the memory away, and fails.</b></p>
<p>Nobody has ever remembered Lucian Croix. Nobody has ever stood in front of him with blood on her throat and asked if he's a vampire. Now there's a half-wolf bartender he can't erase, a pact written in her blood, and a traitor inside his own house who asks after everyone's mother.</p>
<p><i>He calls her ghost.</i><br><i>She calls him Your Majesty when she wants to cut him.</i></p>
<p>One of them is going to have to stop lying first.</p>
<p><b>Inside:</b></p>
<ul>
<li>A vampire king who feeds on his city and doesn't apologize</li>
<li>The only woman in four hundred years he can't make forget</li>
<li>Revenge, a blood pact, and a murderer hiding in plain sight</li>
<li>Touch her and die</li>
<li>Dual POV, plus chapters from the villain</li>
<li>Complete HEA, no cliffhanger</li>
<li>Bonus scene: the night of the pact, from her side of the bed</li>
</ul>
<p><i>King of Teeth is Book One of The Blood Code, a dark paranormal romance series. Each book follows a new couple. For readers 18+: explicit sexual content, blood play, breath play, graphic violence, and dark themes. Full content list inside the book.</i></p>
```

### Keywords (7 boxes, 50 characters max each)

Every keyword has to describe what's actually in the book (misleading keywords are a KDP violation). KDP also forbids other authors' names, other book titles, and "bestseller" or "free". Don't repeat words that are already in the title, subtitle or series name. Amazon indexes them anyway, so repeats waste slots.

1. `vampire king romance forced proximity blood bond`
2. `revenge romance morally gray hero possessive`
3. `new orleans paranormal romance southern gothic`
4. `age gap immortal romance villain pov murder`
5. `shifter werewolf half wolf heroine bartender`
6. `touch her and die obsessed alpha hero spicy`
7. `blood pact forbidden love adult fantasy romance`

Stay away from *dubcon*, *non-con*, *taboo* and *erotica* in the metadata. Amazon can quietly filter the book out of general search for those words. The content list inside the book is the right place for them, and it's already there.

### Categories (pick 3 in the category browser)

The names below are KDP's current ones. Search them in the picker, because Amazon renames them from time to time.

1. **Fiction › Romance › Paranormal › Vampires**: the primary shelf, and where you'll get a category-bestseller flag.
2. **Fiction › Romance › Paranormal › Shapeshifters**: Selene is half wolf. It's a smaller category, so the ranking is easier.
3. **Fiction › Romance › Romantic Suspense**, or **Fiction › Romance › Fantasy**: the murder plot earns Suspense.

**Don't** pick an Erotica category. It moves the book into the adult-filtered store and it disappears from normal search.

### AI disclosure (required, and answer it honestly)

KDP asks whether the book contains AI-generated content.
- **Text: Yes.** The manuscript was drafted with an AI assistant. Choose the option that matches how much of it you rewrote yourself ("Some sections, with extensive edits" versus "Entire work, with minimal or no editing").
- **Images:** depends on your cover. **No** if the designer made it without AI image tools. **Yes** if any AI-generated imagery is in it. Ask the designer in writing.
- **Translations:** No.

Readers never see this answer; it's for Amazon only. Getting it wrong can put the account at risk.

**Copyright note:** under current US Copyright Office guidance, AI-generated text on its own isn't copyrightable. Only your human authorship is protected: your edits, selection and arrangement. The copyright page stays; just be aware of how far it reaches.

### Pre-order

Optional. A 2–4 week pre-order gives ARC reviews time to land on release day. KDP needs the final file 72 hours before release.

---

## 2. Kindle eBook: Content

| Field | Enter |
|---|---|
| DRM | **No**. It does nothing against piracy, it irritates readers, and it can't be changed after publishing. |
| Manuscript | `King_of_Teeth.epub` |
| Cover | *Upload a cover you already have*, then the designer's JPG |
| AI | see above |
| ISBN | leave blank (ebooks don't need one) |

## 3. Kindle eBook: Rights and pricing

| Field | Recommendation |
|---|---|
| **KDP Select** | **Enroll.** Dark romance is one of Kindle Unlimited's strongest genres, and a debut earns more from KU page reads than from sales. It means 90 days of ebook exclusivity. The paperback isn't affected. |
| Territories | All territories (worldwide rights) |
| Primary marketplace | Amazon.com |
| Royalty | **70%** |
| **List price** | **$4.99 USD.** Let KDP convert the other stores, then round: £3.99, €4.99, CA$6.99, AU$7.99. |
| Launch pricing | **Publish at $0.99 for launch week** (35% royalty), then raise the list price to $4.99 by hand. Cheap ranking, and the also-boughts fill up faster. Don't plan a Kindle Countdown Deal for launch: it needs 30 days in KDP Select *and* 30 days at an unchanged price first, so it's a month-two tool. Full calendar in `market/LAUNCH_PLAN.md`. |
| Book Lending | On |

Royalty at $4.99: about **$3.41** per sale. The file is ~0.8 MB, so the delivery fee is about $0.12.

KU pays roughly $0.004 per page read, and KENP for ~115k words (book, bonus scene and teaser) comes to ~500 pages, so one full read is worth about **$2.00**. These are estimates; KDP shows the exact KENP after publishing.

---

## 4. Paperback: Details

Use the same Title, Subtitle, Series, Author and Description as the ebook. Link the two formats so reviews are shared (KDP usually does this by itself).

| Field | Enter |
|---|---|
| Keywords and categories | same as the ebook |
| **Adult content** ("inappropriate for under 18") | **Yes**. The honest answer, and standard for explicit dark romance. |
| Reading age | 18+ |

## 5. Paperback: Content

| Field | Enter |
|---|---|
| ISBN | **Get a free KDP ISBN.** The imprint shows as "Independently published". Buy your own from Bowker only if you want your own imprint name or plan to publish wide in print. |
| Publication date | leave blank |
| Ink and paper | **Black and white interior, cream paper** (standard for fiction; the spine spec assumes cream) |
| Trim size | **6 × 9 in** |
| Bleed | **No bleed** |
| Cover finish | **Matte** (dark covers look premium in matte; glossy shows fingerprints and glare) |
| Manuscript | `King_of_Teeth.pdf` |
| Cover | *Upload a print-ready PDF cover*, then the designer's full-wrap PDF |
| AI | same answers as the ebook |

If KDP reports a page count other than 408, it will reject the cover on spine width, so send the designer the new count (spine = pages × 0.0025 in on cream).

## 6. Paperback: Pricing

KDP print cost (US, black ink, 6×9, 408 pages): $1.00 + 408 × $0.012 = **about $5.90**. Check it in the pricing box, because KDP updates its rates.

| List price | Amazon royalty (60%) | Expanded distribution (40%) |
|---|---|---|
| $16.99 | $4.29 | $0.90 |
| **$17.99 (recommended)** | **$4.89** | **$1.30** |
| $18.99 | $5.49 | $1.70 |

- **Expanded Distribution: On.** Bookstores and libraries can order the book; the margin is thin, but you get the reach.
- **Hardcover (optional, later):** a case laminate at $27.99 for collectors. Special editions sell in this genre. It needs its own cover from the designer.

---

## 7. After it's live (the commercial part)

1. **Author Central** (author.amazon.com): claim the book, add a bio, link the series.
2. **Series page:** confirm *The Blood Code* groups Book 1. Add *Vow of Poison* as Book 2 once it's on pre-order, since the teaser at the back of the book is doing that sales work.
3. **A+ Content** (free, under Marketing): three modules.
   - A comparison or banner with the tagline.
   - Three screenshot lines from `market/POSITIONING.md`: nos. 1, 3 and 7 carry no spoilers.
   - A trope-icon strip: vampire king · revenge · touch her and die · HEA.
4. **ARCs:** 30–60 early readers through BookSirens, BookFunnel or StoryOrigin, 3–4 weeks before launch. Reviews in the first 72 hours drive the algorithm.
5. **Short-form video:** use the launch hooks and screenshot lines in `market/POSITIONING.md`. Never post the killer's name or *Verity*.
6. **Amazon Ads:** start with auto-targeting at $5–10 a day for two weeks. Then build manual keyword campaigns from the search terms that convert.
7. **Look Inside:** the first ~10% is free. The content list and the ch. 1 bar scene both fall inside it, and those are the sales hooks.

---

## Notes before you hit Publish

**A. Pen name: Aurelia Thorn.** It's set in the build (title page, copyright, EPUB metadata). Before you publish, search Amazon and Goodreads for the exact name to be sure there's no existing author using it. Claim it on Author Central the day the book goes live.

**B. Cover.** It's coming from you or a freelancer. The spec above has everything they need.

**C. *Verity* is resolved.** It's spoken once, by Cassian as he dies (Ch. 34), as the canon rule requires. The epilogue's final page now points at the poison money and hands the account to Silas, which is Book 2's thread. Never use *Verity* in marketing.

**D. Fonts.** The interior embeds Crimson Text, Cormorant Garamond, and the renamed KoT Small Caps derivatives. Font licenses are in `fonts/`.

**E. Validation.** I checked the files myself:
- **EPUB:** mimetype stored first, metadata present, nav present, every XHTML parses.
- **PDF:** exact 6 × 9 dimensions, and every font in the interior is embedded.

Layout revision verified on 2026-09-27: both EPUB editions pass EPUBCheck 5.1.0 with no errors or warnings. The PDF remains 408 pages at 6 ? 9 inches, with embedded fonts, 50 bookmarks, and 45 story sections beginning on fresh pages. EPUB layouts were checked in local browser rendering at phone/tablet sizes, with enlarged text and dark mode. Kindle Previewer and the KDP upload preview remain separate platform-specific checks.
