#!/usr/bin/env python3
"""Pasa la portada a 6º semestre: SEM_ACTUAL, CURSO (materias del calendario), ACTUALES (plan de estudios)
y textos que decían "5º semestre". Sirve para site/index.html, site/app.html, site/estudio.js y la copia del artefacto. Idempotente."""
import sys
R=[
 ('const SEM_ACTUAL=5; /* semestre que cursa Marcos ahora */','const SEM_ACTUAL=6; /* semestre que cursa Marcos ahora */'),
 ('/* Materias que Marcos está cursando (plan Médico Cirujano UDLAP, 5º semestre).','/* Materias que Marcos está cursando (plan Médico Cirujano UDLAP, 6º semestre).'),
 ('''const CURSO={sem:5,materias:[
  {n:"Bioética en Ciencias de la Salud"},{n:"Psiquiatría",g:"psiquiatria"},{n:"Gastroenterología",g:"gastro"},{n:"Cirugía",g:"cirugia"},
  {n:"Oftalmología",g:"oftalmo"},{n:"Otorrinolaringología",g:"otorrino"},{n:"Campos Clínicos I"},{n:"Casos Clínicos I"},{n:"Temas Selectos I"}]};''',
  '''const CURSO={sem:6,materias:[
  {n:"Salud Pública y Epidemiología en Ciencias de la Salud",g:"salud-publica"},{n:"Temas Selectos II"},{n:"Neurología"},{n:"Gastrocirugía"},
  {n:"Obstetricia"},{n:"Dermatología"},{n:"Nefrología"},{n:"Campos Clínicos II"},{n:"Casos Clínicos II"}]};'''),
 ('/* lo que Marcos cursa ahora (otoño 2026), según su portal UDLAP */\n  const ACTUALES=["Psiquiatría","Gastroenterología","Cirugía","Oftalmología","Otorrinolaringología","Campos Clínicos III"];',
  '/* lo que Marcos cursa ahora (6º semestre, primavera 2027) */\n  const ACTUALES=["Salud Pública y Epidemiología en Ciencias de la Salud","Temas Selectos II","Neurología","Gastrocirugía","Obstetricia","Dermatología","Nefrología","Campos Clínicos II","Casos Clínicos II"];'),
 ('<span class="h" id="cfSemLbl">5º semestre</span>','<span class="h" id="cfSemLbl">6º semestre</span>'),
 ('isSem(it)?"5º semestre":""','isSem(it)?(typeof CURSO!=="undefined"?CURSO.sem:6)+"º semestre":""'),
 ('typeof CURSO!=="undefined"?CURSO.sem:5','typeof CURSO!=="undefined"?CURSO.sem:6'),
 ('preparas a un estudiante de 5º semestre de Médico Cirujano','preparas a un estudiante de ${typeof CURSO!=="undefined"?CURSO.sem:6}º semestre de Médico Cirujano'),
]
for p in sys.argv[1:]:
    s=open(p,encoding='utf-8').read();n=0
    for a,b in R:
        if a in s: s=s.replace(a,b);n+=1
    open(p,'w',encoding='utf-8').write(s);print(p,n,'cambios')
