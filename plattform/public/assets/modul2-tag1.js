'use strict';
(() => {
 for(const button of document.querySelectorAll('[data-copy]'))button.addEventListener('click',async()=>{
  const status=button.parentElement.querySelector('.copystatus');
  try{await navigator.clipboard.writeText(document.getElementById(button.dataset.copy).textContent);status.textContent='Kopiert. In das bezeichnete Feld oder passende Werkzeug einfügen.';}
  catch(_){status.textContent='Kopieren gesperrt. Text bitte markieren und manuell kopieren.';}
 });
 const data=document.getElementById('quiz-data');
 if(data&&!document.querySelector('[data-quiz-persist]')){const quiz=JSON.parse(data.textContent);for(const field of document.querySelectorAll('[data-q]'))field.querySelector('[data-answer]').addEventListener('click',()=>{
  const out=field.querySelector('.feedback'),choice=field.querySelector('input:checked');out.hidden=false;
  if(!choice){out.textContent='Wähle zuerst eine Antwort. Du darfst neu versuchen.';return;}
  const row=quiz[Number(field.dataset.q)-1],ok=Number(choice.value)===row.right;out.classList.toggle('retry',!ok);out.textContent=(ok?'Passt. ':'Noch einmal überlegen: ')+row.why;
 });}
 const calc=document.getElementById('credit-calculate');
 if(calc){calc.addEventListener('click',()=>{
  const m=Number(document.getElementById('credit-modules').value),r=Number(document.getElementById('credit-runs').value),out=document.getElementById('credit-result');
  if(!Number.isInteger(m)||!Number.isInteger(r)||m<1||m>20||r<1||r>10000){out.textContent='Bitte ganze Zahlen eingeben: 1 bis 20 Bausteine und 1 bis 10.000 Starts.';return;}
  const total=m*r;out.textContent=m+' Bausteine × '+r+' Starts = '+total.toLocaleString('de-DE')+' Credits. Das ist unser Rechenbeispiel, keine Messung deines Kontos. '+(total>1000?'Das wäre mehr als dein gesamtes Monatsguthaben von 1.000 Credits.':'Wenn du noch alle 1.000 Credits hättest, blieben rechnerisch '+(1000-total).toLocaleString('de-DE')+' übrig.')+' Deinen echten Restverbrauch prüfst du direkt in Make.';
 });document.getElementById('polling-example').addEventListener('click',()=>{document.getElementById('polling-result').textContent='Eine Abfrage je 15 Minuten: 4 × 24 × 30 = 2.880 Abfragen in 30 Tagen. Bei 1 Credit je Abfrage sind das 2.880 Credits, noch ohne Folgeschritte. Nur ein Rechenbeispiel; kein Zeitplan aktiviert.';});}
 const check=document.getElementById('json-check');
 if(check)check.addEventListener('click',()=>{
  const status=document.getElementById('json-result'),output=document.getElementById('json-output');output.textContent='';let value;
  try{value=JSON.parse(document.getElementById('json-input').value);}catch(_){status.textContent='Kein gültiges JSON. Prüfe doppelte Anführungszeichen, Kommas und Klammern.';return;}
  if(!value||typeof value!=='object'||Array.isArray(value)){status.textContent='Für diese Übung wird ein einzelnes Objekt mit projekt, kategorie und freigabe benötigt.';return;}
  if(typeof value.projekt!=='string'||!value.projekt.trim()||typeof value.kategorie!=='string'||!['VIDEO','MARKETING','SONSTIGES'].includes(value.kategorie)||typeof value.freigabe!=='boolean'){
   status.textContent='Felder prüfen: projekt als nichtleerer Text, kategorie als VIDEO, MARKETING oder SONSTIGES, freigabe als echtes true oder false ohne Anführungszeichen.';return;
  }
  const pass=value.kategorie==='VIDEO'&&value.freigabe===true;
  status.textContent='Die drei Übungsfelder passen zum erwarteten Format. Filter: '+(pass?'würde passieren.':'würde stoppen.')+' Das ist nur die Browser-Lernhilfe, kein Make-Lauf und keine fachliche Freigabe.';
  output.textContent='Projekt: '+value.projekt+'\nKategorie: '+value.kategorie+'\nFreigabe: '+value.freigabe;
 });
 const memo=document.getElementById('memo');
 if(memo){const status=document.getElementById('note-status'),day=Number(document.documentElement.dataset.courseDay||1),key='kurs:modul2:lektion1:'+document.documentElement.dataset.person+(day===1?'':':tag'+day);
  try{memo.value=localStorage.getItem(key)||'';}catch(_){status.textContent='Speicherung nicht verfügbar. Die Text-Mitnahme funktioniert trotzdem.';}
  document.getElementById('save-note').addEventListener('click',()=>{try{localStorage.setItem(key,memo.value);status.textContent='Nur auf diesem Gerät in diesem Browser gespeichert.';}catch(_){status.textContent='Nicht gespeichert. Bitte als Text mitnehmen.';}});
  document.getElementById('download-note').addEventListener('click',()=>{const url=URL.createObjectURL(new Blob(['Modul 2 · Lektion 1 · Tag '+day+' · Mein Test\n\n'+memo.value],{type:'text/plain;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='Modul2-Lektion1-Tag'+day+'-Mein-Test.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),10000);});
 }
 if(matchMedia('(max-width:950px)').matches){const menu=document.querySelector('nav details');if(menu)menu.open=false;}
})();
