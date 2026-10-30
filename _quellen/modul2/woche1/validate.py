"""Browserprüfung Learning Hub + Wochenheft Modul 2 · Woche 1.

Aufruf (Server läuft): python -X utf8 modul2/woche1/validate.py [http://localhost:5387/hefte]
Prüft für Ingo, Carmen, Tabea in Chrome und WebKit: alle Reiter, Lernkarten, Selbsttest, Training,
Use-Case-Werkzeuge mit Speicherung über Neuladen, Kopieren (Chrome liest die Zwischenablage zurück),
Downloads, Deep-Links, Tagesseiten-Banner, Leseseite, Übersicht und 320/390/1280 px ohne Querscrollen.
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://localhost:5387/hefte'
OUT = Path(__file__).resolve().parents[2] / 'build/modul2-woche1'
CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
PERSONS = ['ingo', 'carmen', 'tabea']
TABS = ['start', 'labor', 'vorlagen', 'training', 'learnings', 'karten', 'test', 'aufgaben', 'folien', 'woerter', 'heft']


def check_person(ctx, pid, engine, report):
    errors = []
    page = ctx.new_page()
    page.on('pageerror', lambda e: errors.append(f'pageerror {e}'))
    page.on('console', lambda m: errors.append(f'console {m.text}') if m.type == 'error' else None)
    hub = f'{BASE}/{pid}/modul-2/tag-5/'
    page.goto(hub)
    page.wait_for_load_state('networkidle')
    assert page.evaluate("document.querySelector('[aria-selected=true]').dataset.tab") == 'start'
    for t in TABS:
        page.click(f'[data-tab="{t}"]')
        vis = page.evaluate("[...document.querySelectorAll('.tpanel')].filter(p=>!p.hidden).map(p=>p.id)")
        assert vis == [t], (t, vis)
    # Lernkarten umdrehen und einsortieren
    page.click('[data-tab="karten"]')
    page.click('#karten .kcard')
    page.click('#karten .btn.primary')
    assert 'Karte 2 von 40' in page.inner_text('#karten')
    # Selbsttest
    page.click('[data-tab="test"]')
    page.click('#test .qopt >> nth=1')
    assert page.is_visible('#test .qwhy')
    # Training
    page.click('[data-tab="training"]')
    assert page.inner_text('#training .lt-dashboard').strip() or page.inner_text('#training .lt-stage').strip()
    # Learnings: Sitzt + Filter
    page.click('[data-tab="learnings"]')
    page.click('#lrn-l1 .lc-sitzt')
    page.click('[data-day-filter="5"]')
    assert page.evaluate("[...document.querySelectorAll('.lcard')].filter(c=>!c.hidden).length") == 12
    # Folien starten bei Use-Case-Folie 1 (= 35)
    page.click('[data-tab="folien"]')
    assert 'tag-24/35.jpg' in page.get_attribute('#folien .v-stage img', 'src')
    # Use-Case-Labor
    page.click('[data-tab="labor"]')
    page.once('dialog', lambda d: d.accept())
    page.click('[data-zf-demo]')
    page.fill('[data-save="sb1-name"]', 'Testfall ' + pid)
    page.fill('[data-save="sb1-nutzen"]', '12 Stunden pro Monat')
    page.select_option('[data-save="st1-standard"]', '3')
    page.check('[data-save="st1-k1"]')
    page.click('.tr-stage .btn.primary')
    page.wait_for_timeout(400)
    assert '✓' in page.inner_text('[data-sb-pane="1"] .sb-check')
    # Vorlagen: erledigt + Kopieren
    page.click('[data-tab="vorlagen"]')
    page.check('[data-save="vorlage-a1"]')
    page.wait_for_timeout(1200)
    page.click('#vorlage-a1 [data-copy-url]')
    page.wait_for_timeout(300)
    copied = page.inner_text('#vorlage-a1 [data-copy-url]')
    clip = None
    if engine == 'chromium':
        clip = page.evaluate('navigator.clipboard.readText()')
        assert json.loads(clip)['flow'][0]['module'] == 'util:SetVariable2'
    assert 'Kopiert' in copied, copied
    # Neuladen: alles noch da?
    page.reload()
    page.wait_for_load_state('networkidle')
    state = page.evaluate("""() => ({
      zf: document.querySelectorAll('.zf-row:not(.kopf)').length,
      name: document.querySelector('[data-save="sb1-name"]').value,
      st: document.querySelector('[data-save="st1-standard"]').value,
      vorl: document.querySelector('[data-vorlagen-count]').textContent,
      sitzt: document.querySelector('.hub-stat [data-v="sitzt"]').textContent,
      labor: +document.querySelector('[data-labor-count]').textContent})""")
    assert state['zf'] == 4 and state['name'] == 'Testfall ' + pid and state['st'] == '3' and state['vorl'] == '1' and state['sitzt'].startswith('1 von'), state
    # Downloads
    for href in page.eval_on_selector_all('#vorlagen a[download]', 'els => els.map(e => e.href)'):
        r = page.request.get(href)
        assert r.ok, href
    # Deep-Link von außen
    page.goto(hub + '?x=1#vorlage-a7')
    page.wait_for_timeout(1200)
    assert page.evaluate("document.querySelector('[aria-selected=true]').dataset.tab") == 'vorlagen'
    assert abs(page.evaluate("document.getElementById('vorlage-a7').getBoundingClientRect().top")) < 200
    # Breiten
    widths = {}
    for w in (320, 390, 1280):
        page.set_viewport_size({'width': w, 'height': 900})
        for t in ('start', 'labor', 'vorlagen'):
            page.click(f'[data-tab="{t}"]')
            over = page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            widths[f'{w}-{t}'] = over
            assert over <= 1, (w, t, over)
        if w == 390:
            page.click('[data-tab="start"]')
            page.screenshot(path=str(OUT / f'hub-{pid}-{engine}-390.png'), full_page=False)
    page.set_viewport_size({'width': 1280, 'height': 900})
    page.click('[data-tab="start"]')
    page.screenshot(path=str(OUT / f'hub-{pid}-{engine}-1280.png'))
    # Leseseite
    page.goto(hub + 'lernheft/')
    page.wait_for_load_state('networkidle')
    assert page.input_value('[data-save="sb1-name"]') == 'Testfall ' + pid
    for w in (320, 390):
        page.set_viewport_size({'width': w, 'height': 900})
        over = page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
        assert over <= 1, ('lernheft', w, over)
    page.set_viewport_size({'width': 1280, 'height': 900})
    # Tagesseiten Mo–Do: Reiter „Heute“ mit Vorlagen-Link, Lernhefte mit Hinweis-Kasten
    for d in (1, 2, 3, 4):
        page.goto(f'{BASE}/{pid}/modul-2/tag-{d}/')
        assert page.is_visible('#heute') and page.locator('#heute a[href*="#vorlage-a"]').count(), d
        page.goto(f'{BASE}/{pid}/modul-2/tag-{d}/lernheft/')
        assert page.is_visible('.hub-banner'), d
    # Übersicht
    page.goto(f'{BASE}/{pid}/')
    assert page.is_visible('.hub-station')
    page.close()
    errs = [e for e in errors if 'favicon' not in e]
    assert not errs, errs
    report.append(dict(person=pid, engine=engine, state=state, widths=widths, clipboard=bool(clip)))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = []
    with sync_playwright() as p:
        for engine in ('chromium', 'webkit'):
            kw = {'executable_path': CHROME} if engine == 'chromium' else {}
            b = getattr(p, engine).launch(**kw)
            for pid in PERSONS:
                ctx = b.new_context(permissions=['clipboard-read', 'clipboard-write'] if engine == 'chromium' else [])
                check_person(ctx, pid, engine, report)
                ctx.close()
            b.close()
    (OUT / 'validate.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print(f'OK: {len(report)} Prüfläufe (3 Personen × Chrome/WebKit) ohne Fehler')


if __name__ == '__main__':
    main()
