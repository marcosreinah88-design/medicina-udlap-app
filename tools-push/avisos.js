// Lee del gist de sincronización los avisos programados y las suscripciones del cel, y manda los que ya tocan.
// El gist va cifrado (AES-256-GCM, llave derivada de la misma clave MED_SYNC); también entiende la copia vieja sin cifrar.
const webpush = require("web-push");
const { webcrypto } = require("crypto");
const subtle = webcrypto.subtle;
const T = process.env.MED_SYNC;
if (!T) { console.log("Falta el secreto MED_SYNC: no hay a quién avisar."); process.exit(0); }
const DESC = "Medicina UDLAP · sincronización cifrada (no borrar)", DESC_OLD = "Medicina UDLAP · sincronización (no borrar)";
const FILE = "medicina-udlap.json", SENT = "avisos-enviados.json";
const API = process.env.MED_API || "https://api.github.com";
const H = { Authorization: "Bearer " + T, Accept: "application/vnd.github+json", "User-Agent": "medicina-udlap-avisos" };
async function gh(p, o = {}) {
  const r = await fetch(API + p, { ...o, headers: { ...H, ...(o.body ? { "Content-Type": "application/json" } : {}) } });
  if (!r.ok) throw new Error(p + " → " + r.status);
  return r.json();
}
const txt = async (f) => (f.truncated ? await (await fetch(f.raw_url, { headers: H })).text() : f.content);
const J = (s, d) => { try { return JSON.parse(s); } catch (e) { return d; } };
const te = new TextEncoder(), td = new TextDecoder();
async function unseal(s) {
  const j = J(s, null);
  if (!j) return {};
  if (j.v !== 2) return (j.data && typeof j.data === "object") ? j.data : {};
  const ikm = await subtle.importKey("raw", te.encode(T), "HKDF", false, ["deriveKey"]);
  const key = await subtle.deriveKey({ name: "HKDF", hash: "SHA-256", salt: te.encode("medicina-udlap/sync/v2"), info: te.encode("datos") },
    ikm, { name: "AES-GCM", length: 256 }, false, ["decrypt"]);
  const pt = await subtle.decrypt({ name: "AES-GCM", iv: Buffer.from(j.iv, "base64"), additionalData: te.encode(FILE) }, key, Buffer.from(j.ct, "base64"));
  return (J(td.decode(pt), {}) || {}).data || {};
}
(async () => {
  let id = null, old = null;
  for (let page = 1; page <= 5 && !id; page++) {
    const l = await gh("/gists?per_page=100&page=" + page);
    for (const x of l) {
      if (!x || !x.files || !x.files[FILE]) continue;
      if (x.description === DESC && !id) id = x.id;
      else if (x.description === DESC_OLD && !old) old = x.id;
    }
    if (l.length < 100) break;
  }
  id = id || old;
  if (!id) { console.log("Todavía no hay gist de sincronización."); return; }
  const g = await gh("/gists/" + id);
  let data;
  try { data = await unseal(await txt(g.files[FILE])); }
  catch (e) { console.log("No pude abrir el gist cifrado: MED_SYNC debe ser la misma clave que usan la Mac y el cel."); process.exit(1); }
  const vapid = J(data["medicina-push-vapid"], null), subs = J(data["medicina-push-subs"], []), avisos = J(data["medicina-avisos"], []);
  if (!vapid || !Array.isArray(subs) || !subs.length || !Array.isArray(avisos)) { console.log("No hay cel con avisos activados."); return; }
  const sent = g.files[SENT] ? J(await txt(g.files[SENT]), {}) : {};
  const now = Date.now();
  const due = avisos.filter((a) => a && a.id && a.at <= now + 2 * 60e3 && a.at > now - 3 * 3600e3 && !sent[a.id]).sort((a, b) => a.at - b.at);
  console.log(`${avisos.length} avisos programados, ${due.length} por mandar, ${subs.length} cel(es).`);
  if (!due.length) return;
  webpush.setVapidDetails("https://marcosreinah88-design.github.io/medicina-udlap-app/", vapid.publicKey, vapid.privateKey);
  for (const a of due) {
    for (const s of subs) {
      // solo servicios de avisos conocidos (Apple, Google, Mozilla, Microsoft)
      const ep = s && s.sub && String(s.sub.endpoint || "");
      if (!/^https:\/\/([a-z0-9.-]+\.)?(push\.apple\.com|fcm\.googleapis\.com|push\.services\.mozilla\.com|notify\.windows\.com)\//.test(ep)) continue;
      try { await webpush.sendNotification(s.sub, JSON.stringify({ id: String(a.id).slice(0, 120), title: String(a.title || "").slice(0, 120), body: String(a.body || "").slice(0, 400), route: String(a.route || "calendario").slice(0, 80) }), { TTL: 3 * 3600, urgency: "high" }); }
      catch (e) { console.log("No se pudo mandar a un cel:", e.statusCode || "error"); }
    }
    sent[a.id] = now;
  }
  for (const k of Object.keys(sent)) if (now - sent[k] > 60 * 864e5) delete sent[k];
  await gh("/gists/" + id, { method: "PATCH", body: JSON.stringify({ files: { [SENT]: { content: JSON.stringify(sent) } } }) });
  console.log("Listo.");
})().catch((e) => { console.error("Error:", e.message); process.exit(1); });
