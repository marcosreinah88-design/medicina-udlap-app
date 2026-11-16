# Esquemas propios (SVG, en español) de patología general para la guía de Biología Celular y Molecular (2º):
# lesión y muerte celular, adaptaciones, tipos de necrosis, inflamación, granuloma y neoplasias.
# Dibujados desde cero: no copian figuras de libros.
# Uso: python3 tools-s12/esquemas_patologia.py      (escribe en tools-s12/img/biologia-celular/)
import math, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
GID = 'biologia-celular'
F = 'font-family="Helvetica,Arial,sans-serif"'
ROJO='#b3261e'; VERDE='#00573c'; NAR='#f26b21'; AZUL='#2b6cb0'; MOR='#7b3fa0'; GRIS='#555'; AMA='#e0a800'
ROSA='#f6cfdc'; ROSA2='#ec9fb8'; NUC='#5b3b8c'; NUC2='#8a6cc0'
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
def box(x,y,w,h,fill,stroke,r=10,sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def tbox(x,y,w,h,lines,fill,stroke,size=14,c='#222',wt='normal'):
    n=len(lines); lh=size*1.25; y0=y+h/2-(n-1)*lh/2+size*.35
    return box(x,y,w,h,fill,stroke)+TL(x+w/2,y0,lines,size,c,'middle',wt,lh)
def circ(cx,cy,r,fill,stroke='none',sw=1.5,extra=''):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'
def ell(cx,cy,rx,ry,fill,stroke='none',sw=1.5,rot=0):
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" transform="rotate({rot} {cx:.1f} {cy:.1f})"/>'
def blob(cx,cy,r,fill,stroke,sw=2,wob=.12,k=5,seed=0,n=40):
    rnd=random.Random(seed); ph=rnd.random()*6.28; ph2=rnd.random()*6.28
    pts=[(cx+r*(1+wob*math.sin(k*t+ph)+wob*.5*math.sin((k+2)*t+ph2))*math.cos(t), cy+r*(1+wob*math.sin(k*t+ph)+wob*.5*math.sin((k+2)*t+ph2))*math.sin(t)) for t in [i/n*6.2832 for i in range(n)]]
    return f'<path d="M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+f'Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
def title(w,t,sub=None):
    o=T(w/2,30,t,20,VERDE,w='bold')
    if sub: o+=T(w/2,52,sub,13,GRIS)
    return o

# ───────── 1. Lesión reversible, necrosis y apoptosis ─────────
b=[title(900,'Lesión celular: reversible, necrosis y apoptosis','La necrosis rompe la membrana e inflama; la apoptosis encoge la célula sin inflamación')]
def cell_normal(cx,cy):
    o=blob(cx,cy,52,ROSA,'#c06080',2,.04,4,1)
    o+=circ(cx,cy,17,NUC2,NUC,2)
    for dx,dy in((-30,-18),(28,20),(-22,26)): o+=ell(cx+dx,cy+dy,9,5,'#f3a35c','#b8641e',1.2,30)
    return o
b.append(cell_normal(110,170)); b.append(T(110,250,'Célula normal',15,w='bold'))
# reversible
cx,cy=330,170
b.append(blob(cx,cy,66,'#fbe3ea','#c06080',2,.05,4,2))
for a in (0.5,1.6,2.7,4.0,5.3): b.append(circ(cx+66*math.cos(a)*1.02,cy+66*math.sin(a)*1.02,10,'#fbe3ea','#c06080',2))
b.append(circ(cx,cy,18,NUC2,NUC,2))
for dx,dy in((-34,-20),(32,22),(-26,30)): b.append(ell(cx+dx,cy+dy,14,9,'#f8c99b','#b8641e',1.2,30))
for dx,dy in((20,-30),(-40,8),(38,-6)): b.append(circ(cx+dx,cy+dy,6,'#fff','#c06080',1))
b.append(T(cx,262,'Lesión reversible',15,w='bold',c=AZUL))
b.append(TL(cx,282,['Tumefacción (entra agua: falla la bomba Na⁺/K⁺)','Ampollas, mitocondrias hinchadas, RE dilatado','Cambio graso (esteatosis)'],12,GRIS))
b.append(arrow(170,170,250,170,'#333'))
b.append(T(210,158,'Isquemia,',11,GRIS)); b.append(T(210,190,'tóxicos…',11,GRIS))
b.append(arrow(400,150,470,150,AZUL,2,9,'5,4')); b.append(T(435,140,'se quita',11,AZUL))
b.append(T(435,172,'la causa',11,AZUL))
b.append(arrow(470,182,400,182,AZUL,2,9,'5,4'))
# punto de no retorno
b.append(f'<line x1="500" y1="70" x2="500" y2="560" stroke="{ROJO}" stroke-width="2" stroke-dasharray="7,6"/>')
b.append(T(500,585,'Punto de no retorno: daño de la membrana y de la mitocondria',13,ROJO,w='bold'))
# necrosis
cx,cy=700,175
b.append(blob(cx,cy,64,'#f8d9e2','#c06080',2,.22,6,7))
for i in range(14):
    a=i/14*6.28; r=76+8*(i%3); y=cy+r*.8*math.sin(a)
    if 112<y<240: b.append(circ(cx+r*math.cos(a),y,3.5,'#e7a3b8'))
b.append(T(cx,98,'Necrosis',17,ROJO,w='bold'))
b.append(T(cx,268,'Membrana rota → sale el contenido → INFLAMACIÓN',12,ROJO,w='bold'))
# cambios nucleares
for i,(lab,kind) in enumerate((('Picnosis','p'),('Cariorrexis','r'),('Cariólisis','l'))):
    x=610+i*90; y=330
    b.append(blob(x,y,30,ROSA,'#c06080',1.5,.08,5,i+20))
    if kind=='p': b.append(circ(x,y,9,'#3b1f66'))
    if kind=='r':
        for dx,dy in((-8,-6),(7,-8),(-2,7),(10,6),(-11,6)): b.append(circ(x+dx,y+dy,3.6,'#3b1f66'))
    if kind=='l': b.append(circ(x,y,14,'#cbb8e6','#cbb8e6'))
    b.append(T(x,378,lab,12,w='bold'))
b.append(T(700,398,'(el núcleo se condensa, se rompe o se desvanece)',11,GRIS))
# neutrofilos llegando
for i,(x,y) in enumerate(((785,125),(805,195),(770,235))):
    b.append(circ(x,y,12,'#e6e0f2','#8a6cc0',1.2))
    b.append(f'<path d="M{x-6},{y-2} q3,-6 6,0 q3,6 6,0" stroke="{NUC}" stroke-width="3" fill="none"/>')
b.append(T(822,200,'neutrófilos',11,MOR,'start'))
# apoptosis
y0=470
b.append(T(700,y0-35,'Apoptosis',17,VERDE,w='bold'))
b.append(blob(560,y0+15,40,ROSA,'#c06080',2,.03,4,3)+circ(560,y0+15,14,'#3b1f66'))
b.append(T(560,y0+75,'Se encoge;',11,GRIS)); b.append(T(560,y0+89,'cromatina condensada',11,GRIS))
b.append(arrow(605,y0+15,640,y0+15,'#333',2,8))
for dx,dy,r in((0,0,15),(26,-14,11),(22,20,12),(-6,26,9)):
    b.append(circ(685+dx,y0+10+dy,r,ROSA,'#c06080',1.5)+circ(685+dx,y0+10+dy,r*.4,'#3b1f66'))
b.append(T(700,y0+75,'Cuerpos apoptóticos',11,GRIS)); b.append(T(700,y0+89,'(membrana íntegra)',11,GRIS))
b.append(arrow(735,y0+15,775,y0+15,'#333',2,8))
b.append(blob(830,y0+15,42,'#e9e4d2','#8c7a3c',2,.15,5,9)+circ(818,y0+12,10,ROSA,'#c06080',1.2)+circ(818,y0+12,4,'#3b1f66')+ell(845,y0+28,10,7,'#bfae7a'))
b.append(T(830,y0+75,'Macrófago los fagocita',11,GRIS)); b.append(T(830,y0+89,'SIN inflamación',11,VERDE,w='bold'))
# notas izq abajo
b.append(tbox(40,330,420,190,['','','Necrosis: patológica, grupos de células,','célula se hincha, membrana rota, inflamación.','','Apoptosis: programada (fisiológica o patológica),','células sueltas, se encoge, necesita ATP,','sin inflamación (caspasas).'],'#f7f7f2','#bbb',13)); b.append(T(250,372,'Necrosis vs apoptosis',15,'#222',w='bold'))
svg('lesion-celular.svg',900,600,''.join(b))

# ───────── 2. Vías de la apoptosis ─────────
b=[title(900,'Vías de la apoptosis','Las dos vías terminan en las caspasas efectoras 3 y 7')]
def fl(x,y,w,h,txt,fill,stroke,size=13,wt='normal'): return tbox(x,y,w,h,txt,fill,stroke,size,'#222',wt)
# intrinseca
b.append(T(220,88,'Vía intrínseca (mitocondrial)',16,AZUL,w='bold'))
b.append(fl(60,104,320,52,['Daño del ADN (p53), falta de factores','de crecimiento, estrés, radiación'],'#e8f0fa',AZUL))
b.append(arrow(220,156,220,182,AZUL))
b.append(fl(60,184,320,52,['Bax y Bak (proapoptóticos)','vencen a Bcl-2 / Bcl-xL'],'#e8f0fa',AZUL))
b.append(arrow(220,236,220,262,AZUL))
# mitocondria dibujo
b.append(ell(220,300,110,34,'#f8c99b','#b8641e',2))
b.append(f'<path d="M130,300 q15,-22 30,0 t30,0 t30,0 t30,0 t30,0 t30,0" fill="none" stroke="#b8641e" stroke-width="2"/>')
for i in range(5): b.append(circ(330+i*14,286+(i%2)*14,5,ROJO))
b.append(T(395,330,'citocromo c sale',12,ROJO,'start'))
b.append(arrow(220,334,220,362,AZUL))
b.append(fl(60,364,320,52,['Apoptosoma (citocromo c + Apaf-1)','→ caspasa 9 (iniciadora)'],'#e8f0fa',AZUL,13,'bold'))
# extrinseca
b.append(T(680,88,'Vía extrínseca (receptores de muerte)',16,MOR,w='bold'))
b.append(fl(520,104,320,52,['FasL (linfocito T) o TNF','se une a su receptor (Fas, TNFR1)'],'#f2ebf8',MOR))
# receptor dibujo
b.append(f'<line x1="520" y1="214" x2="790" y2="214" stroke="#c06080" stroke-width="6"/>')
b.append(T(798,218,'membrana',11,GRIS,'start'))
for x in (640,680,720):
    b.append(f'<rect x="{x-5}" y="188" width="10" height="48" rx="4" fill="{MOR}"/>')
    b.append(circ(x,180,10,'#d8c4ee',MOR,1.5))
b.append(arrow(680,156,680,170,MOR,2,8))
b.append(arrow(680,240,680,262,MOR))
b.append(fl(520,264,320,52,['Dominio de muerte (FADD)','→ caspasa 8 (iniciadora)'],'#f2ebf8',MOR,13,'bold'))
b.append(fl(600,350,280,66,['Linfocito T citotóxico: perforina','abre poros y la granzima B','activa caspasas directamente'],'#f7f7f2','#999',12))
b.append(arrow(700,416,590,478,'#999',2,8,'4,4'))
# convergencia
b.append(arrow(220,416,380,470,AZUL)); b.append(arrow(545,316,545,470,MOR,2.5,10))
b.append(fl(300,472,300,56,['Caspasas efectoras 3 y 7'],'#fde8dc',NAR,16,'bold'))
b.append(arrow(450,528,450,552,NAR))
b.append(T(450,572,'Rompen el citoesqueleto y el ADN → cuerpos apoptóticos → fagocitosis sin inflamación',13,'#222'))
b.append(T(40,450,'Bcl-2 la frena (t(14;18) = linfoma folicular)',12,ROJO,'start'))
svg('apoptosis-vias.svg',900,595,''.join(b))

# ───────── 3. Adaptaciones celulares ─────────
b=[title(900,'Adaptaciones celulares','La célula cambia para sobrevivir al estímulo; la displasia ya no es adaptación')]
def epit(x0,y0,n,w,h,col='#f6cfdc',nuc=NUC2,kind='col'):
    o=''
    for i in range(n):
        x=x0+i*w
        if kind=='col':
            o+=f'<rect x="{x:.1f}" y="{y0-h:.1f}" width="{w:.1f}" height="{h}" fill="{col}" stroke="#c06080" stroke-width="1.5"/>'
            o+=ell(x+w/2,y0-h*.3,w*.28,h*.13,nuc,NUC,1)
    return o
panels=[('Normal',''),('Hipertrofia','↑ tamaño celular'),('Hiperplasia','↑ número de células'),('Atrofia','↓ tamaño o número'),('Metaplasia','un epitelio maduro cambia a otro'),('Displasia','desorden y atipia (precáncer)')]
PW=280; PH=230
for k,(t,s) in enumerate(panels):
    px=20+(k%3)*(PW+10); py=70+(k//3)*(PH+30)
    b.append(box(px,py,PW,PH,'#fcfcfa','#ddd',12,1.5))
    b.append(T(px+PW/2,py+26,t,17,VERDE if k<5 else ROJO,w='bold')); b.append(T(px+PW/2,py+46,s,12,GRIS))
    base=py+PH-36
    b.append(f'<line x1="{px+16}" y1="{base}" x2="{px+PW-16}" y2="{base}" stroke="#7a5a2a" stroke-width="3"/>')
    if k==0: b.append(epit(px+40,base,8,25,90))
    if k==1: b.append(epit(px+20,base,6,40,130).replace(f'rx="{40*.28:.1f}"',f'rx="{40*.28:.1f}"'))
    if k==2: b.append(epit(px+30,base,14,16,90))
    if k==3: b.append(epit(px+70,base,8,17,50))
    if k==4:
        b.append(epit(px+18,base,4,25,90))
        b.append(f'<line x1="{px+120}" y1="{base-100}" x2="{px+120}" y2="{base}" stroke="#999" stroke-dasharray="4,3"/>')
        for r in range(4):
            for i in range(5 if r<3 else 6):
                xx=px+128+i*26+(13 if r%2 else 0); yy=base-10-r*20
                if xx>px+PW-30: continue
                fl_=1-r*.2
                b.append(ell(xx,yy,13,9*fl_+1,'#f6cfdc','#c06080',1.2)+ell(xx,yy,4,3*fl_+.5,NUC2))
        b.append(T(px+70,base+22,'cilíndrico',11,GRIS)); b.append(T(px+200,base+22,'plano estratificado',11,GRIS))
    if k==5:
        rnd=random.Random(5)
        for i in range(36):
            xx=px+30+rnd.random()*(PW-60); yy=base-12-rnd.random()*100
            r=7+rnd.random()*7
            b.append(blob(xx,yy,r+5,'#f6cfdc','#c06080',1,.2,4,i)+blob(xx,yy,r*.7,'#4a2a80','none',0,.25,3,i+50))
        b.append(T(px+PW/2,base+22,'núcleos grandes y oscuros, mitosis altas, sin orden',11,GRIS))
    if k==0: b.append(T(px+PW/2,base+22,'epitelio cilíndrico simple',11,GRIS))
    if k==1: b.append(T(px+PW/2,base+22,'músculo cardiaco en HTA, útero grávido',11,GRIS))
    if k==2: b.append(T(px+PW/2,base+22,'endometrio (estrógenos), próstata, bocio',11,GRIS))
    if k==3: b.append(T(px+PW/2,base+22,'desuso, denervación, isquemia, vejez',11,GRIS))
svg('adaptaciones.svg',900,600,''.join(b))

# ───────── 4. Tipos de necrosis ─────────
b=[title(900,'Patrones de necrosis','Qué se ve y dónde aparece cada uno')]
PW=280; PH=250
def panel(k,t,where,lines):
    px=20+(k%3)*(PW+10); py=66+(k//3)*(PH+16)
    o=box(px,py,PW,PH,'#fcfcfa','#ddd',12,1.5)+T(px+PW/2,py+26,t,17,ROJO,w='bold')+T(px+PW/2,py+45,where,12,AZUL,w='bold')
    o+=TL(px+PW/2,py+PH-38,lines,11.5,GRIS)
    return o,px+PW/2,py+128
# coagulativa
o,cx,cy=panel(0,'Coagulativa','Infarto de corazón y riñón',['Se conserva el contorno de las células','(«células fantasma» sin núcleo, eosinófilas)'])
b.append(o)
for i in range(4):
    for j in range(3):
        x=cx-80+i*48; y=cy-50+j*42
        b.append(f'<rect x="{x}" y="{y}" width="42" height="36" rx="5" fill="#f19bb7" stroke="#d07090" stroke-width="1.5"/>')
        if (i+j)%4==0: b.append(ell(x+21,y+18,6,5,'#c9b3e6','#c9b3e6'))
# licuefactiva
o,cx,cy=panel(1,'Licuefactiva','Cerebro (infarto) y abscesos',['Enzimas digieren el tejido: queda una','cavidad con líquido o pus'])
b.append(o)
b.append(blob(cx,cy,62,'#f6cfdc','#c06080',2,.05,4,30))
b.append(blob(cx,cy,38,'#fff6cf','#c9a227',2,.12,5,31))
rnd=random.Random(4)
for i in range(14):
    a=rnd.random()*6.28; r=rnd.random()*27
    b.append(circ(cx+r*math.cos(a),cy+r*math.sin(a),4,'#bba7d8'))
b.append(T(cx,cy+4,'pus',13,'#8a6d00',w='bold'))
# caseosa
o,cx,cy=panel(2,'Caseosa','Tuberculosis (y algunos hongos)',['Centro blanco amarillento tipo «queso»,','amorfo, rodeado por un granuloma'])
b.append(o)
for i in range(22):
    a=i/22*6.28
    b.append(ell(cx+50*math.cos(a),cy+50*math.sin(a),9,5,'#f6cfdc','#c06080',1,math.degrees(a)+90))
for i in range(40):
    a=i/40*6.28; b.append(circ(cx+64*math.cos(a),cy+64*math.sin(a),3.5,'#4a2a80'))
b.append(blob(cx,cy,36,'#f4ecd2','#c8b67a',1.5,.1,6,33))
b.append(T(cx,cy+5,'caseum',13,'#7a6a30',w='bold'))
# grasa
o,cx,cy=panel(3,'Grasa','Pancreatitis aguda, mama',['Lipasas liberan ácidos grasos que se','unen al Ca²⁺ (saponificación): manchas tiza'])
b.append(o)
for i in range(4):
    for j in range(3):
        b.append(circ(cx-66+i*44,cy-40+j*40,19,'#fff7d9','#d9c27a',1.5))
for x,y in ((cx-50,cy-20),(cx+28,cy+25),(cx+60,cy-40)):
    b.append(blob(x,y,14,'#f2f2f2','#9a9a9a',1.5,.25,5,int(x)))
# fibrinoide
o,cx,cy=panel(4,'Fibrinoide','Vasculitis, HTA maligna',['Inmunocomplejos y fibrina en la pared','del vaso: anillo rosa brillante'])
b.append(o)
b.append(circ(cx,cy,58,'#f6cfdc','#c06080',2))
b.append(circ(cx,cy,56,'none','#e0457a',14,' stroke-opacity="0.75"'))
b.append(circ(cx,cy,26,'#fff','#c06080',2))
for i in range(5): b.append(circ(cx-12+i*6,cy-4+(i%2)*8,6,'#d9534f'))
# gangrenosa
o,cx,cy=panel(5,'Gangrenosa','Extremidades con isquemia (pie diabético)',['Seca = coagulativa (negra, momificada).','Húmeda = + infección y licuefacción'])
b.append(o)
foot=f'M{cx-90},{cy+50} q-6,-60 30,-70 l80,0 q40,0 42,20 l0,40 q0,14 -14,14 Z'
b.append(f'<path d="{foot}" fill="#f1c6a6" stroke="#b07a55" stroke-width="2"/>')
for i,(dx,r) in enumerate(((30,13),(52,11),(70,10),(86,9),(99,8))):
    col='#2b2320' if i==0 else '#f1c6a6'
    b.append(circ(cx-60+dx+ (0 if i else -4),cy-34+i*3,r,col,'#b07a55',1.5))
b.append(f'<path d="M{cx-48},{cy-40} q8,10 -2,22" stroke="#6b3a2a" stroke-width="4" fill="none" stroke-dasharray="3,3"/>')
b.append(T(cx-80,cy-58,'dedo negro',11,'#2b2320','start',w='bold'))
svg('necrosis-tipos.svg',900,610,''.join(b))

# ───────── 5. Reclutamiento de leucocitos ─────────
b=[title(900,'Inflamación aguda: cómo sale el neutrófilo del vaso','Marginación → rodamiento → adhesión firme → diapédesis → quimiotaxis → fagocitosis')]
# vaso
b.append(f'<rect x="20" y="80" width="860" height="150" fill="#fde3e3"/>')
b.append(f'<line x1="20" y1="230" x2="880" y2="230" stroke="#c06080" stroke-width="10"/>')
b.append(f'<rect x="20" y="236" width="860" height="330" fill="#fff7ef" />')
b.append(T(40,104,'Luz del vaso (vénula poscapilar)',13,ROJO,'start',w='bold'))
b.append(arrow(640,104,820,104,ROJO,2,9)); b.append(T(730,96,'flujo',11,ROJO))
for x in range(60,870,46):
    b.append(ell(x,150+((x//46)%3)*18,14,6,'#d9534f'))
def neut(x,y,r=17):
    o=circ(x,y,r,'#eee8f6','#8a6cc0',1.5)
    o+=f'<path d="M{x-9},{y-1} q4,-9 9,0 q4,9 9,0" stroke="{NUC}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    return o
steps=[(110,'Marginación','va a la orilla por estasis'),(250,'Rodamiento','selectinas E y P'),(390,'Adhesión firme','integrinas ↔ ICAM-1 / VCAM-1'),(530,'Diapédesis','entre células (PECAM-1/CD31)')]
for i,(x,t,s) in enumerate(steps):
    y=206 if i else 196
    if i==3:
        b.append(ell(x,232,14,20,'#eee8f6','#8a6cc0',1.5)); b.append(neut(x,262,14))
    else:
        b.append(neut(x,y))
        if i==1: b.append(arrow(x-40,y,x-22,y,'#8a6cc0',2,7))
    b.append(T(x,300 if i<3 else 310,t,14,MOR,w='bold')); b.append(T(x,318 if i<3 else 328,s,11.5,GRIS))
# tejido
b.append(T(40,556,'Tejido (intersticio)',13,'#8a5a2a','start',w='bold'))
# gradiente quimiotaxis
for i in range(12):
    b.append(circ(640+i*18,420+math.sin(i)*30,3+i*.5,NAR,'none',0,f' opacity="{0.2+i*.06:.2f}"'))
b.append(neut(660,410)); b.append(arrow(682,410,740,420,MOR,2,8))
b.append(T(690,470,'Quimiotaxis',14,MOR,w='bold')); b.append(TL(680,488,['C5a, IL-8, LTB₄,','productos bacterianos'],11.5,GRIS))
# fagocitosis
b.append(neut(820,410,22))
for dx,dy in((14,-8),(10,8)): b.append(ell(820+dx,410+dy,5,3,'#2e7d4f'))
b.append(T(820,470,'Fagocitosis',14,MOR,w='bold')); b.append(TL(830,488,['opsoninas:','IgG, C3b'],11.5,GRIS))
b.append(tbox(40,380,520,110,['Mediadores vasculares: histamina (mastocitos, segundos) →','vasodilatación y ↑ permeabilidad → exudado y edema.','Defectos: LAD tipo 1 (falta CD18, integrina) → infecciones sin pus','y caída tardía del cordón umbilical.'],'#f7f7f2','#bbb',12.5))
svg('inflamacion-leucocitos.svg',900,575,''.join(b))

# ───────── 6. Signos cardinales ─────────
b=[title(900,'Signos cardinales de la inflamación','Cada signo tiene un mecanismo y mediadores')]
cards=[('Rubor','enrojecimiento',['Vasodilatación','arteriolar'],'histamina, PGI₂, NO',ROJO),
       ('Calor','temperatura local',['Más flujo de','sangre caliente'],'fiebre: IL-1, TNF, PGE₂',NAR),
       ('Tumor','hinchazón',['↑ permeabilidad →','exudado y edema'],'histamina, bradicinina',AZUL),
       ('Dolor','dolor',['Sensibiliza las','terminaciones nerviosas'],'PGE₂, bradicinina',MOR),
       ('Pérdida de función','functio laesa',['Dolor + edema +','daño del tejido'],'(la agregó Virchow)',GRIS)]
for i,(t,s,m,med,c) in enumerate(cards):
    x=20+i*176; y=70
    b.append(box(x,y,166,250,'#fcfcfa',c,12,2.5))
    b.append(T(x+83,y+34,t,17 if len(t)<12 else 14,c,w='bold')); b.append(T(x+83,y+54,s,12,GRIS))
    cx,cy=x+83,y+118
    if i==0: b.append(circ(cx,cy,36,'#f5a3a3')+circ(cx,cy,20,'#e85d5d'))
    if i==1:
        b.append(f'<rect x="{cx-7}" y="{cy-40}" width="14" height="62" rx="7" fill="#fff" stroke="#555" stroke-width="2"/>'+circ(cx,cy+30,14,NAR,'#555',2)+f'<rect x="{cx-3}" y="{cy-20}" width="6" height="45" fill="{NAR}"/>')
    if i==2: b.append(blob(cx,cy,40,'#cfe0f5',AZUL,2,.08,3,5)+T(cx,cy+5,'edema',12,AZUL))
    if i==3: b.append(f'<path d="M{cx-34},{cy+8} l14,-24 l10,18 l12,-30 l10,26 l12,-12" stroke="{MOR}" stroke-width="4" fill="none" stroke-linejoin="round"/>')
    if i==4: b.append(circ(cx,cy,34,'#eee','#999',2)+f'<line x1="{cx-24}" y1="{cy+24}" x2="{cx+24}" y2="{cy-24}" stroke="{ROJO}" stroke-width="5"/>')
    b.append(TL(x+83,y+186,m,12,'#222'))
    b.append(TL(x+83,y+222,[med],11.5,c,w='bold'))
b.append(T(450,350,'Celso describió los cuatro primeros. Las citocinas sistémicas (IL-1, IL-6, TNF) dan fiebre, leucocitosis y PCR elevada.',12.5,GRIS))
svg('signos-cardinales.svg',900,370,''.join(b))

# ───────── 7. Granuloma ─────────
b=[title(900,'Granuloma','Inflamación crónica que encierra lo que no se puede eliminar')]
cx,cy=290,300
rnd=random.Random(11)
for i in range(120):
    a=rnd.random()*6.28; r=150+rnd.random()*40
    b.append(circ(cx+r*math.cos(a),cy+r*.85*math.sin(a),5.5,'#4a2a80'))
for i in range(60):
    a=i/60*6.28; r=192+rnd.random()*10
    b.append(ell(cx+r*math.cos(a),cy+r*.85*math.sin(a),12,3,'#d9a1b4','none',0,math.degrees(a)+90))
for ring in (105,128):
    n=int(ring/6)
    for i in range(n):
        a=i/n*6.28+ring
        b.append(ell(cx+ring*math.cos(a),cy+ring*.85*math.sin(a),13,6.5,'#f3c9d6','#c06080',1,math.degrees(a)+90))
        b.append(ell(cx+ring*math.cos(a),cy+ring*.85*math.sin(a),5,2.5,NUC2,'none',0,math.degrees(a)+90))
# célula gigante de Langhans
gx,gy=cx+70,cy-70
b.append(blob(gx,gy,34,'#f3c9d6','#c06080',1.5,.08,4,3))
for i in range(11):
    a=math.pi*.15+i/10*math.pi*.9
    b.append(ell(gx+26*math.cos(a),gy+26*math.sin(a),4,3,NUC))
b.append(blob(cx,cy,80,'#f4ecd2','#c8b67a',1.5,.1,6,12))
b.append(T(cx,cy+5,'Necrosis caseosa',14,'#7a6a30',w='bold'))
def P(r,ang): return (cx+r*math.cos(math.radians(ang)), cy+r*.85*math.sin(math.radians(ang)))
labs=[(P(172,-35),'Corona de linfocitos T CD4⁺',['Th1: liberan IFN-γ']),
      ((gx,gy),'Célula gigante de Langhans',['Macrófagos fusionados,','núcleos en herradura']),
      ((cx+30,cy+10),'Necrosis caseosa (centro)',['Típica de la tuberculosis']),
      (P(116,25),'Macrófagos epitelioides',['Activados por IFN-γ;','se juntan como un epitelio']),
      (P(197,45),'Fibroblastos y fibrosis',['Encapsulan la lesión'])]
for i,((x,y),t,sub) in enumerate(labs):
    ty=100+i*92
    b.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="598" y2="{ty-5}" stroke="#333" stroke-width="1.2"/>')
    b.append(circ(x,y,4,'#222'))
    b.append(T(606,ty,t,14,'#222','start',w='bold'))
    b.append(TL(606,ty+19,sub,12,GRIS,'start'))
b.append(TL(450,560,['Granuloma sin caseum: sarcoidosis, cuerpo extraño, Crohn, lepra tuberculoide, arteritis de células gigantes.'],12.5,'#222'))
svg('granuloma.svg',900,580,''.join(b))

# ───────── 8. Aguda vs crónica ─────────
b=[title(900,'Inflamación aguda vs crónica')]
rows=[('','Aguda','Crónica'),('Inicio y duración','Minutos a días','Semanas a años'),('Célula principal','Neutrófilo (primeras 6–24 h)','Macrófago, linfocito, célula plasmática'),
      ('Lo que domina','Exudado, edema, vasodilatación','Destrucción + reparación a la vez'),('Resultado','Resolución, absceso o cronificación','Fibrosis, angiogénesis, granuloma'),
      ('Ejemplos','Apendicitis, neumonía bacteriana','TB, artritis reumatoide, hepatitis C crónica'),('Laboratorio','Leucocitosis con neutrofilia, PCR alta','Anemia de enfermedad crónica, VSG alta')]
cw=[200,330,330]; x0=20; y=60
for r,row in enumerate(rows):
    x=x0; h=44
    for c,txt in enumerate(row):
        fill=VERDE if r==0 and c else ('#eef5f1' if c==0 else ('#fff' if r%2 else '#fafafa'))
        b.append(f'<rect x="{x}" y="{y}" width="{cw[c]}" height="{h}" fill="{fill}" stroke="#ccc"/>')
        col='#fff' if r==0 else ('#00573c' if c==0 else '#222')
        b.append(T(x+(12 if c==0 else cw[c]/2),y+27,txt,14 if r==0 else 13,col,'start' if c==0 else 'middle','bold' if (r==0 or c==0) else 'normal'))
        x+=cw[c]
    y+=h
svg('aguda-cronica.svg',900,y+20,''.join(b))

# ───────── 9. Benigno vs maligno ─────────
b=[title(900,'Neoplasia benigna vs maligna','La metástasis es lo único que define con seguridad a un tumor maligno')]
# benigno
cx,cy=220,240
b.append(f'<rect x="40" y="80" width="360" height="300" rx="14" fill="#fff8f6" stroke="#ddd"/>')
b.append(ell(cx,cy,110,82,'none','#7a5a2a',5))
b.append(ell(cx,cy,104,76,'#f6cfdc','none'))
for i in range(5):
    for j in range(4):
        x=cx-80+i*40; y=cy-48+j*32
        if ((x-cx)/100)**2+((y-cy)/70)**2<1: b.append(ell(x,y,16,12,'#f3c9d6','#c06080',1)+circ(x,y,5,NUC2))
b.append(T(cx,110,'Benigna',19,VERDE,w='bold'))
b.append(T(cx,345,'cápsula',12,'#7a5a2a'))
# maligna
cx,cy=670,255
b.append(f'<rect x="490" y="80" width="370" height="300" rx="14" fill="#fff8f6" stroke="#ddd"/>')
b.append(blob(cx,cy,74,'#f2b8c9','#b3261e',2,.25,7,40))
rnd=random.Random(8)
for i in range(30):
    a=rnd.random()*6.28; r=rnd.random()*55
    rr=6+rnd.random()*7
    b.append(blob(cx+r*math.cos(a),cy+r*math.sin(a),rr+4,'#f3c9d6','#c06080',1,.2,4,i)+blob(cx+r*math.cos(a),cy+r*math.sin(a),rr*.7,'#3b1f66','none',0,.25,3,i+9))
for a in (0.3,1.4,2.6,3.6,5.0):
    x1=cx+72*math.cos(a); y1=cy+72*math.sin(a); x2=cx+112*math.cos(a); y2=cy+min(112*math.sin(a),112)
    b.append(f'<path d="M{x1:.0f},{y1:.0f} Q{(x1+x2)/2+12:.0f},{(y1+y2)/2-10:.0f} {x2:.0f},{y2:.0f}" stroke="#b3261e" stroke-width="7" fill="none" stroke-linecap="round"/>')
b.append(f'<path d="M790,320 q30,10 50,40" stroke="{AZUL}" stroke-width="10" fill="none"/>')
b.append(circ(828,345,7,'#3b1f66')+T(850,372,'vaso',11,AZUL))
b.append(T(cx,110,'Maligna',19,ROJO,w='bold'))
rows=[('Diferenciación','Se parece al tejido de origen','Anaplasia y atipia (núcleos grandes)'),('Crecimiento','Lento, expansivo, encapsulado','Rápido, infiltra los tejidos vecinos'),
      ('Mitosis','Pocas, normales','Muchas y atípicas'),('Metástasis','Nunca','Sí: linfática (carcinomas), hematógena (sarcomas)'),('Nombre','Adenoma, lipoma, leiomioma','Carcinoma (epitelio), sarcoma (mesénquima)')]
y=400
for k,(a,bb,c) in enumerate(rows):
    fill='#fafafa' if k%2 else '#fff'
    b.append(f'<rect x="40" y="{y}" width="820" height="36" fill="{fill}" stroke="#e2e2e2"/>')
    b.append(T(52,y+23,a,13,'#222','start','bold')); b.append(T(330,y+23,bb,12.5,VERDE)); b.append(T(680,y+23,c,12.5,ROJO))
    y+=36
svg('benigno-maligno.svg',900,y+20,''.join(b))

# ───────── 10. Del epitelio normal al carcinoma ─────────
b=[title(900,'Del epitelio normal al carcinoma invasor','Ejemplo clásico: cuello uterino (NIC) por VPH; la clave es la membrana basal')]
st=[('Normal','maduración ordenada',0),('NIC 1','displasia leve (⅓ inferior)',1),('NIC 2','displasia moderada (⅔)',2),('NIC 3 / in situ','todo el espesor, membrana basal íntegra',3),('Carcinoma invasor','rompe la membrana basal',4)]
PW=168
for k,(t,s,g) in enumerate(st):
    px=20+k*(PW+5); top=112; base=350
    b.append(f'<rect x="{px}" y="{top}" width="{PW}" height="{base-top}" fill="#fcfcfa" stroke="#ddd"/>')
    b.append(f'<rect x="{px}" y="{base+2}" width="{PW}" height="140" fill="#fbeee6"/>')
    rnd=random.Random(k+3)
    for row in range(8):
        frac=row/7  # 0 abajo, 1 arriba
        y=base-14-row*28
        atip = frac < g/3.0 if g<4 else True
        n=6
        for i in range(n):
            x=px+16+i*27+(13 if row%2 else 0)
            if x>px+PW-14: continue
            if atip:
                rr=9+rnd.random()*4
                b.append(blob(x,y,rr+3,'#f3c9d6','#c06080',1,.18,4,row*10+i)+blob(x,y,rr*.75,'#3b1f66','none',0,.2,3,row*7+i))
            else:
                flat=frac
                b.append(ell(x,y,12+flat*3,11-flat*7,'#f6cfdc','#c06080',1)+ell(x,y,4,max(1.5,4-flat*2.5),NUC2))
    # membrana basal
    if g<4:
        b.append(f'<line x1="{px}" y1="{base}" x2="{px+PW}" y2="{base}" stroke="{VERDE}" stroke-width="4"/>')
    else:
        b.append(f'<line x1="{px}" y1="{base}" x2="{px+50}" y2="{base}" stroke="{VERDE}" stroke-width="4"/><line x1="{px+110}" y1="{base}" x2="{px+PW}" y2="{base}" stroke="{VERDE}" stroke-width="4"/>')
        for i,(dx,dy) in enumerate(((70,30),(90,58),(60,80),(110,95),(80,120))):
            b.append(blob(px+dx,base+dy,12,'#f3c9d6','#c06080',1,.2,4,i+70)+blob(px+dx,base+dy,8,'#3b1f66','none',0,.2,3,i+80))
    b.append(T(px+PW/2,top-18,t,14.5,ROJO if g>=3 else (NAR if g else VERDE),w='bold'))
    b.append(T(px+PW/2,base+156,s,10.5,GRIS))
    if k<4: b.append(arrow(px+PW-14,90,px+PW+18,90,'#999',2,7))
b.append(T(24,372,'membrana basal',11,VERDE,'start',w='bold')); b.append(T(24,475,'estroma',11,'#8a5a2a','start'))
b.append(T(450,540,'Mientras la membrana basal está íntegra no hay metástasis: por eso el tamizaje (Papanicolaou, VPH) detecta NIC a tiempo.',12.5,'#222'))
svg('carcinogenesis.svg',900,560,''.join(b))
print('listo')
