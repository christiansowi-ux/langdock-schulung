"""Mini-Spiele und Alarmsatz-Bingo für Tag 7. Lernheft, Spiele-Reiter und Präsenter nutzen dieselben Daten.

Karte: (Text, richtige Option, Erklärung). Bei RUECKFRAGE hat jede Karte eigene Optionen.
Alle Fälle sind erfunden, die Regeln stammen von den Folien (Folie 9/10, 12, 15/16, 15).
"""

WUNSCH = dict(
    id='wunsch', titel='Wunsch oder Ziel?', folie='Folien 9 und 10',
    intro='Acht Sätze aus echten Kick-off-Runden (na gut, erfunden). Welcher ist ein prüfbares Ziel?',
    optionen=['Wunsch', 'Ziel'],
    karten=[
     ('Wir wollen weniger E-Mails manuell bearbeiten.', 'Wunsch', 'Original von Folie 9. Wie viel weniger? Welche? Woran gemessen? Alles offen.'),
     ('Unser Ablauf soll moderner werden.', 'Wunsch', '„Modern“ ist keine Maßeinheit. Dein Kühlschrank ist auch modern und hat trotzdem nichts automatisiert.'),
     ('70 Prozent der Rechnungen unter 1.000 Euro ohne Klärungsbedarf werden ohne manuelle Prüfung freigegeben, gemessen an der Freigabequote im Monatsbericht, ab drei Monaten nach Start.', 'Ziel', 'Das Musterbeispiel von Folie 10: alle fünf Bausteine sind da.'),
     ('Wir machen jetzt was mit KI.', 'Wunsch', 'Das ist kein Ziel, das ist eine Lösung auf der Suche nach einem Problem.'),
     ('Jeder eingehende Lead enthält beim Übergang an den Vertrieb mindestens fünf definierte Zusatzfelder, gemessen am Anteil vollständiger Datensätze im CRM, ab dem zweiten Monat.', 'Ziel', 'Auch von Folie 10. Klingt sperrig, lässt sich aber in sechs Monaten eindeutig prüfen.'),
     ('90 Prozent der Druckanfragen im Standardformat werden automatisch vorsortiert.', 'Wunsch', 'Knapp! Anteil, Fallmenge und Handlung stehen da. Es fehlen Kennzahl und Zeitpunkt.'),
     ('Die Durchlaufzeit von Standardrechnungen sinkt bis Ende März von 5 auf 1,5 Tage, gemessen an den Zeitstempeln im System.', 'Ziel', 'Menge, Fallmenge, Handlung, Kennzahl, Zeitpunkt. Alles dabei, und sogar mit Ausgangswert.'),
     ('Alle sollen mit dem neuen Werkzeug glücklicher sein.', 'Wunsch', 'Schön wär’s. Woran misst du Glück? An der Lautstärke in der Kaffeeküche?'),
    ])

RUECKFRAGE = dict(
    id='rueckfrage', titel='Welche Rückfrage passt?', folie='Folien 14 bis 16',
    intro='Kim aus der Buchhaltung erzählt. Du fragst nach. Finde die Rückfrage, die wirklich etwas ans Licht bringt.',
    karten=[
     ('„Normalerweise leite ich die Rechnung gleich weiter.“', 'Und wenn nicht? Wie oft ist „nicht normalerweise“?', 'Hinter „normalerweise“ steckt eine unbekannte Menge an Ausnahmen.',
      ['Super, dann weiß ich Bescheid.', 'Und wenn nicht? Wie oft ist „nicht normalerweise“?', 'Warum machst du das nicht immer?']),
     ('„Ob das eine Sonderrechnung ist, das sieht man dann schon.“', 'Woran genau? Nenne mir drei Merkmale.', 'Erfahrungswissen wird erst nutzbar, wenn es Merkmale bekommt.',
      ['Woran genau? Nenne mir drei Merkmale.', 'Stimmt, sieht man.', 'Warum steht das nirgends?']),
     ('„Die Freigabe macht die Kollegin.“', 'Nach welchen Kriterien? Was passiert, wenn sie im Urlaub ist?', 'Ein Schritt ohne Regel und ohne Vertretung. Der Urlaub ist die beste Testfrage.',
      ['Dann lassen wir den Schritt weg.', 'Warum macht sie das und nicht du?', 'Nach welchen Kriterien? Was passiert, wenn sie im Urlaub ist?']),
     ('„Das ist eigentlich immer gleich.“', 'Zeig mir die letzten fünf Fälle.', 'Die Unterschiede fallen der erzählenden Person selbst nicht mehr auf. Fünf echte Fälle zeigen sie.',
      ['Perfekt, dann automatisieren wir alles.', 'Zeig mir die letzten fünf Fälle.', 'Bist du dir sicher?']),
     ('„Dann geben wir die Rechnung frei.“', 'Wer prüft? Nach welchen Kriterien? Was passiert bei Unsicherheit?', 'Das Musterbeispiel von Folie 14. Erst diese drei Antworten machen daraus einen Schritt, den man bauen kann.',
      ['Wer prüft? Nach welchen Kriterien? Was passiert bei Unsicherheit?', 'Und dann?', 'Könnte das nicht eine KI machen?']),
     ('„Wie das läuft? Das steht alles im Handbuch.“', 'Nimm den letzten Fall von gestern und erzähl mir Schritt für Schritt, was du gemacht hast.', 'Das Handbuch ist die Version, die sein sollte. Du willst die von gestern.',
      ['Gut, dann lese ich das Handbuch.', 'Wann wurde das Handbuch zuletzt aktualisiert?', 'Nimm den letzten Fall von gestern und erzähl mir Schritt für Schritt, was du gemacht hast.']),
     ('„Schiefgehen? Das kommt eigentlich nie vor.“', 'Wann hat das zuletzt nicht funktioniert?', 'Schritt 4 auf Folie 15. Die Frage setzt voraus, dass es passiert ist, und bringt fast immer eine Geschichte.',
      ['Wann hat das zuletzt nicht funktioniert?', 'Schön, dann planen wir das nicht ein.', 'Wirklich nie?']),
    ])

SPALTEN = dict(
    id='spalten', titel='In welche Spalte?', folie='Folien 15 und 17',
    intro='Mitschreiben in drei Spalten klingt leicht. Sortiere diese Notizen ein.',
    optionen=['Handlung', 'System', 'Entscheidung'],
    karten=[
     ('Ich öffne die PDF-Rechnung aus dem Postfach.', 'Handlung', 'Jemand tut etwas.'),
     ('Der Ordner „Eingang Rechnungen“ im Mailprogramm', 'System', 'Hier liegt oder passiert etwas.'),
     ('Liegt der Betrag über 1.000 Euro?', 'Entscheidung', 'Eine Frage mit mehreren Ausgängen. Hier wird nachgebohrt.'),
     ('Ich trage die Bestellnummer ein.', 'Handlung', 'Wieder jemand, der etwas tut. Nachfrage: wo denn?'),
     ('Die Buchhaltungssoftware', 'System', 'Merke dir auch, wer die Zugänge verwaltet. Das wird der längste Posten im Zeitplan.'),
     ('Passt der Lieferant zur Bestellung?', 'Entscheidung', 'Und sofort nachbohren: Woran erkennst du das?'),
     ('Die Excel-Liste auf dem Desktop einer Kollegin', 'System', 'Auch das ist ein System. Leider. Es kommt trotzdem in den Ist-Prozess.'),
     ('Ich leite die Rechnung an die Fachabteilung weiter.', 'Handlung', 'Und eine Übergabe! Merk sie dir für die Bahnen.'),
    ])

TUERSTEHER = dict(
    id='tuersteher', titel='An der Scope-Tür', folie='Folien 12 und 30',
    intro='Du stehst an der Tür. Reinkommen dürfen Rechnungen unter 1.000 Euro, keine Sonderprojekte, kein Klärungsbedarf. Draußen bleiben: alles über 1.000 Euro, Projektabrechnungen, Rechnungen ohne Bestellbezug, alles mit Klärungsvermerk.',
    optionen=['Rein', 'Raus'],
    karten=[
     ('Büromaterial, 240 Euro, mit Bestellnummer', 'Rein', 'Standardfall. Bitte durchgehen.'),
     ('Druckerwartung, 1.480 Euro, mit Bestellnummer', 'Raus', 'Über 1.000 Euro. Tut uns leid, die Liste ist die Liste.'),
     ('Projektabrechnung Messestand, 900 Euro', 'Raus', 'Der Betrag würde passen, aber Projektabrechnungen stehen ausdrücklich draußen.'),
     ('Kaffeebohnen, 86 Euro, ohne Bestellbezug', 'Raus', 'Auch Kaffee braucht einen Bestellbezug. Das tut weh, ist aber so.'),
     ('Software-Lizenz, 300 Euro, Klärungsvermerk „Betrag prüfen“', 'Raus', 'Klärungsvermerk heißt: bleibt beim Menschen.'),
     ('Reinigungsdienst, 650 Euro, mit Bestellnummer', 'Rein', 'Alles sauber. Im wahrsten Sinne.'),
     ('Beratung, exakt 1.000,00 Euro, mit Bestellnummer', 'Raus', 'Erwischt! Sie steht in keiner Liste: weder „unter 1.000“ noch „über 1.000“. Hier greift der Schutzsatz von Folie 30: Was nicht ausdrücklich dazugehört, bleibt draußen. Du hast gerade eine Lücke im Scope gefunden.'),
     ('Neuer Lieferant, 400 Euro, mit Bestellnummer', 'Rein', 'Laut Liste rein. Und eine prima Frage fürs nächste Gespräch: Soll das bei neuen Lieferanten wirklich so sein?'),
    ])

SPIELE = {s['id']: s for s in (WUNSCH, RUECKFRAGE, SPALTEN, TUERSTEHER)}

RAENGE = [(1.0, 'Chefermittlung', 'Alles aufgeklärt. Die Akte kann geschlossen werden.'),
          (.6, 'Kommissariat', 'Solide Spurensuche. Eine Runde mehr und du leitest das Dezernat.'),
          (0, 'Streifendienst', 'Jede Ermittlung fängt so an. Schau dir die Erklärungen an und versuch es gleich nochmal.')]

# (Satz, Rückfrage, von der Folie?)
BINGO = [
 ('Normalerweise …', 'Und wenn nicht? Wie oft ist „nicht normalerweise“?', True),
 ('Da muss man den Dreh raushaben.', 'Was genau ist der Dreh? Zeig ihn mir an einem echten Fall.', False),
 ('Das macht die Kollegin.', 'Nach welchen Kriterien? Was passiert, wenn sie im Urlaub ist?', True),
 ('Das weiß eigentlich jeder.', 'Woher weiß das eine neue Person am ersten Tag?', False),
 ('Das haben wir schon immer so gemacht.', 'Was würde passieren, wenn ihr es morgen nicht macht?', False),
 ('Das klärt sich dann meistens.', 'Wer klärt es, und wie lange dauert das?', False),
 ('Das sieht man dann schon.', 'Woran genau? Nenne mir drei Merkmale.', True),
 ('Das steht irgendwo.', 'Wo genau? Zeig es mir bitte kurz.', False),
 ('Das ist eigentlich immer gleich.', 'Zeig mir die letzten fünf Fälle.', True),
]
