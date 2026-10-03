from pathlib import Path
from lxml import etree
from playwright.sync_api import sync_playwright
import fitz,json,re
base=Path('tmp/pdfs/king-of-teeth').resolve(); epub=base/'epub/EPUB';ns={'h':'http://www.w3.org/1999/xhtml'}
names=['ch-01','ch-02','ch-24','I-1','epilogue','bonus-ghost-that-stayed','teaser-vow-of-poison']
sections=[]
for name in names:
 tree=etree.parse(str(epub/f'{name}.xhtml'))
 sec=tree.find('.//h:section',ns)
 # Keep real text, head, and first 12 paragraphs for a compact pagination proof.
 for el in list(sec)[13:]:sec.remove(el)
 sections.append(etree.tostring(sec,encoding='unicode'))
html='<html><head><meta charset="utf-8"/><link rel="stylesheet" href="style/book.css"/><style>body{font-size:18px;} @page{size:390px 700px;margin:24px;} .book-section{margin:0;}</style></head><body>'+''.join(sections)+'</body></html>'
proof=epub/'pagination-proof.html';proof.write_text(html,encoding='utf-8')
with sync_playwright() as p:
 browser=p.chromium.launch(channel='msedge',headless=True)
 page=browser.new_page();page.goto(proof.as_uri());page.evaluate('document.fonts.ready');page.pdf(path=str(base/'epub-pagination-proof.pdf'),prefer_css_page_size=True,print_background=True);browser.close()
d=fitz.open(base/'epub-pagination-proof.pdf');starts=[]
for i,p in enumerate(d):
 spans=[s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']]
 big=[s for s in spans if s['size']>28 and len(s['text'].strip())>2]
 if big:starts.append({'page':i+1,'heads':[s['text'] for s in big],'first_text':p.get_text().splitlines()[:3]})
print('Pagination proof',len(d),'pages',json.dumps(starts))
assert len(starts)==len(names),(len(starts),len(names))
for n in [1,4,7]:
 if n<=len(d):d[n-1].get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(base/f'epub-pagination-{n}.png')
