# Que el botón AnKing de la portada regrese a la portada (no a "Otros materiales") al salir de la página AnKing.
# Idempotente. Uso: python3 tools-anki/patch_anking_back.py [ruta/index.html del artefacto ...]
import sys,os
D=os.path.dirname(os.path.abspath(__file__))
files=[os.path.join(D,'..','site','index.html'),os.path.join(D,'..','site','app.html')]+sys.argv[1:]
R=[('const fs=window.__fromSem;current="mat:"+id;window.__fromOtr=!fs;','const fs=window.__fromSem,fh=window.__fromHome===id;current="mat:"+id;window.__fromOtr=!fs&&!fh;'),
('$("#vBack .lbl").textContent=fs?"Semestre":"Materiales";','$("#vBack .lbl").textContent=fs?"Semestre":fh?"Inicio":"Materiales";'),
('  /* abrir un material dentro del visor de la página */\n','  document.addEventListener("click",ev=>{if(ev.target.closest&&ev.target.closest("#akBtn"))window.__fromHome="anking"},true);\n  /* abrir un material dentro del visor de la página */\n'),
('if(W[h]!==undefined){hideViewer();','if(W[h]!==undefined){window.__fromHome=null;hideViewer();'),
('$("#vBack").addEventListener("click",()=>{const c=window.__fromCal,','$("#vBack").addEventListener("click",()=>{const fhm=window.__fromHome;window.__fromHome=null;const c=window.__fromCal,'),
('go(sm?"sem-"+sm:c?"calendario":o?"otros":"")','go(sm?"sem-"+sm:c?"calendario":fhm?"":o?"otros":"")')]
for f in files:
    s=open(f,encoding='utf-8').read()
    if '__fromHome' in s: print('ya está',f);continue
    for a,b in R:
        assert s.count(a)==1,(f,a[:40]);s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s);print('listo',f)
