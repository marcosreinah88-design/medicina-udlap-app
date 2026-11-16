// Imágenes de arranque del iPhone (lo que se ve al abrir la app del cel antes de que cargue la página).
// Son la misma pantalla de carga (carga.html), quieta. Uso: (servir site/ en :8765) node tools-carga/splash.js
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const here=__dirname,out=path.join(here,'..','site','img','arranque');fs.mkdirSync(out,{recursive:true});
const block=fs.readFileSync(path.join(here,'carga.html'),'utf8').replace('{{ESCUDO}}',fs.readFileSync(path.join(here,'escudo.b64'),'utf8').trim()).replace(/<script>[\s\S]*?<\/script>/,'');
const css=fs.readFileSync(path.join(here,'..','site','app.html'),'utf8').match(/href="fonts\/([^"]+\.css)"/)[1];
const html=`<!doctype html><html lang="es"><meta charset="utf-8"><link rel="stylesheet" href="fonts/${css}"><body style="margin:0">${block}</body></html>`;
(async()=>{const b=await chromium.launch();
for(const [w,h,d] of JSON.parse(fs.readFileSync(path.join(here,'tamanos.json')))){
  const c=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:d,colorScheme:'light',reducedMotion:'reduce'});const p=await c.newPage();
  await p.route('http://localhost:8765/splash.html',r=>r.fulfill({contentType:'text/html; charset=utf-8',body:html}));
  await p.goto('http://localhost:8765/splash.html');await p.evaluate(()=>document.fonts.ready);
  await p.screenshot({path:path.join(out,`${w*d}x${h*d}.png`)});await c.close();}
await b.close()})();
// después: reducir a 256 colores (python3 tools-carga/reducir.py) para que pesen ~250 KB c/u
