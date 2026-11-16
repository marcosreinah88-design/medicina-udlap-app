# Pantalla de carga: en lugar de negro, el escudo UDLAP en verde y naranja mientras la portada termina de cargar.
# Mete tools-carga/carga.html justo después del script del tema (así respeta modo oscuro/claro) y, en la versión del cel
# (la que tiene app.webmanifest), las imágenes de arranque del iPhone (site/img/arranque/, ver splash.js).
# Uso: python3 tools-carga/patch_carga.py site/index.html site/app.html [artefacto.html]   (se puede correr varias veces)
import os,re,sys,json
here=os.path.dirname(os.path.abspath(__file__))
BLOCK=open(os.path.join(here,'carga.html'),encoding='utf-8').read().strip()
BLOCK=BLOCK.replace('{{ESCUDO}}',open(os.path.join(here,'escudo.b64')).read().strip())
SIZES=json.load(open(os.path.join(here,'tamanos.json')))
SPLASH='<!--arranque-->'+''.join(
  f'<link rel="apple-touch-startup-image" media="(device-width:{w}px) and (device-height:{h}px) and (-webkit-device-pixel-ratio:{d}) and (orientation:portrait)" href="img/arranque/{w*d}x{h*d}.png">'
  for w,h,d in SIZES)+'<!--/arranque-->'
THEME=r'<script>try\{var t=localStorage\.getItem\("carrera-theme"\).*?</script>\n'
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    s=re.sub(r'<!--carga-->.*?<!--/carga-->\n?','',s,flags=re.S)
    n=len(re.findall(THEME,s))
    if n!=1: sys.exit(f'{f}: no encontré el script del tema ({n})')
    s=re.sub(THEME,lambda m:m.group(0)+BLOCK+'\n',s,count=1)
    if 'app.webmanifest' in s:
        s=re.sub(r'<!--arranque-->.*?<!--/arranque-->\n?','',s,flags=re.S)
        a='<link rel="apple-touch-icon" href="icon-180.png">'
        if s.count(a)!=1: sys.exit(f'{f}: no encontré el apple-touch-icon')
        s=s.replace(a,a+'\n'+SPLASH)
    open(f,'w',encoding='utf-8').write(s);print('ok',f)
