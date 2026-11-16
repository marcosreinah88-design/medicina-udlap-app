"""Mete las imágenes de referencia y los esquemas propios en la guía de Gastroenterología (5º)
y en Hepatobiliar (que comparte los temas del Bloque III).

Uso: python3 tools-gastro/patch.py [ruta/a/index.html ...]
     sin argumentos: site/s5/gastro/index.html y site/s5/hepatobiliar/index.html
Idempotente: quita las figuras marcadas con data-gx y las vuelve a poner desde imagenes.tsv.
Las fotos se copian a s5/gastro/img/ref/ (Hepatobiliar las toma de ../gastro/img/ref/).
Sirve igual para la copia del artefacto (misma estructura s5/gastro y s5/hepatobiliar).
"""
import sys, os, re, json, shutil
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from esquemas import ESQ  # noqa: E402

SITE = os.path.join(HERE, '..', 'site')
dsts = sys.argv[1:] or [os.path.join(SITE, 's5', 'gastro', 'index.html'), os.path.join(SITE, 's5', 'hepatobiliar', 'index.html')]

rows = []
for line in open(os.path.join(HERE, 'imagenes.tsv'), encoding='utf-8'):
    if not line.strip() or line.startswith('#'):
        continue
    rows.append(line.rstrip('\n').split('\t'))

CSS = ('.fig .gx-cred{display:block;margin-top:3px;font-size:11.5px;line-height:1.35;color:var(--mut);opacity:.85}'
       '.fig[data-gx] .fx{max-width:580px}/*gx*/')
LBCSS = ('.fig .fig-img{display:block;width:100%;padding:8px;border:0;border-radius:8px;background:#fff;cursor:zoom-in}'
         '.fig .fig-img img{display:block;width:100%;height:auto;max-height:560px;object-fit:contain}.fig-hint{font-style:italic}'
         '.lb{position:fixed;inset:0;z-index:100;background:rgba(5,12,15,.92);overflow:auto;display:flex;flex-direction:column;align-items:center;padding:56px 12px 24px}'
         '.lb img{background:#fff;border-radius:6px;max-width:100%;height:auto;cursor:zoom-in}.lb.big img{max-width:none;width:auto;cursor:zoom-out}'
         '.lb-x{position:fixed;top:10px;right:12px;border:0;border-radius:99px;background:#fff;color:#111;padding:8px 14px;font-weight:700;cursor:pointer}'
         '.lb p{color:#dfe8eb;font-size:14px;margin:8px 0 0;max-width:70ch;text-align:center}/*gx-lb*/')
LBJS = '''<script>/*gx-lb*/(function(){var lb=null;function c(){if(lb){lb.remove();lb=null;document.body.style.overflow='';}}
document.addEventListener('click',function(e){var b=e.target.closest('[data-zoom]');if(b){var cap=b.parentNode.querySelector('figcaption');lb=document.createElement('div');lb.className='lb';lb.setAttribute('role','dialog');lb.innerHTML='<button class="lb-x" type="button">Cerrar ✕</button><img src="'+b.getAttribute('data-zoom')+'" alt="">'+(cap?'<p>'+cap.innerHTML.replace(/<span class="fig-hint">.*?<\\/span>/,'')+'</p>':'');document.body.appendChild(lb);document.body.style.overflow='hidden';return;}
if(lb&&e.target.closest('.lb')){if(e.target.tagName==='IMG')lb.classList.toggle('big');else if(e.target.closest('.lb-x')||e.target===lb)c();}});
document.addEventListener('keydown',function(e){if(e.key==='Escape')c();});window.addEventListener('hashchange',c);})();</script>'''

FIGRE = re.compile(r'\n?<figure class="fig" data-gx="[^"]*">.*?</figure>', re.S)


def fig(name, cap, cred, pre):
    cred_h = f'<small class="gx-cred">{escape(cred)}</small>'
    if name in ESQ:
        svg, _ = ESQ[name]
        return (f'\n<figure class="fig" data-gx="{name}">{svg}<figcaption>{escape(cap)}{cred_h}</figcaption></figure>')
    src = pre + name
    from PIL import Image
    w, h = Image.open(os.path.join(HERE, 'img', name)).size
    return (f'\n<figure class="fig" data-gx="{name}"><button type="button" class="fig-img" data-zoom="{src}" aria-label="Ampliar imagen">'
            f'<img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{escape(cap)}"></button>'
            f'<figcaption>{escape(cap)} <span class="fig-hint">Toca para ampliar.</span>{cred_h}</figcaption></figure>')


for dst in dsts:
    dst = os.path.abspath(dst)
    hepato = os.path.basename(os.path.dirname(dst)) == 'hepatobiliar'
    pre = '../gastro/img/ref/' if hepato else 'img/ref/'
    gdir = os.path.join(os.path.dirname(os.path.dirname(dst)), 'gastro', 'img', 'ref')
    os.makedirs(gdir, exist_ok=True)
    s = open(dst, encoding='utf-8').read()
    i = s.index('window.RB=') + len('window.RB=')
    D, e = json.JSONDecoder().raw_decode(s, i)
    T = {t['id']: t for t in D['topics']}
    for t in D['topics']:
        for x in t['secs']:
            x['h'] = FIGRE.sub('', x['h'])
    n = 0
    for tema, apartado, name, cap, cred in rows:
        if tema not in T:
            continue
        sec = [x for x in T[tema]['secs'] if x['t'] == apartado]
        if not sec:
            sys.exit(f'No encontré «{apartado}» en {tema}')
        sec[0]['h'] += fig(name, cap, cred, pre)
        if name not in ESQ:
            shutil.copy(os.path.join(HERE, 'img', name), os.path.join(gdir, name))
        n += 1
    js = json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    s = s[:i] + js + s[e:]
    k = s.index('</style>')
    if '/*gx*/' not in s:
        s = s[:k] + CSS + s[k:]
        k = s.index('</style>')
    if hepato and '/*gx-lb*/' not in s:
        s = s[:k] + LBCSS + s[k:]
        j = s.rindex('</body>')
        s = s[:j] + LBJS + s[j:]
    open(dst, 'w', encoding='utf-8').write(s)
    print(f'{n} figuras en {dst}')
