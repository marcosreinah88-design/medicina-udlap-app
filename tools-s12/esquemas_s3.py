# Esquemas propios (SVG, en español) para las guías de Microbiología, Fisiología Clínica,
# Simulación III (3º) y Bioquímica (1º). Dibujados desde cero: no copian figuras de libros.
# Uso: python3 tools-s12/esquemas_s3.py        (escribe en tools-s12/img/<guía>/)
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
F = 'font-family="Helvetica,Arial,sans-serif"'
ROJO='#b3261e'; VERDE='#00573c'; NAR='#f26b21'; AZUL='#2b6cb0'; MOR='#7b3fa0'; GRIS='#555'; AMA='#e0a800'
def svg(gid, name, w, h, body):
    d = os.path.join(HERE, 'img', gid); os.makedirs(d, exist_ok=True)
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
def poly(pts): return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)
def curve(fn, x0, x1, X, Y, n=200):
    # fn: x(dominio)->y(dominio); X,Y: mapeos a pixeles
    return poly([(X(x0+(x1-x0)*i/n), Y(fn(x0+(x1-x0)*i/n))) for i in range(n+1)])
def axes(x0,y0,x1,y1,xl,yl):
    return (arrow(x0,y0,x1,y0,'#222',2,9)+arrow(x0,y0,x0,y1,'#222',2,9)
            +T((x0+x1)/2,y0+34,xl,14,'#222')+f'<text x="{x0-38}" y="{(y0+y1)/2}" font-size="14" fill="#222" text-anchor="middle" transform="rotate(-90 {x0-38} {(y0+y1)/2})">{yl}</text>')

# ───────────────────────── MICROBIOLOGÍA ─────────────────────────
M='microbiologia'
# Pared grampositiva vs gramnegativa
b=[]
def capa(x,y,w,h,fill,label,lc='#222'):
    return box(x,y,w,h,fill,'none',4,0)+T(x+w+12,y+h/2+5,label,14,lc,'start')
for X0,tit,col in ((30,'Grampositiva','#6b3fa0'),(470,'Gramnegativa','#c2185b')):
    b.append(T(X0+150,32,tit,19,col,w='bold'))
b.append(T(180,56,'retiene el cristal violeta → morada',13,GRIS)); b.append(T(620,56,'se decolora y toma safranina → rosa',13,GRIS))
# grampositiva
x=30; w=170
b.append(capa(x,80,w,22,'#e7e1f1','Ácidos teicoicos'))
for i in range(9): b.append(f'<line x1="{x+12+i*18}" y1="102" x2="{x+12+i*18}" y2="78" stroke="#7b3fa0" stroke-width="3"/>')
b.append(capa(x,102,w,110,'#c9b3e6','Peptidoglucano grueso'))
for j in range(6): b.append(f'<line x1="{x}" y1="{112+j*18}" x2="{x+w}" y2="{112+j*18}" stroke="#9a7cc9" stroke-width="2"/>')
b.append(T(x+w+12,180,'(20–80 nm, muchas capas)',12,GRIS,'start'))
b.append(capa(x,216,w,26,'#ffe08a','Membrana plasmática'))
b.append(capa(x,246,w,40,'#f4f4f4','Citoplasma'))
# gramnegativa
x=470
b.append(capa(x,80,w,26,'#ffd0dc','Membrana externa con LPS'))
for i in range(9): b.append(f'<path d="M{x+12+i*18},80 l-4,-12 m4,12 l4,-12" stroke="#c2185b" stroke-width="2" fill="none"/>')
b.append(box(x,108,w,46,'#fdf0f4','none',4,0)); b.append(T(x+w+12,121,'Periplasma',14,'#222','start'))
b.append(box(x,124,w,14,'#f2a7bd','none',4,0)); b.append(T(x+w+12,144,'Peptidoglucano delgado',14,'#222','start'))
b.append(capa(x,158,w,26,'#ffe08a','Membrana plasmática'))
b.append(capa(x,188,w,40,'#f4f4f4','Citoplasma'))
b.append(T(x+85,262,'LPS = lípido A (endotoxina) + núcleo + antígeno O',12,'#c2185b'))
svg(M,'pared-gram.svg',900,300,''.join(b))

# Clasificación de Baltimore
b=[T(450,30,'Clasificación de Baltimore: cómo llega cada virus a ARNm',18,VERDE,w='bold')]
gr=[('I','ADN dc','Herpes, adeno, papiloma, viruela',AZUL),('II','ADN mc','Parvovirus B19',AZUL),
    ('III','ARN dc','Rotavirus',NAR),('IV','ARN mc (+)','Polio, hepatitis A y C, dengue, coronavirus',NAR),
    ('V','ARN mc (−)','Influenza, sarampión, rabia, ébola',NAR),('VI','ARN mc (+) con TI','VIH (retrovirus)',MOR),('VII','ADN dc con TI','Hepatitis B',MOR)]
for i,(n,t,e,c) in enumerate(gr):
    y=50+i*52
    b.append(tbox(20,y,90,42,['Grupo '+n],c,c,15,'#fff','bold'))
    b.append(tbox(122,y,180,42,[t],'#fff',c,15,c,'bold'))
    b.append(arrow(306,y+21,560,y+21,c,2.2,9))
    b.append(T(433,y+15,e,12,'#333'))
b.append(tbox(570,50,170,354,['ARNm','','→ proteínas','virales'],'#e8f5ee',VERDE,17,VERDE,'bold'))
b.append(T(450,428,'dc = doble cadena · mc = monocatenario · TI = transcriptasa inversa',13,GRIS))
svg(M,'baltimore.svg',900,440,''.join(b))

# Morfología de colonias
b=[T(450,28,'Morfología de las colonias',18,VERDE,w='bold')]
def fila(y,tit,items):
    o=[T(20,y+5,tit,15,'#222','start','bold')]
    for i,(nom,dib) in enumerate(items):
        cx=170+i*150
        o.append(dib(cx,y)); o.append(T(cx,y+52,nom,13,GRIS))
    return ''.join(o)
C='#f3c46b'; S='#b07a12'
def circ(cx,cy): return f'<circle cx="{cx}" cy="{cy}" r="28" fill="{C}" stroke="{S}" stroke-width="2"/>'
def irreg(cx,cy): return f'<path d="{poly([(cx+28*math.cos(t/20*6.283)*(1+.25*math.sin(3*t/20*6.283)),cy+28*math.sin(t/20*6.283)*(1+.2*math.cos(2*t/20*6.283))) for t in range(21)])}Z" fill="{C}" stroke="{S}" stroke-width="2"/>'
def rizo(cx,cy): return f'<path d="{poly([(cx+(18+12*abs(math.sin(5*t/60*6.283)))*math.cos(t/60*6.283),cy+(18+12*abs(math.sin(5*t/60*6.283)))*math.sin(t/60*6.283)) for t in range(61)])}Z" fill="{C}" stroke="{S}" stroke-width="2"/>'
def filam(cx,cy): return '<g stroke="'+S+'" stroke-width="2">'+''.join(f'<line x1="{cx}" y1="{cy}" x2="{cx+30*math.cos(a/9*6.283):.1f}" y2="{cy+30*math.sin(a/9*6.283):.1f}"/>' for a in range(9))+f'</g><circle cx="{cx}" cy="{cy}" r="10" fill="{C}" stroke="{S}" stroke-width="2"/>'
def borde(kind):
    def f(cx,cy):
        if kind=='entero': pts=[(cx+30*math.cos(t/40*6.283),cy+30*math.sin(t/40*6.283)) for t in range(41)]
        elif kind=='ondulado': pts=[(cx+(28+3*math.sin(8*t/80*6.283))*math.cos(t/80*6.283),cy+(28+3*math.sin(8*t/80*6.283))*math.sin(t/80*6.283)) for t in range(81)]
        elif kind=='lobulado': pts=[(cx+(25+6*abs(math.sin(4*t/80*6.283)))*math.cos(t/80*6.283),cy+(25+6*abs(math.sin(4*t/80*6.283)))*math.sin(t/80*6.283)) for t in range(81)]
        else: pts=[(cx+(27+5*(t%2))*math.cos(t/48*6.283),cy+(27+5*(t%2))*math.sin(t/48*6.283)) for t in range(49)]
        return f'<path d="{poly(pts)}Z" fill="{C}" stroke="{S}" stroke-width="2"/>'
    return f
def elev(kind):
    def f(cx,cy):
        base=cy+22; o=f'<line x1="{cx-50}" y1="{base}" x2="{cx+50}" y2="{base}" stroke="#999" stroke-width="2"/>'
        if kind=='plana': p=f'M{cx-38},{base} L{cx-36},{base-6} L{cx+36},{base-6} L{cx+38},{base}Z'
        elif kind=='elevada': p=f'M{cx-38},{base} L{cx-36},{base-18} L{cx+36},{base-18} L{cx+38},{base}Z'
        elif kind=='convexa': p=f'M{cx-38},{base} Q{cx},{base-50} {cx+38},{base}Z'
        else: p=f'M{cx-38},{base} Q{cx-30},{base-14} {cx-12},{base-16} Q{cx},{base-40} {cx+12},{base-16} Q{cx+30},{base-14} {cx+38},{base}Z'
        return o+f'<path d="{p}" fill="{C}" stroke="{S}" stroke-width="2"/>'
    return f
b.append(fila(80,'Forma',[('Circular',circ),('Irregular',irreg),('Rizoide',rizo),('Filamentosa',filam)]))
b.append(fila(200,'Borde',[('Entero',borde('entero')),('Ondulado',borde('ondulado')),('Lobulado',borde('lobulado')),('Dentado',borde('dentado'))]))
b.append(fila(320,'Elevación',[('Plana',elev('plana')),('Elevada',elev('elevada')),('Convexa',elev('convexa')),('Umbonada',elev('umbonada'))]))
svg(M,'colonias.svg',800,390,''.join(b))

# Incidencia vs prevalencia (la tina)
b=[T(400,28,'Incidencia y prevalencia: la tina',18,VERDE,w='bold')]
b.append(f'<path d="M250,120 L270,330 Q400,350 530,330 L550,120" fill="none" stroke="#444" stroke-width="4"/>')
b.append(f'<path d="M262,210 L270,330 Q400,350 530,330 L538,210Z" fill="#9fd3f2"/>')
b.append(T(400,275,'PREVALENCIA',18,'#0d4f80',w='bold')); b.append(T(400,297,'(todos los casos existentes)',13,'#0d4f80'))
b.append(f'<path d="M150,92 H330 V104" fill="none" stroke="#888" stroke-width="10"/>')
for i in range(5): b.append(f'<circle cx="{330}" cy="{115+i*18}" r="4" fill="#2b8bd6"/>')
b.append(T(130,52,'INCIDENCIA',16,AZUL,'start','bold')); b.append(T(130,72,'casos nuevos en un periodo',12,AZUL,'start'))
b.append(arrow(530,330,660,370,ROJO,3)); b.append(T(670,376,'Muerte',14,ROJO,'start','bold'))
b.append(arrow(400,348,400,405,VERDE,3)); b.append(T(410,400,'Curación',14,VERDE,'start','bold'))
b.append(T(400,440,'Prevalencia ≈ incidencia × duración de la enfermedad',14,'#333',w='bold'))
svg(M,'incidencia-prevalencia.svg',800,460,''.join(b))

# ───────────────────────── FISIOLOGÍA CLÍNICA ─────────────────────────
FC='fisiologia-clinica'
# Potencial de acción: marcapasos vs ventricular
b=[T(450,26,'Potencial de acción: nodo sinusal vs miocito ventricular',17,VERDE,w='bold')]
def apx(x0,y0,pts): return poly([(x0+x,y0-y) for x,y in pts])
# panel izquierdo (marcapasos)
X0,Y0=60,300
b.append(f'<line x1="{X0}" y1="{Y0-60}" x2="{X0+360}" y2="{Y0-60}" stroke="#ccc" stroke-dasharray="4 4"/>'); b.append(T(X0-6,Y0-56,'−60',11,GRIS,'end'))
b.append(f'<line x1="{X0}" y1="{Y0-160}" x2="{X0+360}" y2="{Y0-160}" stroke="#ccc" stroke-dasharray="4 4"/>'); b.append(T(X0-6,Y0-156,'0 mV',11,GRIS,'end'))
pts=[(0,60),(70,100),(80,108),(100,190),(120,178),(160,110),(180,62),(250,100),(262,108),(282,190),(302,178),(342,110),(355,62)]
b.append(f'<path d="{apx(X0,Y0,pts)}" fill="none" stroke="{ROJO}" stroke-width="3" stroke-linejoin="round"/>')
b.append(T(X0+40,Y0-38,'Fase 4',13,AZUL,w='bold')); b.append(T(X0+40,Y0-23,'If (Na⁺) → T-Ca²⁺',11,AZUL))
b.append(T(X0+86,Y0-170,'Fase 0',13,NAR,'end','bold')); b.append(T(X0+86,Y0-155,'L-Ca²⁺',11,NAR,'end'))
b.append(T(X0+150,Y0-175,'Fase 3',13,MOR,'start','bold')); b.append(T(X0+150,Y0-160,'salida de K⁺',11,MOR,'start'))
b.append(T(X0+180,Y0+30,'Nodo sinusal: sin reposo estable, despolarización espontánea',12,GRIS))
# panel derecho (ventricular)
X0=520
b.append(f'<line x1="{X0}" y1="{Y0-30}" x2="{X0+340}" y2="{Y0-30}" stroke="#ccc" stroke-dasharray="4 4"/>'); b.append(T(X0-6,Y0-26,'−90',11,GRIS,'end'))
b.append(f'<line x1="{X0}" y1="{Y0-160}" x2="{X0+340}" y2="{Y0-160}" stroke="#ccc" stroke-dasharray="4 4"/>'); b.append(T(X0-6,Y0-156,'0 mV',11,GRIS,'end'))
pts=[(0,30),(40,30),(46,190),(60,170),(80,160),(190,150),(230,110),(255,40),(270,30),(340,30)]
b.append(f'<path d="{apx(X0,Y0,pts)}" fill="none" stroke="{ROJO}" stroke-width="3" stroke-linejoin="round"/>')
for x,y,f,s,c in ((10,48,'Fase 4','reposo (IK1)',AZUL),(-8,140,'Fase 0','Na⁺ rápido',NAR),(62,222,'Fase 1','Ito (K⁺)',GRIS),
                  (140,172,'Fase 2','meseta: Ca²⁺ entra, K⁺ sale',VERDE),(285,105,'Fase 3','repolarización (K⁺)',MOR)):
    an='end' if x<0 else 'start'; x=abs(x) if x>=0 else 36
    b.append(T(X0+x,Y0-y,f,13,c,an,'bold')); b.append(T(X0+x,Y0-y+15,s,11,c,an))
b.append(T(X0+170,Y0+30,'Miocito ventricular: reposo estable y meseta larga',12,GRIS))
svg(FC,'pa-marcapasos.svg',900,350,''.join(b))

# Reentrada
b=[T(400,28,'Reentrada: el circuito que se perpetúa',18,VERDE,w='bold')]
b.append(arrow(400,50,400,92,'#333',3))
b.append(f'<path d="M400,95 L290,170 L290,300 L400,375 L510,300 L510,170Z" fill="none" stroke="#c9a8e6" stroke-width="34" stroke-linejoin="round"/>')
b.append(f'<path d="M400,95 L290,170 L290,300 L400,375" fill="none" stroke="{AZUL}" stroke-width="5" stroke-linejoin="round"/>')
b.append(arrow(290,300,400,375,AZUL,5,14))
b.append(f'<path d="M400,375 L510,300 L510,170" fill="none" stroke="{ROJO}" stroke-width="5" stroke-linejoin="round"/>')
b.append(arrow(510,200,510,165,ROJO,5,14))
b.append(f'<rect x="490" y="215" width="40" height="22" fill="#222"/>')
b.append(T(545,222,'Bloqueo unidireccional',14,'#222','start','bold')); b.append(T(545,240,'(el impulso no baja por aquí,',12,GRIS,'start')); b.append(T(545,256,'pero sí puede subir)',12,GRIS,'start'))
b.append(T(240,240,'Vía A',15,AZUL,'end','bold')); b.append(T(240,258,'conducción normal',12,AZUL,'end'))
b.append(T(400,410,'Conducción lenta + tejido ya repolarizado al regresar el impulso → reentra y da una taquicardia',13,'#333'))
svg(FC,'reentrada.svg',800,430,''.join(b))

# SRAA
b=[T(450,28,'Sistema renina-angiotensina-aldosterona',18,VERDE,w='bold')]
b.append(tbox(20,60,200,60,['↓ Presión de perfusión renal','↓ Na⁺ en mácula densa','Simpático (β1)'],'#fdecea',ROJO,12))
b.append(arrow(220,90,262,90)); b.append(tbox(265,65,160,50,['Riñón (aparato','yuxtaglomerular): RENINA'],'#fff',NAR,12,'#222','bold'))
b.append(tbox(20,160,200,46,['Angiotensinógeno','(hígado)'],'#fff',GRIS,13))
b.append(arrow(220,183,330,183)); b.append(T(275,175,'renina',12,NAR,w='bold'))
b.append(arrow(345,115,345,165,NAR,2,8,'5 4'))
b.append(tbox(335,160,160,46,['Angiotensina I'],'#fff',GRIS,14))
b.append(arrow(495,183,595,183)); b.append(T(545,175,'ECA (pulmón)',12,AZUL,w='bold'))
b.append(tbox(600,160,180,46,['Angiotensina II'],'#e8f0fb',AZUL,15,AZUL,'bold'))
ef=[('Vasoconstricción arteriolar','↑ resistencia periférica'),('Corteza suprarrenal: ALDOSTERONA','reabsorbe Na⁺ y agua, excreta K⁺'),
    ('Hipófisis: ADH y sed','↑ agua corporal'),('Túbulo proximal','↑ reabsorción de Na⁺')]
for i,(a,c2) in enumerate(ef):
    y=250+i*52
    b.append(arrow(690,206,690 if i==0 else 690,y,AZUL,2,8) if i==0 else f'<path d="M690,206 V{y+20} H560" fill="none" stroke="{AZUL}" stroke-width="2"/>')
    b.append(tbox(300,y,260,42,[a,c2],'#fff',AZUL,12))
b.append(tbox(620,300,200,90,['↑ Volemia','↑ Presión arterial'],'#e8f5ee',VERDE,15,VERDE,'bold'))
b.append(T(450,470,'IECA bloquean la ECA · ARA II bloquean el receptor AT1 · espironolactona bloquea la aldosterona',13,GRIS))
svg(FC,'sraa.svg',900,490,''.join(b))

# Nefrítico vs nefrótico
b=[T(450,28,'Glomérulo: síndrome nefrítico vs nefrótico',18,VERDE,w='bold')]
for X0,tit,col,items,dibu in ((30,'Nefrítico',ROJO,['Inflamación: el capilar','se rompe','• Hematuria (cilindros','  eritrocitarios)','• Proteinuria < 3.5 g/día','• Oliguria, edema, HTA','Ej.: posestreptocócica,','nefropatía por IgA'],'n'),
                              (470,'Nefrótico',AZUL,['Daño a podocitos: la','barrera deja pasar proteína','• Proteinuria > 3.5 g/día','• Hipoalbuminemia, edema','• Hiperlipidemia, lipiduria','Ej.: cambios mínimos,','membranosa, GEFS'],'s')):
    b.append(box(X0,50,400,330,'#fff',col,14,2.5)); b.append(T(X0+200,80,tit,18,col,w='bold'))
    cx,cy=X0+110,190
    b.append(f'<circle cx="{cx}" cy="{cy}" r="62" fill="#fbe3e3" stroke="#d26" stroke-width="3"/>')
    b.append(f'<path d="M{cx-62},{cy+40} q-40,0 -70,30" stroke="#999" stroke-width="10" fill="none"/>')
    if dibu=='n':
        for i in range(6): b.append(f'<circle cx="{cx-20+i*9}" cy="{cy+80+(i%2)*8}" r="6" fill="{ROJO}"/>')
        b.append(T(cx,cy+118,'eritrocitos',12,ROJO))
        for i in range(5): b.append(f'<circle cx="{cx-30+i*15}" cy="{cy-10+((i*7)%15)}" r="5" fill="#f4b400"/>')
        b.append(T(cx,cy-30,'leucocitos',11,'#a07000'))
    else:
        for i in range(12): b.append(f'<circle cx="{cx-35+(i%6)*14}" cy="{cy+78+(i//6)*12}" r="4.5" fill="{AZUL}"/>')
        b.append(T(cx,cy+118,'albúmina',12,AZUL))
    b.append(TL(X0+190,125,items,13,'#222','start',lh=19))
svg(FC,'nefritico-nefrotico.svg',900,400,''.join(b))

# Tipos de choque
b=[T(450,28,'Tipos de choque y su perfil hemodinámico',18,VERDE,w='bold')]
cols=['Tipo','Causa típica','Gasto cardiaco','Resist. vascular','PVC / precarga']
xs=[20,170,430,580,730]; ws=[150,260,150,150,150]
for x,w,c in zip(xs,ws,cols): b.append(tbox(x,50,w-6,40,[c],VERDE,VERDE,14,'#fff','bold'))
rows=[('Hipovolémico','Hemorragia, vómito, quemaduras','↓','↑','↓','#fdecea'),('Cardiogénico','Infarto, arritmia, valvulopatía','↓','↑','↑','#fff4e0'),
      ('Distributivo','Sepsis, anafilaxia, neurogénico','↑ / normal','↓','↓ / normal','#e8f0fb'),('Obstructivo','TEP, taponamiento, neumotórax a tensión','↓','↑','↑','#f1e8f8')]
for i,(t,c,gc,rv,pvc,fill) in enumerate(rows):
    y=98+i*60
    for x,w,v in zip(xs,ws,[t,c,gc,rv,pvc]):
        col=ROJO if v.startswith('↓') else (AZUL if v.startswith('↑') else '#222')
        b.append(tbox(x,y,w-6,52,[v] if len(v)<28 else [v[:v.rfind(',')+1],v[v.rfind(',')+2:]],fill,'#ddd',(22 if len(v)==1 else 16) if x>=430 else 13,col if x>=430 else '#222','bold' if x!=170 else 'normal'))
svg(FC,'choque.svg',900,350,''.join(b))

# Frank-Starling
b=[T(400,26,'Curva de Frank-Starling',18,VERDE,w='bold')]
X=lambda v:90+v*6.2; Y=lambda v:360-v*2.9
b.append(axes(90,360,740,60,'Precarga (volumen telediastólico)','Volumen latido'))
b.append(f'<path d="{curve(lambda v:95*(1-math.exp(-v/28)),0,100,X,Y)}" fill="none" stroke="{VERDE}" stroke-width="4"/>')
b.append(f'<path d="{curve(lambda v:60*(1-math.exp(-v/30)),0,100,X,Y)}" fill="none" stroke="{NAR}" stroke-width="4"/>')
b.append(f'<path d="{curve(lambda v:35*(1-math.exp(-v/35)),0,100,X,Y)}" fill="none" stroke="{ROJO}" stroke-width="4"/>')
b.append(T(X(100)-4,Y(95)-10,'Normal / inotrópico (+)',14,VERDE,'end','bold'))
b.append(T(X(100)-4,Y(60)-10,'Insuficiencia cardiaca',14,NAR,'end','bold'))
b.append(T(X(100)-4,Y(35)-10,'IC grave',14,ROJO,'end','bold'))
b.append(T(X(50),Y(8),'Con IC, subir la precarga casi no sube el gasto: solo congestiona',13,GRIS))
svg(FC,'frank-starling.svg',800,410,''.join(b))

# Ganglios basales (vías directa e indirecta)
b=[T(450,26,'Ganglios basales: vía directa e indirecta (Parkinson)',17,VERDE,w='bold')]
N={'cx':(450,70,'Corteza'),'est':(450,165,'Estriado (caudado + putamen)'),'snc':(770,165,'Sustancia nigra compacta'),
   'gpe':(620,260,'Globo pálido externo'),'nst':(620,350,'Núcleo subtalámico'),'gpi':(280,350,'Globo pálido interno / SNr'),'tal':(450,440,'Tálamo')}
for k,(x,y,t) in N.items(): b.append(tbox(x-110,y-22,220,44,[t],'#fff' if k!='snc' else '#f3e6d0','#555' if k!='snc' else '#8a5a00',13,'#222','bold'))
EXC=VERDE; INH=ROJO
b.append(arrow(450,92,450,141,EXC,3))
b.append(arrow(660,165,562,165,'#8a5a00',3)); b.append(T(610,155,'dopamina',12,'#8a5a00',w='bold'))
b.append(arrow(400,187,300,326,INH,3)); b.append(T(320,250,'directa (D1)',12,INH,'end','bold'))
b.append(arrow(500,187,600,236,INH,3)); b.append(T(575,205,'indirecta (D2)',12,INH,'start','bold'))
b.append(arrow(620,282,620,326,INH,3))
b.append(arrow(510,350,392,350,EXC,3))
b.append(arrow(300,372,400,418,INH,3))
b.append(f'<path d="M560,440 H890 V70 H562" fill="none" stroke="{EXC}" stroke-width="3"/>'); b.append(arrow(600,70,562,70,EXC,3))
b.append(T(20,480,'Verde = excita · Rojo = inhibe. Sin dopamina (Parkinson): menos vía directa y más indirecta → el globo pálido interno frena de más al tálamo → bradicinesia.',12,'#333','start'))
svg(FC,'ganglios-basales.svg',900,500,''.join(b))

# ───────────────────────── SIMULACIÓN III ─────────────────────────
SI='simulacion-iii'
# Lesiones por presión: estadios
b=[T(450,26,'Lesiones por presión: estadios',18,VERDE,w='bold')]
def piel(x0,est):
    w=200; o=[]
    capas=[(60,22,'#f6d2b8'),(82,50,'#f2b5a0'),(132,48,'#fde7a7'),(180,40,'#d9776a'),(220,30,'#e9e3d6')]
    for y,h,c in capas: o.append(f'<rect x="{x0}" y="{y}" width="{w}" height="{h}" fill="{c}"/>')
    cx=x0+w/2
    if est==1: o.append(f'<ellipse cx="{cx}" cy="70" rx="45" ry="9" fill="#d0453a" opacity=".55"/>')
    if est==2: o.append(f'<path d="M{cx-40},60 Q{cx},100 {cx+40},60Z" fill="#e37a7a"/>')
    if est==3: o.append(f'<path d="M{cx-50},60 Q{cx-45},160 {cx},165 Q{cx+45},160 {cx+50},60Z" fill="#c74b4b"/><path d="M{cx-30},150 Q{cx},170 {cx+30},150" stroke="#f5d06f" stroke-width="6" fill="none"/>')
    if est==4: o.append(f'<path d="M{cx-55},60 Q{cx-50},240 {cx},245 Q{cx+50},240 {cx+55},60Z" fill="#a83232"/><rect x="{cx-20}" y="222" width="40" height="22" fill="#f4f1ea" stroke="#888"/>')
    return ''.join(o)
tx=[('Estadio 1','Eritema que no blanquea;','piel íntegra'),('Estadio 2','Pérdida parcial: epidermis','y/o dermis, flictena'),
    ('Estadio 3','Pérdida total de piel;','grasa visible, sin músculo'),('Estadio 4','Exposición de músculo,','tendón o hueso')]
for i in range(4):
    x0=20+i*220; b.append(piel(x0,i+1)); b.append(TL(x0+100,280,list(tx[i]),13,'#222')); b.append(f'<text x="{x0+100}" y="280" font-size="15" font-weight="bold" fill="{ROJO}" text-anchor="middle" dy="-1">{""}</text>')
for y,t in ((71,'Epidermis'),(107,'Dermis'),(156,'Grasa'),(200,'Músculo'),(235,'Hueso')): b.append(T(890,y+4,t,12,GRIS,'start'))
b.append(T(450,345,'También existen: no estadificable (lecho cubierto por esfacelo/escara) y lesión de tejidos profundos (morada).',12,GRIS))
svg(SI,'lpp-estadios.svg',960,360,''.join(b))

# Color del lecho
b=[T(450,26,'Color del lecho de la herida y qué hacer',18,VERDE,w='bold')]
for i,(c,t,d1,d2) in enumerate((('#2b2b2b','Negro','Necrosis seca (escara)','Desbridar'),('#e3c35a','Amarillo','Esfacelo / fibrina','Desbridar, limpiar'),
                                 ('#d9443a','Rojo','Granulación sana','Proteger, mantener húmedo'),('#f4a3b5','Rosa','Epitelización','Proteger'))):
    x=20+i*220
    b.append(f'<circle cx="{x+100}" cy="120" r="70" fill="{c}" stroke="#fff" stroke-width="4"/>')
    for k in range(10 if c!='#2b2b2b' else 0):
        a=k*0.628; b.append(f'<circle cx="{x+100+40*math.cos(a):.1f}" cy="{120+40*math.sin(a):.1f}" r="6" fill="#fff" opacity=".22"/>')
    b.append(T(x+100,220,t,17,'#222',w='bold')); b.append(T(x+100,242,d1,13,GRIS)); b.append(T(x+100,262,'→ '+d2,13,VERDE,w='bold'))
b.append(arrow(130,295,770,295,VERDE,3)); b.append(T(450,320,'la herida avanza hacia la cicatrización',13,VERDE))
svg(SI,'lecho.svg',900,335,''.join(b))

# Agua corporal 60-40-20
b=[T(450,26,'Agua corporal total (adulto de 70 kg): regla 60-40-20',18,VERDE,w='bold')]
b.append(f'<rect x="40" y="60" width="820" height="60" fill="#e9e3d6" stroke="#bbb"/>'); b.append(T(450,96,'Peso corporal 100 %',15,'#555',w='bold'))
b.append(f'<rect x="40" y="130" width="492" height="60" fill="#9fd3f2" stroke="#2b6cb0"/>'); b.append(T(286,166,'Agua corporal total 60 % (≈ 42 L)',15,'#0d4f80',w='bold'))
b.append(f'<rect x="532" y="130" width="328" height="60" fill="#f2f2f2" stroke="#bbb"/>'); b.append(T(696,166,'Sólidos 40 %',14,'#777'))
b.append(f'<rect x="40" y="200" width="328" height="80" fill="#5aa9e6"/>'); b.append(TL(204,232,['Intracelular','2/3 del agua = 40 % del peso (≈ 28 L)','K⁺ es el catión principal'],14,'#fff','middle','bold'))
b.append(f'<rect x="368" y="200" width="123" height="80" fill="#f7b267"/>'); b.append(TL(429,226,['Intersticial','3/4 del EC','≈ 10.5 L'],13,'#5a3200','middle','bold'))
b.append(f'<rect x="491" y="200" width="41" height="80" fill="#e56b6f"/>'); b.append(TL(511,236,['Plasma'],11,'#fff','middle','bold'))
b.append(f'<path d="M368,292 V302 H532 V292" fill="none" stroke="#333" stroke-width="2"/>'); b.append(T(450,322,'Extracelular 1/3 = 20 % del peso (≈ 14 L) · Na⁺ es el catión principal',13,'#333',w='bold'))
b.append(T(450,350,'El plasma es 1/4 del extracelular (≈ 3.5 L). Por eso de 1 L de salina 0.9 % solo ≈ 250 mL se quedan en el vaso.',12,GRIS))
svg(SI,'agua-corporal.svg',900,365,''.join(b))

# Catéteres
b=[T(450,26,'Catéteres periféricos: calibre, color y flujo',18,VERDE,w='bold')]
cat=[('14 G','#f26b21','≈ 270–300'),('16 G','#9e9e9e','≈ 180–220'),('18 G','#2e9d4a','≈ 90–100'),('20 G','#ec6fa2','≈ 55–60'),('22 G','#2b6cb0','≈ 30–35'),('24 G','#f4c430','≈ 18–20')]
for i,(g,c,fl) in enumerate(cat):
    y=60+i*48; wid=26-i*3.6
    b.append(f'<rect x="40" y="{y}" width="90" height="34" rx="6" fill="{c}"/>'); b.append(T(85,y+23,g,15,'#fff' if g not in ('24 G',) else '#222','middle','bold'))
    b.append(f'<rect x="130" y="{y+17-wid/2}" width="300" height="{wid}" fill="#d9e4ec" stroke="#8aa"/>')
    b.append(T(450,y+23,fl+' mL/min',14,'#222','start'))
b.append(T(700,90,'Ley de Poiseuille',15,VERDE,'middle','bold'))
b.append(T(700,120,'Flujo ∝ r⁴ / longitud',16,'#222','middle','bold'))
b.append(TL(700,152,['Doble el radio → 16 veces el flujo.','Más corto y más grueso = más rápido.','En trauma y choque: 14–16 G.','Transfusión: ≥ 18–20 G.'],13,GRIS))
b.append(T(450,355,'Los flujos son aproximados y cambian con la marca; el color sí es estándar (ISO 10555).',12,GRIS))
svg(SI,'cateteres.svg',900,370,''.join(b))

# Gasometría: algoritmo
b=[T(450,26,'Gasometría arterial paso a paso',18,VERDE,w='bold')]
b.append(tbox(330,46,240,44,['1. pH (7.35–7.45)'],'#e8f5ee',VERDE,15,VERDE,'bold'))
b.append(arrow(400,90,230,130)); b.append(arrow(500,90,670,130))
b.append(tbox(100,132,260,44,['pH < 7.35: ACIDEMIA'],'#fdecea',ROJO,15,ROJO,'bold'))
b.append(tbox(540,132,260,44,['pH > 7.45: ALCALEMIA'],'#e8f0fb',AZUL,15,AZUL,'bold'))
for x,t1,t2,c in ((20,'PaCO₂ > 45','Acidosis respiratoria',ROJO),(240,'HCO₃⁻ < 22','Acidosis metabólica',ROJO),(460,'PaCO₂ < 35','Alcalosis respiratoria',AZUL),(680,'HCO₃⁻ > 26','Alcalosis metabólica',AZUL)):
    b.append(tbox(x,224,200,58,[t1,t2],'#fff',c,14,c,'bold'))
b.append(arrow(230,176,120,222,ROJO,2)); b.append(arrow(230,176,340,222,ROJO,2)); b.append(arrow(670,176,560,222,AZUL,2)); b.append(arrow(670,176,780,222,AZUL,2))
b.append(T(450,314,'2. ¿Qué lo explica? PaCO₂ (35–45) y HCO₃⁻ (22–26)',14,'#222'))
b.append(T(450,340,'3. ¿Compensa? Metabólica: Winter → PaCO₂ esperada = 1.5 × HCO₃⁻ + 8 ± 2',14,'#222'))
b.append(T(450,366,'4. Si es acidosis metabólica: anion gap = Na⁺ − (Cl⁻ + HCO₃⁻); normal 8–12',14,'#222'))
svg(SI,'gasometria.svg',900,385,''.join(b))

# Anion gap (gamblegram)
b=[T(400,26,'Anion gap: cationes = aniones',18,VERDE,w='bold')]
sc=2.2; base=360
def col(x,parts):
    o=[]; y=base
    for v,c,t in parts:
        h=v*sc; y-=h; o.append(f'<rect x="{x}" y="{y:.1f}" width="150" height="{h:.1f}" fill="{c}" stroke="#fff" stroke-width="2"/>'); o.append(T(x+75,y+h/2+5,t,13,'#fff' if c not in ('#ffe08a','#eee') else '#222','middle','bold'))
    return ''.join(o)
b.append(col(60,[(140,'#2b6cb0','Na⁺ 140')]))
b.append(col(230,[(104,'#00573c','Cl⁻ 104'),(24,'#5aa9e6','HCO₃⁻ 24'),(12,'#ffe08a','AG 12')]))
b.append(T(135,base+24,'Cationes',14,'#222',w='bold')); b.append(T(305,base+24,'Aniones medidos',14,'#222',w='bold'))
b.append(col(480,[(104,'#00573c','Cl⁻ 104'),(10,'#5aa9e6','HCO₃⁻ 10'),(26,'#f26b21','AG 26')]))
b.append(T(555,base+24,'AG elevado',14,NAR,w='bold'))
b.append(TL(770,150,['Se acumula un ácido','no medido: lactato,','cetonas, urea, tóxicos','(metanol, etilenglicol,','salicilatos)'],13,GRIS))
b.append(T(400,base+52,'Si el AG es normal, el HCO₃⁻ perdido se reemplaza por Cl⁻ (hiperclorémica: diarrea, ATR, salina en exceso).',12,GRIS))
svg(SI,'anion-gap.svg',900,425,''.join(b))

# Pupilas por nivel
b=[T(450,26,'Pupilas en el paciente en coma: dónde está la lesión',18,VERDE,w='bold')]
def ojo(cx,cy,r,dot=False):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="44" ry="26" fill="#fff" stroke="#555" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="20" fill="#7a9cc6"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#111"/>')
P=[('Diencefálica','Pequeñas, reactivas',4,4),('Uncal (III par)','Midriasis unilateral fija',4,16),('Mesencefálica','Medias, fijas',9,9),('Protuberancia','Puntiformes',1.8,1.8),('Metabólica / tóxica','Pequeñas, reactivas (salvo tóxicos)',5,5)]
for i,(t,d,r1,r2) in enumerate(P):
    y=70+i*66
    b.append(ojo(70,y+16,r1)); b.append(ojo(170,y+16,r2))
    b.append(T(240,y+12,t,15,'#222','start','bold')); b.append(T(240,y+32,d,13,GRIS,'start'))
b.append(T(450,420,'Pupilas reactivas con coma profundo sugieren causa metabólica; la midriasis unilateral es herniación uncal hasta no demostrar lo contrario.',12,GRIS))
svg(SI,'pupilas.svg',900,435,''.join(b))

# ───────────────────────── BIOQUÍMICA ─────────────────────────
BQ='bioquimica'
# Michaelis-Menten
b=[T(400,26,'Cinética de Michaelis-Menten',18,VERDE,w='bold')]
X=lambda s:90+s*6.2; Y=lambda v:360-v*2.8
b.append(axes(90,360,740,60,'[S] concentración de sustrato','Velocidad (v)'))
b.append(f'<line x1="{X(0)}" y1="{Y(100)}" x2="{X(100)}" y2="{Y(100)}" stroke="{ROJO}" stroke-dasharray="6 5" stroke-width="2"/>'); b.append(T(X(100)+4,Y(100)+5,'Vmáx',14,ROJO,'end',))
b.append(f'<path d="{curve(lambda s:100*s/(15+s),0,100,X,Y)}" fill="none" stroke="{VERDE}" stroke-width="4"/>')
b.append(f'<line x1="{X(0)}" y1="{Y(50)}" x2="{X(15)}" y2="{Y(50)}" stroke="{AZUL}" stroke-dasharray="5 4" stroke-width="2"/><line x1="{X(15)}" y1="{Y(50)}" x2="{X(15)}" y2="{Y(0)}" stroke="{AZUL}" stroke-dasharray="5 4" stroke-width="2"/>')
b.append(T(X(0)-6,Y(50)+5,'Vmáx/2',13,AZUL,'end')); b.append(T(X(15),Y(0)+18,'Km',14,AZUL,w='bold'))
b.append(TL(X(55),Y(40),['v = Vmáx·[S] / (Km + [S])','Km bajo = mucha afinidad','(se satura con poco sustrato)'],14,'#222','start'))
svg(BQ,'michaelis.svg',800,410,''.join(b))

# Inhibición (Lineweaver-Burk)
b=[T(450,26,'Inhibición enzimática: dobles recíprocos (Lineweaver-Burk)',17,VERDE,w='bold')]
for X0,tit,lines,txt in ((20,'Competitiva',[(0.6,0.5,VERDE,'sin inhibidor'),(0.6,1.0,ROJO,'con inhibidor')],['Mismo cruce en el eje Y: Vmáx igual','Km aumenta (se vence con más sustrato)']),
                         (460,'No competitiva',[(0.6,0.5,VERDE,'sin inhibidor'),(1.2,1.0,ROJO,'con inhibidor')],['Mismo cruce en el eje X: Km igual','Vmáx disminuye'])):
    ox,oy=X0+150,300
    b.append(T(X0+210,60,tit,16,'#222',w='bold'))
    b.append(f'<line x1="{X0+20}" y1="{oy}" x2="{X0+410}" y2="{oy}" stroke="#222" stroke-width="2"/><line x1="{ox}" y1="{oy+20}" x2="{ox}" y2="80" stroke="#222" stroke-width="2"/>')
    b.append(T(X0+405,oy+20,'1/[S]',12,'#222','end')); b.append(T(ox+6,90,'1/v',12,'#222','start'))
    for k,(i0,sl,c,lab) in enumerate(lines):
        # y = i0 + sl*x  (en unidades: 1 unidad = 100 px en x, 100 px en y)
        if tit=='Competitiva': x_int=-i0/sl
        else: x_int=-i0/sl
        x1=max(x_int-0.15,-1.35); x2=1.8; K=60
        b.append(f'<line x1="{ox+x1*100:.1f}" y1="{oy-(i0+sl*x1)*K:.1f}" x2="{ox+x2*100:.1f}" y2="{oy-(i0+sl*x2)*K:.1f}" stroke="{c}" stroke-width="3"/>')
        b.append(T(ox+x2*100+6,oy-(i0+sl*x2)*K+4,lab,12,c,'start','bold'))
    b.append(TL(X0+210,345,txt,13,GRIS))
b.append(T(450,395,'Cruce con el eje Y = 1/Vmáx · cruce con el eje X = −1/Km',13,'#333',w='bold'))
svg(BQ,'inhibicion.svg',900,410,''.join(b))

# Curva de disociación de la Hb
b=[T(400,26,'Curva de disociación de la hemoglobina',18,VERDE,w='bold')]
X=lambda p:90+p*6.2; Y=lambda s:360-s*2.8
hill=lambda p50:(lambda p:100*p**2.7/(p50**2.7+p**2.7))
b.append(axes(90,360,740,60,'PO₂ (mmHg)','Saturación de Hb (%)'))
for p in (0,20,40,60,80,100): b.append(T(X(p),376,str(p),11,GRIS))
b.append(f'<path d="{curve(hill(20),0.1,100,X,Y)}" fill="none" stroke="{AZUL}" stroke-width="3" stroke-dasharray="7 5"/>')
b.append(f'<path d="{curve(hill(26.8),0.1,100,X,Y)}" fill="none" stroke="{VERDE}" stroke-width="4"/>')
b.append(f'<path d="{curve(hill(36),0.1,100,X,Y)}" fill="none" stroke="{ROJO}" stroke-width="3" stroke-dasharray="7 5"/>')
b.append(f'<line x1="{X(0)}" y1="{Y(50)}" x2="{X(26.8)}" y2="{Y(50)}" stroke="#999" stroke-dasharray="4 4"/><line x1="{X(26.8)}" y1="{Y(50)}" x2="{X(26.8)}" y2="{Y(0)}" stroke="#999" stroke-dasharray="4 4"/>')
b.append(T(X(26.8)+4,Y(4),'P50 ≈ 27',12,'#555','start'))
b.append(TL(X(52),Y(36),['Derecha (rojo): ↓ afinidad, entrega O₂','↑ CO₂, ↑ H⁺ (↓ pH), ↑ temperatura, ↑ 2,3-BPG'],13,ROJO,'start'))
b.append(TL(X(52),Y(18),['Izquierda (azul): ↑ afinidad','Hb fetal, CO, alcalosis, hipotermia'],13,AZUL,'start'))
svg(BQ,'curva-hb.svg',800,410,''.join(b))

# Glucólisis
b=[T(450,26,'Glucólisis (citosol)',18,VERDE,w='bold')]
st=[('Glucosa','',''),('Glucosa-6-P','Hexocinasa / glucocinasa','−1 ATP'),('Fructosa-6-P','Fosfoglucosa isomerasa',''),('Fructosa-1,6-bisP','PFK-1 (paso limitante)','−1 ATP'),
    ('Gliceraldehído-3-P (×2)','Aldolasa + triosa fosfato isomerasa',''),('1,3-bisfosfoglicerato (×2)','G3P deshidrogenasa','+2 NADH'),('3-fosfoglicerato (×2)','Fosfoglicerato cinasa','+2 ATP'),
    ('Fosfoenolpiruvato (×2)','Mutasa + enolasa',''),('Piruvato (×2)','Piruvato cinasa','+2 ATP')]
for i,(m,e,a) in enumerate(st):
    y=46+i*50; irr=e.startswith(('Hexo','PFK','Piruvato c'))
    b.append(tbox(300,y,300,34,[m],'#fff' if not irr else '#fff4e0',NAR if irr else '#888',14,'#222','bold'))
    if i:
        b.append(arrow(450,y-16,450,y-1,ROJO if irr else '#555',3 if irr else 2,8))
        b.append(T(290,y-4,e,12,ROJO if irr else GRIS,'end','bold' if irr else 'normal'))
        if a: b.append(T(610,y-4,a,13,VERDE if a.startswith('+') else ROJO,'start','bold'))
b.append(TL(780,140,['Balance neto','2 ATP + 2 NADH','+ 2 piruvato'],15,VERDE,'middle','bold'))
b.append(TL(780,260,['En rojo: pasos','irreversibles','(la gluconeogénesis','los rodea)'],12,ROJO))
svg(BQ,'glucolisis.svg',900,500,''.join(b))

# Ciclo de Krebs
b=[T(400,26,'Ciclo de Krebs (matriz mitocondrial)',18,VERDE,w='bold')]
inter=['Citrato','Isocitrato','α-cetoglutarato','Succinil-CoA','Succinato','Fumarato','Malato','Oxalacetato']
prod={1:'NADH + CO₂',2:'NADH + CO₂',3:'GTP',4:'FADH₂',6:'NADH'}
cx,cy,R=400,285,178
RX=250
pts=[(cx+RX*math.cos(-math.pi/2+(i+.5)*2*math.pi/8),cy+R*math.sin(-math.pi/2+(i+.5)*2*math.pi/8)) for i in range(8)]
b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{RX}" ry="{R}" fill="none" stroke="#c7dccf" stroke-width="10"/>')
for i in range(8):
    a1=-math.pi/2+(i+.5)*2*math.pi/8+0.22; a2=-math.pi/2+(i+1.5)*2*math.pi/8-0.22
    x1,y1=cx+RX*math.cos(a1),cy+R*math.sin(a1); x2,y2=cx+RX*math.cos(a2),cy+R*math.sin(a2)
    b.append(arrow(x1,y1,x2,y2,VERDE,2.5,9))
    if i in prod:
        am=(a1+a2)/2; b.append(T(cx+(RX+30)*math.cos(am),cy+(R+30)*math.sin(am)+5,prod[i],13,NAR if 'NADH' in prod[i] or 'FAD' in prod[i] else AZUL,'middle','bold'))
for (x,y),n in zip(pts,inter): b.append(tbox(x-66,y-16,132,32,[n],'#fff','#00573c',13,'#222','bold'))
b.append(tbox(cx+60,40,160,34,['Acetil-CoA (2C)'],'#fff4e0',NAR,14,'#222','bold'))
b.append(arrow(cx+140,74,pts[0][0]+10,pts[0][1]-17,NAR,2.5,9))
b.append(TL(cx,cy-8,['Por cada acetil-CoA:','3 NADH · 1 FADH₂','1 GTP · 2 CO₂'],14,VERDE,'middle','bold'))
svg(BQ,'krebs.svg',800,520,''.join(b))

# Cadena de transporte de electrones
b=[T(450,26,'Cadena respiratoria y ATP sintasa (membrana mitocondrial interna)',17,VERDE,w='bold')]
b.append(f'<rect x="20" y="170" width="860" height="70" fill="#ffe7a3"/>')
b.append(T(30,110,'Espacio intermembrana (muchos H⁺)',13,GRIS,'start')); b.append(T(30,300,'Matriz',13,GRIS,'start'))
cpx=[(90,'I','#5aa9e6'),(230,'II','#9fd3f2'),(390,'III','#7b3fa0'),(560,'IV','#b3261e')]
for x,n,c in cpx:
    hh=110 if n!='II' else 60; yy=150 if n!='II' else 185
    b.append(f'<rect x="{x}" y="{yy}" width="80" height="{hh}" rx="14" fill="{c}"/>'); b.append(T(x+40,yy+hh/2+6,n,20,'#fff',w='bold'))
    if n!='II': b.append(arrow(x+40,150,x+40,95,ROJO,2.5,9)); b.append(T(x+40,85,'H⁺',14,ROJO,w='bold'))
b.append(f'<circle cx="320" cy="205" r="16" fill="{NAR}"/>'); b.append(T(320,210,'Q',13,'#fff',w='bold'))
b.append(f'<circle cx="490" cy="150" r="14" fill="#c2185b"/>'); b.append(T(490,154,'c',12,'#fff',w='bold'))
b.append(T(130,300,'NADH → NAD⁺',13,'#222',w='bold')); b.append(T(270,300,'FADH₂ → FAD',13,'#222',w='bold'))
b.append(T(600,300,'½ O₂ + 2H⁺ → H₂O',13,'#222',w='bold'))
b.append(f'<rect x="720" y="150" width="70" height="110" rx="12" fill="{VERDE}"/>'); b.append(T(755,210,'ATP',14,'#fff',w='bold'))
b.append(f'<circle cx="755" cy="285" r="26" fill="{VERDE}"/>'); b.append(arrow(755,95,755,148,ROJO,2.5,9)); b.append(T(755,85,'H⁺',14,ROJO,w='bold'))
b.append(T(755,330,'ADP + Pi → ATP',13,VERDE,w='bold')); b.append(T(755,350,'ATP sintasa (V)',12,VERDE))
inh=['Inhibidores: I = rotenona · III = antimicina A · IV = cianuro, CO, azida · V = oligomicina','Desacopladores (2,4-dinitrofenol, termogenina): dejan pasar H⁺ sin hacer ATP → calor']
b.append(TL(450,385,inh,13,'#333'))
svg(BQ,'cadena.svg',900,420,''.join(b))

# Lipoproteínas
b=[T(450,26,'Lipoproteínas: tamaño, densidad y función',18,VERDE,w='bold')]
lp=[('Quilomicrón',70,'#f7d774','Grasa de la dieta → tejidos','ApoB-48, C-II, E'),('VLDL',50,'#f7b267','TG del hígado → tejidos','ApoB-100, C-II, E'),
    ('IDL',36,'#f4978e','Restos de VLDL','ApoB-100, E'),('LDL',28,'#e56b6f','Colesterol → tejidos («malo»)','ApoB-100'),('HDL',16,'#5aa9e6','Colesterol de tejidos → hígado («bueno»)','ApoA-I')]
x=40
for n,r,c,f,apo in lp:
    cx=x+r; b.append(f'<circle cx="{cx}" cy="140" r="{r}" fill="{c}" stroke="#fff" stroke-width="3"/>'); b.append(f'<circle cx="{cx}" cy="140" r="{r}" fill="none" stroke="#999" stroke-width="1" stroke-dasharray="3 3"/>')
    b.append(T(cx,240,n,15,'#222',w='bold')); b.append(TL(cx,262,[f[:f.find('→')+1] if '→' in f else f, f[f.find('→')+2:] if '→' in f else ''],11,GRIS)); b.append(T(cx,302,apo,11,VERDE,w='bold'))
    x+=2*r+(110 if r<40 else 70)
b.append(arrow(60,340,840,340,AZUL,2.5)); b.append(T(60,360,'más grande, más triglicéridos, menos densa',12,AZUL,'start')); b.append(T(840,360,'más pequeña, más proteína, más densa',12,AZUL,'end'))
svg(BQ,'lipoproteinas.svg',900,375,''.join(b))

# Ciclo de la urea
b=[T(450,26,'Ciclo de la urea (hígado)',18,VERDE,w='bold')]
b.append(f'<rect x="20" y="50" width="330" height="360" rx="22" fill="#fff4e0" stroke="{NAR}" stroke-width="2"/>'); b.append(T(185,74,'Mitocondria',14,NAR,w='bold'))
b.append(T(620,74,'Citosol',14,GRIS,w='bold'))
b.append(tbox(40,100,290,40,['NH₄⁺ + HCO₃⁻ + 2 ATP'],'#fff','#888',13))
b.append(arrow(185,140,185,185)); b.append(T(195,168,'CPS-I (activada por N-acetilglutamato)',11,ROJO,'start','bold'))
b.append(tbox(70,188,230,36,['Carbamoil fosfato'],'#fff',NAR,14,'#222','bold'))
b.append(tbox(70,300,230,36,['Ornitina'],'#fff',NAR,14,'#222','bold'))
b.append(tbox(70,248,0,0,[''],'#fff','#fff',1))
b.append(f'<path d="M185,224 V262" stroke="#555" stroke-width="2"/><path d="M185,300 V275" stroke="#555" stroke-width="2"/>')
b.append(arrow(185,268,420,140,'#555',2.5)); b.append(T(270,190,'OTC',12,ROJO,'start','bold'))
b.append(tbox(420,110,180,36,['Citrulina'],'#fff','#555',14,'#222','bold'))
b.append(arrow(600,128,680,170)); b.append(T(700,150,'+ aspartato, ATP',12,GRIS,'start'))
b.append(tbox(640,172,200,36,['Argininosuccinato'],'#fff','#555',14,'#222','bold'))
b.append(arrow(740,208,740,250)); b.append(T(750,236,'→ fumarato (a Krebs)',12,GRIS,'start'))
b.append(tbox(660,252,160,36,['Arginina'],'#fff','#555',14,'#222','bold'))
b.append(arrow(660,280,560,330)); b.append(T(620,330,'arginasa',12,ROJO,'start','bold'))
b.append(tbox(420,330,140,40,['UREA → orina'],'#e8f5ee',VERDE,14,VERDE,'bold'))
b.append(arrow(660,288,305,318,'#555',2.5,10,'6 4')); b.append(T(480,300,'ornitina regresa',12,GRIS))
b.append(T(450,440,'Defecto de OTC (ligado al X, el más común): hiperamonemia + ácido orótico alto.',13,'#333'))
svg(BQ,'urea.svg',900,455,''.join(b))
print('ok')
