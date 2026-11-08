/* Medicina UDLAP · sincronización entre aparatos (Mac y cel).
   Todo lo que la página guarda en este aparato (exámenes, plan, material, avances de las guías) se copia a un
   gist privado de la cuenta de GitHub de Marcos. Cada aparato junta sus cambios con los del otro (mezcla a tres bandas). */
(()=>{
  if(window.__medSync)return;window.__medSync=1;
  const okHost=location.protocol==="app:"||/github\.io$/.test(location.hostname)||/^(localhost|127\.0\.0\.1)$/.test(location.hostname);
  if(!okHost)return;
  const API=window.__MEDSYNC_API||"https://api.github.com",P="__medsync_",FILE="medicina-udlap.json",SENT="avisos-enviados.json";
  /* v2: el archivo va cifrado (AES-256-GCM) con una llave que sale de tu clave; GitHub solo guarda datos ilegibles.
     DESC_OLD es la copia vieja sin cifrar: si aparece, se junta con lo de este aparato y se borra. */
  const DESC="Medicina UDLAP · sincronización cifrada (no borrar)",DESC_OLD="Medicina UDLAP · sincronización (no borrar)";
  const GID=P+"gist2",BASE=P+"base2",LCHK=P+"lchk";
  const SKIP=new Set(["carrera-theme"]);
  const get=k=>{try{return localStorage.getItem(k)}catch(e){return null}},set=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}},del=k=>{try{localStorage.removeItem(k)}catch(e){}};
  const T0=Date.now();let flash=0,busy=false,again=false,lastOk=+get(P+"ok")||0,lastErr="";
  const token=()=>get(P+"token");
  function snap(){const o={};try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k&&!k.startsWith(P)&&!SKIP.has(k))o[k]=localStorage.getItem(k)}}catch(e){}return o}
  const base=()=>{try{return JSON.parse(get(BASE)||"{}")}catch(e){return {}}};
  /* ===== cifrado ===== */
  const te=new TextEncoder(),td=new TextDecoder();
  const toB64=u=>{let s="";const a=new Uint8Array(u);for(let i=0;i<a.length;i+=0x8000)s+=String.fromCharCode.apply(null,a.subarray(i,i+0x8000));return btoa(s)};
  const fromB64=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
  let kc=null,kfor=null;
  async function aesKey(){
    const t=token();if(kc&&kfor===t)return kc;
    const ikm=await crypto.subtle.importKey("raw",te.encode(t),"HKDF",false,["deriveKey"]);
    kc=await crypto.subtle.deriveKey({name:"HKDF",hash:"SHA-256",salt:te.encode("medicina-udlap/sync/v2"),info:te.encode("datos")},ikm,{name:"AES-GCM",length:256},false,["encrypt","decrypt"]);
    kfor=t;return kc;
  }
  const AAD=te.encode(FILE);
  async function seal(data){
    const iv=crypto.getRandomValues(new Uint8Array(12));
    const ct=await crypto.subtle.encrypt({name:"AES-GCM",iv,additionalData:AAD},await aesKey(),te.encode(JSON.stringify({data})));
    return JSON.stringify({v:2,alg:"A256GCM",saved:new Date().toISOString(),iv:toB64(iv),ct:toB64(ct)});
  }
  async function unseal(txt){
    let j;try{j=JSON.parse(txt)}catch(e){return {}}
    if(!j||j.v!==2)return j&&j.data&&typeof j.data==="object"?j.data:{};
    let pt;try{pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:fromB64(j.iv),additionalData:AAD},await aesKey(),fromB64(j.ct))}
    catch(e){throw Object.assign(new Error("llave"),{nokey:true})}
    const d=JSON.parse(td.decode(pt)).data;return d&&typeof d==="object"?d:{};
  }
  async function gh(path,opt={}){
    const r=await fetch(API+path,Object.assign({cache:"no-store"},opt,{headers:Object.assign({Authorization:"Bearer "+token(),Accept:"application/vnd.github+json"},opt.body?{"Content-Type":"application/json"}:{})}));
    if(r.status===401||r.status===403)throw Object.assign(new Error("clave"),{auth:true});
    if(!r.ok)throw new Error("GitHub "+r.status);
    return r.status===204?{}:r.json();
  }
  async function findGists(){
    const out={enc:null,old:[]};
    for(let page=1;page<=5;page++){
      const l=await gh("/gists?per_page=100&page="+page);
      for(const x of l){if(!x||!x.files||!x.files[FILE])continue;if(x.description===DESC&&!out.enc)out.enc=x.id;else if(x.description===DESC_OLD)out.old.push(x.id)}
      if(l.length<100)break;
    }
    return out;
  }
  async function fileText(f){if(!f)return null;if(!f.truncated)return f.content;const r=await fetch(f.raw_url,{cache:"no-store"});return r.text()}
  async function readRemote(id){
    const g=await gh("/gists/"+id),txt=await fileText(g.files&&g.files[FILE]);
    return txt==null?{}:unseal(txt);
  }
  /* conflicto (los dos aparatos cambiaron lo mismo): listas con id se juntan; el calendario junta exámenes y palomitas */
  function both(k,l,r,first){
    try{
      const a=JSON.parse(l),b=JSON.parse(r);
      const byId=(x,y)=>{const m=new Map();y.forEach(e=>e&&e.id!=null&&m.set(e.id,e));x.forEach(e=>e&&e.id!=null&&m.set(e.id,e));return [...m.values()]};
      if(Array.isArray(a)&&Array.isArray(b)&&a.concat(b).every(e=>e&&typeof e==="object"&&"id" in e))return JSON.stringify(byId(a,b));
      if(a&&b&&Array.isArray(a.items)&&Array.isArray(b.items))return JSON.stringify(Object.assign({},b,a,{items:byId(a.items,b.items)}));
      if(a&&b&&Array.isArray(a.exams)&&Array.isArray(b.exams))return JSON.stringify(Object.assign({},b,a,{exams:byId(a.exams,b.exams),done:Object.assign({},b.done,a.done),tasks:byId(a.tasks||[],b.tasks||[])}));
    }catch(e){}
    return first?r:l;
  }
  function merge(B,L,R,first){
    const out={},keys=new Set([...Object.keys(B),...Object.keys(L),...Object.keys(R)]);
    for(const k of keys){
      if(k.startsWith(P)||SKIP.has(k))continue;
      const b=B[k],l=L[k],r=R[k];let v;
      if(l===r)v=l;else if(l===b)v=r;else if(r===b)v=l;else if(l===undefined||r===undefined)v=l===undefined?r:l;else v=both(k,l,r,first);
      if(typeof v==="string")out[k]=v;
    }
    return out;
  }
  const same=(a,b)=>{const ka=Object.keys(a),kb=Object.keys(b);return ka.length===kb.length&&ka.every(k=>a[k]===b[k])};
  /* copia vieja sin cifrar: se junta con lo de este aparato (sin borrar nada de aquí) */
  async function absorbOld(ids){
    let changed=false,sent=null;
    for(const oid of ids){
      const g=await gh("/gists/"+oid),txt=await fileText(g.files&&g.files[FILE]);
      if(g.files&&g.files[SENT])sent=await fileText(g.files[SENT]);
      let R0={};try{const j=JSON.parse(txt||"{}");R0=j&&j.data&&typeof j.data==="object"?j.data:{}}catch(e){}
      const L=snap();
      for(const k in R0){
        const v=R0[k];if(k.startsWith(P)||SKIP.has(k)||typeof v!=="string")continue;
        const m=k in L?both(k,L[k],v,false):v;
        if(m!==L[k]){set(k,m);changed=true}
      }
    }
    return {changed,sent};
  }
  async function sync(manual){
    if(!token())return;
    if(busy){again=true;return}
    busy=true;paint("…");
    try{
      let id=get(GID),first=!get(BASE),old=[],changed=false,warn="";
      const now=Date.now();
      if(!id||now-(+get(LCHK)||0)>10*60e3){const f=await findGists();if(!id&&f.enc){id=f.enc;set(GID,id)}old=f.old;set(LCHK,String(now))}
      let sentOld=null;
      if(old.length){const a=await absorbOld(old);changed=a.changed;sentOld=a.sent}
      const L=snap();
      if(!id){
        const files={[FILE]:{content:await seal(L)}};if(sentOld)files[SENT]={content:sentOld};
        const g=await gh("/gists",{method:"POST",body:JSON.stringify({description:DESC,public:false,files})});
        set(GID,g.id);set(BASE,JSON.stringify(L));
      }else{
        let R;
        try{R=await readRemote(id)}
        catch(e){
          if(/ 404$/.test(e.message)){del(GID);del(BASE);del(LCHK);busy=false;return sync(manual)}
          if(!e.nokey)throw e;
          R=null;warn="Tu otro aparato usa una clave distinta: pon la misma clave en los dos";
        }
        const out=R?merge(base(),L,R,first):L;
        for(const k of Object.keys(L))if(!(k in out)){del(k);changed=true}
        for(const k in out)if(L[k]!==out[k]){set(k,out[k]);changed=true}
        if(!R||!same(out,R))await gh("/gists/"+id,{method:"PATCH",body:JSON.stringify({files:{[FILE]:{content:await seal(out)}}})});
        set(BASE,JSON.stringify(out));
      }
      /* ya quedó la copia cifrada: se borran las copias viejas sin cifrar */
      for(const oid of old){try{await gh("/gists/"+oid,{method:"DELETE"})}catch(e){}}
      del(P+"gist");del(P+"base");
      if(changed)arrived();
      lastOk=Date.now();set(P+"ok",String(lastOk));lastErr=warn;
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
<p class="st ${lastErr?"bad":""}" style="${!lastErr&&Date.now()-flash<5000?"color:#0a7a4f;font-weight:700":""}">${lastErr||(Date.now()-flash<5000?"✓ Listo, todo está al día en este aparato":"Última sincronización: "+ago(lastOk))}</p>
<div class="row"><button data-a="now">Sincronizar ahora</button><button class="sec" data-a="close">Cerrar</button></div>
${pushHTML()}
<p class="st" style="margin-top:16px">¿Cambiaste de clave? <a href="#" data-a="off">Desconectar este aparato</a></p>`;
    }else{
      c.innerHTML=`<h3>Sincronizar Mac y cel</h3><p>Tus exámenes, plan, material y avances se guardan cifrados en un archivo privado de tu cuenta de GitHub, y tus aparatos lo comparten. Se hace una sola vez:</p>
<ol><li><a href="https://github.com/settings/tokens/new?scopes=gist&description=Medicina%20UDLAP" target="_blank" rel="noopener">Abre esta página de GitHub</a> (ya trae todo marcado).</li><li>En <b>Expiration</b> elige <b>No expiration</b>, baja hasta el final y presiona <b>Generate token</b>.</li><li>Copia la clave que empieza con <b>ghp_</b> y pégala aquí. Usa la misma en tu Mac y en tu cel.</li></ol>
<input placeholder="ghp_…" autocomplete="off" autocapitalize="off" spellcheck="false"><p class="st bad" hidden></p>
<div class="row"><button data-a="go">Conectar</button><button class="sec" data-a="close">Cerrar</button></div>`;
    }
  }
  /* ===== avisos en el cel (Web Push) ===== */
  const canPush=()=>location.protocol!=="app:"&&"serviceWorker" in navigator&&"PushManager" in window&&"Notification" in window;
  const standalone=()=>matchMedia("(display-mode: standalone)").matches||navigator.standalone===true;
  const pushOn=()=>!!get(P+"pushdev")&&window.Notification&&Notification.permission==="granted";
  function pushHTML(){
    if(location.protocol==="app:")return `<p class="st">En esta Mac los avisos los manda la app (menú Avisos).</p>`;
    if(!canPush())return `<h3 style="margin-top:18px;font-size:16px">Avisos en este cel</h3><p class="st">${/iPhone|iPad/.test(navigator.userAgent)&&!standalone()?"Para recibir avisos, primero agrega la app a tu pantalla de inicio (Compartir → Agregar a pantalla de inicio) y ábrela desde ese ícono.":"Este navegador no permite avisos."}</p>`;
    if(!pushOn())return `<h3 style="margin-top:18px;font-size:16px">Avisos en este cel</h3><p>Exámenes, plan de estudio, fechas UDLAP y partidos, aunque la app esté cerrada.</p><p class="st bad" id="pushErr" hidden></p><div class="row"><button data-a="push">Activar avisos</button></div>`;
    return `<h3 style="margin-top:18px;font-size:16px">Avisos en este cel: activados</h3>${get(P+"secret")?`<p class="st">GitHub te los manda (pueden llegar unos minutos tarde).</p>`:`<p><b>Último paso, una sola vez:</b> para que GitHub pueda mandarte los avisos necesita tu misma clave.</p><ol><li><a href="https://github.com/marcosreinah88-design/medicina-udlap-app/settings/secrets/actions/new" target="_blank" rel="noopener">Abre esta página de GitHub</a>.</li><li>En <b>Name</b> escribe <b>MED_SYNC</b>.</li><li>En <b>Secret</b> pega tu clave (la misma ghp_…) y presiona <b>Add secret</b>.</li></ol><div class="row"><button class="sec" data-a="secret">Ya la guardé</button></div>`}<div class="row"><button class="sec" data-a="ptest">Probar un aviso aquí</button><button class="sec" data-a="poff">Apagar avisos en este cel</button></div>`;
  }
  const b64u=b=>btoa(String.fromCharCode(...new Uint8Array(b))).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"");
  const ub64=s=>{s=s.replace(/-/g,"+").replace(/_/g,"/");s+="===".slice((s.length+3)%4);return Uint8Array.from(atob(s),c=>c.charCodeAt(0))};
  async function vapid(){
    let v=null;try{v=JSON.parse(get("medicina-push-vapid")||"null")}catch(e){}
    if(v&&v.publicKey&&v.privateKey)return v;
    const k=await crypto.subtle.generateKey({name:"ECDSA",namedCurve:"P-256"},true,["sign"]);
    const pub=b64u(await crypto.subtle.exportKey("raw",k.publicKey)),jwk=await crypto.subtle.exportKey("jwk",k.privateKey);
    v={publicKey:pub,privateKey:jwk.d};set("medicina-push-vapid",JSON.stringify(v));return v;
  }
  async function pushEnable(){
    const perm=await Notification.requestPermission();
    if(perm!=="granted")throw new Error("Sin permiso: actívalo en Ajustes → Notificaciones → Medicina UDLAP.");
    await sync(true);
    const v=await vapid(),reg=await navigator.serviceWorker.ready;
    let sub=await reg.pushManager.getSubscription();
    if(sub&&b64u(sub.options&&sub.options.applicationServerKey||new ArrayBuffer(0))!==v.publicKey){try{await sub.unsubscribe()}catch(e){}sub=null}
    if(!sub)sub=await reg.pushManager.subscribe({userVisibleOnly:true,applicationServerKey:ub64(v.publicKey)});
    const dev=get(P+"pushdev")||("cel-"+Math.random().toString(36).slice(2,10));
    let subs=[];try{subs=JSON.parse(get("medicina-push-subs")||"[]")}catch(e){}
    subs=subs.filter(x=>x&&x.id!==dev).concat([{id:dev,sub:sub.toJSON(),ua:navigator.userAgent.slice(0,120),t:Date.now()}]);
    set("medicina-push-subs",JSON.stringify(subs));set(P+"pushdev",dev);
    await sync(true);
  }
  async function pushOff(){
    const dev=get(P+"pushdev");
    try{const reg=await navigator.serviceWorker.ready,sub=await reg.pushManager.getSubscription();if(sub)await sub.unsubscribe()}catch(e){}
    let subs=[];try{subs=JSON.parse(get("medicina-push-subs")||"[]")}catch(e){}
    set("medicina-push-subs",JSON.stringify(subs.filter(x=>x&&x.id!==dev)));del(P+"pushdev");await sync(true);
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
      else if(k==="now"){a.disabled=true;a.textContent="Sincronizando…";await sync(true);flash=Date.now();render(d);setTimeout(()=>{const x=document.getElementById("syncDlg");if(x)render(x)},5200)}
      else if(k==="off"){ev.preventDefault();[P+"token",GID,BASE,LCHK,P+"gist",P+"base",P+"ok",P+"secret"].forEach(del);kc=null;lastOk=0;lastErr="";paint()}
      else if(k==="push"){a.disabled=true;a.textContent="Activando…";try{await pushEnable()}catch(er){render(d);const e=d.querySelector("#pushErr");if(e){e.hidden=false;e.textContent=er.message&&/[áéíóú]|Sin/.test(er.message)?er.message:"No se pudo activar: "+(er.message||er)}return}render(d)}
      else if(k==="secret"){set(P+"secret","1");render(d)}
      else if(k==="poff"){await pushOff();render(d)}
      else if(k==="ptest"){try{const reg=await navigator.serviceWorker.ready;reg.showNotification("Aviso de prueba",{body:"Así te van a llegar los avisos de exámenes, plan, fechas UDLAP y partidos.",icon:"icon-192.png"})}catch(e){}}
      else if(k==="go"){
        const v=d.querySelector("input").value.trim(),e=d.querySelector(".bad");
        if(!/^(ghp_|github_pat_)[A-Za-z0-9_]{20,}$/.test(v)){e.hidden=false;e.textContent="Esa no parece una clave de GitHub (empieza con ghp_).";return}
        a.disabled=true;a.textContent="Conectando…";set(P+"token",v);[GID,BASE,LCHK,P+"base",P+"gist"].forEach(del);
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
