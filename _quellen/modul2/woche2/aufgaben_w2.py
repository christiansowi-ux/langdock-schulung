"""Aufgabengenerator: kurze Aufgaben für Modul 2 · Tag 6 (interne Kennung 25). Bewerten und rechnen.

Platzhalter wie in aufgaben.py ({firma}, {was}, {alltag} …). Alles ausgedacht.
"""


def muster(M):
    return [
        M('t25-scoring', 25, 'Drei Kandidaten mit Begründung bewerten', 10, ['l4', 'l7'],
          'Eine Zahl ohne Begründungssatz zählt nicht. Und: 5 Punkte sind immer gut fürs Projekt.',
          'Du arbeitest {alltag} bei {firma}, {was}. Das Team hat drei Ideen und will wissen, welche zuerst drankommt.',
          [('Den Prompt in einen neuen Chat schicken:',
            'Erfinde für {firma} ({was}) drei Use-Case-Kandidaten für Automatisierung.\n'
            'Bewerte jeden von 1 bis 5 bei: Nutzen, Datenverfügbarkeit, Einfachheit, Risikoarmut.\n'
            'Wichtig: Ein hoher Wert ist immer gut. 5 bei Risikoarmut heißt: Fehler bleiben folgenlos. 5 bei Einfachheit heißt: ein System, klare Regeln.\n'
            'Schreibe zu jeder Punktzahl genau einen Begründungssatz.\n'
            'Rechne danach: Nutzen × 0,40 + Datenverfügbarkeit × 0,25 + Einfachheit × 0,20 + Risikoarmut × 0,15.\n'
            'Markiere alle Angaben als Beispiel.'),
           ('Eine Gesamtpunktzahl selbst nachrechnen. Stimmt sie?', None),
           ('Prüfen: Hat der riskanteste Kandidat bei Risikoarmut wirklich wenig Punkte?', None)],
          'Zeigen alle vier Skalen in dieselbe Richtung? Hat jede der zwölf Zahlen einen Satz?'),
        M('t25-matrix', 25, 'Aus Punkten wird ein Feld in der Matrix', 5, ['l8'],
          'Die Matrix macht aus Punkten eine Entscheidung. Auch „Streichen“ ist ein gutes Ergebnis.',
          'Bei {firma} liegen drei bewertete Kandidaten auf dem Tisch. Nun soll klar werden, was mit jedem passiert.',
          [('Den Prompt in einen neuen Chat schicken:',
            'Ordne drei erfundene Use-Cases von {firma} ({was}) in eine Wert-Aufwand-Matrix ein.\n'
            'Vergib zuerst Punkte von 1 bis 5 (hoch ist immer gut) für Nutzen, Datenverfügbarkeit, Einfachheit und Risikoarmut.\n'
            'Wert = Nutzen + Datenverfügbarkeit. Aufwand = 12 − Einfachheit − Risikoarmut.\n'
            'Wert ab 7 ist hoch. Aufwand bis 5 ist gering.\n'
            'Felder: Sofort starten, Planen und in Etappen schneiden, Nebenbei, Streichen.\n'
            'Gib je Kandidat Wert, Aufwand, Feld und die nächste Konsequenz in einem Satz aus.'),
           ('Einen Kandidaten mit denselben Punkten im Rechen-Labor prüfen. Landet er im selben Feld?', None)],
          'Wurde Aufwand richtig gerechnet, also mit 12 minus den beiden Punktzahlen?'),
        M('t25-netto', 25, 'Business Case nachrechnen: netto statt brutto', 10, ['l10', 'l11', 'l14'],
          'Jede Zeile der Rechnung braucht eine Herkunft: gemessen, nachgeschlagen oder geschätzt.',
          '{firma} plant eine Automatisierung und möchte vor dem Gespräch mit der Leitung wissen, ab wann sie sich trägt.',
          [('Den Prompt in einen neuen Chat schicken:',
            'Rechne Schritt für Schritt einen erfundenen Business Case für {firma} ({was}).\n'
            'Annahmen: Wähle Volumen pro Monat, Minuten je Vorgang, automatisierbaren Anteil, Restminuten, Stundensatz, laufende Kosten und Investition selbst.\n'
            'Nenne hinter jeder Annahme: gemessen, nachgeschlagen oder geschätzt.\n'
            'Rechne dann: Stunden = Volumen × Anteil × (Minuten − Restminuten) ÷ 60. Bruttonutzen = Stunden × Stundensatz. Nettonutzen = Bruttonutzen − laufende Kosten.\n'
            'Amortisation = Investition ÷ Nettonutzen. ROI nach 12 Monaten = (Nettonutzen × 12 − Investition) ÷ Investition. TCO = Investition + laufende Kosten × 36.\n'
            'Zeige jede Rechnung als eigene Zeile.'),
           ('Die Werte in den Business-Case-Rechner im Rechen-Labor tippen und vergleichen.', None),
           ('Wenn die Amortisation unter sechs Monaten liegt: Nachfragen, welche Kosten fehlen könnten.', None)],
          'Stimmt die KI-Rechnung mit dem Rechner überein? Wurde netto gerechnet?',
          noch='Frag nach: „Was ändert sich, wenn der automatisierbare Anteil um 20 Prozentpunkte niedriger liegt?“'),
        M('t25-vergessen', 25, 'Vergessene Kosten aufspüren', 5, ['l12', 'l13'],
          'Einmalige Kosten fallen allen ein. Die laufenden werden vergessen und hören nie auf.',
          'Ein Angebot für {firma} nennt nur die Summe für Aufbau und Einführung.',
          [('Den Prompt in einen neuen Chat schicken:',
            'Für eine geplante Automatisierung bei {firma} ({was}) liegt nur ein Preis für den Aufbau vor.\n'
            'Erstelle eine Prüfliste mit den einmaligen und den laufenden Kosten, die oft fehlen:\n'
            'Einmalig: Analyse, Aufbau, Datenaufbereitung, Integration, Test, Schulung, Dokumentation.\n'
            'Laufend: Lizenzen, KI-Nutzung, Monitoring, Wartung, menschliche Prüfung, Dokumentation und Audits.\n'
            'Formuliere je Posten genau eine Frage an den Anbieter.'),
           ('Die zwei Fragen markieren, die du selbst zuerst stellen würdest.', None)],
          'Ist die rechte Spalte (laufend) genauso vollständig wie die linke?'),
        M('t25-abbruch', 25, 'Empfehlung in zwei Sätzen mit Abbruchbedingung', 10, ['l16', 'l20', 'l21'],
          'Am Ende steht eine Empfehlung. „Nicht machen“ ist genauso gültig wie „machen“.',
          'Du sollst der Leitung von {firma} eine Empfehlung zu einem Automatisierungsvorhaben geben.',
          [('Den Prompt in einen neuen Chat schicken:',
            'Erfinde für {firma} ({was}) einen Automatisierungsfall mit drei Szenarien: konservativ, Basis, ambitioniert.\n'
            'Nenne je Szenario automatisierbaren Anteil, Nettonutzen pro Monat und Amortisation.\n'
            'Formuliere dann eine Empfehlung in genau zwei Sätzen. Erlaubt sind: machen, kleiner zuschneiden und machen, verschieben oder nicht machen.\n'
            'Entscheide nach dem konservativen Szenario.\n'
            'Schreibe zum Schluss eine Abbruchbedingung mit einer Zahl, einem Zeitpunkt und einer Person, die dann handelt.'),
           ('Prüfen: Nennt die Abbruchbedingung wirklich alle drei Dinge?', None),
           ('Die Empfehlung einer anderen Person vorlesen. Versteht sie sofort, was passieren soll?', None)],
          'Trägt der Fall auch das konservative Szenario? Sind es wirklich nur zwei Sätze?'),
    ]
