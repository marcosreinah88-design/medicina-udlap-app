# Mete los esquemas propios (tools-farmaco/img/) en las guías de Farmacología Básica (3º) y Farmacología II (4º).
# Idempotente: quita el bloque <!--fx-->…<!--/fx--> anterior y lo vuelve a poner.
# Uso: python3 tools-farmaco/patch_farmaco.py [carpeta del sitio]   (por defecto site/; sirve igual para la copia del artefacto)
import json, os, sys, re
from urllib.parse import quote
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'site')
CRED = 'Esquema propio, hecho a partir de los apuntes de la clase.'

# clave → [(archivo, pie)]. Básica: "unidad|título del apartado"; Farmacología II: id del tema.
BASICA = {
 'farmacocinetica|Concepto y vías de administración': [('ladme.svg', '<b>LADME.</b> Solo el fármaco libre (no unido a albúmina) se distribuye, actúa, se metaboliza y se elimina; la vía IV se salta la liberación y la absorción.')],
 'farmacocinetica|Absorción y transporte a través de membranas': [('transporte-membranas.svg', '<b>Mecanismos de transporte.</b> La mayoría de los fármacos cruza por difusión pasiva: liposolubles y no ionizados, a favor del gradiente.')],
 'farmacocinetica|pKa y ecuación de Henderson-Hasselbalch': [('atrapamiento-ionico.svg', '<b>Atrapamiento iónico</b> con el ejemplo de la clase: el naproxeno (pKa 5) se ioniza en el plasma y queda «atrapado» (252 vs 1.001 en el jugo gástrico).')],
 'farmacocinetica|Primer paso, profármacos y biodisponibilidad': [
    ('primer-paso.svg', '<b>Primer paso hepático.</b> Lo que se absorbe en el intestino pasa por la porta al hígado antes de llegar a la circulación; las vías sublingual e IV lo evitan.'),
    ('biodisponibilidad.svg', '<b>Curva concentración-tiempo.</b> Biodisponibilidad oral = AUC oral / AUC IV; la ventana terapéutica queda entre la concentración mínima eficaz y la tóxica.')],
 'farmacocinetica|Metabolismo (biotransformación) y CYP450': [('fases-metabolismo.svg', '<b>Fase I y fase II.</b> La fase I cambia la estructura (CYP450) y puede activar o inactivar; la fase II conjuga para volver el fármaco hidrosoluble.')],
 'farmacocinetica|Excreción': [('excrecion-renal.svg', '<b>Excreción renal.</b> Filtración del fármaco libre, secreción activa en el túbulo proximal y reabsorción pasiva solo de la forma no ionizada.')],
 'farmacodinamia|Tipos de receptores': [('tipos-receptores.svg', '<b>Familias de receptores</b> y qué tan rápido responden; con ejemplos de la tabla de canales de la clase.')],
 'farmacodinamia|Afinidad, curvas dosis-respuesta, eficacia y potencia': [('potencia-eficacia.svg', '<b>Potencia vs eficacia.</b> La potencia se lee en la EC50 (eje horizontal); la eficacia, en la altura del techo.')],
 'farmacodinamia|Agonistas, antagonistas y sinergismo': [('agonistas-antagonistas.svg', '<b>Cómo se mueve la curva.</b> El antagonista competitivo la corre a la derecha; el no competitivo baja el máximo; el agonista parcial nunca llega al 100 %.')],
 'posologia|Concentración y porcentajes': [('concentraciones.svg', '<b>Equivalencias que más se usan</b> para pasar de porcentaje o proporción a mg/mL antes de la regla de tres.')],
 'rams|Teratogenicidad': [('teratogenia.svg', '<b>Periodos de susceptibilidad.</b> Las semanas 3 a 8 (organogénesis) concentran las malformaciones mayores.')],
 'desarrollo|Desarrollo clínico': [('fases-desarrollo.svg', '<b>Fases del desarrollo de un fármaco</b> con las cifras de participantes de la clase.')],
 'interacciones|Interacciones farmacocinéticas': [('interacciones-cyp.svg', '<b>Inductores e inhibidores del CYP450.</b> El inhibidor sube los niveles del otro fármaco (toxicidad); el inductor los baja (falla terapéutica).')],
 'antiinflamatorios|Inflamación y mediadores': [('acido-araquidonico.svg', '<b>Cascada del ácido araquidónico.</b> Los glucocorticoides frenan la fosfolipasa A₂ (ambas ramas); los AINE solo la COX.')],
 'antiinflamatorios|AINE: COX-1 vs COX-2': [('cox1-cox2.svg', '<b>COX-1 vs COX-2.</b> Por qué el AINE no selectivo daña estómago y riñón, y por qué los coxibs aumentan el riesgo trombótico.')],
 'antiinflamatorios|Analgésicos opioides': [('opioides.svg', '<b>Receptor μ en la sinapsis del dolor.</b> Menos neurotransmisor antes de la sinapsis e hiperpolarización después.')],
 'colinergicos|Neurotransmisión y sistema nervioso autónomo': [
    ('sna-vias.svg', '<b>Vías del sistema nervioso autónomo</b> con su neurotransmisor y receptor en cada sinapsis.'),
    ('sinapsis-colinergica.svg', '<b>Sinapsis colinérgica.</b> Síntesis por ChAT, liberación dependiente de Ca²⁺, degradación por acetilcolinesterasa y dónde actúa cada fármaco.')],
 'adrenergicos|Catecolaminas: síntesis y metabolismo': [('catecolaminas.svg', '<b>Síntesis y fin de la acción de la noradrenalina:</b> recaptación (NET), MAO y COMT.')],
 'adrenergicos|Receptores adrenérgicos': [('receptores-adrenergicos.svg', '<b>Receptores adrenérgicos</b> con su proteína G, su efecto principal y un agonista y un antagonista de ejemplo.')],
}
FII = {
 'atb': [('sitios-antibioticos.svg', '<b>Dianas de los antibióticos</b> en la bacteria: pared, membrana, ácidos nucleicos, ribosoma (30S y 50S) y folato.'),
         ('folato.svg', '<b>Bloqueo secuencial del folato:</b> sulfonamidas y trimetoprim actúan en dos pasos seguidos de la misma vía.')],
 'tb': [('tuberculosis.svg', '<b>Esquema de 6 meses</b> (fase intensiva y de continuación) y dónde actúa cada fármaco de primera línea, con su RAM típica.')],
 'hongos': [('antimicoticos.svg', '<b>Dianas de los antimicóticos:</b> síntesis de ergosterol, ergosterol de la membrana, glucano de la pared, ácidos nucleicos y mitosis.')],
 'virus': [('ciclo-vih.svg', '<b>Ciclo del VIH</b> y la etapa que bloquea cada familia de antirretrovirales.'),
           ('influenza-herpes.svg', '<b>Influenza y herpes.</b> M2, endonucleasa y neuraminidasa en influenza; activación del aciclovir por la timidina cinasa viral.')],
 'par': [('antiparasitarios.svg', '<b>Antiparasitarios según la ubicación:</b> amebicidas luminales vs tisulares y fase del Plasmodium que ataca cada antipalúdico.')],
 'park': [('parkinson.svg', '<b>Fármacos antiparkinsonianos:</b> más levodopa al cerebro (carbidopa, entacapona), menos degradación (MAO-B), agonistas D₂ y antimuscarínicos.')],
 'dm': [('celula-beta.svg', '<b>Secreción de insulina en la célula β:</b> sulfonilureas y glinidas cierran el canal de K⁺-ATP; las incretinas la potencian solo si hay glucosa.'),
        ('hipoglucemiantes.svg', '<b>Dónde actúa cada familia</b> de hipoglucemiantes orales e inyectables no insulínicos.')],
 'tir': [('tiroides.svg', '<b>Síntesis de T4 y T3</b> (NIS, TPO, tiroglobulina) y el paso que bloquea cada antitiroideo.')],
 'ans': [('gaba-a.svg', '<b>Receptor GABA-A.</b> BZD e hipnóticos Z aumentan la frecuencia de apertura; los barbitúricos, la duración.')],
}

def uri(path):
    s = open(path).read().replace('"', "'")
    return 'data:image/svg+xml,' + quote(s, safe="=:/,;.-_'()")

def fig(gid, fname, cap):
    alt = re.sub('<[^>]+>', '', cap)
    return (f'<figure class="fxf"><button type="button" class="fxz" aria-label="Ampliar esquema">'
            f'<img src="{uri(os.path.join(HERE, "img", gid, fname))}" alt="{alt}" loading="lazy" decoding="async"></button>'
            f'<figcaption>{cap}<small>{CRED}</small></figcaption></figure>')

CSS = ('.fxs{display:grid;gap:14px;margin:16px 0 6px}'
       '.fxf{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden}'
       '.fxz{display:block;width:100%;padding:0;margin:0;border:0;background:#fff;cursor:zoom-in;position:relative}'
       '.fxz img{display:block;width:100%;height:auto}'
       '.fxz::after{content:"⤢ Ampliar";position:absolute;right:8px;bottom:8px;font:600 .72rem/1 system-ui,sans-serif;color:#fff;background:rgba(0,0,0,.55);border-radius:999px;padding:5px 9px}'
       '.fxf figcaption{padding:10px 13px 12px;font-size:.9rem;line-height:1.45}'
       '.fxf figcaption small{display:block;margin-top:5px;color:var(--muted);font-size:.74rem}'
       '.fxl{position:fixed;inset:0;z-index:999;background:rgba(10,14,13,.94);overflow:auto;display:flex;flex-direction:column;'
       'padding:max(10px,env(safe-area-inset-top,0px)) 10px max(10px,env(safe-area-inset-bottom,0px))}'
       '.fxl .fxb{display:flex;gap:8px;justify-content:flex-end;padding-bottom:8px;position:sticky;top:0}'
       '.fxl button{font:600 .85rem system-ui,sans-serif;color:#fff;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:7px 13px;cursor:pointer}'
       '.fxl .fxi{flex:1;display:grid;place-items:center;overflow:auto}'
       '.fxl img{background:#fff;border-radius:8px;width:min(100%,1400px);height:auto}'
       '.fxl.big img{width:min(2400px,240vw);max-width:none}'
       '.fxl p{color:#e9efec;max-width:860px;margin:10px auto 0;font:.9rem/1.45 system-ui,sans-serif}.fxl p small{display:block;opacity:.7;margin-top:4px}')
JS = ('(function(){var L=null,from=null;function close(){if(!L)return;L.remove();L=null;document.body.style.overflow="";if(from)from.focus({preventScroll:true})}'
      'document.addEventListener("click",function(e){var z=e.target.closest(".fxz");if(z&&!L){from=z;var f=z.closest(".fxf");L=document.createElement("div");L.className="fxl";'
      'L.setAttribute("role","dialog");L.setAttribute("aria-modal","true");L.setAttribute("aria-label","Esquema ampliado");'
      'L.innerHTML=\'<div class="fxb"><button type="button" data-zz>Acercar</button><button type="button" data-x aria-label="Cerrar">✕ Cerrar</button></div><div class="fxi"></div><p></p>\';'
      'var im=f.querySelector("img").cloneNode();im.removeAttribute("loading");L.querySelector(".fxi").appendChild(im);'
      'L.querySelector("p").innerHTML=f.querySelector("figcaption").innerHTML;document.body.appendChild(L);document.body.style.overflow="hidden";L.querySelector("[data-x]").focus();return}'
      'if(!L)return;if(e.target.closest("[data-x]"))return close();if(e.target.closest("[data-zz]")){var b=L.classList.toggle("big");e.target.textContent=b?"Alejar":"Acercar";return}'
      'if(e.target===L||e.target.classList.contains("fxi"))close()});'
      'document.addEventListener("keydown",function(e){if(L&&e.key==="Escape")close()})})();')

def patch(path, gid, figs, hook_old, hook_new, wrap):
    if not os.path.exists(path):
        print('no existe', path); return
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<!--fx-->.*?<!--/fx-->', '', s, flags=re.S)
    data = {k: wrap(''.join(fig(gid, f, c) for f, c in v)) for k, v in figs.items()}
    block = ('<!--fx--><style>' + CSS + '</style><script>self.FXF=' + json.dumps(data, ensure_ascii=False)
             + ';' + JS + '</script><!--/fx-->')
    i = s.index('<script>')                    # primer script en línea = el de la guía
    s = s[:i] + block + s[i:]
    if hook_new not in s:
        assert s.count(hook_old) == 1, (path, hook_old)
        s = s.replace(hook_old, hook_new)
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', path, sum(len(v) for v in figs.values()), 'esquemas')

patch(os.path.join(SITE, 's3', 'farmacologia', 'index.html'), 'farmacologia', BASICA,
      '<div class="sec-body">${b}</div>',
      '<div class="sec-body">${b}${(self.FXF&&FXF[u.id+"|"+h])||""}</div>',
      lambda h: '<div class="fxs">' + h + '</div>')
patch(os.path.join(SITE, 's4', 'apps', 'farmacologia-ii.html'), 'farmacologia-ii', FII,
      'if(t.extra) h+=',
      'if(self.FXF&&FXF[t.id]) h+=`<section class="group" style="--tc:var(${t.color})"><h3>Esquemas</h3>${FXF[t.id]}</section>`;if(t.extra) h+=',
      lambda h: '<div class="fxs">' + h + '</div>')
