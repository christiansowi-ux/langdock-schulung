"""A small JSON-to-text lesson, 27 October 2026, with no external accounts."""
from .content import BRIEF
import json
RESEARCH_DATE='27.10.2026'
VARIANT=dict(projekt='Nordlicht',thema='Interview vorbereiten',kanal='Internes Projektbriefing',status='ENTWURF')
QUIZ=[
 ('Was macht der Baustein Parse JSON in unserer Übung?',['Er macht aus dem JSON-Text vier auswählbare Felder','Er veröffentlicht einen Instagram-Beitrag','Er schreibt automatisch eine E-Mail'],0,'Parse JSON liest die beschrifteten Angaben. Der nächste Baustein kann projekt, thema, kanal und status einzeln übernehmen.'),
 ('Wie änderst du das Thema richtig?',['Du benennst das Feld thema in etwas anderes um','Du lässt thema stehen und änderst nur den Text rechts vom Doppelpunkt','Du entfernst alle Anführungszeichen'],1,'Der Feldname thema bleibt gleich. Nur sein Inhalt wird ausgetauscht. So findet der zweite Baustein das Feld weiterhin.'),
 ('Du hast im ersten Baustein das Thema geändert. In der neuen Ausgabe steht trotzdem das alte Thema. Was prüfst du?',['Ob das Thema im zweiten Baustein fest getippt statt als Datenfeld ausgewählt wurde','Ob du ein größeres KI-Abo brauchst','Ob du sofort alle Abläufe löschen musst'],0,'Ein fest getippter Text bleibt unverändert. Ein ausgewähltes Datenfeld übernimmt den Wert aus dem aktuellen Lauf. Prüfe auch, ob du das neueste Ergebnis ansiehst.'),
 ('Brauchst du für unsere Hauptübung ein Outlook- oder Instagram-Konto?',['Ja, sonst geht JSON nicht','Nein. Die zwei Bausteine arbeiten mit unseren Testangaben nur in Make','Ja, und eine bezahlte KI-API dazu'],1,'Die Hauptübung liest Testangaben und zeigt einen Text in Make an. Das Outlook-Excel-Beispiel der Folien hat zusätzliche Voraussetzungen und steht im Zusatzteil.')
]

def output(data):
 return '\n'.join(['Projekt: '+data['projekt'],'Thema: '+data['thema'],'Kanal: '+data['kanal'],'Status: '+data['status'],'Noch keine Veröffentlichung.'])

def core(make_page):
 def p(key,title,blocks,section='Schritt für Schritt',**extra):
  return dict(make_page(key,title,blocks,2,section),**extra)
 return [
 p('start','Heute wird aus vier Angaben ein übersichtlicher Text',[
  ('p','Gestern hast du einen Namen in eine Begrüßung eingesetzt. Heute übernimmst du vier Angaben: Projekt, Thema, Kanal und Status. Make setzt sie zu einem kleinen Zettel zusammen. Diesen Vorbereitungszettel nennt man auch Briefing.'),
  ('flow',['Vier beschriftete Angaben eingeben','Die Angaben einzeln auswählen','Einen übersichtlichen Text in Make lesen']),
  ('h','Am Ende kannst du drei Dinge'),
  ('p','1. Ein einfaches JSON-Beispiel lesen.\n2. Vier Angaben in einen Text übernehmen.\n3. Die Angaben ändern und das neue Ergebnis prüfen.'),
  ('note','Du brauchst nur deinen vorhandenen Make-Free-Account. Es wird kein Beitrag veröffentlicht und keine Nachricht verschickt. Der automatische Zeitplan bleibt aus.'),
  ('p','Lies erst „Verstehen“. Baue danach die sechs kleinen Schritte nach. Zum Schluss kommen vier Quizfragen. Deine Quizantworten werden auf diesem Gerät in diesem Browser gespeichert; die Anzeige sagt dir, ob das geklappt hat.')], 'Dein Ziel für Dienstag'),
 p('wiedereinstieg','Falls du gestern gefehlt hast: Das reicht für heute',[
  ('table',(['Wort auf dem Bildschirm','Einfach erklärt'],[['Scenario / Szenario','Der ganze Ablauf auf der Arbeitsfläche.'],['Module / Modul','Ein einzelner Baustein. Er erscheint als Kreis.'],['Run once','Einmal ausführen. Du startest selbst.'],['Input / Output','Das geht hinein / das kommt heraus.'],['Mapping','Ein Datenfeld aus einem früheren Baustein auswählen.']])),
  ('p','Du musst den gestrigen Ablauf nicht öffnen oder verändern. Wir beginnen heute mit einem eigenen neuen Szenario. Du kannst alle Schritte mit den vorbereiteten Testangaben nachvollziehen.'),
  ('check','Erkläre dir selbst: Ich baue einen Ablauf aus zwei Bausteinen. Der erste liest Angaben, der zweite setzt daraus einen Text zusammen.')]),
 p('json','JSON ist wie ein Zettel mit beschrifteten Feldern',[
  ('p','Stell dir diesen kleinen Zettel vor:'),
  ('table',(['Beschriftung','Was auf dem Zettel steht'],[['projekt','Papierfunke'],['thema','Workshop am 30.10.'],['kanal','Instagram'],['status','ENTWURF']])),
  ('p','Ohne Beschriftung wäre „Papierfunke, Workshop, Instagram“ schwerer zuzuordnen. Die Beschriftungen sagen Make genau, welche Angabe wofür gedacht ist.'),
  ('h','Und was ist daran JSON?'),
  ('p','JSON ist eine feste Schreibweise für solche Angaben. Computerprogramme können sie gut austauschen und wieder auseinanderlesen. Es ist keine KI und du musst dafür heute nicht programmieren.'),
  ('note','Instagram ist in unserem Beispiel nur Text auf dem Zettel. Dieses Wort verbindet kein Konto und veröffentlicht nichts.')]),
 p('json-regeln','Du musst nur diese Schreibregeln erkennen',[
  ('code','{\n  "thema": "Workshop am 30.10."\n}'),
  ('p','Links steht der Feldname thema. Rechts steht sein Inhalt Workshop am 30.10. Der Doppelpunkt trennt beides. Die doppelten Anführungszeichen gehören bei diesen Texten dazu.'),
  ('table',(['Zeichen','Bedeutung'],[['{ und }','Hier beginnt und endet der gesamte Zettel.'],['"thema"','Die Beschriftung eines Feldes.'],[':','Jetzt folgt der Inhalt dieses Feldes.'],['"Workshop am 30.10."','Der Text, der in diesem Feld steht.'],[',','Trennt zwei Felder. Hinter dem letzten Feld steht kein Komma.']])),
  ('note','Für unsere Übung kopierst du das vollständige Muster im Bauschritt. Keine zusätzlichen ```-Zeichen, Überschriften oder Erklärsätze mitkopieren. Ändere zunächst keine Klammern oder Feldnamen.')],code_role='sample'),
 p('mapping','Vier Werte übernehmen - statt alles fest einzutippen',[
  ('p','Wenn du den fertigen Satz „Projekt: Papierfunke“ vollständig in den zweiten Baustein tippst, bleibt Papierfunke dort fest stehen. Auch dann, wenn das Projekt vorne inzwischen anders heißt.'),
  ('p','Deshalb tippst du nur „Projekt: “ und wählst danach das Feld projekt aus dem ersten Baustein. So wird immer dessen aktueller Inhalt eingesetzt. Für Thema, Kanal und Status machst du es genauso.'),
  ('flow',['Feste Beschriftung: Projekt: plus Leerzeichen','Ausgewähltes Feld: projekt','Später im Ergebnis: Projekt: Papierfunke']),
  ('check','Merksatz: Die Beschriftung tippe ich. Den wechselnden Inhalt wähle ich als Datenfeld aus.'),
  ('note','Ein farbiges Datenfeld ist nicht dasselbe wie getippter Text in eckigen Klammern. Tippe also nicht [projekt] als Ersatz für die Auswahl ein.')]),
 p('budget','Klein testen und den Verbrauch im Blick behalten',[
  ('p','Wir bauen nur zwei Bausteine. Der erste verarbeitet genau einen Zettel, also ein JSON-Objekt. In Make heißt dieses zusammengehörige Datenpäckchen Bundle.'),
  ('table',(['Geplanter Versuch','Rechenbeispiel'],[['Ersten Baustein allein einmal testen','1 Credit'],['Beide Bausteine mit dem ersten Beispiel ausführen','2 Credits'],['Beide Bausteine mit geänderten Angaben ausführen','2 Credits'],['Zusammen','Ungefähr 5 Credits']])),
  ('note','Das sind Planwerte für unsere einfachen Bausteine und ein Datenpäckchen, keine Messung deines Kontos. Weitere Tests oder Fehler können zusätzlich verbrauchen. Prüfe den echten Zähler vorher und nachher. Die selbst gesetzten 50 Lerncredits gelten für die gesamte Vier-Tage-Reihe, nicht für jeden Tag neu.'),
  ('p','Lass die automatische Planung aus. Heute bestimmst du selbst, wann Run once startet. Verwende erfundene Angaben wie im Beispiel.')]),
 p('wf2','Schritt 1: Ein neues Szenario mit JSON öffnen',[
  ('h','Mach das'),
  ('p','1. Öffne Make und gehe zu Scenarios.\n2. Erstelle ein neues eigenes Szenario. Den gestrigen Ablauf lässt du bestehen.\n3. Nenne den neuen Ablauf M2-02 Redaktionsbriefing.\n4. Suche über das Plus die App JSON.\n5. Wähle darin Parse JSON. Das bedeutet: JSON-Text in einzelne Felder zerlegen.\n6. Lass die automatische Planung aus.'),
  ('h','So sieht es richtig aus'),
  ('p','Du hast zunächst genau einen Baustein: Parse JSON. Der zweite kommt erst nach der ersten erfolgreichen Probe dazu.'),
  ('note','Die JSON-App braucht keine Verbindung zu einem zusätzlichen Konto. Für diese Übung gibt es nichts in Instagram, Outlook oder einem KI-Dienst anzumelden. [M8]')]),
 p('wf2-daten','Schritt 2: Die vier Testangaben einfügen',[
  ('h','Mach das'),
  ('p','1. Kopiere nur den folgenden JSON-Text. Im Web hilft dir der Kopieren-Knopf.\n2. Füge ihn im Baustein Parse JSON in das Feld JSON string ein.\n3. Lass Data structure zunächst leer, wenn das angeboten wird.\n4. Bestätige den Baustein und speichere den Ablauf. Noch keinen zweiten Baustein anschließen.'),
  ('json',BRIEF),
  ('h','Was bedeutet Data structure?'),
  ('p','Das ist eine Beschreibung, welche Felder Make erwarten soll. Bei unserem einfachen Beispiel kann Make sie beim ersten manuellen Lauf aus dem Muster erkennen. Du musst dafür heute kein eigenes Schema entwerfen.'),
  ('note','Der Text oben sind Übungsdaten für JSON string. Er ist keine importierbare Make-Vorlage und gehört nicht zu „Import blueprint“. Der nächste Schritt ist Run once. [M8]')],code_role='input'),
 p('wf2-felder','Schritt 3: Prüfen, ob vier Felder angekommen sind',[
  ('h','Mach das'),
  ('p','1. Prüfe: Bisher ist nur Parse JSON auf der Arbeitsfläche.\n2. Klicke auf Run once.\n3. Öffne danach die kleine Ergebnis-Anzeige am ausgeführten Baustein. Sie erscheint häufig als weißer Kreis mit einer Zahl.\n4. Klappe bei Bedarf Output auf. Suche die vier Felder projekt, thema, kanal und status.'),
  ('table',(['Feld','Erwarteter Inhalt'],[[k,v] for k,v in BRIEF.items()])),
  ('h','So sieht es richtig aus'),
  ('p','Du siehst die vier Angaben getrennt voneinander. Der erste Baustein hat den Text lesbar aufgeteilt. Erst jetzt fügst du den nächsten hinzu.'),
  ('h','Falls es nicht klappt'),
  ('p','Ein JSON-Fehler? Kopiere das vollständige Muster noch einmal. Prüfe besonders Anführungszeichen und Kommas. Keine Felder zur Auswahl? Kontrolliere, ob dieser erste Lauf tatsächlich erfolgreich war.'),
  ('note','Wenn deine Oberfläche eine Struktur ausdrücklich verlangt: Data structure → Add → Generator öffnen, dasselbe Muster als Beispieldaten einfügen und speichern. Danach den Baustein erneut testen. Menübezeichnungen können abweichen. [M8]')]),
 p('wf2-text','Schritt 4: Den Text aus vier Datenfeldern bauen',[
  ('h','Mach das'),
  ('p','1. Füge rechts hinter Parse JSON einen zweiten Baustein hinzu.\n2. Suche Tools → Compose a string. Damit setzt du Text zusammen.\n3. Klicke in dessen Feld Text. Tippe Projekt: und danach ein Leerzeichen.\n4. Wähle dann aus dem ersten Baustein das Datenfeld projekt aus.\n5. Beginne eine neue Zeile: Tippe Thema: plus Leerzeichen und wähle thema.\n6. Ergänze auf die gleiche Weise die Zeilen Kanal: mit kanal und Status: mit status.\n7. Schreibe in eine letzte neue Zeile fest: Noch keine Veröffentlichung.\n8. Bestätige und speichere.'),
  ('table',(['Diesen Text tippst du','Dieses Feld wählst du aus'],[['Projekt: plus Leerzeichen','projekt'],['Thema: plus Leerzeichen','thema'],['Kanal: plus Leerzeichen','kanal'],['Status: plus Leerzeichen','status']])),
  ('h','So sieht es richtig aus'),
  ('p','Dein Textfeld enthält feste Beschriftungen und vier ausgewählte farbige Datenfelder. Die Texte Papierfunke und Workshop am 30.10. tippst du hier nicht als Ersatz für die Felder ein.'),
  ('note','Die Feldliste fehlt? Gehe zur erfolgreichen Ausgabe aus Schritt 3 zurück und prüfe die Verbindung zwischen den beiden Bausteinen. Erst Daten bereitstellen, dann auswählen.')]),
 p('wf2-ergebnis','Schritt 5: Deinen ersten Vorbereitungszettel lesen',[
  ('h','Mach das'),
  ('p','1. Speichere beide verbundenen Bausteine.\n2. Starte den gesamten Ablauf mit Run once.\n3. Öffne die aktuelle Ausgabe des zweiten Bausteins.\n4. Vergleiche Zeile für Zeile mit dem erwarteten Text.'),
  ('code',output(BRIEF)),
  ('check','Stehen alle vier Werte neben der richtigen Beschriftung? Sind Datum und Status unverändert? Ein grünes Symbol zeigt einen technisch ausgeführten Schritt, aber noch keinen inhaltlich richtigen Text.'),
  ('note','Das Wort Instagram beschreibt nur den vorgesehenen Kanal. Dieser Ablauf hat keinen Beitrag erstellt oder veröffentlicht. Die Ausgabe steht nur in Make.')],code_role='expected'),
 p('wf2-test','Schritt 6: Andere Angaben, derselbe Ablauf',[
  ('p','Jetzt prüfen wir, ob der zweite Baustein wirklich die aktuellen Angaben übernimmt. Tausche dafür nur die Testdaten im ersten Baustein aus.'),
  ('json',VARIANT),
  ('h','Mach das'),
  ('p','1. Öffne den ersten Baustein Parse JSON.\n2. Ersetze den bisherigen Inhalt von JSON string durch dieses zweite Beispiel. Die vier Feldnamen bleiben gleich.\n3. Bestätige und speichere. Den zweiten Baustein änderst du nicht.\n4. Starte den gesamten Ablauf erneut mit Run once.\n5. Öffne die neueste Ausgabe des zweiten Bausteins.'),
  ('check','Jetzt sollen Projekt: Nordlicht, Thema: Interview vorbereiten und Kanal: Internes Projektbriefing erscheinen. Status bleibt ENTWURF. Wenn das ohne Änderung des zweiten Bausteins klappt, funktioniert deine Zuordnung.'),
  ('note','Mit der Einzelprobe und den beiden vollständigen Läufen sind wir im Rechenbeispiel bei ungefähr 5 Credits. Lass den Zeitplan aus und speichere. Die Hauptübung ist fertig.')],code_role='input'),
 p('hilfe','Falls dein Ergebnis anders aussieht',[
  ('table',(['Beobachtung','Was du prüfst'],[['Make meldet ungültiges JSON','Vollständiges Muster kopiert? Gerade doppelte Anführungszeichen? Kein Komma direkt vor der letzten schließenden Klammer?'],['Die vier Felder fehlen in der Auswahl','Zuerst nur Parse JSON erfolgreich ausführen. Dann den zweiten Baustein ergänzen.'],['Es bleibt beim alten Thema','Im zweiten Baustein das Feld thema auswählen, statt den alten Inhalt fest einzutippen.'],['Projekt und Thema sind vertauscht','Bei Projekt: muss projekt ausgewählt sein, bei Thema: das Feld thema.'],['Ein altes Ergebnis steht noch da','Den zuletzt ausgeführten Lauf öffnen. Frühere Ergebnisse ändern sich nicht nachträglich.']])),
  ('p','Ändere immer erst die vermutete Fehlerstelle und starte dann gezielt neu. Viele Starts hintereinander erklären den Fehler nicht und können Guthaben verbrauchen.'),
  ('note','Du musst für die Hauptübung nicht absichtlich kaputtes JSON in Make ausführen. Zum Verstehen reicht: Fehlt ein Anführungszeichen, kann der Text nicht korrekt gelesen werden. Spätere Fehlerproben brauchen eigenes Restbudget.')]),
 p('quiz','Vier Fragen zu deinem Datenzettel',[
  ('quiz',None),('p','Du darfst nachlesen und Antworten ändern. Der Speicherstatus gilt für dieses Gerät und diesen Browser. Bei gesperrtem Speicher kannst du den Stand als Text herunterladen. Die PDF-Lösungen folgen auf der nächsten Seite.')], 'Dein Selbstcheck'),
 p('antworten','Die Lösungen mit einfachen Erklärungen',[
  ('p',str(n)+'. Antwort '+ 'ABC'[right]+': '+why) for n,(_,_,right,why) in enumerate(QUIZ,1)
 ]+[('check','Erkläre den Unterschied: Feldname und Feldinhalt. Warum ändert der zweite Test nur die Inhalte?')], 'Nachsehen'),
 p('mitnahme','Das behältst du von heute',[
  ('p','JSON ist eine feste Schreibweise für beschriftete Angaben. Parse JSON macht die Felder einzeln nutzbar. Durch Mapping wählst du die passenden Felder im nächsten Baustein aus.'),
  ('h','Dein eigener kurzer Merkzettel'),
  ('p','Meine vier Felder heißen: ______________________________\nIm zweiten Baustein wähle ich sie aus, damit: _____________\nBeim zweiten Test hat sich geändert: _____________________\nMein echter Verbrauch vorher / nachher: __________________\nHier brauche ich noch Hilfe: _____________________________'),
  ('note','Morgen lernen wir Bedingungen: Wann darf ein Schritt weiterlaufen und wann soll er stoppen? Heute reicht es, die vier Angaben richtig zu übernehmen und das veränderte Ergebnis zu prüfen.')], 'Dein Abschluss'),
 p('datentypen','Zum Nachlesen: Nicht jede Angabe ist Text',[
  ('p','Unsere Hauptübung verwendet nur vier Texte. Die Folien zeigen außerdem andere Arten von Werten. Du musst sie heute nicht in den Ablauf einbauen.'),
  ('table',(['Name','Beispiel','Einfach erklärt'],[['String','"Papierfunke"','Text in doppelten Anführungszeichen.'],['Number','200 oder 3.14','Eine Zahl, ohne Anführungszeichen. Dezimalzahlen haben in JSON einen Punkt.'],['Boolean','true oder false','Ein echter Ja-/Nein-Wert ohne Anführungszeichen. "true" wäre dagegen Text.'],['Null','null','Es ist kein Wert vorhanden. Das ist nicht die Zahl 0 und nicht leerer Text "".']])),
  ('check','Welcher Unterschied steckt zwischen 200 und "200"? Der erste Wert ist eine Zahl, der zweite Text. Die Zeichen außen gehören zur Bedeutung.')], 'Freiwillig: Folienwissen'),
 p('listen','Zum Nachlesen: Ein Zettel oder eine Liste?',[
  ('table',(['JSON-Begriff','So erkennst du ihn','Alltagsbild'],[['Object','Geschweifte Klammern { }','Ein einzelner Zettel mit benannten Feldern.'],['Array','Eckige Klammern [ ]','Eine geordnete Liste, etwa mehrere Projekte.']])),
  ('p','Unser Muster beginnt mit { und endet mit }. Es ist genau ein Objekt. Eine JSON-Liste kann dagegen mehrere Einträge enthalten. Wenn Parse JSON eine solche Liste verarbeitet, können mehrere Datenpäckchen entstehen. Nachfolgende Bausteine können dadurch mehrfach laufen.'),
  ('note','Heute bleiben wir bei einem einzigen Objekt. Das hält Ergebnis und Verbrauch überschaubar. In Make heißt das Päckchen Bundle. Die Folien verwenden teilweise das allgemeinere Wort Item.')], 'Freiwillig: Folienwissen'),
 p('outlook','Was die Outlook-Excel-Folien zeigen',[
  ('p','Die Folien 12 bis 16 zeigen einen größeren Ablauf: Eine neue E-Mail aus Outlook wird als neue Zeile in Excel eingetragen. Das ist ein anschauliches Beispiel, braucht aber einen passenden Microsoft-365-Zugang mit Outlook und OneDrive sowie erlaubte Verbindungen zu Make.'),
  ('flow',['Neue E-Mail im Postfach erkennen','Angaben wie Betreff und Absender übernehmen','Eine Zeile in einer echten Excel-Tabelle ergänzen']),
  ('p','Die vorgeschlagene Datei heißt E-Mail-Eingang.xlsx. Das Blatt heißt Eingänge. Der Bereich muss in Excel tatsächlich als Tabelle formatiert sein. Nur fett gedruckte Überschriften reichen dafür nicht.'),
  ('table',(['Spalte in Excel','Passende Angabe aus der E-Mail'],[['Eingang Zeitstempel','Wann die Nachricht ankam'],['Name Absender','Name der absendenden Person'],['E-Mail Absender','Deren E-Mail-Adresse'],['Betreff','Die Betreffzeile'],['Inhalt','Eine kurze Vorschau des Inhalts'],['Web-Link','Link zur Nachricht, soweit im Ergebnis vorhanden']])),
  ('note','Das sind Erklärungen zur Vorlage, keine zusätzliche Pflichtübung heute. Unser kostenloser Ersatz übt das Auswählen und Weitergeben mit vorbereiteten Angaben. Er legt keine echte Excel-Zeile an.')], 'Freiwillig: Originalübung verstehen'),
 p('outlook-pruefen','Was bei der Originalübung zusätzlich zu prüfen wäre',[
  ('p','Der erste Baustein heißt in der Vorlage Microsoft 365 Email → Watch Emails. Er prüft den angegebenen Posteingang. Der zweite heißt Microsoft 365 Excel → Add a Table Row. Er ergänzt eine Zeile in der gewählten Tabelle.'),
  ('p','Die Beispielwerte der Folie sind Inbox, All emails, Limit 2 und From now on. Sie gehören zur dort gezeigten Einrichtung. Welche Felder tatsächlich verfügbar sind, muss man im eigenen Modul prüfen. Feldpfade nicht blind aus einer Folie eintippen.'),
  ('h','Testen und später überwachen'),
  ('p','Mit passenden eigenen Zugängen würde man eine Test-E-Mail verwenden und die neue Tabellenzeile kontrollieren. Danach prüft man im Verlauf History Ergebnis, Fehler und Verbrauch. Auch unvollständige Ausführungen müssen angesehen werden. Eine kurze Beschreibung und Bilder des tatsächlichen Ergebnisses dokumentieren den Test.'),
  ('note','Die Folie zeigt außerdem einen 15-Minuten-Zeitplan und das Aktivieren des Szenarios. Das übernehmen wir nicht für unseren kostenlosen Lernversuch. Regelmäßiges Nachsehen kann auch ohne neue Nachricht Credits verbrauchen. Watch bedeutet nicht automatisch „sofort“. Der jeweilige Auslöser und Tarif müssen zum Einsatz passen.')], 'Freiwillig: Originalübung verstehen'),
 p('datenfluss','So hängen die Folienthemen zusammen',[
  ('flow',['Angaben kommen hinein','Ein Schritt liest oder verarbeitet sie','Einzelne Felder werden ausgewählt','Der nächste Schritt verwendet diese Felder']),
  ('p','Eine Variable ist ein benannter, veränderlicher Wert. Gestern war es vorname. Heute sind es projekt, thema, kanal und status. Der zweite Test zeigt: Derselbe Ablauf kann andere Inhalte übernehmen.'),
  ('p','Die Folien erweitern den Weg später um KI: Eingabe → KI-Auftrag → Antwort in festen JSON-Feldern → Felder auslesen → nächste Aktion. Diese klare Ordnung hilft Programmen, Daten auszutauschen. Für unsere heutige Übung brauchen wir den KI-Schritt noch nicht.'),
  ('note','Ein korrekt lesbares JSON beweist keine richtigen Inhalte. Auch eine KI kann einen falschen Termin in sauberem JSON ausgeben. Deshalb prüfst du sowohl die Schreibweise als auch die Bedeutung der Angaben.')], 'Freiwillig: Folienwissen')
 ]

SLIDE_HELP={
12:'Die Originalaufgabe übernimmt neue Outlook-Nachrichten nach Excel. Man lernt Startauslöser, Aktion, Mapping, Test, Planung und Dokumentation. Dafür werden neben Make ein geeigneter Microsoft-365- und OneDrive-Zugang benötigt. Heute üben wir den Datenweg mit Testangaben ohne diese zusätzlichen Konten.',
13:'Die Vorlage legt EMailTabelle an und bereitet E-Mail-Eingang.xlsx mit dem Blatt Eingänge vor. Wichtig: Der Bereich ist eine echte Excel-Tabelle. Watch Emails wird mit Postfach, Kriterien, kleiner Anzahl und Start ab jetzt eingestellt. Diese Werte sind Beispiele der Originalfolie und müssen im eigenen Modul überprüft werden.',
14:'Add a Table Row schreibt eine Tabellenzeile. Für jede Spalte wird die passende Angabe aus der E-Mail ausgewählt. Danach wird mit einer eigenen Testnachricht geprüft, ob die Werte wirklich in der Tabelle ankommen. Unsere Textausgabe macht dieselbe Grundidee ohne Excel-Verbindung sichtbar.',
15:'Die Vorlage erklärt regelmäßige Ausführung, Aktivieren, Verlauf, unvollständige Läufe und Dokumentation mit Bildern. Für unseren Unterricht bleibt die automatische Planung aus. Ein laufender 15-Minuten-Zeitplan kann das kleine Creditbudget aufbrauchen. Ein Testprotokoll muss zeigen, was wirklich ausgeführt wurde.',
16:'Die Folie zeigt das Ergebnis der Originalübung. Es ist ein Beispielbild und kein Nachweis für einen Lauf in deinem Konto. Vergleiche bei eigenen Versuchen immer die tatsächliche Eingabe mit der tatsächlichen Ausgabe.',
24:'JSON ordnet Angaben in benannte Felder und Listen. Das erleichtert das Austauschen und Lesen zwischen Programmen. Bei KI kann eine vereinbarte JSON-Ausgabe helfen; JSON allein macht eine Antwort aber nicht wahr. Unsere Übung nutzt dieses Format ohne KI.',
25:'Die sechs Grundarten heißen Text, Zahl, Wahrheitswert, Null, Objekt und Liste. Die Beispiele im Zusatzteil zeigen die Schreibweise. Besonders wichtig: true ist ein Ja-/Nein-Wert; "true" ist Text. Unsere Hauptübung verwendet nur vier Texte.',
26:'Benannte Werte können sich ändern. Statt für jede neue Angabe einen anderen Ablauf zu bauen, wählst du das passende Feld aus. Parse JSON macht die Felder des Textes verfügbar. Der zweite Versuch mit Nordlicht zeigt, ob der neue Inhalt richtig weitergegeben wird.',
27:'Die Folie zeigt den Weg von der Datenaufnahme über eine mögliche KI-Verarbeitung zum Auslesen und Weitergeben. Make spricht dabei von Bundles, also Datenpäckchen. Unsere kleine Variante ist: ein JSON-Objekt lesen → Felder auswählen → Text erzeugen. Einen KI-Aufruf oder Außenversand behauptet sie nicht.'
}

IDEA_HELP={
9:('Korrekturwünsche fürs Videoteam sammeln','Ein Zettel könnte zeigen: „Runde 2 - Datum im Bildtext ändern“. So sieht die nächste Person genau, worum es geht.','Heute anpassbar: Den Text in thema ändern und das neue Ergebnis prüfen. Make schneidet dadurch noch kein Video.'),
10:('Eine Videovorschau zur Prüfung vormerken','Ein interner Zettel erinnert daran, Bild, Text, Ton und Format anzusehen. Ein Link allein prüft die Datei noch nicht.','Freigaben und Bedingungen kommen erst Mittwoch. Heute genügt ein Textentwurf ohne Versand.'),
11:('Eine Druckanfrage übersichtlich notieren','Beispiel: „200 Flyer; Papier noch offen“. Die offene Frage soll im Zettel sichtbar bleiben.','Heute anpassbar: thema auf diesen Text und kanal auf Vertrieb setzen. Es entsteht kein verbindliches Angebot.'),
12:('Ein vorbereitetes Angebot intern vorlegen','Ein Hinweis könnte anzeigen, dass ein Mensch ein Angebot prüfen soll. Er soll keine ungeprüfte Zusage auslösen.','Das Filtern nach einer Freigabe folgt Mittwoch. Heute keinen Außenversand oder echten Preis einbauen.'),
13:('Ein Kundengespräch vorbereiten','Aus „Format und Abholung klären“ wird ein kleiner Gesprächszettel. Bestätigte Fakten und offene Fragen bleiben erkennbar.','Heute anpassbar: thema auf den Beispieltext und kanal auf Gespräch setzen. Anschließend die Ausgabe vergleichen.'),
14:('Eine Rückfrage als Entwurf festhalten','Beispiel: „Nach Papiermuster fragen“. So kann das Team den nächsten Schritt besprechen.','Heute nur einen Zettel erstellen. Ein späterer Terminlauf und eine echte Kontaktaufnahme wären zusätzliche Schritte.'),
15:('Offene und erledigte Vorgänge unterscheiden','Ein Status kann helfen, nicht versehentlich an einem abgeschlossenen Fall weiterzuarbeiten.','Heute darfst du den Text im Feld status ändern und die Ausgabe ansehen. Ein Status stoppt noch keinen Ablauf; dafür braucht man später eine Bedingung.'),
16:('Neue Kolleginnen und Kollegen begrüßen','Eine persönliche Begrüßung lässt sich aus einem Namen und festen Textteilen zusammensetzen. Das kennst du schon von Tag 1.','Wenn du das gestern gebaut hast: Luna und Mira vergleichen. Keine echten Nutzerkonten anlegen und nichts automatisch verschicken.')
}
