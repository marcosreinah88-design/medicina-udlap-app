# Arma site/casos/<guía>.json (casos clínicos tipo examen de las guías de 5º) desde tools-casos/casos/*.txt
# y conecta site/casos.js a cada guía (botón flotante «Casos clínicos»). Idempotente.
# Uso: python3 tools-casos/build.py [carpeta del sitio]   (por omisión site/; sirve igual para la copia del artefacto)
# Después: node tools-estudio/banco.js (los casos también entran a Estudio → modo examen) y firmar.
#
# Formato de cada archivo (una línea por dato; líneas vacías y // se ignoran):
#   # Tema               (tal cual se llama en la guía; agrupa los casos)
#   ## Título del caso   (corto: lo que se ve en la revisión)
#   C viñeta clínica     (puede ir en varias líneas C seguidas)
#   P pregunta
#   * respuesta correcta :: por qué es la correcta
#   - distractor :: por qué no
#   E perla final (opcional)
#   **negritas**; † = no viene en los apuntes de la guía.
import os, re, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'site')

# guía → (archivo de casos, temas que le tocan o None = todos, nombre que se muestra, archivo de la guía)
GASTRO_ESOF = ['ERGE y trastornos motores del esófago', 'Acalasia', 'Enfermedad ácido-péptica (úlcera péptica)', 'Gastroparesia',
               'Esófago de Barrett', 'Infección por Helicobacter pylori', 'Sangrado de tubo digestivo alto', 'Dispepsia funcional']
GASTRO_HEPATO = ['Hepatitis virales de la A a la E', 'Hepatitis autoinmune', 'Colangitis biliar primaria', 'Cirrosis: prevenir la descompensación y la muerte',
                 'Hipertensión portal y cirrosis descompensada: Baveno VIII', 'Litiasis biliar', 'Colangitis aguda: guías de Tokio 2018', 'Pancreatitis aguda',
                 'Pruebas de función hepática alteradas', 'Enfermedad hepática esteatósica asociada a disfunción metabólica (MASLD)',
                 'Detección y referencia oportuna del cáncer gastrointestinal (AMG)']
GUIAS = {
    'gastro':       ('gastro.txt', None, 'Gastroenterología', 's5/gastro/index.html'),
    'esofago':      ('gastro.txt', GASTRO_ESOF, 'Esófago y estómago', 's5/esofago/index.html'),
    'hepatobiliar': ('gastro.txt', GASTRO_HEPATO, 'Hígado, vías biliares y páncreas', 's5/hepatobiliar/index.html'),
    'cirugia':      ('cirugia.txt', None, 'Cirugía', 's5/cirugia/index.html'),
    'imagenologia': ('imagenologia.txt', None, 'Imagenología', 's5/imagenologia/index.html'),
    'oftalmo':      ('oftalmo.txt', None, 'Oftalmología', 's5/oftalmo/index.html'),
    'otorrino':     ('otorrino.txt', None, 'Otorrinolaringología', 's5/otorrino/index.html'),
    'psiquiatria':  ('psiquiatria.txt', None, 'Psiquiatría', 's5/psiquiatria/index.html'),
}

def parse(path):
    casos, tema, c = [], None, None
    def fin():
        if c is None: return
        w = f"{path}: caso «{c['h']}»"
        if not c['v'] or not c['q']: raise SystemExit(w + ': falta viñeta (C) o pregunta (P)')
        if len(c['o']) < 4 or c['o'][0][2] != '*' or sum(o[2] == '*' for o in c['o']) != 1:
            raise SystemExit(w + ': necesita una sola correcta (*) en primer lugar y al menos 3 distractores (-)')
        casos.append({'id': 'c' + hashlib.sha1((tema + '|' + c['h']).encode()).hexdigest()[:8], 't': tema, 'h': c['h'],
                      'v': ' '.join(c['v']), 'q': c['q'], 'o': [[o[0], o[1]] for o in c['o']], 'e': c['e']})
    for n, raw in enumerate(open(path, encoding='utf-8'), 1):
        line = raw.strip()
        if not line or line.startswith('//'): continue
        if line.startswith('##'):
            fin(); c = {'h': line[2:].strip(), 'v': [], 'q': '', 'o': [], 'e': ''}
            if tema is None: raise SystemExit(f'{path}:{n}: caso fuera de un tema')
            continue
        k, rest = line[0], line[1:].strip()
        if k == '#': fin(); c = None; tema = rest; continue
        if c is None: raise SystemExit(f'{path}:{n}: línea fuera de un caso')
        if k == 'C': c['v'].append(rest)
        elif k == 'P': c['q'] = rest
        elif k in '*-':
            txt, _, why = rest.partition('::'); c['o'].append([txt.strip(), why.strip(), k])
        elif k == 'E': c['e'] = rest
        else: raise SystemExit(f'{path}:{n}: no entiendo la línea: {line[:40]}')
    fin()
    ids = [x['id'] for x in casos]
    if len(ids) != len(set(ids)): raise SystemExit(f'{path}: dos casos con el mismo tema y título')
    return casos

TAG = re.compile(r'<script src="[^"]*casos\.js"[^>]*></script><!--casos-->')
os.makedirs(os.path.join(SITE, 'casos'), exist_ok=True)
cache = {}
for g, (src, temas, nombre, page) in GUIAS.items():
    casos = cache.get(src) or cache.setdefault(src, parse(os.path.join(HERE, 'casos', src)))
    if temas:
        falta = [t for t in temas if t not in {c['t'] for c in casos}]
        if falta: print('  aviso', g, 'sin casos de:', '; '.join(falta))
        casos = [c for c in casos if c['t'] in temas]
        casos.sort(key=lambda c: temas.index(c['t']))
    json.dump({'g': g, 'n': nombre, 'c': casos}, open(os.path.join(SITE, 'casos', g + '.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, separators=(',', ':'))
    p = os.path.join(SITE, page)
    if not os.path.isfile(p): print('  falta', page); continue
    s = TAG.sub('', open(p, encoding='utf-8').read())
    tag = f'<script src="../../casos.js" data-cc="{g}" data-n="{len(casos)}" defer></script><!--casos-->'
    i = s.rfind('</body>')
    s = s[:i] + tag + s[i:] if i >= 0 else s + tag
    open(p, 'w', encoding='utf-8').write(s)
    print(f'{g:13} {len(casos):3} casos, {len({c["t"] for c in casos}):2} temas')
