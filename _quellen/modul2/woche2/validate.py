"""Browserprüfung Modul 2 · Tag 6: Tagesseite, Rechen-Labor, Präsenter-Modus.

Aufruf (Server läuft): python -X utf8 modul2/woche2/validate.py [http://localhost:5387/hefte]
Prüft für Ingo, Carmen, Tabea in Chrome und WebKit: alle Reiter, Rechner mit Folienbeispiel,
Speicherung über Neuladen, Freitagsdaten als Erinnerung, Präsenter (Schritte, Tasten, Begriffe auf den Folien,
Live-Rechner, Referentenansicht) und 320/390/1280 px ohne Querscrollen.
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://localhost:5387/hefte'
OUT = Path(__file__).resolve().parents[2] / 'build/modul2-woche2'
CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
PERSONS = ['ingo', 'carmen', 'tabea']
TABS = ['start', 'labor', 'vorlagen', 'demos', 'training', 'learnings', 'karten', 'test', 'aufgaben', 'folien', 'woerter', 'heft']
PRAES = '/praesentation/modul-2/tag-6/'


def warten(page, ausdruck, sekunden=6):
    """Fragt selbst ab: wait_for_function nutzt eval, das die Sicherheitsregel der Seite (CSP) beim zweiten Versuch sperrt."""
    for _ in range(int(sekunden * 20)):
        if page.evaluate(ausdruck):
            return
        page.wait_for_timeout(50)
    raise AssertionError('Zeitüberschreitung: ' + ausdruck)


def check_day(ctx, pid, engine, report):
    errors = []
    page = ctx.new_page()
    page.on('pageerror', lambda e: errors.append(f'pageerror {e}'))
    page.on('console', lambda m: errors.append(f'console {m.text}') if m.type == 'error' else None)
    tag = f'{BASE}/{pid}/modul-2/tag-6/'
    # Freitag vorbelegen: dieselben Schlüssel wie im Use-Case-Labor von Tag 5
    page.goto(f'{BASE}/{pid}/modul-2/tag-5/')
    page.wait_for_load_state('networkidle')
    page.click('[data-tab="labor"]')
    page.fill('[data-save="sb1-name"]', 'Freitagsfall ' + pid)
    page.fill('[data-save="sb1-nutzen"]', '12 Stunden pro Monat')
    page.wait_for_timeout(500)
    page.goto(tag)
    page.wait_for_load_state('networkidle')
    assert page.evaluate("document.querySelector('[aria-selected=true]').dataset.tab") == 'start'
    for t in TABS:
        page.click(f'[data-tab="{t}"]')
        vis = page.evaluate("[...document.querySelectorAll('.tpanel')].filter(p=>!p.hidden).map(p=>p.id)")
        assert vis == [t], (t, vis)
    page.click('[data-tab="karten"]'); page.click('#karten .kcard'); page.click('#karten .btn.primary')
    assert 'Karte 2 von 26' in page.inner_text('#karten')
    page.click('[data-tab="test"]'); page.click('#test .qopt >> nth=1'); assert page.is_visible('#test .qwhy')
    page.click('[data-tab="folien"]'); assert 'tag-25/01.jpg' in page.get_attribute('#folien .v-stage img', 'src')
    # Rechen-Labor
    page.click('[data-tab="start"]')
    assert 'Freitagsfall ' + pid in page.inner_text('#start')
    page.click('[data-tab="labor"]')
    page.click('[data-bc-beispiel]')
    page.wait_for_timeout(300)
    text = page.inner_text('#labor')
    for soll in ('1.485', '1.185', '22.800', '18,5', '255,5'):
        assert soll in text, (soll, 'Business Case')
    # Szenarien: Vorschlag ergibt das Rechenbeispiel aus dem Heft
    page.click('[data-sz-vorschlag]')
    page.wait_for_timeout(200)
    sz = page.inner_text('[data-tool="szenario"]')
    for soll in ('635', 'rund 19 Monate', '36,5', 'rund 38 %'):
        assert soll in sz, (soll, sz)
    # Speicherung über Neuladen
    page.reload(); page.wait_for_load_state('networkidle')
    assert page.input_value('[data-save="bc-volumen"]') == '800'
    # Downloads
    page.click('[data-tab="vorlagen"]')
    for href in page.eval_on_selector_all('#vorlagen a[download]', 'els => els.map(e => e.href)'):
        assert page.request.get(href).ok, href
    widths = {}
    for w in (320, 390, 1280):
        page.set_viewport_size({'width': w, 'height': 900})
        for t in ('start', 'labor', 'vorlagen'):
            page.click(f'[data-tab="{t}"]')
            over = page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            widths[f'{w}-{t}'] = over
            assert over <= 1, (w, t, over)
        page.screenshot(path=str(OUT / f'tag6-{pid}-{engine}-{w}.png'))
    page.goto(tag + 'lernheft/')
    page.wait_for_load_state('networkidle')
    assert 'Freitagsfall ' + pid in page.inner_text('body')
    for w in (320, 390):
        page.set_viewport_size({'width': w, 'height': 900})
        over = page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
        assert over <= 1, ('lernheft', w, over)
    page.close()
    errs = [e for e in errors if 'favicon' not in e]
    assert not errs, errs
    report.append(dict(person=pid, engine=engine, widths=widths))


def check_praes(ctx, engine, report):
    errors = []
    page = ctx.new_page()
    page.on('pageerror', lambda e: errors.append(f'pageerror {e}'))
    page.on('console', lambda m: errors.append(f'console {m.text}') if m.type == 'error' else None)
    page.set_viewport_size({'width': 1280, 'height': 800})
    page.goto(BASE + PRAES)
    page.wait_for_load_state('networkidle')
    n = page.evaluate('PRAES.frames.length')
    assert n == 33, n
    assert 'Erinnerung 1/4' in page.inner_text('.pos')
    # Jeder Schritt jeder Folie: Karte passt in die Folie, Bild lädt
    fehler = []
    for i in range(n):
        page.evaluate(f'PRAES.geh({i}, 0)')
        warten(page, "document.querySelector('.folie>img').complete && document.querySelector('.folie>img').naturalWidth>0")
        orte = page.evaluate(f'PRAES.frames[{i}].orte.length')
        kern = 1 if page.evaluate(f'!!PRAES.frames[{i}].kern') else 0
        for o in range(orte):
            page.evaluate(f'PRAES.geh({i}, {1 + kern + o})')
            box = page.evaluate("""() => { const f=document.querySelector('.folie').getBoundingClientRect(), k=document.querySelector('.karte').getBoundingClientRect(), o=PRAES.frames[PRAES.pos()[0]];
              return {sicht:getComputedStyle(document.querySelector('.karte')).display!=='none', l:k.left-f.left, t:k.top-f.top, r:f.right-k.right, b:f.bottom-k.bottom}; }""")
            if not box['sicht'] or min(box['l'], box['t'], box['r'], box['b']) < -1:
                fehler.append((i, o, box))
    assert not fehler, fehler
    # Tasten: Schritt, Folie, Erklärungen aus
    page.evaluate('PRAES.geh(4, 0)')
    page.keyboard.press('ArrowRight')
    assert page.evaluate('PRAES.pos()') == [4, 1]
    assert page.is_visible('.band')
    page.keyboard.press('ArrowDown')
    assert page.evaluate('PRAES.pos()') == [5, 0]
    page.keyboard.press('e')
    assert page.locator('.mark:visible').count() == 0
    page.keyboard.press('e')
    # Live-Rechner auf Folie 19
    idx = page.evaluate("PRAES.frames.findIndex(f=>f.id==='19')")
    page.evaluate(f'PRAES.geh({idx}, 0)')
    page.keyboard.press('l')
    assert '10 Monate' in page.inner_text('.live')
    assert '1.485' in page.inner_text('.live')
    page.screenshot(path=str(OUT / f'praes-live-{engine}.png'))
    page.keyboard.press('Escape')
    # Übersicht
    page.keyboard.press('g')
    assert page.locator('.raster button').count() == 33
    page.keyboard.press('Escape')
    # Sprungmarke und Referentenansicht
    page.goto(BASE + PRAES + '#16.3')
    page.wait_for_load_state('networkidle')
    warten(page, 'PRAES.pos()[1] === 3')
    page.screenshot(path=str(OUT / f'praes-16-{engine}.png'))
    ref = ctx.new_page()
    ref.on('pageerror', lambda e: errors.append(f'ref {e}'))
    ref.goto(BASE + PRAES + '?ansicht=referent#16.3')
    ref.wait_for_load_state('networkidle')
    assert 'Alle drei Zahlen' in ref.inner_text('.ref-notiz')
    page.keyboard.press('ArrowRight')
    ref.wait_for_timeout(300)
    assert ref.evaluate('PRAES.pos()') == page.evaluate('PRAES.pos()')
    ref.screenshot(path=str(OUT / f'praes-referent-{engine}.png'))
    ref.close()
    # Breiten
    for w in (320, 390, 1280):
        page.set_viewport_size({'width': w, 'height': 800})
        page.wait_for_timeout(120)
        over = page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
        assert over <= 1, ('praes', w, over)
    page.screenshot(path=str(OUT / f'praes-1280-{engine}.png'))
    # Handy: Erklärung gut lesbar unter der Folie, Rechner ebenso
    page.set_viewport_size({'width': 390, 'height': 800})
    page.wait_for_timeout(150)
    idx = page.evaluate("PRAES.frames.findIndex(f=>f.id==='16')")
    page.evaluate(f'PRAES.geh({idx}, 3, true)')
    page.wait_for_timeout(150)
    assert page.locator('.unter .karte').is_visible()
    size = page.evaluate("parseFloat(getComputedStyle(document.querySelector('.unter .karte')).fontSize)")
    assert size >= 15, size
    page.screenshot(path=str(OUT / f'praes-390-{engine}.png'))
    page.click('.kn:has-text("Live-Rechner")')
    assert page.locator('.unter .live').is_visible()
    page.screenshot(path=str(OUT / f'praes-390-live-{engine}.png'))
    assert page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth') <= 1
    page.set_viewport_size({'width': 1280, 'height': 800})
    page.close()
    errs = [e for e in errors if 'favicon' not in e]
    assert not errs, errs
    report.append(dict(praesenter=engine, folien=n))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = []
    with sync_playwright() as p:
        for engine in ('chromium', 'webkit'):
            kw = {'executable_path': CHROME} if engine == 'chromium' else {}
            b = getattr(p, engine).launch(**kw)
            for pid in PERSONS:
                ctx = b.new_context()
                check_day(ctx, pid, engine, report)
                ctx.close()
            ctx = b.new_context()
            check_praes(ctx, engine, report)
            ctx.close()
            b.close()
    (OUT / 'validate.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print(f'OK: {len(report)} Prüfläufe ohne Fehler')


if __name__ == '__main__':
    main()
