/* La corona abre Plan de Volumen: en la Mac, la app descargada (la app de Medicina la reconoce); en el cel, su versión instalable */
(()=>{
  const fix=()=>document.querySelectorAll('a.crownA').forEach(a=>{a.href="https://marcosreinah88-design.github.io/plan-volumen/"});
  if(document.readyState==="loading")addEventListener("DOMContentLoaded",fix);else fix();
})();
