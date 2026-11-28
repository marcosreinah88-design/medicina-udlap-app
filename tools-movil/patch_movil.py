# Ajustes para el cel (iPhone): zona segura de la app instalada, sin zoom al escribir, «Tu día» sin cortes,
# visor que no queda bajo la rayita de inicio y espacio para los botones flotantes de las guías.
# Uso: python3 tools-movil/patch_movil.py site/index.html site/app.html
#      python3 tools-movil/patch_movil.py --artefacto <copia del artefacto.html>   (sin el margen de arriba: claude.ai ya lo pone)
# Idempotente: reemplaza los bloques <style id="movil"> y <script id="movil-js"> (antes de </body>) si ya existen.
import re,sys,os
D=os.path.dirname(os.path.abspath(__file__))
CSS=open(os.path.join(D,'movil.css'),encoding='utf-8').read().strip()
JS=open(os.path.join(D,'movil.js'),encoding='utf-8').read().strip()
ST='<style id="movil">\n'+CSS+'\n</style>'
SC='<script id="movil-js">\n'+JS+'\n</script>'
VP=re.compile(r'<meta name="viewport" content="([^"]*)">')
def vp(m):
    c=[x.strip() for x in m.group(1).split(',') if x.strip() and not x.strip().startswith('maximum-scale')]
    i=next((k for k,x in enumerate(c) if x.startswith('initial-scale')),len(c)-1)
    c.insert(i+1,'maximum-scale=1')  # iOS: no hace zoom (y no deja la página movida) al tocar un campo de texto; pellizcar sigue funcionando
    return '<meta name="viewport" content="'+','.join(c)+'">'
ART='--artefacto' in sys.argv
if ART: ST=ST.replace('</style>',':root{--mv-top:0px}\n</style>')
for f in [a for a in sys.argv[1:] if a!='--artefacto']:
    s=open(f,encoding='utf-8').read()
    s=re.sub(r'\n?<style id="movil">.*?</style>','',s,flags=re.S)
    s=re.sub(r'\n?<script id="movil-js">.*?</script>','',s,flags=re.S)
    # al final del body: así gana sobre los estilos de la portada y de sus parches anteriores
    i=s.rfind('</body>')
    if i<0: s=s.rstrip('\n')+'\n'+ST+'\n'+SC+'\n'   # el hub no cierra </body>: va al final del archivo
    else: s=s[:i]+ST+'\n'+SC+'\n'+s[i:]
    if VP.search(s): s=VP.sub(vp,s,count=1)
    else: print("aviso: sin meta viewport en",f)
    open(f,'w',encoding='utf-8').write(s);print("ok",f)
