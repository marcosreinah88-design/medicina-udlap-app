# Contexto para Claude (leer primero)

Resumen corto del proyecto para no re-explorar el repo en cada pedido. Autor de todo: **Marcos David Reinah Guzmán** (Medicina, UDLAP). Repo público: aquí NO van claves ni datos personales.

## Qué es
- Página "Carrera de Medicina": hub con 1º–8º semestre + MIP + SS (1º, 2º, 7º, 8º = "Pronto"; `SEM_ACTUAL=5`). Cada semestre abre su página original en iframe (`site/sN/index.html`).
- Se publica como artefacto de claude.ai y se copia aquí en `site/` para la app de Mac y la versión del cel.

## Estructura
| Ruta | Qué es |
|---|---|
| `site/index.html` | Hub para la app de Mac (todo en un archivo, ~740 KB). |
| `site/app.html` | Mismo hub para el cel (PWA, `pwa.js`, `sw.js`, `app.webmanifest`). |
| `site/s3` `s4` `s5` `s6` | Semestres: 3º archivero (anatomía, farmacología), 4º carpeta (`apps/`), 5º estante (cirugía, duelo, esófago, gastro, hepatobiliar, imagenología, oftalmo, otorrino, psiquiatría, quiz-hepatico), 6º anaquel (`artefactos/infectologia`, `salud-publica`). |
| `site/x/` | "Otros materiales" incrustados: geb, signos, svb, triage, triage-clase. |
| `pwa/sw.js`, `pwa/pwa.js` | Fuente del uso sin internet del cel. `build_site.py` los copia a `site/` (reemplazan los del hub). El sw guarda primero lo básico (portada, fonts, scripts) y luego el resto, reanudable; la versión la saca de `manifest.json`, así que no hay que cambiar nada al publicar. |
| `site/sync.js` | Sincronización Mac↔cel por gist cifrado (AES-256-GCM, llave HKDF de la clave de GitHub). |
| `site/estudio.js` | Sección **Estudio** (`#estudio`, botón junto a Calificaciones): tarjetas con repetición espaciada, modo examen con cronómetro y % de aciertos, contador Pomodoro por materia, notas rápidas por clase (botón "Mandar a Obsidian" → bóveda CASA, `Medicina/Notas de clase/<materia>`). También mete en Calificaciones la calculadora "¿Cuánto necesito sacar?" (pesos por parcial). Datos en `carrera-tarjetas`, `carrera-repaso`, `carrera-preguntas(-prog)`, `carrera-simulacros`, `carrera-estudio-tiempo`, `carrera-notas`, `carrera-parciales` (se sincronizan). |
| `site/estudio-banco.json` + `tools-estudio/` | Tarjetas y preguntas sacadas de las guías (`node tools-estudio/banco.js`; correrlo al agregar o cambiar una guía). `tools-estudio/patch_estudio.py` conecta estudio.js al hub (ruta, script y avisos "Repasa hoy" 5, 3 y 2 días antes de cada examen); re-aplicarlo si se rearma el hub. |
| `site/anim.js` + `tools-anim/` | Animaciones discretas: fundido al abrir semestres/guías/secciones, tarjetas que suben en cascada, aparición al hacer scroll en la portada, contadores de la franja naranja, respuesta sutil de botones, fundido al salir y la portada vuelve a entrar en cascada al regresar (el overlay ya tiene `hidden`; la clase `an-x` lo deja ver 260 ms) y, dentro de los iframes de semestres/guías/materiales, aparición de sus tarjetas (detectadas por sombra/esquinas), y el `#viewer` propio de cada semestre entra y sale suave al abrir/cerrar una guía (clases `an-vi`/`an-vx`); al volver al semestre sus tarjetas visibles entran en cascada (`__anReenter`, clase `an-ik`) al hacer scroll o cambiar de pestaña. Solo opacidad/desplazamiento (no toca colores ni modo oscuro), se apaga con "Reducir movimiento" y no cambia colores, letras ni acomodo de semestres/guías. `tools-anim/patch_anim.py` lo conecta al hub (después de estudio.js); re-aplicarlo si se rearma el hub. |
| `site/subrayar.js` + `tools-subrayar/` | **Subrayador**: dentro de semestres, guías y materiales, al seleccionar texto sale una barra con 4 colores; tocar un subrayado deja cambiar color o quitarlo; seleccionar texto ya subrayado muestra "Quitar", y la esquina de abajo a la izquierda dice "Quitar subrayados (n)" para borrar todos los de la página (pide confirmar). Se guarda por página en `carrera-subrayados` (se sincroniza Mac ↔ cel). `patch_subrayar.py` lo conecta a `site/index.html`, `site/app.html` (después de anim.js) y lo mete en línea en la copia del artefacto; `firmar.py <clave.pem>` rehace y firma el manifiesto. Re-aplicarlo si se rearma el hub. |
| `tools-sky/` | Cielo de la portada que sigue la hora real de Puebla, sin internet: amanecer (≈1 h antes a 3 h después de que sale el sol), día, atardecer (3 h antes a 1 h después de la puesta) y noche con estrellas y la luna en su fase real del día. La etiqueta del horizonte siempre dice a qué hora amaneció y atardeció hoy. Tocar el escudo (botón escondido) cambia a mano a la escena siguiente a la que se ve (amanecer → atardecer → noche → día; al dar la vuelta completa o al recargar vuelve a automático). `sky.css` + `sky.js` son la fuente; `patch_sky.py` los mete en `site/index.html`, `site/app.html` y en la copia del artefacto. Para probar: `window.__skyNow=new Date(...)` antes de cargar. |
| `site/assistant.js` | Asistente de exámenes/pendientes con Gemini (gratis). |
| `site/manifest.json` + `manifest.sig` | Lista sha256 de archivos + firma Ed25519. La app rechaza todo lo que no esté firmado. |
| `main.js`, `preload.js` | App de Mac (Electron, v1.4). Cambiarlos requiere zip nuevo. |
| `build_site.py` | `hub/` → `site/`, tipografías locales, manifest y firma. |
| `pack.py` | Arma los zips con el instalador `.command`. |
| `.github/workflows/pages.yml` | Publica `site/` en GitHub Pages (cel) al cambiar `site/**` en `main`. |
| `.github/workflows/avisos.yml` + `tools-push/` | Avisos push al cel (secreto `MED_SYNC`). Los dispara cron-job.org cada 5 min vía workflow_dispatch; el cron de GitHub (2 veces por hora) es solo respaldo. Guía: `docs/avisos-cron-job.md`. |

## Flujo de un cambio en la página
1. Editar y republicar el artefacto hub (las fuentes del hub se concatenan: head.html, data.js, ft.js, tail.js, cal.js, grades.js, horario.js, ajustes.js, ctolib.js, otroslib.js, material.js).
2. Si se rearma desde las fuentes, aplicar los parches de diseño en orden: `patch_calendario_v2.py` → `patch_portada_v2.py` → `patch_botones.py`, y luego los de `tools-estudio`, `tools-anim`, `tools-sky` y `tools-subrayar`.
3. `build_site.py` (necesita la clave privada de firma, que vive fuera del repo) y subir `site/` a `main` por PR. Mac y cel se actualizan solos.

## Reglas que no se rompen
- Todo el contenido vive dentro de la página (artefactos nuevos se incrustan). Excepciones: CTO (links a Drive) y la corona (solo link al artefacto "Plan de Volumen", nunca se incrusta).
- Cada semestre y cada guía conserva su diseño original. Colores UDLAP: verde `#00573c`, naranja `#f26b21`.
- Solo opciones gratis. Nada de datos personales (calificaciones, horario) ni claves en el código: el usuario los pega en la app.
- CSP: connect-src solo self, api.github.com, gist.githubusercontent.com, generativelanguage.googleapis.com. Un dominio nuevo va en `build_site.py` y `main.js`.
- Nunca subir la clave privada de firma, PDFs de CTO ni `seed-cto.json`.
- Mínima aprobatoria UDLAP 7.5; la carrera son 8 semestres + Internado + Servicio social (no hay 9º ni 10º).
