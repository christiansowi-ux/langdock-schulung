"""Aufgabengenerator: kurze Aufgaben für Modul 2 · Tag 7 (interne Kennung 26). Rollenspiele zur Prozessaufnahme.

Platzhalter wie in aufgaben.py ({firma}, {was}, {alltag} …). Alles ausgedacht. Die KI spielt Rollen, damit das Üben Spaß macht.
"""


def muster(M):
    return [
        M('t26-interview', 26, 'Rollenspiel: Die KI ist die schweigsame Kollegin', 10, ['l9', 'l11'],
          'Prozesse werden erzählt. Die Kunst liegt im Nachfragen, und die vier Alarmsätze zeigen dir, wo.',
          'Du arbeitest {alltag} bei {firma}, {was}. Du willst einen Ablauf verstehen, doch die Person erzählt nur das Nötigste.',
          [('Den Prompt in einen neuen Chat schicken:',
            'Spiele eine erfahrene Person bei {firma} ({was}). Ich führe mit dir ein Prozessinterview über einen erfundenen, alltäglichen Ablauf.\n'
            'Regeln für dich: Antworte kurz und freundlich. Sage von dir aus nur das Nötigste. Verwende immer wieder Sätze wie „normalerweise“, „das sieht man dann schon“, „das macht die Kollegin“ und „das ist eigentlich immer gleich“.\n'
            'Details, Regeln und Ausnahmen verrätst du erst, wenn ich gezielt nachfrage.\n'
            'Wenn ich „Auswertung“ schreibe, zeigst du mir: welche Alarmsätze ich überhört habe, was ich herausgefunden habe und was ich noch nicht weiß.\n'
            'Fang an, indem du dich kurz vorstellst.'),
           ('Stell mindestens fünf Rückfragen und schreibe in drei Spalten mit: Handlung, System, Entscheidung.', None),
           ('Schreibe „Auswertung“ und schau, was du überhört hast.', None)],
          'Hast du nach dem letzten echten Fall gefragt? Hast du bei jedem Alarmsatz nachgehakt, ohne dass es nach Vorwurf klang?',
          noch='Spiele es nochmal und frag von Anfang an: „Nimm den letzten Fall von gestern und erzähl mir Schritt für Schritt, was du gemacht hast.“'),
        M('t26-zielsatz', 26, 'Die strenge Prüfstelle für Zielsätze', 5, ['l5', 'l6'],
          'Ein Ziel hat fünf Bausteine: Anteil oder Menge, Fallmenge, Handlung, Kennzahl, Zeitpunkt.',
          'Bei {firma} heißt es: „Wir wollen da irgendwie schneller werden.“ Mach daraus ein Ziel.',
          [('Den Prompt in einen neuen Chat schicken:',
            'Du bist eine freundliche, aber strenge Prüfstelle für Projektziele bei {firma} ({was}).\n'
            'Ein Ziel braucht fünf Bausteine: 1. Anteil oder Menge, 2. abgegrenzte Fallmenge, 3. konkrete Handlung, 4. Kennzahl, 5. Zeitpunkt.\n'
            'Ich schicke dir gleich einen Zielsatz. Sage mir je Baustein: vorhanden oder fehlt. Wenn etwas fehlt, stelle genau eine Rückfrage und gib einen trockenen, witzigen Kommentar dazu.\n'
            'Formuliere den Satz nicht für mich um, bis ich darum bitte.\n'
            'Mein erster Versuch: Wir wollen schneller werden.'),
           ('Verbessere deinen Satz, bis alle fünf Bausteine vorhanden sind.', None),
           ('Probiere den fertigen Satz im Zielsatz-Baukasten der Ermittlungsakte aus.', None)],
          'Könnte in sechs Monaten eine fremde Person eindeutig entscheiden, ob das Ziel erreicht ist?'),
        M('t26-sipoc', 26, 'SIPOC in zehn Minuten', 10, ['l12'],
          'SIPOC legt fest, wo der Prozess anfängt und wo er aufhört.',
          '{firma} will einen Ablauf automatisieren, und niemand weiß genau, wo er endet.',
          [('Den Prompt in einen neuen Chat schicken:',
            'Stelle mir für einen erfundenen Ablauf bei {firma} ({was}) nacheinander genau fünf Fragen, eine pro Nachricht:\n'
            'Woher kommt der Input? Was genau kommt an? Welche fünf bis sieben Hauptschritte gibt es? Was entsteht am Ende? Wer bekommt das Ergebnis?\n'
            'Baue aus meinen Antworten danach eine SIPOC-Tabelle mit den Spalten Lieferant, Input, Prozess, Output, Empfänger.\n'
            'Schreibe darunter: „Der Prozess beginnt hier: …“ und „Der Prozess endet hier: …“.\n'
            'Nenne zum Schluss eine Sache, die jemand gern noch ins Projekt schieben würde und die nach dieser Tabelle nicht dazugehört.'),
           ('Stelle dir einen Timer auf zehn Minuten.', None)],
          'Stehen Anfang und Ende so klar da, dass darüber niemand mehr streiten muss?'),
        M('t26-sop', 26, 'Der Neue-Kollegin-Test', 10, ['l20'],
          'Ein SOP ist so geschrieben, dass eine neue Kollegin ohne Nachfrage arbeiten kann.',
          'Bei {firma} fängt nächste Woche eine neue Person an. Sie soll einen wiederkehrenden Ablauf übernehmen.',
          [('Einen Ablauf aus {alltag} aufschreiben, fünf bis acht Schritte, ohne viel nachzudenken.', None),
           ('Den Prompt mit deinem Ablauf in einen neuen Chat schicken:',
            'Spiele eine neue Person im ersten Arbeitsmonat bei {firma} ({was}). Du bist motiviert, kennst aber keine Abkürzungen, Systeme oder internen Regeln.\n'
            'Lies diese Anleitung und markiere jede Stelle, an der du nachfragen müsstest. Nicht diskutieren, nur markieren.\n'
            'Gib je Markierung aus: Stelle, deine Frage, und ob es eine fehlende Regel oder eine noch nicht erfasste Ausnahme ist.\n'
            'Prüfe auch: Nennt jeder Schritt eine Rolle und ein System? Sind Wartezeiten eigene Schritte?\n'
            'Anleitung: [hier deinen Ablauf einfügen. Nur erfundene oder freigegebene Angaben]'),
           ('Die zwei wichtigsten Markierungen beheben und noch einmal prüfen lassen.', None)],
          'Beginnt jeder Schritt mit der Rolle? Sind die Wartezeiten aufgeschrieben?'),
        M('t26-scope', 26, 'Monat drei: Der Fachbereich will mehr', 10, ['l21'],
          'Die Out-of-Scope-Liste verhindert die Diskussion, die sonst in Monat drei kommt.',
          'Das Projekt bei {firma} läuft, und plötzlich kommen neue Wünsche auf den Tisch.',
          [('Drei Zeilen In Scope und drei Zeilen Out of Scope für einen erfundenen Fall aufschreiben.', None),
           ('Den Prompt mit deinen Listen in einen neuen Chat schicken:',
            'Spiele eine freundliche, sehr hartnäckige Person aus dem Fachbereich von {firma} ({was}). Wir sind in Monat drei eines Automatisierungsprojekts.\n'
            'Versuche nacheinander drei Wünsche ins Projekt zu schieben, die nach meinen Listen nicht dazugehören. Klinge dabei harmlos: „Das ist doch nur eine Kleinigkeit.“\n'
            'Ich antworte jeweils und berufe mich auf den Scope. Am Ende sagst du mir, welche Lücke meine Liste hatte.\n'
            'In Scope: [deine Liste]\nOut of Scope: [deine Liste]\nAlles, was hier nicht ausdrücklich aufgeführt ist, gilt als außerhalb des Umfangs.'),
           ('Die Lücke, die dabei auffällt, in deine Liste aufnehmen.', None)],
          'Konntest du freundlich bleiben und trotzdem bei der Liste? Was fehlte darauf?'),
    ]
