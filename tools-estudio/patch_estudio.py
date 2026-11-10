# Conecta la sección Estudio (site/estudio.js) a la página: ruta #estudio, script y avisos "repasa hoy".
# Uso: python3 tools-estudio/patch_estudio.py site/index.html site/app.html   (se puede correr dos veces sin duplicar)
import sys
R=[
 ('const W={calendario:window.Cal,calificaciones:window.Grades,','const W={calendario:window.Cal,calificaciones:window.Grades,estudio:window.Estudio,'),
 ('<script src="sync.js"></script>','<script src="estudio.js"></script>\n<script src="sync.js"></script>'),
 # avisos: "repasa hoy" 5, 3 y 2 días antes de cada examen (además de los de 7 días y 1 día que ya había)
 ('add1("ex1:"+e.id+":"+e.date,at(n1,20),"Mañana es tu examen de "+e.name,"Duerme bien. Repaso general hoy y a descansar.");}',
  'add1("ex1:"+e.id+":"+e.date,at(n1,20),"Mañana es tu examen de "+e.name,"Duerme bien. Repaso general hoy y a descansar.");\n'
  '      for(const k of [5,3,2]){const mt=window.Estudio&&Estudio.examMat?Estudio.examMat(e):"";add1("rep"+k+":"+e.id+":"+e.date,at(ymd(add(parse(e.date),-k)),19),"Repasa hoy: "+e.name+" en "+k+" días","Haz tus tarjetas pendientes"+(mt?" de "+mt:"")+" y un examen de práctica de 10 preguntas en Estudio.","estudio")}}'),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    for a,b in R:
        if b in s: continue
        n=s.count(a)
        if n!=1: sys.exit(f"{f}: {n} veces: {a[:70]}")
        s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s);print("ok",f)
