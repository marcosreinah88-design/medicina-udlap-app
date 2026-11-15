#!/usr/bin/env python3
# Búsqueda avanzada en el buscador de la portada: botón «Búsqueda avanzada» bajo la barra con filtros
# de semestre, materia y apartado (Fisiopatología, Epidemiología, Tratamiento, Posología…), cada uno con
# cuántas guías daría; se combinan con la palabra buscada y se pueden limpiar. Sin filtros busca igual que antes.
# Fuente del buscador: tools-buscador/avanzada.js · índice de apartados: node tools-buscador/apartados.js
# Uso: python3 tools-buscador/patch_avanzada.py site/index.html site/app.html [artefacto.html]   (idempotente)
import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = '/*busqueda-avanzada-v2*/'
START = '/* buscador: materias, temas y palabras clave de todas las guías */'
END = '/* modo oscuro: botón en la portada'

CSS = '''/*adv-css*/
.adv{margin:10px 2px 0}
.adv-t{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);background:var(--paper);color:var(--green-3);border-radius:999px;padding:6px 13px;font:700 .84rem var(--f-display);cursor:pointer;transition:border-color .2s,color .2s}
.adv-t:hover,.adv-t[aria-expanded=true]{border-color:var(--orange);color:var(--orange-2)}
.adv-t svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round}
.adv-t[aria-expanded=true] .cv{transform:rotate(180deg)}.adv-t .cv{transition:transform .2s}
.adv-n{display:inline-grid;place-items:center;min-width:19px;height:19px;padding:0 5px;border-radius:999px;background:var(--orange);color:#fff;font:700 .7rem var(--f-mono)}
.adv-n[hidden]{display:none}
.adv-p{margin-top:10px;background:var(--paper);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);padding:14px 16px 12px;display:grid;gap:12px;animation:advIn .22s ease-out}
.adv-p[hidden]{display:none}
@keyframes advIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}
.adv-g>.mono{display:block;color:var(--orange-2);font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;margin-bottom:6px}
.adv-h{margin:-2px 0 7px;color:var(--muted);font-size:.8rem;line-height:1.35}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:999px;padding:5px 6px 5px 11px;font:600 .8rem var(--f-display);cursor:pointer;min-height:32px;transition:background .15s,border-color .15s,opacity .15s}
.chip:hover{border-color:var(--green-3)}
.chip .cn{min-width:20px;padding:1px 6px;border-radius:999px;background:var(--paper);color:var(--muted);font:600 .68rem var(--f-mono);text-align:center}
.chip[aria-pressed=true]{background:var(--green-3);border-color:var(--green-3);color:#fff}
.chip[aria-pressed=true] .cn{background:rgba(255,255,255,.2);color:#fff}
.chip.zero{opacity:.45}
.adv-load{color:var(--muted);font-size:.82rem}
.adv-f{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;border-top:1px dashed var(--line);padding-top:10px}
.adv-f span{color:var(--muted);font-size:.8rem;line-height:1.35;flex:1 1 200px}
.adv-f button{border:1px solid var(--orange);background:transparent;color:var(--orange-2);border-radius:999px;padding:5px 12px;font:700 .8rem var(--f-display);cursor:pointer}
.adv-f button[hidden]{display:none}
.rfl{display:block;margin-top:3px;color:var(--orange-2);font-size:.78rem}
.rcard .rap span{cursor:pointer;display:inline-flex;flex-wrap:wrap;align-items:baseline;gap:5px}
.rcard .rap span:hover,.rcard .rap span:focus-visible{border-color:var(--c);outline:none}
.rcard .rap i{font-style:normal;font:700 .64rem var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--orange-2)}
.rclr{border:1px solid var(--orange);background:transparent;color:var(--orange-2);border-radius:999px;padding:3px 11px;font:700 .8rem var(--f-display);cursor:pointer;margin-left:4px}
@media (max-width:480px){.adv-p{padding:12px}.chip{font-size:.78rem}}
'''

HTML_AFTER = '<button class="clr" id="qc" type="button" hidden aria-label="Borrar búsqueda">Esc ✕</button></div>'
HTML = '''
    <div class="adv" id="adv"><button class="adv-t" id="advT" type="button" aria-expanded="false" aria-controls="advP"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M7 12h10M10 18h4"/></svg>Búsqueda avanzada<span class="adv-n" id="advN" hidden></span><svg class="cv" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
    <div class="adv-p" id="advP" hidden role="group" aria-label="Filtros de búsqueda">
      <div class="adv-g"><span class="mono">Apartado o subtema</span><p class="adv-h">Busca la palabra solo dentro de esa parte de cada tema (por ejemplo, «omeprazol» solo en Posología y dosis).</p><div class="chips" data-f="ap"></div></div>
      <div class="adv-g"><span class="mono">Materia</span><div class="chips" data-f="mat"></div></div>
      <div class="adv-g"><span class="mono">Semestre</span><div class="chips" data-f="sem"></div></div>
      <div class="adv-f"><span id="advS">Sin filtros: busca en toda la carrera.</span><button type="button" id="advClr" hidden>Limpiar filtros</button></div>
    </div></div>'''


def patch(path):
    s = open(path, encoding='utf8').read()
    o = s
    if '/*adv-css*/' in s:
        i = s.index('/*adv-css*/')
        j = s.index('.rnone{', i)
        s = s[:i] + s[j:]
    i = s.index('.rnone{')
    s = s[:i] + CSS + s[i:]
    assert s.count(HTML_AFTER) == 1, 'no encontré la barra de búsqueda'
    if 'id="advT"' in s:
        i = s.index(HTML_AFTER) + len(HTML_AFTER)
        j = s.index('</div></div>', s.index('id="advClr"')) + len('</div></div>')
        s = s[:i] + s[j:]
    s = s.replace(HTML_AFTER, HTML_AFTER + HTML)
    js = open(os.path.join(HERE, 'avanzada.js'), encoding='utf8').read().rstrip('\n') + '\n'
    a = s.index(START)
    b = s.index(END, a)
    if s[a:b] != js:
        s = s[:a] + js + s[b:]
    if s != o:
        open(path, 'w', encoding='utf8').write(s)
        print('parchado', path)
    else:
        print('ya estaba', path)


for p in sys.argv[1:] or ['site/index.html', 'site/app.html']:
    patch(p)
