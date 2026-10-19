# Lernplattform – quint-games.de/hefte

> Aktueller und vollständiger: **`../UEBERGABE.md`** (Stand, Ablauf je Kurstag, Lernhefte, Aufgabengenerator, Server).

Live: **https://quint-games.de/hefte/** (noindex). Carmen, Ingo und Tabea wählen ihren Namen und finden je Kurstag:
Learnings (kurz + „Nochmal erklärt“ + Folienbild), Lernkarten, Selbsttest, alle Folien (Viewer, Videos), Wörter des Tages
und das Arbeitsheft zum Ausfüllen (Learnings am Heftende, einzeln als PDF). Überall gibt es „Unklar?“ – die Meldung
landet bei der Schulungsleitung (Glocke oben auf jeder Seite, sobald angemeldet; Seite `/hefte/dozent/`).

Personen und Profile: Carmen = B (Teamleitung, Business & Website, Mac), Ingo = A (Druck & Vertrieb), Tabea = C (Video, Design & Creative, ohne Agents).

## Aufbau
- Inhalte: `../_quellen/kurs.py` (Personen, Tage, Learnings, Wörter, Lernkarten, Selbsttest), `../_quellen/folien.json`
  (Folienanzahl + Links, aus den Folien-PDFs), Hefte wie gewohnt in `../_quellen/` (Tag 1), `tag2/`, `tag3/`.
  Ab Tag 3 **ein** Heft für alle (`tag3/heft.html`, 95 % gleich) + je Person `tag3/zusatz_<person>.html` mit den freiwilligen
  Zusatzaufgaben (Blöcke `<!-- Z1 -->` … `<!-- Z3 -->`, je `<h3>`, `<span class="time">`, `<p class="goal">`).
- `python ../_quellen/build.py --tag N` baut die Druck-PDFs, `python ../_quellen/build.py --web` (→ `_quellen/plattform.py`)
  schreibt `public/`: `index.html` (Personenwahl), `<person>/`, `<person>/tag-N/`, `<person>/tag-N/heft/`,
  `<person>/tag-N/lernblatt/`, `<person>/lernblatt/`, `dozent/`, `pdf/`, `manifest.json`.
- Von Hand gepflegt: `public/assets/` – `app.js/app.css` (Unklar-Dialog, Glocke, Learnings-PDF, auf allen Seiten),
  `kurs.js/kurs.css` (Plattform-Seiten), `dozent.js`, `hefte.js/web.css` (Heft ausfüllen), `fonts/`.
  Folienbilder `public/folien/tag-N/` (NN.jpg 1600 px, tNN.jpg Vorschau, Folien_TagN.pdf).
- Die Tag-3-Hefte vom Vormittag (30.09.) liegen unverändert unter `public/tag-3/<slug>/` – dort hängen gespeicherte Antworten.
- `server.mjs`: statisch + `POST /api/pdf` (Heft mit Antworten oder Lernblatt mit Auswahl, Chromium) + `/api/fragen`
  (melden, Status abfragen per unratbarer ID) + `/api/dozent/*` (Login mit `DOZENT_PASSWORT`, HttpOnly-Cookie 30 Tage).
  Fragen liegen in `data/fragen.json` (Docker-Volume `./data`).
- `.env` (nie ins Chat/Git): `DOZENT_PASSWORT=…`, `COOKIE_SECRET=…` – lokal hier im Ordner, auf dem Server
  `/opt/stacks/langdock-hefte/.env` (deploy.sh lädt sie mit hoch, chmod 600).

## Neuen Kurstag online stellen
1. Folien-PDF als Bilder (PyMuPDF, NN.jpg 1600 px + tNN.jpg 360 px + Folien_TagN.pdf nach `public/folien/tag-N/`, Eintrag in `_quellen/folien.json`)
   Übungsdokumente (falls nötig) wie `_quellen/tag4/material.py` → `public/material/tag-N/`, Liste in `plattform.py` `MATERIAL`, Übungsseite in `UEBUNG`
2. `kurs.py` (Tag 4 steht in `kurs_tag4.py`): Tag mit Learnings (Folie je Learning), Wörtern, Lernkarten, Selbsttest eintragen
3. Heft: eine Vorlage + `zusatz_<person>.html`, in `_quellen/build.py` unter `TAGE` eintragen, `python build.py --tag N`
4. `python build.py --web`, lokal testen: `node server.mjs` → http://localhost:8080/hefte/ und
   `node ops/qa.mjs http://localhost:8080/hefte <ordner> --flow` (Bilder 1280/390, Querscrollen, JS-Fehler, Unklar-Ablauf, PDFs)
5. `bash ops/deploy.sh`, danach `node ops/qa.mjs https://quint-games.de/hefte <ordner> --flow`

**Wichtig:** Heft-Antworten werden über die Reihenfolge der Felder zugeordnet (f0, f1, …). Hefte, die schon ausgefüllt
werden, nicht mehr umbauen (Learnings am Ende sind feldfrei und daher unkritisch).
