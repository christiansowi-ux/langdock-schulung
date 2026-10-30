"""Aufgabengenerator: kurze Use-Case-Aufgaben für Modul 2 · Tag 5 (interne Kennung 24).

Platzhalter wie in aufgaben.py ({firma}, {was}, {alltag}, {beschwerde} …). Alles ausgedacht.
"""


def muster(M):
    return [
        M('t24-zeitfresser', 24, 'Zeitfresser rechnen statt raten', 10, ['l24'],
          'Die nervigste Aufgabe ist selten die teuerste. Erst rechnen, dann bewerten.',
          'Du arbeitest {alltag} bei {firma}, {was}. Ihr wollt herausfinden, welche wiederkehrende Arbeit am meisten Zeit frisst.',
          [('Den Prompt in einen neuen Chat schicken:',
            'Du hilfst bei einer Zeitfresser-Analyse für {firma} ({was}).\n'
            'Liste 8 typische Tätigkeiten auf, die mindestens wöchentlich vorkommen.\n'
            'Gib als Tabelle aus: Tätigkeit | Häufigkeit pro Monat (Schätzung) | Minuten je Vorgang (Schätzung) | Minuten pro Monat.\n'
            'Rechne die letzte Spalte aus (Häufigkeit × Minuten) und sortiere absteigend.\n'
            'Markiere alle Zahlen als Schätzung.'),
           ('Zwei Zeilen selbst nachrechnen. Stimmt die Multiplikation?', None),
           ('Die Top 3 in den Zeitfresser-Rechner im Use-Case-Labor übernehmen.', None)],
          'Rechnet die KI richtig? Sind die Schätzungen plausibel – oder nur nach Gefühl?',
          noch='Frag nach: „Welche der Top 3 wäre am leichtesten als fester Workflow ohne KI lösbar?“'),
        M('t24-interview', 24, 'Schmerz-Interview üben', 10, ['l31'],
          'Nicht fragen, was automatisiert werden soll – sondern was weh tut. Und wörtlich mitschreiben.',
          'Bei {firma} willst du mit einer Person aus dem Team ein kurzes Schmerz-Interview führen.',
          [('Den Prompt in einen neuen Chat schicken:',
            'Wir machen ein Rollenspiel. Du arbeitest bei {firma} ({was}) und hast viel Routinearbeit.\n'
            'Ich stelle dir nacheinander vier Fragen. Antworte jeweils mit 2–3 Sätzen, ehrlich und konkret, mit erfundenen Beispielen.\n'
            'Warte nach jeder Antwort auf meine nächste Frage.'),
           ('Die vier Fragen einzeln stellen: 1. Was machst du regelmäßig, obwohl du weißt, dass ein Computer es könnte? '
            '2. Wo wartest du auf jemand anderen? 3. Was musst du zweimal eintippen? 4. Wann hat das zuletzt nicht funktioniert – und was ist dann passiert?', None),
           ('Die Antworten wörtlich ins Use-Case-Labor kopieren und Wartezeiten und Doppeleingaben markieren.', None)],
          'Wo stecken Wartezeiten und Doppeleingaben? Das sind oft die besten Kandidaten.'),
        M('t24-steckbrief', 24, 'Aus einer Idee wird ein Steckbrief', 10, ['l28', 'l25'],
          'Was nicht ins Raster passt, ist noch eine Idee. Nutzen braucht Zahl, Einheit und Zeitraum.',
          '{firma} ist {was}. Eine Idee aus dem Team: „Wir sollten KI für unsere Anfragen nutzen.“',
          [('Den Prompt in einen neuen Chat schicken:',
            'Mach aus dieser vagen Idee einen Use-Case-Steckbrief für {firma} ({was}): „Wir sollten KI für unsere Anfragen nutzen.“\n'
            'Felder: Name, Verantwortlich, Problem, Auslöser, Input, Was übernimmt das System, Output, Volumen, Nutzen, Richtig wenn, Nicht dabei.\n'
            'Wenn du etwas nicht weißt, schreib „OFFEN – nachfragen bei …“ statt zu raten.\n'
            'Nutzen immer als Zahl + Einheit + Zeitraum, als Schätzung markiert.'),
           ('Prüfen: Welche Felder sind OFFEN? Wer könnte sie beantworten?', None)],
          'Rät die KI Zahlen, statt OFFEN zu schreiben? Dann nachschärfen: „Erfinde keine Zahlen.“'),
        M('t24-stufe', 24, 'Welche Autonomie-Stufe passt?', 5, ['l29', 'l30'],
          'Die Stufe wird pro Pfad festgelegt: Standardfall oft Stufe 3, Ausnahme Stufe 2.',
          'Bei {firma} gibt es diese Beschwerde: {beschwerde} Ein System soll künftig Antwortentwürfe für Beschwerden vorbereiten.',
          [('Den Prompt in einen neuen Chat schicken:',
            'Ein Workflow bei {firma} bereitet Antwortentwürfe auf Beschwerden vor. Beispiel: {beschwerde}\n'
            'Ordne Standardfall und Ausnahme je einer Autonomie-Stufe zu (0 manuell, 1 Assistenz, 2 Mensch gibt jeden Fall frei, '
            '3 System entscheidet mit Stichproben, 4 ohne Aufsicht) und begründe kurz.\n'
            'Prüfe auch: Braucht es dafür überhaupt ein Sprachmodell, oder reicht eine Regel?'),
           ('Mit der Treppe im Use-Case-Labor vergleichen.', None)],
          'Kundenwirksame Antworten laufen meist über einen Menschen (Stufe 2). Wer 200 Entwürfe am Tag nur durchklickt, ist faktisch Stufe 4.'),
    ]
