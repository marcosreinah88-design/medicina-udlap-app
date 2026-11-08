// Puente mínimo entre la página y la app: la página manda la lista de avisos.
const { contextBridge, ipcRenderer } = require("electron");
contextBridge.exposeInMainWorld("medApp", {
  schedule: (items) => ipcRenderer.send("med:schedule", JSON.parse(JSON.stringify(items || [])))
});
