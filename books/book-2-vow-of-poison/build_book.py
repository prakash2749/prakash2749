"""
Build EPUB and PDF for Vow of Poison
Beautiful dark romance formatting with stylish drop caps
Uses: ebooklib (EPUB), reportlab (PDF) — no external C deps
"""

import os
import re
from ebooklib import epub

from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, FrameBreak,
    BaseDocTemplate, PageTemplate, Frame, NextPageTemplate, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from xml.sax.saxutils import escape

# === FONTS (embedded; KDP print requires every font embedded) ===
from reportlab.lib.fonts import addMapping
FONT_DIR = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont('Book', os.path.join(FONT_DIR, 'pala.ttf')))
pdfmetrics.registerFont(TTFont('Book-Bold', os.path.join(FONT_DIR, 'palab.ttf')))
pdfmetrics.registerFont(TTFont('Book-Italic', os.path.join(FONT_DIR, 'palai.ttf')))
pdfmetrics.registerFont(TTFont('Book-BoldItalic', os.path.join(FONT_DIR, 'palabi.ttf')))
pdfmetrics.registerFont(TTFont('Sym', os.path.join(FONT_DIR, 'seguisym.ttf')))
addMapping('Book', 0, 0, 'Book')
addMapping('Book', 1, 0, 'Book-Bold')
addMapping('Book', 0, 1, 'Book-Italic')
addMapping('Book', 1, 1, 'Book-BoldItalic')
# reportlab references Helvetica on every page by default; KDP flags any
# non-embedded font, so point the canvas default at the embedded one.
from reportlab import rl_config
rl_config.canvas_basefontname = 'Book'

# === CONFIG ===
MANUSCRIPT_DIR = r"d:\Vampire dark romance\books\book-2-vow-of-poison\manuscript"
OUTPUT_DIR = r"d:\Vampire dark romance\books\book-2-vow-of-poison"
BOOK_TITLE = "Vow of Poison"
BOOK_SUBTITLE = "The Blood Code \u2014 Book Two"
AUTHOR = "Aurelia Thorn"
TRIM_W = 6 * inch
TRIM_H = 9 * inch
DARK_RED = HexColor('#8b0000')
MEDIUM_GRAY = HexColor('#666666')
LIGHT_GRAY = HexColor('#999999')
BLACK = HexColor('#1a1a1a')
ORNAMENT = "\u2726"

# === CHAPTER ORDER ===
CHAPTER_ORDER = [
    ("ch-01.md", "Chapter One", "chapter"),
    ("ch-02.md", "Chapter Two", "chapter"),
    ("ch-03.md", "Chapter Three", "chapter"),
    ("ch-04.md", "Chapter Four", "chapter"),
    ("ch-05.md", "Chapter Five", "chapter"),
    ("I-1.md", "Interstitial: Cray", "interstitial"),
    ("ch-06.md", "Chapter Six", "chapter"),
    ("ch-07.md", "Chapter Seven", "chapter"),
    ("ch-08.md", "Chapter Eight", "chapter"),
    ("ch-09.md", "Chapter Nine", "chapter"),
    ("ch-10.md", "Chapter Ten", "chapter"),
    ("ch-11.md", "Chapter Eleven", "chapter"),
    ("I-2.md", "Interstitial: Cray", "interstitial"),
    ("ch-12.md", "Chapter Twelve", "chapter"),
    ("ch-13.md", "Chapter Thirteen", "chapter"),
    ("ch-14.md", "Chapter Fourteen", "chapter"),
    ("ch-15.md", "Chapter Fifteen", "chapter"),
    ("ch-16.md", "Chapter Sixteen", "chapter"),
    ("ch-17.md", "Chapter Seventeen", "chapter"),
    ("I-3.md", "Interstitial: Cray", "interstitial"),
    ("ch-18.md", "Chapter Eighteen", "chapter"),
    ("ch-19.md", "Chapter Nineteen", "chapter"),
    ("ch-20.md", "Chapter Twenty", "chapter"),
    ("ch-21.md", "Chapter Twenty-One", "chapter"),
    ("ch-22.md", "Chapter Twenty-Two", "chapter"),
    ("ch-23.md", "Chapter Twenty-Three", "chapter"),
    ("I-4.md", "Interstitial: Cray", "interstitial"),
    ("ch-24.md", "Chapter Twenty-Four", "chapter"),
    ("ch-25.md", "Chapter Twenty-Five", "chapter"),
    ("ch-26.md", "Chapter Twenty-Six", "chapter"),
    ("ch-27.md", "Chapter Twenty-Seven", "chapter"),
    ("ch-28.md", "Chapter Twenty-Eight", "chapter"),
    ("I-5.md", "Interstitial: Cray", "interstitial"),
    ("ch-29.md", "Chapter Twenty-Nine", "chapter"),
    ("ch-30.md", "Chapter Thirty", "chapter"),
    ("ch-31.md", "Chapter Thirty-One", "chapter"),
    ("ch-32.md", "Chapter Thirty-Two", "chapter"),
    ("ch-33.md", "Chapter Thirty-Three", "chapter"),
    ("ch-34.md", "Chapter Thirty-Four", "chapter"),
    ("epilogue.md", "Epilogue", "epilogue"),
    ("bonus-drink.md", "Bonus Scene: Drink", "bonus"),
    ("teaser-son-of-wolves.md", "Sneak Peek: Son of Wolves", "teaser"),
]

# ============================================================
# SHARED TEXT UTILITIES
# ============================================================

FRONT_MATTER_FILE = os.path.join(OUTPUT_DIR, "FRONT_MATTER.md")
FRONT_PAGES = ["Copyright", "Dedication", "Before You Begin", "Playlist", "The Blood Code"]
BACK_PAGES = ["Thank You"]
NO_TOC_PAGES = {"Copyright", "Dedication"}


def front_sections():
    """{section title: [paragraph, ...]} for the ## sections of FRONT_MATTER.md."""
    with open(FRONT_MATTER_FILE, 'r', encoding='utf-8') as f:
        text = f.read()
    out = {}
    for block in re.split(r'^## ', text, flags=re.MULTILINE)[1:]:
        title, _, body = block.partition('\n')
        body = body.split('\n---')[0]
        out[title.strip()] = [p.strip() for p in re.split(r'\n\s*\n', body.strip()) if p.strip()]
    return out


def read_manuscript(filename):
    filepath = os.path.join(MANUSCRIPT_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def clean_markdown(text):
    """Strip metadata headers, placement notes, etc."""
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    lines = text.split('\n')
    clean_lines = []
    in_header = True
    for line in lines:
        if in_header:
            if re.match(r'^#\s', line):
                continue
            if re.match(r'^\*?(Placement|POV|Word count|Heat|Chapter)', line, re.IGNORECASE):
                continue
            if line.strip() == '' and not clean_lines:
                continue
            if line.strip():
                in_header = False
        if not in_header:
            clean_lines.append(line)
    return '\n'.join(clean_lines).strip()


def split_paragraphs(text):
    """Split text into paragraph blocks, marking scene breaks and subheaders."""
    text = clean_markdown(text)
    text = re.sub(r'\n\s*[-*]{3,}\s*\n', '\n\n{SCENE_BREAK}\n\n', text)
    text = re.sub(r'^##\s+(.+)$', r'{SUBHEADER:\1}', text, flags=re.MULTILINE)
    paragraphs = re.split(r'\n\n+', text.strip())
    return [p.strip() for p in paragraphs if p.strip()]


def md_inline_to_html(text):
    """Convert inline markdown (*italic*, **bold**) to HTML tags."""
    text = escape(text)
    # Unescape our own tags first
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    # Re-escape properly but preserve markdown
    # Actually let's work with raw text and just handle markdown
    return text


def smart_quotes(text):
    """Straight quotes to typographic ones, deciding by both neighbors.

    A quote opens when what follows it is a word (or italics) and what
    precedes it is nothing, whitespace, a bracket, or a dash. Everything else
    closes. That keeps interrupted speech ("Wait—") closing properly.
    """
    out = []
    n = len(text)
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
        else:
            if prev.isalnum():
                out.append("\u2019")          # it's, Lucian's
            elif before_open and after_word:
                out.append("\u2018")
            else:
                out.append("\u2019")
    text = "".join(out)
    # elisions read as a closing quote: 'em, 'til, 'cause, '90s
    text = re.sub(r"\u2018(?=(?:em|til|cause|round|bout)\b|\d\ds?\b|n\u2019)", "\u2019", text,
                  flags=re.IGNORECASE)
    return text


def convert_inline(text):
    """Convert *italic* and **bold** to reportlab/html tags."""
    text = smart_quotes(text)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)
    # Convert em-dash
    text = text.replace(' -- ', ' \u2014 ')
    text = text.replace('--', '\u2014')
    return text


# ============================================================
# EPUB BUILD
# ============================================================

EPUB_CSS = """
body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 1.1em;
    line-height: 1.75;
    color: #1a1a1a;
    margin: 0;
    padding: 0 1.5em;
    text-align: justify;
    hyphens: auto;
    -webkit-hyphens: auto;
}
.title-page {
    text-align: center;
    padding-top: 30%;
    page-break-after: always;
}
.title-page h1 {
    font-size: 2.8em;
    font-weight: 900;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8b0000;
    margin-bottom: 0.2em;
    line-height: 1.1;
}
.title-page .subtitle {
    font-size: 1.05em;
    font-weight: 400;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #4a4a4a;
    margin-top: 0.5em;
}
.title-page .author {
    font-size: 1.3em;
    font-style: italic;
    color: #666;
    margin-top: 3em;
}
.title-page .ornament {
    font-size: 1.5em;
    color: #8b0000;
    margin: 1.5em 0;
    letter-spacing: 0.5em;
}
.chapter-header {
    text-align: center;
    margin-top: 18%;
    margin-bottom: 3em;
    page-break-before: always;
}
.chapter-header .chapter-label {
    font-size: 0.85em;
    font-weight: 400;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    color: #8b0000;
    margin-bottom: 0.3em;
    display: block;
}
.chapter-header h2 {
    font-size: 1.6em;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #1a1a1a;
    margin: 0.2em 0 0.5em;
    border: none;
}
.chapter-header .ornament {
    font-size: 1.2em;
    color: #8b0000;
    letter-spacing: 0.5em;
}
.interstitial-header {
    text-align: center;
    margin-top: 18%;
    margin-bottom: 3em;
    page-break-before: always;
}
.interstitial-header .chapter-label {
    font-size: 0.75em;
    font-weight: 400;
    letter-spacing: 0.5em;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 0.3em;
    display: block;
}
.interstitial-header h2 {
    font-size: 1.3em;
    font-weight: 400;
    font-style: italic;
    letter-spacing: 0.1em;
    color: #4a4a4a;
    margin: 0.2em 0 0.5em;
    border: none;
}
.interstitial-header .ornament {
    font-size: 1em;
    color: #999;
    letter-spacing: 0.5em;
}
.first-paragraph::first-letter {
    float: left;
    font-size: 3.6em;
    font-weight: 900;
    line-height: 1;
    padding-right: 0.08em;
    margin-top: 0.05em;
    color: #8b0000;
}
p {
    margin: 0;
    text-indent: 1.5em;
    widows: 2;
    orphans: 2;
}
.first-paragraph {
    text-indent: 0;
}
.scene-break {
    text-align: center;
    margin: 2em 0;
    font-size: 1.2em;
    color: #8b0000;
    letter-spacing: 0.5em;
}
em, i { font-style: italic; }
strong, b { font-weight: 700; }
h2 {
    font-size: 1.1em;
    text-align: center;
    color: #8b0000;
    letter-spacing: 0.2em;
    margin: 2em 0 1em;
    font-weight: 400;
}
.half-title {
    text-align: center;
    padding-top: 40%;
    page-break-after: always;
}
.half-title h1 {
    font-size: 2em;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #1a1a1a;
}
.copyright {
    font-size: 0.8em;
    text-align: left;
    padding-top: 20%;
    page-break-after: always;
}
.copyright p {
    text-indent: 0;
    margin: 0 0 0.8em 0;
}
.dedication {
    text-align: center;
    padding-top: 35%;
    font-style: italic;
    font-size: 1.1em;
    color: #666;
    page-break-after: always;
}
"""


def epub_chapter_html(filename, title, ch_type):
    text = read_manuscript(filename)
    paragraphs = split_paragraphs(text)

    if ch_type == "interstitial":
        header = '<div class="interstitial-header"><span class="chapter-label">Interstitial</span><h2>Cray</h2><div class="ornament">\u2014 \u2726 \u2014</div></div>'
    elif ch_type == "prologue":
        header = '<div class="chapter-header"><span class="chapter-label">Prologue</span><h2>Vow of Poison</h2><div class="ornament">\u2726 \u2726 \u2726</div></div>'
    elif ch_type == "epilogue":
        header = '<div class="chapter-header"><span class="chapter-label">Epilogue</span><h2>Morning, Keeper</h2><div class="ornament">\u2726 \u2726 \u2726</div></div>'
    elif ch_type == "bonus":
        header = '<div class="chapter-header"><span class="chapter-label">Bonus Scene — Chapter 23, His Side</span><h2>Drink</h2><div class="ornament">✦ ✦ ✦</div></div>'
    elif ch_type == "teaser":
        header = '<div class="chapter-header"><span class="chapter-label">Sneak Peek \u2014 The Blood Code, Book Three</span><h2>Son of Wolves</h2><div class="ornament">\u2726 \u2726 \u2726</div></div>'
    else:
        header = f'<div class="chapter-header"><span class="chapter-label">{title}</span><div class="ornament">\u2726</div></div>'

    parts = [header]
    is_first = True
    for para in paragraphs:
        if para == '{SCENE_BREAK}':
            parts.append('<div class="scene-break">\u2726 \u2726 \u2726</div>')
            is_first = True
            continue
        if para.startswith('{SUBHEADER:'):
            name = para.replace('{SUBHEADER:', '').rstrip('}')
            parts.append(f'<h2>{name}</h2>')
            is_first = True
            continue
        para_html = convert_inline(para).replace('\n', '<br/>')
        cls = ' class="first-paragraph"' if is_first else ''
        parts.append(f'<p{cls}>{para_html}</p>')
        if is_first:
            is_first = False

    return '\n'.join(parts)


def build_epub():
    print("Building EPUB...")
    book = epub.EpubBook()
    book.set_identifier('king-of-teeth-blood-code-1')
    book.set_title(BOOK_TITLE)
    book.set_language('en')
    book.add_author(AUTHOR)
    book.add_metadata('DC', 'description', 'A dark fantasy romance. Vampire-ruled New Orleans. Two registers of every sentence.')
    book.add_metadata('DC', 'subject', 'Dark Romance')
    book.add_metadata('DC', 'subject', 'Fantasy Romance')

    css_item = epub.EpubItem(uid="style", file_name="style/default.css",
                             media_type="text/css", content=EPUB_CSS.encode('utf-8'))
    book.add_item(css_item)

    spine = ['nav']
    toc = []

    # Title page
    tp = epub.EpubHtml(title='Title Page', file_name='title.xhtml', lang='en')
    tp.content = f'''<html><head><link rel="stylesheet" href="style/default.css"/></head><body>
<div class="title-page">
<div class="ornament">\u2726</div>
<h1>Vow<br/>of<br/>Poison</h1>
<div class="ornament">\u2014 \u2726 \u2014</div>
<p class="subtitle">The Blood Code \u2014 Book Two</p>
<p class="author">{AUTHOR}</p>
</div></body></html>'''
    tp.add_item(css_item)
    book.add_item(tp)
    spine.append(tp)

    # Front matter pages, from FRONT_MATTER.md
    fm = front_sections()

    def simple_page(name, paras, n):
        if name == "Copyright":
            inner = '<div class="copyright">' + ''.join(
                f'<p>{convert_inline(p)}</p>' for p in paras) + '</div>'
        elif name == "Dedication":
            inner = '<div class="dedication">' + ''.join(
                f'<p>{convert_inline(p)}</p>' for p in paras) + '</div>'
        else:
            items = []
            for p in paras:
                lines = [l.strip() for l in p.split('\n') if l.strip()]
                if all(l.startswith('- ') for l in lines):
                    items.append('<ul>' + ''.join(
                        f'<li>{convert_inline(l[2:])}</li>' for l in lines) + '</ul>')
                else:
                    items.append('<p>' + '<br/>'.join(convert_inline(l) for l in lines) + '</p>')
            inner = (f'<div class="chapter-header"><h2>{name}</h2>'
                     f'<div class="ornament">✦</div></div>' + ''.join(items))
        pg = epub.EpubHtml(title=name, file_name=f'page-{n}.xhtml', lang='en')
        pg.content = (f'<html><head><link rel="stylesheet" href="style/default.css"/>'
                      f'</head><body>{inner}</body></html>')
        pg.add_item(css_item)
        book.add_item(pg)
        spine.append(pg)
        if name not in NO_TOC_PAGES:
            toc.append(pg)

    for n, name in enumerate(FRONT_PAGES):
        simple_page(name, fm[name], n)

    # Half title
    ht = epub.EpubHtml(title='Half Title', file_name='halftitle.xhtml', lang='en')
    ht.content = '''<html><head><link rel="stylesheet" href="style/default.css"/></head><body>
<div class="half-title"><h1>Vow of Poison</h1></div></body></html>'''
    ht.add_item(css_item)
    book.add_item(ht)
    spine.append(ht)

    # Chapters
    i_count = 0
    for filename, title, ch_type in CHAPTER_ORDER:
        print(f"  EPUB: {filename}")
        if ch_type == "teaser":
            for k, name in enumerate(BACK_PAGES):
                simple_page(name, fm[name], 100 + k)
        if ch_type == "interstitial":
            i_count += 1
            safe = f"interstitial-{i_count}"
            toc_title = f"Cray ({i_count})"
        else:
            safe = filename.replace('.md', '')
            toc_title = title

        ch = epub.EpubHtml(title=toc_title, file_name=f'{safe}.xhtml', lang='en')
        body = epub_chapter_html(filename, title, ch_type)
        ch.content = f'<html><head><link rel="stylesheet" href="style/default.css"/></head><body>{body}</body></html>'
        ch.add_item(css_item)
        book.add_item(ch)
        toc.append(ch)
        spine.append(ch)

    # No cover inside the EPUB: KDP takes the cover as a separate upload,
    # and the cover comes from a designer, not from this script.

    book.toc = toc
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    out = os.path.join(OUTPUT_DIR, 'Vow_of_Poison.epub')
    epub.write_epub(out, book, {})
    print(f"  EPUB saved: {out}")
    return out


# ============================================================
# PDF BUILD (reportlab)
# ============================================================

class DropCapParagraph(Flowable):
    """A custom flowable that renders a drop cap aligned to the first text line."""

    CAP_LINES = 3

    def __init__(self, text, style, cap_size=36, cap_color=DARK_RED):
        Flowable.__init__(self)
        self.full_text = text
        self.style = style
        self.cap_size = cap_size
        self.cap_color = cap_color
        m = re.match(r'^(<[^>]+>)*(.)(.*)', text)
        if m:
            self.pre_tags = m.group(1) or ''
            self.cap_letter = m.group(2)
            self.rest_text = m.group(3)
        else:
            self.cap_letter = text[0] if text else ''
            self.rest_text = text[1:] if len(text) > 1 else ''
            self.pre_tags = ''

    def _cap_metrics(self):
        face = pdfmetrics.getFont('Book-Bold').face
        units_per_em = getattr(face, 'unitsPerEm', 1000)
        ascent_ratio = face.ascent / units_per_em
        cap_ascent = self.cap_size * ascent_ratio
        body_leading = self.style.leading
        body_ascent = self.style.fontSize * ascent_ratio
        drop_height = body_leading * self.CAP_LINES
        cap_w = pdfmetrics.stringWidth(self.cap_letter, 'Book-Bold', self.cap_size)
        return cap_w, cap_ascent, body_ascent, drop_height, body_leading

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        cap_w, cap_ascent, body_ascent, drop_height, body_leading = self._cap_metrics()
        self.cap_w = cap_w + 5

        rest_style = ParagraphStyle(
            'dropcap_rest',
            parent=self.style,
            firstLineIndent=0,
            leftIndent=self.cap_w,
            textColor=self.style.textColor,
        )
        rest_html = self.pre_tags + self.rest_text
        self.rest_para = Paragraph(rest_html, rest_style)
        rw, rh = self.rest_para.wrap(availWidth, availHeight)
        self.rest_h = rh

        # Size the box to the capital itself, not to three full lines, so a
        # one-line opener doesn't leave a hole under it.
        self.height = max(rh, cap_ascent + body_leading * 0.35)
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        cap_w, cap_ascent, body_ascent, drop_height, body_leading = self._cap_metrics()
        cap_baseline = self.height - cap_ascent
        canvas.saveState()
        canvas.setFillColor(self.cap_color)
        canvas.setFont('Book-Bold', self.cap_size)
        canvas.drawString(0, cap_baseline, self.cap_letter)
        canvas.restoreState()
        # Top-align the text beside the cap; short openers otherwise sank to
        # the bottom of the three-line box and left the capital stranded above.
        self.rest_para.drawOn(canvas, 0, self.height - self.rest_h)


class OrnamentFlowable(Flowable):
    """Centered ornament line."""
    def __init__(self, text="\u2726", color=DARK_RED, size=14):
        Flowable.__init__(self)
        self.text = text
        self.color = color
        self.size = size

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        self.height = self.size + 8
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(self.color)
        self.canv.setFont('Sym', self.size)
        tw = self.canv.stringWidth(self.text, 'Sym', self.size)
        self.canv.drawString((self.width - tw) / 2, 4, self.text)
        self.canv.restoreState()


class SceneBreak(Flowable):
    """Scene break ornament."""
    def __init__(self):
        Flowable.__init__(self)

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        self.height = 36
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(DARK_RED)
        self.canv.setFont('Sym', 10)
        text = "\u2726   \u2726   \u2726"
        tw = self.canv.stringWidth(text, 'Sym', 10)
        self.canv.drawString((self.width - tw) / 2, 14, text)
        self.canv.restoreState()


def make_styles():
    """Create all paragraph styles for the PDF."""
    s = {}

    s['body'] = ParagraphStyle(
        'body',
        fontName='Book',
        fontSize=10.5,
        leading=14.6,
        textColor=BLACK,
        alignment=TA_JUSTIFY,
        firstLineIndent=16,
        spaceBefore=0,
        spaceAfter=0,
    )

    s['body_first'] = ParagraphStyle(
        'body_first',
        parent=s['body'],
        firstLineIndent=0,
    )

    s['small'] = ParagraphStyle(
        'small',
        fontName='Book',
        fontSize=8.5,
        leading=12,
        textColor=BLACK,
        alignment=TA_LEFT,
        spaceAfter=6,
    )

    s['title_main'] = ParagraphStyle(
        'title_main',
        fontName='Book-Bold',
        fontSize=36,
        leading=40,
        textColor=DARK_RED,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=6,
    )

    s['title_subtitle'] = ParagraphStyle(
        'title_subtitle',
        fontName='Book',
        fontSize=12,
        leading=16,
        textColor=MEDIUM_GRAY,
        alignment=TA_CENTER,
        spaceBefore=12,
        spaceAfter=0,
    )

    s['title_author'] = ParagraphStyle(
        'title_author',
        fontName='Book-Italic',
        fontSize=14,
        leading=18,
        textColor=MEDIUM_GRAY,
        alignment=TA_CENTER,
        spaceBefore=36,
        spaceAfter=0,
    )

    s['dedication'] = ParagraphStyle(
        'dedication',
        fontName='Book-Italic',
        fontSize=12,
        leading=18,
        textColor=MEDIUM_GRAY,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=0,
    )

    s['half_title'] = ParagraphStyle(
        'half_title',
        fontName='Book-Bold',
        fontSize=24,
        leading=30,
        textColor=BLACK,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=0,
    )

    s['chapter_label'] = ParagraphStyle(
        'chapter_label',
        fontName='Book',
        fontSize=10,
        leading=14,
        textColor=DARK_RED,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=4,
    )

    s['chapter_title'] = ParagraphStyle(
        'chapter_title',
        fontName='Book-Bold',
        fontSize=18,
        leading=24,
        textColor=BLACK,
        alignment=TA_CENTER,
        spaceBefore=4,
        spaceAfter=8,
    )

    s['interstitial_label'] = ParagraphStyle(
        'interstitial_label',
        fontName='Book',
        fontSize=9,
        leading=13,
        textColor=MEDIUM_GRAY,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=4,
    )

    s['interstitial_title'] = ParagraphStyle(
        'interstitial_title',
        fontName='Book-Italic',
        fontSize=16,
        leading=22,
        textColor=MEDIUM_GRAY,
        alignment=TA_CENTER,
        spaceBefore=4,
        spaceAfter=8,
    )

    s['subheader'] = ParagraphStyle(
        'subheader',
        fontName='Book-Bold',
        fontSize=12,
        leading=16,
        textColor=DARK_RED,
        alignment=TA_CENTER,
        spaceBefore=24,
        spaceAfter=12,
    )

    s['end_page'] = ParagraphStyle(
        'end_page',
        fontName='Book-Bold',
        fontSize=13,
        leading=18,
        textColor=DARK_RED,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=0,
    )

    s['end_tease'] = ParagraphStyle(
        'end_tease',
        fontName='Book-Italic',
        fontSize=12,
        leading=18,
        textColor=MEDIUM_GRAY,
        alignment=TA_CENTER,
        spaceBefore=12,
        spaceAfter=0,
    )

    return s


def add_page_number(canvas, doc):
    """Footer: centered page number."""
    page_num = canvas.getPageNumber()
    if page_num > 3:  # Skip front matter
        canvas.saveState()
        canvas.setFont('Book', 9)
        canvas.setFillColor(LIGHT_GRAY)
        text = str(page_num)
        canvas.drawCentredString(TRIM_W / 2, 0.55 * inch, text)
        canvas.restoreState()


def no_page_number(canvas, doc):
    """No footer — for chapter openers and front matter."""
    pass


def build_pdf():
    print("Building PDF...")

    styles = make_styles()
    out = os.path.join(OUTPUT_DIR, 'Vow_of_Poison.pdf')

    doc = BaseDocTemplate(
        out,
        pagesize=(TRIM_W, TRIM_H),
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.8 * inch,
        title=BOOK_TITLE,
        author=AUTHOR,
    )

    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        id='normal'
    )

    # Two templates: one with page numbers, one without
    doc.addPageTemplates([
        PageTemplate(id='blank', frames=[frame], onPage=no_page_number),
        PageTemplate(id='normal', frames=[frame], onPage=add_page_number),
    ])

    story = []

    # --- TITLE PAGE ---
    story.append(NextPageTemplate('blank'))
    story.append(Spacer(1, 2.0 * inch))
    story.append(OrnamentFlowable("\u2726", DARK_RED, 16))
    story.append(Spacer(1, 18))
    story.append(Paragraph("KING", styles['title_main']))
    story.append(Paragraph("<i>of</i>", ParagraphStyle('of', parent=styles['title_subtitle'], fontSize=16, textColor=MEDIUM_GRAY)))
    story.append(Paragraph("TEETH", styles['title_main']))
    story.append(Spacer(1, 8))
    story.append(OrnamentFlowable("\u2014  \u2726  \u2014", DARK_RED, 12))
    story.append(Paragraph("THE BLOOD CODE \u2014 BOOK ONE", styles['title_subtitle']))
    story.append(Paragraph(AUTHOR, styles['title_author']))
    story.append(PageBreak())

    # --- FRONT MATTER (from FRONT_MATTER.md) ---
    fm = front_sections()

    def pdf_simple_page(name, paras):
        if name == "Copyright":
            story.append(Spacer(1, 2.4 * inch))
            for p in paras:
                story.append(Paragraph(convert_inline(p), styles['small']))
        elif name == "Dedication":
            story.append(Spacer(1, 2.3 * inch))
            for p in paras:
                story.append(Paragraph(convert_inline(p), styles['dedication']))
                story.append(Spacer(1, 6))
        else:
            story.append(Spacer(1, 0.6 * inch))
            story.append(Paragraph(name.upper(), styles['chapter_label']))
            story.append(OrnamentFlowable("✦", DARK_RED, 12))
            story.append(Spacer(1, 14))
            for p in paras:
                lines = [l.strip() for l in p.split('\n') if l.strip()]
                if all(l.startswith('- ') for l in lines):
                    for l in lines:
                        story.append(Paragraph('• ' + convert_inline(l[2:]), styles['body']))
                else:
                    style = styles['body'] if len(lines) == 1 else styles['body_first']
                    story.append(Paragraph('<br/>'.join(convert_inline(l) for l in lines), style))
                story.append(Spacer(1, 4))
        story.append(PageBreak())

    for name in FRONT_PAGES:
        pdf_simple_page(name, fm[name])

    # --- HALF TITLE ---
    story.append(Spacer(1, 2.8 * inch))
    story.append(Paragraph("KING OF TEETH", styles['half_title']))
    story.append(PageBreak())

    # Switch to normal pages
    story.append(NextPageTemplate('normal'))

    # --- CHAPTERS ---
    for filename, title, ch_type in CHAPTER_ORDER:
        print(f"  PDF: {filename}")
        if ch_type == "teaser":
            story.append(NextPageTemplate('blank'))
            story.append(PageBreak())
            for name in BACK_PAGES:
                pdf_simple_page(name, fm[name])
        text = read_manuscript(filename)
        paragraphs = split_paragraphs(text)

        # Chapter header (top of new page)
        story.append(NextPageTemplate('blank'))  # No page num on chapter opener
        story.append(PageBreak())
        story.append(Spacer(1, 1.8 * inch))

        if ch_type == "interstitial":
            story.append(Paragraph("INTERSTITIAL", styles['interstitial_label']))
            story.append(Paragraph("Cray", styles['interstitial_title']))
            story.append(OrnamentFlowable("\u2014 \u2726 \u2014", LIGHT_GRAY, 10))
        elif ch_type == "prologue":
            story.append(Paragraph("PROLOGUE", styles['chapter_label']))
            story.append(Paragraph("KING OF TEETH", styles['chapter_title']))
            story.append(OrnamentFlowable("\u2726  \u2726  \u2726", DARK_RED, 12))
        elif ch_type == "epilogue":
            story.append(Paragraph("EPILOGUE", styles['chapter_label']))
            story.append(Paragraph("MORNING, KEEPER", styles['chapter_title']))
            story.append(OrnamentFlowable("\u2726  \u2726  \u2726", DARK_RED, 12))
        elif ch_type == "bonus":
            story.append(Paragraph("BONUS SCENE — CHAPTER 23, HIS SIDE", styles['chapter_label']))
            story.append(Paragraph("DRINK", styles['chapter_title']))
            story.append(OrnamentFlowable("✦  ✦  ✦", DARK_RED, 12))
        elif ch_type == "teaser":
            story.append(Paragraph("SNEAK PEEK \u2014 THE BLOOD CODE, BOOK THREE", styles['chapter_label']))
            story.append(Paragraph("SON OF WOLVES", styles['chapter_title']))
            story.append(OrnamentFlowable("\u2726  \u2726  \u2726", DARK_RED, 12))
        else:
            story.append(Paragraph(title.upper(), styles['chapter_label']))
            story.append(OrnamentFlowable("\u2726", DARK_RED, 12))

        story.append(Spacer(1, 24))

        # Switch back to normal for body text
        story.append(NextPageTemplate('normal'))

        is_first = True
        for para in paragraphs:
            if para == '{SCENE_BREAK}':
                story.append(SceneBreak())
                is_first = True
                continue

            if para.startswith('{SUBHEADER:'):
                name = para.replace('{SUBHEADER:', '').rstrip('}')
                story.append(Paragraph(name, styles['subheader']))
                is_first = True
                continue

            para_html = convert_inline(para)
            # Replace literal newlines in a paragraph with spaces
            para_html = para_html.replace('\n', ' ')

            if is_first:
                # Drop cap for first paragraph after chapter header or scene break
                story.append(DropCapParagraph(para_html, styles['body_first'],
                                              cap_size=36, cap_color=DARK_RED))
                is_first = False
            else:
                story.append(Paragraph(para_html, styles['body']))

    # --- END PAGE ---
    story.append(NextPageTemplate('blank'))
    story.append(PageBreak())
    story.append(Spacer(1, 2.5 * inch))
    story.append(Paragraph("END OF BOOK ONE", styles['end_page']))
    story.append(Spacer(1, 12))
    story.append(OrnamentFlowable("\u2726  \u2726  \u2726", DARK_RED, 14))
    story.append(Spacer(1, 18))
    story.append(Paragraph("The Blood Code continues with Rémy &amp; Isabeau in", styles['end_tease']))
    story.append(Paragraph("<b>Book Three: Son of Wolves</b>",
                           ParagraphStyle('book2', parent=styles['end_page'], fontSize=14, textColor=BLACK)))

    doc.build(story)
    print(f"  PDF saved: {out}")
    return out


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print(f"  Building: {BOOK_TITLE}")
    print(f"  Author:   {AUTHOR}")
    print(f"  Source:    {MANUSCRIPT_DIR}")
    print("=" * 60)

    epub_path = build_epub()
    pdf_path = build_pdf()

    print()
    print("=" * 60)
    print("  BUILD COMPLETE")
    print(f"  EPUB: {epub_path}")
    print(f"  PDF:  {pdf_path}")
    print("=" * 60)
