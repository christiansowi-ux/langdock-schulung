"""Rendert die Use-Case-Präsentation (gebündelte HTML aus Downloads) zu Originalfolien.

Aufruf (einmalig, aus _quellen):
  python -X utf8 -I modul2/woche1/folien_rendern.py "C:/Users/chris/Downloads/Use_Cases_identifizieren_v2 (2).html"

Weitere Präsentation: ... <html> <ordner> <offset> <anzahl> <pdfname>
Tag 6: ... tag-25 0 29 Folien_Modul2_Tag6_Bewerten-und-Rechnen.pdf
Ergebnis: plattform/public/folien/<ordner>/NN.jpg (1600 px), tNN.jpg (360 px) und das Folien-PDF.
Die HTML läuft nur im lokalen Headless-Chrome.
"""
import json
import sys
from pathlib import Path

import fitz
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
FOLIEN = ROOT / 'plattform/public/folien'
CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'


def main(src, ordner='tag-24', offset=34, anzahl=32, pdfname='Folien_Modul2_Tag5_Use-Cases.pdf'):
    """offset 34 bei Tag 5: 1–34 sind dort die Make-Folien (Kopie aus tag-20)."""
    OUT = FOLIEN / ordner
    OUT.mkdir(parents=True, exist_ok=True)
    pdf = OUT / pdfname
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        page.goto(Path(src).resolve().as_uri())
        page.wait_for_timeout(6000)
        count = page.evaluate("document.querySelectorAll('deck-stage > section').length")
        page.emulate_media(media='print')
        page.pdf(path=str(pdf), width='1920px', height='1080px', print_background=True, prefer_css_page_size=True)
        browser.close()
    doc = fitz.open(pdf)
    assert len(doc) == count == anzahl, (len(doc), count)
    for i, pg in enumerate(doc, 1):
        zoom = 1600 / pg.rect.width
        nr = offset + i
        tmp = OUT / f'{nr:02d}.png'
        pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(tmp)
        im = Image.open(tmp).convert('RGB')
        im.save(OUT / f'{nr:02d}.jpg', quality=86, optimize=True)
        im.resize((360, round(360 * im.height / im.width))).save(OUT / f't{nr:02d}.jpg', quality=82)
        tmp.unlink()
    print(json.dumps({'slides': len(doc), 'pdf': str(pdf)}))


if __name__ == '__main__':
    a = sys.argv[1:]
    main(a[0], *(a[1:2]), *(int(x) for x in a[2:4]), *(a[4:5]))
