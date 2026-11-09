# Avisos al cel con cron-job.org

El cron de GitHub Actions es poco confiable (se retrasa 10 a 30 min o se salta corridas). Por eso los avisos
los dispara **cron-job.org** (gratis): cada 5 minutos llama a la API de GitHub para correr el workflow
`Avisos al cel` (`.github/workflows/avisos.yml`). El cron de GitHub se queda como respaldo, dos veces por hora.
Nunca llegan avisos repetidos: `tools-push/avisos.js` anota en el gist cada aviso ya enviado.

## 1. Crear la clave (token) de GitHub

1. Entra a https://github.com/settings/personal-access-tokens/new (Settings → Developer settings →
   Personal access tokens → **Fine-grained tokens** → Generate new token).
2. **Token name:** `cron-job avisos`.
3. **Expiration:** la más larga que deje (anota la fecha para renovarla).
4. **Repository access:** *Only select repositories* → `medicina-udlap-app`.
5. **Permissions → Repository permissions → Actions:** *Read and write*. Nada más.
6. **Generate token** y copia la clave (empieza con `github_pat_`). Solo se muestra una vez.

Esta clave solo puede correr workflows de este repo; no puede leer tu gist ni tus datos.

## 2. Crear el cronjob

1. Crea cuenta gratis en https://cron-job.org y entra a **Dashboard → Cronjobs → Create cronjob**.
2. **Title:** `Avisos medicina`.
3. **URL:** `https://api.github.com/repos/marcosreinah88-design/medicina-udlap-app/actions/workflows/avisos.yml/dispatches`
4. **Execution schedule:** *Every 5 minutes* (o *Custom* → `*/5 * * * *`).
5. Pestaña **Advanced**:
   - **Request method:** `POST`
   - **Headers** (agrega uno por uno):
     - `Accept` = `application/vnd.github+json`
     - `Authorization` = `Bearer github_pat_TU_CLAVE`
     - `X-GitHub-Api-Version` = `2022-11-28`
     - `Content-Type` = `application/json`
   - **Request body:** `{"ref":"main"}`
6. Guarda y usa **Test run**. Debe responder **204 No Content**.
7. En GitHub → pestaña **Actions** → *Avisos al cel* debe aparecer una corrida nueva con la etiqueta
   `workflow_dispatch`.

## Si algo falla

| Respuesta | Qué significa |
|---|---|
| 204 | Todo bien. |
| 401 | La clave está mal copiada o caducó. Crea otra y cámbiala en el header `Authorization`. |
| 403 | A la clave le falta el permiso *Actions: Read and write* o no incluye este repo. |
| 404 | La URL está mal escrita, o la clave no tiene acceso al repo. |
| 422 | El body no es `{"ref":"main"}`. |

En cron-job.org activa **Notify me when the cronjob fails** para que te avise por correo si la clave caduca.
