"""Casos del simulador de Gastro en formato lineal (pedido del usuario, 28 nov 2026).

Cada paso es una sola decisión con UNA respuesta correcta, como un diagrama de flujo:
- Pasos «est» (pedir varios estudios): se vuelven una cadena «¿qué haces primero?» →
  «con ese resultado, ¿qué sigue?» (seq) o una sola opción que junta los estudios que van
  juntos (bundle); el resultado del estudio correcto se muestra al responder (campo r).
- Pasos «varias» (marcar todo lo que aplica): una pregunta con la acción principal como
  única correcta; las demás acciones correctas salen después como «Además» (campo add).
  Opciones nuevas marcadas con † (no vienen del artículo).
Formato de salida de cada paso: {f, q, o:[[texto, 1|0, explicación]], r?, add?}.
"""

EST = {  # (caso, paso) con 2 o más estudios clave → cómo se encadenan (índices de opción)
    ("acal1", 0): ("seq", [0, 1]), ("acal2", 0): ("seq", [0, 1]), ("barr2", 0): ("seq", [0, 1]),
    ("gp1", 0): ("seq", [0, 1]), ("gp2", 0): ("bundle", [4, 0]), ("stda1", 0): ("seq", [1, 0]),
    ("dia3", 0): ("bundle", [0, 1]), ("cel1", 0): ("bundle", [0, 1]), ("cel2", 0): ("seq", [0, 1]),
    ("cro1", 0): ("seq", [0, 1, 2]), ("cro2", 0): ("bundle", [1, 0]), ("cuci1", 0): ("seq", [0, 1]),
    ("cuci2", 0): ("seq", [0, 1]), ("sii1", 0): ("bundle", [0, 1]), ("est2", 0): ("bundle", [0, 1]),
    ("stdb1", 0): ("bundle", [0, 1]), ("pfh1", 0): ("seqb", [0, [1, 2, 3]]), ("pfh2", 0): ("seq", [1, 0]),
    ("hva1", 0): ("seq", [0, 2]), ("hvb1", 0): ("bundle", [0, 1]), ("hvc1", 0): ("seq", [0, 1]),
    ("hai1", 0): ("seq", [0, 1]), ("cbp1", 0): ("seq", [0, 1]), ("masld1", 0): ("seq", [0, 1]),
    ("cir1", 0): ("bundle", [0, 1]), ("bav2", 0): ("bundle", [0, 1]), ("col1", 0): ("bundle", [0, 1]),
    ("col2", 0): ("bundle", [1, 0]), ("pan1", 0): ("bundle", [0, 1]), ("pan3", 0): ("seq", [0, 1]),
}

D = "†"
VARIAS = {  # (caso, paso): q, p = opción principal (única correcta), extra = distractores nuevos, drop = opciones que se quitan
    ("erge1", 2): dict(q="¿Cuál es la base del tratamiento hoy?", p=0, extra=[
        ("IBP a demanda, solo cuando tenga ardor", "La prueba terapéutica es diaria, antes del desayuno, por 6 semanas; a demanda es para mantenimiento." + D)]),
    ("erge2", 2): dict(q="¿Qué haces?", p=0),
    ("acal1", 2): dict(q="¿Qué opciones definitivas le ofreces?", comp=(
        "Cualquiera de las tres: Heller laparoscópico con Dor, dilatación neumática (iniciando con 30 mm) o POEM",
        "Las tres son definitivas y funcionan muy bien en el tipo 2. Heller + Dor: mejoría >90 % a 5 años. Dilatación: empezar con 30 mm (perforación 1 % vs 9 %). POEM: 82–98 %, pero da más ERGE (47 %)."),
        extra=[("Solo POEM: la dilatación y el Heller ya no se recomiendan", "Las tres opciones son válidas; se elige según el centro y el paciente." + D)]),
    ("barr1", 2): dict(q="Además de continuar el IBP, ¿cada cuándo lo vigilas?", p=1, extra=[
        ("Endoscopía cada año", "Anual no corresponde a Barrett sin displasia; sin displasia y ≥3 cm es cada 3 años." + D),
        ("Endoscopía cada 5 años", "Cada 5 años es para segmentos de 1 a <3 cm; este mide ≥3 cm.")]),
    ("ulc2", 2): dict(q="¿Qué es lo primero en su manejo?", p=0, extra=[
        ("Cambiar el naproxeno por ibuprofeno", "Cualquier AINE no selectivo sigue dañando la mucosa; si necesita antiinflamatorio, COX-2 + IBP." + D),
        ("Solo antiácidos y seguir con el naproxeno", "Sin quitar la causa la úlcera no cicatriza." + D)]),
    ("ulc3", 2): dict(q="¿Cuál es el tratamiento definitivo?", p=1, extra=[
        ("Gastrectomía subtotal de urgencia", "Para la perforación basta el parche de epiplón; la resección es para úlceras gigantes o sospecha de cáncer." + D),
        ("Endoscopía urgente para cerrar la perforación con clips", "La perforación con peritonitis es quirúrgica." + D)]),
    ("gp1", 2): dict(q="¿Cuál es el primer paso del manejo?", p=0, extra=[
        ("G-POEM", "Es para gastroparesia refractaria; aquí apenas empieza el manejo." + D)]),
    ("gp2", 2): dict(q="¿Qué evita que se repitan los episodios?", p=2, extra=[
        ("Ondansetrón diario como preventivo", "El antiemético alivia el episodio, pero no lo previene." + D)]),
    ("hp1", 2): dict(q="¿Qué haces primero?", p=0, extra=[
        ("Triple con claritromicina 7 días", "Con resistencia alta a claritromicina se prefiere cuádruple con bismuto 14 días." + D),
        ("Solo vigilancia endoscópica, sin erradicar", "Erradicar reduce 55 % el cáncer gástrico en familiares de primer grado.")]),
    ("stda1", 2): dict(q="En la endoscopía, ¿cómo tratas la úlcera Forrest IIa?", p=2, drop=[5, 6], extra=[
        ("Epinefrina sola", "La epinefrina nunca va como monoterapia: se combina con método térmico o clip."),
        ("No tratarla porque ya no sangra", "Forrest IIa es de alto riesgo y se trata." + D)]),
    ("dia1", 2): dict(q="¿Cuál es la base del tratamiento?", p=0, extra=[
        ("Dieta astringente estricta varios días", "No se recomiendan dietas restrictivas: reiniciar pronto la dieta habitual."),
        ("Coprocultivo a todos antes de tratar", "En diarrea acuosa sin datos de alarma no se piden estudios de heces de rutina." + D)]),
    ("dia2", 2): dict(q="¿Qué antibiótico eliges?", p=0, extra=[
        ("Ciprofloxacino", "Campylobacter resiste mucho a quinolonas; con fiebre o disentería se prefiere azitromicina.")]),
    ("dia3", 2): dict(q="Mientras llega el resultado, ¿qué haces?", p=0, extra=[
        ("Trimetoprim-sulfametoxazol empírico", "Nada de antibióticos hasta conocer el patógeno: en STEC aumentan el riesgo de SUH." + D)]),
    ("dia4", 2): dict(q="¿Qué tratamiento le das?", p=0, drop=[1, 4], extra=[
        ("Metronidazol oral", "Ya no es primera línea para C. difficile." + D),
        ("Vancomicina IV", "La vancomicina IV no llega al colon; para C. difficile es oral." + D)]),
    ("cron2", 2): dict(q="¿Cuál es el tratamiento de elección?", p=0, extra=[
        ("Prednisona a dosis altas", "La budesonida es de elección: igual de eficaz con menos efectos sistémicos." + D)]),
    ("cel1", 3): dict(q="¿Cuál es el tratamiento?", p=0, extra=[
        ("Dieta baja en gluten solo cuando tenga síntomas", "Tiene que ser estricta y de por vida: pequeñas cantidades mantienen el daño." + D),
        ("Enzimas que digieren el gluten en lugar de la dieta", "Ningún fármaco ha demostrado eficacia; el único tratamiento es la dieta.")]),
    ("cro1", 2): dict(q="¿Qué terapia eliges para inducir y mantener?", p=0),
    ("cro2", 2): dict(q="¿Qué haces primero?", p=0, extra=[
        ("Iniciar infliximab hoy, antes de drenar", "Primero se controla la sepsis: drenaje y setón; después infliximab." + D)]),
    ("cuci2", 2): dict(q="¿Cuál es la base del tratamiento?", p=0, extra=[
        ("Mesalazina oral a dosis alta como único tratamiento", "En el brote grave hospitalizado la base son los esteroides IV." + D),
        ("Colectomía de urgencia al ingreso", "La cirugía se considera si no responde (día 3) o hay complicación." + D)]),
    ("sii1", 2): dict(q="¿Por dónde empiezas el tratamiento?", p=0, extra=[
        ("Colonoscopia para tranquilizarla", "Sin datos de alarma y <45 años no está indicada; explicar el diagnóstico es parte del tratamiento.")]),
    ("stdb1", 3): dict(q="¿Cómo tratas el divertículo con vaso visible?", p=0, extra=[
        ("Colectomía segmentaria de entrada", "La cirugía es para sangrado recurrente o que no se controla." + D),
        ("Embolización arterial programada", "La angiografía es para sangrado activo que no se localiza o no se controla por endoscopía." + D)]),
    ("stdb2", 2): dict(q="¿Qué haces primero?", p=0, extra=[
        ("Colonoscopia urgente antes de estabilizarla", "Primero líquidos para normalizar presión y FC; después los estudios.")]),
    ("pfh2", 2): dict(q="¿Cuál es la conducta principal?", p=0, extra=[
        ("Volver a dar el antibiótico para confirmar", "La reexposición puede causar una reacción más grave." + D),
        ("CPRE para destapar la vía biliar", "El ultrasonido no mostró obstrucción: es colestasis por fármaco.")]),
    ("hva1", 2): dict(q="¿Cuál es el tratamiento?", p=0, extra=[
        ("Tenofovir", "Es para hepatitis B; la hepatitis A no tiene antiviral." + D),
        ("Inmunoglobulina al paciente", "La profilaxis es para los contactos, no para el enfermo." + D)]),
    ("hvb1", 2): dict(q="¿Con qué lo tratas?", p=0, extra=[
        ("Adefovir", "Poca potencia y nefrotoxicidad; se prefieren entecavir o tenofovir." + D)]),
    ("hvc1", 2): dict(q="¿Con qué lo tratas?", p=0, extra=[
        ("Ribavirina sola", "No cura el VHC; hoy se usan antivirales de acción directa pangenotípicos." + D)]),
    ("hai1", 2): dict(q="¿Con qué inicias la inducción?", p=0, extra=[
        ("Azatioprina sola desde el primer día", "Se agrega a las 2 semanas, ya iniciada la prednisolona." + D),
        ("Esperar 3 meses a ver si se resuelve sola", "La HAI activa se trata; sin tratamiento progresa a cirrosis." + D)]),
    ("cbp1", 2): dict(q="¿Cuál es el tratamiento de primera línea?", p=0, extra=[
        ("Ácido obeticólico de primera línea", "Es segunda línea, para quien no responde al ursodesoxicólico." + D)]),
    ("masld1", 2): dict(q="¿Cuál es la base del tratamiento?", p=0, extra=[
        ("Vitamina E como única medida", "La base es bajar ≥10 % de peso; los fármacos se suman, no lo sustituyen." + D),
        ("Suspender cualquier estatina por las transaminasas", "Las estatinas son seguras en MASLD y bajan su riesgo cardiovascular.")]),
    ("cir1", 2): dict(q="¿Qué inicias para la hipertensión portal?", p=0, drop=[5], extra=[
        ("Nada hasta que tenga várices grandes", "Con hipertensión portal clínicamente significativa el BBNS previene la descompensación."),
        ("Propranolol a dosis altas sin importar la presión", "Carvedilol es el preferido y se ajusta a la presión arterial." + D)]),
    ("bav1", 2): dict(q="¿Qué inicias desde la sospecha, antes de la endoscopía?", p=0, extra=[
        ("Solo IBP IV y esperar la endoscopía", "En sospecha de sangrado variceal el vasoactivo va desde la sospecha." + D)]),
    ("bav2", 2): dict(q="¿Con qué tratas el SHR-LRA?", p=0, extra=[
        ("Dopamina a dosis renal", "No sirve en el SHR-LRA." + D)]),
    ("bav3", 2): dict(q="¿Qué ofreces para la ascitis refractaria?", p=0, extra=[
        ("Paracentesis de gran volumen sin albúmina", "Más de 5 L requiere albúmina para evitar disfunción circulatoria." + D),
        ("Furosemida a dosis máxima", "Ya es refractaria a diuréticos; subirlos daña el riñón." + D)]),
    ("col1", 2): dict(q="¿Cuándo drenas la vía biliar?", p=1, extra=[
        ("Solo si no responde a 72 h de antibiótico", "Eso es para el grado leve; en grado II el drenaje temprano (≤24 h) bajó la mortalidad." + D)]),
    ("col2", 2): dict(q="¿Cómo drenas la vía biliar?", p=0, extra=[
        ("Esfinterotomía y extracción de todos los litos hoy", "Con coagulopatía e inestabilidad: stent primero, extracción después."),
        ("Esperar a que se normalice el INR para la CPRE", "El grado III necesita drenaje urgente en cuanto se estabilice.")]),
    ("pan1", 2): dict(q="¿Cuál es la base del manejo inicial?", p=0, extra=[
        ("Solución salina a chorro, 4 L en las primeras horas", "La reanimación agresiva aumenta la sobrecarga; líquidos guiados por metas." + D)]),
    ("pan2", 2): dict(q="¿Cuál es el primer escalón para la necrosis infectada?", p=1, extra=[
        ("Necrosectomía endoscópica directa como primer paso", "El abordaje escalonado empieza con drenaje; la necrosectomía es el siguiente escalón."),
        ("Suspender la enteral y pasar a parenteral", "La nutrición enteral es preferible.")]),
}

FIRST = "¿Qué haces primero?"
NEXT = "Con ese resultado, ¿qué sigue?"


def _dot(s):
    s = s.strip()
    return s if s.endswith((".", "?", "†")) else s + "."


def _lc(s):
    w = s.split(" ")[0]
    return s[:1].lower() + s[1:] if len(w) > 1 and w[1:].isalpha() and w[1:].islower() else s


def _q(q, first):
    if not first:
        return NEXT
    return FIRST if ("estudios" in q or q.startswith("¿Qué pides") or q == "¿Qué haces?") else q


def _est(cid, i, p):
    o = p["o"]
    keys = [j for j, x in enumerate(o) if x[1] == 2]
    mode, spec = EST.get((cid, i), ("seq", keys))
    assert sorted(sum(([x] if isinstance(x, int) else x for x in spec), [])) == sorted(keys), (cid, i)

    def fb(j, later=()):
        v = o[j][1]
        if j in later:
            return "Todavía no: va después. " + o[j][3]
        if v == 1:
            return "Razonable, pero no es el paso clave ahora. " + o[j][3]
        return o[j][3]

    def bundle(group, first, used):
        names = " + ".join(o[j][0] for j in group)
        opts = [[names, 1, " ".join(_dot(o[j][3]) for j in group)]]
        for j in group:
            others = " y ".join(_lc(o[k][0]) for k in group if k != j)
            opts.append(["Solo " + _lc(o[j][0]), 0, f"Incompleto: también necesitas {others}."])
        opts += [[o[j][0], 0, fb(j)] for j in range(len(o)) if j not in keys and j not in used]
        r = " ".join(f"**{o[j][0]}:** {_dot(o[j][2])}" for j in group)
        return {"f": p["f"], "q": _q(p["q"], first), "o": opts, "r": r}

    def single(j, later, first, used):
        opts = [[o[j][0], 1, o[j][3]]]
        opts += [[o[k][0], 0, fb(k, later)] for k in range(len(o)) if k != j and k not in used]
        return {"f": p["f"], "q": _q(p["q"], first), "o": opts, "r": _dot(o[j][2])}

    if mode == "bundle":
        return [bundle(spec, True, [])]
    if mode == "seqb":
        a, grp = spec
        return [single(a, grp, True, []), bundle(grp, False, [a])]
    out, used = [], []
    for n, j in enumerate(spec):
        out.append(single(j, spec[n + 1:], n == 0, used))
        used.append(j)
    return out


def _varias(cid, i, p):
    sp = VARIAS[(cid, i)]
    o = p["o"]
    drop = set(sp.get("drop", []))
    good = [j for j, x in enumerate(o) if x[1]]
    if "comp" in sp:
        opts = [[sp["comp"][0], 1, sp["comp"][1]]]
        add = []
    else:
        m = sp["p"]
        assert o[m][1], (cid, i)
        opts = [[o[m][0], 1, o[m][2]]]
        add = [_dot(o[j][0]) for j in good if j != m]
    opts += [[o[j][0], 0, o[j][2]] for j, x in enumerate(o) if not x[1] and j not in drop]
    opts += [[t, 0, f] for t, f in sp.get("extra", [])]
    st = {"f": p["f"], "q": sp["q"], "o": opts}
    if add:
        st["add"] = " ".join(add)
    return st


def linealizar(casos):
    for c in casos:
        nuevos = []
        for i, p in enumerate(c["pasos"]):
            if p["tipo"] == "est":
                nuevos += _est(c["id"], i, p)
            elif p["tipo"] == "varias":
                nuevos.append(_varias(c["id"], i, p))
            else:
                nuevos.append({"f": p["f"], "q": p["q"], "o": [[x[0], 1 if x[1] else 0, x[2]] for x in p["o"]]})
        for st in nuevos:
            assert sum(x[1] for x in st["o"]) == 1, (c["id"], st["q"])
            assert len(st["o"]) >= 3, (c["id"], st["q"], len(st["o"]))
        c["pasos"] = nuevos
    return casos


# ---- motor de la página: una decisión por paso ----
STEPBOX = r"""function stepBox(c) {
  const cur = S.cur, p = c.pasos[cur.step];
  const opts = cur.order[cur.step].map(i => {
    const o = p.o[i], picked = cur.picks[0] === i;
    let cl = '', mk = '', extra = '';
    if (cur.done) {
      cl = 'lock ';
      if (o[1] && picked) { cl += 'g'; mk = 'Correcto'; }
      else if (o[1]) { cl += 'y'; mk = 'Este era el camino'; }
      else if (picked) { cl += 'r'; mk = 'Se descarta'; }
      else { cl += 'n'; mk = 'Se descarta'; }
      extra = `<span class="fb">${md(o[2])}</span>`;
    }
    return `<label class="opt ${cl}"><input type="radio" name="o" value="${i}" ${picked ? 'checked' : ''} ${cur.done ? 'disabled' : ''}>
      <span class="ot">${md(o[0])}</span>${mk ? `<span class="mk">${mk}</span>` : ''}${extra}</label>`;
  }).join('');
  const ok = cur.done ? cur.scores[cur.step] === 100 : null;
  const last = cur.step === c.pasos.length - 1;
  const luego = cur.done && (p.r || p.add) ? `<div class="luego">${p.r ? `<b>Resultado:</b> ${md(p.r)}` : ''}${p.add ? `<div${p.r ? ' style="margin-top:8px"' : ''}><b>Además:</b> ${md(p.add)}</div>` : ''}</div>` : '';
  return `<div class="step">
    <div class="kind">Paso ${cur.step + 1} de ${c.pasos.length} · ${FASE[p.f]}</div>
    <h2>${md(p.q)}</h2>
    <p class="hint">${cur.done ? (ok ? 'Bien. Así sigue el caso:' : 'Esa opción se descarta. Sigue por el camino correcto:') : 'Elige una opción. Solo una es correcta.'}</p>
    <div class="opts">${opts}</div>
    ${luego}
    ${cur.done ? `<div class="act"><span class="pts ${ok ? 's-hi' : 's-lo'}" style="padding:4px 10px;border-radius:8px">${ok ? '✓ Correcto' : '✗ Incorrecto'}</span>
        <button class="btn btn-acc" id="next">${last ? 'Ver resultado del caso' : 'Siguiente paso'} →</button></div>` : ''}
  </div>`;
}
"""

BINDSTEP = r"""function bindStep(c) {
  const cur = S.cur;
  if (cur.step >= c.pasos.length) {
    const g = id => document.getElementById(id);
    g('again').onclick = () => openCase(c.id);
    if (g('nextc')) g('nextc').onclick = () => { S.shift.i++; openCase(S.shift.ids[S.shift.i]); };
    if (g('sum')) g('sum').onclick = () => { S.view = 'sum'; render(); window.scrollTo(0, 0); };
    if (g('home')) g('home').onclick = () => { S.view = 'home'; S.shift = null; render(); };
    return;
  }
  const p = c.pasos[cur.step];
  document.getElementById('stepbox').querySelectorAll('input[name=o]').forEach(inp => inp.onchange = () => {
    if (cur.done) return;
    const i = +inp.value, ok = !!p.o[i][1];
    cur.picks = [i]; cur.scores[cur.step] = ok ? 100 : 0; cur.done = true;
    const k = p.o.findIndex(o => o[1]);
    cur.results.push({n: p.o[k][0], r: p.r || '', miss: !ok});
    ok ? sOk() : sBad();
    caseView();
    const b = document.getElementById('stepbox'); if (b && window.innerWidth < 900) b.scrollIntoView({block:'start', behavior:'smooth'});
  });
  const nx = document.getElementById('next');
  if (nx) nx.onclick = () => {
    cur.step++; cur.done = false; cur.picks = [];
    if (cur.step >= c.pasos.length) {
      const sc = Math.round(cur.scores.reduce((a, b) => a + b, 0) / cur.scores.length);
      if (S.shift) S.shift.res.push({id:c.id, sc, fases:c.pasos.map((p, i) => [p.f, cur.scores[i]])});
      const prev = mem.best[c.id];
      mem.best[c.id] = prev == null ? sc : Math.max(prev, sc); save(); topStat();
      if (sc >= 85) tone([523, 659, 784], .14);
    }
    caseView();
    const b = document.getElementById('stepbox'); if (b) b.scrollIntoView({block:'start', behavior:'smooth'});
  };
}
"""

TEXTOS = [
    ("Recibes al paciente, pides estudios, haces el diagnóstico y decides el tratamiento. Cada paso se califica y se explica con el artículo del curso.",
     "Como un diagrama de flujo: en cada paso eliges una sola opción, ves el resultado y sigues; lo que no va se descarta con su explicación del artículo del curso."),
    ("<b>${esc(r.n)}${r.miss ? ' · no lo pediste, pero era clave' : ''}</b>", "<b>${esc(r.n)}${r.miss ? ' · aquí te equivocaste' : ''}</b>"),
    ("Aún no hay resultados. Pide estudios para verlos aquí.", "Aquí se va armando tu camino, paso a paso."),
]


def motor(page):
    a = page.index("function stepBox(c) {"); b = page.index("\nfunction resultBox(c) {")
    page = page[:a] + STEPBOX + page[b:]
    a = page.index("function bindStep(c) {"); b = page.index("\n/* ---------- resumen")
    page = page[:a] + BINDSTEP + page[b:]
    for x, y in TEXTOS:
        assert page.count(x) == 1, x
        page = page.replace(x, y)
    assert page.count("<h3>Resultados</h3>") == 2
    page = page.replace("<h3>Resultados</h3>", "<h3>Tu camino</h3>")
    return page
