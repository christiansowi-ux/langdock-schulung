"""Modul 2 · Tag 7: Tagesseite (alle Funktionen + Ermittlungsakte + Spiele), Lernheft zum Lesen und PDF-Fassung."""
import json

from ..woche1.bausteine import E
from ..woche1.hub import CONTENT_CSS, HUB_CSS, READ_CSS, PRINT_CSS, FONT_FACES, ASSETS, ROOT, _inline_css
from ..woche2.hub import WOCHE2_CSS, PRINT_EXTRA, _kapitel, _ico
from . import inhalt
from .daten import TAG, LERNHEFT, FOLIEN_PDF, N_FOLIEN
from .praesentation import ADRESSE as PRAES
from .spiele import SPIELE

VERSION = 'tag7-1'

TAG7_CSS = '''
.wh .akte{background:#fffdf3;border:1px dashed #d8c566;border-radius:12px;padding:12px 16px;margin:14px 0}
.wh .akte .lbl{color:#7a5d00}.wh .akte p{margin:0}
.wh .kernsatz{margin:18px 0;padding:18px 22px;border-radius:16px;background:#032a21;color:#fff;font-family:"Instrument Serif",Georgia,serif;font-size:clamp(23px,3.1vw,31px);line-height:1.2}
.wh .dialog{display:grid;gap:8px;margin:14px 0}
.wh .dl-z{max-width:82%;justify-self:start;background:#f1f4f2;border-radius:16px 16px 16px 4px;padding:8px 14px}
.wh .dl-z b{display:block;font-size:12.5px;color:#58615c}.wh .dl-z p{margin:0;color:#0f1513}
.wh .dl-du{justify-self:end;background:#e2fcf7;border-radius:16px 16px 4px 16px}.wh .dl-du b{color:#05614c}
.wh .tagebuch{list-style:none;margin:14px 0;padding:0 0 0 20px;border-left:3px dashed #c7e5dc}
.wh .tagebuch li{position:relative;margin:0 0 14px}
.wh .tagebuch li::before{content:"";position:absolute;left:-28px;top:4px;width:13px;height:13px;border-radius:50%;background:#05dbba;box-shadow:0 0 0 3px #fff}
.wh .tb-z{font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#05614c}
.wh .tagebuch p{margin:2px 0 3px;color:#0f1513}.wh .tagebuch em{font-style:normal;font-size:13px;font-weight:700;background:#e2fcf7;color:#05614c;border-radius:999px;padding:2px 10px}
.wh .zeitstrahl{margin:16px 0}
.wh .zs-bar{display:flex;height:46px;border-radius:10px;overflow:hidden;border:1px solid #dfe5e2}
.wh .zs-w{display:flex;align-items:center;justify-content:center;min-width:0;background:repeating-linear-gradient(135deg,#f1f4f2,#f1f4f2 7px,#e4e9e6 7px,#e4e9e6 14px)}
.wh .zs-w i{font-style:normal;font-size:13px;font-weight:700;color:#58615c;white-space:nowrap}
.wh .zs-a{flex:0 0 3px;background:#05614c}
.wh .zs-l{display:flex;flex-wrap:wrap;gap:4px 16px;margin:6px 0 0;font-size:13.5px;color:#58615c}
.wh .zs-l i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:6px;vertical-align:-1px}.wh .zs-pa{background:#dfe5e2}.wh .zs-pb{background:#05614c}
.wh .sp-intro{margin:0 0 10px}
.wh .sp-z{font-size:13px;font-weight:700;color:#58615c;margin:0 0 6px}
.wh .sp-t{font-size:19px;line-height:1.35;font-weight:700;color:#0f1513;margin:0 0 12px}
.wh .sp-opt{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px}
.wh .sp-b{font:inherit;font-weight:650;font-size:15px;line-height:1.3;text-align:left;cursor:pointer;background:#fff;border:1.5px solid #05614c;color:#05614c;border-radius:12px;padding:9px 14px}
.wh .sp-b:hover:not(:disabled){background:#e8f4f0}.wh .sp-b:disabled{cursor:default;border-color:#d5dcd8;color:#8d9692}
.wh .sp-b.richtig,.wh .sp-b.richtig:disabled{background:#e2fcf7;border-color:#05dbba;color:#032a21}.wh .sp-b.falsch,.wh .sp-b.falsch:disabled{background:#fbe6e3;border-color:#d91e0c;color:#8a1408}
.wh .sp-b[aria-pressed=true]{background:#05614c;color:#fff}
.wh .sp-w{margin:0 0 10px;font-weight:600}.wh .sp-erg{font-size:26px;font-weight:800;color:#0f1513;margin:0}.wh .sp-rang{font-size:18px;font-weight:700;color:#05614c;margin:2px 0 6px}
.wh .bingo{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:0 0 10px}
.wh .bg-z{font:inherit;font-size:14.5px;font-weight:650;line-height:1.25;min-height:76px;cursor:pointer;background:#fff;border:1.5px solid #c7e5dc;border-radius:12px;padding:8px;color:#0f1513;text-align:center}
.wh .bg-z:hover{border-color:#05614c}.wh .bg-z[aria-pressed=true]{background:#05614c;border-color:#05614c;color:#fff}
.wh div.bg-z small{display:block;font-weight:500;color:#58615c;margin-top:4px}
.wh .bg-frage{font-weight:700;color:#05614c;min-height:1.5em}
.wh .aufloesung{font-size:13.5px;color:#58615c}
.wh .uhr{display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;margin:0 0 12px;padding:8px 12px;border-radius:12px;background:#f4f6f5}
.wh .uhr-z{font-size:24px;font-variant-numeric:tabular-nums;color:#0f1513;min-width:66px}.wh .uhr-t{flex:1 1 100%;font-weight:600;font-size:14.5px}.wh .uhr-t:empty{display:none}
.wh .uhr-ende{background:#fdf6d6}
.wh .rd-tabs{display:flex;gap:8px;margin:0 0 10px}
.wh .ms-kopf,.wh .ms-zeile{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) 34px;gap:6px;margin:0 0 6px}
.wh .ms-kopf span,.wh .bh-kopf span,.wh .sop-kopf span{font-size:13px;font-weight:700;color:#58615c}
.wh .ms-zeile input,.wh .bh-zeile input,.wh .bh-zeile select,.wh .sop-zeile input,.wh .sop-zeile select,.wh .bh-zeile input{width:100%;min-width:0;font:inherit;font-size:14.5px;padding:7px 8px;border:1px solid #c2c8c5;border-radius:9px;background:#fff;color:#0f1513}
.wh .zeile-weg{font:inherit;width:34px;height:34px;border-radius:9px;border:1px solid #dfe5e2;background:#fff;color:#58615c;cursor:pointer;line-height:1}.wh .zeile-weg:hover{border-color:#d91e0c;color:#d91e0c}
.wh .alarm-liste{list-style:none;margin:10px 0;padding:0}.wh .alarm-liste li{background:#fbe6e3;border-radius:10px;padding:7px 12px;margin:0 0 6px;font-size:14.5px;color:#0f1513}.wh .alarm-liste b{color:#8a1408}
.wh .ms-vorlesen{background:#f4f6f5;border-radius:12px;padding:12px 16px 12px 34px;margin:10px 0}.wh .ms-vorlesen li{margin:4px 0}
.wh .ms-fertig{display:flex;flex-wrap:wrap;gap:6px 18px;margin:10px 0}
.wh .stand{font-weight:600;margin:10px 0 0}.wh .stand:empty{display:none}.wh .stand.ok{color:#05614c}
.wh .stempel{display:inline-block;margin-left:12px;transform:rotate(-5deg);border:2.5px solid #05614c;border-radius:7px;padding:1px 9px;font-size:12.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#05614c}
.wh .sipoc{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}.wh .sipoc .fld{min-width:0;margin:0}.wh .sipoc small{min-height:3em}
.wh .absperr{margin:12px 0;padding:10px;border-radius:12px;background:repeating-linear-gradient(-45deg,#f6cf09,#f6cf09 14px,#0d0d0d 14px,#0d0d0d 28px)}
.wh .absperr p{margin:0;background:#fff;border-radius:8px;padding:8px 12px;color:#0f1513}
.wh .bh-bahnen{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px}.wh .bh-bahnen .fld{margin:0 0 8px;min-width:0}
.wh .bh-kopf,.wh .bh-zeile{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1.2fr) minmax(0,1.2fr) 80px 90px 34px;gap:6px;margin:0 0 6px;align-items:center}
.wh .bh-skizze{overflow-x:auto;margin:12px 0;border:1px solid #dfe5e2;border-radius:12px;background:#fff}.wh .bh-skizze svg{display:block;max-width:none;font-family:Archivo,"Segoe UI",sans-serif}
.wh .bh-leer{margin:0;padding:18px;color:#58615c}.wh .bh-wisch{position:sticky;left:0;margin:0;padding:6px 12px;font-size:13px;color:#58615c}
.wh .bh-was{border-top:1px solid #dfe5e2;margin-top:12px;padding-top:4px}.wh .bh-was-t{font-size:14px;color:#58615c;margin:0 0 8px}.wh .bh-kn{display:flex;flex-wrap:wrap;gap:8px}.wh .bh-was-e{font-weight:700;color:#05614c;margin:10px 0 0}
.wh .bh-zeilen,.wh .sop-zeilen{overflow:hidden;padding:2px}
.wh .sop-kopf,.wh .sop-zeile{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,2fr) minmax(0,1.1fr) minmax(0,1fr) 34px;gap:6px;margin:0 0 6px;align-items:center}
.wh .sop-zeile.warte input{background:#fdf6d6}.wh .sop-w{font-size:13.5px;font-weight:700;color:#7a5d00;padding-left:4px}
.wh .ziel-satz{font-size:18px;font-weight:700;line-height:1.4;color:#0f1513;background:#e2fcf7;border-radius:12px;padding:12px 16px;margin:6px 0 10px}
.wh .ziel-fehlt{list-style:none;margin:0 0 8px;padding:0}.wh .ziel-fehlt li{font-size:14.5px;margin:3px 0}
.wh .scope-raster{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.wh .schutzsatz{background:#f4f6f5;border-radius:10px;padding:8px 12px}
.wh .scope-ann{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.wh .scope-ann .fld{margin:0 0 8px}
.wh .kr-zeile{display:grid;grid-template-columns:minmax(0,1.5fr) repeat(4,minmax(0,1fr));gap:8px;border-bottom:1px solid #eef1ef;padding-top:8px}.wh .kr-zeile .fld{margin:0 0 8px;min-width:0}.wh .kr-zeile .fld>span{font-size:13px}
.wh .akte-liste{list-style:none;margin:0 0 10px;padding:0;columns:2}.wh .akte-liste li{margin:3px 0;color:#58615c}.wh .akte-liste li.ok{color:#05614c;font-weight:700}
.wh .symbole{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin:14px 0}
.wh .sym{border:1px solid #dfe5e2;border-radius:14px;padding:12px;background:#fff}.wh .sym b{display:block;color:#0f1513}.wh .sym small{color:#05614c;font-weight:700}.wh .sym p{margin:6px 0 0;font-size:14px;line-height:1.4}
.wh .sym-i{display:block;height:36px;margin-bottom:8px}.wh .sym-start::before,.wh .sym-ende::before{content:"";display:block;width:30px;height:30px;border-radius:50%;border:1.6px solid #0f1513}.wh .sym-ende::before{border:4.5px solid #05614c}
.wh .sym-task::before{content:"";display:block;width:50px;height:30px;border-radius:7px;border:1.6px solid #0f1513}.wh .sym-raute::before{content:"";display:block;width:23px;height:23px;transform:translate(5px,6px) rotate(45deg);border:1.6px solid #0f1513}
.wh .sym-bahn::before{content:"";display:block;width:64px;height:30px;border:1px solid #58615c;background:linear-gradient(#f1f4f2 50%,#fff 50%)}
.wh .eisberg{margin:12px 0;border-radius:16px;overflow:hidden;border:1px solid #c7e5dc}
.wh .eb-a{background:#fff;padding:12px 16px;text-align:center;color:#0f1513}.wh .eb-a small,.wh .eb-u small{display:block;font-size:13px}
.wh .eb-u{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 16px;background:#032a21;color:#fff;padding:14px 16px}.wh .eb-u b{color:#05dbba}.wh .eb-u small{grid-column:1/-1;color:rgba(255,255,255,.75);text-align:center}
.konfetti{position:fixed;inset:0;z-index:50;overflow:hidden;pointer-events:none}.konfetti i{position:absolute;top:-16px;width:9px;height:14px;border-radius:2px;animation:konf 1.4s ease-in forwards}
@keyframes konf{to{transform:translateY(105vh) rotate(560deg);opacity:.7}}
@media (max-width:900px){.wh .sipoc,.wh .bh-bahnen{grid-template-columns:repeat(2,minmax(0,1fr))}.wh .symbole{grid-template-columns:repeat(2,minmax(0,1fr))}.wh .kr-zeile{grid-template-columns:repeat(2,minmax(0,1fr))}.wh .kr-zeile .fld:first-child{grid-column:1/-1}
.wh .bh-kopf,.wh .sop-kopf{display:none}.wh .bh-zeile{grid-template-columns:repeat(2,minmax(0,1fr));border-bottom:1px solid #eef1ef;padding-bottom:8px}.wh .bh-zeile input:first-child{grid-column:1/-1}
.wh .sop-zeile{grid-template-columns:minmax(0,1fr) 34px;border-bottom:1px solid #eef1ef;padding-bottom:8px}.wh .sop-zeile>*:nth-child(2),.wh .sop-zeile>*:nth-child(3),.wh .sop-zeile>*:nth-child(4){grid-column:1/-1}.wh .sop-zeile>.zeile-weg{grid-row:1;grid-column:2}
.wh .ms-kopf{display:none}.wh .ms-zeile{grid-template-columns:minmax(0,1fr) 34px;border-bottom:1px solid #eef1ef;padding-bottom:8px}.wh .ms-zeile input:nth-child(2),.wh .ms-zeile input:nth-child(3){grid-column:1/-1}.wh .ms-zeile>.zeile-weg{grid-row:1;grid-column:2}}
@media (max-width:560px){.wh .scope-raster,.wh .scope-ann{grid-template-columns:1fr}.wh .akte-liste{columns:1}.wh .eb-u{grid-template-columns:1fr}.wh .sp-t{font-size:17px}.wh .bg-z{font-size:13px;min-height:84px;padding:6px}.wh .sipoc{grid-template-columns:1fr}.wh .sipoc small{min-height:0}.wh .zs-w i{font-size:11px}}
@media (prefers-reduced-motion:reduce){.konfetti{display:none}}
'''

PRINT_T7 = '''
.wh .k-head,.wh .teil-kopf{break-after:avoid}.wh .einfach,.wh .merk,.wh .achtung,.wh .tipp,.wh .korrektur,.wh .beispiel,.wh .tab tr,.wh .karte,.wh .sym,.wh .steck-bsp .steck-h{break-inside:avoid}.wh .steck-h,.wh h3,.wh h4{break-after:avoid}
.wh .dialog,.wh .tagebuch li,.wh .akte,.wh .kernsatz,.wh .zeitstrahl,.wh .bingo,.wh .eisberg,.wh .symbole{break-inside:avoid}
.wh .kernsatz{background:#e8f4f0;color:#032a21}.wh .eb-u{background:#e8f4f0;color:#0f1513}.wh .eb-u b{color:#05614c}.wh .eb-u small{color:#58615c}
.wh .bingo .bg-z{min-height:22mm;font-size:9.6pt}
.bahn-druck th{background:#f4f6f5;color:#0f1513;font-weight:700}
'''


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
  <button class="lc-thumb" type="button" data-folie="{f}" aria-label="Folie {f} groß ansehen"><img src="/hefte/folien/tag-26/t{f:02d}.jpg" alt="" loading="lazy" width="360" height="203"></button>
</li>''')
    return ''.join(out)


def _start():
    schritte = [('1', 'Befragen', 'Partnerinterview in drei Spalten, mit Alarmsatz-Bingo.', 'akte', 'b4'), ('2', 'Skizzieren', 'SIPOC und Ist-Prozess in Bahnen. Wo sind die Tage hin?', 'akte', 'n4'),
                ('3', 'Aufschreiben', 'SOP, den auch eine neue Kollegin versteht.', 'akte', 'n6'), ('4', 'Beweise sichern', 'Zielsatz, Scope und Erfolgskriterien.', 'akte', 'k6')]
    plan = ''.join(f'<a class="hub-day" href="#{c}" data-tab-go="{tab}" data-jump="{c}"><div class="d-top"><span class="d-wd">Auftrag {n}</span></div><h3>{E(t)}</h3><p>{E(x)}</p></a>' for n, t, x, tab, c in schritte)
    tiles = [('labor', 'akte', 'Ermittlungsakte', 'Mitschrift, Bahnen mit Skizze, SOP, Ziel, Scope, Kriterien. Alles speichert sich.', ''),
             ('test', 'spiele', 'Spiele und Bingo', 'Vier Mini-Spiele und die Bingo-Karte fürs Interview.', ''),
             ('praes', None, 'Folien erklärt', 'Alle Folien mit Erklärungen direkt zu den Begriffen.', ''),
             ('vorlagen', 'vorlagen', '3 Make-Vorlagen', 'Zielsatz-Prüfer, Durchlaufzeit-Detektiv, Scope-Tür.', ''),
             ('karten', 'karten', 'Lernkarten', '{k} Karten: umdrehen, ehrlich einsortieren.', ''),
             ('training', 'training', 'Trainieren', 'Fünf Fragen, Wiederholung nach 1, 3 und 7 Tagen.', ''),
             ('test', 'test', 'Selbsttest', '{t} Fragen mit sofortiger Erklärung.', '<span class="hub-note">Bestwert: <b data-v="test">noch offen</b></span>'),
             ('labor', 'aufgaben', 'Aufgaben als Rollenspiel', 'Die KI spielt die schweigsame Kollegin. Du fragst nach.', ''),
             ('heft', 'heft', 'Lernheft', 'Zum Lesen im Browser oder als PDF mit Ausfülltabellen.', '')]
    import kurs
    t = kurs.TAGE[TAG]
    kacheln = ''
    for ico, tab, ti, tx, extra in tiles:
        tx = tx.replace('{k}', str(len(t['karten']))).replace('{t}', str(len(t['test'])))
        attr = f'href="#{tab}" data-tab-go="{tab}"' if tab else f'href="{PRAES}" target="_blank" rel="noopener"'
        kacheln += f'<a class="hub-tile" {attr}><span class="t-ico" aria-hidden="true">{_ico(ico)}</span><b>{E(ti)}</b><span>{E(tx)}</span>{extra}</a>'
    return f'''<section class="tpanel wrap" id="start" role="tabpanel" aria-label="Heute">
  <h2 class="hub-h2">Was bisher geschah</h2>
  <div class="wh">{inhalt.montag_tool(True)}{inhalt.P("Gestern hast du gerechnet, ob sich dein Fall lohnt. Heute prüfst du, ob die Annahmen stimmen. [[Der ganze Rückblick steht im Lernheft.]]").replace("[[", '<a href="lernheft/#r1">').replace("]]", "</a>")}</div>
  <h2 class="hub-h2">Der Fall des Tages: Wo sind die fünf Tage hin?</h2>
  <div class="wh">{inhalt.tagebuch()}{inhalt.zeitstrahl()}{inhalt.achtung("Die wichtigste Regel für Ermittelnde", "**Der einzige Verdächtige ist der Prozess.** Niemand hat etwas falsch gemacht.")}</div>
  <h2 class="hub-h2">Deine vier Aufträge</h2>
  <div class="hub-week hub-week-4">{plan}</div>
  <h2 class="hub-h2">Alles an einem Ort</h2>
  <div class="hub-grid">{kacheln}</div>
  <div class="wh">{inhalt.achtung("Speichern", "Deine Eingaben bleiben nur in diesem Browser auf diesem Gerät. Für ein anderes Gerät in der Ermittlungsakte unten „Meine Akte herunterladen“ nutzen.")}</div>
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
    strip = ''.join(f'<a class="v-th" href="/hefte/folien/tag-26/{i:02d}.jpg" data-n="{i}"><img src="/hefte/folien/tag-26/t{i:02d}.jpg" alt="Folie {i}" loading="lazy" width="360" height="203"><span>{i}</span></a>' for i in range(1, N_FOLIEN + 1))
    fdata = json.dumps({'tag': TAG, 'n': N_FOLIEN, 'start': 1, 'ratio': 1.7778, 'links': {}}, ensure_ascii=False)
    heft = inhalt.body(pid, True)
    akte = _kapitel(heft, 'b4', 'n4', 'n6', 'k6', 'k7')
    vorlagen = _kapitel(heft, 'm0', 'vorlage-a12', 'vorlage-a13', 'vorlage-a14')
    spiele = ''.join(inhalt.spiel_tool(s, True) for s in SPIELE) + inhalt.bingo_tool(True)
    toc = ''.join(f'<li><a href="lernheft/#{tid}">{E(title)}</a></li>' for tid, title, _ in inhalt.TOC)
    body = f'''<section class="hub-hero"><div class="wrap">
  <p class="kicker">Modul 2 · Tag 7 · {E(t["datum"])} · Lektion 4 · {E(p["name"])}</p>
  <h1>Tatort <em>Prozess</em>.</h1>
  <p class="lead">{E(t["kurz"])}</p>
  <div class="hero-btns"><a class="btn primary" href="lernheft/">Lernheft lesen</a><a class="btn" href="#akte" data-tab-go="akte">Zur Ermittlungsakte</a><a class="btn" href="#spiele" data-tab-go="spiele">Spiele und Bingo</a><a class="btn" href="{PRAES}" target="_blank" rel="noopener">Folien erklärt</a></div>
  <div class="hub-stats" aria-live="polite">
    <div class="hub-stat"><b data-v="sitzt">0 von {n_learn}</b><span>Learnings sitzen</span></div>
    <div class="hub-stat"><b data-v="test">noch offen</b><span>Selbsttest</span></div>
    <div class="hub-stat"><b data-stat-verh>noch offen</b><span>Arbeit zu Warten</span></div>
    <div class="hub-stat"><b data-stat-akte>0 von 7</b><span>Teile der Akte</span></div>
  </div>
</div></section>
<div class="tabs-wrap"><nav class="tabs wrap" role="tablist" aria-label="Bereiche von Tag 7">
  <a role="tab" href="#start" data-tab="start">Heute</a>
  <a role="tab" href="#akte" data-tab="akte">Ermittlungsakte</a>
  <a role="tab" href="#spiele" data-tab="spiele">Spiele<span class="tn">5</span></a>
  <a role="tab" href="#vorlagen" data-tab="vorlagen">Make-Vorlagen<span class="tn">3</span></a>
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
{_start()}
<section class="tpanel wrap" id="akte" role="tabpanel" aria-label="Ermittlungsakte">
  <div class="panel-head"><div><h2>Deine Ermittlungsakte</h2><p>Die vier Arbeitsaufträge von heute zum Ausfüllen. Die Teile hängen zusammen: aus der Mitschrift werden Bahnen, aus den Bahnen der SOP und die Durchlaufzeit im Erfolgskriterium.</p></div>
  <div class="btnrow"><a class="btn" href="lernheft/">Erklärungen im Lernheft</a></div></div>
  <div class="wh">{akte}</div>
</section>
<section class="tpanel wrap" id="spiele" role="tabpanel" aria-label="Spiele">
  <div class="panel-head"><div><h2>Spiele und Bingo</h2><p>Vier kurze Runden zum Üben, dazu die Bingo-Karte fürs Interview. Dein Bestwert bleibt in diesem Browser. Am Ende gibt es einen Dienstgrad.</p></div></div>
  <div class="wh">{spiele}</div>
</section>
<section class="tpanel wrap" id="vorlagen" role="tabpanel" aria-label="Make-Vorlagen">
  <div class="panel-head"><div><h2>Make-Vorlagen des Tages</h2><p>Die Regeln von heute als fertige Make-Szenarien. Die Vorlagen von gestern findest du bei <a href="/hefte/{pid}/modul-2/tag-6/#vorlagen">Tag 6</a>, die neun aus der ersten Woche bei <a href="/hefte/{pid}/modul-2/tag-5/#vorlagen">Tag 5</a>.</p></div></div>
  <div class="wh">{vorlagen}</div>
</section>
{demowerkstatt.panel(pid, TAG)}
{lerntraining.panel(pid, TAG, kurs.TAGE)}
<section class="tpanel wrap" id="learnings" role="tabpanel" aria-label="Learnings">
  <div class="panel-head"><div><h2>Die Learnings von Tag 7</h2><p>Das Wichtigste in einem Satz. „Nochmal erklärt“ öffnet die einfache Erklärung. Was sitzt, abhaken; was unklar ist, melden.</p></div>
    <div class="btnrow"><button class="btn ghost" type="button" data-act="expand">Alle aufklappen</button><button class="btn" type="button" data-lernblatt="{pid}/tag-{TAG}">Alle als PDF</button><button class="btn" type="button" data-lernblatt-sel="{pid}/tag-{TAG}" disabled>Auswahl als PDF</button></div></div>
  <ol class="lcards">{_learnings()}</ol>
</section>
<section class="tpanel wrap" id="karten" role="tabpanel" aria-label="Lernkarten">
  <div class="panel-head"><div><h2>Lernkarten</h2><p>{len(t["karten"])} Karten zum heutigen Tag. Frage lesen, Antwort überlegen, Karte umdrehen. Dann ehrlich einsortieren: gewusst oder nochmal.</p></div></div>
  <div class="deck" data-deck><ol class="karten-src">{karten}</ol></div>
</section>
<section class="tpanel wrap" id="test" role="tabpanel" aria-label="Selbsttest">
  <div class="panel-head"><div><h2>Selbsttest</h2><p>{len(t["test"])} kurze Fragen. Nach jeder Antwort steht sofort da, warum. Nichts wird bewertet, es ist nur für dich.</p></div></div>
  <div class="quiz" data-quiz><ol class="test-src">{tests}</ol></div>
</section>
<section class="tpanel wrap" id="aufgaben" role="tabpanel" aria-label="Aufgaben">
  <div class="panel-head"><div><h2>Aufgabengenerator</h2><p>Freiwillige Übungen mit Rollenspiel: Die KI spielt schweigsame Kolleginnen, neue Mitarbeitende und den Fachbereich in Monat drei. Jedes Mal neu gemischt, mit ausgedachten Firmen aus deinem Bereich.</p></div>
    <div class="btnrow"><a class="btn" href="/hefte/{pid}/aufgaben/">Aus allen Tagen würfeln</a></div></div>
{P.aufg_widget(TAG)}
</section>
<section class="tpanel wrap" id="folien" role="tabpanel" aria-label="Folien">
  <div class="panel-head"><div><h2>Die Folien</h2><p>Alle {N_FOLIEN} Folien der Lektion. Blättern mit den Pfeilen, per Wischen oder mit den Pfeiltasten. In der Ansicht „Folien erklärt“ stehen die Erklärungen direkt an den Begriffen.</p></div>
    <div class="btnrow"><a class="btn primary" href="{PRAES}" target="_blank" rel="noopener">Folien erklärt starten</a><a class="btn" href="/hefte/folien/tag-26/{FOLIEN_PDF}" download>Folien als PDF</a></div></div>
  <div class="viewer" data-viewer><script type="application/json" class="v-data">{fdata}</script><div class="v-strip">{strip}</div></div>
</section>
<section class="tpanel wrap" id="woerter" role="tabpanel" aria-label="Wörter">
  <div class="panel-head"><div><h2>Die Wörter des Tages</h2><p>{len(t["begriffe"])} Fachwörter, jedes in einem einfachen Satz.</p></div></div>
  <label class="sr-only" for="w-such">Wörter durchsuchen</label><input class="words-search" id="w-such" type="search" placeholder="Wort suchen, z. B. Durchlaufzeit" data-words-search>
  <dl class="words">{words}</dl>
</section>
<section class="tpanel wrap" id="heft" role="tabpanel" aria-label="Lernheft">
  <div class="hub-heft">
    <div class="cover"><div><p class="kicker">Lernheft · Modul 2 · Tag 7</p><h3>Tatort <em>Prozess</em></h3><p>Beginnt mit dem Rückblick auf Montag. Jedes Thema einfach erklärt, mit Alltagsbeispiel, Dialogen und Spielen.</p></div>
      <div class="btnrow"><a class="btn primary" href="lernheft/">Im Browser lesen</a><a class="btn" href="/hefte/pdf/{LERNHEFT}?v={VERSION}" download>PDF herunterladen</a></div></div>
    <div><h3>Inhalt</h3><ol>{toc}</ol></div>
  </div>
</section>'''
    html = P.page(f'Modul 2 · Tag 7 · Prozess verstehen – {p["name"]}', body, person=pid, tag=TAG, kind='day',
                  scripts=('kurs.js', 'aufgaben.js', 'lerntraining-core.js', 'lerntraining.js', 'demo-core.js', 'demos.js', f'wochenheft.js?v={VERSION}', f'prozess.js?v={VERSION}'),
                  crumbs=P.crumb(('Lernplattform', '/hefte/'), (p['name'], f'/hefte/{pid}/#modul-2'), ('Tag 7', '')))
    html = _inline_css(html)
    return html.replace('</head>', f'<style id="wochenhub">{FONT_FACES}{CONTENT_CSS}{HUB_CSS}{WOCHE2_CSS}{TAG7_CSS}.hub-week-4{{grid-template-columns:repeat(4,minmax(0,1fr))}}a.hub-day{{text-decoration:none;color:inherit}}.sr-only{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}@media (max-width:900px){{.hub-week-4{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}@media (max-width:560px){{.hub-week-4{{grid-template-columns:1fr}}}}</style>\n</head>', 1)


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
<title>{E(name)} · Lernheft Modul 2 · Tag 7 · Prozess verstehen</title><link rel="icon" href="/hefte/assets/favicon.svg">
<style>{app_css}{FONT_FACES}{READ_CSS}{CONTENT_CSS}{WOCHE2_CSS}{TAG7_CSS}</style>
<script src="/hefte/assets/app.js" defer></script><script src="/hefte/assets/wochenheft.js?v={VERSION}" defer></script><script src="/hefte/assets/prozess.js?v={VERSION}" defer></script></head><body>
<a class="skip" href="#main">Zum Inhalt</a>
<header class="rd-top"><div class="rd-top-in"><a href="/hefte/{pid}/modul-2/tag-7/">← Tag 7</a><span>{E(name)} · Lernheft Modul 2 · Tag 7</span><a class="rd-pdf" href="/hefte/pdf/{LERNHEFT}?v={VERSION}" download>PDF</a></div></header>
<section class="rd-cover"><div class="rd-cover-in"><p class="eyebrow">Lernheft · Modul 2 · Tag 7 · Dienstag, 03.11.2026</p>
<h1>Tatort <em>Prozess</em>.</h1>
<p>Eine Rechnung braucht fünf Tage, gearbeitet wird zwölf Minuten daran. Heute findest du heraus, wo die Zeit bleibt: befragen, skizzieren, Beweise sichern. Der einzige Verdächtige ist der Prozess.</p>
<div class="rd-btns"><a class="btn primary" href="#teil-r">Mit dem Rückblick starten</a><a class="btn" href="#teil-s">Zum Fall des Tages</a><a class="btn" href="#teil-b">Zur Befragung</a><a class="btn" href="{PRAES}" target="_blank" rel="noopener">Folien erklärt</a></div></div></section>
<div class="rd-layout"><nav class="rd-nav" aria-label="Inhalt des Lernhefts">{_nav()}</nav>
<main id="main" class="wh"><p class="rd-hint"><b>So nutzt du das Heft:</b> Lies zuerst „Einfach gesagt“. Die Spiele kannst du direkt hier spielen, und die Werkzeuge speichern in diesem Browser. Lernkarten, Selbsttest und Training findest du auf der <a href="/hefte/{pid}/modul-2/tag-7/">Tagesseite</a>.</p>
{inhalt.body(pid, True)}</main></div></body></html>'''


def render_print():
    toc = ''.join(f'<div><b>{E(title)}</b><ol>' + ''.join(f'<li>{E(lbl)}</li>' for _, lbl in items) + '</ol></div>' for _, title, items in inhalt.TOC)
    logo = (ROOT / 'plattform/public/assets/futureway_logo.png').as_uri()
    fonts = FONT_FACES.replace('url(/hefte/assets/fonts/', 'url(' + (ASSETS / 'fonts').as_uri() + '/')
    archivo = (ASSETS / 'app.css').read_text(encoding='utf8').split('.nw')[0].replace('url(fonts/', 'url(' + (ASSETS / 'fonts').as_uri() + '/')
    pr = PRINT_CSS.replace('Modul 2 · Wochenheft Woche 1 · Stand 30.10.2026', 'Modul 2 · Tag 7 · Prozess verstehen · Stand 03.11.2026')
    text = inhalt.body(None, False).replace('<details class="verstehen">', '<details class="verstehen" open>')
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Lernheft Modul 2 · Tag 7 · Prozess verstehen</title>
<style>{archivo}{fonts}{CONTENT_CSS}{WOCHE2_CSS}{TAG7_CSS}{pr}{PRINT_EXTRA}{PRINT_T7}</style></head><body>
<section class="pr-cover"><img src="{logo}" alt="Futureway KI Institut"><p class="eyebrow">Lernheft · Modul 2 · Tag 7 · Dienstag, 03.11.2026</p>
<h1>Tatort<br><em>Prozess</em>.</h1>
<p>Eine Rechnung braucht fünf Tage, gearbeitet wird zwölf Minuten daran. Heute findest du heraus, wo die Zeit bleibt. Das Heft beginnt mit dem Rückblick auf Montag und erklärt jedes Thema einfach: mit Alltagsbeispiel, Dialogen, Spielen zum Abhaken und einer Bingo-Karte.</p>
<div class="pr-meta"><div><b>38</b><span>Originalfolien begleitet</span></div><div><b>4</b><span>Arbeitsaufträge</span></div><div><b>4 + 1</b><span>Spiele und Bingo</span></div><div><b>3</b><span>Make-Vorlagen</span></div></div></section>
<section class="pr-toc"><h2>Inhalt</h2><div class="t">{toc}</div>
<p style="margin-top:8mm;font-size:9.5pt;color:#5c6360">Online mit Skizzen-Werkzeug, Spielen, Lernkarten, Selbsttest und Training: quint-games.de/hefte → eigener Name → Modul 2 → Tag 7. Alle Beispiele erfunden.</p></section>
<div class="wh">{text}</div></body></html>'''
