/* Botón «Seguir leyendo en AMBOSS» al final de cada subtema de las guías.
   Fuente: tools-amboss/amboss.src.js + tools-amboss/terminos.tsv → python3 tools-amboss/build.py → site/amboss.js
   Es solo un enlace: abre la búsqueda de AMBOSS (en inglés) con el término del subtema, en el navegador,
   y ahí entras con tu cuenta. No copia nada de AMBOSS.
   Cada guía carga este archivo con data-g="<id>" (lo pone patch_amboss.py); CFG dice dónde están sus subtemas. */
(function(){
if(window.__amb)return;
var TAB=/*TABLA*/{}/*FIN*/;
var BASE="https://next.amboss.com/us/search?v=overview&q=";
var me=document.currentScript||document.querySelector("script[data-amb-g]");
var G=(me&&me.getAttribute("data-amb-g"))||"";
var S12={h:"details.sub>summary",t:"h3",c:[["article.tema",".thead h2"]]};
/* h: título del subtema · t: dónde está el texto dentro del título · c: [caja, título] del tema que lo contiene
   b: caja del subtema (el botón va al final de ella) · si no hay b y el título es <summary>, va al final de su <details>;
   si no, va justo antes del siguiente subtema (o al final de su contenedor) */
var CFG={
 "s12":S12,
 "s3-farmacologia":{h:"details.sec>summary",c:[["main",".label-body h2"]]},
 "s3-anatomia":{h:"details.topic>summary",t:".tt",c:[["section.unit",".unit-h h2"]]},
 "s4-cirugia":{h:"article.topic .tbody h3",c:[["article.topic",".thead h2"]]},
 "s4-farmacologia-ii":{h:"details.drug>summary,.key h4",t:".nm",b:".key",c:[["section.group","h3"],["main",".thead h2"]]},
 "s4-hematologia":{h:"article.note h3",c:[["article.note","h2"]]},
 "s4-inmunologia":{h:"section.topic h3",c:[["section.topic",".topic-head h2"]]},
 "s4-nutricion":{h:"article.label h3",c:[["article.label","h2"]]},
 "s4-simulacion-iv":{h:"div.panel h3",b:"div.panel"},
 "s5-cirugia":{h:"details.card>summary",t:".ti",c:[["#view",".cover h1"]]},
 "s5-tp":{h:"details.sec>summary",c:[["article.tp","h1"]]},
 "s5-imagenologia":{h:"details.topic>summary",t:".tt",c:[["section.unit",".unit-h h2"]]},
 "s5-oftalmo":{h:"details.topic>summary",t:".t-title",c:[["section.block",".block-h h2"]]},
 "s5-otorrino":{h:"section.sec h3",b:"section.sec",c:[["main",".thead h1"]]},
 "s5-psiquiatria":{h:"section.tema h3",c:[["section.tema",".tema-head h2"]]},
 "s6-infectologia":{h:"section.topic>h3,details.org>summary",t:".org-name",c:[["section.topic",".topic-head h2"]]},
 "s6-salud-publica":{h:"section.sec h3",b:"section.sec"},
 "x-signos":{h:"details.topic>summary",t:".tt",c:[["section.unit",".unit-h h2"]]},
 "x-triage":{h:"details.topic>summary"},
 "x-slides":{h:"#scaler>section h2",b:"section",abs:1}
};
var cfg=CFG[G]||CFG[G.replace(/^(s[123])-.*/,"s12")];
if(!cfg)return;
var DROP=".n,.no,.num,.sn,.kd,.tag,.cam,.mod,.meta,.hint,.chev,.done-ic,.cnt,.amb-btn,small,svg";
function norm(s){return String(s||"").normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase()
  .replace(/^\s*(clase|tema)?\s*\d+(\.\d+)*\s*[·.\-:)]?\s*/,"").replace(/\s*\d+\s*(img|imagen(es)?|tarjetas?)\b.*$/,"")
  .replace(/[✓★†*]/g,"").replace(/\s+/g," ").trim()}
function txt(el,tsel){
  var x=tsel&&el.querySelector(tsel);if(x)return x.textContent;
  var c=el.cloneNode(true);c.querySelectorAll(DROP).forEach(function(n){n.remove()});return c.textContent}
function ctxOf(h){
  for(var i=0;cfg.c&&i<cfg.c.length;i++){var box=h.closest(cfg.c[i][0]);if(!box)continue;var t=box.querySelector(cfg.c[i][1]);if(t&&t!==h)return txt(t)}
  return ""}
var seen={};
function query(title,ctx){
  var nt=norm(title),nc=norm(ctx),v=TAB[nc+" › "+nt];
  if(v==null)v=TAB[nt];
  if(v==null&&TAB["* "+nt]!=null){var ce=TAB[nc];v=ce&&ce!=="-"?(ce+" "+TAB["* "+nt]).trim():null}
  seen[nc+" › "+nt]=[title.trim(),ctx.trim(),v==null?0:1];
  if(v==null){var c2=TAB[nc];return c2&&c2!=="-"?c2:title.trim()}
  return v==="-"?"":v}
function mk(q){
  var a=document.createElement("a");a.className="amb-btn"+(cfg.abs?" amb-abs":"");a.href=BASE+encodeURIComponent(q);a.target="_blank";a.rel="noopener";
  a.title="Abre AMBOSS en tu navegador: "+q;a.setAttribute("data-amb","");
  a.innerHTML='<span class="amb-a" aria-hidden="true">A</span><span>Seguir leyendo en AMBOSS</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>';
  a.addEventListener("click",function(e){e.stopPropagation()});
  var w=document.createElement("div");w.className="amb-w";w.appendChild(a);return w}
function place(h,w){
  if(cfg.b){var bx=h.closest(cfg.b);if(bx){bx.appendChild(w);return}}
  if(h.tagName==="SUMMARY"){h.parentElement.appendChild(w);return}
  var all=[].slice.call(document.querySelectorAll(cfg.h));
  var n=h.nextElementSibling;
  while(n){if(n.matches(cfg.h)||all.some(function(x){return n.contains(x)}))break;n=n.nextElementSibling}
  if(n)n.parentElement.insertBefore(w,n);else h.parentElement.appendChild(w)}
function run(){
  document.querySelectorAll(cfg.h).forEach(function(h){
    if(h.__amb||h.closest(".amb-w"))return;
    var title=txt(h,cfg.t);if(!norm(title))return;
    h.__amb=1;var q=query(title,ctxOf(h));if(!q)return;place(h,mk(q))});
  /* temas sin subtemas: un botón al final del tema */
  if(cfg.c)document.querySelectorAll(cfg.c[0][0]).forEach(function(box){
    if(box.__amb||box.querySelector(cfg.h))return;var t=box.querySelector(cfg.c[0][1]);if(!t||!norm(txt(t)))return;
    box.__amb=1;var tt=txt(t),nt=norm(tt),v=TAB[nt];seen[nt+" › "]=[tt.trim(),"",v==null?0:1];
    if(v==="-")return;box.appendChild(mk(v||tt.trim()))})}
var css=document.createElement("style");
css.textContent='.amb-w{display:flex;justify-content:flex-end;margin:12px 0 4px;clear:both}'+
 '.amb-btn{display:inline-flex;align-items:center;gap:8px;font:600 13px/1.2 system-ui,-apple-system,"Segoe UI",sans-serif;color:#0b6b5c;background:rgba(14,138,118,.08);border:1px solid rgba(14,138,118,.35);border-radius:999px;padding:7px 13px 7px 8px;text-decoration:none!important;cursor:pointer;transition:background .15s,border-color .15s}'+
 '.amb-btn:hover{background:rgba(14,138,118,.16);border-color:rgba(14,138,118,.6)}'+
 '.amb-btn .amb-a{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#0e8a76;color:#fff;font:800 11px/1 system-ui,sans-serif}'+
 '.amb-btn svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}'+
 'details>.amb-w{margin:6px 14px 12px}'+
 '.amb-abs{position:absolute;right:28px;bottom:22px;z-index:5;transform:scale(1.8);transform-origin:100% 100%}.amb-w:has(.amb-abs){margin:0}'+
 '@media (prefers-color-scheme:dark){.amb-btn{color:#7fd8c6;background:rgba(127,216,198,.1);border-color:rgba(127,216,198,.35)}}'+
 'html[data-theme=dark] .amb-btn,body.dark .amb-btn,html.dark .amb-btn{color:#7fd8c6;background:rgba(127,216,198,.1);border-color:rgba(127,216,198,.35)}'+
 'html[data-theme=light] .amb-btn{color:#0b6b5c;background:rgba(14,138,118,.08);border-color:rgba(14,138,118,.35)}'+
 '@media print{.amb-w{display:none}}';
(document.head||document.documentElement).appendChild(css);
var tm=0;function sch(){clearTimeout(tm);tm=setTimeout(run,120)}
window.__amb={seen:seen,run:run,q:query,norm:norm};
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",run);else run();
new MutationObserver(function(m){for(var i=0;i<m.length;i++){if(m[i].addedNodes.length){sch();return}}}).observe(document.documentElement,{childList:true,subtree:true});
})();
