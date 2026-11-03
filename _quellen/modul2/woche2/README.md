# Modul 2 · Tag 6 · Bewerten und rechnen, mit Präsenter-Modus (02.11.2026)

Auftrag von Chris am 02.11.2026: neue Folien erklären, das Lernheft „immer verständlich erklären“, Freitags-Use-Cases am Anfang als Erinnerung wiederholen, und aus den Folien einen Präsenter-Modus bauen, mit Erklärungen direkt an den Begriffen auf der Folie. Stehende Regel: jede Lektion ist ein Learning Hub mit Lernkarten und allen Modul-1-Funktionen.

## Was entstanden ist

| Teil | Adresse | Inhalt |
| --- | --- | --- |
| Tagesseite | `/hefte/{person}/modul-2/tag-6/` | Heute (mit Freitags-Erinnerung), Rechen-Labor, 2 Make-Vorlagen, Demos, Trainieren, 22 Learnings, 26 Lernkarten, 10 Testfragen, Aufgaben (5 neue Muster), 29 Folien, 30 Wörter, Lernheft |
| Lernheft Web | `/hefte/{person}/modul-2/tag-6/lernheft/` | Erinnerung, Plan, Bewerten, Priorisieren, Rechnen, Entscheiden, Mitnehmen; jedes Kapitel mit „Einfach gesagt“, Alltagsvergleich und Prüffrage |
| Lernheft PDF | `pdf/Lernheft_Modul2_Tag6_Bewerten-und-Rechnen.pdf` | 35 Seiten A4 mit Ausfülltabellen |
| Präsenter-Modus | `/hefte/praesentation/modul-2/tag-6/` | 4 Freitagsfolien + 29 Folien, 86 Begriffe direkt auf der Folie |
| Make-Vorlagen | `material/modul2-woche2/` | A10 Scoring-Rechner, A11 Business-Case-Rechner, `START_HIER.txt`, ZIP |
| Folien | `folien/tag-25/` | 01–29, Vorschaubilder, PDF |

Interne Kennung ist Tag **25**. Speicher: `kurs:v1:{person}:t25:*` und `kurs:m2w1:{person}:*`; dieses Präfix teilt sich der Tag mit dem Use-Case-Labor von Tag 5, deshalb erscheinen die Freitags-Steckbriefe automatisch in der Erinnerung.

## Dateien

- `daten.py` Learnings, Karten, Test, Wörter · `inhalt.py` Lernheft und Werkzeuge · `vorlagen.py` Make-Vorlagen · `hub.py` Tagesseite, Leseseite, Druck · `aufgaben_w2.py` Aufgabenmuster
- `praesentation_daten.py` Inhalte je Folie · `praesentation.py` baut die Seite · `sprechernotizen.json` Notizen aus der Originalpräsentation · `plattform/public/assets/praesentation.js` Bühne
- `plattform/public/assets/bewerten.js` Rechner im Rechen-Labor
- `build.py` Vorlagen und PDF · `validate.py` Browserprüfung

## Präsenter-Modus

Der Bau sucht jeden Begriff im Folien-PDF (`page.search_for`) und legt die Markierung exakt über das Wort. **Findet er einen Begriff nicht, bricht der Bau ab.** Bei einer neuen Folienfassung also nur die Texte in `praesentation_daten.py` anpassen. Eigenes Layout ohne Kopf und Fuß: der Marker `eigenes-layout` nimmt die Seite aus `einheit.vereinheitlichen` und aus der Rahmenprüfung.

Schrittfolge je Folie: Folie, „Einfach gesagt“, Begriffe mit Scheinwerfer, ggf. „Wichtig“, „Frage an die Runde“. Tasten: → Leertaste Bild↓ weiter, ← zurück, ↓↑ ganze Folie, E Erklärungen, L Live-Rechner, G Übersicht, R Referentenansicht (`?ansicht=referent`, synchron per BroadcastChannel), F Vollbild. Auf dem Handy steht die Erklärung unter der Folie, Wischen blättert.

## Rechnungen und Hinweise zu den Folien

Die Rechnungen der Folien stimmen: 1.485 €, 1.185 €, rund 10 Monate, 18,5 %, 255,5 %, 22.800 €. Eigene Szenarien: konservativ 50 %/400 € ergibt 635 €, rund 19 Monate, −36,5 %. Kipp-Punkt für 24 Monate: rund 38 %.

Präzisierungen stehen als Hinweis im Heft und im Präsenter, die Originalfolien bleiben unverändert:

1. Folie 9 nennt vier Ausschlusskriterien, am Freitag waren es fünf (fehlt: Prozess wird gerade umgestellt).
2. Folien 12/14 sagen „Aufwand = Komplexität + Risiko“, bewertet wird aber Einfachheit/Risikoarmut (hoch = gut). Deshalb: Aufwand = 12 − Einfachheit − Risikoarmut. Die Folien setzen keine Grenze; unser Vorschlag: Wert ab 7 hoch, Aufwand bis 5 gering.
3. Folie 23: Die Faustregel gilt nicht mit den Beispielkosten von Folie 19 (15 Std. ergeben rund 32 Monate). Sie ist nur ein Schnelltest.
4. Folie 17 nennt verbleibende Prüfung als laufende Kosten, Folie 19 zieht die Restprüfzeit schon beim Nutzen ab. Nicht doppelt zählen.
5. Die Folien verweisen auf „Arbeitsheft 2“. Es lag nicht vor; Rechner und Ausfülltabellen folgen den Folien.

## Prüfung und Grenzen

Live seit 02.11.2026 über einen versehentlich ausgelösten Release (Name `--help`), Details in `UEBERGABE.md`. Live-Prüfungen bestanden.

`validate.py`: 3 Personen und Präsenter in Chrome und WebKit, Karte in jedem Begriffsschritt innerhalb der Folie, Live-Rechner, Referentenansicht, 320/390/1280 px. `qa_einheit.py`, `woche1/validate.py` und Node-Tests laufen weiter durch.

Make: Schema und Module mit Makes eigener Prüfung validiert. **Nicht in einem Make-Konto importiert oder ausgeführt.** Nicht direkt auf Carmens Mac getestet. Die Sprechernotizen stehen technisch in der Seite; wer den Link hat, kann sie öffnen.
