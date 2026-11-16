# Esquemas propios (SVG, en español) para las guías de Fisiología (2º) y Anatomofisiología (1º).
# Dibujados desde cero con valores fisiológicos de referencia: no copian figuras de libros.
# Uso: python3 tools-s12/esquemas_fisio.py        (escribe en tools-s12/img/fisiologia/ y img/anatomofisiologia/)
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
F = 'font-family="Helvetica,Arial,sans-serif"'
ROJO='#b3261e'; VERDE='#00573c'; NAR='#f26b21'; AZUL='#2b6cb0'; MOR='#7b3fa0'; GRIS='#555'; AMA='#e0a800'; CAFE='#8a5a2b'; TEAL='#0f6f6a'

def svg(gid, name, w, h, body):
    d = os.path.join(HERE, 'img', gid); os.makedirs(d, exist_ok=True)
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {F}>'
         f'<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')
    open(os.path.join(d, name), 'w').write(s)

def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def T(x,y,s,size=15,c='#222',anchor='middle',w='normal',extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{c}" text-anchor="{anchor}" font-weight="{w}"{extra}>{esc(s)}</text>'
def TL(x,y,lines,size=13,c='#222',anchor='middle',w='normal',lh=None):
    lh = lh or size*1.25
    return ''.join(T(x,y+i*lh,l,size,c,anchor,w) for i,l in enumerate(lines))
def TR(x,y,s,size=14,c='#222',w='normal'):   # texto vertical
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{c}" text-anchor="middle" font-weight="{w}" transform="rotate(-90 {x:.1f} {y:.1f})">{esc(s)}</text>'
def line(x1,y1,x2,y2,c='#333',w=2,dash=''):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{da}/>'
def arrow(x1,y1,x2,y2,c='#333',w=2.5,head=10,dash=''):
    a = math.atan2(y2-y1, x2-x1)
    hx1 = x2-head*math.cos(a-.4); hy1 = y2-head*math.sin(a-.4)
    hx2 = x2-head*math.cos(a+.4); hy2 = y2-head*math.sin(a+.4)
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2-head*.7*math.cos(a):.1f}" y2="{y2-head*.7*math.sin(a):.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{da}/>'
            f'<path d="M{x2:.1f},{y2:.1f} L{hx1:.1f},{hy1:.1f} L{hx2:.1f},{hy2:.1f}Z" fill="{c}"/>')
def box(x,y,w,h,fill,stroke,r=10,sw=2):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def tbox(x,y,w,h,lines,fill,stroke,size=14,c='#222',wt='normal'):
    n=len(lines); lh=size*1.25; y0=y+h/2-(n-1)*lh/2+size*.35
    return box(x,y,w,h,fill,stroke)+TL(x+w/2,y0,lines,size,c,'middle',wt,lh)
def circ(cx,cy,r,fill,stroke='none',sw=2):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def poly(pts): return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)
def path(d,stroke='#333',w=2.5,fill='none',dash='',extra=''):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{da}{extra}/>'
def smooth(pts, t=.5):
    """Catmull-Rom → Bézier: curva suave que pasa por todos los puntos."""
    if len(pts) < 3: return poly(pts)
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(len(pts)-1):
        p0 = pts[i-1] if i else pts[i]; p1 = pts[i]; p2 = pts[i+1]; p3 = pts[i+2] if i+2 < len(pts) else p2
        c1 = (p1[0]+(p2[0]-p0[0])*t/3, p1[1]+(p2[1]-p0[1])*t/3)
        c2 = (p2[0]-(p3[0]-p1[0])*t/3, p2[1]-(p3[1]-p1[1])*t/3)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d
def interp(pts, x):
    for (x0,y0),(x1,y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1: return y0 + (y1-y0)*(x-x0)/(x1-x0 or 1)
    return pts[-1][1]
def axes(x0,y0,x1,y1,xl,yl,size=14):
    return (arrow(x0,y0,x1,y0,'#222',2,9)+arrow(x0,y0,x0,y1,'#222',2,9)
            +T((x0+x1)/2,y0+34,xl,size,'#222')+TR(x0-40,(y0+y1)/2,yl,size))
def num(cx,cy,n,c=VERDE,r=13):
    return circ(cx,cy,r,c)+T(cx,cy+5,n,14,'#fff',w='bold')
def ion(cx,cy,s,c,r=14,size=11):
    return circ(cx,cy,r,c)+T(cx,cy+4,s,size,'#fff',w='bold')
def brace_h(x1,x2,y,c='#333',up=True,d=8):
    s = -1 if up else 1
    return path(f'M{x1},{y} q0,{s*d} {d},{s*d} L{(x1+x2)/2-d},{y+s*d} q{d},0 {d},{s*d} q0,{-s*d} {d},{-s*d} L{x2-d},{y+s*d} q{d},0 {d},{-s*d}', c, 1.8)
def brace_v(x,y1,y2,c='#333',right=True,d=8):
    s = 1 if right else -1
    return path(f'M{x},{y1} q{s*d},0 {s*d},{d} L{x+s*d},{(y1+y2)/2-d} q0,{d} {s*d},{d} q{-s*d},0 {-s*d},{d} L{x+s*d},{y2-d} q0,{d} {-s*d},{d}', c, 1.8)
def title(w,s,y=28,size=18): return T(w/2,y,s,size,VERDE,w='bold')

FI = 'fisiologia'
AF = 'anatomofisiologia'

# ═════════════════════════ FISIOLOGÍA (2º) ═════════════════════════
# ── Tipos de transporte a través de la membrana
W,H=980,470
b=[title(W,'Tipos de transporte a través de la membrana')]
MY0,MY1=215,285   # bicapa
b.append(f'<rect x="20" y="{MY0}" width="{W-40}" height="{MY1-MY0}" fill="#fdf3dc"/>')
for x in range(28,W-20,16):
    b.append(circ(x,MY0+7,6,'#f0b65a')); b.append(circ(x,MY1-7,6,'#f0b65a'))
    for dx in (-2,2):
        b.append(line(x+dx,MY0+13,x+dx,(MY0+MY1)/2-2,'#d6a24c',1.5)); b.append(line(x+dx,MY1-13,x+dx,(MY0+MY1)/2+2,'#d6a24c',1.5))
b.append(T(30,62,'LÍQUIDO EXTRACELULAR',13,AZUL,'start','bold')); b.append(T(215,62,'Na⁺ ≈ 140 mM · K⁺ ≈ 4 mM',12,AZUL,'start'))
b.append(T(30,452,'CITOPLASMA',13,ROJO,'start','bold')); b.append(T(140,452,'Na⁺ ≈ 12 mM · K⁺ ≈ 140 mM',12,ROJO,'start'))
cols=[(110,'Difusión simple','sin proteína, a favor'),(290,'Difusión facilitada','canal o transportador'),
      (480,'Ósmosis','agua por acuaporinas'),(680,'Activo primario','gasta ATP directamente'),(870,'Activo secundario','usa el gradiente de Na⁺')]
for cx,t1,t2 in cols:
    b.append(T(cx,98,t1,14,'#222',w='bold')); b.append(T(cx,116,t2,12,GRIS))
for xx in (200,385,575,778): b.append(line(xx,86,xx,380,'#ddd',1,'4 4'))
# 1 difusión simple
for dx,(s_,c) in zip((-30,0,30),(('O₂',AZUL),('CO₂',GRIS),('O₂',AZUL))):
    b.append(T(110+dx,160,s_,12,c,w='bold')); b.append(arrow(110+dx,170,110+dx,312,c,2.2,9))
b.append(T(110,338,'de más a menos',12,GRIS)); b.append(T(110,353,'concentración',12,GRIS))
# 2 canal
cx=290
b.append(box(cx-34,MY0-6,24,MY1-MY0+12,'#7fb8e6','#2b6cb0',8)); b.append(box(cx+10,MY0-6,24,MY1-MY0+12,'#7fb8e6','#2b6cb0',8))
b.append(ion(cx,170,'K⁺',ROJO,12,10)); b.append(arrow(cx,185,cx,318,AZUL,2.6,10)); b.append(T(cx,345,'canal iónico, GLUT',12,GRIS))
# 3 ósmosis
cx=480
b.append(box(cx-30,MY0-6,20,MY1-MY0+12,'#a5d8ff','#1c7ed6',8)); b.append(box(cx+10,MY0-6,20,MY1-MY0+12,'#a5d8ff','#1c7ed6',8))
for y in (170,200,240,270): b.append(circ(cx,y,6,'#4dabf7'))
b.append(T(cx+14,165,'H₂O',12,'#1c7ed6','start','bold'))
b.append(arrow(cx,292,cx,322,'#1c7ed6',2.4,9)); b.append(T(cx,345,'el agua va hacia',12,GRIS)); b.append(T(cx,360,'más osmolalidad',12,GRIS))
# 4 bomba Na/K
cx=680; cy=(MY0+MY1)/2
b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="44" ry="52" fill="#d3f9d8" stroke="{VERDE}" stroke-width="2.5"/>')
b.append(T(cx,cy-4,'Na⁺/K⁺',12,VERDE,w='bold')); b.append(T(cx,cy+12,'ATPasa',12,VERDE,w='bold'))
b.append(arrow(cx-60,MY1+45,cx-60,MY0-45,ROJO,2.6,10)); b.append(T(cx-60,MY0-52,'3 Na⁺ salen',13,ROJO,'middle','bold'))
b.append(arrow(cx+60,MY0-45,cx+60,MY1+45,AZUL,2.6,10)); b.append(T(cx+60,MY1+64,'2 K⁺ entran',13,AZUL,'middle','bold'))
b.append(T(cx-60,MY1+64,'ATP → ADP',12,VERDE,'middle','bold'))
b.append(T(cx,375,'la inhibe la digoxina',11.5,GRIS))
# 5 SGLT
cx=870
b.append(box(cx-32,MY0-6,64,MY1-MY0+12,'#ffe8cc','#e8590c',14)); b.append(T(cx,(MY0+MY1)/2+5,'SGLT',13,'#c2410c',w='bold'))
b.append(T(cx-22,160,'Na⁺',12,ROJO,w='bold')); b.append(T(cx+26,160,'glucosa',12,'#c2410c',w='bold'))
b.append(arrow(cx-16,170,cx-16,318,ROJO,2.4,9)); b.append(arrow(cx+16,170,cx+16,318,'#c2410c',2.4,9))
b.append(T(cx,345,'el Na⁺ baja su gradiente',12,GRIS)); b.append(T(cx,360,'y arrastra la glucosa',12,GRIS))
b.append(T(W/2,410,'Pasivo (sin ATP): difusión simple, facilitada y ósmosis · Activo: primario (ATP) y secundario (gradiente que dejó la bomba)',12.5,'#333'))
svg(FI,'transporte.svg',W,H,''.join(b))

# ── Potencial de acción neuronal
W,H=900,470
b=[title(W,'Potencial de acción neuronal')]
X0,Y0,XW=90,380,560      # eje: 0–5 ms
def Vy(v): return Y0-(v+90)*2.6       # −90…+40 mV
def Tx(t): return X0+t/5*XW
b.append(axes(X0,Y0,X0+XW+30,60,'Tiempo (ms)','Potencial de membrana (mV)'))
for v in (-90,-70,-55,0,30):
    b.append(line(X0,Vy(v),X0+XW,Vy(v),'#e3e3e3',1,'4 4')); b.append(T(X0-8,Vy(v)+4,str(v).replace('-','−'),12,GRIS,'end'))
for t in range(0,6): b.append(T(Tx(t),Y0+17,str(t),12,GRIS))
b.append(T(X0+XW+4,Vy(-55)-6,'umbral',12,NAR,'end','bold'))
# periodos refractarios
b.append(f'<rect x="{Tx(1.05):.1f}" y="62" width="{Tx(2.25)-Tx(1.05):.1f}" height="{Y0-62}" fill="#fde2e2" opacity=".55"/>')
b.append(f'<rect x="{Tx(2.25):.1f}" y="62" width="{Tx(3.6)-Tx(2.25):.1f}" height="{Y0-62}" fill="#fff3bf" opacity=".6"/>')
b.append(T((Tx(1.05)+Tx(2.25))/2,76,'Refractario absoluto',11.5,ROJO,w='bold'))
b.append(T((Tx(2.25)+Tx(3.6))/2,76,'Refractario relativo',11.5,'#a07800',w='bold'))
pts=[(0,-70),(.6,-70),(.75,-66),(.95,-56),(1.05,-48),(1.2,0),(1.35,28),(1.45,30),(1.6,15),(1.9,-30),(2.25,-70),(2.5,-82),(2.9,-80),(3.6,-72),(4.2,-70),(5,-70)]
P=[(Tx(t),Vy(v)) for t,v in pts]
b.append(path(smooth(P,.45),ROJO,3.2))
b.append(arrow(Tx(.62),Y0-4,Tx(.62),Vy(-70)+6,'#444',2,8)); b.append(T(Tx(.62),Y0-8+0,'estímulo',11,'#444','start',extra=' dx="6"'))
# fases (marcadores)
fx=[(.3,-70,0,-16,'1'),(1.0,-52,-14,-6,'2'),(1.23,-10,-22,0,'3'),(1.45,30,24,4,'4'),(1.85,-20,22,0,'5'),(2.65,-81,0,-16,'6')]
for t,v,dx,dy,n in fx: b.append(num(Tx(t)+dx,Vy(v)+dy,n,'#333',11))
lx=680
leg=[('1','Reposo (−70 mV): fuga de K⁺'),('2','Llega al umbral (−55 mV)'),('3','Despolarización: entra Na⁺'),
     ('4','Pico (+30 mV): se inactiva el Na⁺'),('5','Repolarización: sale K⁺'),('6','Hiperpolarización: el K⁺ cierra tarde')]
for i,(n,s) in enumerate(leg):
    y=104+i*44; b.append(num(lx,y,n,'#333',11)); b.append(TL(lx+18,y+5,[s],12.5,'#222','start'))
# barras de canales
y=418
b.append(T(X0,y-4+0,'',1))
b.append(box(Tx(.95),y-10,Tx(1.5)-Tx(.95),14,'#ffc9c9','none',4,0)); b.append(T(Tx(.95)-6,y+1,'Canales de Na⁺ abiertos',11.5,ROJO,'end','bold'))
b.append(box(Tx(1.4),y+12,Tx(2.95)-Tx(1.4),14,'#a5d8ff','none',4,0)); b.append(T(Tx(1.4)-6,y+23,'Canales de K⁺ abiertos',11.5,AZUL,'end','bold'))
b.append(T(lx,400,'La lidocaína y la tetrodotoxina',12,GRIS,'start')); b.append(T(lx,416,'bloquean los canales de Na⁺:',12,GRIS,'start')); b.append(T(lx,432,'sin fase 3 no hay potencial.',12,GRIS,'start'))
svg(FI,'pa-neuronal.svg',W,H,''.join(b))

# ── Sinapsis química
W,H=1030,470
b=[title(W,'Sinapsis química paso a paso',24)]
b.append(path('M405,44 L405,92 C300,96 230,140 230,192 C230,252 300,272 450,272 C600,272 670,252 670,192 C670,140 600,96 495,92 L495,44','#7b3fa0',3,'#f3eafa'))
b.append(T(450,120,'Terminal presináptica',14,MOR,w='bold'))
b.append(arrow(450,40,450,84,ROJO,3,10)); b.append(T(375,64,'potencial de acción',12,ROJO,'end','bold'))
import random; random.seed(3)
for (x,y) in [(330,170),(380,195),(430,160),(480,190),(540,165),(585,205),(400,235),(500,235),(345,222)]:
    b.append(circ(x,y,17,'#fff','#7b3fa0',2))
    for k in range(5): b.append(circ(x+random.uniform(-9,9),y+random.uniform(-9,9),2.6,NAR))
b.append(path('M438,272 Q450,252 462,272',MOR,2,'#fff'))
for (dx,dy) in [(-30,22),(-12,30),(5,24),(20,32),(35,20),(-20,40),(12,44),(28,40)]: b.append(circ(450+dx,272+dy,3,NAR))
b.append(box(272,252,20,30,'#ffd43b','#c99700',5)); b.append(box(296,252,20,30,'#ffd43b','#c99700',5))
b.append(arrow(294,304,294,234,'#c99700',2.4,9)); b.append(T(266,298,'Ca²⁺',13,'#a07800','end','bold'))
b.append(T(150,296,'Hendidura',13,GRIS,'start')); b.append(T(150,312,'sináptica',13,GRIS,'start'))
b.append(path('M200,340 L700,340 L700,430 L200,430Z','#2b6cb0',0,'#e7f1fb'))
b.append(line(200,340,700,340,AZUL,3))
for x in (380,450,520): b.append(box(x-16,326,32,28,'#74c0fc',AZUL,6))
b.append(arrow(450,356,450,410,AZUL,2.6,9)); b.append(T(462,400,'entra Na⁺ (PEPS) o Cl⁻ (PIPS)',12,AZUL,'start','bold'))
b.append(T(450,450,'Neurona o célula postsináptica',14,AZUL,w='bold'))
b.append(arrow(600,306,628,260,'#2f9e44',2.4,9)); b.append(T(640,284,'recaptura',12,'#2f9e44','start','bold'))
b.append(T(640,300,'(la bloquean los ISRS)',11,GRIS,'start'))
b.append(T(566,332,'✂ enzima (AChE)',11.5,ROJO,'start'))
pasos=[('1',474,58),('2',318,236),('3',488,262),('4',412,312),('5',432,382),('6',584,284)]
for n,x,y in pasos: b.append(num(x,y,n,'#333',11))
leg=['Llega el potencial de acción','Se abren canales de Ca²⁺','Exocitosis de vesículas (SNARE)','El neurotransmisor se une al receptor','Potencial postsináptico','Se retira: recaptura o enzima']
for i,s_ in enumerate(leg):
    y=120+i*36; b.append(num(784,y,str(i+1),'#333',11)); b.append(T(802,y+5,s_,13,'#222','start'))
svg(FI,'sinapsis.svg',W,H,''.join(b))
svg(FI,'sinapsis.svg',W,H,''.join(b))

# ── Sarcómero relajado y contraído
W,H=900,470
b=[title(W,'El sarcómero: deslizamiento de los filamentos')]
def sarc(cy, z1, z2, thin, lab):
    o=[T(30,cy-58,lab,15,VERDE,'start','bold')]
    mid=(z1+z2)/2
    for zz in (z1,z2):
        o.append(path(f'M{zz},{cy-56} l-7,14 l14,14 l-14,14 l14,14 l-14,14 l14,14 l-14,14 l7,6','#333',3))
    for dy in (-36,0,36):
        for x0,x1 in ((z1,z1+thin),(z2-thin,z2)):
            o.append(line(x0,cy+dy,x1,cy+dy,AZUL,4))
            for xx in range(int(x0)+6,int(x1),12): o.append(circ(xx,cy+dy,3.2,'#74c0fc'))
    for dy in (-18,18):
        o.append(line(mid-160,cy+dy,mid+160,cy+dy,ROJO,7))
        for xx in range(int(mid-150),int(mid+151),20):
            if abs(xx-mid)<14: continue
            s_=-1 if xx<mid else 1
            o.append(line(xx,cy+dy,xx+s_*7,cy+dy-8,ROJO,2.4)); o.append(line(xx,cy+dy,xx+s_*7,cy+dy+8,ROJO,2.4))
    o.append(line(mid,cy-48,mid,cy+48,'#7b3fa0',2,'5 4'))
    return ''.join(o), mid
s1,m1=sarc(140,150,750,250,'Relajado')
b.append(s1)
y=200
b.append(brace_h(290,610,y,ROJO,False)); b.append(T(450,y+28,'Banda A (miosina: no cambia)',12.5,ROJO,w='bold'))
b.append(brace_h(400,500,y-128,'#7b3fa0',True)); b.append(T(450,y-142,'Zona H',12.5,MOR,w='bold'))
b.append(brace_h(150,290,y,AZUL,False)); b.append(T(220,y+28,'½ banda I',12.5,AZUL,w='bold'))
b.append(brace_h(610,750,y,AZUL,False)); b.append(T(680,y+28,'½ banda I',12.5,AZUL,w='bold'))
b.append(T(150,y-128,'Disco Z',12.5,'#333',w='bold')); b.append(T(750,y-128,'Disco Z',12.5,'#333',w='bold'))
b.append(T(m1+8,y-10+0,'',1))
s2,m2=sarc(340,230,670,250,'Contraído')
b.append(s2)
y=400
b.append(brace_h(290,610,y,ROJO,False)); b.append(T(450,y+28,'Banda A igual',12.5,ROJO,w='bold'))
b.append(brace_h(230,290,y,AZUL,False)); b.append(T(222,y+28,'banda I ↓',12.5,AZUL,'end','bold'))
b.append(brace_h(610,670,y,AZUL,False)); b.append(T(678,y+28,'banda I ↓',12.5,AZUL,'start','bold'))
b.append(T(450,272,'Línea M',12,MOR,w='bold'))
b.append(T(780,300,'Los discos Z',12.5,'#333','start')); b.append(T(780,317,'se acercan; la',12.5,'#333','start')); b.append(T(780,334,'zona H y la',12.5,'#333','start')); b.append(T(780,351,'banda I se',12.5,'#333','start')); b.append(T(780,368,'acortan.',12.5,'#333','start'))
b.append(line(40,458,60,458,AZUL,4)); b.append(T(66,462,'actina (delgado)',12,AZUL,'start'))
b.append(line(200,458,220,458,ROJO,6)); b.append(T(226,462,'miosina (grueso)',12,ROJO,'start'))
svg(FI,'sarcomero.svg',W,H,''.join(b))

# ── Curva longitud-tensión
W,H=760,400
b=[title(W,'Relación longitud-tensión del sarcómero')]
X0,Y0=100,330
def Lx(l): return X0+(l-1.0)/3.0*560
def Ty(t): return Y0-t*2.4
b.append(axes(X0,Y0,X0+590,70,'Longitud del sarcómero (µm)','Tensión activa (% de la máxima)'))
for l in (1.0,1.5,2.0,2.5,3.0,3.5,4.0): b.append(T(Lx(l),Y0+18,str(l),12,GRIS))
for t in (0,50,100): b.append(T(X0-8,Ty(t)+4,str(t),12,GRIS,'end'))
b.append(f'<rect x="{Lx(2.0):.1f}" y="{Ty(100)-6:.1f}" width="{Lx(2.25)-Lx(2.0):.1f}" height="{Y0-Ty(100)+6:.1f}" fill="#e6f4ea"/>')
pts=[(1.27,0),(1.67,78),(2.0,100),(2.25,100),(3.65,0)]
b.append(path(poly([(Lx(l),Ty(t)) for l,t in pts]),ROJO,3.4))
b.append(T(Lx(2.12),Ty(100)-30,'Longitud óptima',13,VERDE,w='bold'))
b.append(T(Lx(2.12),Ty(100)-14,'≈ 2.0–2.2 µm',12,VERDE))
b.append(TL(Lx(1.64),Ty(40),['Muy corto:','filamentos','chocan'],12,GRIS,'start'))
b.append(TL(Lx(3.15),Ty(70),['Muy estirado: casi no','hay superposición','actina-miosina'],12,GRIS,'start'))
svg(FI,'longitud-tension.svg',W,H,''.join(b))

# ── Potenciales de acción cardiacos
W,H=960,470
b=[title(W,'Potenciales de acción del corazón')]
def panel(x0,w,tmax,pts,ttl,col,ticks):
    y0=360
    def X(t): return x0+t/tmax*w
    def Y(v): return y0-(v+100)*2.3
    o=[T(x0+w/2,58,ttl,15,col,w='bold'), axes(x0,y0,x0+w+20,72,'Tiempo (ms)','mV')]
    for v in (-90,-60,-40,0,20):
        o.append(line(x0,Y(v),x0+w,Y(v),'#e6e6e6',1,'4 4')); o.append(T(x0-8,Y(v)+4,str(v).replace('-','−'),11.5,GRIS,'end'))
    for t in ticks: o.append(T(X(t),y0+17,str(t),11.5,GRIS))
    o.append(path(smooth([(X(t),Y(v)) for t,v in pts],.35),col,3.2))
    return o,X,Y
o,X,Y=panel(90,360,400,[(0,-90),(18,-90),(22,-60),(26,20),(34,22),(42,6),(60,4),(120,2),(180,-4),(220,-20),(260,-62),(285,-86),(300,-90),(400,-90)],'Miocito ventricular (respuesta rápida)',ROJO,(0,100,200,300,400))
b+=o
for t,v,n,dx,dy in [(24,-20,'0',-18,0),(38,20,'1',16,-2),(130,2,'2',0,-18),(250,-50,'3',16,0),(350,-90,'4',0,-16)]: b.append(num(X(t)+dx,Y(v)+dy,n,ROJO,11))
leg=[('0','entra Na⁺ rápido'),('1','sale K⁺ (muesca)'),('2','meseta: entra Ca²⁺ (L)'),('3','sale K⁺'),('4','reposo estable −90 mV')]
o2,X2,Y2=panel(590,300,800,[(0,-60),(120,-50),(230,-42),(260,-30),(290,8),(310,10),(340,-10),(400,-55),(430,-60),(550,-50),(660,-42),(690,-30),(720,8),(740,10),(770,-10),(800,-40)],'Nodo sinusal (marcapasos)',VERDE,(0,200,400,600,800))
b+=o2
for t,v,n,dx,dy in [(130,-50,'4',0,-18),(275,-12,'0',-18,0),(370,-30,'3',16,0)]: b.append(num(X2(t)+dx,Y2(v)+dy,n,VERDE,11))
b.append(line(X2(0),Y2(-40),X2(800),Y2(-40),NAR,1.4,'6 4')); b.append(T(X2(800),Y2(-40)-6,'umbral',11,NAR,'end','bold'))
for i,(n,s_) in enumerate(leg): b.append(num(110+i*0,0,'',ROJO,0))
for i,(n,s_) in enumerate(leg):
    xx=100+(i%3)*150 if i<3 else 100+(i-3)*150; yy=428 if i<3 else 450
    b.append(num(xx,yy-5,n,ROJO,9)); b.append(T(xx+14,yy,s_,11.5,'#333','start'))
for i,(n,s_) in enumerate([('4','sube sola: corriente funny (Na⁺)'),('0','entra Ca²⁺ (más lenta)'),('3','sale K⁺')]):
    b.append(num(600,423+i*16,n,VERDE,7)); b.append(T(612,427+i*16,s_,11.5,'#333','start'))
svg(FI,'pa-cardiaco.svg',W,H,''.join(b))

# ── ECG: ondas, segmentos e intervalos
W,H=900,420
b=[title(W,'El electrocardiograma de un latido')]
gx0,gy0,gw,gh=60,50,780,300
for i in range(0,gw+1,10):
    b.append(line(gx0+i,gy0,gx0+i,gy0+gh,'#f6c6c6' if i%50 else '#eb9a9a',1 if i%50 else 1.6))
for j in range(0,gh+1,10):
    b.append(line(gx0,gy0+j,gx0+gw,gy0+j,'#f6c6c6' if j%50 else '#eb9a9a',1 if j%50 else 1.6))
BL=260
def ex(t): return gx0+40+t*1.6     # t en ms → 1 mm (10 px) = 40 ms ⇒ 0.25 px/ms … escala didáctica
pts=[(0,0),(30,0),(50,8),(80,14),(110,8),(130,0),(170,0),(178,-8),(190,0),(205,120),(220,-24),(232,0),(260,0),(300,0),(330,10),(370,34),(400,30),(425,10),(450,0),(470,0)]
P=[(ex(t),BL-v*1.2) for t,v in pts]
b.append(path(smooth(P,.25),'#111',3))
def lab(t,v,s_,dy=-14,c='#111'): return T(ex(t),BL-v*1.2+dy,s_,15,c,w='bold')
b+= [lab(80,14,'P',-12),lab(178,-8,'Q',24),lab(205,120,'R',-10),lab(220,-24,'S',24),lab(372,34,'T',-12)]
# intervalos
yb=330
def iv(t1,t2,y,s_,c):
    return line(ex(t1),y,ex(t2),y,c,2.4)+line(ex(t1),y-6,ex(t1),y+6,c,2.4)+line(ex(t2),y-6,ex(t2),y+6,c,2.4)+T((ex(t1)+ex(t2))/2,y-6,s_,12.5,c,w='bold')
b.append(iv(30,170,yb,'PR 0.12–0.20 s',AZUL))
b.append(iv(170,232,yb+28,'QRS < 0.12 s',ROJO))
b.append(iv(170,450,yb+56,'QT (depende de la FC)',MOR))
b.append(iv(232,300,BL-60,'segmento ST',VERDE))
b.append(T(ex(0)+4,BL+20,'línea isoeléctrica',12,GRIS,'start'))
b.append(box(690,70,200,90,'#fff','#ddd',8,1)); b.append(TL(700,90,['P = despolarización auricular','QRS = despolarización ventricular','T = repolarización ventricular','(la repolarización auricular','queda escondida en el QRS)'],12.5,'#222','start'))
b.append(T(60,410,'Papel: cuadro chico = 0.04 s y 0.1 mV · cuadro grande = 0.20 s y 0.5 mV (escala del dibujo ampliada para ver las ondas)',11.5,GRIS,'start'))
svg(FI,'ecg.svg',W,H,''.join(b))

# ── Diagrama de Wiggers (ciclo cardiaco izquierdo)
W,H=960,770
b=[title(W,'Ciclo cardiaco (diagrama de Wiggers)')]
X0,XW=120,720
def tx(t): return X0+t/0.8*XW
fases=[(0,.10,'Sístole\nauricular','#fff4e6'),(.10,.15,'Contracción\nisovolumétrica','#ffe3e3'),(.15,.40,'Eyección','#fff0f0'),
       (.40,.48,'Relajación\nisovolumétrica','#e7f5ff'),(.48,.60,'Llenado\nrápido','#ebfbee'),(.60,.80,'Llenado lento\n(diástasis)','#f4fce3')]
for t1,t2,s_,c in fases:
    b.append(f'<rect x="{tx(t1):.1f}" y="52" width="{tx(t2)-tx(t1):.1f}" height="600" fill="{c}"/>')
    b.append(num((tx(t1)+tx(t2))/2,72,str(fases.index((t1,t2,s_,c))+1),'#444',11))
for t in (.10,.15,.40,.48): b.append(line(tx(t),52,tx(t),652,'#aaa',1.2,'4 3'))
b.append(T(tx(.125),112,'',1))
# ECG
def ey(v): return 140-v*0.45
ecg=[(0,0),(.02,0),(.04,8),(.06,0),(.085,0),(.09,-5),(.10,60),(.11,-12),(.12,0),(.25,0),(.29,14),(.33,0),(.8,0)]
ecg=[(t-0.06 if t>=0.06 else t,v) for t,v in ecg]
ecg=[(0,0),(.005,4),(.03,8),(.05,0),(.075,-4),(.085,60),(.095,-12),(.105,0),(.24,0),(.29,16),(.34,0),(.78,0),(.8,4)]
b.append(path(smooth([(tx(t),ey(v)) for t,v in ecg],.2),'#111',2.2))
b.append(T(X0-10,ey(0)+4,'ECG',13,'#111','end','bold'))
b.append(T(tx(.03),ey(8)-6,'P',12,'#111',w='bold')); b.append(T(tx(.085),ey(60)-4,'QRS',12,'#111',w='bold')); b.append(T(tx(.29),ey(16)-6,'T',12,'#111',w='bold'))
# Presiones
PY0=470
def py(p): return PY0-p*2.3
b.append(line(X0,PY0,X0+XW,PY0,'#222',1.6)); b.append(line(X0,PY0,X0,py(135),'#222',1.6))
for p in (0,20,40,60,80,100,120): b.append(T(X0-8,py(p)+4,str(p),11.5,GRIS,'end')); b.append(line(X0,py(p),X0+XW,py(p),'#e3e3e3',.8))
b.append(TR(X0-48,py(65),'Presión (mmHg)',13))
ao=[(0,86),(.05,84),(.10,82),(.15,80),(.20,108),(.26,120),(.32,116),(.40,100),(.41,94),(.43,99),(.50,94),(.60,89),(.70,85),(.80,82)]
lv=[(0,4),(.04,6),(.08,10),(.10,10),(.125,40),(.15,80),(.20,110),(.26,122),(.32,117),(.40,100),(.43,55),(.46,12),(.48,4),(.52,2),(.60,3),(.70,4),(.80,5)]
la=[(0,5),(.04,9),(.08,7),(.11,5),(.13,8),(.17,3),(.30,7),(.40,11),(.47,13),(.52,6),(.60,4),(.70,5),(.80,6)]
b.append(path(smooth([(tx(t),py(p)) for t,p in ao],.4),'#c92a2a',3))
b.append(path(smooth([(tx(t),py(p)) for t,p in lv],.4),'#1864ab',3.2))
b.append(path(smooth([(tx(t),py(p)) for t,p in la],.4),'#2f9e44',2.6))
b.append(T(tx(.70),py(88)-8,'Aorta',13,'#c92a2a','start','bold'))
b.append(T(tx(.28),py(124)-4,'Ventrículo izquierdo',13,'#1864ab','start','bold'))
b.append(T(tx(.64),py(5)-10,'Aurícula izquierda',13,'#2f9e44','start','bold'))
b.append(T(tx(.42),py(94)+16,'muesca dicrota',11,'#c92a2a','start'))
for t,p,s_,dx,dy,anc in [(.15,80,'abre la aórtica',-6,-8,'end'),(.40,100,'cierra la aórtica',6,-26,'start'),(.10,10,'cierra la mitral',-6,-34,'end'),(.48,4,'abre la mitral',6,-16,'start')]:
    b.append(circ(tx(t),py(p),5,'#fff','#111',2)); b.append(T(tx(t)+dx,py(p)+dy,s_,11.5,'#111',anc,'bold'))
for t,p,s_ in [(.04,9,'a'),(.13,8,'c'),(.47,13,'v')]: b.append(T(tx(t),py(p)-8,s_,12,'#2f9e44',w='bold'))
# Volumen
VY0=600
def vy(v): return VY0-(v-40)*1.0
b.append(line(X0,VY0,X0+XW,VY0,'#222',1.6)); b.append(line(X0,VY0,X0,vy(135),'#222',1.6))
for v in (50,80,120): b.append(T(X0-8,vy(v)+4,str(v),11.5,GRIS,'end'))
b.append(TR(X0-48,vy(88),'Volumen VI (mL)',13))
vol=[(0,110),(.05,114),(.10,120),(.15,120),(.20,96),(.28,68),(.35,54),(.40,50),(.48,50),(.53,80),(.60,100),(.70,106),(.80,110)]
b.append(path(poly([(tx(t),vy(v)) for t,v in vol]) if False else smooth([(tx(t),vy(v)) for t,v in vol],.3),'#5f3dc4',3))
b.append(T(tx(.15)+6,vy(120)-6,'telediastólico 120 mL',11.5,'#5f3dc4','start','bold'))
b.append(T(tx(.40)+4,vy(50)-8,'telesistólico 50 mL',11.5,'#5f3dc4','start','bold'))
# Ruidos
SY=630
for t,s_ in [(.10,'R1'),(.40,'R2')]:
    for k in range(5): b.append(line(tx(t)-8+k*4,SY-8+(k%2)*4,tx(t)-8+k*4,SY+8-(k%2)*4,'#333',2))
    b.append(T(tx(t),SY+26,s_,13,'#333',w='bold'))
b.append(T(X0-10,SY+4,'Ruidos',13,'#111','end','bold'))
for t in range(0,9,2): b.append(T(tx(t/10),668,f'{t/10:.1f} s',11.5,GRIS))
for i,(t1,t2,s_,c) in enumerate(fases):
    xx=X0+(i%3)*250; yy=690+(i//3)*20
    b.append(num(xx,yy-4,str(i+1),'#444',8)); b.append(T(xx+12,yy,s_.replace('\n',' '),12,'#333','start'))
b.append(T(tx(.4),752,'R1 = cierre de mitral y tricúspide · R2 = cierre de aórtica y pulmonar · VS = 120 − 50 = 70 mL · FE ≈ 58 %',12,'#333'))
svg(FI,'wiggers.svg',W,H,''.join(b))

# ── Asa presión-volumen del VI
def edp(V): return 2+9*max(V-40,0)**2/80**2
def asa(Vd,Vs,Pab,Pci,Ppk):
    sv=Vd-Vs
    fill=[(Vs+(Vd-Vs)*i/10, max(edp(Vs+(Vd-Vs)*i/10),3)) for i in range(11)]
    ej=[(Vd,Pab),(Vd-.12*sv,Ppk-8),(Vd-.45*sv,Ppk),(Vd-.8*sv,Ppk-6),(Vs,Pci)]
    return fill, ej
W,H=900,520
b=[title(W,'Asa presión-volumen del ventrículo izquierdo')]
X0,Y0=110,440
def vx(v): return X0+v*3.6
def pyy(p): return Y0-p*2.6
b.append(axes(X0,Y0,X0+560,80,'Volumen del ventrículo izquierdo (mL)','Presión (mmHg)'))
for v in range(0,151,25): b.append(T(vx(v),Y0+18,str(v),12,GRIS))
for p in range(0,141,20): b.append(T(X0-8,pyy(p)+4,str(p),12,GRIS,'end'))
fill,ej=asa(120,50,80,100,124)
b.append(path(smooth([(vx(v),pyy(p)) for v,p in [(x,edp(x)) for x in range(40,156,5)]],.4),'#888',1.8,dash='6 4'))
b.append(T(vx(150)+10,pyy(edp(150))-24,'relación telediastólica',11.5,'#777','end'))
b.append(path(poly([(vx(5),pyy(0)),(vx(62),pyy(127))]),'#888',1.8,dash='6 4')); b.append(TL(vx(58)-8,pyy(128)-4,['relación telesistólica','(contractilidad)'],11.5,'#777','end'))
loop=smooth([(vx(v),pyy(p)) for v,p in fill],.4)+' L'+f'{vx(120):.1f},{pyy(80):.1f}'+smooth([(vx(v),pyy(p)) for v,p in ej],.5)[1+len(f"{vx(120):.1f},{pyy(80):.1f}"):]+f' L{vx(50):.1f},{pyy(fill[0][1]):.1f}Z'
b.append(path(loop,'#1864ab',3.4,'#e7f1fb'))
for v,p,s_ ,dx,dy,anc in [(50,3,'A · abre la mitral',-10,-6,'end'),(120,edp(120),'B · cierra la mitral',8,16,'start'),(120,80,'C · abre la aórtica',10,4,'start'),(50,100,'D · cierra la aórtica',-10,-6,'end')]:
    b.append(circ(vx(v),pyy(p),6,'#fff','#111',2.2)); b.append(T(vx(v)+dx,pyy(p)+dy,s_,12.5,'#111',anc,'bold'))
b.append(num(vx(85),pyy(18),'1',AZUL,11)); b.append(num(vx(120)+16,pyy(45),'2',AZUL,11)); b.append(num(vx(85),pyy(108),'3',AZUL,11)); b.append(num(vx(50)-16,pyy(50),'4',AZUL,11))
leg=['1  Llenado diastólico (A→B)','2  Contracción isovolumétrica (B→C)','3  Eyección (C→D)','4  Relajación isovolumétrica (D→A)']
for i,s_ in enumerate(leg): b.append(T(690,140+i*24,s_,12.5,'#222','start'))
b.append(arrow(vx(85),pyy(60),vx(120)-4,pyy(60),'#5f3dc4',2,9)); b.append(arrow(vx(85),pyy(60),vx(50)+4,pyy(60),'#5f3dc4',2,9)); b.append(T(vx(85),pyy(60)-8,'Volumen latido = 70 mL',12.5,'#5f3dc4',w='bold'))
b.append(TL(690,270,['El área dentro del asa','es el trabajo sistólico.','','FE = VS / VTD','= 70 / 120 ≈ 58 %'],12.5,'#222','start'))
svg(FI,'presion-volumen.svg',W,H,''.join(b))

# ── Qué le pasa al asa con precarga, poscarga y contractilidad
W,H=960,380
b=[title(W,'Cómo cambia el asa presión-volumen')]
def mini(x0,ttl,col,new,note,esl=None):
    o=[T(x0+140,62,ttl,15,col,w='bold')]
    def X(v): return x0+20+v*1.7
    def Y(p): return 320-p*1.6
    o.append(arrow(x0+20,320,x0+290,320,'#222',1.6,8)); o.append(arrow(x0+20,320,x0+20,80,'#222',1.6,8))
    o.append(T(x0+155,340,'Volumen',12,GRIS)); o.append(TR(x0+6,200,'Presión',12,GRIS))
    for (Vd,Vs,Pab,Pci,Ppk),c,w_,da in (((120,50,80,100,124),'#999',2.2,'6 4'),(new,col,3,'')):
        f_,e_=asa(Vd,Vs,Pab,Pci,Ppk)
        d=smooth([(X(v),Y(p)) for v,p in f_],.4)+' L'+' '.join(f'{X(v):.1f},{Y(p):.1f}' for v,p in e_[:1])+' '+smooth([(X(v),Y(p)) for v,p in e_],.5).replace('M','L',1)+f' L{X(Vs):.1f},{Y(f_[0][1]):.1f}Z'
        o.append(path(d,c,w_,'none',da))
    if esl: o.append(path(poly([(X(esl[0][0]),Y(esl[0][1])),(X(esl[1][0]),Y(esl[1][1]))]),col,1.6,dash='5 4'))
    o.append(TL(x0+150,358,note,12,'#333'))
    return ''.join(o)
b.append(mini(20,'↑ Precarga',VERDE,(145,52,80,100,128),['VTD ↑ → volumen latido ↑']))
b.append(mini(340,'↑ Poscarga',ROJO,(120,72,112,122,142),['la aórtica abre a más presión → VS ↓']))
b.append(mini(660,'↑ Contractilidad',AZUL,(120,32,80,98,136),['VTS ↓ → VS y FE ↑'],((0,0),(52,148))))
b.append(T(W/2,H-4,'Gris punteado = asa normal',11.5,GRIS))
svg(FI,'pv-cambios.svg',W,H,''.join(b))

# ── Frank-Starling
W,H=820,420
b=[title(W,'Ley de Frank-Starling')]
X0,Y0=100,350
b.append(axes(X0,Y0,X0+560,70,'Precarga (volumen telediastólico)','Volumen latido'))
def fs(x,vm,k): return vm*(1-math.exp(-x/k))
def cur(vm,k): return [(X0+x*5.2, Y0-fs(x,vm,k)) for x in range(0,106,3)]
b.append(path(smooth(cur(250,28),.4),AZUL,3)); b.append(T(X0+548,Y0-250-4,'↑ Contractilidad (simpático, digoxina, dobutamina)',12.5,AZUL,'end','bold'))
b.append(path(smooth(cur(185,30),.4),VERDE,3.4)); b.append(T(X0+548,Y0-185-8,'Normal',13,VERDE,'end','bold'))
b.append(path(smooth(cur(100,34),.4),ROJO,3)); b.append(T(X0+548,Y0-100-8,'Insuficiencia cardiaca (FE ↓)',12.5,ROJO,'end','bold'))
for xx,vm,k,c in ((40,185,30,VERDE),(70,100,34,ROJO)):
    b.append(circ(X0+xx*5.2,Y0-fs(xx,vm,k),6,c))
b.append(arrow(X0+42*5.2,Y0-fs(40,185,30)+4,X0+68*5.2,Y0-fs(70,100,34)-8,'#555',2,9,'5 4'))
b.append(TL(X0+300,Y0-40,['La IC se mueve a la derecha y abajo:','más volumen (congestión) con menos gasto'],12,'#555','start'))
b.append(TL(X0+20,95,['A más estiramiento, más fuerza…','hasta un límite (meseta).'],12.5,'#333','start'))
svg(FI,'frank-starling.svg',W,H,''.join(b))

# ── Fuerzas de Starling en el capilar
W,H=920,430
b=[title(W,'Fuerzas de Starling a lo largo del capilar')]
b.append(f'<rect x="40" y="60" width="840" height="300" rx="16" fill="#fff9db"/>'); b.append(T(60,84,'Intersticio',13,'#a07800','start','bold'))
b.append(path('M120,170 L800,170 L800,250 L120,250Z','#c92a2a',0,'url(#gcap)'))
b.insert(1,'<defs><linearGradient id="gcap" x1="0" x2="1"><stop offset="0" stop-color="#ffa8a8"/><stop offset="1" stop-color="#a5b4fc"/></linearGradient></defs>')
b.append(line(120,170,800,170,'#862e9c',2.4)); b.append(line(120,250,800,250,'#862e9c',2.4))
b.append(T(120,280,'Extremo arterial',13,ROJO,'start','bold')); b.append(T(800,280,'Extremo venoso',13,AZUL,'end','bold'))
b.append(arrow(60,210,118,210,ROJO,3)); b.append(arrow(802,210,860,210,AZUL,3))
b.append(T(460,215,'albúmina retiene el agua: presión oncótica ≈ 25 mmHg (igual en todo el capilar)',12.5,'#333'))
for x,ph,col in ((200,35,ROJO),(460,25,'#7048e8'),(720,15,AZUL)):
    b.append(T(x,196,f'Pc {ph} mmHg',12.5,col,w='bold'))
# flechas netas
for x in (170,230,290): b.append(arrow(x,168,x,110,ROJO,3,10))
b.append(T(230,100,'Filtración neta (sale líquido)',13,ROJO,w='bold'))
for x in (650,710,770): b.append(arrow(x,110,x,166,AZUL,3,10))
b.append(T(710,100,'Reabsorción neta (regresa)',13,AZUL,w='bold'))
b.append(path('M380,310 C430,290 500,290 560,310','#2f9e44',10)); b.append(T(470,340,'Linfáticos: recogen el ~10 % que no regresa',12.5,'#2f9e44',w='bold'))
b.append(arrow(470,262,470,296,'#2f9e44',2.4,9))
b.append(TL(460,384,['Edema = ↑ presión hidrostática (IC) · ↓ presión oncótica (nefrótico, cirrosis)','· ↑ permeabilidad (sepsis, quemaduras) · obstrucción linfática'],12.5,'#333'))
svg(FI,'starling-capilar.svg',W,H,''.join(b))

# ── Volúmenes y capacidades pulmonares (espirograma)
W,H=940,500
b=[title(W,'Volúmenes y capacidades pulmonares')]
X0,Y0=90,420
def ly(L): return Y0-L*58
def lt(t): return X0+t*45
b.append(arrow(X0,Y0,X0+560,Y0,'#222',2,9)); b.append(arrow(X0,Y0,X0,ly(6.6),'#222',2,9))
for L in range(0,7): b.append(T(X0-8,ly(L)+4,str(L),12,GRIS,'end')); b.append(line(X0,ly(L),X0+540,ly(L),'#eee',1))
b.append(TR(X0-40,ly(3),'Volumen (L)',14)); b.append(T(X0+270,Y0+28,'Tiempo',13,GRIS))
pts=[]
for i in range(0,61):
    t=i*0.05; pts.append((t,2.4+0.25*(1-math.cos(2*math.pi*t/1.0))))
pts+= [(3.4,2.9),(3.9,5.2),(4.3,6.0),(4.6,5.7),(5.2,2.6),(5.7,1.2),(6.0,1.3),(6.6,2.4)]
for i in range(1,61):
    t=6.6+i*0.05; pts.append((t,2.4+0.25*(1-math.cos(2*math.pi*(t-6.6)/1.0))))
b.append(path(smooth([(lt(t),ly(L)) for t,L in pts],.35),AZUL,2.8))
# volúmenes (izquierda de las barras)
bx=660
vols=[(0,1.2,'Volumen residual','1.2 L','#adb5bd'),(1.2,2.4,'Reserva espiratoria','1.2 L','#74c0fc'),(2.4,2.9,'Volumen corriente','0.5 L','#63e6be'),(2.9,6.0,'Reserva inspiratoria','3.1 L','#ffd8a8')]
for a,z,n,v,c in vols:
    b.append(f'<rect x="{bx}" y="{ly(z):.1f}" width="46" height="{ly(a)-ly(z):.1f}" fill="{c}" stroke="#fff" stroke-width="2"/>')
    b.append(T(bx-8,(ly(a)+ly(z))/2-1,n,12,'#222','end','bold')); b.append(T(bx-8,(ly(a)+ly(z))/2+14,v,11.5,GRIS,'end'))
caps=[(0,6.0,'CPT 6 L',870),(1.2,6.0,'Capacidad vital 4.8 L',820),(2.4,6.0,'Cap. inspiratoria 3.6 L',770),(0,2.4,'CRF 2.4 L',770)]
for a,z,n,x in caps:
    b.append(brace_v(x-50,ly(z)+2,ly(a)-2,'#5f3dc4',True,7)); b.append(TR(x-20,(ly(a)+ly(z))/2,n,12,'#5f3dc4','bold'))
b.append(T(bx+23,Y0+20,'',1))
b.append(TL(X0+10,470,['CPT = capacidad pulmonar total · CRF = capacidad residual funcional','El volumen residual (y por eso CRF y CPT) no se mide con espirometría.'],12,'#333','start'))
svg(FI,'volumenes.svg',W,H,''.join(b))

# ── Curvas flujo-volumen
W,H=900,460
b=[title(W,'Curvas flujo-volumen: normal, obstructiva y restrictiva')]
X0,YM=90,250
def fvx(L): return X0+(8-L)*80      # volumen: 8 L a la izquierda → 0 a la derecha
def fy(f): return YM-f*18
b.append(arrow(X0,YM,X0+680,YM,'#222',2,9)); b.append(arrow(X0,fy(-6.5),X0,fy(10.5),'#222',2,9))
for L in range(7,-1,-1): b.append(T(fvx(L),fy(-6.5)+18,str(L),11.5,GRIS)); b.append(line(fvx(L),YM-4,fvx(L),YM+4,'#222',1.5))
b.append(T(X0+340,fy(-6.5)+38,'Volumen pulmonar (L) →  menos aire',12.5,GRIS))
for f in (-6,-3,3,6,9): b.append(T(X0-8,fy(f)+4,str(f),11.5,GRIS,'end'))
b.append(TR(X0-42,fy(5),'Flujo espiratorio (L/s)',12.5)); b.append(TR(X0-42,fy(-3.5),'Inspiración',12))
def fv(tlc,rv,pk,scoop,col,lab,lx,ly_,w=3):
    fvc=tlc-rv; o=[]
    ex=[(tlc,0)]
    for i in range(1,41):
        v=tlc-fvc*i/40
        frac=i/40
        if frac<.12: f=pk*frac/.12
        else:
            q=(frac-.12)/.88; f=pk*(1-q)**(1+scoop)
        ex.append((v,f))
    ins=[(rv+fvc*i/30,-0.75*pk*math.sin(math.pi*i/30)) for i in range(1,31)]
    o.append(path(smooth([(fvx(v),fy(f)) for v,f in ex+ins],.3)+'Z',col,w))
    o.append(T(lx,ly_,lab,13,col,'start','bold'))
    return ''.join(o)
b.append(fv(6,1,9,0,'#2f9e44','Normal',fvx(5.9),fy(9)-8))
b.append(fv(7.6,3.6,5,1.6,ROJO,'Obstructiva',fvx(7.9),fy(5.2)-8))
b.append(fv(4.2,1.2,7.2,0,AZUL,'Restrictiva',fvx(3.9),fy(7.6)-6))
b.append(TL(640,70,['Obstructiva (asma, EPOC):','pico bajo, curva «excavada»,','aire atrapado (VR ↑)','','Restrictiva (fibrosis):','curva pequeña y angosta,','volúmenes ↓, FEV1/FVC normal'],12,'#333','start'))
svg(FI,'flujo-volumen.svg',W,H,''.join(b))

# ── Ventilación/perfusión del vértice a la base
W,H=900,440
b=[title(W,'Ventilación y perfusión: del vértice a la base (de pie)')]
b.append(path('M150,88 C120,92 96,140 84,200 C70,270 58,330 66,372 C74,396 120,392 170,382 C205,375 222,360 224,330 L222,150 C220,110 190,86 150,88Z','#2b6cb0',2.5,'url(#gvq)'))
b.insert(1,'<defs><linearGradient id="gvq" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#e7f5ff"/><stop offset="1" stop-color="#ff8787"/></linearGradient></defs>')
b.append(T(145,82,'Vértice',13,'#333',w='bold')); b.append(T(145,412,'Base',13,'#333',w='bold'))
b.append(TL(145,170,['alvéolos','grandes,','poco flujo'],11.5,'#1c4f80'))
b.append(TL(145,320,['más flujo','(gravedad)'],11.5,'#7a1010'))
X0,Y0=330,390
def hy(h): return Y0-h*280       # 0 base → 1 vértice
def qx(v): return X0+v*260
b.append(arrow(X0,Y0,X0+420,Y0,'#222',2,9)); b.append(arrow(X0,Y0,X0,hy(1.08),'#222',2,9))
b.append(T(X0+200,Y0+30,'Flujo por unidad de pulmón (relativo)',12.5,GRIS))
b.append(T(X0-8,hy(0)+4,'base',11.5,GRIS,'end')); b.append(T(X0-8,hy(1)+4,'vértice',11.5,GRIS,'end'))
Q=[(h,1.45-1.35*h) for h in [i/20 for i in range(21)]]
V=[(h,0.85-0.5*h) for h in [i/20 for i in range(21)]]
b.append(path(poly([(qx(q),hy(h)) for h,q in Q]),ROJO,3.2)); b.append(T(qx(1.45)-4,hy(.1),'Perfusión (Q)',13,ROJO,'start','bold'))
b.append(path(poly([(qx(v),hy(h)) for h,v in V]),AZUL,3.2)); b.append(T(qx(.85)-10,hy(0)-8,'Ventilación (V)',13,AZUL,'end','bold'))
for h,r in ((0.04,'≈ 0.6'),(.7,'≈ 1'),(1,'≈ 3')):
    b.append(tbox(X0+440,hy(h)-16,110,32,[f'V/Q {r}'],'#fff','#5f3dc4',13,'#5f3dc4','bold'))
b.append(TL(X0+300,hy(.42),['Vértice: V/Q alto','(TB y aire viven ahí)','Base: V/Q bajo'],12,'#333','start'))
svg(FI,'vq-pulmon.svg',W,H,''.join(b))

# ── Espectro V/Q: cortocircuito ↔ normal ↔ espacio muerto
W,H=960,360
b=[title(W,'Del cortocircuito al espacio muerto')]
def unidad(cx,kind,ttl,sub,col):
    o=[T(cx,64,ttl,15,col,w='bold'),T(cx,82,sub,12.5,GRIS)]
    o.append(arrow(cx,104,cx,140,'#1c7ed6' if kind!='shunt' else '#adb5bd',3,10))
    o.append(T(cx+12,118,'aire',11.5,'#1c7ed6' if kind!='shunt' else '#adb5bd','start'))
    fill='#ffffff' if kind!='shunt' else '#ffe8a1'
    o.append(circ(cx,190,46,fill,'#1c7ed6',3))
    if kind=='shunt':
        for k in range(6): o.append(path(f'M{cx-38},{176+k*7} q19,-6 38,0 q19,6 38,0','#e0a800',1.6))
        o.append(T(cx,195,'líquido / colapso',11,'#8a6d00',w='bold'))
    o.append(path(f'M{cx-110},270 C{cx-60},250 {cx+60},250 {cx+110},270','#c92a2a' if kind!='dead' else '#ced4da',16))
    if kind=='dead':
        o.append(circ(cx-20,256,13,'#495057')); o.append(T(cx-20,288,'émbolo',11.5,'#333',w='bold'))
    else:
        o.append(arrow(cx-90,300,cx+90,300,'#c92a2a',2.4,9)); o.append(T(cx,318,'sangre',11.5,'#c92a2a'))
    if kind=='normal':
        o.append(arrow(cx-14,236,cx-14,258,'#1c7ed6',2.4,8)); o.append(T(cx-4,250,'O₂',11,'#1c7ed6','start','bold'))
    return ''.join(o)
b.append(unidad(160,'shunt','Cortocircuito (shunt)','V/Q = 0',ROJO))
b.append(unidad(480,'normal','Unidad normal','V/Q ≈ 0.8',VERDE))
b.append(unidad(800,'dead','Espacio muerto','V/Q = ∞',AZUL))
b.append(T(160,346,'Neumonía, atelectasia, edema: NO mejora con O₂ 100 %',12,'#333'))
b.append(T(800,346,'Tromboembolia pulmonar',12,'#333'))
svg(FI,'vq-espectro.svg',W,H,''.join(b))

# ── La nefrona: qué hace cada segmento y dónde actúan los diuréticos
W,H=1000,660
b=[title(W,'La nefrona: qué hace cada segmento')]
b.append(f'<rect x="20" y="44" width="{W-40}" height="226" fill="#fff8f0"/>'); b.append(T(32,64,'CORTEZA',13,'#b26b2b','start','bold'))
b.append(f'<rect x="20" y="270" width="{W-40}" height="370" fill="#fdeee4"/>'); b.append(T(W-32,290,'MÉDULA',13,'#b26b2b','end','bold'))
CP='#d9480f'; CD='#1971c2'; CA='#2b8a3e'; CT='#9c36b5'; CC='#e67700'
GX,GY=330,140
b.append(circ(GX,GY,50,'#fff','#868e96',3))
for k in range(9):
    ang=k/9*2*math.pi; b.append(circ(GX+21*math.cos(ang),GY+21*math.sin(ang),12,'#ffc9c9','#c92a2a',1.6))
b.append(arrow(170,96,GX-46,GY-16,'#c92a2a',6,14)); b.append(T(70,90,'arteriola aferente',12,'#c92a2a','start','bold'))
b.append(arrow(GX-44,GY+18,170,186,'#a61e4d',4,12)); b.append(T(70,206,'arteriola eferente',12,'#a61e4d','start','bold'))
b.append(T(GX,GY+70,'Glomérulo: filtra ≈ 180 L/día',12,'#495057'))
tcp=[(GX+48,GY+8),(410,110),(450,90),(480,125),(445,160),(410,185),(440,215),(475,232),(490,262)]
b.append(path(smooth(tcp,.6),CP,12))
b.append(path('M490,262 L494,560 C496,610 556,610 558,560 L560,430',CD,8))
b.append(path('M560,430 L562,262',CA,13))
dct=[(562,262),(572,222),(610,200),(650,226),(675,200),(700,170),(726,180)]
b.append(path(smooth(dct,.5),CT,10))
b.append(circ(566,244,8,CA,'#fff',2)); b.append(T(580,286,'mácula densa',11,CA,'start','bold'))
b.append(path('M726,64 L726,620',CC,14)); b.append(arrow(726,604,726,646,CC,3,10)); b.append(T(740,640,'orina',12,CC,'start','bold'))
def etiqueta(x,y,w,h,col,tit,lines,pill=None):
    o=[box(x,y,w,h,'#fff',col,8,2.2), T(x+10,y+19,tit,13,col,'start','bold')]
    o+= [T(x+10,y+38+i*16,l,11.5,'#222','start') for i,l in enumerate(lines)]
    if pill:
        pw=len(pill)*6.6+18; o.append(box(x+w-pw-8,y+h-24,pw,18,'#fff4e6','#e8590c',9,1.5)); o.append(T(x+w-pw/2-8,y+h-11,pill,11,'#c2410c',w='bold'))
    return ''.join(o)
b.append(etiqueta(40,250,250,112,CP,'① Túbulo proximal',['~65 % del Na⁺ y del agua','toda la glucosa (SGLT2)','aminoácidos y HCO₃⁻'],'acetazolamida · iSGLT2'))
b.append(line(410,185,290,290,CP,1.5,'4 3'))
b.append(etiqueta(40,380,250,96,CD,'② Asa descendente',['permeable al AGUA, no a solutos:','el líquido se concentra al bajar'],None))
b.append(line(492,440,290,428,CD,1.5,'4 3'))
b.append(etiqueta(40,494,250,112,CA,'③ Rama ascendente gruesa',['NKCC2: Na⁺, K⁺, 2Cl⁻','IMPERMEABLE al agua','→ diluye el líquido'],'furosemida'))
b.append(line(561,340,290,540,CA,1.5,'4 3'))
b.append(etiqueta(760,70,225,112,CT,'④ Túbulo distal',['NCC: Na⁺ y Cl⁻','reabsorbe Ca²⁺ (PTH)','casi no reabsorbe agua'],'tiazidas'))
b.append(line(650,222,760,150,CT,1.5,'4 3'))
b.append(etiqueta(760,300,225,150,CC,'⑤ Túbulo colector',['Principal: ENaC (entra Na⁺,','sale K⁺) ↑ aldosterona','ADH → acuaporina 2 (agua)','Intercalada α: secreta H⁺'],'espironolactona · amilorida'))
b.append(line(726,380,760,380,CC,1.5,'4 3'))
svg(FI,'nefrona.svg',W,H,''.join(b))

# ── Mecanismo de contracorriente del asa de Henle
W,H=960,620
b=[title(W,'Asa de Henle: multiplicador por contracorriente')]
b.insert(1,'<defs><linearGradient id="gmed" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff8f0"/><stop offset="1" stop-color="#f08c4a"/></linearGradient></defs>')
b.append(f'<rect x="40" y="70" width="700" height="500" fill="url(#gmed)" rx="12"/>')
b.append(line(40,150,740,150,'#b26b2b',1.5,'6 4')); b.append(T(50,140,'Corteza',12,'#b26b2b','start','bold')); b.append(T(50,170,'Médula',12,'#b26b2b','start','bold'))
def ly2(o): return 150+(o-300)/900*400       # mOsm/kg → y
for o in (300,600,900,1200):
    b.append(T(760,ly2(o)+5,f'{o}',14,'#a1440f','start','bold'))
b.append(T(760,ly2(1200)+26,'mOsm/kg',12,'#a1440f','start')); b.append(T(760,92,'Intersticio',13,'#a1440f','start','bold'))
DX,AX,CX=230,330,560
b.append(path(f'M{DX},90 L{DX},520 C{DX},575 {AX},575 {AX},520 L{AX},90',CD,24,'none',extra=' stroke-opacity=".25"'))
b.append(path(f'M{DX},90 L{DX},520 C{DX},575 {AX},575 {AX},520',CD,4))
b.append(path(f'M{AX},520 L{AX},300','#5c940d',4)); b.append(path(f'M{AX},300 L{AX},90',CA,9))
b.append(arrow(DX,74,DX,110,CD,3,10)); b.append(arrow(AX,110,AX,72,CA,3,10))
for o,y in ((300,ly2(300)+30),(600,ly2(600)),(900,ly2(900)),(1200,ly2(1200)-20)):
    b.append(tbox(DX-74,y-14,58,26,[str(o)],'#fff',CD,13,CD,'bold'))
for o,y in ((1200,ly2(1200)-20),(900,ly2(900)),(600,ly2(600)),(400,ly2(450)),(100,110)):
    b.append(tbox(AX+16,y-14,58,26,[str(o)],'#fff',CA,13,CA,'bold'))
for y in (230,340,470): b.append(arrow(DX,y,DX-60,y,'#1c7ed6',2.4,9)); b.append(T(DX-62,y-6,'H₂O',11,'#1c7ed6','end','bold'))
for y in (180,250): b.append(arrow(AX,y,AX+90,y,'#2b8a3e',2.6,9)); b.append(T(AX+94,y+4,'NaCl (NKCC2)',11,'#2b8a3e','start','bold'))
b.append(T(DX,598,'Rama descendente',12.5,CD,w='bold')); b.append(T(DX,612,'solo sale agua',11.5,GRIS))
b.append(T(AX+40,598,'Rama ascendente',12.5,CA,w='bold')); b.append(T(AX+40,612,'solo salen solutos',11.5,GRIS))
# colector
b.append(path(f'M{CX},90 L{CX},560','#e67700',12))
b.append(arrow(CX,560,CX,600,'#e67700',3,10)); b.append(T(CX,92-8,'Túbulo colector',12.5,'#e67700',w='bold'))
for y in (220,320,420,500): b.append(arrow(CX,y,CX-56,y,'#1c7ed6',2.4,9))
b.append(T(CX-60,212,'H₂O',11,'#1c7ed6','end','bold'))
b.append(tbox(CX+20,250,150,62,['Con ADH','(acuaporina 2):','orina ≈ 1200'],'#fff','#e67700',12,'#a1440f','bold'))
b.append(tbox(CX+20,330,150,62,['Sin ADH','(diabetes insípida):','orina ≈ 50–100'],'#fff','#868e96',12,'#495057','bold'))
b.append(TL(CX+20,430,['La urea reciclada y','los vasa recta (que','también corren en','contracorriente) mantienen','el gradiente.'],11.5,'#333','start'))
svg(FI,'contracorriente.svg',W,H,''.join(b))

# ── Arteriolas glomerulares y TFG
W,H=980,330
b=[title(W,'Arteriolas del glomérulo y filtración glomerular')]
def glo(x0,aw,ew,ttl,tfg,col,cause):
    o=[T(x0+110,62,ttl,14,'#222',w='bold')]
    o.append(line(x0+10,160,x0+80,160,'#c92a2a',aw)); o.append(line(x0+140,160,x0+210,160,'#a61e4d',ew))
    o.append(circ(x0+110,160,32,'#ffe3e3','#c92a2a',2.5))
    for k in range(6): o.append(circ(x0+110+15*math.cos(k*1.05),160+15*math.sin(k*1.05),7,'#ffc9c9','#c92a2a',1.2))
    o.append(T(x0+40,200,'aferente',11,'#c92a2a')); o.append(T(x0+180,200,'eferente',11,'#a61e4d'))
    o.append(T(x0+110,238,tfg,16,col,w='bold')); o.append(TL(x0+110,262,cause,12,'#333'))
    return ''.join(o)
b.append(glo(10,24,12,'Dilatar la aferente','TFG ↑',VERDE,['prostaglandinas']))
b.append(glo(250,5,12,'Contraer la aferente','TFG ↓',ROJO,['AINE (quitan las','prostaglandinas)']))
b.append(glo(490,12,5,'Contraer la eferente','TFG ↑',VERDE,['angiotensina II']))
b.append(glo(730,12,22,'Dilatar la eferente','TFG ↓',ROJO,['IECA y ARA II']))
b.append(T(W/2,315,'«Triple whammy»: AINE + IECA/ARA II + diurético en un paciente deshidratado → lesión renal aguda',12.5,'#333'))
svg(FI,'arteriolas.svg',W,H,''.join(b))

# ── Reflejo barorreceptor
W,H=900,420
b=[title(W,'Reflejo barorreceptor: control de la presión latido a latido')]
nodes=[(450,90,'↓ Presión arterial','(p. ej., al ponerse de pie)',ROJO),
       (740,210,'↓ Estiramiento de barorreceptores','seno carotídeo (IX) · arco aórtico (X)',MOR),
       (450,330,'Bulbo (centro cardiovascular)','↑ simpático · ↓ vago',AZUL),
       (160,210,'Taquicardia, ↑ contractilidad','y vasoconstricción',CAFE)]
for x,y,t1,t2,c in nodes: b.append(tbox(x-150,y-32,300,64,[t1,t2],'#fff',c,13.5,c,'bold'))
b.append(arrow(600,104,700,170,'#555',2.6)); b.append(arrow(700,252,600,316,'#555',2.6)); b.append(arrow(300,316,200,252,'#555',2.6)); b.append(arrow(312,210,352,210,'#555',2.6))
b.append(T(456,214,'La presión se recupera',15,VERDE,w='bold'))
b.append(T(450,236,'(si el reflejo falla: hipotensión ortostática)',12,GRIS))
b.append(T(450,405,'Masaje del seno carotídeo = el reflejo al revés: ↑ vago → puede terminar una taquicardia supraventricular',12,'#333'))
svg(FI,'barorreflejo.svg',W,H,''.join(b))

# ── Ejes tiroideo y suprarrenal
W,H=900,520
b=[title(W,'Ejes hipotálamo-hipófisis con retroalimentación negativa')]
def eje(x,ttl,items,col,fb):
    o=[T(x,64,ttl,16,col,w='bold')]
    ys=[100,210,320,430]
    for (org,hor),y in zip(items,ys):
        o.append(tbox(x-110,y-26,220,52,[org],'#fff',col,14,col,'bold'))
        if hor: o.append(arrow(x,y+28,x,y+80,col,3,10)); o.append(T(x+12,y+60,hor,14,'#222','start','bold'))
    for y0,y1,dx in fb:
        o.append(path(f'M{x-112},{y0} C{x-112-dx},{y0} {x-112-dx},{y1} {x-112},{y1}',ROJO,2.2,dash='6 4'))
        o.append(arrow(x-125,y1+4,x-112,y1,ROJO,2.2,9))
    o.append(T(x-112-fb[0][2]+14,(fb[0][0]+fb[0][1])/2,'−',22,ROJO,'middle','bold'))
    return ''.join(o)
b.append(eje(250,'Eje tiroideo',[('Hipotálamo','TRH'),('Adenohipófisis','TSH'),('Tiroides','T4 (mucha) y T3'),('Tejidos: T4 → T3 (activa)',None)],AZUL,[(320,210,70),(320,100,110)]))
b.append(eje(650,'Eje suprarrenal',[('Hipotálamo','CRH'),('Adenohipófisis','ACTH'),('Corteza suprarrenal','cortisol'),('Tejidos: ↑ glucosa, antiinflamatorio',None)],MOR,[(320,210,70),(320,100,110)]))
b.append(T(450,500,'Lesión primaria (en la glándula): hormona final ↓ y hormona trópica ↑ · Lesión central: ambas ↓',12.5,'#333'))
svg(FI,'ejes.svg',W,H,''.join(b))

# ── Célula parietal
W,H=900,500
b=[title(W,'Célula parietal: cómo se secreta el ácido')]
b.append(path('M240,110 L660,110 L660,390 L240,390Z','#1971c2',2.5,'#e7f5ff'))
b.append(T(250,96,'Luz del estómago (apical)',13,'#1971c2','start','bold'))
b.append(f'<ellipse cx="450" cy="250" rx="120" ry="55" fill="#d0ebff" stroke="#1971c2" stroke-width="1.5"/>'); b.append(T(450,248,'AMPc / Ca²⁺',14,'#1864ab',w='bold')); b.append(T(450,268,'(señal dentro de la célula)',12,GRIS))
b.append(f'<ellipse cx="450" cy="112" rx="58" ry="22" fill="#ffd8a8" stroke="#e8590c" stroke-width="2.4"/>'); b.append(T(450,117,'H⁺/K⁺-ATPasa',12.5,'#c2410c',w='bold'))
b.append(arrow(424,92,410,46,ROJO,2.6,9)); b.append(T(402,50,'H⁺',14,ROJO,'end','bold'))
b.append(arrow(492,46,478,90,AZUL,2.6,9)); b.append(T(500,50,'K⁺',14,AZUL,'start','bold'))
b.append(box(568,100,24,24,'#d3f9d8','#2f9e44',5)); b.append(arrow(580,98,580,50,'#2f9e44',2.4,9)); b.append(T(590,52,'Cl⁻',14,'#2f9e44','start','bold'))
b.append(tbox(672,58,210,32,['IBP (omeprazol) la bloquean'],'#fff4e6','#e8590c',12,'#c2410c','bold'))
b.append(T(226,60,'H⁺ + Cl⁻ = HCl',13,'#333','end','bold'))
b.append(arrow(450,194,450,138,'#555',2.6,10))
for x,nom,lig,blo,c in ((320,'M3','Acetilcolina (vago)','anticolinérgicos',MOR),(450,'CCK-B','Gastrina (células G)','',VERDE),(580,'H2','Histamina (ECL)','famotidina',AZUL)):
    b.append(box(x-32,374,64,32,'#fff',c,8,2.4)); b.append(T(x,395,nom,13,c,w='bold'))
    b.append(arrow(x,372,x if x==450 else x+(450-x)*.35,306,c,2.4,9))
    b.append(T(x,428,lig,12,'#222',w='bold')); b.append(T(x,444,f'bloqueo: {blo}' if blo else ' ',11.5,GRIS))
b.append(T(450,478,'Sangre (basolateral)',13,ROJO,w='bold'))
b.append(TL(680,300,['HCO₃⁻ sale a','la sangre al','secretar ácido:','«marea alcalina»'],12,'#333','start'))
b.append(arrow(640,350,700,380,'#555',2,9))
b.append(TL(220,230,['También','produce el','factor intrínseco','(para la B12)'],12,'#333','end'))
svg(FI,'celula-parietal.svg',W,H,''.join(b))

# ── Tubo digestivo: hormonas y sitios de absorción
W,H=960,470
b=[title(W,'Dónde se secreta y dónde se absorbe cada cosa')]
seg=[('Estómago',80,250,'#ffc9c9',['Gastrina (G, antro): ↑ ácido','HCl y factor intrínseco']),
     ('Duodeno',250,420,'#ffe8cc',['CCK (I): vesícula y enzimas','Secretina (S): HCO₃⁻','GIP (K): incretina']),
     ('Yeyuno',420,620,'#fff3bf',['Motilina (M): complejo','motor migratorio']),
     ('Íleon',620,830,'#d3f9d8',['Íleon terminal'])]
for n,x0,x1,c,h in seg:
    b.append(box(x0,190,x1-x0-6,70,c,'#868e96',18,1.6)); b.append(T((x0+x1-6)/2,232,n,16,'#333',w='bold'))
    for i,l in enumerate(h): b.append(T((x0+x1-6)/2,110+i*18,l,12,'#222',w='bold' if i==0 else 'normal'))
b.append(T(90,80,'SECRECIÓN',12,'#868e96','start','bold')); b.append(T(90,300,'ABSORCIÓN',12,'#868e96','start','bold'))
b.append(arrow(830,225,900,225,'#868e96',3)); b.append(T(905,230,'colon',12,GRIS,'start'))
abso=[(335,['Hierro (Fe²⁺)','Calcio']),(520,['Folato','Glucosa (SGLT1)','Aminoácidos','Grasas (micelas)']),(725,['Vitamina B12','Sales biliares (~95 %)'])]
for x,ls in abso:
    b.append(arrow(x,262,x,316,VERDE,2.6,9))
    for i,l in enumerate(ls): b.append(T(x,338+i*18,l,13,VERDE,w='bold'))
b.append(T(480,450,'Resección de íleon o Crohn ileal → déficit de B12 y diarrea por sales biliares',12.5,'#333'))
svg(FI,'tubo-digestivo.svg',W,H,''.join(b))

import shutil
for src,dst in (('simulacion-iii/gasometria.svg','fisiologia/gasometria.svg'),('simulacion-iii/agua-corporal.svg','anatomofisiologia/agua-corporal.svg')):
    os.makedirs(os.path.join(HERE,'img',os.path.dirname(dst)),exist_ok=True)
    shutil.copyfile(os.path.join(HERE,'img',src),os.path.join(HERE,'img',dst))

# ═════════════════════════ ANATOMOFISIOLOGÍA (1º) ═════════════════════════
# ── Homeostasis: asa de control
W,H=960,430
b=[title(W,'Homeostasis: retroalimentación negativa y positiva')]
b.append(T(250,64,'Negativa: corrige el cambio (termorregulación)',14,AZUL,w='bold'))
ns=[(250,110,'Estímulo','↑ temperatura corporal',ROJO),(395,200,'Receptor','termorreceptores de la piel',MOR),
    (250,290,'Centro integrador','hipotálamo',AZUL),(105,200,'Efector','sudor y vasodilatación',VERDE)]
for x,y,t1,t2,c in ns: b.append(tbox(x-95,y-30,190,60,[t1,t2],'#fff',c,12,c,'bold'))
b.append(arrow(346,124,380,166,'#555',2.4)); b.append(arrow(380,234,346,276,'#555',2.4)); b.append(arrow(154,276,120,234,'#555',2.4))
b.append(path('M105,168 C105,125 120,110 150,110','#2f9e44',2.6,dash='6 4')); b.append(arrow(140,110,152,110,'#2f9e44',2.6,10))
b.append(T(128,150,'−',26,'#2f9e44','middle','bold'))
b.append(TL(250,350,['La respuesta se OPONE al cambio y regresa','al punto de ajuste (glucemia, presión, temperatura).'],12.5,'#333'))
b.append(line(500,60,500,410,'#ddd',1.5,'5 5'))
b.append(T(730,64,'Positiva: amplifica hasta un desenlace (parto)',14,ROJO,w='bold'))
ps=[(730,110,'La cabeza del bebé','estira el cuello uterino'),(730,190,'Nervios → hipotálamo','→ neurohipófisis'),(730,270,'Oxitocina','contracciones más fuertes')]
for x,y,t1,t2 in ps: b.append(tbox(x-120,y-28,240,56,[t1,t2],'#fff',ROJO,12.5,ROJO,'bold'))
b.append(arrow(730,138,730,160,'#555',2.4)); b.append(arrow(730,218,730,240,'#555',2.4))
b.append(path('M850,270 C905,270 905,110 850,110','#c92a2a',2.6,dash='6 4')); b.append(arrow(870,110,852,110,'#c92a2a',2.6,10)); b.append(T(915,194,'+',26,ROJO,'middle','bold'))
b.append(TL(730,350,['El ciclo se refuerza hasta que nace el bebé.','Otros: coagulación, pico de LH.'],12.5,'#333'))
svg(AF,'homeostasis.svg',W,H,''.join(b))

# ── Regiones abdominales y cuadrantes
W,H=920,470
b=[title(W,'Abdomen: 9 regiones y 4 cuadrantes')]
def torso(x0):
    return path(f'M{x0+40},70 C{x0+20},140 {x0+10},250 {x0+30},330 C{x0+60},420 {x0+330},420 {x0+360},330 C{x0+380},250 {x0+370},140 {x0+350},70Z','#868e96',2.5,'#fff4e6')
b.append(torso(30))
X1,X2,Y1,Y2=155,265,175,285
b.append(line(X1,80,X1,400,'#c2410c',2,'6 4')); b.append(line(X2,80,X2,400,'#c2410c',2,'6 4'))
b.append(line(50,Y1,370,Y1,'#c2410c',2,'6 4')); b.append(line(50,Y2,370,Y2,'#c2410c',2,'6 4'))
reg=[(100,130,['Hipocondrio','derecho']),(210,130,['Epigastrio']),(320,130,['Hipocondrio','izquierdo']),
     (100,232,['Flanco','derecho']),(210,232,['Mesogastrio','(umbilical)']),(320,232,['Flanco','izquierdo']),
     (100,335,['Fosa ilíaca','derecha']),(210,335,['Hipogastrio']),(320,335,['Fosa ilíaca','izquierda'])]
for x,y,ls in reg: b.append(TL(x,y,ls,12,'#333','middle','bold'))
b.append(T(210,446,'Líneas medioclaviculares, subcostal e intertubercular',11.5,GRIS))
b.append(torso(500))
b.append(line(695,80,695,400,'#1971c2',2.4)); b.append(line(520,232,870,232,'#1971c2',2.4)); b.append(circ(695,232,6,'#1971c2'))
for x,y,t1,t2 in ((610,160,'Superior derecho','hígado, vesícula'),(780,160,'Superior izquierdo','estómago, bazo'),(610,310,'Inferior derecho','apéndice, ciego'),(780,310,'Inferior izquierdo','sigmoides')):
    b.append(T(x,y,t1,12.5,'#1971c2',w='bold')); b.append(T(x,y+17,t2,11.5,'#333'))
b.append(T(695,446,'Líneas media y transumbilical (cruce en el ombligo)',11.5,GRIS))
b.append(T(210,62,'(derecha del paciente a la izquierda de la imagen)',11,GRIS)); b.append(T(695,62,'',1))
svg(AF,'regiones-abdomen.svg',W,H,''.join(b))

# ── Sistema nervioso autónomo
W,H=960,500
b=[title(W,'Sistema nervioso autónomo: simpático y parasimpático')]
# médula esquemática
b.append(box(440,60,80,400,'#f1f3f5','#868e96',30,2)); b.append(T(480,52,'SNC',12,GRIS,w='bold'))
segs=[('Tronco (III, VII, IX, X)',70,140,VERDE),('Torácica T1–T12',150,320,ROJO),('Lumbar L1–L2',320,370,ROJO),('Sacra S2–S4',390,450,VERDE)]
for n,y0,y1,c in segs:
    b.append(f'<rect x="446" y="{y0}" width="68" height="{y1-y0}" rx="8" fill="{c}" opacity=".18"/>'); b.append(TL(480,(y0+y1)/2-4,n.split(' ',1),11,c,'middle','bold'))
# simpático (izquierda): pre corta → ganglio paravertebral → post larga
b.append(T(220,72,'SIMPÁTICO: toracolumbar',15,ROJO,w='bold')); b.append(T(220,90,'«lucha o huida»',12,GRIS))
for i,y in enumerate((180,250,340)):
    b.append(line(446,y,360,y,ROJO,3)); b.append(circ(350,y,11,'#ffc9c9',ROJO,2)); b.append(line(339,y,200,y,ROJO,3,'7 4'))
b.append(T(400,170,'ACh',11,ROJO,w='bold')); b.append(T(240,170,'noradrenalina',11,ROJO,w='bold'))
b.append(TL(30,200,['Pupila: midriasis','Corazón: ↑ FC','Bronquios: dilata','Intestino: ↓','Glucosa: ↑'],12,'#333','start'))
b.append(T(350,210,'ganglio cerca',10.5,GRIS)); b.append(T(350,222,'de la médula',10.5,GRIS))
b.append(TL(220,400,['Pre corta y post larga.','Médula suprarrenal = ganglio','que suelta adrenalina a la sangre.'],11.5,'#333'))
# parasimpático (derecha): pre larga → ganglio cerca del órgano
b.append(T(740,72,'PARASIMPÁTICO: craneosacro',15,VERDE,w='bold')); b.append(T(740,90,'«reposo y digestión»',12,GRIS))
for y in (120,420):
    b.append(line(514,y,770,y,VERDE,3)); b.append(circ(780,y,11,'#d3f9d8',VERDE,2)); b.append(line(791,y,840,y,VERDE,3,'7 4'))
b.append(T(640,112,'ACh (pre larga)',11,VERDE,w='bold')); b.append(T(815,112,'ACh',11,VERDE,w='bold'))
b.append(T(780,152,'ganglio junto',10.5,GRIS)); b.append(T(780,164,'o dentro del órgano',10.5,GRIS))
b.append(TL(640,230,['Pupila: miosis','Corazón: ↓ FC (vago)','Bronquios: contrae','Intestino: ↑ motilidad','Vejiga: micción'],12,'#333','start'))
b.append(TL(740,460,['El vago (X) lleva ~75 % del parasimpático.'],11.5,'#333'))
svg(AF,'sna.svg',W,H,''.join(b))

# ── Doble circulación
W,H=900,530
b=[title(W,'Circulación pulmonar y sistémica')]
b.append(tbox(330,56,240,56,['Pulmones','(capilares: se oxigena)'],'#e7f5ff','#1971c2',13,'#1971c2','bold'))
b.append(tbox(330,420,240,56,['Cuerpo','(capilares: entrega O₂)'],'#fff4e6','#e8590c',13,'#c2410c','bold'))
# corazón: 4 cámaras
HX,HY=450,265
b.append(box(HX-130,HY-70,128,64,'#a5d8ff','#1971c2',10)); b.append(TL(HX-66,HY-42,['Aurícula','derecha'],12,'#1864ab','middle','bold'))
b.append(box(HX+2,HY-70,128,64,'#ffc9c9','#c92a2a',10)); b.append(TL(HX+66,HY-42,['Aurícula','izquierda'],12,'#a61e1e','middle','bold'))
b.append(box(HX-130,HY+4,128,74,'#74c0fc','#1971c2',10)); b.append(TL(HX-66,HY+36,['Ventrículo','derecho'],12,'#0b3d70','middle','bold'))
b.append(box(HX+2,HY+4,128,74,'#ff8787','#c92a2a',10)); b.append(TL(HX+66,HY+36,['Ventrículo','izquierdo'],12,'#6b0f0f','middle','bold'))

# vasos
b.append(path('M330,448 L220,448 Q200,448 200,428 L200,240 Q200,225 220,225 L312,225','#1971c2',5)); b.append(arrow(300,225,318,225,'#1971c2',5,12))
b.append(path('M318,305 L296,305 Q280,305 280,289 L280,100 Q280,84 296,84 L318,84','#fff',13))
b.append(path('M318,305 L296,305 Q280,305 280,289 L280,100 Q280,84 296,84 L318,84','#1971c2',5)); b.append(arrow(310,84,330,84,'#1971c2',5,12))
b.append(path('M570,84 L664,84 Q680,84 680,100 L680,209 Q680,225 664,225 L594,225','#c92a2a',5)); b.append(arrow(600,225,582,225,'#c92a2a',5,12))
b.append(path('M582,305 L604,305 Q620,305 620,321 L620,432 Q620,448 604,448 L586,448','#c92a2a',5)); b.append(arrow(590,448,572,448,'#c92a2a',5,12))
b.append(TL(205,130,['Arterias','pulmonares','(SIN O₂)'],12,'#1971c2','middle','bold'))
b.append(TL(130,330,['Venas cavas','(regresan','a la AD)'],12,'#1971c2','middle','bold'))
b.append(TL(770,140,['Venas pulmonares','(CON O₂)'],12,'#c92a2a','middle','bold'))
b.append(TL(710,370,['Aorta','(sale del VI)'],12,'#c92a2a','middle','bold'))
b.append(T(450,500,'Las ARTERIAS salen del corazón y las VENAS llegan, lleven o no oxígeno.',12.5,'#333'))
b.append(T(450,516,'Válvulas: tricúspide y pulmonar (lado derecho) · mitral y aórtica (lado izquierdo)',11.5,GRIS))
svg(AF,'circulacion.svg',W,H,''.join(b))

# ── Unión neuromuscular
W,H=900,440
b=[title(W,'Unión neuromuscular')]
b.append(path('M380,50 L380,110 C300,120 280,150 280,190 C280,232 330,246 450,246 C570,246 620,232 620,190 C620,150 600,120 520,110 L520,50','#7b3fa0',3,'#f3eafa'))
b.append(T(450,140,'Terminal de la motoneurona',13,MOR,w='bold'))
b.append(arrow(450,44,450,100,ROJO,3,10)); b.append(T(462,70,'potencial de acción',12,ROJO,'start','bold'))
import random as _r; _r.seed(5)
for (x,y) in [(350,190),(400,170),(450,196),(500,172),(550,192)]:
    b.append(circ(x,y,15,'#fff','#7b3fa0',2))
    for k in range(4): b.append(circ(x+_r.uniform(-7,7),y+_r.uniform(-7,7),2.4,NAR))
b.append(box(300,232,18,26,'#ffd43b','#c99700',4)); b.append(arrow(309,276,309,214,'#c99700',2.4,8)); b.append(T(296,290,'Ca²⁺ entra',11.5,'#a07800','end','bold'))
for (dx,dy) in [(-20,22),(0,30),(20,24),(-8,40),(12,42)]: b.append(circ(450+dx,248+dy,3,NAR))
b.append(T(560,284,'ACh',13,NAR,'start','bold'))
# placa motora con pliegues
d='M180,300 '+' '.join(f'L{x},300 L{x+8},330 L{x+16},300' for x in range(330,580,40))+' L720,300 L720,420 L180,420Z'
b.append(path(d,'#c92a2a',2.5,'#ffe3e3'))
for x in (370,450,530): b.append(box(x-14,290,28,18,'#ff8787','#c92a2a',4))
b.append(T(450,370,'Fibra muscular (placa motora)',13,'#a61e1e',w='bold'))
b.append(T(450,392,'Receptor nicotínico → entra Na⁺ → potencial de acción muscular',12,'#333'))
b.append(TL(650,170,['Miastenia gravis:','anticuerpos contra el','receptor nicotínico'],12,'#333','start'))
b.append(TL(130,170,['Botulínica: impide','liberar ACh'],12,'#333','end'))
b.append(T(620,330,'AChE degrada la ACh',11.5,ROJO,'start','bold'))
svg(AF,'union-neuromuscular.svg',W,H,''.join(b))

# ── Hipotálamo e hipófisis
W,H=920,490
b=[title(W,'Hipotálamo e hipófisis')]
b.append(path('M300,60 C420,40 560,50 620,90 C640,130 600,160 520,170 L400,170 C320,165 280,120 300,60Z','#7b3fa0',2.5,'#f3eafa'))
b.append(T(460,100,'HIPOTÁLAMO',15,MOR,w='bold')); b.append(T(460,120,'TRH · CRH · GnRH · GHRH · dopamina',12,'#333'))
b.append(T(460,140,'(y produce ADH y oxitocina)',11.5,GRIS))
# tallo
b.append(path('M440,170 L440,240 M500,170 L500,240','#7b3fa0',3))
for y in (190,210,230): b.append(line(445,y,470,y+6,'#c92a2a',1.5))
b.append(T(400,215,'sistema porta',11.5,'#c92a2a','end','bold'))
b.append(path('M510,175 L515,240','#7b3fa0',2,dash='4 3')); b.append(T(528,210,'axones',11.5,MOR,'start','bold'))
# adeno y neuro
b.append(f'<ellipse cx="400" cy="300" rx="110" ry="62" fill="#ffe8cc" stroke="#e8590c" stroke-width="2.5"/>'); b.append(T(400,292,'Adenohipófisis',14,'#c2410c',w='bold')); b.append(T(400,310,'(anterior)',11.5,GRIS))
b.append(f'<ellipse cx="560" cy="300" rx="62" ry="54" fill="#e5dbff" stroke="#7048e8" stroke-width="2.5"/>'); b.append(T(560,296,'Neurohipófisis',13,'#5f3dc4',w='bold')); b.append(T(560,312,'(posterior)',11.5,GRIS))
ad=[('FSH','gónadas'),('LH','gónadas'),('ACTH','suprarrenal'),('TSH','tiroides'),('Prolactina','mama'),('GH','hígado: IGF-1')]
for i,(h,t) in enumerate(ad):
    y=380+i*0; x=130+i*0
for i,(h,t) in enumerate(ad):
    x=60+i*0; y=0
cols=[(150,380),(150,410),(150,440),(330,380),(330,410),(330,440)]
for (h,t),(x,y) in zip(ad,cols):
    b.append(T(x,y,h,13,'#c2410c','end','bold')); b.append(T(x+8,y,'→ '+t,12,'#333','start'))
b.append(arrow(330,350,250,368,'#e8590c',2.2,9))
b.append(T(240,470-8,'',1))
b.append(T(700,390,'ADH → riñón (agua)',13,'#5f3dc4','start','bold')); b.append(T(700,414,'Oxitocina → útero y mama',13,'#5f3dc4','start','bold'))
b.append(arrow(612,320,694,384,'#7048e8',2.2,9))
b.append(T(240,472,'FLAT PiG: FSH, LH, ACTH, TSH, Prolactina, GH',12,'#c2410c','middle','bold'))
svg(AF,'hipofisis.svg',W,H,''.join(b))

# ── Corteza y médula suprarrenal
W,H=880,420
b=[title(W,'Glándula suprarrenal por capas: sal, azúcar y sexo')]
cx,cy=250,240
for r,c,n in ((170,'#ffe066',''),(130,'#ffa94d',''),(92,'#ff8787',''),(56,'#b197fc','')):
    b.append(circ(cx,cy,r,c,'#fff',3))
b.append(T(cx,cy+5,'Médula',13,'#3b2a7a',w='bold'))
rows=[('Cápsula',None,'',GRIS),('Zona glomerular','Aldosterona','SAL',CAFE),('Zona fasciculada','Cortisol','AZÚCAR','#d9480f'),('Zona reticular','Andrógenos','SEXO','#c92a2a'),('Médula','Adrenalina y noradrenalina','simpático','#5f3dc4')]
ys=[(cy-172,90),(cy-150,108),(cy-111,140),(cy-74,180),(cy-20,230)]
for (n,hrm,mn,c),(yp,ly) in zip(rows[1:],ys[1:]):
    b.append(line(cx+8,yp+16,470,ly,c,1.6,'4 3'))
    b.append(T(480,ly+4,n,14,c,'start','bold'))
    b.append(T(640,ly+4,hrm,13,'#222','start'))
    b.append(T(480,ly+22,f'«{mn}»',12,GRIS,'start'))
b.append(T(cx,cy-178,'cápsula',11.5,GRIS))
b.append(TL(480,330,['De afuera hacia adentro: G-F-R','«cuanto más profundo, más dulce».','La aldosterona la regula sobre todo la','angiotensina II (no la ACTH).'],12.5,'#333','start'))
svg(AF,'suprarrenal.svg',W,H,''.join(b))

# ── Ciclo menstrual
W,H=920,520
b=[title(W,'Ciclo ovárico y menstrual (28 días)')]
X0,XW=110,720
def dx(d): return X0+(d-1)/27*XW
fases=[(1,14,'Fase folicular','#e7f5ff'),(14,28,'Fase lútea (14 días)','#fff4e6')]
for a,z,n,c in fases:
    b.append(f'<rect x="{dx(a):.1f}" y="52" width="{dx(z)-dx(a):.1f}" height="420" fill="{c}"/>'); b.append(T((dx(a)+dx(z))/2,70,n,13,'#333',w='bold'))
b.append(line(dx(14),52,dx(14),472,'#e8590c',2,'6 4')); b.append(T(dx(14),88,'Ovulación (≈ día 14)',12,'#e8590c',w='bold'))
# Hormonas hipofisarias
HY0=230
def hy_(v): return HY0-v*1.2
LH=[(1,12),(6,12),(11,16),(13,40),(14,100),(15,40),(17,14),(28,10)]
FSH=[(1,22),(4,24),(8,16),(12,16),(14,40),(15,20),(18,10),(26,14),(28,22)]
b.append(path(smooth([(dx(d),hy_(v)) for d,v in LH],.4),'#1971c2',3)); b.append(T(dx(15)+8,hy_(92),'LH',13,'#1971c2','start','bold'))
b.append(path(smooth([(dx(d),hy_(v)) for d,v in FSH],.4),'#2f9e44',3)); b.append(T(dx(15.5)+6,hy_(28),'FSH',13,'#2f9e44','start','bold'))
b.append(T(X0-10,hy_(50),'Hipófisis',12,'#333','end','bold'))
# Hormonas ováricas
OY0=380
def oy(v): return OY0-v*1.1
E=[(1,10),(6,18),(10,50),(13,90),(14,70),(16,30),(21,55),(25,40),(28,10)]
P_=[(1,4),(13,4),(15,10),(18,60),(21,90),(24,60),(28,6)]
b.append(path(smooth([(dx(d),oy(v)) for d,v in E],.4),'#c2255c',3)); b.append(T(dx(12.6),oy(92)-6,'Estrógenos',13,'#c2255c','end','bold'))
b.append(path(smooth([(dx(d),oy(v)) for d,v in P_],.4),'#e67700',3)); b.append(T(dx(21),oy(92)-8,'Progesterona',13,'#e67700','middle','bold'))
b.append(T(X0-10,oy(50),'Ovario',12,'#333','end','bold'))
# endometrio
EY=440
endo=[(1,6),(5,4),(6,8),(14,24),(21,34),(27,30),(28,10)]
b.append(path(smooth([(dx(d),EY-v) for d,v in endo],.4)+f' L{dx(28):.1f},{EY} L{dx(1):.1f},{EY}Z','#c92a2a',1.5,'#ffc9c9'))
b.append(T(X0-10,EY-10,'Endometrio',12,'#333','end','bold'))
b.append(T(dx(3),EY+18,'menstruación',11.5,'#c92a2a',w='bold')); b.append(T(dx(9),EY+18,'proliferativa',11.5,'#333')); b.append(T(dx(21),EY+18,'secretora',11.5,'#333'))
for d in (1,7,14,21,28): b.append(T(dx(d),492,f'día {d}',11.5,GRIS))
b.append(T(W/2,512,'Ovulación = 14 días antes de la siguiente regla (ciclo de 32 días → día 18)',12.5,'#333'))
svg(AF,'ciclo-menstrual.svg',W,H,''.join(b))

for src,dst in (('fisiologia/nefrona.svg','anatomofisiologia/nefrona.svg'),('fisiologia/tubo-digestivo.svg','anatomofisiologia/tubo-digestivo.svg'),
                ('fisiologia-clinica/conduccion.webp','anatomofisiologia/conduccion.webp'),('fisiologia/volumenes.svg','anatomofisiologia/volumenes.svg')):
    shutil.copyfile(os.path.join(HERE,'img',src),os.path.join(HERE,'img',dst))
