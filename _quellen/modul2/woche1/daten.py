"""Lerndaten für den Learning Hub Modul 2 · Woche 1 (interne Tag-Kennung 24).

Folien im gemeinsamen Viewer: 1–34 = Make-Lektion (Tag 1–4), 35–66 = Use Cases (Tag 5).
"""
MAKE_N = 34
UC_N = 32
DATUM = '30.10.2026'
TAG = 24
LERNHEFT = 'Wochenheft_Modul2_Woche1_Make-und-Use-Cases.pdf'


def U(n):
    """Use-Case-Folie n im gemeinsamen Viewer."""
    return MAKE_N + n


def folie_label(n):
    return f'Make-Folie {n}' if n <= MAKE_N else f'Use-Case-Folie {n - MAKE_N}'


# (id, folie, tag, satz, erklaert)
LEARNINGS = [
 ('l1', 4, 1, 'KI-Automation heißt hier: ein festes Gerüst, in dem an einzelnen Stellen eine KI arbeitet.',
  'Der Weg steht vorher fest: was den Ablauf startet, welche Schritte folgen und was am Ende herauskommt. Nur dort, wo früher ein Mensch lesen und beurteilen musste – einordnen, zusammenfassen, Angaben aus Freitext ziehen, formulieren – sitzt ein Sprachmodell. Der Rest ist normale Datenarbeit. So bleibt der Ablauf kontrollierbar, testbar und wiederholbar.'),
 ('l2', 5, 1, 'Ein Agent plant den Weg selbst – ein Workflow folgt immer demselben vorgezeichneten Weg.',
  'Agentisch (z. B. Claude Cowork): Du nennst ein Ziel, das Modell wählt Werkzeuge und Reihenfolge erst während der Arbeit. Flexibel, aber schwer zu wiederholen und zu prüfen. Workflow (Make, n8n, Zapier): Du zeichnest die Schritte vorher. Jeder Durchlauf nimmt dieselbe Strecke – gut für gleichförmige Aufgaben mit viel Menge. Im Kurs meint „KI-Automatisierung“ ab jetzt immer den Workflow.'),
 ('l3', 6, 1, 'Jeder Workflow hat vier Teile: Auslöser → Daten holen → Verarbeiten → Ergebnis erzeugen.',
  'Egal ob Make, n8n oder Zapier – das Grundmuster ist gleich, nur die Wörter unterscheiden sich. Beispiel: Neue Anfrage kommt an (Auslöser) → Angaben aus der Mail lesen (Daten holen) → einordnen (Verarbeiten) → Zeile in einer Tabelle (Ergebnis).'),
 ('l4', 7, 1, 'Trigger startet, Modul arbeitet, Mapping verbindet, Execution ist ein Durchlauf.',
  'Trigger: das Ereignis, das startet (Zeitplan, Webhook, manueller Start). Modul: ein einzelner Arbeitsschritt (n8n sagt Node, Zapier Step). Mapping: Felder von einem Schritt in den nächsten einsetzen – laut Folie die häufigste Fehlerquelle überhaupt. Execution: ein Durchlauf; hier wird abgerechnet und im Fehlerfall nachgelesen.'),
 ('l5', 8, 1, 'KI-Schritte streuen. Feste Auswahl, festes Format und wiederholte Tests machen sie verlässlicher.',
  'Ein Sprachmodell wählt Wort für Wort nach Wahrscheinlichkeit. Darum kommt derselbe Lieferant mal als „Musterbau GmbH“, mal als „Musterbau“ heraus – drei Schreibweisen ergeben drei Datensätze. Die Temperatur senkt die Streuung, aber nie auf null. Gegenmittel: erlaubte Werte vorgeben, Antwort als JSON verlangen und prüfen, dieselbe Eingabe zehnmal testen und ein Feld „unsicher“ mitliefern lassen.'),
 ('l6', 10, 1, 'Erst Betriebsmodell und Team klären, dann ein einziges Werkzeug wählen.',
  'Leitfragen der Folie: Selbst betreiben oder Cloud-Dienst? Wer kann es technisch? (ohne Technik: Zapier/Langdock, mit einer technischen Person: Make, mit Entwicklung: n8n). Abrechnung verstehen: Zapier pro Task, Make nach Operationen bzw. heute Credits, n8n Cloud pro Ausführung – Modellkosten kommen dazu. Geeignet sind wiederkehrende, beschreibbare Abläufe mit klaren Eingängen, genug Menge und prüfbarem Ergebnis.'),
 ('l7', 11, 1, 'Klein anfangen, mit Ausreißern testen und Fehler aktiv melden lassen.',
  'Der erste Workflow hat 5–7 Schritte, nicht den kompliziertesten Prozess. Getestet wird auch mit leeren Feldern, Sonderzeichen und falschen Formaten. Es gibt einen Fehlerweg mit Wiederholung, eine Benachrichtigung und getrennte Test- und Echtumgebungen. Typische Fehler: zu groß anfangen, alles per KI lösen, Fließtext statt fester Felder weiterreichen, nach dem Start keine Stichproben.'),
 ('l8', None, 1, 'Make Free: 1.000 Credits im Monat. Zeitplan aus lassen und bewusst mit „Run once“ testen.',
  'Ein normales Modul verbraucht pro Arbeitsgang meist 1 Credit; Router und Filter selbst kosten nichts, KI-Module können mehr kosten. Free erlaubt zwei aktive Szenarien und Zeitpläne ab 15 Minuten. Eine Abfrage alle 15 Minuten würde 2.880 Credits im Monat allein fürs Nachsehen verbrauchen – deshalb üben wir nur mit Einzelstarts. Maßgeblich ist die Anzeige im eigenen Konto.'),
 ('l9', 12, 2, 'Die Folienübung Outlook → Excel zeigt das ganze Handwerk: Trigger, Action, Mapping, Test, Zeitplan, History.',
  'Jede neue Mail (Microsoft 365 Email › Watch Emails) wird als Zeile in eine echte Excel-Tabelle geschrieben (Excel › Add a Table Row). Wichtig: Der Bereich in Excel muss als Tabelle formatiert sein, sonst findet Make das Ziel nicht. Dafür braucht man ein Microsoft-365-Konto. Unsere Vorlagen üben dieselben Handgriffe ohne fremdes Konto.'),
 ('l10', 24, 2, 'JSON ist ein beschrifteter Zettel: links der Feldname, rechts der Wert.',
  'JSON (JavaScript Object Notation) ist ein leichtes, für Menschen lesbares Datenformat. Systeme und KI-Modelle tauschen darüber Daten aus. Vorteil für Automationen: feste, gleich aufgebaute Antworten, die sich einfach zerlegen lassen.'),
 ('l11', 25, 2, 'Sechs JSON-Typen: String, Number, Boolean, Null, Object, Array.',
  'String = Text in Anführungszeichen ("Produkt X"). Number = Zahl ohne Anführungszeichen (123, 3.14). Boolean = true oder false. Null = absichtlich leer (nicht dasselbe wie ""). Object = Sammlung von Feldern in { }. Array = geordnete Liste in [ ].'),
 ('l12', 26, 2, 'Variablen tragen Werte von Schritt zu Schritt. Daten wandern als Päckchen (Bundles) durch den Ablauf.',
  'Eine Variable ist ein Platzhalter für einen Wert, der sich je Durchlauf ändert. Make und n8n machen aus JSON automatisch Felder, die man im nächsten Modul einsetzt (mappt). Jedes Modul bekommt ein Päckchen, verarbeitet es und gibt ein neues weiter.'),
 ('l13', 27, 2, 'Parse JSON macht aus JSON-Text einzelne Felder, die man mappen kann.',
  'Kommt eine KI-Antwort als JSON-Text an, zerlegt JSON › Parse JSON sie in betreff, kategorie, prioritaet … Danach kann jedes Feld einzeln weiterverwendet werden. Ist der Text kein gültiges JSON, stoppt das Modul mit einem Fehler – das ist gewollt.'),
 ('l14', 28, 3, 'Ein Filter ist eine Tür (weiter oder Stopp), ein Router ist eine Weiche (mehrere Wege).',
  'Filter prüfen Daten an einer Stelle; nur passende gehen weiter. Das spart Kosten, weil unnötige KI-Schritte gar nicht erst laufen. Router teilen einen Ablauf in mehrere Wege, z. B. Anfragen nach Abteilung. Jeder Weg hat seinen eigenen Filter – passen mehrere, laufen mehrere Wege.'),
 ('l15', 29, 3, 'AND heißt: alle Bedingungen müssen stimmen. OR heißt: mindestens eine.',
  'Vergleichsoperatoren prüfen zwei Werte: gleich, ungleich, größer, kleiner, enthält. Logische Operatoren verbinden Bedingungen: AND (alle wahr) oder OR (mindestens eine wahr).'),
 ('l16', 17, 3, 'Ein Webhook meldet sich sofort (Push). Polling fragt immer wieder nach (Pull).',
  'Ein Webhook ist eine automatische Nachricht an eine feste Adresse, sobald etwas passiert (z. B. Formular abgeschickt). Das ist schneller und sparsamer als regelmäßiges Nachfragen. Eine API muss man dagegen ausdrücklich anfragen.'),
 ('l17', 30, 3, 'System-Prompt = Rolle und Regeln. User-Prompt = konkrete Eingabe. Assistant = Antwort des Modells.',
  'Der System-Prompt legt Identität, Ton und Regeln fest und gilt für jede Antwort. Der User-Prompt ist die konkrete Frage. Die Assistant-Antwort wird Teil des Verlaufs. In der API kommen alle drei als Liste von messages mit role und content.'),
 ('l18', 18, 3, 'Die große Folienübung: Formular → KI ordnet ein → JSON zerlegen → Router verteilt.',
  'Tally-Formular startet sofort, Mistral liefert ein festes JSON (betreff, body_text, kategorie, prioritaet), Parse JSON zerlegt es, eine Bestätigung geht raus, der Router verteilt an Vertrieb, Support oder Marketing. Braucht vier zusätzliche Konten und einen API-Schlüssel. Vor echten Mails an Kundschaft gehört eine menschliche Prüfung dazu.'),
 ('l19', None, 4, 'HTTP GET liest Daten. Status 200 heißt: Abruf hat geklappt – nicht: Inhalt ist richtig.',
  'Eine API ist eine vereinbarte Adresse für Daten, HTTP der Weg dorthin. GET liest nur. Der Statuscode sagt, ob der Abruf technisch klappte (200 = ok, 404 = nicht gefunden). Ob die gelesenen Daten fachlich stimmen, ist eine zweite Frage.'),
 ('l20', 32, 4, 'ISO 8601 mit Z oder Offset ist eindeutig. Ohne Zeitzone drohen Stunden-Verschiebungen.',
  '2026-07-29T14:35:07Z: Datum, T als Trenner, Uhrzeit, Z = UTC. +02:00 heißt zwei Stunden vor UTC (Sommerzeit Berlin), im Winter gilt +01:00. Ohne Z oder Offset ist der Zeitpunkt mehrdeutig. ISO 8601 nutzt immer 24 Stunden.'),
 ('l21', 34, 4, 'formatDate macht aus einem Zeitpunkt lesbaren Text – in der richtigen Zeitzone.',
  'formatDate(now; "DD.MM.YYYY HH:mm"; "Europe/Berlin") ergibt z. B. 30.10.2026 10:00. Für Menschen ist das deutsche Format richtig, für APIs und Vergleiche das Format, das das Zielfeld erwartet – meist ISO 8601.'),
 ('l22', U(6), 5, '„95 % ohne messbaren Effekt“ ist nicht dasselbe wie „abgebrochen“. Zahlen genau lesen.',
  'MIT NANDA (2025) misst generative KI-Piloten ohne nachweisbaren Effekt auf das Geschäftsergebnis – oft, weil vorher kein Ausgangswert erhoben wurde. Gartner prognostiziert, dass über 40 % der agentenbasierten Projekte bis Ende 2027 abgebrochen werden. Zwei verschiedene Messgrößen, nicht addierbar. Gemeinsam: Das Modell war nie die Hauptursache.'),
 ('l23', U(7), 5, 'Projekte scheitern an Ziel, Messung, Daten, Zuständigkeit und Betrieb – nicht am Modell.',
  'Die fünf Ursachen: unklares Ziel, keine Erfolgskriterien, Daten nicht maschinell verfügbar, Recht und Zuständigkeit zu spät geprüft, niemand verantwortet den Betrieb. „Das Modell war zu schwach“ ist auf der Folie ausdrücklich durchgestrichen. Erfolgreiche Projekte entscheiden vorher: gestufte Autonomie, Freigaben nach Umkehrbarkeit, ROI-Prüfpunkte, ein benannter Eigentümer.'),
 ('l24', U(9), 5, 'Zeitfresser werden gerechnet, nicht gefühlt: Häufigkeit × Minuten je Vorgang.',
  'Jede Tätigkeit, die mindestens wöchentlich vorkommt, mit Häufigkeit pro Monat, Minuten je Vorgang, Anzahl Systeme und Fehleranfälligkeit notieren. Erst rechnen, dann sortieren. Die nervigste Aufgabe ist selten die teuerste.'),
 ('l25', U(11), 5, 'Ein Use-Case braucht alle drei: echtes Problem, abgrenzbaren KI-Teil, messbaren Mehrwert.',
  'Fehlt der messbare Mehrwert, ist es ein Bauchgefühl-Projekt. Fehlt der KI-Teil, ist es eine Prozessverbesserung. Fehlt das echte Problem, sucht eine Technik eine Anwendung. Fast jeder Fall startet in einer dieser Zwischenzonen.'),
 ('l26', U(13), 5, 'Die Ebene entscheidet über die Kennzahl: Aufgabe → Sekunden, Prozess → Durchlaufzeit, Use-Case → Geschäftswirkung.',
  'Wer nur eine Aufgabe beschleunigt, aber die Wartezeit davor und danach lässt, ändert für das Unternehmen nichts. Wer Geschäftswirkung verspricht, muss sie auch messen – nicht nur Sekunden pro Vorgang.'),
 ('l27', U(15), 5, 'Gute Use-Cases sind korrigierbar, haben einen Eigentümer und genug Volumen.',
  'Neben den sechs bekannten Merkmalen (abgegrenzt, datenbasiert, umsetzbar, messbar, wiederholbar, im Unternehmen verankert) fehlen oft drei: Fehler bleiben folgenlos oder werden bemerkt, eine benannte Person steht für die Ergebnisse gerade, und der Ablauf kommt oft genug vor.'),
 ('l28', U(17), 5, 'Im Steckbrief ist Nutzen immer Zahl + Einheit + Zeitraum.',
  '„Spart 30 Stunden im Monat in der Buchhaltung“ zählt, „spart Zeit“ nicht. Felder, die du nicht füllen kannst, markierst du – leere Felder sind ein Ergebnis, kein Versagen.'),
 ('l29', U(20), 5, 'Autonomie hat fünf Stufen (0–4) und wird pro Pfad festgelegt, nicht pro Workflow.',
  '0 manuell, 1 Assistenz, 2 Mensch gibt jeden Fall frei, 3 System entscheidet mit Stichproben, 4 ohne Aufsicht. Häufiges gutes Muster: Standardfall Stufe 3, Ausnahme Stufe 2. Wer 200 Vorschläge am Tag durchklickt, ist faktisch Stufe 4. Für Endentscheidungen über Menschen ist Stufe 4 nicht zulässig.'),
 ('l30', U(22), 5, 'Erst Regel, dann KI an einer Stelle, Agent zuletzt. KI liest – die Regel entscheidet.',
  'Treppe: Lässt sich die Entscheidung als Regel formulieren? → fester Workflow. Reicht ein Modell an genau einer Stelle? → Sprachmodell im Workflow. Wechseln Werkzeuge und Reihenfolge je Fall? → Agent. Beispiel Rechnung: Das Modell liest vier Felder, eine feste Regel entscheidet über die Freigabe. Ändert sich die Grenze, ändert sich nur eine Zahl.'),
 ('l31', U(24), 5, 'Use-Cases findet man systematisch: Zeitfresser, Prozess-Inventur, Schmerz-Interviews, Datenspuren.',
  'Ein Brainstorming liefert, was gerade in Artikeln steht. Besser: eine Woche Tätigkeiten mitschreiben, Kernprozesse mit Volumen und Fehlerhäufigkeit schätzen, Kolleginnen und Kollegen befragen und Postfächer oder Tickets auswerten. Zehn bis fünfzehn grobe Kandidaten sind ein gutes Ergebnis.'),
 ('l32', U(27), 5, 'Bei HR, Marketing und Vertrieb die rechtlichen Fallstricke früh prüfen.',
  'Bewerbungen bewerten oder ranken gilt nach der EU-KI-Verordnung in der Regel als Hochrisiko. Vollautomatische Absagen sind nach Art. 22 DSGVO grundsätzlich unzulässig. Tragfähig: KI strukturiert, ein Mensch bewertet. Bei veröffentlichten KI-Inhalten, Lead-Scoring und Werbemails Kennzeichnung, Datenschutz und Werberecht vorher klären.'),
 ('l33', U(30), 5, 'Fünf Ausschlusskriterien kommen vor jeder Rechnung.',
  'Kein Zugriff auf die Daten, kein Verantwortlicher im Fachbereich, rechtlich unzulässiges Ziel, kein definierbarer richtiger Output, Prozess wird gerade umgestellt. Wer hier durchfällt, wird gar nicht erst bewertet.'),
]

KARTEN = [
 ('Was ist KI-Automatisierung nach der Kursdefinition?', 'Ein vorab festgelegter, wiederholbarer Ablauf, der durch ein Ereignis startet und an einzelnen Stellen ein Sprachmodell nutzt.'),
 ('Woran unterscheidest du Agent und Workflow?', 'Wer den Weg bestimmt: Beim Agenten plant das Modell zur Laufzeit, beim Workflow steht der Weg vorher fest.'),
 ('Nenne die vier Teile jedes Workflows.', 'Auslöser → Daten holen → Verarbeiten → Ergebnis erzeugen.'),
 ('Was ist Mapping?', 'Felder aus einem früheren Schritt in einen späteren einsetzen. Laut Folie die häufigste Fehlerquelle.'),
 ('Was ist eine Execution?', 'Ein einzelner Durchlauf. Dort wird abgerechnet und im Fehlerfall nachgelesen.'),
 ('Vier Mittel gegen streuende KI-Antworten?', 'Feste Auswahl statt Freitext, JSON-Format prüfen, dieselbe Eingabe oft testen, Feld „unsicher“ mitliefern lassen.'),
 ('Wie viele Credits hat Make Free im Monat?', '1.000 Credits. Dazu zwei aktive Szenarien und Zeitpläne ab 15 Minuten.'),
 ('Warum lassen wir den Zeitplan aus?', 'Jede Abfrage kostet Credits – alle 15 Minuten wären 2.880 Credits im Monat nur fürs Nachsehen.'),
 ('Wo startest du einen Test in Make?', 'Mit „Run once“ im Scenario Builder.'),
 ('Wo siehst du das Ergebnis eines Moduls?', 'In der kleinen Sprechblase über dem Modul nach dem Lauf: OUTPUT.'),
 ('Was ist ein Blueprint?', 'Eine JSON-Datei mit Modulen, Einstellungen und Mappings eines Szenarios – zum Exportieren und Importieren.'),
 ('Wie importierst du einen Blueprint?', 'Neues Szenario → drei Punkte oben rechts → Import blueprint → Datei wählen → Save.'),
 ('Was macht Tools › Set variable?', 'Es legt einen Wert unter einem Namen bereit, z. B. vorname = Luna.'),
 ('Was macht Tools › Compose a string?', 'Es baut einen Text aus festen Wörtern und gemappten Werten.'),
 ('Was ist JSON?', 'Ein lesbares Datenformat aus Feldnamen und Werten, z. B. {"projekt": "Papierfunke"}.'),
 ('Unterschied zwischen null und ""?', 'null heißt absichtlich kein Wert, "" ist ein leerer Text.'),
 ('Ist "true" in Anführungszeichen ein Boolean?', 'Nein, das ist Text. Ein Boolean ist true oder false ohne Anführungszeichen.'),
 ('Was macht Parse JSON?', 'Es zerlegt JSON-Text in einzelne Felder, die man mappen kann.'),
 ('Was ist ein Bundle?', 'Ein Datenpäckchen, das durch die Module wandert. Mehr Bundles können mehr Arbeitsgänge auslösen.'),
 ('Filter oder Router: Was ist die Tür, was die Weiche?', 'Filter = Tür (weiter/Stopp), Router = Weiche (mehrere Wege).'),
 ('Kosten Router und Filter Credits?', 'Selbst nicht. Die Module dahinter können Credits verbrauchen.'),
 ('AND oder OR: Wann reicht eine erfüllte Bedingung?', 'Bei OR. Bei AND müssen alle stimmen.'),
 ('Webhook oder Polling: Was ist Push?', 'Der Webhook – er meldet sich sofort, wenn etwas passiert.'),
 ('Was steht im System-Prompt?', 'Rolle, Ton und Regeln für das Modell. Er gilt für jede Antwort.'),
 ('Was bedeutet HTTP-Status 200?', 'Der Abruf hat technisch geklappt. Ob der Inhalt stimmt, ist eine eigene Frage.'),
 ('Was bedeutet das Z in 2026-07-29T14:35:07Z?', 'UTC (Zulu-Zeit, +00:00).'),
 ('Welche Uhrzeit ist 2026-10-30T09:00:00Z in Berlin?', '10:00 Uhr – Ende Oktober gilt Winterzeit (+01:00).'),
 ('Wofür steht formatDate in Make?', 'Es formatiert einen Zeitpunkt als Text, z. B. "DD.MM.YYYY HH:mm" in "Europe/Berlin".'),
 ('Woran scheitern KI-Projekte laut Folie meistens?', 'An Ziel, Erfolgskriterien, Datenlage, Governance und Betrieb – nicht am Modell.'),
 ('Wie rechnest du einen Zeitfresser?', 'Häufigkeit pro Monat × Minuten je Vorgang = Minuten pro Monat.'),
 ('Drei Bedingungen für einen echten Use-Case?', 'Echtes Problem, abgrenzbarer KI-Teil, messbarer Mehrwert.'),
 ('Welche Kennzahl gehört zur Ebene „Prozess“?', 'Durchlaufzeit und Fehlerquote.'),
 ('Wie sieht ein gutes Nutzenfeld aus?', 'Zahl + Einheit + Zeitraum, z. B. „15 Stunden pro Monat im Innendienst“.'),
 ('Was heißt Stufe 2 (Human-in-the-Loop)?', 'Ein Mensch gibt jeden einzelnen Fall frei.'),
 ('Was ist das häufigste gute Autonomie-Muster?', 'Standardfall auf Stufe 3, Ausnahme auf Stufe 2.'),
 ('Wann ist eine Bestätigung nur scheinbar Stufe 2?', 'Wenn die Person keine Zeit oder Information zum Widersprechen hat – wer 200 Fälle durchklickt, ist faktisch Stufe 4.'),
 ('Was fragst du zuerst auf der Entscheidungstreppe?', 'Ob sich die Entscheidung als Regel formulieren lässt – dann reicht ein fester Workflow ohne KI.'),
 ('Rechnungsbeispiel: Wer liest, wer entscheidet?', 'Das Sprachmodell liest vier Felder, eine feste Regel entscheidet über die Freigabe.'),
 ('Vier Zugänge, um Use-Cases zu finden?', 'Zeitfresser-Analyse, Prozess-Inventur, Schmerz-Interviews, Datenspuren auswerten.'),
 ('Nenne zwei Ausschlusskriterien.', 'Z. B. kein Datenzugriff, kein Verantwortlicher, rechtlich unzulässig, kein richtiger Output definierbar, Prozess wird umgestellt.'),
]

# (frage, optionen, richtig, warum)
TEST = [
 ('Was ist nach der Kursdefinition KI-Automatisierung?',
  ['Ein Agent plant selbst, welche Werkzeuge er nimmt', 'Ein fester Ablauf mit KI an einzelnen Stellen', 'Jede Nutzung eines Chatbots'], 1,
  'Das Gerüst ist deterministisch, die KI sitzt nur dort, wo früher ein Mensch lesen und beurteilen musste.'),
 ('Du willst eine Vorlage testen. Was schonst du dein Credit-Budget am besten?',
  ['Zeitplan auf 15 Minuten stellen', 'Mit Run once einzeln starten', 'Das Szenario auf Active schalten'], 1,
  'Einzelstarts kosten nur, wenn du sie auslöst. Ein Zeitplan fragt auch dann ab, wenn nichts passiert.'),
 ('In Baustein 2 steht trotz Namenswechsel immer „Luna“. Was ist die wahrscheinlichste Ursache?',
  ['Der Name wurde fest eingetippt statt gemappt', 'Make hat keine Credits mehr', 'Der Browser ist zu alt'], 0,
  'Nur eine gemappte Kachel übernimmt den neuen Wert aus Baustein 1.'),
 ('Welcher Wert ist ein JSON-Boolean?',
  ['"true"', 'true', '"ja"'], 1, 'Boolean-Werte stehen ohne Anführungszeichen. "true" ist Text.'),
 ('Wozu brauchst du Parse JSON?',
  ['Um JSON-Text in einzelne Felder zu zerlegen', 'Um eine Mail zu verschicken', 'Um Credits zu sparen'], 0,
  'Erst nach dem Zerlegen kannst du jedes Feld einzeln mappen.'),
 ('Ein Filter verlangt kategorie = VIDEO AND freigabe = true. Was passiert bei VIDEO und false?',
  ['Es geht weiter', 'Der Weg stoppt am Filter', 'Make ändert false in true'], 1,
  'Bei AND müssen beide Bedingungen stimmen.'),
 ('Was beschreibt einen Webhook richtig?',
  ['Make fragt alle 15 Minuten nach', 'Die andere Anwendung meldet sich sofort bei einer festen Adresse', 'Ein Modell plant den Weg selbst'], 1,
  'Webhooks sind Push: Das Ereignis löst die Nachricht sofort aus.'),
 ('Die Test-API liefert Status 200 und completed = false. Was heißt das?',
  ['Der Abruf ist fehlgeschlagen', 'Der Abruf hat geklappt, die Testaufgabe ist laut Daten unerledigt', 'Make hat einen Fehler gemacht'], 1,
  'Technischer Status und Inhalt der Daten sind zwei verschiedene Dinge.'),
 ('Welche Angabe ist eindeutig?',
  ['2026-07-29T14:35:07', '29.07.2026 14:35', '2026-07-29T14:35:07Z'], 2,
  'Nur mit Z oder Offset ist klar, welche Zeitzone gemeint ist.'),
 ('Welches Nutzenfeld gehört in einen Steckbrief?',
  ['Spart viel Zeit', 'Spart 15 Stunden pro Monat im Innendienst', 'Macht alle glücklicher'], 1,
  'Nutzen braucht Zahl, Einheit und Zeitraum – sonst kann man ihn nicht prüfen.'),
 ('Eine Person bestätigt täglich 200 KI-Vorschläge, ohne sie prüfen zu können. Welche Stufe ist das faktisch?',
  ['Stufe 2', 'Stufe 4', 'Stufe 0'], 1,
  'Echte Stufe 2 heißt: Die Person kann tatsächlich prüfen und hat Zeit dafür. Sonst entscheidet faktisch das System.'),
 ('Eine Entscheidung lässt sich als klare Regel schreiben, der Input ist strukturiert. Was nimmst du?',
  ['Einen Agenten', 'Ein Sprachmodell an jeder Stelle', 'Einen festen Workflow mit Regeln'], 2,
  'Beim ersten Ja auf der Treppe stehen bleiben: deterministisch, testbar, im Betrieb praktisch kostenlos.'),
]

# (begriff, erklärung)
BEGRIFFE = [
 ('Szenario', 'Ein ganzer Ablauf in Make – von Auslöser bis Ergebnis.'),
 ('Modul', 'Ein einzelner Arbeitsschritt in Make. In n8n heißt das Node, in Zapier Step.'),
 ('Trigger (Auslöser)', 'Das Ereignis, das den Ablauf startet: Zeitplan, Webhook oder manueller Start.'),
 ('Action', 'Ein Schritt, der etwas tut, z. B. eine Zeile anlegen oder einen Text bauen.'),
 ('Mapping', 'Einen Wert aus einem früheren Modul in ein späteres Feld einsetzen.'),
 ('Execution / Lauf', 'Ein einzelner Durchlauf des Szenarios.'),
 ('Run once', 'Knopf, mit dem du das Szenario genau einmal von Hand startest.'),
 ('History', 'Liste früherer Läufe mit Status und Verbrauch.'),
 ('Credit', 'Make-Abrechnungseinheit. Ein normales Modul braucht pro Arbeitsgang meist 1 Credit.'),
 ('Operation', 'Ein Arbeitsgang eines Moduls mit einem Datenpäckchen.'),
 ('Bundle', 'Ein Datenpäckchen, das von Modul zu Modul wandert.'),
 ('Blueprint', 'JSON-Datei eines ganzen Szenarios zum Teilen, Sichern und Importieren.'),
 ('JSON', 'Lesbares Datenformat aus Feldnamen und Werten in geschweiften Klammern.'),
 ('String', 'JSON-Typ für Text in Anführungszeichen.'),
 ('Number', 'JSON-Typ für Zahlen ohne Anführungszeichen.'),
 ('Boolean', 'JSON-Typ für true oder false.'),
 ('Null', 'Absichtlich kein Wert – nicht dasselbe wie leerer Text.'),
 ('Object', 'Sammlung von Feldern in { }.'),
 ('Array', 'Geordnete Liste von Werten in [ ].'),
 ('Parse JSON', 'Make-Modul, das JSON-Text in einzelne Felder zerlegt.'),
 ('Variable', 'Platzhalter für einen Wert, der sich je Lauf ändern kann.'),
 ('Filter', 'Prüfstelle auf einer Verbindung: Nur passende Daten gehen weiter.'),
 ('Router', 'Weiche, die einen Ablauf in mehrere Wege teilt.'),
 ('AND / OR', 'AND: alle Bedingungen müssen stimmen. OR: eine reicht.'),
 ('Webhook', 'Adresse, an die eine Anwendung sofort Daten schickt, wenn etwas passiert.'),
 ('Polling', 'Regelmäßiges Nachfragen, ob es Neues gibt.'),
 ('API', 'Vereinbarte Schnittstelle, über die Programme Daten austauschen.'),
 ('HTTP GET', 'Anfrage, die Daten nur liest.'),
 ('Statuscode', 'Zahl, die sagt, ob der Abruf geklappt hat (200 ok, 404 nicht gefunden).'),
 ('ISO 8601', 'Internationales Datumsformat, z. B. 2026-10-30T09:00:00Z.'),
 ('UTC / Z', 'Weltzeit ohne Verschiebung. Das Z am Ende eines Zeitstempels heißt UTC.'),
 ('System-Prompt', 'Feste Anweisung an die KI zu Rolle, Ton und Regeln.'),
 ('Strukturierter Output', 'KI-Antwort als JSON mit festen Feldern statt Fließtext.'),
 ('Human-in-the-Loop', 'Fester Haltepunkt, an dem ein Mensch freigibt.'),
 ('Use-Case', 'Echtes Problem + abgrenzbarer KI-Teil + messbarer Mehrwert.'),
 ('Zeitfresser', 'Wiederkehrende Tätigkeit, gerechnet als Häufigkeit × Minuten.'),
 ('Steckbrief', 'Raster mit elf Feldern, das eine Idee zu einem prüfbaren Use-Case macht.'),
 ('Autonomie-Stufe', 'Wie viel das System allein entscheiden darf: Stufe 0 bis 4.'),
 ('Eigentümer', 'Benannte Person im Fachbereich, die für die Ergebnisse geradesteht.'),
 ('Ausschlusskriterium', 'Grund, einen Kandidaten gar nicht erst zu bewerten.'),
]

# Klassenbuch (Plan nach Folien, nicht Protokoll des tatsächlichen Unterrichts)
KLASSENBUCH = [
 ('Montag, 26.10.2026', 'Einführung in die KI-Automatisierung mit Make', [
  'Grundlagen der KI-Automatisierung und Abgrenzung zu agentischen Arbeitsweisen',
  'Anatomie eines Workflows: Trigger, Module, Mapping und Ausführungen',
  'Streuung von KI-Schritten und Gegenmaßnahmen wie strukturierte Ausgaben',
  'Werkzeugauswahl, Kostenmodelle und Eignung von Prozessen für Automatisierung',
  'Einrichtung von Make Free, Creditbudget und erster Workflow mit Variablen']),
 ('Dienstag, 27.10.2026', 'Daten, JSON und Mapping in Make', [
  'Praktische Übung: Trigger, Action, Mapping, Test und Aktivierung eines Workflows',
  'JSON als Datenformat für KI-Workflows und die elementaren Datentypen',
  'Variablen, Datenfluss und Datenpakete (Bundles) zwischen Modulen',
  'Daten mit Parse JSON zerlegen und in Folgemodulen weiterverwenden',
  'Test mit veränderten Eingaben und nachvollziehbare Dokumentation']),
 ('Mittwoch, 28.10.2026', 'Filter, Router und KI im Workflow', [
  'Filter und Router zur Steuerung des Datenflusses',
  'Vergleichsoperatoren sowie logische Verknüpfungen mit AND und OR',
  'Webhooks im Vergleich zu Polling und API-Abfragen',
  'System-, User- und Assistant-Prompts für KI-Schritte im Workflow',
  'Kontaktformular-Workflow mit KI-Klassifikation, strukturierter Ausgabe und menschlicher Prüfung']),
 ('Donnerstag, 29.10.2026', 'APIs, Zeitformate und Abschluss der Make-Lektion', [
  'Abruf einer öffentlichen Test-API mit HTTP GET',
  'Statuscodes, Antwortdaten und Fehlerfälle unterscheiden',
  'Zeitformate und Zeitstempel: ISO 8601, UTC und Zeitzonen-Offsets',
  'Datumsformatierung mit formatDate und typische Fehlerquellen',
  'Prüfung, Dokumentation und Sicherung eigener Workflows']),
 ('Freitag, 30.10.2026', 'Relevante Use-Cases für KI-Automatisierung identifizieren', [
  'Ausgangslage: Studien zu KI-Pilotprojekten und typische Ursachen für das Scheitern',
  'Abgrenzung von Aufgabe, Prozess und Use-Case sowie passende Kennzahlen',
  'Zeitfresser-Analyse, Schmerz-Interviews und Merkmale guter und schlechter Use-Cases',
  'Use-Case-Steckbriefe mit Auslöser, Input, Output, Volumen und beziffertem Nutzen',
  'Automatisierungsgrade, Ausschlusskriterien und rechtliche Fallstricke in HR, Marketing und Vertrieb']),
]


def course():
    """Eintrag für kurs.TAGE[24] im Format der Modul-1-Tage (alle Standardfunktionen)."""
    return dict(
        titel='Use Cases finden + Learning Hub der Woche',
        unter='Modul 2 · Woche 1 · Tag 5',
        datum=DATUM, modul=2, lektion=2, modul_tag=5, url='modul-2/tag-5/', hub=True,
        kurz='Heute: gute Automatisierungs-Kandidaten finden und bewerten. Dazu die ganze Make-Woche zum Wiederholen: Wochenheft, 9 fertige Make-Vorlagen, Lernkarten, Selbsttest und Training.',
        lernheft=LERNHEFT,
        learnings=[dict(id=i, folie=f, tag=d, satz=s, erklaert=e) for i, f, d, s, e in LEARNINGS],
        karten=KARTEN,
        test=[dict(frage=q, optionen=o, richtig=r, warum=w) for q, o, r, w in TEST],
        begriffe=BEGRIFFE,
    )


assert len({l[0] for l in LEARNINGS}) == len(LEARNINGS)
assert all(len(e[2]) == 5 for e in KLASSENBUCH)
