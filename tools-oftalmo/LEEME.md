# Imágenes de Oftalmología (5º)

Imágenes de referencia y esquemas propios para `site/s5/oftalmo/`.

- `fotos.py`: recorta las figuras de OpenStax (Anatomy & Physiology 2e y Microbiology, CC BY 4.0; varias fotos son de CDC, dominio público), borra los rótulos en inglés y los escribe en español (usa `relabel()` de `tools-gastro/fotos.py`). Los originales van en `orig/` (no se suben): `git clone --filter=blob:none --no-checkout --depth 1 https://github.com/openstax/osbooks-anatomy-physiology` (y `osbooks-microbiology`) + `git checkout HEAD -- media/<archivo>`. De la figura de bastones y conos solo va el dibujo: la micrografía es «Regents of University of Michigan ©».
- `esquemas.py`: 11 esquemas propios en SVG en línea con las clases `.dg` de la guía (respetan el modo oscuro). Lo que no viene de los apuntes va con †.
- `imagenes.tsv`: tema (inicio del título) → subtítulo h4 después del cual va (vacío = al final del tema), archivo o esquema, pie y crédito.
- `patch.py [index.html ...]`: idempotente (marca `data-ox`). Copia las fotos a `img/ref/` junto al index y agrega el visor para ampliar (`.ox-lb`; la guía ya usa `.lb` para rótulos SVG). Sirve igual para la copia del artefacto.

Después: `node tools-buscador/apartados.js` y `python3 tools-subrayar/firmar.py <clave.pem>`.
