# Conecta 1º y 2º semestre al hub (site/index.html y site/app.html) usando tools-s12/hub.json.
# Idempotente: si ya se aplicó, reemplaza los bloques marcados con /*s12*/.
# Uso: python3 tools-s12/patch_hub.py [archivo.html ...]   (sin argumentos: index.html y app.html)
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')
hub = json.load(open(os.path.join(HERE, 'hub.json'), encoding='utf-8'))

def js(v):
    return json.dumps(v, ensure_ascii=False, separators=(',', ':'))

def g_entry(g):
    return ('{id:%s,sem:%d,icon:%s,color:%s,area:%s,title:%s,sub:%s,\n  desc:%s,\n  stats:%s,temas:%d,\n  feat:%s,\n  toc:%s,\n  kw:%s}'
            % (js(g['id']), g['sem'], js(g['icon']), js(g['color']), js(g['area']), js(g['title']), js(g['sub']),
               js(g['desc']), js(g['stats']), g['temas'], js(g['feat']), js(g['toc']), js(g['kw'])))

G_BLOCK = '/*s12:G*/\n ' + ',\n '.join(g_entry(g) for g in hub['G']) + ',\n /*/s12:G*/'
FT_BLOCK = '/*s12:FT*/' + ','.join('%s: %s' % (js(k), js(v)) for k, v in hub['FT'].items()) + ', /*/s12:FT*/'
SEMS_OLD = '{n:1},{n:2},'
SEMS_NEW = ('{n:1,name:"Primer semestre",note:"Ciencias básicas: histología, bioquímica, anatomofisiología, embriología y genética."},'
            '{n:2,name:"Segundo semestre",note:"Fisiología, biología celular y molecular, anatomía humana I y simulación."},')

def patch(path):
    s = open(path, encoding='utf-8').read()
    n0 = len(s)
    # 1) semestres con nombre y nota
    if SEMS_OLD in s:
        s = s.replace(SEMS_OLD, SEMS_NEW, 1)
    elif SEMS_NEW not in s:
        raise SystemExit(f'{path}: no encontré la lista SEMS')
    # 2) guías en G (al inicio, para que salgan en orden de semestre)
    if '/*s12:G*/' in s:
        s = re.sub(r'/\*s12:G\*/.*?/\*/s12:G\*/', lambda m: G_BLOCK, s, count=1, flags=re.S)
    else:
        i = s.index('const G=[\n') + len('const G=[\n')
        s = s[:i] + ' ' + G_BLOCK + '\n' + s[i:]
    # 3) archivo de cada guía
    old = '({3:"s3/"+g.id+"/index.html"'
    new = '({1:"s1/guias/"+g.id+".html",2:"s2/guias/"+g.id+".html",3:"s3/"+g.id+"/index.html"'
    if old in s and new not in s:
        s = s.replace(old, new, 1)
    elif new not in s:
        raise SystemExit(f'{path}: no encontré guideFile')
    # 4) texto completo para el buscador
    if '/*s12:FT*/' in s:
        s = re.sub(r'/\*s12:FT\*/.*?/\*/s12:FT\*/', lambda m: FT_BLOCK, s, count=1, flags=re.S)
    else:
        s = s.replace('const FT={', 'const FT={' + FT_BLOCK, 1)
    # 5) nombre del semestre en "Material extra"
    old = 'const SEMNAME={3:"3er semestre"'
    new = 'const SEMNAME={1:"1er semestre",2:"2do semestre",3:"3er semestre"'
    if old in s and new not in s:
        s = s.replace(old, new, 1)
    open(path, 'w', encoding='utf-8').write(s)
    print(os.path.basename(path), n0, '→', len(s), 'bytes')

files = sys.argv[1:] or [os.path.join(SITE, 'index.html'), os.path.join(SITE, 'app.html')]
for f in files:
    patch(f)
