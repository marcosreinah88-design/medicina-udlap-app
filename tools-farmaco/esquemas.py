# Esquemas propios (SVG, en español) para las guías de Farmacología Básica (3º) y Farmacología II (4º).
# Dibujados desde cero (no copian figuras de libros). Los datos siguen lo que dice cada guía.
# Uso: python3 tools-farmaco/esquemas.py      (escribe tools-farmaco/img/<guía>/*.svg)
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
F = 'font-family="Helvetica,Arial,sans-serif"'
ROJO='#b3261e'; VERDE='#00573c'; NAR='#f26b21'; AZUL='#2b6cb0'; MOR='#7b3fa0'; GRIS='#555'; AMA='#c98a00'; TEAL='#1c6b66'
CLARO={'v':'#e8f5ee','n':'#fdeee4','a':'#e6effa','r':'#fbe6e4','m':'#f1e8f7','g':'#f2f2f2','y':'#fff6d6','t':'#dceeeb'}

def svg(gid, name, w, h, body):
    d = os.path.join(HERE, 'img', gid); os.makedirs(d, exist_ok=True)
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {F}>'
         f'<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')
    open(os.path.join(d, name), 'w').write(s)
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def T(x,y,s,size=15,c='#222',anchor='middle',w='normal',it=False):
    st=' font-style="italic"' if it else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{c}" text-anchor="{anchor}" font-weight="{w}"{st}>{esc(s)}</text>'
def TL(x,y,lines,size=13,c='#222',anchor='middle',w='normal',lh=None):
    lh = lh or size*1.25
    return ''.join(T(x,y+i*lh,l,size,c,anchor,w) for i,l in enumerate(lines))
def line(x1,y1,x2,y2,c='#333',w=2,dash=''):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{da}/>'
def arrow(x1,y1,x2,y2,c='#333',w=2.5,head=10,dash=''):
    a = math.atan2(y2-y1, x2-x1)
    hx1 = x2-head*math.cos(a-.4); hy1 = y2-head*math.sin(a-.4)
    hx2 = x2-head*math.cos(a+.4); hy2 = y2-head*math.sin(a+.4)
    return (line(x1,y1,x2-head*.7*math.cos(a),y2-head*.7*math.sin(a),c,w,dash)
            +f'<path d="M{x2:.1f},{y2:.1f} L{hx1:.1f},{hy1:.1f} L{hx2:.1f},{hy2:.1f}Z" fill="{c}"/>')
def block(x1,y1,x2,y2,c=ROJO,w=3):
    # flecha de inhibición (termina en barra ⊣)
    a = math.atan2(y2-y1, x2-x1); px,py = -math.sin(a)*9, math.cos(a)*9
    return line(x1,y1,x2,y2,c,w,'6 4')+line(x2-px,y2-py,x2+px,y2+py,c,w+1)
def box(x,y,w,h,fill,stroke,r=10,sw=2,dash=''):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}/>'
def tbox(x,y,w,h,lines,fill,stroke,size=14,c='#222',wt='normal',r=10):
    if isinstance(lines,str): lines=[lines]
    n=len(lines); lh=size*1.25; y0=y+h/2-(n-1)*lh/2+size*.35
    return box(x,y,w,h,fill,stroke,r)+TL(x+w/2,y0,lines,size,c,'middle',wt,lh)
def drug(x,y,txt,c=ROJO,size=13,anchor='middle'):
    # píldora con el nombre del fármaco
    w=len(txt)*size*.56+18; h=size+11
    x0={'middle':x-w/2,'start':x,'end':x-w}[anchor]
    return box(x0,y-h/2,w,h,c,c,h/2,1)+T(x0+w/2,y+size*.36,txt,size,'#fff','middle','bold')
def circ(cx,cy,r,fill,stroke='none',sw=2): return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def path(d,stroke='#333',w=2,fill='none',dash=''):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{da}/>'
def poly(pts): return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)
def curve(fn, x0, x1, X, Y, n=160):
    return poly([(X(x0+(x1-x0)*i/n), Y(fn(x0+(x1-x0)*i/n))) for i in range(n+1)])
def axes(x0,y0,x1,y1,xl,yl):
    return (arrow(x0,y0,x1,y0,'#222',2,9)+arrow(x0,y0,x0,y1,'#222',2,9)
            +T((x0+x1)/2,y0+32,xl,13,'#222')
            +f'<text x="{x0-22}" y="{(y0+y1)/2}" font-size="13" fill="#222" text-anchor="middle" transform="rotate(-90 {x0-22} {(y0+y1)/2})">{esc(yl)}</text>')
def title(w,s,sub=None):
    o=T(w/2,30,s,19,VERDE,w='bold')
    if sub: o+=T(w/2,52,sub,13,GRIS)
    return o
def membrane(x1,x2,y,h=34,c='#e9c46a'):
    # bicapa lipídica esquemática
    o=[box(x1,y,x2-x1,h,'#fff7df','none',0,0)]
    for x in range(int(x1)+6,int(x2),12):
        o.append(circ(x,y+5,4.2,c)); o.append(circ(x,y+h-5,4.2,c))
        o.append(line(x-1.5,y+9,x-1.5,y+h/2-2,'#c9a54a',1.3)); o.append(line(x+1.5,y+9,x+1.5,y+h/2-2,'#c9a54a',1.3))
        o.append(line(x-1.5,y+h/2+2,x-1.5,y+h-9,'#c9a54a',1.3)); o.append(line(x+1.5,y+h/2+2,x+1.5,y+h-9,'#c9a54a',1.3))
    return ''.join(o)
def legend_drug(x,y,txt='= sitio donde actúa el fármaco'):
    return drug(x,y,'Fármaco',ROJO,12,'start')+T(x+82,y+4,txt,12,GRIS,'start')

# ═════════════════════════ FARMACOLOGÍA BÁSICA (3º) ═════════════════════════
G='farmacologia'

# 1. LADME
W,H=920,430
b=[title(W,'LADME: el viaje del fármaco por el organismo')]
b.append(tbox(20,90,150,70,['Forma','farmacéutica','(tableta)'],CLARO['g'],GRIS,13))
b.append(arrow(172,125,232,125,GRIS)); b.append(T(202,115,'L',16,NAR,w='bold'))
b.append(tbox(234,90,140,70,['Fármaco','disuelto en el','sitio de absorción'],CLARO['y'],AMA,13))
b.append(arrow(376,125,436,125,GRIS)); b.append(T(406,115,'A',16,NAR,w='bold'))
# plasma
b.append(box(438,70,230,180,CLARO['r'],ROJO,14))
b.append(T(553,94,'PLASMA',15,ROJO,w='bold'))
b.append(tbox(452,108,92,52,['Fármaco','libre'],'#fff',ROJO,13,ROJO,'bold'))
b.append(tbox(562,108,92,52,['Unido a','albúmina'],'#fff',GRIS,13))
b.append(arrow(544,128,560,128,GRIS,2,7)); b.append(arrow(560,142,546,142,GRIS,2,7))
b.append(T(553,186,'Solo el fármaco LIBRE',12,'#222')); b.append(T(553,202,'se distribuye, actúa,',12,'#222')); b.append(T(553,218,'se metaboliza y se elimina',12,'#222'))
# IV
b.append(arrow(553,44,553,70,AZUL,2.5)); b.append(T(565,60,'Vía IV: entra directo (sin L ni A, F = 100 %)',12,AZUL,'start','bold'))
# D
b.append(arrow(670,120,740,120,GRIS)); b.append(arrow(740,138,670,138,GRIS)); b.append(T(705,110,'D',16,NAR,w='bold'))
b.append(tbox(742,78,170,100,['Tejidos','sitio de acción','(receptor) y depósitos','(grasa, hueso)'],CLARO['v'],VERDE,13))
# M
b.append(arrow(520,252,430,318,GRIS)); b.append(T(462,280,'M',16,NAR,w='bold'))
b.append(tbox(300,320,200,80,['Hígado (CYP450)','Fase I y fase II','→ metabolitos más polares'],CLARO['n'],NAR,13))
# E
b.append(arrow(600,252,690,318,GRIS)); b.append(T(660,280,'E',16,NAR,w='bold'))
b.append(tbox(620,320,220,80,['Excreción','riñón (orina) · bilis (heces)','pulmón, sudor, leche'],CLARO['a'],AZUL,13))
b.append(arrow(502,360,618,360,GRIS,2,9))
b.append(T(20,415,'L liberación · A absorción · D distribución · M metabolismo · E excreción',13,GRIS,'start'))
svg(G,'ladme.svg',W,H,''.join(b))

# 2. Transporte a través de membranas
W,H=920,400
b=[title(W,'Cómo cruza un fármaco la membrana')]
b.append(T(30,96,'Exterior',13,GRIS,'start')); b.append(T(30,290,'Interior (citoplasma)',13,GRIS,'start'))
b.append(membrane(20,900,170,40))
cols=[(115,'Difusión pasiva','Liposolubles, no ionizados','a favor del gradiente, sin energía',VERDE),
      (290,'Filtración acuosa','Moléculas pequeñas e','hidrosolubles, por poros',AZUL),
      (465,'Difusión facilitada','Con transportador,','a favor del gradiente, sin ATP',TEAL),
      (640,'Transporte activo','Con transportador y ATP,','contra el gradiente (saturable)',NAR),
      (815,'Endocitosis','Macromoléculas:','la membrana las envuelve',MOR)]
for x,t,l1,l2,c in cols:
    b.append(T(x,72,t,14,c,w='bold'))
    b.append(TL(x,320,[l1,l2],12,'#333'))
# pasiva: muchas bolitas arriba, pocas abajo
x=115
for i,(dx,dy) in enumerate([(-30,110),(-10,125),(15,105),(30,130),(-25,145),(5,148)]): b.append(circ(x+dx,dy,6,VERDE))
for dx,dy in [(-12,240),(18,255)]: b.append(circ(x+dx,dy,6,VERDE))
b.append(arrow(x,150,x,238,VERDE,3))
# poro
x=290
b.append(box(x-14,168,28,44,'#fff','#7aa6d6',3,2))
for dy in (110,130,145): b.append(circ(x+(dy%3-1)*14,dy,4.5,AZUL))
b.append(arrow(x,120,x,250,AZUL,2.5)); b.append(circ(x+10,252,4.5,AZUL))
# facilitada
x=465
b.append(f'<path d="M{x-22},168 h44 v44 h-44 z" fill="#bfe1dc" stroke="{TEAL}" stroke-width="2"/>')
b.append(path(f'M{x-6},170 v40 M{x+6},170 v40',TEAL,2))
for dx,dy in [(-28,115),(0,130),(26,112),(-14,148)]: b.append(f'<rect x="{x+dx-6}" y="{dy-6}" width="12" height="12" fill="{TEAL}"/>')
b.append(arrow(x,150,x,240,TEAL,3)); b.append(f'<rect x="{x+16}" y="{240}" width="12" height="12" fill="{TEAL}"/>')
# activo
x=640
b.append(f'<path d="M{x-22},168 h44 v44 h-44 z" fill="#fbd6bd" stroke="{NAR}" stroke-width="2"/>')
for dx,dy in [(-24,120),(22,130)]: b.append(f'<polygon points="{x+dx},{dy-7} {x+dx+7},{dy+6} {x+dx-7},{dy+6}" fill="{NAR}"/>')
for dx,dy in [(-30,235),(-12,250),(10,238),(28,252),(0,265)]: b.append(f'<polygon points="{x+dx},{dy-7} {x+dx+7},{dy+6} {x+dx-7},{dy+6}" fill="{NAR}"/>')
b.append(arrow(x,240,x,110,NAR,3))
b.append(tbox(x+30,222,50,24,'ATP','#fff',NAR,12,NAR,'bold',12))
b.append(T(x,98,'p. ej. glucoproteína P (expulsa)',11,GRIS))
# endocitosis
x=815
b.append(box(x-40,166,80,48,'#fff','none',0,0))
b.append(path(f'M{x-40},170 C{x-20},170 {x-26},226 {x},226 C{x+26},226 {x+20},170 {x+40},170','#e9c46a',9))
b.append(circ(x,196,10,MOR))
b.append(circ(x,262,20,'#fff','#e9c46a',6)); b.append(circ(x,262,9,MOR)); b.append(T(x+30,266,'vesícula',11,MOR,'start'))
b.append(circ(x,112,10,MOR)); b.append(arrow(x,126,x,180,MOR,2.5))
b.append(T(460,380,'Lo que más pesa en la absorción: liposolubilidad, grado de ionización (pKa vs pH), tamaño y flujo sanguíneo',12,GRIS))
svg(G,'transporte-membranas.svg',W,H,''.join(b))

# 3. Atrapamiento iónico (naproxeno pKa 5)
W,H=920,400
b=[title(W,'Atrapamiento iónico: ácido débil (naproxeno, pKa 5)','pH = pKa + log [A⁻]/[HA]   ·   solo la forma NO ionizada (HA) cruza la membrana')]
b.append(box(30,80,360,250,CLARO['y'],AMA,14)); b.append(T(210,108,'Jugo gástrico · pH 2',16,'#8a5a00',w='bold'))
b.append(box(530,80,360,250,CLARO['r'],ROJO,14)); b.append(T(710,108,'Plasma · pH 7.4',16,ROJO,w='bold'))
b.append(box(430,70,60,270,'#fff7df','#c9a54a',4,2)); b.append(T(460,360,'membrana',12,GRIS))
b.append(arrow(250,300,670,300,VERDE,3)); b.append(arrow(670,316,250,316,VERDE,3))
b.append(T(460,292,'HA cruza',14,VERDE,w='bold'))
for x0,ha,a,txt1,txt2 in ((80,'HA = 1','A⁻ = 0.001','Total = 1.001','Casi todo no ionizado'),(580,'HA = 1','A⁻ = 251','Total = 252','Casi todo ionizado → atrapado')):
    b.append(tbox(x0,140,110,46,ha,'#fff',VERDE,15,VERDE,'bold'))
    b.append(tbox(x0+130,140,130,46,a,'#fff',GRIS,15,'#222','bold'))
    b.append(T(x0+130,228,txt1,17,'#222',w='bold')); b.append(T(x0+130,252,txt2,13,GRIS))
b.append(T(460,388,'El ácido débil se acumula del lado alcalino (plasma); una base débil se acumula del lado ácido.',13,'#333'))
svg(G,'atrapamiento-ionico.svg',W,H,''.join(b))

# 4. Primer paso
W,H=920,380
b=[title(W,'Efecto de primer paso hepático')]
b.append(tbox(30,90,150,60,['Vía oral','(tableta)'],CLARO['g'],GRIS,14))
b.append(arrow(182,120,250,120,GRIS))
b.append(tbox(252,90,150,60,['Intestino','(pared: CYP3A4, P-gp)'],CLARO['y'],AMA,13))
b.append(arrow(404,120,472,120,'#7a4b2a',4)); b.append(T(438,108,'vena porta',12,'#7a4b2a',w='bold'))
b.append(tbox(474,84,170,72,['HÍGADO','metaboliza una parte','antes de llegar'],CLARO['n'],NAR,13,'#222','bold'))
b.append(arrow(646,120,714,120,ROJO,4))
b.append(tbox(716,84,180,72,['Circulación','sistémica'],CLARO['r'],ROJO,15,ROJO,'bold'))
b.append(arrow(560,158,560,196,GRIS,2)); b.append(T(560,214,'fracción que se pierde (metabolitos)',12,GRIS))
# vías que lo evitan
b.append(tbox(250,270,180,60,['Sublingual','(venas a cava superior)'],CLARO['v'],VERDE,13))
b.append(tbox(450,270,180,60,['Rectal (parcial)','IV, IM, SC, inhalada'],CLARO['v'],VERDE,13))
b.append(path('M632,300 H806 V166',VERDE,2.5,'none','7 5')); b.append(arrow(806,180,806,160,VERDE,2.5)); b.append(line(430,300,450,300,VERDE,2.5,'7 5'))
b.append(T(130,296,'Vías que evitan',13,VERDE,w='bold')); b.append(T(130,313,'el primer paso →',13,VERDE,w='bold'))
b.append(T(460,362,'Biodisponibilidad (F): fracción que llega sin cambios a la circulación sistémica. IV = 100 %.',13,'#333'))
svg(G,'primer-paso.svg',W,H,''.join(b))

# 5. Biodisponibilidad: curvas IV vs oral
W,H=900,400
b=[title(W,'Curva concentración-tiempo: IV vs oral')]
x0,y0,x1,y1=90,340,620,70
X=lambda t: x0+t*(x1-x0-20)/12; Y=lambda c: y0-c*(y0-y1-20)/100
b.append(axes(x0,y0,x1,y1,'Tiempo (h)','Concentración plasmática'))
ka,ke=1.1,0.25
oral=lambda t: 70*(ka/(ka-ke))*(math.exp(-ke*t)-math.exp(-ka*t))
iv=lambda t: 95*math.exp(-ke*t)
b.append(f'<path d="{curve(oral,0,12,X,Y)} L{X(12):.1f},{y0} L{X(0):.1f},{y0}Z" fill="{NAR}" opacity=".15"/>')
b.append(path(curve(iv,0,12,X,Y),AZUL,3)); b.append(path(curve(oral,0,12,X,Y),NAR,3))
# CME / CMT
for c,lab,col in ((78,'Concentración mínima tóxica',ROJO),(18,'Concentración mínima eficaz',VERDE)):
    b.append(line(x0,Y(c),x1-10,Y(c),col,1.6,'6 5')); b.append(T(x1-10,Y(c)-6,lab,11,col,'end'))
tmax=math.log(ka/ke)/(ka-ke); cmax=oral(tmax)
b.append(line(X(tmax),Y(cmax),X(tmax),y0,GRIS,1.3,'3 4')); b.append(T(X(tmax),y0+16,'Tmax',11,GRIS))
b.append(circ(X(tmax),Y(cmax),5,NAR)); b.append(T(X(tmax)+10,Y(cmax)-8,'Cmax',12,NAR,'start','bold'))
b.append(T(X(6),Y(18)+40,'AUC oral',13,NAR,w='bold'))
b.append(T(X(0.35),Y(95)-8,'IV',13,AZUL,'start','bold'))
# panel
b.append(box(650,80,230,250,CLARO['g'],'#ccc',12,1))
b.append(TL(765,110,['F = AUC oral / AUC IV'],14,'#222','middle','bold'))
b.append(TL(668,145,['• IV: Cmax inmediata, F = 100 %','• Oral: sube (absorción) y','   luego baja (eliminación)','• Cmax: concentración pico','• Tmax: cuándo se alcanza','• AUC: exposición total','• Ventana terapéutica: entre','   la mínima eficaz y la tóxica'],12,'#333','start',lh=19))
svg(G,'biodisponibilidad.svg',W,H,''.join(b))

# 6. Metabolismo: fase I y II
W,H=920,330
b=[title(W,'Biotransformación hepática: fase I y fase II')]
b.append(tbox(20,100,150,80,['Fármaco','lipófilo'],CLARO['y'],AMA,15,'#222','bold'))
b.append(arrow(172,140,250,140,GRIS,3))
b.append(tbox(252,80,210,120,['FASE I','(no sintética)','Oxidación · reducción','· hidrólisis','CYP450 (monooxigenasas)'],CLARO['n'],NAR,13))
b.append(arrow(464,140,540,140,GRIS,3))
b.append(tbox(542,80,210,120,['FASE II','(sintética, conjugación)','Glucurónico · sulfato ·','acetilación · glutatión','· glicina'],CLARO['m'],MOR,13))
b.append(arrow(754,140,800,140,GRIS,3))
b.append(tbox(802,100,100,80,['Hidro-','soluble','→ orina','o bilis'],CLARO['a'],AZUL,13,AZUL,'bold'))
b.append(path('M360,202 C360,260 640,260 650,204',GRIS,2,'none','6 5')); b.append(arrow(645,214,651,202,GRIS,2))
b.append(T(505,262,'algunos van directo a fase II',12,GRIS))
b.append(TL(360,290,['La fase I puede ACTIVAR (profármaco → fármaco) o INACTIVAR.','Inductores (rifampicina, tabaco en 1A2) ↑ CYP → ↓ niveles; inhibidores (cimetidina, fluconazol, verapamilo) ↓ CYP → ↑ niveles.'],12,'#333','middle',lh=18))
svg(G,'fases-metabolismo.svg',W,H,''.join(b))

# 7. Excreción renal
W,H=920,410
b=[title(W,'Excreción renal: filtración, secreción y reabsorción')]
# nefrona esquemática
b.append(circ(150,170,52,'#fbe6e4',ROJO,2.5)); b.append(T(150,166,'Glomérulo',13,ROJO,w='bold')); b.append(T(150,184,'filtración',12,ROJO))
b.append(path('M200,170 H330 C380,170 380,250 430,250 H560 C620,250 620,170 680,170 H840',AZUL,14)); b.append(path('M200,170 H330 C380,170 380,250 430,250 H560 C620,250 620,170 680,170 H840','#e6effa',9))
b.append(T(850,175,'orina',13,AZUL,'start','bold'))
b.append(T(150,250,'Pasa solo el fármaco',12,'#222')); b.append(T(150,266,'LIBRE (no unido a',12,'#222')); b.append(T(150,282,'proteínas), PM pequeño',12,'#222'))
b.append(arrow(290,96,290,160,NAR,3)); b.append(T(290,86,'Secreción tubular activa (proximal)',13,NAR,w='bold'))
b.append(T(300,112,'transportadores de ácidos y bases',11,NAR,'start'))
b.append(T(300,130,'(penicilina; el probenecid la bloquea)',11,GRIS,'start'))
b.append(arrow(500,236,500,180,VERDE,3)); b.append(T(500,168,'Reabsorción pasiva (distal)',13,VERDE,w='bold'))
b.append(T(510,290,'Solo regresa la forma NO ionizada y liposoluble',12,VERDE,'middle'))
b.append(box(40,320,840,74,CLARO['g'],'#ccc',12,1))
b.append(TL(460,346,['Orina ALCALINA → ioniza ácidos débiles (salicilatos, barbitúricos, metotrexato) → no se reabsorben → se eliminan más.','Orina ÁCIDA → favorece la eliminación de bases débiles (anfetaminas, morfina).  PM < 300 → riñón; PM > 500 → bilis.'],12,'#333',lh=20))
svg(G,'excrecion-renal.svg',W,H,''.join(b))

# 8. Tipos de receptores
W,H=940,420
b=[title(W,'Tipos de receptores y su velocidad de respuesta')]
b.append(T(16,96,'Fuera',12,GRIS,'start')); b.append(T(16,260,'Dentro',12,GRIS,'start'))
b.append(membrane(70,700,150,36))
# 1 canal iónico
x=150
b.append(box(x-34,140,26,56,'#bfe1dc',TEAL,6)); b.append(box(x+8,140,26,56,'#bfe1dc',TEAL,6))
b.append(circ(x-21,128,9,NAR)); b.append(arrow(x,110,x,236,TEAL,3)); b.append(T(x+16,104,'iones',11,TEAL,'start'))
b.append(T(x,76,'1. Canal iónico',13,TEAL,w='bold')); b.append(T(x,300,'milisegundos',12,'#222','middle','bold'))
b.append(TL(x,320,['Nicotínico, GABA-A','(BZD), canales de Na⁺,','Ca²⁺ y K⁺-ATP'],11,GRIS))
# 2 proteína G
x=345
b.append(path(f'M{x-30},150 v36 m10,-36 v36 m10,-36 v36 m10,-36 v36 m10,-36 v36 m10,-36 v36 m10,-36 v36',MOR,5))
b.append(circ(x,134,9,NAR))
b.append(f'<ellipse cx="{x+40}" cy="{206}" rx="22" ry="13" fill="#d9c7ec" stroke="{MOR}" stroke-width="2"/>'); b.append(T(x+40,211,'G',13,MOR,w='bold'))
b.append(arrow(x+40,222,x+40,246,MOR,2)); b.append(tbox(x+5,248,80,24,'AMPc / IP₃','#fff',MOR,11,MOR,'bold',8))
b.append(T(x,76,'2. Acoplado a proteína G',13,MOR,w='bold')); b.append(T(x,300,'segundos',12,'#222','middle','bold'))
b.append(TL(x,320,['Muscarínicos, α y β','adrenérgicos, opioides'],11,GRIS))
# 3 enzimático (tirosina cinasa)
x=555
b.append(box(x-30,112,22,38,'#fde2cf',NAR,6)); b.append(box(x+8,112,22,38,'#fde2cf',NAR,6))
b.append(box(x-24,150,10,36,NAR,NAR,2)); b.append(box(x+14,150,10,36,NAR,NAR,2))
b.append(box(x-30,186,22,34,'#fde2cf',NAR,6)); b.append(box(x+8,186,22,34,'#fde2cf',NAR,6))
b.append(T(x-19,236,'P',12,NAR,w='bold')); b.append(T(x+19,236,'P',12,NAR,w='bold'))
b.append(circ(x,104,9,VERDE))
b.append(T(x,76,'3. Con actividad enzimática',13,NAR,w='bold')); b.append(T(x,300,'minutos',12,'#222','middle','bold'))
b.append(TL(x,320,['Insulina, factores de','crecimiento (tirosina cinasa)'],11,GRIS))
# 4 nuclear
x=810
b.append(box(735,90,160,190,'#fafafa','#bbb',14,1.5,'5 4')); b.append(T(x,112,'citoplasma',11,GRIS))
b.append(f'<ellipse cx="{x}" cy="{220}" rx="58" ry="40" fill="#e6effa" stroke="{AZUL}" stroke-width="2"/>'); b.append(T(x,250,'núcleo (ADN)',11,AZUL))
b.append(circ(x,130,9,AMA)); b.append(arrow(x,142,x,188,AMA,2.5)); b.append(T(x+10,170,'liposoluble',11,'#8a5a00','start'))
b.append(path(f'M{x-30},215 q10,-10 20,0 t20,0 t20,0',AZUL,2))
b.append(T(x,76,'4. Intracelular (nuclear) †',13,AZUL,w='bold')); b.append(T(x,300,'horas a días',12,'#222','middle','bold'))
b.append(TL(x,320,['Glucocorticoides, hormonas','tiroideas y sexuales'],11,GRIS))
b.append(T(W/2,385,'El fármaco (círculo de color) es el ligando. † El tipo 4 es complemento: la clase vio los tres primeros.',12,GRIS))
svg(G,'tipos-receptores.svg',W,H,''.join(b))

# helpers para curvas dosis-respuesta (eje x = log dosis)
def sig(ec50,emax=100,n=1.3): return lambda x: emax/(1+10**(n*(ec50-x)))
# 9. Potencia vs eficacia
W,H=900,410
b=[title(W,'Curvas dosis-respuesta: potencia vs eficacia')]
x0,y0,x1,y1=90,340,620,70
X=lambda x: x0+(x+3)*(x1-x0-20)/6; Y=lambda e: y0-e*(y0-y1-30)/100
b.append(axes(x0,y0,x1,y1,'log [dosis]','Efecto (% del máximo)'))
for e in (50,100): b.append(line(x0,Y(e),x1-10,Y(e),'#bbb',1,'4 4')); b.append(T(x0-6,Y(e)+4,f'{e}',11,GRIS,'end'))
for ec,em,c,lab in ((-1.3,100,AZUL,'A'),(0.6,100,VERDE,'B'),(-0.2,60,NAR,'C')):
    b.append(path(curve(sig(ec,em),-3,3,X,Y),c,3))
for lab,c,x,y in (('A',AZUL,-1.75,62),('B',VERDE,1.05,62),('C',NAR,0.4,72)): b.append(T(X(x),Y(y),lab,16,c,'middle','bold'))
for ec,c in ((-1.3,AZUL),(0.6,VERDE)):
    b.append(line(X(ec),Y(50),X(ec),y0,c,1.4,'3 4')); b.append(T(X(ec),y0+16,'EC50',10,c))
b.append(box(645,80,240,250,CLARO['g'],'#ccc',12,1))
b.append(TL(660,108,['A vs B: misma EFICACIA (mismo','techo), A es más POTENTE','(EC50 menor: menos dosis).','','C: menor EFICACIA (efecto máximo','más bajo), aunque se dé más dosis.','','La eficacia importa más en la','clínica que la potencia.','','Pendiente: qué tanto cambia el','efecto al variar la dosis.'],12,'#333','start',lh=18))
svg(G,'potencia-eficacia.svg',W,H,''.join(b))

# 10. Agonistas y antagonistas
W,H=920,420
b=[title(W,'Agonistas y antagonistas en la curva dosis-respuesta')]
def panel(px,tit,curves,note):
    o=[]; x0,y0,x1,y1=px+50,330,px+410,90
    X=lambda x: x0+(x+3)*(x1-x0-10)/6; Y=lambda e: y0-e*(y0-y1-20)/100
    o.append(axes(x0,y0,x1,y1,'log [agonista]','Efecto'))
    o.append(T((x0+x1)/2,76,tit,15,'#222',w='bold'))
    for f,c,lab,lx,ly,dash in curves:
        o.append(path(curve(f,-3,3,X,Y),c,3,'none',dash)); o.append(T(X(lx),Y(ly),lab,12,c,'start','bold'))
    o.append(TL((x0+x1)/2,y0+52,note,12,GRIS))
    return ''.join(o)
b.append(panel(0,'Agonista completo vs parcial',[(sig(-1),VERDE,'Agonista completo',-2.9,80,''),(sig(-1.2,55),NAR,'Agonista parcial',0.4,44,'')],
    ['El parcial no llega al 100 % aunque ocupe todos los receptores']))
b.append(panel(460,'Antagonista competitivo vs no competitivo',[(sig(-1.4),VERDE,'Solo agonista',-2.9,80,''),(sig(0.6),AZUL,'+ competitivo',1.05,40,'7 5'),(sig(-1.4,55),ROJO,'+ no competitivo',-0.9,64,'3 4')],
    ['Competitivo: a la DERECHA, mismo máximo (se vence con más dosis)','No competitivo (irreversible): baja el MÁXIMO']))
svg(G,'agonistas-antagonistas.svg',W,H,''.join(b))

# 11. Porcentajes y conversiones
W,H=900,330
b=[title(W,'Concentraciones: lo que significa cada expresión')]
items=[('5 %  (p/v)','= 5 g en 100 mL','= 50 mg/mL',VERDE),('0.9 %  (p/v)','= 0.9 g en 100 mL','= 9 mg/mL (sol. salina)',AZUL),
       ('1 : 1000','= 1 g en 1000 mL','= 1 mg/mL (adrenalina)',NAR),('1 : 10 000','= 1 g en 10 000 mL','= 0.1 mg/mL',MOR)]
for i,(a,bb,c,col) in enumerate(items):
    x=30+i*218
    b.append(box(x,76,200,130,'#fff',col,12,2.5)); b.append(T(x+100,110,a,20,col,w='bold'))
    b.append(T(x+100,146,bb,14,'#222')); b.append(T(x+100,176,c,14,'#222','middle','bold'))
b.append(box(30,228,840,80,CLARO['g'],'#ccc',12,1))
b.append(TL(450,256,['1 g = 1000 mg = 1 000 000 µg      ·      1 L = 1000 mL      ·      1 mL ≈ 20 gotas (macrogotero)','Truco: % p/v × 10 = mg/mL      ·      regla de tres: dosis indicada × volumen / concentración'],13,'#333',lh=22))
svg(G,'concentraciones.svg',W,H,''.join(b))

# 12. Teratogenia: periodos de susceptibilidad
W,H=920,330
b=[title(W,'Periodos de susceptibilidad a teratógenos')]
def wx(s):  # escala por tramos: 0-2 y 2-8 se ven grandes, 8-38 comprimido
    return 40+s*55 if s<=2 else (150+(s-2)*55 if s<=8 else 480+(s-8)*400/30)
segs=[(0,2,'Todo o nada',GRIS,'Muere el embrión o','se repara sin defecto'),
      (2,8,'Periodo embrionario (organogénesis)',ROJO,'MÁXIMA susceptibilidad:','malformaciones mayores'),
      (8,38,'Periodo fetal',AMA,'Defectos funcionales y menores,','retraso del crecimiento, SNC')]
for s0,s1,t,c,l1,l2 in segs:
    b.append(box(wx(s0),90,wx(s1)-wx(s0)-3,60,c,c,6,1))
    tx=(wx(s0)+wx(s1))/2
    if s1-s0<3:
        b.append(T(tx,126,t,13,'#fff',w='bold')); b.append(TL(tx,178,[l1,l2],12,'#333'))
    else:
        b.append(T(tx,126,t,14,'#fff',w='bold')); b.append(TL(tx,178,[l1,l2],12,'#333'))
for s in (0,2,8,12,20,28,38):
    b.append(line(wx(s),152,wx(s),160,GRIS,1.5)); b.append(T(wx(s),74,f'{s}',11,GRIS))
b.append(T(460,56,'semanas desde la concepción (escala no proporcional)',11,GRIS))
b.append(box(40,240,840,66,CLARO['g'],'#ccc',12,1))
b.append(TL(460,266,['Ejemplos: talidomida (focomelia), isotretinoína, warfarina, valproato y fenitoína, IECA (2º–3º trimestre),','tetraciclinas (dientes), metotrexato. Categoría FDA X = contraindicado; D = riesgo demostrado.'],12,'#333',lh=19))
svg(G,'teratogenia.svg',W,H,''.join(b))

# 13. Fases del desarrollo de un fármaco
W,H=940,330
b=[title(W,'Del laboratorio a la farmacia: fases del desarrollo')]
ph=[('Preclínico','animales y','laboratorio','2–6 años',GRIS),('Fase I','15–30 sanos','seguridad, FC,','dosis máxima',AZUL),
    ('Fase II','200–500','pacientes · dosis','y posible eficacia',TEAL),('Fase III','2 000–5 000','multicéntrico:','establece eficacia',VERDE),
    ('Registro','aprobación','(COFEPRIS,','FDA)',NAR),('Fase IV','poscomercia-','lización:','farmacovigilancia',MOR)]
for i,(t,a,bb,c,col) in enumerate(ph):
    x=20+i*153
    b.append(f'<path d="M{x},80 h125 l20,45 l-20,45 h-125 l20,-45z" fill="{col}"/>')
    b.append(T(x+80,131,t,15,'#fff',w='bold'))
    b.append(TL(x+80,200,[a,bb,c],12,'#333'))
b.append(T(W/2,300,'Doble ciego, grupo control y consentimiento informado desde fase II; solo ~1 de cada 10 que entran a fase I llega a la farmacia.',12,GRIS))
svg(G,'fases-desarrollo.svg',W,H,''.join(b))

# 14. Cascada del ácido araquidónico
W,H=940,470
b=[title(W,'Cascada del ácido araquidónico y dónde actúan los fármacos')]
b.append(tbox(340,66,260,44,'Fosfolípidos de membrana',CLARO['y'],AMA,14,'#222','bold'))
b.append(arrow(470,112,470,160,GRIS,3)); b.append(T(482,140,'Fosfolipasa A₂',13,'#222','start'))
b.append(drug(330,138,'Glucocorticoides')); b.append(block(398,138,462,138))
b.append(tbox(360,162,220,44,'Ácido araquidónico',CLARO['n'],NAR,15,'#222','bold'))
b.append(arrow(420,208,250,262,GRIS,3)); b.append(arrow(520,208,690,262,GRIS,3))
b.append(T(345,252,'COX-1 / COX-2',13,'#222','start','bold')); b.append(T(600,252,'5-lipooxigenasa',13,'#222','end','bold'))
b.append(drug(150,212,'AINE · paracetamol (SNC)')); b.append(block(205,226,318,236))
b.append(drug(810,212,'Zileutón')); b.append(block(780,226,622,236))
b.append(tbox(150,264,200,40,'PGG₂ → PGH₂',CLARO['r'],ROJO,14,'#222','bold'))
b.append(tbox(600,264,200,40,'Leucotrienos',CLARO['a'],AZUL,14,'#222','bold'))
pr=[('PGE₂','fiebre, dolor, protege mucosa y riñón'),('PGI₂','antiagregante, vasodilata (endotelio)'),('TXA₂','agrega plaquetas, vasoconstriñe'),('PGF₂α','útero, cérvix'),('PGD₂','quimiotáctico')]
for i,(n,d) in enumerate(pr):
    y=330+i*25; b.append(T(70,y,n,13,ROJO,'start','bold')); b.append(T(132,y,d,12,'#333','start'))
b.append(T(560,330,'LTB₄',13,AZUL,'start','bold')); b.append(T(672,330,'quimiotaxis de neutrófilos',12,'#333','start'))
b.append(T(560,355,'LTC₄, D₄, E₄',13,AZUL,'start','bold')); b.append(T(672,355,'broncoconstricción, permeabilidad',12,'#333','start'))
b.append(T(560,380,'Lipoxinas',13,AZUL,'start','bold')); b.append(T(672,380,'frenan la inflamación',12,'#333','start'))
b.append(drug(600,410,'Montelukast','#b3261e',12,'start')); b.append(T(704,414,'bloquea el receptor de LTD₄',12,GRIS,'start'))
b.append(T(W/2,458,'Por eso los AINE pueden dar broncoespasmo en asmáticos sensibles: la vía se desvía hacia leucotrienos.',12,GRIS))
svg(G,'acido-araquidonico.svg',W,H,''.join(b))

# 15. COX-1 vs COX-2
W,H=900,330
b=[title(W,'COX-1 vs COX-2: por qué los AINE dan efectos adversos')]
b.append(tbox(40,70,370,50,'COX-1 · constitutiva («de mantenimiento»)',CLARO['v'],VERDE,15,VERDE,'bold'))
b.append(tbox(490,70,370,50,'COX-2 · inducible (inflamación)',CLARO['r'],ROJO,15,ROJO,'bold'))
b.append(TL(60,150,['• Protege la mucosa gástrica (moco, ↓ ácido)','• Mantiene el flujo renal','• TXA₂ en plaquetas → agregación'],13,'#222','start',lh=22))
b.append(TL(510,150,['• Dolor, fiebre e inflamación','• También es constitutiva en riñón, endotelio','  (PGI₂) y SNC'],13,'#222','start',lh=22))
b.append(box(40,232,820,80,CLARO['g'],'#ccc',12,1))
b.append(TL(60,258,['Bloquear COX-1 → gastritis/úlcera, sangrado, daño renal.   Bloquear COX-2 → analgesia, antipirexia, antiinflamatorio.','Coxibs (celecoxib, selectivos COX-2): menos daño gástrico, pero ↓ PGI₂ con TXA₂ intacto → más riesgo trombótico.'],12,'#333','start',lh=22))
svg(G,'cox1-cox2.svg',W,H,''.join(b))

# 16. Opioides en la sinapsis del dolor
W,H=920,420
b=[title(W,'Cómo produce analgesia un opioide (receptor μ)')]
b.append(path('M120,70 H460 V200 C460,250 420,262 380,262 H200 C160,262 120,250 120,200Z',AZUL,2.5,CLARO['a']))
b.append(T(140,94,'Terminal de la neurona aferente del dolor',13,AZUL,'start','bold'))
for x in (220,290,360): b.append(circ(x,180,16,'#fff',AZUL,2)); b.append(circ(x-5,176,3.5,AZUL)); b.append(circ(x+5,185,3.5,AZUL))
b.append(T(290,140,'vesículas con glutamato y sustancia P',12,AZUL))
b.append(box(150,250,40,24,'#fff','#888',4)); b.append(T(170,267,'Ca²⁺',11,'#555',w='bold'))
b.append(box(420,250,36,24,'#fff',ROJO,6)); b.append(T(438,267,'μ',14,ROJO,w='bold'))
for x in (240,290,340): b.append(circ(x,300,4,AZUL))
b.append(path('M120,330 H460 V400 H120Z',MOR,2.5,CLARO['m'])); b.append(T(140,388,'Neurona del asta dorsal (lleva la señal al cerebro)',12,MOR,'start','bold'))
b.append(box(420,318,36,24,'#fff',ROJO,6)); b.append(T(438,335,'μ',14,ROJO,w='bold'))
b.append(box(150,318,40,24,'#fff','#888',4)); b.append(T(170,335,'K⁺',11,'#555',w='bold'))
b.append(drug(560,296,'Opioide',ROJO)); b.append(arrow(526,290,460,264,ROJO,2.2,8)); b.append(arrow(526,302,460,328,ROJO,2.2,8))
b.append(box(600,70,300,104,CLARO['a'],AZUL,10,1.5))
b.append(TL(614,96,['PRESINÁPTICO: proteína Gi →','↓ AMPc y cierra canales de Ca²⁺','→ se libera menos neurotransmisor'],13,'#222','start',lh=20))
b.append(box(600,184,300,84,CLARO['m'],MOR,10,1.5))
b.append(TL(614,210,['POSTSINÁPTICO: abre canales de K⁺','→ hiperpolariza: la señal no sube'],13,'#222','start',lh=20))
b.append(box(600,326,300,78,CLARO['r'],ROJO,10,1.5))
b.append(TL(614,350,['RAM μ: depresión respiratoria, miosis,','estreñimiento, náusea, sedación,','dependencia. Antídoto: naloxona.'],12,'#222','start',lh=18))
svg(G,'opioides.svg',W,H,''.join(b))

# 17. Sistema nervioso autónomo: vías
W,H=980,440
b=[title(W,'Sistema nervioso autónomo: neurotransmisores y receptores')]
rows=[('Parasimpático (ganglio cerca del órgano)','ACh','Nn','ACh','M',560,'Corazón, glándulas, músculo liso',VERDE,True),
      ('Simpático (ganglio cerca de la médula)','ACh','Nn','NA','α / β',200,'Corazón, vasos, bronquios',NAR,True),
      ('Simpático → glándulas sudoríparas','ACh','Nn','ACh','M',200,'Glándula sudorípara',NAR,True),
      ('Simpático → médula suprarrenal','ACh','Nn','','',200,'Médula suprarrenal (= ganglio)',AMA,False),
      ('Somático (motor)','ACh','Nm','','',None,'Músculo esquelético (placa motora)',AZUL,None)]
for i,(name,n1,r1,n2,r2,gx,org,c,gang) in enumerate(rows):
    y=100+i*66
    b.append(T(20,y-14,name,13,c,'start','bold'))
    b.append(circ(40,y+6,10,c))
    if gang is None:
        b.append(line(50,y+6,640,y+6,c,3)); b.append(T(345,y+26,n1,12,'#222','middle','bold'))
        b.append(box(642,y-8,56,28,'#fff',c,6)); b.append(T(670,y+11,r1,11,c,w='bold'))
    else:
        b.append(line(50,y+6,gx-14,y+6,c,3)); b.append(T((50+gx)/2,y+26,n1,12,'#222','middle','bold'))
        b.append(box(gx-14,y-6,24,24,'#fff',c,4)); b.append(T(gx-2,y+11,r1,10,c,w='bold'))
        b.append(circ(gx+22,y+6,10,c))
        if gang:
            b.append(line(gx+32,y+6,640,y+6,c,3)); b.append(T((gx+640)/2,y+26,n2,12,'#222','middle','bold'))
            b.append(box(642,y-8,56,28,'#fff',c,6)); b.append(T(670,y+11,r2,11,c,w='bold'))
        else:
            b.append(T(gx+38,y+11,'libera adrenalina (~80 %) y NA a la sangre',12,'#222','start','bold'))
    b.append(T(712,y+11,org,12,'#333','start'))
b.append(T(20,416,'ACh = acetilcolina · NA = noradrenalina · Nn = nicotínico ganglionar · Nm = nicotínico muscular · M = muscarínico',12,GRIS,'start'))
svg(G,'sna-vias.svg',W,H,''.join(b))

# 18. Sinapsis colinérgica
W,H=940,480
b=[title(W,'Sinapsis colinérgica: síntesis, liberación y degradación de la ACh')]
b.append(path('M160,70 H560 V250 C560,300 510,310 460,310 H260 C210,310 160,300 160,250Z',VERDE,2.5,CLARO['v']))
b.append(T(190,95,'Terminal presináptica',13,VERDE,'start','bold'))
b.append(T(220,125,'Colina + acetil-CoA',13,'#222','start')); b.append(arrow(300,132,300,168,GRIS,2)); b.append(T(310,154,'ChAT',12,'#222','start','bold'))
b.append(T(282,186,'ACh',14,VERDE,'start','bold'))
b.append(arrow(320,182,382,212,GRIS,2)); b.append(T(350,186,'VAChT',11,GRIS,'start'))
for x,y in ((420,236),(480,256),(370,266)):
    b.append(circ(x,y,22,'#fff',VERDE,2))
    for dx,dy in ((-7,-5),(6,-6),(0,7)): b.append(circ(x+dx,y+dy,3.2,VERDE))
b.append(T(190,292,'Ca²⁺ entra → exocitosis',12,AZUL,'start','bold'))
b.append(drug(650,150,'Vesamicol',ROJO,11)); b.append(block(612,156,446,226,ROJO,2)); b.append(T(650,174,'bloquea VAChT',11,GRIS))
b.append(drug(680,250,'Toxina botulínica',ROJO,11)); b.append(block(624,254,508,268,ROJO,2)); b.append(T(680,274,'impide la liberación',11,GRIS))
# recaptación de colina + hemicolinio
b.append(path('M200,340 C170,330 168,250 176,214',GRIS,1.8,'none','4 4')); b.append(arrow(176,224,177,206,GRIS,1.8,7))
b.append(drug(90,200,'Hemicolinio',ROJO,11)); b.append(block(134,208,170,212,ROJO,2)); b.append(T(90,224,'bloquea la',11,GRIS)); b.append(T(90,238,'captación',11,GRIS)); b.append(T(90,252,'de colina',11,GRIS))
# hendidura
b.append(T(20,360,'Hendidura',12,GRIS,'start'))
for x in (330,370,410,450): b.append(circ(x,352,3.6,VERDE))
b.append(tbox(200,338,96,30,'AChE',CLARO['n'],NAR,13,NAR,'bold',8))
b.append(T(248,384,'ACh → colina + acetato',11,GRIS))
b.append(drug(720,352,'Anticolinesterasas: neostigmina, fisostigmina, donepezilo',ROJO,11)); b.append(block(530,352,302,353,ROJO,2))
# postsináptica
b.append(path('M160,400 H560 V466 H160Z',MOR,2.5,CLARO['m'])); b.append(T(180,454,'Membrana postsináptica',13,MOR,'start','bold'))
b.append(box(340,390,40,22,'#fff',MOR,5)); b.append(T(360,406,'M',12,MOR,w='bold'))
b.append(box(420,390,40,22,'#fff',MOR,5)); b.append(T(440,406,'N',12,MOR,w='bold'))
b.append(drug(740,404,'Atropina (M) · bloq. neuromusculares (Nm)',ROJO,11)); b.append(block(608,404,464,402,ROJO,2))
b.append(drug(740,444,'Agonistas directos: betanecol, pilocarpina (M)',VERDE,11)); b.append(arrow(606,444,462,410,VERDE,2,8))
svg(G,'sinapsis-colinergica.svg',W,H,''.join(b))

# 19. Síntesis de catecolaminas + terminal noradrenérgica
W,H=940,480
b=[title(W,'Catecolaminas: síntesis, liberación y fin de su acción')]
steps=[('L-tirosina','Tirosina hidroxilasa (paso limitante)'),('L-DOPA','DOPA descarboxilasa'),('Dopamina','Dopamina β-hidroxilasa (en la vesícula)'),('Noradrenalina','PNMT (médula suprarrenal)'),('Adrenalina','')]
for i,(m,e) in enumerate(steps):
    y=70+i*74
    c=[GRIS,AMA,MOR,NAR,ROJO][i]
    b.append(tbox(30,y,170,38,m,'#fff',c,14,c,'bold'))
    if e: b.append(arrow(115,y+40,115,y+72,GRIS,2)); b.append(T(128,y+58,e,12,'#333','start'))
b.append(T(212,166,'⊣ la inhibe la α-metiltirosina',11,ROJO,'start','bold'))
# terminal
b.append(path('M470,64 H910 V240 C910,280 870,290 830,290 H550 C510,290 470,280 470,240Z',NAR,2.5,CLARO['n']))
b.append(T(490,89,'Terminal noradrenérgica',13,NAR,'start','bold'))
for x,y in ((620,200),(700,226),(780,200)):
    b.append(circ(x,y,22,'#fff',NAR,2)); b.append(T(x,y+5,'NA',11,NAR,w='bold'))
b.append(tbox(800,104,90,32,'MAO','#fff',GRIS,13,'#222','bold',8)); b.append(T(845,152,'(mitocondria)',11,GRIS))
b.append(drug(580,130,'Reserpina (VMAT)',ROJO,11)); b.append(block(612,144,618,174,ROJO,2))
b.append(T(490,270,'α₂ presináptico frena la liberación (clonidina)',11,AZUL,'start','bold'))
b.append(T(480,322,'Hendidura',12,GRIS,'start'))
for x in (600,640,680,720): b.append(circ(x,318,4,NAR))
b.append(path('M732,318 C800,318 840,310 846,294',GRIS,2,'none')); b.append(arrow(845,302,847,288,GRIS,2,8))
b.append(T(850,330,'Recaptación (NET) ~90 %',12,'#222','middle','bold'))
b.append(drug(850,356,'Cocaína, tricíclicos',ROJO,11))
b.append(tbox(530,340,180,30,'COMT (extraneuronal)','#fff',GRIS,12,'#222','bold',8))
b.append(T(620,392,'Metabolitos (ácido vanililmandélico) → orina',12,GRIS))
b.append(path('M470,412 H910 V452 H470Z',MOR,2,CLARO['m'])); b.append(T(690,438,'Receptores α y β en la célula efectora',13,MOR,w='bold'))
svg(G,'catecolaminas.svg',W,H,''.join(b))

# 20. Receptores adrenérgicos y segundos mensajeros
W,H=940,400
b=[title(W,'Receptores adrenérgicos: proteína G y efecto principal')]
rec=[('α₁','Gq','↑ IP₃ / Ca²⁺','Vasoconstricción, midriasis,','contrae esfínter vesical',ROJO,'Fenilefrina','Prazosina'),
     ('α₂','Gi','↓ AMPc','Frena liberación de NA,','↓ insulina, agrega plaquetas',AZUL,'Clonidina','Yohimbina'),
     ('β₁','Gs','↑ AMPc','↑ FC e inotropismo,','libera renina',NAR,'Dobutamina','Metoprolol'),
     ('β₂','Gs','↑ AMPc','Broncodilatación, vasodilatación,','relaja útero, glucogenólisis',VERDE,'Salbutamol','Propranolol*'),
     ('β₃','Gs','↑ AMPc','Lipólisis','(adipocitos)',MOR,'Mirabegrón†','—')]
for i,(r,g,m,e1,e2,c,ag,an) in enumerate(rec):
    x=20+i*182
    b.append(tbox(x,70,168,52,r,c,c,24,'#fff','bold'))
    b.append(tbox(x+20,134,128,30,g+'  →  '+m,'#fff',c,12,c,'bold',8))
    b.append(TL(x+84,196,[e1,e2],12,'#222'))
    b.append(T(x+84,262,'Agonista',11,GRIS)); b.append(drug(x+84,282,ag,VERDE,11))
    b.append(T(x+84,316,'Antagonista',11,GRIS)); b.append(drug(x+84,336,an,ROJO,11) if an!='—' else T(x+84,340,'—',13,GRIS))
b.append(T(W/2,384,'* Propranolol bloquea β₁ y β₂ (no selectivo). Regla: Gs ↑ AMPc · Gi ↓ AMPc · Gq ↑ Ca²⁺.  † complemento',12,GRIS))
svg(G,'receptores-adrenergicos.svg',W,H,''.join(b))

# 21. Interacciones por CYP
W,H=900,360
b=[title(W,'Interacciones por citocromo P450: inductores e inhibidores')]
for x,tit,c,fl,res,ej in ((30,'INHIBIDOR',ROJO,'↓ actividad del CYP','↑ niveles del otro fármaco → TOXICIDAD',
        ['Fluconazol, ketoconazol','Claritromicina, eritromicina','Cimetidina, verapamilo','Fluoroquinolonas, jugo de toronja']),
     (470,'INDUCTOR',AZUL,'↑ síntesis del CYP (días)','↓ niveles del otro fármaco → FALLA',
        ['Rifampicina','Carbamazepina, fenitoína','Fenobarbital','Tabaco (1A2), alcohol crónico'])):
    b.append(tbox(x,70,400,44,tit,c,c,17,'#fff','bold'))
    b.append(T(x+200,140,fl,14,'#222',w='bold')); b.append(arrow(x+200,150,x+200,176,GRIS,2))
    b.append(T(x+200,196,res,14,c,w='bold'))
    b.append(TL(x+200,232,ej,13,'#333',lh=20))
b.append(T(W/2,345,'Peligrosas sobre todo con margen terapéutico estrecho: warfarina, fenitoína, teofilina, ciclosporina, digoxina.',12,GRIS))
svg(G,'interacciones-cyp.svg',W,H,''.join(b))

# ═════════════════════════ FARMACOLOGÍA II (4º) ═════════════════════════
G='farmacologia-ii'

# 1. Sitios de acción de los antibióticos
W,H=960,520
b=[title(W,'Dónde actúa cada familia de antibióticos')]
b.append(f'<rect x="250" y="90" width="460" height="330" rx="160" fill="#f6efe2" stroke="#8a6a3a" stroke-width="10"/>')
b.append(f'<rect x="262" y="102" width="436" height="306" rx="150" fill="#fffaf0" stroke="#d6a84a" stroke-width="4"/>')
b.append(T(480,124,'pared (peptidoglucano)',11,'#8a6a3a')); b.append(T(480,140,'membrana',11,'#b58a2a'))
# ADN
b.append(path('M360,250 C390,200 430,300 460,250 S520,200 540,250 S600,300 620,250',AZUL,3))
b.append(T(490,292,'ADN',13,AZUL,w='bold'))
# ribosomas
for x,y in ((370,350),(560,350)):
    b.append(f'<ellipse cx="{x}" cy="{y-12}" rx="30" ry="16" fill="#d9c7ec" stroke="{MOR}" stroke-width="2"/>'); b.append(T(x,y-8,'50S',11,MOR,w='bold'))
    b.append(f'<ellipse cx="{x}" cy="{y+14}" rx="22" ry="11" fill="#efe3f8" stroke="{MOR}" stroke-width="2"/>'); b.append(T(x,y+18,'30S',10,MOR,w='bold'))
b.append(T(465,398,'ribosoma 70S',11,MOR))
# folato
b.append(tbox(420,166,120,32,'vía del folato','#e8f5ee',VERDE,12,VERDE,'bold',8))
# etiquetas
L=[ (20,96,'PARED CELULAR',['β-lactámicos (penicilinas, cefalosporinas,','carbapenems, aztreonam): PBP','Vancomicina (D-Ala-D-Ala), bacitracina'],'#8a6a3a',(252,140)),
    (20,236,'ADN / ARN',['Fluoroquinolonas: ADN girasa y topo IV','Rifampicina: ARN polimerasa','Metronidazol, nitrofurantoína: dañan ADN'],AZUL,(360,250)),
    (20,376,'RIBOSOMA 30S',['Aminoglucósidos (bactericidas)','Tetraciclinas'],MOR,(348,364)),
    (730,96,'MEMBRANA',['Polimixinas (colistina)','Daptomicina'],'#b58a2a',(706,170)),
    (730,206,'FOLATO',['Sulfonamidas','Trimetoprim','(juntos: cotrimoxazol)'],VERDE,(540,182)),
    (730,326,'RIBOSOMA 50S',['Macrólidos (eritro-, azitro-,','claritromicina), clindamicina,','cloranfenicol, linezolid'],MOR,(590,338))]
for x,y,t,ls,c,(tx,ty) in L:
    b.append(T(x,y,t,13,c,'start','bold')); b.append(TL(x,y+19,ls,12,'#333','start',lh=17))
    ax = x+225 if x<300 else x-6
    b.append(line(ax,y-4,tx,ty,c,1.5,'4 3')); b.append(circ(tx,ty,4,c))
b.append(T(W/2,470,'Regla: 30S → «A» y «T» (aminoglucósidos, tetraciclinas); 50S → macrólidos, clindamicina, cloranfenicol, linezolid.',12,GRIS))
b.append(T(W/2,492,'Bactericidas: β-lactámicos, vancomicina, aminoglucósidos, quinolonas. Bacteriostáticos: tetraciclinas, macrólidos, clindamicina, sulfas.',12,GRIS))
svg(G,'sitios-antibioticos.svg',W,H,''.join(b))

# 2. Vía del folato
W,H=940,330
b=[title(W,'Antagonistas del folato: bloqueo secuencial')]
st=[('PABA + pteridina',CLARO['g'],GRIS),('Ácido dihidrofólico (DHF)',CLARO['y'],AMA),('Ácido tetrahidrofólico (THF)',CLARO['v'],VERDE),('Purinas y timidina → ADN',CLARO['a'],AZUL)]
xs=[20,260,500,740]
for (t,f,c),x in zip(st,xs): b.append(tbox(x,90,190,56,[t] if len(t)<20 else t.split(' (') if '(' in t else [t],f,c,13,'#222','bold'))
b.append(arrow(212,118,258,118,GRIS,3)); b.append(arrow(452,118,498,118,GRIS,3)); b.append(arrow(692,118,738,118,GRIS,3))
b.append(T(226,176,'Dihidropteroato',12,'#222','end')); b.append(T(226,192,'sintasa',12,'#222','end'))
b.append(drug(235,226,'Sulfonamidas',ROJO)); b.append(block(235,212,235,128,ROJO))
b.append(T(466,176,'Dihidrofolato',12,'#222','end')); b.append(T(466,192,'reductasa (DHFR)',12,'#222','end'))
b.append(drug(475,226,'Trimetoprim',ROJO)); b.append(block(475,212,475,128,ROJO))
b.append(T(475,256,'(en humanos la DHFR la bloquea el metotrexato)',11,GRIS))
b.append(box(20,276,900,42,CLARO['g'],'#ccc',10,1))
b.append(T(470,302,'Cada uno solo es bacteriostático; juntos (cotrimoxazol, 1:5) son sinérgicos y bactericidas. El humano no sintetiza folato: lo toma de la dieta.',12,'#333'))
svg(G,'folato.svg',W,H,''.join(b))

# 3. Tuberculosis: esquema y dianas
W,H=960,470
b=[title(W,'Tuberculosis: esquema de 6 meses y dónde actúa cada fármaco')]
x0=40; mw=140
b.append(box(x0,76,2*mw,54,VERDE,VERDE,8)); b.append(T(x0+mw,100,'Fase intensiva · 2 meses',14,'#fff',w='bold')); b.append(T(x0+mw,120,'I + R + P (+ E o S si hay resistencia)',12,'#fff'))
b.append(box(x0+2*mw+4,76,4*mw-4,54,TEAL,TEAL,8)); b.append(T(x0+4*mw,100,'Fase de continuación · 4 meses',14,'#fff',w='bold')); b.append(T(x0+4*mw,120,'I + R',12,'#fff'))
for m in range(7): b.append(line(x0+m*mw,134,x0+m*mw,142,GRIS,1.5)); b.append(T(x0+m*mw,158,f'mes {m}',11,GRIS))
# micobacteria
cx,cy=470,300
b.append(f'<rect x="{cx-170}" y="{cy-80}" width="340" height="160" rx="80" fill="#fff3d6" stroke="#8a6a3a" stroke-width="12"/>')
b.append(f'<rect x="{cx-158}" y="{cy-68}" width="316" height="136" rx="68" fill="#fffaf0" stroke="#c9a54a" stroke-width="3"/>')
b.append(T(cx,cy-92,'pared rica en ácidos micólicos y arabinogalactano',11,'#8a6a3a'))
b.append(path(f'M{cx-90},{cy} C{cx-60},{cy-30} {cx-30},{cy+30} {cx},{cy} S{cx+60},{cy-30} {cx+90},{cy}',AZUL,3)); b.append(T(cx,cy+30,'ADN → ARN',12,AZUL,w='bold'))
D4=[(40,196,'Isoniacida (I)',['Inhibe la síntesis de ácidos','micólicos (activada por KatG)','RAM: hepatitis, neuropatía','(dar piridoxina)'],(cx-140,cy-74)),
    (40,340,'Etambutol (E)',['Inhibe arabinosil transferasa','(arabinogalactano)','RAM: neuritis óptica','(no en niños)'],(cx-160,cy+40)),
    (720,196,'Rifampicina (R)',['Inhibe ARN polimerasa','RAM: orina/lágrimas naranjas,','hepatitis, inductor de CYP'],(cx+40,cy-4)),
    (720,340,'Pirazinamida (P)',['Activa en pH ácido (pirazinamidasa)','RAM: hiperuricemia (gota),','hepatotoxicidad'],(cx+150,cy+30))]
for x,y,t,ls,(tx,ty) in D4:
    b.append(drug(x,y,t,ROJO,12,'start')); b.append(TL(x,y+26,ls,12,'#333','start',lh=16))
    ax=x+190 if x<300 else x-6
    b.append(line(ax,y,tx,ty,ROJO,1.5,'4 3')); b.append(circ(tx,ty,4,ROJO))
b.append(T(W/2,452,'Siempre combinado (evita resistencia). Dosis: INH 5 mg/kg · RIF 10 mg/kg · PZA 30 mg/kg. Estreptomicina: no en embarazo.',12,GRIS))
svg(G,'tuberculosis.svg',W,H,''.join(b))

# 4. Antimicóticos
W,H=960,470
b=[title(W,'Antimicóticos: dianas en la célula del hongo')]
cx,cy=360,280
b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="230" ry="160" fill="#eef6ea" stroke="#5a7a3a" stroke-width="12"/>')
b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="214" ry="144" fill="#fffaf0" stroke="#d6a84a" stroke-width="4"/>')
b.append(T(cx,cy-170,'pared: β-1,3-glucano y quitina',11,'#5a7a3a',w='bold')); b.append(T(cx,cy-112,'membrana con ERGOSTEROL',11,'#b58a2a',w='bold'))
b.append(f'<ellipse cx="{cx+90}" cy="{cy+40}" rx="70" ry="50" fill="#e6effa" stroke="{AZUL}" stroke-width="2"/>'); b.append(T(cx+90,cy+44,'núcleo (ADN/ARN)',11,AZUL,w='bold'))
# vía ergosterol
for i,(t,c) in enumerate((('Escualeno',GRIS),('Lanosterol',AMA),('Ergosterol',NAR))):
    b.append(tbox(cx-170,cy-90+i*66,110,30,t,'#fff',c,12,c,'bold',8))
    if i<2: b.append(arrow(cx-115,cy-58+i*66,cx-115,cy-26+i*66,GRIS,2,8))
b.append(T(cx-122,cy-38,'escualeno',10,'#333','end')); b.append(T(cx-122,cy-26,'epoxidasa',10,'#333','end')); b.append(T(cx-122,cy+28,'14α-des-',10,'#333','end')); b.append(T(cx-122,cy+40,'metilasa',10,'#333','end'))
# fármacos
b.append(drug(720,110,'Equinocandinas (caspofungina)',ROJO,12)); b.append(T(720,132,'inhiben la síntesis de glucano (pared)',11,GRIS)); b.append(block(620,112,cx+150,cy-140,ROJO,2))
b.append(drug(720,170,'Terbinafina',ROJO,12)); b.append(T(720,192,'escualeno epoxidasa',11,GRIS)); b.append(block(680,172,cx-106,cy-42,ROJO,2))
b.append(drug(720,230,'Azoles (fluconazol, itraconazol…)',ROJO,12)); b.append(T(720,252,'14-α-desmetilasa del lanosterol',11,GRIS)); b.append(block(626,232,cx-106,cy+24,ROJO,2))
b.append(drug(720,290,'Polienos (anfotericina B, nistatina)',ROJO,12)); b.append(T(720,312,'se unen al ergosterol → poros',11,GRIS)); b.append(block(620,292,cx+212,cy-10,ROJO,2))
b.append(drug(720,350,'Flucitosina',ROJO,12)); b.append(T(720,372,'→ 5-FU dentro del hongo: ADN/ARN',11,GRIS)); b.append(block(684,352,cx+150,cy+46,ROJO,2))
b.append(drug(720,410,'Griseofulvina',ROJO,12)); b.append(T(720,432,'microtúbulos: frena la mitosis',11,GRIS)); b.append(block(678,412,cx+60,cy+100,ROJO,2))
b.append(T(30,456,'Los azoles también inhiben CYP humanos (interacciones); la anfotericina B es nefrotóxica.',12,GRIS,'start'))
svg(G,'antimicoticos.svg',W,H,''.join(b))

# 5. Ciclo del VIH
W,H=960,450
b=[title(W,'Ciclo del VIH y dónde actúa cada familia de antirretrovirales')]
st=[('1','Unión','gp120 a CD4','y CCR5/CXCR4'),('2','Fusión','gp41: entra','la cápside'),('3','Transcripción','inversa: ARN','viral → ADN'),
    ('4','Integración','el ADN viral','entra al genoma'),('5','Transcripción','y traducción:','poliproteínas'),('6','Ensamblaje,','gemación y','maduración')]
for i,(n,a,bb,c) in enumerate(st):
    x=20+i*157
    b.append(box(x,74,140,112,CLARO['m'],MOR,12,2))
    b.append(circ(x+20,94,13,MOR)); b.append(T(x+20,99,n,13,'#fff',w='bold'))
    b.append(TL(x+76,126,[a,bb,c],13,'#222',lh=18))
    if i<5: b.append(arrow(x+141,130,x+156,130,GRIS,2,7))
b.append(T(W/2,60,'(todo ocurre dentro del linfocito T CD4+)',12,MOR))
dr=[(0,['Maraviroc'],'antagonista de CCR5'),(1,['Enfuvirtida'],'se une a gp41'),
    (2,['ITIAN: zidovudina,','tenofovir, emtricitabina','ITINN: efavirenz,','nevirapina'],'TI = transcriptasa inversa'),
    (3,['Raltegravir,','dolutegravir'],'inhibidores de integrasa'),(5,['Saquinavir, ritonavir','(«-navir»)'],'inhibidores de proteasa')]
for i,ls,sub in dr:
    x=20+i*157+70
    b.append(block(x,288-38+0 if False else 252,x,190,ROJO,2.5))
    b.append(box(x-72,254,144,22+18*len(ls),ROJO,ROJO,10,1))
    b.append(TL(x,254+(22+18*len(ls))/2-(len(ls)-1)*9+4,ls,12,'#fff','middle','bold',18))
    b.append(T(x,254+22+18*len(ls)+16,sub,11,GRIS))
b.append(T(20+4*157+70,272,'(aquí no actúa',11,GRIS)); b.append(T(20+4*157+70,288,'la clase vista)',11,GRIS))
b.append(box(20,390,920,48,CLARO['g'],'#ccc',10,1))
b.append(TL(480,410,['TAR: al menos 3 fármacos (p. ej. 2 ITIAN + 1 inhibidor de integrasa) para evitar resistencia.','El ritonavir a dosis bajas «potencia» a otros inhibidores de proteasa porque inhibe CYP3A4.'],12,'#333',lh=17))
svg(G,'ciclo-vih.svg',W,H,''.join(b))

# 6. Influenza y herpes
W,H=960,440
b=[title(W,'Antivirales de influenza y de herpes')]
# panel influenza
b.append(T(240,74,'Influenza',16,NAR,w='bold'))
b.append(f'<rect x="30" y="90" width="420" height="250" rx="30" fill="#fffaf0" stroke="#d6a84a" stroke-width="3"/>')
b.append(T(60,112,'célula respiratoria',11,GRIS,'start'))
b.append(circ(120,180,30,'#fde2cf',NAR,2)); b.append(T(120,184,'virus',11,NAR,w='bold')); b.append(T(120,226,'endosoma:',11,GRIS)); b.append(T(120,240,'desnudamiento',11,GRIS))
b.append(box(146,168,14,24,'#fff',AZUL,3)); b.append(T(168,160,'canal M2',11,AZUL,'start','bold'))
b.append(tbox(210,250,130,34,'ARN pol: endonucleasa','#fff',MOR,11,MOR,'bold',8))
b.append(circ(400,120,22,'#fde2cf',NAR,2)); b.append(T(400,124,'nuevo',10,NAR,w='bold'))
b.append(path('M390,140 L380,160',VERDE,6)); b.append(T(372,178,'neuraminidasa',11,VERDE,'end','bold'))
b.append(T(372,192,'(lo libera de la célula)',10,GRIS,'end'))
b.append(drug(130,370,'Amantadina, rimantadina',ROJO,11)); b.append(T(130,392,'M2 · solo influenza A',11,GRIS)); b.append(block(170,356,156,196,ROJO,2))
b.append(drug(275,330+70,'Baloxavir',ROJO,11)); b.append(T(275,422,'dosis única',11,GRIS)); b.append(block(275,388,275,286,ROJO,2))
b.append(drug(400,370,'Oseltamivir, zanamivir, peramivir',ROJO,11)); b.append(T(400,392,'neuraminidasa · A y B',11,GRIS)); b.append(block(400,356,384,162,ROJO,2))
# panel herpes
b.append(T(730,74,'Herpes (VHS, VVZ) y CMV',16,MOR,w='bold'))
st=[('Aciclovir','#fff',GRIS),('Aciclovir-monofosfato','#fff',AMA),('Aciclovir-trifosfato','#fff',ROJO)]
for i,(t,f,c) in enumerate(st):
    b.append(tbox(520,96+i*84,180,40,t,f,c,13,c,'bold',8))
    if i<2: b.append(arrow(610,138+i*84,610,178+i*84,GRIS,2))
b.append(T(620,162,'timidina cinasa VIRAL',11,'#222','start','bold')); b.append(T(620,176,'(solo células infectadas)',10,GRIS,'start'))
b.append(T(620,246,'cinasas celulares',11,'#222','start'))
b.append(tbox(520,344,180,40,'ADN polimerasa viral','#e6effa',AZUL,13,AZUL,'bold',8)); b.append(block(610,306,610,342,ROJO,3))
b.append(T(610,402,'compite con dGTP y termina la cadena',11,'#333'))
b.append(TL(790,110,['Valaciclovir y','famciclovir: profármacos','orales (mejor F)','','Ganciclovir (CMV):','lo activa la cinasa UL97','','Foscarnet: no necesita','activarse (útil si hay','resistencia a TK)'],11,'#333','start',lh=15))
svg(G,'influenza-herpes.svg',W,H,''.join(b))

# 7. Amebiasis y paludismo
W,H=960,430
b=[title(W,'Antiparasitarios: según dónde está el parásito')]
b.append(T(240,74,'Amebiasis (E. histolytica)',15,TEAL,w='bold'))
b.append(tbox(30,92,200,110,['LUZ INTESTINAL','quistes y trofozoítos'],CLARO['y'],AMA,13,'#222','bold'))
b.append(tbox(250,92,200,110,['PARED Y TEJIDOS','colitis, absceso','hepático'],CLARO['r'],ROJO,13,'#222','bold'))
b.append(TL(130,226,['Amebicidas LUMINALES:','diloxanida, yodoquinol,','paromomicina','(portador asintomático)'],12,'#333',lh=17))
b.append(TL(350,226,['Amebicidas TISULARES:','metronidazol, tinidazol,','emetina; cloroquina','(hígado)'],12,'#333',lh=17))
b.append(box(30,310,420,64,CLARO['g'],'#ccc',10,1)); b.append(TL(240,334,['Colitis o absceso: metronidazol y DESPUÉS un luminal','para erradicar los quistes que quedan en la luz.'],12,'#333',lh=18))
# paludismo
b.append(T(720,74,'Paludismo (Plasmodium)',15,MOR,w='bold'))
b.append(tbox(500,92,140,60,['Mosquito','Anopheles'],CLARO['g'],GRIS,13))
b.append(tbox(660,92,140,60,['Fase hepática','(hipnozoítos: vivax,','ovale)'],CLARO['n'],NAR,12))
b.append(tbox(820,92,120,60,['Fase','eritrocítica','(fiebre)'],CLARO['r'],ROJO,12))
b.append(arrow(642,122,658,122,GRIS,2,8)); b.append(arrow(802,122,818,122,GRIS,2,8))
b.append(path('M880,154 C880,200 570,200 570,156',GRIS,2,'none','5 4')); b.append(arrow(572,166,570,154,GRIS,2,8)); b.append(T(560,212,'gametocitos → mosquito',11,GRIS,'start'))
b.append(drug(730,250,'Primaquina',ROJO,12)); b.append(TL(730,276,['hepática y gametocitos','(evita recaídas; ver G6PD)'],11,GRIS))
b.append(drug(880,250,'Cloroquina',ROJO,12)); b.append(TL(880,276,['de elección','eritrocítica'],11,GRIS))
b.append(drug(730,330,'Quinina / quinidina',ROJO,12)); b.append(drug(880,330,'Artemisinina',ROJO,12)); b.append(TL(880,356,['grave o','multirresistente'],11,GRIS))
b.append(block(730,236,730,154,ROJO,2)); b.append(block(880,236,880,154,ROJO,2))
b.append(T(W/2,414,'Helmintos: nematodos → mebendazol, albendazol, pirantel, ivermectina; trematodos → prazicuantel; cestodos → niclosamida, prazicuantel, albendazol.',12,GRIS))
svg(G,'antiparasitarios.svg',W,H,''.join(b))

# 8. Parkinson: sinapsis dopaminérgica
W,H=960,480
b=[title(W,'Parkinson: cómo aumentar la dopamina (y frenar la ACh)')]
# periferia
b.append(box(20,70,300,380,'#f7f7f7','#bbb',14,1.5)); b.append(T(170,94,'PERIFERIA (sangre, intestino)',12,GRIS,w='bold'))
b.append(tbox(70,110,200,36,'Levodopa (oral)','#fff',VERDE,13,VERDE,'bold',8))
b.append(arrow(170,148,170,210,GRIS,2)); b.append(T(180,170,'DOPA',11,'#333','start')); b.append(T(180,184,'descarboxilasa',11,'#333','start'))
b.append(drug(96,172,'Carbidopa',ROJO,11)); b.append(block(136,172,164,176,ROJO,2)); b.append(T(96,196,'(o benserazida)',10,GRIS))
b.append(tbox(70,212,200,46,['Dopamina periférica','(náusea, hipotensión)'],'#fff',GRIS,12,'#333','normal',8))
b.append(drug(170,296,'Entacapona (COMT)',ROJO,11)); b.append(T(170,318,'↓ degradación periférica',11,GRIS))
b.append(TL(170,358,['Carbidopa y entacapona','no cruzan la BHE'],11,GRIS))
b.append(T(170,410,'→ más levodopa llega al cerebro',12,VERDE,w='bold'))
# BHE
b.append(f'<rect x="336" y="70" width="16" height="380" fill="#e9c46a"/>'); b.append(f'<text x="344" y="300" font-size="11" fill="#8a6a00" text-anchor="middle" transform="rotate(-90 344 300)">barrera hematoencefálica</text>')
b.append(arrow(272,128,424,186,VERDE,3)); b.append(T(360,110,'cruza la BHE (transportador de aminoácidos)',11,VERDE,'start'))
# neurona nigroestriada
b.append(path('M370,140 H700 V250 C700,290 660,300 620,300 H450 C410,300 370,290 370,250Z',VERDE,2.5,CLARO['v']))
b.append(T(390,162,'Neurona de la sustancia negra',12,VERDE,'start','bold'))
b.append(tbox(424,180,110,30,'L-DOPA → DA','#fff',VERDE,12,VERDE,'bold',8))
for x,y in ((500,250),(570,262),(630,240)): b.append(circ(x,y,18,'#fff',VERDE,2)); b.append(T(x,y+4,'DA',10,VERDE,w='bold'))
b.append(tbox(590,180,90,28,'MAO-B','#fff',GRIS,12,'#222','bold',8))
for x in (500,540,580,620): b.append(circ(x,320,4,VERDE))
b.append(path('M370,340 H700 V420 H370Z',MOR,2.5,CLARO['m'])); b.append(T(390,410,'Neurona del estriado',12,MOR,'start','bold'))
b.append(box(520,330,44,24,'#fff',MOR,5)); b.append(T(542,347,'D₂',12,MOR,w='bold'))
b.append(box(620,330,44,24,'#fff','#888',5)); b.append(T(642,347,'M',12,'#555',w='bold'))
# fármacos derecha
b.append(drug(830,186,'Selegilina, rasagilina (MAO-B)',ROJO,11)); b.append(block(744,186,682,192,ROJO,2))
b.append(drug(830,246,'Amantadina: ↑ liberación',VERDE,11)); b.append(arrow(752,246,652,250,VERDE,2,8))
b.append(drug(830,306,'Agonistas: pramipexol, ropinirol,',VERDE,11)); b.append(T(830,328,'bromocriptina, apomorfina (D₂)',11,'#333')); b.append(arrow(740,306,566,336,VERDE,2,8))
b.append(drug(830,372,'Antimuscarínicos: trihexifenidilo,',ROJO,11)); b.append(T(830,394,'biperideno (temblor)',11,'#333')); b.append(block(740,372,666,346,ROJO,2))
W,H=960,500
b.append(T(480,484,'En el Parkinson falta dopamina y sobra acetilcolina en el estriado. El haloperidol (bloquea D₂) lo puede provocar.',12,GRIS))
svg(G,'parkinson.svg',W,H,''.join(b))

# 9. Célula β y secretagogos
W,H=960,450
b=[title(W,'Célula β: cómo se libera la insulina y dónde actúan los secretagogos')]
b.append(f'<rect x="200" y="90" width="460" height="300" rx="40" fill="#f2f8f4" stroke="{VERDE}" stroke-width="3"/>')
b.append(T(430,114,'Célula β del páncreas',13,VERDE,w='bold'))
b.append(T(110,170,'Glucosa',14,'#222','middle','bold')); b.append(arrow(150,166,226,166,GRIS,2.5))
b.append(box(214,152,24,30,'#fff',AZUL,5)); b.append(T(226,206,'GLUT2',11,AZUL,w='bold'))
b.append(T(320,170,'glucosa → metabolismo',12,'#333','middle')); b.append(arrow(320,180,320,216,GRIS,2)); b.append(T(320,234,'↑ ATP / ADP',13,'#222','middle','bold'))
b.append(arrow(370,232,628,232,GRIS,2))
b.append(box(632,214,36,40,'#fff',NAR,6)); b.append(T(694,226,'canal K⁺-ATP',11,NAR,'start','bold')); b.append(T(694,242,'(SUR1) se CIERRA',11,NAR,'start'))
b.append(T(560,280,'despolarización',12,'#333')); b.append(arrow(560,288,560,316,GRIS,2))
b.append(box(632,300,36,40,'#fff',AZUL,6)); b.append(T(694,318,'canal de Ca²⁺',11,AZUL,'start','bold')); b.append(T(694,334,'se ABRE → entra Ca²⁺',11,AZUL,'start'))
b.append(T(470,336,'Ca²⁺ ↑ → exocitosis',13,'#222','middle','bold'))
for x in (300,350,400): b.append(circ(x,350,16,'#fff',VERDE,2)); b.append(T(x,354,'Ins',9,VERDE,w='bold'))
b.append(arrow(300,368,300,420,VERDE,3)); b.append(T(312,416,'insulina a la sangre',12,VERDE,'start','bold'))
b.append(drug(820,110,'Sulfonilureas, glinidas',ROJO,12)); b.append(T(820,132,'cierran el K⁺-ATP aunque',11,GRIS)); b.append(T(820,146,'no haya glucosa → hipoglucemia',11,GRIS)); b.append(block(760,156,672,216,ROJO,2))
b.append(drug(820,380,'GLP-1 e iDPP-4 (incretinas)',VERDE,12)); b.append(T(820,402,'↑ AMPc: potencian la secreción',11,GRIS)); b.append(T(820,416,'solo si hay glucosa (poca hipoglucemia)',11,GRIS)); b.append(arrow(730,374,420,344,VERDE,2,8))
b.append(T(30,440,'El diazóxido hace lo contrario: abre el K⁺-ATP y frena la secreción.',12,GRIS,'start'))
svg(G,'celula-beta.svg',W,H,''.join(b))

# 10. Dónde actúa cada familia de hipoglucemiantes
W,H=960,440
b=[title(W,'Hipoglucemiantes: el órgano en el que actúa cada familia')]
org=[(480,100,'Páncreas',['Sulfonilureas, glinidas: ↑ secreción','GLP-1 / iDPP-4: ↑ insulina con glucosa','y ↓ glucagón'],NAR),
     (160,190,'Hígado',['Metformina: ↓ gluconeogénesis','(no da hipoglucemia; RAM: GI,','acidosis láctica, ↓ B12)'],'#7a4b2a'),
     (800,190,'Músculo y grasa',['Glitazonas (pioglitazona):','↑ sensibilidad (PPAR-γ)','RAM: edema, ↑ peso, IC'],ROJO),
     (160,340,'Intestino',['Acarbosa, miglitol:','retrasan la absorción de','carbohidratos (flatulencia)'],AMA),
     (800,340,'Riñón',['iSGLT2 (gliflozinas):','glucosuria; protegen corazón','y riñón; RAM: infecc. genitales'],AZUL)]
cx,cy=480,280
b.append(circ(cx,cy,56,CLARO['r'],ROJO,2)); b.append(T(cx,cy-4,'Glucemia',14,ROJO,w='bold')); b.append(T(cx,cy+18,'↓',18,ROJO,w='bold'))
for x,y,t,ls,c in org:
    b.append(box(x-140,y-40,280,96,'#fff',c,10,2))
    b.append(T(x,y-16,t,14,c,w='bold')); b.append(TL(x,y+6,ls,12,'#222',lh=16))
    ex,ey=(x,y+56) if x==480 else ((x+140,y+8) if x<480 else (x-140,y+8))
    a=math.atan2(ey-cy,ex-cx); b.append(line(ex,ey,cx+60*math.cos(a),cy+60*math.sin(a),c,2,'5 4'))
svg(G,'hipoglucemiantes.svg',W,H,''.join(b))

# 11. Síntesis de hormonas tiroideas
W,H=960,470
b=[title(W,'Síntesis de hormonas tiroideas y dónde actúan los antitiroideos')]
b.append(box(40,110,170,260,CLARO['r'],ROJO,12)); b.append(T(125,134,'Capilar',13,ROJO,w='bold'))
b.append(box(230,90,420,300,'#fff7ec',NAR,20,2.5)); b.append(T(440,114,'Célula folicular',13,NAR,w='bold'))
b.append(box(670,110,250,260,'#fff3c4',AMA,40,2)); b.append(T(795,134,'Coloide (tiroglobulina)',13,'#8a6a00',w='bold'))
b.append(T(125,180,'I⁻ (yoduro)',13,'#222','middle','bold')); b.append(arrow(166,176,258,176,MOR,2.5)); b.append(box(242,164,22,24,'#fff',MOR,5)); b.append(T(272,160,'NIS',11,MOR,'start','bold'))
b.append(arrow(300,180,660,180,MOR,2)); b.append(T(470,170,'I⁻ va al coloide',11,MOR))
b.append(tbox(700,160,190,64,['TPO: oxida I⁻, lo une','a tirosinas (MIT, DIT)','y las acopla → T4, T3'],'#fff',NAR,12,'#222'))
b.append(arrow(780,226,780,280,GRIS,2)); b.append(tbox(700,282,190,40,'Tiroglobulina con T4/T3','#fff',AMA,12,'#222','bold',8))
b.append(arrow(698,302,420,302,GRIS,2)); b.append(T(560,294,'endocitosis y proteólisis',11,GRIS))
b.append(arrow(300,302,170,302,GRIS,3)); b.append(T(125,300,'T4 (90 %)',13,'#222','middle','bold')); b.append(T(125,318,'T3 (10 %)',13,'#222','middle','bold'))
b.append(T(125,350,'periferia: T4 → T3',11,GRIS)); b.append(T(125,364,'(desyodasa)',11,GRIS))
b.append(drug(330,232,'Perclorato, tiocianato',ROJO,11)); b.append(block(330,218,256,190,ROJO,2))
b.append(drug(560,250,'Metimazol, PTU',ROJO,12)); b.append(block(620,248,700,200,ROJO,2))
b.append(drug(440,350,'Yodo en exceso (Lugol)',ROJO,11)); b.append(T(440,372,'frena la liberación (Wolff-Chaikoff)',11,GRIS)); b.append(block(440,336,440,306,ROJO,2))
b.append(drug(125,410,'PTU, propranolol',ROJO,11)); b.append(T(125,432,'↓ conversión T4 → T3',11,GRIS)); b.append(block(125,396,125,370,ROJO,2))
b.append(T(560,418,'Yodo-131: destruye tejido. Levotiroxina (T4) = reemplazo en hipotiroidismo.',12,GRIS))
b.append(T(560,438,'PTU en el 1er trimestre del embarazo; metimazol en el resto (el PTU es más hepatotóxico).',12,GRIS))
svg(G,'tiroides.svg',W,H,''.join(b))

# 12. Receptor GABA-A
W,H=940,440
b=[title(W,'Receptor GABA-A: dónde se unen BZD, hipnóticos Z y barbitúricos')]
b.append(membrane(40,580,190,40))
cx=300
sub=[(-120,'γ','#fde2cf'),(-70,'α','#bfe1dc'),(-20,'β','#d9c7ec'),(70,'α','#bfe1dc'),(120,'β','#d9c7ec')]
for dx,t,c in sub:
    b.append(box(cx+dx-22,120,44,180,c,'#666',16,1.5)); b.append(T(cx+dx,214,t,16,'#333',w='bold'))
b.append(arrow(cx+25,108,cx+25,330,VERDE,3)); b.append(T(cx+25,98,'Cl⁻',14,VERDE,'middle','bold'))
b.append(T(cx+25,354,'canal abierto: entra Cl⁻ → hiperpolarización → menos excitabilidad',12,VERDE,'middle','bold'))
b.append(circ(cx+2,128,9,AZUL)); b.append(T(cx-14,104,'GABA',11,AZUL,'end','bold')); b.append(line(cx-12,106,cx-2,120,AZUL,1.2))
b.append(circ(cx-95,128,9,NAR)); b.append(T(cx-146,126,'sitio BZD',11,NAR,'end','bold')); b.append(T(cx-146,140,'(entre α y γ)',11,NAR,'end'))
b.append(drug(730,110,'Benzodiacepinas, hipnóticos Z',NAR,12)); b.append(T(730,132,'↑ FRECUENCIA de apertura',11,GRIS)); b.append(T(730,146,'(necesitan GABA → techo de seguridad)',11,GRIS)); b.append(path(f'M626,110 C500,70 {cx-60},70 {cx-90},118',NAR,1.6,'none','4 4'))
b.append(drug(730,210,'Barbitúricos',ROJO,12)); b.append(T(730,232,'↑ DURACIÓN de apertura; a dosis altas',11,GRIS)); b.append(T(730,246,'abren el canal sin GABA → coma',11,GRIS)); b.append(line(678,210,cx+142,210,ROJO,1.6,'4 3'))
b.append(drug(730,300,'Flumazenil',VERDE,12)); b.append(T(730,322,'compite por el sitio BZD (antídoto)',11,GRIS)); b.append(T(730,336,'no revierte barbitúricos ni alcohol',11,GRIS))
b.append(box(40,380,860,46,CLARO['g'],'#ccc',10,1))
b.append(T(470,408,'Alcohol + BZD o barbitúricos = depresión respiratoria sumada. La buspirona NO actúa aquí (agonista parcial 5-HT1A).',12,'#333'))
svg(G,'gaba-a.svg',W,H,''.join(b))
