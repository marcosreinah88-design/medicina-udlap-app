"""Mete las imágenes de referencia y los esquemas propios en la guía de Oftalmología (5º).

Uso: python3 tools-oftalmo/patch.py [ruta/a/s5/oftalmo/index.html ...]   (sin argumentos: site/s5/oftalmo/index.html)
Idempotente: quita las figuras marcadas con data-ox y las vuelve a poner desde imagenes.tsv.
Las fotos se copian a img/ref/ junto al index.html. Sirve igual para la copia del artefacto
(que solo difiere en la línea de fuentes).
"""
import sys, os, re, shutil
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from esquemas import ESQ  # noqa: E402

SITE = os.path.join(HERE, '..', 'site')
dsts = sys.argv[1:] or [os.path.join(SITE, 's5', 'oftalmo', 'index.html')]

rows = []
for line in open(os.path.join(HERE, 'imagenes.tsv'), encoding='utf-8'):
    if line.strip() and not line.startswith('#'):
        rows.append(line.rstrip('\n').split('\t'))

CSS = ('.fig .ox-cred{display:block;margin-top:3px;font-size:.76rem;line-height:1.35;color:var(--muted);opacity:.9}'
       '.fig .fig-img{display:block;width:100%;padding:8px;border:0;border-radius:8px;background:#fff;cursor:zoom-in}'
       '.fig .fig-img img{display:block;width:100%;height:auto;max-height:560px;object-fit:contain}.fig-hint{font-style:italic}'
       '.ox-lb{position:fixed;inset:0;z-index:100;background:rgba(5,12,15,.92);overflow:auto;display:flex;flex-direction:column;align-items:center;padding:56px 12px 24px}'
       '.ox-lb img{background:#fff;border-radius:6px;max-width:100%;height:auto;cursor:zoom-in}.ox-lb.big img{max-width:none;width:auto;cursor:zoom-out}'
       '.ox-lb-x{position:fixed;top:10px;right:12px;border:0;border-radius:99px;background:#fff;color:#111;padding:8px 14px;font-weight:700;cursor:pointer}'
       '.ox-lb p{color:#dfe8eb;font-size:14px;margin:8px 0 0;max-width:70ch;text-align:center}/*ox*/')
JS = '''<script>/*ox-lb*/(function(){var lb=null;function c(){if(lb){lb.remove();lb=null;document.body.style.overflow='';}}
document.addEventListener('click',function(e){var b=e.target.closest('[data-zoom]');if(b){var cap=b.parentNode.querySelector('figcaption');lb=document.createElement('div');lb.className='ox-lb';lb.setAttribute('role','dialog');lb.innerHTML='<button class="ox-lb-x" type="button">Cerrar ✕</button><img src="'+b.getAttribute('data-zoom')+'" alt="">'+(cap?'<p>'+cap.innerHTML.replace(/<span class="fig-hint">.*?<\\/span>/,'')+'</p>':'');document.body.appendChild(lb);document.body.style.overflow='hidden';return;}
if(lb&&e.target.closest('.ox-lb')){if(e.target.tagName==='IMG')lb.classList.toggle('big');else if(e.target.closest('.ox-lb-x')||e.target===lb)c();}});
document.addEventListener('keydown',function(e){if(e.key==='Escape')c();});window.addEventListener('hashchange',c);})();</script>'''

FIGRE = re.compile(r'\n?\s*<figure class="fig" data-ox="[^"]*">.*?</figure>', re.S)
TOPRE = re.compile(r'<details class="topic"[^>]*><summary>(.*?)</summary>', re.S)


def fig(name, cap, cred):
    cred_h = f'<small class="ox-cred">{escape(cred)}</small>'
    if name in ESQ:
        return f'\n    <figure class="fig" data-ox="{name}">{ESQ[name][0]}<figcaption>{escape(cap)}{cred_h}</figcaption></figure>'
    from PIL import Image
    w, h = Image.open(os.path.join(HERE, 'img', name)).size
    src = 'img/ref/' + name
    return (f'\n    <figure class="fig" data-ox="{name}"><button type="button" class="fig-img" data-zoom="{src}" aria-label="Ampliar imagen">'
            f'<img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{escape(cap)}"></button>'
            f'<figcaption>{escape(cap)} <span class="fig-hint">Toca para ampliar.</span>{cred_h}</figcaption></figure>')


for dst in dsts:
    dst = os.path.abspath(dst)
    rdir = os.path.join(os.path.dirname(dst), 'img', 'ref')
    os.makedirs(rdir, exist_ok=True)
    s = open(dst, encoding='utf-8').read()
    s = FIGRE.sub('', s)
    n = 0
    for tema, despues, name, cap, cred in rows:
        m = next((m for m in TOPRE.finditer(s) if re.sub('<[^>]+>', '', m.group(1)).strip().startswith(tema)), None)
        if not m:
            sys.exit(f'No encontré el tema «{tema}»')
        end = s.index('</div></details>', m.end())
        pos = end
        if despues:
            h = s.find(f'<h4>{despues}</h4>', m.end(), end)
            if h < 0:
                sys.exit(f'No encontré «{despues}» en {tema}')
            nxt = s.find('<h4', h + 4, end)
            pos = nxt if nxt >= 0 else end
        while s[pos - 1] in ' \n':
            pos -= 1
        s = s[:pos] + fig(name, cap, cred) + s[pos:]
        if name not in ESQ:
            shutil.copy(os.path.join(HERE, 'img', name), os.path.join(rdir, name))
        n += 1
    if '/*ox*/' not in s:
        k = s.index('</style>', s.index('.fig figcaption{'))
        s = s[:k] + CSS + s[k:]
    if '/*ox-lb*/' not in s:
        j = s.rindex('</body>')
        s = s[:j] + JS + s[j:]
    open(dst, 'w', encoding='utf-8').write(s)
    print(f'{n} figuras en {dst}')
