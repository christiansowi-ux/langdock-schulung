"""Kapitel des Wochenhefts Modul 2 · Woche 1 (26.–30.10.2026).

Teil A: Make-Grundlagen (Tag 1–4), Teil B: Make-Werkstatt (9 Vorlagen),
Teil C: Use Cases identifizieren (Tag 5), Teil D: Mitnehmen.
Stand der Make-Angaben: Herstellerunterlagen 26.–30.10.2026.
"""
import json
from .bausteine import (E, md, P, H, merk, achtung, tipp, korrektur, beispiel, tab, flow, karten,
                        glossar, details, code, folien, kapitel, teil)
from .blueprints import AUTOMATIONS, STECKBRIEF_FELDER, STECKBRIEF_BEISPIEL
from .daten import KLASSENBUCH, BEGRIFFE

MATERIAL = '/hefte/material/modul2-woche1'
ZIP = 'Make-Vorlagen-Woche1.zip'
LEVEL = {1: 'ganz leicht', 2: 'leicht', 3: 'mit Router'}
TAGNAME = {1: 'Montag · Tag 1', 2: 'Dienstag · Tag 2', 3: 'Mittwoch · Tag 3', 4: 'Donnerstag · Tag 4', 5: 'Freitag · Tag 5'}


# ================================================================ Teil A · Make-Grundlagen

def teil_a():
    k = []
    k.append(kapitel('a1', 'A1', 'Montag · Folien 2, 4–6', 'Was „KI-Automation“ in diesem Kurs heißt',
        P('Auf Folie 2 stand die Frage: „Was ist für euch (KI-)Automation?“ Die Antworten im Raum waren sehr verschieden – deshalb legt der Kurs eine **enge Definition** fest:') +
        merk('KI-Automatisierung ist ein vorab festgelegter, wiederholbarer Ablauf, der durch ein Ereignis startet und an einzelnen Stellen ein Sprachmodell einsetzt. Kurz: ein festes Gerüst mit KI-Schritten darin.') +
        P('**Fest (deterministisch)** heißt: Du bestimmst vorher, welcher Schritt wann läuft, welche Daten wohin fließen und was am Ende entsteht. Der Weg ist bekannt, bevor der Ablauf startet.',
          'Die KI sitzt nur dort, wo früher ein Mensch **lesen und beurteilen** musste: einordnen, zusammenfassen, Angaben aus Freitext herausziehen, formulieren. Alles andere ist normale Datenarbeit. So bleibt die Unschärfe der KI auf einzelne Schritte begrenzt – der Ablauf bleibt kontrollierbar, testbar und wiederholbar.') +
        H('Zwei Dinge, die beide „KI-Automatisierung“ heißen') +
        tab(['', 'Agentische Automatisierung', 'Workflow-Automatisierung'], [
            ['Wer bestimmt den Weg?', 'Das Modell plant selbst, wählt Werkzeuge, führt aus. Der Weg entsteht während der Arbeit.', 'Du zeichnest den Weg vorher als Schritte. Jeder Durchlauf nimmt dieselbe Strecke.'],
            ['Stärke', 'Sehr flexibel', 'Exakt wiederholbar, testbar, überwachbar'],
            ['Schwäche', 'Schwer zu wiederholen und zu prüfen', 'Wenig flexibel'],
            ['Gut für', 'Einmalige, schlecht vorhersehbare Aufgaben', 'Gleichförmige Abläufe mit viel Menge'],
            ['Beispiele', 'Claude Cowork, Hermes Agent', 'Make, n8n, Zapier']]) +
        P('Ab jetzt meint der Kurs mit KI-Automatisierung immer **Workflow-Automatisierung**.') +
        H('Die Anatomie jedes Workflows') +
        flow([('Auslöser', 'Etwas passiert: neue Mail, Formular, Uhrzeit, Klick'), ('Daten holen', 'Die nötigen Angaben werden gelesen'),
              ('Verarbeiten', 'Prüfen, umformen, einordnen – evtl. mit KI'), ('Ergebnis erzeugen', 'Zeile, Entwurf, Aufgabe, Meldung')]) +
        beispiel('Alltagsbeispiel', 'Ein Pizzadienst: Bestellung geht ein (Auslöser) → Adresse und Pizza werden gelesen (Daten holen) → Küche bekommt einen Zettel, Fahrer eine Route (Verarbeiten) → Pizza ist da (Ergebnis). Jeden Abend derselbe Weg – nur die Daten ändern sich.') +
        folien(('make', 2), ('make', 4), ('make', 5), ('make', 6))))

    k.append(kapitel('a2', 'A2', 'Montag · Folie 7', 'Die Wörter, mit denen du ab jetzt arbeitest',
        P('Diese vier Begriffe gelten in allen Werkzeugen. Wenn du sie verstehst, kannst du jede Make-Anleitung lesen:') +
        glossar([
            ('Trigger', 'Das Ereignis, das den Ablauf startet: Zeitplan, Webhook oder manueller Start.', 'In unseren Vorlagen: dein Klick auf Run once.'),
            ('Node / Modul / Step', 'Ein einzelner Arbeitsschritt. n8n sagt Node, Make Modul, Zapier Step.', 'In Make: ein Kreis auf der Arbeitsfläche.'),
            ('Mapping', 'Felder zwischen Schritten zuordnen: „Nimm den Wert aus Schritt 1 und setz ihn hier ein.“', 'Laut Folie die häufigste Fehlerquelle überhaupt.'),
            ('Execution', 'Ein einzelner Durchlauf. Hier wird abgerechnet und im Fehlerfall nachgelesen.', 'In Make findest du ihn unter History.')]) +
        H('Die vier KI-Bausteine') +
        karten([('1', 'LLM-Node', 'Ruft ein Sprachmodell auf. Eingestellt werden Modell, Prompt und Temperatur.'),
                ('2', 'Prompt-Template', 'Fester Prompt mit Platzhaltern, die bei jedem Lauf gefüllt werden. Muss getestet und versioniert werden.'),
                ('3', 'Strukturierter Output', 'Die Antwort kommt als JSON mit festen Feldern. Laut Folie der wichtigste Kniff der KI-Automatisierung.'),
                ('4', 'Human-in-the-Loop', 'Ein fester Haltepunkt, an dem ein Mensch bei kritischen Abläufen freigibt.')], cols=2) +
        folien(('make', 7))))

    k.append(kapitel('a3', 'A3', 'Montag · Folie 8', 'Warum KI-Schritte streuen – und was dagegen hilft',
        P('Ein Sprachmodell **rechnet keine Antwort aus**. Es wählt Stück für Stück den wahrscheinlichsten nächsten Baustein. Deshalb kann dieselbe Eingabe unterschiedliche Ergebnisse liefern.') +
        beispiel('Beispiel von der Folie', 'Derselbe Lieferant erscheint als „Musterbau GmbH“, „Musterbau“ oder „Musterbau GmbH & Co. KG“. Drei Schreibweisen – und in der Tabelle entstehen drei verschiedene Datensätze.') +
        P('Der Regler **Temperatur** verringert die Streuung, setzt sie aber nie auf null.') +
        karten([('1', 'Auswahl statt Freitext', 'Erlaubte Werte vorgeben: „Antworte ausschließlich mit einem Wert aus: IT, Marketing, Fuhrpark, Sonstiges.“'),
                ('2', 'Festes Format, geprüft', 'Ergebnis als JSON anfordern und im nächsten Schritt gegen das Schema prüfen. Passt es nicht, wird wiederholt.'),
                ('3', 'Testen heißt wiederholen', 'Dieselbe Eingabe zehnmal laufen lassen. Die Streuung ist das Qualitätsmaß – nicht ein einzelner Erfolg.'),
                ('4', 'Zweifel sichtbar machen', 'Das Modell liefert ein Feld „unsicher“ mit. Diese Fälle gehen an einen Menschen.')], cols=2) +
        merk('Ein erfolgreicher Durchlauf beweist nichts. Erst viele gleiche Ergebnisse zeigen, dass ein KI-Schritt verlässlich ist.') +
        folien(('make', 8))))

    k.append(kapitel('a4', 'A4', 'Montag · Folien 9–11', 'Welches Werkzeug, welche Kosten, welche Abläufe?',
        P('Die Folie zeigt einen Marktüberblick (Stand Juli 2026) und betont: Funktionen und Preise ändern sich schnell. Die Frage ist nicht „Welches Tool ist das beste?“, sondern **„Welches passt zu unseren Systemen und zum Team?“** Weitere genannte Werkzeuge: Workato, Pipedream, Activepieces, Latenode, Gumloop, UiPath (für Altsysteme ohne Schnittstelle).') +
        tab(['Leitfrage', 'Was sie bedeutet'], [
            ['1 · Betriebsmodell zuerst', 'Selbst betreiben (Self-Hosting) oder als Cloud-Dienst (SaaS)? Das grenzt stärker ein als jede Funktion.'],
            ['2 · Technisches Profil', 'Ohne Technik → Zapier oder Langdock. Mit einer technischen Person → **Make**. Mit Entwicklung → n8n.'],
            ['3 · Abrechnung verstehen', 'Zapier pro Task, Make pro Operation (heute in **Credits** angezeigt), n8n Cloud pro Ausführung. KI-Kosten (Token) kommen dazu.']]) +
        tipp('Folienregel', 'Ein Werkzeug für den Anfang – nicht drei.') +
        H('Welche Abläufe sich eignen') +
        tab(['Gut geeignet', 'Schlecht geeignet'], [
            ['Wiederkehrend, in Worten beschreibbar, klare Eingangsformate, genug Menge, prüfbares Ergebnis', 'Braucht laufend fachliches Urteil, ändert sich oft oder kommt selten vor'],
            ['Posteingang sortieren, Rechnungsdaten auslesen, Berichte zusammenstellen', 'Kreative Einzelentscheidungen, seltene Sonderfälle']]) +
        P('**Der Zwischenweg:** Viele ungeeignete Abläufe enthalten geeignete Teilschritte. Automatisiere die Vorbereitung – die Entscheidung bleibt beim Menschen.') +
        H('Was einen Workflow betriebsfähig macht') +
        karten([('✓', 'Mit Ausreißern testen', 'Leere Felder, Sonderzeichen, falsche Dateiformate – nicht nur das saubere Beispiel.'),
                ('✓', 'Fehlerweg und Wiederholung', 'Ein neuer Versuch nach kurzer Wartezeit löst viele Störungen. Für den Rest gibt es einen festen Fehlerweg.'),
                ('✓', 'Aktive Benachrichtigung', 'Ein Fehler muss gemeldet werden. Ein Protokoll, in das niemand schaut, ist keine Überwachung.'),
                ('✓', 'Umgebungen trennen', 'Test und Echtbetrieb getrennt, mit eigenen Zugängen und Testempfängern.')], cols=2) +
        tab(['Typischer Fehler', 'Besser'], [
            ['Zu groß angefangen', 'Mit 5–7 Schritten beginnen'], ['Alles über KI gelöst', 'Was eine Formel kann, macht eine Formel – billiger und zuverlässiger'],
            ['Freitext statt fester Felder', 'JSON mit festen Feldern weitergeben'], ['Keine Stichproben nach dem Start', 'Regelmäßig Ergebnisse prüfen, bevor sich jemand beschwert']]) +
        folien(('make', 9), ('make', 10), ('make', 11))))

    k.append(kapitel('a5', 'A5', 'Make 2026 · Stand 30.10.2026', 'Deine Arbeitsfläche und dein Budget in Make',
        H('Der Free-Account') +
        tab(['Im Free-Plan', 'Was das für dich heißt'], [
            ['**1.000 Credits pro Monat**', 'Gemeinsames Budget für alle deine Szenarien.'],
            ['**2 aktive Szenarien**', 'Beliebig viele Szenarien speichern – aber nur zwei dürfen gleichzeitig automatisch laufen. Unsere Vorlagen bleiben inaktiv.'],
            ['**Zeitplan ab 15 Minuten**', 'Regelmäßige Läufe frühestens alle 15 Minuten. Wir nutzen keinen Zeitplan.'],
            ['**Tools, JSON, Router, Filter, HTTP**', 'Ohne fremdes Konto nutzbar – genau damit arbeiten unsere Vorlagen.']]) +
        H('So rechnet Make') +
        P('Ein normales Modul verbraucht pro Arbeitsgang (Operation) meist **1 Credit**. Router und Filter kosten selbst nichts – nur die Module dahinter. KI-Module können deutlich mehr verbrauchen.') +
        tab(['Beispiel', 'Planwert'], [
            ['Zwei normale Module, ein Lauf', '2 Credits'], ['Derselbe Lauf fünfmal', '10 Credits'],
            ['Filter stoppt nach Modul 1', '1 Credit'], ['Abfrage alle 15 Minuten, 30 Tage lang', '4 × 24 × 30 = **2.880 Credits** nur fürs Nachsehen']]) +
        achtung('Wichtig', 'Planwerte sind gerechnet, nicht in deinem Konto gemessen. Maßgeblich ist die Anzeige in deiner Organisation. Deshalb: Zeitplan aus, nur mit **Run once** testen, vorher und nachher den Credit-Stand ansehen.') +
        H('Orientierung im Scenario Builder') +
        tab(['Was du siehst', 'Wozu'], [
            ['**Scenarios** (linke Leiste)', 'Liste deiner Abläufe. Hier: **+ Create a new scenario**.'],
            ['**Arbeitsfläche (Canvas)**', 'Die Kreise sind Module, die Linien zeigen den Datenweg.'],
            ['**Großes Plus**', 'Neues Modul suchen und anhängen.'],
            ['**Run once** (unten)', 'Startet das Szenario genau einmal.'],
            ['**Sprechblase über einem Modul**', 'Erscheint nach dem Lauf: INPUT (was ankam) und OUTPUT (was herauskam).'],
            ['**Schraubenschlüssel unter einer Linie**', '„Set up a filter“ – hier baust du Filter.'],
            ['**Drei Punkte oben rechts**', 'Import blueprint, Export blueprint, Copy blueprint to clipboard.'],
            ['**History**', 'Frühere Läufe mit Status und Verbrauch.']]) +
        tipp('Wenn es anders aussieht', 'Make ändert die Oberfläche regelmäßig. Such nach den englischen Wörtern aus diesem Heft – sie bleiben meist gleich.') +
        H('Neu seit 2025/2026 – nur zur Einordnung') +
        P('Make hat inzwischen eigene KI-Module und **KI-Agenten** im Programm. Sie verbrauchen je nach Modell mehr Credits und brauchen teils eigene Einstellungen. Für diese Woche lernen wir das Fundament ohne KI-Konto: Daten, Mapping, Filter, Router, HTTP und Zeit.')))

    k.append(kapitel('a6', 'A6', 'Montag · Vorlage A1', 'Dein erster Ablauf: der Begrüßungs-Mixer',
        P('Am Montag hast du dein erstes Szenario gebaut: Aus einem Vornamen wird ein Satz. Klingt klein – zeigt aber das wichtigste Prinzip von Make: **Mapping**.') +
        flow([('Tools › Set variable', 'vorname = Luna'), ('Tools › Compose a string', 'Hallo {{1.vorname}}! Willkommen in Modul 2.'), ('Ergebnis', 'Hallo Luna! Willkommen in Modul 2.')]) +
        P('Die **1** in `{{1.vorname}}` heißt: „aus Modul Nummer 1“. `vorname` ist der Name des Fachs. Make zeigt das als farbige **Kachel** (Pill). Ändert sich der Wert in Modul 1, ändert sich automatisch der Satz in Modul 2.') +
        merk('Nur gemappte Kacheln übernehmen neue Werte. Fest eingetippter Text bleibt immer gleich.') +
        P('Fertig zum Import: **Vorlage A1** in Teil B.')))

    k.append(kapitel('a7', 'A7', 'Dienstag · Folien 12–16', 'Die Folienübung: jede neue Mail als Excel-Zeile',
        P('Die erste große Folienübung zeigt das ganze Handwerk eines echten Workflows. Ziel: **Jede neue E-Mail im Outlook-Posteingang landet automatisch als Zeile in einer Excel-Tabelle.**') +
        tab(['Schritt', 'Was passiert', 'Worauf achten'], [
            ['1 · Szenario anlegen', 'Neues Szenario „EMailTabelle“', '–'],
            ['2 · Excel vorbereiten', 'In OneDrive: E-Mail-Eingang.xlsx, Blatt „Eingänge“, Kopfzeile mit 6 Spalten', 'Bereich **als Tabelle formatieren** – sonst findet Make das Ziel nicht'],
            ['3 · Trigger', 'Microsoft 365 Email › **Watch Emails**: Inbox, All emails, Limit 2, From now on', 'Ereignisbasiert'],
            ['4 · Action', 'Microsoft 365 Excel › **Add a Table Row**: Workbook, Worksheet, Tabelle1', 'Microsoft-Konto verbinden'],
            ['5 · Mapping', 'Zeitstempel → Received Date Time, Name → From: Name, Adresse → From: Address, Betreff → Subject, Inhalt → Body Preview, Link → Web Link', 'Jede Spalte bekommt genau ein Feld'],
            ['6 · Test', 'Run once, Testmail schicken, neue Zeile prüfen', 'Trigger, Action und Zeile kontrollieren'],
            ['7 · Zeitplan', 'Uhr-Symbol: At regular intervals, 15 Minuten', 'Kostet Credits bei jeder Abfrage'],
            ['8 · Aktivieren', 'Schalter auf Active, History prüfen: Success, Credits, Incomplete executions leer', '–'],
            ['9 · Dokumentieren', 'Trigger, Actions, Ablauf in eigenen Worten, Mapping, Screenshots', '–']]) +
        achtung('Voraussetzung', 'Für diese Übung brauchst du ein Microsoft-365-Konto mit Outlook und OneDrive. Ein dauerhaft aktiver 15-Minuten-Zeitplan kann im Free-Plan schnell viele Credits verbrauchen (siehe A5). Unsere Vorlagen üben dieselben Handgriffe – Trigger, Mapping, Test – ganz ohne fremdes Konto.') +
        folien(('make', 12), ('make', 13), ('make', 14), ('make', 15), ('make', 16))))

    typen = [['String', 'Text in doppelten Anführungszeichen', '"Produkt X"'], ['Number', 'Ganze oder Kommazahl, ohne Anführungszeichen', '123 · 3.14'],
             ['Boolean', 'Wahrheitswert', 'true · false'], ['Null', 'Absichtlich leer – nicht dasselbe wie ""', 'null'],
             ['Object', 'Sammlung von Feldern in geschweiften Klammern', '{"name": "Alice", "age": 30}'],
             ['Array', 'Geordnete Liste in eckigen Klammern', '["Apfel", "Birne", "Orange"]']]
    k.append(kapitel('a8', 'A8', 'Dienstag · Folien 24–27', 'JSON, Variablen und Datenfluss',
        P('**JSON** (JavaScript Object Notation) ist ein leichtes, für Menschen lesbares Datenformat. Stell es dir als **beschrifteten Zettel** vor: links der Feldname, rechts der Wert.') +
        code(json.dumps({'projekt': 'Papierfunke', 'thema': 'Workshop am 30.10.', 'kanal': 'Instagram', 'status': 'ENTWURF'}, ensure_ascii=False, indent=2), 'Unser Redaktionsbriefing (Vorlage A2)') +
        P('Warum JSON für KI-Automation so wichtig ist: **gleich aufgebaute Ausgaben**, **einfaches Zerlegen**, **Austausch zwischen Systemen** und **gute Lesbarkeit**.') +
        H('Die sechs Datentypen') + tab(['Typ', 'Bedeutung', 'Beispiel'], typen) +
        achtung('Häufiger Fehler', '"true" in Anführungszeichen ist Text, kein Boolean. Und null ist nicht dasselbe wie "" (leerer Text).') +
        H('Variablen und Datenfluss') +
        P('**Variablen** sind Platzhalter für Werte, die sich je Durchlauf ändern – z. B. die Antwort einer KI oder eine Eingabe. Sie tragen Werte von Modul zu Modul.',
          'In Make und n8n wandern Daten als **Päckchen** (Make: Bundles, n8n: Items) durch den Ablauf. Jedes Modul nimmt ein Päckchen, verarbeitet es und gibt ein neues weiter.') +
        flow([('1 · Datenaufnahme', 'Trigger bringt das erste Päckchen'), ('2 · KI-Verarbeitung', 'Modell liefert JSON'),
              ('3 · Zerlegen & Mapping', 'Parse JSON macht Felder daraus'), ('4 · Aktion', 'Folgemodule nutzen die Felder')]) +
        merk('Parse JSON zerlegt JSON-Text in einzelne Felder. Erst dann kannst du jedes Feld einzeln mappen.') +
        folien(('make', 24), ('make', 25), ('make', 26), ('make', 27))))

    k.append(kapitel('a9', 'A9', 'Mittwoch · Folien 17, 28–29', 'Filter, Router, Operatoren und Webhooks',
        karten([('1', 'Filter = Tür', 'Prüft Daten an einer Stelle. Nur wenn die Bedingung stimmt, geht es weiter. Spart Kosten, weil unnötige (KI-)Schritte nicht laufen. Beispiel: nur Mails von bekannten Absendern.'),
                ('2', 'Router = Weiche', 'Teilt den Ablauf in mehrere Wege. Jeder Weg hat seinen eigenen Filter. Beispiel: Anfragen nach Abteilung verteilen.')], cols=2) +
        H('Vergleichsoperatoren') +
        tab(['Operator', 'Frage', 'In Make'], [
            ['Gleich (=)', 'Sind beide Werte identisch?', 'Equal to'], ['Ungleich (!=)', 'Sind sie verschieden?', 'Not equal to'],
            ['Größer / kleiner', 'Zahlenvergleich', 'Greater than / Less than'], ['Enthält', 'Steckt ein Text in einem anderen?', 'Contains']]) +
        H('Logische Operatoren') +
        tab(['', 'Bedeutung', 'Beispiel'], [
            ['**AND**', 'Alle Bedingungen müssen stimmen.', 'kategorie = VIDEO **und** freigabe = true'],
            ['**OR**', 'Mindestens eine muss stimmen.', 'Anliegen = Support **oder** Anliegen = Beschwerde']]) +
        tipp('So sieht es in Make aus', 'Bedingungen untereinander in einem Block sind AND. Mit „Add OR rule“ entsteht ein neuer Block – die Blöcke sind OR-verknüpft. Genau das siehst du in Vorlage A9.') +
        H('Webhooks: sofort statt immer wieder nachfragen') +
        tab(['', 'Wie es funktioniert'], [
            ['**Webhook (Push)**', 'Eine Anwendung schickt automatisch eine Nachricht an eine feste Adresse, sobald etwas passiert – wie ein Rückruf.'],
            ['**Polling (Pull)**', 'Der Workflow fragt regelmäßig nach: „Gibt es Neues?“ – auch wenn nichts passiert ist.'],
            ['**API-Abfrage**', 'Man fragt ausdrücklich nach Daten, wenn man sie braucht.']]) +
        merk('Webhooks sind der effizienteste Weg, auf Ereignisse in Echtzeit zu reagieren: kein Warten, keine leeren Abfragen.') +
        folien(('make', 17), ('make', 28), ('make', 29))))

    k.append(kapitel('a10', 'A10', 'Mittwoch · Folien 18–23, 30', 'KI im Workflow: Rollen, festes Format, Kontaktformular',
        H('Drei Rollen in jedem KI-Aufruf') +
        tab(['Rolle', 'Was sie ist', 'Beispiel'], [
            ['**System**', 'Identität, Ton und Regeln. Für Nutzende unsichtbar, gilt für jede Antwort.', '„Du bist Experte für digitale Transformation. Antworte präzise.“'],
            ['**User**', 'Die konkrete Frage oder Eingabe.', '„Was sind die größten Hürden bei KI im Unternehmen?“'],
            ['**Assistant**', 'Die Antwort des Modells. Wird Teil des Verlaufs.', '„Datenqualität, Integration, Widerstand im Team.“']]) +
        P('In der Chat-Completion-Schnittstelle werden die drei als Liste `messages` übergeben, jeweils mit `role` und `content`.') +
        H('Die große Folienübung: Kontaktformular automatisch beantworten') +
        flow([('Tally › Watch New Response', 'Formular startet sofort (instant)'), ('Mistral › Create a Completion', 'System-Prompt, Temperatur 0.3, Antwort als json_object'),
              ('JSON › Parse JSON', 'betreff, body_text, kategorie, prioritaet'), ('Outlook › Send a Message', 'Bestätigung an den Absender'),
              ('Router', 'Vertrieb (HubSpot), Support, Marketing, Sonstiges')]) +
        tab(['Gelernt wird', 'Warum es wichtig ist'], [
            ['Formular als Trigger', 'Ereignis startet sofort, kein Zeitplan nötig'],
            ['Enger System-Prompt mit Beispielen', 'Rolle, Firmenkontext, erlaubte Kategorien und Prioritäten, striktes JSON'],
            ['JSON statt Fließtext erzwingen', 'Nur so kann Parse JSON die Antwort sicher zerlegen'],
            ['Router nach Kategorie', 'Jede Abteilung bekommt nur ihre Fälle'],
            ['Vier Testfälle inkl. Widerspruch', 'Dropdown „Sonstiges“, Text „Support“: Wie entscheidet die KI?']]) +
        achtung('Voraussetzungen und Vorsicht', 'Diese Übung braucht Tally, einen Mistral-API-Schlüssel, Microsoft 365 und HubSpot. Echte Mails an echte Menschen erst nach Tests mit Testempfängern und mit menschlicher Prüfung. Überlege auch: Was passiert mit SPAM?') +
        P('Unsere Vorlage **A4 (Anfragen-Weiche)** übt denselben Router ohne Konten – die „KI-Einordnung“ ersetzt dort eine feste Testangabe.') +
        folien(('make', 18), ('make', 19), ('make', 20), ('make', 21), ('make', 22), ('make', 23), ('make', 30))))

    k.append(kapitel('a11', 'A11', 'Donnerstag · Folien 31–34', 'APIs lesen und Zeitangaben richtig behandeln',
        H('Eine Test-API lesen') +
        P('Eine **API** ist eine vereinbarte Adresse, über die Programme Daten austauschen. **HTTP** ist der Weg dorthin. **GET** heißt: nur lesen, nichts verändern.') +
        tab(['Statuscode', 'Bedeutung'], [['200', 'OK – Abruf hat geklappt'], ['404', 'Nicht gefunden – falsche Adresse'], ['401 / 403', 'Keine Berechtigung'], ['500', 'Fehler beim Server']]) +
        merk('Status 200 heißt: Der Abruf hat technisch geklappt. Ob die Daten fachlich stimmen, ist eine zweite Frage.') +
        H('Zeitformate') +
        P('Zeit ist in Workflows knifflig: Zeitzonen, Sommer- und Winterzeit, verschiedene Schreibweisen. Drei Formate begegnen dir ständig:') +
        tab(['Format', 'Beispiel', 'Wofür'], [
            ['ISO 8601', '2026-07-29T14:35:07Z', 'Standard in APIs und Make'], ['Unix-Zeitstempel', '1785335707', 'Sekunden seit 1.1.1970'],
            ['Lokales Format', '29.07.2026 16:35', 'Nur für Menschen lesbar']]) +
        tab(['ISO 8601', 'Bedeutung'], [
            ['2026-07-29', 'Nur Datum'], ['14:35:07', 'Nur Uhrzeit'], ['2026-07-29T14:35:07', 'Datum + Uhrzeit, **T** ist fester Trenner – aber ohne Zone mehrdeutig!'],
            ['2026-07-29T14:35:07**Z**', 'Z = Zulu = UTC+0 – bevorzugt in APIs'], ['2026-07-29T14:35:07**+02:00**', 'Zwei Stunden vor UTC (Sommerzeit Berlin)'],
            ['2026-07-29T08:35:07**-06:00**', 'Sechs Stunden hinter UTC'], ['2026-07-29T14:35:07**.483**Z', 'Mit Millisekunden']]) +
        H('formatDate in Make') +
        code('formatDate(now; "DD.MM.YYYY HH:mm"; "Europe/Berlin")', 'Make-Funktion, kein Chat-Prompt') +
        P('formatDate macht aus einem Zeitpunkt lesbaren Text. Das Muster bestimmt die Schreibweise, die Zone den Ort. **Europe/Berlin** kennt Sommer- und Winterzeit automatisch: Ende Oktober gilt +01:00, im Juli +02:00.') +
        tab(['Fehlerquelle', 'Was passiert'], [
            ['Zeitzone vergessen', 'Stunden-Verschiebungen'], ['Falsches Trennzeichen', 'ISO schreibt - vor, manche Systeme / – nie mischen'],
            ['12 statt 24 Stunden', '2:35 PM ist kein gültiges ISO-Format'], ['Millisekunden ignoriert', 'Vergleiche schlagen wegen .000 fehl'],
            ['Lokales Format in API-Feldern', '29.07.2026 ist kein ISO 8601']]) +
        korrektur('Folie 34', 'Die Folie sagt „lokale Formate niemals in Variablen“. Genauer: Für Ausgaben an Menschen (Mail-Text, Notiz) ist das deutsche Format richtig. Für APIs, Vergleiche und Speicherung gilt das Format, das das Zielfeld erwartet – meist ISO 8601. Das Folienbeispiel „16:35“ passt zum Juli (+02:00).') +
        P('Fertig zum Import: **Vorlage A5** (Test-API) und **Vorlage A6** (Zeitstempel-Übersetzer).') +
        folien(('make', 31), ('make', 32), ('make', 33), ('make', 34))))
    return teil('teil-a', 'A', 'Make-Grundlagen der Woche', 'Montag bis Donnerstag in einem Durchgang: alle 34 Folien, aktuell eingeordnet und in Alltagssprache erklärt.', ''.join(k))


# ================================================================ Teil B · Make-Werkstatt

def import_anleitung():
    return kapitel('b0', 'B0', 'Gilt für alle 9 Vorlagen', 'So holst du eine fertige Vorlage in dein Make',
        P('Eine **Vorlage (Blueprint)** ist eine JSON-Datei, in der ein komplettes Szenario steckt: Module, Einstellungen und Mappings. Du musst nichts nachbauen – nur importieren, starten und verstehen.') +
        flow([('1 · Herunterladen', 'Auf „JSON herunterladen“ klicken. Die Datei landet in „Downloads“.'),
              ('2 · Neues Szenario', 'In Make links **Scenarios** → **+ Create a new scenario**.'),
              ('3 · Importieren', 'Oben rechts die **drei Punkte (…)** → **Import blueprint** → **Choose file** → Datei wählen → **Save**.'),
              ('4 · Speichern', 'Unten das **Speichern-Symbol** (Diskette) klicken.'),
              ('5 · Starten', '**Run once** klicken. Kurz warten, bis die Kreise grün werden.'),
              ('6 · Ergebnis lesen', 'Auf die **Sprechblase** über dem letzten Modul klicken → **OUTPUT** aufklappen.')], cls='steps') +
        tipp('Ohne Datei: kopieren und einfügen', 'Auf „JSON kopieren“ klicken. In Make ein neues Szenario öffnen, mit der rechten Maustaste auf die leere Fläche klicken → **Paste**. Am Mac: Rechtsklick = mit zwei Fingern aufs Trackpad tippen oder Control + Klick.') +
        achtung('Drei Sicherheitsregeln', '1. Zeitplan bleibt aus – die Vorlagen starten nur per Run once. 2. Keine Vorlage verschickt, veröffentlicht oder speichert etwas außerhalb von Make. 3. Nur erfundene Beispieldaten eintragen.') +
        tab(['Nr.', 'Vorlage', 'Tag', 'Lernt', 'Credits je Lauf'],
            [[f'A{a["nr"]}', a['titel'], TAGNAME[a['tag']], a['lernt'], f'≈ {a["credits"]}'] for a in AUTOMATIONS]) +
        P(f'Alle neun auf einmal: **{ZIP}** (ZIP-Datei, vorher entpacken). Für alle Vorlagen mit je zwei Tests planst du rund **40 Credits** ein.'))


def vorlage(a, web=True):
    nr = a['nr']
    file = f'M2-{a["slug"]}.blueprint.json'
    mods = ''.join(
        f'<div class="bp-mod"><p class="bp-mod-h"><span class="bp-app">{E(app)}</span><span class="bp-name">{E(name)}</span></p>' +
        tab(['Feld', 'Steht drin', 'Bedeutet'], [[f'**{f}**', f'`{v}`', x] for f, v, x in fields], cls='bp-tab') + '</div>'
        for app, name, fields in a['module'])
    dots = '●' * a['level'] + '○' * (3 - a['level'])
    buttons = (f'<div class="bp-btns"><a class="btn primary" href="{MATERIAL}/{file}" download>JSON herunterladen</a>'
               f'<button class="btn" type="button" data-copy-url="{MATERIAL}/{file}">JSON kopieren</button>'
               f'<label class="bp-done"><input type="checkbox" data-save="vorlage-a{nr}"> erledigt</label></div>') if web else \
              f'<p class="bp-file">Datei: <b>{E(file)}</b> · quint-games.de/hefte/material/modul2-woche1/</p>'
    fehler = ''.join(f'<li><b>{md(t)}</b> {md(x)}</li>' for t, x in a['fehler'])
    body = (f'<div class="bp-meta"><span class="chip">{E(TAGNAME[a["tag"]])}</span><span class="chip">{dots} {E(LEVEL[a["level"]])}</span>'
            f'<span class="chip">≈ {a["minuten"]} Min.</span><span class="chip">≈ {a["credits"]} Credits je Lauf</span><span class="chip">kein fremdes Konto</span></div>'
            + P(a['kurz']) + f'<p class="bp-lernt"><b>Du lernst:</b> {md(a["lernt"])}</p>' + buttons +
            H('Was in der Vorlage steckt – Modul für Modul', 4) + mods +
            H('Testen', 4) +
            f'<ol class="bp-steps"><li>Importieren und speichern (siehe B0).</li><li><b>Run once</b> klicken.</li><li>{md(a["soll_wo"])}.</li></ol>' +
            f'<div class="soll"><span class="lbl">So soll es aussehen</span><pre>{E(a["soll"])}</pre></div>' +
            H('Selbst ändern', 4) +
            f'<div class="aendern"><p><b>Deine Aufgabe:</b> {md(a["aendern"][0])}</p><p><b>Dann siehst du:</b> {md(a["aendern"][1])}</p></div>' +
            f'<div class="fehlerhilfe"><span class="lbl">Wenn es hakt</span><ul>{fehler}</ul></div>')
    return kapitel(f'vorlage-a{nr}', f'A{nr}', f'Make-Vorlage · {TAGNAME[a["tag"]]}', a['titel'], body, cls='vorlage')


def teil_b(web=True):
    inner = import_anleitung() + ''.join(vorlage(a, web) for a in AUTOMATIONS)
    return teil('teil-b', 'B', 'Make-Werkstatt: 9 fertige Vorlagen',
                'Herunterladen, importieren, Run once – und jede Einstellung verstehen. Alles läuft mit Make Free, ohne fremdes Konto.', inner)


# ================================================================ Teil C · Use Cases (Tag 5)

def zeitfresser_tool(web=True):
    if not web:
        rows = ''.join('<tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for _ in range(8))
        return ('<div class="tab-wrap"><table class="tab ausfuell"><thead><tr><th>Tätigkeit (mind. wöchentlich)</th><th>Häufigkeit / Monat</th><th>Minuten je Vorgang</th>'
                '<th>Systeme</th><th>Fehler n/m/h</th><th>Minuten / Monat</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
                '<p class="ausfuell-zeile">Top 3: 1. ____________________ 2. ____________________ 3. ____________________</p>')
    return ('<div class="tool" data-tool="zeitfresser"><div class="tool-h"><b>Zeitfresser-Rechner</b><span>rechnet und sortiert automatisch · speichert in diesem Browser</span></div>'
            '<div class="zf-table" role="table" aria-label="Zeitfresser-Liste"></div>'
            '<div class="btnrow"><button class="btn" type="button" data-zf-add>+ Tätigkeit</button><button class="btn" type="button" data-zf-sort>Nach Minuten sortieren</button>'
            '<button class="btn ghost" type="button" data-zf-demo>Beispiel laden</button></div>'
            '<div class="zf-top" aria-live="polite"></div></div>')


def interview_tool(web=True):
    fragen = ['Was machst du regelmäßig, obwohl du weißt, dass ein Computer es könnte?', 'Wo wartest du auf jemand anderen?',
              'Was musst du zweimal eintippen?', 'Wann hat das zuletzt nicht funktioniert – und was ist dann passiert?']
    if not web:
        return '<ol class="interview-print">' + ''.join(f'<li><b>{E(f)}</b><span class="linie"></span><span class="linie"></span></li>' for f in fragen) + '</ol>'
    return ('<div class="tool"><div class="tool-h"><b>Schmerz-Interview · wörtlich mitschreiben</b><span>speichert in diesem Browser</span></div>' +
            ''.join(f'<label class="fld"><span>{i}. {E(f)}</span><textarea rows="3" data-save="interview-{i}" placeholder="Wörtlich notieren – nicht zusammenfassen"></textarea></label>'
                    for i, f in enumerate(fragen, 1)) +
            '<label class="fld"><span>Danach allein: Wo stecken Wartezeiten und Doppeleingaben?</span><textarea rows="2" data-save="interview-markiert"></textarea></label></div>')


def steckbrief_tool(web=True):
    if not web:
        return ('<div class="tab-wrap"><table class="tab ausfuell steck"><thead><tr><th>Feld</th><th>Kandidat 1</th><th>Kandidat 2</th><th>Kandidat 3</th></tr></thead><tbody>' +
                ''.join(f'<tr><td><b>{i}. {E(label)}</b></td><td></td><td></td><td></td></tr>' for i, (_, label, _, _) in enumerate(STECKBRIEF_FELDER, 1)) +
                '</tbody></table></div>')
    tabs = ''.join(f'<button type="button" class="sb-tab" data-sb="{k}" aria-pressed="{str(k == 1).lower()}">Kandidat {k}</button>' for k in (1, 2, 3))
    panes = ''
    for k in (1, 2, 3):
        fields = ''.join(f'<label class="fld"><span>{i}. {E(label)}</span><small>{E(hint)}</small>'
                         f'<input type="text" data-save="sb{k}-{key}"{" data-nutzen" if key == "nutzen" else ""}></label>'
                         for i, (key, label, hint, _) in enumerate(STECKBRIEF_FELDER, 1))
        panes += f'<div class="sb-pane" data-sb-pane="{k}"{"" if k == 1 else " hidden"}>{fields}<p class="sb-check" aria-live="polite"></p></div>'
    return ('<div class="tool" data-tool="steckbrief"><div class="tool-h"><b>Drei Steckbriefe · je elf Felder</b><span>Nutzen-Check läuft mit · speichert in diesem Browser</span></div>'
            f'<div class="sb-tabs">{tabs}</div>{panes}'
            '<div class="btnrow"><button class="btn primary" type="button" data-export>Meine Use-Case-Arbeit herunterladen (.md)</button></div></div>')


def stufen_tool(web=True):
    stufen = ['0 · Manuell', '1 · Assistenz', '2 · Human-in-the-Loop', '3 · Semi-Autonom', '4 · Autonom']
    krit = ['Zugriff auf die nötigen Daten vorhanden', 'Verantwortliche Person im Fachbereich benannt', 'Ziel ist rechtlich zulässig',
            'Richtiger Output ist definierbar', 'Prozess wird nicht gerade umgestellt']
    if not web:
        return ('<div class="tab-wrap"><table class="tab ausfuell"><thead><tr><th></th><th>Kandidat 1</th><th>Kandidat 2</th><th>Kandidat 3</th></tr></thead><tbody>'
                '<tr><td><b>Stufe Standardfall + Begründung</b></td><td></td><td></td><td></td></tr><tr><td><b>Stufe Ausnahme + Begründung</b></td><td></td><td></td><td></td></tr>' +
                ''.join(f'<tr><td>☐ {E(c)}</td><td></td><td></td><td></td></tr>' for c in krit) +
                '<tr><td><b>Drei fremde Einwände</b></td><td></td><td></td><td></td></tr></tbody></table></div>')
    opts = ''.join(f'<option value="{i}">{E(s)}</option>' for i, s in enumerate(stufen))
    cols = ''
    for k in (1, 2, 3):
        cols += (f'<div class="st-col" data-st="{k}"><p class="st-h">Kandidat {k} <span data-sb-name="{k}"></span></p>'
                 f'<label class="fld"><span>Standardfall</span><select data-save="st{k}-standard"><option value="">wählen …</option>{opts}</select></label>'
                 f'<label class="fld"><span>Ausnahme</span><select data-save="st{k}-ausnahme"><option value="">wählen …</option>{opts}</select></label>'
                 f'<label class="fld"><span>Begründung</span><textarea rows="2" data-save="st{k}-warum"></textarea></label>'
                 f'<label class="chk"><input type="checkbox" data-save="st{k}-zeit"> Die prüfende Person hat Zeit und Information zum Widersprechen</label>'
                 '<p class="st-sub">Ausschlusskriterien</p>' +
                 ''.join(f'<label class="chk"><input type="checkbox" data-save="st{k}-k{i}"> {E(c)}</label>' for i, c in enumerate(krit, 1)) +
                 f'<label class="fld"><span>Drei fremde Einwände</span><textarea rows="3" data-save="st{k}-einwaende"></textarea></label>'
                 '<p class="st-result" aria-live="polite"></p></div>')
    return f'<div class="tool" data-tool="stufen"><div class="tool-h"><b>Stufe, Ausschluss, Kreuzverhör</b><span>speichert in diesem Browser</span></div><div class="st-grid">{cols}</div></div>'


def treppe_tool(web=True):
    steps = [('Ist der Input strukturiert und lässt sich die Entscheidung als Regel formulieren?', 'Stufe 1 · Fester Workflow mit Regeln', 'Deterministisch, testbar, im Betrieb praktisch kostenlos.'),
             ('Genügt ein Modell an genau einer Stelle – einordnen, herausziehen, formulieren?', 'Stufe 2 · Sprachmodell im Workflow', 'Ablauf bleibt fest, Kosten je Aufruf, Stichproben nötig.'),
             ('Sind Werkzeuge und Reihenfolge je Fall unterschiedlich?', 'Stufe 3 · Agent mit eigener Planung', 'Schwer testbar, teuer im Betrieb.')]
    if not web:
        return flow([(q, f'Ja → {a}') for q, a, _ in steps] + [('Dreimal Nein', 'Use-Case neu definieren – zurück zum Auslöser')])
    data = E(json.dumps(steps, ensure_ascii=False))
    return (f'<div class="tool treppe" data-tool="treppe" data-steps="{data}"><div class="tool-h"><b>Entscheidungstreppe zum Durchklicken</b>'
            '<span>Von oben nach unten – beim ersten Ja stehen bleiben</span></div><div class="tr-stage" aria-live="polite"></div></div>')


def teil_c(pid=None, web=True):
    k = []
    k.append(kapitel('c1', 'C1', 'Freitag · Use-Case-Folien 1–2', 'Was heute am Ende vorliegt',
        P('Heute geht es nicht um mehr Wissen über Automatisierung, sondern um **drei bewertbare Kandidaten aus deinem eigenen Bereich**. Das ist Teil 1 von 5 der Reihe „KI-Automatisierung im Unternehmen“.') +
        karten([('01', 'Eine Zeitfresser-Liste', 'Sortiert nach Häufigkeit mal Dauer – nicht nach gefühlter Lästigkeit. Diese Sortierung überrascht in fast jeder Gruppe.'),
                ('02', 'Drei Use-Case-Steckbriefe', 'Mit Volumen, Auslöser, Input, Output und beziffertem Nutzen.'),
                ('03', 'Je Kandidat ein Automatisierungsgrad', 'Wie viel darf das System allein tun? Das bestimmt Risiko, Aufwand, Preis und rechtliche Einordnung.'),
                ('04', 'Eine Vorauswahl, die hält', 'Kandidaten, die den Ausschlusskriterien standhalten – an denen man nicht scheitert, bevor man begonnen hat.')], cols=2) +
        tipp('So arbeitest du heute', 'Lesen in diesem Heft, ausfüllen im Use-Case-Labor des Learning Hubs (oder in den Drucktabellen). Die Make-Vorlagen A7–A9 machen die Ideen sichtbar.') +
        folien(('uc', 1), ('uc', 2))))

    k.append(kapitel('c2', 'C2', 'Freitag · Use-Case-Folien 4–6', 'Die Ausgangslage – und wie man Zahlen richtig liest',
        tab(['Zahl', 'Was sie misst', 'Quelle laut Folie'], [
            ['**95 %**', 'Generative KI-Piloten ohne messbaren Effekt auf das Geschäftsergebnis', 'MIT NANDA, State of AI in Business 2025 (150 Interviews, 350 Befragte, 300 Einführungen)'],
            ['**> 40 %**', 'Agentenbasierte KI-Projekte, die bis Ende 2027 abgebrochen werden (Prognose)', 'Gartner, 25.06.2025'],
            ['**≈ 75 %**', 'Führungskräfte, die angeben, agentische KI einzusetzen (Selbstauskunft)', 'Forrester, 03.06.2026'],
            ['**17 %**', 'Haben KI-Agenten tatsächlich im Einsatz; über 60 % wollen es in zwei Jahren', 'Gartner CIO Survey 2026'],
            ['**11 %**', 'Haben produktionsreife agentische Systeme; 42 % ohne formale Strategie', 'Deloitte Tech Trends 2026']]) +
        P('Was das bedeutet: Fast alle melden Einsatz, produktiv läuft es bei einem Bruchteil. Es gibt einen **Rückstau an Pilotprojekten**, die entweder in Betrieb gehen oder abgebrochen werden. Dazu „Agent washing“: Von tausenden Anbietern mit dem Etikett „agentisch“ sind nach Gartner-Schätzung nur etwa 130 wirklich agentisch (Richtwert ohne offengelegte Methode).') +
        achtung('Nicht vermischen', '„Kein messbarer ROI“ und „abgebrochen“ sind verschiedene Messgrößen und lassen sich nicht addieren. Viele der 95 % liefen weiter – oft wurde nur vorher kein Ausgangswert gemessen. Die 40 % sind eine Prognose, u. a. auf Basis einer Umfrage unter 3.412 Webinar-Teilnehmenden.') +
        merk('In keiner Ursache steht „das Modell war nicht gut genug“. Über Erfolg entscheidet die Arbeit vor und nach dem Bauen: Auswahl, Messung und Verantwortung im Betrieb.') +
        folien(('uc', 4), ('uc', 5), ('uc', 6))))

    k.append(kapitel('c3', 'C3', 'Freitag · Use-Case-Folien 7–8', 'Woran es liegt – und was erfolgreiche Projekte anders machen',
        tab(['Ursache', 'Woran man sie erkennt'], [
            ['1 · Unklare Zielsetzung', '„Weniger E-Mails bearbeiten“ ist kein Ziel'], ['2 · Fehlende Erfolgskriterien', 'Niemand weiß, wann es gut ist'],
            ['3 · Schlechte Datenlage', 'Der Input ist nicht maschinell verfügbar'], ['4 · Fehlende Governance', 'Recht und Zuständigkeit erst am Ende geprüft'],
            ['5 · Niemand verantwortet den Betrieb', 'Nach dem Start ist niemand zuständig'], ['~~6 · Das Modell war zu schwach~~', 'Auf der Folie durchgestrichen – genau das ist der Punkt']]) +
        H('Vier Merkmale der Projekte, die durchkommen') +
        karten([('01', 'Gestufte Autonomie', 'Erst Unterstützung, dann Automatisierung, echte Autonomie als Ziel – nicht als Start. Ausgeliefert wird der engste Zuschnitt mit messbarem Nutzen.'),
                ('02', 'Freigaben nach Umkehrbarkeit', 'Unumkehrbare, kundenwirksame und ausgabenwirksame Schritte laufen über einen Menschen. Umkehrbare Schritte mit kleinem Einsatz laufen frei mit Stichproben.'),
                ('03', 'ROI-Prüfpunkte je Phase', 'Jede Ausweitung verdient ihr Budget neu – gegen einen Ausgangswert vom Projektstart, mit Freigabe aus den Finanzen.'),
                ('04', 'Ein benannter Eigentümer', 'Aufsicht, Sicherheit und Kosten werden früh geklärt, nicht nach dem Rollout.')], cols=2) +
        folien(('uc', 7), ('uc', 8))))

    k.append(kapitel('c4', 'C4', 'Arbeitsauftrag 01 · Use-Case-Folie 9 · 25 + 10 Min.', 'Zeitfresser erfassen – rechnen statt schätzen',
        flow([('01', 'Jede Tätigkeit eintragen, die mindestens wöchentlich vorkommt.'), ('02', 'Je Zeile: Häufigkeit pro Monat, Minuten je Vorgang, Anzahl Systeme, Fehleranfälligkeit (n/m/h).'),
              ('03', '„Minuten pro Monat“ = Häufigkeit × Minuten. Erst rechnen, dann bewerten.'), ('04', 'Sortieren und die drei größten Posten markieren.')], cls='steps') +
        zeitfresser_tool(web) +
        beispiel('Am Tisch', 'Vergleicht die Top 3. Wer hat den größten Posten – und hätte den vorher jemand geraten?') +
        merk('Fertig, wenn unter der Tabelle drei Posten mit Zahl stehen – nicht mit Gefühl.') +
        tipp('Mit Make nachrechnen', 'Vorlage A7 „Zeitfresser-Rechner“ rechnet genau diese Formel und sortiert ab 600 Minuten im Monat in „Top-Kandidat“.') +
        folien(('uc', 9))))

    k.append(kapitel('c5', 'C5', 'Freitag · Use-Case-Folien 11–13', 'Was ein Use-Case ist – und auf welcher Ebene du misst',
        P('Ein Use-Case entsteht erst, wenn **alle drei Bedingungen** zusammenkommen:') +
        karten([('1', 'Echtes Problem', 'Ein konkretes Geschäftsproblem, das jemanden stört.'), ('2', 'KI-Lösung', 'Ein klar abgrenzbarer Teil des Ablaufs ist übernehmbar.'),
                ('3', 'Messbarer Mehrwert', 'Das Ergebnis ist nachweisbar besser als vorher.')]) +
        tab(['Es fehlt …', 'Dann ist es …'], [['messbarer Mehrwert', 'ein Bauchgefühl-Projekt'], ['die KI-Lösung', 'eine Prozessverbesserung, keine Automatisierung'],
                                             ['das echte Problem', 'Technologie sucht Anwendung']]) +
        H('Aufgabe, Prozess, Use-Case') +
        tab(['Ebene', 'Beispiel', 'Kennzahl', 'Typischer Fehler'], [
            ['**Aufgabe** – eine einzelne Handlung', 'E-Mail zusammenfassen', 'Sekunden pro Vorgang', 'Etwas automatisieren, das im Gesamtablauf kaum Zeit kostet'],
            ['**Prozess** – mehrere Aufgaben mit Übergaben', 'Bewerber sichten', 'Durchlaufzeit, Fehlerquote', 'Schritte optimieren, aber Übergaben lassen – der Vorgang liegt genauso lange'],
            ['**Use-Case** – Problem, Prozess, Ziel und KI-Lösung', 'Erstbewertung von Bewerbungen nach definierten Skills', 'Geschäftswirkung: Kosten, Umsatz, Risiko', 'Geschäftswirkung versprechen, aber nur Aufgabenzeit messen']]) +
        merk('Wird nur bei einer einzelnen Aufgabe Zeit gespart, die Wartezeit davor und danach bleibt aber gleich, ändert sich für das Unternehmen nichts.') +
        folien(('uc', 11), ('uc', 12), ('uc', 13))))

    k.append(kapitel('c6', 'C6', 'Arbeitsauftrag 02 · Use-Case-Folie 14 · 2 × 20 + 5 Min.', 'Schmerz-Interview: fragen, was weh tut',
        P('Nicht fragen, was automatisiert werden soll – sondern was weh tut. Bildet Paare, eine Person fragt, eine antwortet. Nach 20 Minuten tauschen. Die vier Fragen in dieser Reihenfolge, nichts hinzufügen, nichts weglassen. **Antworten wörtlich notieren** – Zusammenfassungen sind schon Deutung.') +
        interview_tool(web) +
        merk('Fertig, wenn beide Rollen durchlaufen sind und die Antworten wörtlich notiert sind.') +
        korrektur('Use-Case-Folie 24', 'Dort ist von „den drei Fragen aus dem vorherigen Arbeitsauftrag“ die Rede. Folie 14 nennt vier Fragen – wir arbeiten mit allen vier.') +
        folien(('uc', 14))))

    k.append(kapitel('c7', 'C7', 'Freitag · Use-Case-Folien 15–16', 'Gute Use-Cases erkennen – und schlechte früh aussortieren',
        H('Sechs bekannte Merkmale') +
        P('Klar abgegrenzt · datenbasiert · real umsetzbar · messbar · wiederholbar · im Unternehmen verankert') +
        H('Drei, die meist fehlen') +
        karten([('!', 'Fehlertolerant oder korrigierbar', 'Ein Fehler bleibt folgenlos oder wird bemerkt und rückgängig gemacht. Gilt beides nicht, braucht es zwingend eine menschliche Freigabe.'),
                ('!', 'Es gibt einen Eigentümer', 'Eine benannte Person im Fachbereich steht nach dem Projekt für die Ergebnisse gerade. Sonst bemerkt niemand Auffälligkeiten.'),
                ('!', 'Ausreichendes Volumen', 'Was dreimal im Jahr vorkommt, rechnet sich fast nie – egal wie nervig es ist.')]) +
        H('Zehn Warnsignale') +
        tab(['Die fünf klassischen', 'Die fünf, die teuer werden'], [
            ['Zu allgemein – „Wir wollen KI im Marketing nutzen“', 'Der Prozess ändert sich gerade – dann wird Wegwerfarbeit gebaut'],
            ['Nicht datenbasiert – „Ich glaube, wir haben genug Infos“', 'Daten nur in Köpfen oder fremden PDFs – die halbe Lösung ist Datenbeschaffung'],
            ['Nicht priorisierbar – „Alles ist wichtig“', 'Niemand kann sagen, was „richtig“ ist – dann gibt es nichts zum Testen'],
            ['Nicht automatisierbar – braucht Kreativität oder komplexes Urteil', 'Ersparnis über viele Personen verstreut – 2 Minuten × 200 Personen werden nie nutzbare Zeit'],
            ['Kein echtes Problem – KI um der KI willen', 'Hochreguliert, ohne dass es jemand geprüft hat – Personalauswahl, Bonität, Gesundheitsdaten']]) +
        folien(('uc', 15), ('uc', 16))))

    persona = {
        'ingo': ('Ingo · Druck & Vertrieb', STECKBRIEF_BEISPIEL),
        'carmen': ('Carmen · Team & Website', [('name', 'Website-Anfragen vorsortieren'), ('eigentuemer', 'Teamleitung Kundenkontakt'),
            ('problem', 'Anfragen aus dem Kontaktformular landen ungeordnet in einem Postfach; Antworten dauern 3 Tage.'), ('ausloeser', 'Neue Formular-Einsendung'),
            ('input', 'Formularfelder: Name, Anliegen (Auswahl), Nachricht'), ('verarbeitung', 'Anliegen einordnen, Dringlichkeit markieren, Antwortentwurf vorbereiten'),
            ('output', 'Aufgabe im Team-Board + Antwortentwurf zur Freigabe'), ('volumen', '120 Anfragen pro Monat'), ('nutzen', '10 Stunden pro Monat im Team, Antwortzeit von 3 auf 1 Tag'),
            ('richtig_wenn', 'Kategorie stimmt mit der Einschätzung der Teamleitung überein'), ('nicht_dabei', 'Kein automatischer Versand, keine Preis- oder Vertragszusagen')]),
        'tabea': ('Tabea · Video & Design', [('name', 'Feedbackrunden zu Videoschnitten bündeln'), ('eigentuemer', 'Projektleitung Video'),
            ('problem', 'Feedback kommt verstreut per Mail und Chat; Änderungen werden übersehen.'), ('ausloeser', 'Neuer Kommentar im Freigabe-Link oder neue Mail mit Projektkürzel'),
            ('input', 'Kommentartext, Timecode, Projektname'), ('verarbeitung', 'Kommentare nach Projekt sammeln, nach Timecode sortieren, Doppelte markieren'),
            ('output', 'Eine Änderungsliste pro Schnittversion'), ('volumen', '60 Feedbackrunden pro Monat'), ('nutzen', '8 Stunden pro Monat im Schnitt-Team'),
            ('richtig_wenn', 'Jeder Kommentar steht genau einmal mit richtigem Timecode in der Liste'), ('nicht_dabei', 'Keine automatischen Schnittänderungen, keine Antworten an Kundschaft')])}
    order = [pid] + [x for x in persona if x != pid] if pid in persona else list(persona)
    labels = {key: label for key, label, _, _ in STECKBRIEF_FELDER}
    beispiele = ''.join(
        f'<div class="steck-bsp{" mein" if p == pid else ""}"><p class="steck-h">{E(persona[p][0])}{" · dein Bereich" if p == pid else ""}</p>' +
        tab(['Feld', 'Beispiel (erfunden)'], [[labels[key], val] for key, val in persona[p][1]], cls='steck-tab') + '</div>'
        for p in order)
    k.append(kapitel('c8', 'C8', 'Arbeitsauftrag 03 · Use-Case-Folie 17 · 55 Min.', 'Use-Case-Steckbriefe – was nicht ins Raster passt, ist noch eine Idee',
        flow([('01', 'Drei Kandidaten aus deiner Zeitfresser-Liste wählen, möglichst aus verschiedenen Bereichen.'),
              ('02', 'Je Kandidat die elf Felder der Reihe nach füllen – von „Name“ bis „Was gehört ausdrücklich nicht dazu“.'),
              ('03', 'Nutzenfeld: eine Zahl, eine Einheit, ein Zeitraum.'), ('04', 'Jedes Feld markieren, das du nicht füllen kannst. Markieren statt raten.')], cls='steps') +
        tab(['Nr.', 'Feld', 'So füllst du es'], [[str(i), f'**{label}**', hint] for i, (_, label, hint, _) in enumerate(STECKBRIEF_FELDER, 1)]) +
        korrektur('Folie 17', 'Die Folie nennt elf Felder, das Arbeitsheft mit dem genauen Raster lag uns nicht vor. Die elf Felder oben sind unser Vorschlag aus den Angaben der Folien 2 und 17 (Name … Volumen, Auslöser, Input, Output, Nutzen … „Was gehört ausdrücklich nicht dazu“). Gilt im Kurs ein anderes Raster, dieses verwenden.') +
        steckbrief_tool(web) +
        H('Drei fertige Beispiele zum Abgucken') + beispiele +
        merk('Fertig, wenn drei Steckbriefe stehen und jedes Nutzenfeld eine Zahl mit Einheit und Zeitraum trägt.') +
        tipp('Mit Make ausgeben', 'Vorlage A8 „Use-Case-Steckbrief“ macht aus den elf Feldern einen sauberen Text zum Kopieren.') +
        folien(('uc', 17))))

    k.append(kapitel('c9', 'C9', 'Freitag · Use-Case-Folien 19–20', 'Wie viel darf das System allein? Fünf Stufen',
        P('„Automatisiert“ ist keine Ja-Nein-Frage, sondern eine **Skala mit fünf Stufen**. Je höher, desto mehr Effizienz – und desto mehr Risiko, Nachweispflicht und rechtliche Anforderungen.') +
        tab(['Stufe', 'Name', 'Wer entscheidet?'], [
            ['0', 'Manuell', 'Mensch, ohne Unterstützung'], ['1', 'Assistenz', 'Mensch entscheidet, System schlägt vor'],
            ['2', 'Human-in-the-Loop', 'Mensch gibt jeden Fall frei'], ['3', 'Semi-Autonom', 'System entscheidet, Mensch prüft Stichproben und Ausnahmen'],
            ['4', 'Autonom', 'System entscheidet und handelt ohne Aufsicht – **für Entscheidungen über Menschen nicht zulässig**']]) +
        H('Die Stufe gilt pro Pfad, nicht pro Workflow') +
        karten([('01', 'Schaden bestimmt die Stufe', 'Je höher der Schaden eines Fehlers, desto niedriger die Stufe. Rechnungsfreigabe startet auf 2 und wandert nach der Testphase in Betragsgrenzen auf 3.'),
                ('02', 'Standard 3, Ausnahme 2', 'Dieses Muster deckt einen großen Teil aller realistischen Fälle ab.'),
                ('03', 'Steigen nur mit Messdaten', 'Eine Stufe darf steigen, wenn Messdaten es rechtfertigen. Genau dafür gibt es die Testphase.'),
                ('04', 'Menschen ≠ Stufe 4', 'Für Entscheidungen über Menschen ist Stufe 4 in der Endentscheidung nicht zulässig.')], cols=2) +
        achtung('Der häufigste Denkfehler', 'Ein Mensch, der bestätigt, ist nur dann echte Stufe 2, wenn er tatsächlich prüfen kann und Zeit dafür hat. Wer 200 Vorschläge am Tag durchklickt, ist faktisch Stufe 4 – mit allen Risiken, aber ohne Kontrolle.') +
        folien(('uc', 19), ('uc', 20))))

    k.append(kapitel('c10', 'C10', 'Freitag · Use-Case-Folien 21–22', 'Braucht es überhaupt KI? Die Entscheidungstreppe',
        P('Nicht jede Automatisierung braucht ein Sprachmodell. Von oben nach unten fragen und **beim ersten Ja stehen bleiben** – jede Stufe weiter unten kann mehr, kostet aber Nachvollziehbarkeit.') +
        treppe_tool(web) +
        P('Grundlage aller Stufen: Anbindung über Schnittstellen – Daten holen und schreiben, statt Oberflächen zu bedienen.') +
        H('Fallbeispiel Rechnungsfreigabe: Das Modell liest – die Regel entscheidet') +
        tab(['Das Sprachmodell …', 'Die Regel …'], [
            ['liest die Rechnung und zieht vier Felder heraus: Betrag, Lieferant, Kostenstelle, Bestellbezug', 'prüft: Lieferant im Stammdatensatz?'],
            ['gibt je Feld an, wie sicher die Erkennung war', 'gültiger Bestellbezug? · Betrag unter 1.000 €? · Sicherheit über der Schwelle?']]) +
        karten([('✓', 'Begründbar', 'Jede Freigabe lässt sich erklären – genau das braucht die Dokumentation.'), ('✓', 'Testbar', 'Die Entscheidungslogik ist deterministisch.'),
                ('✓', 'Günstig', 'Das Modell läuft nur einmal je Rechnung.'), ('✓', 'Leicht zu ändern', 'Neue Betragsgrenze = eine Zahl ändern, kein Prompt, kein neuer Modelltest.')], cols=2) +
        tipp('Selbst ausprobieren', 'Vorlage A9 „Rechnungs-Regel“ baut genau diese Regel mit UND/ODER-Filtern – ohne KI-Konto.') +
        folien(('uc', 21), ('uc', 22))))

    k.append(kapitel('c11', 'C11', 'Freitag · Use-Case-Folien 24–26', 'Wo man Use-Cases systematisch findet',
        karten([('1', 'Zeitfresser-Analyse (von unten)', 'Eine Woche lang jede wiederkehrende Tätigkeit mit Dauer und Häufigkeit notieren. Auswertung: Häufigkeit × Dauer.'),
                ('2', 'Prozess-Inventur (von oben)', 'Alle Kernprozesse auflisten und je Prozess schätzen: Volumen pro Monat, Anteil Handarbeit, Systemwechsel, Fehlerhäufigkeit. Hohe Werte überall = Kandidat.'),
                ('3', 'Schmerz-Interviews', 'Die vier Fragen aus Arbeitsauftrag 02.'),
                ('4', 'Datenspuren auswerten', 'Tickets, Postfächer, CRM-Verläufe zeigen objektiv, wo Menge entsteht. Drei Monate Betreffzeilen im Support liefern eine belastbare Kategorienliste – und gleich die Testdaten.')], cols=2) +
        merk('Ergebnis dieser Phase ist eine Liste, keine Entscheidung. Zehn bis fünfzehn grob beschriebene Kandidaten sind ein gutes Ergebnis.') +
        H('Hohe Trefferquote – oft übersehen') +
        tab(['Bereich', 'Typische Kandidaten'], [
            ['Finanzen & Buchhaltung', 'Rechnungseingang mit Datenauslese und Freigabevorbereitung · Mahnwesen nach Regelwerk · Belegprüfung Reisekosten · Auffälligkeiten in Buchungen'],
            ['Kundenservice & Support', 'Eingänge einordnen und weiterleiten · Antwortentwürfe aus der Wissensdatenbank mit Freigabe · lange Ticketverläufe zusammenfassen · wiederkehrende Ursachen erkennen'],
            ['Operations, Einkauf, Logistik', 'Bestellung, Lieferschein und Rechnung abgleichen · Lieferanten-Rückfragen strukturiert erfassen · Termin- und Kapazitätsmeldungen aus Mails in Systemdaten überführen'],
            ['IT & Verwaltung', 'Zugänge nach Rollenprofil anlegen und entziehen · Störungsmeldungen auswerten · Dokumentation aktuell halten']]) +
        f'<blockquote class="kernsatz">Der Großteil produktiver Automatisierung besteht darin, unstrukturierte Eingänge in strukturierte Daten zu verwandeln – und anschließend nach Regeln damit zu arbeiten.<cite>Use-Case-Folie 26</cite></blockquote>' +
        folien(('uc', 24), ('uc', 25), ('uc', 26))))

    k.append(kapitel('c12', 'C12', 'Freitag · Use-Case-Folien 27–29', 'HR, Marketing, Vertrieb – und die Fallstricke',
        tab(['Bereich', 'Typische Use-Cases', 'Darauf achten'], [
            ['**HR**', 'CV-Screening · Onboarding-Unterlagen · persönliche Trainingspläne', 'Bewerbende bewerten, filtern oder ranken gilt nach der EU-KI-Verordnung in der Regel als **Hochrisiko**. Tragfähig: „KI strukturiert Bewerbungen und legt sie mit Begründung zur menschlichen Bewertung vor.“'],
            ['**Marketing**', 'Social-Media-Planung · Inhalte in andere Formate bringen · Keyword-Recherche · Bestandsinhalte durchsuchbar machen · Kampagnen auswerten · Übersetzung mit Endprüfung', 'Kennzeichnung KI-generierter Veröffentlichungen gehört in den Workflow-Endpunkt'],
            ['**Vertrieb**', 'Lead-Qualifizierung · Angebotszusammenfassungen · Follow-ups · Leads um Zusatzinfos anreichern', 'Lead-Scoring mit Einfluss auf Konditionen kann eine Datenschutz-Folgenabschätzung auslösen; automatischer Erstversand von Werbemails ist rechtlich besonders heikel']]) +
        korrektur('Use-Case-Folie 27', 'Art. 22 DSGVO verbietet ausschließlich automatisierte Entscheidungen mit rechtlicher oder ähnlich erheblicher Wirkung **grundsätzlich** – mit engen Ausnahmen (Vertrag, Gesetz, ausdrückliche Einwilligung) und dann mit Schutzmaßnahmen wie dem Recht auf menschliches Eingreifen. Für die Praxis bleibt die Folienregel richtig: keine vollautomatischen Absagen. Ab wann die Hochrisiko-Pflichten der KI-Verordnung genau greifen, hängt vom aktuellen Stand der EU-Änderungen ab – vor einem echten Projekt prüfen.') +
        korrektur('Use-Case-Folie 28', 'Die Transparenzpflichten der KI-Verordnung (Art. 50) gelten ab 2. August 2026. Für Anwender betreffen sie vor allem Deepfakes und KI-erzeugte Texte, die die Öffentlichkeit über Angelegenheiten von öffentlichem Interesse informieren – mit Ausnahme, wenn ein Mensch redaktionell prüft und verantwortet. Nicht jeder Marketingtext ist automatisch kennzeichnungspflichtig. Anbieter generativer Systeme müssen Ausgaben maschinenlesbar markieren. Im Zweifel und bei Werbemails: rechtlich prüfen lassen.') +
        H('Drei Zahlen aus der Praxis – und wie man sie prüft') +
        tab(['Behauptung', 'Prüffrage'], [
            ['**70 %** – Agentur: KI übernimmt 70 % der Vorformulierungen beim Content-Recycling', '**Bezugsgröße:** 70 % wovon, gemessen woran? Ohne Ausgangsmessung wertlos.'],
            ['**400** – SaaS-Firma: KI bewertet 400 Leads nach Idealkundenprofil', '**Restaufwand:** Was kostet die Nachbearbeitung? 70 % fertiger Entwurf mit 80 % Korrekturzeit spart nichts.'],
            ['**8 h** – Mittelständler: KI übernimmt erstes Screening von 200 Bewerbungen/Monat, spart 8 h/Woche', '**Realisierung:** 8 Stunden verteilt auf fünf Personen oder gebündelt bei einer? Nur gebündelte Zeit wird nutzbar.']]) +
        merk('Jede Zahl ist eine Behauptung, bis sie nachgerechnet ist.') +
        folien(('uc', 27), ('uc', 28), ('uc', 29))))

    k.append(kapitel('c13', 'C13', 'Arbeitsauftrag 04 · Use-Case-Folien 30–31 · 40 + 30 Min.', 'Ausschlusskriterien und Kreuzverhör',
        tab(['Ausschlusskriterium', 'Warum es nicht wegzurechnen ist'], [
            ['Kein Zugriff auf die nötigen Daten', 'Technisch oder rechtlich. Die halbe Lösung wäre ein Datenbeschaffungsprojekt – gesondert entscheiden.'],
            ['Kein Verantwortlicher im Fachbereich', 'Nach der Übergabe bemerkt niemand Auffälligkeiten.'],
            ['Rechtlich unzulässige Zielsetzung', 'Etwa die vollautomatische Absage im Bewerbungsprozess. Kein Zuschnitt und kein Budget ändern daran etwas.'],
            ['Kein definierbarer richtiger Output', 'Entscheiden zwei Erfahrene denselben Fall unterschiedlich, gibt es nichts zum Testen. Erst eine Entscheidungsregel schaffen.'],
            ['Der Prozess wird gerade umgestellt', 'Erst den Zielprozess klären, dann automatisieren.']]) +
        flow([('Allein · 40 Min.', 'Je Kandidat Stufe für Standardfall und Ausnahme mit Begründung. Prüffrage: Hat die prüfende Person Zeit und Information zu widersprechen? Wenn nein: die faktisch höhere Stufe eintragen. Dann die fünf Kriterien abhaken.'),
              ('Dreiergruppe · 30 Min.', 'Eine Person stellt einen Kandidaten in 3 Minuten vor. Die anderen nennen **nur Warnsignale** – nicht loben, nicht verbessern, nicht ermutigen. Jede Person notiert die drei stärksten Einwände.')]) +
        stufen_tool(web) +
        merk('Fertig, wenn jede Person drei fremde Einwände notiert hat. Wer keinen bekommen hat, hat zu vage vorgetragen.') +
        folien(('uc', 30), ('uc', 31))))

    k.append(kapitel('c14', 'C14', 'Freitag · Use-Case-Folie 32', 'Was heute entstanden ist – und wie es weitergeht',
        P('Im Heft steht jetzt: eine gerechnete Zeitfresser-Liste, drei Steckbriefe, je ein festgelegter Automatisierungsgrad, geprüfte Ausschlusskriterien und drei fremde Einwände je Kandidat.') +
        P('**Im nächsten Block** werden die Kandidaten nach vier Kriterien bewertet – dabei passiert ein Rechenfehler, den fast jede Gruppe macht. Danach wird für den stärksten Fall gerechnet, ob er sich überhaupt lohnt.') +
        tipp('Freiwillige Hausaufgabe', 'Für deinen aussichtsreichsten Kandidaten die tatsächlichen Volumenzahlen besorgen, statt sie zu schätzen. Wer mit echten Zahlen kommt, rechnet einen echten Business Case statt einer Übung. Dabei nur Zahlen verwenden, die du weitergeben darfst.') +
        folien(('uc', 32))))
    return teil('teil-c', 'C', 'Freitag: Use Cases identifizieren', 'Vom Zeitfresser zum geprüften Kandidaten – mit allen vier Arbeitsaufträgen zum Ausfüllen.', ''.join(k))


# ================================================================ Teil D · Mitnehmen

def spickzettel():
    return kapitel('d1', 'D1', 'Die Woche auf einer Seite', 'Spickzettel',
        '<div class="spick">' + ''.join(f'<div class="spick-box"><h4>{E(t)}</h4><ul>' + ''.join(f'<li>{md(x)}</li>' for x in items) + '</ul></div>' for t, items in [
            ('Grundidee', ['Festes Gerüst + KI nur an einzelnen Stellen', 'Auslöser → Daten holen → Verarbeiten → Ergebnis', 'Workflow statt Agent, wenn es wiederholbar sein soll']),
            ('Make bedienen', ['Free: 1.000 Credits, 2 aktive Szenarien, ab 15 Min.', 'Testen mit **Run once**, Zeitplan aus', 'Ergebnis in der Sprechblase → OUTPUT', 'Import: … → Import blueprint']),
            ('Daten', ['JSON = Feldname: Wert', 'String, Number, Boolean, Null, Object, Array', 'Parse JSON zerlegt Text in Felder', 'Mapping `{{1.feld}}` = Wert aus Modul 1']),
            ('Steuern', ['Filter = Tür, Router = Weiche', 'AND = alle, OR = eine', 'Webhook = sofort (Push)', 'Router/Filter kosten selbst keine Credits']),
            ('KI-Schritte', ['System-Prompt = Rolle + Regeln', 'Antwort als JSON mit erlaubten Werten', 'Zehnmal testen, Feld „unsicher“', 'Mensch vor Außenwirkung']),
            ('API & Zeit', ['GET liest, 200 = Abruf ok', 'ISO 8601 mit Z oder Offset', 'formatDate(…; "DD.MM.YYYY HH:mm"; "Europe/Berlin")', 'Winter +01:00, Sommer +02:00']),
            ('Use-Case finden', ['Häufigkeit × Minuten = Zeitfresser', 'Problem + KI-Teil + Mehrwert', 'Nutzen = Zahl + Einheit + Zeitraum', 'Eigentümer, Volumen, korrigierbar']),
            ('Zuschnitt', ['Stufen 0–4, pro Pfad', 'Standard 3, Ausnahme 2', 'Erst Regel, dann KI, Agent zuletzt', 'Fünf Ausschlusskriterien zuerst'])]) + '</div>')


def klassenbuch():
    return kapitel('d2', 'D2', 'Plan nach Folien – nicht das Protokoll des Unterrichts', 'Wochenrückblick: fünf Stichpunkte pro Tag',
        ''.join(f'<div class="kb-tag"><p class="kb-h"><b>{E(d)}</b> – {E(t)}</p><ul>' + ''.join(f'<li>{E(x)}</li>' for x in pts) + '</ul></div>' for d, t, pts in KLASSENBUCH))


def woerter():
    return kapitel('d3', 'D3', 'Alle Fachwörter der Woche', 'Wörterliste', glossar([(a, b, '') for a, b in BEGRIFFE]))


def quellen():
    rows = [
        ('Make: Pricing / Free-Plan', 'https://www.make.com/en/pricing'), ('Make: Credits', 'https://help.make.com/credits'),
        ('Make: Operations', 'https://help.make.com/operations'), ('Make: Scenario blueprints (Import/Export)', 'https://help.make.com/blueprints'),
        ('Make: Mapping', 'https://help.make.com/mapping'), ('Make: Filter', 'https://help.make.com/filtering'), ('Make: Router', 'https://help.make.com/router'),
        ('Make: HTTP-App', 'https://apps.make.com/http'), ('Make: JSON-App', 'https://apps.make.com/json'), ('Make: Webhooks', 'https://help.make.com/webhooks'),
        ('Make: Datums- und Zeitfunktionen', 'https://help.make.com/date-and-time-functions'), ('JSONPlaceholder (Test-API)', 'https://jsonplaceholder.typicode.com/'),
        ('EU-KI-Verordnung (Verordnung (EU) 2024/1689)', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj'), ('DSGVO Art. 22', 'https://eur-lex.europa.eu/eli/reg/2016/679/oj')]
    return kapitel('d4', 'D4', 'Stand 30.10.2026', 'Quellen, Prüfstand und Grenzen',
        P('Make-Angaben (Free-Plan, Credits, Oberfläche, Blueprint-Import) wurden am 26.–30.10.2026 mit den offiziellen Hilfeseiten abgeglichen. Das Format der neun Vorlagen wurde mit echten Make-Exporten abgeglichen. **Die Vorlagen wurden nicht in euren Konten ausgeführt;** Credit-Angaben sind Planwerte. Die Test-API wurde am 30.10.2026 direkt abgerufen (HTTP 200, Werte wie in A5).',
          'Alle Firmen, Namen und Zahlen in Beispielen sind erfunden. Zahlen und Studien aus den Use-Case-Folien sind als Angaben der Folie wiedergegeben. Rechtliche Hinweise sind Einordnung, keine Rechtsberatung.') +
        '<ul class="quellen">' + ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{E(n)}</a><br><small>{E(u)}</small></li>' for n, u in rows) + '</ul>')


def teil_d():
    return teil('teil-d', 'D', 'Mitnehmen', 'Spickzettel, Wochenrückblick, Wörter und Quellen.', spickzettel() + klassenbuch() + woerter() + quellen())


TOC = [('teil-a', 'A · Make-Grundlagen', [('a1', 'Was KI-Automation heißt'), ('a2', 'Die wichtigsten Wörter'), ('a3', 'KI-Schritte streuen'),
        ('a4', 'Werkzeug, Kosten, Abläufe'), ('a5', 'Make 2026: Fläche & Budget'), ('a6', 'Erster Ablauf'), ('a7', 'Folienübung Mail → Excel'),
        ('a8', 'JSON & Datenfluss'), ('a9', 'Filter, Router, Webhooks'), ('a10', 'KI im Workflow'), ('a11', 'API & Zeit')]),
       ('teil-b', 'B · Make-Werkstatt', [('b0', 'So importierst du')] + [(f'vorlage-a{a["nr"]}', f'A{a["nr"]} {a["titel"]}') for a in AUTOMATIONS]),
       ('teil-c', 'C · Use Cases (Freitag)', [('c1', 'Ziel des Tages'), ('c2', 'Ausgangslage'), ('c3', 'Ursachen & Erfolg'), ('c4', '01 Zeitfresser'),
        ('c5', 'Was ein Use-Case ist'), ('c6', '02 Schmerz-Interview'), ('c7', 'Gut oder schlecht?'), ('c8', '03 Steckbriefe'), ('c9', 'Autonomie-Stufen'),
        ('c10', 'Braucht es KI?'), ('c11', 'Wo man sucht'), ('c12', 'HR, Marketing, Vertrieb'), ('c13', '04 Ausschluss & Kreuzverhör'), ('c14', 'Ergebnis & Ausblick')]),
       ('teil-d', 'D · Mitnehmen', [('d1', 'Spickzettel'), ('d2', 'Wochenrückblick'), ('d3', 'Wörter'), ('d4', 'Quellen & Grenzen')])]
