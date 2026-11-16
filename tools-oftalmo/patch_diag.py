"""Agrega a la guía de Oftalmología (5º) la parte de diagnóstico, la tabla de ojo rojo, la de fármacos
con dosis y el bloque 07 de casos clínicos con «Ponme a prueba». Contenido en diag_temas.py.

Uso: python3 tools-oftalmo/patch_diag.py [ruta/a/s5/oftalmo/index.html ...]   (sin argumentos: site/s5/oftalmo/index.html)
     python3 tools-oftalmo/patch_diag.py --amboss     (agrega los términos nuevos a tools-amboss/terminos.tsv)
Idempotente: todo lo agregado lleva data-dx (HTML) o /*dx*/ (JS) y se quita antes de volver a ponerlo.
Sirve igual para la copia del artefacto (que solo difiere en la línea de fuentes).
Después: tools-amboss/build.py, node tools-estudio/banco.js, node tools-buscador/apartados.js,
palabras nuevas al buscador (buscador_oftalmo.py) y tools-subrayar/firmar.py.
"""
import sys, os, re, json
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import diag_temas as D  # noqa: E402

SITE = os.path.join(HERE, '..', 'site')


def topic(title, key, body):
    return (f'\n  <details class="topic" data-dx="{key}"><summary>{title} <span class="tag">nuevo</span></summary>'
            f'<div class="body">{body.rstrip()}\n  </div></details>\n')


def caso_html(i, c):
    title, vin, qs = c
    items = []
    for j, (q, opts, ok, ex) in enumerate(qs):
        bs = ''.join(f'<button type="button" class="opt" data-l="{"ABCD"[k]}">{escape(o)}</button>' for k, o in enumerate(opts))
        items.append(f'<div class="cz-item" data-ok="{ok}"><h4>{j + 1}. {escape(q)}</h4><div class="opts">{bs}</div>'
                     f'<p class="expl" hidden>{escape(ex)}</p></div>')
    return (f'\n  <details class="topic" data-dx="caso{i + 1}"><summary>Caso {i + 1}: {escape(title)}</summary><div class="body">'
            f'<div class="caso" data-caso="{i + 1}"><p class="cz-vin">{escape(vin)}</p>'
            f'<button type="button" class="btn pri cz-go">Ponme a prueba</button>'
            f'<div class="cz-q" hidden>{"".join(items)}<p class="cz-res" hidden></p>'
            f'<button type="button" class="chipbtn cz-again" hidden>Intentar otra vez</button></div></div>\n  </div></details>\n')


B7 = ('\n<!-- ========== 07 ========== -->\n<section class="block" id="b7" data-dx="b7" style="--c:var(--h7)">\n'
      '  <div class="block-h"><span class="n">07</span><h2>Casos clínicos</h2></div>\n'
      '  <div class="note dx-intro"><b>Cómo usarlos</b>Lee el caso, piensa tu respuesta y luego toca <b>Ponme a prueba</b>. '
      'Son casos escritos para practicar con lo que viene en la guía; los datos que no vienen de tus apuntes van con †.'
      ' <button type="button" class="chipbtn cz-rand">Ponme a prueba con un caso al azar</button></div>\n'
      + ''.join(caso_html(i, c) for i, c in enumerate(D.CASOS)) + '</section>\n')

CSS = ('<style data-dx>'
       ':root{--h7:#a13d6b}'
       '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--h7:#ec8fbb}}'
       ':root[data-theme="dark"]{--h7:#ec8fbb}'
       '.dx-dag{color:var(--muted);font-size:.75em;margin-left:1px}'
       '.dx-cmp td:first-child{font-weight:700;white-space:nowrap}'
       '.caso{display:grid;gap:12px}.cz-vin{background:color-mix(in srgb,var(--c,var(--accent)) 8%,var(--surface));border:1px solid var(--line);border-radius:12px;padding:12px 14px;max-width:none!important}'
       '.cz-go{justify-self:start}.cz-q{display:grid;gap:14px}.cz-item{display:grid;gap:8px}.cz-item h4{margin:0!important}'
       '.cz-res{font-weight:700}.cz-again{justify-self:start}.dx-intro .cz-rand{margin-top:8px;display:inline-block}'
       '</style>')

JS = r'''<script data-dx>/*dx-casos*/(function(){
var K="oft-casos",st={};try{st=JSON.parse(localStorage.getItem(K)||"{}")}catch(e){}
function save(){try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
document.querySelectorAll(".caso").forEach(function(c){
  var id=c.getAttribute("data-caso"),go=c.querySelector(".cz-go"),q=c.querySelector(".cz-q"),res=c.querySelector(".cz-res"),again=c.querySelector(".cz-again");
  var items=[].slice.call(c.querySelectorAll(".cz-item"));
  function reset(){items.forEach(function(it){it.removeAttribute("data-done");it.querySelectorAll(".opt").forEach(function(b){b.disabled=false;b.classList.remove("right","wrong")});it.querySelector(".expl").hidden=true});res.hidden=true;again.hidden=true}
  function check(){var done=items.filter(function(it){return it.hasAttribute("data-done")});if(done.length<items.length)return;
    var ok=done.filter(function(it){return it.getAttribute("data-done")==="1"}).length;
    res.textContent=(ok===items.length?"Muy bien: ":"Resultado: ")+ok+" de "+items.length+" correctas."+(st[id]!=null?" La vez anterior: "+st[id]+" de "+items.length+".":"");
    res.style.color=ok===items.length?"var(--ok)":"var(--warn)";res.hidden=false;again.hidden=false;st[id]=ok;save()}
  go.onclick=function(){q.hidden=false;go.hidden=true;var f=q.querySelector(".opt");if(f)f.focus({preventScroll:true})};
  again.onclick=reset;
  items.forEach(function(it){var ok=+it.getAttribute("data-ok"),bs=[].slice.call(it.querySelectorAll(".opt")),ex=it.querySelector(".expl"),base=ex.textContent;
    bs.forEach(function(b,i){b.onclick=function(){bs.forEach(function(x,j){x.disabled=true;if(j===ok)x.classList.add("right")});
      if(i!==ok)b.classList.add("wrong");it.setAttribute("data-done",i===ok?"1":"0");
      ex.textContent=(i===ok?"Correcto. ":"Incorrecto. ")+base;ex.hidden=false;check()}})})});
var r=document.querySelector(".cz-rand");if(r)r.onclick=function(){
  var cs=[].slice.call(document.querySelectorAll("#b7 details.topic")),pend=cs.filter(function(d){return st[d.querySelector(".caso").getAttribute("data-caso")]==null});
  var pool=pend.length?pend:cs,d=pool[Math.floor(Math.random()*pool.length)];if(!d)return;
  d.open=true;var g=d.querySelector(".cz-go");if(g&&!g.hidden)g.click();d.scrollIntoView({behavior:"smooth",block:"start"})};
})();</script>'''

TOC_LI = ('<li data-dx="toc"><a href="#b7" style="--c:var(--h7)"><span class="n">07</span><span class="tt">Casos clínicos</span>'
          '<span class="tp" data-b="b7"></span></a></li>')


def js_row(x):
    return '\n,' + json.dumps(list(x), ensure_ascii=False) + '/*dx*/'


def patch(s):
    # quitar lo anterior
    s = re.sub(r'\n  <details class="topic" data-dx="[^"]*">.*?</details>\n', '', s, flags=re.S)
    s = re.sub(r'\n<!-- ========== 07 ========== -->\n<section class="block" id="b7" data-dx="b7".*?</section>\n', '', s, flags=re.S)
    s = re.sub(r'<style data-dx>.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<script data-dx>.*?</script>', '', s, flags=re.S)
    s = s.replace('\n        ' + TOC_LI, '')
    s = re.sub(r'\n,\[.*?\]/\*dx\*/', '', s)

    def after_topic(s, title_start, html):
        m = re.search(r'<details class="topic"><summary>' + re.escape(title_start), s)
        assert m, title_start
        end = s.index('</details>', m.end()) + len('</details>')
        return s[:end] + '\n' + html.rstrip('\n') + s[end:]

    # bloque 06: después de «Exploración: agudeza…»
    s = after_topic(s, 'Exploración: agudeza, campo, color y pupilas', ''.join(topic(t, k, b) for t, k, b in D.B6))
    # bloque 05: al final (antes del comentario del bloque 06)
    i = s.index('\n<!-- ========== 06 ========== -->')
    j = s.rindex('</section>', 0, i)
    s = s[:j] + ''.join(topic(t, k, b) for t, k, b in D.B5) + s[j:]
    # bloque 07: después del bloque 06, antes del aviso «No hay temas»
    i = s.index('<p id="noRes"')
    s = s[:i] + B7 + s[i:]
    # índice lateral
    anchor = '<span class="tp" data-b="b6"></span></a></li>'
    s = s.replace(anchor, anchor + '\n        ' + TOC_LI, 1)
    # textos de portada y BLOCKS
    s = s.replace('<span><b>6</b> bloques</span>', '<span><b>7</b> bloques</span>')
    s = s.replace('Resumen de tus apuntes de clase en seis bloques.', 'Resumen de tus apuntes de clase en seis bloques y casos clínicos para practicar.')
    s = re.sub(r'(b6:"Refracción y exploración")(\};)', r'\1,b7:"Casos clínicos"\2', s)
    # tarjetas y quiz
    i = s.index('\n];\nconst QUIZ=[')
    s = s[:i] + ''.join(js_row(c) for c in D.CARDS) + s[i:]
    q0 = s.index('const QUIZ=[')
    i = s.index('\n];', q0)
    s = s[:i] + ''.join(js_row(q) for q in D.QUIZ) + s[i:]
    # estilos y script
    s = s.replace('</head>', CSS + '</head>', 1)
    i = s.index('<script src="../../anki/anki.js"')
    s = s[:i] + JS + s[i:]
    return s


def amboss():
    p = os.path.join(HERE, '..', 'tools-amboss', 'terminos.tsv')
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'\n# dx-oftalmo:inicio.*?# dx-oftalmo:fin', '', t, flags=re.S)
    rows = [f'{a}\t{b}' for a, b in D.AMBOSS] + [f'{D.CASOS_T} › Caso {i + 1}: {c[0]}\t-' for i, c in enumerate(D.CASOS)]
    block = '\n# dx-oftalmo:inicio (lo pone tools-oftalmo/patch_diag.py --amboss)\n' + '\n'.join(rows) + '\n# dx-oftalmo:fin'
    anchor = 'Pares craneales en la exploración\tcranial nerves eye examination'
    assert anchor in t
    t = t.replace(anchor, anchor + block, 1)
    open(p, 'w', encoding='utf-8').write(t)
    print('terminos.tsv:', len(rows), 'términos de Oftalmología')


if __name__ == '__main__':
    if sys.argv[1:] == ['--amboss']:
        amboss()
        sys.exit()
    for dst in sys.argv[1:] or [os.path.join(SITE, 's5', 'oftalmo', 'index.html')]:
        s = open(dst, encoding='utf-8').read()
        s2 = patch(s)
        open(dst, 'w', encoding='utf-8').write(s2)
        print(dst, len(s), '→', len(s2), 'bytes')
