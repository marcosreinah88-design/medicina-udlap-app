// Búsqueda avanzada del buscador de la portada: arma site/buscador-apartados.json
// Recorre cada guía en Chromium (abriendo cada tema, como tools-amboss/harvest.js) y junta qué palabras
// aparecen dentro de cada tipo de apartado (Fisiopatología, Epidemiología, Tratamiento, Posología…),
// con el tema/subtema donde salen. La portada lo carga solo cuando se usa el filtro «Apartado».
// Uso: node tools-buscador/apartados.js            (escribe site/buscador-apartados.json)
//      SITE=<carpeta> node tools-buscador/apartados.js   (para otra copia del sitio)
// Correrlo otra vez al agregar o cambiar una guía (después de tools-s12/build.py y patch_amboss.py).
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const SITE=process.env.SITE||path.join(__dirname,'..','site');
const ROOT=path.join(__dirname,'..');
/* páginas → id de la guía en G (mismo orden que guideFile() del hub) */
const PAGES={
 's1/guias/histologia.html':'histologia','s1/guias/bioquimica.html':'bioquimica','s1/guias/anatomofisiologia.html':'anatomofisiologia',
 's1/guias/embriologia-genetica.html':'embriologia-genetica','s1/guias/simulacion-i.html':'simulacion-i',
 's2/guias/fisiologia.html':'fisiologia','s2/guias/biologia-celular.html':'biologia-celular','s2/guias/anatomia-humana-i.html':'anatomia-humana-i','s2/guias/simulacion-ii.html':'simulacion-ii',
 's3/farmacologia/index.html':'farmacologia','s3/anatomia/index.html':'anatomia',
 's3/fisiologia-clinica/index.html':'fisiologia-clinica','s3/microbiologia/index.html':'microbiologia','s3/simulacion-iii/index.html':'simulacion-iii','s3/propedeutica/index.html':'propedeutica',
 's4/apps/hematologia.html':'hematologia','s4/apps/farmacologia-ii.html':'farmacologia-ii','s4/apps/inmunologia.html':'inmunologia',
 's4/apps/simulacion-iv.html':'simulacion-iv','s4/apps/nutricion.html':'nutricion','s4/apps/cirugia.html':'cirugia-principios',
 's5/cirugia/index.html':'cirugia','s5/gastro/index.html':'gastro','s5/imagenologia/index.html':'imagenologia','s5/oftalmo/index.html':'oftalmo',
 's5/otorrino/index.html':'otorrino','s5/psiquiatria/index.html':'psiquiatria','s5/esofago/index.html':'esofago','s5/hepatobiliar/index.html':'hepatobiliar',
 's6/artefactos/infectologia.html':'infectologia','s6/artefactos/salud-publica.html':'salud-publica',
};
/* temas que solo se pintan al tocarlos (igual que tools-amboss/harvest.js) */
const NAV={
 's3/farmacologia/index.html':'#index button[data-go]',
 's4/apps/cirugia.html':'aside#toc button','s4/apps/farmacologia-ii.html':'nav#nav button.tbtn',
 's4/apps/hematologia.html':'button.topic-card',
 's5/cirugia/index.html':'button.ov','s5/esofago/index.html':'a.tcard','s5/hepatobiliar/index.html':'a.tcard',
 's5/gastro/index.html':'a.row','s5/otorrino/index.html':'button.trow',
};
/* guías que por sí mismas son de un apartado (todo su contenido cuenta) */
const WHOLE={fisiologia:['fisiologia'],anatomofisiologia:['anatomia','fisiologia'],'anatomia-humana-i':['anatomia'],anatomia:['anatomia'],
 farmacologia:['farmacologia'],'farmacologia-ii':['farmacologia']};
const CATS=require('./apartados-cats.json');

/* se corre dentro de la página: devuelve [[apartado, tema › subtema, texto], …] */
function inPage({CATS,amb}){
  const RX=CATS.map(c=>[c.id,new RegExp('^\\s*(?:[\\dIVX]+[.)\\-:]\\s*)?(?:'+c.rx+')','i')]);
  const fold=s=>String(s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
  const own=e=>(e.textContent||'').replace(/\s+/g,' ').trim();
  const catOf=t=>{if(!t||t.length>48)return null;const f=fold(t);for(const [id,r] of RX)if(r.test(f))return id;return null};
  const SKIP='script,style,svg,noscript,template,.amb-w,button.amb-btn,[aria-hidden=true]';
  /* etiqueta = título corto con forma de título (h1–h6, summary, dt, th, negritas o mayúsculas) que empieza con un apartado */
  const LTAG=/^(H[1-6]|SUMMARY|DT|TH|B|STRONG|LABEL|LEGEND|CAPTION)$/;
  const looks=e=>{if(LTAG.test(e.tagName))return true;if(/^(LI|TD|P|A|BUTTON|OPTION)$/.test(e.tagName))return false;
    const cs=getComputedStyle(e);return +cs.fontWeight>=600||cs.textTransform==='uppercase'||cs.fontVariantCaps==='small-caps'};
  const labels=new Map();
  for(const e of document.body.querySelectorAll('*')){
    if(e.closest(SKIP)||e.closest('button,a,[role=tab],nav,option,select'))continue;const t=own(e);const c=catOf(t);if(!c)continue;
    if([...e.children].some(k=>own(k)===t))continue; /* que lo tome el hijo más chico… */
    let L=e;while(L.parentElement&&L.parentElement!==document.body&&own(L.parentElement)===t)L=L.parentElement; /* …y luego el envoltorio */
    if(![e,L].some(looks)&&!/:\s*$/.test(t))continue;
    labels.set(L,c);
  }
  const LV=e=>{const m=/^H([1-6])$/.exec(e.tagName);if(m)return +m[1];const h=e.querySelector('h1,h2,h3,h4,h5,h6');return h?+h.tagName[1]:7};
  const HEADS='h1,h2,h3,h4,h5,h6,summary,dt';
  const LK=[...labels.keys()];
  /* el apartado termina en el siguiente título del mismo nivel o más alto, o en otra etiqueta */
  const isStop=(n,L,lv)=>{if(n.nodeType!==1)return false;if(labels.has(n)||LK.some(x=>x!==L&&n.contains(x)))return true;
    if(L.tagName===n.tagName&&L.className===n.className&&own(n).length<=48)return true;
    const hs=n.matches(HEADS)?[n]:[...n.querySelectorAll(HEADS)];return hs.some(h=>LV(h)<=lv)};
  const out=[];
  /* tema y subtema donde está algo (con la configuración de amboss.js) */
  const subs=amb&&amb.h?[...document.querySelectorAll(amb.h)]:[];
  const txt=(el,tsel)=>{const x=tsel&&el.querySelector(tsel);return own(x||el).replace(/^\s*(clase|tema)?\s*\d+(\.\d+)*\s*[·.\-:)]?\s*/i,'').slice(0,90)};
  const where=n=>{
    let sub='',tema='';
    for(let i=subs.length-1;i>=0;i--){if(subs[i]===n||subs[i].compareDocumentPosition(n)&Node.DOCUMENT_POSITION_FOLLOWING){sub=txt(subs[i],amb.t);break}}
    for(const [box,ts] of (amb&&amb.c)||[]){const b=n.closest(box);if(b){const t=b.querySelector(ts);if(t){tema=txt(t);break}}}
    if(!tema&&!(amb&&amb.c)){const t=document.querySelector('h1');tema=t?txt(t):''}
    return sub&&sub!==tema?tema+' › '+sub:(tema||sub)};
  const textOf=n=>{if(n.nodeType===3)return n.nodeValue;if(n.nodeType!==1||n.matches(SKIP))return '';const c=n.cloneNode(true);c.querySelectorAll(SKIP).forEach(x=>x.remove());return c.textContent};
  for(const [L0,c] of labels){
    let L=L0,parts=[];
    if(L.tagName==='SUMMARY'){parts.push(textOf(L.parentElement))}
    else if(L.tagName==='TH'){
      const tr=L.parentElement,tb=L.closest('table');const allTh=[...tr.children].every(x=>x.tagName==='TH');
      if(allTh&&tb){const i=[...tr.children].indexOf(L);for(const r of tb.querySelectorAll('tr'))if(r!==tr&&r.children[i])parts.push(textOf(r.children[i]))}
      else parts.push(textOf(tr))}
    else if(L.tagName==='DT'){let n=L.nextElementSibling;while(n&&n.tagName!=='DT'){parts.push(textOf(n));n=n.nextElementSibling}}
    else{
      /* si la etiqueta va sola en su caja, subir hasta que tenga hermanos */
      const lv=LV(L0)<7?LV(L0):LV(L)<7?LV(L):7;
      while(!L.nextSibling&&L.parentElement&&L.parentElement!==document.body&&own(L.parentElement).length<=48)L=L.parentElement;
      let n=L.nextSibling;
      while(n){if(isStop(n,L,lv))break;parts.push(textOf(n));n=n.nextSibling}
    }
    const t=parts.join(' ').replace(/\s+/g,' ').trim();if(t.length>2)out.push([c,where(L0),t]);
  }
  /* dosis escritas en cualquier lado (mg/kg, mg cada 8 h, UI/día…) cuentan como Posología */
  const DOSE=/\b\d+(?:[.,]\d+)?\s*(?:-\s*\d+(?:[.,]\d+)?\s*)?(?:mg|mcg|µg|μg|g|gr|ui|u|meq|mmol|ml)\s*(?:\/\s*(?:kg|m2|m²|d[ií]a|h|min|dosis)|c\/|cada\s+\d|al\s+d[ií]a|v\.?o|i\.?v|i\.?m|s\.?c|vo\b|iv\b|im\b)/i;
  for(const e of document.body.querySelectorAll('li,p,td,dd,tr')){
    if(e.closest(SKIP))continue;if(e.tagName!=='TR'&&e.querySelector('li,p,td,dd'))continue;
    const t=own(e);if(t.length<400&&DOSE.test(t))out.push(['posologia',where(e),t]);
  }
  return out;
}

const STOP=new Set('para por con sin del las los una uno unos unas que como mas mas pero sus son esta este estos estas entre sobre hasta desde cuando donde porque puede pueden tiene tienen hay ser muy tambien otra otro otros otras cada todo toda todos todas'.split(' '));
const fold=s=>String(s).normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
const words=t=>fold(t).split(/[^a-z0-9ñ]+/).filter(w=>w.length>=3&&!STOP.has(w)&&!/^\d+$/.test(w)&&!/^[0-9a-f]{5,}$/.test(w));

(async()=>{
  const b=await chromium.launch();
  const ambSrc=fs.readFileSync(path.join(ROOT,'tools-amboss','amboss.src.js'),'utf8');
  const S12={h:"details.sub>summary",t:"h3",c:[["article.tema",".thead h2"]]};
  const CFG=eval('('+ambSrc.slice(ambSrc.indexOf('var CFG=')+8,ambSrc.indexOf('};',ambSrc.indexOf('var CFG='))+1)+')');
  const AMBG=Object.fromEntries((fs.readFileSync(path.join(ROOT,'tools-amboss','patch_amboss.py'),'utf8').match(/'([^']+\.html)':'[^']+'/g)||[]).map(x=>{const p=x.split("'");return [p[1],p[3]]}));
  const res={};
  const ONLY=process.env.ONLY;const prev=ONLY&&fs.existsSync(path.join(SITE,'buscador-apartados.json'))?JSON.parse(fs.readFileSync(path.join(SITE,'buscador-apartados.json'),'utf8')).g:{};
  Object.assign(res,prev);
  for(const [f,gid] of Object.entries(PAGES)){
    if(ONLY&&!ONLY.split(',').includes(gid))continue;
    const key=AMBG[f]||'';const amb=/^s[12]-/.test(key)?S12:CFG[key]||null;
    const url='file://'+path.join(SITE,f);
    const recs=[];
    const grab=async p=>{await p.waitForTimeout(350);recs.push(...await p.evaluate(inPage,{CATS:CATS.map(c=>({id:c.id,rx:c.rx})),amb}))};
    let ctx=await b.newContext();let p=await ctx.newPage();
    await p.goto(url,{waitUntil:'load'});await p.waitForTimeout(700);await grab(p);
    const sel=NAV[f];
    if(sel){const n=await p.$$eval(sel,e=>e.length);
      for(let i=0;i<n;i++){await ctx.close();ctx=await b.newContext();p=await ctx.newPage();await p.goto(url,{waitUntil:'load'});await p.waitForTimeout(450);
        const els=await p.$$(sel);if(!els[i])continue;
        try{await els[i].click({timeout:3000})}catch(e){await els[i].evaluate(x=>x.click())}
        await p.waitForTimeout(550);await grab(p)}}
    await ctx.close();
    if(process.env.DEBUG)fs.writeFileSync(path.join(require('os').tmpdir(),'apartados-'+gid+'.json'),JSON.stringify(recs,null,1));
    /* apartado → lugar → palabras */
    const m={};
    for(const [c,w,t] of recs){(m[c]=m[c]||{});const s=(m[c][w]=m[c][w]||new Set());for(const x of words(t))s.add(x)}
    const o={};for(const c of Object.keys(m).sort()){o[c]=Object.entries(m[c]).filter(([w,s])=>s.size).map(([w,s])=>[w,[...s].sort().join(' ')])}
    if(WHOLE[gid])o.$=WHOLE[gid];
    res[gid]=o;
    console.error(gid.padEnd(20),Object.entries(o).filter(([k])=>k!=='$').map(([k,v])=>k+':'+v.length).join(' '));
  }
  await b.close();
  const out={v:1,cats:CATS.map(c=>[c.id,c.label]),g:res};
  fs.writeFileSync(path.join(SITE,'buscador-apartados.json'),JSON.stringify(out));
  console.error('buscador-apartados.json',(fs.statSync(path.join(SITE,'buscador-apartados.json')).size/1024).toFixed(0),'KB');
})();
