#!/usr/bin/env python3
# Buscador de la portada: al abrir una guía y buscar la palabra adentro, ya no recorre
# los apartados "como loco". Ahora:
#   1) busca primero lo que ya se ve, luego lo escondido (abre su apartado), luego el buscador propio de la guía;
#   2) solo si nada de eso funciona recorre los apartados UNA vez (no una vez por palabra), con límite de 20 s,
#      y únicamente con palabras que sí existen en esa guía (lista FT del hub);
#   3) mientras recorre, la guía se atenúa y no se puede tocar (para que no se vea brincando);
#   4) si no la encuentra, regresa la guía a su inicio y avisa "No encontré … Te dejé en el inicio" (se quita sola).
# Uso: python3 tools-buscador/patch_buscador.py site/index.html site/app.html [artefacto.html]   (idempotente)
import sys

MARK = '/*buscador-v2*/'

REPL = [
# brute: varias palabras a la vez, límite configurable, devuelve la palabra encontrada y regresa al inicio si falla
('''  async function brute(doc,win,t,my){''',
 '''  async function brute(doc,win,ts,my,ms){''' + MARK),
('''    const found=async()=>{const v=textHits(doc,t);if(!v.length)return false;if(v.some(h=>shown(h.node.parentElement,win)))return true;return await reveal(v[0],doc,win,my)};''',
 '''    const found=async()=>{for(const t of ts){const v=textHits(doc,t);if(!v.length)continue;if(v.some(h=>shown(h.node.parentElement,win)))return t;if(await reveal(v[0],doc,win,my))return t}return false};'''),
('''    const homeSet=new Set(cands(doc,win).map(c=>c.s));let hit=false;const later=[];
    const out=()=>my!==token||Date.now()-t0>25000;''',
 '''    const homeSet=new Set(cands(doc,win).map(c=>c.s));let hit=false;const later=[];
    const out=()=>my!==token||Date.now()-t0>(ms||9000);'''),
('''        if(await found()){hit=true;break}
        const sub=''',
 '''        if((hit=await found()))break;
        const sub='''),
('''          if(await found()){hit=true;break}
        }''',
 '''          if((hit=await found()))break;
        }'''),
('''    }finally{
      if(ls)try{''',
 '''      if(!hit&&my===token)await goHome();
    }finally{
      if(ls)try{'''),
# locate: orden barato → caro, un solo recorrido, aviso final
('''  async function locate(frame,q,my){
    const win=frame.contentWindow,doc=frame.contentDocument;if(!doc)return;
    const terms=[fold(q)].concat(fold(q).split(/\\s+/).filter(x=>x.length>2).sort((a,b)=>b.length-a.length));
    for(const t of [...new Set(terms)]){
      if(my!==token)return;
      label=t;ctx={doc,win,t};
      let all=textHits(doc,t);
      if(!all.length){
        for(const box of searchBoxes(doc,win)){box.value=q;["input","keyup","change"].forEach(ev=>box.dispatchEvent(new win.Event(ev,{bubbles:true})));await wait(250);all=textHits(doc,t);if(all.length)break;box.value="";box.dispatchEvent(new win.Event("input",{bubbles:true}))}
      }
      if(!all.length||!visibleHits(doc,win,t).length){
        if(all.length&&await reveal(all[0],doc,win,my)&&visibleHits(doc,win,t).length){}
        else{say(`Buscando “${q}” en los apartados de la guía…`,false);await brute(doc,win,t,my)}
      }
      hits=textHits(doc,t);
      if(hits.length){const vi=hits.findIndex(h=>shown(h.node.parentElement,win));await focusHit(vi<0?0:vi,my);return}
    }
    say(`No encontré “${q}” dentro de esta guía`,false);
  }''',
 '''  async function locate(frame,q,my,gid){
    const win=frame.contentWindow,doc=frame.contentDocument;if(!doc)return;
    const fq=fold(q).replace(/\\s+/g," ").trim();
    const terms=[...new Set([fq].concat(fq.split(" ").filter(x=>x.length>2).sort((a,b)=>b.length-a.length)))].filter(Boolean);
    const pick=async t=>{label=t;ctx={doc,win,t};hits=textHits(doc,t);if(!hits.length)return false;const vi=hits.findIndex(h=>shown(h.node.parentElement,win));await focusHit(vi<0?0:vi,my);return true};
    /* 1) lo que ya se ve */
    for(const t of terms){if(my!==token)return;if(visibleHits(doc,win,t).length&&await pick(t))return}
    /* 2) está en la página pero escondido: abrir su apartado */
    for(const t of terms){if(my!==token)return;const all=textHits(doc,t);if(all.length&&await reveal(all[0],doc,win,my)&&visibleHits(doc,win,t).length&&await pick(t))return}
    /* 3) el buscador propio de la guía */
    for(const box of searchBoxes(doc,win)){if(my!==token)return;box.value=q;["input","keyup","change"].forEach(ev=>box.dispatchEvent(new win.Event(ev,{bubbles:true})));await wait(250);
      for(const t of terms)if(textHits(doc,t).length&&await pick(t))return;
      box.value="";box.dispatchEvent(new win.Event("input",{bubbles:true}))}
    /* 4) recorrer los apartados UNA sola vez, con límite, y solo con palabras que sí están en esta guía */
    const ft=gid&&typeof FT==="object"&&FT[gid]?" "+FT[gid]:null;
    const known=t=>!ft||t.split(" ").every(w=>w.length<4||ft.includes(w));
    const bt=terms.filter(known);
    let t=null;
    if(bt.length&&my===token){
      say(`Buscando “${q}” en los apartados de la guía…`,false);
      const st=frame.style,o=[st.opacity,st.pointerEvents,st.transition];st.transition="opacity .2s";st.opacity=".35";st.pointerEvents="none";
      try{t=await brute(doc,win,bt,my,20000)}finally{[st.opacity,st.pointerEvents,st.transition]=o}
    }
    if(my!==token)return;
    if(t&&await pick(t))return;
    ctx=null;hits=[];try{win.scrollTo(0,0)}catch(e){}
    let inData=false;try{inData=terms.some(t=>fold(doc.documentElement.innerHTML).includes(t))}catch(e){}
    say(inData?`No encontré “${q}” a la vista; seguramente está en las preguntas o tarjetas de esta guía (salen al practicar). Te dejé en el inicio.`:`No encontré “${q}” dentro de esta guía. Te dejé en el inicio.`,false);
    setTimeout(()=>{if(my===token)close()},6000);
  }'''),
('''  function run(frame,q){
    const my=++token;if(ctx)clearMarks(ctx.doc);hits=[];
    say(`Buscando “${q}”…`,false);
    const go=()=>setTimeout(()=>locate(frame,q,my).catch(''',
 '''  function run(frame,q,gid){
    const my=++token;if(ctx)clearMarks(ctx.doc);hits=[];
    say(`Buscando “${q}”…`,false);
    const go=()=>setTimeout(()=>locate(frame,q,my,gid).catch('''),
('''const f=show(g.sem,g);if(q)Finder.run(f,decodeURIComponent(q));else Finder.close()''',
 '''const f=show(g.sem,g);if(q)Finder.run(f,decodeURIComponent(q),g.id);else Finder.close()'''),
]

for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    if MARK in s:
        print(f, ': ya tenía el arreglo'); continue
    for a, b in REPL:
        n = s.count(a)
        if n != 1:
            sys.exit('%s: esperaba 1 vez y hay %d de:\n%s' % (f, n, a[:120]))
        s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s)
    print(f, ': listo')
