'use strict';
(() => {
 for(const button of document.querySelectorAll('[data-copy]'))button.addEventListener('click',async()=>{
  const text=document.getElementById(button.dataset.copy).textContent,status=button.parentElement.querySelector('.copystatus');
  try{await navigator.clipboard.writeText(text);status.textContent='Kopiert. Im passenden Werkzeug einfügen.';}
  catch(_){status.textContent='Kopieren gesperrt: Bitte Text markieren und manuell kopieren.';}
 });
 if(matchMedia('(max-width:950px)').matches){const menu=document.querySelector('nav details');if(menu)menu.open=false;}
})();
