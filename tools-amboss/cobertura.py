# Revisa qué subtemas (de harvest.js) todavía no tienen término en terminos.tsv.
# Uso: node tools-amboss/harvest.js > /tmp/sub.tsv && python3 tools-amboss/cobertura.py /tmp/sub.tsv [filtro]
import sys,os,re,unicodedata
HERE=os.path.dirname(os.path.abspath(__file__))
def norm(s):
    s=unicodedata.normalize('NFD',s); s=''.join(c for c in s if unicodedata.category(c)!='Mn').lower()
    s=re.sub(r'^\s*(clase|tema)?\s*\d+(\.\d+)*\s*[·.\-:)]?\s*','',s)
    s=re.sub(r'\s*\d+\s*(img|imagen(es)?|tarjetas?)\b.*$','',s)
    s=re.sub(r'[✓★†*]','',s); return re.sub(r'\s+',' ',s).strip()
tab={}
for ln in open(os.path.join(HERE,'terminos.tsv'),encoding='utf-8'):
    ln=ln.rstrip('\n')
    if not ln.strip() or ln.startswith('#'): continue
    k,v=ln.split('\t',1)
    if k.startswith('* '): key='* '+norm(k[2:])
    elif ' › ' in k: a,b=k.split(' › ',1); key=norm(a)+' › '+norm(b)
    else: key=norm(k)
    tab[key]=v.strip()
def q(t,c):
    nt,nc=norm(t),norm(c)
    v=tab.get(nc+' › '+nt)
    if v is None: v=tab.get(nt)
    if v is None and ('* '+nt) in tab and tab.get(nc) not in (None,'-'): v=(tab[nc]+' '+tab['* '+nt]).strip()
    return v
flt=sys.argv[2] if len(sys.argv)>2 else ''
miss=[];cur=None;n=0
for l in open(sys.argv[1],encoding='utf-8'):
    f,c,t,_=l.rstrip('\n').split('\t'); n+=1
    if flt and flt not in f: continue
    if not t: continue
    if q(t,c) is None:
        if (f,c)!=cur: cur=(f,c); print(f'\n## {f} :: {c} ::',end=' ')
        print(t,end=' | '); miss.append(t)
print(f'\n\nfaltan {len(miss)} de {n}')
