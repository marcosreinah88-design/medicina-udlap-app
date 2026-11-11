/* cielo de Puebla: la portada sigue la hora real (amanecer, día, atardecer y noche con la luna del día) */
(()=>{
  const hero=document.querySelector(".hero"),sun=$("#sun"),lbl=$("#skyLbl"),svg=sun.ownerSVGElement,luna=$("#luna"),stars=$("#skyStars");
  if(!hero||!sun)return;
  const LAT=19.0414,LNG=-98.2063,rad=Math.PI/180,e=rad*23.4397,J1970=2440588,J2000=2451545,H=36e5;
  const {sin,cos,tan,asin,acos,atan2,PI}=Math;
  /* horas de salida y puesta del sol (fórmulas astronómicas, sin internet) */
  function times(date){
    const lw=rad*-LNG,phi=rad*LAT,J=date.valueOf()/864e5-0.5+J1970-J2000;
    const n=Math.round(J-0.0009-lw/(2*PI)),ds=0.0009+lw/(2*PI)+n;
    const M=rad*(357.5291+0.98560028*ds),C=rad*(1.9148*sin(M)+0.02*sin(2*M)+0.0003*sin(3*M));
    const L=M+C+rad*102.9372+PI,dec=asin(sin(e)*sin(L));
    const Jt=J2000+ds+0.0053*sin(M)-0.0069*sin(2*L);
    const w=acos((sin(rad*-0.833)-sin(phi)*sin(dec))/(cos(phi)*cos(dec)));
    const Js=J2000+0.0009+(w+lw)/(2*PI)+n+0.0053*sin(M)-0.0069*sin(2*L),Jr=Jt-(Js-Jt);
    const d=j=>new Date((j+0.5-J1970)*864e5);
    return {rise:d(Jr),set:d(Js)};
  }
  /* fase de la luna: 0 nueva, .25 cuarto creciente, .5 llena, .75 cuarto menguante */
  function moon(date){
    const d=date.valueOf()/864e5-0.5+J1970-J2000;
    const M=rad*(357.5291+0.98560028*d),C=rad*(1.9148*sin(M)+0.02*sin(2*M)+0.0003*sin(3*M)),L=M+C+rad*102.9372+PI;
    const sDec=asin(sin(e)*sin(L)),sRA=atan2(sin(L)*cos(e),cos(L));
    const Lm=rad*(218.316+13.176396*d),Mm=rad*(134.963+13.064993*d),F=rad*(93.272+13.22935*d);
    const l=Lm+rad*6.289*sin(Mm),b=rad*5.128*sin(F),dist=385001-20905*cos(Mm);
    const mRA=atan2(sin(l)*cos(e)-tan(b)*sin(e),cos(l)),mDec=asin(sin(b)*cos(e)+cos(b)*sin(e)*sin(l));
    const sd=149598000,ph=acos(sin(sDec)*sin(mDec)+cos(sDec)*cos(mDec)*cos(sRA-mRA));
    const inc=atan2(sd*sin(ph),dist-sd*cos(ph));
    const ang=atan2(cos(sDec)*sin(sRA-mRA),sin(sDec)*cos(mDec)-cos(sDec)*sin(mDec)*cos(sRA-mRA));
    return {f:(1+cos(inc))/2,p:0.5+0.5*inc*(ang<0?-1:1)/PI};
  }
  const moonName=p=>p<.03||p>.97?"Luna nueva":p<.22?"Luna creciente":p<.28?"Cuarto creciente":p<.47?"Gibosa creciente":p<.53?"Luna llena":p<.72?"Gibosa menguante":p<.78?"Cuarto menguante":"Luna menguante";
  function drawMoon(p){
    if(!luna)return;
    const r=40,k=cos(2*PI*p),rx=Math.abs(k)*r,wax=p<.5;
    const outer=wax?1:0,term=wax?(k>0?0:1):(k>0?1:0);
    const lit=`M0 ${-r}A${r} ${r} 0 0 ${outer} 0 ${r}A${rx.toFixed(2)} ${r} 0 0 ${term} 0 ${-r}Z`;
    luna.querySelector(".lit").setAttribute("d",lit);
    luna.querySelector("#lunaClip path").setAttribute("d",lit);
  }
  /* estrellas fijas (siempre en el mismo lugar) */
  if(stars&&!stars.childElementCount){
    let s=7;const rnd=()=>(s=(s*16807)%2147483647)/2147483647,NS="http://www.w3.org/2000/svg";
    for(let i=0;i<90;i++){const c=document.createElementNS(NS,"circle");const big=rnd()<.12;
      c.setAttribute("cx",(rnd()*100).toFixed(2)+"%");c.setAttribute("cy",(Math.pow(rnd(),1.4)*78).toFixed(2)+"%");c.setAttribute("r",big?1.6:(0.5+rnd()*0.7).toFixed(2));
      if(rnd()<.45){c.classList.add("tw");c.style.animationDelay=(-rnd()*6).toFixed(2)+"s";c.style.animationDuration=(3+rnd()*4).toFixed(2)+"s"}
      stars.appendChild(c)}
  }
  const hm=d=>d.toLocaleTimeString("es-MX",{hour:"numeric",minute:"2-digit",hour12:false,timeZone:"America/Mexico_City"});
  const ramp=(x,a,b)=>x<=a?0:x>=b?1:(x-a)/(b-a);
  /* cuánto pesa cada escena ahora (0 a 1): amanecer ~1 h antes hasta 3 h después de que sale el sol,
     atardecer desde 3 h antes hasta 1 h después de que se pone, noche el resto */
  function weights(now,t){
    const r=+t.rise,s=+t.set;
    const dawn=ramp(now,r-1.25*H,r-0.75*H)*(1-ramp(now,r+2.5*H,r+3*H));
    const dusk=ramp(now,s-3*H,s-2.5*H)*(1-ramp(now,s+0.6*H,s+1.1*H));
    const night=Math.max(1-ramp(now,r-1*H,r-0.4*H),ramp(now,s+0.5*H,s+1*H));
    return {dawn,dusk,night};
  }
  const SCENES={dawn:{dawn:1,dusk:0,night:0},dusk:{dawn:0,dusk:1,night:0},night:{dawn:0,dusk:0,night:1},day:{dawn:0,dusk:0,night:0}};
  let manual=null;
  function place(now,t,w){
    /* el sol: al amanecer sube por el oriente (izquierda); al atardecer baja detrás del cráter del Popo */
    const r=svg.getBoundingClientRect(),k=(r.height/180||1)/(r.width/1200||1);
    let cx,cy;
    if(w.dusk>=w.dawn){cx=690;cy=34-((+t.set-now)/H)*22}else{cx=150;cy=176-((now-t.rise)/H)*60}
    sun.querySelectorAll("ellipse").forEach(el=>{const base=el.classList.contains("disk")?17:90;el.setAttribute("cx",cx);el.setAttribute("cy",cy.toFixed(1));el.setAttribute("ry",base);el.setAttribute("rx",(base*k).toFixed(2))});
  }
  function tick(){
    const real=window.__skyNow?+window.__skyNow:Date.now();
    const noon=new Date(real);noon.setHours(12,0,0,0);const t=times(noon);
    const forced=window.__sky||manual;
    let now=real,w;
    if(forced&&SCENES[forced]){w=SCENES[forced];now=forced==="dawn"?+t.rise+0.9*H:forced==="dusk"?+t.set-0.7*H:real}
    else w=weights(real,t);
    const top=w.night>=.5?"night":w.dawn>=.5?"dawn":w.dusk>=.5?"dusk":"day";
    hero.classList.toggle("dawn",top==="dawn");hero.classList.toggle("dusk",top==="dusk");hero.classList.toggle("night",top==="night");
    hero.style.setProperty("--wd",w.dawn.toFixed(3));hero.style.setProperty("--wk",w.dusk.toFixed(3));hero.style.setProperty("--wn",w.night.toFixed(3));
    hero.style.setProperty("--ws",Math.max(w.dawn,w.dusk).toFixed(3));
    if(w.dawn||w.dusk)place(now,t,w);
    const m=moon(new Date(real));drawMoon(m.p);
    const icon=top==="night"?"☾":"☀",name={dawn:"Amanecer",dusk:"Atardecer",night:moonName(m.p),day:"Día"}[top];
    const extra=top==="night"?`<span class="lg">&nbsp;· ${Math.round(m.f*100)}% iluminada</span>`:"";
    const rise=+t.rise<=real?"amaneció":"amanece",set=+t.set<=real?"atardeció":"atardece";
    lbl.innerHTML=`<b>${icon} ${name}</b>${extra}<span class="lg">&nbsp;· Puebla hoy ${rise} ${hm(t.rise)} y ${set} ${hm(t.set)}</span><span class="sm">&nbsp;· ↑${hm(t.rise)} ↓${hm(t.set)}</span>${manual?'<em>manual</em>':""}`;
    lbl.title=manual?"Escena elegida a mano: toca para cambiar (vuelve sola al recargar)":"Cambia sola con la hora; toca para elegir otra escena";
    lbl.hidden=false;
  }
  /* cambio manual: tocar el escudo o la etiqueta pasa por amanecer, atardecer, noche, día y de vuelta a automático */
  const seal=$("#seal"),ORDER=[null,"dawn","dusk","night","day"];
  function cycle(){manual=ORDER[(ORDER.indexOf(manual)+1)%ORDER.length];tick();
    if(seal){seal.classList.remove("spin");void seal.offsetWidth;seal.classList.add("spin");setTimeout(()=>seal.classList.remove("spin"),600)}}
  if(seal){seal.addEventListener("click",cycle);seal.addEventListener("keydown",ev=>{if(ev.key==="Enter"||ev.key===" "){ev.preventDefault();cycle()}})}
  lbl.addEventListener("click",cycle);
  tick();setInterval(tick,60000);
  addEventListener("resize",()=>{if(hero.classList.contains("dusk")||hero.classList.contains("dawn"))tick()});
  document.addEventListener("visibilitychange",()=>{if(!document.hidden)tick()});
  window.__skyTimes=times;window.__skyMoon=moon;window.__skyTick=tick;
})();
