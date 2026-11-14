/* Medicina UDLAP · SRS: el mismo programador estilo Anki para las tarjetas de las guías, las páginas de materia,
   el mazo AnKing y la sección Estudio. Incluye la pantalla de repaso (como Anki), el historial y las Estadísticas.
   Todo se guarda en este aparato (localStorage) y sync.js lo copia cifrado a tus otros aparatos. Nada va al repo.
   Datos:
   - carrera-anki-<mazo>  {v:2,c:{clave:estado},lim,rlim,N,name}   estado de cada tarjeta de un mazo de Anki
   - carrera-repaso       {items:[{id,...estado}]}                  tarjetas de tus guías y las tuyas (Estudio)
   - carrera-srs-log      {items:[{id,r:[t,mazo,botón,tipo,ivl,ivlAnt,facilidad,ms,nueva]}]}  últimos 5000 repasos
   - carrera-srs-dias     {v:1,d:{"aaaa-mm-dd":{mazo:[apr,joven,madura,reapr,ms,jOk,jMal,mOk,mMal,nuevas]}},n:{mazo:nombre}}
   estado: q 0 aprendiendo · 1 repaso · 2 reaprendiendo | s paso | e facilidad % | i intervalo (días) | n repasos | l olvidos
           d cuándo toca (ms) | u último repaso (ms) | sp suspendida | bu enterrada (día) | nw sigue siendo nueva */
(function(){
  if(window.SRS)return;
  const DAY=864e5,MIN=6e4,LS=[1,10],RS=[10],GRAD=1,EASY=4,MAXI=36500,AHEAD=20*MIN,LOGMAX=5000;
  const J=(k,d)=>{try{const v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}};
  const S=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v));return true}catch(e){return false}};
  const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const pad=n=>String(n).padStart(2,"0");
  const dayStart=t=>{const d=new Date(t-4*36e5);d.setHours(4,0,0,0);return d.getTime()};/* el día cambia a las 4 a. m., como en Anki */
  const ymd=d=>d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate());
  const dayKey=t=>ymd(new Date(dayStart(t)));
  const keyMs=k=>{const [y,m,d]=k.split("-").map(Number);return new Date(y,m-1,d,4).getTime()};
  const hash=s=>{let h=5381;for(let i=0;i<s.length;i++)h=(h*33^s.charCodeAt(i))>>>0;return h.toString(36)};
  const isNew=p=>!p||p.nw;
  const dark=()=>{const t=document.documentElement.dataset.theme||document.body&&document.body.dataset.theme;
    if(t)return t==="dark";try{return matchMedia("(prefers-color-scheme: dark)").matches}catch(e){return false}};

  /* ===== programador (SM-2 de Anki: pasos 1 y 10 min, se gradúa a 1 día, Fácil 4 días, facilidad 250 %) ===== */
  function sched(p,g,now){
    const c=p&&!p.nw?Object.assign({},p):{q:0,s:0,e:250,i:0,n:0,l:0,d:now};let m=0;
    delete c.bu;
    if(c.q!==1){
      const st=c.q===2?RS:LS;let grad=0;c.s=c.s||0;
      if(g===0){c.s=0;m=st[0]}
      else if(g===1)m=c.s===0?(st.length>1?Math.round((st[0]+st[1])/2):Math.min(Math.round(st[0]*1.5),st[0]+1440)):st[c.s];
      else if(g===2){if(c.s+1<st.length){c.s++;m=st[c.s]}else grad=c.q===2?Math.max(1,c.i):GRAD}
      else grad=c.q===2?Math.max(1,c.i)+1:EASY;
      if(grad){c.q=1;c.s=0;c.i=grad}
    }else{
      const late=Math.max(0,Math.floor((dayStart(now)-c.d)/DAY)),h=Math.max(c.i+1,Math.round(c.i*1.2)),
        gd=Math.max(h+1,Math.round((c.i+late/2)*c.e/100)),ez=Math.max(gd+1,Math.round((c.i+late)*c.e/100*1.3));
      if(g===0){c.l=(c.l||0)+1;c.e=Math.max(130,c.e-20);c.i=1;c.q=2;c.s=0;m=RS[0]}
      else if(g===1){c.i=h;c.e=Math.max(130,c.e-15)}
      else if(g===2)c.i=gd;
      else{c.i=ez;c.e+=15}
    }
    c.i=Math.min(c.i,MAXI);c.n=(c.n||0)+1;c.d=m?now+m*MIN:dayStart(now)+c.i*DAY;c.u=now;c.m=m;return c;
  }
  function answer(p,g,now){/* como sched, más el "fuzz" de Anki para que no se amontonen el mismo día */
    const n=sched(p,g,now);
    if(!n.m&&n.i>=3){const f=Math.max(1,Math.round(n.i*.05));n.i=Math.min(MAXI,n.i+Math.round((Math.random()*2-1)*f));n.d=dayStart(now)+n.i*DAY}
    return n;
  }
  const ivTxt=c=>{if(c.m)return c.m<60?"<"+c.m+" min":Math.round(c.m/60)+" h";
    const i=c.i,f=x=>String(Math.round(x*10)/10).replace(".",",");return i<30?i+" d":i<365?f(i/30)+" m":f(i/365)+" a"};

  /* ===== dónde se guarda cada tarjeta ===== */
  const stores=new Map();
  function deckStore(M){
    if(stores.has("a:"+M))return stores.get("a:"+M);
    const KEY="carrera-anki-"+M;let P;
    const load=()=>{P=J(KEY,null);
      if(Array.isArray(P)){/* versión 1: lista de "ya me la sé" → repaso a 4 días */
        const now=Date.now(),c={};P.forEach(h=>c[h]={q:1,s:0,e:250,i:4,n:1,l:0,d:dayStart(now)+4*DAY});P={v:2,c};S(KEY,P)}
      if(!P||typeof P!=="object"||!P.c)P={v:2,c:{}};return P};
    load();
    const st={id:M,KEY,get:k=>P.c[k],meta:()=>P,reload:load,all:()=>P.c,
      put(k,s){load();if(s)P.c[k]=s;else delete P.c[k];S(KEY,P)},
      set(o){load();Object.assign(P,o);S(KEY,P)}};
    stores.set("a:"+M,st);return st;
  }
  function repasoStore(){
    if(stores.has("r"))return stores.get("r");
    const KEY="carrera-repaso";let M;
    const conv=x=>{if(typeof x.d!=="string")return x;/* formato viejo de Estudio (fechas aaaa-mm-dd) */
      const y=Object.assign({},x),q=x.st!==undefined?x.st:(x.n>0?1:0);y.q=q;y.d=keyMs(x.d);y.s=x.s||0;y.e=x.e||250;delete y.st;return y};
    const load=()=>{const v=J(KEY,null);M=new Map();(v&&Array.isArray(v.items)?v.items:[]).forEach(x=>x&&x.id!=null&&M.set(x.id,conv(x)));return M};
    load();
    const st={id:"repaso",KEY,get:k=>M.get(k),reload:load,
      put(k,s){load();if(s)M.set(k,Object.assign({},s,{id:k}));else M.delete(k);const v=J(KEY,{})||{};v.items=[...M.values()];S(KEY,v)}};
    stores.set("r",st);return st;
  }
  const reloadAll=()=>stores.forEach(s=>s.reload());

  /* ===== historial ===== */
  const LOGK="carrera-srs-log",DIASK="carrera-srs-dias";
  const dias=()=>{const v=J(DIASK,null);return v&&v.d?v:{v:1,d:{},n:{}}};
  const logItems=()=>{const v=J(LOGK,null);return v&&Array.isArray(v.items)?v.items.filter(x=>x&&Array.isArray(x.r)):[]};
  function record(deck,name,g,prev,next,ms,now){
    const wasNew=isNew(prev),y=wasNew||prev.q===0?0:prev.q===2?2:1,li=wasNew?0:prev.q===1?prev.i:-(prev.q===2?RS[0]:LS[prev.s||0]);
    const it={id:now.toString(36)+Math.random().toString(36).slice(2,5),r:[now,deck,g+1,y,next.m?-next.m:next.i,li,wasNew?250:prev.e,Math.round(ms),wasNew?1:0]};
    const L=logItems();L.push(it);S(LOGK,{items:L.slice(-LOGMAX)});
    const D=dias(),dk=dayKey(now),day=D.d[dk]||(D.d[dk]={}),row=day[deck]||(day[deck]=[0,0,0,0,0,0,0,0,0,0]),before=row.slice();
    if(y===0)row[0]++;else if(y===2)row[3]++;else if(li>=21){row[2]++;row[g>0?7:8]++}else{row[1]++;row[g>0?5:6]++}
    row[4]+=Math.round(ms);if(wasNew)row[9]++;if(name)D.n[deck]=name;S(DIASK,D);
    return {id:it.id,dk,deck,before};
  }
  function unrecord(u){
    S(LOGK,{items:logItems().filter(x=>x.id!==u.id)});
    const D=dias();if(D.d[u.dk]){D.d[u.dk][u.deck]=u.before;S(DIASK,D)}
  }
  function today(ids){/* nuevas y repasos de hoy en esos mazos */
    const d=dias().d[dayKey(Date.now())]||{};let nw=0,rv=0,n=0,ms=0;
    for(const k in d)if(!ids||ids.includes(k)){const r=d[k];nw+=r[9];rv+=r[1]+r[2];n+=r[0]+r[1]+r[2]+r[3];ms+=r[4]}
    return {nw,rv,n,ms};
  }

  /* ===== colas (como Anki: aprendiendo primero, luego repasos con las nuevas intercaladas) ===== */
  function queues(cards,o,now){
    const end=dayStart(now)+DAY,tk=dayKey(now),L=[],La=[],R=[],N=[];let wait=Infinity,sus=0,bur=0;
    for(const c of cards){const p=c.st.get(c.k);
      if(p&&p.sp){sus++;continue}if(p&&p.bu===tk){bur++;continue}
      if(isNew(p))N.push(c);
      else if(p.q!==1){if(p.d<=now)L.push(c);else if(p.d<=now+AHEAD)La.push(c);else if(p.d<end)wait=Math.min(wait,p.d)}
      else if(p.d<end)R.push(c)}
    const g=c=>c.st.get(c.k);
    L.sort((a,b)=>g(a).d-g(b).d);La.sort((a,b)=>g(a).d-g(b).d);
    R.sort((a,b)=>(dayStart(g(a).d)-dayStart(g(b).d))||((o.rnd(a)-o.rnd(b))));
    if(o.shuffleNew)N.sort((a,b)=>o.rnd(a)-o.rnd(b));
    const t=today(o.ids),allN=N.length;
    return {L,La,R:R.slice(0,Math.max(0,o.revLim()-t.rv)),N:N.slice(0,Math.max(0,o.newLim()-t.nw)),allN,allR:R.length,wait,sus,bur,t};
  }

  /* ===== estilos (pantalla tipo Anki) ===== */
  const CSS=`.srs{--s-bg:#fff;--s-bar:#f2f2f2;--s-ink:#111;--s-mute:#6b6b6b;--s-line:#d9d9d9;--s-btn:#fff;--s-btnh:#e8e8e8;
--s-new:#1f6fde;--s-lrn:#c3312a;--s-rev:#1e8a3a;--s-cz:#1a5fd0;--s-acc:#00573c;
font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--s-ink);background:var(--s-bg);text-align:left;
display:flex;flex-direction:column;min-height:420px;border-radius:inherit}
.srs[data-dark]{--s-bg:#2c2c2e;--s-bar:#232325;--s-ink:#ececec;--s-mute:#a5a5a8;--s-line:#47474a;--s-btn:#3a3a3d;--s-btnh:#47474b;
--s-new:#6ea8ff;--s-lrn:#ff7b6b;--s-rev:#5fd07a;--s-cz:#7fb0ff;--s-acc:#4fbf8f}
.srs *{box-sizing:border-box}.srs button{font:inherit;cursor:pointer;color:inherit}
.srs-top{display:flex;align-items:center;gap:6px;padding:8px 12px;background:var(--s-bar);border-bottom:1px solid var(--s-line);font-size:13.5px;flex-wrap:nowrap;min-height:44px}
.srs-top b{font-weight:600;margin-right:auto;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0;flex:1 1 120px}
.srs-tb{border:0;background:none;padding:5px 9px;border-radius:6px;color:var(--s-ink)!important}.srs-tb:hover,.srs-tb[aria-pressed=true]{background:var(--s-btnh)}
.srs-main{flex:1;display:flex;flex-direction:column;overflow:auto;position:relative}
.srs-card{flex:1;padding:28px 20px 30px;text-align:center;font-size:21px;line-height:1.5;max-width:780px;width:100%;margin:0 auto;overflow-wrap:anywhere}
.srs-card hr{border:0;border-top:1px solid var(--s-line);margin:20px 0}
.srs-card .tema{font-size:12px;color:var(--s-mute);letter-spacing:.04em;text-transform:uppercase;margin-bottom:14px}
.srs-card .cz{color:var(--s-cz);font-weight:700}
.srs-bot{position:sticky;bottom:0;background:var(--s-bar);border-top:1px solid var(--s-line);padding:8px 10px 10px;text-align:center}
.srs-cnt{font-variant-numeric:tabular-nums;font-size:14px;margin-bottom:6px;color:var(--s-mute)}
.srs-cnt .n{color:var(--s-new)}.srs-cnt .l{color:var(--s-lrn)}.srs-cnt .r{color:var(--s-rev)}.srs-cnt u{text-underline-offset:3px;text-decoration-thickness:2px}
.srs-b{border:1px solid var(--s-line);background:var(--s-btn);border-radius:6px;padding:8px 22px;min-width:120px;box-shadow:0 1px 0 rgba(0,0,0,.06)}
.srs-b:hover{background:var(--s-btnh)}.srs-b.p{background:var(--s-acc);border-color:var(--s-acc);color:#fff!important}
.srs-ans{display:flex;justify-content:center;gap:8px;flex-wrap:nowrap}
.srs-ans div{display:flex;flex-direction:column;align-items:center;gap:3px;flex:0 1 120px}
.srs-ans small{font-size:12px;color:var(--s-mute);font-variant-numeric:tabular-nums}
.srs-ans .srs-b{min-width:0;width:100%;padding:8px 6px;font-weight:600}
.srs-ans .g0{color:var(--s-lrn)!important}.srs-ans .g2{color:var(--s-rev)!important}.srs-ans .g3{color:var(--s-new)!important}
.srs-k{font-size:11.5px;color:var(--s-mute);margin-top:6px}
.srs-ov{padding:34px 20px;text-align:center;max-width:520px;margin:0 auto;width:100%}
.srs-ov h3{font-size:22px;margin:0 0 18px;font-weight:600}
.srs-ov table{margin:0 auto 20px;border-collapse:collapse;font-size:16px}.srs-ov td{padding:3px 10px;text-align:left}.srs-ov td+td{text-align:right;font-weight:700;font-variant-numeric:tabular-nums}
.srs-ov .n{color:var(--s-new)}.srs-ov .l{color:var(--s-lrn)}.srs-ov .r{color:var(--s-rev)}
.srs-ov p{color:var(--s-mute);font-size:13.5px;margin:14px 0 0}
.srs-opt{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:18px;font-size:13px;color:var(--s-mute)}
.srs-opt select{font:inherit;padding:3px 6px;border:1px solid var(--s-line);border-radius:6px;background:var(--s-btn);color:var(--s-ink)}
.srs-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:14px}
.srs-menu{position:absolute;right:10px;top:6px;z-index:5;background:var(--s-bg);border:1px solid var(--s-line);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.2);padding:4px;display:flex;flex-direction:column;min-width:190px}
.srs-menu button{border:0;background:none;text-align:left;padding:8px 10px;border-radius:6px;display:flex;justify-content:space-between;gap:12px}.srs-menu button:hover{background:var(--s-btnh)}.srs-menu kbd{color:var(--s-mute);font:12px inherit}
.srs-toast{position:absolute;left:50%;top:10px;transform:translateX(-50%);background:var(--s-ink);color:var(--s-bg);padding:6px 12px;border-radius:6px;font-size:13px;z-index:6}
.srs-decks{width:100%;border-collapse:collapse;font-size:14.5px}.srs-decks th{font-weight:600;color:var(--s-mute);font-size:12.5px;text-align:right;padding:6px 10px;border-bottom:1px solid var(--s-line)}
.srs-decks th:first-child,.srs-decks td:first-child{text-align:left}.srs-decks td{padding:7px 10px;text-align:right;border-bottom:1px solid var(--s-line);font-variant-numeric:tabular-nums}
.srs-decks tr[data-deck]{cursor:pointer}.srs-decks tr[data-deck]:hover td{background:var(--s-btnh)}.srs-decks .z{color:var(--s-mute);opacity:.45}
.srs-decks td.n{color:var(--s-new)}.srs-decks td.l{color:var(--s-lrn)}.srs-decks td.r{color:var(--s-rev)}.srs-decks .sem td{font-weight:600;color:var(--s-mute);font-size:12px;text-transform:uppercase;letter-spacing:.04em;background:var(--s-bar);cursor:default}
/* estadísticas */
.srs-st{padding:14px 14px 30px;max-width:900px;margin:0 auto;width:100%}
.srs-st .bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px}
.srs-seg{display:inline-flex;border:1px solid var(--s-line);border-radius:8px;overflow:hidden}.srs-seg button{border:0;background:var(--s-btn);padding:5px 11px;font-size:13px}.srs-seg button[aria-pressed=true]{background:var(--s-acc);color:#fff!important}
.srs-sc{background:var(--s-bg);border:1px solid var(--s-line);border-radius:10px;padding:14px 16px;margin-bottom:12px}
.srs-sc h4{margin:0 0 4px;font-size:16px;text-align:center}.srs-sc .sub{color:var(--s-mute);font-size:12.5px;text-align:center;margin:0 0 10px}
.srs-sc svg{display:block;width:100%;height:auto;overflow:visible}.srs-sc svg text{fill:var(--s-mute);font-size:10px}
.srs-sc .kv{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:4px 16px;font-size:13.5px;margin-top:10px}.srs-sc .kv b{font-variant-numeric:tabular-nums}
.srs-sc table{width:100%;border-collapse:collapse;font-size:13.5px;font-variant-numeric:tabular-nums}.srs-sc th,.srs-sc td{padding:5px 6px;border-bottom:1px solid var(--s-line);text-align:right}.srs-sc th:first-child,.srs-sc td:first-child{text-align:left}.srs-sc th{color:var(--s-mute);font-weight:600;font-size:12px}
.srs-leg{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;font-size:12.5px;margin-top:8px}.srs-leg span{display:inline-flex;align-items:center;gap:5px}.srs-leg i{width:10px;height:10px;border-radius:3px;display:inline-block}
.srs-today{font-size:15px;text-align:center;line-height:1.7}
.srs-tip{position:fixed;z-index:2147483646;pointer-events:none;background:#111;color:#fff;font:12.5px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;padding:6px 9px;border-radius:6px;max-width:240px;box-shadow:0 4px 14px rgba(0,0,0,.25)}
.srs [data-tip]:hover{opacity:.8}
@media (max-width:560px){.srs-top .tx{display:none}.srs-top{padding:6px 6px;font-size:13px}.srs-card{font-size:19px;padding:22px 14px}.srs-ans{gap:5px}.srs-ans .srs-b{font-size:14px;padding:9px 2px}.srs-k{display:none}}`;
  function css(){if(document.getElementById("srs-css"))return;const s=document.createElement("style");s.id="srs-css";s.textContent=CSS;document.head.appendChild(s)}
  let tipEl=null;
  function tips(root){
    root.addEventListener("pointermove",e=>{const t=e.target.closest&&e.target.closest("[data-tip]");
      if(!t){if(tipEl)tipEl.hidden=true;return}
      if(!tipEl){tipEl=document.createElement("div");tipEl.className="srs-tip";document.body.appendChild(tipEl)}
      tipEl.hidden=false;tipEl.innerHTML=t.dataset.tip;const w=tipEl.offsetWidth,h=tipEl.offsetHeight;
      tipEl.style.left=Math.max(4,Math.min(innerWidth-w-4,e.clientX-w/2))+"px";tipEl.style.top=Math.max(4,e.clientY-h-12)+"px"});
    root.addEventListener("pointerleave",()=>{if(tipEl)tipEl.hidden=true});
  }

  /* ===== texto de la tarjeta (negritas, renglones y huecos tipo cloze) ===== */
  const fmt=s=>esc(s).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").split(" · ").join("<br>");
  const CZ=/\[(?:…|\.\.\.|[^\]\n]{1,40})\]/;
  const isCloze=c=>CZ.test(c.f)&&/\*\*/.test(c.b);
  const front=c=>isCloze(c)?esc(c.f).replace(/\[(…|\.\.\.|[^\]\n]{1,40})\]/g,'<span class="cz">[$1]</span>').split(" · ").join("<br>"):fmt(c.f);
  const back=c=>isCloze(c)?esc(c.b).replace(/\*\*(.+?)\*\*/g,'<span class="cz">$1</span>').split(" · ").join("<br>"):fmt(c.f)+'<hr id="answer">'+fmt(c.b);

  /* ===== pantalla de repaso =====
     o: {title, cards:()=>[{k,st,f,b,t,deck,dn}], ids:[mazos] o null, newLim(), revLim(), setLim({lim,rlim}), onStats(), onBack(), back:"Mazos"} */
  function reviewer(host,o){
    css();const root=document.createElement("div");root.className="srs";if(o.dark!=null?o.dark:dark())root.dataset.dark="";
    host.appendChild(root);tips(root);
    const ord=new Map();o.rnd=c=>{const k=c.st.id+c.k;if(!ord.has(k))ord.set(k,Math.random());return ord.get(k)};
    let scr=o.start||"ov",cur=null,curQ="",show=false,undo=[],cnt=0,shown=0,menu=false,toastT=0,timer=0,Q=null,extraNew=0;
    const newLim=()=>o.newLim()+extraNew;
    const qo={ids:o.ids,newLim,revLim:o.revLim,rnd:o.rnd,shuffleNew:o.shuffleNew};
    function pick(){
      const now=Date.now();Q=queues(o.cards(),qo,now);show=false;menu=false;
      if(Q.L.length){cur=Q.L[0];curQ="l"}
      else if(Q.R.length&&Q.N.length){const k=Math.max(2,Math.round(Q.R.length/Q.N.length)+1);cnt++;if(cnt%k===0){cur=Q.N[0];curQ="n"}else{cur=Q.R[0];curQ="r"}}
      else if(Q.R.length){cur=Q.R[0];curQ="r"}else if(Q.N.length){cur=Q.N[0];curQ="n"}
      else if(Q.La.length){cur=Q.La[0];curQ="l"}else{cur=null;curQ=""}
      shown=Date.now();
    }
    const counts=()=>({n:Q.N.length,l:Q.L.length+Q.La.length,r:Q.R.length});
    function toast(t){clearTimeout(toastT);const el=document.createElement("div");el.className="srs-toast";el.textContent=t;
      const m=root.querySelector(".srs-main");if(m){m.querySelectorAll(".srs-toast").forEach(x=>x.remove());m.appendChild(el)}toastT=setTimeout(()=>el.remove(),1600)}
    function grade(g){
      if(!cur||!show)return;const c=cur,prev=c.st.get(c.k),now=Date.now();
      const n=answer(prev,g,now),m=n.m;delete n.m;
      const rec=record(c.deck,c.dn,g,prev,Object.assign({m},n),Math.min(6e4,now-shown),now);
      c.st.put(c.k,n);undo.push({c,prev,rec,show:true});if(undo.length>30)undo.shift();
      pick();draw();
    }
    function act(a){
      if(!cur)return;const c=cur,prev=c.st.get(c.k),tk=dayKey(Date.now());
      const n=Object.assign({},prev||{nw:1});if(a==="bury")n.bu=tk;else n.sp=1;
      c.st.put(c.k,n);undo.push({c,prev,rec:null});pick();draw();toast(a==="bury"?"Tarjeta enterrada hasta mañana":"Tarjeta suspendida");
    }
    function doUndo(){const u=undo.pop();if(!u)return;u.c.st.put(u.c.k,u.prev||null);if(u.rec)unrecord(u.rec);
      Q=queues(o.cards(),qo,Date.now());cur=u.c;curQ=isNew(u.prev)?"n":u.prev.q===1?"r":"l";show=!!u.show;shown=Date.now();menu=false;scr="rv";draw();toast("Se deshizo")}
    function top(){
      return `<div class="srs-top">${scr!=="ov"||o.onBack?`<button class="srs-tb" data-a="back" title="Volver">‹ ${esc(scr==="ov"?o.back||"Mazos":"Resumen")}</button>`:""}<b>${esc(o.title())}</b>
        ${o.onStats?`<button class="srs-tb" data-a="stats">Estadísticas</button>`:""}
        ${scr==="rv"?`<button class="srs-tb" data-a="undo" ${undo.length?"":"disabled style=opacity:.4"} title="Deshacer (Z)">↶<span class="tx"> Deshacer</span></button><button class="srs-tb" data-a="menu" aria-label="Más" title="Más">⋯</button>`:""}</div>`;
    }
    function draw(){
      clearTimeout(timer);
      if(!Q)pick();
      if(scr==="rv"&&!cur)scr="done";
      let h=top()+`<div class="srs-main">`;
      if(scr==="ov"){
        const k=counts(),t=Q.t;
        h+=`<div class="srs-ov"><h3>${esc(o.title())}</h3><table><tr><td>Nuevas:</td><td class="n">${k.n}</td></tr><tr><td>Aprendiendo:</td><td class="l">${k.l}</td></tr><tr><td>Por repasar:</td><td class="r">${k.r}</td></tr></table>
          <button class="srs-b p" data-a="study" ${k.n+k.l+k.r?"":"disabled"}>Estudiar ahora</button>
          <p>${t.n?`Hoy estudiaste ${t.n} tarjeta${t.n===1?"":"s"} en ${Math.max(1,Math.round(t.ms/MIN))} min.`:"Hoy aún no estudias este mazo."}${Q.allN>k.n?` Quedan ${Q.allN.toLocaleString("es-MX")} nuevas sin ver.`:""}</p>
          <div class="srs-opt"><label>Nuevas por día <select data-k="lim">${[0,5,10,20,30,50,100,9999].map(v=>`<option value="${v}"${v===o.newLim()?" selected":""}>${v===9999?"sin límite":v}</option>`).join("")}</select></label>
          <label>Repasos máx. por día <select data-k="rlim">${[50,100,200,500,9999].map(v=>`<option value="${v}"${v===o.revLim()?" selected":""}>${v===9999?"sin límite":v}</option>`).join("")}</select></label></div>
          ${Q.sus?`<div class="srs-row"><button class="srs-tb" data-a="unsus">Reactivar ${Q.sus} suspendida${Q.sus===1?"":"s"}</button></div>`:""}</div>`;
      }else if(scr==="done"){
        const w=Q.wait<Infinity?Q.wait-Date.now():0;
        if(w>0&&w<36e5)timer=setTimeout(()=>{pick();if(cur)scr="rv";draw()},w+500);
        h+=`<div class="srs-ov"><h3>¡Enhorabuena! Terminaste este mazo por ahora.</h3>
          <p style="font-size:15px">${w>0?`Las que estás aprendiendo regresan en ${w<36e5?Math.max(1,Math.round(w/MIN))+" min":Math.round(w/36e5)+" h"}.`:"Lo siguiente toca mañana."}${Q.allN?` Te quedan ${Q.allN.toLocaleString("es-MX")} nuevas sin ver.`:""}${Q.allR>Q.R.length?` Llegaste al límite de repasos de hoy (${Q.allR-Q.R.length} más esperan).`:""}</p>
          <div class="srs-row">${Q.allN?`<button class="srs-b" data-a="more">Estudiar 10 nuevas más</button>`:""}${w>0?`<button class="srs-b" data-a="ahead">Repasarlas ya</button>`:""}${undo.length?`<button class="srs-b" data-a="undo">Deshacer</button>`:""}${o.onStats?`<button class="srs-b" data-a="stats">Ver estadísticas</button>`:""}</div></div>`;
      }else{
        const c=cur,p=c.st.get(c.k),now=Date.now(),k=counts();
        const num=(x,cl,q)=>q===curQ?`<u class="${cl}">${x}</u>`:`<span class="${cl}">${x}</span>`;
        h+=`<div class="srs-card">${c.t?`<div class="tema">${esc(c.t)}</div>`:""}${show?back(c):front(c)}</div>`;
        if(menu)h+=`<div class="srs-menu"><button data-a="undo" ${undo.length?"":"disabled"}>Deshacer <kbd>Z</kbd></button><button data-a="bury">Enterrar hasta mañana <kbd>-</kbd></button><button data-a="sus">Suspender tarjeta <kbd>@</kbd></button></div>`;
        h+=`</div><div class="srs-bot"><div class="srs-cnt">${num(k.n,"n","n")} + ${num(k.l,"l","l")} + ${num(k.r,"r","r")}</div>`+
          (show?`<div class="srs-ans">${["Otra vez","Difícil","Bien","Fácil"].map((l,g)=>`<div><small>${ivTxt(sched(p,g,now))}</small><button class="srs-b g${g}" data-g="${g}">${l}</button></div>`).join("")}</div><div class="srs-k">1 Otra vez · 2 Difícil · 3 Bien (o espacio) · 4 Fácil · Z deshacer</div>`
                :`<button class="srs-b" data-a="show">Mostrar respuesta</button><div class="srs-k">Espacio para mostrar</div>`)+`</div>`;
        root.innerHTML=h;return;
      }
      root.innerHTML=h+`</div>`;
    }
    root.addEventListener("click",e=>{
      const t=e.target.closest("[data-a],[data-g]");if(!t||t.disabled)return;
      if(t.dataset.g){grade(+t.dataset.g);return}
      const a=t.dataset.a;
      if(a==="back"){if(scr==="ov")o.onBack&&o.onBack();else{scr="ov";Q=null;draw()}return}
      if(a==="stats"){o.onStats&&o.onStats();return}
      if(a==="menu"){menu=!menu;draw();return}
      if(a==="study"){scr="rv";pick();draw()}
      else if(a==="show"){show=true;draw()}
      else if(a==="undo")doUndo();
      else if(a==="bury"||a==="sus")act(a==="bury"?"bury":"sus");
      else if(a==="more"){extraNew+=10;scr="rv";pick();draw()}
      else if(a==="ahead"){const now=Date.now();let best=null;for(const c of o.cards()){const p=c.st.get(c.k);if(p&&!p.nw&&!p.sp&&p.q!==1&&(!best||p.d<best.p.d))best={c,p}}
        if(best){cur=best.c;curQ="l";show=false;shown=Date.now();scr="rv";Q=queues(o.cards(),qo,now);draw()}}
      else if(a==="unsus"){for(const c of o.cards()){const p=c.st.get(c.k);if(p&&p.sp){const n=Object.assign({},p);delete n.sp;c.st.put(c.k,n.nw&&Object.keys(n).length===1?null:n)}}Q=null;draw()}
    });
    root.addEventListener("change",e=>{const k=e.target.dataset.k;if(!k)return;o.setLim({[k]:+e.target.value});Q=null;draw()});
    const key=e=>{
      if(!root.isConnected){document.removeEventListener("keydown",key);return}
      if(root.offsetParent===null&&getComputedStyle(root).position!=="fixed")return;/* pestaña escondida */
      if(/INPUT|SELECT|TEXTAREA/.test((e.target||{}).tagName||"")||e.metaKey||e.ctrlKey&&e.key!=="z"||e.altKey)return;
      if(scr==="ov"&&(e.key===" "||e.key==="Enter")&&counts().n+counts().l+counts().r){e.preventDefault();scr="rv";pick();draw();return}
      if(scr!=="rv"){if((e.key==="z"||e.key==="Z")&&undo.length)doUndo();return}
      if(e.key===" "||e.key==="Enter"){e.preventDefault();if(!show){show=true;draw()}else grade(2)}
      else if(show&&/^[1-4]$/.test(e.key))grade(+e.key-1);
      else if(e.key==="z"||e.key==="Z")doUndo();
      else if(e.key==="-")act("bury");
      else if(e.key==="@"||e.key==="!")act("sus");
      else if(e.key==="Escape"&&menu){menu=false;draw()}
    };
    document.addEventListener("keydown",key);
    draw();
    return {el:root,refresh(){Q=null;if(scr==="rv"&&cur&&!show){pick()}draw()},study(){scr="rv";pick();draw()},destroy(){clearTimeout(timer);document.removeEventListener("keydown",key);root.remove()}};
  }

  /* ===== lista de mazos (como la pantalla principal de Anki) =====
     decks: [{id,name,group,cards:()=>[...],ids,newLim,revLim}] */
  function deckCounts(d){const ord=()=>0;const Q=queues(d.cards(),{ids:d.ids,newLim:d.newLim,revLim:d.revLim,rnd:ord},Date.now());return {n:Q.N.length,l:Q.L.length+Q.La.length,r:Q.R.length,total:d.cards().length}}
  function deckList(decks){
    let grp=null,h=`<table class="srs-decks"><thead><tr><th>Mazo</th><th>Nuevas</th><th>Aprender</th><th>Por repasar</th></tr></thead><tbody>`;
    for(const d of decks){
      if(d.group&&d.group!==grp){grp=d.group;h+=`<tr class="sem"><td colspan="4">${esc(grp)}</td></tr>`}
      const k=deckCounts(d),z=v=>v?"":" z";
      h+=`<tr data-deck="${esc(d.id)}"><td>${esc(d.name)} <small style="color:var(--s-mute)">${k.total.toLocaleString("es-MX")}</small></td><td class="n${z(k.n)}">${k.n}</td><td class="l${z(k.l)}">${k.l}</td><td class="r${z(k.r)}">${k.r}</td></tr>`;
    }
    return h+`</tbody></table>`;
  }

  /* ===== estadísticas (como las de Anki) =====
     o: {title, decks:()=>[{id,name,total,states:()=>[estado...]}], scopes:[[valor,etiqueta]], scope} */
  const COL={nw:"#3b82f6",lrn:"#f59e0b",rl:"#dc2626",yg:"#7cc46f",mt:"#23753a",sus:"#a3a3a3",bur:"#c8b27a"};
  function svgBars(data,o){/* data: [{x,tip,segs:[[valor,color]]}] → barras apiladas */
    const W=640,H=o.h||170,P=[8,4,22,34],n=data.length||1,raw=Math.max(1,Math.max(0,...data.map(d=>d.segs.reduce((a,s)=>a+s[0],0)))/3),e10=Math.pow(10,Math.floor(Math.log10(raw))),stp=o.fmtY?raw:[1,2,5,10].map(m=>m*e10).find(v=>v>=raw),mx=stp*3,bw=(W-P[3]-P[1])/n,y=v=>(H-P[2])-(v/mx)*(H-P[2]-P[0]);
    let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(o.label||"")}">`;
    for(let i=0;i<=3;i++){const v=mx*i/3,yy=y(v);s+=`<line x1="${P[3]}" x2="${W-P[1]}" y1="${yy}" y2="${yy}" stroke="currentColor" stroke-opacity=".12"/><text x="${P[3]-5}" y="${yy+3}" text-anchor="end">${o.fmtY?o.fmtY(v):Math.round(v)}</text>`}
    data.forEach((d,i)=>{let acc=0;const x=P[3]+i*bw+Math.min(2,bw*.15),w=Math.max(1,bw-Math.min(4,bw*.3));
      d.segs.forEach(([v,c])=>{if(!v)return;const y1=y(acc+v),y0=y(acc);s+=`<rect x="${x}" y="${y1}" width="${w}" height="${Math.max(.5,y0-y1-(acc?1:0))}" fill="${c}" rx="${Math.min(2,w/2)}"/>`;acc+=v});
      s+=`<rect x="${P[3]+i*bw}" y="${P[0]}" width="${bw}" height="${H-P[2]-P[0]}" fill="transparent" data-tip="${esc(d.tip)}"/>`;
      if(d.lab)s+=`<text x="${x+w/2}" y="${H-P[2]+13}" text-anchor="middle">${esc(d.lab)}</text>`});
    return s+`</svg>`;
  }
  const leg=items=>`<div class="srs-leg">${items.map(([c,l])=>`<span><i style="background:${c}"></i>${l}</span>`).join("")}</div>`;
  const pc=(a,b)=>b?Math.round(a/b*1000)/10+" %":"—";
  const nf=v=>Math.round(v).toLocaleString("es-MX");
  const MES=["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
  const dlab=k=>{const [y,m,d]=k.split("-").map(Number);return d+" "+MES[m-1]};
  function stats(host,o){
    css();const root=document.createElement("div");root.className="srs";if(o.dark!=null?o.dark:dark())root.dataset.dark="";host.appendChild(root);tips(root);
    let scope=o.scope||"",range=30;
    function draw(){
      reloadAll();
      const all=o.decks(),decks=all.filter(d=>!scope||d.id===scope||(d.ids||[]).includes(scope)||(scope.startsWith("@")&&d.group===scope.slice(1)));
      const ids=new Set();decks.forEach(d=>{ids.add(d.id);(d.ids||[]).forEach(i=>ids.add(i))});
      const D=dias(),now=Date.now(),t0=dayStart(now),tk=dayKey(now),inS=k=>ids.has(k);
      /* recuento de tarjetas */
      const cc={nw:0,lrn:0,rl:0,yg:0,mt:0,sus:0,bur:0},iv=[],ez=[],fc=new Map();let total=0;
      for(const d of decks){total+=d.total;let seen=0;
        for(const p of d.states()){if(!p)continue;if(p.nw){if(p.sp)cc.sus++;else if(p.bu===tk)cc.bur++;continue}seen++;
          if(p.sp)cc.sus++;else if(p.bu===tk)cc.bur++;else if(p.q===0)cc.lrn++;else if(p.q===2)cc.rl++;else if(p.i>=21)cc.mt++;else cc.yg++;
          if(p.q===1&&!p.sp){iv.push(p.i);ez.push(p.e);const dd=Math.max(0,Math.ceil((dayStart(p.d)-t0)/DAY));fc.set(dd,(fc.get(dd)||0)+1)}
          else if(!p.sp&&p.q!==1&&p.d<t0+DAY)fc.set(0,(fc.get(0)||0)+1)}
        }
      cc.nw=Math.max(0,total-cc.lrn-cc.rl-cc.yg-cc.mt-cc.sus-cc.bur);
      /* repasos por día */
      const days=Object.keys(D.d).sort(),rowsOf=k=>{const r=[0,0,0,0,0,0,0,0,0,0],d=D.d[k]||{};for(const dk in d)if(inS(dk))d[dk].forEach((v,i)=>r[i]+=v);return r};
      const T=rowsOf(tk),tn=T[0]+T[1]+T[2]+T[3];
      const L=logItems().filter(x=>inS(x.r[1]));const lt=L.filter(x=>x.r[0]>=t0);
      const again=lt.filter(x=>x.r[2]===1).length,lrnT=lt.filter(x=>x.r[3]===0).length,revT=lt.filter(x=>x.r[3]===1).length,rlT=lt.filter(x=>x.r[3]===2).length,
        matT=lt.filter(x=>x.r[3]===1&&x.r[5]>=21);
      let h=`<div class="srs-st"><div class="bar">${o.scopes?`<select data-k="scope" style="font:inherit;padding:5px 8px;border:1px solid var(--s-line);border-radius:8px;background:var(--s-btn);color:var(--s-ink);max-width:100%">${o.scopes().map(([v,l])=>`<option value="${esc(v)}"${v===scope?" selected":""}>${esc(l)}</option>`).join("")}</select>`:`<b>${esc(o.title||"")}</b>`}
        <span class="srs-seg" style="margin-left:auto">${[[30,"1 mes"],[90,"3 meses"],[365,"1 año"]].map(([v,l])=>`<button data-r="${v}" aria-pressed="${v===range}">${l}</button>`).join("")}</span></div>`;
      /* Hoy */
      h+=`<section class="srs-sc"><h4>Hoy</h4><div class="srs-today">${tn?`Estudiaste <b>${tn}</b> tarjeta${tn===1?"":"s"} en <b>${Math.max(1,Math.round(T[4]/MIN))} min</b> hoy (${(T[4]/1000/tn).toFixed(1).replace(".",",")} s/tarjeta).<br>
        Veces que pulsaste Otra vez: <b>${again}</b> (${pc(lt.length-again,lt.length)} correctas)<br>Aprender: <b>${lrnT}</b>, Repasar: <b>${revT}</b>, Reaprender: <b>${rlT}</b><br>
        Tarjetas maduras: <b>${matT.filter(x=>x.r[2]>1).length}</b> de ${matT.length} correctas (${pc(matT.filter(x=>x.r[2]>1).length,matT.length)})`:"Hoy no has estudiado ninguna tarjeta."}</div></section>`;
      /* Previsión */
      const fd=[];for(let i=0;i<range;i++)fd.push(fc.get(i)||0);const fsum=fd.reduce((a,b)=>a+b,0);
      const step=range>60?7:1,fb=[];for(let i=0;i<range;i+=step){const v=fd.slice(i,i+step).reduce((a,b)=>a+b,0);const dt=dayKey(t0+i*DAY+36e5);fb.push({segs:[[v,COL.yg]],tip:`${step>1?"Semana del "+dlab(dt):i===0?"Hoy":i===1?"Mañana":dlab(dt)}: <b>${v}</b> tarjeta${v===1?"":"s"}`,lab:i%(step>1?28:range>30?14:5)===0?(i===0?"hoy":"+"+i+" d"):""})}
      h+=`<section class="srs-sc"><h4>Previsión</h4><p class="sub">Tarjetas que te tocará repasar en los próximos días</p>${svgBars(fb,{label:"Previsión"})}
        <div class="kv"><span>Total: <b>${nf(fsum)}</b> repasos</span><span>Promedio: <b>${(fsum/range).toFixed(1).replace(".",",")}</b> al día</span><span>Toca mañana: <b>${nf(fd[1]||0)}</b></span><span>Atrasadas y de hoy: <b>${nf(fd[0]||0)}</b></span></div></section>`;
      /* Calendario */
      const yr=[];let mxc=1;for(let i=364;i>=0;i--){const k=dayKey(t0-i*DAY+36e5),r=rowsOf(k),n=r[0]+r[1]+r[2]+r[3];yr.push([k,n]);mxc=Math.max(mxc,n)}
      const first=new Date(keyMs(yr[0][0])).getDay(),cw=11.4,cs=10;let cal=`<svg viewBox="0 0 ${Math.ceil((yr.length+first)/7)*cw+20} ${7*cw+16}" role="img" aria-label="Calendario">`;
      const shade=n=>!n?"currentColor":["#c6e8bf","#8fd18a","#4daf5c","#23753a"][Math.min(3,Math.floor(n/mxc*4))];
      let lm=-1;yr.forEach(([k,n],i)=>{const j=i+first,x=20+Math.floor(j/7)*cw,y=12+(j%7)*cw,m=+k.split("-")[1];
        if(j%7===0&&m!==lm){lm=m;cal+=`<text x="${x}" y="8">${MES[m-1]}</text>`}
        cal+=`<rect x="${x}" y="${y}" width="${cs}" height="${cs}" rx="2" fill="${shade(n)}" ${n?"":`fill-opacity=".08"`} data-tip="${dlab(k)}: <b>${n}</b> repaso${n===1?"":"s"}"/>`});
      ["L","M","V"].forEach((d,i)=>cal+=`<text x="2" y="${12+[1,3,5][i]*cw+8}">${d}</text>`);
      const studied=yr.filter(x=>x[1]).length;let streak=0;for(let i=yr.length-1;i>=0;i--){if(yr[i][1])streak++;else if(i===yr.length-1)continue;else break}
      h+=`<section class="srs-sc"><h4>Calendario</h4>${cal}</svg><div class="kv"><span>Días estudiados: <b>${studied}</b> de 365</span><span>Racha: <b>${streak}</b> día${streak===1?"":"s"}</span></div></section>`;
      /* Repasos */
      const rb=[];let rs=[0,0,0,0,0],rdays=0;const rstep=range>60?7:1;
      for(let i=range-rstep;i>=0;i-=rstep){const seg=[0,0,0,0,0];for(let j=0;j<rstep;j++){const r=rowsOf(dayKey(t0-(i+j)*DAY+36e5));for(let q=0;q<5;q++)seg[q]+=r[q];if(r[0]+r[1]+r[2]+r[3])rdays++}
        for(let q=0;q<5;q++)rs[q]+=seg[q];const n=seg[0]+seg[1]+seg[2]+seg[3],dt=dayKey(t0-i*DAY+36e5);
        rb.push({segs:[[seg[2],COL.mt],[seg[1],COL.yg],[seg[3],COL.rl],[seg[0],COL.lrn]],tip:`${rstep>1?"Semana al "+dlab(dt):i===0?"Hoy":dlab(dt)}: <b>${n}</b> repasos<br>Aprender ${seg[0]} · Jóvenes ${seg[1]} · Maduras ${seg[2]} · Reaprender ${seg[3]}<br>${Math.round(seg[4]/MIN)} min`,lab:(i/rstep)%(range>60?4:range>30?14:5)===0?(i===0?"hoy":"−"+i+" d"):""})}
      const rn=rs[0]+rs[1]+rs[2]+rs[3];
      h+=`<section class="srs-sc"><h4>Repasos</h4><p class="sub">Cuántas tarjetas repasaste cada día</p>${svgBars(rb,{label:"Repasos"})}${leg([[COL.lrn,"Aprender"],[COL.yg,"Jóvenes"],[COL.mt,"Maduras"],[COL.rl,"Reaprender"]])}
        <div class="kv"><span>Días estudiados: <b>${rdays}</b> de ${range} (${pc(rdays,range)})</span><span>Total: <b>${nf(rn)}</b> repasos</span><span>Promedio: <b>${(rn/range).toFixed(1).replace(".",",")}</b> al día</span><span>Tiempo: <b>${Math.round(rs[4]/MIN)} min</b></span></div></section>`;
      /* Recuento de tarjetas */
      const parts=[["nw","Nuevas"],["lrn","Aprendiendo"],["rl","Reaprendiendo"],["yg","Jóvenes"],["mt","Maduras"],["sus","Suspendidas"],["bur","Enterradas"]],ct=Math.max(1,parts.reduce((a,[k])=>a+cc[k],0));
      let x=0,stk=`<svg viewBox="0 0 640 28" role="img" aria-label="Recuento de tarjetas">`;parts.forEach(([k,l])=>{if(!cc[k])return;const w=cc[k]/ct*640;stk+=`<rect x="${x}" y="2" width="${Math.max(1,w-2)}" height="24" rx="4" fill="${COL[k]}" data-tip="${l}: <b>${nf(cc[k])}</b> (${pc(cc[k],ct)})"/>`;x+=w});
      h+=`<section class="srs-sc"><h4>Recuento de tarjetas</h4>${stk}</svg><table style="margin-top:10px"><tbody>${parts.map(([k,l])=>`<tr><td><i style="display:inline-block;width:10px;height:10px;border-radius:3px;background:${COL[k]};margin-right:6px"></i>${l}</td><td>${nf(cc[k])}</td><td>${pc(cc[k],ct)}</td></tr>`).join("")}<tr><td><b>Total</b></td><td><b>${nf(ct)}</b></td><td></td></tr></tbody></table></section>`;
      /* Intervalos y facilidad */
      const hist=(arr,edges,labf)=>edges.slice(0,-1).map((e,i)=>{const n=arr.filter(v=>v>=e&&v<edges[i+1]).length;return {segs:[[n,COL.mt]],tip:`${labf(e,edges[i+1])}: <b>${n}</b> tarjeta${n===1?"":"s"}`,lab:i%2===0?String(e):""}});
      const ie=[1,2,3,4,5,7,10,14,21,30,45,60,90,120,180,270,365,730,36501];
      h+=`<section class="srs-sc"><h4>Intervalos</h4><p class="sub">Cada cuántos días vuelve cada tarjeta (las que ya están en repaso)</p>${iv.length?svgBars(hist(iv,ie,(a,b)=>b>36500?`${a}+ días`:`${a}–${b-1} días`),{label:"Intervalos"})+`<div class="kv"><span>Intervalo promedio: <b>${(iv.reduce((a,b)=>a+b,0)/iv.length).toFixed(1).replace(".",",")} días</b></span><span>Más largo: <b>${Math.max(...iv)} días</b></span></div>`:`<p class="sub">Todavía no hay tarjetas en repaso.</p>`}</section>`;
      const ee=[130,150,170,190,210,230,250,270,290,310,400];
      h+=`<section class="srs-sc"><h4>Facilidad</h4><p class="sub">Qué tan fáciles te resultan (250 % es lo normal; baja con Otra vez y Difícil)</p>${ez.length?svgBars(hist(ez,ee,(a,b)=>`${a}–${b-1} %`),{label:"Facilidad"})+`<div class="kv"><span>Facilidad promedio: <b>${Math.round(ez.reduce((a,b)=>a+b,0)/ez.length)} %</b></span></div>`:`<p class="sub">Todavía no hay tarjetas en repaso.</p>`}</section>`;
      /* Botones de respuesta */
      const lr=L.filter(x=>x.r[0]>=t0-(range-1)*DAY),grp=[["Aprendiendo",x=>x.r[3]!==1],["Jóvenes",x=>x.r[3]===1&&x.r[5]<21],["Maduras",x=>x.r[3]===1&&x.r[5]>=21]];
      const bc=["#dc2626","#9ca3af","#23753a","#3b82f6"],bd=[];
      grp.forEach(([gl,f])=>{const s=lr.filter(f),tot=s.length;[0,1,2,3].forEach(b=>{const n=s.filter(x=>x.r[2]===b+1).length;bd.push({segs:[[n,bc[b]]],tip:`${gl} · ${["Otra vez","Difícil","Bien","Fácil"][b]}: <b>${n}</b> (${pc(n,tot)})`,lab:b===1?gl:""})});bd.push({segs:[],tip:"",lab:""})});bd.pop();
      const corr=grp.map(([gl,f])=>{const s=lr.filter(f);return `${gl}: <b>${pc(s.filter(x=>x.r[2]>1).length,s.length)}</b> correctas (${s.length})`});
      h+=`<section class="srs-sc"><h4>Botones de respuesta</h4>${lr.length?svgBars(bd,{label:"Botones de respuesta"})+leg([[bc[0],"Otra vez"],[bc[1],"Difícil"],[bc[2],"Bien"],[bc[3],"Fácil"]])+`<div class="kv">${corr.map(c=>`<span>${c}</span>`).join("")}</div>`:`<p class="sub">Sin repasos en este periodo.</p>`}</section>`;
      /* Desglose por hora */
      const hb=[];for(let hr=0;hr<24;hr++){const s=lr.filter(x=>new Date(x.r[0]).getHours()===hr),ok=s.filter(x=>x.r[2]>1).length;hb.push({segs:[[s.length,COL.nw]],tip:`${hr}:00–${hr}:59: <b>${s.length}</b> repasos<br>${pc(ok,s.length)} correctas`,lab:hr%3===0?hr+"h":""})}
      h+=`<section class="srs-sc"><h4>Desglose por hora</h4><p class="sub">A qué hora estudias (pasa el cursor para ver qué tanto aciertas)</p>${lr.length?svgBars(hb,{label:"Desglose por hora",h:140}):`<p class="sub">Sin repasos en este periodo.</p>`}</section>`;
      /* Retención real */
      const per=[["Hoy",0],["Ayer",-1],["Última semana",7],["Último mes",30],["Último año",365],["Total",99999]];
      const sumR=(a,b)=>{const r=[0,0,0,0];for(const k of days){const ms=keyMs(k);if(ms<t0-a*DAY||ms>t0-b*DAY)continue;const x=rowsOf(k);r[0]+=x[5];r[1]+=x[6];r[2]+=x[7];r[3]+=x[8]}return r};
      h+=`<section class="srs-sc"><h4>Retención real</h4><p class="sub">De las tarjetas en repaso, cuántas recordaste (Difícil, Bien o Fácil cuentan como correctas)</p><table><thead><tr><th></th><th>Jóvenes</th><th>Maduras</th><th>Total</th><th>Repasos</th></tr></thead><tbody>${per.map(([l,v])=>{const r=v===0?sumR(0,0):v===-1?sumR(1,1):sumR(v-1,0);
        return `<tr><td>${l}</td><td>${pc(r[0],r[0]+r[1])}</td><td>${pc(r[2],r[2]+r[3])}</td><td>${pc(r[0]+r[2],r[0]+r[1]+r[2]+r[3])}</td><td>${nf(r[0]+r[1]+r[2]+r[3])}</td></tr>`}).join("")}</tbody></table></section>`;
      /* Por materia */
      if(all.length>1){
        const rows=decks.map(d=>{let a=0,yg=0,mt=0;for(const p of d.states()){if(!p||p.nw)continue;a++;if(p.q===1){if(p.i>=21)mt++;else yg++}}
          const dd=new Set([d.id].concat(d.ids||[]));let n=0,ok=0,bad=0;for(const k of days){if(keyMs(k)<t0-29*DAY)continue;const r=D.d[k];for(const x in r)if(dd.has(x)){n+=r[x][0]+r[x][1]+r[x][2]+r[x][3];ok+=r[x][5]+r[x][7];bad+=r[x][6]+r[x][8]}}
          return {d,a,yg,mt,n,ok,bad}}).filter(r=>r.a||r.n).sort((x,y)=>y.n-x.n||y.a-x.a);
        h+=`<section class="srs-sc"><h4>Por materia</h4><p class="sub">Repasos y retención de los últimos 30 días</p>${rows.length?`<div style="overflow-x:auto"><table><thead><tr><th>Mazo</th><th>Vistas</th><th>Jóvenes</th><th>Maduras</th><th>Repasos (30 d)</th><th>Retención</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.d.name)}</td><td>${nf(r.a)} / ${nf(r.d.total)}</td><td>${nf(r.yg)}</td><td>${nf(r.mt)}</td><td>${nf(r.n)}</td><td>${pc(r.ok,r.ok+r.bad)}</td></tr>`).join("")}</tbody></table></div>`:`<p class="sub">Aún no has estudiado ningún mazo.</p>`}</section>`;
      }
      root.innerHTML=h+`</div>`;
    }
    root.addEventListener("click",e=>{const b=e.target.closest("[data-r]");if(b){range=+b.dataset.r;draw()}});
    root.addEventListener("change",e=>{if(e.target.dataset.k==="scope"){scope=e.target.value;draw()}});
    draw();
    return {el:root,refresh:draw,setScope(s){scope=s;draw()},destroy(){root.remove()}};
  }

  /* todos los mazos de Anki que ya se abrieron en este aparato (para las estadísticas de "todas las materias") */
  function knownDecks(){
    const out=[],D=dias();
    try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k&&k.startsWith("carrera-anki-")&&k!=="carrera-anking-clave"){const id=k.slice(13),st=deckStore(id),P=st.meta();
      out.push({id,name:P.name||D.n[id]||id,total:Math.max(P.N||0,Object.keys(P.c).length),states:()=>Object.values(st.all())})}}}catch(e){}
    return out.sort((a,b)=>a.name.localeCompare(b.name,"es"));
  }

  window.SRS={sched,answer,ivTxt,dayStart,dayKey,hash,isNew,deckStore,repasoStore,reloadAll,record,today,queues,reviewer,deckList,deckCounts,stats,knownDecks,css,dark,front,back,isCloze};
})();
