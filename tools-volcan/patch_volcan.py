# Volcán de la portada: fumarola continua, explosiones de ceniza (columna con volumen, rayos, caída de ceniza)
# y erupciones de lava (resplandor que parpadea, bombas con estela que ruedan, chispas, coladas, brillo en el cielo).
# Reemplaza la fumarola y las erupciones viejas por tools-volcan/volcan.css y tools-volcan/volcan.js.
# Uso: python3 tools-volcan/patch_volcan.py site/index.html site/app.html [artefacto.html]   (se puede correr varias veces)
import os,re,sys
here=os.path.dirname(os.path.abspath(__file__))
CSS=open(os.path.join(here,'volcan.css'),encoding='utf-8').read().strip()+'\n'
JS=open(os.path.join(here,'volcan.js'),encoding='utf-8').read().strip()+'\n'
SKY='<i class="v-sky" id="volcSky"></i>'
SVG=('<!--volcan-->\n      <!-- fumarola, ceniza y lava: tools-volcan (capa .volc) -->\n      <!--/volcan-->')
LAYER=('<!--volcan-capa--><span class="v-fum" id="volcFum"><i></i><i></i><i></i><i></i><i></i></span>'
       '<div class="volc" id="volc"><canvas id="volcCv"></canvas></div><!--/volcan-capa-->')
def sub1(s,pat,rep,f,what):
    n=len(re.findall(pat,s,flags=re.S))
    if n!=1: sys.exit(f"{f}: no encontré {what} ({n})")
    return re.sub(pat,lambda m:rep,s,flags=re.S)
OLDCSS=[r'\.horizon \.smoke path\{[^}]*\}\n?',r'\.horizon \.smoke path\+path\{[^}]*\}\n?',r'\.horizon \.glow\{[^}]*\}\n?',
        r'\.horizon \.ash,\.horizon \.bomb\{[^}]*\}\n?',r'\.horizon \.ash\{[^}]*\}\n?',r'\.horizon \.ash\.dk\{[^}]*\}\n?',
        r'\.horizon \.bomb\{[^}]*\}\n?',r'\.horizon \.flow\{[^}]*\}\n?',r'@keyframes smoke\{[^}]*\{[^}]*\}[^}]*\{[^}]*\}\}\n?',
        r'\.hero\.dusk \.horizon \.smoke path,\.hero\.dawn \.horizon \.smoke path\{[^}]*\}\n?',r'\.hero\.night \.horizon \.smoke path\{[^}]*\}\n?']
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    for p in OLDCSS: s=re.sub(p,'',s)
    if '/* ===== volcán:' in s:
        s=sub1(s,r'/\* ===== volcán:.*?/\* ===== /volcán ===== \*/\n?',CSS,f,'el CSS del volcán')
    else:
        s=sub1(s,r'(?=@keyframes draw\{)',CSS,f,'dónde poner el CSS')
    s=sub1(s,r'<!--volcan-->.*?<!--/volcan-->|<!-- fumarola -->.*?<g id="erupt"></g>',SVG,f,'la fumarola del SVG')
    if 'id="volcSky"' not in s:
        s=sub1(s,r'(?=<svg viewBox="0 0 1200 180" preserveAspectRatio="none">)',SKY,f,'el SVG del horizonte')
    if '<!--volcan-capa-->' in s: s=sub1(s,r'<!--volcan-capa-->.*?<!--/volcan-capa-->',LAYER,f,'la capa del volcán')
    else: s=sub1(s,r'(?=<span class="skylbl" id="skyLbl")',LAYER,f,'dónde poner la capa del volcán')
    s=sub1(s,r'/\* el Popo despierta de vez en cuando.*?(?:next\(R\(4500,6000\)\);\n\}\)\(\);|/\* fin volcán \*/)\n?',JS,f,'el script de erupciones')
    open(f,'w',encoding='utf-8').write(s);print('ok',f)
