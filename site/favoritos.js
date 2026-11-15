/* Favoritos por semestre: una estrella en cada materia; las favoritas salen primero en su semestre
   (las demás conservan su orden original). Se guarda en localStorage "carrera-favoritos" como
   {"s5":["gastro","psiquiatria"],...} y viaja con la sincronización Mac ↔ cel como lo demás.
   Cada página de semestre llama Fav.init({...}) justo después de su script; la estrella toma la
   forma de su diseño (skin): circle, ribbon, tab o glass. */
(function(){
"use strict";
if(window.Fav)return;
const KEY="carrera-favoritos";
const load=()=>{try{const o=JSON.parse(localStorage.getItem(KEY)||"{}");return o&&typeof o==="object"&&!Array.isArray(o)?o:{}}catch(e){return{}}};
const save=o=>{try{for(const k of Object.keys(o))if(!Array.isArray(o[k])||!o[k].length)delete o[k];
  if(Object.keys(o).length)localStorage.setItem(KEY,JSON.stringify(o));else localStorage.removeItem(KEY)}catch(e){}};
const reduce=()=>{try{return matchMedia("(prefers-reduced-motion: reduce)").matches}catch(e){return false}};
const STAR='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 3.3l2.68 5.43 5.99.87-4.33 4.23 1.02 5.96L12 17l-5.36 2.82 1.02-5.96L3.33 9.6l5.99-.87z"/></svg>';
const DARK_OFF="background:rgba(17,22,30,.82);color:#fff;box-shadow:0 4px 14px -6px rgba(0,0,0,.7)";
const STYLE=`
.fav-w{position:relative;display:grid;min-width:0}
.fav-h{position:relative}
.fav-w>*{min-width:0}
.fav{position:absolute;z-index:6;top:12px;right:12px;width:36px;height:36px;display:grid;place-items:center;margin:0;padding:0;border:0;cursor:pointer;
 border-radius:999px;color:#14202b;background:rgba(255,255,255,.93);box-shadow:0 4px 14px -6px rgba(0,0,0,.45);
 -webkit-tap-highlight-color:transparent;touch-action:manipulation;transition:transform .18s ease,background-color .18s ease,color .18s ease}
.fav svg{width:19px;height:19px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linejoin:round;pointer-events:none}
.fav[aria-pressed="true"]{background:#f26b21;color:#fff}
.fav[aria-pressed="true"] svg{fill:currentColor}
.fav:hover{transform:scale(1.08)}
.fav:focus-visible{outline:2px solid #f26b21;outline-offset:2px}
.fav.pop{animation:favPop .38s cubic-bezier(.3,.7,.3,1.4)}
@keyframes favPop{0%{transform:scale(.7)}60%{transform:scale(1.2)}100%{transform:scale(1)}}
.fav-w:hover>.fav{transform:translateY(var(--fav-lift,-2px))}
.fav-w:hover>.fav:hover{transform:translateY(var(--fav-lift,-2px)) scale(1.08)}
/* laminilla / ficha / carpeta del anaquel: esquina de etiqueta */
.fav.fav--tab{border-radius:9px}
/* carpeta de 4º: vidrio como la etiqueta de la portada */
.fav.fav--glass{color:#fff;background:rgba(0,0,0,.32);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);box-shadow:none}
.fav.fav--glass[aria-pressed="true"]{background:#f26b21}
/* libreta y estante: separador de listón que cuelga del borde */
.fav.fav--ribbon{top:0;right:18px;width:32px;height:46px;border-radius:0;padding-top:7px;place-items:start center;box-shadow:none;
 clip-path:polygon(0 0,100% 0,100% 100%,50% 80%,0 100%)}
.fav.fav--ribbon svg{width:17px;height:17px}
.fav.fav--ribbon:hover,.fav-w:hover>.fav.fav--ribbon:hover{transform:translateY(3px)}
.fav-w:hover>.fav.fav--ribbon{transform:translateY(var(--fav-lift,-2px))}
.fav.fav--ribbon.pop{animation:favDrop .42s cubic-bezier(.3,.7,.3,1.4)}
@keyframes favDrop{0%{transform:translateY(-14px)}70%{transform:translateY(3px)}100%{transform:none}}
.fav-live{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .fav:not([aria-pressed="true"]):not(.fav--glass){${DARK_OFF}}}
:root[data-theme="dark"] .fav:not([aria-pressed="true"]):not(.fav--glass){${DARK_OFF}}
@media (prefers-reduced-motion: reduce){.fav,.fav-w:hover>.fav,.fav:hover{transition:none!important;animation:none!important;transform:none!important}}
`;

function init(c){
  if(!c||!Array.isArray(c.list)||!c.sem)return;
  const d=document,list=c.list,sem=c.sem;
  const grid=typeof c.grid==="string"?d.querySelector(c.grid):c.grid;if(!grid)return;
  if(!d.getElementById("fav-css")){const st=d.createElement("style");st.id="fav-css";st.textContent=STYLE;(d.head||d.documentElement).appendChild(st)}
  const live=d.createElement("span");live.className="fav-live";live.setAttribute("aria-live","polite");d.body.appendChild(live);
  const orig=new Map(list.map((it,i)=>[it.id,i]));
  const name=it=>c.name?c.name(it):(it.titulo||it.title||it.materia||it.id);
  const favs=()=>{const a=load()[sem];return Array.isArray(a)?a.filter(x=>typeof x==="string"):[]};
  const is=id=>favs().includes(id);
  function sort(){
    const f=favs(),rank=id=>{const k=f.indexOf(id);return k<0?1e6+(orig.has(id)?orig.get(id):1e5):k};
    /* favoritas en el orden en que se marcaron; el resto en su orden original */
    list.sort((a,b)=>rank(a.id)-rank(b.id));
  }
  function decorate(){
    const f=favs();
    grid.querySelectorAll(c.card).forEach(card=>{
      const id=c.id(card);if(!id||!orig.has(id))return;
      let host=card,btn;
      if(c.wrap){
        host=card.parentElement&&card.parentElement.classList.contains("fav-w")?card.parentElement:null;
        if(!host){host=d.createElement("div");host.className="fav-w";card.parentNode.insertBefore(host,card);host.appendChild(card)}
      }
      if(!c.wrap)host.classList.add("fav-h");
      host.dataset.favId=id;
      btn=host.querySelector(":scope>.fav");
      if(!btn){btn=d.createElement("button");btn.type="button";btn.className="fav"+(c.skin?" fav--"+c.skin:"");btn.dataset.fav=id;btn.innerHTML=STAR;
        if(c.wrap)host.appendChild(btn);else host.insertBefore(btn,host.firstChild)}
      const on=f.includes(id),it=list.find(x=>x.id===id),n=it?name(it):id;
      btn.setAttribute("aria-pressed",on?"true":"false");
      btn.setAttribute("aria-label",(on?"Quitar de favoritas: ":"Poner en favoritas: ")+n);
      btn.title=on?"Quitar de favoritas":"Favorita: que salga primero";
      card.classList.toggle("fav-on",on);
    });
  }
  function paint(anim){
    const before=new Map();
    if(anim&&!reduce())grid.querySelectorAll("[data-fav-id]").forEach(el=>before.set(el.dataset.favId,el.getBoundingClientRect()));
    sort();
    try{c.render()}catch(e){}
    decorate();
    if(c.after)try{c.after(is)}catch(e){}
    if(!before.size)return;
    grid.querySelectorAll("[data-fav-id]").forEach(el=>{
      const b=before.get(el.dataset.favId);if(!b||!el.animate)return;
      const a=el.getBoundingClientRect(),dx=b.left-a.left,dy=b.top-a.top;
      if(Math.abs(dx)<1&&Math.abs(dy)<1)return;
      el.animate([{transform:`translate(${dx}px,${dy}px)`},{transform:"none"}],{duration:420,easing:"cubic-bezier(.2,.8,.2,1)"});
    });
  }
  function toggle(id){
    const all=load(),f=Array.isArray(all[sem])?all[sem].filter(x=>x!==id&&orig.has(x)):[];
    const on=!is(id);if(on)f.push(id);all[sem]=f;save(all);
    const it=list.find(x=>x.id===id);
    live.textContent=it?(on?name(it)+" está en favoritas y sale primero":name(it)+" ya no está en favoritas"):"";
    paint(true);
    const b=grid.querySelector(`.fav[data-fav="${CSS.escape?CSS.escape(id):id}"]`);
    if(b){if(on&&!reduce()){b.classList.remove("pop");void b.offsetWidth;b.classList.add("pop")}b.focus({preventScroll:true})}
  }
  /* la estrella no abre la materia */
  grid.addEventListener("click",e=>{const b=e.target.closest(".fav");if(!b||!grid.contains(b))return;
    e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();toggle(b.dataset.fav)},true);
  /* búsquedas, filtros y cambios de tema vuelven a dibujar las tarjetas */
  let busy=false;
  new MutationObserver(()=>{if(busy)return;busy=true;try{decorate()}finally{busy=false}}).observe(grid,{childList:true});
  /* lo que llega del otro aparato */
  addEventListener("storage",e=>{if(e.key===KEY||e.key===null)paint(false)});
  paint(false);
}
window.Fav={init};
})();
