"""The familiar reading layout, with Tuesday's content and navigation."""
from .day1_web import block as common_block

def block(kind,value,ident):
 html=common_block(kind,value,ident)
 for label in ['Parse JSON','JSON string','Data structure']:
  html=html.replace(label,'<strong>'+label+'</strong>')
 return html

def organize(items,sections):
 bykey={p['key']:s for p,s in zip(items,sections)}
 groups=[('verstehen','1 · Verstehen','Vier beschriftete Angaben statt eines einzelnen Namens.',['start','wiedereinstieg','json','json-regeln','mapping','budget']),('nachbauen','2 · Nachbauen','Sechs kleine Schritte. Nach jeder Probe siehst du, was angekommen sein soll.',['wf2','wf2-daten','wf2-felder','wf2-text','wf2-ergebnis','wf2-test','hilfe']),('pruefen','3 · Prüfen und behalten','Vier Fragen, ein Merkzettel und dein gespeicherter Quizstand.',['quiz','antworten','mitnahme'])]
 intro='''<div class="reading-intro"><p class="eyebrow">Dienstag, 27.10.2026 · Modul 2 · Tag 2</p><h1>Aus vier Angaben wird ein klarer Text</h1><p>JSON lesen, Felder auswählen, Ergebnis prüfen. Du wirst durch jeden Schritt geführt.</p><div class="today-important"><strong>Heute wichtig:</strong> Ein Testzettel, zwei Bausteine. Keine KI, kein Instagram-Konto, kein Versand. Der automatische Zeitplan bleibt aus.</div><div class="reading-route"><a href="#verstehen">1. Verstehen</a><a href="#nachbauen">2. Nachbauen</a><a href="#pruefen">3. Prüfen</a></div></div>'''
 used=set();body=[intro]
 for ident,title,desc,keys in groups:
  part=[]
  for key in keys:
   used.add(key);html=bykey[key]
   if key=='antworten':html='<details class="answer-help"><summary>Lösungen und Erklärungen nachlesen</summary>'+html+'</details>'
   part.append(html)
  if ident=='pruefen':part.append(sections[-1])
  body.append(f'<div class="lesson-part" id="{ident}"><div class="part-heading"><p class="phase-title">{title}</p><p>{desc}</p></div>'+''.join(part)+'</div>')
 extra=''.join(bykey[p['key']] for p in items if p['key'] not in used)
 body.append('<details class="extra-reading" id="zusatz"><summary>Freiwillig: Datentypen, Outlook-Excel-Beispiel, acht Ideen und Folien</summary><p>Die Hauptübung ist erledigt. Hier kannst du nachlesen. Die Outlook-Verbindung ist keine weitere Pflichtaufgabe.</p>'+extra+'</details>')
 return ''.join(body)

def navigation(pid):
 return f'''<p class="nav-today">Dein Lernweg für Tag 2</p><ol class="today-nav"><li><a href="#verstehen">1 · Verstehen<small>JSON wie einen Zettel lesen</small></a></li><li><a href="#nachbauen">2 · Nachbauen<small>Sechs kleine Schritte</small></a></li><li><a href="#pruefen">3 · Prüfen<small>Quiz und Merkzettel</small></a></li></ol><p><a href="#zusatz">Freiwillig nachlesen</a></p><p><a href="/hefte/{pid}/modul-2/tag-2/">Zur Tagesübersicht</a></p><p><a href="/hefte/{pid}/modul-2/tag-1/lernheft/">Tag 1 noch einmal ansehen</a></p><p class="nav-hint">Achte auf „Mach das“, „So sieht es richtig aus“ und die gelben Hinweise.</p>'''
