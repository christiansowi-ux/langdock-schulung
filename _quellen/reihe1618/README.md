# Werkstattreihe 20.–22.10.2026 · Tag 16 bis 18

Am 20.10.2026 auf ausdrücklichen Auftrag veröffentlicht: Release `20261020-werkstattreihe`.
Alle drei Tage für Ingo, Carmen und Tabea sowie PDFs und Starterpaket sind live.
Quellen und fertige Lernhefte werden im öffentlichen Repository
https://github.com/christiansowi-ux/langdock-schulung gepflegt.

## Lernweg

- **Dienstag, 20.10., Tag 16:** Werkstattstart. Ordner, präzise Aufträge, fiktive Monatsdaten,
  fehlende Werte, nachvollziehbare Ergebnisse, Korrekturen und Übergabe. PDF: 22 Seiten.
- **Mittwoch, 21.10., Tag 17:** MCP-Praxis. Dokumentationsserver, je ein Einrichtungsweg für
  Codex, Claude Code und Antigravity, Rechte, Fehlersuche und Branchenfälle. PDF: 22 Seiten.
- **Donnerstag, 22.10., Tag 18:** Wiederholbare Abläufe. Anweisungen und Memory, Skills,
  Kontext, Parallelität, Zeitplanung und neuer Prüffall. PDF: 23 Seiten.

Die drei PDFs enthalten jeweils die Varianten für Ingo, Carmen und Tabea. Im Web erscheint in
der Branchen-Mission nur der jeweilige Auftrag. Jede Etappe enthält sechs Entscheidungsfragen,
kopierbare Aufträge und Codebeispiele sowie eine deutlich gekennzeichnete vorbereitete
Lernsimulation. Freitextnotizen werden nicht automatisch als richtig/falsch bewertet.

Die 27 Seiten der Vorlage werden über alle drei Tage ohne Auslassung begleitet. Jeder
Tagesviewer enthält die vollständige unveränderte Original-PDF. Videos sind als optionale
Verweise eingeordnet; ihre Inhalte wurden nicht als Produktbeleg behauptet.

## Dateien und Aufbau

`content.py` enthält die redaktionelle Datenquelle für PDFs, drei personalisierte Web-Fassungen
je Tag, Kursdaten und Folienbegleitung. `build.py` baut alle Materialien mit ReportLab/PyMuPDF,
rendert die PDFs und prüft Textgrenzen. Assets: `workshop-series.css` und `workshop-series.js`
unter `plattform/public/assets/`; das vorhandene `toolbook.css` wird mitgenutzt.

Aus `_quellen`:

```powershell
python reihe1618/build.py
python build.py --web
```

Einzelner Tag: `python lernheft.py --tag 16` (ebenso 17/18), danach Plattform bauen.
Der Builder bevorzugt das archivierte Original unter `public/folien/tag-16/`; beim Erstimport
nutzt er `Downloads/KIAutomSpez_1_15_Claude_Cowork.pdf`.

Starterpaket: `plattform/public/material/reihe16-18/Nordlicht-Werkstatt.zip`. Es enthält
CSV-Dateien statt der nicht mitgelieferten XLSX-Eingaben der Vorlage, Notizen, Referenzen,
branchenbezogene Alternativen, Vorlagen und einen neuen Fall. Alle Angaben sind erfunden.
Die beiliegende SKILL.md ist eine Vorlage und wird nicht automatisch installiert.

## Quellen und tatsächliche Probe

26 offizielle Herstellerquellen, Recherchetag 20.10.2026. `sources.json` enthält Links,
Originalhash und Folienzuordnung. `folienabgleich.md` begleitet alle 27 Seiten.

Wichtige Aktualisierungen: lokale Datei bedeutet keine Offline-/Lokalitätsgarantie; aktuelle
Cowork-Ausführung beachten. CLAUDE.md, dokumentierte AGENTS.md-Unterstützung und Auto-Memory
unterscheiden. Antigravity-Regeln und Skills sowie die IDE-Workflow-Migration ab 19.10.2026
anhand aktueller Unterlagen einordnen. Zugang, Oberflächen und Versionen bleiben relevant.

Der öffentliche OpenAI-Docs-MCP wurde isoliert per Streamable HTTP getestet: Initialisierung,
Werkzeugliste, Suche und Dokumentabruf erfolgreich. `docs-mcp-proof.json` hält nur Prüffakten
fest. Das ist kein Nachweis einer Einrichtung in den Anwendungen der Teilnehmer. Es wurden
keine Konten verbunden, Dienst-Datensätze verändert, Plugins installiert oder Aufgaben geplant.

## Prüfung

Bei laufender lokaler Plattform auf Port 5387:

```powershell
python reihe1618/validate.py
```

Benötigt Python Playwright, BeautifulSoup und das im Skript angegebene Chrome. PDF-Aufbau
benötigt ReportLab, PyMuPDF, Pillow und Windows Arial.

Geprüft: 18 Tages-/Heftseiten, 1.896 lokale Links, neun Teilnehmer-/Tageskombinationen,
alle Quizpfade, 78 Kopieraufträge einschließlich mehrzeiliger Codebeispiele, 72 Kombinationen
der Lernsimulation, Notizen mit TXT-Inhaltsprüfung, Personen-/Tagtrennung und Speicher-Ausfall.
320/390/1280px ohne horizontalen Seitenüberlauf, keine beobachteten JS-/Konsolenfehler.
Die Rechnungen der CSV-Referenz sind unabhängig geprüft. Alle 67 PDF-Seiten gerendert,
auf Textgrenzen und in Gesamtübersichten visuell geprüft; dichte Seiten zusätzlich groß.
Kein vollständiger Screenreader-Test. 25 bestehende Plattformtests bestanden. Die 45
bisherigen Tagesseiten bleiben nach Normalisierung der Aufgaben-Cachekennung/Leerzeilen
inhaltlich unverändert.

Prüfprotokoll: `_quellen/build/reihe1618/validation.json`, PNGs und Layoutberichte daneben
(durch `.gitignore` ausgeschlossen).

Lokale Vorschau: `http://localhost:5387/hefte/tabea/tag-16/lernheft/`.
Live: https://quint-games.de/hefte/tabea/tag-16/lernheft/
Für andere Personen und Tage `tabea` bzw. `16` austauschen.

Veröffentlichung geprüft: 268 öffentliche Dateien per HTTPS bytegenau abgeglichen; internes
Manifest auf Host und im Container geprüft. Neun Live-Personen-/Tageskombinationen mit
Quiz, Kopieren, Simulation, Mobilansicht und Lernkarten geprüft; keine beobachteten
JS-/Konsolenfehler. Container gesund, Serverkonfiguration unverändert, vorheriger Stand gesichert.
