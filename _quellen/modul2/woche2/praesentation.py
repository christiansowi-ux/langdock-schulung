"""Präsenter-Modus: Folien mit Erklärungen direkt an den Begriffen (Modul 2 · Tag 6).

Sucht jeden Begriff im Original-PDF und legt die Markierung exakt über das Wort auf dem Folienbild.
Fehlt ein Begriff auf der Folie, bricht der Bau ab, damit nichts falsch markiert wird.
Sprechernotizen stehen nur in der Referentenansicht.
"""
import json
from pathlib import Path

import fitz

from .praesentation_daten import ERINNERUNG, FOLIEN

ROOT = Path(__file__).resolve().parents[3]
PUB = ROOT / 'plattform/public'
ADRESSE = '/hefte/praesentation/modul-2/tag-6/'
PDF_HEUTE = PUB / 'folien/tag-25/Folien_Modul2_Tag6_Bewerten-und-Rechnen.pdf'
PDF_FREITAG = PUB / 'folien/tag-24/Folien_Modul2_Tag5_Use-Cases.pdf'
NOTIZEN = Path(__file__).with_name('sprechernotizen.json')
VERSION = 'p3'


def _orte(page, begriffe, kennung):
    w, h = page.rect.width, page.rect.height
    out = []
    for b in begriffe:
        rects = page.search_for(b['s'])
        assert rects, f'Begriff nicht auf der Folie: {kennung}: {b["s"]}'
        n = b.get('n', 1)
        r = rects[n - 1] if len(rects) >= n else rects[0]
        # Bei Treffern über zwei Zeilen die zusammengehörigen Rechtecke vereinen
        wort_treffer = len(b['s'].split()) > 1
        if wort_treffer and len(rects) > 1 and abs(rects[1].x0 - rects[0].x0) < w * .35 and 0 < rects[1].y0 - rects[0].y0 < h * .07 and n == 1:
            r = rects[0] | rects[1]
        out.append(dict(x=round(r.x0 / w * 100, 2), y=round(r.y0 / h * 100, 2), w=round(r.width / w * 100, 2), h=round(r.height / h * 100, 2),
                        t=b['t'], e=b['e'], b=b.get('b', '')))
    return out


def daten():
    heute, freitag = fitz.open(PDF_HEUTE), fitz.open(PDF_FREITAG)
    notizen = json.loads(NOTIZEN.read_text(encoding='utf8'))
    frames = []
    for i, f in enumerate(ERINNERUNG, 1):
        page = freitag[f['seite'] - 1]
        frames.append(dict(id=f'e{i}', bild=f'/hefte/folien/tag-24/{34 + f["seite"]:02d}.jpg', daumen=f'/hefte/folien/tag-24/t{34 + f["seite"]:02d}.jpg', label=f'Erinnerung {i}/{len(ERINNERUNG)}',
                           titel=f['titel'], kern=f['kern'], frage=f.get('frage', ''), hinweis='', live='', notiz='Kurze Wiederholung von Freitag. Nicht neu erklären, nur Erinnerung wecken und die Frage stellen.',
                           orte=_orte(page, f['begriffe'], f'Freitag {f["seite"]}')))
    for n, f in FOLIEN.items():
        page = heute[n - 1]
        frames.append(dict(id=str(n), bild=f'/hefte/folien/tag-25/{n:02d}.jpg', daumen=f'/hefte/folien/tag-25/t{n:02d}.jpg', label=f'Folie {n}/{len(FOLIEN)}',
                           titel=notizen[str(n)]['titel'], kern=f['kern'], frage=f.get('frage', ''), hinweis=f.get('hinweis', ''), live=f.get('live', ''),
                           notiz=notizen[str(n)]['notiz'], orte=_orte(page, f['begriffe'], f'Folie {n}')))
    return frames


CSS = '''
:root{--bg:#f4f6f5;--line:#dfe5e2;--head:#0f1513;--ink:#2a312e;--mut:#58615c;--brand:#05614c;--brand-d:#073d31;--soft:#e8f4f0;--mint:#05dbba;--mintsoft:#e2fcf7;--gold:#fdf6d6;--goldline:#ead777}
*{box-sizing:border-box}html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.45 Archivo,"Segoe UI",system-ui,sans-serif;overflow:hidden;display:flex;flex-direction:column}
button{font:inherit;cursor:pointer}a{color:var(--brand)}
#p-app{flex:1 1 auto;min-height:0;display:flex;flex-direction:column}body.ref #p-app{display:block}
.leiste{flex:0 0 auto;display:flex;align-items:center;gap:8px 12px;flex-wrap:wrap;padding:8px 14px;background:#fff;border-bottom:1px solid var(--line)}
.leiste .pos{font-weight:800;color:var(--head);white-space:nowrap}.leiste .ti{color:var(--mut);flex:1 1 180px;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kn{border:1px solid #c9d2ce;background:#fff;color:var(--head);border-radius:999px;padding:7px 13px;font-weight:650;font-size:14px;white-space:nowrap}
.kn:hover{border-color:var(--brand);color:var(--brand)}.kn[aria-pressed=true]{background:var(--brand);border-color:var(--brand);color:#fff}
.kn.haupt{background:var(--brand);border-color:var(--brand);color:#fff}.kn.haupt:hover{background:#044434;color:#fff}
.buehne{flex:1 1 auto;min-height:0;display:flex;align-items:center;justify-content:center;padding:10px;position:relative}
.folie{position:relative;aspect-ratio:16/9;max-width:100%;width:min(100%,calc((100vh - var(--platz,118px))*16/9));overflow:hidden;background:#fff;border-radius:10px;box-shadow:0 2px 6px rgba(15,21,19,.08),0 18px 44px rgba(3,42,33,.12);container-type:inline-size}
.folie>img{display:block;width:100%;height:100%;object-fit:contain}.folie>img.wechsel{animation:blende .28s ease-out}
@keyframes blende{from{opacity:.25}to{opacity:1}}
body.voll .leiste{position:fixed;z-index:7;top:0;left:0;right:0;transform:translateY(-101%);transition:transform .25s}body.voll.zeigen .leiste{transform:none}body.voll .buehne{padding:0}body.voll .folie{border-radius:0;width:min(100vw,calc(100vh*16/9));box-shadow:none}body.voll .ablauf{display:none}
.mark{position:absolute;z-index:1;padding:0;border:0;background:rgba(5,219,186,.14);border-bottom:.28cqw solid var(--mint);border-radius:.4cqw;transition:background .15s}
.mark:hover,.mark:focus-visible{background:rgba(5,219,186,.32);outline:none}
.mark i{position:absolute;left:-.9cqw;top:-1.1cqw;min-width:1.9cqw;height:1.9cqw;padding:0 .4cqw;border-radius:999px;background:var(--brand);color:#fff;font:800 1.15cqw/1.9cqw Archivo,sans-serif;text-align:center;box-shadow:0 0 0 .14cqw #fff}
.mark.aktiv{z-index:3;background:transparent;border-bottom-color:transparent}
body.aus .mark{display:none}
.mark.neu i{animation:puls 1.6s ease-out 2}
@keyframes puls{0%{box-shadow:0 0 0 .14cqw #fff,0 0 0 .14cqw rgba(5,219,186,.8)}100%{box-shadow:0 0 0 .14cqw #fff,0 0 0 1.6cqw rgba(5,219,186,0)}}
.spot{position:absolute;z-index:2;display:none;border-radius:.6cqw;box-shadow:0 0 0 200vmax rgba(10,24,20,.5);outline:.28cqw solid var(--mint);outline-offset:.2cqw;pointer-events:none;transition:left .35s cubic-bezier(.2,.8,.2,1),top .35s cubic-bezier(.2,.8,.2,1),width .35s cubic-bezier(.2,.8,.2,1),height .35s cubic-bezier(.2,.8,.2,1)}
.spot.an{display:block}
.karte{position:absolute;z-index:4;display:none;width:max(280px,36cqw);max-width:94%;background:#fff;border-radius:max(10px,1.2cqw);padding:max(11px,1.5cqw) max(13px,1.8cqw);box-shadow:0 .6cqw 3cqw rgba(3,42,33,.34);border-top:max(3px,.45cqw) solid var(--mint);font-size:max(13px,1.5cqw);line-height:1.4;animation:rein .22s ease-out}
.karte.an{display:block}
@keyframes rein{from{opacity:0;transform:translateY(.7cqw)}to{opacity:1;transform:none}}
.karte .nr{font-size:max(10.5px,1.05cqw);font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--brand)}
.karte h3{margin:.2cqw 0 .5cqw;font-size:max(17px,2.1cqw);line-height:1.15;letter-spacing:-.02em;color:var(--head)}
.karte p{margin:0}.karte .bsp{margin-top:.8cqw;padding:max(6px,.7cqw) max(8px,1cqw);border-radius:max(7px,.8cqw);background:var(--soft);color:var(--head)}
.karte .bsp b{display:block;font-size:max(10.5px,1.05cqw);letter-spacing:.06em;text-transform:uppercase;color:var(--brand)}
.band{position:absolute;z-index:4;left:3%;right:3%;bottom:3.5%;display:none;background:#fff;border-radius:max(10px,1.2cqw);padding:max(10px,1.4cqw) max(13px,2cqw);box-shadow:0 .6cqw 3cqw rgba(3,42,33,.3);font-size:max(14px,1.9cqw);line-height:1.35;color:var(--head);border-left:.6cqw solid var(--mint);animation:rein .22s ease-out}
.band.an{display:block}.band.fr{border-left-color:var(--brand);background:var(--mintsoft)}.band.hi{border-left-color:#d4b23a;background:var(--gold)}
.band b{display:block;font-size:max(10.5px,1.1cqw);letter-spacing:.08em;text-transform:uppercase;color:var(--brand);margin-bottom:.2cqw}
.ablauf{flex:0 0 auto;display:flex;gap:4px;padding:0 14px 8px;align-items:center}
.ablauf button{flex:1 1 0;min-width:0;height:8px;border-radius:99px;border:0;background:#d5dcd8;padding:0}
.ablauf button.fertig{background:#7fc4b2}.ablauf button.jetzt{background:var(--brand)}.ablauf button.erinn{background:#ecd77a}.ablauf button.erinn.fertig{background:#d4b23a}.ablauf button.erinn.jetzt{background:#8a6a00}
.live{position:absolute;right:2%;top:3%;width:max(300px,38cqw);max-width:96%;max-height:94%;overflow:auto;display:none;background:#fff;border-radius:max(10px,1.2cqw);padding:max(11px,1.4cqw) max(13px,1.7cqw);box-shadow:0 .6cqw 3cqw rgba(3,42,33,.34);font-size:max(13px,1.4cqw);z-index:5;border-top:.45cqw solid var(--brand)}
.live.an{display:block}.live h3{margin:0 0 .6cqw;font-size:max(15px,1.9cqw);color:var(--head)}
.live label{display:grid;grid-template-columns:1fr auto;gap:0 .8cqw;margin:.5cqw 0;font-weight:600;color:var(--head)}.live label output{font-weight:800;color:var(--brand)}
.live input[type=range]{grid-column:1/-1;width:100%;accent-color:var(--brand)}
.erg{display:grid;grid-template-columns:1fr 1fr;gap:.6cqw;margin-top:.8cqw}.erg div{background:var(--soft);border-radius:.7cqw;padding:.6cqw .8cqw}.erg b{display:block;font-size:max(15px,1.9cqw);color:var(--head);font-variant-numeric:tabular-nums}.erg span{font-size:max(11px,1.1cqw);color:var(--mut)}
.erg .gross{grid-column:1/-1;background:var(--mintsoft)}.erg .warn{background:var(--gold)}
.tipp{position:absolute;z-index:6;left:50%;bottom:4%;transform:translateX(-50%);max-width:92%;background:var(--head);color:#fff;border-radius:999px;padding:9px 18px;font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;animation:rein .25s ease-out}
.raster{position:fixed;inset:0;z-index:9;display:none;background:var(--bg);overflow:auto;padding:18px}
.raster.an{display:block}.raster h2{margin:0 0 12px;color:var(--head)}.raster .gitter{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px}
.raster button{border:1px solid var(--line);background:#fff;border-radius:12px;padding:6px;text-align:left}.raster button:hover{border-color:var(--brand)}.raster img{display:block;width:100%;border-radius:8px}.raster span{display:block;font-size:13px;padding:5px 3px 2px;color:var(--ink)}.raster b{color:var(--brand)}
.hilfe{position:fixed;inset:0;z-index:10;display:none;align-items:center;justify-content:center;background:rgba(10,24,20,.45);padding:16px}.hilfe.an{display:flex}
.hilfe>div{background:#fff;border-radius:18px;padding:22px 26px;max-width:560px;width:100%;box-shadow:0 18px 50px rgba(3,42,33,.3)}.hilfe h2{margin:0 0 10px;color:var(--head)}.hilfe table{width:100%;border-collapse:collapse}.hilfe td{padding:6px 8px;border-top:1px solid var(--line)}.hilfe kbd{background:var(--soft);border-radius:6px;padding:2px 7px;font:700 13px Archivo,sans-serif;color:var(--brand-d);white-space:nowrap}
/* Referentenansicht */
body.ref{overflow:auto;display:block}
.ref-raster{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:14px;padding:14px;align-items:start}
.ref-box{background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 16px;margin:0 0 12px}.ref-box h3{margin:0 0 6px;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--brand)}
.ref-box p{margin:0;font-size:18px;line-height:1.45;color:var(--head)}.ref-notiz p{font-size:20px}
.ref-liste{list-style:none;margin:0;padding:0}.ref-liste button{width:100%;text-align:left;border:0;background:none;padding:7px 9px;border-radius:9px;color:var(--ink)}.ref-liste button:hover{background:var(--soft)}.ref-liste button[aria-current=true]{background:var(--brand);color:#fff;font-weight:700}
.ref-kl{display:grid;grid-template-columns:1fr 1fr;gap:10px}.ref-kl img{width:100%;border-radius:10px;border:1px solid var(--line);display:block}
.ref-uhr{font-variant-numeric:tabular-nums;font-weight:800;color:var(--head)}
@media (max-width:760px){.leiste .ti,.kn.opt{display:none}.ref-raster{grid-template-columns:1fr}.leiste{padding:7px 10px}.leiste .pos{flex:1 1 100%}.kn{padding:6px 11px;font-size:13px}
.buehne{flex:0 0 auto;padding:8px 10px 4px}.folie{width:100%}.mark i{min-width:15px;height:15px;font-size:9.5px;line-height:15px;left:-6px;top:-7px}.tipp{display:none}
.unter{flex:1 1 auto;min-height:0;overflow:auto;padding:4px 10px 10px}.unter .karte,.unter .band,.unter .live{position:static;width:auto;max-width:none;max-height:none;margin:0 0 8px;font-size:16px;box-shadow:0 1px 3px rgba(15,21,19,.1),0 6px 18px rgba(3,42,33,.08);border-radius:14px;padding:13px 15px}
.unter .karte h3{font-size:19px;margin:2px 0 6px}.unter .band{font-size:16px}.unter .karte .nr,.unter .karte .bsp b,.unter .band b{font-size:11.5px}.unter .karte .bsp{margin-top:8px;padding:8px 10px;border-radius:9px}.unter .live h3{font-size:17px}.unter .erg b{font-size:17px}.unter .erg span{font-size:12px}.unter .erg{gap:6px}.unter .erg div{padding:8px 10px;border-radius:9px}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
'''


def schreiben():
    frames = daten()
    data = json.dumps(frames, ensure_ascii=False).replace('<', '\\u003c')
    html = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<!-- eigenes-layout -->
<title>Folien erklärt · Modul 2 · Tag 6 · Bewerten und rechnen</title><link rel="icon" href="/hefte/assets/favicon.svg">
<style>@font-face{{font-family:"Archivo";font-style:normal;font-weight:400 800;font-display:swap;src:url(/hefte/assets/fonts/archivo-latin.woff2) format("woff2")}}{CSS}</style>
<script src="/hefte/assets/praesentation.js?v={VERSION}" defer></script></head><body>
<script type="application/json" id="p-daten">{data}</script>
<div id="p-app" data-tag="modul-2/tag-6" data-titel="Modul 2 · Tag 6 · Bewerten und rechnen"><noscript><p style="padding:20px">Der Präsenter-Modus braucht JavaScript. Die Folien gibt es auch als <a href="/hefte/folien/tag-25/Folien_Modul2_Tag6_Bewerten-und-Rechnen.pdf">PDF</a>.</p></noscript></div>
</body></html>'''
    out = PUB / 'praesentation/modul-2/tag-6/index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf8')
    return sum(len(f['orte']) for f in frames), len(frames)
