"""Freitag 23.10.2026: zehn Design- und zehn reine Make-Vorbereitungsstationen."""
DATE='23.10.2026'
SOURCE_FILE='KIAutomSpez_1_16_Claude_Design.pdf'
PDF='Lernheft_Tag19_Design-und-Make-Ausblick.pdf'
BONUS_PDF='Bonusheft_KI-Ideen-und-20-Prompts.pdf'
SOURCES={
 'C1':('Claude: aktueller Einstieg in Design','https://support.claude.com/en/articles/14604416-get-started-with-claude-design'),
 'C2':('Claude: Designsysteme und eigene Zugänge','https://support.claude.com/en/articles/14604397-set-up-your-design-system-in-claude-design'),
 'C3':('Claude: Wechsel der bisherigen Design-Oberfläche','https://support.claude.com/en/articles/17440474-move-from-standalone-claude-design-to-claude'),
 'G1':('Google: Stitch, Canvas, DESIGN.md und Übergabe','https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/'),
 'A1':('Canva: Magic Design','https://www.canva.com/magic-design/'),
 'A2':('Canva: Ränder, Beschnitt und Schnittmarken','https://www.canva.com/help/margins-bleed-crop-marks/'),
 'M1':('Make: Module als Bausteine','https://help.make.com/types-of-modules'),
 'M2':('Make: Informationen zuordnen (Mapping)','https://help.make.com/mapping'),
 'M3':('Make: Start und Zeitplan','https://help.make.com/schedule-a-scenario'),
 'M4':('Make: Credits und Verbrauch','https://help.make.com/credits'),
}
PAGES=[]
def add(key,title,blocks,slides=(),part='design'):
 PAGES.append(dict(key=key,title=title,deck=('Design · ' if part=='design' else 'Make · nur Vorbereitung · ')+DATE,blocks=blocks,slides=list(slides),part=part))

add('start','Von der Idee zum sichtbaren Entwurf',[
 ('p','Heute verbinden wir zwei Gedanken: Erst gestalten wir eine Idee verständlich. Dann schauen wir voraus, wie wiederkehrende Arbeit ab Montag mit Make geordnet werden kann.'),
 ('table',(['Erste Hälfte: Design','Zweite Hälfte: Make-Ausblick'],[['10 Lernstationen: Claude Design, Google Stitch und Canva.','10 Lesestationen: sehr einfache Begriffe und Alltagsbilder.'],['Beschreiben, ansehen, gezielt verbessern und prüfen.','Verstehen, was nächste Woche auf uns zukommt.'],['Eine kleine Design-Idee darf heute entstehen.','Heute keine Übungen, kein Konto anlegen und nichts verbinden.']])),
 ('note','Die 50/50-Aufteilung bezieht sich auf die 20 Lernstationen und die geplante Aufmerksamkeit. Folienverzeichnis und Quellen stehen zusätzlich im Anhang. Make startet praktisch erst am Montag, 26.10.2026.'),
 ('p','Die Design-Vorlage umfasst 20 Folien, Ausgabe Juli 2026. Alle Seiten sind im Anhang zugeordnet. Produktänderungen sind als Aktualisierung gekennzeichnet. Alle Beispiele mit Nordlicht, Luna und Papierfunke sind erfunden.')],(1,2))

add('prinzip','Ein Wunsch wird ein erster Entwurf',[
 ('p','Stell dir vor, du erzählst einer Gestalterin von einem Teamnachmittag. Sie zeigt dir eine erste Seite. Du siehst sofort, ob Überschrift, Bilder und Reihenfolge passen. Genau dieses gemeinsame Verfeinern ist die Idee der Folien.'),
 ('h','Die drei Schritte'),('p','Beschreiben: Für wen ist die Arbeit und was soll sie erreichen?\nAnsehen: Ist die wichtigste Aussage sofort erkennbar?\nVerbessern: Eine konkrete Änderung nennen und erneut ansehen.'),
 ('p','Eine Leinwand, oft Canvas genannt, ist der sichtbare Arbeitsbereich. Ein Prototyp ist ein ausprobierbarer Entwurf. Ein klickbarer Button kann dabei nur einen vorbereiteten nächsten Bildschirm zeigen; er beweist noch keine funktionierende Buchung.'),
 ('prompt','Entwirf einen übersichtlichen digitalen Aushang für den fiktiven Nordlicht-Teamnachmittag. Zielgruppe: Kolleginnen und Kollegen ohne Vorwissen. Fakten: 30.10.2026, 15 Uhr, Raum Sonnenhof; Thema: Ideen teilen; Teilnahme freiwillig. Zeige zuerst die wichtigste Information, dann drei kurze Hinweise. Ruhige Farben, große lesbare Schrift, keine erfundenen Kontaktdaten. Falls du nur Text ausgeben kannst, liefere eine klare Layoutbeschreibung statt eine erstellte Datei zu behaupten.'),
 ('check','Beim Design: Kann man in fünf Sekunden erkennen, worum es geht, wann es stattfindet und für wen es gedacht ist?')],(3,4))

add('zugang','Wo du Claude Design heute findest',[
 ('note','Aktualisiert am 23.10.2026: Die ältere Folienaussage „nur bezahlte Pläne, Enterprise aus“ ist für Design nicht mehr allgemein richtig. Der aktuelle Einstieg beschreibt Design in Chats und im Artifacts-Bereich, auch im Free-Plan. Organisationsfreigaben und Nutzungsgrenzen bleiben relevant. [C1]'),
 ('p','Die frühere separate Oberfläche claude.ai/design wird laut Hersteller am 14.12.2026 geschlossen. Bestehende Arbeiten benötigen den vorgesehenen Umzugsweg; das ist kein Anlass, sie heute zu löschen. [C3]'),
 ('p','Wichtig: Ein eigenes wiederverwendbares Designsystem ist eine gesonderte Funktion. Der aktuelle Leitfaden nennt Pro, Max, Team und Enterprise. Bei Enterprise muss diese Funktion gesondert freigeschaltet sein. „Design ist verfügbar“ heißt deshalb nicht „jede Designsystem-Funktion ist verfügbar“. [C2]'),
 ('h','Wenn die Oberfläche anders aussieht'),('p','Im Chat das gewünschte visuelle Ergebnis beschreiben oder nach dem Design- bzw. Artifacts-Bereich suchen. Falls er im eigenen Zugang fehlt, denselben Auftrag als Textstruktur vorbereiten. Keine kostenpflichtige Buchung für diese Lernstation nötig.'),
 ('p','Claude Code kann je nach aktueller Oberfläche über /design an dieser Arbeit anknüpfen. Die Folienidee einer Übergabe bleibt damit relevant; Menünamen aus einem Video sind keine dauerhafte Anleitung. [C1]')],(10,12))

add('brief','Gutes Material schlägt einen Zaubersatz',[
 ('p','Ein brauchbarer Auftrag enthält Zielgruppe, Anlass, bestätigte Inhalte, gewünschtes Format und ein paar Gestaltungsregeln. Eine eigene Skizze oder freigegebene Vorlage kann mehr helfen als zehn Adjektive wie „modern, premium, wow“.'),
 ('table',(['Material','So wird es nützlich'],[['Text und Dokumente','Nur relevante bestätigte Fakten; lange Unterlagen mit Prioritäten versehen.'],['Bilder und Screenshots','Erklären, was daran gefällt: etwa klare Reihenfolge oder viel Freiraum.'],['Vorhandene Website oder Code','Als erlaubte Referenz nutzen; konkrete Importmöglichkeiten im eigenen Zugang prüfen.'],['Eigene Marke','Farben, freigegebene Schriften und Logos mitgeben. Fehlende Angaben offenlassen.']])),
 ('note','Die Folien nennen verschiedene Datei- und Importwege. Welches Format tatsächlich angenommen wird, zeigt die verwendete Oberfläche. Eine hochgeladene Datei ist nicht automatisch vollständig gelesen.'),
 ('prompt','Prüfe vor dem Entwurf diese Vorgaben: Nordlicht-Teamnachmittag, 30.10.2026, 15 Uhr, Raum Sonnenhof, freiwillig. Stil: freundlich und ruhig. Format: eine Bildschirmseite. Nenne zuerst fehlende Informationen, die wirklich nötig sind. Erfinde keine Anmeldung, Preise oder Personen. Erstelle danach eine erste Struktur mit Überschrift, Terminblock und drei kurzen Abschnitten.')],(5,11))

add('regeln','Ein kleiner Stilzettel für Wiedererkennung',[
 ('p','Ein Designsystem ist wie ein gemeinsames Rezeptbuch: Welche Farben, Schriften, Abstände und Bausteine sollen wiederkehren? Mit guten eigenen Vorlagen kann das Team konsistenter arbeiten. Es bleibt nötig zu prüfen, ob diese Regeln tatsächlich eingehalten werden. [C2]'),
 ('code','Eigener Stilzettel: Nordlicht\nStimmung: freundlich, ruhig, klar\nFarben: dunkelgrün, cremeweiß, ein warmer Akzent\nSchrift: gut lesbare serifenlose Schrift mit erlaubter Nutzung\nAufbau: eine Hauptüberschrift, kurze Abschnitte, viel Freiraum\nRegel: bestätigte Fakten wörtlich richtig übernehmen'),
 ('note','Die Folie schlägt vor, eine fremde Marken-DESIGN.md per Prompt zu „bereinigen“. Eine KI kann daraus keine Rechtefreigabe machen. Wir starten mit eigenen Regeln. Fremde Markennamen zu entfernen belegt weder erlaubte Nutzung noch ausreichenden Abstand.'),
 ('p','DESIGN.md ist zunächst eine Textdatei mit Gestaltungsregeln. Google beschreibt für Stitch den Import und Export solcher Regeln. Eine Datei mit diesem Namen wirkt nicht in jedem Werkzeug automatisch. [G1]'),
 ('check','Beim Design: Wird dieselbe Farbe für dieselbe Funktion benutzt? Sind zwei Überschriften derselben Ebene gleich gestaltet?')],(7,13,14))

add('feedback','So wird „schöner“ zu einer klaren Änderung',[
 ('table',(['Unklar','Konkret und prüfbar'],[['Mach es besser.','Der Termin soll direkt unter der Überschrift stehen.'],['Mehr Wow.','Ein starkes Hauptmotiv, weniger kleine Dekorationen.'],['Alles wirkt komisch.','Die drei Karten sollen gleich breit sein; Texte linksbündig.'],['Mach es barrierefrei.','Erhöhe die Textlesbarkeit und prüfe Tastaturbedienung; nenne verbleibende Probleme.']])),
 ('p','Die Folien unterscheiden Änderungen im Gespräch, direkte Bearbeitung, Kommentare und Feinregler. Nutze die Möglichkeit, die dein Zugang anbietet. Ein Kommentar hilft für die genaue Stelle; eine globale Stiländerung gehört in den gemeinsamen Auftrag.'),
 ('prompt','Verbessere nur die Lesbarkeit des vorhandenen Entwurfs: Termin direkt unter die Hauptüberschrift, maximal drei kurze Inhaltsblöcke, keine Schrift über einem unruhigen Bild. Behalte die bestätigten Fakten und die bisherige Farbpalette bei. Liste anschließend die tatsächlich geänderten Stellen und noch ungeprüfte Punkte auf.'),
 ('p','Eine CLAUDE.md ist im Folienbeispiel eine gewünschte Erinnerung an Feedback. Dass eine Datei existiert, beweist ihre spätere Berücksichtigung nicht. Für dieses Design reicht ein sichtbarer Stilzettel plus erneuter Vergleich.')],(6,13))

add('stitch','Google Stitch: ein anderer Weg zur Oberfläche',[
 ('p','Stitch richtet sich besonders an Entwürfe für Websites und Apps. Google beschreibt eine freie Arbeitsfläche, Eingaben aus Text, Bildern oder Code sowie verknüpfbare Bildschirme für einen Prototyp. [G1]'),
 ('p','Für Carmen kann das eine übersichtliche Teamseite sein. Ingo sieht, wie eine Druckanfrage online aussehen könnte. Tabea kann eine Projektübersicht mit klaren Vorschaukarten skizzieren. Das sind unsere Anwendungsideen, keine gemessene Rangliste.'),
 ('prompt','Entwirf in Stitch eine deutsche mobile Startseite für die fiktive Papierfunke-Werkstatt. Angebot: kleine Druckideen gemeinsam planen. Ziel: Besucher verstehen den Ablauf. Drei Abschnitte: Idee besprechen, Entwurf prüfen, Produktion anfragen. Eine Hauptaktion „Ablauf ansehen“, die zum Ablaufabschnitt führt. Ruhiges Cremeweiß und Dunkelgrün. Keine Preise, Bewertungen, Kundennamen oder echte Anmeldung. Zeige zwei unterschiedliche Layoutvarianten.'),
 ('note','Stitch kann laut Google Designregeln und Entwürfe an weitere Werkzeuge übergeben, darunter Antigravity. Ein Export oder klickbarer Ablauf ist noch kein geprüfter veröffentlichter Webdienst. [G1]'),
 ('check','Beim Vergleich: dieselben Fakten in beiden Werkzeugen verwenden. Zuerst Verständlichkeit vergleichen, danach Dekoration.')],(8,9))

add('wahl','Welches Werkzeug passt zu welchem Ergebnis?',[
 ('table',(['Dein Ergebnis','Ein sinnvoller Start'],[['Entwurf im Gespräch weiterentwickeln','Claude Design: Inhalte und Gestaltung gemeinsam verfeinern. [C1]'],['Website-/App-Oberfläche vergleichen','Google Stitch: Varianten und Bildschirmabläufe. [G1]'],['Flyer oder Social-Post bearbeiten','Canva: Layoutumgebung und Vorlagen; Magic Design als möglicher Einstieg. [A1]'],['Entwurf zu funktionierender Software machen','Zum Beispiel Claude Code, Codex oder Antigravity im passenden Projekt; Umsetzung anschließend testen.']])),
 ('p','Der Ablauf zählt mehr als der Name: Erst die Aufgabe klären, dann ein passendes Werkzeug wählen. Ein normales Textchat-System kann dafür Texte und ein Gestaltungskonzept liefern. Ohne Bild- oder Dateiwerkzeug erzeugt es damit noch kein fertiges Layout.'),
 ('p','Für Ingo ist eine lesbare Druckvorlage wichtiger als ein Effekt. Für Carmen eine verständliche Seite mit sinnvoller Hauptaktion. Für Tabea eine starke Bildhierarchie mit bearbeitbaren Texten.'),
 ('note','Bei Canva prüfst du den vorgesehenen Export, die tatsächlichen Bildrechte und die Vorgaben der Druckerei. Beschnitt bedeutet Hintergrund über den späteren Schnittrand hinaus, Sicherheitsabstand schützt Text im Inneren. Die konkreten Maße gibt die Produktion vor. [A2]')],(8,9,11))

add('deck','Ein kleines Deck nach der Folienmethode',[
 ('p','Die Folienaufgabe kombiniert drei Vorbereitungen: Gestaltungsregeln, ein wiederverwendbares Gerüst und inhaltliche Stichpunkte. Das spart nur dann Zeit, wenn die Inhalte stimmen und das Gerüst zur Aufgabe passt. Ein bestimmtes Modell oder eine maximale Denkstufe ist keine Voraussetzung für den ersten Versuch.'),
 ('prompt','Erstelle einen Entwurf für vier Workshop-Folien zum Thema „Zeitmanagement ohne Stress“ für ein fiktives Nordlicht-Team. Inhalt: 1. Heute eine wichtigste Aufgabe wählen. 2. Einen ungestörten 25-Minuten-Block planen. 3. Nachrichten in vereinbarten Zeitfenstern lesen. 4. Am Ende einen nächsten Schritt notieren. Stil: dunkelgrün, cremeweiß, große lesbare Schrift, pro Folie ein Gedanke. Kein erfundener Produktivitätsnachweis. Liefere vier sichtbare Folien, falls dein Werkzeug das unterstützt; sonst vier klar abgegrenzte Folientexte samt Layoutbeschreibung.'),
 ('h','Ein Ergebnis richtig übergeben'),('p','Die bearbeitbare Quelle, den sichtbaren Export und offene Punkte zusammen ablegen. Export anschließend öffnen. HTML, PDF und Präsentationsdatei haben unterschiedliche Eigenschaften; der verfügbare Export hängt vom Werkzeug ab.'),
 ('note','Optionale Videos aus den Folien sind Vertiefung, keine Pflicht und kein Nachweis heutiger Menüs. Die Video-Karten bleiben im Original erhalten. [Originalfolien 15–20]')],(13,15,16,17,18,19,20))

add('bruecke','Erst gestalten, dann den Ablauf verstehen',[
 ('p','Ein ansprechender Entwurf beantwortet: Wie soll etwas aussehen und verstanden werden? Ein Ablauf beantwortet: Was soll nach einem Ereignis passieren? Diese Fragen ergänzen sich.'),
 ('table',(['Design heute','Ausblick auf Montag'],[['Ein Anfrageformular als sichtbaren Entwurf zeigen.','Verstehen, woher eine Anfrage kommt und wohin Informationen gehen.'],['Ein Bestätigungsfenster gestalten.','Unterscheiden, ob nur ein Entwurf gezeigt oder wirklich etwas gespeichert wurde.'],['Eine klare Inhaltsstruktur entwickeln.','Denselben Informationsweg wiederholt und nachvollziehbar ausführen.']])),
 ('check','Design-Abschluss: Fakten richtig? Wichtigstes sofort sichtbar? Text lesbar? Export öffnet sich? Bearbeitbare Quelle vorhanden?'),
 ('p','Die nächsten zehn Stationen liest du nur als Vorschau. Du brauchst Make heute nicht zu öffnen und keine Aufgabe darin zu lösen.'),
 ('note','Montag ist der praktische Start. Heute geht es darum, die Begriffe dann schon einmal gehört zu haben.')],(9,11,12))

add('make-start','Make ist wie eine kleine Arbeitsstraße',[
 ('p','Stell dir eine Poststelle vor: Eine Information kommt an, wird am passenden Arbeitsplatz bearbeitet und landet am richtigen Ziel. Make kann solche vorher festgelegten Abläufe zwischen Anwendungen ausführen.'),
 ('p','Das ist oft Automatisierung: Wiederkehrende Schritte werden nach Regeln erledigt. Nicht jeder Schritt braucht KI. „Vorname in eine Begrüßung einsetzen“ ist zum Beispiel eine klare Zuordnung, keine kreative Denkaufgabe.'),
 ('flow',['Eine Information kommt an','Ein Schritt verarbeitet sie','Ein Ergebnis liegt vor']),
 ('note','Nur ein Erklärbild. Hier wird nichts ausgeführt, gespeichert oder versendet. Alle praktischen Make-Schritte beginnen am Montag.'),
 ('h','Warum wir klein anfangen'),('p','Ein winziger verständlicher Ablauf ist leichter zu erklären als zehn verbundene Dienste. Erst wenn Quelle, Schritt und Ergebnis klar sind, lohnt sich die nächste Verbindung.')],part='make')

add('szenario','Ein Szenario ist der ganze Ablauf',[
 ('p','In Make heißt ein zusammenhängender Ablauf Szenario, auf Englisch Scenario. Gemeint ist die ganze Kette, nicht nur ein einzelner Baustein.'),
 ('h','Alltagsbild: eine Rezeptkarte'),('p','„Zutaten abwiegen, mischen, backen“ ist der gesamte Ablauf. Jeder einzelne Handgriff hat eine Aufgabe. So ähnlich besteht ein Szenario aus Modulen. [M1]'),
 ('flow',['Start des Ablaufs','Vereinbarte Schritte','Erwartetes Ergebnis']),
 ('p','Ein Szenario braucht ein klares Ziel. „Irgendwas automatisch machen“ ist dafür zu ungenau. „Eine neue Anfrage in einer Übersicht erfassen“ beschreibt schon Quelle und Ergebnis.'),
 ('note','Diese Beispiele erklären Begriffe. Sie sind keine Bauanleitung und sollen heute nicht umgesetzt werden.')],part='make')

add('modul','Ein Modul macht einen einzelnen Schritt',[
 ('p','Ein Modul ist ein Baustein im Szenario. Es hat eine bestimmte Aufgabe, etwa eine Information holen oder einen Eintrag anlegen. Das Symbol der Anwendung sagt noch nicht, welche einzelne Handlung gewählt ist. [M1]'),
 ('table',(['Alltag','In einem späteren Ablauf'],[['Ein Brief kommt in der Poststelle an.','Information wird verfügbar.'],['Jemand liest die Anschrift.','Ein Schritt nutzt bestimmte Angaben.'],['Der Brief kommt ins passende Fach.','Information wird am vorgesehenen Ziel abgelegt.']])),
 ('p','Begriffe wie „Abrufen“, „Erstellen“ und „Ändern“ meinen verschiedene Handlungen. Ein vorhandenes Dokument lesen ist etwas anderes, als es zu überschreiben.'),
 ('note','Heute genügt dieses Bild: Ein Baustein = eine überschaubare Aufgabe. Die Auswahl im Programm schauen wir uns Montag gemeinsam an.')],part='make')

add('ausloeser','Was setzt etwas in Gang?',[
 ('p','Im Alltag ist eine Türklingel ein Auslöser: Etwas passiert und eine Reaktion beginnt. Bei einer Automatisierung kann zum Beispiel eine neue freigegebene Anfrage ein Anlass sein. Viele solche Startbausteine heißen Trigger. [M1]'),
 ('p','Nicht jeder Ablauf muss rund um die Uhr laufen. Es gibt auch bewusst angestoßene Durchläufe. Entscheidend ist, dass klar ist, wann der Ablauf beginnen soll.'),
 ('h','Ein Beispiel nur zum Verstehen'),('p','„Wenn eine neue freigegebene Anfrage vorliegt, soll sie in der internen Übersicht erscheinen.“ Der erste Satzteil beschreibt den Anlass. Der zweite das gewünschte Ergebnis.'),
 ('note','Ein Trigger ist nicht automatisch eine KI. Er erkennt bzw. erhält ein vereinbartes Ereignis. Die genaue technische Variante ist heute noch nicht nötig.')],part='make')

add('daten','Daten sind erst einmal einzelne Angaben',[
 ('p','Das Wort Daten klingt groß. Hier können damit ganz kleine Dinge gemeint sein: ein Vorname, ein Datum, eine Stückzahl oder ein kurzer Betreff.'),
 ('table',(['Bezeichnung eines Feldes','Beispielwert'],[['Vorname','Luna'],['Produkt','Flyer'],['Stückzahl','200'],['Termin','Noch nicht bestätigt']])),
 ('p','Eine Feldbezeichnung ist das Etikett. Der Wert ist das, was auf dem Zettel steht. „Stückzahl“ und „200“ sind deshalb nicht dasselbe.'),
 ('p','Make gibt Informationen zwischen Schritten weiter. Ein zusammengehöriges Informationspaket wird oft Bundle genannt. Für Montag reicht: Ein Päckchen mit den Angaben, die ein Schritt bekommen oder erzeugt hat. [M2]'),
 ('note','„Noch nicht bestätigt“ bleibt offen. Fehlende Informationen dürfen nicht unbemerkt als sichere Aussage weitergegeben werden.')],part='make')

add('zuordnen','Mapping heißt: die richtige Angabe ins richtige Feld',[
 ('p','Wenn auf einem Formular „Vorname“ steht und im nächsten Schritt eine Begrüßung entstehen soll, muss die passende Angabe an die richtige Stelle gelangen. Diese Zuordnung heißt in Make Mapping. [M2]'),
 ('flow',['Vorname: Luna','Vorname an die Begrüßung zuordnen','Hallo Luna']),
 ('p','Das Bild erklärt eine Zuordnung. Es ist kein heute auszuführender Test und benötigt keine Kontoanmeldung.'),
 ('h','Warum das wichtig ist'),('p','Wenn versehentlich eine Stückzahl im Namensfeld landet, kann technisch alles durchlaufen und trotzdem ein unsinniges Ergebnis entstehen. Deshalb prüfen wir später sowohl die Verbindung als auch den Inhalt.'),
 ('note','Mapping ist keine Zauberei: Es beschreibt, welche vorhandene Information an welcher Stelle weiterverwendet wird.')],part='make')

add('verbindungen','Eine Verbindung ist eine erteilte Erlaubnis',[
 ('p','Wenn zwei Anwendungen zusammenarbeiten sollen, benötigt der Ablauf gegebenenfalls eine passende Verbindung. Connection ist das englische Wort dafür. Sie kann Zugriff auf ein bestimmtes Konto oder bestimmte Inhalte erlauben.'),
 ('p','Alltagsbild: Ein Schlüssel öffnet eine vereinbarte Tür. Er bedeutet nicht, dass jemand in jedem Raum alles tun soll. Deshalb passen Zugang, freigegebene Daten und gewünschte Handlung zusammen.'),
 ('h','Was wir heute bewusst noch nicht brauchen'),('p','Keine E-Mail-Verbindung, keinen Zugang zu echten Kundenunterlagen und keine selbst gekauften Zusatzdienste. Welche Umgebung am Montag genutzt wird, legen wir gemeinsam fest.'),
 ('note','Zum Verstehen sind keine Passwörter oder API-Schlüssel nötig. Ein API-Schlüssel ist ein technischer Zugangsschlüssel; er gehört nicht in einen geteilten Chat oder ein Lernheft.')],part='make')

add('kontrolle','Ein Durchlauf und ein Zeitplan sind verschieden',[
 ('p','Ein einzelner Durchlauf beantwortet später: Was passiert jetzt mit diesen Eingaben? Ein Zeitplan legt dagegen fest, wann bzw. wie häufig der Ablauf automatisch laufen soll. [M3]'),
 ('table',(['Begriff','Einfache Bedeutung'],[['Einzelner Durchlauf','Einmal den vorgesehenen Weg ausführen.'],['Zeitplan','Wiederkehrende Ausführung vereinbaren.'],['Eingabe','Das geht in einen Schritt hinein.'],['Ausgabe','Das kommt aus dem Schritt heraus.']])),
 ('p','Ein grüner Status sagt allein noch nicht, dass die richtige Person, der richtige Inhalt oder das richtige Ziel gewählt wurde. Später schauen wir uns deshalb Eingabe und Ausgabe an.'),
 ('note','Hier gibt es keine Klickfolge. Zeitpläne werden heute weder eingerichtet noch aktiviert. Montag beginnen wir mit einem kleinen kontrollierten Ablauf.')],part='make')

add('einordnung','KI kann helfen, klare Regeln bleiben wichtig',[
 ('p','Eine KI kann beispielsweise aus einem freigegebenen Text einen Entwurf für eine Zusammenfassung machen. Ein anderer Schritt könnte diesen Entwurf an einem vorgesehenen Ort ablegen. Das sind zwei verschiedene Aufgaben.'),
 ('table',(['Aufgabe','Was daran zählt'],[['Eine vorhandene Zahl übertragen','Die richtige Zahl im richtigen Feld.'],['Einen Text zusammenfassen','Inhaltstreue und klar sichtbare Unsicherheiten.'],['Eine Information weitergeben','Passendes Ziel und erlaubte Handlung.']])),
 ('p','Make bezeichnet seine Verbrauchseinheit heute als Credits. Wie viel ein Ablauf verbraucht, hängt von den verwendeten Funktionen ab; insbesondere KI kann anders berechnet werden als einfache Schritte. Heute muss niemand dafür etwas buchen. [M4]'),
 ('note','Mehr Bausteine bedeuten nicht automatisch ein besseres Ergebnis. Der beste erste Ablauf ist der, den alle Beteiligten verstehen.')],part='make')

add('montag','Am Montag geht es gemeinsam los',[
 ('p','Am Montag, 26.10.2026, beginnt Make praktisch. Heute musst du dafür nichts einrichten, nichts üben und keine Hausaufgabe im Programm erledigen.'),
 ('h','Der rote Faden für nächste Woche'),('p','Wir sehen gemeinsam die Arbeitsfläche. Wir lernen an einem kleinen Ablauf, wie Bausteine verbunden sind. Wir unterscheiden Eingabe und Ausgabe. Erst danach werden größere Anwendungsfälle verständlich.'),
 ('table',(['Was du heute schon gehört hast','In anderen Worten'],[['Szenario','Der ganze Arbeitsweg.'],['Modul','Ein einzelner Baustein.'],['Trigger','Ein vereinbarter Startanlass.'],['Mapping','Informationen passend zuordnen.'],['Verbindung','Erlaubter Zugang zu einer Anwendung.']])),
 ('p','Für Ingo könnten später Anfragen und Druckdaten interessant werden, für Carmen Teamabläufe und Website-Anfragen, für Tabea Projektinformationen und Freigaben. Das sind Ausblicke, noch keine eingerichteten Automationen.'),
 ('note','Heute endet die Vorbereitung. Kein Make-Quiz, keine Simulation und keine praktische Aufgabe sind Teil dieses Hefts.')],part='make')

assert len(PAGES)==20 and sum(p['part']=='make' for p in PAGES)==10

SLIDES=[
 (1,'Einordnung','Die Vorlage gehört zu Modul 1, Lektion 16, Ausgabe Juli 2026. Heute ergänzen wir aktuelle Produktänderungen und einen getrennten Make-Ausblick.'),
 (2,'Design ohne Vorwissen','Die Grundidee ist ein Gespräch über ein sichtbares Ergebnis. Du musst nicht alle Fachbegriffe vorher kennen.'),
 (3,'Was Design erzeugen soll','Die Vorlage nennt visuelle Entwürfe wie Seiten, Präsentationen und Prototypen. Ein Entwurf bleibt anschließend zu prüfen.'),
 (4,'Beschreiben, ansehen, verbessern','Das Grundmuster ist eine wiederholte Rückmeldung am sichtbaren Ergebnis, kein magischer Einmalprompt.'),
 (5,'Mit Material starten','Eigene bestätigte Inhalte und erlaubte Referenzen helfen. Importformat und tatsächliche Verarbeitung im benutzten Zugang prüfen.'),
 (6,'Änderungen präzise formulieren','Gespräch, direkte Bearbeitung und Kommentare sind unterschiedliche Wege zum Feedback. Genaue Änderungen sind leichter zu prüfen.'),
 (7,'Gemeinsame Gestaltungsregeln','Ein Designsystem bündelt Farben, Schriften und Bausteine. Seine Verfügbarkeit und seine tatsächliche Anwendung separat prüfen. [C2]'),
 (8,'Zugänglichkeit und Prototypen','Ein interaktiver Entwurf kann eine Idee verständlich machen. Die experimentellen Medienbeispiele der Vorlage sind keine Zusage für jedes heutige Konto.'),
 (9,'Export und Weiterarbeit','Ergebnis und bearbeitbare Quelle unterscheiden. Eine Übergabe an ein Programm ersetzt keine Prüfung der fertigen Anwendung.'),
 (10,'Zugang: heute anders','Die Juli-Angaben zum bezahlten Zugang und zur Enterprise-Voreinstellung sind überholt. Aktuelles Design und Designsysteme getrennt betrachten. [C1, C2, C3]'),
 (11,'Grenzen gehören dazu','Schwache Eingaben, widersprüchliche Inhalte und ungeprüfte Gestaltung werden durch einen Generator nicht automatisch richtig.'),
 (12,'Der Kern','Sprache hilft vom Wunsch zum Entwurf. Fachliche und gestalterische Entscheidungen bleiben Teil des Prozesses.'),
 (13,'Workshop-Deck','Eigene Regeln, ein Gerüst und bestätigte Stichpunkte vorbereiten. Fremde Markenregeln werden nicht durch einen Bereinigungsprompt freigegeben. Maximale Denkstufe und bestimmte Wartezeiten sind keine allgemeine Pflicht.'),
 (14,'DESIGN.md-Sammlung','Die Vorlage verlinkt eine externe Sammlung. Wir übernehmen daraus keine fremde Marke, sondern verwenden einen selbst formulierten Stilzettel.'),
 (15,'Video zur Deck-Methode','Optionaler Videohinweis. Die zugrunde liegende Idee sind vorbereitete Inhalte, Gestaltungsregeln und ein Gerüst; heutige Menüs anhand Herstellerhilfe prüfen.'),
 (16,'Optionale Videos','Trennseite zur freiwilligen Vertiefung. Keine zusätzliche Pflichtaufgabe.'),
 (17,'Kurzes Design-Video','Optionaler Erfahrungsbericht. Der Titel „2.0“ ist keine hier geprüfte Versions- oder Qualitätszusage.'),
 (18,'Längerer Design-Guide','Optionales Video mit Werbeverweisen. Werbung und Produktempfehlungen sind keine Unterrichtsvoraussetzung.'),
 (19,'Weiterer Design-Überblick','Optionaler Videohinweis. Inhalte des Videos wurden nicht als Herstellerbeleg übernommen.'),
 (20,'Ausführlicher Videokurs','Freiwillige Vertiefung; keine zweistündige Pflicht und keine Hausaufgabe für den Make-Start.')]

def course():
 return dict(titel='Designideen und ein leichter Make-Ausblick',unter='Lektion 16 · Freitag',datum=DATE,folien=SOURCE_FILE,folie_start=1,kurz='50% Design mit Alternativen · 50% reine Vorbereitung auf Montag',lernheft=PDF,
  learnings=[dict(id=f'l{i}',folie=0,satz=p['title'],erklaert=next(v for k,v in p['blocks'] if k=='p')) for i,p in enumerate(PAGES,1)],
  karten=[],test=[],begriffe=[('Canvas','Sichtbare Arbeitsfläche für einen Entwurf.'),('Prototyp','Entwurf zum Ansehen oder Ausprobieren.'),('Designsystem','Gemeinsame Regeln für das Aussehen.'),('Szenario','Der gesamte festgelegte Ablauf in Make.'),('Modul','Ein einzelner Baustein des Ablaufs.'),('Mapping','Angaben einer passenden nächsten Stelle zuordnen.')])
