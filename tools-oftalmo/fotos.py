"""Prepara las figuras libres (OpenStax A&P 2e y Microbiology, CC BY 4.0; varias fotos de CDC en dominio público)
para la guía de Oftalmología (5º): recorta, borra los rótulos en inglés y los vuelve a escribir en español.
Se evita la micrografía de retina «Regents of University of Michigan ©» (no es CC BY): de esa figura solo va el dibujo.

Uso: python3 tools-oftalmo/fotos.py
Originales (no se suben) en tools-oftalmo/orig/, bajados desde GitHub:
  git clone --filter=blob:none --no-checkout --depth 1 https://github.com/openstax/osbooks-anatomy-physiology
  git clone --filter=blob:none --no-checkout --depth 1 https://github.com/openstax/osbooks-microbiology
  git checkout HEAD -- media/<archivo>      (dentro de cada clon)
Salida: tools-oftalmo/img/*.webp (≤1000 px de ancho). Reutiliza relabel() de tools-gastro/fotos.py.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools-gastro'))
import fotos as G  # noqa: E402
G.ORIG = os.path.join(HERE, 'orig')
G.OUT = os.path.join(HERE, 'img')

S = {}

S['orbita-huesos.webp'] = dict(name='713_Bones_Forming_Orbit.jpg', size=19, labels=[
    (5, 24, 119, 40, 'Hueso frontal', 'l'),
    (770, 22, 961, 42, 'Agujero supraorbitario', 'l'),
    (4, 60, 184, 96, 'Reborde\nsupraorbitario', 'l', {'size': 18}),
    (4, 134, 143, 155, 'Esfenoides', 'l'),
    (770, 140, 873, 156, 'Hueso nasal', 'l'),
    (4, 177, 107, 197, 'Canal óptico', 'l'),
    (769, 169, 899, 185, 'Hueso lagrimal', 'l'),
    (770, 198, 896, 214, 'Etmoides', 'l'),
    (4, 220, 212, 240, 'Fisura orbitaria superior', 'l'),
    (769, 227, 902, 243, 'Fosa lagrimal', 'l'),
    (4, 289, 151, 310, 'Cigomático', 'l'),
    (770, 288, 894, 304, 'Palatino', 'l'),
    (770, 326, 947, 342, 'Agujero infraorbitario', 'l'),
    (158, 413, 222, 429, 'Maxilar', 'l'),
], pad=(0, 0, 50, 0))

S['lagrimal-via.webp'] = dict(name='OSC_Microbio_21_01_lacrimapp.jpg', size=19, labels=[
    (5, 3, 156, 26, 'glándula lagrimal', 'l'),
    (270, 54, 354, 103, 'canalículos\nlagrimales', 'l'),
    (503, 158, 633, 176, 'saco lagrimal', 'l'),
    (503, 324, 696, 343, 'conducto nasolagrimal', 'l'),
    (50, 338, 217, 362, 'puntos lagrimales', 'l'),
], pad=(0, 0, 30, 0))

S['globo-estructura.webp'] = dict(name='1413_Structure_of_the_Eye.jpg', size=32, labels=[
    (1706, 120, 1984, 155, 'Cavidad posterior', 'l', {'bold': True}),
    (1733, 162, 2025, 190, 'Cámara vítrea', 'l'),
    (1, 220, 253, 290, 'Músculo recto\nsuperior', 'l'),
    (1733, 249, 2075, 327, 'Seno venoso escleral\n(canal de Schlemm)', 'l'),
    (1, 339, 105, 368, 'Esclera', 'l'),
    (1733, 377, 2100, 414, 'Fibras zonulares', 'l'),
    (1, 451, 129, 479, 'Coroides', 'l'),
    (1735, 467, 1812, 495, 'Cristalino', 'l'),
    (1733, 528, 1854, 557, 'Córnea', 'l'),
    (3, 678, 253, 706, 'Fóvea central', 'l'),
    (1735, 652, 1813, 687, 'Pupila', 'l'),
    (1705, 733, 1966, 768, 'Cavidad anterior', 'l', {'bold': True}),
    (1705, 772, 2150, 812, '(contiene humor acuoso):', 'l'),
    (3, 561, 107, 589, 'Retina', 'l'),
    (1736, 591, 1781, 619, 'Iris', 'l'),
    (1735, 828, 2038, 856, 'Cámara posterior', 'l'),
    (1733, 870, 2019, 898, 'Cámara anterior', 'l'),
    (1, 833, 275, 872, 'Nervio óptico (II)', 'l'),
    (1, 951, 246, 1028, 'Arteria y vena\ncentral retiniana', 'l'),
    (1733, 944, 2100, 980, 'Fibras zonulares', 'l'),
    (1705, 1028, 1928, 1064, 'Cuerpo ciliar:', 'l', {'bold': True}),
    (1, 1069, 183, 1146, 'Papila óptica\n(punto ciego)', 'l'),
    (1735, 1070, 1978, 1106, 'Procesos ciliares', 'l'),
    (1735, 1112, 1965, 1147, 'Músculo ciliar', 'l'),
    (1, 1180, 228, 1250, 'Músculo recto\ninferior', 'l'),
], pad=(0, 0, 90, 0))

S['musculos-extraoculares.webp'] = dict(name='1412_Extraocular_Muscles.jpg', size=32, labels=[
    (250, 15, 519, 85, 'Músculo oblicuo\nsuperior', 'l'),
    (1097, 40, 1237, 67, 'Tróclea', 'l'),
    (1448, 43, 1589, 113, 'Recto\nsuperior', 'l'),
    (2101, 44, 2241, 71, 'Tróclea', 'l'),
    (1099, 109, 1368, 179, 'Tendón del\noblicuo superior', 'l'),
    (2102, 163, 2243, 241, 'Oblicuo\nsuperior', 'l'),
    (1099, 221, 1350, 291, 'Músculo recto\nsuperior', 'l'),
    (1099, 334, 1322, 403, 'Músculo recto\nlateral', 'l'),
    (1297, 483, 1520, 511, 'Recto lateral', 'c'),
    (2022, 483, 2241, 511, 'Recto medial', 'c'),
    (1414, 598, 1531, 675, 'Oblicuo\ninferior', 'c'),
    (1970, 598, 2083, 667, 'Recto\ninferior', 'l'),
    (38, 697, 271, 775, 'Anillo tendinoso\ncomún (de Zinn)', 'l'),
    (460, 697, 685, 767, 'Músculo recto\ninferior', 'l'),
    (845, 697, 1088, 767, 'Músculo oblicuo\ninferior', 'l'),
    (313, 820, 766, 856, 'Vista lateral del ojo derecho', 'c'),
    (1539, 820, 2011, 856, 'Vista anterior del ojo derecho', 'c'),
], pad=(0, 0, 40, 0))

S['parpado-orbita.webp'] = dict(name='1411_Eye_in_The_Orbit.jpg', size=30, labels=[
    (1380, 125, 1520, 160, 'Ceja', 'l'),
    (1378, 203, 1641, 273, 'Músculo orbicular\ndel ojo', 'l'),
    (1378, 332, 1675, 408, 'Músculo elevador del\npárpado superior', 'l'),
    (1380, 429, 1730, 464, 'Conjuntiva palpebral', 'l'),
    (1380, 509, 1547, 544, 'Pestañas', 'l'),
    (1378, 630, 1500, 659, 'Córnea', 'l'),
    (1378, 915, 1571, 951, 'Conjuntiva bulbar', 'l'),
], pad=(0, 0, 60, 0))

S['fotorreceptores.webp'] = dict(name='1414_Rods_and_Cones.jpg', size=16, labels=[
    (181, 132, 265, 171, 'Epitelio\npigmentario', 'l'),
    (181, 183, 323, 201, 'Melanina', 'l'),
    (181, 242, 328, 260, 'Cilio conector', 'l'),
    (120, 320, 224, 334, 'Bastones', 'r'),
    (120, 499, 231, 513, 'Núcleos', 'r'),
    (892, 183, 936, 197, 'Discos', 'l'),
    (891, 242, 997, 256, 'Mitocondrias', 'l'),
    (891, 355, 1022, 373, 'Aparato de Golgi', 'l'),
    (891, 398, 934, 412, 'Cono', 'l'),
    (892, 548, 981, 565, 'Célula bipolar', 'l'),
    (891, 729, 998, 747, 'Célula ganglionar', 'l'),
    (599, 927, 653, 941, 'LUZ', 'c'),
], crop=(0, 0, 1090, 948), pad=(0, 0, 40, 0))

S['via-visual-campos.webp'] = dict(name='1420_Optical_Fields.jpg', size=28, labels=[
    (439, 5, 683, 34, 'Campo visual izquierdo', 'r'),
    (811, 5, 1079, 41, 'Campo visual derecho', 'l'),
    (630, 113, 861, 141, 'Campo binocular', 'c'),
    (155, 306, 332, 383, 'Campo visual\ndel ojo izquierdo', 'r'),
    (1288, 306, 1471, 383, 'Campo visual\ndel ojo derecho', 'l'),
    (249, 546, 400, 574, 'Lado izquierdo', 'r'),
    (1103, 546, 1281, 582, 'Lado derecho', 'l'),
    (1238, 700, 1470, 736, 'Hipófisis', 'l'),
    (125, 785, 333, 821, 'Nervios ópticos', 'r'),
    (1257, 827, 1470, 862, 'Quiasma óptico', 'l'),
    (165, 955, 333, 995, 'Cintilla óptica', 'r'),
    (1197, 955, 1471, 1075, 'Núcleo\nsupraquiasmático\ndel hipotálamo', 'l'),
    (3, 1078, 333, 1147, 'Núcleo geniculado\nlateral del tálamo', 'r'),
    (199, 1364, 364, 1434, 'Corteza visual\nizquierda', 'l'),
    (1138, 1364, 1328, 1434, 'Corteza visual\nderecha', 'l'),
    (648, 1509, 846, 1537, 'Vista inferior', 'c'),
], pad=(0, 0, 60, 0))

S['hipofisis-quiasma.webp'] = dict(name='1614_Pituitary_Tumor-02.jpg', size=30, labels=[
    (966, 140, 1176, 176, 'Quiasma óptico', 'c'),
    (1228, 140, 1468, 176, 'Silla turca', 'c'),
    (1538, 140, 1750, 176, 'Quiasma óptico', 'c'),
    (1802, 140, 2035, 176, 'Silla turca', 'c'),
    (1134, 692, 1278, 781, 'Hipófisis\nnormal', 'c'),
    (1705, 692, 1853, 773, 'Tumor de\nhipófisis', 'c'),
])

S['reflejo-pupilar.webp'] = dict(name='1509_Pupillary_Reflex_Pathways.jpg', size=29, labels=[
    (1041, 69, 1184, 138, 'Núcleo\npretectal', 'l'),
    (1796, 75, 2127, 235, 'Los potenciales del\nojo derecho llegan\na ambos núcleos\npretectales.', 'l'),
    (736, 202, 928, 279, 'Nervios\noculomotores (III)', 'l'),
    (548, 322, 667, 400, 'Ganglios\nciliares', 'l'),
    (320, 564, 607, 663, 'Se ilumina solo\nel ojo derecho.', 'l'),
    (1796, 422, 2127, 749, 'Los núcleos pretectales\nestimulan los dos\nnúcleos de\nEdinger-Westphal,\naunque la luz solo\nllegó al ojo derecho.', 'l'),
    (1298, 684, 1749, 980, 'Ambos Edinger-Westphal\nmandan potenciales por\nlos dos nervios\noculomotores y se\ncontraen ambas pupilas.', 'l'),
], pad=(0, 0, 90, 0))

S['queratitis-acanthamoeba.webp'] = dict(name='OSC_Microbio_21_05_acanthamoe.jpg', size=24, labels=[
    (60, 369, 310, 392, 'Quiste', 'c'),
    (440, 369, 790, 392, 'Trofozoíto', 'c'),
])

# Fotos sin texto: solo se recortan / se pasan a WebP
S['conjuntivitis-ojo.webp'] = dict(name='OSC_Microbio_21_01_ConjBleph.jpg', crop=(0, 0, 381, 254))
S['blefaritis.webp'] = dict(name='OSC_Microbio_21_01_ConjBleph.jpg', crop=(381, 0, 842, 254))
S['queratitis-cornea.webp'] = dict(name='OSC_Microbio_21_01_ConjBleph.jpg', crop=(842, 0, 1300, 254))
S['conjuntivitis-bacteriana.webp'] = dict(name='OSC_Microbio_21_02_bactconj.jpg')
S['oftalmia-neonatal.webp'] = dict(name='OSC_Microbio_21_02_neonatorum.jpg')
S['tracoma-triquiasis.webp'] = dict(name='OSC_Microbio_21_02_trichiasis.jpg')
S['orbitopatia-graves.webp'] = dict(name='OSC_Microbio_19_02_exophth.jpg')
S['snellen.webp'] = dict(name='1606_Snellen_Chart-02.jpg', width=700)

if __name__ == '__main__':
    for out, sp in S.items():
        sp = dict(sp)
        name = sp.pop('name')
        print(out, G.relabel(name, out, **sp))
