"""Kleine HTML-Bausteine für das Wochenheft (Web und Druck teilen dasselbe HTML)."""
import html
import re


def E(s):
    return html.escape(str(s), quote=True)


def md(s):
    """Escaped Text mit **fett**, `code` und Zeilenumbrüchen."""
    t = E(s)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    t = re.sub(r'~~(.+?)~~', r'<s>\1</s>', t)
    return t.replace('\n', '<br>')


def P(*texts):
    return ''.join(f'<p>{md(t)}</p>' for t in texts)


def H(text, level=3):
    return f'<h{level}>{md(text)}</h{level}>'


def merk(text):
    return f'<div class="merk"><span class="lbl">Merksatz</span><p>{md(text)}</p></div>'


def achtung(title, text):
    return f'<div class="achtung"><span class="lbl">{E(title)}</span><p>{md(text)}</p></div>'


def tipp(title, text):
    return f'<div class="tipp"><span class="lbl">{E(title)}</span><p>{md(text)}</p></div>'


def korrektur(ref, text):
    return (f'<div class="korrektur"><span class="lbl">Präzisierung zu {E(ref)}</span>'
            f'<p>{md(text)}</p></div>')


def beispiel(title, text):
    return f'<div class="beispiel"><span class="lbl">{E(title)}</span><p>{md(text)}</p></div>'


def tab(head, rows, cls=''):
    th = ''.join(f'<th scope="col">{md(h)}</th>' for h in head)
    body = ''.join('<tr>' + ''.join(f'<td data-label="{E(head[i])}">{md(c)}</td>' for i, c in enumerate(r)) + '</tr>'
                   for r in rows)
    return f'<div class="tab-wrap"><table class="tab {cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def flow(items, cls=''):
    lis = ''.join(f'<li><b>{md(a)}</b>{f"<span>{md(b)}</span>" if b else ""}</li>' for a, b in items)
    return f'<ol class="flow {cls}">{lis}</ol>'


def karten(items, cols=3, cls=''):
    cards = ''.join(f'<div class="karte">{f"<span class=num>{E(n)}</span>" if n else ""}<h4>{md(t)}</h4><p>{md(x)}</p></div>'
                    for n, t, x in items)
    return f'<div class="karten c{cols} {cls}">{cards}</div>'


def glossar(items):
    rows = ''.join(f'<div class="g-row"><dt>{md(a)}</dt><dd>{md(b)}{f"<small>{md(c)}</small>" if c else ""}</dd></div>'
                   for a, b, c in items)
    return f'<dl class="glossar">{rows}</dl>'


def details(summary, inner, cls=''):
    return f'<details class="mehr {cls}"><summary>{md(summary)}</summary><div class="mehr-in">{inner}</div></details>'


def code(text, label=''):
    lab = f'<span class="code-lbl">{E(label)}</span>' if label else ''
    return f'<div class="code">{lab}<pre>{E(text)}</pre></div>'


def folien(*refs):
    """Hinweis auf Originalfolien: ('make', 7) oder ('uc', 12)."""
    parts = []
    for deck, n in refs:
        nr, label = (n, f'Make-Folie {n}') if deck == 'make' else (34 + n, f'Use-Case-Folie {n}')
        parts.append(f'<a href="/hefte/folien/tag-24/{nr:02d}.jpg" target="_blank" rel="noopener" data-folie="{nr}">{label}</a>')
    return '<p class="folien-ref">Originalfolien: ' + ' · '.join(parts) + '</p>'


def kapitel(cid, nr, kicker, title, body, cls=''):
    return (f'<section class="kapitel {cls}" id="{E(cid)}"><header class="k-head"><span class="k-nr">{E(nr)}</span>'
            f'<div><p class="k-kicker">{E(kicker)}</p><h2>{md(title)}</h2></div></header>{body}</section>')


def teil(tid, buchstabe, title, intro, inner):
    return (f'<div class="teil" id="{E(tid)}"><div class="teil-kopf"><span class="teil-b">{E(buchstabe)}</span>'
            f'<div><h2 class="teil-t">{md(title)}</h2><p>{md(intro)}</p></div></div>{inner}</div>')
