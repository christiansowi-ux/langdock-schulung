'use strict';
(() => {
 const quiz=JSON.parse(document.getElementById('quiz-data').textContent);
 const day=Number(document.documentElement.dataset.tag);
 for(const field of document.querySelectorAll('[data-q]')){
  field.querySelector('[data-answer]').addEventListener('click',()=>{
   const chosen=field.querySelector('input:checked'),out=field.querySelector('.feedback');out.hidden=false;
   if(!chosen){out.textContent='Wähle zuerst eine Antwort. Du darfst neu versuchen.';out.classList.add('retry');return;}
   const row=quiz[Number(field.dataset.q)-1],ok=Number(chosen.value)===row.right;
   out.classList.toggle('retry',!ok);out.textContent=(ok?'Passt. ':'Noch einmal überlegen: ')+row.why;
  });
 }
 for(const button of document.querySelectorAll('[data-copy]'))button.addEventListener('click',async()=>{
  const text=document.getElementById(button.dataset.copy).textContent,status=button.parentElement.querySelector('.copystatus');
  try{await navigator.clipboard.writeText(text);status.textContent='Kopiert. In die passende Oberfläche einfügen.';}
  catch(_){status.textContent='Kopieren hier gesperrt: Text markieren und manuell kopieren.';}
 });
 for(const lab of document.querySelectorAll('.lab'))lab.querySelector('[data-lab-check]').addEventListener('click',()=>{
  const signals=[...lab.querySelectorAll('[data-signal]')].map(x=>x.checked),out=lab.querySelector('.lab-result');
  const hints={16:['Ohne benannte Quelle und Zeitraum bleibt der Auftrag unklar.','Fehlende Angaben dürfen nicht als vollständig erscheinen.','Ohne Prüffälle bleibt das Ergebnis ungeprüft.'],17:['Ein Konfigurationseintrag allein belegt noch kein benutzbares Tool.','Verbindung bedeutet nicht automatisch Zugriff auf das Testobjekt.','Ohne tatsächlichen Aufruf ist keine MCP-Nutzung belegt.'],18:['Alte Erinnerungen ersetzen die neue Datei nicht.','Eine Nullbasis darf keine erfundene Prozentzahl erzeugen.','Die Übergabe muss für jemand anderen nachvollziehbar sein.']};
  const missing=signals.map((v,i)=>v?'':hints[day][i]).filter(Boolean);out.classList.toggle('retry',missing.length>0);
  out.textContent=missing.length?missing.join(' '):'Alle drei Lern-Prüfpunkte gewählt. Das ist nur das Ergebnis dieser vorbereiteten Simulation; kein Beleg für einen echten KI-Lauf oder eine Verbindung.';
 });
 const memo=document.getElementById('memo'),status=document.getElementById('note-status'),key='kurs:werkstattreihe:v1:'+document.documentElement.dataset.person+':t'+day;
 try{memo.value=localStorage.getItem(key)||'';}catch(_){status.textContent='Speicherung nicht verfügbar. Die Text-Mitnahme funktioniert trotzdem.';}
 document.getElementById('save-note').addEventListener('click',()=>{try{localStorage.setItem(key,memo.value);status.textContent='Auf diesem Gerät in diesem Browser gespeichert.';}catch(_){status.textContent='Nicht gespeichert. Bitte als Text mitnehmen.';}});
 document.getElementById('download-note').addEventListener('click',()=>{const url=URL.createObjectURL(new Blob(['Tag '+day+' · Werkstattreihe\n\n'+memo.value],{type:'text/plain;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='Tag'+day+'-Meine-Uebergabe.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),10000);});
 if(matchMedia('(max-width:950px)').matches)document.querySelector('nav details').open=false;
})();
