"""Mete las imágenes de referencia (con pie y crédito) en la guía de Imagenología (5º).
Uso: python3 tools-imagenologia/patch.py [ruta a imagenologia/index.html]   (por defecto site/s5/imagenologia/index.html)
Idempotente: quita las entradas con crédito (3 elementos) y las vuelve a poner desde imagenes.tsv.
Las imágenes del apunte (2 elementos) no se tocan."""
import sys, os, json, base64
HERE = os.path.dirname(os.path.abspath(__file__))
dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'site', 's5', 'imagenologia', 'index.html')
s = open(dst, encoding='utf-8').read()

i = s.index('const IMG=') + len('const IMG=')
IMG, e = json.JSONDecoder().raw_decode(s, i)
for k in list(IMG):
    IMG[k] = [x for x in IMG[k] if len(x) == 2]
    if not IMG[k]: del IMG[k]
mime = {'webp': 'image/webp', 'svg': 'image/svg+xml', 'png': 'image/png', 'jpg': 'image/jpeg'}
n = 0
for line in open(os.path.join(HERE, 'imagenes.tsv'), encoding='utf-8'):
    if not line.strip() or line.startswith('#'): continue
    tema, f, cap, cred = line.rstrip('\n').split('\t')
    data = open(os.path.join(HERE, 'img', f), 'rb').read()
    uri = f"data:{mime[f.rsplit('.',1)[1]]};base64," + base64.b64encode(data).decode()
    IMG.setdefault(tema, []).append([uri, cap, cred])
    n += 1
s = s[:i] + json.dumps(IMG, ensure_ascii=False, separators=(',', ':')) + s[e:]

# Galería: separa las del apunte de las de referencia (con crédito)
OLD = '''${L?`<h4>Imágenes del apunte (${L.length})</h4><div class="gal">${L.map((x,i)=>`<button class="fig" data-lb="${t.id}" data-i="${i}"><span class="ph"><i>${String(i+1).padStart(2,"0")}</i><img loading="lazy" src="${x[0]}" alt="${x[1].replace(/"/g,"&quot;")}"></span><span class="cap">${hl(x[1],q)}</span></button>`).join("")}</div>`:""}'''
NEW = '''${L?[["Imágenes del apunte",L.map((x,i)=>[x,i]).filter(z=>!z[0][2])],["Imágenes de referencia",L.map((x,i)=>[x,i]).filter(z=>z[0][2])]].filter(g=>g[1].length).map(([h,G])=>`<h4>${h} (${G.length})</h4><div class="gal">${G.map(([x,i],k)=>`<button class="fig" data-lb="${t.id}" data-i="${i}"><span class="ph"><i>${String(k+1).padStart(2,"0")}</i><img loading="lazy" src="${x[0]}" alt="${x[1].replace(/"/g,"&quot;")}"></span><span class="cap">${hl(x[1],q)}${x[2]?`<small class="cred">${x[2]}</small>`:""}</span></button>`).join("")}</div>`).join(""):""}'''
if OLD in s:
    s = s.replace(OLD, NEW)
elif NEW not in s:
    sys.exit('No encontré la galería')
OLDL = '$("#lbC").textContent=x[1];'
NEWL = '$("#lbC").textContent=x[1]+(x[2]?" · "+x[2]:"");'
if OLDL in s: s = s.replace(OLDL, NEWL)
CSS = '.cap .cred{display:block;margin-top:3px;font-size:10.5px;line-height:1.3;color:var(--muted);font-weight:400}/*img-ref*/'
if '/*img-ref*/' not in s:
    k = s.index('</style>')
    s = s[:k] + CSS + '\n' + s[k:]
open(dst, 'w', encoding='utf-8').write(s)
print(f'{n} imágenes de referencia en {dst}')
