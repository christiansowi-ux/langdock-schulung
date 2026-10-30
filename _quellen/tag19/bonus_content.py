"""Fünf Praxisfälle und genau zwanzig zusätzliche, eigenständig nutzbare Prompts."""
PAGES=[]
def add(key,title,blocks,deck='Bonus · KI im Alltag · 23.10.2026'):
 PAGES.append(dict(key=key,title=title,deck=deck,blocks=blocks))
add('start','Kleine Aufträge. Sichtbare Ergebnisse.',[
 ('p','Fünf ausführliche Anwendungsfälle und zwanzig zusätzliche Prompts für Druck und Vertrieb, Team und Website sowie Gestaltung. Alle enthaltenen Firmen, Namen, Termine und Geschäftsdaten sind erfunden.'),
 ('table',(['Fünf Anwendungsfälle','20 weitere Prompts'],[['Logoidee in einem 5-Minuten-Entwurfsfenster.','Kundenkommunikation, Text, Struktur und Gestaltung.'],['Website-Prototyp in einem 30-Minuten-Plan.','Jeder Prompt enthält seine eigenen Beispieldaten.'],['Flyer, Workshop-Deck und Content-Paket.','Kopieren, im passenden Werkzeug nutzen, Ergebnis prüfen.']])),
 ('note','„100% klappt“ ist bei generativer KI keine ehrliche Zusage. Diese Aufträge sind präzise und besitzen Prüfkriterien. Sie wurden redaktionell auf Verständlichkeit geprüft, nicht als Erfolgstest in allen Produkten ausgeführt. Auch gute Prompts brauchen gelegentlich eine Korrekturrunde.'),
 ('p','Die Zeitfenster meinen einen ersten prüfbaren Entwurf bei vorhandenem Zugang. Anmeldung, Wartezeiten, Rechteklärung, fachliche Freigabe und Veröffentlichung können zusätzlich Zeit benötigen.')])
add('methode','Die kurze Bedienungsanleitung',[
 ('h','1. Die passende Oberfläche wählen'),('p','Ein Textchat kann Texte und Konzepte liefern. Ein Bildgenerator braucht eine aktivierte Bildfunktion. Eine sichtbare Website benötigt einen Design- oder Code-Arbeitsbereich. Ein Text, der „Logo erstellt“ sagt, ist noch keine Bilddatei.'),
 ('h','2. Den ganzen Prompt übernehmen'),('p','Die Beispiele funktionieren ohne ausgefüllte Platzhalter. Für die eigene Arbeit danach nur bestätigte Inhalte einsetzen. Keine vertraulichen Kundenunterlagen allein für einen schnellen Versuch hochladen.'),
 ('h','3. Ergebnis gegen den Auftrag prüfen'),('p','Stimmen Fakten, Länge, Format und Anzahl? Kann die Datei geöffnet werden? Funktioniert die vorgesehene kleine Aktion? Erst dann den nächsten Schritt planen.'),
 ('prompt','Prüfe deinen letzten Entwurf gegen meinen ursprünglichen Auftrag. Gib eine Tabelle mit Anforderung, tatsächlichem Ergebnis und nötiger Korrektur aus. Unterscheide selbst kontrollierte Punkte von Dingen, die ich noch prüfen muss. Korrigiere anschließend nur die festgestellten Abweichungen. Erfinde keine erfolgreiche Prüfung.'),
 ('note','Der Selbstcheck einer KI ersetzt keine unabhängige Kontrolle. Die Korrekturzeilen im Heft gehören im selben Gespräch direkt hinter das Ergebnis.')])

def case(n,title,where,time,prompt,check,repair,note):
 add('fall-'+str(n),title,[('h','Wo einsetzen'),('p',where),('p','Zeitplan: '+time),('prompt',prompt),('check',check),('p','Wenn es hakt: '+repair),('note',note)],f'Anwendungsfall {n} von 5 · erster prüfbarer Entwurf')

case(1,'Eine Logoidee in fünf Minuten',
 'Bildgenerator für das Symbol; Canva oder ein vergleichbarer Layouteditor für den separat gesetzten Namen.',
 'Minute 0–1: Ziel und Motiv. 1–3: drei Ideen. 3–4: eine vereinfachen. 4–5: klein und einfarbig prüfen. Generierungszeit kann darüber hinausgehen.',
 'Erzeuge drei klar getrennte Symbolideen für die erfundene Papierfunke-Werkstatt: kleine Druckprojekte, freundlich, präzise, unkompliziert. Jedes Symbol verbindet eine gefaltete Papierkante mit einem einzelnen kleinen Funken. Einfarbig dunkelgrün auf reinweißem Hintergrund, flache klare Formen, keine Verläufe, Schatten, 3D-Effekte, Mockups oder Buchstaben. Die drei Ideen müssen in ihrer Form erkennbar verschieden sein. Keine bestehenden Marken nachahmen. Ziel: ein einfaches Zeichen, das auch klein noch erkennbar ist. Falls du keine Bilder erzeugen kannst, liefere drei präzise Motivbeschreibungen und kennzeichne sie als Konzept.',
 'Sind es drei unterschiedliche Ideen? Funktioniert eine bei kleiner Ansicht und in Schwarzweiß? Den Namen „Papierfunke“ im Editor korrekt und bearbeitbar daneben setzen; passende Schriftlizenz prüfen.',
 'Vereinfache Idee 2 auf zwei klare Formen. Entferne dünne Innenlinien. Zeige nur dieses Zeichen, schwarz auf weiß, ohne Text.',
 'Fünf Minuten liefern eine Logoidee, kein garantiert perfektes oder markenrechtlich freigegebenes Logo. Ein PNG ist keine Vektordatei. Für skalierbare Produktion gegebenenfalls sauber nachzeichnen und Dateiformat tatsächlich prüfen.')

case(2,'Eine gute Website in 30 Minuten beginnen',
 'Claude Design oder Google Stitch für den Entwurf; ein Code-Arbeitsbereich für eine lokale HTML-Vorschau. Nicht in einen reinen Textchat einfügen und eine Live-Seite erwarten.',
 '0–5: Ziel und Inhalte. 5–15: erste Seite. 15–23: eine Verbesserung. 23–30: Mobilansicht, Text und Hauptaktion prüfen.',
 'Baue einen deutschsprachigen, lokal prüfbaren Einseiter für die erfundene Papierfunke-Werkstatt. Zielgruppe: kleine Teams, die einen Druckentwurf planen. Einzige bestätigte Leistungen: Ideen besprechen, Entwürfe gemeinsam prüfen, Produktionsanfrage vorbereiten. Keine Preise, Testimonials, Auszeichnungen oder Kontaktdaten erfinden. Abschnitte: klare Hauptüberschrift, drei Leistungen, Ablauf in drei Schritten, drei FAQ. Hauptbutton „Ablauf ansehen“ führt zum Ablaufabschnitt. Stil: Cremeweiß, Dunkelgrün, großzügiger Freiraum, gut lesbare Schrift. Kein Kontaktformular, Tracking oder externer Dienst. Im Code-Arbeitsbereich: eine eigenständige index.html mit internem CSS und ohne externe Abhängigkeiten erstellen. Im Designwerkzeug: entsprechenden sichtbaren Prototyp erzeugen. Nenne anschließend, was tatsächlich erstellt und geprüft wurde.',
 'Die Vorschau bei 390px und am Desktop öffnen. Text vollständig? Button springt korrekt? Tastaturfokus sichtbar? Keine erfundenen Leistungen? Datei vorhanden?',
 'Korrigiere nur horizontalen Überlauf und den Fokus der Hauptaktion. Behalte Inhalt und Farbpalette bei. Erkläre, welche Prüfungen wirklich ausgeführt wurden.',
 '30 Minuten sind ein Zeitbudget für einen begrenzten Prototyp. Hosting, echte Formulare, Domain, Rechtstexte, Datenschutz und umfassende Barrierefreiheitsprüfung sind weitere Arbeitsschritte.')

case(3,'Ein Flyer, den man wirklich lesen kann',
 'Textchat für Inhalt; Canva oder ein Layoutprogramm für ein bearbeitbares A5-Layout. Ein ganzes Textbild aus dem Bildgenerator erschwert Korrekturen.',
 '3 Minuten: Fakten. 5 Minuten: Text und Struktur. 7 Minuten: Layout. Danach Export und Produktionsprüfung.',
 'Bereite einen A5-Hochformat-Flyer für das erfundene Papierfunke-Ideenatelier vor. Bestätigte Fakten: 06.11.2026, 16–18 Uhr, Raum Sonnenhof; Thema „Deine erste Druckidee“; für Einsteiger; Eintritt frei; keine Anmeldung vorgesehen. Erstelle eine Überschrift mit maximal 7 Wörtern, einen Einstieg mit maximal 25 Wörtern, drei kurze Nutzenpunkte, einen gut sichtbaren Terminblock und die Schlusszeile „Komm mit einer Idee vorbei“. Liefere außerdem eine Layoutskizze in Worten mit getrennten Textbereichen und einem ruhigen Papiermotiv. Keine Adresse, Sponsoren, Bewertungen oder weiteren Angebote ergänzen. Schrift muss im Layout separat bearbeitbar bleiben. Ohne Layoutwerkzeug nur Text und Konzept ausgeben.',
 'Termin, Uhrzeit, Ort und „Eintritt frei“ mit der Quelle vergleichen. Im Endformat lesen. Vor Produktion Export, Bildqualität, Schriften, Beschnitt und Sicherheitsabstand mit der Druckerei klären.',
 'Kürze den Einstieg auf höchstens 20 Wörter. Mache Termin und Ort zum zweitauffälligsten Bereich. Ergänze keine neuen Fakten.',
 'Ein schöner Bildschirmflyer ist noch keine geprüfte Druckdatei. „PDF Print“ allein bestätigt weder ein benötigtes Farbprofil noch die Vorgaben jeder Druckerei. Herstellerhilfe: [A2] im Freitagsheft.')

case(4,'Ein Workshop-Deck aus vier Gedanken',
 'Claude Design oder eine verfügbare Präsentationsumgebung; im Textchat alternativ ein Folienmanuskript.',
 '3 Minuten: Fakten. 5 Minuten: Struktur. 7 Minuten: Gestaltung. Danach Lesbarkeit und Export prüfen.',
 'Erstelle vier Workshop-Folien für ein fiktives Team zum Thema „Fokus ohne Fachwörter“. Inhalte: 1. Eine wichtigste Aufgabe auswählen. 2. 25 Minuten ungestört arbeiten, wenn die Tätigkeit das erlaubt. 3. Fragen für den nächsten Austausch sammeln. 4. Den nächsten kleinen Schritt notieren. Stil: Cremeweiß und Dunkelgrün; pro Folie eine klare Überschrift, höchstens drei kurze Punkte und eine passende einfache Skizze. Keine wissenschaftliche Wirksamkeit behaupten. Ergänze je zwei Sätze Sprechernotizen. Falls du nur Text liefern kannst, trenne Folientext, Bildidee und Sprechernotizen. Erstelle keine erfundenen Quellen.',
 'Vier Folien? Nur die vorgegebenen Inhalte? Wenig Text? Notizen separat? Export tatsächlich geöffnet? Ein Folientitel allein ist noch keine Präsentationsdatei.',
 'Entferne doppelte Aussagen. Kürze Folie 2 auf einen einzigen verständlichen Hauptgedanken; Sprechernotizen dürfen ausführlicher bleiben.',
 'Eigene Gestaltungsregeln verwenden. Ein automatisch erzeugtes Deck kann inhaltlich oder visuell nachgebessert werden müssen.')

case(5,'Aus einem Faktenzettel wird ein Content-Paket',
 'Normaler Textchat. Kein Social-Konto verbinden; Beiträge bleiben Entwürfe.',
 '2 Minuten: Fakten prüfen. 5 Minuten: drei Formate. 3 Minuten: Aussagen und Zeichenlängen kontrollieren.',
 'Verwandle ausschließlich diese erfundenen Fakten in drei deutsche Content-Entwürfe: Papierfunke-Ideenatelier, 06.11.2026, 16–18 Uhr, Raum Sonnenhof, Thema „Deine erste Druckidee“, Einsteiger willkommen, Eintritt frei, keine Anmeldung vorgesehen. Ausgabe: 1. Ein Social-Post mit maximal 450 Zeichen. 2. Ein fünfteiliger Karussell-Text mit maximal 18 Wörtern pro Karte. 3. Ein kurzer Newsletter-Absatz mit maximal 80 Wörtern. Ton freundlich, konkret und ohne Druck. Keine Plätze-Knappheit, Erfolgsgarantien, Links, Adressen oder Hashtags erfinden. Trenne die Formate klar. Liste danach die im Text verwendeten Veranstaltungsfakten auf. Nichts veröffentlichen.',
 'Datum und Uhrzeit in allen Varianten gleich? Jeder Zusatz aus den Fakten ableitbar? Keine erfundenen Links? Zeichen und Wörter stichprobenartig nachzählen.',
 'Überarbeite nur den Social-Post: sachlicher Einstieg, höchstens ein Ausrufezeichen, alle Veranstaltungsfakten unverändert.',
 'Mehr Formate bedeuten keine zusätzlichen Fakten. Ein freundlicher Entwurf darf keine unbestätigten Versprechen ergänzen.')

PROMPTS=[
 ('Eine freundliche Kundenantwort','Ingo · Textchat',
 'Schreibe eine Antwort mit höchstens 110 Wörtern auf diese erfundene Anfrage: „Wir brauchen 200 Flyer für Freitag. Könnt ihr das schaffen? Was kostet das?“ Bestätigt ist nur: Druckerei Papierfunke prüft Termine nach Sichtung der Datei; Preis hängt von Format, Papier und Ausführung ab. Frage freundlich nach Endformat, Papierwunsch, ein- oder beidseitigem Druck und dem genauen benötigten Datum. Versprich weder Preis noch Liefertermin. Ausgabe: Betreff und Mailentwurf, danach eine Liste der fehlenden Angaben. Nicht versenden.',
 'Kein zugesagter Termin und kein erfundener Preis.','Kürze den Entwurf auf 80 Wörter; behalte alle vier nötigen Rückfragen.'),
 ('Ein Angebot auf Lücken prüfen','Ingo · Textchat',
 'Prüfe nur diesen fiktiven Angebotstext: „200 Flyer A5, 135g, 4/4-farbig, 79 Euro, Lieferung Freitag.“ Erstelle eine Tabelle: vorhandene Angabe, Unklarheit, passende Rückfrage. Prüfe besonders, ob Netto/Brutto, Papierart, Versandkosten, genauer Liefertermin und Datenprüfung eindeutig genannt sind. Rechne keine Steuer aus und ergänze keine Konditionen. Erkläre danach in zwei einfachen Sätzen, warum ein kurzer Angebotstext trotzdem Rückfragen brauchen kann.',
 'Es dürfen keine fehlenden Konditionen als gegeben erscheinen.','Trenne bestätigte Angaben und bloße Vermutungen noch deutlicher.'),
 ('Aus Chaos wird ein Druckbriefing','Ingo · Textchat',
 'Ordne diese erfundenen Notizen zu einem einseitigen Druckbriefing: „200 Flyer; Aktion im November; Logo liegt vor; vielleicht A5; beidseitig; Papier unbekannt; Termin noch offen; Zielgruppe kleine Teams; Headline fehlt.“ Nutze Rubriken Ziel, bestätigte Vorgaben, offene Entscheidungen, benötigte Dateien, nächste Rückfragen. Behandle „vielleicht A5“ nicht als Freigabe. Keine Angaben erfinden. Am Schluss höchstens drei priorisierte Fragen formulieren.',
 'A5 muss offen bleiben, 200 und beidseitig sind bestätigt.','Markiere jede offene Entscheidung ausdrücklich als ungeklärt.'),
 ('Korrekturlesen ohne Inhalt zu verändern','Alle · Textchat',
 'Korrigiere Rechtschreibung und Zeichensetzung dieses fiktiven Textes: „Unser Ideenatellier findet am 06.11.2026 von 16 bis 18 Uhr im Raum Sonnenhof statt. Der eintrit ist frei, eine Anmeldung ist nicht nötig.“ Ändere keine Daten, Uhrzeiten, Orte oder Aussagen. Gib zuerst den korrigierten Text aus, dann eine Änderungsliste mit vorher/nachher. Gib abschließend die unveränderten Fakten separat wieder.',
 'Datum, Zeit, Ort und Anmeldung müssen unverändert bleiben.','Mache stilistische Änderungen rückgängig und behalte nur echte Korrekturen.'),
 ('FAQ aus wenigen echten Fakten','Carmen · Textchat',
 'Schreibe sechs kurze FAQ für die fiktive Papierfunke-Werkstatt. Nur diese Fakten sind bestätigt: Beratung zu Druckideen; gemeinsame Entwurfsprüfung; Vorbereitung einer Produktionsanfrage; keine veröffentlichten Preise; Termine nach Absprache. Jede Antwort höchstens 35 Wörter. Wenn eine Frage nicht beantwortbar ist, sage klar, was noch zu klären ist. Keine Öffnungszeiten, Liefergebiete, Garantien oder Kontaktadresse erfinden. Ausgabe: Frage/Antwort, danach Liste offener Angaben.',
 'Es darf keine erfundene Öffnungszeit oder Garantie vorkommen.','Ersetze unbestätigte Angaben durch eine klare offene Frage.'),
 ('Kleine Website-Texte mit großer Klarheit','Carmen · Textchat',
 'Formuliere Microcopy für eine rein lokale Demo: Ein Button merkt Interesse an einem fiktiven Teamfrühstück nur im Browser; es gibt keine Anmeldung, keinen Versand und keinen Servereintrag. Liefere drei Buttontexte mit höchstens 4 Wörtern, eine eindeutige Bestätigung und einen kurzen Hinweis zur lokalen Speicherung. Keine Formulierung darf behaupten, man sei registriert. Begründe deine bevorzugte Variante in zwei Sätzen.',
 '„Angemeldet“ und „versendet“ wären sachlich falsch.','Mache die Bestätigung genauer: nur lokal gemerkt, keine Anmeldung.'),
 ('Besprechungsnotizen sortieren','Carmen · Textchat',
 'Erstelle aus diesen fiktiven Notizen ein kurzes Ergebnisprotokoll: „Mira prüft Flyertext bis Dienstag. Websitebild noch offen. Tom schlägt blau vor, keine Entscheidung. Team entscheidet: Terminblock größer. Budget unbekannt.“ Rubriken: Entscheidungen, Aufgaben mit Person und Frist, Vorschläge, offene Fragen. Unbekannte Zuständigkeiten und Fristen als nicht festgelegt markieren. Wandle Vorschläge nicht in Beschlüsse um.',
 'Blau muss Vorschlag bleiben; Budget bleibt unbekannt.','Prüfe jede Entscheidung auf einen eindeutigen Beschluss in den Notizen.'),
 ('Eine Sitzung, die schnell zum Punkt kommt','Carmen · Textchat',
 'Plane eine 25-minütige fiktive Teamsitzung zur Auswahl eines Flyerentwurfs. Ziel: am Ende eine Variante und maximal drei Änderungen festlegen. Drei Personen, zwei Entwürfe, keine weiteren Vorinformationen. Gib eine Agenda mit Minutenangaben aus, die zusammen genau 25 ergeben. Ergänze eine kurze Einstiegsfrage und eine einfache Entscheidungsmethode. Keine zusätzlichen Hilfsmittel voraussetzen. Keine echten Entscheidungen vorwegnehmen.',
 'Minuten addieren und prüfen, ob Auswahl und Änderungen Platz haben.','Korrigiere nur die Zeitaufteilung auf insgesamt genau 25 Minuten.'),
 ('Prioritäten mit ehrlichen Grenzen','Alle · Textchat',
 'Ordne diese erfundenen Aufgaben für einen Vormittag mit 90 Minuten: Kundentermin bestätigen (5 Min, heute fällig), Entwurf prüfen (30 Min, morgen fällig), Materialordner sortieren (40 Min, keine Frist), Teamfragen beantworten (15 Min, heute), neue Farben testen (25 Min, optional). Gib einen Plan mit höchstens 90 Minuten und eine getrennte Später-Liste aus. Begründe knapp. Keine weiteren Fristen oder Abhängigkeiten erfinden.',
 'Maximal 90 Minuten; optionale Arbeit darf Pflichtaufgaben nicht verdrängen.','Prüfe die Summe erneut und verschiebe Überhang auf die Später-Liste.'),
 ('Eine kleine Tabelle sauber einordnen','Ingo und Carmen · Textchat',
 'Ordne diese fiktiven Zeilen ein: A01;Flyer;offen / A02;Website;erledigt / A03;Logo;Status fehlt / A04;Flyer;offen. Ausgabe als Tabelle mit ID, Thema, Status und Handlungsbedarf. Zähle anschließend die Zeilen je bestätigtem Status und die ungeklärten Zeilen getrennt. Status fehlt darf weder als offen noch als erledigt gezählt werden. IDs erhalten, keine Daten ergänzen.',
 'Offen=2, erledigt=1, ungeklärt=1; insgesamt 4 Zeilen.','Korrigiere die Zählung und führe ungeklärte Werte separat.'),
 ('Fachwörter in Alltagssprache übersetzen','Alle · Textchat',
 'Erkläre einer Person ohne Fachwissen diese Begriffe: Prototyp, Canvas, Designsystem, Export. Je Begriff: ein Satz mit höchstens 20 Wörtern, ein Alltagsvergleich und ein Beispiel aus einer fiktiven Flyer- oder Websiteplanung. Verwende keine weiteren unerklärten Fachwörter. Sage ausdrücklich, warum eine sichtbare Vorschau noch keine veröffentlichte Website ist.',
 'Erklärung muss ohne weitere Fachwörter verständlich sein.','Ersetze alle neu eingeführten Fachwörter durch einfache Umschreibungen.'),
 ('Ein hilfreicher Entscheidungsbaum','Carmen · Textchat',
 'Erstelle einen einfachen Entscheidungsbaum für fiktive Druckanfragen. Bekannte Regeln: Fehlt das Endformat, danach fragen. Ist das Format bekannt, aber die Stückzahl fehlt, danach fragen. Sind beide bekannt, Unterlagen zur Prüfung vorbereiten. Nie Preis oder Termin zusagen. Gib maximal fünf kurze Wenn-dann-Zeilen und drei Testbeispiele aus. Zeige je Test den richtigen nächsten Schritt.',
 'Bei zwei fehlenden Angaben zuerst das Format fragen; keine Zusage.','Entferne Zweige, die Informationen voraussetzen, die nicht angegeben sind.'),
 ('Eine leicht verständliche Textfassung','Alle · Textchat',
 'Überarbeite diese fiktive Information in klarer Alltagssprache: „Zur Optimierung der internen Abstimmungsprozesse wird um fristgerechte Übermittlung sämtlicher Korrekturwünsche bis Dienstag, 12 Uhr, gebeten.“ Erhalte Bedeutung und Frist. Gib eine freundliche Fassung mit höchstens 35 Wörtern und eine sehr kurze Variante mit höchstens 18 Wörtern aus. Keine neue Begründung erfinden. Kennzeichne das Ergebnis als verständliche Sprache, nicht als zertifizierte Leichte Sprache.',
 'Dienstag, 12 Uhr bleibt unverändert; keine Zertifizierung behaupten.','Vereinfache den Satzbau weiter, ohne die Frist zu ändern.'),
 ('Eine Farbidee mit benannten Rollen','Tabea · Textchat',
 'Schlage für die fiktive Papierfunke-Werkstatt zwei Farbpaletten mit je vier Hex-Farben vor. Stimmung freundlich und ruhig. Rollen: Hintergrund, Haupttext, Akzent, dezente Fläche. Gib je Palette eine kurze Begründung und empfohlene Kombinationen aus. Behaupte keinen gemessenen Kontrast. Nenne stattdessen die Kombinationen, die vor Nutzung mit einem Kontrastprüfer getestet werden sollen. Keine fremde Marke kopieren.',
 'Jede Farbe braucht eine Rolle; Kontrast darf nicht als gemessen ausgegeben werden.','Verringere die Zahl der Akzentfarben und benenne klare Text-Hintergrund-Paare.'),
 ('Eine Geschichte in sechs Standbildern','Tabea · Textchat',
 'Schreibe ein Storyboard als sechs Standbilder für eine fiktive Präsentation über eine Druckidee. Handlung: leeres Papier, erste Skizze, gemeinsames Feedback, überarbeiteter Entwurf, Druckmuster, fertiger Flyer. Pro Bild: sichtbare Aktion, Bildausschnitt und eine Texteinblendung mit höchstens fünf Wörtern. Keine Video- oder Audiodatei erzeugen. Keine Produktionsqualität oder Wirkung garantieren.',
 'Sechs Bilder, erkennbarer Fortschritt, kurze Einblendungen.','Mache die Veränderung zwischen Bild 3 und 4 sichtbar und konkret.'),
 ('Ein Bildbriefing ohne Zufallsdekoration','Tabea · Textchat oder Bildgenerator',
 'Konzipiere ein quadratisches Motiv für eine erfundene Papierwerkstatt: Hände falten ein cremeweißes Blatt auf einem dunkelgrünen Arbeitstisch, seitliches weiches Tageslicht, wenige Werkzeuge, ruhiger Hintergrund. Im oberen Drittel freie Fläche für später gesetzten Text. Keine Buchstaben, Logos oder Wasserzeichen im Motiv, keine fremden Marken. Bei Bildfunktion ein Motiv erzeugen; sonst präzise Bildbeschreibung liefern. Bezeichne die freie Fläche und den Blickfang.',
 'Freie Textfläche vorhanden? Hände und Faltung plausibel? Kein eingebrannter Text.','Entferne Dekoration; lasse im oberen Drittel eine zusammenhängende ruhige Fläche.'),
 ('Fünf Bildunterschriften ohne Übertreibung','Tabea · Textchat',
 'Formuliere fünf deutsche Bildunterschriften für ein fiktives Foto: Auf einem Tisch liegen ein Papiermuster und zwei Entwurfsskizzen. Bestätigt: internes Ideenatelier, Team prüft Varianten. Jede Unterschrift maximal 25 Wörter, freundlich und konkret. Unterschiedliche Einstiege. Keine Kundennamen, Erfolge, Umweltsiegel, Verkaufszahlen oder Termine erfinden. Keine Veröffentlichung. Gib zum Schluss alle verwendeten Tatsachen in einer Liste aus.',
 'Nur das beschriebene Foto und die bestätigte Situation verwenden.','Entferne unbelegte Wertungen wie „perfekt“ und „garantiert“.'),
 ('Übersetzen mit unveränderten Fakten','Alle · Textchat',
 'Übersetze diesen fiktiven Veranstaltungstext freundlich ins Englische: „Papierfunke-Ideenatelier am 06.11.2026 von 16 bis 18 Uhr im Raum Sonnenhof. Eintritt frei. Keine Anmeldung vorgesehen.“ Erhalte den Raumnamen. Schreibe das Datum als 6 November 2026, damit Monat und Tag eindeutig sind. Gib Übersetzung und eine Faktenvergleichstabelle aus. Keine neue Information hinzufügen.',
 'Datum 6 November, 16–18 Uhr, Raumname und Anmeldung vergleichen.','Korrigiere ausschließlich Abweichungen in der Faktenvergleichstabelle.'),
 ('Ein Miniquiz aus einem festen Text','Alle · Textchat',
 'Erstelle ein Miniquiz ausschließlich zu diesem fiktiven Design-Merktext: „Ein Prototyp ist ein Entwurf zum Ausprobieren. Ein Export ist eine ausgegebene Datei. Ein Designsystem enthält gemeinsame Gestaltungsregeln.“ Genau drei Fragen mit je drei Antwortmöglichkeiten, jeweils nur eine richtig. Noch keine Lösung direkt unter der Frage. Danach einen getrennten Lösungsteil mit je einem Erklärungssatz. Keine Make-Fragen und keine neuen Produktbehauptungen ergänzen.',
 'Alle Lösungen müssen unmittelbar aus dem Merktext hervorgehen.','Ersetze Fragen, die Zusatzwissen benötigen, durch reine Verständnisfragen.'),
 ('Ein Arbeitszettel für den nächsten guten Entwurf','Alle · Textchat',
 'Erstelle eine wiederverwendbare einseitige Arbeitsanweisung für fiktive Team-Aushänge. Regeln: bestätigte Fakten zuerst sammeln, Zielgruppe nennen, eine klare Überschrift, Termin sichtbar, maximal drei Inhaltsblöcke, Text separat bearbeitbar, Fakten und Export prüfen. Ausgabe: sieben nummerierte Schritte, eine kurze Prüfliste und ein ausgefülltes Beispiel mit „Teamnachmittag, 30.10.2026, 15 Uhr, Raum Sonnenhof“. Keine Softwareinstallation, Kontoverbindung oder Veröffentlichung vornehmen.',
 'Anleitung nachvollziehbar, Beispiel korrekt, keine Aktion als ausgeführt behauptet.','Kürze auf eine Seite und ergänze nur konkret überprüfbare Kriterien.'),
]
assert len(PROMPTS)==20
for i,(title,where,prompt,check,repair) in enumerate(PROMPTS,1):
 add(f'prompt-{i:02}',f'{i:02} · {title}',[('p','Wo einsetzen: '+where+'.'),('prompt',prompt),('check',check),('h','Korrektur im selben Gespräch'),('prompt',repair),('note','Der enthaltene Beispielsfall ist erfunden. Für eigene Projekte nur bestätigte und erlaubte Angaben einsetzen.')],f'Zusatzprompt {i} von 20 · kopieren, prüfen, verfeinern')
add('abschluss','Was du aus jedem Entwurf mitnimmst',[
 ('table',(['Aufbewahren','Damit es weitergeht'],[['Der verwendete Auftrag','Du kannst ihn später gezielt ändern.'],['Die bearbeitbare Quelle','Texte und Formen bleiben korrigierbar.'],['Der sichtbare Export','Andere können das Ergebnis öffnen.'],['Offene Prüfungen','Niemand verwechselt Entwurf mit Freigabe.']])),
 ('p','Die fünf Praxisfälle und zwanzig Zusatzprompts gehören zum Bonus. Sie sind keine Make-Übungen und keine Hausaufgabe für Montag.'),
 ('h','Aktualität und Nachweise'),('p','Redaktioneller Stand: 23.10.2026. Produktwege und Designalternativen wurden anhand offizieller Quellen recherchiert. Die Prompts sind eigens formulierte Arbeitsvorlagen; ihre Ergebnisse hängen von Werkzeug, Zugang und Eingabe ab.'),
 ('source',('C1','Claude: Design-Einstieg','https://support.claude.com/en/articles/14604416-get-started-with-claude-design')),
 ('source',('G1','Google: Stitch','https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/')),
 ('source',('A2','Canva: Druckränder und Beschnitt','https://www.canva.com/help/margins-bleed-crop-marks/'))])
