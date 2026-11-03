"""Lernheft Modul 2 · Tag 7: Prozess verstehen und abgrenzen. Roter Faden: „Tatort Prozess“.

Aufbau wie Tag 6: Einfach gesagt → Einzelheiten → Alltagsbeispiel → Prüffrage. Neu: Ermittlungsakte, Dialoge und Mini-Spiele,
damit es nicht trocken wird. Interaktive Werkzeuge nur im Web (web=True), in der PDF-Fassung stehen Ausfülltabellen.
"""
import json

from ..woche1.bausteine import E, md, P, H, merk, achtung, tipp, korrektur, beispiel, tab, flow, karten, glossar, kapitel, teil
from ..woche1.inhalt import vorlage
from ..woche2.inhalt import erkl
from .daten import BEGRIFFE
from .spiele import SPIELE, BINGO, RAENGE
from .vorlagen import AUTOMATIONS, MATERIAL, ZIP

ARBEITSTAG = 480  # Minuten; Annahme für das Verhältnis Arbeit zu Warten

# Schritte der Rechnung von Folie 22: (Bahn, Schritt, Minuten, Wartezeit davor in Tagen, Art). Die Aufteilung der 12 Minuten ist unsere Annahme.
FOLIE22 = [('Lieferant', 'Rechnung senden', 0, 0, 'start'), ('Buchhaltung', 'Rechnung sichten', 2, 1.5, 'task'), ('Buchhaltung', 'Betrag + Lieferant prüfen', 3, 0, 'task'),
           ('Fachabteilung', 'Sachlich prüfen', 3, 2, 'task'), ('Fachabteilung', 'Bestellbezug bestätigen', 1, 0, 'task'), ('Teamleitung', 'Betrag über 1.000 €?', 1, .5, 'raute'),
           ('Teamleitung', 'Freigeben', 1, 0, 'mensch'), ('Buchhaltung', 'Freigabe erfassen', 1, 1, 'task')]
assert sum(s[2] for s in FOLIE22) == 12 and sum(s[3] for s in FOLIE22) == 5
VERHAELTNIS = round(5 * ARBEITSTAG / 12)
assert VERHAELTNIS == 200


def fol(*nums):
    links = ' · '.join(f'<a href="/hefte/folien/tag-26/{n:02d}.jpg" target="_blank" rel="noopener">Folie {n}</a>' for n in nums)
    return f'<p class="folien-ref">Originalfolien: {links}</p>'


def akte(text, titel='Aus der Ermittlungsakte'):
    return f'<div class="akte"><span class="lbl">{E(titel)}</span><p>{md(text)}</p></div>'


def dialog(zeilen):
    out = ''.join(f'<div class="dl-z {"dl-du" if wer == "Du" else ""}"><b>{E(wer)}</b><p>{md(text)}</p></div>' for wer, text in zeilen)
    return f'<div class="dialog">{out}</div>'


def zeitstrahl():
    """Fünf Tage als Balken: Die zwölf Minuten sind nur als feine Striche zu sehen."""
    teile = [('warte', 1.5, 'Ø 1,5 Tage'), ('arbeit', 0, '5 Min.'), ('warte', 2, 'Ø 2 Tage'), ('arbeit', 0, '4 Min.'), ('warte', .5, '0,5'), ('arbeit', 0, '2 Min.'), ('warte', 1, 'Ø 1 Tag'), ('arbeit', 0, '1 Min.')]
    bar = ''.join(f'<span class="zs-w" style="flex:{w} 1 0"><i>{E(t)}</i></span>' if a == 'warte' else f'<span class="zs-a" title="{E(t)} Arbeit"></span>' for a, w, t in teile)
    return (f'<div class="zeitstrahl" role="img" aria-label="Fünf Tage Durchlauf, davon zwölf Minuten Arbeit als feine Striche"><div class="zs-bar">{bar}</div>'
            '<p class="zs-l"><span><i class="zs-pa"></i>Warten: 5 Tage</span><span><i class="zs-pb"></i>Arbeit: 12 Minuten (die feinen Striche, kein Druckfehler)</span></p></div>')


def tagebuch():
    t = [('Start', 'Der Lieferant schickt mich los. Ich bin Rechnung 0815, eine ganz normale Rechnung über 1.240 Euro, und ich will nur eins: bezahlt werden.', ''),
         ('Ø 1,5 Tage später', 'Endlich öffnet Kim aus der Buchhaltung die Mail. Zwei Minuten sichten, drei Minuten Betrag und Lieferant prüfen. Das war schön. Dann: weiterleiten.', '5 Minuten Arbeit'),
         ('Ø 2 Tage später', 'Ich lag im Postfach der Fachabteilung, zwischen Kantinenplan und Einladung zur Weihnachtsfeier. Alex schaut mich an: Die Bestellung gibt es. Weiter.', '4 Minuten Arbeit'),
         ('Ø 0,5 Tage später', 'Sascha aus der Teamleitung. Über 1.000 Euro? Ja. Freigegeben. Davon eine Minute, um den Kaffee abzustellen.', '2 Minuten Arbeit'),
         ('Ø 1 Tag später', 'Zurück bei Kim. Ein Eintrag. Zur Zahlung freigegeben. Ich bin frei.', '1 Minute Arbeit'),
         ('Fazit', 'Fünf Tage unterwegs. Zwölf Minuten hat sich jemand um mich gekümmert. Den Rest der Woche war ich ein ungelesener Anhang.', '')]
    out = ''.join(f'<li><span class="tb-z">{E(a)}</span><p>{md(b)}</p>{f"<em>{E(c)}</em>" if c else ""}</li>' for a, b, c in t)
    return f'<ol class="tagebuch">{out}</ol>'


# ================================================================ Werkzeuge

def uhr(minuten, text):
    return f'<div class="uhr" data-uhr="{minuten}" data-uhr-text="{E(text)}"><b class="uhr-z">{minuten}:00</b><button class="btn" type="button" data-uhr-los>Start</button><button class="btn ghost" type="button" data-uhr-neu>Zurück auf {minuten}:00</button><span class="uhr-t" aria-live="polite"></span></div>'


def montag_tool(web):
    if not web:
        return '<p class="ausfuell-zeile">Mein Haupt-Use-Case von Montag: _______________________________ Empfehlung: ______________ Amortisation: ______ Monate</p>'
    return ('<div class="tool" data-tool="montag"><div class="tool-h"><b>Dein Stand von Montag</b><span>aus deinem Rechen-Labor in diesem Browser</span></div><div class="ft-liste" aria-live="polite"></div></div>')


def spiel_tool(sid, web):
    s = SPIELE[sid]
    if not web:
        kopf = ['Karte', 'Deine Wahl']
        rows = []
        for k in s['karten']:
            opts = k[3] if len(k) > 3 else s['optionen']
            rows.append([k[0], ' · '.join('☐ ' + o for o in opts)])
        loes = ' · '.join(f'{i}. {k[1]}' for i, k in enumerate(s['karten'], 1))
        return f'<h4>Spiel: {E(s["titel"])}</h4>' + P(s['intro']) + tab(kopf, rows) + f'<p class="aufloesung"><b>Auflösung:</b> {E(loes)}</p>'
    daten = dict(titel=s['titel'], optionen=s.get('optionen'), karten=[dict(t=k[0], r=k[1], w=k[2], o=k[3] if len(k) > 3 else None) for k in s['karten']], raenge=RAENGE)
    return (f'<div class="tool spiel" data-spiel="{sid}"><div class="tool-h"><b>Spiel: {E(s["titel"])}</b><span>{len(s["karten"])} Karten · {E(s["folie"])}</span></div><p class="sp-intro">{md(s["intro"])}</p>'
            f'<script type="application/json" class="sp-daten">{json.dumps(daten, ensure_ascii=False).replace("<", chr(92) + "u003c")}</script><div class="sp-feld" aria-live="polite"></div></div>')


def bingo_tool(web):
    if not web:
        zellen = ''.join(f'<div class="bg-z">{"★ " if f else ""}{E(a)}<small>{E(b)}</small></div>' for a, b, f in BINGO)
        return f'<div class="bingo">{zellen}</div><p class="aufloesung">★ steht auf Folie 16. Die übrigen Sätze haben wir aus dem Alltag ergänzt. Abhaken, sobald du einen hörst. Drei in einer Reihe: Bingo.</p>'
    daten = [dict(a=a, b=b, f=f) for a, b, f in BINGO]
    return (f'<div class="tool" data-tool="bingo"><div class="tool-h"><b>Alarmsatz-Bingo</b><span>antippen, sobald du den Satz hörst · ★ steht auf Folie 16, der Rest ist aus dem Alltag ergänzt</span></div>'
            f'<script type="application/json" class="bg-daten">{json.dumps(daten, ensure_ascii=False)}</script><div class="bingo" data-bingo></div><p class="bg-frage" aria-live="polite">Tippe einen Satz an, sobald er fällt. Hier erscheint dann deine Rückfrage.</p>'
            '<div class="btnrow"><button class="btn ghost" type="button" data-bg-neu>Neue Runde</button></div></div>')


def mitschrift_tool(web):
    if not web:
        rows = ''.join('<tr><td></td><td></td><td></td></tr>' for _ in range(8))
        t = f'<div class="tab-wrap"><table class="tab ausfuell"><thead><tr><th>Handlung</th><th>System</th><th>Entscheidung (Woran erkennst du das?)</th></tr></thead><tbody>{rows}</tbody></table></div>'
        return f'<p class="steck-h">Runde 1 · Fall: ______________________________</p>{t}<p class="steck-h">Runde 2 · Fall: ______________________________</p>{t}<p class="ausfuell-zeile">☐ Runde 1 vorgelesen und bestätigt ☐ Runde 2 vorgelesen und bestätigt</p>'
    return ('<div class="tool" data-tool="mitschrift"><div class="tool-h"><b>Interview-Mitschrift</b><span>meldet Alarmsätze automatisch · speichert in diesem Browser</span></div>'
            + uhr(20, 'Zwanzig Minuten um. Rollentausch! Wer gerade gefragt hat, wird jetzt befragt.') +
            '<div class="rd-tabs" role="group" aria-label="Runde wählen"><button type="button" class="btn" data-ms-runde="1" aria-pressed="true">Runde 1</button><button type="button" class="btn ghost" data-ms-runde="2" aria-pressed="false">Runde 2</button></div>'
            '<label class="fld"><span>Welcher Fall? Der letzte echte, am besten von gestern.</span><input type="text" data-ms-fall placeholder="z. B. Rechnung vom Büromaterial-Lieferanten"></label>'
            '<div class="ms-kopf" aria-hidden="true"><span>Handlung</span><span>System</span><span>Entscheidung</span><span></span></div><div class="ms-zeilen"></div>'
            '<div class="btnrow"><button class="btn" type="button" data-ms-plus>+ Zeile</button><button class="btn ghost" type="button" data-ms-bsp>Beispiel Rechnung 0815 laden</button><button class="btn ghost" type="button" data-ms-vorlesen>Zum Vorlesen anzeigen</button></div>'
            '<ul class="alarm-liste" aria-live="polite"></ul><ol class="ms-vorlesen" hidden></ol>'
            '<div class="ms-fertig"><label class="bp-done"><input type="checkbox" data-save="t7-ms1-ok"> Runde 1 vorgelesen und bestätigt</label><label class="bp-done"><input type="checkbox" data-save="t7-ms2-ok"> Runde 2 vorgelesen und bestätigt</label></div><p class="stand" data-stand="mitschrift" aria-live="polite"></p></div>')


SIPOC = [('s', 'S · Lieferant', 'Woher kommt der Input?', 'Lieferant, Kunde, Vorsystem', 'Lieferant der Rechnung'), ('i', 'I · Input', 'Was genau kommt an?', 'PDF-Rechnung per E-Mail', 'PDF-Rechnung per E-Mail'),
         ('p', 'P · Prozess', 'Fünf bis sieben Hauptschritte, einer pro Zeile', '', 'Rechnung sichten\nBetrag und Lieferant prüfen\nSachlich prüfen\nBestellbezug bestätigen\nFreigeben\nFreigabe erfassen'),
         ('o', 'O · Output', 'Was entsteht?', 'Freigegebene Rechnung mit Protokolleintrag', 'Freigegebene Rechnung mit Protokolleintrag'), ('c', 'C · Empfänger', 'Wer bekommt das Ergebnis?', 'Buchhaltung, Zahlungslauf', 'Buchhaltung, Zahlungslauf')]


def sipoc_tool(web):
    if not web:
        kopf = ''.join(f'<th>{E(t)}<br><small>{E(f)}</small></th>' for _, t, f, _, _ in SIPOC)
        zellen = ''.join('<td style="height:34mm"></td>' for _ in SIPOC)
        return f'<div class="tab-wrap"><table class="tab ausfuell"><thead><tr>{kopf}</tr></thead><tbody><tr>{zellen}</tr></tbody></table></div><p class="ausfuell-zeile">Der Prozess beginnt mit: ____________________________ Er endet mit: ____________________________</p>'
    felder = ''.join(f'<label class="fld"><span>{E(t)}</span><small>{E(f)}</small>' + (f'<textarea rows="6" data-save="t7-sipoc-{k}" data-sipoc="{k}" data-bsp="{E(b)}"></textarea>' if k == 'p' else f'<textarea rows="3" data-save="t7-sipoc-{k}" data-sipoc="{k}" data-bsp="{E(b)}" placeholder="{E(x)}"></textarea>') + '</label>' for k, t, f, x, b in SIPOC)
    return ('<div class="tool" data-tool="sipoc"><div class="tool-h"><b>SIPOC mit Absperrband</b><span>schaffst du es in zehn Minuten?</span></div>'
            + uhr(10, 'Zehn Minuten um. Laut Folie 19 ist der Fall dann noch nicht scharf genug für die technische Planung. Kein Drama, aber ein Befund.') +
            f'<div class="sipoc">{felder}</div><div class="absperr" aria-live="polite"></div><div class="btnrow"><button class="btn ghost" type="button" data-sipoc-bsp>Beispiel Rechnung laden</button></div><p class="stand" data-stand="sipoc" aria-live="polite"></p></div>')


def bahnen_tool(web):
    if not web:
        zeilen = ''.join(f'<tr><th style="width:26mm;height:18mm">Bahn {i}:<br>&nbsp;</th><td></td></tr>' for i in range(1, 6))
        return (f'<div class="tab-wrap"><table class="tab ausfuell bahn-druck"><tbody>{zeilen}</tbody></table></div>'
                '<div class="tab-wrap"><table class="tab ausfuell"><thead><tr><th>Übergabe (von → nach)</th><th>Wartezeit in Tagen</th></tr></thead><tbody>' + '<tr><td></td><td></td></tr>' * 5 + '</tbody></table></div>'
                '<p class="ausfuell-zeile">Bearbeitungszeit gesamt: ________ Minuten · Durchlaufzeit gesamt: ________ Tage · Größte Übergabe: ______________________</p>')
    bahnen = ''.join(f'<label class="fld"><span>Bahn {i}</span><input type="text" data-save="t7-bahn-{i}" data-bahn="{i}" placeholder="{"Person, Rolle oder System" if i == 1 else ""}"></label>' for i in range(1, 6))
    return ('<div class="tool" data-tool="bahnen"><div class="tool-h"><b>Tatortskizze: Ist-Prozess in Bahnen</b><span>zeichnet sich selbst · speichert in diesem Browser</span></div>'
            f'<div class="bh-bahnen">{bahnen}</div>'
            '<div class="bh-kopf" aria-hidden="true"><span>Schritt</span><span>Bahn</span><span>Art</span><span>Arbeit (Min.)</span><span>Warten davor (Tage)</span><span></span></div><div class="bh-zeilen"></div>'
            '<div class="btnrow"><button class="btn" type="button" data-bh-plus>+ Schritt</button><button class="btn ghost" type="button" data-bh-ms>Aus der Mitschrift übernehmen</button><button class="btn ghost" type="button" data-bh-bsp>Fall Rechnung 0815 laden</button></div>'
            '<div class="bh-skizze" tabindex="0" aria-label="Gezeichneter Ablauf in Bahnen"></div><div class="bc-aus bh-aus" aria-live="polite"></div>'
            '<div class="bh-was" hidden><h4>Was wäre, wenn …?</h4><p class="bh-was-t">Nur zum Ausprobieren, deine Zahlen bleiben gespeichert.</p><div class="bh-kn"></div><p class="bh-was-e" aria-live="polite"></p></div><p class="stand" data-stand="bahnen" aria-live="polite"></p></div>')


def sop_tool(web):
    if not web:
        rows = ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 13))
        return ('<div class="tab-wrap"><table class="tab ausfuell"><thead><tr><th>Nr.</th><th>Rolle</th><th>Handlung</th><th>System</th><th>Markierung beim Gegenlesen</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
                '<p class="ausfuell-zeile">Fehlende Regeln: ______ Noch nicht erfasste Ausnahmen: ______ (beides wandert in Block 4)</p>')
    return ('<div class="tool" data-tool="sop"><div class="tool-h"><b>SOP: der Neue-Kollegin-Test</b><span>meldet Alarmsätze automatisch · speichert in diesem Browser</span></div>'
            '<div class="sop-kopf" aria-hidden="true"><span>Rolle</span><span>Handlung</span><span>System</span><span>Markierung</span><span></span></div><div class="sop-zeilen"></div>'
            '<div class="btnrow"><button class="btn" type="button" data-sop-plus>+ Schritt</button><button class="btn" type="button" data-sop-warte>+ Wartezeit</button><button class="btn ghost" type="button" data-sop-bahnen>Aus den Bahnen übernehmen</button><button class="btn ghost" type="button" data-sop-bsp>Beispiel laden</button></div>'
            '<ul class="alarm-liste" aria-live="polite"></ul><label class="bp-done"><input type="checkbox" data-save="t7-sop-ok"> Von einer zweiten Person gegengelesen und markiert</label><p class="stand" data-stand="sop" aria-live="polite"></p></div>')


ZIEL = [('anteil', '01 · Anteil oder Menge', '70 Prozent'), ('fall', '02 · Abgegrenzte Fallmenge', 'der Rechnungen unter 1.000 Euro ohne Klärungsbedarf'), ('handlung', '03 · Konkrete Handlung', 'werden ohne manuelle Prüfung freigegeben'),
        ('kennzahl', '04 · Kennzahl', 'gemessen an der Freigabequote im Monatsbericht'), ('zeit', '05 · Zeitpunkt', 'ab drei Monaten nach Start')]


def ziel_tool(web):
    if not web:
        rows = ''.join(f'<p class="ausfuell-zeile">{E(t)}: ______________________________________________</p>' for _, t, _ in ZIEL)
        return rows + '<p class="ausfuell-zeile">Mein Zielsatz: ______________________________________________________________</p><p class="ausfuell-zeile">__________________________________________________________________________</p><p class="ausfuell-zeile">Projektname ohne Technologiebegriff: ______________________________</p>'
    felder = ''.join(f'<label class="fld"><span>{E(t)}</span><input type="text" data-save="t7-ziel-{k}" data-ziel="{k}" data-bsp="{E(b)}" placeholder="{E(b)}"></label>' for k, t, b in ZIEL)
    return ('<div class="tool" data-tool="ziel"><div class="tool-h"><b>Zielsatz-Baukasten</b><span>sagt dir freundlich, was fehlt</span></div>'
            f'{felder}<label class="fld"><span>Projektname ohne Technologiebegriff</span><input type="text" data-save="t7-ziel-name" data-ziel-name placeholder="z. B. Rechnung in einem Tag"></label>'
            '<div class="ziel-satz" aria-live="polite"></div><ul class="ziel-fehlt" aria-live="polite"></ul><div class="btnrow"><button class="btn ghost" type="button" data-ziel-bsp>Beispiel von Folie 10 laden</button></div><p class="stand" data-stand="ziel" aria-live="polite"></p></div>')


def scope_tool(web):
    if not web:
        zeilen = ''.join('<tr><td></td><td></td></tr>' for _ in range(6))
        ann = ''.join('<tr><td></td><td></td></tr>' for _ in range(3))
        return (f'<div class="tab-wrap"><table class="tab ausfuell"><thead><tr><th>In Scope (mindestens 6)</th><th>Out of Scope (mindestens 6)</th></tr></thead><tbody>{zeilen}</tbody></table></div>'
                '<p class="ausfuell-zeile">Schutzsatz: Alles, was hier nicht ausdrücklich aufgeführt ist, gilt als außerhalb des Umfangs.</p>'
                f'<div class="tab-wrap"><table class="tab ausfuell"><thead><tr><th>Annahme</th><th>Was passiert, wenn sie nicht stimmt?</th></tr></thead><tbody>{ann}</tbody></table></div>')
    ann = ''.join(f'<div class="scope-ann"><label class="fld"><span>Annahme {i}</span><input type="text" data-save="t7-ann{i}" data-ann="{i}"></label><label class="fld"><span>Wenn sie nicht stimmt …</span><input type="text" data-save="t7-ann{i}-wenn" data-ann-wenn="{i}"></label></div>' for i in (1, 2, 3))
    return ('<div class="tool" data-tool="scope"><div class="tool-h"><b>Scope: rein, raus, Annahmen</b><span>ein Eintrag pro Zeile · speichert in diesem Browser</span></div>'
            '<div class="scope-raster"><label class="fld"><span>In Scope</span><small data-scope-zahl="in"></small><textarea rows="7" data-save="t7-in" data-scope="in"></textarea></label>'
            '<label class="fld"><span>Out of Scope, der wichtigere Teil</span><small data-scope-zahl="out"></small><textarea rows="7" data-save="t7-out" data-scope="out"></textarea></label></div>'
            '<p class="schutzsatz"><b>Schutzsatz:</b> Alles, was hier nicht ausdrücklich aufgeführt ist, gilt als außerhalb des Umfangs.</p>'
            f'{ann}<div class="btnrow"><button class="btn ghost" type="button" data-scope-bsp>Beispiel Rechnung laden</button></div><p class="stand" data-stand="scope" aria-live="polite"></p></div>')


KRIT_SP = [('name', 'Kriterium'), ('heute', 'Wert heute'), ('ziel', 'Zielwert'), ('quelle', 'Messquelle'), ('wann', 'Gemessen wann')]


def kriterien_tool(web):
    if not web:
        rows = ''.join('<tr>' + '<td></td>' * 5 + '</tr>' for _ in range(5))
        kopf = ''.join(f'<th>{E(t)}{" (Pflicht!)" if k == "heute" else ""}</th>' for k, t in KRIT_SP)
        return f'<div class="tab-wrap"><table class="tab ausfuell"><thead><tr>{kopf}</tr></thead><tbody>{rows}</tbody></table></div><p class="ausfuell-zeile">Wert unbekannt? Dann in „Wert heute“ eintragen, wie er erhoben wird und bis wann.</p>'
    zeilen = ''
    for z in range(1, 6):
        zeilen += '<div class="kr-zeile">' + ''.join(f'<label class="fld"><span>{E(t)}</span><input type="text" data-save="t7-kr{z}-{k}" data-kr="{z}-{k}"></label>' for k, t in KRIT_SP) + '</div>'
    return ('<div class="tool" data-tool="kriterien"><div class="tool-h"><b>Beweise sichern: Erfolgskriterien</b><span>drei bis fünf Stück · „Wert heute“ ist Pflicht</span></div>'
            f'{zeilen}<ul class="ziel-fehlt kr-fehlt" aria-live="polite"></ul><div class="btnrow"><button class="btn" type="button" data-kr-bahnen>Durchlaufzeit aus den Bahnen übernehmen</button><button class="btn ghost" type="button" data-kr-bsp>Beispiel von Folie 31 laden</button></div><p class="stand" data-stand="kriterien" aria-live="polite"></p></div>')


def export_tool(web):
    if not web:
        return ''
    return ('<div class="tool" data-tool="akte"><div class="tool-h"><b>Deine Ermittlungsakte</b><span>sieben Teile, wie auf Folie 38</span></div><ul class="akte-liste" aria-live="polite"></ul>'
            '<div class="btnrow"><button class="btn primary" type="button" data-t7-export>Meine Akte herunterladen (.md)</button></div></div>')


# ================================================================ Teile des Hefts

def teil_erinnerung(web):
    k = kapitel('r1', 'R1', 'Erinnerung · Montag, 02.11.', 'Was bisher geschah',
        P('Kennst du aus jeder guten Serie: Bevor die neue Folge losgeht, kommen dreißig Sekunden „Was bisher geschah“. Hier sind sie.') +
        montag_tool(web) +
        H('Die letzte Folge in vier Sätzen') +
        karten([('1', 'Bewerten', 'Drei Kandidaten bekamen Punkte. Fünf Punkte sind immer gut fürs Projekt, und jede Zahl braucht einen Satz.'), ('2', 'Priorisieren', 'Die Matrix machte daraus eine Entscheidung. Übrig blieb ein Haupt-Use-Case.'),
                ('3', 'Rechnen', 'Bruttonutzen minus laufende Kosten ist Nettonutzen. Daraus folgen Amortisation, ROI und TCO.'), ('4', 'Entscheiden', 'Das konservative Szenario entscheidet, und „nicht machen“ ist erlaubt.')], cols=2) +
        H('Der Haken an der Sache') +
        P('Deine Rechnung von gestern steht auf Annahmen: so viele Vorgänge, so viele Minuten, so viel Anteil. **Woher weißt du eigentlich, dass es so läuft?** Heute schaust du nach.') +
        H('Drei Fragen zum Warmwerden') +
        ''.join(f'<details class="verstehen"><summary><span class="lbl">Erinnerst du dich?</span> {md(q)}</summary><p>{md(a)}</p></details>' for q, a in [
            ('Was ist der Unterschied zwischen Scoring und Business Case?', 'Das Scoring sagt, was zuerst kommt. Der Business Case sagt, ob es sich überhaupt lohnt.'),
            ('Warum nennt man einen ROI nie ohne Zeitraum?', 'Weil sich der Wert mit der Zeit ändert: im Beispiel 18,5 % nach 12 Monaten und rund 256 % nach 36 Monaten.'),
            ('Was gehört in eine Abbruchbedingung?', 'Eine Zahl, ein Zeitpunkt und eine Person.')]) +
        tipp('Montag verpasst?', 'Kein Problem. Nimm eines der drei fertigen Beispiele weiter hinten im Heft oder fülle das Rechen-Labor von Tag 6 kurz nach.') +
        '<p class="folien-ref">Montagsfolien: <a href="/hefte/folien/tag-25/12.jpg" target="_blank" rel="noopener">Matrix</a> · <a href="/hefte/folien/tag-25/16.jpg" target="_blank" rel="noopener">Kennzahlen</a> · <a href="/hefte/folien/tag-25/19.jpg" target="_blank" rel="noopener">Beispielrechnung</a> · <a href="/hefte/folien/tag-25/28.jpg" target="_blank" rel="noopener">Abbruchbedingung</a></p>')
    return teil('teil-r', '←', 'Was bisher geschah', 'Dreißig Sekunden Rückblick, dann beginnt die Ermittlung.', k)


def teil_start():
    k = kapitel('s1', 'S1', 'Heute · Folien 1 und 2', 'Der Fall des Tages: das Tagebuch der Rechnung 0815',
        erkl('Bisher hast du **über** deinen Fall geredet. Heute schaust du nach, **was tatsächlich passiert**. Du wirst zur Ermittlerin oder zum Ermittler: befragen, skizzieren, Beweise sichern.',
             flow([('1 · Tatort besichtigen', 'Warum Prozesse so chaotisch sind, wie sie sind'), ('2 · Auftrag klären', 'Vom Wunsch zum prüfbaren Ziel'), ('3 · Befragung', 'Interview mit Alarmsatz-Bingo'), ('4 · Tatortskizze', 'SIPOC, Bahnen, SOP'), ('5 · Beweise sichern', 'Scope und Erfolgskriterien')]) +
             H('Spannend wird es hier') +
             tagebuch() + zeitstrahl() +
             merk('Die eine Frage des Tages: Wo sind die fünf Tage hin?') +
             achtung('Die wichtigste Regel für Ermittelnde', '**Der einzige Verdächtige ist der Prozess.** Niemand hat etwas falsch gemacht. Kim, Alex und Sascha arbeiten richtig, nur der Ablauf dazwischen ist nie entworfen worden.'),
             frage='Warum bleibt die Rechnung so lange liegen, obwohl alle fleißig sind?', antwort='Weil die Zeit nicht in der Arbeit steckt, sondern zwischen den Personen. Genau das zeigt dir heute die Bahnen-Ansicht.') +
        P('Das Beispiel ist erfunden, die Zeiten stehen auf Folie 22. Wie sich die 12 Minuten auf die Schritte verteilen, haben wir angenommen.') +
        fol(1, 2))
    return teil('teil-s', 'S', 'Der Fall des Tages', 'Heute hören wir auf, über den Fall zu reden, und schauen nach.', k)


def teil_ausgang():
    k = []
    k.append(kapitel('a1', 'A1', 'Tatort besichtigen · Folien 3, 4', 'Prozesse wurden nicht entworfen. Sie sind passiert.',
        erkl('Niemand hat sich hingesetzt und deinen Ablauf geplant. Er ist über Jahre um Personen, Systemwechsel und Ausnahmen herum gewachsen.',
             tab(['Was du findest', 'Was das heißt', 'So klingt es'], [
                 ['**Historisch gewachsen**', 'Nicht entworfen, sondern entstanden', '„Das machen wir so, seit Frau Berger das 2014 eingeführt hat.“'],
                 ['**Wissen steckt in Personen**', 'Was dokumentiert ist, ist selten der gelebte Ablauf', '„Im Handbuch steht das anders, aber so geht es schneller.“'],
                 ['**Abläufe unterscheiden sich**', 'Je nach Person oder Tageszeit läuft derselbe Vorgang anders', '„Vormittags mach ich das anders, da ist der Server schneller.“'],
                 ['**Verantwortlichkeiten unklar**', 'Wer prüft was? Wer entscheidet final?', '„Das müsste eigentlich die Teamleitung … oder?“'],
                 ['**Daten sind inkonsistent**', 'Unterschiedliche Formate, fehlende Pflichtfelder', '„Das Feld ist Pflicht, außer wir schreiben eine 0 rein.“']]) +
             P('Dann kommt die Automatisierung und deckt all das auf, denn sie braucht eine eindeutige Regel, wo bisher Erfahrung gereicht hat.'),
             'Die Besteckschublade in deiner Küche. Nie geplant, irgendwie gewachsen, und nur eine Person im Haushalt weiß, wo der Korkenzieher liegt. Funktioniert prima, bis jemand anderes kochen soll.',
             'Wer hat den Ablauf in deinem Bereich eigentlich entworfen?', 'Vermutlich niemand. Und wer glaubt, dass die Dokumentation den echten Ablauf beschreibt, meldet sich laut Folien-Notiz meist gar nicht erst.') +
        fol(3, 4)))
    k.append(kapitel('a2', 'A2', 'Tatort besichtigen · Folie 5', 'Zwei Wege, ein Ergebnis',
        erkl('Zwei Personen beantworten dieselbe Anfrage richtig. Nur den einen Weg kann man aufschreiben, und **nur was beschreibbar ist, ist automatisierbar**.',
             tab(['Person A: regelbasiert', 'Person B: erfahrungsbasiert'], [
                 ['Anfrage kategorisieren', 'Anfrage lesen'], ['Standardantwort aus Vorlage', 'Kollegin kurz fragen'], ['Fachlich prüfen', 'Im alten Vorgang nachschauen'], ['Versenden', 'Frei formulieren, nochmal überfliegen, zurück zu „Frei formulieren“']]) +
             merk('Der rechte Weg ist nicht schlechter. Bei schwierigen Fällen ist er oft der bessere. Das Ziel ist nicht, ihn abzuschaffen, sondern zu wissen, wann er greift.'),
             'Zwei Kartoffelsalate, beide köstlich. Der eine nach Rezept. Der andere von Oma: „Wie viel Salz?“ „Bis es passt.“ Nur das Rezept kannst du weitergeben.',
             'Muss Person B also umlernen?', 'Nein. Du musst herausfinden, woran Person B erkennt, wann der schwierige Weg nötig ist. Genau das wird heute die Befragung.') +
        fol(5)))
    k.append(kapitel('a3', 'A3', 'Tatort besichtigen · Folie 6', 'Die Unschärfe ist kein Hindernis',
        '<blockquote class="kernsatz">Diese Unschärfe ist nicht das Hindernis. Sie ist der erste Teil des Nutzens.</blockquote>' +
        erkl('Ein Automatisierungsprojekt zwingt eine Organisation oft zum ersten Mal zu entscheiden, wie ein Ablauf **laufen soll**. Ein Teil des Wertes entsteht schon, bevor irgendetwas automatisiert ist.',
             achtung('Die Kommunikationsregel', 'Widersprüche sind kein Vorwurf an die Beteiligten. Wer das anders rüberbringt, bekommt beim nächsten Gespräch keine ehrlichen Antworten mehr. Deshalb: Verdächtig ist nur der Prozess.'),
             'Ein Umzug. Beim Einpacken merkst du, dass ihr vier Kellen und keinen Dosenöffner habt. Das Aufräumen bringt schon etwas, bevor der Umzugswagen da ist.',
             'Zwei Personen schildern denselben Ablauf verschieden. Wie reagierst du?', 'Neugierig, nicht richtend: „Interessant, dann gibt es hier zwei Wege. Wann nimmt man welchen?“') +
        fol(6)))
    return teil('teil-a', '1', 'Tatort besichtigen', 'Warum Prozesse so aussehen, wie sie aussehen. Und warum das kein Vorwurf ist.', ''.join(k))


def teil_ziel(web):
    k = []
    k.append(kapitel('z1', 'Z1', 'Auftrag klären · Folien 7, 8', 'Projekte starten aus einem Schmerz',
        erkl('Ein gutes Projekt beginnt nicht mit „Wir sollten mal KI einsetzen“, sondern mit etwas, das wirklich wehtut. Der Fachbereich beschreibt **das Problem**, nicht die Lösung.',
             flow([('Benennen', 'Das Problem klar benennen'), ('Definieren', 'Nutzen und Kennzahlen festlegen'), ('Begrenzen', 'Grenzen ziehen'), ('Erst dann', 'Technik')]) +
             merk('Der Test: Kann der Fachbereich das Problem in drei Sätzen erklären, ohne ein Werkzeug zu nennen? Dann ist der Start sauber.'),
             'Beim Arzt sagst du: „Mir tut der Hals weh.“ Wer stattdessen sagt „Verschreiben Sie mir bitte Antibiotika“, verhindert jede bessere Lösung, und vielleicht war es nur der Schal.',
             '„Wir brauchen einen Chatbot.“ Besteht das den Test?', 'Nein, da steckt ein Werkzeug drin. Besser: „Kundschaft wartet drei Tage auf Antworten zu immer denselben Fragen, und das kostet uns Aufträge.“') +
        fol(7, 8)))
    k.append(kapitel('z2', 'Z2', 'Auftrag klären · Folien 9, 10', 'Vom Neujahrsvorsatz zum Ziel: fünf Bausteine',
        erkl('Ein Wunsch wird erst dann zum Ziel, wenn man ihn prüfen kann. Dafür braucht es **fünf Bausteine**. Fehlt einer, kann in sechs Monaten niemand mehr sagen, ob es funktioniert hat.',
             tab(['Baustein', 'Beispiel von Folie 10', 'Neujahrsvorsatz'], [
                 ['**01 Anteil oder Menge**', '70 Prozent', 'zweimal pro Woche'], ['**02 Abgegrenzte Fallmenge**', 'der Rechnungen unter 1.000 Euro ohne Klärungsbedarf', 'außer in Krankheitswochen'],
                 ['**03 Konkrete Handlung**', 'werden ohne manuelle Prüfung freigegeben', '30 Minuten joggen'], ['**04 Kennzahl**', 'gemessen an der Freigabequote im Monatsbericht', 'laut Lauf-App'], ['**05 Zeitpunkt**', 'ab drei Monaten nach Start', 'ab dem 1. Februar']]) +
             spiel_tool('wunsch', web) +
             korrektur('Folien 9 und 10', 'Das „gute“ Ziel auf Folie 9 („70 Prozent der Standardanfragen automatisch vorsortieren“) hat nach dem Maßstab von Folie 10 noch Lücken: Es fehlt der Zeitpunkt, und die Kennzahl steht nur daneben. Folie 9 zeigt den ersten Schritt, Folie 10 den fertigen Satz. Gute Frage an die Runde: Wem ist es aufgefallen?'),
             '„Ich will mehr Sport machen“ überlebt selten den Januar. „Ab 1. Februar zweimal pro Woche 30 Minuten joggen, laut Lauf-App“ kannst du im März nachprüfen. Das ist auch unangenehmer, aber genau das ist der Punkt.',
             'Welcher Baustein wird am häufigsten vergessen?', 'Meist der Zeitpunkt. Ohne ihn kann das Projekt auch 2049 noch erfolgreich werden.') +
        fol(9, 10)))
    k.append(kapitel('z3', 'Z3', 'Auftrag klären · Folie 11', 'Zehn Fragen zum Projektstart',
        erkl('Die ersten fünf Fragen kennt jede Person. **Die anderen fünf entscheiden über den Zeitplan** und werden gern zu spät gestellt.',
             tab(['Die bekannten fünf', 'Die fünf, die früh gestellt gehören', 'Warum so früh?'], [
                 ['Was genau stört: Zeit, Fehler, Doppelarbeit, Nachvollziehbarkeit?', '**Wer entscheidet am Ende?**', 'Nicht wer mitredet, wer freigibt.'],
                 ['Wie oft tritt der Fall auf?', '**Was passiert heute, wenn etwas schiefgeht?**', 'Der Eskalationsweg von heute ist die Vorlage für den automatisierten.'],
                 ['Welche konkreten Fälle sollen automatisiert werden?', '**Welche Systeme sind beteiligt, und wer verwaltet die Zugänge?**', 'Regelmäßig der längste Einzelposten im Zeitplan.'],
                 ['Welche Fälle bewusst nicht?', '**Gibt es einen Betriebsrat, und ist er informiert?**', 'Technik, die Verhalten oder Leistung überwachen kann, ist mitbestimmungspflichtig.'],
                 ['Wie sieht Erfolg aus?', '**Was ist in sechs Monaten anders?**', 'Systemwechsel, Reorganisationen, saisonale Spitzen.']]),
             'Familienurlaub. Alle reden mit, wohin es geht. Wichtiger ist: Wer bucht am Ende, wer hat den Reisepass, und läuft der noch? Die dritte Frage hat schon viele Urlaube beendet, bevor sie anfingen.',
             'Warum steht „Zugänge“ so weit oben?', 'Weil Technik in Tagen gebaut ist, aber ein Zugang zum System oft Wochen dauert. Wer das zu spät fragt, sitzt mit fertigem Ablauf vor verschlossener Tür.') +
        fol(11)))
    k.append(kapitel('z4', 'Z4', 'Auftrag klären · Folie 12', 'So sehen brauchbare Antworten aus',
        erkl('Der Unterschied zwischen Absichtserklärung und Arbeitsgrundlage: **eine Zahl, eine Grenze und eine ausdrückliche Ausschlussliste.**',
             tab(['Frage', 'Rechnungsfreigabe'], [
                 ['Was stört?', 'Hoher Zeitverlust durch eine simple, wiederkehrende Aufgabe. Vier Minuten je Vorgang, überwiegend Suchen und Abgleichen.'], ['Wie oft?', '800 Rechnungsfreigaben pro Monat.'],
                 ['Was soll automatisiert werden?', 'Nicht alle Rechnungen. Sondern: unter 1.000 Euro, keine Sonderprojekte, kein manueller Klärungsbedarf.'],
                 ['Was ausdrücklich nicht?', 'Alles über 1.000 Euro, Projektabrechnungen, Rechnungen ohne Bestellbezug, alles mit Klärungsvermerk.'],
                 ['Wie sieht Erfolg aus?', 'Mindestens 30 Minuten Zeitersparnis pro Tag und Person, bei gleichbleibender Fehlerquote.']]) +
             korrektur('Folien 12, 22 und 31', 'Folien 12 und 31 rechnen mit 4 Minuten je Rechnung, Folie 22 mit 12 Minuten Bearbeitung gesamt. Das passt nur, wenn die 4 Minuten allein den Schritt in der Buchhaltung meinen. Die Folien sagen das nicht ausdrücklich. Für deinen Fall gilt: Sag immer dazu, was du misst. Gestern im Business Case rechneten wir mit den 4 Minuten. Wer alle 12 Minuten zählt, käme auf einen anderen Nutzen.'),
             frage='Was macht „keine Sonderprojekte“ so wertvoll?', antwort='Es ist eine Grenze. An einem einzelnen Fall lässt sich jetzt entscheiden, ob er dazugehört.') +
        fol(12)))
    return teil('teil-z', '2', 'Den Auftrag klären', 'Was genau soll in sechs Monaten anders sein, und wie beweist du es?', ''.join(k))


def teil_befragung(web):
    k = []
    k.append(kapitel('b1', 'B1', 'Befragung · Folien 13, 14', 'Prozesse werden erzählt, nicht modelliert',
        erkl('Du bekommst die Wahrheit nicht aus einem Fragebogen. Du bekommst sie, wenn jemand erzählt und du **sofort nachfragst**.',
             karten([('01', 'Interviews statt Fragebögen', 'Ein Fragebogen bekommt die geschönte Version.'), ('02', 'Handlungen, Entscheidungen, Übergaben', 'Übergaben sind der häufigste Ort für Wartezeit.'),
                     ('03', 'Ausnahmen vor Standardfall', 'Den Standardfall beschreiben alle gleich. Die Ausnahmen nicht.'), ('04', 'Sofort nachfragen', 'Im Moment klären, nicht im Nachgang.')], cols=2) +
             H('So klingt das in echt') +
             dialog([('Kim', 'Dann geben wir die Rechnung frei.'), ('Du', 'Wer ist „wir“?'), ('Kim', 'Na, normalerweise ich.'), ('Du', 'Und wenn nicht? Wie oft ist „nicht normalerweise“?'),
                     ('Kim', 'Wenn ich nicht da bin, macht das die Kollegin.'), ('Du', 'Nach welchen Kriterien? Und wenn sie auch im Urlaub ist?'), ('Kim', '… Dann wartet die Rechnung.'), ('Du', 'Wie lange ungefähr?'), ('Kim', 'Im Sommer? Sag ich jetzt lieber nichts.')]) +
             P('Vier Rückfragen, und aus einem Satz wurden eine Regel, eine Ausnahme, eine fehlende Vertretung und eine Wartezeit. Das Ganze ohne einen einzigen Vorwurf.'),
             'Beim Arzt steht auf dem Fragebogen: „Wie viel Alkohol trinken Sie?“ Antwort: „Selten.“ Im Gespräch kommt dann heraus, dass „selten“ jedes Wochenende heißt.',
             '„Dann geben wir die Rechnung frei.“ Was fehlt?', 'Wer prüft? Nach welchen Kriterien? Was passiert bei Unsicherheit? Erst diese drei Antworten machen daraus einen Schritt, den man bauen kann.') +
        fol(13, 14)))
    k.append(kapitel('b2', 'B2', 'Befragung · Folie 15', 'Das Interview in sechs Schritten',
        erkl('Sechs Schritte, und der wertvollste ist die **Gegenprobe**: Eine zweite Person aus demselben Team erzählt denselben Ablauf.',
             flow([('1 · Erzählen lassen', '„Nimm den letzten Fall von gestern und erzähl mir Schritt für Schritt, was du gemacht hast.“'), ('2 · Mitschreiben', 'In drei Spalten: Handlung, System, Entscheidung'),
                   ('3 · Nachbohren', 'Woran erkennst du das? Was, wenn das Feld leer ist? Wann bist du unsicher? Wen fragst du dann?'), ('4 · Nach dem seltenen Fall fragen', '„Wann hat das zuletzt nicht funktioniert?“'),
                   ('5 · Gegenprobe', 'Eine zweite Person aus demselben Team, unabhängig befragt'), ('6 · Zurückspiegeln', 'Die Skizze vorlesen und bestätigen lassen')], cls='steps') +
             H('Warum die Gegenprobe Gold wert ist') +
             dialog([('Kim', 'Die Rechnungen leite ich sofort an die Fachabteilung weiter.'), ('Alex', 'Die Rechnungen? Die kommen bei uns immer freitags als Sammelmail.')]) +
             merk('Die Abweichungen zwischen beiden Beschreibungen sind das wertvollste Ergebnis des ganzen Tages.') +
             korrektur('Folien 15 und 17', 'Die Gegenprobe ist laut Folie 15 der wertvollste Schritt, kommt im Arbeitsauftrag auf Folie 17 aber nicht vor, weil eure Paare meist nicht aus demselben Team stammen. Nehmt sie euch als Hausaufgabe mit: Eine Person aus deinem Team, fünfzehn Minuten, derselbe Ablauf.') +
             spiel_tool('spalten', web),
             'Zwei Leute sehen einen Unfall. Eine Person sagt rot, die andere grün. Niemand lügt. Aber jetzt weißt du, wo du genauer hinschauen musst.',
             'Warum „der letzte Fall von gestern“ statt „Wie läuft das bei euch?“', 'Allgemeine Beschreibungen sind immer die geschönte Version. Der Fall von gestern hatte echte Umwege.') +
        fol(15)))
    k.append(kapitel('b3', 'B3', 'Befragung · Folie 16', 'Die vier Alarmsätze',
        erkl('Diese vier Sätze zeigen zuverlässig: **Hier fehlt eine Regel.** Sobald du sie hörst, fragst du nach.',
             tab(['Alarmsatz', 'Was er verdeckt', 'Deine Rückfrage'], [
                 ['**„Normalerweise …“**', 'Eine unbekannte Menge an Ausnahmen', 'Und wenn nicht? Wie oft ist „nicht normalerweise“?'],
                 ['**„Das sieht man dann schon“**', 'Erfahrungswissen, das nie beschrieben wurde', 'Woran genau? Nenne mir drei Merkmale.'],
                 ['**„Das macht die Kollegin“**', 'Ein Schritt ohne Regel und ohne Vertretung', 'Nach welchen Kriterien? Was passiert, wenn sie im Urlaub ist?'],
                 ['**„Das ist eigentlich immer gleich“**', 'Unterschiede, die niemandem mehr auffallen', 'Zeig mir die letzten fünf Fälle.']]) +
             P('Das ist keine Nachlässigkeit. Menschen können Erfahrung schneller anwenden, als sie sie beschreiben können. Frag mal jemanden, wie man Fahrrad fährt.') +
             spiel_tool('rueckfrage', web),
             '„Wann ist das Steak gut?“ „Das sieht man dann schon.“ Wer oft grillt, sieht es wirklich. Automatisieren kannst du das aber erst, wenn du drei Merkmale hast: Farbe, Druckprobe, Minuten.',
             'Warum sind diese Sätze kein Vorwurf?', 'Weil sie das normale Ergebnis von Erfahrung sind. Wer sie als Fehler behandelt, bekommt bald nur noch die geschönte Version zu hören.') +
        fol(16)))
    k.append(kapitel('b4', 'B4', 'Arbeitsauftrag 01 · Folie 17 · 2 × 20 Minuten', 'Dein Interview',
        flow([('01 · Befragt werden', 'Beschreibe deinen Prozess am konkreten letzten Fall. Nicht wie er sein sollte, sondern wie er gestern war.'), ('02 · Mitschreiben', 'Als interviewende Person in drei Spalten: Handlung, System, Entscheidung.'),
              ('03 · Nachbohren', 'Bei jeder Entscheidung, mit den vier Rückfragen.'), ('04 · Vorlesen', 'Am Ende jeder Runde laut vorlesen und bestätigen lassen. Was holprig klingt, ist meist die Stelle, an der eine Regel fehlt.')], cls='steps') +
        H('Alarmsatz-Bingo fürs Interview') + bingo_tool(web) + mitschrift_tool(web) +
        beispiel('Rollentausch ist Pflicht', 'Wer nur befragt wurde, merkt nicht, wie schwer präzises Nachfragen ist und wie oft man selbst „normalerweise“ sagt. Mit der Bingo-Karte wird es erst richtig lustig.') +
        merk('Fertig, wenn beide Mitschriften vorgelesen und bestätigt sind. Danach zehn Minuten Notizen ordnen.') + fol(17)))
    return teil('teil-b', '3', 'Die Befragung', 'Ein Interview, vier Alarmsätze und eine Bingo-Karte.', ''.join(k))


def teil_skizze(web):
    k = []
    k.append(kapitel('n1', 'N1', 'Tatortskizze · Folien 18, 19', 'SIPOC: das Absperrband',
        erkl('Bevor du irgendwas zeichnest, legst du fest, **wo der Fall anfängt und wo er aufhört**. Das macht SIPOC: fünf Spalten, zehn Minuten.',
             tab(['Spalte', 'Frage', 'Rechnung', 'Pizza'], [
                 ['**S** Lieferant (Supplier)', 'Woher kommt der Input?', 'Lieferant, Kunde, Vorsystem', 'Hungrige Person mit Telefon'], ['**I** Input', 'Was genau kommt an?', 'PDF-Rechnung per E-Mail', 'Eine Bestellung'],
                 ['**P** Prozess (Process)', 'Fünf bis sieben Hauptschritte', 'Sichten, prüfen, freigeben …', 'Annehmen, belegen, backen, einpacken, ausfahren'],
                 ['**O** Output', 'Was entsteht?', 'Freigegebene Rechnung mit Protokolleintrag', 'Heiße Pizza an der Tür'], ['**C** Empfänger (Customer)', 'Wer bekommt das Ergebnis?', 'Buchhaltung, Zahlungslauf', 'Dieselbe Person, jetzt glücklich']]) +
             merk('Der eigentliche Zweck sind die zwei Markierungen: „Der Prozess beginnt hier“ und „Der Prozess endet hier“.') +
             achtung('Zehn-Minuten-Regel', 'Lassen sich die fünf Spalten nicht in zehn Minuten füllen, ist der Fall noch nicht scharf genug für die technische Planung.'),
             'Die Pizzeria ist für die Pizza bis zur Haustür zuständig. Ob du danach am Küchentisch oder auf dem Sofa isst, gehört nicht mehr dazu. Genau so ein Ende fehlt den meisten ausufernden Projekten.',
             'Warum ufern so viele Projekte aus?', 'Laut Folien-Notiz ist die häufigste Ursache ein Prozess, dessen Ende nie festgelegt wurde. Dann gehört irgendwann auch das Sofa zum Projekt.') +
        fol(18, 19)))
    k.append(kapitel('n2', 'N2', 'Tatortskizze · Folien 20, 21, 24', 'Fünf Symbole reichen',
        erkl('**BPMN** (Business Process Model and Notation) ist der weltweite Standard für Prozessdiagramme und kennt über hundert Symbole. Du brauchst fünf. Das ist kein fauler Kompromiss: Auch Profis nutzen fast nur diesen Kern.',
             '<div class="symbole">' + ''.join(f'<div class="sym"><span class="sym-i sym-{c}" aria-hidden="true"></span><b>{t}</b><small>{b}</small><p>{x}</p></div>' for c, t, b, x in [
                 ('start', 'Start', 'Start-Event', 'Der Auslöser. Jeder Workflow hat genau einen.'), ('ende', 'Ende', 'End-Event', 'Jeder Pfad endet in einem Endpunkt. Kein Pfad endet im Nichts.'), ('task', 'Aufgabe', 'Task', 'Eine Handlung, automatisiert oder manuell.'),
                 ('raute', 'Entscheidung', 'Gateway', 'Mit beschrifteten Ausgängen. Nie mehr als zwei bis drei je Raute.'), ('bahn', 'Bahn', 'Lane', 'Wer führt den Schritt aus: Person, Rolle oder System.')]) + '</div>' +
             P('Dazu kommt ein kleines **Personensymbol** in der Ecke einer Aufgabe: Hier entscheidet ein Mensch. Dort hängen später Kapazität, Zeit und rechtliche Verantwortung. In BPMN heißt das „User Task“.') +
             H('Wann lohnt sich mehr?') +
             tab(['Situation', 'Empfehlung'], [
                 ['Ein Prozess, ein oder zwei Bereiche', '**Schlanke Variante.** Aufwand: Stunden.'], ['Es gibt schon eine Prozesslandkarte oder ein QM-System mit BPMN', '**An den Bestand anschließen.** Sonst entstehen zwei Wahrheiten.'],
                 ['Mehrere verbundene Prozesse oder Zertifizierung', '**Vollständiges BPMN** im Modellierungswerkzeug. Aufwand: Tage bis Wochen.'], ['Der Prozess soll direkt aus dem Modell laufen', '**Technisch ausführbares BPMN.** Ein eigenes Projekt, nicht nebenbei.']]) +
             merk('Faustregel: Zeichne so viel Notation, wie die Person mit dem wenigsten Vorwissen im Raum lesen kann.'),
             'Der U-Bahn-Plan. Er verschweigt fast alles über die echte Stadt und wird genau deshalb von allen verstanden. Niemand braucht die Kanalisation, um vom Hauptbahnhof zum Zoo zu kommen.',
             'Du entdeckst, dass es schon eine Prozesslandkarte gibt. Was tust du?', 'Nachfragen, bevor du zeichnest. Sie ist die beste Vorlage, die du bekommen kannst, und zwei Darstellungen desselben Ablaufs sind schlimmer als keine.') +
        fol(20, 21, 24)))
    k.append(kapitel('n3', 'N3', 'Tatortskizze · Folien 22, 23', 'Der Fall der verschwundenen Tage',
        erkl('Mit **Bahnen** sieht jede Person: Jeder Pfeil über eine Bahngrenze ist eine **Übergabe**. Und dort verschwindet die Zeit.',
             zeitstrahl() +
             tab(['Zeit', 'Bedeutet', 'Im Fall 0815'], [['**Bearbeitungszeit**', 'Jemand arbeitet wirklich daran', '12 Minuten'], ['**Durchlaufzeit**', 'Vom Anfang bis zum Ende, inklusive Warten', '5 Tage (1,5 + 2 + 0,5 + 1)'], ['**Verhältnis**', 'Bei einem 8-Stunden-Arbeitstag (unsere Annahme)', f'1 Minute Arbeit, {VERHAELTNIS} Minuten Warten']]) +
             H('Drei Befunde, die man ohne Bahnen nicht sieht') +
             karten([('1', 'Wartezeit statt Arbeitszeit', 'Die Rechnung von gestern misst Bearbeitungszeit. Was das Geschäft stört, ist oft die Durchlaufzeit. Beides gehört in die Erfolgskriterien.'),
                     ('2', 'Übergaben sind die Kandidaten', 'Zusammenstellen, weiterleiten, warten, erinnern, Rückfrage beantworten. Das lässt sich oft automatisieren, ohne eine einzige fachliche Entscheidung anzutasten. Der risikoärmste Einstieg überhaupt.'),
                     ('3', 'Bahnen zeigen Zuständige', 'Wer eine eigene Bahn hat, ist beteiligt. Wer nachträglich auftaucht, ist ein Risiko.')]) +
             merk('Prüfe an jeder Bahngrenze zuerst: Muss diese Übergabe überhaupt stattfinden? Der wertvollste Schritt entfällt sehr oft einfach.') +
             korrektur('Folien 21 und 22', 'Schau dir die Raute „Betrag über 1.000 €?“ auf Folie 22 genau an: Sie hat nur einen, unbeschrifteten Ausgang. Folie 21 verlangt aber beschriftete Ausgänge, und kein Pfad darf im Nichts enden. Was passiert mit Rechnungen unter 1.000 Euro? Genau diese Frage solltest du im Interview stellen. Die vereinfachte Skizze ist also auch eine kleine Detektivaufgabe.'),
             'Beim Arzt: zwei Stunden Wartezimmer, fünf Minuten Behandlung. Wer die Behandlung halbiert, ist immer noch fast zwei Stunden da. Wer das Wartezimmer abschafft, wird gefeiert.',
             'Du automatisierst die 12 Minuten vollständig. Wie lang ist der Durchlauf?', 'Immer noch rund 5 Tage. Wer nur die Bearbeitungszeit automatisiert, verändert an der Durchlaufzeit fast nichts.') +
        fol(22, 23)))
    k.append(kapitel('n4', 'N4', 'Arbeitsauftrag 02 · Folie 25 · 40 Minuten allein', 'Deine Tatortskizze',
        P('Erst das Absperrband, dann die Skizze. Beides baut auf deiner Mitschrift auf.') +
        sipoc_tool(web) +
        flow([('01 · Bahnen festlegen', 'Personen, Rollen oder Systeme. Eine Bahn je Beteiligtem, höchstens fünf.'), ('02 · Schritte eintragen', 'Aus deiner Mitschrift, jeden in die Bahn dessen, der ihn ausführt.'),
              ('03 · Übergaben beziffern', 'Jeder Pfeil über eine Bahngrenze ist eine Übergabe. Wartezeit schätzen und dranschreiben.'), ('04 · Zwei Summen', 'Bearbeitungszeit gesamt und Durchlaufzeit gesamt.')], cls='steps') +
        bahnen_tool(web) +
        beispiel('Die Auswertungsfrage', 'Wie groß ist der Unterschied, und an welcher Übergabe hängt der größte Anteil? Laut Folien-Notiz gibt es in fast jeder Gruppe einen Fall mit 1 zu 50 oder schlechter. Den stellen wir im Plenum vor.') +
        korrektur('Folie 38', 'Der SIPOC steht auf Folie 38 unter den Ergebnissen, hat aber keinen eigenen Arbeitsauftrag. Wir machen ihn deshalb als Einstieg in Auftrag 02.') +
        merk('Fertig, wenn beide Summen dastehen und jede Übergabe eine Zeitangabe hat.') + fol(25)))
    k.append(kapitel('n5', 'N5', 'Tatortskizze · Folien 26, 27', 'Ist und Soll trennen, und Schritt Null',
        erkl('Erst aufnehmen, was **ist**. Erst danach überlegen, was sein **soll**. Wer beides vermischt, dokumentiert einen Prozess, den es nie gab.',
             tab(['Ist-Prozess', 'Soll-Prozess'], [
                 ['Wie es heute wirklich läuft', 'Wie es nach der Automatisierung laufen soll'], ['Mit Umwegen, Zwischenablagen, Zettelwirtschaft und der einen Datei auf dem Desktop einer Kollegin', 'Mit Markierung: Was entfällt? Was wird automatisiert? Was bleibt bewusst manuell? Welche Übergabe fällt weg?'], ['Ohne Wertung aufgenommen', 'Die Differenz ist der eigentliche Projektinhalt, und die Grundlage für Aufwand und Preis']]) +
             achtung('Der häufigste Fehler', 'Der Ist-Prozess wird schöner aufgeschrieben, als er ist, weil niemand als schlecht organisiert dastehen will. Dagegen hilft nur eins: die Aufnahme ausdrücklich als Bestandsaufnahme ankündigen, nicht als Bewertung.') +
             '<blockquote class="kernsatz">Ein Prozess, der vor der Automatisierung nicht funktioniert, funktioniert danach schneller nicht.</blockquote>' +
             P('Das ist der übersprungene **Schritt Null**. KI auf einem instabilen Ablauf erzeugt schnellere Fehler, keine besseren Ergebnisse. Die Reihenfolge heißt dann: erst reparieren, dann automatisieren. Das ist unbequem und spart Monate.'),
             'Das Vorher-Foto im Fitnessstudio. Wer dabei den Bauch einzieht, sieht nach drei Monaten keinen Fortschritt. Das Foto muss ehrlich sein, sonst ist es wertlos. Und wenn der Trainingsplan Mist ist, hilft auch kein schnelleres Laufband.',
             'Im Interview zeigt jemand stolz eine Abkürzung, die eigentlich verboten ist. Was tust du?', 'Aufnehmen, ohne Wertung. Sie ist Teil des Ist. Ob sie im Soll bleibt, wird später entschieden.') +
        fol(26, 27)))
    k.append(kapitel('n6', 'N6', 'Arbeitsauftrag 03 · Folie 28 · 55 + 20 Minuten', 'Der SOP: so klar, dass der Zettel reicht',
        erkl('**SOP** heißt Standard Operating Procedure, also schriftliche Arbeitsanweisung. Maßstab: Eine neue Kollegin könnte jeden Schritt ausführen, ohne nachzufragen.',
             tab(['Regel', 'Schlecht', 'Gut'], [
                 ['Jeder Schritt beginnt mit der Rolle', '„Ranking prüfen.“', '„Der SEO-Spezialist überprüft das aktuelle Ranking in Software xy.“'],
                 ['Nummeriert, echte Reihenfolge, mit System', '„Danach Rechnung prüfen.“', '„3. Die Buchhaltung gleicht Betrag und Lieferant in der Buchhaltungssoftware ab.“'],
                 ['Wartezeiten sind eigene Schritte', 'Fehlen einfach', '„4. Wartezeit: Die Rechnung liegt im Schnitt 2 Tage im Postfach der Fachabteilung.“']]) +
             H('Gegenlesen zu zweit') +
             P('Die andere Person markiert jede Stelle, an der sie nachfragen müsste. **Nicht diskutieren, nur markieren.** Jede Markierung ist entweder eine fehlende Regel oder eine noch nicht erfasste Ausnahme. Beides wandert in Block 4.') +
             sop_tool(web),
             'Der Zettel für die Person, die im Urlaub deine Katze füttert. „Katze füttern“ reicht nicht. „Morgens um 8 eine halbe Dose aus dem Regal links. Wenn sie nicht frisst: abwarten, sie ist beleidigt. Tierärztin erst nach zwei Tagen.“ Das ist ein SOP.',
             'Was fehlt an „Die Rechnung wird normalerweise schnell geprüft“?', 'Alles: keine Rolle, kein System, kein Kriterium, und ein Alarmsatz ist auch noch dabei.') +
        merk('Fertig, wenn jeder Schritt eine Rolle und ein System nennt und die Markierungen notiert sind.') + fol(28)))
    return teil('teil-n', '4', 'Die Tatortskizze', 'Absperrband, fünf Symbole, Bahnen und der Zettel für die neue Kollegin.', ''.join(k))


def teil_beweise(web):
    k = []
    k.append(kapitel('k1', 'K1', 'Beweise sichern · Folien 29, 30', 'Scope: rein, raus, Annahmen',
        erkl('**Scope** heißt Umfang. Du schreibst auf, was dazugehört, was nicht, und worauf das Ganze beruht. **Die Out-of-Scope-Liste ist der wichtigere Teil**, denn sie verhindert die Diskussion, die sonst in Monat drei kommt.',
             tab(['Liste', 'Was hinein gehört', 'Merke'], [
                 ['**In Scope**', 'Was ausdrücklich dazugehört', 'Konkret genug, um an einem einzelnen Fall zu entscheiden'],
                 ['**Out of Scope**', 'Was ausdrücklich nicht dazugehört', 'Immer mit Schutzsatz: „Alles, was hier nicht ausdrücklich aufgeführt ist, gilt als außerhalb des Umfangs.“'],
                 ['**Annahmen**', 'Datenqualität, Zugänge, Ansprechpersonen, Volumen', 'Ändert sich eine Annahme, ändert sich der Aufwand']]) +
             spiel_tool('tuersteher', web) +
             beispiel('Drei Sätze, die ein halbes Jahr Diskussion ersparen', 'Nur interne Support-E-Mails. Keine Sonderfälle. Keine historischen Daten.'),
             'Du beauftragst jemanden, das Wohnzimmer zu streichen. Beim Termin: „Ach, und die Decke? Und der Flur wäre auch schön.“ Ohne Liste wird es ein Streit. Mit Liste wird es ein neues Angebot.',
             'Warum reicht die In-Scope-Liste nicht?', 'Weil niemand alles aufzählen kann, was nicht gemeint ist. Der Schutzsatz und die Ausschlussliste schließen die Lücke.') +
        fol(29, 30)))
    k.append(kapitel('k2', 'K2', 'Beweise sichern · Folien 31, 32', 'Erfolgskriterien brauchen einen Ausgangswert',
        erkl('Ohne die Spalte **„Wert heute“** gibt es später keinen Nachweis, und keine Verteidigung gegen den Satz „Gefühlt bringt das nichts“.',
             tab(['Kriterium', 'Wert heute', 'Zielwert', 'Messquelle', 'Gemessen wann'], [
                 ['Bearbeitungszeit je Rechnung', '4,0 Minuten', '1,2 Minuten', 'Zeitmessung Stichprobe, 20 Fälle', 'Monat 1 und Monat 4'],
                 ['**Durchlaufzeit je Rechnung**', '5,0 Tage', '1,5 Tage', 'Zeitstempel im System', 'monatlich'],
                 ['Anteil ohne manuelle Prüfung', '0 Prozent', '70 Prozent', 'Freigabeprotokoll', 'monatlich'],
                 ['**Fehlerquote bei Freigaben**', '1,8 Prozent', 'höchstens 1,8 Prozent', 'Nachprüfung Stichprobe', 'Monat 3']]) +
             P('Die Durchlaufzeit kommt aus deiner Bahnen-Analyse. Und das Kriterium, das nur Gleichstand verlangt, ist laut Folien-Notiz oft das, an dem ein Projekt wirklich scheitert. **„Zielwert gleich Ausgangswert“ ist also ausdrücklich erlaubt.**') +
             korrektur('Folie 31', 'Die 1,2 Minuten ergeben sich, wenn 70 % der Rechnungen gar keine Zeit mehr kosten (30 % × 4 Minuten). Im Business Case von gestern stand aber noch eine Restprüfzeit von 0,5 Minuten. Damit wären es rund 1,55 Minuten. Passe den Zielwert an deine Annahme an, und nimm dieselbe Annahme in beiden Rechnungen.') +
             '<blockquote class="kernsatz">Ohne Messgröße gibt es kein Projekt. Nur Beschäftigung.</blockquote>',
             'Wer vor der Diät nicht auf die Waage steigt, kann nach drei Monaten nur noch sagen: „Ich fühl mich leichter.“ Das ist schön, aber kein Beweis, und dem nächsten Stück Kuchen ist es egal.',
             'Warum ist „Fehlerquote höchstens 1,8 %“ so wichtig, obwohl sich nichts verbessert?', 'Es sichert zu, dass die Qualität durch mehr Tempo nicht schlechter wird.') +
        fol(31, 32)))
    k.append(kapitel('k3', 'K3', 'Beweise sichern · Folie 33', 'Wenn du den Ausgangswert nicht kennst',
        erkl('Das ist der häufigste Fall und **kein Grund zum Abbruch**. Es heißt nur: Die erste Projektaufgabe ist eine Messung, und die gehört in Aufwand und Zeitplan.',
             karten([('01', 'Stichprobe von Hand', 'Zwanzig Fälle mit der Stoppuhr. Ungenau, aber in zwei Stunden erledigt und besser als jede Schätzung.'), ('02', 'Systemauswertung', 'Zeitstempel aus Ticketsystem, Postfach oder ERP. Für Durchlaufzeiten fast immer die beste Quelle. Prüfe, ob die Stempel den echten Bearbeitungszeitpunkt zeigen.'),
                     ('03', 'Eine Woche aufschreiben', 'Am wenigsten beliebt, am aussagekräftigsten für verteilte Tätigkeiten.')]) +
             achtung('Was man nicht tun sollte', 'Die Zahl schätzen und später so tun, als sei sie gemessen worden. Das rächt sich genau dann, wenn der Erfolg belegt werden soll.') +
             tipp('Messen, ohne Ärger zu bekommen', 'Miss den Prozess, nicht die Person. Stoppuhr und Zeitstempel können Rückschlüsse auf einzelne Beschäftigte zulassen. Deshalb: Vorher erklären, wozu gemessen wird, und bei einem Betriebsrat diesen früh einbinden (Frage 9 auf Folie 11). Das ist unser Praxis-Hinweis, keine Rechtsberatung.'),
             'Du weißt nicht, wie lange du zur Arbeit brauchst? Fünfmal Stoppuhr, fertig. Nicht perfekt, aber besser als „so zwanzig Minuten, glaub ich“, wenn es in Wahrheit vierzig sind.',
             'Was steht bei unbekanntem Wert in der Spalte „Wert heute“?', 'Wie er erhoben wird und bis wann. Zum Beispiel: „Stichprobe, 20 Fälle, bis 20.11.“') +
        fol(33)))
    k.append(kapitel('k4', 'K4', 'Beweise sichern · Folie 34', 'Wer ist wer im Projekt',
        erkl('Vier Rollen. In kleinen Organisationen oft dieselbe Person, aber **immer ausgesprochen**.',
             tab(['Rolle', 'Aufgabe', 'Beim Hausbau'], [
                 ['**Auftraggeber**', 'Entscheidet über Budget und Umfang, priorisiert bei Konflikten', 'Wer bezahlt'],
                 ['**Fachlicher Eigentümer**', 'Definiert, was fachlich richtig ist, nimmt ab und bleibt nach der Übergabe zuständig', 'Wer darin wohnt und weiß, wie es sein muss'],
                 ['**Umsetzung**', 'Baut, dokumentiert, testet technisch', 'Das Handwerk'], ['**Betrieb**', 'Überwacht nach der Übergabe, reagiert auf Alarme, verwaltet Zugänge', 'Die Hausverwaltung']]) +
             merk('Der fachliche Eigentümer ist die wichtigste und am häufigsten unbesetzte Rolle.') +
             P('Je nach Fall kommen Datenschutzbeauftragte, IT-Sicherheit, Betriebsrat und die Rechtsabteilung dazu.'),
             frage='Du bist allein im Projekt. Brauchst du die Rollen trotzdem?', antwort='Ja. Sprich sie aus: „Heute bin ich Auftraggeber, also entscheide ich das Budget.“ Sonst bleibt jede Scope-Diskussion mit dir selbst offen, und die kann lange dauern.') +
        fol(34)))
    k.append(kapitel('k5', 'K5', 'Beweise sichern · Folien 35, 36', 'Prüfpunkte, und wo der Aufwand wirklich steckt',
        erkl('Ein Projektzyklus ohne Übergangsbedingungen ist eine Wunschliste. Und **der Bau ist selten der größte Posten**.',
             tab(['Phase', 'Prüfpunkt'], [
                 ['Problemdefinition', 'Ziel in einem Satz mit Zahl und Zeitpunkt? Ausschlusskriterien geprüft?'], ['Prozessaufnahme', 'Ist-Prozess in Bahnen dokumentiert? Ausnahmen mit Häufigkeiten erfasst?'], ['Ziel und Abgrenzung', 'In-Scope und Out-of-Scope schriftlich bestätigt?'],
                 ['**Workflow-Skizze**', '**Kann der Fachbereich den Ablauf ohne technische Begriffe nacherzählen?** Der wichtigste Prüfpunkt.'], ['Umsetzung', 'Alle Anforderungssätze im Testsystem erfüllt?'], ['Test', 'Erfolgsquote und Abweichungsrate gegen die Schwelle gemessen?'], ['Übergabe', 'Verantwortliche benannt? Dokumentation durchgegangen? Monitoring aktiv?']]) +
             H('Der Eisberg') +
             '<div class="eisberg" role="img" aria-label="Aufwandsverteilung: nur der Bau mit 20 bis 30 Prozent steht üblicherweise im Angebot"><div class="eb-a"><b>20–30 %</b> Technische Umsetzung<small>steht im Angebot</small></div><div class="eb-u"><span><b>25–35 %</b> Problemdefinition, Aufnahme, Scope</span><span><b>10 %</b> Skizze und Abstimmung</span><span><b>20–25 %</b> Test und Korrekturen</span><span><b>10–15 %</b> Übergabe, Doku, Schulung</span><small>fällt ebenfalls an und steht meist nicht drin</small></div></div>' +
             P('Bei internen Teams gilt dasselbe. Es heißt dort nur nicht „unbezahlt“, sondern „nicht eingeplant“, und es zeigt sich als Terminüberschreitung. Heute hast du also schon ein gutes Viertel des Projekts erledigt, ohne eine Zeile zu bauen.'),
             'Beim Hochzeitsbudget reden alle über Kleid und Band. Am Ende kosten Saal, Essen, Getränke und die Gäste, die doch noch kommen, ein Vielfaches davon.',
             'Ein Angebot lautet „Automatisierung: 5.000 Euro“ und meint nur den Bau. Was kostet es wirklich?', 'Bei 20–30 % Anteil rund 17.000 bis 25.000 Euro Gesamtaufwand. Frag nach, wer den Rest macht.') +
        fol(35, 36)))
    k.append(kapitel('k6', 'K6', 'Arbeitsauftrag 04 · Folie 37 · 45 + 35 Minuten', 'Ziel, Scope, Erfolgskriterien',
        flow([('01 · Zielsatz', 'Erst die fünf Bausteine einzeln füllen, dann zusammensetzen. Höchstens drei Sätze, dazu ein Projektname ohne Technologiebegriff.'), ('02 · Scope', 'Mindestens sechs Einträge in Scope, mindestens sechs out of Scope, dazu drei Annahmen mit der Notiz, was passiert, wenn sie nicht stimmen.'),
              ('03 · Erfolgskriterien', 'Drei bis fünf Stück, davon mindestens eines zur Durchlaufzeit aus deiner Bahnen-Analyse.'), ('04 · Wert heute', 'Pflichtspalte. Wo die Zahl unbekannt ist, steht dort, wie sie erhoben wird und bis wann.')], cls='steps') +
        ziel_tool(web) + scope_tool(web) + kriterien_tool(web) +
        beispiel('Im Plenum', 'Drei Zielsätze werden vorgelesen und gemeinsam geschärft. Freiwillige zuerst.') +
        merk('Fertig, wenn der Zielsatz alle fünf Bausteine enthält und jedes Kriterium eine Spalte „Wert heute“ hat.') + fol(37)))
    k.append(kapitel('k7', 'K7', 'Abschluss · Folie 38', 'Die Akte ist komplett',
        P('Der Fall ist jetzt beschrieben, abgegrenzt und messbar. Ab morgen wird konstruiert.') +
        tab(['Teil der Akte', 'Aus Auftrag'], [['Interviewmitschrift in drei Spalten', '01'], ['SIPOC mit festgelegtem Anfang und Ende', '02'], ['Ist-Prozess in Bahnen mit bezifferten Übergaben', '02'], ['Vollständiger SOP, gegengelesen', '03'], ['Zielsatz mit fünf Bausteinen', '04'], ['In-Scope- und Out-of-Scope-Listen mit Annahmen', '04'], ['Drei bis fünf Erfolgskriterien mit Ausgangswerten', '04']]) +
        export_tool(web) +
        P('**Im nächsten Block** wird aus dem beschriebenen Ablauf eine Konstruktion, mit Entscheidungslogik, Ausnahmepfaden, Fehlerverhalten und einem Testplan, der vorher festlegt, was gut genug ist.') +
        tipp('Hausaufgabe, die den Unterschied macht', 'Bring zwei oder drei echte Fälle aus deinem Prozess **anonymisiert** mit. Namen, Adressen und Beträge unkenntlich machen. Wer morgen mit echten Beispielen arbeitet, baut einen echten Testplan statt einer Übung. Und falls noch Zeit ist: die Gegenprobe mit einer Person aus deinem Team.') + fol(38)))
    return teil('teil-k', '5', 'Beweise sichern', 'Was gehört dazu, was nicht, und woran misst du in sechs Monaten den Erfolg?', ''.join(k))


# (Bereich, Haupt-Use-Case von Montag, Zielsatz, SIPOC-Anfang, SIPOC-Ende, [(Bahn, Warten davor)], Minuten, draußen, Kriterium)
BEISPIELE = {
    'ingo': ('Ingo · Druck & Vertrieb', 'Druckanfragen vorsortieren',
             '70 Prozent der Druckanfragen mit vollständigen Angaben werden automatisch der richtigen Druckart zugeordnet, gemessen an der Zuordnungsquote im Wochenbericht, ab zwei Monaten nach Start.',
             'Anfrage per Formular oder E-Mail', 'Vorsortierte Anfrage mit allen Angaben beim Innendienst', [('Innendienst', 1), ('Druckvorstufe', 1.5), ('Innendienst', .5)], 8,
             'Sonderformate, Aufträge ab 5.000 Stück, Reklamationen', 'Durchlaufzeit je Anfrage: heute 3 Tage, Ziel 1 Tag, Zeitstempel im Postfach, monatlich'),
    'carmen': ('Carmen · Team & Website', 'Website-Anfragen vorsortieren',
               '70 Prozent der Website-Anfragen mit eindeutigem Anliegen werden automatisch der zuständigen Person zugewiesen, gemessen am Anteil ohne Umleitung im Monatsbericht, ab dem dritten Monat.',
               'Ausgefülltes Website-Formular', 'Anfrage liegt bei der zuständigen Person', [('Team-Postfach', .5), ('Teamleitung', 1), ('Zuständige Person', 1)], 8,
               'Bewerbungen, Beschwerden, Anfragen mit laufendem Vertrag', 'Durchlaufzeit je Anfrage: heute 2,5 Tage, Ziel 0,5 Tage, Zeitstempel im Formularsystem, monatlich'),
    'tabea': ('Tabea · Video & Design', 'Feedbackrunden bündeln',
              '80 Prozent der Feedbackrunden zu Standardvideos werden automatisch in einer Liste gebündelt und an den Schnitt übergeben, gemessen am Anteil ohne Nachfrage, ab zwei Monaten nach Start.',
              'Rohschnitt mit Feedback-Link', 'Gebündelte Änderungsliste beim Schnitt', [('Kundschaft', 2), ('Projektleitung', 1), ('Schnitt', 1)], 12,
              'Erstgespräche, Freigaben durch die Rechtsabteilung, Kampagnen mit mehreren Beteiligten', 'Durchlaufzeit je Runde: heute 4 Tage, Ziel 1,5 Tage, Zeitstempel im Projektwerkzeug, je Monat'),
}


def teil_mitnehmen(pid, web):
    order = [pid] + [x for x in BEISPIELE if x != pid] if pid in BEISPIELE else list(BEISPIELE)
    out = ''
    for p in order:
        label, haupt, ziel, a, e, bahnen, minuten, raus, krit = BEISPIELE[p]
        tage = sum(w for _, w in bahnen)
        verh = round(tage * ARBEITSTAG / minuten)
        groesste = max(bahnen, key=lambda b: b[1])
        wege = ' → '.join(f'{b} (Ø {str(w).replace(".", ",")} Tage)' for b, w in bahnen)
        out += (f'<div class="steck-bsp{" mein" if p == pid else ""}"><p class="steck-h">{E(label)}{" · dein Bereich" if p == pid else ""}</p>' +
                tab(['Teil der Akte', 'Beispiel'], [
                    ['Haupt-Use-Case', haupt], ['Zielsatz', ziel], ['SIPOC', f'Beginnt mit: {a}. Endet mit: {e}.'], ['Bahnen', wege],
                    ['Zwei Summen', f'{minuten} Minuten Bearbeitung, {str(tage).replace(".", ",")} Tage Durchlauf, also 1 zu {verh}. Größte Übergabe: {groesste[0]}.'],
                    ['Out of Scope', raus], ['Erfolgskriterium', krit]], cls='steck-tab') + '</div>')
    v = ''.join(vorlage(a, web, MATERIAL) for a in AUTOMATIONS)
    k = kapitel('m1', 'M1', 'Alle Zahlen erfunden', 'Drei fertige Akten zum Abgucken', out +
                tipp('Fällt dir etwas auf?', 'In allen drei Fällen ist nicht die Arbeit das Problem. Die Minuten bleiben dieselben wie gestern im Business Case. Die Tage hat gestern niemand gerechnet.'))
    s = kapitel('m2', 'M2', 'Der Tag auf einer Seite', 'Spickzettel für Ermittelnde',
                '<div class="spick">' + ''.join(f'<div class="spick-box"><h4>{E(t)}</h4><ul>' + ''.join(f'<li>{md(x)}</li>' for x in items) + '</ul></div>' for t, items in [
                    ('Die Grundregel', ['Verdächtig ist nur der Prozess', 'Widerspruch ist Gold, kein Vorwurf', 'Nur Beschreibbares ist automatisierbar']),
                    ('Das Ziel', ['Anteil, Fallmenge, Handlung, Kennzahl, Zeitpunkt', 'Test: drei Sätze ohne Werkzeug', 'Zahl, Grenze, Ausschlussliste']),
                    ('Die Befragung', ['Letzter Fall von gestern', 'Handlung, System, Entscheidung', 'Normalerweise? Sieht man? Die Kollegin? Immer gleich?', 'Gegenprobe ist der wertvollste Schritt']),
                    ('Die Skizze', ['SIPOC: Anfang und Ende in 10 Minuten', 'Start, Ende, Aufgabe, Entscheidung, Bahn', 'Pfeil über Bahngrenze = Übergabe', 'Zwei Summen: Bearbeitung und Durchlauf']),
                    ('Vor dem Bauen', ['Muss die Übergabe überhaupt sein?', 'Ist und Soll trennen', 'Schritt Null: erst reparieren', 'SOP: Rolle, System, Wartezeit als Schritt']),
                    ('Die Beweise', ['Out of Scope mit Schutzsatz', 'Wert heute ist Pflicht', 'Unbekannt? Erste Aufgabe: messen', 'Fachlicher Eigentümer benannt?', 'Bau nur 20–30 % des Aufwands'])]) + '</div>')
    w = kapitel('m3', 'M3', 'Alle Fachwörter des Tages', 'Wörterliste', glossar([(a, b, '') for a, b in BEGRIFFE]))
    q = kapitel('m4', 'M4', 'Stand 03.11.2026', 'Prüfstand und Grenzen',
                P('Die Zeiten auf Folie 22 ergeben zusammen die genannten 5 Tage. Die Präzisierungen stehen bei den jeweiligen Kapiteln. Das Arbeitsheft 3, auf das die Folien verweisen, lag uns nicht vor: Werkzeuge und Ausfülltabellen folgen den Angaben der Folien. '
                  'Die Reihe zählt laut Folie 2 jetzt sechs Blöcke, die Folien von gestern sprachen noch von fünf Teilen. Die Make-Vorlagen sind mit Makes eigener Prüfung abgeglichen, aber nicht in euren Konten ausgeführt. Kim, Alex, Sascha, die Rechnung 0815 und alle Beispiele sind erfunden. Die Bonus-Sätze im Bingo stammen von uns, nicht von den Folien.'))
    return teil('teil-m', '↓', 'Mitnehmen', 'Beispiele, Make-Vorlagen, Spickzettel und Wörter.', k + vorlagen_kapitel(web) + v + s + w + q)


def vorlagen_kapitel(web):
    knopf = f'<p><a class="btn primary" href="{MATERIAL}/{ZIP}" download>Alle drei Vorlagen als ZIP</a></p>' if web else ''
    return kapitel('m0', 'M0', 'Make-Vorlagen · Import wie gewohnt', 'Ermitteln in Make',
                   P('Drei fertige Vorlagen machen die Regeln von heute in Make sichtbar. Alle laufen mit Make Free und ohne fremdes Konto.') +
                   flow([('1 · Herunterladen', 'JSON-Datei speichern.'), ('2 · Neues Szenario', 'In Make: Scenarios → + Create a new scenario.'),
                         ('3 · Importieren', 'Drei Punkte oben rechts → Import blueprint → Datei wählen → Save.'), ('4 · Starten', 'Speichern, dann Run once. Das Ergebnis steht in der Sprechblase über dem letzten Modul.')], cls='steps') + knopf)


TOC = [('teil-r', '← Was bisher geschah', [('r1', 'Der Rückblick auf Montag')]),
       ('teil-s', 'Der Fall des Tages', [('s1', 'Das Tagebuch der Rechnung 0815')]),
       ('teil-a', '1 · Tatort besichtigen', [('a1', 'Prozesse sind passiert'), ('a2', 'Zwei Wege, ein Ergebnis'), ('a3', 'Die Unschärfe')]),
       ('teil-z', '2 · Den Auftrag klären', [('z1', 'Der Schmerz'), ('z2', 'Fünf Bausteine'), ('z3', 'Zehn Fragen'), ('z4', 'Brauchbare Antworten')]),
       ('teil-b', '3 · Die Befragung', [('b1', 'Prozesse werden erzählt'), ('b2', 'Sechs Schritte'), ('b3', 'Vier Alarmsätze'), ('b4', 'Auftrag 01: Interview')]),
       ('teil-n', '4 · Die Tatortskizze', [('n1', 'SIPOC'), ('n2', 'Fünf Symbole'), ('n3', 'Die verschwundenen Tage'), ('n4', 'Auftrag 02: Bahnen'), ('n5', 'Ist, Soll, Schritt Null'), ('n6', 'Auftrag 03: SOP')]),
       ('teil-k', '5 · Beweise sichern', [('k1', 'Scope'), ('k2', 'Erfolgskriterien'), ('k3', 'Wenn der Wert fehlt'), ('k4', 'Rollen'), ('k5', 'Prüfpunkte, Aufwand'), ('k6', 'Auftrag 04: Ziel, Scope, Kriterien'), ('k7', 'Die Akte ist komplett')]),
       ('teil-m', 'Mitnehmen', [('m1', 'Drei Akten'), ('m0', 'Make-Vorlagen'), ('m2', 'Spickzettel'), ('m3', 'Wörter'), ('m4', 'Grenzen')])]

ABDECKUNG = {1: 's1', 2: 's1', 3: 'a1', 4: 'a1', 5: 'a2', 6: 'a3', 7: 'z1', 8: 'z1', 9: 'z2', 10: 'z2', 11: 'z3', 12: 'z4', 13: 'b1', 14: 'b1', 15: 'b2', 16: 'b3', 17: 'b4', 18: 'n1', 19: 'n1',
             20: 'n2', 21: 'n2', 22: 'n3', 23: 'n3', 24: 'n2', 25: 'n4', 26: 'n5', 27: 'n5', 28: 'n6', 29: 'k1', 30: 'k1', 31: 'k2', 32: 'k2', 33: 'k3', 34: 'k4', 35: 'k5', 36: 'k5', 37: 'k6', 38: 'k7'}
assert sorted(ABDECKUNG) == list(range(1, 39))


def body(pid, web=True):
    return teil_erinnerung(web) + teil_start() + teil_ausgang() + teil_ziel(web) + teil_befragung(web) + teil_skizze(web) + teil_beweise(web) + teil_mitnehmen(pid, web)
