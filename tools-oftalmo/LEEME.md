# Imágenes de Oftalmología (5º)

Imágenes de referencia y esquemas propios para `site/s5/oftalmo/`.

- `fotos.py`: recorta las figuras de OpenStax (Anatomy & Physiology 2e y Microbiology, CC BY 4.0; varias fotos son de CDC, dominio público), borra los rótulos en inglés y los escribe en español (usa `relabel()` de `tools-gastro/fotos.py`). Los originales van en `orig/` (no se suben): `git clone --filter=blob:none --no-checkout --depth 1 https://github.com/openstax/osbooks-anatomy-physiology` (y `osbooks-microbiology`) + `git checkout HEAD -- media/<archivo>`. De la figura de bastones y conos solo va el dibujo: la micrografía es «Regents of University of Michigan ©».
- `esquemas.py`: 11 esquemas propios en SVG en línea con las clases `.dg` de la guía (respetan el modo oscuro). Lo que no viene de los apuntes va con †.
- `imagenes.tsv`: tema (inicio del título) → subtítulo h4 después del cual va (vacío = al final del tema), archivo o esquema, pie y crédito.
- `patch.py [index.html ...]`: idempotente (marca `data-ox`). Copia las fotos a `img/ref/` junto al index y agrega el visor para ampliar (`.ox-lb`; la guía ya usa `.lb` para rótulos SVG). Sirve igual para la copia del artefacto.

Después: `node tools-buscador/apartados.js` y `python3 tools-subrayar/firmar.py <clave.pem>`.

## Diagnóstico, ojo rojo, fármacos y casos clínicos (nov 2026)

- `diag_temas.py`: el contenido. Bloque 06: Agudeza visual (cómo se anota), Lámpara de hendidura, Tonometría, Oftalmoscopía directa e indirecta, OCT y otros estudios (de las notas de Notion › 7mo semestre › Oftalmología; lo demás con †). Bloque 05: Ojo rojo (tabla comparativa) y Fármacos con dosis. Bloque 07 nuevo: 12 casos clínicos con «Ponme a prueba» (2 preguntas cada uno; resultado guardado en `oft-casos`), más tarjetas y preguntas de quiz.
- `patch_diag.py [index.html ...]`: idempotente (marca `data-dx` y `/*dx*/`). Sirve igual para la copia del artefacto. `--amboss` pone los términos en `tools-amboss/terminos.tsv`.
- `buscador_oftalmo.py site/index.html site/app.html [artefacto]`: suma las palabras nuevas a la lista `oftalmo` del buscador.

Después: `python3 tools-amboss/build.py`, `node tools-estudio/banco.js`, `node tools-buscador/apartados.js` y firmar.
