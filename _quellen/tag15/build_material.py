from pathlib import Path
import sys,json,html,re,shutil,hashlib
import fitz
from PIL import Image,ImageOps,ImageDraw
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
ROOT=Path(__file__).resolve().parents[2]
Q=ROOT/'_quellen'
sys.path.insert(0,str(Q))
from tag15.content import DATE,PAGES,SLIDES,SOURCES,QUIZ
PUBLIC=ROOT/'plattform/public'
OUT=ROOT/'Tag 15 - KI-Werkzeuge im Vergleich'
PDF='Lernheft_Tag15_KI-Werkzeuge-im-Vergleich.pdf'
OUT.mkdir(exist_ok=True)
E=html.escape
INK='#183f35';PAPER='#faf7ee';MUTED='#52685e';GOLD='#f4df89'

def render_web(pid):
 names={'ingo':'Ingo','carmen':'Carmen','tabea':'Tabea'}
 profile=names[pid]
 body=[]
 for i,page in enumerate(PAGES,1):
  key=page['key']
  blocks=[]
  if key=='quiz':
   for n,(q,opts,right,why) in enumerate(QUIZ,1):
    labels=''.join(f'<label><input type="radio" name="q{n}" value="{k}"> {E(t)}</label>' for k,t in enumerate(opts))
    blocks.append(f'<fieldset data-quiz="{n}"><legend>{n}. {E(q)}</legend>{labels}<button type="button" data-answer>Antwort prüfen</button><p role="status" class="feedback" hidden></p></fieldset>')
  else:
   for j,(kind,value) in enumerate(page['blocks']):
    if kind=='table':
     cols,rows=value
     blocks.append('<div class="tablewrap" tabindex="0" role="region" aria-label="'+E(page['title'])+'"><table><thead><tr>'+''.join('<th scope="col">'+E(t)+'</th>' for t in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(t)+'</td>' for t in row)+'</tr>' for row in rows)+'</tbody></table></div>')
    elif kind=='source':
     sid,title,url=value;blocks.append(f'<p class="source" id="src-{sid}"><b>[{sid}]</b> <a href="{E(url)}" target="_blank" rel="noopener noreferrer">{E(title)}</a><br><span>{E(url)}</span></p>')
    elif kind=='h':blocks.append('<h3>'+E(value)+'</h3>')
    elif kind=='prompt':blocks.append(f'<div class="prompt"><b>Dein Auftrag zum Kopieren</b><pre id="prompt-{i}-{j}">{E(value)}</pre><button type="button" data-copy="prompt-{i}-{j}">Auftrag kopieren</button><span role="status" class="copystatus"></span></div>')
    elif kind=='answer':blocks.append('<details><summary>Erst nachdenken, dann die mögliche Antwort öffnen</summary><p>'+E(value)+'</p></details>')
    else:blocks.append('<'+('aside' if kind in ('note','check') else 'p')+' class="'+kind+'">'+E(value).replace('\n','<br>')+'</'+('aside' if kind in ('note','check') else 'p')+'>')
  # Pair each explanation with the unchanged original slide, including graphical ones.
  if key.startswith('folien-'):
   first=int(key.split('-')[1])
   blocks.append('<details><summary>Beide Originalfolien ansehen</summary>'+''.join(f'<figure><a href="/hefte/folien/tag-15/Folien_Tag15.pdf#page={n}"><img loading="lazy" src="/hefte/folien/tag-15/{n:02d}.jpg" alt="Originalfolie {n}: {E(SLIDES[n-1][1])}"></a><figcaption>Originalfolie {n} · unveränderte Vorlage, nicht als aktuelle Produktzusage lesen</figcaption></figure>' for n in (first,first+1))+'</details>')
  body.append(f'<section class="chapter" id="k{i}" data-key="{key}"><p class="eyebrow">{i:02} / {len(PAGES)} · {E(page["deck"])}</p><h2>{E(page["title"])}</h2>'+''.join(blocks)+'</section>')
 toc=''.join(f'<li><a href="#k{i}">{i:02} · {E(p["title"])}</a></li>' for i,p in enumerate(PAGES,1))
 data=json.dumps([dict(right=r,why=w) for q,o,r,w in QUIZ],ensure_ascii=False).replace('<','\\u003c')
 return f'''<!doctype html><html lang="de" data-person="{pid}" data-tag="15" data-page="lernheft"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><link rel="icon" href="/hefte/assets/favicon.svg" type="image/svg+xml"><title>{profile} · Lernheft Tag 15 · KI-Werkzeuge</title><link rel="stylesheet" href="/hefte/assets/toolbook.css"><script src="/hefte/assets/toolbook.js" defer></script></head><body><a class="skip" href="#main">Zum Inhalt</a><header><a href="/hefte/{pid}/tag-15/">← Tag 15</a><span>{profile} · KI-Werkzeuge im Vergleich</span><a href="/hefte/pdf/{PDF}" download>PDF herunterladen</a></header><div class="layout"><nav aria-label="Kapitel"><details open><summary>Dein Lernweg</summary><p><a class="missionlink" href="#{ {'ingo':'k11','carmen':'k13','tabea':'k15'}[pid]}">Direkt zu deinen Missionen →</a></p><ol>{toc}</ol></details></nav><main id="main">{''.join(body)}<section class="chapter"><h2>Dein eigener Merksatz</h2><label for="memo">Was willst du morgen noch wissen?</label><textarea id="memo" rows="4" placeholder="Zum Beispiel: Ein Skill ist ein Arbeitszettel, keine Verbindung."></textarea><button type="button" id="save-note">Notiz auf diesem Gerät speichern</button><button type="button" id="download-note">Als Text mitnehmen</button><p role="status" id="note-status">Notiz bleibt in diesem Browser; keine Übermittlung an einen KI-Dienst.</p></section></main></div><script type="application/json" id="quiz-data">{data}</script></body></html>'''

def make_pdf():
 for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
 pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
 c=canvas.Canvas(str(OUT/PDF),pagesize=(595.276,841.89))
 c.setTitle('Vom Chat zur kleinen Werkstatt · Tag 15 · Antigravity, Codex und Claude Code')
 c.setAuthor('Futureway KI Institut')
 c.setSubject('Branchen-Missionen, Plugins und MCP · Recherche 19.10.2026 · 28 Folien begleitet')
 width=499.276
 def p(text,size=10.7,bold=False,color=INK,space=9,left=0):
  st=ParagraphStyle('b',fontName='Bold' if bold else 'Body',fontSize=size,leading=size*1.33,textColor=HexColor(color),splitLongWords=True)
  obj=Paragraph(text,st);_,h=obj.wrap(width-left,800)
  return obj,h,space,left
 def flow(page,scale=1):
  result=[]
  for kind,val in page['blocks']:
   if kind=='table':
    cols,rows=val;count=len(cols)
    if count==4:colw=[90]+[(width-90)/3]*3
    elif count==3:colw=[118,(width-118)/2,(width-118)/2]
    else:colw=[144,width-144]
    st=ParagraphStyle('cell',fontName='Body',fontSize=9.2*scale,leading=12*scale,textColor=HexColor(INK))
    hs=ParagraphStyle('head',parent=st,fontName='Bold',textColor=HexColor('#ffffff'))
    data=[[Paragraph(E(t),hs) for t in cols]]+[[Paragraph(E(t),st) for t in r] for r in rows]
    table=Table(data,colWidths=colw,hAlign='LEFT')
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor(INK)),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#eeeee3'),HexColor('#f6f1e4')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),9*scale),('BOTTOMPADDING',(0,0),(-1,-1),9*scale),('LINEBELOW',(0,0),(-1,0),1,HexColor(GOLD))]))
    _,h=table.wrap(width,800);result.append((kind,table,h,13*scale,0))
   elif kind=='source':
    sid,title,url=val
    ob,h,g,l=p(f'<b>[{sid}] {E(title)}</b><br/><link href="{E(url,quote=True)}" color="{INK}">{E(url)}</link>',10*scale,space=15*scale)
    result.append((kind,ob,h,g,l))
   else:
    size=(13 if kind=='h' else 10.4 if kind in ('note','check','prompt','answer') else 10.7)*scale
    text=E(val).replace('\n','<br/>')
    if kind=='prompt':text='<b>Dein Auftrag</b><br/>'+text
    if kind=='check':text='<b>Selbstcheck · </b>'+text
    ob,h,g,l=p(text,size,bold=(kind=='h'),color='#6b491d' if kind=='note' else INK,space=(12 if kind=='h' else 10)*scale,left=12 if kind in ('note','check','prompt') else 0)
    result.append((kind,ob,h,g,l))
  return result
 report=[]
 for num,page in enumerate(PAGES,1):
  c.bookmarkPage(page['key']);c.addOutlineEntry(page['title'],page['key'],0,False)
  c.setFillColor(HexColor(PAPER));c.rect(0,0,596,842,fill=1,stroke=0)
  c.setFillColor(HexColor(INK));c.rect(0,808,596,34,fill=1,stroke=0)
  c.setFillColor(HexColor('#ffffff'));c.setFont('Bold',8.8);c.drawString(48,821,'FUTUREWAY KI INSTITUT · TAG 15 · KI-WERKZEUGE IM VERGLEICH')
  c.setFillColor(HexColor(MUTED));c.setFont('Body',8.3);c.drawString(48,26,'19.10.2026 · Beispiele erfunden · Quellen ab Seite 38');c.drawRightString(547,26,str(num))
  y=781
  ob,h,g,l=p(E(page['deck']),9,True,color=MUTED,space=15);ob.drawOn(c,48,y-h);y-=h+g
  ob,h,g,l=p(E(page['title']),35 if num==1 else 25,True,space=18);ob.drawOn(c,48,y-h);y-=h+g
  scale=1;items=flow(page,scale)
  while sum(x[2]+x[3]+(12 if x[0] in ('note','check','prompt') else 0) for x in items)>y-53 and scale>.88:
   scale-=.02;items=flow(page,scale)
  required=sum(x[2]+x[3]+(12 if x[0] in ('note','check','prompt') else 0) for x in items)
  assert required<=y-47,(num,page['key'],required,y)
  for kind,obj,h,g,l in items:
   box=kind in ('note','check','prompt')
   if box:
    c.setFillColor(HexColor('#f4e9c1' if kind=='note' else '#e7ecdf' if kind=='check' else '#eee9dd'))
    c.roundRect(42,y-h-8,width+12,h+12,5,fill=1,stroke=0)
   obj.drawOn(c,48+l,y-h-(4 if box else 0));y-=h+g+(12 if box else 0)
  if num==1:
   for x,label,sub,no in [(48,'DRUCK','Rechnen & beraten','01'),(219,'TEAM','Planen & prüfen','02'),(390,'KREATIV','Gestalten & bewegen','03')]:
    c.setFillColor(HexColor('#e7ecdf'));c.roundRect(x,136,157,119,9,fill=1,stroke=0)
    c.setFillColor(HexColor(GOLD));c.circle(x+28,222,14,fill=1,stroke=0)
    c.setFillColor(HexColor(INK));c.setFont('Bold',10);c.drawCentredString(x+28,218,no);c.setFont('Bold',13);c.drawString(x+14,183,label);c.setFont('Body',9);c.drawString(x+14,161,sub)
  report.append(dict(page=num,key=page['key'],bottom=round(y,1),scale=round(scale,2)))
  c.showPage()
 c.save()
 return report

def main():
 report=make_pdf()
 folder=PUBLIC/'folien/tag-15';folder.mkdir(parents=True,exist_ok=True)
 original=folder/'Folien_Tag15.pdf'
 if not original.exists():original=Path.home()/'Downloads/Einfuhrung-Claude.pdf'
 assert original.exists()
 src_hash=hashlib.sha256(original.read_bytes()).hexdigest()
 if original.resolve()!=(folder/'Folien_Tag15.pdf').resolve():shutil.copy2(original,folder/'Folien_Tag15.pdf')
 doc=fitz.open(original);assert len(doc)==28
 slides=[]
 for n,p in enumerate(doc,1):
  slides.append(dict(n=n,links=[l['uri'] for l in p.get_links() if l.get('uri')]))
  for w,prefix in [(1440,''),(360,'t')]:
   pix=p.get_pixmap(matrix=fitz.Matrix(w/p.rect.width,w/p.rect.width),alpha=False)
   Image.frombytes('RGB',[pix.width,pix.height],pix.samples).save(folder/f'{prefix}{n:02}.jpg',quality=90)
 f=Q/'folien.json';data=json.loads(f.read_text(encoding='utf8'));data['15']=dict(pdf='Einfuhrung-Claude.pdf',n=28,ratio=round(doc[0].rect.width/doc[0].rect.height,4),slides=slides);f.write_text(json.dumps(data,ensure_ascii=False,indent=1),encoding='utf8')
 (PUBLIC/'pdf').mkdir(exist_ok=True);shutil.copy2(OUT/PDF,PUBLIC/'pdf'/PDF)
 # Optional direct export; the regular platform build also renders these pages.
 for pid in ('ingo','carmen','tabea'):
  target=PUBLIC/pid/'tag-15/lernheft';target.mkdir(parents=True,exist_ok=True);(target/'index.html').write_text(render_web(pid),encoding='utf8')
 src=Path(__file__).parent
 (src/'lernheft.html').write_text(render_web('tabea'),encoding='utf8')
 (src/'sources.json').write_text(json.dumps(dict(date=DATE,method='Offizielle Dokumentation, kein eigener Produkttest',sources=[dict(id=s,title=t,url=u) for s,t,u in SOURCES],original_sha256=src_hash,slides=28),ensure_ascii=False,indent=2),encoding='utf8')
 (src/'folienabgleich.md').write_text('# Folienabgleich · 19.10.2026\n\nVorlage unverändert. Alle 28 Seiten textlich und visuell geprüft. Erklärungen und Präzisierungen sind redaktionelle Lernhilfen.\n\n'+''.join(f'## Folie {n}: {t}\n\n{s}\n\n{d}\n\nBeispiel: {ex}\n\nFrage: {q}\n\nAntwort: {a}\n\nPräzisierung: {cor or "Keine zusätzliche Korrektur."}\n\n' for n,t,s,d,ex,q,a,cor in SLIDES),encoding='utf8')
 # All final pages rendered; bounds and page count checked independently with PyMuPDF.
 qa=ROOT/'_quellen/build/tag15';qa.mkdir(parents=True,exist_ok=True)
 final=fitz.open(OUT/PDF);assert len(final)==41
 for i,p in enumerate(final,1):
  for b in p.get_text('blocks'):
   assert b[0]>=20 and b[1]>=10 and b[2]<=575 and b[3]<=827,(i,b)
  p.get_pixmap(dpi=85).save(qa/f'page-{i:02}.png')
 for start in range(1,42,12):
  sheet=Image.new('RGB',(4*310,3*460),'#deded6');dr=ImageDraw.Draw(sheet)
  for off,n in enumerate(range(start,min(start+12,42))):
   im=Image.open(qa/f'page-{n:02}.png');im.thumbnail((298,425));x=(off%4)*310+6;y=(off//4)*460+20;sheet.paste(im,(x,y));dr.text((x,y-15),str(n),fill='black')
  sheet.save(qa/f'contact-{start:02}.jpg',quality=85)
 (qa/'layout-check.json').write_text(json.dumps(report,indent=2),encoding='utf8')
 assert hashlib.sha256(original.read_bytes()).hexdigest()==src_hash
 assert hashlib.sha256((folder/'Folien_Tag15.pdf').read_bytes()).hexdigest()==src_hash
 print(json.dumps(dict(pdf=str(OUT/PDF),pages=len(final),slides=28,min_scale=min(r['scale'] for r in report),original_sha256=src_hash),ensure_ascii=False))

if __name__=='__main__':main()
