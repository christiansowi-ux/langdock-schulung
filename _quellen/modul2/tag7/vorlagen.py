"""Drei leichte Make-Vorlagen für Modul 2 · Tag 7: Zielsatz-Prüfer, Durchlaufzeit-Detektiv, Scope-Tür.

Bausteine und Prüfung wie in woche1/blueprints.py. Keine fremden Konten, kein Versand, kein Zeitplan.
Zahlen werden mit * 1 zu Zahlen gemacht, bevor sie addiert werden (Set multiple variables liefert Text).
Fehlende Bausteine heißen „offen“, weil leere Felder in Filtern schwer zu erklären sind.
"""
from ..woche1.blueprints import set_vars, compose, router, filt, cond, blueprint, check

MATERIAL = '/hefte/material/modul2-tag7'
ZIP = 'Make-Vorlagen-Tag7.zip'

BAUSTEINE = [('anteil', 'Anteil oder Menge'), ('fallmenge', 'Fallmenge'), ('handlung', 'Handlung'), ('kennzahl', 'Kennzahl'), ('zeitpunkt', 'Zeitpunkt')]
FEHLT = ''.join('{{if(1.' + k + ' = "offen"; "[' + t + '] "; "")}}' for k, t in BAUSTEINE)

WARTEN = '1.warte1 * 1 + 1.warte2 * 1 + 1.warte3 * 1 + 1.warte4 * 1'
ERGEBNIS = ('Bearbeitungszeit: {{1.minuten}} Minuten\nDurchlaufzeit: {{2.tage}} Tage\n'
            'Auf 1 Minute Arbeit kommen {{2.verhaeltnis}} Minuten Warten.\nGrößte Übergabe: {{2.groesste}} Tage\n')
GRUND = ('{{if(1.betrag * 1 >= 1000; "[ab 1.000 Euro] "; "")}}{{if(1.sonderprojekt = "ja"; "[Sonderprojekt] "; "")}}'
         '{{if(1.klaerungsvermerk = "ja"; "[Klärungsvermerk] "; "")}}{{if(1.bestellbezug = "nein"; "[kein Bestellbezug] "; "")}}')

AUTOMATIONS = [
 dict(
  nr=12, slug='A12_Zielsatz-Pruefer', tag=7, level=2, minuten=15, credits=2,
  titel='Zielsatz-Prüfer',
  kurz='Fünf Bausteine rein. Raus kommt ein fertiger Zielsatz, oder die freundliche Auskunft, was noch fehlt.',
  lernt='Mit einem Router zwei Wege bauen und mit if() genau die fehlenden Teile nennen.',
  flow=lambda: [
   set_vars(1, 0, 0, '1 · Fünf Bausteine', [('anteil', '70 Prozent'), ('fallmenge', 'der Rechnungen unter 1.000 Euro ohne Klärungsbedarf'), ('handlung', 'werden ohne manuelle Prüfung freigegeben'),
                                            ('kennzahl', 'gemessen an der Freigabequote im Monatsbericht'), ('zeitpunkt', 'offen')]),
   router(2, 300, 0, '2 · Alles da?', [
    [compose(3, 600, -120, '3a · Das ist ein Ziel', 'ZIEL: {{1.anteil}} {{1.fallmenge}} {{1.handlung}}, {{1.kennzahl}}, {{1.zeitpunkt}}.',
             filt('Alle fünf Bausteine sind da', [cond('{{1.' + k + '}}', 'text:notequal', 'offen') for k, _ in BAUSTEINE]))],
    [compose(4, 600, 120, '3b · Das ist ein Wunsch', 'WUNSCH: Noch kein prüfbares Ziel.\nEs fehlt: ' + FEHLT + '\nFehlt ein Baustein, kann in sechs Monaten niemand mehr prüfen, ob es funktioniert hat.',
             filt('Mindestens ein Baustein ist offen', *[[cond('{{1.' + k + '}}', 'text:equal', 'offen')] for k, _ in BAUSTEINE]))]])],
  module=[
   ('Tools › Set multiple variables', '1 · Fünf Bausteine',
    [('anteil, fallmenge', '70 Prozent · der Rechnungen unter …', 'Wie viel, und von welchen Fällen? Wie auf Folie 10.'), ('handlung, kennzahl', 'werden … freigegeben · gemessen an …', 'Was passiert, und woran erkennst du es?'),
     ('zeitpunkt', 'offen', 'Absichtlich noch offen. Trage „offen“ ein, solange ein Baustein fehlt.')]),
   ('Flow Control › Router', '2 · Alles da?',
    [('Zwei Wege', 'je ein Filter', 'Es läuft immer genau einer der beiden Wege.')]),
   ('Filter auf den Wegen', 'Alles da / etwas offen',
    [('Oben', 'alle fünf ungleich „offen“', 'Mehrere Bedingungen in einer Gruppe heißen UND.'), ('Unten', 'einer gleich „offen“', 'Fünf Gruppen mit je einer Bedingung heißen ODER.')]),
   ('Tools › Compose a string (2×)', '3a und 3b',
    [('Text oben', 'der fertige Satz', 'Setzt die fünf Bausteine zusammen.'), ('Text unten', 'if(… = "offen"; "[…] "; "")', 'Schreibt nur die Bausteine hin, die fehlen.')])],
  soll='WUNSCH: Noch kein prüfbares Ziel.\nEs fehlt: [Zeitpunkt] \nFehlt ein Baustein, kann in sechs Monaten niemand mehr prüfen, ob es funktioniert hat.',
  soll_wo='Nur Baustein 3b bekommt eine Sprechblase. Dort steht dein Ergebnis unter OUTPUT',
  aendern=('Trage bei zeitpunkt ein: ab drei Monaten nach Start. Dann noch einmal Run once.', 'Jetzt läuft der obere Weg: ZIEL: 70 Prozent der Rechnungen unter 1.000 Euro ohne Klärungsbedarf werden ohne manuelle Prüfung freigegeben, gemessen an der Freigabequote im Monatsbericht, ab drei Monaten nach Start.'),
  fehler=[('Es läuft der falsche Weg', 'Prüfe die Schreibweise: Das Wort muss genau offen heißen, klein und ohne Leerzeichen.'),
          ('Nichts bekommt eine Sprechblase', 'Hast du Run once geklickt und vorher gespeichert? Ein Feld ganz leer zu lassen statt „offen“ zu schreiben, kann ebenfalls verwirren.')]),
 dict(
  nr=13, slug='A13_Durchlaufzeit-Detektiv', tag=7, level=2, minuten=15, credits=3,
  titel='Durchlaufzeit-Detektiv',
  kurz='Der Fall der verschwundenen Tage in Make: Bearbeitungszeit und vier Übergaben rein, Durchlaufzeit, Verhältnis und Befund raus.',
  lernt='Zwischenergebnisse in einem zweiten Baustein rechnen und den Befund per Router wählen.',
  flow=lambda: [
   set_vars(1, 0, 0, '1 · Die Spuren', [('minuten', '12'), ('warte1', '1.5'), ('warte2', '2'), ('warte3', '0.5'), ('warte4', '1'), ('stunden_pro_tag', '8')]),
   set_vars(2, 300, 0, '2 · Rechnen', [('tage', '{{' + WARTEN + '}}'), ('verhaeltnis', '{{round((' + WARTEN + ') * 1.stunden_pro_tag * 60 / 1.minuten)}}'),
                                       ('groesste', '{{max(1.warte1 * 1; 1.warte2 * 1; 1.warte3 * 1; 1.warte4 * 1)}}')]),
   router(3, 600, 0, '3 · Welcher Befund?', [
    [compose(4, 900, -120, '4a · Wartezeit-Alarm', ERGEBNIS + 'Befund: Hier wird vor allem gewartet. Prüfe zuerst die Übergaben, nicht die Arbeit.',
             filt('Mindestens 1 zu 50', [cond('{{2.verhaeltnis}}', 'number:greaterorequal', '50')]))],
    [compose(5, 900, 120, '4b · Unauffällig', ERGEBNIS + 'Befund: Arbeit und Warten liegen nah beieinander. Schau dir hier die Arbeitsschritte an.',
             filt('Unter 1 zu 50', [cond('{{2.verhaeltnis}}', 'number:less', '50')]))]])],
  module=[
   ('Tools › Set multiple variables', '1 · Die Spuren',
    [('minuten', '12', 'Bearbeitungszeit gesamt von Folie 22.'), ('warte1 bis warte4', '1.5 · 2 · 0.5 · 1', 'Wartezeit an den vier Übergaben in Tagen. Dezimalzahlen mit Punkt schreiben.'),
     ('stunden_pro_tag', '8', 'Unsere Annahme: ein Arbeitstag hat acht Stunden.')]),
   ('Tools › Set multiple variables', '2 · Rechnen',
    [('tage', 'warte1 + warte2 + warte3 + warte4', 'Die Durchlaufzeit. Die 12 Minuten fallen dabei kaum ins Gewicht.'), ('verhaeltnis', 'Wartezeit in Minuten ÷ Arbeitsminuten', 'Auf 1 Minute Arbeit kommen so viele Minuten Warten.'),
     ('groesste', 'max(warte1; warte2; warte3; warte4)', 'Hier hängt der größte Anteil.')]),
   ('Flow Control › Router', '3 · Welcher Befund?',
    [('Zwei Wege', 'ab 50 oder darunter', 'Die Folien-Notiz nennt 1 zu 50 oder schlechter als häufigen Fall. Die Grenze ist unser Vorschlag.')]),
   ('Tools › Compose a string (2×)', '4a und 4b',
    [('Text', 'Ergebnis und Befund', 'Beide Wege geben dieselben Zahlen aus, aber einen anderen Befund.')])],
  soll='Bearbeitungszeit: 12 Minuten\nDurchlaufzeit: 5 Tage\nAuf 1 Minute Arbeit kommen 200 Minuten Warten.\nGrößte Übergabe: 2 Tage\nBefund: Hier wird vor allem gewartet. Prüfe zuerst die Übergaben, nicht die Arbeit.',
  soll_wo='Nur Baustein 4a bekommt eine Sprechblase',
  aendern=('Automatisiere zuerst die Arbeit: minuten auf 2. Danach stattdessen wieder minuten 12 und die größte Übergabe streichen: warte2 auf 0.', 'Mit 2 Minuten bleibt die Durchlaufzeit bei 5 Tagen. Ohne die Übergabe sind es nur noch 3 Tage. Genau das ist die Aussage von Folie 22.'),
  fehler=[('Fehler beim Rechnen', 'Ein Wert enthält ein Komma. 1.5 mit Punkt schreiben, nicht 1,5.'),
          ('Das Verhältnis ist riesig', 'Das stimmt vermutlich. Trage testweise weniger Wartezeit ein und schau, ab wann der Befund wechselt.')]),
 dict(
  nr=14, slug='A14_Scope-Tuer', tag=7, level=2, minuten=15, credits=2,
  titel='Die Scope-Tür',
  kurz='Die Scope-Regeln von Folie 12 als Tür: Eine Rechnung klopft an, und Make sagt rein oder raus, samt Grund.',
  lernt='Eine Scope-Liste in Filter übersetzen. So wird aus Text eine Regel, die man testen kann.',
  flow=lambda: [
   set_vars(1, 0, 0, '1 · Wer klopft an?', [('rechnung', 'Kaffeebohnen'), ('betrag', '86'), ('sonderprojekt', 'nein'), ('klaerungsvermerk', 'nein'), ('bestellbezug', 'nein')]),
   router(2, 300, 0, '2 · An der Tür', [
    [compose(3, 600, -120, '3a · Rein', 'REIN: {{1.rechnung}} ({{1.betrag}} Euro) gehört zum Scope. Die Automatisierung darf ran.',
             filt('Alle Regeln erfüllt', [cond('{{1.betrag}}', 'number:less', '1000'), cond('{{1.sonderprojekt}}', 'text:equal', 'nein'), cond('{{1.klaerungsvermerk}}', 'text:equal', 'nein'), cond('{{1.bestellbezug}}', 'text:equal', 'ja')]))],
    [compose(4, 600, 120, '3b · Raus', 'RAUS: {{1.rechnung}} ({{1.betrag}} Euro) bleibt beim Menschen.\nGrund: ' + GRUND,
             filt('Mindestens eine Regel verletzt', [cond('{{1.betrag}}', 'number:greaterorequal', '1000')], [cond('{{1.sonderprojekt}}', 'text:equal', 'ja')], [cond('{{1.klaerungsvermerk}}', 'text:equal', 'ja')], [cond('{{1.bestellbezug}}', 'text:equal', 'nein')]))]])],
  module=[
   ('Tools › Set multiple variables', '1 · Wer klopft an?',
    [('rechnung, betrag', 'Kaffeebohnen · 86', 'Eine erfundene Rechnung. Nur die Zahl, ohne Euro-Zeichen.'), ('sonderprojekt, klaerungsvermerk', 'nein · nein', 'Nur ja oder nein schreiben, klein.'), ('bestellbezug', 'nein', 'Auch Kaffee braucht einen Bestellbezug.')]),
   ('Flow Control › Router', '2 · An der Tür',
    [('Zwei Wege', 'Rein oder Raus', 'Die In-Scope-Regeln stehen im oberen Filter, die Out-of-Scope-Regeln im unteren.')]),
   ('Filter auf den Wegen', 'Alle Regeln / eine verletzt',
    [('Oben', 'vier Bedingungen in einer Gruppe', 'Alle müssen stimmen (UND).'), ('Unten', 'vier Gruppen', 'Eine verletzte Regel reicht (ODER).')]),
   ('Tools › Compose a string (2×)', '3a und 3b',
    [('Text unten', 'if(… ; "[Grund] "; "")', 'Nennt genau die Regeln, die nicht erfüllt sind.')])],
  soll='RAUS: Kaffeebohnen (86 Euro) bleibt beim Menschen.\nGrund: [kein Bestellbezug] ',
  soll_wo='Nur Baustein 3b bekommt eine Sprechblase',
  aendern=('Setze bestellbezug auf ja. Danach teste: betrag 1000.', 'Mit Bestellbezug: REIN. Mit genau 1000 Euro: RAUS mit dem Grund [ab 1.000 Euro]. Die Folie sagt nur „unter“ und „über“ 1.000 Euro. In einer echten Regel musst du diese Lücke entscheiden, und hier ist sie entschieden.'),
  fehler=[('Kein Weg läuft', 'Bei sonderprojekt, klaerungsvermerk und bestellbezug muss genau ja oder nein stehen. „Nein“ mit großem N oder ein Leerzeichen passt nicht auf die Regeln.'),
          ('Es erscheint kein Grund', 'Der Betrag enthält vielleicht einen Punkt oder ein Euro-Zeichen. 1480 schreiben, nicht 1.480 €.')]),
]


def build_all():
    files = {}
    for a in AUTOMATIONS:
        bp = blueprint(f'M2 · A{a["nr"]} {a["titel"]}', a['flow']())
        check(bp)
        files[f'M2-{a["slug"]}.blueprint.json'] = bp
    return files
