"""Lernheft Modul 2 · Tag 6: Use Cases bewerten und rechnen. Beginnt mit der Erinnerung an Freitag.

Aufbau je Thema nach LERNKONZEPT.md: Einfach gesagt → Einzelheiten → Alltagsbeispiel → Verständnisfrage → mögliche Antwort.
Interaktive Werkzeuge nur im Web (web=True), in der PDF-Fassung stehen Ausfülltabellen.
"""
from ..woche1.bausteine import E, md, P, H, merk, achtung, tipp, korrektur, beispiel, tab, flow, karten, glossar, kapitel, teil
from ..woche1.blueprints import STECKBRIEF_FELDER
from ..woche1.inhalt import vorlage
from .daten import BEGRIFFE
from .vorlagen import AUTOMATIONS, MATERIAL, ZIP

KRITERIEN = [('n', 'Nutzen', 40, 'kaum messbar', 'spürbar, schwer beziffert', 'hoher, messbarer Effekt'),
             ('d', 'Datenverfügbarkeit', 25, 'Daten fehlen oder unzugänglich', 'vorhanden, aber uneinheitlich', 'vollständig, sauber, zugänglich'),
             ('e', 'Einfachheit', 20, 'viele Systeme, viele Sonderfälle', 'überschaubar', 'ein System, klare Regeln'),
             ('r', 'Risikoarmut', 15, 'Fehler haben gravierende Folgen', 'Fehler korrigierbar', 'Fehler folgenlos')]
HERKUNFT = ['gemessen', 'nachgeschlagen', 'geschätzt']
NUTZEN = [('volumen', 'Volumen pro Monat', 'Vorgänge', 800), ('zeit', 'Zeit heute je Vorgang', 'Minuten', 4), ('anteil', 'Automatisierbarer Anteil', '%', 70),
          ('rest', 'Restzeit je automatisiertem Vorgang', 'Minuten', 0.5), ('satz', 'Stundensatz', '€', 45), ('fehler', 'Vermiedene Fehlerkosten pro Monat', '€', 0)]
EINMALIG = [('e1', 'Analyse und Prozessaufnahme', 1500), ('e2', 'Aufbau des Workflows', 4500), ('e3', 'Datenaufbereitung', 2400), ('e4', 'Integration in bestehende Systeme', 1500),
            ('e5', 'Test und Abnahme', 900), ('e6', 'Schulung und Einführung', 900), ('e7', 'Dokumentation, ggf. Datenschutz-Folgenabschätzung', 300)]
LAUFEND = [('l1', 'Plattform und Lizenzen', 90), ('l2', 'Nutzung der KI-Modelle', 60), ('l3', 'Monitoring und Betrieb', 40), ('l4', 'Wartung und Anpassung', 100),
           ('l5', 'Zusätzliche menschliche Prüfung', 0), ('l6', 'Dokumentation und Audits', 10)]
assert sum(x[2] for x in EINMALIG) == 12000 and sum(x[2] for x in LAUFEND) == 300


def fol(*nums):
    links = ' · '.join(f'<a href="/hefte/folien/tag-25/{n:02d}.jpg" target="_blank" rel="noopener">Folie {n}</a>' for n in nums)
    return f'<p class="folien-ref">Originalfolien: {links}</p>'


def erkl(einfach, inner='', alltag='', frage='', antwort=''):
    out = f'<div class="einfach"><span class="lbl">Einfach gesagt</span><p>{md(einfach)}</p></div>{inner}'
    if alltag:
        out += beispiel('Wie im Alltag', alltag)
    if frage:
        out += (f'<details class="verstehen"><summary><span class="lbl">Kurz prüfen</span> {md(frage)}</summary><p><b>Mögliche Antwort:</b> {md(antwort)}</p></details>')
    return out


def bc(v, m, a, r, sd, lauf, inv):
    """Gleiche Rechnung wie Folie 19 und bewerten.js: Stunden auf ganze Zahl gerundet."""
    h = round(v * a / 100 * (m - r) / 60)
    brutto = h * sd
    netto = brutto - lauf
    return dict(h=h, brutto=brutto, netto=netto, amort=inv / netto, roi12=(netto * 12 - inv) / inv * 100, roi36=(netto * 36 - inv) / inv * 100, tco=inv + lauf * 36)


def de(x, d=0):
    s = f'{x:,.{d}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


FOLIE19 = bc(800, 4, 70, .5, 45, 300, 12000)
assert FOLIE19['brutto'] == 1485 and FOLIE19['netto'] == 1185 and FOLIE19['tco'] == 22800 and round(FOLIE19['roi12'], 1) == 18.5


# ================================================================ Werkzeuge

def freitag_tool(web):
    if not web:
        return ('<p class="ausfuell-zeile">Meine drei Kandidaten von Freitag: 1. ______________________ 2. ______________________ 3. ______________________</p>')
    return ('<div class="tool" data-tool="freitag"><div class="tool-h"><b>Deine Kandidaten von Freitag</b><span>aus deinem Use-Case-Labor in diesem Browser</span></div>'
            '<div class="ft-liste" aria-live="polite"></div></div>')


def scoring_tool(web):
    if not web:
        rows = ''.join(f'<tr><td><b>{E(c[1])}</b></td><td>{c[2]} %</td><td></td><td></td><td></td></tr>' for c in KRITERIEN)
        return (''.join(f'<p class="steck-h">Kandidat {k}: ______________________________</p><div class="tab-wrap"><table class="tab ausfuell"><thead><tr><th>Kriterium</th><th>Gewicht</th><th>Punkte 1–5</th><th>gewichtet</th><th>Begründung in einem Satz</th></tr></thead><tbody>{rows}<tr><td colspan="3"><b>Summe</b></td><td></td><td></td></tr></tbody></table></div>' for k in (1, 2, 3)))
    gew = ''.join(f'<label class="fld"><span>{E(c[1])} in %</span><input type="number" min="0" max="100" value="{c[2]}" data-save="gw-{c[0]}" data-gw></label>' for c in KRITERIEN)
    cols = ''
    for k in (1, 2, 3):
        rows = ''
        for c in KRITERIEN:
            opts = '<option value="">–</option>' + ''.join(f'<option value="{i}">{i}</option>' for i in range(1, 6))
            rows += (f'<div class="bw-zeile"><label class="fld"><span>{E(c[1])}</span><select data-save="bw{k}-{c[0]}" data-bw="{k}" data-krit="{c[0]}">{opts}</select></label>'
                     f'<label class="fld bw-warum"><span>Warum diese Punktzahl?</span><input type="text" data-save="bw{k}-{c[0]}-warum" data-warum="{k}" placeholder="Ein Satz"></label></div>')
        cols += (f'<div class="bw-karte"><label class="fld"><span>Kandidat {k}</span><input type="text" data-save="bw{k}-name" data-bw-name="{k}"></label>{rows}'
                 f'<p class="bw-summe" data-bw-summe="{k}" aria-live="polite"></p></div>')
    return (f'<div class="tool" data-tool="scoring"><div class="tool-h"><b>Scoring-Rechner</b><span>rechnet gewichtet · speichert in diesem Browser</span></div>'
            f'<div class="gw-zeile">{gew}</div><p class="gw-summe" aria-live="polite"></p>'
            f'<div class="bw-raster">{cols}</div><p class="bw-stand" aria-live="polite"></p>'
            '<div class="btnrow"><button class="btn ghost" type="button" data-bw-beispiel>Beispiel laden</button></div></div>')


def matrix_tool(web):
    felder = [('sofort', 'Sofort starten', 'Hoher Wert · geringer Aufwand'), ('planen', 'Planen und in Etappen schneiden', 'Hoher Wert · hoher Aufwand'),
              ('nebenbei', 'Nebenbei, wenn Kapazität frei ist', 'Geringer Wert · geringer Aufwand'), ('streichen', 'Streichen', 'Geringer Wert · hoher Aufwand')]
    cells = ''.join(f'<div class="mx-feld mx-{key}" data-feld="{key}"><b>{E(t)}</b><small>{E(s)}</small><div class="mx-chips"></div></div>' for key, t, s in felder)
    if not web:
        return (f'<div class="mx">{cells}</div>'
                '<div class="tab-wrap"><table class="tab ausfuell"><thead><tr><th>Kandidat</th><th>Wert (Nutzen + Daten)</th><th>Aufwand (12 − Einfachheit − Risikoarmut)</th><th>Feld und Konsequenz</th></tr></thead>'
                '<tbody><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr></tbody></table></div>'
                '<p class="ausfuell-zeile">Mein Haupt-Use-Case: ______________________________________________</p>')
    return (f'<div class="tool" data-tool="matrix"><div class="tool-h"><b>Wert-Aufwand-Matrix</b><span>füllt sich aus deinem Scoring</span></div><div class="mx">{cells}</div>'
            '<div class="mx-tab" aria-live="polite"></div>'
            '<label class="fld"><span>Mein Haupt-Use-Case – mit diesem Fall wird ab jetzt gerechnet</span><select data-save="haupt" data-haupt><option value="">wählen …</option><option value="1">Kandidat 1</option><option value="2">Kandidat 2</option><option value="3">Kandidat 3</option></select></label></div>')


def _her(key):
    return ''.join([f'<select data-save="{key}-her" data-her aria-label="Woher stammt die Zahl?"><option value="">Woher?</option>'] + [f'<option value="{h}">{h}</option>' for h in HERKUNFT] + ['</select>'])


def bc_tool(web):
    if not web:
        zeile = lambda t: f'<tr><td>{E(t)}</td><td></td><td></td></tr>'
        kopf = '<thead><tr><th>Zeile</th><th>Mein Wert</th><th>Woher? gemessen / nachgeschlagen / geschätzt</th></tr></thead>'
        return (f'<div class="tab-wrap"><table class="tab ausfuell">{kopf}<tbody>' + ''.join(zeile(f'{t} ({u})') for _, t, u, _ in NUTZEN) + '</tbody></table></div>'
                f'<div class="tab-wrap"><table class="tab ausfuell">{kopf}<tbody>' + ''.join(zeile('Einmalig: ' + t) for _, t, _ in EINMALIG) + zeile('Summe einmalig') + '</tbody></table></div>'
                f'<div class="tab-wrap"><table class="tab ausfuell">{kopf}<tbody>' + ''.join(zeile('Laufend: ' + t) for _, t, _ in LAUFEND) + zeile('Summe laufend') + '</tbody></table></div>'
                '<p class="ausfuell-zeile">Ersparnis ______ Std/Monat · Bruttonutzen ________ € · Nettonutzen ________ € · Amortisation ______ Monate</p>')
    nutz = ''.join(f'<div class="bc-zeile"><label for="bc-{k}">{E(t)} <small>{E(u)}</small></label><input id="bc-{k}" type="number" min="0" step="any" data-save="bc-{k}" data-bc="{k}" data-bsp="{w}">{_her("bc-" + k)}</div>' for k, t, u, w in NUTZEN)
    ein = ''.join(f'<div class="bc-zeile"><label for="bc-{k}">{E(t)} <small>€</small></label><input id="bc-{k}" type="number" min="0" step="any" data-save="bc-{k}" data-ein="{k}" data-bsp="{w}">{_her("bc-" + k)}</div>' for k, t, w in EINMALIG)
    lauf = ''.join(f'<div class="bc-zeile"><label for="bc-{k}">{E(t)} <small>€/Monat</small></label><input id="bc-{k}" type="number" min="0" step="any" data-save="bc-{k}" data-lauf="{k}" data-bsp="{w}">{_her("bc-" + k)}</div>' for k, t, w in LAUFEND)
    return ('<div class="tool" data-tool="bc"><div class="tool-h"><b>Business-Case-Rechner</b><span>für deinen Haupt-Use-Case · speichert in diesem Browser</span></div>'
            '<p class="bc-haupt" data-bc-haupt></p>'
            f'<div class="bc-raster"><div><h4>Nutzenseite</h4>{nutz}</div><div><h4>Einmalige Kosten</h4>{ein}<h4>Laufende Kosten</h4>{lauf}</div></div>'
            '<label class="fld"><span>Qualitative Effekte – benennen, nicht rechnen</span><textarea rows="2" data-save="bc-qualitativ" placeholder="z. B. weniger Stress im Team, schnellere Antworten für die Kundschaft"></textarea></label>'
            '<div class="bc-aus" aria-live="polite"></div><ul class="bc-hinweise" aria-live="polite"></ul>'
            '<div class="btnrow"><button class="btn ghost" type="button" data-bc-beispiel>Beispiel Rechnungsfreigabe laden</button></div></div>')


def szenario_tool(web):
    if not web:
        rows = ''.join(f'<tr><td><b>{t}</b></td><td></td><td></td><td></td></tr>' for t in ('Automatisierbarer Anteil', 'Nettonutzen pro Monat', 'Amortisation in Monaten', 'ROI nach 12 Monaten'))
        return f'<div class="tab-wrap"><table class="tab ausfuell"><thead><tr><th></th><th>Konservativ</th><th>Basis</th><th>Ambitioniert</th></tr></thead><tbody>{rows}</tbody></table></div>'
    return ('<div class="tool" data-tool="szenario"><div class="tool-h"><b>Drei Szenarien</b><span>nutzt die Zahlen aus dem Business-Case-Rechner</span></div>'
            '<div class="sz-raster"><div class="sz sz-k"><h4>Konservativ</h4><label class="fld"><span>Automatisierbarer Anteil in %</span><input type="number" min="0" max="100" data-save="sz-k-anteil" data-sz="k-anteil"></label><label class="fld"><span>Laufende Kosten €/Monat</span><input type="number" min="0" data-save="sz-k-lauf" data-sz="k-lauf"></label><div class="sz-aus" data-sz-aus="k"></div><small>Das Szenario, das entscheidet.</small></div>'
            '<div class="sz sz-b"><h4>Basis</h4><p class="sz-info">Deine Rechnung von oben</p><div class="sz-aus" data-sz-aus="b"></div><small>Der Fall, den du vorträgst.</small></div>'
            '<div class="sz sz-a"><h4>Ambitioniert</h4><label class="fld"><span>Automatisierbarer Anteil in %</span><input type="number" min="0" max="100" data-save="sz-a-anteil" data-sz="a-anteil"></label><label class="fld"><span>Laufende Kosten €/Monat</span><input type="number" min="0" data-save="sz-a-lauf" data-sz="a-lauf"></label><div class="sz-aus" data-sz-aus="a"></div><small>Kein Plan, sondern eine Obergrenze.</small></div></div>'
            '<div class="btnrow"><button class="btn ghost" type="button" data-sz-vorschlag>Vorschlag eintragen (Anteil −20 / +15 Punkte, doppelte Wartung)</button></div>'
            '<div class="sz-kipp"><label class="fld"><span>Wann muss die Investition spätestens drin sein? (Monate)</span><input type="number" min="1" value="24" data-save="sz-ziel" data-sz-ziel></label><p data-sz-kipp aria-live="polite"></p></div></div>')


def entscheidung_tool(web):
    wahl = ['machen', 'kleiner zuschneiden und machen', 'verschieben', 'nicht machen']
    if not web:
        return ('<p class="ausfuell-zeile">Der Fall kippt, wenn: ______________________________________________________</p>'
                '<p class="ausfuell-zeile">Empfehlung (☐ machen ☐ kleiner zuschneiden und machen ☐ verschieben ☐ nicht machen):</p><p class="ausfuell-zeile">__________________________________________________________________</p><p class="ausfuell-zeile">__________________________________________________________________</p>'
                '<p class="ausfuell-zeile">Abbruchbedingung – Zahl: ____________ Zeitpunkt: ____________ Person: ____________ Was passiert dann: ____________</p>')
    opts = '<option value="">wählen …</option>' + ''.join(f'<option>{E(w)}</option>' for w in wahl)
    return (f'<div class="tool" data-tool="entscheidung"><div class="tool-h"><b>Empfehlung und Abbruchbedingung</b><span>speichert in diesem Browser</span></div>'
            '<label class="fld"><span>Der Fall kippt, wenn …</span><input type="text" data-save="ent-kipp" placeholder="z. B. der automatisierbare Anteil unter 38 % fällt"></label>'
            f'<label class="fld"><span>Meine Empfehlung</span><select data-save="ent-wahl" data-ent>{opts}</select></label>'
            '<label class="fld"><span>Begründung in zwei Sätzen</span><textarea rows="3" data-save="ent-text" data-ent></textarea></label>'
            '<div class="ab-raster"><label class="fld"><span>Abbruch: Zahl</span><input type="text" data-save="ab-zahl" data-ent placeholder="unter 50 % richtig eingeordnet"></label><label class="fld"><span>Zeitpunkt</span><input type="text" data-save="ab-zeit" data-ent placeholder="nach 3 Monaten"></label><label class="fld"><span>Person</span><input type="text" data-save="ab-person" data-ent placeholder="Leitung Innendienst"></label><label class="fld"><span>Was passiert dann?</span><input type="text" data-save="ab-dann" data-ent placeholder="Projekt stoppen, Ablauf neu prüfen"></label></div>'
            '<p class="ent-stand" aria-live="polite"></p><div class="btnrow"><button class="btn primary" type="button" data-w2-export>Meine Tagesarbeit herunterladen (.md)</button></div></div>')


def faustregel_tool(web):
    if not web:
        return ''
    return ('<div class="tool" data-tool="faustregel"><div class="tool-h"><b>Schnelltest</b><span>nichts wird gespeichert</span></div><div class="ab-raster">'
            '<label class="fld"><span>Volumen pro Monat</span><input type="number" min="0" value="400" data-fr="v"></label><label class="fld"><span>Eingesparte Minuten je Vorgang</span><input type="number" min="0" step="any" value="3" data-fr="m"></label></div><p class="fr-aus" aria-live="polite"></p></div>')


# ================================================================ Teile des Hefts

def teil_erinnerung(web):
    felder = ' · '.join(f[3] for f in STECKBRIEF_FELDER)
    k = kapitel('r1', 'R1', 'Erinnerung · Freitag, 30.10.', 'Das war Freitag: Use Cases finden',
        P('Bevor wir heute rechnen, holen wir kurz zurück, was am Freitag entstanden ist. Das brauchst du gleich alles wieder.') +
        freitag_tool(web) +
        H('Was ein Use-Case ist') +
        karten([('1', 'Echtes Problem', 'Etwas stört jemanden wirklich.'), ('2', 'Abgrenzbarer KI-Teil', 'Ein klar umrissenes Stück kann das System übernehmen.'), ('3', 'Messbarer Mehrwert', 'Man kann zeigen, dass es danach besser ist.')]) +
        P('Fehlt eines davon, ist es noch kein Use-Case, sondern ein Bauchgefühl, eine Prozessverbesserung oder Technik auf der Suche nach einem Problem.') +
        H('Was du am Freitag gemacht hast') +
        tab(['Schritt', 'Worum ging es', 'Merkregel'], [
            ['Zeitfresser', 'Wiederkehrende Arbeit aufschreiben und rechnen', 'Häufigkeit × Minuten – die nervigste Aufgabe ist selten die teuerste'],
            ['Schmerz-Interview', 'Vier Fragen, Antworten wörtlich notieren', 'Nicht fragen, was automatisiert werden soll, sondern was weh tut'],
            ['Steckbrief', f'Elf Felder: {felder}', 'Nutzen = Zahl + Einheit + Zeitraum. Offene Felder markieren statt raten'],
            ['Autonomie-Stufe', 'Stufe 0 manuell bis Stufe 4 autonom, je Pfad', 'Standardfall oft Stufe 3, Ausnahme Stufe 2'],
            ['Braucht es KI?', 'Erst Regel, dann KI an einer Stelle, Agent zuletzt', 'Das Sprachmodell liest – die Regel entscheidet'],
            ['Ausschlusskriterien', 'Datenzugriff, Verantwortliche Person, Rechtslage, richtiges Ergebnis, stabiler Ablauf', 'Wer hier durchfällt, wird nicht weiter geprüft']]) +
        H('Drei Fragen zum Warmwerden') +
        ''.join(f'<details class="verstehen"><summary><span class="lbl">Erinnerst du dich?</span> {md(q)}</summary><p>{md(a)}</p></details>' for q, a in [
            ('Warum reicht „spart Zeit“ im Steckbrief nicht?', 'Weil man es nicht prüfen kann. Es braucht eine Zahl, eine Einheit und einen Zeitraum, zum Beispiel „15 Stunden pro Monat im Innendienst“.'),
            ('Wann ist eine menschliche Freigabe nur scheinbar eine?', 'Wenn die Person keine Zeit oder Information zum Prüfen hat. Wer 200 Vorschläge am Tag durchklickt, ist faktisch Stufe 4.'),
            ('Was ist am Rechnungsbeispiel das Besondere?', 'Das Sprachmodell liest nur die vier Felder. Eine feste Regel entscheidet. Deshalb ist die Entscheidung erklärbar und leicht zu ändern.')]) +
        tipp('Keine Steckbriefe von Freitag?', 'Kein Problem. Nimm eines der drei fertigen Beispiele weiter hinten im Heft oder fülle deine Kandidaten im Use-Case-Labor des Tags 5 nach.') +
        '<p class="folien-ref">Freitagsfolien: <a href="/hefte/folien/tag-24/45.jpg" target="_blank" rel="noopener">Use-Case</a> · <a href="/hefte/folien/tag-24/51.jpg" target="_blank" rel="noopener">Steckbrief</a> · <a href="/hefte/folien/tag-24/53.jpg" target="_blank" rel="noopener">Autonomie</a> · <a href="/hefte/folien/tag-24/64.jpg" target="_blank" rel="noopener">Ausschluss</a></p>')
    return teil('teil-r', '←', 'Erinnerung an Freitag', 'Fünf Minuten zurückblicken, dann geht es mit deinen drei Kandidaten weiter.', k)


def teil_start():
    k = kapitel('s1', 'S1', 'Heute · Folien 1 und 3', 'Der Plan für heute: vier Schritte',
        flow([('1 · Bewerten', 'Drei Kandidaten bekommen Punkte'), ('2 · Priorisieren', 'Aus Punkten wird eine Reihenfolge'), ('3 · Rechnen', 'Der stärkste Fall wird durchgerechnet'), ('4 · Entscheiden', 'Du sprichst eine Empfehlung aus')]) +
        erkl('Heute beantwortest du zwei Fragen, die oft verwechselt werden: **Was kommt zuerst?** und **Lohnt es sich überhaupt?**',
             tab(['', 'Priorisierung', 'Wirtschaftlichkeit'], [
                 ['Frage', 'Welcher Kandidat hat das beste Verhältnis aus Nutzen, Datenlage, Aufwand und Risiko?', 'Übersteigt der Nutzen die Gesamtkosten über die Nutzungsdauer – und wann?'],
                 ['Werkzeug', 'Scoring (Punkte vergeben)', 'Business Case (Rechnung)'],
                 ['Ergebnis', 'Eine Reihenfolge', 'Ein Ja oder Nein']]),
             'Du vergleichst drei Autos und findest deinen Favoriten. Das ist die Reihenfolge. Ob du dir den Favoriten mit Versicherung, Sprit und Werkstatt überhaupt leisten kannst, ist die zweite Frage.',
             'Warum reicht eine sortierte Liste nicht?', 'Auch der beste Kandidat auf der Liste kann sich am Ende nicht lohnen. Das zeigt erst die Rechnung.') +
        fol(1, 3))
    return teil('teil-s', 'S', 'Der Plan für heute', 'Vom Kandidatenfeld zur begründeten Entscheidung.', k)


def teil_bewerten(web):
    k = []
    k.append(kapitel('b1', 'B1', 'Bewerten · Folien 2, 4, 5', 'Vier Kriterien – und was dahintersteckt',
        erkl('Jeder Kandidat wird an denselben vier Maßstäben gemessen. Nur so lassen sich Fälle aus ganz verschiedenen Bereichen vergleichen.',
             tab(['Kriterium', 'Bedeutet', 'Diese Fragen beantwortest du'], [
                 ['**Nutzen**', 'Wie viel Mehrwert entsteht – finanziell und qualitativ?', 'Volumen pro Monat · Zeit pro Vorgang · Fehlerkosten heute · Wird die Zeit nutzbar?'],
                 ['**Datenverfügbarkeit**', 'Sind die Daten in Menge und Qualität da?', 'Wo liegen die Daten? · Zugriff geklärt? · Format · Vollständigkeit · Personenbezug (lassen sich Daten einer Person zuordnen?)'],
                 ['**Komplexität und Aufwand**', 'Technik, Organisation, Personal, Zeit', 'Beteiligte Systeme · Entscheidungszweige · Sonderfälle · Abhängigkeit von Dritten'],
                 ['**Risiko**', 'Was kann rechtlich, organisatorisch oder qualitativ schiefgehen?', 'Schaden bei Fehler · Reversibilität (lässt sich der Fehler rückgängig machen?) · Rechtslage · Reputation (guter Ruf)']]),
             'Bei der Wohnungssuche fragst du bei jeder Wohnung dasselbe: Wie viel Platz? Wie weit zur Arbeit? Wie teuer? Wie laut? Erst dann kannst du vergleichen.',
             'Du weißt nicht, wo die Daten liegen. Welche Punktzahl gibst du bei Datenverfügbarkeit?', 'Eine niedrige, und du schreibst genau das als Begründung auf. Wer die Prüffrage nicht beantworten kann, hat die Antwort auch nicht in der Punktzahl.') +
        fol(2, 4, 5)))
    skala = tab(['Kriterium', '1 Punkt', '3 Punkte', '5 Punkte'], [[f'**{c[1]}**', c[3], c[4], c[5]] for c in KRITERIEN])
    k.append(kapitel('b2', 'B2', 'Bewerten · Folien 6, 7', 'Die wichtigste Regel: hoher Wert = gut',
        erkl('Alle vier Skalen zeigen in dieselbe Richtung. **5 Punkte sind immer gut für das Projekt.** Deshalb heißt es beim Bewerten nicht „Komplexität“ und „Risiko“, sondern **Einfachheit** und **Risikoarmut**.',
             skala + achtung('Der Fehler, den fast jede Gruppe macht', 'Wer „Risiko: 5“ als „sehr riskant“ einträgt und alles zusammenzählt, gibt dem riskantesten und aufwendigsten Fall die höchste Punktzahl.'),
             'Bei einem Hotelvergleich vergibst du Sterne. Fünf Sterne bei „Ruhe“ heißt: schön ruhig. Würdest du fünf Sterne für „Lärm“ vergeben, gewänne das lauteste Hotel.',
             'Ein Ablauf berührt acht Systeme und hat viele Sonderfälle. Wie viele Punkte bekommt er bei Einfachheit?', '1 Punkt. Viele Systeme und viele Sonderfälle bedeuten wenig Einfachheit.') +
        fol(6, 7)))
    k.append(kapitel('b3', 'B3', 'Bewerten · Folie 8', 'Gewichtung: Was zählt wie stark?',
        erkl('Nicht jedes Kriterium ist gleich wichtig. Die **Gewichtung** legt fest, wie stark es zählt. Zusammen sind es immer 100 %.',
             tab(['Kriterium', 'Vorschlag fürs Erstprojekt', 'Warum'], [
                 ['Nutzen', '40 %', 'Ohne Nutzen kein Projekt'], ['Datenverfügbarkeit', '25 %', 'Ohne Daten läuft nichts'],
                 ['Einfachheit', '20 %', 'Das erste Projekt soll fertig werden'], ['Risikoarmut', '15 %', 'Bei stark regulierten Abläufen höher setzen']]) +
             H('So rechnest du, Schritt für Schritt') +
             tab(['Kriterium', 'Punkte', 'Gewicht', 'Gewichteter Wert'], [
                 ['Nutzen', '4', '× 0,40', '1,60'], ['Datenverfügbarkeit', '4', '× 0,25', '1,00'], ['Einfachheit', '3', '× 0,20', '0,60'], ['Risikoarmut', '4', '× 0,15', '0,60'], ['**Summe**', '', '', '**3,80**']]) +
             merk('Das erste Projekt muss nicht das wertvollste sein, sondern das, das fertig wird.'),
             'Beim Autokauf zählt für die eine Person der Verbrauch doppelt, für die andere der Kofferraum. Eine eigene Gewichtung ist erlaubt – sie muss nur begründet sein.',
             'Warum liegt Nutzen vorn, wenn das erste Projekt doch vor allem fertig werden soll?', 'Weil auch ein kleines Projekt einen sichtbaren Nutzen braucht. Datenlage, Einfachheit und Risikoarmut zusammen wiegen aber mit 60 % schwerer und sorgen dafür, dass es fertig wird.') +
        fol(8)))
    k.append(kapitel('b4', 'B4', 'Bewerten · Folie 9', 'Vor dem Rechnen: der Filter',
        erkl('Manche Dinge lassen sich nicht wegrechnen. Trifft eines davon zu, wird der Kandidat **gar nicht erst bewertet**.',
             tab(['Ausschlusskriterium', 'Warum Schluss ist'], [
                 ['Kein Zugriff auf die Daten', 'Technisch oder rechtlich. Die halbe Lösung wäre dann Datenbeschaffung, und das ist ein eigenes Projekt.'],
                 ['Kein Verantwortlicher im Fachbereich', 'Nach der Übergabe bemerkt niemand mehr Auffälligkeiten.'],
                 ['Rechtlich unzulässiges Ziel', 'Kein Zuschnitt, keine Technik und kein Budget ändern daran etwas.'],
                 ['Kein definierbarer richtiger Output', 'Ohne Sollergebnis gibt es nichts zum Testen. Erst braucht es eine Entscheidungsregel.']]) +
             korrektur('Folie 9', 'Die Folie nennt vier Punkte, am Freitag waren es fünf. Der fünfte gilt weiterhin: Wird der Ablauf gerade umgestellt, erst den Zielablauf klären, dann automatisieren.'),
             'Wer keinen Führerschein hat, vergleicht keine Autos. Egal, wie gut das Angebot ist.',
             'Ist ein Ausschluss dasselbe wie eine schlechte Punktzahl?', 'Nein. Eine schlechte Punktzahl lässt sich vergleichen. Ein Ausschluss beendet die Prüfung.') +
        fol(9)))
    k.append(kapitel('b5', 'B5', 'Arbeitsauftrag 01 · Folie 10 · 45 Minuten allein', 'Deine drei Kandidaten bewerten',
        flow([('01', 'Gewichtung festlegen: 40 / 25 / 20 / 15 oder eine eigene, Summe 100 %.'), ('02', 'Die drei Kandidaten vom Freitag übernehmen.'),
              ('03', 'Je Kandidat alle vier Kriterien mit 1 bis 5 bewerten.'), ('04', 'Zu jeder Bewertung ein Begründungssatz. Eine Zahl ohne Satz zählt nicht.')], cls='steps') +
        scoring_tool(web) +
        merk('Fertig, wenn drei Gesamtsummen dastehen und jede der zwölf Bewertungen einen Satz hat.') + fol(10)))
    return teil('teil-b', '1', 'Bewerten', 'Aus Bauchgefühl wird eine begründete Punktzahl.', ''.join(k))


def teil_priorisieren(web):
    k = []
    k.append(kapitel('p1', 'P1', 'Priorisieren · Folien 11, 12', 'Die Wert-Aufwand-Matrix',
        erkl('Eine einzelne Punktzahl sagt noch nicht, was zu tun ist. Die Matrix teilt die Kandidaten in **vier Felder** auf, und jedes Feld hat eine klare Konsequenz.',
             tab(['Feld', 'Konsequenz'], [
                 ['**Hoher Wert · geringer Aufwand**', '**Sofort starten.** Hier liegt das Erstprojekt.'],
                 ['**Hoher Wert · hoher Aufwand**', '**Planen und in Etappen schneiden.** Nicht als Ganzes beauftragen.'],
                 ['**Geringer Wert · geringer Aufwand**', '**Nebenbei**, wenn Kapazität frei ist. Kein Projekt, kein Budget, kein Fahrplan.'],
                 ['**Geringer Wert · hoher Aufwand**', '**Streichen.** Das ist ein Ergebnis, kein Scheitern.']]) +
             H('So kommst du zu den zwei Zahlen') +
             tab(['Wert', 'Aufwand'], [['Nutzen + Datenverfügbarkeit', '12 − Einfachheit − Risikoarmut'], ['Beispiel: 4 + 4 = **8**', 'Beispiel: 12 − 3 − 4 = **5**']]) +
             korrektur('Folien 12 und 14', 'Die Folien schreiben „Aufwand = Komplexität + Risiko“, bewertet wird aber Einfachheit und Risikoarmut (hoher Wert = gut). Zählt man diese Punkte einfach zusammen, sieht der einfachste Fall wie der aufwendigste aus. Darum drehen wir sie um: 12 − Einfachheit − Risikoarmut. Die Folien legen außerdem keine Grenze fest. Unser Vorschlag: Wert ab 7 ist hoch, Aufwand bis 5 ist gering. Genau 6 ordnen wir vorsichtig ein.'),
             'Du planst den Samstag: Spülmaschine reparieren (viel Wert, wenig Aufwand) machst du sofort. Das Bad renovieren (viel Wert, viel Aufwand) planst du in Etappen. Fotos sortieren (wenig Wert, wenig Aufwand) nebenbei. Einen Teppich von Hand knüpfen (wenig Wert, viel Aufwand) streichst du.',
             'Warum ist „Streichen“ das wichtigste Feld?', 'Weil es Zeit und Geld für Vorhaben freimacht, die sich nicht lohnen. Es ist eine gute Entscheidung, keine Niederlage.') +
        fol(11, 12)))
    k.append(kapitel('p2', 'P2', 'Priorisieren · Folie 13', 'Die Reihenfolge der ersten drei Projekte',
        erkl('Nicht die höchste Punktzahl kommt zuerst. Jedes der ersten drei Projekte hat **eine eigene Aufgabe**.',
             karten([('1', 'Vertrauensaufbau', 'Klein, wenig Risiko, sichtbarer Nutzen. Zeigt allen: Es funktioniert.'), ('2', 'Substanz', 'Der wirtschaftlich stärkste Fall. Jetzt kann die Organisation ihn tragen.'),
                     ('3', 'Hebel', 'Nutzt dieselben Daten und Anbindungen. Der Aufwand sinkt, weil die Grundlage steht.')]) +
             merk('Diese Reihenfolge bringt nicht rechnerisch am meisten (wertmaximierend), sondern führt am sichersten zu fertigen Projekten (abschlussmaximierend).'),
             'Wer laufen lernt, startet nicht mit dem Marathon. Erst fünf Kilometer schaffen, dann die lange Strecke – und die Schuhe vom ersten Lauf hast du dann schon.',
             'Was passiert laut Folien-Notiz, wenn man mit dem größten Fall anfängt?', 'Nach sechs Monaten hat man noch nichts vorzuzeigen.') +
        fol(13)))
    k.append(kapitel('p3', 'P3', 'Arbeitsauftrag 02 · Folie 14 · 20 Minuten', 'Matrix und Haupt-Use-Case',
        flow([('01', 'Je Kandidat Wert und Aufwand bilden.'), ('02', 'Die drei Kandidaten in die Matrix eintragen.'), ('03', 'Feld ablesen und Konsequenz notieren.'), ('04', 'Einen Haupt-Use-Case festlegen. Mit diesem Fall wird ab jetzt gerechnet.')], cls='steps') +
        matrix_tool(web) +
        beispiel('Am Tisch', 'Zwei Minuten: Wer hat einen Fall im Feld „Streichen“? Das ist ein Ergebnis, kein Scheitern.') +
        merk('Fertig, wenn ein Haupt-Use-Case mit Namen feststeht.') + fol(14)))
    return teil('teil-p', '2', 'Priorisieren', 'Aus Punkten wird eine Reihenfolge und ein Haupt-Use-Case.', ''.join(k))


def teil_rechnen(web):
    f = FOLIE19
    k = []
    k.append(kapitel('c0', 'C1', 'Rechnen · Folien 15, 16', 'Drei Kennzahlen, drei Fragen',
        erkl('Ein **Business Case** ist die Rechnung, ob sich ein Vorhaben lohnt. Drei Zahlen reichen, jede beantwortet eine andere Frage.',
             H('Zuerst drei Wörter') +
             tab(['Wort', 'Bedeutet', 'Beispiel'], [
                 ['**Investition**', 'Was du einmalig zahlst, bevor es losgeht', '12.000 €'],
                 ['**Bruttonutzen**', 'Was der Fall jeden Monat einbringt', '1.485 € / Monat'],
                 ['**Nettonutzen**', 'Bruttonutzen minus laufende Kosten', '1.485 € − 300 € = 1.185 € / Monat']]) +
             H('Die drei Kennzahlen') +
             tab(['Kennzahl', 'Frage', 'Formel', 'Beispiel'], [
                 ['**ROI** (Return on Investment)', 'Wie viel kommt zurück?', '(Nettonutzen × Monate − Investition) ÷ Investition', '12 Monate: 18,5 % · 36 Monate: rund 256 %'],
                 ['**Amortisation**', 'Ab wann ist das Geld wieder drin?', 'Investition ÷ Nettonutzen pro Monat', '12.000 € ÷ 1.185 € = rund 10 Monate'],
                 ['**TCO** (Total Cost of Ownership)', 'Was kostet es insgesamt?', 'Investition + laufende Kosten × Nutzungsdauer (meist 36 Monate)', '12.000 € + 300 € × 36 = 22.800 €']]) +
             achtung('Immer netto rechnen', 'Ohne laufende Kosten wirkt alles besser. Mit dem Bruttonutzen käme die Amortisation auf 8 statt 10 Monate. Im Betrieb trägt der Fall dann nicht. Und einen ROI nie ohne Zeitraum nennen.'),
             'Eine Kaffeemaschine fürs Büro kostet 1.200 €. Sie erspart 150 € gekauften Kaffee im Monat, Bohnen und Wartung kosten 30 €. Netto bleiben 120 €. Nach 10 Monaten ist sie bezahlt (Amortisation). Nach einem Jahr hast du 20 % mehr zurück als investiert (ROI). Über drei Jahre kostet sie insgesamt 2.280 € (TCO).',
             'Jemand sagt: „Der ROI liegt bei 256 %!“ Was fragst du?', 'Über welchen Zeitraum? Im Beispiel gilt das erst nach 36 Monaten, nach 12 Monaten sind es 18,5 %.') +
        fol(15, 16)))
    k.append(kapitel('c2', 'C2', 'Rechnen · Folien 17, 18', 'Kosten, die gern vergessen werden',
        erkl('Die einmaligen Kosten fallen allen ein. **Vergessen wird meist die rechte Spalte – und die läuft jeden Monat weiter.**',
             tab(['Einmalig', 'Laufend'], [
                 ['Analyse und Prozessaufnahme', 'Plattform und Lizenzen'], ['Aufbau des Workflows', 'Nutzung der KI-Modelle'], ['Datenaufbereitung', 'Monitoring und Betrieb (laufende Überwachung)'],
                 ['Integration in bestehende Systeme', 'Wartung und Anpassung'], ['Test und Abnahme', 'Verbleibende menschliche Prüfung'], ['Schulung und Einführung', 'Dokumentation und Audits (geordnete Prüfungen)'],
                 ['Dokumentation, ggf. Datenschutz-Folgenabschätzung', '']]) +
             H('Drei Erfahrungswerte zum Gegenprüfen') +
             karten([('15–25 %', 'des Budgets für Datenaufbereitung', 'Der Posten, der in Angeboten am häufigsten fehlt.'), ('8–16 h', 'Schulung je Person', 'Ohne diese Stunden bleibt das System stehen, obwohl es läuft.'), ('20–30 %', 'Puffer auf die Schätzung', 'Die Regel, nicht die Ausnahme.')]) +
             merk('Wer unter sechs Monaten Amortisation rechnet, hat meist etwas vergessen.') +
             P('Diese Werte stammen aus der Projektpraxis. Sie sind Richtwerte, keine gemessenen Kennzahlen.'),
             'Beim Auto denkt jeder an den Kaufpreis. Versicherung, Steuer, Reifen und Werkstatt kommen trotzdem, jedes Jahr wieder.',
             'Dein Fall amortisiert sich laut Rechnung in vier Monaten. Was tust du?', 'Misstrauisch werden und die Kostenliste noch einmal durchgehen. Meist fehlen laufende Kosten, Datenaufbereitung oder Schulung.') +
        fol(17, 18)))
    k.append(kapitel('c3', 'C3', 'Rechnen · Folie 19', 'Das Beispiel Zeile für Zeile',
        erkl('Die Rechnung ist eine Kette. Jede Zeile baut auf der vorherigen auf. Das Beispiel ist die Rechnungsfreigabe vom Freitag.',
             tab(['Schritt', 'Rechnung', 'Ergebnis'], [
                 ['Wie viele Vorgänge übernimmt das System?', '800 × 70 %', '560 im Monat'],
                 ['Wie viel Zeit spart einer davon?', '4 Min. − 0,5 Min. Restprüfung', '3,5 Min.'],
                 ['Ersparnis im Monat', '560 × 3,5 Min. ÷ 60', f'rund {f["h"]} Std.'],
                 ['**Bruttonutzen**', f'{f["h"]} Std. × 45 €', f'**{de(f["brutto"])} €**'],
                 ['**Nettonutzen**', f'{de(f["brutto"])} € − 300 €', f'**{de(f["netto"])} €**'],
                 ['**Amortisation**', f'12.000 € ÷ {de(f["netto"])} €', '**rund 10 Monate**']]) +
             P('Genau sind es 32,7 Stunden und 10,1 Monate, die Folie rundet. Vermiedene Fehlerkosten sind hier nicht eingerechnet. Alle Werte sind Beispielwerte.') +
             korrektur('Folien 17 und 19', '„Verbleibende menschliche Prüfung“ steht auf Folie 17 bei den laufenden Kosten, im Rechenbeispiel ist die Restprüfzeit aber schon beim Nutzen abgezogen. Nicht doppelt zählen: Im Rechner steht deshalb bei den laufenden Kosten nur zusätzliche Prüfung, die nicht schon in der Restzeit steckt.'),
             frage='Warum zählen nur 560 und nicht alle 800 Vorgänge?', antwort='Nur 70 % lassen sich automatisieren. Die übrigen 30 % bearbeitet weiterhin ein Mensch, dort entfällt keine Zeit.') +
        fol(19)))
    k.append(kapitel('c4', 'C4', 'Rechnen · Folie 20', 'Nur zählen, was zählbar wird',
        erkl('Es gibt drei Arten von Nutzen. **Nur zwei dürfen in die Rechnung.**',
             tab(['Art', 'Bedeutet', 'In den ROI?'], [
                 ['**Harte Einsparung**', 'Zeit, die wirklich entfällt – nicht Zeit, die nur anders verbracht wird', 'Ja'],
                 ['**Vermiedene Kosten**', 'Fehler, Nacharbeit, verlorenes Skonto (Preisnachlass für schnelles Zahlen), belegbar aus dem Ist-Zustand', 'Ja'],
                 ['**Qualitative Effekte**', 'Zufriedenheit, Entlastung, Außenwirkung', 'Nein: benennen, nicht rechnen']]) +
             achtung('Verteilte Zeit täuscht', 'Zwei Minuten täglich bei 200 Personen sind rechnerisch 130 Stunden im Monat – und praktisch fast nie nutzbar, weil die Zeit nie am Stück anfällt. Gebündelte Zeit bei wenigen Personen ist mehr wert.'),
             'Wenn du jeden Tag zwei Minuten früher mit dem Zähneputzen fertig bist, hast du am Monatsende nicht eine Stunde frei. Fällt dagegen ein wöchentlicher Termin weg, gewinnst du wirklich Zeit.',
             'Das Team ist dank Automation entspannter. Rechnest du das in den ROI ein?', 'Nein. Es ist wichtig und gehört in die Entscheidung, aber in ein eigenes Feld.') +
        fol(20)))
    k.append(kapitel('c5', 'C5', 'Arbeitsauftrag 03 · Folie 21 · 60 Minuten', 'Deinen Business Case rechnen',
        flow([('01', 'Nutzenseite füllen: Volumen, Zeit, Anteil, Restaufwand, Stundensatz, Fehlerkosten.'), ('02', 'Kostenseite füllen: einmalig und laufend, Zeile für Zeile.'),
              ('03', 'Bei jeder Zahl angeben, woher sie stammt: gemessen, nachgeschlagen oder geschätzt.'), ('04', 'Summen und Nettonutzen bilden.')], cls='steps') +
        bc_tool(web) +
        merk('Fertig, wenn keine Zeile ohne Herkunftsangabe dasteht und Bruttonutzen, Kostensummen und Nettonutzen berechnet sind.') + fol(21)))
    k.append(kapitel('c6', 'C6', 'Rechnen · Folien 22, 23', 'Drei Szenarien und eine Faustregel',
        erkl('Eine einzige Zahl täuscht Sicherheit vor. Deshalb rechnest du den Fall **dreimal**, mit vorsichtigen, geplanten und optimistischen Annahmen.',
             tab(['Szenario', 'Annahmen', 'Rolle'], [
                 ['**Konservativ**', 'Weniger automatisierbar, doppelter Wartungsaufwand', '**Das Szenario, das entscheidet.**'],
                 ['**Basis**', 'Die geplanten Annahmen', 'Der Fall, den du vorträgst'],
                 ['**Ambitioniert**', 'Mehr automatisierbar, sinkende Modellkosten', 'Kein Plan, sondern eine Obergrenze']]) +
             merk('Die Frage lautet nicht „Rechnet es sich?“, sondern „Tragen wir auch das konservative Szenario?“') +
             H('Die Faustregel: Lohnt sich das Rechnen überhaupt?') +
             P('**Volumen pro Monat × eingesparte Minuten je Vorgang ≥ 10–15 Stunden im Monat.** Beispiele: 400 × 3 Min. = 20 Std. (trägt sich), 40 × 10 Min. = 6,7 Std. (trägt sich nicht).') +
             faustregel_tool(web) +
             P('Darunter kann ein Projekt trotzdem richtig sein, etwa wegen Qualität, Risiko oder Compliance (Einhaltung von Regeln). Dann muss genau das im Business Case stehen, keine erfundene Wirtschaftlichkeit.') +
             korrektur('Folie 23', 'Die Folie sagt, ab 10–15 Stunden amortisiere sich ein typisches Vorhaben in unter zwei Jahren. Das gilt nur bei kleinem Zuschnitt. Mit den Kosten aus dem Beispiel (12.000 € + 300 €/Monat) und 45 € Stundensatz wären es bei 15 Stunden rund 32 Monate. Die Faustregel ist ein Schnelltest, keine Rechnung.'),
             'Vor dem Urlaub planst du mit gutem Wetter, rechnest aber das Budget so, dass es auch bei Regen und teurem Mietwagen reicht.',
             'Der Fall trägt nur im ambitionierten Szenario. Was heißt das?', 'Er ist kein sicherer Kandidat. Entweder kleiner zuschneiden, verschieben oder nicht machen.') +
        fol(22, 23)))
    k.append(kapitel('c7', 'C7', 'Arbeitsauftrag 04, Teil 1 · Folie 28', 'Deine Szenarien',
        szenario_tool(web) + fol(28)))
    return teil('teil-c', '3', 'Rechnen', 'Der Business Case für deinen Haupt-Use-Case.', ''.join(k))


def teil_entscheiden(web):
    k = []
    k.append(kapitel('d1', 'D1', 'Entscheiden · Folien 24, 25, 26', 'Was trägt – und was scheitert',
        erkl('Am Ende geht es um eine Empfehlung. Dabei helfen die Erfahrungen aus vielen Projekten.',
             H('Acht Gewohnheiten, die den Unterschied machen') +
             tab(['', ''], [['01 Mit vorhandenen Daten starten', '05 Den Ist-Zustand messen, bevor du etwas änderst'], ['02 In kleinen Schritten denken', '06 In den Arbeitsablauf einbauen, nicht daneben'],
                            ['03 Klare Ergebnisse festlegen', '07 Die Ausnahme planen, bevor der Standardfall gebaut wird'], ['04 Abläufe verstehen, bevor Technik einzieht', '08 Eine Abbruchbedingung setzen']]) +
             H('Zehn Stolpersteine') +
             tab(['Im Projekt', 'Nach dem Projekt – die teureren'], [
                 ['Zu große Use-Cases', '**Der Pilot wird nie produktiv:** Testzugänge und manueller Start sind kein Betrieb'],
                 ['Unklare Ziele', '**Niemand ist zuständig, wenn es klemmt:** Der Ablauf stoppt still, und keiner merkt es'],
                 ['Fehlende Daten', '**Erfolg wird an Aktivität gemessen:** „Zwölf Automatisierungen“ ist keine Kennzahl'],
                 ['Keine Erfolgskriterien', '**Recht wird am Ende geprüft:** Nachträglich einbauen ist ein Neubau'],
                 ['Ergebnis nicht überprüfbar', '**Abhängigkeit von einer Person:** Das Risiko ist nicht kleiner, nur verlagert']]),
             'Eine neue Küche ist schnell eingebaut. Ärgerlich wird es danach, wenn niemand weiß, wer für die Geräte zuständig ist oder die Anleitung nur eine Person kennt.',
             'Was ist an „zwölf Automatisierungen“ falsch?', 'Es zählt Aktivität, nicht Wirkung. Besser: gesparte Stunden, weniger Fehler, kürzere Durchlaufzeit.') +
        fol(24, 25, 26)))
    k.append(kapitel('d2', 'D2', 'Arbeitsauftrag 04, Teil 2 · Folien 27, 28 · 25 Minuten', 'Empfehlung und Abbruchbedingung',
        merk('„Nicht machen“ ist ein Arbeitsergebnis, kein Scheitern.') +
        erkl('Der Tag endet nicht mit einer Rechnung, sondern mit einer **Empfehlung in zwei Sätzen** und einer **Abbruchbedingung**. Sie legt vorher fest, woran du merkst, dass es nicht funktioniert.',
             tab(['Teil', 'Beispiel'], [
                 ['Der Punkt, an dem der Fall kippt (Break-even)', 'Fällt der automatisierbare Anteil unter 38 %, dauert die Amortisation länger als 24 Monate.'],
                 ['Empfehlung', 'Machen. Der Fall trägt auch im konservativen Szenario, die Investition ist nach rund 19 Monaten drin.'],
                 ['Abbruchbedingung', 'Sind nach 3 Monaten weniger als 50 % der Rechnungen automatisch richtig vorbereitet, stoppt die Leitung Buchhaltung das Projekt und lässt den Ablauf neu prüfen.']]),
             frage='Was fehlt an „Wenn es nicht gut läuft, schauen wir nochmal“?', antwort='Eine Zahl, ein Zeitpunkt und eine Person. Ohne die läuft ein schlechtes Projekt einfach weiter.') +
        entscheidung_tool(web) +
        beispiel('Im Plenum', 'Jede Person nennt ihre Empfehlung in zwei Sätzen. Keine Diskussion, nur Vortrag.') +
        fol(27, 28)))
    k.append(kapitel('d3', 'D3', 'Abschluss · Folie 29', 'Was jetzt entschieden ist',
        P('Aus drei Kandidaten ist eine begründete Reihenfolge geworden, aus einer Ahnung eine Rechnung. Du hast jetzt:') +
        tab(['Ergebnis', 'Schritt'], [['Eigene Gewichtung, Summe 100 %', 'Bewerten'], ['Drei Scoring-Bögen mit Begründung je Zeile', 'Bewerten'], ['Matrix und benannter Haupt-Use-Case', 'Priorisieren'],
                                      ['Business Case mit Herkunftsangabe je Zahl', 'Rechnen'], ['Drei Szenarien, Break-even, Empfehlung, Abbruchbedingung', 'Entscheiden']]) +
        P('**Im nächsten Block** wird der Ablauf auseinandergenommen, auf dem die Rechnung beruht. Dort zeigt sich, ob die angenommenen Zeiten und Mengen wirklich so anfallen.') +
        tipp('Bis dahin', 'Besprich deine Empfehlung mit der Person, die den Fall später verantwortet. Wer widerspricht, zeigt dir die Annahme, die noch nicht belastbar ist.') + fol(29)))
    return teil('teil-d', '4', 'Entscheiden', 'Vom Ergebnis zur Empfehlung – „nicht machen“ ist erlaubt.', ''.join(k))


BEISPIELE = {
    'ingo': ('Ingo · Druck & Vertrieb', 'Druckanfragen vorsortieren', (180, 8, 70, 1, 38, 120, 4800), [('Druckanfragen vorsortieren', 4, 4, 3, 4), ('Angebote automatisch versenden', 5, 2, 2, 1), ('Monatsbericht formatieren', 2, 3, 5, 5)]),
    'carmen': ('Carmen · Team & Website', 'Website-Anfragen vorsortieren', (120, 8, 70, 1, 42, 90, 3600), [('Website-Anfragen vorsortieren', 4, 4, 3, 4), ('Bewerbungen automatisch vorfiltern', 4, 3, 2, 1), ('Team-Protokolle formatieren', 2, 3, 5, 5)]),
    'tabea': ('Tabea · Video & Design', 'Feedbackrunden bündeln', (60, 12, 80, 2, 40, 60, 3200), [('Feedbackrunden bündeln', 4, 3, 3, 4), ('Rohschnitt automatisch erstellen', 4, 2, 1, 2), ('Dateien einheitlich benennen', 2, 4, 5, 5)])}
FELD = lambda wert, aufw: ('Sofort starten' if aufw <= 5 else 'Planen, in Etappen') if wert >= 7 else ('Nebenbei' if aufw <= 5 else 'Streichen')


def teil_mitnehmen(pid, web):
    order = [pid] + [x for x in BEISPIELE if x != pid] if pid in BEISPIELE else list(BEISPIELE)
    out = ''
    for p in order:
        label, haupt, a, kand = BEISPIELE[p]
        r = bc(*a)
        rows = [[n, de(a1 * .4 + b1 * .25 + c1 * .2 + d1 * .15, 2), str(a1 + b1), str(12 - c1 - d1), FELD(a1 + b1, 12 - c1 - d1)] for n, a1, b1, c1, d1 in kand]
        out += (f'<div class="steck-bsp{" mein" if p == pid else ""}"><p class="steck-h">{E(label)}{" · dein Bereich" if p == pid else ""}</p>' +
                tab(['Kandidat', 'Punktzahl', 'Wert', 'Aufwand', 'Feld'], rows, cls='steck-tab') +
                P(f'**Haupt-Use-Case: {haupt}.** {a[0]} Vorgänge × {a[2]} % × {de(a[1] - a[3])} Min. ≈ {r["h"]} Std./Monat. Bruttonutzen {de(r["brutto"])} €, laufend {de(a[5])} €, Nettonutzen {de(r["netto"])} €. '
                  f'Investition {de(a[6])} €: Amortisation rund {de(r["amort"])} Monate, ROI nach 12 Monaten {de(r["roi12"], 1)} %, nach 36 Monaten {de(r["roi36"], 1)} %, TCO {de(r["tco"])} €.') + '</div>')
    v = ''.join(vorlage(a, web, MATERIAL) for a in AUTOMATIONS)
    k = kapitel('m1', 'M1', 'Alle Zahlen erfunden', 'Drei fertige Beispiele zum Abgucken', out +
                tipp('Fällt dir etwas auf?', 'Tabeas Fall ist nach 12 Monaten noch leicht im Minus und nach 36 Monaten klar im Plus. Genau deshalb nennt man einen ROI nie ohne Zeitraum. Mit 8 Stunden liegt er außerdem unter der Faustregel und braucht weitere Gründe wie weniger übersehenes Feedback.'))
    s = kapitel('m2', 'M2', 'Der Tag auf einer Seite', 'Spickzettel',
                '<div class="spick">' + ''.join(f'<div class="spick-box"><h4>{E(t)}</h4><ul>' + ''.join(f'<li>{md(x)}</li>' for x in items) + '</ul></div>' for t, items in [
                    ('Zwei Fragen', ['Scoring: Was kommt zuerst?', 'Business Case: Lohnt es sich?']),
                    ('Bewerten', ['Nutzen, Daten, Einfachheit, Risikoarmut', 'Hoher Wert = gut', '40 / 25 / 20 / 15', 'Keine Zahl ohne Satz']),
                    ('Matrix', ['Wert = Nutzen + Daten', 'Aufwand = 12 − Einfachheit − Risikoarmut', 'Sofort · Planen · Nebenbei · Streichen']),
                    ('Rechnen', ['Netto = Brutto − laufend', 'ROI = (Netto × Monate − Invest) ÷ Invest', 'Amortisation = Invest ÷ Netto', 'TCO = Invest + laufend × 36']),
                    ('Ehrlich bleiben', ['Jede Zahl: gemessen, nachgeschlagen, geschätzt', 'Qualitatives benennen, nicht rechnen', 'Unter 6 Monaten: etwas vergessen?']),
                    ('Entscheiden', ['Das konservative Szenario entscheidet', 'Abbruch: Zahl, Zeitpunkt, Person', '„Nicht machen“ ist erlaubt'])]) + '</div>')
    w = kapitel('m3', 'M3', 'Alle Fachwörter des Tages', 'Wörterliste', glossar([(a, b, '') for a, b in BEGRIFFE]))
    q = kapitel('m4', 'M4', 'Stand 02.11.2026', 'Prüfstand und Grenzen',
                P('Alle Rechnungen der Folien wurden nachgerechnet und stimmen. Die Präzisierungen stehen bei den jeweiligen Kapiteln. Das Arbeitsheft 2, auf das die Folien verweisen, lag uns nicht vor: Rechner und Ausfülltabellen folgen den Angaben der Folien. '
                  'Die Make-Vorlagen sind mit Makes eigener Prüfung abgeglichen, aber nicht in euren Konten ausgeführt. Alle Beispiele und Zahlen sind erfunden. Prozentwerte und Erfahrungswerte sind Angaben der Folien.'))
    return teil('teil-m', '↓', 'Mitnehmen', 'Beispiele, Make-Vorlagen, Spickzettel und Wörter.', k + vorlagen_kapitel(web) + v + s + w + q)


def vorlagen_kapitel(web):
    knopf = f'<p><a class="btn primary" href="{MATERIAL}/{ZIP}" download>Beide Vorlagen als ZIP</a></p>' if web else ''
    return kapitel('m0', 'M0', 'Make-Vorlagen · Import wie am Freitag', 'Bewerten und rechnen in Make',
                   P('Zwei fertige Vorlagen machen die Rechnungen von heute in Make sichtbar. Beide laufen mit Make Free und ohne fremdes Konto.') +
                   flow([('1 · Herunterladen', 'JSON-Datei speichern.'), ('2 · Neues Szenario', 'In Make: Scenarios → + Create a new scenario.'),
                         ('3 · Importieren', 'Drei Punkte oben rechts → Import blueprint → Datei wählen → Save.'), ('4 · Starten', 'Speichern, dann Run once. Das Ergebnis steht in der Sprechblase über dem letzten Modul.')], cls='steps') + knopf)


TOC = [('teil-r', '← Erinnerung an Freitag', [('r1', 'Das war Freitag')]),
       ('teil-s', 'Der Plan für heute', [('s1', 'Vier Schritte, zwei Fragen')]),
       ('teil-b', '1 · Bewerten', [('b1', 'Vier Kriterien'), ('b2', 'Hoher Wert = gut'), ('b3', 'Gewichtung'), ('b4', 'Der Filter'), ('b5', 'Auftrag 01: Scoring')]),
       ('teil-p', '2 · Priorisieren', [('p1', 'Wert-Aufwand-Matrix'), ('p2', 'Reihenfolge'), ('p3', 'Auftrag 02: Haupt-Use-Case')]),
       ('teil-c', '3 · Rechnen', [('c0', 'Drei Kennzahlen'), ('c2', 'Vergessene Kosten'), ('c3', 'Beispiel Zeile für Zeile'), ('c4', 'Was zählt'), ('c5', 'Auftrag 03: Business Case'), ('c6', 'Szenarien, Faustregel'), ('c7', 'Auftrag 04: Szenarien')]),
       ('teil-d', '4 · Entscheiden', [('d1', 'Was trägt, was scheitert'), ('d2', 'Empfehlung, Abbruch'), ('d3', 'Was jetzt feststeht')]),
       ('teil-m', 'Mitnehmen', [('m1', 'Drei Beispiele'), ('m0', 'Make-Vorlagen'), ('m2', 'Spickzettel'), ('m3', 'Wörter'), ('m4', 'Grenzen')])]

ABDECKUNG = {1: 's1', 2: 'b1', 3: 's1', 4: 'b1', 5: 'b1', 6: 'b2', 7: 'b2', 8: 'b3', 9: 'b4', 10: 'b5', 11: 'p1', 12: 'p1', 13: 'p2', 14: 'p3', 15: 'c0', 16: 'c0', 17: 'c2', 18: 'c2',
             19: 'c3', 20: 'c4', 21: 'c5', 22: 'c6', 23: 'c6', 24: 'd1', 25: 'd1', 26: 'd1', 27: 'd2', 28: 'd2', 29: 'd3'}
assert sorted(ABDECKUNG) == list(range(1, 30))


def body(pid, web=True):
    return teil_erinnerung(web) + teil_start() + teil_bewerten(web) + teil_priorisieren(web) + teil_rechnen(web) + teil_entscheiden(web) + teil_mitnehmen(pid, web)
