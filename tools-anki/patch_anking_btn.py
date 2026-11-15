# Pone el botón "AnKing" en la portada (junto a Calificaciones); abre x/anking vía #mat-anking.
# Idempotente. Uso: python3 tools-anki/patch_anking_btn.py <ruta/al/index.html del artefacto ...>
import os,sys
HERE=os.path.dirname(os.path.abspath(__file__)); SITE=os.environ.get('SITE') or os.path.join(HERE,'..','site')
BTN=('  <a class="theme" id="akBtn" href="#mat-anking" title="AnKing en español"><svg viewBox="0 0 24 24" aria-hidden="true">'
     '<rect x="3" y="6.5" width="14" height="11" rx="2"/><path d="M7 3.5h12a2 2 0 0 1 2 2V15M7 11h6"/></svg><span>AnKing</span></a>\n')
CSS0='#themeBtn span,#grBtn span,#bbBtn span{display:none}#themeBtn,#grBtn,#bbBtn,#cfgBtn{padding:7px}'
CSS1='#themeBtn span,#grBtn span,#bbBtn span,#akBtn span{display:none}#themeBtn,#grBtn,#bbBtn,#akBtn,#cfgBtn{padding:7px}.topbtns{gap:5px}'
# Solo para el artefacto: en la app AnKing vive dentro de Estudio (sin botón ni tarjeta aparte).
for p in sys.argv[1:]:
    s=open(p,encoding='utf-8').read()
    if 'id="akBtn"' in s: print('ya está',p); continue
    i=s.index('<a class="theme" id="grBtn"'); j=s.index('</a>\n',i)+5
    s=s[:j]+BTN+s[j:]
    assert CSS0 in s, p
    s=s.replace(CSS0,CSS1,1)
    open(p,'w',encoding='utf-8').write(s); print('listo',p)
