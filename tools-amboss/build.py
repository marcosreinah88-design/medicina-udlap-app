# Arma site/amboss.js: el código de tools-amboss/amboss.src.js con la tabla terminos.tsv adentro.
# terminos.tsv: una línea por término, «español<TAB>búsqueda en inglés». Para corregir a dónde lleva un botón, cambia
# la columna de la derecha y vuelve a correr esto (y luego firmar). Llaves:
#   «tema › subtema»  → solo ese subtema dentro de ese tema
#   «subtema»         → ese título en cualquier guía
#   «* palabra»       → apartado genérico (tratamiento, diagnóstico…): se busca «<tema en inglés> <palabra>»
#   valor «-»         → sin botón (portadas, bibliografía, casos de práctica)
# Las llaves van sin acentos y en minúsculas (como las deja norm() del script); build.py las normaliza solo.
import os,json,re,sys,unicodedata
HERE=os.path.dirname(os.path.abspath(__file__)); SITE=os.environ.get('SITE') or os.path.join(HERE,'..','site')
def norm(s):
    s=unicodedata.normalize('NFD',s); s=''.join(c for c in s if unicodedata.category(c)!='Mn').lower()
    s=re.sub(r'^\s*(clase|tema)?\s*\d+(\.\d+)*\s*[·.\-:)]?\s*','',s)
    s=re.sub(r'\s*\d+\s*(img|imagen(es)?|tarjetas?)\b.*$','',s)
    s=re.sub(r'[✓★†*]','',s); return re.sub(r'\s+',' ',s).strip()
tab={}
for ln in open(os.path.join(HERE,'terminos.tsv'),encoding='utf-8'):
    ln=ln.rstrip('\n')
    if not ln.strip() or ln.startswith('#'): continue
    k,v=ln.split('\t',1); v=v.strip()
    if k.startswith('* '): key='* '+norm(k[2:])
    elif ' › ' in k: a,b=k.split(' › ',1); key=norm(a)+' › '+norm(b)
    else: key=norm(k)
    tab[key]=v
src=open(os.path.join(HERE,'amboss.src.js'),encoding='utf-8').read()
out=re.sub(r'/\*TABLA\*/.*?/\*FIN\*/','/*TABLA*/'+json.dumps(tab,ensure_ascii=False,separators=(',',':'))+'/*FIN*/',src,flags=re.S)
open(os.path.join(SITE,'amboss.js'),'w',encoding='utf-8').write(out)
print('amboss.js:',len(tab),'términos')
