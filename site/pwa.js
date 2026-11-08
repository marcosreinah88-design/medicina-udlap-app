/* Medicina UDLAP · instalación en el cel (pantalla de inicio) y avisos de versión nueva */
(()=>{
  if(!("serviceWorker" in navigator)||location.protocol!=="https:"&&location.hostname!=="localhost")return;
  const toast=(m,b,f)=>window.__medToast&&window.__medToast(m,b,f);
  const first=!navigator.serviceWorker.controller;
  navigator.serviceWorker.register("sw.js").then(reg=>{
    const watch=w=>w&&w.addEventListener("statechange",()=>{
      if(w.state==="installed"){
        if(navigator.serviceWorker.controller)toast("Hay una versión nueva del repositorio","Actualizar",()=>w.postMessage("skip"));
        else toast("Listo: ya funciona sin internet","OK",()=>{});
      }
    });
    if(reg.waiting&&navigator.serviceWorker.controller)toast("Hay una versión nueva del repositorio","Actualizar",()=>reg.waiting.postMessage("skip"));
    watch(reg.installing);
    reg.addEventListener("updatefound",()=>watch(reg.installing));
    document.addEventListener("visibilitychange",()=>{if(!document.hidden)reg.update().catch(()=>{})});
    setInterval(()=>reg.update().catch(()=>{}),30*60e3);
  }).catch(()=>{});
  let reloading=false;
  navigator.serviceWorker.addEventListener("controllerchange",()=>{if(!first&&!reloading){reloading=true;location.reload()}});
})();
