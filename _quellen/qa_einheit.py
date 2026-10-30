"""Gesamtprüfung der vereinheitlichten Plattform (30.10.2026).

python -X utf8 qa_einheit.py [BASIS-URL]   (Server lokal auf :5387 oder live)
Statisch: jeder interne Link jeder Seite zeigt auf eine vorhandene Datei (Weiterleitungen werden aufgelöst),
keine Links mehr auf alte Tag-Adressen (außer Lernblatt), jede Seite hat Kopfzeile, Fußzeile und Design,
keine doppelten IDs, Kontraste der Farbwerte ≥ 4,5:1.
Browser (Chrome + WebKit): je Seitenfamilie keine JS-Fehler, kein Querscrollen bei 390 px, Reiter, Lernkarten,
Selbsttest, Training, Weiterleitung mit Sprungmarke, Modul-2-Quiz speichert über Neuladen.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / 'plattform/public'
BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://localhost:5387/hefte'
OUT = Path(__file__).resolve().parent / 'build/redesign'
STUB = '<!-- weiterleitung -->'


def target_file(path):
    p = PUB / unquote(path[len('/hefte/'):])
    if p.is_dir() or path.endswith('/'):
        p = p / 'index.html'
    return p


def statisch():
    pages = sorted(PUB.rglob('*.html'))
    broken, old, problems, stubs = [], [], [], 0
    for f in pages:
        text = f.read_text(encoding='utf8')
        rel = f.relative_to(PUB).as_posix()
        if STUB in text:
            stubs += 1
            tgt = re.search(r'data-weiter="([^"]+)"', text).group(1)
            if not target_file(tgt).exists():
                broken.append((rel, 'stub->' + tgt))
            continue
        url = '/hefte/' + rel[:-len('index.html')] if rel.endswith('index.html') else '/hefte/' + rel
        soup = BeautifulSoup(text, 'html.parser')
        if not soup.select_one('header.ui-top') or not soup.select_one('footer.foot') or not soup.select_one('style#ui-design'):
            problems.append((rel, 'Rahmen fehlt'))
        ids = [e['id'] for e in soup.select('[id]')]
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            problems.append((rel, 'doppelte IDs ' + ','.join(sorted(dup))[:80]))
        for e in soup.select('a[href],link[href],script[src],img[src]'):
            u = e.get('href') or e.get('src')
            if not u or u.startswith(('http:', 'https:', 'mailto:', 'data:', '#', 'javascript:')):
                continue
            full = urljoin(url, u)
            path = urlsplit(full).path
            if not path.startswith('/hefte/') or path.startswith('/hefte/api/'):
                continue
            if re.match(r'/hefte/(ingo|carmen|tabea)/tag-\d+/(?!lernblatt)', path + ('/' if not path.endswith('/') else '')) and '/lernblatt' not in path:
                old.append((rel, path))
            tf = target_file(path)
            if not tf.exists():
                broken.append((rel, path))
            elif STUB in tf.read_text(encoding='utf8', errors='ignore')[:200] if tf.suffix == '.html' else False:
                tgt = re.search(r'data-weiter="([^"]+)"', tf.read_text(encoding='utf8')).group(1)
                if not target_file(tgt).exists():
                    broken.append((rel, path + ' -> ' + tgt))
    return dict(pages=len(pages), stubs=stubs, broken=broken[:40], n_broken=len(broken), old=old[:20], n_old=len(old), problems=problems[:40], n_problems=len(problems))


def kontrast():
    def lum(h):
        h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
        return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]

    def ratio(a, b):
        la, lb = sorted([lum(a), lum(b)], reverse=True)
        return round((la + .05) / (lb + .05), 2)
    pairs = {'Text auf Seite': ('#2a312e', '#f4f6f5'), 'Text auf Karte': ('#2a312e', '#ffffff'), 'Nebentext auf Karte': ('#58615c', '#ffffff'),
             'Nebentext auf Seite': ('#58615c', '#f4f6f5'), 'Grün auf Weiß': ('#05614c', '#ffffff'), 'Weiß auf Grün': ('#ffffff', '#05614c'),
             'Text auf Hinweis gelb': ('#2a312e', '#fdf6d6'), 'Text auf Mint': ('#0f1513', '#e2fcf7'), 'Blau-Link auf Weiß': ('#0a5bb8', '#ffffff'),
             'Weiß auf Tabellenkopf': ('#ffffff', '#073d31')}
    res = {k: ratio(*v) for k, v in pairs.items()}
    assert all(v >= 4.5 for v in res.values()), res
    return res


def browser():
    from playwright.sync_api import sync_playwright
    pages = {'start': '/', 'uebersicht': '/carmen/', 'm1-tag12': '/carmen/modul-1/tag-12/', 'm1-tag2': '/carmen/modul-1/tag-2/',
             'm1-tag19': '/carmen/modul-1/tag-19/', 'm2-tag2': '/carmen/modul-2/tag-2/', 'hub': '/carmen/modul-2/tag-5/',
             'lh12': '/carmen/modul-1/tag-12/lernheft/', 'lh16': '/carmen/modul-1/tag-16/lernheft/', 'lh19': '/carmen/modul-1/tag-19/lernheft/',
             'bonus19': '/carmen/modul-1/tag-19/bonus/', 'm2lh2': '/carmen/modul-2/tag-2/lernheft/', 'praxis': '/carmen/modul-1/tag-10/praxis/',
             'heft2': '/carmen/modul-1/tag-2/heft/', 'aufgaben': '/carmen/aufgaben/', 'lernblatt': '/carmen/tag-12/lernblatt/',
             'wochenheft': '/carmen/modul-2/tag-5/lernheft/', 'dozent': '/dozent/'}
    report = []
    with sync_playwright() as p:
        for engine in ('chromium', 'webkit'):
            kw = {'executable_path': 'C:/Program Files/Google/Chrome/Application/chrome.exe'} if engine == 'chromium' else {}
            b = getattr(p, engine).launch(**kw)
            ctx = b.new_context(viewport={'width': 1280, 'height': 860})
            page = ctx.new_page()
            errs = []
            page.on('pageerror', lambda e: errs.append(str(e)))
            for name, u in pages.items():
                page.set_viewport_size({'width': 1280, 'height': 860})
                page.goto(BASE + u)
                page.wait_for_load_state('networkidle')
                assert page.is_visible('header.ui-top'), name
                page.set_viewport_size({'width': 390, 'height': 860})
                page.wait_for_timeout(150)
                over = page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
                assert over <= 1, (engine, name, over)
                if engine == 'chromium':
                    page.screenshot(path=str(OUT / f'qa-{name}-390.png'))
            page.set_viewport_size({'width': 1280, 'height': 860})
            # Tagesseiten: Startreiter, Lernkarten, Selbsttest, Training
            for u, first in (('/carmen/modul-2/tag-2/', 'heute'), ('/carmen/modul-1/tag-19/', 'heute'), ('/carmen/modul-1/tag-12/', 'learnings'), ('/carmen/modul-2/tag-5/', 'start')):
                page.goto(BASE + u); page.wait_for_load_state('networkidle')
                assert page.evaluate("document.querySelector('[aria-selected=true]').dataset.tab") == first, (u, first)
                page.click('[data-tab="karten"]'); page.click('#karten .kcard'); page.click('#karten .btn.primary')
                assert 'Karte 2 von' in page.inner_text('#karten'), u
                page.click('[data-tab="test"]'); page.click('#test .qopt >> nth=0'); assert page.is_visible('#test .qwhy'), u
                page.click('[data-tab="training"]'); assert page.inner_text('#training').strip(), u
                page.click('[data-tab="folien"]'); assert page.get_attribute('#folien .v-stage img', 'src'), u
            # Weiterleitung alter Adressen mit Sprungmarke
            page.goto(BASE + '/carmen/tag-21/#karten'); page.wait_for_url('**/modul-2/tag-2/#karten', timeout=8000)
            page.goto(BASE + '/carmen/tag-12/lernheft/#k3'); page.wait_for_url('**/modul-1/tag-12/lernheft/#k3', timeout=8000)
            # Modul-2-Lernheft: Quiz speichert weiter (alter Schlüssel)
            page.goto(BASE + '/carmen/modul-2/tag-2/lernheft/'); page.wait_for_load_state('networkidle')
            radios = page.locator('#quiz input[type=radio], .quiz input[type=radio], input[type=radio]')
            if radios.count():
                radios.first.check(); page.wait_for_timeout(400); page.reload(); page.wait_for_load_state('networkidle')
                assert page.locator('input[type=radio]').first.is_checked(), 'Quiz-Speicher'
            ctx.close(); b.close()
            assert not errs, (engine, errs[:5])
            report.append(dict(engine=engine, pages=len(pages), errors=0))
    return report


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    s = statisch()
    print(json.dumps({k: v for k, v in s.items() if not isinstance(v, list) or v}, ensure_ascii=False, indent=1)[:4000])
    assert s['n_broken'] == 0 and s['n_old'] == 0 and s['n_problems'] == 0, 'statische Prüfung fehlgeschlagen'
    print('Kontraste:', kontrast())
    print('Browser:', browser())
    print('OK: Gesamtprüfung bestanden')
