"""Wednesday: one rule first, two optional useful mini-automations."""
RESEARCH_DATE='27.10.2026'
FEED='https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml'
EXTRA_SOURCES={
 'R1':('Make: RSS lesen','https://apps.make.com/rss'),
 'G1':('Make: Google Sheets verbinden','https://apps.make.com/google-sheets'),
 'G2':('Make: eine Tabellenzeile ergänzen','https://apps.make.com/google-sheets-modules'),
 'N1':('tagesschau: öffentlicher Nachrichtenfeed',FEED)
}
QUIZ=[
 ('Der Filter erlaubt nur FERTIG. Welcher Status darf weiter?',['ENTWURF','FERTIG','Jeder beliebige Text'],1,'Nur der vereinbarte Wert FERTIG erfüllt unsere eine Regel.'),
 ('Bei ENTWURF läuft der zweite Baustein nicht. Ist das hier ein Fehler?',['Nein. Genau dafür haben wir den Filter eingebaut','Ja. Alles muss immer weiterlaufen','Ja. Du musst ein KI-Abo kaufen'],0,'Ein Stopp ist hier das gewünschte Ergebnis. Ein Entwurf soll noch keine Bereitschaftsmeldung auslösen.'),
 ('Wo sitzt der Filter in unserem Ablauf?',['Als Satz in einem KI-Chat','Auf der Verbindung zwischen den beiden Bausteinen','Nur im Namen des Szenarios'],1,'Der Filter prüft auf der Verbindung, ob die Daten zum nächsten Baustein weiterdürfen.'),
 ('Was hat unsere Freigabe-Ampel nach dem Test wirklich gemacht?',['Einen Beitrag veröffentlicht','Eine Nachricht an Kunden verschickt','Je nach Teststatus einen Text in Make erzeugt oder den Weg gestoppt'],2,'Es gibt keinen Versand und keine Veröffentlichung. Die Hauptübung zeigt die Regel in Make. Die echten Zusatzaktionen sind im Bonus klar beschrieben.')
]

def core(make_page):
 def p(key,title,blocks,section='Ganz einfach'):
  return make_page(key,title,blocks,3,section)
 return [
 p('start','Mittwoch: Nur Fertiges darf weiter',[
  ('p','Heute machen wir es kleiner: Du gibst nur ein Wort ein. Steht dort FERTIG, darf Make einen nächsten Schritt ausführen. Steht dort ENTWURF, stoppt der Weg.'),
  ('flow',['Ein Wort: FERTIG oder ENTWURF','Eine Regel prüft das Wort','Weiter oder Stopp']),
  ('h','Das ist deine einzige Hauptaufgabe'),
  ('p','Baue eine kleine Freigabe-Ampel. Du brauchst zwei Bausteine und eine Regel dazwischen. Kein JSON, keine KI und keine neue Anmeldung.'),
  ('note','Unsere Ampel ist eine Übung mit einem erfundenen Status. Sie veröffentlicht nichts und ersetzt keine echte Freigabe durch eine zuständige Person.'),
  ('p','Wenn das klappt, wähle höchstens ein Extra: eine Idee in Google Sheets speichern oder eine Schlagzeile holen. Beide stehen mit eigener kurzer Anleitung im Bonus. Du musst nicht alles bauen.')], 'Dein Ziel am 28.10.2026'),
 p('filter','Ein Filter ist wie eine kleine Tür',[
  ('p','Stell dir eine Tür mit einem Schild vor: „Nur Fertiges“. Die Tür schaut auf deinen Status. Bei FERTIG geht sie auf. Bei ENTWURF bleibt sie zu. So arbeitet unser Filter.'),
  ('table',(['Wort in Make','Was es heute bedeutet'],[['Szenario','Dein ganzer Ablauf.'],['Modul','Ein Baustein, als Kreis dargestellt.'],['Filter','Die Regel auf der Verbindung zwischen zwei Bausteinen.'],['Run once','Du startest einen einzelnen Versuch selbst.']])),
  ('check','Wenn ENTWURF gestoppt wird, hat der Filter seine Aufgabe erfüllt. Nicht jeder Stopp ist ein Fehler.'),
  ('p','Die kleine Ampel darunter ist nur zum Ausprobieren im Browser. Sie startet nichts in Make und kostet keine Make-Credits.')]),
 p('wf3','Schritt 1: Einen Status bereitstellen',[
  ('h','Mach das'),
  ('p','1. Öffne in Make ein neues eigenes Szenario. Nenne es M2-03 Freigabe-Ampel.\n2. Wähle über das Plus Tools → Set variable.\n3. Trage bei Variable name status ein.\n4. Trage bei Variable value FERTIG ein. Falls eine Lebensdauer gefragt wird: One execution.\n5. Bestätige, speichere und klicke einmal auf Run once.\n6. Öffne die Ausgabe am Baustein. Dort muss FERTIG stehen.'),
  ('table',(['Feld','Eingabe'],[['Variable name','status'],['Variable value','FERTIG']])),
  ('note','Die automatische Planung bleibt ausgeschaltet. Dieser erste Test stellt nur deinen Wert bereit. Du hast noch nichts verschickt.')]),
 p('wf3-text','Schritt 2: Die Meldung vorbereiten',[
  ('h','Mach das'),
  ('p','1. Ergänze rechts einen zweiten Baustein: Tools → Compose a string.\n2. Tippe in Text: Beitrag zur Planung bereit. Status: und danach ein Leerzeichen.\n3. Wähle dahinter den Wert status aus dem ersten Baustein aus.\n4. Bestätige und speichere.'),
  ('h','So sieht es richtig aus'),
  ('p','Dein Text enthält den festen Satz und ein ausgewähltes farbiges Feld. Dieses Feld übernimmt den Status vom ersten Baustein.'),
  ('note','FERTIG hier nicht noch einmal fest eintippen. Der Status soll aus dem ersten Baustein kommen. Der Filter folgt im nächsten Schritt.')]),
 p('wf3-filter','Schritt 3: Genau eine Regel einsetzen',[
  ('h','Mach das'),
  ('p','1. Klicke auf die Verbindung zwischen den beiden Bausteinen.\n2. Gib dem Filter den Namen Nur Fertiges.\n3. Wähle links das Feld status aus dem ersten Baustein.\n4. Wähle als Textvergleich Equal to. Das heißt „ist gleich“.\n5. Tippe rechts FERTIG ein.\n6. Speichere den Filter und den Ablauf.'),
  ('flow',['status aus Baustein 1','Textvergleich: Equal to','Fester Vergleichswert: FERTIG']),
  ('note','Das ist schon die ganze Regel. Kein zweites Feld, kein AND, kein Router. Je nach Sprache kann „Equal to“ als „Gleich“ erscheinen. [M9]')]),
 p('wf3-test','Schritt 4: Einmal weiter, einmal stoppen',[
  ('h','Erster Test: FERTIG'),
  ('p','Speichere und starte den ganzen Ablauf mit Run once. Öffne die neue Ausgabe des zweiten Bausteins. Erwartet: Beitrag zur Planung bereit. Status: FERTIG'),
  ('h','Zweiter Test: ENTWURF'),
  ('p','Öffne den ersten Baustein. Ändere nur Variable value von FERTIG zu ENTWURF. Speichere und starte erneut. Jetzt soll der Filter den Weg stoppen. Der zweite Baustein erzeugt in diesem Lauf keine neue Meldung.'),
  ('table',(['Dein Testwert','Was passieren soll'],[['FERTIG','Die Meldung wird im zweiten Baustein erzeugt.'],['ENTWURF','Der Weg stoppt vor dem zweiten Baustein.']])),
  ('check','Öffne den aktuellen Lauf. Eine alte Ausgabe mit FERTIG ist kein Ergebnis des neuen ENTWURF-Tests.'),
  ('note','Geplant: 1 Credit für die Einzelprobe, 2 für den Weiter-Test und 1 für den Stopp-Test. Zusammen ungefähr 4 Credits. Der Filter selbst kostet keine Credits; weitere Starts können zusätzliche verbrauchen. Es zählt die Anzeige deines Kontos. [M2]')]),
 p('hilfe','Wenn es nicht so klappt',[
  ('table',(['Beobachtung','Das prüfst du'],[['ENTWURF läuft trotzdem weiter','Ist der Filter wirklich auf der Verbindung gespeichert? Links status, rechts FERTIG?'],['FERTIG wird gestoppt','Steht im ersten Baustein genau FERTIG, ohne zusätzliche Leerzeichen? Ist das richtige Feld ausgewählt?'],['Die Meldung bleibt alt','Die Ausgabe des neuesten Laufs ansehen. Historische Ergebnisse ändern sich nicht nachträglich.'],['status ist nicht auswählbar','Zuerst den ersten Baustein allein ausführen und dessen Ausgabe prüfen.']])),
  ('p','Ändere immer nur eine Sache und teste dann gezielt. Wenn beide Fälle wie erwartet funktionieren, bist du mit der Hauptaufgabe fertig.'),
  ('h','So passt es zu deinem Bereich'),
  ('p','Video: „Drehplan zur Prüfung bereit“. Vertrieb: „Angebotsentwurf zur Prüfung bereit“. Team: „Teaminfo zur Prüfung bereit“. Dafür änderst du nur den festen Text im zweiten Baustein. Die Regel bleibt gleich.')]),
 p('quiz','Vier sehr leichte Fragen',[
  ('quiz',None),('p','Du darfst nachlesen. Deine Auswahl und die geprüften Antworten werden auf diesem Gerät in diesem Browser gespeichert. Bei Problemen hilft der Textdownload.')], 'Dein kurzer Selbstcheck'),
 p('antworten','Die Lösungen kurz erklärt',[
  ('p',str(n)+'. Antwort '+'ABC'[right]+': '+why) for n,(_,_,right,why) in enumerate(QUIZ,1)
 ], 'Nachsehen'),
 p('mitnahme','Das reicht für Mittwoch',[
  ('p','Ich kann erklären: Mein Filter lässt FERTIG durch und stoppt ENTWURF. Ich habe beide Fälle geprüft. Die Meldung steht nur in Make.'),
  ('p','Mein erster Test ergab: ______________________________\nMein zweiter Test ergab: _____________________________\nMein echter Verbrauch vorher / nachher: ______________\nHier brauche ich noch Hilfe: _________________________'),
  ('note','Alles richtig? Dann ist die Hauptaufgabe erledigt. Wähle nur bei Interesse ein Bonusbeispiel. Die komplexe Kontaktformular-Kette aus den Folien ist keine weitere Bauaufgabe für heute.')], 'Dein Abschluss'),
 p('rss','Extra 1: Eine frische Schlagzeile holen',[
  ('p','Nützlich für ein kleines Ideen- oder Nachrichtenboard: Make liest eine Überschrift und einen Link. Keine zusätzliche Anmeldung. Als Beispiel verwenden wir den öffentlichen deutschsprachigen tagesschau-Feed. Eine Schlagzeile ist noch kein geprüfter eigener Social-Media-Text.'),
  ('h','Mach das'),
  ('p','1. Erstelle ein eigenes neues Szenario M2-03 Schlagzeile. Zeitplan aus lassen.\n2. Wähle RSS → Retrieve RSS Feed Items. Verwende Retrieve, nicht Watch.\n3. Füge die Feed-Adresse unten in URL ein. Setze Maximum number of returned items auf 1. Datumsfilter für diesen Versuch leer lassen.\n4. Speichere und führe zunächst nur diesen Baustein mit Run once aus.\n5. Öffne die Ausgabe. Suche nach der Überschrift und dem Link zum Artikel. Die Überschrift kann täglich wechseln.'),
  ('code',FEED),
  ('check','Ist eine echte Überschrift mit passendem Link angekommen? Die Adresse wurde am 27.10.2026 direkt gelesen: HTTP 200 und gültiger RSS-Feed. Das ist kein Test des Moduls in deinem Make-Konto.'),
  ('note','Nur ein Artikel pro Versuch. So vermeidest du eine große Liste. Geplanter Verbrauch für einen einfachen Einzelabruf: ungefähr 1 Credit. Feed-Anbieter können ihr Angebot später ändern. [R1, N1]')], 'Freiwillig: keine neue Anmeldung'),
 p('rss-text','Aus der Schlagzeile wird dein Lesezettel',[
  ('h','Mach das'),
  ('p','1. Hänge Tools → Compose a string hinter den erfolgreich getesteten RSS-Baustein.\n2. Tippe Lesetipp: und ein Leerzeichen. Wähle das Feld für die Überschrift aus der RSS-Ausgabe, häufig Title.\n3. Füge eine neue Zeile hinzu und wähle den Artikel-Link aus derselben Ausgabe.\n4. Speichere und starte beide Bausteine einmal.\n5. Prüfe, ob die Überschrift und der Link im fertigen Text zusammenpassen.'),
  ('p','Jetzt hast du einen kleinen wiederverwendbaren Lesezettel statt einer abgeschriebenen Überschrift. Für andere Themen kannst du später einen passenden öffentlichen RSS-Feed einsetzen.'),
  ('note','Die Ausgabe wird nicht automatisch verschickt oder veröffentlicht. Dieselbe Meldung kann bei erneutem Abruf wiederkommen: Wir bauen hier keinen Speicher für bereits gelesene Artikel. Mit Einzelprobe und einem Zweierlauf zusammen geplant ungefähr 3 Credits.')], 'Freiwillig: zweiter kleiner Schritt'),
 p('ideen-speicher','Extra 2: Eine Idee in Google Sheets sichern',[
  ('p','Hier entsteht wirklich eine gespeicherte Tabellenzeile. Wähle dieses Extra nur, wenn du bereits ein eigenes Google-Konto hast und es mit Make verbinden möchtest. Sonst nimm das RSS-Beispiel.'),
  ('h','Mach das'),
  ('p','1. Erstelle in Google Sheets eine neue eigene Tabelle Ideenparkplatz. Schreibe in A1 Idee und in B1 Bereich.\n2. Lege in Make ein neues manuelles Szenario M2-03 Idee sichern an. Erster Baustein: Tools → Set variable, Name idee, Wert Teamfoto für die Website. Einmal allein testen.\n3. Ergänze Google Sheets → Add a Row. Verbinde dein eigenes Google-Konto. Wähle die neue Tabelle und ihr Tabellenblatt; Table contains headers: Yes.\n4. Wähle beim Feld Idee den Wert idee aus dem ersten Baustein. Trage bei Bereich fest Marketing ein.\n5. Speichere und starte beide Bausteine einmal mit Run once.\n6. Öffne Google Sheets. Unter den Überschriften muss deine neue Zeile stehen.'),
  ('check','Die Idee wird vom ersten Baustein in deine neue Tabelle übertragen. Später änderst du nur den Wert im ersten Baustein. Jeder weitere Start ergänzt eine Zeile; er ersetzt die vorherige nicht.'),
  ('note','Einzelprobe und kompletter Zweierlauf: geplant ungefähr 3 Credits. Kontoverbindung kann extra Zeit brauchen. Werden zusätzliche Technik oder Freigaben verlangt, wähle das RSS-Extra. Keine Bezahl- oder Cloud-Entwickler-Einrichtung für diese Übung anfangen. [G1, G2]')], 'Freiwillig: vorhandenes Google-Konto'),
 p('folienbegriffe','Die schwierigen Folien in Alltagssprache',[
  ('table',(['Begriff','Ganz einfach'],[['Webhook','Wie eine Türklingel: Ein anderer Dienst meldet ein Ereignis. Polling ist eher wiederholtes Nachsehen.'],['Router','Eine Weggabelung mit mehreren möglichen Routen. Mehr als eine passende Route kann laufen.'],['AND / OR','AND: beide Regeln müssen passen. OR: mindestens eine muss passen. Heute brauchst du nur eine Regel.'],['System / User / Assistant','Übergeordnete KI-Regeln / konkrete Eingabe / KI-Antwort. Die Schnittstelle entscheidet, welche Rollen unterstützt sind.']])),
  ('p','Die Folien zeigen ein großes Kontaktformular mit Tally, Modell-API, E-Mail und HubSpot. Dort wird eine Nachricht eingeordnet, als JSON ausgegeben und passend weitergeleitet. Dafür braucht man mehrere Zugänge und mehr Erfahrung.'),
  ('note','Heute nicht nachbauen. KI-Ergebnisse müssen vor echtem Versand auf Inhalt und Freigabe geprüft werden. Ein korrektes JSON oder ein niedriger Temperaturwert beweist keine richtige Antwort. Ein normaler Make-Router verarbeitet Routen nacheinander, nicht parallel. [M10, M12]')], 'Freiwillig: nur verstehen')
 ]

SLIDE_HELP={
17:'Ein Webhook meldet ein Ereignis an eine vereinbarte Adresse, ähnlich einer Klingel. Polling fragt regelmäßig nach. Ein API-Aufruf kann Daten lesen oder schreiben. Webhooks können schnell starten, aber Warteschlangen und Verarbeitung brauchen ebenfalls Zeit. Heute richten wir keinen öffentlichen Eingang ein.',
18:'Die große Originalübung verbindet Formular, KI-Einordnung, Bestätigungsmail und zuständige Teams. Tally, Modell-API, Microsoft 365 und HubSpot benötigen eigene passende Zugänge. Diese Kette ist kein Pflichtprojekt für den Einstieg und nicht automatisch vollständig durch Make Free bezahlt.',
19:'Das Tally-Formular sammelt Vorname, Nachname, E-Mail, Anliegen und Nachricht. Die Kategorien sind Angebot/Projekt, Support/Hilfe, Feedback/Beschwerde, Partnerschaft/Kooperation und Sonstiges. Ein neuer Formulareingang kann den Ablauf starten. Heute genügt ein selbst gesetzter Teststatus.',
20:'Die Vorlage holt Testdaten, gibt der KI Regeln und verlangt Antwortfelder für betreff, body_text, kategorie und prioritaet. Beispiele helfen beim Prüfen. Konkreter Modellname, Modulnummer und Einstellung aus Juli 2026 müssen beim Einsatz neu geprüft werden. Ein JSON-Wunsch allein garantiert keine richtige Antwort.',
21:'Parse JSON würde die Modellantwort in Felder aufteilen. Danach kann man mit erlaubten Angaben eine Mail vorbereiten und Routen wählen. Eine KI-Antwort soll vor dem echten Versand geprüft werden. Die heutige Ampel zeigt nur den kleinen Teil „darf weiter oder soll stoppen“.',
22:'Die Vorlage verteilt nach Angebot, Support, Feedback/Beschwerde, Partnerschaft, Sonstiges und zusätzlich Spam. Vertrieb könnte einen Kontakt und eine Aufgabe in HubSpot bekommen; Support eine interne Nachricht. Das benötigt weitere Konten, passende Prioritätswerte und Regeln für Zweifelsfälle. Normale Router-Routen laufen nacheinander.',
23:'Die große Kette würde mit Angebot, Support, Beschwerde und widersprüchlichen Angaben getestet. Verlauf, Verbrauch, Routing und Ergebnisse müssten dokumentiert werden. Heute dokumentierst du nur zwei kleine Fälle: FERTIG geht weiter, ENTWURF stoppt. Aktivieren einer fremden großen Vorlage ist nicht nötig.',
28:'Ein Filter ist eine Tür mit einer Regel. Ein Router ist eine Weggabelung. Beide steuern, welche Schritte ausgeführt werden. Wenn ein Filter stoppt, kann er unnötige Folgeschritte vermeiden. Für den ersten einfachen Versuch reicht unsere einzelne Tür.',
29:'Vergleiche sind Fragen wie gleich, ungleich, größer, kleiner oder enthält. Zahlenvergleiche brauchen passende Zahlen. AND verlangt alle verbundenen Regeln; OR mindestens eine. Wir verwenden nur den einfachen Textvergleich status ist gleich FERTIG.',
30:'System-Regeln geben einer passenden KI-Schnittstelle die Grundrichtung. User ist die konkrete Frage oder Eingabe. Assistant ist die Antwort im Verlauf. Man unterscheidet diese Rollen, damit Regeln, Eingaben und Antworten nicht durcheinandergeraten. Für die Ampel brauchst du kein KI-Modell.'
}
IDEA_HELP={
17:('Ein erster Tag ohne Sucherei','Eine kurze Liste hilft neuen Kolleginnen beim Einstieg.','Ein Einfall kann im Ideenparkplatz landen. Kein HR-System nötig.'),
18:('Ein Mentoring-Vorschlag','Zwei Menschen sollen erst nach Zustimmung miteinander sprechen.','Die Ampel erklärt das Prinzip. Ein Teststatus ersetzt keine echte Zustimmung.'),
19:('Ein kleines Teamritual','Eine Idee für einen kurzen Freitagsaustausch sammeln.','Im Ideenparkplatz speichern. Das erstellt noch keinen Kalendereintrag.'),
20:('Eine klare Übergabe','Eine Vertretung soll sehen: Flyertext fertig, Bildauswahl offen.','Für diese Lernrunde genügt eine verständliche Notiz. Kein kompliziertes Projektwerkzeug anschließen.'),
21:('Eine Rückfrage festhalten','Bei einer Anfrage fehlt der Termin.','Die Rückfrage als Idee oder Notiz sammeln. Make soll keinen Termin erfinden.'),
22:('Einen Supportfall weitergeben','Ein Problem soll die richtige Person zur Prüfung bekommen.','Die Ampel hilft beim Verstehen der Weitergabe. Einen echten Versand bauen wir hier nicht.'),
23:('Eine Beschwerde zur Prüfung legen','Eine Rückmeldung zur Druckfarbe muss ein Mensch ansehen.','Eine interne Prüfnotiz vorbereiten. Keine automatische Zusage an Kunden erzeugen.')
}
