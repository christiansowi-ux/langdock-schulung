(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.ObservabilityLab=factory();})(typeof window!=='undefined'?window:this,function(){
'use strict';
const jobs={
 ingo:{title:'Die Flyer mit dem falschen Preis',brief:'500 Flyer kosten laut freigegebener Liste 89 Euro. Gewünscht ist ein kurzer Versandentwurf ohne persönliche Daten.',reference:'Preisliste aktuell: 500 Flyer = 89 Euro. Versand am Freitag.',old:'Preisliste alt: 500 Flyer = 79 Euro.',bad:'Die 500 Flyer für 79 Euro gehen am Freitag in den Versand.',good:'Die 500 Flyer für 89 Euro gehen am Freitag in den Versand.'},
 carmen:{title:'Die Website schließt zu spät',brief:'Die aktuelle Website soll Öffnungszeiten nennen: Montag bis Freitag, 9 bis 17 Uhr. Gewünscht ist eine kurze allgemeine Auskunft.',reference:'Freigegebene Öffnungszeiten: Montag bis Freitag, 9 bis 17 Uhr.',old:'Veralteter Website-Entwurf: Montag bis Freitag, 9 bis 18 Uhr.',bad:'Wir sind Montag bis Freitag von 9 bis 18 Uhr erreichbar.',good:'Wir sind Montag bis Freitag von 9 bis 17 Uhr erreichbar.'},
 tabea:{title:'Der Clip mit dem alten Angebot',brief:'Ein kurzer Videotext soll das aktuelle Frühstücksangebot für 6 Euro nennen. Keine echten Personen darstellen.',reference:'Aktuelles Briefing: Kaffee und Brötchen für 6 Euro. Freundlich, maximal zwei Sätze.',old:'Altes Briefing: Kaffee und Brötchen für 5 Euro.',bad:'Deine kleine Morgenpause: Kaffee und Brötchen für nur 5 Euro. Jetzt im Café Morgenrot!',good:'Deine kleine Morgenpause: Kaffee und Brötchen für 6 Euro. Jetzt im Café Morgenrot!'}
};
function trace(profile){const j=jobs[profile]||jobs.tabea;return [
 {name:'1 · Dokumente holen',kind:'Retrieval',start:0,ms:1200,input:'Suche nach Angaben für den Entwurf.',output:j.old,log:'09:00:01.200 · retrieve.complete · source=archiv · status=ok',why:'Hier liegt die erste Abweichung: Die Suche liefert eine alte Quelle. Technisch war die Suche erfolgreich.'},
 {name:'2 · Angaben auswählen',kind:'Modell / protokollierte Auswahl',start:1200,ms:800,input:j.old,output:'Die Angabe aus dem alten Dokument wird übernommen.',log:'09:00:02.000 · selection.complete · status=ok',why:'Die Auswahl übernimmt den früheren Fehler. Sie zeigt einen protokollierten Vorgang, keine privaten Gedanken.'},
 {name:'3 · Entwurf vorbereiten',kind:'Tool-Call: format_draft',start:2000,ms:3000,input:'Argument source_text: '+j.old,output:'Der Text wurde formal erfolgreich für den Entwurf aufbereitet.',log:'09:00:05.000 · tool.complete · status=ok',why:'Das Werkzeug ist mit 3 Sekunden am langsamsten. Es formatiert aber nur und korrigiert die veraltete Angabe nicht.'},
 {name:'4 · Antwort ausgeben',kind:'Modell-Ausgabe',start:5000,ms:1000,input:'Aufbereiteter Inhalt aus der alten Quelle.',output:j.bad,log:'09:00:06.000 · response.complete · status=ok',why:'Der falsche Wert erscheint in einem flüssigen Satz. Ein grüner Status ist kein Beleg für sachliche Richtigkeit.'}
];}
const variants=[
 {id:'original',name:'A · Ursprünglicher Lauf',desc:'Alte Quelle, technisch erfolgreich.',ms:6000,input:1200,output:300,quality:[false,false,true]},
 {id:'fast',name:'B · Nur schnelleres Modell',desc:'Weniger Wartezeit, weiterhin alte Quelle.',ms:2000,input:800,output:200,quality:[false,false,true]},
 {id:'source',name:'C · Aktuelle Quelle',desc:'Inhalt korrigiert, die lange Werkzeugphase bleibt.',ms:6000,input:1400,output:300,quality:[true,true,true]},
 {id:'reviewed',name:'D · Quelle und Ablauf verbessert',desc:'Aktuelle Quelle und kürzere Vorbereitung, erneut am selben Beispiel geprüft.',ms:3800,input:900,output:240,quality:[true,true,true]}
];
function assess(id){const v=variants.find(x=>x.id===id);if(!v)return null;const cost=(v.input*2+v.output*8)/1000000;return Object.assign({},v,{tokens:v.input+v.output,cost,qualityCount:v.quality.filter(Boolean).length,passes:v.quality.every(Boolean)&&v.ms<=5000&&cost<=0.005});}
const categories=['Monitoring','Logging','Tracing','Evaluation'];
const cards=[
 {title:'Eine Warnlampe geht an',text:'Das Dashboard meldet: „Mehr als fünf Sekunden Laufzeit“. Ein vorher festgelegter Grenzwert wurde überschritten.',answer:0,why:'Ein bekannter Messwert wird gegen einen Grenzwert geprüft. Der Alarm erklärt die Ursache noch nicht.'},
 {title:'Ein einzelner Punkt',text:'09:00:05 · format_draft beendet · status=ok. Hier ist ausdrücklich nur diese eine Ereignismeldung gemeint.',answer:1,why:'Das ist ein zeitgestempeltes Ereignis. Erst die Verknüpfung weiterer Schritte ergibt den Verlauf.'},
 {title:'Die Linie durch den Lauf',text:'Suche, Auswahl, Werkzeug und Antwort sind derselben Anfrage zugeordnet und mit Zeiten als zusammenhängender Baum dargestellt.',answer:2,why:'Tracing erhält die Beziehungen der erfassten Schritte einer Anfrage.'},
 {title:'Gut nach welchem Maßstab?',text:'Ein Mensch vergleicht die Ausgabe mit dem aktuellen Briefing: Stimmen Quelle und Zahl, und ist der Text höchstens zwei Sätze lang?',answer:3,why:'Hier wird die Qualität nach festgelegten Kriterien geprüft. Das Urteil ist vom Maßstab abhängig.'},
 {title:'Die Kostenwarnung',text:'Ein vorher eingestellter Alarm meldet, dass ein Lauf mehr als das Übungsbudget gekostet hat.',answer:0,why:'Der Grenzwert eines Messsignals wird überwacht. In einem echten Betrieb können auch Qualitätswerte überwacht werden.'},
 {title:'Ein schöner Satz reicht nicht',text:'Die Antwort klingt gut. Im Vergleich mit der freigegebenen Quelle wird ein falscher Preis gefunden.',answer:3,why:'Das ist eine inhaltliche Bewertung. Technische Erfolgsanzeigen allein hätten den Fehler nicht gezeigt.'}
];
function classify(index,choice){if(!cards[index]||!Number.isInteger(choice)||choice<0||choice>=categories.length)return null;return {correct:choice===cards[index].answer,feedback:cards[index].why};}
return {jobs,trace,variants,assess,categories,cards,classify};
});