# Conecta el subrayador (site/subrayar.js) a la página.
# Uso: python3 tools-subrayar/patch_subrayar.py site/index.html site/app.html [artefacto.html]
#  - en site/*.html agrega <script src="subrayar.js"> después de anim.js
#  - en la copia del artefacto (que lleva todo adentro) lo mete en línea antes de </body>
# Se puede correr varias veces sin duplicar.
import os,re,sys
here=os.path.dirname(os.path.abspath(__file__))
JS=open(os.path.join(here,'..','site','subrayar.js'),encoding='utf-8').read().strip()
A='<script src="anim.js"></script>';B=A+'\n<script src="subrayar.js"></script>'
INL_RE=re.compile(r'<script>/\* Subrayador:.*?</script>\n?',re.S)
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if A in s:
        if B not in s: s=s.replace(A,B,1)
    else:
        s=INL_RE.sub('',s)
        i=s.rfind('</body>')
        if i<0: sys.exit(f"{f}: no encontré </body>")
        s=s[:i]+'<script>'+JS+'\n</script>\n'+s[i:]
    open(f,'w',encoding='utf-8').write(s);print('ok',f)
