# Modul 2 · Woche 1 · Learning Hub, Wochenheft und Make-Vorlagen (30.10.2026)

Auftrag von Chris am 30.10.2026: Use Cases identifizieren als Tag 5, alle vier Make-Tage in einem Wochenheft zusammenfassen (Make-Grundlagen Stand 2026), fertige leichte Make-Automationen als JSON zum Import mit vollständiger Erklärung, Wochenübersicht mit je 5 Stichpunkten. Nachtrag im selben Auftrag: **Lernkarten und alle Funktionen aus Modul 1 auch im neuen Modul – wie ein Learning Hub.**

## Was entstanden ist

| Teil | Adresse | Inhalt |
| --- | --- | --- |
| Learning Hub (Tag 5) | `/hefte/{person}/modul-2/tag-5/` (+ Kompatibilität `/tag-24/`) | Start mit Wochenübersicht und Fortschritt, Use-Case-Labor, 9 Make-Vorlagen, Trainieren (1/3/7 Tage), 33 Learnings mit Sitzt/Unklar/Tagesfilter, 40 Lernkarten, 12 Selbsttestfragen, Aufgabengenerator (4 neue Muster), 66 Folien im Viewer, 40 Wörter mit Suche, Wochenheft |
| Wochenheft Web | `/hefte/{person}/modul-2/tag-5/lernheft/` | Teil A Make-Grundlagen (34 Folien), Teil B 9 Vorlagen, Teil C Use Cases (32 Folien, 4 Arbeitsaufträge interaktiv), Teil D Spickzettel, Wochenrückblick, Wörter, Quellen |
| Wochenheft PDF | `pdf/Wochenheft_Modul2_Woche1_Make-und-Use-Cases.pdf` | 62 Seiten A4, Druckfassung mit Ausfülltabellen |
| Make-Vorlagen | `material/modul2-woche1/` | 9 `.blueprint.json`, `START_HIER.txt`, `Make-Vorlagen-Woche1.zip` |
| Folien | `folien/tag-24/` | 01–34 Make (Kopie aus tag-20), 35–66 Use Cases, Gesamt-PDF |
| Tag 1–4 | `/modul-2/tag-{1..4}/` und Lernhefte | Hinweis-Kasten mit Direktlink zur passenden Vorlage, Lernkarten, Selbsttest, Hub |

Interne Kennung des Hubs ist Tag **24** (`kurs.TAGE[24]`, `hub=True`). Dadurch funktionieren Lernkarten, Selbsttest, Learnings, Lernblatt-PDF, Training und Aufgaben mit derselben Technik wie in Modul 1 (`kurs.js`, `lerntraining.js`, `aufgaben.js`). Speicher: `kurs:v1:{person}:t24:*` (Modul-1-Schema) und `kurs:m2w1:{person}:*` (Use-Case-Labor, Vorlagen erledigt).

## Die 9 Vorlagen

A1 Begrüßungs-Mixer · A2 Redaktionsbriefing (Parse JSON) · A3 Freigabe-Ampel (Filter) · A4 Anfragen-Weiche (Router, enthält) · A5 Test-API (HTTP v4, JSONPlaceholder) · A6 Zeitstempel-Übersetzer (formatDate) · A7 Zeitfresser-Rechner (Rechnen + Zahlenfilter) · A8 Use-Case-Steckbrief (11 Felder) · A9 Rechnungs-Regel (UND/ODER, Stufe 2/3).

Alle ohne fremdes Konto, kein Versand, kein Zeitplan. Modul-IDs und Filter-Operatoren wurden am 30.10.2026 mit echten Make-Exporten aus der Make-Community abgeglichen (`util:SetVariable2`, `util:SetVariables`, `util:ComposeTransformer`, `json:ParseJSON`, `builtin:BasicRouter`, `http:MakeRequest` v4, `text:equal`, `text:notequal`, `text:contain:ci`, `number:greaterorequal`; `number:less` nach Make-Namensschema). Import laut help.make.com/blueprints: drei Punkte oben rechts → Import blueprint. **Nicht in einem Make-Konto importiert oder ausgeführt** – Credit-Angaben sind Planwerte. Test-API am 30.10.2026 direkt abgerufen (todos/1 und /2, HTTP 200).

## Use-Case-Folien

Quelle: `Use_Cases_identifizieren_v2 (2).html` (gebündelte Präsentation, Teil 1/5). Einmalig gerendert mit `folien_rendern.py` (lokaler Headless-Chrome, Druckansicht → 32 Seiten). Sprechernotizen ausgewertet. Präzisierungen im Heft: Folie 24 („drei Fragen“ statt vier), Folie 17 (11 Felder als Vorschlag, Arbeitsheft lag nicht vor), Folie 27 (Art. 22 DSGVO „grundsätzlich“, Hochrisiko-Zeitpunkt prüfen), Folie 28 (Art. 50 KI-VO ab 2.8.2026, nicht jeder Marketingtext), Make-Folie 34 (lokale Formate für Menschen erlaubt).

## Bauen und prüfen

```
cd _quellen
python -X utf8 modul2/woche1/build.py        # Vorlagen, Folien tag-24, PDF, Prüfbilder, Klassenbuch
python -X utf8 build.py --web                 # Hub, Wochenheft-Web, Übersichten, Aufgaben-Daten
python -X utf8 modul2/woche1/validate.py      # Server auf :5387; optional Live-URL als Argument
```

`validate.py` prüft je Person in Chrome und WebKit: alle 11 Reiter, Lernkarte, Selbsttest, Training, Tagesfilter, Folienstart 35, Zeitfresser/Steckbrief/Stufen/Treppe, Speichern über Neuladen, Kopieren (Chrome liest die Zwischenablage zurück), 10 Downloads, Deep-Link `#vorlage-a7`, 320/390/1280 px ohne Querscrollen, Leseseite, Banner auf Tag 1–4, Übersicht, keine Konsolenfehler.

## Veröffentlichung 30.10.2026

Release `20261030-woche1-hub`: 227 öffentliche Dateien (166 neu, 61 geändert). 54 ältere Modul-1-Tagesseiten unterscheiden sich nur im Aufgaben-Cachetoken und wurden bewusst nicht veröffentlicht. Vorher Live-Stand gesichert (`public-before.tar.gz`, Image `langdock-hefte:pre-20261030-woche1-hub`). 226 Dateien per HTTPS bytegenau verglichen, Manifest im Container geprüft, alle 227 Host-Dateien geprüft, Container gesund, Serverdateien unverändert. Nachrelease `20261030-woche1-hub-2` (nur `wochenheft.js`: Vorlagen erst laden, wenn sichtbar – keine abgebrochenen Anfragen in Safari/WebKit). Danach `validate.py` gegen https://quint-games.de/hefte: 6 von 6 Läufen (3 Personen × Chrome/WebKit) ohne Fehler. Kein Test auf Carmens Mac selbst, keine Screenreader-Abnahme, kein Make-Import in Teilnehmerkonten.
