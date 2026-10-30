"""Neun fertige, sehr leichte Make-Vorlagen (Blueprints) für Modul 2, Woche 1.

Alle Vorlagen laufen mit Make Free, ohne Verbindung zu einem fremden Konto
(einzige Ausnahme A5: öffentliche Test-API ohne Anmeldung). Keine Vorlage
verschickt, veröffentlicht oder speichert etwas außerhalb von Make.

Format am 30.10.2026 mit Makes eigener Prüfung abgeglichen (validate_blueprint_schema, validate_module_configuration, eu1) und mit echten Make-Exporten aus der
Make-Community (util:SetVariable2, util:SetVariables, util:ComposeTransformer,
json:ParseJSON, builtin:BasicRouter, http:MakeRequest v4, Filter-Operatoren)
und help.make.com/blueprints (Import über ... > Import blueprint).
"""
import json

# ------------------------------------------------------------ Bausteine

def _designer(x, y, name):
    return {'x': x, 'y': y, 'name': name}


def set_var(mid, x, y, label, name, value):
    return {
        'id': mid, 'module': 'util:SetVariable2', 'version': 1, 'parameters': {},
        'mapper': {'name': name, 'value': value},
        'metadata': {
            'designer': _designer(x, y, label),
            'restore': {},
            'expect': [
                {'name': 'name', 'type': 'text', 'label': 'Variable name', 'required': True},
                {'name': 'value', 'type': 'any', 'label': 'Variable value'}],
            'interface': [{'name': name, 'label': name, 'type': 'any'}]}}


def set_vars(mid, x, y, label, pairs):
    return {
        'id': mid, 'module': 'util:SetVariables', 'version': 1, 'parameters': {},
        'mapper': {'variables': [{'name': n, 'value': v} for n, v in pairs]},
        'metadata': {
            'designer': _designer(x, y, label),
            'restore': {'expect': {'variables': {'items': [None] * len(pairs)}}},
            'expect': [
                {'name': 'variables', 'type': 'array', 'label': 'Variables',
                 'validate': {'unique': {'by': 'name'}},
                 'spec': {'type': 'collection', 'label': 'Variable', 'name': 'value', 'spec': [
                     {'name': 'name', 'label': 'Variable name', 'type': 'text', 'required': True},
                     {'name': 'value', 'label': 'Variable value', 'type': 'any'}]}}],
            'interface': [{'name': n, 'label': n, 'type': 'any'} for n, _ in pairs]}}


def compose(mid, x, y, label, text, filt=None):
    module = {
        'id': mid, 'module': 'util:ComposeTransformer', 'version': 1, 'parameters': {},
        'mapper': {'value': text},
        'metadata': {'designer': _designer(x, y, label), 'restore': {},
                     'expect': [{'name': 'value', 'type': 'text', 'label': 'Text'}]}}
    if filt:
        module['filter'] = filt
    return module


def parse_json(mid, x, y, label, text):
    return {
        'id': mid, 'module': 'json:ParseJSON', 'version': 1, 'parameters': {'type': ''},
        'mapper': {'json': text},
        'metadata': {
            'designer': _designer(x, y, label),
            'restore': {'parameters': {'type': {'label': 'Choose a data structure'}}},
            'parameters': [{'name': 'type', 'type': 'udt', 'label': 'Data structure'}],
            'expect': [{'name': 'json', 'type': 'text', 'label': 'JSON string', 'required': True}]}}


def http_get(mid, x, y, label, url):
    flags = ['headers', 'shareCookies', 'parseResponse', 'allowRedirects', 'stopOnHttpError', 'requestCompressedContent']
    expect = {name: {'mode': 'chose'} for name in flags}
    expect.update({'method': {'mode': 'chose', 'label': 'GET'}, 'contentType': {'label': 'Empty'},
                   'paginationType': {'label': 'Empty'}, 'queryParameters': {'mode': 'chose'}})
    return {
        'id': mid, 'module': 'http:MakeRequest', 'version': 4,
        'parameters': {'authenticationType': 'noAuth', 'tlsType': ''},
        'mapper': {'url': url, 'method': 'get', 'shareCookies': False, 'parseResponse': True,
                   'allowRedirects': True, 'stopOnHttpError': True, 'requestCompressedContent': True},
        'metadata': {
            'designer': _designer(x, y, label),
            'restore': {'expect': expect, 'parameters': {
                'tlsType': {'label': 'Empty'}, 'authenticationType': {'label': 'No authentication'}}},
            'parameters': [
                {'name': 'authenticationType', 'type': 'select', 'label': 'Authentication type', 'required': True,
                 'validate': {'enum': ['noAuth', 'apiKey', 'basicAuth', 'oAuth']}},
                {'name': 'tlsType', 'type': 'select', 'label': 'Transport layer security (TLS)',
                 'validate': {'enum': ['mTls', 'tls']}}],
            'expect': [
                {'name': 'url', 'type': 'url', 'label': 'URL', 'required': True},
                {'name': 'method', 'type': 'select', 'label': 'Method', 'required': True,
                 'validate': {'enum': ['get', 'head', 'post', 'put', 'patch', 'delete', 'options']}},
                {'name': 'parseResponse', 'type': 'boolean', 'label': 'Parse response', 'required': True},
                {'name': 'stopOnHttpError', 'type': 'boolean', 'label': 'Return error if HTTP request fails', 'required': True},
                {'name': 'allowRedirects', 'type': 'boolean', 'label': 'Allow redirects', 'required': True},
                {'name': 'shareCookies', 'type': 'boolean', 'label': 'Share cookies with other HTTP modules', 'required': True},
                {'name': 'requestCompressedContent', 'type': 'boolean', 'label': 'Request compressed content', 'required': True}]}}


def router(mid, x, y, label, routes):
    return {'id': mid, 'module': 'builtin:BasicRouter', 'version': 1, 'mapper': None,
            'metadata': {'designer': _designer(x, y, label)},
            'routes': [{'flow': flow} for flow in routes]}


def cond(a, op, b):
    return {'a': a, 'o': op, 'b': b}


def filt(name, *groups):
    """Jede Gruppe ist eine UND-Liste. Mehrere Gruppen sind ODER-verknüpft."""
    return {'name': name, 'conditions': [list(g) for g in groups]}


def blueprint(name, flow):
    return {'name': name, 'flow': flow, 'metadata': {
        'instant': False, 'version': 1,
        'scenario': {'roundtrips': 1, 'maxErrors': 3, 'autoCommit': True, 'autoCommitTriggerLast': True,
                     'sequential': False, 'slots': None, 'confidential': False, 'dataloss': False,
                     'dlq': False, 'freshVariables': False},
        'designer': {'orphans': []}}}


# ------------------------------------------------------------ Die neun Vorlagen
# Jede Vorlage: Datei, Kurzinfo, Modul-Erklärungen, Test, Soll, Ändern, Fehlerhilfe.

BERLIN = '"DD.MM.YYYY HH:mm"; "Europe/Berlin"'

AUTOMATIONS = [
 dict(
  nr=1, slug='A1_Begruessungs-Mixer', tag=1, level=1, minuten=10, credits=2,
  titel='Begrüßungs-Mixer',
  kurz='Aus einem Vornamen wird ein fertiger Begrüßungssatz.',
  lernt='Mapping: Ein Wert aus Baustein 1 wird in Baustein 2 eingesetzt.',
  flow=lambda: [
   set_var(1, 0, 0, '1 · Vorname bereitstellen', 'vorname', 'Luna'),
   compose(2, 300, 0, '2 · Begrüßung bauen', 'Hallo {{1.vorname}}! Willkommen in Modul 2.')],
  module=[
   ('Tools › Set variable', '1 · Vorname bereitstellen',
    [('Variable name', 'vorname', 'So heißt das Fach, in dem der Wert liegt.'),
     ('Variable value', 'Luna', 'Das ist der Inhalt. Hier darfst du später einen anderen Namen eintippen.')]),
   ('Tools › Compose a string', '2 · Begrüßung bauen',
    [('Text', 'Hallo {{1.vorname}}! Willkommen in Modul 2.',
      'Der Teil {{1.vorname}} ist eine Platzhalter-Kachel: „nimm den Wert vorname aus Baustein 1“.')])],
  soll='Hallo Luna! Willkommen in Modul 2.',
  soll_wo='Weiße Sprechblase über Baustein 2 → OUTPUT → Text',
  aendern=('Im Baustein 1 bei Variable value „Luna“ durch „Mira“ ersetzen, OK, speichern, wieder Run once.',
           'Hallo Mira! Willkommen in Modul 2.'),
  fehler=[('Es steht trotzdem „Luna“ da', 'Im Baustein 2 wurde der Name fest eingetippt statt als Kachel eingesetzt. Text löschen und {{1.vorname}} aus der Auswahlliste (Baustein 1) anklicken.'),
          ('Ausgabe ist leer', 'Prüfen, ob in Baustein 1 bei Variable value wirklich ein Name steht.')]),
 dict(
  nr=2, slug='A2_Redaktionsbriefing', tag=2, level=1, minuten=10, credits=2,
  titel='Redaktionsbriefing aus JSON',
  kurz='Ein JSON-Zettel mit vier Angaben wird zu einem lesbaren Briefing.',
  lernt='JSON lesen, Parse JSON nutzen und vier Felder mappen.',
  flow=lambda: [
   parse_json(1, 0, 0, '1 · JSON-Zettel lesen',
              json.dumps({'projekt': 'Papierfunke', 'thema': 'Workshop am 30.10.', 'kanal': 'Instagram', 'status': 'ENTWURF'},
                         ensure_ascii=False, indent=2)),
   compose(2, 300, 0, '2 · Briefing schreiben',
           'Projekt: {{1.projekt}}\nThema: {{1.thema}}\nKanal: {{1.kanal}}\nStatus: {{1.status}}\nNoch keine Veröffentlichung.')],
  module=[
   ('JSON › Parse JSON', '1 · JSON-Zettel lesen',
    [('Data structure', 'leer lassen', 'Make erkennt die Felder beim ersten Lauf selbst.'),
     ('JSON string', '{"projekt": "Papierfunke", "thema": "Workshop am 30.10.", "kanal": "Instagram", "status": "ENTWURF"}',
      'Der beschriftete Zettel. Links steht immer der Feldname, rechts der Wert.')]),
   ('Tools › Compose a string', '2 · Briefing schreiben',
    [('Text', 'Projekt: {{1.projekt}} … Status: {{1.status}}',
      'Vier Kacheln aus Baustein 1. Der feste Text davor (Projekt:, Thema: …) bleibt immer gleich.')])],
  soll='Projekt: Papierfunke\nThema: Workshop am 30.10.\nKanal: Instagram\nStatus: ENTWURF\nNoch keine Veröffentlichung.',
  soll_wo='Sprechblase über Baustein 2 → OUTPUT → Text',
  aendern=('Im Baustein 1 nur die Werte tauschen: projekt „Nordlicht“, thema „Interview vorbereiten“, kanal „Internes Projektbriefing“. Anführungszeichen und Kommas stehen lassen.',
           'Projekt: Nordlicht · Thema: Interview vorbereiten · Kanal: Internes Projektbriefing · Status: ENTWURF'),
  fehler=[('Fehlermeldung „Source is not valid JSON“', 'Ein Anführungszeichen, Komma oder eine Klammer fehlt. Die Vorlage neu importieren oder nur die Werte zwischen den Anführungszeichen ändern.'),
          ('Kacheln in Baustein 2 sind grau', 'Normal vor dem ersten Lauf. Nach einmal Run once kennt Make die Felder.')]),
 dict(
  nr=3, slug='A3_Freigabe-Ampel', tag=3, level=1, minuten=10, credits=2,
  titel='Freigabe-Ampel mit Filter',
  kurz='Nur FERTIG darf weiter. ENTWURF bleibt stehen.',
  lernt='Ein Filter auf der Verbindung entscheidet: weiter oder Stopp.',
  flow=lambda: [
   set_var(1, 0, 0, '1 · Status bereitstellen', 'status', 'FERTIG'),
   compose(2, 300, 0, '2 · Meldung schreiben', 'Beitrag zur Planung bereit. Status: {{1.status}}',
           filt('Nur FERTIG darf weiter', [cond('{{1.status}}', 'text:equal', 'FERTIG')]))],
  module=[
   ('Tools › Set variable', '1 · Status bereitstellen',
    [('Variable name', 'status', 'Das Fach heißt status.'), ('Variable value', 'FERTIG', 'Der Testwert. Groß geschrieben, ohne Leerzeichen.')]),
   ('Filter (auf der Verbindungslinie)', 'Nur FERTIG darf weiter',
    [('Condition', '{{1.status}}  ·  Equal to  ·  FERTIG', 'Lies: „Ist der Status genau gleich FERTIG?“ Nur dann geht es weiter.')]),
   ('Tools › Compose a string', '2 · Meldung schreiben',
    [('Text', 'Beitrag zur Planung bereit. Status: {{1.status}}', 'Wird nur ausgeführt, wenn der Filter Ja sagt.')])],
  soll='Beitrag zur Planung bereit. Status: FERTIG',
  soll_wo='Sprechblase über Baustein 2',
  aendern=('Im Baustein 1 „FERTIG“ durch „ENTWURF“ ersetzen, speichern, Run once.',
           'Baustein 2 bekommt keine Sprechblase. Der Lauf endet am Filter. Das ist richtig.'),
  fehler=[('Bei FERTIG passiert auch nichts', 'Schreibweise prüfen: genau FERTIG, groß, ohne Leerzeichen am Ende.'),
          ('Filter ist weg', 'Auf den Schraubenschlüssel unter der Verbindungslinie klicken → Set up a filter. Werte wie oben eintragen.')]),
 dict(
  nr=4, slug='A4_Anfragen-Weiche', tag=3, level=2, minuten=15, credits=2,
  titel='Anfragen-Weiche mit Router',
  kurz='Eine Anfrage landet je nach Anliegen bei Vertrieb, Support oder „Sonstiges“.',
  lernt='Router = Weiche mit mehreren Wegen. Jeder Weg hat seinen eigenen Filter.',
  flow=lambda: [
   set_vars(1, 0, 0, '1 · Anfrage bereitstellen', [('name', 'Kim Beispiel'), ('anliegen', 'Support'),
            ('nachricht', 'Der Download-Link aus der Bestätigung funktioniert nicht.')]),
   router(2, 300, 0, '2 · Weiche', [
    [compose(3, 600, -150, '3a · An Vertrieb', 'VERTRIEB: Bitte ein Angebot für {{1.name}} vorbereiten.\nNachricht: {{1.nachricht}}',
             filt('Anliegen enthält Angebot', [cond('{{1.anliegen}}', 'text:contain:ci', 'Angebot')]))],
    [compose(4, 600, 0, '3b · An Support', 'SUPPORT: {{1.name}} braucht Hilfe.\nNachricht: {{1.nachricht}}',
             filt('Anliegen enthält Support', [cond('{{1.anliegen}}', 'text:contain:ci', 'Support')]))],
    [compose(5, 600, 150, '3c · Sonstiges', 'SONSTIGES: Ein Mensch schaut sich die Anfrage von {{1.name}} an.\nNachricht: {{1.nachricht}}',
             filt('Anliegen ist Sonstiges', [cond('{{1.anliegen}}', 'text:equal', 'Sonstiges')]))]])],
  module=[
   ('Tools › Set multiple variables', '1 · Anfrage bereitstellen',
    [('name', 'Kim Beispiel', 'Erfundene Person.'), ('anliegen', 'Support', 'Danach richtet sich die Weiche. Erlaubt: Angebot, Support, Sonstiges.'),
     ('nachricht', 'Der Download-Link …', 'Wird nur weitergereicht.')]),
   ('Flow Control › Router', '2 · Weiche',
    [('Wege', '3 Wege nach rechts', 'Der Router selbst kostet keine Credits. Er prüft jeden Weg einzeln.')]),
   ('Filter auf jedem Weg', 'enthält Angebot · enthält Support · ist Sonstiges',
    [('Operator', 'Contains (case insensitive) / Equal to', '„enthält“ findet das Wort auch in einem längeren Text, Groß-/Kleinschreibung egal.')]),
   ('Tools › Compose a string (3×)', '3a / 3b / 3c',
    [('Text', 'VERTRIEB: … / SUPPORT: … / SONSTIGES: …', 'Je Weg eine interne Notiz. Es wird nichts verschickt.')])],
  soll='SUPPORT: Kim Beispiel braucht Hilfe.\nNachricht: Der Download-Link aus der Bestätigung funktioniert nicht.',
  soll_wo='Nur Baustein 3b bekommt eine Sprechblase',
  aendern=('anliegen nacheinander auf „Angebot / Projekt“ und dann auf „Sonstiges“ setzen.',
           '„Angebot / Projekt“ → nur 3a läuft (enthält Angebot). „Sonstiges“ → nur 3c läuft.'),
  fehler=[('Zwei Wege laufen gleichzeitig', 'Richtig beobachtet: Ein Router startet jeden Weg, dessen Filter passt. Steht z. B. „Angebot und Support“ drin, laufen 3a und 3b.'),
          ('Kein Weg läuft', 'Der Wert passt zu keinem Filter, z. B. Tippfehler „Suport“. Genau das zeigt, warum feste Auswahllisten besser sind als Freitext.')]),
 dict(
  nr=5, slug='A5_Test-API-lesen', tag=4, level=2, minuten=10, credits=2,
  titel='Test-API lesen (HTTP)',
  kurz='Make holt einen Datensatz von einer öffentlichen Test-Schnittstelle.',
  lernt='HTTP GET, Statuscode 200 und Felder aus „Data“ mappen.',
  flow=lambda: [
   http_get(1, 0, 0, '1 · Testaufgabe abholen', 'https://jsonplaceholder.typicode.com/todos/1'),
   compose(2, 300, 0, '2 · Ergebnis lesbar machen',
           'Testaufgabe {{1.data.id}}: {{1.data.title}}\nErledigt: {{1.data.completed}}\nHTTP-Status: {{1.statusCode}}')],
  module=[
   ('HTTP › Make a request', '1 · Testaufgabe abholen',
    [('Authentication type', 'No authentication', 'Die Test-API braucht keine Anmeldung und keinen Schlüssel.'),
     ('URL', 'https://jsonplaceholder.typicode.com/todos/1', 'Die Adresse der Daten. /todos/1 = Datensatz Nummer 1.'),
     ('Method', 'GET', 'GET heißt: nur lesen, nichts verändern.'),
     ('Parse response', 'Yes', 'Make zerlegt die Antwort sofort in Felder (data.id, data.title …).')]),
   ('Tools › Compose a string', '2 · Ergebnis lesbar machen',
    [('Text', 'Testaufgabe {{1.data.id}}: {{1.data.title}} …', 'Die Kacheln findest du in der Auswahl unter Data.')])],
  soll='Testaufgabe 1: delectus aut autem\nErledigt: false\nHTTP-Status: 200',
  soll_wo='Sprechblase über Baustein 2 (Stand der Test-API am 30.10.2026)',
  aendern=('In Baustein 1 die URL auf …/todos/2 ändern.', 'Testaufgabe 2: quis ut nam facilis et officia qui · Erledigt: false · HTTP-Status: 200'),
  fehler=[('Fehler 404', 'Die Adresse gibt es nicht (z. B. /todos/9999). Status 404 heißt „nicht gefunden“ – Make stoppt mit Fehler.'),
          ('Felder sind leer', 'Parse response muss auf Yes stehen. Sonst kommt nur ein langer Text an.')]),
 dict(
  nr=6, slug='A6_Zeitstempel-Uebersetzer', tag=4, level=2, minuten=10, credits=2,
  titel='Zeitstempel-Übersetzer',
  kurz='Ein ISO-Zeitstempel in UTC wird zur deutschen Uhrzeit.',
  lernt='ISO 8601, das Z (= UTC) und formatDate mit Zeitzone Europe/Berlin.',
  flow=lambda: [
   set_var(1, 0, 0, '1 · Zeitstempel bereitstellen', 'zeitpunkt', '2026-07-29T14:35:07Z'),
   compose(2, 300, 0, '2 · In Berliner Zeit umrechnen',
           'Original (UTC): {{1.zeitpunkt}}\nIn Berlin: {{formatDate(1.zeitpunkt; ' + BERLIN + ')}} Uhr\n'
           'Jetzt gerade in Berlin: {{formatDate(now; ' + BERLIN + ')}} Uhr')],
  module=[
   ('Tools › Set variable', '1 · Zeitstempel bereitstellen',
    [('Variable name', 'zeitpunkt', ''), ('Variable value', '2026-07-29T14:35:07Z', 'Das Z am Ende heißt UTC. Beispiel aus Folie 32.')]),
   ('Tools › Compose a string', '2 · In Berliner Zeit umrechnen',
    [('Text', 'formatDate(1.zeitpunkt; "DD.MM.YYYY HH:mm"; "Europe/Berlin")',
      'formatDate macht aus einem Zeitpunkt lesbaren Text. Das Muster sagt wie, die Zone sagt wo.')])],
  soll='Original (UTC): 2026-07-29T14:35:07Z\nIn Berlin: 29.07.2026 16:35 Uhr\nJetzt gerade in Berlin: (deine aktuelle Uhrzeit)',
  soll_wo='Sprechblase über Baustein 2',
  aendern=('zeitpunkt auf 2026-10-30T09:00:00Z ändern.', 'In Berlin: 30.10.2026 10:00 Uhr – im Winter nur +1 Stunde, im Juli +2.'),
  fehler=[('Stunden stimmen nicht', 'Zeitzone fehlt oder ist falsch geschrieben. Genau Europe/Berlin, mit Schrägstrich.'),
          ('Statt Datum steht nur der Originaltext', 'Im Text fehlt formatDate( … ) oder eine Klammer. Vorlage neu importieren.')]),
 dict(
  nr=7, slug='A7_Zeitfresser-Rechner', tag=5, level=2, minuten=15, credits=2,
  titel='Zeitfresser-Rechner',
  kurz='Make rechnet Häufigkeit × Minuten und sortiert in „Top-Kandidat“ oder „kleiner Posten“.',
  lernt='Rechnen in Make und Zahlen-Filter (größer/kleiner) im Router.',
  flow=lambda: [
   set_vars(1, 0, 0, '1 · Tätigkeit eintragen', [('taetigkeit', 'Rechnungsdaten abtippen'), ('pro_monat', '60'), ('minuten', '12')]),
   router(2, 300, 0, '2 · Wie groß ist der Posten?', [
    [compose(3, 600, -100, '3a · Top-Kandidat',
             'TOP-KANDIDAT: {{1.taetigkeit}}\n{{1.pro_monat}} × {{1.minuten}} Min. = {{1.pro_monat * 1.minuten}} Minuten pro Monat (rund {{round(1.pro_monat * 1.minuten / 60)}} Stunden).\nLohnt einen Use-Case-Steckbrief.',
             filt('Ab 600 Minuten im Monat', [cond('{{1.pro_monat * 1.minuten}}', 'number:greaterorequal', '600')]))],
    [compose(4, 600, 100, '3b · Kleiner Posten',
             'KLEINER POSTEN: {{1.taetigkeit}}\n{{1.pro_monat}} × {{1.minuten}} Min. = {{1.pro_monat * 1.minuten}} Minuten pro Monat.\nVielleicht nervig, aber eher kein Start-Kandidat.',
             filt('Unter 600 Minuten im Monat', [cond('{{1.pro_monat * 1.minuten}}', 'number:less', '600')]))]])],
  module=[
   ('Tools › Set multiple variables', '1 · Tätigkeit eintragen',
    [('taetigkeit', 'Rechnungsdaten abtippen', 'Deine Tätigkeit in Worten.'),
     ('pro_monat', '60', 'Wie oft im Monat? Nur die Zahl.'), ('minuten', '12', 'Wie viele Minuten pro Vorgang? Nur die Zahl.')]),
   ('Flow Control › Router + 2 Zahlen-Filter', '2 · Wie groß ist der Posten?',
    [('Weg oben', '{{1.pro_monat * 1.minuten}}  ·  Greater than or equal to  ·  600', '600 Minuten = 10 Stunden im Monat. Unsere Lern-Grenze, keine Norm.'),
     ('Weg unten', '{{1.pro_monat * 1.minuten}}  ·  Less than  ·  600', 'Alles darunter.')]),
   ('Tools › Compose a string (2×)', '3a / 3b',
    [('Text', '… {{1.pro_monat * 1.minuten}} Minuten …', 'Das Sternchen * heißt „mal“. round( ) rundet auf ganze Stunden.')])],
  soll='TOP-KANDIDAT: Rechnungsdaten abtippen\n60 × 12 Min. = 720 Minuten pro Monat (rund 12 Stunden).\nLohnt einen Use-Case-Steckbrief.',
  soll_wo='Nur Baustein 3a bekommt eine Sprechblase',
  aendern=('Eine nervige, aber seltene Aufgabe testen: taetigkeit „Monatsbericht formatieren“, pro_monat 2, minuten 45.',
           'KLEINER POSTEN … 90 Minuten pro Monat. Genau die Folien-Botschaft: Die nervigste Aufgabe ist selten die teuerste.'),
  fehler=[('Kein Weg läuft', 'Bei pro_monat oder minuten steht ein Wort oder ein Komma („12,5“). Nur ganze Zahlen ohne Einheit eintragen.'),
          ('Rechnung zeigt Text statt Zahl', 'Das Sternchen fehlt oder steht außerhalb der geschweiften Klammern.')]),
 dict(
  nr=8, slug='A8_Use-Case-Steckbrief', tag=5, level=1, minuten=15, credits=2,
  titel='Use-Case-Steckbrief',
  kurz='Elf Angaben werden zu einem sauberen Steckbrief zum Kopieren.',
  lernt='Viele Variablen auf einmal setzen und als Vorlage ausgeben.',
  flow=lambda: [
   set_vars(1, 0, 0, '1 · Steckbrief ausfüllen', STECKBRIEF_BEISPIEL),
   compose(2, 300, 0, '2 · Steckbrief formatieren', STECKBRIEF_TEXT)],
  module=[
   ('Tools › Set multiple variables', '1 · Steckbrief ausfüllen',
    [('11 Felder', 'name … nicht_dabei', 'Die elf Felder aus dem Arbeitsauftrag 03. Ersetze die Beispielwerte durch deinen Kandidaten.')]),
   ('Tools › Compose a string', '2 · Steckbrief formatieren',
    [('Text', 'USE-CASE-STECKBRIEF … {{1.name}} …', 'Fester Rahmen plus elf Kacheln. Ergebnis kannst du kopieren und ins Heft legen.')])],
  soll='USE-CASE-STECKBRIEF\n1 Name: Druckanfragen vorsortieren\n…\n9 Nutzen: 15 Stunden pro Monat im Innendienst\n…',
  soll_wo='Sprechblase über Baustein 2 → Text → rechts oben kopieren',
  aendern=('Alle Werte in Baustein 1 durch deinen eigenen Kandidaten ersetzen (nur erfundene oder ungefährliche Angaben).',
           'Dein eigener Steckbrief im gleichen Format.'),
  fehler=[('Ein Feld bleibt leer', 'Die Variable hat in Baustein 1 keinen Wert. Leere Felder sind kein Fehler, sondern ein Ergebnis: im Heft markieren.'),
          ('Name falsch geschrieben', 'Variablennamen in Baustein 1 nicht umbenennen, nur die Werte ändern.')]),
 dict(
  nr=9, slug='A9_Rechnungs-Regel', tag=5, level=3, minuten=20, credits=2,
  titel='Rechnungs-Regel: KI liest, Regel entscheidet',
  kurz='Vier Prüfregeln entscheiden, ob eine Rechnung Standardfall (Stufe 3) oder Ausnahme (Stufe 2) ist.',
  lernt='UND/ODER im Filter, Autonomie-Stufen pro Pfad (Folie 20–22).',
  flow=lambda: [
   set_vars(1, 0, 0, '1 · Ausgelesene Rechnung (Beispiel)', [
    ('lieferant', 'Papierhaus Muster GmbH'), ('lieferant_bekannt', 'ja'), ('bestellbezug', 'ja'),
    ('betrag', '840'), ('sicherheit', '93')]),
   router(2, 300, 0, '2 · Regel prüft', [
    [compose(3, 600, -100, '3a · Standardfall (Stufe 3)',
             'STANDARDFALL · Stufe 3\nRechnung von {{1.lieferant}} über {{1.betrag}} € erfüllt alle vier Regeln.\nFreigabe vorbereitet. Ein Mensch prüft Stichproben.',
             filt('Alle 4 Regeln erfüllt (UND)', [
                 cond('{{1.lieferant_bekannt}}', 'text:equal', 'ja'), cond('{{1.bestellbezug}}', 'text:equal', 'ja'),
                 cond('{{1.betrag}}', 'number:less', '1000'), cond('{{1.sicherheit}}', 'number:greaterorequal', '90')]))],
    [compose(4, 600, 100, '3b · Ausnahme (Stufe 2)',
             'AUSNAHME · Stufe 2\nRechnung von {{1.lieferant}} über {{1.betrag}} € braucht eine menschliche Freigabe.\nBekannt: {{1.lieferant_bekannt}} · Bestellbezug: {{1.bestellbezug}} · Sicherheit: {{1.sicherheit}} %',
             filt('Mindestens 1 Regel verletzt (ODER)',
                  [cond('{{1.lieferant_bekannt}}', 'text:notequal', 'ja')], [cond('{{1.bestellbezug}}', 'text:notequal', 'ja')],
                  [cond('{{1.betrag}}', 'number:greaterorequal', '1000')], [cond('{{1.sicherheit}}', 'number:less', '90')]))]])],
  module=[
   ('Tools › Set multiple variables', '1 · Ausgelesene Rechnung (Beispiel)',
    [('lieferant … sicherheit', 'Papierhaus Muster GmbH · ja · ja · 840 · 93',
      'So sähe das Ergebnis eines KI-Leseschritts aus. Hier tippen wir es selbst ein – kein KI-Konto nötig.')]),
   ('Router · Weg oben: UND-Filter', 'Alle 4 Regeln erfüllt',
    [('4 Bedingungen in einer Gruppe', 'bekannt = ja UND Bestellbezug = ja UND Betrag < 1000 UND Sicherheit ≥ 90',
      'Alle vier müssen stimmen (AND).')]),
   ('Router · Weg unten: ODER-Filter', 'Mindestens 1 Regel verletzt',
    [('4 Gruppen, verbunden mit OR', 'bekannt ≠ ja ODER Bestellbezug ≠ ja ODER Betrag ≥ 1000 ODER Sicherheit < 90',
      'Eine verletzte Regel reicht für die Ausnahme.')]),
   ('Tools › Compose a string (2×)', '3a / 3b', [('Text', 'STANDARDFALL … / AUSNAHME …', 'Interne Notiz, keine Zahlung, kein Versand.')])],
  soll='STANDARDFALL · Stufe 3\nRechnung von Papierhaus Muster GmbH über 840 € erfüllt alle vier Regeln.\nFreigabe vorbereitet. Ein Mensch prüft Stichproben.',
  soll_wo='Nur Baustein 3a bekommt eine Sprechblase',
  aendern=('betrag auf 1450 ändern (oder sicherheit auf 71).', 'AUSNAHME · Stufe 2 … braucht eine menschliche Freigabe. Ändert sich die Betragsgrenze, änderst du nur eine Zahl im Filter – keinen Prompt.'),
  fehler=[('Beide Wege laufen', 'Ein Wert passt zu beiden Filtern, z. B. Tippfehler bei „ja“. Groß-/Kleinschreibung beachten: genau ja.'),
          ('Kein Weg läuft', 'betrag oder sicherheit enthält ein Komma, € oder %. Nur ganze Zahlen eintragen.')]),
]

STECKBRIEF_FELDER = [
 ('name', 'Name des Use-Cases', 'Kurz und konkret: Verb + Gegenstand.', 'Name'),
 ('eigentuemer', 'Verantwortlich im Fachbereich', 'Eine benannte Rolle oder Person, die nach dem Projekt für die Ergebnisse geradesteht.', 'Verantwortlich'),
 ('problem', 'Was tut heute weh?', 'Das echte Problem in einem Satz – nicht die gewünschte Technik.', 'Problem'),
 ('ausloeser', 'Auslöser', 'Welches Ereignis startet den Ablauf? (z. B. neue E-Mail, Formular, 1. des Monats)', 'Auslöser'),
 ('input', 'Input', 'Welche Daten kommen rein, in welchem Format, wo liegen sie?', 'Input'),
 ('verarbeitung', 'Was übernimmt das System?', 'Der klar abgegrenzte Teil: lesen, einordnen, zusammenfassen, prüfen …', 'System übernimmt'),
 ('output', 'Output', 'Was kommt heraus und wohin? (Tabelle, Entwurf, Aufgabe …)', 'Output'),
 ('volumen', 'Volumen', 'Wie oft pro Monat? Gezählt, nicht gefühlt.', 'Volumen'),
 ('nutzen', 'Nutzen', 'Eine Zahl + Einheit + Zeitraum. „Spart Zeit“ zählt nicht.', 'Nutzen'),
 ('richtig_wenn', 'Richtig ist das Ergebnis, wenn …', 'Woran zwei Menschen übereinstimmend erkennen, dass es stimmt.', 'Richtig, wenn'),
 ('nicht_dabei', 'Ausdrücklich nicht dabei', 'Was das System nicht darf oder nicht tut.', 'Nicht dabei')]

STECKBRIEF_BEISPIEL = [
 ('name', 'Druckanfragen vorsortieren'),
 ('eigentuemer', 'Leitung Innendienst'),
 ('problem', 'Anfragen kommen unvollständig per E-Mail; Rückfragen kosten Tage.'),
 ('ausloeser', 'Neue E-Mail im Postfach anfragen@'),
 ('input', 'E-Mail-Text: Produkt, Auflage, Format, Papier, Termin'),
 ('verarbeitung', 'Angaben auslesen, fehlende Felder markieren, Rückfrage-Entwurf vorbereiten'),
 ('output', 'Neue Zeile in der Anfragetabelle + Entwurf zur Prüfung'),
 ('volumen', '180 Anfragen pro Monat'),
 ('nutzen', '15 Stunden pro Monat im Innendienst'),
 ('richtig_wenn', 'Alle fünf Angaben stimmen mit der E-Mail überein'),
 ('nicht_dabei', 'Keine Preise, kein automatischer Versand an Kundschaft')]

STECKBRIEF_TEXT = 'USE-CASE-STECKBRIEF\n' + '\n'.join(
    f'{i} {short}: {{{{1.{key}}}}}' for i, (key, _, _, short) in enumerate(STECKBRIEF_FELDER, 1)) + \
    '\n\nOffene Felder markieren statt raten.'


def build_all():
    """Gibt {dateiname: blueprint-dict} zurück."""
    files = {}
    for a in AUTOMATIONS:
        name = f'M2 · A{a["nr"]} {a["titel"]}'
        files[f'M2-{a["slug"]}.blueprint.json'] = blueprint(name, a['flow']())
    return files


def check(bp):
    """Kleine Strukturprüfung: IDs eindeutig, Mappings zeigen auf vorhandene Module."""
    import re
    ids, refs = [], []

    def walk(flow):
        for m in flow:
            ids.append(m['id'])
            text = json.dumps(m.get('mapper')) + json.dumps(m.get('filter'))
            refs.extend(int(x) for x in re.findall(r'\{\{[^}]*?\b(\d+)\.', text))
            for r in m.get('routes', []):
                walk(r['flow'])
    walk(bp['flow'])
    assert len(ids) == len(set(ids)), ids
    assert set(refs) <= set(ids), (refs, ids)
    return len(ids)
