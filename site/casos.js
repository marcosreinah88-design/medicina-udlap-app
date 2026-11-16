/* Casos clínicos tipo examen («Ponme a prueba») de las guías de 5º semestre. Uso:
   <script src="../../casos.js" data-cc="gastro" defer></script>
   Agrega un botón flotante «Casos clínicos» que abre los casos de esa guía (casos/<guía>.json, los arma tools-casos/build.py).
   Dos modos: «Ponme a prueba» (respuesta y justificación de cada opción al momento) y «Simulacro» (10 casos con
   cronómetro; calificación y revisión al final). Avance en localStorage carrera-casos = {"<guía>":{"<id>":[aciertos,intentos,últimaBien,fecha]}}
   (se sincroniza Mac ↔ cel como todo lo demás). † = dato que no viene de los apuntes de la guía. */
(function(){
  const me=document.currentScript;if(!me||window.__casos)return;window.__casos=1;
  const G=me.dataset.cc,BASE=me.src.replace(/[^\/]*$/,""),KEY="carrera-casos";
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const fmt=s=>esc(s).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>");
  const dark=()=>{const t=document.documentElement.dataset.theme||document.body&&document.body.dataset.theme;
    if(t)return t==="dark";try{return matchMedia("(prefers-color-scheme: dark)").matches}catch(e){return false}};
  const reduce=()=>{try{return matchMedia("(prefers-reduced-motion: reduce)").matches}catch(e){return false}};
  const CSS=`.cc{--cc-bg:#fbfaf6;--cc-card:#fff;--cc-ink:#1d2a24;--cc-mute:#5d6b64;--cc-line:#dfe3dc;--cc-g:#00573c;--cc-o:#f26b21;--cc-soft:#e8f1ec;--cc-ok:#1f7a4d;--cc-okb:#e3f3ea;--cc-bad:#b3362b;--cc-badb:#fbe9e6;
font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--cc-ink);text-align:left}
.cc[data-dark]{--cc-bg:#121815;--cc-card:#1b2420;--cc-ink:#e7ece8;--cc-mute:#a3b0a9;--cc-line:#2e3a34;--cc-g:#4fbf8f;--cc-o:#ff9558;--cc-soft:#1f3329;--cc-ok:#5fd09a;--cc-okb:#173326;--cc-bad:#ff8a7a;--cc-badb:#3a1f1b}
.cc *{box-sizing:border-box}.cc button{font:inherit;cursor:pointer;color:inherit}
.cc-fab{position:fixed;right:16px;bottom:16px;z-index:2147483000;display:flex;align-items:center;gap:8px;padding:10px 16px;border-radius:999px;border:0;background:#f26b21;color:#fff;cursor:pointer;
font:600 14px/1.2 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.22);transition:bottom .2s}
.cc-fab small{background:#00573c;border-radius:999px;padding:2px 8px;font-weight:700}
.cc-fab svg{width:18px;height:18px;flex:none}
.cc-ov{position:fixed;inset:0;z-index:2147483001;background:rgba(10,20,15,.55);display:flex;align-items:stretch;justify-content:center;padding:16px}
.cc-ov>.cc{background:var(--cc-bg);width:100%;max-width:820px;border-radius:14px;overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,.35);display:flex;flex-direction:column;-webkit-overflow-scrolling:touch}
.cc-hd{display:flex;align-items:flex-start;gap:12px;padding:16px 18px 12px;border-bottom:1px solid var(--cc-line);position:sticky;top:0;background:var(--cc-bg);z-index:2}
.cc-hd h2{margin:0;font-size:19px;line-height:1.25}.cc-hd p{margin:2px 0 0;color:var(--cc-mute);font-size:13px}
.cc-x{margin-left:auto;border:1px solid var(--cc-line);background:var(--cc-card);border-radius:10px;width:36px;height:36px;flex:none;font-size:16px}
.cc-pad{padding:16px 18px 22px;display:flex;flex-direction:column;gap:14px}
.cc-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.cc-stat{background:var(--cc-card);border:1px solid var(--cc-line);border-radius:12px;padding:10px 12px}
.cc-stat b{display:block;font-size:22px;line-height:1.1;font-variant-numeric:tabular-nums}.cc-stat span{font-size:12px;color:var(--cc-mute)}
.cc-h3{margin:4px 0 0;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--cc-mute);font-weight:700}
.cc-temas{display:flex;flex-wrap:wrap;gap:6px}
.cc-chip{border:1px solid var(--cc-line);background:var(--cc-card);border-radius:999px;padding:6px 12px;font-size:13px;line-height:1.3;text-align:left}
.cc-chip i{font-style:normal;color:var(--cc-mute);margin-left:4px;font-variant-numeric:tabular-nums}
.cc-chip[aria-pressed=true]{background:var(--cc-g);border-color:var(--cc-g);color:#fff}.cc-chip[aria-pressed=true] i{color:#e9f3ee}
.cc[data-dark] .cc-chip[aria-pressed=true],.cc[data-dark] .cc-btn.p,.cc[data-dark] .cc-btn.g{color:#0f1712}.cc[data-dark] .cc-chip[aria-pressed=true] i{color:#1d3a2c}
.cc-acts{display:flex;flex-wrap:wrap;gap:8px}
.cc-btn{border:1px solid var(--cc-line);background:var(--cc-card);border-radius:12px;padding:11px 16px;font-weight:600;display:inline-flex;align-items:center;gap:8px;min-height:44px}
.cc-btn.p{background:var(--cc-o);border-color:var(--cc-o);color:#fff}.cc-btn.g{background:var(--cc-g);border-color:var(--cc-g);color:#fff}
.cc-btn[disabled]{opacity:.45;cursor:default}
.cc-btn small{font-weight:500;opacity:.85}
.cc-note{font-size:13px;color:var(--cc-mute);margin:0}
.cc-prog{height:6px;border-radius:99px;background:var(--cc-line);overflow:hidden}.cc-prog i{display:block;height:100%;background:var(--cc-o);transition:width .25s}
.cc-meta{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;font-size:13px;color:var(--cc-mute)}
.cc-tag{font-size:12px;color:var(--cc-o);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.cc-time{margin-left:auto;font-variant-numeric:tabular-nums;font-weight:600}
.cc-case{background:var(--cc-card);border:1px solid var(--cc-line);border-left:4px solid var(--cc-g);border-radius:12px;padding:16px 18px}
.cc-case h3{margin:0 0 6px;font-size:16px}.cc-case p{margin:0}
.cc-q{font-weight:700;font-size:16px;margin:0}
.cc-ops{display:flex;flex-direction:column;gap:8px;margin:0;padding:0;list-style:none}
.cc-op{width:100%;display:flex;gap:10px;align-items:flex-start;text-align:left;border:1px solid var(--cc-line);background:var(--cc-card);border-radius:12px;padding:11px 14px;min-height:44px}
.cc-op>b{flex:none;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;background:var(--cc-soft);color:var(--cc-g);font-size:13px}
.cc-op>span{flex:1}
.cc-op:not([disabled]):hover{border-color:var(--cc-g)}
.cc-op.sel{border-color:var(--cc-o);box-shadow:0 0 0 1px var(--cc-o)}
.cc-op.ok{border-color:var(--cc-ok);background:var(--cc-okb)}.cc-op.ok>b{background:var(--cc-ok);color:#fff}
.cc-op.bad{border-color:var(--cc-bad);background:var(--cc-badb)}.cc-op.bad>b{background:var(--cc-bad);color:#fff}
.cc-op[disabled]{cursor:default}
.cc-why{display:block;font-size:13.5px;color:var(--cc-mute);margin-top:4px}
.cc-op.ok .cc-why,.cc-op.bad .cc-why{color:var(--cc-ink)}
.cc-fb{border-radius:12px;padding:12px 14px;font-size:14.5px}
.cc-fb.ok{background:var(--cc-okb);border:1px solid var(--cc-ok)}.cc-fb.bad{background:var(--cc-badb);border:1px solid var(--cc-bad)}
.cc-fb strong{display:block;margin-bottom:2px}
.cc-perla{background:var(--cc-soft);border-radius:12px;padding:12px 14px;font-size:14.5px}
.cc-perla b:first-child{color:var(--cc-g)}
.cc-nav{display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap}
.cc-big{font-size:44px;font-weight:800;line-height:1;font-variant-numeric:tabular-nums}
.cc-res{display:flex;gap:16px;align-items:center;background:var(--cc-card);border:1px solid var(--cc-line);border-radius:14px;padding:16px 18px}
.cc-res p{margin:0}
.cc-rev{border:1px solid var(--cc-line);border-radius:12px;background:var(--cc-card)}
.cc-rev>summary{cursor:pointer;padding:12px 14px;display:flex;gap:10px;align-items:flex-start;list-style:none}
.cc-rev>summary::-webkit-details-marker{display:none}
.cc-rev>summary>b{flex:none;width:24px;height:24px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:13px}
.cc-rev>div{padding:0 14px 14px;display:flex;flex-direction:column;gap:10px}
.cc-dag{font-size:12px;color:var(--cc-mute);margin:0}
@media (max-width:520px){.cc-ov{padding:0}.cc-ov>.cc{border-radius:0}.cc-fab span{display:none}.cc-stats{gap:6px}.cc-stat b{font-size:19px}}
@media (prefers-reduced-motion:reduce){.cc-prog i,.cc-fab{transition:none}}`;
  const ICON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6v4H9z"/><path d="M8 5H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><path d="m9 14 2 2 4-4"/></svg>';
  let DATA=null,ov=null,last=null;
  const load=()=>DATA?Promise.resolve(DATA):fetch(BASE+"casos/"+G+".json").then(r=>{if(!r.ok)throw new Error("http "+r.status);return r.json()}).then(d=>DATA=d);
  const P=()=>{try{const a=JSON.parse(localStorage.getItem(KEY)||"{}");return a&&typeof a==="object"?a:{}}catch(e){return {}}};
  const mine=()=>P()[G]||{};
  function save(id,ok){
    const a=P(),g=a[G]||(a[G]={}),x=g[id]||[0,0,0,0];
    g[id]=[x[0]+(ok?1:0),x[1]+1,ok?1:0,Date.now()];
    try{localStorage.setItem(KEY,JSON.stringify(a))}catch(e){}
  }
  const shuffle=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
  const L="ABCDEFG";

  /* ===== botón flotante ===== */
  function fab(){
    if(!document.body||document.querySelector(".cc-fab"))return;
    const st=document.createElement("style");st.textContent=CSS;document.head.appendChild(st);
    const b=document.createElement("button");b.type="button";b.className="cc-fab";
    b.setAttribute("aria-label","Casos clínicos tipo examen: ponme a prueba");
    b.innerHTML=ICON+"<span>Casos clínicos</span>"+(me.dataset.n?"<small>"+esc(me.dataset.n)+"</small>":"");
    b.onclick=open;document.body.appendChild(b);
    // si la guía tiene el botón de Anki, este va encima
    const place=()=>{const ak=document.querySelector(".ak-fab");const r=ak&&ak.getBoundingClientRect();b.style.bottom=r&&r.width?(innerHeight-r.top+10)+"px":"16px"};
    place();[300,1200,3000].forEach(t=>setTimeout(place,t));addEventListener("resize",place);
  }

  /* ===== ventana ===== */
  function open(){
    if(ov)return;last=document.activeElement;
    ov=document.createElement("div");ov.className="cc-ov";ov.setAttribute("role","dialog");ov.setAttribute("aria-modal","true");ov.setAttribute("aria-label","Casos clínicos");
    ov.innerHTML='<div class="cc"'+(dark()?" data-dark":"")+'><div class="cc-pad"><p class="cc-note">Cargando casos…</p></div></div>';
    ov.addEventListener("click",e=>{if(e.target===ov)close()});
    document.body.appendChild(ov);document.documentElement.style.overflow="hidden";
    load().then(home).catch(()=>{box().innerHTML=head("Casos clínicos","")+'<div class="cc-pad"><p class="cc-note">No se pudieron cargar los casos. Revisa tu conexión y vuelve a intentarlo.</p></div>';wire()});
  }
  function close(){if(!ov)return;clearInterval(timer);ov.remove();ov=null;document.documentElement.style.overflow="";if(last&&last.focus)last.focus()}
  document.addEventListener("keydown",e=>{if(!ov)return;if(e.key==="Escape"){e.preventDefault();close()}
    else if(cur&&/^[1-7a-gA-G]$/.test(e.key)&&!e.metaKey&&!e.ctrlKey){const i=isNaN(+e.key)?L.indexOf(e.key.toUpperCase()):+e.key-1;const o=box().querySelectorAll(".cc-op")[i];if(o&&!o.disabled)o.click()}
    else if(e.key==="Enter"&&cur){const n=box().querySelector("[data-next]");if(n&&document.activeElement===document.body){e.preventDefault();n.click()}}});
  const box=()=>ov.querySelector(".cc");
  const head=(t,sub)=>'<div class="cc-hd"><div><h2>'+esc(t)+'</h2>'+(sub?'<p>'+sub+'</p>':'')+'</div><button class="cc-x" type="button" aria-label="Cerrar" data-x>✕</button></div>';
  function wire(){const x=box().querySelector("[data-x]");if(x)x.onclick=close;box().scrollTop=0}

  /* ===== inicio ===== */
  let sel=new Set(),cur=null,timer=null;
  function temas(){const m=new Map();DATA.c.forEach(c=>m.set(c.t,(m.get(c.t)||0)+1));return [...m]}
  function pool(){return DATA.c.filter(c=>!sel.size||sel.has(c.t))}
  function home(){
    cur=null;clearInterval(timer);
    const p=mine(),all=DATA.c,done=all.filter(c=>p[c.id]),ac=done.reduce((s,c)=>s+p[c.id][0],0),it=done.reduce((s,c)=>s+p[c.id][1],0);
    const fall=all.filter(c=>p[c.id]&&!p[c.id][2]),nuevos=all.filter(c=>!p[c.id]);
    const n=pool().length;
    box().innerHTML=head("Casos clínicos tipo examen",esc(DATA.n)+" · "+all.length+" casos basados en tu guía")+
      '<div class="cc-pad">'+
      '<div class="cc-stats"><div class="cc-stat"><b>'+done.length+'<small style="font-size:13px;color:var(--cc-mute)">/'+all.length+'</small></b><span>casos resueltos</span></div>'+
      '<div class="cc-stat"><b>'+(it?Math.round(100*ac/it)+" %":"—")+'</b><span>de aciertos</span></div>'+
      '<div class="cc-stat"><b>'+fall.length+'</b><span>por repasar</span></div></div>'+
      '<p class="cc-h3">Temas</p><div class="cc-temas" role="group" aria-label="Elegir temas"><button type="button" class="cc-chip" data-all aria-pressed="'+(!sel.size)+'">Todos<i>'+all.length+'</i></button>'+
      temas().map(([t,k])=>'<button type="button" class="cc-chip" data-t="'+esc(t)+'" aria-pressed="'+sel.has(t)+'">'+esc(t)+'<i>'+k+'</i></button>').join("")+'</div>'+
      '<div class="cc-acts"><button type="button" class="cc-btn p" data-ccgo="prueba"'+(n?"":" disabled")+'>Ponme a prueba <small>'+n+' caso'+(n===1?"":"s")+'</small></button>'+
      '<button type="button" class="cc-btn g" data-ccgo="simulacro"'+(n?"":" disabled")+'>Simulacro <small>'+Math.min(10,n)+' casos con reloj</small></button>'+
      '<button type="button" class="cc-btn" data-ccgo="fallados"'+(fall.length?"":" disabled")+'>Repasar los que fallé <small>'+fall.length+'</small></button>'+
      (nuevos.length&&nuevos.length<all.length?'<button type="button" class="cc-btn" data-ccgo="nuevos">Solo nuevos <small>'+nuevos.length+'</small></button>':'')+'</div>'+
      '<p class="cc-note"><b>Ponme a prueba</b>: eliges una respuesta y ves al momento por qué cada opción es correcta o no. <b>Simulacro</b>: como en el examen, la calificación y la revisión salen al final. Las opciones se revuelven en cada intento y el tema del caso se muestra hasta que respondes, para que no te dé pistas. Atajos: teclas 1–5 o A–E para responder.</p>'+
      '<p class="cc-dag">Casos de práctica escritos con el contenido de esta guía; † marca lo que no viene en tus apuntes.</p></div>';
    wire();
    box().querySelectorAll(".cc-chip").forEach(b=>b.onclick=()=>{if(b.hasAttribute("data-all"))sel.clear();else{const t=b.dataset.t;sel.has(t)?sel.delete(t):sel.add(t)}home()});
    box().querySelectorAll("[data-ccgo]").forEach(b=>b.onclick=()=>{
      const m=b.dataset.ccgo;
      if(m==="fallados")run(shuffle(fall),"prueba","Repaso de fallados");
      else if(m==="nuevos")run(shuffle(nuevos.filter(c=>!sel.size||sel.has(c.t))),"prueba","Casos nuevos");
      else if(m==="simulacro")run(shuffle(pool()).slice(0,10),"simulacro","Simulacro");
      else run(shuffle(pool()),"prueba","Ponme a prueba");
    });
  }

  /* ===== resolver ===== */
  function run(list,mode,title){
    if(!list.length)return home();
    cur={list:list.map(c=>({c,ord:shuffle(c.o.map((_,i)=>i)),pick:-1})),i:0,mode,title,t0:Date.now()};
    clearInterval(timer);
    if(mode==="simulacro")timer=setInterval(()=>{const el=ov&&box().querySelector(".cc-time");if(el)el.textContent=clock()},1000);
    show();
  }
  const clock=()=>{const s=Math.floor((Date.now()-cur.t0)/1000);return Math.floor(s/60)+":"+String(s%60).padStart(2,"0")};
  function show(){
    const k=cur.list[cur.i],c=k.c,n=cur.list.length,answered=k.pick>=0,prueba=cur.mode==="prueba";
    box().innerHTML=head(cur.title,"Caso "+(cur.i+1)+" de "+n)+
      '<div class="cc-pad"><div class="cc-prog" aria-hidden="true"><i style="width:'+Math.round(100*(cur.i+(answered?1:0))/n)+'%"></i></div>'+
      '<div class="cc-meta"><span class="cc-tag">'+(answered&&prueba?esc(c.t):"Caso clínico")+'</span>'+(cur.mode==="simulacro"?'<span class="cc-time" aria-label="Tiempo">'+clock()+'</span>':'')+'</div>'+
      '<div class="cc-case">'+(answered&&prueba&&c.h?'<h3>'+fmt(c.h)+'</h3>':'')+'<p>'+fmt(c.v)+'</p></div>'+
      '<p class="cc-q">'+fmt(c.q)+'</p>'+
      '<ol class="cc-ops">'+k.ord.map((oi,j)=>{
        let cls="";if(answered&&prueba){if(oi===0)cls=" ok";else if(oi===k.pick)cls=" bad"}else if(answered&&oi===k.pick)cls=" sel";
        return '<li><button type="button" class="cc-op'+cls+'" data-o="'+oi+'"'+(answered&&prueba?" disabled":"")+'><b>'+L[j]+'</b><span>'+fmt(c.o[oi][0])+
          (answered&&prueba&&c.o[oi][1]?'<span class="cc-why">'+(oi===0?"✓ ":"✗ ")+fmt(c.o[oi][1])+'</span>':'')+'</span></button></li>'}).join("")+'</ol>'+
      (answered&&prueba?'<div class="cc-fb '+(k.pick===0?"ok":"bad")+'" role="status"><strong>'+(k.pick===0?"¡Correcto!":"Incorrecto")+'</strong>La respuesta es <b>'+fmt(c.o[0][0])+'</b>.</div>'+
        (c.e?'<div class="cc-perla"><b>Perla:</b> '+fmt(c.e)+'</div>':''):'')+
      '<div class="cc-nav"><button type="button" class="cc-btn" data-home>Salir</button>'+
      (cur.mode==="simulacro"&&cur.i>0?'<button type="button" class="cc-btn" data-prev>Anterior</button>':'')+
      (answered||cur.mode==="simulacro"?'<button type="button" class="cc-btn p" data-next'+(answered?"":" disabled")+'>'+(cur.i+1<n?"Siguiente":"Ver resultado")+'</button>':'')+'</div></div>';
    wire();
    box().querySelector("[data-home]").onclick=()=>{if(cur.list.some(x=>x.pick>=0)&&cur.mode==="simulacro"&&!confirmExit())return;home()};
    const pv=box().querySelector("[data-prev]");if(pv)pv.onclick=()=>{cur.i--;show()};
    const nx=box().querySelector("[data-next]");if(nx)nx.onclick=()=>{if(cur.i+1<n){cur.i++;show()}else result()};
    box().querySelectorAll(".cc-op:not([disabled])").forEach(b=>b.onclick=()=>{
      const oi=+b.dataset.o;
      if(prueba){k.pick=oi;save(c.id,oi===0);show();const fb=box().querySelector(".cc-fb");if(fb)fb.scrollIntoView({behavior:reduce()?"auto":"smooth",block:"nearest"})}
      else{k.pick=oi;show()}
    });
  }
  function confirmExit(){
    // sin diálogos del navegador: segundo toque para confirmar
    const b=box().querySelector("[data-home]");if(b.dataset.sure)return true;
    b.dataset.sure=1;b.textContent="¿Salir sin calificar? Toca otra vez";setTimeout(()=>{if(b.isConnected){delete b.dataset.sure;b.textContent="Salir"}},4000);return false;
  }
  function result(){
    clearInterval(timer);
    if(cur.mode==="simulacro")cur.list.forEach(k=>save(k.c.id,k.pick===0));
    const n=cur.list.length,ok=cur.list.filter(k=>k.pick===0).length,pct=Math.round(100*ok/n),cal=Math.round(100*ok/n)/10;
    const bad=cur.list.filter(k=>k.pick!==0).map(k=>k.c);
    const porTema=new Map();cur.list.forEach(k=>{const x=porTema.get(k.c.t)||[0,0];x[1]++;if(k.pick===0)x[0]++;porTema.set(k.c.t,x)});
    box().innerHTML=head("Resultado",esc(cur.title)+(cur.mode==="simulacro"?" · "+clock():""))+
      '<div class="cc-pad"><div class="cc-res"><div class="cc-big" style="color:'+(cal>=7.5?"var(--cc-ok)":"var(--cc-bad)")+'">'+cal.toFixed(1)+'</div>'+
      '<div><p><b>'+ok+' de '+n+'</b> correctos ('+pct+' %).</p><p class="cc-note">'+(cal>=7.5?"Aprobado con la mínima UDLAP (7.5).":"Por debajo de 7.5, la mínima aprobatoria UDLAP: repasa los temas que fallaste.")+'</p></div></div>'+
      (porTema.size>1?'<p class="cc-h3">Por tema</p><div class="cc-temas">'+[...porTema].map(([t,x])=>'<span class="cc-chip">'+esc(t)+'<i>'+x[0]+'/'+x[1]+'</i></span>').join("")+'</div>':'')+
      '<div class="cc-acts">'+(bad.length?'<button type="button" class="cc-btn p" data-again>Repetir los que fallé <small>'+bad.length+'</small></button>':'')+
      '<button type="button" class="cc-btn" data-home>Volver a los temas</button></div>'+
      (cur.mode==="simulacro"?'<p class="cc-h3">Revisión</p>'+cur.list.map((k,i)=>{const c=k.c,good=k.pick===0;
        return '<details class="cc-rev"'+(good?"":" open")+'><summary><b style="background:'+(good?"var(--cc-ok)":"var(--cc-bad)")+'">'+(good?"✓":"✗")+'</b><span><span class="cc-tag">'+esc(c.t)+'</span><br>'+fmt(c.h||c.q)+'</span></summary><div>'+
          '<p>'+fmt(c.v)+'</p><p class="cc-q">'+fmt(c.q)+'</p>'+
          '<ol class="cc-ops">'+k.ord.map((oi,j)=>'<li><div class="cc-op'+(oi===0?" ok":oi===k.pick?" bad":"")+'"><b>'+L[j]+'</b><span>'+fmt(c.o[oi][0])+(c.o[oi][1]?'<span class="cc-why">'+(oi===0?"✓ ":"✗ ")+fmt(c.o[oi][1])+'</span>':'')+'</span></div></li>').join("")+'</ol>'+
          (k.pick<0?'<p class="cc-note">Sin responder.</p>':'')+(c.e?'<div class="cc-perla"><b>Perla:</b> '+fmt(c.e)+'</div>':'')+'</div></details>'}).join(""):'')+
      '</div>';
    wire();cur=null;
    box().querySelector("[data-home]").onclick=home;
    const ag=box().querySelector("[data-again]");if(ag)ag.onclick=()=>run(shuffle(bad),"prueba","Repaso de fallados");
  }

  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",fab);else fab();
  window.Casos={open};
})();
