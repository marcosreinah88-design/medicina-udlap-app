"""Recorta y traduce las fotos libres (OpenStax CC BY 4.0 / dominio público) para Imagenología.
Uso: python3 tools-imagenologia/fotos.py <carpeta con los originales>
Los originales salen de github.com/openstax/osbooks-{anatomy-physiology,college-physics-bundle,microbiology}
(media/<archivo>) y de github.com/ieee8023/covid-chestxray-dataset (images/2c35005f.jpg)."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageChops
import numpy as np

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def load(n):
    return Image.open(os.path.join(SRC, n)).convert('RGB')

def trim(im, tol=242):
    a = np.asarray(im.convert('L'))
    m = a < tol
    ys, xs = np.where(m)
    if not len(xs): return im
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

def save(im, name, maxw=900, q=72):
    im = trim(im)
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    if im.height > 900:
        im = im.resize((round(im.width * 900 / im.height), 900), Image.LANCZOS)
    im.save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=q, method=6)

def relabel(im, boxes):
    """boxes: (x0,y0,x1,y1, texto, tamaño, color_fondo|None, color_texto)"""
    d = ImageDraw.Draw(im)
    a = np.asarray(im)
    for x0, y0, x1, y1, txt, sz, bg, fg in boxes:
        if bg is None:  # color del borde alrededor
            ring = np.concatenate([a[y0-4:y0-1, x0:x1].reshape(-1, 3), a[y1+1:y1+4, x0:x1].reshape(-1, 3)])
            bg = tuple(int(v) for v in np.median(ring, 0))
        d.rectangle((x0, y0, x1, y1), fill=bg)
        f = ImageFont.truetype(F, sz)
        d.multiline_text((x0 + 6, y0 + 4), txt, font=f, fill=fg, spacing=4)
    return im

# Historia
save(load('Figure 30_03_02a.jpg'), 'historia-mano-bertha')
# Rayos X
save(load('01_16_X-ray_of_Hand.jpg'), 'rx-mano')
save(load('Figure_31_04_05aa.jpg'), 'rx-torax-marcapasos')
save(load('Figure_31_04_04aa.jpg'), 'rx-panoramica')
save(load('Figure 25_03_15a.jpg'), 'rx-torax-valvulas')
# Protección radiológica (rótulos al español)
im = load('Figure_33_02_02a.jpg')
im = relabel(im, [
    (320, 176, 520, 218, 'Tubo de rayos X', 24, None, (0, 0, 0)),
    (596, 446, 700, 484, 'Película', 24, None, (0, 0, 0)),
    (10, 562, 196, 648, 'Colimador\nde plomo', 24, None, (0, 0, 0)),
    (340, 666, 590, 708, 'Mandil de plomo', 26, None, (0, 0, 0)),
])
save(im, 'rad-dental-proteccion')
# TC
save(load('Figure_31_04_06aa.jpg'), 'tc-equipo')
save(load('Figure_31_04_07aa.jpg'), 'tc-craneo-3d')
mi = load('113abcd_Medical_Imaging_Techniques.jpg')
save(mi.crop((0, 0, 930, 870)), 'tc-cortes-craneo')
save(mi.crop((986, 0, 2075, 870)), 'rm-equipo-2')
save(mi.crop((986, 1020, 2075, 1787)), 'eco-obstetrico')
# Ecografía
us = load('Figure_18_07_04.jpg')
save(us.crop((0, 0, 589, 481)), 'eco-estudio')
save(us.crop((664, 0, 1300, 481)), 'eco-feto-12sem')
save(load('Figure_18_07_05a.jpg'), 'eco-3d')
# Doppler
save(load('Figure_18_07_06a.jpg'), 'doppler-carotida')
# RM
save(load('Figure_23_02_03a.jpg'), 'rm-equipo')
save(load('Figure_08_08_03a.jpg'), 'rm-funcional')
save(load('OSC_Microbio_26_03_WNV.jpg').crop((735, 0, 1200, 528)), 'rm-tc-encefalitis')
# Contraste: angiografía coronaria
im = load('2016_Occluded_Coronay_Arteries.jpg')
im = relabel(im, [
    (478, 50, 946, 151, 'Obstrucción del tronco común\nde la coronaria izquierda', 30, (226, 226, 226), (0, 0, 0)),
    (163, 476, 470, 576, 'Obstrucción de\nla circunfleja', 30, (226, 226, 226), (0, 0, 0)),
])
save(im, 'contraste-coronariografia')
# EVC / edema
hs = load('1602_The_Hemorrhagic_Stroke-02.jpg')
save(hs.crop((0, 0, 852, 1242)), 'evc-hemorragia-esquema')
save(hs.crop((1032, 0, 2033, 1242)), 'evc-hemorragia-tc')
# SNC
save(load('OSC_Microbio_26_04_Neurocyst.jpg'), 'snc-neurocisticercosis')
# Tórax
save(load('cxr_2c35005f.jpg'), 'tele-normal')
pn = load('OSC_Microbio_03_02_pneumonia.jpg')
save(pn.crop((0, 0, 319, 290)), 'neumonia-infiltrado')
save(pn.crop((395, 0, 700, 290)), 'neumonia-normal')
save(load('OSC_Microbio_04_02_Xray.jpg'), 'neumonia-cavitacion')
save(load('OSC_Microbio_22_04_Aspirgil.jpg'), 'neumonia-aspergiloma')
print('ok')
