from pathlib import Path
import os,sys,json,tempfile
from playwright.sync_api import sync_playwright
Q=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Q))
from modul2.tag1.series import QUIZZES
BASE=os.environ.get('TODAY_TEST_URL','http://localhost:5387/hefte/').rstrip('/')+'/'
QA=Q/'build/modul2-tag1';QA.mkdir(exist_ok=True,parents=True)
report=dict(base=BASE,views=0,persistedRestarts=0,blockedStorage=0,corruptStorage=0,downloads=0,errors=[])
def key(person):return 'kurs:modul2:lektion1:'+person+':tag1:quiz:v2'
def url(person):return BASE+person+'/modul-2/tag-1/lernheft/'
def go(p,u):assert p.goto(u).status in (200,304);p.wait_for_load_state('networkidle')
def listen(p):p.on('pageerror',lambda e:report['errors'].append(str(e)))
with sync_playwright() as pw:
 for engine in ['webkit','chromium']:
  kw=dict(headless=True)
  if engine=='chromium':kw['executable_path']='C:/Program Files/Google/Chrome/Application/chrome.exe'
  with tempfile.TemporaryDirectory(prefix='make-today-',ignore_cleanup_errors=True) as data:
   ctx=getattr(pw,engine).launch_persistent_context(data,viewport=dict(width=1280,height=950),accept_downloads=True,reduced_motion='reduce',**kw)
   ctx.route('**/*.css*',lambda route:route.abort())
   p=ctx.new_page();listen(p)
   for person in ['carmen','ingo','tabea']:
    go(p,url(person));assert p.locator('h1').inner_text()=='Dein erster Ablauf in Make';assert not p.locator('#zusatz').get_attribute('open');assert 'Speicher bereit' in p.locator('#quiz-storage-status').inner_text()
    assert p.locator('.lesson-part').count()==3;assert p.locator('.do-steps').count()>=5
    p.locator('.today-nav a[href="#nachbauen"]').click();assert p.evaluate('location.hash')=='#nachbauen'
    assert p.locator('[data-key="wf1"]').is_visible()
    first=p.locator('[data-q="1"]');first.locator('[data-answer]').click();assert 'zuerst' in first.locator('.feedback').inner_text()
    first.locator('input[value="0"]').check();p.reload();assert first.locator('input[value="0"]').is_checked();assert first.locator('.feedback').is_hidden()
    first.locator('[data-answer]').click();assert 'Noch einmal' in first.locator('.feedback').inner_text();p.reload();assert 'Noch einmal' in first.locator('.feedback').inner_text()
    for n,(_,_,right,why) in enumerate(QUIZZES[1],1):
     f=p.locator(f'[data-q="{n}"]');f.locator(f'input[value="{right}"]').check();f.locator('[data-answer]').click();assert f.locator('.feedback').inner_text()=='Passt. '+why
    p.locator('#quiz-save').click();assert 'Gespeichert' in p.locator('#quiz-storage-status').inner_text();p.reload();assert 'wiederhergestellt' in p.locator('#quiz-storage-status').inner_text();assert '4 richtig' in p.locator('#quiz-progress').inner_text()
    with p.expect_download() as pending:p.locator('#quiz-download').click()
    path=QA/f'quiz-{engine}-{person}.txt';pending.value.save_as(path);out=path.read_text(encoding='utf8');assert person in out and out.count('Richtig.')==4;report['downloads']+=1
    p.locator('#credit-calculate').click();assert '10 Credits' in p.locator('#credit-result').inner_text()
    for width in [320,390,834,1280]:
     p.set_viewport_size(dict(width=width,height=950));assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(engine,person,width)
    if person=='carmen':
     p.goto(url(person));p.set_viewport_size(dict(width=1280,height=950));p.screenshot(path=str(QA/f'today-start-{engine}.png'))
     p.locator('#pruefen').scroll_into_view_if_needed();p.screenshot(path=str(QA/f'today-quiz-{engine}.png'))
     p.set_viewport_size(dict(width=390,height=950));p.locator('#nachbauen').scroll_into_view_if_needed();p.screenshot(path=str(QA/f'today-mobile-{engine}.png'))
     p.evaluate('document.body.style.fontSize="200%"');assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');p.evaluate('document.body.style.fontSize=""')
    report['views']+=1
   ctx.close()
   # Real browser restart with the same on-disk profile, not an injected storage snapshot.
   ctx=getattr(pw,engine).launch_persistent_context(data,viewport=dict(width=1280,height=950),**kw);p=ctx.new_page();listen(p);go(p,url('carmen'));assert 'wiederhergestellt' in p.locator('#quiz-storage-status').inner_text();assert '4 richtig' in p.locator('#quiz-progress').inner_text();report['persistedRestarts']+=1;ctx.close()
  b=getattr(pw,engine).launch(**kw)
  ctx=b.new_context(accept_downloads=True);ctx.add_init_script("Storage.prototype.getItem=function(){throw new Error('blocked')};Storage.prototype.setItem=function(){throw new Error('blocked')}");p=ctx.new_page();listen(p);go(p,url('carmen'));f=p.locator('[data-q="1"]');f.locator('input[value="1"]').check();f.locator('[data-answer]').click();assert 'Passt.' in f.locator('.feedback').inner_text();assert 'nicht' in p.locator('#quiz-storage-status').inner_text()
  with p.expect_download() as pending:p.locator('#quiz-download').click()
  path=QA/f'quiz-blocked-{engine}.txt';pending.value.save_as(path);assert 'Richtig.' in path.read_text(encoding='utf8');report['downloads']+=1;report['blockedStorage']+=1;ctx.close()
  for bad in ['{','null',json.dumps(dict(version=2,rows=[dict(answer=99,checked=True)]*4))]:
   ctx=b.new_context();ctx.add_init_script('(function(){try{localStorage.setItem('+json.dumps(key('carmen'))+','+json.dumps(bad)+')}catch(e){}})()');p=ctx.new_page();listen(p);go(p,url('carmen'));assert p.locator('[data-q="1"] input:checked').count()==0;assert 'nicht geladen' in p.locator('#quiz-storage-status').inner_text();report['corruptStorage']+=1;ctx.close()
  b.close()
assert not report['errors'],report
(QA/('today-live.json' if BASE.startswith('https:') else 'today-local.json')).write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report))
