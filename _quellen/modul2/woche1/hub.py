"""Learning Hub Modul 2 · Woche 1 (Tag 5) und Wochenheft (Web + Druck).

render_hub(pid)  -> /hefte/<pid>/modul-2/tag-5/   (alle Modul-1-Funktionen + Vorlagen + Use-Case-Labor)
render_web(pid)  -> /hefte/<pid>/modul-2/tag-5/lernheft/   (Wochenheft zum Lesen)
render_print()   -> HTML für die PDF-Fassung
"""
import json
import re
from pathlib import Path

from .bausteine import E, md
from .blueprints import AUTOMATIONS
from .daten import TAG, LERNHEFT, MAKE_N, UC_N, folie_label
from . import inhalt

ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / 'plattform/public/assets'
NAMES = {'ingo': 'Ingo', 'carmen': 'Carmen', 'tabea': 'Tabea'}
FOLIEN_PDF = 'Folien_Woche1_Make-und-Use-Cases.pdf'
VERSION = 'woche1-1'

DAYS = [
    (1, 'Mo', '26.10.', 'Make verstehen und klein anfangen', 'Grundlagen, Credits, erster Ablauf', [1]),
    (2, 'Di', '27.10.', 'Daten verstehen und weitergeben', 'JSON, Parse JSON, Mapping', [2]),
    (3, 'Mi', '28.10.', 'Die einfache Freigabe-Ampel', 'Filter, Router, Webhooks, KI-Rollen', [3, 4]),
    (4, 'Do', '29.10.', 'Verbinden, prüfen, abschließen', 'Test-API, ISO 8601, formatDate', [5, 6]),
    (5, 'Fr', '30.10.', 'Use Cases identifizieren', 'Zeitfresser, Steckbriefe, Autonomie', [7, 8, 9]),
]

FONT_FACES = '''@font-face{font-family:"Instrument Serif";font-style:normal;font-weight:400;font-display:swap;src:url(/hefte/assets/fonts/instrument-serif-latin.woff2) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Instrument Serif";font-style:normal;font-weight:400;font-display:swap;src:url(/hefte/assets/fonts/instrument-serif-latin-ext.woff2) format("woff2");unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+20A0-20AB,U+20AD-20C0,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"Instrument Serif";font-style:italic;font-weight:400;font-display:swap;src:url(/hefte/assets/fonts/instrument-serif-italic-latin.woff2) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Instrument Serif";font-style:italic;font-weight:400;font-display:swap;src:url(/hefte/assets/fonts/instrument-serif-italic-latin-ext.woff2) format("woff2");unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+20A0-20AB,U+20AD-20C0,U+2C60-2C7F,U+A720-A7FF}
'''

# Inhalt des Wochenhefts (Web, Hub-Reiter und Druck teilen diese Regeln)
CONTENT_CSS = '''
.wh{--fw:#05614c;--fw-d:#032a21;--fw-m:#05dbba;--fw-mt:#e2fcf7;--fw-t:#e8f4f0;--fw-l:#c7e5dc;--ink:#2c302e;--head:#0d0d0d;--mut:#5c6360;--line:#dadedc;--gold:#f6cf09;--gold-t:#fdf6d6;--red:#d91e0c;--red-t:#fbe6e3;color:var(--ink)}
.wh .serif{font-family:"Instrument Serif",Georgia,serif;font-weight:400;letter-spacing:0}
.wh .teil{margin:0 0 56px}
.wh .teil-kopf{display:flex;gap:20px;align-items:center;background:linear-gradient(120deg,var(--fw-d),var(--fw) 70%);color:#fff;border-radius:22px;padding:26px 28px;margin:0 0 26px;position:relative;overflow:hidden}
.wh .teil-kopf::after{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,rgba(5,219,186,.45),transparent 70%)}
.wh .teil-b{flex:0 0 auto;width:64px;height:64px;border-radius:18px;background:var(--fw-m);color:var(--fw-d);font:800 34px/64px Archivo,sans-serif;text-align:center}
.wh .teil-t{color:#fff!important;margin:0 0 4px;font-size:clamp(24px,3.4vw,34px);line-height:1.1;letter-spacing:-.02em}
.wh .teil-kopf p{margin:0;color:rgba(255,255,255,.82);max-width:62ch}
.wh .kapitel{background:#fff;border:1px solid var(--line);border-radius:20px;padding:26px 28px 22px;margin:0 0 18px;box-shadow:0 1px 2px rgba(0,0,0,.04),0 10px 30px rgba(3,42,33,.05);scroll-margin-top:84px}
.wh .k-head{display:flex;gap:16px;align-items:flex-start;margin:0 0 14px}
.wh .k-nr{flex:0 0 auto;min-width:52px;height:40px;padding:0 10px;border-radius:12px;background:var(--fw-t);color:var(--fw);font:800 16px/40px Archivo,sans-serif;text-align:center}
.wh .k-kicker{margin:0 0 3px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--fw);font-weight:700}
.wh .kapitel h2{margin:0;font-size:clamp(21px,2.6vw,27px);line-height:1.18;color:var(--head);letter-spacing:-.02em}
.wh .kapitel h3{font-size:19px;margin:22px 0 8px;color:var(--head)}
.wh .kapitel h4{font-size:16.5px;margin:18px 0 6px;color:var(--head)}
.wh p{margin:0 0 10px;line-height:1.6}
.wh code{background:#eef3f1;border-radius:6px;padding:1px 6px;font:600 .92em ui-monospace,Consolas,monospace;color:#0b4a3b;word-break:break-word}
.wh .lbl{display:inline-block;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:800;margin:0 0 4px}
.wh .merk{border-left:5px solid var(--fw-m);background:var(--fw-mt);border-radius:0 14px 14px 0;padding:14px 18px;margin:16px 0}
.wh .merk .lbl{color:var(--fw)}
.wh .merk p{font-weight:700;color:var(--head);margin:0;font-size:17px;line-height:1.45}
.wh .achtung{background:var(--gold-t);border:1px solid #f1e08a;border-radius:14px;padding:14px 18px;margin:16px 0}
.wh .achtung .lbl{color:#7a5d00}
.wh .tipp{background:#eef5ff;border:1px solid #cfe1fb;border-radius:14px;padding:14px 18px;margin:16px 0}
.wh .tipp .lbl{color:#0a5bb8}
.wh .korrektur{background:#f4f2fb;border:1px dashed #b9b0dd;border-radius:14px;padding:14px 18px;margin:16px 0}
.wh .korrektur .lbl{color:#4a3d8f}
.wh .beispiel{background:#f5f6f5;border-radius:14px;padding:14px 18px;margin:16px 0}
.wh .beispiel .lbl{color:var(--mut)}
.wh .achtung p,.wh .tipp p,.wh .korrektur p,.wh .beispiel p{margin:0}
.wh .tab-wrap{overflow-x:auto;margin:12px 0 16px;border:1px solid var(--line);border-radius:14px}
.wh table.tab{width:100%;border-collapse:collapse;font-size:15px;background:#fff}
.wh .tab th{background:var(--fw-d);color:#fff;text-align:left;padding:10px 12px;font-size:13.5px;font-weight:700;vertical-align:bottom}
.wh .tab td{padding:10px 12px;border-top:1px solid var(--line);vertical-align:top;line-height:1.45}
.wh .tab tbody tr:nth-child(even) td{background:#f8faf9}
.wh ol.flow{list-style:none;margin:14px 0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;counter-reset:f}
.wh ol.flow li{position:relative;background:var(--fw-t);border:1px solid var(--fw-l);border-radius:14px;padding:12px 14px}
.wh ol.flow li b{display:block;color:var(--fw-d);font-size:15px}
.wh ol.flow li span{display:block;font-size:14px;color:var(--ink);margin-top:3px;line-height:1.4}
.wh ol.flow.steps{grid-template-columns:1fr}
.wh ol.flow.steps li{display:grid;grid-template-columns:minmax(120px,190px) 1fr;gap:12px;align-items:baseline}
.wh ol.flow.steps li span{margin:0}
.wh .karten{display:grid;gap:12px;margin:14px 0}
.wh .karten.c2{grid-template-columns:repeat(2,minmax(0,1fr))}
.wh .karten.c3{grid-template-columns:repeat(3,minmax(0,1fr))}
.wh .karte{border:1px solid var(--line);border-radius:16px;padding:16px;background:linear-gradient(180deg,#fff,#fbfcfb)}
.wh .karte .num{display:inline-flex;min-width:30px;height:30px;padding:0 8px;align-items:center;justify-content:center;border-radius:9px;background:var(--fw);color:#fff;font-weight:800;font-size:14px;margin-bottom:8px}
.wh .karte h4{margin:0 0 6px;font-size:16.5px}
.wh .karte p{margin:0;font-size:15px;line-height:1.5}
.wh dl.glossar{margin:12px 0;display:grid;gap:8px}
.wh .g-row{display:grid;grid-template-columns:minmax(140px,220px) 1fr;gap:14px;padding:10px 0;border-top:1px solid var(--line)}
.wh .g-row dt{font-weight:800;color:var(--head)}
.wh .g-row dd{margin:0}
.wh .g-row small{display:block;color:var(--mut);margin-top:3px}
.wh .code{background:#0f1a17;color:#d7f7ee;border-radius:14px;padding:14px 16px;margin:12px 0;overflow-x:auto}
.wh .code pre{margin:0;font:14px/1.5 ui-monospace,Consolas,monospace;white-space:pre-wrap;word-break:break-word}
.wh .code-lbl{display:block;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--fw-m);font-weight:800;margin-bottom:6px}
.wh .folien-ref{font-size:13.5px;color:var(--mut);margin:14px 0 0;padding-top:10px;border-top:1px dashed var(--line)}
.wh .folien-ref a{color:#0a5bb8;font-weight:600}
.wh .kernsatz{margin:18px 0;padding:22px 24px;border-radius:18px;background:var(--fw-d);color:#fff;font:400 clamp(22px,2.8vw,30px)/1.25 "Instrument Serif",Georgia,serif}
.wh .kernsatz cite{display:block;margin-top:10px;font:600 13px Archivo,sans-serif;color:var(--fw-m);font-style:normal}
.wh .chip{display:inline-flex;align-items:center;gap:6px;border-radius:999px;background:var(--fw-t);color:var(--fw-d);font-size:13px;font-weight:700;padding:5px 11px}
.wh .bp-meta{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}
.wh .bp-lernt{background:#f5f6f5;border-radius:12px;padding:10px 14px}
.wh .bp-btns{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:14px 0}
.wh .bp-done{display:inline-flex;gap:8px;align-items:center;font-weight:700;font-size:14.5px;padding:8px 12px;border-radius:999px;border:1px solid var(--line);cursor:pointer}
.wh .bp-done input{width:18px;height:18px;accent-color:var(--fw)}
.wh .bp-mod{margin:10px 0 14px}
.wh .bp-mod-h{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 4px}
.wh .bp-app{background:var(--fw);color:#fff;border-radius:8px;padding:3px 9px;font-weight:700;font-size:13.5px}
.wh .bp-name{font-weight:700;color:var(--head)}
.wh .bp-tab td:first-child{width:22%}.wh .bp-tab td:nth-child(2){width:36%}
.wh .bp-steps{margin:6px 0 10px;padding-left:22px}
.wh .soll{background:#0f1a17;border-radius:14px;padding:14px 16px;margin:10px 0;color:#d7f7ee}
.wh .soll .lbl{color:var(--fw-m)}
.wh .soll pre{margin:0;font:600 15px/1.5 ui-monospace,Consolas,monospace;white-space:pre-wrap}
.wh .aendern{border:2px solid var(--fw-m);border-radius:14px;padding:12px 16px;margin:10px 0}
.wh .aendern p{margin:4px 0}
.wh .fehlerhilfe{background:var(--red-t);border-radius:14px;padding:12px 16px;margin:10px 0}
.wh .fehlerhilfe .lbl{color:#9b1408}
.wh .fehlerhilfe ul{margin:4px 0 0;padding-left:20px}
.wh .fehlerhilfe li{margin:4px 0}
.wh .bp-file{font-size:14px;color:var(--mut)}
.wh .steck-bsp{margin:14px 0}.wh .steck-h{font-weight:800;margin:0 0 4px}
.wh .steck-bsp.mein .tab-wrap{border:2px solid var(--fw-m)}
.wh .spick{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.wh .spick-box{border:1px solid var(--line);border-radius:14px;padding:12px 16px;background:#fbfcfb}
.wh .spick-box h4{margin:0 0 6px;color:var(--fw)}
.wh .spick-box ul{margin:0;padding-left:18px}
.wh .spick-box li{margin:2px 0;font-size:14.5px}
.wh .kb-tag{border-left:4px solid var(--fw);padding:4px 0 4px 16px;margin:14px 0}
.wh .kb-h{margin:0 0 4px}
.wh .kb-tag ul{margin:0;padding-left:20px}
.wh .quellen{padding-left:18px}.wh .quellen li{margin:6px 0}
.wh .mehr summary{cursor:pointer;font-weight:700;color:var(--fw)}
.wh .tool{border:2px solid var(--fw-l);background:linear-gradient(180deg,#fbfefd,#fff);border-radius:18px;padding:16px 18px;margin:16px 0}
.wh .tool-h{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;margin:0 0 12px}
.wh .tool-h b{font-size:17px;color:var(--fw-d)}
.wh .tool-h span{font-size:13px;color:var(--mut)}
.wh .fld{display:block;margin:0 0 12px}
.wh .fld>span{display:block;font-weight:700;color:var(--head);margin-bottom:4px;font-size:15px}
.wh .fld small{display:block;color:var(--mut);font-size:13px;margin:-2px 0 4px}
.wh .fld input,.wh .fld textarea,.wh .fld select,.wh .zf-table input,.wh .zf-table select{width:100%;font:inherit;font-size:15.5px;padding:9px 11px;border:1px solid #c2c8c5;border-radius:10px;background:#fff;color:var(--head)}
.wh .fld input:focus,.wh .fld textarea:focus,.wh .fld select:focus,.wh .zf-table input:focus{outline:3px solid rgba(5,219,186,.45);border-color:var(--fw)}
.wh .chk{display:flex;gap:8px;align-items:flex-start;margin:6px 0;font-size:14.5px;cursor:pointer}
.wh .chk input{width:18px;height:18px;flex:0 0 auto;margin-top:2px;accent-color:var(--fw)}
.wh .zf-row{display:grid;grid-template-columns:minmax(0,2.4fr) repeat(4,minmax(0,1fr)) minmax(90px,1fr) 36px;gap:8px;align-items:center;padding:6px 0;border-bottom:1px solid var(--line)}
.wh .zf-row.kopf{font-size:12.5px;font-weight:800;color:var(--mut);text-transform:uppercase;letter-spacing:.04em;border-bottom:2px solid var(--fw-l)}
.wh .zf-row.top{background:var(--fw-mt);border-radius:10px}
.wh .zf-min{font-weight:800;color:var(--fw-d);text-align:right;font-variant-numeric:tabular-nums}
.wh .zf-del{border:0;background:none;color:var(--mut);font-size:20px;cursor:pointer;border-radius:8px}
.wh .zf-del:hover{background:var(--red-t);color:var(--red)}
.wh .zf-top{margin-top:12px;font-weight:700}
.wh .zf-top ol{margin:6px 0 0;padding-left:22px}
.wh .sb-tabs{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 12px}
.wh .sb-tab{border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 14px;font-weight:700;cursor:pointer}
.wh .sb-tab[aria-pressed="true"]{background:var(--fw);border-color:var(--fw);color:#fff}
.wh .sb-check{font-weight:700}.wh .sb-check.ok{color:var(--fw)}.wh .sb-check.warn{color:#9b5d00}
.wh .st-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.wh .st-col{border:1px solid var(--line);border-radius:14px;padding:12px;background:#fff}
.wh .st-h{font-weight:800;color:var(--fw-d);margin:0 0 8px}.wh .st-h span{font-weight:600;color:var(--mut)}
.wh .st-sub{font-weight:800;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);margin:12px 0 4px}
.wh .st-result{font-weight:700;margin:8px 0 0}.wh .st-result.ok{color:var(--fw)}.wh .st-result.warn{color:#9b5d00}
.wh .tr-q{font-size:19px;font-weight:700;color:var(--head);margin:0 0 12px}
.wh .tr-step{font-size:12.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--fw)}
.wh .tr-res{background:var(--fw-d);color:#fff;border-radius:14px;padding:16px 18px}
.wh .tr-res b{display:block;font-size:20px;color:var(--fw-m)}
.wh .btnrow{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}
.wh .copied{color:var(--fw);font-weight:700;font-size:14px}
@media (max-width:760px){
 .wh .kapitel{padding:20px 16px 16px;border-radius:16px}
 .wh .karten.c2,.wh .karten.c3,.wh .spick,.wh .st-grid{grid-template-columns:1fr}
 .wh ol.flow.steps li{grid-template-columns:1fr;gap:2px}
 .wh .g-row{grid-template-columns:1fr;gap:2px}
 .wh .teil-kopf{padding:20px 18px;gap:14px}.wh .teil-b{width:48px;height:48px;font-size:26px;line-height:48px;border-radius:14px}
 .wh table.tab{font-size:14px}
 .wh .tab-wrap{border:0;overflow:visible}
 .wh table.tab,.wh .tab thead,.wh .tab tbody,.wh .tab tr,.wh .tab td{display:block;width:auto!important}
 .wh .tab thead{display:none}
 .wh .tab tr{border:1px solid var(--line);border-radius:12px;margin:0 0 8px;overflow:hidden}
 .wh .tab td{border-top:1px solid var(--line)}.wh .tab td:first-child{border-top:0;background:#f5f8f7!important;font-weight:700}
 .wh .tab td[data-label]:not([data-label=""])::before{content:attr(data-label);display:block;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);font-weight:800}
 .wh .zf-row{grid-template-columns:1fr 1fr 1fr;grid-template-areas:"t t t" "h m s" "f min del"}
 .wh .zf-row.kopf{display:none}
 .wh .zf-row>:nth-child(1){grid-area:t}.wh .zf-row>:nth-child(2){grid-area:h}.wh .zf-row>:nth-child(3){grid-area:m}.wh .zf-row>:nth-child(4){grid-area:s}.wh .zf-row>:nth-child(5){grid-area:f}.wh .zf-row>:nth-child(6){grid-area:min}.wh .zf-row>:nth-child(7){grid-area:del}
}
'''

# Learning-Hub-Rahmen (zusätzlich zu app.css/kurs.css der Plattform)
HUB_CSS = '''
.hub-hero{background:radial-gradient(900px 420px at 88% -10%,rgba(5,219,186,.35),transparent 60%),linear-gradient(135deg,#032a21 0%,#05614c 62%,#0a7a60 100%);color:#fff;padding:44px 0 34px;position:relative;overflow:hidden}
.hub-hero::after{content:"";position:absolute;inset:auto -80px -120px auto;width:360px;height:360px;border-radius:50%;border:1px solid rgba(255,255,255,.12)}
.hub-hero .kicker{color:#05dbba}
.hub-hero h1{color:#fff!important;font-size:clamp(34px,5.4vw,62px);line-height:1.02;letter-spacing:-.035em;margin:0 0 12px;max-width:18ch}
.hub-hero h1 em{font-family:"Instrument Serif",Georgia,serif;font-style:italic;font-weight:400;color:#05dbba;letter-spacing:0}
.hub-hero .lead{color:rgba(255,255,255,.86);max-width:62ch;font-size:18px;margin:0}
.hub-hero .hero-btns .btn{border-color:rgba(255,255,255,.35);color:#fff;background:rgba(255,255,255,.06)}
.hub-hero .hero-btns .btn.primary{background:#05dbba;border-color:#05dbba;color:#032a21}
.hub-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:26px}
.hub-stat{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:16px;padding:12px 14px}
.hub-stat b{display:block;font-size:24px;line-height:1.1;color:#fff;font-variant-numeric:tabular-nums}
.hub-stat>span{font-size:13px;color:rgba(255,255,255,.75)}
.hub-week{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin:8px 0 26px}
.hub-day{position:relative;background:#fff;border:1px solid var(--line);border-radius:18px;padding:16px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:6px}
.hub-day.heute{border:2px solid #05dbba;background:linear-gradient(180deg,#f2fffc,#fff)}
.hub-day .d-top{display:flex;justify-content:space-between;align-items:center}
.hub-day .d-wd{font-weight:800;color:#05614c;font-size:14px;letter-spacing:.06em;text-transform:uppercase}
.hub-day .d-badge{font-size:11px;font-weight:800;background:#05dbba;color:#032a21;border-radius:999px;padding:3px 8px}
.hub-day h3{font-size:17px;line-height:1.2;margin:2px 0;color:var(--head)}
.hub-day p{font-size:14px;margin:0;color:var(--muted)}
.hub-day .d-links{margin-top:auto;display:flex;flex-wrap:wrap;gap:6px;padding-top:8px}
.hub-day .d-links a{font-size:13px;font-weight:700;border:1px solid var(--line);border-radius:999px;padding:4px 10px;text-decoration:none}
.hub-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:8px 0 26px}
.hub-tile{display:flex;flex-direction:column;gap:6px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;text-decoration:none;color:var(--ink);box-shadow:var(--shadow);transition:transform .18s,box-shadow .18s,border-color .18s}
.hub-tile:hover{transform:translateY(-3px);border-color:#05dbba;box-shadow:0 14px 34px rgba(3,42,33,.12)}
.hub-tile .t-ico{width:42px;height:42px;border-radius:12px;background:#e8f4f0;color:#05614c;display:flex;align-items:center;justify-content:center}.hub-tile .t-ico svg{width:24px;height:24px}
.hub-tile b{font-size:18px;color:var(--head)}
.hub-tile span{font-size:14.5px;color:var(--muted)}
.hub-tile .t-meter{height:6px;border-radius:3px;background:#e6e8e9;overflow:hidden;margin-top:auto}
.hub-tile .t-meter i{display:block;height:100%;width:0;background:#05dbba;transition:width .4s}
.hub-h2{font-size:24px;margin:28px 0 10px;letter-spacing:-.02em}
.hub-note{font-size:14px;color:var(--muted)}
.tabs a[data-tab="start"]{font-weight:800}
.tabs a .tn{display:inline-block;margin-left:6px;font-size:11px;font-weight:800;color:#032a21;background:#05dbba;border-radius:999px;padding:1px 7px;vertical-align:2px}
.lc-day{display:inline-block;font-size:11.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#05614c;background:#e8f4f0;border-radius:999px;padding:3px 9px;margin-bottom:6px}
.lc-filter{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
.lc-filter button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 13px;font-weight:700;cursor:pointer}
.lc-filter button[aria-pressed="true"]{background:#05614c;color:#fff;border-color:#05614c}
.words-search{width:100%;max-width:420px;font:inherit;padding:10px 12px;border:1px solid var(--line2);border-radius:12px;margin:0 0 14px}
.hub-heft{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:18px;align-items:start}
.hub-heft .cover{background:linear-gradient(150deg,#032a21,#05614c);color:#fff;border-radius:20px;padding:26px;min-height:260px;display:flex;flex-direction:column;justify-content:space-between}
.hub-heft .cover h3{color:#fff!important;font-size:30px;line-height:1.05;margin:8px 0}
.hub-heft .cover em{font-family:"Instrument Serif",Georgia,serif;color:#05dbba;font-weight:400}
.hub-heft ol{padding-left:20px}
@media (max-width:900px){.hub-week{grid-template-columns:repeat(2,minmax(0,1fr))}.hub-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.hub-stats{grid-template-columns:repeat(2,minmax(0,1fr))}.hub-heft{grid-template-columns:1fr}}
@media (max-width:560px){.hub-week,.hub-grid{grid-template-columns:1fr}.hub-hero{padding:30px 0 24px}}
'''

# Wochenheft-Leseseite (eigener Rahmen)
READ_CSS = '''
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:#f3f5f4;font:16.5px/1.6 Archivo,"Segoe UI",system-ui,sans-serif;color:#2c302e}
a{color:#05614c}
.skip{position:absolute;left:-999px}.skip:focus{left:12px;top:12px;background:#fff;padding:8px 12px;z-index:9}
.rd-top{background:#0d0d0d;color:#fff}
.rd-top-in{max-width:1240px;margin:0 auto;padding:12px 20px;display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:space-between}
.rd-top a{color:#fff;text-decoration:none;font-weight:700;font-size:14.5px}
.rd-top .rd-pdf{background:#05dbba;color:#032a21;border-radius:999px;padding:8px 14px}
.rd-top span{color:rgba(255,255,255,.7);font-size:14px}
.rd-cover{background:radial-gradient(800px 380px at 85% 0%,rgba(5,219,186,.35),transparent 60%),linear-gradient(135deg,#032a21,#05614c 65%);color:#fff}
.rd-cover-in{max-width:1240px;margin:0 auto;padding:46px 20px 40px}
.rd-cover .eyebrow{color:#05dbba;font-weight:800;letter-spacing:.14em;text-transform:uppercase;font-size:12.5px;margin:0 0 10px}
.rd-cover h1{font-size:clamp(36px,6vw,70px);line-height:1;letter-spacing:-.035em;margin:0 0 14px;max-width:16ch}
.rd-cover h1 em{font-family:"Instrument Serif",Georgia,serif;font-style:italic;font-weight:400;color:#05dbba;letter-spacing:0}
.rd-cover p{max-width:64ch;color:rgba(255,255,255,.86);margin:0 0 8px}
.rd-cover .rd-btns{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;font:700 15px/1.2 Archivo,system-ui,sans-serif;padding:11px 18px;border-radius:999px;border:1px solid #c2c8c5;background:#fff;color:#0d0d0d;text-decoration:none;cursor:pointer}
.btn.primary{background:#05614c;border-color:#05614c;color:#fff}
.btn.ghost{background:transparent}
.rd-cover .btn{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.35);color:#fff}
.rd-cover .btn.primary{background:#05dbba;border-color:#05dbba;color:#032a21}
.rd-layout{max-width:1240px;margin:0 auto;padding:28px 20px 60px;display:grid;grid-template-columns:260px minmax(0,1fr);gap:28px}
.rd-nav{position:sticky;top:16px;align-self:start;max-height:calc(100vh - 32px);overflow:auto;font-size:14px;background:#fff;border:1px solid #dadedc;border-radius:18px;padding:14px}
.rd-nav p{margin:12px 0 4px;font-weight:800;color:#05614c;font-size:12.5px;letter-spacing:.08em;text-transform:uppercase}
.rd-nav p:first-child{margin-top:0}
.rd-nav ol{list-style:none;margin:0;padding:0}
.rd-nav a{display:block;padding:5px 8px;border-radius:8px;text-decoration:none;color:#2c302e}
.rd-nav a:hover,.rd-nav a.on{background:#e8f4f0;color:#032a21;font-weight:700}
.rd-hint{background:#fdf6d6;border-radius:14px;padding:12px 16px;margin:0 0 20px}
.rd-layout>*{min-width:0}
@media (max-width:960px){.rd-layout{grid-template-columns:minmax(0,1fr);padding:20px 16px 48px}.rd-nav{position:static;max-height:none}.rd-cover-in,.rd-top-in{padding-left:16px;padding-right:16px}}
'''

PRINT_CSS = '''
@page{size:A4;margin:16mm 14mm 16mm 14mm;@bottom-right{content:counter(page) " / " counter(pages);font:600 9pt Archivo,sans-serif;color:#767d79}
 @bottom-left{content:"Futureway KI Institut · Modul 2 · Wochenheft Woche 1 · Stand 30.10.2026";font:600 8.5pt Archivo,sans-serif;color:#767d79}}
@page:first{margin:0;@bottom-right{content:none}@bottom-left{content:none}}
*{box-sizing:border-box}
body{margin:0;font:10.6pt/1.5 Archivo,"Segoe UI",sans-serif;color:#2c302e;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pr-cover{height:297mm;background:radial-gradient(160mm 110mm at 90% 0%,rgba(5,219,186,.4),transparent 60%),linear-gradient(140deg,#032a21,#05614c 70%);color:#fff;padding:28mm 22mm;display:flex;flex-direction:column;break-after:page}
.pr-cover img{width:44mm;filter:brightness(0) invert(1);margin-bottom:auto}
.pr-cover .eyebrow{color:#05dbba;font-weight:800;letter-spacing:.16em;text-transform:uppercase;font-size:10pt}
.pr-cover h1{font-size:46pt;line-height:.98;letter-spacing:-.03em;margin:6mm 0}
.pr-cover h1 em{font-family:"Instrument Serif",Georgia,serif;font-style:italic;font-weight:400;color:#05dbba;letter-spacing:0}
.pr-cover p{font-size:12pt;max-width:150mm;color:rgba(255,255,255,.88)}
.pr-cover .pr-meta{margin-top:14mm;display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}
.pr-cover .pr-meta div{border:1px solid rgba(255,255,255,.3);border-radius:4mm;padding:3mm 4mm}
.pr-cover .pr-meta b{display:block;font-size:20pt;color:#fff}
.pr-cover .pr-meta span{font-size:9pt;color:rgba(255,255,255,.75)}
.pr-toc{break-after:page}
.pr-toc h2{font-size:24pt;margin:0 0 6mm;color:#0d0d0d}
.pr-toc .t{columns:2;column-gap:10mm}
.pr-toc .t div{break-inside:avoid;margin:0 0 5mm}
.pr-toc b{display:block;color:#05614c;font-size:11pt;margin-bottom:1.5mm}
.pr-toc li{font-size:10pt;margin:.6mm 0}
.wh .teil{margin:0}
.wh .teil-kopf{break-before:page;break-after:avoid;margin-bottom:6mm}
.wh .kapitel{box-shadow:none;border-radius:4mm;padding:6mm 6mm 4mm;margin:0 0 5mm;break-inside:auto}
.wh .k-head,.wh h3,.wh h4,.wh .bp-mod-h{break-after:avoid}
.wh .merk,.wh .achtung,.wh .tipp,.wh .korrektur,.wh .beispiel,.wh .karte,.wh .soll,.wh .aendern,.wh .fehlerhilfe,.wh ol.flow li,.wh .spick-box,.wh .kb-tag,.wh tr,.wh .g-row,.wh .code{break-inside:avoid}
.wh .vorlage{break-before:page}
.wh .kapitel h2{font-size:17pt}
.wh p,.wh td{orphans:3;widows:3}
.wh .tab-wrap{overflow:visible}
.wh table.tab{font-size:9.6pt}
.wh .tab th{font-size:9pt}
.wh .karten.c3{grid-template-columns:repeat(3,1fr)}
.wh .folien-ref a{color:#0a5bb8;text-decoration:none}
.wh .ausfuell td{height:9mm}
.wh .ausfuell.steck td{height:11mm}
.wh .ausfuell-zeile{margin-top:4mm}
.wh .interview-print li{margin:0 0 4mm}
.wh .interview-print .linie{display:block;border-bottom:1px solid #9aa19d;height:8mm}
.wh .kernsatz{font-size:18pt}
'''


def _inline_css(page_html):
    """Externe Plattform-CSS direkt einbetten (robust gegen ausgefallene CSS-Abrufe)."""
    def repl(m):
        name = m.group(1)
        css = (ASSETS / name).read_text(encoding='utf8')
        css = re.sub(r'url\((?!data:|/|https?:)([^)]+)\)', r'url(/hefte/assets/\1)', css)
        assert '</style' not in css.lower()
        return f'<style data-src="{name}">{css}</style>'
    return re.sub(r'<link rel="stylesheet" href="/hefte/assets/([\w.-]+\.css)">', repl, page_html)


def _learnings(pid):
    import plattform as P  # noqa: lokaler Import, um Zyklen zu vermeiden
    import kurs
    t = kurs.TAGE[TAG]
    out = []
    for i, l in enumerate(t['learnings'], 1):
        ref = f't{TAG}:learning:{l["id"]}'
        f = l['folie']
        fol = (f'<a class="lc-folie" href="#folien" data-folie="{f}">{E(folie_label(f))} ansehen</a>' if f
               else '<span class="lc-quelle">Quelle: Make-Hilfe (help.make.com), Stand 30.10.2026</span>')
        thumb = (f'<button class="lc-thumb" type="button" data-folie="{f}" aria-label="{E(folie_label(f))} groß ansehen">'
                 f'<img src="/hefte/folien/tag-24/t{f:02d}.jpg" alt="" loading="lazy" width="360" height="203"></button>' if f else '')
        out.append(f'''<li class="lcard" data-lrn="{l["id"]}" data-day="{l["tag"]}" id="lrn-{l["id"]}">
  <div class="lc-no">{i:02d}</div>
  <div class="lc-main">
    <span class="lc-day">{E(inhalt.TAGNAME[l["tag"]])}</span>
    <h3 class="lc-satz">{E(l["satz"])}</h3>
    <details class="lc-more"><summary>Nochmal erklärt</summary><p>{E(l["erklaert"])}</p></details>
    <div class="lc-actions">
      <button class="chipbtn lc-sitzt" type="button" aria-pressed="false"><span class="ck" aria-hidden="true"></span>Sitzt</button>
      {fol}
      <label class="lc-pick"><input type="checkbox" value="{l["id"]}"> fürs Lernblatt</label>
      <button class="unklar" type="button" data-unklar-ref="{ref}" data-unklar-label="{E("Learning " + str(i) + ": " + l["satz"])}">Unklar?</button>
    </div>
  </div>
  {thumb}
</li>''')
    return ''.join(out), len(t['learnings'])


def _start(pid, n_learn):
    days = ''
    for n, wd, datum, titel, sub, vorl in DAYS:
        heute = n == 5
        if heute:
            links = '<a href="#labor" data-tab-go="labor">Use-Case-Labor</a><a href="lernheft/">Wochenheft</a>'
        else:
            links = (f'<a href="/hefte/{pid}/modul-2/tag-{n}/">Tagesseite</a><a href="/hefte/{pid}/modul-2/tag-{n}/lernheft/">Lernheft</a>')
        links += ''.join(f'<a href="#vorlage-a{a}" data-tab-go="vorlagen" data-jump="vorlage-a{a}">A{a}</a>' for a in vorl)
        days += (f'<div class="hub-day{" heute" if heute else ""}"><div class="d-top"><span class="d-wd">{wd} · {datum}</span>'
                 f'{"<span class=d-badge>heute</span>" if heute else ""}</div><h3>{E(titel)}</h3><p>{E(sub)}</p><div class="d-links">{links}</div></div>')
    tiles = [
        ('vorlagen', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/></svg>', '9 Make-Vorlagen', 'Herunterladen, importieren, Run once – jede Einstellung erklärt.', '<span class="hub-note"><b data-vorlagen-count>0</b> von 9 erledigt</span><div class="t-meter"><i data-vorlagen-meter></i></div>'),
        ('labor', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/></svg>', 'Use-Case-Labor', 'Zeitfresser rechnen, Steckbriefe füllen, Stufe festlegen.', '<span class="hub-note"><b data-labor-count>0</b> Felder ausgefüllt</span>'),
        ('karten', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="5" width="12" height="15" rx="2"/><path d="M8 3h10a2 2 0 0 1 2 2v13"/></svg>', 'Lernkarten', f'{40} Karten der ganzen Woche: umdrehen, ehrlich einsortieren.', ''),
        ('training', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12a8 8 0 0 1 14-5.3L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-14 5.3L4 15"/><path d="M4 20v-5h5"/></svg>', 'Trainieren', 'Fünf Fragen, eigene Antwort, Wiederholung nach 1, 3 und 7 Tagen.', ''),
        ('test', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="4"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/></svg>', 'Selbsttest', '12 Fragen mit sofortiger Erklärung.', '<span class="hub-note">Bestwert: <b data-v="test">noch offen</b></span><div class="t-meter"><i data-m="test"></i></div>'),
        ('learnings', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/></svg>', 'Learnings', f'{n_learn} Kernsätze mit Erklärung – abhaken, was sitzt.', f'<span class="hub-note"><b data-v="sitzt">0 von {n_learn}</b> sitzen</span><div class="t-meter"><i data-m="sitzt"></i></div>'),
        ('folien', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 16l5-5 4 4 3-3 6 6"/><circle cx="15.5" cy="9" r="1.5"/></svg>', 'Alle Folien', f'{MAKE_N} Make-Folien + {UC_N} Use-Case-Folien im Viewer.', ''),
        ('woerter', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 18l4-12 4 12M5.5 14h5"/><path d="M14 10h6l-6 8h6"/></svg>', 'Wörter', 'Alle Fachbegriffe der Woche mit Suche.', ''),
        ('heft', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h6a3 3 0 0 1 3 3v12a2.5 2.5 0 0 0-2.5-2.5H4z"/><path d="M20 5h-6a3 3 0 0 0-3 3v12a2.5 2.5 0 0 1 2.5-2.5H20z"/></svg>', 'Wochenheft', 'Alles zusammengefasst – lesen im Browser oder als PDF.', ''),
    ]
    tiles_html = ''.join(f'<a class="hub-tile" href="#{tid}" data-tab-go="{tid}"><span class="t-ico" aria-hidden="true">{ico}</span><b>{E(t)}</b><span>{E(x)}</span>{extra}</a>'
                         for tid, ico, t, x, extra in tiles)
    return f'''<section class="tpanel wrap" id="start" role="tabpanel" aria-label="Start">
  <h2 class="hub-h2">Deine Woche in Modul 2</h2>
  <div class="hub-week">{days}</div>
  <h2 class="hub-h2">Alles an einem Ort</h2>
  <div class="hub-grid">{tiles_html}</div>
  <div class="wh">{inhalt.P("**So lernst du heute am besten:** 1. Use-Case-Folien im Kurs mitverfolgen, 2. im Use-Case-Labor deine drei Kandidaten ausfüllen, 3. Vorlagen A7–A9 in Make ausprobieren, 4. zum Schluss 5 Minuten trainieren.")}
  {inhalt.achtung("Speichern", "Alles, was du hier abhakst oder einträgst, bleibt nur in diesem Browser auf diesem Gerät. Für ein anderes Gerät im Use-Case-Labor „Meine Use-Case-Arbeit herunterladen“ nutzen.")}</div>
</section>'''


def render_hub(pid):
    import plattform as P
    import kurs
    import lerntraining
    t = kurs.TAGE[TAG]
    p = kurs.PERSONEN[pid]
    lcards, n_learn = _learnings(pid)
    from .daten import KARTEN, TEST, BEGRIFFE  # der Hub zeigt die ganze Woche, die Tagesdaten verteilen sich auf Tag 1–5
    karten = ''.join(f'<li><b>{E(q)}</b><span>{E(a)}</span></li>' for q, a in KARTEN)
    tests = ''.join(
        f'<li><p class="tq">{E(q)}</p><ol class="to">' +
        ''.join(f'<li{" data-ok" if j == r else ""}>{E(o)}</li>' for j, o in enumerate(opts)) +
        f'</ol><p class="tw"><b>Warum:</b> {E(w)}</p></li>' for q, opts, r, w in TEST)
    words = ''.join(f'<div class="word"><dt>{E(a)}</dt><dd>{E(b)}</dd></div>' for a, b in BEGRIFFE)
    n_fol = MAKE_N + UC_N
    strip = ''.join(f'<a class="v-th" href="/hefte/folien/tag-24/{i:02d}.jpg" data-n="{i}"><img src="/hefte/folien/tag-24/t{i:02d}.jpg" alt="{E(folie_label(i))}" loading="lazy" width="360" height="203"><span>{i}</span></a>'
                    for i in range(1, n_fol + 1))
    fdata = json.dumps({'tag': TAG, 'n': n_fol, 'start': MAKE_N + 1, 'ratio': 1.7778, 'links': {}}, ensure_ascii=False)
    labor_ids = ['c4', 'c6', 'c8', 'c9', 'c10', 'c13']
    teil_c = inhalt.teil_c(pid, web=True)
    labor = ''.join(re.search(rf'<section class="kapitel [^"]*" id="{cid}">.*?</section>', teil_c, re.S).group(0) for cid in labor_ids)
    toc = ''.join(f'<li><b>{E(title)}</b> · ' + ' · '.join(f'<a href="lernheft/#{cid}">{E(lbl)}</a>' for cid, lbl in items[:6]) + (' …' if len(items) > 6 else '') + '</li>'
                  for _, title, items in inhalt.TOC)
    body = f'''<section class="hub-hero"><div class="wrap">
  <p class="kicker">Modul 2 · Woche 1 · Learning Hub · {E(p["name"])}</p>
  <h1>Make-Woche <em>komplett</em> – plus Use Cases.</h1>
  <p class="lead">Heute, Freitag 30.10.: Use Cases identifizieren. Und alles aus Montag bis Donnerstag zum Wiederholen – Wochenheft, 9 fertige Make-Vorlagen, Lernkarten, Selbsttest und Training.</p>
  <div class="hero-btns"><a class="btn primary" href="#labor" data-tab-go="labor">Ins Use-Case-Labor</a><a class="btn" href="#vorlagen" data-tab-go="vorlagen">Make-Vorlagen holen</a><a class="btn" href="#training" data-tab-go="training">5 Minuten trainieren</a><a class="btn" href="lernheft/">Wochenheft lesen</a></div>
  <div class="hub-stats" aria-live="polite">
    <div class="hub-stat"><b data-v="sitzt">0 von {n_learn}</b><span>Learnings sitzen</span></div>
    <div class="hub-stat"><b data-v="test">noch offen</b><span>Selbsttest</span></div>
    <div class="hub-stat"><b><span data-vorlagen-count>0</span> / 9</b><span>Make-Vorlagen erledigt</span></div>
    <div class="hub-stat"><b data-labor-count>0</b><span>Use-Case-Felder ausgefüllt</span></div>
  </div>
</div></section>
<div class="tabs-wrap"><nav class="tabs wrap" role="tablist" aria-label="Bereiche des Learning Hubs">
  <a role="tab" href="#start" data-tab="start">Start</a>
  <a role="tab" href="#labor" data-tab="labor">Use-Case-Labor<span class="tn">heute</span></a>
  <a role="tab" href="#vorlagen" data-tab="vorlagen">Make-Vorlagen<span class="tn">9</span></a>
  <a role="tab" href="#training" data-tab="training">Trainieren</a>
  <a role="tab" href="#learnings" data-tab="learnings">Learnings</a>
  <a role="tab" href="#karten" data-tab="karten">Lernkarten</a>
  <a role="tab" href="#test" data-tab="test">Selbsttest</a>
  <a role="tab" href="#aufgaben" data-tab="aufgaben">Aufgaben</a>
  <a role="tab" href="#folien" data-tab="folien">Folien</a>
  <a role="tab" href="#woerter" data-tab="woerter">Wörter</a>
  <a role="tab" href="#heft" data-tab="heft">Wochenheft</a>
</nav></div>
{_start(pid, n_learn)}
<section class="tpanel wrap" id="labor" role="tabpanel" aria-label="Use-Case-Labor">
  <div class="panel-head"><div><h2>Use-Case-Labor</h2><p>Die vier Arbeitsaufträge von heute zum Ausfüllen – mit Rechner, Nutzen-Check und Entscheidungstreppe. Alles bleibt in diesem Browser; am Ende als Datei herunterladen.</p></div>
  <div class="btnrow"><a class="btn" href="lernheft/#teil-c">Ganzen Teil C lesen</a></div></div>
  <div class="wh">{labor}</div>
</section>
<section class="tpanel wrap" id="vorlagen" role="tabpanel" aria-label="Make-Vorlagen">
  <div class="panel-head"><div><h2>Make-Vorlagen der Woche</h2><p>Neun sehr leichte Automationen als fertige JSON-Dateien. Alle laufen mit Make Free und ohne fremdes Konto. Jede Einstellung ist erklärt.</p></div>
  <div class="btnrow"><a class="btn primary" href="{inhalt.MATERIAL}/{inhalt.ZIP}" download>Alle 9 als ZIP</a></div></div>
  <div class="wh">{inhalt.teil_b(web=True)}</div>
</section>
{lerntraining.panel(pid, TAG, kurs.TAGE)}
<section class="tpanel wrap" id="learnings" role="tabpanel" aria-label="Learnings">
  <div class="panel-head">
    <div><h2>Die Learnings der Woche</h2><p>Ein Satz pro Gedanke – „Nochmal erklärt“ öffnet die einfache Erklärung. Was sitzt, abhaken; was unklar ist, melden.</p></div>
    <div class="btnrow">
      <button class="btn ghost" type="button" data-act="expand">Alle aufklappen</button>
      <button class="btn" type="button" data-lernblatt="{pid}/tag-{TAG}">Alle als PDF</button>
      <button class="btn" type="button" data-lernblatt-sel="{pid}/tag-{TAG}" disabled>Auswahl als PDF</button>
    </div>
  </div>
  <div class="lc-filter" role="group" aria-label="Nach Tag filtern"><button type="button" data-day-filter="" aria-pressed="true">Ganze Woche</button>{"".join(f'<button type="button" data-day-filter="{n}" aria-pressed="false">{wd}</button>' for n, wd, *_ in DAYS)}</div>
  <ol class="lcards">{lcards}</ol>
</section>
<section class="tpanel wrap" id="karten" role="tabpanel" aria-label="Lernkarten">
  <div class="panel-head"><div><h2>Lernkarten</h2><p>{len(KARTEN)} Karten aus der ganzen Woche. Frage lesen, Antwort überlegen, Karte umdrehen. Dann ehrlich einsortieren: gewusst oder nochmal. Tastatur: Leertaste dreht, 1 = nochmal, 2 = gewusst.</p></div></div>
  <div class="deck" data-deck><ol class="karten-src">{karten}</ol></div>
</section>
<section class="tpanel wrap" id="test" role="tabpanel" aria-label="Selbsttest">
  <div class="panel-head"><div><h2>Selbsttest</h2><p>{len(TEST)} kurze Fragen zu Make und Use Cases. Nach jeder Antwort steht sofort da, warum. Nichts wird bewertet – es ist nur für dich.</p></div></div>
  <div class="quiz" data-quiz><ol class="test-src">{tests}</ol></div>
</section>
<section class="tpanel wrap" id="aufgaben" role="tabpanel" aria-label="Aufgaben">
  <div class="panel-head"><div><h2>Aufgabengenerator</h2><p>Freiwillige Übungen zu Use Cases – jedes Mal neu gemischt, mit ausgedachten Firmen aus deinem Bereich. Die Make-Aufgaben stehen bei jeder Vorlage unter „Selbst ändern“.</p></div>
    <div class="btnrow"><a class="btn" href="/hefte/{pid}/aufgaben/">Aus allen Tagen würfeln</a></div></div>
{P.aufg_widget(TAG)}
</section>
<section class="tpanel wrap" id="folien" role="tabpanel" aria-label="Folien">
  <div class="panel-head"><div><h2>Alle Folien der Woche</h2><p>Folien 1–{MAKE_N}: Make-Lektion (Montag bis Donnerstag). Folien {MAKE_N + 1}–{n_fol}: Use Cases (heute, die Ansicht startet dort). Blättern mit Pfeilen, Wischen oder Pfeiltasten.</p></div>
    <div class="btnrow"><a class="btn" href="/hefte/folien/tag-24/{FOLIEN_PDF}" download>Alle Folien als PDF</a></div></div>
  <div class="viewer" data-viewer><script type="application/json" class="v-data">{fdata}</script><div class="v-strip">{strip}</div></div>
</section>
<section class="tpanel wrap" id="woerter" role="tabpanel" aria-label="Wörter">
  <div class="panel-head"><div><h2>Die Wörter der Woche</h2><p>{len(BEGRIFFE)} Fachwörter, jedes in einem einfachen Satz.</p></div></div>
  <label class="sr-only" for="w-such">Wörter durchsuchen</label><input class="words-search" id="w-such" type="search" placeholder="Wort suchen, z. B. Mapping" data-words-search>
  <dl class="words">{words}</dl>
</section>
<section class="tpanel wrap" id="heft" role="tabpanel" aria-label="Wochenheft">
  <div class="hub-heft">
    <div class="cover"><div><p class="kicker" style="color:#05dbba">Wochenheft · Modul 2 · Woche 1</p><h3>Make <em>&amp;</em> Use Cases</h3><p>Alle Grundlagen der Make-Woche, 9 Vorlagen mit Anleitung, der komplette Use-Case-Tag, Spickzettel und Wochenrückblick.</p></div>
      <div class="btnrow"><a class="btn primary" href="lernheft/">Im Browser lesen</a><a class="btn" style="background:transparent;color:#fff;border-color:rgba(255,255,255,.4)" href="/hefte/pdf/{LERNHEFT}?v={VERSION}" download>PDF herunterladen</a></div></div>
    <div><h3>Inhalt</h3><ol>{toc}</ol>
      <p class="hub-note">Die Tageshefte von Montag bis Donnerstag bleiben unverändert erreichbar – das Wochenheft fasst sie zusammen und ergänzt den Freitag.</p>
      <p><a class="btn" href="{inhalt.MATERIAL}/{inhalt.ZIP}" download>Alle Make-Vorlagen (ZIP)</a></p></div>
  </div>
</section>'''
    html = P.page(f'Modul 2 · Learning Hub Woche 1 – {p["name"]}', body, person=pid, tag=TAG, kind='day',
                  scripts=('kurs.js', 'aufgaben.js', 'lerntraining-core.js', 'lerntraining.js', f'wochenheft.js?v={VERSION}'),
                  crumbs=P.crumb(('Lernplattform', '/hefte/'), (p['name'], f'/hefte/{pid}/#modul-2'), ('Modul 2 · Tag 5 · Hub', '')))
    html = _inline_css(html)
    return html.replace('</head>', f'<style id="wochenhub">{FONT_FACES}{CONTENT_CSS}{HUB_CSS}.sr-only{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}</style>\n</head>', 1)


def _nav():
    out = ''
    for tid, title, items in inhalt.TOC:
        out += f'<p><a href="#{tid}" style="padding:0;color:inherit">{E(title)}</a></p><ol>' + ''.join(f'<li><a href="#{cid}">{E(lbl)}</a></li>' for cid, lbl in items) + '</ol>'
    return out


def wochenheft_body(pid, web=True):
    return inhalt.teil_a() + inhalt.teil_b(web) + inhalt.teil_c(pid, web) + inhalt.teil_d()


def render_web(pid):
    name = NAMES[pid]
    app_css = (ASSETS / 'app.css').read_text(encoding='utf8').replace('url(fonts/', 'url(/hefte/assets/fonts/')
    return f'''<!doctype html><html lang="de" data-person="{pid}" data-tag="{TAG}" data-page="wochenheft"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>{E(name)} · Wochenheft Modul 2 · Make &amp; Use Cases</title><link rel="icon" href="/hefte/assets/favicon.svg">
<style>{app_css}{FONT_FACES}{READ_CSS}{CONTENT_CSS}</style>
<script src="/hefte/assets/app.js" defer></script><script src="/hefte/assets/wochenheft.js?v={VERSION}" defer></script></head><body>
<a class="skip" href="#main">Zum Inhalt</a>
<header class="rd-top"><div class="rd-top-in"><a href="/hefte/{pid}/modul-2/tag-5/">← Learning Hub</a><span>{E(name)} · Wochenheft Modul 2 · Woche 1 · 26.–30.10.2026</span><a class="rd-pdf" href="/hefte/pdf/{LERNHEFT}?v={VERSION}" download>PDF</a></div></header>
<section class="rd-cover"><div class="rd-cover-in"><p class="eyebrow">Wochenheft · Modul 2 · KI-Automation · Woche 1</p>
<h1>Make <em>verstehen</em>, Use Cases <em>finden</em>.</h1>
<p>Alles aus Montag bis Donnerstag in einem Heft – aktuell zum Stand Oktober 2026 und in Alltagssprache erklärt. Dazu neun fertige Make-Vorlagen zum Importieren und der komplette Freitag: Use Cases identifizieren.</p>
<div class="rd-btns"><a class="btn primary" href="#teil-a">Lesen starten</a><a class="btn" href="#teil-b">Make-Vorlagen</a><a class="btn" href="#teil-c">Use Cases</a><a class="btn" href="/hefte/{pid}/modul-2/tag-5/#karten">Lernkarten</a></div></div></section>
<div class="rd-layout"><nav class="rd-nav" aria-label="Inhalt des Wochenhefts">{_nav()}</nav>
<main id="main" class="wh"><p class="rd-hint"><b>So nutzt du das Heft:</b> Teil A lesen, Teil B in Make ausprobieren, Teil C heute im Kurs ausfüllen. Eingaben bleiben in diesem Browser. Lernkarten, Selbsttest und Training findest du im <a href="/hefte/{pid}/modul-2/tag-5/">Learning Hub</a>.</p>
{wochenheft_body(pid, True)}</main></div></body></html>'''


def render_print():
    toc = ''.join(f'<div><b>{E(title)}</b><ol>' + ''.join(f'<li>{E(lbl)}</li>' for _, lbl in items) + '</ol></div>' for _, title, items in inhalt.TOC)
    logo = (ROOT / 'plattform/public/assets/futureway_logo.png').as_uri()
    fonts = FONT_FACES.replace('url(/hefte/assets/fonts/', 'url(' + (ASSETS / 'fonts').as_uri() + '/')
    archivo = (ASSETS / 'app.css').read_text(encoding='utf8').split('.nw')[0].replace('url(fonts/', 'url(' + (ASSETS / 'fonts').as_uri() + '/')
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Wochenheft Modul 2 · Woche 1 · Make &amp; Use Cases</title>
<style>{archivo}{fonts}{CONTENT_CSS}{PRINT_CSS}</style></head><body>
<section class="pr-cover"><img src="{logo}" alt="Futureway KI Institut"><p class="eyebrow">Wochenheft · Modul 2 · KI-Automation · Woche 1</p>
<h1>Make <em>verstehen</em>,<br>Use Cases <em>finden</em>.</h1>
<p>Montag bis Donnerstag zusammengefasst, Stand Oktober 2026, in Alltagssprache erklärt. Neun fertige Make-Vorlagen mit vollständiger Anleitung. Freitag, 30.10.2026: Use Cases identifizieren – mit allen Arbeitsaufträgen zum Ausfüllen.</p>
<div class="pr-meta"><div><b>66</b><span>Originalfolien begleitet</span></div><div><b>9</b><span>Make-Vorlagen (JSON)</span></div><div><b>4</b><span>Arbeitsaufträge</span></div><div><b>1</b><span>Spickzettel</span></div></div></section>
<section class="pr-toc"><h2>Inhalt</h2><div class="t">{toc}</div>
<p style="margin-top:8mm;font-size:9.5pt;color:#5c6360">Online mit Lernkarten, Selbsttest, Training und Download der Vorlagen: quint-games.de/hefte → eigener Name → Modul 2 → Tag 5. Alle Beispiele erfunden. Credit-Angaben sind Planwerte.</p></section>
<div class="wh">{wochenheft_body(None, False)}</div></body></html>'''


BANNER_CSS = ('.hub-banner{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:space-between;margin:0 0 22px;padding:16px 18px;'
              'border-radius:16px;background:linear-gradient(120deg,#032a21,#05614c);color:#fff;font-family:Archivo,system-ui,sans-serif}'
              '.hub-banner p{margin:0;color:#fff;max-width:62ch;line-height:1.45}.hub-banner b{color:#05dbba}'
              '.hub-banner nav{display:flex;flex-wrap:wrap;gap:8px}.hub-banner a{color:#032a21;background:#05dbba;border-radius:999px;padding:7px 13px;'
              'font-weight:700;font-size:14px;text-decoration:none}.hub-banner a.alt{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.35)}')


def banner(pid, day):
    """Hinweis auf den Learning Hub für die Tagesseiten und Lernhefte Montag bis Donnerstag."""
    vorl = next(v for n, *_, v in DAYS if n == day)
    hub = f'/hefte/{pid}/modul-2/tag-5/'
    links = ''.join(f'<a href="{hub}#vorlage-a{a}">Make-Vorlage A{a}</a>' for a in vorl)
    return (f'<style>{BANNER_CSS}</style><aside class="hub-banner" aria-label="Neu im Learning Hub"><p><b>Neu:</b> Für diesen Tag gibt es jetzt '
            f'eine fertige Make-Vorlage zum Importieren – plus Lernkarten, Selbsttest und Training für die ganze Woche im Learning Hub.</p>'
            f'<nav>{links}<a class="alt" href="{hub}#karten">Lernkarten</a><a class="alt" href="{hub}#test">Selbsttest</a><a class="alt" href="{hub}">Learning Hub</a></nav></aside>')


def mit_banner(html, pid, day):
    assert html.count('<main id="main">') == 1
    return html.replace('<main id="main">', '<main id="main">' + banner(pid, day), 1)
