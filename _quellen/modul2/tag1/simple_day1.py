"""Day one: explain one small, observable example before adding vocabulary."""

QUIZ=[
 ('Was ist in Make ein Szenario?',['Nur der fertige Begrüßungstext','Der ganze Ablauf mit seinen verbundenen Bausteinen','Ein zusätzliches KI-Abo'],1,'Das Szenario ist der ganze Ablauf. Die einzelnen Kreise darin heißen Module.'),
 ('Du änderst Luna im ersten Baustein zu Mira. Trotzdem steht im neuen Ergebnis Luna. Was prüfst du zuerst?',['Ob Luna im Text fest eingetippt ist','Ob du eine KI bezahlen musst','Ob du einen neuen Computer brauchst'],0,'Der zweite Baustein soll den Namen vom ersten übernehmen. Fest eingetippter Text verändert sich nicht von selbst.'),
 ('Ein Name wird durch zwei einfache Bausteine geschickt. Ein solcher Lauf braucht geplant 2 Credits. Wie viele brauchen fünf gleiche Läufe?',['2 Credits','10 Credits','0 Credits'],1,'Fünfmal zwei sind zehn. Das ist eine Rechnung für unser einfaches Beispiel. Den echten Verbrauch liest du im Konto ab.'),
 ('Wie startest du unsere Übung?',['Du lässt sie jede Minute laufen','Du verbindest sofort ein Kundenpostfach','Du klickst bewusst auf Run once und benutzt einen Testnamen'],2,'Run once heißt: einmal starten. Wir üben mit erfundenen Namen und ohne Versand an andere Menschen.'),
]

def core(make_page):
 def p(key,title,blocks,section='Schritt für Schritt'):
  return make_page(key,title,blocks,1,section)
 return [
 p('start','Heute baust du deine erste kleine Automatisierung',[
  ('p','Du gibst einen Namen ein. Make setzt diesen Namen in eine Begrüßung ein. Mehr muss dein erster Ablauf heute noch nicht können.'),
  ('flow',['Du gibst Luna ein.','Make übernimmt den Namen.','Als Ergebnis steht dort: Hallo Luna! Willkommen in Modul 2.']),
  ('h','Am Ende kannst du drei Dinge'),
  ('p','1. Zwei Bausteine in Make verbinden.\n2. Einen Namen automatisch in einen Text einsetzen.\n3. Den Namen ändern und prüfen, ob sich der Text mitändert.'),
  ('note','Lies zuerst die Erklärungen und baue dann in Ruhe mit. Du brauchst nur deinen Make-Free-Account. Keine Zahlungsdaten, kein KI-Abo und kein E-Mail-Konto verbinden.'),
  ('h','So findest du dich im Heft zurecht'),
  ('p','„Mach das“ ist dein nächster Schritt. „So sieht es richtig aus“ beschreibt das erwartete Ergebnis. „Falls es nicht klappt“ hilft dir weiter. Die Begriffe werden dort erklärt, wo du sie brauchst.'),
  ('p','Das ist Tag 1 von 4. Daten und JSON kommen Dienstag, Filter und KI Mittwoch, APIs und Zeitangaben Donnerstag. Die Ideen und Folienerklärungen hinten sind zum Nachlesen. Du musst heute keine acht zusätzlichen Aufgaben erledigen.')], 'Dein Ziel für heute'),
 p('automation','Was heißt eigentlich automatisieren?',[
  ('p','Stell dir vor, du begrüßt immer wieder neue Menschen. Jedes Mal tippst du fast denselben Satz. Nur der Name ändert sich: „Hallo Luna!“ oder „Hallo Mira!“.'),
  ('p','Beim Automatisieren legst du einmal fest: Nimm diesen Namen und setze ihn in diesen Satz ein. Danach kann Make dieselben Schritte mit einem anderen Namen wiederholen. Du baust also einen wiederverwendbaren Arbeitsablauf.'),
  ('h','Make ist das Werkzeug für diesen Ablauf'),
  ('p','Du verbindest sichtbare Bausteine auf einer Arbeitsfläche. Ein Baustein hält den Namen bereit. Der nächste baut daraus den Begrüßungstext. Du brauchst dafür heute keinen Programmcode.'),
  ('h','Wo kommt KI ins Spiel?'),
  ('p','Für „Hallo“ plus Name ist keine KI nötig. Eine KI wäre zum Beispiel hilfreich, wenn sie aus langen Notizen einen Textentwurf machen soll. Dann muss ein Mensch prüfen, ob der Entwurf stimmt.'),
  ('note','Ein automatisch erzeugtes Ergebnis ist nicht automatisch richtig. Steht der falsche Name am Anfang, kann auch die Begrüßung den falschen Namen enthalten.'),
  ('check','Erkläre den Ablauf in einem Satz: „Make nimmt ___ und macht daraus ___.“')]),
 p('anatomie','Die Kreise in Make sind deine Bausteine',[
  ('flow',['Baustein 1: Name merken','Baustein 2: Begrüßung zusammensetzen','Ergebnis im zweiten Baustein lesen']),
  ('table',(['Wort in Make','Das bedeutet es hier'],[['Scenario / Szenario','Dein gesamter Ablauf mit beiden Bausteinen.'],['Module / Modul','Ein einzelner Baustein, also ein Kreis auf der Arbeitsfläche.'],['Run once','Einmal starten. Make führt den Ablauf einmal aus.'],['Input / Output','Input ist die Eingabe. Output ist das Ergebnis eines Bausteins.']])),
  ('p','Du musst die englischen Wörter nicht auswendig lernen. Suche beim Nachbauen einfach nach den Namen, die im Heft stehen.'),
  ('h','Wie beginnt so ein Ablauf?'),
  ('p','Heute startest du selbst mit Run once. Später kann zum Beispiel eine neue Anfrage den Ablauf auslösen. Ein solcher Startbaustein heißt Trigger. Heute brauchst du keinen zusätzlichen Trigger.'),
  ('note','Run once heißt nicht „nur so tun als ob“. Wäre ein E-Mail-Versand eingebaut, könnte er wirklich senden. Unsere Übung zeigt nur Text in Make an.')]),
 p('free','Was du mit deinem kostenlosen Konto machst',[
  ('p','Öffne deinen vorhandenen Make-Free-Account. Für die heutige Übung reicht er aus. Du musst kein anderes Programm anschließen.'),
  ('table',(['Dein Free-Account','Was das für dich bedeutet'],[['1.000 Credits pro Monat','Das ist dein monatliches Guthaben für ausgeführte Schritte. Alle deine Abläufe teilen sich dieses Guthaben.'],['Bis zu zwei aktive Szenarien','Arbeite die Übungen nacheinander durch. Lösche keine fremden oder wichtigen Abläufe, um Platz zu schaffen.'],['Geplante Wiederholung frühestens alle 15 Minuten','Das betrifft einen regelmäßigen Zeitplan. Unsere Übung startest du selbst mit Run once.']])),
  ('h','Diese Einstellung ist heute wichtig'),
  ('p','Die automatische Planung bleibt ausgeschaltet. Wenn „On demand“ angezeigt wird, heißt das hier: Du startest bei Bedarf selbst. Prüfe die Planung, bevor du testest.'),
  ('note','Kostenloser Account bedeutet nicht: Jeder Versuch kostet 0 Credits. Wir bezahlen für den beschriebenen Testweg nichts zusätzlich, verbrauchen aber vorhandene Credits. Schau vor und nach dem Üben in deine Verbrauchsanzeige. Es gelten die Werte in deinem Konto. [M1, M7]')]),
 p('credits','Credits einfach erklärt: dein Guthaben für Schritte',[
  ('p','Denk an Credits wie an Guthabenpunkte. Wenn Make einen einfachen Baustein ausführt, braucht das gewöhnlich einen Credit. Unsere Übung verarbeitet immer nur einen Namen auf einmal.'),
  ('table',(['Was du ausführst','Geplanter Verbrauch'],[['Nur den ersten Baustein einmal testen','1 Credit'],['Beide Bausteine einmal durchlaufen lassen','2 Credits'],['Beide Bausteine fünfmal durchlaufen lassen','5 × 2 = 10 Credits']])),
  ('p','Im Heft steht manchmal „Bundle“. Das heißt: ein zusammengehöriges Datenpäckchen. Bei uns ist das der eine Name. Kommen später mehrere Päckchen an, kann derselbe Baustein mehrfach arbeiten und mehr Guthaben verbrauchen.'),
  ('h','Was kostet unser heutiger Versuch ungefähr?'),
  ('p','Erster Baustein allein: 1. Danach beide mit Luna: 2. Danach beide mit Mira: 2. Zusammen sind das geplant 5 Credits. Weitere Versuche oder Fehler können zusätzliche Credits brauchen.'),
  ('note','Das sind Rechenbeispiele, keine Messung deines Kontos. Andere Bausteine, besonders KI-Aufrufe, können anders zählen. Für alle vier Unterrichtstage zusammen planen wir höchstens 50 Credits ein. Diese selbst gesetzte Grenze ist keine automatische Sperre in Make.'),
  ('p','Die Lernhilfe darunter rechnet nur im Browser. Sie führt keinen Make-Ablauf aus und verbraucht keine Make-Credits. Der Zusatzknopf zeigt: Alle 15 Minuten nachsehen wären 4 Abfragen pro Stunde, also 4 × 24 × 30 = 2.880 im Monat. Deshalb lassen wir die automatische Planung aus. [M2, M3]')]),
 p('oberflaeche','Zuerst: einen leeren Ablauf öffnen',[
  ('h','Mach das'),
  ('p','1. Öffne Make und melde dich mit deinem vorhandenen Konto an.\n2. Gehe links zu Scenarios. Das bedeutet „Szenarien“, also deine Arbeitsabläufe.\n3. Wähle Create a new scenario oder die entsprechend benannte Schaltfläche für einen neuen Ablauf.\n4. Gib dem Ablauf den Namen: M2-01 Begruessungs-Mixer.\n5. Lass die automatische Planung aus. Speichere deinen Ablauf.'),
  ('h','So sieht es richtig aus'),
  ('p','Du siehst eine leere Arbeitsfläche mit einer Möglichkeit, über ein Plus den ersten Baustein hinzuzufügen. Die Fläche heißt manchmal Canvas. Das ist nur ein anderes Wort für Arbeitsfläche.'),
  ('h','Falls es nicht klappt'),
  ('p','Du siehst schon einen fertigen Ablauf? Dann bearbeite ihn nicht einfach weiter. Gehe zurück und öffne einen neuen. Make zeigt ein Konto- oder Aktivierungslimit? Frage nach, statt bestehende wichtige Abläufe zu löschen.'),
  ('note','Manche Beschriftungen unterscheiden sich je nach Sprache und Oberfläche. Die englischen Suchnamen der Bausteine stehen deshalb genau im Heft.')]),
 p('mapping','Der wichtigste Unterschied: tippen oder übernehmen?',[
  ('p','Du kannst „Hallo Luna!“ vollständig eintippen. Dann bleibt Luna im Text stehen, auch wenn der erste Baustein inzwischen Mira enthält.'),
  ('p','Oder du tippst nur die festen Teile und wählst den Namen aus dem ersten Baustein aus. Dann übernimmt Make immer den Namen aus dem aktuellen Lauf. Dieses Auswählen und Übernehmen heißt Mapping.'),
  ('table',(['So baust du den Text','Was bei einem neuen Namen passiert'],[['Alles fest eintippen: Hallo Luna!','Luna bleibt stehen.'],['Hallo tippen + Namenswert auswählen + ! tippen','Aus Luna wird Mira, wenn vorne Mira steht.']])),
  ('h','Woran erkennst du den übernommenen Namen?'),
  ('p','Im Textfeld erscheint der ausgewählte Wert als farbiges Feld. Farbe und Beschriftung können unterschiedlich aussehen. Wichtig ist: Du hast das Feld aus dem ersten Baustein angeklickt. Du hast nicht selbst [vorname] oder Luna als Ersatz dafür eingetippt.'),
  ('check','Merksatz: Was ich fest tippe, bleibt fest. Was ich aus dem ersten Baustein auswähle, kann sich mit dessen Wert ändern.')]),
 p('wf1','Schritt 1: Make soll sich Luna merken',[
  ('p','Unser erster Baustein ist ein kleiner beschrifteter Zettel: Auf dem Zettel steht „vorname“. Sein Inhalt ist „Luna“. So einen benannten Wert nennt man Variable.'),
  ('h','Mach das'),
  ('p','1. Klicke auf das Plus für den ersten Baustein.\n2. Suche die App Tools. Das heißt „Werkzeuge“.\n3. Wähle darin Set variable. Das heißt: einen benannten Wert festlegen.\n4. Trage bei Variable name genau vorname ein.\n5. Trage bei Variable value genau Luna ein.\n6. Falls Variable lifetime angezeigt wird: One execution wählen. Der Wert wird dann für diesen Durchlauf bereitgehalten.\n7. Bestätige den Baustein und speichere den Ablauf.'),
  ('table',(['Feld','Was du eingibst'],[['Variable name','vorname'],['Variable value','Luna'],['Variable lifetime, falls sichtbar','One execution']])),
  ('h','Warum zwei verschiedene Felder?'),
  ('p','vorname ist die Beschriftung des Zettels. Luna ist der Inhalt. Beim zweiten Versuch änderst du nur den Inhalt zu Mira; die Beschriftung vorname bleibt gleich.'),
  ('note','Tools benötigt für diesen Versuch keine Verbindung zu einem anderen Konto. Falls du eine Anmeldung bei einer zusätzlichen App einrichten sollst, prüfe, ob du wirklich Tools → Set variable gewählt hast.')]),
 p('wf1-einzeltest','Schritt 2: Prüfen, ob der Name angekommen ist',[
  ('h','Mach das'),
  ('p','1. In deinem Ablauf ist bisher nur der erste Baustein.\n2. Klicke auf Run once. Das heißt „einmal ausführen“.\n3. Warte, bis der Lauf beendet ist.\n4. Öffne die kleine Ergebnis-Anzeige am ausgeführten Baustein. Sie wird häufig als weißer Kreis mit einer Zahl angezeigt.\n5. Suche bei Output, also der Ausgabe, nach deinem Wert Luna.'),
  ('h','So sieht es richtig aus'),
  ('p','In der Ausgabe steht Luna. Das bedeutet: Der erste Baustein hat den Namen bereitgestellt. Noch gibt es keinen Begrüßungstext, denn der zweite Baustein fehlt noch.'),
  ('h','Falls es nicht klappt'),
  ('p','Kein Ergebnis-Kreis zu sehen? Prüfe, ob du Run once wirklich gestartet hast. Eine Fehlermeldung? Öffne sie und lies sie, statt mehrfach auf Start zu klicken. Ein anderer Name? Prüfe Variable value und starte nach der Korrektur erneut.'),
  ('note','Diese Einzelprobe ist geplant 1 Credit. Notiere den tatsächlichen Verbrauch in deinem Konto. Du musst nicht nach jedem Klick starten; nur beim ausdrücklich beschriebenen Test.')]),
 p('wf1-text','Schritt 3: Den Begrüßungstext zusammensetzen',[
  ('h','Mach das'),
  ('p','1. Ergänze rechts hinter dem ersten Baustein über das Plus einen zweiten.\n2. Wähle Tools → Compose a string. Das heißt: einen Text zusammensetzen.\n3. Klicke in das Feld Text. Tippe zuerst Hallo und danach ein Leerzeichen.\n4. Wähle im Auswahlfenster den Namenswert aus dem ersten Baustein. In unserem Beispiel enthält er Luna.\n5. Tippe hinter das farbige Feld: ! Willkommen in Modul 2.\n6. Bestätige den zweiten Baustein und speichere.'),
  ('flow',['Fester Text: Hallo plus Leerzeichen','Ausgewähltes Feld: Name aus Baustein 1','Fester Text: ! Willkommen in Modul 2.']),
  ('h','So sieht es richtig aus'),
  ('p','Zwischen „Hallo “ und „!“ steht im Eingabefeld ein ausgewähltes, farbiges Datenfeld. Es ist die Verbindung zum ersten Baustein. Die Erklärung „Name aus Baustein 1“ hier im Heft sollst du nicht als Text eintippen.'),
  ('h','Falls das Namensfeld nicht zur Auswahl steht'),
  ('p','Prüfe zuerst, ob beide Bausteine verbunden sind und ob dein erster Test Luna als Ausgabe gezeigt hat. Klicke dann erneut in das Textfeld und öffne die Feldauswahl des ersten Bausteins. Nicht einfach Luna als Ersatz eintippen. [M5, M6]')]),
 p('wf1-ergebnis','Schritt 4: Deine erste Begrüßung lesen',[
  ('h','Mach das'),
  ('p','1. Prüfe: Beide Bausteine sind verbunden und die automatische Planung ist aus.\n2. Speichere und klicke auf Run once. Jetzt laufen beide Bausteine nacheinander.\n3. Öffne die Ergebnis-Anzeige am zweiten Baustein.\n4. Lies dessen Ausgabe.'),
  ('code','So soll die Ausgabe lauten:\nHallo Luna! Willkommen in Modul 2.'),
  ('h','Was hat Make gerade gemacht?'),
  ('p','Der erste Baustein stellte Luna bereit. Der zweite nahm diesen Wert und setzte ihn zwischen die festen Textteile. Eine KI wurde dabei nicht gebraucht.'),
  ('check','Steht der vollständige Satz da? Sind der Name und die Leerzeichen richtig? Ein grünes Häkchen sagt nur, dass der Schritt technisch durchlief. Ob der Text passt, kontrollierst du selbst.'),
  ('note','Dieser vollständige Lauf kostet in unserem einfachen Rechenbeispiel 2 Credits. Zusammen mit der ersten Einzelprobe sind es geplant 3. Das Ergebnis steht nur in Make. Es wurde keine Nachricht verschickt.')]),
 p('wf1-test','Schritt 5: Aus Luna wird Mira',[
  ('p','Jetzt kommt der wichtigste Test: Kann dein Ablauf wirklich einen anderen Namen übernehmen?'),
  ('h','Mach das'),
  ('p','1. Öffne den ersten Baustein Set variable.\n2. Ändere nur Variable value: Aus Luna wird Mira.\n3. Lass Variable name auf vorname stehen.\n4. Bestätige und speichere. Den zweiten Baustein veränderst du nicht.\n5. Starte den ganzen Ablauf erneut mit Run once.\n6. Öffne die aktuelle Ausgabe des zweiten Bausteins.'),
  ('code','Jetzt soll dort stehen:\nHallo Mira! Willkommen in Modul 2.'),
  ('h','Warum dieser Test so wichtig ist'),
  ('p','Wenn sich der Name im Ergebnis ohne Änderung des zweiten Bausteins mitändert, hast du den Wert richtig übernommen. Genau dafür baut man einen wiederverwendbaren Ablauf.'),
  ('check','Erkläre es in eigenen Worten: „Den Namen ändere ich in ___. Der zweite Baustein ___.“'),
  ('note','Mit dieser zweiten vollständigen Probe sind es insgesamt geplant 5 Credits. Danach bist du mit der Hauptübung fertig. Lass die automatische Planung aus und speichere deinen Ablauf.')]),
 p('hilfe','Falls dein Ergebnis anders aussieht',[
  ('table',(['Was du siehst','Was du als Nächstes prüfst'],[['Weiterhin Hallo Luna!','Ist Luna im zweiten Baustein fest getippt? Wähle dort stattdessen den Namenswert aus dem ersten Baustein.'],['Hallo ! ohne Namen','Steht im ersten Baustein wirklich Mira? Ist dessen Namensfeld im zweiten ausgewählt?'],['Hallo [vorname]!','[vorname] wurde als Text getippt. Entferne es und wähle das echte Datenfeld aus.'],['HalloMira! ohne Abstand','Füge hinter dem festen Wort Hallo ein Leerzeichen ein.'],['Du siehst ein altes Ergebnis','Öffne die Ausgabe des neuesten Laufs. Frühere Ausgaben ändern sich nachträglich nicht.']])),
  ('p','Korrigiere immer erst den vermuteten Fehler und starte dann gezielt neu. So verstehst du die Ursache und verbrauchst weniger Credits als mit vielen zufälligen Versuchen.'),
  ('note','Zusatz für später: Ein leerer Name kann technisch einen Text wie „Hallo !“ ergeben. Das wäre trotzdem kein guter Begrüßungstext. Darum lernen wir später, fehlende Angaben zu erkennen. Heute musst du dafür keinen weiteren Ablauf bauen.')]),
 p('agent','Noch ein Folienbegriff: Workflow oder Agent?',[
  ('p','Workflow bedeutet Arbeitsablauf. Bei unserer Übung hast du jeden Schritt selbst festgelegt: erst den Namen bereitstellen, dann den Text zusammensetzen. Make folgt diesem Weg.'),
  ('p','Ein KI-Agent bekommt eher ein Ziel, zum Beispiel: „Finde aus diesen freigegebenen Unterlagen Antworten auf meine Frage.“ Er kann innerhalb seiner erlaubten Möglichkeiten weitere Schritte auswählen. Deshalb muss man auch seine Schritte und Antworten prüfen.'),
  ('table',(['Fester Ablauf','KI-Agent'],[['Du legst den Weg vorher fest.','Er kann innerhalb seiner Möglichkeiten Schritte zum Ziel auswählen.'],['Unser Beispiel: Name → Begrüßung.','Beispiel: passende Unterlagen suchen → Antwort entwerfen.']])),
  ('p','Manche Werkzeuge verbinden beide Arbeitsweisen. Ein fester Ablauf kann auch einen KI-Schritt enthalten. KI kann zum Beispiel einen Text entwerfen, während die restlichen Schritte fest vorgegeben sind.'),
  ('note','KI kann auch bei gleicher Frage unterschiedliche Antworten geben. Ein guter Prompt allein beweist nicht, dass die Antwort stimmt. Prüfe Inhalt und Format und teste auch schwierige Beispiele. Ein Mensch entscheidet über wichtige Freigaben.')], 'Zum Verstehen, keine Zusatzaufgabe'),
 p('quiz','Vier einfache Fragen zu deinem Ablauf',[
  ('quiz',None),('p','Versuche es zuerst selbst. Im Web erklärt „Antwort prüfen“ die Lösung. Deine Auswahl und die geprüften Antworten werden in diesem Browser gespeichert; eine Anzeige sagt dir, ob das geklappt hat. Im PDF stehen die Lösungen auf der nächsten Seite. Du darfst nachlesen und es erneut versuchen.')], 'Dein kurzer Selbstcheck'),
 p('antworten','Die Lösungen mit einfachen Erklärungen',[
  ('p',f'{i}. Antwort {"ABC"[right]}: {why}') for i,(_,_,right,why) in enumerate(QUIZ,1)
 ]+[('check','Erkläre jemandem ohne Make-Erfahrung: Was ist der erste Baustein? Was macht der zweite? Warum hast du auch Mira ausprobiert?')], 'Nachsehen'),
 p('mitnahme','Das kannst du jetzt - und so geht es weiter',[
  ('h','Dein eigener kurzer Merkzettel'),
  ('p','Mein erster Baustein heißt: __________________________\nDarin stand zuerst: __________________________________\nMein zweiter Baustein macht: __________________________\nBeim zweiten Test kam heraus: ________________________\nMein echter Verbrauch laut Konto: _____________________\nHier brauche ich noch Hilfe: __________________________'),
  ('h','Für heute reicht das'),
  ('p','Du kannst einen Namen bereitstellen, ihn in einen Text übernehmen und das Ergebnis mit einem zweiten Namen prüfen. Das ist eine kleine, echte Automatisierung. Du musst sie heute nicht mit E-Mail, KI oder einem Kundensystem verbinden.'),
  ('note','Morgen nehmen wir mehrere Angaben statt nur eines Namens. Daraus entsteht ein kleiner übersichtlicher Zettel für einen Beitrag. JSON wird dann von Grund auf erklärt. Die Ideen und Folien hinten kannst du bei Bedarf nachlesen.')], 'Dein Abschluss'),
 ]

SLIDE_HELP={
 1:'Hier beginnt Modul 2. In dieser Lektion lernst du über vier Tage, wie wiederkehrende Arbeitsschritte automatisch ablaufen können. Die Originalfolien sind aus Juli 2026; die ergänzenden Herstellerangaben wurden am 26.10.2026 geprüft.',
 2:'Die Einstiegsfrage lautet sinngemäß: Was stellst du dir unter Automatisierung vor? Unser leichtes Beispiel ist eine Begrüßung, bei der Make einen Namen übernimmt.',
 3:'Der Kurs geht schrittweise weiter: erst Grundlagen, dann Automatisierung und Softwareentwicklung, später eigene Projekte und Beispiele für den Beruf. Du musst diese späteren Themen heute noch nicht beherrschen.',
 4:'Automatisierung heißt: Ein vorher festgelegter Weg wird wiederholt ausgeführt. Ein KI-Schritt kann darin vorkommen, ist aber nicht für jede Aufgabe nötig. Unsere Begrüßung funktioniert ohne KI.',
 5:'Bei einem Workflow legst du den Weg fest. Ein Agent kann innerhalb seiner erlaubten Möglichkeiten Schritte zu einem Ziel auswählen. Werkzeuge können beides verbinden. Beide brauchen passende Kontrollen.',
 6:'Viele Abläufe haben dieselbe Grundidee: etwas startet, Angaben kommen herein, sie werden verarbeitet und ein Ergebnis entsteht. Bei uns: Run once starten, Name bereitstellen, Begrüßung bauen, Text nachlesen.',
 7:'Die Wörter beschreiben Teile des Weges: Trigger = Startauslöser, Modul = Baustein, Mapping = Wert aus einem früheren Baustein auswählen, Run = Durchlauf. Bei KI kommen dazu: Modell = die verwendete KI, Prompt = ihr Auftrag, feste Antwortfelder = eine vorher vereinbarte Ordnung der Antwort. Wichtige Ergebnisse prüft und bestätigt ein Mensch.',
 8:'KI kann unterschiedlich antworten. Bitte um ein klares Format, prüfe die erlaubten Angaben und teste schwierige Fälle. Der Einstellwert „Temperatur“ beeinflusst die Auswahl von Antworten, ist aber kein Schalter für Wahrheit. Auch korrekt aufgebauter Antworttext kann inhaltlich falsch sein.',
 9:'Die Folie zeigt verschiedene Werkzeuge zum damaligen Stand. Wir starten mit Make, weil du dort den Ablauf aus sichtbaren Bausteinen zusammensetzen kannst. Nicht jede gezeigte Funktion oder jedes andere Werkzeug ist automatisch kostenlos.',
 10:'Wähle zunächst eine kleine, häufig wiederkehrende Aufgabe mit gut prüfbarem Ergebnis. Die Frage ist: Welche Schritte sparen dir Arbeit? Rechne den Verbrauch mit ein. Bei Make heißt das Guthaben heute Credits; alte Angaben zu „Operations“ allein reichen zur Preisplanung nicht aus.',
 11:'Ein brauchbarer Ablauf soll auch mit anderen Eingaben verständlich funktionieren. Deshalb testest du Luna und Mira und prüfst nicht nur ein grünes Symbol. Größere Abläufe brauchen außerdem einen sichtbaren Umgang mit Fehlern und eine Trennung von Übungsbetrieb und echtem Einsatz. Heute reichen zwei Bausteine.'
}

IDEA_HELP={
 1:('Ideen an einem Ort sammeln','Stell dir einen Zettel vor: „Blick hinter die Kulissen - für Instagram“. Später kann Make solche Angaben immer gleich ordnen.','Heute nur verstehen: Ein Thema wird in einen festen Text eingesetzt, ähnlich wie unser Name. Mehrere Felder kommen Dienstag.'),
 2:('Einen Newsletter vorbereiten','Aus Thema, Datum und Zielgruppe entsteht ein kurzer Zettel für die Person, die den Newsletter schreibt. Das ist noch kein versandter Newsletter.','Beispiel: „Ideenatelier am 06.11.“ Der Termin soll unverändert übernommen werden. Dafür kommen Dienstag weitere Felder dazu.'),
 3:('Erkennen, welche Kampagne freigegeben ist','Ein interner Hinweis könnte lauten: „Die Herbstaktion ist freigegeben.“ Ohne Freigabe soll kein solcher Hinweis entstehen.','Das ist eine Vorschau auf Mittwoch: Ein Filter entscheidet, ob ein Schritt ausgeführt werden darf. Heute noch nicht nachbauen.'),
 4:('Einen Kampagnenlink verständlich beschriften','Statt eines nackten Links bekommst du einen Zettel mit Kampagnenname und Zieladresse. Das Team sieht leichter, wozu der Link gehört.','Das folgt derselben Idee wie die Begrüßung: feste Wörter mit ausgewählten Angaben verbinden. Ein Linktext misst noch keine Klicks.'),
 5:('Eine alte Idee später wieder anschauen','Eine Fotoidee soll nicht verloren gehen. Make könnte einen Zettel für die spätere Prüfung vorbereiten.','Beispiel: „Workshop-Foto erneut prüfen“. Einen automatischen Erinnerungstermin bauen wir heute noch nicht.'),
 6:('Ein Videoprojekt übersichtlich vorbereiten','Projektname, Thema und geplanter Einsatz werden zu einem kurzen Zettel für das Team. So müssen dieselben Angaben nicht mehrfach abgetippt werden.','Beispiel: „Nordlicht - Interview vorbereiten“. Mehrere Angaben übernehmen wir ab Dienstag. Es wird dabei noch kein Video erstellt.'),
 7:('Nur freigegebene Videoanfragen weitergeben','Eine Anfrage soll erst in die Planung gehen, wenn ein Mensch sie freigegeben hat. Make kann später prüfen, ob die vereinbarte Freigabe vorliegt.','Das üben wir Mittwoch mit erfundenen Angaben. Ein Testwert ersetzt keine echte Einwilligung oder geschäftliche Freigabe.'),
 8:('Einheitliche Namen für Projektdateien vorbereiten','Aus Projekt und Arbeitsschritt könnte der Vorschlag „Nordlicht_Interview_Entwurf“ entstehen. Das Team erkennt leichter, was gemeint ist.','Heute entsteht nur ein Textvorschlag. Für das tatsächliche Umbenennen echter Dateien wäre später eine zusätzliche Verbindung nötig.')
}
