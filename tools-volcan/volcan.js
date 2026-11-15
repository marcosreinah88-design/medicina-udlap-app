/* el Popo despierta de vez en cuando: explosiones de ceniza con columna, rayos y caída de ceniza, o erupciones de lava con brasas y coladas (canvas que solo trabaja mientras dura la erupción) */
(()=>{
  const hero=document.querySelector(".hero"),box=$("#volc"),cv=$("#volcCv"),glowSky=$("#volcSky"),fum=$("#volcFum");
  if(!hero||!box||!cv||!cv.getContext)return;
  const RM=matchMedia("(prefers-reduced-motion: reduce)");
  const ctx=cv.getContext("2d");
  const R=(a,b)=>a+Math.random()*(b-a),clamp=(x,a,b)=>x<a?a:x>b?b:x,ease=t=>1-Math.pow(1-clamp(t,0,1),3);
  const smooth=t=>{t=clamp(t,0,1);return t*t*(3-2*t)};
  /* viento del día: como en la vida real, empuja la ceniza del Popo hacia el Iztaccíhuatl (a la derecha en el dibujo) */
  const WIND=R(.75,1.05);
  if(fum)fum.style.setProperty("--wx",WIND.toFixed(2));
  /* perfil del Popo en coordenadas del dibujo (1200 x 180) */
  const RIDGE=[[0,180],[470,180],[640,34],[656,30],[684,30],[700,34],[800,120],[870,120],[890,112],[912,96],[930,100],[1200,100]];
  const FLOWS=[[[664,31],[656,42],[650,56],[642,70],[635,87],[624,105],[616,124]],[[678,31],[687,44],[692,58],[700,73],[708,91],[719,110]]];
  let W=0,H=0,top0=0,hz=1,S=1,ox=0,oy=0,dpr=1;
  function geo(){
    const b=box.getBoundingClientRect(),h=box.parentNode.getBoundingClientRect();
    W=b.width;H=b.height;top0=h.top-b.top;hz=h.height||1;S=clamp(hz/190,.55,1.1);
    dpr=Math.min(devicePixelRatio||1,W<560?1.5:2);
    const cw=Math.round(W*dpr),ch=Math.round(H*dpr);
    if(cv.width!==cw||cv.height!==ch){cv.width=cw;cv.height=ch}
    ox=X(670);oy=Y(29);
  }
  const X=x=>x/1200*W,Y=y=>top0+y/180*hz;
  function ground(px){
    const x=px/W*1200;
    for(let i=1;i<RIDGE.length;i++){const a=RIDGE[i-1],b=RIDGE[i];if(x<=b[0]){const k=(x-a[0])/(b[0]-a[0]||1);return Y(a[1]+(b[1]-a[1])*k)}}
    return Y(180);
  }
  /* camino de una colada: se subdivide, serpentea un poco y se ensancha cuesta abajo; cada punto lleva [x,y,distancia,ancho,nx,ny] */
  function arm(base,seed,wmul){
    const pts=[];
    for(let i=1;i<base.length;i++){const a=base[i-1],b=base[i];for(let k=0;k<4;k++){const u=k/4;pts.push([a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u])}}
    pts.push(base[base.length-1].slice());
    let len=0;const N=pts.length;
    for(let i=0;i<N;i++){const p=pts[i],q=pts[Math.min(N-1,i+1)],r=pts[Math.max(0,i-1)],tx=q[0]-r[0],ty=q[1]-r[1],tl=Math.hypot(tx,ty)||1;
      const nx=-ty/tl,ny=tx/tl,u=i/(N-1),wig=(Math.sin(seed+i*.9)*1.6+Math.sin(seed*2.3+i*2.1)*.8)*S*u;
      p[0]+=nx*wig;p[1]+=ny*wig*.4;
      if(i)len+=Math.hypot(p[0]-pts[i-1][0],p[1]-pts[i-1][1]);
      p.push(len,(3.2+6*Math.pow(u,.8)+Math.sin(seed+i*1.7)*.9)*wmul,nx,ny)}
    return {pts,len};
  }
  const scene=()=>hero.classList.contains("night")?"night":hero.classList.contains("dusk")?"dusk":hero.classList.contains("dawn")?"dawn":"day";
  /* colores de la ceniza según la luz: sombra, lado iluminado y (de noche) reflejo de la lava */
  const PAL={
    day:  {dk:[96,92,88],  lt:[226,222,214],fall:"92,86,80"},
    dawn: {dk:[92,82,100], lt:[255,214,200],fall:"88,76,92"},
    dusk: {dk:[70,56,72],  lt:[255,186,146],fall:"66,50,62"},
    night:{dk:[40,44,56],  lt:[118,126,146],fall:"40,42,52"}
  };
  /* bocanadas pre-dibujadas: varios lóbulos con sombra abajo y luz arriba (se dibujan una vez por escena) */
  let sprites=null,spriteKey="";
  function puffSprite(p,lit,seed){
    const c=document.createElement("canvas"),z=128;c.width=c.height=z;const g=c.getContext("2d");
    let s=seed;const rnd=()=>(s=(s*16807)%2147483647)/2147483647;
    const rgba=(c,a)=>`rgba(${c[0]},${c[1]},${c[2]},${a})`;
    /* coliflor: un cuerpo suave y muchos lóbulos chicos, con luz arriba y sombra abajo */
    const mix=(k)=>[0,1,2].map(i=>Math.round(p.dk[i]+(p.lt[i]-p.dk[i])*k));
    let gr=g.createRadialGradient(64,68,0,64,68,50);gr.addColorStop(0,rgba(p.dk,.95));gr.addColorStop(.65,rgba(p.dk,.7));gr.addColorStop(1,rgba(p.dk,0));g.fillStyle=gr;g.fillRect(0,0,z,z);
    const lobes=[];for(let i=0;i<14;i++){const a=rnd()*6.283,d=Math.sqrt(rnd())*34;lobes.push([64+Math.cos(a)*d*1.1,64+Math.sin(a)*d*.85,13+rnd()*12])}
    lobes.sort((a,b)=>b[1]-a[1]);
    lobes.forEach(([x,y,r])=>{const up=clamp((84-y)/50,0,1)*.75;
      gr=g.createRadialGradient(x-r*.12,y-r*.22,0,x,y,r);gr.addColorStop(0,rgba(mix(.15+.6*up),.75));gr.addColorStop(.55,rgba(mix(.08+.35*up),.5));gr.addColorStop(1,rgba(mix(up*.2),0));
      g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,7);g.fill()});
    if(lit){g.globalCompositeOperation="source-atop";const lg=g.createLinearGradient(0,40,0,128);lg.addColorStop(0,"rgba(255,120,40,0)");lg.addColorStop(1,"rgba(255,110,30,.75)");g.fillStyle=lg;g.fillRect(0,0,z,z)}
    g.globalCompositeOperation="destination-in";const m=g.createRadialGradient(64,64,30,64,64,64);m.addColorStop(0,"#000");m.addColorStop(.8,"rgba(0,0,0,.9)");m.addColorStop(1,"rgba(0,0,0,0)");g.fillStyle=m;g.fillRect(0,0,z,z);
    return c;
  }
  function glowSprite(stops){const c=document.createElement("canvas");c.width=c.height=64;const g=c.getContext("2d"),gr=g.createRadialGradient(32,32,0,32,32,32);stops.forEach(([o,col])=>gr.addColorStop(o,col));g.fillStyle=gr;g.fillRect(0,0,64,64);return c}
  function makeSprites(){
    const sc=scene();if(sprites&&spriteKey===sc)return;spriteKey=sc;const p=PAL[sc];
    sprites={ash:[11,23,37,51].map(s=>puffSprite(p,false,s)),lit:[7,19,43].map(s=>puffSprite(p,true,s)),
      lava:glowSprite([[0,"rgba(255,244,200,1)"],[.18,"rgba(255,170,60,.9)"],[.5,"rgba(255,80,20,.35)"],[1,"rgba(255,60,10,0)"]]),
      dull:glowSprite([[0,"rgba(255,170,110,.8)"],[.4,"rgba(200,90,50,.3)"],[1,"rgba(160,60,40,0)"]])};
  }
  /* partículas */
  let puffs=[],fall=[],bombs=[],sparks=[],flows=[],bolts=[],emit=[],glows=[],raf=0,last=0;
  function addPuff(o){puffs.push(Object.assign({age:0,spr:(Math.random()*4)|0},o))}
  function lavaColor(T,a){/* 1 = blanco-amarillo, .6 naranja, .3 rojo, 0 roca oscura */
    const k=clamp(T,0,1),r=k>.3?255:Math.round(90+165*(k/.3)),g=k>.6?Math.round(150+100*((k-.6)/.4)):Math.round(30+120*(k/.6)),b=k>.8?Math.round(60+140*((k-.8)/.2)):Math.round(10+40*k);
    return `rgba(${r},${g},${b},${a})`;
  }
  function step(now){
    const dt=Math.min(.05,(now-last)/1000||.016);last=now;
    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);
    emit=emit.filter(e=>(e.t+=dt,e.fn(e.t,dt)!==false));
    const top=Math.min(oy*.62,110*S);
    /* resplandor del cráter */
    glows=glows.filter(g=>{g.t+=dt;if(g.t>g.d)return false;
      const k=g.t/g.d,base=g.kind==="lava"?(k<.08?k/.08:1-smooth((k-.55)/.45)):(1-k)*(1-k);
      const fl=g.kind==="lava"?.72+.28*Math.sin(g.t*23)*Math.sin(g.t*7.3+1):1,rr=g.r*(0.85+.25*fl);
      ctx.globalCompositeOperation="lighter";ctx.globalAlpha=clamp(base*fl,0,1);
      ctx.drawImage(g.kind==="lava"?sprites.lava:sprites.dull,ox-rr,oy-rr*.75,rr*2,rr*1.5);
      if(g.kind==="lava"){ctx.globalAlpha=clamp(base*(.6+.4*fl),0,1);ctx.fillStyle="#ffe08a";ctx.beginPath();ctx.ellipse(ox,oy+1*S,7*S*Math.max(.35,W/1200),1.6*S,0,0,7);ctx.fill()}
      ctx.globalCompositeOperation="source-over";ctx.globalAlpha=1;return true});
    /* coladas de lava por las laderas */
    /* coladas de lava: lengua ancha e irregular con costra oscura, canal incandescente trenzado y brazos que se separan */
    ctx.lineCap="round";ctx.lineJoin="round";
    flows=flows.filter(f=>{f.t+=dt;if(f.t>f.life)return false;
      const fade=1-smooth((f.t-(f.life-3.5))/3.5);
      f.arms.forEach(a=>{
        const at=f.t-a.delay;if(at<=0)return;
        const prog=ease(at/a.adv),want=prog*a.len,heat=1-clamp((at-a.adv*.7)/(f.life-a.delay-a.adv*.7),0,1);
        const P=a.pts;let n=1;while(n<P.length-1&&P[n][2]<want)n++;
        /* 1) resplandor sobre la nieve */
        ctx.globalCompositeOperation="lighter";
        for(let i=1;i<=n&&i<P.length;i++){const q=P[i-1],r=P[i];ctx.strokeStyle=`rgba(255,80,20,${.16*fade*heat})`;ctx.lineWidth=(r[3]*2.6+4)*S;ctx.beginPath();ctx.moveTo(q[0],q[1]);ctx.lineTo(r[0],r[1]);ctx.stroke()}
        /* 2) costra oscura (bordes ya fríos), más ancha cuesta abajo */
        ctx.globalCompositeOperation="source-over";
        for(let i=1;i<=n&&i<P.length;i++){const q=P[i-1],r=P[i];ctx.strokeStyle=`rgba(${Math.round(70+50*heat)},${Math.round(22+12*heat)},12,${.92*fade})`;ctx.lineWidth=r[3]*S*1.35;ctx.beginPath();ctx.moveTo(q[0],q[1]);ctx.lineTo(r[0],r[1]);ctx.stroke()}
        /* 3) cuerpo naranja: se enfría primero en el frente y en los bordes */
        for(let i=1;i<=n&&i<P.length;i++){const q=P[i-1],r=P[i],u=r[2]/a.len,T=clamp(heat*(.95-.45*u)-(1-prog)*.05,0,1);
          ctx.strokeStyle=lavaColor(T*.85,fade*clamp(heat*1.4,0,1));ctx.lineWidth=r[3]*S*.85;ctx.beginPath();ctx.moveTo(q[0],q[1]);ctx.lineTo(r[0],r[1]);ctx.stroke()}
        /* 4) canal incandescente: dos hilos que se cruzan y parpadean */
        if(heat>.05){ctx.globalCompositeOperation="lighter";
          for(const side of [-1,1]){ctx.beginPath();for(let i=0;i<=n&&i<P.length;i++){const r=P[i],o=side*r[3]*.22*S*Math.sin(r[2]*.25+f.t*1.6+side);
              const x=r[0]+r[4]*o,y=r[1]+r[5]*o;i?ctx.lineTo(x,y):ctx.moveTo(x,y)}
            ctx.strokeStyle=`rgba(255,${210+Math.round(30*Math.random())},120,${.4*fade*heat*heat*(.8+.2*Math.random())})`;ctx.lineWidth=Math.max(.7,.9*S);ctx.stroke()}}
        /* 5) frente en forma de lóbulo, más brillante mientras avanza */
        const tip=P[Math.min(n,P.length-1)];
        if(prog<.995||heat>.6){const r=tip[3]*S*1.5;ctx.globalCompositeOperation="lighter";ctx.globalAlpha=fade*(prog<.995?.9:.5)*heat;ctx.drawImage(sprites.lava,tip[0]-r,tip[1]-r*.8,r*2,r*1.6);ctx.globalAlpha=1}
        ctx.globalCompositeOperation="source-over";
      });
      return true});
    /* columna de ceniza: sube rápido, frena, se abre como hongo y el viento la arrastra */
    for(const p of puffs){p.age+=dt;
      const h=oy-p.y,k=smooth(h/top);
      p.vy+=((-p.buoy*(1-k))-p.vy)*Math.min(1,p.drag*dt);
      p.vx+=((WIND*p.wind*S*clamp(W/1200,.5,1)*(.1+1.3*k))-p.vx)*Math.min(1,.7*dt);
      if(h>top*.92)p.vy*=1-Math.min(1,3*dt);
      p.x+=p.vx*dt;p.y+=p.vy*dt;p.r=p.r0+p.grow*(1-Math.exp(-p.age/2.2))+p.age*p.spread*k;
    }
    puffs=puffs.filter(p=>p.age<p.life);
    for(const p of puffs){
      const a=p.a*Math.min(1,p.age/.3)*(1-smooth((p.age/p.life-.5)/.5));if(a<=.01)continue;
      ctx.globalAlpha=a;const img=(p.lit?sprites.lit:sprites.ash)[p.spr%(p.lit?3:4)],r=p.r;
      ctx.drawImage(img,p.x-r*1.1,p.y-r,r*2.2,r*2);
    }
    ctx.globalAlpha=1;
    /* rayos volcánicos dentro de la nube */
    bolts=bolts.filter(b=>{b.t+=dt;if(b.t>b.d)return false;
      const on=b.t<.05||(b.t>.09&&b.t<.16);if(!on)return true;
      ctx.globalCompositeOperation="lighter";ctx.strokeStyle="rgba(206,214,255,.95)";ctx.lineWidth=1.4*S;ctx.shadowColor="#b9c4ff";ctx.shadowBlur=8*S;
      ctx.beginPath();b.pts.forEach((q,i)=>i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1]));ctx.stroke();
      ctx.shadowBlur=0;ctx.globalCompositeOperation="source-over";return true});
    /* ceniza que cae de la nube, inclinada por el viento */
    ctx.lineWidth=Math.max(.8,1*S);ctx.lineCap="round";
    fall=fall.filter(f=>{f.age+=dt;if(f.age>f.life)return false;
      f.x+=f.vx*dt;f.y+=f.vy*dt;if(f.y>ground(f.x))return false;
      const a=f.a*Math.min(1,f.age/.4)*(1-f.age/f.life);
      ctx.strokeStyle=`rgba(${f.c},${a})`;ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.lineTo(f.x-f.vx*.12,f.y-f.vy*.12);ctx.stroke();return true});
    /* bombas de lava: tiro parabólico, estela, se enfrían y ruedan por la ladera */
    const g=230*S;
    bombs=bombs.filter(b=>{b.age+=dt;
      if(!b.roll){b.vy+=g*dt;b.x+=b.vx*dt;b.y+=b.vy*dt;b.T-=.28*dt;b.trail.push([b.x,b.y]);if(b.trail.length>7)b.trail.shift();
        if(b.vy>0&&b.age>.12&&b.y>=ground(b.x)){b.roll=true;b.y=ground(b.x);b.dir=b.x<ox?-1:1;b.sp=R(14,34)*S}}
      else{b.sp*=1-Math.min(1,.9*dt);b.x+=b.dir*b.sp*dt;b.y=ground(b.x);b.T-=.42*dt;if(b.trail.length)b.trail.shift()}
      if(b.T<=0||b.y>H)return false;
      const T=clamp(b.T,0,1);
      if(b.trail.length>1){ctx.globalCompositeOperation="lighter";for(let i=1;i<b.trail.length;i++){const a=b.trail[i-1],c=b.trail[i];ctx.strokeStyle=lavaColor(T*.9,.5*i/b.trail.length);ctx.lineWidth=b.s*1.3*(i/b.trail.length);ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(c[0],c[1]);ctx.stroke()}}
      ctx.globalCompositeOperation="lighter";if(T>.35){const r=b.s*4*T;ctx.globalAlpha=T*.7;ctx.drawImage(sprites.lava,b.x-r,b.y-r,r*2,r*2);ctx.globalAlpha=1}
      ctx.globalCompositeOperation="source-over";ctx.fillStyle=lavaColor(T,Math.min(1,T*3));ctx.beginPath();ctx.arc(b.x,b.y,b.s,0,7);ctx.fill();return true});
    /* chispas que parpadean */
    ctx.globalCompositeOperation="lighter";
    sparks=sparks.filter(s=>{s.age+=dt;if(s.age>s.life)return false;s.vy+=g*.7*dt;s.vx*=1-.6*dt;s.x+=s.vx*dt;s.y+=s.vy*dt;
      const a=(1-s.age/s.life)*(.55+.45*Math.random());ctx.strokeStyle=lavaColor(1-s.age/s.life*.6,a);ctx.lineWidth=Math.max(.8,1.1*S);ctx.beginPath();ctx.moveTo(s.x,s.y);ctx.lineTo(s.x-s.vx*.035,s.y-s.vy*.035);ctx.stroke();return true});
    ctx.globalCompositeOperation="source-over";ctx.globalAlpha=1;
    if(emit.length||puffs.length||fall.length||bombs.length||sparks.length||flows.length||bolts.length||glows.length)raf=requestAnimationFrame(step);
    else{raf=0;ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);hero.classList.remove("v-on")}
  }
  function run(){if(!raf){last=performance.now();raf=requestAnimationFrame(step)}hero.classList.add("v-on")}
  /* resplandor en el cielo (detrás de los volcanes) */
  function skyGlow(kind,ms){
    if(!glowSky||!glowSky.animate)return;
    const sc=scene(),m=kind==="lava"?{night:.95,dusk:.75,dawn:.65,day:.32}[sc]:{night:.35,dusk:.25,dawn:.2,day:0}[sc];
    if(!m)return;
    glowSky.style.background=kind==="lava"?"":"radial-gradient(closest-side,rgba(255,170,110,.5),rgba(200,110,70,.18) 50%,rgba(160,80,50,0))";
    const kf=[{opacity:0}];for(let i=1;i<10;i++)kf.push({opacity:m*(kind==="lava"?(.7+.3*Math.random())*(i<7?1:(10-i)/4):(1-i/10)),offset:i/10});kf.push({opacity:0});
    glowSky.animate(kf,{duration:ms,easing:"ease-in-out"});
  }
  function ash(){
    geo();makeSprites();const sc=scene(),p=PAL[sc],big=Math.random()<.45,E=big?3.6:2.6,top=Math.min(oy*.62,110*S);
    glows.push({kind:"dull",t:0,d:1.4,r:30*S});skyGlow("ash",big?7000:5000);
    let acc=0;
    emit.push({t:0,fn:(t,dt)=>{
      if(t>E)return false;
      const rate=(big?30:22)*(1-.55*t/E);acc+=rate*dt;
      while(acc>=1){acc--;
        const jet=1-t/E;
        addPuff({x:ox+R(-3,3)*S,y:oy-1*S,vx:R(-8,8)*S,vy:-R(80,125)*S*(.55+.45*jet),buoy:R(10,20)*S*(big?1.2:1),drag:R(.9,1.4),wind:R(42,60),
          r0:R(7,10)*S,grow:R(24,36)*S*(big?1.25:1),spread:R(5,9)*S,life:R(8.5,11.5)*(big?1.15:1),a:R(.75,.95),lit:sc==="night"&&jet>.7&&Math.random()<.4});
      }
    }});
    /* caída de ceniza desde la parte alta de la nube */
    emit.push({t:0,fn:(t,dt)=>{
      if(t>E+5)return false;if(t<1.6)return;
      const hi=puffs.filter(q=>oy-q.y>top*.45);if(!hi.length)return;
      for(let i=0;i<Math.round(dt*(big?40:26));i++){const q=hi[(Math.random()*hi.length)|0];
        fall.push({x:q.x+R(-.6,.6)*q.r,y:q.y+q.r*.45,vx:WIND*R(10,22)*S,vy:R(16,28)*S,age:0,life:R(2.2,3.6),a:R(.18,.34),c:p.fall})}
    }});
    /* rayos dentro de la nube (se ven mejor sin sol) */
    if(sc!=="day"&&Math.random()<(big?.75:.4)){
      const n=big?2:1;
      for(let i=0;i<n;i++){const at=R(1,2.8);emit.push({t:0,fn:t=>{if(t<at)return;
        const cand=puffs.filter(q=>oy-q.y>top*.25);if(!cand.length)return false;
        const q=cand[(Math.random()*cand.length)|0];let x=q.x,y=q.y-q.r*.2;const pts=[[x,y]];
        const segs=5+((Math.random()*3)|0),len=R(40,70)*S;
        for(let j=0;j<segs;j++){x+=R(-7,7)*S;y+=len/segs;pts.push([x,y])}
        bolts.push({t:0,d:.2,pts});
        if(glowSky&&glowSky.animate)glowSky.animate([{opacity:0,background:"radial-gradient(closest-side,rgba(205,215,255,.55),rgba(205,215,255,0))"},{opacity:.9},{opacity:0}],{duration:220});
        return false}})}
    }
    run();
  }
  function lava(){
    geo();makeSprites();const sc=scene(),dur=R(4.8,6.4);
    glows.push({kind:"lava",t:0,d:dur+4.5,r:46*S});skyGlow("lava",(dur+5)*1000);
    const bursts=[0,R(1,1.6),R(2.2,3),R(3.4,4.4)].filter(b=>b<dur);
    const fire=(n,force)=>{
      for(let i=0;i<n;i++){const a=R(-.62,.62),v=R(95,165)*S*force,xs=clamp(W/1200,.45,1);
        bombs.push({x:ox+R(-4,4)*S,y:oy,vx:Math.sin(a)*v*(.55+.45*xs),vy:-Math.cos(a)*v,s:Math.max(1.1,R(1.3,2.5)*S),T:R(.95,1.1),age:0,trail:[]})}
      for(let i=0;i<n*2;i++){const a=R(-.5,.5),v=R(110,210)*S*force;sparks.push({x:ox+R(-3,3)*S,y:oy,vx:Math.sin(a)*v*.7,vy:-Math.cos(a)*v,age:0,life:R(.5,1.1)})}
    };
    bursts.forEach((b,i)=>emit.push({t:0,fn:t=>{if(t<b)return;fire(Math.round(R(8,13))*(i?1:1.3)|0,i?R(.85,1.05):1.1);return false}}));
    /* fuente continua y chorro de vapor/ceniza iluminado por abajo */
    let acc=0,accP=0;
    emit.push({t:0,fn:(t,dt)=>{if(t>dur)return false;acc+=dt*9;accP+=dt*4;
      while(acc>=1){acc--;const a=R(-.3,.3),v=R(50,90)*S;sparks.push({x:ox+R(-2,2)*S,y:oy,vx:Math.sin(a)*v,vy:-Math.cos(a)*v,age:0,life:R(.4,.8)})}
      while(accP>=1){accP--;addPuff({x:ox+R(-3,3)*S,y:oy-2*S,vx:R(-4,4)*S,vy:-R(30,50)*S,buoy:R(10,16)*S,drag:1,wind:R(24,36),r0:R(4,6)*S,grow:R(9,15)*S,spread:R(2,4)*S,life:R(5,7),a:R(.5,.7),lit:sc!=="day"})}
    }});
    /* coladas que bajan por la ladera, primero la del poniente */
    const both=Math.random()<.3,first=Math.random()<.6?0:1;
    FLOWS.forEach((f,i)=>{if(!both&&i!==first)return;const at=.5+(i!==first)*R(.8,1.4);
      emit.push({t:0,fn:t=>{if(t<at)return;
        const adv=R(6.5,8.5),main=arm(f.map(([x,y])=>[X(x),Y(y)]),R(0,9),1),arms=[Object.assign(main,{delay:0,adv})];
        /* uno o dos brazos que se separan de la colada principal y bajan por su cuenta */
        const nb=Math.random()<.6?2:1;
        for(let b=0;b<nb;b++){const k=R(.3,.7),P=main.pts,j=Math.max(2,Math.round(k*(P.length-1))),o=P[j],dir=(Math.random()<.5?-1:1);
          const len=main.len*R(.25,.45),dx=X(1200)/1200*dir*R(8,16),pts=[[o[0],o[1]]];
          for(let q=1;q<=4;q++){const u=q/4;pts.push([o[0]+dx*u+(P[Math.min(P.length-1,j+q*2)][0]-o[0])*.4*u,o[1]+len*u*.9])}
          const a=arm(pts,R(0,9),.7);a.delay=adv*k*R(.9,1.1);a.adv=adv*R(.35,.5);arms.push(a)}
        flows.push({t:0,adv,life:adv+R(6,8),arms});return false}});
    });
    run();
  }
  /* solo con la portada a la vista, la pestaña activa y sin "Reducir movimiento" */
  let seen=true;
  if("IntersectionObserver" in window)new IntersectionObserver(es=>{seen=es[0].isIntersecting;hero.classList.toggle("v-off",!seen)}).observe(hero);
  const can=()=>!RM.matches&&seen&&!document.hidden&&(typeof current==="undefined"||current===null);
  let timer=null;
  function next(ms){clearTimeout(timer);timer=setTimeout(()=>{
    if(can()&&!raf)(Math.random()<.5?ash:lava)();
    next(R(13000,26000));
  },ms)}
  addEventListener("resize",()=>{if(raf)geo()});
  window.__volcan={ash,lava};
  if(!RM.matches)next(R(4500,6500));
  if(RM.addEventListener)RM.addEventListener("change",()=>{if(!RM.matches)next(R(4500,6500))});
})();
/* fin volcán */
