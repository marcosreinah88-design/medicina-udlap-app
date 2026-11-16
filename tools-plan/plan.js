  /*plan2*/
  /* ---------- el plan de estudio por examen (v2) ----------
     Reparte los temas de cada examen entre los días que faltan según el tiempo que de verdad tienes:
     horas por día (entre semana, sábado, domingo), Mi horario (días con muchas clases = menos tiempo),
     el tiempo de tus pendientes, días sin clases UDLAP y días que marcas como "no puedo estudiar".
     Los exámenes más cercanos se acomodan primero; el siguiente usa lo que queda. Si te atrasas,
     los temas que no hiciste se vuelven a repartir solos y te aviso. Todo vive en state.plan (se sincroniza). */
  const PL_DIF={1:{l:"Fácil",f:.6},2:{l:"Normal",f:1},3:{l:"Difícil",f:1.6}};
  const PL_PEND={proyecto:[60,60],presentacion:[60,60],tarea:[45],lectura:[45],practica:[30],tramite:[20],otro:[30]};
  const PL_HIST="carrera-plan-hist";
  let PL={cap:{},used:{},info:{},at:{},late:new Set(),lateIt:[],over:[]},plOpen=new Set(),plAiMsg={};
  function planClean(p){
    const o={cfg:{},off:{},pin:{},dif:{}},src=p&&typeof p==="object"?p:{},c=src.cfg&&typeof src.cfg==="object"?src.cfg:{};
    const num=(v,a,b,d)=>{v=v==null||v===""?NaN:+v;return v===v?Math.max(a,Math.min(b,Math.round(v))):d};
    o.cfg={wd:num(c.wd,0,720,120),sa:num(c.sa,0,720,180),su:num(c.su,0,720,150),tm:num(c.tm,15,240,60),hor:c.hor===0?0:1,pen:c.pen===0?0:1,rev:c.rev===0?0:1};
    const dt=/^\d{4}-\d{2}-\d{2}$/;
    if(src.off&&typeof src.off==="object")Object.keys(src.off).filter(k=>dt.test(k)).sort().slice(-200).forEach(k=>o.off[k]=1);
    if(src.pin&&typeof src.pin==="object")for(const k of Object.keys(src.pin).slice(0,400))if(k.length<240&&dt.test(src.pin[k]))o.pin[k]=src.pin[k];
    if(src.dif&&typeof src.dif==="object")for(const k of Object.keys(src.dif).slice(0,1500))if(k.length<240&&(src.dif[k]===1||src.dif[k]===3))o.dif[k]=src.dif[k];
    return o;
  }
  function planMerge(st,local){
    /* la cuenta no tenía plan todavía: se queda el de este aparato */
    const lp=local&&local.plan;if(!lp)return;
    const empty=p=>!p||(!Object.keys(p.off).length&&!Object.keys(p.pin).length&&!Object.keys(p.dif).length&&JSON.stringify(p.cfg)===JSON.stringify(planClean().cfg));
    if(empty(st.plan)&&!empty(lp))st.plan=lp;
  }
  function planPrune(lim,keep){
    const P=state.plan||(state.plan=planClean()),t=today();
    for(const k in P.off)if(k<lim)delete P.off[k];
    for(const k in P.pin)if(P.pin[k]<t||!keep.has(k.split("|")[0]))delete P.pin[k];
    for(const k in P.dif)if(!keep.has(k.split("|")[0]))delete P.dif[k];
  }
  const plC=()=>(state.plan||(state.plan=planClean())).cfg;
  const plDur=m=>{m=Math.round(m/5)*5;if(m<60)return m+" min";const h=Math.floor(m/60),r=m%60;return h+" h"+(r?" "+r:"")};
  /* horas de clase de un día según Mi horario (0 = lunes) */
  function plClassH(wd){
    try{const v=JSON.parse(store.get("carrera-horario")||"null");if(!v||!Array.isArray(v.items))return 0;
      const mn=s=>{const m=/^(\d{1,2}):(\d{2})$/.exec(s||"");return m?+m[1]*60+ +m[2]:null};
      return v.items.reduce((a,x)=>{const s=mn(x.start),e=mn(x.end);return a+(Array.isArray(x.days)&&x.days.map(Number).includes(wd)&&s!=null&&e>s?(e-s)/60:0)},0)}catch(e){return 0}
  }
  /* minutos para estudiar ese día (antes de pendientes y otros exámenes) */
  function planBase(d){
    const c=plC(),P=state.plan;if(P.off[d])return 0;
    const wd=parse(d).getDay();let m=wd===6?c.sa:wd===0?c.su:c.wd;
    if(wd>0&&wd<6&&(UD[d]||[]).some(ev=>ev.k==="asueto"||ev.k==="vacaciones"))m=Math.max(m,c.sa);
    else if(c.hor&&wd>0&&m>0){const h=plClassH(wd-1);if(h>4)m=Math.max(30,m-Math.round((h-4)*30/5)*5)}
    return m;
  }
  function planLate(t){
    let H={};try{H=JSON.parse(store.get(PL_HIST)||"{}")||{}}catch(e){}
    const lim=ymd(add(parse(t),-14)),late=new Set();
    for(const d in H){if(d<lim||!Array.isArray(H[d])){delete H[d];continue}
      if(d<t)for(const k of H[d]){const [id,,i]=String(k).split(":"),e=state.exams.find(x=>x.id===id);
        if(e&&e.date>=t&&+i<e.topics.length&&!state.done[k])late.add(k)}}
    return {H,late};
  }
  function build(){
    const t=today(),days={},c=plC(),P=state.plan;
    const cap={},used={},info={},at={};
    const capOf=d=>cap[d]!=null?cap[d]:(cap[d]=planBase(d));
    const use=(d,m)=>{capOf(d);used[d]=(used[d]||0)+m};
    const left=d=>capOf(d)-(used[d]||0);
    const push=(d,item)=>{item.day=d;(days[d]=days[d]||[]).push(item)};
    const late=planLate(t).late;
    /* pendientes: salen en su día y se descuenta su tiempo de los días antes de la entrega */
    for(const p of state.tasks){if(p.done||!p.due)continue;
      push(p.due<t?t:p.due,{kind:"pend",p,e:{date:p.due,color:PT[p.type].c},text:p.title,key:null});
      if(c.pen&&p.due>=t&&p.flag!=="delegar"&&p.flag!=="eliminar")(PL_PEND[p.type]||[30]).forEach((m,i)=>{let d=ymd(add(parse(p.due),-(i+1)));if(d<t)d=t;use(d,m)});}
    const exams=state.exams.filter(e=>e.date>=t).sort((a,b)=>a.date.localeCompare(b.date)||a.id.localeCompare(b.id));
    for(const e of exams){
      push(e.date,{e,kind:"exam",text:"Examen: "+e.name,key:null});
      const start=[ymd(add(parse(e.date),-e.lead)),t].sort().pop(),n=diff(start,e.date);
      const tk=i=>e.id+":t:"+i;
      const I=info[e.id]={total:e.topics.length,done:e.topics.filter((x,i)=>state.done[tk(i)]).length,mins:0,days:0,late:0,over:0,start};
      if(n<=0)continue;
      const revDay=c.rev&&n>=3?ymd(add(parse(e.date),-1)):null,D=[];
      for(let k=0;k<n;k++){const d=ymd(add(parse(start),k));if(d!==revDay)D.push(d)}
      I.days=D.filter(d=>capOf(d)>0).length;
      if(revDay){const m=Math.max(45,Math.min(120,Math.round(e.topics.length*c.tm*.15/15)*15));
        if(!state.done[e.id+":r"])use(revDay,m);push(revDay,{e,kind:"review",text:"Repaso general de "+e.name,sub:"Todos los temas + un simulacro o quiz",key:e.id+":r",min:m})}
      if(!e.topics.length){
        for(const d of D){if(capOf(d)<=0)continue;const m=Math.max(30,Math.min(c.tm,left(d)));if(!state.done[e.id+":s:"+d])use(d,m);I.mins+=m;
          push(d,{e,kind:"study",text:"Estudiar "+e.name,sub:"Avanza con tus apuntes o la guía",key:e.id+":s:"+d,min:m})}
        continue}
      const place=(d,o)=>{if(!state.done[o.key]){use(d,o.m);I.mins+=o.m}at[o.key]=d;
        push(d,{e,kind:"topic",text:o.x,sub:e.name,key:o.key,topic:o.x,min:o.m,dif:o.dif,late:late.has(o.key)})};
      const free=[];
      e.topics.forEach((x,i)=>{const dif=P.dif[e.id+"|"+x]||2,o={x,i,key:tk(i),dif,m:Math.round(c.tm*PL_DIF[dif].f/5)*5},dn=state.done[o.key];
        if(dn&&dn<t)return;
        if(dn){place(t,o);return}
        const pd=P.pin[e.id+"|"+x];if(pd&&pd>=t&&pd<e.date){place(pd,o);return}
        free.push(o)});
      if(free.length&&D.length){
        /* reparte según el tiempo libre que queda cada día; si no alcanza, el exceso se reparte parejo */
        const T=free.reduce((a,o)=>a+o.m,0);let w=D.map(d=>Math.max(0,left(d))),W=w.reduce((a,b)=>a+b,0);
        if(W<T){const ok=D.map(d=>capOf(d)>0?1:0),nOk=ok.reduce((a,b)=>a+b,0),ex=(T-W)/(nOk||D.length);w=w.map((x,j)=>x+(nOk?ok[j]:1)*ex)}
        const cum=[];let s=0;for(const x of w){s+=x;cum.push(s)}
        let acc=0;for(const o of free){const mid=(acc+o.m/2)/T*s;acc+=o.m;let j=cum.findIndex(v=>v>mid);if(j<0)j=D.length-1;place(D[j],o)}
      }else if(free.length){free.forEach(o=>place(t,o))}
      /* días de estudio sin tema nuevo: repaso de lo ya visto */
      let seen=I.done>0;
      for(const d of D){const has=(days[d]||[]).some(x=>x.e===e&&x.kind==="topic");if(has){seen=true;continue}
        if(capOf(d)<=0)continue;
        if(seen)push(d,{e,kind:"study",text:(I.done===I.total?"Repasar ":"Repasar lo visto de ")+e.name,sub:I.done===I.total?"Ya cubriste todos los temas: practica con preguntas":"Flashcards o preguntas de los temas anteriores",key:e.id+":s:"+d})}
      I.late=e.topics.filter((x,i)=>late.has(tk(i))).length;
    }
    const over=[];
    for(const d in used)if(d>=t&&used[d]>capOf(d)+15)over.push(d);
    for(const e of exams){const I=info[e.id];if(I)I.over=over.filter(d=>d>=I.start&&d<e.date&&(days[d]||[]).some(x=>x.e===e&&x.kind==="topic")).length}
    const order={exam:0,pend:1,review:2,topic:3,study:4};
    for(const d in days)days[d].sort((a,b)=>a.e.date.localeCompare(b.e.date)||order[a.kind]-order[b.kind]);
    PL={cap,used,info,at,late,over:over.sort(),capOf};
    return days;
  }
  /* carga del día junto al título del día en el plan */
  function planLoad(d){
    const u=Math.round(PL.used[d]||0),c=PL.capOf?PL.capOf(d):0,P=state.plan;
    if(P&&P.off[d])return `<span class="pl-load off">No estudias este día</span>`;
    if(!u&&!c)return "";
    const over=u>c+15;
    return `<span class="pl-load${over?" over":""}" title="Tiempo planeado de estudio y pendientes / tiempo que tienes ese día"><i style="--p:${c?Math.min(100,Math.round(u/c*100)):100}%"></i>${plDur(u)} de ${plDur(c)}</span>`;
  }
  function planActs(it,done){
    if(it.kind!=="topic"||done)return "";
    const tm=ymd(add(parse(it.day<today()?today():it.day),1));
    return tm<it.e.date?`<button type="button" class="mini pl-mv" data-plmv="${esc(it.e.id+"|"+it.topic)}" data-pld="${tm}" title="Pasar este tema al día siguiente">${it.day<=today()?"Mañana":"Un día después"}</button>`:"";
  }
  function planMeta(it){
    return [it.sub,it.min?"≈ "+plDur(it.min):"",it.kind==="topic"&&it.dif&&it.dif!==2?PL_DIF[it.dif].l:""].filter(Boolean).join(" · ");
  }
  const plOkAI=()=>{try{return (location.protocol==="app:"||/github\.io$/.test(location.hostname)||/^(localhost|127\.0\.0\.1)$/.test(location.hostname))}catch(e){return false}};
  const plKey=()=>{try{return localStorage.getItem("__medsync_gemkey")}catch(e){return null}};
  function planTop(t){
    const P=state.plan,c=P.cfg,up=state.exams.filter(e=>e.date>=t).sort((a,b)=>a.date.localeCompare(b.date));
    const det=(id,sum,body,cls)=>`<details class="${cls||"pl-det"}" data-plo="${id}"${plOpen.has(id)?" open":""}><summary>${sum}</summary>${body}</details>`;
    let h="";
    const lateIt=[...PL.late];
    if(lateIt.length)h+=`<div class="pl-note late"><b>Te ${lateIt.length===1?"quedó 1 tema":"quedaron "+lateIt.length+" temas"} sin hacer de días pasados.</b> Ya ${lateIt.length===1?"lo reacomodé":"los reacomodé"} en los días que quedan antes del examen.<span class="pl-btns"><button type="button" class="mini" data-plact="hoy">Ponerlos hoy</button><button type="button" class="mini" data-plact="ok">Entendido</button></span></div>`;
    if(PL.over.length){const d0=PL.over[0],u=PL.used[d0]||0,cp=PL.capOf(d0);
      h+=`<div class="pl-note over"><b>No te alcanza el tiempo ${PL.over.length===1?"un día":PL.over.length+" días"}.</b> El ${esc(nice(d0))} tienes ${plDur(u)} planeadas y solo ${plDur(cp)} libres. Puedes empezar antes (edita el examen y cambia «Empezar a estudiar»), subir tus horas abajo o marcar temas como fáciles.</div>`}
    if(up.length){
      h+=`<div class="pl-exs">`+up.map(e=>{const I=PL.info[e.id]||{total:e.topics.length,done:0,mins:0,days:0,late:0,over:0},n=diff(t,e.date);
        const pct=I.total?Math.round(I.done/I.total*100):0,per=I.days?I.mins/I.days:0;
        const st=I.late?`<em class="pl-st bad">${I.late} atrasado${I.late>1?"s":""}</em>`:I.over?`<em class="pl-st warn">Apretado</em>`:I.total&&I.done===I.total?`<em class="pl-st ok">Temas listos</em>`:`<em class="pl-st ok">Al día</em>`;
        const line=I.total?`${I.done} de ${I.total} temas · ${I.mins?"faltan ≈ "+plDur(I.mins)+(per?" · ≈ "+plDur(per)+" al día":""):"nada pendiente"}`:"Sin temas: agrega los temas al editar el examen para repartirlos por día";
        const rows=e.topics.map((x,i)=>{const k=e.id+":t:"+i,dn=state.done[k],dif=P.dif[e.id+"|"+x]||2,d=PL.at[k];
          return `<div class="pl-tr${dn?" done":""}${PL.late.has(k)&&!dn?" late":""}"><input type="checkbox" data-key="${esc(k)}"${dn?" checked":""} aria-label="Marcar ${esc(x)} como estudiado"><span>${esc(x)}<small>${dn?"hecho "+esc(nice(dn)):d?esc(nice(d))+(d===t?" · hoy":""):""}</small></span><button type="button" class="pl-dif d${dif}" data-pldif="${esc(e.id+"|"+x)}" title="Toca para cambiar: Fácil, Normal, Difícil">${PL_DIF[dif].l}</button></div>`}).join("");
        const ai=!e.topics.length?"":plKey()&&plOkAI()?`<div class="pl-ai"><button type="button" class="mini" data-plai="${esc(e.id)}"${plAiMsg[e.id]==="…"?" disabled":""}>${plAiMsg[e.id]==="…"?"Calculando…":"Calcular dificultad con Gemini"}</button>${plAiMsg[e.id]&&plAiMsg[e.id]!=="…"?`<small>${esc(plAiMsg[e.id])}</small>`:""}</div>`:plOkAI()?`<p class="pl-hint">Si guardas tu clave gratis de Gemini en el Asistente (Pendientes), aquí puedo estimar qué temas son más largos.</p>`:"";
        return `<div class="pl-ex" style="--c:${e.color}"><div class="pl-eh"><b>${esc(e.name)}</b>${st}</div><small class="pl-ed">${esc(nice(e.date))} · ${n===0?"hoy":rel(n).toLowerCase()}</small>${I.total?`<div class="prog"><i style="width:${pct}%"></i></div>`:""}<small class="pl-el">${esc(line)}</small>`+
          (e.topics.length?det("t:"+e.id,"Temas y dificultad",`<p class="pl-hint">Los difíciles cuentan más tiempo (≈ ${plDur(c.tm*1.6)}), los fáciles menos (≈ ${plDur(c.tm*.6)}).</p>${rows}${ai}`):"")+`</div>`}).join("")+`</div>`;
    }
    const opt=(v,list)=>list.map(m=>`<option value="${m}"${m===v?" selected":""}>${m?plDur(m):"Nada"}</option>`).join("");
    const H=[0,30,60,90,120,150,180,210,240,300,360,480],TM=[30,45,60,75,90,120];
    const sw=(k,b,s)=>`<label class="pl-sw"><input type="checkbox" data-plc="${k}"${c[k]?" checked":""}><i></i><span><b>${b}</b><small>${s}</small></span></label>`;
    const offs=Object.keys(P.off).filter(d=>d>=t).sort();
    h+=det("cfg",`Ajustar mi plan <small>${plDur(c.wd)} entre semana · ${plDur(c.sa)} sáb · ${plDur(c.su)} dom</small>`,
      `<div class="pl-cfg"><label>Lunes a viernes<select data-plc="wd">${opt(c.wd,H)}</select></label><label>Sábado<select data-plc="sa">${opt(c.sa,H)}</select></label><label>Domingo<select data-plc="su">${opt(c.su,H)}</select></label><label>Un tema normal<select data-plc="tm">${opt(c.tm,TM)}</select></label></div>`+
      sw("hor","Usar Mi horario","Los días con más de 4 h de clase te dejo menos tiempo")+sw("pen","Contar mis pendientes","Resto el tiempo de tareas, proyectos y lecturas antes de su entrega")+sw("rev","Repaso general un día antes","El día antes del examen solo repasas")+
      `<p class="pl-hint">Días sin clases UDLAP cuentan como sábado. Para un día en que no puedas estudiar, tócalo en el calendario de «Mis exámenes».</p>`+
      (offs.length?`<div class="pl-offs">${offs.map(d=>`<button type="button" class="mini" data-ploff="${d}" title="Quitar">${esc(nice(d))} ✕</button>`).join("")}</div>`:"")+
      (Object.keys(P.pin).length?`<button type="button" class="linkbtn" data-plact="unpin">Quitar los temas que moví a mano (${Object.keys(P.pin).length})</button>`:""),"pl-det pl-cfgd");
    return `<div class="pl-top">${h}</div>`;
  }
  function planRender(t,days){
    /* guarda qué temas tocaban hoy (para avisarte mañana si se quedó alguno) */
    try{const {H}=planLate(t);H[t]=(days[t]||[]).filter(x=>x.kind==="topic").map(x=>x.key);const v=JSON.stringify(H);if(store.get(PL_HIST)!==v)store.set(PL_HIST,v)}catch(e){}
    const box=$("#calPlan");if(!box)return;
    box.insertAdjacentHTML("afterbegin",planTop(t));
    const sub=$("#calPlanSub");if(sub&&PL.late.size)sub.textContent=PL.late.size+" atrasado"+(PL.late.size>1?"s":"")+" · reacomodado"+(PL.late.size>1?"s":"");
    else if(sub&&PL.over.length)sub.textContent="no te alcanza el tiempo";
  }
  function planToday(t){
    const box=$("#calToday");if(!box||!PL.late.size)return;
    box.insertAdjacentHTML("beforeend",`<p class="pl-tnote">${PL.late.size===1?"1 tema atrasado ya está":PL.late.size+" temas atrasados ya están"} reacomodado${PL.late.size>1?"s":""} en tu plan. <button type="button" class="linkbtn" data-plact="hoy">Ponerlos hoy</button></p>`);
  }
  function planDay(box,d){
    if(!d||d<today())return;const off=!!state.plan.off[d],c=PL.capOf?PL.capOf(d):0,u=PL.used[d]||0;
    box.insertAdjacentHTML("beforeend",`<div class="pl-dayb"><small>${off?"Marcaste que no estudias este día.":"Tiempo para estudiar: "+plDur(c)+(u?" · planeado "+plDur(u):"")}</small><button type="button" class="mini" data-ploff="${d}">${off?"Sí puedo estudiar este día":"No puedo estudiar este día"}</button></div>`);
  }
  async function planAI(id){
    const e=state.exams.find(x=>x.id===id),key=plKey();if(!e||!key||!e.topics.length)return;
    plAiMsg[id]="…";render();
    const prompt=`Eres tutor de un estudiante de Medicina (UDLAP, México) que prepara el examen "${e.name}". Para cada tema estima cuánto cuesta estudiarlo comparado con un tema típico de esa materia: 1 = corto o fácil, 2 = normal, 3 = largo o difícil (mucha fisiopatología, clasificaciones, fármacos o dosis). Temas:\n`+e.topics.map((x,i)=>i+". "+x).join("\n");
    const S=(type,x)=>Object.assign({type},x||{});
    const body=JSON.stringify({contents:[{role:"user",parts:[{text:prompt}]}],generationConfig:{responseMimeType:"application/json",temperature:.2,
      responseSchema:S("OBJECT",{properties:{temas:S("ARRAY",{items:S("OBJECT",{properties:{i:S("INTEGER"),d:S("INTEGER")},required:["i","d"]})})},required:["temas"]})}});
    let msg="";
    try{
      let r;for(const m of ["gemini-flash-latest","gemini-3.8-flash","gemini-2.5-flash"]){r=await fetch("https://generativelanguage.googleapis.com/v1beta/models/"+m+":generateContent",{method:"POST",headers:{"content-type":"application/json","x-goog-api-key":key},body});if(r.status!==404)break}
      if(r.status===429)throw new Error("Llegaste al límite gratis de Gemini por ahora; intenta en un rato.");
      if(!r.ok)throw new Error("Gemini respondió con error "+r.status+".");
      const j=await r.json(),tx=(((j.candidates||[])[0]||{}).content||{}).parts;const x=JSON.parse((tx||[]).map(p=>p.text||"").join("").replace(/^```(json)?|```$/g,"").trim());
      let n=0;const P=state.plan;
      for(const o of x.temas||[]){const i=+o.i,d=+o.d;if(!(i>=0&&i<e.topics.length)||![1,2,3].includes(d))continue;const k=e.id+"|"+e.topics[i];if(d===2)delete P.dif[k];else P.dif[k]=d;n++}
      msg=n?"Listo: Gemini calificó "+n+" temas. Puedes cambiar cualquiera tocándolo.":"Gemini no regresó temas; intenta otra vez.";
    }catch(err){msg=err&&err.message&&!/JSON|Unexpected/.test(err.message)?err.message:(navigator.onLine===false?"Sin conexión: esto necesita internet.":"No entendí la respuesta de Gemini; intenta otra vez.")}
    plAiMsg[id]=msg;save();
  }
  (()=>{
    const css=`.pl-top{display:grid;gap:10px;margin:0 0 16px}
.pl-note{border-radius:12px;padding:10px 12px;font-size:.86rem;line-height:1.4;border:1px solid var(--line);border-left:4px solid var(--orange);background:color-mix(in srgb,var(--orange) 7%,var(--paper))}
.pl-note.over{border-left-color:#c0392b;background:color-mix(in srgb,#c0392b 7%,var(--paper))}
.pl-note b{display:block;margin-bottom:2px}.pl-btns{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}.pl-btns .mini{margin:0}
.pl-exs{display:grid;gap:10px}
.pl-ex{border:1px solid var(--line);border-left:4px solid var(--c);border-radius:12px;padding:10px 12px;background:color-mix(in srgb,var(--c) 4%,var(--paper));display:grid;gap:5px;min-width:0}
.pl-eh{display:flex;justify-content:space-between;align-items:baseline;gap:8px}.pl-eh b{min-width:0;overflow-wrap:anywhere;line-height:1.25}
.pl-ed,.pl-el{color:var(--muted);font-size:.78rem;line-height:1.35}
.pl-ex .prog{height:5px;border-radius:9px;background:var(--line);overflow:hidden}.pl-ex .prog i{display:block;height:100%;background:var(--c)}
.pl-st{flex:none;font:700 .62rem var(--f-mono);letter-spacing:.06em;text-transform:uppercase;font-style:normal;padding:3px 8px;border-radius:99px;white-space:nowrap}
.pl-st.ok{background:color-mix(in srgb,var(--green-3) 15%,transparent);color:var(--go)}.pl-st.warn{background:color-mix(in srgb,var(--orange) 18%,transparent);color:var(--orange-2)}.pl-st.bad{background:color-mix(in srgb,#c0392b 16%,transparent);color:#c0392b}
.pl-det>summary{cursor:pointer;font:700 .84rem var(--f-display);color:var(--go);padding:4px 0;list-style:none;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.pl-det>summary::-webkit-details-marker{display:none}.pl-det>summary::before{content:"▸";display:inline-block;transition:transform .15s}.pl-det[open]>summary::before{transform:rotate(90deg)}
.pl-det>summary small{font:600 .68rem var(--f-mono);color:var(--muted);letter-spacing:.04em}
.pl-cfgd{border:1px dashed var(--line);border-radius:12px;padding:8px 12px}
.pl-tr{display:flex;align-items:center;gap:9px;padding:6px 0;border-top:1px solid var(--line);font-size:.86rem}
.pl-tr:first-of-type{border-top:0}.pl-tr input{flex:none;width:18px;height:18px;accent-color:var(--orange);margin:0;cursor:pointer}
.pl-tr span{flex:1;min-width:0;overflow-wrap:anywhere;line-height:1.3}.pl-tr span small{display:block;color:var(--muted);font-size:.72rem}
.pl-tr.done span{text-decoration:line-through;opacity:.6}.pl-tr.late span small{color:#c0392b;font-weight:600}
.pl-dif{flex:none;border:1.5px solid var(--line);background:var(--paper);color:var(--ink);border-radius:99px;padding:4px 10px;font:700 .72rem var(--f-display);cursor:pointer;min-width:66px;min-height:30px}
.pl-dif.d1{border-color:color-mix(in srgb,var(--green-3) 55%,var(--line));color:var(--go)}.pl-dif.d3{border-color:color-mix(in srgb,#c0392b 55%,var(--line));color:#c0392b}
.pl-ai{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:6px}.pl-ai .mini{margin:0}.pl-ai small{color:var(--muted);font-size:.76rem}
.pl-hint{margin:4px 0 6px;color:var(--muted);font-size:.76rem;line-height:1.4}
.pl-cfg{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin:6px 0 8px}
.pl-cfg label{display:grid;gap:4px;font:700 .74rem var(--f-display);color:var(--muted)}
.pl-cfg select{width:100%;min-width:0;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);border-radius:10px;padding:7px 8px;font:700 .86rem var(--f-display)}
@media (max-width:560px){.pl-cfg{grid-template-columns:1fr 1fr}}
.pl-sw{display:flex;align-items:center;gap:12px;padding:8px 0;border-top:1px solid var(--line);cursor:pointer}
.pl-sw input{position:absolute;opacity:0;pointer-events:none}.pl-sw i{flex:none;width:40px;height:24px;border-radius:99px;background:var(--line);position:relative;transition:background .2s}
.pl-sw i::after{content:"";position:absolute;top:3px;left:3px;width:18px;height:18px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.25);transition:transform .2s}
.pl-sw input:checked+i{background:var(--green-3)}.pl-sw input:checked+i::after{transform:translateX(16px)}.pl-sw input:focus-visible+i{outline:2px solid var(--orange);outline-offset:2px}
.pl-sw span{min-width:0}.pl-sw b{display:block;font-size:.86rem}.pl-sw small{display:block;color:var(--muted);font-size:.74rem;line-height:1.35}
.pl-offs{display:flex;flex-wrap:wrap;gap:6px}.pl-offs .mini{margin:0}
.pl-load{margin-left:auto;display:inline-flex;align-items:center;gap:6px;font:600 .68rem var(--f-mono);color:var(--muted);white-space:nowrap}
.pl-load i{width:42px;height:5px;border-radius:9px;background:var(--line);overflow:hidden;position:relative}.pl-load i::after{content:"";position:absolute;inset:0 auto 0 0;width:var(--p);background:var(--green-3);border-radius:9px}
.pl-load.over{color:#c0392b}.pl-load.over i::after{background:#c0392b}.pl-load.off{font-style:italic}
.task.late{border-color:color-mix(in srgb,#c0392b 40%,var(--line))}.pl-late{font-style:normal;font:700 .6rem var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:#fff;background:#c0392b;border-radius:99px;padding:2px 7px;margin-left:6px;vertical-align:2px}
.task .mini.pl-mv{flex:none;margin:0;align-self:center}
.pl-tnote{margin:10px 0 0;font-size:.84rem;color:var(--muted)}
.pl-dayb{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;margin-top:10px;padding-top:8px;border-top:1px dashed var(--line)}.pl-dayb small{color:var(--muted);font-size:.78rem}.pl-dayb .mini{margin:0}
@media (prefers-reduced-motion:reduce){.pl-det>summary::before,.pl-sw i,.pl-sw i::after{transition:none}}`;
    const st=document.createElement("style");st.id="plCss";st.textContent=css;document.head.appendChild(st);
    const cal=document.getElementById("cal");if(!cal)return;
    cal.addEventListener("toggle",ev=>{const d=ev.target;if(d&&d.dataset&&d.dataset.plo){if(d.open)plOpen.add(d.dataset.plo);else plOpen.delete(d.dataset.plo)}},true);
    cal.addEventListener("click",ev=>{
      const P=state.plan,t=today();let b;
      if(b=ev.target.closest("[data-plmv]")){ev.preventDefault();P.pin[b.dataset.plmv]=b.dataset.pld;save();return}
      if(b=ev.target.closest("[data-pldif]")){ev.preventDefault();const k=b.dataset.pldif,v=P.dif[k]||2,nx=v===2?3:v===3?1:2;if(nx===2)delete P.dif[k];else P.dif[k]=nx;save();return}
      if(b=ev.target.closest("[data-ploff]")){ev.preventDefault();const d=b.dataset.ploff;if(P.off[d])delete P.off[d];else P.off[d]=1;save();return}
      if(b=ev.target.closest("[data-plai]")){ev.preventDefault();planAI(b.dataset.plai);return}
      if(b=ev.target.closest("[data-plact]")){ev.preventDefault();const a=b.dataset.plact;
        if(a==="unpin"){P.pin={};save();return}
        if(a==="hoy"){for(const k of PL.late){const [id,,i]=k.split(":"),e=state.exams.find(x=>x.id===id);if(e&&e.topics[+i]!=null&&t<e.date)P.pin[id+"|"+e.topics[+i]]=t}}
        if(a==="hoy"||a==="ok"){try{const {H}=planLate(t);for(const d in H)if(d<t)H[d]=H[d].filter(k=>!PL.late.has(k));store.set(PL_HIST,JSON.stringify(H))}catch(e){}}
        save();return}
    });
    cal.addEventListener("change",ev=>{const s=ev.target.closest("[data-plc]");if(!s)return;const k=s.dataset.plc;
      state.plan.cfg[k]=s.type==="checkbox"?(s.checked?1:0):+s.value;save()});
  })();
  /*/plan2*/
