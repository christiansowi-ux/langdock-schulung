"""Baut Modul 2 · Tag 6: Make-Vorlagen (JSON + ZIP), Lernheft-PDF und Prüfbilder.

Aus _quellen:  python -X utf8 modul2/woche2/build.py   (oder: python lernheft.py --tag 25)
Danach:        python build.py --web   (schreibt Tagesseite, Leseseite, Präsenter-Modus und Übersichten)
Einmalig vorher: modul2/woche1/folien_rendern.py mit ordner='tag-25'
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
QA = Q / 'build/modul2-woche2'
MAT = PUB / 'material/modul2-woche2'
sys.path.insert(0, str(Q))

from modul2.woche1.blueprints import check  # noqa: E402
from modul2.woche2.daten import LERNHEFT  # noqa: E402
from modul2.woche2.hub import render_print  # noqa: E402
from modul2.woche2.vorlagen import AUTOMATIONS, ZIP, build_all  # noqa: E402

CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
OUT_DIR = ROOT / 'Modul 2 - KI-Automation/Lektion 3 - Bewerten und Rechnen'

START = '''MAKE-VORLAGEN · MODUL 2 · TAG 6 (Stand 02.11.2026)
=================================================

Zwei sehr leichte Rechen-Szenarien für Make Free. Kein fremdes Konto nötig.
Keine Vorlage verschickt, veröffentlicht oder speichert etwas außerhalb von Make.

SO GEHT DER IMPORT
1. ZIP entpacken (Rechtsklick > Alle extrahieren / am Mac Doppelklick).
2. In Make links "Scenarios" > "+ Create a new scenario".
3. Oben rechts die drei Punkte (...) > "Import blueprint" > "Choose file".
4. Eine .blueprint.json-Datei wählen > "Save".
5. Unten speichern (Diskette) und "Run once" klicken.
6. Auf die Sprechblase über dem letzten Modul klicken > OUTPUT.

Zeitplan bitte AUS lassen. Jeder Lauf kostet etwa 1 Credit pro ausgeführtem Modul.
Ausführliche Erklärung jeder Einstellung: Lernheft Tag 6, Reiter Vorlagen.

{liste}
'''


def vorlagen():
    MAT.mkdir(parents=True, exist_ok=True)
    files = build_all()
    names = []
    for name, bp in files.items():
        check(bp)
        text = json.dumps(bp, ensure_ascii=False, indent=2)
        (MAT / name).write_text(text, encoding='utf8')
        names.append(name)
    liste = '\n'.join(f'A{a["nr"]}  {a["titel"]:<36} ->  {a["soll"].splitlines()[0]}' for a in AUTOMATIONS)
    start = START.format(liste=liste)
    (MAT / 'START_HIER.txt').write_text(start, encoding='utf8')
    with zipfile.ZipFile(MAT / ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('Make-Vorlagen-Tag6/START_HIER.txt', start)
        for name in names:
            z.write(MAT / name, f'Make-Vorlagen-Tag6/{name}')
    return names


def pdf():
    from playwright.sync_api import sync_playwright
    QA.mkdir(parents=True, exist_ok=True)
    html = QA / 'lernheft-druck.html'
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


def main():
    names = vorlagen()
    pages = pdf()
    report = dict(vorlagen=len(names), pdf_seiten=pages, pdf=str(OUT_DIR / LERNHEFT))
    (QA / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
