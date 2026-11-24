"""Agrega «Exámenes por artículo del Bloque III» (Gastro, 3er parcial) al Material extra de 5º.

Uso:
  python3 tools-extra/patch_examen_articulos.py <examenes.html> <carpeta del sitio> [--artefacto]

- <examenes.html>: el artefacto original tal cual (claude.ai/artifact/JdigMESSa1SVLhkZsgdT6n).
  Un examen por cada uno de los 12 artículos troncales, con preguntas distintas a las del
  «Examen de práctica del Bloque III» (s5/examen-bloque-iii).
- Escribe <sitio>/s5/examenes-por-articulo/index.html. En el repo las fuentes van locales
  (../../fonts/gaa65f3420f.css, las mismas del examen del Bloque III); con --artefacto se deja
  el link de Google Fonts, como las demás guías de la copia del artefacto.
- Lo agrega a EXTRA de <sitio>/s5/index.html (Material extra del estante de 5º) y, en el hub
  (<sitio>/index.html y <sitio>/app.html si existe), a la lista de guías, al buscador (FT) y a
  Otros materiales (MAT), justo después del examen del Bloque III. Idempotente.
Después: node tools-estudio/banco.js y firmar (tools-subrayar/firmar.py).
"""
import sys, os, re, html, unicodedata

ID = "examenes-por-articulo"
AFTER = "examen-bloque-iii"
TITLE = "Exámenes por artículo del Bloque III"
FONT_LOCAL = '<link rel="stylesheet" href="../../fonts/gaa65f3420f.css">'

src, site = sys.argv[1], sys.argv[2]
artefacto = "--artefacto" in sys.argv[3:]
page = open(src, encoding="utf-8").read()

# ---- página ----
if not artefacto:
    page = re.sub(r'<link rel="preconnect"[^>]*>\n?', "", page)
    page, n = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]*">', FONT_LOCAL, page)
    assert n == 1, "no encontré el link de Google Fonts"
dst = os.path.join(site, "s5", ID, "index.html")
os.makedirs(os.path.dirname(dst), exist_ok=True)
open(dst, "w", encoding="utf-8").write(page)
print("escribí", dst)

blk = next(b for b in re.findall(r"<script>([\s\S]*?)</script>", page) if "const PREGUNTAS" in b)
nq = len(re.findall(r"^\{ q: ", blk, re.M))
nt = len(re.findall(r'^\s+"\d\d": "', blk.split("const FUENTES")[0].split("const TEMAS")[1], re.M))
print(nq, "preguntas,", nt, "artículos")


def fold(s):
    s = unicodedata.normalize("NFD", html.unescape(s))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


head = re.search(r'<header class="report">([\s\S]*?)</header>', page).group(1)
text = " ".join(re.findall(r'"((?:[^"\\]|\\.)*)"', blk)) + " " + re.sub(r"<[^>]+>", " ", head)
words = " ".join(sorted(set(re.findall(r"[a-z]{4,}", fold(text)))))

# ---- estante de 5º: Material extra ----
DESC = ("Un examen por cada uno de los 12 artículos troncales del 3er parcial, con preguntas nuevas que no repiten "
        "las del examen de práctica: pruebas hepáticas, hepatitis virales y autoinmune, CBP, MASLD, cirrosis, "
        "Baveno VIII, litiasis, colangitis (Tokio 2018), pancreatitis y oncología digestiva. Cada explicación cita "
        "el artículo. Simulacro mixto de 40, juego Contrarreloj y Pomodoro.")
TAGS = ("examen examenes articulo articulos parcial bloque iii simulacro fisiopatologia higado hepatico biliar pfh "
        "kwo hepatitis virales autoinmune cbp masld cirrosis baveno portal litiasis colangitis tokio pancreatitis "
        "cancer oncologia contrarreloj pomodoro")
s5p = os.path.join(site, "s5", "index.html")
s = open(s5p, encoding="utf-8").read()
if f'id:"{ID}"' not in s:
    entry = (f',\n  {{id:"{ID}",title:"{TITLE}",desc:"{DESC}",'
             f'stats:[["{nq}","preguntas"],["{nt}","artículos"],["40","simulacro"]],tags:"{TAGS}"}}')
    m = re.search(rf'\{{id:"{AFTER}"[^\n]*\}}', s)
    s = s[:m.end()] + entry + s[m.end():]
    open(s5p, "w", encoding="utf-8").write(s)
    print("EXTRA de 5º:", s5p)

# ---- hub: lista de guías, buscador y Otros materiales ----
G = f' {{id:"{ID}",sem:5,color:"#2c6a4c",area:"Gastroenterología",title:"{TITLE}",temas:{nt},stats:[],feat:[],toc:[]}}'
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
