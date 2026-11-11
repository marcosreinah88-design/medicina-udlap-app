/* Animaciones discretas de la portada y sus secciones.
   - Al abrir un semestre, una guía o una sección (Calendario, Calificaciones, Estudio, CTO...) entra con un fundido corto
     y sus tarjetas suben un poco, una tras otra.
   - En la portada las tarjetas aparecen suavemente al bajar con el scroll y los números de la franja naranja cuentan hasta su valor.
   - Al salir (regresar a la portada o cerrar una sección) se desvanece en lugar de cortarse de golpe.
   - Dentro de cada semestre, guía y material, sus tarjetas y temas aparecen suavemente al bajar y al cambiar de pestaña,
     y los desplegables abren suave. Solo se agrega movimiento: no se cambia ningún color, letra ni acomodo de esas páginas.
   - Dentro de cada semestre, abrir y cerrar una guía también entra y sale suave.
   - Botones con respuesta sutil al pasar el mouse y al tocarlos.
   Solo usa opacidad y desplazamiento (no cambia colores, así que el modo oscuro queda igual) y se apaga por completo
   si el sistema tiene activado "Reducir movimiento". */
(function(){
"use strict";
if(window.__carreraAnim)return;window.__carreraAnim=true;
const EASE="cubic-bezier(.2,.7,.2,1)";
const css=`
@media (prefers-reduced-motion:no-preference){
@keyframes anFade{from{opacity:0}to{opacity:1}}
@keyframes anRise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.an-r{opacity:0;transform:translateY(18px)}
.an-r.an-v{opacity:1;transform:none;transition:opacity .6s ${EASE} var(--an-d,0s),transform .6s ${EASE} var(--an-d,0s)}
.an-o>:not(.vbar){animation:anFade .3s ease-out both}
@keyframes anOut{to{opacity:0;transform:translateY(10px)}}
.cal.an-x[hidden],.viewer.an-x[hidden]{display:flex!important;pointer-events:none;animation:anOut .26s ease-in both}
.an-k{animation:anRise .45s ${EASE} both;animation-delay:calc(var(--an-i,0) * 45ms + 60ms)}
.frames iframe.an-f{animation:anFade .35s ease-out both}
.an-d>:not(summary){animation:anRise .3s ${EASE} both}
.theme,.vbtn,.cbtn{transition:background-color .2s,border-color .2s,color .2s,box-shadow .2s,transform .15s}
.theme:active,.vbtn:active,.cbtn:active,.resume:active,.ch-k:active{transform:scale(.96)}
.xcard{transition:box-shadow .25s,transform .25s ${EASE}}
.xcard:hover{transform:translateY(-2px);box-shadow:0 14px 30px -18px rgba(0,0,0,.35)}
.tnode .dot{transition:transform .2s ${EASE}}
.tnode:hover .dot{transform:scale(1.08)}
}`;
const st=document.createElement("style");st.id="anim-css";st.textContent=css;document.head.appendChild(st);

const reduced=()=>matchMedia("(prefers-reduced-motion: reduce)").matches;
const once=(el,cls,ms)=>{el.classList.remove(cls);void el.offsetWidth;el.classList.add(cls);clearTimeout(el.__anT);el.__anT=setTimeout(()=>el.classList.remove(cls),ms)};

/* 1. Portada: aparición suave al hacer scroll */
const HOME_SEL=["main .hday","main .search","main .sec-h","main .track",".sems .stile",".extra .sec-h",".extra .xcard","body>footer .in"];
function reveal(){
  if(reduced()||!("IntersectionObserver" in window))return;
  const els=[...document.querySelectorAll(HOME_SEL.join(","))].filter(e=>!e.closest(".cal,.viewer"));
  const done=e=>{e.classList.remove("an-r","an-v");e.style.removeProperty("--an-d")};
  const io=new IntersectionObserver(es=>{
    let k=0;
    for(const x of es){if(!x.isIntersecting)continue;const e=x.target;io.unobserve(e);
      const row=e.classList.contains("stile")||e.classList.contains("xcard");
      e.style.setProperty("--an-d",(row?(k++%4)*0.07:0)+"s");
      requestAnimationFrame(()=>e.classList.add("an-v"));
      setTimeout(()=>done(e),1100)}
  },{rootMargin:"0px 0px -6% 0px",threshold:0.08});
  for(const e of els){e.classList.add("an-r");io.observe(e)}
}

/* 2. Números de la franja naranja: cuentan desde 0 */
function countUp(){
  if(reduced())return;
  document.querySelectorAll("#totals b").forEach((b,i)=>{
    const m=/^(\d+)(.*)$/.exec(b.textContent.trim());if(!m)return;
    const end=+m[1],rest=m[2],t0=performance.now()+i*90,dur=900;if(end<2)return;
    const tick=t=>{const p=Math.min(1,Math.max(0,(t-t0)/dur)),v=Math.round(end*(1-Math.pow(1-p,3)));
      b.textContent=v+rest;if(p<1)requestAnimationFrame(tick)};
    b.textContent="0"+rest;requestAnimationFrame(tick);
  });
}

/* 3. Abrir semestres, guías y secciones */
const CARDS=".calhero,.gr-hero,.ccard,.cshelf,.es-card,.ctoEntry,.otile";
function opened(el){
  if(reduced())return;
  if(el.tagName==="IFRAME"){if(el.parentElement&&el.parentElement.id==="frames")once(el,"an-f",500);return}
  if(!el.matches(".cal,.viewer"))return;
  el.classList.remove("an-x");
  once(el,"an-o",400);
  const cs=[...el.querySelectorAll(CARDS)].filter(c=>!c.parentElement.closest(CARDS)).slice(0,10);
  cs.forEach((c,i)=>{c.style.setProperty("--an-i",i);once(c,"an-k",1200)});
}
/* al cerrar: el atributo hidden ya está puesto (la lógica de la página no cambia); solo se sigue viendo 260 ms mientras se desvanece */
function closed(el){
  if(reduced()||!el.matches(".cal,.viewer"))return;
  once(el,"an-x",300);
  /* de regreso en la portada: lo que se ve vuelve a entrar suave, en cascada, mientras la sección se desvanece */
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    if([...document.querySelectorAll(".cal,.viewer")].some(o=>!o.hidden))return;
    const H=innerHeight,HOME=".hero .inst,.hero .kicker,.hero h1,.hero .motto,.hero .resume,.hero .seal,.band .in>div,"+HOME_SEL.join(",");
    const vis=[...document.querySelectorAll(HOME)].filter(e=>{if(e.closest(".cal,.viewer")||e.classList.contains("an-r")||e.hidden)return false;const r=e.getBoundingClientRect();return r.height>0&&r.bottom>0&&r.top<H});
    vis.slice(0,14).forEach((e,i)=>{e.style.setProperty("--an-i",i);once(e,"an-k",1300)});
    if(vis.some(e=>e.closest(".band")))countUp();
  }));
}
new MutationObserver(ms=>{for(const m of ms){const t=m.target;
    if(m.type==="childList"){for(const n of m.addedNodes)if(n.tagName==="IFRAME"&&!n.hidden)opened(n);continue}
    if(m.oldValue!==null&&!t.hidden)opened(t);else if(m.oldValue===null&&t.hidden)closed(t)}})
  .observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:["hidden"],attributeOldValue:true});

/* 4. Desplegables (<details>): el contenido entra suave al abrir */
document.addEventListener("toggle",e=>{const d=e.target;if(d.tagName==="DETAILS"&&d.open&&!reduced())once(d,"an-d",500)},true);

/* 5. Dentro de semestres, guías y materiales (iframes de la misma página): aparición suave de sus tarjetas.
   Se detectan solas (sombra o esquinas redondeadas con fondo/borde) para no tocar el código de cada guía. */
const ICSS=`@media (prefers-reduced-motion:no-preference){
.an-ir{opacity:0!important}
.an-ir.an-it{transform:translateY(14px)!important}
.an-ir.an-iv{opacity:1!important;transform:none!important;transition:opacity .5s ${EASE} var(--an-d,0s),transform .5s ${EASE} var(--an-d,0s)!important}
@keyframes anRiseI{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.an-id>:not(summary){animation:anRiseI .3s ${EASE} both}
@keyframes anVIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes anVOut{from{opacity:1;transform:none}to{opacity:0;transform:translateY(12px)}}
#viewer.an-vi{animation:anVIn .32s ${EASE} both}
#viewer.an-vx[hidden]{display:var(--an-disp,block)!important;pointer-events:none;animation:anVOut .26s ease-in both}}`;
function inner(f){
  let w,d;try{w=f.contentWindow;d=f.contentDocument}catch(e){return}
  if(!w||!d||!d.body||w.__carreraAnim||reduced())return;w.__carreraAnim=true;
  const st=d.createElement("style");st.textContent=ICSS;(d.head||d.body).appendChild(st);
  const seen=new WeakSet(),SKIP="input,textarea,select,label,option,nav,[role=tablist],[role=dialog],dialog,iframe,video,canvas";
  const typing=()=>{const a=d.activeElement;return a&&/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName)};
  const inSeen=e=>{for(let p=e;p&&p!==d.body;p=p.parentElement)if(seen.has(p))return true;return false};
  let k=0,kt=0;
  const io=new w.IntersectionObserver(es=>{
    const now=w.performance.now();if(now-kt>250)k=0;kt=now;
    for(const x of es){if(!x.isIntersecting)continue;const e=x.target;io.unobserve(e);
      e.style.setProperty("--an-d",Math.min(k++,8)*0.05+"s");
      w.requestAnimationFrame(()=>e.classList.add("an-iv"));
      w.setTimeout(()=>{e.classList.remove("an-ir","an-it","an-iv");e.style.removeProperty("--an-d")},1000)}
  },{rootMargin:"0px 0px -4% 0px",threshold:0.05});
  function scan(root,animate){
    const H=w.innerHeight,list=root===d.body?d.body.querySelectorAll("*"):[root,...root.querySelectorAll("*")];let n=0;
    for(const e of list){
      if(seen.has(e)||n>400)continue;
      if(e.matches(SKIP)||e.closest(SKIP))continue;
      const cs=w.getComputedStyle(e);if(cs.display==="none"||cs.display==="contents"||cs.position!=="static"&&cs.position!=="relative")continue;
      const r=e.getBoundingClientRect();if(r.width<120||r.height<40||r.height>H*1.4)continue;
      const card=cs.boxShadow!=="none"||(parseFloat(cs.borderTopLeftRadius)>=6&&(cs.backgroundColor!=="rgba(0, 0, 0, 0)"||parseFloat(cs.borderTopWidth)>0));
      if(!card||inSeen(e))continue;
      seen.add(e);n++;
      if(!animate||cs.animationName!=="none")continue;
      e.classList.add("an-ir");if(cs.transform==="none")e.classList.add("an-it");io.observe(e);
    }
  }
  scan(d.body,true);
  /* pestañas, buscadores y temas que aparecen después: se revisa solo lo que cambió, antes de pintar */
  new w.MutationObserver(ms=>{
    if(reduced())return;const quiet=typing(),roots=new Set();
    for(const m of ms){const t=m.target;if(m.type==="attributes"&&seen.has(t))continue;if(t&&t.nodeType===1)roots.add(t)}
    for(const r of roots)if(r.isConnected&&![...roots].some(o=>o!==r&&o.contains(r)))scan(r,!quiet)
  }).observe(d.body,{subtree:true,childList:true,attributes:true,attributeFilter:["class","hidden","open","style"]});
  d.addEventListener("toggle",e=>{const x=e.target;if(x.tagName==="DETAILS"&&x.open&&!reduced())once(x,"an-id",500)},true);
  /* cada página de semestre abre sus guías en su propio #viewer: entra y sale suave */
  const v=d.getElementById("viewer");
  if(v){
    if(!v.hidden)v.style.setProperty("--an-disp",w.getComputedStyle(v).display);
    new w.MutationObserver(()=>{if(reduced())return;
      if(!v.hidden){v.classList.remove("an-vx");v.style.setProperty("--an-disp",w.getComputedStyle(v).display);once(v,"an-vi",450)}
      else if(v.style.getPropertyValue("--an-disp")){v.classList.remove("an-vi");once(v,"an-vx",300)}
    }).observe(v,{attributes:true,attributeFilter:["hidden"]});
  }
  d.addEventListener("load",e=>{const x=e.target;if(x&&x.tagName==="IFRAME")inner(x)},true);
  d.querySelectorAll("iframe").forEach(x=>{try{if(x.contentDocument&&x.contentDocument.readyState==="complete"&&x.contentDocument.body&&x.contentDocument.body.childElementCount)inner(x)}catch(e){}});
}
document.addEventListener("load",e=>{const f=e.target;if(f&&f.tagName==="IFRAME"&&f.closest(".viewer"))inner(f)},true);
document.querySelectorAll(".viewer iframe").forEach(f=>{try{if(f.contentDocument&&f.contentDocument.readyState==="complete")inner(f)}catch(e){}});

const start=()=>{reveal();countUp()};
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);else start();
})();
