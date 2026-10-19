"""Tag 8 (Lektion 7: Skills, Folien 1-14) - wird von kurs.py eingelesen.
Ergaenzt um Fakten aus docs.langdock.com (Skills: Erstellen, FAQ) - dort mit 'quelle': 'Langdock'."""
TAG8 = {
    'titel': 'Skills – einmal erklären, immer anwenden',
    'unter': 'Lektion 7 · Skills',
    'datum': '07.10.2026',
    'folien': 'Skills.pdf',
    'kurz': 'Was ein Skill ist, wie Langdock ihn automatisch anwendet, wie man ihn baut und testet – und warum man fremde Skills nie ungeprüft übernimmt.',
    'lernheft': 'Lernheft_Tag8_Skills.pdf',
    'learnings': [
        {'id': 'l1', 'folie': 2, 'satz': 'Ein Skill ist ein ausgefeilter Prompt, den man immer wieder verwenden kann.',
         'erklaert': 'Ohne Skill wird der perfekte Prompt jedes Mal neu getippt, jede Person im Team geht anders vor und das Wissen steckt im Kopf. '
                     'Mit Skill wird das Briefing einmal erstellt und gespeichert – die KI wendet es automatisch und für alle gleich an.'},
        {'id': 'l2', 'folie': 3, 'satz': 'Ein Skill ist ein gespeichertes Briefing – einmal geschrieben, ab dann automatisch angewendet.',
         'erklaert': 'Er holt wiederkehrendes Wissen aus dem Kopf ins Werkzeug. Wie ein Einarbeitungs-Leitfaden für neue Leute im Team: '
                     'einmal gründlich geschrieben, danach muss man nichts mehr von vorn erklären.'},
        {'id': 'l3', 'folie': 4, 'satz': 'Die KI liest zuerst nur die Kurzbeschreibung – die Anweisungen lädt sie erst, wenn sie passen.',
         'erklaert': 'Aktive Skills warten im Hintergrund. Bei jeder Nachricht prüft die KI die kurzen Beschreibungen; passt eine, lädt sie die vollen '
                     'Anweisungen und führt sie aus – ohne dass man den Skill nennen muss. So bleiben viele Skills gleichzeitig nutzbar.'},
        {'id': 'l4', 'folie': 5, 'satz': 'Prompt, Skill, Agent: jetzt getippt, automatisch im Hintergrund, gezielt aufgerufen.',
         'erklaert': 'Ein Prompt ist eine einzelne Anweisung im Moment. Ein Skill ist ein wiederverwendbares Anweisungs-Set, das von selbst anspringt. '
                     'Ein Agent ist eine eigene Umgebung mit Anweisungen, Wissen und Werkzeugen, zu der man gezielt hingeht. '
                     'Faustregel: Soll etwas immer gelten, ohne dass jemand irgendwohin navigiert, ist es ein Skill.'},
        {'id': 'l5', 'folie': 6, 'satz': 'Skills entstehen auf drei Wegen: selbst schreiben, mit dem Chat erstellen oder als Datei hochladen.',
         'erklaert': 'Manuell schreiben gibt die meiste Kontrolle. „Mit Chat erstellen“ macht aus einer Beschreibung in normaler Sprache einen Entwurf. '
                     'Eine SKILL.md- oder ZIP-Datei eignet sich zum Austausch zwischen Werkzeugen und Teams. Empfehlung: mit dem Chat beginnen, dann von Hand verfeinern.'},
        {'id': 'l6', 'folie': 7, 'satz': 'Neue Skills gibt es in der Langdock-Bibliothek, im eigenen Wissen, im Internet – oder man baut sie selbst.',
         'erklaert': 'Die Langdock-Bibliothek bietet fertige, getestete Pakete für den schnellen Start. Interne Anleitungen, Fragen-Listen oder bewährte '
                     'Abläufe lassen sich in Skills verwandeln. Online helfen große Sammlungen – und das eigene Fachwissen ergibt maßgeschneiderte Skills.'},
        {'id': 'l7', 'folie': 8, 'satz': 'Online gibt es große Skill-Sammlungen – Suchwort „Claude Skills“.',
         'erklaert': 'Beispiele von der Folie: das Verzeichnis „Awesome MCP Servers“ mit Agent Skills, die öffentliche Sammlung von Anthropic auf GitHub '
                     '(anthropics/skills) und große Community-Sammlungen. Praktisch als Ideenquelle – aber nie ungeprüft übernehmen.'},
        {'id': 'l8', 'folie': 9, 'satz': 'Fremde Skills nie ungeprüft übernehmen.',
         'erklaert': 'Herkunft prüfen, Verhalten verstehen, Datenschutz sicherstellen. Ein ungeprüfter Skill kann falsche Ergebnisse liefern, Daten '
                     'preisgeben oder verändern – im schlimmsten Fall schleust er Schadsoftware ein.'},
        {'id': 'l9', 'folie': 10, 'satz': 'Vor dem Aktivieren: alle Dateien, Zugriffe, Links und Rechte prüfen.',
         'erklaert': 'SKILL.md, Skripte und alle weiteren Dateien im ZIP ansehen. Auf unerwartete Netzwerk- oder Dateizugriffe und fremde Adressen achten. '
                     'Einem Skill nur die Rechte und Verbindungen geben, die er wirklich braucht. Tipp der Folie: einen Skill-Scanner nutzen.'},
        {'id': 'l10', 'folie': 11, 'satz': 'Ein Skill = eine Aufgabe.',
         'erklaert': 'Keine Alles-Könner, keine vagen Beschreibungen, nichts ungetestet einsetzen. Stattdessen klare Auslöser, ein festes Ausgabeformat '
                     'und gründliche Tests vor dem Teilen. Teile und herrsche: lieber drei kleine, verlässliche Skills als einen überladenen.'},
        {'id': 'l11', 'folie': 11, 'satz': 'Die Beschreibung entscheidet, wann ein Skill anspringt.',
         'erklaert': 'Die KI wählt Skills nach der Bedeutung ihrer Beschreibung, nicht nach dem Namen. Eine vage Beschreibung lässt den Skill zur '
                     'falschen Zeit oder gar nicht anspringen. Darum hinein: Wann soll er helfen, mit welchen Worten fragen Leute danach?'},
        {'id': 'l12', 'folie': 12, 'satz': 'Mit Integrationen wird die KI vom Ratgeber zum Macher.',
         'erklaert': 'Ein Skill allein gibt nur Anweisungen. Kommt eine Integration dazu – eine Verbindung zu einem anderen System wie E-Mail, '
                     'Ablage oder Kundendatenbank –, kann die KI die Anweisung dort auch ausführen.'},
        {'id': 'l13', 'folie': 13, 'satz': 'Sechs Ideen für erste Skills: Protokoll, Marken-Ton, Nachfassen, Bewerbung, Support, Pflichthinweise.',
         'erklaert': 'Protokoll-Skill (Notizen → Protokoll mit Aufgabenliste), Marken-Ton-Skill (Texte im Hausstil), Follow-up-Skill (Nachfass-E-Mail '
                     'aus Gesprächsnotizen), Interview-Skill (Bewerbungsnotizen nach festem Raster), Support-Skill (Antworten im Styleguide) und '
                     'Compliance-Skill (Pflichthinweise in Kundentexten).'},
        {'id': 'l14', 'folie': 14, 'satz': 'Vor dem Bau klären: Aufgabe, Auslöser, feste Infos, Ergebnisformat – danach testen.',
         'erklaert': 'Welche Aufgabe kommt immer wieder? Mit welchen Worten wird danach gefragt? Was gehört fest in die Anweisungen? Wie soll das '
                     'Ergebnis jedes Mal aussehen? Start: Skills → „+ Skill hinzufügen“ → „Mit Chat erstellen“. Bonus: 2–3 Testszenarien, ob der Skill '
                     'im richtigen Moment anspringt und das Format einhält.'},
        {'id': 'l15', 'folie': None, 'quelle': 'Langdock', 'satz': 'Skills haben Grenzen: bis zu 30 aktive, kein Gedächtnis, Skripte laufen nicht.',
         'erklaert': 'Laut Langdock-Hilfe: bis zu 30 aktive Skills pro Person (zu viele führen zu falscher Auswahl), kein Gedächtnis über Gespräche hinweg, '
                     'keine aktuellen Daten ohne Integration. Skripte in einem ZIP dienen nur als Nachschlagewerk und werden nicht ausgeführt. '
                     'Einen Skill kann man auch bewusst über das @-Menü wählen.'},
    ],
    'begriffe': [
        ('Skill', 'Ein gespeichertes Briefing für die KI, das automatisch angewendet wird, wenn es zur Anfrage passt.'),
        ('Beschreibung', 'Der kurze Text, an dem die KI erkennt, wann ein Skill passt – der wichtigste Teil.'),
        ('Anweisungen', 'Der ausführliche Teil des Skills: was die KI genau tun soll und in welchem Format.'),
        ('Auslöser', 'Die Situation oder die Worte, bei denen ein Skill anspringen soll (englisch: Trigger).'),
        ('SKILL.md', 'Eine Textdatei, in der ein Skill gespeichert ist – zum Hochladen und Austauschen.'),
        ('Skill-Bibliothek', 'Sammlung fertiger, geprüfter Skills in Langdock.'),
        ('Agent', 'Eine eigene Umgebung mit Anweisungen, Wissen und Werkzeugen, die man gezielt aufruft.'),
        ('Integration', 'Eine Verbindung zu einem anderen System (z. B. E-Mail oder Ablage), über die die KI handeln kann.'),
        ('Skill-Scanner', 'Ein Werkzeug, das Skills vor dem Einsatz auf Risiken prüft.'),
        ('Testszenario', 'Eine Probe-Anfrage, mit der man prüft, ob ein Skill richtig anspringt und das Format einhält.'),
    ],
    'karten': [
        ('Was ist ein Skill?', 'Ein gespeichertes Briefing für die KI – einmal geschrieben, ab dann automatisch angewendet.'),
        ('Welches Problem löst ein Skill?', 'Gute Prompts müssen nicht mehr neu getippt werden, und das ganze Team arbeitet gleich.'),
        ('Was liest die KI bei jeder Nachricht?', 'Nur die kurze Beschreibung jedes aktiven Skills – die Anweisungen lädt sie erst, wenn es passt.'),
        ('Prompt, Skill oder Agent: Was springt von selbst an?', 'Der Skill – im Hintergrund, wenn er zur Anfrage passt.'),
        ('Die Faustregel für Skills?', 'Soll etwas immer gelten, ohne dass jemand irgendwohin navigiert → Skill.'),
        ('Drei Wege, einen Skill zu erstellen?', 'Manuell schreiben, mit dem Chat erstellen, SKILL.md oder ZIP hochladen.'),
        ('Womit sollte man anfangen?', 'Mit dem Chat erstellen – und den Entwurf danach von Hand verfeinern.'),
        ('Warum ist die Beschreibung so wichtig?', 'Sie entscheidet, ob und wann der Skill anspringt. Vage = falsche Zeit oder gar nicht.'),
        ('Was prüft man vor dem Aktivieren eines fremden Skills?', 'Alle Dateien, Netzwerk- und Dateizugriffe, externe Links und die Rechte.'),
        ('Die wichtigste Regel beim Bauen?', 'Ein Skill = eine Aufgabe. Lieber drei kleine als einen Alles-Könner.'),
        ('Was macht eine Integration?', 'Sie verbindet die KI mit einem System – aus dem Ratgeber wird ein Macher.'),
        ('Wie testet man einen neuen Skill?', 'Mit 2–3 Testszenarien: Springt er im richtigen Moment an? Hält er das Format – auch bei knappen Anfragen?'),
    ],
    'test': [
        {'frage': 'Was liest die KI bei jeder Nachricht von allen aktiven Skills?',
         'optionen': ['Die vollständigen Anweisungen', 'Nur die kurze Beschreibung', 'Gar nichts – man muss den Skill nennen'], 'richtig': 1,
         'warum': 'Erst wenn die Beschreibung passt, lädt die KI die vollen Anweisungen (Folie 4).'},
        {'frage': 'Eine Regel soll in jedem Chat gelten, ohne dass jemand etwas aufruft. Was passt?',
         'optionen': ['Ein Prompt', 'Ein Skill', 'Ein Agent'], 'richtig': 1,
         'warum': 'Faustregel von Folie 5: Soll etwas immer gelten, ohne Navigation → Skill.'},
        {'frage': 'Womit beginnt man laut Folie am besten einen neuen Skill?',
         'optionen': ['Mit dem Chat erstellen, dann von Hand verfeinern', 'Sofort eine ZIP-Datei aus dem Internet laden', 'Mit einem Skill, der alles kann'], 'richtig': 0,
         'warum': 'So entsteht schnell ein Entwurf, den man gezielt anpasst (Folie 6).'},
        {'frage': 'Ein fremder Skill enthält eine unbekannte Web-Adresse, an die Daten gehen sollen. Was tun?',
         'optionen': ['Aktivieren und abwarten', 'Nicht aktivieren, sondern genau prüfen', 'Nur den Namen ändern'], 'richtig': 1,
         'warum': 'Unerwartete Netzwerk-Aufrufe und externe Links sind Warnzeichen (Folie 10).'},
        {'frage': 'Was ist besser?',
         'optionen': ['Ein Skill für Protokolle, Mails und Social Media', 'Drei kleine Skills mit je einer Aufgabe', 'Gar keine Beschreibung'], 'richtig': 1,
         'warum': 'Ein Skill = eine Aufgabe. Teile und herrsche (Folie 11).'},
        {'frage': 'Was braucht ein Skill, damit die KI auch in einem anderen System handeln kann?',
         'optionen': ['Eine Integration', 'Eine längere Beschreibung', 'Mehr Großbuchstaben'], 'richtig': 0,
         'warum': 'Skill = Anweisung, Integration = Verbindung, zusammen = Handlung (Folie 12).'},
    ],
}
