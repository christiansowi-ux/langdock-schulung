"""Reading order and emphasis for today's beginner lesson only."""
import re
from tag19.build import E,block_web

def text(value):
 result=E(value)
 for word in ['Run once','Variable name','Variable value','Variable lifetime','One execution','Set variable','Compose a string','On demand']:
  result=result.replace(word,'<strong>'+word+'</strong>')
 return result.replace('\n','<br>')

def block(kind,value,ident):
 if kind=='p':
  lines=value.splitlines()
  if lines and all(re.match(r'^\d+\. ',line) for line in lines):
   return '<ol class="do-steps">'+''.join('<li>'+text(re.sub(r'^\d+\. ','',line))+'</li>' for line in lines)+'</ol>'
  return '<p class="p">'+text(value)+'</p>'
 if kind=='h':
  name='do-heading' if value=='Mach das' else 'result-heading' if value=='So sieht es richtig aus' else 'help-heading' if value.startswith('Falls') else ''
  return '<h3 class="'+name+'">'+E(value)+'</h3>'
 if kind=='note':return '<aside class="note"><strong>Wichtig</strong><p>'+text(value)+'</p></aside>'
 if kind=='check':return '<aside class="check"><strong>Kurz prüfen</strong><p>'+text(value)+'</p></aside>'
 return block_web(kind,value,ident)

def quiz_controls():
 return '''<div class="quiz-save" data-quiz-persist><p><strong>Deine Antworten bleiben erhalten.</strong> Sie werden bei jeder Auswahl automatisch in diesem Browser gespeichert. Das gilt für dieses Gerät und diesen Teilnehmerzugang, nicht für andere Geräte.</p><p id="quiz-storage-status" role="status">Speicher wird geprüft …</p><p id="quiz-progress" role="status"></p><button type="button" id="quiz-save">Quizstand jetzt speichern</button><button type="button" id="quiz-download">Quizstand als Text herunterladen</button><p>Falls dein Browser das Speichern blockiert, kannst du den Stand als Text mitnehmen.</p></div>'''

def organize(items,sections):
 bykey={p['key']:s for p,s in zip(items,sections)}
 groups=[('verstehen','1 · Verstehen','Lerne nur die Begriffe, die du heute brauchst.',['start','automation','anatomie','free','credits','oberflaeche','mapping']),('nachbauen','2 · Nachbauen','Ein kleiner Schritt nach dem anderen. Erst das Ergebnis prüfen, dann weiter.',['wf1','wf1-einzeltest','wf1-text','wf1-ergebnis','wf1-test','hilfe']),('pruefen','3 · Prüfen und behalten','Vier Fragen, dein Merkzettel und der gespeicherte Quizstand.',['quiz','antworten','mitnahme'])]
 intro='''<div class="reading-intro"><p class="eyebrow">Heute · Modul 2 · Tag 1</p><h1>Dein erster Ablauf in Make</h1><p>Ein Name rein. Eine Begrüßung raus. Du wirst durch jeden Schritt geführt.</p><div class="today-important"><strong>Heute wichtig:</strong> Nur zwei Bausteine bauen. Mit Luna und Mira testen. Den automatischen Zeitplan aus lassen.</div><div class="reading-route"><a href="#verstehen">1. Verstehen</a><a href="#nachbauen">2. Nachbauen</a><a href="#pruefen">3. Prüfen</a></div></div>'''
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
 body.append('<details class="extra-reading" id="zusatz"><summary>Freiwillig: weitere Begriffe, acht Ideen, Folien und Quellen</summary><p>Die Hauptaufgabe ist erledigt. Hier kannst du später nachlesen. Es sind keine zusätzlichen Pflichtaufgaben für heute.</p>'+extra+'</details>')
 return ''.join(body)

def navigation(pid):
 return f'''<p class="nav-today">Dein Lernweg für heute</p><ol class="today-nav"><li><a href="#verstehen">1 · Verstehen<small>Einfach erklärt</small></a></li><li><a href="#nachbauen">2 · Nachbauen<small>Fünf kleine Schritte</small></a></li><li><a href="#pruefen">3 · Prüfen<small>Quiz und Merkzettel</small></a></li></ol><p><a href="#zusatz">Freiwillig nachlesen</a></p><p><a href="/hefte/{pid}/modul-2/tag-1/">Zur Tagesübersicht</a></p><p class="nav-hint">Achte auf „Mach das“, „So sieht es richtig aus“ und die gelben Hinweise.</p>'''
