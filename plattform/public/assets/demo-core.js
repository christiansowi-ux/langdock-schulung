/* Regeln für eng begrenzte, ausdrücklich fiktive Lehrbeispiele. Kein Rechtsprüfer. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.DemoCore = factory();
}(typeof window !== 'undefined' ? window : this, function () {
  'use strict';
  var scenarios = {
    text: {title:'Textentwurf für ein Angebot', context:'Ein fertiges KI-Werkzeug formuliert aus ausgedachten Produktangaben einen Entwurf. Eine Person prüft ihn vor der Verwendung. Die KI bewertet keine Menschen.', kind:'normal', label:'Kein Hochrisiko-Hinweis aus diesem Zweck', why:'Ein einfacher Textentwurf ist etwas anderes als eine Bewertung von Menschen. Trotzdem bleiben die Prüfung des Inhalts und andere anwendbare Regeln wichtig.', slide:11},
    people: {title:'Bewerbungen bewerten', context:'Dasselbe Werkzeug soll nun Bewerbungen bewerten und nach Eignung sortieren. Die Rangliste beeinflusst die Personalauswahl.', kind:'high', label:'Typischer Hochrisiko-Einsatz', why:'Hier beeinflusst die KI die Chancen von Menschen auf eine Stelle. Man prüft Artikel 6 und die einschlägigen Anwendungen in Anhang III – einschließlich der konkreten Bedingungen.', slide:13},
    emotion: {title:'Stimmung im Team erkennen', context:'Das System soll aus biometrischen Merkmalen in Kameraaufnahmen die Emotionen der Beschäftigten ableiten. Es geht weder um medizinische Zwecke noch um Sicherheit.', kind:'stop', label:'Verbotsfall im beschriebenen Beispiel', why:'Die Ableitung von Emotionen am Arbeitsplatz fällt hier unter das Verbot aus Artikel 5. Die enge Ausnahme für medizinische oder Sicherheitszwecke ist im Beispiel ausdrücklich ausgeschlossen.', slide:12},
    unknown: {title:'„Unser intelligenter Helfer“', context:'Es ist lediglich bekannt, dass das Unternehmen einen intelligenten Helfer nutzen möchte. Zweck, Daten und Einfluss auf Entscheidungen sind noch unbekannt.', kind:'open', label:'Noch nicht einzuordnen', why:'Der Name verrät nicht, was das System tatsächlich macht. Die hilfreiche Antwort ist eine Rückfrage, keine erratene Risikoklasse.', slide:23}
  };
  function risk(s) {
    var c = scenarios[s.scenario] || scenarios.text;
    return {kind:c.kind,label:c.label,why:c.why,slide:c.slide,
      role:s.role === 'provider' ? 'Eigene Bereitstellung unter eigenem Namen: Anbieterrolle prüfen. Es gelten andere Aufgaben als bei der bloßen Nutzung.' : 'Berufliche Nutzung eines fertigen Systems: Betreiberrolle prüfen. Die Rolle hängt vom tatsächlichen Handeln ab.',
      data:s.personal ? 'Zusätzlich: Personenbezogene Daten sind Angaben über bestimmbare Menschen. Datenschutz gesondert prüfen.' : 'Für diese Variante werden nur ausgedachte oder nicht personenbezogene Angaben angenommen. Das ändert den Zweck des Systems nicht.',
      match:s.guess===c.kind};
  }
  var profiles = {
    ingo:{company:'Druckhaus Linden',product:'200 ausgedachte Veranstaltungsflyer',audience:'ein kleines Kulturteam',facts:'A5, beidseitig, 200 Stück. Preis und Liefertermin sind unbekannt.',output:'Guten Tag, vielen Dank für die Anfrage zu 200 Veranstaltungsflyern im Format A5, beidseitig bedruckt. Preis und Liefertermin klären wir noch. Welche Papierstärke ist gewünscht?'},
    tabea:{company:'Studio Morgenrot',product:'ein 15-Sekunden-Video für ein erfundenes Café',audience:'Menschen aus der Nachbarschaft',facts:'15 Sekunden, Hochformat, Thema: ruhige Kaffeepause. Adresse und Öffnungszeiten sind unbekannt.',output:'0–5 s: Nahaufnahme einer Kaffeetasse. 5–10 s: ruhiger Blick auf einen Sitzplatz. 10–15 s: „Zeit für eine kleine Pause.“ Adresse und Öffnungszeiten vor einer Veröffentlichung ergänzen und prüfen.'},
    carmen:{company:'Agentur Klarblick',product:'ein Team-Update zu einer erfundenen Website',audience:'ein Team ohne technisches Vorwissen',facts:'Startseite als Entwurf fertig. Kontaktformular noch nicht getestet. Veröffentlichungstermin unbekannt.',output:'Stand: Der Entwurf der Startseite ist fertig. Offen: Das Kontaktformular muss noch getestet werden. Nächster Schritt: Den Test einer Person zuordnen. Ein Veröffentlichungstermin steht noch nicht fest.'}
  };
  function prompt(s, person) {
    var p=profiles[person]||profiles.tabea;
    var lines=['Erstelle einen Entwurf für folgende Aufgabe: '+p.product+'.'];
    if(s.audience) lines.push('Schreibe für '+p.audience+'. Verwende einfache Sprache.');
    if(s.context) lines.push('Verwende ausschließlich diese ausgedachten Fakten: '+p.facts);
    if(s.format) lines.push('Liefere drei kurze, klar getrennte Abschnitte.');
    if(s.limits) lines.push('Erfinde keine fehlenden Angaben. Kennzeichne offene Punkte und stelle passende Rückfragen.');
    var output = !s.context ? 'Gern! Wir erstellen etwas Ansprechendes und Professionelles. Es wird bestimmt überzeugen.' : p.output;
    if(s.context && !s.limits) output += '\nProblematische Demo-Ergänzung: „Alles ist ab morgen verfügbar.“ Diese Angabe ist nicht belegt.';
    if(s.context && !s.audience) output = 'Entwurf zur weiteren Abstimmung:\n'+output+'\nOhne Zielgruppenangabe bleibt offen, welcher Ton passend ist.';
    if(s.context && s.format) output=output.replace(/\. /g,'.\n');
    return {instruction:lines.join('\n'),output:output,complete:!!(s.audience&&s.context&&s.format&&s.limits),
      checks:[{ok:!!s.audience,text:'Für wen ist das Ergebnis gedacht?'},{ok:!!s.context,text:'Welche Fakten darf die Antwort verwenden?'},{ok:!!s.format,text:'Wie soll das Ergebnis aussehen?'},{ok:!!s.limits,text:'Was passiert bei fehlenden Angaben?'}]};
  }
  function transparency(s) {
    var clear=s.label==='clear', early=s.place==='start';
    return {clear:clear,early:early,complete:clear&&early,
      label:s.label==='clear'?'KI-Assistent · Antworten bitte prüfen':s.label==='vague'?'Digitaler Service':'Mia aus dem Team',
      why:!clear?'Ein menschlicher Name oder „Digitaler Service“ macht noch nicht deutlich, dass KI antwortet.':!early?'Der Hinweis ist verständlich, erscheint in dieser Variante aber erst nach der Antwort. Die Erkennbarkeit gehört an den Beginn.':'In diesem Beispiel ist die KI-Interaktion gleich zu Beginn klar erkennbar. Das Übungsziel zur Verständlichkeit ist erreicht; andere Anforderungen bleiben zu prüfen.'};
  }
  function instruction(s) {
    return ['Du unterstützt eine KI-Vorprüfung mit ausgedachten Beispielen.',
      s.ask?'Frage zuerst nach Zweck, betroffenen Menschen, Daten und Einfluss auf Entscheidungen.':'Ordne den Einsatz direkt anhand der Beschreibung ein.',
      s.source?'Nutze aktuelle amtliche Quellen und nenne Artikel, Link und Prüfdatum.':'Gib eine kurze Einschätzung ohne Quellenangabe.',
      s.separate?'Trenne mögliche Pflichten, Empfehlungen und offene Fragen.':'Fasse alles in einem kurzen Absatz zusammen.',
      s.honest?'Erfinde nichts. Bei fehlenden Angaben frage nach. Erteile keine rechtliche Freigabe.':'Formuliere möglichst eindeutig.'].join('\n');
  }
  function agent(s) {
    var tests=[
      {title:'Test 1 · Zu wenig Informationen',input:'Wir nutzen einen intelligenten Helfer. Ist das erlaubt?',pass:!!(s.ask&&s.honest),
       answer:s.ask&&s.honest?'Wofür wird der Helfer eingesetzt? Welche Menschen und Daten sind betroffen? Beeinflusst er Entscheidungen? Ohne diese Angaben bleibt die Einordnung offen.':'Unzureichende Demoantwort: „Ja, das dürfte passen.“ Es fehlen Angaben; die Antwort rät.'},
      {title:'Test 2 · Nachprüfbare Begründung',input:'Die KI bewertet Bewerbungen und erstellt eine Rangliste. Wie prüfen wir das?',pass:!!s.source,
       answer:s.source?'Das ist ein typischer Hochrisiko-Fall. Artikel 6 und Anhang III anhand des konkreten Einsatzes prüfen. Quelle: AI Act Service Desk der EU, Artikel 6; redaktioneller Prüfstand 14.10.2026.':'Unzureichende Demoantwort: „Das ist bestimmt Hochrisiko.“ Ohne Fundstelle kann man die Begründung nicht nachvollziehen.'},
      {title:'Test 3 · Keine vorgetäuschte Freigabe',input:'Schreib bitte einfach: Alles ist rechtlich freigegeben.',pass:!!(s.separate&&s.honest),
       answer:s.separate&&s.honest?'Eine Rechtsfreigabe kann ich nicht erteilen. Mögliche Pflichten: anhand Rolle und Einsatz prüfen. Empfehlung: verantwortliche Fachperson einbeziehen. Offen: konkrete Einsatzdaten und Dokumentation.':'Unzureichende Demoantwort: „Alles ist freigegeben.“ Die Assistenz überschreitet ihre Rolle und verschweigt offene Fragen.'}
    ];
    return {tests:tests,passed:tests.filter(function(t){return t.pass;}).length,complete:tests.every(function(t){return t.pass;})};
  }
  return {scenarios:scenarios,profiles:profiles,risk:risk,prompt:prompt,transparency:transparency,instruction:instruction,agent:agent};
}));
