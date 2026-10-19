"""Tag 9 (Lektion 8: Agenten, Folien 1-19) - wird von kurs.py eingelesen.
Ergaenzt um Fakten aus docs.langdock.com (Agent-Konfigurator, Workflows) - dort mit 'quelle': 'Langdock'.
Hinweis: Folie 19 schreibt MCP als "Message Communication Protocol" - richtig ist Model Context Protocol (so auch Folie 8 von Tag 8)."""
TAG9 = {
    'titel': 'Agenten – KI, die plant und handelt',
    'unter': 'Lektion 8 · Agenten',
    'datum': '08.10.2026',
    'folien': 'Agenten.pdf',
    'kurz': 'Was einen Agenten von einem Assistenten unterscheidet, woraus er besteht, wie er in Schleifen arbeitet, wo der Mensch eingreift – und wie mehrere Agenten zusammenarbeiten.',
    'lernheft': 'Lernheft_Tag9_Agenten.pdf',
    'learnings': [
        {'id': 'l1', 'folie': 3, 'satz': 'Generative KI erstellt Inhalte, agentische KI trifft Entscheidungen und führt aus.',
         'erklaert': 'Generative KI reagiert auf einen Prompt und erzeugt Texte, Bilder, Musik oder Code. Agentische KI ist vorausschauend: Sie plant Schritte, '
                     'entscheidet und handelt selbstständig, um ein Ziel mit wenig menschlicher Aufsicht zu erreichen – und passt sich an, wenn sich etwas ändert.'},
        {'id': 'l2', 'folie': 4, 'satz': 'Ein Agent erledigt Aufgaben selbstständig: Er plant seinen Weg und nutzt Werkzeuge.',
         'erklaert': 'Im Kern steuert ein Sprachmodell als „Gehirn“ (darum auch LLM-Agent). Anders als ein reines Sprachmodell ruft er Werkzeuge auf, '
                     'holt aktuelle Informationen, zerlegt Ziele in Teilaufgaben und erreicht so auch schwierige Ziele – teils ohne dass ein Mensch eingreift.'},
        {'id': 'l3', 'folie': 5, 'satz': 'Ein Agent hat sieben Fähigkeiten – von Wahrnehmen bis Lernen.',
         'erklaert': 'Wahrnehmung (Eingaben verstehen), Gedächtnis (kurz für das Gespräch, lang in einer Wissensdatenbank), Planung (in Teilaufgaben zerlegen), '
                     'Entscheidung (Lösungswege abwägen), Handeln mit Werkzeugen, Kommunikation (mit Menschen und anderen Agenten) und Lernen aus Erfahrung.'},
        {'id': 'l4', 'folie': 6, 'satz': 'Agenten sind selbstständig, vorausschauend, spezialisiert, anpassungsfähig und per Sprache steuerbar.',
         'erklaert': 'Sie verfolgen Ziele über mehrere Schritte ohne ständige Aufsicht, suchen selbst im Web oder in Datenbanken, reichen von einfachen '
                     'Routineaufgaben bis zu schwierigen Problemen, lernen aus Feedback – und ganze Software lässt sich auf ein „Gespräch“ mit ihnen reduzieren.'},
        {'id': 'l5', 'folie': 7, 'satz': 'Ein Assistent schlägt vor, ein Agent entscheidet und handelt.',
         'erklaert': 'Ein Assistent braucht für jede Aktion einen Prompt, nutzt feste Funktionen und arbeitet Schritt für Schritt im Dialog – sehr zuverlässig. '
                     'Ein Agent braucht einen Prompt, wählt seine Werkzeuge selbst, zerlegt Aufgaben und verkettet sie – mächtiger, aber abhängig von Werkzeugen und fehleranfälliger.'},
        {'id': 'l6', 'folie': 8, 'satz': 'Der technische Rahmen eines Agenten hat fünf Teile.',
         'erklaert': 'Sprachmodell (Herzstück fürs Verstehen und Entscheiden), Werkzeuge und Aktionen (z. B. Websuche, Datenanalyse, Integrationen), '
                     'eine Umgebung, in der er Code ausführen kann, Wissen (Dokumente, Ordner, Datenbanken) und Steuerung (Anweisungen, Regeln, Abbruchbedingungen). '
                     'Zusammen heißt das oft „Agent Harness“.'},
        {'id': 'l7', 'folie': 9, 'satz': 'Zwei Arten, Agenten zu steuern: ReAct denkt nach jedem Schritt neu, ReWOO plant alles vorab.',
         'erklaert': 'ReAct: Denken → Handeln → Beobachten in einer Schleife, nach jedem Ergebnis wird neu geplant – flexibel und nachvollziehbar. '
                     'ReWOO: Erst ein vollständiger Plan, dann alle Werkzeuge gebündelt – spart Rechenzeit, und man kann den Plan vorher prüfen.'},
        {'id': 'l8', 'folie': 10, 'satz': 'Ein Agent arbeitet in Schleifen – und braucht klare Bremsen.',
         'erklaert': 'Denken, Planen, Handeln, Beobachten – so oft, bis das Ziel erreicht ist. Die Zahl der Runden legt er selbst fest. Beenden soll er bei Zielerreichung, '
                     'nach einer Höchstzahl an Schritten, bei Zeit- oder Kostengrenzen oder wenn ein Mensch eingreift. Ohne solche Bremsen drohen Endlosschleifen und Kosten.'},
        {'id': 'l9', 'folie': 11, 'satz': 'Human-in-the-Loop: Vor wichtigen Aktionen fragt der Agent einen Menschen.',
         'erklaert': 'Vor kritischen Schritten wie Massen-E-Mails oder Zahlungen holt er eine Freigabe ein und pausiert so lange. Rückmeldungen von Menschen '
                     'verbessern ihn, und bei Fehlverhalten kann man ihn sofort abschalten.'},
        {'id': 'l10', 'folie': 12, 'satz': 'Agenten prüft man auf zwei Arten: Stimmt die Antwort – und was hat er getan?',
         'erklaert': 'Evaluierung misst die Qualität: Passt die Antwort zum Kontext, stimmen die Fakten mit den Quellen überein, kommt bei gleicher Frage Ähnliches heraus? '
                     'Beobachtung (Protokolle, Ablaufspuren, Nutzungszahlen, Daumen hoch/runter) zeigt, welche Schritte und Werkzeuge er genutzt hat.'},
        {'id': 'l11', 'folie': 13, 'satz': 'Selbstständige Agenten brauchen Kontrolle und Schutz.',
         'erklaert': 'Risiken: Entscheidungen sind schwer nachvollziehbar, Verzerrungen aus Trainingsdaten können sich verstärken, schlecht geschützte Schnittstellen '
                     'öffnen Datenlecks. Schutz: Zugriffskontrollen, Verschlüsselung, eindeutige Kennungen je Agent und menschliche Aufsicht. Die Regeln (z. B. EU AI Act) hinken hinterher.'},
        {'id': 'l12', 'folie': 15, 'satz': 'Ein Eltern-Agent kann Teilaufgaben an spezialisierte Sub-Agents abgeben.',
         'erklaert': 'Jeder Sub-Agent arbeitet eigenständig mit eigenen Anweisungen, eigenem Wissen, eigenen Werkzeugen und passendem Modell. '
                     'So entstehen fokussierte Spezialisten statt eines überladenen Alles-Könners.'},
        {'id': 'l13', 'folie': 16, 'satz': 'Mehrere Agenten lassen sich zentral, dezentral, hierarchisch oder föderiert koordinieren.',
         'erklaert': 'Zentral: ein Orchestrator verteilt und entscheidet – viel Kontrolle, aber ein Engpass. Dezentral: Agenten stimmen sich direkt ab. '
                     'Hierarchisch: Manager-Agenten steuern ausführende Agenten wie in einer Firma. Föderiert: Zusammenarbeit über Firmengrenzen, ohne alle Daten zu teilen.'},
        {'id': 'l14', 'folie': 17, 'satz': 'Mehrere Agenten bringen Tempo und Ausfallsicherheit – aber auch neue Fehlerquellen.',
         'erklaert': 'Vorteile: Teilaufgaben laufen parallel, fällt einer aus, übernehmen andere, neue Agenten kommen bei Bedarf dazu. Risiken: Nutzen alle dasselbe '
                     'Sprachmodell, können sich Fehler vervielfachen; widersprüchliche Ziele führen zu schlechten Ergebnissen; ohne Bremsen drohen Endlosschleifen.'},
        {'id': 'l15', 'folie': 18, 'satz': 'Agenten starten per Chat, Formular, Zeitplan, Webhook, Integration oder Knopfdruck.',
         'erklaert': 'Chat: direkte Unterhaltung. Formular: sobald jemand Angaben abschickt. Geplant: zu festen Zeiten, z. B. für Berichte. Webhook/API: wenn ein anderes System '
                     'Daten schickt. Integration: wenn in einer verbundenen Anwendung etwas passiert, z. B. eine neue E-Mail. Manuell: per Knopfdruck.'},
        {'id': 'l16', 'folie': 19, 'satz': 'Zum Bauen gibt es Plattformen wie Langdock und n8n – und Protokolle wie MCP und A2A.',
         'erklaert': 'Langdock für Chatbots, Agenten, Workflows und Integrationen; n8n für sichtbare Abläufe zum Zusammenklicken; Agenten-Umgebungen von Anthropic. '
                     'MCP (Model Context Protocol) verbindet Werkzeuge mit Agenten, A2A lässt Agenten direkt miteinander sprechen.'},
        {'id': 'l17', 'folie': None, 'quelle': 'Langdock', 'satz': 'Ein Langdock-Agent besteht aus Anweisungen, Wissen, Fähigkeiten, Integrationen und Modell.',
         'erklaert': 'Im Agenten-Baukasten: Name und Beschreibung, Anweisungen (Rolle, Aufgabe, Kontext, Format), Wissen (Dateien, Ordner, Wissensbasen), '
                     'Fähigkeiten wie Websuche oder Bilderstellung, Integrationen mit Lesen/Schreiben und Bestätigung vor Aktionen, Modell, Kreativität und Gesprächsstarter. '
                     'Workflows starten manuell, per Formular, Webhook, Zeitplan oder Integration.'},
    ],
    'begriffe': [
        ('Generative KI', 'KI, die auf einen Prompt hin Inhalte erstellt – Text, Bild, Musik, Code.'),
        ('Agentische KI', 'KI, die selbst plant, entscheidet und handelt, um ein Ziel zu erreichen.'),
        ('KI-Agent', 'Ein System, das Aufgaben selbstständig erledigt und dabei Werkzeuge nutzt.'),
        ('Werkzeug (Tool)', 'Eine Funktion, die der Agent aufrufen kann, z. B. Websuche oder eine Verbindung zu einem anderen Programm.'),
        ('Agent Harness', 'Der technische Rahmen eines Agenten: Modell, Werkzeuge, Code-Umgebung, Wissen und Steuerung.'),
        ('ReAct / ReWOO', 'Zwei Steuerungsarten: nach jedem Schritt neu denken – oder alles vorab planen.'),
        ('Abbruchbedingung', 'Eine Regel, wann der Agent aufhört: Ziel erreicht, zu viele Schritte, Zeit oder Kosten überschritten.'),
        ('Human-in-the-Loop', 'Ein Mensch gibt wichtige Schritte frei, bevor der Agent sie ausführt.'),
        ('Sub-Agent', 'Ein spezialisierter Agent, dem ein übergeordneter Agent eine Teilaufgabe gibt.'),
        ('Orchestrator', 'Der zentrale Agent, der Aufgaben verteilt und das Ergebnis zusammenführt.'),
    ],
    'karten': [
        ('Generative oder agentische KI: Wer trifft Entscheidungen?', 'Die agentische KI – sie plant, entscheidet und führt aus. Generative KI erstellt Inhalte.'),
        ('Was ist das „Gehirn“ eines Agenten?', 'Ein Sprachmodell (LLM) – darum heißt er auch LLM-Agent.'),
        ('Was kann ein Agent, was ein reines Sprachmodell nicht kann?', 'Werkzeuge aufrufen, aktuelle Infos holen, Teilaufgaben bilden und selbstständig handeln.'),
        ('Nenne vier der sieben Fähigkeiten eines Agenten.', 'Wahrnehmung, Gedächtnis, Planung, Entscheidung, Handeln mit Werkzeugen, Kommunikation, Lernen.'),
        ('Assistent oder Agent: Wer braucht für jede Aktion einen Prompt?', 'Der Assistent. Dem Agenten genügt ein Prompt, danach arbeitet er selbstständig.'),
        ('Warum ist ein Agent fehleranfälliger als ein Assistent?', 'Weil er von Werkzeugen und Schnittstellen abhängt, die ausfallen oder falsch antworten können.'),
        ('Die fünf Teile des technischen Rahmens?', 'Sprachmodell, Werkzeuge/Aktionen, Code-Umgebung, Wissen, Steuerung.'),
        ('ReAct oder ReWOO: Wo kann man den Plan vorher prüfen?', 'Bei ReWOO – der Agent plant zuerst alles und führt dann gebündelt aus.'),
        ('Wann soll ein Agent seine Schleife beenden?', 'Bei Zielerreichung, nach Höchstzahl an Schritten, bei Zeit- oder Kostengrenze oder wenn ein Mensch eingreift.'),
        ('Was heißt Human-in-the-Loop?', 'Vor kritischen Aktionen holt der Agent eine menschliche Freigabe ein und wartet so lange.'),
        ('Was macht ein Orchestrator?', 'Er verteilt Aufgaben an andere Agenten, überwacht sie und trifft die finale Entscheidung.'),
        ('Nenne vier Wege, wie ein Agent starten kann.', 'Chat, Formular, Zeitplan, Webhook/API, Integration (z. B. neue E-Mail), manuell per Knopfdruck.'),
    ],
    'test': [
        {'frage': 'Welche Aussage passt zu agentischer KI?',
         'optionen': ['Sie erstellt nur Texte auf Zuruf', 'Sie plant, entscheidet und handelt, um ein Ziel zu erreichen', 'Sie funktioniert nur ohne Sprachmodell'], 'richtig': 1,
         'warum': 'Merksatz von Folie 3: Generative KI erstellt Inhalte, agentische KI trifft Entscheidungen und führt aus.'},
        {'frage': 'Ein Werkzeug braucht für jede Aktion einen neuen Prompt und schlägt nur vor. Was ist es?',
         'optionen': ['Ein KI-Assistent', 'Ein KI-Agent', 'Ein Orchestrator'], 'richtig': 0,
         'warum': 'Assistent: schlägt vor, Nutzer entscheidet. Agent: ein Prompt genügt, er entscheidet und handelt (Folie 7).'},
        {'frage': 'Bei welcher Steuerungsart kann man den Plan vor der Ausführung prüfen?',
         'optionen': ['ReAct', 'ReWOO', 'Bei keiner'], 'richtig': 1,
         'warum': 'ReWOO plant alle Schritte vorab und ruft die Werkzeuge gebündelt auf (Folie 9).'},
        {'frage': 'Was droht ohne saubere Abbruchbedingungen?',
         'optionen': ['Endlosschleifen mit unnötigen Kosten', 'Schnellere Ergebnisse', 'Gar nichts'], 'richtig': 0,
         'warum': 'Deshalb braucht jede Schleife Bremsen wie Höchstzahl an Schritten oder ein Budget (Folie 10).'},
        {'frage': 'Ein Agent soll 500 Kunden eine E-Mail schicken. Was ist laut Folie 11 sinnvoll?',
         'optionen': ['Sofort senden', 'Vorher eine menschliche Freigabe einholen', 'Die E-Mail zweimal senden'], 'richtig': 1,
         'warum': 'Massen-E-Mails sind eine kritische Aktion – Human-in-the-Loop.'},
        {'frage': 'Ein zentraler Agent verteilt Aufgaben an Spezialisten und entscheidet am Ende. Wie heißt das?',
         'optionen': ['Föderiert', 'Dezentral', 'Zentralisiert (Orchestrator)'], 'richtig': 2,
         'warum': 'Der Orchestrator ist das zentrale „Gehirn“ – mit viel Kontrolle, aber möglichem Engpass (Folie 16).'},
    ],
}
