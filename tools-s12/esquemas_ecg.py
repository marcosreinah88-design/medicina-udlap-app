# Dibuja los esquemas propios de ECG de Fisiología Clínica (basados en «Electro en esquemas», Sustancia P).
# Uso: python3 tools-s12/esquemas_ecg.py tools-s12/img/fisiologia-clinica   (imprime las posiciones % para los marcadores ^^)
import math, os, sys
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
F = 'font-family="Helvetica,Arial,sans-serif"'
ROJO='#b3261e'; VERDE='#00573c'; NAR='#f26b21'; AZUL='#2b6cb0'; MOR='#7b3fa0'; GRIS='#555'
def svg(name, w, h, body):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {F}><rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>'
    open(os.path.join(OUT, name), 'w').write(s)
def grid(x0, y0, w, h, mm):
    o = []
    n = int(w/mm); m = int(h/mm)
    for i in range(n+1):
        x = x0+i*mm; big = i % 5 == 0
        o.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0+m*mm}" stroke="{"#f19aa8" if big else "#fbd9df"}" stroke-width="{1.4 if big else .7}"/>')
    for j in range(m+1):
        y = y0+j*mm; big = j % 5 == 0
        o.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+n*mm}" y2="{y:.1f}" stroke="{"#f19aa8" if big else "#fbd9df"}" stroke-width="{1.4 if big else .7}"/>')
    return ''.join(o)
def g(t, c, a, s): return a*math.exp(-((t-c)/s)**2)
def beat(t):
    # t en segundos desde el inicio de la P; devuelve mm
    return (g(t,.05,1.5,.025) + g(t,.155,-1.2,.006) + g(t,.175,13,.009) + g(t,.198,-3.2,.008)
            + g(t,.43,3.2,.055) + g(t,.36,.4,.05))
def path(x0, y0, pxmm, dur, fn, step=.002):
    pts = []
    t = 0
    while t <= dur:
        pts.append(f'{x0+t*25*pxmm:.1f},{y0-fn(t)*pxmm:.1f}')
        t += step
    return 'M' + ' L'.join(pts)
def arrow(x1,y1,x2,y2,c,w=3,head=11):
    a = math.atan2(y2-y1, x2-x1)
    hx1 = x2-head*math.cos(a-.4); hy1 = y2-head*math.sin(a-.4)
    hx2 = x2-head*math.cos(a+.4); hy2 = y2-head*math.sin(a+.4)
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2-head*.7*math.cos(a):.1f}" y2="{y2-head*.7*math.sin(a):.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{x2:.1f},{y2:.1f} L{hx1:.1f},{hy1:.1f} L{hx2:.1f},{hy2:.1f}Z" fill="{c}"/>')
def T(x,y,s,size=15,c='#222',anchor='middle',w='normal'):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{c}" text-anchor="{anchor}" font-weight="{w}">{s}</text>'

# 1) Papel
mm = 14
b = [grid(20, 30, 560, 280, mm)]
# un cuadro grande resaltado
X, Y = 20+mm*15, 30+mm*5
b.append(f'<rect x="{X}" y="{Y}" width="{5*mm}" height="{5*mm}" fill="none" stroke="{ROJO}" stroke-width="3"/>')
b.append(arrow(X, Y-10, X+5*mm, Y-10, AZUL, 2.5, 9)); b.append(T(X+2.5*mm, Y-16, '0.20 s', 14, AZUL, w='bold'))
b.append(arrow(X+5*mm+10, Y+5*mm, X+5*mm+10, Y, ROJO, 2.5, 9)); b.append(T(X+5*mm+16, Y+2.5*mm+5, '0.5 mV', 14, ROJO, 'start', 'bold'))
# cuadro chico
x2, y2 = 20+mm*28, 30+mm*12
b.append(f'<rect x="{x2}" y="{y2}" width="{mm}" height="{mm}" fill="#ffe08a" stroke="{NAR}" stroke-width="2.5"/>')
b.append(T(x2+mm+8, y2+10, '1 mm = 0.04 s', 13, GRIS, 'start', 'bold')); b.append(T(x2+mm+8, y2+26, '1 mm = 0.1 mV', 13, GRIS, 'start', 'bold'))
# pulso de calibración 10 mm
cx, cy = 20+mm*2, 30+mm*17
b.append(f'<path d="M{cx-mm},{cy} H{cx} V{cy-10*mm} H{cx+5*mm} V{cy} H{cx+7*mm}" fill="none" stroke="#111" stroke-width="2.5"/>')
b.append(T(cx+2.5*mm, cy-10*mm-8, '1 mV = 10 mm', 13, '#111', w='bold'))
# segundo
b.append(arrow(20+mm*25, 30+mm*19, 20+mm*25+25*mm*0+mm*25*0+mm*15, 30+mm*19, VERDE, 2.5, 9))
b.append(T(20+mm*32.5, 30+mm*19-7, '1 s = 5 cuadros grandes (25 mm/s)', 13, VERDE, w='bold'))
svg('papel.svg', 600, 330, ''.join(b))

# 2) Complejo PQRST con segmentos e intervalos (esquema: 1 cuadro chico = 0.04 s)
W, H = 640, 400; cell = 24; hs = cell/0.04; vs = 12; x0 = 60; y0 = 250
b = [grid(10, 20, 620, 360, cell/5*5/5*1 if False else cell/5*1*5/5)]
b = [grid(10, 20, 620, 360, cell)]
dur = .62
pts = []; t = 0
while t <= dur:
    pts.append(f'{x0+t*hs:.1f},{y0-beat(t)*vs:.1f}'); t += .002
b.append(f'<path d="M10,{y0} L{x0},{y0} L' + ' L'.join(pts) + f' L630,{y0}" fill="none" stroke="#111" stroke-width="3" stroke-linejoin="round"/>')
px = lambda t: x0+t*hs
def band(t1, t2, row, c, label):
    y = 302+row*28
    return (f'<rect x="{px(t1):.1f}" y="{y}" width="{px(t2)-px(t1):.1f}" height="24" rx="6" fill="{c}"/>'
            + T((px(t1)+px(t2))/2, y+17, label, 13, '#fff', w='bold'))
b.append(band(0, .15, 0, NAR, 'Intervalo PR'))
b.append(band(.15, .215, 0, ROJO, 'QRS'))
b.append(band(.215, .36, 0, VERDE, 'Segmento ST'))
b.append(band(.09, .15, 1, '#b58900', ''))
b.append(T(px(.09)-6, 302+28+17, 'Segmento PR', 13, '#8a6a00', 'end', 'bold'))
b.append(band(.15, .53, 2, MOR, 'Intervalo QT'))
for t in (0, .15, .215, .53):
    b.append(f'<line x1="{px(t):.1f}" y1="40" x2="{px(t):.1f}" y2="372" stroke="#777" stroke-dasharray="4 4" stroke-width="1"/>')
svg('complejo.svg', W, H, ''.join(b))
pc = lambda x, y: f'{100*x/W:.0f},{100*y/H:.0f}'
print('complejo', {'P': pc(px(.05), y0-1.5*vs-22), 'q': pc(px(.155)-20, y0+12), 'R': pc(px(.175)+22, y0-13*vs+10),
     'S': pc(px(.198)+20, y0+3.2*vs+4), 'J': pc(px(.215)+22, y0-16), 'T': pc(px(.43), y0-3.2*vs-22)})

# 3) Einthoven
W, H = 600, 470
RA, LA, LL = (160, 90), (440, 90), (300, 400)
C = (300, 190)
b = [f'<path d="M{RA[0]},{RA[1]} L{LA[0]},{LA[1]} L{LL[0]},{LL[1]}Z" fill="#e8f1fb" stroke="none"/>']
b.append(arrow(RA[0]+20, RA[1]-18, LA[0]-20, LA[1]-18, '#d63384', 4))
b.append(arrow(RA[0]-14, RA[1]+28, LL[0]-22, LL[1]-2, MOR, 4))
b.append(arrow(LA[0]+14, LA[1]+28, LL[0]+22, LL[1]-2, '#7cb518', 4))
for (a, c) in ((RA, '#3aa0c8'), (LA, '#e0457b'), (LL, NAR)):
    b.append(arrow(C[0], C[1], a[0]+(C[0]-a[0])*.12, a[1]+(C[1]-a[1])*.12, c, 3.5))
b.append(f'<circle cx="{C[0]}" cy="{C[1]}" r="34" fill="{ROJO}" opacity=".9"/>' + T(C[0], C[1]+5, 'corazón', 13, '#fff', w='bold'))
for (p, lab, dx, dy, an) in ((RA, 'Brazo derecho', -20, 5, 'end'), (LA, 'Brazo izquierdo', 20, 5, 'start'), (LL, 'Pierna izquierda', 0, 42, 'middle')):
    b.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="11" fill="#333"/>')
    b.append(T(p[0]+dx, p[1]+dy, lab, 14, '#222', an, 'bold'))
# signos de polaridad de las bipolares
signs = [((RA[0]+14, RA[1]-30), '−'), ((LA[0]-14, LA[1]-30), '+'), ((RA[0]-30, RA[1]+40), '−'), ((LL[0]-38, LL[1]-10), '+'),
         ((LA[0]+30, LA[1]+40), '−'), ((LL[0]+38, LL[1]-10), '+')]
for (x, y), s in signs:
    col = '#2f9e44' if s == '+' else '#d6336c'
    b.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{col}"/>' + T(x, y+5, s, 16, '#fff', w='bold'))
svg('einthoven.svg', W, H, ''.join(b))
pe = lambda x, y: f'{100*x/W:.0f},{100*y/H:.0f}'
print('einthoven', {'DI': pe(300, 48), 'DII': pe(185, 255), 'DIII': pe(415, 255), 'aVR': pe(200, 125), 'aVL': pe(400, 125), 'aVF': pe(300, 330)})

# 4) Hexaxial
W, H = 600, 560; C = (300, 280); R = 200
b = [f'<circle cx="{C[0]}" cy="{C[1]}" r="{R}" fill="#f4f8f6" stroke="#ccd" stroke-width="1.5"/>']
# zona normal -30 a +90 (ángulos en sentido horario desde 0 = derecha)
def pt(deg, r): a = math.radians(deg); return (C[0]+r*math.cos(a), C[1]+r*math.sin(a))
a1, a2 = pt(-30, R), pt(90, R)
b.append(f'<path d="M{C[0]},{C[1]} L{a1[0]:.1f},{a1[1]:.1f} A{R},{R} 0 0 1 {a2[0]:.1f},{a2[1]:.1f}Z" fill="#c8ecc9" opacity=".8"/>')
for d in range(0, 360, 30):
    p = pt(d, R)
    b.append(f'<line x1="{C[0]}" y1="{C[1]}" x2="{p[0]:.1f}" y2="{p[1]:.1f}" stroke="#c3c9cf" stroke-width="1.2" stroke-dasharray="5 5"/>')
leads = {0: '#e0457b', 60: MOR, 120: '#7cb518', 90: NAR, -30: '#c2185b', -150: '#3aa0c8'}
for d, c in leads.items():
    p = pt(d, R-6); b.append(arrow(C[0], C[1], p[0], p[1], c, 4.5, 15))
for d in range(-150, 181, 30):
    p = pt(d, R+24); lab = '±180°' if d == 180 else (f'{d:+d}°' if d else '0°')
    b.append(T(p[0], p[1]+5, lab, 14, '#333', w='bold'))
b.append(f'<circle cx="{C[0]}" cy="{C[1]}" r="26" fill="{ROJO}"/>')
b.append(T(C[0]+95, C[1]+70, 'eje normal', 14, VERDE, w='bold'))
svg('hexaxial.svg', W, H, ''.join(b))
ph = lambda d, r=R-50: (lambda p: f'{100*p[0]/W:.0f},{100*p[1]/H:.0f}')(pt(d, r))
print('hexaxial', {'DI': ph(0, R-60), 'DII': ph(60), 'DIII': ph(120), 'aVF': ph(90), 'aVL': ph(-30), 'aVR': ph(-150)})

# 5) Eje: cuadrantes DI / aVF
W, H = 600, 520; C = (300, 260); R = 190
def sector(d1, d2, c):
    p1, p2 = pt(d1, R), pt(d2, R)
    large = 1 if (d2-d1) % 360 > 180 else 0
    return f'<path d="M{C[0]},{C[1]} L{p1[0]:.1f},{p1[1]:.1f} A{R},{R} 0 {large} 1 {p2[0]:.1f},{p2[1]:.1f}Z" fill="{c}" stroke="#fff" stroke-width="2"/>'
b = [sector(-30, 90, '#b8e986'), sector(90, 180, '#8fd8f0'), sector(180, 270, '#f7a8c8'), sector(270, 330, '#ffe27a')]
b.append(f'<line x1="{C[0]-R-20}" y1="{C[1]}" x2="{C[0]+R+20}" y2="{C[1]}" stroke="#223" stroke-width="2"/>')
b.append(f'<line x1="{C[0]}" y1="{C[1]-R-20}" x2="{C[0]}" y2="{C[1]+R+20}" stroke="#223" stroke-width="2"/>')
for d, lab in ((0, '0° (DI +)'), (180, '±180° (DI −)'), (90, '+90° (aVF +)'), (-90, '−90° (aVF −)'), (-30, '−30°')):
    p = pt(d, R+(60 if d in (0,180) else 30)); b.append(T(p[0], p[1]+5, lab, 14, '#222', w='bold'))
svg('eje.svg', W, H, ''.join(b))
pq = lambda d, r=R*.6: (lambda p: f'{100*p[0]/W:.0f},{100*p[1]/H:.0f}')(pt(d, r))
print('eje', {'normal': pq(30), 'derecha': pq(135), 'extrema': pq(225), 'izquierda': pq(300, R*.7)})

# 6) Precordiales: corte transversal (anterior arriba, izquierda del paciente a la derecha de la imagen)
W, H = 600, 470
b = [f'<ellipse cx="300" cy="240" rx="260" ry="175" fill="#fde4d6" stroke="#d9a58b" stroke-width="3"/>']
b.append('<ellipse cx="165" cy="250" rx="95" ry="120" fill="#f6c4dd"/><ellipse cx="440" cy="255" rx="95" ry="120" fill="#f6c4dd"/>')
b.append('<rect x="280" y="72" width="40" height="22" rx="6" fill="#efe3b4" stroke="#c9b77a"/>')  # esternón
b.append('<circle cx="300" cy="385" r="26" fill="#efe3b4" stroke="#c9b77a"/>')  # vértebra
b.append('<ellipse cx="315" cy="210" rx="92" ry="78" fill="#e86a5c"/>')
b.append('<ellipse cx="290" cy="170" rx="44" ry="28" fill="#c0392b"/>' + T(290, 175, 'VD', 14, '#fff', w='bold'))
b.append('<ellipse cx="350" cy="225" rx="46" ry="40" fill="#a93226"/>' + T(350, 230, 'VI', 14, '#fff', w='bold'))
b.append(T(300, 26, 'ANTERIOR', 13, GRIS, w='bold') + T(300, 440, 'POSTERIOR', 13, GRIS, w='bold'))
b.append(T(70, 245, 'Der.', 13, GRIS, w='bold') + T(535, 245, 'Izq.', 13, GRIS, w='bold'))
E = {'V1': (262, 82), 'V2': (338, 82), 'V3': (390, 92), 'V4': (440, 108), 'V5': (500, 148), 'V6': (548, 210)}
for k, (x, y) in E.items():
    b.append(arrow(x, y, 315+(x-315)*.45, 210+(y-210)*.45, '#2a7fb8', 2.5, 10))
    b.append(f'<circle cx="{x}" cy="{y}" r="12" fill="#8fe3f0" stroke="#1d6f8a" stroke-width="2"/>')
svg('precordiales.svg', W, H, ''.join(b))
print('precordiales', {k: f'{100*x/W:.0f},{100*(y-24)/H:.0f}' for k, (x, y) in E.items()})

# 7) Vectores: secuencia de activación
W, H = 600, 480
b = []
heart = 'M175,140 C150,140 120,170 125,215 C135,300 230,400 315,440 C400,395 480,300 485,215 C490,165 455,135 420,140 Z'
b.append(f'<path d="{heart}" fill="#fbe1dd" stroke="#c0392b" stroke-width="3"/>')
b.append('<path d="M150,140 C150,80 280,70 290,140 Z" fill="#fcd2cb" stroke="#c0392b" stroke-width="3"/>')
b.append('<path d="M320,140 C330,70 460,80 460,140 Z" fill="#fcd2cb" stroke="#c0392b" stroke-width="3"/>')
b.append('<path d="M300,150 C300,250 312,330 315,420" fill="none" stroke="#c0392b" stroke-width="10" stroke-linecap="round"/>')
b.append('<circle cx="190" cy="100" r="9" fill="#2f9e44"/>' + T(190, 82, 'nodo sinusal', 12, '#2f9e44', w='bold'))
b.append('<circle cx="300" cy="150" r="8" fill="#2f9e44"/>' + T(352, 160, 'nodo AV', 12, '#2f9e44', w='bold'))
b.append(arrow(185, 105, 255, 135, '#22a6c9', 6, 16))   # 1 aurículas: der→izq, arriba→abajo
b.append(arrow(330, 230, 270, 260, '#e1b000', 6, 16))   # 2 septo: izq→der
b.append(arrow(315, 250, 410, 360, '#7cb518', 7, 18))   # 3 paredes libres (punta del VI)
b.append(arrow(450, 300, 430, 175, '#e03131', 6, 16))   # 4 bases: abajo→arriba
b.append(arrow(190, 300, 210, 190, '#e03131', 6, 16))
b.append(arrow(260, 330, 380, 400, '#4263eb', 5, 14))   # 5 repolarización: misma dirección
svg('vectores.svg', W, H, ''.join(b))
pv = lambda x, y: f'{100*x/W:.0f},{100*y/H:.0f}'
print('vectores', {'1': pv(225, 112), '2': pv(300, 238), '3': pv(370, 300), '4': pv(452, 235), '5': pv(320, 380)})

# 8) Frecuencia: regla 300-150-100…
mm = 6; W = 620; H = 230
b = [grid(10, 20, 600, 180, mm)]
rr = 21  # mm entre R → ~71 lpm
x0 = 10+mm*5
def strip(t):
    tt = t % (rr/25)
    return beat(tt+.02) * .55
xs = []
pts = []
t = 0
while x0+t*25*mm < 600:
    pts.append(f'{x0+t*25*mm:.1f},{140-strip(t)*mm:.1f}'); t += .004
b.append(f'<path d="M10,140 L{x0},140 L' + ' L'.join(pts) + '" fill="none" stroke="#111" stroke-width="2"/>')
nums = [300, 150, 100, 75, 60, 50, 43, 37, 33, 30]
rx = x0+(.195-.02)*25*mm
for i, n in enumerate(nums, 1):
    x = rx+i*5*mm
    if x > 605: break
    b.append(f'<line x1="{x:.1f}" y1="34" x2="{x:.1f}" y2="196" stroke="{ROJO}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    b.append(T(x, 44, str(n), 12, ROJO, w='bold'))
b.append(f'<line x1="{rx:.1f}" y1="34" x2="{rx:.1f}" y2="196" stroke="{VERDE}" stroke-width="2.4"/>')
b.append(T(rx, 214, 'R sobre línea gruesa', 12, VERDE, w='bold'))
svg('frecuencia.svg', W, H, ''.join(b))
print('freq second R x', rx+rr*mm, 'between lines')
