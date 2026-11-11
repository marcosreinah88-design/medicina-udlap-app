/* Animaciones discretas de la portada y sus secciones.
   - Al abrir un semestre, una guía o una sección (Calendario, Calificaciones, Estudio, CTO...) entra con un fundido corto
     y sus tarjetas suben un poco, una tras otra.
   - En la portada las tarjetas aparecen suavemente al bajar con el scroll y los números de la franja naranja cuentan hasta su valor.
   - Botones con respuesta sutil al pasar el mouse y al tocarlos.
   Solo usa opacidad y desplazamiento (no cambia colores, así que el modo oscuro queda igual) y se apaga por completo
   si el sistema tiene activado "Reducir movimiento". No toca las páginas originales de cada semestre ni de las guías. */
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
function reveal(){
  if(reduced()||!("IntersectionObserver" in window))return;
  const sel=["main .hday","main .search","main .sec-h","main .track",".sems .stile",".extra .sec-h",".extra .xcard","body>footer .in"];
  const els=[...document.querySelectorAll(sel.join(","))].filter(e=>!e.closest(".cal,.viewer"));
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
  once(el,"an-o",400);
  const cs=[...el.querySelectorAll(CARDS)].filter(c=>!c.parentElement.closest(CARDS)).slice(0,10);
  cs.forEach((c,i)=>{c.style.setProperty("--an-i",i);once(c,"an-k",1200)});
}
new MutationObserver(ms=>{for(const m of ms){const t=m.target;if(m.oldValue!==null&&!t.hidden)opened(t)}})
  .observe(document.body,{subtree:true,attributes:true,attributeFilter:["hidden"],attributeOldValue:true});

/* 4. Desplegables (<details>): el contenido entra suave al abrir */
document.addEventListener("toggle",e=>{const d=e.target;if(d.tagName==="DETAILS"&&d.open&&!reduced())once(d,"an-d",500)},true);

const start=()=>{reveal();countUp()};
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);else start();
})();
