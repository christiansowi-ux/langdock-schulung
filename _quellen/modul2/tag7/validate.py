"""Browserprüfung Modul 2 · Tag 7: Tagesseite, Ermittlungsakte, Spiele, Präsenter-Modus.

Aufruf (Server läuft): python -X utf8 modul2/tag7/validate.py [http://localhost:5387/hefte]
Prüft für Ingo, Carmen, Tabea in Chrome und WebKit: alle Reiter, Stand von Montag, Spiele bis zur Auswertung, Bingo,
Mitschrift mit Alarmsatz-Melder, Bahnen mit Folienbeispiel und Skizze, Datenfluss in SOP und Kriterien, Speicherung über Neuladen,
Präsenter (Schritte, Karten, Mitmachen, Referentenansicht) und 320/390/1280 px ohne Querscrollen.
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://localhost:5387/hefte'
OUT = Path(__file__).resolve().parents[2] / 'build/modul2-tag7'
CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
PERSONS = ['ingo', 'carmen', 'tabea']
TABS = ['start', 'akte', 'spiele', 'vorlagen', 'demos', 'training', 'learnings', 'karten', 'test', 'aufgaben', 'folien', 'woerter', 'heft']
PRAES = '/praesentation/modul-2/tag-7/'


def warten(page, ausdruck, sekunden=6):
    """Fragt selbst ab: wait_for_function nutzt eval, das die Sicherheitsregel der Seite (CSP) beim zweiten Versuch sperrt."""
    for _ in range(int(sekunden * 20)):
        if page.evaluate(ausdruck):
            return
        page.wait_for_timeout(50)
    raise AssertionError('Zeitüberschreitung: ' + ausdruck)


def spiel_durch(page, sid):
    """Spielt alle Karten richtig durch und erwartet die höchste Auswertung."""
    box = f'[data-spiel="{sid}"]'
    for _ in range(12):
        if page.locator(f'{box} .sp-erg').count():
            break
        loesung = page.evaluate(f"""() => {{ const b=document.querySelector('{box}'), d=JSON.parse(b.querySelector('.sp-daten').textContent), t=b.querySelector('.sp-t').textContent; return d.karten.find(k=>k.t===t).r; }}""")
        page.locator(f'{box} .sp-b').filter(has_text=loesung).first.click()
        assert page.locator(f'{box} .sp-w.ok').count() == 1, sid
        page.locator(f'{box} .sp-weiter .btn').click()
    assert 'Chefermittlung' in page.inner_text(box), sid


def check_day(ctx, pid, engine, report):
    errors = []
    page = ctx.new_page()
    page.on('pageerror', lambda e: errors.append(f'pageerror {e}'))
    page.on('console', lambda m: errors.append(f'console {m.text}') if m.type == 'error' else None)
    page.on('dialog', lambda d: d.accept())
    tag = f'{BASE}/{pid}/modul-2/tag-7/'
    # Montag vorbelegen: dieselben Schlüssel wie im Rechen-Labor von Tag 6
    page.goto(f'{BASE}/{pid}/modul-2/tag-6/')
    page.wait_for_load_state('networkidle')
    page.click('[data-tab="labor"]')
    page.fill('[data-save="bw1-name"]', 'Montagsfall ' + pid)
    page.select_option('[data-save="haupt"]', '1')
    page.click('[data-bc-beispiel]')
    page.wait_for_timeout(500)
    page.goto(tag)
    page.wait_for_load_state('networkidle')
    assert page.evaluate("document.querySelector('[aria-selected=true]').dataset.tab") == 'start'
    start = page.inner_text('#start')
    assert 'Montagsfall ' + pid in start and 'rund 10 Monate' in start, start[:300]
    for t in TABS:
        page.click(f'[data-tab="{t}"]')
        vis = page.evaluate("[...document.querySelectorAll('.tpanel')].filter(p=>!p.hidden).map(p=>p.id)")
        assert vis == [t], (t, vis)
    page.click('[data-tab="karten"]'); page.click('#karten .kcard'); page.click('#karten .btn.primary')
    assert 'Karte 2 von 38' in page.inner_text('#karten')
    page.click('[data-tab="test"]'); page.click('#test .qopt >> nth=1'); assert page.is_visible('#test .qwhy')
    page.click('[data-tab="folien"]'); assert 'tag-26/01.jpg' in page.get_attribute('#folien .v-stage img', 'src')
    # Spiele und Bingo
    page.click('[data-tab="spiele"]')
    for sid in ('wunsch', 'rueckfrage', 'spalten', 'tuersteher'):
        spiel_durch(page, sid)
    felder = page.locator('#spiele [data-bingo] .bg-z')
    assert felder.count() == 9
    for i in (0, 4, 8):
        felder.nth(i).click()
        felder = page.locator('#spiele [data-bingo] .bg-z')
    assert 'BINGO' in page.inner_text('#spiele [data-tool="bingo"] .bg-frage')
    page.wait_for_timeout(2500)
    # Ermittlungsakte: Mitschrift mit Alarm, Bahnen, Datenfluss
    page.click('[data-tab="akte"]')
    page.click('[data-ms-bsp]')
    alarme = page.inner_text('[data-tool="mitschrift"] .alarm-liste')
    assert '„normalerweise“' in alarme and '„das sieht man“' in alarme, alarme
    page.click('[data-ms-vorlesen]')
    assert page.is_visible('.ms-vorlesen')
    page.click('[data-sipoc-bsp]')
    assert 'PDF-Rechnung' in page.inner_text('.absperr')
    assert page.locator('[data-stand="sipoc"] .stempel').count() == 1, page.inner_text('[data-stand="sipoc"]')
    page.click('[data-bh-bsp]')
    bahn = page.inner_text('[data-tool="bahnen"]')
    for soll in ('12 Minuten', '5,0 Tage', '1 zu 200', 'Fachabteilung'):
        assert soll in bahn, (soll, bahn[:400])
    assert page.locator('.bh-skizze svg').count() == 1
    assert page.locator('[data-stand="bahnen"] .stempel').count() == 1, page.inner_text('[data-stand="bahnen"]')
    assert page.inner_text('[data-stat-verh]') == '1 zu 200'
    # Was wäre, wenn: Arbeit weg ändert kaum etwas, Übergabe weg sehr viel
    page.click('.bh-kn .sp-b >> nth=0')
    assert '5,0 → 5,0' in page.inner_text('.bh-was-e'), page.inner_text('.bh-was-e')
    page.click('.bh-kn .sp-b >> nth=0')
    page.locator('.bh-kn .sp-b').filter(has_text='Fachabteilung').first.click()
    assert '5,0 → 3,0' in page.inner_text('.bh-was-e'), page.inner_text('.bh-was-e')
    page.click('[data-sop-bahnen]')
    assert page.locator('.sop-zeile').count() == 12, page.locator('.sop-zeile').count()
    page.click('[data-sop-bsp]')
    page.check('[data-save="t7-sop-ok"]')
    assert page.locator('[data-stand="sop"] .stempel').count() == 1, page.inner_text('[data-stand="sop"]')
    page.click('[data-kr-bahnen]')
    assert page.input_value('[data-save="t7-kr1-heute"]') == '5,0 Tage'
    page.click('[data-kr-bsp]')
    assert page.locator('[data-stand="kriterien"] .stempel').count() == 1, page.inner_text('[data-stand="kriterien"]')
    # Zielsatz: Rückmeldung, wenn etwas fehlt, und Technikbegriff im Namen
    page.fill('[data-save="t7-ziel-anteil"]', '70 Prozent')
    assert '2049' in page.inner_text('.ziel-fehlt')
    page.click('[data-ziel-bsp]')
    page.fill('[data-save="t7-ziel-name"]', 'KI-Rechnungsbot')
    assert 'Technologiebegriff' in page.inner_text('.ziel-fehlt')
    page.fill('[data-save="t7-ziel-name"]', 'Rechnung in einem Tag')
    assert 'ab drei Monaten nach Start.' in page.inner_text('.ziel-satz')
    assert page.locator('[data-stand="ziel"] .stempel').count() == 1, page.inner_text('[data-stand="ziel"]')
    page.click('[data-scope-bsp]')
    assert page.locator('[data-stand="scope"] .stempel').count() == 1, page.inner_text('[data-stand="scope"]')
    # Speicherung über Neuladen
    page.wait_for_timeout(400)
    page.reload(); page.wait_for_load_state('networkidle')
    page.click('[data-tab="akte"]')
    assert page.locator('.bh-skizze svg').count() == 1
    assert page.input_value('[data-save="t7-ziel-zeit"]') == 'ab drei Monaten nach Start'
    assert page.locator('.sop-zeile').count() == 6
    # Downloads
    page.click('[data-tab="vorlagen"]')
    for href in page.eval_on_selector_all('#vorlagen a[download]', 'els => els.map(e => e.href)'):
        assert page.request.get(href).ok, href
    widths = {}
    for w in (320, 390, 1280):
        page.set_viewport_size({'width': w, 'height': 900})
        for t in ('start', 'akte', 'spiele', 'vorlagen'):
            page.click(f'[data-tab="{t}"]')
            over = page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            widths[f'{w}-{t}'] = over
            assert over <= 1, (w, t, over)
        page.screenshot(path=str(OUT / f'tag7-{pid}-{engine}-{w}.png'))
    page.goto(tag + 'lernheft/')
    page.wait_for_load_state('networkidle')
    assert 'Montagsfall ' + pid in page.inner_text('body')
    for w in (320, 390):
        page.set_viewport_size({'width': w, 'height': 900})
        page.reload(); page.wait_for_load_state('networkidle')  # WebKit misst nach reinem Fensterwechsel bis zur nächsten Neuberechnung einen veralteten Wert
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
    assert n == 42, n
    assert 'Was bisher geschah 1/4' in page.inner_text('.pos')
    # Jeder Schritt jeder Folie: Karte passt in die Folie, Bild lädt
    fehler = []
    for i in range(n):
        page.evaluate(f'PRAES.geh({i}, 0)')
        warten(page, "document.querySelector('.folie>img').complete && document.querySelector('.folie>img').naturalWidth>0")
        orte = page.evaluate(f'PRAES.frames[{i}].orte.length')
        kern = 1 if page.evaluate(f'!!PRAES.frames[{i}].kern') else 0
        for o in range(orte):
            page.evaluate(f'PRAES.geh({i}, {1 + kern + o})')
            box = page.evaluate("""() => { const f=document.querySelector('.folie').getBoundingClientRect(), k=document.querySelector('.karte').getBoundingClientRect();
              return {sicht:getComputedStyle(document.querySelector('.karte')).display!=='none', l:k.left-f.left, t:k.top-f.top, r:f.right-k.right, b:f.bottom-k.bottom}; }""")
            if not box['sicht'] or min(box['l'], box['t'], box['r'], box['b']) < -1:
                fehler.append((i, o, box))
    assert not fehler, fehler
    # Die Leiste bleibt auf dem Präsentationsrechner einzeilig, auch mit Mitmachen-Knopf
    for i in range(n):
        page.evaluate(f'PRAES.geh({i}, 0)')
        assert page.evaluate("document.querySelector('.leiste').offsetHeight") < 70, i
    # Aus der Akte erscheint als eigener Schritt
    idx = page.evaluate("PRAES.frames.findIndex(f=>f.id==='22')")
    orte = page.evaluate(f'PRAES.frames[{idx}].orte.length')
    page.evaluate(f'PRAES.geh({idx}, {2 + orte})')
    assert 'AUS DER AKTE' in page.inner_text('.band').upper(), page.inner_text('.band')
    # Mitmachen: Bahnen auf Folie 22
    page.evaluate(f'PRAES.geh({idx}, 0)')
    page.keyboard.press('l')
    live = page.inner_text('.live')
    assert '5,0 Tage' in live and '1 zu 200' in live, live
    page.screenshot(path=str(OUT / f'praes-bahnen-{engine}.png'))
    page.keyboard.press('Escape')
    # Mitmachen: Spiel auf Folie 9, Klick darf nicht weiterblättern
    idx = page.evaluate("PRAES.frames.findIndex(f=>f.id==='9')")
    page.evaluate(f'PRAES.geh({idx}, 0)')
    page.keyboard.press('l')
    assert page.is_visible('.live .sp-t')
    page.locator('.live .sp-b').first.click()
    assert page.is_visible('.live .sp-w')
    page.keyboard.press('Enter')
    assert page.evaluate('PRAES.pos()') == [idx, 0]
    assert 'Karte 2 von 8' in page.inner_text('.live')
    page.screenshot(path=str(OUT / f'praes-spiel-{engine}.png'))
    page.keyboard.press('Escape')
    # Mitmachen: Zielsatz, Bingo, Aufwand
    idx = page.evaluate("PRAES.frames.findIndex(f=>f.id==='10')")
    page.evaluate(f'PRAES.geh({idx}, 0)')
    page.keyboard.press('l')
    page.locator('.live .sp-b').filter(has_text='Zeitpunkt').click()
    assert '2049' in page.inner_text('.live')
    page.screenshot(path=str(OUT / f'praes-ziel-{engine}.png'))
    page.keyboard.press('Escape')
    idx = page.evaluate("PRAES.frames.findIndex(f=>f.id==='16')")
    page.evaluate(f'PRAES.geh({idx}, 0)')
    page.keyboard.press('l')
    for i in (0, 4, 8):
        page.locator('.live .lv-z').nth(i).click()
    assert 'BINGO' in page.inner_text('.live')
    page.screenshot(path=str(OUT / f'praes-bingo-{engine}.png'))
    page.keyboard.press('Escape')
    idx = page.evaluate("PRAES.frames.findIndex(f=>f.id==='36')")
    page.evaluate(f'PRAES.geh({idx}, 0)')
    page.keyboard.press('l')
    assert '17.000 bis 25.000' in page.inner_text('.live'), page.inner_text('.live')
    page.keyboard.press('Escape')
    # Übersicht
    page.keyboard.press('g')
    assert page.locator('.raster button').count() == 42
    page.keyboard.press('Escape')
    # Sprungmarke und Referentenansicht
    page.goto(BASE + PRAES + '#22.2')
    page.wait_for_load_state('networkidle')
    warten(page, 'PRAES.pos()[1] === 2')
    page.wait_for_timeout(350)
    page.screenshot(path=str(OUT / f'praes-22-{engine}.png'))
    ref = ctx.new_page()
    ref.on('pageerror', lambda e: errors.append(f'ref {e}'))
    ref.goto(BASE + PRAES + '?ansicht=referent#22.2')
    ref.wait_for_load_state('networkidle')
    assert 'stärkste Moment' in ref.inner_text('.ref-notiz')
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
    # Handy: Erklärung und Spiel gut lesbar unter der Folie
    page.set_viewport_size({'width': 390, 'height': 800})
    page.wait_for_timeout(150)
    idx = page.evaluate("PRAES.frames.findIndex(f=>f.id==='22')")
    page.evaluate(f'PRAES.geh({idx}, 2, true)')
    page.wait_for_timeout(150)
    assert page.locator('.unter .karte').is_visible()
    size = page.evaluate("parseFloat(getComputedStyle(document.querySelector('.unter .karte')).fontSize)")
    assert size >= 15, size
    page.screenshot(path=str(OUT / f'praes-390-{engine}.png'))
    idx = page.evaluate("PRAES.frames.findIndex(f=>f.id==='12')")
    page.evaluate(f'PRAES.geh({idx}, 0, true)')
    page.wait_for_timeout(100)
    page.click('.kn:has-text("Spiel")')
    assert page.locator('.unter .live').is_visible()
    page.screenshot(path=str(OUT / f'praes-390-spiel-{engine}.png'))
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
