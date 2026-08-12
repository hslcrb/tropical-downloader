/**
 * Tropical Downloader - Main App Shell
 * Tab routing, WebSocket client, API client, Toast system.
 */

const API_BASE = "http://127.0.0.1:8765";
const WS_URL   = "ws://127.0.0.1:8765/ws";

// ── API Client ────────────────────────────────────────────────────────────────
const api = {
  async call(method, path, body) {
    const opts = { method, headers: { "Content-Type": "application/json" } };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(`${API_BASE}${path}`, opts);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || data.error || "Request failed");
    return data;
  },
  get:    (path) => api.call("GET", path),
  post:   (path, body) => api.call("POST", path, body),
  put:    (path, body) => api.call("PUT", path, body),
  delete: (path) => api.call("DELETE", path),
};

window.$api = api;

// ── WebSocket Client ──────────────────────────────────────────────────────────
class WSClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.listeners = {};
    this._reconnectDelay = 1000;
    this.connect();
  }

  connect() {
    try {
      this.ws = new WebSocket(this.url);
      this.ws.onopen = () => {
        console.log("[WS] Connected");
        this._reconnectDelay = 1000;
      };
      this.ws.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data);
          this._dispatch(msg.type, msg);
        } catch {}
      };
      this.ws.onclose = () => {
        console.log("[WS] Disconnected, reconnecting...");
        setTimeout(() => this.connect(), this._reconnectDelay);
        this._reconnectDelay = Math.min(this._reconnectDelay * 1.5, 10000);
      };
    } catch (e) {
      console.warn("[WS] Connect failed:", e);
      setTimeout(() => this.connect(), this._reconnectDelay);
    }
  }

  on(type, fn) {
    if (!this.listeners[type]) this.listeners[type] = [];
    this.listeners[type].push(fn);
  }

  _dispatch(type, msg) {
    (this.listeners[type] || []).forEach(fn => fn(msg));
    (this.listeners["*"] || []).forEach(fn => fn(msg));
  }
}

window.$ws = new WSClient(WS_URL);

// ── Toast System ──────────────────────────────────────────────────────────────
function showToast(msg, type = "info") {
  const container = document.getElementById("toast-container");
  const el = document.createElement("div");
  el.className = `toast toast-${type}`;
  el.textContent = msg;
  container.appendChild(el);
  setTimeout(() => el.remove(), 3100);
}
window.$toast = showToast;

// ── Tab Router ────────────────────────────────────────────────────────────────
const tabBtns = document.querySelectorAll(".tab-btn");
const tabPanes = document.querySelectorAll(".tab-pane");

tabBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    const target = btn.dataset.tab;
    tabBtns.forEach(b => b.classList.toggle("active", b === btn));
    tabPanes.forEach(p => p.classList.toggle("active", p.id === `tab-${target}`));
  });
});

// ── Backend Status ────────────────────────────────────────────────────────────
const statusDot  = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");

async function checkBackend() {
  try {
    const data = await api.get("/");
    statusDot.classList.add("ready");
    statusText.textContent = "백엔드 준비";
  } catch {
    statusDot.classList.remove("ready");
    statusText.textContent = "백엔드 연결 중...";
    setTimeout(checkBackend, 2000);
  }
}
checkBackend();

// Electron IPC backend-ready event
if (window.api) {
  // Called by main.js via webContents.send
  window.addEventListener("message", (e) => {
    if (e.data === "backend-ready") {
      checkBackend();
    }
  });
}

// ── Dynamic Component Loader ──────────────────────────────────────────────────
import("./components/QuickDownloadTab.js").then(m => m.mount(document.getElementById("tab-quick")));
import("./components/FormatInspectorTab.js").then(m => m.mount(document.getElementById("tab-inspector")));
import("./components/PlaylistChannelTab.js").then(m => m.mount(document.getElementById("tab-playlist")));
import("./components/ChannelBackupTab.js").then(m => m.mount(document.getElementById("tab-channel")));
import("./components/QueueTab.js").then(m => m.mount(document.getElementById("tab-queue")));
import("./components/HistoryLogsTab.js").then(m => m.mount(document.getElementById("tab-history")));
import("./components/MediaPlayerTab.js").then(m => m.mount(document.getElementById("tab-player")));
import("./components/AdvancedTab.js").then(m => m.mount(document.getElementById("tab-advanced")));
import("./components/SettingsTab.js").then(m => m.mount(document.getElementById("tab-settings")));
