# Carga el diseño de la página Estudio (site/estudio-diseno.css) en la portada de Mac y del cel.
# Uso: python3 tools-estudio/patch_diseno.py site/index.html site/app.html   (se puede correr dos veces sin duplicar)
import sys
A='<script src="estudio.js"></script>'
B='<link rel="stylesheet" href="estudio-diseno.css">\n'+A
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'href="estudio-diseno.css"' in s: print("ya estaba",f); continue
    n=s.count(A)
    if n!=1: sys.exit(f"{f}: {n} veces: {A}")
    open(f,'w',encoding='utf-8').write(s.replace(A,B));print("ok",f)
