/* Medicina UDLAP · Estudio: tarjetas con repetición espaciada, modo examen, contador de estudio (Pomodoro)
   y notas rápidas por clase. También agrega a Calificaciones la calculadora "¿Cuánto necesito sacar?".
   Todo se guarda en este aparato (localStorage) y sync.js lo copia cifrado a tus otros aparatos.
   Las tarjetas y preguntas "de tus guías" salen de estudio-banco.json (lo arma tools-estudio/banco.js). */
(()=>{
  if(window.Estudio)return;
  /* ===== utilidades ===== */
  const get=k=>{try{return localStorage.getItem(k)}catch(e){return null}},set=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}};
  const J=(k,d)=>{try{const v=JSON.parse(get(k)||"null");return v==null?d:v}catch(e){return d}};
  const list=k=>{const v=J(k,null);return v&&Array.isArray(v.items)?v.items.filter(x=>x&&x.id!=null):[]};
  const saveList=(k,items,extra)=>set(k,JSON.stringify(Object.assign({},extra||{},{items})));
  const esc=s=>String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const norm=t=>String(t||"").normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase().replace(/[^a-z0-9]+/g," ").trim();
  const pad=n=>String(n).padStart(2,"0");
  const ymd=d=>d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate());
  const today=()=>ymd(new Date());
  const parseD=s=>{const [y,m,d]=s.split("-").map(Number);return new Date(y,m-1,d)};
  const addD=(s,n)=>{const d=parseD(s);d.setDate(d.getDate()+n);return ymd(d)};
  const diffD=(a,b)=>Math.round((parseD(b)-parseD(a))/864e5);
  const MES=["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
  const nice=s=>{const d=parseD(s);return d.getDate()+" "+MES[d.getMonth()]};
  const uid=p=>p+Date.now().toString(36)+Math.random().toString(36).slice(2,6);
  const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
  const mmss=s=>{s=Math.max(0,Math.round(s));return Math.floor(s/60)+":"+pad(s%60)};
  const hm=m=>{m=Math.round(m);return m<60?m+" min":Math.floor(m/60)+" h"+(m%60?" "+(m%60)+" min":"")};
  const pct=(a,b)=>b?Math.round(a/b*100):0;

  const K={cards:"carrera-tarjetas",prog:"carrera-repaso",qs:"carrera-preguntas",qprog:"carrera-preguntas-prog",sims:"carrera-simulacros",time:"carrera-estudio-tiempo",notes:"carrera-notas",parc:"carrera-parciales",cfg:"carrera-estudio-ajustes",tab:"carrera-fold-estudio-tab"};
  const POMO="__medsync_pomo"; /* contador en marcha: solo en este aparato */
  const cfg=()=>Object.assign({nuevas:20,repasos:200,foco:25,descanso:5},J(K.cfg,{}));

  /* ===== materias ===== */
  const CUR=()=>typeof CURSO!=="undefined"?CURSO.materias.map(m=>m.n):[];
  const GUIDES=()=>typeof G!=="undefined"?G:[];
  let BANK=null,bankP=null;
  function loadBank(){
    if(BANK)return Promise.resolve(BANK);
    if(!bankP)bankP=fetch("estudio-banco.json",{cache:"force-cache"}).then(r=>r.ok?r.json():null).catch(()=>null).then(b=>{
      const g=b&&Array.isArray(b.g)?b.g:[];
      BANK={g,c:(b&&b.c||[]).map(x=>({id:x[0],mat:(g[x[1]]||[])[1]||"",gid:(g[x[1]]||[])[0]||"",t:x[2],f:x[3],b:x[4],src:x[5]==="a"?"anki":"guia"})),
        q:(b&&b.q||[]).map(x=>({id:x[0],mat:(g[x[1]]||[])[1]||"",gid:(g[x[1]]||[])[0]||"",t:x[2],q:x[3],o:x[4],a:x[5],e:x[6],src:x[7]==="a"?"anki":"guia"}))};
      /* guías que no traen tarjetas (solo preguntas): sus preguntas también sirven como tarjetas */
      const withCards=new Set(BANK.c.map(c=>c.gid));
      BANK.q.filter(q=>!withCards.has(q.gid)).forEach(q=>BANK.c.push({id:"x"+q.id,mat:q.mat,gid:q.gid,t:q.t,f:q.q,b:q.o[q.a]+(q.e?" · "+q.e:""),src:"guia"}));
      return BANK});
    return bankP;
  }
  const myCards=()=>list(K.cards).filter(x=>x.f&&x.b);
  const myQs=()=>list(K.qs).filter(x=>x.q&&Array.isArray(x.o)&&x.o.length>1);
  const allCards=()=>(BANK?BANK.c:[]).concat(myCards());
  const allQs=()=>(BANK?BANK.q:[]).concat(myQs());
  function materias(){
    const s=new Map();const add=m=>{m=String(m||"").trim();if(m&&!s.has(norm(m)))s.set(norm(m),m)};
    CUR().forEach(add);(BANK?BANK.g.map(g=>g[1]):[]).forEach(add);myCards().forEach(x=>add(x.mat));myQs().forEach(x=>add(x.mat));
    list("carrera-horario").forEach(x=>add(x.mat));
    return [...s.values()];
  }
  const sameMat=(a,b)=>!b||norm(a)===norm(b);
  /* examen del calendario → materia (por la guía que le pusiste o por el nombre) */
  function examMat(e){
    if(e.guide){const g=GUIDES().find(x=>x.id===e.guide);if(g){const b=BANK&&BANK.g.find(x=>x[0]===g.id);return b?b[1]:g.area}}
    const n=norm(e.name);return materias().filter(m=>n.includes(norm(m))).sort((a,b)=>b.length-a.length)[0]||"";
  }
  const upcoming=()=>{const t=today();const c=J("carrera-calendario",{});return (Array.isArray(c.exams)?c.exams:[]).filter(e=>e&&e.date>=t&&e.name).sort((a,b)=>a.date.localeCompare(b.date))};

  /* ===== tarjetas: el mismo programador estilo Anki que las guías (anki/srs.js) =====
     Las tarjetas "de tu Anki" comparten avance con el botón "Tus tarjetas de Anki" de cada guía (carrera-anki-<mazo>);
     las de tus guías y las tuyas siguen en carrera-repaso. Historial y estadísticas: carrera-srs-log / carrera-srs-dias. */
  let srsP=null;
  const loadSRS=()=>window.SRS?Promise.resolve(window.SRS):srsP||(srsP=new Promise(ok=>{const s=document.createElement("script");s.src="anki/srs.js";s.onload=()=>ok(window.SRS||null);s.onerror=()=>ok(null);document.head.appendChild(s)}));
  let DK=null,DKsig="";
  function decks(){/* un mazo por materia, como en la pantalla principal de Anki */
    if(!window.SRS||!BANK)return [];
    const sig=BANK.c.length+":"+myCards().length+":"+myCards().map(c=>c.id).join(",").length;if(DK&&DKsig===sig)return DK;
    const R=SRS.repasoStore(),by=new Map(),semOf=new Map(),gname=new Map();
    BANK.g.forEach(g=>{gname.set(g[0],g[1]);const k=norm(g[1]);semOf.set(k,Math.min(semOf.has(k)?semOf.get(k):99,g[2]||99))});
    const mine=myCards().map(c=>Object.assign({src:"mia"},c));
    for(const c of mine.concat(BANK.c)){const key=norm(c.mat)||"sin materia";let d=by.get(key);
      if(!d){d={id:"m:"+key,name:c.mat||"Sin materia",list:[],ids:new Set()};by.set(key,d)}
      let x;
      if(c.src==="anki"&&String(c.gid).startsWith("anki-")){const M=c.gid.slice(5);x={k:SRS.hash(c.f+"|"+c.b),st:SRS.deckStore(M),f:c.f,b:c.b,t:c.t,deck:M,dn:gname.get(c.gid)||c.mat}}
      else{const id=c.gid?"g-"+c.gid:"mia-"+key.replace(/ /g,"-");x={k:c.id,st:R,f:c.f,b:c.b,t:c.t,deck:id,dn:c.gid?(c.mat+" · guía"):(c.mat+" · tuyas")}}
      d.ids.add(x.deck);d.list.push(x)}
    DK=[...by.values()].map(d=>{const sem=semOf.has(norm(d.name))?semOf.get(norm(d.name)):99,ids=[...d.ids];
      return {id:d.id,name:d.name,sem,group:sem<99?sem+"º semestre":"Tus tarjetas",ids,cards:()=>d.list,total:d.list.length,states:()=>d.list.map(x=>x.st.get(x.k)),
        newLim:()=>cfg().nuevas,revLim:()=>cfg().repasos||200}})
      .sort((a,b)=>a.sem-b.sem||a.name.localeCompare(b.name,"es"));
    DKsig=sig;return DK;
  }
  const deckOf=m=>m?decks().find(d=>norm(d.name)===norm(m)):null;
  function setLim(o){const c=cfg();if(o.lim!=null)c.nuevas=o.lim;if(o.rlim!=null)c.repasos=o.rlim;set(K.cfg,JSON.stringify(c));const s=$("#esNew");if(s)s.value=String(c.nuevas)}
  function dueInfo(m){
    let due=0,nw=0,total=0,learned=0;
    for(const d of decks()){if(m&&norm(d.name)!==norm(m))continue;const k=SRS.deckCounts(d);due+=k.r+k.l;nw+=k.n;total+=k.total;
      for(const p of d.states())if(p&&!p.nw&&p.q===1&&p.i>=21)learned++}
    return {total,due,nw,learned,newLeft:nw};
  }

  /* ===== estilos ===== */
  const css=`
#estudio .es-tabs{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 16px}
#estudio .es-tab{border:1.5px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;padding:9px 16px;font:800 .9rem var(--f-display);cursor:pointer;display:inline-flex;gap:7px;align-items:center}
#estudio .es-tab svg{width:17px;height:17px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
#estudio .es-tab[aria-selected="true"]{background:var(--green);border-color:var(--green);color:#fff}
#estudio .es-tab b{background:var(--orange);color:#fff;border-radius:999px;font-size:.72rem;padding:1px 7px}
#estudio .es-mats{display:flex;gap:6px;overflow-x:auto;padding:2px 0 12px;margin-bottom:6px;scrollbar-width:thin}
#estudio .es-chip{flex:none;border:1px solid var(--line);background:transparent;color:var(--ink);border-radius:999px;padding:6px 12px;font:600 .82rem var(--f-display);cursor:pointer;white-space:nowrap}
#estudio .es-chip[aria-pressed="true"]{background:var(--orange);border-color:var(--orange);color:#fff}
#estudio .es-hero{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;align-items:end}
#estudio .es-hero .gh-kick{grid-column:1/-1;margin:0;font:600 .72rem var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:#ffb98f}
#estudio .es-k{min-width:0}#estudio .es-k b{display:block;font:900 clamp(1.7rem,3.6vw,2.5rem)/1 var(--f-display);font-stretch:85%}
#estudio .es-k span{display:block;font-size:.8rem;color:#cfe5da;margin-top:4px}
#estudio .es-next{grid-column:1/-1;margin:4px 0 0;font-size:.92rem;color:#e7f3ec}#estudio .es-next b{color:#ffb98f}
#estudio .es-pane[hidden]{display:none}
#estudio .es-modo{display:flex;gap:6px;margin:0 0 12px;padding:4px;border-radius:14px;background:color-mix(in srgb,var(--line) 55%,transparent)}
#estudio .es-modo button{flex:1;border:0;background:transparent;color:var(--ink);font:800 .88rem var(--f-display);padding:10px 8px;border-radius:10px;cursor:pointer}
#estudio .es-modo button[aria-pressed="true"]{background:var(--paper);color:var(--go);box-shadow:0 1px 3px rgba(0,0,0,.15)}
#estudio .es-modo{order:-3!important}
#estudio .es-modo small{display:block;font:600 .66rem var(--f-mono);color:var(--muted);letter-spacing:.04em;margin-top:1px}
#estudio .es-akkey{padding:18px;display:grid;gap:10px}#estudio .es-akkey input{font:inherit;padding:10px 12px;border:1.5px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink)}
#estudio .es-row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
#estudio .es-srsbox{padding:0;overflow:hidden}#estudio .es-srsbox>.srs{min-height:460px}#estudio .es-srsbox>h3,#estudio .es-srsbox>p{padding:0 18px}#estudio .es-srsbox>h3{padding-top:16px}
#estudio .es-stat{display:flex;gap:18px;flex-wrap:wrap;margin:2px 0 14px}#estudio .es-stat div b{display:block;font:900 1.6rem/1 var(--f-display)}#estudio .es-stat div span{font-size:.78rem;color:var(--muted)}
#estudio .es-card{border:1.5px solid var(--line);border-radius:16px;padding:22px 20px;min-height:190px;display:flex;flex-direction:column;gap:12px;background:var(--bg)}
#estudio .es-card .es-meta{font:600 .72rem var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
#estudio .es-card .es-f{font:700 1.18rem/1.4 var(--f-display)}
#estudio .es-card .es-b{font-size:1rem;line-height:1.5;border-top:1.5px dashed var(--line);padding-top:12px}
#estudio .es-grades{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
#estudio .es-grades button{border:0;border-radius:12px;padding:10px 6px;font:800 .88rem var(--f-display);cursor:pointer;color:#fff}
#estudio .es-grades small{display:block;font:600 .7rem var(--f-mono);opacity:.85;margin-top:2px}
#estudio .es-grades .g0{background:#c0392b}#estudio .es-grades .g1{background:#c9a24a}#estudio .es-grades .g2{background:var(--green-3)}#estudio .es-grades .g3{background:#2f6fc1}
#estudio .cbtn.sec{background:transparent;color:var(--ink);border:1.5px solid var(--line)}
#estudio .cbtn:disabled{opacity:.5;cursor:default}
#estudio .es-q{font:700 1.08rem/1.45 var(--f-display);margin:6px 0 14px}
#estudio .es-opts{display:grid;gap:8px}
#estudio .es-opt{text-align:left;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);border-radius:12px;padding:11px 14px;font:500 .95rem/1.4 var(--f-display);cursor:pointer;display:flex;gap:10px}
#estudio .es-opt i{font-style:normal;font-weight:800;color:var(--muted)}
#estudio .es-opt.sel{border-color:var(--orange);box-shadow:0 0 0 2px color-mix(in srgb,var(--orange) 30%,transparent)}
#estudio .es-opt.ok{border-color:#1f9d6b;background:color-mix(in srgb,#1f9d6b 14%,var(--bg))}
#estudio .es-opt.ko{border-color:#c0392b;background:color-mix(in srgb,#c0392b 12%,var(--bg))}
#estudio .es-exp{font-size:.9rem;line-height:1.5;color:var(--muted);margin:10px 0 0}
#estudio .es-top{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:6px;font:700 .85rem var(--f-mono)}
#estudio .es-clock{background:var(--green);color:#fff;border-radius:999px;padding:4px 12px}#estudio .es-clock.low{background:#c0392b}
#estudio .es-bar{height:6px;background:var(--line);border-radius:9px;overflow:hidden;margin:4px 0 14px}#estudio .es-bar i{display:block;height:100%;background:var(--orange)}
#estudio .es-bars{display:grid;gap:9px}#estudio .es-bars div{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 10px;font-size:.86rem}
#estudio .es-bars em{grid-column:1/-1;height:8px;border-radius:9px;background:var(--line);overflow:hidden;font-style:normal}#estudio .es-bars em i{display:block;height:100%;border-radius:9px}
#estudio .es-big{font:900 clamp(2.4rem,6vw,3.6rem)/1 var(--f-display);text-align:center;margin:8px 0}
#estudio .es-res li{margin:10px 0;line-height:1.45}#estudio .es-res small{display:block;color:var(--muted)}
#estudio .es-ring{position:relative;width:min(260px,70vw);aspect-ratio:1;margin:6px auto 12px}
#estudio .es-ring svg{width:100%;height:100%;transform:rotate(-90deg)}#estudio .es-ring circle{fill:none;stroke-width:9}
#estudio .es-ring .bg{stroke:var(--line)}#estudio .es-ring .fg{stroke:var(--orange);stroke-linecap:round;transition:stroke-dashoffset .9s linear}
#estudio .es-ring.brk .fg{stroke:var(--green-3)}
#estudio .es-ring div{position:absolute;inset:0;display:grid;place-content:center;text-align:center}
#estudio .es-ring b{font:900 clamp(2.6rem,9vw,3.6rem)/1 var(--f-display);font-variant-numeric:tabular-nums}#estudio .es-ring span{font-size:.85rem;color:var(--muted);margin-top:6px}
#estudio .es-presets{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-bottom:12px}
#estudio .es-note{border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin:8px 0;background:var(--bg)}
#estudio .es-note summary{cursor:pointer;display:flex;gap:8px;align-items:baseline;list-style:none}#estudio .es-note summary b{flex:1;min-width:0}
#estudio .es-note summary small{color:var(--muted);font:600 .72rem var(--f-mono);white-space:nowrap}
#estudio .es-note .es-x{white-space:pre-wrap;line-height:1.5;margin:10px 0;font-size:.94rem}
#estudio .es-ok{color:#1f9d6b;font-weight:700}#estudio .es-mut{color:var(--muted)}
#estudio .es-mine{max-height:280px;overflow:auto;margin-top:8px}#estudio .es-mine div{display:flex;gap:8px;align-items:flex-start;border-top:1px solid var(--line);padding:7px 0;font-size:.86rem}#estudio .es-mine div span{flex:1;min-width:0}
#estudio textarea.es-ta{min-height:180px;resize:vertical;font:500 .95rem/1.5 var(--f-display)}
#estudio .es-h4{font:800 .95rem var(--f-display);margin:16px 0 8px}
#estudio .es-help{font-size:.82rem;color:var(--muted);line-height:1.45;margin:4px 0 10px}
#esPill{position:fixed;z-index:9989;left:calc(14px + env(safe-area-inset-left));bottom:calc(14px + env(safe-area-inset-bottom));display:flex;gap:8px;align-items:center;border:0;border-radius:999px;padding:9px 14px;background:var(--orange);color:#fff;font:800 .85rem var(--f-display);box-shadow:0 8px 24px rgba(0,0,0,.3);cursor:pointer;font-variant-numeric:tabular-nums}
#esPill.brk{background:var(--green-3)}#esPill[hidden]{display:none}
#gpCalc table{width:100%;border-collapse:collapse;font-size:.88rem}#gpCalc th{text-align:left;font:600 .7rem var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:4px 4px}
#gpCalc td{padding:3px 4px}#gpCalc td input{width:100%;min-width:0;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);border-radius:8px;padding:7px 8px;font:500 .9rem var(--f-display)}
#gpCalc td:nth-child(2),#gpCalc td:nth-child(3){width:78px}#gpCalc td:last-child{width:28px}
#gpCalc .gp-x{border:0;background:transparent;color:var(--muted);font-size:1.1rem;cursor:pointer}
#gpCalc .gp-out{margin-top:10px;font-size:.95rem;line-height:1.5}#gpCalc .gp-out b{color:var(--orange)}
#estudio .cal-main .ccard{order:-1!important}#estudio .cal-side .ccard{order:1!important}
@media (max-width:860px){#estudio .es-hero{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){#estudio .es-tab span{display:none}#estudio .es-tab{padding:9px 13px}#estudio .es-grades{grid-template-columns:repeat(2,1fr)}#esBtn span{display:none}}
`;
  const ICO={
    book:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/><path d="M9 8h7"/></svg>',
    cards:'<svg viewBox="0 0 24 24"><rect x="3" y="6" width="14" height="14" rx="2"/><path d="M7 3h12a2 2 0 0 1 2 2v12"/></svg>',
    exam:'<svg viewBox="0 0 24 24"><path d="M9 4h6v3H9z"/><path d="M8 5H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><path d="M8 13l2.5 2.5L16 10"/></svg>',
    timer:'<svg viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2M9 2h6"/></svg>',
    stats:'<svg viewBox="0 0 24 24"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
    note:'<svg viewBox="0 0 24 24"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/></svg>'};

  /* ===== vista ===== */
  const TABS=[["tarjetas","Tarjetas",ICO.cards],["examen","Modo examen",ICO.exam],["contador","Contador",ICO.timer],["notas","Notas",ICO.note],["stats","Estadísticas",ICO.stats]];
  const html=`<div class="cal" id="estudio" hidden role="dialog" aria-modal="true" aria-labelledby="esTtl">
  <div class="vbar gut"><a class="vbtn" href="#" id="esBack"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg><span class="lbl">Inicio</span></a>
    <div class="ttl" id="esTtl">${ICO.book}Estudio</div></div>
  <div class="cal-body gut"><div class="in">
    <section class="gr-hero es-hero" id="esHero"></section>
    <div class="es-tabs" role="tablist">${TABS.map(([k,l,i])=>`<button class="es-tab" type="button" role="tab" data-tab="${k}" aria-selected="false">${i}<span>${l}</span><b hidden></b></button>`).join("")}</div>
    <div class="es-mats" id="esMats" aria-label="Materia"></div>
    <div class="es-pane" data-pane="tarjetas"><div class="cal-grid"><div class="cal-main">
      <div class="es-modo" id="esModo" role="group" aria-label="Modo de tarjetas"></div><section class="ccard es-srsbox" id="esCards"></section></div><div class="cal-side">
      <details class="ccard udet fold" data-fold="es-addc"><summary><h3>Agregar tarjeta</h3><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary>
        <form class="cform" id="esCForm" autocomplete="off">
          <div class="row2"><label>Materia<input class="es-matin" list="esMatList" maxlength="80" required></label><label>Tema <span class="h">opcional</span><input id="esCTema" maxlength="80"></label></div>
          <label>Frente (pregunta)<textarea id="esCF" rows="2" maxlength="600" required></textarea></label>
          <label>Reverso (respuesta)<textarea id="esCB" rows="3" maxlength="1200" required></textarea></label>
          <div class="btns"><button class="cbtn" type="submit">Guardar tarjeta</button></div></form>
        <div class="es-mine" id="esMineC"></div></details>
      <details class="ccard udet fold" data-fold="es-ia"><summary><h3>Crear con IA <small>gratis</small></h3><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary>
        <p class="es-help">Gemini (gratis, con la clave del Asistente del Calendario) te hace tarjetas y preguntas tipo ENARM de un tema. Si pegas tus apuntes o un fragmento del CTO, las saca de ahí.</p>
        <form class="cform" id="esIA" autocomplete="off">
          <div class="row2"><label>Materia<input class="es-matin" list="esMatList" maxlength="80" required></label><label>Tema<input id="esIATema" maxlength="120" placeholder="Ej. Esquizofrenia" required></label></div>
          <label>Texto base <span class="h">opcional: apuntes o CTO</span><textarea id="esIATxt" rows="3" maxlength="20000"></textarea></label>
          <div class="row2"><label>Tarjetas<select id="esIANc"><option>0</option><option>10</option><option selected>15</option><option>25</option></select></label><label>Preguntas<select id="esIANq"><option>0</option><option selected>10</option><option>20</option></select></label></div>
          <p class="cerr" id="esIAErr" hidden></p><div class="btns"><button class="cbtn" type="submit">Crear</button></div></form></details>
      <details class="ccard udet fold" data-fold="es-cset"><summary><h3>Ajustes</h3><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary>
        <label class="gr-min">Tarjetas nuevas por día (cada materia) <select id="esNew"><option>0</option><option>5</option><option>10</option><option>20</option><option>30</option><option>50</option><option>100</option></select></label></details>
    </div></div></div>
    <div class="es-pane" data-pane="examen" hidden><div class="cal-grid"><div class="cal-main"><section class="ccard" id="esExam"></section></div>
      <div class="cal-side"><section class="ccard" id="esExStats"></section>
      <details class="ccard udet fold" data-fold="es-addq"><summary><h3>Agregar pregunta</h3><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary>
        <form class="cform" id="esQForm" autocomplete="off">
          <div class="row2"><label>Materia<input class="es-matin" list="esMatList" maxlength="80" required></label><label>Tema <span class="h">opcional</span><input id="esQTema" maxlength="80"></label></div>
          <label>Pregunta<textarea id="esQQ" rows="3" maxlength="1200" required></textarea></label>
          <label>Opciones <span class="h">una por renglón; pon * al inicio de la correcta</span><textarea id="esQO" rows="4" maxlength="1600" placeholder="Haloperidol&#10;*Clozapina&#10;Risperidona&#10;Litio" required></textarea></label>
          <label>Explicación <span class="h">opcional</span><textarea id="esQE" rows="2" maxlength="1200"></textarea></label>
          <p class="cerr" id="esQErr" hidden></p><div class="btns"><button class="cbtn" type="submit">Guardar pregunta</button></div></form>
        <div class="es-mine" id="esMineQ"></div></details></div></div></div>
    <div class="es-pane" data-pane="stats" hidden><section class="ccard es-srsbox" id="esStats"></section></div>
    <div class="es-pane" data-pane="contador" hidden><div class="cal-grid"><div class="cal-main"><section class="ccard" id="esPomo"></section></div>
      <div class="cal-side"><section class="ccard" id="esTime"></section></div></div></div>
    <div class="es-pane" data-pane="notas" hidden><div class="cal-grid"><div class="cal-main"><section class="ccard" id="esNotes"></section></div>
      <div class="cal-side"><section class="ccard" id="esNForm"></section></div></div></div>
    <datalist id="esMatList"></datalist>
  </div></div></div>`;

  let tab="tarjetas",mat="",ready=false,lastY=0;
  const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
  function mount(){
    if(ready)return;ready=true;
    const st=document.createElement("style");st.textContent=css;document.head.appendChild(st);
    document.body.insertAdjacentHTML("beforeend",html+`<button id="esPill" type="button" hidden></button>`);
    const t=get(K.tab);if(TABS.some(x=>x[0]===t))tab=t;
    $("#esBack").addEventListener("click",ev=>{ev.preventDefault();goHome()});
    $$("#estudio .es-tab").forEach(b=>b.addEventListener("click",()=>{tab=b.dataset.tab;set(K.tab,tab);render()}));
    $("#esMats").addEventListener("click",ev=>{const b=ev.target.closest("[data-mat]");if(!b)return;mat=b.dataset.mat;render()});
    $$("#estudio details.fold").forEach(d=>{const k="carrera-fold-"+d.dataset.fold,v=get(k);if(v!=null)d.open=v==="1";d.addEventListener("toggle",()=>set(k,d.open?"1":"0"))});
    $("#esPill").addEventListener("click",()=>{tab="contador";set(K.tab,tab);location.hash="estudio";render()});
    bindCards();bindExam();bindPomo();bindNotes();
    document.addEventListener("keydown",onKey);
    addEventListener("storage",ev=>{if(ev.key&&ev.key.startsWith("carrera-")&&!$("#estudio").hidden&&!exam){if(window.SRS)SRS.reloadAll();render()}});
    tickPomo();setInterval(tickPomo,1000);
  }
  const goHome=()=>{if(typeof go==="function")go("");else location.hash=""};
  function open(){
    mount();if(!$("#estudio").hidden)return;
    lastY=window.scrollY;
    if(!mat){const e=upcoming()[0];if(e&&diffD(today(),e.date)<=14)mat=examMat(e)}
    $("#estudio").hidden=false;document.documentElement.style.overflow="hidden";document.title="Estudio · Carrera de Medicina";
    render();Promise.all([loadBank(),loadSRS()]).then(()=>{if(!mat){const e=upcoming()[0];if(e&&diffD(today(),e.date)<=14)mat=examMat(e)}render()});
  }
  function close(){
    if(!ready||$("#estudio").hidden)return;$("#estudio").hidden=true;document.documentElement.style.overflow="";document.title="Carrera de Medicina";
    requestAnimationFrame(()=>window.scrollTo(0,lastY));tickPomo();
  }
  function onKey(ev){
    if($("#estudio").hidden)return;const typing=/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement&&document.activeElement.tagName);
    if(ev.key==="Escape"&&!typing&&!document.querySelector("#estudio .srs-menu")){goHome();return}
    if(typing)return;
    if(tab==="examen"&&exam&&!exam.done&&/^[1-5a-e]$/i.test(ev.key)){const i=/\d/.test(ev.key)?+ev.key-1:ev.key.toLowerCase().charCodeAt(0)-97;pick(i)}
  }

  function render(){
    if(!ready||$("#estudio").hidden)return;
    $$("#estudio .es-tab").forEach(b=>b.setAttribute("aria-selected",String(b.dataset.tab===tab)));
    $$("#estudio .es-pane").forEach(p=>p.hidden=p.dataset.pane!==tab);
    const ms=materias();
    $("#esMatList").innerHTML=ms.map(m=>`<option value="${esc(m)}">`).join("");
    $("#esMats").innerHTML=[["","Todas"]].concat(ms.map(m=>[m,m])).map(([v,l])=>`<button type="button" class="es-chip" data-mat="${esc(v)}" aria-pressed="${norm(v)===norm(mat)}">${esc(l)}</button>`).join("");
    $$("#estudio .es-matin").forEach(i=>{if(!i.value&&mat)i.value=mat});
    const di=dueInfo("");const badge=$('#estudio .es-tab[data-tab="tarjetas"] b');badge.hidden=!(di.due+di.newLeft);badge.textContent=di.due+di.newLeft;
    renderModo();$("#esMats").hidden=tab==="tarjetas"&&modo==="anking";
    renderHero();
    if(tab==="tarjetas")renderCards();else if(tab==="stats")renderStats();else if(tab==="examen")renderExam();else if(tab==="contador")renderPomo();else renderNotes();
  }
  function renderHero(){
    const t=today(),di=dueInfo(mat),sims=list(K.sims).filter(s=>sameMat(s.mat,mat)&&diffD(s.d,t)<=30),ok=sims.reduce((a,s)=>a+s.ok,0),n=sims.reduce((a,s)=>a+s.n,0);
    const tm=list(K.time).filter(s=>sameMat(s.mat,mat)),mToday=tm.filter(s=>s.d===t).reduce((a,s)=>a+s.m,0),mWeek=tm.filter(s=>diffD(s.d,t)<7).reduce((a,s)=>a+s.m,0);
    const ex=upcoming().filter(e=>!mat||sameMat(examMat(e),mat))[0];
    $("#esHero").innerHTML=`<p class="gh-kick">${mat?esc(mat):"Todas tus materias"}${BANK&&window.SRS?"":" · cargando tus guías…"}</p>
      <div class="es-k"><b>${di.due+di.newLeft}</b><span>tarjetas para hoy</span></div>
      <div class="es-k"><b>${n?pct(ok,n)+"%":"—"}</b><span>aciertos (30 días)</span></div>
      <div class="es-k"><b>${hm(mToday)}</b><span>estudiado hoy</span></div>
      <div class="es-k"><b>${hm(mWeek)}</b><span>en 7 días</span></div>
      ${ex?`<p class="es-next">Próximo examen: <b>${esc(ex.name)}</b> · ${diffD(t,ex.date)===0?"hoy":diffD(t,ex.date)===1?"mañana":"en "+diffD(t,ex.date)+" días ("+nice(ex.date)+")"}</p>`:""}`;
  }

  /* ===== Tarjetas (pantallas de Anki: Mazos → resumen del mazo → repaso) ===== */
  /* ===== Modo AnKing: mazo AnKing en español (cifrado), un mazo por sistema; avance propio (carrera-anki-anking-<sistema>) ===== */
  const KM="carrera-es-modo",CK="carrera-anking-clave";
  let modo=get(KM)==="anking"?"anking":"normal",AK=null,akP=null,akErr="",akSel=null;
  async function akDecrypt(buf){
    const pass=(get(CK)||"").trim();if(!pass)throw new Error("nokey");
    const te=new TextEncoder(),ikm=await crypto.subtle.importKey("raw",te.encode(pass),"HKDF",false,["deriveKey"]);
    const key=await crypto.subtle.deriveKey({name:"HKDF",hash:"SHA-256",salt:te.encode("medicina-udlap/anking/v1"),info:te.encode("mazo")},ikm,{name:"AES-GCM",length:256},false,["decrypt"]);
    const u=new Uint8Array(buf);let pt;try{pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:u.slice(0,12)},key,u.slice(12))}catch(e){throw new Error("badkey")}
    return JSON.parse(await new Response(new Blob([pt]).stream().pipeThrough(new DecompressionStream("gzip"))).text());
  }
  function loadAK(){
    if(AK)return Promise.resolve(AK);
    if(akP)return akP;
    akErr="";
    akP=fetch("anki/anking/index.json").then(r=>{if(!r.ok)throw new Error("http");return r.json()}).then(async idx=>{
      const out=[];
      for(const m of idx){
        const t=await fetch("anki/anking/"+m.id+".txt").then(r=>{if(!r.ok)throw new Error("http");return r.text()});
        const d=await akDecrypt(Uint8Array.from(atob(t.trim()),c=>c.charCodeAt(0)));
        const id="anking-"+m.id,st=SRS.deckStore(id),P=st.meta();
        if(P.N!==d.c.length||P.name!==m.n)st.set({N:d.c.length,name:m.n});
        const cards=d.c.map(c=>({k:SRS.hash(c[1]+"|"+c[2]),st,f:c[1],b:c[2],t:c[0],deck:id,dn:m.n}));
        out.push({id,slug:m.id,name:m.n,group:"AnKing en español",ids:[id],cards:()=>cards,total:cards.length,
          newLim:()=>{const l=st.meta().lim;return l!=null?l:20},revLim:()=>st.meta().rlim||200,store:st});
      }
      return AK=out;
    }).catch(e=>{akErr=e&&e.message||"err";akP=null;return null});
    return akP;
  }
  function renderAK(){
    const box=$("#esCards");
    if(rv&&AK&&akSel&&rvKey==="ak:"+akSel&&box.contains(rv.el)){rv.refresh();return}
    if(rv){rv.destroy();rv=null}
    if(!window.SRS){rvKey=null;box.innerHTML=`<h3>AnKing</h3><p class="es-mut">Cargando…</p>`;return}
    if(!AK){rvKey=null;
      if(akErr==="nokey"||akErr==="badkey"){
        box.innerHTML=`<div class="es-akkey"><h3>Mazo AnKing</h3><p class="es-help">${akErr==="badkey"?"Esa clave no abre el mazo. Revísala.":"Escribe la clave del mazo AnKing. Solo se pide una vez y se sincroniza con tus otros aparatos."}</p><input type="password" id="esAkKey" autocomplete="off" placeholder="Clave"><div class="btns"><button class="cbtn" type="button" id="esAkGo">Abrir mazo</button></div></div>`;
        const go=()=>{const v=$("#esAkKey").value.trim();if(!v)return;set(CK,v);akErr="";akP=null;renderAK()};
        $("#esAkGo").onclick=go;$("#esAkKey").onkeydown=e=>{if(e.key==="Enter")go()};return}
      if(akErr){box.innerHTML=`<h3>AnKing</h3><p class="es-mut">No pude cargar el mazo AnKing. Revisa tu conexión e inténtalo de nuevo.</p><div class="es-row"><button class="cbtn" type="button" id="esAkRe">Reintentar</button></div>`;$("#esAkRe").onclick=()=>{akErr="";renderAK()};return}
      box.innerHTML=`<h3>AnKing en español</h3><p class="es-mut">Abriendo el mazo (35,034 tarjetas)…</p>`;
      loadAK().then(()=>{if(modo==="anking"&&!$("#estudio").hidden)render()});return}
    const d=akSel&&AK.find(x=>x.id===akSel);
    if(d){rvKey="ak:"+d.id;box.innerHTML="";
      rv=SRS.reviewer(box,{title:()=>"AnKing · "+d.name,cards:d.cards,ids:d.ids,newLim:d.newLim,revLim:d.revLim,setLim:o=>d.store.set(o),shuffleNew:true,
        onStats:()=>{tab="stats";set(K.tab,tab);render()},onBack:()=>{akSel=null;render()},back:"Mazos AnKing"});return}
    rvKey="ak:list";SRS.css();
    box.innerHTML=`<div class="srs"${SRS.dark()?" data-dark":""}><div class="srs-top"><b>AnKing en español</b><button class="srs-tb" type="button" data-es="stats">Estadísticas</button></div>
      <div style="padding:6px 8px 4px;overflow-x:auto">${SRS.deckList(AK)}</div>
      <p class="srs-k" style="text-align:center;padding:4px 10px 14px">Un mazo por sistema, con repaso estilo Anki (Otra vez, Difícil, Bien, Fácil). Su avance es aparte de tus tarjetas normales.</p></div>`;
  }
  function renderModo(){
    const m=$("#esModo");if(!m)return;
    m.innerHTML=`<button type="button" data-modo="normal" aria-pressed="${modo==="normal"}">Estudio normal<small>tus guías y tarjetas</small></button><button type="button" data-modo="anking" aria-pressed="${modo==="anking"}">Modo AnKing<small>mazo en español</small></button>`;
  }
  let rv=null,rvKey=null,stv=null;
  function renderCards(){
    const box=$("#esCards");
    if(modo==="anking"){renderAK();return}
    if(!BANK||!window.SRS){if(rv){rv.destroy();rv=null}rvKey=null;box.innerHTML=`<h3>Tarjetas</h3><p class="es-mut">Cargando tus tarjetas…</p>`;return}
    const d=deckOf(mat),key=(d?d.id:mat?"none:"+mat:"")+"|"+DKsig;
    if(rvKey===key&&(rv?box.contains(rv.el):box.querySelector(".srs"))){if(rv)rv.refresh();else drawDecks(box);return}
    if(rv){rv.destroy();rv=null}rvKey=key;box.innerHTML="";
    if(mat&&!d){box.innerHTML=`<h3>Tarjetas <small>${esc(mat)}</small></h3><p class="es-mut">Todavía no hay tarjetas de esta materia. Agrega las tuyas o créalas con IA.</p>`;return}
    if(!d){drawDecks(box);return}
    rv=SRS.reviewer(box,{title:()=>d.name,cards:d.cards,ids:d.ids,newLim:d.newLim,revLim:d.revLim,setLim:o=>{setLim(o);renderHero()},
      onStats:()=>{tab="stats";set(K.tab,tab);render()},onBack:()=>{mat="";render()},back:"Mazos"});
  }
  function drawDecks(box){
    SRS.css();const ds=decks(),t=SRS.today(null);
    box.innerHTML=`<div class="srs"${SRS.dark()?" data-dark":""}><div class="srs-top"><b>Mazos</b><button class="srs-tb" type="button" data-es="stats">Estadísticas</button></div>
      <div style="padding:6px 8px 4px;overflow-x:auto">${ds.length?SRS.deckList(ds):`<p class="es-mut">Todavía no hay tarjetas.</p>`}</div>
      <p class="srs-k" style="text-align:center;padding:4px 10px 14px">${t.n?`Hoy estudiaste ${t.n} tarjeta${t.n===1?"":"s"} en ${Math.max(1,Math.round(t.ms/6e4))} min.`:"Hoy aún no estudias."} Toca una materia para ver su resumen y estudiar. Funciona igual que Anki y comparte el avance con el botón «Tus tarjetas de Anki» de cada guía.</p></div>`;
  }
  function renderStats(){
    const box=$("#esStats");
    if(!BANK||!window.SRS){box.innerHTML=`<h3>Estadísticas</h3><p class="es-mut">Cargando…</p>`;return}
    const d=deckOf(mat),sc=d?d.id:"";
    if(stv&&box.contains(stv.el)){stv.setScope(sc);return}
    box.innerHTML="";
    stv=SRS.stats(box,{decks:()=>decks(),scopes:()=>[["","Todas las materias"]].concat(decks().map(x=>[x.id,x.name])),scope:sc});
  }
  function bindCards(){
    $("#esModo").addEventListener("click",ev=>{const b=ev.target.closest("[data-modo]");if(!b||b.dataset.modo===modo)return;modo=b.dataset.modo;set(KM,modo);akSel=null;if(rv){rv.destroy();rv=null}rvKey=null;$("#esCards").innerHTML="";render()});
    $("#esCards").addEventListener("click",ev=>{
      if(modo==="anking"){const r=ev.target.closest("tr[data-deck]");if(r&&AK&&AK.find(x=>x.id===r.dataset.deck)){akSel=r.dataset.deck;render();return}}
      const r=ev.target.closest("tr[data-deck]");if(r){const d=decks().find(x=>x.id===r.dataset.deck);if(d){mat=d.name;render()}return}
      const b=ev.target.closest("button");if(!b)return;
      if(b.dataset.es==="stats"){tab="stats";set(K.tab,tab);render()}
    });
    $("#esCForm").addEventListener("submit",ev=>{ev.preventDefault();const f=ev.target;
      const items=list(K.cards);items.push({id:uid("t"),mat:f.querySelector(".es-matin").value.trim(),t:$("#esCTema").value.trim(),f:$("#esCF").value.trim(),b:$("#esCB").value.trim(),src:"mia"});
      saveList(K.cards,items);$("#esCF").value="";$("#esCB").value="";$("#esCF").focus();mineCards();render()});
    $("#esMineC").addEventListener("click",ev=>{const d=ev.target.closest("[data-del]");if(!d)return;
      if(!d.classList.contains("warn")){d.classList.add("warn");d.textContent="¿Seguro?";return}
      saveList(K.cards,list(K.cards).filter(x=>x.id!==d.dataset.del));mineCards();render()});
    $("#esNew").value=String(cfg().nuevas);
    $("#esNew").addEventListener("change",ev=>{setLim({lim:+ev.target.value});if(rv){rv.destroy();rv=null;rvKey=null}render()});
    $("#esIA").addEventListener("submit",ev=>{ev.preventDefault();genIA(ev.target)});
    mineCards();
  }
  function mineCards(){const l=myCards().slice(-60).reverse();
    $("#esMineC").innerHTML=l.length?`<p class="es-help">Tus tarjetas (${myCards().length}):</p>`+l.map(c=>`<div><span><b>${esc(c.f)}</b><br><small class="es-mut">${esc(c.mat)} · ${esc(c.b.slice(0,90))}</small></span><button class="mini" type="button" data-del="${esc(c.id)}">Borrar</button></div>`).join(""):""}

  /* ===== IA (Gemini gratis, misma clave que el Asistente) ===== */
  async function genIA(f){
    const err=$("#esIAErr"),btn=f.querySelector("button[type=submit]");err.hidden=true;
    const key=get("__medsync_gemkey");
    if(!key){err.textContent="Primero pega tu clave gratis de Gemini en el Asistente (Calendario → Asistente). Solo se hace una vez.";err.hidden=false;return}
    const m=f.querySelector(".es-matin").value.trim(),tema=$("#esIATema").value.trim(),txt=$("#esIATxt").value.trim(),nc=+$("#esIANc").value,nq=+$("#esIANq").value;
    if(!nc&&!nq){err.textContent="Elige cuántas tarjetas o preguntas quieres.";err.hidden=false;return}
    btn.disabled=true;btn.textContent="Creando…";
    const S=(type,extra)=>Object.assign({type},extra||{});
    const schema=S("OBJECT",{properties:{tarjetas:S("ARRAY",{items:S("OBJECT",{properties:{frente:S("STRING"),reverso:S("STRING")},required:["frente","reverso"]})}),
      preguntas:S("ARRAY",{items:S("OBJECT",{properties:{pregunta:S("STRING"),opciones:S("ARRAY",{items:S("STRING")}),correcta:S("INTEGER"),explicacion:S("STRING")},required:["pregunta","opciones","correcta","explicacion"]})})},required:["tarjetas","preguntas"]});
    const sys=`Eres profesor de medicina en México y preparas a un estudiante de 5º semestre de Médico Cirujano (UDLAP) para sus parciales y el ENARM.
Materia: ${m}. Tema: ${tema}.
Haz exactamente ${nc} tarjetas de memoria (frente = pregunta corta y concreta; reverso = respuesta breve, con el dato clave) y ${nq} preguntas de opción múltiple estilo ENARM (caso clínico corto cuando aplique, 4 opciones, una sola correcta, "correcta" es el índice empezando en 0, explicación de 1 a 3 frases de por qué).
Todo en español de México, con guías mexicanas (GPC, NOM) cuando aplique. ${txt?"Básate SOLO en el texto que te da el estudiante; no inventes datos que no estén ahí.":"Usa información médica actual y confiable."} Responde solo con el JSON pedido.`;
    const body=JSON.stringify({system_instruction:{parts:[{text:sys}]},contents:[{role:"user",parts:[{text:txt||("Tema: "+tema)}]}],generationConfig:{responseMimeType:"application/json",responseSchema:schema,temperature:0.4}});
    try{
      let r;for(const md of ["gemini-flash-latest","gemini-3.8-flash","gemini-2.5-flash"]){
        try{r=await fetch("https://generativelanguage.googleapis.com/v1beta/models/"+md+":generateContent",{method:"POST",headers:{"content-type":"application/json","x-goog-api-key":key},body})}catch(e){throw new Error("Sin conexión: crear con IA necesita internet.")}
        if(r.status!==404)break}
      const j=await r.json().catch(()=>({}));
      if(r.status===429)throw new Error("Llegaste al límite gratis de Gemini por ahora; intenta en un rato.");
      if(r.status===403||r.status===400&&/API key/i.test(j.error&&j.error.message||""))throw new Error("La clave de Gemini no sirve; revísala en el Asistente.");
      if(!r.ok)throw new Error("Gemini respondió con error "+r.status+".");
      const c=j.candidates&&j.candidates[0],t=c&&c.content&&c.content.parts?c.content.parts.map(x=>x.text||"").join(""):"";
      let x;try{x=JSON.parse(t.replace(/^```(json)?|```$/g,"").trim())}catch(e){throw new Error("No entendí la respuesta; intenta otra vez.")}
      const cards=(x.tarjetas||[]).filter(y=>y&&y.frente&&y.reverso).slice(0,40).map(y=>({id:uid("t"),mat:m,t:tema,f:String(y.frente).slice(0,600),b:String(y.reverso).slice(0,1200),src:"ia"}));
      const qs=(x.preguntas||[]).filter(y=>y&&y.pregunta&&Array.isArray(y.opciones)&&y.opciones.length>1&&y.correcta>=0&&y.correcta<y.opciones.length).slice(0,40)
        .map(y=>({id:uid("p"),mat:m,t:tema,q:String(y.pregunta).slice(0,1200),o:y.opciones.slice(0,6).map(o=>String(o).slice(0,300)),a:+y.correcta,e:String(y.explicacion||"").slice(0,1200),src:"ia"}));
      if(cards.length)saveList(K.cards,list(K.cards).concat(cards));
      if(qs.length)saveList(K.qs,list(K.qs).concat(qs));
      err.textContent=`Listo: ${cards.length} tarjetas y ${qs.length} preguntas de ${tema}. Revísalas: la IA se puede equivocar.`;err.hidden=false;err.style.color="#1f9d6b";
      $("#esIATxt").value="";mat=m;mineCards();mineQs();render();
    }catch(e){err.style.color="";err.textContent=e.message;err.hidden=false}
    btn.disabled=false;btn.textContent="Crear";
  }

  /* ===== Modo examen ===== */
  let exam=null,exTimer=null;
  const qprog=()=>{const m=new Map();list(K.qprog).forEach(p=>m.set(p.id,p));return m};
  function renderExam(){
    const box=$("#esExam");
    if(!BANK){box.innerHTML=`<h3>Modo examen</h3><p class="es-mut">Cargando preguntas de tus guías…</p>`;return}
    if(exam&&!exam.done)return drawQ();
    if(exam&&exam.done)return drawRes();
    const pool=allQs().filter(q=>sameMat(q.mat,mat)),pm=qprog(),wrong=pool.filter(q=>{const p=pm.get(q.id);return p&&p.ko>0&&p.last===0});
    const temas=[...new Set(pool.map(q=>q.t).filter(Boolean))].sort((a,b)=>a.localeCompare(b,"es"));
    const seen=pool.filter(q=>pm.has(q.id)).length;
    box.innerHTML=`<h3>Modo examen <small>${esc(mat||"todas las materias")}</small></h3>
      ${pool.length?`<p class="es-help">${pool.length} preguntas disponibles · ya contestaste ${seen} · ${wrong.length} falladas la última vez.</p>
      <form class="cform" id="esExForm">
        ${temas.length?`<label>Tema<select id="esExTema"><option value="">Todos los temas</option>${temas.map(t=>`<option>${esc(t)}</option>`).join("")}</select></label>`:""}
        <div class="row2"><label>Preguntas<select id="esExN"><option>10</option><option selected>20</option><option>40</option><option>60</option><option>100</option></select></label>
        <label>Tiempo<select id="esExT"><option value="60">1 min por pregunta</option><option value="78" selected>1.3 min (tipo ENARM)</option><option value="0">Sin límite</option></select></label></div>
        <label>Cuáles<select id="esExWho"><option value="new">Primero las que no has visto</option><option value="all">Al azar de todas</option><option value="ko" ${wrong.length?"":"disabled"}>Solo las que fallé (${wrong.length})</option></select></label>
        <label style="display:flex;gap:8px;align-items:center;font-weight:600"><input type="checkbox" id="esExNow" style="width:auto"> Ver la respuesta al momento (modo estudio)</label>
        <div class="btns"><button class="cbtn" type="submit">Empezar</button></div></form>`
      :`<p class="es-mut">Todavía no hay preguntas de esta materia. Agrega las tuyas o créalas con IA (en Tarjetas → Crear con IA).</p>`}`;
    drawStats();
  }
  function startExam(){
    const tema=$("#esExTema")?$("#esExTema").value:"",n=+$("#esExN").value,per=+$("#esExT").value,who=$("#esExWho").value,now=$("#esExNow").checked;
    let pool=allQs().filter(q=>sameMat(q.mat,mat)&&(!tema||q.t===tema));const pm=qprog();
    if(who==="ko")pool=pool.filter(q=>{const p=pm.get(q.id);return p&&p.ko>0&&p.last===0});
    pool=shuffle(pool.slice());if(who==="new")pool.sort((a,b)=>(pm.has(a.id)?1:0)-(pm.has(b.id)?1:0));
    const qs=pool.slice(0,n).map(q=>{const order=shuffle(q.o.map((_,i)=>i));return Object.assign({},q,{order,ans:null})});
    if(!qs.length)return;
    exam={qs,i:0,now,start:Date.now(),limit:per?per*qs.length:0,done:false,mat,tema};
    clearInterval(exTimer);exTimer=setInterval(()=>{if(!exam||exam.done){clearInterval(exTimer);return}
      const c=$("#esClock");if(exam.limit){const left=exam.limit-(Date.now()-exam.start)/1000;if(c){c.textContent=mmss(left);c.classList.toggle("low",left<60)}if(left<=0)finishExam()}else if(c)c.textContent=mmss((Date.now()-exam.start)/1000)},1000);
    renderExam();
  }
  function drawQ(){
    const q=exam.qs[exam.i],answered=q.ans!=null,show=exam.now&&answered,el=(Date.now()-exam.start)/1000;
    $("#esExam").innerHTML=`<div class="es-top"><span>Pregunta ${exam.i+1} de ${exam.qs.length}</span><span class="es-clock" id="esClock">${exam.limit?mmss(exam.limit-el):mmss(el)}</span></div>
      <div class="es-bar"><i style="width:${pct(exam.qs.filter(x=>x.ans!=null).length,exam.qs.length)}%"></i></div>
      <p class="es-help">${esc(q.mat)}${q.t?" · "+esc(q.t):""}</p><p class="es-q">${esc(q.q)}</p>
      <div class="es-opts">${q.order.map((oi,k)=>`<button type="button" class="es-opt${q.ans===k?" sel":""}${show&&oi===q.a?" ok":""}${show&&q.ans===k&&oi!==q.a?" ko":""}" data-k="${k}"><i>${"ABCDEF"[k]}</i><span>${esc(q.o[oi])}</span></button>`).join("")}</div>
      ${show&&q.e?`<p class="es-exp">${esc(q.e)}</p>`:""}
      <div class="es-row" style="margin-top:16px;justify-content:space-between"><button class="cbtn sec" type="button" data-nav="-1" ${exam.i?"":"disabled"}>Anterior</button>
      <button class="cbtn sec" type="button" data-nav="end">Terminar</button>
      <button class="cbtn" type="button" data-nav="1">${exam.i===exam.qs.length-1?"Calificar":"Siguiente"}</button></div>`;
  }
  function pick(k){const q=exam.qs[exam.i];if(!q||k>=q.order.length)return;if(exam.now&&q.ans!=null)return;q.ans=k;drawQ()}
  function finishExam(){
    if(!exam||exam.done)return;exam.done=true;clearInterval(exTimer);exam.secs=Math.round((Date.now()-exam.start)/1000);
    const qs=exam.qs,ok=qs.filter(q=>q.ans!=null&&q.order[q.ans]===q.a).length,t=today();
    const pm=list(K.qprog),idx=new Map(pm.map((p,i)=>[p.id,i]));
    for(const q of qs){if(q.ans==null)continue;const good=q.order[q.ans]===q.a;let p=idx.has(q.id)?pm[idx.get(q.id)]:null;
      if(!p){p={id:q.id,ok:0,ko:0};pm.push(p);idx.set(q.id,pm.length-1)}if(good)p.ok++;else p.ko++;p.last=good?1:0;p.u=t}
    saveList(K.qprog,pm);
    const mats=[...new Set(qs.map(q=>q.mat))],sims=list(K.sims);
    for(const m of mats){const l=qs.filter(q=>q.mat===m);sims.push({id:uid("s"),d:t,mat:m,tema:exam.tema||"",n:l.length,ok:l.filter(q=>q.ans!=null&&q.order[q.ans]===q.a).length,s:Math.round(exam.secs*l.length/qs.length)})}
    saveList(K.sims,sims.slice(-300));
    exam.ok=ok;renderExam();renderHero();
  }
  function drawRes(){
    const qs=exam.qs,n=qs.length,ok=exam.ok,p=pct(ok,n),bad=qs.filter(q=>q.ans==null||q.order[q.ans]!==q.a);
    $("#esExam").innerHTML=`<h3>Resultado</h3><p class="es-big" style="color:${p>=80?"#1f9d6b":p>=60?"#c9a24a":"#c0392b"}">${p}%</p>
      <p style="text-align:center" class="es-mut">${ok} de ${n} correctas · ${mmss(exam.secs)} (${Math.round(exam.secs/n)} s por pregunta)</p>
      <div class="btns" style="text-align:center;margin:12px 0"><button class="cbtn" type="button" id="esExNew">Otro examen</button></div>
      ${bad.length?`<h4 class="es-h4">Para repasar (${bad.length})</h4><ol class="es-res">${bad.map(q=>`<li>${esc(q.q)}<small>${q.ans==null?"Sin contestar":"Pusiste: "+esc(q.o[q.order[q.ans]])} · <span class="es-ok">Correcta: ${esc(q.o[q.a])}</span></small>${q.e?`<small>${esc(q.e)}</small>`:""}</li>`).join("")}</ol>`:`<p style="text-align:center">¡Perfecto! 🎉</p>`}`;
    drawStats();
  }
  function drawStats(){
    const sims=list(K.sims),by=new Map();
    for(const s of sims){const k=norm(s.mat);const o=by.get(k)||{mat:s.mat,n:0,ok:0,last:""};o.n+=s.n;o.ok+=s.ok;if(s.d>o.last)o.last=s.d;by.set(k,o)}
    const rows=[...by.values()].sort((a,b)=>b.n-a.n),col=p=>p>=80?"#1f9d6b":p>=60?"#c9a24a":"#c0392b";
    const last=sims.slice(-6).reverse();
    $("#esExStats").innerHTML=`<h3>Tus aciertos <small>por materia</small></h3>${rows.length?`<div class="es-bars">${rows.map(r=>{const p=pct(r.ok,r.n);return `<div><span>${esc(r.mat)}</span><b style="color:${col(p)}">${p}%</b><em><i style="width:${p}%;background:${col(p)}"></i></em><small class="es-mut" style="grid-column:1/-1">${r.ok}/${r.n} · último ${nice(r.last)}</small></div>`}).join("")}</div>
      <h4 class="es-h4">Últimos exámenes</h4>${last.map(s=>`<p class="es-help" style="margin:4px 0">${nice(s.d)} · ${esc(s.mat)}${s.tema?" · "+esc(s.tema):""} · <b>${pct(s.ok,s.n)}%</b> (${s.ok}/${s.n})</p>`).join("")}`
      :`<p class="es-mut">Aquí verás tu % de aciertos por materia cuando hagas tu primer examen.</p>`}`;
  }
  function bindExam(){
    $("#esExam").addEventListener("submit",ev=>{if(ev.target.id==="esExForm"){ev.preventDefault();startExam()}});
    $("#esExam").addEventListener("click",ev=>{
      const o=ev.target.closest("[data-k]");if(o){pick(+o.dataset.k);return}
      const nv=ev.target.closest("[data-nav]");if(nv&&exam&&!exam.done){const v=nv.dataset.nav;
        if(v==="end"){if(!nv.classList.contains("warn")&&exam.qs.some(q=>q.ans==null)){nv.classList.add("warn");nv.textContent="¿Calificar ya?";return}finishExam();return}
        if(v==="1"&&exam.i===exam.qs.length-1){finishExam();return}
        exam.i=Math.max(0,Math.min(exam.qs.length-1,exam.i+ +v));drawQ();const top=$("#esExam").getBoundingClientRect().top;if(top<0)$("#esExam").scrollIntoView({block:"start"});return}
      if(ev.target.closest("#esExNew")){exam=null;renderExam()}
    });
    $("#esQForm").addEventListener("submit",ev=>{ev.preventDefault();const f=ev.target,e=$("#esQErr");
      const lines=$("#esQO").value.split("\n").map(s=>s.trim()).filter(Boolean),a=lines.findIndex(s=>s.startsWith("*"));
      if(lines.length<2||a<0){e.textContent="Pon al menos 2 opciones y marca la correcta con * al inicio.";e.hidden=false;return}e.hidden=true;
      const items=list(K.qs);items.push({id:uid("p"),mat:f.querySelector(".es-matin").value.trim(),t:$("#esQTema").value.trim(),q:$("#esQQ").value.trim(),o:lines.map(s=>s.replace(/^\*\s*/,"")),a,e:$("#esQE").value.trim(),src:"mia"});
      saveList(K.qs,items);["#esQQ","#esQO","#esQE"].forEach(s=>$(s).value="");mineQs();render()});
    $("#esMineQ").addEventListener("click",ev=>{const d=ev.target.closest("[data-del]");if(!d)return;
      if(!d.classList.contains("warn")){d.classList.add("warn");d.textContent="¿Seguro?";return}
      saveList(K.qs,list(K.qs).filter(x=>x.id!==d.dataset.del));mineQs();render()});
    mineQs();
  }
  function mineQs(){const l=myQs().slice(-60).reverse();
    $("#esMineQ").innerHTML=l.length?`<p class="es-help">Tus preguntas (${myQs().length}):</p>`+l.map(q=>`<div><span><b>${esc(q.q.slice(0,120))}</b><br><small class="es-mut">${esc(q.mat)} · ${esc(q.o[q.a])}</small></span><button class="mini" type="button" data-del="${esc(q.id)}">Borrar</button></div>`).join(""):""}

  /* ===== Contador de estudio (Pomodoro) ===== */
  const pomo=()=>J(POMO,null);
  const setPomo=p=>{if(p)set(POMO,JSON.stringify(p));else{try{localStorage.removeItem(POMO)}catch(e){}}};
  const left=p=>p?(p.paused!=null?p.paused:(p.end-Date.now())/1000):0;
  function logTime(m,minutes){if(minutes<1)return;const items=list(K.time);items.push({id:uid("m"),mat:m||"Sin materia",d:today(),m:Math.round(minutes)});saveList(K.time,items.slice(-2000))}
  function notify(title,body){
    try{const a=new (window.AudioContext||window.webkitAudioContext)(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=880;g.gain.setValueAtTime(.2,a.currentTime);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+1.2);o.start();o.stop(a.currentTime+1.2)}catch(e){}
    try{if(window.Notification&&Notification.permission==="granted"){
      if(navigator.serviceWorker&&navigator.serviceWorker.controller)navigator.serviceWorker.ready.then(r=>r.showNotification(title,{body,icon:"icon-192.png",tag:"pomo",data:{route:"estudio"}})).catch(()=>{});
      else new Notification(title,{body})}}catch(e){}
    if(window.__medToast)window.__medToast(title,"OK",()=>{});
  }
  function startPomo(phase,mins,m){
    try{if(window.Notification&&Notification.permission==="default")Notification.requestPermission().catch(()=>{})}catch(e){}
    setPomo({mat:m,phase,len:mins*60,end:Date.now()+mins*60e3,paused:null,started:Date.now()});tickPomo();renderPomo();
  }
  function tickPomo(){
    const p=pomo(),pill=$("#esPill");
    if(p&&p.paused==null&&left(p)<=0){
      if(p.phase==="foco"){logTime(p.mat,p.len/60);notify("¡Terminaste "+Math.round(p.len/60)+" min de "+(p.mat||"estudio")+"!","Tómate "+cfg().descanso+" minutos de descanso.");startPomo("descanso",cfg().descanso,p.mat);return}
      setPomo(null);notify("Se acabó el descanso","Cuando quieras, empieza otro bloque.");if(tab==="contador")render();
    }
    if(pill){const q=pomo();const vis=q&&$("#estudio")&&$("#estudio").hidden;pill.hidden=!vis;
      if(vis){pill.className=q.phase==="descanso"?"brk":"";pill.textContent=(q.paused!=null?"⏸ ":"⏱ ")+mmss(left(q))+" · "+(q.phase==="descanso"?"Descanso":(q.mat||"Estudio"))}}
    if(ready&&!$("#estudio").hidden&&tab==="contador")drawRing();
    const q=pomo();if(q&&ready&&!$("#estudio").hidden&&tab==="contador")document.title=mmss(left(q))+" · Estudio";
  }
  function drawRing(){
    const p=pomo(),r=$("#esRing");if(!r)return;const L=p?left(p):cfg().foco*60,len=p?p.len:cfg().foco*60,C=2*Math.PI*54;
    r.classList.toggle("brk",!!p&&p.phase==="descanso");
    r.querySelector(".fg").style.strokeDashoffset=String(C*(1-Math.max(0,L)/len));
    r.querySelector("b").textContent=mmss(L);
    r.querySelector("span").textContent=!p?"Listo para empezar":p.phase==="descanso"?"Descanso":p.paused!=null?"En pausa · "+(p.mat||"Sin materia"):(p.mat||"Sin materia");
  }
  function renderPomo(){
    const p=pomo(),c=cfg(),C=2*Math.PI*54,ms=materias(),cur=p?p.mat:(mat||nowClass()||"");
    $("#esPomo").innerHTML=`<h3>Contador de estudio</h3>
      <div class="es-ring" id="esRing"><svg viewBox="0 0 120 120"><circle class="bg" cx="60" cy="60" r="54"/><circle class="fg" cx="60" cy="60" r="54" stroke-dasharray="${C}" stroke-dashoffset="0"/></svg><div><b></b><span></span></div></div>
      ${p?`<div class="es-row" style="justify-content:center">${p.paused!=null?`<button class="cbtn" type="button" data-p="resume">Seguir</button>`:`<button class="cbtn" type="button" data-p="pause">Pausa</button>`}
        <button class="cbtn sec" type="button" data-p="stop">${p.phase==="descanso"?"Saltar descanso":"Terminar"}</button></div>
        ${p.phase==="foco"?`<p class="es-help" style="text-align:center">Si terminas antes, se guarda lo que llevas (desde 5 min).</p>`:""}`
      :`<form class="cform" id="esPForm"><label>Materia<select id="esPMat"><option value="">Sin materia</option>${ms.map(m=>`<option ${norm(m)===norm(cur)?"selected":""}>${esc(m)}</option>`).join("")}</select></label>
        <div class="es-presets">${[[25,5],[50,10],[90,15]].map(([f,d])=>`<button type="button" class="es-chip" data-pre="${f},${d}" aria-pressed="${c.foco===f&&c.descanso===d}">${f} + ${d} min</button>`).join("")}</div>
        <div class="btns" style="text-align:center"><button class="cbtn" type="submit">Empezar ${c.foco} min</button></div></form>`}`;
    drawRing();renderTime();
  }
  function renderTime(){
    const t=today(),tm=list(K.time),sum=l=>l.reduce((a,s)=>a+s.m,0);
    const by=new Map();for(const s of tm.filter(s=>diffD(s.d,t)<30)){const k=norm(s.mat);const o=by.get(k)||{mat:s.mat,m:0,w:0};o.m+=s.m;if(diffD(s.d,t)<7)o.w+=s.m;by.set(k,o)}
    const rows=[...by.values()].sort((a,b)=>b.m-a.m),mx=Math.max(1,...rows.map(r=>r.m));
    const exs=upcoming().filter(e=>diffD(t,e.date)<=21).slice(0,4).map(e=>{const m=examMat(e),from=addD(e.date,-Math.max(7,+e.lead||7));return {e,m,min:sum(tm.filter(s=>s.d>=from&&sameMat(s.mat,m)))}});
    const days=[...Array(7)].map((_,i)=>addD(t,i-6)),dm=days.map(d=>sum(tm.filter(s=>s.d===d))),dx=Math.max(1,...dm);
    $("#esTime").innerHTML=`<h3>Tus horas <small>de estudio</small></h3>
      <div class="es-stat"><div><b>${hm(sum(tm.filter(s=>s.d===t)))}</b><span>hoy</span></div><div><b>${hm(sum(tm.filter(s=>diffD(s.d,t)<7)))}</b><span>7 días</span></div><div><b>${hm(sum(tm.filter(s=>diffD(s.d,t)<30)))}</b><span>30 días</span></div></div>
      <div style="display:grid;grid-template-columns:repeat(7,1fr);gap:6px;align-items:end;height:90px;margin:4px 0 4px">${dm.map((m,i)=>`<div title="${nice(days[i])}: ${hm(m)}" style="height:${Math.max(3,m/dx*100)}%;background:${days[i]===t?"var(--orange)":"var(--green-3)"};border-radius:6px 6px 2px 2px;opacity:${m?1:.25}"></div>`).join("")}</div>
      <div style="display:grid;grid-template-columns:repeat(7,1fr);gap:6px;font:600 .66rem var(--f-mono);color:var(--muted);text-align:center">${days.map(d=>"DLMMJVS"[parseD(d).getDay()]).join("</span><span>").replace(/^/,"<span>")+"</span>"}</div>
      ${exs.length?`<h4 class="es-h4">Antes de tus exámenes</h4>${exs.map(x=>`<p class="es-help" style="margin:5px 0"><b>${esc(x.e.name)}</b> (${diffD(t,x.e.date)===0?"hoy":"en "+diffD(t,x.e.date)+" d"}) · llevas <b>${hm(x.min)}</b>${x.m?" de "+esc(x.m):""}</p>`).join("")}`:""}
      ${rows.length?`<h4 class="es-h4">Por materia (30 días)</h4><div class="es-bars">${rows.map(r=>`<div><span>${esc(r.mat)}</span><b>${hm(r.m)}</b><em><i style="width:${r.m/mx*100}%;background:var(--orange)"></i></em><small class="es-mut" style="grid-column:1/-1">${hm(r.w)} esta semana</small></div>`).join("")}</div>`:`<p class="es-mut">Usa el contador y aquí verás cuántas horas le metes a cada materia.</p>`}`;
  }
  function bindPomo(){
    $("#esPomo").addEventListener("click",ev=>{
      const pr=ev.target.closest("[data-pre]");if(pr){const [f,d]=pr.dataset.pre.split(",").map(Number);set(K.cfg,JSON.stringify(Object.assign(cfg(),{foco:f,descanso:d})));renderPomo();return}
      const b=ev.target.closest("[data-p]");if(!b)return;const p=pomo();if(!p)return;
      if(b.dataset.p==="pause"){p.paused=left(p);setPomo(p)}
      else if(b.dataset.p==="resume"){p.end=Date.now()+p.paused*1000;p.paused=null;setPomo(p)}
      else if(b.dataset.p==="stop"){if(p.phase==="foco"){const done=(p.len-left(p))/60;if(done>=5)logTime(p.mat,done)}setPomo(null);document.title="Estudio · Carrera de Medicina"}
      renderPomo();renderHero();
    });
    $("#esPomo").addEventListener("submit",ev=>{ev.preventDefault();startPomo("foco",cfg().foco,$("#esPMat").value)});
  }

  /* ===== Notas rápidas por clase ===== */
  function nowClass(){
    const h=list("carrera-horario"),d=new Date(),dow=(d.getDay()+6)%7,min=d.getHours()*60+d.getMinutes(),m=t=>{const x=/^(\d{1,2}):(\d{2})$/.exec(t||"");return x?+x[1]*60+ +x[2]:null};
    const c=h.find(x=>Array.isArray(x.days)&&x.days.includes(dow)&&m(x.start)!=null&&min>=m(x.start)-15&&min<=m(x.end)+45);return c?c.mat:"";
  }
  let editing=null,nq="";
  const safeName=s=>String(s).replace(/[\\/:*?"<>|#^\[\]]/g," ").replace(/\s+/g," ").trim().slice(0,90);
  const noteMd=n=>`---\nmateria: "${String(n.mat).replace(/"/g,"'")}"\nfecha: ${n.f}\ntags: [medicina, clase]\n---\n# ${n.t}\n\n${n.x}\n`;
  const obsUrl=n=>"obsidian://new?vault=CASA&file="+encodeURIComponent("Medicina/Notas de clase/"+safeName(n.mat||"Sin materia")+"/"+n.f+" "+safeName(n.t))+"&content="+encodeURIComponent(noteMd(n))+"&overwrite=true";
  function renderNotes(){
    const ns=list(K.notes).filter(n=>sameMat(n.mat,mat)&&(!nq||norm(n.t+" "+n.x+" "+n.mat).includes(norm(nq)))).sort((a,b)=>b.f.localeCompare(a.f)||b.u-a.u);
    const by=new Map();ns.forEach(n=>{const k=n.mat||"Sin materia";(by.get(k)||by.set(k,[]).get(k)).push(n)});
    const mac=location.protocol==="app:";
    const box=$("#esNotes"),focus=document.activeElement&&document.activeElement.id==="esNQ";
    box.innerHTML=`<h3>Tus notas <small>${list(K.notes).length} en total</small></h3>
      <input id="esNQ" type="search" placeholder="Buscar en tus notas…" value="${esc(nq)}" style="width:100%;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);border-radius:10px;padding:10px 12px;font:500 .95rem var(--f-display);margin-bottom:6px">
      ${ns.length?[...by].map(([m,l])=>`<h4 class="es-h4">${esc(m)} <small class="es-mut">(${l.length})</small></h4>${l.map(n=>`<details class="es-note"><summary><b>${esc(n.t)}</b><small>${nice(n.f)}${n.o?" · en Obsidian":""}</small></summary>
        <div class="es-x">${esc(n.x)}</div><div class="es-row">${mac?"":`<a class="mini" href="${esc(obsUrl(n))}" data-obs="${esc(n.id)}">Mandar a Obsidian</a>`}<button class="mini" type="button" data-copy="${esc(n.id)}">${mac?"Copiar para Obsidian":"Copiar"}</button><button class="mini" type="button" data-edit="${esc(n.id)}">Editar</button><button class="mini" type="button" data-ndel="${esc(n.id)}">Borrar</button></div></details>`).join("")}`).join("")
      :`<p class="es-mut">${nq?"No encontré notas con eso.":"Todavía no hay notas. Escribe la primera en clase: se guarda sola en tu Mac y tu cel."}</p>`}
      <p class="es-help" style="margin-top:12px">${mac?"En la app de Mac usa “Copiar para Obsidian” y pégala en tu bóveda CASA (Medicina › Notas de clase). Desde el cel o el navegador, “Mandar a Obsidian” la crea sola.":"“Mandar a Obsidian” la crea en tu bóveda CASA, en Medicina › Notas de clase › materia (necesitas Obsidian instalado en este aparato)."}</p>`;
    if(focus){const i=$("#esNQ");i.focus();i.setSelectionRange(i.value.length,i.value.length)}
    renderNForm();
  }
  function renderNForm(){
    const n=editing?list(K.notes).find(x=>x.id===editing):null,cls=nowClass(),d=new Date();
    const keep=$("#esNForm").querySelector("#esNX");if(keep&&!n&&keep.value&&document.activeElement===keep)return;
    $("#esNForm").innerHTML=`<h3>${n?"Editar nota":"Nota rápida"}${cls&&!n?` <small>en clase de ${esc(cls)}</small>`:""}</h3>
      <form class="cform" id="esNF" autocomplete="off">
        <div class="row2"><label>Materia<input id="esNM" list="esMatList" maxlength="80" value="${esc(n?n.mat:(cls||mat))}" required></label><label>Fecha<input id="esND" type="date" value="${n?n.f:today()}" required></label></div>
        <label>Título<input id="esNT" maxlength="120" value="${esc(n?n.t:"Clase del "+d.getDate()+" de "+["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"][d.getMonth()])}" required></label>
        <label>Nota<textarea class="es-ta" id="esNX" maxlength="40000" placeholder="Lo que dijo el profe, lo que viene en el examen, dudas…" required>${esc(n?n.x:(get("__medsync_notadraft")||""))}</textarea></label>
        <div class="btns"><button class="cbtn" type="submit">${n?"Guardar cambios":"Guardar nota"}</button>${n?` <button class="cbtn sec" type="button" id="esNCancel">Cancelar</button>`:""}</div></form>`;
  }
  function bindNotes(){
    $("#esNotes").addEventListener("input",ev=>{if(ev.target.id==="esNQ"){nq=ev.target.value;renderNotes()}});
    $("#esNotes").addEventListener("click",ev=>{
      const t=ev.target.closest("[data-copy],[data-edit],[data-ndel],[data-obs]");if(!t)return;
      const id=t.dataset.copy||t.dataset.edit||t.dataset.ndel||t.dataset.obs,items=list(K.notes),n=items.find(x=>x.id===id);if(!n)return;
      if(t.dataset.copy){const txt=noteMd(n);(navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(()=>{t.textContent="¡Copiada!"},()=>{t.textContent="No se pudo copiar"});return}
      if(t.dataset.obs){n.o=Date.now();saveList(K.notes,items);setTimeout(renderNotes,800);return}
      if(t.dataset.edit){editing=id;renderNForm();$("#esNX").focus();return}
      if(!t.classList.contains("warn")){t.classList.add("warn");t.textContent="¿Seguro?";return}
      saveList(K.notes,items.filter(x=>x.id!==id));if(editing===id)editing=null;renderNotes();
    });
    $("#esNForm").addEventListener("input",ev=>{if(ev.target.id==="esNX"&&!editing)set("__medsync_notadraft",ev.target.value)});
    $("#esNForm").addEventListener("click",ev=>{if(ev.target.id==="esNCancel"){editing=null;renderNForm()}});
    $("#esNForm").addEventListener("submit",ev=>{ev.preventDefault();
      const items=list(K.notes),v={mat:$("#esNM").value.trim(),f:$("#esND").value||today(),t:$("#esNT").value.trim(),x:$("#esNX").value,u:Date.now()};
      if(editing){const n=items.find(x=>x.id===editing);if(n)Object.assign(n,v,{o:0})}else items.push(Object.assign({id:uid("n")},v));
      saveList(K.notes,items);editing=null;set("__medsync_notadraft","");$("#esNX").value="";renderNotes();renderHero()});
  }

  /* ===== Calificaciones: ¿cuánto necesito sacar? (por materia, con el peso de cada parcial) ===== */
  const DEF=[["Parcial 1",25],["Parcial 2",25],["Parcial 3",25],["Final",25]];
  function calcMount(){
    const anchor=document.querySelector('#grades details[data-fold="gr-set"]');if(!anchor||document.getElementById("gpCalc"))return;
    anchor.insertAdjacentHTML("beforebegin",`<details class="ccard udet fold" data-fold="gr-parc" id="gpCalc"><summary><h3>¿Cuánto necesito sacar? <small>por materia</small></h3><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary>
      <form class="cform" autocomplete="off" onsubmit="return false"><div class="row2"><label>Materia<input id="gpMat" list="gpMats" maxlength="80" placeholder="Ej. Psiquiatría"><datalist id="gpMats"></datalist></label>
      <label>Tu meta<input id="gpMeta" type="number" min="0" max="10" step="0.1" inputmode="decimal" value="9"></label></div></form>
      <p class="gr-help">Pon el peso de cada evaluación (como viene en tu programa) y lo que sacaste. Deja vacía la calificación de lo que aún no presentas.</p>
      <table><thead><tr><th>Evaluación</th><th>Peso %</th><th>Calif.</th><th></th></tr></thead><tbody id="gpRows"></tbody></table>
      <div class="es-row" style="margin-top:8px;display:flex;gap:8px"><button class="mini" type="button" id="gpAdd">+ Evaluación</button></div>
      <div class="gp-out" id="gpOut"></div></details>`);
    const d=document.getElementById("gpCalc"),k="carrera-fold-gr-parc",v=get(k);if(v!=null)d.open=v==="1";d.addEventListener("toggle",()=>set(k,d.open?"1":"0"));
    const mi=$("#gpMat");$("#gpMats").innerHTML=[...new Set(CUR().concat(list(K.parc).map(x=>x.mat)))].map(m=>`<option value="${esc(m)}">`).join("");
    const first=list(K.parc).sort((a,b)=>(b.u||0)-(a.u||0))[0];mi.value=first?first.mat:(CUR()[1]||CUR()[0]||"");
    const rec=()=>{const m=mi.value.trim();return list(K.parc).find(x=>norm(x.mat)===norm(m))};
    function draw(){const r=rec(),evs=r?r.evs:DEF.map(([n,p])=>({n,p,c:""}));$("#gpMeta").value=r&&r.meta?r.meta:9;
      $("#gpRows").innerHTML=evs.map((e,i)=>`<tr data-i="${i}"><td><input data-f="n" value="${esc(e.n)}" maxlength="40"></td><td><input data-f="p" type="number" min="0" max="100" step="1" inputmode="numeric" value="${e.p===""?"":esc(e.p)}"></td><td><input data-f="c" type="number" min="0" max="10" step="0.1" inputmode="decimal" value="${e.c===""||e.c==null?"":esc(e.c)}"></td><td><button class="gp-x" type="button" data-rm="${i}" aria-label="Quitar">×</button></td></tr>`).join("");out()}
    function read(){return [...$("#gpRows").querySelectorAll("tr")].map(tr=>{const g=f=>tr.querySelector(`[data-f="${f}"]`).value;return {n:g("n"),p:g("p")===""?"":+g("p"),c:g("c")===""?"":Math.max(0,Math.min(10,+String(g("c")).replace(",",".")))}})}
    function save(){const m=mi.value.trim();if(!m)return;const items=list(K.parc).filter(x=>norm(x.mat)!==norm(m));items.push({id:norm(m).replace(/ /g,"-"),mat:m,meta:+$("#gpMeta").value||9,evs:read(),u:Date.now()});saveList(K.parc,items);out()}
    function out(){
      const evs=read(),min=(J("carrera-calificaciones",{}).min)||7.5,meta=+$("#gpMeta").value||9,f=n=>String(Number((+n).toFixed(2)));
      const P=evs.reduce((a,e)=>a+(+e.p||0),0),done=evs.filter(e=>e.c!==""&&+e.p>0),R=evs.filter(e=>e.c===""&&+e.p>0).reduce((a,e)=>a+ +e.p,0);
      const pts=done.reduce((a,e)=>a+e.c*e.p/100,0),wd=done.reduce((a,e)=>a+ +e.p,0);
      const need=g=>R>0?(g-pts)/(R/100):null;
      const line=(g,lbl)=>{const x=need(g);if(R===0)return pts>=g-1e-9?`✓ ${lbl} (${f(g)}): ya lo tienes.`:`✗ ${lbl} (${f(g)}): no se alcanzó.`;
        return x<=0?`✓ ${lbl} (${f(g)}): ya lo tienes asegurado aunque saques 0 en lo que falta.`:x>10?`✗ ${lbl} (${f(g)}): ya no alcanza ni con 10 (máximo posible: ${f(pts+R/10)}).`:`Para ${lbl.toLowerCase()} (${f(g)}) necesitas <b>${f(x)}</b> en promedio en lo que falta (${R}% de la calificación).`};
      $("#gpOut").innerHTML=(P!==100?`<p class="cerr">Los pesos suman ${P}%; deberían sumar 100%.</p>`:"")
        +(done.length?`<p>Llevas <b>${f(pts/(wd/100))}</b> en lo que ya presentaste (${wd}% de la materia, ${f(pts)} puntos de 10).</p>`:`<p class="gr-help">Pon al menos una calificación para calcular.</p>`)
        +(done.length?`<p>${line(min,"Pasar")}</p><p>${line(meta,"Tu meta")}</p>`:"");
    }
    mi.addEventListener("change",draw);
    $("#gpRows").addEventListener("input",save);$("#gpMeta").addEventListener("input",save);
    $("#gpRows").addEventListener("click",ev=>{const b=ev.target.closest("[data-rm]");if(!b)return;b.closest("tr").remove();save()});
    $("#gpAdd").addEventListener("click",()=>{$("#gpRows").insertAdjacentHTML("beforeend",`<tr><td><input data-f="n" value="Evaluación" maxlength="40"></td><td><input data-f="p" type="number" min="0" max="100" step="1" value=""></td><td><input data-f="c" type="number" min="0" max="10" step="0.1" value=""></td><td><button class="gp-x" type="button" data-rm="x">×</button></td></tr>`);save()});
    draw();
  }

  /* botón en la portada (junto a Calificaciones) */
  function button(){
    if(document.getElementById("esBtn"))return;const gr=document.getElementById("grBtn");if(!gr)return;
    gr.insertAdjacentHTML("afterend",`<a class="theme" id="esBtn" href="#estudio">${ICO.book}<span>Estudio</span></a>`);
  }
  function boot(){
    button();calcMount();
    if(!document.getElementById("esStyle0")){const s=document.createElement("style");s.id="esStyle0";s.textContent="@media (max-width:560px){#esBtn span{display:none}}";document.head.appendChild(s)}
    mount();
    if(location.hash==="#estudio")open();
    /* si el contador está corriendo, que se vea la píldora aunque no abras Estudio */
    tickPomo();
  }
  window.Estudio={open,close,examMat:e=>examMat(e)};
  if(document.readyState==="loading")addEventListener("DOMContentLoaded",boot);else boot();
})();
