"""Tag 4 (RAG): ausgedachte Uebungsdokumente als PDF + ZIP + kleine Download-Seite.

    python tag4/material.py      -> ../plattform/public/material/tag-4/  (PDFs, ZIP, index.html)

Alle Firmen, Preise und Regeln sind erfunden. SalesFlow-Zahlen passen zu den Folien 4, 5, 11 und 13
(89 EUR, 15 % ab zehn Lizenzen, 12 Monate Mindestlaufzeit) und zum Fall 01 in RAG Rescue.
"""
import json
import os
import subprocess
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'plattform', 'public', 'material', 'tag-4')
TMP = os.path.join(HERE, '..', 'build', 'material4')

CSS = """
@page { size: A4; margin: 18mm 18mm 18mm 18mm; }
* { box-sizing: border-box; }
body { font-family: Arial, Helvetica, sans-serif; color: #222; font-size: 10.5pt; line-height: 1.5; margin: 0; }
.head { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid var(--c); padding-bottom: 8px; margin-bottom: 14px; }
.brand { font-weight: 800; font-size: 17pt; color: var(--c); letter-spacing: -.01em; }
.brand small { display: block; font-weight: 400; font-size: 8.5pt; color: #666; letter-spacing: 0; }
.uebung { font-size: 8pt; color: #a33; border: 1px solid #e3b5b5; border-radius: 4px; padding: 3px 7px; }
h1 { font-size: 20pt; margin: 6px 0 10px; line-height: 1.15; }
table.meta { border-collapse: collapse; margin: 0 0 16px; font-size: 9.5pt; }
table.meta td { padding: 3px 14px 3px 0; vertical-align: top; }
table.meta td:first-child { color: #666; }
h2 { font-size: 12.5pt; margin: 16px 0 6px; color: var(--c); }
p { margin: 0 0 8px; }
table.t { border-collapse: collapse; width: 100%; margin: 4px 0 10px; font-size: 10pt; }
table.t th, table.t td { border: 1px solid #ccc; padding: 5px 8px; text-align: left; }
table.t th { background: #f2f2f2; }
.foot { margin-top: 22px; border-top: 1px solid #ccc; padding-top: 6px; font-size: 8pt; color: #777; }
.promo h1 { font-size: 30pt; color: var(--c); }
.promo .claim { font-size: 15pt; font-weight: 700; margin: 6px 0 14px; }
.promo .box { background: #f4f6fb; border-radius: 8px; padding: 12px 14px; margin: 10px 0; }
"""

SF = ('SalesFlow Solutions GmbH', 'CRM-Software für Vertriebsteams · fiktives Unternehmen', '#1f4e8c')
DOCS = [
    # dateiname, marke, titel, meta, inhalt, css-klasse
    ('01_SalesFlow_Preisliste_Juli-2026', SF, 'Preisliste SalesFlow – Juli 2026',
     [('Herausgeber', 'SalesFlow Solutions · Finance'), ('Stand', 'Juli 2026'), ('Gültig ab', '01.07.2026'), ('Status', 'freigegeben'), ('Dokumenttyp', 'Preisliste')],
     """<h2>1. Lizenzpreise</h2>
<table class="t"><tr><th>Tarif</th><th>Preis</th><th>Hinweis</th></tr>
<tr><td>SalesFlow Basic</td><td>39,00 Euro pro aktivem Nutzer und Monat</td><td>für kleine Teams</td></tr>
<tr><td>SalesFlow Professional</td><td>89,00 Euro pro aktivem Nutzer und Monat</td><td>für wachsende Vertriebsteams</td></tr>
<tr><td>SalesFlow Enterprise</td><td>individuelles Angebot</td><td>ab 100 Nutzern</td></tr></table>
<h2>2. Abrechnung</h2>
<p>Alle Preise verstehen sich netto zuzüglich Umsatzsteuer. Abgerechnet wird monatlich nach der Zahl der gebuchten Lizenzen. Mengenrabatte werden nach der jeweils gültigen Rabattregel auf den Lizenzpreis angewendet.</p>
<h2>3. Zusatzleistungen</h2>
<p>Einrichtungspaket (optional): 490,00 Euro einmalig. Online-Schulung für ein Team (2 Stunden): 250,00 Euro. Für Zusatzleistungen gelten keine Mengenrabatte.</p>
<h2>4. Ersetzt</h2>
<p>Diese Preisliste ersetzt alle früheren Preislisten.</p>""", ''),
    ('02_SalesFlow_Rabattregeln_Geschaeftskunden', SF, 'Rabattregeln für Geschäftskunden',
     [('Herausgeber', 'SalesFlow Solutions · Finance'), ('Stand', 'Juni 2026'), ('Status', 'freigegeben, verbindlich'), ('Dokumenttyp', 'Rabattregel')],
     """<h2>1. Mengenrabatt Professional</h2>
<p>Ab zehn gleichzeitig gebuchten Professional-Lizenzen gelten 15 Prozent Mengenrabatt auf den monatlichen Lizenzpreis.</p>
<h2>2. Berechnungsweise</h2>
<p>Der Rabatt wird auf die Summe aller Professional-Lizenzen angewendet. Beispiel: 10 Lizenzen × 89,00 Euro = 890,00 Euro; abzüglich 15 Prozent (133,50 Euro) ergibt 756,50 Euro netto im Monat.</p>
<h2>3. Basic und Enterprise</h2>
<p>Für SalesFlow Basic gibt es keine Mengenrabatte. Enterprise-Konditionen werden im individuellen Angebot festgelegt.</p>
<h2>4. Ausnahmen</h2>
<p>Schulungen, Einrichtungspakete und Beratungsleistungen sind von Lizenzrabatten ausgenommen.</p>""", ''),
    ('03_SalesFlow_Vertragsbedingungen_Professional', SF, 'Vertragsbedingungen SalesFlow Professional',
     [('Herausgeber', 'SalesFlow Solutions · Vertragsmanagement'), ('Stand', 'Mai 2026'), ('Status', 'freigegeben'), ('Dokumenttyp', 'Vertragsbedingungen'), ('Gilt für', 'nur den Tarif Professional')],
     """<h2>1. Laufzeit</h2>
<p>Der Professional-Tarif hat eine Mindestvertragslaufzeit von zwölf Monaten ab Vertragsbeginn.</p>
<h2>2. Kündigung</h2>
<p>Nach Ablauf der Mindestlaufzeit kann der Vertrag mit monatlicher Wirkung gekündigt werden. Die Kündigung ist in Textform über das Kundenportal einzureichen; das Portal bestätigt den Beendigungstermin.</p>
<h2>3. Lizenzzahl ändern</h2>
<p>Zusätzliche Lizenzen können jederzeit gebucht werden. Eine Verringerung der Lizenzzahl ist frühestens zum Ende der Mindestlaufzeit möglich.</p>
<h2>4. Andere Tarife</h2>
<p>Für SalesFlow Basic und Enterprise gelten eigene Vertragsbedingungen.</p>""", ''),
    ('04_SalesFlow_Preisliste_Dezember-2025', SF, 'Preisliste SalesFlow – Dezember 2025',
     [('Herausgeber', 'SalesFlow Solutions · Finance'), ('Stand', 'Dezember 2025'), ('Gültig ab', '01.12.2025'), ('Dokumenttyp', 'Preisliste')],
     """<h2>1. Lizenzpreise</h2>
<table class="t"><tr><th>Tarif</th><th>Preis</th></tr>
<tr><td>SalesFlow Basic</td><td>35,00 Euro pro aktivem Nutzer und Monat</td></tr>
<tr><td>SalesFlow Professional</td><td>79,00 Euro pro aktivem Nutzer und Monat</td></tr>
<tr><td>SalesFlow Enterprise</td><td>individuelles Angebot</td></tr></table>
<h2>2. Abrechnung</h2>
<p>Alle Preise verstehen sich netto zuzüglich Umsatzsteuer. Abgerechnet wird monatlich nach der Zahl der gebuchten Lizenzen.</p>""", ''),
    ('05_SalesFlow_Broschuere_Jede-Systemlandschaft', SF, 'Für jede Systemlandschaft.',
     [('Herausgeber', 'SalesFlow Solutions · Marketing'), ('Stand', 'April 2026'), ('Dokumenttyp', 'Werbebroschüre')],
     """<p class="claim">Ein CRM, das sich Ihrem Unternehmen anpasst – nicht umgekehrt.</p>
<div class="box"><b>Offen für alles.</b> Ob SAP, Salesforce oder HubSpot: SalesFlow fügt sich in jede Systemlandschaft ein.</div>
<div class="box"><b>Mehr Überblick im Vertrieb.</b> Unternehmen wie die Nordstern GmbH berichten von mehr Übersicht über ihre Verkaufschancen.</div>
<div class="box"><b>Flexibel starten.</b> Jetzt monatlich kündbar einsteigen – ohne lange Bindung.</div>
<div class="box"><b>Professional – der Tarif für wachsende Teams.</b> Alles, was Ihr Vertrieb braucht, in einer Oberfläche.</div>
<p style="font-size:8pt;color:#777;margin-top:14px">Werbliche Darstellung. Maßgeblich sind Preisliste, Vertragsbedingungen und technische Dokumentation.</p>""", 'promo'),
    ('06_Druckhaus-Lindner_Preisliste-2026', ('Druckhaus Lindner', 'Digital- und Offsetdruck · fiktives Unternehmen', '#8c3b1f'), 'Preisliste Werbedrucksachen 2026',
     [('Herausgeber', 'Druckhaus Lindner · Vertrieb'), ('Stand', 'Januar 2026'), ('Status', 'freigegeben'), ('Dokumenttyp', 'Preisliste')],
     """<h2>1. Flyer (135 g/m² Bilderdruck)</h2>
<table class="t"><tr><th>Produkt</th><th>Auflage</th><th>Preis</th></tr>
<tr><td>Flyer A6, einseitig</td><td>500 Stück</td><td>49,00 Euro</td></tr>
<tr><td>Flyer A6, beidseitig</td><td>1.000 Stück</td><td>69,00 Euro</td></tr>
<tr><td>Flyer A5, beidseitig</td><td>1.000 Stück</td><td>89,00 Euro</td></tr></table>
<h2>2. Plakate und Roll-ups</h2>
<table class="t"><tr><th>Produkt</th><th>Menge</th><th>Preis</th></tr>
<tr><td>Plakat A2, 4-farbig</td><td>10 Stück</td><td>79,00 Euro</td></tr>
<tr><td>Roll-up 85 × 200 cm mit Kassette</td><td>1 Stück</td><td>119,00 Euro</td></tr></table>
<h2>3. Lieferzeiten</h2>
<p>Standard: 5 Werktage nach Druckfreigabe. Express: 2 Werktage, Aufschlag 40 Prozent auf den Produktpreis.</p>
<h2>4. Druckdaten</h2>
<p>PDF/X-4 mit 3 mm Beschnitt. Datencheck ist im Preis enthalten.</p>
<h2>5. Rabatte</h2>
<p>Ab 500 Euro Auftragswert 5 Prozent Rabatt. Express-Aufschläge sind nicht rabattfähig.</p>""", ''),
    ('07_Agentur-Nordlicht_Leistungen-2026', ('Agentur Nordlicht', 'Websites für Handwerksbetriebe · fiktives Unternehmen', '#1f6b5a'), 'Leistungen und Preise 2026',
     [('Herausgeber', 'Agentur Nordlicht · Geschäftsführung'), ('Stand', 'Februar 2026'), ('Status', 'freigegeben'), ('Dokumenttyp', 'Leistungsübersicht')],
     """<h2>1. Über uns</h2>
<p>Agentur Nordlicht, gegründet 2019 in Kiel, 12 Personen im Team. Schwerpunkt: Websites für Handwerksbetriebe.</p>
<h2>2. Website-Pakete</h2>
<table class="t"><tr><th>Paket</th><th>Umfang</th><th>Preis</th></tr>
<tr><td>Website Start</td><td>bis 5 Seiten, Kontaktformular</td><td>2.900 Euro einmalig</td></tr>
<tr><td>Website Plus</td><td>bis 10 Seiten, Blog, Terminanfrage</td><td>4.900 Euro einmalig</td></tr></table>
<h2>3. Pflege</h2>
<p>Website-Pflege (Updates, Sicherheit, kleine Textänderungen): 89 Euro pro Monat, Mindestlaufzeit 12 Monate.</p>
<h2>4. Ablauf</h2>
<p>Projektdauer in der Regel 6 bis 8 Wochen: Kennenlernen, Entwurf, zwei Korrekturschleifen, Livegang.</p>
<h2>5. Nicht enthalten</h2>
<p>Fotoshootings, Texterstellung über 5 Seiten hinaus und Suchmaschinen-Werbung werden gesondert angeboten.</p>""", ''),
    ('08_Cafe-Morgenrot_Markenregeln', ('Café Morgenrot', 'Kaffeehaus · fiktives Unternehmen', '#b8462e'), 'Markenregeln für Social Media',
     [('Herausgeber', 'Café Morgenrot · Inhaberschaft'), ('Stand', 'März 2026'), ('Status', 'freigegeben'), ('Dokumenttyp', 'Markenrichtlinie')],
     """<h2>1. Zielgruppe und Stimmung</h2>
<p>Wir sprechen vor allem Studierende an. Stimmung: ruhig, warm, einladend. Wir sprechen die Leute mit „du“ an.</p>
<h2>2. Claim</h2>
<p>„Langsam wach werden.“ – der Claim steht höchstens einmal pro Beitrag.</p>
<h2>3. Farben und Bildsprache</h2>
<p>Morgenrot, Creme und Espressobraun. Echte Tassen, natürliches Licht, keine Stockfotos mit Personen.</p>
<h2>4. Was wir nicht tun</h2>
<p>Keine Superlative („das Beste“, „unschlagbar“). Keine Preise in Social-Media-Beiträgen. Keine Namen echter Personen, Marken oder Filme. Keine Gesundheitsversprechen.</p>
<h2>5. Hashtags und Öffnungszeiten</h2>
<p>Höchstens drei Hashtags, immer mit #MorgenrotCafe. Öffnungszeiten: Montag bis Samstag, 7 bis 18 Uhr.</p>""", ''),
]


def html(name, brand, title, meta, body, cls):
    rows = ''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in meta)
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{title}</title>
<style>:root{{--c:{brand[2]}}}{CSS}</style></head><body class="{cls}">
<div class="head"><div class="brand">{brand[0]}<small>{brand[1]}</small></div><div class="uebung">Übungsdokument · alle Angaben ausgedacht</div></div>
<h1>{title}</h1><table class="meta">{rows}</table>
{body}
<div class="foot">{brand[0]} ist ein erfundenes Unternehmen. Dieses Dokument dient nur der Übung „RAG“ im Kurs KI Automations Spezialist.</div>
</body></html>'''


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    jobs = []
    for name, brand, title, meta, body, cls in DOCS:
        src = os.path.join(TMP, name + '.html')
        with open(src, 'w', encoding='utf-8') as f:
            f.write(html(name, brand, title, meta, body, cls))
        jobs.append({'html': os.path.abspath(src), 'pdf': os.path.abspath(os.path.join(OUT, name + '.pdf'))})
    jf = os.path.join(TMP, 'jobs.json')
    with open(jf, 'w', encoding='utf-8') as f:
        json.dump(jobs, f)
    subprocess.run(['node', os.path.join(HERE, '..', 'render_plain.mjs'), jf], check=True)
    sets = {
        'SalesFlow_Uebungsdokumente.zip': [d[0] for d in DOCS[:5]],
    }
    for zname, names in sets.items():
        with zipfile.ZipFile(os.path.join(OUT, zname), 'w', zipfile.ZIP_DEFLATED) as z:
            for n in names:
                z.write(os.path.join(OUT, n + '.pdf'), n + '.pdf')
    print('Material:', len(DOCS), 'PDFs +', len(sets), 'ZIP ->', os.path.abspath(OUT))


if __name__ == '__main__':
    main()
