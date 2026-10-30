# Freitag 23.10.2026 · Tag 19 und separates Bonusheft

Am 23.10.2026 auf ausdrücklichen Auftrag live veröffentlicht und geprüft.
Release: `20261023-freitag-design`. Der GitHub-Stand wurde bei diesem Live-Auftrag nicht verändert.

## Umfang

- Freitagsheft: 26 Seiten. Genau zehn Design-Stationen und zehn reine Make-Lesestationen, danach sechs Seiten Folienabgleich/Quellen. Der 50/50-Anteil gilt für den Lernkern. Keine Make-Übungen, Quizfragen, Simulationen, Kontoeinrichtung oder Testläufe. Praktischer Make-Start Montag, 26.10.2026.
- Bonusheft: 28 Seiten, fünf ausgearbeitete Anwendungsfälle plus genau zwanzig zusätzliche Prompts, jeweils mit Einsatzumgebung, Prüfung und Korrekturhilfe. Zeitbudgets stehen für erste prüfbare Entwürfe. Keine 100-Prozent-Erfolgsgarantie und keine behaupteten Tests in allen KI-Produkten.
- Klassenbuch: `klassenbuch-19-23-10-2026.md`, thematisch an Lektion 14–16 orientiert; aktuelle Ergänzungen getrennt eingeordnet.

## Quellen und Original

20 Originalfolien der Juli-Vorlage vollständig und unverändert unter `plattform/public/folien/tag-19/`. Alle Seiten im Anhang eingeordnet. `sources.json` enthält SHA256 und zehn offizielle Quellen, Recherchetag 23.10.2026.

Die aktuelle Claude-Hilfe unterscheidet Design in Chats/Artifacts von gesonderten Designsystem-Funktionen. Zugang und die geplante Schließung der bisherigen separaten Oberfläche werden aktualisiert. Der Bereinigungsprompt für fremde Markenregeln wird nicht als Rechtefreigabe übernommen. Optionale Videos bleiben optionale Verweise.

## Aufbau

Aus `_quellen`:

```powershell
python tag19/build.py
python build.py --web
```

Alternativ: `python lernheft.py --tag 19`, danach Web-Aufbau.

`content.py` enthält den Lernkern und den Folienabgleich; `bonus_content.py` die fünf Fälle und zwanzig zusätzlichen Prompts. `build.py` erzeugt PDFs, Web-Hefte und Originalfolienbilder. Eigene Tagesseite verhindert, dass Make als Übungs-, Quiz- oder Demotag erscheint. `friday19.js` bietet ausschließlich Kopieren und die mobile Inhaltsnavigation. Bisherige Werkstatt-Simulationen bleiben unverändert.

Lokale Vorschau:

- `http://localhost:5387/hefte/tabea/tag-19/`
- `http://localhost:5387/hefte/tabea/tag-19/lernheft/`
- `http://localhost:5387/hefte/tabea/tag-19/bonus/`

Für Ingo und Carmen den Namen im Pfad austauschen. Prüfberichte und gerenderte Seiten stehen unter `_quellen/build/tag19/` und sind nicht versioniert.

## Tatsächlich geprüft

Alle 54 PDF-Seiten gerendert, Textgrenzen geprüft und in Gesamtübersichten visuell kontrolliert; dichte Seiten zusätzlich einzeln angesehen. Keine Verkleinerung der vorgesehenen Schrift nötig. Neun Web-Seiten, 393 lokale Links und 153 Kopieraktionen für Ingo/Carmen/Tabea geprüft, einschließlich verweigerter Zwischenablage. 320/390/1280px ohne horizontalen Seitenüberlauf, keine beobachteten JS-/Konsolenfehler. Original-PDF bytegleich; beide PDF-Downloads bytegleich. 54 vorhandene Tagesseiten bleiben nach Normalisierung der Aufgaben-Cachekennung und Leerzeichen inhaltlich unverändert.

25 bestehende Node-Plattformtests bestanden. Auch die neue Tagesübersicht ist bei 320/390/1280px ohne horizontalen Seitenüberlauf geprüft. Kein vollständiger Screenreader-Test.

## Live-Prüfung

Alle neun Tages-/Heft-/Bonusseiten für Ingo, Carmen und Tabea im Browser geprüft, sechs repräsentative Kopieraktionen erfolgreich, 320/390/1280px ohne horizontalen Überlauf und keine beobachteten JS-/Konsolenfehler. Make-Bereich ohne interaktive Übungssteuerelemente. 121 öffentliche Dateien einschließlich beider PDFs per HTTPS bytegenau geprüft; internes Manifest im Container sowie alle 122 Zieldateien auf dem Host geprüft. Container gesund, Serverdateien unverändert, vorheriges Public-Verzeichnis und Docker-Image gesichert.

Live-Beispiel: https://quint-games.de/hefte/tabea/tag-19/
