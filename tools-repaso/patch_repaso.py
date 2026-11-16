# Conecta «Qué repasar hoy» (site/repaso.js) a la portada.
# Uso: python3 tools-repaso/patch_repaso.py [archivos .html]   (sin argumentos: site/index.html y site/app.html)
#  - En la app va justo después de estudio.js (usa sus mazos con Estudio.decks).
#  - En la copia del artefacto (sin Estudio) va antes de </body>; ahí publica también repaso.js en la raíz.
#  - Actualiza la lista ANKI de repaso.js con los mazos de site/estudio-banco.json (para el artefacto).
# Idempotente: se puede correr dos veces sin duplicar. Luego: tools-subrayar/firmar.py <clave.pem>.
import sys,os,json,re
here=os.path.dirname(os.path.abspath(__file__));site=os.path.join(here,'..','site')
tag='<script src="repaso.js"></script>'
files=sys.argv[1:] or [os.path.join(site,'index.html'),os.path.join(site,'app.html')]
for f in files:
    s=open(f,encoding='utf-8').read()
    if tag in s: print('ya estaba',f);continue
    a='<script src="estudio.js"></script>'
    if a in s: s=s.replace(a,a+'\n'+tag,1)
    else:
        i=s.rfind('</body>')
        if i<0: sys.exit(f+': sin </body>')
        s=s[:i]+tag+'\n'+s[i:]
    open(f,'w',encoding='utf-8').write(s);print('ok',f)
bank=os.path.join(site,'estudio-banco.json')
if os.path.exists(bank):
    g=json.load(open(bank,encoding='utf-8'))['g']
    lst=json.dumps([[x[0][5:],x[1],x[2]] for x in g if str(x[0]).startswith('anki-')],ensure_ascii=False,separators=(',',':'))
    p=os.path.join(site,'repaso.js');s=open(p,encoding='utf-8').read()
    n=re.sub(r'/\*ANKI\*/.*?/\*/ANKI\*/',lambda m:'/*ANKI*/'+lst+'/*/ANKI*/',s,count=1,flags=re.S)
    if n!=s: open(p,'w',encoding='utf-8').write(n);print('lista ANKI actualizada')
