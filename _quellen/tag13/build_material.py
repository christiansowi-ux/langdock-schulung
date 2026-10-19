from pathlib import Path
import sys,json,shutil,html,hashlib
import fitz
ROOT=Path(__file__).resolve().parents[2]
Q=ROOT/'_quellen';PUBLIC=ROOT/'plattform/public';sys.path.insert(0,str(Q))
from einfach_tag13 import SLIDES,SOURCES,CHAPTERS
from kurs_tag13 import TAG13
E=html.escape
src=Q/'tag13';src.mkdir(exist_ok=True)
original=PUBLIC/'folien/tag-13/Folien_Tag13.pdf'
if not original.exists(): original=Path.home()/'Downloads/DSGVO.pdf'
doc=fitz.open(original)
dest=PUBLIC/'folien/tag-13';dest.mkdir(parents=True,exist_ok=True)
if original.resolve() != (dest/'Folien_Tag13.pdf').resolve(): shutil.copy2(original,dest/'Folien_Tag13.pdf')
for i,p in enumerate(doc,1):
    for width,prefix in [(1440,''),(360,'t')]:
        target=dest
        pix=p.get_pixmap(matrix=fitz.Matrix(width/p.rect.width,width/p.rect.width),alpha=False)
        from PIL import Image
        Image.frombytes('RGB',[pix.width,pix.height],pix.samples).save(target/f'{prefix}{i:02d}.jpg',quality=90)
fol=json.loads((Q/'folien.json').read_text(encoding='utf-8'))
fol['13']=dict(pdf='DSGVO.pdf',n=len(doc),ratio=round(doc[0].rect.width/doc[0].rect.height,4),slides=[dict(n=i,links=[]) for i in range(1,75)])
(Q/'folien.json').write_text(json.dumps(fol,ensure_ascii=False,indent=1),encoding='utf-8')
parts=['<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Lernheft Tag 13 – DSGVO</title>{{HEAD}}</head><body class="lh">{{BAR}}',
 '<section class="lp cover"><img class="logo" src="{{LOGO}}" alt="Futureway KI Institut"><p class="kicker">Tag 13 · Lektion 12 · 15.10.2026</p><div class="big" style="font-size:64pt">Daten mit<br>Köpfchen.</div><div class="big2">Datenschutz<br>zum Verstehen.</div><p class="sub">74 Folien in verständlichen Worten. Mit erfundenen Beispielen, Fragen zum Mitdenken und klar markierten Präzisierungen.</p><span class="note">{{ICON:book}} Eine Folie, ein Gedanke. Man muss nicht alles am Stück lesen.</span></section>']
for n,title,simple,points,example,q,a,correction,articles in SLIDES:
    parts.append(f'<section class="lp" id="k{n}"><div class="kh"><span class="kn">{n:02}</span><div><p class="kk">Originalfolie {n} · DSGVO</p><h2>{E(title)}</h2></div>{{{{UX:{n}}}}}</div><p class="lead">{E(simple)}</p><ul>'+''.join(f'<li style="margin-bottom:3mm">{E(x)}</li>' for x in points)+f'</ul><div class="fall" style="display:block"><h4>Ausgedachtes Beispiel</h4><p>{E(example)}</p></div>'+ (f'<div class="card"><h4>Präzisierung zur Folie</h4><p>{E(correction)}</p></div>' if correction else '')+f'<div class="merk"><span class="ml">Erst selbst überlegen</span><p>{E(q)}</p></div><details><summary>Eine mögliche Antwort</summary><p>{E(a)}</p></details><p class="small">Fundstelle: {E(articles) if articles else "Einführung / Lernbegleitung"}. <a href="/hefte/folien/tag-13/Folien_Tag13.pdf#page={n}">Originalfolie {n}</a> · <a href="#quellen">Quellen</a></p></section>')
parts.append('<section class="lp" id="quellen"><div class="kh"><h2>Quellen und Einordnung</h2></div><p>Geprüft am 15.10.2026. Bildungsunterlage, keine Rechtsberatung.</p><ul>'+''.join(f'<li><a href="{E(u)}">{E(t)}</a></li>' for t,u in SOURCES)+'</ul></section></body></html>')
(src/'lernheft.html').write_text('\n'.join(parts),encoding='utf-8')
cfg=dict(src='tag13/lernheft.html',out='Tag 13 - DSGVO',pdf=TAG13['lernheft'],kurz='DSGVO',label='Lernheft · DSGVO – Daten mit Köpfchen',titles={s[0]:s[1] for s in SLIDES})
f=Q/'lernheft.py';text=f.read_text(encoding='utf-8')
if "13: {'src': 'tag13/" not in text:
    text=text.replace('    # Praxishefte:', '    13: '+repr(cfg)+',\n    # Praxishefte:');f.write_text(text,encoding='utf-8')
audit=['# Tag 13 – DSGVO: Quellen und Folienabgleich','Stand: 15.10.2026. Original-PDF unverändert, 74 Seiten; jede Seite textlich und in gerenderter Übersicht gesichtet.','Original SHA-256: '+hashlib.sha256(original.read_bytes()).hexdigest(),'## Quellen']
audit += [f'- [{t}]({u})' for t,u in SOURCES]
audit += ['## Folienbezogene Präzisierungen']+[f'- Folie {s[0]}: {s[7]} (Fundstelle: {s[8]})' for s in SLIDES if s[7]]
audit += ['## Vollständige Zuordnung','| Folie | Erklärung / Web-Lernheft | Inhalte |','|---|---|---|']+[f'| {s[0]} | #einfach-{s[0]} / #k{s[0]} | {s[1]} |' for s in SLIDES]
(src/'quellen-und-korrekturen.md').write_text('\n'.join(audit),encoding='utf-8')
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
out=ROOT/cfg['out'];out.mkdir(exist_ok=True);pdf=out/cfg['pdf'];c=canvas.Canvas(str(pdf),pagesize=(595.276,841.89));c.setTitle('Tag 13 – DSGVO: Daten mit Köpfchen');c.setAuthor('Futureway KI Institut')
ink='#183f35';W=499
def para(text,y,size=11,font='Body',color=ink,leading=None):
    st=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.42,textColor=HexColor(color))
    p=Paragraph(text,st);_,h=p.wrap(W,800);p.drawOn(c,48,y-h);return y-h
def page(no,kicker):
    c.setFillColor(HexColor('#faf7ee'));c.rect(0,0,596,842,fill=1,stroke=0)
    c.setFillColor(HexColor(ink));c.rect(0,808,596,34,fill=1,stroke=0);c.setFont('Bold',9);c.setFillColor(HexColor('#ffffff'));c.drawString(48,821,'FUTUREWAY KI INSTITUT · TAG 13 · DSGVO')
    c.setFillColor(HexColor(ink));c.setFont('Body',9);c.drawString(48,25,'Lernbegleitung · 15.10.2026 · Beispiele erfunden');c.drawRightString(547,25,str(no));return para(E(kicker),780,10,'Bold')-18
y=page(1,'DIE DATENSCHUTZ-WERKSTATT');y=para('Daten mit<br/>Köpfchen.',y,49,'Bold',leading=52)-24;y=para('74 Folien. Verständliche Worte.<br/>Viele kleine Aha-Momente.',y,22,'Bold')-22
y=para('Dieses Heft begleitet jede Folie der Lektion 12. Man liest einen Gedanken, probiert das Beispiel im Kopf aus und beantwortet die Frage, bevor man die mögliche Antwort liest.',y)-14
y=para('Die interaktive Werkstatt enthält Daten-Detektiv, Prompt-Labor und Posteingang. Alles funktioniert mit vorbereiteten, erfundenen Fällen und ohne Agent-Zugang.',y)-18
for t,a,b in CHAPTERS:y=para(f'<b>{a:02}–{b:02}</b>  {E(t)}',y,10)-5
y=para('Originalfolien bleiben unverändert. Fachliche Präzisierungen sind klar markiert. Bildungsangebot, keine rechtliche Freigabe.',y-12,10);assert y>40,y;c.showPage()
page_heights=[]
for n,title,simple,points,example,q,a,correction,articles in SLIDES:
    y=page(n+1,f'FOLIE {n:02} / 74 · ERST VERSTEHEN, DANN WEITER')
    y=para(E(title),y,24,'Bold',leading=28)-16;y=para(E(simple),y,13,'Bold')-17
    for p in points:y=para('• '+E(p),y,10.5)-7
    y=para('<b>Ausgedachtes Beispiel</b><br/>'+E(example),y-7,11)-13
    if correction:y=para('<b>Präzisierung zur Originalfolie</b><br/>'+E(correction),y,10,color='#755016')-13
    y=para('<b>Erst selbst überlegen:</b> '+E(q),y,11)-10
    y=para('<b>Eine mögliche Antwort:</b> '+E(a),y,10.5)-14
    y=para('Fundstelle: '+E(articles or 'Einführung / Lernbegleitung')+'. Quellen auf Seite 76.',y,8.5,color='#4c6359')
    assert y>45,(n,y);page_heights.append((n,round(y,1)));c.showPage()
y=page(76,'QUELLEN · NICHT ALLES IST EINE AMTLICHE QUELLE');y=para('Nachlesen. Nachfragen.<br/>Selbst erklären.',y,27,'Bold')-20
for title,url in SOURCES:y=para(f'<b>{E(title)}</b><br/><link href="{E(url)}" color="#1a6b5a">Quelle öffnen</link>',y,11)-17
y=para('Quellenabgleich: 15.10.2026. Rechtliche Regeln sind vom konkreten Einsatz abhängig. Das Trust Center ist eine Anbieterquelle; geschützte Vertragsunterlagen wurden nicht abgerufen. Die Originalvorlage heißt DSGVO.pdf, 74 Folien, Ausgabe Juli 2026.',y-8,10)-15
y=para('Auf der Plattform: <link href="https://quint-games.de/hefte/" color="#1a6b5a">quint-games.de/hefte</link><br/>Person wählen → Tag 13 → Demos oder Einfach erklärt.',y,11);assert y>45,y;c.save()
scratch=Path(__file__).parent;(scratch/'pdf-layout.json').write_text(json.dumps(page_heights))
# Generated files remain in the project; copy deliverables separately when needed.
print('Tag13: 74 original slides + thumbnails, full web companion, 76-page PDF and coverage map created.')
