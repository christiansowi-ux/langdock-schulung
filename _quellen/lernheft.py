"""Lernhefte (nur lesen und merken) - ab Tag 4.

    python lernheft.py [--tag 4|5] [--preview [dpi]]   -> "../Tag N - .../Lernheft_TagN_....pdf" (+ Seitencheck, Vorschau build/preview/LH_*.png)
    plattform.py ruft web_page(pid, tag) fuer /<person>/tag-N/lernheft/ auf.
"""
import base64
import html as H
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kurs  # noqa: E402

BUILD = os.path.join(HERE, 'build')
BASE = '/hefte'

_S = '<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICONS = {
    'chat': _S + '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>',
    'search': _S + '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.6-4.6"/></svg>',
    'pen': _S + '<path d="M15 4l5 5-9.5 9.5H5.5v-5z"/><path d="M4 21h16"/></svg>',
    'window': _S + '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 13h10M7 16h7"/></svg>',
    'cpu': _S + '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/><path d="M10 14l1-4h2l1 4M10.5 12.5h3"/></svg>',
    'check': _S + '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.6L16 9.5"/></svg>',
    'book': _S + '<path d="M2 5h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H2z"/><path d="M22 5h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z"/></svg>',
    'layers': _S + '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/></svg>',
    'star': _S + '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg>',
    'slides': _S + '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M12 16v4M8 20h8"/></svg>',
    'brain': _S + '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 3 3h1V4z"/><path d="M15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-3 3h-1V4z"/></svg>',
    'file': _S + '<path d="M14 3H6v18h12V7z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></svg>',
    'globe': _S + '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/></svg>',
    'plug': _S + '<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0z"/><path d="M12 18v4"/></svg>',
    'arrow': _S + '<path d="M4 12h15M13 6l6 6-6 6"/></svg>',
    'alert': _S + '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/></svg>',
    'briefcase': _S + '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V4h6v3M3 13h18"/></svg>',
    'megaphone': _S + '<path d="M3 10v4h4l8 5V5L7 10z"/><path d="M19 9a4 4 0 0 1 0 6"/></svg>',
    'target': _S + '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/></svg>',
    'clock': _S + '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    'lock': _S + '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>',
    'report': _S + '<path d="M6 3h9l4 4v14H6z"/><path d="M9 12h7M9 15h7M9 18h4M15 3v4h4"/></svg>',
    'flask': _S + '<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/><path d="M7.5 14h9"/></svg>',
}

HEFTE = {
    4: {'src': 'tag4/lernheft.html', 'out': 'Tag 4 - RAG', 'pdf': 'Lernheft_Tag4_RAG.pdf', 'kurz': 'RAG',
        'label': 'Lernheft &nbsp;·&nbsp; RAG – erst suchen, dann antworten',
        'titles': {1: 'Woher kennt die KI die Antwort?', 2: 'Überzeugend heißt nicht richtig', 3: 'Ein Dokument macht es präzise',
                   4: 'RAG: erst suchen, dann antworten', 5: 'Chunks und Embeddings', 6: 'Suche nach Bedeutung',
                   7: 'Die Wissensbasis entscheidet', 8: 'Unser Fall – gerettet', 9: 'Prüfen wie ein Team',
                   10: 'Wo RAG hilft – und wo nicht', 11: 'RAG zum Anfassen', 12: 'Die Lektion auf einer Seite',
                   13: 'Zwölf Merkfragen', 14: 'Die Wörter des Tages'}},
    5: {'src': 'tag5/lernheft.html', 'out': 'Tag 5 - Deep Research', 'pdf': 'Lernheft_Tag5_Deep-Research.pdf', 'kurz': 'Deep Research',
        'label': 'Lernheft &nbsp;·&nbsp; Deep Research – Recherche, die eine Entscheidung trägt',
        'titles': {1: 'Was ist Deep Research?', 2: 'So läuft Deep Research in Langdock', 3: 'Erst die Entscheidung, dann die Suche',
                   4: 'Der Bauplan: sechs Abschnitte', 5: 'Zweck und Ausgangslage', 6: 'Der Untersuchungsrahmen',
                   7: 'Belege und Regeln', 8: 'Das Vorgehen', 9: 'Die Ergebnisform', 10: 'Der ganze Auftrag auf einen Blick',
                   11: 'Grenzen – und was man prüft', 12: 'Üben im Prompt-Labor', 13: 'Die Lektion auf einer Seite',
                   14: 'Zwölf Merkfragen', 15: 'Die Wörter des Tages'}},
    6: {'src': 'tag6/lernheft.html', 'out': 'Tag 6 - Prompt Engineering', 'pdf': 'Lernheft_Tag6_Prompt-Engineering-1.pdf',
        'kurz': 'Prompt Engineering', 'uebungen': (11, 12),
        'label': 'Lernheft &nbsp;·&nbsp; Prompt Engineering – gute Prompts schreiben',
        'titles': {1: 'Was ist ein Prompt?', 2: 'Warum Prompts so wichtig sind', 3: 'Die zehn Fehler (1–5)',
                   4: 'Die zehn Fehler (6–10)', 5: 'Schnell: das RTF-Framework', 6: 'Wichtig: die vier Elemente',
                   7: 'Unser Fall – gerettet', 8: 'Einen Prompt verbessern', 9: 'Die Prompt-Bibliothek in Langdock',
                   10: 'Die Lektion auf einer Seite', 11: 'Üben in Langdock (1)', 12: 'Üben in Langdock (2)',
                   13: 'Zwölf Merkfragen', 14: 'Die Wörter des Tages'}},
    7: {'src': 'tag7/lernheft.html', 'out': 'Tag 7 - Prompting-Techniken', 'pdf': 'Lernheft_Tag7_Prompt-Engineering-2.pdf',
        'kurz': 'Prompting-Techniken', 'uebungen': (13, 14),
        'label': 'Lernheft &nbsp;·&nbsp; Prompting-Techniken – von Few-Shot bis zum Agenten',
        'titles': {1: 'Welche Technik wann?', 2: 'Zero-Shot: ohne Beispiel', 3: 'One-Shot und Few-Shot',
                   4: 'Chain-of-Thought: Schritt für Schritt', 5: 'Tree-of-Thought: mehrere Wege', 6: 'ReAct: denken, handeln, beobachten',
                   7: 'Self-Refine und Self-Consistency', 8: 'System-Prompts', 9: 'Markdown im Prompt',
                   10: 'XML und JSON', 11: 'Vom Prompt zum Agenten', 12: 'Die Lektion auf einer Seite',
                   13: 'Üben in Langdock (1)', 14: 'Üben in Langdock (2)', 15: 'Zwölf Merkfragen', 16: 'Die Wörter des Tages'}},
    8: {'src': 'tag8/lernheft.html', 'out': 'Tag 8 - Skills', 'pdf': 'Lernheft_Tag8_Skills.pdf',
        'kurz': 'Skills', 'uebungen': (13, 14),
        'label': 'Lernheft &nbsp;·&nbsp; Skills – einmal erklären, immer anwenden',
        'titles': {1: 'Vom Prompt zum Skill', 2: 'Was ist ein Skill?', 3: 'So arbeitet ein Skill in Langdock',
                   4: 'Prompt, Skill oder Agent?', 5: 'Drei Wege zum eigenen Skill', 6: 'Die Beschreibung entscheidet',
                   7: 'Wo es Skills gibt', 8: 'Niemals ungeprüft übernehmen', 9: 'Ein Skill, eine Aufgabe',
                   10: 'Unser Fall: der Protokoll-Skill', 11: 'Integrationen und Ideen', 12: 'Die Lektion auf einer Seite',
                   13: 'Üben in Langdock (1)', 14: 'Üben in Langdock (2)', 15: 'Zwölf Merkfragen', 16: 'Die Wörter des Tages'}},
    9: {'src': 'tag9/lernheft.html', 'out': 'Tag 9 - Agenten', 'pdf': 'Lernheft_Tag9_Agenten.pdf',
        'kurz': 'Agenten', 'uebungen': (14, 15),
        'label': 'Lernheft &nbsp;·&nbsp; Agenten – KI, die plant und handelt',
        'titles': {1: 'Generativ oder agentisch?', 2: 'Was ist ein Agent?', 3: 'Sieben Fähigkeiten eines Agenten',
                   4: 'Assistent oder Agent?', 5: 'Der technische Rahmen', 6: 'ReAct und ReWOO', 7: 'Die Schleife und ihre Bremsen',
                   8: 'Der Mensch bleibt im Spiel', 9: 'Prüfen und absichern', 10: 'Viele Agenten im Team',
                   11: 'Wie Agenten starten – und womit man sie baut', 12: 'Unser Fall: der Angebots-Agent', 13: 'Die Lektion auf einer Seite',
                   14: 'Üben in Langdock (1)', 15: 'Üben in Langdock (2)', 16: 'Zwölf Merkfragen', 17: 'Die Wörter des Tages'}},
    10: {'src': 'tag10/lernheft.html', 'out': 'Tag 10 - APIs und MCP', 'pdf': 'Lernheft_Tag10_APIs-und-MCP.pdf',
         'kurz': 'APIs & MCP', 'uebungen': (14, 15),
         'label': 'Lernheft &nbsp;·&nbsp; APIs &amp; MCP – wie Software miteinander spricht',
         'titles': {1: 'APIs im Alltag', 2: 'Anfrage und Antwort', 3: 'Hat’s geklappt?', 4: 'Grenzen und Schlüssel',
                    5: 'MCP – der USB-C-Anschluss für KI', 6: 'So funktioniert MCP', 7: 'MCP oder API?', 8: 'REST verstehen',
                    9: 'Fünf Methoden, vier Grundaufgaben', 10: 'Der Buchladen: lesen und anlegen', 11: 'Ändern und löschen',
                    12: 'Unser Fall: Firmenrecherche mit MCP', 13: 'Die Lektion auf einer Seite',
                    14: 'Üben in Langdock (1)', 15: 'Üben in Langdock (2)', 16: 'Zwölf Merkfragen', 17: 'Die Wörter des Tages'}},
    11: {'src': 'tag11/lernheft.html', 'out': 'Tag 11 - KI-Infrastruktur', 'pdf': 'Lernheft_Tag11_KI-Infrastruktur.pdf',
         'kurz': 'KI-Infrastruktur', 'uebungen': (14, 15),
         'label': 'Lernheft &nbsp;·&nbsp; KI-Infrastruktur – welcher Stack ist der richtige?',
         'titles': {1: 'Der Stack als Landkarte', 2: 'Warum eigene Infrastruktur?', 3: 'Regeln und Standards', 4: 'Wo das Modell läuft',
                    5: 'Grafikspeicher und Quantisierung', 6: 'Wie schnell? Drei Kennzahlen', 7: 'Vier API-Typen', 8: 'Bündeln, steuern, bedienen',
                    9: 'Drei Betriebsmodelle', 10: 'Souveränität in Stufen', 11: 'Kosten und Betrieb', 12: 'Unser Fall: der Kanzlei-Stack',
                    13: 'Die Lektion auf einer Seite', 14: 'Üben in Langdock (1)', 15: 'Üben in Langdock (2)', 16: 'Zwölf Merkfragen', 17: 'Die Wörter des Tages'}},
    12: {'src': 'tag12/lernheft.html',
     'out': 'Tag 12 - EU AI Act',
     'pdf': 'Lernheft_Tag12_EU-AI-Act.pdf',
     'kurz': 'EU AI Act',
     'uebungen': (14, 15),
     'label': 'Lernheft &nbsp;·&nbsp; EU AI Act - KI richtig einordnen',
     'titles': {1: 'Erst den Einsatz verstehen',
                2: 'Wer trägt welche Verantwortung?',
                3: 'Die Risikostufen als Lernhilfe',
                4: 'Wann man stoppen muss',
                5: 'Hochrisiko: Zweck statt Branche',
                6: 'Pflichten passend zuordnen',
                7: 'Ein Steckbrief macht den Anfang',
                8: 'KI muss passend erkennbar sein',
                9: 'GPAI: das Modell hinter dem System',
                10: 'Termine immer mit Stand lesen',
                11: 'KI-Kompetenz und Verantwortung',
                12: 'Unser Fall: die Vorprüfung',
                13: 'Die Lektion auf einer Seite',
                14: 'Üben in Langdock: aufbauen',
                15: 'Üben in Langdock: testen',
                16: 'Zwölf Merkfragen',
                17: 'Die Wörter des Tages',
                18: 'Quellen und Korrekturen'}},
    13: {'src': 'tag13/lernheft.html', 'out': 'Tag 13 - DSGVO', 'pdf': 'Lernheft_Tag13_DSGVO.pdf', 'kurz': 'DSGVO', 'label': 'Lernheft · DSGVO – Daten mit Köpfchen', 'titles': {1: 'Datenschutz zum Anfassen', 2: 'Wissen hilft – eine Freigabe ist es nicht', 3: 'Datenschutz schützt Menschen', 4: 'Die Regeln greifen ineinander', 5: 'Erst die Wörter entwirren', 6: 'Ein Mensch muss nicht namentlich dastehen', 7: 'Schon Speichern ist Verarbeitung', 8: 'Wenn aus Angaben eine Bewertung wird', 9: 'Deckname ist nicht unsichtbar', 10: 'Wer entscheidet, wer erledigt?', 11: 'Sechs Fragen statt Paragrafen-Nebel', 12: 'Die sechs Grundsätze in Alltagssprache', 13: 'Gutes Handeln braucht Spuren', 14: 'Nicht alles mitgeben, nicht alles umwidmen', 15: 'Der Prompt macht eine Diät', 16: 'Die Eintrittskarte heißt Rechtsgrundlage', 17: 'Sechs mögliche Eintrittskarten', 18: 'Berechtigtes Interesse: drei ehrliche Fragen', 19: 'Der Newsletter braucht mehr als eine Adressliste', 20: 'Eine echte Wahl statt eines versteckten Häkchens', 21: 'Ja muss Ja heißen – und zurücknehmbar sein', 22: 'Manche Angaben brauchen besonders viel Schutz', 23: 'Die besonders geschützten Kategorien', 24: 'Ausnahme heißt nicht „passt schon“', 25: 'Menschen sollen nicht im Dunkeln stehen', 26: 'Der Beipackzettel für die Datenreise', 27: '„Was wisst ihr über mich?“', 28: 'Die Menschen haben einen Werkzeugkasten', 29: 'Eine Anfrage startet einen klaren Ablauf', 30: 'Daten brauchen einen Auszugsplan', 31: 'Wenn die Maschine über Chancen entscheidet', 32: 'Nicht jede Automatik darf allein entscheiden', 33: 'Ausnahmen brauchen Schutzgeländer', 34: 'Ein Mensch muss wirklich mitentscheiden', 35: 'Datenschutz ist auch Organisation', 36: 'Die datensparsame Einstellung ist der Startzustand', 37: 'Der AVV regelt einen bestimmten Auftrag', 38: 'Die Landkarte der Datenverarbeitung', 39: 'Wenn etwas schiefgeht: ruhig und zügig handeln', 40: 'Sicherheit richtet sich nach dem Risiko', 41: 'TOM: Technik plus gute Abläufe', 42: 'Das Schutzpaket zum Anfassen', 43: 'KI-Schutz beginnt vor dem Prompt', 44: '72 Stunden sind kein Warteauftrag', 45: 'Bei hohem Risiko müssen Menschen Bescheid wissen', 46: 'Vorher tiefer prüfen, wenn viel auf dem Spiel steht', 47: 'Die Folgenabschätzung schaut auf die Menschen', 48: 'Wann eine Datenschutz-Fachperson benannt werden muss', 49: 'Daten können weiter reisen als gedacht', 50: 'Schutz soll an der Grenze nicht verschwinden', 51: 'Angemessenheit: ein geprüfter Übermittlungsweg', 52: 'Es gibt mehrere geeignete Garantien', 53: 'SCCs: Vertragsbausteine mit Pflichten', 54: 'SCCs passend auswählen und wirklich umsetzen', 55: 'Vertrag plus Wirklichkeitscheck', 56: 'BCRs: verbindliche Regeln im Konzern', 57: 'Ausnahmen sind schmale Türen', 58: 'Vor dem Hochladen einmal die Datenreise prüfen', 59: 'Warum Sorgfalt zählt', 60: 'Zwei Obergrenzen – keine Pauschalstrafe', 61: 'Dokumente machen Abläufe sichtbar', 62: 'Ein Steckbrief pro Verarbeitung', 63: 'Ein Beispiel ist noch keine fertige Vorlage', 64: 'Vier Teile einer Folgenabschätzung', 65: 'Ein Risikowert braucht Begründung', 66: 'Wie wahrscheinlich – und wie schwer?', 67: 'Die Dokumenten-Schubladen', 68: 'Datenschutzhinweise, die man versteht', 69: 'Das Gelernte in kleine Entscheidungen übersetzen', 70: 'Eine Ampel ist ein Hinweis, keine Erlaubnis', 71: 'Der Tool-Check vor dem Start', 72: 'Zehn Merksätze – mit den nötigen Grenzen', 73: 'Die nächste sinnvolle Handlung', 74: 'Das Trust Center als Recherche-Start'}},
    14: {'src': 'tag14/lernheft.html', 'out': 'Tag 14 - Agent Observability', 'pdf': 'Lernheft_Tag14_Agent-Observability.pdf', 'kurz': 'Agent Observability', 'label': 'Lernheft · Der Antwort auf der Spur', 'titles': {1: 'Der Blick hinter die Antwort', 2: 'Drei Lupen für einen KI-Lauf', 3: 'Kein Fehlercode. Trotzdem falsch.', 4: 'Punkte, Linie und Kontrolllampe', 5: 'Vier Fragen statt einer grünen Lampe', 6: 'Eine Anfrage, viele kleine Stationen', 7: 'Langdock mit Langfuse verbinden', 8: 'Was der Kontrollblick sichtbar macht', 9: 'So wird aus Wissen ein Versuch', 10: 'Der Fehlerdetektiv', 11: 'Vier Spuren, vier Schubladen', 12: 'Klingt gut – stimmt es auch?', 13: 'Die Zehn-Sekunden-Schnecke'}, 'uebungen': (10, 11, 12, 13)},
    # Praxishefte: zum Mitmachen, gehoeren zu einem Kurstag (tag), eigene Adresse /<person>/tag-N/praxis/
    'p10': {'tag': 10, 'art': 'Praxisheft', 'ref': 'praxis', 'unter': 'zum Mitmachen', 'src': 'tag10/praxisheft.html',
            'out': 'Tag 10 - APIs und MCP', 'pdf': 'Praxisheft_Tag10_APIs-und-MCP.pdf', 'kurz': 'APIs & MCP selbst ausprobieren',
            'label': 'Praxisheft &nbsp;·&nbsp; APIs &amp; MCP selbst ausprobieren',
            'titles': {1: 'Die erste API im Browser', 2: 'Echte Daten: Bücher, Feiertage, Kurse', 3: 'Statuscodes live erleben',
                       4: 'Alle Methoden mit Hoppscotch', 5: 'Langdock als API-Dolmetscher', 6: 'Den ersten MCP-Server in Langdock verbinden',
                       7: 'MCP testen – im Chat und im Agenten', 8: 'Kostenlose MCP-Server zum Ausprobieren', 9: 'Kostenlose APIs zum Lernen',
                       10: 'Sicher bleiben – und aufräumen', 11: 'Drei Mini-Challenges', 12: 'Der Spickzettel'}},
}


from tag15.content import PAGES as TAG15_PAGES
HEFTE[15] = {'src': 'tag15/lernheft.html', 'out': 'Tag 15 - KI-Werkzeuge im Vergleich',
             'pdf': 'Lernheft_Tag15_KI-Werkzeuge-im-Vergleich.pdf', 'kurz': 'KI-Werkzeuge',
             'label': 'Lernheft · Vom Chat zur kleinen Werkstatt', 'uebungen': (11,12,13,14,15,16),
             'titles': {i:p['title'] for i,p in enumerate(TAG15_PAGES,1)}}

def toc_titles(tag):
    """Kapitel fuer das Inhaltsverzeichnis der Plattform: alles vor 'Lektion auf einer Seite' + die Uebungsseite."""
    cfg = HEFTE[tag]
    items = sorted(cfg['titles'].items())
    if 'uebungen' in cfg:
        first = cfg['uebungen'][0]
        return [(k, v) for k, v in items if k < first - 1] + [(first, 'Freiwillige Übungen in Langdock')]
    return items[:-3]
TITLES = HEFTE[4]['titles']  # fuer aeltere Aufrufer


def esc(s):
    return H.escape(str(s), quote=True)


def compose(head, logo, bar='', ux=False, zooms=None, tag=4):
    cfg = HEFTE[tag]
    day = cfg.get('tag', tag)          # Praxishefte ('p10') gehoeren zu einem Kurstag
    t = kurs.TAGE[day]
    html = open(os.path.join(HERE, cfg['src']), encoding='utf-8').read()
    qa = '\n'.join(f'    <div><span class="qn">FRAGE {i:02d}</span><b>{esc(q)}</b><p>{esc(a)}</p></div>'
                   for i, (q, a) in enumerate(t['karten'], 1))
    gl = '\n'.join(f'    <div><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in t['begriffe'])
    # Langdock-Variablen wie {{ thema }} in Karten/Begriffen sind Text, keine Platzhalter
    qa, gl = (x.replace('{{', '&#123;&#123;').replace('}}', '&#125;&#125;') for x in (qa, gl))

    def uxbtn(m):
        n = int(m.group(1))
        if not ux:
            return ''
        return (f'<button class="unklar ux" type="button" data-unklar-ref="t{day}:{cfg.get("ref", "lernheft")}:k{n}" data-unklar-hash="#k{n}" '
                f'data-unklar-label="{cfg.get("art", "Lernheft")} · {esc(cfg["titles"][n])}">Unklar?</button>')
    html = re.sub(r'\{\{UX:(\d+)\}\}', uxbtn, html)
    html = re.sub(r'\{\{ICON:(\w+)\}\}', lambda m: ICONS[m.group(1)], html)
    # Langdock-Variable {{ name }} - als Entities, damit die Platzhalter-Pruefung unten nicht anschlaegt
    html = re.sub(r'\{\{VAR:(\w+)\}\}', lambda m: f'<span class="vtag">&#123;&#123; {m.group(1)} &#125;&#125;</span>', html)
    for k, v in (('{{QA}}', qa), ('{{GLOSSAR}}', gl), ('{{HEAD}}', head), ('{{LOGO}}', logo), ('{{BAR}}', bar)):
        html = html.replace(k, v)
    if zooms:
        parts = html.split('<section class="lp')
        html = parts[0] + ''.join(f'<section style="--z:{zooms[i]}" class="lp' + part for i, part in enumerate(parts[1:]))
    if '{{' in html:
        i = html.index('{{')
        raise AssertionError('Platzhalter uebrig: ' + html[i:i + 40])
    return html


def web_page(pid, tag=4):
    """Web-Fassung je Person (wegen "Unklar?" und Zurueck-Link)."""
    if tag == 15:
        from tag15.build_material import render_web
        return render_web(pid)
    cfg = HEFTE[tag]
    day = cfg.get('tag', tag)
    p = kurs.PERSONEN[pid]
    head = (f'<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">'
            f'<link rel="icon" href="{BASE}/assets/favicon.svg" type="image/svg+xml">'
            f'<link rel="stylesheet" href="{BASE}/assets/app.css"><link rel="stylesheet" href="{BASE}/assets/lernheft.css">'
            f'<script src="{BASE}/assets/app.js" defer></script>')
    bar = (f'<header class="lhbar{" praxis" if cfg.get("art") == "Praxisheft" else ""}"><a href="{BASE}/{pid}/tag-{day}/">&larr; Tag {day}</a>'
           f'<div class="t"><b>{cfg.get("art", "Lernheft")} Tag {day} · {cfg["kurz"]}</b><span>{esc(p["name"])} · {cfg.get("unter", "zum Lesen und Merken")}</span></div>'
           f'<span id="dz-slot"></span><a class="btn" href="{BASE}/pdf/{cfg["pdf"]}" download>Als PDF</a></header>')
    html = compose(head, f'{BASE}/assets/futureway_logo.png', bar, ux=True, tag=tag)
    return html.replace('<html lang="de">', f'<html lang="de" data-person="{pid}" data-tag="{day}" data-page="lernheft">', 1)


def main():
    arg = sys.argv[sys.argv.index('--tag') + 1] if '--tag' in sys.argv else '4'
    if arg == '15':
        from tag15.build_material import main as build_tag15
        return build_tag15()
    tag = int(arg) if arg.isdigit() else arg      # z. B. --tag p10 fuer das Praxisheft von Tag 10
    cfg = HEFTE[tag]
    OUT_DIR, PDF_NAME, LABEL = os.path.join(HERE, '..', cfg['out']), cfg['pdf'], cfg['label']
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(HERE, 'futureway_logo.png'), 'rb') as f:
        logo = 'data:image/png;base64,' + base64.b64encode(f.read()).decode()
    head = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
            '<style>' + open(os.path.join(HERE, 'lernheft.css'), encoding='utf-8').read() + '</style>')
    src = os.path.join(BUILD, f'lernheft_t{tag}.html')
    with open(src, 'w', encoding='utf-8') as f:
        f.write(compose(head, logo, tag=tag))
    # 1. Durchgang: Platzbedarf messen -> Zoom je Seite, damit jede Seite die A4-Hoehe fuellt
    zf = os.path.join(BUILD, 'lernheft_zoom.json')
    subprocess.run(['node', os.path.join(HERE, 'measure_lp.mjs'), src, '--fit', zf], check=True)
    zooms = json.load(open(zf))
    with open(src, 'w', encoding='utf-8') as f:
        f.write(compose(head, logo, zooms=zooms, tag=tag))
    # 2. Durchgang: passt jede Seite (Hoehe und Breite)?
    subprocess.run(['node', os.path.join(HERE, 'measure_lp.mjs'), src], check=True)
    final = os.path.join(OUT_DIR, PDF_NAME)
    job = {'html': src, 'pdf': os.path.join(BUILD, PDF_NAME), 'pdfPlain': os.path.join(BUILD, 'plain_' + PDF_NAME), 'label': LABEL, 'final': final}
    jf = os.path.join(BUILD, 'jobs_lernheft.json')
    with open(jf, 'w', encoding='utf-8') as f:
        json.dump([job], f)
    subprocess.run(['node', os.path.join(HERE, 'render.mjs'), jf], check=True)
    from pypdf import PdfReader, PdfWriter
    full, plain = PdfReader(job['pdf']), PdfReader(job['pdfPlain'])
    w = PdfWriter()
    w.add_page(plain.pages[0])
    for pg in full.pages[1:]:
        w.add_page(pg)
    art, day = cfg.get('art', 'Lernheft'), cfg.get('tag', tag)
    w.add_metadata({'/Title': f'{art} Tag {day} - {cfg["kurz"]}', '/Author': 'Futureway KI Institut',
                    '/Subject': f'KI Automations Spezialist - {art} zu Tag {day} {cfg["kurz"]}'})
    with open(final, 'wb') as f:
        w.write(f)
    print(f'{PDF_NAME}: {len(full.pages)} Seiten')
    if '--preview' in sys.argv:
        import fitz
        pv = os.path.join(BUILD, 'preview')
        os.makedirs(pv, exist_ok=True)
        for old in os.listdir(pv):
            if old.startswith('LH_'):
                os.remove(os.path.join(pv, old))
        nxt = sys.argv[sys.argv.index('--preview') + 1] if len(sys.argv) > sys.argv.index('--preview') + 1 else ''
        dpi = int(nxt) if nxt.isdigit() else 70
        for i, page in enumerate(fitz.open(final)):
            page.get_pixmap(dpi=dpi).save(os.path.join(pv, f'LH_{i + 1:02d}.png'))


if __name__ == '__main__':
    main()
