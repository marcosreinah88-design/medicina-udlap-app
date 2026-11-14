/* Tarjetas de Anki de Marcos (revisadas y corregidas). Uso:
   <script src=".../anki/anki.js" data-m="hematologia" data-n="2284" defer></script>
   - Dentro de una guía: agrega un botón flotante "Tus tarjetas de Anki" que abre el repaso.
   - En una página con <div id="ak-root"></div>: muestra el repaso dentro de la página.
   Datos: anki/<materia>.json  {id,n,s,c:[[tema,frente,reverso]],q:[[tema,pregunta,[opciones],correcta,explicación]]}
   Progreso ("ya me la sé") en localStorage carrera-anki-<materia>. */
(function(){
  const me=document.currentScript;if(!me)return;
  const M=me.dataset.m,N=+me.dataset.n||0,BASE=me.src.replace(/[^\/]*$/,"");
  const KEY="carrera-anki-"+M;
  const J=(k,d)=>{try{const v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}};
  const S=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}};
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const fmt=s=>esc(s).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").split(" · ").join("<br>");
  const norm=s=>String(s).normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase();
  const hash=s=>{let h=5381;for(let i=0;i<s.length;i++)h=(h*33^s.charCodeAt(i))>>>0;return h.toString(36)};
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
.ak-ov .ak{background:var(--ak-bg);width:100%;max-width:760px;border-radius:16px;overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.ak-in{padding:20px}
.ak-hd{display:flex;align-items:flex-start;gap:12px;margin-bottom:14px}.ak-hd h2{margin:0;font-size:20px;line-height:1.25}.ak-hd p{margin:2px 0 0;color:var(--ak-mute);font-size:13px}
.ak-x{margin-left:auto;border:1px solid var(--ak-line);background:var(--ak-card);color:var(--ak-ink);border-radius:10px;width:36px;height:36px;flex:none}
.ak-bar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.ak-bar select,.ak-bar input{font:inherit;padding:8px 10px;border:1px solid var(--ak-line);border-radius:10px;background:var(--ak-card);color:var(--ak-ink);min-width:0;flex:1 1 180px}
.ak-tabs{display:flex;gap:6px;margin-bottom:14px;border-bottom:1px solid var(--ak-line)}
.ak-tabs button{border:0;background:none;color:var(--ak-mute);padding:8px 12px;border-bottom:3px solid transparent;font-weight:600}
.ak-tabs button[aria-selected=true]{color:var(--ak-g);border-color:var(--ak-o)}
.ak-prog{height:6px;background:var(--ak-line);border-radius:6px;overflow:hidden;margin:4px 0 14px}.ak-prog i{display:block;height:100%;background:var(--ak-g)}
.ak-card{background:var(--ak-card);border:1px solid var(--ak-line);border-radius:14px;padding:22px;min-height:190px;display:flex;flex-direction:column;gap:12px}
.ak-tema{font-size:12px;color:var(--ak-o);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.ak-f{font-size:19px;font-weight:600;line-height:1.35}.ak-b{border-top:1px dashed var(--ak-line);padding-top:12px;font-size:16px}
.ak-act{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.ak-btn{flex:1 1 120px;padding:11px 14px;border-radius:12px;border:1px solid var(--ak-line);background:var(--ak-card);color:var(--ak-ink);font-weight:600}
.ak-btn.p{background:var(--ak-g);border-color:var(--ak-g);color:#fff}.ak-btn.o{border-color:var(--ak-o);color:var(--ak-o)}
.ak-meta{display:flex;justify-content:space-between;color:var(--ak-mute);font-size:13px;margin-top:10px;gap:8px;flex-wrap:wrap}
.ak-list{display:flex;flex-direction:column;gap:8px}.ak-li{background:var(--ak-card);border:1px solid var(--ak-line);border-radius:12px;padding:12px 14px}
.ak-li b.f{display:block;margin-bottom:4px}.ak-li .bk{color:var(--ak-mute)}.ak-li.ok{border-left:4px solid var(--ak-g)}
.ak-more{margin:10px auto 0;display:block}
.ak-opt{display:block;width:100%;text-align:left;padding:11px 14px;border-radius:12px;border:1px solid var(--ak-line);background:var(--ak-card);color:var(--ak-ink);margin-top:8px}
.ak-opt.ok{border-color:#1e8a57;background:rgba(30,138,87,.12)}.ak-opt.no{border-color:#c0392b;background:rgba(192,57,43,.1)}
.ak-empty{color:var(--ak-mute);text-align:center;padding:30px 10px}
@media (max-width:520px){.ak-ov{padding:0}.ak-ov .ak{border-radius:0}.ak-in{padding:16px}.ak-f{font-size:17px}}`;
  function css(){if(document.getElementById("ak-css"))return;const s=document.createElement("style");s.id="ak-css";s.textContent=CSS;document.head.appendChild(s)}
  let DATA=null;
  const load=()=>DATA?Promise.resolve(DATA):fetch(BASE+M+".json").then(r=>r.json()).then(d=>{d.c.forEach(c=>c.push(hash(c[1]+"|"+c[2])));DATA=d;return d});
  function app(host,inPage,close){
    const st={tab:"repasar",tema:"",q:"",i:0,show:false,deck:[],lim:60,qi:0,qa:-1,qord:[],ok:0,tot:0};
    let known=new Set(J(KEY,[]));
    const save=()=>S(KEY,[...known]);
    const root=document.createElement("div");root.className="ak";if(dark())root.dataset.dark="";host.appendChild(root);
    const cards=()=>DATA.c.filter(c=>(!st.tema||c[0]===st.tema)&&(!st.q||norm(c[1]+" "+c[2]).includes(norm(st.q))));
    const qs=()=>DATA.q.filter(q=>!st.tema||q[0]===st.tema);
    function deal(){const p=cards().filter(c=>!known.has(c[3]));for(let i=p.length-1;i>0;i--){const j=Math.random()*(i+1)|0;[p[i],p[j]]=[p[j],p[i]]}st.deck=p;st.show=false}
    function dealQ(){st.qord=qs().map((_,i)=>i).sort(()=>Math.random()-.5);st.qi=0;st.qa=-1;st.ok=0;st.tot=0}
    function temas(){const m=new Map();DATA.c.forEach(c=>m.set(c[0],(m.get(c[0])||0)+1));DATA.q.forEach(q=>m.set(q[0],(m.get(q[0])||0)));return [...m]}
    function body(){
      if(st.tab==="repasar"){
        const all=cards(),k=all.filter(c=>known.has(c[3])).length,pct=all.length?Math.round(100*k/all.length):0;
        let h=`<div class="ak-meta" style="margin-top:0"><span>${k} de ${all.length} ya te las sabes (${pct} %)</span><span>${st.deck.length} por repasar</span></div><div class="ak-prog"><i style="width:${pct}%"></i></div>`;
        const c=st.deck[0];
        if(!c)return h+`<div class="ak-empty">${all.length?"¡Ya te sabes todas las de esta selección!":"No hay tarjetas con ese filtro."}</div>`+(k?`<div class="ak-act"><button class="ak-btn o" data-a="reset">Volver a repasar todas</button></div>`:"");
        h+=`<div class="ak-card"><div class="ak-tema">${esc(c[0])}</div><div class="ak-f">${fmt(c[1])}</div>${st.show?`<div class="ak-b">${fmt(c[2])}</div>`:""}</div>`;
        h+=st.show?`<div class="ak-act"><button class="ak-btn o" data-a="otra">Otra vez</button><button class="ak-btn p" data-a="se">Ya me la sé</button></div>`
          :`<div class="ak-act"><button class="ak-btn p" data-a="ver">Ver respuesta</button><button class="ak-btn" data-a="salta">Saltar</button></div>`;
        return h+`<div class="ak-meta"><span>Espacio: voltear · 1: otra vez · 2: me la sé</span></div>`;
      }
      if(st.tab==="lista"){
        const all=cards();if(!all.length)return `<div class="ak-empty">No hay tarjetas con ese filtro.</div>`;
        return `<div class="ak-meta" style="margin:0 0 8px"><span>${all.length} tarjetas</span></div><div class="ak-list">`+all.slice(0,st.lim).map(c=>`<div class="ak-li${known.has(c[3])?" ok":""}"><b class="f">${fmt(c[1])}</b><div class="bk">${fmt(c[2])}</div></div>`).join("")+`</div>`
          +(all.length>st.lim?`<button class="ak-btn ak-more" data-a="mas">Ver más (${all.length-st.lim})</button>`:"");
      }
      const L=qs();if(!L.length)return `<div class="ak-empty">No hay preguntas de opción múltiple en este tema.</div>`;
      if(st.qi>=st.qord.length)return `<div class="ak-card"><div class="ak-f">Terminaste: ${st.ok} de ${st.tot} correctas (${st.tot?Math.round(100*st.ok/st.tot):0} %)</div></div><div class="ak-act"><button class="ak-btn p" data-a="qrst">Otra ronda</button></div>`;
      const q=L[st.qord[st.qi]];
      return `<div class="ak-meta" style="margin:0 0 8px"><span>Pregunta ${st.qi+1} de ${st.qord.length}</span><span>${st.ok} de ${st.tot} correctas</span></div><div class="ak-card"><div class="ak-tema">${esc(q[0])}</div><div class="ak-f">${fmt(q[1])}</div><div>`
        +q[2].map((o,i)=>`<button class="ak-opt${st.qa<0?"":i===q[3]?" ok":i===st.qa?" no":""}" data-o="${i}" ${st.qa<0?"":"disabled"}>${"ABCDE"[i]}) ${fmt(o)}</button>`).join("")+`</div>${st.qa>=0&&q[4]?`<div class="ak-b">${fmt(q[4])}</div>`:""}</div>`
        +(st.qa>=0?`<div class="ak-act"><button class="ak-btn p" data-a="qnext">Siguiente</button></div>`:"");
    }
    function draw(){
      const T=temas(),hasQ=DATA.q.length>0;
      root.innerHTML=`<div class="ak-in"><div class="ak-hd"><div><h2>${esc(DATA.n)} · tus tarjetas de Anki</h2><p>${DATA.c.length} tarjetas${hasQ?" y "+DATA.q.length+" preguntas":""}, revisadas y corregidas.</p></div>${close?`<button class="ak-x" data-a="cerrar" aria-label="Cerrar">✕</button>`:""}</div>
        <div class="ak-bar"><select data-k="tema" aria-label="Tema"><option value="">Todos los temas</option>${T.map(([t,n])=>`<option value="${esc(t)}"${t===st.tema?" selected":""}>${esc(t)} (${n})</option>`).join("")}</select>
        ${st.tab==="lista"?`<input data-k="q" type="search" placeholder="Buscar en las tarjetas" value="${esc(st.q)}">`:""}</div>
        <div class="ak-tabs" role="tablist">${[["repasar","Repasar"],["lista","Ver todas"]].concat(hasQ?[["quiz","Preguntas"]]:[]).map(([k,l])=>`<button role="tab" data-t="${k}" aria-selected="${st.tab===k}">${l}</button>`).join("")}</div>
        <div class="ak-body">${body()}</div></div>`;
    }
    const redraw=()=>{root.querySelector(".ak-body").innerHTML=body()};
    root.addEventListener("click",e=>{
      const t=e.target.closest("[data-t],[data-a],[data-o]");if(!t)return;
      if(t.dataset.t){st.tab=t.dataset.t;if(st.tab==="quiz"&&!st.qord.length)dealQ();draw();return}
      if(t.dataset.o!==undefined){if(st.qa>=0)return;const q=qs()[st.qord[st.qi]];st.qa=+t.dataset.o;st.tot++;if(st.qa===q[3])st.ok++;redraw();return}
      const a=t.dataset.a;
      if(a==="cerrar")return close();
      if(a==="ver")st.show=true;
      else if(a==="salta"||a==="otra"){const c=st.deck.shift();st.deck.splice(Math.min(st.deck.length,a==="otra"?5:st.deck.length),0,c);st.show=false}
      else if(a==="se"){known.add(st.deck.shift()[3]);save();st.show=false}
      else if(a==="reset"){cards().forEach(c=>known.delete(c[3]));save();deal()}
      else if(a==="mas")st.lim+=100;
      else if(a==="qnext"){st.qi++;st.qa=-1}
      else if(a==="qrst")dealQ();
      redraw();
    });
    root.addEventListener("change",e=>{if(e.target.dataset.k==="tema"){st.tema=e.target.value;st.lim=60;deal();dealQ();draw()}});
    root.addEventListener("input",e=>{if(e.target.dataset.k==="q"){st.q=e.target.value;st.lim=60;redraw()}});
    const key=e=>{if(st.tab!=="repasar"||/INPUT|SELECT|TEXTAREA/.test((e.target||{}).tagName||""))return;
      if(e.key===" "){e.preventDefault();if(!st.show){st.show=true;redraw()}}
      else if(st.show&&(e.key==="1"||e.key==="2")){root.querySelector(`[data-a="${e.key==="1"?"otra":"se"}"]`).click()}
      else if(e.key==="Escape"&&close)close()};
    document.addEventListener("keydown",key);
    deal();draw();
    return ()=>document.removeEventListener("keydown",key);
  }
  function start(){
    css();
    const host=document.getElementById("ak-root");
    if(host){load().then(()=>app(host,true,null)).catch(()=>{host.textContent="No se pudieron cargar las tarjetas."});return}
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
