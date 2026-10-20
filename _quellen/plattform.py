"""Lernplattform quint-games.de/hefte: Personen -> Tage -> Learnings, Lernkarten, Selbsttest, Folien, Arbeitsheft.

    python build.py --web      (ruft build() auf, schreibt ../plattform/public)

Seiten:  /                      Personenwahl (Carmen, Ingo, Tabea)
         /<person>/             Kursuebersicht mit Fortschritt und eigenen Fragen
         /<person>/tag-N/       Tagesseite (Learnings, Lernkarten, Selbsttest, Folien, Woerter, Arbeitsheft)
         /<person>/aufgaben/    Aufgabengenerator ueber alle Tage (je Tag zusaetzlich als Reiter "Aufgaben")
         /<person>/tag-N/heft/  Arbeitsheft zum Ausfuellen (Learnings am Ende, einzeln als PDF)
         /<person>/tag-N/lernblatt/ und /<person>/lernblatt/   Learnings als Druckblatt (Quelle fuer den PDF-Export)
         /dozent/               Fragen der Teilnehmenden ("Unklar?"), Login mit Passwort aus der Server-.env
Alte Tag-3-Hefte vom Vormittag bleiben unter /tag-3/<slug>/ erreichbar (gespeicherte Antworten haengen an ihrer Adresse).
"""
import html as H
import json
import os
import re
import shutil

import hashlib

import aufgaben
import build as B
import kurs
import lernheft
import lerntraining
import einfach_tag12
import einfach_tag13
import datenschutzwerkstatt
import einfach_tag14
import einfach_tag15
from reihe1618.build import render_simple as workshop_simple
import observabilitywerkstatt
import demowerkstatt

WEB_OUT = os.path.join(B.OUT, 'plattform', 'public')
BASE = '/hefte'
FOLIEN = json.load(open(os.path.join(B.HERE, 'folien.json'), encoding='utf-8'))
LEGACY = {  # Tag-3-Hefte vom Vormittag (30.09.) - Antworten liegen im Browser unter diesen Kennungen
    'ingo': ('tag-3/druck-vertrieb', 'Druck & Vertrieb', 'Langdock_Tag3_LLMs-unter-der-Lupe_A_Druck-und-Vertrieb.pdf'),
    'carmen': ('tag-3/teamleitung-business-website', 'Teamleitung, Business & Website', 'Langdock_Tag3_LLMs-unter-der-Lupe_B_Teamleitung-Business-Website.pdf'),
    'tabea': ('tag-3/video-design-creative', 'Video, Design & Creative', 'Langdock_Tag3_LLMs-unter-der-Lupe_C_Video-Design-Creative.pdf'),
}
PX_ICON = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
           '<rect x="5" y="8" width="38" height="32" rx="5"/><path d="M13 19l6 5-6 5M23 30h11"/></svg>')
LH_ICON = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"><path d="M5 10h14a5 5 0 0 1 5 5v25a4 4 0 0 0-4-4H5z"/><path d="M43 10H29a5 5 0 0 0-5 5v25a4 4 0 0 1 4-4h15z"/></svg>'
UEBUNG = {3: ('Prompt-Labor', 'https://prompt.veluna-labs.de/'), 4: ('RAG Rescue', 'https://rag.veluna-labs.de/'),
          5: ('Prompt-Labor · Deep Research', 'https://prompt.veluna-labs.de/#/deep-research'),
          6: ('Prompt-Labor', 'https://prompt.veluna-labs.de/'), 7: ('Prompt-Labor', 'https://prompt.veluna-labs.de/')}
# Personen-Material je Tag (Dateien in public/material/tag-N/)
MATERIAL = {4: {'alle': [('SalesFlow_Uebungsdokumente.zip', 'Alle SalesFlow-Dokumente (ZIP)', 'die fünf Dokumente für Aufgabe 2 und 3'),
                         ('01_SalesFlow_Preisliste_Juli-2026.pdf', '01 Preisliste Juli 2026', 'aktuell, freigegeben'),
                         ('02_SalesFlow_Rabattregeln_Geschaeftskunden.pdf', '02 Rabattregeln für Geschäftskunden', 'aktuell, freigegeben'),
                         ('03_SalesFlow_Vertragsbedingungen_Professional.pdf', '03 Vertragsbedingungen Professional', 'aktuell, freigegeben'),
                         ('04_SalesFlow_Preisliste_Dezember-2025.pdf', '04 Preisliste Dezember 2025', 'alt – für Aufgabe 3'),
                         ('05_SalesFlow_Broschuere_Jede-Systemlandschaft.pdf', '05 Broschüre „Für jede Systemlandschaft“', 'Werbung – für Aufgabe 3')],
                 'ingo': [('06_Druckhaus-Lindner_Preisliste-2026.pdf', 'Preisliste Druckhaus Lindner 2026', 'für Zusatzaufgabe 3')],
                 'carmen': [('07_Agentur-Nordlicht_Leistungen-2026.pdf', 'Leistungen Agentur Nordlicht 2026', 'für Zusatzaufgabe 3')],
                 'tabea': [('08_Cafe-Morgenrot_Markenregeln.pdf', 'Markenregeln Café Morgenrot', 'für Zusatzaufgabe 3')]}}


def iso(datum):
    d, m, y = datum.split('.')
    return f'{y}-{m}-{d}'
esc = B.esc


def write(rel, text):
    path = os.path.join(WEB_OUT, *rel.split('/'))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def icon(pid):
    return B.ICONS[kurs.PERSONEN[pid]['profil']]


# ---------------------------------------------------------------- Rahmen der Plattform-Seiten
def page(title, body, *, person='', tag='', kind='', crumbs='', scripts=('kurs.js',), desc=''):
    attrs = f' data-page="{kind}"' + (f' data-person="{person}"' if person else '') + (f' data-tag="{tag}"' if tag else '')
    js = ''.join(f'<script src="{BASE}/assets/{s}" defer></script>' for s in ('app.js',) + tuple(scripts))
    return f'''<!doctype html>
<html lang="de"{attrs}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(title)}</title>
{f'<meta name="description" content="{esc(desc)}">' if desc else ''}
<link rel="icon" href="{BASE}/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{BASE}/assets/app.css">
<link rel="stylesheet" href="{BASE}/assets/kurs.css">
<link rel="stylesheet" href="{BASE}/assets/lerntraining.css">
<link rel="stylesheet" href="{BASE}/assets/demos.css">
{'<link rel="stylesheet" href="/hefte/assets/privacy.css">' if tag == 13 else '<link rel="stylesheet" href="/hefte/assets/observability.css">' if tag == 14 else ''}
{js}
</head>
<body class="kurs">
<a class="skip" href="#main">Zum Inhalt springen</a>
<header class="top"><div class="top-in">
  <a class="top-brand" href="{BASE}/"><img src="{BASE}/assets/futureway_logo.png" alt="Futureway KI Institut" width="132" height="53"></a>
  <nav class="crumbs" aria-label="Brotkrumen">{crumbs}</nav>
  <div class="top-right"><span id="dz-slot"></span>{f'<a class="top-switch" href="{BASE}/?wechseln=1">Person wechseln</a>' if person else ''}</div>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap foot-in">
  <span>Futureway KI Institut · Kurs „KI Automations Spezialist“ · Praxisblock Langdock</span>
  <span><a href="https://quint-marketplace.de/impressum">Impressum</a> · <a href="https://quint-marketplace.de/datenschutz">Datenschutz</a> · <a href="{BASE}/dozent/">Für die Schulungsleitung</a></span>
</div></footer>
</body>
</html>
'''


def nowrap(text):
    """Woerter mit Bindestrich (KI-Anfrage, KI-Modell) nicht am Bindestrich umbrechen."""
    return re.sub(r'(\S+-\S+)', lambda m: f'<span class="nw">{m.group(1)}</span>', esc(text))


def crumb(*parts):
    out = []
    for i, (label, href) in enumerate(parts):
        last = i == len(parts) - 1
        out.append(f'<span aria-current="page">{esc(label)}</span>' if last or not href else f'<a href="{href}">{esc(label)}</a>')
    return '<span class="sep">/</span>'.join(out)


# ---------------------------------------------------------------- Aufgabengenerator (Daten: aufgaben.py -> assets/aufgaben.json)
AUFG_SRC = f'{BASE}/assets/aufgaben.json'
AUFG_VER = '0'  # wird in build() aus dem Inhalt gesetzt
AUFG_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true">'
             '<rect x="3.5" y="3.5" width="17" height="17" rx="4"/><circle cx="8.5" cy="8.5" r="1.3" fill="currentColor"/>'
             '<circle cx="15.5" cy="15.5" r="1.3" fill="currentColor"/><circle cx="15.5" cy="8.5" r="1.3" fill="currentColor"/>'
             '<circle cx="8.5" cy="15.5" r="1.3" fill="currentColor"/><circle cx="12" cy="12" r="1.3" fill="currentColor"/></svg>')


def aufg_widget(n=None):
    """Steuerung + Karte. n = Tagesseite (Reiter), None = alle Tage mit Tag-Auswahl."""
    if n is None:
        days = ''.join(f'<label><input type="checkbox" value="{d}" checked> Tag {d}</label>' for d in kurs.TAGE)
        extra = f'<fieldset class="aufg-days"><legend>Aus welchen Tagen?</legend>{days}</fieldset>'
    else:
        extra = ('<label class="aufg-chk"><input type="checkbox" class="aufg-frueher"> auch Aufgaben aus früheren Tagen</label>'
                 if n > min(kurs.TAGE) else '')
    return f'''<div class="aufg" data-aufg data-src="{AUFG_SRC}?v={AUFG_VER}"{f' data-tag="{n}"' if n else ''}>
  <div class="aufg-mode" role="group" aria-label="Art der Aufgaben">
    <button type="button" data-mode="kurz" aria-pressed="true"><b>Kurzaufgaben</b><span>5–10 Minuten, ein Gedanke</span></button>
    <button type="button" data-mode="deep" aria-pressed="false"><b>Deep Learn</b><span>1 Stunde, 5 Etappen, alles in Langdock</span></button>
  </div>
  <div class="aufg-ctl">
    <button class="btn primary aufg-roll" type="button">Neue Aufgabe würfeln</button>
    <label class="sel">Bereich<select class="aufg-bereich"><option value="mein">Mein Bereich</option><option value="druck">Druck &amp; Vertrieb</option><option value="web">Business &amp; Website</option><option value="video">Video &amp; Design</option><option value="alle">Gemischt</option></select></label>
    <label class="sel">Dauer<select class="aufg-dauer"><option value="">egal</option><option value="5">etwa 5 Minuten</option><option value="10">etwa 10 Minuten</option></select></label>
    {extra}
  </div>
  <p class="aufg-stat" aria-live="polite"></p>
  <article class="aufg-card" aria-live="polite"><noscript>Der Aufgabengenerator braucht JavaScript.</noscript></article>
  <p class="aufg-note">Alle Firmen, Namen und Zahlen sind ausgedacht. Die Prompts in Langdock in einen neuen Chat kopieren – der Fortschritt bleibt nur in diesem Browser.</p>
</div>'''


def aufgaben_page(pid):
    p = kurs.PERSONEN[pid]
    body = f'''<section class="hero wrap slim">
  <p class="kicker">Freiwillig · aus dem Stoff aller Kurstage</p>
  <h1>Aufgabengenerator</h1>
  <p class="lead">Praxisnahe Aufgaben für Langdock – jedes Mal neu gemischt, passend zum eigenen Bereich. Kurzaufgaben dauern 5–10 Minuten, Deep-Learn-Aufgaben eine Stunde mit fünf Etappen und einem fertigen Ergebnis. Es geht nicht um Fachbegriffe, sondern darum, wie ein guter Prompt aussieht und was er verändert.</p>
</section>
<section class="wrap">
{aufg_widget()}
</section>'''
    return page(f'Aufgabengenerator – {p["name"]}', body, person=pid, kind='aufgaben', scripts=('kurs.js', 'aufgaben.js'),
                crumbs=crumb(('Lernplattform', f'{BASE}/'), (p['name'], f'{BASE}/{pid}/'), ('Aufgaben', '')))


# ---------------------------------------------------------------- Startseite: Personenwahl
def index_page():
    cards = []
    for pid in kurs.REIHENFOLGE:
        p = kurs.PERSONEN[pid]
        cards.append(f'''<a class="pcard" href="{BASE}/{pid}/" data-pick="{pid}">
  <span class="pc-ico">{icon(pid)}</span>
  <span class="pc-name">{esc(p["name"])}</span>
  <span class="pc-fach">{esc(p["fach"])}{" · arbeitet am Mac" if p["mac"] else ""}</span>
  <span class="pc-go">Los geht’s <span aria-hidden="true">→</span></span>
</a>''')
    tage = ''.join(f'<li><b>Tag {n}</b><span>{esc(t["titel"])}</span></li>' for n, t in kurs.TAGE.items())
    body = f'''<section class="hero wrap">
  <p class="kicker">KI Automations Spezialist · Praxisblock Langdock</p>
  <h1>Nachlernen, üben, ausfüllen.</h1>
  <p class="lead">Alles aus dem Kurs an einem Ort: die Learnings jedes Tages, die Folien, Lernkarten, ein kurzer Selbsttest – und die Arbeitshefte zum Ausfüllen. Einfach den eigenen Namen wählen.</p>
  <div class="resume" id="resume" hidden></div>
</section>
<section class="wrap">
  <h2 class="h-sec">Wer lernt hier?</h2>
  <div class="pcards">{"".join(cards)}</div>
  <ol class="tagline" aria-label="Die Kurstage">{tage}</ol>
</section>
<section class="wrap notes">
  <h2 class="h-sec">Gut zu wissen</h2>
  <ul>
    <li><b>Kein Konto nötig.</b> Fortschritt und Heft-Eingaben werden nur in diesem Browser gespeichert. Wer das Gerät wechselt, sichert im Heft über „Mehr → Antworten als Datei sichern“.</li>
    <li><b>Freiwillig üben:</b> Der Aufgabengenerator würfelt kurze Aufgaben aus dem Stoff jedes Tages – mit ausgedachten Firmen aus dem eigenen Bereich.</li>
    <li><b>Etwas unklar?</b> Überall gibt es den Knopf „Unklar?“. Die Frage landet direkt bei der Schulungsleitung – die Antwort erscheint dann hier auf der Seite.</li>
    <li><b>Datenschutz:</b> Gespeichert wird auf dem Server nur, was man selbst als unklar meldet (Vorname, Stelle, eigener Text). Heft-Antworten gehen nur beim PDF-Export kurz an den Server und werden sofort verworfen.</li>
    <li><b>Nur ausgedachte Daten eintragen</b> – wie in allen Übungen.</li>
  </ul>
</section>'''
    return page('Praxisblock Langdock – Lernplattform', body, kind='index',
                crumbs='<span aria-current="page">Lernplattform</span>', desc='Learnings, Folien und Arbeitshefte zum Kurs.')


# ---------------------------------------------------------------- Kursuebersicht je Person
def overview_page(pid):
    p = kurs.PERSONEN[pid]
    stations = []
    for n, t in kurs.TAGE.items():
        stations.append(f'''<li class="station" data-tag="{n}" data-date="{iso(t["datum"])}">
  <div class="st-dot" aria-hidden="true">{n}</div>
  <div class="st-card">
    <p class="st-kicker">Tag {n} · {esc(t["datum"])} <span class="chip-heute" hidden>heute</span></p>
    <h3><a href="{BASE}/{pid}/tag-{n}/">{esc(t["titel"])}</a></h3>
    <p class="st-text">{esc(t["kurz"])}</p>
    <ul class="meter">
      <li><span>Learnings, die sitzen</span><span class="bar"><i data-m="sitzt"></i></span><b data-v="sitzt">0 von {len(t["learnings"])}</b></li>
      <li><span>Selbsttest</span><span class="bar"><i data-m="test"></i></span><b data-v="test">noch offen</b></li>
      {'<li><span>Arbeitsheft</span><span class="bar"><i data-m="heft"></i></span><b data-v="heft">noch nicht begonnen</b></li>' if str(n) in B.TAGE else ''}
    </ul>
    <div class="st-btns"><a class="btn primary" href="{BASE}/{pid}/tag-{n}/">Tag {n} öffnen</a>{f'<a class="btn" href="{BASE}/{pid}/tag-{n}/lernheft/">Lernheft</a>' if t.get("lernheft") else f'<a class="btn" href="{BASE}/{pid}/tag-{n}/heft/">Arbeitsheft</a>'}{f'<a class="btn praxis" href="{BASE}/{pid}/tag-{n}/praxis/">Praxisheft</a>' if t.get("praxisheft") else ''}</div>
  </div>
</li>''')
    body = f'''<section class="hero wrap slim">
  <p class="kicker">{esc(p["fach"])}{" · Mac" if p["mac"] else ""}</p>
  <h1>Hallo {esc(p["name"])}.</h1>
  <p class="lead">{len(kurs.TAGE)} Kurstage, alles zum Nachlernen – oben anfangen oder dort weitermachen, wo man aufgehört hat.</p>
</section>
{lerntraining.overview(pid, kurs.TAGE)}
<section class="wrap">
  <ol class="journey">{"".join(stations)}</ol>
</section>
<section class="wrap">
  <div class="panel-card aufg-teaser">
    <div class="ic">{AUFG_ICON}</div>
    <div>
      <h2 class="h-sec">Aufgabengenerator</h2>
      <p>Freiwillige Übungsaufgaben aus allen Kurstagen – jedes Mal neu gemischt, mit ausgedachten Firmen aus dem Bereich {esc(p["fach"])}. Kurz für zwischendurch oder Deep Learn: eine Stunde, alles in Langdock. <span class="muted" data-aufg-count></span></p>
      <div class="btnrow"><a class="btn primary" href="{BASE}/{pid}/aufgaben/">Aufgabe würfeln</a></div>
    </div>
  </div>
</section>
<section class="wrap two-col">
  <div class="panel-card" id="meine-fragen">
    <h2 class="h-sec">Meine Fragen an die Schulungsleitung</h2>
    <p class="muted" data-empty>Noch nichts als unklar markiert. Überall auf den Seiten gibt es dafür den Knopf „Unklar?“.</p>
    <ul class="qlist"></ul>
  </div>
  <div class="panel-card">
    <h2 class="h-sec">Alles zum Lernen als PDF</h2>
    <p>Die Learnings aller Kurstage auf einem Lernblatt – mit einfacher Erklärung und Folienbild.</p>
    <div class="btnrow"><button class="btn primary" type="button" data-lernblatt="{pid}/alle">Alle Learnings als PDF</button><a class="btn" href="{BASE}/{pid}/lernblatt/">Ansehen</a></div>
  </div>
</section>'''
    return page(f'{p["name"]} – Kursübersicht', body, person=pid, kind='overview', scripts=('kurs.js', 'aufgaben.js', 'lerntraining-core.js', 'lerntraining.js'),
                crumbs=crumb(('Lernplattform', f'{BASE}/'), (p['name'], '')))


# ---------------------------------------------------------------- Tagesseite
def slide_src(tag, n, thumb=False):
    return f'{BASE}/folien/tag-{tag}/{"t" if thumb else ""}{n:02d}.jpg'


def day_page(pid, n):
    p, t = kurs.PERSONEN[pid], kurs.TAGE[n]
    fol = FOLIEN.get(str(n))
    has_fol = bool(fol and fol['n'] > 1)
    bt = B.TAGE.get(str(n))
    lcards = []
    for i, l in enumerate(t['learnings'], 1):
        ref = f't{n}:learning:{l["id"]}'
        label = f'Learning {i}: {l["satz"]}'
        fol_btn = (f'<a class="lc-folie" href="#folien" data-folie="{l["folie"]}">Folie {l["folie"]} ansehen</a>' if l['folie']
                   else f'<span class="lc-quelle">{"Quelle: " + esc(l["quelle"]) if l.get("quelle") else "aus dem Arbeitsheft"}</span>')
        thumb = (f'<button class="lc-thumb" type="button" data-folie="{l["folie"]}" aria-label="Folie {l["folie"]} groß ansehen">'
                 f'<img src="{slide_src(n, l["folie"], True)}" alt="" loading="lazy" width="360" height="{round(360 / fol["ratio"])}"></button>'
                 if l['folie'] else '')
        lcards.append(f'''<li class="lcard" data-lrn="{l["id"]}" id="lrn-{l["id"]}">
  <div class="lc-no">{i:02d}</div>
  <div class="lc-main">
    <h3 class="lc-satz">{esc(l["satz"])}</h3>
    <details class="lc-more"><summary>Nochmal erklärt</summary><p>{esc(l["erklaert"])}</p></details>
    {f'<p class="small"><a href="#einfach-{l["folie"]}">Mit Alltagsbeispiel verstehen →</a></p>' if n in (12,13,14,15,16,17,18) and l['folie'] else ''}
    <div class="lc-actions">
      <button class="chipbtn lc-sitzt" type="button" aria-pressed="false"><span class="ck" aria-hidden="true"></span>Sitzt</button>
      {fol_btn}
      <label class="lc-pick"><input type="checkbox" value="{l["id"]}"> fürs Lernblatt</label>
      <button class="unklar" type="button" data-unklar-ref="{ref}" data-unklar-label="{esc(label)}">Unklar?</button>
    </div>
  </div>
  {thumb}
</li>''')
    karten = ''.join(f'<li><b>{esc(q)}</b><span>{esc(a)}</span></li>' for q, a in t['karten'])
    tests = []
    for i, q in enumerate(t['test'], 1):
        opts = ''.join(f'<li{" data-ok" if j == q["richtig"] else ""}>{esc(o)}</li>' for j, o in enumerate(q['optionen']))
        tests.append(f'<li><p class="tq">{esc(q["frage"])}</p><ol class="to">{opts}</ol><p class="tw"><b>Warum:</b> {esc(q["warum"])}</p></li>')
    words = ''.join(f'<div class="word"><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in t['begriffe'])
    strip = '' if not has_fol else ''.join(f'<a class="v-th" href="{slide_src(n, i)}" data-n="{i}"><img src="{slide_src(n, i, True)}" alt="Folie {i}" loading="lazy" width="360" height="{round(360 / fol["ratio"])}"><span>{i}</span></a>'
                    for i in range(1, fol['n'] + 1))
    fdata = '' if not has_fol else json.dumps({'tag': n, 'n': fol['n'], 'start': t.get('folie_start', 1), 'ratio': fol['ratio'], 'links': {s['n']: s['links'] for s in fol['slides'] if s['links']}}, ensure_ascii=False)
    videos = ''
    if t.get('videos'):
        vs = ''.join(f'''<div class="video" data-yt="{v["id"]}">
  <div class="v-frame"><button class="v-load" type="button"><span class="play" aria-hidden="true"></span><span>Video laden</span><small>Beim Laden verbindet sich die Seite mit YouTube.</small></button></div>
  <div class="v-meta"><b>{esc(v["titel"])}</b><span>{esc(v["dauer"])} Min · englisch, deutsche Untertitel einschaltbar · Folie {v["folie"]}</span><p>{esc(v["text"])}</p>
  <a href="https://www.youtube.com/watch?v={v["id"]}" rel="noopener" target="_blank">Auf YouTube öffnen ↗</a></div>
</div>''' for v in t['videos'])
        videos = f'<h3 class="h-sub">Die Videos aus der Lektion</h3><div class="videos">{vs}</div>'
    # Arbeitsheft-Karte
    extra = ''
    if bt and bt.get('personen'):
        z = B.read(bt['dir'], f'zusatz_{pid}.html')
        titles = re.findall(r'<!--\s*Z(\d)\s*-->\s*<h3>(.*?)</h3>', z, re.S)
        extra = ('<div class="zlist"><p class="zl-h">Zusatzaufgaben für ' + esc(p['fach']) + ' – freiwillig</p><ol>'
                 + ''.join(f'<li>{tt}</li>' for _, tt in titles) + '</ol></div>')
    if n == 3:
        legacy = LEGACY[pid]
        extra += (f'<p class="legacy" data-legacy="{legacy[0]}" hidden>Heute Vormittag schon im ersten Tag-3-Heft gearbeitet? Die Eingaben sind nicht verloren: '
                  f'<a href="{BASE}/{legacy[0]}/">frühere Fassung öffnen</a>.</p>')
    if bt and not bt.get('personen'):
        extra = f'<p class="muted">Das Heft von Tag {n} für {esc(p["fach"])}{" (Mac-Ausgabe)" if (n == 2 and p["mac"]) else ""} – so wie im Kurs, jetzt zum Ausfüllen im Browser.</p>'
    if n in UEBUNG:
        extra += (f'<p class="uebung">Übungsseite für Abschnitt 2: <a href="{UEBUNG[n][1]}" target="_blank" rel="noopener">'
                  f'{UEBUNG[n][0]} · {UEBUNG[n][1].split("//")[1].rstrip("/")} ↗</a></p>')
    mat = ''
    if n in MATERIAL:
        items = MATERIAL[n]['alle'] + MATERIAL[n].get(pid, [])
        mat = (f'<div class="matlist" id="material"><p class="zl-h">Übungsdokumente – alle Angaben ausgedacht</p><ul>'
               + ''.join(f'<li><a href="{BASE}/material/tag-{n}/{f}" download>{esc(label)}</a><span>{esc(note)}</span></li>' for f, label, note in items)
               + f'</ul><p class="muted small">Auch ohne Plattform erreichbar: quint-games.de/hefte/material/tag-{n}</p></div>')
    heft_pdf = heft_pdf_name(pid, n) if bt else ''
    uebung = (f'<p class="uebung">Übungsseite: <a href="{UEBUNG[n][1]}" target="_blank" rel="noopener">'
              f'{UEBUNG[n][0]} · {UEBUNG[n][1].split("//")[1].rstrip("/")} ↗</a></p>') if n in UEBUNG else ''
    hero_heft = (f'<a class="btn" href="{BASE}/{pid}/tag-{n}/lernheft/">Lernheft öffnen</a>' if t.get('lernheft')
                 else f'<a class="btn" href="{BASE}/{pid}/tag-{n}/heft/">Arbeitsheft öffnen</a>')
    praxis_card = ''
    if t.get('praxisheft'):
        pcfg = lernheft.HEFTE[t['praxisheft']]
        hero_heft += (f'<a class="btn praxis" href="{BASE}/{pid}/tag-{n}/praxis/"><span class="px-dot" aria-hidden="true"></span>'
                      f'Praxisheft: selbst ausprobieren</a>')
        praxis_card = f'''  <div class="heftcard pxcard">
    <div class="hc-ico">{PX_ICON}</div>
    <div class="hc-main">
      <p class="kicker">Praxisheft Tag {n} · zum Mitmachen</p>
      <h2>{esc(pcfg["kurz"])}</h2>
      <p>Echte, kostenlose APIs im Browser abfragen, alle Methoden mit Hoppscotch durchspielen, Statuscodes erleben – und den ersten MCP-Server in Langdock verbinden und testen. Mit geprüften Listen kostenloser MCP-Server und APIs. Jede Adresse und jeder Prompt mit „Kopieren“-Knopf.</p>
      <div class="px-mini" aria-hidden="true"><span>$ GET api.open-meteo.com/v1/forecast …</span><span class="ok">→ 200 OK</span><span>$ Langdock → Integrationen → MCP</span><span class="ok">→ Verbindung ok · 3 Werkzeuge</span></div>
      <ol class="lhtoc">{''.join(f'<li><a href="{BASE}/{pid}/tag-{n}/praxis/#k{k}">{esc(tt)}</a></li>' for k, tt in sorted(pcfg["titles"].items()))}</ol>
      <div class="btnrow"><a class="btn praxis" href="{BASE}/{pid}/tag-{n}/praxis/">Praxisheft öffnen</a><a class="btn" href="{BASE}/pdf/{pcfg["pdf"]}" download>Als PDF herunterladen</a></div>
    </div>
  </div>'''
    lernheft_card = ''
    if t.get('lernheft'):
        lh_titles = lernheft.toc_titles(n)
        lh_ueb = 'uebungen' in lernheft.HEFTE[n]
        lh_more = (f'<p class="muted small">Das Übungsheft mit allen Aufgaben gibt es weiterhin: <a href="{BASE}/{pid}/tag-{n}/heft/">Arbeitsheft öffnen</a>.</p>'
                   if bt else '')
        lernheft_card = f'''  <div class="heftcard lhcard">
    <div class="hc-ico">{LH_ICON}</div>
    <div class="hc-main">
      <p class="kicker">Lernheft Tag {n} · zum Lesen und Merken</p>
      <h2>{esc(t["titel"])}</h2>
      <p>{'Teil der fortlaufenden Werkstattreihe vom 20. bis 22. Oktober. Mit aktuellen Anleitungen, Branchen-Missionen, Mitmach-Simulation, Starterpaket und zugeordneten Originalfolien.' if n in (16,17,18) else '28 Originalfolien, ein aktueller Vergleich von Antigravity, Codex und Claude Code sowie sechs Branchen-Missionen. Dazu Plugins, MCP, Selbstchecks und Originalfolien zum Nachsehen.' if n == 15 else 'Alle 74 Folien als kurze Begleitung mit vollständigen Einzelheiten, Beispielen und je einer Merkfrage. Man kann direkt zum gewünschten Gedanken springen.' if n == 13 else 'Alle acht Folien verständlich begleitet, mit Beispielen, Merkfragen und einer praktischen Anleitung zur Spurensuche. Ergänzungen und Voraussetzungen sind markiert.' if n == 14 else f'Die ganze Lektion in {len(lh_titles) - lh_ueb} kurzen Kapiteln – eine Seite pro Gedanke, mit Bildern, Merksätzen, der Lektion auf einer Seite und zwölf Merkfragen.'} Kein Stift nötig: Geübt wird gemeinsam im Kurs.{' Dazu freiwillige Übungen für Langdock – Prompt kopieren, ausprobieren, vergleichen.' if lh_ueb else ''}</p>
      <ol class="lhtoc">{''.join(f'<li><a href="{BASE}/{pid}/tag-{n}/lernheft/#k{k}">{esc(tt)}</a></li>' for k, tt in lh_titles)}</ol>
      <div class="btnrow"><a class="btn primary" href="{BASE}/{pid}/tag-{n}/lernheft/">Lernheft lesen</a><a class="btn" href="{BASE}/pdf/{t["lernheft"]}" download>Als PDF herunterladen</a></div>
      {uebung}
      {mat}
      {lh_more}
    </div>
  </div>'''
        mat = ''
    folien_sec = f'''<section class="tpanel wrap" id="folien" role="tabpanel" aria-label="Folien">
  <div class="panel-head"><div><h2>Die Folien</h2><p>Alle {fol["n"] if has_fol else 0} Folien der Lektion.{f' Heute geht es ab Folie {t["folie_start"]} weiter – die Ansicht startet dort.' if t.get('folie_start', 1) > 1 else ''} Blättern mit den Pfeilen, per Wischen oder mit den Pfeiltasten.</p></div>
    <div class="btnrow"><a class="btn" href="{BASE}/folien/tag-{n}/Folien_Tag{n}.pdf" download>Folien als PDF</a></div></div>
  <div class="viewer" data-viewer>
    <script type="application/json" class="v-data">{fdata}</script>
    <div class="v-strip">{strip}</div>
  </div>
  {videos}
</section>

''' if has_fol else ''
    body = f'''<section class="hero wrap day">
  <p class="kicker">Tag {n} · {esc(t["datum"])} · {esc(t["unter"])}</p>
  <h1>{nowrap(t["titel"])}</h1>
  <p class="lead">{esc(t["kurz"])}</p>
  <div class="hero-btns"><a class="btn primary" href="#demos" data-tab-go="demos">In der Demo ausprobieren</a>{'<a class="btn" href="#einfach" data-tab-go="einfach">Einfach erklärt</a>' if n in (12,13,14,15,16,17,18) else '<a class="btn" href="#learnings" data-tab-go="learnings">Die Learnings lesen</a>'}<a class="btn" href="#training" data-tab-go="training">5 Minuten trainieren</a>{hero_heft}</div>
  <p class="progress-line" aria-live="polite"><span data-v="sitzt">0 von {len(t["learnings"])}</span> Learnings sitzen · Selbsttest <span data-v="test">noch offen</span>{' · Heft <span data-v="heft">noch nicht begonnen</span>' if bt else ''}</p>
</section>
<div class="tabs-wrap"><nav class="tabs wrap" role="tablist" aria-label="Bereiche von Tag {n}">
  <a role="tab" href="#demos" data-tab="demos">Demos</a>
  {'<a role="tab" href="#einfach" data-tab="einfach">Einfach erklärt</a>' if n in (12,13,14,15,16,17,18) else ''}
  <a role="tab" href="#training" data-tab="training">Trainieren</a>
  <a role="tab" href="#learnings" data-tab="learnings">Learnings</a>
  <a role="tab" href="#karten" data-tab="karten">Lernkarten</a>
  <a role="tab" href="#test" data-tab="test">Selbsttest</a>
  <a role="tab" href="#aufgaben" data-tab="aufgaben">Aufgaben</a>
  {'<a role="tab" href="#folien" data-tab="folien">Folien</a>' if has_fol else ''}
  <a role="tab" href="#woerter" data-tab="woerter">Wörter</a>
  <a role="tab" href="#heft" data-tab="heft">{("Lernheft + Praxis" if t.get("praxisheft") else "Lernheft") if t.get("lernheft") else "Arbeitsheft"}</a>
</nav></div>

{einfach_tag12.render() if n == 12 else einfach_tag13.render() if n == 13 else einfach_tag14.render() if n == 14 else einfach_tag15.render() if n == 15 else workshop_simple(n) if n in (16,17,18) else ''}
{lerntraining.panel(pid, n, kurs.TAGE)}
{datenschutzwerkstatt.panel(pid,n) if n == 13 else observabilitywerkstatt.panel(pid,n) if n == 14 else demowerkstatt.panel(pid, n)}
<section class="tpanel wrap" id="learnings" role="tabpanel" aria-label="Learnings">
  <div class="panel-head">
    <div><h2>Die Learnings von Tag {n}</h2><p>Das Wichtigste in einem Satz – „Nochmal erklärt“ öffnet die einfache Erklärung. Was sitzt, abhaken; was unklar ist, melden.</p></div>
    <div class="btnrow">
      <button class="btn ghost" type="button" data-act="expand">Alle aufklappen</button>
      <button class="btn" type="button" data-lernblatt="{pid}/tag-{n}">Alle als PDF</button>
      <button class="btn" type="button" data-lernblatt-sel="{pid}/tag-{n}" disabled>Auswahl als PDF</button>
    </div>
  </div>
  <ol class="lcards">{"".join(lcards)}</ol>
</section>

<section class="tpanel wrap" id="karten" role="tabpanel" aria-label="Lernkarten">
  <div class="panel-head"><div><h2>Lernkarten</h2><p>Frage lesen, Antwort überlegen, Karte umdrehen. Dann ehrlich einsortieren: gewusst oder nochmal.</p></div></div>
  <div class="deck" data-deck>
    <ol class="karten-src">{karten}</ol>
  </div>
</section>

<section class="tpanel wrap" id="test" role="tabpanel" aria-label="Selbsttest">
  <div class="panel-head"><div><h2>Selbsttest</h2><p>{len(t["test"])} kurze Fragen. Nach jeder Antwort steht sofort da, warum. Nichts wird bewertet – es ist nur für einen selbst.</p></div></div>
  <div class="quiz" data-quiz><ol class="test-src">{"".join(tests)}</ol></div>
</section>

<section class="tpanel wrap" id="aufgaben" role="tabpanel" aria-label="Aufgaben">
  <div class="panel-head"><div><h2>Aufgabengenerator</h2><p>Freiwillige Aufgaben zum Stoff von Tag {n} – jedes Mal neu gemischt, mit ausgedachten Firmen aus dem eigenen Bereich. Kurzaufgaben für zwischendurch oder Deep Learn: eine Stunde, eine größere Aufgabe, alles in Langdock.</p></div>
    <div class="btnrow"><a class="btn" href="{BASE}/{pid}/aufgaben/">Aus allen Tagen würfeln</a></div></div>
{aufg_widget(n)}
</section>

{folien_sec}<section class="tpanel wrap" id="woerter" role="tabpanel" aria-label="Wörter">
  <div class="panel-head"><div><h2>Die Wörter des Tages</h2><p>Jedes Fachwort in einem einfachen Satz.</p></div></div>
  <dl class="words">{words}</dl>
</section>

<section class="tpanel wrap" id="heft" role="tabpanel" aria-label="{"Lernheft" if t.get("lernheft") else "Arbeitsheft"}">
{praxis_card}
{lernheft_card}
  <div class="heftcard"{' style="display:none"' if (t.get("lernheft") or not bt) else ''}>
    <div class="hc-ico">{icon(pid)}</div>
    <div class="hc-main">
      <p class="kicker">Arbeitsheft Tag {n}</p>
      <h2>{esc(t["titel"])} – für {esc(p["name"])}</h2>
      {extra}
      {mat}
      <p class="hc-prog"><span data-v="heft">noch nicht begonnen</span></p>
      <div class="btnrow"><a class="btn primary" href="{BASE}/{pid}/tag-{n}/heft/">Heft öffnen und ausfüllen</a><a class="btn" href="{BASE}/pdf/{heft_pdf}" download>Leeres Heft als PDF</a></div>
      <p class="muted small">Am Ende jedes Hefts stehen noch einmal alle Learnings des Tages – einzeln auswählbar und als PDF zum Lernen.</p>
    </div>
  </div>
</section>'''
    return page(f'Tag {n} · {t["titel"]} – {p["name"]}', body, person=pid, tag=n, kind='day', scripts=('kurs.js', 'aufgaben.js', 'lerntraining-core.js', 'lerntraining.js', 'demo-core.js', 'demos.js') + (('privacy-core.js', 'privacy.js') if n == 13 else ('observability-core.js', 'observability.js') if n == 14 else ()),
                crumbs=crumb(('Lernplattform', f'{BASE}/'), (p['name'], f'{BASE}/{pid}/'), (f'Tag {n}', '')))


def heft_pdf_name(pid, n):
    cfg = B.TAGE[str(n)]
    for key, src, pdf, label, hp in B.hefte_of(str(n)):
        if hp == pid:
            return pdf
    raise KeyError(pid)


# ---------------------------------------------------------------- Arbeitsheft (Web-Fassung)
def heft_page(pid, n, manifest):
    tag = str(n)
    cfg = B.TAGE[tag]
    p, t = kurs.PERSONEN[pid], kurs.TAGE[n]
    key, src, pdf, label, _ = next(h for h in B.hefte_of(tag) if h[4] == pid)
    hid = f'{pid}/tag-{n}'
    footer = H.unescape(label).replace('\xa0', ' ')
    footer = 'KI Automations Spezialist  ·  Praxisblock Langdock  ·  ' + re.sub(r'\s+·\s+', '  ·  ', footer)
    pdfname = f'Tag{n}_{p["name"]}'
    head = (f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<meta name="robots" content="noindex, nofollow">'
            f'<meta name="heft-id" content="{hid}"><meta name="heft-file" content="{pdfname}">'
            f'<link rel="icon" href="{BASE}/assets/favicon.svg" type="image/svg+xml">'
            f'<link rel="stylesheet" href="{BASE}/assets/style.css">'
            f'<link rel="stylesheet" href="{BASE}/assets/web.css">'
            f'<link rel="stylesheet" href="{BASE}/assets/app.css">'
            f'<style>@page {{ size: A4; margin: 14mm 16mm 17mm 16mm;'
            f' @bottom-left {{ content: "{footer}"; font-family: Archivo, sans-serif; font-size: 7.5pt; color: #6b6f73; }}'
            f' @bottom-right {{ content: "Seite " counter(page) " von " counter(pages); font-family: Archivo, sans-serif; font-size: 7.5pt; color: #6b6f73; }} }}'
            f' @page :first {{ @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}</style>'
            f'<script src="{BASE}/assets/hefte.js" defer></script>'
            f'<script src="{BASE}/assets/app.js" defer></script>')
    html = B.compose(cfg, src, head, f'{BASE}/assets/futureway_logo.png', tag, pid if cfg.get('personen') else None)
    mac = n == 2 and p['mac']
    bar = (f'<header class="webbar">'
           f'<a class="wb-back" href="{BASE}/{pid}/tag-{n}/">&larr; Tag {n}</a>'
           f'<div class="wb-title"><b>Arbeitsheft Tag {n} · {esc(t["titel"])}</b><span>{esc(p["name"])} · {esc(p["fach"])}{" · Mac" if mac else ""}</span></div>'
           f'<div class="wb-status" id="wb-status" aria-live="polite">Noch nichts eingetragen</div>'
           f'<div class="wb-actions"><span id="dz-slot"></span><button type="button" id="wb-pdf" class="wb-primary">PDF herunterladen</button>'
           f'<details class="wb-more"><summary>Mehr</summary><div class="wb-menu">'
           f'<a href="#lrn-anchor" id="wb-lrn">Zu den Learnings</a>'
           f'<button type="button" id="wb-export">Antworten als Datei sichern</button>'
           f'<label class="wb-file">Antworten aus Datei laden<input type="file" id="wb-import" accept=".json,application/json"></label>'
           f'<a href="{BASE}/pdf/{pdf}" download>Leeres Heft als PDF (zum Ausdrucken)</a>'
           f'<button type="button" id="wb-print">Drucken</button>'
           f'<button type="button" id="wb-reset" class="wb-danger">Alle Eingaben löschen</button>'
           f'</div></details></div></header>'
           f'<p class="wb-hint">In Felder und Linien tippen, Kästchen anklicken – alles wird automatisch in diesem Browser gespeichert. '
           f'Etwas unklar? Bei jedem Schritt gibt es den Knopf „Unklar?“ – die Schulungsleitung sieht es sofort.</p>')
    html = html.replace('<body>', '<body class="web">\n' + bar, 1)
    html = html.replace('<section class="section lrn-section"', '<span id="lrn-anchor"></span><section class="section lrn-section"', 1)
    html = html.replace('<html lang="de">', f'<html lang="de" data-heft="{hid}" data-person="{pid}" data-tag="{n}" data-page="heft">', 1)
    write(f'{pid}/tag-{n}/heft/index.html', html)
    manifest['hefte'][hid] = {'file': pdfname, 'name': f'{p["name"]} · Tag {n}', 'path': f'{hid}/heft/'}
    return pdf


# ---------------------------------------------------------------- Lernblatt (Druckfassung der Learnings)
def lernblatt_page(pid, tage, manifest):
    p = kurs.PERSONEN[pid]
    alle = len(tage) > 1
    key = f'{pid}/alle' if alle else f'{pid}/tag-{tage[0]}'
    rel = f'{pid}/lernblatt/index.html' if alle else f'{pid}/tag-{tage[0]}/lernblatt/index.html'
    title = 'Learnings aller Kurstage' if alle else f'Learnings Tag {tage[0]} · {kurs.TAGE[tage[0]]["titel"]}'
    file = f'Learnings_{"alle_Tage" if alle else "Tag" + str(tage[0])}_{p["name"]}'
    footer = f'KI Automations Spezialist  ·  Praxisblock Langdock  ·  {title}  ·  {p["name"]}'
    secs = ''.join(B.learnings_html(n, thumbs=f'{BASE}/folien/tag-{n}/t{{n:02d}}.jpg') for n in tage)
    back = f'{BASE}/{pid}/' if alle else f'{BASE}/{pid}/tag-{tage[0]}/'
    html = f'''<!doctype html>
<html lang="de" data-person="{pid}" data-page="lernblatt" data-lernblatt="{key}"{"" if alle else f' data-tag="{tage[0]}"'}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(title)} – {esc(p["name"])}</title>
<link rel="icon" href="{BASE}/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{BASE}/assets/style.css">
<link rel="stylesheet" href="{BASE}/assets/web.css">
<link rel="stylesheet" href="{BASE}/assets/app.css">
<style>@page {{ size: A4; margin: 14mm 16mm 17mm 16mm;
 @bottom-left {{ content: "{footer}"; font-family: Archivo, sans-serif; font-size: 7.5pt; color: #6b6f73; }}
 @bottom-right {{ content: "Seite " counter(page) " von " counter(pages); font-family: Archivo, sans-serif; font-size: 7.5pt; color: #6b6f73; }} }}</style>
<script src="{BASE}/assets/app.js" defer></script>
</head>
<body class="web lernblatt">
<header class="webbar">
  <a class="wb-back" href="{back}">&larr; Zurück</a>
  <div class="wb-title"><b>{esc(title)}</b><span>Lernblatt für {esc(p["name"])}</span></div>
  <div class="wb-status" id="lb-status"></div>
  <div class="wb-actions"><span id="dz-slot"></span><button type="button" class="wb-primary" data-lernblatt-here="{key}">Als PDF herunterladen</button></div>
</header>
<section class="lb-cover">
  <img class="logo" src="{BASE}/assets/futureway_logo.png" alt="Futureway KI Institut">
  <p class="kicker">KI Automations Spezialist · Praxisblock Langdock · Lernblatt</p>
  <h1>{nowrap(title)}</h1>
  <p class="lb-for">für <b>{esc(p["name"])}</b> · {esc(p["fach"])}</p>
  <p class="lb-sel" hidden></p>
</section>
{secs}
</body>
</html>
'''
    write(rel, html)
    ids = {str(n): [l['id'] for l in kurs.TAGE[n]['learnings']] for n in tage}
    manifest['lernblaetter'][key] = {'file': file, 'ids': ids}


# ---------------------------------------------------------------- Material-Seite je Tag
def material_page(n):
    t = kurs.TAGE[n]
    blocks = [('Für alle', MATERIAL[n]['alle'])] + [(f'Zusatzaufgabe für {kurs.PERSONEN[q]["name"]}', MATERIAL[n][q]) for q in kurs.REIHENFOLGE if q in MATERIAL[n]]
    lists = ''.join(f'<h2 class="h-sec">{esc(h)}</h2><ul class="matgrid">'
                    + ''.join(f'<li><a class="matcard" href="{f}" download><b>{esc(label)}</b><span>{esc(note)}</span><em>{"ZIP" if f.endswith(".zip") else "PDF"} herunterladen</em></a></li>' for f, label, note in items)
                    + '</ul>' for h, items in blocks)
    body = f"""<section class="hero wrap slim">
  <p class="kicker">Tag {n} · {esc(t["unter"])}</p>
  <h1>Übungsdokumente</h1>
  <p class="lead">Alle Firmen, Preise und Regeln in diesen Dokumenten sind ausgedacht. Man lädt sie herunter und baut damit in Langdock eine Wissensbasis.</p>
</section>
<section class="wrap matpage">{lists}</section>"""
    return page(f'Übungsdokumente Tag {n}', body, kind='material', scripts=(),
                crumbs=crumb(('Lernplattform', f'{BASE}/'), (f'Tag {n} · Übungsdokumente', '')))


# ---------------------------------------------------------------- Dozenten-Seite
def dozent_page():
    body = '''<section class="hero wrap slim">
  <p class="kicker">Nur für die Schulungsleitung</p>
  <h1>Fragen aus dem Kurs</h1>
  <p class="lead">Alles, was Carmen, Ingo und Tabea als „unklar“ markiert haben – mit Stelle, Zeit und eigenem Text. Antworten erscheinen bei der Person direkt auf der Seite.</p>
</section>
<section class="wrap" id="dz-app">
  <form class="dz-login panel-card" id="dz-login" hidden>
    <h2 class="h-sec">Anmelden</h2>
    <label for="dz-pw">Passwort</label>
    <input id="dz-pw" type="password" autocomplete="current-password" required>
    <button class="btn primary" type="submit">Anmelden</button>
    <p class="dz-err" role="alert" hidden></p>
  </form>
  <div id="dz-board" hidden>
    <div class="dz-bar">
      <div class="seg" role="group" aria-label="Filter Status">
        <button type="button" data-f="offen" aria-pressed="true">Offen <b data-c="offen">0</b></button>
        <button type="button" data-f="beantwortet" aria-pressed="false">Beantwortet <b data-c="beantwortet">0</b></button>
        <button type="button" data-f="alle" aria-pressed="false">Alle <b data-c="alle">0</b></button>
      </div>
      <div class="seg" role="group" aria-label="Filter Person">
        <button type="button" data-p="" aria-pressed="true">Alle</button>
        <button type="button" data-p="carmen" aria-pressed="false">Carmen</button>
        <button type="button" data-p="ingo" aria-pressed="false">Ingo</button>
        <button type="button" data-p="tabea" aria-pressed="false">Tabea</button>
      </div>
      <div class="dz-right"><button class="btn ghost" type="button" id="dz-notify">Browser-Benachrichtigungen an</button><button class="btn ghost" type="button" id="dz-logout">Abmelden</button></div>
    </div>
    <p class="muted small" id="dz-updated"></p>
    <ul class="dz-list" id="dz-list"></ul>
    <p class="dz-empty muted" id="dz-empty" hidden>Keine Fragen in dieser Ansicht.</p>
  </div>
</section>'''
    return page('Schulungsleitung – Fragen', body, kind='dozent', scripts=('dozent.js',),
                crumbs=crumb(('Lernplattform', f'{BASE}/'), ('Schulungsleitung', '')))


# ---------------------------------------------------------------- Alles bauen
def build():
    os.makedirs(os.path.join(WEB_OUT, 'assets'), exist_ok=True)
    os.makedirs(os.path.join(WEB_OUT, 'pdf'), exist_ok=True)
    shutil.copy(os.path.join(B.HERE, 'style.css'), os.path.join(WEB_OUT, 'assets', 'style.css'))
    shutil.copy(os.path.join(B.HERE, 'futureway_logo.png'), os.path.join(WEB_OUT, 'assets', 'futureway_logo.png'))
    shutil.copy(os.path.join(B.HERE, 'lernheft.css'), os.path.join(WEB_OUT, 'assets', 'lernheft.css'))
    for n, t in kurs.TAGE.items():
        if t.get('lernheft'):
            src = os.path.join(B.HERE, '..', lernheft.HEFTE[n]['out'], t['lernheft'])
            if os.path.exists(src):
                shutil.copy(src, os.path.join(WEB_OUT, 'pdf', t['lernheft']))
            else:
                print('WARNUNG: Lernheft-PDF fehlt:', src)
        if t.get('praxisheft'):
            pcfg = lernheft.HEFTE[t['praxisheft']]
            src = os.path.join(B.HERE, '..', pcfg['out'], pcfg['pdf'])
            if os.path.exists(src):
                shutil.copy(src, os.path.join(WEB_OUT, 'pdf', pcfg['pdf']))
            else:
                print('WARNUNG: Praxisheft-PDF fehlt:', src)
    for old in ('assets/index.js',):
        path = os.path.join(WEB_OUT, *old.split('/'))
        if os.path.exists(path):
            os.remove(path)
    manifest = {'personen': kurs.REIHENFOLGE, 'hefte': {}, 'lernblaetter': {}}
    # alte Tag-3-Hefte vom Vormittag (liegen fertig unter public/tag-3/, werden nicht neu gebaut)
    for pid, (hid, name, pdf) in LEGACY.items():
        if os.path.exists(os.path.join(WEB_OUT, *hid.split('/'), 'index.html')):
            manifest['hefte'][hid] = {'file': 'Tag3_' + hid.split('/')[1] + '_Vormittag', 'name': name + ' (Vormittag)', 'path': hid + '/'}
    fehler = aufgaben.pruefen(kurs.TAGE)
    if fehler:
        raise SystemExit('Aufgabengenerator: ' + '; '.join(fehler))
    global AUFG_VER
    data = json.dumps(aufgaben.export(kurs.TAGE), ensure_ascii=False, separators=(',', ':'))
    AUFG_VER = hashlib.sha1(data.encode('utf-8')).hexdigest()[:10]
    write('assets/aufgaben.json', data)
    write('index.html', index_page())
    write('dozent/index.html', dozent_page())
    for n in MATERIAL:
        write(f'material/tag-{n}/index.html', material_page(n))
    for pid in kurs.REIHENFOLGE:
        write(f'{pid}/index.html', overview_page(pid))
        write(f'{pid}/aufgaben/index.html', aufgaben_page(pid))
        for n in kurs.TAGE:
            write(f'{pid}/tag-{n}/index.html', day_page(pid, n))
            if str(n) in B.TAGE:
                pdf = heft_page(pid, n, manifest)
                final = os.path.join(B.TAGE[str(n)]['out'], pdf)
                if os.path.exists(final):
                    shutil.copy(final, os.path.join(WEB_OUT, 'pdf', pdf))
                else:
                    print('WARNUNG: Druck-PDF fehlt:', final)
            lernblatt_page(pid, [n], manifest)
            if kurs.TAGE[n].get('lernheft'):
                write(f'{pid}/tag-{n}/lernheft/index.html', lernheft.web_page(pid, n))
            if kurs.TAGE[n].get('praxisheft'):
                write(f'{pid}/tag-{n}/praxis/index.html', lernheft.web_page(pid, kurs.TAGE[n]['praxisheft']))
        lernblatt_page(pid, list(kurs.TAGE), manifest)
    with open(os.path.join(WEB_OUT, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print('Plattform:', len(manifest['hefte']), 'Hefte,', len(manifest['lernblaetter']), 'Lernblätter')
