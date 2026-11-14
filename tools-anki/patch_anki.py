# Conecta las tarjetas de Anki (site/anki/<materia>.json + site/anki/anki.js) a la página.
# - Guías que ya existen: botón flotante "Tus tarjetas de Anki".
# - Materias sin página: crea su página y la agrega a la página de su semestre y a "Otros materiales".
# Idempotente: correrlo otra vez después de build.py (tools-s12) o de rearmar el hub.
# Uso: python3 tools-anki/patch_anki.py [ruta/al/index.html del artefacto ...]
import os,re,json,sys,html
HERE=os.path.dirname(os.path.abspath(__file__)); SITE=os.path.join(HERE,'..','site')
J=lambda m:json.load(open(os.path.join(SITE,'anki',m+'.json'),encoding='utf-8'))
EXIST={'simulacion-i':'s1/guias/simulacion-i.html','simulacion-ii':'s2/guias/simulacion-ii.html','anatomia-humana-i':'s2/guias/anatomia-humana-i.html',
 'farmacologia':'s3/farmacologia/index.html','anatomia':'s3/anatomia/index.html','hematologia':'s4/apps/hematologia.html','farmacologia-ii':'s4/apps/farmacologia-ii.html',
 'inmunologia':'s4/apps/inmunologia.html','simulacion-iv':'s4/apps/simulacion-iv.html','nutricion':'s4/apps/nutricion.html','cirugia-principios':'s4/apps/cirugia.html',
 'gastro':'s5/gastro/index.html','cirugia':'s5/cirugia/index.html','oftalmo':'s5/oftalmo/index.html','otorrino':'s5/otorrino/index.html','imagenologia':'s5/imagenologia/index.html',
 'infectologia':'s6/artefactos/infectologia.html','salud-publica':'s6/artefactos/salud-publica.html'}
# materias nuevas: (archivo, título, color, frase, código)
NEW={'microbiologia':('s3/microbiologia/index.html','Microbiología y Parasitología','#6b3fa0','Bacterias, virus, hongos y parásitos','MIC'),
 'simulacion-iii':('s3/simulacion-iii/index.html','Laboratorio de Simulación III','#c4142f','Choque, heridas, gasometría y cálculo de goteo','SIM'),
 'ecosofia':('s3/ecosofia/index.html','Ecosofía','#3f7d3a','Ecología, sociedad y salud','ECO'),
 'examen-basicos':('s4/apps/examen-basicos.html','Examen de Conocimientos Básicos','#1d4e89','Repaso de ciencias básicas de 1º a 4º','EXB'),
 'bioetica':('s5/bioetica/index.html','Bioética en Ciencias de la Salud','#8a5a2b','Principios, consentimiento y dilemas','BIO'),
 'campos-clinicos-i':('s5/campos-clinicos-i/index.html','Campos Clínicos I','#00573c','Medicina interna en el hospital','CC1'),
 'casos-clinicos-i':('s5/casos-clinicos-i/index.html','Casos Clínicos I','#b0412e','Cómo presentar y analizar un caso','CAS'),
 'casos-clinicos-ii':('s6/artefactos/casos-clinicos-ii.html','Casos Clínicos II','#7a2e5c','Casos clínicos del 6º semestre','CA2'),
 'enarm':('x/enarm/index.html','ENARM','#f26b21','Preguntas tipo examen, pediatría y vocabulario médico en inglés','ENA')}
SEMN={0:'Material extra',1:'1er semestre',2:'2do semestre',3:'3er semestre',4:'4º semestre',5:'5º semestre',6:'6º semestre'}
def rel(f): return '../'*f.count('/')+'anki/anki.js'
def tag(m,f,n):
    if f.startswith('s6/artefactos/'):
        # el anaquel de 6º abre sus artefactos como srcdoc (la ruta base es la de s6/), así que se carga con ruta según dónde esté
        return ('<script data-anki>(function(){var s=document.createElement("script");s.src=(location.protocol==="about:"?"../":"../../")+"anki/anki.js";'
                f's.dataset.m="{m}";s.dataset.n="{n}";document.body.appendChild(s)}})()</script><!--anki-->')
    return f'<script src="{rel(f)}" data-m="{m}" data-n="{n}" defer></script><!--anki-->'
def temas(d):
    seen=[];[seen.append(x[0]) for x in d['c']+d['q'] if x[0] not in seen]; return seen
def write(p,s):
    open(p,'w',encoding='utf-8').write(s)
# 1) botón en las guías que ya existen
for m,f in EXIST.items():
    p=os.path.join(SITE,f); s=open(p,encoding='utf-8').read(); d=J(m)
    s=re.sub(r'<script (?:src="[^"]*anki/anki\.js"[^>]*|data-anki)>.*?</script><!--anki-->','',s,flags=re.S)
    s=s.replace('</body>',tag(m,f,len(d['c'])+len(d['q']))+'</body>',1) if '</body>' in s else s+tag(m,f,len(d['c'])+len(d['q']))
    write(p,s)
# 2) páginas nuevas
PAGE=open(os.path.join(HERE,'materia.html'),encoding='utf-8').read()
for m,(f,title,color,frase,cod) in NEW.items():
    d=J(m); t=temas(d); p=os.path.join(SITE,f); os.makedirs(os.path.dirname(p),exist_ok=True)
    s=(PAGE.replace('{{TITLE}}',html.escape(title)).replace('{{COLOR}}',color).replace('{{FRASE}}',html.escape(frase)).replace('{{COD}}',cod)
        .replace('{{SEM}}',SEMN[d['s']]).replace('{{NC}}',f"{len(d['c']):,}".replace(',',',')).replace('{{NQ}}',str(len(d['q']))).replace('{{NT}}',str(len(t)))
        .replace('{{TEMAS}}',''.join(f'<li>{html.escape(x)}</li>' for x in t[:14])+('<li>…</li>' if len(t)>14 else ''))
        .replace('{{SCRIPT}}',tag(m,f,len(d['c'])+len(d['q']))))
    write(p,s)
def ins(path,marker_open,marker_close,anchor,block,before=True):
    s=open(path,encoding='utf-8').read()
    s=re.sub(re.escape(marker_open)+r'.*?'+re.escape(marker_close)+r'\n?','',s,flags=re.S)
    b=marker_open+'\n'+block+'\n'+marker_close+'\n'
    i=s.find(anchor)
    if i<0: print('NO ANCLA',path,anchor[:40]); return
    s=s[:i]+b+s[i:] if before else s[:i+len(anchor)]+'\n'+b+s[i+len(anchor):]
    write(path,s)
js=lambda x:json.dumps(x,ensure_ascii=False)
def nums(m): d=J(m); return len(d['c']),len(d['q']),len(temas(d))
# 3) semestres
# 3º: ITEMS (archivero)
blk=[]
for m in ['microbiologia','simulacion-iii','ecosofia']:
    f,title,color,frase,cod=NEW[m]; c,q,t=nums(m)
    st={'temas':t,'tarjetas':c}; 
    if q: st['preguntas']=q
    blk.append(f' {{id:{js(m)},src:{js(m+"/index.html")},materia:{js(J(m)["n"])},title:{js(title)},desc:{js(frase+". Tus tarjetas de Anki, revisadas y corregidas.")},feats:["Repaso con tarjetas","Ver todas","Buscador","Progreso"],stats:{js(st)},cover:"gen",keys:{js(" ".join(temas(J(m))).lower())}}},')
ins(os.path.join(SITE,'s3/index.html'),' ,/*anki:items*/',' /*/anki:items*/','\n];\n\nconst $=s=>',"\n".join(blk))
# 4º: ITEMS (carpeta)
f,title,color,frase,cod=NEW['examen-basicos']; c,q,t=nums('examen-basicos')
art=('<svg class="art" viewBox="0 0 480 240" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="480" height="240" fill="#e3ebf5"/>'
     +''.join(f'<rect x="{250+i*26}" y="{40+i*18}" width="170" height="110" rx="12" fill="#fff" stroke="#1d4e89" stroke-width="2" transform="rotate({-8+i*6} {335+i*26} {95+i*18})"/>' for i in range(3))
     +'<text x="372" y="168" font-size="46" font-weight="700" fill="#1d4e89" text-anchor="middle" font-family="Georgia,serif">?</text></svg>')
blk=('  {id:"examen-basicos",file:"apps/examen-basicos.html",title:"Examen de Conocimientos Básicos",subject:"Tarjetas de Anki",color:"#1d4e89",'
     'bg:"linear-gradient(135deg,#e3ebf5 0%,#eef2f8 100%)",bgDark:"linear-gradient(135deg,#1b2a40 0%,#1f2633 100%)",'
     f'desc:{js(frase+": tus tarjetas de Anki, revisadas y corregidas.")},nums:[[{js(f"{c:,}")},"tarjetas"],[{js(str(t))},"temas"]],'
     'tags:["Repaso con tarjetas","Ver todas","Buscador","Progreso"],keywords:"examen basicos ciencias basicas anatomia fisiologia bioquimica histologia embriologia farmacologia",'
     f'art:{js(art)}}},')
ins(os.path.join(SITE,'s4/index.html'),'  /*anki:items*/','  /*/anki:items*/','const ITEMS = [\n',blk,before=False)
# 5º: EXTRA (estante)
blk=[]
for m in ['bioetica','campos-clinicos-i','casos-clinicos-i']:
    f,title,color,frase,cod=NEW[m]; c,q,t=nums(m)
    blk.append(f'  {{id:{js(m)},title:{js(title)},desc:{js(frase+". Tus tarjetas de Anki, revisadas y corregidas.")},stats:[[{js(str(c))},"tarjetas"],[{js(str(t))},"temas"]],tags:{js("anki tarjetas "+" ".join(temas(J(m))).lower())}}},')
ins(os.path.join(SITE,'s5/index.html'),'  /*anki:extra*/','  /*/anki:extra*/','const EXTRA=[\n',"\n".join(blk),before=False)
# 6º: ARTEFACTOS (anaquel)
f,title,color,frase,cod=NEW['casos-clinicos-ii']; t=temas(J('casos-clinicos-ii'))
blk=f'  {{id:"casos-clinicos-ii",titulo:"Casos Clínicos II",materia:"Casos Clínicos II",codigo:"CA2",color:"#7a2e5c",descripcion:{js(frase+": tus tarjetas de Anki, revisadas y corregidas.")},temas:{js(t)},modos:["Repasar","Ver todas"]}},'
ins(os.path.join(SITE,'s6/index.html'),'  /*anki:items*/','  /*/anki:items*/','const ARTEFACTOS = [\n',blk,before=False)
# 4) hub: "Otros materiales" (las 9 nuevas, para encontrarlas también desde la portada)
hubs=[os.path.join(SITE,'index.html'),os.path.join(SITE,'app.html')]+sys.argv[1:]
blk=[]
for m,(f,title,color,frase,cod) in NEW.items():
    d=J(m); src={'src':f} if not f.startswith('x/') else {}
    e={'id':'anki-'+m if m!='enarm' else 'enarm','title':title+(' · tarjetas de Anki' if m!='enarm' else ' · tus tarjetas de Anki'),'kind':'artifact','subject':d['n'] if m!='enarm' else 'ENARM'}
    if d['s']: e['fromSem']=d['s']
    e.update(src)
    blk.append('    '+re.sub(r'"(\w+)":',r'\1:',js(e))+',')
for h in hubs:
    if os.path.exists(h): ins(h,'    /*anki:mat*/','    /*/anki:mat*/','    /* material extra que ya vive en la página de un semestre',"\n".join(blk))
print('listo')
