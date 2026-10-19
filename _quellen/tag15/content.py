"""Redaktioneller Stand 19.10.2026. Quellen geprüft, keine Produkttests behauptet."""
DATE='19.10.2026'
SOURCES=[
('O1','OpenAI · Desktop und Codex','https://learn.chatgpt.com/docs/app'),
('O2','OpenAI · Preise und Nutzung','https://learn.chatgpt.com/docs/pricing'),
('O3','OpenAI · MCP','https://learn.chatgpt.com/docs/extend/mcp?surface=cli'),
('O4','OpenAI · Skills in Plugins','https://developers.openai.com/plugins/concepts/skills'),
('G1','Google · Antigravity im Überblick','https://www.antigravity.google/docs/overview'),
('G2','Google · Funktionen','https://www.antigravity.google/docs/features'),
('G3','Google · Preise','https://antigravity.google/pricing'),
('G4','Google · MCP','https://www.antigravity.google/docs/mcp'),
('G5','Google · Plugins','https://www.antigravity.google/docs/plugins'),
('A1','Anthropic · Claude Code im Überblick','https://code.claude.com/docs/en/overview'),
('A2','Anthropic · Desktop','https://code.claude.com/docs/en/desktop'),
('A3','Anthropic · Preise','https://claude.com/pricing'),
('A4','Anthropic · MCP','https://code.claude.com/docs/en/mcp'),
('A5','Anthropic · Plugins','https://code.claude.com/docs/en/plugins'),
('A6','Anthropic · Chat-Suche und Memory','https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context'),
('P1','HubSpot · MCP Server','https://developers.hubspot.com/ai-tools/mcp'),
('P2','Canva · Design-MCP','https://www.canva.dev/docs/apps/mcp/'),
('P3','Canva · Zugang, Rechte und Tarife','https://www.canva.dev/docs/apps/mcp/access/'),
('P4','Figma · kompatible Clients und Zugriffsarten','https://www.figma.com/mcp-catalog/'),
('P5','Figma · Werkzeuge','https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/'),
('P6','Microsoft · Playwright MCP','https://github.com/microsoft/playwright-mcp'),
('P7','HeyGen · Remote MCP, Anmeldung und Credits','https://www.heygen.com/en-gb/model-context-protocol'),
('P8','Remotion · offizielle Plugins','https://www.remotion.dev/docs/ai/plugins'),
('P9','Remotion · Agent Skills','https://www.remotion.dev/docs/ai/skills'),
]

# Blocks: p=Absatz, h=Zwischentitel, note=Merkfeld, prompt=kopierbarer Auftrag,
# table=(Spaltenüberschriften, Zeilen), check=Selbstcheck.
PAGES=[]
def page(key,title,deck,blocks):
 PAGES.append(dict(key=key,title=title,deck=deck,blocks=blocks))

page('start','Vom Chat zur kleinen Werkstatt','Lernheft · Tag 15 · Einführung Claude und Werkzeugvergleich',[
 ('p','Antigravity, Codex und Claude Code verständlich vergleichen. Kleine Helfer bauen, Ergebnisse selbst prüfen und passende Erweiterungen entdecken.'),
 ('h','Drei Arbeitswelten. Ein gemeinsamer Start.'),
 ('p','Ingo: Druck und Vertrieb. Carmen: Team, Business und Website am Mac. Tabea: Video, Design und kreative Arbeit. Alle Beispiele, Firmen und Zahlen sind erfunden.'),
 ('note','Heute zählt ein sichtbares Ergebnis: ein Angebotsrechner, eine Website-Demo oder ein Storyboard-Helfer. Vorkenntnisse im Programmieren sind dafür keine Eintrittskarte. Prüfen und Nachfragen gehören dazu.'),
 ('p','Mit sechs kurzen Missionen, sechs ausgewählten Erweiterungen, einem fairen Vergleichslabor und der Begleitung aller 28 Originalfolien.'),
 ('p','Recherche: 19.10.2026, offizielle Herstellerdokumentation. Empfehlungen sind didaktische Einschätzungen, kein eigener Leistungstest der drei Produkte. Verfügbarkeit hängt von Oberfläche, Tarif, Freigaben und Region ab.')])

page('route','Dein Weg durch das Heft','Erst verstehen · dann ausprobieren · danach begründen',[
 ('table',(['Station','Hier findest du sie'],[
 ['Werkzeuge verstehen','Seiten 3–8: Begriffe, Vergleich und Kosten'],
 ['Gemeinsam arbeiten','Seiten 9–10: Ablauf und Vergleichslabor'],
 ['Deine Missionen','Seiten 11–16: jeweils zwei Aufgaben pro Arbeitsbereich'],
 ['Erweiterungen entdecken','Seiten 17–21: Plugins, MCP, Zugang und Grenzen'],
 ['Wissen testen','Seiten 22–23: Quiz mit begründeten Antworten'],
 ['Alle Folien nachlernen','Seiten 24–37: Originalfolien 1–28, paarweise begleitet'],
 ['Quellen und Mitnahme','Seiten 38–41: Links, Eintragung und Transfer'] ])),
 ('h','Das kannst du anschließend erklären'),
 ('p','Du unterscheidest Modell, Chat, Arbeitsumgebung, Skill, Plugin und MCP. Du wählst einen passenden ersten Versuch für deinen Beruf und formulierst klare Prüfregeln. Du erkennst, ob die KI nur etwas beschreibt oder tatsächlich eine Datei verändert hat.'),
 ('h','So lernst du ohne zusätzlichen Zugang'),
 ('p','Die Missionen haben eine Chat-Variante. Du kannst etwa in einem normalen Langdock-Chat Entwürfe, Testfälle und kleine HTML-Texte erarbeiten. Das ersetzt keine echte Verbindung zu Canva oder HubSpot. Ohne verbundenes Werkzeug bleibt der Auftrag eine Vorbereitung.'),
 ('check','Vor dem Start: Nenne eine Arbeit, bei der du oft dieselben Angaben neu sortierst. Was wäre ein kleines, sichtbar prüfbares Ergebnis?')])

page('begriffe','Wer denkt, wer arbeitet, wer verbindet?','Ein Beispiel statt sechs Fremdwörter',[
 ('table',(['Begriff','Alltagsbild','Beispiel'],[
 ['Modell','Der Motor, der Antworten erzeugt','Ein Claude- oder GPT-Modell'],
 ['Chat','Das Gespräch am Schreibtisch','Du lässt einen Text umschreiben'],
 ['Coding-Agent','Eine Assistenz mit Werkzeugen','Sie liest Dateien und ändert einen Rechner'],
 ['Arbeitsumgebung','Die Werkstatt um die Assistenz','Antigravity, Codex oder Claude Code'],
 ['Skill','Ein wiederverwendbarer Arbeitszettel','So erstellen wir ein Storyboard'],
 ['MCP','Die vereinbarte Werkzeug-Schnittstelle','Ein angebundener Dienst liefert CRM-Daten'],
 ['Plugin','Ein installierbares Paket','Enthält zum Beispiel Skills und eine Verbindung'] ])),
 ('note','Claude ist nicht gleich Claude Code: claude.ai ist unter anderem eine Chat-Oberfläche. Claude Code ist ein Werkzeug für Arbeit an Projekten. Die API ist ein eigener technischer Zugang. Ein Abo bezahlt nicht automatisch jede API-Nutzung. [A1, A3]'),
 ('p','Beispiel: Ingo erklärt im Chat einen Mengenrabatt. Ein Agent baut daraus eine HTML-Datei. Ein Skill beschreibt die gewünschte Arbeitsweise. Erst eine eingerichtete MCP-Verbindung könnte passende Daten aus HubSpot holen. Eine Verbindung macht aus geratenen Zahlen keine geprüften Preise.'),
 ('p','Die Verpackung unterscheidet sich je Produkt. Ein gleichnamiger Skill oder MCP-Server kann übertragbar sein; ein Plugin-Paket und seine Einrichtung sind es nicht automatisch. [O3, O4, G5, A5]')])

page('vergleich','Drei Werkstätten im Vergleich','Herstellerfunktionen und unsere Einsatzideen auseinanderhalten',[
 ('table',(['Frage','Antigravity','Codex','Claude Code'],[
 ['Womit starte ich?','App, CLI oder IDE','Desktop, Web, CLI oder IDE je Zugang','Desktop, Terminal, IDE oder Web je Zugang'],
 ['Woran arbeitet es?','Projektdateien, Befehle, Vorschau','Dateien, Code und weitere Arbeitsmaterialien','Projektdateien, Code und Befehle'],
 ['Wie erweitere ich es?','Skills, Plugins und MCP','Skills, Plugins und MCP','Skills, Plugins und MCP'],
 ['Was ist mein Prüfpunkt?','Geänderter Stand und sichtbare Vorschau','Geänderte Dateien und ausgeführte Checks','Änderungsansicht und ausgeführte Checks'],
 ['Guter erster Versuch*','Eine interaktive Website-Demo','Ein kleiner Rechner oder Dateien-Helfer','Ein vorhandenes Projekt verständlich ändern'] ])),
 ('p','Funktionen: [G1, G2, O1, A1]. *Die letzte Zeile sind Vorschläge für den Unterricht. Alle drei können ähnliche Aufgaben bearbeiten. Kein Produkt gewinnt allein durch seinen Namen.'),
 ('h','Die drei Fragen vor der Entscheidung'),
 ('p','1. Was soll am Ende wirklich vorliegen: Text, bearbeitbare Datei oder laufende Anwendung? 2. Wo liegen die Ausgangsdaten, und wer darf darauf zugreifen? 3. Kannst du die Ausgabe fachlich und mit kleinen Testfällen prüfen?'),
 ('note','Ein Screenshot einer hübschen Seite beweist noch keine funktionierende Anwendung. Ein bestandener Beispieltest beweist noch keine fehlerfreie Lösung für alle Fälle.')])

page('antigravity','Antigravity: eine sichtbare Versuchswerkstatt','Google · App und Entwicklungsumgebungen',[
 ('p','Google beschreibt inzwischen eine eigenständige Antigravity-App, eine CLI und IDE-Angebote. Du arbeitest an einem Projekt; der Agent kann Werkzeuge einsetzen. Browser-Funktionen und überprüfbare Arbeitsartefakte unterstützen den Blick auf das Ergebnis. Die Oberflächen haben Unterschiede. [G1, G2]'),
 ('h','Unser Einstiegsvorschlag'),
 ('p','Carmen beschreibt eine fiktive Seite für ein Teamfrühstück. Der Agent erstellt eine kleine Vorschau. Sie prüft auf dem Handy, ob Text und Schaltflächen verständlich bleiben. Ingo kann denselben Ablauf für einen Mengenrechner nutzen; Tabea für eine klickbare Szenenauswahl.'),
 ('prompt','Baue in einem neuen Übungsordner eine einzelne HTML-Demo für ein fiktives Teamfrühstück. Drei Terminkarten, deutlich lesbare Texte und ein Button „Interesse merken“. Der Button zeigt nur lokal eine Bestätigung, speichert und sendet nichts. Erkläre zuerst in einfachen Worten deinen Plan. Zeige danach, welche Datei geändert wurde und wie ich die Demo öffne.'),
 ('h','Woran du weiterarbeiten kannst'),
 ('p','Wenn das Ergebnis nur als Bild erscheint: nach der bearbeitbaren Datei und der tatsächlichen Vorschau fragen. Wenn der Button keine Wirkung hat: den beobachteten Fehler mit Klickfolge melden. Einen funktionierenden Stand vor weiteren Änderungen sichern.'),
 ('check','Auf 390 Pixel Breite: keine abgeschnittenen Texte. Jeder Button ist per Tastatur erreichbar. Eine Bestätigung verspricht keine Anmeldung oder versendete Nachricht.')])

page('codex','Codex: aus einer Aufgabe wird eine Datei','OpenAI · unterschiedliche Oberflächen, gemeinsamer Arbeitsauftrag',[
 ('p','Die aktuelle OpenAI-Dokumentation führt Codex zusammen mit der ChatGPT-Desktop-Arbeitsumgebung. Daneben gibt es CLI-, IDE- und Web-Zugänge. Datei-, Browser- und Computerfunktionen hängen von der Oberfläche und den bereitgestellten Werkzeugen ab. Nicht jede Sitzung hat dieselben Möglichkeiten. [O1, O2]'),
 ('h','Unser Einstiegsvorschlag'),
 ('p','Ingo lässt einen kleinen Angebotsrechner erstellen und prüft dessen Rechnung selbst. Carmen kann eine Website-Änderung beschreiben. Tabea kann aus einer erfundenen Szenenliste eine filterbare Übersicht bauen. Entscheidend ist die Datei, die du öffnen und kontrollieren kannst.'),
 ('prompt','Erstelle eine lokale HTML-Datei für einen fiktiven Angebotsrechner. Pro Stück 0,20 Euro netto; ab 500 Stück 10 Prozent Rabatt auf die gesamte Nettosumme. Gib Menge, Rabatt und Nettosumme getrennt aus. Nur ganze Mengen ab 1 sind zulässig. Keine externen Dienste oder Bibliotheken. Prüfe 499, 500, 0 und eine leere Eingabe. Erkläre mir Ergebnis und verbleibende Grenzen.'),
 ('note','Eine Aussage „geprüft“ braucht einen Beleg: Welche Eingaben wurden verwendet? Welches Ergebnis kam tatsächlich heraus? Falls der Agent den Code hier nicht ausführen kann, muss er das sagen und dir manuelle Prüfschritte geben.'),
 ('check','499 Stück = 99,80 Euro; 500 Stück = 90,00 Euro netto. 0 und leer dürfen kein gültiges Angebot erzeugen. Dies sind Übungsregeln, keine echten Druckpreise.')])

page('claudecode','Claude Code: im Projekt zusammenarbeiten','Anthropic · mehr als ein Chat über Programmierung',[
 ('p','Claude Code kann Projektdateien lesen, bearbeiten und Befehle ausführen. Es gibt unter anderem Terminal-, IDE-, Desktop- und Web-Oberflächen. Die Desktop-Anwendung ist für macOS und Windows dokumentiert; Details und Erweiterungen unterscheiden sich je Sitzung. [A1, A2]'),
 ('h','Unser Einstiegsvorschlag'),
 ('p','Carmen öffnet einen eigenen Übungsordner am Mac und lässt zunächst erklären, welche Dateien darin liegen. Erst danach folgt eine kleine Änderung. Tabea kann eine Szenenliste überarbeiten; Ingo den Rechner aus der vorherigen Mission kontrollieren lassen.'),
 ('prompt','Arbeite nur im neuen Übungsordner. Wenn noch keine Datei vorhanden ist, erstelle eine einfache HTML-Seite mit drei fiktiven Workshop-Terminen. Erkläre mir die Bestandteile ohne Fachwissen. Ändere anschließend die Karten so, dass sie auf kleinen Bildschirmen untereinander stehen. Zeige die Änderungen und nenne drei konkrete Prüfungen. Veröffentliche nichts.'),
 ('h','Projekt-Regeln sind ein Arbeitsgedächtnis auf Papier'),
 ('p','Ein eigener Zettel kann festhalten: kurze Sätze, keine externen Schriftarten, große Schaltflächen, nur fiktive Angaben. Solche Regeln helfen bei wiederholter Arbeit. Sie ersetzen weder Datenrechte noch die Kontrolle einer Änderung. Claude Codes Projektkontext ist nicht dasselbe wie die Memory-Funktion im normalen Chat.'),
 ('check','Kannst du die bearbeitete Datei benennen? Ist die mobile Ansicht sichtbar besser? Hat der Agent einen echten Test beschrieben oder lediglich einen Test vorgeschlagen?')])

page('kosten','Was kostet der erste Versuch?','Herstellerangaben vom 19.10.2026 · USD, keine Euro-Umrechnung',[
 ('table',(['Werkzeug','Orientierung für Einzelpersonen','Darauf achten'],[
 ['Antigravity','Individual: 0 USD/Monat. Höhere Limits über Google AI Pro/Ultra.','Pro-/Ultra-Preis im regionalen Angebot prüfen; Quoten und Credits beachten. [G3]'],
 ['Codex','Plus: 20 USD/Monat. Pro ab 100 USD/Monat; weitere Stufen.','Free/Go bieten begrenzten Zugang laut Rollout. Zusatzcredits und API-Abrechnung unterscheiden. [O2]'],
 ['Claude Code','In Claude Pro enthalten: 20 USD/Monat; alternativ 200 USD jährlich im Voraus.','Free enthält laut Preisliste kein Claude Code. Max und Team bieten andere Kontingente. [A3]'] ])),
 ('p','Preise sind eine Momentaufnahme der angezeigten USD-Listenangaben. Region, Steuer und Abrechnungsweg können den Endpreis verändern. Vor einem Kauf den tatsächlichen Checkout und die Nutzungsgrenzen lesen. Ein Monatsabo bedeutet keine unbegrenzten Aufgaben.'),
 ('h','Drei getrennte Geldtöpfe'),
 ('p','1. Das Abo der Arbeitsumgebung. 2. Gegebenenfalls API-Nutzung oder zusätzliche Credits. 3. Der angebundene Dienst, etwa Canva, Figma oder HeyGen. Ein Plugin kann kostenlos installierbar sein und trotzdem kostenpflichtige Leistungen auslösen.'),
 ('note','Für den Unterricht reicht zunächst eine Chat-Variante mit fiktiven Angaben. Kein Abo nur für diese Übungen abschließen. Wer einen vorhandenen freigegebenen Zugang hat, nutzt ihn für einen begrenzten Versuch.'),
 ('check','Du hast ein KI-Abo. Sind damit automatisch Video-Credits eines anderen Herstellers bezahlt? Nein: der angeschlossene Dienst hat eigene Bedingungen.')])

page('ablauf','Die 5-Schritte-Werkstatt','Ein guter Auftrag ist ein kleiner, prüfbarer Auftrag',[
 ('h','1 · Ziel und Grenzen'),('p','Beschreibe ein sichtbares Ergebnis: eine lokale Datei, drei Karten, ein Rechenweg. Nenne Zielgruppe, Beispieldaten und das, was der Button tatsächlich tun soll.'),
 ('h','2 · In einfachen Worten planen'),('p','Lass dir erklären, welche Dateien entstehen, welche Verbindung gebraucht würde und welche Angaben fehlen. Frage nach, bis du den Ablauf selbst erzählen kannst.'),
 ('h','3 · Einen kleinen Stand bauen'),('p','Ein Rechenweg oder eine Seite genügt. Ein begrenzter Übungsordner macht Änderungen überschaubar. Eine Kopie des letzten funktionierenden Stands erleichtert den nächsten Versuch.'),
 ('h','4 · Selber prüfen'),('p','Teste einen normalen Fall, eine Grenze und einen Fehlerfall. Vergleiche mit dem eigenen Rechenweg oder den Ausgangsdaten. Prüfe Texte, mobile Darstellung und Tastaturbedienung.'),
 ('h','5 · Ergebnis und nächsten Schritt festhalten'),('p','Notiere: Was ist wirklich fertig? Was wurde nur simuliert? Welche offene Frage bleibt? Erst eine bewusste nächste Entscheidung macht aus einer lokalen Demo eine veröffentlichte Anwendung oder einen echten Versand.'),
 ('note','Beispiel: „Erstelle einen Entwurf für eine Nachfassmail“ ist kein Auftrag, die Mail zu versenden. Ein Satz im Prompt begrenzt die Aufgabe; technische Rechte und vorhandene Werkzeuge begrenzen zusätzlich, was tatsächlich möglich ist.'),
 ('check','Erkläre den Ablauf einem Kollegen in 30 Sekunden, ohne die Wörter Agent, API oder Framework zu verwenden.')])

page('labor','Das faire Vergleichslabor','Gleicher Auftrag · gleiche Regeln · erst dann urteilen',[
 ('p','Wir haben hier keinen eigenen Produktvergleich gemessen. Mit diesem Versuch könnt ihr selbst eine begründete Einschätzung für euren Alltag gewinnen. Eine einzelne Runde bleibt eine kleine Stichprobe.'),
 ('prompt','Erstelle eine lokale, eigenständige HTML-Demo für den fiktiven Workshop „Papier trifft Pixel“. Drei Angebotskarten: Druck-Check 30 Minuten, Website-Check 45 Minuten, Video-Check 60 Minuten. Ein Filter zeigt nur Angebote bis 45 Minuten. Ein leeres Ergebnis wird verständlich erklärt. Keine externen Dienste, kein Versand, keine Registrierung. Zeige die Datei, erkläre die Bedienung und prüfe Startansicht, Filter und Tastatur.'),
 ('table',(['Kriterium','Deine Beobachtung je Werkzeug'],[
 ['Auftrag erfüllt?','Alle drei Karten; Filter nimmt nur 30 und 45 Minuten mit.'],
 ['Ergebnis prüfbar?','Datei, Startschritte und tatsächlich ausgeführte Checks benannt.'],
 ['Verständlich?','Kann ich den Ablauf ohne Hilfe erklären?'],
 ['Grenzen ehrlich?','Keine echte Buchung, keine erfundenen Testergebnisse.'],
 ['Aufwand passend?','Eigene Minuten, Korrekturen und sichtbaren Verbrauch notieren.'] ])),
 ('check','Gib pro Kriterium 0 = fehlt, 1 = teilweise, 2 = erfüllt. Diese Skala ist eine Unterrichtshilfe, kein wissenschaftlicher Benchmark. Produkt, Modell, Oberfläche, Datum und Hilfestellungen dazuschreiben. Bei einem Pflichtfehler zuerst verbessern, statt nur Punkte zu addieren.')])

page('ingo1','Ingo · Die Rabatt-Rakete','Mission 1 · etwa 10 Minuten · Druck und Vertrieb',[
 ('p','Ein Kunde fragt nach 499, 500 und 1.000 Flyern. Du brauchst eine Antwort, deren Rechnung jeder nachvollziehen kann. Die Preise sind reine Übungswerte.'),
 ('prompt','Du bist mein verständlicher Rechenpartner. Fiktiver Stückpreis: 0,20 Euro netto. Ab 500 Stück gibt es 10 Prozent Rabatt auf die ganze Nettosumme. Erkläre die Regel an 499, 500 und 1.000 Stück. Zeige eine Tabelle mit Menge, Summe vor Rabatt, Rabatt und Endsumme. Erfinde keine Steuer, Versand- oder Produktionskosten. Stelle mir anschließend eine Fangfrage; verrate die Lösung erst nach meiner Antwort.'),
 ('h','Wenn du einen Coding-Agent nutzt'),
 ('p','Lass anschließend dieselbe Regel als lokale HTML-Datei bauen. Nutze Antigravity, Codex oder Claude Code nach den Einstiegshinweisen. Erst wenn die Rechnung stimmt, darf die Gestaltung bunter werden. Ein freundlicher Fehlertext bei 0 oder leer gehört dazu.'),
 ('check','Sollwerte netto: 499 → 99,80 Euro; 500 → 90,00 Euro; 1.000 → 180,00 Euro. Die größere Menge kann an der Rabattgrenze günstiger sein. Der Rechner muss genau die vereinbarte Regel darstellen.'),
 ('h','Bonus: Du bist der Fehlerdetektiv'),
 ('p','Bitte die KI um ein absichtlich falsches Rechenbeispiel und suche den Fehler. Kennzeichne den falschen Entwurf deutlich. Erkläre anschließend einem Kunden den richtigen Rechenweg in zwei Sätzen.'),
 ('note','Für eine echte Druckfreigabe fehlen hier unter anderem konkrete Preislisten, Papier, Format, Druckverfahren und vereinbarte Zusatzkosten. Eine Browser-Demo bestätigt weder Druckqualität noch Produktionsfähigkeit.')])

page('ingo2','Ingo · Wer bekommt als Nächstes Aufmerksamkeit?','Mission 2 · etwa 8 Minuten · CRM ohne Kundendaten',[
 ('prompt','Nutze nur diese fiktive Liste: Mondfalter – Angebot seit 8 Tagen offen, Rückruf gewünscht; Papierpilot – Angebot seit 2 Tagen offen, kein Rückruf vereinbart; Farbfuchs – bereits abgesagt. Sortiere sinnvolle nächste Schritte, begründe sie mit der Liste und schreibe für Mondfalter einen freundlichen Mailentwurf mit höchstens 60 Wörtern. Erfinde keine Zusage und versende nichts. Frage mich danach, welcher Eintrag auf keinen Fall wie eine offene Chance behandelt werden sollte.'),
 ('h','Mögliche Auflösung'),
 ('p','Mondfalter zuerst prüfen, weil ein Rückruf gewünscht ist. Für Papierpilot einen passenden späteren Schritt planen; kein vereinbarter Rückruf wurde genannt. Farbfuchs ist abgesagt. Es gibt hier keinen Anlass, daraus eine Verkaufszusage zu machen.'),
 ('h','Mit HubSpot MCP wird daraus ein angebundener Versuch'),
 ('p','Der offizielle Remote-Server kann CRM-Objekte und Aktivitäten zugänglich machen; die tatsächlich verfügbaren Aktionen hängen von Zugang und Rechten ab. Er ist vom HubSpot Developer MCP zum Bauen von Erweiterungen zu unterscheiden. [P1]'),
 ('p','Für einen ersten Versuch legt die Kursleitung ausschließlich fiktive Testeinträge in einem freigegebenen Bereich an. Der Auftrag bleibt: drei benannte Einträge lesen, Empfehlung und Entwurf ausgeben. Keine Änderungen und kein Versand. Ohne eingerichteten Zugang bleibt die Liste aus dem Prompt die Quelle.'),
 ('check','Steht bei jedem Vorschlag, welcher Listeneintrag ihn begründet? Hat die KI Entwurf und Versand unterschieden? Kannst du eine Behauptung markieren, die in den Daten gar nicht vorkommt?'),
 ('note','Spannender Anschluss: Mit Canva ein Angebotsmotiv erstellen. Ein gut aussehendes Motiv ersetzt keine Druckdatenprüfung. Siehe Erweiterungskoffer auf den Seiten 17–20.')])

page('carmen1','Carmen · Die Website mit dem Schummel-Button','Mission 1 · etwa 10 Minuten · Team und Website',[
 ('prompt','Erstelle einen verständlichen Entwurf für eine kleine fiktive Teamfrühstück-Seite. Termin: 23.10.2026 um 9 Uhr im Raum Sonnenhof. Drei Karten: Kaffee, Obst, Brötchen. Ein Button heißt „Interesse merken“. Er soll nur einen Hinweis auf dieser Seite zeigen: „Demo: Dein Interesse wurde nicht übermittelt.“ Keine Namen erfassen, kein Formular senden. Gib mir zuerst Aufbau und Texte und anschließend einen einfachen manuellen Prüfplan.'),
 ('h','Am Mac mit Agent-Zugang'),
 ('p','Lass die Seite in einem neuen lokalen Übungsordner als HTML umsetzen. Frage nach dem genauen Startweg für deine gewählte Oberfläche. Auf dem Mac ist die Desktop-Oberfläche von Claude Code dokumentiert; Codex und Antigravity bieten ebenfalls Arbeitsoberflächen. Die Installation ersetzt keine technische Einweisung. [A2, O1, G1]'),
 ('h','Finde den Schummel-Button'),
 ('p','Ein Button mit „Du bist angemeldet!“ wäre falsch: Es gibt hier weder Speicherung noch Übermittlung. Korrigiere den Text. Prüfe dann, ob der Hinweis nach einem Tastaturklick genauso erscheint wie nach einem Mausklick.'),
 ('check','Alle drei Karten sichtbar? Termin stimmt? Keine übermittelte Anmeldung behauptet? Bei 390 Pixel Breite keine abgeschnittenen Inhalte? Kannst du mit Tab zum Button und mit Enter auslösen?'),
 ('note','Chat-Variante: Text und Prüfplan reichen. Wenn der Chat keine Datei ausführen kann, behauptet ihr keine getestete Website. Die praktische Browserprüfung wird dann gemeinsam durchgeführt.')])

page('carmen2','Carmen · Teamchaos wird ein Plan','Mission 2 · etwa 8 Minuten · Verantwortung sichtbar machen',[
 ('prompt','Sortiere diese erfundenen Besprechungsnotizen: Lea prüft bis Mittwoch die Startseite. Ben wartet auf das Logo von Mia. Für den Datenschutzhinweis fehlt noch eine zuständige Person. Erstelle eine Tabelle: Aufgabe, verantwortlich, Termin, offene Frage. Ergänze nichts als angebliche Tatsache. Formuliere danach eine Rückfrage an das Team in höchstens drei Sätzen. Gib nur einen Entwurf aus.'),
 ('h','Dein Selbstcheck'),
 ('p','Lea und Mittwoch dürfen eingetragen werden. Für Bens Fertigstellung fehlt ein Termin. Mia liefert das Logo, aber eine Frist steht nicht im Text. Beim Datenschutzhinweis bleibt die Zuständigkeit offen. „Unbekannt“ ist genauer als eine erfundene Person.'),
 ('h','Plugin-Idee: Website sehen und wirklich prüfen'),
 ('p','Mit Figma MCP kann ein Agent auf berechtigte Designinhalte zugreifen. Der Figma-Katalog unterscheidet aktuell: Codex und Claude Code lesen/schreiben lokal und remote; Antigravity ist dort nur lokal mit Lesezugriff aufgeführt. [P4]'),
 ('p','Mit Playwright MCP lassen sich Browserabläufe wie die Bedienung einer Testseite durchführen. Microsoft bietet daneben einen CLI-/Skills-Weg an. Für manche Coding-Aufgaben ist dieser eine Alternative zur MCP-Verbindung. [P6]'),
 ('check','Lass auf einer lokalen Testseite exakt drei Dinge prüfen: Button erreichbar, Bestätigung korrekt, keine horizontale Verschiebung auf schmaler Ansicht. Ein Screenshot allein prüft die Bedienung nicht.'),
 ('note','Bonus: Bitte um zwei Varianten der Team-Rückfrage, einmal freundlich-kurz und einmal locker. Entscheide selbst, welche zu eurem Team passt. Kein automatischer Versand.')])

page('tabea1','Tabea · Das Storyboard-Mischpult','Mission 1 · etwa 10 Minuten · Video und kreative Arbeit',[
 ('prompt','Wir planen einen fiktiven 15-Sekunden-Clip für das Papierfestival „Pixel & Papier“. Zielgruppe: Menschen ohne Designwissen. Drei Szenen mit je 5 Sekunden. Erstelle eine Tabelle: Zeitraum, Bildidee, gesprochener Satz, Texteinblendung. Höchstens 30 gesprochene Wörter insgesamt und höchstens 6 Wörter pro Einblendung. Keine echten Marken, Personen oder Musikvorgaben. Stelle mir danach zwei spielerische Stilvarianten zur Wahl.'),
 ('h','Jetzt wirst du zur Regie'),
 ('p','Wähle etwa „gemütliche Papierwelt“ oder „rasantes Farbchaos“. Lass die KI die gleiche Botschaft im neuen Stil umschreiben. Zähle Wörter nach und lies den Text laut mit Stoppuhr. Ein passender Wortumfang garantiert noch keinen passenden Sprechrhythmus.'),
 ('h','Mit einem Coding-Agent'),
 ('p','Lass aus dem Storyboard eine lokale HTML-Szenenübersicht erstellen: drei Karten und einen Filter für „Nahaufnahme“ oder „Übersicht“. Das ist ein Planungswerkzeug. Ein Storyboard ist noch kein gerendertes Video, und ein Code-Agent ist nicht automatisch mit deinem Schnittprogramm verbunden.'),
 ('check','Zeitbereiche 0–5, 5–10, 10–15 Sekunden? Jede Szene verständlich? Gesamttext höchstens 30 Wörter? Einblendungen lesbar? Keine ungeprüften Behauptungen über ein echtes Produkt?'),
 ('note','Ohne Agent-Zugang: normaler Langdock-Chat genügt für das Storyboard. Füge die drei Szenen von Hand in dein vorhandenes Kreativwerkzeug ein. So bleibt die Aufgabe vollständig nutzbar.')])

page('tabea2','Tabea · Eine Idee, drei sichtbare Wege','Mission 2 · etwa 8 Minuten plus optionaler Render-Versuch',[
 ('table',(['Weg','Damit experimentierst du','Dein Ergebnis'],[
 ['Canva MCP','Ein bearbeitbares Motiv oder eine Präsentation','Entwurf mit anschließendem Blick in Canva. [P2]'],
 ['HeyGen Remote MCP','Ein kurzer Avatar-Erklärclip','Ein tatsächlicher Render nutzt vorhandene Plan-Credits. [P7]'],
 ['Remotion Plugin / Skills','Ein Video aus beschreibbarem Code','Lokales Projekt, Vorschau und späterer Export. [P8, P9]'] ])),
 ('prompt','Entwirf für das fiktive Papierfestival drei Titelkarten. Format 1080 × 1920 Pixel. Pro Karte höchstens sechs Wörter, kontrastreiche Farben und große Schrift. Beschreibe für jede Karte Aufbau, Text und eine einfache Bewegung. Gib erst einen Plan aus. Behaupte ohne angebundenes Werkzeug nicht, dass eine Canva-Datei oder ein Video erstellt wurde.'),
 ('h','Wähle einen optionalen Anschluss'),
 ('p','Canva: eine Kopie eines eigenen Testdesigns bearbeiten und den Link öffnen. HeyGen: erst Skript und vorgesehene Credit-Nutzung prüfen; dann mit erlaubtem Standardavatar einen kurzen Versuch starten. Remotion: eine Titelkarte animieren, Vorschau ansehen und Schriftgröße korrigieren.'),
 ('check','Plan, bearbeitbare Datei, Vorschau und fertiger Export sind vier verschiedene Zustände. Benenne deinen tatsächlichen Stand. Bei einem Video zusätzlich Sprache, Aussprache, Bildrechte und Musikrechte selbst prüfen.'),
 ('note','Ein eigener digitaler Zwilling braucht bei HeyGen dokumentierte Zustimmung. Für diese Aufgabe reicht ein freigegebener Standardavatar. Remotion hat eigene Lizenzbedingungen; vor beruflichem Einsatz die aktuelle Lizenz und mögliche Kosten prüfen. Die Plugin-Installation ist keine pauschale Nutzungslizenz.')])

page('koffer','Der Erweiterungskoffer','Sechs ausgewählte Helfer statt einer endlosen Plugin-Liste',[
 ('table',(['Erweiterung / Typ','Ingos Start','Carmens Start','Tabeas Start'],[
 ['HubSpot / Remote MCP','Test-Angebote sortieren','Übergaben im CRM lesen','Kampagnenbriefing lesen'],
 ['Canva / Remote MCP','Angebotsmotiv entwerfen','Workshop-Präsentation','Storyboard und Social-Motiv'],
 ['Figma / MCP','Rechner-Layout verstehen','Design zur Website prüfen','Designvorlage bearbeiten'],
 ['Playwright / lokales MCP','Rechner im Browser testen','Demo-Website bedienen','Portfolio-Filter prüfen'],
 ['HeyGen / Remote MCP','30-Sekunden-Erklärung planen','Onboarding-Clip planen','Avatar-Erklärclip'],
 ['Remotion / Plugin + Skills','Animierte Angebotskarte','Kurzer Infoclip','Motion-Design-Titelkarte'] ])),
 ('p','Die Fälle sind unsere Unterrichtsideen. Die dokumentierten Fähigkeiten und Zugangshürden stehen auf den folgenden Seiten. Es wurde nichts installiert oder mit euren Konten verbunden.'),
 ('h','So liest du die Verbindungshinweise'),
 ('p','„Offiziell genannt“ bedeutet: Der Anbieter benennt den Client oder liefert dafür einen Weg. „Manuell zu prüfen“ bedeutet: MCP-Grundunterstützung reicht allein nicht als Beweis für Anmeldung und alle Werkzeuge. Kein Häkchen in diesem Heft bedeutet einen durch uns getesteten Betrieb.'),
 ('note','Mit einem Helfer anfangen. Erst wenn eine echte Wiederholung Arbeit kostet, lohnt sich der nächste Anschluss. Ein Skill gibt eine Arbeitsweise vor; ein MCP-Server stellt Werkzeuge bereit. Manche Plugins bündeln beides. [O3, O4, G5, A5]')])

page('koffer1','Angebote und Motive','HubSpot + Canva · besonders für Druck, Vertrieb und Business',[
 ('h','HubSpot · vom CRM zur nächsten sinnvollen Frage'),
 ('p','Offizieller Remote-MCP-Server: CRM-Daten und Aktivitäten lesen und je verfügbaren Rechten auch bearbeiten. Geeignet für Ingos Nachfassliste. Verwechsel ihn nicht mit dem Developer MCP für die Entwicklung von HubSpot-Erweiterungen. [P1]'),
 ('p','Zugang: HubSpot-Konto, passende OAuth-Anmeldung und freigegebene Datenrechte; bei eigener Integration zusätzlicher Einrichtungsaufwand. Die Dokumentation nennt kompatible MCP-Clients, aber keinen hier vollständig getesteten Weg für alle drei Werkzeuge. Daher Anmeldung und Tool-Liste je Oberfläche zuerst prüfen. Kosten: HubSpot-Tarif, Limits und mögliche Integrationskosten separat klären. Kein pauschales „kostenlos“.'),
 ('prompt','Lies nur die drei ausdrücklich benannten Test-Angebote. Nenne Status und nächste Rückfrage mit Quellenbezug. Verändere nichts und schreibe nur einen Mailentwurf. Falls dir ein Tool oder Recht fehlt, erkläre die Lücke.'),
 ('h','Canva · der kreative Anschluss, nicht der Dev-MCP'),
 ('p','Der offizielle Design-MCP unterstützt Entwürfe, Bearbeitung, Suche und Exporte. Der separate Canva Dev MCP hilft beim Entwickeln von Canva-Apps und hat einen anderen Zweck. [P2]'),
 ('p','Zugang: eigenes Canva-Konto, individuelle OAuth-Anmeldung und Bearbeitungsrechte. Kernfunktionen gibt es laut Dokumentation in allen Plänen; etwa Größenanpassung und Brand Kits brauchen Pro oder höher. Credits und Limits bleiben relevant. Vorhandenen Connector bevorzugen; bei eigener Client-Integration gelten Zulassungsanforderungen. Nicht jeder Client ist automatisch freigeschaltet. [P3]'),
 ('prompt','Erstelle nach meiner Auswahl einen Entwurf für das fiktive Papierfestival. Nutze nur meine freigegebene Testvorlage. Gib den Bearbeitungslink zurück. Ein Export ist erst fertig, wenn der Dienst ihn bestätigt hat.')])

page('koffer2','Design sehen. Bedienung prüfen.','Figma + Playwright · besonders für Website und kreative Arbeit',[
 ('h','Figma · diese Kompatibilität macht einen Unterschied'),
 ('p','Der offizielle Katalog nennt Codex und Claude Code mit lokalem und entferntem Server sowie Lese- und Schreibzugriff. Antigravity ist mit lokalem Server und reinem Lesezugriff gelistet. Das ist kein gleichwertiger Bearbeitungsweg. [P4]'),
 ('p','Figma dokumentiert Werkzeuge zum Lesen von Designkontext sowie zum Bearbeiten unterstützter Inhalte. Was du nutzen kannst, hängt von Client, Server, Datei und Rechten ab. [P5] Zugang: Figma-Konto, Anmeldung bei Remote-Zugang bzw. passende Desktop-Einrichtung lokal; Dateirechte und aktuelle Sitz-/Tarifkontingente prüfen. Kosten: Figma-Tarif und Limits zusätzlich zum KI-Zugang.'),
 ('prompt','Lies meinen benannten Testframe. Erkläre Abstände, Schriftgrößen und Buttonzustände verständlich. Schlage eine mobile Umsetzung vor. Bearbeite nur dann eine Designkopie, wenn der verwendete Client tatsächlich Schreibwerkzeuge anbietet und der Auftrag sie umfasst.'),
 ('h','Playwright · ein Browser, der Handgriffe ausführen kann'),
 ('p','Microsofts MCP-Server stellt Browsersteuerung bereit. Der Projektleitfaden nennt unter anderem Claude Code und Codex; andere Clients brauchen passende MCP-Konfiguration. Für Antigravity die lokale Verbindung gesondert prüfen. Node-Laufzeit und Browserumgebung sind einzurichten. Das Paket ist quelloffen; Agent-/Infrastrukturkosten sind davon getrennt. [P6]'),
 ('prompt','Öffne ausschließlich meine lokale Testseite. Prüfe Mengen 499, 500 und 0 sowie den Fehlertext bei leerer Eingabe. Berichte beobachtete Ergebnisse getrennt von vermuteten Ursachen. Keine echten Formulare senden.'),
 ('check','Ein isoliertes Übungsprofil verhindert Verwechslungen mit deinem Arbeitsbrowser. Browsersteuerung ist ein handlungsfähiges Werkzeug, keine bloße Textanalyse.')])

page('koffer3','Vom Skript zum bewegten Bild','HeyGen + Remotion · besonders für Video, Design und Erklärungen',[
 ('h','HeyGen · Video über Remote MCP'),
 ('p','Der offizielle Dienst verbindet sich per OAuth mit dem HeyGen-Webkonto. Für Remote MCP wird kein API-Schlüssel benötigt. Laut Anbieter gibt es keinen separaten MCP-Aufpreis; Render nutzen die Premium-Credits des vorhandenen Plans. Die eigene REST-API hat einen anderen Abrechnungsweg. Claude Code und weitere Clients haben Anbieter-Anleitungen; für Codex oder Antigravity den konkreten Anschlussweg in der gewählten Oberfläche prüfen. [P7]'),
 ('prompt','Bereite einen 15-Sekunden-Erklärclip zum fiktiven Papierfestival vor: erlaubter Standardavatar, deutsche Sprache, drei kurze Sätze. Zeige Skript und benötigte Einstellungen. Starte einen kostenpflichtigen Render erst nach meiner ausdrücklichen Auswahl dieses Entwurfs.'),
 ('h','Remotion · Videos als bearbeitbares Projekt'),
 ('p','Remotion bietet offizielle Plugins für Codex und Claude Code. Das Paket enthält Agent Skills für Remotion-Projekte. Ein Remotion-Plugin für Antigravity ist auf dieser Liste nicht genannt. Dort sind die offiziellen Skills höchstens ein manuell zu prüfender Weg, keine bestätigte Plugin-Kompatibilität. [P8, P9]'),
 ('p','Voraussetzungen: lokale Entwicklungsumgebung, Node und Projekt-Abhängigkeiten; optional eigene Medien. Kosten: KI-Nutzung, ggf. Render-Infrastruktur und passende Remotion-Lizenz. Eine ansehnliche Vorschau sagt noch nichts über eine gewerbliche Lizenz aus.'),
 ('prompt','Erstelle in einem neuen Remotion-Übungsprojekt eine 5-Sekunden-Titelkarte: „Papier trifft Pixel“, Hochformat 1080 × 1920, klarer Kontrast, ruhiges Einblenden. Verwende keine fremden Medien. Zeige zuerst die Vorschau. Erkläre den Unterschied zwischen Projekt, Vorschau und MP4.'),
 ('check','Prüfe den Clip laut und ohne Ton. Ist die Botschaft in beiden Situationen verständlich? Lass dich von einer Animation nicht vom Inhalt ablenken.')])

page('anschluss','Eine Verbindung ist erst der Anfang','Einrichtungsweg und Fehlerhilfe ohne Terminal-Voraussetzung',[
 ('table',(['Werkzeug','Wo du beginnst','Dann prüfen'],[
 ['Antigravity','MCP in Customizations/Settings oder MCP Store; CLI mit /mcp.','Die Anleitungen unterscheiden App, CLI und IDE. [G4]'],
 ['Codex','Plugins bzw. dokumentierte MCP-Einrichtung der eigenen Oberfläche.','Web, Desktop, CLI und IDE haben unterschiedliche Einrichtungswege. [O3]'],
 ['Claude Code','Desktop-Verbindungen oder MCP-Verwaltung der CLI.','Remote-Dienst bzw. lokalen Server passend einrichten. [A2, A4]'] ])),
 ('h','Vier Dinge wirklich kontrollieren'),
 ('p','1. Anbieter: Stammt der Anschluss vom Hersteller oder ist er ein Community-Projekt? 2. Konto: Welches Testkonto ist angemeldet? 3. Werkzeuge: Sind Lesen, Ändern oder Export tatsächlich verfügbar? 4. Grenzen: Welche Daten, Kosten und Aktionen sind erlaubt? Ein Prompt allein ändert die technischen Rechte nicht.'),
 ('h','Wenn etwas nicht klappt'),
 ('p','Kein Tool sichtbar: Verbindung, Oberfläche und Administratorfreigabe prüfen. Lesen klappt, Schreiben nicht: Rechte, Client-Unterstützung und Dateizugriff prüfen. Anmeldung scheitert: unterstützten OAuth-Weg verwenden. Kontingent erschöpft: Verbrauch im Dienst prüfen. Nicht aus einem Fehlversuch auf eine generelle Produktgrenze schließen.'),
 ('note','Erste echte Probe: genau ein benanntes Testobjekt lesen. Danach eine Kopie ändern und selbst öffnen. Vorher-/Nachher-Stand sichern. Keine Schlüssel in den Chat schreiben und keine Anweisung aus fremden Dokumenten als Freigabe für Aktionen behandeln.'),
 ('check','Ohne Zugang? Nutze einen erfundenen Text oder eine kleine Tabelle aus dem Heft. Sage ausdrücklich „Vorbereitung ohne Verbindung“. So bleibt der Lerneffekt erhalten.')])

QUIZ=[
 ('Du bezahlst Claude Pro. Ist damit jede API-Nutzung bezahlt?',['Ja, jede Nutzung','Nein, Zugangs- und Abrechnungsweg prüfen','Nur am Mac'],1,'Abo und API sind verschiedene Zugänge. Zusätzliche Nutzung kann separat abgerechnet werden.'),
 ('Ein Skill beschreibt den Angebotsablauf. Was fehlt für echte HubSpot-Daten?',['Ein lustigerer Name','Eine eingerichtete Verbindung mit passenden Rechten','Eine längere Antwort'],1,'Arbeitsanweisungen stellen allein keine CRM-Verbindung her.'),
 ('Welcher Figma-Unterschied ist dokumentiert?',['Alle drei schreiben immer','Antigravity ist im Katalog nur lokal und lesend aufgeführt','Codex kann Figma nie lesen'],1,'Der geprüfte Katalog nennt für Codex und Claude Code zusätzlich Schreibzugriff und Remote-Server.'),
 ('Die Demo zeigt „Du bist angemeldet“, speichert aber nichts. Was ist zu ändern?',['Die Behauptung berichtigen','Nur die Farbe','Nichts'],0,'Der Text muss die tatsächliche Wirkung beschreiben. Eine lokale Anzeige ist keine Anmeldung.'),
 ('500 Flyer à 0,20 Euro, 10 Prozent Rabatt auf alles: Summe netto?',['100 Euro','99 Euro','90 Euro'],2,'100 Euro vor Rabatt minus 10 Euro Rabatt ergibt 90 Euro.'),
 ('Was macht einen fairen Werkzeugvergleich aus?',['Jedes bekommt eine andere Aufgabe','Gleicher Auftrag und vorher festgelegte Prüfkriterien','Nur die schönste Startansicht'],1,'Zusätzlich Modell, Oberfläche, Datum und Hilfestellungen festhalten.'),
 ('Die Folie nennt „bis zu 50 Prozent weniger Halluzinationen“. Reicht das?',['Ja, garantiert wahr','Nein, Vergleichsmodell und Messmethode fehlen','Ja, sobald eine Grafik daneben steht'],1,'Ohne Modell, Datum, Aufgaben und Methode lässt sich daraus kein belastbarer Vergleich ableiten.'),
 ('Was ist ein gerendertes Video?',['Eine Bildidee in einem Chat','Der Text einer Remotion-Datei','Ein tatsächlich erzeugter Videoexport'],2,'Plan, Quellprojekt, Vorschau und Export sind verschiedene Zustände.')]
page('quiz','Acht kleine Wissensduelle','Erst entscheiden. Dann auf Seite 23 vergleichen.',[
 ('p','Notiere pro Frage A, B oder C. Erkläre zusätzlich bei zwei Fragen deine Begründung. Die Web-Version zeigt Feedback; hier steht die Auflösung auf der nächsten Seite.')]+[
 ('p',f'{i}. {q}\nA: {o[0]}\nB: {o[1]}\nC: {o[2]}') for i,(q,o,r,w) in enumerate(QUIZ,1)])
page('antworten','Die Auflösungen – mit Denkweg','Selbst prüfen statt nur Punkte sammeln',[
 ('p',f'{i} · {"ABC"[r]} — {w}') for i,(q,o,r,w) in enumerate(QUIZ,1)]+[
 ('h','Deine 60-Sekunden-Erklärung'),('prompt','Ich erkläre dir jetzt den Unterschied zwischen Modell, Arbeitsumgebung, Skill und MCP in meinen Worten. Höre erst zu. Stelle mir danach genau eine Rückfrage zu einer unklaren Stelle. Nutze ein Beispiel aus meinem Beruf und erfinde keine Verbindung zu meinen Konten.'),
 ('check','Eine gute eigene Erklärung nennt: den Motor, die Werkstatt, den Arbeitszettel und die Werkzeug-Verbindung. Danach kann eine andere Person sagen, was schon geht und was noch eingerichtet werden muss.')])

# Vollständiger Folienabgleich: Quelle Einfuhrung-Claude.pdf, 28 Seiten.
# Jede Folie hat Erklärung, Details, Beispiel, Frage, Antwort und ggf. Präzisierung.
SLIDES=[
 (1,'Worum diese Lektion geht','Die Vorlage heißt „Einführung Claude“, Modul 1, Lektion 14, Ausgabe Juli 2026. Dieses Heft ergänzt den Blick auf zwei weitere Arbeitsumgebungen.','Die Kursfolge nennt dieses Material Tag 15. Lektion und Kurstag sind unterschiedliche Zählungen. Die Ausgangsfolien bleiben erhalten.','Du lernst heute nicht nur einen Produktnamen, sondern wählst einen Helfer für eine konkrete kleine Arbeit.','Ist Lektion 14 automatisch Kurstag 14?','Nein. Die Foliennummer der Lektion und die Reihenfolge unseres Kurses sind getrennt.',''),
 (2,'Claude: Modell, Plattform und Werkzeuge','Claude bezeichnet ein Angebot rund um Sprachmodelle. Ein Modell erzeugt Antworten; eine Anwendung macht es für Menschen bedienbar.','Zur Plattform gehört der technische API-Zugang. Anwendungen und Werkzeuge ermöglichen unter anderem Schreiben, Analyse, Code und Arbeit mit Bildern.','Ein Chat erklärt Ingos Rechnung. Claude Code kann mit passenden Werkzeugen eine Rechner-Datei erstellen.','Warum ist „Claude kann das“ oft zu ungenau?','Weil Modell, Anwendung, Werkzeuge, Tarif und Rechte entscheiden, was im konkreten Fall möglich ist.','Eine Fähigkeit des Modells ist nicht automatisch eine Funktion jeder Oberfläche. [A1]'),
 (3,'Sicherheit ist ein Entwicklungsziel','Anthropic betont Sicherheit und beschreibt Constitutional AI: Grundsätze sollen das Verhalten beim Training und Bewerten lenken.','Die Folie nennt außerdem Text, Code, Bild, Recherche und Automatisierung sowie fortlaufende Updates. Bedienbarkeit und Sicherheit sind Ziele, keine Beweise für jeden Einzelfall.','Eine höfliche KI kann trotzdem eine falsche Lieferfrist behaupten. Ingo gleicht sie mit der Quelle ab.','Beweist ein Sicherheitsversprechen, dass jede Antwort stimmt?','Nein. Inhalte und tatsächliche Aktionen müssen weiterhin geprüft werden.','„Safety first“ ist eine Selbstdarstellung und kein allgemeines Qualitätsranking gegenüber anderen Produkten.'),
 (4,'Anthropic als Unternehmen','Anthropic ist der Anbieter hinter Claude. Die Vorlage nennt Gründung 2021 in San Francisco und die Unternehmensform Public Benefit Corporation.','Als Mitgründer werden unter anderem Dario und Daniela Amodei sowie Jared Kaplan genannt. Hintergrundwissen hilft bei der Einordnung des Anbieters.','Carmen fragt vor einer Auswahl: Wer liefert das Werkzeug und wo finde ich verlässliche Produktunterlagen?','Sagt der Gründungsort etwas über die Richtigkeit meiner Antwort?','Nein. Für die Aufgabe zählen überprüfbare Funktionen, Bedingungen und Ergebnisse.','Unternehmensgeschichte allein belegt weder aktuelle Produktqualität noch einen bestimmten Datenverarbeitungsort.'),
 (5,'Die Amodeis und die erklärte Mission','Die Folie stellt Dario und Daniela Amodei mit ihren Rollen und ihrem beruflichen Hintergrund vor. Sie beschreibt den Anspruch, nützliche und kontrollierbare KI zu entwickeln.','Solche Porträts erklären die Entstehungsgeschichte. Aktuelle Führungsrollen und zugespitzte Selbstaussagen sind für die heutige Tool-Auswahl keine feste Entscheidungsregel.','Tabea bewertet einen Storyboard-Entwurf an Verständlichkeit und Vorgaben, nicht am Lebenslauf eines Unternehmensgründers.','Was hilft dir für deinen Versuch mehr: ein Porträt oder ein konkreter Test?','Ein passender Test mit eigenen Kriterien. Das Porträt liefert Hintergrund.','Die Folien sind eine Momentaufnahme. Aus der Mission folgt keine Garantie für sichere Ausgaben.'),
 (6,'Forschung, Personen und Teamgröße','Die Vorlage verbindet Jared Kaplan mit Skalierungsforschung und Chris Olah mit dem Verstehen neuronaler Netze.','Skalierung fragt vereinfacht, wie sich Modelle durch mehr Rechenleistung oder Daten verändern. Interpretierbarkeit fragt, wie sich innere Vorgänge besser untersuchen lassen. Die Folie nennt außerdem 500+ Beschäftigte.','Ein größeres Küchenteam kann mehr kochen; das beweist nicht, dass dein konkretes Gericht gelingt.','Beweist die Teamgröße eine bessere Antwort?','Nein. Größe ist weder eine Genauigkeitsmessung noch ein Test deiner Aufgabe.','Die Personalzahl ist undatiert und wird hier nicht als aktueller Unternehmensstand bestätigt.'),
 (7,'Public Benefit Corporation verständlich','Eine Public Benefit Corporation hat neben wirtschaftlichen Zielen einen festgelegten gemeinwohlbezogenen Zweck. Die Folie betont Verantwortung und Transparenz.','Das ist eine Unternehmensform und ein erklärter Auftrag. Daraus lassen sich keine pauschalen Garantien für jede Geschäftsentscheidung oder Antwort ableiten.','Ein Unternehmen nennt Bildung als Ziel. Trotzdem prüft Carmen Preis, Leistung und Vertragsbedingungen vor dem Einsatz.','Bedeutet PBC automatisch gemeinnützig oder fehlerfrei?','Nein. Das ist weder die Aussage über Steuerstatus noch ein Qualitätssiegel für alle Produkte.','Die Zuspitzung „Ethik vor Profit“ beschreibt keinen bedingungslosen Vorrang bei jeder Entscheidung. Diese Passage ist eine Lernhilfe, keine Rechtsberatung zur Gesellschaftsform.'),
 (8,'Zuverlässig, verständlich und steuerbar','Die erklärte Mission nennt verlässliche Systeme, Einblick in ihr Verhalten und Möglichkeiten zur Steuerung.','Sicherheit, Interpretierbarkeit, Kontrolle und Transparenz sind unterschiedliche Themen. Eine erklärende Antwort macht die tatsächliche innere Verarbeitung noch nicht vollständig sichtbar.','Tabea fordert sechs Wörter pro Titelkarte und zählt nach. So prüft sie eine konkrete Vorgabe.','Ist eine überzeugende Erklärung gleich ein Beweis?','Nein. Du brauchst prüfbare Ausgangsdaten, Ergebnisse und gegebenenfalls tatsächliche Werkzeugspuren.','Ziele der Forschung nicht mit schon vollständig gelösten Eigenschaften verwechseln.'),
 (9,'Beteiligungen und Bewertungen kritisch lesen','Die Grafik zeigt behauptete Eigentumsanteile verschiedener Gruppen und eine Unternehmensbewertung.','Anteile, Investitionen und Bewertungen sind unterschiedliche Größen. Sie brauchen jeweils Stichtag und nachvollziehbare Belege. Prozentzahlen in einer Grafik werden durch ihre Darstellung nicht verlässlich.','Ingo entscheidet über einen Rechner nicht anhand einer großen Börsen- oder Bewertungszahl. Er prüft seine Rechenfälle.','Darfst du die gezeigte Bewertung als bestätigten aktuellen Fakt übernehmen?','Nein. Für diese konkreten Zahlen fehlt hier eine belastbare Belegkette.','Die Prozentverteilung und die behauptete Bewertung von 965 Milliarden US-Dollar werden nicht als verifiziert übernommen und spielen im Vergleich keine Rolle.'),
 (10,'Vergleich von Firmen ist kein Produkttest','Die Tabelle stellt Anthropic und OpenAI gegenüber. Sie vermischt Unternehmensform, Mission, Bewertungen und subjektive Urteile.','Bezeichnungen wie „hoch“ bei Transparenz oder ein zugespitzter Unternehmensstil brauchen Kriterien. Constitutional AI ist ein Ansatz, keine automatische Überlegenheit.','Carmen gibt beiden Werkzeugen dieselbe Website-Aufgabe und bewertet vorher festgelegte Punkte.','Was fehlt einer Tabelle mit „besser“ und „sicherer“?','Messbare Kriterien, aktuelle Belege und ein nachvollziehbarer Vergleich für dieselbe Aufgabe.','Die Beschreibung von OpenAI allein als „capped profit seit 2019“ und die angegebenen Bewertungen sind kein verlässlich belegter aktueller Vergleich. Keine aktuelle Rechtsstruktur oder Rangfolge daraus ableiten.'),
 (11,'Benchmarks sind begrenzte Testaufgaben','MMLU prüft Wissen in verschiedenen Fachgebieten, HumanEval Codeaufgaben, GSM8K Textrechnen und TruthfulQA ausgewählte Fragen zu irreführenden Antworten.','Jeder Test deckt nur einen Ausschnitt ab. Aussagekräftig wird ein Ergebnis erst mit genauer Modellversion, Datum, Testbedingungen und Messwerten.','Eine gute Rechennote beweist nicht, dass ein Modell Tabeas Bildsprache trifft. Dafür braucht sie eine eigene passende Probe.','Warum küren die Folien hier keinen belastbaren Sieger?','Es fehlen konkrete vergleichbare Ergebnisse und die Bedingungen der Messung.','Aus den bloßen Namen der Tests folgt keine aktuelle Rangliste der drei Arbeitsumgebungen.'),
 (12,'Weniger erfunden – aber wie gemessen?','Die Folie nennt weniger Halluzinationen sowie Bemühungen gegen schädliche oder verzerrte Ausgaben. Halluzination heißt hier: eine plausibel klingende, unbelegte oder falsche Angabe.','Für eine Prozentverbesserung braucht man mindestens Vergleichsmodell, Aufgaben, Version, Zeitpunkt und Methode. Bias bedeutet etwa systematische Verzerrungen; Tests können sie untersuchen, nicht pauschal ausschließen.','Eine KI erfindet einen Papierstandard. Ingo lässt die Quelle nennen und prüft, ob sie die Behauptung tatsächlich trägt.','Beweist „bis zu 50 Prozent weniger“ eine halbierte Fehlerquote in deiner Arbeit?','Nein. Ohne passende Messgrundlage lässt sich das nicht übertragen.','Die 50-Prozent-Angabe wird nicht als belegte Leistungszusage übernommen. Auch ein getestetes Modell kann falsche Inhalte erzeugen.'),
 (13,'Was Modelle unterstützen können','Die Folie nennt Programmieren, Schreiben, Analyse, Mathematik, Wissenschaft und Bildverständnis. Beispiele sind Erklären, Fehlersuche, Zusammenfassen und Übersetzen.','Bei Code werden etwa Python, JavaScript, Java, C++, Go und Rust genannt. Bei Bildern nennt die Vorlage PNG, JPEG, GIF und WebP sowie Texterkennung. Konkrete Eingabegrenzen hängen von der Anwendung ab.','Tabea lässt einen Screenshot beschreiben und vergleicht Texte und Farben mit dem Original.','Wird jeder erzeugte Code automatisch ausgeführt?','Nein. Dafür braucht die Anwendung ein verfügbares, berechtigtes Ausführungswerkzeug.','„Python im Chat ab Claude 4“ nicht als allgemeine Modellgarantie lesen: Code schreiben und Code tatsächlich ausführen sind verschiedene Fähigkeiten. OCR kann Zeichen falsch erkennen.'),
 (14,'Haiku, Sonnet und Opus einordnen','Die Folie erklärt Modellfamilien mit drei Rollen: Haiku eher schnell, Sonnet ausgewogen, Opus für anspruchsvolle Aufgaben.','Das ist eine grobe Orientierung. Modellversion, Aufgabe, Kontext, aktivierte Werkzeuge und Nutzungslimits verändern das Ergebnis. Die Familiennamen sind keine vollständige aktuelle Modellliste.','Für drei Überschriften reicht oft eine kleine Probe. Bei einem komplexen Projekt prüfst du mehrere Arbeitsweisen an denselben Fällen.','Ist das größte Modell für jede Aufgabe die beste Wahl?','Nein. Qualität, Zeit, Aufwand und Kosten müssen zur Aufgabe passen.','Keine heutige Siegerliste aus den alten Familienbeschreibungen ableiten. Aktuelle Verfügbarkeit im eigenen Tarif prüfen. [A3]'),
 (15,'Zugänge auseinanderhalten','Die Vorlage zeigt Web, Desktop, Claude Code, API, Mobilgeräte und Zugänge über Cloud-Anbieter wie Bedrock oder Vertex AI.','Zugang, Funktionen, Rechnung und Datenbedingungen können sich unterscheiden. Desktop bedeutet zunächst eine installierte Anwendung, nicht automatisch ein lokal rechnendes Modell.','Carmen installiert eine App am Mac. Für die Antworten eines gehosteten Modells bleibt eine Verbindung zum Dienst nötig.','Ist Claude nach der Desktop-Installation vollständig offline nutzbar?','Nein. Die Installation macht ein Cloud-Modell nicht zu einem lokalen Offline-Modell.','Die pauschale Offline-Aussage der Vorlage wird korrigiert. Auch eine Datei auf deinem Gerät kann für eine Modellanfrage übertragenen Kontext liefern. [A1, A2]'),
 (16,'Artifacts: ein Ergebnis zum Weiterarbeiten','Artifacts können etwa Code, Inhalte oder interaktive Entwürfe in einer eigenen Ansicht zugänglich machen.','Die Folie nennt Dokument- und Exportformate wie PDF, DOCX, XLSX und PPTX. Eine Vorschau, ein Quelltext und eine erzeugte Download-Datei sind verschiedene Ergebnisse. Nicht jeder Code läuft in jeder Vorschau.','Tabea sieht eine Storyboard-Vorschau. Sie prüft, ob ein bearbeitbarer Entwurf oder nur ein Bild vorliegt.','Beweist eine PDF-Erwähnung im Chat, dass eine PDF erzeugt wurde?','Nein. Es muss eine tatsächlich vorhandene, öffnungsfähige Datei geben.','Formate und Ausführungsfunktionen hängen von aktuellen Produktfunktionen und Werkzeugen ab. Eine Beschreibung ist kein Export.'),
 (17,'Computer Use: aus Text werden Handgriffe','Computersteuerung kann Bildschirme erfassen und mit passenden Werkzeugen klicken, tippen und Oberflächen bedienen.','Die Folie nennt etwa Browser, Formulare und CRM-Arbeit. Dafür braucht es eingerichtete Werkzeuge und passende Rechte. Eine beschriebene Handlung ist noch keine ausgeführte Handlung.','Carmen lässt auf einer lokalen Testseite einen Demo-Button betätigen und schaut selbst auf die sichtbare Bestätigung.','Was ist riskanter als einen Mailtext zu entwerfen?','Eine tatsächlich versendete Mail oder eine Änderung an echten Datensätzen.','Im Unterricht nur begrenzte Testseiten und fiktive Angaben verwenden. Nicht aus einem Demo-Video auf verfügbare Computersteuerung in jeder Sitzung schließen.'),
 (18,'Projects: ein gemeinsamer Ordner mit Auftrag','Ein Chat-Projekt bündelt Anweisungen, Gespräche und bereitgestellte Wissensquellen für einen Arbeitsbereich.','Die relevanten Dateien und Regeln müssen bewusst ausgewählt werden. Ein hochgeladenes Dokument wird nicht automatisch in jeder Antwort vollständig berücksichtigt oder fehlerfrei wiedergegeben.','Ingo stellt eine fiktive Preisregel und einen gewünschten Antwortstil bereit und prüft eine neue Frage daran.','Sind alle Projektdateien automatisch vollständig in jedem Satz berücksichtigt?','Nein. Quelle nennen lassen und die konkrete Aussage gegenprüfen.','Ein Chat-Projekt und ein Code-Projektordner sind verschiedene Konzepte, auch wenn beide Projekte heißen.'),
 (19,'Memory: was über Gespräche hinweg bleibt','Memory kann ausgewählten Kontext für spätere Gespräche bereitstellen. Chat-Suche kann frühere Gespräche auffinden.','Der aktuelle Anbieterleitfaden beschreibt eigene Einstellungen, Verwaltungsfunktionen und tarif- bzw. organisationsabhängige Verfügbarkeit. Verlasse dich nicht auf ein unbegrenztes oder wortgetreues Gedächtnis. [A6]','Carmen sagt, dass Rückfragen kurz sein sollen. Für einen verbindlichen Termin verwendet sie dennoch die aktuelle Projektquelle.','Ersetzt Memory die aktuelle Preis- oder Terminliste?','Nein. Verbindliche Angaben brauchen eine aktuelle benannte Quelle.','Einstellungen auf Folien sind Momentaufnahmen. Eigene Schalter und gespeicherte Inhalte im aktuellen Konto prüfen.'),
 (20,'Websuche: aktuell finden, dann prüfen','Websuche kann aktuelle Quellen zu Nachrichten, Preisen, Wetter, Produktdokumentation und anderen Fragen liefern.','Ein Suchtreffer ist kein Wahrheitsbeweis. Prüfe Datum, Anbieter, genaue Aussage und ob die Fundstelle die Behauptung wirklich unterstützt. Ohne Suchwerkzeug ist eine Antwort keine aktuelle Recherche.','Tabea sucht die Anleitung eines Videodienstes und kontrolliert, ob der beschriebene Anschluss für ihren Client gilt.','Worauf achtest du neben einem Link?','Auf Quelle, Zeitpunkt, konkrete Textstelle und passende Produktversion.','Auch Herstellerangaben können sich ändern. Dieses Heft nennt deshalb den Recherchetag und trennt Dokumentation von eigenen Tests.'),
 (21,'Claude Code im Terminalbild','Die Folie zeigt eine textbasierte Arbeitsoberfläche für die Projektarbeit. Im Terminal werden Befehle und Rückmeldungen als Text sichtbar.','Claude Code ist nicht auf das Terminal beschränkt. Aktuelle Dokumentation beschreibt auch Desktop, IDE und Web. Die Möglichkeiten unterscheiden sich. [A1, A2]','Carmen kann eine unterstützte Desktop-Oberfläche nutzen und trotzdem nach Dateien, Änderungen und Prüfungen fragen.','Muss ich Code verstehen, um einen ersten Auftrag zu formulieren?','Nein. Du musst aber Ziel und Prüfkriterien verstehen und bei unklaren Schritten nachfragen.','Ein Screenshot belegt eine Oberfläche zu einem Zeitpunkt, keine vollständige Funktionsliste für heute.'),
 (22,'MCP: Werkzeuge statt Copy-and-paste','MCP ist eine standardisierte Schnittstelle, über die Anwendungen externe Informationen und Werkzeuge nutzen können.','Die Folie nennt GitHub, Jira, Drive, Gmail, Notion, Slack, Asana und Datenbanken als mögliche Einsatzfelder. Für jeden Dienst braucht es eine konkrete Integration und passende Anmeldung. [A4, O3, G4]','Ingo liest fiktive CRM-Angebote über einen eingerichteten Anschluss, anstatt die Liste manuell zu kopieren.','Gibt MCP automatisch Zugriff auf alle Konten?','Nein. Server, Client, Konto, Rechte und konkrete Werkzeuge begrenzen den Zugriff.','Kompatibles Protokoll bedeutet noch keine identische Client-Unterstützung. Lesen, Schreiben, Export und Versand getrennt prüfen.'),
 (23,'Skills: ein wiederverwendbares Vorgehen','Ein Skill hält Anweisungen und gegebenenfalls Ressourcen für wiederkehrende Aufgaben bereit.','Beispiele der Folie sind Datenarbeit, Webentwicklung, maschinelles Lernen, Dokumente und eigene Abläufe. Ein Verzeichnis wie skills.sh ist eine Fundstelle, kein Gütesiegel.','Tabea hält fest: zuerst Zielgruppe, dann drei Szenen, dann Zeit und Wörter prüfen. Das kann ein Arbeitszettel oder ein Skill sein.','Was unterscheidet Skill und MCP?','Der Skill beschreibt den Arbeitsweg; MCP kann Werkzeuge und externe Daten anbinden.','Fremde Skills vor Nutzung prüfen. Anweisungen erteilen allein keine technischen Berechtigungen. [O4, A5, G5]'),
 (24,'Datenschutzeinstellungen bewusst lesen','Der Screenshot zeigt unter anderem Schalter für grobe Standortinformationen und die Verwendung zur Verbesserung von KI-Modellen sowie Verwaltungsbereiche für Exporte und geteilte Inhalte.','Ein ausgeschalteter Schalter im Bild zeigt nur den damaligen Zustand dieses abgebildeten Kontos. Er beweist weder deinen aktuellen Kontostand noch sämtliche Datenflüsse.','Carmen schaut im eigenen Konto nach, welche Angaben für den vorgesehenen Kursversuch eingestellt und freigegeben sind.','Reicht ein Foto eines ausgeschalteten Trainingsschalters als Nachweis für dein Konto?','Nein. Die tatsächlichen aktuellen Einstellungen und geltenden Bedingungen müssen geprüft werden.','Trainingseinstellung, Speicherung, Freigabe und Zugriff durch einen verbundenen Dienst sind verschiedene Fragen. Der Screenshot ersetzt keine Freigabe für echte Daten.'),
 (25,'Memory-Schalter getrennt verstehen','Der zweite Screenshot zeigt getrennte Einstellungen für das Suchen bzw. Referenzieren früherer Chats und für das Erzeugen von Erinnerungen.','Diese Funktionen betreffen unterschiedliche Arten von Kontext. Was heute verfügbar und voreingestellt ist, hängt auch von Tarif, Organisation und Produktstand ab. Die aktuelle Hilfe beschreibt die Verwaltung. [A6]','Tabea prüft, ob sie für einen einmaligen erfundenen Fall überhaupt dauerhaftes Erinnern benötigt.','Sind Chat-Verlauf und Memory dasselbe?','Nein. Ein gespeichertes Gespräch ist nicht automatisch identisch mit den daraus übernommenen Erinnerungen.','Die im Screenshot gezeigten ausgeschalteten Schalter nicht als allgemeine Standardeinstellung ausgeben. Keine Behauptung, dass dadurch alle Daten gelöscht oder alle Übertragungen verhindert seien.'),
 (26,'Adaptive Thinking und Aufwand','Die Folie beschreibt, dass ein Modell je nach Aufgabe mehr oder weniger Rechen- bzw. Denkaufwand einsetzen kann.','Mehr Aufwand kann Zeit und Verbrauch verändern. Ob und wie das einstellbar ist, hängt von Modell und Oberfläche ab. Eine lange Denkphase ist kein Genauigkeitsbeweis.','Eine kurze Überschrift braucht einen anderen Versuch als ein fehlerhafter Angebotsrechner mit mehreren Sonderfällen.','Woran erkennst du eine bessere Lösung?','An erfüllten Vorgaben und bestandenen passenden Prüfungen, nicht an der Wartezeit.','Die sichtbare Erklärung eines Modells ist kein vollständiger Blick in seine internen Abläufe.'),
 (27,'Die Bewerbungsübung richtig einordnen','Der Folientitel nennt Claude Code. Die beschriebenen Schritte passen überwiegend zu einem Projekt im normalen Claude-Chat: Lebenslauf bereitstellen, Anweisungen ergänzen und an zwei Stellenanzeigen testen.','Vorgesehen sind Rückfragen auf Deutsch, neue Chats zum Vergleichen, ein DOCX-Entwurf, Anschreiben und Interviewvorbereitung mit Stärken und Schwächen. Anschließend soll man alte und neue Ergebnisse vergleichen und den Auftrag verbessern.','Übe mit dem erfundenen Profil „Alex Beispiel“, drei belegten Fähigkeiten und einer fiktiven Anzeige. Jede Aussage muss aus dem Profil ableitbar bleiben.','Darf die KI für ein stärkeres Anschreiben zusätzliche Berufserfahrung erfinden?','Nein. Fehlende Angaben als Rückfrage behandeln. Verbesserung heißt nicht Erfindung.','Die erwähnte externe LinkedIn-Anweisung liegt nicht vollständig vor und wird nicht als Kursvorgabe übernommen. Chat-Projekt und Claude Code auseinanderhalten. Die Chat-Übung ist auch in Langdock möglich; DOCX-Ausgabe hängt vom verfügbaren Werkzeug ab.'),
 (28,'Weiterlernen mit Quellen','Die Schlussfolie verweist auf weiterführende Videos und Seiten sowie auf Modell-, Prompt- und Hilfeseiten von Anthropic.','Die Namen Suprmind und KI Creators Club sind zusätzliche Fundstellen, nicht automatisch aktuelle oder überprüfte Produktdokumentation. Für Funktionen zuerst die offiziellen Unterlagen nutzen.','Carmen prüft eine Videoanleitung gegen die heutige Herstellerseite, bevor sie die Einrichtung übernimmt.','Welche Quelle nutzt du zuerst für eine heutige Preis- oder Kompatibilitätsfrage?','Die aktuelle offizielle Preis- oder Dokumentationsseite mit Datum und passenden Bedingungen.','Alle Quellen dieses Hefts sind am 19.10.2026 recherchiert. Die Folien stammen aus Juli 2026. Links und Produktnamen können sich später ändern.')
]

for start in range(0,28,2):
 blocks=[]
 for n,title,simple,detail,example,q,a,correction in SLIDES[start:start+2]:
  blocks += [('h',f'Folie {n:02} · {title}'),('p',simple+' '+detail),('p','Beispiel: '+example),('check','Denkfrage: '+q),('answer','Mögliche Antwort: '+a)]
  if correction:blocks += [('note',correction)]
 page(f'folien-{start+1}',f'Folien {start+1:02} und {start+2:02}','Alle 28 Originalfolien · verständlich begleitet',blocks)

for i in range(0,len(SOURCES),8):
 blocks=[('p','Recherchetag: 19.10.2026. Offizielle Herstellerseiten. Der Funktionsumfang wurde anhand der Dokumentation eingeordnet, nicht durch eine vollständige Installation oder einen Vergleichstest bestätigt. Quellenkennungen im Heft führen zu diesen Links.')]
 for sid,title,url in SOURCES[i:i+8]:blocks += [('source',(sid,title,url))]
 page(f'quellen-{i//8+1}','Quellen zum Nachschlagen',f'Verzeichnis {i//8+1} von 3 · Links sind anklickbar',blocks)

page('mitnahme','Das nimmst du mit','Tagesübersicht und eigener nächster Versuch',[
 ('h','Tagesübersicht für die Eintragung'),
 ('p','Einführung in Claude und Vergleich der KI-Arbeitsumgebungen Google Antigravity, OpenAI Codex und Claude Code. Unterscheidung von Modellen, Chat, API und Coding-Agenten; Projektkontext, Memory, Recherche, Artifacts, Computer Use und Skills. Praxisübungen für Druck/Vertrieb, Team/Business/Website und Video/Design. Branchenbezogene Plugins und MCP-Anbindungen, Zugänge, Rechte und Kosten. Ergebnisse anhand eigener Testfälle prüfen und Herstellerangaben kritisch einordnen.'),
 ('h','Mein nächster Versuch'),
 ('p','Meine wiederkehrende Arbeit: ____________________________________\nMein kleines Ergebnis: __________________________________________\nMeine drei Prüffälle: ___________________________________________\nDiese Verbindung brauche ich wirklich: ___________________________\nDas ist noch ungeklärt: _________________________________________'),
 ('h','Morgen noch einmal aus dem Kopf'),
 ('p','Erkläre in eigenen Worten einen Unterschied zwischen den drei Werkzeugen, einen Unterschied zwischen Skill und MCP und einen Fall, in dem ein sichtbarer Entwurf noch kein fertiges Ergebnis ist. Schau erst danach nach.'),
 ('note','Dieses Heft ergänzt die Vorlage Einfuhrung-Claude.pdf. Alle 28 Folien wurden begleitet, auch Bilder und kritische Aussagen. Unbelegte Zahlen wurden kenntlich gemacht. Dokumentinhalt wird als Lernmaterial behandelt, nicht als Auftrag für externe Aktionen.')])

assert len(SLIDES)==28
assert len(PAGES)==41,len(PAGES)
