"""Suma al buscador de la portada (lista FT["oftalmo"]) las palabras del contenido de diag_temas.py.
Uso: python3 tools-oftalmo/buscador_oftalmo.py site/index.html site/app.html [artefacto.html]   (idempotente)
"""
import sys, os, re, unicodedata, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import diag_temas as D  # noqa: E402


def fold(s):
    s = unicodedata.normalize('NFD', html.unescape(s))
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()


txt = []
for grp in (D.B6, D.B5):
    for t, _, b in grp:
        txt += [t, re.sub(r'<[^>]+>', ' ', b)]
for t, v, qs in D.CASOS:
    txt += [t, v] + [q + ' ' + ' '.join(o) + ' ' + e for q, o, _, e in qs]
txt += [' '.join(c) for c in D.CARDS] + [D.CASOS_T]
new = set(re.findall(r'[a-z]{4,}', fold(' '.join(txt))))

for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    m = re.search(r'"oftalmo": "([^"]*)"', s)
    old = set(m.group(1).split())
    words = ' '.join(sorted(old | new))
    s = s[:m.start(1)] + words + s[m.end(1):]
    open(p, 'w', encoding='utf-8').write(s)
    print(p, len(old), '→', len(old | new), 'palabras')
