"""
Build the EPUB and print PDF for King of Teeth (typesetting v3, 2026-09-27).

PDF  : 6 x 9 in KDP paperback, black ink. Mirrored margins, running heads,
       true small caps, three-line drop caps, hyphenation, widow/orphan control,
       crown ornaments, section bookmarks and logical page labels.
EPUB : reflowable EPUB 3 with subset-embedded fonts, PNG ornaments, explicit
       section breaks, accessible chapter headings and dark-mode styles.
       Two files: King_of_Teeth.epub (KDP, no cover inside) and
       King_of_Teeth_ARC.epub (cover embedded, for ARC readers / BookFunnel).

Fonts (SIL Open Font License, embedding permitted, licenses in fonts/):
  Crimson Text        body
  Cormorant Garamond  display, drop caps, chapter numbers
  KoT Small Caps      Cormorant Garamond with its smcp glyphs mapped onto
                      lowercase (built by fontTools; ReportLab cannot switch
                      OpenType features). Renamed per the OFL.

Uses: ebooklib (EPUB), reportlab + pyphen (PDF), fontTools + Pillow (assets).
The v1 builder is kept as build_book_v1.py.
"""

import io
import os
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from ebooklib import epub
from PIL import Image, ImageDraw
from fontTools import subset as ft_subset
from fontTools.ttLib import TTFont as FTFont

from reportlab import rl_config
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, PageBreak,
                                PageTemplate, Paragraph, Spacer)
from reportlab.platypus.flowables import ImageAndFlowables

# ============================================================
# CONFIG
# ============================================================
OUTPUT_DIR = str(Path(__file__).resolve().parent)
MANUSCRIPT_DIR = os.path.join(OUTPUT_DIR, "manuscript")
FONT_DIR = os.path.join(OUTPUT_DIR, "fonts")
COVER_IMAGE = os.path.join(OUTPUT_DIR, "cover", "King_of_Teeth_ebook_cover.jpg")
BOOK_TITLE = "King of Teeth"
SERIES = "The Blood Code"
SERIES_NO = 1
AUTHOR = "Aurelia Thorn"
PUB_DATE = "2026"
DESCRIPTION = ("Every woman he feeds on forgets him. She's the one who stayed. "
               "A vampire king hunting his father's killer. A half-wolf bartender "
               "hunting hers. A blood pact, a traitor in the house, and a monster "
               "who has never once been seen for what he is, until now.")

# ---- print geometry (KDP 6 x 9, 301-500 pp: inside margin >= 0.625 in) ----
TRIM_W, TRIM_H = 6 * inch, 9 * inch
M_TOP, M_BOT = 0.80 * inch, 0.80 * inch
M_IN, M_OUT = 0.85 * inch, 0.62 * inch
TEXT_W = TRIM_W - M_IN - M_OUT
HEAD_Y = TRIM_H - 0.50 * inch       # running-head baseline
FOLIO_Y = 0.46 * inch               # folio baseline
BODY_SIZE = 11.36   # 408 pp including fresh-page POV sections; matches the existing cover
BODY_LEAD = 15.65
TARGET_PAGES = 408   # must match the paperback cover (cover/King_of_Teeth_Paperback_408pp_Cream_6x9.pdf)
# KDP black-ink interior: everything is black or gray, so print = proof.
INK = HexColor("#151515")
GRAY = HexColor("#555555")
SOFT = HexColor("#7a7a7a")

# EPUB accent (screens show colour; e-ink shows a dark gray)
EPUB_ACCENT = "#6e1b1b"

NUMBER_WORDS = {}

CHAPTER_ORDER = [
    ("00-prologue.md", "Prologue", "prologue"),
    ("ch-01.md", "Chapter One", "chapter"),
    ("ch-02.md", "Chapter Two", "chapter"),
    ("ch-03.md", "Chapter Three", "chapter"),
    ("I-1.md", "Interlude I", "interstitial"),
    ("ch-04.md", "Chapter Four", "chapter"),
    ("ch-05.md", "Chapter Five", "chapter"),
    ("ch-06.md", "Chapter Six", "chapter"),
    ("ch-07.md", "Chapter Seven", "chapter"),
    ("ch-08.md", "Chapter Eight", "chapter"),
    ("ch-09.md", "Chapter Nine", "chapter"),
    ("I-2.md", "Interlude II", "interstitial"),
    ("ch-10.md", "Chapter Ten", "chapter"),
    ("ch-11.md", "Chapter Eleven", "chapter"),
    ("ch-12.md", "Chapter Twelve", "chapter"),
    ("ch-13.md", "Chapter Thirteen", "chapter"),
    ("ch-14.md", "Chapter Fourteen", "chapter"),
    ("ch-15.md", "Chapter Fifteen", "chapter"),
    ("ch-16.md", "Chapter Sixteen", "chapter"),
    ("ch-17.md", "Chapter Seventeen", "chapter"),
    ("I-3.md", "Interlude III", "interstitial"),
    ("ch-18.md", "Chapter Eighteen", "chapter"),
    ("ch-19.md", "Chapter Nineteen", "chapter"),
    ("ch-20.md", "Chapter Twenty", "chapter"),
    ("ch-21.md", "Chapter Twenty-One", "chapter"),
    ("ch-22.md", "Chapter Twenty-Two", "chapter"),
    ("ch-23.md", "Chapter Twenty-Three", "chapter"),
    ("ch-24.md", "Chapter Twenty-Four", "chapter"),
    ("ch-25.md", "Chapter Twenty-Five", "chapter"),
    ("I-4.md", "Interlude IV", "interstitial"),
    ("ch-26.md", "Chapter Twenty-Six", "chapter"),
    ("ch-27.md", "Chapter Twenty-Seven", "chapter"),
    ("ch-28.md", "Chapter Twenty-Eight", "chapter"),
    ("ch-29.md", "Chapter Twenty-Nine", "chapter"),
    ("ch-30.md", "Chapter Thirty", "chapter"),
    ("I-5.md", "Interlude V", "interstitial"),
    ("ch-31.md", "Chapter Thirty-One", "chapter"),
    ("ch-32.md", "Chapter Thirty-Two", "chapter"),
    ("ch-33.md", "Chapter Thirty-Three", "chapter"),
    ("ch-34.md", "Chapter Thirty-Four", "chapter"),
    ("ch-35.md", "Chapter Thirty-Five", "chapter"),
    ("ch-36.md", "Chapter Thirty-Six", "chapter"),
    ("epilogue.md", "Epilogue", "epilogue"),
    ("bonus-ghost-that-stayed.md", "Bonus Scene: The Ghost That Stayed", "bonus"),
    ("teaser-vow-of-poison.md", "Sneak Peek: Vow of Poison", "teaser"),
]

FRONT_MATTER_FILE = os.path.join(OUTPUT_DIR, "FRONT_MATTER.md")
FRONT_PAGES = ["Copyright", "Dedication", "Before You Begin"]
BACK_PAGES = ["The Blood Code", "Playlist", "Thank You"]
NO_TOC_PAGES = {"Copyright", "Dedication"}

# ============================================================
# SHARED TEXT UTILITIES
# ============================================================


def front_sections():
    """{section title: [paragraph, ...]} for the ## sections of FRONT_MATTER.md."""
    with open(FRONT_MATTER_FILE, "r", encoding="utf-8") as f:
        text = f.read()
    out = {}
    for block in re.split(r"^## ", text, flags=re.MULTILINE)[1:]:
        title, _, body = block.partition("\n")
        body = body.split("\n---")[0]
        out[title.strip()] = [p.strip() for p in re.split(r"\n\s*\n", body.strip()) if p.strip()]
    return out


def read_manuscript(filename):
    with open(os.path.join(MANUSCRIPT_DIR, filename), "r", encoding="utf-8") as f:
        return f.read()


def chapter_pov(filename):
    """'# 1 · Selene' -> 'Selene'; teaser '# Vow of Poison · Chapter One · Silas' -> 'Silas'."""
    first = read_manuscript(filename).lstrip().split("\n", 1)[0]
    m = re.match(r"^#\s+.*·\s*([A-Za-zÀ-ÿ]+)\s*$", first)
    return m.group(1) if m else None


def clean_markdown(text):
    """Strip the # title line, placement notes and similar metadata."""
    text = text.replace("\r\n", "\n")
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    clean, in_header = [], True
    for line in text.split("\n"):
        if in_header:
            if re.match(r"^#\s", line):
                continue
            if re.match(r"^\*?(Placement|POV|Word count|Heat|Chapter)", line, re.IGNORECASE):
                continue
            if line.strip() == "" and not clean:
                continue
            if line.strip():
                in_header = False
        if not in_header:
            clean.append(line)
    return "\n".join(clean).strip()


def split_paragraphs(text):
    """Paragraph blocks, with {SCENE_BREAK} and {POV:Name} markers.

    A scene break that sits directly before a POV heading is dropped: the POV
    label carries its own ornament, and two ornaments in a row look like a typo.
    """
    text = clean_markdown(text)
    text = re.sub(r"\n\s*[-*]{3,}\s*\n", "\n\n{SCENE_BREAK}\n\n", text)
    # [ \t] not \s: \s would swallow the blank line and glue the heading to the next paragraph
    text = re.sub(r"^##[ \t]+(?:§[ \t]*\d+[ \t]*[—-][ \t]*)?(.+?)[ \t]*$", r"{POV:\1}", text, flags=re.MULTILINE)
    paras = [p.strip() for p in re.split(r"\n\n+", text.strip()) if p.strip()]
    out = []
    for p in paras:
        if p.startswith("{POV:") and out and out[-1] == "{SCENE_BREAK}":
            out.pop()
        out.append(p)
    return out


def smart_quotes(text):
    """Straight quotes to typographic ones, deciding by both neighbours."""
    out, n = [], len(text)
    for i, ch in enumerate(text):
        if ch not in "\"'":
            out.append(ch)
            continue
        prev = text[i - 1] if i else ""
        nxt = text[i + 1] if i + 1 < n else ""
        after_word = nxt != "" and (nxt.isalnum() or nxt in "*_\u2026")
        prev2 = text[i - 2] if i > 1 else ""
        before_open = (prev == "" or prev.isspace() or prev in "([\u2014\u2013"
                       or (prev in "*_" and (prev2 == "" or prev2.isspace())))
        if ch == '"':
            out.append("\u201c" if before_open and after_word else "\u201d")
        elif prev.isalnum():
            out.append("\u2019")
        elif before_open and after_word:
            out.append("\u2018")
        else:
            out.append("\u2019")
    text = "".join(out)
    return re.sub(r"\u2018(?=(?:em|til|cause|round|bout)\b|\d\ds?\b|n\u2019)", "\u2019",
                  text, flags=re.IGNORECASE)


def convert_inline(text):
    """*italic* / **bold** to <i>/<b>; -- to em dash; escape &, <, >."""
    text = smart_quotes(text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    text = re.sub(r"(?<![A-Za-z0-9])_(.+?)_(?![A-Za-z0-9])", r"<i>\1</i>", text)
    text = text.replace(" -- ", " \u2014 ").replace("--", "\u2014")
    return text


LEAD_RE = re.compile(r"^((?:[A-Za-zÀ-ÿ\u2019'\-]+)(?:\s+[A-Za-zÀ-ÿ\u2019'\-]+){0,3})")


def split_lead(html, min_chars=9, max_words=3):
    """Split a paragraph's opening words off for a small-caps lead-in.

    Returns (lead, rest). Takes whole words up to ~min_chars, stopping at any
    punctuation or markup, so the lead never breaks inside a tag.
    """
    words, used, i = [], 0, 0
    for m in re.finditer(r"[A-Za-zÀ-ÿ\u2019'\-]+|\s+|.", html):
        tok = m.group(0)
        if tok.isspace():
            if not words:
                break
            i = m.end()
            continue
        if not re.fullmatch(r"[A-Za-zÀ-ÿ\u2019'\-]+", tok):
            break
        words.append(tok)
        used += len(tok)
        i = m.end()
        if used >= min_chars or len(words) >= max_words:
            break
    if not words:
        return "", html
    lead = html[:i].rstrip()
    return lead, html[len(lead):]


def number_word(title):
    return title.split(" ", 1)[1] if title.startswith("Chapter ") else title


# ============================================================
# FONTS
# ============================================================
F = {
    "Body": "CrimsonText-Regular.ttf",
    "Body-Italic": "CrimsonText-Italic.ttf",
    "Body-Bold": "CrimsonText-SemiBold.ttf",
    "Body-BoldItalic": "CrimsonText-BoldItalic.ttf",
    "Disp": "CormorantGaramond-Medium.ttf",
    "Disp-Italic": "CormorantGaramond-Italic.ttf",
    "Disp-MedIt": "CormorantGaramond-MediumItalic.ttf",
    "Disp-Semi": "CormorantGaramond-SemiBold.ttf",
    "Disp-Bold": "CormorantGaramond-Bold.ttf",
    "SC": "KoTSmallCaps-SemiBold.ttf",
    "SC-Med": "KoTSmallCaps-Medium.ttf",
}
for name, fn in F.items():
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fn)))
addMapping("Body", 0, 0, "Body")
addMapping("Body", 1, 0, "Body-Bold")
addMapping("Body", 0, 1, "Body-Italic")
addMapping("Body", 1, 1, "Body-BoldItalic")
rl_config.canvas_basefontname = "Body"   # keep Helvetica out of the PDF (KDP embeds check)


def cap_ratio(font):
    return pdfmetrics.getFont(font).face.capHeight / 1000.0


# ============================================================
# PDF FLOWABLES
# ============================================================
DOC = None  # the active BookDoc; markers write page flags onto it


class PageFlag(Flowable):
    """Zero-size marker: tags the page it lands on (opener, front, blank...)."""

    def __init__(self, *flags, record=None, bookmark=None):
        super().__init__()
        self.flags, self.record = flags, record
        self.bookmark = bookmark
        self.width = self.height = 0

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        DOC.page_flags.update(self.flags)
        if self.record:
            DOC.recorded[self.record] = DOC.page
        if self.bookmark:
            key, title = self.bookmark
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, level=0)
            DOC.recorded[key] = DOC.page
        if self.record == "prologue":
            self.canv.addPageLabel(DOC.page - 1, style="D", start=1)


class Crown(Flowable):
    """A fine-lined crown with tapered rules, drawn as vectors for print."""

    def __init__(self, width=96, color=INK, height=12):
        super().__init__()
        self.w, self.color, self.h = width, color, height

    def wrap(self, aw, ah):
        self.width, self.height = aw, self.h
        return aw, self.h

    def draw(self):
        c = self.canv
        cx, cy = self.width / 2, self.h / 2
        c.saveState()
        c.setStrokeColor(self.color)
        c.setFillColor(self.color)
        c.setLineWidth(0.55)
        p = c.beginPath()
        p.moveTo(cx - 6.5, cy - 2.5)
        for dx, dy in [(-8, 3.5), (-3, 0.5), (0, 5), (3, 0.5), (8, 3.5), (6.5, -2.5)]:
            p.lineTo(cx + dx, cy + dy)
        p.close()
        c.drawPath(p, stroke=1, fill=0)
        c.line(cx - 6, cy - 4.2, cx + 6, cy - 4.2)
        for sign in (-1, 1):
            p = c.beginPath()
            p.moveTo(cx + sign * 15, cy + .35)
            p.lineTo(cx + sign * self.w / 2, cy)
            p.lineTo(cx + sign * 15, cy - .35)
            p.close()
            c.drawPath(p, stroke=0, fill=1)
        c.restoreState()


class Tracked(Flowable):
    """One line of letter-spaced display text, centred on the measure."""

    def __init__(self, text, font, size, tracking=0.0, color=INK, space_after=0, lead=None):
        super().__init__()
        self.text, self.font, self.size = text, font, size
        self.tracking, self.color, self.space_after = tracking, color, space_after
        self.lead = lead if lead is not None else size * 1.2

    def wrap(self, aw, ah):
        self.width = aw
        self.height = self.lead + self.space_after
        return self.width, self.height

    def draw(self):
        c = self.canv
        w = pdfmetrics.stringWidth(self.text, self.font, self.size) + self.tracking * (len(self.text) - 1)
        t = c.beginText()
        t.setTextOrigin((self.width - w) / 2, self.space_after + (self.lead - self.size) / 2 + self.size * 0.18)
        t.setFont(self.font, self.size)
        t.setCharSpace(self.tracking)
        t.setFillColor(self.color)
        t.textOut(self.text)
        t.setCharSpace(0)          # PDF text state persists: never leak tracking into body text
        c.saveState()
        c.drawText(t)
        c.restoreState()


class Fleuron(Flowable):
    """Hairline - diamond - hairline, tapering outward."""

    def __init__(self, width=96, color=INK, gap=6, d=3.2, height=12):
        super().__init__()
        self.w, self.color, self.gap, self.d, self.h = width, color, gap, d, height

    def wrap(self, aw, ah):
        self.width = aw
        self.height = self.h
        return self.width, self.height

    def draw(self):
        c = self.canv
        cx, cy = self.width / 2, self.h / 2
        c.saveState()
        c.setFillColor(self.color)
        c.setStrokeColor(self.color)
        half = self.w / 2
        for sgn in (-1, 1):
            p = c.beginPath()           # tapered hairline: thick near the diamond
            x0, x1 = cx + sgn * (self.d + self.gap), cx + sgn * half
            p.moveTo(x0, cy + 0.55)
            p.lineTo(x1, cy)
            p.lineTo(x0, cy - 0.55)
            p.close()
            c.drawPath(p, fill=1, stroke=0)
        p = c.beginPath()
        p.moveTo(cx, cy + self.d)
        p.lineTo(cx + self.d, cy)
        p.lineTo(cx, cy - self.d)
        p.lineTo(cx - self.d, cy)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()


class SceneBreak(Flowable):
    """Three small diamonds; takes two lines of the grid and stays with its next paragraph."""

    def __init__(self):
        super().__init__()
        self.keepWithNext = 1

    def wrap(self, aw, ah):
        self.width, self.height = aw, BODY_LEAD * 2
        return self.width, self.height

    def draw(self):
        c = self.canv
        cx, cy, d = self.width / 2, self.height / 2 + 1, 2.3
        c.saveState()
        c.setFillColor(GRAY)
        for dx in (-16, 0, 16):
            p = c.beginPath()
            p.moveTo(cx + dx, cy + d)
            p.lineTo(cx + dx + d, cy)
            p.lineTo(cx + dx, cy - d)
            p.lineTo(cx + dx - d, cy)
            p.close()
            c.drawPath(p, fill=1, stroke=0)
        c.restoreState()


class DropCap(Flowable):
    """Three-line drop cap in Cormorant SemiBold.

    Its cap height runs from the top of line one's capitals to the baseline of
    line three. An opening quote hangs in the margin. Used inside
    ImageAndFlowables so exactly three lines wrap beside it.
    """
    LINES = 3

    def __init__(self, letter, quote=""):
        super().__init__()
        self.letter, self.quote = letter, quote
        target = (self.LINES - 1) * BODY_LEAD + BODY_SIZE * cap_ratio("Body")
        self.size = target / cap_ratio("Disp-Semi")
        self.gap = 3.2

    def wrap(self, aw, ah):
        self.width = pdfmetrics.stringWidth(self.letter, "Disp-Semi", self.size) + self.gap
        self.height = self.LINES * BODY_LEAD
        return self.width, self.height

    def _restrictSize(self, aw, ah):     # ImageAndFlowables treats us as its image
        return self.wrap(aw, ah)

    def _unRestrictSize(self):
        pass

    def draw(self):
        c = self.canv
        base = self.height - BODY_SIZE - (self.LINES - 1) * BODY_LEAD
        c.saveState()
        c.setFillColor(INK)
        c.setFont("Disp-Semi", self.size)
        c.drawString(0, base, self.letter)
        if self.quote:
            qs = self.size * 0.42
            qw = pdfmetrics.stringWidth(self.quote, "Disp-Semi", qs)
            c.setFont("Disp-Semi", qs)
            top = base + self.size * cap_ratio("Disp-Semi")
            c.drawString(-qw - 1.5, top - qs * 0.72, self.quote)
        c.restoreState()


# ============================================================
# PDF STYLES
# ============================================================
def make_styles():
    s = {}
    s["body"] = ParagraphStyle(
        "body", fontName="Body", fontSize=BODY_SIZE, leading=BODY_LEAD, textColor=INK,
        alignment=TA_JUSTIFY, firstLineIndent=BODY_SIZE * 1.25,
        hyphenationLang="en_US", embeddedHyphenation=0,   # 1 duplicates words across splits (RL 5 bug)
        allowWidows=0, allowOrphans=0)
    s["body_first"] = ParagraphStyle("body_first", parent=s["body"], firstLineIndent=0)
    s["fm_body"] = ParagraphStyle("fm_body", parent=s["body"], fontSize=9.6, leading=12.6,
                                  firstLineIndent=0, spaceAfter=4.2)
    s["fm_bullet"] = ParagraphStyle("fm_bullet", parent=s["fm_body"], leftIndent=12,
                                    bulletIndent=2, spaceAfter=1.8, bulletFontName="Body")
    s["fm_center_it"] = ParagraphStyle("fm_center_it", parent=s["fm_body"], fontName="Disp-MedIt",
                                       fontSize=11.5, leading=14, alignment=TA_CENTER,
                                       hyphenationLang=None, spaceBefore=3)
    s["fm_center"] = ParagraphStyle("fm_center", parent=s["fm_body"], alignment=TA_CENTER,
                                    hyphenationLang=None)
    s["copyright"] = ParagraphStyle("copyright", fontName="Body", fontSize=8.3, leading=11.2,
                                    textColor=INK, alignment=TA_LEFT, spaceAfter=5.5)
    s["dedication"] = ParagraphStyle("dedication", fontName="Disp-MedIt", fontSize=15,
                                     leading=21, textColor=INK, alignment=TA_CENTER)
    s["subtitle_it"] = ParagraphStyle("subtitle_it", fontName="Disp-MedIt", fontSize=14,
                                      leading=18, textColor=GRAY, alignment=TA_CENTER)
    s["playlist"] = ParagraphStyle("playlist", fontName="Body", fontSize=10.4, leading=17,
                                   textColor=INK, alignment=TA_CENTER)
    return s


def lead_html(html):
    """Paragraph markup with the opening words in true small caps.

    Leading space (after a one-letter drop cap such as "I") stays outside the lead.
    """
    pre = re.match(r"^\s*", html).group(0)
    lead, rest = split_lead(html[len(pre):])
    if not lead:
        return html
    return f'{pre}<font name="SC" size="{BODY_SIZE + 0.6}">{lead.lower()}</font>{rest}'


def opener_paragraph(html, styles):
    """Drop cap + small-caps lead-in for the first paragraph of a chapter or section."""
    m = re.match(r"^([\u201c\u2018]?)([A-Za-zÀ-ÿ])", html)
    if not m:
        return [Paragraph(lead_html(html), styles["body_first"])]
    quote, letter = m.group(1), m.group(2)
    rest = html[m.end():]
    # the rest of the first word joins the small-caps lead
    para = Paragraph(lead_html(rest), styles["body_first"])
    return [ImageAndFlowables(DropCap(letter, quote), [para], imageSide="left",
                              imageLeftPadding=0, imageRightPadding=0,
                              imageTopPadding=0, imageBottomPadding=0)]


def after_break_paragraph(html, styles):
    return Paragraph(lead_html(html), styles["body_first"])


# ============================================================
# PDF DOCUMENT
# ============================================================
class BookDoc(BaseDocTemplate):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.page_flags = set()
        self.recorded = {}


def on_page(canvas, doc):
    """Page begin: mirror the text block (recto: gutter on the left)."""
    fr = doc.pageTemplate.frames[0]
    fr._x1 = M_IN if doc.page % 2 == 1 else M_OUT
    fr._geom()
    if doc.page == 1:
        canvas.addPageLabel(0, style="ROMAN_LOWER", start=1)


def tracked_center(c, text, font, size, tracking, y, color):
    w = pdfmetrics.stringWidth(text, font, size) + tracking * (len(text) - 1)
    x = (M_IN if c.getPageNumber() % 2 == 1 else M_OUT) + (TEXT_W - w) / 2
    t = c.beginText()
    t.setTextOrigin(x, y)
    t.setFont(font, size)
    t.setCharSpace(tracking)
    t.setFillColor(color)
    t.textOut(text)
    t.setCharSpace(0)
    c.drawText(t)


def on_page_end(canvas, doc):
    """Page end: running head and folio, according to the page's flags."""
    flags = doc.page_flags
    doc.page_flags = set()
    if flags & {"blank", "front", "back"}:
        return
    n = doc.page
    canvas.saveState()
    if "opener" not in flags:
        head = AUTHOR.lower() if n % 2 == 0 else BOOK_TITLE.lower()
        tracked_center(canvas, head, "SC-Med", 9.6, 1.9, HEAD_Y, GRAY)
    folio = n - doc.recorded.get("prologue", 1) + 1
    tracked_center(canvas, str(folio), "Body", 9.5, 0.3, FOLIO_Y, GRAY)
    canvas.restoreState()


def title_page_story(styles):
    st = []
    # 1 - half title
    st += [PageFlag("front"), Spacer(1, 2.7 * inch),
           Tracked("KING OF TEETH", "Disp-Semi", 17, 5.2), PageBreak()]
    # 2 - blank verso
    st += [PageFlag("blank"), Spacer(1, 1), PageBreak()]
    # 3 - title page
    st += [PageFlag("front", bookmark=("title", BOOK_TITLE)), Spacer(1, 1.55 * inch),
           Crown(150, INK), Spacer(1, 22),
           Tracked("KING", "Disp-Bold", 60, 7, INK, lead=62),
           Tracked("of", "Disp-Italic", 27, 1, GRAY, lead=30),
           Tracked("TEETH", "Disp-Bold", 60, 7, INK, lead=62),
           Spacer(1, 20), Fleuron(150, INK), Spacer(1, 14),
           Tracked("the blood code \u00b7 book one", "SC-Med", 11.5, 3.2, GRAY),
           Spacer(1, 1.75 * inch),
           Tracked("AURELIA THORN", "Disp-Semi", 16, 5.5, INK),
           PageBreak()]
    return st


def front_page_story(name, paras, styles):
    st = []
    if name == "Copyright":
        st += [PageFlag("front"), Spacer(1, 4.1 * inch)]
        for p in paras:
            st.append(Paragraph(convert_inline(p), styles["copyright"]))
    elif name == "Dedication":
        st += [PageFlag("front"), Spacer(1, 2.35 * inch)]
        for p in paras:
            st.append(Paragraph(convert_inline(p), styles["dedication"]))
            st.append(Spacer(1, 6))
        st += [Spacer(1, 16), Fleuron(70, GRAY)]
        st += [PageBreak(), PageFlag("blank"), Spacer(1, 1)]      # 6 - blank verso
    else:
        st += [PageFlag("front", bookmark=("before-you-begin", name)), Spacer(1, 0.05 * inch),
               Tracked(name.lower(), "SC", 13, 3.4, INK, space_after=6),
               Fleuron(80, INK), Spacer(1, 12)]
        for k, p in enumerate(paras):
            lines = [l.strip() for l in p.split("\n") if l.strip()]
            if all(l.startswith("- ") for l in lines):
                for l in lines:
                    st.append(Paragraph(convert_inline(l[2:]), styles["fm_bullet"], bulletText="\u2022"))
                st.append(Spacer(1, 3))
            else:
                closing = k >= len(paras) - 2          # "If you're still here..." / "Welcome..."
                style = styles["fm_center_it"] if closing else styles["fm_body"]
                st.append(Paragraph("<br/>".join(convert_inline(l) for l in lines), style))
        st.append(PageFlag("front"))   # second page of Before You Begin
    st.append(PageBreak())
    return st


def back_page_story(name, paras, styles):
    st = [PageFlag("back", bookmark=(name.lower().replace(" ", "-"), name)), Spacer(1, 1.2 * inch),
          Tracked(name.lower(), "SC", 13, 3.4, INK, space_after=6),
          Fleuron(80, INK), Spacer(1, 18)]
    for p in paras:
        lines = [l.strip() for l in p.split("\n") if l.strip()]
        if name == "Playlist":
            for l in lines:
                st.append(Paragraph(convert_inline(l), styles["playlist"]))
        elif all(re.match(r"^\d+\.\s", l) for l in lines):
            for l in lines:
                st.append(Paragraph(convert_inline(re.sub(r"^\d+\.\s*", "", l)), styles["playlist"]))
            st.append(Spacer(1, 10))
        else:
            st.append(Paragraph("<br/>".join(convert_inline(l) for l in lines), styles["fm_center"]))
    st.append(PageBreak())
    return st


def opener_story(filename, title, ch_type, styles):
    """The display block at the head of a chapter-type unit."""
    st = [PageFlag("opener", bookmark=(filename.removesuffix(".md"), title)), Spacer(1, 1.35 * inch)]
    pov = chapter_pov(filename)
    if ch_type == "chapter":
        st += [Crown(96, INK), Spacer(1, 14),
               Tracked("chapter", "SC-Med", 11, 3.6, GRAY),
               Tracked(number_word(title), "Disp-MedIt", 34, 0.4, INK, lead=40),
               Spacer(1, 6),
               Tracked((pov or "").lower(), "SC", 12.5, 4.2, INK)]
    elif ch_type == "interstitial":
        st += [Fleuron(96, GRAY), Spacer(1, 14),
               Tracked(title.split()[0].lower() + " " + title.split()[1], "SC-Med", 11, 3.6, GRAY),
               Tracked("Cassian", "Disp-MedIt", 34, 0.4, INK, lead=40)]
    elif ch_type == "prologue":
        st += [Fleuron(96, INK), Spacer(1, 14),
               Tracked("Prologue", "Disp-MedIt", 38, 0.4, INK, lead=44)]
    elif ch_type == "epilogue":
        st += [Fleuron(96, INK), Spacer(1, 14),
               Tracked("Epilogue", "Disp-MedIt", 38, 0.4, INK, lead=44),
               Spacer(1, 4),
               Tracked("we\u2019re not finished", "SC-Med", 11, 3.2, GRAY)]
    elif ch_type == "bonus":
        st += [Tracked("bonus scene", "SC-Med", 11, 3.6, GRAY), Spacer(1, 6),
               Fleuron(96, INK), Spacer(1, 12),
               Tracked("The Ghost That Stayed", "Disp-MedIt", 29, 0.3, INK, lead=36),
               Spacer(1, 4),
               Paragraph("Chapter Eleven, from her side of the bed", styles["subtitle_it"])]
    elif ch_type == "teaser":
        st += [Tracked("a first look at book two", "SC-Med", 11, 3.6, GRAY), Spacer(1, 6),
               Fleuron(96, INK), Spacer(1, 12),
               Tracked("Vow of Poison", "Disp-MedIt", 34, 0.4, INK, lead=40),
               Spacer(1, 6),
               Tracked("chapter one \u00b7 " + (pov or "").lower(), "SC", 11.5, 3.6, INK)]
    st.append(Spacer(1, 0.46 * inch))
    for piece in st:
        piece.keepWithNext = 1
    return st


def pov_label(name):
    """In-chapter POV switch (prologue, epilogue)."""
    return [Spacer(1, BODY_LEAD * 0.6), Fleuron(60, GRAY, d=2.6, height=10),
            Spacer(1, 4), Tracked(name.lower(), "SC", 11.5, 3.8, INK, space_after=BODY_LEAD * 0.55)]


def body_story(filename, styles):
    st = []
    first, after_break = True, False
    pov_index = 0
    paras = split_paragraphs(read_manuscript(filename))
    for i, para in enumerate(paras):
        if para == "{SCENE_BREAK}":
            st.append(SceneBreak())
            after_break = True
            continue
        if para.startswith("{POV:"):
            pov_index += 1
            label = pov_label(para[5:-1])
            if first:                       # prologue opens straight onto a POV label
                label = label[3:]
            else:
                st += [PageBreak(), PageFlag("opener", record=f"{filename.removesuffix('.md')}-pov-{pov_index}"),
                       Spacer(1, 0.6 * inch)]
            for piece in label:            # ornament + name + next paragraph stay together
                piece.keepWithNext = 1
            st += label
            first = True
            continue
        html = convert_inline(para).replace("\n", " ")
        if first:
            st += opener_paragraph(html, styles)
            first = after_break = False
        elif after_break:
            st.append(after_break_paragraph(html, styles))
            after_break = False
        else:
            st.append(Paragraph(html, styles["body"]))
    return st


def build_story(styles, extra_blank_before_prologue=False):
    story = title_page_story(styles)
    fm = front_sections()
    for name in FRONT_PAGES:
        story += front_page_story(name, fm[name], styles)
    if extra_blank_before_prologue:
        story += [PageFlag("blank"), Spacer(1, 1), PageBreak()]
    for filename, title, ch_type in CHAPTER_ORDER:
        if ch_type == "teaser":
            story.append(PageBreak())
            for name in BACK_PAGES:
                story += back_page_story(name, fm[name], styles)
        elif filename != CHAPTER_ORDER[0][0]:
            story.append(PageBreak())
        if filename == CHAPTER_ORDER[0][0]:
            story.append(PageFlag(record="prologue"))
        story += opener_story(filename, title, ch_type, styles)
        story += body_story(filename, styles)
    # end page
    story += [PageBreak(), PageFlag("back"), Spacer(1, 2.4 * inch),
              Tracked("end of book one", "SC", 13, 3.6, INK, space_after=8),
              Fleuron(110, INK), Spacer(1, 22),
              Paragraph("The Blood Code continues with Silas &amp; Ondine in", styles["subtitle_it"]),
              Spacer(1, 8),
              Tracked("VOW OF POISON", "Disp-Semi", 17, 5, INK)]
    return story


def build_pdf():
    global DOC
    print("Building PDF...")
    styles = make_styles()
    out = os.path.join(OUTPUT_DIR, "King_of_Teeth.pdf")
    for extra in (False, True):
        DOC = BookDoc(out, pagesize=(TRIM_W, TRIM_H), leftMargin=M_IN, rightMargin=M_OUT,
                      topMargin=M_TOP, bottomMargin=M_BOT, title=BOOK_TITLE, author=AUTHOR,
                      subject=f"{SERIES}, Book {SERIES_NO}", creator=AUTHOR)
        frame = Frame(M_IN, M_BOT, TEXT_W, TRIM_H - M_TOP - M_BOT, id="text",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        DOC.addPageTemplates([PageTemplate(id="book", frames=[frame],
                                           onPage=on_page, onPageEnd=on_page_end)])
        DOC.build(build_story(styles, extra))
        if DOC.recorded.get("prologue", 1) % 2 == 1:   # prologue on a recto: done
            break
        print("  prologue fell on a verso; adding a blank page and rebuilding")
    print(f"  PDF saved: {out}  (prologue p.{DOC.recorded.get('prologue')}, {DOC.page} pages)")
    import json
    Path(OUTPUT_DIR, "layout-page-map.json").write_text(
        json.dumps({"pages": DOC.page, "starts": DOC.recorded}, indent=2), encoding="utf-8")
    if DOC.page != TARGET_PAGES:
        print(f"  !! PAGE COUNT {DOC.page} != {TARGET_PAGES}: the cover spine no longer fits. Nudge "
              f"BODY_SIZE by 0.02-0.05 until it is {TARGET_PAGES}, or have the cover re-exported.")
    return out


# ============================================================
# EPUB
# ============================================================
EPUB_FONT_FILES = {
    "CrimsonText-Regular.ttf": ("Crimson Text", "normal", "normal"),
    "CrimsonText-Italic.ttf": ("Crimson Text", "normal", "italic"),
    "CrimsonText-SemiBold.ttf": ("Crimson Text", "bold", "normal"),
    "CrimsonText-BoldItalic.ttf": ("Crimson Text", "bold", "italic"),
    "CormorantGaramond-SemiBold.ttf": ("Cormorant Garamond", "600", "normal"),
    "CormorantGaramond-MediumItalic.ttf": ("Cormorant Garamond", "500", "italic"),
    "CormorantGaramond-Bold.ttf": ("Cormorant Garamond", "bold", "normal"),
    "KoTSmallCaps-SemiBold.ttf": ("KoT Small Caps", "normal", "normal"),
}


def subset_font(path, text):
    """Subset to the characters the book uses: keeps the EPUB (and KDP's per-MB delivery fee) small."""
    f = FTFont(path)
    opts = ft_subset.Options()
    opts.layout_features = ["kern", "liga"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    sub = ft_subset.Subsetter(opts)
    sub.populate(text=text)
    sub.subset(f)
    buf = io.BytesIO()
    f.save(buf)
    return buf.getvalue()


def ornament_png(kind, color=EPUB_ACCENT):
    """Anti-aliased ornaments drawn at 4x and downsampled."""
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    S = 4
    if kind in {"fleuron", "crown"}:
        W, H = 360, 30
    else:
        W, H = 150, 24
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cy = H * S // 2
    col = (r, g, b, 255)
    if kind == "crown":
        cx = W * S // 2
        pts = [(-20, -8), (-25, 10), (-9, 1), (0, 14), (9, 1), (25, 10), (20, -8), (-20, -8)]
        d.line([(cx + dx*S, cy-dy*S) for dx, dy in pts], fill=col, width=2*S)
        d.line([(cx-18*S,cy+12*S),(cx+18*S,cy+12*S)], fill=col, width=2*S)
        for sign in (-1, 1):
            d.polygon([(cx+sign*45*S,cy-S),(cx+sign*176*S,cy),(cx+sign*45*S,cy+S)],fill=col)
    elif kind == "fleuron":
        cx, dd = W * S // 2, 9 * S
        d.polygon([(cx, cy - dd), (cx + dd, cy), (cx, cy + dd), (cx - dd, cy)], fill=col)
        for sgn in (-1, 1):
            x0, x1 = cx + sgn * (dd + 14 * S), cx + sgn * (W * S // 2 - 4)
            d.polygon([(x0, cy - 2 * S), (x1, cy), (x0, cy + 2 * S)], fill=col)
    else:
        dd = 6 * S
        for cx in (W * S // 2 - 40 * S, W * S // 2, W * S // 2 + 40 * S):
            d.polygon([(cx, cy - dd), (cx + dd, cy), (cx, cy + dd), (cx - dd, cy)], fill=col)
    im = im.resize((W, H), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def epub_css():
    faces = "\n".join(
        f'@font-face {{ font-family: "{fam}"; font-weight: {w}; font-style: {s}; '
        f'src: url("../fonts/{fn}"); }}'
        for fn, (fam, w, s) in EPUB_FONT_FILES.items())
    return faces + f"""
@page {{ margin: 5%; }}
body {{ font-family: "Crimson Text", Georgia, serif; line-height: 1.5; margin: 0; padding: 0;
        orphans: 2; widows: 2; }}
.book-section {{ page-break-before: always; break-before: page; }}
p {{ margin: 0; text-indent: 1.3em; text-align: justify; hyphens: auto; -webkit-hyphens: auto; }}
p.first, p.after-break, p.noindent {{ text-indent: 0; }}
p.first {{ orphans: 3; }}
span.dropcap {{ font-family: "Cormorant Garamond", Georgia, serif; font-weight: 600;
        font-size: 2.6em; line-height: 0; vertical-align: baseline; color: {EPUB_ACCENT}; }}
span.lead {{ font-family: "KoT Small Caps", "Cormorant Garamond", Georgia, serif;
        font-variant: small-caps; text-transform: lowercase; letter-spacing: 0.04em; }}
.head {{ text-align: center; margin: 2.6em 0 1.8em; page-break-inside: avoid; break-inside: avoid;
        page-break-after: avoid; break-after: avoid; }}
.head p {{ text-indent: 0; text-align: center; }}
.head h1, .head p {{ hyphens: none; -webkit-hyphens: none; }}
.chapter-label {{ display: block; font-family: "KoT Small Caps", Georgia, serif; font-variant: small-caps;
        font-size: 0.4em; font-style: normal; letter-spacing: 0.28em; margin: 0.9em 0 0.2em; }}
.chapter-number {{ display: block; }}
.label {{ font-family: "KoT Small Caps", "Cormorant Garamond", serif; font-variant: small-caps;
        letter-spacing: 0.28em; font-size: 0.95em; color: #5a5a5a; margin: 0.9em 0 0.1em 0; }}
h1.num, h1.title {{ font-family: "Cormorant Garamond", Georgia, serif; font-style: italic;
        font-weight: 500; font-size: 2.35em; line-height: 1.15; margin: 0.05em 0 0.15em 0;
        color: inherit; }}
.pov {{ font-family: "KoT Small Caps", "Cormorant Garamond", serif; font-variant: small-caps;
        letter-spacing: 0.32em; font-size: 1.05em; margin: 0.2em 0 0 0; color: {EPUB_ACCENT}; }}
.sub {{ font-family: "Cormorant Garamond", Georgia, serif; font-style: italic; font-size: 1.1em;
        color: #555; margin-top: 0.3em; }}
p.orn {{ text-align: center; text-indent: 0; margin: 0; }}
p.orn img {{ width: 38%; max-width: 12em; height: auto; }}
p.scene {{ text-align: center; text-indent: 0; margin: 1.1em 0;
        page-break-inside: avoid; break-inside: avoid; page-break-after: avoid; break-after: avoid; }}
p.scene img {{ width: 18%; max-width: 5em; height: auto; }}
.pov-shift {{ text-align: center; margin: 1.8em 0 0.9em 0;
        page-break-inside: avoid; break-inside: avoid; page-break-after: avoid; break-after: avoid; }}
.head + .pov-shift {{ margin-top: 0; }}
.pov-shift p {{ text-indent: 0; text-align: center; }}
.titlepage {{ text-align: center; margin-top: 18%; }}
.titlepage p {{ text-indent: 0; text-align: center; }}
.t-big {{ font-family: "Cormorant Garamond", Georgia, serif; font-weight: bold; font-size: 3.1em;
        letter-spacing: 0.14em; line-height: 1.05; margin: 0; color: inherit; }}
.t-of {{ font-family: "Cormorant Garamond", Georgia, serif; font-style: italic; font-size: 1.5em;
        color: #555; margin: 0; }}
.t-series {{ font-family: "KoT Small Caps", "Cormorant Garamond", serif; font-variant: small-caps;
        letter-spacing: 0.25em; color: #555; margin-top: 0.8em; }}
.t-author {{ font-family: "Cormorant Garamond", Georgia, serif; font-weight: 600;
        letter-spacing: 0.3em; font-size: 1.2em; margin-top: 3.2em; }}
.copyright {{ font-size: 0.8em; margin-top: 30%; }}
.copyright p {{ text-indent: 0; margin-bottom: 0.7em; text-align: left; }}
.dedication {{ margin-top: 30%; text-align: center; }}
.dedication p {{ font-family: "Cormorant Garamond", Georgia, serif; font-style: italic;
        font-size: 1.3em; text-indent: 0; text-align: center; margin-bottom: 0.3em; }}
.matter p {{ text-indent: 0; margin-bottom: 0.7em; }}
.matter p.c {{ text-align: center; }}
.matter ul {{ margin: 0.2em 0 0.9em 1.2em; padding: 0; }}
.matter li {{ margin-bottom: 0.35em; text-align: left; }}
.list p {{ text-align: center; text-indent: 0; margin-bottom: 0.45em; }}
.contents p {{ text-indent: 0; text-align: left; margin: 0; padding: 0.5em 0;
        border-bottom: 1px solid #bbb; page-break-inside: avoid; break-inside: avoid; }}
.contents a {{ color: inherit; text-decoration: none; display: block; }}
.contents .toc-pov {{ font-style: italic; font-size: 0.9em; }}
.end {{ text-align: center; margin-top: 30%; }}
.end p {{ text-indent: 0; text-align: center; }}
@media (prefers-color-scheme: dark) {{
  .label, .sub, .t-of, .t-series {{ color: inherit; }}
  .pov, span.dropcap {{ color: #dca2a2; }}
  .orn img, .scene img {{ filter: brightness(2.7); }}
}}
@media (max-width: 420px) {{
  .head {{ margin-top: 1.5em; margin-bottom: 1.3em; }}
  .t-big {{ font-size: 2.6em; letter-spacing: 0.08em; }}
  .t-author {{ letter-spacing: 0.16em; }}
  .label, .pov, .t-series {{ letter-spacing: 0.16em; }}
}}
"""


def x(text):
    return escape(text)


def epub_lead(html):
    pre = re.match(r"^\s*", html).group(0)
    lead, rest = split_lead(html[len(pre):])
    return (f'{pre}<span class="lead">{lead}</span>{rest}') if lead else html


def epub_opener_p(html):
    m = re.match(r"^([\u201c\u2018]?)([A-Za-zÀ-ÿ])", html)
    if not m:
        return f'<p class="first">{epub_lead(html)}</p>'
    q, letter, rest = m.group(1), m.group(2), html[m.end():]
    return f'<p class="first"><span class="dropcap">{q}{letter}</span>{epub_lead(rest)}</p>'


def epub_head(filename, title, ch_type):
    pov = chapter_pov(filename)
    orn = '<p class="orn"><img src="images/fleuron.png" alt=""/></p>'
    if ch_type == "chapter":
        orn = orn.replace("fleuron.png", "crown.png")
        return (f'<div class="head">{orn}'
                f'<h1 class="num"><span class="chapter-label">Chapter</span> '
                f'<span class="chapter-number">{number_word(title)}</span></h1>'
                f'<p class="pov">{(pov or "").lower()}</p></div>')
    if ch_type == "interstitial":
        return (f'<div class="head">{orn}<p class="label">{title.split()[0].lower()} {title.split()[1]}</p>'
                f'<h1 class="title">Cassian</h1></div>')
    if ch_type == "prologue":
        return f'<div class="head">{orn}<h1 class="title">Prologue</h1></div>'
    if ch_type == "epilogue":
        return (f'<div class="head">{orn}<h1 class="title">Epilogue</h1>'
                f'<p class="label">we\u2019re not finished</p></div>')
    if ch_type == "bonus":
        return (f'<div class="head"><p class="label">bonus scene</p>{orn}'
                f'<h1 class="title">The Ghost That Stayed</h1>'
                f'<p class="sub">Chapter Eleven, from her side of the bed</p></div>')
    return (f'<div class="head"><p class="label">a first look at book two</p>{orn}'
            f'<h1 class="title">Vow of Poison</h1>'
            f'<p class="pov">chapter one \u00b7 {(pov or "").lower()}</p></div>')


def epub_body(filename, paragraphs=None):
    out, first, after_break = [], True, False
    for para in (split_paragraphs(read_manuscript(filename)) if paragraphs is None else paragraphs):
        if para == "{SCENE_BREAK}":
            out.append('<p class="scene"><img src="images/scene.png" alt="* * *"/></p>')
            after_break = True
            continue
        if para.startswith("{POV:"):
            out.append('<div class="pov-shift"><p class="orn"><img src="images/fleuron.png" alt=""/></p>'
                       f'<p class="pov">{x(para[5:-1]).lower()}</p></div>')
            first = True
            continue
        html = convert_inline(para).replace("\n", "<br/>")
        if first:
            out.append(epub_opener_p(html))
            first = after_break = False
        elif after_break:
            out.append(f'<p class="after-break">{epub_lead(html)}</p>')
            after_break = False
        else:
            out.append(f"<p>{html}</p>")
    return "\n".join(out)


def page(title, fname, body, css, lang="en", semantic="chapter"):
    it = epub.EpubHtml(title=title, file_name=fname, lang=lang)
    it.content = (f'<html xmlns="http://www.w3.org/1999/xhtml" '
                  f'xmlns:epub="http://www.idpf.org/2007/ops"><head><title>{x(title)}</title></head>'
                  f'<body><section class="book-section" id="start" epub:type="{semantic}">'
                  f'{body}</section></body></html>')
    it.add_item(css)
    return it


def matter_body(name, paras):
    if name == "Copyright":
        return '<div class="copyright">' + "".join(f"<p>{convert_inline(p)}</p>" for p in paras) + "</div>"
    if name == "Dedication":
        return '<div class="dedication">' + "".join(f"<p>{convert_inline(p)}</p>" for p in paras) + "</div>"
    parts = []
    for p in paras:
        lines = [l.strip() for l in p.split("\n") if l.strip()]
        if all(l.startswith("- ") for l in lines):
            parts.append("<ul>" + "".join(f"<li>{convert_inline(l[2:])}</li>" for l in lines) + "</ul>")
        elif name == "Playlist" or all(re.match(r"^\d+\.\s", l) for l in lines):
            parts.append('<div class="list">' + "".join(
                f"<p>{convert_inline(re.sub(r'^\d+\.\s*', '', l))}</p>" for l in lines) + "</div>")
        else:
            cls = ' class="c"' if name != "Before You Begin" else ""
            parts.append(f"<p{cls}>" + "<br/>".join(convert_inline(l) for l in lines) + "</p>")
    return ('<div class="head"><p class="orn"><img src="images/fleuron.png" alt=""/></p>'
            f'<h1 class="title">{x(name)}</h1></div><div class="matter">' + "".join(parts) + "</div>")


def build_epub(with_cover=False):
    label = "ARC (cover embedded)" if with_cover else "KDP"
    print(f"Building EPUB ({label})...")
    book = epub.EpubBook()
    book.set_identifier("king-of-teeth-blood-code-1" + ("-arc" if with_cover else ""))
    book.set_title(BOOK_TITLE)
    book.set_language("en")
    book.add_author(AUTHOR)
    book.add_metadata("DC", "description", DESCRIPTION)
    book.add_metadata("DC", "publisher", AUTHOR)
    book.add_metadata("DC", "date", PUB_DATE)
    book.add_metadata("DC", "rights", f"Copyright \u00a9 {PUB_DATE} {AUTHOR}. All rights reserved.")
    for subj in ("Fiction / Romance / Paranormal / Vampires", "Fiction / Romance / Dark"):
        book.add_metadata("DC", "subject", subj)
    book.add_metadata(None, "meta", SERIES, {"property": "belongs-to-collection", "id": "series"})
    book.add_metadata(None, "meta", "series", {"refines": "#series", "property": "collection-type"})
    book.add_metadata(None, "meta", str(SERIES_NO), {"refines": "#series", "property": "group-position"})
    book.add_metadata(None, "meta", "", {"name": "calibre:series", "content": SERIES})
    book.add_metadata(None, "meta", "", {"name": "calibre:series_index", "content": str(SERIES_NO)})

    # every character the book uses, for font subsetting
    fm = front_sections()
    alltext = BOOK_TITLE + AUTHOR + SERIES + "\u2019\u2018\u201c\u201d\u2014\u00b7*"
    alltext += "".join(" ".join(v) for v in fm.values())
    for fn, title, _ in CHAPTER_ORDER:
        alltext += title + smart_quotes(read_manuscript(fn))
    alltext += alltext.lower() + alltext.upper() + "0123456789"
    for fn in EPUB_FONT_FILES:
        book.add_item(epub.EpubItem(uid=fn, file_name=f"fonts/{fn}", media_type="font/ttf",
                                    content=subset_font(os.path.join(FONT_DIR, fn), alltext)))
    for name in ("fleuron", "scene", "crown"):
        book.add_item(epub.EpubItem(uid=name, file_name=f"images/{name}.png", media_type="image/png",
                                    content=ornament_png(name)))
    css = epub.EpubItem(uid="css", file_name="style/book.css", media_type="text/css",
                        content=epub_css().encode("utf-8"))
    book.add_item(css)

    if with_cover:
        with open(COVER_IMAGE, "rb") as f:
            book.set_cover("images/cover.jpg", f.read(), create_page=True)
        book.get_item_with_id("cover").is_linear = True   # reachable first page (EPUBCheck OPF-096)

    # the nav doc stays in the manifest for reader menus; readers see the styled Contents page instead
    spine, toc = (["cover"] if with_cover else []), []
    tp = page("Title Page", "title.xhtml",
              '<div class="titlepage"><p class="orn"><img src="images/crown.png" alt=""/></p>'
              '<p class="t-big">KING</p><p class="t-of">of</p><p class="t-big">TEETH</p>'
              '<p class="orn"><img src="images/fleuron.png" alt=""/></p>'
              f'<p class="t-series">the blood code \u00b7 book one</p>'
              f'<p class="t-author">{AUTHOR.upper()}</p></div>', css, semantic="titlepage")
    book.add_item(tp)
    spine.append(tp)
    for n, name in enumerate(FRONT_PAGES):
        semantic = {"Copyright": "copyright-page", "Dedication": "dedication"}.get(name, "preface")
        pg = page(name, f"front-{n}.xhtml", matter_body(name, fm[name]), css, semantic=semantic)
        book.add_item(pg)
        spine.append(pg)
        if name not in NO_TOC_PAGES:
            toc.append(pg)
    contents = page("Contents", "contents.xhtml", "", css)
    book.add_item(contents)
    spine.append(contents)

    start = None
    for filename, title, ch_type in CHAPTER_ORDER:
        if ch_type == "teaser":
            for k, name in enumerate(BACK_PAGES):
                pg = page(name, f"back-{k}.xhtml", matter_body(name, fm[name]), css, semantic="afterword")
                book.add_item(pg)
                spine.append(pg)
                toc.append(pg)
        pov = chapter_pov(filename)
        if ch_type == "chapter":
            toc_title = f"{title} \u00b7 {pov}"
        elif ch_type == "interstitial":
            toc_title = f"{title} \u00b7 Cassian"
        else:
            toc_title = title
        safe = filename.replace(".md", "").replace("00-", "")
        semantic = ch_type if ch_type in {"prologue", "epilogue"} else "chapter"
        # Separate spine documents are more dependable than CSS alone in Kindle
        # conversion. Each internal POV transition gets a fresh reading section.
        segments = [[]]
        for para in split_paragraphs(read_manuscript(filename)):
            if para.startswith("{POV:") and segments[-1]:
                segments.append([])
            segments[-1].append(para)
        ch = page(toc_title, f"{safe}.xhtml", epub_head(filename, title, ch_type) + epub_body(filename, segments[0]), css,
                  semantic=semantic)
        book.add_item(ch)
        spine.append(ch)
        toc.append(ch)
        for index, segment in enumerate(segments[1:], 2):
            pov_name = segment[0][5:-1]
            continuation = page(f"{title} · {pov_name} ({index})", f"{safe}-pov-{index}.xhtml",
                                epub_body(filename, segment), css, semantic=semantic)
            book.add_item(continuation)
            spine.append(continuation)
        if start is None:
            start = ch

    end = page("The End", "end.xhtml",
               '<div class="end"><p class="label">end of book one</p>'
               '<p class="orn"><img src="images/fleuron.png" alt=""/></p>'
               '<p class="sub">The Blood Code continues with Silas &amp; Ondine in</p>'
               '<p class="t-author" style="margin-top:0.8em">VOW OF POISON</p></div>', css, semantic="afterword")
    book.add_item(end)
    spine.append(end)

    links = []
    for it in toc:
        if it.title == "Before You Begin":
            continue
        title, separator, pov = it.title.partition(" · ")
        label = x(title)
        if separator:
            label += f' <span class="toc-pov">· {x(pov)}</span>'
        links.append(f'<p><a href="{it.file_name}#start">{label}</a></p>')
    links = "".join(links)
    contents.content = page("Contents", "contents.xhtml",
                        '<div class="head"><p class="orn"><img src="images/fleuron.png" alt=""/></p>'
                        f'<h1 class="title">Contents</h1></div><div class="contents">{links}</div>',
                        css, semantic="toc").content
    book.toc = toc
    book.spine = spine
    book.guide = [{"type": "toc", "title": "Contents", "href": contents.file_name},
                  {"type": "text", "title": "Start Reading", "href": start.file_name}]
    book.add_item(epub.EpubNcx())
    nav = epub.EpubNav()
    nav.add_item(css)
    book.add_item(nav)
    out = os.path.join(OUTPUT_DIR, "King_of_Teeth_ARC.epub" if with_cover else "King_of_Teeth.epub")
    epub.write_epub(out, book, {"epub3_landmark": True})
    print(f"  EPUB saved: {out}  ({os.path.getsize(out) / 1024:.0f} KB)")
    return out


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print(f"  Building: {BOOK_TITLE}  |  {AUTHOR}")
    print("=" * 60)
    epub_path = build_epub()
    arc_path = build_epub(with_cover=True) if os.path.exists(COVER_IMAGE) else None
    pdf_path = build_pdf()
    print()
    print("=" * 60)
    print("  BUILD COMPLETE")
    print(f"  EPUB: {epub_path}")
    if arc_path:
        print(f"  ARC:  {arc_path}")
    print(f"  PDF:  {pdf_path}")
    print("=" * 60)
