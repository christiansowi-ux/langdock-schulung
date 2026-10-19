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
