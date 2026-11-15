# Conecta las favoritas (site/favoritos.js) a las páginas de cada semestre.
# Uso: python3 tools-fav/patch_favoritos.py [carpeta del sitio]   (por defecto site/; sirve igual para la copia del artefacto)
#  - mete <script src="../favoritos.js"> antes del script de la página y Fav.init({...}) justo después
#  - también parcha tools-s12/semestre.html (plantilla de 1º y 2º) para que build.py lo conserve
# Se puede correr varias veces sin duplicar.
import os,re,sys
here=os.path.dirname(os.path.abspath(__file__))
root=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(here,'..','site'))

S12="""{sem:SKIN==="notebook"?"s2":"s1",list:ARTEFACTOS,grid:"#grid",card:".item",wrap:true,skin:SKIN==="notebook"?"ribbon":"circle",
 id:el=>el.dataset.id,name:a=>a.titulo,render:()=>{chips();hprog();render()}}"""
CFG={
 's1':S12,'s2':S12,
 's3':"""{sem:"s3",list:ITEMS,grid:"#grid",card:".card",wrap:true,skin:"tab",id:el=>el.dataset.open,name:it=>it.title,render:()=>render()}""",
 's4':"""{sem:"s4",list:ITEMS,grid:"#shelf",card:"article.card",skin:"glass",
 id:el=>{const a=el.querySelector("a.cover");return a?a.getAttribute("href").slice(1):""},name:it=>it.title,render:()=>{renderTop();renderShelf()}}""",
 's5':"""{sem:"s5",list:G,grid:"#grid",card:".book-card",skin:"ribbon",id:el=>el.id.slice(2),name:g=>g.title,render:()=>render(),
 after:is=>{
  $("#books").innerHTML=G.map((g,i)=>`<button class="book${i===4?" lean":""}${is(g.id)?" fav-on":""}" type="button" data-open="${g.id}" style="--sp:${g.sp};--h:${HEIGHTS[i]}px" aria-label="Abrir ${esc(g.title)}${is(g.id)?" (favorita)":""}">${is(g.id)?'<i class="fav-b" aria-hidden="true"></i>':""}<span>${esc(SPINE[g.id][0])}</span><em>${esc(SPINE[g.id][1])}</em></button>`).join("");
  $("#chips").innerHTML=G.map(g=>`<button class="chip" type="button" data-jump="${g.id}" style="--c:${g.color}"><i></i>${esc(g.area==="Otorrinolaringología"?"Otorrino":g.area==="Gastroenterología"?"Gastro":g.area)}</button>`).join("");
 }}""",
 's6':"""{sem:"s6",list:ARTEFACTOS,grid:"#grid",card:".folder",wrap:true,skin:"tab",id:el=>el.dataset.id,name:a=>a.titulo,render:()=>render()}""",
}
EXTRA_CSS={
 # 1º y 2º: la etiqueta "N temas" se recorre para dejar sitio a la estrella
 's12':'.fav-w .item .ctop{right:58px}body.notebook .fav-w .item .ctop{right:60px}',
 's5':'.fav-b{position:absolute;top:1px;left:50%;width:14px;height:14px;margin-left:-7px;background:#fff;filter:drop-shadow(0 0 1.5px rgba(0,0,0,.6));clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)}',
}
SRC='<script src="../favoritos.js"></script>\n'
INIT_RE=re.compile(r'\n?<script data-fav>.*?</script>',re.S)
CSS_RE=re.compile(r'<style data-fav>.*?</style>\n?',re.S)
MARK={'s1':'const ARTEFACTOS','s2':'const ARTEFACTOS','s3':'const ITEMS','s4':'const ITEMS','s5':'const G=','s6':'const ARTEFACTOS'}

def patch(path,key,cfg,css):
    s=open(path,encoding='utf-8').read()
    s=INIT_RE.sub('',s);s=CSS_RE.sub('',s)
    m=s.find(MARK[key]);
    if m<0: sys.exit(f"{path}: no encontré {MARK[key]}")
    a=s.rfind('<script>',0,m);b=s.find('</script>',m)+len('</script>')
    if SRC not in s: s=s[:a]+SRC+s[a:];b+=len(SRC);a+=len(SRC)
    init='\n<script data-fav>try{Fav.init('+cfg+')}catch(e){}</script>'
    s=s[:b]+init+s[b:]
    if css:
        i=s.find(SRC);s=s[:i]+'<style data-fav>'+css+'</style>\n'+s[i:]
    open(path,'w',encoding='utf-8').write(s);print('ok',path)

for k in ['s1','s2','s3','s4','s5','s6']:
    p=os.path.join(root,k,'index.html')
    if os.path.exists(p): patch(p,k,CFG[k],EXTRA_CSS['s12'] if k in('s1','s2') else EXTRA_CSS.get(k))
tpl=os.path.join(here,'..','tools-s12','semestre.html')
if len(sys.argv)<=1 and os.path.exists(tpl):
    s=open(tpl,encoding='utf-8').read()
    patch(tpl,'s1',S12,EXTRA_CSS['s12'])
