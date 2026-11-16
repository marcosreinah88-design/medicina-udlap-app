# Esquemas propios (SVG, en español) para Anatomía Humana I (2º) y Anatomía 2 (3º).
# Dibujados desde cero (no copian figuras de libros).
# Uso: python3 tools-s12/esquemas_anatomia.py
#   Anatomía I  -> tools-s12/img/anatomia-humana-i/
#   Anatomía 2  -> site/s3/anatomia/img/  (la guía de 3º no usa build.py)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Reusa los ayudantes de dibujo de esquemas_s3.py (solo la parte de funciones, sin dibujar sus esquemas)
_src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'esquemas_s3.py'),encoding='utf-8').read()
exec(_src[:_src.index('# ───────────────────────── MICROBIOLOGÍA')])
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
def save(path, w, h, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {F}><rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')
A1 = os.path.join(HERE, 'img', 'anatomia-humana-i')
A2 = os.path.join(ROOT, 'site', 's3', 'anatomia', 'img')
def L(x1,y1,x2,y2,c='#444',w=3): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'

# ───────── Plexo braquial (raíces → troncos → divisiones → fascículos → ramas) ─────────
b=[]
cols=[('Raíces',70),('Troncos',230),('Divisiones',390),('Fascículos',560),('Ramas terminales',760)]
for t,x in cols: b.append(T(x,34,t,15,GRIS,w='bold'))
R={'C5':80,'C6':140,'C7':200,'C8':260,'T1':320}
for k,y in R.items(): b.append(tbox(40,y-17,60,34,[k],'#eef6f2',VERDE,15,VERDE,'bold'))
TR={'Superior':110,'Medio':200,'Inferior':290}
for k,y in TR.items(): b.append(tbox(180,y-17,100,34,[k],'#fff4ec',NAR,14))
b+= [L(100,80,180,110),L(100,140,180,110),L(100,200,180,200),L(100,260,180,290),L(100,320,180,290)]
DV={'sup-a':(390,90),'sup-p':(390,130),'med-a':(390,185),'med-p':(390,215),'inf-a':(390,275),'inf-p':(390,305)}
for k,(x,y) in DV.items():
    ant=k.endswith('a'); b.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{"#fff" if ant else "#ddd"}" stroke="#555" stroke-width="2"/>')
b+= [L(280,110,383,90),L(280,110,383,130),L(280,200,383,185),L(280,200,383,215),L(280,290,383,275),L(280,290,383,305)]
b.append(T(390,350,'○ anterior   ● posterior',12,GRIS))
FA={'Lateral':(560,100,'#e8f0fb',AZUL),'Posterior':(560,200,'#f2f2f2','#555'),'Medial':(560,300,'#f6ecfa',MOR)}
for k,(x,y,f,c) in FA.items(): b.append(tbox(x-55,y-17,110,34,[k],f,c,14,c,'bold'))
b+= [L(397,90,505,100,AZUL),L(397,185,505,100,AZUL),L(397,130,505,200),L(397,215,505,200),L(397,305,505,200),L(397,275,505,300,MOR)]
RM=[('Musculocutáneo','C5–C7',70,'Lateral',AZUL),('Mediano','C5–T1',150,'Lat + Med','#1b6b4a'),('Axilar','C5–C6',215,'Posterior','#555'),('Radial','C5–T1',265,'Posterior','#555'),('Cubital (ulnar)','C8–T1',335,'Medial',MOR)]
for n,raiz,y,_,c in RM: b.append(tbox(690,y-18,150,36,[n],'#fff',c,14,c,'bold')); b.append(T(850,y+5,raiz,12,GRIS,'start'))
b+= [L(615,100,690,70,AZUL),L(615,100,690,150,AZUL),L(615,300,690,150,MOR),L(615,200,690,215),L(615,200,690,265),L(615,300,690,335,MOR)]
b.append(T(40,395,'Lesiones clásicas',15,ROJO,'start','bold'))
b.append(TL(40,420,['Erb-Duchenne (tronco superior, C5–C6): brazo en «propina de mesero», aducido y en rotación medial.','Klumpke (tronco inferior, C8–T1): mano en garra; puede haber Horner si se lesiona T1.','Axilar: fractura del cuello quirúrgico del húmero · Radial: diáfisis humeral (mano caída) · Mediano: túnel del carpo'],13,'#333','start'))
b.append(T(450,500,'«Ríos Tienen Dos Corrientes Rápidas»: Raíces, Troncos, Divisiones, Cordones (fascículos), Ramas',13,VERDE,'middle','bold'))
save(os.path.join(A1,'plexo-braquial.svg'),920,520,''.join(b))

# ───────── Triángulos del cuello ─────────
b=[]
# cuello visto de lado: mandíbula arriba, clavícula abajo, ECM diagonal, trapecio posterior
b.append('<path d="M120,70 Q300,40 470,90" stroke="#888" stroke-width="5" fill="none"/>')
b.append(T(300,40,'Borde inferior de la mandíbula',13,GRIS))
b.append('<path d="M80,420 L520,420" stroke="#888" stroke-width="7"/>'); b.append(T(300,445,'Clavícula',13,GRIS))
b.append('<path d="M100,70 L100,420" stroke="#bbb" stroke-width="2" stroke-dasharray="6 5"/>'); b.append(f'<text x="88" y="250" font-size="13" fill="{GRIS}" text-anchor="middle" transform="rotate(-90 88 250)">Línea media</text>')
# ECM
b.append('<path d="M440,95 L470,105 L215,420 L175,420 Z" fill="#f4b6a6" stroke="#c0604a" stroke-width="2"/>')
b.append(f'<text x="345" y="260" font-size="14" fill="#8a3324" text-anchor="middle" transform="rotate(-51 345 260)">Esternocleidomastoideo</text>')
# trapecio
b.append('<path d="M520,110 L560,120 L560,420 L470,420 Z" fill="#f4c9a6" stroke="#c0804a" stroke-width="2"/>')
b.append(f'<text x="535" y="300" font-size="13" fill="#8a5324" text-anchor="middle" transform="rotate(-80 535 300)">Trapecio</text>')
# omohioideo vientre inferior en triángulo posterior y superior en anterior
b.append('<path d="M330,180 Q250,230 180,250" stroke="#b56" stroke-width="5" fill="none"/>')
b.append('<path d="M405,330 Q450,360 500,330" stroke="#b56" stroke-width="5" fill="none"/>')
b.append(T(240,270,'Omohioideo',12,'#a04060'))
# digástrico
b.append('<path d="M150,110 Q260,190 420,110" stroke="#9a6" stroke-width="5" fill="none"/>'); b.append(T(290,175,'Digástrico',12,'#4a7a2a'))
b.append(TL(205,350,['Triángulo','anterior'],15,AZUL,'middle','bold'))
b.append(TL(480,250,['Triángulo','posterior'],15,NAR,'middle','bold'))
lst=[('Submandibular (digástrico)','glándula submandibular, arteria facial'),('Submentoniano','ganglios submentonianos'),('Carotídeo','bifurcación carotídea, yugular interna, X y XII'),('Muscular','infrahioideos, tiroides'),('Posterior: occipital y supraclavicular','nervio accesorio (XI), plexo cervical, subclavia')]
b.append(T(600,70,'Subdivisiones y contenido',15,'#222','start','bold'))
for i,(a,c) in enumerate(lst):
    y=105+i*62; b.append(T(600,y,a,14,AZUL if i<4 else NAR,'start','bold')); b.append(T(600,y+20,c,13,'#444','start'))
b.append(TL(600,430,['El anterior queda entre la línea media, la mandíbula y el ECM;','el posterior entre el ECM, el trapecio y la clavícula.'],12,GRIS,'start'))
save(os.path.join(A1,'triangulos-cuello.svg'),980,470,''.join(b))

# ───────── Segmentos de Couinaud ─────────
b=[]
b.append('<path d="M60,200 Q60,70 260,60 Q480,50 620,110 Q700,150 640,200 Q560,280 380,330 Q200,360 100,300 Q60,260 60,200Z" fill="#c9805e" stroke="#7a3b22" stroke-width="3"/>')
b.append('<line x1="330" y1="55" x2="300" y2="345" stroke="#fff" stroke-width="3" stroke-dasharray="8 6"/>')
b.append(T(335,48,'Línea de Cantlie (vesícula → VCI)',13,'#222'))
b.append('<line x1="470" y1="70" x2="520" y2="270" stroke="#fff" stroke-width="2" stroke-dasharray="4 5"/>')
b.append('<line x1="150" y1="90" x2="200" y2="330" stroke="#fff" stroke-width="2" stroke-dasharray="4 5"/>')
b.append('<line x1="70" y1="200" x2="330" y2="185" stroke="#fff" stroke-width="2" stroke-dasharray="4 5"/>')
b.append('<line x1="500" y1="175" x2="650" y2="160" stroke="#fff" stroke-width="2" stroke-dasharray="4 5"/>')
seg=[('VII',110,150),('VI',140,265),('VIII',245,135),('V',245,270),('IVa',400,130),('IVb',395,260),('II',560,130),('III',560,215),('I',330,200)]
for s,x,y in seg:
    b.append(f'<circle cx="{x}" cy="{y-6}" r="22" fill="#fff" fill-opacity=".9"/>'); b.append(T(x,y,s,17,'#5a2410',w='bold'))
b.append(T(200,390,'Hígado derecho: V–VIII',15,'#7a3b22','middle','bold')); b.append(T(500,390,'Hígado izquierdo: II–IV',15,'#7a3b22','middle','bold'))
b.append(TL(350,420,['I = lóbulo caudado (drena directo a la VCI). Vista anterior esquemática. Cada segmento tiene su propia rama portal, arterial y biliar, y se reseca por separado.','Las venas suprahepáticas (líneas finas) separan los sectores; el plano portal separa arriba (VII, VIII, IVa, II) de abajo (VI, V, IVb, III).'],12,GRIS))
save(os.path.join(A2,'couinaud.svg'),700,460,''.join(b))

# ───────── Hernias inguinales y triángulo de Hesselbach ─────────
b=[]
b.append(T(330,30,'Pared abdominal anterior vista desde dentro (lado derecho)',14,GRIS,'middle','bold'))
b.append('<path d="M60,330 Q330,380 600,330" stroke="#b08850" stroke-width="7" fill="none"/>'); b.append(T(330,385,'Ligamento inguinal',13,'#7a5a20'))
b.append('<rect x="70" y="60" width="90" height="270" fill="#f3c7b8" stroke="#c0604a" stroke-width="2"/>'); b.append(f'<text x="115" y="200" font-size="14" fill="#8a3324" text-anchor="middle" transform="rotate(-90 115 200)">Borde del recto abdominal</text>')
b.append('<path d="M330,330 Q300,200 260,60" stroke="#c0392b" stroke-width="6" fill="none"/>'); b.append(T(300,52,'Vasos epigástricos inferiores',13,ROJO))
b.append('<path d="M160,330 L160,150 Q230,250 318,330 Z" fill="#2b6cb0" fill-opacity=".14" stroke="#2b6cb0" stroke-width="2" stroke-dasharray="6 4"/>')
b.append(TL(205,275,['Triángulo','de Hesselbach'],13,AZUL,'middle','bold'))
b.append('<ellipse cx="420" cy="300" rx="34" ry="22" fill="#fff" stroke="#00573c" stroke-width="3"/>'); b.append(TL(420,250,['Anillo inguinal','profundo'],13,VERDE,'middle','bold'))
b.append(arrow(545,250,455,292,NAR,3)); b.append(TL(565,190,['Hernia indirecta:','lateral a los vasos,','entra por el anillo profundo'],13,NAR,'middle','bold'))
b.append(arrow(110,420,205,320,MOR,3)); b.append(TL(110,440,['Hernia directa: medial a los vasos,','empuja la fascia transversalis (Hesselbach)'],13,MOR,'start','bold'))
b.append(TL(330,500,['Hesselbach = borde del recto (medial) · vasos epigástricos inferiores (lateral) · ligamento inguinal (inferior).','Femoral: por debajo del ligamento inguinal, medial a la vena femoral (más en mujeres).'],12,'#333'))
save(os.path.join(A2,'hernias-inguinales.svg'),680,535,''.join(b))
print('ok')
