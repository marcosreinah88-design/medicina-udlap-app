/*xmat*/window.XMAT=(()=>{
/* Íconos, etiqueta de tipo y grupos del Material extra (fuente: tools-xmat/xmat.js).
   Íconos propios (SVG de trazo, viewBox 48). Lo usan la portada (Otros materiales, Material extra de
   cada semestre, buscador) y la página de 5º. Los grupos solo juntan la vista: cada material conserva
   su id, su página y su progreso guardado. */
const T={
  examen:{l:"Examen",c:"#00573c",svg:`<rect x="11" y="8" width="26" height="34" rx="3"/><path d="M19 8V6h10v2a2 2 0 0 1-2 2h-6a2 2 0 0 1-2-2z"/><path d="M16 20l2.5 2.5L23 18M27 20h5M16 30l2.5 2.5L23 28M27 30h5"/>`},
  articulos:{l:"Examen por artículo",c:"#1e6a4e",svg:`<path d="M16 5h14l8 8v24H16z"/><path d="M30 5v8h8"/><path d="M11 11v31h21"/><path d="M21 22l3 3 6-6M21 30h11"/>`},
  simulacro:{l:"Simulacro",c:"#c4501a",svg:`<circle cx="24" cy="27" r="14"/><path d="M24 27l6-6M20 5h8M24 5v8M36 13l3-3"/><path d="M24 17v2M14 27h2M32 27h2M24 35v2"/>`},
  simulador:{l:"Simulador",c:"#0f4a3f",svg:`<rect x="5" y="8" width="38" height="26" rx="3"/><path d="M9 22h7l3-7 5 13 3-8 2 2h10"/><path d="M18 42h12M24 34v8"/>`},
  repaso:{l:"Repaso",c:"#2c6a4c",svg:`<path d="M24 12c-5-4-12-5-18-4v28c6-1 13 0 18 4 5-4 12-5 18-4V8c-6-1-13 0-18 4z"/><path d="M24 12v28"/><path d="M11 16h7M11 22h7M11 28h5M30 16h7M30 22h7M30 28h5"/>`},
  juego:{l:"Juego",c:"#b5562a",svg:`<path d="M14 15h20a9 9 0 0 1 9 9v7a4 4 0 0 1-7 2.6L31 29H17l-5 4.6A4 4 0 0 1 5 31v-7a9 9 0 0 1 9-9z"/><path d="M15 20v7M11.5 23.5h7"/><circle cx="31" cy="21.5" r="1.4" fill="currentColor"/><circle cx="35" cy="25.5" r="1.4" fill="currentColor"/>`},
  quiz:{l:"Quiz",c:"#9a5a00",svg:`<path d="M8 8h32a3 3 0 0 1 3 3v19a3 3 0 0 1-3 3H23l-9 8v-8H8a3 3 0 0 1-3-3V11a3 3 0 0 1 3-3z"/><path d="M19.5 16.5a4.5 4.5 0 1 1 6 4.2c-1.2.5-1.5 1.3-1.5 2.8"/><circle cx="24" cy="27.5" r="1.4" fill="currentColor"/>`},
  tarjetas:{l:"Tarjetas",c:"#2a62b8",svg:`<rect x="14" y="7" width="27" height="20" rx="3" transform="rotate(8 27 17)"/><rect x="7" y="17" width="29" height="22" rx="3"/><path d="M13 25h17M13 31h11"/>`},
  calculadora:{l:"Calculadora",c:"#4f7a28",svg:`<rect x="11" y="5" width="26" height="38" rx="3"/><rect x="15" y="9" width="18" height="8" rx="1.5"/><circle cx="18" cy="24" r="1.4" fill="currentColor"/><circle cx="24" cy="24" r="1.4" fill="currentColor"/><circle cx="30" cy="24" r="1.4" fill="currentColor"/><circle cx="18" cy="31" r="1.4" fill="currentColor"/><circle cx="24" cy="31" r="1.4" fill="currentColor"/><circle cx="30" cy="31" r="1.4" fill="currentColor"/><circle cx="18" cy="38" r="1.4" fill="currentColor"/><path d="M24 38h6"/>`},
  diapositivas:{l:"Diapositivas",c:"#d9561b",svg:`<rect x="6" y="8" width="36" height="24" rx="3"/><path d="M24 32v8M16 42h16M12 15h14M12 21h20M12 26h10"/>`},
  interactivo:{l:"Guía interactiva",c:"#c62828",svg:`<rect x="8" y="6" width="26" height="36" rx="3"/><path d="M14 14h14M14 20h10"/><path d="M27 27l12 5-5 2 4 5-2 2-4-5-2 5z"/>`},
  cto:{l:"Manual CTO",c:"#00543c",svg:`<path d="M10 40V10a4 4 0 0 1 4-4h24v30H14a4 4 0 0 0-4 4zm0 0a4 4 0 0 0 4 4h24v-8"/><path d="M18 14h12M18 20h8"/>`},
};
/* tipo de cada material que vive dentro de la página (ids de 5º y de Otros materiales) */
const ID={
  "esofago":"repaso","hepatobiliar":"repaso","duelo":"juego","quiz-hepatico":"quiz",
  "examen-bloque-iii":"examen","examenes-por-articulo":"articulos","simulacros-bloque-iii":"simulacro",
  "simulador-casos-gastro":"simulador",
  "bioetica":"tarjetas","campos-clinicos-i":"tarjetas","casos-clinicos-i":"tarjetas",
  "anki-ecosofia":"tarjetas","anki-examen-basicos":"tarjetas","anki-bioetica":"tarjetas","anki-campos-clinicos-i":"tarjetas",
  "anki-casos-clinicos-i":"tarjetas","anki-casos-clinicos-ii":"tarjetas","enarm":"tarjetas","anking":"tarjetas",
  "triage":"interactivo","signos":"interactivo","triage-clase":"diapositivas","svb":"diapositivas","geb":"calculadora",
};
/* materiales que agregue la persona: tipo por el título */
const RE=[[/simulador|guardia/,"simulador"],[/simulacro/,"simulacro"],[/examen|parcial/,"examen"],[/anki|tarjeta|flashcard/,"tarjetas"],
  [/quiz|trivia/,"quiz"],[/duelo|juego|jeopardy/,"juego"],[/repaso|resumen/,"repaso"],[/calculadora/,"calculadora"]];
const norm=s=>String(s||"").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"");
/* strict=true: solo por id (para el buscador, donde «Repaso de Cirugía» es una guía, no material extra) */
function tipo(it,strict){if(ID[it.id])return ID[it.id];if(strict)return null;const t=norm(it.title);for(const [re,k] of RE)if(re.test(t))return k;return null}
function info(it,strict){const k=tipo(it,strict);return k?{k,...T[k]}:null}
/* materiales parecidos que se muestran juntos en una sola tarjeta (el orden de ids = orden adentro) */
const GR=[
  {id:"g-examenes-b3",l:"Exámenes",t:"examen",subject:"Gastroenterología",title:"Exámenes y simulacros del Bloque III",
   desc:"Todo para practicar el 3er parcial de Gastro: examen de práctica, un examen por cada artículo y simulacros revueltos como el parcial.",
   ids:["examen-bloque-iii","examenes-por-articulo","simulacros-bloque-iii"]},
  {id:"g-repasos-gastro",l:"Repasos",t:"repaso",subject:"Gastroenterología",title:"Repasos de Gastro",
   desc:"Los artículos de clase resumidos, con tarjetas, preguntas y algoritmos.",ids:["esofago","hepatobiliar"]},
  {id:"g-juegos-gastro",l:"Juegos",t:"juego",subject:"Gastroenterología",title:"Juego y quiz de Gastro",
   desc:"Para repasar jugando: el tablero por equipos y el quiz contrarreloj.",ids:["duelo","quiz-hepatico"]},
  {id:"g-anki",l:"Tarjetas",t:"tarjetas",subject:"Tarjetas de Anki",title:"Tus tarjetas de Anki",
   desc:"Tus tarjetas revisadas y corregidas de las materias que no tienen guía.",
   ids:["bioetica","campos-clinicos-i","casos-clinicos-i","anki-ecosofia","anki-examen-basicos","anki-bioetica","anki-campos-clinicos-i","anki-casos-clinicos-i","anki-casos-clinicos-ii","enarm","anking"]},
  {id:"g-triage",l:"Urgencias",t:"interactivo",subject:"Urgencias",title:"Triage",
   desc:"La guía interactiva y la clase en diapositivas.",ids:["triage","triage-clase"]},
];
const SHORT={"esofago":"Esófago y Estómago","hepatobiliar":"Hepatobiliar · Bloque III","examen-bloque-iii":"Examen de práctica",
  "examenes-por-articulo":"Exámenes por artículo","simulacros-bloque-iii":"Simulacros","duelo":"Duelo Gastro","quiz-hepatico":"Quiz de pruebas hepáticas",
  "triage":"Triage en urgencias","triage-clase":"Clase: qué es y cómo se realiza","anking":"AnKing en español","enarm":"ENARM"};
const short=it=>SHORT[it.id]||String(it.title).replace(/\s*·\s*(tus\s+)?tarjetas(\s+de\s+anki)?\s*$/i,"");
/* junta la lista: [{it}] o [{grp,items}] en el lugar del primero de cada grupo; un grupo con 1 solo queda suelto */
function group(list){
  const out=[],at=new Map();
  for(const it of list){
    const g=GR.find(g=>g.ids.includes(it.id));
    if(!g){out.push({it});continue}
    if(!at.has(g.id)){at.set(g.id,out.length);out.push({grp:g,items:[]})}
    out[at.get(g.id)].items.push(it);
  }
  return out.map(e=>e.grp&&e.items.length===1?{it:e.items[0]}:e).map(e=>{if(e.grp)e.items.sort((a,b)=>e.grp.ids.indexOf(a.id)-e.grp.ids.indexOf(b.id));return e});
}
const svg=(s,cls)=>`<svg${cls?` class="${cls}"`:""} viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${s}</svg>`;
/* etiqueta para el buscador de la portada */
function badge(g){const I=info(g,true);return I?`<span class="xmat-b" style="--xc:${I.c}">${svg(I.svg)}${I.l} · Material extra</span>`:""}
return {T,ID,tipo,info,GR,group,short,svg,badge,norm};
})();
