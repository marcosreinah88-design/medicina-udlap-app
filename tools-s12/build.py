# Arma las guías y las páginas de 1º y 2º semestre a partir de tools-s12/guias/*.txt
# Uso: python3 tools-s12/build.py            → escribe site/s1/, site/s2/ y tools-s12/hub.json
# Después: python3 tools-s12/patch_hub.py (conecta los semestres al hub), node tools-estudio/banco.js y firmar.
#
# Formato de cada guía (una línea por dato):
#   @id, @sem, @title, @materia, @codigo, @color, @sub, @desc, @kw, @nota, @extra, @orden, @modos
#   # Título del tema          > introducción corta (del tema, o del subtema si va después de ##)
#   ## Subtema
#   - punto del temario         ! dato de alto rendimiento     + correlación clínica
#   = Título :: paso → paso    (diagrama de flujo; el título es opcional)
#   % cifra :: qué significa   (cifras clave)       ~ término :: definición (conceptos para revelar)
#   & MNEMOTECNIA :: qué significa
#   | col ¦ col ¦ col          (tabla; la primera fila es el encabezado)
#   ? frente :: reverso        (tarjeta)
#   Q pregunta :: *correcta :: distractor :: distractor || explicación
#   **negritas**; † marca lo que se agregó para completar el tema.
import os, re, json, glob, html, random, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')

def inline(s):
    s = html.escape(s.strip(), quote=False)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)

def parse(path):
    g = {'temas': [], 'modos': 'Estudiar,Tarjetas,Examen'}
    t = sub = None
    def block(k):
        # agrega al último bloque del subtema si es del mismo tipo; si no, abre uno nuevo
        nonlocal sub
        if sub is None:
            sub = {'t': '', 'b': []}
            t['subs'].append(sub)
        if not sub['b'] or sub['b'][-1]['k'] != k or k == 'fl':
            sub['b'].append({'k': k, 'x': []})
        return sub['b'][-1]['x']
    for n, raw in enumerate(open(path, encoding='utf-8'), 1):
        line = raw.rstrip('\n')
        if not line.strip() or line.lstrip().startswith('//'):
            continue
        if line.startswith('##'):
            if t is None:
                raise SystemExit(f'{path}:{n}: subtema fuera de un tema')
            sub = {'t': inline(line[2:]), 'b': []}
            t['subs'].append(sub)
            continue
        k, rest = line[0], line[1:].strip()
        if k == '@':
            key, _, val = rest.partition(' ')
            g[key] = val.strip()
        elif k == '#':
            t = {'t': rest, 'subs': [], 'cards': [], 'quiz': []}
            sub = None
            g['temas'].append(t)
        elif t is None:
            raise SystemExit(f'{path}:{n}: línea fuera de un tema')
        elif k == '>':
            if sub is None:
                t['intro'] = inline(rest)
            else:
                sub['i'] = inline(rest)
        elif k == '-':
            block('ul').append(inline(rest))
        elif k == '!':
            block('hy').append(inline(rest))
        elif k == '+':
            block('cl').append(inline(rest))
        elif k == '|':
            block('tb').append('¦'.join(inline(c) for c in rest.split('¦')))
        elif k == '=':
            # diagrama de flujo: "= Título :: paso → paso → paso" (título opcional)
            ttl, _, steps = rest.rpartition('::')
            x = block('fl')
            x.append(inline(ttl) if ttl else '')
            x += [inline(p) for p in steps.split('→')]
        elif k == '%':
            v, _, l = rest.partition('::')
            if not l:
                raise SystemExit(f'{path}:{n}: cifra sin "::"')
            block('st').append({'v': inline(v), 'l': inline(l)})
        elif k == '~':
            w, _, d = rest.partition('::')
            if not d:
                raise SystemExit(f'{path}:{n}: concepto sin "::"')
            block('tm').append({'w': inline(w), 'd': inline(d)})
        elif k == '&':
            m, _, d = rest.partition('::')
            block('mn').append({'m': inline(m), 's': inline(d)})
        elif k == '?':
            f, _, b = rest.partition('::')
            if not b:
                raise SystemExit(f'{path}:{n}: tarjeta sin "::"')
            t['cards'].append({'f': inline(f), 'b': inline(b)})
        elif k == 'Q':
            body, _, exp = rest.partition('||')
            parts = [p.strip() for p in body.split('::')]
            q, opts = parts[0], parts[1:]
            if len(opts) < 3 or not opts[0].startswith('*'):
                raise SystemExit(f'{path}:{n}: la pregunta necesita 3+ opciones y la correcta primero con *')
            opts[0] = opts[0][1:]
            rnd = random.Random(q)
            order = list(range(len(opts)))
            rnd.shuffle(order)
            t['quiz'].append({'q': inline(q), 'o': [inline(opts[i]) for i in order], 'a': order.index(0), 'e': inline(exp)})
        else:
            raise SystemExit(f'{path}:{n}: no entiendo la línea: {line[:60]}')
    for t in g['temas']:
        for key in ('cards', 'quiz'):
            if not t[key]:
                del t[key]
    g['sem'] = int(g['sem'])
    g['orden'] = int(g.get('orden', 50))
    return g

def nsubs(g):
    return sum(sum(1 for s in t['subs'] if s['t']) for t in g['temas'])

def fold(s):
    s = unicodedata.normalize('NFD', s)
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()

def words(g):
    txt = [g['title'], g.get('desc', '')]
    for t in g['temas']:
        txt.append(t['t'])
        txt += [t.get('intro', '')]
        for sb in t['subs']:
            txt += [sb['t'], sb.get('i', '')]
            for b in sb['b']:
                for x in b['x']:
                    txt += list(x.values()) if isinstance(x, dict) else [x]
        for c in t.get('cards', []):
            txt += [c['f'], c['b']]
        for q in t.get('quiz', []):
            txt += [q['q'], q['e']] + q['o']
    plain = re.sub(r'<[^>]+>', ' ', ' '.join(txt))
    return ' '.join(sorted({w for w in re.findall(r'[a-z0-9]+', fold(html.unescape(plain))) if len(w) >= 3 and not w.isdigit()}))

SEMS = {
    1: dict(title='1er semestre', kicker='Primer semestre', back='Mesa', bodyclass='slides',
            layout='Layout: mesa de laboratorio. Cada guía es un portaobjetos (etiqueta de color + muestra); al abrir una, ocupa toda la pantalla.',
            lede='Ciencias básicas morfológicas y moleculares: histología, bioquímica, anatomofisiología, embriología y genética. Cada laminilla abre su guía con temario, conceptos de alto rendimiento, correlación clínica, tarjetas y examen.',
            deco='<svg class="deco" viewBox="0 0 190 150" aria-hidden="true"><g fill="none" stroke="var(--accent)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M74 14h22l-4 34H78z"/><path d="M85 48v14"/><path d="M80 62h10l-2 12h-6z"/><path d="M104 30c34 8 46 46 30 80"/><path d="M50 112h96"/><path d="M134 110v26M60 136h104"/></g><rect x="58" y="102" width="56" height="8" rx="2" fill="var(--orange)" opacity=".85"/><circle cx="85" cy="106" r="3" fill="#fff" opacity=".9"/></svg>',
            otras=[['Lengua Extranjera I', 'Alemán I'], ['Tecnologías de la Información en la Construcción del Conocimiento', ''], ['Optativa de Matemáticas', 'Matemáticas para Pensar']]),
    2: dict(title='2do semestre', kicker='Segundo semestre', back='Libreta', bodyclass='notebook',
            layout='Layout: libreta de laboratorio. Cada guía es un cuaderno de espiral del color de su materia; al abrir una, ocupa toda la pantalla.',
            lede='De la célula al organismo: fisiología, biología celular y molecular, anatomía humana I y simulación. Cada libreta abre su guía con temario, conceptos de alto rendimiento, correlación clínica, tarjetas y examen.',
            deco='<svg class="deco" viewBox="0 0 190 150" aria-hidden="true"><g fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><rect x="50" y="14" width="96" height="122" rx="8" stroke="var(--accent)"/><path d="M42 30h16M42 52h16M42 74h16M42 96h16M42 118h16" stroke="var(--orange)"/><path d="M70 60h18l6-14 8 30 6-16h22" stroke="var(--accent)"/><path d="M70 96h56M70 110h40" stroke="var(--accent)" opacity=".5"/></g></svg>',
            otras=[['Lengua Extranjera II', 'Alemán II'], ['Argumentación Académica', ''], ['Optativa de Ciencias del Comportamiento', 'Alimentación y Vida'], ['Optativa de Artes', 'Arte, Historia y Cultura']]),
}

def main():
    guias = sorted((parse(p) for p in glob.glob(os.path.join(HERE, 'guias', '*.txt'))), key=lambda g: (g['sem'], g['orden']))
    tpl = open(os.path.join(HERE, 'guia.html'), encoding='utf-8').read()
    hub = {'G': [], 'FT': {}}
    for g in guias:
        sem = g['sem']
        data = {'id': g['id'], 'title': g['title'], 'kicker': f"{SEMS[sem]['kicker']} · {g['materia']}",
                'desc': g.get('desc', ''), 'nota': inline(g['nota']) if g.get('nota') else '', 'temas': g['temas']}
        out = (tpl.replace('__TITLE__', html.escape(g['title']))
                  .replace('__COLOR__', g['color']).replace('__CODE__', html.escape(g['codigo']))
                  .replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')))
        d = os.path.join(SITE, f's{sem}', 'guias')
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, g['id'] + '.html'), 'w', encoding='utf-8').write(out)
        nc = sum(len(t.get('cards', [])) for t in g['temas'])
        nq = sum(len(t.get('quiz', [])) for t in g['temas'])
        g['_n'] = (len(g['temas']), nc, nq)
        print(f"s{sem}/guias/{g['id']}.html  temas {len(g['temas']):3}  subtemas {nsubs(g):3}  tarjetas {nc:4}  preguntas {nq:4}")
        hub['G'].append({'id': g['id'], 'sem': sem, 'icon': g.get('icon', 'anat'), 'color': g['color'], 'area': g['materia'],
                         'title': g['title'], 'sub': g.get('sub', ''), 'desc': g.get('desc', ''),
                         'stats': [[str(len(g['temas'])), 'temas'], [str(nsubs(g)), 'subtemas'], [str(nq), 'preguntas']], 'temas': len(g['temas']),
                         'feat': ['Subtemas', 'Diagramas', 'Alto rendimiento', 'Correlación clínica', 'Tarjetas', 'Examen'],
                         'toc': [t['t'] for t in g['temas']], 'kw': g.get('kw', '')})
        hub['FT'][g['id']] = words(g)
    stpl = open(os.path.join(HERE, 'semestre.html'), encoding='utf-8').read()
    for sem, S in SEMS.items():
        arts = [{'id': g['id'], 'titulo': g['title'], 'materia': g['materia'], 'codigo': g['codigo'], 'color': g['color'],
                 'descripcion': g.get('desc', ''), 'temas': [t['t'] for t in g['temas']], 'modos': g['modos'].split(','),
                 'ntemas': g['_n'][0], 'nsubs': nsubs(g), 'ntarjetas': g['_n'][1], 'npreguntas': g['_n'][2], 'extra': bool(g.get('extra'))}
                for g in guias if g['sem'] == sem]
        out = stpl
        for k, v in {'__LAYOUT__': S['layout'], '__TITLE__': S['title'], '__KICKER__': S['kicker'], '__LEDE__': S['lede'],
                     '__BACK__': S['back'], '__BODYCLASS__': S['bodyclass'], '__DECO__': S['deco'],
                     '__ARTEFACTOS__': json.dumps(arts, ensure_ascii=False, indent=1),
                     '__OTRAS__': json.dumps(S['otras'], ensure_ascii=False)}.items():
            out = out.replace(k, v)
        os.makedirs(os.path.join(SITE, f's{sem}'), exist_ok=True)
        open(os.path.join(SITE, f's{sem}', 'index.html'), 'w', encoding='utf-8').write(out)
        print(f's{sem}/index.html', len(arts), 'guías')
    json.dump(hub, open(os.path.join(HERE, 'hub.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
