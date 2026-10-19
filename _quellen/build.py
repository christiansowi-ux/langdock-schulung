"""Praxisblock Langdock - baut die Arbeitshefte als PDF.

    python build.py [--tag 1|2|3] [--preview]   |   python build.py --web  (Plattform, siehe plattform.py)
      Tag 1 (Standard): ../Langdock_Praxisblock_*.pdf
      Tag 2 Modellauswahl: ../Tag 2 - Modellauswahl/Langdock_Tag2_Modellauswahl_*.pdf  (Quellen in tag2/)
    Zwischenstand in build/ (mit --preview auch build/preview/<Tag>_<Heft>_<Seite>.png)
"""
import base64, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
BUILD = os.path.join(HERE, 'build')

INFO = ('<svg class="i" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="#006ed6" stroke-width="2"/>'
        '<line x1="12" y1="11" x2="12" y2="17" stroke="#006ed6" stroke-width="2.2" stroke-linecap="round"/>'
        '<circle cx="12" cy="7.4" r="1.35" fill="#006ed6"/></svg>')

CHECKBOX = ('<span style="display:inline-block;flex:0 0 31mm;text-align:center"><span style="display:inline-block;width:3.9mm;height:3.9mm;'
            'border:.35mm solid #111;border-radius:.7mm;vertical-align:-.6mm"></span></span>')

LEGEND_1 = f'''<div class="legend">
  <div><span class="where new">Neuer Chat</span><span>neuen Chat öffnen, dann den Prompt eingeben</span></div>
  <div><span class="where same">Im selben Chat</span><span>im bisherigen Chat weiterschreiben</span></div>
  <div><span class="where img">Bild-Schaltfläche</span><span>Bild von Langdock erzeugen lassen</span></div>
  <div><span class="tag ph">[eckige Klammern]</span><span>durch eigene Angaben ersetzen</span></div>
  <div><span class="tag watch">Beobachten</span><span>darauf beim Ergebnis achten</span></div>
  <div><span class="tag merke">Merke</span><span>das Wichtigste zum Mitnehmen</span></div>
  <div><span class="tag safe">Sicher</span><span>Datenschutz und Verantwortung</span></div>
  <div>{CHECKBOX}<span>erledigt? abhaken</span></div>
</div>'''

LEGEND_2 = '''<div class="legend">
  <div><span class="where new">Neuer Chat</span><span>neuen Chat öffnen, dann den Prompt eingeben</span></div>
  <div><span class="where same">Im selben Chat</span><span>im Chat weiterschreiben</span></div>
  <div><span class="where model">Modell 1</span><span>notiertes Modell wählen</span></div>
  <div><span class="where think">Thinking an</span><span>Reasoning an (Umriss = aus)</span></div>
  <div><span class="where web">Websuche an</span><span>Websuche an (Umriss = aus)</span></div>
  <div><span class="where img">Bild-Schaltfläche</span><span>Bild erzeugen lassen</span></div>
  <div><span class="tag ph">[eckige Klammern]</span><span>eigene Angaben einsetzen</span></div>
  <div><span class="tag sol">Kontrolllösung</span><span>steht Kopf – erst danach drehen</span></div>
</div>'''

BILANZ_1 = '''<div class="keep" style="margin-top:7mm">
  <h4>Hype oder Realität? – die eigene Bilanz nach heute</h4>
  <p>Wie in Lektion 1: Wo ist KI schon besser – und wo muss sie noch aufholen? Diesmal aus eigener Erfahrung, im eigenen Fachgebiet.</p>
  <table class="fill full tall">
    <tr><th>Hier war Langdock heute richtig stark</th><th>Hier musste man korrigieren oder Fachwissen einbringen</th></tr>
    <tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr>
  </table>
</div>
<div class="keep" style="margin-top:6mm">
  <h4>Für den nächsten Schulungstag</h4>
  <p class="small">Wofür setzt man den eigenen Copilot als Erstes ein?</p>
  <div class="lines full" style="--n:2"></div>
  <p class="small">Welche Frage soll beim nächsten Mal geklärt werden?</p>
  <div class="lines full" style="--n:2"></div>
</div>'''

BILANZ_2 = '''<div class="keep" style="margin-top:5mm">
  <h4>Zum Mitnehmen: der Modellwahl-Check</h4>
  <p>Diesen Prompt in der Prompt-Bibliothek speichern – damit lässt sich jede neue Aufgabe in einer Minute einordnen.</p>
  <div class="prompt full"><div class="lbl">Prompt für die Prompt-Bibliothek</div>
    <p>Welches Modell in meinem Langdock-Workspace passt zu dieser Aufgabe: <span class="ph">[Aufgabe]</span>? Prüfe Reasoning, Input, Output, Kontextfenster, Kosten, Tempo, Datenschutz, Lizenz und Deutsch. Empfiehl die kleinste Option, die den Job zuverlässig erledigt, sag, ob Thinking nötig ist – und ob ein Spezialwerkzeug außerhalb von Langdock besser passt.</p></div>
</div>
<div class="keep" style="margin-top:5mm">
  <h4>Meine Modell-Landkarte</h4>
  <p>Vier Aufgaben aus dem eigenen Arbeitsalltag – und welches Modell man ab morgen dafür nimmt.</p>
  <table class="fill full">
    <tr><th>Aufgabe aus dem eigenen Alltag</th><th style="width:40mm">Modell</th><th style="width:20mm">Thinking?</th><th>Warum? (welche der 9 Fragen)</th></tr>
    <tr><td style="height:10mm"></td><td></td><td></td><td></td></tr><tr><td style="height:10mm"></td><td></td><td></td><td></td></tr>
    <tr><td style="height:10mm"></td><td></td><td></td><td></td></tr><tr><td style="height:10mm"></td><td></td><td></td><td></td></tr>
  </table>
</div>
<div class="keep" style="margin-top:5mm">
  <h4>Für den nächsten Schulungstag</h4>
  <p class="small">Welche Frage soll beim nächsten Mal geklärt werden?</p>
  <div class="lines full" style="--n:2"></div>
</div>'''

LEGEND_3 = f'''<div class="legend">
  <div><span class="where new">Neuer Chat</span><span>Langdock: neuen Chat öffnen</span></div>
  <div><span class="where same">Im selben Chat</span><span>Langdock: im Chat weiterschreiben</span></div>
  <div><span class="where lab">Prompt-Labor</span><span>Schritt auf prompt.veluna-labs.de</span></div>
  <div><span class="fref">Folie 5</span><span>passende Folie aus der Lektion</span></div>
  <div><span class="tag watch">Beobachten</span><span>darauf beim Ergebnis achten</span></div>
  <div><span class="tag sol">Kontrolllösung</span><span>steht Kopf – erst danach drehen</span></div>
  <div><span class="zl">Zusatz</span><span>freiwillig, für den eigenen Bereich</span></div>
  <div>{CHECKBOX}<span>erledigt? abhaken</span></div>
</div>'''

LEGEND_4 = LEGEND_3.replace('<span class="where lab">Prompt-Labor</span><span>Schritt auf prompt.veluna-labs.de</span>',
                             '<span class="where lab">RAG Rescue</span><span>Schritt auf rag.veluna-labs.de</span>')

TAGE = {
    '1': {
        'dir': '', 'out': OUT, 'legend': LEGEND_1, 'bilanz': BILANZ_1, 'subject': 'Praxisblock Langdock',
        'hefte': [
            ('A', 'a_druck.html',    'Langdock_Praxisblock_A_Druck-und-Vertrieb.pdf',          'Druck &amp; Vertrieb'),
            ('B', 'b_business.html', 'Langdock_Praxisblock_B_Teamleitung-Business-Website.pdf', 'Teamleitung, Business &amp; Website'),
            ('C', 'c_creative.html', 'Langdock_Praxisblock_C_Video-Design-Creative.pdf',        'Video, Design &amp; Creative Direction'),
        ],
    },
    '2': {
        'dir': 'tag2', 'out': os.path.join(OUT, 'Tag 2 - Modellauswahl'), 'legend': LEGEND_2, 'bilanz': BILANZ_2,
        'subject': 'Praxisblock Langdock - Tag 2 Modellauswahl', 'compact': True,
        'hefte': [
            ('A', 'a_druck.html',    'Langdock_Tag2_Modellauswahl_A_Druck-und-Vertrieb.pdf',          'Modellauswahl &nbsp;·&nbsp; Druck &amp; Vertrieb'),
            ('B', 'b_business.html', 'Langdock_Tag2_Modellauswahl_B_Teamleitung-Business-Website.pdf', 'Modellauswahl &nbsp;·&nbsp; Teamleitung, Business &amp; Website &nbsp;·&nbsp; für Mac'),
            ('C', 'c_creative.html', 'Langdock_Tag2_Modellauswahl_C_Video-Design-Creative.pdf',        'Modellauswahl &nbsp;·&nbsp; Video, Design &amp; Creative'),
        ],
    },
    '3': {
        'dir': 'tag3', 'out': os.path.join(OUT, 'Tag 3 - LLMs unter der Lupe'), 'legend': LEGEND_3, 'bilanz': '',
        'subject': 'Praxisblock Langdock - Tag 3 LLMs unter der Lupe', 'compact': True, 'personen': 'heft.html',
        'pdfname': 'Langdock_Tag3_LLMs-unter-der-Lupe_{Name}.pdf', 'label': 'LLMs unter der Lupe &nbsp;·&nbsp; {Name} &nbsp;·&nbsp; {fach}',
        'hefte': [],
    },
    '4': {
        'dir': 'tag4', 'out': os.path.join(OUT, 'Tag 4 - RAG'), 'legend': LEGEND_4, 'bilanz': '',
        'subject': 'Praxisblock Langdock - Tag 4 RAG', 'compact': True, 'personen': 'heft.html',
        'pdfname': 'Langdock_Tag4_RAG_{Name}.pdf', 'label': 'RAG &nbsp;·&nbsp; {Name} &nbsp;·&nbsp; {fach}',
        'hefte': [],
    },
}


def read(*parts):
    with open(os.path.join(HERE, *parts), encoding='utf-8') as f:
        return f.read()


# ---------- Personen und Learnings (Daten in kurs.py) ----------
sys.path.insert(0, HERE)
import kurs  # noqa: E402

PROFIL_PERSON = {v['profil']: k for k, v in kurs.PERSONEN.items()}   # A -> ingo, B -> carmen, C -> tabea
ICONS = {'A': '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"><path d="M14 18V6h20v12"/><rect x="6" y="18" width="36" height="16" rx="3"/><path d="M14 28h20v14H14z"/><path d="M18 33h12M18 37h8"/></svg>',
         'B': '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"><rect x="5" y="7" width="38" height="29" rx="3"/><path d="M5 14h38"/><path d="M14 31v-5M21 31v-9M28 31v-7M35 31v-12"/><path d="M17 42h14M24 36v6"/></svg>',
         'C': '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"><rect x="4" y="17" width="28" height="21" rx="3"/><path d="M32 23.5l11-6v20l-11-6z"/><circle cx="12" cy="10.5" r="4.5"/><circle cx="24" cy="10.5" r="4.5"/></svg>'}


def esc(s):
    import html as h
    return h.escape(str(s), quote=True)


def person_vars(pid):
    p = kurs.PERSONEN[pid]
    mac = p['mac']
    return {
        'name': esc(p['name']), 'Name': p['name'], 'fach': esc(p['fach']), 'fach_kurz': esc(p['fach']),
        'icon': ICONS[p['profil']].replace('currentColor', '#1a6b5a'),
        'zip': ('am Mac im Finder den Ordner „Downloads“ öffnen und die ZIP-Datei doppelklicken – der Ordner entpackt sich von selbst.' if mac
                else 'im Ordner „Downloads“ mit der rechten Maustaste auf die ZIP-Datei klicken → „Alle extrahieren …“.'),
        'foto': ('am Mac: <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>4</kbd> und den Bereich aufziehen' if mac
                 else 'unter Windows: <kbd>Windows</kbd> <kbd>⇧</kbd> <kbd>S</kbd>'),
    }


def zusatz_blocks(cfg, pid):
    """tagN/zusatz_<person>.html in Bloecke <!-- Z1 --> ... zerlegen und als freiwillige Zusatzaufgaben einrahmen."""
    raw = read(cfg['dir'], f'zusatz_{pid}.html')
    parts = re.split(r'<!--\s*Z(\d)\s*-->', raw)
    fach = esc(kurs.PERSONEN[pid]['fach'])
    out = {}
    for i in range(1, len(parts), 2):
        n, body = parts[i], parts[i + 1].strip()
        m = re.match(r'<h3>(.*?)</h3>\s*(<span class="time">.*?</span>)\s*(<p class="goal">.*?</p>)', body, re.S)
        assert m, f'Zusatz {n} ({pid}) braucht <h3>, <span class="time"> und <p class="goal">'
        rest = body[m.end():]
        out[n] = (f'<div class="zusatz" data-zusatz="{n}">'
                  f'<div class="zusatz-top"><div class="zusatz-head"><span class="zlabel">Zusatzaufgabe {n} · freiwillig · {fach}</span></div>'
                  f'<div class="task-head z"><h3>{m.group(1)}</h3>{m.group(2)}</div>{m.group(3)}</div>{rest}</div>')
    return out


def learnings_html(tag, thumbs=None):
    """Abschnitt "Die Learnings von Tag N" (Heftende und Lernblatt). thumbs = URL-Muster fuer Folien-Vorschaubilder."""
    t = kurs.TAGE[int(tag)]
    items = []
    for i, l in enumerate(t['learnings'], 1):
        fref = f'<span class="fref" data-folie="{l["folie"]}">Folie {l["folie"]}</span>' if l['folie'] else f'<span class="fref aus">{"Quelle: " + esc(l["quelle"]) if l.get("quelle") else "Aus dem Arbeitsheft"}</span>'
        pic = ''
        if thumbs:
            img = f'<img class="lrn-thumb" alt="Folie {l["folie"]}" src="{thumbs.format(n=l["folie"])}">' if l['folie'] else ''
            pic = f'<div class="lrn-pic">{img}</div>'
        items.append(f'<li data-lrn="{l["id"]}"><div class="lrn-no">{i}</div><div class="lrn-body"><b class="lrn-satz">{esc(l["satz"])}</b>'
                     f'<p>{esc(l["erklaert"])}</p>{fref}</div>{pic}</li>')
    words = ''.join(f'<div><b>{esc(a)}</b>{esc(b)}</div>' for a, b in t['begriffe'])
    return (f'<section class="section lrn-section" data-lrn-tag="{tag}">'
            f'<div class="sec-head"><div class="sec-no">Zum Nachlernen</div><h2>Die Learnings von Tag {tag}</h2>'
            f'<p>{esc(t["titel"])} – das Wichtigste in kurzen Sätzen, jeweils einfach erklärt und mit der passenden Folie.</p></div>'
            f'<div class="lrn-tools"></div>'
            f'<ol class="lrn{" thumbs" if thumbs else ""}">{"".join(items)}</ol>'
            f'<div class="keep lrn-wordbox"><h4>Die Wörter des Tages</h4><div class="lrn-words">{words}</div></div></section>')


def compose(cfg, src, head, logo, tag, pid=None):
    """Ein Heft aus Quelle + Bausteinen zusammensetzen (gemeinsam fuer PDF und Web)."""
    html = read(cfg['dir'], src)
    html = re.sub(r'\{\{FRAG:(\w+)\}\}', lambda m: read(cfg['dir'], m.group(1) + '.html'), html)
    if pid:
        pv = person_vars(pid)
        html = re.sub(r'\{\{P:(\w+)\}\}', lambda m: pv[m.group(1)], html)
        z = zusatz_blocks(cfg, pid)
        html = re.sub(r'\{\{ZUSATZ:(\d)\}\}', lambda m: z[m.group(1)], html)
    if '{{GRUNDLAGEN}}' in html:
        html = html.replace('{{GRUNDLAGEN}}', read(cfg['dir'], 'grundlagen.html'))
    lrn = learnings_html(tag)
    if '{{LEARNINGS}}' in html:
        html = html.replace('{{LEARNINGS}}', lrn)
    else:
        html = html.replace('</body>', lrn + '\n</body>', 1)
    for k, val in (('{{HEAD}}', head), ('{{LEGEND}}', cfg['legend']), ('{{BILANZ}}', cfg['bilanz']), ('{{LOGO}}', logo), ('{{I}}', INFO)):
        html = html.replace(k, val)
    if cfg.get('compact'):
        html = re.sub(r'<table class="fill"(?=[ >])', '<table class="fill compact"', html)
    html = re.sub(r'(<div class="task-head">.*?</div>\s*<p class="goal">.*?</p>)', r'<div class="task-top">\1</div>', html, flags=re.S)
    if '{{' in html:
        i = html.index('{{')
        raise AssertionError(f'Platzhalter uebrig in {src}: {html[i:i + 40]}')
    return html


def hefte_of(tag):
    """[(key, src, pdf, label, person)] - Tag 1/2 je Profil, ab Tag 3 ein Heft je Person aus einer Vorlage."""
    cfg = TAGE[tag]
    if cfg.get('personen'):
        out = []
        for pid in kurs.REIHENFOLGE:
            p = kurs.PERSONEN[pid]
            out.append((p['profil'], cfg['personen'], cfg['pdfname'].format(Name=p['name']),
                        cfg['label'].format(Name=p['name'], fach=esc(p['fach'])), pid))
        return out
    return [(k, src, pdf, label, PROFIL_PERSON[k]) for k, src, pdf, label in cfg['hefte']]


def main():
    if '--web' in sys.argv:
        import plattform
        return plattform.build()
    tag = sys.argv[sys.argv.index('--tag') + 1] if '--tag' in sys.argv else '1'
    cfg = TAGE[tag]
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(cfg['out'], exist_ok=True)
    with open(os.path.join(HERE, 'futureway_logo.png'), 'rb') as f:
        logo = 'data:image/png;base64,' + base64.b64encode(f.read()).decode()
    head = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
            '<style>' + read('style.css') + '</style>')

    jobs = []
    for key, src, pdf, label, pid in hefte_of(tag):
        html = compose(cfg, src, head, logo, tag, pid if cfg.get('personen') else None)
        dst = os.path.join(BUILD, f't{tag}_{pid}.html')
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(html)
        jobs.append({'html': dst, 'pdf': os.path.join(BUILD, pdf), 'pdfPlain': os.path.join(BUILD, 'plain_' + pdf),
                     'label': label, 'final': os.path.join(cfg['out'], pdf), 'key': key, 'pid': pid})

    jobfile = os.path.join(BUILD, 'jobs.json')
    with open(jobfile, 'w', encoding='utf-8') as f:
        json.dump(jobs, f)
    subprocess.run(['node', os.path.join(HERE, 'render.mjs'), jobfile], check=True)

    # Titelseite ohne Fusszeile, Rest mit Fusszeile
    from pypdf import PdfReader, PdfWriter
    for job in jobs:
        full, plain = PdfReader(job['pdf']), PdfReader(job['pdfPlain'])
        assert len(full.pages) == len(plain.pages)
        w = PdfWriter()
        w.add_page(plain.pages[0])
        for p in full.pages[1:]:
            w.add_page(p)
        w.add_metadata({'/Title': os.path.splitext(os.path.basename(job['final']))[0].replace('_', ' '),
                        '/Author': 'Futureway KI Institut', '/Subject': 'KI Automations Spezialist - ' + cfg['subject']})
        with open(job['final'], 'wb') as f:
            w.write(f)
        print(f"{os.path.basename(job['final'])}: {len(full.pages)} Seiten")

    if '--preview' in sys.argv:
        import fitz
        pv = os.path.join(BUILD, 'preview')
        os.makedirs(pv, exist_ok=True)
        for job in jobs:
            doc = fitz.open(job['final'])
            for i, page in enumerate(doc):
                page.get_pixmap(dpi=70).save(os.path.join(pv, f"T{tag}{job['pid']}_{i + 1:02d}.png"))


if __name__ == '__main__':
    main()
