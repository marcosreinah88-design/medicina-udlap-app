/* Tarjetas de Anki de Marcos (revisadas y corregidas). Uso:
   <script src=".../anki/anki.js" data-m="hematologia" data-n="2284" defer></script>
   - Dentro de una guía: agrega un botón flotante "Tus tarjetas de Anki" que abre el repaso.
   - En una página con <div id="ak-root"></div>: muestra el repaso dentro de la página.
   Datos: anki/<materia>.json  {id,n,s,c:[[tema,frente,reverso]],q:[[tema,pregunta,[opciones],correcta,explicación]]}
   Repaso como Anki (Otra vez / Difícil / Bien / Fácil) con repetición espaciada tipo SM-2:
   pasos de aprendizaje 1 y 10 min, se gradúa a 1 día (Fácil: 4 días), luego intervalo × facilidad.
   Progreso en localStorage carrera-anki-<materia>: {v:2,c:{hash:{q,s,e,i,n,l,d}},day,nw,hoy,lim}. */
(function(){
  const me=document.currentScript;if(!me)return;
  const M=me.dataset.m,N=+me.dataset.n||0,BASE=me.src.replace(/[^\/]*$/,"");
  const KEY="carrera-anki-"+M;
  const J=(k,d)=>{try{const v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}};
  const S=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}};
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const fmt=s=>esc(s).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").split(" · ").join("<br>");
  const norm=s=>String(s).normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase();
  const hash=s=>{let h=5381;for(let i=0;i<s.length;i++)h=(h*33^s.charCodeAt(i))>>>0;return h.toString(36)};
  const dark=()=>{const t=document.documentElement.dataset.theme||document.body&&document.body.dataset.theme;
    if(t)return t==="dark";try{return matchMedia("(prefers-color-scheme: dark)").matches}catch(e){return false}};
  /* ===== programador estilo Anki ===== */
  const LS=[1,10],RS=[10],GRAD=1,EASY=4,MAXI=3650,DAY=864e5,MIN=6e4;
  const dayStart=t=>{const d=new Date(t-4*36e5);d.setHours(4,0,0,0);return d.getTime()};/* el día cambia a las 4 a. m., como en Anki */
  const dayKey=t=>{const d=new Date(dayStart(t));return d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate()};
  /* q: 0 nueva/aprendiendo, 1 repaso, 2 reaprendiendo · s: paso · e: facilidad (%) · i: intervalo (días) · n: repasos · l: olvidos · d: cuándo toca (ms) */
  function sched(p,g,now){
    const c=p?Object.assign({},p):{q:0,s:0,e:250,i:0,n:0,l:0,d:now};let m=0;
    if(c.q!==1){
      const st=c.q===2?RS:LS;let grad=0;
      if(g===0){c.s=0;m=st[0]}
      else if(g===1)m=c.s===0?(st.length>1?Math.round((st[0]+st[1])/2):Math.min(Math.round(st[0]*1.5),st[0]+1440)):st[c.s];
      else if(g===2){if(c.s+1<st.length){c.s++;m=st[c.s]}else grad=c.q===2?Math.max(1,c.i):GRAD}
      else grad=c.q===2?Math.max(1,c.i)+1:EASY;
      if(grad){c.q=1;c.s=0;c.i=grad}
    }else{
      const late=Math.max(0,Math.floor((dayStart(now)-c.d)/DAY)),h=Math.max(c.i+1,Math.round(c.i*1.2)),
        gd=Math.max(h+1,Math.round((c.i+late/2)*c.e/100)),ez=Math.max(gd+1,Math.round((c.i+late)*c.e/100*1.3));
      if(g===0){c.l++;c.e=Math.max(130,c.e-20);c.i=1;c.q=2;c.s=0;m=RS[0]}
      else if(g===1){c.i=h;c.e=Math.max(130,c.e-15)}
      else if(g===2)c.i=gd;
      else{c.i=ez;c.e+=15}
    }
    c.i=Math.min(c.i,MAXI);c.n++;c.d=m?now+m*MIN:dayStart(now)+c.i*DAY;c.m=m;return c;
  }
  const ivTxt=c=>{if(c.m)return c.m<=1?"<1 min":c.m<60?c.m+" min":Math.round(c.m/60)+" h";
    const i=c.i,f=x=>String(Math.round(x*10)/10).replace(".",",");return i<30?i+" d":i<365?f(i/30)+" m":f(i/365)+" a"};
  const CSS=`.ak{--ak-bg:#fbfaf6;--ak-card:#fff;--ak-ink:#1d2a24;--ak-mute:#5d6b64;--ak-line:#dfe3dc;--ak-g:#00573c;--ak-o:#f26b21;--ak-soft:#e8f1ec;
font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ak-ink);text-align:left}
.ak[data-dark]{--ak-bg:#121815;--ak-card:#1b2420;--ak-ink:#e7ece8;--ak-mute:#a3b0a9;--ak-line:#2e3a34;--ak-g:#4fbf8f;--ak-o:#ff9558;--ak-soft:#1f3329}
.ak *{box-sizing:border-box}.ak button{font:inherit;cursor:pointer}
.ak-fab{position:fixed;right:16px;bottom:16px;z-index:2147483000;display:flex;align-items:center;gap:8px;padding:10px 16px;border-radius:999px;border:0;background:#00573c;color:#fff;
font:600 14px/1.2 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.22)}
.ak-fab small{background:#f26b21;border-radius:999px;padding:2px 8px;font-weight:700}
.ak-ov{position:fixed;inset:0;z-index:2147483001;background:rgba(10,20,15,.55);display:flex;align-items:stretch;justify-content:center;padding:16px}
.ak-ov .ak{background:var(--ak-bg);width:100%;max-width:760px;border-radius:16px;overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.ak-in{padding:20px}
.ak-hd{display:flex;align-items:flex-start;gap:12px;margin-bottom:14px}.ak-hd h2{margin:0;font-size:20px;line-height:1.25}.ak-hd p{margin:2px 0 0;color:var(--ak-mute);font-size:13px}
.ak-x{margin-left:auto;border:1px solid var(--ak-line);background:var(--ak-card);color:var(--ak-ink);border-radius:10px;width:36px;height:36px;flex:none}
.ak-bar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.ak-bar select,.ak-bar input{font:inherit;padding:8px 10px;border:1px solid var(--ak-line);border-radius:10px;background:var(--ak-card);color:var(--ak-ink);min-width:0;flex:1 1 180px}
.ak-tabs{display:flex;gap:6px;margin-bottom:14px;border-bottom:1px solid var(--ak-line)}
.ak-tabs button{border:0;background:none;color:var(--ak-mute);padding:8px 12px;border-bottom:3px solid transparent;font-weight:600}
.ak-tabs button[aria-selected=true]{color:var(--ak-g);border-color:var(--ak-o)}
.ak-prog{height:6px;background:var(--ak-line);border-radius:6px;overflow:hidden;margin:4px 0 14px}.ak-prog i{display:block;height:100%;background:var(--ak-g)}
.ak-card{background:var(--ak-card);border:1px solid var(--ak-line);border-radius:14px;padding:22px;min-height:190px;display:flex;flex-direction:column;gap:12px}
.ak-tema{font-size:12px;color:var(--ak-o);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.ak-f{font-size:19px;font-weight:600;line-height:1.35}.ak-b{border-top:1px dashed var(--ak-line);padding-top:12px;font-size:16px}
.ak-act{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.ak-btn{flex:1 1 120px;padding:11px 14px;border-radius:12px;border:1px solid var(--ak-line);background:var(--ak-card);color:var(--ak-ink);font-weight:600}
.ak-btn.p{background:var(--ak-g);border-color:var(--ak-g);color:#fff}.ak-btn.o{border-color:var(--ak-o);color:var(--ak-o)}
.ak-meta{display:flex;justify-content:space-between;color:var(--ak-mute);font-size:13px;margin-top:10px;gap:8px;flex-wrap:wrap}
.ak-list{display:flex;flex-direction:column;gap:8px}.ak-li{background:var(--ak-card);border:1px solid var(--ak-line);border-radius:12px;padding:12px 14px}
.ak-li b.f{display:block;margin-bottom:4px}.ak-li .bk{color:var(--ak-mute)}.ak-li.ok{border-left:4px solid var(--ak-g)}
.ak-more{margin:10px auto 0;display:block}
.ak-opt{display:block;width:100%;text-align:left;padding:11px 14px;border-radius:12px;border:1px solid var(--ak-line);background:var(--ak-card);color:var(--ak-ink);margin-top:8px}
.ak-opt.ok{border-color:#1e8a57;background:rgba(30,138,87,.12)}.ak-opt.no{border-color:#c0392b;background:rgba(192,57,43,.1)}
.ak-empty{color:var(--ak-mute);text-align:center;padding:30px 10px}
.ak-cnt{display:flex;gap:14px;align-items:center;font-weight:700;font-variant-numeric:tabular-nums}.ak-cnt span{display:inline-flex;gap:4px;align-items:baseline}.ak-cnt small{font-weight:500;color:var(--ak-mute)}
.ak-cnt .n{color:#2a6fdb}.ak-cnt .l{color:#c0392b}.ak-cnt .r{color:var(--ak-g)}.ak-cnt .cur{text-decoration:underline;text-underline-offset:4px}
.ak[data-dark] .ak-cnt .n{color:#7aa7ff}.ak[data-dark] .ak-cnt .l{color:#ff7b6b}
.ak-gr{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:14px}
.ak-gr button{display:flex;flex-direction:column;align-items:center;gap:2px;padding:10px 6px;border-radius:12px;border:1.5px solid var(--ak-line);background:var(--ak-card);color:var(--ak-ink);font-weight:700}
.ak-gr button small{font-weight:500;color:var(--ak-mute);font-size:12px}
.ak-gr .g0{border-color:#c0392b;color:#c0392b}.ak-gr .g1{border-color:#8a6d1e;color:#8a6d1e}.ak-gr .g2{border-color:var(--ak-g);color:var(--ak-g)}.ak-gr .g3{border-color:#2a6fdb;color:#2a6fdb}
.ak[data-dark] .ak-gr .g0{border-color:#ff7b6b;color:#ff7b6b}.ak[data-dark] .ak-gr .g1{border-color:#e0c060;color:#e0c060}.ak[data-dark] .ak-gr .g3{border-color:#7aa7ff;color:#7aa7ff}
.ak-gr button:hover{background:var(--ak-soft)}
.ak-st{font-size:12px;color:var(--ak-mute);margin-top:6px}.ak-st b{color:var(--ak-o)}
.ak-sm{font-size:13px;color:var(--ak-mute);display:flex;gap:6px;align-items:center}.ak-sm select{font:inherit;padding:2px 6px;border:1px solid var(--ak-line);border-radius:8px;background:var(--ak-card);color:var(--ak-ink)}
.ak-lnk{border:0;background:none;color:var(--ak-mute);text-decoration:underline;padding:4px;font-size:13px}
@media (max-width:520px){.ak-gr button{padding:9px 2px;font-size:14px}.ak-ov{padding:0}.ak-ov .ak{border-radius:0}.ak-in{padding:16px}.ak-f{font-size:17px}}`;
  function css(){if(document.getElementById("ak-css"))return;const s=document.createElement("style");s.id="ak-css";s.textContent=CSS;document.head.appendChild(s)}
  let DATA=null;
  const load=()=>DATA?Promise.resolve(DATA):fetch(BASE+M+".json").then(r=>r.json()).then(d=>{d.c.forEach(c=>c.push(hash(c[1]+"|"+c[2])));DATA=d;return d});
  function app(host,inPage,close){
    const st={tab:"repasar",tema:"",q:"",show:false,cur:null,curQ:"",cnt:0,undo:null,sure:false,lim:60,qi:0,qa:-1,qord:[],ok:0,tot:0,order:new Map()};
    let P=J(KEY,null);
    if(Array.isArray(P)){/* versión anterior: lista de "ya me la sé" → pasan a repaso a 4 días */
      const now=Date.now(),c={};P.forEach(h=>c[h]={q:1,s:0,e:250,i:4,n:1,l:0,d:dayStart(now)+4*DAY});P={v:2,c}}
    if(!P||typeof P!=="object"||!P.c)P={v:2,c:{}};if(!P.lim)P.lim=20;
    const save=()=>S(KEY,P);
    const today=()=>{const k=dayKey(Date.now());if(P.day!==k){P.day=k;P.nw=0;P.hoy=0}};
    const root=document.createElement("div");root.className="ak";if(dark())root.dataset.dark="";host.appendChild(root);
    const cards=()=>DATA.c.filter(c=>(!st.tema||c[0]===st.tema)&&(!st.q||norm(c[1]+" "+c[2]).includes(norm(st.q))));
    const qs=()=>DATA.q.filter(q=>!st.tema||q[0]===st.tema);
    const rnd=h=>{if(!st.order.has(h))st.order.set(h,Math.random());return st.order.get(h)};
    function queues(ahead){
      today();const now=Date.now(),end=dayStart(now)+DAY,L=[],R=[],N=[];let wait=Infinity;
      for(const c of cards()){const p=P.c[c[3]];
        if(!p)N.push(c);else if(p.q!==1){if(p.d<=now+(ahead?20*MIN:0))L.push(c);else wait=Math.min(wait,p.d)}else if(p.d<end)R.push(c)}
      L.sort((a,b)=>P.c[a[3]].d-P.c[b[3]].d);R.sort((a,b)=>rnd(a[3])-rnd(b[3]));N.sort((a,b)=>rnd(a[3])-rnd(b[3]));
      return {L,R,N:N.slice(0,Math.max(0,P.lim-(P.nw||0))),allN:N.length,wait};
    }
    function pick(){
      let Q=queues(false);if(!Q.L.length&&!Q.R.length&&!Q.N.length)Q=queues(true);
      st.show=false;st.sure=false;
      if(Q.L.length){st.cur=Q.L[0];st.curQ="l"}
      else if(Q.R.length&&Q.N.length){const k=Math.max(2,Math.round(Q.R.length/Q.N.length)+1);st.cnt++;if(st.cnt%k===0){st.cur=Q.N[0];st.curQ="n"}else{st.cur=Q.R[0];st.curQ="r"}}
      else if(Q.R.length){st.cur=Q.R[0];st.curQ="r"}else if(Q.N.length){st.cur=Q.N[0];st.curQ="n"}else{st.cur=null;st.curQ=""}
      return Q;
    }
    let timer=0;
    const fmtWait=ms=>{const m=Math.max(1,Math.round(ms/MIN));return m<60?m+" min":Math.round(m/60)+" h"};
    function deal(){st.cur=null;pick()}
    function grade(g){
      const c=st.cur;if(!c||!st.show)return;const h=c[3],prev=P.c[h],now=Date.now();
      const n=sched(prev,g,now);
      if(!n.m&&n.i>=3){const f=Math.max(1,Math.round(n.i*.05));n.i=Math.min(MAXI,n.i+Math.round((Math.random()*2-1)*f));n.d=dayStart(now)+n.i*DAY}
      delete n.m;today();st.undo={h,prev,nw:P.nw,hoy:P.hoy};
      if(!prev)P.nw=(P.nw||0)+1;P.hoy=(P.hoy||0)+1;P.c[h]=n;save();pick();
    }
    function doUndo(){const u=st.undo;if(!u)return;if(u.prev)P.c[u.h]=u.prev;else delete P.c[u.h];P.nw=u.nw;P.hoy=u.hoy;save();
      const c=DATA.c.find(x=>x[3]===u.h);st.undo=null;if(c){st.cur=c;st.curQ=u.prev?(u.prev.q===1?"r":"l"):"n";st.show=true}}
    function dealQ(){st.qord=qs().map((_,i)=>i).sort(()=>Math.random()-.5);st.qi=0;st.qa=-1;st.ok=0;st.tot=0}
    function temas(){const m=new Map();DATA.c.forEach(c=>m.set(c[0],(m.get(c[0])||0)+1));DATA.q.forEach(q=>m.set(q[0],(m.get(q[0])||0)));return [...m]}
    function state(h){const p=P.c[h];if(!p)return "nueva";if(p.q!==1)return "aprendiendo";const d=Math.round((p.d-dayStart(Date.now()))/DAY);return d<=0?"toca hoy":"vuelve en "+ivTxt({i:d})}
    function body(){
      if(st.tab==="repasar"){
        clearTimeout(timer);
        const Q=queues(false),all=cards(),seen=all.filter(c=>P.c[c[3]]).length,mad=all.filter(c=>{const p=P.c[c[3]];return p&&p.q===1&&p.i>=21}).length,pct=all.length?Math.round(100*seen/all.length):0;
        if(st.cur&&!all.includes(st.cur))pick();
        const cnt=`<div class="ak-cnt"><span class="n${st.curQ==="n"?" cur":""}">${Q.N.length}<small>nuevas</small></span><span class="l${st.curQ==="l"?" cur":""}">${Q.L.length}<small>aprendiendo</small></span><span class="r${st.curQ==="r"?" cur":""}">${Q.R.length}<small>repaso</small></span></div>`;
        let h=`<div class="ak-meta" style="margin-top:0">${cnt}<label class="ak-sm">Nuevas por día <select data-k="lim">${[10,20,30,50,100,9999].map(v=>`<option value="${v}"${v===P.lim?" selected":""}>${v===9999?"sin límite":v}</option>`).join("")}</select></label></div>
          <div class="ak-prog"><i style="width:${pct}%"></i></div><div class="ak-st" style="margin:-8px 0 12px">${seen} de ${all.length} ya vistas · ${mad} maduras (21 días o más) · hoy repasaste <b>${P.hoy||0}</b></div>`;
        const c=st.cur;
        if(!c){
          const w=Q.wait<Infinity?Q.wait-Date.now():0;
          if(w>0&&w<36e5)timer=setTimeout(()=>{if(!st.cur&&st.tab==="repasar"){pick();redraw()}},w+500);
          h+=`<div class="ak-empty">${!all.length?"No hay tarjetas con ese filtro.":`<b style="font-size:18px;color:var(--ak-g)">¡Terminaste por hoy!</b><br>`+
            (w>0?`Las que estás aprendiendo regresan en ${fmtWait(w)}.`:"Las siguientes tocan mañana.")+(Q.allN&&P.lim<9999?` Te quedan ${Q.allN} nuevas sin ver.`:"")}</div>`;
          h+=`<div class="ak-act">${Q.allN?`<button class="ak-btn p" data-a="mas10">Aprender 10 nuevas más hoy</button>`:""}${w>0?`<button class="ak-btn" data-a="ahead">Repasarlas ya</button>`:""}${st.undo?`<button class="ak-btn" data-a="undo">Deshacer</button>`:""}</div>`;
        }else{
          h+=`<div class="ak-card"><div class="ak-tema">${esc(c[0])}</div><div class="ak-f">${fmt(c[1])}</div>${st.show?`<div class="ak-b">${fmt(c[2])}</div>`:""}</div>`;
          const p=P.c[c[3]],now=Date.now();
          h+=st.show?`<div class="ak-gr">${["Otra vez","Difícil","Bien","Fácil"].map((l,g)=>`<button type="button" class="g${g}" data-g="${g}">${l}<small>${ivTxt(sched(p,g,now))}</small></button>`).join("")}</div>`
            :`<div class="ak-act"><button class="ak-btn p" data-a="ver">Mostrar respuesta</button></div>`;
        }
        if(!seen&&!st.cur)return h;
        return h+`<div class="ak-meta"><span>Espacio: mostrar / Bien · 1 Otra vez · 2 Difícil · 3 Bien · 4 Fácil${st.undo?" · Z deshacer":""}</span><span>${st.undo&&c?`<button class="ak-lnk" data-a="undo">Deshacer</button>`:""}<button class="ak-lnk" data-a="reset">${st.sure?"¿Seguro? Toca otra vez para borrar el avance":"Reiniciar avance"}</button></span></div>`;
      }
      if(st.tab==="lista"){
        const all=cards();if(!all.length)return `<div class="ak-empty">No hay tarjetas con ese filtro.</div>`;
        return `<div class="ak-meta" style="margin:0 0 8px"><span>${all.length} tarjetas</span></div><div class="ak-list">`+all.slice(0,st.lim).map(c=>`<div class="ak-li${P.c[c[3]]&&P.c[c[3]].q===1?" ok":""}"><b class="f">${fmt(c[1])}</b><div class="ak-st">${state(c[3])}</div><div class="bk">${fmt(c[2])}</div></div>`).join("")+`</div>`
          +(all.length>st.lim?`<button class="ak-btn ak-more" data-a="mas">Ver más (${all.length-st.lim})</button>`:"");
      }
      const L=qs();if(!L.length)return `<div class="ak-empty">No hay preguntas de opción múltiple en este tema.</div>`;
      if(st.qi>=st.qord.length)return `<div class="ak-card"><div class="ak-f">Terminaste: ${st.ok} de ${st.tot} correctas (${st.tot?Math.round(100*st.ok/st.tot):0} %)</div></div><div class="ak-act"><button class="ak-btn p" data-a="qrst">Otra ronda</button></div>`;
      const q=L[st.qord[st.qi]];
      return `<div class="ak-meta" style="margin:0 0 8px"><span>Pregunta ${st.qi+1} de ${st.qord.length}</span><span>${st.ok} de ${st.tot} correctas</span></div><div class="ak-card"><div class="ak-tema">${esc(q[0])}</div><div class="ak-f">${fmt(q[1])}</div><div>`
        +q[2].map((o,i)=>`<button class="ak-opt${st.qa<0?"":i===q[3]?" ok":i===st.qa?" no":""}" data-o="${i}" ${st.qa<0?"":"disabled"}>${"ABCDE"[i]}) ${fmt(o)}</button>`).join("")+`</div>${st.qa>=0&&q[4]?`<div class="ak-b">${fmt(q[4])}</div>`:""}</div>`
        +(st.qa>=0?`<div class="ak-act"><button class="ak-btn p" data-a="qnext">Siguiente</button></div>`:"");
    }
    function draw(){
      const T=temas(),hasQ=DATA.q.length>0;
      root.innerHTML=`<div class="ak-in"><div class="ak-hd"><div><h2>${esc(DATA.n)} · tus tarjetas de Anki</h2><p>${DATA.c.length} tarjetas${hasQ?" y "+DATA.q.length+" preguntas":""}, revisadas y corregidas.</p></div>${close?`<button class="ak-x" data-a="cerrar" aria-label="Cerrar">✕</button>`:""}</div>
        <div class="ak-bar"><select data-k="tema" aria-label="Tema"><option value="">Todos los temas</option>${T.map(([t,n])=>`<option value="${esc(t)}"${t===st.tema?" selected":""}>${esc(t)} (${n})</option>`).join("")}</select>
        ${st.tab==="lista"?`<input data-k="q" type="search" placeholder="Buscar en las tarjetas" value="${esc(st.q)}">`:""}</div>
        <div class="ak-tabs" role="tablist">${[["repasar","Repasar"],["lista","Ver todas"]].concat(hasQ?[["quiz","Preguntas"]]:[]).map(([k,l])=>`<button role="tab" data-t="${k}" aria-selected="${st.tab===k}">${l}</button>`).join("")}</div>
        <div class="ak-body">${body()}</div></div>`;
    }
    const redraw=()=>{root.querySelector(".ak-body").innerHTML=body()};
    root.addEventListener("click",e=>{
      const t=e.target.closest("[data-t],[data-a],[data-o],[data-g]");if(!t)return;
      if(t.dataset.g){grade(+t.dataset.g);redraw();return}
      if(t.dataset.t){st.tab=t.dataset.t;if(st.tab==="quiz"&&!st.qord.length)dealQ();draw();return}
      if(t.dataset.o!==undefined){if(st.qa>=0)return;const q=qs()[st.qord[st.qi]];st.qa=+t.dataset.o;st.tot++;if(st.qa===q[3])st.ok++;redraw();return}
      const a=t.dataset.a;
      if(a==="cerrar")return close();
      if(a!=="reset")st.sure=false;
      if(a==="ver")st.show=true;
      else if(a==="undo")doUndo();
      else if(a==="mas10"){today();P.nw=(P.nw||0)-10;save();pick()}
      else if(a==="ahead"){const Q=queues(true);let best=null;for(const c of cards()){const p=P.c[c[3]];if(p&&p.q!==1&&(!best||p.d<P.c[best[3]].d))best=c}
        if(best){st.cur=best;st.curQ="l";st.show=false}else pick()}
      else if(a==="reset"){if(!st.sure){st.sure=true;redraw();return}cards().forEach(c=>delete P.c[c[3]]);st.undo=null;save();deal()}
      else if(a==="mas")st.lim+=100;
      else if(a==="qnext"){st.qi++;st.qa=-1}
      else if(a==="qrst")dealQ();
      redraw();
    });
    root.addEventListener("change",e=>{const k=e.target.dataset.k;if(k==="tema"){st.tema=e.target.value;st.lim=60;deal();dealQ();draw()}
      else if(k==="lim"){P.lim=+e.target.value;save();if(!st.show)pick();redraw()}});
    root.addEventListener("input",e=>{if(e.target.dataset.k==="q"){st.q=e.target.value;st.lim=60;redraw()}});
    const key=e=>{if(st.tab!=="repasar"||/INPUT|SELECT|TEXTAREA/.test((e.target||{}).tagName||""))return;
      if(e.key===" "||e.key==="Enter"){if(!st.cur)return;e.preventDefault();if(!st.show)st.show=true;else grade(2);redraw()}
      else if(st.show&&/^[1-4]$/.test(e.key)){grade(+e.key-1);redraw()}
      else if((e.key==="z"||e.key==="Z")&&st.undo){doUndo();redraw()}
      else if(e.key==="Escape"&&close)close()};
    document.addEventListener("keydown",key);
    deal();draw();
    return ()=>{clearTimeout(timer);document.removeEventListener("keydown",key)};
  }
  function start(){
    css();
    const host=document.getElementById("ak-root");
    if(host){load().then(()=>app(host,true,null)).catch(()=>{host.textContent="No se pudieron cargar las tarjetas."});return}
    const b=document.createElement("button");b.className="ak-fab";b.type="button";
    b.innerHTML=`Tus tarjetas de Anki${N?` <small>${N.toLocaleString("es-MX")}</small>`:""}`;
    b.onclick=()=>load().then(()=>{
      const ov=document.createElement("div");ov.className="ak-ov";ov.setAttribute("role","dialog");ov.setAttribute("aria-modal","true");
      let off=null;const close=()=>{off&&off();ov.remove();b.style.display=""};
      ov.addEventListener("click",e=>{if(e.target===ov)close()});
      document.body.appendChild(ov);b.style.display="none";off=app(ov,false,close);
    }).catch(()=>{b.textContent="No se pudieron cargar las tarjetas"});
    document.body.appendChild(b);
  }
  document.readyState==="loading"?document.addEventListener("DOMContentLoaded",start):start();
})();
