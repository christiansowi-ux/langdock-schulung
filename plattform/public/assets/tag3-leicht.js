'use strict';
(() => {
 const root=document.querySelector('[data-quiz-persist]'),data=document.getElementById('quiz-data');
 if(!root||!data)return;
 const quiz=JSON.parse(data.textContent),fields=[...document.querySelectorAll('fieldset[data-q]')];
 const key='kurs:modul2:lektion1:'+document.documentElement.dataset.person+':tag3:quiz:v2';
 const status=document.getElementById('quiz-storage-status'),progress=document.getElementById('quiz-progress');
 let rows=quiz.map(()=>({answer:null,checked:false}));
 function feedback(i){
  const field=fields[i],row=rows[i],out=field.querySelector('.feedback');
  if(!row.checked){out.hidden=true;return;}
  const ok=row.answer===quiz[i].right;out.hidden=false;out.classList.toggle('retry',!ok);out.textContent=(ok?'Passt. ':'Noch einmal überlegen: ')+quiz[i].why;
 }
 function summary(){
  const chosen=rows.filter(r=>r.answer!==null).length,checked=rows.filter(r=>r.checked).length,right=rows.filter((r,i)=>r.checked&&r.answer===quiz[i].right).length;
  progress.textContent=chosen+' von '+quiz.length+' beantwortet · '+checked+' geprüft · '+right+' richtig. Du darfst jede Antwort noch ändern.';
 }
 function save(){
  try{localStorage.setItem(key,JSON.stringify({version:2,rows}));status.classList.remove('save-error');status.textContent='Gespeichert auf diesem Gerät in diesem Browser. Nach dem Neuladen kannst du hier weiterlernen.';return true;}
  catch(_){status.classList.add('save-error');status.textContent='Dein Browser erlaubt das Speichern gerade nicht. Deine Auswahl bleibt bis zum Verlassen der Seite sichtbar. Lade den Quizstand als Text herunter.';return false;}
 }
 try{
  const raw=localStorage.getItem(key);
  if(raw){
   const saved=JSON.parse(raw);
   if(saved.version!==2||!Array.isArray(saved.rows)||saved.rows.length!==quiz.length||!saved.rows.every(r=>r&&typeof r.checked==='boolean'&&(r.answer===null||Number.isInteger(r.answer)&&r.answer>=0&&r.answer<3)&&(!r.checked||r.answer!==null)))throw new Error('invalid quiz data');
   rows=saved.rows.map(r=>({answer:r.answer,checked:r.checked}));status.textContent='Dein gespeicherter Quizstand wurde wiederhergestellt. Du kannst weiterlernen.';
  }else{localStorage.setItem(key,JSON.stringify({version:2,rows}));status.textContent='Speicher bereit. Deine Antworten werden automatisch auf diesem Gerät in diesem Browser gespeichert.';}
 }catch(_){status.classList.add('save-error');status.textContent='Ein alter Quizstand konnte nicht geladen werden oder der Browser blockiert den Speicher. Du kannst die Fragen trotzdem beantworten und deinen Stand als Text herunterladen.';}
 fields.forEach((field,i)=>{
  if(rows[i].answer!==null)field.querySelector('input[value="'+rows[i].answer+'"]').checked=true;
  feedback(i);
  field.querySelectorAll('input').forEach(input=>input.addEventListener('change',()=>{rows[i]={answer:Number(input.value),checked:false};feedback(i);summary();save();}));
  field.querySelector('[data-answer]').addEventListener('click',()=>{
   const out=field.querySelector('.feedback');
   if(rows[i].answer===null){out.hidden=false;out.classList.remove('retry');out.textContent='Wähle zuerst eine Antwort. Du darfst neu versuchen.';return;}
   rows[i].checked=true;feedback(i);summary();save();
  });
 });
 document.getElementById('quiz-save').addEventListener('click',save);
 document.getElementById('quiz-download').addEventListener('click',()=>{
  const text=['Modul 2 · Tag 3 · Mein Quizstand',document.documentElement.dataset.person,'',...rows.map((r,i)=>{
   const field=fields[i],question=field.querySelector('legend').textContent,answer=r.answer===null?'Noch keine Auswahl':field.querySelector('input[value="'+r.answer+'"]').parentElement.textContent.trim();
   return question+'\nMeine Antwort: '+answer+'\n'+(r.checked?(r.answer===quiz[i].right?'Richtig. ':'Noch einmal ansehen. ')+quiz[i].why:'Noch nicht geprüft.');
  })].join('\n\n');
  const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='Make-Tag3-'+document.documentElement.dataset.person+'-Quizstand.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),10000);
 });
 function reveal(){let target;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)));}catch(_){return;}if(!target)return;for(let el=target;el;el=el.parentElement)if(el.tagName==='DETAILS')el.open=true;}
 addEventListener('hashchange',reveal);reveal();summary();
})();

(() => {
 const select=document.getElementById('ampel-status'),button=document.getElementById('ampel-test'),out=document.getElementById('ampel-result');
 if(!select||!button||!out)return;
 button.addEventListener('click',()=>{
  const pass=select.value==='FERTIG';out.classList.toggle('retry',!pass);
  out.textContent=pass?'Weiter: FERTIG erfüllt unsere Regel. In Make dürfte jetzt der zweite Baustein laufen.':'Stopp: ENTWURF erfüllt die Regel nicht. In Make würde der zweite Baustein in diesem Lauf nicht ausgeführt.';
 });
})();
