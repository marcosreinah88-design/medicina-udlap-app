"""Esquemas propios (SVG en línea) para la guía de Oftalmología (5º).
Usan las clases .dg de la guía (ln, lead, surf, soft, irsf, ves, vesd, warnf…) y sus variables,
así respetan el modo oscuro. ESQ[nombre] = (svg, texto alternativo).
"""
from html import escape

FUN = '#f3c99a'      # fondo de ojo (fijo: se ve igual en claro y oscuro)
FUN_B = '#d89a5c'
DISC = '#fbe6c4'
HEM = '#8f1d1d'
EXU = '#e7c443'
FLUO = '#7fdc6a'


def svg(name, vb, alt, body):
    return (f'<div class="fig-scroll"><svg class="dg" viewBox="{vb}" role="img" aria-label="{escape(alt)}">'
            f'<defs><marker id="ox-ar-{name}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M0,0L10,5L0,10z" fill="var(--accent)"/></marker></defs>{body}</svg></div>')


def lab(pts, x, y, t, sub=None, anchor='start', cls='b'):
    """Línea guía por los puntos pts y rótulo en (x, y)."""
    p = ' '.join(f'{a},{b}' for a, b in pts)
    s = f'<polyline class="lead" points="{p}"/>' if len(pts) > 1 else ''
    s += f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{t}</text>'
    if sub:
        for i, ln in enumerate(sub.split('\n')):
            s += f'<text x="{x}" y="{y + 14 + 13 * i}" text-anchor="{anchor}" class="sm mut">{ln}</text>'
    return s


def fondo(cx, cy, r, dx, cid):
    """Fondo de ojo derecho: papila a la derecha (nasal), arcadas y mácula. dx = distancia papila-mácula."""
    px, mx = cx + dx * 0.55, cx - dx * 0.45
    s = (f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{FUN}" stroke="{FUN_B}" stroke-width="2"/>'
         f'<g clip-path="url(#{cid})">'
         f'<circle cx="{mx}" cy="{cy}" r="{r * 0.27}" fill="{FUN_B}" opacity=".35"/>'
         f'<circle cx="{mx}" cy="{cy}" r="{r * 0.07}" fill="#b5723a" opacity=".8"/>'
         f'<circle cx="{mx}" cy="{cy}" r="1.6" fill="#fff"/>')
    for sg in (-1, 1):
        s += (f'<path class="ves" stroke-width="2" d="M{px - 4},{cy + sg * 6} C{px - 25},{cy + sg * r * .55} {mx + 10},{cy + sg * r * .62} {cx - r},{cy + sg * r * .35}"/>'
              f'<path class="vesd" stroke-width="3" d="M{px - 2},{cy + sg * 9} C{px - 18},{cy + sg * r * .7} {mx},{cy + sg * r * .78} {cx - r},{cy + sg * r * .55}"/>'
              f'<path class="ves" stroke-width="1.6" d="M{px + 4},{cy + sg * 6} C{px + 20},{cy + sg * r * .4} {px + 40},{cy + sg * r * .6} {cx + r},{cy + sg * r * .7}"/>'
              f'<path class="vesd" stroke-width="2.2" d="M{px + 6},{cy + sg * 9} C{px + 30},{cy + sg * r * .3} {px + 50},{cy + sg * r * .4} {cx + r},{cy + sg * r * .45}"/>'
              f'<path class="ves" stroke-width="1.2" d="M{mx + 30},{cy + sg * r * .5} Q{mx + 12},{cy + sg * r * .3} {mx + 6},{cy + sg * r * .2}"/>')
    s += (f'<circle cx="{px}" cy="{cy}" r="{r * 0.15}" fill="{DISC}" stroke="#e2b77e"/>'
          f'<circle cx="{px + 2}" cy="{cy}" r="{r * 0.055}" fill="#fffaf0"/></g>')
    return s, px, mx


ESQ = {}

# ---------- Organización de la retina: fondo de ojo normal ----------
_b, px, mx = fondo(185, 150, 125, 150, 'ox-cl-fn')
ESQ['fondo-normal'] = (svg('fondo-normal', '0 0 600 300',
    'Fondo de ojo derecho normal: papila a la derecha (lado nasal), de donde salen las arcadas vasculares superior e inferior; la mácula con la fóvea y la foveola en el centro de las arcadas, a la izquierda (temporal); la periferia alrededor.',
    _b + '<text x="185" y="294" text-anchor="middle" class="sm mut">Ojo derecho visto con el oftalmoscopio</text>'
    + '<text x="62" y="20" text-anchor="middle" class="sm mut">TEMPORAL</text><text x="300" y="20" text-anchor="middle" class="sm mut">NASAL</text>'
    + lab([(px + 18, 145), (390, 70)], 396, 70, 'Papila (disco óptico)', 'lado nasal; salen la arteria y la vena\ncentrales; es el punto ciego')
    + lab([(140, 70), (175, 40), (390, 40)], 396, 36, 'Arcadas temporales', '')
    + lab([(mx + 4, 156), (230, 200), (390, 180)], 396, 176, 'Mácula → fóvea → foveola', 'en el centro de las arcadas; solo conos,\nsin vasos: la visión más fina')
    + lab([(110, 230), (150, 262), (390, 262)], 396, 252, 'Periferia', 'predominan los bastones; termina\nen la ora serrata')
    + '<text x="396" y="125" class="sm mut">Arteria: roja clara, más delgada †</text><text x="396" y="139" class="sm mut">Vena: más oscura y gruesa †</text>'
    ), '')

# ---------- Retinopatía diabética ----------
_b, px, mx = fondo(165, 150, 135, 160, 'ox-cl-rd')
les = ''
for x, y in [(110, 130), (125, 172), (88, 160), (140, 118), (96, 186), (150, 180)]:
    les += f'<circle cx="{x}" cy="{y}" r="2.4" fill="{HEM}"/>'
for x, y, r in [(70, 110, 6), (210, 215, 7), (60, 200, 5), (180, 228, 5)]:
    les += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{HEM}" opacity=".9"/>'
les += f'<ellipse cx="205" cy="92" rx="11" ry="3.5" fill="{HEM}" transform="rotate(-20 205 92)"/>'
for x, y in [(112, 150), (118, 140), (104, 145), (120, 158), (100, 160), (114, 166)]:
    les += f'<circle cx="{x - 30}" cy="{y}" r="2.6" fill="{EXU}" stroke="#b8941f" stroke-width=".5"/>'
for x, y in [(150, 62), (175, 255)]:
    les += f'<ellipse cx="{x}" cy="{y}" rx="12" ry="7" fill="#fbfaf3" opacity=".95"/>'
les += (f'<g stroke="#d43a2e" stroke-width="1" fill="none"><path d="M{px - 10},{140} q8,-14 16,-2 q6,10 -6,12 q-12,2 -8,-12"/>'
        f'<path d="M{px},{160} q10,-6 14,4 q2,10 -10,6"/><path d="M{px - 16},{158} q-6,10 4,12"/></g>')
cls = ''
etapas = [('Sin RD', 'nada', 'var(--ok)'), ('RDNP leve', 'solo micro-\naneurismas', 'var(--h3)'),
          ('RDNP moderada', 'más que leve,\nmenos que severa', 'var(--warn)'),
          ('RDNP severa', 'regla 4-2-1 *', 'var(--bad)'), ('Proliferativa', 'neovasos o\nhemorragia vítrea', '#7d1d2c')]
for i, (t, d, c) in enumerate(etapas):
    x = 10 + i * 117
    cls += (f'<rect x="{x}" y="318" width="110" height="64" rx="8" class="surf" stroke="{c}" stroke-width="2"/>'
            f'<text x="{x + 55}" y="338" text-anchor="middle" class="b" style="fill:{c}">{t}</text>')
    for j, ln in enumerate(d.split('\n')):
        cls += f'<text x="{x + 55}" y="{356 + 13 * j}" text-anchor="middle" class="sm">{ln}</text>'
    if i:
        cls += f'<line x1="{x - 7}" y1="350" x2="{x - 1}" y2="350" stroke="var(--muted)" stroke-width="1.5" marker-end="url(#ox-ar-rd-hallazgos)"/>'
ESQ['rd-hallazgos'] = (svg('rd-hallazgos', '0 0 600 420',
    'Fondo de ojo con retinopatía diabética: microaneurismas como puntos rojos, hemorragias en punto y mancha, una hemorragia en llama, exudados duros amarillos cerca de la mácula, manchas algodonosas blancas y neovasos sobre la papila. Abajo, las etapas: sin retinopatía, no proliferativa leve, moderada y severa, y proliferativa.',
    _b + les
    + lab([(140, 118), (330, 36)], 336, 36, 'Microaneurismas', 'lo primero que aparece (pérdida de pericitos)')
    + lab([(160, 62), (330, 86)], 336, 86, 'Manchas algodonosas', 'infartos de la capa de fibras (isquemia)')
    + lab([(214, 89), (330, 132)], 336, 132, 'Hemorragia en llama', 'capa de fibras nerviosas')
    + lab([(px + 8, 152), (330, 176)], 336, 176, 'Neovasos en la papila', 'los induce el VEGF: etapa proliferativa')
    + lab([(90, 170), (120, 200), (330, 222)], 336, 222, 'Exudados duros', 'lípidos que se fugan: edema macular')
    + lab([(216, 220), (330, 266)], 336, 266, 'Hemorragias en punto y mancha', 'capas profundas de la retina')
    + '<text x="300" y="306" text-anchor="middle" class="b">Clasificación †</text>' + cls
    + '<text x="300" y="402" text-anchor="middle" class="sm mut">* Hemorragias en los 4 cuadrantes, arrosariamiento venoso en 2, o anomalías microvasculares intrarretinianas (AMIR) en 1.</text>'
    + '<text x="300" y="416" text-anchor="middle" class="sm mut">El edema macular puede aparecer en cualquier etapa.</text>'
    ), '')


# ---------- Glaucoma: ángulo abierto vs cerrado ----------
def angulo(ox, cerrado):
    s = (f'<path d="M{ox + 22},{190} Q{ox + 40},{60} {ox + 270},{38}" stroke="var(--accent)" stroke-width="12" fill="none" opacity=".35"/>'
         f'<rect x="{ox + 14}" y="186" width="20" height="16" rx="3" class="warnf" stroke="var(--warn)"/>'
         f'<ellipse cx="{ox + 40}" cy="236" rx="22" ry="14" fill="var(--bad)" opacity=".35"/>'
         f'<ellipse cx="{ox + 232}" cy="252" rx="62" ry="44" class="soft" stroke="var(--accent)"/>')
    if cerrado:
        s += (f'<path d="M{ox + 30},{205} Q{ox + 110},{150} {ox + 190},{205}" stroke="var(--iris)" stroke-width="9" fill="none" stroke-linecap="round"/>'
              f'<path d="M{ox + 58},{228} Q{ox + 90},{214} {ox + 108},{194}" stroke="var(--accent)" stroke-width="1.6" fill="none" marker-end="url(#ox-ar-glaucoma-angulo)"/>'
              f'<text x="{ox + 196}" y="222" class="b" style="fill:var(--bad)">✕</text>'
              f'<text x="{ox + 20}" y="180" class="b" style="fill:var(--bad)" text-anchor="middle">✕</text>')
    else:
        s += (f'<path d="M{ox + 48},{210} L{ox + 192},{204}" stroke="var(--iris)" stroke-width="9" fill="none" stroke-linecap="round"/>'
              f'<path d="M{ox + 62},{232} Q{ox + 150},{226} {ox + 205},{214} Q{ox + 210},{150} {ox + 110},{150} Q{ox + 60},{150} {ox + 38},{182}" stroke="var(--accent)" stroke-width="1.6" fill="none" marker-end="url(#ox-ar-glaucoma-angulo)"/>')
    return s


ESQ['glaucoma-angulo'] = (svg('glaucoma-angulo', '0 0 600 340',
    'Dos cortes del segmento anterior. Ángulo abierto: el humor acuoso sale de los procesos ciliares, pasa por la pupila, cruza la cámara anterior y drena por la malla trabecular. Ángulo cerrado: el iris se abomba hacia adelante, tapa la malla y el acuoso queda atrapado detrás del iris.',
    angulo(0, False) + angulo(305, True)
    + '<text x="150" y="20" text-anchor="middle" class="b">Ángulo abierto</text><text x="455" y="20" text-anchor="middle" class="b" style="fill:var(--bad)">Cierre angular</text>'
    + lab([(24, 202), (10, 290)], 10, 302, 'Malla trabecular → Schlemm', None, cls='sm')
    + '<text x="130" y="76" class="sm mut">Córnea</text><text x="110" y="196" class="sm" style="fill:var(--iris)">Iris</text>'
    + '<text x="232" y="258" text-anchor="middle" class="sm mut">Cristalino</text><text x="40" y="262" text-anchor="middle" class="sm mut">Cuerpo ciliar</text>'
    + '<text x="150" y="318" text-anchor="middle" class="sm">Gonioscopía: se ven 3–4 estructuras</text><text x="150" y="332" text-anchor="middle" class="sm mut">crónico, silencioso; daña la periferia primero</text>'
    + '<text x="455" y="300" text-anchor="middle" class="sm">El acuoso no pasa por la pupila (bloqueo pupilar †),</text>'
    + '<text x="455" y="314" text-anchor="middle" class="sm">empuja el iris hacia adelante y tapa la malla</text>'
    + '<text x="455" y="332" text-anchor="middle" class="sm mut">ojo rojo doloroso, PIO ≥ 60, pupila semimidriática</text>'
    ), '')

# ---------- Uveítis: localización y signos ----------
ESQ['uveitis-zonas'] = (svg('uveitis-zonas', '0 0 600 300',
    'Corte del ojo con las zonas de la uveítis: anterior en el iris y el cuerpo ciliar, intermedia en la pars plana y el vítreo, y posterior en la retina y la coroides. A la derecha, los signos de la uveítis anterior.',
    '<clipPath id="ox-cl-uv"><circle cx="170" cy="150" r="115"/></clipPath>'
    '<circle cx="170" cy="150" r="115" class="surf" stroke="var(--ink)" stroke-width="1.5"/>'
    '<path d="M70,95 Q30,150 70,205" fill="none" stroke="var(--ink)" stroke-width="1.5"/>'
    '<g clip-path="url(#ox-cl-uv)">'
    '<path d="M170,42 A108,108 0 0 1 170,258" fill="none" stroke="var(--bad)" stroke-width="10" opacity=".5"/>'
    '<ellipse cx="128" cy="150" rx="40" ry="88" fill="var(--warn)" opacity=".22"/>'
    '</g>'
    '<ellipse cx="88" cy="150" rx="12" ry="34" class="soft" stroke="var(--accent)"/>'
    '<g stroke="var(--iris)" stroke-width="6" stroke-linecap="round"><line x1="76" y1="98" x2="80" y2="128"/><line x1="76" y1="202" x2="80" y2="172"/></g>'
    '<ellipse cx="92" cy="88" rx="12" ry="7" class="irsf" opacity=".7"/><ellipse cx="92" cy="212" rx="12" ry="7" class="irsf" opacity=".7"/>'
    + lab([(80, 112), (40, 36)], 10, 30, 'Anterior', 'iris y cuerpo ciliar', cls='b')
    + lab([(128, 70), (150, 20)], 150, 16, 'Intermedia', 'pars plana y vítreo', cls='b')
    + lab([(250, 76), (300, 36)], 306, 36, 'Posterior', 'retina y coroides', cls='b')
    + '<text x="306" y="84" class="b">Signos de uveítis anterior</text>'
    + ''.join(f'<text x="306" y="{104 + 18 * i}" class="sm">• {t}</text>' for i, t in enumerate([
        'Inyección circuncorneal violácea', 'Precipitados en el endotelio corneal', 'Células y turbidez en el acuoso',
        'Nódulos de Koeppe en el borde pupilar', 'Hipopión (pus en la cámara anterior) †', 'Sinequias: iris pegado al cristalino †']))
    + '<text x="306" y="222" class="b">Intermedia</text><text x="306" y="238" class="sm">miodesopsias, vitritis, edema macular cistoide</text>'
    + '<text x="306" y="262" class="sm mut">Antes del esteroide, medir la PIO: la uveítis</text><text x="306" y="276" class="sm mut">puede dar glaucoma secundario.</text>'
    ), '')

# ---------- Orzuelo vs chalazión ----------
def parpado(ox):
    return (f'<path d="M{ox + 60},20 Q{ox + 40},120 {ox + 70},200" fill="none" stroke="var(--ink)" stroke-width="1.5"/>'
            f'<rect x="{ox + 78}" y="70" width="22" height="128" rx="6" class="line"/>'
            f'<rect x="{ox + 84}" y="80" width="10" height="120" rx="5" class="warnf" stroke="var(--warn)"/>'
            f'<path d="M{ox + 70},200 L{ox + 104},202" stroke="var(--ink)" stroke-width="1.5"/>'
            f'<path d="M{ox + 72},198 q-10,20 -30,36" stroke="var(--ink)" stroke-width="2" fill="none"/>'
            f'<ellipse cx="{ox + 68}" cy="186" rx="5" ry="8" class="soft" stroke="var(--accent)"/>')


ESQ['orzuelo-chalazion'] = (svg('orzuelo-chalazion', '0 0 600 300',
    'Corte del párpado superior con la placa tarsal, la glándula de Meibomio dentro del tarso y la de Zeiss junto a la pestaña. El orzuelo externo es un absceso de la glándula de Zeiss y el interno de la de Meibomio, ambos dolorosos. El chalazión es un nódulo estéril e indoloro dentro del tarso.',
    parpado(0) + parpado(300)
    + '<circle cx="66" cy="186" r="14" fill="var(--bad)" opacity=".55"/><circle cx="96" cy="150" r="13" fill="var(--bad)" opacity=".55"/>'
    + '<circle cx="390" cy="135" r="20" fill="var(--warn)" opacity=".6" stroke="var(--warn)"/>'
    + '<text x="20" y="30" class="sm mut">Piel</text><text x="110" y="62" class="sm mut">Tarso</text>'
    + lab([(52, 186), (20, 262)], 10, 274, 'Orzuelo externo', 'glándula de Zeiss', cls='b')
    + lab([(108, 150), (160, 110)], 166, 104, 'Orzuelo interno', 'glándula de Meibomio')
    + '<text x="166" y="160" class="b" style="fill:var(--bad)">Dolorosos, agudos</text><text x="166" y="176" class="sm">absceso estafilocócico</text><text x="166" y="190" class="sm">compresas y antibiótico;</text><text x="166" y="204" class="sm">no puncionar</text>'
    + lab([(410, 135), (460, 100)], 466, 96, 'Chalazión', 'Meibomio, dentro del tarso')
    + '<text x="466" y="150" class="b" style="fill:var(--warn)">Indoloro, crónico</text><text x="466" y="166" class="sm">lipogranuloma estéril</text><text x="466" y="180" class="sm">rosácea, seborrea u</text><text x="466" y="194" class="sm">orzuelo que no resolvió</text><text x="466" y="208" class="sm">→ resección</text>'
    + '<text x="342" y="252" class="sm mut">Pestaña</text>'
    ), '')


# ---------- Pinguécula vs pterigión ----------
def ojo(ox):
    return (f'<path d="M{ox + 20},120 Q{ox + 140},30 {ox + 260},120 Q{ox + 140},210 {ox + 20},120 Z" class="sclera" stroke="var(--ink)" stroke-width="1.5"/>'
            f'<circle cx="{ox + 140}" cy="120" r="46" class="irsf" opacity=".85"/><circle cx="{ox + 140}" cy="120" r="16" fill="#111"/>'
            f'<circle cx="{ox + 140}" cy="120" r="46" fill="none" stroke="#6b4f9a" stroke-width="2"/>')


ESQ['pinguecula-pterigion'] = (svg('pinguecula-pterigion', '0 0 600 260',
    'Dos ojos derechos de frente. Pinguécula: nódulo blanco-amarillento en la conjuntiva nasal, junto al limbo, sin entrar a la córnea. Pterigión: tejido fibrovascular triangular que nace en la conjuntiva nasal y avanza sobre la córnea, con cabeza, cuerpo y casquete.',
    ojo(0) + ojo(310)
    + '<ellipse cx="225" cy="122" rx="18" ry="11" fill="#e9d48a" stroke="#c0a347"/>'
    + '<clipPath id="ox-cl-pt"><path d="M330,120 Q450,30 570,120 Q450,210 330,120 Z"/></clipPath><g clip-path="url(#ox-cl-pt)">'
    + '<path d="M575,92 L478,112 Q470,120 478,128 L575,150 Z" fill="#e7a3a0" opacity=".9"/>'
    + '<g stroke="#c0443a" stroke-width="1"><line x1="560" y1="104" x2="484" y2="116"/><line x1="560" y1="138" x2="484" y2="124"/><line x1="560" y1="121" x2="482" y2="120"/></g></g>'
    + '<path d="M472,108 Q462,120 472,132" stroke="#9aa3a8" stroke-width="3" fill="none"/>'
    + '<text x="70" y="20" class="sm mut">TEMPORAL</text><text x="230" y="20" class="sm mut">NASAL</text><text x="380" y="20" class="sm mut">TEMPORAL</text><text x="540" y="20" class="sm mut">NASAL</text>'
    + '<text x="140" y="226" text-anchor="middle" class="b">Pinguécula</text><text x="140" y="242" text-anchor="middle" class="sm">no cruza el limbo · elastosis</text><text x="140" y="256" text-anchor="middle" class="sm mut">lubricante; si se inflama, fluorometolona</text>'
    + '<text x="450" y="226" text-anchor="middle" class="b">Pterigión</text><text x="450" y="242" text-anchor="middle" class="sm">invade la córnea → astigmatismo</text><text x="450" y="256" text-anchor="middle" class="sm mut">cirugía con injerto si llega al eje visual</text>'
    + lab([(468, 120), (440, 190)], 400, 202, 'Casquete', None, cls='sm') + lab([(486, 120), (500, 186)], 480, 198, 'Cabeza', None, cls='sm')
    + lab([(540, 120), (560, 186)], 548, 198, 'Cuerpo', None, cls='sm')
    ), '')


# ---------- Cirugía refractiva: LASIK vs PRK ----------
def cornea(ox, lasik):
    s = (f'<path d="M{ox},140 Q{ox + 140},40 {ox + 280},140" fill="none" stroke="var(--accent)" stroke-width="44" opacity=".22"/>'
         f'<path d="M{ox},140 Q{ox + 140},40 {ox + 280},140" fill="none" stroke="var(--ink)" stroke-width="1" transform="translate(0,22)" opacity=".5"/>')
    if lasik:
        s += (f'<path d="M{ox + 60},86 C{ox + 40},52 {ox + 70},34 {ox + 140},36" fill="none" stroke="var(--warn)" stroke-width="9" stroke-linecap="round"/>'
              f'<path d="M{ox + 80},100 Q{ox + 140},70 {ox + 200},100" fill="var(--bad)" opacity=".35"/>'
              f'<circle cx="{ox + 58}" cy="88" r="3" fill="var(--warn)"/>')
    else:
        s += (f'<path d="M{ox + 30},116 Q{ox + 140},34 {ox + 250},116" fill="none" stroke="#e7c443" stroke-width="5" stroke-dasharray="70 120 1000" />'
              f'<path d="M{ox + 90},74 Q{ox + 140},60 {ox + 190},74 Q{ox + 140},68 {ox + 90},74" fill="var(--bad)" opacity=".5"/>')
    return s


ESQ['lasik-prk'] = (svg('lasik-prk', '0 0 600 250',
    'Corte de la córnea. En el LASIK se levanta un colgajo con bisagra, el láser talla el estroma debajo y el colgajo se recoloca. En la PRK se retira el epitelio central y el láser trata directamente la superficie.',
    cornea(10, True) + cornea(310, False)
    + '<text x="230" y="20" text-anchor="middle" class="b">LASIK</text><text x="450" y="20" text-anchor="middle" class="b">PRK</text>'
    + lab([(52, 64), (30, 30)], 10, 24, 'Colgajo levantado (bisagra)', None, cls='sm')
    + '<text x="150" y="122" text-anchor="middle" class="sm" style="fill:var(--bad)">ablación en el estroma</text>'
    + '<text x="450" y="104" text-anchor="middle" class="sm" style="fill:var(--bad)">ablación en la superficie</text>'
    + '<text x="380" y="46" class="sm mut">epitelio retirado en el centro</text>'
    + '<text x="150" y="186" text-anchor="middle" class="sm">Se recoloca el colgajo; recuperación rápida</text>'
    + '<text x="150" y="202" text-anchor="middle" class="sm mut">riesgos del colgajo †</text>'
    + '<text x="450" y="186" text-anchor="middle" class="sm">El epitelio vuelve a crecer en días</text>'
    + '<text x="450" y="202" text-anchor="middle" class="sm mut">más dolor al inicio; sin colgajo †</text>'
    + '<text x="300" y="234" text-anchor="middle" class="sm">No operar si hay graduación inestable, queratocono, ojo seco importante o enfermedad activa.</text>'
    ), '')


# ---------- Queratitis infecciosas: cómo se ven con fluoresceína ----------
def ojo_azul(cx, cid):
    return (f'<clipPath id="{cid}"><circle cx="{cx}" cy="110" r="74"/></clipPath>'
            f'<circle cx="{cx}" cy="110" r="80" fill="#1a2a5c"/><circle cx="{cx}" cy="110" r="74" fill="#22346e" stroke="#3a4f92"/>'
            f'<circle cx="{cx}" cy="110" r="22" fill="#0b1230"/>')


_d = '<g stroke="%s" stroke-width="4" fill="none" stroke-linecap="round">' % FLUO
_d += '<path d="M70,92 L95,104 L120,98 L140,112"/><path d="M95,104 L92,128"/><path d="M120,98 L126,80"/><path d="M140,112 L150,130"/></g>'
_d += ''.join(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{FLUO}"/>' for x, y in [(70, 92), (92, 128), (126, 80), (150, 130)])
ESQ['queratitis-patrones'] = (svg('queratitis-patrones', '0 0 600 260',
    'Tres córneas teñidas con fluoresceína bajo luz azul. Herpes: úlcera dendrítica, ramificada con bulbos terminales. Bacteriana: infiltrado blanco-amarillo con secreción y nivel de pus en la cámara anterior (hipopión). Micótica: infiltrado de bordes plumosos con lesiones satélite.',
    ojo_azul(110, 'ox-q1') + _d + ojo_azul(300, 'ox-q2') + ojo_azul(490, 'ox-q3')
    + '<g clip-path="url(#ox-q2)"><circle cx="300" cy="100" r="26" fill="#f2ead0"/><circle cx="300" cy="100" r="31" fill="none" stroke="' + FLUO + '" stroke-width="4"/>'
    + '<rect x="220" y="160" width="160" height="40" fill="#efe6c2"/></g>'
    + '<g clip-path="url(#ox-q3)"><path d="M470,100 q8,-18 22,-8 q16,-6 16,10 q10,12 -4,20 q-6,14 -20,6 q-16,4 -16,-10 q-12,-8 2,-18z" fill="#d9dccf" opacity=".95"/>'
    + '<circle cx="490" cy="108" r="40" fill="none" stroke="#d9dccf" stroke-width="2" stroke-dasharray="3 5"/>'
    + ''.join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#d9dccf"/>' for x, y in [(452, 78), (532, 92), (522, 146), (458, 144), (500, 60)]) + '</g>'
    + '<text x="110" y="216" text-anchor="middle" class="b">Herpes simple</text><text x="110" y="232" text-anchor="middle" class="sm">úlcera dendrítica</text><text x="110" y="246" text-anchor="middle" class="sm mut">sin esteroides</text>'
    + '<text x="300" y="216" text-anchor="middle" class="b">Bacteriana</text><text x="300" y="232" text-anchor="middle" class="sm">infiltrado + hipopión</text><text x="300" y="246" text-anchor="middle" class="sm mut">amplio espectro sin esperar el Gram</text>'
    + '<text x="490" y="216" text-anchor="middle" class="b">Micótica</text><text x="490" y="232" text-anchor="middle" class="sm">bordes plumosos, satélites</text><text x="490" y="246" text-anchor="middle" class="sm mut">trauma con material vegetal</text>'
    ), '')

# ---------- Folículos vs papilas ----------
_f = '<path d="M30,150 Q140,40 250,150 Z" fill="#e9e3d8" stroke="#b9ad98"/>'
_f += '<g stroke="#c0443a" stroke-width="1.6" fill="none"><path d="M30,150 Q60,110 80,96"/><path d="M250,150 Q220,110 200,96"/><path d="M20,140 Q40,120 52,112"/><path d="M262,140 Q240,120 228,112"/></g>'
_p = '<path d="M330,150 L350,80 L430,60 L520,82 L560,150 Z" fill="#e7a3a0" stroke="#c0443a"/>'
_p += '<g stroke="#a81f1f" stroke-width="1.8" fill="none"><path d="M445,150 L445,92"/><path d="M445,96 L410,76"/><path d="M445,96 L480,74"/><path d="M445,96 L440,64"/><path d="M445,110 L380,96"/><path d="M445,110 L515,98"/></g>'
ESQ['foliculos-papilas'] = (svg('foliculos-papilas', '0 0 600 240',
    'Folículo: elevación redondeada y pálida de tejido linfoide con los vasos rodeándola desde la base. Papila: elevación roja poligonal con un vaso central que se ramifica como rayos.',
    _f + _p + '<line x1="10" y1="150" x2="590" y2="150" stroke="var(--ink)" stroke-width="1.5"/>'
    + '<text x="140" y="24" text-anchor="middle" class="b">Folículo</text><text x="445" y="24" text-anchor="middle" class="b">Papila</text>'
    + '<text x="140" y="174" text-anchor="middle" class="sm">tejido linfoide; los vasos lo rodean</text><text x="140" y="190" text-anchor="middle" class="sm">más en el tarso inferior</text>'
    + '<text x="140" y="210" text-anchor="middle" class="b sm" style="fill:var(--accent)">virales, clamidia, tóxicas</text>'
    + '<text x="445" y="174" text-anchor="middle" class="sm">vaso central; varias forman un empedrado</text><text x="445" y="190" text-anchor="middle" class="sm">más en el tarso superior</text>'
    + '<text x="445" y="210" text-anchor="middle" class="b sm" style="fill:var(--accent)">bacterianas y alérgicas</text>'
    ), '')


# ---------- Cristalino y acomodación ----------
def acom(ox, cerca):
    ry = 46 if cerca else 46
    rx = 22 if cerca else 12
    y_c = 52 if cerca else 40
    s = (f'<ellipse cx="{ox + 150}" cy="120" rx="{rx}" ry="{ry}" class="soft" stroke="var(--accent)" stroke-width="1.5"/>'
         f'<ellipse cx="{ox + 150}" cy="{120 - 92}" rx="{20 if cerca else 14}" ry="{14 if cerca else 10}" class="badf" opacity=".5"/>'
         f'<ellipse cx="{ox + 150}" cy="{120 + 92}" rx="{20 if cerca else 14}" ry="{14 if cerca else 10}" class="badf" opacity=".5"/>')
    zl = 'stroke-dasharray="3 3"' if cerca else ''
    for sg in (-1, 1):
        for d in (-8, 0, 8):
            s += f'<line x1="{ox + 150 + d}" y1="{120 + sg * (92 - (14 if cerca else 10))}" x2="{ox + 150 + d * .6}" y2="{120 + sg * (ry - 2)}" stroke="var(--muted)" stroke-width="1" {zl}/>'
    fx = ox + 150 + (110 if cerca else 130)
    for y in (90, 120, 150):
        x0 = ox + (40 if cerca else 20)
        y0 = 120 if cerca else y
        s += f'<polyline points="{x0},{y0} {ox + 150},{y} {fx},120" fill="none" stroke="var(--warn)" stroke-width="1.2"/>'
    if cerca:
        s += f'<circle cx="{ox + 40}" cy="120" r="5" fill="var(--warn)"/>'
    return s


ESQ['acomodacion'] = (svg('acomodacion', '0 0 600 270',
    'Lejos: el músculo ciliar está relajado, la zónula tensa y el cristalino aplanado; los rayos paralelos enfocan en la retina. Cerca: el ciliar se contrae, la zónula se afloja y el cristalino se abomba para enfocar un objeto cercano, junto con miosis y convergencia.',
    acom(0, False) + acom(300, True)
    + '<text x="150" y="250" text-anchor="middle" class="b">Lejos (≥ 6 m): no acomoda</text><text x="150" y="266" text-anchor="middle" class="sm">ciliar relajado · zónula tensa · cristalino plano</text>'
    + '<text x="450" y="250" text-anchor="middle" class="b">Cerca: acomoda</text><text x="450" y="266" text-anchor="middle" class="sm">ciliar contraído (III) · zónula floja · más curvo</text>'
    + '<text x="196" y="30" class="sm" style="fill:var(--bad)">músculo ciliar</text><text x="196" y="122" class="sm mut">zónula</text>'
    + '<text x="520" y="40" class="sm mut">+ miosis y</text><text x="520" y="54" class="sm mut">convergencia</text><text x="340" y="108" class="sm mut">objeto</text>'
    ), '')

# ---------- Presbicia: amplitud de acomodación por edad ----------
_dat = [(10, 14), (20, 11), (30, 8.5), (40, 5.5), (45, 3.5), (50, 2.5), (60, 1.2), (70, 1)]
_ch = '<line x1="60" y1="210" x2="580" y2="210" stroke="var(--ink)" stroke-width="1"/><line x1="60" y1="20" x2="60" y2="210" stroke="var(--ink)" stroke-width="1"/>'
for v in (0, 4, 8, 12):
    y = 210 - v * 12.5
    _ch += f'<text x="52" y="{y + 4}" text-anchor="end" class="sm mut">{v}</text>'
for i, (e, a) in enumerate(_dat):
    x = 80 + i * 62
    h = a * 12.5
    c = 'var(--bad)' if a < 4 else 'var(--accent)'
    _ch += (f'<rect x="{x}" y="{210 - h}" width="40" height="{h}" rx="4" fill="{c}" opacity=".75"/>'
            f'<text x="{x + 20}" y="226" text-anchor="middle" class="sm">{e}</text>'
            f'<text x="{x + 20}" y="{204 - h}" text-anchor="middle" class="sm b">{a:g}</text>')
_ch += '<line x1="60" y1="160" x2="580" y2="160" stroke="var(--warn)" stroke-width="1.5" stroke-dasharray="6 4"/>'
ESQ['presbicia-edad'] = (svg('presbicia-edad', '0 0 600 260',
    'Gráfica de barras de la amplitud de acomodación por edad: unas 14 dioptrías a los 10 años, 11 a los 20, 8.5 a los 30, 5.5 a los 40, 3.5 a los 45, 2.5 a los 50 y cerca de 1 desde los 60. Una línea marca unas 4 dioptrías, lo que hace falta para leer cómodo a 33 cm.',
    _ch + '<text x="20" y="115" text-anchor="middle" class="sm mut" transform="rotate(-90 20 115)">Dioptrías que puede acomodar</text>'
    + '<text x="320" y="248" text-anchor="middle" class="sm mut">Edad (años)</text>'
    + '<text x="575" y="152" text-anchor="end" class="sm" style="fill:var(--warn)">≈ 4 D: leer cómodo a 33 cm</text>'
    ), '')
