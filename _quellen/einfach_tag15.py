"""Alle Originalfolien in der bestehenden Tagesansicht begleiten."""
from html import escape as E
from tag15.content import SLIDES

def render():
 cards=[]
 for n,title,simple,detail,example,q,a,correction in SLIDES:
  cards.append(f'<article class="simple-slide" id="einfach-{n}"><p class="kicker">Folie {n} von 28</p><h3>{E(title)}</h3><p class="simple-main">{E(simple)}</p><p>{E(detail)}</p><div class="simple-example"><p><b>Ausgedachtes Beispiel:</b> {E(example)}</p></div><div class="simple-check"><p><b>Erst selbst überlegen:</b> {E(q)}</p><details><summary>Eine mögliche Antwort</summary><p>{E(a)}</p></details></div>'+(f'<p class="simple-correction"><b>Präzisierung:</b> {E(correction)}</p>' if correction else '')+f'<p><a href="#folien" data-folie="{n}">Originalfolie {n} ansehen</a> · <a href="lernheft/#k{24+(n-1)//2}">Im Lernheft nachlesen</a></p></article>')
 return '<section class="tpanel wrap" id="einfach" role="tabpanel" aria-label="Einfach erklärt"><div class="panel-head"><div><h2>Alle 28 Folien in verständlichen Worten</h2><p>Erklärungen, Beispiele und Merkfragen. Historische oder unbelegte Aussagen sind erkennbar eingeordnet; aktuelle Quellen stehen im Lernheft.</p></div></div>'+''.join(cards)+'</section>'
