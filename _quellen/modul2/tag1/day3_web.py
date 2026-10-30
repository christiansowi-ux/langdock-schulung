from .day1_web import block as common_block

def block(kind,value,ident):
 html=common_block(kind,value,ident)
 for label in ['Equal to','FERTIG','ENTWURF']:
  html=html.replace(label,'<strong>'+label+'</strong>')
 return html

def traffic_lab():
 return '''<div class="learninglab" id="ampel-lab"><h3>Erst hier ohne Make ausprobieren</h3><label for="ampel-status">Welchen Status schickst du zur Tür?</label><select id="ampel-status"><option value="FERTIG">FERTIG</option><option value="ENTWURF">ENTWURF</option></select><button type="button" id="ampel-test">Die eine Regel testen</button><p id="ampel-result" role="status">Wähle einen Status. Die Regel lautet: Nur FERTIG darf weiter.</p><p>Das ist nur eine Lernhilfe im Browser. Kein Make-Aufruf, keine Veröffentlichung und kein Creditverbrauch.</p></div>'''

def organize(items,sections):
 bykey={p['key']:s for p,s in zip(items,sections)}
 groups=[('verstehen','1 · Verstehen','Eine Regel. Mehr musst du dir zunächst nicht merken.',['start','filter']),('nachbauen','2 · Nachbauen','Vier kleine Schritte mit bekannten Bausteinen.',['wf3','wf3-text','wf3-filter','wf3-test','hilfe']),('pruefen','3 · Prüfen','Vier leichte Fragen und dein Merkzettel.',['quiz','antworten','mitnahme'])]
 intro='''<div class="reading-intro"><p class="eyebrow">Mittwoch, 28.10.2026 · Modul 2 · Tag 3</p><h1>Eine Regel. Zwei Bausteine. Fertig.</h1><p>FERTIG geht weiter. ENTWURF bleibt stehen. Das ist dein Hauptziel.</p><div class="today-important"><strong>Ganz klein anfangen:</strong> Kein JSON. Keine KI. Keine neue Anmeldung. Erst die Freigabe-Ampel bauen, danach höchstens ein freiwilliges Extra.</div><div class="reading-route"><a href="#verstehen">1. Verstehen</a><a href="#nachbauen">2. Nachbauen</a><a href="#pruefen">3. Prüfen</a><a href="#extras">Leichte Extras</a></div></div>'''
 used=set();body=[intro]
 for ident,title,desc,keys in groups:
  part=[]
  for key in keys:
   used.add(key);html=bykey[key]
   if key=='antworten':html='<details class="answer-help"><summary>Lösungen kurz nachlesen</summary>'+html+'</details>'
   part.append(html)
  if ident=='pruefen':part.append(sections[-1])
  body.append(f'<div class="lesson-part" id="{ident}"><div class="part-heading"><p class="phase-title">{title}</p><p>{desc}</p></div>'+''.join(part)+'</div>')
 used.update(['rss','rss-text','ideen-speicher'])
 body.append('<section class="lesson-part" id="extras"><div class="part-heading"><p class="phase-title">Nur wenn du möchtest: ein leichtes Extra</p><p>Wähle eines. Nicht alles nacheinander bauen.</p></div><details class="extra-reading"><summary>Ohne neue Anmeldung: eine Schlagzeile holen</summary>'+bykey['rss']+bykey['rss-text']+'</details><details class="extra-reading"><summary>Mit vorhandenem Google-Konto: eine Idee speichern</summary>'+bykey['ideen-speicher']+'</details></section>')
 extra=''.join(bykey[p['key']] for p in items if p['key'] not in used)
 body.append('<details class="extra-reading" id="zusatz"><summary>Nur nachlesen: Folien, weitere Ideen und schwierige Begriffe</summary><p>Das ist keine weitere Bauaufgabe für Mittwoch.</p>'+extra+'</details>')
 return ''.join(body)

def navigation(pid):
 return f'''<p class="nav-today">Mittwoch ganz leicht</p><ol class="today-nav"><li><a href="#verstehen">1 · Verstehen<small>Nur eine Regel</small></a></li><li><a href="#nachbauen">2 · Nachbauen<small>Vier kleine Schritte</small></a></li><li><a href="#pruefen">3 · Prüfen<small>Quiz speichern</small></a></li></ol><p><a href="#extras">Freiwillig: zwei leichte Extras</a></p><p><a href="#zusatz">Die Folien einfach erklärt</a></p><p><a href="/hefte/{pid}/modul-2/tag-3/">Zur Tagesübersicht</a></p><p class="nav-hint">Achte auf „Mach das“, „Kurz prüfen“ und die gelben Hinweise. Ein Stopp bei ENTWURF ist richtig.</p>'''
