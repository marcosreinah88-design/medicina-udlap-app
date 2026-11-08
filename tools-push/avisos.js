// Lee del gist de sincronización los avisos programados y las suscripciones del cel, y manda los que ya tocan.
const webpush = require("web-push");
const T = process.env.MED_SYNC;
if (!T) { console.log("Falta el secreto MED_SYNC: no hay a quién avisar."); process.exit(0); }
const DESC = "Medicina UDLAP · sincronización (no borrar)", FILE = "medicina-udlap.json", SENT = "avisos-enviados.json";
const H = { Authorization: "Bearer " + T, Accept: "application/vnd.github+json", "User-Agent": "medicina-udlap-avisos" };
async function gh(p, o = {}) {
  const r = await fetch((process.env.MED_API || "https://api.github.com") + p, { ...o, headers: { ...H, ...(o.body ? { "Content-Type": "application/json" } : {}) } });
  if (!r.ok) throw new Error(p + " → " + r.status);
  return r.json();
}
const txt = async (f) => (f.truncated ? await (await fetch(f.raw_url, { headers: H })).text() : f.content);
const J = (s, d) => { try { return JSON.parse(s); } catch (e) { return d; } };
(async () => {
  let id = null;
  for (let page = 1; page <= 5 && !id; page++) {
    const l = await gh("/gists?per_page=100&page=" + page);
    const g = l.find((x) => x.description === DESC && x.files && x.files[FILE]);
    if (g) id = g.id;
    if (l.length < 100) break;
  }
  if (!id) { console.log("Todavía no hay gist de sincronización."); return; }
  const g = await gh("/gists/" + id);
  const data = (J(await txt(g.files[FILE]), {}) || {}).data || {};
  const vapid = J(data["medicina-push-vapid"], null), subs = J(data["medicina-push-subs"], []), avisos = J(data["medicina-avisos"], []);
  if (!vapid || !subs.length) { console.log("No hay cel con avisos activados."); return; }
  const sent = g.files[SENT] ? J(await txt(g.files[SENT]), {}) : {};
  const now = Date.now();
  const due = avisos.filter((a) => a && a.id && a.at <= now + 2 * 60e3 && a.at > now - 3 * 3600e3 && !sent[a.id]).sort((a, b) => a.at - b.at);
  console.log(`${avisos.length} avisos programados, ${due.length} por mandar, ${subs.length} cel(es).`);
  if (!due.length) return;
  webpush.setVapidDetails("https://marcosreinah88-design.github.io/medicina-udlap-app/", vapid.publicKey, vapid.privateKey);
  for (const a of due) {
    for (const s of subs) {
      try { await webpush.sendNotification(s.sub, JSON.stringify({ id: a.id, title: a.title, body: a.body, route: a.route }), { TTL: 3 * 3600, urgency: "high" }); }
      catch (e) { console.log("No se pudo mandar a", s.id, e.statusCode || e.message); }
    }
    sent[a.id] = now;
  }
  for (const k of Object.keys(sent)) if (now - sent[k] > 60 * 864e5) delete sent[k];
  await gh("/gists/" + id, { method: "PATCH", body: JSON.stringify({ files: { [SENT]: { content: JSON.stringify(sent) } } }) });
  console.log("Listo.");
})().catch((e) => { console.error(e.message); process.exit(1); });
