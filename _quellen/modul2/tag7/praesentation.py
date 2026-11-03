"""Präsenter-Modus Modul 2 · Tag 7: gleiche Bühne wie Tag 6, dazu Mitmachen auf der Folie (Spiele, Bingo, Bahnen, Baustein weglassen, Aufwand).

Fehlt ein Begriff auf der Folie, bricht der Bau ab, damit nichts falsch markiert wird. Sprechernotizen stehen nur in der Referentenansicht.
"""
import json
from pathlib import Path

import fitz

from ..woche2.praesentation import CSS, VERSION, _orte
from .praesentation_daten import ERINNERUNG, FOLIEN, ZIEL_LIVE
from .spiele import SPIELE, BINGO, RAENGE

ROOT = Path(__file__).resolve().parents[3]
PUB = ROOT / 'plattform/public'
ADRESSE = '/hefte/praesentation/modul-2/tag-7/'
PDF_HEUTE = PUB / 'folien/tag-26/Folien_Modul2_Tag7_Prozess-verstehen.pdf'
PDF_MONTAG = PUB / 'folien/tag-25/Folien_Modul2_Tag6_Bewerten-und-Rechnen.pdf'
NOTIZEN = Path(__file__).with_name('sprechernotizen.json')


def _spiel(sid):
    s = SPIELE[sid]
    return dict(titel=s['titel'], optionen=s.get('optionen'), raenge=RAENGE, karten=[dict(t=k[0], r=k[1], w=k[2], o=k[3] if len(k) > 3 else None) for k in s['karten']])


def _live(f):
    live = f.get('live', '')
    daten = None
    if live == 'spiel':
        daten = _spiel(f['spiel'])
    elif live == 'bingo':
        daten = [dict(a=a, b=b, f=x) for a, b, x in BINGO]
    elif live == 'ziel':
        daten = ZIEL_LIVE
    return dict(live=live, liveName=f.get('liveName', ''), liveDaten=daten)


def daten():
    heute, montag = fitz.open(PDF_HEUTE), fitz.open(PDF_MONTAG)
    notizen = json.loads(NOTIZEN.read_text(encoding='utf8'))
    frames = []
    for i, f in enumerate(ERINNERUNG, 1):
        page = montag[f['seite'] - 1]
        frames.append(dict(id=f'e{i}', bild=f'/hefte/folien/tag-25/{f["seite"]:02d}.jpg', daumen=f'/hefte/folien/tag-25/t{f["seite"]:02d}.jpg', label=f'Was bisher geschah {i}/{len(ERINNERUNG)}',
                           titel=f['titel'], kern=f['kern'], frage=f.get('frage', ''), hinweis='', fun='', live='', notiz='Kurzer Rückblick auf Montag. Nicht neu erklären, nur Erinnerung wecken und die Frage stellen.',
                           orte=_orte(page, f['begriffe'], f'Montag {f["seite"]}')))
    for n, f in FOLIEN.items():
        page = heute[n - 1]
        frames.append(dict(id=str(n), bild=f'/hefte/folien/tag-26/{n:02d}.jpg', daumen=f'/hefte/folien/tag-26/t{n:02d}.jpg', label=f'Folie {n}/{len(FOLIEN)}',
                           titel=notizen[str(n)]['titel'], kern=f['kern'], frage=f.get('frage', ''), hinweis=f.get('hinweis', ''), fun=f.get('fun', ''),
                           notiz=notizen[str(n)]['notiz'], orte=_orte(page, f['begriffe'], f'Folie {n}'), **_live(f)))
    return frames


def schreiben():
    frames = daten()
    data = json.dumps(frames, ensure_ascii=False).replace('<', '\\u003c')
    html = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<!-- eigenes-layout -->
<title>Folien erklärt · Modul 2 · Tag 7 · Prozess verstehen</title><link rel="icon" href="/hefte/assets/favicon.svg">
<style>@font-face{{font-family:"Archivo";font-style:normal;font-weight:400 800;font-display:swap;src:url(/hefte/assets/fonts/archivo-latin.woff2) format("woff2")}}{CSS}</style>
<script src="/hefte/assets/praesentation.js?v={VERSION}" defer></script></head><body>
<script type="application/json" id="p-daten">{data}</script>
<div id="p-app" data-tag="modul-2/tag-7" data-titel="Modul 2 · Tag 7 · Prozess verstehen und abgrenzen"><noscript><p style="padding:20px">Der Präsenter-Modus braucht JavaScript. Die Folien gibt es auch als <a href="/hefte/folien/tag-26/Folien_Modul2_Tag7_Prozess-verstehen.pdf">PDF</a>.</p></noscript></div>
</body></html>'''
    out = PUB / 'praesentation/modul-2/tag-7/index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf8')
    return sum(len(f['orte']) for f in frames), len(frames)
