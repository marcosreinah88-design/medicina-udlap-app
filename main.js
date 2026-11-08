// Medicina UDLAP (Marcos David Reinah Guzmán)
// Todo el contenido viene dentro de la app (carpeta site/) y funciona sin internet.
// Cuando hay internet, la app revisa UPDATE_URL y baja solo los archivos que cambiaron.
const { app, BrowserWindow, protocol, net, shell, Menu, Notification, ipcMain } = require("electron");
const path = require("path");
const fs = require("fs");
const crypto = require("crypto");
const { pathToFileURL } = require("url");

const UPDATE_URL = process.env.MED_UPDATE_URL || "https://raw.githubusercontent.com/marcosreinah88-design/medicina-udlap-app/main/site"; // sitio con la copia más reciente de la página
const CHECK_EVERY_MIN = 30;

protocol.registerSchemesAsPrivileged([
  { scheme: "app", privileges: { standard: true, secure: true, supportFetchAPI: true, stream: true } }
]);

const BUNDLED = path.join(__dirname, "site");
let CACHE; // userData/contenido: archivos más nuevos que los que vienen en la app
const readJSON = (p) => { try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch (e) { return null; } };
let bundledMan, activeMan;

const isInternal = (u) => u.startsWith("app://");
let SEED = "[]"; try { SEED = fs.readFileSync(path.join(__dirname, "seed-cto.json"), "utf8"); } catch (e) {}

/* ajustes solo para la app: doctype, CTO de Marcos y textos de guardado */
function adaptIndex(html) {
  const seed = `<script>try{if(!localStorage.getItem("carrera-material"))localStorage.setItem("carrera-material",${JSON.stringify(SEED)})}catch(e){}window.__MAC_APP=true</script>`;
  html = html
    .replace("(Sin cuenta: lo que agregues se guarda solo en este navegador.)", "(Lo que agregues se guarda en esta Mac.)")
    .replace(/Guardado solo en este navegador \(inicia sesión para sincronizar\)/g, "Guardado en esta Mac")
    .replace(/Guardado solo en este navegador/g, "Guardado en esta Mac");
  const head = /^\s*<!doctype/i.test(html) ? "" : '<!doctype html>\n<html lang="es">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n';
  return head + seed + "\n" + html;
}

function resolveFile(rel) {
  const inCache = path.join(CACHE, rel);
  if (activeMan && activeMan.files[rel] && fs.existsSync(inCache)) return inCache;
  return path.join(BUNDLED, rel);
}

function registerProtocol() {
  protocol.handle("app", async (req) => {
    const u = new URL(req.url);
    let rel = decodeURIComponent(u.pathname).replace(/^\/+/, "");
    if (!rel || rel.endsWith("/")) rel += "index.html";
    if (rel.split("/").includes("..")) return new Response("No encontrado", { status: 404 });
    const file = resolveFile(rel);
    if (rel === "index.html") {
      try {
        return new Response(adaptIndex(fs.readFileSync(file, "utf8")), { headers: { "content-type": "text/html; charset=utf-8" } });
      } catch (e) { return new Response("No encontrado", { status: 404 }); }
    }
    return net.fetch(pathToFileURL(file).toString());
  });
}

/* ===== actualización automática ===== */
const sha = (buf) => crypto.createHash("sha256").update(buf).digest("hex");
let updating = false;
async function checkForUpdate(win) {
  if (updating || !/^https?:\/\//.test(UPDATE_URL)) return;
  updating = true;
  try {
    const res = await net.fetch(UPDATE_URL + "/manifest.json?t=" + Date.now(), { cache: "no-store" });
    if (!res.ok) return;
    const remote = await res.json();
    if (!remote || !remote.files || (activeMan && remote.version <= activeMan.version)) return;
    let changed = 0;
    for (const [rel, h] of Object.entries(remote.files)) {
      if (rel.split("/").includes("..")) continue;
      const target = path.join(CACHE, rel);
      if (bundledMan.files[rel] === h) { if (fs.existsSync(target)) fs.unlinkSync(target); continue; }
      if (fs.existsSync(target) && sha(fs.readFileSync(target)) === h) continue;
      const r = await net.fetch(UPDATE_URL + "/" + rel.split("/").map(encodeURIComponent).join("/"), { cache: "no-store" });
      if (!r.ok) throw new Error("descarga " + rel);
      const buf = Buffer.from(await r.arrayBuffer());
      if (sha(buf) !== h) throw new Error("archivo incompleto " + rel);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target + ".tmp", buf);
      fs.renameSync(target + ".tmp", target);
      changed++;
    }
    fs.writeFileSync(path.join(CACHE, "manifest.json"), JSON.stringify(remote));
    activeMan = remote;
    if (changed) fire("Medicina UDLAP se actualizó", "Hay contenido nuevo en tu repositorio. Abre la app para verlo.", "");
    if (win && !win.isDestroyed()) {
      win.webContents.session.clearCache();
      win.webContents.executeJavaScript(`(()=>{if(document.getElementById("appUpd"))return;const d=document.createElement("div");d.id="appUpd";
        d.style.cssText="position:fixed;z-index:99999;left:50%;bottom:22px;transform:translateX(-50%);background:#00543c;color:#fff;font:600 14px system-ui;padding:10px 12px 10px 16px;border-radius:999px;box-shadow:0 10px 30px rgba(0,0,0,.35);display:flex;gap:12px;align-items:center";
        d.innerHTML='Hay una versión nueva del repositorio <button style="border:0;background:#f26b21;color:#fff;font:700 13px system-ui;padding:7px 14px;border-radius:999px;cursor:pointer">Actualizar</button>';
        d.querySelector("button").onclick=()=>location.reload();document.body.appendChild(d)})()`).catch(() => {});
    }
  } catch (e) { /* sin internet o falla: se queda con la versión que ya tiene */ }
  finally { updating = false; }
}

/* ===== notificaciones =====
   La página (calendario) manda la lista de avisos de las próximas semanas; aquí se guardan y se lanzan a su hora,
   aunque la ventana esté cerrada. Con "Abrir al iniciar sesión" la app queda trabajando en segundo plano. */
let NOTIF_FILE, notif = { items: [], fired: [], enabled: true };
const saveNotif = () => { try { fs.writeFileSync(NOTIF_FILE, JSON.stringify(notif)); } catch (e) {} };
function showWindow(route) {
  let w = BrowserWindow.getAllWindows()[0];
  if (!w) w = createWindow();
  if (route) w.webContents.executeJavaScript(`location.hash=${JSON.stringify(route)}`).catch(() => {});
  if (w.isMinimized()) w.restore();
  w.show(); w.focus();
}
function fire(title, body, route) {
  if (!Notification.isSupported()) return;
  const n = new Notification({ title, body, silent: false });
  n.on("click", () => showWindow(route));
  n.show();
}
function tickNotif() {
  if (!notif.enabled) return;
  const now = Date.now(), fired = new Set(notif.fired);
  let changed = false;
  for (const it of notif.items) {
    if (fired.has(it.id) || it.at > now || it.at < now - 3 * 3600e3) continue;
    fire(it.title, it.body, it.route); fired.add(it.id); changed = true;
  }
  if (changed) { notif.fired = [...fired].slice(-500); saveNotif(); }
}
ipcMain.on("med:schedule", (e, items) => {
  if (!Array.isArray(items)) return;
  notif.items = items.filter((x) => x && typeof x.id === "string" && typeof x.at === "number" && typeof x.title === "string")
    .slice(0, 400).map((x) => ({ id: x.id.slice(0, 120), at: x.at, title: x.title.slice(0, 120), body: String(x.body || "").slice(0, 400), route: String(x.route || "calendario").slice(0, 80) }));
  saveNotif(); tickNotif();
});

// la corona abre la app de Plan de Volumen si está instalada; si no, su página
const PLAN_APPS = ["/Applications/Plan de Volumen.app", path.join(require("os").homedir(), "Applications", "Plan de Volumen.app")];
function openOut(url) {
  if (!/^(https?:|mailto:)/i.test(url)) return;
  if (/marcosreinah88-design\.github\.io\/plan-volumen|claude\.ai\/artifact\/Rk2qXH6zwGc8jRwbc142mK/.test(url)) {
    const appPath = PLAN_APPS.find((p) => fs.existsSync(p));
    if (appPath) { shell.openPath(appPath).then((err) => { if (err) shell.openExternal(url); }); return; }
  }
  shell.openExternal(url);
}
// links externos (Drive, PubMed, etc.) se abren en el navegador
app.on("web-contents-created", (_e, wc) => {
  wc.setWindowOpenHandler(({ url }) => { if (isInternal(url)) return { action: "allow" }; openOut(url); return { action: "deny" }; });
  wc.on("will-frame-navigate", (e) => { if (!isInternal(e.url)) { e.preventDefault(); openOut(e.url); } });
});

function createWindow(hidden) {
  const win = new BrowserWindow({
    show: !hidden,
    width: 1320, height: 900, minWidth: 380, minHeight: 500,
    title: "Medicina UDLAP", backgroundColor: "#003b2a",
    webPreferences: { contextIsolation: true, sandbox: true, spellcheck: false, preload: path.join(__dirname, "preload.js") }
  });
  win.loadURL("app://medicina/index.html");
  win.webContents.once("did-finish-load", () => checkForUpdate(win));
  return win;
}

app.whenReady().then(() => {
  CACHE = path.join(app.getPath("userData"), "contenido");
  fs.mkdirSync(CACHE, { recursive: true });
  bundledMan = readJSON(path.join(BUNDLED, "manifest.json")) || { version: 0, files: {} };
  const cached = readJSON(path.join(CACHE, "manifest.json"));
  activeMan = cached && cached.version > bundledMan.version ? cached : bundledMan;
  registerProtocol();
  NOTIF_FILE = path.join(app.getPath("userData"), "avisos.json");
  notif = Object.assign(notif, readJSON(NOTIF_FILE) || {});
  if (!notif.loginSet) { app.setLoginItemSettings({ openAtLogin: true, openAsHidden: true }); notif.loginSet = true; saveNotif(); }
  setInterval(tickNotif, 30 * 1000);
  Menu.setApplicationMenu(Menu.buildFromTemplate([
    { role: "appMenu" }, { role: "editMenu" },
    { label: "Ver", submenu: [
      { label: "Buscar actualizaciones", click: () => { const w = BrowserWindow.getAllWindows()[0]; checkForUpdate(w); } },
      { role: "reload", label: "Recargar" }, { role: "togglefullscreen", label: "Pantalla completa" }, { type: "separator" },
      { role: "resetZoom", label: "Tamaño real" }, { role: "zoomIn", label: "Acercar" }, { role: "zoomOut", label: "Alejar" }] },
    { label: "Avisos", submenu: [
      { label: "Recibir notificaciones", type: "checkbox", checked: notif.enabled !== false, click: (mi) => { notif.enabled = mi.checked; saveNotif(); } },
      { label: "Abrir al iniciar sesión (para avisar aunque no la abras)", type: "checkbox", checked: app.getLoginItemSettings().openAtLogin, click: (mi) => app.setLoginItemSettings({ openAtLogin: mi.checked, openAsHidden: true }) },
      { type: "separator" },
      { label: "Probar una notificación", click: () => fire("Medicina UDLAP", "Así te van a llegar los avisos de exámenes, plan de estudio, fechas UDLAP y partidos.", "calendario") }
    ] },
    { role: "windowMenu" }
  ]));
  const atLogin = app.getLoginItemSettings().wasOpenedAtLogin || process.argv.includes("--hidden");
  const win = createWindow(atLogin);
  setInterval(() => checkForUpdate(BrowserWindow.getAllWindows()[0] || win), CHECK_EVERY_MIN * 60 * 1000);
  app.on("activate", () => { const w = BrowserWindow.getAllWindows()[0]; if (!w) createWindow(); else { w.show(); w.focus(); } });
});
app.on("window-all-closed", () => { if (process.platform !== "darwin") app.quit(); });
