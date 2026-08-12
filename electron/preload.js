/**
 * Tropical Downloader - Electron Preload Script
 * Exposes safe IPC API to renderer process via contextBridge.
 */
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("api", {
  // Backend info
  getBackendPort: () => 8765,

  // Folder / file system
  selectFolder: () => ipcRenderer.invoke("selectFolder"),
  openPath: (path) => ipcRenderer.invoke("openPath", path),
  openFile: (path) => ipcRenderer.invoke("openFile", path),

  // System notifications
  showNotification: (title, body) =>
    ipcRenderer.invoke("showNotification", { title, body }),

  // Backend status
  getBackendStatus: () => ipcRenderer.invoke("getBackendStatus"),

  // App info
  getAppVersion: () => ipcRenderer.invoke("getAppVersion"),
});
