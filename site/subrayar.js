/* Subrayador: dentro de semestres, guías y materiales, selecciona un texto y elige un color para subrayarlo.
   Se guarda por página en localStorage "carrera-subrayados" (se sincroniza Mac ↔ cel como lo demás).
   Tocar un subrayado deja cambiarle el color o quitarlo. No toca el diseño de las guías. */
(function(){
"use strict";
if(window.__carreraSub)return;window.__carreraSub=true;
const KEY="carrera-subrayados";
const COLORS=[["am","Amarillo","rgba(255,213,0,.5)"],["ve","Verde","rgba(80,200,120,.42)"],["ro","Rosa","rgba(255,105,170,.4)"],["az","Azul","rgba(80,160,255,.4)"]];
const CMAP=Object.fromEntries(COLORS.map(c=>[c[0],c[2]]));
const SKIPTAG=/^(SCRIPT|STYLE|NOSCRIPT|TEXTAREA|INPUT|SELECT|OPTION|SVG|svg|CANVAS|IFRAME|TEMPLATE)$/;
const load=()=>{try{const o=JSON.parse(localStorage.getItem(KEY)||"{}");return o&&typeof o==="object"&&!Array.isArray(o)?o:{}}catch(e){return{}}};
const save=o=>{try{for(const k of Object.keys(o))if(!o[k].length)delete o[k];localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}};
const clean=h=>h&&typeof h.id==="string"&&/^[a-z0-9]{4,20}$/.test(h.id)&&typeof h.t==="string"&&h.t.length>0&&h.t.length<=5000&&CMAP[h.c];
const uid=()=>Date.now().toString(36)+Math.random().toString(36).slice(2,6);

const CSS=`mark.sbx{background:var(--sbx)!important;color:inherit!important;padding:0!important;margin:0!important;border-radius:2px;
-webkit-box-decoration-break:clone;box-decoration-break:clone;cursor:pointer;font:inherit!important;text-decoration:inherit}
mark.sbx.sbx-on{outline:2px solid rgba(242,107,33,.75);outline-offset:1px}
.sbx-bar{position:fixed;z-index:2147483646;display:flex;align-items:center;gap:6px;padding:7px 9px;border-radius:999px;
background:#1f2a26;box-shadow:0 6px 22px rgba(0,0,0,.28),0 0 0 1px rgba(255,255,255,.08);font:600 13px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
color:#fff;-webkit-user-select:none;user-select:none;touch-action:manipulation;animation:sbxIn .14s ease-out}
@keyframes sbxIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
.sbx-bar[hidden]{display:none}
.sbx-all{left:max(12px,env(safe-area-inset-left,0px));bottom:calc(12px + env(safe-area-inset-bottom,0px));padding:5px;opacity:.92}
.sbx-all .sbx-l{padding-left:8px}
.sbx-bar button.x.warn{background:#c0392b}
.sbx-bar .sbx-l{padding:0 4px 0 2px;opacity:.85;white-space:nowrap}
.sbx-bar button{all:unset;box-sizing:border-box;width:28px;height:28px;border-radius:50%;cursor:pointer;display:grid;place-items:center;flex:none}
.sbx-bar button.c{border:2px solid rgba(255,255,255,.85)}
.sbx-bar button.c.sel{box-shadow:0 0 0 2px #f26b21}
.sbx-bar button.x{width:auto;height:28px;border-radius:999px;padding:0 10px;background:rgba(255,255,255,.12);gap:5px;display:flex;align-items:center}
.sbx-bar button:focus-visible{outline:2px solid #f26b21;outline-offset:2px}
.sbx-bar svg{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
@media print{.sbx-bar{display:none!important}}`;
const SOLID={am:"#ffd500",ve:"#50c878",ro:"#ff69aa",az:"#50a0ff"};
const TRASH='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 12.5A1.6 1.6 0 0 0 8.6 21h6.8a1.6 1.6 0 0 0 1.6-1.5L18 7M9 7V4.5h6V7"/></svg>';

function pageKey(w){
  let p="";try{p=decodeURIComponent(w.location.pathname||"")}catch(e){}
  const m=p.match(/(?:^|\/)((?:s\d+|x)\/.+)$/);
  if(m)return m[1].replace(/\/$/,"/index.html");
  try{return "doc:"+(w.document.title||p).slice(0,80)}catch(e){return "doc:"+p}
}

function attach(w){
  let d;try{d=w.document}catch(e){return}
  if(!d||!d.body||w.__carreraSubIn)return;w.__carreraSubIn=true;
  const key=pageKey(w);
  const st=d.createElement("style");st.textContent=CSS;(d.head||d.body).appendChild(st);

  /* texto de la página como una sola cadena, con el lugar de cada nodo */
  function textMap(){
    const list=[];let pos=0;
    const tw=d.createTreeWalker(d.body,4,{acceptNode(n){
      for(let p=n.parentNode;p&&p!==d.body;p=p.parentNode){if(p.nodeType===1&&(SKIPTAG.test(p.tagName)||p.classList.contains("sbx-bar")))return 2}
      return 1}});
    let n;while((n=tw.nextNode())){list.push({n,s:pos});pos+=n.data.length}
    return {list,str:list.map(x=>x.n.data).join("")};
  }
  function pointOff(map,c,o){
    if(c.nodeType===3){const e=map.list.find(x=>x.n===c);if(e)return e.s+o}
    const ch=c.nodeType===3?c:c.childNodes[o];
    if(ch){for(const x of map.list){if(ch===x.n||ch.contains(x.n)||(ch.compareDocumentPosition(x.n)&4))return x.s}return map.str.length}
    let last=null;for(const x of map.list){if(c.contains(x.n))last=x;else if(last)break}
    if(last)return last.s+last.n.data.length;
    for(const x of map.list)if(c.compareDocumentPosition(x.n)&4)return x.s;
    return map.str.length;
  }
  let busy=false;
  function wrap(map,a,b,h){
    busy=true;
    try{
      for(const x of map.list){
        const s=x.s,e=s+x.n.data.length;if(e<=a||s>=b)continue;
        let node=x.n;const from=Math.max(a,s)-s,to=Math.min(b,e)-s;
        if(!node.data.slice(from,to).trim())continue;
        const par=node.parentNode;if(!par||/^(TABLE|TBODY|THEAD|TFOOT|TR|UL|OL|DL|SELECT)$/.test(par.tagName))continue;
        if(from>0)node=node.splitText(from);
        if(to-from<node.data.length)node.splitText(to-from);
        const m=d.createElement("mark");m.className="sbx";m.dataset.sb=h.id;m.style.setProperty("--sbx",CMAP[h.c]);
        node.parentNode.insertBefore(m,node);m.appendChild(node);
      }
    }finally{busy=false}
  }
  function unwrap(id){
    busy=true;
    try{d.querySelectorAll('mark.sbx[data-sb="'+id+'"]').forEach(m=>{const p=m.parentNode;while(m.firstChild)p.insertBefore(m.firstChild,m);p.removeChild(m);p.normalize()})}
    finally{busy=false}
  }
  function locate(map,h){
    const str=map.str;let best=-1,score=-1,i=str.indexOf(h.t);
    while(i>=0){
      let sc=0;const pre=str.slice(Math.max(0,i-(h.p||"").length),i),suf=str.slice(i+h.t.length,i+h.t.length+(h.s||"").length);
      for(let k=1;k<=pre.length&&pre[pre.length-k]===h.p[h.p.length-k];k++)sc++;
      for(let k=0;k<suf.length&&suf[k]===h.s[k];k++)sc++;
      if(sc>score){score=sc;best=i}
      i=str.indexOf(h.t,i+1);
    }
    return best;
  }
  function applyAll(){
    const all=(load()[key]||[]).filter(clean);if(!all.length)return;
    const missing=all.filter(h=>!d.querySelector('mark.sbx[data-sb="'+h.id+'"]'));if(!missing.length)return;
    let map=textMap();
    for(const h of missing){const i=locate(map,h);if(i<0)continue;wrap(map,i,i+h.t.length,h);map=textMap()}
  }

  /* barra flotante */
  const bar=d.createElement("div");bar.className="sbx-bar";bar.hidden=true;bar.setAttribute("role","toolbar");bar.setAttribute("aria-label","Subrayar");
  d.body.appendChild(bar);
  let pending=null,current=null,overlap=new Set();
  function hide(){bar.hidden=true;pending=null;overlap=new Set();if(current)d.querySelectorAll("mark.sbx.sbx-on").forEach(m=>m.classList.remove("sbx-on"));current=null}
  function place(r){
    bar.hidden=false;
    const vw=w.innerWidth,vh=w.innerHeight,bw=bar.offsetWidth,bh=bar.offsetHeight;
    let x=Math.min(Math.max(8,r.left+r.width/2-bw/2),vw-bw-8);
    let y=r.bottom+10;if(y+bh>vh-8)y=r.top-bh-10;if(y<8)y=Math.min(vh-bh-8,Math.max(8,r.top+8));
    bar.style.left=x+"px";bar.style.top=y+"px";
  }
  function render(sel){
    bar.innerHTML='<span class="sbx-l">'+(current?"Subrayado":"Subrayar")+'</span>'+
      COLORS.map(c=>'<button type="button" class="c'+(sel===c[0]?" sel":"")+'" data-c="'+c[0]+'" style="background:'+SOLID[c[0]]+'" aria-label="'+c[1]+'" title="'+c[1]+'"></button>').join("")+
      (current||overlap.size?'<button type="button" class="x" data-x="1" aria-label="Quitar subrayado">'+TRASH+'Quitar</button>':"");
  }
  const keep=e=>{e.preventDefault()};
  bar.addEventListener("mousedown",keep);bar.addEventListener("touchstart",e=>{if(e.target.closest("button"))keep(e)},{passive:false});
  bar.addEventListener("click",e=>{
    const b=e.target.closest("button");if(!b)return;e.preventDefault();e.stopPropagation();
    const all=load(),arr=(all[key]||[]).filter(clean);
    if(current){
      const h=arr.find(x=>x.id===current);
      if(b.dataset.x){all[key]=arr.filter(x=>x.id!==current);save(all);unwrap(current);count()}
      else if(h&&b.dataset.c){h.c=b.dataset.c;all[key]=arr;save(all);d.querySelectorAll('mark.sbx[data-sb="'+h.id+'"]').forEach(m=>m.style.setProperty("--sbx",CMAP[h.c]))}
      hide();return;
    }
    if(pending&&b.dataset.x){all[key]=arr.filter(x=>!overlap.has(x.id));save(all);overlap.forEach(unwrap);try{w.getSelection().removeAllRanges()}catch(e){}hide();count();return}
    if(!pending||!b.dataset.c)return hide();
    const map=textMap(),a=pointOff(map,pending.startContainer,pending.startOffset),z=pointOff(map,pending.endContainer,pending.endOffset);
    if(!(z>a)){hide();return}
    let A=a,Z=z;while(A<Z&&/\s/.test(map.str[A]))A++;while(Z>A&&/\s/.test(map.str[Z-1]))Z--;
    if(Z-A<1||Z-A>5000){hide();return}
    const h={id:uid(),c:b.dataset.c,t:map.str.slice(A,Z),p:map.str.slice(Math.max(0,A-40),A),s:map.str.slice(Z,Z+40),at:Date.now()};
    /* si se encima con otro subrayado, el nuevo lo reemplaza */
    const over=new Set();d.querySelectorAll("mark.sbx").forEach(m=>{try{if(pending.intersectsNode(m))over.add(m.dataset.sb)}catch(e){}});
    over.forEach(unwrap);
    const m2=over.size?textMap():map;
    const i=over.size?locate(m2,h):A;
    wrap(m2,i<0?A:i,(i<0?A:i)+h.t.length,h);
    all[key]=arr.filter(x=>!over.has(x.id)).concat(h);save(all);
    try{w.getSelection().removeAllRanges()}catch(e){}
    hide();count();
  });

  let t=0;
  d.addEventListener("selectionchange",()=>{
    clearTimeout(t);
    t=setTimeout(()=>{
      const s=w.getSelection();
      if(!s||s.isCollapsed||!s.rangeCount){if(!current)hide();return}
      const r=s.getRangeAt(0);
      if(!d.body.contains(r.commonAncestorContainer)||bar.contains(r.commonAncestorContainer))return;
      const anc=r.commonAncestorContainer.nodeType===1?r.commonAncestorContainer:r.commonAncestorContainer.parentElement;
      if(anc&&anc.closest&&anc.closest("input,textarea,[contenteditable=''],[contenteditable=true]"))return;
      if(!s.toString().trim())return;
      if(current){d.querySelectorAll("mark.sbx.sbx-on").forEach(m=>m.classList.remove("sbx-on"));current=null}
      pending=r.cloneRange();overlap=new Set();
      d.querySelectorAll("mark.sbx").forEach(m=>{try{if(r.intersectsNode(m))overlap.add(m.dataset.sb)}catch(e){}});
      render(null);
      const rects=r.getClientRects();const rr=rects.length?rects[rects.length-1]:r.getBoundingClientRect();
      place(rr);
    },/Mobi|iPhone|iPad|Android/.test(w.navigator.userAgent)?350:120);
  });
  d.addEventListener("click",e=>{
    if(bar.contains(e.target)||pill.contains(e.target))return;
    const m=e.target.closest&&e.target.closest("mark.sbx");
    const s=w.getSelection();
    if(m&&(!s||s.isCollapsed)){
      d.querySelectorAll("mark.sbx.sbx-on").forEach(x=>x.classList.remove("sbx-on"));
      current=m.dataset.sb;pending=null;
      const h=(load()[key]||[]).find(x=>x.id===current);
      d.querySelectorAll('mark.sbx[data-sb="'+current+'"]').forEach(x=>x.classList.add("sbx-on"));
      render(h&&h.c);place(m.getBoundingClientRect());return;
    }
    if(!bar.hidden&&(!s||s.isCollapsed))hide();
  },true);
  w.addEventListener("scroll",()=>{if(!bar.hidden&&current)hide()},{passive:true});
  d.addEventListener("keydown",e=>{if(e.key==="Escape"&&!bar.hidden)hide()});

  /* esquina: cuántos subrayados hay en esta página y "Quitar todos" (pide confirmar con un segundo toque) */
  const pill=d.createElement("div");pill.className="sbx-bar sbx-all";pill.hidden=true;d.body.appendChild(pill);
  let sure=false,sureT=0;
  function count(){
    const n=(load()[key]||[]).filter(clean).length;
    if(!n){pill.hidden=true;sure=false;return}
    pill.hidden=false;
    pill.innerHTML=sure
      ?'<span class="sbx-l">\u00bfQuitar los '+n+'?</span><button type="button" class="x warn" data-all="go">'+TRASH+'S\u00ed, quitar</button><button type="button" class="x" data-all="no">No</button>'
      :'<button type="button" class="x" data-all="ask" aria-label="Quitar todos los subrayados de esta p\u00e1gina">'+TRASH+'Quitar subrayados ('+n+')</button>';
  }
  pill.addEventListener("mousedown",keep);
  pill.addEventListener("click",e=>{
    const b=e.target.closest("button");if(!b)return;e.preventDefault();e.stopPropagation();clearTimeout(sureT);
    if(b.dataset.all==="ask"){sure=true;sureT=setTimeout(()=>{sure=false;count()},6000)}
    else if(b.dataset.all==="go"){const all=load();(all[key]||[]).forEach(h=>unwrap(h.id));delete all[key];save(all);d.querySelectorAll("mark.sbx").forEach(m=>unwrap(m.dataset.sb));sure=false;hide()}
    else sure=false;
    count();
  });
  applyAll();count();
  /* pestañas o secciones que se dibujan después, y cambios que llegan del otro aparato */
  let mt=0;
  new w.MutationObserver(ms=>{if(busy)return;if(ms.every(m=>bar.contains(m.target)||pill.contains(m.target)))return;clearTimeout(mt);mt=setTimeout(applyAll,300)})
    .observe(d.body,{subtree:true,childList:true});
  w.addEventListener("storage",e=>{if(e.key===KEY){applyAll();count()}});

  /* guías dentro de la página del semestre */
  d.addEventListener("load",e=>{const x=e.target;if(x&&x.tagName==="IFRAME")hook(x)},true);
  d.querySelectorAll("iframe").forEach(hook);
}
function hook(f){
  try{
    const go=()=>{try{const w=f.contentWindow;if(w&&w.document&&w.document.readyState!=="loading"&&w.document.body&&w.location.href!=="about:blank")attach(w)}catch(e){}};
    go();
  }catch(e){}
}
document.addEventListener("load",e=>{const f=e.target;if(f&&f.tagName==="IFRAME")hook(f)},true);
document.querySelectorAll("iframe").forEach(hook);
})();
