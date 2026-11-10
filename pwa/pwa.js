/* Medicina UDLAP · instalación en el cel (pantalla de inicio), uso sin internet y avisos de versión nueva */
(()=>{
  if(!("serviceWorker" in navigator)||location.protocol!=="https:"&&location.hostname!=="localhost")return;
  const sw=navigator.serviceWorker;
  let box;
  function toast(msg,btn,fn,ms){
    if(!document.body)return;
    if(!box){box=document.createElement("div");box.setAttribute("role","status");
      box.style.cssText="position:fixed;left:50%;bottom:calc(76px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:99999;max-width:calc(100% - 32px);display:flex;gap:12px;align-items:center;background:#00573c;color:#fff;font:500 14px/1.3 system-ui,-apple-system,sans-serif;padding:10px 14px;border-radius:12px;box-shadow:0 6px 24px rgba(0,0,0,.25)";
      document.body.appendChild(box)}
    box.textContent=msg;box.style.display="flex";
    if(btn){const b=document.createElement("button");b.textContent=btn;
      b.style.cssText="background:#f26b21;color:#fff;border:0;border-radius:8px;padding:6px 10px;font:600 13px system-ui,-apple-system,sans-serif";
      b.onclick=()=>{box.style.display="none";fn&&fn()};box.appendChild(b)}
    clearTimeout(box._t);if(ms)box._t=setTimeout(()=>{box.style.display="none"},ms);
  }
  const KEY="med-offline-listo";
  const ready=()=>{try{return localStorage.getItem(KEY)==="1"}catch(e){return false}};
  let shownProgress=false;
  sw.addEventListener("message",ev=>{
    const d=ev.data||{};
    if(d.type==="med-progress"&&!ready()&&d.total>20){shownProgress=true;toast("Guardando para usar sin internet… "+Math.round(100*d.done/d.total)+"%")}
    if(d.type==="med-synced"){
      if(d.complete&&!ready()){try{localStorage.setItem(KEY,"1")}catch(e){}toast("Listo: ya funciona sin internet","OK",null,6000)}
      else if(d.appChanged)toast("Hay una versión nueva del repositorio","Actualizar",()=>location.reload());
      else if(shownProgress&&box)box.style.display="none";
    }
  });
  const ask=()=>{if(navigator.onLine!==false&&sw.controller)sw.controller.postMessage("sync")};
  sw.register("sw.js").then(reg=>{
    sw.ready.then(ask);
    document.addEventListener("visibilitychange",()=>{if(!document.hidden){reg.update().catch(()=>{});ask()}});
    window.addEventListener("online",ask);
    setInterval(()=>{reg.update().catch(()=>{});ask()},30*60e3);
  }).catch(()=>{});
  /* cuando entra un service worker nuevo, recarga una vez para que tome el control */
  const hadController=!!sw.controller;let reloading=false;
  sw.addEventListener("controllerchange",()=>{if(hadController&&!reloading){reloading=true;location.reload()}else ask()});
})();
