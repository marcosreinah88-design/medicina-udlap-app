# Agrega «Casos clínicos» a las características (feat) de las guías de 5º en el hub, para que se vea en su tarjeta
# y el buscador de la portada las encuentre con «casos clínicos». Idempotente.
# Uso: python3 tools-casos/patch_hub.py [archivo.html ...]   (por omisión site/index.html y site/app.html; sirve para la copia del artefacto)
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FILES = sys.argv[1:] or [os.path.join(HERE, '..', 'site', f) for f in ('index.html', 'app.html')]
IDS = ['gastro', 'esofago', 'hepatobiliar', 'cirugia', 'imagenologia', 'oftalmo', 'otorrino', 'psiquiatria']
for f in FILES:
    s = open(f, encoding='utf-8').read(); n = 0
    for g in IDS:
        m = re.search(r'\{id:"' + g + r'",sem:5,', s)
        if not m: print('  no está', g, 'en', os.path.basename(f)); continue
        fm = re.compile(r'feat:\[([^\]]*)\]').search(s, m.end())
        if not fm or fm.start() - m.end() > 1500: print('  sin feat', g); continue
        if '"Casos clínicos"' in fm.group(1): continue
        s = s[:fm.start()] + 'feat:["Casos clínicos"' + (',' + fm.group(1) if fm.group(1).strip() else '') + ']' + s[fm.end():]; n += 1
    open(f, 'w', encoding='utf-8').write(s)
    print(os.path.basename(f), n, 'guías')
