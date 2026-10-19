"""Tag 10 (Lektion 9: APIs & MCP, Folien 1-33) - wird von kurs.py eingelesen.
Ergaenzt um Fakten aus docs.langdock.com (MCP als Integration) - dort mit 'quelle': 'Langdock'.
Auf den Folien: Folie 29 (PUT) zeigt als Methode "PATCH" - gemeint ist PUT; "Athorization" = Authorization."""
TAG10 = {
    'titel': 'APIs & MCP – wie Software miteinander spricht',
    'unter': 'Lektion 9 · APIs & MCP',
    'datum': '09.10.2026',
    'folien': 'APIs-and-MCP.pdf',
    'kurz': 'Was eine API ist, wie Anfrage, Antwort und Statuscode zusammenspielen, wie man sich ausweist – und wie MCP KI-Agenten mit Werkzeugen und Daten verbindet.',
    'lernheft': 'Lernheft_Tag10_APIs-und-MCP.pdf',
    'praxisheft': 'p10',  # Schluessel in lernheft.HEFTE -> /<person>/tag-10/praxis/
    'videos': [
        {'id': 'cGuyrANVi4A', 'titel': 'How Model Context Protocol (MCP) actually works', 'dauer': '07:58', 'folie': 13,
         'text': 'Kurz erklärt von Google Cloud: wie ein Agent über MCP Werkzeuge findet und aufruft.'},
        {'id': '185XGEMefgc', 'titel': 'MCP vs API: Why traditional APIs are failing AI agents', 'dauer': '12:25', 'folie': 18,
         'text': 'Warum klassische APIs für Agenten unpraktisch sind und was MCP anders macht.'},
    ],
    'learnings': [
        {'id': 'l1', 'folie': 2, 'satz': 'APIs nutzt man längst – meist ohne es zu merken.',
         'erklaert': 'Die Wetter-App holt Echtzeitdaten vom Server, „Mit Google anmelden“ läuft über eine API, Bezahldienste wie Stripe oder PayPal sind APIs, '
                     'und Google Maps liefert Routen per API. Überall sprechen zwei Programme im Hintergrund miteinander.'},
        {'id': 'l2', 'folie': 4, 'satz': 'Eine API ist wie ein Kellner im Restaurant.',
         'erklaert': 'Die App ist der Gast und stellt Anfragen. Die API ist der Kellner: Sie nimmt die Bestellung auf, übersetzt und bringt das Ergebnis. '
                     'Der Server ist die Küche, die alles verarbeitet. Der Gast muss nicht wissen, wie gekocht wird.'},
        {'id': 'l3', 'folie': 5, 'satz': 'Es gibt mehrere API-Standards – im Web ist REST der Standard.',
         'erklaert': 'SOAP (XML, schwergewichtig, eher veraltet, z. B. ELSTER), REST (HTTP + JSON, z. B. Stripe, GitHub), GraphQL (der Client bestimmt die Daten), '
                     'Webhook (der Server meldet sich selbst bei Ereignissen), gRPC (sehr schnell) und WebSocket (dauerhafte Live-Verbindung, z. B. Live-Chat).'},
        {'id': 'l4', 'folie': 6, 'satz': 'Auf jede Anfrage folgt eine Antwort – meist im JSON-Format.',
         'erklaert': 'Die Anfrage (Request) sagt, was man will, z. B. „Gib mir das Wetter in Berlin“. Die Antwort (Response) kommt als strukturierte Daten, '
                     'etwa { "stadt": "Berlin", "temp": 25, "wetter": "sonnig" } – lesbar für Maschinen und Menschen.'},
        {'id': 'l5', 'folie': 32, 'satz': 'Der Statuscode zeigt sofort, ob es geklappt hat.',
         'erklaert': '2xx heißt Erfolg (200 OK, 201 angelegt, 204 gelöscht ohne Inhalt). 4xx heißt: Die Anfrage war fehlerhaft (404 nicht gefunden, '
                     '401 Schlüssel fehlt oder ist ungültig, 429 zu viele Anfragen). 5xx heißt: Fehler auf dem Server (500). Faustregel: 4xx liegt an mir, 5xx am Server.'},
        {'id': 'l6', 'folie': 8, 'satz': 'APIs haben Grenzen: Anfragen pro Minute und Kosten pro Aufruf.',
         'erklaert': 'Das Rate Limit erlaubt nur eine bestimmte Zahl an Anfragen pro Minute – wer mehr schickt, bekommt Fehler 429. '
                     'Viele APIs, besonders KI-APIs, rechnen jeden Aufruf ab. Darum nur abfragen, was man wirklich braucht.'},
        {'id': 'l7', 'folie': 9, 'satz': 'APIs schützen sich mit API-Key oder OAuth 2.0.',
         'erklaert': 'Ein API-Key ist ein persönlicher Zugangscode – einfach einzurichten, aber niemals teilen. OAuth 2.0 erlaubt Zugriff, ohne ein Passwort '
                     'weiterzugeben – das Prinzip hinter „Mit Google anmelden“.'},
        {'id': 'l8', 'folie': 12, 'satz': 'MCP ist der „USB-C-Anschluss“ für KI.',
         'erklaert': 'APIs verbinden Software mit Software. Das Model Context Protocol (MCP) verbindet KI-Modelle und Agenten einheitlich mit Werkzeugen, Daten '
                     'und APIs – ein Standard statt tausender einzelner Anbindungen.'},
        {'id': 'l9', 'folie': 14, 'satz': 'Über MCP fragt der Agent den Server, was er kann – und ruft dann die passenden Werkzeuge auf.',
         'erklaert': 'Der Agent (MCP-Client) hat Modell, Anweisungen und Werkzeuge. Er holt sich vom MCP-Server die Liste der Werkzeuge und ruft sie bei Bedarf auf. '
                     'Der Server erledigt die Arbeit mit Dokumenten, Datenbanken oder anderen Diensten.'},
        {'id': 'l10', 'folie': 15, 'satz': 'MCP tauscht vier Arten von Dingen aus: Werkzeuge, Ressourcen, Prompts und Kontext.',
         'erklaert': 'Werkzeuge (Tools) sind Aktionen wie „Datenbank durchsuchen“ oder „E-Mail senden“. Ressourcen sind Daten wie ein Dokument oder ein Datensatz. '
                     'Prompts sind wiederverwendbare Vorlagen für bestimmte Aufgaben. Kontext sind nützliche Zusatzinfos von außen.'},
        {'id': 'l11', 'folie': 16, 'satz': 'Ein MCP-Server beschreibt sich selbst.',
         'erklaert': 'Fragt das Modell „Was kannst du?“, antwortet z. B. ein Google-Maps-MCP mit seinen Werkzeugen (Orte suchen, Wetter abfragen, Routen berechnen) '
                     '– samt Eingaben und Ausgaben. Automatisch entdeckt, selbstbeschreibend, einheitlich.'},
        {'id': 'l12', 'folie': 17, 'satz': 'Hinter MCP stecken weiter APIs – MCP macht sie für Agenten nutzbar.',
         'erklaert': 'APIs sind für Programme gemacht, die Menschen geschrieben haben. MCP ist für Modelle gemacht, die wie Menschen überlegen. '
                     'Der MCP-Server ist eine Zwischenschicht, die im Hintergrund weiter ganz normale API-Anfragen schickt.'},
        {'id': 'l13', 'folie': 20, 'satz': 'REST: zustandslos, um Ressourcen herum gebaut, Antworten in JSON.',
         'erklaert': 'Zustandslos: Jede Anfrage enthält alles Nötige, der Server merkt sich dazwischen nichts. Ressourcenorientiert: Dinge wie „Bücher“ stehen im '
                     'Mittelpunkt und haben eindeutige Adressen. Antworten meist in JSON.'},
        {'id': 'l14', 'folie': 22, 'satz': 'Fünf HTTP-Methoden setzen CRUD um: Erstellen, Lesen, Ändern, Löschen.',
         'erklaert': 'POST legt Neues an (Create), GET liest (Read), PUT ersetzt komplett und PATCH ändert einzelne Felder (Update), DELETE löscht (Delete). '
                     'CRUD sind die vier Grundoperationen jeder Datenverwaltung.'},
        {'id': 'l15', 'folie': 24, 'satz': 'Ressourcen sind die „Nomen“ einer API – jede hat ihre eigene Adresse.',
         'erklaert': 'Im Buchladen-Beispiel: /buecher steht für alle Bücher, /buecher/42 für genau ein Buch, /kunden für die Kundendaten. '
                     'GET /buecher holt alle, POST /buecher legt ein neues an.'},
        {'id': 'l16', 'folie': 26, 'satz': 'Eine Anfrage besteht aus Methode, Adresse, Ausweis und manchmal Inhalt.',
         'erklaert': 'Methode (z. B. GET), URL mit Parametern (?autor=Goethe&jahr=1808), Authorization (z. B. ein Bearer-Token) und – bei POST, PUT, PATCH – '
                     'ein Body mit den Daten. Zurück kommen Statuscode und JSON. PUT ersetzt alles (fehlende Felder gehen verloren), PATCH ändert nur das Mitgeschickte.'},
        {'id': 'l17', 'folie': 33, 'satz': 'Die Aufgabe: einen Agenten zur Firmenrecherche mit einem MCP-Server erweitern.',
         'erklaert': 'Agent-Vorlage „Unternehmensrecherche“ in Langdock duplizieren und testen, den MCP-Server von handelsregister.ai als Integration verbinden '
                     '(eigener API-Key), Werkzeuge wie get_company_overview, get_financials, get_news, get_website_content auswählen und mit Namen und Parametern '
                     'in die Anweisungen schreiben. Credits und Tokens im Blick behalten.'},
        {'id': 'l18', 'folie': None, 'quelle': 'Langdock', 'satz': 'In Langdock werden MCP-Server als Integration verbunden.',
         'erklaert': 'Laut Langdock-Hilfe: Integrationen → Integration hinzufügen → als Typ MCP wählen, die Server-Adresse eintragen und sich z. B. mit API-Key '
                     'ausweisen. Im Agenten wählt man die Werkzeuge dann unter „Aktionen“ aus. Umgekehrt gibt es auch einen Langdock-MCP-Server, über den andere '
                     'Programme Langdock-Agenten aufrufen.'},
    ],
    'begriffe': [
        ('API', 'Schnittstelle, über die zwei Programme miteinander sprechen – wie ein Kellner zwischen Gast und Küche.'),
        ('Request / Response', 'Anfrage und Antwort: Was man will – und was zurückkommt.'),
        ('JSON', 'Ein einfaches Textformat für Daten in geschweiften Klammern, lesbar für Menschen und Maschinen.'),
        ('Statuscode', 'Die Zahl in der Antwort, die zeigt, ob es geklappt hat (2xx), an der Anfrage lag (4xx) oder am Server (5xx).'),
        ('Rate Limit', 'Höchstzahl an Anfragen pro Zeit – darüber gibt es Fehler 429.'),
        ('API-Key', 'Persönlicher Zugangscode für eine API – nie weitergeben.'),
        ('OAuth 2.0', 'Zugriff erlauben, ohne ein Passwort zu teilen – wie „Mit Google anmelden“.'),
        ('REST', 'Der Standard für Web-APIs: zustandslos, Ressourcen mit eigenen Adressen, Antworten in JSON.'),
        ('CRUD', 'Erstellen, Lesen, Ändern, Löschen – umgesetzt mit POST, GET, PUT/PATCH, DELETE.'),
        ('Webhook', 'Der Server meldet sich von selbst, wenn etwas passiert – statt dass man ständig nachfragt.'),
        ('MCP', 'Model Context Protocol: einheitlicher Anschluss, über den KI-Agenten Werkzeuge und Daten nutzen.'),
        ('MCP-Server', 'Stellt Werkzeuge bereit, beschreibt sich selbst und spricht im Hintergrund mit APIs.'),
    ],
    'karten': [
        ('Wofür steht der Kellner im API-Vergleich?', 'Für die API: Sie nimmt die Anfrage vom Gast (App) auf und bringt das Ergebnis aus der Küche (Server).'),
        ('Welcher API-Standard ist im Web am verbreitetsten?', 'REST – über HTTP, mit Antworten in JSON.'),
        ('In welchem Format kommen die meisten Antworten?', 'In JSON – strukturierte Daten in geschweiften Klammern.'),
        ('Was bedeuten 2xx, 4xx und 5xx?', '2xx Erfolg, 4xx Fehler in der Anfrage (Client), 5xx Fehler auf dem Server.'),
        ('Was bedeutet Fehler 429?', 'Zu viele Anfragen – das Rate Limit ist überschritten.'),
        ('API-Key oder OAuth: Wo teilt man kein Passwort?', 'Bei OAuth 2.0 – Zugriff erlauben, ohne ein Passwort weiterzugeben.'),
        ('Warum nennt man MCP den „USB-C-Anschluss“ für KI?', 'Ein einheitlicher Standard verbindet KI mit vielen Werkzeugen – statt tausender Einzel-Anbindungen.'),
        ('Welche vier Dinge tauscht MCP aus?', 'Werkzeuge, Ressourcen, Prompts und Kontext.'),
        ('Ersetzt MCP die APIs?', 'Nein. Der MCP-Server schickt im Hintergrund weiter API-Anfragen – er macht sie für Agenten nutzbar.'),
        ('Welche Methode für welche Aufgabe?', 'GET lesen, POST anlegen, PUT komplett ersetzen, PATCH einzelne Felder ändern, DELETE löschen.'),
        ('PUT oder PATCH, um nur den Preis zu ändern?', 'PATCH – PUT würde alle nicht mitgeschickten Felder überschreiben.'),
        ('Wie bindet man in Langdock einen MCP-Server an?', 'Integrationen → Integration hinzufügen → MCP, Adresse und Schlüssel eintragen; im Agenten unter „Aktionen“ auswählen.'),
    ],
    'test': [
        {'frage': 'Im Kellner-Vergleich: Wer ist die Küche?',
         'optionen': ['Die App', 'Die API', 'Der Server'], 'richtig': 2,
         'warum': 'App = Gast, API = Kellner, Server = Küche, die verarbeitet und liefert (Folie 4).'},
        {'frage': 'Eine Anfrage liefert den Statuscode 404. Was bedeutet das?',
         'optionen': ['Alles gut', 'Die Ressource wurde nicht gefunden', 'Der Server ist abgestürzt'], 'richtig': 1,
         'warum': '404 = Not Found. 4xx-Fehler liegen an der Anfrage, nicht am Server.'},
        {'frage': 'Welche Methode ändert nur den Preis eines Buchs, ohne den Rest zu überschreiben?',
         'optionen': ['PUT', 'PATCH', 'DELETE'], 'richtig': 1,
         'warum': 'PATCH ändert nur die mitgeschickten Felder. PUT ersetzt das ganze Objekt.'},
        {'frage': 'Was gehört NICHT in einen Chat oder eine E-Mail?',
         'optionen': ['Ein JSON-Beispiel', 'Der eigene API-Key', 'Ein Statuscode'], 'richtig': 1,
         'warum': 'Ein API-Key ist ein persönlicher Zugangscode – niemals teilen (Folie 9).'},
        {'frage': 'Was macht ein MCP-Server?',
         'optionen': ['Er ersetzt alle APIs', 'Er macht Werkzeuge und APIs für KI-Agenten einheitlich nutzbar', 'Er speichert nur Passwörter'], 'richtig': 1,
         'warum': 'Im Hintergrund laufen weiter API-Anfragen – MCP ist die Zwischenschicht für Agenten (Folie 17).'},
        {'frage': 'Ein Shop meldet sich bei jeder neuen Bestellung von selbst bei deinem System. Welcher Standard ist das?',
         'optionen': ['Webhook', 'SOAP', 'GraphQL'], 'richtig': 0,
         'warum': 'Beim Webhook meldet sich der Server bei einem Ereignis selbst (Folie 5).'},
    ],
}
