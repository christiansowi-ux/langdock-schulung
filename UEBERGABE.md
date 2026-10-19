# Übergabe – Langdock-Schulung „KI Automations Spezialist“

Stand: **14.10.2026** · Kurstage 1–11 online; Tag 12 lokal fertig und geprüft, noch nicht veröffentlicht · Lernplattform: **https://quint-games.de/hefte/** (noindex)

---

## 1. Worum es geht

Futureway KI Institut, Kurs „KI Automations Spezialist“, **Praxisblock Langdock**. Chris (Schulungsleitung) bekommt je Kurstag
die Folien als PDF (`Downloads\<Thema>.pdf`) und daraus entsteht:

| Baustein | Inhalt |
|---|---|
| **Tagesseite** | Learnings (Satz + „Nochmal erklärt“ + Folienbild), Lernkarten, Selbsttest, Folien-Viewer (+ Videos), Wörter, Reiter „Aufgaben“, Lernheft |
| **Lernheft** (ab Tag 4) | PDF + Webfassung, nur zum Lesen und Merken, eine Seite je Gedanke, Merksatz unten, freiwillige Übungen für Langdock am Ende |
| **Praxisheft** (nur Tag 10) | zum Mitmachen: kostenlose APIs und MCP-Server live ausprobieren, eigener dunkler Button |
| **Aufgabengenerator** | freiwillige Zufallsaufgaben je Tag: Kurzaufgaben (5–10 Min) und Deep Learn (60 Min, 5 Etappen) |
| **Unklar?** | überall; Meldung landet bei Chris (Glocke oben, `/hefte/dozent/`), Antwort erscheint bei der Person |

**Teilnehmende** (fest, keine Accounts – Fortschritt nur im Browser):

| Person | Profil | Bereich | Besonderheit |
|---|---|---|---|
| Carmen | B | Teamleitung, Business & Website | arbeitet am **Mac** |
| Ingo | A | Druck & Vertrieb | – |
| Tabea | C | Video, Design & Creative | **kein Agenten-Zugang** → immer Weg ohne Agent anbieten (Projekt, Chat, Skill, Prompt-Bibliothek) |

---

## 2. Stand je Kurstag

| Tag | Datum | Thema (Lektion) | Heft | Generator kurz / deep |
|---|---|---|---|---|
| 1 | 28.09. | KI – Hype oder Realität? | Arbeitsheft A/B/C (Hauptordner) | 5 / 1 |
| 2 | 29.09. | Welches KI-Modell für welche Aufgabe? | Arbeitsheft je Person | 4 / 1 |
| 3 | 30.09. | LLMs unter der Lupe (Prompt-Labor) | ein Heft + Zusatz je Person | 3 / 1 |
| 4 | 01.10. | RAG (+ rag.veluna-labs.de) | Arbeitsheft + **Lernheft** + Material | 4 / 1 |
| 5 | 02.10. | Deep Research (Folien = nur Titel) | Lernheft | 4 / 1 |
| 6 | 05.10. | Prompt Engineering, Teil 1 (Folien 1–26 von 41) | Lernheft | 10 / 2 |
| 7 | 06.10. | Prompting-Techniken, Teil 2 (Folien 27–41) | Lernheft | 10 / 2 |
| 8 | 07.10. | Skills (Lektion 7) | Lernheft | 9 / 2 |
| 9 | 08.10. | Agenten (Lektion 8) | Lernheft | 10 / 2 |
| 10 | 09.10. | APIs & MCP (Lektion 9) | Lernheft + **Praxisheft** | 15 / 3 |
| 11 | 12.10. | KI-Infrastruktur (Lektion 10) | Lernheft | 9 / 2 |

Dazu je Tag 3 allgemeine Aufgaben, die automatisch aus den Learnings entstehen.
Zählung: ab Tag 8 gilt **Tag N = Lektion N − 1** (Tag 6 und 7 = Lektion 6 in zwei Teilen).

PDFs liegen in `Tag N - <Thema>\` (z. B. `Tag 11 - KI-Infrastruktur\Lernheft_Tag11_KI-Infrastruktur.pdf`) und online unter
`https://quint-games.de/hefte/pdf/<Datei>`.

---

## 3. Ordner und Dateien

```
Langdock-Schulung\
├─ UEBERGABE.md                 ← diese Datei
├─ Tag N - <Thema>\             ← fertige PDFs je Tag
├─ _quellen\                    ← alles, was gebaut wird
│  ├─ kurs.py                   Personen, Reihenfolge, Tage 1–3; importiert kurs_tagN.py (ab Tag 4)
│  ├─ kurs_tagN.py              Tagesdaten: titel, unter, datum, folien, kurz, lernheft, (praxisheft), videos,
│  │                            learnings (id, folie | quelle, satz, erklaert), begriffe, karten, test
│  ├─ folien.json               je Tag: pdf, n (Anzahl), slides[{n, links}], ratio
│  ├─ tagN\lernheft.html        Lernheft-Vorlage (Platzhalter siehe Abschnitt 5)
│  ├─ tag10\praxisheft.html     Praxisheft
│  ├─ lernheft.py               HEFTE-Liste (Lernhefte + 'p10'), baut PDF + Webfassung
│  ├─ lernheft.css              gemeinsamer Heft-Stil (Druck A4 + Bildschirm + Handy)
│  ├─ aufgaben.py               Aufgabengenerator: Firmen, Kurz-Muster, Deep Learn, Prüfung
│  ├─ plattform.py              baut alle Plattform-Seiten (über build.py --web)
│  ├─ build.py                  Arbeitshefte Tag 1–4 + Einstieg für --web
│  ├─ measure_lp.mjs / render.mjs / render_plain.mjs   Seiten messen, PDF rendern (playwright-core)
│  └─ build\                    Zwischenstände, Vorschaubilder build\preview\
└─ plattform\                   ← Webserver (Node 22, ohne Framework)
   ├─ server.mjs                statisch + /api/pdf + /api/fragen + /api/dozent/*
   ├─ public\                   wird von build.py --web geschrieben – AUSSER public\assets\ und public\folien\
   │  ├─ assets\                von Hand gepflegt: app.js/css, kurs.js/css, aufgaben.js, dozent.js, hefte.js, web.css
   │  └─ folien\tag-N\          NN.jpg (1600 px), tNN.jpg (360 px), Folien_TagN.pdf
   ├─ ops\deploy.sh             Upload + Container neu bauen
   ├─ ops\qa.mjs                Prüflauf (Bilder, Querscrollen, JS-Fehler, Abläufe)
   ├─ .env                      DOZENT_PASSWORT, COOKIE_SECRET – nie in Chat oder Git
   └─ README.md                 ältere Kurzbeschreibung (vor Lernheften) – diese Datei ist aktueller
```

**Werkzeuge:** Python 3.12 mit `PyMuPDF` (fitz), `pypdf`, `Pillow`; Node 24; `playwright-core` wird aus
`C:\Users\chris\Documents\Unreal Projects\Stille\website\node_modules\` geladen (Pfad steht in den .mjs-Dateien).
Lokaler Server in der Claude-Desktop-App: Preview-Name **`langdock-hefte`** (Port 8080, `.claude/launch.json` im Stille-Projekt).

---

## 4. Neuen Kurstag online stellen (Ablauf, wie seit Tag 6)

1. **Folien lesen** (Text je Folie mit PyMuPDF; reine Bildfolien rendern und ansehen).
2. **Folienbilder + folien.json** – Snippet:
   ```python
   import fitz, json, os
   from PIL import Image
   n, src = 12, r'C:\Users\chris\Downloads\<Thema>.pdf'
   out = rf'plattform\public\folien\tag-{n}'; os.makedirs(out, exist_ok=True)
   # zusätzlich: PDF nach out\Folien_Tag{n}.pdf kopieren
   d = fitz.open(src); slides = []
   for i, p in enumerate(d, 1):
       p.get_pixmap(matrix=fitz.Matrix(1600 / p.rect.width, 1600 / p.rect.width)).save(f'{out}/{i:02d}.png')
       im = Image.open(f'{out}/{i:02d}.png').convert('RGB'); im.save(f'{out}/{i:02d}.jpg', quality=86, optimize=True)
       im.resize((360, round(360 * im.height / im.width))).save(f'{out}/t{i:02d}.jpg', quality=82); os.remove(f'{out}/{i:02d}.png')
       slides.append({'n': i, 'links': list(dict.fromkeys(l['uri'] for l in p.get_links() if l.get('uri')))})
   F = json.load(open(r'_quellen\folien.json', encoding='utf-8'))
   F[str(n)] = {'pdf': os.path.basename(src), 'n': len(d), 'slides': slides, 'ratio': round(d[0].rect.width / d[0].rect.height, 4)}
   json.dump(F, open(r'_quellen\folien.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
   ```
3. **Langdock-Funktionen prüfen**, die im Heft vorkommen (docs.langdock.com) – Learnings aus der Doku mit `'folie': None, 'quelle': 'Langdock'`.
4. **`_quellen/kurs_tagN.py`** anlegen (Vorlage: `kurs_tag11.py`), in `kurs.py` am Ende eintragen:
   `from kurs_tagN import TAGN` / `TAGE[N] = TAGN`. Üblich: 15–20 Learnings, 10–12 Begriffe, 12 Karten, 6 Testfragen.
5. **Lernheft** `_quellen/tagN/lernheft.html` (Vorlage: `tag11/lernheft.html`): Titelblatt, „So liest man“, ~12 Kapitel,
   „Lektion auf einer Seite“, 2 Seiten Übungen, Merkfragen `{{QA}}`, Wörter `{{GLOSSAR}}`. Eintrag in `lernheft.py` → `HEFTE[N]`
   (src, out, pdf, kurz, `uebungen: (14, 15)`, label, titles 1…17 – Titel müssen zu den `{{UX:n}}` passen).
   Bauen: `cd _quellen` → `python lernheft.py --tag N --preview` (misst jede Seite, passt den Zoom an, bricht ab, wenn eine Seite zu groß/breit ist).
6. **Aufgaben** in `_quellen/aufgaben.py`: ~8–10 Kurz-Muster `M('tN-…', N, …)` und **mindestens 1 Deep Learn** `DL('dl-…', N, N, …)`
   (5 Etappen, zusammen **genau 60 Min**). Prüfen: `python aufgaben.py`.
7. **Web bauen:** `python build.py --web`.
8. **QA:** Seiten des Tages in `plattform/ops/qa.mjs` (Liste `pages`) ergänzen, lokalen Server starten, dann
   `node ops/qa.mjs http://localhost:8080/hefte <ordner> --flow` → muss mit „Alles in Ordnung“ enden.
9. **Ausrollen:** `cd plattform` → `bash ops/deploy.sh`, danach derselbe QA-Lauf gegen `https://quint-games.de/hefte`.
10. Antwort an Chris: Links, Heft-PDF, was neu ist, **Folienfehler** (Tippfehler, falsche Angaben) melden.

---

## 5. Lernheft – Technik und Bausteine

- Jede `<section class="lp">` ist **eine A4-Seite** (Inhalt 178 × 266 mm). `measure_lp.mjs --fit` sucht je Seite den größten Zoom
  (1,0–1,36), damit die Seite gefüllt ist; der zweite Durchgang prüft Höhe **und Breite**.
- Platzhalter: `{{HEAD}} {{BAR}} {{LOGO}} {{ICON:name}} {{UX:n}} {{QA}} {{GLOSSAR}} {{VAR:name}}` (Langdock-Variable `{{ name }}` –
  sonst schlägt die Platzhalter-Prüfung an). Icons: chat, search, pen, window, cpu, check, book, layers, star, slides, brain, file,
  globe, plug, arrow, alert, briefcase, megaphone, target, clock, lock, report, flask.
- Häufige Bausteine (`lernheft.css`): `.kh/.kn` Kapitelkopf, `.merk` Merksatz, `.fall` / `.fq` Fall, `.vs` Vergleich, `.flow6`
  (+ `.f4`) Schritte, `.fw.c3/.c4` Kacheln, `.err10` nummerierte Liste, `.cmp3` (+ `.two`) Tabelle, `.map6` Zuordnung, `.techmap`
  (+ `.t3`) Chips, `.code` dunkler Code, `.split2` zwei Codes, `.auftrag` Steckbrief, `.stk` Ebenen, `.calc2` Rechnung, `.cheat`
  Lektion auf einer Seite, `.ueb/.ucode` Übung mit Kopier-Knopf (online), `.reg` Liste (Praxisheft), `.chk` Checkliste.
- Webfassung: `/<person>/tag-N/lernheft/` (Unklar je Kapitel, Kopier-Knöpfe), PDF-Download oben.
- **Praxisheft** = zweite Heft-Art: `HEFTE['p10']` mit `tag`, `art`, `ref`, `unter`; im Kurstag `'praxisheft': 'p10'` →
  Seite `/<person>/tag-10/praxis/`, dunkler Button im Kopf der Tagesseite, eigene Karte im Reiter „Lernheft + Praxis“.
  Bauen: `python lernheft.py --tag p10`.

---

## 6. Aufgabengenerator

- Daten: `_quellen/aufgaben.py` → beim Web-Build als `public/assets/aufgaben.json`; Logik: `public/assets/aufgaben.js`.
- **12 ausgedachte Firmen** (`LAGEN`, je 4 pro Bereich druck/web/video) mit Feldern wie firma, was, rolle, produkt, fakten,
  zielgruppe, kanal_fuer, ziel, mail, beschwerde, notizen, stil, leistung, preis, recherche_thema … – Texte nutzen `{feld}`.
  Bereichsfelder: alltag, aufg_text, aufg_bild, ms_frage, rabatt.
- **Rechenaufgaben** (Zahlen aus dem Seed, Lösung wird mitgerechnet): `kunden`, `rabatt`, `vram`, `kosten` → Platzhalter `{r_frage}`, `{r_weg}`.
- Eine Aufgabe = Muster × Firma × Seed; die **Nummer** (z. B. `t7-json.d1.55`) baut überall dieselbe Aufgabe (`?aufgabe=`).
- **Tages-Regel** (Fix 09.10.): Eine Tagesseite zeigt **nur** Aufgaben ihres Tages (Kurz und Deep). Der Haken „auch frühere Tage“
  gilt nur auf der Seite; eine Nummer eines anderen Tages leitet auf dessen Tagesseite um. Seite „aus allen Tagen“: `/<person>/aufgaben/`.
- `python aufgaben.py` prüft: alle Platzhalter füllbar, Learnings existieren, Deep Learn = 60 Min, Deep-Learn-Learnings nur von Tagen ≤ eigener Tag.
- `qa.mjs --flow` prüft alle Tagesseiten auf den richtigen Tag und die Weiterleitung.

---

## 7. Plattform, Server, Sicherheit

- Server: **Quint-VPS** `root@212.227.85.113` (Schlüssel `~/.ssh/id_ed25519`), Stack **`/opt/stacks/langdock-hefte`** (Docker,
  gemeinsames Traefik-Netz `web`, Router-Priorität 115, Pfad `/hefte`). **Nur diesen Stack anfassen** – auf dem Server laufen viele
  andere Dienste (u. a. das Portal `quint-games`, nicht anfassen).
- `.env` lokal in `plattform\` und auf dem Server (chmod 600) – **nie** ins Chat, in Git oder in Dateien kopieren.
- Fragen liegen in `data/fragen.json` (Docker-Volume). Dozenten-Login per HMAC-Cookie (30 Tage).
- CSP: nur eigene Quellen + `youtube-nocookie.com` für Videos.
- Mehrere `qa.mjs --flow`-Läufe direkt hintereinander laufen in die Anmeldebremse (Dozenten-Login / Meldungen) → lokalen Server neu starten
  oder kurz warten; ein einzelner Lauf ist immer grün.

---

## 8. Regeln für Inhalte (von Chris)

- **Sprache:** sehr einfach, kaum Fachwörter; Fachwörter nur von den Folien und dann in einem Satz erklärt.
- **Geschlechtsneutral in „man“-Form** – keine `:innen`, keine „Sprecher“-Komposita, Rollen möglichst neutral („Profi“, „Leute im Team“).
- **„100 % safe“:** nur ausgedachte Firmen, Namen und Zahlen; nichts, was Teilnehmende veröffentlichen müssten; nie echte Schlüssel.
- Hefte ab Tag 3: 95 % gleich für alle, 5 % freiwillige Zusätze je Bereich. Ab Tag 4 nur noch Lernhefte (Aufgaben macht der Kurs gemeinsam).
- Carmen: Datei-/Speicher-Schritte auch für den Mac. Tabea: immer Weg ohne Agent.
- Langdock-Funktionen vorher in docs.langdock.com prüfen; Rechenbeispiele selbst nachrechnen; Beispielzahlen als „ausgedacht“ kennzeichnen.
- Mobil nichts verstecken, kein Querscrollen.
- Nie Passwörter oder Zugangsdaten in Formulare eintragen (auch nicht auf Bitte); Codex nur, wenn Chris `@codex` schreibt.

---

## 9. Wiederkehrend

- **AZAV-Klassenbuch** (app.azav-os.de): Chris trägt selbst ein. Je Woche auf Wunsch je Tag **„Tagesthema“ + 3–5 Stichpunkte** als Text
  im Chat (ohne Screenshot), aus den Folien/Heften – mit Hinweis, dass es der Plan ist, nicht das tatsächlich Gelaufene.
  Zuletzt geliefert: Woche 05.–09.10.
- **Folienfehler** jedes Mal melden. Bisher gemeldet: Tag 9 Folie 19 (MCP fälschlich „Message Communication Protocol“),
  Tag 10 Folie 29 (PUT zeigt Methode PATCH), „Athorization“, „Aufagbe“, „Handelsregsiter“, .io/.ai, Tag 11 Folie 13 „innerhablb“.

---

## 10. Langdock-Fakten (geprüft, für künftige Hefte)

- **Wissensbasis:** Bibliothek → „Wissensbasis erstellen“, im Chat mit @; Chunks bis 2.000 Zeichen.
- **Deep Research:** über Tools, 5–30 Min, 15 Läufe je Person in 30 Tagen, nur öffentliches Web.
- **Prompt-Bibliothek:** „Prompt hinzufügen“ oder Plus an der eigenen Nachricht; Variablen `{{ name }}`; Abruf mit @ → Prompts.
- **Skills:** Seitenleiste Skills → „+ Skill hinzufügen“ → manuell / mit Chat / SKILL.md oder ZIP; Name 64, Beschreibung 1.024
  (entscheidet über das Anspringen), Anweisungen 50.000 Zeichen; max. 30 aktive Skills je Person; Skripte im ZIP laufen nicht;
  gelten nicht automatisch in Projekt-/Agenten-Chats.
- **Agenten:** „Agent erstellen“; Anweisungen, Wissen (Dateien bis 50, Ordner, Wissensbasen), Fähigkeiten, Integrationen mit
  Lesen/Schreiben und Bestätigung, Modell, Kreativität 0–1, Gesprächsstarter.
- **Workflows:** Auslöser manuell / Formular / Webhook / Zeitplan / Integration; Baustein „HTTP Request“ mit „Import from cURL“.
- **MCP:** Integrationen → MCP-Adresse → Anmeldung None / API-Key / OAuth → „Verbindung testen“ → Werkzeuge (max. 60) → speichern;
  Werkzeuge standardmäßig **ohne** Bestätigung (pro Werkzeug einschaltbar); im Chat per @ nutzbar (auch ohne Agent).
  Am 09.10. ohne Anmeldung erreichbar: learn.microsoft.com/api/mcp, mcp.deepwiki.com/mcp, mcp.kiwi.com, mcp.exa.ai/mcp,
  mcp.context7.com/mcp, huggingface.co/mcp, knowledge-mcp.global.api.aws, docs.mcp.cloudflare.com/mcp.

---

## 11. Offene Punkte

- Integrationen anlegen dürfen nicht alle Konten – ggf. im Langdock-Workspace freischalten (steht im Praxisheft als Hinweis).
- Übungs-Integrationen und Übungs-Skills nach dem Kurs aufräumen (Teilnehmende).
- `plattform/README.md` ist älter (vor Lernheften, Generator, Praxisheft) – bei Gelegenheit auf diese Datei kürzen.
- Kostenlose MCP-Server/APIs können sich ändern – vor erneutem Einsatz kurz mit einem MCP-Handshake bzw. Browser-Aufruf prüfen.


## Ergänzung 14.10.2026 - Tag 12 EU AI Act

- Grundlage: `Downloads/EU-AI-Act.pdf`, 23 Seiten, Lektion 11. Claude-Verlauf vom 12./13.10. und diese Übergabe abgeglichen. Live-Startseite zeigt aktuell Tage 1-11.
- Tag 12 lokal vollständig: 20 Learnings, 12 Karten, 6 Selbsttestfragen, 12 Begriffe, 23 Originalfolien, 20-seitiges Lernheft, 10 Kurzaufgaben + 2 Deep Learn (je 5 Etappen / 60 Min.). Datum der neuen Ausgabe: 14.10.2026.
- Dateien: `_quellen/kurs_tag12.py`, `tag12/lernheft.html`, `tag12/quellen-und-korrekturen.md`, `tag12/pruefprompt.txt`. Registrierung in `kurs.py` und `lernheft.py`; Aufgaben in `aufgaben.py`. Neue QA-Routen in `plattform/ops/qa.mjs`.
- Lernheft: `Tag 12 - EU AI Act/Lernheft_Tag12_EU-AI-Act.pdf`; Web für alle drei Personen unter `/hefte/<person>/tag-12/` und `/lernheft/`.
- Einfache Sprache, fiktiver durchgehender Fall Studio Morgen, Tabea ohne Agent mit gleichem Chat-Prüfprompt. Aktuelle Langdock-Doku bestätigt: Skills lassen sich im Agenten unter Instructions / Skills ausdrücklich anhängen; Zugriffsrechte auf den Skill nötig. Web Search muss aktiviert werden.
- Amtliche Quellen am 14.10. geprüft. Korrekturen u. a.: Folie 6 Art. 26 statt Art. 29; Omnibus ändert auch Inhalte; Pflichten nach Rolle trennen; keine pauschale Art.-27-Pflicht; keine allgemeine Veröffentlichung sämtlicher GPAI-Modellinfos in einem EU-Register. Korrekturen im Lernheft und separater Quellenliste. Folien-PDF bleibt bytegleich.
- Prüfung: Generator-Prüfung ohne Fehler, PDF-Seitenmaßprüfung aller 20 Seiten + visuelle Kontrolle, 453 Struktur-/Link-/HTTP-/Bestandsschutzprüfungen. Browser: drei Personen bei 390/1280 px ohne horizontalen Überlauf und ohne JS-Fehler; Selbsttest 6/6, Karten, Kurz/Deep, lokales Unklar-Senden, dynamischer Lernblatt-PDF-Export (5 Seiten) geprüft. Der vollständige alte ops/qa.mjs --flow-Lauf wurde nicht ausgeführt; Backend unverändert.
- Lokale Vorschau: `http://localhost:5387/hefte/`, Prozess in Codex gestartet, `DATA_DIR` zeigt ausschließlich auf Testdaten im aktuellen Chat/work. Keine echten Fragen verändert, kein Dozenten-Login verwendet.
- Backup und Validierung unter `C:/Users/chris/Documents/Codex/2026-10-14/scha/work/`: `langdock-vor-tag12.zip` (ohne Secrets und Teilnehmerfragen), `before-hashes.json`, `validation-tag12.json`, `validate_tag12.py`.
- Veröffentlichungsstatus: NICHT deployed. Freigabe für Live-Schritt steht aus. Das vorbereitete `work/tag12-public.tar.gz` enthält nur neue/geänderte öffentliche Dateien; kein Servercode, keine .env, keine Fragen. Vor Deployment Live-Stand und Backup prüfen, nur Stack langdock-hefte verwenden.

## Ergänzung 14.10.2026 – aktives Lernen und vollständige einfache Erklärungen

- Chris wünscht ausdrücklich weniger trockene Vermittlung, verständliche Umschreibungen ohne vorausgesetztes Fachwissen und vollständige inhaltliche Folienabdeckung. Der dauerhafte redaktionelle Standard steht in `LERNKONZEPT.md`.
- Alle 12 Tage haben jetzt „Trainieren“: fünf Ausgangsfragen, eigene Antwort vor dem Aufdecken, ehrliche Selbsteinschätzung, begrenzte Wiederholung unsicherer Karten, spätere Abrufe nach 1/3/7 Tagen. Neue eigene Merksätze pro Person/Tag; getrennte lokale Speicherung ohne Änderungen an alten Heftfeldern.
- Tag 12 hat zusätzlich „Einfach erklärt“: jede der 23 Folien mit verständlicher Erklärung, vollständigerer Detailauflösung, Alltagsbeispiel, Frage und Musterantwort. Grafiktext von Folie 4 visuell gelesen; alle fünf Ziele übernommen. Originalfolien bleiben unverändert. Fachliche Korrekturen klar markiert.
- Tag 12 hat 23 neue Abruffragen zusätzlich zu den bestehenden 12 Lernkarten und sechs Quizfragen. Neun Fallübungen insgesamt, pro Person fünf; Auswahlantworten mit individuellem Feedback und erneuter Runde nur für offene Fälle. Tabea mit normalem Chat als Agent-Alternative.
- Code: `_quellen/einfach_tag12.py`, `_quellen/lerntraining.py`, Einbindung in `plattform.py`; neue öffentliche Assets `lerntraining-core.js`, `lerntraining.js`, `lerntraining.css`; Reiter-/Sprungnavigation in `kurs.js` erweitert.
- Prüfung: sieben Tests der Terminlogik; 277 Inhalts-/Integrationsprüfungen und 462 bestehende Struktur-/Link-/Bestandsschutzprüfungen. Im Browser komplette Abrufrunde mit unsicherer Wiederholung, alle fünf Fälle, falsches Feedback und erneute Runde, persistente Notiz/Termin, profilgetrennte Daten, früherer Kurstag, direkte Verweise bis Originalfolie geprüft. 320/390/768/1280 px ohne horizontalen Seitenüberlauf. Kein vollständiger Screenreader-Audit oder neuer kompletter Backend-Testlauf.
- Paket `work/tag12-public.tar.gz` und Manifest aktualisiert (108 öffentliche Dateien gegenüber Ausgangsstand). Es enthält Tag 12 UND die neue Lernoberfläche. Keine echten Teilnehmerfragen verändert; Browserproben betreffen nur localhost. Weiterhin NICHT live veröffentlicht.

## Live-Veröffentlichung 14.10.2026 – von Chris ausdrücklich beauftragt

- Chris: „Mach die anderen Änderungen jetzt erstmal live. Und danach kannst du weiter machen.“ Tag 12, Einfach erklärt, Erinnerungsrunden und Fallwerkstatt sind jetzt veröffentlicht. Frühere Hinweise „nicht live“ beschreiben den vorherigen Stand.
- Nur das freigegebene Paket mit 108 öffentlichen Dateien eingespielt; angefangene neue Demo-Umgebungen NICHT enthalten. Vorher jeden Zielpfad gegen den Ausgangsstand geprüft.
- Backup: `/opt/stacks/langdock-hefte/releases/20261014-training/public-before.tar.gz`; altes Image `langdock-hefte:pre-20261014-training`, neues Image `langdock-hefte:release-20261014-training`.
- Neubau mit bestehendem Servercode und Paketen; `.env`, Compose-Konfiguration und Teilnehmerfragen unverändert. Nur Dienst `langdock-hefte` neu gestartet. Healthcheck erfolgreich.
- 107 öffentlich abrufbare Dateien per HTTPS inhaltlich exakt gegen SHA-256 des Pakets geprüft. `manifest.json` wird absichtlich nicht als öffentliche Route ausgeliefert; separat auf Host und im Container prüfen.
- Browser live: 23 Erklärungsabschnitte, Trainingsstart, Reiter und keine JS-Warnungen/Fehler. Nachweis im aktuellen Chat: `outputs/Lernplattform-live.jpg`, Prüfprotokoll `work/live-verification.json`.
- Die zusätzlich gewünschten interaktiven Demo-Umgebungen werden danach zunächst lokal weitergebaut.

## Demo-Werkstatt – lokaler Folgestand nach dem Live-Release

- Neue Demo-Navigation und ausdrucksstärkere Werkstattoberfläche. Prompt-Studio an allen Tagen, zusätzlich Einsatz-Labor, Website-Chat und Assistenz-Teststand an Tag 12. Die Originalfolien und vollständigen einfachen Erklärungen bleiben erreichbar.
- Feste, ausgedachte Beispiele; keine API, kein echtes Sprachmodell, keine Account-Erstellung, kein externer Versand. Simulation sichtbar gekennzeichnet, keine rechtliche Freigabe. Prompt kopierbar; Lernnotiz als lokale TXT-Datei herunterladbar.
- Code: `_quellen/demowerkstatt.py`, Einbindung in `plattform.py`, Assets `demo-core.js`, `demos.js`, `demos.css`, Tests `ops/demos.test.cjs`.
- Sieben bisherige Termin-Tests plus sechs Demo-Tests (einschließlich aller 16 Kombinationen der Assistenzregeln) bestanden. 144 Strukturprüfungen aller 36 Tagesseiten, 471 bestehende Struktur-/Link-/Bestandsschutzprüfungen bestanden.
- Browser: alle vier Einsatzfälle, fehlende Vermutung, Prompt-Bausteine, sichtbarer später/früher KI-Hinweis, Besucherfrage, Assistenz 0/3 → 3/3, TXT-Download, gespeicherter Zustand, vier Bildschirmbreiten und keine beobachteten JS-Fehler. Kein vollständiger Screenreader-Test.
- Neues Paket `work/demos-public.tar.gz` basiert auf dem veröffentlichten Training-Stand; Manifest `work/demos-release-manifest.json`. Das alte freigegebene `tag12-public.tar.gz` wird nicht überschrieben. Demos noch NICHT live.


## Demo-Werkstatt live – 14.10.2026

Auf ausdrücklichen Wunsch von Chris sind jetzt auch die vier Demo-Umgebungen veröffentlicht: Prompt-Studio, Einsatz-Labor, Website-Werkstatt und Assistenz-Teststand. Das Prompt-Studio steht an allen zwölf Tagen bereit, alle vier Demos an Tag 12, jeweils für Ingo, Tabea und Carmen.

Release: `20261014-demos`. 48 geänderte öffentliche Dateien wurden nach Prüfung des Ausgangsstands übertragen. Alle 48 über HTTPS ausgelieferten Dateien stimmen per SHA-256 mit dem geprüften Paket überein. Container gesund; Prompt-Interaktion und Website-Hinweisprüfung direkt live getestet, keine Browserfehler.

Backup: `/opt/stacks/langdock-hefte/releases/20261014-demos/public-before.tar.gz`. Vorheriges Image: `langdock-hefte:pre-20261014-demos`; neues Image: `langdock-hefte:release-20261014-demos`. Bestehender Servercode, Konfiguration und Teilnehmerdaten wurden beibehalten. Frühere Hinweise auf einen ausschließlich lokalen Demo-Stand sind damit überholt.

Live: https://quint-games.de/hefte/tabea/tag-12/#demos


## Tag 13 – DSGVO: lokaler geprüfter Stand vom 15.10.2026

Noch nicht veröffentlicht. Tag 12 und die bisherigen Demos bleiben im Release 20261014-demos live.

- Quelle: DSGVO.pdf, 74 Folien. Original bytegenau erhalten; alle Folien einzeln in einfacher Sprache mit Details, erfundenem Beispiel, eigener Frage, Musterantwort und nötigen Präzisierungen begleitet. Amtliche Quellen im Heft und in `_quellen/tag13/quellen-und-korrekturen.md`.
- Neue Datenschutz-Werkstatt für Ingo, Carmen und Tabea: sechs Daten-Detektiv-Fälle, ein interaktiver Datenrucksack mit jeweils neun Feldern, sechs Posteingang-Fälle. Fehler erklären den Denkweg, neue Versuche bleiben möglich. Die Prompt-Mission unterscheidet Druck/Versand, Website-Antwort und Videotext.
- 74 neue Erinnerungsfragen, 28 Learnings, zwölf Lernkarten, acht Selbsttestfragen, zwanzig Wörter. Acht zusätzliche Kurzaufgaben und eine Deep-Learn-Aufgabe mit fünf Etappen ergänzen den vorhandenen Generator.
- Kein echter KI-Aufruf, keine externen Nachrichten; alle Beispieldaten erfunden. Lernstand und Notiz nur im Browser je Person. TXT-Mitnahme. Ohne lokalen Speicher bleibt vorübergehendes Üben möglich.
- Druckheft: `Tag 13 - DSGVO/Lernheft_Tag13_DSGVO.pdf`, 76 Seiten. Cover, 74 Folienbegleitungen, Quellen. Native Textblöcke innerhalb der Seitengrenzen; Sichtproben einschließlich dichter Seiten kontrolliert.
- Quellen: `_quellen/einfach_tag13.py`, `kurs_tag13.py`, `aufgaben_tag13.py`, `datenschutzwerkstatt.py`, `tag13/lernheft.html`. Materialaufbau mit `python tag13/build_material.py`, danach `python build.py --web` (aus `_quellen`). Builder verwendet bevorzugt das bereits eingebundene Original, sonst Downloads/DSGVO.pdf; PyMuPDF, Pillow und ReportLab sowie Windows Arial erforderlich.
- Assets: `privacy-core.js`, `privacy.js`, `privacy.css`. Tests: `node --test ops/privacy.test.cjs ops/demos.test.cjs ops/lerntraining.test.cjs` – 19/19 bestanden, darunter alle 1.536 Prompt-Feldkombinationen.
- Struktur: alle 74 Erklärungen und Originalbilder, drei Personen, 177 lokale Verweise auf existierende Ziele, Original-PDF-Hash identisch. 36 bisherige Tagesseiten inhaltlich unverändert, lediglich Aufgaben-Cachekennung/Leerzeile verändert. Neun HTTP-Stichproben erfolgreich.
- Browser: alle zwölf Entscheidungsfälle, Fehlversuche, fehlende/überflüssige/richtige Promptdaten, gespeicherte Notiz/Fortschritt, Profiltrennung, drei Promptvarianten, Tastaturaktivierung, Trainingsstart, Kurz-/Deep-Learn-Aufgabe, Erklärung→Originalfolie, Quellenanker. Kein horizontaler Überlauf bei 320/390px; kein vollständiger Screenreader-Test. Keine beobachteten JS-Warnungen/Fehler. TXT-Download angestoßen; Dateiinhalt nicht separat im Browserdownload geöffnet.
- Lokale Vorschau: http://localhost:5387/hefte/tabea/tag-13/#demos (Server im aktuellen Chat).
- Sicherung und Veröffentlichungspaket im Chat-Arbeitsverzeichnis `C:/Users/chris/Documents/Codex/2026-10-14/scha/work/dsgvo/`: `before-tag13.zip`, `before-hashes.json`, `tag13-public.tar.gz`, `release-manifest.json`. 212 öffentliche Dateien, etwa 10,3 MB; kein Servercode, keine Konfiguration, keine Teilnehmerdaten. Vor Veröffentlichung Live-Ausgangsstand erneut prüfen.


## Tag 13 live – 15.10.2026

Chris hat ausdrücklich „Mach es live danke.“ beauftragt. Release `20261015-dsgvo` ist veröffentlicht. Alle drei Profile, die drei Datenschutz-Missionen, 74 Folienbegleitungen, Übungen und das Lernheft sind live. Frühere Hinweise „noch nicht live“ sind für Tag 13 damit überholt.

212 öffentliche Dateien nach Ausgangsstandsprüfung veröffentlicht. 211 öffentlich erreichbare Dateien per HTTPS bytegenau gegen die geprüften SHA-256-Werte bestätigt; internes manifest.json separat auf Host und im Container bestätigt. Dienst running/healthy. Daten-Detektiv und erfolgreiche Prompt-Minimierung direkt live im Browser geprüft, keine JS-Warnungen oder Fehler beobachtet.

Backup: `/opt/stacks/langdock-hefte/releases/20261015-dsgvo/public-before.tar.gz`. Vorheriges Image `langdock-hefte:pre-20261015-dsgvo`, neues Image `langdock-hefte:release-20261015-dsgvo`. Bestehender Servercode, Konfiguration und Teilnehmerdaten beibehalten. Nur Dienst langdock-hefte neu gestartet. Prüfprotokoll im Chat: `work/dsgvo/live-verification.json`.

Live: https://quint-games.de/hefte/tabea/tag-13/#demos


## Tag 14 – Agent Observability, 16.10.2026 – lokal fertig und geprüft

- Auftrag: heutigen Kurstag aus Agent-Observability.pdf erstellen, dazu Tagesthema und Stichpunkte für das AZAV-Klassenbuch. Noch nicht veröffentlicht; Tag 13 bleibt im Release 20261015-dsgvo live.
- Original: acht Folien, Ausgabe Juli 2026. Text und gerenderte Gesamtübersicht aller Seiten abgeglichen, Link-Karte von Folie 7 zusätzlich vergrößert geprüft. Original bytegenau erhalten. Folie 7 „alle Konversationen“ auf aktivierte angebundene Agenten präzisiert; aktuelle Langfuse-Anleitung vom 16.10.2026. Beobachtete Vorgänge nicht mit privaten Modellgedanken gleichsetzen; Graph, Kostenerfassung und Vollständigkeit hängen von Instrumentierung ab.
- Alle acht Folien vollständig in Einfach erklärt und im elfseitigen Lernheft: Details, erfundene Beispiele, Merkfragen, Musterantworten, markierte Präzisierungen. Zusätzlich Praxisanleitung mit drei Missionen und Quellenverzeichnis.
- Daten: 18 Learnings, zwölf Lernkarten, sechs Quizfragen, 16 Wörter, acht neue Trainingsfragen. Sechs zusätzliche Kurzaufgaben und eine Deep-Learn-Aufgabe in fünf Etappen/60 Minuten, alle ohne Agent-Zugang nutzbar.
- Agenten-Cockpit: vier anklickbare Trace-Stationen und Ursachenwahl, vier Varianten nach festen Qualitäts-/Zeit-/Kostenkriterien, sechs Begriffszuordnungen mit Feedback und erneuten Versuchen. Personalisierung: Ingo/Versandpreis, Carmen/Website-Öffnungszeit, Tabea/Videotext. Nur vorbereitete Daten; keine echte Anbindung, keine API, kein Versand.
- Speicher: kurs:observability:v1:<person>:t14. Lokale Speicherung von drei Lernständen und Merksatz; Notiz als TXT. Bei nicht verfügbarem Speicher vorübergehend nutzbar. Alte Speicherkennungen und Heftfelder unverändert.
- Code: einfach_tag14.py, kurs_tag14.py, aufgaben_tag14.py, observabilitywerkstatt.py, public/assets/observability-core.js, observability.js, observability.css. Integration in kurs.py/plattform.py/lerntraining.py/aufgaben.py/lernheft.py.
- Materialaufbau: aus _quellen `python tag14/build_material.py`, danach `python build.py --web`. Der Builder nutzt bevorzugt das bereits eingebundene Original und sonst Downloads/Agent-Observability.pdf. Folienlinks sind Strings nach bestehendem Schema.
- Prüfung: 25 Node-Tests bestanden (neue Variantenlogik, falsche/schnelle Antwort, alle Profile und Stationen, eindeutige sechs Signalaufgaben; bestehende Privacy/Demo/Training-Tests). Alle acht Erklärungen, drei Profile, 45 lokale Ziele, neun HTTP-Proben, Originalhash und unveränderter Inhalt aller 39 bisherigen Tagesseiten bestätigt (nur Aufgaben-Cachekennung geändert). Keine bestehenden Dateien entfernt.
- PDF: elf Seiten, alle Textblöcke innerhalb der Seiten, Sichtprüfung aller elf gerenderten Seiten. Ausgabe in Tag 14 - Agent Observability. Keine Layoutfehler beobachtet.
- Browser: alle vier Stationen, falsche/richtige Ursachenwahl, Vergleich B/C/D samt Feedback, alle sechs Signalaufgaben mit Fehlversuch, Notiz/Fortschritt nach Reload, getrennte Personen, Tastaturaktivierung und wiederhergestellter Variantenfokus, Erklärungslink und Originalfolie, Trainingsübersicht, generierte Tagesaufgabe und TXT-Download samt Inhalt geprüft. 320/390/1280px ohne horizontalen Dokumentüberlauf. Keine beobachteten JS-Warnungen/Fehler. Kein vollständiger Screenreader-Test.
- Vorschau: http://localhost:5387/hefte/tabea/tag-14/#demos . Lokaler Server des Chats auf 5387, synthetischer QA-Datenordner.
- Sicherung und vorbereitetes öffentliches Paket im Chat-Arbeitsordner work/observability/: before.zip, before-hashes.json, tag14-public.tar.gz, release-manifest.json, validate.py. Kein Servercode, keine Konfiguration und keine Teilnehmerfragen im Paket. Vor Veröffentlichung Live-Stand prüfen.
- Klassenbuch: Freitag 16.10., Agent Observability – Tracing, Logging und Evaluation. Inhalte und praktische Simulation erläutern; eine echte Langdock-/Langfuse-Verbindung wurde nicht durchgeführt.
- Ergänzung zur Wochenübersicht, von Chris bestätigt: Dienstag 13.10. war Teil 2 der KI-Infrastruktur-Lektion vom Montag 12.10. Die bisherigen Plattformdaten von Tag 11 wurden dadurch nicht umdatiert.


## Tag 14 mit leichten Langdock-Spielen live – 16.10.2026

Chris: „Mach mal noch paar leichte Aufgaben rein in das Lernheft jeweils die man in Langdock machen kann, die sollen auch spaßig sein.“ Danach ausdrücklich „und mach es dann alles live bitte“.

- Vier zusätzliche Spiele für normalen Langdock-Chat: Fehlerdetektiv; Vier Spuren, vier Schubladen; Klingt gut – stimmt es auch?; Zehn-Sekunden-Schnecke. Je etwa 5–8 Minuten, Fall, Spielauftrag, Selbstcheck, verdeckte Web-Auflösung und freiwillige Bonusrunde. Jede Aufgabe mit eigener Variante für Ingo, Carmen und Tabea; zwölf vollständige kopierbare Prompts pro Web-Lernheft. PDF zeigt gemeinsame Spielaufträge und drei wählbare Fälle, jetzt 15 Seiten. Keine echten Systeme gemessen und keine Langdock-Konten verbunden.
- Daten in `_quellen/tag14/easy_tasks.py`. Builder `tag14/build_material.py` ergänzt Web- und PDF-Seiten, Inhaltsverzeichnis k10–k13 und Quellenverweise auf Seite 15. Vollständige Folienbegleitung erhalten.
- Bei der Browserprüfung Copy-Bug gefunden und korrigiert: app.js hatte innerText zu Beginn aus zugeklappten Bereichen gelesen; dieser war leer. Jetzt Fallback auf textContent. Sechs repräsentative Prompts über alle vier Spiele und alle Profile kopiert und nichtleeren vollständigen Inhalt bestätigt; auch live geprüft. Geöffnete normale Prompts verwenden weiterhin innerText.
- Alle 15 PDF-Seiten auf Textgrenzen geprüft; alle vier neuen Seiten gerendert und visuell geprüft. Drei Web-Hefte enthalten je alle zwölf vollständigen Prompts. Die bestehende Strukturprüfung erneut bestanden (39 frühere Tagesseiten inhaltlich erhalten; Original-PDF unverändert).
- Veröffentlichung: Release 20261016-observability, 82 öffentliche Dateien nach Prüfung des Live-Ausgangsstands. 81 per HTTPS bytegenau bestätigt, internes manifest.json auf Host und Container mit SHA256 15ea152828618308608a4702290e0fcfaaa18f6a78218acd0f8f84a5bb31398e bestätigt. Container running/healthy. Live-Kopierfunktion und Cockpit-Ursachenwahl erfolgreich, keine beobachteten JS-Warnungen/Fehler.
- Backup: `/opt/stacks/langdock-hefte/releases/20261016-observability/public-before.tar.gz`. Vorheriges Image `langdock-hefte:pre-20261016-observability`; neues Image `langdock-hefte:release-20261016-observability`. Servercode, Konfiguration und Teilnehmerdaten beibehalten. Nur Dienst langdock-hefte neu gestartet.
- Im Chat work/observability/: geprüfter release-manifest.json, tag14-public.tar.gz, deploy_remote.py, live-verification.json. Vor späteren Änderungen neuen Ausgangsstand verwenden; validate.py erstellt ein Vorbereitungspaket und ist kein Nachweis für spätere Live-Releases.
- Live-Aufgaben: https://quint-games.de/hefte/tabea/tag-14/lernheft/#k10 . Tag 14 samt vollständigem Agenten-Cockpit ist veröffentlicht. Frühere Hinweise „lokal / nicht veröffentlicht“ beschreiben den vorigen Stand.


## Tag 15 · Claude, Antigravity und Codex · 19.10.2026 · lokal fertig

Neues Lernheft auf Basis von Einfuhrung-Claude.pdf. Chris hat den Vergleich für die drei Branchen und anschließend spannende Plugins/MCP beauftragt. Für diesen Tag wurde keine Veröffentlichung angefordert. Vorheriger Live-Stand Tag 14 bleibt bestehen.

- 41-seitiges PDF, parallel als Web-Lernheft für Ingo, Carmen und Tabea. Sechs kurze Branchen-Missionen mit gewöhnlichem Chat als Alternative, ein gemeinsames Vergleichslabor und acht Wissensfragen. Tagesübersicht zur Eintragung auf Seite 41.
- Alle 28 Originalfolien textlich und visuell geprüft und einzeln in einfachen Worten begleitet, einschließlich der Einstellungsbilder. Original bytegleich eingebunden; SHA256 531a45652a7eededbefc90bc4686ff423e47a8e66a8dc79d63fca1dd637c5745.
- 24 offizielle Herstellerquellen, Recherchetag 19.10.2026. Aktuelle Produktoberflächen und Tarife eingeordnet; keine eigenen Produkt-Benchmarks oder bestätigte Einrichtung behauptet. Unbelegte Beteiligungs-/Bewertungszahlen und 50-Prozent-Halluzinationsaussage ausdrücklich eingeordnet. Offline-Aussage und Verwechslung Chat-Projekt/Claude Code korrigiert.
- Erweiterungen: HubSpot Remote MCP, Canva Design-MCP, Figma MCP, Microsoft Playwright MCP, HeyGen Remote MCP sowie Remotion Plugins/Skills. Mini-Aufträge, Rechte, Anmeldung, mögliche Kosten und Client-Unterschiede benannt. Figma-Katalog: Codex/Claude Code lesen und schreiben lokal/remote, Antigravity lokal/lesend. Keine Konten verbunden, keine Erweiterung installiert.
- Integration: kurs_tag15.py, einfach_tag15.py, tag15/content.py und build_material.py. Registrierung in kurs.py/lernheft.py, 28 neue Wiederholungsfragen in lerntraining.py. Assets toolbook.css/js. Reproduzierbarer Aufbau und Prüfung: _quellen/tag15/README.md.
- Verifikation: alle 41 PDF-Seiten gerendert, Kontakte vollständig visuell geprüft; Tabellen und dichte Seiten zusätzlich groß geprüft. Textblöcke innerhalb Seitengrenzen, keine Schriftverkleinerung erforderlich. 897 lokale Verweise kontrolliert. Browser je Profil: 24 Quizpfade, 17 vollständige Aufträge kopiert, Notiz speichern und TXT-Inhalt geprüft; Profiltrennung sowie fehlender Speicher getestet. Kein horizontaler Überlauf bei 320/390/1280px. Keine beobachteten JS-/Konsolenfehler nach Korrektur einer Klassenkollision im Einfach-Bereich. Bestehende 19 Lerntraining-/Demo-/Datenschutztests bestanden. Kein vollständiger Screenreader-Test.
- Prüfdaten und Screenshots: _quellen/build/tag15/validation.json und web-*.png. Quelle/Korrekturen: tag15/sources.json und folienabgleich.md.
- PDF: Tag 15 - KI-Werkzeuge im Vergleich/Lernheft_Tag15_KI-Werkzeuge-im-Vergleich.pdf. Zusätzliche Ausgabekopie im Chat unter output/pdf/.
- Lokale Vorschau läuft auf http://localhost:5387/hefte/tabea/tag-15/lernheft/#k17 ; ebenso ingo und carmen. Plattformserver unverändert. Für eine spätere Veröffentlichung neues geprüftes Paket und aktuellen Live-Ausgangsstand verwenden.


## Tag 15 live – 19.10.2026

Chris hat mit „mach alles live“ ausdrücklich die Veröffentlichung beauftragt. Release `20261019-ki-werkzeuge` ist veröffentlicht. Alle vorherigen Hinweise „lokal / nicht live“ sind für Tag 15 überholt.

- 123 öffentliche Dateien nach Abgleich mit dem Live-Ausgangsstand veröffentlicht; keine abweichenden fremden Änderungen festgestellt. Die Inhalte aller 42 bisherigen Tagesseiten sind nach Normalisierung der Aufgaben-Cachekennung und Leerzeilen unverändert.
- 122 öffentliche Dateien per HTTPS bytegenau gegen das Paket bestätigt. Internes manifest.json auf Host und im Container geprüft: SHA256 `9ca17a6132a17b42c2de924d21d0974a0d6c83ac96f55fd10e94b9c9ff8384c9`. Dienst running/healthy; vorhandene Serverdateien und Konfiguration per Hash unverändert. Bestehendes Datenvolume beibehalten.
- Live-Browserprüfung aller drei Profile: 41 Kapitel, 28 Folienerklärungen, falsche/richtige Quizantwort, vollständigen Auftrag kopieren, 390px-Ansicht ohne Querscrollen, Antwort aufklappen und Learning abhaken. Keine beobachteten JS-/Konsolenfehler.
- Backup `/opt/stacks/langdock-hefte/releases/20261019-ki-werkzeuge/public-before.tar.gz`; vorheriges Image `langdock-hefte:pre-20261019-ki-werkzeuge`, neues Image `langdock-hefte:release-20261019-ki-werkzeuge`. Nur Dienst langdock-hefte neu gestartet.
- Paket und Protokolle im Chat-Arbeitsverzeichnis `work/toolvergleich/release/`: release-manifest.json, tag15-public.tar.gz, deploy_remote.py, live-verification.json, server-verification.json, live-browser.json sowie Screenshots.
- Live: https://quint-games.de/hefte/tabea/tag-15/lernheft/#k17 ; ebenso ingo und carmen. PDF, Originalfolien und alle Branchen-Missionen sind erreichbar. Es wurden keine externen Plugin-Dienste eingerichtet oder Konten verbunden.
