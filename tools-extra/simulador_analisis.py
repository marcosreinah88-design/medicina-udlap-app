"""Análisis del caso al terminarlo (pedido del usuario, 28 nov 2026).

Al cerrar cada caso, acierte o falle, se muestra paso por paso: la pregunta, lo que elegiste frente a la
respuesta correcta, por qué la correcta lo es, por qué se descarta cada una de las otras opciones y qué
siguió en el caso. Usa las explicaciones que ya trae cada opción (no agrega peso a casos.json). Los
pasos fallados salen abiertos; los acertados, cerrados con su análisis a un toque. Solo aparece al
final, así que no revela el diagnóstico antes de tiempo.
"""

CSS = """.ana{grid-column:1/-1;margin-top:6px;text-align:left;min-width:0}
.ana>h3{font-size:22px;margin:0 0 4px}
.ana .ana-dx{color:var(--mute);font-size:14.5px;margin:0 0 12px}
.ana details{border:1.5px solid var(--line);border-radius:12px;margin-top:10px;background:var(--bg)}
.ana details.miss{border-color:color-mix(in srgb,var(--bad) 45%,var(--line))}
.ana summary{cursor:pointer;padding:12px 14px;display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 10px;align-items:start;list-style:none}
.ana summary::-webkit-details-marker{display:none}
.ana summary .q{font-weight:600}
.ana summary small{grid-column:2;color:var(--mute);font-size:13px}
.ana .bd{padding:0 14px 14px}
.ana .it{border-left:3px solid var(--line);padding:6px 0 6px 12px;margin-top:8px;font-size:15px}
.ana .it b{display:block;font-size:12.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute);margin-bottom:2px}
.ana .it .op{font-weight:600}
.ana .it .ex{display:block;color:var(--mute);margin-top:2px}
.ana .it.ok{border-left-color:var(--ok)}.ana .it.ok b{color:var(--ok)}
.ana .it.bad{border-left-color:var(--bad)}.ana .it.bad b{color:var(--bad)}
.ana .it.sig{border-left-color:var(--acc)}
.ana .no{margin:4px 0 0;padding:0;list-style:none}
.ana .no li{margin-top:6px}
"""

JS = r"""
function analisis(c) {
  const cur = S.cur, sel = cur.sel || [];
  const pasos = c.pasos.map((p, i) => {
    const k = p.o.findIndex(o => o[1]), s = sel[i], ok = s === k;
    const otras = p.o.map((o, j) => j).filter(j => j !== k && j !== s);
    const tu = ok ? '' : s != null ? `<div class="it bad"><b>Elegiste · se descarta</b><span class="op">${md(p.o[s][0])}</span><span class="ex">${md(p.o[s][2])}</span></div>` : '';
    const sig = p.r || p.add ? `<div class="it sig"><b>Qué siguió</b>${p.r ? md(p.r) : ''}${p.add ? `${p.r ? '<br>' : ''}<span class="ex">Además: ${md(p.add)}</span>` : ''}</div>` : '';
    return `<details class="${ok ? '' : 'miss'}" ${ok ? '' : 'open'}>
      <summary><span class="score-tag ${ok ? 's-hi' : 's-lo'}">${ok ? '✓' : '✗'}</span><span class="q">${i + 1}. ${FASE[p.f]}: ${md(p.q)}</span><small>${ok ? 'La tuviste bien · toca para ver por qué' : 'Aquí te equivocaste'}</small></summary>
      <div class="bd">${tu}
        <div class="it ok"><b>${ok ? 'Elegiste la correcta' : 'Respuesta correcta'}</b><span class="op">${md(p.o[k][0])}</span><span class="ex">${md(p.o[k][2])}</span></div>
        ${otras.length ? `<div class="it"><b>Por qué no las otras</b><ul class="no">${otras.map(j => `<li><span class="op">${md(p.o[j][0])}</span><span class="ex">${md(p.o[j][2])}</span></li>`).join('')}</ul></div>` : ''}
        ${sig}</div></details>`;
  }).join('');
  return `<div class="ana"><h3>Análisis del caso</h3><p class="ana-dx">Diagnóstico: <b style="color:var(--ink)">${esc(c.tema)}</b> · ${esc(c.pac)}</p>${pasos}</div>`;
}
"""

REPL = [
    (".res li{border-left:3px solid var(--ok);", CSS + ".res li{border-left:3px solid var(--ok);"),
    ("function resultBox(c) {", JS.lstrip() + "\nfunction resultBox(c) {"),
    ("    <div class=\"brk\">${brk}</div>\n    <div class=\"perla\"><b class=\"k\">Perla para el examen</b>${md(c.perla)}</div>",
     "    <div class=\"brk\">${brk}</div>\n    ${analisis(c)}\n    <div class=\"perla\"><b class=\"k\">Perla para el examen</b>${md(c.perla)}</div>"),
    ("    cur.picks = [i]; cur.scores[cur.step] = ok ? 100 : 0; cur.done = true;\n",
     "    cur.picks = [i]; cur.scores[cur.step] = ok ? 100 : 0; cur.done = true; (cur.sel = cur.sel || [])[cur.step] = i;\n"),
]


def analisis(page):
    for a, b in REPL:
        assert page.count(a) == 1, a[:80]
        page = page.replace(a, b)
    return page
