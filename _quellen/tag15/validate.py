from pathlib import Path
import sys,json,hashlib
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'_quellen'))
from tag15.content import QUIZ,PAGES,SLIDES
PUB=ROOT/'plattform/public';QA=ROOT/'_quellen/build/tag15'
report={'profiles':[],'errors':[],'local_links':0}
for pid in ('ingo','carmen','tabea'):
 for suffix in ('','lernheft/'):
  path=PUB/pid/'tag-15'/suffix/'index.html'
  soup=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser')
  ids=[n['id'] for n in soup.select('[id]')];assert len(ids)==len(set(ids)),(path,'duplicate id')
  if suffix:assert len(soup.select('.chapter[data-key]'))==41
  else:assert len(soup.select('[id^="einfach-"]'))==28
  for node in soup.select('a[href],img[src],script[src],link[href]'):
   if any('display:none' in parent.get('style','').replace(' ','') for parent in node.parents):continue
   url=node.get('href') or node.get('src');p=urlsplit(url)
   if p.scheme or p.netloc:continue
   if p.path.startswith('/hefte/'):
    target=PUB/unquote(p.path[len('/hefte/'):]);target=target/'index.html' if target.is_dir() else target
   elif p.path:
    target=path.parent/unquote(p.path);target=target/'index.html' if target.is_dir() else target
   else:target=path
   assert target.exists(),(path,url,target)
   if p.fragment and target.suffix=='.html':
    other=soup if target==path else BeautifulSoup(target.read_text(encoding='utf8'),'html.parser')
    assert other.find(id=p.fragment),(path,url,'missing anchor')
   report['local_links']+=1
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe')
 for pid in ('ingo','carmen','tabea'):
  ctx=browser.new_context(permissions=['clipboard-read','clipboard-write'],accept_downloads=True,reduced_motion='reduce')
  p=ctx.new_page();p.on('pageerror',lambda e:report['errors'].append(str(e)))
  p.on('console',lambda msg:report['errors'].append(msg.text) if msg.type=='error' else None)
  url=f'http://localhost:5387/hefte/{pid}/tag-15/lernheft/'
  assert p.goto(url).status==200;p.wait_for_load_state('networkidle')
  assert p.locator('.chapter[data-key]').count()==41
  for n,(_,opts,right,why) in enumerate(QUIZ,1):
   field=p.locator(f'[data-quiz="{n}"]')
   field.locator('[data-answer]').click();assert 'Wähle erst' in field.locator('.feedback').inner_text()
   field.locator(f'input[value="{(right+1)%3}"]').check();field.locator('[data-answer]').click();assert 'Noch einmal' in field.locator('.feedback').inner_text()
   field.locator(f'input[value="{right}"]').check();field.locator('[data-answer]').click();assert field.locator('.feedback').inner_text()=='Passt. '+why
  # Every copyable prompt, not only the currently visible mission.
  count=p.locator('[data-copy]').count()
  for button in p.locator('[data-copy]').all():
   target=button.get_attribute('data-copy');expected=p.locator('#'+target).text_content();button.click()
   assert p.evaluate('navigator.clipboard.readText()')==expected and len(expected)>80
  memo=f'Nur {pid}: Ein Skill ist kein Datenzugang.'
  p.locator('#memo').fill(memo);p.locator('#save-note').click();p.reload();assert p.locator('#memo').input_value()==memo
  with p.expect_download() as pending:p.locator('#download-note').click()
  download=pending.value;dest=QA/f'note-{pid}.txt';download.save_as(dest);assert memo in dest.read_text(encoding='utf8')
  widths=[]
  for w in (320,390,1280):
   p.set_viewport_size({'width':w,'height':900});p.reload();p.wait_for_load_state('networkidle')
   assert p.evaluate('document.documentElement.scrollWidth <= innerWidth'),(pid,w,'overflow')
   widths.append(w)
  p.set_viewport_size({'width':1280,'height':1000});p.goto(url+'#k17');p.wait_for_load_state('networkidle');p.screenshot(path=str(QA/f'web-{pid}.png'))
  p.goto(f'http://localhost:5387/hefte/{pid}/tag-15/#einfach');p.wait_for_load_state('networkidle')
  assert p.locator('#einfach').is_visible()
  assert p.locator('#einfach [id^="einfach-"]').count()==28
  p.goto(f'http://localhost:5387/hefte/{pid}/');p.wait_for_load_state('networkidle');assert p.locator('a[href$="/tag-15/"]').count()>=1
  report['profiles'].append({'id':pid,'quiz_cases':24,'prompts':count,'widths':widths,'note_download':True})
  ctx.close()
 # Shared origin storage must remain separated by profile; blocked storage fallback.
 ctx=browser.new_context();p=ctx.new_page();p.goto('http://localhost:5387/hefte/ingo/tag-15/lernheft/')
 p.locator('#memo').fill('Ingos private Übungsnotiz');p.locator('#save-note').click()
 p.goto('http://localhost:5387/hefte/tabea/tag-15/lernheft/');assert p.locator('#memo').input_value()==''
 ctx.close()
 ctx=browser.new_context();ctx.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('disabled')}})")
 p=ctx.new_page();p.goto('http://localhost:5387/hefte/ingo/tag-15/lernheft/');p.locator('#memo').fill('Temporär');p.locator('#save-note').click();assert 'Nicht gespeichert' in p.locator('#note-status').inner_text();ctx.close()
 browser.close()
assert not report['errors'],report['errors']
original=Path.home()/'Downloads/Einfuhrung-Claude.pdf'
assert hashlib.sha256(original.read_bytes()).digest()==hashlib.sha256((PUB/'folien/tag-15/Folien_Tag15.pdf').read_bytes()).digest()
(QA/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
