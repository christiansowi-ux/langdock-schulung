from pathlib import Path
import json,sys,shutil,html,hashlib,re
import fitz
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
ROOT=Path(__file__).resolve().parents[2];Q=ROOT/'_quellen';PUBLIC=ROOT/'plattform/public';sys.path.insert(0,str(Q))
from einfach_tag14 import SLIDES,SOURCES
from kurs_tag14 import TAG14
from tag14.easy_tasks import EXERCISES,START
E=html.escape
original=PUBLIC/'folien/tag-14/Folien_Tag14.pdf'
if not original.exists():original=Path.home()/'Downloads/Agent-Observability.pdf'
doc=fitz.open(original);assert len(doc)==8
folder=PUBLIC/'folien/tag-14';folder.mkdir(parents=True,exist_ok=True)
if original.resolve()!=(folder/'Folien_Tag14.pdf').resolve():shutil.copy2(original,folder/'Folien_Tag14.pdf')
slides=[]
for i,p in enumerate(doc,1):
 links=[l['uri'] for l in p.get_links() if l.get('uri')]
 slides.append(dict(n=i,links=links))
 for width,prefix in [(1440,''),(360,'t')]:
  pix=p.get_pixmap(matrix=fitz.Matrix(width/p.rect.width,width/p.rect.width),alpha=False)
  Image.frombytes('RGB',[pix.width,pix.height],pix.samples).save(folder/f'{prefix}{i:02d}.jpg',quality=90)
f=Q/'folien.json';cfg=json.loads(f.read_text(encoding='utf8'));cfg['14']=dict(pdf='Agent-Observability.pdf',n=8,ratio=round(doc[0].rect.width/doc[0].rect.height,4),slides=slides);f.write_text(json.dumps(cfg,ensure_ascii=False,indent=1),encoding='utf8')
practice=[('Mission 1: Spurensuche','Im Agenten-Cockpit alle vier Stationen öffnen. Aktuelle Referenz, Eingabe und Ergebnis vergleichen. Die erste falsche Abzweigung benennen. Den längsten Schritt getrennt davon bestimmen.'),('Mission 2: Vergleichslabor','Vor dem Vergleich gelten drei Qualitätskriterien: aktuelle Quelle, richtige Fakten, höchstens zwei Sätze. Zusätzlich maximal fünf Sekunden und 0,005 Euro Demo-Modellkosten. Alle vier vorbereiteten Varianten vergleichen und die Auswahl begründen.'),('Mission 3: Signal-Check','Sechs Beobachtungen Monitoring, Logging, Tracing oder Evaluation zuordnen. Erst selbst entscheiden, dann die Erklärung lesen. Unsichere Fälle erneut bearbeiten.'),('Der eigene Transfer','Einen Merksatz und eine offene Frage notieren. Eine sinnvolle Änderung vorschlagen und mit denselben Kriterien an mehreren erfundenen Fällen erneut prüfen. Eine schnellere falsche Antwort ist keine inhaltliche Verbesserung.'),('Ohne Agent-Zugang','Die drei Missionen funktionieren vollständig im Browser. In einem normalen Langdock-Chat kann man anschließend einen erfundenen Verlauf erklären lassen. Dabei darf die KI keine echten Messwerte oder eine echte Verbindung behaupten.'),('Optionaler echter Test im Kurs','Nur mit berechtigtem, freigegebenem Zugang: die aktuelle Herstelleranleitung aus Folie 7 gemeinsam durchgehen, einen vorgesehenen Agenten anbinden und eine erfundene Testfrage prüfen. Schlüssel privat halten; keine echten Daten ungeprüft übertragen. Das Cockpit selbst stellt keine Verbindung her.')]
src=Q/'tag14';src.mkdir(exist_ok=True)
parts=['<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Lernheft Tag 14 – Agent Observability</title>{{HEAD}}</head><body class="lh">{{BAR}}<section class="lp cover"><img class="logo" src="{{LOGO}}" alt="Futureway KI Institut"><p class="kicker">Tag 14 · Lektion 13 · 16.10.2026</p><div class="big" style="font-size:54pt">Der Antwort<br>auf der Spur.</div><div class="big2">Das Agenten-Cockpit.</div><p class="sub">Acht Folien verständlich erklärt. Mit ausgedachten Beispielen, Merkfragen und drei Mitmach-Missionen. Dazu vier kurze Langdock-Spiele mit Varianten für alle drei Bereiche.</p><span class="note">{{ICON:search}} Erst die Spuren lesen. Dann urteilen.</span></section>']
for n,title,simple,points,example,question,answer,correction,_ in SLIDES:
 parts.append(f'<section class="lp" id="k{n}"><div class="kh"><span class="kn">{n:02}</span><div><p class="kk">Originalfolie {n} · Agent Observability</p><h2>{E(title)}</h2></div>{{{{UX:{n}}}}}</div><p class="lead">{E(simple)}</p><ul>'+''.join('<li>'+E(x)+'</li>' for x in points)+'</ul><div class="fall" style="display:block"><h4>Ausgedachtes Beispiel</h4><p>'+E(example)+'</p></div>'+(f'<div class="card"><h4>Präzisierung und ergänzende Lernhilfe</h4><p>{E(correction)}</p></div>' if correction else '')+f'<div class="merk"><span class="ml">Erst selbst überlegen</span><p>{E(question)}</p></div><details><summary>Eine mögliche Antwort</summary><p>{E(answer)}</p></details><p class="small"><a href="/hefte/folien/tag-14/Folien_Tag14.pdf#page={n}">Originalfolie {n}</a> · <a href="#quellen">Quellen und Prüfdatum</a></p></section>')
parts.append('<section class="lp" id="k9"><div class="kh"><h2>So wird aus Wissen ein Versuch</h2></div><p>Ergänzende Lernhilfen. Alle Zahlen und Fälle im Cockpit sind erfunden.</p>'+''.join('<h3>'+E(t)+'</h3><p>'+E(d)+'</p>' for t,d in practice)+'</section>')
for i,task in enumerate(EXERCISES,10):
 prompts=''.join('<details class="ueb"><summary>'+E(person)+'</summary><p>In einen neuen Langdock-Chat kopieren:</p><div class="ucode">'+E(case+'\n\n'+task['prompt'])+'</div></details>' for person,case in task['cases'])
 parts.append(f'<section class="lp" id="k{i}"><div class="kh"><span class="kn">{i:02}</span><div><p class="kk">Leichtes Langdock-Spiel · {E(task["minutes"])}</p><h2>{E(task["title"])}</h2></div>{{{{UX:{i}}}}}</div><p class="lead">{E(task["goal"])}</p><p>{E(START)}</p><p><b>So spielt man:</b> {E(task["steps"])}</p>'+prompts+f'<div class="merk"><span class="ml">Kleiner Selbstcheck</span><p>{E(task["check"])}</p></div><details><summary>Erst nach dem Versuch: mögliche Auflösung</summary><p>{E(task["solution"])}</p></details><p><b>Freiwillige Bonusrunde:</b> {E(task["bonus"])}</p><p class="small">Nur erfundene Angaben. Die KI hilft beim Üben; ihre Rückmeldung mit Referenz und Auflösung selbst vergleichen. Keine echte Messung, kein externer Versand.</p></section>')
parts.append('<section class="lp" id="quellen"><h2>Quellen und Folienabgleich</h2><p>Alle acht Originalfolien textlich und visuell abgeglichen. Ausgabe Juli 2026; Produktanleitung und Präzisierungen geprüft am 16.10.2026. Original unverändert. Das Lernheft ist keine Bestätigung einer echten Anbindung.</p><ul>'+''.join(f'<li><a href="{E(u)}">{E(t)}</a></li>' for t,u in SOURCES)+'</ul></section></body></html>')
(src/'lernheft.html').write_text('\n'.join(parts),encoding='utf8')
conf=dict(src='tag14/lernheft.html',out='Tag 14 - Agent Observability',pdf=TAG14['lernheft'],kurz='Agent Observability',label='Lernheft · Der Antwort auf der Spur',titles={s[0]:s[1] for s in SLIDES}|{9:'So wird aus Wissen ein Versuch'}|{i:t['title'] for i,t in enumerate(EXERCISES,10)},uebungen=(10,11,12,13))
p=Q/'lernheft.py';text=p.read_text(encoding='utf8')
if re.search(r'^    14: ',text,re.M): text=re.sub(r'^    14: .*$',lambda m:'    14: '+repr(conf)+',',text,flags=re.M)
else: text=text.replace('    # Praxishefte:', '    14: '+repr(conf)+',\n    # Praxishefte:')
p.write_text(text,encoding='utf8')
for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
out=ROOT/conf['out'];out.mkdir(exist_ok=True);c=canvas.Canvas(str(out/conf['pdf']),pagesize=(595.276,841.89));c.setTitle('Tag 14 – Agent Observability: Der Antwort auf der Spur');c.setAuthor('Futureway KI Institut')
W=499;ink='#183f35'
def para(text,y,size=10.3,bold=False,color=ink):
 st=ParagraphStyle('p',fontName='Bold' if bold else 'Body',fontSize=size,leading=size*1.36,textColor=HexColor(color));p=Paragraph(text,st);_,h=p.wrap(W,800);p.drawOn(c,48,y-h);return y-h

def page(no,kicker):
 c.setFillColor(HexColor('#faf7ee'));c.rect(0,0,596,842,fill=1,stroke=0);c.setFillColor(HexColor(ink));c.rect(0,808,596,34,fill=1,stroke=0);c.setFillColor(HexColor('#ffffff'));c.setFont('Bold',9);c.drawString(48,821,'FUTUREWAY KI INSTITUT · TAG 14 · AGENT OBSERVABILITY');c.setFillColor(HexColor(ink));c.setFont('Body',9);c.drawString(48,25,'16.10.2026 · Beispiele und Cockpit-Messwerte erfunden');c.drawRightString(547,25,str(no));return para(E(kicker),780,10,True)-16

y=page(1,'DAS AGENTEN-COCKPIT');y=para('Der Antwort<br/>auf der Spur.',y,45,True)-25;y=para('Grün gelaufen.<br/>Trotzdem daneben?',y,25,True)-22
y=para('Acht Originalfolien in verständlichen Worten. Jede Folie mit Einzelheiten, ausgedachtem Beispiel, einer Frage zum Mitdenken und einer möglichen Antwort.',y,13)-18
y=para('Man verfolgt einen Ablauf, entdeckt einen Fehler und prüft eine Verbesserung. Ganz ohne Agent-Zugang und ohne echte Kundendaten.',y,13)-25
for t,d in [('01 · Verstehen','Warum eine grüne Betriebsanzeige noch keine gute Antwort beweist.'),('02 · Beobachten','Logs sind die Punkte. Ein Trace verbindet den Weg.'),('03 · Prüfen','Qualität, Zeit und Kosten zusammen beurteilen.')]:
 y=para(E(t),y,15,True)-6;y=para(E(d),y,12)-18
y=para('Die echte Langdock-/Langfuse-Aufgabe wird mit ihren Voraussetzungen erklärt. Das Lern-Cockpit nutzt vorbereitete Fälle und aktiviert keine Verbindung.',y,10.5);assert y>45;c.showPage()
heights=[]
for n,title,simple,points,example,question,answer,correction,_ in SLIDES:
 y=page(n+1,f'FOLIE {n:02} / 8 · VERSTEHEN, BEVOR MAN WEITERKLICKT');y=para(E(title),y,24,True)-15;y=para(E(simple),y,12,True)-15
 for p in points:y=para('• '+E(p),y,10.1)-6
 y=para('<b>Ausgedachtes Beispiel</b><br/>'+E(example),y-6,10.5)-12
 if correction:y=para('<b>Präzisierung und ergänzende Lernhilfe</b><br/>'+E(correction),y,9.8,color='#755016')-12
 y=para('<b>Erst selbst überlegen:</b> '+E(question),y,10.5)-9;y=para('<b>Eine mögliche Antwort:</b> '+E(answer),y,10.5)-10;y=para(f'Originalfolie {n}. Quellen und Prüfdatum auf Seite 15.',y,8.5,color='#4c6359');assert y>45,(n,y);heights.append((n,round(y,1)));c.showPage()
y=page(10,'DIE DREI MISSIONEN · ERGÄNZENDE LERNHILFEN');y=para('So wird aus Wissen<br/>ein Versuch.',y,27,True)-20
for title,body in practice:y=para(E(title),y,12,True)-6;y=para(E(body),y,10.5)-17
assert y>45,y;c.showPage()
for i,task in enumerate(EXERCISES,11):
 y=page(i,'LEICHTES LANGDOCK-SPIEL · '+task['minutes'].upper());y=para(E(task['title']),y,25,True)-14
 y=para(E(task['goal']),y,12,True)-12;y=para(E(START),y,10)-12
 y=para('<b>So spielt man:</b> '+E(task['steps']),y,10)-12
 y=para('1 · Den eigenen Fall wählen',y,12,True)-7
 for person,case in task['cases']:
  y=para('<b>'+E(person)+'</b><br/>'+E(case),y,9.6)-9
 y=para('2 · Diesen Spielauftrag zusammen mit deinem Fall kopieren',y,11,True)-7
 y=para(E(task['prompt']),y,9.8)-12
 y=para('<b>Selbstcheck:</b> '+E(task['check']),y,10)-9
 y=para('<b>Erst nach dem Versuch lesen:</b> '+E(task['solution']),y,9.5,color='#755016')-9
 y=para('<b>Freiwillige Bonusrunde:</b> '+E(task['bonus']),y,9.8)-8
 y=para('Nur erfundene Angaben. Rückmeldung der KI selbst mit der Referenz vergleichen.',y,8.5)
 assert y>45,(task['title'],y);heights.append(('Spiel '+str(i-10),round(y,1)));c.showPage()
y=page(15,'QUELLEN UND FOLIENABGLEICH');y=para('Nachlesen.<br/>Selbst erklären.',y,29,True)-24
for title,url in SOURCES:y=para(f'<b>{E(title)}</b><br/><link href="{E(url)}" color="#176954">Offizielle Dokumentation öffnen</link>',y,11)-18
y=para('Grundlage: Agent-Observability.pdf, acht Folien, Ausgabe Juli 2026. Alle Seiten textlich und visuell abgeglichen. Quellenprüfung: 16.10.2026. Cockpit, Messwerte, Beispiele und die Praxisanleitung ergänzen die Originalfolien. Produktoberflächen und Berechtigungen können je Workspace abweichen.',y-10,11)-18
y=para('<link href="https://quint-games.de/hefte/" color="#176954">Zur Lernplattform</link> · Person wählen → Tag 14.',y,11);assert y>45;c.save()
(src/'pdf-layout.json').write_text(json.dumps(heights),encoding='utf8')
audit=['# Tag 14 – Folienabgleich und Quellen','Stand: 16.10.2026. Acht Originalfolien vollständig textlich und in gerenderter Übersicht geprüft.','Original-SHA256: '+hashlib.sha256(original.read_bytes()).hexdigest(),'','## Präzisierungen']+[f'- Folie {s[0]}: {s[7]}' for s in SLIDES if s[7]]+['','## Zuordnung','| Folie | Erklärung | Web-Lernheft |','|---|---|---|']+[f'| {s[0]} | #einfach-{s[0]} | #k{s[0]} |' for s in SLIDES]+['','## Quellen']+[f'- [{t}]({u})' for t,u in SOURCES]
(src/'quellen-und-folienabgleich.md').write_text('\n'.join(audit),encoding='utf8')
print('Tag 14: 8 slides, full web booklet, 15-page PDF with 4 easy Langdock games and coverage map built.')
