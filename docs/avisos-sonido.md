# Sonido propio para los avisos del cel

El sonido de los avisos es una campanita de tres notas (Mi–Sol#–Si). Los archivos están en `docs/sonido/`:
`aviso-medicina.caf` (iPhone/Bark) y `aviso-medicina.mp3` (Android).

## Qué hace la app sola (ya incluido)
- **App abierta:** cuando llega un aviso, suena la campanita dentro de la app (después de haber tocado la pantalla una vez).
- **Android:** el aviso siempre vibra con el patrón propio "ta-ta-taaa" y vuelve a sonar aunque sea un aviso repetido.
- **iPhone (app web en la pantalla de inicio):** Apple no deja que una app web elija su sonido; usa el sonido normal de iOS.
  Para un sonido propio en iPhone, usar Bark (abajo).

## iPhone: sonido propio con Bark (gratis)
[Bark](https://apps.apple.com/app/id1403753865) es una app gratis y de código abierto que recibe avisos y sí deja poner sonido propio.
1. Instala Bark en el iPhone y ábrela; acepta las notificaciones.
2. Pasa `aviso-medicina.caf` al iPhone (AirDrop o Archivos). En Bark ve a **Sonidos** → **Subir sonido** y elígelo.
   El sonido debe quedar con el nombre `aviso-medicina` (así lo pide el aviso).
3. En Bark copia la clave del cel: es la parte entre `https://api.day.app/` y la siguiente `/` del ejemplo que muestra la app.
4. En GitHub: repositorio → Settings → Secrets and variables → Actions → **New repository secret**, nombre `MED_BARK`, valor = esa clave.
5. Listo: el siguiente aviso llega por Bark con la campanita, el ícono de Medicina UDLAP y en el grupo "Medicina UDLAP".
   Al tocarlo abre la app en la sección del aviso. Para no recibir doble, si Bark lo entregó ya no se manda el aviso web al iPhone.
   (Puedes apagar los avisos web en Ajustes → Notificaciones → Medicina si aun así ves dobles.)

Para quitar Bark: borra el secreto `MED_BARK` y los avisos vuelven a llegar solo por la app web.

## Android: elegir la campanita como sonido
Ajustes → Apps → Medicina UDLAP (o Chrome → Notificaciones → el sitio) → Notificaciones → **Sonido** → elegir `aviso-medicina.mp3`
(primero cópialo a la carpeta *Notifications* o *Ringtones* del cel).
