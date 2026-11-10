// Saca tarjetas y preguntas de opción múltiple de las guías (formatos distintos en cada una).
const fs=require('fs'),vm=require('vm'),path=require('path');
function literals(src){
  const out=[];
  for(let i=0;i<src.length;i++){
    const c0=src[i];if(c0!=='['&&c0!=='{')continue;
    if(c0==='['&&!/^\[\s*[\[\{"]/.test(src.slice(i,i+6)))continue;
    if(c0==='{'&&!/^\{\s*"?[a-zA-Z_]+"?\s*:/.test(src.slice(i,i+30)))continue;
    let d=0,j=i,q=null;
    for(;j<src.length;j++){const c=src[j];
      if(q){if(c==='\\'){j++;continue}if(c===q)q=null;continue}
      if(c==='"'||c==="'"||c==='`'){q=c;continue}
      if(c==='['||c==='{'||c==='(')d++;else if(c===']'||c==='}'||c===')'){d--;if(d===0)break}}
    const txt=src.slice(i,j+1);
    if(txt.length>300&&!/=>|function|\$\{/.test(txt.slice(0,2000))){try{const v=vm.runInNewContext('('+txt+')',{},{timeout:300});if(v&&typeof v==='object'){out.push(v);i=j}}catch(e){}}
  }
  return out;
}
const strip=s=>String(s).replace(/<[^>]+>/g,'').replace(/&nbsp;/g,' ').replace(/&gt;/g,'>').replace(/&lt;/g,'<').replace(/&amp;/g,'&').replace(/&quot;/g,'"').replace(/\s+/g,' ').trim();
const S=v=>typeof v==='string'&&strip(v).length>1;
let IDS={};
function ids(v,d=0){if(d>6||!v||typeof v!=='object')return;if(Array.isArray(v)){v.forEach(x=>ids(x,d+1));return}
  const n=[v.title,v.t,v.name,v.n].find(x=>typeof x==='string'&&x.length>2&&x.length<90);if(typeof v.id==='string'&&n&&!IDS[v.id])IDS[v.id]=strip(n);for(const k in v)ids(v[k],d+1)}
function walk(v,ctx,res,depth=0){
  if(depth>8||!v||typeof v!=='object')return;
  if(Array.isArray(v)){
    // tarjetas como pares [frente, reverso]
    if(v.length>=6&&v.every(x=>Array.isArray(x)&&x.length===3&&/^[a-z0-9_-]{1,20}$/i.test(x[0])&&S(x[1])&&S(x[2]))){v.forEach(x=>res.c.push({t:IDS[x[0]]||ctx.t,f:strip(x[1]),b:strip(x[2])}));return}
    if(v.length>=6&&v.every(x=>Array.isArray(x)&&x.length>=2&&x.length<=3&&S(x[0])&&S(x[1])&&strip(x[0]).length<400)){v.forEach(x=>res.c.push({t:ctx.t,f:strip(x[0]),b:strip(x[1])}));return}
    // preguntas como [tema, texto, [opciones], idx, explicación]
    if(v.length>=4&&v.every(x=>Array.isArray(x)&&typeof x[0]==='string'&&x[0].length<25&&S(x[1])&&Array.isArray(x[2])&&typeof x[3]==='number')){v.forEach(x=>res.q.push({t:IDS[x[0]]||ctx.t,q:strip(x[1]),o:x[2].map(strip),a:x[3],e:x[4]?strip(x[4]):''}));return}
    // preguntas como [texto, [opciones], idx, explicación]
    if(v.length>=4&&v.every(x=>Array.isArray(x)&&S(x[0])&&Array.isArray(x[1])&&typeof x[2]==='number')){v.forEach(x=>res.q.push({t:ctx.t,q:strip(x[0]),o:x[1].map(strip),a:x[2],e:x[3]?strip(x[3]):''}));return}
    v.forEach(x=>walk(x,ctx,res,depth+1));return;
  }
  const o=v,t=typeof o.title==='string'?o.title:typeof o.t==='string'&&o.t.length>2&&o.t.length<80&&!o.q?o.t:ctx.t;
  const c2={t};
  const qt=['q','s','p','pregunta','question','stem'].find(k=>S(o[k]));
  const ot=['o','opts','opciones','options'].find(k=>Array.isArray(o[k])&&o[k].length>=2);
  if(qt&&ot){
    const opts=o[ot];let a=['a','r','c','ans','answer','correct','ok'].map(k=>o[k]).find(x=>typeof x==='number');
    let list=null,e=['e','w','why','exp','x','r'].map(k=>o[k]).find(x=>typeof x==='string')||'';
    if(opts.every(S)&&typeof a==='number'&&a>=0&&a<opts.length)list=opts.map(strip);
    else if(opts.every(x=>Array.isArray(x)&&S(x[0])&&(typeof x[1]==='number'||typeof x[1]==='boolean'))){list=opts.map(x=>strip(x[0]));a=opts.findIndex(x=>x[1]===1||x[1]===true);const w=opts[a];if(w&&S(w[2]))e=w[2]}
    if(list&&a>=0&&list.every(x=>x.length<300)){res.q.push({t:o.t&&o.t.length<80?ctx.t:t,q:strip(o[qt]),o:list,a,e:strip(e)});return}
  }
  // anatomía: {t, q:[texto, opciones, idx, exp]}
  if(Array.isArray(o.q)&&S(o.q[0])&&Array.isArray(o.q[1])&&typeof o.q[2]==='number'){res.q.push({t:ctx.t,q:strip(o.q[0]),o:o.q[1].map(strip),a:o.q[2],e:o.q[3]?strip(o.q[3]):''});return}
  const pairs=[['f','b'],['front','back'],['frente','reverso'],['q','a'],['p','r'],['k','v'],['term','def']];
  for(const [x,y] of pairs)if(S(o[x])&&S(o[y])&&Object.keys(o).length<=5&&strip(o[x]).length<400){res.c.push({t,f:strip(o[x]),b:strip(o[y])});return}
  for(const k in o)walk(o[k],c2,res,depth+1);
}
module.exports=function(file){
  const html=fs.readFileSync(file,'utf8');
  const scripts=[...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]).join('\n;\n');
  const res={q:[],c:[]};
  const lits=literals(scripts);IDS={};lits.forEach(v=>ids(v));for(const v of lits)walk(v,{t:''},res);
  // quiz de pruebas hepáticas: la primera opción es la correcta (la guía las revuelve) y "t" es la letra de la sección
  if(/const PREGUNTAS\s*=/.test(scripts)){const secs={};for(const x of scripts.matchAll(/\b([A-Z]):\s*"([^"]{3,80})"/g))secs[x[1]]=x[2];
    const i=scripts.indexOf('[',scripts.search(/const PREGUNTAS\s*=/));const arr=literals(scripts.slice(i))[0]||[];
    for(const o of arr)if(o&&S(o.q)&&Array.isArray(o.o))res.q.push({t:secs[o.t]||'',q:strip(o.q),o:o.o.map(strip),a:0,e:strip(o.e||'')});}
  const seen=new Set();for(const k of ['q','c'])res[k]=res[k].filter(x=>{const h=(x.q||x.f)+'|'+(x.b||x.o.join());if(seen.has(h))return false;seen.add(h);return true});
  return res;
};
if(require.main===module){const r=module.exports(process.argv[2]);console.log('preguntas',r.q.length,'tarjetas',r.c.length);console.log(JSON.stringify(r.q[0]));console.log(JSON.stringify(r.c[0]));console.log(JSON.stringify(r.c[Math.floor(r.c.length/2)]))}
