# Agrega las guías nuevas de 3º (armadas por build.py en site/s3/<id>/index.html) al archivero original de 3º.
# - ITEMS: una entrada por guía (bloque marcado /*s3guias:items*/), antes de las tarjetas de Anki.
# - Portadas con el estilo del archivero (bloque CSS /*s3guias:css*/ y ramas en cover()).
# - Nota al pie con las materias de formación general que no tienen guía.
# Idempotente. Uso: python3 tools-s12/patch_s3.py [ruta/a/s3/index.html ...]   (sin argumentos: site/s3/index.html)
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')
hub = json.load(open(os.path.join(HERE, 'hub.json'), encoding='utf-8'))
js = lambda v: json.dumps(v, ensure_ascii=False)

# portada de cada guía: (etiqueta, título con <i>, dibujo SVG)
ECG = '<svg class="dw" viewBox="0 0 200 60" aria-hidden="true"><path d="M0 34h46l6-10 6 10h10l5 8 7-38 8 46 6-16h18l8-12 9 12h71" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/></svg>'
MIC = ('<svg class="dw" viewBox="0 0 200 60" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.5">'
       '<circle cx="120" cy="22" r="9"/><circle cx="138" cy="30" r="9"/><circle cx="124" cy="40" r="9"/>'
       '<rect x="154" y="14" width="34" height="14" rx="7"/><rect x="160" y="36" width="34" height="14" rx="7" transform="rotate(-18 177 43)"/>'
       '<path d="M96 48c8-10 14 2 22-6"/></g></svg>')
SIM = ('<svg class="dw" viewBox="0 0 200 60" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.5">'
       '<rect x="150" y="2" width="30" height="26" rx="6"/><path d="M165 28v8"/><path d="M161 36h8l-1 8h-6z"/><path d="M165 44c0 10-30 6-40 14"/></g>'
       '<path d="M165 50c-3 4-3 6 0 8 3-2 3-4 0-8z" fill="currentColor"/></svg>')
PRO = ('<svg class="dw" viewBox="0 0 200 60" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">'
       '<path d="M120 4v18a16 16 0 0 0 32 0V4"/><path d="M136 38v6a14 14 0 0 0 28 0v-8"/><circle cx="164" cy="30" r="6"/></g></svg>')
COVERS = {
    'fisiologia-clinica': ('FCL · Fisiopatología', 'Fisiología <i>Clínica</i>', ECG),
    'microbiologia': ('MIC · Bacterias, virus y parásitos', 'Microbiología <i>y Parasitología</i>', MIC),
    'simulacion-iii': ('SIM · Laboratorio', 'Simulación <i>III</i>', SIM),
    'propedeutica': ('PRO · Semiología', 'Propedéutica', PRO),
}
FEATS = ['Resumen por tema', 'Diagramas', 'Alto rendimiento', 'Tarjetas', 'Examen']
NOTA = ('Italiano I (Lengua Extranjera III), Escritura Académica y Ética, Sociedad y Medio Ambiente son materias de formación general: '
        'no tienen guía, igual que en 1º y 2º. Ecosofía conserva solo sus tarjetas de Anki.')

CSS = ('/*s3guias:css*/\n'
       '.cv-g{background:var(--gc);color:#fff}\n'
       '.cv-g .big{font-family:var(--display);font-size:40px;line-height:1.02}\n'
       '.cv-g .big i{font-style:italic;opacity:.85}\n'
       '.cv-g .dw{position:absolute;right:14px;top:16px;width:58%;max-width:230px;height:auto;color:rgba(255,255,255,.55)}\n'
       '/*/s3guias:css*/\n')
COVER_JS = ('  /*s3guias:cover*/if(it.cover==="g") return `<div class="cover cv-g" style="--gc:${it.gc}"><span class="tag">${esc(it.tag)}</span>${it.dw}<span class="big">${it.big}</span></div>`;/*/s3guias:cover*/\n')

def entries():
    out = []
    for g in hub['G']:
        if g['sem'] != 3 or g['id'] not in COVERS:
            continue
        tag, big, dw = COVERS[g['id']]
        st = {k: int(v) for v, k in g['stats']}
        out.append(' {id:%s,src:%s,materia:%s,title:%s,desc:%s,feats:%s,stats:%s,cover:"g",gc:%s,tag:%s,big:%s,dw:%s,keys:%s}'
                   % (js(g['id']), js(g['id'] + '/index.html'), js(g['area']), js(g['title']), js(g['desc']), js(FEATS),
                      js(st), js(g['color']), js(tag), js(big), js(dw), js(' '.join(g['toc']).lower() + ' ' + g['kw'])))
    return out

def patch(path):
    s = open(path, encoding='utf-8').read()
    # 1) ITEMS
    s = re.sub(r' ,/\*s3guias:items\*/.*?/\*/s3guias:items\*/\n?', '', s, flags=re.S)
    blk = ' ,/*s3guias:items*/\n' + ',\n'.join(entries()) + '\n /*/s3guias:items*/\n'
    anchor = ' ,/*anki:items*/' if ' ,/*anki:items*/' in s else '\n];\n\nconst $=s=>'
    i = s.index(anchor)
    s = s[:i] + blk + s[i:]
    # 2) CSS de portadas
    s = re.sub(r'/\*s3guias:css\*/.*?/\*/s3guias:css\*/\n', '', s, flags=re.S)
    s = s.replace('/* visor */', CSS + '\n/* visor */', 1)
    # 3) cover()
    s = re.sub(r'  /\*s3guias:cover\*/.*?/\*/s3guias:cover\*/\n', '', s, flags=re.S)
    s = s.replace('function cover(it){\n', 'function cover(it){\n' + COVER_JS, 1)
    # 4) nota al pie
    s = re.sub(r'\n  <p class="foot" data-s3guias>.*?</p>', '', s, flags=re.S)
    s = s.replace('</p>\n</div>\n\n<div class="viewer"', '</p>\n  <p class="foot" data-s3guias>' + NOTA + '</p>\n</div>\n\n<div class="viewer"', 1)
    # placeholder del buscador
    s = s.replace('placeholder="Buscar: farmacología, irrigación, quiz…"', 'placeholder="Buscar: arritmias, Gram, gasometría, marchas…"')
    open(path, 'w', encoding='utf-8').write(s)
    print(path, 'ok', len(entries()), 'guías')

for p in sys.argv[1:] or [os.path.join(SITE, 's3', 'index.html')]:
    patch(p)
