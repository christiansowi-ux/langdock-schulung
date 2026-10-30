"""Lernkarten, Selbsttest und Wörter für die Tage ohne eigene Modul-1-Daten (Tag 19, Modul 2 Tag 1–5).

Regel seit 30.10.2026: Jeder Kurstag ist ein Learning Hub mit allen Funktionen (siehe LERNKONZEPT.md).
Die Wochenlisten aus modul2/woche1/daten.py werden auf die Make-Tage verteilt; Tag 24 behält nur
den Use-Case-Anteil als Daten (der Hub zeigt trotzdem die ganze Woche), damit das Training keine
Karte doppelt anbietet.
"""
from modul2.woche1 import daten as W
from modul2.tag1.series import QUIZZES

KARTEN_TAG = [1] * 14 + [2] * 5 + [3] * 5 + [4] * 4 + [5] * 12
TEST_TAG = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5]
BEGRIFFE_TAG = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 3, 3, 3, 5, 5, 5, 5, 5, 5]
assert len(KARTEN_TAG) == len(W.KARTEN) and len(TEST_TAG) == len(W.TEST) and len(BEGRIFFE_TAG) == len(W.BEGRIFFE)

TAG19_KARTEN = [
    ('Was macht einen Design-Auftrag besser als ein „Zaubersatz“?', 'Gutes Material: Zielgruppe, Anlass, bestätigte Inhalte und gewünschtes Format.'),
    ('Was ist ein Designsystem?', 'Gemeinsame Regeln für Farben, Schriften, Abstände und Bausteine – wie ein Rezeptbuch für Wiedererkennung.'),
    ('Wie wird aus „mach es schöner“ eine klare Änderung?', 'Konkret sagen, was sich wo wie ändern soll, z. B. „Überschrift größer, Abstand darüber halbieren“.'),
    ('Wofür eignet sich Google Stitch besonders?', 'Für Entwürfe von Oberflächen, also Websites und Apps.'),
    ('Was zählt mehr als der Name des Werkzeugs?', 'Der Ablauf: erst die Aufgabe klären, dann ein passendes Werkzeug wählen, dann das Ergebnis prüfen.'),
    ('Was ist ein Szenario in Make?', 'Der ganze zusammenhängende Ablauf von Auslöser bis Ergebnis.'),
    ('Was ist ein Modul in Make?', 'Ein einzelner Baustein mit einer bestimmten Aufgabe im Szenario.'),
    ('Was ist ein Auslöser?', 'Das Ereignis, das den Ablauf startet – wie eine Türklingel.'),
    ('Was heißt Mapping?', 'Die richtige Angabe ins richtige Feld des nächsten Schritts setzen.'),
    ('Was ist eine Verbindung in Make?', 'Eine erteilte Erlaubnis, damit Make mit einer anderen Anwendung arbeiten darf.'),
    ('Durchlauf oder Zeitplan – was ist der Unterschied?', 'Ein Durchlauf verarbeitet die Eingaben einmal. Ein Zeitplan legt fest, wann immer wieder gestartet wird.'),
]
TAG19_TEST = [
    dict(frage='Was verbessert einen Design-Auftrag am stärksten?',
         optionen=['Ein besonders langer Zaubersatz', 'Gutes Material: Zielgruppe, Anlass, Inhalte, Format', 'Eine möglichst kurze Bitte'], richtig=1,
         warum='Das Werkzeug kann nur gestalten, was es weiß. Bestätigte Inhalte und ein klarer Zweck wirken mehr als Formulierungstricks.'),
    dict(frage='Was ist ein Designsystem?', optionen=['Gemeinsame Regeln für das Aussehen', 'Ein bestimmtes Grafikprogramm', 'Ein Druckformat'], richtig=0,
         warum='Farben, Schriften, Abstände und Bausteine werden einmal festgelegt und dann wiederverwendet.'),
    dict(frage='Welcher Wunsch ist eine klare Änderung?', optionen=['„Mach es schöner“', '„Überschrift größer und Abstand darüber halbieren“', '„Mehr Wow“'], richtig=1,
         warum='Nur eine konkrete Änderung lässt sich umsetzen und hinterher prüfen.'),
    dict(frage='In Make ist ein Szenario …', optionen=['ein einzelner Schritt', 'der ganze festgelegte Ablauf', 'eine Verbindung zu einem Konto'], richtig=1,
         warum='Module sind die einzelnen Schritte, das Szenario ist der ganze Ablauf.'),
    dict(frage='Was setzt einen Ablauf in Gang?', optionen=['Mapping', 'Ein Auslöser', 'Ein Modul ohne Eingang'], richtig=1,
         warum='Ein Auslöser (Trigger) ist das Ereignis, das den Ablauf startet.'),
]


def _aus_learnings(t):
    """Karten aus den Learnings eines Tages: Satz als Frage, Erklärung als Antwort."""
    out = []
    for l in t['learnings']:
        e = (l.get('erklaert') or '').strip()
        if len(e) > 60 and not e.endswith(':'):
            out.append((f'Erkläre in eigenen Worten: {l["satz"]}', e))
    return out


def ergaenzen(TAGE):
    t19 = TAGE[19]
    t19['karten'] = TAG19_KARTEN + _aus_learnings(t19)[:6]
    t19['test'] = TAG19_TEST
    t19['hub_tag'] = True
    for day in (1, 2, 3, 4):
        t = TAGE[19 + day]
        t['karten'] = [k for k, d in zip(W.KARTEN, KARTEN_TAG) if d == day] + _aus_learnings(t)[:8]
        t['test'] = [dict(frage=q, optionen=list(o), richtig=r, warum=w) for q, o, r, w in QUIZZES[day]] + \
                    [dict(frage=q, optionen=o, richtig=r, warum=w) for (q, o, r, w), d in zip(W.TEST, TEST_TAG) if d == day]
        t['begriffe'] = [b for b, d in zip(W.BEGRIFFE, BEGRIFFE_TAG) if d == day]
        t['hub_tag'] = True
    t24 = TAGE[24]
    t24['karten'] = [k for k, d in zip(W.KARTEN, KARTEN_TAG) if d == 5]
    t24['test'] = [dict(frage=q, optionen=o, richtig=r, warum=w) for (q, o, r, w), d in zip(W.TEST, TEST_TAG) if d == 5]
    t24['begriffe'] = [b for b, d in zip(W.BEGRIFFE, BEGRIFFE_TAG) if d == 5]
