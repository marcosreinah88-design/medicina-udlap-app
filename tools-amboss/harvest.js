// Recorre cada guía (abriendo cada tema) y junta todos los subtemas que ve amboss.js.
// Uso: node tools-amboss/harvest.js > subtemas.tsv   (columnas: guía, tema, subtema, ¿tiene término?, búsqueda)
// Sirve para saber qué falta en terminos.tsv.
const {chromium}=require('playwright');const path=require('path');
const SITE=process.env.SITE||path.join(__dirname,'..','site');
const NAV={
 's3/farmacologia/index.html':'#index button[data-go]',
 's4/apps/cirugia.html':'aside#toc button','s4/apps/farmacologia-ii.html':'nav#nav button.tbtn',
 's4/apps/hematologia.html':'button.topic-card',
 's5/cirugia/index.html':'button.ov','s5/esofago/index.html':'a.tcard','s5/hepatobiliar/index.html':'a.tcard',
 's5/gastro/index.html':'a.row','s5/otorrino/index.html':'button.trow',
};
const PAGES=require('fs').readFileSync(path.join(__dirname,'patch_amboss.py'),'utf8').match(/'([^']+\.html)':'[^']+'/g).map(x=>x.split("'")[1]);
const only=process.argv[2];
(async()=>{const b=await chromium.launch();const rows=new Map();
for(const f of PAGES){ if(only&&!f.includes(only))continue;
  const url='file://'+path.join(SITE,f);let ctx=await b.newContext();let p=await ctx.newPage();
  const grab=async()=>{await p.waitForTimeout(400);const s=await p.evaluate(()=>{window.__amb&&window.__amb.run();return window.__amb?window.__amb.seen:{}});
    const qs=await p.evaluate(()=>[...document.querySelectorAll('.amb-btn')].length);
    for(const k in s)rows.set(f+'|'+k,[f,s[k][1],s[k][0],s[k][2]]);return qs};
  await p.goto(url,{waitUntil:'load'});await p.waitForTimeout(700);let nb=await grab();
  const sel=NAV[f];
  if(sel){const n=await p.$$eval(sel,e=>e.length);
    for(let i=0;i<n;i++){await ctx.close();ctx=await b.newContext();p=await ctx.newPage();await p.goto(url,{waitUntil:'load'});await p.waitForTimeout(500);const els=await p.$$(sel);if(!els[i])continue;
      try{await els[i].click({timeout:3000})}catch(e){await els[i].evaluate(x=>x.click())}
      await p.waitForTimeout(600);nb+=await grab()}}
  console.error(f,'botones vistos',nb);await ctx.close()}
for(const r of rows.values())console.log(r.map(x=>String(x).replace(/\s+/g,' ').trim()).join('\t'));
await b.close()})();
