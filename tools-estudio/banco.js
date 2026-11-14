// Arma site/estudio-banco.json: tarjetas y preguntas sacadas de las guías de cada semestre,
// para el repaso con tarjetas y el modo examen de la sección "Estudio".
// Uso: node tools-estudio/banco.js   (correrlo otra vez cuando se agregue o cambie una guía)
const fs=require('fs'),path=require('path'),crypto=require('crypto'),extraer=require('./extraer.js');
const site=path.join(__dirname,'..','site');
// guía → archivo y materia (la materia es la del plan UDLAP con que se cruza el calendario)
const GUIAS=[
  ['histologia','s1/guias/histologia.html','Histología',1],
  ['bioquimica','s1/guias/bioquimica.html','Bioquímica Clínica',1],
  ['anatomofisiologia','s1/guias/anatomofisiologia.html','Anatomofisiología',1],
  ['embriologia-genetica','s1/guias/embriologia-genetica.html','Embriología y Genética',1],
  ['simulacion-i','s1/guias/simulacion-i.html','Simulación',1],
  ['anatomia-dental','s1/guias/anatomia-dental.html','Anatomía Dental',1],
  ['fisiologia','s2/guias/fisiologia.html','Fisiología',2],
  ['biologia-celular','s2/guias/biologia-celular.html','Biología Celular y Molecular',2],
  ['anatomia-humana-i','s2/guias/anatomia-humana-i.html','Anatomía Humana I',2],
  ['simulacion-ii','s2/guias/simulacion-ii.html','Simulación',2],
  ['farmacologia','s3/farmacologia/index.html','Farmacología',3],
  ['anatomia','s3/anatomia/index.html','Anatomía',3],
  ['hematologia','s4/apps/hematologia.html','Hematología',4],
  ['farmacologia-ii','s4/apps/farmacologia-ii.html','Farmacología',4],
  ['inmunologia','s4/apps/inmunologia.html','Inmunología',4],
  ['simulacion-iv','s4/apps/simulacion-iv.html','Simulación',4],
  ['nutricion','s4/apps/nutricion.html','Nutrición',4],
  ['cirugia-principios','s4/apps/cirugia.html','Principios de cirugía',4],
  ['psiquiatria','s5/psiquiatria/index.html','Psiquiatría',5],
  ['gastro','s5/gastro/index.html','Gastroenterología',5],
  ['esofago','s5/esofago/index.html','Gastroenterología',5],
  ['hepatobiliar','s5/hepatobiliar/index.html','Gastroenterología',5],
  ['quiz-hepatico','s5/quiz-hepatico/index.html','Gastroenterología',5],
  ['cirugia','s5/cirugia/index.html','Cirugía',5],
  ['oftalmo','s5/oftalmo/index.html','Oftalmología',5],
  ['otorrino','s5/otorrino/index.html','Otorrinolaringología',5],
  ['infectologia','s6/artefactos/infectologia.html','Infectología',6],
  ['salud-publica','s6/artefactos/salud-publica.html','Salud Pública',6],
];
const id=(p,s)=>p+crypto.createHash('sha1').update(s).digest('base64url').slice(0,9);
const out={v:1,g:[],q:[],c:[]},seen=new Set();
for(const [gid,file,mat,sem] of GUIAS){
  const f=path.join(site,file);if(!fs.existsSync(f)){console.log('falta',file);continue}
  const r=extraer(f),gi=out.g.length;let nq=0,nc=0;
  out.g.push([gid,mat,sem]);
  for(const x of r.q){const k='q'+x.q+'|'+x.o.join('|');if(seen.has(k)||x.o.length<2||x.a<0||x.a>=x.o.length)continue;seen.add(k);out.q.push([id('q',k),gi,x.t||'',x.q,x.o,x.a,x.e||'']);nq++}
  for(const x of r.c){const k='c'+x.f+'|'+x.b;if(seen.has(k)||x.b.length>700)continue;seen.add(k);out.c.push([id('c',k),gi,x.t||'',x.f,x.b]);nc++}
  console.log(gid.padEnd(20),'preguntas',String(nq).padStart(4),'tarjetas',String(nc).padStart(4));
}
fs.writeFileSync(path.join(site,'estudio-banco.json'),JSON.stringify(out));
console.log('total',out.q.length,'preguntas,',out.c.length,'tarjetas,',Math.round(fs.statSync(path.join(site,'estudio-banco.json')).size/1024),'KB');
