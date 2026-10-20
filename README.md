# Langdock-Schulung · interaktive Lernplattform

Schulungsmaterial und Quellcode der Lernplattform unter **https://quint-games.de/hefte/**.
Stand: 20.10.2026, einschließlich der veröffentlichten Lernreihe Tag 16–18 für den 20.–22.10.2026.

Die Plattform bietet Lernhefte, Originalfolien, einfache Erklärungen, Lernkarten, Selbsttests,
Erinnerungsübungen und interaktive Demos für Druck/Vertrieb, Team/Business/Website und Video/Design.
Die Übungen verwenden erfundene Angaben. Quellen und fachliche Präzisierungen stehen in den Materialien.

## Verzeichnisse

- `_quellen/`: redaktionelle Inhalte und Python-Generatoren für Hefte und Plattform.
- `plattform/`: Node-Server, Docker-Dateien, Browser-Code, Tests und gebaute öffentliche Inhalte.
- `Tag …/`: fertige Lernhefte als PDF.
- `LERNKONZEPT.md`: didaktisches Konzept.
- `UEBERGABE.md`: Projektverlauf, Betriebs- und Veröffentlichungsprotokoll.

Originalfolien und benötigte öffentliche Materialien liegen in `plattform/public/` und sind mit versioniert.
Der aktuelle Stand enthält 18 Kurstage. Fertige öffentliche Dateien erlauben einen Start ohne vorherigen PDF-Build.

Die neue Werkstattreihe verbindet Claude Code, Codex und Antigravity: Werkstattstart, MCP-Praxis und effiziente Abläufe. Aufbau und Quellen: [`_quellen/reihe1618/README.md`](_quellen/reihe1618/README.md).

## Lokal starten

Voraussetzungen: Node.js ab 22; für PDF-Exporte zusätzlich ein unterstütztes Chrome/Chromium.

```powershell
cd plattform
npm ci
# Optional: .env.example nach .env kopieren und eigene Werte setzen.
$env:PORT='5387'
npm start
```

Danach **http://localhost:5387/hefte/** öffnen. Ohne eigene Dozenten-Zugangsdaten bleibt die
entsprechende Verwaltungsfunktion deaktiviert. Persönliche Laufzeitdaten und lokale `.env`-Dateien
werden nicht versioniert. Keine Produktionsschlüssel für eine lokale Vorschau übernehmen.

## Inhalte neu bauen

Python-Generatoren verwenden unter anderem PyMuPDF, Pillow, ReportLab, BeautifulSoup und je nach
Heft zusätzliche PDF-/Browser-Werkzeuge. Manche PDF-Builder erwarten Windows Arial oder eigene
Browser-Abhängigkeiten. Hinweise pro Tag beachten; der Web-Aufbau benötigt keinen neuen PDF-Export.

```powershell
cd _quellen
python build.py --web
```

Tag 15 separat bauen:

```powershell
python tag15/build_material.py
python build.py --web
```

Weitere Details: [`_quellen/tag15/README.md`](_quellen/tag15/README.md) und
[`plattform/README.md`](plattform/README.md).

## Prüfungen

```powershell
cd plattform
node --test ops/lerntraining.test.cjs ops/demos.test.cjs ops/privacy.test.cjs
```

Die Browserprüfung für Tag 15 benötigt eine laufende lokale Plattform auf Port 5387,
Python Playwright, BeautifulSoup und das im Prüfskript angegebene Chrome:

```powershell
cd _quellen
python tag15/validate.py
```

## Veröffentlichung und Daten

GitHub-Push und Live-Veröffentlichung sind getrennte Vorgänge. Dieses Repository enthält keinen
automatischen Deployment-Workflow. Vor einer Veröffentlichung den aktuellen Serverstand prüfen,
sichern und nur das vorgesehene Schulungsprojekt aktualisieren. Der tatsächlich verwendete
Release- und Sicherungsweg steht in `UEBERGABE.md`; ältere generische Deploy-Skripte nicht blind ausführen.

Teilnehmerfragen unter `plattform/data/`, `.env`, private Schlüssel, Abhängigkeiten und temporäre
Prüfdateien sind ausgeschlossen. Die früheren Arbeitsplatzpfade in Betriebsnotizen sind historische
Angaben und müssen auf einem anderen Rechner angepasst werden.

Die enthaltenen Fremdmaterialien und Folien behalten ihre jeweiligen Rechte. Dieses Repository
erteilt dafür keine zusätzliche öffentliche Weiterverbreitungslizenz.
