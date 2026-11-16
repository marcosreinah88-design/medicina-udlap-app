# Imágenes de Gastroenterología (5º)

Imágenes de referencia y esquemas propios para `site/s5/gastro/` y `site/s5/hepatobiliar/` (que comparte los 11 temas del Bloque III).

- `fotos.py`: recorta las figuras de OpenStax (Anatomy & Physiology 2e y Microbiology, CC BY 4.0; muchas fotos son de CDC/NIH, dominio público), borra los rótulos en inglés y los escribe en español. Los originales van en `orig/` (no se suben): se bajan con `git clone --filter=blob:none --no-checkout --depth 1 https://github.com/openstax/osbooks-anatomy-physiology` (y `osbooks-microbiology`) + `git checkout HEAD -- media/<archivo>`. Se evitan las micrografías «Regents of University of Michigan ©».
- `esquemas.py`: 9 esquemas propios en SVG en línea (usan las clases `fx-*` de la guía, así respetan el modo oscuro).
- `imagenes.tsv`: tema → apartado (título exacto), archivo o esquema, pie y crédito.
- `patch.py [index.html ...]`: idempotente (marca `data-gx`). Copia las fotos a `s5/gastro/img/ref/`; Hepatobiliar las toma de `../gastro/img/ref/` y recibe el visor para ampliar. Sirve igual para la copia del artefacto.

Después: `node tools-buscador/apartados.js` y `python3 tools-subrayar/firmar.py <clave.pem>`.
