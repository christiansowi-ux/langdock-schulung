"""Modul 2 · Tag 6: Tagesseite (alle Funktionen + Rechen-Labor), Lernheft zum Lesen und PDF-Fassung."""
import json
import re
from pathlib import Path

from ..woche1.bausteine import E
from ..woche1.hub import CONTENT_CSS, HUB_CSS, READ_CSS, PRINT_CSS, FONT_FACES, ASSETS, ROOT, _inline_css
from . import inhalt
from .daten import TAG, LERNHEFT, FOLIEN_PDF, N_FOLIEN
from .praesentation import ADRESSE as PRAES

VERSION = 'tag6-1'

WOCHE2_CSS = '''
.wh .einfach{background:#e8f4f0;border-radius:14px;padding:14px 18px;margin:12px 0}
.wh .einfach .lbl{color:#05614c}.wh .einfach p{margin:0;font-size:17px;line-height:1.5;color:#0f1513}
.wh details.verstehen{border:1px solid #c7e5dc;border-radius:14px;padding:11px 16px;margin:12px 0;background:#fff}
.wh details.verstehen summary{cursor:pointer;font-weight:650;color:#0f1513}
.wh details.verstehen .lbl{color:#05614c;margin-right:6px}
.wh details.verstehen p{margin:8px 0 0}
.wh .ft-liste{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}
.wh .ft-karte{border:1px solid #dfe5e2;border-radius:12px;padding:10px 14px;background:#fff}
.wh .ft-karte b{display:block;color:#0f1513}.wh .ft-karte span{font-size:14px;color:#58615c}
.wh .gw-zeile{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.wh .ok{color:#05614c;font-weight:700}.wh .warn{color:#8a5a00;font-weight:700}
.wh .bw-raster{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:10px}
.wh .bw-karte{border:1px solid #dfe5e2;border-radius:14px;padding:12px;background:#fff;min-width:0}
.wh .bw-zeile{border-top:1px solid #eef1ef;padding-top:8px}
.wh .bw-summe{font-size:16px;margin:8px 0 0}
.wh .mx{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0}
.wh .mx-feld{border-radius:14px;padding:12px 14px;min-height:92px;background:#f4f6f5;border:1px solid #dfe5e2}
.wh .mx-feld b{display:block;color:#0f1513}.wh .mx-feld small{color:#58615c}
.wh .mx-sofort{background:#e2fcf7;border-color:#05dbba}.wh .mx-planen{background:#e8f4f0;border-color:#c7e5dc}
.wh .mx-streichen{background:#fff;border:1px dashed #b42318}
.wh .mx-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.wh .mx-chip{background:#05614c;color:#fff;border-radius:999px;padding:4px 10px;font-size:13.5px;font-weight:700}
.wh .mx-tab p{margin:4px 0;font-size:15px}
.wh .bc-haupt{font-weight:700;color:#05614c}
.wh .bc-raster{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.wh .bc-raster>div{min-width:0}
.wh .bc-zeile{display:grid;grid-template-columns:minmax(0,1fr) 92px 122px;gap:6px;align-items:center;padding:5px 0;border-bottom:1px solid #eef1ef}
.wh .bc-zeile label{font-size:14.5px;font-weight:600;color:#0f1513}.wh .bc-zeile small{font-weight:500;color:#58615c}
.wh .bc-zeile input,.wh .bc-zeile select{width:100%;min-width:0;font:inherit;font-size:14.5px;padding:7px 8px;border:1px solid #c2c8c5;border-radius:9px;background:#fff;color:#0f1513}
.wh .bc-aus{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin:12px 0}
.wh .bc-kachel{border:1px solid #dfe5e2;border-radius:12px;padding:10px 12px;background:#fff}
.wh .bc-kachel b{display:block;font-size:19px;color:#0f1513;font-variant-numeric:tabular-nums}.wh .bc-kachel span{font-size:13px;color:#58615c}
.wh .bc-kachel.gut{background:#e2fcf7;border-color:#05dbba}.wh .bc-kachel.warn{background:#fdf6d6;border-color:#ead777}
.wh .bc-hinweise{margin:6px 0;padding-left:20px}.wh .bc-hinweise li{font-size:14.5px;margin:3px 0;font-weight:600}
.wh .sz-raster{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.wh .sz{border:1px solid #dfe5e2;border-radius:14px;padding:12px;background:#fff;min-width:0}
.wh .sz h4{margin:0 0 8px}.wh .sz small{color:#58615c}.wh .sz-info{font-size:14.5px;color:#58615c}
.wh .sz-k{border:2px solid #05614c}
.wh .sz-aus{display:grid;gap:6px;margin:8px 0}
.wh .sz-kipp{margin-top:12px;padding-top:10px;border-top:1px solid #dfe5e2}
.wh [data-sz-kipp]{font-weight:700}
.wh .ab-raster{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px}
.wh .fr-aus{font-size:16px;margin:4px 0 0}
.wh .steck-bsp .steck-tab td{font-size:14.5px}
@media (max-width:900px){.wh .bw-raster,.wh .sz-raster,.wh .bc-raster{grid-template-columns:1fr}.wh .gw-zeile{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:480px){.wh .bc-zeile{grid-template-columns:1fr 1fr}.wh .bc-zeile label{grid-column:1/-1}}
'''

PRINT_EXTRA = '''
.wh details.verstehen{break-inside:avoid}.wh details.verstehen summary{list-style:none}
.wh .mx-feld{break-inside:avoid}
.wh .teil-kopf{background:#e8f4f0}.wh .teil-t{color:#0f1513!important}.wh .teil-kopf p{color:#2a312e}.wh .teil-b{background:#05614c;color:#fff}
.wh .tab th{background:#073d31}
.pr-cover{background:radial-gradient(160mm 110mm at 90% 0%,rgba(5,219,186,.22),transparent 60%),linear-gradient(180deg,#eef8f4,#fff);color:#0f1513}
.pr-cover img{filter:none}.pr-cover h1 em{color:#05614c}.pr-cover .eyebrow{color:#05614c}.pr-cover p{color:#2a312e}
.pr-cover .pr-meta div{border-color:#c7e5dc;background:#fff}.pr-cover .pr-meta b{color:#0f1513}.pr-cover .pr-meta span{color:#58615c}
'''


def _kapitel(html, *ids):
    return ''.join(re.search(rf'<section class="kapitel [^"]*" id="{cid}">.*?</section>', html, re.S).group(0) for cid in ids)


def _learnings():
    import kurs
    t = kurs.TAGE[TAG]
    out = []
    for i, l in enumerate(t['learnings'], 1):
        f = l['folie']
        label = E(f'Learning {i}: {l["satz"]}')
        out.append(f'''<li class="lcard" data-lrn="{l["id"]}" id="lrn-{l["id"]}">
  <div class="lc-no">{i:02d}</div>
  <div class="lc-main">
    <h3 class="lc-satz">{E(l["satz"])}</h3>
    <details class="lc-more"><summary>Nochmal erklärt</summary><p>{E(l["erklaert"])}</p></details>
    <div class="lc-actions">
      <button class="chipbtn lc-sitzt" type="button" aria-pressed="false"><span class="ck" aria-hidden="true"></span>Sitzt</button>
      <a class="lc-folie" href="#folien" data-folie="{f}">Folie {f} ansehen</a>
      <label class="lc-pick"><input type="checkbox" value="{l["id"]}"> fürs Lernblatt</label>
      <button class="unklar" type="button" data-unklar-ref="t{TAG}:learning:{l["id"]}" data-unklar-label="{label}">Unklar?</button>
    </div>
  </div>
  <button class="lc-thumb" type="button" data-folie="{f}" aria-label="Folie {f} groß ansehen"><img src="/hefte/folien/tag-25/t{f:02d}.jpg" alt="" loading="lazy" width="360" height="203"></button>
</li>''')
    return ''.join(out)


ICON = {
    'labor': '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7h8M8 11h2M12 11h2M16 11h0M8 15h2M12 15h2M16 15v2"/>',
    'praes': '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M12 16v4M8 20h8M9 9l2 2 4-3"/>',
    'vorlagen': '<path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/>',
    'karten': '<rect x="4" y="5" width="12" height="15" rx="2"/><path d="M8 3h10a2 2 0 0 1 2 2v13"/>',
    'training': '<path d="M4 12a8 8 0 0 1 14-5.3L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-14 5.3L4 15"/><path d="M4 20v-5h5"/>',
    'test': '<rect x="4" y="4" width="16" height="16" rx="4"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/>',
    'heft': '<path d="M4 5h6a3 3 0 0 1 3 3v12a2.5 2.5 0 0 0-2.5-2.5H4z"/><path d="M20 5h-6a3 3 0 0 0-3 3v12a2.5 2.5 0 0 1 2.5-2.5H20z"/>'}


def _ico(k):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{ICON[k]}</svg>'


def _start(n_learn):
    schritte = [('1', 'Bewerten', 'Drei Kandidaten bekommen Punkte: 12 Bewertungen mit Begründung.', 'labor', 'b5'), ('2', 'Priorisieren', 'Matrix ausfüllen und einen Haupt-Use-Case festlegen.', 'labor', 'p3'),
                ('3', 'Rechnen', 'Business Case mit Herkunft je Zahl und drei Szenarien.', 'labor', 'c5'), ('4', 'Entscheiden', 'Empfehlung in zwei Sätzen und Abbruchbedingung.', 'labor', 'd2')]
    plan = ''.join(f'<a class="hub-day" href="#{c}" data-tab-go="{tab}" data-jump="{c}"><div class="d-top"><span class="d-wd">Schritt {n}</span></div><h3>{E(t)}</h3><p>{E(x)}</p></a>' for n, t, x, tab, c in schritte)
    tiles = [('labor', 'labor', 'Rechen-Labor', 'Scoring, Matrix, Business Case und Szenarien rechnen automatisch.', ''),
             ('praes', None, 'Folien erklärt', 'Alle Folien mit Erklärungen direkt zu den Begriffen.', ''),
             ('vorlagen', 'vorlagen', '2 Make-Vorlagen', 'Scoring und Business Case in Make, fertig zum Importieren.', ''),
             ('karten', 'karten', 'Lernkarten', f'{{k}} Karten: umdrehen, ehrlich einsortieren.', ''),
             ('training', 'training', 'Trainieren', 'Fünf Fragen, Wiederholung nach 1, 3 und 7 Tagen.', ''),
             ('test', 'test', 'Selbsttest', '{t} Fragen mit sofortiger Erklärung.', '<span class="hub-note">Bestwert: <b data-v="test">noch offen</b></span>')]
    import kurs
    t = kurs.TAGE[TAG]
    kacheln = ''
    for ico, tab, ti, tx, extra in tiles:
        tx = tx.replace('{k}', str(len(t['karten']))).replace('{t}', str(len(t['test'])))
        attr = f'href="#{tab}" data-tab-go="{tab}"' if tab else f'href="{PRAES}" target="_blank" rel="noopener"'
        kacheln += f'<a class="hub-tile" {attr}><span class="t-ico" aria-hidden="true">{_ico(ico)}</span><b>{E(ti)}</b><span>{E(tx)}</span>{extra}</a>'
    return f'''<section class="tpanel wrap" id="start" role="tabpanel" aria-label="Heute">
  <h2 class="hub-h2">Erinnerung an Freitag</h2>
  <div class="wh">{inhalt.freitag_tool(True)}{inhalt.P("Ein Use-Case braucht ein **echtes Problem**, einen **abgrenzbaren KI-Teil** und einen **messbaren Mehrwert**. Am Freitag hast du Zeitfresser gerechnet, Steckbriefe gefüllt, Autonomie-Stufen festgelegt und Ausschlusskriterien geprüft. [[Die ganze Erinnerung steht im Lernheft.]]").replace("[[", '<a href="lernheft/#r1">').replace("]]", "</a>")}</div>
  <h2 class="hub-h2">Dein Weg heute</h2>
  <div class="hub-week hub-week-4">{plan}</div>
  <h2 class="hub-h2">Alles an einem Ort</h2>
  <div class="hub-grid">{kacheln}</div>
  <div class="wh">{inhalt.achtung("Speichern", "Deine Eingaben bleiben nur in diesem Browser auf diesem Gerät. Für ein anderes Gerät im Rechen-Labor unten „Meine Tagesarbeit herunterladen“ nutzen.")}</div>
</section>'''


def render_day(pid):
    import plattform as P
    import kurs
    import lerntraining
    import demowerkstatt
    t = kurs.TAGE[TAG]
    p = kurs.PERSONEN[pid]
    n_learn = len(t['learnings'])
    karten = ''.join(f'<li><b>{E(q)}</b><span>{E(a)}</span></li>' for q, a in t['karten'])
    tests = ''.join(
        f'<li><p class="tq">{E(q["frage"])}</p><ol class="to">' + ''.join(f'<li{" data-ok" if j == q["richtig"] else ""}>{E(o)}</li>' for j, o in enumerate(q['optionen'])) +
        f'</ol><p class="tw"><b>Warum:</b> {E(q["warum"])}</p></li>' for q in t['test'])
    words = ''.join(f'<div class="word"><dt>{E(a)}</dt><dd>{E(b)}</dd></div>' for a, b in t['begriffe'])
    strip = ''.join(f'<a class="v-th" href="/hefte/folien/tag-25/{i:02d}.jpg" data-n="{i}"><img src="/hefte/folien/tag-25/t{i:02d}.jpg" alt="Folie {i}" loading="lazy" width="360" height="203"><span>{i}</span></a>' for i in range(1, N_FOLIEN + 1))
    fdata = json.dumps({'tag': TAG, 'n': N_FOLIEN, 'start': 1, 'ratio': 1.7778, 'links': {}}, ensure_ascii=False)
    heft = inhalt.body(pid, True)
    labor = _kapitel(heft, 'b5', 'p3', 'c5', 'c6', 'c7', 'd2')
    vorlagen = _kapitel(heft, 'm0', 'vorlage-a10', 'vorlage-a11')
    toc = ''.join(f'<li><a href="lernheft/#{tid}">{E(title)}</a></li>' for tid, title, _ in inhalt.TOC)
    body = f'''<section class="hub-hero"><div class="wrap">
  <p class="kicker">Modul 2 · Tag 6 · {E(t["datum"])} · Lektion 3 · {E(p["name"])}</p>
  <h1>Bewerten, rechnen, <em>entscheiden</em>.</h1>
  <p class="lead">{E(t["kurz"])}</p>
  <div class="hero-btns"><a class="btn primary" href="lernheft/">Lernheft lesen</a><a class="btn" href="#labor" data-tab-go="labor">Ins Rechen-Labor</a><a class="btn" href="{PRAES}" target="_blank" rel="noopener">Folien erklärt</a><a class="btn" href="#training" data-tab-go="training">5 Minuten trainieren</a></div>
  <div class="hub-stats" aria-live="polite">
    <div class="hub-stat"><b data-v="sitzt">0 von {n_learn}</b><span>Learnings sitzen</span></div>
    <div class="hub-stat"><b data-v="test">noch offen</b><span>Selbsttest</span></div>
    <div class="hub-stat"><b data-haupt-name>noch offen</b><span>Haupt-Use-Case</span></div>
    <div class="hub-stat"><b data-stat-amort>noch offen</b><span>Amortisation</span></div>
  </div>
</div></section>
<div class="tabs-wrap"><nav class="tabs wrap" role="tablist" aria-label="Bereiche von Tag 6">
  <a role="tab" href="#start" data-tab="start">Heute</a>
  <a role="tab" href="#labor" data-tab="labor">Rechen-Labor</a>
  <a role="tab" href="#vorlagen" data-tab="vorlagen">Make-Vorlagen<span class="tn">2</span></a>
  <a role="tab" href="#demos" data-tab="demos">Demos</a>
  <a role="tab" href="#training" data-tab="training">Trainieren</a>
  <a role="tab" href="#learnings" data-tab="learnings">Learnings</a>
  <a role="tab" href="#karten" data-tab="karten">Lernkarten</a>
  <a role="tab" href="#test" data-tab="test">Selbsttest</a>
  <a role="tab" href="#aufgaben" data-tab="aufgaben">Aufgaben</a>
  <a role="tab" href="#folien" data-tab="folien">Folien</a>
  <a role="tab" href="#woerter" data-tab="woerter">Wörter</a>
  <a role="tab" href="#heft" data-tab="heft">Lernheft</a>
</nav></div>
{_start(n_learn)}
<section class="tpanel wrap" id="labor" role="tabpanel" aria-label="Rechen-Labor">
  <div class="panel-head"><div><h2>Rechen-Labor</h2><p>Die vier Arbeitsaufträge von heute zum Ausfüllen. Alles rechnet automatisch, deine Kandidaten vom Freitag sind schon eingetragen, wenn du denselben Browser nutzt.</p></div>
  <div class="btnrow"><a class="btn" href="lernheft/">Erklärungen im Lernheft</a></div></div>
  <div class="wh">{labor}</div>
</section>
<section class="tpanel wrap" id="vorlagen" role="tabpanel" aria-label="Make-Vorlagen">
  <div class="panel-head"><div><h2>Make-Vorlagen des Tages</h2><p>Die Rechnungen von heute als fertige Make-Szenarien. Die neun Vorlagen der letzten Woche findest du im <a href="/hefte/{pid}/modul-2/tag-5/#vorlagen">Learning Hub von Tag 5</a>.</p></div></div>
  <div class="wh">{vorlagen}</div>
</section>
{demowerkstatt.panel(pid, TAG)}
{lerntraining.panel(pid, TAG, kurs.TAGE)}
<section class="tpanel wrap" id="learnings" role="tabpanel" aria-label="Learnings">
  <div class="panel-head"><div><h2>Die Learnings von Tag 6</h2><p>Das Wichtigste in einem Satz – „Nochmal erklärt“ öffnet die einfache Erklärung. Was sitzt, abhaken; was unklar ist, melden.</p></div>
    <div class="btnrow"><button class="btn ghost" type="button" data-act="expand">Alle aufklappen</button><button class="btn" type="button" data-lernblatt="{pid}/tag-{TAG}">Alle als PDF</button><button class="btn" type="button" data-lernblatt-sel="{pid}/tag-{TAG}" disabled>Auswahl als PDF</button></div></div>
  <ol class="lcards">{_learnings()}</ol>
</section>
<section class="tpanel wrap" id="karten" role="tabpanel" aria-label="Lernkarten">
  <div class="panel-head"><div><h2>Lernkarten</h2><p>{len(t["karten"])} Karten zum heutigen Tag. Frage lesen, Antwort überlegen, Karte umdrehen. Dann ehrlich einsortieren: gewusst oder nochmal.</p></div></div>
  <div class="deck" data-deck><ol class="karten-src">{karten}</ol></div>
</section>
<section class="tpanel wrap" id="test" role="tabpanel" aria-label="Selbsttest">
  <div class="panel-head"><div><h2>Selbsttest</h2><p>{len(t["test"])} kurze Fragen. Nach jeder Antwort steht sofort da, warum. Nichts wird bewertet – es ist nur für dich.</p></div></div>
  <div class="quiz" data-quiz><ol class="test-src">{tests}</ol></div>
</section>
<section class="tpanel wrap" id="aufgaben" role="tabpanel" aria-label="Aufgaben">
  <div class="panel-head"><div><h2>Aufgabengenerator</h2><p>Freiwillige Übungen zum Bewerten und Rechnen – jedes Mal neu gemischt, mit ausgedachten Firmen aus deinem Bereich.</p></div>
    <div class="btnrow"><a class="btn" href="/hefte/{pid}/aufgaben/">Aus allen Tagen würfeln</a></div></div>
{P.aufg_widget(TAG)}
</section>
<section class="tpanel wrap" id="folien" role="tabpanel" aria-label="Folien">
  <div class="panel-head"><div><h2>Die Folien</h2><p>Alle {N_FOLIEN} Folien der Lektion. Blättern mit den Pfeilen, per Wischen oder mit den Pfeiltasten. In der Ansicht „Folien erklärt“ stehen die Erklärungen direkt an den Begriffen.</p></div>
    <div class="btnrow"><a class="btn primary" href="{PRAES}" target="_blank" rel="noopener">Folien erklärt starten</a><a class="btn" href="/hefte/folien/tag-25/{FOLIEN_PDF}" download>Folien als PDF</a></div></div>
  <div class="viewer" data-viewer><script type="application/json" class="v-data">{fdata}</script><div class="v-strip">{strip}</div></div>
</section>
<section class="tpanel wrap" id="woerter" role="tabpanel" aria-label="Wörter">
  <div class="panel-head"><div><h2>Die Wörter des Tages</h2><p>{len(t["begriffe"])} Fachwörter, jedes in einem einfachen Satz.</p></div></div>
  <label class="sr-only" for="w-such">Wörter durchsuchen</label><input class="words-search" id="w-such" type="search" placeholder="Wort suchen, z. B. Amortisation" data-words-search>
  <dl class="words">{words}</dl>
</section>
<section class="tpanel wrap" id="heft" role="tabpanel" aria-label="Lernheft">
  <div class="hub-heft">
    <div class="cover"><div><p class="kicker">Lernheft · Modul 2 · Tag 6</p><h3>Bewerten <em>&amp;</em> rechnen</h3><p>Beginnt mit der Erinnerung an Freitag. Jedes Thema einfach erklärt, mit Alltagsbeispiel und Frage zum Prüfen.</p></div>
      <div class="btnrow"><a class="btn primary" href="lernheft/">Im Browser lesen</a><a class="btn" href="/hefte/pdf/{LERNHEFT}?v={VERSION}" download>PDF herunterladen</a></div></div>
    <div><h3>Inhalt</h3><ol>{toc}</ol></div>
  </div>
</section>'''
    html = P.page(f'Modul 2 · Tag 6 · Bewerten und rechnen – {p["name"]}', body, person=pid, tag=TAG, kind='day',
                  scripts=('kurs.js', 'aufgaben.js', 'lerntraining-core.js', 'lerntraining.js', 'demo-core.js', 'demos.js', f'wochenheft.js?v={VERSION}', f'bewerten.js?v={VERSION}'),
                  crumbs=P.crumb(('Lernplattform', '/hefte/'), (p['name'], f'/hefte/{pid}/#modul-2'), ('Tag 6', '')))
    html = _inline_css(html)
    return html.replace('</head>', f'<style id="wochenhub">{FONT_FACES}{CONTENT_CSS}{HUB_CSS}{WOCHE2_CSS}.hub-week-4{{grid-template-columns:repeat(4,minmax(0,1fr))}}a.hub-day{{text-decoration:none;color:inherit}}.sr-only{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}@media (max-width:900px){{.hub-week-4{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}@media (max-width:560px){{.hub-week-4{{grid-template-columns:1fr}}}}</style>\n</head>', 1)


def _nav():
    out = ''
    for tid, title, items in inhalt.TOC:
        out += f'<p><a href="#{tid}" style="padding:0;color:inherit">{E(title)}</a></p><ol>' + ''.join(f'<li><a href="#{cid}">{E(lbl)}</a></li>' for cid, lbl in items) + '</ol>'
    return out


def render_web(pid):
    names = {'ingo': 'Ingo', 'carmen': 'Carmen', 'tabea': 'Tabea'}
    name = names[pid]
    app_css = (ASSETS / 'app.css').read_text(encoding='utf8').replace('url(fonts/', 'url(/hefte/assets/fonts/')
    return f'''<!doctype html><html lang="de" data-person="{pid}" data-tag="{TAG}" data-page="wochenheft"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>{E(name)} · Lernheft Modul 2 · Tag 6 · Bewerten und rechnen</title><link rel="icon" href="/hefte/assets/favicon.svg">
<style>{app_css}{FONT_FACES}{READ_CSS}{CONTENT_CSS}{WOCHE2_CSS}</style>
<script src="/hefte/assets/app.js" defer></script><script src="/hefte/assets/wochenheft.js?v={VERSION}" defer></script><script src="/hefte/assets/bewerten.js?v={VERSION}" defer></script></head><body>
<a class="skip" href="#main">Zum Inhalt</a>
<header class="rd-top"><div class="rd-top-in"><a href="/hefte/{pid}/modul-2/tag-6/">← Tag 6</a><span>{E(name)} · Lernheft Modul 2 · Tag 6</span><a class="rd-pdf" href="/hefte/pdf/{LERNHEFT}?v={VERSION}" download>PDF</a></div></header>
<section class="rd-cover"><div class="rd-cover-in"><p class="eyebrow">Lernheft · Modul 2 · Tag 6 · Montag, 02.11.2026</p>
<h1>Bewerten, rechnen, <em>entscheiden</em>.</h1>
<p>Heute wird aus deinen drei Kandidaten vom Freitag eine begründete Entscheidung. Erst kurz zurückblicken, dann Schritt für Schritt: Jedes Thema einfach erklärt, mit Beispiel und einer Frage zum Prüfen.</p>
<div class="rd-btns"><a class="btn primary" href="#teil-r">Mit der Erinnerung starten</a><a class="btn" href="#teil-b">Bewerten</a><a class="btn" href="#teil-c">Rechnen</a><a class="btn" href="{PRAES}" target="_blank" rel="noopener">Folien erklärt</a></div></div></section>
<div class="rd-layout"><nav class="rd-nav" aria-label="Inhalt des Lernhefts">{_nav()}</nav>
<main id="main" class="wh"><p class="rd-hint"><b>So nutzt du das Heft:</b> Lies zuerst „Einfach gesagt“. Die Details kannst du danach in Ruhe nachlesen. Die Rechner füllst du direkt hier aus, sie speichern in diesem Browser. Lernkarten, Selbsttest und Training findest du auf der <a href="/hefte/{pid}/modul-2/tag-6/">Tagesseite</a>.</p>
{inhalt.body(pid, True)}</main></div></body></html>'''


def render_print():
    toc = ''.join(f'<div><b>{E(title)}</b><ol>' + ''.join(f'<li>{E(lbl)}</li>' for _, lbl in items) + '</ol></div>' for _, title, items in inhalt.TOC)
    logo = (ROOT / 'plattform/public/assets/futureway_logo.png').as_uri()
    fonts = FONT_FACES.replace('url(/hefte/assets/fonts/', 'url(' + (ASSETS / 'fonts').as_uri() + '/')
    archivo = (ASSETS / 'app.css').read_text(encoding='utf8').split('.nw')[0].replace('url(fonts/', 'url(' + (ASSETS / 'fonts').as_uri() + '/')
    pr = PRINT_CSS.replace('Modul 2 · Wochenheft Woche 1 · Stand 30.10.2026', 'Modul 2 · Tag 6 · Bewerten und rechnen · Stand 02.11.2026')
    text = inhalt.body(None, False).replace('<details class="verstehen">', '<details class="verstehen" open>')
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Lernheft Modul 2 · Tag 6 · Bewerten und rechnen</title>
<style>{archivo}{fonts}{CONTENT_CSS}{WOCHE2_CSS}{pr}{PRINT_EXTRA}</style></head><body>
<section class="pr-cover"><img src="{logo}" alt="Futureway KI Institut"><p class="eyebrow">Lernheft · Modul 2 · Tag 6 · Montag, 02.11.2026</p>
<h1>Bewerten, rechnen,<br><em>entscheiden</em>.</h1>
<p>Aus deinen drei Kandidaten vom Freitag wird eine begründete Entscheidung. Das Heft beginnt mit der Erinnerung an Freitag und erklärt jedes Thema einfach: mit Beispiel und einer Frage zum Prüfen.</p>
<div class="pr-meta"><div><b>29</b><span>Originalfolien begleitet</span></div><div><b>4</b><span>Arbeitsaufträge</span></div><div><b>2</b><span>Make-Vorlagen</span></div><div><b>3</b><span>Beispiele je Bereich</span></div></div></section>
<section class="pr-toc"><h2>Inhalt</h2><div class="t">{toc}</div>
<p style="margin-top:8mm;font-size:9.5pt;color:#5c6360">Online mit Rechnern, Lernkarten, Selbsttest und Training: quint-games.de/hefte → eigener Name → Modul 2 → Tag 6. Alle Beispiele erfunden.</p></section>
<div class="wh">{text}</div></body></html>'''
