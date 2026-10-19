"""Lokale Demo-Umgebungen; kein externer KI-Aufruf, keine echten Daten."""
import html

def panel(pid, n):
    labs = [('prompt', '01', 'Prompt-Studio', 'Aus einer vagen Bitte wird ein brauchbarer Auftrag.', 'Auftrag → Ergebnis')]
    if n == 12:
        labs += [('einsatz', '02', 'Ein Werkzeug. Vier Einsätze.', 'Den Zweck ändern und die Unterschiede entdecken.', 'Zweck → Prüffragen'),
                 ('hinweis', '03', 'Die Website-Werkstatt', 'Einen KI-Chat aus Sicht der Besucher gestalten.', 'Gestaltung → Wirkung'),
                 ('assistenz', '04', 'Assistenz auf dem Prüfstand', 'Arbeitsregeln bauen und drei Testfälle durchspielen.', 'Regeln → Verhalten')]
    buttons = ''.join(f'<button type="button" class="demo-room" data-room="{key}" aria-pressed="false" aria-controls="demo-stage"><span class="demo-room-no">{no}</span><strong>{title}</strong><span>{desc}</span><small>{flow} <span data-done="{key}"></span></small></button>' for key,no,title,desc,flow in labs)
    return f'''<section class="tpanel wrap" id="demos" role="tabpanel" aria-label="Demos">
      <div class="demo-hero"><div><p class="demo-eyebrow">Die Demo-Werkstatt · selbst ausprobieren</p>
        <h2>Was passiert,<br>wenn man es anders macht?</h2>
        <p>Etwas verändern. Die Wirkung sehen. Den Unterschied verstehen.</p>
        <div class="demo-tags"><span>Ohne Anmeldung</span><span>Ohne echte Daten</span><span>Im eigenen Tempo</span></div></div>
        <div class="demo-hero-sketch" aria-hidden="true"><span>Die eigene Idee</span><i>↓</i><span class="demo-sketch-active">Ausprobieren & verändern</span><i>↓</i><span>Der Aha-Moment</span></div></div>
      <div data-demos data-profile="{html.escape(pid)}" data-day="{n}">
        <p class="demo-save" role="status"></p>
        <div class="demo-rooms" aria-label="Demo auswählen">{buttons}</div>
        <div id="demo-stage" class="demo-stage"></div>
        <noscript><p>Die Demo-Werkstatt braucht JavaScript. Die Learnings und Lernhefte funktionieren weiterhin ohne die Simulation.</p></noscript>
        <p class="demo-bottom">Alles hier ist eine Lernsimulation mit vorbereiteten Beispielen. Es wird kein echtes KI-System eingerichtet, keine Nachricht verschickt und keine Website veröffentlicht. Einstellungen bleiben für die gewählte Person nur in diesem Browser. Die Demos ersetzen weder die vollständigen Folien noch eine konkrete fachliche Prüfung.</p>
      </div></section>'''
