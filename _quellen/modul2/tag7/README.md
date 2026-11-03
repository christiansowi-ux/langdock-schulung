# Modul 2 · Tag 7 · Tatort Prozess (03.11.2026)

Auftrag von Chris am 03.11.2026: Dieselbe Lektion wie Tag 6 für den Dienstag, also Lernheft, Learning Hub und Präsenter-Modus zum Deck `KIAutomSpez_2_04_Geschäftsprozesse.pdf`. Dazu: „spaßiger und nicht so trocken, aber vom Schema und Style ist alles gut.“

## Wie es spaßiger wurde

Aufbau und Design sind wie an Tag 6. Neu sind Ton und Mitmachen:

- **Roter Faden „Tatort Prozess“:** Ihr ermittelt, der einzige Verdächtige ist der Prozess (passt zur Regel auf Folie 6: Widersprüche sind kein Vorwurf).
- **Das Tagebuch der Rechnung 0815:** Die Zeiten von Folie 22 als Geschichte. Kim, Alex und Sascha sind erfunden und bewusst geschlechtsneutral benannt.
- **Dialoge:** So klingt Nachfragen in echt (Kapitel B1, B2).
- **Alltagsvergleiche:** Omas Kartoffelsalat, Pizza als SIPOC, der Zettel für die Katzenbetreuung als SOP, das Vorher-Foto als Ist-Prozess.
- **4 Mini-Spiele und Alarmsatz-Bingo** mit Dienstgrad am Ende. Daten in `spiele.py`, die Lernheft, Spiele-Reiter und Präsenter teilen.
- **Werkzeuge mit Persönlichkeit:** Alarmsatz-Melder, Stoppuhr, Absperrband, sich selbst zeichnende Bahnen, „Was wäre, wenn?“, Prüf-Stempel, freundliche Sprüche zu fehlenden Bausteinen.
- **Aufgaben als Rollenspiel:** Die KI spielt die schweigsame Kollegin, die neue Person oder den Fachbereich in Monat drei.

## Was entstanden ist

| Teil | Adresse | Inhalt |
| --- | --- | --- |
| Tagesseite | `/hefte/{person}/modul-2/tag-7/` | Heute (Rückblick auf Montag, Tagebuch), Ermittlungsakte, Spiele, 3 Make-Vorlagen, Demos, Trainieren, 26 Learnings, 38 Lernkarten, 12 Testfragen, Aufgaben (5 neue Muster), 38 Folien, 37 Wörter, Lernheft |
| Lernheft Web | `/hefte/{person}/modul-2/tag-7/lernheft/` | Was bisher geschah, Fall des Tages, 5 Teile entlang der Folienabschnitte, Mitnehmen; jedes Kapitel mit „Einfach gesagt“, Alltagsvergleich und Prüffrage |
| Lernheft PDF | `pdf/Lernheft_Modul2_Tag7_Prozess-verstehen.pdf` | A4 mit Ausfülltabellen, Spielen zum Ankreuzen und Bingo-Karte |
| Präsenter-Modus | `/hefte/praesentation/modul-2/tag-7/` | 4 Montagsfolien + 38 Folien, 134 Begriffe, „Aus der Akte“, Mitmachen auf der Folie |
| Make-Vorlagen | `material/modul2-tag7/` | A12 Zielsatz-Prüfer, A13 Durchlaufzeit-Detektiv, A14 Die Scope-Tür, `START_HIER.txt`, ZIP |
| Folien | `folien/tag-26/` | 01–38, Vorschaubilder, PDF (direkt aus dem gelieferten PDF) |

Interne Kennung ist Tag **26**. Speicher: `kurs:v1:{person}:t26:*` und `kurs:m2w1:{person}:*`. Dieses Präfix teilt sich der Tag mit den Rechnern von Tag 6, deshalb erscheint der Stand von Montag automatisch. Eigene Felder beginnen mit `t7-`.

## Dateien

- `daten.py` Learnings, Karten, Test, Wörter · `inhalt.py` Lernheft und Werkzeuge · `spiele.py` Spiele und Bingo · `vorlagen.py` Make-Vorlagen · `hub.py` Tagesseite, Leseseite, Druck · `aufgaben_t7.py` Aufgabenmuster
- `praesentation_daten.py` Inhalte je Folie · `praesentation.py` baut die Seite · `sprechernotizen.json` Notizen aus der HTML-Fassung des Decks · `plattform/public/assets/praesentation.js` Bühne (gemeinsam mit Tag 6)
- `plattform/public/assets/prozess.js` Werkzeuge und Spiele
- `build.py` Vorlagen und PDF · `validate.py` Browserprüfung

## Datenfluss in der Ermittlungsakte

Mitschrift → „Aus der Mitschrift übernehmen“ → Bahnen → „Aus den Bahnen übernehmen“ → SOP. Bahnen → „Durchlaufzeit übernehmen“ → Erfolgskriterien. Am Ende „Meine Akte herunterladen“ als Markdown.

## Präsenter-Modus

Wie Tag 6, neu in `praesentation.js`: Schritt `fun` („Aus der Akte“) und die Mitmachen-Werkzeuge `spiel`, `bingo`, `bahnen`, `ziel`, `aufwand`. Der Knopf heißt je Folie anders (`liveName`), Taste L. Tag 6 nutzt dieselbe Datei weiter, deshalb nach Änderungen auch `woche2/validate.py` laufen lassen.

## Hinweise zu den Folien

Die Originalfolien bleiben unverändert, die Präzisierungen stehen im Heft und im Präsenter:

1. Folie 9/10: Das „gute“ Ziel auf Folie 9 hat nach Folie 10 noch keinen Zeitpunkt.
2. Folien 12, 22, 31: 4 Minuten je Rechnung gegen 12 Minuten Bearbeitung gesamt. Passt nur, wenn die 4 Minuten allein die Buchhaltung meinen.
3. Folien 21/22: Die Raute auf Folie 22 hat nur einen unbeschrifteten Ausgang, Folie 21 verlangt beschriftete. Als Detektivfrage genutzt.
4. Folie 31: 1,2 Minuten gelten ohne Restprüfzeit. Mit den 0,5 Minuten von Montag wären es rund 1,55 Minuten.
5. Folien 15/17: Die Gegenprobe gilt als wertvollster Schritt, fehlt aber im Arbeitsauftrag. Als Hausaufgabe mitgegeben.
6. Folie 38: Der SIPOC steht bei den Ergebnissen, hat aber keinen eigenen Auftrag. Bei uns Einstieg in Auftrag 02.
7. Folie 2 zählt sechs Blöcke, das Deck von Montag sprach von fünf Teilen.
8. Die Folien verweisen auf „Arbeitsheft 3“. Es lag nicht vor; Werkzeuge und Ausfülltabellen folgen den Folien.

Eigene Annahmen, im Heft gekennzeichnet: Aufteilung der 12 Minuten je Schritt, 8-Stunden-Tag für das Verhältnis 1 zu 200, Befundgrenze 1 zu 50 in A13, die fünf Bonus-Sätze im Bingo, der Hinweis zu Zeitmessung und Betriebsrat auf Folie 33.

## Prüfung und Grenzen

Live seit 03.11.2026 (Release `20261103-tag7-prozess`), Live-Prüfungen bestanden.

`validate.py`: 3 Personen und Präsenter in Chrome und WebKit. Alle Reiter, Spiele bis zur Auswertung, Bingo, Alarmsatz-Melder, Bahnen mit Folienbeispiel und Skizze, Datenfluss, Speicherung über Neuladen, Karte in jedem Begriffsschritt innerhalb der Folie, 320/390/1280 px.

Make: Schema und Module mit Makes eigener Prüfung validiert. **Nicht in einem Make-Konto importiert oder ausgeführt.** Nicht direkt auf Carmens Mac getestet. Die Sprechernotizen stehen technisch in der Seite; wer den Link hat, kann sie öffnen.
