"""Esquemas propios en español (SVG) para la guía de Imagenología. Reescribe tools-imagenologia/img/*.svg"""
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
FONT = "font-family='IBM Plex Sans,Helvetica,Arial,sans-serif'"

def svg(name, w, h, body):
    s = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}' {FONT}><rect width='{w}' height='{h}' fill='#ffffff'/>{body}</svg>"
    open(os.path.join(OUT, name + '.svg'), 'w').write(s)

def T(x, y, t, size=16, anchor='start', fill='#111a21', weight='400', extra=''):
    t = str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f"<text x='{x}' y='{y}' font-size='{size}' text-anchor='{anchor}' fill='{fill}' font-weight='{weight}' {extra}>{t}</text>"

def title(t, sub=''):
    return T(24, 38, t, 22, weight='700') + (T(24, 62, sub, 14, fill='#56656f') if sub else '')

# 1. Las 5 densidades radiológicas
items = [('#0b0b0b', 'Aire', 'Pulmón, gas intestinal', 'Radiolúcido'), ('#4a4a4a', 'Grasa', 'Tejido adiposo, planos grasos', ''),
         ('#8c8c8c', 'Agua / tejido blando', 'Músculo, sangre, vísceras', ''), ('#d6d6d6', 'Calcio / hueso', 'Huesos, calcificaciones', ''),
         ('#ffffff', 'Metal', 'Prótesis, contraste, proyectiles', 'Radiopaco')]
b = title('Las 5 densidades radiológicas', 'De más negro (deja pasar los rayos X) a más blanco (los absorbe)')
for i, (c, n, ej, ext) in enumerate(items):
    x = 24 + i * 172
    b += f"<rect x='{x}' y='86' width='160' height='120' rx='10' fill='{c}' stroke='#9aa7b0'/>"
    b += T(x + 80, 236, n, 16, 'middle', weight='700') + T(x + 80, 258, ej, 12, 'middle', '#56656f')
    if ext: b += T(x + 80, 152, ext, 15, 'middle', '#f0b03c' if i == 0 else '#9a5a00', '700')
b += "<defs><marker id='a' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='8' markerHeight='8' orient='auto'><path d='M0,0L10,5L0,10z' fill='#56656f'/></marker></defs>"
b += "<line x1='40' y1='290' x2='860' y2='290' stroke='#56656f' stroke-width='2' marker-end='url(#a)'/>" + T(450, 314, 'Mayor número atómico y densidad = más atenuación = más blanco', 14, 'middle', '#56656f')
svg('rx-5-densidades', 900, 330, b)

# 2. Escala Hounsfield y ventanas
vals = [(-1000, 'Aire −1000'), (-500, 'Pulmón −400 a −600'), (-75, 'Grasa −50 a −100'), (0, 'Agua 0'), (1000, 'Hueso +1000')]
def xs(v): return 60 + (v + 1000) / 4000 * 780
b = title('Escala de unidades Hounsfield (TC)', 'Cada vóxel recibe un número según cuánto atenúa respecto al agua')
b += "<defs><linearGradient id='g' x1='0' x2='1'><stop offset='0' stop-color='#000'/><stop offset='0.5' stop-color='#fff'/><stop offset='1' stop-color='#fff'/></linearGradient></defs>"
b += f"<rect x='60' y='90' width='780' height='46' fill='url(#g)' stroke='#9aa7b0'/>"
for v, n in vals:
    x = xs(v)
    b += f"<line x1='{x}' y1='84' x2='{x}' y2='150' stroke='#9a5a00' stroke-width='2'/>"
    yy = {-1000: 168, -500: 186, -75: 204, 0: 222, 1000: 168}[v]
    b += f"<line x1='{x}' y1='150' x2='{x}' y2='{yy-14}' stroke='#c9d1d7'/>" + T(x, yy, n, 13, 'middle', weight='600')
b += f"<line x1='{xs(3000)}' y1='84' x2='{xs(3000)}' y2='150' stroke='#9a5a00' stroke-width='2'/>" + T(xs(3000), 168, 'Metal hasta +3000', 13, 'middle', weight='600')
b += T(24, 256, 'Ventanas (centro y amplitud que se ven en gris)', 16, weight='700')
wins = [('Pulmón', -1400, -650, '#2f6b8e'), ('Tejidos blandos', -160, 240, '#16796f'), ('Hueso', -600, 1400, '#a5621a')]
for i, (n, a, z, c) in enumerate(wins):
    y = 272 + i * 34
    b += f"<rect x='{xs(max(a,-1000))}' y='{y}' width='{xs(z)-xs(max(a,-1000))}' height='22' rx='4' fill='{c}' opacity='.85'/>"
    b += T(xs(z) + 8, y + 16, f'{n}: {a} a {z}', 13, fill=c, weight='700')
b += T(24, 396, 'Fuera de la ventana todo se ve negro (por debajo) o blanco (por arriba). Hiperdenso / isodenso / hipodenso.', 13, fill='#56656f')
svg('tc-hounsfield', 900, 412, b)

# 3. Ecogenicidad y artefactos
b = title('Escala de grises en ecografía', 'Cómo se describe lo que se ve (modo B)')
eco = [('#f2f2f2', 'Hiperecoico', 'Blanco: hueso, fibrosis, grasa ecogénica'), ('#8a8a8a', 'Isoecoico', 'Igual que el tejido vecino'),
       ('#3a3a3a', 'Hipoecoico', 'Gris oscuro: tejido celular, rico en agua'), ('#000000', 'Anecoico', 'Negro: líquido (quiste, vesícula, vejiga)')]
for i, (c, n, d) in enumerate(eco):
    x = 24 + i * 214
    b += f"<rect x='{x}' y='84' width='200' height='70' rx='8' fill='{c}' stroke='#9aa7b0'/>" + T(x + 100, 178, n, 15, 'middle', weight='700') + T(x + 100, 198, d, 11, 'middle', '#56656f')
# artefactos
b += T(24, 240, 'Artefactos útiles', 16, weight='700')
# lito con sombra
b += "<rect x='40' y='256' width='250' height='170' fill='#3d3d3d'/><ellipse cx='165' cy='300' rx='40' ry='22' fill='#f5f5f5'/><rect x='125' y='300' width='80' height='126' fill='#050505'/>"
b += T(165, 446, 'Sombra acústica posterior', 14, 'middle', weight='700') + T(165, 464, 'Lito, hueso, costilla', 12, 'middle', '#56656f')
# quiste con refuerzo
b += "<rect x='325' y='256' width='250' height='170' fill='#3d3d3d'/><rect x='410' y='300' width='80' height='126' fill='#8e8e8e'/><ellipse cx='450' cy='300' rx='42' ry='30' fill='#000'/>"
b += T(450, 446, 'Refuerzo acústico posterior', 14, 'middle', weight='700') + T(450, 464, 'Detrás de líquido (quiste)', 12, 'middle', '#56656f')
# reverberación
b += "<rect x='610' y='256' width='250' height='170' fill='#3d3d3d'/>" + ''.join(f"<line x1='625' x2='845' y1='{280+i*30}' y2='{280+i*30}' stroke='#e6e6e6' stroke-width='{4-i*0.6:.1f}' opacity='{1-i*0.17:.2f}'/>" for i in range(5))
b += T(735, 446, 'Reverberación', 14, 'middle', weight='700') + T(735, 464, 'Líneas repetidas (pleura de pulmón sano)', 12, 'middle', '#56656f')
svg('eco-ecogenicidad', 900, 480, b)

# 4. Transductores
b = title('Transductores y su frecuencia', 'Más frecuencia = más resolución pero menos penetración')
tr = [('Lineal', '5–10 MHz', '~9 cm', 'Superficial, vasos, mama', "M60,120 h120 v30 h-120z", "M60,150 h120 v120 h-120z"),
      ('Convexo', '2–5 MHz', '~30 cm', 'Abdomen, obstetricia', "M60,150 q60,-40 120,0 v-30 h-120z", "M60,150 q60,-40 120,0 L230,290 L10,290z"),
      ('Sectorial', '1–5 MHz', '~35 cm', 'Corazón (entre costillas)', "M100,120 h40 v30 h-40z", "M120,150 L210,300 L30,300z"),
      ('Intracavitario', '5–8 MHz', '~13 cm', 'Útero y ovarios', "M110,90 h20 v60 h-20z", "M120,150 q-60,10 -50,70 L120,240 L170,220 q10,-60 -50,-70z")]
for i, (n, f, p, u, prob, beam) in enumerate(tr):
    g = f"<g transform='translate({20+i*220},0)'><path d='{beam}' fill='#f0b03c' opacity='.28'/><path d='{prob}' fill='#2f6b8e'/>"
    g += T(120, 330, n, 16, 'middle', weight='700') + T(120, 352, f + ' · ' + p, 13, 'middle', '#9a5a00', '700') + T(120, 372, u, 12, 'middle', '#56656f') + '</g>'
    b += g
svg('eco-transductores', 900, 390, b)

# 5. Doppler
b = title('Doppler: dirección del flujo', 'Los eritrocitos reflejan el sonido y cambian su frecuencia')
b += "<defs><marker id='r' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto'><path d='M0,0L10,5L0,10z' fill='#c0392b'/></marker><marker id='bl' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto'><path d='M0,0L10,5L0,10z' fill='#1f5fbf'/></marker></defs>"
for k, (cx, col, mk, lab, sub, dirx) in enumerate([(230, '#c0392b', 'r', 'ROJO: se acerca', 'al transductor (frecuencia sube)', -1), (670, '#1f5fbf', 'bl', 'AZUL: se aleja', 'del transductor (frecuencia baja)', 1)]):
    b += f"<rect x='{cx-50}' y='84' width='100' height='34' rx='6' fill='#2f6b8e'/>" + T(cx, 106, 'Transductor', 13, 'middle', '#fff', '600')
    b += f"<path d='M{cx-30},118 L{cx-120},300 L{cx+120},300 L{cx+30},118z' fill='#f0b03c' opacity='.15'/>"
    b += f"<rect x='{cx-190}' y='210' width='380' height='46' rx='23' fill='{col}' opacity='.85'/>"
    x1, x2 = (cx + 140, cx - 140) if dirx < 0 else (cx - 140, cx + 140)
    b += f"<line x1='{x1}' y1='196' x2='{x2}' y2='{196 - 40*(-1)}' stroke='{col}' stroke-width='3' marker-end='url(#{mk})' opacity='0'/>"
    # flecha de flujo dentro del vaso, inclinada hacia/lejos del transductor
    b += f"<line x1='{cx-120}' y1='233' x2='{cx+120}' y2='233' stroke='#fff' stroke-width='4' marker-end='url(#{mk})'/>" if False else ''
    ys, ye = (262, 160) if dirx < 0 else (160, 262)
    b += f"<line x1='{cx-60}' y1='{ys}' x2='{cx+60}' y2='{ye}' stroke='{col}' stroke-width='5' marker-end='url(#{mk})'/>"
    b += T(cx, 330, lab, 17, 'middle', col, '700') + T(cx, 352, sub, 13, 'middle', '#56656f')
b += T(450, 392, 'Color: rojo se acerca, azul se aleja; más brillante = más velocidad.  Power: más sensible, sin dirección ni aliasing.', 13, 'middle', '#111a21')
b += T(450, 414, 'Espectral: curva de velocidad contra tiempo (sístole y diástole).', 13, 'middle', '#56656f')
svg('doppler-color', 900, 430, b)

# 6. RM: T1 vs T2
b = title('Cómo se ve cada tejido en T1 y T2', 'T1 = anatomía · T2 = patología (el agua brilla)')
rows = [('Agua / LCR / edema', '#1a1a1a', '#f4f4f4'), ('Grasa', '#f4f4f4', '#d0d0d0'), ('Sustancia blanca', '#d8d8d8', '#5a5a5a'),
        ('Sustancia gris', '#8a8a8a', '#9a9a9a'), ('Hueso cortical / aire', '#050505', '#050505'), ('Gadolinio (T1 + C)', '#ffffff', '—')]
b += T(330, 100, 'T1', 18, 'middle', weight='700') + T(470, 100, 'T2', 18, 'middle', weight='700') + T(560, 100, 'Regla', 15, weight='700')
notes = ['Oscuro en T1, brillante en T2', 'Brillante en ambas (STIR la anula)', 'Más clara que la gris en T1', 'Más oscura que la blanca en T1', 'Sin señal: negro en ambas', 'Realce = hiperintenso en T1']
for i, (n, c1, c2) in enumerate(rows):
    y = 116 + i * 46
    b += T(24, y + 26, n, 14, weight='600')
    b += f"<rect x='280' y='{y}' width='100' height='36' rx='6' fill='{c1}' stroke='#9aa7b0'/>"
    b += (f"<rect x='420' y='{y}' width='100' height='36' rx='6' fill='{c2}' stroke='#9aa7b0'/>" if c2 != '—' else T(470, y + 24, '—', 16, 'middle'))
    b += T(560, y + 24, notes[i], 13, fill='#56656f')
b += T(24, 410, 'FLAIR = T2 que anula el LCR (el edema sigue brillante).  DWI: la restricción a la difusión brilla (isquemia aguda).', 13, fill='#111a21')
svg('rm-t1-t2', 900, 426, b)

# 7. Fases del contraste en TC
b = title('Fases de la TC con contraste yodado IV', 'Tiempos aproximados desde la inyección')
ph = [('Simple', 'sin contraste', 'Calcio, sangre aguda, litos', '#8c8c8c'), ('Arterial', '~25–35 s', 'Aorta y arterias brillantes; lesiones hipervasculares', '#c0392b'),
      ('Portal / venosa', '~60–70 s', 'Parénquima hepático y venas; la más usada en abdomen', '#2f6b8e'), ('Tardía / excretora', '3–10 min', 'Contraste en vías urinarias; lavado de lesiones', '#a5621a')]
for i, (n, t, d, c) in enumerate(ph):
    x = 24 + i * 216
    b += f"<rect x='{x}' y='84' width='204' height='12' rx='6' fill='{c}'/>"
    b += T(x, 124, n, 16, weight='700', fill=c) + T(x, 146, t, 14, weight='600') + ''.join(T(x, 170 + j * 17, ln, 12, fill='#56656f') for j, ln in enumerate(d.split('; ')))
b += T(24, 250, 'Yodados: RX y TC (eliminación renal, pedir creatinina).  Gadolinio: solo RM.  Bario: tubo digestivo (no si hay perforación).', 13)
svg('contraste-fases', 900, 270, b)

# 8. HSA esquema + Fisher
b = title('Hemorragia subaracnoidea en TC simple', 'Esquema: sangre hiperdensa en cisternas basales (polígono de Willis)')
b += "<g transform='translate(40,80)'><ellipse cx='160' cy='170' rx='150' ry='165' fill='#1a1a1a'/><ellipse cx='160' cy='170' rx='138' ry='153' fill='#7d7d7d'/>"
b += "<path d='M160,120 L178,160 L225,150 L190,182 L215,230 L160,205 L105,230 L130,182 L95,150 L142,160z' fill='#f2f2f2'/>"
b += "<path d='M190,182 Q240,170 268,150' stroke='#f2f2f2' stroke-width='7' fill='none'/><path d='M130,182 Q80,170 52,150' stroke='#f2f2f2' stroke-width='7' fill='none'/>"
b += "<ellipse cx='160' cy='250' rx='26' ry='20' fill='#5e5e5e'/><path d='M120,290 q40,30 80,0' stroke='#5e5e5e' stroke-width='8' fill='none'/>"
b += T(160, 360, 'Estrella hiperdensa + cisuras de Silvio', 13, 'middle', weight='600') + '</g>'
b += T(400, 110, 'Escala de Fisher (tomográfica)', 16, weight='700')
fis = [('1', 'Sin sangre visible'), ('2', 'Capa difusa < 1 mm'), ('3', 'Coágulo cisternal > 1 mm'), ('4', 'Hematoma parenquimatoso o hemorragia intraventricular')]
for i, (g, d) in enumerate(fis):
    y = 130 + i * 52
    b += f"<rect x='400' y='{y}' width='42' height='38' rx='8' fill='#ad3f5c'/>" + T(421, y + 26, g, 18, 'middle', '#fff', '700') + T(456, y + 25, d, 14)
b += T(400, 360, 'Causa espontánea más común: aneurisma sacular roto (85%).', 13, fill='#56656f')
b += T(400, 380, 'La sensibilidad de la TC baja con el tiempo y con poca sangre.', 13, fill='#56656f')
svg('hsa-esquema-fisher', 900, 450, b)

# 9. Edema citotóxico vs vasogénico
def brain(cx, kind):
    g = f"<g transform='translate({cx},90)'><ellipse cx='150' cy='150' rx='140' ry='150' fill='#202020'/><ellipse cx='150' cy='150' rx='130' ry='140' fill='#6e6e6e'/><ellipse cx='150' cy='150' rx='100' ry='110' fill='#9a9a9a'/>"
    g += "<path d='M150,40 v220' stroke='#202020' stroke-width='4'/>"
    if kind == 'c':
        g += "<path d='M150,60 A100,110 0 0,0 52,170 L150,170z' fill='#4a4a4a'/><path d='M150,40 A130,140 0 0,0 20,150 L52,170 A100,110 0 0,1 150,60z' fill='#4a4a4a'/>"
    else:
        g += "<circle cx='95' cy='130' r='16' fill='#dcdcdc' stroke='#fff' stroke-width='3'/>"
        for a, d in [(-60, 'M95,130 q-10,-40 -5,-55'), (0, 'M95,130 q-35,-5 -45,10'), (0, 'M95,130 q-30,25 -35,45'), (0, 'M95,130 q15,40 5,60'), (0, 'M95,130 q35,10 30,35')]:
            g += f"<path d='{d}' stroke='#4a4a4a' stroke-width='16' fill='none' stroke-linecap='round'/>"
        g += "<circle cx='95' cy='130' r='16' fill='#dcdcdc' stroke='#fff' stroke-width='3'/>"
    return g + '</g>'
b = title('Edema cerebral en TC: citotóxico vs vasogénico', 'Esquemas axiales (gris = corteza, gris claro = sustancia blanca, oscuro = edema)')
b += brain(40, 'c') + brain(480, 'v')
b += T(190, 410, 'Citotóxico (isquemia)', 16, 'middle', '#2f6b8e', '700') + T(190, 432, 'Se pierde la diferenciación gris-blanca', 13, 'middle') + T(190, 452, 'Afecta corteza y sustancia blanca · DWI restringe', 13, 'middle', '#56656f')
b += T(630, 410, 'Vasogénico (tumor, absceso)', 16, 'middle', '#ad3f5c', '700') + T(630, 432, 'Dedos en sustancia blanca, respeta la corteza', 13, 'middle') + T(630, 452, 'Se conserva gris-blanca · DWI no restringe', 13, 'middle', '#56656f')
svg('edema-tipos', 900, 470, b)

# 10. Intra vs extraaxial
b = title('¿Intraaxial o extraaxial?', 'Signos que dicen que la lesión está fuera del cerebro')
b += "<g transform='translate(40,80)'><path d='M0,40 Q200,-10 400,40' stroke='#a5621a' stroke-width='14' fill='none'/>"  # hueso
b += "<path d='M0,58 Q200,8 400,58' stroke='#7a4ea3' stroke-width='4' fill='none'/>"  # duramadre
b += "<path d='M0,64 Q200,14 400,64 L400,330 L0,330z' fill='#bdbdbd'/>"  # cerebro
b += "<path d='M0,64 Q200,14 400,64 L400,100 Q200,50 0,100z' fill='#8a8a8a'/>"  # corteza
b += "<path d='M120,40 Q200,20 280,40 Q290,120 200,150 Q110,120 120,40z' fill='#f0b03c' stroke='#9a5a00' stroke-width='2'/>"
b += "<path d='M118,46 Q200,150 282,46' stroke='#111' stroke-width='5' fill='none' stroke-dasharray='2 6' opacity='0'/>"
b += "<path d='M112,60 Q200,175 288,60' stroke='#1a1a1a' stroke-width='6' fill='none'/>"  # hendidura LCR
b += "<path d='M95,52 Q60,48 30,54' stroke='#7a4ea3' stroke-width='9' fill='none'/><path d='M305,52 Q340,48 370,54' stroke='#7a4ea3' stroke-width='9' fill='none'/>"  # cola dural
b += "<path d='M115,72 Q200,190 285,72' stroke='#8a8a8a' stroke-width='10' fill='none'/></g>"
lab = [('Base dural amplia y cola dural', 120), ('Hendidura de LCR entre masa y cerebro', 150), ('Sustancia gris entre la masa y la blanca', 180),
       ('Vasos subaracnoideos desplazados', 210), ('Espacio subaracnoideo ensanchado', 240), ('Reacción del hueso (hiperostosis)', 270)]
for t, y in lab:
    b += f"<circle cx='500' cy='{y-5}' r='5' fill='#7a4ea3'/>" + T(514, y, t, 14)
b += T(500, 320, 'Ejemplo típico: meningioma (después de los 40).', 13, fill='#56656f')
b += T(500, 340, 'Intraaxial en adulto: metástasis y gliomas.', 13, fill='#56656f')
b += T(240, 440, 'Esquema: masa extraaxial (naranja) empujando la corteza', 13, 'middle', '#56656f')
svg('snc-extraaxial', 900, 460, b)

# 11. BI-RADS
b = title('Categorías BI-RADS', 'Mastografía, ecografía y RM de mama')
bi = [('0', 'Incompleto', 'Faltan proyecciones o estudios', '#8c8c8c'), ('1', 'Negativo', 'Tamizaje de rutina', '#1b7a49'), ('2', 'Benigno', 'Tamizaje de rutina', '#1b7a49'),
      ('3', 'Probablemente benigno', 'Malignidad ≤ 2% · control corto (≈6 meses)', '#a5621a'), ('4', 'Sospechoso', 'Malignidad > 2 a < 95% (4A, 4B, 4C) · biopsia', '#c0392b'),
      ('5', 'Altamente sugestivo', 'Malignidad ≥ 95% · biopsia', '#8b1a1a'), ('6', 'Malignidad comprobada', 'Ya tiene biopsia: tratamiento', '#4a148c')]
for i, (n, d, c, col) in enumerate(bi):
    y = 80 + i * 48
    b += f"<rect x='24' y='{y}' width='46' height='40' rx='8' fill='{col}'/>" + T(47, y + 28, n, 20, 'middle', '#fff', '700')
    b += T(86, y + 18, d, 15, weight='700') + T(86, y + 36, c, 13, fill='#56656f')
b += T(24, 430, '† Rangos de malignidad del ACR BI-RADS (5ª ed.).', 12, fill='#56656f')
svg('mama-birads', 620, 444, b)

# 12. Proyecciones mamográficas
b = title('Proyecciones de mastografía', 'Se colocan en espejo (derecha e izquierda)')
for k, (x, n, d) in enumerate([(60, 'Craneocaudal (CC)', 'Compresión de arriba abajo'), (480, 'Mediolateral oblicua (MLO)', 'Incluye el pectoral y la axila')]):
    g = f"<g transform='translate({x},80)'>"
    if k == 0:
        g += "<path d='M40,40 h220 v40 q-110,170 -220,0z' fill='#d9d9d9' stroke='#9aa7b0'/><path d='M60,70 q90,120 180,0' fill='#9e9e9e' opacity='.6'/><circle cx='150' cy='200' r='7' fill='#555'/>"
    else:
        g += "<path d='M40,30 L120,30 Q260,140 200,240 Q120,300 40,240z' fill='#d9d9d9' stroke='#9aa7b0'/><path d='M40,30 L120,30 L40,150z' fill='#7a7a7a'/><path d='M70,120 q90,60 90,110' stroke='#9e9e9e' stroke-width='40' fill='none' opacity='.6'/>"
        g += T(52, 60, 'Pectoral', 12, fill='#fff', weight='600')
    g += T(150, 300, n, 16, 'middle', weight='700') + T(150, 322, d, 13, 'middle', '#56656f') + '</g>'
    b += g
b += T(450, 430, 'Blanco = tejido glandular · oscuro = grasa · líneas = tejido conectivo · ganglios con centro graso', 13, 'middle')
svg('mama-proyecciones', 900, 450, b)

# 13. Línea del tiempo
ev = [(1895, 'Röntgen descubre los rayos X (8 nov)'), (1900, 'Edison: fluoroscopia'), (1946, 'Purcell: resonancia magnética nuclear'),
      (1962, 'Holmes, Wright y Howry: transductor manual'), (1971, 'Hounsfield: prototipo de TC'), (1973, 'Lauterbur: primeras imágenes de RM'),
      (1980, 'Fujifilm: placas de fósforo (digital)'), (2003, 'Nobel a Lauterbur y Mansfield')]
b = title('Línea del tiempo de la imagenología')
b += "<line x1='120' y1='78' x2='120' y2='%d' stroke='#9aa7b0' stroke-width='3'/>" % (70 + len(ev) * 40)
for i, (y, t) in enumerate(ev):
    yy = 96 + i * 40
    b += f"<circle cx='120' cy='{yy-5}' r='7' fill='#9a5a00'/>" + T(100, yy, str(y), 16, 'end', '#9a5a00', '700') + T(140, yy, t, 15)
svg('historia-linea', 620, 90 + len(ev) * 40, b)
print('ok')
