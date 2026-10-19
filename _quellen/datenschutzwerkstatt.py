"""Tag 13: spielerische, rein lokale Lernmissionen."""
import html
def panel(pid,n):
    return f'''<section class="tpanel wrap" id="demos" role="tabpanel" aria-label="Demos">
    <div class="privacy-lab" data-privacy data-profile="{html.escape(pid)}">
      <div class="privacy-hero"><div><p class="kicker">Datenschutz-Werkstatt · Tag 13</p><h2>Die Daten bleiben.<br>Der Knoten geht.</h2><p>Heute ist man Daten-Detektiv. Drei kleine Missionen, überraschende Fälle und immer ein „Aha, deshalb!“.</p><p class="privacy-chips"><span>Nur erfundene Fälle</span><span>Kein Zeitlimit</span><span>Fehler sind zum Lernen da</span></p></div><div class="privacy-stamp" aria-hidden="true"><span>MISSION</span><b>Weniger<br>Daten.<br>Mehr<br>Durchblick.</b><span>STUDIO MORGEN</span></div></div>
      <div class="privacy-map" aria-label="Mission auswählen">
        <button type="button" data-mission="detective" aria-pressed="true" aria-controls="privacy-stage"><span>01 · ERKENNEN</span><b>Wer steckt dahinter?</b><small>Sechs Fundstücke. Name weg – Mensch weg?</small><em data-badge="detective">Noch offen</em></button>
        <button type="button" data-mission="prompt" aria-pressed="false" aria-controls="privacy-stage"><span>02 · AUSPROBIEREN</span><b>Der Prompt packt aus.</b><small>Nur mitnehmen, was die Aufgabe braucht.</small><em data-badge="prompt">Noch offen</em></button>
        <button type="button" data-mission="inbox" aria-pressed="false" aria-controls="privacy-stage"><span>03 · ENTSCHEIDEN</span><b>Post mit Fragezeichen.</b><small>Sechs Nachrichten. Was wäre jetzt sinnvoll?</small><em data-badge="inbox">Noch offen</em></button>
      </div>
      <p class="privacy-save" role="status" data-privacy-save></p>
      <div id="privacy-stage" class="privacy-stage"></div>
      <section class="privacy-takeaway"><h3>Ein Gedanke, der mitkommt.</h3><label for="privacy-note">In eigenen Worten: Worauf achtet man beim nächsten KI-Einsatz?</label><textarea id="privacy-note" rows="3" maxlength="1500" placeholder="Zum Beispiel: Eine Kundennummer ist noch keine Anonymisierung …" aria-describedby="privacy-local"></textarea><p id="privacy-local">Nur erfundene Angaben. Die Notiz bleibt auf diesem Gerät in diesem Browser. Sie wird nicht automatisch bewertet.</p><button class="btn" type="button" data-privacy-download>Lernnotiz mitnehmen · TXT</button></section>
      <div class="privacy-bridge"><div><h3>Den Aha-Moment genauer verstehen.</h3><p>Die Werkstatt übt ausgewählte Gedanken. Unter „Einfach erklärt“ werden alle 74 Folien begleitet – mit Einzelheiten, Beispielen, Quellen und markierten Korrekturen.</p></div><a class="btn primary" href="#einfach" data-tab-go="einfach">Zur ganzen Lektion →</a></div>
      <p class="small">Vorbereitete Lernsimulation, keine echte KI, keine externen Nachrichten und keine rechtliche Freigabe. Fortschritt wird nur lokal je Person gespeichert. Ohne verfügbaren Speicher funktioniert die Runde vorübergehend.</p>
      <noscript><p>Für die Missionen braucht man JavaScript. Die vollständigen Erklärungen und das Lernheft bleiben lesbar.</p></noscript>
    </div></section>'''
