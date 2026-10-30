from pathlib import Path
import sys,json,hashlib,shutil,zipfile
import fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3];Q=ROOT/'_quellen';PUB=ROOT/'plattform/public';QA=Q/'build/modul2-tag1';MATERIAL=PUB/'material/modul2-tag1'
sys.path.insert(0,str(Q))
from modul2.tag1.content import DATE,SOURCES,BRIEF,VIDEO
from modul2.tag1.ideas import IDEAS
from modul2.tag1.series import BOOKS,ENTRIES
from modul2.tag1.simple_day1 import IDEA_HELP
from modul2.tag1.simple_day2 import IDEA_HELP as IDEA_HELP2,VARIANT,RESEARCH_DATE
from modul2.tag1.simple_day3 import IDEA_HELP as IDEA_HELP3,EXTRA_SOURCES,FEED
from modul2.tag1.series_render import pages,render_web,render_day,NAMES,ORIGINAL
from tag19.build import make_pdf

def starter():
 base=MATERIAL/'Make-Starterpaket';base.mkdir(parents=True,exist_ok=True)
 files={'01-redaktionsbriefing.json':json.dumps(BRIEF,ensure_ascii=False,indent=2),'02-video-freigabe.json':json.dumps(VIDEO,ensure_ascii=False,indent=2),'03-ki-musterantwort.json':json.dumps(dict(kategorie='VIDEO',unsicher=False,begruendung='Die Nachricht fragt nach einem Interviewablauf.'),ensure_ascii=False,indent=2),'START_HIER.md':'# Make-Starterpaket · 26.10.2026\n\nNur Testmaterial, KEINE importierbaren Make-Blueprints. Alle Geschäftsfälle sind erfunden. 03-ki-musterantwort.json ist vorbereitet, nicht das Ergebnis eines hier ausgeführten Modellaufrufs.\n\nDie ersten drei Workflows brauchen nur Make Free. Automatische Planung aus lassen. Vor und nach Testläufen Restcredits ansehen. Anleitung im Lernheft.\n','Mein-Testprotokoll.md':'# Mein eigener Test\nZiel:\nVerwendeter Datensatz:\nAusgeführte Module und Filter:\nErwartetes Ergebnis:\nTatsächlich beobachtet:\nCredits vorher / nachher:\nZweiter Testfall:\nOffene Frage:\n','Budget.txt':'Eigene Lernrunde: maximal50Credits als Unterrichtsbudget, kein Tariflimit.\nWF1: ersteEinzelprobe1 + kompletterLauf2 + zweiterName2 = geplant5.\nWF2: Einzelprobe1 + kompletterLauf2 + Variante2 = geplant5.\nWF3: Einzelprobe1 + passenderFall2 + zweiStopps1+1 = geplant5.\nWF4optional: HTTP-Einzelprobe1 + kompletterLauf2 = geplant3.\nGemeinsam18Credits unter den genannten Ein-Bundle-Annahmen; weitereFehler/Tests zusätzlich. TatsächlicheAnzeigezählt.\n'}
 for name,text in files.items():(base/name).write_text(text,encoding='utf8')
 (base/'30-Ideen.json').write_text(json.dumps(IDEAS,ensure_ascii=False,indent=2),encoding='utf8')
 for idea in IDEAS:
  p=base/'ideen'/f'{idea["n"]:02}.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(dict(projekt='Lernversuch',thema=idea['title'],kanal=idea['group'],status='ENTWURF'),ensure_ascii=False,indent=2),encoding='utf8')
 archive=MATERIAL/'Make-Starterpaket.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in base.rglob('*'):
   if p.is_file():z.write(p,p.relative_to(MATERIAL).as_posix())
 return archive

def day_starters(days=None):
 base=MATERIAL/'Make-Starterpaket'
 for day,b in BOOKS.items():
  if days is not None and day not in days:continue
  path=MATERIAL/f'Make-Tag{day}-Starterpaket.zip'
  texts={'START_HIER.md':f'# Modul 2 · Lektion 1 · Tag {day}/4\n\n{b["weekday"]}, {b["date"]}: {b["subtitle"]}.\nNur Testmaterial, keine Make-Blueprints. Automatische Planung aus lassen; Creditverbrauch vor/nach Versuch prüfen. Andere Etappen folgen an ihrem Tag.\n', 'Mein-Testprotokoll.md':(base/'Mein-Testprotokoll.md').read_text(encoding='utf8'),'Ideen-heute.md':'\n\n'.join(str(i['n'])+' · '+i['title']+'\n'+i['test']+'\nAusbau: '+i['extras'] for i in IDEAS if i['n'] in b['ideas'])}
  if day==1:
   texts['START_HIER.md']='# Dein erster Ablauf in Make\n\nHeute nur eine Aufgabe: aus einem Namen eine Begrüßung machen.\n\n1. Lies die einfache Anleitung im Tagesheft.\n2. Baustein 1: Tools > Set variable. Variable name: vorname. Variable value: Luna.\n3. Ersten Baustein einmal mit Run once testen. Die Ausgabe soll Luna enthalten.\n4. Baustein 2: Tools > Compose a string. Hallo und ein Leerzeichen tippen, den Namenswert aus Baustein 1 auswählen, dann ! Willkommen in Modul 2. tippen.\n5. Speichern und beide Bausteine mit Run once starten. Ausgabe: Hallo Luna! Willkommen in Modul 2.\n6. Nur im ersten Baustein Luna zu Mira ändern. Speichern, nochmals starten. Ausgabe: Hallo Mira! Willkommen in Modul 2.\n\nAutomatische Planung aus lassen. Es wird nichts verschickt. Keine zusätzlichen Konten verbinden. Rechenbeispiel für diese Versuche: 1 + 2 + 2 = 5 Credits. Echte Kontoanzeige vorher und nachher prüfen.\n\nDas sind Merkzettel, keine importierbaren Make-Abläufe. Die Ideen sind freiwilliger Ausblick. Du musst sie heute nicht nachbauen.\n'
   texts['Testnamen.txt']='Erster kompletter Lauf: Luna\nErwartet: Hallo Luna! Willkommen in Modul 2.\n\nZweiter kompletter Lauf: Mira\nErwartet: Hallo Mira! Willkommen in Modul 2.\n\nNur Variable value im ersten Baustein ändern. Der zweite Baustein übernimmt den Namen.\n'
   texts['Mein-Testprotokoll.md']='# Mein kleiner Merkzettel\n\nDas habe ich im ersten Baustein eingetragen:\n\nDas kam im zweiten Baustein heraus:\n\nDas passierte nach dem Wechsel von Luna zu Mira:\n\nMein Verbrauch laut Konto vorher / nachher:\n\nHier brauche ich noch Hilfe:\n'
   texts['Ideen-heute.md']='# Die Ideen sind freiwilliger Ausblick\n\nHeute reicht die Begrüßung mit zwei Namen. Kein JSON lernen und keine zusätzlichen Konten verbinden.\n\n'+ '\n\n'.join(str(n)+' · '+v[0]+'\n'+v[1]+'\n'+v[2] for n,v in IDEA_HELP.items())
  if day==2:
   texts['Redaktionsbriefing.json']=json.dumps(BRIEF,ensure_ascii=False,indent=2)
   texts['Zweiter-Versuch.json']=json.dumps(VARIANT,ensure_ascii=False,indent=2)
   texts['START_HIER.md']='# Tag 2: Aus vier Angaben wird ein Text\n\nDienstag, 27.10.2026. Lies die vollständige Anleitung im Tagesheft.\n\n1. Eigenes neues Szenario M2-02 Redaktionsbriefing anlegen. Zeitplan aus lassen.\n2. JSON > Parse JSON hinzufügen. Den Inhalt von Redaktionsbriefing.json in JSON string einfügen. Das sind Übungsdaten, kein Make-Blueprint zum Importieren.\n3. Zunächst nur dieses Modul mit Run once ausführen. Vier Felder in der Ausgabe prüfen.\n4. Tools > Compose a string anschließen. Projekt:, Thema:, Kanal:, Status: tippen und jeweils das passende Feld aus Parse JSON auswählen. Letzte feste Zeile: Noch keine Veröffentlichung.\n5. Beide Bausteine mit Run once ausführen. Alle vier Werte im Ergebnis vergleichen.\n6. Nur JSON string durch Zweiter-Versuch.json ersetzen. Erneut starten; der zweite Baustein bleibt unverändert. Erwartet: Nordlicht, Interview vorbereiten, Internes Projektbriefing und ENTWURF.\n\nEs wird nichts verschickt. Keine weiteren Konten verbinden. Rechenbeispiel: 1 + 2 + 2 = 5 Credits, weitere Tests zusätzlich. Echte Anzeige im Make-Konto vorher und nachher prüfen.\n'
   texts['Mein-Testprotokoll.md']='# Mein Merkzettel für Tag 2\n\nMeine vier Felder heißen:\n\nDas stand nach dem ersten Test in der Ausgabe:\n\nDas hat sich beim zweiten Test geändert:\n\nMein echter Verbrauch vorher / nachher:\n\nHier brauche ich noch Hilfe:\n'
   texts['Ideen-heute.md']='# Freiwillige Ideen für Tag 2\n\nDie Hauptaufgabe ist der Datenzettel mit zwei Beispielen. Die Ideen sind keine acht weiteren Pflichtaufgaben.\n\n'+'\n\n'.join(str(n)+' · '+v[0]+'\n'+v[1]+'\n'+v[2] for n,v in IDEA_HELP2.items())
  if day==3:
   texts['START_HIER.md']='# Mittwoch ganz leicht: Freigabe-Ampel\n\n28.10.2026. Nur die Hauptaufgabe bauen, danach höchstens ein Extra wählen. Keine Make-Blueprints in diesem Paket.\n\n1. Neues Szenario M2-03 Freigabe-Ampel. Planung aus. Tools > Set variable: Variable name status, Variable value FERTIG. Einmal allein testen.\n2. Tools > Compose a string ergänzen: Beitrag zur Planung bereit. Status: plus den ausgewählten status-Wert aus Baustein 1.\n3. Auf die Verbindung klicken. Filter: status, Textvergleich Equal to, fester Wert FERTIG. Speichern.\n4. Ganzen Ablauf testen: FERTIG erzeugt die Meldung. Nur im ersten Baustein zu ENTWURF ändern, speichern, neu starten: jetzt soll der Weg stoppen.\n\nGeplant 1 + 2 + 1 = ungefähr 4 Credits. Echten Verbrauch im Konto prüfen. Die Meldung steht nur in Make. Es wird nichts verschickt.\n\nFreiwillige Extras und ihre vollständigen Klickwege stehen im Lernheft: Schlagzeile aus RSS lesen oder Idee in eigener Google-Tabelle sichern. Google-Extra nur mit vorhandenem eigenen Konto.\n'
   texts['Testwerte.txt']='Erster Test: FERTIG -> Meldung erscheint.\nZweiter Test: ENTWURF -> Weg stoppt. Keine neue Ausgabe des zweiten Bausteins.\n'
   texts['Mein-Testprotokoll.md']='# Mein Ampel-Test\n\nBei FERTIG passierte:\n\nBei ENTWURF passierte:\n\nMein echter Verbrauch vorher / nachher:\n\nMeine Frage:\n'
   texts['RSS-Adresse.txt']=FEED+'\nModul: RSS > Retrieve RSS Feed Items. Maximum number of returned items: 1. Planung aus.\n'
   texts['Ideenparkplatz.txt']='Für das Google-Extra: eigene neue Tabelle Ideenparkplatz. Zelle A1: Idee. Zelle B1: Bereich.\nDanach die Schritt-für-Schritt-Anleitung im Lernheft befolgen. Jeder Start fügt eine neue Zeile hinzu.\n'
   texts['Ideen-heute.md']='# Nur zum Nachlesen\n\n'+'\n\n'.join(str(n)+' · '+v[0]+'\n'+v[1]+'\n'+v[2] for n,v in IDEA_HELP3.items())
  if day==4:texts['Test-API.txt']='GET https://jsonplaceholder.typicode.com/todos/1\nKeine Anmeldung, kein API-Key. Kleiner fiktiver Testdatensatz.\nZeitangaben sind eine separate optionale Übung; API-Beispiel enthält kein Datum.\n'
  with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
   for name,value in texts.items():z.writestr(f'Make-Tag{day}-Starterpaket/'+name,value)
 if days is not None:return
 # Shared old link remains a collection, but recommends the individual days.
 (base/'START_HIER.md').write_text('# Vier-Tage-Reihe · 26.–29.10.2026\n\nMontag: Begrüßungs-Mixer. Dienstag: JSON und Redaktionsbriefing. Mittwoch: Filter und Video-Freigabe. Donnerstag: API, Zeitangaben und Abschluss.\nDie Tageshefte und Make-Tag1- bis Make-Tag4-Starterpakete sind der empfohlene Einstieg. Dieses Paket sammelt Material für alle vier Tage, keine heutige Aufgabenliste. Keine Make-Blueprints.\n',encoding='utf8')
 with zipfile.ZipFile(MATERIAL/'Make-Starterpaket.zip','w',zipfile.ZIP_DEFLATED) as z:
  for file in base.rglob('*'):
   if file.is_file():z.write(file,file.relative_to(MATERIAL).as_posix())

def main(day=None):
 QA.mkdir(parents=True,exist_ok=True)
 if day is None:starter();day_starters()
 else:day_starters([day])
 report=[]
 original=PUB/'folien/tag-20'/ORIGINAL
 assert original.exists() and len(fitz.open(original))==34
 for d in ([day] if day else BOOKS):
  b=BOOKS[d];items=pages(d);target=ROOT/b['out']/b['pdf'];qa=QA/f'day-{d}';qa.mkdir(exist_ok=True)
  layout=make_pdf(items,target,f'Modul 2 · Lektion 1 · Tag {d}/4 · '+b['title'],header=f'MODUL 2 · LEKTION 1 · TAG {d}/4',date=b['date'],research_date=RESEARCH_DATE if d in (2,3) else DATE);shutil.copy2(target,PUB/'pdf'/b['pdf'])
  assert len({x['key'] for x in items})==len(items)
  with fitz.open(target) as doc:
   assert len(doc)==len(items)
   for n,page in enumerate(doc,1):
    for block in page.get_text('blocks'):assert block[0]>=20 and block[1]>=10 and block[2]<=575 and block[3]<=830,(d,n,block)
    page.get_pixmap(dpi=85).save(qa/f'page-{n:02}.png')
   for first in range(1,len(doc)+1,12):
    sheet=Image.new('RGB',(1240,1380),'#deded6');draw=ImageDraw.Draw(sheet)
    for offset,n in enumerate(range(first,min(first+12,len(doc)+1))):
     im=Image.open(qa/f'page-{n:02}.png');im.thumbnail((298,425));x=offset%4*310+6;y=offset//4*460+20;sheet.paste(im,(x,y));draw.text((x,y-15),str(n),fill='black')
    sheet.save(qa/f'contact-{first:02}.jpg',quality=90)
  for pid in NAMES:
   for suffix,content in [('',render_day(pid,d)),('lernheft/',render_web(pid,d))]:
    path=PUB/pid/f'modul-2/tag-{d}'/suffix/'index.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf8')
  (qa/'layout.json').write_text(json.dumps(layout,indent=2),encoding='utf8');report.append(dict(day=d,pages=len(items),min_scale=min(r['scale'] for r in layout),pdf=str(target)))
 (Path(__file__).parent/'sources.json').write_text(json.dumps(dict(date=DATE,sources=SOURCES,original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),slide_assignment={str(d):b['slides'] for d,b in BOOKS.items()},idea_assignment={str(d):b['ideas'] for d,b in BOOKS.items()}),ensure_ascii=False,indent=2),encoding='utf8')
 (Path(__file__).parent/'klassenbuch-26-29-10-2026.md').write_text('# Modul 2 · Lektion 1 · 26.–29.10.2026\n\n'+''.join('## '+b['weekday']+', '+b['date']+'\n\n'+''.join('- '+text+'\n' for text in ENTRIES[d])+'\n' for d,b in BOOKS.items()),encoding='utf8')
 (QA/'series-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else None)
