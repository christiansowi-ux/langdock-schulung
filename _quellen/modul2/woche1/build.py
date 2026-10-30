"""Baut Modul 2 · Woche 1: Make-Vorlagen (JSON + ZIP), Folien der Woche, Wochenheft-PDF und Prüfbilder.

Aus _quellen:  python -X utf8 -I modul2/woche1/build.py   (oder: python lernheft.py --tag 24)
Danach:        python build.py --web   (schreibt Hub, Wochenheft-Webseiten und Übersichten)
Einmalig vorher: modul2/woche1/folien_rendern.py (Use-Case-Folien 35–66)
"""
import json
import shutil
import sys
import zipfile
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
Q = HERE.parents[1]
ROOT = Q.parent
PUB = ROOT / 'plattform/public'
QA = Q / 'build/modul2-woche1'
MAT = PUB / 'material/modul2-woche1'
sys.path.insert(0, str(Q))

from modul2.woche1.blueprints import AUTOMATIONS, build_all, check  # noqa: E402
from modul2.woche1.daten import KLASSENBUCH, LERNHEFT, MAKE_N, UC_N  # noqa: E402
from modul2.woche1.hub import render_print, FOLIEN_PDF  # noqa: E402
from modul2.woche1.inhalt import ZIP  # noqa: E402

CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
OUT_DIR = ROOT / 'Modul 2 - KI-Automation/Wochenheft Woche 1'

START = '''MAKE-VORLAGEN · MODUL 2 · WOCHE 1 (Stand 30.10.2026)
====================================================

Neun sehr leichte Szenarien für Make Free. Kein fremdes Konto nötig
(A5 liest nur eine öffentliche Test-API ohne Anmeldung).
Keine Vorlage verschickt, veröffentlicht oder speichert etwas außerhalb von Make.

SO GEHT DER IMPORT
1. ZIP entpacken (Rechtsklick > Alle extrahieren / am Mac Doppelklick).
2. In Make links "Scenarios" > "+ Create a new scenario".
3. Oben rechts die drei Punkte (...) > "Import blueprint" > "Choose file".
4. Eine .blueprint.json-Datei wählen > "Save".
5. Unten speichern (Diskette) und "Run once" klicken.
6. Auf die Sprechblase über dem letzten Modul klicken > OUTPUT.

Zeitplan bitte AUS lassen. Jeder Lauf kostet etwa 1 Credit pro ausgeführtem Modul.
Für alle neun Vorlagen mit je zwei Tests rund 40 Credits einplanen.
Ausführliche Erklärung jeder Einstellung: Wochenheft, Teil B.

{liste}
'''


def vorlagen():
    MAT.mkdir(parents=True, exist_ok=True)
    files = build_all()
    names = []
    for name, bp in files.items():
        check(bp)
        text = json.dumps(bp, ensure_ascii=False, indent=2)
        assert len(text.encode()) < 2_000_000
        (MAT / name).write_text(text, encoding='utf8')
        names.append(name)
    liste = '\n'.join(f'A{a["nr"]}  {a["titel"]:<44} Tag {a["tag"]}  ->  {a["soll"].splitlines()[0]}' for a in AUTOMATIONS)
    start = START.format(liste=liste)
    (MAT / 'START_HIER.txt').write_text(start, encoding='utf8')
    with zipfile.ZipFile(MAT / ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('Make-Vorlagen-Woche1/START_HIER.txt', start)
        for name in names:
            z.write(MAT / name, f'Make-Vorlagen-Woche1/{name}')
    return names


def folien():
    src, dst = PUB / 'folien/tag-20', PUB / 'folien/tag-24'
    dst.mkdir(parents=True, exist_ok=True)
    for i in range(1, MAKE_N + 1):
        for pre in ('', 't'):
            shutil.copy2(src / f'{pre}{i:02d}.jpg', dst / f'{pre}{i:02d}.jpg')
    for i in range(1, MAKE_N + UC_N + 1):
        assert (dst / f'{i:02d}.jpg').exists() and (dst / f't{i:02d}.jpg').exists(), i
    out = fitz.open()
    out.insert_pdf(fitz.open(src / 'Folien_Modul2_Tag1.pdf'))
    out.insert_pdf(fitz.open(dst / 'Folien_Modul2_Tag5_Use-Cases.pdf'))
    assert len(out) == MAKE_N + UC_N
    out.save(dst / FOLIEN_PDF, garbage=3, deflate=True)
    return len(out)


def pdf():
    from playwright.sync_api import sync_playwright
    QA.mkdir(parents=True, exist_ok=True)
    html = QA / 'wochenheft-druck.html'
    html.write_text(render_print(), encoding='utf8')
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUT_DIR / LERNHEFT
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        page = b.new_page()
        page.goto(html.as_uri())
        page.wait_for_timeout(800)
        page.emulate_media(media='print')
        page.pdf(path=str(target), format='A4', print_background=True, prefer_css_page_size=True)
        b.close()
    shutil.copy2(target, PUB / 'pdf' / LERNHEFT)
    doc = fitz.open(target)
    shots = QA / 'pdf'
    shots.mkdir(exist_ok=True)
    for n, pg in enumerate(doc, 1):
        pg.get_pixmap(dpi=60).save(shots / f'p{n:02d}.png')
    for first in range(1, len(doc) + 1, 12):
        sheet = Image.new('RGB', (1240, 1400), '#d9ddd9')
        d = ImageDraw.Draw(sheet)
        for off, n in enumerate(range(first, min(first + 12, len(doc) + 1))):
            im = Image.open(shots / f'p{n:02d}.png')
            im.thumbnail((298, 430))
            x, y = off % 4 * 310 + 6, off // 4 * 465 + 22
            sheet.paste(im, (x, y))
            d.text((x, y - 16), str(n), fill='black')
        sheet.save(QA / f'kontakt-{first:02d}.jpg', quality=88)
    return len(doc)


def klassenbuch():
    text = '# Wochenübersicht Modul 2 · 26.–30.10.2026\n\nPlan nach Folien, nicht das Protokoll des tatsächlichen Unterrichts.\n\n' + ''.join(
        f'## {d} – {t}\n\n' + ''.join(f'- {x}\n' for x in pts) + '\n' for d, t, pts in KLASSENBUCH)
    (HERE / 'klassenbuch-26-30-10-2026.md').write_text(text, encoding='utf8')


def main():
    names = vorlagen()
    n_fol = folien()
    pages = pdf()
    klassenbuch()
    report = dict(vorlagen=len(names), folien=n_fol, pdf_seiten=pages, pdf=str(OUT_DIR / LERNHEFT))
    (QA / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
