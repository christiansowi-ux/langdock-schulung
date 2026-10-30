from pathlib import Path
import sys,json,hashlib
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];Q=ROOT/'_quellen';sys.path.insert(0,str(Q))
from tag19.content import PAGES,SOURCE_FILE,PDF,BONUS_PDF
from tag19.bonus_content import PAGES as BONUS,PROMPTS
from tag19.build import pages
PUB=ROOT/'plattform/public';QA=Q/'build/tag19';report=dict(pages=0,links=0,copies=0,errors=[],profiles=[])
assert len(PAGES)==20 and sum(p['part']=='make' for p in PAGES)==10
assert len(PROMPTS)==20 and len([p for p in BONUS if p['key'].startswith('fall-')])==5
for p in PAGES[10:]:
 assert not any(k in ('prompt','code','check','quiz','mission') for k,v in p['blocks']),p['key']
assert hashlib.sha256((Path.home()/'Downloads'/SOURCE_FILE).read_bytes()).digest()==hashlib.sha256((PUB/'folien/tag-19/Folien_Tag19.pdf').read_bytes()).digest()
for person in ('ingo','carmen','tabea'):
 for suffix in ('','lernheft/','bonus/'):
  path=PUB/person/'tag-19'/suffix/'index.html';soup=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser');ids=[e['id'] for e in soup.select('[id]')];assert len(ids)==len(set(ids))
  for e in soup.select('a[href],script[src],link[href],img[src]'):
   u=urlsplit(e.get('href') or e.get('src'))
   if u.scheme or u.netloc:continue
   target=PUB/unquote(u.path[7:]) if u.path.startswith('/hefte/') else path.parent/unquote(u.path) if u.path else path
   if target.is_dir():target=target/'index.html'
   assert target.exists(),(path,str(target))
   if u.fragment and target.suffix=='.html':assert BeautifulSoup(target.read_text(encoding='utf8'),'html.parser').find(id=u.fragment),(path,u.fragment)
   report['links']+=1
  report['pages']+=1
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe')
 for person in ('ingo','carmen','tabea'):
  ctx=browser.new_context(permissions=['clipboard-read','clipboard-write'],viewport={'width':1280,'height':950},reduced_motion='reduce');p=ctx.new_page()
  p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
  url=f'http://localhost:5387/hefte/{person}/tag-19/'
  assert p.goto(url).status==200;assert p.locator('details.original').count()==20
  assert p.locator('[data-quiz],.lab,[data-answer]').count()==0
  p.locator('#folie-13 summary').click();assert p.locator('#folie-13 img').is_visible()
  for suffix,expected in [('lernheft/',len(pages())),('bonus/',len(BONUS))]:
   assert p.goto(url+suffix).status==200;p.wait_for_load_state('networkidle');assert p.locator('section.chapter').count()==expected
   if suffix=='lernheft/':
    assert p.locator('[data-part="design"]').count()==p.locator('[data-part="make"]').count()==10
    assert p.locator('[data-part="make"] button,[data-part="make"] input,[data-part="make"] textarea,[data-part="make"] [data-copy]').count()==0
   for button in p.locator('[data-copy]').all():
    ident=button.get_attribute('data-copy');expectedtext=p.locator('#'+ident).text_content();button.click();p.wait_for_function("id => document.getElementById(id).parentElement.querySelector('.copystatus').textContent.startsWith('Kopiert.')",arg=ident)
    assert p.evaluate('navigator.clipboard.readText()').replace('\r\n','\n')==expectedtext.replace('\r\n','\n');report['copies']+=1
   for width in (320,390,1280):
    p.set_viewport_size({'width':width,'height':950});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(person,suffix,width)
   if person=='tabea':p.screenshot(path=str(QA/('bonus-web.png' if suffix=='bonus/' else 'friday-web.png')))
  report['profiles'].append(person);ctx.close()
 # Denied clipboard uses an honest manual-copy path.
 ctx=browser.new_context();ctx.add_init_script("Object.defineProperty(navigator,'clipboard',{value:{writeText:async()=>{throw new Error('denied')}}})");p=ctx.new_page();p.goto('http://localhost:5387/hefte/ingo/tag-19/bonus/');b=p.locator('[data-copy]').first;b.click();p.wait_for_function("document.querySelector('.copystatus').textContent.includes('manuell')");ctx.close();browser.close()
assert not report['errors'],report['errors']
(QA/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False))
