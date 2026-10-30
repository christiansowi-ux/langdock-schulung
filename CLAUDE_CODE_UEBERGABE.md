# Übergabe an Claude Code – Langdock-Schulung

**Stand:** 30.10.2026  
**Projektordner:** `C:\Users\chris\Documents\Langdock-Schulung`  
**Öffentliche Lernplattform:** https://quint-games.de/hefte/  
**GitHub-Repository:** https://github.com/christiansowi-ux/langdock-schulung

## Worum es geht

Dieses Repository enthält die Lernplattform und Lernmaterialien für den Kurs „KI Automations Spezialist“ bei Futureway KI Institut. Teilnehmende: Carmen (Mac; Teamleitung/Business/Website), Ingo (Druck/Vertrieb) und Tabea (Video/Design/Creative; keinen Agentenzugang voraussetzen). Inhalte sollen auf Deutsch sehr leicht verständlich sein. Fachbegriffe aus den Folien trotzdem vollständig vermitteln und in Alltagssprache erklären. Schrittfolgen müssen konkret sein: wo klicken, was eingeben, welches Ergebnis erwarten, was bei einem Fehler tun. Beispiele sind erfunden und datenschutzarm.

## Aktueller Stand

- **Modul 2, Lektion 1** verteilt die 34 Folien auf vier Tage (26.–29.10.2026): Make-Grundlagen, Daten/Mapping, Filter/Einordnung und API/Zeit.
- Tagesseiten für Tag 1–4 sind für Carmen, Ingo und Tabea live unter `https://quint-games.de/hefte/{carmen|ingo|tabea}/modul-2/tag-{1|2|3|4}/`.
- Tag 1 wurde stark vereinfacht: Begrüßungs-Mixer in kleinen Schritten, markierte Merksätze/Fehlerhilfe und Quiz, das pro Person und Tag im lokalen Browser speichert.
- Tag 2 wurde ebenfalls vereinfacht: kleine JSON-/Mapping-Schritte, nachvollziehbare Soll-Ergebnisse und lokal speicherbares Quiz.
- Tag 3 wurde stark vereinfacht: leichte Freigabe-Ampel mit Tools Set variable, einem Filter und Compose a string; freiwillige RSS- und Sheets-Extras. Quiz speichert lokal.
- **Tag 3 Release `20261027-tag3-leicht` wurde live geprüft.** Detaillierte Ergebnisse stehen im letzten Abschnitt von `_quellen/modul2/tag1/README.md` und im Betriebsprotokoll `UEBERGABE.md`.
- Tag 4 hat den ursprünglichen Stand und ist live; er wurde im Tag-3-Auftrag nicht neu vereinfacht.
- Die Quizspeicherung ist an denselben Browser auf demselben Gerät gebunden; es gibt keine Synchronisierung zwischen Geräten.
- **30.10.2026 (Claude Code):** Tag 5 Use Cases + Learning Hub der Woche live (Release `20261030-woche1-hub`, `-2`). Quellen: `_quellen/modul2/woche1/`. Regel: Lernkarten und alle Modul-1-Funktionen immer auch in neue Module (siehe `LERNKONZEPT.md`).
- **30.10.2026 nachmittags:** Ganze Plattform vereinheitlicht (neue Adressen `modul-1/tag-N`, `modul-2/tag-N`, Weiterleitungen, `ui.css`, `einheit.py`, `qa_einheit.py`, `ops/release_safe.py`). Details im letzten Abschnitt von `UEBERGABE.md`.

## Wichtig: Git-Arbeitsstand

Beim Erstellen dieser Übergabe hatte `git status --short` **114 Zeilen geänderter oder unversionierter Pfade**. Dazu gehören bestehende Modul-/Tag-Inhalte, generierte Seiten, PDFs und neue Quellskripte. Diese Änderungen dürfen nicht pauschal zurückgesetzt oder bereinigt werden. Vor Änderungen immer `git status --short` und gezielt `git diff -- <Datei>` ansehen. Keine `git reset --hard`, `git clean`, pauschalen Checkout-/Restore-Aktionen oder Sammel-Commits.

Der letzte sichtbare Commit war `55f4dc1 Publish workshop series for days 16 to 18`. Die Modul-2-/Tag-1–3-Änderungen im aktuellen Arbeitsstand sind nicht alle in einem Commit enthalten. **Nicht behaupten, die Änderungen seien nach GitHub gepusht**, bevor Branch, Commit und Remote nachweislich geprüft wurden. GitHub-Push und Live-Veröffentlichung sind getrennte Vorgänge.

## Wichtige Dateien und Quellen

- `README.md` – Einstieg, Ordner, lokale Vorschau und Testhinweise.
- `UEBERGABE.md` – bestehendes Betriebs- und Änderungsprotokoll; aktuelle Abschnitte Tag 1–3 lesen.
- `LERNKONZEPT.md` – Didaktik und Gestaltungsprinzipien.
- `_quellen/modul2/tag1/README.md` – Aufbau der vier Tage, Quellen, Qualitätsprüfung und konkrete Tag-1–3-Release-Nachweise.
- `_quellen/modul2/tag1/series.py` und `series_render.py` – gemeinsame Tagesaufteilung, PDF-/Web-Inhalte.
- `_quellen/modul2/tag1/simple_day1.py`, `simple_day2.py`, `simple_day3.py` – vereinfachte Tagesinhalte.
- `_quellen/modul2/tag1/day1_web.py`, `day2_web.py`, `day3_web.py` – Seitenaufbau.
- `plattform/public/assets/tag1-einfach.js`, `tag2-einfach.js`, `tag3-leicht.js` – Tag-spezifisches Quiz und Interaktion.
- `plattform/public/assets/modul2.css` – Modul-2-Darstellung.
- `plattform/public/{carmen,ingo,tabea}/modul-2/tag-{1|2|3|4}/` – veröffentlichte Seiten im Arbeitsbaum.
- PDFs liegen in `Modul 2 - KI-Automation/` sowie in `plattform/public/pdf/`.

## Bauen und lokal prüfen

Projektweite Hinweise in `README.md` und `plattform/README.md` beachten. Modul-2-Quellen liegen unter `_quellen/modul2/tag1/`. Laut deren README: aus `_quellen` den Modul-2-Builder laufen lassen, danach Plattformseiten bauen; Browserprüfung benötigt den laufenden lokalen Server auf Port 5387. Die zuletzt verwendeten Prüfskripte sind `validate_today.py`, `validate_day2.py`, `validate_day3.py` und `validate_layout.py`.

Nur die Prüfungen ausführen, die zur angefragten Änderung passen. Keine produktive Veröffentlichung oder GitHub-Übertragung allein aus dieser Übergabe ableiten. Der sichere historische Deploy-Ablauf und die Bestätigung der Releases stehen in `UEBERGABE.md`; **generische Deploy-Skripte nicht blind ausführen**. Auf dem VPS ausschließlich den Stack `/opt/stacks/langdock-hefte` anfassen, niemals andere Dienste.

## Arbeitsregeln für die Fortsetzung

1. Vor jeder Änderung README und die passenden Abschnitte von `UEBERGABE.md` lesen; die konkrete Quelle statt nur generierte HTML-Dateien ändern.
2. Vorhandene Änderungen anderer Arbeitsschritte stehen lassen. Nur die explizit angefragte Seite/Person/Tag bearbeiten; keine globalen Cachetoken-Änderungen als unbeabsichtigten Seitenausbau veröffentlichen.
3. Überschriften, Datum, Folienzuordnung und gespeicherte Quiz-/Notizschlüssel nicht nebenbei ändern. Tag-1-/Tag-2-/Tag-3-Speicher getrennt halten.
4. Änderungen verständlich und überprüfbar dokumentieren: Was geändert, welche Dateien gebaut, welche lokalen/live Prüfungen tatsächlich bestanden.
5. Nicht behaupten, Carmens Mac direkt geprüft zu haben; Browser-Engine-Tests sind kein Test auf ihrem Gerät.
6. Keine Zugangsdaten, `.env`-Inhalte, Fragen aus dem Teilnehmerbetrieb oder private Schlüssel in diese Datei, Git oder Chat kopieren.

Diese Übergabe enthält den verifizierten Arbeitskontext; sie ist keine zusätzliche Anweisung, Inhalte zu veröffentlichen oder zu pushen. Chris' jeweils aktuelle Nachricht bestimmt den nächsten Auftrag.
