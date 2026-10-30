from pathlib import Path
import sys,json,hashlib,zipfile,re,urllib.request
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];Q=ROOT/'_quellen';PUB=ROOT/'plattform/public';QA=Q/'build/modul2-tag1';sys.path.insert(0,str(Q))
from modul2.tag1.series import BOOKS,QUIZZES
from modul2.tag1.build import pages

def main():
 report=dict(pages=0,links=0,copies=0,quizPaths=0,jsonCases=0,profiles=[],errors=[])
 assert sorted(n for b in BOOKS.values() for n in b['slides'])==list(range(1,35))
 assert sorted(n for b in BOOKS.values() for n in b['ideas'])==list(range(1,31))
 source=next((Path.home()/'Downloads').glob('KIAutomSpez_2_01*.pdf'))
 assert hashlib.sha256(source.read_bytes()).digest()==hashlib.sha256((PUB/'folien/tag-20/Folien_Modul2_Tag1.pdf').read_bytes()).digest()
 for day,b in BOOKS.items():
  assert [p['key'] for p in pages(day) if re.fullmatch(r'wf[1-4]',p['key'])]==['wf'+str(day)]
  with zipfile.ZipFile(PUB/f'material/modul2-tag1/Make-Tag{day}-Starterpaket.zip') as z:
   names=z.namelist();assert all(n.startswith(f'Make-Tag{day}-Starterpaket/') for n in names)
   if day==1:assert not any(n.endswith('.json') for n in names)
   if day==2:assert any(n.endswith('Redaktionsbriefing.json') for n in names)
   if day==3:assert any(n.endswith('Video-Freigabe.json') for n in names)
   if day==4:assert any(n.endswith('Test-API.txt') for n in names)
  data=urllib.request.urlopen('http://localhost:5387/hefte/pdf/'+b['pdf']).read();assert hashlib.sha256(data).digest()==hashlib.sha256((PUB/'pdf'/b['pdf']).read_bytes()).digest()
 for person in ['ingo','carmen','tabea']:
  paths=[PUB/person/'index.html']+[PUB/person/rel/'index.html' for d in BOOKS for rel in [f'modul-2/tag-{d}',f'modul-2/tag-{d}/lernheft',f'tag-{19+d}',f'tag-{19+d}/lernheft']]
  for path in paths:
   soup=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser');ids=[e['id'] for e in soup.select('[id]')];assert len(ids)==len(set(ids)),path
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
  for person in ['ingo','carmen','tabea']:
   ctx=browser.new_context(permissions=['clipboard-read','clipboard-write'],accept_downloads=True,viewport={'width':1280,'height':950},reduced_motion='reduce');p=ctx.new_page()
   p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
   base=f'http://localhost:5387/hefte/{person}/';p.goto(base);p.wait_for_load_state('networkidle');assert p.locator('#modul-1 .station').count()==19;assert p.locator('#modul-2 .station').count()==4
   assert p.locator('#modul-2 .st-dot').all_text_contents()==['1','2','3','4']
   if person=='tabea':p.locator('#modul-2').scroll_into_view_if_needed();p.screenshot(path=str(QA/'series-overview.png'))
   for day,b in BOOKS.items():
    url=base+f'modul-2/tag-{day}/';assert p.goto(url).status==200;p.wait_for_load_state('networkidle');assert p.locator('details.original').count()==len(b['slides'])
    ids=[int(x.get_attribute('id').split('-')[1]) for x in p.locator('details.original').all()];assert ids==b['slides']
    assert p.goto(url+'lernheft/').status==200;p.wait_for_load_state('networkidle');assert p.locator('.chapter[data-key]').count()==len(pages(day))
    assert p.locator('.idea-data').count()==len(b['ideas']);assert [int(x.get_attribute('data-idea')) for x in p.locator('.idea-data').all()]==b['ideas']
    assert p.locator('#credit-lab').count()==(1 if day==1 else 0);assert p.locator('#json-lab').count()==(1 if day==3 else 0)
    for button in p.locator('[data-copy]').all():
     ident=button.get_attribute('data-copy');expected=p.locator('#'+ident).text_content();button.click();p.wait_for_function("id=>document.getElementById(id).parentElement.querySelector('.copystatus').textContent.startsWith('Kopiert.')",arg=ident)
     assert p.evaluate('navigator.clipboard.readText()').replace('\r\n','\n')==expected.replace('\r\n','\n');report['copies']+=1
    for i,(q,opts,right,why) in enumerate(QUIZZES[day],1):
     f=p.locator(f'[data-q="{i}"]');f.locator('[data-answer]').click();assert 'zuerst' in f.locator('.feedback').inner_text()
     f.locator(f'input[value="{(right+1)%3}"]').check();f.locator('[data-answer]').click();assert 'Noch einmal' in f.locator('.feedback').inner_text()
     f.locator(f'input[value="{right}"]').check();f.locator('[data-answer]').click();assert f.locator('.feedback').inner_text()=='Passt. '+why;report['quizPaths']+=3
    if day==1:
     p.locator('#credit-calculate').click();assert '10 Credits' in p.locator('#credit-result').inner_text();p.locator('#polling-example').click();assert '2.880' in p.locator('#polling-result').inner_text()
    if day==3:
     for value,expected in [('{"projekt":"N","kategorie":"VIDEO","freigabe":true}','würde passieren'),('{"projekt":"N","kategorie":"VIDEO","freigabe":false}','würde stoppen'),('{"projekt":"N","kategorie":"VIDEO","freigabe":"true"}','Felder prüfen'),('null','einzelnes Objekt'),('{','Kein gültiges')]:
      p.locator('#json-input').fill(value);p.locator('#json-check').click();assert expected in p.locator('#json-result').inner_text();report['jsonCases']+=1
    assert p.locator('#memo').input_value()==''
    memo=f'{person}: Tag {day}, beobachteter eigener Test.';p.locator('#memo').fill(memo);p.locator('#save-note').click();p.reload();assert p.locator('#memo').input_value()==memo
    with p.expect_download() as pending:p.locator('#download-note').click()
    output=QA/f'note-series-{person}-{day}.txt';pending.value.save_as(output);assert memo in output.read_text(encoding='utf8') and f'Tag {day}' in output.read_text(encoding='utf8')
    for width in [320,390,1280]:
     p.set_viewport_size({'width':width,'height':950});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(person,day,width)
    if person=='tabea':p.locator(f'[data-key="{b["workflow"]}"]').scroll_into_view_if_needed();p.screenshot(path=str(QA/f'series-day-{day}.png'))
    report['profiles'].append(dict(person=person,day=day))
   # Earlier notes must still be present after visiting all four days.
   p.goto(base+'modul-2/tag-1/lernheft/');assert p.locator('#memo').input_value()==f'{person}: Tag 1, beobachteter eigener Test.';ctx.close()
  browser.close()
 assert not report['errors'],report['errors']
 (QA/'series-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
