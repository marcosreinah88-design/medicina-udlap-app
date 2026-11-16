# Conecta site/amboss.js a cada guía (botón «Seguir leyendo en AMBOSS» al final de cada subtema).
# Idempotente: correrlo otra vez después de tools-s12/build.py o de cambiar una guía.
# Uso: python3 tools-amboss/patch_amboss.py          (site/ del repo)
#      SITE=<carpeta copia del artefacto> python3 tools-amboss/patch_amboss.py
import os,re
HERE=os.path.dirname(os.path.abspath(__file__)); SITE=os.environ.get('SITE') or os.path.join(HERE,'..','site')
PAGES={
 's1/guias/anatomofisiologia.html':'s1-anatomofisiologia','s1/guias/bioquimica.html':'s1-bioquimica',
 's1/guias/embriologia-genetica.html':'s1-embriologia','s1/guias/histologia.html':'s1-histologia','s1/guias/simulacion-i.html':'s1-simulacion-i',
 's2/guias/anatomia-humana-i.html':'s2-anatomia-humana-i','s2/guias/biologia-celular.html':'s2-biologia-celular',
 's2/guias/fisiologia.html':'s2-fisiologia','s2/guias/simulacion-ii.html':'s2-simulacion-ii',
 's3/farmacologia/index.html':'s3-farmacologia','s3/anatomia/index.html':'s3-anatomia',
 's3/fisiologia-clinica/index.html':'s3-fisiologia-clinica','s3/microbiologia/index.html':'s3-microbiologia',
 's3/simulacion-iii/index.html':'s3-simulacion-iii','s3/propedeutica/index.html':'s3-propedeutica',
 's4/apps/cirugia.html':'s4-cirugia','s4/apps/farmacologia-ii.html':'s4-farmacologia-ii','s4/apps/hematologia.html':'s4-hematologia',
 's4/apps/inmunologia.html':'s4-inmunologia','s4/apps/nutricion.html':'s4-nutricion','s4/apps/simulacion-iv.html':'s4-simulacion-iv',
 's5/cirugia/index.html':'s5-cirugia','s5/esofago/index.html':'s5-tp','s5/gastro/index.html':'s5-tp','s5/hepatobiliar/index.html':'s5-tp',
 's5/imagenologia/index.html':'s5-imagenologia','s5/oftalmo/index.html':'s5-oftalmo','s5/otorrino/index.html':'s5-otorrino',
 's5/psiquiatria/index.html':'s5-psiquiatria',
 's6/artefactos/infectologia.html':'s6-infectologia','s6/artefactos/salud-publica.html':'s6-salud-publica',
 'x/signos/index.html':'x-signos','x/triage/index.html':'x-triage','x/svb/index.html':'x-slides','x/triage-clase/index.html':'x-slides',
}
def tag(f,g):
    if f.startswith('s6/artefactos/'):
        # el anaquel de 6º abre sus artefactos como srcdoc (ruta base = s6/), igual que anki.js
        return ('<script data-amb>(function(){var s=document.createElement("script");s.src=(location.protocol==="about:"?"../":"../../")+"amboss.js";'
                f's.setAttribute("data-amb-g","{g}");document.body.appendChild(s)}})()</script><!--amboss-->')
    return f'<script src="{"../"*f.count("/")}amboss.js" data-amb-g="{g}" defer></script><!--amboss-->'
n=0
for f,g in PAGES.items():
    p=os.path.join(SITE,f)
    if not os.path.exists(p): print('falta',f); continue
    s=open(p,encoding='utf-8').read()
    s=re.sub(r'<script (?:src="[^"]*amboss\.js"[^>]*|data-amb)>.*?</script><!--amboss-->','',s,flags=re.S)
    t=tag(f,g); i=s.rfind('</body>')
    s=s[:i]+t+s[i:] if i>=0 else s+t
    open(p,'w',encoding='utf-8').write(s); n+=1
print('amboss conectado en',n,'páginas')
