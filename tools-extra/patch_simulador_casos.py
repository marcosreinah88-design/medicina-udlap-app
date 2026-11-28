"""Agrega el «Simulador de casos clínicos de Gastro» al Material extra de 5º.

Uso:
  python3 tools-extra/patch_simulador_casos.py <carpeta del original> <carpeta del sitio> [--artefacto]

- <carpeta del original>: index.html y casos.json del artefacto tal cual
  (claude.ai/artifact/BU7D323awy9cYsXa3FvGAw). 68 casos de los tres bloques de Gastro
  (esófago y estómago, intestino, hígado/vía biliar/páncreas/onco): estudios, diagnóstico,
  tratamiento y evolución, cada paso calificado y explicado con el artículo del curso.
  El diagnóstico (tema) queda oculto hasta revelarlo (ver «diagnóstico oculto» abajo).
  Los casos se pasan a formato lineal (una sola respuesta correcta por paso) con
  tools-extra/simulador_lineal.py.
  Son casos por pasos (cada pregunta depende de la historia del paciente), así que no se
  agregan a tools-estudio/banco.js.
- Escribe <sitio>/s5/simulador-casos-gastro/{index.html,casos.json}. En el repo las fuentes
  de Google se pasan a locales con fonts.py; con --artefacto se deja el link de Google Fonts.
- Lo agrega a EXTRA de <sitio>/s5/index.html y, en el hub (<sitio>/index.html y app.html si
  existe), a la lista de guías, al buscador (FT) y a Otros materiales (MAT), después de los
  simulacros del Bloque III. Idempotente.
Después: firmar (tools-subrayar/firmar.py).
"""
import sys, os, re, html, json, shutil, subprocess, tempfile, unicodedata

ID = "simulador-casos-gastro"
AFTER = "simulacros-bloque-iii"
TITLE = "Simulador de casos clínicos de Gastro"
here = os.path.dirname(os.path.abspath(__file__))

src, site = sys.argv[1], sys.argv[2]
artefacto = "--artefacto" in sys.argv[3:]
page = open(os.path.join(src, "index.html"), encoding="utf-8").read()
casos = json.load(open(os.path.join(src, "casos.json"), encoding="utf-8"))
assert "fetch('casos.json')" in page

# ---- diagnóstico oculto (pedido del usuario, 28 nov 2026) ----
# El tema del caso es el diagnóstico: en la ficha del paciente sale un botón «Revelar diagnóstico»
# y se muestra solo al tocarlo, al calificar el paso de diagnóstico o al terminar el caso. En el
# censo sale «Diagnóstico oculto» hasta que el caso ya se atendió (o si se filtró por ese tema).
# Títulos que decían la respuesta se cambian por el motivo de consulta.
TITULOS = {
    "acal2": "Disfagia que avanzó demasiado rápido",
    "cuci4": "CUCI con fosfatasa alcalina alta",
    "pan3": "Dolor a la espalda, fiebre e ictericia",
    "col2": "Confundido, con fiebre e ictericia",
}
for c in casos:
    if c["id"] in TITULOS:
        c["t"] = TITULOS[c["id"]]
assert sum(c["id"] in TITULOS for c in casos) == len(TITULOS)

REV = [
    (".opt.lock{cursor:default}",
     ".opt.lock{cursor:default}\n"
     ".rev{border:1.5px dashed var(--line);background:var(--soft);color:var(--mute);border-radius:99px;"
     "padding:3px 12px;font-size:14px;font-weight:600;min-height:32px}.rev:hover{border-color:var(--scrub2);color:var(--ink)}"
     ".dxv{color:var(--mute);font-weight:500}"),
    ('<span class="tm"><span>${esc(c.tema)}</span>',
     '<span class="tm"><span>${s != null || S.f.tema !== \'all\' ? esc(c.tema) : \'Diagnóstico oculto\'}</span>'),
    ('<span style="color:var(--mute);font-weight:500">${esc(c.tema)}</span>',
     '${dxShown(c) ? `<span class="dxv">${esc(c.tema)}</span>` : `<button class="rev" id="rev" data-rev>Revelar diagnóstico</button>`}'),
    ("  monitor(document.getElementById('cm'), c.sv.fc);\n  bindStep(c);",
     "  monitor(document.getElementById('cm'), c.sv.fc);\n"
     "  const rv = document.getElementById('rev');\n"
     "  if (rv) rv.onclick = () => { S.cur.rev = true; rv.outerHTML = `<span class=\"dxv\">${esc(c.tema)}</span>`; };\n"
     "  bindStep(c);"),
    ("function stepBox(c) {",
     "function dxShown(c) {\n"
     "  const cur = S.cur, k = c.pasos.findIndex(p => p.f === 'dx');\n"
     "  return cur.rev || S.f.tema !== 'all' || cur.step >= c.pasos.length || (k >= 0 && (k < cur.step || (k === cur.step && cur.done)));\n"
     "}\n\nfunction stepBox(c) {"),
]
for a, b in REV:
    assert page.count(a) == 1, a
    page = page.replace(a, b)

# ---- casos lineales (pedido del usuario, 28 nov 2026): una sola respuesta correcta por paso ----
sys.path.insert(0, here)
import simulador_lineal
casos = simulador_lineal.linealizar(casos)
# ---- casos nuevos (pedido del usuario, 28 nov 2026: «agrega más casos, muchos más») ----
# Cada tanda en casos_nuevos/tandaN.py ya viene lineal: una sola respuesta correcta por paso.
import glob, importlib.util
sys.path.insert(0, os.path.join(here, "casos_nuevos"))
for fn in sorted(glob.glob(os.path.join(here, "casos_nuevos", "tanda*.py")), key=lambda f: int(re.sub(r"\D", "", os.path.basename(f)))):
    spec = importlib.util.spec_from_file_location(os.path.basename(fn)[:-3], fn)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    casos += mod.CASOS
ids = [c["id"] for c in casos]
assert len(ids) == len(set(ids)), "ids repetidos"
for c in casos:
    assert c["b"] in ("ee", "int", "hbp") and c["dif"] in (1, 2, 3), c["id"]
    for st in c["pasos"]:
        assert st["f"] in ("est", "dx", "tx", "evo"), c["id"]
        assert sum(o[1] for o in st["o"]) == 1 and len(st["o"]) >= 3, (c["id"], st["q"])
        assert len({o[0] for o in st["o"]}) == len(st["o"]), (c["id"], st["q"])
page = simulador_lineal.motor(page)
page, casos = simulador_lineal.monitor(page, casos)  # signos y ECG acordes a cada paciente

# ---- página ----
dstdir = os.path.join(site, "s5", ID)
os.makedirs(dstdir, exist_ok=True)
if not artefacto:
    # fonts.py localiza las fuentes de Google (las deja en <sitio>/fonts y cambia el link)
    tmp = tempfile.mkdtemp()
    os.makedirs(os.path.join(tmp, "s5", ID))
    shutil.copytree(os.path.join(site, "fonts"), os.path.join(tmp, "fonts"))
    open(os.path.join(tmp, "s5", ID, "index.html"), "w", encoding="utf-8").write(page)
    subprocess.run([sys.executable, os.path.join(here, "..", "fonts.py"), tmp], check=True)
    page = open(os.path.join(tmp, "s5", ID, "index.html"), encoding="utf-8").read()
    assert "fonts.googleapis" not in page
    for f in os.listdir(os.path.join(tmp, "fonts")):
        if not os.path.exists(os.path.join(site, "fonts", f)):
            shutil.copy(os.path.join(tmp, "fonts", f), os.path.join(site, "fonts", f))
    shutil.rmtree(tmp)
open(os.path.join(dstdir, "index.html"), "w", encoding="utf-8").write(page)
json.dump(casos, open(os.path.join(dstdir, "casos.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
nc = len(casos)
npasos = sum(len(c["pasos"]) for c in casos)
nt = len({c["tema"] for c in casos})
print("escribí", dstdir, "·", nc, "casos,", npasos, "pasos,", nt, "temas")


def fold(s):
    s = unicodedata.normalize("NFD", html.unescape(s))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


text = " ".join(strings(casos)) + " simulador casos clinicos guardia gastroenterologia"
words = " ".join(sorted(set(re.findall(r"[a-z]{4,}", fold(text)))))

# ---- estante de 5º: Material extra ----
DESC = (f"{nc} casos clínicos de los tres bloques de Gastro, lineales como un diagrama de flujo: en cada paso "
        "eliges una sola opción (estudio, diagnóstico, tratamiento, evolución), ves el resultado y lo que no va se "
        "descarta con su explicación del artículo del curso: ERGE, acalasia, Barrett, úlcera y H. pylori, sangrados, diarreas, celiaquía, Crohn, CUCI, "
        "Roma V, hepatitis, cirrosis y Baveno VIII, litiasis, colangitis, pancreatitis y oncología digestiva.")
TAGS = ("simulador casos clinicos guardia paciente estudios diagnostico tratamiento evolucion gastro esofago estomago "
        "erge acalasia barrett ulcera pylori dispepsia gastroparesia stda stdb intestino diarrea celiaca crohn cuci "
        "roma estrenimiento ciclosporiasis higado hepatitis autoinmune cbp masld cirrosis baveno litiasis colangitis "
        "tokio pancreatitis oncologia")
s5p = os.path.join(site, "s5", "index.html")
s = open(s5p, encoding="utf-8").read()
entry = (f'{{id:"{ID}",title:"{TITLE}",desc:"{DESC}",'
         f'stats:[["{nc}","casos"],["{npasos}","pasos"],["{nt}","temas"]],tags:"{TAGS}"}}')
if f'id:"{ID}"' in s:  # ya estaba: se actualiza la descripción
    s = re.sub(rf'\{{id:"{ID}",title:[^\n]*\}}', lambda m: entry, s)
else:
    m = re.search(rf'\{{id:"{AFTER}"[^\n]*\}}', s)
    assert m, "no encontré la entrada anterior en EXTRA"
    s = s[:m.end()] + ",\n  " + entry + s[m.end():]
open(s5p, "w", encoding="utf-8").write(s)
print("EXTRA de 5º:", s5p)

# ---- hub: lista de guías, buscador y Otros materiales ----
G = f' {{id:"{ID}",sem:5,color:"#0f4a3f",area:"Gastroenterología",title:"{TITLE}",temas:{nt},stats:[],feat:[],toc:[]}}'
MAT = f'    {{id:"{ID}",title:"{TITLE}",kind:"artifact",subject:"Gastroenterología",fromSem:5,src:"s5/{ID}/index.html"}},'
for name in ("index.html", "app.html"):
    p = os.path.join(site, name)
    if not os.path.exists(p):
        continue
    h = open(p, encoding="utf-8").read()
    if f'{{id:"{ID}",sem:5' not in h:
        m = re.search(rf'\{{id:"{AFTER}",sem:5[^\n]*\}}', h)
        h = h[:m.end()] + ",\n" + G + h[m.end():]
    if f'"{ID}": "' not in h:
        m = re.search(rf'"{AFTER}": "[^"]*"', h)
        h = h[:m.end()] + f', "{ID}": "{words}"' + h[m.end():]
    else:
        h = re.sub(rf'"{ID}": "[^"]*"', f'"{ID}": "{words}"', h)
    if f'{{id:"{ID}",title:' not in h:
        m = re.search(rf'\n    \{{id:"{AFTER}",title:[^\n]*\n', h)
        h = h[:m.end()] + MAT + "\n" + h[m.end():]
    open(p, "w", encoding="utf-8").write(h)
    print("hub:", p)
