# Imágenes de referencia de Imagenología (5º)

La guía `site/s5/imagenologia/` ya traía 354 imágenes del apunte. Aquí se agregan **imágenes de referencia** con pie y crédito (solo licencias libres) para los temas que no tenían o tenían pocas.

- `fotos.py <carpeta>`: recorta y traduce rótulos de las fotos originales (OpenStax CC BY 4.0, muchas de CDC/NIH/U.S. Navy en dominio público; una telerradiografía normal CC BY 3.0 del covid-19-image-repository). Los originales se bajan de GitHub (`git clone --filter=blob:none --no-checkout` de `openstax/osbooks-anatomy-physiology`, `osbooks-college-physics-bundle`, `osbooks-microbiology` + `git checkout HEAD -- media/<archivo>`). Wikimedia/NIH/Radiopaedia no se pueden abrir desde la nube.
- `esquemas.py`: esquemas propios en español (SVG): 5 densidades, Hounsfield, ecogenicidad, transductores, Doppler, T1/T2, fases de contraste, HSA + Fisher, edema, intra/extraaxial, BI-RADS, proyecciones de mama y línea del tiempo.
- `imagenes.tsv`: tema → archivo, pie y crédito.
- `patch.py [ruta]`: idempotente; quita las imágenes con crédito y las vuelve a poner. En la guía salen en «Imágenes de referencia», separadas de «Imágenes del apunte»; el visor muestra el crédito. Sirve igual para la copia del artefacto.

Después: `python3 tools-subrayar/firmar.py <clave.pem>`.
