"""Esquemas propios en español para la guía de Gastroenterología (5º).
Devuelve SVG en línea con las clases de la guía (fx-ink, fx-mut, fx-arr…) para que respeten el modo oscuro.
Uso: from esquemas import ESQ  ->  {nombre: (svg, aria)}
"""
from html import escape

C = dict(v='#1E6A4E', n='#D9822B', r='#B3261E', a='#2F6FB3', m='#7A849A', o='#B97A00', p='#8E4FB0', t='#13807D')
_n = [0]


class F:
    def __init__(self, h, label, maxw=580):
        _n[0] += 1
        self.id = f'gx{_n[0]}'
        self.h, self.label, self.maxw, self.p = h, label, maxw, []

    def t(self, x, y, s, fs=11, cls='fx-ink', anchor='middle', bold=False, lh=None):
        lines = s.split('\n')
        lh = lh or fs * 1.22
        y0 = y - (len(lines) - 1) * lh / 2
        sp = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else round(lh, 2)}">{escape(l)}</tspan>' for i, l in enumerate(lines))
        fw = ' font-weight="700"' if bold else ''
        self.p.append(f'<text x="{x}" y="{round(y0, 2)}" font-size="{fs}" text-anchor="{anchor}" class="{cls}"'
                      f'{fw} dominant-baseline="middle">{sp}</text>')

    def box(self, x, y, w, h, col, s='', fs=11, bold=False, op=.13, rx=9, tx=None):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" style="fill:{col};fill-opacity:{op};stroke:{col};stroke-width:1.5"/>')
        if s:
            self.t(tx if tx is not None else x + w / 2, y + h / 2, s, fs, bold=bold, anchor='middle' if tx is None else 'start')

    def raw(self, s):
        self.p.append(s)

    def arr(self, x1, y1, x2, y2):
        self.p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="fx-arr" marker-end="url(#{self.id})"/>')

    def svg(self):
        d = (f'<defs><marker id="{self.id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
             f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="fx-arrhead"/></marker></defs>')
        return (f'<svg viewBox="0 0 400 {self.h}" role="img" aria-label="{escape(self.label)}" class="fx" '
                f'style="max-width:{self.maxw}px">{d}{"".join(self.p)}</svg>')


ESQ = {}


def reg(name, f):
    ESQ[name] = (f.svg(), f.label)


# 1. Barrera antirreflujo y hernia hiatal
f = F(306, 'Barrera antirreflujo y tipos de hernia hiatal')
f.t(200, 12, 'La barrera antirreflujo de la unión esofagogástrica', 12, bold=True)
for i, (a, b) in enumerate([('EEI', 'tono basal; falla\ncon relajaciones\ntransitorias'),
                            ('Pilares del\ndiafragma', 'abrazan el EEI\ny lo refuerzan\nal inspirar'),
                            ('Ángulo de His', 'válvula entre el\nesófago y el fondo'),
                            ('Ligamento\nfrenoesofágico', 'mantiene la UEG\ndebajo del diafragma')]):
    x = 6 + i * 98
    f.box(x, 26, 92, 34, C['v'], a, 10.5, True)
    f.t(x + 46, 80, b, 8.4, 'fx-mut')
f.t(200, 116, 'Hernia hiatal: la UEG sube al tórax, se separa del diafragma → más reflujo', 9.5, 'fx-mut')
f.t(200, 140, 'Tipos de hernia hiatal †', 12, bold=True)
for i, (a, b, c) in enumerate([('Tipo I', 'Deslizamiento', 'La UEG sube; la más\ncomún (~95 %)'),
                               ('Tipo II', 'Paraesofágica', 'El fondo sube junto a\nla UEG, que no se mueve'),
                               ('Tipo III', 'Mixta', 'Sube la UEG y\ntambién el fondo'),
                               ('Tipo IV', 'Compleja', 'Además otro órgano:\ncolon, bazo, epiplón')]):
    x = 6 + i * 98
    col = C['n'] if i else C['a']
    f.box(x, 154, 92, 44, col, a + '\n' + b, 10.5, True)
    f.t(x + 46, 222, c, 8.4, 'fx-mut')
f.box(6, 256, 388, 42, C['r'], 'II–IV: riesgo de vólvulo, encarcelamiento y sangrado;\nse operan si dan síntomas. La tipo I se trata como ERGE.', 10.5, op=.1)
reg('erge-barrera', f)

# 2. Acalasia: Chicago 4.0
f = F(316, 'Topografía de presión esofágica en los tres tipos de acalasia (Chicago 4.0)')
f.t(200, 12, 'Así se ve la deglución en la manometría de alta resolución', 12, bold=True)
tit = [('Tipo I (clásica)', 'Cuerpo sin presión:\n100 % fallidas', 'Responde bien a\nPOEM, Heller o dilatación'),
       ('Tipo II', 'Presurización\npanesofágica ≥20 %', 'El que mejor responde\na cualquier tratamiento'),
       ('Tipo III (espástica)', 'Contracciones prematuras\n≥20 % (LD <4.5 s)', 'Responde peor; preferir\nPOEM (miotomía larga)')]
for i, (a, b, c) in enumerate(tit):
    x = 8 + i * 130
    f.t(x + 60, 32, a, 11, bold=True)
    f.raw(f'<rect x="{x}" y="44" width="120" height="150" rx="6" class="fx-row"/>')
    f.t(x + 4, 52, 'EES', 8, 'fx-mut', 'start')
    f.raw(f'<rect x="{x+4}" y="58" width="112" height="10" rx="3" style="fill:{C["r"]};fill-opacity:.55"/>')
    f.raw(f'<rect x="{x+20}" y="58" width="22" height="10" style="fill:{C["a"]};fill-opacity:.5"/>')  # EES se relaja
    if i == 1:
        f.raw(f'<rect x="{x+30}" y="72" width="70" height="98" rx="4" style="fill:{C["o"]};fill-opacity:.45"/>')
    if i == 2:
        f.raw(f'<path d="M{x+34} 74 L{x+56} 74 L{x+76} 166 L{x+54} 166 Z" style="fill:{C["r"]};fill-opacity:.55"/>')
    f.raw(f'<rect x="{x+4}" y="172" width="112" height="14" rx="3" style="fill:{C["r"]};fill-opacity:.75"/>')
    f.t(x + 60, 179, 'EEI no se relaja (IRP alta)', 8, 'fx-ink')
    f.t(x + 60, 222, b, 9.5)
    f.t(x + 60, 262, c, 9.5, 'fx-mut')
f.arr(8, 288, 120, 288)
f.t(200, 304, 'tiempo →   ·   arriba EES, abajo EEI   ·   color = presión', 9.5, 'fx-mut')
reg('acalasia-chicago', f)

# 3. Barrett: Praga y secuencia
f = F(306, 'Clasificación de Praga y secuencia metaplasia-displasia-adenocarcinoma')
f.t(100, 12, 'Clasificación de Praga (C y M)', 12, bold=True)
f.raw('<rect x="60" y="28" width="80" height="200" rx="8" style="fill:#E9A9A0;fill-opacity:.25;stroke:#B07A72;stroke-width:1.2"/>')
f.raw('<rect x="60" y="150" width="80" height="78" style="fill:#E07A4A;fill-opacity:.55"/>')
f.raw('<path d="M84 150 L84 96 Q92 88 100 96 L100 150 Z" style="fill:#E07A4A;fill-opacity:.55"/>')
f.raw('<line x1="52" y1="228" x2="148" y2="228" style="stroke:var(--ink);stroke-width:1.6"/>')
f.t(100, 240, 'UEG (inicio de los pliegues gástricos)', 9, 'fx-mut')
f.raw('<line x1="38" y1="150" x2="38" y2="228" class="fx-arr"/><line x1="160" y1="92" x2="160" y2="228" class="fx-arr"/>')
f.t(30, 189, 'C', 13, bold=True)
f.t(170, 160, 'M', 13, bold=True, anchor='start')
f.t(100, 274, 'C = extensión circunferencial\nM = extensión máxima (lengüeta)\nEjemplo: C2M5 · ≥3 cm = segmento largo', 9.5, 'fx-mut')
f.t(300, 12, 'Secuencia', 12, bold=True)
steps = [('Epitelio escamoso', C['m']), ('ERGE crónica', C['n']), ('Metaplasia intestinal\n(células caliciformes)', C['o']),
         ('Displasia de bajo grado', C['n']), ('Displasia de alto grado', C['r']), ('Adenocarcinoma', C['r'])]
for i, (s, col) in enumerate(steps):
    y = 28 + i * 44
    f.box(222, y, 156, 32, col, s, 10, i in (2, 5))
    if i < 5:
        f.arr(300, y + 32, 300, y + 43)
reg('barrett-praga', f)

# 4. Forrest
f = F(296, 'Clasificación de Forrest con riesgo de resangrado y conducta')
f.t(200, 12, 'Clasificación de Forrest de la úlcera que sangró', 12, bold=True)
f.t(56, 34, 'Forrest', 10, 'fx-mut', bold=True)
f.t(160, 34, 'Hallazgo', 10, 'fx-mut', bold=True)
f.t(270, 34, 'Resangrado sin\ntratamiento †', 9.5, 'fx-mut', bold=True)
f.t(355, 34, 'Endoterapia', 10, 'fx-mut', bold=True)
rows = [('Ia', 'Sangrado en chorro', '≈ 55–90 %', 'Sí', C['r']), ('Ib', 'Sangrado en capa', '≈ 55 %', 'Sí', C['r']),
        ('IIa', 'Vaso visible', '≈ 43 %', 'Sí', C['r']), ('IIb', 'Coágulo adherido', '≈ 22 %', 'Valorar', C['n']),
        ('IIc', 'Mancha pigmentada', '≈ 10 %', 'No', C['v']), ('III', 'Base limpia (fibrina)', '≈ 5 %', 'No', C['v'])]
for i, (a, b, c, d, col) in enumerate(rows):
    y = 52 + i * 38
    f.box(8, y, 384, 32, col, op=.1)
    f.t(56, y + 16, a, 13, bold=True)
    f.t(160, y + 16, b, 10.5)
    f.t(270, y + 16, c, 10.5)
    f.t(355, y + 16, d, 10.5, bold=d == 'Sí')
f.t(200, 286, 'Ia–IIa: terapia endoscópica combinada (nunca epinefrina sola) + IBP en dosis alta', 9.5, 'fx-mut')
reg('stda-forrest', f)

# 5. Gastroparesia: curva de retención
f = F(290, 'Gammagrafía de vaciamiento gástrico: retención a 1, 2 y 4 horas')
f.t(200, 12, 'Gammagrafía de 4 h con comida sólida', 12, bold=True)
X0, Y0, W, H = 46, 36, 286, 196
f.raw(f'<line x1="{X0}" y1="{Y0+H}" x2="{X0+W}" y2="{Y0+H}" class="fx-axis"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y0+H}" class="fx-axis"/>')
for v in (0, 25, 50, 75, 100):
    y = Y0 + H - v * H / 100
    f.raw(f'<line x1="{X0}" y1="{y}" x2="{X0+W}" y2="{y}" class="fx-grid"/>')
    f.t(X0 - 6, y, f'{v}', 9, 'fx-mut', 'end')
for hh in (0, 1, 2, 3, 4):
    f.t(X0 + hh * W / 4, Y0 + H + 12, f'{hh} h', 9, 'fx-mut')
f.t(X0 + 4, Y0 - 8, '% retenido', 9, 'fx-mut', 'start')
px = lambda hh, v: (round(X0 + hh * W / 4, 1), round(Y0 + H - v * H / 100, 1))
# bandas de gravedad a 4 h
for lo, hi, col, s in ((10, 15, C['o'], 'leve'), (15, 35, C['n'], 'moderada'), (35, 100, C['r'], 'grave')):
    x, y1 = px(4, hi)
    _, y2 = px(4, lo)
    f.raw(f'<rect x="{x-8}" y="{y1}" width="16" height="{y2-y1}" style="fill:{col};fill-opacity:.35"/>')
    f.t(x + 12, (y1 + y2) / 2, s, 8.5, 'fx-ink', 'start')
nl = [px(*p) for p in ((0, 100), (1, 75), (2, 40), (3, 15), (4, 5))]
gp = [px(*p) for p in ((0, 100), (1, 95), (2, 80), (3, 60), (4, 42))]
f.raw('<polyline points="' + ' '.join(f'{a},{b}' for a, b in nl) + f'" style="fill:none;stroke:{C["v"]};stroke-width:2.4"/>')
f.raw('<polyline points="' + ' '.join(f'{a},{b}' for a, b in gp) + f'" style="fill:none;stroke:{C["r"]};stroke-width:2.4;stroke-dasharray:6 4"/>')
for hh, v in ((1, 90), (2, 60), (4, 10)):
    x, y = px(hh, v)
    f.raw(f'<circle cx="{x}" cy="{y}" r="4" style="fill:var(--surface);stroke:var(--ink);stroke-width:1.5"/>')
    if hh == 4:
        f.t(x - 12, y - 4, f'>{v} %', 9, 'fx-ink', 'end', True)
    else:
        f.t(x + 6, y - 9, f'>{v} %', 9, 'fx-ink', 'start', True)
f.t(200, 260, 'Verde: vaciamiento normal · Rojo punteado: gastroparesia grave (ejemplo)', 9.5, 'fx-mut')
f.t(200, 276, 'Puntos = límites de anormalidad †; la retención >10 % a 4 h es la que define', 9.5, 'fx-mut')
reg('gastroparesia-curva', f)

# 6. H. pylori: pruebas
f = F(286, 'Pruebas para H. pylori y cuándo usarlas')
f.t(200, 12, 'Pruebas para infección activa por H. pylori', 12, bold=True)
f.box(6, 26, 190, 26, C['v'], 'No invasivas', 11, True)
f.box(204, 26, 190, 26, C['a'], 'Invasivas (endoscopía)', 11, True)
L = ['Aliento con urea ¹³C\nestándar no invasivo', 'Antígeno en heces\nmonoclonal', 'Serología: NO distingue\ninfección activa de pasada']
R = ['Histología (Sydney)\nestándar invasivo', 'Prueba rápida de ureasa', 'Cultivo y PCR:\nresistencia a antibióticos']
for i in range(3):
    f.box(6, 60 + i * 44, 190, 38, C['m'] if i == 2 else C['v'], L[i], 10, op=.08)
    f.box(204, 60 + i * 44, 190, 38, C['a'], R[i], 10, op=.08)
f.box(6, 200, 388, 34, C['n'], 'Antes de cualquier prueba (salvo serología): suspender IBP 14 días\ny antibióticos o bismuto 4 semanas †', 10, op=.12)
f.box(6, 242, 388, 34, C['r'], 'Confirmar la erradicación ≥4 semanas después del tratamiento\ncon aliento o antígeno fecal (nunca con serología)', 10, op=.1)
reg('hpylori-pruebas', f)

# 7. Celiaquía: Marsh-Oberhuber
f = F(276, 'Clasificación de Marsh-Oberhuber de la biopsia duodenal')
f.t(200, 12, 'Clasificación de Marsh-Oberhuber †', 12, bold=True)
spec = [('0', 'Normal', 80, 28, 1), ('1', 'Infiltrativa', 80, 28, 5), ('2', 'Hiperplásica', 80, 46, 5),
        ('3a', 'Atrofia\nparcial', 48, 50, 6), ('3b', 'Atrofia\nsubtotal', 22, 56, 7), ('3c', 'Atrofia\ntotal', 2, 62, 7)]
base = 150
for i, (k, s, vh, cd, iel) in enumerate(spec):
    x = 8 + i * 65
    f.raw(f'<rect x="{x}" y="{base}" width="58" height="{cd+10}" class="fx-tissue"/>')
    for j in range(2):
        vx = x + 6 + j * 26
        if vh > 4:
            f.raw(f'<rect x="{vx}" y="{base-vh}" width="20" height="{vh+2}" rx="10" style="fill:#E8B4A0;stroke:#B07A72;stroke-width:1"/>')
        f.raw(f'<rect x="{vx+6}" y="{base+2}" width="8" height="{cd}" rx="4" class="fx-crypt"/>')
    if vh <= 4:
        f.raw(f'<line x1="{x}" y1="{base}" x2="{x+58}" y2="{base}" style="stroke:#B07A72;stroke-width:2"/>')
    for j in range(iel):
        cx = x + 8 + (j * 11) % 44
        cy = base - min(vh, 20) * .6 + (j % 2) * 6 if vh > 4 else base - 3
        f.raw(f'<circle cx="{cx}" cy="{cy}" r="2.6" style="fill:{C["p"]}"/>')
    f.t(x + 29, 34, 'Marsh ' + k, 10.5, bold=True)
    f.t(x + 29, 236, s, 9.5, 'fx-mut')
f.raw(f'<circle cx="16" cy="266" r="3" style="fill:{C["p"]}"/>')
f.t(24, 266, 'linfocitos intraepiteliales (>25 por 100 enterocitos desde Marsh 1) · criptas cada vez más profundas', 9, 'fx-mut', 'start')
reg('celiaquia-marsh', f)

# 8. Crohn contra CUCI
f = F(300, 'Distribución y profundidad de la enfermedad de Crohn y la colitis ulcerosa')
f.t(200, 12, 'Crohn contra CUCI', 12, bold=True)
segs = ['Boca', 'Esóf.', 'Estóm.', 'Duod.', 'Yeyuno', 'Íleon', 'Ciego', 'Colon', 'Sigm.', 'Recto']
w = 37
for row, (nm, col, on) in enumerate([('Crohn', C['p'], [0, 0, 1, 0, 1, 2, 2, 1, 0, 0]),
                                     ('CUCI', C['a'], [0, 0, 0, 0, 0, 0, 1, 2, 2, 2])]):
    y = 40 + row * 64
    f.t(8, y - 8, nm, 11, bold=True, anchor='start')
    for i, s in enumerate(segs):
        x = 16 + i * w
        op = (0, .35, .8)[on[i]]
        f.raw(f'<rect x="{x}" y="{y}" width="{w-3}" height="22" rx="4" class="fx-row"/>')
        if op:
            f.raw(f'<rect x="{x}" y="{y}" width="{w-3}" height="22" rx="4" style="fill:{col};fill-opacity:{op}"/>')
        f.t(x + (w - 3) / 2, y + 32, s, 8, 'fx-mut')
f.t(200, 160, 'Crohn: en parches, de la boca al ano (más en íleon terminal); CUCI: desde el recto, continua †', 9, 'fx-mut')
# profundidad
for i, (nm, col, d) in enumerate([('Crohn: transmural → fístulas y estenosis', C['p'], 4), ('CUCI: solo mucosa → sangrado', C['a'], 1)]):
    x = 8 + i * 198
    lay = ['Mucosa', 'Submucosa', 'Muscular', 'Serosa']
    for j, l in enumerate(lay):
        y = 180 + j * 18
        f.raw(f'<rect x="{x}" y="{y}" width="186" height="16" rx="3" class="fx-row"/>')
        if j < d:
            f.raw(f'<rect x="{x}" y="{y}" width="186" height="16" rx="3" style="fill:{col};fill-opacity:.45"/>')
        f.t(x + 93, y + 8, l, 9)
    f.t(x + 93, 262, nm, 9.5, bold=True)
f.t(200, 286, 'Granulomas, fístulas y recto respetado → Crohn · Recto siempre afectado y sin saltos → CUCI', 9, 'fx-mut')
reg('eii-comparacion', f)

# 9. Colaterales portosistémicas
f = F(300, 'Colaterales portosistémicas en la hipertensión portal')
f.t(200, 12, 'Cuando sube la presión portal, la sangre busca salida', 12, bold=True)
f.box(130, 26, 140, 34, C['r'], 'Hipertensión portal\n(GPVH ≥10 mmHg)', 10.5, True)
rows = [('V. gástrica izquierda\n(coronaria)', 'V. ácigos', 'Várices esofágicas\ny gástricas', C['r']),
        ('V. paraumbilicales', 'V. epigástricas\nde la pared', 'Cabeza de medusa', C['o']),
        ('V. rectal superior', 'V. rectales\nmedia e inferior', 'Várices anorrectales\n(no son hemorroides)', C['p']),
        ('V. esplénica', 'V. renal izquierda', 'Derivación\nesplenorrenal', C['a'])]
f.t(66, 76, 'Lado portal', 9.5, 'fx-mut', bold=True)
f.t(200, 76, 'Lado sistémico', 9.5, 'fx-mut', bold=True)
f.t(334, 76, 'Se manifiesta como', 9.5, 'fx-mut', bold=True)
for i, (a, b, c, col) in enumerate(rows):
    y = 88 + i * 50
    f.box(6, y, 120, 40, col, a, 9.5, op=.1)
    f.box(140, y, 120, 40, C['m'], b, 9.5, op=.08)
    f.box(274, y, 120, 40, col, c, 9.5, True, op=.16)
    f.arr(126, y + 20, 139, y + 20)
    f.arr(260, y + 20, 273, y + 20)
f.t(200, 292, 'GPVH ≥10 mmHg: hipertensión portal clínicamente significativa †', 9.5, 'fx-mut')
reg('cirrosis-colaterales', f)
