from pathlib import Path
import sys,json,hashlib,csv,io,itertools
from decimal import Decimal
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];Q=ROOT/'_quellen';sys.path.insert(0,str(Q))
from reihe1618.content import BOOKS,QUIZ,SLIDES,course
from lerntraining import cards
PUB=ROOT/'plattform/public';QA=Q/'build/reihe1618';report=dict(pages=0,links=0,profiles=[],errors=[])
original=Path.home()/'Downloads/KIAutomSpez_1_15_Claude_Cowork.pdf';original_hash=hashlib.sha256(original.read_bytes()).hexdigest()
assert sorted(n for b in BOOKS.values() for n in b['slides'])==list(range(1,28))
for day,b in BOOKS.items():
 assert hashlib.sha256((PUB/f'folien/tag-{day}/Folien_Tag{day}.pdf').read_bytes()).hexdigest()==original_hash
 deck=cards({day:course(day)},day);assert len({c['id'] for c in deck})==len(deck)
 for person in ('ingo','carmen','tabea'):
  for suffix in ('','lernheft/'):
   path=PUB/person/f'tag-{day}'/suffix/'index.html';soup=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser')
   ids=[x['id'] for x in soup.select('[id]')];assert len(ids)==len(set(ids)),path
   if suffix:assert len(soup.select('.chapter[data-key]'))==len(b['pages'])
   else:assert len(soup.select('#einfach .simple-slide'))==len(b['slides'])
   for node in soup.select('a[href],img[src],script[src],link[href]'):
    if any('display:none' in x.get('style','').replace(' ','') for x in node.parents):continue
    url=node.get('href') or node.get('src');u=urlsplit(url)
    if u.scheme or u.netloc:continue
    if u.path.startswith('/hefte/'):target=PUB/unquote(u.path[7:])
    elif u.path:target=path.parent/unquote(u.path)
    else:target=path
    if target.is_dir():target=target/'index.html'
    assert target.exists(),(path,url,target)
    if u.fragment and target.suffix=='.html':
     other=soup if target==path else BeautifulSoup(target.read_text(encoding='utf8'),'html.parser');assert other.find(id=u.fragment),(path,url)
    report['links']+=1
   report['pages']+=1
# Independent arithmetic check against the published teaching reference.
base=PUB/'material/reihe16-18/Nordlicht-Werkstatt';amounts={};seen={};missing=[]
for row in csv.DictReader(io.StringIO((base/'01_eingang/umsatz_regionen.csv').read_text(encoding='utf8')),delimiter=';'):
 identifier=row['beleg_id']
 if identifier in seen:assert seen[identifier]==row;continue
 seen[identifier]=row
 region=row['region'].strip().capitalize()
 if not row['umsatz_eur']:missing.append(region);continue
 amounts[region]=amounts.get(region,Decimal(0))+Decimal(row['umsatz_eur'].replace(',','.'))
assert amounts=={'Nord':120000,'Süd':80000,'Ost':105000,'West':100000} and missing==['Süd']
assert sum(amounts.values())==405000
refs=list(csv.DictReader(io.StringIO((base/'02_referenz/erwartete_kennzahlen.csv').read_text(encoding='utf8')),delimiter=';'))
for r in refs:
 assert Decimal(r['bekanntes_ist'])==amounts[r['region']]
 assert Decimal(r['plan_delta'])==Decimal(r['bekanntes_ist'])-Decimal(r['plan'])
 assert Decimal(r['vorjahr_delta'])==Decimal(r['bekanntes_ist'])-Decimal(r['vorjahr'])
 if Decimal(r['vorjahr'])==0:assert r['vorjahr_delta_prozent']=='nicht definiert'
for r in csv.DictReader(io.StringIO((base/'04_neuer_fall/daten_neu.csv').read_text(encoding='utf8')),delimiter=';'):
 if r['region']=='Nord':assert (Decimal(r['ist_eur'])-Decimal(r['plan_eur']))/Decimal(r['plan_eur'])==Decimal('-.1')
 if r['region']=='Neu':assert r['plan_eur']==r['vorjahr_eur']=='0'
report['arithmetic']=True
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe')
 for day,b in BOOKS.items():
  for person in ('ingo','carmen','tabea'):
   ctx=browser.new_context(permissions=['clipboard-read','clipboard-write'],accept_downloads=True,reduced_motion='reduce',viewport={'width':1280,'height':950})
   p=ctx.new_page();p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
   url=f'http://localhost:5387/hefte/{person}/tag-{day}/'
   assert p.goto(url+'lernheft/').status==200;p.wait_for_load_state('networkidle')
   assert p.locator('.chapter[data-key]').count()==len(b['pages'])
   # The branch prompt must be the correct per-person variant.
   chapter=next(x for x in b['pages'] if x['key']=='branchen');variants=next(v for k,v in chapter['blocks'] if k=='mission')
   assert variants[person] in p.locator('[data-key="branchen"]').inner_text()
   for other in ('ingo','carmen','tabea'):
    if other!=person:assert variants[other] not in p.locator('[data-key="branchen"]').inner_text()
   for i,(q,opts,right,why) in enumerate(QUIZ[day],1):
    f=p.locator(f'[data-q="{i}"]');f.locator('[data-answer]').click();assert 'zuerst' in f.locator('.feedback').inner_text()
    f.locator(f'input[value="{(right+1)%3}"]').check();f.locator('[data-answer]').click();assert 'Noch einmal' in f.locator('.feedback').inner_text()
    f.locator(f'input[value="{right}"]').check();f.locator('[data-answer]').click();assert f.locator('.feedback').inner_text()=='Passt. '+why
   copies=p.locator('[data-copy]').count()
   for button in p.locator('[data-copy]').all():
    text=p.locator('#'+button.get_attribute('data-copy')).text_content();button.click()
    p.wait_for_function("id => document.getElementById(id).parentElement.querySelector('.copystatus').textContent.startsWith('Kopiert.')",arg=button.get_attribute('data-copy'))
    assert p.evaluate('navigator.clipboard.readText()').replace('\r\n','\n')==text.replace('\r\n','\n'),(day,person,button.get_attribute('data-copy'),'copy mismatch')
    assert len(text)>20,(day,person,button.get_attribute('data-copy'),len(text))
   # All eight states in the explicitly simulated exercise.
   lab=p.locator('.lab')
   for flags in itertools.product([False,True],repeat=3):
    for index,on in enumerate(flags):lab.locator(f'[data-signal="{index}"]').set_checked(on)
    lab.locator('[data-lab-check]').click();feedback=lab.locator('.lab-result').inner_text()
    assert ('Alle drei' in feedback)==all(flags)
    if all(flags):assert 'kein Beleg' in feedback
   memo=f'{person}-t{day}: Quelle und Prüfung vor Tempo.';p.locator('#memo').fill(memo);p.locator('#save-note').click();p.reload();assert p.locator('#memo').input_value()==memo
   with p.expect_download() as pending:p.locator('#download-note').click()
   target=QA/f'note-{person}-{day}.txt';pending.value.save_as(target);assert memo in target.read_text(encoding='utf8')
   for width in (320,390,1280):
    p.set_viewport_size({'width':width,'height':900});p.reload();p.wait_for_load_state('networkidle');assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(day,person,width)
   p.locator('[data-key="branchen"]').scroll_into_view_if_needed();p.screenshot(path=str(QA/f'web-{person}-{day}.png'))
   p.goto(url+'#einfach');p.wait_for_load_state('networkidle');assert p.locator('#einfach').is_visible();assert p.locator('#einfach .simple-slide').count()==len(b['slides'])
   p.goto(url+'#learnings');p.wait_for_load_state('networkidle');button=p.locator('.lc-sitzt').first;button.click();assert button.get_attribute('aria-pressed')=='true'
   report['profiles'].append(dict(day=day,person=person,quiz_paths=18,copied=copies,simulation_states=8,widths=[320,390,1280],note=True))
   ctx.close()
 # Day and person scopes must not leak notes across a shared browser.
 ctx=browser.new_context();p=ctx.new_page();p.goto('http://localhost:5387/hefte/ingo/tag-16/lernheft/');p.locator('#memo').fill('Ingo nur Dienstag');p.locator('#save-note').click()
 for person,day in [('carmen',16),('ingo',17)]:
  p.goto(f'http://localhost:5387/hefte/{person}/tag-{day}/lernheft/');assert p.locator('#memo').input_value()==''
 ctx.close()
 ctx=browser.new_context();ctx.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('disabled')}})");p=ctx.new_page();p.goto('http://localhost:5387/hefte/tabea/tag-18/lernheft/');p.locator('#memo').fill('Temporär');p.locator('#save-note').click();assert 'Nicht gespeichert' in p.locator('#note-status').inner_text();ctx.close();browser.close()
assert not report['errors'],report['errors']
(QA/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
