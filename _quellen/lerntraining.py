"""Aktives Erinnern für alle Tage; redaktionelle Fallwerkstatt für Tag 12.

Antworten bleiben lokal. Inhaltsfingerprints vermeiden veralteten Lernstand nach
Änderungen. Quellen der Fälle: geprüfte Learnings in kurs_tag12.py.
"""
import hashlib
import html
import json
import einfach_tag12
import einfach_tag13
import einfach_tag14
from tag15.content import SLIDES as SLIDES15


def cards(tage, until):
    out = []
    for n, t in tage.items():
        if n > until:
            continue
        if n == 12:
            rows = [(s[5], s[6], s[2], s[4], s[0]) for s in einfach_tag12.SLIDES]
        elif n == 13:
            rows = [(s[5], s[6], s[2], s[4], s[0]) for s in einfach_tag13.SLIDES]
        elif n == 14:
            rows = [(s[5], s[6], s[2], s[4], s[0]) for s in einfach_tag14.SLIDES]
        elif n == 15:
            rows = [(s[5], s[6], s[2], s[4], s[0]) for s in SLIDES15]
        else:
            rows = [(q, a, '', '', None) for q, a in t['karten']]
        for q, a, explanation, example, slide in rows:
            digest = hashlib.sha256('\n'.join((q, a, explanation, example)).encode()).hexdigest()[:12]
            out.append(dict(id=f't{n}-{digest}', day=n, question=q, answer=a,
                            title=t['titel'], explanation=explanation, example=example, slide=slide))
    return out


def case(id, title, scene, options, correct, feedback, takeaway, learning, article):
    return dict(id=id, title=title, scene=scene, options=options, correct=correct,
                feedback=feedback, takeaway=takeaway, learning=learning, article=article)


COMMON = [
    case('zweck', 'Gleiches Werkzeug, anderes Risiko',
         'Bei der fiktiven Firma Nordlicht korrigiert eine KI Tippfehler in Stellenanzeigen. Nun soll dasselbe Werkzeug Bewerbungen bewerten und eine Rangliste erstellen. „Das Tool war doch schon freigegeben“, heißt es im Team. Was ist der nächste Schritt?',
         ['Die bisherige Freigabe übernehmen: Das Modell bleibt gleich.',
          'Den neuen Zweck, betroffene Menschen und Entscheidungseinfluss prüfen.',
          'Jede KI-Nutzung im Unternehmen dauerhaft beenden.'], 1,
         ['Die alte Prüfung bezog sich auf einen anderen Einsatz. Ein unveränderter Modellname ersetzt keine Prüfung des neuen Zwecks.',
          'Genau: Bewerbungsbewertung ist ein typischer Hochrisikofall. Man prüft die konkrete Anwendung und geltende Anforderungen, bevor man sie einsetzt.',
          'Ein pauschaler Stopp aller Anwendungen folgt daraus nicht. Die Rechtschreibhilfe und die Bewerbungsbewertung müssen getrennt betrachtet werden.'],
         'Ein neuer Zweck braucht eine neue Prüfung.', 'l9', 6),
    case('quelle', 'Die KI klingt sehr sicher',
         'Eine Kursassistenz schreibt: „Alle Pflichten sind erfüllt. Der Einsatz ist rechtlich freigegeben.“ Es fehlen Quellen, Datum und Angaben dazu, welche Daten verarbeitet werden. Wie geht man damit um?',
         ['Die Freigabe übernehmen, weil die Antwort eindeutig klingt.',
          'Nur das Wort „rechtlich“ entfernen und den Text weitergeben.',
          'Fehlende Angaben klären, aktuelle Quellen prüfen und die zuständige Person einbeziehen.'], 2,
         ['Sicherer Ton ist kein Beleg. Ohne Einsatzdaten und Quellen ist die Aussage nicht belastbar.',
          'Eine sprachliche Änderung löst die fehlende Prüfung nicht. Die offenen Fragen bleiben offen.',
          'Richtig: Die Assistenz unterstützt eine Vorprüfung. Eine begründete Einschätzung zeigt Quellen, Grenzen und offene Fragen.'],
         'KI hilft beim Prüfen; sie erteilt keine rechtliche Freigabe.', 'l19', None),
    case('fehler', 'Den Denkfehler entdecken',
         'Auf einem internen Merkblatt steht: „Geringes KI-Risiko bedeutet: Datenschutz und Urheberrecht spielen keine Rolle.“ Welche Korrektur passt?',
         ['Auch bei geringem KI-Risiko müssen andere anwendbare Regeln geprüft werden.',
          'Der Satz stimmt, solange das KI-Werkzeug kostenlos ist.',
          'Datenschutz gilt erst, wenn die KI selbst Personenentscheidungen trifft.'], 0,
         ['Richtig: Die KI-Risikoklasse ersetzt weder die Datenschutzprüfung noch die Prüfung von Nutzungsrechten.',
          'Der Preis des Werkzeugs entscheidet nicht über Datenschutz oder Nutzungsrechte.',
          'Schon die Verarbeitung personenbezogener Daten kann Datenschutzpflichten auslösen; eine automatische Entscheidung ist dafür nicht erforderlich.'],
         'KI-Risikoprüfung und andere Rechtsfragen gehören nebeneinander auf die Checkliste.', 'l13', None),
]

PROFILES = {
    'tabea': [
        case('video', 'Ein täuschend echtes Kundenlob',
             'Das fiktive Studio Morgenrot erstellt einen KI-Clip, in dem eine erfundene Kundin ein Produkt lobt. Bild und Stimme wirken wie eine echte Aufnahme. Der Clip soll ohne Hinweis veröffentlicht werden. Was sollte vor der Veröffentlichung geklärt werden?',
             ['Nichts, denn eine erfundene Person macht den Clip automatisch unproblematisch.',
              'Täuschungseindruck, mögliche Offenlegungspflichten und weitere Rechte prüfen.',
              'Nur einen winzigen Hinweis in unsichtbaren Dateimetadaten ergänzen.'], 1,
             ['Auch erfundene Inhalte können Menschen über ihre Echtheit täuschen. Die konkrete Gestaltung und der Kontext müssen geprüft werden.',
              'Genau: Ein täuschend echter synthetischer Clip verlangt eine konkrete Prüfung. Technische Markierung und eine für Menschen erkennbare Offenlegung sind unterschiedliche Dinge.',
              'Metadaten ersetzen eine erforderliche sichtbare Offenlegung nicht. Der Hinweis muss im konkreten Kontext verständlich und zugänglich sein.'],
             'Vor dem Veröffentlichen fragen: Was könnte das Publikum für echt halten?', 'l15', 50),
        case('chat', 'Üben ohne Agent-Zugang',
             'Für die Übung soll man einen KI-Einsatz vorprüfen. Im eigenen Langdock-Konto lassen sich keine Agenten erstellen. Wie kann man trotzdem sinnvoll lernen?',
             ['Die Zugangsdaten einer anderen Person verwenden.',
              'Die Übung auslassen, weil nur ein Agent die Fragen stellen kann.',
              'Im normalen Chat den Prüfablauf nutzen und einen verfügbaren Skill über @ auswählen.'], 2,
             ['Fremde Zugangsdaten sind kein sinnvoller Übungsweg. Der Prüfablauf lässt sich im eigenen Chat anwenden.',
              'Die Lernaufgabe ist das strukturierte Prüfen. Dafür ist kein selbst erstellter Agent erforderlich.',
              'Richtig: Zweck, Rolle, Menschen, Daten und Entscheidungseinfluss lassen sich auch im normalen Chat klären. Quellen und Ergebnis anschließend prüfen.'],
             'Der Prüfablauf ist die Fähigkeit; der Agent ist nur ein Werkzeug dafür.', 'l20', None),
    ],
    'ingo': [
        case('druck', 'Ein KI-Text für den Angebotsentwurf',
             'Das fiktive Druckhaus Linden nutzt KI für einen Angebotsentwurf. Eine Kollegin sagt: „Dann sind wir Anbieter des Sprachmodells und müssen dessen gesamte technische Dokumentation veröffentlichen.“ Wie ordnet man das ein?',
             ['Die bloße berufliche Nutzung macht das Druckhaus nicht zum Anbieter des Modells.',
              'Die Aussage stimmt bei jeder Nutzung eines Chats.',
              'Man muss nur den Modellnamen aus dem Angebot entfernen.'], 0,
             ['Richtig: In diesem beschriebenen Einsatz nutzt das Druckhaus ein Werkzeug. Ob durch eigene Bereitstellung oder Umbauten weitere Rollen entstehen, prüft man gesondert.',
              'Modell-Anbieter und berufliche Nutzer haben unterschiedliche Rollen. Die Aussage verwechselt diese Rollen.',
              'Die Rollen hängen vom tatsächlichen Handeln ab, nicht davon, ob der Modellname im Angebot steht.'],
             'Erst die eigene Rolle klären, dann die passenden Pflichten zuordnen.', 'l2', None),
        case('vertrieb', 'Ein Vertriebshelfer mit offenen Fragen',
             'Die fiktive Firma Papierblick möchte einen „intelligenten Vertriebshelfer“ einsetzen. Mehr ist noch nicht bekannt. Ein Kollege fordert sofort die Risikoklasse. Welche Antwort ist belastbar?',
             ['„Vertrieb ist immer geringes Risiko.“',
              '„Dafür fehlen Zweck, Daten, betroffene Menschen und Einfluss auf Entscheidungen.“',
              '„Jeder Vertriebshelfer ist automatisch verboten.“'], 1,
             ['Eine Abteilungsbezeichnung reicht nicht aus. Ein Textentwurf und eine folgenreiche Personenbewertung sind unterschiedliche Einsätze.',
              'Genau: Die fehlenden Angaben sind das Ergebnis der ersten Prüfung. Man muss keine Risikoklasse erraten.',
              'Ohne konkrete Einsatzbeschreibung lässt sich auch ein Verbot nicht pauschal behaupten.'],
             'Eine gute Vorprüfung macht fehlende Informationen sichtbar.', 'l19', None),
    ],
    'carmen': [
        case('team', 'Ein Zertifikat für alle?',
             'Die fiktive Agentur Nordlicht will KI-Kompetenz aufbauen. Das Team hat unterschiedliche Aufgaben und Vorkenntnisse. Welche Maßnahme passt zum Kursverständnis von Artikel 4?',
             ['Allen dasselbe Zertifikat kaufen und damit jede weitere Unterstützung beenden.',
              'Nur den Namen eines KI-Tools per E-Mail mitteilen.',
              'Passende Übungen, Grenzen und Ansprechpersonen je Arbeitsaufgabe festlegen.'], 2,
             ['Artikel 4 schreibt kein bestimmtes Zertifikat vor. Ein Zertifikat allein sagt wenig darüber, ob die Unterstützung zu den Aufgaben passt.',
              'Ein Toolname vermittelt noch keinen sinnvollen Umgang mit dessen Möglichkeiten und Grenzen.',
              'Richtig: Vorwissen, konkrete Arbeit und betroffene Menschen zählen. Lernmaßnahmen sollten dazu passen und praktisch nutzbar sein.'],
             'KI-Kompetenz wächst an den Aufgaben des Teams.', 'l4', 4),
        case('website', 'Wer antwortet hier eigentlich?',
             'Auf der Website der fiktiven Agentur Klarblick soll ein KI-Chat wie eine menschliche Kollegin auftreten. Besucher können nicht erkennen, dass KI antwortet. Was klärt man vor dem Start?',
             ['Wie KI-Interaktion klar und spätestens bei der ersten Interaktion erkennbar wird und wer dafür zuständig ist.',
              'Ob ein menschlich klingender Name als Hinweis genügt.',
              'Ob man den Hinweis erst zeigt, wenn jemand nachfragt.'], 0,
             ['Richtig: Artikel 50 Absatz 1 betrifft Anbieter und die erkennbare direkte KI-Interaktion, sofern sie nicht ohnehin offensichtlich ist. Die eigene Rolle und Umsetzung klärt man mit dem Anbieter.',
              'Ein menschlicher Name macht die KI-Nutzung gerade nicht deutlich.',
              'Ein erst auf Nachfrage erscheinender Hinweis kommt für die erforderliche Erkennbarkeit bei der ersten Interaktion zu spät.'],
             'Transparenz gehört an den Beginn der Begegnung mit der KI.', 'l14', 50),
    ],
}


def payload(pid, n, tage):
    cases = (PROFILES[pid] + COMMON) if n == 12 else []
    return dict(day=n, cards=cards(tage, n), cases=cases)


def panel(pid, n, tage):
    data = json.dumps(payload(pid, n, tage), ensure_ascii=False).replace('<', '\\u003c')
    return f'''<section class="tpanel wrap" id="training" role="tabpanel" aria-label="Trainieren">
  <div class="lt-intro"><div><p class="kicker">Kleine Runde · ungefähr 5 Minuten · ohne Zeitdruck</p>
    <h2>Aus Wissen wird Können.</h2><p>Erst selbst überlegen, dann vergleichen. Was noch wackelt, kommt wieder.</p></div>
    <ol class="lt-path" aria-label="So wird geübt"><li><b>01</b> Erinnern</li><li><b>02</b> Anwenden</li><li><b>03</b> Wiederholen</li></ol></div>
  <div data-training><script type="application/json" class="lt-data">{data}</script>
    <p class="lt-storage" role="status" hidden></p><div class="lt-dashboard"></div>
    <div class="lt-stage"></div>
    <details class="lt-transfer"><summary>In eigenen Worten: Was nehme ich mit?</summary>
      <label for="lt-note">Ein Merksatz und ein ausgedachtes Beispiel aus dem eigenen Bereich</label>
      <textarea id="lt-note" rows="4" maxlength="3000" placeholder="Ich achte künftig auf … Zum Beispiel …" aria-describedby="lt-note-hint"></textarea>
      <p id="lt-note-hint">Nur ausgedachte Daten. Die Notiz bleibt in diesem Browser und wird nicht automatisch bewertet.</p>
      <p class="lt-note-status" role="status"></p></details>
    <p class="lt-footnote">Der Lernstand gehört zur gewählten Person und bleibt auf diesem Gerät in diesem Browser. Er ist keine Prüfung oder Zertifizierung. Beim Löschen der Browserdaten geht er verloren.</p>
    <noscript><p>Das Training braucht JavaScript. Die Learnings und Lernhefte kann man weiterhin lesen.</p></noscript>
  </div></section>'''


def overview(pid, tage):
    data = json.dumps(dict(cards=cards(tage, max(tage))), ensure_ascii=False).replace('<', '\\u003c')
    return f'''<section class="wrap lt-overview" data-training-overview>
      <script type="application/json" class="lt-data">{data}</script>
      <p class="kicker">Dranbleiben in kleinen Schritten</p><h2>Eine kurze Runde reicht für heute.</h2>
      <p data-review-summary>Fünf Fragen abrufen, die eigene Antwort vergleichen und Unsicheres gezielt wiederholen.</p>
      <a class="btn primary" data-review-link href="/hefte/{html.escape(pid)}/tag-{max(tage)}/#training">5-Minuten-Runde starten →</a>
    </section>'''
