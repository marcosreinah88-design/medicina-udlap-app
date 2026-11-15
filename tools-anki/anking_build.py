# Arma el mazo AnKing traducido y CIFRADO (site/anki/anking/<sistema>.txt en base64 + index.json).
# Las traducciones NO van al repositorio (es público): viven en project-files/anki/anking/.
# Uso: python3 tools-anki/anking_build.py <carpeta con notes.json y out/*.tsv> <archivo con la clave> [SITE]
# Cifrado: gzip + AES-256-GCM, llave = HKDF-SHA256(clave, salt "medicina-udlap/anking/v1", info "mazo"); archivo = iv(12) + ct.
import sys,os,json,re,glob,gzip,unicodedata,base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
SRC,KEYF=sys.argv[1],sys.argv[2]
SITE=sys.argv[3] if len(sys.argv)>3 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site')
OUT=os.path.join(SITE,'anki','anking');os.makedirs(OUT,exist_ok=True)
pw=open(KEYF).read().strip().encode()
key=HKDF(algorithm=hashes.SHA256(),length=32,salt=b'medicina-udlap/anking/v1',info=b'mazo').derive(pw)
notes={o['k']:o for o in json.load(open(os.path.join(SRC,'notes.json')))}
tr={}
for f in sorted(glob.glob(os.path.join(SRC,'out','*.tsv'))):
    for l in open(f,encoding='utf-8'):  # también las partes de lotes a medio terminar
        p=l.rstrip('\n').split('\t')
        if len(p)==2: p.append('')
        if len(p)==3 and p[0].isdigit(): tr[int(p[0])]=p
CL=re.compile(r'\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}')
def cards(t,e):
    out=[]
    nums=sorted({int(m.group(1)) for m in CL.finditer(t)})
    for n in nums:
        f=CL.sub(lambda m:('['+(m.group(3) or '…')+']') if int(m.group(1))==n else m.group(2),t)
        b=CL.sub(lambda m:('**'+m.group(2)+'**') if int(m.group(1))==n else m.group(2),t)
        out.append((f,b+(' · '+e if e else '')))
    return out
slug=lambda s:re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFD',s).encode('ascii','ignore').decode().lower()).strip('-')
# mazos muy chicos se juntan con su sistema; dentro del mazo siguen como tema propio
JUNTA={'Genética':'Bioquímica','Biología celular':'Bioquímica','Oftalmología':'Neurología',
       'General':'Urgencias, cirugía y medicina interna','Urgencias':'Urgencias, cirugía y medicina interna',
       'Cirugía y anestesia':'Urgencias, cirugía y medicina interna','Medicina interna':'Urgencias, cirugía y medicina interna',
       'Patología general':'Farmacología y patología general','Farmacología':'Farmacología y patología general'}
decks={};miss=0;x=0
for k,o in notes.items():
    p=tr.get(k)
    if not p: miss+=1;continue
    if p[1]=='X': x+=1;continue
    for f,b in cards(p[1].strip(),p[2].strip()):
        decks.setdefault(JUNTA.get(o['s'],o['s']),[]).append([o['s'],f,b])
idx=[]
for s,c in sorted(decks.items(),key=lambda kv:-len(kv[1])):
    sid=slug(s);d={'id':'anking-'+sid,'n':'AnKing · '+s,'s':0,'c':c,'q':[]}
    raw=gzip.compress(json.dumps(d,ensure_ascii=False,separators=(',',':')).encode(),9)
    iv=os.urandom(12);open(os.path.join(OUT,sid+'.txt'),'w').write(base64.b64encode(iv+AESGCM(key).encrypt(iv,raw,None)).decode())
    idx.append({'id':sid,'n':s,'c':len(c)})
json.dump(idx,open(os.path.join(OUT,'index.json'),'w'),ensure_ascii=False,indent=0)
print('mazos',len(idx),'tarjetas',sum(i['c'] for i in idx),'notas sin traducir',miss,'descartadas',x)
