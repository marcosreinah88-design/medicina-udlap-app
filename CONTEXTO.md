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
| `site/sync.js` | Sincronización Mac↔cel por gist cifrado (AES-256-GCM, llave HKDF de la clave de GitHub). |
| `site/assistant.js` | Asistente de exámenes/pendientes con Gemini (gratis). |
| `site/manifest.json` + `manifest.sig` | Lista sha256 de archivos + firma Ed25519. La app rechaza todo lo que no esté firmado. |
| `main.js`, `preload.js` | App de Mac (Electron, v1.4). Cambiarlos requiere zip nuevo. |
| `build_site.py` | `hub/` → `site/`, tipografías locales, manifest y firma. |
| `pack.py` | Arma los zips con el instalador `.command`. |
| `.github/workflows/pages.yml` | Publica `site/` en GitHub Pages (cel) al cambiar `site/**` en `main`. |
| `.github/workflows/avisos.yml` + `tools-push/` | Avisos push al cel cada ~10 min (secreto `MED_SYNC`). |

## Flujo de un cambio en la página
1. Editar y republicar el artefacto hub (las fuentes del hub se concatenan: head.html, data.js, ft.js, tail.js, cal.js, grades.js, horario.js, ajustes.js, ctolib.js, otroslib.js, material.js).
2. Si se rearma desde las fuentes, aplicar los parches de diseño en orden: `patch_calendario_v2.py` → `patch_portada_v2.py` → `patch_botones.py`.
3. `build_site.py` (necesita la clave privada de firma, que vive fuera del repo) y subir `site/` a `main` por PR. Mac y cel se actualizan solos.

## Reglas que no se rompen
- Todo el contenido vive dentro de la página (artefactos nuevos se incrustan). Excepciones: CTO (links a Drive) y la corona (solo link al artefacto "Plan de Volumen", nunca se incrusta).
- Cada semestre y cada guía conserva su diseño original. Colores UDLAP: verde `#00573c`, naranja `#f26b21`.
- Solo opciones gratis. Nada de datos personales (calificaciones, horario) ni claves en el código: el usuario los pega en la app.
- CSP: connect-src solo self, api.github.com, gist.githubusercontent.com, generativelanguage.googleapis.com. Un dominio nuevo va en `build_site.py` y `main.js`.
- Nunca subir la clave privada de firma, PDFs de CTO ni `seed-cto.json`.
- Mínima aprobatoria UDLAP 7.5; la carrera son 8 semestres + Internado + Servicio social (no hay 9º ni 10º).
