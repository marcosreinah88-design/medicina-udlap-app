# Reduce las imágenes de arranque a 256 colores (con tramado) para que no pesen tanto.
import glob,os
from PIL import Image
d=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site','img','arranque')
for f in glob.glob(os.path.join(d,'*.png')):
    Image.open(f).convert('RGB').quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.FLOYDSTEINBERG).save(f,optimize=True)
