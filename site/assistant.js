/* Medicina UDLAP · asistente con IA: lee una foto, PDF o texto y propone pendientes y exámenes para el calendario.
   Usa Gemini de Google con la clave gratis de Marcos (Google AI Studio), guardada solo en este aparato. */
(()=>{
  const okHost=location.protocol==="app:"||/github\.io$/.test(location.hostname)||/^(localhost|127\.0\.0\.1)$/.test(location.hostname);
  if(!okHost)return;
  const API=window.__MEDAI_API||"https://generativelanguage.googleapis.com/v1beta/models/",MODELS=["gemini-flash-latest","gemini-3.8-flash","gemini-2.5-flash"],KEY="__medsync_gemkey";
  const get=k=>{try{return localStorage.getItem(k)}catch(e){return null}},set=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}},del=k=>{try{localStorage.removeItem(k)}catch(e){}};
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const ymd=d=>d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
  const DIAS=["domingo","lunes","martes","miércoles","jueves","viernes","sábado"];
  let files=[],props=null,busy=false;

  const css=`.aib{display:inline-flex;align-items:center;gap:7px;margin:2px 0 6px 8px;cursor:pointer;font:700 .9rem var(--f-display);color:#fff;border:0;border-radius:999px;padding:8px 14px;background:linear-gradient(135deg,#00543c,#0a6b4e);box-shadow:0 4px 12px rgba(0,84,60,.25)}
.aib svg{width:17px;height:17px}.aibox h4 svg{width:18px;height:18px;flex:none;color:var(--orange,#f26b21)}.aibox{border:1.5px solid color-mix(in srgb,var(--green-3,#0a6b4e) 40%,var(--line));border-radius:14px;padding:14px;margin:8px 0 12px;background:color-mix(in srgb,var(--green-3,#0a6b4e) 5%,transparent)}
.aibox h4{margin:0 0 4px;font:800 1rem var(--f-display);display:flex;align-items:center;gap:8px}.aibox p{margin:4px 0;font-size:.86rem;line-height:1.45}.aibox .mut{color:var(--muted)}
.aibox textarea,.aibox input[type=password]{width:100%;box-sizing:border-box;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);border-radius:10px;padding:10px 12px;font:500 .93rem var(--f-display);margin-top:8px}
.aibox textarea{min-height:84px;resize:vertical}.aibox .row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:8px}
.aibox button{border:0;border-radius:999px;padding:8px 15px;font:700 .85rem var(--f-display);cursor:pointer;background:var(--orange,#f26b21);color:#fff}.aibox button.sec{background:transparent;color:var(--ink);border:1.5px solid var(--line)}
.aibox button:disabled{opacity:.55;cursor:default}.aibox .chip{display:inline-flex;align-items:center;gap:6px;font-size:.78rem;border:1px solid var(--line);border-radius:999px;padding:3px 6px 3px 10px}
.aibox .chip b{cursor:pointer;font-weight:800;padding:0 4px}.aibox ol{margin:6px 0;padding-left:20px;font-size:.86rem}.aibox a{color:var(--orange,#f26b21);font-weight:700}
.aibox .err{color:#c0392b;font-weight:600}.aiitem{display:flex;gap:10px;align-items:flex-start;padding:9px 10px;border:1px solid var(--line);border-left:4px solid var(--c);border-radius:10px;margin-top:7px;background:var(--paper)}
.aiitem input{margin-top:3px;width:18px;height:18px;accent-color:var(--orange,#f26b21);flex:none}.aiitem b{display:block;font-size:.92rem}.aiitem small{color:var(--muted);font-size:.78rem}
.aispin{display:inline-block;width:14px;height:14px;border:2px solid currentColor;border-right-color:transparent;border-radius:50%;animation:aisp .8s linear infinite;vertical-align:-2px}@keyframes aisp{to{transform:rotate(360deg)}}`;
  const STAR='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l1.9 5.6L19.5 9.5l-5.6 1.9L12 17l-1.9-5.6L4.5 9.5l5.6-1.9zM19 14l.9 2.6 2.6.9-2.6.9L19 21l-.9-2.6-2.6-.9 2.6-.9z"/></svg>';

  function mount(){
    const box=document.getElementById("pnBox");if(!box||document.getElementById("aiBtn"))return;
    const st=document.createElement("style");st.textContent=css;document.head.appendChild(st);
    const b=document.createElement("button");b.type="button";b.id="aiBtn";b.className="aib";b.innerHTML=STAR+"Asistente";
    const panel=document.createElement("div");panel.id="aiBox";panel.className="aibox";panel.hidden=true;
    box.insertAdjacentElement("afterend",b);b.insertAdjacentElement("afterend",panel);
    box.style.display="inline-block";box.addEventListener("toggle",()=>{box.style.display=box.open?"block":"inline-block"});
    b.onclick=()=>{panel.hidden=!panel.hidden;if(!panel.hidden){draw();const t=panel.querySelector("textarea,input");if(t)t.focus()}};
    panel.addEventListener("click",onClick);panel.addEventListener("change",onChange);
  }
  function draw(msg){
    const p=document.getElementById("aiBox");if(!p)return;
    if(!get(KEY)){
      p.innerHTML=`<h4>${STAR}Asistente de pendientes</h4><p>Mándale una foto o PDF del calendario de una materia, o escríbele lo que tienes que hacer, y te propone los pendientes y exámenes con su fecha. Usa Gemini de Google con una clave gratis (se hace una vez):</p>
<ol><li>Abre <a href="https://aistudio.google.com/apikey" target="_blank" rel="noopener">Google AI Studio</a> y entra con tu cuenta de Google.</li><li>Presiona <b>Create API key</b> (si te pide proyecto, elige el que te ofrece) y copia la clave completa (empieza con <b>AIza</b> o <b>AQ.</b>).</li><li>Pégala aquí. Se guarda solo en este aparato; en tu otro aparato la pegas otra vez.</li></ol>
<p class="mut">Es gratis con un límite diario de sobra para esto. No pongas tarjeta ni actives facturación.</p>
<input type="password" id="aiKey" placeholder="Pega tu clave aquí" autocomplete="off"><p class="err" id="aiErr" hidden></p><div class="row"><button type="button" data-ai="key">Guardar clave</button></div>`;
      return;
    }
    if(props){
      const all=[...props.exams.map((x,i)=>({k:"e"+i,c:"#00543c",t:"Examen: "+x.name,s:fmt(x.date)+(x.topics&&x.topics.length?" · "+x.topics.length+" temas":"")})),
        ...props.tasks.map((x,i)=>{const T=Cal.types[x.type]||Cal.types.otro,F=Cal.flags[x.flag];return {k:"t"+i,c:T.c,t:x.title,s:[T.l,x.mat,x.due?"entrega "+fmt(x.due):"sin fecha",F?F.l:"",x.notes].filter(Boolean).join(" · ")}})];
      p.innerHTML=`<h4>${STAR}Esto encontré</h4>${props.msg?`<p>${esc(props.msg)}</p>`:""}`+(all.length?all.map(a=>`<label class="aiitem" style="--c:${a.c}"><input type="checkbox" data-pick="${a.k}" checked><span><b>${esc(a.t)}</b><small>${esc(a.s)}</small></span></label>`).join("")+
        `<div class="row"><button type="button" data-ai="add">Agregar seleccionados</button><button type="button" class="sec" data-ai="back">Corregir</button><button type="button" class="sec" data-ai="close">Cancelar</button></div>`:
        `<p class="mut">No encontré nada para agregar.</p><div class="row"><button type="button" class="sec" data-ai="back">Volver</button></div>`);
      return;
    }
    p.innerHTML=`<h4>${STAR}Asistente de pendientes</h4><p class="mut">Ej. "El viernes entrego el caso clínico de cirugía, es urgente" o adjunta la foto del calendario de la materia.</p>
<textarea id="aiTxt" placeholder="¿Qué quieres agregar?">${esc(window.__aiDraft||"")}</textarea>
<div class="row" id="aiFiles">${files.map((f,i)=>`<span class="chip">${esc(f.name)}<b data-rm="${i}" title="Quitar">×</b></span>`).join("")}</div>
${msg?`<p class="err">${esc(msg)}</p>`:""}
<div class="row"><button type="button" data-ai="go"${busy?" disabled":""}>${busy?'<span class="aispin"></span> Leyendo…':"Analizar"}</button><label class="sec" style="cursor:pointer;border:1.5px solid var(--line);border-radius:999px;padding:7px 14px;font:700 .85rem var(--f-display)">📎 Foto o PDF<input type="file" id="aiFile" accept="image/*,application/pdf" multiple hidden></label>
<span style="flex:1"></span><a href="#" data-ai="forget" class="mut" style="font-size:.78rem;font-weight:500;color:var(--muted)">Quitar clave</a></div>`;
  }
  const fmt=s=>{const [y,m,d]=s.split("-").map(Number),x=new Date(y,m-1,d);return DIAS[x.getDay()].slice(0,3)+" "+d+"/"+m};
  async function onChange(ev){
    if(ev.target.id==="aiFile"){
      for(const f of ev.target.files){if(f.size>15e6){draw("El archivo "+f.name+" pesa más de 15 MB.");return}
        const data=await new Promise((r,j)=>{const fr=new FileReader();fr.onload=()=>r(String(fr.result).split(",")[1]);fr.onerror=j;fr.readAsDataURL(f)});
        files.push({name:f.name,type:f.type||"application/pdf",data})}
      saveDraft();draw();
    }
  }
  const saveDraft=()=>{const t=document.getElementById("aiTxt");if(t)window.__aiDraft=t.value};
  async function onClick(ev){
    const rm=ev.target.closest("[data-rm]");if(rm){saveDraft();files.splice(+rm.dataset.rm,1);draw();return}
    const a=ev.target.closest("[data-ai]");if(!a)return;const k=a.dataset.ai;
    if(k==="key"){const v=document.getElementById("aiKey").value.trim(),e=document.getElementById("aiErr");
      if(!/^(AIza[A-Za-z0-9_\-]{30,}|AQ\.[A-Za-z0-9_.\-]{30,}|[A-Za-z0-9_.\-]{35,})$/.test(v)){e.hidden=false;e.textContent="Esa no parece una clave de Google AI Studio. Cópiala completa, sin espacios.";return}
      set(KEY,v);draw();return}
    if(k==="forget"){ev.preventDefault();del(KEY);draw();return}
    if(k==="close"){props=null;files=[];window.__aiDraft="";document.getElementById("aiBox").hidden=true;return}
    if(k==="back"){props=null;draw();return}
    if(k==="add"){
      const pick=new Set([...document.querySelectorAll("#aiBox [data-pick]:checked")].map(x=>x.dataset.pick));
      const n=Cal.addFromAI({tasks:props.tasks.filter((x,i)=>pick.has("t"+i)),exams:props.exams.filter((x,i)=>pick.has("e"+i))});
      props=null;files=[];window.__aiDraft="";
      const p=document.getElementById("aiBox");p.innerHTML=`<h4>${STAR}Listo</h4><p>Agregué ${n} ${n===1?"cosa":"cosas"} a tu calendario.</p><div class="row"><button type="button" class="sec" data-ai="back">Agregar más</button><button type="button" class="sec" data-ai="close">Cerrar</button></div>`;
      return}
    if(k==="go"){
      saveDraft();const txt=(window.__aiDraft||"").trim();
      if(!txt&&!files.length){draw("Escribe algo o adjunta una foto o PDF.");return}
      busy=true;draw();
      try{props=await ask(txt);busy=false;draw()}
      catch(e){busy=false;draw(e.message||"No se pudo.")}
    }
  }
  function context(){
    const now=new Date(),t=ymd(now);
    const mats=(typeof CURSO!=="undefined"?CURSO.materias:[]).map(m=>"- "+m.n+(m.g?" (guía: "+m.g+")":"")).join("\n");
    return `Eres el asistente del calendario de estudio de Marcos, estudiante de Medicina en la UDLAP (${typeof CURSO!=="undefined"?CURSO.sem:5}º semestre).
Hoy es ${DIAS[now.getDay()]} ${t}. Zona horaria de Puebla, México.
Tu trabajo: leer lo que Marcos escribe o adjunta (fotos o PDF de calendarios de materias, programas, avisos) y proponer qué agregar.
- "examenes": exámenes, parciales, finales, quizzes con fecha. name = "Materia · qué examen" (ej. "Cirugía · 2º parcial"). Si hay temas, ponlos en topics (uno por elemento). guide = id de guía de la materia si existe.
- "pendientes": todo lo demás que hay que hacer o entregar (tareas, proyectos, presentaciones, lecturas, prácticas o guardias, trámites).
  type: tarea | proyecto | presentacion | lectura | practica | tramite | otro.
  flag (opcional): urgente (vence pronto o lo pide así) | necesario | delegar | eliminar. Si no queda claro, déjalo vacío.
  due: fecha de entrega YYYY-MM-DD o vacío si no tiene.
- mat: usa exactamente uno de estos nombres de materia si corresponde; si no, vacío:
${mats}
- Convierte fechas relativas ("el viernes", "en dos semanas") a fechas reales contando desde hoy. Si una fecha no trae año, usa la próxima que venga.
- No inventes cosas que no estén en el texto o los archivos. No incluyas lo que ya pasó.
- "mensaje": una o dos frases en español para Marcos (qué encontraste, dudas o algo que no se leyó bien).
Responde solo con el JSON pedido.`;
  }
  const S=(type,extra)=>Object.assign({type},extra||{});
  const SCHEMA=S("OBJECT",{properties:{
    mensaje:S("STRING"),
    examenes:S("ARRAY",{items:S("OBJECT",{properties:{name:S("STRING"),date:S("STRING",{description:"YYYY-MM-DD"}),topics:S("ARRAY",{items:S("STRING")}),guide:S("STRING")},required:["name","date"]})}),
    pendientes:S("ARRAY",{items:S("OBJECT",{properties:{title:S("STRING"),type:S("STRING",{enum:["tarea","proyecto","presentacion","lectura","practica","tramite","otro"]}),mat:S("STRING"),due:S("STRING",{description:"YYYY-MM-DD o vacío"}),flag:S("STRING",{enum:["","urgente","necesario","delegar","eliminar"]}),notes:S("STRING")},required:["title","type"]})})},
    required:["mensaje","examenes","pendientes"]});
  async function ask(txt){
    const key=get(KEY);if(!key)throw new Error("Falta la clave.");
    const parts=files.map(f=>({inline_data:{mime_type:f.type,data:f.data}}));
    parts.push({text:txt||"Revisa los archivos y propón qué agregar."});
    const body=JSON.stringify({system_instruction:{parts:[{text:context()}]},contents:[{role:"user",parts}],generationConfig:{responseMimeType:"application/json",responseSchema:SCHEMA,temperature:0.2}});
    let r,last="";
    for(const m of MODELS){
      try{r=await fetch(API+m+":generateContent",{method:"POST",headers:{"content-type":"application/json","x-goog-api-key":key},body})}
      catch(e){throw new Error("Sin conexión: el asistente necesita internet.")}
      if(r.status===404){last="modelo";continue}
      break;
    }
    const j=await r.json().catch(()=>({})),m=(j.error&&j.error.message)||"";
    if(r.status===400&&/API key/i.test(m)||r.status===403)throw new Error("La clave no sirve. Revisa que la copiaste completa (o quítala y pégala otra vez).");
    if(r.status===429)throw new Error("Llegaste al límite gratis de Gemini por ahora; intenta en un rato.");
    if(!r.ok)throw new Error("Gemini respondió con error "+r.status+(m?": "+m.slice(0,140):"")+".");
    const c=j.candidates&&j.candidates[0],t=c&&c.content&&c.content.parts?c.content.parts.map(x=>x.text||"").join(""):"";
    if(!t)throw new Error(c&&c.finishReason==="SAFETY"?"Gemini no quiso leer eso; intenta con otra foto o escríbelo.":"No entendí la respuesta; intenta otra vez.");
    let x;try{x=JSON.parse(t.replace(/^```(json)?|```$/g,"").trim())}catch(e){throw new Error("No entendí la respuesta; intenta otra vez.")}
    return {msg:String(x.mensaje||""),exams:Array.isArray(x.examenes)?x.examenes:[],tasks:Array.isArray(x.pendientes)?x.pendientes:[]};
  }
  if(document.readyState==="loading")addEventListener("DOMContentLoaded",mount);else mount();
})();
