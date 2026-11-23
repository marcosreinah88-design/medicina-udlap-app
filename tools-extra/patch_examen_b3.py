"""Agrega el «Examen de práctica del Bloque III» (Gastro, 3er parcial) al Material extra de 5º.

Uso:
  python3 tools-extra/patch_examen_b3.py <examen.html> <carpeta del sitio> [--artefacto]

- <examen.html>: el artefacto original tal cual (claude.ai/artifact/Gb9ShPxBwujrQ9SxSmAKuK).
- Escribe <sitio>/s5/examen-bloque-iii/index.html. En el repo las fuentes van locales
  (../../fonts/gaa65f3420f.css, las mismas del Quiz de pruebas hepáticas); con --artefacto
  se deja el link de Google Fonts, como las demás guías de la copia del artefacto.
- Lo agrega a EXTRA de <sitio>/s5/index.html (Material extra del estante de 5º) y, en el
  hub (<sitio>/index.html y <sitio>/app.html si existe), a la lista de guías, al buscador
  (FT) y a Otros materiales (MAT). Idempotente.
Después: node tools-estudio/banco.js y firmar (tools-subrayar/firmar.py).
"""
import sys, os, re, html, unicodedata

ID = "examen-bloque-iii"
TITLE = "Examen de práctica del Bloque III"
FONT_LOCAL = '<link rel="stylesheet" href="../../fonts/gaa65f3420f.css">'

src, site = sys.argv[1], sys.argv[2]
artefacto = "--artefacto" in sys.argv[3:]
page = open(src, encoding="utf-8").read()

# ---- página del examen ----
if not artefacto:
    page = re.sub(r'<link rel="preconnect"[^>]*>\n?', "", page)
    page, n = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]*">', FONT_LOCAL, page)
    assert n == 1, "no encontré el link de Google Fonts"
dst = os.path.join(site, "s5", ID, "index.html")
os.makedirs(os.path.dirname(dst), exist_ok=True)
open(dst, "w", encoding="utf-8").write(page)
print("escribí", dst)

# cuántas preguntas y temas (para la tarjeta)
blk = next(b for b in re.findall(r"<script>([\s\S]*?)</script>", page) if "const PREGUNTAS" in b)
nq = len(re.findall(r'(?:\{ t: "|\{"t":")[A-Z]"', blk))
nt = len(re.findall(r'^\s+[A-Z]: "', blk.split("const FUENTES")[0].split("const TEMAS")[1], re.M))
print(nq, "preguntas,", nt, "temas")


def fold(s):
    s = unicodedata.normalize("NFD", html.unescape(s))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


head = re.search(r'<header class="report">([\s\S]*?)</header>', page).group(1)
text = " ".join(re.findall(r'"((?:[^"\\]|\\.)*)"', blk)) + " " + re.sub(r"<[^>]+>", " ", head)
words = " ".join(sorted(set(re.findall(r"[a-z]{4,}", fold(text)))))

# ---- estante de 5º: Material extra ----
DESC = ("Examen de práctica del 3er parcial con los 12 artículos troncales: pruebas hepáticas, hepatitis virales "
        "y autoinmune, CBP, MASLD, cirrosis y Baveno VIII, litiasis, colangitis (Tokio 2018), pancreatitis y "
        "oncología digestiva. Simulacro de 40, preguntas de fisiopatología, juego Contrarreloj y Pomodoro.")
TAGS = ("examen practica parcial bloque iii simulacro fisiopatologia higado hepatico biliar pfh hepatitis "
        "autoinmune cbp masld cirrosis baveno portal litiasis colangitis tokio pancreatitis cancer oncologia "
        "contrarreloj pomodoro")
s5p = os.path.join(site, "s5", "index.html")
s = open(s5p, encoding="utf-8").read()
if f'id:"{ID}"' not in s:
    entry = (f',\n  {{id:"{ID}",title:"{TITLE}",desc:"{DESC}",'
             f'stats:[["{nq}","preguntas"],["{nt}","temas"],["40","simulacro"]],tags:"{TAGS}"}}')
    m = re.search(r'\{id:"quiz-hepatico"[^\n]*\}', s)
    s = s[:m.end()] + entry + s[m.end():]
    open(s5p, "w", encoding="utf-8").write(s)
    print("EXTRA de 5º:", s5p)

# ---- hub: lista de guías, buscador y Otros materiales ----
G = f' {{id:"{ID}",sem:5,color:"#1e6a4e",area:"Gastroenterología",title:"{TITLE}",temas:{nt},stats:[],feat:[],toc:[]}}'
MAT = f'    {{id:"{ID}",title:"{TITLE}",kind:"artifact",subject:"Gastroenterología",fromSem:5,src:"s5/{ID}/index.html"}},'
for name in ("index.html", "app.html"):
    p = os.path.join(site, name)
    if not os.path.exists(p):
        continue
    h = open(p, encoding="utf-8").read()
    if f'{{id:"{ID}",sem:5' not in h:
        m = re.search(r'\{id:"quiz-hepatico",sem:5[^\n]*\}', h)
        h = h[:m.end()] + ",\n" + G + h[m.end():]
    if f'"{ID}": "' not in h:
        m = re.search(r'"quiz-hepatico": "[^"]*"', h)
        h = h[:m.end()] + f', "{ID}": "{words}"' + h[m.end():]
    else:
        h = re.sub(rf'"{ID}": "[^"]*"', f'"{ID}": "{words}"', h)
    if f'{{id:"{ID}",title:' not in h:
        m = re.search(r'\n    \{id:"quiz-hepatico",title:[^\n]*\n', h)
        h = h[:m.end()] + MAT + "\n" + h[m.end():]
    open(p, "w", encoding="utf-8").write(h)
    print("hub:", p)
