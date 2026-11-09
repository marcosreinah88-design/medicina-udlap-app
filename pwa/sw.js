/* Medicina UDLAP · funciona sin internet.
   1) Al instalarse guarda lo básico (portada, tipografías, scripts) para que la app abra sin internet.
   2) Después baja el resto (semestres y guías) poco a poco; si se corta, sigue donde se quedó.
   3) Cada vez que se abre la app revisa manifest.json y solo baja los archivos que cambiaron.
   No hay que cambiar nada aquí al publicar: la versión sale de manifest.json. */
const C="med-offline",H="__hashes";
const scope=()=>self.registration.scope;
const urlOf=f=>new URL(f.split("/").map(encodeURIComponent).join("/"),scope()).href;
const skip=f=>f==="_headers"||f==="sw.js"||f==="manifest.json"||f==="manifest.sig";
const basic=f=>!f.includes("/")||f.startsWith("fonts/")||f.startsWith("img/");

async function getManifest(){
  const r=await fetch(new URL("manifest.json",scope()).href+"?t="+Date.now(),{cache:"no-store"});
  if(!r.ok)throw new Error("manifest");
  return r.json();
}
async function readHashes(cache){const r=await cache.match(H);return r?r.json():{}}
async function fetchOk(url){
  let err;
  for(let i=0;i<3;i++){
    try{const r=await fetch(url,{cache:"no-cache"});if(r.ok&&!r.redirected)return r;err=new Error(r.status)}catch(e){err=e}
    await new Promise(z=>setTimeout(z,800*(i+1)));
  }
  throw err;
}
/* copia lo que ya estaba en cachés viejas (versiones anteriores de este sw) para no volver a bajarlo */
async function adoptOld(cache,man,hashes){
  for(const k of await caches.keys()){
    if(k===C||!k.startsWith("med-"))continue;
    const old=await caches.open(k);const r=await old.match(H);const oh=r?await r.json():{};
    for(const f in man.files){
      if(hashes[f]===man.files[f]||oh[f]!==man.files[f])continue;
      const hit=await old.match(urlOf(f));if(hit){await cache.put(urlOf(f),hit);hashes[f]=man.files[f]}
    }
  }
}
async function tell(msg){for(const c of await self.clients.matchAll({includeUncontrolled:true}))c.postMessage(msg)}

/* baja lo que falte o haya cambiado; onlyBasic=true solo lo necesario para abrir */
let running=null,runningFull=false,again=false;
function sync(onlyBasic){
  if(running){
    if(onlyBasic)return running;
    if(runningFull){again=true;return running}
    return running.catch(()=>{}).then(()=>sync(false));
  }
  again=false;
  runningFull=!onlyBasic;
  running=(async()=>{
    const man=await getManifest();
    const cache=await caches.open(C);
    const hashes=await readHashes(cache);
    await adoptOld(cache,man,hashes);
    const want=Object.keys(man.files).filter(f=>!skip(f)&&(!onlyBasic||basic(f)));
    const todo=want.filter(f=>hashes[f]!==man.files[f]).sort((a,b)=>basic(b)-basic(a));
    const appChanged=todo.some(f=>basic(f)&&hashes[f]);
    let done=0,failed=0,lastSave=Date.now();
    const save=()=>cache.put(H,new Response(JSON.stringify(hashes)));
    const queue=todo.slice();
    await Promise.all(Array.from({length:4},async()=>{
      while(queue.length){
        const f=queue.shift();
        try{await cache.put(urlOf(f),await fetchOk(urlOf(f)));hashes[f]=man.files[f]}
        catch(e){failed++;if(onlyBasic)throw e}
        done++;
        if(Date.now()-lastSave>3000){lastSave=Date.now();await save();if(!onlyBasic)tell({type:"med-progress",done,total:todo.length})}
      }
    }));
    if(!onlyBasic){
      for(const f of Object.keys(hashes))if(!(f in man.files)){delete hashes[f];await cache.delete(urlOf(f))}
    }
    await save();
    const r={complete:!onlyBasic&&failed===0,downloaded:todo.length-failed,failed,appChanged:!onlyBasic&&appChanged&&failed===0};
    if(!onlyBasic)tell({type:"med-synced",...r});
    return r;
  })().finally(()=>{running=null;runningFull=false});
  /* si pidieron revisar otra vez mientras bajaba (por ejemplo, volvió el internet), repite una vez */
  running.then(r=>{if(again&&!r.complete)return sync(false)}).catch(()=>{});
  return running;
}

self.addEventListener("install",ev=>ev.waitUntil(sync(true).then(()=>self.skipWaiting())));
self.addEventListener("activate",ev=>ev.waitUntil((async()=>{
  for(const k of await caches.keys())if(k!==C&&k.startsWith("med-"))await caches.delete(k);
  await self.clients.claim();
})()));
self.addEventListener("message",ev=>{
  if(ev.data==="sync")ev.waitUntil(sync(false).catch(()=>tell({type:"med-synced",offline:true})));
  else if(ev.data==="skip")self.skipWaiting();
});
self.addEventListener("fetch",ev=>{
  const u=new URL(ev.request.url);
  if(ev.request.method!=="GET"||u.origin!==location.origin)return;
  const sp=new URL(scope()).pathname;
  if(!u.pathname.startsWith(sp))return;
  let rel=decodeURIComponent(u.pathname.slice(sp.length));
  if(rel===""||rel.endsWith("/"))rel+=rel===""&&ev.request.mode==="navigate"?"app.html":"index.html";
  if(rel==="manifest.json"||rel==="manifest.sig"||rel==="sw.js")return;
  ev.respondWith((async()=>{
    const cache=await caches.open(C);
    const hit=await cache.match(urlOf(rel));
    if(hit)return hit;
    try{
      const r=await fetch(ev.request);
      /* lo que se abra con internet también queda guardado */
      if(r.ok&&!r.redirected&&r.type==="basic")cache.put(urlOf(rel),r.clone()).catch(()=>{});
      return r;
    }catch(e){
      if(ev.request.mode==="navigate"){const a=await cache.match(urlOf("app.html"));if(a)return a}
      return new Response("Sin internet",{status:503,headers:{"Content-Type":"text/plain; charset=utf-8"}});
    }
  })());
});
/* avisos que manda GitHub (exámenes, plan, fechas UDLAP, partidos) */
self.addEventListener("push",ev=>{
  let d={};try{d=ev.data?ev.data.json():{}}catch(e){d={title:"Medicina UDLAP",body:ev.data?ev.data.text():""}}
  ev.waitUntil(self.registration.showNotification(d.title||"Aviso",{body:d.body||"",icon:"icon-192.png",badge:"icon-192.png",tag:d.id||undefined,data:{route:d.route||"calendario"}}));
});
self.addEventListener("notificationclick",ev=>{
  ev.notification.close();
  const url=new URL("app.html#"+(ev.notification.data&&ev.notification.data.route||"calendario"),self.registration.scope).href;
  ev.waitUntil((async()=>{
    const cs=await self.clients.matchAll({type:"window",includeUncontrolled:true});
    for(const c of cs){if("focus" in c){try{await c.navigate(url)}catch(e){}return c.focus()}}
    return self.clients.openWindow(url);
  })());
});
