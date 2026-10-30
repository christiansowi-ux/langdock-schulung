"""Einheitliche Plattform (30.10.2026, Auftrag Chris: „alles gleich, geordnet, hell, keine vermischten Sachen“).

Läuft am Ende von build.py --web über alle Seiten in plattform/public:
1. Kanonische Adressen: /hefte/<person>/modul-1/tag-N/ (Tag 1–19) und /modul-2/tag-N/ (interne Tage 20–24).
   Unterseiten lernheft/, heft/, praxis/, bonus/ ziehen mit. Alte Adressen /tag-N/... werden zu Weiterleitungen
   (Hash und Parameter bleiben erhalten). Lernblätter bleiben unter /tag-N/lernblatt/ (Quelle für den PDF-Dienst).
2. Alle Links auf die neuen Adressen umschreiben.
3. Jede Seite bekommt dieselbe Kopfzeile (Logo, Brotkrumen, Aktionen der Seite) und Fußzeile.
4. Das gemeinsame Design (assets/ui.css) wird eingebettet – zuletzt, damit es überall gilt.
Speicherstände hängen an Tag-Nummern und Heft-Kennungen, nicht an Adressen; sie bleiben erhalten.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / 'plattform/public'
BASE = '/hefte'
PERSONEN = {'ingo': 'Ingo', 'carmen': 'Carmen', 'tabea': 'Tabea'}
SUBS = ('lernheft', 'heft', 'praxis', 'bonus')
STUB = '<!-- weiterleitung -->'
MODUL = {1: 'Modul 1 · KI-Grundlagen', 2: 'Modul 2 · KI-Automation'}
SUBNAME = {'lernheft': 'Lernheft', 'heft': 'Arbeitsheft', 'praxis': 'Praxisheft', 'bonus': 'Bonusheft', 'lernblatt': 'Lernblatt'}
FOOTER = ('<footer class="foot"><div class="wrap foot-in"><span>Futureway KI Institut · Kurs „KI Automations Spezialist“</span>'
          '<span><a href="https://quint-marketplace.de/impressum">Impressum</a> · <a href="https://quint-marketplace.de/datenschutz">Datenschutz</a> · '
          '<a href="/hefte/dozent/">Für die Schulungsleitung</a></span></div></footer>')
LOGO = '<a class="top-brand" href="/hefte/"><img src="/hefte/assets/futureway_logo.png" alt="Futureway KI Institut" width="132" height="53"></a>'
SERIF = '''@font-face{font-family:"Instrument Serif";font-style:italic;font-weight:400;font-display:swap;src:url(/hefte/assets/fonts/instrument-serif-italic-latin.woff2) format("woff2")}
@font-face{font-family:"Archivo";font-style:normal;font-weight:400 800;font-display:swap;src:url(/hefte/assets/fonts/archivo-latin.woff2) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
'''


def esc(s):
    return html.escape(str(s), quote=True)


def modul_von(n):
    return 1 if n <= 19 else 2


def modul_tag(n):
    return n if n <= 19 else n - 19


def tag_pfad(n):
    return f'modul-{modul_von(n)}/tag-{modul_tag(n)}/'


def tag_url(pid, n, sub=''):
    return f'{BASE}/{pid}/{tag_pfad(n)}{sub}'


# ------------------------------------------------------------------ 1. Umzug + Weiterleitungen

def stub(ziel):
    z = esc(ziel)
    return (f'<!doctype html>{STUB}<html lang="de"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>Weiterleitung</title>'
            f'<link rel="canonical" href="{z}"><meta http-equiv="refresh" content="2; url={z}">'
            f'<script src="/hefte/assets/weiter.js" defer></script></head><body data-weiter="{z}" style="font-family:system-ui,sans-serif;padding:24px">'
            f'<p>Diese Seite ist umgezogen: <a href="{z}">weiter zur neuen Adresse</a></p></body></html>')


def umzug(tage):
    """Verschiebt frisch gebaute Seiten an die kanonische Adresse und hinterlässt Weiterleitungen."""
    moved = 0
    for pid in PERSONEN:
        for n in tage:
            for sub in ('',) + SUBS:
                rel = f'{sub}/' if sub else ''
                old = PUB / pid / f'tag-{n}' / rel / 'index.html'
                if not old.exists():
                    continue
                text = old.read_text(encoding='utf8')
                new = PUB / pid / tag_pfad(n) / rel / 'index.html'
                if STUB not in text:
                    new.parent.mkdir(parents=True, exist_ok=True)
                    new.write_text(text, encoding='utf8')
                    moved += 1
                old.write_text(stub(tag_url(pid, n, rel)), encoding='utf8')
    man = PUB / 'manifest.json'
    m = json.loads(man.read_text(encoding='utf8'))
    for hid, h in m['hefte'].items():
        mm = re.fullmatch(r'(ingo|carmen|tabea)/tag-(\d+)', hid)
        if mm:
            h['path'] = f'{mm.group(1)}/{tag_pfad(int(mm.group(2)))}heft/'
    man.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf8')
    return moved


# ------------------------------------------------------------------ 2. Links

LINK = re.compile(r'/hefte/(ingo|carmen|tabea)/tag-(\d+)(/[^"\'\s<>]*)?')


def links(text):
    def repl(m):
        pid, n, rest = m.group(1), int(m.group(2)), m.group(3) or '/'
        if rest.startswith('/lernblatt'):
            return m.group(0)
        return f'/hefte/{pid}/{tag_pfad(n)}' + rest.lstrip('/')
    return LINK.sub(repl, text)


# ------------------------------------------------------------------ 3. Kopfzeile, Fußzeile, Design

def crumbs(rel, tage):
    """Brotkrumen aus dem Pfad relativ zu public/."""
    parts = rel.split('/')[:-1]
    c = [('Lernplattform', f'{BASE}/')]
    if not parts:
        return c
    if parts[0] == 'dozent':
        return c + [('Schulungsleitung', '')]
    if parts[0] == 'material':
        return c + [('Material ' + parts[1].replace('tag-', 'Tag '), '')]
    if parts[0] == 'tag-3':
        return c + [('Tag 3 · Heft vom Vormittag', '')]
    pid = parts[0]
    if pid not in PERSONEN:
        return c
    c.append((PERSONEN[pid], f'{BASE}/{pid}/'))
    rest = parts[1:]
    if not rest:
        return c
    if rest[0] == 'aufgaben':
        return c + [('Aufgaben', '')]
    if rest[0] == 'lernblatt':
        return c + [('Lernblatt aller Tage', '')]
    n = None
    if rest[0].startswith('modul-') and len(rest) > 1:
        mod, mt = int(rest[0][6:]), int(rest[1][4:])
        n = mt if mod == 1 else mt + 19
        sub = rest[2] if len(rest) > 2 else ''
    elif rest[0].startswith('tag-'):
        n = int(rest[0][4:])
        sub = rest[1] if len(rest) > 1 else ''
    if n is None or n not in tage:
        return c
    mod = modul_von(n)
    titel = tage[n]['titel']
    kurz = titel if len(titel) <= 34 else titel[:32].rsplit(' ', 1)[0] + ' …'
    c.append((MODUL[mod], f'{BASE}/{pid}/#modul-{mod}'))
    c.append((f'Tag {modul_tag(n)} · {kurz}', tag_url(pid, n) if sub else ''))
    if sub:
        c.append((SUBNAME.get(sub, sub), ''))
    return c


def crumb_html(c):
    out = []
    for i, (label, href) in enumerate(c):
        last = i == len(c) - 1
        out.append(f'<span aria-current="page">{esc(label)}</span>' if last or not href else f'<a href="{esc(href)}">{esc(label)}</a>')
    return '<nav class="crumbs" aria-label="Brotkrumen">' + '<span class="sep">/</span>'.join(out) + '</nav>'


def header(text, rel, tage):
    m = re.search(r'<header\b[^>]*>.*?</header>', text, re.S)
    if not m:
        return text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(m.group(0), 'html.parser')
    h = soup.header
    nav = crumb_html(crumbs(rel, tage))
    if 'top' in (h.get('class') or []) and h.find(class_='top-in'):
        right = h.find(class_='top-right')
        right_html = right.decode_contents() if right else ''
    else:
        box = h
        kids = [k for k in box.children if getattr(k, 'name', None)]
        if len(kids) == 1 and kids[0].name == 'div' and not kids[0].get('id'):
            box = kids[0]
            kids = [k for k in box.children if getattr(k, 'name', None)]
        keep = []
        for k in kids:
            cls = k.get('class') or []
            txt = k.get_text(' ', strip=True)
            if k.name == 'a' and (txt.startswith('←') or 'wb-back' in cls) and not k.has_attr('download'):
                continue  # Zurück-Link: steckt jetzt in den Brotkrumen
            if (k.name == 'span' and not k.get('id')) or (k.name == 'div' and ({'t', 'wb-title'} & set(cls))):
                continue  # Titelzeile: steckt jetzt in den Brotkrumen
            if k.name == 'a' and k.has_attr('download'):
                k['class'] = list(set(cls) | {'btn'})
            keep.append(str(k))
        right_html = ''.join(keep)
    pid = rel.split('/')[0]
    if pid in PERSONEN and 'top-switch' not in right_html:
        right_html += f'<a class="top-switch" href="{BASE}/?wechseln=1">Person wechseln</a>'
    new = f'<header class="top ui-top"><div class="top-in">{LOGO}{nav}<div class="top-right">{right_html}</div></div></header>'
    return text[:m.start()] + new + text[m.end():]


def familie(text, rel):
    if re.search(r'<body[^>]*class="[^"]*\bkurs\b', text):
        return 'ui-kurs'
    if re.search(r'<body[^>]*class="[^"]*\blh\b', text):
        return 'ui-lh'
    if re.search(r'<body[^>]*class="[^"]*\bweb\b', text):
        return 'ui-web'
    return 'ui-tb'


def vereinheitlichen(tage):
    css = (PUB / 'assets/ui.css').read_text(encoding='utf8')
    assert '</style' not in css.lower()
    style = f'<style id="ui-design">{SERIF}{css}</style>'
    count = 0
    for p in sorted(PUB.rglob('*.html')):
        rel = p.relative_to(PUB).as_posix()
        text = p.read_text(encoding='utf8')
        if STUB in text:
            continue
        if 'id="ui-design"' in text:  # schon vereinheitlicht (statische Seite): nur das Design auffrischen
            new = re.sub(r'<style id="ui-design">.*?</style>', lambda _: style, text, count=1, flags=re.S)
            if new != text:
                p.write_text(new, encoding='utf8')
            continue
        text = links(text)
        text = header(text, rel, tage)
        fam = familie(text, rel)
        text = re.sub(r'<body([^>]*?)class="([^"]*)"', lambda m: f'<body{m.group(1)}class="{m.group(2)} ui {fam}"', text, count=1) \
            if re.search(r'<body[^>]*class="', text) else re.sub(r'<body', f'<body class="ui {fam}"', text, count=1)
        text = text.replace('</head>', style + '</head>', 1)
        if 'class="foot"' not in text:
            text = text.replace('</body>', FOOTER + '</body>', 1)
        p.write_text(text, encoding='utf8')
        count += 1
    return count


def alles(tage):
    moved = umzug(tage)
    count = vereinheitlichen(tage)
    print(f'Einheit: {moved} Seiten an neue Adressen, {count} Seiten vereinheitlicht')
