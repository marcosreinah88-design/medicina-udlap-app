# Cielo automático de la portada: amanecer, día, atardecer y noche con estrellas y la luna en su fase real.
# Reemplaza el bloque del cielo (CSS, HTML y script) por tools-sky/sky.css y tools-sky/sky.js.
# Uso: python3 tools-sky/patch_sky.py site/index.html site/app.html [artefacto.html]   (se puede correr varias veces)
import os,re,sys
here=os.path.dirname(os.path.abspath(__file__))
CSS=open(os.path.join(here,'sky.css'),encoding='utf-8').read().strip()+'\n'
JS=open(os.path.join(here,'sky.js'),encoding='utf-8').read().strip()+'\n'
SKY=('<div class="sky" aria-hidden="true"><i class="sky-dawn"></i><i class="sky-dusk"></i><i class="sky-night"></i>'
     '<svg class="sky-stars" id="skyStars"></svg></div>')
LUNA=('<div class="luna" id="luna"><svg viewBox="-50 -50 100 100"><defs><clipPath id="lunaClip"><path d=""/></clipPath></defs>'
      '<circle class="dark" r="40"/><path class="lit" d=""/><g clip-path="url(#lunaClip)">'
      '<circle class="cr" cx="-12" cy="-14" r="7"/><circle class="cr" cx="14" cy="6" r="9"/><circle class="cr" cx="-6" cy="18" r="5"/>'
      '<circle class="cr" cx="20" cy="-18" r="4"/><circle class="cr" cx="-22" cy="6" r="4.5"/></g></svg></div>')
LBL='<button type="button" class="skylbl" id="skyLbl" tabindex="-1" hidden></button>'
def sub1(s,pat,rep,f,what):
    n=len(re.findall(pat,s,flags=re.S))
    if n!=1: sys.exit(f"{f}: no encontré {what} ({n})")
    return re.sub(pat,lambda m:rep,s,flags=re.S)
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    s=sub1(s,r'/\* ===== cielo: .*?(?=\.seal\{cursor:pointer)',CSS,f,'el CSS del cielo')
    s=sub1(s,r'<div class="sky" aria-hidden="true">.*?</div>',SKY,f,'el div del cielo')
    s=sub1(s,r'<span class="skylbl" id="skyLbl" hidden></span>|<button type="button" class="skylbl" id="skyLbl"[^>]*></button>',LBL,f,'la etiqueta del cielo')
    if 'id="luna"' not in s:
        s=s.replace('<div class="horizon in" aria-hidden="true">','<div class="horizon in" aria-hidden="true">\n    '+LUNA,1)
    s=sub1(s,r'/\* cielo de Puebla.*?(?=route\(\);showResume\(\);)',JS,f,'el script del cielo')
    open(f,'w',encoding='utf-8').write(s);print('ok',f)
