"""Zwei leichte Make-Vorlagen für Modul 2 · Tag 6: Scoring und Business Case.

Bausteine und Prüfung wie in woche1/blueprints.py. Keine fremden Konten, kein Versand, kein Zeitplan.
Zahlen werden mit * 1 zu Zahlen gemacht, bevor sie addiert werden (Set multiple variables liefert Text).
"""
from ..woche1.blueprints import set_vars, compose, router, filt, cond, blueprint, check

MATERIAL = '/hefte/material/modul2-woche2'
ZIP = 'Make-Vorlagen-Tag6.zip'

GEWICHTET = 'round((1.nutzen * 0.4 + 1.daten * 0.25 + 1.einfachheit * 0.2 + 1.risikoarmut * 0.15) * 100) / 100'
WERT = '1.nutzen * 1 + 1.daten * 1'
AUFWAND = '12 - 1.einfachheit - 1.risikoarmut'
TEXT = 'Kandidat: {{1.kandidat}}\nGewichtete Punktzahl: {{' + GEWICHTET + '}}\nWert: {{' + WERT + '}} · Aufwand: {{' + AUFWAND + '}}\n'

STUNDEN = 'round(1.volumen * 1.anteil / 100 * (1.minuten - 1.restminuten) / 60)'

AUTOMATIONS = [
 dict(
  nr=10, slug='A10_Scoring-Rechner', tag=6, level=2, minuten=15, credits=2,
  titel='Scoring-Rechner mit Matrix',
  kurz='Vier Punktzahlen rein, gewichtete Punktzahl und Matrix-Feld raus.',
  lernt='Gewichtet rechnen, Skala umdrehen und mit einem Router das richtige Feld wählen.',
  flow=lambda: [
   set_vars(1, 0, 0, '1 · Kandidat bewerten', [('kandidat', 'Druckanfragen vorsortieren'), ('nutzen', '4'), ('daten', '4'), ('einfachheit', '3'), ('risikoarmut', '4')]),
   router(2, 300, 0, '2 · Welches Feld?', [
    [compose(3, 600, -220, '3a · Sofort starten', TEXT + 'Feld: SOFORT STARTEN. Hier liegt das Erstprojekt.',
             filt('Viel Wert, wenig Aufwand', [cond('{{' + WERT + '}}', 'number:greaterorequal', '7'), cond('{{' + AUFWAND + '}}', 'number:less', '6')]))],
    [compose(4, 600, -70, '3b · Planen', TEXT + 'Feld: PLANEN und in Etappen schneiden.',
             filt('Viel Wert, viel Aufwand', [cond('{{' + WERT + '}}', 'number:greaterorequal', '7'), cond('{{' + AUFWAND + '}}', 'number:greaterorequal', '6')]))],
    [compose(5, 600, 80, '3c · Nebenbei', TEXT + 'Feld: NEBENBEI, wenn Kapazität frei ist.',
             filt('Wenig Wert, wenig Aufwand', [cond('{{' + WERT + '}}', 'number:less', '7'), cond('{{' + AUFWAND + '}}', 'number:less', '6')]))],
    [compose(6, 600, 230, '3d · Streichen', TEXT + 'Feld: STREICHEN. Das ist ein Ergebnis, kein Scheitern.',
             filt('Wenig Wert, viel Aufwand', [cond('{{' + WERT + '}}', 'number:less', '7'), cond('{{' + AUFWAND + '}}', 'number:greaterorequal', '6')]))]])],
  module=[
   ('Tools › Set multiple variables', '1 · Kandidat bewerten',
    [('kandidat', 'Druckanfragen vorsortieren', 'Der Name deines Kandidaten.'), ('nutzen, daten', '4 und 4', 'Punkte von 1 bis 5. Nur die Zahl.'),
     ('einfachheit, risikoarmut', '3 und 4', 'Auch hier gilt: hoher Wert = gut.')]),
   ('Flow Control › Router', '2 · Welches Feld?',
    [('Vier Wege', 'je ein Filter mit zwei Bedingungen', 'Wert ab 7 ist hoch, Aufwand unter 6 ist gering. Immer läuft genau ein Weg.')]),
   ('Filter auf jedem Weg', 'z. B. Viel Wert, wenig Aufwand',
    [('Wert', 'nutzen + daten', 'Wie in der Matrix auf Folie 12.'), ('Aufwand', '12 − einfachheit − risikoarmut', 'Die Skala wird umgedreht: hohe Punkte bei Einfachheit bedeuten wenig Aufwand.')]),
   ('Tools › Compose a string (4×)', '3a bis 3d',
    [('Text', 'Kandidat, Punktzahl, Wert, Aufwand, Feld', 'Die Punktzahl rechnet 40 / 25 / 20 / 15 und rundet auf zwei Stellen.')])],
  soll='Kandidat: Druckanfragen vorsortieren\nGewichtete Punktzahl: 3.8\nWert: 8 · Aufwand: 5\nFeld: SOFORT STARTEN. Hier liegt das Erstprojekt.',
  soll_wo='Nur Baustein 3a bekommt eine Sprechblase. Make schreibt Dezimalzahlen mit Punkt',
  aendern=('Einen schwierigen Fall testen: nutzen 2, daten 2, einfachheit 2, risikoarmut 2.', 'Punktzahl 2 · Wert 4 · Aufwand 8 · Feld: STREICHEN.'),
  fehler=[('Kein Weg läuft', 'Eine Punktzahl enthält ein Wort oder fehlt. Nur die Zahlen 1 bis 5 eintragen.'),
          ('Die Punktzahl wirkt zu hoch', 'Prüfen, ob du bei Einfachheit und Risikoarmut wirklich „hoher Wert = gut“ bewertet hast.')]),
 dict(
  nr=11, slug='A11_Business-Case-Rechner', tag=6, level=2, minuten=15, credits=3,
  titel='Business-Case-Rechner',
  kurz='Die Kette von Folie 19 in Make: vom Volumen bis zu Amortisation, ROI und TCO.',
  lernt='Eine Rechenkette in Schritte teilen und Ergebnisse weiterverwenden.',
  flow=lambda: [
   set_vars(1, 0, 0, '1 · Annahmen eintragen', [('volumen', '800'), ('minuten', '4'), ('anteil', '70'), ('restminuten', '0.5'), ('stundensatz', '45'), ('laufend', '300'), ('investition', '12000')]),
   set_vars(2, 300, 0, '2 · Nutzen rechnen', [('stunden', '{{' + STUNDEN + '}}'), ('brutto', '{{' + STUNDEN + ' * 1.stundensatz}}'), ('netto', '{{' + STUNDEN + ' * 1.stundensatz - 1.laufend}}')]),
   compose(3, 600, 0, '3 · Ergebnis ausgeben',
           'Ersparnis: {{2.stunden}} Std. pro Monat\nBruttonutzen: {{2.brutto}} €\nNettonutzen: {{2.netto}} €\n'
           'Amortisation: rund {{round(1.investition / 2.netto)}} Monate\n'
           'ROI nach 12 Monaten: {{round((2.netto * 12 - 1.investition) / 1.investition * 1000) / 10}} %\n'
           'ROI nach 36 Monaten: {{round((2.netto * 36 - 1.investition) / 1.investition * 1000) / 10}} %\n'
           'TCO über 3 Jahre: {{1.investition * 1 + 1.laufend * 36}} €')],
  module=[
   ('Tools › Set multiple variables', '1 · Annahmen eintragen',
    [('volumen, minuten', '800 und 4', 'Vorgänge im Monat und Minuten je Vorgang heute.'), ('anteil, restminuten', '70 und 0.5', 'Prozent automatisierbar und Restzeit je Vorgang. Dezimalzahlen mit Punkt schreiben.'),
     ('stundensatz, laufend, investition', '45, 300 und 12000', 'Euro. Nur die Zahl, ohne €-Zeichen.')]),
   ('Tools › Set multiple variables', '2 · Nutzen rechnen',
    [('stunden', 'volumen × anteil ÷ 100 × eingesparte Minuten ÷ 60', 'Auf ganze Stunden gerundet, wie auf Folie 19.'), ('brutto, netto', 'stunden × stundensatz, dann minus laufend', 'Immer netto rechnen.')]),
   ('Tools › Compose a string', '3 · Ergebnis ausgeben',
    [('Text', 'Amortisation, ROI 12 und 36 Monate, TCO', 'Die Formeln von Folie 16. Der ROI wird auf eine Nachkommastelle gerundet.')])],
  soll='Ersparnis: 33 Std. pro Monat\nBruttonutzen: 1485 €\nNettonutzen: 1185 €\nAmortisation: rund 10 Monate\nROI nach 12 Monaten: 18.5 %\nROI nach 36 Monaten: 255.5 %\nTCO über 3 Jahre: 22800 €',
  soll_wo='Sprechblase über Baustein 3. Die Folie rundet 255,5 % auf rund 256 %',
  aendern=('Das konservative Szenario testen: anteil 50 und laufend 400.', 'Ersparnis 23 Std. · Nettonutzen 635 € · Amortisation rund 19 Monate · ROI nach 12 Monaten −36.5 %.'),
  fehler=[('Fehler oder leeres Ergebnis', 'Ein Wert enthält ein Komma oder €-Zeichen. 0.5 mit Punkt schreiben, Euro ohne Zeichen.'),
          ('Amortisation wirkt falsch', 'Ist der Nettonutzen null oder negativ, amortisiert sich der Fall nie. Dann sind die Annahmen oder der Fall das Problem.')]),
]


def build_all():
    files = {}
    for a in AUTOMATIONS:
        bp = blueprint(f'M2 · A{a["nr"]} {a["titel"]}', a['flow']())
        check(bp)
        files[f'M2-{a["slug"]}.blueprint.json'] = bp
    return files
