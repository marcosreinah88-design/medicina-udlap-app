/* cel: dentro de las guías, deja espacio al final para que los botones flotantes (Anki, Casos clínicos) no tapen lo último (tools-movil) */
(function(){
  var CSS="#movil-sp{display:none;height:88px}@media (max-width:560px){#movil-sp{display:block}}";
  function fix(f){
    var d;try{d=f.contentDocument}catch(e){return}
    if(!d||!d.body||d.__movil)return;d.__movil=1;
    try{
      var st=d.createElement("style");st.textContent=CSS;(d.head||d.body).appendChild(st);
      var add=function(){
        if(d.getElementById("movil-sp")||!d.querySelector(".ak-fab,.cc-fab"))return;
        var v=d.defaultView,cs=v&&v.getComputedStyle(d.body);
        if(!cs||cs.display!=="block")return;
        var s=d.createElement("div");s.id="movil-sp";s.setAttribute("aria-hidden","true");d.body.appendChild(s)};
      add();setTimeout(add,1500);setTimeout(add,5000);
      watch(d);
    }catch(e){}
  }
  function hook(f){f.addEventListener("load",function(){fix(f)});try{if(f.contentDocument&&f.contentDocument.readyState==="complete")fix(f)}catch(e){}}
  function watch(root){
    try{
      [].forEach.call(root.querySelectorAll("iframe"),hook);
      new MutationObserver(function(ms){ms.forEach(function(m){[].forEach.call(m.addedNodes,function(n){
        if(n.tagName==="IFRAME")hook(n);else if(n.querySelectorAll)[].forEach.call(n.querySelectorAll("iframe"),hook)})})})
        .observe(root.documentElement||root,{childList:true,subtree:true});
    }catch(e){}
  }
  var fr=document.getElementById("frames");if(fr)watch(document);
})();
