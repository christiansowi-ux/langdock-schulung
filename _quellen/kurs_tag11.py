"""Tag 11 (Lektion 10: KI-Infrastruktur, Folien 1-19) - wird von kurs.py eingelesen.
Auf den Folien: Folie 13 "innerhablb" (= innerhalb)."""
TAG11 = {
    'titel': 'KI-Infrastruktur – welcher Stack ist der richtige?',
    'unter': 'Lektion 10 · KI-Infrastruktur',
    'datum': '12.10.2026',
    'folien': 'KI-Infrastruktur.pdf',
    'kurz': 'Was technisch hinter KI im Unternehmen steckt: Modelle, Server, Schnittstellen, Plattformen – und wie man zwischen fertigem Dienst, '
            'verwalteter Plattform und Eigenbetrieb entscheidet.',
    'lernheft': 'Lernheft_Tag11_KI-Infrastruktur.pdf',
    'learnings': [
        {'id': 'l1', 'folie': 2, 'satz': 'Die Leitfragen: Was brauche ich technisch – und wie viel baue ich selbst?',
         'erklaert': 'Ein KI-„Stack“ ist der Stapel aus Bausteinen, die zusammen ein KI-Werkzeug ergeben: Modell, Server, Schnittstellen, Oberfläche, Wissensspeicher '
                     'und Schutz. Man kann alles fertig kaufen, alles selbst betreiben – oder etwas dazwischen wählen.'},
        {'id': 'l2', 'folie': 3, 'satz': 'Vier Gründe für eigene Infrastruktur: Daten, Regeln, Unabhängigkeit, planbare Kosten.',
         'erklaert': 'Datensouveränität (Daten auf eigenen Servern), Compliance (wer die Technik kontrolliert, kontrolliert die Einhaltung der Regeln), '
                     'kein Lock-in (nicht von einem US-Anbieter abhängig) und planbare Kosten (Kosten für Rechenleistung statt Preis pro Person).'},
        {'id': 'l3', 'folie': 3, 'satz': '„Server in Frankfurt“ heißt noch nicht souverän.',
         'erklaert': 'Der US-amerikanische CLOUD Act gilt für US-Konzerne weltweit – auch wenn ihre Rechenzentren in Deutschland stehen. '
                     'US-Behörden können die Herausgabe von Daten verlangen. Entscheidend ist also auch, welchem Recht der Anbieter unterliegt.'},
        {'id': 'l4', 'folie': 3, 'satz': 'Fünf Regelwerke und Standards prägen den Rahmen.',
         'erklaert': 'DSGVO (Schutz personenbezogener Daten in der EU), EU AI Act (KI-Regeln nach Risiko, schrittweise ab 2025), BSI C5 (deutscher Standard für sichere Cloud), '
                     'ISO 27001 (internationaler Standard für Informationssicherheit) und SOC 2 (US-Prüfstandard für Datensicherheit bei Dienstleistern).'},
        {'id': 'l5', 'folie': 4, 'satz': 'Serving-Engines sind die Programme, die ein Modell betreiben – für Server oder für den eigenen Rechner.',
         'erklaert': 'Für leistungsstarke Server: vLLM, SGLang oder Lösungen von NVIDIA. Für den eigenen Rechner zum Ausprobieren: Ollama, llama.cpp, LM Studio oder GPT4All.'},
        {'id': 'l6', 'folie': 5, 'satz': 'Der Grafikspeicher (VRAM) ist der Engpass: rund 2 GB je Milliarde Parameter.',
         'erklaert': 'In 16-Bit-Genauigkeit braucht ein Modell etwa 2 GB Grafikspeicher pro Milliarde Parameter. Modelle mit 7–8 Milliarden laufen auf einem Laptop oder einer '
                     'normalen Grafikkarte, 70 Milliarden brauchen mehrere Grafikkarten, über 100 Milliarden einen Rechner-Verbund.'},
        {'id': 'l7', 'folie': 5, 'satz': 'Quantisierung macht Modelle kleiner – fast ohne Qualitätsverlust.',
         'erklaert': 'Die Zahlen im Modell werden von 16 auf 8 oder 4 Bit verkürzt. Ein 70-Milliarden-Modell schrumpft so von etwa 140 GB auf etwa 40 GB. '
                     'Übliche Formate: GGUF (lokal mit Ollama/llama.cpp), GPTQ und AWQ (Grafikkarten, 4 Bit) und FP8 (moderne Grafikkarten).'},
        {'id': 'l8', 'folie': 6, 'satz': 'Drei Kennzahlen zeigen, wie gut ein KI-Dienst läuft: Reaktionszeit, Tempo, gleichzeitige Nutzung.',
         'erklaert': 'TTFT (Zeit bis zum ersten Wort) ist die gefühlte Reaktionszeit. Tokens pro Sekunde zeigen, wie flüssig der Text kommt. Durchsatz und Parallelität '
                     'sagen, wie viele Menschen gleichzeitig arbeiten können – und damit die Kosten pro Person. Schnelle Antwort und viele Nutzer gleichzeitig gibt es selten zugleich.'},
        {'id': 'l9', 'folie': 7, 'satz': '„OpenAI-kompatibel“ macht Anbieter austauschbar – nur Adresse und Schlüssel tauschen.',
         'erklaert': 'Es gibt vier API-Arten: Completion (alt), Chat Completions (heute Standard), Responses/Messages (neu, für Agenten) und Embeddings (Text → Zahlen für Suche und RAG). '
                     'Viele Anbieter verstehen dieselbe „OpenAI-kompatible“ Schnittstelle: Ein Wechsel heißt nur base_url und Key austauschen.'},
        {'id': 'l10', 'folie': 8, 'satz': 'Aggregatoren bündeln viele Modell-Anbieter unter einem Zugang.',
         'erklaert': 'So kann man je nach Kosten, Verfügbarkeit und Spezialgebiet das passende Modell wählen – oft mit Überwachung und automatischem Ausweichen bei Ausfällen. '
                     'Beispiele von der Folie: OpenRouter, together.ai, Requesty, Fireworks AI, Azure AI Foundry, IONOS, STACKIT, AKI.'},
        {'id': 'l11', 'folie': 9, 'satz': 'Ein Gateway ist die Schaltzentrale vor den Modellen.',
         'erklaert': 'Es verwaltet Schlüssel, Budgets und Grenzen, springt bei Ausfällen auf ein anderes Modell um und protokolliert jede Anfrage. '
                     'Beispiele: LiteLLM, Portkey, Kong, Cloudflare.'},
        {'id': 'l12', 'folie': 10, 'satz': 'Oberfläche und Wissensspeicher kann man auch selbst betreiben.',
         'erklaert': 'Open-Source-Oberflächen wie Open WebUI (am beliebtesten, mit RAG), AnythingLLM (Fokus auf Dokumente), LibreChat oder Jan. Als Vektor-Datenbank für RAG: '
                     'Qdrant (schnell), Weaviate (kombinierte Suche), Chroma (leichtgewichtig) oder pgvector (in PostgreSQL).'},
        {'id': 'l13', 'folie': 12, 'satz': 'Drei Betriebsmodelle: fertig nutzen, verwaltete Plattform oder alles selbst.',
         'erklaert': 'Turnkey (ChatGPT, Claude, Gemini, Copilot): sofort nutzbar, beste Modelle – aber Daten beim US-Anbieter. Managed (z. B. Langdock): fertige Oberfläche auf '
                     'EU-Infrastruktur, DSGVO-konform, wenig Aufwand – oft der Mittelweg für den Mittelstand. Self-hosted: maximale Kontrolle, aber viel Aufwand und Fachwissen.'},
        {'id': 'l14', 'folie': 13, 'satz': 'EU-Region ist nicht EU-Recht: Souveränität hat Stufen.',
         'erklaert': 'Von wenig zu viel Kontrolle: SaaS (gemeinsamer Dienst), Single-Tenant (eigene Instanz beim Anbieter), Bring Your Own Cloud (in der eigenen Cloud), '
                     'On-Prem (im eigenen Haus). Für eine Kanzlei eher die kontrollierten Stufen wählen. US-Anbieter mit EU-Rechenzentren unterliegen weiter dem CLOUD Act.'},
        {'id': 'l15', 'folie': 14, 'satz': 'Souveränität betrifft auch das Modell: Es gibt starke europäische Anbieter.',
         'erklaert': 'Mistral (Frankreich), Aleph Alpha und Black Forest Labs mit FLUX für Bilder (Deutschland), Apertus (Schweiz, vollständig offen). Souveräne Infrastruktur: '
                     'StackIT, aki.io, noirdoc. Offene Modelle wie Llama, Qwen oder DeepSeek lassen sich in der EU betreiben.'},
        {'id': 'l16', 'folie': 15, 'satz': 'API-Kosten wachsen mit der Nutzung, eigener Betrieb ist nach der Anschaffung flach.',
         'erklaert': 'Ab einem bestimmten Volumen (Break-Even) wird Eigenbetrieb günstiger. Preismodelle: pro Person (Turnkey/Managed), pro Token (API), pro GPU-Stunde '
                     '(eigene Server) oder gemischt. Die Gesamtkosten (TCO) = Hardware + Strom + Personal + Abschreibung.'},
        {'id': 'l17', 'folie': 16, 'satz': 'Ohne Überwachung und Schutz kein echter Betrieb.',
         'erklaert': 'Schutz: noirdoc maskiert persönliche Daten vor dem Modell, Llama Guard filtert Inhalte, NeMo Guardrails setzt Regeln, Lakera schützt vor Prompt Injection. '
                     'Überwachung: Langfuse (Open Source, EU), Helicone (Kosten), Phoenix/Arize, OpenLLMetry.'},
        {'id': 'l18', 'folie': 17, 'satz': 'Make or Buy: vier Leitfragen führen zur Entscheidung.',
         'erklaert': 'Sensible Daten? → EU-Anbieter oder eigener Betrieb. Hohe Auslastung? → Eigenbetrieb prüfen (Break-Even). Schneller Start? → Managed-Plattform wie Langdock. '
                     'Sonst → selbst betreiben mit EU-API (z. B. aki.io oder StackIT).'},
        {'id': 'l19', 'folie': 18, 'satz': 'Der Stack ist eine Landkarte – und Souveränität heißt EU-Anbieter plus EU-Recht.',
         'erklaert': 'Jedes Werkzeug sitzt auf einer Ebene, keines ist überall. „OpenAI-kompatibel“ macht Anbieter austauschbar. Souveränität entsteht nicht durch EU-Server allein, '
                     'sondern durch das Recht, dem das Unternehmen unterliegt.'},
        {'id': 'l20', 'folie': 19, 'satz': 'Die Aufgabe: einen Stack für eine Kanzlei bauen und begründen.',
         'erklaert': 'Betriebsmodell wählen, jede Schicht festlegen (Modell, Inferenz, Gateway, Oberfläche, RAG, Datenschutz), jede Wahl an einer Randbedingung begründen '
                     '(Schweigepflicht nach §203, DSGVO, nur EU, Budget) und den Break-Even rechnen – für 200 Nutzer und 500.000 Tokens pro Tag.'},
    ],
    'begriffe': [
        ('Stack', 'Der Stapel aus Bausteinen, die zusammen ein KI-System ergeben: Modell, Server, Schnittstelle, Oberfläche, Speicher, Schutz.'),
        ('Souveränität', 'Volle Kontrolle über Daten und Technik – nach EU-Recht, ohne Zugriff ausländischer Behörden.'),
        ('CLOUD Act', 'US-Gesetz: US-Firmen müssen Daten auch aus ausländischen Rechenzentren herausgeben.'),
        ('Serving-Engine', 'Programm, das ein Sprachmodell auf einem Rechner betreibt, z. B. vLLM oder Ollama.'),
        ('VRAM', 'Grafikspeicher – reicht er nicht, läuft das Modell nicht.'),
        ('Quantisierung', 'Zahlen im Modell verkürzen (16 → 8 → 4 Bit), damit es weniger Speicher braucht.'),
        ('TTFT', 'Time to First Token: Zeit bis zum ersten Wort der Antwort.'),
        ('OpenAI-kompatibel', 'Gleiche Schnittstelle wie OpenAI – Anbieterwechsel durch Tausch von Adresse und Schlüssel.'),
        ('Gateway', 'Schaltzentrale vor den Modellen: Schlüssel, Budgets, Ausweichmodelle, Protokolle.'),
        ('Turnkey / Managed / Self-hosted', 'Fertig nutzen · verwaltete Plattform · alles selbst betreiben.'),
        ('Break-Even', 'Der Punkt, ab dem Eigenbetrieb günstiger ist als Abo oder API.'),
        ('TCO', 'Gesamtkosten: Hardware + Strom + Personal + Abschreibung.'),
    ],
    'karten': [
        ('Was ist ein KI-Stack?', 'Der Stapel aus Bausteinen: Modell, Server, Schnittstelle, Oberfläche, Wissensspeicher, Schutz und Überwachung.'),
        ('Warum ist „Server in Frankfurt“ nicht automatisch souverän?', 'Wegen des CLOUD Act: US-Konzerne müssen Daten weltweit herausgeben – egal wo der Server steht.'),
        ('Nenne zwei Gründe für eigene Infrastruktur.', 'Datensouveränität, Kontrolle über Compliance, kein Lock-in, planbare Kosten.'),
        ('Faustregel für den Grafikspeicher?', 'In 16 Bit rund 2 GB pro Milliarde Parameter – ein 8B-Modell also etwa 16 GB.'),
        ('Was bringt Quantisierung?', 'Weniger Speicher bei kaum Qualitätsverlust: 70B schrumpft von ~140 GB auf ~40 GB.'),
        ('Was misst TTFT?', 'Die Zeit bis zum ersten Wort – die gefühlte Reaktionszeit.'),
        ('Was heißt „OpenAI-kompatibel“?', 'Gleiche Schnittstelle – ein Anbieterwechsel heißt nur base_url und Key tauschen.'),
        ('Wofür ist ein Gateway da?', 'Schlüssel, Budgets, Grenzen, Ausweichmodelle und Protokolle an einer Stelle.'),
        ('Die drei Betriebsmodelle?', 'Turnkey (fertig, US), Managed (z. B. Langdock, EU) und Self-hosted (alles selbst).'),
        ('EU-Region oder EU-Jurisdiktion – was zählt für Souveränität?', 'Die Jurisdiktion: EU-Anbieter unter EU-Recht, nicht nur EU-Server.'),
        ('Woraus besteht die TCO?', 'Hardware + Strom + Personal + Abschreibung.'),
        ('Die vier Leitfragen für Make or Buy?', 'Sensible Daten? Hohe Auslastung? Schneller Start? Sonst: selbst betreiben mit EU-API.'),
    ],
    'test': [
        {'frage': 'Ein US-Anbieter speichert Daten in Frankfurt. Ist das automatisch souverän?',
         'optionen': ['Ja, der Server steht in Deutschland', 'Nein, der CLOUD Act gilt für US-Konzerne weltweit', 'Nur am Wochenende'], 'richtig': 1,
         'warum': '„Server in Frankfurt“ ≠ souverän – entscheidend ist das Recht, dem der Anbieter unterliegt (Folie 3).'},
        {'frage': 'Wie viel Grafikspeicher braucht ein 70-Milliarden-Modell ungefähr in 16 Bit?',
         'optionen': ['ca. 14 GB', 'ca. 140 GB', 'ca. 1.400 GB'], 'richtig': 1,
         'warum': 'Faustregel 2 GB pro Milliarde Parameter: 70 × 2 = 140 GB. Mit 4-Bit-Quantisierung etwa 40 GB (Folie 5).'},
        {'frage': 'Was muss man bei einer „OpenAI-kompatiblen“ API für einen Anbieterwechsel ändern?',
         'optionen': ['Das ganze Programm neu schreiben', 'Nur base_url und Key', 'Die Grafikkarte'], 'richtig': 1,
         'warum': 'Das macht Souveränität praktisch machbar (Folie 7).'},
        {'frage': 'Welches Betriebsmodell ist laut Folie oft der pragmatische Mittelweg für den Mittelstand?',
         'optionen': ['Turnkey', 'Managed', 'Self-hosted'], 'richtig': 1,
         'warum': 'Fertige Oberfläche auf EU-Infrastruktur, DSGVO-konform, wenig Aufwand (Folie 12).'},
        {'frage': 'Was gehört NICHT zur TCO?',
         'optionen': ['Strom', 'Personal', 'Die Farbe des Logos'], 'richtig': 2,
         'warum': 'TCO = Hardware + Strom + Personal + Abschreibung (Folie 15).'},
        {'frage': 'Ein Unternehmen hat sensible Daten. Was empfiehlt das Make-or-Buy-Schema zuerst?',
         'optionen': ['EU-Anbieter oder eigener Betrieb', 'Den billigsten US-Dienst', 'Gar keine KI'], 'richtig': 0,
         'warum': 'Erste Leitfrage: Sensible Daten? → EU-Anbieter / On-Prem (Folie 17).'},
    ],
}
