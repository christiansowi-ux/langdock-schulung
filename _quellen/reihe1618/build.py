from pathlib import Path
import sys,html,json,hashlib,shutil,zipfile,csv,io
import fitz
from PIL import Image,ImageDraw
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[2];Q=ROOT/'_quellen';PUBLIC=ROOT/'plattform/public'
sys.path.insert(0,str(Q))
from reihe1618.content import BOOKS,QUIZ,SLIDES,SOURCES,DATE,SOURCE_FILE
E=lambda value:html.escape(str(value).replace('\u2011','-').replace('\u2013','-').replace('\u2014','-'))
NAMES={'ingo':'Ingo','carmen':'Carmen','tabea':'Tabea'}
INK='#183f35';PAPER='#faf7ee';GOLD='#f4df89';W=499.276
MATERIAL=PUBLIC/'material/reihe16-18'

def expanded(day,page,pid=None):
 out=[]
 for kind,value in page['blocks']:
  if kind=='mission':
   for person in ([pid] if pid else NAMES):
    out += [('h',NAMES[person]+' · dein Auftrag'),('prompt',value[person])]
  elif kind=='quiz':
   for i,(question,options,right,why) in enumerate(QUIZ[day],1):
    out += [('p',f'{i}. {question}\n'+ '\n'.join(f'{"ABC"[j]}: {o}' for j,o in enumerate(options)))]
  else:out.append((kind,value))
 return out

def render_web(pid,day):
 b=BOOKS[day];chapters=[]
 for no,page in enumerate(b['pages'],1):
  parts=[]
  if page['key']=='spiel':
   for i,(q,options,right,why) in enumerate(QUIZ[day],1):
    parts.append(f'<fieldset data-q="{i}"><legend>{i}. {E(q)}</legend>'+''.join(f'<label><input name="q{i}" type="radio" value="{j}"> {E(opt)}</label>' for j,opt in enumerate(options))+'<button type="button" data-answer>Antwort prüfen</button><p class="feedback" role="status" hidden></p></fieldset>')
  else:
   for j,(kind,v) in enumerate(expanded(day,page,pid)):
    if kind=='table':
     cols,rows=v
     parts.append('<div class="tablewrap" tabindex="0" role="region" aria-label="'+E(page['title'])+'"><table><thead><tr>'+''.join('<th scope="col">'+E(c)+'</th>' for c in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(t)+'</td>' for t in row)+'</tr>' for row in rows)+'</tbody></table></div>')
    elif kind=='source':
     sid,title,url=v;parts.append(f'<p class="source" id="src-{sid}"><b>[{sid}]</b> <a href="{E(url)}" target="_blank" rel="noopener noreferrer">{E(title)}</a><br><span>{E(url)}</span></p>')
    elif kind in ('prompt','code'):
     parts.append(f'<div class="prompt"><b>{"Auftrag" if kind=="prompt" else "Beispiel / passende Oberfläche beachten"}</b><pre id="copy-{no}-{j}">{E(v)}</pre><button type="button" data-copy="copy-{no}-{j}">Kopieren</button><span role="status" class="copystatus"></span></div>')
    elif kind=='h':parts.append('<h3>'+E(v)+'</h3>')
    elif kind=='answer':parts.append('<details><summary>Mögliche Antwort öffnen</summary><p>'+E(v)+'</p></details>')
    elif kind=='originals':
     parts.append('<details><summary>Zuordnung zur unveränderten Originalvorlage</summary>'+''.join(f'<figure><a href="/hefte/folien/tag-{day}/Folien_Tag{day}.pdf#page={n}"><img src="/hefte/folien/tag-{day}/{n:02}.jpg" loading="lazy" alt="Originalfolie {n}: {E(SLIDES[n-1][1])}"></a><figcaption>Originalfolie {n}, Ausgabe Juli 2026. Abbildungen und Aussagen sind eingeordnet, keine heutige Funktionszusage.</figcaption></figure>' for n in v)+'</details>')
    else:
     tag='aside' if kind in ('note','check') else 'p';parts.append(f'<{tag} class="{kind}">'+E(v).replace('\n','<br>')+f'</{tag}>')
  if page['key']=='branchen':parts.append(lab_markup(day))
  chapters.append(f'<section class="chapter" id="k{no}" data-key="{page["key"]}"><p class="eyebrow">{no:02} / {len(b["pages"])} · {E(page["deck"])}</p><h2>{E(page["title"])}</h2>'+''.join(parts)+'</section>')
 toc=''.join(f'<li><a href="#k{i}">{i:02} · {E(p["title"])}</a></li>' for i,p in enumerate(b['pages'],1))
 branch=next(i for i,p in enumerate(b['pages'],1) if p['key']=='branchen')
 data=json.dumps([dict(right=r,why=w) for q,o,r,w in QUIZ[day]],ensure_ascii=False).replace('<','\\u003c')
 related=' · '.join(f'<a href="/hefte/{pid}/tag-{d}/lernheft/">{bb["weekday"]}</a>' for d,bb in BOOKS.items())
 return f'''<!doctype html><html lang="de" data-person="{pid}" data-tag="{day}" data-page="lernheft"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><link rel="icon" href="/hefte/assets/favicon.svg"><title>{NAMES[pid]} · Tag {day} · {E(b['title'])}</title><link rel="stylesheet" href="/hefte/assets/toolbook.css"><link rel="stylesheet" href="/hefte/assets/workshop-series.css"><script src="/hefte/assets/workshop-series.js" defer></script></head><body><a class="skip" href="#main">Zum Inhalt</a><header><a href="/hefte/{pid}/tag-{day}/">← Tag {day}</a><span>{NAMES[pid]} · Werkstattreihe {day-15}/3</span><a href="/hefte/pdf/{b['pdf']}" download>PDF herunterladen</a></header><div class="layout"><nav aria-label="Kapitel"><details open><summary>Dein Lernweg</summary><p>{related}</p><p><a class="missionlink" href="#k{branch}">Deine Branchen-Mission →</a></p><p><a href="/hefte/material/reihe16-18/Nordlicht-Werkstatt.zip" download>Starterpaket herunterladen</a></p><ol>{toc}</ol></details></nav><main id="main">{''.join(chapters)}<section class="chapter"><h2>Deine Übergabe für die nächste Etappe</h2><label for="memo">Mein Ergebnis, meine Prüfungen, meine offene Frage</label><textarea id="memo" rows="5"></textarea><button id="save-note" type="button">Auf diesem Gerät speichern</button><button id="download-note" type="button">Als Text mitnehmen</button><p id="note-status" role="status">Die Notiz bleibt lokal in diesem Browser. Kein Versand an einen KI-Dienst.</p></section></main></div><script type="application/json" id="quiz-data">{data}</script></body></html>'''

def lab_markup(day):
 title={16:'Auftrags-Mixer',17:'MCP-Steckbrett',18:'Der Wiederholungs-Check'}[day]
 labels={16:['Quelle und Zeitraum benannt','Fehlende Werte sichtbar','Prüffälle festgelegt'],17:['Verbindung und Tool sichtbar','Passendes Testobjekt lesbar','Tatsächlichen Aufruf belegt'],18:['Neue Quelldatei verwendet','Nullbasis richtig behandelt','Ergebnis von anderer Person geprüft']}[day]
 return '<div class="lab"><p class="eyebrow">Vorbereitete Lernsimulation · keine echte KI oder Dienstverbindung</p><h3>'+title+'</h3><p>Schalte die drei Prüfpunkte ein oder aus und vergleiche den vorbereiteten Lernhinweis.</p>'+''.join(f'<label><input type="checkbox" data-signal="{i}"> {E(label)}</label>' for i,label in enumerate(labels))+'<button type="button" data-lab-check>Versuch prüfen</button><p class="lab-result" role="status">Noch kein Versuch geprüft.</p></div>'

def make_pdf(day):
 b=BOOKS[day];out=ROOT/b['out'];out.mkdir(exist_ok=True)
 for name,font in [('Body','arial.ttf'),('Bold','arialbd.ttf')]:
  if name not in pdfmetrics.getRegisteredFontNames():pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/font)))
 pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
 c=canvas.Canvas(str(out/b['pdf']),pagesize=(595.276,841.89));c.setTitle(f'Tag {day} · {b["title"]}');c.setAuthor('Futureway KI Institut');report=[]
 def para(text,size=10.6,bold=False,width=W):
  o=Paragraph(text,ParagraphStyle('p',fontName='Bold' if bold else 'Body',fontSize=size,leading=size*1.36,textColor=HexColor(INK)));_,h=o.wrap(width,900);return o,h
 def items(page,scale):
  result=[]
  for kind,v in expanded(day,page):
   if kind=='originals':
    v='Unveränderte Vorlage: Originalfolie(n) '+', '.join(map(str,v))+'. Im zugehörigen Web-Heft einzeln aufklappbar; vollständige Original-PDF im Folienbereich.';kind='p'
   if kind=='table':
    cols,rows=v;n=len(cols);widths=([144,W-144] if n==2 else [125]+[(W-125)/(n-1)]*(n-1))
    st=ParagraphStyle('cell',fontName='Body',fontSize=9.5*scale,leading=12.8*scale,textColor=HexColor(INK));hs=ParagraphStyle('h',parent=st,fontName='Bold',textColor=HexColor('#ffffff'))
    t=Table([[Paragraph(E(x),hs) for x in cols]]+[[Paragraph(E(x),st) for x in row] for row in rows],colWidths=widths)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor(INK)),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#e9eee1'),HexColor('#f1eee2')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8*scale),('BOTTOMPADDING',(0,0),(-1,-1),8*scale)]));_,h=t.wrap(W,900);result.append((kind,t,h,13*scale,0));continue
   if kind=='source':
    sid,title,url=v;txt=f'<b>[{sid}] {E(title)}</b><br/><link href="{E(url)}" color="{INK}">{E(url)}</link>';size=10.4
   else:
    txt=E(v).replace('\n','<br/>');size=13 if kind=='h' else 10.1 if kind=='code' else 10.6
    if kind=='prompt':txt='<b>Dein Auftrag</b><br/>'+txt
    if kind=='check':txt='<b>Selbstcheck · </b>'+txt
   box=kind in ('prompt','code','check','note');o,h=para(txt,size*scale,kind=='h',W-20 if box else W)
   result.append((kind,o,h,(17 if box else 11)*scale,10 if box else 0))
  return result
 for n,page in enumerate(b['pages'],1):
  c.bookmarkPage(page['key']);c.addOutlineEntry(page['title'],page['key'])
  c.setFillColor(HexColor(PAPER));c.rect(0,0,596,842,fill=1,stroke=0);c.setFillColor(HexColor(INK));c.rect(0,808,596,34,fill=1,stroke=0)
  c.setFillColor(HexColor('#ffffff'));c.setFont('Bold',9);c.drawString(48,821,f'FUTUREWAY KI INSTITUT · TAG {day} · WERKSTATTREIHE {day-15}/3')
  c.setFillColor(HexColor('#52685e'));c.setFont('Body',8);c.drawString(48,26,b['date']+' · Recherche 20.10.2026 · Beispiele erfunden');c.drawRightString(547,26,f'{n} / {len(b["pages"])}')
  y=780;o,h=para(E(page['deck']),9,True);o.drawOn(c,48,y-h);y-=h+15
  o,h=para(E(page['title']),33 if n==1 else 25,True);o.drawOn(c,48,y-h);y-=h+20
  scale=1;rows=items(page,scale)
  while sum(r[2]+r[3]+(8 if r[4] else 0) for r in rows)>y-51 and scale>.90:
   scale-=.02;rows=items(page,scale)
  total=sum(r[2]+r[3]+(8 if r[4] else 0) for r in rows)
  assert total<y-45,(day,n,page['key'],total,y)
  for kind,o,h,g,left in rows:
   if left:
    c.setFillColor(HexColor('#f4e9c1' if kind=='note' else '#e7ecdf' if kind=='check' else '#eee9dd'));c.roundRect(42,y-h-8,W+12,h+12,5,fill=1,stroke=0)
   o.drawOn(c,48+left,y-h-(4 if left else 0));y-=h+g+(8 if left else 0)
  if n==1 and y>195:
   for x,caption,num in [(48,'VERSTEHEN','1'),(220,'AUSPROBIEREN','2'),(392,'WEITERGEBEN','3')]:
    c.setFillColor(HexColor(GOLD if int(num)==day-15 else '#e7ecdf'));c.roundRect(x,90,154,55,7,fill=1,stroke=0);c.setFillColor(HexColor(INK));c.setFont('Bold',11);c.drawString(x+12,123,num);c.setFont('Body',9);c.drawString(x+12,105,caption)
  report.append(dict(page=n,key=page['key'],bottom=round(y,1),scale=round(scale,2)));c.showPage()
 c.save();return out/b['pdf'],report

def starter():
 MATERIAL.mkdir(parents=True,exist_ok=True)
 base=MATERIAL/'Nordlicht-Werkstatt';base.mkdir(exist_ok=True)
 files={
 'START_HIER.md':'# Nordlicht-Werkstatt\n\nAlle Angaben sind erfunden. Fallzeitraum März 2025 aus der Folienvorlage. Originale unverändert lassen. Die beiden XLSX-Eingaben der Vorlage werden hier durch CSV-Dateien ersetzt; sie waren nicht beigefügt. CSV-Trennzeichen: Semikolon; Zahlen mit deutschem Dezimalkomma.\n\nDienstag: Daten und Aussagen prüfen. Mittwoch: passende Quelle kontrolliert verbinden oder Dateialternative. Donnerstag: Ablauf am neuen Fall wiederholen.\n\nReferenzen erst nach erstem Versuch ansehen, außer beim bewussten Wiedereinstieg. 05_ergebnis für eigene Ausgaben neu anlegen. Keine echten Accounts oder geheimen Daten enthalten.\n',
 '01_eingang/umsatz_regionen.csv':'beleg_id;region;produktgruppe;umsatz_eur\nA001;Nord;Flyer;60000,00\nA002; nord ;Broschueren;60000,00\nA003;Süd;Flyer;80000,00\nA004;Süd;Broschueren;\nA005;Ost;Flyer;55000,00\nA006;Ost;Broschueren;50000,00\nA007;West;Flyer;70000,00\nA008;West;Broschueren;30000,00\nA001;Nord;Flyer;60000,00\n\n',
 '01_eingang/budget_2025.csv':'region;monat;plan_eur\nNord;2025-03;100000,00\nSüd;2025-03;100000,00\nOst;2025-03;100000,00\nWest;2025-03;100000,00\n',
 '01_eingang/vorjahr.csv':'region;monat;umsatz_eur\nNord;2024-03;110000,00\nSüd;2024-03;90000,00\nOst;2024-03;100000,00\nWest;2024-03;0,00\n',
 '01_eingang/notizen_vertriebsleitung.txt':'Fiktive Notizen, bewusst zu prüfen:\n- Nord: keine zusätzliche Ursachenquelle vorhanden.\n- Süd: Eine Umsatzangabe fehlt noch. Eine behauptete Verschiebung in den April ist bisher nicht belegt.\n- Ost: Der Umsatz sei gegenüber Vorjahr gefallen. Prüft diese Behauptung gegen die Zahlen!\n- West: Vorjahresbasis ist mit 0 angegeben. Keine gewöhnliche prozentuale Änderung berechnen.\n',
 '02_referenz/erwartete_kennzahlen.csv':'region;bekanntes_ist;plan;vorjahr;plan_delta;plan_delta_prozent;vorjahr_delta;vorjahr_delta_prozent;vollstaendig\nNord;120000;100000;110000;20000;20;10000;9,090909;ja\nSüd;80000;100000;90000;-20000;-20;-10000;-11,111111;nein\nOst;105000;100000;100000;5000;5;5000;5;ja\nWest;100000;100000;0;0;0;100000;nicht definiert;ja\n',
 '02_referenz/kontrollregeln.md':'# Prüfreferenz\n\nA001 nur einmal zählen, weil die Zeile exakt wiederholt wird. Die leere A004 bleibt ungeklärt. Bekannte Summen: Nord 120000, Süd 80000 unvollständig, Ost 105000, West 100000 Euro. Bekannte Gesamtsumme 405000 Euro ist unvollständig. Ost ist im Vorjahresvergleich um 5 Prozent gewachsen, nicht gefallen. West-Vorjahresrate nicht definiert, da Basis 0.\n\nAmpel als Unterrichtsregel: Zielerreichung ab 100% grün; ab90% bis unter100% gelb; unter90% rot. Unvollständigkeit zusätzlich als Text ausweisen.\n',
 '03_vorlagen/arbeitsauftrag.md':'# Vor dem Auftrag ausfüllen\nZiel:\nQuelle und Zeitraum:\nRegeln für fehlende Werte und Dubletten:\nAusgabeformat:\nDrei Prüffälle:\nGrenzen und offene Fragen:\n',
 '03_vorlagen/uebergabe.md':'# Übergabe\nErgebnisdatei:\nVerwendete Quellen:\nBestätigte Zahlen:\nOffene Punkte:\nTatsächlich durchgeführte Prüfungen:\nNächster Schritt:\n',
 '03_vorlagen/skill-beispiel/SKILL.md':'---\nname: nordlicht-bericht\ndescription: Prüft fiktive Monatsdaten und erstellt einen nachvollziehbaren Kurzbericht.\n---\n1. Quelle und Zeitraum feststellen.\n2. Fehlende Werte und exakte Dubletten melden.\n3. Bereinigungen begründen; Originale unverändert lassen.\n4. Kennzahlen mit passender Bezugsgröße berechnen.\n5. Mindestens drei Prüffälle kontrollieren.\n6. Ergebnis und offene Fragen getrennt ausgeben.\n7. Keine Nachrichten senden oder Daten veröffentlichen.\n\nDiese Vorlage ist nicht automatisch installiert. Passenden Produktpfad gemeinsam prüfen.\n',
 '04_neuer_fall/daten_neu.csv':'region;monat;ist_eur;plan_eur;vorjahr_eur\nNord;2025-04;90000;100000;100000\nSüd;2025-04;110000;100000;100000\nNeu;2025-04;5000;0;0\n',
 'branchen/crm_test.csv':'angebot;status;betrag_eur;naechster_schritt\nMondfalter;offen;1200;Rückruf gewünscht\nPapierpilot;offen;800;Termin unbekannt\nFarbfuchs;abgesagt;600;Kein offenes Angebot\n',
 'branchen/website_test.md':'# Fiktiver Testframe\nTeamfrühstück, 23.10.2026 9 Uhr, Raum Sonnenhof. Karten: Kaffee, Obst, Brötchen. Button: Interesse merken. Er zeigt nur lokal: Demo, es wurde nichts übermittelt. Keine Registrierung, kein Versand.\n\nPrüfungen: 390px ohne abgeschnittenen Text; Tastaturbedienung; korrekte Bestätigung.\n',
 'branchen/storyboard_test.md':'# Fiktiver interner Clip\nPapierfestival Pixel & Papier. 15 Sekunden; drei Szenen zu je fünf Sekunden; höchstens sechs Wörter je Texteinblendung. Nur belegte Aussagen, keine echten Marken oder Personen. Plan, bearbeitbare Datei und Videoexport getrennt benennen.\n',
 }
 for name,text in files.items():p=base/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf8')
 archive=MATERIAL/'Nordlicht-Werkstatt.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in base.rglob('*'):
   if p.is_file():z.write(p,p.relative_to(MATERIAL).as_posix())
 return archive

def render_simple(day):
 b=BOOKS[day];parts=[]
 for n in b['slides']:
  _,title,detail,example,q,a=SLIDES[n-1]
  idx=next(i for i,p in enumerate(b['pages'],1) if any(k=='originals' and n in v for k,v in p['blocks']))
  parts.append(f'<article class="simple-slide" id="einfach-{n}"><p class="kicker">Originalfolie {n} · heutige Zuordnung</p><h3>{E(title)}</h3><p>{E(detail)}</p><div class="simple-example"><p>{E(example)}</p></div><div class="simple-check"><p>{E(q)}</p><details><summary>Mögliche Antwort</summary><p>{E(a)}</p></details></div><p><a href="#folien" data-folie="{n}">Originalfolie {n}</a> · <a href="lernheft/#k{idx}">Im Lernheft</a></p></article>')
 return '<section class="tpanel wrap" id="einfach" role="tabpanel" aria-label="Einfach erklärt"><div class="panel-head"><div><h2>Die heutige Folienbegleitung</h2><p>Alle 27 Originalseiten sind über die drei Tage verteilt begleitet. Der Folienviewer enthält die unveränderte vollständige Vorlage.</p></div></div>'+''.join(parts)+'</section>'

def main(day=None):
 days=[day] if day else list(BOOKS);archive=starter()
 original=PUBLIC/'folien/tag-16/Folien_Tag16.pdf'
 if not original.exists():original=Path.home()/'Downloads'/SOURCE_FILE
 original_hash=hashlib.sha256(original.read_bytes()).hexdigest();doc=fitz.open(original);assert len(doc)==27
 cfgpath=Q/'folien.json';cfg=json.loads(cfgpath.read_text(encoding='utf8'))
 report=[]
 for d in days:
  b=BOOKS[d];pdf,layout=make_pdf(d)
  target=PUBLIC/'pdf'/b['pdf'];shutil.copy2(pdf,target)
  folder=PUBLIC/f'folien/tag-{d}';folder.mkdir(parents=True,exist_ok=True)
  if original.resolve()!=(folder/f'Folien_Tag{d}.pdf').resolve():shutil.copy2(original,folder/f'Folien_Tag{d}.pdf')
  rows=[]
  for n,p in enumerate(doc,1):
   rows.append(dict(n=n,links=[l['uri'] for l in p.get_links() if l.get('uri')]))
   for width,prefix in ((1440,''),(360,'t')):
    output=folder/f'{prefix}{n:02}.jpg'
    if d!=16 and (PUBLIC/f'folien/tag-16/{prefix}{n:02}.jpg').exists():shutil.copy2(PUBLIC/f'folien/tag-16/{prefix}{n:02}.jpg',output)
    else:
     pix=p.get_pixmap(matrix=fitz.Matrix(width/p.rect.width,width/p.rect.width),alpha=False);Image.frombytes('RGB',[pix.width,pix.height],pix.samples).save(output,quality=90)
  cfg[str(d)]=dict(pdf=SOURCE_FILE,n=27,ratio=round(doc[0].rect.width/doc[0].rect.height,4),slides=rows)
  for pid in NAMES:
   out=PUBLIC/pid/f'tag-{d}/lernheft';out.mkdir(parents=True,exist_ok=True);(out/'index.html').write_text(render_web(pid,d),encoding='utf8')
  (Path(__file__).parent/f'lernheft-{d}.html').write_text(render_web('tabea',d),encoding='utf8')
  qa=Q/f'build/reihe1618/tag-{d}';qa.mkdir(parents=True,exist_ok=True)
  final=fitz.open(pdf);assert len(final)==len(b['pages'])
  for i,p in enumerate(final,1):
   for block in p.get_text('blocks'):assert block[0]>=20 and block[1]>=10 and block[2]<=575 and block[3]<=830,(d,i,block)
   p.get_pixmap(dpi=85).save(qa/f'page-{i:02}.png')
  for start in range(1,len(final)+1,12):
   sheet=Image.new('RGB',(1240,1380),'#deded6');dr=ImageDraw.Draw(sheet)
   for off,n in enumerate(range(start,min(start+12,len(final)+1))):
    im=Image.open(qa/f'page-{n:02}.png');im.thumbnail((298,425));x=off%4*310+6;y=off//4*460+20;sheet.paste(im,(x,y));dr.text((x,y-15),str(n),fill='black')
   sheet.save(qa/f'contact-{start:02}.jpg',quality=90)
  (qa/'layout.json').write_text(json.dumps(layout,indent=2),encoding='utf8')
  report.append(dict(day=d,pages=len(final),min_scale=min(r['scale'] for r in layout),pdf=str(pdf)))
 cfgpath.write_text(json.dumps(cfg,ensure_ascii=False,indent=1),encoding='utf8')
 src=Path(__file__).parent
 (src/'sources.json').write_text(json.dumps(dict(date=DATE,sources={key:dict(title=t,url=u) for key,(t,u) in SOURCES.items()},original_sha256=original_hash,slide_assignment={str(d):b['slides'] for d,b in BOOKS.items()}),ensure_ascii=False,indent=2),encoding='utf8')
 (src/'folienabgleich.md').write_text('# Folienabgleich · 27 Originalseiten\n\n'+''.join(f'## {n}: {t}\n\n{detail}\n\nBeispiel: {ex}\n\nFrage: {q}\n\nAntwort: {a}\n\n' for n,t,detail,ex,q,a in SLIDES),encoding='utf8')
 assert sorted(n for b in BOOKS.values() for n in b['slides'])==list(range(1,28))
 print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else None)
