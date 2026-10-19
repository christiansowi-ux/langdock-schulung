'use strict';
(() => {
  const feedback = JSON.parse(document.getElementById('quiz-data').textContent);
  for (const field of document.querySelectorAll('[data-quiz]')) {
    field.querySelector('[data-answer]').addEventListener('click', () => {
      const selected = field.querySelector('input:checked');
      const status = field.querySelector('.feedback');
      status.hidden = false;
      if (!selected) { status.textContent = 'Wähle erst eine Antwort. Du kannst beliebig oft ausprobieren.'; status.classList.add('retry'); return; }
      const data = feedback[Number(field.dataset.quiz) - 1];
      const right = Number(selected.value) === data.right;
      status.classList.toggle('retry', !right);
      status.textContent = (right ? 'Passt. ' : 'Noch einmal überlegen: ') + data.why;
    });
  }
  for (const button of document.querySelectorAll('[data-copy]')) {
    button.addEventListener('click', async () => {
      const text = document.getElementById(button.dataset.copy).textContent;
      const status = button.parentElement.querySelector('.copystatus');
      try { await navigator.clipboard.writeText(text); status.textContent = 'Auftrag kopiert. In einen neuen Chat einfügen.'; }
      catch (_) { status.textContent = 'Kopieren ist hier gesperrt. Markiere den Auftrag und kopiere ihn manuell.'; }
    });
  }
  const memo = document.getElementById('memo');
  const status = document.getElementById('note-status');
  const key = 'kurs:toolbook:v1:' + document.documentElement.dataset.person + ':t15';
  try { memo.value = localStorage.getItem(key) || ''; }
  catch (_) { status.textContent = 'Speicherung ist nicht verfügbar. Du kannst deine Notiz als Text mitnehmen.'; }
  document.getElementById('save-note').addEventListener('click', () => {
    try { localStorage.setItem(key, memo.value); status.textContent = 'Auf diesem Gerät in diesem Browser gespeichert.'; }
    catch (_) { status.textContent = 'Nicht gespeichert. Bitte nutze die Text-Mitnahme.'; }
  });
  document.getElementById('download-note').addEventListener('click', () => {
    const text = 'Tag 15 · KI-Werkzeuge im Vergleich\n19.10.2026\n\n' + memo.value;
    const url = URL.createObjectURL(new Blob([text], {type: 'text/plain;charset=utf-8'}));
    const a = document.createElement('a'); a.href = url; a.download = 'Tag15-Mein-Merksatz.txt'; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 10000);
  });
  if (window.matchMedia('(max-width:950px)').matches) document.querySelector('nav details').open = false;
})();
