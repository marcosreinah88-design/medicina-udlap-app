"""Agrega el «Simulador de casos clínicos de Gastro» al Material extra de 5º.

Uso:
  python3 tools-extra/patch_simulador_casos.py <carpeta del original> <carpeta del sitio> [--artefacto]

- <carpeta del original>: index.html y casos.json del artefacto tal cual
  (claude.ai/artifact/BU7D323awy9cYsXa3FvGAw). 68 casos de los tres bloques de Gastro
  (esófago y estómago, intestino, hígado/vía biliar/páncreas/onco): estudios, diagnóstico,
  tratamiento y evolución, cada paso calificado y explicado con el artículo del curso.
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
shutil.copy(os.path.join(src, "casos.json"), os.path.join(dstdir, "casos.json"))
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
DESC = (f"{nc} casos clínicos de los tres bloques de Gastro: recibes al paciente con su monitor, pides estudios, "
        "haces el diagnóstico y decides el tratamiento y la evolución. Cada paso se califica y se explica con el "
        "artículo del curso: ERGE, acalasia, Barrett, úlcera y H. pylori, sangrados, diarreas, celiaquía, Crohn, CUCI, "
        "Roma V, hepatitis, cirrosis y Baveno VIII, litiasis, colangitis, pancreatitis y oncología digestiva.")
TAGS = ("simulador casos clinicos guardia paciente estudios diagnostico tratamiento evolucion gastro esofago estomago "
        "erge acalasia barrett ulcera pylori dispepsia gastroparesia stda stdb intestino diarrea celiaca crohn cuci "
        "roma estrenimiento ciclosporiasis higado hepatitis autoinmune cbp masld cirrosis baveno litiasis colangitis "
        "tokio pancreatitis oncologia")
s5p = os.path.join(site, "s5", "index.html")
s = open(s5p, encoding="utf-8").read()
if f'id:"{ID}"' not in s:
    entry = (f',\n  {{id:"{ID}",title:"{TITLE}",desc:"{DESC}",'
             f'stats:[["{nc}","casos"],["{npasos}","decisiones"],["{nt}","temas"]],tags:"{TAGS}"}}')
    m = re.search(rf'\{{id:"{AFTER}"[^\n]*\}}', s)
    assert m, "no encontré la entrada anterior en EXTRA"
    s = s[:m.end()] + entry + s[m.end():]
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
