from pathlib import Path
from playwright.sync_api import sync_playwright
import json
base=Path('tmp/pdfs/king-of-teeth').resolve(); epub=base/'epub/EPUB'
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(channel='msedge',headless=True)
 for mode,size,color in [('phone',18,'light'),('large',27,'light'),('dark',20,'dark'),('tablet',20,'light')]:
  viewport={'width':390 if mode!='tablet' else 768,'height':844 if mode!='tablet' else 1024}
  page=browser.new_page(viewport=viewport,color_scheme=color)
  for name in ['title','ch-01','ch-24','I-1','prologue','contents','bonus-ghost-that-stayed','teaser-vow-of-poison']:
   page.goto((epub/f'{name}.xhtml').as_uri())
   bg='#171717' if color=='dark' else '#fffdf8';fg='#e8e1d7' if color=='dark' else '#201d1b'
   page.add_style_tag(content=f'html{{background:{bg};color:{fg};}} body{{font-size:{size}px;padding:24px;max-width:620px;margin:auto;}}')
   page.evaluate('document.fonts.ready')
   report=page.evaluate('''() => ({width:innerWidth,scroll:document.documentElement.scrollWidth,heads:[...document.querySelectorAll('h1')].map(e=>({text:e.textContent,top:e.getBoundingClientRect().top,bottom:e.getBoundingClientRect().bottom})),fonts:document.fonts.status})''')
   report.update(mode=mode,section=name);results.append(report)
   if (mode=='phone' and name in ['title','ch-01','contents']) or (mode=='large' and name=='ch-24') or (mode=='dark' and name=='ch-01') or (mode=='tablet' and name=='prologue'):
    page.screenshot(path=str(base/f'epub-{mode}-{name}.png'))
  page.close()
 browser.close()
(base/'browser-checks.json').write_text(json.dumps(results,indent=2))
print('Layouts checked',len(results),'overflow',[(r['mode'],r['section'],r['scroll']) for r in results if r['scroll']>r['width']])
