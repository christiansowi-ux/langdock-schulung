# Tag 15 · KI-Werkzeuge im Vergleich

Stand 19.10.2026. Veröffentlicht und geprüft: Release `20261019-ki-werkzeuge`. Live: https://quint-games.de/hefte/tabea/tag-15/lernheft/#k17 .

- `content.py`: einheitliche Daten für das 41-seitige PDF und die drei Web-Hefte. 28 Folienbegleitungen, sechs Branchen-Missionen, sechs Erweiterungen, acht Quizfragen und 24 offizielle Quellen.
- `build_material.py`: ReportLab-PDF, Originalfolien und Vorschaubilder, Web-Heft, Quellenprotokoll und PDF-Seitenprüfung. Bevorzugt die eingebundene Originaldatei; Downloads dient als Erstimport.
- `sources.json`: Herstellerquellen mit Recherchetag und Original-Hash. Keine eigene Installation oder Leistungsprüfung der angebotenen Produkte behauptet.
- `folienabgleich.md`: jede Originalfolie einzeln mit Erklärung, Beispiel, Frage, Antwort und Präzisierung.
- `validate.py`: Struktur und lokale Links, alle Quizpfade, alle 17 Copy-Aufträge pro Profil, Notiz mit Download, Profiltrennung und Speicher-Ausfall sowie 320/390/1280-Pixel-Ansichten.

Aus `_quellen`:

```powershell
python tag15/build_material.py
python build.py --web
```

`python lernheft.py --tag 15` verwendet ebenfalls den ReportLab-Aufbau. Danach den Plattformaufbau ausführen. Die Web-Assets liegen wie die übrigen Plattformskripte unter `plattform/public/assets/toolbook.css` und `toolbook.js`.

Lokal prüfen: Plattformserver auf Port 5387 starten, danach `python tag15/validate.py`. Browserprüfungen verwenden das installierte Chrome headless und benötigen Python Playwright und BeautifulSoup. PDF benötigt ReportLab, PyMuPDF und Pillow sowie Windows Arial.

Lokale Vorschau: `http://localhost:5387/hefte/tabea/tag-15/lernheft/#k17`. Für andere Profile `tabea` gegen `ingo` oder `carmen` austauschen. Die vorhandene Tagesansicht enthält zusätzlich 28 einfache Erklärungen, Originalfolien, Learnings, Karten, Quiz und zeitversetztes Erinnern. Das generische Prompt-Studio bleibt vorhanden; die neuen Branchen-Missionen stehen im Lernheft. Es wurden keine fremden Konten verbunden und keine Dienste installiert.

Chris hat am 19.10.2026 mit „mach alles live“ die Veröffentlichung beauftragt. Tag 15 ist live. Bei späteren Änderungen aktuellen Live-Ausgangsstand und Servercode erneut prüfen. Veröffentlichungsprotokoll: UEBERGABE.md und im Chat-Arbeitsverzeichnis work/toolvergleich/release/.
