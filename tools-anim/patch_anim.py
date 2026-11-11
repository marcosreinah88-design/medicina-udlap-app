# Conecta las animaciones discretas (site/anim.js) a la página.
# Uso: python3 tools-anim/patch_anim.py site/index.html site/app.html   (se puede correr dos veces sin duplicar)
import sys
A='<script src="estudio.js"></script>';B=A+'\n<script src="anim.js"></script>'
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if B not in s:
        if s.count(A)!=1: sys.exit(f"{f}: falta {A} (aplica antes tools-estudio/patch_estudio.py)")
        s=s.replace(A,B)
    open(f,'w',encoding='utf-8').write(s);print("ok",f)
