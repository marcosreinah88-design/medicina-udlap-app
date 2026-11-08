/* Medicina UDLAP · sincronización entre aparatos (Mac y cel).
   Todo lo que la página guarda en este aparato (exámenes, plan, material, avances de las guías) se copia a un
   gist privado de la cuenta de GitHub de Marcos. Cada aparato junta sus cambios con los del otro (mezcla a tres bandas). */
(()=>{
  if(window.__medSync)return;window.__medSync=1;
  const okHost=location.protocol==="app:"||/github\.io$/.test(location.hostname)||/^(localhost|127\.0\.0\.1)$/.test(location.hostname);
  if(!okHost)return;
  const API=window.__MEDSYNC_API||"https://api.github.com",P="__medsync_",DESC="Medicina UDLAP · sincronización (no borrar)",FILE="medicina-udlap.json";
  const SKIP=new Set(["carrera-theme"]);
  const get=k=>{try{return localStorage.getItem(k)}catch(e){return null}},set=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}},del=k=>{try{localStorage.removeItem(k)}catch(e){}};
  const T0=Date.now();let busy=false,again=false,lastOk=+get(P+"ok")||0,lastErr="";
  const token=()=>get(P+"token");
  function snap(){const o={};try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k&&!k.startsWith(P)&&!SKIP.has(k))o[k]=localStorage.getItem(k)}}catch(e){}return o}
  const base=()=>{try{return JSON.parse(get(P+"base")||"{}")}catch(e){return {}}};
  async function gh(path,opt={}){
    const r=await fetch(API+path,Object.assign({cache:"no-store"},opt,{headers:Object.assign({Authorization:"Bearer "+token(),Accept:"application/vnd.github+json"},opt.body?{"Content-Type":"application/json"}:{})}));
    if(r.status===401||r.status===403)throw Object.assign(new Error("clave"),{auth:true});
    if(!r.ok)throw new Error("GitHub "+r.status);
    return r.json();
  }
  async function findGist(){
    for(let page=1;page<=5;page++){
      const l=await gh("/gists?per_page=100&page="+page);
      const g=l.find(x=>x.description===DESC&&x.files&&x.files[FILE]);if(g)return g.id;
      if(l.length<100)break;
    }
    return null;
  }
  async function readRemote(id){
    const g=await gh("/gists/"+id),f=g.files&&g.files[FILE];if(!f)return {};
    let txt=f.content;if(f.truncated){const r=await fetch(f.raw_url,{cache:"no-store"});txt=await r.text()}
    try{const j=JSON.parse(txt);return j&&j.data&&typeof j.data==="object"?j.data:{}}catch(e){return {}}
  }
  const body=data=>JSON.stringify({files:{[FILE]:{content:JSON.stringify({v:1,saved:new Date().toISOString(),data})}}});
  /* conflicto (los dos aparatos cambiaron lo mismo): listas con id se juntan; el calendario junta exámenes y palomitas */
  function both(k,l,r,first){
    try{
      const a=JSON.parse(l),b=JSON.parse(r);
      const byId=(x,y)=>{const m=new Map();y.forEach(e=>e&&e.id!=null&&m.set(e.id,e));x.forEach(e=>e&&e.id!=null&&m.set(e.id,e));return [...m.values()]};
      if(Array.isArray(a)&&Array.isArray(b)&&a.concat(b).every(e=>e&&typeof e==="object"&&"id" in e))return JSON.stringify(byId(a,b));
      if(a&&b&&Array.isArray(a.exams)&&Array.isArray(b.exams))return JSON.stringify(Object.assign({},b,a,{exams:byId(a.exams,b.exams),done:Object.assign({},b.done,a.done)}));
    }catch(e){}
    return first?r:l;
  }
  function merge(B,L,R,first){
    const out={},keys=new Set([...Object.keys(B),...Object.keys(L),...Object.keys(R)]);
    for(const k of keys){
      if(k.startsWith(P)||SKIP.has(k))continue;
      const b=B[k],l=L[k],r=R[k];let v;
      if(l===r)v=l;else if(l===b)v=r;else if(r===b)v=l;else if(l===undefined||r===undefined)v=l===undefined?r:l;else v=both(k,l,r,first);
      if(v!==undefined)out[k]=v;
    }
    return out;
  }
  const same=(a,b)=>{const ka=Object.keys(a),kb=Object.keys(b);return ka.length===kb.length&&ka.every(k=>a[k]===b[k])};
  async function sync(manual){
    if(!token())return;
    if(busy){again=true;return}
    busy=true;paint("…");
    try{
      let id=get(P+"gist"),first=!get(P+"base");
      if(!id){id=await findGist();if(id)set(P+"gist",id)}
      const L=snap();
      if(!id){
        const g=await gh("/gists",{method:"POST",body:JSON.stringify(Object.assign(JSON.parse(body(L)),{description:DESC,public:false}))});
        set(P+"gist",g.id);set(P+"base",JSON.stringify(L));
      }else{
        let R;try{R=await readRemote(id)}catch(e){if(/ 404$/.test(e.message)){del(P+"gist");busy=false;return sync(manual)}throw e}
        const out=merge(base(),L,R,first);
        let changed=false;
        for(const k of Object.keys(L))if(!(k in out)){del(k);changed=true}
        for(const k in out)if(L[k]!==out[k]){set(k,out[k]);changed=true}
        if(!same(out,R))await gh("/gists/"+id,{method:"PATCH",body:body(out)});
        set(P+"base",JSON.stringify(out));
        if(changed)arrived();
      }
      lastOk=Date.now();set(P+"ok",String(lastOk));lastErr="";
    }catch(e){lastErr=e.auth?"La clave no sirve o ya no tiene permiso":navigator.onLine===false?"Sin internet: se sincroniza al volver":"No pude sincronizar ahora"}
    busy=false;paint();
    if(again){again=false;sync()}
  }
  function arrived(){
    const typing=document.activeElement&&/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName);
    if(Date.now()-T0<10000||document.hidden){location.reload();return}
    toast("Llegaron cambios de tu otro aparato","Ver",()=>location.reload(),typing);
  }
  function toast(msg,btn,fn){
    if(document.getElementById("syncToast"))return;
    const d=document.createElement("div");d.id="syncToast";
    d.style.cssText="position:fixed;z-index:99998;left:50%;bottom:calc(22px + env(safe-area-inset-bottom));transform:translateX(-50%);background:#00543c;color:#fff;font:600 14px system-ui;padding:10px 12px 10px 16px;border-radius:999px;box-shadow:0 10px 30px rgba(0,0,0,.35);display:flex;gap:12px;align-items:center;max-width:calc(100vw - 32px)";
    d.innerHTML='<span></span><button style="border:0;background:#f26b21;color:#fff;font:700 13px system-ui;padding:7px 14px;border-radius:999px;cursor:pointer;white-space:nowrap"></button>';
    d.querySelector("span").textContent=msg;const b=d.querySelector("button");b.textContent=btn;b.onclick=()=>{d.remove();fn()};
    document.body.appendChild(d);
  }
  window.__medToast=toast;

  /* ===== botón y panel ===== */
  const css=`#syncBtn{position:fixed;z-index:9990;right:calc(14px + env(safe-area-inset-right));bottom:calc(14px + env(safe-area-inset-bottom));width:42px;height:42px;border-radius:50%;border:1px solid rgba(255,255,255,.25);background:rgba(0,59,42,.88);color:#fff;display:grid;place-items:center;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.25);backdrop-filter:blur(6px)}
#syncBtn svg{width:20px;height:20px}#syncBtn i{position:absolute;right:3px;top:3px;width:9px;height:9px;border-radius:50%;background:#9aa;border:2px solid #003b2a}
#syncBtn.ok i{background:#3ddc84}#syncBtn.err i{background:#f26b21}#syncBtn.run svg{animation:syncspin 1s linear infinite}@keyframes syncspin{to{transform:rotate(360deg)}}
#syncDlg{position:fixed;inset:0;z-index:99997;background:rgba(0,20,14,.55);display:grid;place-items:center;padding:16px}
#syncDlg .card{background:#fffdf8;color:#1d2a24;max-width:440px;width:100%;border-radius:18px;padding:22px 20px;font:15px/1.5 system-ui;box-shadow:0 20px 60px rgba(0,0,0,.4);max-height:calc(100vh - 32px);overflow:auto}
#syncDlg h3{margin:0 0 6px;font:700 19px system-ui;color:#00543c}#syncDlg p{margin:6px 0}#syncDlg ol{padding-left:20px;margin:8px 0}#syncDlg li{margin:6px 0}
#syncDlg a{color:#c4521a;font-weight:600}#syncDlg input{width:100%;box-sizing:border-box;font:14px ui-monospace,monospace;padding:10px 12px;border:1px solid #c9d3cd;border-radius:10px;margin:6px 0;background:#fff;color:#1d2a24}
#syncDlg .row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}#syncDlg button{border:0;border-radius:999px;padding:9px 16px;font:700 14px system-ui;cursor:pointer;background:#00543c;color:#fff}
#syncDlg button.sec{background:#e8ece9;color:#1d2a24}#syncDlg .st{font-size:13px;color:#5b6b63}#syncDlg .bad{color:#b3401a}
@media (prefers-color-scheme:dark){#syncDlg .card{background:#13201b;color:#e7eee9}#syncDlg input{background:#0c1612;color:#e7eee9;border-color:#2c3d35}#syncDlg button.sec{background:#24332c;color:#e7eee9}#syncDlg .st{color:#9fb2a8}#syncDlg a{color:#ff9a5c}}`;
  const ICON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 0 1-15.5 6.2"/><path d="M3 12A9 9 0 0 1 18.5 5.8"/><path d="M18 2v4h-4"/><path d="M6 22v-4h4"/></svg>';
  const ago=t=>{if(!t)return "nunca";const m=Math.round((Date.now()-t)/6e4);return m<1?"hace un momento":m<60?"hace "+m+" min":m<1440?"hace "+Math.round(m/60)+" h":"hace "+Math.round(m/1440)+" días"};
  function paint(run){
    const b=document.getElementById("syncBtn");if(!b)return;
    b.className=run?"run":!token()?"":lastErr?"err":"ok";
    b.title=!token()?"Sincronizar Mac y cel":lastErr||("Sincronizado "+ago(lastOk));
    b.hidden=!!location.hash.replace("#","")&&location.hash!=="#inicio";
    const c=document.getElementById("calSync");
    if(c&&token()&&!lastErr&&lastOk){c.classList.add("ok");const s=c.querySelector("span");if(s)s.textContent="Sincronizado con tu Mac y tu cel · "+ago(lastOk)}
    const d=document.getElementById("syncDlg");if(d&&!run)render(d);
  }
  function render(d){
    const c=d.querySelector(".card");
    if(token()){
      c.innerHTML=`<h3>Sincronización activa</h3><p>Tus exámenes, plan de estudio, material y avances de las guías se comparten entre todos los aparatos donde pegaste esta clave.</p>
<p class="st ${lastErr?"bad":""}">${lastErr||"Última sincronización: "+ago(lastOk)}</p>
<div class="row"><button data-a="now">Sincronizar ahora</button><button class="sec" data-a="close">Cerrar</button></div>
<p class="st" style="margin-top:16px">¿Cambiaste de clave? <a href="#" data-a="off">Desconectar este aparato</a></p>`;
    }else{
      c.innerHTML=`<h3>Sincronizar Mac y cel</h3><p>Tus exámenes, plan, material y avances se guardan en un archivo privado de tu cuenta de GitHub, y tus aparatos lo comparten. Se hace una sola vez:</p>
<ol><li><a href="https://github.com/settings/tokens/new?scopes=gist&description=Medicina%20UDLAP" target="_blank" rel="noopener">Abre esta página de GitHub</a> (ya trae todo marcado).</li><li>En <b>Expiration</b> elige <b>No expiration</b>, baja hasta el final y presiona <b>Generate token</b>.</li><li>Copia la clave que empieza con <b>ghp_</b> y pégala aquí. Usa la misma en tu Mac y en tu cel.</li></ol>
<input placeholder="ghp_…" autocomplete="off" autocapitalize="off" spellcheck="false"><p class="st bad" hidden></p>
<div class="row"><button data-a="go">Conectar</button><button class="sec" data-a="close">Cerrar</button></div>`;
    }
  }
  function open(){
    let d=document.getElementById("syncDlg");if(d)return;
    d=document.createElement("div");d.id="syncDlg";d.innerHTML='<div class="card" role="dialog" aria-modal="true"></div>';
    document.body.appendChild(d);render(d);
    d.addEventListener("click",async ev=>{
      if(ev.target===d){d.remove();return}
      const a=ev.target.closest("[data-a]");if(!a)return;
      const k=a.dataset.a;
      if(k==="close")d.remove();
      else if(k==="now")sync(true);
      else if(k==="off"){ev.preventDefault();[P+"token",P+"gist",P+"base",P+"ok"].forEach(del);lastOk=0;lastErr="";paint()}
      else if(k==="go"){
        const v=d.querySelector("input").value.trim(),e=d.querySelector(".bad");
        if(!/^(ghp_|github_pat_)[A-Za-z0-9_]{20,}$/.test(v)){e.hidden=false;e.textContent="Esa no parece una clave de GitHub (empieza con ghp_).";return}
        a.disabled=true;a.textContent="Conectando…";set(P+"token",v);del(P+"base");del(P+"gist");
        await sync(true);
        if(lastErr){const er=lastErr;del(P+"token");lastErr="";render(d);const e2=d.querySelector(".bad");e2.hidden=false;e2.textContent=er}
      }
    });
  }
  function mount(){
    const st=document.createElement("style");st.textContent=css;document.head.appendChild(st);
    const b=document.createElement("button");b.id="syncBtn";b.type="button";b.setAttribute("aria-label","Sincronizar Mac y cel");b.innerHTML=ICON+"<i></i>";b.onclick=open;
    document.body.appendChild(b);paint();
    addEventListener("hashchange",()=>paint());
  }
  if(document.readyState==="loading")addEventListener("DOMContentLoaded",mount);else mount();
  /* cuándo sincroniza: al abrir, al volver a la app, cada minuto, y unos segundos después de cualquier cambio */
  setTimeout(()=>sync(),1200);
  addEventListener("visibilitychange",()=>{if(!document.hidden)sync()});
  addEventListener("online",()=>sync());
  setInterval(()=>{if(!document.hidden)sync()},60000);
  setInterval(()=>{if(token()&&!busy&&!same(snap(),base()))sync()},5000);
  setInterval(()=>paint(),30000);
})();
