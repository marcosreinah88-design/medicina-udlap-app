"""Memoria de progreso del simulador de casos (pedido del usuario, 28 nov 2026).

Por caso guarda: intentos (n), intentos sin errores (a), último puntaje (l), racha sin errores (r),
pasos fallados en el último intento (f) y cuándo (u). Estados: sin contestar / fallado / dominado
(dominado = el último intento sin errores). «Práctica inteligente» elige casos con muestreo ponderado:
los fallados pesan mucho más que los dominados, y un caso fallado vuelve a salir unos pacientes después
en el mismo turno. Todo va en la misma llave de localStorage (sim-gastro-final-v1), que site/sync.js
ya sincroniza entre Mac y cel; sync.js junta esta llave caso por caso.
"""

JS = r"""if (!mem.p) mem.p = {};
for (const k in mem.best) if (!mem.p[k]) mem.p[k] = {n:1, a:mem.best[k] >= 85 ? 1 : 0, l:mem.best[k], r:mem.best[k] >= 85 ? 1 : 0, u:0};
const limpiar = () => { if (mem.z) for (const k in mem.p) if ((mem.p[k].u || 0) < mem.z) { delete mem.p[k]; delete mem.best[k]; } };
limpiar();
/* la app sincroniza desde la página principal: si cambia la llave, se vuelve a leer */
addEventListener('storage', e => {
  if (e.key !== KEY) return;
  try { const m = JSON.parse(e.newValue || 'null'); if (m && m.best) { mem = Object.assign({best:{}, p:{}, snd:true}, m); limpiar(); if (S.view === 'home') render(); else topStat(); } } catch(err) {}
});
const est = id => { const p = mem.p[id]; return !p ? 'nuevo' : p.l >= 85 ? 'dom' : 'fal'; };
const EST = {nuevo:'Sin contestar', fal:'Fallados', dom:'Dominados'};
function registrar(id, sc, fallos) {
  const p = mem.p[id] || (mem.p[id] = {n:0, a:0, l:null, r:0, u:0});
  p.n++; if (sc >= 85) { p.a++; p.r++; } else p.r = 0;
  p.l = sc; p.f = fallos; p.u = Date.now();
  mem.best[id] = mem.best[id] == null ? sc : Math.max(mem.best[id], sc);
  save();
}
/* peso para la práctica: fallados ≫ nuevos > dominados (menos entre más racha; un poco más si hace mucho) */
function peso(id) {
  const p = mem.p[id]; if (!p) return 3;
  if (p.l < 85) return 6 + Math.min(4, p.n - p.a);
  return Math.max(.25, 1.5 / (1 + p.r)) * (Date.now() - (p.u || 0) > 7 * 864e5 ? 2 : 1);
}
/* muestreo ponderado sin reemplazo (Efraimidis-Spirakis) */
function practica(list, n) {
  return list.map(c => ({id:c.id, k:Math.pow(Math.random(), 1 / peso(c.id))})).sort((a, b) => b.k - a.k).slice(0, n || list.length).map(x => x.id);
}
function tagEst(id) {
  const p = mem.p[id], e = est(id);
  const tt = p ? ` title="${p.n} ${p.n === 1 ? 'intento' : 'intentos'}, ${p.a} sin errores"` : '';
  return e === 'nuevo' ? '<span class="score-tag s-no">Nuevo</span>'
    : e === 'dom' ? `<span class="score-tag s-hi"${tt}>Dominado${p.r > 1 ? ' ×' + p.r : ''}</span>`
    : `<span class="score-tag s-lo"${tt}>Fallado · ${p.l}</span>`;
}
"""

REPL = [
    # estado guardado + funciones
    ("let mem = {best:{}, snd:true};", "let mem = {best:{}, p:{}, snd:true};"),
    ("const save = () => { try { localStorage.setItem(KEY, JSON.stringify(mem)); } catch(e) {} };\n",
     "const save = () => { try { localStorage.setItem(KEY, JSON.stringify(mem)); } catch(e) {} };\n" + JS),
    ("f:{b:'all', tema:'all', dif:'all'}", "f:{b:'all', tema:'all', dif:'all', e:'all'}"),
    # barra superior
    ("  const done = Object.keys(mem.best).filter(k => BYID[k]).length;\n"
     "  document.getElementById('top-stat').textContent = `${done} de ${CASOS.length} casos atendidos`;",
     "  const done = Object.keys(mem.p).filter(k => BYID[k]).length, dom = CASOS.filter(c => est(c.id) === 'dom').length;\n"
     "  document.getElementById('top-stat').textContent = `${done} de ${CASOS.length} contestados · ${dom} dominados`;"),
    # censo: contadores y filtro por estado
    ("  const list = filtered();\n"
     "  const done = list.filter(c => mem.best[c.id] != null);\n"
     "  const avg = done.length ? Math.round(done.reduce((a, c) => a + mem.best[c.id], 0) / done.length) : null;\n"
     "  const weak = list.filter(c => mem.best[c.id] != null && mem.best[c.id] < 70);\n",
     "  const all = filtered();\n"
     "  const cnt = {nuevo:0, fal:0, dom:0}; all.forEach(c => cnt[est(c.id)]++);\n"
     "  const list = S.f.e === 'all' ? all : all.filter(c => est(c.id) === S.f.e);\n"
     "  const weak = all.filter(c => est(c.id) === 'fal');\n"
     "  const echip = (k, lab) => `<button class=\"chip\" data-e=\"${k}\" aria-pressed=\"${S.f.e === k}\">${esc(lab)}${k === 'all' ? '' : ` <b style=\"font-family:JetBrains Mono,monospace\">${cnt[k]}</b>`}</button>`;\n"),
    ("      <div class=\"go-row\">\n",
     "      <div class=\"flabel\" style=\"margin-top:16px\">Mi progreso</div>\n"
     "      <div class=\"chips\" id=\"fe\">${echip('all', 'Todos')}${echip('nuevo', EST.nuevo)}${echip('fal', EST.fal)}${echip('dom', EST.dom)}</div>\n"
     "      <div class=\"go-row\">\n"),
    ("        <button class=\"btn btn-ghost\" id=\"weak\" ${weak.length ? '' : 'disabled'}>Repasar fallados (${weak.length})</button>",
     "        <button class=\"btn btn-ghost\" id=\"smart\" ${all.length ? '' : 'disabled'} title=\"Te pone más seguido los casos que fallas; los dominados salen menos\">Práctica inteligente</button>\n"
     "        <button class=\"btn btn-ghost\" id=\"weak\" ${weak.length ? '' : 'disabled'}>Repasar fallados (${weak.length})</button>"),
    ("        <div class=\"stat\"><b>${list.length}</b><span>casos con este filtro</span></div>\n"
     "        <div class=\"stat\"><b>${done.length}</b><span>ya atendidos</span></div>\n"
     "        <div class=\"stat\"><b>${avg == null ? '—' : avg}</b><span>promedio de puntos</span></div>",
     "        <div class=\"stat\"><b>${cnt.nuevo}</b><span>sin contestar</span></div>\n"
     "        <div class=\"stat\"><b>${cnt.fal}</b><span>fallados</span></div>\n"
     "        <div class=\"stat\"><b>${cnt.dom}</b><span>dominados</span></div>"),
    ("        <span class=\"score-tag ${cls(s)}\">${s == null ? 'Nuevo' : s + ' pts'}</span>",
     "        ${tagEst(c.id)}"),
    ("'<div class=\"empty\">No hay casos con este filtro.</div>'",
     "`<div class=\"empty\">${S.f.e === 'all' ? 'No hay casos con este filtro.' : 'No tienes casos ' + EST[S.f.e].toLowerCase() + ' con este filtro.'}</div>`"),
    ("    <p style=\"color:var(--mute);font-size:13.5px;margin-top:18px\">68 casos escritos a partir de los artículos troncales de los tres bloques. Lo marcado con † es conocimiento general que no viene en el artículo. Tu progreso se guarda solo en este navegador.</p>",
     "    <p style=\"color:var(--mute);font-size:13.5px;margin-top:18px\">${CASOS.length} casos escritos a partir de los artículos troncales de los tres bloques y de guías reconocidas. Lo marcado con † es conocimiento general que no viene en el artículo. Tu progreso (contestados, fallados y dominados) se guarda en este aparato; en la app se sincroniza entre Mac y cel.</p>\n"
     "    ${Object.keys(mem.p).length ? '<button class=\"btn btn-plain\" id=\"reset\" style=\"margin-top:6px\">Reiniciar progreso</button>' : ''}"),
    ("  document.getElementById('weak').onclick = () => startShift(shuffle(weak.map(c => c.id)));\n",
     "  document.getElementById('weak').onclick = () => startShift(shuffle(weak.map(c => c.id)));\n"
     "  document.getElementById('smart').onclick = () => startShift(practica(all, S.n), false, true);\n"
     "  app.querySelectorAll('#fe .chip').forEach(b => b.onclick = () => { S.f.e = b.dataset.e; render(); });\n"
     "  const rs = document.getElementById('reset');\n"
     "  if (rs) rs.onclick = () => {\n"
     "    if (rs.dataset.ok) { mem.p = {}; mem.best = {}; mem.z = Date.now(); save(); S.f.e = 'all'; render(); return; }\n"
     "    rs.dataset.ok = '1'; rs.textContent = '¿Seguro? Toca otra vez para borrar todo';\n"
     "    setTimeout(() => { if (rs.isConnected) { delete rs.dataset.ok; rs.textContent = 'Reiniciar progreso'; } }, 4000);\n"
     "  };\n"),
    # turno de práctica: un caso fallado vuelve a salir 3 pacientes después (una vez)
    ("function startShift(ids, single) { S.shift = {ids, i:0, res:[], single:!!single}; openCase(ids[0]); }",
     "function startShift(ids, single, smart) { S.shift = {ids, i:0, res:[], single:!!single, smart:!!smart, re:{}}; openCase(ids[0]); }"),
    ("      const prev = mem.best[c.id];\n"
     "      mem.best[c.id] = prev == null ? sc : Math.max(prev, sc); save(); topStat();\n",
     "      registrar(c.id, sc, cur.scores.map((s, i) => s < 100 ? i : -1).filter(i => i >= 0)); topStat();\n"
     "      if (S.shift && S.shift.smart && sc < 85 && !S.shift.re[c.id]) { S.shift.re[c.id] = 1; S.shift.ids.splice(Math.min(S.shift.ids.length, S.shift.i + 4), 0, c.id); }\n"),
    ("${mem.best[c.id] != null ? `<div style=\"color:var(--mute);font-size:14px\">Tu mejor puntaje: ${mem.best[c.id]}</div>` : ''}",
     "${mem.p[c.id] ? `<div style=\"color:var(--mute);font-size:14px\">Intentos: ${mem.p[c.id].n} · sin errores: ${mem.p[c.id].a} · mejor: ${mem.best[c.id]}${S.shift && S.shift.ids.indexOf(c.id, S.shift.i + 1) > -1 ? ' · volverá a salir en este turno' : ''}</div>` : ''}"),
]


def memoria(page):
    for a, b in REPL:
        assert page.count(a) == 1, a[:80]
        page = page.replace(a, b)
    return page
