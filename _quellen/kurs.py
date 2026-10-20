"""Kursinhalt fuer die Plattform: Personen, Tage, Learnings, Begriffe, Lernkarten, Selbsttest.
Sprache: einfach, man-Form, neutral. Jeder Fachbegriff wird dort erklaert, wo er vorkommt.
Folie = Nummer im Foliensatz des Tages (fuer den Sprung in den Folien-Viewer)."""

PERSONEN = {
    'carmen': {'name': 'Carmen', 'profil': 'B', 'fach': 'Teamleitung, Business & Website', 'mac': True},
    'ingo':   {'name': 'Ingo',   'profil': 'A', 'fach': 'Druck & Vertrieb', 'mac': False},
    'tabea':  {'name': 'Tabea',  'profil': 'C', 'fach': 'Video, Design & Creative', 'mac': False},
}
REIHENFOLGE = ['carmen', 'ingo', 'tabea']

TAGE = {}

# ---------------------------------------------------------------- Tag 1
TAGE[1] = {
    'titel': 'KI – Hype oder Realität?',
    'unter': 'Lektion 1 · und erste Schritte mit Prompts in Langdock',
    'datum': '28.09.2026',
    'folien': 'KIAutomSpez_1_1_HypeOderRealitat.pdf',
    'kurz': 'Wo KI heute wirklich steht, woher sie kommt – und wie ein guter Prompt aufgebaut ist.',
    'learnings': [
        {'id': 'l1', 'folie': 3, 'satz': 'Die meisten Unternehmen sehen KI als wichtigste Zukunftstechnologie.',
         'erklaert': 'Laut einer Bitkom-Umfrage sagen das 81 % der Unternehmen und 67 % der Bevölkerung. Für einen Hype, der massiv überschätzt wird, halten KI nur 17 % der Unternehmen und 28 % der Bevölkerung.'},
        {'id': 'l2', 'folie': 5, 'satz': 'KI ist in vielen Firmen schon angekommen.',
         'erklaert': '2018 setzten nur 3 % der Unternehmen KI ein, 2025 sind es 36 %. Weitere 47 % planen oder diskutieren es. Für nur noch 17 % ist KI „kein Thema“.'},
        {'id': 'l3', 'folie': 4, 'satz': 'Jobs verändern sich eher, als dass sie verschwinden.',
         'erklaert': '67 % der Unternehmen erwarten in den nächsten fünf Jahren keine Auswirkung auf die Zahl der Stellen, 20 % erwarten weniger, 7 % mehr. 31 % sagen: KI hilft gegen den Fachkräftemangel. In Deutschland könnten in 15 Jahren etwa 1,6 Millionen Arbeitsplätze betroffen sein – abgebaut oder neu geschaffen. Studien zeigen außerdem: Oft entstehen neue Aufgaben und mehr Arbeitsdruck statt echter Entlastung.'},
        {'id': 'l4', 'folie': 2, 'satz': 'Fachwissen wird durch KI wichtiger, nicht unwichtiger.',
         'erklaert': 'Unternehmen, die KI nutzen, um das Können ihrer Leute zu verstärken, wachsen schneller als Firmen, die vor allem automatisieren. Die KI liefert Vorschläge – entscheiden und prüfen tut der Mensch.'},
        {'id': 'l5', 'folie': 7, 'satz': 'Es gibt nicht die eine Definition von KI.',
         'erklaert': 'Stanford: die Wissenschaft, intelligente Maschinen zu bauen. MIT: Maschinen, die menschliche Fähigkeiten wie Denken, Lernen, Planen und Kreativität nachahmen. EU-Kommission: Systeme, die ihre Umgebung analysieren und bis zu einem gewissen Grad selbstständig handeln.'},
        {'id': 'l6', 'folie': 8, 'satz': 'Der Turing-Test fragt: Kann man Mensch und Maschine im Gespräch unterscheiden?',
         'erklaert': 'Alan Turing beschrieb 1950 ein Gedankenexperiment: Eine Person unterhält sich mit einem Menschen und einer Maschine, ohne zu wissen, wer wer ist. Kann sie die Maschine nicht erkennen, gilt die Maschine als intelligent. Durchgeführt wurde der Test damals nicht – die Computer waren viel zu schwach.'},
        {'id': 'l7', 'folie': 9, 'satz': 'In manchem ist KI schon besser als Menschen – in anderem holt sie noch auf.',
         'erklaert': 'Besser als Menschen in Tests: Texte lesen und verstehen, Bilder, Handschrift und Sprache erkennen. Bei Mathe, Code und Allgemeinwissen hat KI fast aufgeschlossen. Deutlich zurück liegt sie beim komplexen Schlussfolgern, also beim Denken über viele Schritte. Es geht aber schnell: 2026 hat ein Modell von OpenAI eine Mathe-Vermutung aus dem Jahr 1946 widerlegt (Folie 12).'},
        {'id': 'l8', 'folie': 10, 'satz': 'Bilder und Videos aus der KI sind in wenigen Jahren fast echt geworden.',
         'erklaert': '2014 waren KI-Gesichter noch unscharfe graue Flecken, heute entstehen fotorealistische Bilder. Beim bekannten „Will Smith isst Spaghetti“-Vergleich sieht man den Sprung von März 2023 zu Mai 2026 auch bei Videos (Folie 11).'},
        {'id': 'l9', 'folie': 13, 'satz': 'Die KI-Geschichte kennt Hochs und Tiefs.',
         'erklaert': '1950 Turing-Test, 1956 entsteht der Begriff „Künstliche Intelligenz“. Zweimal folgte auf zu große Erwartungen ein „KI-Winter“ mit weniger Geld und Interesse (1974–1980 und 1987–1993). 1997 schlägt der Schachcomputer Deep Blue den Weltmeister. Seit den 2000ern geht es steil bergauf. Lehre: Hype und Enttäuschung wechseln sich ab.'},
        {'id': 'l10', 'folie': 14, 'satz': 'Der Durchbruch mit GPT hat drei Gründe.',
         'erklaert': '1. Eine neue Bauweise (der „Transformer“, 2017) lässt sich auf Grafikchips sehr schnell rechnen. 2. Es gibt riesige Mengen Trainingsmaterial aus dem Internet. 3. Man bedient KI einfach mit Sprache – dadurch kann sie jede Person nutzen. Dazu kommt: Diese Modelle erzeugen etwas Neues – Text, Bilder, Code, Videos.'},
        {'id': 'l11', 'folie': None, 'satz': 'Ein guter Prompt hat fünf Bausteine: Rolle, Situation, Ziel, Format, Grenzen.',
         'erklaert': 'Prompt = die Anweisung an die KI. Rolle: Wer soll die KI sein? Situation: Was ist los? Ziel: Was soll am Ende herauskommen? Format: Länge, Liste, Tonfall. Grenzen: Was darf nicht passieren, z. B. „keine Preise erfinden“. Je klarer diese Punkte, desto weniger muss man nachbessern.'},
        {'id': 'l12', 'folie': None, 'satz': 'Die KI zuerst Fragen stellen lassen – und mit ihr üben.',
         'erklaert': 'Der Satz „Stelle mir zuerst Fragen, bevor du …“ spart die meisten Korrekturen. In Rollenspielen spielt die KI das Gegenüber (z. B. Kundschaft) und bewertet danach das Gespräch.'},
        {'id': 'l13', 'folie': None, 'satz': 'KI-Bilder sind Ideen und Entwürfe, keine fertigen Druckdaten.',
         'erklaert': 'Ein guter Bild-Prompt beschreibt Motiv, Umgebung, Stil, Licht, Blickwinkel, Farben und Format – und was nicht ins Bild soll. Vor dem Veröffentlichen oder Drucken prüft man Qualität und Nutzungsrechte.'},
        {'id': 'l14', 'folie': None, 'satz': 'Sicher arbeiten: nur ausgedachte Daten eingeben – und Ergebnisse immer prüfen.',
         'erklaert': 'Keine echten Namen, Kundendaten oder Verträge in Übungen. Die KI kann Zahlen, Preise und Fakten erfinden und klingt dabei überzeugend. Deshalb: Belege verlangen und selbst gegenprüfen.'},
    ],
    'begriffe': [
        ('KI (Künstliche Intelligenz)', 'Computerprogramme, die Aufgaben lösen, für die man sonst menschliches Denken braucht.'),
        ('Generative KI', 'KI, die etwas Neues erzeugt: Texte, Bilder, Musik, Videos oder Code.'),
        ('Prompt', 'Die Anweisung oder Frage, die man der KI gibt.'),
        ('Turing-Test', 'Gedankenexperiment von 1950: Erkennt man im Gespräch, ob man mit Mensch oder Maschine spricht?'),
        ('KI-Winter', 'Zeit, in der das Interesse und das Geld für KI stark zurückgingen, weil zu viel versprochen wurde.'),
        ('Expertensystem', 'Frühe KI (1980er), die mit festen Regeln von Fachleuten arbeitete.'),
        ('GPT', '„Generative Pre-trained Transformer“ – die Modellart hinter ChatGPT und vielen anderen Chat-KIs.'),
        ('Agent', 'In Langdock: ein eigener KI-Assistent mit fester Anweisung, der immer gleich arbeitet.'),
    ],
    'karten': [
        ('Wie viel Prozent der Unternehmen halten KI für die wichtigste Zukunftstechnologie?', '81 % (Bevölkerung: 67 %).'),
        ('Wie viele Unternehmen setzten 2025 KI ein?', '36 % – 2018 waren es nur 3 %.'),
        ('Was prüft der Turing-Test?', 'Ob man im Gespräch erkennen kann, ob das Gegenüber Mensch oder Maschine ist.'),
        ('Was ist ein „KI-Winter“?', 'Eine Phase, in der Interesse und Geld für KI stark zurückgingen – nach zu großen Erwartungen.'),
        ('Welche drei Gründe machten den Durchbruch mit GPT möglich?', 'Neue Bauweise (Transformer) passend zu Grafikchips, riesige Datenmengen, Bedienung mit Sprache.'),
        ('Worin ist KI schon besser als Menschen?', 'Z. B. Texte verstehen, Bilder, Handschrift und Sprache erkennen.'),
        ('Worin muss KI noch aufholen?', 'Beim komplexen Schlussfolgern über viele Schritte.'),
        ('Die fünf Bausteine eines guten Prompts?', 'Rolle, Situation, Ziel, Format, Grenzen.'),
        ('Welcher Satz spart die meisten Korrekturen?', '„Stelle mir zuerst Fragen, bevor du …“'),
        ('Wird Fachwissen durch KI unwichtiger?', 'Nein – Firmen, die KI zur Verstärkung von Fachwissen nutzen, wachsen schneller.'),
    ],
    'test': [
        {'frage': 'Wie viele Unternehmen halten KI laut Bitkom für einen massiv überschätzten Hype?',
         'optionen': ['17 %', '47 %', '81 %'], 'richtig': 0,
         'warum': '17 % der Unternehmen sagen „Hype“ – 81 % sehen KI als wichtigste Zukunftstechnologie.'},
        {'frage': 'Was stimmt über den Turing-Test von 1950?',
         'optionen': ['Er wurde damals mit einem Computer durchgeführt.', 'Er war ein Gedankenexperiment.', 'Er misst, wie schnell eine KI rechnet.'], 'richtig': 1,
         'warum': 'Turing beschrieb nur, wie ein solcher Test ablaufen würde – die Computer waren damals viel zu schwach.'},
        {'frage': 'Was war ein „KI-Winter“?',
         'optionen': ['Eine Zeit mit wenig Geld und Interesse für KI', 'Ein Kälteproblem in Rechenzentren', 'Der Name eines frühen Chatbots'], 'richtig': 0,
         'warum': 'Nach zu großen Versprechen folgten zweimal Enttäuschung und weniger Investitionen.'},
        {'frage': 'Welcher Punkt gehört NICHT zu den Gründen für den Durchbruch mit GPT?',
         'optionen': ['Bedienung mit normaler Sprache', 'Riesige Datenmengen aus dem Internet', 'Ein Gesetz, das KI vorschreibt'], 'richtig': 2,
         'warum': 'Die Gründe: neue Bauweise passend zu Grafikchips, viele Daten, Bedienung mit Sprache.'},
        {'frage': 'Welcher Baustein sagt der KI, was auf keinen Fall passieren darf?',
         'optionen': ['Rolle', 'Grenzen', 'Format'], 'richtig': 1,
         'warum': 'Grenzen legen fest, was nicht passieren darf – z. B. „Erfinde keine Preise“.'},
        {'frage': 'Wofür eignen sich KI-Bilder am besten?',
         'optionen': ['Als fertige Druckdaten ohne Prüfung', 'Als Ideen und Entwürfe', 'Als Beweisfotos'], 'richtig': 1,
         'warum': 'KI-Bilder sind stark bei Ideen und Stimmungen – vor Druck oder Veröffentlichung wird geprüft.'},
    ],
}

# ---------------------------------------------------------------- Tag 2
TAGE[2] = {
    'titel': 'Welches KI-Modell für welche Aufgabe?',
    'unter': 'Lektion 2 · Modellauswahl',
    'datum': '29.09.2026',
    'folien': 'Tag-2-Modellauswahl.pdf',
    'kurz': 'Wer die großen KI-Anbieter sind, wie man Modellnamen liest – und wie man das passende Modell auswählt.',
    'learnings': [
        {'id': 'l1', 'folie': 3, 'satz': 'Drei Regionen prägen die KI-Welt: USA, China und Europa.',
         'erklaert': 'Die USA haben die Spitzenmodelle (OpenAI, Anthropic, Google, Meta, xAI). China holt mit frei verfügbaren Modellen rasant auf (DeepSeek, Qwen, Kimi, GLM). Europa setzt auf Unabhängigkeit und Datenschutz (Mistral, Aleph Alpha, Black Forest Labs).'},
        {'id': 'l2', 'folie': 4, 'satz': 'Hinter jedem Chat steckt ein Anbieter mit eigener Strategie.',
         'erklaert': 'OpenAI (ChatGPT) ist der bekannteste Anbieter. Google baut Gemini in Suche, Android und Büro-Programme ein. Anthropic (Claude) legt besonderen Wert auf Sicherheit. Mistral aus Frankreich bietet Modelle, die man auch selbst betreiben kann.'},
        {'id': 'l3', 'folie': 7, 'satz': 'Politik kann ein Modell über Nacht abschalten.',
         'erklaert': 'Juni 2026: Das US-Handelsministerium ordnet an, dass Ausländer die Modelle Fable 5 und Mythos 5 nicht nutzen dürfen. Nach Nationalität filtern geht nicht – also schaltet Anthropic beide weltweit ab. Lehre: Wer sich nur auf einen Anbieter verlässt, geht ein Risiko ein.'},
        {'id': 'l4', 'folie': 11, 'satz': '„Open Weight“ heißt: Man kann das Modell selbst betreiben und anpassen.',
         'erklaert': 'Die „Gewichte“ sind das gelernte Wissen eines Modells. Sind sie frei verfügbar (z. B. bei Llama, DeepSeek, Qwen), kann man das Modell auf eigenen Rechnern laufen lassen. Das ist nicht ganz dasselbe wie komplett offener Quellcode.'},
        {'id': 'l5', 'folie': 17, 'satz': 'Für Bild, Ton und Video gibt es Spezialisten.',
         'erklaert': 'Midjourney (Bilder), Black Forest Labs mit FLUX (Foto-Realismus, aus Freiburg), ElevenLabs (Stimmen), Runway (Video), Suno (Musik). Perplexity ist eine Antwortmaschine: Sie sucht live im Internet und antwortet mit Quellen (Folie 18). Nicht jede Aufgabe löst ein Chat-Modell am besten.'},
        {'id': 'l13', 'folie': 16, 'satz': 'Fast jede große KI rechnet auf Chips von NVIDIA.',
         'erklaert': 'Fast jedes große Modell wird auf Grafikchips (GPUs) von NVIDIA trainiert. Im Oktober 2025 war NVIDIA das erste Unternehmen der Welt, das 5 Billionen Dollar wert war. Diese Chips begegnen einem an Tag 3 im Rechenzentrum wieder.'},
        {'id': 'l6', 'folie': 19, 'satz': 'Modellnamen bestehen aus vier Bausteinen.',
         'erklaert': '1. Generation (eine Zahl, z. B. GPT-5.6). 2. Größe und Leistung (z. B. Opus / Sonnet / Haiku oder Pro / Flash / Lite). 3. Besondere Fähigkeit (z. B. Bild oder Code). 4. Nachdenk-Modus. Faustregel: „mini“, „flash“, „lite“ heißt kleiner, schneller, günstiger.'},
        {'id': 'l7', 'folie': 20, 'satz': 'Nachdenk-Modelle („Reasoning“) lohnen sich nur bei harten Denkaufgaben.',
         'erklaert': 'Reasoning heißt: Das Modell denkt erst Schritt für Schritt nach, bevor es antwortet. Stark bei Mathe, Code, Analysen und Planung. Bei einfachen Aufgaben (Mail umformulieren, zusammenfassen) ist es nur langsamer und teurer.'},
        {'id': 'l8', 'folie': 21, 'satz': 'Ranglisten und Testwerte mit Vorsicht lesen.',
         'erklaert': 'Viele Tests sind so leicht geworden, dass alle Modelle über 90 % schaffen. Manche Anbieter trainieren gezielt auf die Tests. Eine Zahl sagt wenig über den eigenen Anwendungsfall – selbst ausprobieren ist besser.'},
        {'id': 'l9', 'folie': 22, 'satz': 'Neun Fragen führen zur richtigen Wahl.',
         'erklaert': '1. Braucht es Nachdenken? 2. Was geht hinein (Text, Bild, Ton)? 3. Was soll herauskommen? 4. Wie viel Text muss hineinpassen? 5. Was darf es kosten? 6. Wie schnell muss es sein? 7. Wie sensibel sind die Daten? 8. Frei verfügbar oder nicht? 9. Wie gut kann es Deutsch?'},
        {'id': 'l10', 'folie': 22, 'satz': 'Die kleinste Lösung nehmen, die den Job zuverlässig erledigt.',
         'erklaert': 'Größere Modelle kosten mehr und sind oft langsamer. Für viele Alltagsaufgaben reicht ein mittleres oder kleines Modell. Am Ende entscheidet der eigene Test.'},
        {'id': 'l11', 'folie': 24, 'satz': 'Nicht für alles ist ein Sprachmodell das richtige Werkzeug.',
         'erklaert': 'Genaues Rechnen und Optimieren gehört in Tabellen oder Spezialprogramme. Die KI hilft dabei, Aufgaben zu verstehen, aufzuschreiben und Ergebnisse zu prüfen.'},
        {'id': 'l12', 'folie': None, 'satz': 'In Langdock wählt man das Modell selbst – und testet mehrere.',
         'erklaert': 'Die Modellauswahl sitzt im Eingabefeld. Man kann den Nachdenk-Modus ein- und ausschalten und für aktuelle Themen die Websuche nutzen. Derselbe Prompt mit zwei, drei Modellen zeigt schnell, welches am besten passt.'},
    ],
    'begriffe': [
        ('Modell', 'Die eigentliche KI, die Antworten erzeugt, z. B. GPT-5.5 oder Claude Opus.'),
        ('Anbieter', 'Die Firma, die ein Modell entwickelt und betreibt, z. B. OpenAI, Google, Anthropic, Mistral.'),
        ('Open Weight', 'Das gelernte Wissen eines Modells ist frei verfügbar – man kann es selbst betreiben.'),
        ('Reasoning', 'Nachdenk-Modus: Das Modell denkt Schritt für Schritt, bevor es antwortet.'),
        ('Benchmark', 'Ein standardisierter Test, mit dem man Modelle vergleicht.'),
        ('Kontextfenster', 'Wie viel Text ein Modell auf einmal lesen kann.'),
        ('Souveränität', 'Unabhängigkeit: Daten und Technik bleiben unter eigener Kontrolle, z. B. in Europa.'),
        ('Multimodal', 'Ein Modell, das nicht nur Text, sondern auch Bilder, Ton oder Video versteht.'),
    ],
    'karten': [
        ('Welche drei Regionen prägen die KI-Welt?', 'USA (Spitzenmodelle), China (holt mit freien Modellen auf), Europa (setzt auf Souveränität).'),
        ('Nenne zwei europäische KI-Anbieter.', 'Z. B. Mistral, Aleph Alpha, Black Forest Labs.'),
        ('Was bedeutet „Open Weight“?', 'Das gelernte Wissen des Modells ist frei verfügbar – man kann es selbst betreiben und anpassen.'),
        ('Was bedeutet „mini“, „flash“ oder „lite“ im Namen?', 'Kleiner, schneller, günstiger.'),
        ('Wann lohnt sich ein Nachdenk-Modell?', 'Bei harten Denkaufgaben: Mathe, Code, Analyse, Planung.'),
        ('Warum sind Ranglisten mit Vorsicht zu lesen?', 'Viele Tests sind zu leicht, manche Anbieter trainieren darauf – eine Zahl sagt wenig über den eigenen Fall.'),
        ('Welche Faustregel gilt bei der Modellwahl?', 'Die kleinste Lösung nehmen, die den Job zuverlässig erledigt – und selbst testen.'),
        ('Was lehrt der Fall der abgeschalteten Modelle (Juni 2026)?', 'Politik kann Modelle über Nacht abschalten – Abhängigkeit von einem Anbieter ist ein Risiko.'),
        ('Wofür ist ein Sprachmodell NICHT das beste Werkzeug?', 'Für genaues Rechnen und Optimieren – das gehört in Tabellen oder Spezialprogramme.'),
        ('Nenne drei der neun Auswahlfragen.', 'Z. B. Nachdenken nötig? Kosten? Datenschutz? (weitere: Input, Output, Textmenge, Tempo, Lizenz, Deutsch)'),
    ],
    'test': [
        {'frage': 'Welcher Anbieter kommt aus Europa?',
         'optionen': ['DeepSeek', 'Mistral', 'xAI'], 'richtig': 1,
         'warum': 'Mistral ist ein französisches Unternehmen. DeepSeek kommt aus China, xAI aus den USA.'},
        {'frage': 'Wofür steht „Haiku“ bei Claude-Modellen?',
         'optionen': ['Das stärkste Modell', 'Das schnelle, kleine Modell', 'Ein Bildmodell'], 'richtig': 1,
         'warum': 'Opus ist die stärkste Stufe, Sonnet die Mitte, Haiku die schnelle, kleine Stufe.'},
        {'frage': 'Wann ist ein Nachdenk-Modell (Reasoning) eher unnötig?',
         'optionen': ['Beim Lösen einer Rechenaufgabe', 'Beim Umformulieren einer kurzen Mail', 'Beim Planen eines Projekts'], 'richtig': 1,
         'warum': 'Bei einfachen Aufgaben ist Nachdenken nur langsamer und teurer.'},
        {'frage': 'Was heißt „Open Weight“?',
         'optionen': ['Das Modell ist kostenlos im Browser nutzbar', 'Das gelernte Wissen ist frei verfügbar und selbst betreibbar', 'Das Modell hat kein Gewichtslimit'], 'richtig': 1,
         'warum': 'Die Gewichte (das gelernte Wissen) sind frei – man kann das Modell selbst betreiben.'},
        {'frage': 'Was ist die Faustregel bei der Modellwahl?',
         'optionen': ['Immer das größte Modell nehmen', 'Die kleinste Lösung, die den Job zuverlässig erledigt', 'Immer das Modell mit dem besten Testwert'], 'richtig': 1,
         'warum': 'Größer heißt teurer und langsamer – entscheidend ist, dass der Job zuverlässig klappt.'},
        {'frage': 'Wohin gehört genaues Rechnen am ehesten?',
         'optionen': ['In eine Tabelle oder Spezialsoftware', 'In ein Bildmodell', 'In ein Musikmodell'], 'richtig': 0,
         'warum': 'Die KI hilft beim Verstehen und Prüfen – das Rechnen selbst gehört in Tabellen oder Spezialprogramme.'},
    ],
}

# ---------------------------------------------------------------- Tag 3
TAGE[3] = {
    'titel': 'Was passiert bei einer KI-Anfrage?',
    'unter': 'Lektion 3 · LLMs unter der Lupe',
    'datum': '30.09.2026',
    'folien': 'LLMs-unter-der-Lupe.pdf',
    'kurz': 'Der Weg einer Frage vom Bildschirm ins Rechenzentrum und zurück – Station für Station.',
    'videos': [
        {'id': 'LPZh9BOjkQs', 'titel': 'Large Language Models explained briefly', 'dauer': '7:58', 'folie': 8,
         'text': 'Wie ein großes Sprachmodell lernt und Wort für Wort eine Antwort bildet.'},
        {'id': 'lPTcTh5sRug', 'titel': 'How AI Turns Words Into Vectors: Embeddings', 'dauer': '3:35', 'folie': 9,
         'text': 'Wie Wörter zu Zahlen werden – und warum „König“ näher an „Königin“ liegt als an „Apfel“.'},
    ],
    'learnings': [
        {'id': 'l1', 'folie': 2, 'satz': 'Hinter dem Chatfenster steckt ein Weg in fünf Stationen.',
         'erklaert': 'Anfrage → Transport → Load Balancer → API → Rechenzentrum. Und die Antwort nimmt denselben Weg zurück.'},
        {'id': 'l2', 'folie': 3, 'satz': 'Station 1 – Die Anfrage: Man sieht nur die Oberfläche.',
         'erklaert': 'Man tippt in einer App oder im Browser, zum Beispiel in Langdock. Die eigentliche „Intelligenz“ läuft nicht auf dem eigenen Gerät, sondern woanders. Die Nachricht verlässt das Gerät und geht ins Internet.'},
        {'id': 'l3', 'folie': 4, 'satz': 'Station 2 – Transport: Die Anfrage reist verschlüsselt.',
         'erklaert': 'Die Anfrage wird über HTTPS/SSL verschickt – wie ein versiegelter Brief, den unterwegs niemand lesen kann. Sie landet beim Modellanbieter, z. B. OpenAI, Google oder Anthropic. „Request“ ist nur das Fachwort für Anfrage.'},
        {'id': 'l4', 'folie': 5, 'satz': 'Station 3 – Load Balancer: Er verteilt die Anfragen.',
         'erklaert': 'Millionen Menschen fragen gleichzeitig. Der Load Balancer schickt jede Anfrage an einen freien Server – wie ein Weichenstellwerk am Bahnhof. Ohne ihn wäre alles überlastet.'},
        {'id': 'l5', 'folie': 6, 'satz': 'Station 4 – API: die Schnittstelle zum Modell.',
         'erklaert': 'Die API leitet die Anfrage an das richtige KI-Modell weiter, übersetzt sie in ein Format, das das Modell versteht, und bringt die Antwort zurück. API heißt „Application Programming Interface“ – eine Schnittstelle, über die Programme miteinander sprechen.'},
        {'id': 'l6', 'folie': 7, 'satz': 'Station 5 – Rechenzentrum: Hier läuft das Sprachmodell.',
         'erklaert': 'Ein Gebäude voller Hochleistungsrechner. Dort laufen die großen Sprachmodelle (LLMs), z. B. GPT-5.5 oder Opus 4.8. Die schwere Rechenarbeit übernehmen Spezialchips (GPUs oder TPUs).'},
        {'id': 'l7', 'folie': 7, 'satz': 'Im Rechenzentrum wird zuerst der Kontext zusammengebaut.',
         'erklaert': 'Kontext = alles, was die KI für genau diese Frage bekommt: die Frage selbst, den bisherigen Chat und angehängte Dateien. Was nicht darin steht, kennt die KI nicht.'},
        {'id': 'l8', 'folie': 7, 'satz': 'Der Text wird in Tokens zerlegt.',
         'erklaert': 'Tokens sind kleine Textstücke: ganze Wörter, Wortteile oder Zeichen. Lange Wörter werden oft in mehrere Stücke geteilt. Mit diesen Stücken rechnet das Modell.'},
        {'id': 'l9', 'folie': 9, 'satz': 'Aus Tokens werden Zahlen, die Bedeutung abbilden.',
         'erklaert': 'Jedes Stück bekommt eine Zahlenreihe (ein „Vektor“, der Vorgang heißt „Embedding“). Wörter mit ähnlicher Bedeutung bekommen ähnliche Zahlen – deshalb „weiß“ die KI, dass König näher an Königin liegt als an Apfel.'},
        {'id': 'l10', 'folie': 7, 'satz': 'Die Antwort entsteht Token für Token.',
         'erklaert': 'Das Modell rechnet ein Stück nach dem anderen aus und schickt jedes sofort los. Deshalb erscheint die Antwort live, Stück für Stück, auf dem Bildschirm – das nennt man Stream.'},
        {'id': 'l11', 'folie': 7, 'satz': 'Danach wird der Zwischenspeicher geleert.',
         'erklaert': 'Ist die Antwort fertig, wird der Speicher der Spezialchips (Cache) für die nächsten Anfragen anderer Menschen freigemacht.'},
        {'id': 'l12', 'folie': None, 'satz': 'Fehlt etwas im Kontext, erfindet die KI eher, als dass sie nachfragt.',
         'erklaert': 'Aus dem Prompt-Labor (Modul 01): Eine fehlende Angabe erzeugt keine Fehlermeldung, sondern eine plausible Erfindung. Darum gibt man der KI alles Nötige mit – oder sagt ihr, was sie bei Lücken tun soll.'},
    ],
    'begriffe': [
        ('LLM', '„Large Language Model“ – ein großes Sprachmodell, z. B. GPT oder Claude.'),
        ('Anfrage / Request', 'Die Nachricht, die man an die KI schickt.'),
        ('HTTPS / SSL', 'Verschlüsselte, sichere Übertragung im Internet – wie ein versiegelter Brief.'),
        ('Server', 'Ein Rechner, der für andere Rechner Aufgaben erledigt.'),
        ('Load Balancer', 'Verteilt viele Anfragen auf freie Server – wie ein Weichenstellwerk.'),
        ('API', 'Eine Schnittstelle, über die Programme miteinander sprechen.'),
        ('Rechenzentrum', 'Ein Gebäude voller Hochleistungsrechner.'),
        ('GPU / TPU', 'Spezialchips, die sehr viele Rechnungen gleichzeitig schaffen.'),
        ('Token', 'Ein kleines Textstück: ein Wort, ein Wortteil oder ein Zeichen.'),
        ('Embedding / Vektor', 'Zahlenreihe, die die Bedeutung eines Textstücks abbildet.'),
        ('Stream', 'Die Antwort kommt Stück für Stück live an.'),
        ('Kontext', 'Alles, was die KI für diese eine Frage bekommt.'),
    ],
    'karten': [
        ('Welche fünf Stationen durchläuft eine KI-Anfrage?', 'Anfrage → Transport → Load Balancer → API → Rechenzentrum.'),
        ('Wie wird die Anfrage übertragen?', 'Verschlüsselt über HTTPS/SSL – wie ein versiegelter Brief.'),
        ('Was macht der Load Balancer?', 'Er verteilt die vielen Anfragen auf freie Server – wie ein Weichenstellwerk.'),
        ('Was macht die API?', 'Sie leitet die Anfrage ans richtige Modell, übersetzt sie in ein passendes Format und bringt die Antwort zurück.'),
        ('Wo läuft das Sprachmodell?', 'Im Rechenzentrum, auf Spezialchips (GPUs/TPUs).'),
        ('Was ist der Kontext?', 'Alles, was die KI für diese Frage bekommt: Frage, bisheriger Chat, Anhänge.'),
        ('Was ist ein Token?', 'Ein kleines Textstück – ein Wort, ein Wortteil oder ein Zeichen.'),
        ('Was ist ein Embedding?', 'Zahlen, die die Bedeutung eines Textstücks abbilden. Ähnliche Bedeutung = ähnliche Zahlen.'),
        ('Warum erscheint die Antwort Stück für Stück?', 'Sie wird Token für Token berechnet und sofort geschickt (Stream).'),
        ('Was passiert nach der Antwort mit dem Zwischenspeicher?', 'Der Cache wird geleert – für die Anfragen anderer.'),
        ('Was tut die KI, wenn eine Angabe fehlt?', 'Sie füllt die Lücke meist mit einer plausiblen Erfindung, statt nachzufragen.'),
    ],
    'test': [
        {'frage': 'In welcher Reihenfolge läuft eine Anfrage?',
         'optionen': ['Anfrage → API → Transport → Rechenzentrum → Load Balancer', 'Anfrage → Transport → Load Balancer → API → Rechenzentrum', 'Rechenzentrum → API → Anfrage → Transport → Load Balancer'], 'richtig': 1,
         'warum': 'Erst verlässt die Anfrage das Gerät, reist verschlüsselt, wird verteilt, von der API übersetzt und im Rechenzentrum berechnet.'},
        {'frage': 'Was macht der Load Balancer?',
         'optionen': ['Er macht die Antwort inhaltlich besser', 'Er verteilt Anfragen auf freie Server', 'Er verschlüsselt die Nachricht'], 'richtig': 1,
         'warum': 'Wie ein Weichenstellwerk schickt er jede Anfrage zu einem freien Server.'},
        {'frage': 'Was sind Tokens?',
         'optionen': ['Kleine Textstücke, mit denen das Modell rechnet', 'Passwörter für die Anmeldung', 'Die Preise pro Anfrage'], 'richtig': 0,
         'warum': 'Der Text wird in kleine Stücke zerlegt – ganze Wörter, Wortteile oder Zeichen.'},
        {'frage': 'Warum „tippt“ die KI ihre Antwort Stück für Stück?',
         'optionen': ['Damit es spannender wirkt', 'Weil die Antwort Token für Token berechnet und sofort geschickt wird', 'Weil das Internet langsam ist'], 'richtig': 1,
         'warum': 'Jedes Stück wird berechnet und direkt übertragen – das ist der Stream.'},
        {'frage': 'Was bedeutet Embedding?',
         'optionen': ['Das Einbetten eines Videos', 'Textstücke werden zu Zahlen, die Bedeutung abbilden', 'Das Speichern des Chats'], 'richtig': 1,
         'warum': 'Ähnliche Bedeutungen bekommen ähnliche Zahlen – so erkennt die KI, was zusammengehört.'},
        {'frage': 'Was passiert, wenn im Prompt eine wichtige Angabe fehlt?',
         'optionen': ['Die KI meldet einen Fehler', 'Die KI füllt die Lücke meist mit einer plausiblen Erfindung', 'Die KI antwortet gar nicht'], 'richtig': 1,
         'warum': 'Eine Lücke erzeugt keine Fehlermeldung, sondern eine Erfindung – darum den Kontext mitgeben.'},
    ],
}

# Tag 4 (RAG) steht in kurs_tag4.py
from kurs_tag4 import TAG4  # noqa: E402
TAGE[4] = TAG4

# Tag 5 (Deep Research) steht in kurs_tag5.py
from kurs_tag5 import TAG5  # noqa: E402
TAGE[5] = TAG5

# Tag 6/7 (Prompt Engineering) stehen in kurs_tag6.py / kurs_tag7.py
from kurs_tag6 import TAG6  # noqa: E402
from kurs_tag7 import TAG7  # noqa: E402
TAGE[6] = TAG6
TAGE[7] = TAG7
from kurs_tag8 import TAG8  # noqa: E402
TAGE[8] = TAG8
from kurs_tag9 import TAG9  # noqa: E402
TAGE[9] = TAG9
from kurs_tag10 import TAG10  # noqa: E402
TAGE[10] = TAG10
from kurs_tag11 import TAG11  # noqa: E402
TAGE[11] = TAG11

from kurs_tag12 import TAG12
TAGE[12] = TAG12
from kurs_tag13 import TAG13
TAGE[13] = TAG13

from kurs_tag14 import TAG14
TAGE[14] = TAG14

from kurs_tag15 import TAG15
TAGE[15] = TAG15

from reihe1618.content import course as workshop_course
for workshop_day in (16, 17, 18):
    TAGE[workshop_day] = workshop_course(workshop_day)
