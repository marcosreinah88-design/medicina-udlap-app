"""Prepara las fotos y figuras libres (OpenStax, CC BY 4.0; muchas de CDC/NIH en dominio público).
Se evitan las micrografías «Regents of University of Michigan ©» (no son CC BY)
para la guía de Gastroenterología (5º): recorta, borra los rótulos en inglés y los vuelve a escribir en español.

Uso: python3 tools-gastro/fotos.py
Los originales se bajan de GitHub (no hace falta openstax.org):
  git clone --filter=blob:none --no-checkout --depth 1 https://github.com/openstax/osbooks-anatomy-physiology
  git clone --filter=blob:none --no-checkout --depth 1 https://github.com/openstax/osbooks-microbiology
  git checkout HEAD -- media/<archivo>      (dentro de cada clon)
y se copian a tools-gastro/orig/. Salida: tools-gastro/img/*.webp (≤1000 px de ancho).
"""
import os
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(HERE, 'orig')
OUT = os.path.join(HERE, 'img')
FONT = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
FONTB = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONTI = '/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf'


def bg_of(im, box, pad=3):
    """Color de fondo alrededor de un rótulo (moda del borde)."""
    x0, y0, x1, y1 = box
    W, H = im.size
    px = []
    for x in range(max(0, x0 - pad), min(W, x1 + pad)):
        for y in (max(0, y0 - pad), min(H - 1, y1 + pad)):
            px.append(im.getpixel((x, y)))
    for y in range(max(0, y0 - pad), min(H, y1 + pad)):
        for x in (max(0, x0 - pad), min(W - 1, x1 + pad)):
            px.append(im.getpixel((x, y)))
    q = [tuple(c // 8 * 8 for c in p) for p in px]
    m = Counter(q).most_common(1)[0][0]
    sel = [p for p, k in zip(px, q) if k == m]
    return tuple(sum(c[i] for c in sel) // len(sel) for i in range(3))


def relabel(name, out, labels=(), erase=(), crop=None, size=16, pad=(0, 0, 0, 0), width=1000, color=(30, 30, 30)):
    im = Image.open(os.path.join(ORIG, name)).convert('RGB')
    d = ImageDraw.Draw(im)
    for b in erase:
        x0, y0, x1, y1 = b[:4]
        fill = b[4] if len(b) > 4 else bg_of(im, (x0, y0, x1, y1))
        d.rectangle((x0 - 2, y0 - 2, x1 + 2, y1 + 2), fill=fill)
    jobs = []
    for L in labels:
        x0, y0, x1, y1, txt, al = L[:6]
        opt = L[6] if len(L) > 6 else {}
        fill = opt.get('bg') or bg_of(im, (x0, y0, x1, y1))
        d.rectangle((x0 - 2, y0 - 2, x1 + 2, y1 + 2), fill=fill)
        jobs.append((x0, y0, x1, y1, txt, al, opt))
    # lienzo con margen por si el español es más largo
    l, t, r, b = pad
    if any(pad):
        big = Image.new('RGB', (im.width + l + r, im.height + t + b), 'white')
        big.paste(im, (l, t))
        im = big
    d = ImageDraw.Draw(im)
    for x0, y0, x1, y1, txt, al, opt in jobs:
        fs = opt.get('size', size)
        f = ImageFont.truetype(FONTB if opt.get('bold') else FONTI if opt.get('it') else FONT, fs)
        lines = txt.split('\n')
        lh = round(fs * 1.18)
        th = lh * len(lines)
        cy = (y0 + y1) / 2 + t
        yy = cy - th / 2 + opt.get('dy', 0)
        for ln in lines:
            w = d.textlength(ln, font=f)
            if al == 'l':
                xx = x0 + l
            elif al == 'r':
                xx = x1 + l - w
            else:
                xx = (x0 + x1) / 2 + l - w / 2
            d.text((xx, yy), ln, font=f, fill=opt.get('color', color))
            yy += lh
    if crop:
        im = im.crop(crop)
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    im.save(os.path.join(OUT, out), 'WEBP', quality=78, method=6)
    return im.size


S = {}

# ---------- Esófago y estómago ----------
S['erge-esofago.webp'] = dict(name='2412_The_Esophagus.jpg', size=18, labels=[
    (447, 265, 614, 309, 'Esfínter esofágico\nsuperior', 'l'),
    (0, 328, 73, 343, 'Tráquea', 'l'),
    (1, 577, 103, 597, 'Esófago', 'l'),
    (443, 577, 611, 621, 'Esfínter esofágico\ninferior', 'l'),
    (1, 777, 81, 792, 'Estómago', 'l'),
], pad=(0, 0, 20, 0))

S['ulcera-estomago.webp'] = dict(name='2414_Stomach.jpg', size=16, labels=[
    (959, 2, 1019, 18, 'Cardias', 'l'),
    (1, 40, 103, 59, 'Esófago', 'l'),
    (1, 73, 193, 89, 'Muscular externa:', 'l', {'bold': True}),
    (960, 74, 1027, 89, 'Fondo', 'l'),
    (13, 98, 174, 117, 'Capa longitudinal', 'l'),
    (12, 123, 133, 142, 'Capa circular', 'l'),
    (12, 148, 133, 168, 'Capa oblicua', 'l'),
    (960, 184, 1024, 199, 'Serosa', 'l'),
    (960, 305, 1006, 324, 'Cuerpo', 'l'),
    (275, 315, 427, 330, 'Curvatura menor', 'l'),
    (1, 360, 156, 404, 'Esfínter pilórico\n(válvula) en el píloro', 'l'),
    (960, 388, 1021, 403, 'Luz', 'l'),
    (960, 445, 1120, 464, 'Pliegues de la mucosa', 'l'),
    (1, 548, 108, 580, 'Duodeno', 'l'),
    (180, 652, 296, 672, 'Canal pilórico', 'l'),
    (465, 721, 596, 741, 'Antro pilórico', 'l'),
    (722, 721, 883, 736, 'Curvatura mayor', 'l'),
], pad=(0, 0, 40, 0))

S['ulcera-glandula.webp'] = dict(name='2415_Histology_of_StomachN.jpg', size=14, labels=[
    (847, 50, 952, 65, 'Célula parietal', 'l'),
    (229, 70, 326, 117, 'Epitelio\nsuperficial', 'l'),
    (847, 89, 939, 108, 'Fosita gástrica', 'l'),
    (69, 170, 140, 185, 'Mucosa', 'l'),
    (847, 208, 968, 229, 'Glándula gástrica', 'l'),
    (227, 240, 293, 282, 'Lámina\npropia', 'l'),
    (853, 295, 937, 311, 'Célula principal', 'l'),
    (227, 304, 325, 343, 'Muscular de\nla mucosa', 'l'),
    (69, 354, 177, 370, 'Submucosa', 'l'),
    (226, 381, 352, 401, 'Capa oblicua', 'l'),
    (226, 421, 347, 441, 'Capa circular', 'l'),
    (69, 432, 167, 472, 'Muscular\nexterna', 'l'),
    (817, 433, 969, 474, 'Célula\nenteroendocrina', 'l'),
    (227, 463, 337, 506, 'Capa\nlongitudinal', 'l'),
    (69, 523, 134, 539, 'Serosa', 'l'),
])

S['ulcera-hpylori.webp'] = dict(name='OSC_Microbio_24_03_Ulcers.jpg', size=19, labels=[
    (33, 202, 249, 286, 'El epitelio gástrico\nsano está cubierto\npor una capa de moco.', 'l'),
    (407, 297, 478, 311, 'moco', 'l'),
    (487, 345, 813, 430, 'Helicobacter pylori coloniza\nel epitelio y disminuye\nla producción de moco.', 'l'),
    (1008, 355, 1151, 465, 'El ácido\ngástrico forma\nla úlcera.', 'l'),
    (866, 412, 919, 430, 'úlcera', 'l'),
    (690, 469, 831, 492, 'célula epitelial', 'l'),
    (209, 920, 355, 939, 'eritrocito', 'l'),
    (511, 1128, 618, 1151, 'neutrófilo', 'l'),
    (717, 1162, 823, 1184, 'monocito', 'l'),
], pad=(0, 0, 30, 0))

S['hpylori-invasion.webp'] = dict(name='OSC_Microbio_15_02_Invasion.jpg', size=22, labels=[
    (245, 11, 349, 64, 'gel de mucina\ngástrica', 'l'),
    (424, 11, 520, 59, 'células\nepiteliales', 'l'),
    (110, 40, 202, 63, 'H. pylori', 'l', {'it': True}),
    (83, 426, 541, 541, 'El ácido mantiene la mucina en\nestado de gel esponjoso, que\nla bacteria no puede atravesar.', 'l'),
    (607, 426, 1070, 541, 'La bacteria libera ureasa: neutraliza\nel ácido, la mucina se licua y la\nbacteria nada a través de ella.', 'l'),
])

# ---------- Intestino ----------
S['celiaquia-vellosidad.webp'] = dict(name='2418_Histology_Small_IntestinesN.jpg', size=30, crop=(0, 0, 2290, 1010), labels=[
    (1092, 5, 1234, 33, 'Quilífero', 'l'),
    (1553, 32, 1813, 67, 'Enterocitos', 'l'),
    (592, 64, 843, 134, 'Vaso\nsanguíneo', 'l'),
    (1976, 79, 2208, 156, 'Microvellosidades\n(borde en cepillo)', 'c'),
    (1553, 88, 1697, 124, 'Capilar', 'l'),
    (1553, 145, 1652, 180, 'Arteria', 'l'),
    (1553, 200, 1727, 229, 'Célula caliciforme', 'l'),
    (633, 258, 743, 286, 'Luz', 'l'),
    (630, 317, 759, 388, 'Pliegues\ncirculares', 'l'),
    (93, 348, 200, 425, 'Capas\nmusculares', 'r', {'dy': 14}),
    (331, 364, 385, 391, 'Vellosidades', 'r', {'size': 24, 'dy': -4}),
    (1551, 474, 1789, 509, 'Cripta intestinal', 'l'),
    (1051, 874, 1331, 909, 'Vaso linfático', 'c'),
    (718, 945, 1056, 973, 'Muscular de la mucosa', 'c'),
    (1302, 945, 1560, 981, 'Glándula duodenal', 'c'),
], pad=(60, 0, 0, 0))

S['cuci-colon-histo.webp'] = dict(name='2421_Histology_of_the_Large_IntestineN.jpg', size=15, crop=(0, 0, 1125, 500), labels=[
    (320, 4, 450, 43, 'Orificios de\nlas glándulas', 'l'),
    (845, 5, 915, 19, 'Microvellosidades', 'c'),
    (948, 51, 1068, 86, 'El enterocito\nabsorbe agua', 'l'),
    (13, 129, 134, 147, 'Intestino grueso', 'l'),
    (302, 209, 425, 227, 'Glándula intestinal', 'r'),
    (948, 234, 1077, 269, 'La célula caliciforme\nsecreta moco', 'l'),
    (264, 405, 441, 426, 'Fibra muscular lisa', 'r'),
    (803, 427, 948, 445, 'Nódulo linfático', 'l'),
    (264, 445, 434, 460, 'Muscular de la mucosa', 'r'),
    (264, 470, 362, 484, 'Submucosa', 'r'),
], pad=(0, 0, 40, 0))

S['aguda-cdiff-colitis.webp'] = dict(name='OSC_Microbio_24_03_pseudocoli.jpg', size=20, labels=[
    (34, 189, 232, 207, 'microbiota normal', 'c'),
    (397, 341, 468, 355, 'moco', 'l'),
    (940, 344, 1139, 367, 'seudomembrana', 'l'),
    (700, 409, 841, 432, 'célula epitelial', 'l'),
    (540, 534, 771, 553, 'Clostridioides difficile', 'l', {'it': True}),
    (208, 974, 354, 993, 'eritrocito', 'l'),
    (509, 1182, 616, 1205, 'neutrófilo', 'l'),
    (715, 1216, 821, 1238, 'monocito', 'l'),
], pad=(0, 0, 40, 0))

S['cyclospora-ooquiste.webp'] = dict(name='OSC_Microbio_24_05_Cyclospor.jpg', size=22, labels=[
    (529, 205, 705, 245, 'C. cayetanensis', 'l', {'it': True}),
])

S['cronica-giardia.webp'] = dict(name='OSC_Microbio_05_01_giardia.jpg', crop=(0, 0, 995, 445))
S['aguda-cdiff.webp'] = dict(name='OSC_Microbio_04_04_Clostridia.jpg')
S['aguda-rotavirus.webp'] = dict(name='OSC_Microbio_24_04_Rotavirus.jpg')
S['aguda-vibrio.webp'] = dict(name='OSC_Microbio_11_06_VC.jpg')
S['aguda-salmonella.webp'] = dict(name='OSC_Microbio_24_03_Salmonella.jpg')
S['hpylori-mev.webp'] = dict(name='OSC_Microbio_04_02_Hpylori.jpg')

# ---------- Hígado, vía biliar y páncreas ----------
S['pruebas-lobulillo.webp'] = dict(name='2423_Microscopic_Anatomy_of_Liver.jpg', size=15, labels=[
    (339, 122, 437, 136, 'Vena central', 'l'),
    (338, 172, 431, 208, 'Tejido\nconjuntivo', 'l'),
    (340, 228, 399, 242, 'Lobulillos', 'l'),
    (6, 338, 136, 377, 'Vena interlobulillar\n(a la vena hepática)', 'l'),
    (598, 443, 677, 457, 'Sinusoides', 'l'),
    (6, 444, 104, 458, 'Vena central', 'l'),
    (6, 507, 105, 546, 'Placas de\nhepatocitos', 'l'),
    (597, 507, 703, 521, 'Vénula portal', 'l'),
    (597, 535, 718, 549, 'Arteriola portal', 'l'),
    (596, 561, 667, 575, 'Conducto biliar', 'l'),
    (276, 803, 409, 821, 'De la vena porta', 'c'),
], pad=(0, 0, 30, 0))

S['pruebas-ictericia.webp'] = dict(name='OSC_Microbio_24_04_HepJaundic.jpg', size=20, crop=(640, 180, 1293, 499), labels=[
    (975, 202, 1159, 225, 'signos de ictericia', 'l'),
], erase=[(974, 473, 1001, 496)])

S['virales-virus.webp'] = dict(name='OSC_Microbio_24_04_Hepatitis.jpg')

S['cirrosis-porta.webp'] = dict(name='2138_Hepatic_Portal_Vein_System.jpg', size=31, labels=[
    (18, 24, 264, 59, 'Porta hepática', 'r', {'bold': True}),
    (18, 82, 117, 118, 'Cística', 'r'),
    (18, 141, 218, 169, 'Vesícula biliar', 'r'),
    (1233, 167, 1437, 203, 'Gástrica derecha', 'l'),
    (1231, 276, 1362, 312, 'Esplénica', 'l', {'bold': True}),
    (17, 286, 378, 322, 'Mesentérica superior', 'r', {'bold': True}),
    (1232, 337, 1468, 373, 'Gastroepiploica', 'l'),
    (18, 355, 272, 383, 'Gastroomental', 'r'),
    (1233, 398, 1406, 426, 'Pancreática', 'l'),
    (19, 423, 366, 451, 'Pancreaticoduodenal', 'r'),
    (18, 492, 210, 520, 'Cólica media', 'r'),
    (1232, 553, 1567, 580, 'Mesentérica inferior', 'l', {'bold': True}),
    (19, 561, 187, 597, 'Cólica derecha', 'r'),
    (1233, 618, 1376, 646, 'Cólica izquierda', 'l'),
    (19, 629, 150, 657, 'Ileocólica', 'r'),
    (1232, 683, 1364, 719, 'Sigmoidea', 'l'),
    (19, 698, 164, 726, 'Intestinales', 'r'),
    (1232, 749, 1472, 785, 'Rectal superior', 'l'),
], pad=(80, 0, 40, 0))

S['litiasis-via-biliar.webp'] = dict(name='2425_Gallbladder.jpg', size=17, labels=[
    (6, 19, 157, 39, 'Conducto hepático izquierdo', 'r'),
    (6, 60, 171, 80, 'Conducto hepático derecho', 'r'),
    (6, 98, 106, 118, 'Conducto cístico', 'r'),
    (7, 226, 125, 242, 'Vesícula biliar:', 'l', {'bold': True}),
    (30, 261, 76, 281, 'Cuerpo', 'l'),
    (30, 296, 97, 311, 'Fondo', 'l'),
    (30, 331, 75, 347, 'Cuello', 'l'),
    (524, 479, 635, 524, 'Conducto\nhepático común', 'l'),
    (452, 600, 496, 616, 'Hígado', 'l'),
    (635, 583, 718, 623, 'Colédoco', 'l'),
], pad=(90, 0, 50, 0))

S['pancreas-anatomia.webp'] = dict(name='2424_Exocrine_and_Endocrine_Pancreas.jpg', size=16, labels=[
    (137, 2, 303, 18, 'Colédoco', 'l'),
    (409, 3, 550, 18, 'Conducto pancreático', 'l'),
    (520, 70, 614, 122, 'Cola del\npáncreas', 'l'),
    (397, 187, 468, 203, 'Lobulillos', 'l'),
    (428, 281, 607, 326, 'Las células acinares\nsecretan enzimas', 'l'),
    (58, 312, 220, 332, 'Cabeza del páncreas', 'l'),
    (5, 462, 144, 528, 'Las células de los\nislotes secretan\nhormonas', 'l'),
    (6, 743, 147, 759, 'Conducto pancreático', 'r'),
    (273, 807, 625, 827, 'Las células exocrinas secretan el jugo pancreático', 'c'),
], pad=(40, 0, 40, 0))


S['onco-pared.webp'] = dict(name='2402_Layers_of_the_Gastrointestinal_Tract.jpg', size=15, labels=[
    (609, 17, 647, 33, 'Vena', 'l'),
    (406, 71, 591, 116, 'Plexo submucoso\n(de Meissner)', 'l'),
    (960, 83, 1056, 103, 'Mesenterio', 'l'),
    (996, 139, 1052, 159, 'Arteria', 'l'),
    (367, 154, 472, 194, 'Glándulas en\nla submucosa', 'l'),
    (998, 196, 1051, 211, 'Nervio', 'l'),
    (129, 222, 245, 238, 'Submucosa', 'l', {'bold': True}),
    (3, 259, 157, 275, 'Glándula en la mucosa', 'l'),
    (2, 309, 123, 350, 'Conducto de una\nglándula externa', 'l'),
    (833, 383, 986, 403, 'Plexo mientérico', 'l'),
    (3, 417, 156, 437, 'Tejido linfático', 'l'),
    (747, 438, 821, 454, 'Serosa:', 'l', {'bold': True}),
    (3, 455, 65, 470, 'Luz', 'l'),
    (758, 463, 989, 479, 'Tejido conjuntivo laxo', 'l'),
    (759, 488, 853, 508, 'Epitelio', 'l'),
    (3, 509, 92, 525, 'Mucosa:', 'l', {'bold': True}),
    (15, 534, 110, 554, 'Epitelio', 'l'),
    (678, 534, 800, 549, 'Muscular:', 'l', {'bold': True}),
    (689, 558, 831, 574, 'Músculo circular', 'l'),
    (15, 559, 152, 579, 'Lámina propia', 'l'),
    (15, 584, 202, 600, 'Muscular de la mucosa', 'l'),
    (690, 584, 872, 604, 'Músculo longitudinal', 'l'),
], pad=(0, 0, 40, 0))

if __name__ == '__main__':
    for out, sp in S.items():
        sp = dict(sp)
        name = sp.pop('name')
        print(out, relabel(name, out, **sp))
