# Modul 2 · KI-Automation · Lektion 1 in vier Tagen

Die 34 Originalfolien bilden eine gemeinsame Lektion, verteilt auf Montag, 26.10., bis Donnerstag, 29.10.2026. Recherche und Quellenstand: 26.10.2026.

| Tag | Schwerpunkt und Praxis | Folien | Ideen | PDF-Seiten |
| --- | --- | --- | --- | --- |
| Montag | Make-Grundlagen, Free-Budget, Begrüßungs-Mixer | 1–11 | 1–8 | 25 |
| Dienstag | JSON, Datentypen, Mapping, Redaktionsbriefing | 12–16, 24–27 | 9–16 | 28 |
| Mittwoch | Filter, Router, Webhooks, KI-Einordnung, Video-Freigabe | 17–23, 28–30 | 17–23 | 23 |
| Donnerstag | Test-API, Zeitangaben, Qualität und Abschluss | 31–34 | 24–30 | 15 |

Jede Folie und jede der 30 Ideen ist genau einmal zugeordnet. Jedes Tagesheft hat ein eigenes Starterpaket, einen Hauptworkflow, vier Quizfragen mit Erklärungen und getrennte lokale Notizen. Die gesamte Original-PDF bleibt erreichbar; die Tagesansicht zeigt nur die zugeordneten Folien. Alle vier Tage sind schon als Vorschau zugänglich.

## Kostenloser Einstieg

Manuelle Ausführung, keine regelmäßige Planung. Erste drei Hauptworkflows nur mit Make Free; Donnerstag optional öffentlicher JSONPlaceholder-GET ohne API-Key. Free: 1.000 Monatscredits, zwei aktive Szenarien, mindestens 15 Minuten bei regelmäßiger Ausführung, am Recherchetag offiziell geprüft. Planwerte bei einem Bundle: 5 + 5 + 5 + 3 = 18 Credits für die beschriebenen Versuche. Weitere Tests und Fehler zusätzlich. Das eigene Unterrichtsbudget von 50 Credits gilt für die gesamte Reihe. Die Kontoanzeige ist maßgeblich.

Die kostenpflichtigen bzw. kontenabhängigen Outlook/Excel- und Formular/KI/CRM-Beispiele aus der Vorlage werden eingeordnet. Keine kostenlosen externen KI-APIs behauptet. Keine Make-Szenarien in Teilnehmerkonten ausgeführt; Creditwerte sind berechnet. Nur der öffentliche API-GET wurde tatsächlich mit HTTP 200 geprüft (`api-proof.json`).

## Qualität und Bauen

66 PDF-Seiten gerendert, Textgrenzen und alle Gesamtansichten visuell geprüft; minimale Schrift-Skalierung 0,96. Browserprüfung: 51 Seiten, 2.058 lokale Verweise, 33 Kopieraktionen, 144 Quizpfade, 15 JSON-Fälle, alle zwölf Teilnehmer-/Tageskombinationen. Notizen bleiben pro Person und Tag getrennt; der bisherige Montag-Speicherschlüssel bleibt erhalten. 320/390/1280 px ohne horizontalen Überlauf, keine beobachteten JavaScript- oder Konsolenfehler.

Aus `_quellen`: `python modul2/tag1/build.py`, dann `python build.py --web`. Bei laufendem Server auf Port 5387: `python modul2/tag1/validate.py`. QA unter `_quellen/build/modul2-tag1/`. Zentrale Tageszuordnung: `series.py`; Web/PDF-Kapitel: `series_render.py`. `content.py` bleibt der gemeinsame Folien- und Erklärungsbestand. Die internen Kennungen 20–23 erhalten alte Tag-Links; sichtbar sind Modul 2, Lektion 1, Tag 1–4.

## Veröffentlichung

Release `20261026-modul2-vier-tage` ersetzt die frühere Verteilung aller Inhalte auf Montag. Tagesadressen: `/hefte/{ingo|carmen|tabea}/modul-2/tag-{1|2|3|4}/`. Live-Nachweise werden nach Veröffentlichung im Betriebsprotokoll ergänzt.


Live am 26.10.2026: Release `20261026-modul2-vier-tage`. 28 Live-Seiten inklusive aller zwölf Teilnehmer-/Tageskombinationen erfolgreich geprüft. 136 öffentliche Dateien per HTTPS bytegenau verglichen, internes Manifest und 137 Host-Zieldateien geprüft. Container gesund, Serverdateien unverändert; vorherige Public-Dateien und Docker-Image gesichert. 25 bestehende Node-Tests bestanden. 54 ältere Tagesseiten nach Normalisierung von Leerzeichen und Aufgaben-Cacheparameter inhaltlich unverändert. Live: https://quint-games.de/hefte/tabea/modul-2/tag-1/ bis `/tag-4/`.


## Darstellungsfehler Carmen · 26.10.2026

Screenshot zeigte ein vollständig ungestaltetes Modul-2-Lernheft. Bei eigenen Live-Aufrufen lieferten die drei CSS-Dateien HTTP 200 und wurden auch in WebKit angewendet; die konkrete Ursache auf Carmens Gerät war nicht reproduzierbar. Der komplette Lesestil steht jetzt direkt im HTML, statt von drei separaten CSS-Abrufen abzuhängen. Gilt für alle zwölf Teilnehmer-/Tageskombinationen, jeweils Tagesseite und Lernheft, einschließlich der bisherigen Tag-20–23-Adressen. PDF-Inhalte und Notizschlüssel unverändert.

Regression `modul2/tag1/validate_layout.py`: externe CSS-Anfragen blockiert; pro lokalem und Live-Lauf 48 Browseransichten in WebKit/Chrome, vier Breiten (320/390/834/1280), 96 Quizantworten und Budgetrechner erfolgreich. Keine externen Layout-Anfragen mehr nötig, keine beobachteten JavaScript-Fehler. Dies ist ein Engine-Test, kein direkter Zugriff auf Carmens Mac.

Live-Release `20261026-carmen-layout`: 48 öffentliche HTML-Dateien per HTTPS bytegenau verglichen, 49 Host-Dateien inklusive Manifest geprüft. Container gesund, Serverdateien unverändert, vorherige Dateien und Docker-Image gesichert.


## Heute einfacher erklärt und Quiz gespeichert · 26.10.2026

Nur Modul 2, Tag 1 überarbeitet. Das Lernheft führt mit einem Beispiel durch Verstehen, Nachbauen, Prüfen: Luna bereitstellen, Begrüßung bauen, mit Mira testen. Fünf getrennte Bauschritte erklären jeweils Klickweg, Soll-Ergebnis und Fehlerhilfe. Begriffe werden am Beispiel erklärt. Wichtige Hinweise sind beschriftet und farblich hervorgehoben; englische Bedienwörter fett, Handlungen nummeriert. Agentenwissen, acht Ideen und die Einordnung der elf Originalfolien stehen im freiwilligen, im Web zugeklappten Anhang. Keine JSON-Aufgaben oder Zusatzkonten am ersten Tag. Das Starterpaket enthält einfache Merkzettel und Testnamen. Die neue PDF umfasst 25 Seiten ohne verkleinerte Schrift (Skalierung 1,0); alle Seiten gerendert, Gesamtansichten und Bauschritt groß geprüft.

Ursache des Quiz-Speicherproblems: Der frühere Handler prüfte Antworten lediglich im Arbeitsspeicher und schrieb keinen Quizstand in localStorage. Heute werden Auswahl und Prüfstatus automatisch pro Teilnehmer gespeichert, mit sichtbarem Status, zusätzlichem Speichern-Knopf und Textexport. Speicherung gilt für diesen Browser auf diesem Gerät; keine Synchronisierung zwischen Geräten. Fehlerhafter oder gesperrter Speicher ergibt einen Hinweis statt falscher Erfolgsmeldung. Notizschlüssel bleiben unverändert. Logik und Stile für die neue Oberfläche werden nur bei Tag 1 aktiv.

Lokale und Live-Prüfung jeweils in WebKit und Chrome für Carmen, Ingo und Tabea: sechs Ansichten, jeweils echte Browser-Neustarts mit gleichem Profil (zwei Engines), Auswahl und Feedback nach Neuladen, zwei Fälle mit blockiertem Speicher, sechs beschädigte Speicherstände und acht Textdownloads. Kein beobachteter JavaScript-Fehler. Vier Breiten (320/390/834/1280), vergrößerte Schrift, blockierte externe CSS-Dateien sowie Antwortprüfung/Speichern per Tastatur kontrolliert. Keine vollständige Screenreader-Abnahme und keine Szenarioausführung in Teilnehmerkonten.

Release `20261026-tag1-einfach` live: 27 öffentliche Dateien per HTTPS bytegenau geprüft, 28 Host-Dateien einschließlich Manifest. 1.191 lokale Verweise geprüft. Vollständige öffentliche Dateiliste vor/nach verglichen: außerhalb der Release-Ziele alles unverändert, insbesondere die späteren Tagesseiten. 54 nur durch den globalen Aufgaben-Cachetoken abweichende alte Tagesseiten ausdrücklich nicht veröffentlicht. Im gemeinsamen Aufgabendatensatz änderte sich nur Eintrag 20 (heute). Container gesund, Serverdateien unverändert, Sicherung vor Veröffentlichung vorhanden.


## Tag 2 im einfachen Leselayout · 27.10.2026

Dienstag (Modul 2, Lektion 1, Tag 2) für Carmen, Ingo und Tabea überarbeitet. Wie Tag 1: Verstehen → Nachbauen → Prüfen, beschriftete wichtige Hinweise, nummerierte Handlungen, Soll-Ergebnis und Fehlerhilfe. Sechs kleine Bauschritte: eigenes Szenario, vier JSON-Testangaben einfügen, ersten Baustein allein prüfen, vier Felder in Compose a string auswählen, Ausgabe lesen, zweites Beispiel mit Nordlicht prüfen. Vorbereitungszettel ohne KI-, Microsoft- oder Social-Verbindung. Outlook/Excel, weitere Datentypen, Datenfluss, Ideen 9–16 und alle neun zugeordneten Originalfolien bleiben im freiwilligen Anhang erklärt. Muster sind ausdrücklich JSON-Eingaben und keine importierbaren Szenario-Blueprints.

Die aktuelle Make-Dokumentation zu JSON, Mapping, Operations und Blueprints am 27.10.2026 erneut gelesen; Nachweis in `sources-day2.json`. Keine Szenarien in Teilnehmerkonten ausgeführt. Budgetangaben sind Planwerte. Tages-PDF: 28 Seiten, alle gerendert und visuell geprüft, Schrift-Skalierung durchgehend 1,0. Testpaket mit erstem/zweitem JSON-Muster, einfacher Anleitung und Merkzettel. PDF und Plattform wurden gemeinsam aktualisiert.

Quiz mit automatischer Speicherung von Auswahl und Prüfstatus, zusätzlichem Speichern-Knopf, sichtbarer Fehlermeldung und Textexport. Eigener Schlüssel `kurs:modul2:lektion1:{person}:tag2:quiz:v2`; Tag-1-Quizschlüssel und bestehende Tag-2-Notizschlüssel unverändert. Speicherung ist lokal auf diesem Gerät im jeweiligen Browser; keine Gerätesynchronisierung. Fehlerhafte Daten werden nicht als gültige Ergebnisse übernommen.

Lokal und live jeweils in WebKit/Chrome geprüft: sechs Teilnehmeransichten, zwei echte Neustarts mit gleichem Browserprofil, Auswahl/Feedback nach Reload, zwei Fälle mit gesperrtem Speicher, sechs beschädigte Speicherstände und acht Quizdownloads. Zweier-JSON-Muster und Kopieraktionen geprüft; Tag-1-Speicher bleibt getrennt. 320/390/834/1280 px sowie vergrößerte Schrift und blockierte externe CSS-Anfragen geprüft; keine beobachteten JS-Fehler. Keine direkte Prüfung auf Carmens Mac und keine vollständige Screenreader-Abnahme.

Release `20261027-tag2-einfach` live. 25 öffentliche Dateien per HTTPS bytegenau verglichen, 26 Host-Dateien einschließlich Manifest geprüft; 1.179 lokale Verweise kontrolliert. Die gesamte öffentliche Dateiliste vor/nach abgeglichen: außerhalb der vorgesehenen Ziele alles unverändert. Tag-1-Seiten, dessen PDF/Quizcode sowie die späteren Tagesseiten unverändert. Alte Seiten mit bloß abweichender Aufgaben-Cachekennung nicht veröffentlicht. Im gemeinsamen Aufgabendatensatz änderte sich nur Eintrag 21 (Tag 2). Container gesund, Serverdateien unverändert, Sicherung vor Veröffentlichung vorhanden.


## Mittwoch nochmals deutlich vereinfacht · 28.10.2026 (veröffentlicht 27.10.)

Tag 3 heißt jetzt „Die einfache Freigabe-Ampel“. Die sichtbare Hauptstrecke hat nur zwei Erklärkapitel, vier Bauschritte, Fehlerhilfe und vier sehr leichte Quizfragen. Hauptablauf: Tools Set variable stellt den Textstatus bereit, genau ein Filter erlaubt FERTIG, Tools Compose a string zeigt die Meldung. ENTWURF stoppt. Kein JSON, AND/OR, Router, KI-Aufruf oder zusätzliches Konto in der Hauptübung. Browser-Ampel zum kostenlosen Durchspielen von Weiter/Stopp.

Zwei klar freiwillige kleine Automationen statt einer großen Kontaktformular-Kette: RSS Retrieve RSS Feed Items liest maximal eine Schlagzeile aus dem öffentlich geprüften deutschsprachigen tagesschau-Feed; Compose a string macht einen Lesezettel daraus. Zweites Extra nur mit bestehendem Google-Konto: eine Idee aus Set variable nach Google Sheets Add a Row übertragen. Jede Ausführung fügt eine Zeile in die eigene neue Tabelle hinzu. Keine Veröffentlichung, kein Mailversand, keine externen Kontoschreibaktionen durch den Agenten. Google-Einrichtung nicht als bei jedem Konto sofort lauffähig versprochen; RSS bleibt die Alternative ohne zusätzliche Anmeldung.

Die zehn Originalfolien (17–23 und 28–30), sieben restlichen Branchenideen und die schwierigen Begriffe bleiben im aufklappbaren Nachleseteil. System-/User-/Assistant-Rollen, Formular-KI-Kette, Fehlerprüfung und Router-Reihenfolge werden erklärt, aber nicht als Baupflicht aufgegeben. Recherche am 27.10.2026 anhand offizieller Make-Unterlagen; öffentlicher RSS-GET separat mit HTTP 200 und gültigen Items geprüft (`sources-day3.json`, `rss-day3-proof.json`). Keine Make-Szenarien in Teilnehmerkonten ausgeführt, keine Google-Verbindung eingerichtet. Planwerte klar von echtem Verbrauch getrennt: Hauptversuche ungefähr 4 Credits; jedes freiwillige Extra mit Einzelprobe und Zweierlauf ungefähr 3. Unterrichtsbudget für die ganze Reihe bleibt 50.

PDF: 23 Seiten, alle gerendert, Textgrenzen geprüft und alle Kontaktansichten visuell kontrolliert, Schrift-Skalierung überall 1,0. Neues Starterpaket enthält nur einfache Merkzettel, die zwei Status-Testwerte und RSS-Adresse statt JSON-/KI-Aufgaben. Quiz behält Auswahl und Prüfstatus pro Teilnehmer und Tag 3 im jeweiligen Browser auf diesem Gerät. Speichern-Knopf, Speicheranzeige und Textdownload sind vorhanden; kein Geräteabgleich. Frühere Quiz- und Notizschlüssel bleiben unverändert.

Lokal und live jeweils sechs Teilnehmeransichten in WebKit/Chrome, zwei echte Browser-Neustarts, zwei Fälle mit blockiertem Speicher, sechs beschädigte Speicherstände und acht Quizdownloads geprüft. Beide Ampelwerte, RSS-Kopierknopf (Chrome inklusive tatsächlichem Lesen der Zwischenablage), getrennte Tag-1-/Tag-2-Speicher und vier Breiten (320/390/834/1280) plus vergrößerte Schrift geprüft. Externe CSS-Anfragen absichtlich gesperrt; Layout bleibt eingebaut. Keine beobachteten JS-Fehler. Kein direkter Zugriff auf Carmens Mac und keine vollständige Screenreader-Abnahme.

Release `20261027-tag3-leicht` live für Carmen, Ingo und Tabea. 29 öffentliche Dateien per HTTPS bytegenau verglichen; 30 Host-Dateien inklusive Manifest geprüft. 1.482 lokale Verweise kontrolliert. Komplette öffentliche Dateiliste vorher/nachher verglichen: außerhalb der Release-Ziele alles unverändert. Die anderen Tagesseiten und ihre PDFs bleiben unverändert; nur Übersichten und abhängige Aufgaben-/Lernblattdateien wurden passend zu Tag 3 aktualisiert. Im gemeinsamen Aufgabendatensatz änderte sich ausschließlich Eintrag 22. 54 ältere Tagesseiten mit bloßer Cachekennung-Abweichung nicht veröffentlicht. Container gesund, Serverdateien unverändert, vorheriges Public-Verzeichnis und Image gesichert.
