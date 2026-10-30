"""Eine Folienlektion, vier aufeinander aufbauende Unterrichtstage, 26.–29.10.2026."""
from copy import deepcopy
from .content import PAGES as BASE, PDF, SOURCES, SLIDES, DATE
from .ideas import IDEAS
from .simple_day1 import core as simple_core, QUIZ as SIMPLE_QUIZ
from .simple_day2 import core as simple_core2, QUIZ as SIMPLE_QUIZ2
from .simple_day3 import core as simple_core3, QUIZ as SIMPLE_QUIZ3
BOOKS={
 1:dict(date='26.10.2026',weekday='Montag',title='Make verstehen und klein anfangen',subtitle='Grundlagen, Free-Budget und dein Begrüßungs-Mixer',pdf=PDF,out='Modul 2 - KI-Automation/Lektion 1 - Make-Einstieg',slides=list(range(1,12)),keys=['automation','anatomie','free','credits','oberflaeche','mapping','wf1','wf1-test'],ideas=list(range(1,9)),sources=['M1','M2','M3','M4','M5','M6','M7','M15'],workflow='wf1'),
 2:dict(date='27.10.2026',weekday='Dienstag',title='Daten verstehen und richtig weitergeben',subtitle='JSON, Mapping und dein Mini-Redaktionsbriefing',pdf='Lernheft_Modul2_Tag2_Daten-und-Mapping.pdf',out='Modul 2 - KI-Automation/Lektion 1 - Tag 2 Daten und Mapping',slides=list(range(12,17))+list(range(24,28)),keys=['json','wf2','wf2-test','outlook'],ideas=list(range(9,17)),sources=['M3','M6','M8','M14'],workflow='wf2'),
 3:dict(date='28.10.2026',weekday='Mittwoch',title='Anfragen kontrolliert weiterleiten',subtitle='Filter, Freigaben, Webhooks und die Rolle der KI',pdf='Lernheft_Modul2_Tag3_Filter-und-KI.pdf',out='Modul 2 - KI-Automation/Lektion 1 - Tag 3 Filter und KI',slides=list(range(17,24))+list(range(28,31)),keys=['filter','wf3','webhook','ki-schritt','ki-pruefen','kontakt'],ideas=list(range(17,24)),sources=['M2','M8','M9','M10','M12'],workflow='wf3'),
 4:dict(date='29.10.2026',weekday='Donnerstag',title='Verbinden, prüfen und sauber abschließen',subtitle='Test-API, Zeitangaben und ein nachvollziehbarer eigener Ablauf',pdf='Lernheft_Modul2_Tag4_API-Zeit-und-Abschluss.pdf',out='Modul 2 - KI-Automation/Lektion 1 - Tag 4 API Zeit und Abschluss',slides=list(range(31,35)),keys=['wf4','wf4-test','zeit','qualitaet'],ideas=list(range(24,31)),sources=['M1','M2','M3','M7','M11','M13','M14','J1'],workflow='wf4'),
}
QUIZZES={
1:[('Was ist ein Szenario?',['Nur der letzte Text','Der gesamte festgelegte Ablauf','Ein bezahltes KI-Modell'],1,'Ein Szenario verbindet die einzelnen Schritte zu einem Arbeitsweg.'),('Mira steht im ersten Modul, aber Luna bleibt in der Begrüßung. Was prüfst du zuerst?',['Ob Luna fest eingetippt wurde','Ob ein KI-Modell fehlt','Ob der Rechner neu gestartet werden muss'],0,'Der letzte Baustein muss den aktuellen Mapping-Wert verwenden.'),('Zwei einfache Module, ein Bundle, fünf vollständige Läufe: Planwert?',['2 Credits','10 Credits','Immer 0 Credits'],1,'Zwei ausgeführte Module mal fünf Läufe ergeben unter diesen Annahmen zehn Credits.'),('Wie üben wir heute?',['Dauerbetrieb jede Minute','Mit einem echten Kundensystem','Manuell mit Run once und Testnamen'],2,'Ein kleiner manueller Versuch hält Ergebnis und Verbrauch überschaubar.')],
2:[('Was macht Parse JSON?',['Es zerlegt passenden JSON-Text in Felder','Es garantiert richtige Geschäftsdaten','Es veröffentlicht einen Beitrag'],0,'Lesbares Format und fachlich richtige Werte sind unterschiedliche Dinge.'),('Welcher Wert ist ein echter Wahrheitswert?',['"true" als Text','true ohne Anführungszeichen','"ja vielleicht"'],1,'JSON unterscheidet Text von Boolean-Werten.'),('Du änderst das Thema im JSON, aber die Ausgabe bleibt alt. Was prüfen?',['Ob Mapping und aktueller Lauf stimmen','Ob ein größeres Abo nötig ist','Ob alle Daten gelöscht werden müssen'],0,'Ein fest getippter Text oder ein alter Ergebnis-Kreis zeigt nicht den neuen Eingang.'),('Braucht jeder den Outlook-Excel-Aufbau?',['Ja, Make liefert Microsoft 365 mit','Nein, heute gibt es einen internen kostenlosen Ersatz','Ja, sonst kann man Mapping nicht lernen'],1,'Weitere Konten und Rechte sind Voraussetzung der Originalintegration, nicht unseres Testwegs.')],
3:[('Der Filter verlangt VIDEO AND freigabe=true. Was passiert bei VIDEO und false?',['Weiter zur Textausgabe','Am Filter stoppen','Make setzt false auf true'],1,'Bei AND müssen beide Bedingungen erfüllt sein.'),('Zwei Router-Bedingungen passen. Was kann passieren?',['Beide Wege können laufen','Automatisch nur einer','Keiner, Router sind nur Dekoration'],0,'Normale Router-Routen müssen bei Bedarf ausdrücklich gegenseitig ausgeschlossen werden.'),('Gültiges JSON beweist eine richtige KI-Kategorie?',['Ja, immer','Nein, Inhalt und erlaubte Werte separat prüfen','Nur bei maximaler Temperatur'],1,'Format, Wertebereich und tatsächliche Bedeutung benötigen getrennte Prüfungen.'),('Was ist ein Webhook?',['Ein geheimer KI-Prompt','Ein kostenloses Mailkonto','Ein HTTPS-Eingang für Ereignisdaten'],2,'Ein Webhook ist ein Benachrichtigungsweg; er ersetzt nicht jede API.')],
4:[('Die Test-API liefert HTTP 200 und completed=false. Was bedeutet das?',['Die Abfrage schlug fehl','Die Abfrage kann erfolgreich sein; die Testaufgabe ist unerledigt','Make hat kein Guthaben'],1,'Technische Ausführung und Inhalt der gelesenen Daten unterscheiden.'),('Was bedeutet das Z in einem Zeitstempel?',['UTC','Immer Berliner Ortszeit','Zukünftiger Termin'],0,'Z steht für UTC. Die Ortsanzeige hängt von der Zone und dem Datum ab.'),('Was macht formatDate?',['Es erstellt immer einen Kalendereintrag','Es zeigt einen Datumswert als formatierten Text','Es bestätigt einen Kundentermin'],1,'Formatieren ist eine Umwandlung zur Anzeige, keine externe Terminaktion.'),('Was gehört in eine ehrliche Übergabe?',['Nur ein grünes Symbol','Nur der Name des Tools','Testdaten, Soll/Ist, beobachteter Verbrauch und offene Punkte'],2,'Die nächste Person muss nachvollziehen können, was tatsächlich geprüft wurde.')]
}
ENTRIES={
1:['Grundlagen der KI-Automatisierung und Abgrenzung zu agentischen Arbeitsweisen.','Einführung in Make: Szenarien, Module, Ausführungen und Datenfluss.','Free-Account, Creditbudget und kontrollierte manuelle Testläufe.','Erster kleiner Workflow mit Variablen und gemappten Textausgaben.','Ergebnisprüfung mit verändertem Testnamen und dokumentiertem Lernstand.'],
2:['Strukturierte Daten und grundlegende JSON-Datentypen verstehen.','Daten mit Parse JSON in nutzbare Felder zerlegen.','Mapping und Wiederverwendung am Beispiel eines Redaktionsbriefings.','Outlook-Excel-Beispiel der Folien samt Zugängen und Voraussetzungen einordnen.','Varianten, fehlerhafte Eingaben und nachvollziehbare Übergabe prüfen.'],
3:['Filter, Vergleichsoperatoren sowie AND- und OR-Bedingungen anwenden.','Freigaben und kontrollierte Weiterleitung an einer Videoanfrage prüfen.','Router und Webhooks als Erweiterungen von Arbeitsabläufen verstehen.','KI-Klassifikation, Prompt-Rollen und strukturierte Antworten einordnen.','Formularintegration, Unsicherheit und menschliche Prüfung vor externen Aktionen.'],
4:['Öffentliche Test-API mit einem lesenden HTTP-Abruf verstehen.','Antwortstatus, Dateninhalt und Fehlerfälle unterscheiden.','Zeitstempel, Zeitzonen und Datumsformatierung nachvollziehen.','Kleine Abläufe auf Eingabe, Ergebnis und Creditverbrauch prüfen.','Ergebnisse dokumentieren, sichern und einen passenden Anwendungsfall auswählen.']}
QUIZZES[1]=SIMPLE_QUIZ
QUIZZES[2]=SIMPLE_QUIZ2
QUIZZES[3]=SIMPLE_QUIZ3
BOOKS[3]['title']='Die einfache Freigabe-Ampel'
BOOKS[3]['sources']=['M2','M5','M9','M10','M12','R1','G1','G2','N1']

def page(key,title,blocks,day,section='Lernweg'):
 b=BOOKS[day];return dict(key=key,title=title,deck=f'Modul 2 · Lektion 1 · Tag {day}/4 · {b["weekday"]}, {b["date"]} · {section}',blocks=blocks)

def core_pages(day):
 if day==1:return simple_core(page)
 if day==2:return simple_core2(page)
 if day==3:return simple_core3(page)
 b=BOOKS[day];base={p['key']:p for p in BASE};result=[]
 plan=[['Montag, 26.10.','Make-Grundlagen und ein Begrüßungs-Mixer.'],['Dienstag, 27.10.','JSON, Mapping und ein Redaktionsbriefing.'],['Mittwoch, 28.10.','Filter, Freigaben, Webhooks und KI-Einordnung.'],['Donnerstag, 29.10.','Test-API, Zeitangaben, Prüfung und Abschluss.']]
 result.append(page('start',b['title'],[('p',b['subtitle']+'. Die eine Originallektion wird über vier Unterrichtstage bearbeitet. Heute gilt nur die markierte Etappe; die anderen Themen folgen an ihrem Tag.'),('table',(['Vier Tage, ein roter Faden','Schwerpunkt'],plan)),('note',f'Heute: {b["weekday"]}, {b["date"]}, Tag {day} von 4. Herstellerrecherche vom 26.10.2026. Die ersten drei Tagesworkflows benötigen nur Make Free; am Donnerstag kommt optional ein öffentlicher GET-Abruf ohne Zusatzkonto hinzu. Keine bezahlte KI-API nötig.'),('p','Die 30 Ideen sind auf die Hefte verteilt: 8 + 8 + 7 + 7. Sie sind Anregungen für die ganze Reihe, keine zusätzlichen heutigen Pflichtaufgaben. Die vollständige unveränderte Original-PDF bleibt verlinkt; die Begleitung zeigt jeweils nur die heute zugeordneten Folien.')],day,'Deine heutige Etappe'))
 if day>1:
  result.append(page('wiedereinstieg','Mit deinem letzten Ergebnis weitergehen',[
   ('p',{2:'Gestern hast du einen Namen gemappt. Heute bekommen mehrere Angaben feste Feldnamen. Nimm deinen kurzen Testzettel mit; du musst den alten Ablauf nicht neu bauen.',3:'Gestern wurde aus JSON ein Briefing. Heute entscheiden klare Bedingungen, welche Angaben weitergehen dürfen. Beginne mit dem gültigen JSON aus dem Starterpaket.',4:'Gestern hast du Freigaben und Grenzen geprüft. Heute liest du optional eine öffentliche Testquelle, verstehst Zeitangaben und schließt deinen kleinen Ablauf nachvollziehbar ab.'}[day]),
   ('check','Erkläre in zwei Sätzen Quelle, Verarbeitung und Ergebnis deiner letzten Übung. Ein grünes Häkchen ersetzt keine Erklärung.'),
   ('note','Wenn du den vorherigen Tag verpasst hast: Die Tages-Testdateien und die beschriebenen Sollwerte erlauben einen Einstieg. Sie sind Referenzen, kein Beleg für einen selbst ausgeführten Lauf.')],day,'Anknüpfen'))
 for key in b['keys']:
  p=deepcopy(base[key]);p['deck']=page(key,p['title'],[],day)['deck']
  p['blocks']=[(k,v.replace('Die 30 Ideen hinten liefern weitere Themen für genau dieses kleine Muster.','Die Ideen der Reihe liefern weitere Themen für dieses Muster.').replace('Für den ersten Tag keine echten Postfächer verbinden oder dauerhaft aktivieren.','Für diesen kostenlosen Lernweg keine echten Postfächer verbinden oder dauerhaft aktivieren.').replace('vorhandene Free-Credits nutzen','vorhandene Free-Credits nutzen')) if isinstance(v,str) else (k,v) for k,v in p['blocks']]
  if key=='credits':p['blocks']=[(k,v.replace('Unser Lernbudget: höchstens 50 Credits als selbst gewählte Grenze, etwa 10 Credits pro Übung plus 10 Reserve.','Unser Lernbudget für die gesamte Vier-Tage-Reihe: höchstens 50 Credits als selbst gewählte Grenze, etwa 10 pro Tagesworkflow plus 10 Reserve.')) if isinstance(v,str) else (k,v) for k,v in p['blocks']]
  result.append(p)
 if day==2:
  result.append(page('daten-check','Ein Päckchen oder eine ganze Liste?',[
   ('p','Unser Redaktionsbriefing verwendet genau ein JSON-Objekt. Eine Liste kann dagegen mehrere Bundles erzeugen; der nächste Baustein arbeitet dann möglicherweise mehrfach. Wir bleiben heute bei einem klaren einzelnen Fall.'),
   ('table',(['Prüffall','Was du erwartest'],[['Ein gültiges Objekt mit vier Feldern','Ein korrekt zugeordnetes Briefing.'],['Neues Projekt und neuer Kanal','Nur die gemappten Werte ändern sich.'],['Kaputtes JSON','Sichtbarer Fehler statt scheinbar fertigem Ergebnis.']])),
   ('check','Notiere den tatsächlich beobachteten Verbrauch. Der gestrige Zweierlauf und der heutige Zweierlauf können dieselbe Modulzahl haben, aber andere Inhalte.'),
   ('note','Noch keine großen Listen, Schleifen oder echten Kundendaten. Erst wenn ein einzelnes Päckchen nachvollziehbar ist, lohnt sich der Ausbau.')],day,'Vertiefen'))
 if day==3:
  result.append(page('filter-check','Vier kleine Fälle statt eines Zufallstreffers',[
   ('table',(['kategorie / freigabe','Erwartung beim vereinbarten Filter'],[['VIDEO / true','Weiter zur internen Planungsnotiz.'],['VIDEO / false','Stoppen.'],['MARKETING / true','Stoppen.'],['SONSTIGES / false','Stoppen.']])),
   ('p','Ändere im gültigen JSON nur diese beiden Werte. Verwende jedes Mal den aktuellen vollständigen Lauf zur Kontrolle. Ein gestoppter Fall darf im letzten Baustein keine neue Ausgabe erzeugen.'),
   ('check','Erkläre, welche Bedingung den Fall aufhält. Eine Freigabe ist im Beispiel ein Testwert; eine echte geschäftliche Freigabe benötigt einen nachvollziehbaren zuständigen Menschen.'),
   ('note','Die Browser-Lernhilfe kann dieselbe Regel vormachen, ist aber weder ein Make-Lauf noch eine echte Freigabe. Weitere Tests verbrauchen gegebenenfalls zusätzliche Credits.')],day,'Prüfen'))
 if day==4:
  result.append(page('zeit-praxis','Eine Zeitangabe lesbar ausgeben',[
   ('p','Freiwillige Erweiterung nach dem API-Versuch: In einem eigenen manuellen Mini-Szenario Tools → Set variable hinzufügen, name: zeitpunkt. Im Wert über die Funktionsauswahl now einsetzen. Danach Tools → Compose a string mit einer formatierten Ausgabe des gemappten Datumswerts ergänzen.'),
   ('code','Funktionsprinzip in Make:\nformatDate(gemappter Datumswert; "DD.MM.YYYY HH:mm"; "Europe/Berlin")'),
   ('p','„Gemappter Datumswert“ ist hier eine Erklärung, kein einzutippender Funktionsparameter. Das Feld aus dem ersten Modul über die Oberfläche einsetzen. Kontrolliere die lokale Uhrzeit gegen die gewählte Zone und notiere, wann du den Test ausgeführt hast.'),
   ('check','Es entsteht lesbarer Text in der Modulausgabe, kein Kalendereintrag. Der API-Datensatz /todos/1 enthält kein Terminfeld; ein solcher Termin darf daraus nicht erfunden werden.'),
   ('note','Diese zusätzliche Zweierübung ist optional und hat eigene Credits. Vorher Restbudget prüfen. Gemeinsames Lehrbudget für die Reihe bleibt 50 Credits als Planungsgrenze, keine Kontosperre.')],day,'Optional vertiefen'))
 result.append(page('quiz','Vier Entscheidungen zum heutigen Tag',[('quiz',None),('p','Im Web kannst du nach einer Begründung erneut versuchen. Im PDF folgt die Auflösung. Die Fragen prüfen Begriffe und Denkwege, nicht die Einrichtung deines Kontos.')],day,'Selbstcheck'))
 result.append(page('antworten','Die Antworten mit Denkweg',[('p',f'{i}. {"ABC"[r]} · {why}') for i,(q,o,r,why) in enumerate(QUIZZES[day],1)]+[('check','Erkläre eine Antwort mit deinem eigenen kleinen Tagesbeispiel.')],day,'Nachsehen'))
 nexttext={1:'Morgen: Aus einzelnen Angaben werden JSON-Felder und ein kleines Redaktionsbriefing.',2:'Morgen: Ein Filter entscheidet, ob eine freigegebene Videoanfrage weitergehen darf.',3:'Morgen: Öffentliche Testdaten lesen, Zeitangaben verstehen und Ergebnisse sichern.',4:'Nach der Reihe: einen begrenzten eigenen Anwendungsfall mit erlaubten Testdaten auswählen; weitere Konten oder echte Außenaktionen separat prüfen.'}[day]
 result.append(page('mitnahme','Deine Tagesübergabe',[
  ('h','Fünf Stichpunkte für das Klassenbuch'),('p','\n'.join('• '+v for v in ENTRIES[day])),
  ('h','Was ich wirklich beobachtet habe'),('p','Mein Eingang und Ziel: _________________________________\nMein Ergebnis: ________________________________________\nGeprüfter zweiter Fall: __________________________________\nCredits vorher / nachher: _______________________________\nOffener Punkt: _________________________________________'),('note',nexttext)],day,'Mitnehmen'))
 return result

def course(day):
 b=BOOKS[day];brief=('Eine Regel, zwei Bausteine und zwei freiwillige leichte Extras.' if day==3 else b['subtitle']+f'. Tag {day} der gemeinsamen Folienlektion, Make Free und passende Branchenideen.');return dict(titel=b['title'],unter=f'Modul 2 · Lektion 1 · Tag {day}/4',datum=b['date'],modul=2,lektion=1,modul_tag=day,url=f'modul-2/tag-{day}/',custom_lesson=True,kurz=brief,lernheft=b['pdf'],learnings=[dict(id=f'l{i}',folie=0,satz=p['title'],erklaert=next((v for k,v in p['blocks'] if k=='p'),p['title'])) for i,p in enumerate(core_pages(day),1)],karten=[],test=[],begriffe=[])

assert sorted(n for b in BOOKS.values() for n in b['slides'])==list(range(1,35))
assert sorted(n for b in BOOKS.values() for n in b['ideas'])==list(range(1,31))
