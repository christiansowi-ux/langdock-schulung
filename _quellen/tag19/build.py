from pathlib import Path
import sys,html,json,hashlib,shutil
import fitz
from PIL import Image,ImageDraw
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[2];Q=ROOT/'_quellen';PUB=ROOT/'plattform/public'
sys.path.insert(0,str(Q))
from tag19.content import PAGES,SLIDES,SOURCES,DATE,SOURCE_FILE,PDF,BONUS_PDF
from tag19.bonus_content import PAGES as BONUS
INK='#183f35';PAPER='#faf7ee';W=499.276
NAMES={'ingo':'Ingo','carmen':'Carmen','tabea':'Tabea'}
QA=Q/'build/tag19'
E=lambda v:html.escape(str(v).replace('\u2011','-').replace('\u2013','-').replace('\u2014','-'))

def pages():
 out=list(PAGES)
 for start in range(0,20,5):
  rows=SLIDES[start:start+5]
  out.append(dict(key='folien-'+str(start+1),title='Die Vorlage in einfachen Worten',deck='Folienabgleich · Originalseiten '+str(start+1)+' bis '+str(start+5),blocks=[(kind,value) for n,title,text in rows for kind,value in [('h',f'{n:02} · {title}'),('p',text)]]))
 for no,ids in enumerate([['C1','C2','C3','G1','A1','A2'],['M1','M2','M3','M4']],1):
  out.append(dict(key='quellen-'+str(no),title='Quellen und Aktualität',deck='Anhang · offizielle Quellen · '+DATE,blocks=[('p','Recherche am 23.10.2026. Originalfolien und heutige Produktbeschreibung unterscheiden. Die Aufgaben und Alltagsvergleiche sind eigene Lernhilfen. Keine vollständigen Produkttests auf allen Teilnehmerkonten. Make ist ausschließlich Vorbereitung, ohne Übungsauftrag.')]+[('source',(k,*SOURCES[k])) for k in ids]))
 return out

def make_pdf(items,target,title,bonus=False,header=None,date=None,research_date=None):
 target.parent.mkdir(parents=True,exist_ok=True)
 for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf')]:
  if name not in pdfmetrics.getRegisteredFontNames():pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
 pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
 c=canvas.Canvas(str(target),pagesize=(595.276,841.89));c.setTitle(title);c.setAuthor('Futureway KI Institut');report=[]
 def paragraph(text,size=10.6,bold=False,width=W):
  p=Paragraph(text,ParagraphStyle('p',fontName='Bold' if bold else 'Body',fontSize=size,leading=size*1.35,textColor=HexColor(INK)));_,h=p.wrap(width,1000);return p,h
 def rows(page,scale):
  result=[]
  for kind,value in page['blocks']:
   if kind=='table':
    cols,data=value;st=ParagraphStyle('cell',fontName='Body',fontSize=9.6*scale,leading=13*scale,textColor=HexColor(INK));hs=ParagraphStyle('h',parent=st,fontName='Bold',textColor=HexColor('#ffffff'))
    t=Table([[Paragraph(E(x),hs) for x in cols]]+[[Paragraph(E(x),st) for x in row] for row in data],colWidths=[W/len(cols)]*len(cols));t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor(INK)),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#e8ede1'),HexColor('#f0ecdf')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7*scale),('BOTTOMPADDING',(0,0),(-1,-1),7*scale)]));_,h=t.wrap(W,1000);result.append((kind,t,h,13*scale,0));continue
   if kind=='source':
    sid,name,url=value;text=f'<b>[{sid}] {E(name)}</b><br/><link href="{E(url)}" color="{INK}">{E(url)}</link>';size=9.8
   else:
    if kind=='flow':value='  →  '.join(value)
    text=E(value).replace('\n','<br/>');size=12.5 if kind=='h' else 10.4 if kind=='code' else 10.6
    if kind=='prompt':text='<b>Zum Kopieren</b><br/>'+text
    if kind=='check':text='<b>Prüfen · </b>'+text
   box=kind in ('note','prompt','code','check','flow');o,h=paragraph(text,size*scale,kind=='h',W-20 if box else W);result.append((kind,o,h,(14 if box else 10)*scale,10 if box else 0))
  return result
 for n,page in enumerate(items,1):
  c.bookmarkPage(page['key']);c.addOutlineEntry(page['title'],page['key']);c.setFillColor(HexColor(PAPER));c.rect(0,0,596,842,fill=1,stroke=0);c.setFillColor(HexColor(INK));c.rect(0,808,596,34,fill=1,stroke=0)
  c.setFillColor(HexColor('#ffffff'));c.setFont('Bold',9);c.drawString(48,821,'FUTUREWAY KI INSTITUT · '+(header or ('BONUSHEFT' if bonus else 'TAG 19 · FREITAG')))
  stamp=date or DATE
  c.setFillColor(HexColor('#52685e'));c.setFont('Body',8);c.drawString(48,26,stamp+' · Recherche '+(research_date or stamp)+' · Beispiele erfunden');c.drawRightString(547,26,f'{n} / {len(items)}')
  y=780;o,h=paragraph(E(page['deck']),9,True);o.drawOn(c,48,y-h);y-=h+14
  o,h=paragraph(E(page['title']),31 if n==1 else 25,True);o.drawOn(c,48,y-h);y-=h+18
  scale=1;rr=rows(page,scale)
  while sum(r[2]+r[3]+(6 if r[4] else 0) for r in rr)>y-51 and scale>.92:
   scale-=.02;rr=rows(page,scale)
  assert sum(r[2]+r[3]+(6 if r[4] else 0) for r in rr)<y-45,(n,page['key'],sum(r[2]+r[3] for r in rr),y)
  for kind,o,h,g,left in rr:
   if left:
    c.setFillColor(HexColor('#f2e6bd' if kind=='note' else '#e5ecde' if kind in ('flow','check') else '#eee9dd'));c.roundRect(42,y-h-7,W+12,h+11,5,fill=1,stroke=0)
   o.drawOn(c,48+left,y-h-(3 if left else 0));y-=h+g+(6 if left else 0)
  report.append(dict(page=n,key=page['key'],bottom=round(y,1),scale=round(scale,2)));c.showPage()
 c.save();return report

def block_web(kind,value,ident):
 if kind=='table':
  cols,rows=value;return '<div class="tablewrap" tabindex="0" role="region" aria-label="Vergleich"><table><thead><tr>'+''.join('<th scope="col">'+E(v)+'</th>' for v in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
 if kind=='source':
  sid,title,url=value;return f'<p class="source"><b>[{sid}]</b> <a href="{E(url)}" target="_blank" rel="noopener noreferrer">{E(title)}</a><br>{E(url)}</p>'
 if kind in ('prompt','code'):
  button=f'<button type="button" data-copy="{ident}">Kopieren</button><span class="copystatus" role="status"></span>' if kind=='prompt' else ''
  return f'<div class="prompt"><pre id="{ident}">{E(value)}</pre>{button}</div>'
 if kind=='flow':return '<ol class="flow" aria-label="Erklärbild, kein ausführbarer Ablauf">'+''.join('<li>'+E(v)+'</li>' for v in value)+'</ol>'
 tag='h3' if kind=='h' else 'aside' if kind in ('note','check') else 'p'
 return f'<{tag} class="{kind}">'+E(value).replace('\n','<br>')+f'</{tag}>'

def shell(pid,title,sections,toc,bonus=False,day=False):
 nav=f'<a href="/hefte/{pid}/tag-19/">Freitag im Überblick</a><p><a href="/hefte/{pid}/tag-19/lernheft/">Freitagsheft</a> · <a href="/hefte/{pid}/tag-19/bonus/">Bonusheft</a></p>'
 pdf=BONUS_PDF if bonus else PDF
 return f'''<!doctype html><html lang="de" data-person="{pid}" data-tag="19"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{NAMES[pid]} · {E(title)}</title><link rel="icon" href="/hefte/assets/favicon.svg"><link rel="stylesheet" href="/hefte/assets/toolbook.css"><link rel="stylesheet" href="/hefte/assets/workshop-series.css"><style>.flow{{list-style:none;padding:0;display:grid;gap:.6rem}}.flow li{{padding:1rem;background:#e5ecde;border-left:4px solid #547449}}.flow li+li:before{{content:'↓ ';font-weight:bold}}.original img{{max-width:100%;height:auto;border:1px solid #ccd0c4}}.chapter a{{overflow-wrap:anywhere}}</style><script src="/hefte/assets/friday19.js" defer></script></head><body><a class="skip" href="#main">Zum Inhalt</a><header><a href="/hefte/{pid}/">← Kursübersicht</a><span>{NAMES[pid]} · Freitag, {DATE}</span><a href="/hefte/pdf/{pdf}" download>PDF herunterladen</a></header><div class="layout"><nav aria-label="Inhalt"><details open><summary>Dein Lernweg</summary>{nav}<ol>{toc}</ol></details></nav><main id="main">{sections}</main></div></body></html>'''

def render_web(pid,bonus=False):
 items=BONUS if bonus else pages();sections=[]
 for i,p in enumerate(items,1):
  blocks=''.join(block_web(k,v,f'copy-{i}-{j}') for j,(k,v) in enumerate(p['blocks']))
  sections.append(f'<section class="chapter" id="k{i}" data-key="{p["key"]}" data-part="{p.get("part","bonus" if bonus else "anhang")}"><p class="eyebrow">{i:02} / {len(items)} · {E(p["deck"])}</p><h2>{E(p["title"])}</h2>{blocks}</section>')
 toc=''.join(f'<li><a href="#k{i}">{i:02} · {E(p["title"])}</a></li>' for i,p in enumerate(items,1))
 return shell(pid,'Bonus: fünf Fälle und 20 Prompts' if bonus else 'Design und Make-Ausblick',''.join(sections),toc,bonus)

def render_day(pid):
 intro=f'''<section class="chapter" id="start"><p class="eyebrow">Tag 19 · Freitag, {DATE}</p><h2>Designideen und ein leichter Make-Ausblick</h2><p>Die erste Hälfte: Claude Design, Google Stitch und Canva. Die zweite Hälfte: reine Vorbereitung auf Montag, 26.10.2026.</p><aside class="note">Make heute nur verstehen. Keine Übungen, Kontoeinrichtung, Quizfragen oder Testläufe.</aside><p><a href="lernheft/">Freitagsheft lesen →</a></p><p><a href="bonus/">Bonusheft: fünf Anwendungsfälle und 20 Prompts →</a></p><p><a href="/hefte/pdf/{PDF}" download>Freitagsheft als PDF</a> · <a href="/hefte/pdf/{BONUS_PDF}" download>Bonusheft als PDF</a></p></section>'''
 original='<section class="chapter" id="folien"><h2>Die vollständige Originalvorlage</h2><p>20 Folien, Ausgabe Juli 2026. Herstelleränderungen stehen im Lernheft. Die Vorlage enthält Video- und Werbeverweise; sie sind keine heutigen Pflichtaufgaben.</p><p><a href="/hefte/folien/tag-19/Folien_Tag19.pdf">Original-PDF öffnen</a></p>'
 for n,title,detail in SLIDES:
  original+=f'<details class="original" id="folie-{n}"><summary>{n:02} · {E(title)}</summary><p>{E(detail)}</p><a href="/hefte/folien/tag-19/Folien_Tag19.pdf#page={n}"><img loading="lazy" src="/hefte/folien/tag-19/{n:02}.jpg" alt="Originalfolie {n}: {E(title)}"></a></details>'
 return shell(pid,'Freitag · Design und Make-Ausblick',intro+original+'</section>','<li><a href="#start">Freitag</a></li><li><a href="#folien">Originalfolien</a></li>',day=True)

def main():
 QA.mkdir(parents=True,exist_ok=True)
 targets=[(pages(),ROOT/'Tag 19 - Design und Make-Ausblick'/PDF,'Design und Make-Ausblick',False),(BONUS,ROOT/'Bonus - KI im Alltag'/BONUS_PDF,'Fünf KI-Anwendungsfälle und 20 Prompts',True)]
 report=[]
 for items,target,title,bonus in targets:
  layout=make_pdf(items,target,title,bonus);shutil.copy2(target,PUB/'pdf'/target.name)
  qa=QA/('bonus' if bonus else 'freitag');qa.mkdir(exist_ok=True)
  with fitz.open(target) as d:
   assert len(d)==len(items)
   for n,p in enumerate(d,1):
    for b in p.get_text('blocks'):assert b[0]>=20 and b[1]>=10 and b[2]<=575 and b[3]<=830,(target,n,b)
    p.get_pixmap(dpi=85).save(qa/f'page-{n:02}.png')
   for start in range(1,len(d)+1,12):
    sheet=Image.new('RGB',(1240,1380),'#deded6');draw=ImageDraw.Draw(sheet)
    for offset,n in enumerate(range(start,min(start+12,len(d)+1))):
     im=Image.open(qa/f'page-{n:02}.png');im.thumbnail((298,425));x=offset%4*310+6;y=offset//4*460+20;sheet.paste(im,(x,y));draw.text((x,y-15),str(n),fill='black')
    sheet.save(qa/f'contact-{start:02}.jpg',quality=90)
  (qa/'layout.json').write_text(json.dumps(layout,indent=2),encoding='utf8');report.append(dict(pdf=str(target),pages=len(items),min_scale=min(r['scale'] for r in layout)))
 folder=PUB/'folien/tag-19';folder.mkdir(parents=True,exist_ok=True);original=folder/'Folien_Tag19.pdf'
 if not original.exists():shutil.copy2(Path.home()/'Downloads'/SOURCE_FILE,original)
 with fitz.open(original) as d:
  assert len(d)==20;rows=[]
  for n,p in enumerate(d,1):
   rows.append(dict(n=n,links=[l['uri'] for l in p.get_links() if l.get('uri')]))
   for width,prefix in [(1440,''),(360,'t')]:
    pix=p.get_pixmap(matrix=fitz.Matrix(width/p.rect.width,width/p.rect.width),alpha=False);Image.frombytes('RGB',[pix.width,pix.height],pix.samples).save(folder/f'{prefix}{n:02}.jpg',quality=90)
  cfgpath=Q/'folien.json';cfg=json.loads(cfgpath.read_text(encoding='utf8'));cfg['19']=dict(pdf=SOURCE_FILE,n=20,ratio=round(d[0].rect.width/d[0].rect.height,4),slides=rows);cfgpath.write_text(json.dumps(cfg,ensure_ascii=False,indent=1),encoding='utf8')
 for pid in NAMES:
  for sub,content in [('lernheft',render_web(pid)),('bonus',render_web(pid,True))]:
   out=PUB/pid/'tag-19'/sub;out.mkdir(parents=True,exist_ok=True);(out/'index.html').write_text(content,encoding='utf8')
  (PUB/pid/'tag-19/index.html').write_text(render_day(pid),encoding='utf8')
 (Path(__file__).parent/'sources.json').write_text(json.dumps(dict(date=DATE,sources=SOURCES,original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),core_design_pages=10,core_make_reading_pages=10),ensure_ascii=False,indent=2),encoding='utf8')
 (QA/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
