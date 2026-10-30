import json
from pathlib import Path
from .content import DATE,SOURCES,SLIDES,VIDEO
from .ideas import IDEAS
from .series import BOOKS,QUIZZES,core_pages
from .simple_day1 import SLIDE_HELP,IDEA_HELP
from .simple_day2 import SLIDE_HELP as SLIDE_HELP2,IDEA_HELP as IDEA_HELP2
from .simple_day3 import SLIDE_HELP as SLIDE_HELP3,IDEA_HELP as IDEA_HELP3,EXTRA_SOURCES
from .day1_web import block as simple_block,organize,quiz_controls,navigation
from .day2_web import block as simple_block2,organize as organize2,navigation as navigation2
from .day3_web import block as simple_block3,organize as organize3,navigation as navigation3,traffic_lab
from tag19.build import block_web,E
NAMES={'ingo':'Ingo','carmen':'Carmen','tabea':'Tabea'}
ORIGINAL='Folien_Modul2_Tag1.pdf'


def embedded_styles(day):
 # Keep the complete reading layout with the document, including when a
 # browser cache, extension, or interrupted request drops external CSS.
 assets=Path(__file__).resolve().parents[3]/'plattform/public/assets'
 css='\n'.join((assets/name).read_text(encoding='utf8') for name in ('toolbook.css','workshop-series.css','modul2.css'))
 if day in (1,2,3):css+='\n'+(assets/'tag1-einfach.css').read_text(encoding='utf8')
 if day==3:css+='\n#extras{scroll-margin-top:5rem}#ampel-status{font:inherit;padding:.6rem;max-width:100%;border:1px solid #547449;border-radius:5px}#ampel-result{padding:1rem;border-left:4px solid #547449;background:#fffdf5}#ampel-result.retry{border-color:#a46b00;background:#f4e9c1}'
 assert '</style' not in css.lower()
 return '<style id="module-reading-layout">'+css+'</style>'

def pages(day=1):
 b=BOOKS[day];result=[]
 for p in core_pages(day):
  blocks=[]
  for k,v in p['blocks']:
   if k=='json':blocks.append(('code',json.dumps(v,ensure_ascii=False,indent=2)))
   elif k=='quiz':
    for i,(q,opts,right,why) in enumerate(QUIZZES[day],1):blocks.append(('p',f'{i}. {q}\n'+'\n'.join(f'{"ABC"[j]}: {opt}' for j,opt in enumerate(opts))))
   else:blocks.append((k,v))
  result.append(dict(p,blocks=blocks))
 chosen=[idea for idea in IDEAS if idea['n'] in b['ideas']]
 step=3 if day in (1,2,3) else 5
 for start in range(0,len(chosen),step):
  group=chosen[start:start+step];blocks=[('p','Nur zum Anschauen: Du musst diese Ideen heute nicht nachbauen. Suche dir höchstens eine aus, die zu deinem Alltag passt. Einige brauchen Wissen aus den nächsten Tagen.' if day in (1,2,3) else 'Diese Ideen gehören zur gesamten Vier-Tage-Reihe. Heute anschauen und passend zum Lernstand auswählen; spätere Testwege sind Ausblick. Kostenlos bedeutet im Rahmen der eigenen Make-Credits. Weitere Dienste und echte Außenaktionen separat prüfen.')]
  for idea in group:
   if day==1:
    title,explain,preview=IDEA_HELP[idea['n']];blocks.extend([('h',f'{idea["n"]:02} · {title}'),('p',explain),('p',preview)])
   elif day==2:
    title,explain,preview=IDEA_HELP2[idea['n']];blocks.extend([('h',f'{idea["n"]:02} · {title}'),('p',explain),('p',preview)])
   elif day==3:
    title,explain,preview=IDEA_HELP3[idea['n']];blocks.extend([('h',f'{idea["n"]:02} · {title}'),('p',explain),('p',preview)])
   else:blocks.extend([('h',f'{idea["n"]:02} · {idea["title"]} · {idea["group"]}'),('p',f'Start: {idea["start"]}. Weg: {idea["steps"]}. Ergebnis: {idea["result"]}'),('p','Kleine Probe: '+idea['test']),('p','Ausbau: '+idea['extras'])])
  result.append(dict(key='ideen-'+str(group[0]['n']),title='Ideen für deinen Bereich',deck=f'Tag {day}/4 · Ideen {group[0]["n"]} bis {group[-1]["n"]} von 30',blocks=blocks,idea_ids=[x['n'] for x in group]))
 assigned=[(n,title,SLIDE_HELP[n] if day==1 else SLIDE_HELP2[n] if day==2 else SLIDE_HELP3[n] if day==3 else detail) for n,title,detail in SLIDES if n in b['slides']]
 slide_step=3 if day in (2,3) else 5
 for start in range(0,len(assigned),slide_step):
  group=assigned[start:start+slide_step]
  result.append(dict(key='folien-'+str(group[0][0]),title='Die heutigen Originalfolien eingeordnet',deck='Tag '+str(day)+'/4 · Originalfolien '+', '.join(str(s[0]) for s in group),blocks=[(kind,v) for n,title,detail in group for kind,v in [('h',f'{n:02} · {title}'),('p',detail.replace('Der erste Tag übt stattdessen denselben Datenweg mit internen Testfeldern.','Die Reihe übt den Datenweg zunächst mit internen Testfeldern.'))]]))
 for start in range(0,len(b['sources']),6):
  lookup={**SOURCES,**EXTRA_SOURCES} if day==3 else SOURCES
  result.append(dict(key='quellen-'+str(start+1),title='Offizielle Quellen zum Nachsehen',deck='Recherche 26.10.2026 · keine Kontoeinrichtung behauptet',blocks=[('p','Diese Herstellerseiten sind zum Nachschlagen, keine zusätzliche Leseaufgabe. Stand: 26.10.2026. Die Klickanleitung wurde anhand der Dokumentation vorbereitet; wir haben keinen Ablauf in deinem Make-Konto ausgeführt. Die Creditbeispiele sind gerechnet. Deinen tatsächlichen Verbrauch prüfst du selbst.' if day==1 else 'Herstellerunterlagen am 26.10.2026 geprüft. Öffentlicher GET-Test separat ausgeführt; keine Make-Szenarien in Teilnehmerkonten angelegt oder ausgeführt. Eigene Beispiele und Sollwerte sind Lernhilfen.')]+[('source',(k,*lookup[k])) for k in b['sources'][start:start+6]]))
 if day==2:
  for item in result:
   if item['key'].startswith('quellen-'):
    item['deck']='Herstelleranleitungen geprüft am 27.10.2026'
    item['blocks'][0]=('p','Diese Seiten sind zum Nachschlagen, keine weitere Aufgabe. Die vier Herstelleranleitungen wurden am 27.10.2026 geprüft. Wir haben keine Szenarien in deinem Make-Konto ausgeführt. Die Creditwerte sind Rechenbeispiele; deinen tatsächlichen Verbrauch siehst du nur in deinem Konto.')
 if day==3:
  for item in result:
   if item['key'].startswith('quellen-'):
    item['deck']='Unterlagen geprüft am 27.10.2026 · Unterricht am 28.10.2026'
    item['blocks'][0]=('p','Nur zum Nachschlagen. Die Anleitungen wurden am 27.10.2026 anhand offizieller Herstellerseiten vorbereitet. Nur der öffentliche RSS-Feed wurde direkt per HTTP gelesen. Kein Szenario wurde in Teilnehmerkonten ausgeführt, keine Google-Verbindung eingerichtet. Creditwerte sind Planwerte.')
 return result

def lab(kind):
 if kind=='credits':return '''<div class="learninglab" id="credit-lab"><h3>Probier die Rechnung hier aus</h3><p>Dieser Rechner ist nur zum Lernen. Er startet nichts in Make und verbraucht keine Credits. Wir rechnen hier mit einem Namen pro Lauf und einem Credit pro ausgeführtem einfachen Baustein.</p><label>Wie viele Bausteine laufen nacheinander? <input id="credit-modules" type="number" min="1" max="20" value="2"></label><label>Wie oft startest du den ganzen Ablauf? <input id="credit-runs" type="number" min="1" max="10000" value="5"></label><button type="button" id="credit-calculate">Credits ausrechnen</button><p id="credit-result" role="status"></p><button type="button" id="polling-example">Zusatz: Warum lassen wir den Zeitplan aus?</button><p id="polling-result" role="status"></p></div>'''
 return '<div class="learninglab" id="json-lab"><h3>Den vereinbarten Filter verstehen</h3><p>Nur eine Browser-Lernhilfe, kein Make-/KI-Aufruf und keine fachliche Freigabe. Erwartet werden projekt als Text, kategorie aus VIDEO/MARKETING/SONSTIGES und freigabe als echter Wahrheitswert.</p><label for="json-input">Deine Testdaten</label><textarea id="json-input" rows="7">'+E(json.dumps(VIDEO,ensure_ascii=False,indent=2))+'</textarea><button type="button" id="json-check">Daten prüfen</button><p id="json-result" role="status"></p><pre id="json-output"></pre></div>'

def shell(pid,title,body,toc,day):
 b=BOOKS[day];links=''.join(f'<li><a href="/hefte/{pid}/modul-2/tag-{d}/"'+(' aria-current="page"' if d==day else '')+f'>{book["weekday"]} · Tag {d}</a></li>' for d,book in BOOKS.items())
 html=f'''<!doctype html><html lang="de" data-person="{pid}" data-tag="{19+day}" data-course-day="{day}" data-module="2"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{NAMES[pid]} · Modul 2 · Tag {day} · {E(title)}</title><link rel="icon" href="/hefte/assets/favicon.svg">{embedded_styles(day)}<script src="/hefte/assets/modul2-tag1.js?v={('tag1-einfach-1' if day==1 else 'vier-tage-1')}" defer></script></head><body><a class="skip" href="#main">Zum Inhalt</a><header><a href="/hefte/{pid}/#modul-2">← Modulübersicht</a><span>{NAMES[pid]} · {b['weekday']} · Tag {day}/4 · {b['date']}</span><a href="/hefte/pdf/{b['pdf']}" download>Tages-PDF</a></header><div class="layout"><nav aria-label="Vier-Tage-Lernreihe"><details open><summary>Modul 2 · Lektion 1 in vier Tagen</summary><ul>{links}</ul><p><a href="/hefte/{pid}/modul-2/tag-{day}/lernheft/">Heutiges Lernheft</a> · <a href="/hefte/material/modul2-tag1/Make-Tag{day}-Starterpaket.zip" download>Heutiges Testmaterial</a></p><ol>{toc}</ol></details></nav><main id="main">{body}</main></div></body></html>'''

 if day==1:
  html=html.replace('/hefte/pdf/'+b['pdf'],'/hefte/pdf/'+b['pdf']+'?v=einfach-2')
  html=html.replace('</head>','<script src="/hefte/assets/tag1-einfach.js?v=1" defer></script></head>')
  if 'class="reading-intro"' in body:
   start=html.index('<nav aria-label=');end=html.index('</nav>',start)+len('</nav>')
   html=html[:start]+'<nav aria-label="Heutiger Lernweg">'+navigation(pid)+'</nav>'+html[end:]
 if day==2:
  html=html.replace('/hefte/pdf/'+b['pdf'],'/hefte/pdf/'+b['pdf']+'?v=tag2-einfach-1')
  html=html.replace('modul2-tag1.js?v=vier-tage-1','modul2-tag1.js?v=tag2-einfach-1')
  html=html.replace('</head>','<script src="/hefte/assets/tag2-einfach.js?v=1" defer></script></head>')
  if 'class="reading-intro"' in body:
   start=html.index('<nav aria-label=');end=html.index('</nav>',start)+len('</nav>')
   html=html[:start]+'<nav aria-label="Heutiger Lernweg">'+navigation2(pid)+'</nav>'+html[end:]
 if day==3:
  html=html.replace('/hefte/pdf/'+b['pdf'],'/hefte/pdf/'+b['pdf']+'?v=tag3-leicht-1')
  html=html.replace('modul2-tag1.js?v=vier-tage-1','modul2-tag1.js?v=tag3-leicht-1')
  html=html.replace('</head>','<script src="/hefte/assets/tag3-leicht.js?v=1" defer></script></head>')
  if 'class="reading-intro"' in body:
   start=html.index('<nav aria-label=');end=html.index('</nav>',start)+len('</nav>')
   html=html[:start]+'<nav aria-label="Heutiger Lernweg">'+navigation3(pid)+'</nav>'+html[end:]
 return html


def render_web(pid,day=1):
 items=pages(day);sections=[]
 for i,p in enumerate(items,1):
  parts=[]
  if p['key']=='quiz':
   if day in (1,2,3):parts.append(quiz_controls())
   for j,(q,opts,right,why) in enumerate(QUIZZES[day],1):parts.append(f'<fieldset data-q="{j}"><legend>{j}. {E(q)}</legend>'+''.join(f'<label><input type="radio" name="q{j}" value="{k}"> {E(opt)}</label>' for k,opt in enumerate(opts))+'<button type="button" data-answer>Antwort prüfen</button><p class="feedback" role="status" hidden></p></fieldset>')
  else:
   for j,(kind,v) in enumerate(p['blocks']):
    ident=f'copy-{i}-{j}'
    if kind=='code' and day==3:parts.append(f'<div class="prompt"><b>RSS-Adresse zum Einfügen in URL</b><pre id="{ident}">{E(v)}</pre><button type="button" data-copy="{ident}">Adresse kopieren</button><span class="copystatus" role="status"></span></div>')
    elif kind=='code' and day==2 and p.get('code_role')=='expected':parts.append('<div class="prompt expected-output"><b>Erwartetes Ergebnis</b><pre>'+E(v)+'</pre><p>Diesen Text liest du in der Ausgabe. Du musst ihn nicht als festen Text in Make einfügen.</p></div>')
    elif kind=='code' and day==2 and p.get('code_role')=='sample':parts.append('<div class="prompt"><b>Nur zum Lesen: ein kleines JSON-Beispiel</b><pre>'+E(v)+'</pre><p>Das vollständige Muster zum Einfügen steht in Schritt 2.</p></div>')
    elif kind=='code' and day==2:parts.append(f'<div class="prompt"><b>Zum Einfügen in JSON string</b><pre id="{ident}">{E(v)}</pre><button type="button" data-copy="{ident}">Nur den JSON-Text kopieren</button><span class="copystatus" role="status"></span></div>')
    elif kind=='code' and day==1:parts.append('<div class="prompt expected-output"><b>Erwartetes Ergebnis</b><pre>'+E(v.split('\n',1)[-1])+'</pre><p>Diesen Satz liest du in der Ausgabe. Du musst ihn hier nicht kopieren.</p></div>')
    elif kind=='code':parts.append(f'<div class="prompt"><b>Testdaten oder Beispiel · Kontext beachten</b><pre id="{ident}">{E(v)}</pre><button type="button" data-copy="{ident}">Kopieren</button><span class="copystatus" role="status"></span></div>')
    else:parts.append(simple_block(kind,v,ident) if day==1 else simple_block2(kind,v,ident) if day==2 else simple_block3(kind,v,ident) if day==3 else block_web(kind,v,ident))
  if day==1 and p['key']=='credits':parts.append(lab('credits'))
  if day==3 and p['key']=='filter':parts.append(traffic_lab())
  for n in p.get('idea_ids',[]):
   if day==1:parts.append('<details class="idea-data" data-idea="'+str(n)+'"><summary>Was muss ich dafür heute tun?</summary><p>Nichts zusätzlich bauen. Überlege nur: Würde mir diese Idee Arbeit sparen? Die Hauptübung bleibt die Begrüßung mit Luna und Mira.</p></details>')
   elif day==2:parts.append('<details class="idea-data" data-idea="'+str(n)+'"><summary>Ist das heute eine weitere Aufgabe?</summary><p>Nein. Der Datenzettel mit zwei Beispielen ist die Hauptübung. Die Ideen helfen dir, später einen passenden eigenen Fall auszuwählen.</p></details>')
   elif day==3:parts.append('<details class="idea-data" data-idea="'+str(n)+'"><summary>Muss ich das auch bauen?</summary><p>Nein. Die Freigabe-Ampel ist die Hauptaufgabe. Wähle danach höchstens eines der beiden leichten Extras.</p></details>')
   else:
    idea=IDEAS[n-1];parts.append('<details class="idea-data" data-idea="'+str(n)+'"><summary>Testdaten für Idee '+str(n)+'</summary><pre>'+E(json.dumps(dict(projekt='Lernversuch',thema=idea['title'],kanal=idea['group'],status='ENTWURF'),ensure_ascii=False,indent=2))+'</pre><p>Für Workflow 2 ab Dienstag anpassen. Das ist ein Briefing-Test, kein vollständiger Ausbau.</p></details>')
  sections.append(f'<section class="chapter" id="k{i}" data-key="{p["key"]}"><p class="eyebrow">{i:02} / {len(items)} · {E(p["deck"])}</p><h2>{E(p["title"])}</h2>'+''.join(parts)+'</section>')
 note_label='Was hast du gemacht? Was kam heraus? Wo brauchst du noch Hilfe?' if day in (1,2,3) else 'Ziel, Eingang, beobachtetes Ergebnis, Verbrauch und offener Punkt'
 sections.append(f'''<section class="chapter"><h2>Mein heutiger Versuch</h2><label for="memo">{note_label}</label><textarea id="memo" rows="6"></textarea><button type="button" id="save-note">Auf diesem Gerät speichern</button><button type="button" id="download-note">Als Text mitnehmen</button><p role="status" id="note-status">Nur in diesem Browser, keine Übertragung an Make.</p></section>''')
 data=json.dumps([dict(right=r,why=w) for q,o,r,w in QUIZZES[day]],ensure_ascii=False).replace('<','\\u003c')
 toc=''.join(f'<li><a href="#k{i}">{i:02} · {E(p["title"])}</a></li>' for i,p in enumerate(items,1))
 content=organize(items,sections) if day==1 else organize2(items,sections) if day==2 else organize3(items,sections) if day==3 else ''.join(sections)
 return shell(pid,BOOKS[day]['title'],content+f'<script type="application/json" id="quiz-data">{data}</script>',toc,day)

def render_day(pid,day=1):
 b=BOOKS[day];items=pages(day);workflow=next(i for i,p in enumerate(items,1) if p['key']==b['workflow']);firstidea=next(i for i,p in enumerate(items,1) if p.get('idea_ids'))
 schedule=''.join(f'<li><a href="/hefte/{pid}/modul-2/tag-{d}/">{book["weekday"]}, {book["date"]}: {E(book["subtitle"])}</a></li>' for d,book in BOOKS.items())
 body=f'''<section class="chapter" id="start"><p class="eyebrow">Modul 2 · Lektion 1 · {b['weekday']}, {b['date']} · Tag {day} von 4</p><h2>{E(b['title'])}</h2><p>{E(b['subtitle'])}. Die Folienlektion ist auf Montag bis Donnerstag verteilt.</p><p><a href="lernheft/">Heutiges Lernheft öffnen →</a> · <a href="/hefte/pdf/{b['pdf']}" download>Heutiges PDF</a></p><aside class="note">Heute nur diese Etappe. Manuell testen und den gemeinsamen Free-Creditverbrauch im Blick behalten. Die anderen Tageshefte sind Vorschau und Material für ihren Unterrichtstag.</aside><p><a href="lernheft/#k{workflow}">Dein heutiger Workflow</a> · <a href="lernheft/#k{firstidea}">Die heutigen {len(b['ideas'])} Ideen</a></p><p><a href="/hefte/material/modul2-tag1/Make-Tag{day}-Starterpaket.zip" download>Heutiges Testmaterial herunterladen</a></p></section><section class="chapter" id="reihe"><h2>Unser Weg bis Donnerstag</h2><ol>{schedule}</ol></section>'''
 if day==1:
  body=f'''<section class="chapter" id="start"><p class="eyebrow">Modul 2 · Montag, 26.10.2026 · Tag 1 von 4</p><h2>Dein erster kleiner Ablauf in Make</h2><p>Du gibst Luna ein. Make macht daraus „Hallo Luna! Willkommen in Modul 2.“ Danach änderst du den Namen zu Mira und prüfst, ob sich die Begrüßung mitändert.</p><p><a href="lernheft/">Hier anfangen: die einfache Schritt-für-Schritt-Anleitung →</a></p><aside class="note">Du brauchst nur deinen vorhandenen kostenlosen Make-Account. Verbinde heute kein E-Mail-Konto und keine KI. Lass den automatischen Zeitplan aus. Die Begriffe werden im Heft erklärt, sobald du sie brauchst.</aside><p><a href="lernheft/#k{workflow}">Ich habe die Erklärung gelesen: direkt zum Bauen</a></p><p><a href="/hefte/pdf/{b['pdf']}" download>Lernheft als PDF</a> · <a href="/hefte/material/modul2-tag1/Make-Tag1-Starterpaket.zip" download>Merkzettel und Testnamen herunterladen</a></p><p>Hauptaufgabe: die Begrüßung bauen und mit zwei Namen prüfen. Die acht Ideen und Folien hinten sind zum Nachlesen, keine acht weiteren Aufgaben.</p></section><section class="chapter" id="reihe"><h2>Heute klein anfangen, bis Donnerstag weiterlernen</h2><ol>{schedule}</ol></section>'''
 if day==2:
  body=f'''<section class="chapter" id="start"><p class="eyebrow">Dienstag, 27.10.2026 · Modul 2 · Tag 2 von 4</p><h1>Aus vier Angaben wird ein klarer Text</h1><p>Heute liest Make einen kleinen beschrifteten Datenzettel und setzt daraus einen übersichtlichen Text zusammen. Du lernst JSON, ohne Programmcode schreiben zu müssen.</p><p><a href="lernheft/">Hier anfangen: die einfache Schritt-für-Schritt-Anleitung →</a></p><aside class="note"><strong>Heute wichtig</strong><p>Nur zwei Bausteine. Ein vorbereiteter Testzettel. Kein Outlook, keine KI und keine Veröffentlichung. Der automatische Zeitplan bleibt aus.</p></aside><p><a href="lernheft/#nachbauen">Direkt zu den sechs Bauschritten</a> · <a href="lernheft/#pruefen">Zum speicherbaren Quiz</a></p><p><a href="/hefte/pdf/{b['pdf']}" download>Lernheft als PDF</a> · <a href="/hefte/material/modul2-tag1/Make-Tag2-Starterpaket.zip" download>Testdaten und Merkzettel herunterladen</a></p><p>Die acht Ideen, weiteren Datentypen und die Outlook-Excel-Vorlage stehen im freiwilligen Zusatzteil. Du musst sie heute nicht zusätzlich nachbauen.</p></section><section class="chapter" id="reihe"><h2>Gestern ein Name, heute vier Angaben</h2><p>Für den Einstieg musst du Tag 1 nicht erneut bauen. Das Tagesheft erklärt die nötigen Wörter noch einmal.</p><ol>{schedule}</ol></section>'''
 if day==3:
  body=f'''<section class="chapter" id="start"><p class="eyebrow">Mittwoch, 28.10.2026 · Modul 2 · Tag 3</p><h1>Eine Regel. Zwei Bausteine. Fertig.</h1><p>Wir machen es ganz klein: FERTIG darf weiter, ENTWURF bleibt stehen. Dafür brauchst du kein JSON, keine KI und keine zusätzliche Anmeldung.</p><p><a href="lernheft/">Die ganz einfache Anleitung öffnen →</a></p><aside class="note"><strong>Deine Hauptaufgabe</strong><p>Zwei bekannte Bausteine, eine Regel und zwei Testfälle. Danach bist du fertig.</p></aside><p><a href="lernheft/#extras">Freiwillig: eine Schlagzeile holen oder eine Idee speichern</a> · <a href="lernheft/#pruefen">Zum speicherbaren Quiz</a></p><p><a href="/hefte/pdf/{b['pdf']}" download>Das einfache PDF</a> · <a href="/hefte/material/modul2-tag1/Make-Tag3-Starterpaket.zip" download>Kurzen Merkzettel herunterladen</a></p><p>Router, Webhooks und die große KI-Kette stehen nur zum Nachlesen im Zusatzteil. Sie sind keine Pflichtübungen.</p></section><section class="chapter" id="reihe"><h2>Unser Weg bis Donnerstag</h2><ol>{schedule}</ol></section>'''
 body+=f'<section class="chapter" id="folien"><h2>Die heute zugeordneten Originalfolien</h2><p>Heute: '+', '.join(map(str,b['slides']))+'. Alle 34 Seiten werden genau einem Tag zugeordnet. Im vollständigen Original bleibt alles unverändert erhalten.</p><p><a href="/hefte/folien/tag-20/'+ORIGINAL+'">Vollständige Original-PDF öffnen</a></p>'
 for n,title,detail in SLIDES:
  if n in b['slides']:body+=f'<details class="original" id="folie-{n}"><summary>{n:02} · {E(title)}</summary><p>{E(SLIDE_HELP[n] if day==1 else SLIDE_HELP2[n] if day==2 else SLIDE_HELP3[n] if day==3 else detail)}</p><a href="/hefte/folien/tag-20/{ORIGINAL}#page={n}"><img loading="lazy" src="/hefte/folien/tag-20/{n:02}.jpg" alt="Originalfolie {n}: {E(title)}"></a></details>'
 return shell(pid,b['title'],body+'</section>','<li><a href="#start">Heute</a></li><li><a href="#reihe">Vier-Tage-Plan</a></li><li><a href="#folien">Heutige Folien</a></li>',day)
