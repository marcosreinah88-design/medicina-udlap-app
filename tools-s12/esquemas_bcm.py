# Esquemas propios (SVG, en español) de biología celular y molecular para la guía de Biología Celular y Molecular (2º):
# célula y organelos, membrana, vía secretora, citoesqueleto, cromatina, replicación, procesamiento del ARNm,
# traducción, ciclo celular, proteínas G y PCR.
# Dibujados desde cero: no copian figuras de libros.
# Uso: python3 tools-s12/esquemas_bcm.py      (escribe en tools-s12/img/biologia-celular/)
import math, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
GID = 'biologia-celular'
F = 'font-family="Helvetica,Arial,sans-serif"'
ROJO='#b3261e'; VERDE='#00573c'; NAR='#f26b21'; AZUL='#2b6cb0'; MOR='#7b3fa0'; GRIS='#555'; AMA='#e0a800'
ROSA='#f6cfdc'; NUC='#5b3b8c'; NUC2='#8a6cc0'; CIT='#fdf3e7'; MEM='#c0788f'

def svg(name, w, h, body):
    d = os.path.join(HERE, 'img', GID); os.makedirs(d, exist_ok=True)
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {F}><rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>'
    open(os.path.join(d, name), 'w').write(s)
def T(x,y,s,size=15,c='#222',anchor='middle',w='normal'):
    s = str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{c}" text-anchor="{anchor}" font-weight="{w}">{s}</text>'
def TL(x,y,lines,size=13,c='#222',anchor='middle',w='normal',lh=None):
    lh = lh or size*1.25
    return ''.join(T(x,y+i*lh,l,size,c,anchor,w) for i,l in enumerate(lines))
def arrow(x1,y1,x2,y2,c='#333',w=2.5,head=10,dash=''):
    a = math.atan2(y2-y1, x2-x1)
    hx1 = x2-head*math.cos(a-.4); hy1 = y2-head*math.sin(a-.4)
    hx2 = x2-head*math.cos(a+.4); hy2 = y2-head*math.sin(a+.4)
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2-head*.7*math.cos(a):.1f}" y2="{y2-head*.7*math.sin(a):.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{da}/>'
            f'<path d="M{x2:.1f},{y2:.1f} L{hx1:.1f},{hy1:.1f} L{hx2:.1f},{hy2:.1f}Z" fill="{c}"/>')
def line(x1,y1,x2,y2,c='#333',w=1.5,dash=''):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{da}/>'
def box(x,y,w,h,fill,stroke,r=10,sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def tbox(x,y,w,h,lines,fill,stroke,size=14,c='#222',wt='normal'):
    n=len(lines); lh=size*1.25; y0=y+h/2-(n-1)*lh/2+size*.35
    return box(x,y,w,h,fill,stroke)+TL(x+w/2,y0,lines,size,c,'middle',wt,lh)
def circ(cx,cy,r,fill,stroke='none',sw=1.5,extra=''):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'
def ell(cx,cy,rx,ry,fill,stroke='none',sw=1.5,rot=0):
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" transform="rotate({rot} {cx:.1f} {cy:.1f})"/>'
def path(d,stroke='#333',w=2,fill='none',extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'
def blob(cx,cy,r,fill,stroke,sw=2,wob=.12,k=5,seed=0,n=48,sx=1,sy=1):
    rnd=random.Random(seed); ph=rnd.random()*6.28; ph2=rnd.random()*6.28
    pts=[(cx+sx*r*(1+wob*math.sin(k*t+ph)+wob*.5*math.sin((k+2)*t+ph2))*math.cos(t), cy+sy*r*(1+wob*math.sin(k*t+ph)+wob*.5*math.sin((k+2)*t+ph2))*math.sin(t)) for t in [i/n*6.2832 for i in range(n)]]
    return f'<path d="M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+f'Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
def title(w,t,sub=None):
    o=T(w/2,30,t,20,VERDE,w='bold')
    if sub: o+=T(w/2,52,sub,13,GRIS)
    return o
def label(px,py,tx,ty,txt,anchor='start',c='#222',size=13,w='normal'):
    return line(px,py,tx,ty,'#777',1.2)+circ(px,py,2.6,'#333')+T(tx+(4 if anchor=='start' else -4 if anchor=='end' else 0),ty+4,txt,size,c,anchor,w)
def mito(cx,cy,rx,ry,rot=0):
    o=ell(cx,cy,rx,ry,'#f8c99b','#b8641e',1.6,rot)
    n=max(3,int(rx/9)); d=f'M{cx-rx*.8:.1f},{cy:.1f}'
    for i in range(n):
        x=cx-rx*.8+(i+.5)*(1.6*rx/n); d+=f' L{x:.1f},{cy+(-1 if i%2 else 1)*ry*.6:.1f}'
    d+=f' L{cx+rx*.8:.1f},{cy:.1f}'
    return o+f'<g transform="rotate({rot} {cx:.1f} {cy:.1f})">'+path(d,'#b8641e',1.3)+'</g>'
def rib(x,y,r=3): return circ(x,y,r,'#3b3b6b')

# ───────── 1. Célula animal y organelos ─────────
W,H=900,640
b=[title(W,'La célula eucariota y sus organelos','Esquema de una célula animal (no está a escala)')]
cx,cy=430,350
b.append(blob(cx,cy,250,CIT,MEM,4,.05,3,4,90,1.05,.95))
# núcleo
b.append(circ(360,330,92,'#e7dcf5',NUC,3))
b.append(circ(360,330,84,'none',NUC,1.5,' stroke-dasharray="2,0"'))
for a in range(0,360,40):
    x=360+88*math.cos(math.radians(a)); y=330+88*math.sin(math.radians(a))
    b.append(circ(x,y,4,'#fff',NUC,1.5))
b.append(circ(380,315,26,'#5b3b8c'))  # nucléolo
rnd=random.Random(3)
for i in range(18):
    a=rnd.random()*6.28; r=30+rnd.random()*45
    b.append(circ(360+r*math.cos(a),330+r*math.sin(a),5+rnd.random()*4,'#c2aee2'))
# RER (cisternas alrededor del núcleo a la derecha)
for k in range(4):
    r=110+k*16
    d=f'M{360+r*math.cos(math.radians(-60)):.1f},{330+r*math.sin(math.radians(-60)):.1f} A{r},{r} 0 0 1 {360+r*math.cos(math.radians(40)):.1f},{330+r*math.sin(math.radians(40)):.1f}'
    b.append(path(d,'#3f7fbf',7)+path(d,'#cfe2f5',3.5))
    for a in range(-58,40,9):
        b.append(rib(360+(r+5)*math.cos(math.radians(a)),330+(r+5)*math.sin(math.radians(a)),2.4))
# REL (abajo)
for k in range(3):
    y=488+k*14
    d=f'M250,{y} q20,-10 40,0 t40,0 t40,0'
    b.append(path(d,'#3f7fbf',7)+path(d,'#cfe2f5',3.5))
# Golgi
for k in range(5):
    r=60-k*7
    d=f'M{590-r:.1f},{230+k*11} q{r},{-28+k*2} {2*r},0'
    b.append(path(d,'#d97a1f',7)+path(d,'#fde3c4',3.5))
for (x,y) in ((640,215),(655,245),(530,215),(620,300),(560,180)): b.append(circ(x,y,7,'#fde3c4','#d97a1f',1.8))
# mitocondrias
b.append(mito(600,420,46,22,-20)); b.append(mito(250,200,40,19,25)); b.append(mito(500,520,38,18,10))
# lisosomas
for (x,y) in ((660,360),(220,420)): b.append(circ(x,y,17,'#f4c2c2','#b3261e',2)+circ(x-4,y-3,3,'#b3261e')+circ(x+5,y+4,2.5,'#b3261e'))
# peroxisoma
b.append(circ(690,450,14,'#e6f2d0','#5c8a1e',2)+f'<rect x="684" y="444" width="12" height="12" fill="#9cc25a" transform="rotate(45 690 450)"/>')
# centrosoma
for dx,rot in ((0,0),(14,90)):
    b.append(f'<rect x="{240+dx-5}" y="{285-14}" width="10" height="28" rx="2" fill="#7fb07f" stroke="{VERDE}" stroke-width="1.5" transform="rotate({rot} {240+dx} 285)"/>')
# ribosomas libres
for i in range(26):
    a=rnd.random()*6.28; r=150+rnd.random()*80
    x=cx+r*math.cos(a); y=cy+r*.85*math.sin(a)
    if 180<x<690 and 140<y<580: b.append(rib(x,y,2.6))
# microvellosidades arriba
for i in range(9):
    x=330+i*22; b.append(path(f'M{x},{112} L{x},{86}',MEM,8)+path(f'M{x},{112} L{x},{87}',CIT,4))
# etiquetas
b.append(T(380,362,'Nucléolo',12,NUC,'middle','bold'))
b.append(label(250,200,60,150,'Mitocondria (ATP)','start'))
b.append(label(240,285,60,250,'Centrosoma (2 centriolos)','start'))
b.append(label(293,387,60,340,'Núcleo (envoltura con poros)','start'))
b.append(label(220,420,60,430,'Lisosoma (pH ~5)','start'))
b.append(label(270,500,60,510,'Retículo endoplásmico liso','start'))
b.append(label(410,98,620,72,'Microvellosidades (actina)','start'))
b.append(label(488,270,700,120,'Retículo endoplásmico rugoso','start'))
b.append(label(590,236,700,180,'Aparato de Golgi','start'))
b.append(label(655,245,700,240,'Vesículas de transporte','start'))
b.append(label(660,360,730,350,'Lisosoma','start'))
b.append(label(690,450,730,440,'Peroxisoma','start'))
b.append(label(600,420,730,500,'Mitocondria: crestas','start'))
b.append(label(561,555,730,590,'Membrana plasmática','start'))
svg('celula-organelos.svg',W,H,''.join(b))

# ───────── 2. Membrana plasmática (mosaico fluido) ─────────
W,H=900,520
b=[title(W,'Membrana plasmática: modelo de mosaico fluido','Bicapa de fosfolípidos con colesterol, proteínas y glucocálix')]
top,bot=210,330
b.append(T(30,150,'Exterior',14,VERDE,'start','bold')); b.append(T(30,420,'Citoplasma',14,NAR,'start','bold'))
def plipid(x,y,up=True):
    s=-1 if not up else 1
    o=circ(x,y,7,'#f3a35c','#b8641e',1.2)
    o+=path(f'M{x-3},{y+s*7} l0,{s*12} l2,{s*8} l-2,{s*10}','#b8641e',1.6)
    o+=path(f'M{x+3},{y+s*7} l0,{s*30}','#b8641e',1.6)
    return o
skip=[(200,260),(370,420),(560,640),(720,760)]
xs=[x for x in range(70,840,16) if not any(a<=x<=b_ for a,b_ in skip)]
for x in xs:
    b.append(plipid(x,top,True)); b.append(plipid(x,bot,False))
# colesterol
for x in (118,310,470,686,808):
    b.append(f'<rect x="{x-4}" y="{top+12}" width="8" height="26" rx="3" fill="{AMA}" stroke="#8a6a00" stroke-width="1"/>')
# proteína integral (canal)
b.append(box(200,top-30,60,180,'#9cc1e8',AZUL,18,2)); b.append(f'<rect x="223" y="{top-30}" width="14" height="180" fill="#fff" opacity=".8"/>')
# receptor con glucocálix
b.append(box(370,top-20,50,160,'#b9a3dc',MOR,16,2))
b.append(path(f'M395,{top-20} l0,-26 m0,10 l-14,-16 m14,16 l14,-16 m-14,-6 l-8,-14 m8,14 l9,-14','#5c8a1e',3))
for (x,y) in ((381,top-62),(409,top-62),(387,top-74),(404,top-74)): b.append(circ(x,y,5,'#9cc25a','#5c8a1e',1))
# transportador grande
b.append(blob(600,270,60,'#a9d7c5',VERDE,2,.08,3,8,48,.75,1.2))
# glucolípido
b.append(path(f'M134,{top-7} l0,-30 m0,8 l-12,-14 m12,14 l12,-14','#5c8a1e',3))
for (x,y) in ((122,top-51),(146,top-51),(134,top-44)): b.append(circ(x,y,5,'#9cc25a','#5c8a1e',1))
# periférica
b.append(ell(740,bot+24,34,16,'#f6b6a0',ROJO,2))
b.append(ell(750,top-22,30,14,'#f6b6a0',ROJO,2))
# etiquetas
b.append(label(230,top-30,160,90,'Proteína integral (canal)','middle'))
b.append(label(395,top-70,420,80,'Glucoproteína (receptor) → glucocálix','middle'))
b.append(label(134,top-50,80,118,'Glucolípido','middle'))
b.append(label(600,200,620,120,'Transportador','middle'))
b.append(label(750,top-36,790,120,'Proteína periférica','middle'))
b.append(label(470,top+25,520,440,'Colesterol (regula la fluidez)','middle'))
b.append(label(310+16*1,bot,300,470,'Cabeza polar (hidrófila)','middle'))
b.append(label(694,top+30,700,420,'Colas (hidrófobas)','middle'))
b.append(label(740,bot+38,790,480,'Proteína periférica','middle'))
b.append(f'<line x1="870" y1="{top-8}" x2="870" y2="{bot+8}" stroke="{GRIS}" stroke-width="1.5"/>'+T(862,(top+bot)/2+4,'≈ 7–8 nm',12,GRIS,'end'))
svg('membrana-mosaico.svg',W,H,''.join(b))

# ───────── 3. Vía secretora ─────────
W,H=900,520
b=[title(W,'Vía secretora: del ribosoma a su destino','La manosa-6-fosfato (Golgi) es la «dirección» de las enzimas lisosomales')]
# núcleo/RER
b.append(path('M40,140 A120,120 0 0 1 40,420','#7a62b0',14)+path('M40,140 A120,120 0 0 1 40,420','#e7dcf5',8))
b.append(T(60,470,'Núcleo',13,NUC,'start','bold'))
for k in range(3):
    r=150+k*26; d=f'M{40+r*math.cos(math.radians(-55)):.1f},{280+r*math.sin(math.radians(-55)):.1f} A{r},{r} 0 0 1 {40+r*math.cos(math.radians(55)):.1f},{280+r*math.sin(math.radians(55)):.1f}'
    b.append(path(d,'#3f7fbf',10)+path(d,'#cfe2f5',5))
    for a in range(-52,56,7): b.append(rib(40+(r+8)*math.cos(math.radians(a)),280+(r+8)*math.sin(math.radians(a)),3))
b.append(T(170,100,'RER',16,AZUL,'middle','bold'))
b.append(TL(170,500-0,['Péptido señal + SRP → entra al RER;','plegamiento y N-glucosilación'],12,GRIS))
# vesículas COPII
for (x,y) in ((272,240),(298,240)): b.append(circ(x,y,9,'#cfe2f5','#3f7fbf',2))
b.append(arrow(255,265,330,265,'#3f7fbf',2.5)); b.append(T(285,222,'COPII',12,AZUL,'middle','bold'))
b.append(T(290,242,'',12))
# Golgi
gx=420
for k in range(5):
    y=200+k*26
    b.append(path(f'M{gx-70},{y} q70,-22 140,0','#d97a1f',12)+path(f'M{gx-70},{y} q70,-22 140,0','#fde3c4',7))
b.append(T(gx,165,'Aparato de Golgi',16,'#b0600f','middle','bold'))
b.append(T(gx-90,196,'cis',12,GRIS,'end')); b.append(T(gx-90,252,'medial',12,GRIS,'end')); b.append(T(gx-90,306,'trans',12,GRIS,'end'))
b.append(TL(gx,350,['O-glucosilación, clasifica','y marca con manosa-6-fosfato'],12,GRIS))
# salidas
dest=[(130,'#f4c2c2',ROJO,'Lisosoma',['Enzimas con manosa-6-P','(si falta: enfermedad de células I)']),
      (270,'#d9ecd2',VERDE,'Membrana plasmática',['Receptores, canales,','transportadores']),
      (410,'#fde3c4','#b0600f','Secreción',['Constitutiva o regulada','(insulina, enzimas pancreáticas)'])]
for y,fill,st,t,sub in dest:
    b.append(arrow(gx+75,306,640,y+18,st,2.5))
    b.append(box(650,y-14,230,72,fill,st,12,2)); b.append(T(765,y+8,t,15,st,'middle','bold')); b.append(TL(765,y+28,sub,12,'#333'))
svg('via-secretora.svg',W,H,''.join(b))

# ───────── 4. Citoesqueleto y motores ─────────
W,H=900,600
b=[title(W,'Citoesqueleto y motores moleculares','Tres filamentos de distinto grosor; cinesina y dineína caminan sobre los microtúbulos')]
rows=[(110,'Microfilamentos (actina)','≈ 7 nm',ROJO,'#f4b4a8','Microvellosidades, contracción, anillo de citocinesis'),
      (210,'Filamentos intermedios','≈ 10 nm','#8a6a00','#f1dc8f','Resistencia mecánica; marcadores de tumores'),
      (310,'Microtúbulos (tubulina α/β)','≈ 25 nm',VERDE,'#9fd3b4','Huso mitótico, cilios 9+2, transporte axonal')]
for y,t,d,c,f,sub in rows:
    b.append(T(40,y-22,t,15,c,'start','bold')); b.append(T(40,y+38,sub,12,GRIS,'start'))
    if 'actina' in t:
        for i in range(30):
            x=60+i*14; b.append(circ(x,y-3+4*math.sin(i*.9),6,f,c,1)); b.append(circ(x+7,y+5-4*math.sin(i*.9),6,f,c,1))
        th=16
    elif 'intermedios' in t:
        for k in range(4): b.append(path(f'M60,{y-8+k*5} '+' '.join(f'Q{60+i*30+15},{y-8+k*5+(8 if (i+k)%2 else -8)} {60+i*30+30},{y-8+k*5}' for i in range(14)),c,3))
        th=22
    else:
        b.append(box(60,y-18,420,36,f,c,18,1.5))
        for i in range(30):
            b.append(circ(66+i*14,y-9,6,'#c8ead5' if i%2 else f,c,1)); b.append(circ(66+i*14,y+9,6,f if i%2 else '#c8ead5',c,1))
        th=36
    b.append(f'<line x1="500" y1="{y-th/2-2}" x2="500" y2="{y+th/2+2}" stroke="#333" stroke-width="1.5"/>')
    b.append(T(510,y+5,d,14,'#333','start','bold'))
# motores
y=490
b.append(T(450,385,'Transporte axonal sobre un microtúbulo',15,'#222','middle','bold'))
b.append(box(80,y-10,740,20,'#9fd3b4',VERDE,10,1.5))
b.append(T(70,y+5,'−',22,VERDE,'end','bold')); b.append(T(830,y+6,'+',22,VERDE,'start','bold'))
b.append(T(80,y+42,'Soma (centrosoma)',12,GRIS,'start')); b.append(T(820,y+42,'Terminal del axón',12,GRIS,'end'))
# cinesina → +
kx=560
b.append(path(f'M{kx-10},{y-10} l6,-22 M{kx+10},{y-10} l-6,-22','#2b6cb0',5)+path(f'M{kx},{y-32} l0,-20','#2b6cb0',4)+circ(kx,y-64,15,'#fde3c4','#d97a1f',2))
b.append(arrow(kx+30,y-40,kx+130,y-40,AZUL,3)); b.append(T(kx+95,y-55,'Cinesina → (+)',14,AZUL,'middle','bold'))
b.append(T(kx+70,y+70,'Anterógrado: vesículas, neurotransmisores',12,AZUL))
# dineína ← -
dx=320
b.append(path(f'M{dx-10},{y-10} l6,-22 M{dx+10},{y-10} l-6,-22',MOR,5)+path(f'M{dx},{y-32} l0,-20',MOR,4)+circ(dx,y-64,15,'#f4c2c2',ROJO,2))
b.append(arrow(dx-30,y-40,dx-130,y-40,MOR,3)); b.append(T(dx-95,y-55,'(−) ← Dineína',14,MOR,'middle','bold'))
b.append(T(dx-70,y+70,'Retrógrado: rabia, herpes, toxina tetánica',12,MOR))
b.append(T(450,y+100,'La dineína también mueve cilios y flagelos (falla en el síndrome de Kartagener).',12.5,'#333'))
svg('citoesqueleto-motores.svg',W,H,''.join(b))

# ───────── 5. Empaquetamiento de la cromatina ─────────
W,H=900,380
b=[title(W,'Del ADN al cromosoma','Cada nivel compacta más el ADN; la heterocromatina está condensada e inactiva')]
y=200
# doble hélice
for i in range(80):
    x=30+i*2.2; b.append(circ(x,y+12*math.sin(i*.35),1.8,AZUL)); b.append(circ(x,y-12*math.sin(i*.35),1.8,ROJO))
b.append(TL(100,290,['Doble hélice','≈ 2 nm'],13,'#222'))
b.append(arrow(215,y,245,y,'#999',2,8))
# nucleosomas (cuentas en un hilo)
xs=[290,350,410]
b.append(path(f'M255,{y} '+' '.join(f'L{x-22},{y}' for x in xs)+' L470,'+str(y),'#333',2))
for x in xs:
    b.append(circ(x,y,20,'#9fd3b4',VERDE,2)); b.append(path(f'M{x-22},{y+4} q22,-22 44,-8','#333',2.2)); b.append(path(f'M{x-22},{y+10} q22,14 44,-2','#333',2.2))
b.append(TL(355,290,['Nucleosomas','«cuentas en un hilo»','8 histonas + H1 de enlace'],13,'#222'))
b.append(arrow(480,y,510,y,'#999',2,8))
# fibra 30nm
for i in range(10):
    a=i*.9; b.append(circ(560+i*6,y+18*math.sin(a),9,'#9fd3b4',VERDE,1.2))
b.append(TL(590,290,['Fibra de','30 nm'],13,'#222'))
b.append(arrow(640,y,670,y,'#999',2,8))
# bucles
b.append(line(735,160,735,240,'#999',4))
for k in range(6):
    yy=168+k*14; sg=-1 if k%2 else 1
    b.append(path(f'M735,{yy} C{735+sg*60},{yy-22} {735+sg*60},{yy+22} 735,{yy+6}','#4c9a6a',3))
b.append(TL(735,290,['Bucles en','andamio'],13,'#222'))
b.append(arrow(785,y,805,y,'#999',2,8))
# cromosoma
b.append(f'<g transform="translate(845 200)">'+ell(-12,-35,12,36,'#7b3fa0',NUC,1.5,-8)+ell(12,-35,12,36,'#7b3fa0',NUC,1.5,8)+ell(-12,35,12,36,'#7b3fa0',NUC,1.5,8)+ell(12,35,12,36,'#7b3fa0',NUC,1.5,-8)+circ(0,0,7,'#e7dcf5',NUC,1.5)+'</g>')
b.append(TL(845,290,['Cromosoma','en metafase'],13,'#222'))
b.append(T(450,350,'Acetilar histonas relaja la cromatina (eucromatina, activa); metilar el ADN la silencia.',13,'#333'))
svg('cromatina-niveles.svg',W,H,''.join(b))

# ───────── 6. Horquilla de replicación ─────────
W,H=900,520
b=[title(W,'Horquilla de replicación','La ADN polimerasa solo sintetiza 5′→3′: una hebra continua y otra en fragmentos de Okazaki')]
fx,fy=380,260
# hebras parentales
b.append(path(f'M60,{fy-8} L{fx},{fy-8}','#555',6)); b.append(path(f'M60,{fy+8} L{fx},{fy+8}','#555',6))
for i in range(20): b.append(line(70+i*15,fy-5,70+i*15,fy+5,'#bbb',2))
b.append(T(60,fy-24,'ADN original',13,GRIS,'start'))
# brazos
b.append(path(f'M{fx},{fy-8} L840,120','#555',6)); b.append(path(f'M{fx},{fy+8} L840,400','#555',6))
b.append(T(846,118,"3′",14,'#333','start','bold')); b.append(T(846,410,"5′",14,'#333','start','bold'))
# helicasa
b.append(f'<polygon points="{fx-6},{fy-28} {fx+34},{fy} {fx-6},{fy+28}" fill="{NAR}" stroke="#a64612" stroke-width="2"/>')
b.append(label(fx+10,fy-14,fx-30,fy-90,'Helicasa (abre)','end',NAR,13,'bold'))
# topoisomerasa
b.append(circ(220,fy,16,'#f4c2c2',ROJO,2)); b.append(label(220,fy-16,200,fy-60,'Topoisomerasa (girasa)','middle',ROJO,13,'bold'))
# SSB
for t in (.35,.55,.75):
    x=fx+(840-fx)*t; y1=fy-8+(120-fy+8)*t; y2=fy+8+(400-fy-8)*t
    b.append(circ(x,y1+2,6,'#d9ecd2',VERDE,1.2)); b.append(circ(x+10,y2-2,6,'#d9ecd2',VERDE,1.2))
b.append(label(fx+(840-fx)*.55,fy-8+(120-fy+8)*.55+2,690,80,'Proteínas SSB','start',VERDE,13,'bold'))
# hebra adelantada (abajo? usar arriba como molde 3'->5', nueva continua)
# arriba: molde 3' en el extremo derecho → hebra nueva continua 5'→3' hacia la horquilla
def onarm(t,sign,off): # punto sobre brazo superior (sign=-1) o inferior (+1) con desplazamiento perpendicular
    x=fx+(840-fx)*t; y=fy+sign*8+((120 if sign<0 else 400)-fy-sign*8)*t
    return x, y+off
x1,y1=onarm(.92,-1,18); x2,y2=onarm(.08,-1,18)
b.append(path(f'M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}',AZUL,6))
xa,ya=onarm(.3,-1,18); xb,yb=onarm(.16,-1,18); b.append(arrow(xa,ya,xb,yb,AZUL,6,16))
b.append(T(640,250,'Hebra adelantada (continua)',14,AZUL,'middle','bold'))
b.append(circ(x2+8,y2,13,'#cfe2f5',AZUL,2)); b.append(T(x2+8,y2+4,'δ',13,AZUL,'middle','bold'))
# hebra retrasada: fragmentos
for t0,t1 in ((.12,.3),(.36,.56),(.62,.84)):
    a1,a2=onarm(t1,1,-18); c1,c2=onarm(t0,1,-18)
    b.append(path(f'M{a1:.0f},{a2:.0f} L{c1:.0f},{c2:.0f}','#2f9e6b',6))
    p1,p2=onarm(t1,1,-18); q1,q2=onarm(t1-.04,1,-18)
    b.append(path(f'M{p1:.0f},{p2:.0f} L{q1:.0f},{q2:.0f}',ROJO,7))  # cebador ARN al inicio (5')
b.append(T(640,420,'Hebra retrasada: fragmentos de Okazaki',14,'#2f7a52','middle','bold'))
b.append(T(640,440,'(ADN polimerasa δ; se aleja de la horquilla)',12,GRIS))
p1,p2=onarm(.84,1,-18); b.append(label(p1,p2,720,330,'Cebador de ARN (primasa)','start',ROJO,13,'bold'))
q1,q2=onarm(.33,1,-18); b.append(label(q1,q2,520,370,'ADN ligasa sella las uniones','middle','#333',13,'bold'))
b.append(T(450,490,'Replicación semiconservativa: cada molécula hija conserva una hebra original.',13,'#333'))
svg('horquilla-replicacion.svg',W,H,''.join(b))

# ───────── 7. Procesamiento del ARNm ─────────
W,H=900,500
b=[title(W,'Del gen al ARNm maduro','Caperuza 5′, cola de poli-A y splicing ocurren en el núcleo')]
def exons(y,parts,x0=150,h=30,cap=False,tail=False,label_y=None):
    o=''; x=x0
    for kind,w in parts:
        if kind=='E': o+=box(x,y,w,h,'#9fd3b4',VERDE,4,2)
        elif kind=='I': o+=box(x,y+h/2-4,w,8,'#ddd','#999',3,1)
        else: o+=box(x,y,w,h,'#f6cfdc',MEM,4,1.5)
        x+=w
    return o,x
gene=[('P',70),('E',90),('I',80),('E',70),('I',110),('E',100)]
o,xe=exons(100,gene,120); b.append(o)
b.append(T(155,94,'Promotor (TATA)',12,MEM)); b.append(T(40,120,'Gen (ADN)',14,'#222','start','bold'))
for i,(x,t) in enumerate(((235,'Exón 1'),(385,'Exón 2'),(590,'Exón 3'))): b.append(T(x,150,t,12,VERDE))
b.append(T(315,150,'Intrón',12,GRIS)); b.append(T(495,150,'Intrón',12,GRIS))
b.append(arrow(400,165,400,195,'#333')); b.append(T(410,186,'Transcripción (ARN polimerasa II)',13,'#333','start'))
o,xe=exons(210,gene[1:],190); b.append(o); b.append(T(40,230,'Pre-ARNm',14,'#222','start','bold'))
b.append(arrow(400,255,400,285,'#333')); b.append(T(410,276,'Caperuza 5′ + cola de poli-A + splicing (espliceosoma, snRNP)',13,'#333','start'))
# intrón lazo
b.append(path('M300,330 q-20,-30 0,-38 q20,8 0,38','#999',3)+T(330,312,'intrón en lazo, se degrada',11,GRIS,'start'))
o,xe=exons(340,[('E',90),('E',70),('E',100)],230); b.append(o)
b.append(circ(214,355,14,'#fde3c4','#d97a1f',2)+T(214,360,'m⁷G',10,'#8a4a00','middle','bold'))
b.append(path(f'M{xe},355 '+' '.join(f'l8,{-5 if i%2 else 5}' for i in range(12)),'#d97a1f',3)+T(xe+50,385,'AAAA…',13,'#b0600f','middle','bold'))
b.append(T(40,360,'ARNm maduro',14,'#222','start','bold'))
b.append(T(214,395,'Caperuza 5′',12,'#b0600f'))
b.append(arrow(400,410,400,440,'#333')); b.append(T(410,432,'Sale por el poro nuclear → traducción en el citoplasma',13,'#333','start'))
b.append(T(450,478,'Splicing alternativo: diferentes combinaciones de exones dan varias proteínas de un mismo gen.',12.5,'#333'))
svg('procesamiento-arnm.svg',W,H,''.join(b))

# ───────── 8. Traducción en el ribosoma ─────────
W,H=900,540
b=[title(W,'Traducción: sitios E, P y A del ribosoma','El ARNt entra al sitio A, el péptido pasa al P y el ARNt vacío sale por el E')]
my=380
b.append(ell(370,my-110,215,125,'#e7dcf5',NUC,2)); b.append(T(370,my-244,'Subunidad grande (60S)',13,NUC,'middle','bold'))
b.append(ell(370,my+36,190,32,'#cbbfe6',NUC,2)); b.append(T(370,my+86,'Subunidad pequeña (40S)',13,NUC,'middle','bold'))
for i,(sname,t) in enumerate((('E','salida'),('P','peptidil'),('A','aminoacil'))):
    x=260+i*110; b.append(box(x-46,my-200,92,192,'#fff','#b8a6dd',10,1.5))
    b.append(T(x,my-176,sname,22,NUC,'middle','bold')); b.append(T(x,my-158,t,12,GRIS))
def trna(x,col,aas=()):
    o=path(f'M{x-11},{my-4} L{x-11},{my-56} M{x+11},{my-4} L{x+11},{my-56}',col,7)+circ(x,my-64,13,col)
    for k,(n,cl) in enumerate(aas):
        yy=my-92-k*24; o+=circ(x,yy,11,cl,'#555',1.5)+T(x,yy+4,n,9.5,'#222','middle','bold')
    return o
b.append(trna(260,'#cfcfcf'))
b.append(trna(370,'#f3a35c',(('Phe','#cfe2f5'),('Ala','#9fd3b4'),('Met','#fde3c4'))))
b.append(trna(480,'#7fb2e5',(('Lys','#f6cfdc'),)))
b.append(path(f'M60,{my} L840,{my}','#555',4))
cod='AUG GCU UUC AAA GGC UAA'.split()
for i,c in enumerate(cod):
    x=150+i*110; b.append(T(x,my+24,c,15,ROJO if c in('AUG','UAA') else '#222','middle','bold'))
b.append(T(60,my+24,"5′",14,'#333','start','bold')); b.append(T(840,my+24,"3′",14,'#333','end','bold'))
b.append(arrow(640,my-210,505,my-110,AZUL,2.5)); b.append(T(630,my-236,'Entra el aminoacil-ARNt',13,AZUL,'start','bold'))
b.append(T(630,my-219,'(lo cargó la aminoacil-ARNt sintetasa)',12,GRIS,'start'))
b.append(arrow(240,my-90,150,my-170,'#999',2.5)); b.append(T(40,my-182,'Sale el ARNt vacío',13,GRIS,'start','bold'))
b.append(label(425,my-104,620,my-110,'Peptidil transferasa:','start','#333',12.5,'bold'))
b.append(T(624,my-90,'el ARNr (ribozima) une el péptido',12,GRIS,'start')); b.append(T(624,my-74,'al aminoácido del sitio A',12,GRIS,'start'))
b.append(arrow(560,my+60,680,my+60,'#333',2,8)); b.append(T(690,my+65,'avanza 5′→3′',12,'#333','start'))
b.append(T(450,510,'AUG = inicio (metionina) · UAA, UAG, UGA = terminación',13,'#333'))
svg('traduccion-ribosoma.svg',W,H,''.join(b))

# ───────── 9. Ciclo celular ─────────
W,H=900,560
b=[title(W,'Ciclo celular y sus puntos de control','Las ciclinas y sus CDK lo empujan; p53, Rb y p21 lo frenan')]
cx,cy,R=330,310,170
fases=[('G1',0,150,'#9fd3b4','Crecimiento'),('S',150,250,'#9cc1e8','Replica el ADN'),('G2',250,320,'#f1dc8f','Prepara la mitosis'),('M',320,360,'#f4b4a8','Mitosis')]
def arc(a0,a1,r0,r1):
    a0,a1=math.radians(a0-90),math.radians(a1-90)
    p=lambda a,r:(cx+r*math.cos(a),cy+r*math.sin(a))
    la=1 if a1-a0>math.pi else 0
    (x1,y1),(x2,y2),(x3,y3),(x4,y4)=p(a0,r1),p(a1,r1),p(a1,r0),p(a0,r0)
    return f'M{x1:.1f},{y1:.1f} A{r1},{r1} 0 {la} 1 {x2:.1f},{y2:.1f} L{x3:.1f},{y3:.1f} A{r0},{r0} 0 {la} 0 {x4:.1f},{y4:.1f}Z'
for n,a0,a1,c,s in fases:
    b.append(f'<path d="{arc(a0+1,a1-1,95,R)}" fill="{c}" stroke="#fff" stroke-width="3"/>')
    am=math.radians((a0+a1)/2-90); b.append(T(cx+132*math.cos(am),cy+132*math.sin(am)+2,n,24,'#222','middle','bold'))
    b.append(T(cx+132*math.cos(am),cy+132*math.sin(am)+20,s,11,'#333'))
b.append(TL(cx,cy-6,['Interfase','G1 + S + G2'],15,'#333','middle','bold'))
# checkpoints
for ang,t,yy in ((150,'Punto G1/S',0),(320,'Punto G2/M',0),(345,'Punto del huso (metafase)',0)):
    a=math.radians(ang-90); x=cx+(R+8)*math.cos(a); y=cy+(R+8)*math.sin(a)
    b.append(f'<rect x="{x-9:.1f}" y="{y-9:.1f}" width="18" height="18" fill="{ROJO}" transform="rotate(45 {x:.1f} {y:.1f})"/>')
b.append(label(cx+(R+8)*math.cos(math.radians(60)),cy+(R+8)*math.sin(math.radians(60)),560,430,'Punto G1/S: el más importante (Rb, p53)','start',ROJO,13,'bold'))
b.append(label(cx+(R+8)*math.cos(math.radians(230)),cy+(R+8)*math.sin(math.radians(230)),40,150,'Punto G2/M (daño del ADN)','start',ROJO,13,'bold'))
b.append(label(cx+(R+8)*math.cos(math.radians(255)),cy+(R+8)*math.sin(math.radians(255)),180,90,'Punto del huso','middle',ROJO,13,'bold'))
# G0
b.append(circ(cx+250,cy-150,34,'#eee','#999',2)+T(cx+250,cy-145,'G0',18,'#555','middle','bold'))
b.append(path(f'M{cx+90},{cy-130} Q{cx+180},{cy-200} {cx+218},{cy-158}','#999',2.5)); b.append(T(cx+265,cy-100,'Reposo (estables)',11,GRIS))
# motores y frenos
b.append(box(560,250,320,140,'#f7f7f2','#bbb',12,1.5))
b.append(T(720,275,'Motores y frenos',15,'#222','middle','bold'))
b.append(TL(575,300,['Ciclina D–CDK4/6: fosforila Rb → libera E2F','Ciclina E–CDK2: entrada a S','Ciclina B–CDK1: entrada a M','Frenos: p53 → p21; p27; p16 (inhiben CDK)'],12.5,'#333','start'))
b.append(T(450,540,'Lábiles: siempre en ciclo · Estables: en G0, regresan · Permanentes: no se dividen',13,'#333'))
svg('ciclo-celular.svg',W,H,''.join(b))

# ───────── 10. Proteínas G ─────────
W,H=900,560
b=[title(W,'Receptores acoplados a proteína G','Gs sube el AMPc, Gi lo baja y Gq activa la fosfolipasa C')]
my=190
b.append(f'<rect x="20" y="{my-14}" width="860" height="28" fill="#f6cfdc" stroke="{MEM}" stroke-width="1.5"/>')
cols=[(150,'Gs',AZUL,'#cfe2f5',['β1, β2, D1, H2, V2'],['Adenilato ciclasa ↑','ATP → AMPc ↑','PKA'],'Toxina del cólera la deja encendida'),
      (450,'Gi','#555','#e5e5e5',['α2, M2, D2'],['Adenilato ciclasa ↓','AMPc ↓'],'Toxina pertussis la bloquea'),
      (750,'Gq',MOR,'#e7dcf5',['H1, α1, V1, M1, M3'],['Fosfolipasa C','PIP₂ → IP₃ + DAG','IP₃: Ca²⁺ ↑ · DAG: PKC'],'«HAVe 1 M&M»')]
for x,g,c,f,rec,steps,note in cols:
    for k in range(7): b.append(f'<rect x="{x-48+k*14}" y="{my-26}" width="10" height="52" rx="4" fill="{f}" stroke="{c}" stroke-width="1.5"/>')
    b.append(circ(x,my-48,12,NAR,'#a64612',1.5)); b.append(T(x,my-68,'Ligando',12,'#a64612','middle','bold'))
    b.append(T(x,my-90,'Receptores: '+rec[0],12.5,'#333','middle'))
    b.append(ell(x+70,my+34,30,18,f,c,2)); b.append(T(x+70,my+39,g,15,c,'middle','bold'))
    yy=my+70
    for s in steps:
        b.append(arrow(x,yy-10,x,yy+10,c,2,8)) if yy>my+70 else None
        b.append(tbox(x-125,yy+12,250,38,[s],f,c,13,'#222','bold')); yy+=60
    b.append(T(x,yy+30,note,12,GRIS))
b.append(T(450,540,'7 dominios transmembrana · respuesta: Gs relaja bronquio (β2), Gq contrae músculo liso (α1)',13,'#333'))
svg('proteinas-g.svg',W,H,''.join(b))

# ───────── 11. PCR ─────────
W,H=900,470
b=[title(W,'Un ciclo de PCR','Cada ciclo duplica el fragmento: tras 30 ciclos hay ~10⁹ copias')]
steps=[(150,'1. Desnaturalización','~95 °C','Se separan las hebras',ROJO,'#f4c2c2'),
       (450,'2. Alineamiento','~55 °C','Los cebadores se unen',AZUL,'#cfe2f5'),
       (750,'3. Extensión','~72 °C','La Taq polimerasa sintetiza',VERDE,'#d9ecd2')]
for x,t,temp,s,c,f in steps:
    b.append(box(x-130,80,260,250,f,c,14,2))
    b.append(T(x,108,t,16,c,'middle','bold')); b.append(T(x,132,temp,14,'#333','middle','bold'))
    if 'Desn' in t:
        b.append(path(f'M{x-100},175 L{x+100},175','#555',6)); b.append(path(f'M{x-100},245 L{x+100},245','#555',6))
        b.append(arrow(x,190,x,160,c,2,8)); b.append(arrow(x,230,x,260,c,2,8))
    elif 'Alin' in t:
        b.append(path(f'M{x-100},175 L{x+100},175','#555',6)); b.append(path(f'M{x-100},245 L{x+100},245','#555',6))
        b.append(path(f'M{x+40},188 L{x+95},188',ROJO,6)); b.append(path(f'M{x-95},232 L{x-40},232',ROJO,6))
        b.append(T(x,212,'cebadores',12,ROJO,'middle','bold'))
    else:
        b.append(path(f'M{x-100},175 L{x+100},175','#555',6)); b.append(path(f'M{x-100},245 L{x+100},245','#555',6))
        b.append(path(f'M{x+95},188 L{x-60},188',ROJO,6)); b.append(path(f'M{x-95},232 L{x+60},232',ROJO,6))
        b.append(path(f'M{x+40},188 L{x-60},188',AZUL,6)); b.append(path(f'M{x-40},232 L{x+60},232',AZUL,6))
        b.append(circ(x-66,188,9,'#9fd3b4',VERDE,1.5)); b.append(circ(x+66,232,9,'#9fd3b4',VERDE,1.5))
    b.append(T(x,300,s,13,'#333'))
for x in (280,580): b.append(arrow(x+8,205,x+32,205,'#555',3))
b.append(path('M750,340 Q450,420 150,340','#999',2.5,'none',' stroke-dasharray="6,5"')); b.append(f'<path d="M150,340 l14,2 l-6,10z" fill="#999"/>')
b.append(T(450,402,'Se repite 25–35 veces en el termociclador',13,GRIS,'middle','bold'))
b.append(T(450,446,'RT-PCR: primero la transcriptasa inversa pasa el ARN a ADNc (carga viral de VIH, COVID-19).',13,'#333'))
svg('pcr-ciclo.svg',W,H,''.join(b))
print('listo')
