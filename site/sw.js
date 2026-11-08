/* Medicina UDLAP · funciona sin internet: guarda todo el repositorio en el cel y lo renueva cuando hay versión nueva */
const V=1794163738,C="med-"+V;
self.addEventListener("install",ev=>ev.waitUntil((async()=>{
  const man=await (await fetch("manifest.json?v="+V,{cache:"no-store"})).json();
  const cache=await caches.open(C);
  let oldHashes={},old=null;
  for(const k of await caches.keys()){if(k!==C&&k.startsWith("med-")){old=await caches.open(k);const r=await old.match("__hashes");if(r)oldHashes=await r.json()}}
  const files=Object.keys(man.files).filter(f=>f!=="_headers"&&f!=="sw.js");
  let i=0;
  async function one(f){
    const url=new URL(f.split("/").map(encodeURIComponent).join("/"),self.registration.scope).href;
    let res=old&&oldHashes[f]===man.files[f]?await old.match(url):null;
    if(!res){res=await fetch(url,{cache:"no-store"});if(!res.ok)throw new Error(f)}
    await cache.put(url,res);
  }
  const queue=files.slice();
  await Promise.all(Array.from({length:6},async()=>{while(queue.length)await one(queue.shift())}));
  await cache.put("__hashes",new Response(JSON.stringify(man.files)));
})()));
self.addEventListener("activate",ev=>ev.waitUntil((async()=>{
  for(const k of await caches.keys())if(k!==C&&k.startsWith("med-"))await caches.delete(k);
  await self.clients.claim();
})()));
self.addEventListener("message",ev=>{if(ev.data==="skip")self.skipWaiting()});
self.addEventListener("fetch",ev=>{
  const u=new URL(ev.request.url);
  if(ev.request.method!=="GET"||u.origin!==location.origin)return;
  ev.respondWith((async()=>{
    const cache=await caches.open(C);
    let path=u.pathname;if(path.endsWith("/"))path+=ev.request.mode==="navigate"&&u.pathname===new URL(self.registration.scope).pathname?"app.html":"index.html";
    const hit=await cache.match(new URL(path,u.origin).href);
    if(hit)return hit;
    try{return await fetch(ev.request)}catch(e){
      if(ev.request.mode==="navigate"){const a=await cache.match(new URL("app.html",self.registration.scope).href);if(a)return a}
      return new Response("Sin internet",{status:503});
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
