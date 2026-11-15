/* buscador: materias, temas y palabras clave de todas las guías */
/*busqueda-avanzada-v1*/
(()=>{
  const q=$("#q"),out=$("#results"),hint=$("#shint"),clr=$("#qc"),kbd=$("#qk");
  const advT=$("#advT"),advP=$("#advP"),advN=$("#advN"),advS=$("#advS"),advClr=$("#advClr");
  const semName=n=>(SEMS.find(s=>s.n===n)||{}).name||"";
  const matKey=g=>fold(g.area).replace(/\s+general$/,"");
  const IDX=G.map(g=>({g,mk:matKey(g),title:fold(g.title),area:fold(g.area),toc:(g.toc||[]).map(fold),rest:fold([g.sub,g.desc,g.kw,(g.feat||[]).join(" ")].join(" ")),sem:fold(semName(g.sem)+" "+ord(g.sem)),ft:" "+((typeof FT!=="undefined"&&FT[g.id])||"")+" "}));
  /* materias (una por área; Cirugía y Cirugía general van juntas) */
  const MATS=[];for(const x of IDX){let m=MATS.find(v=>v.k===x.mk);if(!m)MATS.push(m={k:x.mk,label:x.g.area,sem:x.g.sem});if(x.g.area.length<m.label.length)m.label=x.g.area;m.sem=Math.min(m.sem,x.g.sem)}
  MATS.sort((a,b)=>a.sem-b.sem||a.label.localeCompare(b.label,"es"));
  const SEMS_G=[...new Set(G.map(g=>g.sem))].sort((a,b)=>a-b);
  /* apartados: se cargan de buscador-apartados.json la primera vez que se usan */
  let AP=null,apLoading=null,CATS=[];
  const loadAP=()=>apLoading||(apLoading=fetch("buscador-apartados.json",{cache:"force-cache"}).then(r=>{if(!r.ok)throw 0;return r.json()}).then(d=>{
      CATS=d.cats||[];AP={};
      for(const x of IDX){const o=(d.g||{})[x.g.id]||{},m={};
        for(const [c,places] of Object.entries(o)){if(c==="$")continue;m[c]={all:" "+places.map(p=>p[1]).join(" ")+" ",places:places.map(p=>({w:p[0],s:" "+p[1]+" "}))}}
        for(const c of o.$||[]){const cur=m[c]||(m[c]={all:" ",places:[]});cur.whole=true;cur.all+=x.ft}
        AP[x.g.id]=m}
      paintChips();run()}).catch(()=>{apLoading=null;advS.textContent="No pude cargar los apartados. Revisa tu conexión e inténtalo otra vez."}));
  /* filtros elegidos (se recuerdan en este aparato) */
  const sel={sem:new Set(),mat:new Set(),ap:new Set()};
  try{const s=JSON.parse(store.get("busqueda-filtros")||"{}");for(const k in sel)(s[k]||[]).forEach(v=>sel[k].add(k==="sem"?+v:v))}catch(e){}
  const save=()=>store.set("busqueda-filtros",JSON.stringify({sem:[...sel.sem],mat:[...sel.mat],ap:[...sel.ap]}));
  const nSel=()=>sel.sem.size+sel.mat.size+sel.ap.size;
  function mark(text,terms){
    const f=fold(text);const hit=new Array(text.length).fill(false);
    for(const t of terms){let i=f.indexOf(t);while(i>-1){for(let k=i;k<i+t.length;k++)hit[k]=true;i=f.indexOf(t,i+t.length)}}
    let o="",on=false;Array.from(text).forEach((c,i)=>{if(hit[i]&&!on){o+="<mark>";on=true}if(!hit[i]&&on){o+="</mark>";on=false}o+=esc(c)});
    return o+(on?"</mark>":"");
  }
  const catLabel=c=>(CATS.find(v=>v[0]===c)||[c,c])[1];
  /* ¿la guía coincide con las palabras? (sin apartados: como siempre) */
  function scoreOf(x,terms){
    let score=0;
    for(const t of terms){
      let s=0;
      if(x.title.includes(t))s+=10;if(x.area.includes(t))s+=8;
      const tc=x.toc.filter(v=>v.includes(t)).length;if(tc)s+=4+tc;
      if(x.rest.includes(t))s+=2;if(x.sem.includes(t))s+=1;if(x.ft.includes(" "+t))s+=3;
      if(!s)return 0;score+=s;
    }
    return score;
  }
  /* con apartados: cada palabra tiene que estar dentro de alguno de los apartados elegidos */
  function apHits(x,terms,cats){
    const m=AP&&AP[x.g.id];if(!m)return null;
    const cs=[...cats].filter(c=>m[c]);if(!cs.length)return null;
    if(!terms.length)return {score:1,places:[],cats:cs};
    let score=0;
    for(const t of terms){let s=0;for(const c of cs)if(m[c].all.includes(" "+t))s+=3;if(!s)return null;score+=s}
    const places=[],seen=new Set(),hitCats=new Set();
    for(const c of cs){
      for(const p of m[c].places){const n=terms.filter(t=>p.s.includes(" "+t)).length;if(!n)continue;hitCats.add(c);const k=c+"|"+p.w;if(!seen.has(k)){seen.add(k);places.push({c,w:p.w,n})}}
      if(m[c].whole&&terms.every(t=>x.ft.includes(" "+t)||x.title.includes(t)))hitCats.add(c);
    }
    places.sort((a,b)=>b.n-a.n);
    return {score:score+places.length,places,cats:[...hitCats]};
  }
  /* todas las coincidencias para unas palabras y unos filtros (sirve también para contar cada filtro) */
  function search(terms,f){
    const res=[];
    for(const x of IDX){
      if(f.sem.size&&!f.sem.has(x.g.sem))continue;
      if(f.mat.size&&!f.mat.has(x.mk))continue;
      if(f.ap.size){
        if(!AP)continue;
        const h=apHits(x,terms,f.ap);if(!h)continue;
        res.push({x,score:h.score,ap:h,tocHits:[],words:[]});continue;
      }
      if(!terms.length){res.push({x,score:1,tocHits:[],words:[]});continue}
      const score=scoreOf(x,terms);if(!score)continue;
      const tocHits=(x.g.toc||[]).filter((v,i)=>terms.some(t=>x.toc[i].includes(t)));
      const words=tocHits.length?[]:[...new Set(terms.flatMap(t=>{const r=[];let i=x.ft.indexOf(" "+t);while(i>-1&&r.length<4){r.push(x.ft.slice(i+1,x.ft.indexOf(" ",i+1)));i=x.ft.indexOf(" "+t,i+1)}return r}))].slice(0,5);
      res.push({x,score,tocHits,words});
    }
    return res.sort((a,b)=>b.score-a.score||a.x.g.sem-b.x.g.sem);
  }
  /* chips de los filtros con cuántos resultados daría cada uno */
  function paintChips(){
    const chips=(k,list)=>list.map(([v,label])=>`<button type="button" class="chip" data-f="${k}" data-v="${esc(v)}" aria-pressed="${sel[k].has(v)}">${esc(label)}<span class="cn"></span></button>`).join("");
    advP.querySelector('[data-f="sem"]').innerHTML=chips("sem",SEMS_G.map(n=>[n,ord(n)+" semestre"]));
    advP.querySelector('[data-f="mat"]').innerHTML=chips("mat",MATS.map(m=>[m.k,m.label]));
    advP.querySelector('[data-f="ap"]').innerHTML=AP?chips("ap",CATS):`<span class="adv-load">Cargando apartados…</span>`;
  }
  function counts(terms){
    for(const b of advP.querySelectorAll(".chip")){
      const k=b.dataset.f,v=k==="sem"?+b.dataset.v:b.dataset.v;
      const f={sem:sel.sem,mat:sel.mat,ap:sel.ap,[k]:new Set([v])};
      const n=search(terms,f).length;
      b.querySelector(".cn").textContent=n;b.classList.toggle("zero",!n&&!sel[k].has(v));
      b.setAttribute("aria-pressed",sel[k].has(v));
      b.setAttribute("aria-label",`${b.firstChild.textContent}: ${n} ${n===1?"guía":"guías"}`);
    }
  }
  function summary(){
    const n=nSel();advN.hidden=!n;advN.textContent=n;advClr.hidden=!n;
    const parts=[];
    if(sel.sem.size)parts.push([...sel.sem].sort().map(v=>ord(v)).join(", ")+" semestre");
    if(sel.mat.size)parts.push(MATS.filter(m=>sel.mat.has(m.k)).map(m=>m.label).join(", "));
    if(sel.ap.size)parts.push("solo en "+[...sel.ap].map(catLabel).join(", ").toLowerCase());
    advS.textContent=n?"Buscando en: "+parts.join(" · "):"Sin filtros: busca en toda la carrera.";
    return parts;
  }
  function run(){
    const raw=q.value.trim(),terms=fold(raw).split(/\s+/).filter(Boolean),n=nSel();
    clr.hidden=!raw;kbd.hidden=!!raw;hint.hidden=!!raw||!!n;
    if(sel.ap.size&&!AP)loadAP();
    const parts=summary();
    if(!advP.hidden)counts(terms);
    if(!terms.length&&!n){out.hidden=true;out.innerHTML="";return}
    out.hidden=false;
    if(sel.ap.size&&!AP){out.innerHTML=`<p class="rcount">Cargando apartados…</p>`;return}
    const res=search(terms,sel);
    const fl=n?`<span class="rfl">${esc(parts.join(" · "))}</span>`:"";
    if(!res.length){out.innerHTML=terms.length?`<p class="rnone">No encontré nada con <b>“${esc(raw)}”</b>${n?" con estos filtros":""}. ${n?`<button type="button" class="rclr" data-clr>Quitar filtros</button>`:"Prueba con otra palabra o el nombre de la materia."}</p>`:`<p class="rnone">Ninguna guía tiene esos filtros juntos. <button type="button" class="rclr" data-clr>Quitar filtros</button></p>`;return}
    const topics=res.reduce((a,r)=>a+(r.ap?r.ap.places.length:r.tocHits.length),0);
    const what=sel.ap.size?(topics===1?"apartado que coincide":"apartados que coinciden"):(topics===1?"tema que coincide":"temas que coinciden");
    out.innerHTML=`<p class="rcount">${res.length} ${res.length>1?"guías":"guía"}${terms.length&&topics?` · ${topics} ${what}`:""}${!terms.length?" · escribe una palabra para buscar adentro":""}${fl}</p><div class="rlist">`+res.slice(0,60).map(({x,tocHits,words,ap})=>{
      const g=x.g;let body;
      if(ap){
        const pl=ap.places.slice(0,4),more=ap.places.length-pl.length;
        body=pl.length?`<span class="rt rap">${pl.map(p=>{const w=p.w.split(" › ").pop();return `<span role="link" tabindex="0" data-goto="${esc(w)}"><i>${esc(catLabel(p.c))}</i>${mark(p.w.length>70?p.w.slice(0,68)+"…":p.w,terms)}</span>`}).join("")}${more>0?`<em>y ${more} más</em>`:""}</span>`
          :`<span class="rd">${terms.length?"En: ":"Tiene: "}${esc(ap.cats.map(catLabel).join(", "))}${terms.length&&ap.cats.some(c=>AP[g.id][c].whole)?" (toda la guía)":""}</span>`;
      }else{
        const shown=tocHits.slice(0,4),more=tocHits.length-shown.length;
        body=shown.length?`<span class="rt">${shown.map(v=>`<span>${mark(v,terms)}</span>`).join("")}${more>0?`<em>y ${more} más</em>`:""}</span>`:words.length?`<span class="rd">En el contenido:</span><span class="rt">${words.map(v=>`<span>${mark(v,terms)}</span>`).join("")}</span>`:`<span class="rd">${mark(g.desc||g.sub||"",terms)}</span>`;
      }
      return `<button class="rcard" type="button" data-guide="${esc(g.id)}" style="--c:${g.color}">
        <span class="rs">${esc(ord(g.sem))} semestre · ${mark(g.area,terms)}</span>
        <b>${mark(g.title,terms)}</b>
        ${body}
        <span class="rgo">${terms.length?"Ir al apartado":"Abrir guía"} ${ARROW}</span></button>`}).join("")+`</div>`;
  }
  /* abrir y cerrar el panel */
  const openP=on=>{advP.hidden=!on;advT.setAttribute("aria-expanded",on);if(on){if(!AP)loadAP();if(!advP.querySelector(".chip"))paintChips();run()}};
  advT.addEventListener("click",()=>openP(advP.hidden));
  advP.addEventListener("click",e=>{
    const b=e.target.closest(".chip");if(!b)return;
    const k=b.dataset.f,v=k==="sem"?+b.dataset.v:b.dataset.v;
    sel[k].has(v)?sel[k].delete(v):sel[k].add(v);save();run();
  });
  const clearF=()=>{for(const k in sel)sel[k].clear();save();run()};
  advClr.addEventListener("click",clearF);
  paintChips();summary();
  q.addEventListener("input",run);
  clr.addEventListener("click",()=>{q.value="";run();q.focus()});
  hint.addEventListener("click",e=>{const b=e.target.closest("button");if(b){q.value=b.textContent;run();q.focus()}});
  q.addEventListener("keydown",e=>{
    if(e.key==="Escape"){e.stopPropagation();if(q.value){q.value="";run()}else q.blur()}
    if(e.key==="Enter"){const f=out.querySelector(".rcard");if(f)f.click()}
  });
  const goGuide=(id,t)=>go("guia-"+encodeURIComponent(id)+(t?"~"+encodeURIComponent(t):""));
  out.addEventListener("click",e=>{
    if(e.target.closest("[data-clr]")){clearF();return}
    const c=e.target.closest("[data-guide]");if(!c)return;
    const p=e.target.closest("[data-goto]");
    goGuide(c.dataset.guide,p?p.dataset.goto:q.value.trim()); /* el apartado lleva a su subtema; la tarjeta, a la palabra */
  });
  out.addEventListener("keydown",e=>{const p=e.target.closest("[data-goto]");if(p&&(e.key==="Enter"||e.key===" ")){e.preventDefault();e.stopPropagation();p.click()}});
  document.addEventListener("keydown",e=>{
    if(e.key==="/"&&current===null&&document.activeElement!==q&&!/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)){e.preventDefault();q.focus();q.scrollIntoView({block:"center",behavior:"smooth"})}
  });
  if(nSel()){if(sel.ap.size)loadAP();run()}
})();
