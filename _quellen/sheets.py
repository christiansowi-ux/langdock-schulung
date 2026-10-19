"""Uebersichtsboegen aus build/preview: python sheets.py T2A T2B T2C -> build/preview/sheet_<prefix>.png"""
import glob, os, sys
from PIL import Image

PV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build', 'preview')
for pre in sys.argv[1:]:
    files = sorted(glob.glob(os.path.join(PV, pre + '_*.png')))
    ims = [Image.open(f) for f in files]
    w, h = ims[0].size
    cols = 7
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w + (cols + 1) * 10, rows * h + (rows + 1) * 10), (120, 120, 120))
    for i, im in enumerate(ims):
        sheet.paste(im, (10 + (i % cols) * (w + 10), 10 + (i // cols) * (h + 10)))
    sheet.save(os.path.join(PV, 'sheet_' + pre + '.png'))
    print(pre, len(ims))
