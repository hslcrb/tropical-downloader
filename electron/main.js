/**
 * Tropical Downloader - Electron Main Process
 * - Spawns Python FastAPI backend on startup
 * - Manages BrowserWindow lifecycle
 * - Provides IPC handlers for file system operations
 */

const {
  app,
  BrowserWindow,
  ipcMain,
  dialog,
  shell,
  Notification,
} = require("electron");
const path = require("path");
const { spawn } = require("child_process");
const http = require("http");

const BACKEND_PORT = 8765;
const IS_DEV = process.argv.includes("--dev");

let mainWindow = null;
let backendProcess = null;
let backendReady = false;

// ─── Backend Process Management ───────────────────────────────────────────────
function startBackend() {
  const isDev = IS_DEV;

  // Determine python executable
  const pythonExe = process.platform === "win32" ? "python" : "python3";

  // Try to spawn backend
  const args = ["-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", String(BACKEND_PORT), "--log-level", "warning"];
  const cwd = path.join(__dirname, "..");

  console.log(`[Backend] Starting: ${pythonExe} ${args.join(" ")}`);
  console.log(`[Backend] CWD: ${cwd}`);

  backendProcess = spawn(pythonExe, args, {
    cwd,
    stdio: ["ignore", "pipe", "pipe"],
    detached: false,
  });

  backendProcess.stdout.on("data", (d) => {
    process.stdout.write(`[Backend] ${d}`);
  });

  backendProcess.stderr.on("data", (d) => {
    process.stderr.write(`[Backend] ${d}`);
  });

  backendProcess.on("exit", (code, signal) => {
    console.log(`[Backend] Process exited with code ${code}, signal ${signal}`);
    backendReady = false;
    backendProcess = null;
  });

  backendProcess.on("error", (err) => {
    console.error(`[Backend] Process error: ${err.message}`);
    backendReady = false;
  });
}

function stopBackend() {
  if (backendProcess) {
    console.log("[Backend] Stopping backend process...");
    if (process.platform === "win32") {
      spawn("taskkill", ["/pid", backendProcess.pid, "/f", "/t"]);
    } else {
      backendProcess.kill("SIGTERM");
    }
    backendProcess = null;
  }
}

function waitForBackend(timeout = 30000) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    function check() {
      const req = http.request(
        { hostname: "127.0.0.1", port: BACKEND_PORT, path: "/", method: "GET" },
        (res) => {
          if (res.statusCode === 200) {
            backendReady = true;
            console.log("[Backend] Ready!");
            resolve();
          } else {
            retry();
          }
        }
      );
      req.on("error", () => retry());
      req.end();
    }
    function retry() {
      if (Date.now() - start > timeout) {
        reject(new Error("Backend failed to start within timeout"));
        return;
      }
      setTimeout(check, 500);
    }
    check();
  });
}

// ─── Window Creation ──────────────────────────────────────────────────────────
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    show: true,
    backgroundColor: "#0a1a2e",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
      webSecurity: false, // Allow local ES module loading via file://
    },
    icon: path.join(__dirname, "..", "tropical-downloader.ico"),
  });

  const indexPath = path.join(__dirname, "..", "src", "index.html");
  console.log(`[Window] Loading file: ${indexPath}`);

  mainWindow.loadFile(indexPath).catch((err) => {
    console.error("[Window] Failed to load index.html:", err);
  });

  mainWindow.webContents.on("did-fail-load", (event, errorCode, errorDescription) => {
    console.error(`[Window] Load failed (${errorCode}): ${errorDescription}`);
  });

  mainWindow.webContents.on("console-message", (event, level, message, line, sourceId) => {
    console.log(`[Renderer Console] ${message} (${sourceId}:${line})`);
  });

  if (IS_DEV) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on("closed", () => {
    console.log("[Window] Main window closed");
    mainWindow = null;
  });
}

// ─── IPC Handlers ─────────────────────────────────────────────────────────────
ipcMain.handle("selectFolder", async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ["openDirectory"],
  });
  return result.canceled ? null : result.filePaths[0];
});

ipcMain.handle("openPath", async (event, folderPath) => {
  await shell.openPath(folderPath);
  return true;
});

ipcMain.handle("openFile", async (event, filePath) => {
  await shell.openPath(filePath);
  return true;
});

ipcMain.handle("showNotification", async (event, { title, body }) => {
  if (Notification.isSupported()) {
    new Notification({ title, body }).show();
  }
  return true;
});

ipcMain.handle("getBackendStatus", () => ({
  ready: backendReady,
  port: BACKEND_PORT,
}));

ipcMain.handle("getAppVersion", () => app.getVersion());

// ─── App Lifecycle ────────────────────────────────────────────────────────────
app.whenReady().then(async () => {
  console.log("[App] Starting Tropical Downloader v2...");

  // Start Python backend
  startBackend();

  // Create window (immediately, show loading state)
  createWindow();

  // Wait for backend to be ready
  try {
    await waitForBackend(30000);
    mainWindow?.webContents.send("backend-ready");
  } catch (err) {
    console.error("[App] Backend startup failed:", err.message);
    mainWindow?.webContents.send("backend-error", err.message);
  }
});

app.on("window-all-closed", () => {
  stopBackend();
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.on("will-quit", () => {
  stopBackend();
});
