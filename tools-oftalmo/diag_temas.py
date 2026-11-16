# Contenido nuevo de la guía de Oftalmología (5º): diagnóstico, ojo rojo, fármacos y casos clínicos.
# Lo usa patch_diag.py. Convención de la guía: lo que no viene de los apuntes de Marcos va con †.
# Fuentes de los apuntes: Notion › Medicina › 7mo semestre › Oftalmología (páginas «molestias astenópicas»,
# «Campo visual», «Lámpara de hendidura» y «Oftalmoscopía»).

T = '<sup class="dx-dag" title="No viene de tus apuntes">†</sup>'

# ---------- Bloque 06: diagnóstico (se insertan después de «Exploración: agudeza, campo, color y pupilas») ----------
B6 = [
('Agudeza visual: cómo se mide y se anota', 'agudeza', f'''
    <p><b>Agudeza visual</b>: capacidad del ojo para discriminar un objeto a una distancia determinada. Explora el <b>II par</b> junto con el campo visual, la visión al color y los reflejos pupilares.</p>
    <h4>Técnica (cartilla de Snellen)</h4>
    <ol>
      <li>Paciente a <span class="num">6 m (20 pies)</span>. El tamaño de las letras se mide en <b>minutos de arco</b>.</li>
      <li>Primero el <b>ojo derecho</b> (OD) y luego el izquierdo (OS u OI, <i>oculus sinister</i>), tapando el otro.</li>
      <li>Se anota la última línea que lee. Si usa lentes, se mide con ellos{T}.</li>
      <li>Luego con <b>agujero estenopeico</b>: si mejora, el problema es refractivo.</li>
    </ol>
    <div class="tbl"><table>
      <tr><th>Fracción</th><th>Qué significa</th></tr>
      <tr><td>Numerador</td><td>Distancia a la que se hace la prueba (20 pies)</td></tr>
      <tr><td>Denominador</td><td>Distancia a la que una persona con visión normal vería ese tamaño de letra</td></tr>
      <tr><td><span class="num">20/200 (.) 20/70+1</span></td><td>Así se anota en tus apuntes: sin corrección 20/200; con estenopeico 20/70 y una letra más de la línea siguiente</td></tr>
    </table></div>
    <h4>Si no lee ni la letra más grande{T}</h4>
    <div class="tbl"><table>
      <tr><th>Paso</th><th>Se anota</th></tr>
      <tr><td>Acercar la cartilla</td><td>Ej. <span class="num">10/200</span> (a 10 pies lee la de 200)</td></tr>
      <tr><td>Cuenta dedos</td><td><b>CD</b> a tantos metros</td></tr>
      <tr><td>Movimiento de manos</td><td><b>MM</b></td></tr>
      <tr><td>Percepción de luz</td><td><b>PL</b>, con o sin proyección (de qué lado viene la luz)</td></tr>
      <tr><td>Nada</td><td><b>NPL</b>: no percibe luz</td></tr>
    </table></div>
    <ul>
      <li>Equivalencias{T}: <span class="num">20/20 = 6/6 = 1.0</span> decimal; <span class="num">20/40 = 6/12 = 0.5</span>.</li>
      <li>Visión cercana{T}: cartilla de Jaeger o Rosenbaum a <span class="num">33–40 cm</span> (útil en presbicia).</li>
      <li>Niños{T}: cartilla de la E direccional o de figuras (LEA, Allen); en lactantes, si fija y sigue la luz.</li>
      <li>Baja visión y ceguera (OMS){T}: baja visión moderada peor que <span class="num">6/18</span>; ceguera peor que <span class="num">3/60</span> en el mejor ojo.</li>
    </ul>
    <div class="note"><b>Para precisar</b>Tus apuntes dicen que el estenopeico mejora la visión "porque reduce la cantidad de luz que entra". Más bien deja pasar solo los rayos centrales, que no necesitan enfocarse, y así quita el círculo borroso que da el error refractivo{T}. Si con el estenopeico no mejora, piensa en catarata, retina o nervio óptico.</div>
'''),
('Lámpara de hendidura (biomicroscopía)', 'lampara', f'''
    <p>Microscopio binocular con una luz en forma de hendidura. Tiene <b>3 sistemas</b>: óptico, luminoso y mecánico. Se explora de afuera hacia adentro.</p>
    <div class="tbl"><table>
      <tr><th>Estructura</th><th>Qué se busca</th></tr>
      <tr><td>Párpados y pestañas</td><td>Glándulas inflamadas o llenas de grasa, cosas en las pestañas (costras, caspa, liendres{T})</td></tr>
      <tr><td>Conjuntiva tarsal y bulbar</td><td>Folículos, papilas, hiperemia</td></tr>
      <tr><td>Lágrima</td><td><b>Tiempo de ruptura</b>: cuánto tarda en romperse la película (se ve una mancha negra). No debe durar menos de <span class="num">15 s</span>; menos de 10 s apoya ojo seco{T}</td></tr>
      <tr><td>Córnea</td><td>Transparencia, úlceras, cuerpos extraños, tinciones</td></tr>
      <tr><td>Cámara anterior</td><td>Se ven 2 reflejos (córnea e iris) y no debe haber nada entre ellos; también se valora la distancia entre ambos (profundidad). <b>Hipopión</b> = pus; <b>hipema</b> = sangre</td></tr>
      <tr><td>Humor acuoso</td><td>Debe verse negro. <b>Células</b> (fenómeno de Tyndall, partículas) = inflamación. <b>Flare</b> (como humo) = proteínas en el acuoso</td></tr>
      <tr><td>Iris</td><td>Nódulos de Koeppe, melanoma de iris</td></tr>
      <tr><td>Cristalino</td><td>Se dilata la pupila con una gota; opacidades (catarata)</td></tr>
      <tr><td>Vítreo</td><td>"Humo" de fibras; sangre en diabéticos por la retinopatía</td></tr>
    </table></div>
    <h4>Tinciones</h4>
    <div class="tbl"><table>
      <tr><th>Colorante</th><th>Qué evalúa</th></tr>
      <tr><td><b>Fluoresceína</b></td><td>Úlceras y defectos del epitelio; brilla verde con luz azul cobalto{T}. Prueba de Seidel: si se "lava" en un punto, hay herida que fuga acuoso{T}</td></tr>
      <tr><td>Rosa de bengala</td><td>Moco (y células desvitalizadas{T})</td></tr>
      <tr><td>Verde de lisamina</td><td>Moco y células muertas; molesta menos que el rosa de bengala{T}</td></tr>
    </table></div>
    <h4>Lentes especiales</h4>
    <ul>
      <li><b>Goniolente</b> o lente de 3 espejos: ángulo iridocorneal (gonioscopía, STER).</li>
      <li><b>Lupa de 90 D</b>: fondo de ojo, retina y nervio óptico.</li>
      <li><b>Tonometría</b> (PIO): normal <span class="num">10–21 mmHg</span>. Ver el tema "Tonometría y presión intraocular".</li>
    </ul>
    <div class="note"><b>Ojo con tus apuntes</b>"Epipema" es <b>hipema</b> (sangre en la cámara anterior) y los "nódulos de Keppler" son los <b>nódulos de Koeppe</b> (en el borde pupilar, típicos de uveítis). "Tanometría" es tonometría.</div>
'''),
('Tonometría y presión intraocular', 'tonometria', f'''
    <p>De tus apuntes: la PIO normal es de <span class="num">10–21 mmHg</span> y el tonómetro de referencia es el de <b>Goldmann</b>. El resto de este tema es complemento{T}.</p>
    <div class="tbl"><table>
      <tr><th>Tonómetro{T}</th><th>Cómo funciona</th><th>Cuándo se usa</th></tr>
      <tr><td><b>Goldmann</b></td><td>Aplanación: aplana un área fija de la córnea con anestésico y fluoresceína, en la lámpara</td><td>Estándar de oro</td></tr>
      <tr><td>Perkins</td><td>Goldmann de mano</td><td>Paciente acostado, quirófano, niños</td></tr>
      <tr><td>De aire (no contacto)</td><td>Un soplo aplana la córnea</td><td>Tamizaje rápido, sin anestésico</td></tr>
      <tr><td>De rebote (iCare) y Tono-Pen</td><td>Sonda pequeña que toca la córnea</td><td>Niños, consultorio, urgencias</td></tr>
      <tr><td>Digital (palpación)</td><td>Se presiona el globo sobre el párpado cerrado</td><td>Solo orientativa: ojo "duro como piedra" en el cierre angular agudo</td></tr>
    </table></div>
    <ul>
      <li><b>Paquimetría</b>{T}: una córnea gruesa hace que la PIO se lea más alta; una delgada (o después de LASIK), más baja.</li>
      <li>La PIO varía durante el día{T}, suele ser más alta en la mañana; una sola medición no confirma ni descarta glaucoma.</li>
      <li><b>Hipertensión ocular</b>: PIO arriba de 21 sin daño del nervio. En el cierre angular agudo suele pasar de <span class="num">50–60 mmHg</span>.</li>
    </ul>
    <div class="note"><b>No presionar el ojo</b>{T}Si hay sospecha de herida penetrante (ojo abierto), no se mide la PIO ni se aprieta el globo: se pone un protector rígido y se refiere. Con úlcera o infección activa se evita el tonómetro de contacto.</div>
'''),
('Oftalmoscopía directa e indirecta', 'oftalmoscopia', f'''
    <p>El <b>oftalmoscopio directo</b> tiene mango, pilas, reóstato (intensidad de la luz), cabeza con discos de lentes y mirilla. En el disco de lentes, los números <b>rojos</b> (negativos) son para el <b>miope</b> y los <b>verdes</b> (positivos) para el <b>hipermétrope</b>.</p>
    <div class="tbl"><table>
      <tr><th></th><th>Directa</th><th>Indirecta</th></tr>
      <tr><td>Equipo</td><td>Oftalmoscopio de mano</td><td>Se necesita una lupa (20 D o la de 90 D en la lámpara{T})</td></tr>
      <tr><td>Imagen</td><td>Más grande (unas 15 veces{T}), derecha</td><td><b>Al revés</b>, en 3D, menos aumento</td></tr>
      <tr><td>Campo</td><td>Pequeño</td><td>Mucho mayor (llega a la periferia)</td></tr>
      <tr><td>Visión</td><td>Monocular</td><td>Binocular</td></tr>
      <tr><td>Dilatar</td><td>Se puede sin dilatar</td><td>Sí se necesita dilatar</td></tr>
      <tr><td>Resolución</td><td>No da tanta</td><td>Mucho mayor (de tus apuntes)</td></tr>
    </table></div>
    <h4>Qué revisar, en orden{T}</h4>
    <ol>
      <li><b>Reflejo rojo</b> a unos 30 cm: si falta o se ve blanco (leucocoria), piensa en catarata o <b>retinoblastoma</b>.</li>
      <li><b>Papila</b>: bordes nítidos, color naranja rosado, excavación/disco ≤ 0.3–0.5 y simétrica entre ojos (diferencia &gt; 0.2 es sospechosa).</li>
      <li><b>Vasos</b>: relación arteria:vena <span class="num">2:3</span>; cruces arteriovenosos, hemorragias, exudados.</li>
      <li><b>Mácula</b>: al final, pidiendo que mire la luz (molesta).</li>
    </ol>
    <ul>
      <li>Técnica{T}: ojo derecho del paciente con tu ojo derecho y tu mano derecha; entra unos 15° por fuera de su línea de mirada para llegar a la papila.</li>
      <li>Dilatar{T}: tropicamida 1% ± fenilefrina 2.5%. Antes mira la profundidad de la cámara anterior (luz de lado): con <b>ángulo estrecho</b> la dilatación puede desencadenar un cierre angular. No dilatar a un paciente neurológico al que hay que vigilarle las pupilas.</li>
    </ul>
    <div class="note"><b>Para precisar</b>En detalle fino la directa aumenta más; lo que gana la indirecta es campo, visión en 3D y ver a través de medios algo opacos{T}. Por eso en la práctica se usan las dos.</div>
'''),
('OCT y otros estudios de imagen', 'estudios', f'''
    <p>Todo este tema es complemento{T}: para saber qué estudio pedir y qué responde cada uno.</p>
    <div class="tbl"><table>
      <tr><th>Estudio</th><th>Qué es</th><th>Cuándo pedirlo</th></tr>
      <tr><td><b>OCT</b> (tomografía de coherencia óptica)</td><td>Cortes de la retina y el nervio con luz, como una "ecografía con luz"; sin contacto ni contraste</td><td>Edema macular diabético, DMAE, agujero macular; capa de fibras nerviosas en glaucoma y su progresión</td></tr>
      <tr><td>Angio-OCT</td><td>OCT que dibuja los vasos sin inyectar</td><td>Neovasos de la DMAE húmeda, isquemia macular</td></tr>
      <tr><td>Angiografía con fluoresceína</td><td>Fotos seriadas tras fluoresceína IV</td><td>Fugas, neovasos e isquemia (retinopatía diabética, oclusiones). Pone la piel y la orina amarillas; náusea; rara vez anafilaxia</td></tr>
      <tr><td>Campimetría (Humphrey)</td><td>Mapa del campo visual con estímulos de luz</td><td>Glaucoma (escalón nasal, escotoma arqueado), lesiones de la vía visual</td></tr>
      <tr><td>Ecografía modo B</td><td>Ultrasonido del globo</td><td>Cuando no se ve el fondo (catarata densa, hemorragia vítrea): descartar desprendimiento de retina o tumor</td></tr>
      <tr><td>Biometría</td><td>Mide la longitud del ojo</td><td>Calcular la LIO antes de la cirugía de catarata</td></tr>
      <tr><td>Topografía o tomografía corneal y paquimetría</td><td>Forma y grosor de la córnea</td><td>Queratocono, antes de cirugía refractiva</td></tr>
      <tr><td>Gonioscopía</td><td>Lente de contacto con espejos</td><td>Clasificar el ángulo (abierto o cerrado)</td></tr>
      <tr><td>TC de órbitas</td><td>Hueso y tejidos blandos</td><td>Celulitis orbitaria, fracturas, cuerpo extraño metálico (<b>no RM</b> si puede ser metálico)</td></tr>
      <tr><td>RM de órbitas y cráneo</td><td>Nervio óptico y cerebro</td><td>Neuritis óptica (esclerosis múltiple), tumores de la vía visual</td></tr>
    </table></div>
    <div class="key"><b>Regla rápida</b>Mácula → OCT. Vasos que fugan → angiografía. No se ve el fondo → ecografía B. Campo → campimetría. Órbita → TC.</div>
'''),
]

# ---------- Bloque 05: ojo rojo y fármacos (al final del bloque) ----------
B5 = [
('Ojo rojo: tabla comparativa', 'ojorojo', f'''
    <p>Junta lo que ya viene en los temas de conjuntivitis, queratitis, uveítis y glaucoma. La pregunta clave: <b>¿es solo conjuntiva o hay algo más profundo?</b></p>
    <div class="tbl"><table class="dx-cmp">
      <tr><th></th><th>Conjuntivitis</th><th>Queratitis</th><th>Uveítis anterior</th><th>Glaucoma agudo</th></tr>
      <tr><td>Dolor</td><td>Ardor, arenilla (comezón si es alérgica)</td><td>Intenso, sensación de cuerpo extraño</td><td>Moderado, profundo</td><td><b>Muy intenso</b>, con cefalea, náusea y vómito</td></tr>
      <tr><td>Visión</td><td><b>Normal</b></td><td>Baja si la lesión es central</td><td>Algo borrosa</td><td>Muy baja, <b>halos</b> de colores</td></tr>
      <tr><td>Secreción</td><td>Acuosa (viral), purulenta (bacteriana), mucosa (alérgica)</td><td>Lagrimeo; mucopurulenta si es bacteriana</td><td>Lagrimeo</td><td>Lagrimeo</td></tr>
      <tr><td>Hiperemia</td><td>Conjuntival, superficial, hacia los fondos de saco</td><td>Ciliar (periquerática)</td><td>Ciliar, violácea</td><td>Mixta, difusa</td></tr>
      <tr><td>Fotofobia</td><td>Leve o no</td><td>Intensa, blefaroespasmo</td><td>Intensa</td><td>Moderada</td></tr>
      <tr><td>Córnea</td><td>Transparente</td><td>Opacidad o úlcera, <b>tiñe con fluoresceína</b></td><td>Precipitados en el endotelio</td><td>Edematosa, "empañada"</td></tr>
      <tr><td>Pupila</td><td>Normal</td><td>Normal o miosis</td><td><b>Miosis</b>, irregular por sinequias{T}</td><td><b>Semimidriática fija</b></td></tr>
      <tr><td>Cámara anterior</td><td>Normal</td><td>Normal o hipopión</td><td>Células y flare, hipopión</td><td><b>Estrecha</b></td></tr>
      <tr><td>PIO</td><td>Normal</td><td>Normal</td><td>Normal, baja o alta</td><td><b>Muy alta</b> (≥ 50–60)</td></tr>
      <tr><td>Qué hacer</td><td>Médico general: higiene, lubricante, antibiótico o antialérgico según el tipo</td><td>Referir el mismo día; cultivo; antibiótico tópico frecuente; nada de esteroide</td><td>Referir; esteroide tópico + ciclopléjico (medir PIO)</td><td><b>Urgencia</b>: bajar PIO ya y referir para iridotomía</td></tr>
    </table></div>
    <h4>Otros ojos rojos{T}</h4>
    <div class="tbl"><table>
      <tr><th>Cuadro</th><th>Claves</th></tr>
      <tr><td>Hemorragia subconjuntival</td><td>Mancha roja lisa, sin dolor ni baja visual; tos, pujo, HTA, anticoagulantes. Se reabsorbe en 2–3 semanas; medir la presión si se repite</td></tr>
      <tr><td>Epiescleritis</td><td>Sector rojo, molestia leve; los vasos se blanquean con fenilefrina; autolimitada</td></tr>
      <tr><td>Escleritis</td><td>Dolor profundo que despierta al paciente, rojo violáceo; asociada a artritis reumatoide y vasculitis; tratamiento sistémico</td></tr>
      <tr><td>Quemadura química</td><td>Álcali peor que ácido: <b>irrigar de inmediato</b> antes de explorar, hasta pH 7–7.5</td></tr>
    </table></div>
    <div class="note"><b>Datos de alarma: referir</b>Dolor intenso, baja visual, fotofobia, pupila anormal, halos, córnea opaca o que tiñe, usuario de lentes de contacto, trauma o químico, recién nacido, o un ojo rojo que no mejora en 1 semana{T}.</div>
    <div class="key"><b>Regla rápida</b>Ve bien + pupila normal + córnea transparente = conjuntivitis. Si falla cualquiera de las tres, no es "solo conjuntivitis".</div>
'''),
('Fármacos en oftalmología: dosis', 'farmacos', f'''
    <p>Dosis de referencia en adultos{T}, para tenerlas a la mano. Confirma siempre con la guía y la ficha técnica vigentes. "1 gota c/8 h" = en el ojo afectado.</p>
    <h4>Antibióticos</h4>
    <div class="tbl"><table>
      <tr><th>Fármaco</th><th>Para qué</th><th>Dosis habitual</th><th>Ojo con</th></tr>
      <tr><td>Moxifloxacino 0.5% gotas</td><td>Conjuntivitis bacteriana; queratitis bacteriana</td><td>Conjuntivitis: 1 gota c/8 h por 7 días. Queratitis: 1 gota cada hora al inicio</td><td>Primera línea en usuarios de lentes de contacto (cubre <i>Pseudomonas</i>)</td></tr>
      <tr><td>Ciprofloxacino 0.3% gotas</td><td>Conjuntivitis bacteriana, úlcera corneal</td><td>1–2 gotas c/2 h despierto por 2 días, luego c/4 h por 5 días</td><td>Puede dejar precipitado blanco en la córnea</td></tr>
      <tr><td>Tobramicina 0.3% gotas</td><td>Conjuntivitis bacteriana</td><td>1–2 gotas c/4 h (leve) o cada hora (grave)</td><td>Toxicidad epitelial si se usa mucho tiempo</td></tr>
      <tr><td>Cloranfenicol 0.5% gotas</td><td>Conjuntivitis bacteriana</td><td>1 gota c/4–6 h por 7 días</td><td>Muy usado en México; reacción idiosincrática rara</td></tr>
      <tr><td>Eritromicina 0.5% ungüento</td><td>Profilaxis neonatal; blefaritis; niños</td><td>Neonato: una aplicación al nacer. Blefaritis: en el borde del párpado 1–2 veces al día</td><td>No sirve como profilaxis de clamidia</td></tr>
      <tr><td>Fortificados (vancomicina 25–50 mg/ml + ceftazidima 50 mg/ml)</td><td>Úlcera bacteriana grande o central</td><td>1 gota cada hora, alternando</td><td>Se preparan en farmacia hospitalaria</td></tr>
      <tr><td>Ceftriaxona</td><td>Conjuntivitis gonocócica</td><td>Adulto: 1 g IM dosis única. Neonato: 25–50 mg/kg IV o IM dosis única (máx. 125 mg)</td><td>Agregar lavados frecuentes con solución salina</td></tr>
      <tr><td>Azitromicina VO</td><td>Conjuntivitis de inclusión del adulto (clamidia); tracoma</td><td>1 g dosis única (tracoma: 20 mg/kg dosis única)</td><td>Tratar a la pareja</td></tr>
      <tr><td>Eritromicina VO</td><td>Conjuntivitis neonatal por clamidia</td><td>50 mg/kg/día en 4 dosis por 14 días</td><td>Riesgo de estenosis pilórica en menores de 6 semanas</td></tr>
      <tr><td>Doxiciclina VO</td><td>Clamidia del adulto; meibomitis, rosácea ocular</td><td>Clamidia: 100 mg c/12 h por 7 días. Meibomitis: 100 mg al día por 4–6 semanas</td><td>No en embarazo ni menores de 8 años</td></tr>
    </table></div>
    <h4>Antivirales y antifúngicos</h4>
    <div class="tbl"><table>
      <tr><th>Fármaco</th><th>Para qué</th><th>Dosis habitual</th><th>Ojo con</th></tr>
      <tr><td>Ganciclovir 0.15% gel</td><td>Queratitis herpética epitelial (dendrita)</td><td>1 gota 5 veces al día hasta que cierre la úlcera, luego 3 veces al día por 7 días</td><td><b>Nunca esteroide</b> en la dendrita</td></tr>
      <tr><td>Aciclovir 3% ungüento</td><td>Queratitis herpética epitelial</td><td>5 veces al día por 10–14 días</td><td>Puede no estar disponible en todos lados</td></tr>
      <tr><td>Aciclovir VO</td><td>Herpes simple ocular; herpes zóster oftálmico</td><td>Herpes simple: 400 mg 5 veces al día por 7–10 días. Zóster: 800 mg 5 veces al día por 7–10 días</td><td>Zóster: iniciar en las primeras 72 h; ajustar en insuficiencia renal</td></tr>
      <tr><td>Valaciclovir VO</td><td>Herpes zóster oftálmico</td><td>1 g c/8 h por 7 días</td><td>Alternativa con menos tomas</td></tr>
      <tr><td>Natamicina 5% suspensión</td><td>Queratitis por hongos filamentosos (<i>Fusarium</i>)</td><td>1 gota cada 1–2 h al inicio</td><td>Penetra poco; tratamientos largos</td></tr>
    </table></div>
    <h4>Antialérgicos y antiinflamatorios</h4>
    <div class="tbl"><table>
      <tr><th>Fármaco</th><th>Para qué</th><th>Dosis habitual</th><th>Ojo con</th></tr>
      <tr><td>Olopatadina 0.1% gotas</td><td>Conjuntivitis alérgica</td><td>1 gota c/12 h (la de 0.2%, 1 vez al día)</td><td>Antihistamínico + estabilizador de mastocitos</td></tr>
      <tr><td>Ketotifeno 0.025% gotas</td><td>Conjuntivitis alérgica</td><td>1 gota c/12 h</td><td>Ardor al aplicar</td></tr>
      <tr><td>Cromoglicato de sodio 2–4%</td><td>Prevención en alergia estacional</td><td>1–2 gotas 4 veces al día</td><td>Tarda días en hacer efecto</td></tr>
      <tr><td>Ketorolaco 0.4–0.5% gotas</td><td>Dolor e inflamación; alergia si no se puede usar esteroide</td><td>1 gota c/6–8 h</td><td>Uso prolongado: daño corneal</td></tr>
      <tr><td>Fluorometolona 0.1% o loteprednol 0.5%</td><td>Alergia intensa, inflamación leve</td><td>1 gota c/6–12 h, máximo unas 2 semanas</td><td>Esteroides "suaves"; descartar úlcera antes</td></tr>
      <tr><td>Prednisolona acetato 1%</td><td>Uveítis anterior; inflamación posquirúrgica</td><td>Uveítis: 1 gota cada 1–2 h despierto y bajar poco a poco</td><td>Sube la PIO, causa catarata, empeora herpes y hongos. No suspender de golpe</td></tr>
    </table></div>
    <h4>Glaucoma</h4>
    <div class="tbl"><table>
      <tr><th>Fármaco</th><th>Cómo baja la PIO</th><th>Dosis habitual</th><th>Ojo con</th></tr>
      <tr><td>Latanoprost 0.005%</td><td>Prostaglandina: aumenta la salida (vía uveoescleral)</td><td>1 gota en la noche</td><td>Oscurece el iris, alarga las pestañas; evitar con uveítis</td></tr>
      <tr><td>Timolol 0.5%</td><td>Betabloqueador: baja la producción</td><td>1 gota c/12 h</td><td>Contraindicado en asma, EPOC, bradicardia y bloqueo AV</td></tr>
      <tr><td>Brimonidina 0.2%</td><td>Agonista alfa-2: baja la producción</td><td>1 gota c/8–12 h</td><td>Contraindicada en menores de 2 años (apnea, somnolencia); alergia ocular, boca seca</td></tr>
      <tr><td>Dorzolamida 2%</td><td>Inhibidor de anhidrasa carbónica tópico</td><td>1 gota c/8 h (c/12 h junto con timolol)</td><td>Sabor amargo; es sulfonamida</td></tr>
      <tr><td>Acetazolamida</td><td>Inhibidor de anhidrasa carbónica sistémico</td><td>Cierre agudo: 500 mg IV o VO de inicio, luego 250 mg c/6 h</td><td>Alergia a sulfas, insuficiencia renal o hepática; hipopotasemia, parestesias</td></tr>
      <tr><td>Manitol 20%</td><td>Osmótico: saca agua del vítreo</td><td>1–2 g/kg IV en 30–45 min</td><td>Insuficiencia cardiaca o renal</td></tr>
      <tr><td>Pilocarpina 1–2%</td><td>Miótico: jala el iris y abre el ángulo</td><td>Cierre agudo: 1 gota, repetir a los 15 min, cuando la PIO ya empezó a bajar; luego c/6 h hasta la iridotomía</td><td>Con PIO muy alta el esfínter está isquémico y no responde; cefalea</td></tr>
    </table></div>
    <h4>Midriáticos, ciclopléjicos y diagnóstico</h4>
    <div class="tbl"><table>
      <tr><th>Fármaco</th><th>Para qué</th><th>Dosis habitual</th><th>Ojo con</th></tr>
      <tr><td>Tropicamida 1%</td><td>Dilatar para ver el fondo</td><td>1 gota, repetir a los 5 min si hace falta; dura 4–6 h</td><td>Ángulo estrecho; no manejar con la pupila dilatada</td></tr>
      <tr><td>Fenilefrina 2.5%</td><td>Dilatar (alfa-1), se suma a la tropicamida</td><td>1 gota</td><td>La de 10% puede subir la presión arterial; cuidado en cardiópatas y lactantes</td></tr>
      <tr><td>Ciclopentolato 1%</td><td>Refracción con cicloplejía en niños; uveítis</td><td>Refracción: 1 gota y otra a los 5 min, medir a los 30–45 min. Uveítis: c/8 h</td><td>Efectos anticolinérgicos en niños pequeños</td></tr>
      <tr><td>Atropina 1%</td><td>Uveítis (alivia el espasmo ciliar, evita sinequias); penalización en ambliopía</td><td>1 gota c/12–24 h; su efecto dura 7–14 días</td><td>Miopía en niños: atropina 0.01% 1 gota en la noche (baja dosis)</td></tr>
      <tr><td>Tetracaína o proparacaína 0.5%</td><td>Anestesia para explorar, tonometría o sacar cuerpo extraño</td><td>1 gota justo antes</td><td><b>Nunca se receta</b>: su uso repetido destruye el epitelio y causa úlceras</td></tr>
      <tr><td>Fluoresceína (tira o 2%)</td><td>Teñir úlceras, Seidel, tonometría</td><td>Humedecer la tira y tocar el fondo de saco</td><td>Mancha los lentes de contacto blandos</td></tr>
    </table></div>
    <h4>Lubricantes, intravítreos y sistémicos</h4>
    <div class="tbl"><table>
      <tr><th>Fármaco</th><th>Para qué</th><th>Dosis habitual</th><th>Ojo con</th></tr>
      <tr><td>Carboximetilcelulosa 0.5% o hialuronato 0.1–0.2%</td><td>Ojo seco, apoyo en conjuntivitis</td><td>1 gota 4–6 veces al día; gel o ungüento en la noche</td><td>Si se usa más de 4 veces al día, sin conservadores</td></tr>
      <tr><td>Anti-VEGF intravítreo (bevacizumab 1.25 mg, ranibizumab 0.5 mg, aflibercept 2 mg)</td><td>Edema macular diabético, retinopatía proliferativa, DMAE húmeda</td><td>Inyección mensual al inicio y luego según la respuesta</td><td>Riesgo de endoftalmitis con cada inyección</td></tr>
      <tr><td>Vancomicina 1 mg + ceftazidima 2.25 mg intravítreas</td><td>Endoftalmitis bacteriana</td><td>Dosis única en 0.1 ml cada una, tras tomar muestra del vítreo</td><td>Urgencia oftalmológica</td></tr>
      <tr><td>Metilprednisolona IV y prednisona VO</td><td>Arteritis de células gigantes con pérdida visual</td><td>Metilprednisolona 1 g IV al día por 3 días, luego prednisona 1 mg/kg/día (máx. 60 mg)</td><td>Empezar <b>antes</b> de la biopsia; protege el otro ojo</td></tr>
    </table></div>
    <div class="note"><b>Tres reglas de seguridad</b>No recetar anestésico tópico. No dar esteroide en un ojo rojo sin diagnóstico (herpes, hongos, glaucoma). Medir la PIO antes y durante un esteroide.</div>
'''),
]

# ---------- Bloque 07: casos clínicos ----------
# (título del caso, viñeta, [(pregunta, [opciones], índice correcto, explicación), ...])
CASOS = [
('Ojo rojo muy doloroso con halos y vómito',
 'Mujer de 64 años, hipermétrope, que salió del cine con dolor intenso en el ojo derecho, cefalea, náusea y vómito. Ve halos de colores alrededor de las luces. El ojo está rojo, la córnea empañada y la pupila semidilatada, sin respuesta a la luz. Al palpar, el ojo se siente duro.',
 [('¿Cuál es el diagnóstico más probable?', ['Conjuntivitis bacteriana', 'Glaucoma agudo por cierre angular', 'Uveítis anterior aguda', 'Migraña con aura'], 1,
   'Ojo rojo doloroso, halos, edema corneal, pupila semimidriática fija y ojo duro en una hipermétrope que estuvo en la oscuridad (la pupila se dilata y cierra el ángulo).'),
  ('¿Qué haces primero?', ['Dilatar la pupila para ver el fondo de ojo', 'Dar antibiótico tópico y citar en una semana', 'Bajar la PIO (acetazolamida, timolol, manitol) y referir urgente para iridotomía láser', 'Esteroide tópico cada hora'], 2,
   'Es una urgencia: se baja la PIO con fármacos y el bloqueo se resuelve con iridotomía YAG láser. Dilatar empeora el cierre. Al otro ojo también se le hace iridotomía preventiva†.')]),
('Usuaria de lentes de contacto con dolor y mancha blanca',
 'Mujer de 23 años que duerme con sus lentes de contacto blandos. Tiene 2 días con dolor intenso, fotofobia, lagrimeo y baja visual en el ojo izquierdo. Se ve una mancha blanca en la córnea que tiñe con fluoresceína y un poco de pus en la cámara anterior.',
 [('¿Qué tiene?', ['Conjuntivitis alérgica', 'Queratitis bacteriana (pensar en Pseudomonas)', 'Pterigión', 'Hemorragia subconjuntival'], 1,
   'Infiltrado corneal que tiña + hipopión + uso de lentes de contacto = queratitis bacteriana; en usuarios de lentes, Pseudomonas es la clásica†.'),
  ('¿Cuál es la conducta correcta?', ['Parche ocular cerrado y esteroide', 'Retirar los lentes, tomar cultivo y dar fluoroquinolona tópica cada hora; referir el mismo día', 'Recetar anestésico tópico para el dolor', 'Solo lubricante y observar'], 1,
   'Antibiótico de amplio espectro sin esperar el Gram, frecuente. Nunca parchar (favorece la infección†), nunca recetar anestésico, sin esteroide al inicio.')]),
('Pérdida súbita de la visión, sin dolor',
 'Hombre de 68 años, hipertenso y fumador, que al despertar no ve con el ojo derecho. No le duele. Agudeza visual: cuenta dedos. Defecto pupilar aferente en ese ojo. En el fondo de ojo, la retina se ve pálida y la fóvea resalta como una mancha roja.',
 [('¿Diagnóstico?', ['Desprendimiento de retina', 'Oclusión de la arteria central de la retina', 'Glaucoma de ángulo abierto', 'Catarata madura'], 1,
   'Pérdida súbita e indolora + retina pálida + mancha rojo cereza en la fóvea (la coroides se ve a través de la retina más delgada)†.'),
  ('Además de referir urgente, ¿qué estudio no puede faltar?', ['Ecografía de carótidas y estudio cardiovascular (es un "infarto" del ojo)', 'Radiografía de tórax de rutina', 'Cultivo conjuntival', 'Campimetría en 6 meses'], 0,
   'Es un evento embólico: hay que buscar la fuente (carótidas, corazón) como en un ictus†. En mayores de 50 descarta también arteritis de células gigantes (VSG, PCR).')]),
('Destellos, moscas volantes y una cortina',
 'Hombre de 45 años con miopía alta. Desde ayer ve destellos de luz y muchas "moscas" oscuras en el ojo izquierdo; hoy siente que una sombra como cortina le tapa la parte de arriba de la visión.',
 [('¿Qué sospechas?', ['Desprendimiento de retina regmatógeno', 'Conjuntivitis viral', 'Presbicia', 'Neuritis óptica'], 0,
   'Fotopsias + miodesopsias + cortina en un miope alto = desprendimiento de retina. La cortina de arriba suele venir de un desprendimiento inferior†.'),
  ('¿Qué conducta es la correcta?', ['Lentes nuevos', 'Referencia urgente a retina para cirugía', 'Antibiótico tópico', 'Repetir la revisión en 3 meses'], 1,
   'Es urgente, sobre todo si la mácula aún no se despega: el pronóstico visual depende de operar a tiempo (cerclaje, vitrectomía o neumorretinopexia†).')]),
('Cefalea, mandíbula que se cansa y baja visual',
 'Mujer de 76 años con cefalea temporal nueva, dolor al peinarse, cansancio de la mandíbula al masticar y dolor de hombros. Hoy perdió la visión del ojo derecho. La papila de ese ojo se ve pálida e hinchada. VSG de 95 mm/h.',
 [('¿Diagnóstico?', ['Neuropatía óptica isquémica por arteritis de células gigantes', 'Migraña ocular', 'Glaucoma de tensión normal', 'Conjuntivitis bacteriana'], 0,
   'Edad > 50, cefalea temporal, claudicación mandibular, polimialgia y VSG alta: arteritis de células gigantes (temporal)†.'),
  ('¿Qué haces?', ['Esperar la biopsia de la arteria temporal para tratar', 'Esteroides a dosis altas de inmediato y luego biopsia', 'Aspirina sola', 'Antibiótico IV'], 1,
   'Se tratan antes de la biopsia (la biopsia sigue saliendo positiva días después): el objetivo es salvar el otro ojo†.')]),
('Ojo rojo con lagrimeo después de un catarro',
 'Estudiante de 19 años con 3 días de ojo rojo, primero el derecho y ahora los dos. Lagrimea mucho, siente arenilla y casi no tiene comezón. Ve bien. Hay un ganglio preauricular doloroso. Su compañero de cuarto tuvo lo mismo.',
 [('¿Qué tipo de conjuntivitis es?', ['Bacteriana', 'Viral (adenovirus)', 'Alérgica', 'Gonocócica'], 1,
   'Lagrimeo profuso + ganglio preauricular + contagio + antecedente de vías respiratorias = viral por adenovirus.'),
  ('¿Qué le indicas?', ['Esteroide tópico', 'Antibiótico oral', 'Compresas frías, lubricante, lavado de manos y no compartir toallas', 'Anestésico tópico'], 2,
   'Es autolimitada (1–3 semanas). El antibiótico no sirve y el esteroide sin diagnóstico es peligroso. Muy contagiosa: higiene†.')]),
('Recién nacido con mucho pus en los ojos',
 'Recién nacido de 3 días, parto vaginal, madre sin control prenatal. Tiene ambos ojos muy inflamados, párpados hinchados y secreción purulenta abundante que vuelve a salir al limpiarla.',
 [('¿Qué agente sospechas por el tiempo y el cuadro?', ['Chlamydia trachomatis', 'Neisseria gonorrhoeae', 'Conjuntivitis química por profilaxis', 'Adenovirus'], 1,
   'Hiperaguda con pus profuso en los primeros 2–5 días = gonococo. La clamidia aparece más tarde (5–14 días) y la química en las primeras 24 h†.'),
  ('¿Cuál es el tratamiento?', ['Solo ungüento de eritromicina', 'Ceftriaxona IV o IM dosis única + lavados frecuentes con solución salina', 'Esteroide tópico', 'Esperar el cultivo'], 1,
   'Ceftriaxona 25–50 mg/kg (máx. 125 mg) dosis única; riesgo de perforación corneal. Tratar a la madre y su pareja†.')]),
('Joven con lumbalgia y ojo rojo con fotofobia',
 'Hombre de 28 años con dolor lumbar de años que mejora con el ejercicio. Ahora tiene dolor en el ojo derecho, mucha fotofobia y visión algo borrosa. Inyección ciliar violácea, pupila pequeña e irregular y células en la cámara anterior.',
 [('¿Diagnóstico?', ['Uveítis anterior aguda (asociada a HLA-B27)', 'Conjuntivitis alérgica', 'Glaucoma agudo', 'Orzuelo'], 0,
   'Ojo rojo doloroso con fotofobia, miosis y células en la cámara anterior en un paciente con espondilitis anquilosante (HLA-B27)†.'),
  ('¿Qué tratamiento inicial es el adecuado?', ['Pilocarpina', 'Esteroide tópico (prednisolona) + ciclopléjico, midiendo la PIO', 'Solo antibiótico tópico', 'Lentes oscuros y nada más'], 1,
   'El esteroide calma la inflamación y el ciclopléjico quita el dolor y evita sinequias. La pilocarpina (miótico) empeora la uveítis.')]),
('Diabético que nunca se ha revisado los ojos',
 'Hombre de 52 años con diabetes tipo 2 de 12 años de evolución, mal controlada. Nunca ha ido al oftalmólogo. En el fondo de ojo hay microaneurismas, hemorragias, exudados duros y vasos nuevos sobre la papila.',
 [('¿En qué etapa está?', ['Retinopatía no proliferativa leve', 'Retinopatía diabética proliferativa', 'Retina normal', 'Retinopatía hipertensiva grado I'], 1,
   'Los neovasos (por VEGF liberado por la isquemia) definen la etapa proliferativa.'),
  ('¿Qué tratamiento corresponde?', ['Solo mejorar la glucosa y revisar en 2 años', 'Panfotocoagulación láser y/o anti-VEGF intravítreo, además del control metabólico', 'Lentes', 'Antibiótico tópico'], 1,
   'La panfotocoagulación quita el estímulo isquémico; el anti-VEGF frena los neovasos y el edema macular†. Todo diabético tipo 2 se revisa al diagnóstico y luego cada año†.')]),
('Niño con fiebre, ojo salido y dolor al moverlo',
 'Niño de 7 años con sinusitis desde hace una semana. Ahora tiene fiebre, párpados del ojo izquierdo muy hinchados y rojos, el ojo está salido hacia adelante, le duele moverlo y ve menos.',
 [('¿Celulitis preseptal u orbitaria?', ['Preseptal: es solo el párpado', 'Orbitaria: hay proptosis, dolor y limitación al mover el ojo y baja visual', 'Ninguna, es conjuntivitis', 'Orzuelo'], 1,
   'Regla rápida de tu guía: si mueve bien el ojo, ve bien y no hay proptosis, es preseptal. Aquí falla todo: es orbitaria (90% por sinusitis etmoidal).'),
  ('¿Qué sigue?', ['Antibiótico VO en casa', 'Hospitalizar, TC de órbitas y antibióticos IV', 'Compresas calientes', 'Esteroide tópico'], 1,
   'Hospitalizar siempre; TAC orbitocraneal para buscar absceso; vancomicina + ceftazidima + metronidazol IV. Riesgo de trombosis del seno cavernoso.')]),
('Dolor y lagrimeo con una figura ramificada',
 'Mujer de 35 años con antecedente de "fuegos" en el labio. Tiene 2 días con ojo rojo, lagrimeo y sensación de cuerpo extraño. Con fluoresceína se ve una úlcera ramificada. La sensibilidad de la córnea está disminuida.',
 [('¿Diagnóstico?', ['Queratitis por herpes simple', 'Queratitis por hongos', 'Abrasión corneal', 'Conjuntivitis alérgica'], 0,
   'Dendrita con fluoresceína + hipoestesia corneal = herpes simple (unilateral en 90%).'),
  ('¿Qué está contraindicado?', ['Ganciclovir gel', 'Aciclovir oral', 'Esteroide tópico', 'Ciclopléjico'], 2,
   'El esteroide en la queratitis epitelial herpética hace crecer la úlcera (úlcera geográfica) y puede perforar.')]),
('Salpicadura de cal en el ojo',
 'Albañil de 40 años al que le salpicó cal en el ojo derecho hace 10 minutos. Llega con mucho dolor, blefaroespasmo y ojo rojo.',
 [('¿Qué haces primero?', ['Medir la agudeza visual y hacer la historia clínica completa', 'Irrigar de inmediato con solución salina o Ringer (litros) hasta pH neutro', 'Parche y referir', 'Antibiótico tópico'], 1,
   'En las quemaduras químicas se irriga antes de cualquier otra cosa, incluso antes de medir la visión. Los álcalis (cal, cemento) penetran más que los ácidos†.'),
  ('¿Qué hallazgo indica peor pronóstico?', ['Hiperemia conjuntival', 'Isquemia del limbo (conjuntiva blanca alrededor de la córnea)', 'Lagrimeo', 'Fotofobia'], 1,
   'Un limbo blanco y sin vasos significa que se dañaron las células madre del epitelio corneal†: la córnea no podrá repararse bien.')]),
]
CASOS_T = 'Casos clínicos'

CARDS = [
('b6', '¿Cómo se anota una agudeza de 20/200 que con estenopeico mejora a 20/70 y una letra más?', '20/200 (.) 20/70+1'),
('b6', 'Si el paciente no lee la letra más grande de Snellen, ¿qué sigue?', 'Acercar la cartilla, luego cuenta dedos (CD), movimiento de manos (MM), percepción de luz (PL) y no percibe luz (NPL).'),
('b6', '¿Cuáles son los 3 sistemas de la lámpara de hendidura?', 'Óptico, luminoso y mecánico.'),
('b6', '¿Cuánto debe durar el tiempo de ruptura de la lágrima según tus apuntes?', 'No menos de 15 segundos.'),
('b6', 'Fluoresceína, rosa de bengala y verde de lisamina: ¿qué evalúa cada una?', 'Fluoresceína: úlceras. Rosa de bengala: moco. Verde de lisamina: moco y células muertas.'),
('b6', 'Células vs flare en la cámara anterior', 'Células (Tyndall, partículas) = inflamación. Flare (como humo) = proteínas en el acuoso.'),
('b6', 'Oftalmoscopía directa vs indirecta: imagen y dilatación', 'Directa: imagen grande y derecha, monocular, sin dilatar. Indirecta: imagen al revés en 3D, binocular, más campo, requiere dilatar.'),
('b6', 'En el oftalmoscopio, ¿qué lentes son para el miope?', 'Los rojos (negativos). Los verdes (positivos) para el hipermétrope.'),
('b6', '¿Qué estudio pides para ver la mácula o la capa de fibras nerviosas?', 'OCT (tomografía de coherencia óptica).'),
('b6', '¿Qué estudio pides si no se ve el fondo de ojo por catarata densa o hemorragia?', 'Ecografía modo B.'),
('b5', 'Regla rápida para saber si un ojo rojo es "solo conjuntivitis"', 'Ve bien + pupila normal + córnea transparente. Si falla una, hay algo más profundo.'),
('b5', 'Pupila en uveítis anterior vs glaucoma agudo', 'Uveítis: miosis. Glaucoma agudo: semimidriática fija.'),
('b5', '¿Por qué nunca se receta anestésico tópico?', 'Su uso repetido destruye el epitelio corneal y causa úlceras.'),
('b5', 'Dosis de timolol 0.5% y su contraindicación clave', '1 gota c/12 h; contraindicado en asma, EPOC, bradicardia y bloqueo AV.'),
('b5', 'Dosis de acetazolamida en el cierre angular agudo', '500 mg IV o VO de inicio, luego 250 mg c/6 h.'),
('b5', 'Tratamiento de la conjuntivitis gonocócica del adulto', 'Ceftriaxona 1 g IM dosis única + lavados.'),
('b7', 'Mancha rojo cereza con retina pálida y pérdida súbita indolora', 'Oclusión de la arteria central de la retina.'),
('b7', 'Fotopsias + miodesopsias + cortina', 'Desprendimiento de retina: referencia urgente.'),
('b7', 'Quemadura química del ojo: primer paso', 'Irrigar de inmediato hasta pH neutro, antes de explorar.'),
]
QUIZ = [
('b6', 'Si la visión mejora con el agujero estenopeico, el problema es:', ['Refractivo', 'De la retina', 'Del nervio óptico', 'De la córnea por úlcera'], 0, 'El estenopeico corrige el error refractivo; si no mejora, busca otra causa.'),
('b6', 'Pus en la cámara anterior se llama:', ['Hipema', 'Hipopión', 'Flare', 'Sinequia'], 1, 'Hipopión = pus; hipema = sangre.'),
('b6', 'La PIO normal es de:', ['5–10 mmHg', '10–21 mmHg', '21–30 mmHg', '30–40 mmHg'], 1, 'Arriba de 21 sin daño del nervio = hipertensión ocular.'),
('b6', 'La oftalmoscopía indirecta, comparada con la directa:', ['Da imagen derecha y monocular', 'No necesita dilatar', 'Da imagen al revés, binocular y con más campo', 'Tiene más aumento'], 2, 'La directa aumenta más; la indirecta da campo y 3D.'),
('b6', 'Antes de dilatar a un paciente hay que valorar:', ['La agudeza de cerca', 'La profundidad de la cámara anterior', 'La visión al color', 'El reflejo corneal'], 1, 'Con ángulo estrecho, dilatar puede causar un cierre angular agudo.'),
('b5', 'Ojo rojo con córnea que tiñe con fluoresceína y fotofobia intensa:', ['Conjuntivitis alérgica', 'Queratitis', 'Hemorragia subconjuntival', 'Pinguécula'], 1, 'La córnea que tiñe indica lesión del epitelio.'),
('b5', '¿Cuál de estos se contraindica en menores de 2 años?', ['Latanoprost', 'Brimonidina', 'Timolol', 'Dorzolamida'], 1, 'La brimonidina puede dar apnea y somnolencia en lactantes.'),
('b5', 'Fármaco contraindicado en la queratitis herpética epitelial:', ['Ganciclovir gel', 'Prednisolona tópica', 'Aciclovir oral', 'Lubricante'], 1, 'El esteroide hace crecer la dendrita.'),
('b7', 'Mujer hipermétrope con ojo rojo, halos, vómito y pupila semidilatada fija. Primer paso:', ['Dilatar', 'Bajar la PIO y referir para iridotomía', 'Antibiótico', 'Esteroide tópico'], 1, 'Glaucoma agudo por cierre angular: urgencia.'),
('b7', 'Adulta mayor con cefalea temporal, claudicación mandibular y pérdida visual:', ['Biopsia y luego tratar', 'Esteroides de inmediato', 'Aspirina', 'Observar'], 1, 'Arteritis de células gigantes: tratar antes de la biopsia.'),
('b7', 'Recién nacido de 3 días con pus abundante en ambos ojos:', ['Clamidia', 'Gonococo', 'Química', 'Adenovirus'], 1, 'Hiperaguda en los primeros días = gonococo; ceftriaxona.'),
]

# Términos para el botón de AMBOSS (tools-amboss/terminos.tsv)
AMBOSS = [
('Agudeza visual: cómo se mide y se anota', 'visual acuity'),
('Lámpara de hendidura (biomicroscopía)', 'slit lamp examination'),
('Tonometría y presión intraocular', 'tonometry intraocular pressure'),
('Oftalmoscopía directa e indirecta', 'ophthalmoscopy'),
('OCT y otros estudios de imagen', 'optical coherence tomography'),
('Ojo rojo: tabla comparativa', 'red eye'),
('Fármacos en oftalmología: dosis', 'ophthalmic drugs'),
('Casos clínicos', '-'),
]
