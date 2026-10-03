# King of Teeth ? layout revision, 2026-09-27

Updated `King_of_Teeth.pdf`, `King_of_Teeth.epub`, and the companion `King_of_Teeth_ARC.epub`. The repeatable source is `build_book.py`.

## Improvements

- Explicit EPUB section boundaries with modern and legacy page-break rules, one semantic chapter heading per story section, and heading/scene ornaments kept with following text.
- Fine-lined crown ornaments on the title page and main chapter openings; coordinated screen and print styling.
- Responsive chapter spacing, raised EPUB initials that cannot collide with following paragraphs, dark-mode colors, and a clearer linked contents page.
- PDF navigation with 50 bookmarks; front-matter Roman page labels and story numbering beginning at 1 on the prologue.
- Preserved print trim, mirrored margins, embedded serif fonts, and the 408-page extent required by the existing cover.

## Verification

- Both EPUB editions: EPUBCheck 5.1.0, zero errors or warnings.
- All 45 story sections: separate PDF opening pages and separate EPUB spine documents with explicit section breaks.
- PDF: all 408 pages have 6 ? 9 inch geometry; nine fonts embedded; no replacement characters or text outside a 0.3-inch trim safety boundary.
- PDF body text matches the original across the complete book after normalizing line-wrap hyphens, whitespace, and presentation case, excluding running heads and folios. Pagination changed after adding internal POV breaks. EPUB body text matches the original, ignoring presentation-only case and whitespace.
- All EPUB internal links and fragment targets resolve.
- PDF's three intentional blank front-matter pages remain pages 2, 6, and 8.
- Visually reviewed all section opener thumbnails and representative full-size PDF pages, including a Poppler rendering.
- 32 local EPUB layouts checked across phone, tablet, enlarged-text, and dark-mode settings: no horizontal overflow. Seven representative sections tested together in paged rendering: each starts a fresh page.
- Local browser rendering is a compatibility sample, not a Kindle Previewer or physical-device certification. Continuous-scrolling reader modes naturally show sections in a scroll instead of fixed pages.

## Originals

Original files and original builder are preserved in `backup-before-layout-2026-09-27/`. Manuscript files were not edited.

## POV break correction following reader screenshot

The screenshot exposed an internal POV transition, not a numbered chapter boundary. Fixed all ten internal transitions (one in the prologue and nine in the epilogue). Each now starts a new PDF page and a separate EPUB spine document. The first POV stays with its chapter heading. All text is preserved. Both EPUBs were rechecked with EPUBCheck: zero errors and warnings. Reviewed the corrected Lucian opener in both formats. PDF body type is 11.10 pt with unchanged 15.65 pt leading, preserving 408 pages and the existing cover. Updated page locations are in `layout-page-map.json`. The pre-correction editions are preserved in `backup-before-pov-breaks-2026-09-27/`.
