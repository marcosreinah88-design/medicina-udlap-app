"""Íconos, etiqueta de tipo y grupos del Material extra.

Uso:
  python3 tools-xmat/patch_xmat.py <carpeta del sitio>      (site/ del repo o la copia del artefacto)

Parcha <sitio>/index.html, <sitio>/app.html (si existe) y <sitio>/s5/index.html. Idempotente
(marcas /*xmat*/): si ya está, solo actualiza el bloque de datos (xmat.js) y los estilos.

- xmat.js: tipos (examen, simulacro, simulador de casos, repaso, juego, quiz, tarjetas, calculadora,
  diapositivas, guía interactiva) con ícono SVG propio y color; tipo de cada material por id (o por
  título para los que agregue la persona); grupos de materiales parecidos (GR) que se muestran en una
  sola tarjeta con un botón por material. Agrupar solo cambia la vista: cada material conserva su id,
  su ruta (#mat-<id>, s5/#<id>), su página y su progreso guardado; el buscador sigue igual.
- Portada: Otros materiales (ícono y etiqueta por tipo, grupos), Material extra al final de cada
  semestre (etiqueta de tipo), buscador (etiqueta «<Tipo> · Material extra» en los resultados) y la
  biblioteca CTO (copias/versiones del mismo manual en una sola portada con botón «+1 versión»).
- 5º: Material extra del estante con ícono y etiqueta por tipo y los grupos.
Después: firmar (tools-subrayar/firmar.py <clave.pem>).
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
read = lambda p: open(p, encoding="utf-8").read()
JS = read(os.path.join(HERE, "xmat.js")).strip()
CSS = read(os.path.join(HERE, "xmat.css")).strip()
CSS5 = read(os.path.join(HERE, "xmat_s5.css")).strip()
site = sys.argv[1]


def rep(s, old, new, mark, name):
    """reemplazo exacto una sola vez; si ya está la marca, no hace nada"""
    if mark in s:
        return s
    n = s.count(old)
    assert n == 1, f"{name}: encontré {n} veces el texto a cambiar"
    return s.replace(old, new)


def block(s, tag, content, before, name):
    """mete o actualiza <tag id=xmat...> justo antes de `before`"""
    tid = "xmatCss" if tag == "style" else "xmatJs"
    new = f'<{tag} id="{tid}">\n{content}\n</{tag}>\n'
    m = re.search(rf'<{tag} id="{tid}">[\s\S]*?</{tag}>\n', s)
    if m:
        return s[:m.start()] + new + s[m.end():]
    assert s.count(before) == 1, f"{name}: no encontré dónde meter el {tag}"
    return s.replace(before, new + before)


# ---------------- portada ----------------
LAB = 'const lab=it=>{const X=window.XMAT&&XMAT.info(it,!!it.builtin&&!XMAT.ID[it.id]);return X?X.l:KIND[kindOf(it)].l};\n  '
GTILE = r'''function gtile(e){/*xmat*/
    const g=e.grp,I=XMAT.T[g.t],sems=[...new Set(e.items.map(it=>it.fromSem).filter(Boolean))],mixed=new Set(e.items.map(lab)).size>1;
    return `<div class="otile ogrp${e.items.length>4?" big":""}" style="--c:${I.c}">
      <span class="ot-art">${icon(I.svg)}<i>${esc(g.l||I.l)}</i><em>${e.items.length} en 1</em></span>
      <span class="ot-txt"><b>${esc(g.title)}</b><small>${esc([sems.length===1?SEMNAME[sems[0]]||"":"",e.items.length+" materiales juntos"].filter(Boolean).join(" · "))}</small></span>
      <span class="og-list">${e.items.map(it=>{const L=look(it);return `<a class="og-it" href="${esc(it.href)}"${it.builtin||it.inpage?"":' target="_blank" rel="noopener"'} style="--c:${L.c}" title="Abrir ${esc(it.title)}"><span class="og-ic">${icon(L.svg)}</span><span><b>${esc(XMAT.short(it))}</b>${(t=>t?`<small>${esc(t)}</small>`:"")(mixed?lab(it):sems.length>1?SEMNAME[it.fromSem]||lab(it):"")}</span></a>`}).join("")}</span>
    </div>`;
  }
  '''
DEDUP = r'''/*xmat*/const dkey=it=>norm(nice(it.title)).replace(/\s*\(vol\.?\s*\d+\)/,"").replace(/\s*(\(\d+\)|copia|\d+)\s*$/,"").replace(/[^a-z0-9]+/g," ").trim()+"|"+volOf(it.title);
  /* copias o versiones del mismo manual (p. ej. «CTO Anatomía» y «CTO Anatomía 2»): una sola portada; las demás con «+1 versión» */
  function dedup(list){const m=new Map(),out=[];for(const it of list){const k=dkey(it);if(m.has(k)){m.get(k).dups.push(it);continue}const c={...it,dups:[]};m.set(k,c);out.push(c)}return out}
  '''


def hub(p):
    if not os.path.exists(p):
        return
    s = read(p)
    s = block(s, "style", CSS, "<script>\n/* ===== Biblioteca CTO", p)
    s = block(s, "script", JS, "<script>\n/* ===== Biblioteca CTO", p)
    # Otros materiales
    s = rep(s, 'function look(it){const t=norm(it.title);',
            LAB + 'function look(it){/*xmat*/const X=window.XMAT&&XMAT.info(it,!!it.builtin&&!XMAT.ID[it.id]);if(X&&X.k!=="interactivo")return {c:X.c,svg:X.svg};const t=norm(it.title);',
            "function look(it){/*xmat*/", "look")
    s = rep(s, '<span class="ot-art">${icon(L.svg)}<i>${k.b}</i></span>',
            '<span class="ot-art">${icon(L.svg)}<i>${esc(lab(it))}</i></span>', '<i>${esc(lab(it))}</i>', "tile badge")
    s = rep(s, '[it.fromSem?SEMNAME[it.fromSem]||"":k.l,', '[lab(it),it.fromSem?SEMNAME[it.fromSem]||"":"",',
            '[lab(it),it.fromSem', "tile small")
    s = rep(s, 'list=list.filter(it=>norm(it.title+" "+it.subject+" "+KIND[kindOf(it)].l).includes(qq));',
            'list=list.filter(it=>norm(it.title+" "+it.subject+" "+KIND[kindOf(it)].l+" "+lab(it)+" "+((window.XMAT&&XMAT.GR.find(g=>g.ids.includes(it.id)))||{title:""}).title).includes(qq));',
            '+" "+lab(it)+" "+((window.XMAT', "filtro")
    s = rep(s, 'const by=new Map();for(const it of list){const g=it.subject||"Sin materia";if(!by.has(g))by.set(g,[]);by.get(g).push(it)}',
            'const ents=window.XMAT?XMAT.group(list):list.map(it=>({it}));const by=new Map();for(const e of ents){const g=e.grp?e.grp.subject:e.it.subject||"Sin materia";if(!by.has(g))by.set(g,[]);by.get(g).push(e)}',
            "const ents=window.XMAT?XMAT.group(list)", "grupos")
    s = rep(s, '<h3>${esc(g)} <small>${by.get(g).length}</small></h3><div class="ogrid">${by.get(g).map(tile).join("")}</div>',
            '<h3>${esc(g)} <small>${by.get(g).reduce((n,e)=>n+(e.grp?e.items.length:1),0)}</small></h3><div class="ogrid">${by.get(g).map(e=>e.grp?gtile(e):tile(e.it)).join("")}</div>',
            "e.grp?gtile(e):tile(e.it)", "estantes")
    s = rep(s, 'function render(){\n    const grid=$("#otrGrid");', GTILE + 'function render(){\n    const grid=$("#otrGrid");',
            "function gtile(e){/*xmat*/", "gtile")
    # Material extra al final de cada semestre
    s = rep(s, '<span><b>${esc(it.title)}</b><small>${esc(k.l)}</small></span></a>',
            '<span><b>${esc(it.title)}</b><small>${esc(lab(it))}${it.fromSem?" · "+esc(SEMNAME[it.fromSem]||""):""}</small></span></a>',
            '<small>${esc(lab(it))}${it.fromSem', "semestre")
    s = rep(s, 'const ctos=window.CtoLib&&CtoLib.items?CtoLib.items():[];',
            'const ctos=window.CtoLib&&CtoLib.items?(CtoLib.dedup||(x=>x))(CtoLib.items()):[];/*xmat*/', "CtoLib.items()):[];/*xmat*/", "cto semestre")
    s = rep(s, '<span><b>${esc(it.title)}</b><small>Manual CTO · se abre en Drive</small></span></a>`}',
            '<span><b>${esc(it.title)}</b><small>Manual CTO · se abre en Drive${it.dups&&it.dups.length?" · otra versión en la biblioteca CTO":""}</small></span></a>`}',
            "otra versión en la biblioteca CTO", "cto semestre texto")
    # buscador
    s = rep(s, '<span class="rs">${esc(ord(g.sem))} semestre · ${mark(g.area,terms)}</span>',
            '<span class="rs">${esc(ord(g.sem))} semestre · ${mark(g.area,terms)}${window.XMAT?XMAT.badge(g):""}</span>',
            "XMAT.badge(g)", "buscador")
    # biblioteca CTO: repetidos
    s = rep(s, 'document.querySelectorAll("#ctoChips [data-f]").forEach(c=>{\n      const g=c.dataset.f,n=g==="all"?items.length:g==="sem"?items.filter(isSem).length:items.filter(it=>spec(it)[2]===g).length;',
            'document.querySelectorAll("#ctoChips [data-f]").forEach(c=>{const dd=dedup(items);/*xmat*/\n      const g=c.dataset.f,n=g==="all"?dd.length:g==="sem"?dd.filter(isSem).length:dd.filter(it=>spec(it)[2]===g).length;', "const dd=dedup(items);/*xmat*/", "cto chips")
    s = rep(s, '  function render(){\n    const grid=$("#ctoGrid");', '  ' + DEDUP + 'function render(){\n    const grid=$("#ctoGrid");',
            "/*xmat*/const dkey", "cto dedup")
    s = rep(s, 'if(qq)list=list.filter(it=>norm(it.title+" "+it.subject).includes(qq));',
            'if(qq)list=list.filter(it=>norm(it.title+" "+it.subject).includes(qq));list=dedup(list);',
            "list=dedup(list);", "cto lista")
    s = rep(s, '${v?`<i>Vol. ${esc(v)}</i>`:""}</span>',
            '${v?`<i>Vol. ${esc(v)}</i>`:""}</span>\n      ${it.dups&&it.dups.length?`<button class="cb-dup" type="button" data-dup="${esc(it.dups[0].href)}" title="Abrir ${esc(it.dups.map(d=>d.title).join(", "))}">+${it.dups.length} ${it.dups.length>1?"versiones":"versión"}</button>`:""}',
            'class="cb-dup"', "cto portada")
    s = rep(s, '$("#ctoGrid").addEventListener("click",ev=>{\n    const d=ev.target.closest("[data-del]");',
            '$("#ctoGrid").addEventListener("click",ev=>{\n    const du=ev.target.closest("[data-dup]");if(du){ev.preventDefault();ev.stopPropagation();window.open(du.dataset.dup,"_blank","noopener");return}/*xmat*/\n    const d=ev.target.closest("[data-del]");',
            'closest("[data-dup]")', "cto clic")
    s = rep(s, 'return {open,close,set,items:()=>items,util:{spec,icon,norm,mb,BOOK,nice}};',
            'return {open,close,set,items:()=>items,dedup,util:{spec,icon,norm,mb,BOOK,nice}};', "items:()=>items,dedup,", "cto api")
    open(p, "w", encoding="utf-8").write(s)
    print("portada:", p)


# ---------------- 5º ----------------
RENDER5 = r'''function renderExtra(){/*xmat:render*/
  const q=norm($("#q").value.trim()),X=window.XMAT;
  const GO='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  const inGrp=x=>(X.GR.find(g=>g.ids.includes(x.id))||{title:""}).title;
  const list=EXTRA.filter(x=>!q||norm(x.title+" "+x.desc+" "+x.tags+" "+inGrp(x)+" "+((X.info(x)||{}).l||"")).includes(q));
  $(".extra").hidden=!!q&&!list.length;
  const ic=I=>`<span class="xi" aria-hidden="true">${I.svg?X.svg(I.svg):`<svg viewBox="0 0 24 24">${I.s24}</svg>`}</span>`;
  const stats=x=>x.stats.slice(0,2).map(s=>s[0]+" "+s[1]).join(" · ");
  $("#xlist").innerHTML=X.group(list).map(e=>{
    if(!e.grp){const x=e.it,I=X.info(x)||{l:"Material extra",s24:XICONS[x.id]||XICON};
      return `<button class="xitem" type="button" data-open="${x.id}"${I.c?` style="--xc:${I.c}"`:""}>${ic(I)}<span><span class="xtag"><i>${esc(I.l)}</i></span><h3>${hl(x.title,q)}</h3><p>${hl(x.desc,q)}</p><span class="xmeta">${x.stats.map(s=>`<span><b>${s[0]}</b> ${s[1]}</span>`).join("")}</span></span><span class="xgo">Abrir${GO}</span></button>`}
    const g=e.grp,I=X.T[g.t],mixed=new Set(e.items.map(x=>(X.info(x)||{}).k)).size>1;
    return `<div class="xitem xgrp" style="--xc:${I.c}">${ic(I)}<span><span class="xtag"><i>${esc(g.l||I.l)} · ${e.items.length} en 1</i></span><h3>${hl(g.title,q)}</h3><p>${hl(g.desc,q)}</p></span><div class="xsubs">${e.items.map(x=>{const J=X.info(x)||I;return `<button class="xsub" type="button" data-open="${x.id}" style="--xc:${J.c}" title="${esc(x.desc)}">${ic(J)}<span><b>${hl(X.short(x),q)}</b><small>${esc([mixed?J.l:"",stats(x)].filter(Boolean).join(" · "))}</small></span>${GO}</button>`}).join("")}</div></div>`;
  }).join("");
}
'''


def s5(p):
    if not os.path.exists(p):
        return
    s = read(p)
    # estilos y datos justo antes del script principal (después del <style> propio de la página)
    s = re.sub(r'<(style|script) id="xmat(Css|Js)">[\s\S]*?</\1>\n', "", s)
    i = s.index("const EXTRA=[")
    j = s.rfind("<script>", 0, i)
    s = s[:j] + f'<style id="xmatCss">\n{CSS5}\n</style>\n<script id="xmatJs">\n{JS}\n</script>\n' + s[j:]
    s, n = re.subn(r"function renderExtra\(\)\{[\s\S]*?\n\}\n", lambda m: RENDER5, s, count=1)
    assert n == 1, "5º: no encontré renderExtra"
    open(p, "w", encoding="utf-8").write(s)
    print("5º:", p)


for name in ("index.html", "app.html"):
    hub(os.path.join(site, name))
s5(os.path.join(site, "s5", "index.html"))
