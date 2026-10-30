# Verständlich erklären und aktiv lernen

Von Chris am 14.10.2026 ausdrücklich gewünscht: Die Plattform soll weniger trocken sein, den Lerneffekt unterstützen und die Folien vollständig in anderen, ohne Vorwissen verständlichen Worten vermitteln.

## Verbindlicher redaktioneller Ablauf für kommende Lektionen

1. Jede Originalfolie erfassen, einschließlich Text in Grafiken. PDF-Textauszug allein reicht nicht. Visuellen Abgleich machen.
2. Pro Folie: **Einfach gesagt → alle Einzelheiten in verständlicher Sprache → ausgedachtes Alltagsbeispiel → Verständnisfrage → eine mögliche Antwort**.
3. Fachwörter beim ersten Auftreten im Zusammenhang erklären. Inhalt nicht auf ein Schlagwort verkürzen. Einfacher formulieren darf keine Bedingungen, Ausnahmen, Rollen, Fristen oder Arbeitsschritte verschwinden lassen.
4. Originalfolie direkt verlinken. Eine Zuordnungsliste aller Folien führen; keine Folie still überspringen. Inhaltliche Abdeckung und tatsächliches Verständnis sind verschieden: Eine vollständige Zuordnung garantiert noch keinen Lernerfolg.
5. Fehler oder veraltete Aussagen der Quelle nicht als Wahrheit wiederholen. Original unverändert lassen, Korrektur klar markieren, aktuelle Primärquelle und Prüfdatum nennen. Zusatzwissen und didaktische Vergleiche als solche kenntlich machen.
6. Praxisfälle passend zu Druck/Vertrieb, Team/Website und Video/Design ergänzen. Nur erfundene Situationen und Daten. Für Tabea immer einen nutzbaren Weg ohne Agenten vorsehen.
7. Zu jeder Antwortalternative begründen, warum sie passt oder nicht passt. Falsche Antworten ohne Beschämung als Lernanlass nutzen. Unsichere Fälle erneut anbieten.
8. Musterantworten sind mögliche Formulierungen: Andere eigene Worte können denselben Gedanken richtig ausdrücken. Freitext ohne fachlich belastbare Bewertung nicht automatisch als richtig/falsch markieren.
9. Erst selbst erinnern, dann aufdecken. Kleine Runden ohne Countdown; unsichere Karten erneut in derselben Runde, später Wiederholungen mit zeitlichem Abstand.
10. Vor Freigabe: Folienabdeckung und Beispiele redaktionell prüfen, Links und Speicherverhalten testen, kleine Bildschirme und Tastaturbedienung prüfen. Keine unbelegte Zusage, dass etwas „100 % verstanden“ wird.

## Stand der Umsetzung

- Neuer Reiter **Trainieren** an allen 12 Kurstagen für alle drei Personen; zusätzlich Einstieg in der persönlichen Kursübersicht.
- Runde mit maximal fünf Ausgangsfragen; jede unsichere Karte höchstens einmal zusätzlich in dieser Runde. Danach bleibt sie ggf. fällig, ohne Endlosschleife.
- Abruf nach 1, 3 und 7 Kalendertagen. Mehrere Antworten am selben Tag erhöhen die Stufe nicht mehrfach. Freiwilliges Wiederholen vor Fälligkeit verschiebt einen sicheren Termin nicht.
- Fällige Karten aus früheren Tagen zuerst; neue Karten nur aus dem geöffneten Tag. Damit wird niemand beim Einstieg mit ungelerntem früheren Stoff überladen.
- Tag 12: **Einfach erklärt**, 23 Folienbegleitungen und 23 daraus abgeleitete Abruffragen. Insgesamt neun redaktionelle Fälle, davon drei gemeinsam und zwei je Profil; jede Person sieht fünf.
- Bestehende 12 Lernkarten und sechs Selbsttestfragen bleiben zusätzlich erreichbar. Tag 1–11 haben den neuen Abrufablauf auf Basis der vorhandenen Fragen; noch keine neu redigierte vollständige Folienbegleitung wie Tag 12.
- Eigener Merksatz pro Person und Tag. Speicherung ausschließlich im Browser unter `kurs:training:v1:<person>`; alte `kurs:v1:*`- und `hefte:v1:*`-Daten werden nicht umgeschrieben.
- Kein Servertracking, keine Erinnerungs-E-Mails, keine Konten oder Benotung. Bei fehlendem Browser-Speicher wird auf die nur vorübergehende Speicherung hingewiesen.

## Dateien und Wiederaufbau

- `_quellen/einfach_tag12.py`: vollständige redaktionelle Begleitung mit Originalfoliennummern, Beispielen, Antworten und Korrekturen.
- `_quellen/lerntraining.py`: gemeinsame Daten und HTML des Trainings; Profilfälle. Neue Trainingsfragen brauchen stabile Inhaltskennungen.
- `_quellen/plattform.py`: Einbindung und Seitenaufbau.
- `plattform/public/assets/lerntraining-core.js`: Terminlogik, separat testbar.
- `plattform/public/assets/lerntraining.js` und `.css`: Bedienung und Darstellung; diese Assets werden vom Generator nicht überschrieben.
- `plattform/public/assets/kurs.js`: Reiter, zugängliche Zuordnung, Tastatur, direkte Sprünge in Learnings/Erklärungen und Originalfolien.
- Wiederaufbau: im Ordner `_quellen` `python build.py --web`.
- Terminlogik testen: im Ordner `plattform` `node --test ops/lerntraining.test.cjs`.

Live-Status: nur lokal vorbereitet. Keine Veröffentlichung ohne den vereinbarten Freigabeschritt.

## Aktualisierung: Live-Stand und Demo-Werkstatt

Am 14.10.2026 hat Chris die Veröffentlichung der bisherigen Änderungen ausdrücklich beauftragt. Tag 12, vollständige Erklärungen, Erinnerungsrunden und Fallwerkstatt sind jetzt live. Die folgende neue Demo-Werkstatt ist separat lokal vorbereitet:

- **Prompt-Studio an allen Tagen:** Vier Bausteine eines Auftrags an- und ausschalten, vorbereitete Antwort vergleichen, Prompt kopieren und Lernnotiz herunterladen. Die Beispiele unterscheiden sich nach Person.
- **Einsatz-Labor an Tag 12:** Vier vollständig beschriebene fiktive Einsätze. Vermutung abgeben; Rolle, Daten und Zweck voneinander unterscheiden. Kein Klassifikator für beliebige echte Systeme.
- **Website-Werkstatt an Tag 12:** Hinweistext und Zeitpunkt ändern, feste Besucherfrage in einer fiktiven Chat-Oberfläche absenden, Wirkung prüfen.
- **Assistenz-Teststand an Tag 12:** Vier Arbeitsregeln zusammenstellen und drei feste Tests durchspielen. Schlechte Antworten sind ausdrücklich markierte Gegenbeispiele. Das Ergebnis zeigt die regelbasierte Simulation, nicht die Zuverlässigkeit eines echten Sprachmodells.

Vorbereitete Antworten immer deutlich als Simulation kennzeichnen. Die Demos rufen keine externe KI auf und richten nichts in Langdock ein. Die Übung kann ohne Agent-Zugang genutzt werden. Ein Erfolg heißt nur „Aufgabe einmal gelöst“, nicht bestanden, zertifiziert oder rechtlich freigegeben.

Code: `_quellen/demowerkstatt.py`, Assets `demo-core.js`, `demos.js`, `demos.css`. Speicherung getrennt unter `kurs:demos:v1:<person>:t<tag>`; alte Lernstände nicht umschreiben. Tests: `node --test ops/demos.test.cjs ops/lerntraining.test.cjs`.


## Demo-Werkstatt live – 14.10.2026

Auf ausdrücklichen Wunsch von Chris sind jetzt auch die vier Demo-Umgebungen veröffentlicht: Prompt-Studio, Einsatz-Labor, Website-Werkstatt und Assistenz-Teststand. Das Prompt-Studio steht an allen zwölf Tagen bereit, alle vier Demos an Tag 12, jeweils für Ingo, Tabea und Carmen.

Release: `20261014-demos`. 48 geänderte öffentliche Dateien wurden nach Prüfung des Ausgangsstands übertragen. Alle 48 über HTTPS ausgelieferten Dateien stimmen per SHA-256 mit dem geprüften Paket überein. Container gesund; Prompt-Interaktion und Website-Hinweisprüfung direkt live getestet, keine Browserfehler.

Backup: `/opt/stacks/langdock-hefte/releases/20261014-demos/public-before.tar.gz`. Vorheriges Image: `langdock-hefte:pre-20261014-demos`; neues Image: `langdock-hefte:release-20261014-demos`. Bestehender Servercode, Konfiguration und Teilnehmerdaten wurden beibehalten. Frühere Hinweise auf einen ausschließlich lokalen Demo-Stand sind damit überholt.

Live: https://quint-games.de/hefte/tabea/tag-12/#demos


### Tag 13: Datenschutz-Werkstatt
Drei kurze Missionen verbinden Erkennen, Ausprobieren und Entscheiden. Fehlversuche erklären die falsche Annahme; Erfolg wird als einmal gelöst markiert, nicht als Rechtsfreigabe. Die Werkstatt übt ausgewählte Gedanken, die begleitenden 74 Einzelabschnitte erhalten die vollständige Lektion. Eigene Merksätze und zeitversetzte Erinnerungsfragen unterstützen den Transfer. Alle Angaben sind erfunden; die Simulation benötigt weder Agent-Zugang noch echte Personendaten.


### Tag 14: Agenten-Cockpit
Acht Folien vollständig begleitet. Spurensuche trennt frühe Ursache, spätere Folge und längsten Schritt. Vergleichslabor hält Qualitätskriterien vor dem Versuch fest; eine schnellere falsche Antwort kann nicht gewinnen. Signal-Check erklärt jede Zuordnung und erlaubt neue Versuche. Alle drei Missionen nutzen vorbereitete Daten, auch ohne Agent-Zugang. Manuelle Selbsterklärung und acht Erinnerungsfragen ergänzen die Simulation.


### Tag 16–18: Fortlaufende Werkstattreihe
20.–22.10.2026: Erst einen prüfbaren Dateiauftrag bearbeiten, dann eine begrenzte MCP-Leseprobe, zuletzt einen wiederverwendbaren Ablauf am neuen Fall prüfen. Jede Person erhält eine eigene Branchen-Mission; ohne zusätzlichen Zugang bleibt eine ausdrücklich als Datei-/Chatübung bezeichnete Alternative. Anfänger lernen Quelle, Annahme, tatsächliche Aktion und Ergebnis auseinanderzuhalten. Alle 27 Folien einschließlich optionaler Verweise sind über die Reihe begleitet. Die drei Browser-Labore bleiben ausdrücklich vorbereitete Simulationen; ein Haken bestätigt keine echte Produktanbindung. Materialien sind lokal vorbereitet; noch nicht live.


## Veröffentlichung 20.10.2026 · Lernreihe Tag 16–18

Auf ausdrücklichen Auftrag alle neuen Lernhefte und Materialien für den 20.–22.10.2026
veröffentlicht (Release `20261020-werkstattreihe`) und für das öffentliche GitHub-Repository
https://github.com/christiansowi-ux/langdock-schulung übernommen.

269 öffentliche Dateien aktualisiert; 268 per HTTPS bytegenau geprüft, internes Manifest
auf Host und im Container geprüft. Alle neun Kombinationen aus Person und Tag bestehen den
Live-Browsertest (Quiz, Kopieren, Simulation, 390px und Lernkarten), ohne beobachtete JS-Fehler.
Container gesund; bestehende Serverdateien, Zugangsdaten und Laufzeitdaten unverändert.
Vorherige Dateien und Docker-Image sind unter dem Release auf dem Server gesichert.

Die frühere Angabe „nur lokal“ zur Reihe ist damit überholt. Details zu Inhalten und
vorherigen vollständigen lokalen Prüfungen: `_quellen/reihe1618/README.md`.


## Tag 19 live · 23.10.2026

Auf ausdrücklichen Auftrag Freitagsheft und Bonusheft veröffentlicht: Release `20261023-freitag-design`. Alle drei Teilnehmerzugänge, Originalfolien und PDF-Downloads sind erreichbar. 121 öffentliche Dateien per HTTPS bytegenau geprüft; internes Manifest im Container und alle 122 Zieldateien auf dem Host geprüft. Neun Seiten im Live-Browser geprüft, sechs Kopieraktionen erfolgreich, keine beobachteten JS-Fehler. Make bleibt reine Vorbereitung ohne Übungen. Container gesund; Serverkonfiguration und Laufzeitdaten beibehalten. Vorheriger Stand gesichert. Frühere Angabe „nur lokal“ für Tag 19 ist damit überholt.


## Modul 2 · KI-Automation · Lektion 1 · live am 26.10.2026

Neues Modul separat in Start- und Teilnehmerübersichten angelegt; bisherige 19 Tage bleiben unter Modul 1. Kanonischer Pfad `/hefte/{person}/modul-2/tag-1/`, interne Kompatibilitätskennung Tag 20. 41-seitiges Lernheft, vier kleine manuelle Make-Free-Workflows, Testmaterial und 30 Ausbauideen. Make mit 1.000 Credits verständlich erklärt; KI-/Microsoft-/CRM-Voraussetzungen aus den Folien getrennt eingeordnet. Keine KI-API erforderlich für die ersten Übungen; Creditwerte sind Planwerte und keine gemessenen Kontoläufe. Details in `_quellen/modul2/tag1/README.md`.

Release `20261026-modul2-start`: 192 öffentliche Dateien per HTTPS bytegenau geprüft, internes Manifest im Container und alle 193 Zieldateien auf dem Host geprüft. Zehn Live-Seiten für Ingo, Carmen und Tabea einschließlich Modulübersichten, Lernheft, Kopieren, Quiz, Budget und JSON-Lernhilfe geprüft; keine beobachteten JS-/Konsolenfehler. Container gesund, Serverdateien unverändert, vorheriger Stand und Image gesichert. Alle Arbeiten ohne Subagents.


## Korrektur Modul 2 · 26.–29.10.2026 · vier Tage

Die frühere Zusammenfassung aller 34 Folien und vier Workflows in einem 41-seitigen Montag-Heft ist ersetzt. Eine gemeinsame Folienlektion läuft jetzt Montag bis Donnerstag mit vier eigenen Heften (19/15/17/15 Seiten), je einem Hauptworkflow, vier Quizfragen und passenden Testpaketen. 30 Ideen verteilt: 8/8/7/7. Alle 34 Folien genau einmal zugeordnet. Tagesnotizen sind getrennt; Montag behält den bisherigen Speicherschlüssel. Tag 2–4 sind als Vorschau verfügbar. 50 Credits Unterrichtsbudget gelten für die gesamte Reihe. Vollständige Verteilung und Grenzen: `_quellen/modul2/tag1/README.md`. Lokale QA: 51 Seiten, 2.058 Links, 33 Kopieraktionen, 144 Quizpfade, 15 JSON-Fälle, zwölf Teilnehmer-/Tageskombinationen ohne beobachtete JS-Fehler.


## Regel ab 30.10.2026: jedes Modul ist ein Learning Hub

Chris: „Die Lernkarten bitte auch immer einbauen in das neue Modul, alle Funktionen von davor wieder rein, wie ein Learning Hub.“ Neue Module und Wochen bekommen deshalb immer: Learnings mit Sitzt/Unklar, Lernkarten, Selbsttest, Trainieren (1/3/7 Tage), Aufgabengenerator, Folien-Viewer, Wörter und Lernheft – technisch über einen regulären `kurs.TAGE`-Eintrag (Vorbild: Tag 24, `_quellen/modul2/woche1/`). Vereinfachen heißt Bedienung vereinfachen, nie Funktionen weglassen.
