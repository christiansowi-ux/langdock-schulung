"""Regression: the reading layout survives blocked external CSS in WebKit/Chrome."""
from pathlib import Path
import os,json,sys,tarfile
from playwright.sync_api import sync_playwright
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from modul2.tag1.series import BOOKS,QUIZZES
BASE=os.environ.get('LAYOUT_TEST_URL','http://localhost:5387/hefte/').rstrip('/')+'/'
QA=Path(__file__).resolve().parents[2]/'build/modul2-tag1';QA.mkdir(parents=True,exist_ok=True)
report=dict(base=BASE,browsers=[],pages=0,quizChecks=0,blockedCssRequests=0,errors=[])
with sync_playwright() as pw:
 for name in ['webkit','chromium']:
  kwargs=dict(headless=True)
  if name=='chromium':kwargs['executable_path']='C:/Program Files/Google/Chrome/Application/chrome.exe'
  b=getattr(pw,name).launch(**kwargs);ctx=b.new_context(viewport=dict(width=1280,height=950),reduced_motion='reduce');p=ctx.new_page()
  def block(route):
   report['blockedCssRequests']+=1;route.abort()
  ctx.route('**/*.css*',block);p.on('pageerror',lambda e:report['errors'].append(str(e)))
  for person in ['carmen','ingo','tabea']:
   for day in BOOKS:
    for suffix in ['', 'lernheft/']:
     url=BASE+f'{person}/modul-2/tag-{day}/'+suffix;assert p.goto(url).status==200;p.wait_for_load_state('networkidle')
     assert p.locator('#module-reading-layout').count()==1
     assert p.evaluate('getComputedStyle(document.body).backgroundColor')=='rgb(250, 247, 238)'
     assert 'system-ui' in p.evaluate('getComputedStyle(document.body).fontFamily')
     for width in [1280,834,390,320]:
      p.set_viewport_size(dict(width=width,height=950))
      assert p.evaluate('getComputedStyle(document.querySelector(".layout")).display')=='grid'
      assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(name,person,day,suffix,width)
      assert float(p.locator('h2').first.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)'))>=28
     p.set_viewport_size(dict(width=1280,height=950))
     if suffix:
      for n,(_,_,right,why) in enumerate(QUIZZES[day],1):
       f=p.locator(f'[data-q="{n}"]');f.locator(f'input[value="{right}"]').check();f.locator('[data-answer]').click();assert f.locator('.feedback').inner_text()=='Passt. '+why;report['quizChecks']+=1
      if day==1:
       p.locator('#credit-calculate').click();assert '10 Credits' in p.locator('#credit-result').inner_text()
      if person=='carmen' and day==1:p.screenshot(path=str(QA/f'carmen-fixed-{name}.png'))
     report['pages']+=1
  ctx.close();b.close();report['browsers'].append(name)
assert report['blockedCssRequests']==0,report
assert not report['errors'],report
(QA/('layout-live.json' if BASE.startswith('https:') else 'layout-local.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report))
