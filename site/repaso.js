/* Medicina UDLAP · «Qué repasar hoy»: junta las tarjetas que te tocan hoy de TODAS las materias
   (tarjetas de tus guías, tus tarjetas de Anki, las que hiciste tú y AnKing si ya pusiste su clave)
   y deja repasarlas seguidas o materia por materia.
   - Usa el mismo programador estilo Anki (anki/srs.js): el avance es el mismo que en cada guía, en su página
     de materia y en Estudio, y viaja Mac ↔ cel con sync.js (carrera-anki-*, carrera-repaso, carrera-srs-*).
   - Ajustes propios en carrera-repaso-hoy ({nuevas, anking}); también se sincronizan.
   - En la app toma los mazos de Estudio (Estudio.decks); en el artefacto (sin Estudio) arma los mazos
     con anki/<materia>.json (lista ANKI de abajo; la regenera tools-repaso/patch_repaso.py).
   - Ruta #repaso; tarjeta «Repaso de hoy» en «Tu día» de la portada. Respeta modo oscuro y Reducir movimiento. */
(()=>{
  if(window.Repaso)return;
  /* ===== utilidades ===== */
  const $=s=>document.querySelector(s);
  const get=k=>{try{return localStorage.getItem(k)}catch(e){return null}};
  const J=(k,d)=>{try{const v=JSON.parse(get(k)||"null");return v==null?d:v}catch(e){return d}};
  const S=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}};
  const esc=s=>String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const norm=t=>String(t||"").normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase().replace(/[^a-z0-9]+/g," ").trim();
  const nf=n=>Math.round(n).toLocaleString("es-MX");
  const pl=(n,a,b)=>n===1?a:b;
  const pad=n=>String(n).padStart(2,"0");
  const ymd=d=>d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate());
  const parseD=s=>{const [y,m,d]=s.split("-").map(Number);return new Date(y,m-1,d)};
  const diffD=(a,b)=>Math.round((parseD(b)-parseD(a))/864e5);
  const DIAS=["dom","lun","mar","mié","jue","vie","sáb"],MESES=["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"];
  const DAY=864e5;
  const CFGK="carrera-repaso-hoy",CK="carrera-anking-clave";
  const cfg=()=>Object.assign({nuevas:10,anking:true},J(CFGK,{}));
  const setCfg=o=>S(CFGK,Object.assign(cfg(),o));
  const hasKey=()=>!!(get(CK)||"").trim();

  /* tus mazos de Anki (para cuando no hay Estudio, como en el artefacto): [archivo, materia, semestre] */
  const ANKI=/*ANKI*/[["anatomia-humana-i","Anatomía Humana I",2],["anatomia","Anatomía",3],["bioetica","Bioética en Ciencias de la Salud",5],["campos-clinicos-i","Campos Clínicos I",5],["casos-clinicos-i","Casos Clínicos I",5],["casos-clinicos-ii","Casos Clínicos II",6],["cirugia-principios","Principios de cirugía",4],["cirugia","Cirugía",5],["ecosofia","Ecosofía",3],["enarm","ENARM",0],["examen-basicos","Examen de Conocimientos Básicos",4],["farmacologia-ii","Farmacología",4],["farmacologia","Farmacología",3],["gastro","Gastroenterología",5],["hematologia","Hematología",4],["imagenologia","Imagenología",5],["infectologia","Infectología",6],["inmunologia","Inmunología",4],["microbiologia","Microbiología y Parasitología",3],["nutricion","Nutrición",4],["oftalmo","Oftalmología",5],["otorrino","Otorrinolaringología",5],["salud-publica","Salud Pública",6],["simulacion-i","Simulación",1],["simulacion-ii","Simulación",2],["simulacion-iii","Simulación",3],["simulacion-iv","Simulación",4]]/*/ANKI*/;

  /* ===== carga: programador (srs.js), mazos normales y AnKing ===== */
  let srsP=null;
  function loadSRS(){
    if(window.SRS)return Promise.resolve(window.SRS);
    if(window.Estudio&&Estudio.ready)return Estudio.ready().then(()=>window.SRS||null);
    return srsP||(srsP=new Promise(ok=>{
      const old=document.querySelector('script[src$="anki/srs.js"]');
      if(old){const t=setInterval(()=>{if(window.SRS){clearInterval(t);ok(window.SRS)}},80);setTimeout(()=>{clearInterval(t);ok(window.SRS||null)},15000);return}
      const s=document.createElement("script");s.src="anki/srs.js";s.onload=()=>ok(window.SRS||null);s.onerror=()=>ok(null);document.head.appendChild(s)}));
  }
  let OWN=null,ownP=null;
  function ownDecks(){/* sin Estudio: un mazo por materia con tus tarjetas de Anki */
    if(OWN)return Promise.resolve(OWN);
    return ownP||(ownP=Promise.all(ANKI.map(([id,name,sem])=>fetch("anki/"+id+".json",{cache:"force-cache"}).then(r=>r.ok?r.json():null).catch(()=>null).then(d=>({id,name,sem,d}))))
      .then(rs=>{
        const by=new Map();
        for(const {id,name,sem,d} of rs){if(!d||!Array.isArray(d.c))continue;
          const st=SRS.deckStore(id),key=norm(name);let x=by.get(key);
          if(!x){x={id:"m:"+key,name,sem:sem||98,list:[],ids:[],st};by.set(key,x)}
          x.sem=Math.min(x.sem,sem||98);x.ids.push(id);
          d.c.forEach(c=>x.list.push({k:SRS.hash(c[1]+"|"+c[2]),st,f:c[1],b:c[2],t:c[0],deck:id,dn:d.n||name}))}
        return OWN=[...by.values()].map(x=>({id:x.id,name:x.name,sem:x.sem,group:x.sem<98?x.sem+"º semestre":"Otras",ids:x.ids,cards:()=>x.list,total:x.list.length,
          states:()=>x.list.map(c=>c.st.get(c.k)),newLim:()=>{const l=x.st.meta().lim;return l!=null?l:20},revLim:()=>x.st.meta().rlim||200,setLim:o=>x.ids.forEach(i=>SRS.deckStore(i).set(o))}))
          .sort((a,b)=>a.sem-b.sem||a.name.localeCompare(b.name,"es"));
      }));
  }
  function baseDecks(){
    if(window.Estudio&&Estudio.decks&&Estudio.ready)return Estudio.ready().then(()=>{
      const set=o=>{const c=J("carrera-estudio-ajustes",{})||{};if(o.lim!=null)c.nuevas=o.lim;if(o.rlim!=null)c.repasos=o.rlim;S("carrera-estudio-ajustes",c)};
      return Estudio.decks().map(d=>{const sem=d.sem>0&&d.sem<99?d.sem:98;return Object.assign({},d,{sem,group:sem<98?sem+"º semestre":d.group==="Tus tarjetas"?d.group:"Otras",setLim:set})})});
    return ownDecks();
  }
  /* AnKing: el conteo sale de tu avance guardado (sin descifrar); las tarjetas se descifran solo al repasarlas */
  let AKI=null;
  const akIndex=()=>AKI?Promise.resolve(AKI):fetch("anki/anking/index.json",{cache:"force-cache"}).then(r=>r.ok?r.json():[]).catch(()=>[]).then(x=>AKI=Array.isArray(x)?x:[]);
  let AKD=null,akP=null,akErr="";
  async function akDecrypt(t){
    const pass=(get(CK)||"").trim();if(!pass)throw new Error("nokey");
    const te=new TextEncoder(),ikm=await crypto.subtle.importKey("raw",te.encode(pass),"HKDF",false,["deriveKey"]);
    const key=await crypto.subtle.deriveKey({name:"HKDF",hash:"SHA-256",salt:te.encode("medicina-udlap/anking/v1"),info:te.encode("mazo")},ikm,{name:"AES-GCM",length:256},false,["decrypt"]);
    const u=Uint8Array.from(atob(t.trim()),c=>c.charCodeAt(0));let pt;
    try{pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:u.slice(0,12)},key,u.slice(12))}catch(e){throw new Error("badkey")}
    return JSON.parse(await new Response(new Blob([pt]).stream().pipeThrough(new DecompressionStream("gzip"))).text());
  }
  function akDecks(){
    if(AKD)return Promise.resolve(AKD);
    if(akP)return akP;akErr="";
    return akP=akIndex().then(async idx=>{
      const out=[];
      for(const m of idx){
        const t=await fetch("anki/anking/"+m.id+".txt",{cache:"force-cache"}).then(r=>{if(!r.ok)throw new Error("http");return r.text()});
        const d=await akDecrypt(t),id="anking-"+m.id,st=SRS.deckStore(id),P=st.meta();
        if(P.N!==d.c.length||P.name!==m.n)st.set({N:d.c.length,name:m.n});
        const list=d.c.map(c=>({k:SRS.hash(c[1]+"|"+c[2]),st,f:c[1],b:c[2],t:c[0],deck:id,dn:m.n}));
        out.push(akDeck(m,{cards:()=>list,total:list.length}));
      }
      return AKD=out;
    }).catch(e=>{akErr=e&&e.message||"err";akP=null;return null});
  }
  function akDeck(m,extra){
    const id="anking-"+m.id,st=SRS.deckStore(id);
    return Object.assign({id,name:m.n,sem:100,group:"AnKing en español",ids:[id],ak:m.id,store:st,total:m.c||0,
      states:()=>Object.values(st.all()),newLim:()=>{const l=st.meta().lim;return l!=null?l:20},revLim:()=>st.meta().rlim||200,setLim:o=>st.set(o)},extra||{});
  }
  /* cuántas te tocan hoy en un mazo AnKing, solo con tu avance (sin abrir el mazo) */
  function akCounts(d){
    const now=Date.now(),end=SRS.dayStart(now)+DAY,tk=SRS.dayKey(now),st=d.store,P=st.meta();
    let r=0,l=0,seen=0;
    for(const p of Object.values(st.all())){if(!p||p.nw)continue;seen++;if(p.sp||p.bu===tk)continue;
      if(p.q!==1){if(p.d<end)l++}else if(p.d<end)r++}
    const t=SRS.today(d.ids),total=Math.max(P.N||0,d.total||0);
    return {n:Math.max(0,Math.min(d.newLim()-t.nw,total-seen)),l,r:Math.min(r,Math.max(0,d.revLim()-t.rv)),total};
  }
  const counts=d=>d.cards?SRS.deckCounts(d):akCounts(d);

  /* ===== exámenes próximos (del Calendario) ===== */
  function exams(){
    const c=J("carrera-calendario",{})||{},t=ymd(new Date());
    return (Array.isArray(c.exams)?c.exams:[]).filter(e=>e&&e.name&&e.date>=t&&diffD(t,e.date)<=14).sort((a,b)=>a.date.localeCompare(b.date));
  }
  function examFor(d,ex){
    const n=norm(d.name);if(!n)return null;
    for(const e of ex){const m=window.Estudio&&Estudio.examMat?Estudio.examMat(e):"";
      if(m?norm(m)===n:norm(e.name).includes(n))return e}
    return null;
  }

  /* ===== modelo: filas por materia ===== */
  let BASE=null,AKS=null,ROWS=[],loading=false,loaded=false;
  async function load(){
    if(loading)return;loading=true;
    try{
      const SRS=await loadSRS();if(!SRS){loading=false;return}
      const [b,idx]=await Promise.all([baseDecks(),akIndex()]);
      BASE=b||[];AKS=AKD||idx.map(m=>akDeck(m));loaded=true;
    }catch(e){}
    loading=false;compute();
  }
  function compute(){
    if(!loaded)return;
    const ex=exams(),useAK=hasKey()&&cfg().anking,t=ymd(new Date());
    ROWS=BASE.concat(useAK?AKS:[]).map(d=>{const k=counts(d),e=d.ak?null:examFor(d,ex);return {d,k,due:k.r+k.l,e,ed:e?diffD(t,e.date):99}});
    ROWS.sort((a,b)=>(a.ed-b.ed)||((b.due>0)-(a.due>0))||(a.d.sem-b.d.sem)||a.d.name.localeCompare(b.d.name,"es"));
  }
  const tot=()=>ROWS.reduce((a,x)=>{a.r+=x.k.r;a.l+=x.k.l;a.n+=x.k.n;if(x.due)a.m++;return a},{r:0,l:0,n:0,m:0});
  function secsPerCard(){/* tu ritmo real de los últimos 30 días; si no hay, 8 s */
    const D=(J("carrera-srs-dias",{})||{}).d||{},lim=ymd(new Date(Date.now()-30*DAY));let n=0,ms=0;
    for(const k in D){if(k<lim)continue;for(const m in D[k]){const r=D[k][m];n+=r[0]+r[1]+r[2]+r[3];ms+=r[4]}}
    return n>=20?Math.min(40,Math.max(3,ms/n/1000)):8;
  }
  const mins=n=>{const m=Math.max(1,Math.round(n*secsPerCard()/60));return m<60?m+" min":Math.floor(m/60)+" h"+(m%60?" "+m%60+" min":"")};
  function forecast(){/* repasos de los próximos 7 días (sin contar hoy) */
    const t0=SRS.dayStart(Date.now()),f=[0,0,0,0,0,0,0],useAK=hasKey()&&cfg().anking;
    for(const d of BASE.concat(useAK?AKS:[]))for(const p of d.states()){if(!p||p.nw||p.sp||p.q!==1)continue;const i=Math.floor((SRS.dayStart(p.d)-t0)/DAY);if(i>=1&&i<=7)f[i-1]++}
    return f;
  }

  /* ===== estilos (usa los colores de la portada: verde/naranja UDLAP y su modo oscuro) ===== */
  const CSS=`
#repaso .rp-hero{display:flex;gap:22px;align-items:center;flex-wrap:wrap}
#repaso .rp-big{font:900 3.4rem/1 var(--f-display);font-stretch:80%;letter-spacing:-.02em}
#repaso .rp-hero .gh-kick{margin-bottom:4px}
#repaso .rp-sub{margin:6px 0 0;color:var(--on-green-mut,rgba(255,255,255,.75));font-size:.95rem}
#repaso .rp-sub b{color:#fff}
#repaso .rp-hi{flex:1;min-width:220px}
#repaso .rp-go{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
#repaso .rp-go .cbtn{font-size:1rem;padding:13px 22px;border-radius:12px}
#repaso .rp-go .cbtn[disabled]{opacity:.5;cursor:default}
#repaso .rp-opts{display:flex;gap:10px 18px;flex-wrap:wrap;align-items:center;margin-top:14px;font-size:.85rem;color:var(--on-green-mut,rgba(255,255,255,.75))}
#repaso .rp-seg{display:inline-flex;border:1px solid rgba(255,255,255,.28);border-radius:999px;overflow:hidden;margin-left:6px;vertical-align:middle}
#repaso .rp-seg button{border:0;background:transparent;color:#fff;font:700 .8rem var(--f-mono);padding:5px 10px;cursor:pointer}
#repaso .rp-seg button[aria-pressed="true"]{background:var(--orange);color:#fff}
#repaso .rp-tg{display:inline-flex;gap:7px;align-items:center;cursor:pointer;color:#fff}
#repaso .rp-tg input{accent-color:var(--orange);width:16px;height:16px}
#repaso .rp-ex{margin:0 0 14px;padding:10px 14px;border-radius:12px;background:color-mix(in srgb,var(--orange) 12%,var(--paper));border:1px solid color-mix(in srgb,var(--orange) 40%,var(--line));color:var(--ink);font-size:.9rem}
#repaso .rp-grid{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:18px;align-items:start}
#repaso h3{margin:0 0 10px;font:800 1.05rem var(--f-display)}
#repaso h3 small{font:600 .72rem var(--f-mono);color:var(--muted);letter-spacing:.06em;margin-left:6px}
#repaso .rp-list{display:grid;gap:6px}
#repaso .rp-g{margin:12px 0 2px;font:700 .66rem var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
#repaso .rp-row{display:flex;gap:10px;align-items:center;width:100%;text-align:left;border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:12px;padding:10px 12px;font:inherit;cursor:pointer}
#repaso .rp-row:hover{border-color:color-mix(in srgb,var(--orange) 50%,var(--line))}
#repaso .rp-row:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
#repaso .rp-nm{flex:1;min-width:0}
#repaso .rp-nm b{display:block;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#repaso .rp-nm small{display:block;font-size:.74rem;color:var(--muted)}
#repaso .rp-nm small.hot{color:var(--orange-2,var(--orange));font-weight:700}
#repaso .rp-c{display:flex;gap:5px;flex:none}
#repaso .rp-c span{min-width:34px;text-align:center;border-radius:8px;padding:3px 6px;font:800 .8rem var(--f-mono)}
#repaso .rp-c .n{color:#2563eb;background:rgba(37,99,235,.09)}
#repaso .rp-c .l{color:#c2410c;background:rgba(194,65,12,.09)}
#repaso .rp-c .r{color:#15803d;background:rgba(21,128,61,.10)}
#repaso .rp-c .z{opacity:.35;background:transparent}
#repaso .rp-leg{display:flex;gap:12px;flex-wrap:wrap;font-size:.74rem;color:var(--muted);margin:2px 0 8px}
#repaso .rp-leg i{display:inline-block;width:9px;height:9px;border-radius:3px;margin-right:5px;vertical-align:-1px}
#repaso details.rp-ok{margin-top:10px}
#repaso details.rp-ok summary{cursor:pointer;color:var(--muted);font-size:.86rem;padding:6px 2px}
#repaso .rp-fc{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;align-items:end;height:120px;margin-top:6px}
#repaso .rp-fc div{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:4px;font:600 .68rem var(--f-mono);color:var(--muted)}
#repaso .rp-fc i{display:block;width:100%;max-width:30px;border-radius:6px 6px 3px 3px;background:linear-gradient(180deg,var(--green-3,#0a7a55),var(--green,#00573c));min-height:3px}
#repaso .rp-fc b{color:var(--ink);font:800 .72rem var(--f-mono)}
#repaso .rp-note{font-size:.82rem;color:var(--muted);line-height:1.45;margin:10px 0 0}
#repaso .rp-rv{max-width:900px;margin:0 auto}
#repaso .rp-rv .srs{border-radius:14px;overflow:hidden;box-shadow:var(--shadow)}
#repaso .rp-msg{text-align:center;color:var(--muted);padding:30px 10px}
:root[data-theme="dark"] #repaso .rp-c .n{color:#93b4ff;background:rgba(147,180,255,.12)}
:root[data-theme="dark"] #repaso .rp-c .l{color:#ffb38a;background:rgba(255,179,138,.12)}
:root[data-theme="dark"] #repaso .rp-c .r{color:#7cf0b6;background:rgba(124,240,182,.12)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) #repaso .rp-c .n{color:#93b4ff;background:rgba(147,180,255,.12)}:root:not([data-theme="light"]) #repaso .rp-c .l{color:#ffb38a;background:rgba(255,179,138,.12)}:root:not([data-theme="light"]) #repaso .rp-c .r{color:#7cf0b6;background:rgba(124,240,182,.12)}}
@media (max-width:760px){#repaso .rp-grid{grid-template-columns:minmax(0,1fr)}#repaso .rp-big{font-size:2.8rem}#repaso .rp-go .cbtn{flex:1}}
@media (max-width:420px){#repaso .rp-c span{min-width:28px;padding:3px 4px;font-size:.74rem}}
/* tarjeta en «Tu día» de la portada */
.rp-strip{display:flex;gap:12px;align-items:center;margin-top:10px;padding:10px 14px;border-radius:16px;text-decoration:none;color:var(--ink);background:color-mix(in srgb,var(--orange) 8%,var(--paper));border:1px solid color-mix(in srgb,var(--orange) 35%,var(--line));transition:background .15s,border-color .15s}
.rp-strip:hover{background:color-mix(in srgb,var(--orange) 14%,var(--paper));border-color:var(--orange)}
.rp-strip:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
.rp-strip>b{flex:none;min-width:46px;height:46px;padding:0 6px;border-radius:12px;display:grid;place-items:center;font:900 1.4rem/1 var(--f-display);font-stretch:80%;background:var(--orange);color:#fff}
.rp-strip.ok>b{background:linear-gradient(150deg,var(--green-3),var(--green-2))}
.rp-strip>span{flex:1;min-width:0}
.rp-strip small{display:block;font:700 .6rem var(--f-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.rp-strip em{display:block;margin-top:2px;font-style:normal;font-weight:700;font-size:.9rem;line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rp-strip i{flex:none;font-style:normal;font:800 .82rem var(--f-display);color:var(--orange-2,var(--orange));white-space:nowrap}
.rp-strip.solo{max-width:1100px;margin:14px auto 0}
@media (max-width:560px){.rp-strip{padding:9px;gap:9px;border-radius:14px}.rp-strip>b{min-width:38px;height:38px;font-size:1.15rem;border-radius:10px}.rp-strip em{font-size:.8rem}.rp-strip i span{display:none}}
@media (prefers-reduced-motion:no-preference){#repaso:not([hidden]) .cal-body>.in{animation:rpIn .28s ease-out}@keyframes rpIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}}
@media (prefers-reduced-motion:reduce){.rp-strip{transition:none}}
`;
  const ICO=`<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6" width="14" height="14" rx="2"/><path d="M7 3h12a2 2 0 0 1 2 2v12"/><path d="M7 13l2.5 2.5L14 11"/></svg>`;
  const html=`<div class="cal" id="repaso" hidden role="dialog" aria-modal="true" aria-labelledby="rpTtl">
  <div class="vbar gut"><a class="vbtn" href="#" id="rpBack"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg><span class="lbl">Inicio</span></a>
    <div class="ttl" id="rpTtl">${ICO}Qué repasar hoy</div></div>
  <div class="cal-body gut"><div class="in" id="rpIn"></div></div></div>`;

  /* ===== pantalla ===== */
  let ready=false,rv=null,mode="list",lastY=0;
  function mount(){
    if(ready)return;ready=true;
    const st=document.createElement("style");st.id="rpCss";st.textContent=CSS;document.head.appendChild(st);
    document.body.insertAdjacentHTML("beforeend",html);
    $("#rpBack").addEventListener("click",ev=>{ev.preventDefault();if(mode!=="list"){toList();return}goHome()});
    $("#rpIn").addEventListener("click",onClick);
    $("#rpIn").addEventListener("change",ev=>{const t=ev.target;if(t.dataset.rp==="ak"){setCfg({anking:t.checked});compute();draw()}});
    document.addEventListener("keydown",ev=>{if(ev.key==="Escape"&&!$("#repaso").hidden&&!document.querySelector("#repaso .srs-menu")&&!/^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement||{}).tagName||"")){ev.preventDefault();if(mode!=="list")toList();else goHome()}});
  }
  const goHome=()=>{close();if(typeof go==="function")go("");else location.hash=""};/* go("") usa pushState: no avisa con hashchange */
  function open(){
    mount();if(!$("#repaso").hidden)return;
    lastY=window.scrollY;mode="list";
    $("#repaso").hidden=false;document.documentElement.style.overflow="hidden";document.title="Qué repasar hoy · Carrera de Medicina";
    if(window.SRS)SRS.reloadAll();
    compute();draw();load().then(draw);
  }
  function close(){
    if(!ready||$("#repaso").hidden)return;
    if(rv){rv.destroy();rv=null}mode="list";
    $("#repaso").hidden=true;document.documentElement.style.overflow="";document.title="Carrera de Medicina";
    requestAnimationFrame(()=>window.scrollTo(0,lastY));strip();
  }
  function toList(){if(rv){rv.destroy();rv=null}mode="list";if(window.SRS)SRS.reloadAll();compute();draw();$("#repaso .cal-body").scrollTop=0}
  function draw(){
    if(!ready||$("#repaso").hidden||mode!=="list")return;
    const box=$("#rpIn"),now=new Date();
    if(!loaded){box.innerHTML=`<section class="gr-hero"><p class="gh-kick">${DIAS[now.getDay()]} ${now.getDate()} de ${MESES[now.getMonth()]}</p><div class="rp-big">…</div><p class="rp-sub">Juntando tus tarjetas de todas las materias…</p></section>`;return}
    const T=tot(),due=T.r+T.l,c=cfg(),nNew=Math.min(c.nuevas,T.n),ex=exams(),exR=ROWS.filter(x=>x.e&&x.due),keyed=hasKey();
    const fc=forecast(),fmx=Math.max(1,...fc);
    const row=x=>{const k=x.k,z=v=>v?"":" z";
      return `<button class="rp-row" type="button" data-deck="${esc(x.d.id)}"><span class="rp-nm"><b>${esc(x.d.name)}</b>${x.e?`<small class="hot">Examen ${x.ed===0?"hoy":x.ed===1?"mañana":"en "+x.ed+" días"}</small>`:`<small>${nf(k.total||x.d.total||0)} tarjetas</small>`}</span>
        <span class="rp-c"><span class="r${z(k.r)}" title="Por repasar">${k.r}</span><span class="l${z(k.l)}" title="Aprendiendo">${k.l}</span><span class="n${z(k.n)}" title="Nuevas">${k.n}</span></span></button>`};
    const act=ROWS.filter(x=>x.due),idle=ROWS.filter(x=>!x.due);
    let grp=null;const list=act.map(x=>{let h="";const g=x.e?"Con examen pronto":x.d.group;if(g!==grp){grp=g;h=`<p class="rp-g">${esc(g)}</p>`}return h+row(x)}).join("");
    box.innerHTML=`<section class="gr-hero"><div class="rp-hero"><div class="rp-hi">
        <p class="gh-kick">${DIAS[now.getDay()]} ${now.getDate()} de ${MESES[now.getMonth()]} · todas tus materias</p>
        <div class="rp-big">${nf(due)}</div>
        <p class="rp-sub">${due?`${pl(due,"tarjeta te toca","tarjetas te tocan")} hoy en <b>${T.m}</b> ${pl(T.m,"materia","materias")}${T.l?` (${nf(T.l)} aprendiendo)`:""}. Con ${nNew?nNew+" nuevas":"0 nuevas"}: ≈ <b>${mins(due+nNew)}</b>.`:"Vas al día: hoy no vence nada."+(T.n?` Puedes adelantar con nuevas.`:"")}</p></div>
      <div class="rp-go"><button class="cbtn" type="button" data-rp="all" ${due+nNew?"":"disabled"}>Repasar todo seguido</button></div></div>
      <div class="rp-opts"><span>Nuevas mezcladas<span class="rp-seg" role="group" aria-label="Nuevas mezcladas">${[0,10,20,50].map(v=>`<button type="button" data-rp="new" data-v="${v}" aria-pressed="${v===c.nuevas}">${v}</button>`).join("")}</span></span>
        ${keyed?`<label class="rp-tg"><input type="checkbox" data-rp="ak" ${c.anking?"checked":""}>Incluir AnKing</label>`:""}</div></section>
      ${exR.length?`<p class="rp-ex"><b>Examen pronto:</b> ${exR.slice(0,3).map(x=>`${esc(x.d.name)} (${x.ed===0?"hoy":x.ed===1?"mañana":"en "+x.ed+" días"})`).join(", ")}. Sus tarjetas salen primero en la lista.</p>`:""}
      <div class="rp-grid"><section class="ccard"><h3>Por materia <small>toca una para repasar solo esa</small></h3>
        <div class="rp-leg"><span><i style="background:#15803d"></i>Por repasar</span><span><i style="background:#c2410c"></i>Aprendiendo</span><span><i style="background:#2563eb"></i>Nuevas disponibles</span></div>
        <div class="rp-list">${list||`<p class="rp-msg">Nada vence hoy. ¡Bien!</p>`}</div>
        ${idle.length?`<details class="rp-ok"><summary>Al día (${idle.length} ${pl(idle.length,"mazo","mazos")})</summary><div class="rp-list">${idle.map(row).join("")}</div></details>`:""}</section>
      <section class="ccard"><h3>Próximos 7 días</h3>
        <div class="rp-fc" role="img" aria-label="Repasos de los próximos 7 días">${fc.map((v,i)=>{const d=new Date(Date.now()+(i+1)*DAY);return `<div><b>${v}</b><i style="height:${Math.round(v/fmx*80)}%"></i>${i===0?"mañ":DIAS[d.getDay()]}</div>`}).join("")}</div>
        <p class="rp-note">Cuántas tarjetas ya vistas te tocan cada día (sin contar las nuevas que agregues). Repasar hoy evita que se junten.</p>
        <p class="rp-note">Es el mismo avance que en cada guía${window.Estudio?" y en Estudio":""}: lo que repases aquí cuenta allá y se sincroniza con tus otros aparatos.${keyed?"":` Para sumar AnKing, abre su mazo una vez y pon la clave.`}</p></section></div>`;
  }
  async function onClick(ev){
    const b=ev.target.closest("[data-rp],[data-deck]");if(!b)return;
    if(b.dataset.rp==="new"){setCfg({nuevas:+b.dataset.v});draw();return}
    if(b.dataset.rp==="all"){startAll();return}
    if(b.dataset.deck){const x=ROWS.find(r=>r.d.id===b.dataset.deck);if(x)startDeck(x.d)}
  }
  function host(msg){mode="rv";const box=$("#rpIn");box.innerHTML=`<div class="rp-rv">${msg?`<p class="rp-msg">${esc(msg)}</p>`:""}</div>`;$("#repaso .cal-body").scrollTop=0;return box.firstChild}
  /* AnKing: descifrar solo cuando de verdad toca repasarlo */
  async function needAK(rows){
    if(!rows.some(x=>x.d.ak&&!x.d.cards))return true;
    host("Abriendo AnKing… (puede tardar unos segundos)");
    const ak=await akDecks();
    if(!ak){host(akErr==="badkey"?"La clave de AnKing guardada no abre el mazo. Revísala en el mazo AnKing.":"No pude abrir AnKing. Revisa tu conexión e inténtalo otra vez.");return false}
    AKS=ak;compute();return true;
  }
  async function startDeck(d){
    if(d.ak&&!d.cards){if(!await needAK([{d}]))return;d=AKS.find(x=>x.id===d.id);if(!d)return}
    const h=host("");
    rv=SRS.reviewer(h,{title:()=>d.name,cards:d.cards,ids:d.ids,newLim:d.newLim,revLim:d.revLim,setLim:o=>d.setLim&&d.setLim(o),shuffleNew:!!d.ak,
      onBack:toList,back:"Qué repasar hoy"});
    if(SRS.deckCounts(d).r+SRS.deckCounts(d).l+SRS.deckCounts(d).n)rv.study();
  }
  async function startAll(){
    const c=cfg();if(!await needAK(ROWS.filter(x=>x.due||(c.nuevas&&x.k.n))))return;
    /* lo que vence en cada materia (respetando sus límites) + nuevas repartidas por turnos, primero las de examen pronto */
    const now=Date.now(),list=[],ids=new Set(),pools=[];
    for(const x of ROWS){const d=x.d;if(!d.cards)continue;d.ids.forEach(i=>ids.add(i));
      const Q=SRS.queues(d.cards(),{ids:d.ids,newLim:d.newLim,revLim:d.revLim,rnd:()=>0,shuffleNew:!!d.ak},now);
      const tag=c=>Object.assign({},c,{t:d.name+(c.t?" · "+c.t:"")});/* en el repaso de todo, la materia va arriba de cada tarjeta */
      list.push(...Q.L.map(tag),...Q.La.map(tag),...Q.R.map(tag));if(Q.N.length)pools.push(Q.N.map(tag))}
    let left=c.nuevas;while(left>0&&pools.some(p=>p.length))for(const p of pools){if(left<=0)break;const x=p.shift();if(x){list.push(x);left--}}
    if(!list.length){toList();return}
    const h=host("");
    rv=SRS.reviewer(h,{title:()=>"Todo lo de hoy",cards:()=>list,ids:[...ids],newLim:()=>99999,revLim:()=>99999,setLim:()=>{},shuffleNew:true,
      onBack:toList,back:"Qué repasar hoy"});
    rv.study();
  }

  /* ===== tarjeta en la portada («Tu día») ===== */
  let stripT=0;
  function strip(){
    clearTimeout(stripT);
    stripT=setTimeout(()=>{
      if(!loaded){load().then(paintStrip);return}
      if(window.SRS)SRS.reloadAll();compute();paintStrip();
    },loaded?60:1200);
  }
  function paintStrip(){
    let a=document.getElementById("rpStrip");
    if(!a){
      a=document.createElement("a");a.id="rpStrip";a.className="rp-strip";a.href="#repaso";
      const hd=document.querySelector("#homeToday .hd-k");
      if(hd)hd.insertAdjacentElement("afterend",a);
      else{const band=document.querySelector("section.band");if(!band)return;a.classList.add("solo");band.insertAdjacentElement("afterend",a)}
    }
    if(!loaded){a.innerHTML=`<b>…</b><span><small>Repaso de hoy</small><em>Juntando tus tarjetas…</em></span>`;return}
    const T=tot(),due=T.r+T.l,top=ROWS.filter(x=>x.due).slice(0,3).map(x=>x.d.name);
    a.classList.toggle("ok",!due);
    a.innerHTML=`<b>${due>999?Math.round(due/100)/10+"k":due}</b><span><small>Repaso de hoy · todas las materias</small><em>${due?`${nf(due)} ${pl(due,"tarjeta","tarjetas")} en ${T.m} ${pl(T.m,"materia","materias")} · ≈ ${mins(due)}${top.length?" · "+esc(top.join(", ")):""}`:`Vas al día${T.n?` · ${nf(T.n)} nuevas disponibles`:""}`}</em></span><i><span>${due?"Repasar":"Ver"} </span>›</i>`;
    a.setAttribute("aria-label",due?`Repaso de hoy: ${due} tarjetas en ${T.m} materias`:"Repaso de hoy: vas al día");
  }

  /* ===== ruta y arranque ===== */
  function route(){if(location.hash==="#repaso")open();else close()}
  function boot(){
    if(!document.getElementById("rpCss")){const st=document.createElement("style");st.id="rpCss";st.textContent=CSS;document.head.appendChild(st)}
    if(document.querySelector("#homeToday,section.band"))strip();
    route();
  }
  addEventListener("hashchange",route);addEventListener("popstate",route);
  /* lo que llega de tus otros aparatos (sync.js) o de otra pestaña */
  addEventListener("storage",ev=>{if(!ev.key||!/^carrera-(anki-|repaso|srs-|calendario|anking-clave|estudio-ajustes)/.test(ev.key))return;
    if(ev.key===CK){AKD=null;akP=null}
    if(window.SRS)SRS.reloadAll();if(loaded){compute();paintStrip();draw()}});
  document.addEventListener("visibilitychange",()=>{if(document.visibilityState==="visible"&&loaded){if(window.SRS)SRS.reloadAll();compute();paintStrip();draw()}});
  window.Repaso={open,close,refresh:()=>{if(window.SRS)SRS.reloadAll();compute();paintStrip();draw()}};
  if(document.readyState==="loading")addEventListener("DOMContentLoaded",boot);else boot();
})();
