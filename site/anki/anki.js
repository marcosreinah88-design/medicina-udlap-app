/* Tarjetas de Anki de Marcos (revisadas y corregidas). Uso:
   <script src=".../anki/anki.js" data-m="hematologia" data-n="2284" defer></script>
   - Dentro de una guía: agrega un botón flotante "Tus tarjetas de Anki" que abre el repaso.
   - En una página con <div id="ak-root"></div>: muestra el repaso dentro de la página.
   - Mazos cifrados (AnKing): data-src="anking/x.txt" data-enc="1" (la clave vive en carrera-anking-clave).
   Datos: anki/<materia>.json  {id,n,s,c:[[tema,frente,reverso]],q:[[tema,pregunta,[opciones],correcta,explicación]]}
   El repaso, el programador (como Anki) y las Estadísticas viven en anki/srs.js, que también usa la sección Estudio:
   así el avance de una tarjeta es el mismo en la guía, en su página de materia y en Estudio.
   Avance en localStorage carrera-anki-<materia> (ver srs.js). */
(function(){
  const me=document.currentScript;if(!me)return;
  const M=me.dataset.m,N=+me.dataset.n||0,BASE=me.src.replace(/[^\/]*$/,"");
  const SRC=me.dataset.src||M+".json",ENC=!!me.dataset.enc,CK="carrera-anking-clave";
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const fmt=s=>esc(s).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").split(" · ").join("<br>");
  const norm=s=>String(s).normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase();
  const dark=()=>{const t=document.documentElement.dataset.theme||document.body&&document.body.dataset.theme;
    if(t)return t==="dark";try{return matchMedia("(prefers-color-scheme: dark)").matches}catch(e){return false}};
  const CSS=`.ak{--ak-bg:#fbfaf6;--ak-card:#fff;--ak-ink:#1d2a24;--ak-mute:#5d6b64;--ak-line:#dfe3dc;--ak-g:#00573c;--ak-o:#f26b21;--ak-soft:#e8f1ec;
font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ak-ink);text-align:left}
.ak[data-dark]{--ak-bg:#121815;--ak-card:#1b2420;--ak-ink:#e7ece8;--ak-mute:#a3b0a9;--ak-line:#2e3a34;--ak-g:#4fbf8f;--ak-o:#ff9558;--ak-soft:#1f3329}
.ak *{box-sizing:border-box}.ak button{font:inherit;cursor:pointer}
.ak-fab{position:fixed;right:16px;bottom:16px;z-index:2147483000;display:flex;align-items:center;gap:8px;padding:10px 16px;border-radius:999px;border:0;background:#00573c;color:#fff;
font:600 14px/1.2 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.22)}
.ak-fab small{background:#f26b21;border-radius:999px;padding:2px 8px;font-weight:700}
.ak-ov{position:fixed;inset:0;z-index:2147483001;background:rgba(10,20,15,.55);display:flex;align-items:stretch;justify-content:center;padding:16px}
.ak-ov .ak{background:var(--ak-bg);width:100%;max-width:820px;border-radius:14px;overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,.35);display:flex;flex-direction:column}
.ak-in{padding:16px 18px 0}
.ak-hd{display:flex;align-items:flex-start;gap:12px;margin-bottom:10px}.ak-hd h2{margin:0;font-size:19px;line-height:1.25}.ak-hd p{margin:2px 0 0;color:var(--ak-mute);font-size:13px}
.ak-x{margin-left:auto;border:1px solid var(--ak-line);background:var(--ak-card);color:var(--ak-ink);border-radius:10px;width:36px;height:36px;flex:none}
.ak-bar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px}
.ak-bar select,.ak-bar input{font:inherit;padding:7px 10px;border:1px solid var(--ak-line);border-radius:10px;background:var(--ak-card);color:var(--ak-ink);min-width:0;flex:1 1 180px}
.ak-tabs{display:flex;gap:4px;border-bottom:1px solid var(--ak-line);overflow-x:auto}
.ak-tabs button{border:0;background:none;color:var(--ak-mute);padding:8px 12px;border-bottom:3px solid transparent;font-weight:600;white-space:nowrap}
.ak-tabs button[aria-selected=true]{color:var(--ak-g);border-color:var(--ak-o)}
.ak-body{flex:1;display:flex;flex-direction:column;min-height:0}.ak-body>.srs{flex:1;border-radius:0 0 14px 14px}
.ak-pad{padding:14px 18px 20px}
.ak-card{background:var(--ak-card);border:1px solid var(--ak-line);border-radius:14px;padding:22px;display:flex;flex-direction:column;gap:12px}
.ak-tema{font-size:12px;color:var(--ak-o);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.ak-f{font-size:19px;font-weight:600;line-height:1.35}.ak-b{border-top:1px dashed var(--ak-line);padding-top:12px;font-size:16px}
.ak-act{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.ak-btn{flex:1 1 120px;padding:11px 14px;border-radius:12px;border:1px solid var(--ak-line);background:var(--ak-card);color:var(--ak-ink);font-weight:600}
.ak-btn.p{background:var(--ak-g);border-color:var(--ak-g);color:#fff}
.ak-meta{display:flex;justify-content:space-between;color:var(--ak-mute);font-size:13px;margin-bottom:8px;gap:8px;flex-wrap:wrap}
.ak-list{display:flex;flex-direction:column;gap:8px}.ak-li{background:var(--ak-card);border:1px solid var(--ak-line);border-radius:12px;padding:12px 14px}
.ak-li b.f{display:block;margin-bottom:4px}.ak-li .bk{color:var(--ak-mute)}.ak-li.ok{border-left:4px solid var(--ak-g)}
.ak-st{font-size:12px;color:var(--ak-mute);margin:2px 0 4px}.ak-st b{color:var(--ak-o)}
.ak-more{margin:10px auto 0;display:block}
.ak-opt{display:block;width:100%;text-align:left;padding:11px 14px;border-radius:12px;border:1px solid var(--ak-line);background:var(--ak-card);color:var(--ak-ink);margin-top:8px}
.ak-opt.ok{border-color:#1e8a57;background:rgba(30,138,87,.12)}.ak-opt.no{border-color:#c0392b;background:rgba(192,57,43,.1)}
.ak-empty{color:var(--ak-mute);text-align:center;padding:30px 10px}
.ak-lnk{border:0;background:none;color:var(--ak-mute);text-decoration:underline;padding:4px;font-size:13px}
@media (max-width:520px){.ak-ov{padding:0}.ak-ov .ak{border-radius:0}.ak-in{padding:14px 14px 0}.ak-pad{padding:12px 14px 18px}}`;
  function css(){if(document.getElementById("ak-css"))return;const s=document.createElement("style");s.id="ak-css";s.textContent=CSS;document.head.appendChild(s)}
  /* srs.js (programador, repaso y estadísticas) se carga una sola vez */
  const srs=()=>window.SRS?Promise.resolve(window.SRS):new Promise((ok,no)=>{const s=document.createElement("script");s.src=BASE+"srs.js";s.onload=()=>window.SRS?ok(window.SRS):no(new Error("srs"));s.onerror=()=>no(new Error("srs"));document.head.appendChild(s)});
  async function decrypt(buf){
    let pass="";try{pass=localStorage.getItem(CK)||""}catch(e){}
    if(!pass)throw new Error("nokey");
    const te=new TextEncoder(),ikm=await crypto.subtle.importKey("raw",te.encode(pass.trim()),"HKDF",false,["deriveKey"]);
    const key=await crypto.subtle.deriveKey({name:"HKDF",hash:"SHA-256",salt:te.encode("medicina-udlap/anking/v1"),info:te.encode("mazo")},ikm,{name:"AES-GCM",length:256},false,["decrypt"]);
    const u=new Uint8Array(buf);let pt;
    try{pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:u.slice(0,12)},key,u.slice(12))}catch(e){throw new Error("badkey")}
    const txt=await new Response(new Blob([pt]).stream().pipeThrough(new DecompressionStream("gzip"))).text();
    return JSON.parse(txt);
  }
  let DATA=null;
  const load=()=>DATA?Promise.resolve(DATA):srs().then(S=>fetch(BASE+SRC).then(r=>{if(!r.ok)throw new Error("http");return ENC?r.text().then(t=>decrypt(Uint8Array.from(atob(t.trim()),c=>c.charCodeAt(0)))):r.json()})
    .then(d=>{d.c.forEach(c=>c.push(S.hash(c[1]+"|"+c[2])));d.q=d.q||[];DATA=d;return d}));
  function keyForm(host,err){
    host.innerHTML=`<div class="ak"${dark()?" data-dark":""}><div class="ak-pad"><div class="ak-card"><div class="ak-tema">Mazo AnKing</div>
      <div class="ak-f">${err==="badkey"?"Esa clave no abre el mazo. Revísala.":"Escribe la clave del mazo AnKing"}</div>
      <p style="margin:0;color:var(--ak-mute)">Solo se pide una vez: se guarda en este aparato y se pasa a los demás con la sincronización.</p>
      <input type="password" autocomplete="off" placeholder="Clave" style="font:inherit;padding:10px 12px;border:1px solid var(--ak-line);border-radius:10px;background:var(--ak-card);color:var(--ak-ink)">
      <div class="ak-act" style="margin:0"><button class="ak-btn p" type="button">Abrir mazo</button></div></div></div></div>`;
    const i=host.querySelector("input"),go=()=>{const v=i.value.trim();if(!v)return;try{localStorage.setItem(CK,v)}catch(e){}host.innerHTML="";start()};
    host.querySelector("button").onclick=go;i.onkeydown=e=>{if(e.key==="Enter")go()};i.focus();
  }
  function app(host,inPage,close){
    const S=window.SRS,st=S.deckStore(M),name=DATA.n;
    {const P=st.meta();if(P.N!==DATA.c.length||P.name!==name)st.set({N:DATA.c.length,name})}
    const ui={tab:"repasar",tema:"",q:"",lim:60,qi:0,qa:-1,qord:[],ok:0,tot:0};
    const root=document.createElement("div");root.className="ak";if(dark())root.dataset.dark="";host.appendChild(root);
    const cards=()=>DATA.c.filter(c=>(!ui.tema||c[0]===ui.tema)&&(!ui.q||norm(c[1]+" "+c[2]).includes(norm(ui.q))));
    const srsCards=()=>DATA.c.filter(c=>!ui.tema||c[0]===ui.tema).map(c=>({k:c[3],st,f:c[1],b:c[2],t:c[0],deck:M,dn:name}));
    const qs=()=>DATA.q.filter(q=>!ui.tema||q[0]===ui.tema);
    function temas(){const m=new Map();DATA.c.forEach(c=>m.set(c[0],(m.get(c[0])||0)+1));DATA.q.forEach(q=>m.set(q[0],(m.get(q[0])||0)));return [...m]}
    function state(h){const p=st.get(h);if(S.isNew(p))return p&&p.sp?"nueva · suspendida":"nueva";if(p.sp)return "suspendida";if(p.q!==1)return p.q===2?"reaprendiendo":"aprendiendo";
      const d=Math.round((p.d-S.dayStart(Date.now()))/864e5);return (d<=0?"toca hoy":"vuelve en "+S.ivTxt({i:d}))+` · facilidad ${p.e} %`+(p.l?` · olvidada ${p.l} ${p.l===1?"vez":"veces"}`:"")}
    function dealQ(){ui.qord=qs().map((_,i)=>i).sort(()=>Math.random()-.5);ui.qi=0;ui.qa=-1;ui.ok=0;ui.tot=0}
    let view=null;
    function body(){
      const B=root.querySelector(".ak-body");if(view){view.destroy();view=null}B.innerHTML="";
      if(ui.tab==="repasar"){
        const P=()=>st.meta();
        view=S.reviewer(B,{title:()=>name+(ui.tema?" · "+ui.tema:""),cards:srsCards,ids:[M],newLim:()=>P().lim!=null?P().lim:20,revLim:()=>P().rlim||200,
          setLim:o=>st.set(o),onStats:()=>{ui.tab="stats";draw()},shuffleNew:true});
        return;
      }
      if(ui.tab==="stats"){
        view=S.stats(B,{decks:()=>{const own={id:M,name,total:DATA.c.length,states:()=>DATA.c.map(c=>st.get(c[3]))};return [own].concat(S.knownDecks().filter(d=>d.id!==M))},
          scopes:()=>[[M,"Este mazo: "+name],["","Todas tus materias"]],scope:M});
        return;
      }
      const w=document.createElement("div");w.className="ak-pad";B.appendChild(w);
      if(ui.tab==="lista"){
        const all=cards();if(!all.length){w.innerHTML=`<div class="ak-empty">No hay tarjetas con ese filtro.</div>`;return}
        w.innerHTML=`<div class="ak-meta"><span>${all.length.toLocaleString("es-MX")} tarjetas</span></div><div class="ak-list">`+all.slice(0,ui.lim).map(c=>{const p=st.get(c[3]);return `<div class="ak-li${p&&!p.nw&&p.q===1?" ok":""}"><b class="f">${fmt(c[1])}</b><div class="ak-st">${state(c[3])}</div><div class="bk">${fmt(c[2])}</div></div>`}).join("")+`</div>`
          +(all.length>ui.lim?`<button class="ak-btn ak-more" data-a="mas">Ver más (${all.length-ui.lim})</button>`:"");
        return;
      }
      const L=qs();if(!L.length){w.innerHTML=`<div class="ak-empty">No hay preguntas de opción múltiple en este tema.</div>`;return}
      if(ui.qi>=ui.qord.length){w.innerHTML=`<div class="ak-card"><div class="ak-f">Terminaste: ${ui.ok} de ${ui.tot} correctas (${ui.tot?Math.round(100*ui.ok/ui.tot):0} %)</div></div><div class="ak-act"><button class="ak-btn p" data-a="qrst">Otra ronda</button></div>`;return}
      const q=L[ui.qord[ui.qi]];
      w.innerHTML=`<div class="ak-meta"><span>Pregunta ${ui.qi+1} de ${ui.qord.length}</span><span>${ui.ok} de ${ui.tot} correctas</span></div><div class="ak-card"><div class="ak-tema">${esc(q[0])}</div><div class="ak-f">${fmt(q[1])}</div><div>`
        +q[2].map((o,i)=>`<button class="ak-opt${ui.qa<0?"":i===q[3]?" ok":i===ui.qa?" no":""}" data-o="${i}" ${ui.qa<0?"":"disabled"}>${"ABCDE"[i]}) ${fmt(o)}</button>`).join("")+`</div>${ui.qa>=0&&q[4]?`<div class="ak-b">${fmt(q[4])}</div>`:""}</div>`
        +(ui.qa>=0?`<div class="ak-act"><button class="ak-btn p" data-a="qnext">Siguiente</button></div>`:"");
    }
    function draw(){
      const T=temas(),hasQ=DATA.q.length>0;
      root.innerHTML=`<div class="ak-in"><div class="ak-hd"><div><h2>${esc(name)}${ENC?"":" · tus tarjetas de Anki"}</h2><p>${DATA.c.length.toLocaleString("es-MX")} tarjetas${hasQ?" y "+DATA.q.length+" preguntas":""}, ${ENC?"traducidas al español y revisadas":"revisadas y corregidas"}.</p></div>${close?`<button class="ak-x" data-a="cerrar" aria-label="Cerrar">✕</button>`:""}</div>
        ${ui.tab!=="stats"?`<div class="ak-bar"><select data-k="tema" aria-label="Tema"><option value="">Todos los temas</option>${T.map(([t,n])=>`<option value="${esc(t)}"${t===ui.tema?" selected":""}>${esc(t)} (${n})</option>`).join("")}</select>
        ${ui.tab==="lista"?`<input data-k="q" type="search" placeholder="Buscar en las tarjetas" value="${esc(ui.q)}">`:""}</div>`:""}
        <div class="ak-tabs" role="tablist">${[["repasar","Repasar"],["lista","Ver todas"]].concat(hasQ?[["quiz","Preguntas"]]:[]).concat([["stats","Estadísticas"]]).map(([k,l])=>`<button role="tab" data-t="${k}" aria-selected="${ui.tab===k}">${l}</button>`).join("")}</div></div>
        <div class="ak-body"></div>`;
      body();
    }
    root.addEventListener("click",e=>{
      const t=e.target.closest("[data-t],[data-a],[data-o]");if(!t||!root.contains(t)||t.closest(".srs"))return;
      if(t.dataset.t){ui.tab=t.dataset.t;if(ui.tab==="quiz"&&!ui.qord.length)dealQ();draw();return}
      if(t.dataset.o!==undefined){if(ui.qa>=0)return;const q=qs()[ui.qord[ui.qi]];ui.qa=+t.dataset.o;ui.tot++;if(ui.qa===q[3])ui.ok++;body();return}
      const a=t.dataset.a;
      if(a==="cerrar")return close();
      if(a==="mas")ui.lim+=100;else if(a==="qnext"){ui.qi++;ui.qa=-1}else if(a==="qrst")dealQ();
      body();
    });
    root.addEventListener("change",e=>{if(!root.contains(e.target)||e.target.closest(".srs"))return;const k=e.target.dataset.k;if(k==="tema"){ui.tema=e.target.value;ui.lim=60;dealQ();body()}});
    root.addEventListener("input",e=>{if(e.target.dataset.k==="q"){ui.q=e.target.value;ui.lim=60;body()}});
    const esc_=e=>{if(e.key==="Escape"&&close&&!document.querySelector(".srs-menu"))close()};
    document.addEventListener("keydown",esc_);
    /* si llegan cambios de otro aparato o de otra pestaña, se vuelve a leer el avance */
    const onStore=e=>{if(e.key&&(e.key===st.KEY||e.key.startsWith("carrera-srs-"))){st.reload();if(view&&view.refresh)view.refresh()}};
    addEventListener("storage",onStore);
    draw();
    return ()=>{if(view)view.destroy();document.removeEventListener("keydown",esc_);removeEventListener("storage",onStore)};
  }
  function start(){
    css();
    const host=document.getElementById("ak-root");
    if(host){load().then(()=>app(host,true,null)).catch(e=>{if(e.message==="nokey"||e.message==="badkey")keyForm(host,e.message);else host.textContent="No se pudieron cargar las tarjetas."});return}
    const b=document.createElement("button");b.className="ak-fab";b.type="button";
    b.innerHTML=`Tus tarjetas de Anki${N?` <small>${N.toLocaleString("es-MX")}</small>`:""}`;
    b.onclick=()=>load().then(()=>{
      const ov=document.createElement("div");ov.className="ak-ov";ov.setAttribute("role","dialog");ov.setAttribute("aria-modal","true");
      let off=null;const close=()=>{off&&off();ov.remove();b.style.display=""};
      ov.addEventListener("click",e=>{if(e.target===ov)close()});
      document.body.appendChild(ov);b.style.display="none";off=app(ov,false,close);
    }).catch(()=>{b.textContent="No se pudieron cargar las tarjetas"});
    document.body.appendChild(b);
  }
  document.readyState==="loading"?document.addEventListener("DOMContentLoaded",start):start();
})();
