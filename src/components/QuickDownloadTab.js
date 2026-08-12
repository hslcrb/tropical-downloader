/**
 * Quick Download Tab
 * Auto clipboard paste, media preview card, one-click presets (4K, 1080p, 720p, MP3, FLAC).
 */

const PRESETS = [
  { label: "🎬 4K",    format: "bestvideo[height<=2160]+bestaudio/best", container: "mp4", audio_only: false },
  { label: "🖥 1080p", format: "bestvideo[height<=1080]+bestaudio/best", container: "mp4", audio_only: false },
  { label: "📺 720p",  format: "bestvideo[height<=720]+bestaudio/best",  container: "mp4", audio_only: false },
  { label: "🎵 MP3",   format: "bestaudio/best", container: "mp3", audio_only: true,  audio_format: "mp3"  },
  { label: "🎶 FLAC",  format: "bestaudio/best", container: "flac", audio_only: true, audio_format: "flac" },
];

export function mount(root) {
  root.innerHTML = `
    <div style="max-width:780px;margin:0 auto;">
      <div class="glass-card mb-4">
        <div class="section-title">URL 입력</div>
        <div class="flex gap-2 mb-2">
          <input id="qd-url" class="input" placeholder="YouTube URL을 입력하거나 붙여넣기..." />
          <button id="qd-paste" class="btn btn-ghost btn-sm" title="클립보드에서 붙여넣기">📋 붙여넣기</button>
          <button id="qd-analyze" class="btn btn-primary">🔍 분석</button>
        </div>
        <div class="log-output" id="qd-log" style="height:60px;display:none;"></div>
      </div>

      <div id="qd-result" style="display:none;">
        <div id="qd-media-card" class="media-card mb-4"></div>

        <div class="glass-card">
          <div class="section-title">원클릭 다운로드</div>
          <div class="preset-row" id="qd-presets"></div>
        </div>
      </div>

      <div id="qd-loading" style="display:none;text-align:center;padding:40px;">
        <div class="spinner" style="margin:0 auto 12px;width:32px;height:32px;"></div>
        <div style="color:var(--text-muted);font-size:13px;">미디어 정보 분석 중...</div>
      </div>
    </div>
  `;

  const urlInput   = root.querySelector("#qd-url");
  const pasteBtn   = root.querySelector("#qd-paste");
  const analyzeBtn = root.querySelector("#qd-analyze");
  const logEl      = root.querySelector("#qd-log");
  const resultEl   = root.querySelector("#qd-result");
  const loadingEl  = root.querySelector("#qd-loading");
  const presetsEl  = root.querySelector("#qd-presets");
  const cardEl     = root.querySelector("#qd-media-card");

  let currentInfo = null;

  // Paste from clipboard
  pasteBtn.onclick = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text.startsWith("http")) {
        urlInput.value = text.trim();
        doAnalyze();
      }
    } catch {}
  };

  // Auto-paste on focus if clipboard has a URL
  urlInput.addEventListener("focus", async () => {
    if (urlInput.value) return;
    try {
      const text = await navigator.clipboard.readText();
      if (text && text.startsWith("http")) {
        urlInput.value = text.trim();
      }
    } catch {}
  });

  analyzeBtn.onclick = doAnalyze;
  urlInput.addEventListener("keydown", (e) => { if (e.key === "Enter") doAnalyze(); });

  async function doAnalyze() {
    const url = urlInput.value.trim();
    if (!url) return;

    resultEl.style.display = "none";
    loadingEl.style.display = "block";
    logEl.style.display = "block";
    logEl.textContent = "";

    try {
      const resp = await window.$api.post("/api/analyze", { url });
      const info = resp.data;
      currentInfo = info;
      renderMediaCard(info);
      renderPresets(info, url);
      loadingEl.style.display = "none";
      resultEl.style.display = "block";
    } catch (e) {
      loadingEl.style.display = "none";
      logEl.textContent = `[오류] ${e.message}`;
      window.$toast(`분석 실패: ${e.message}`, "error");
    }
  }

  function renderMediaCard(info) {
    const dur = info.duration_string || "00:00";
    const views = info.view_count ? `👁 ${Number(info.view_count).toLocaleString()}` : "";
    cardEl.innerHTML = `
      <img class="media-thumb" src="${info.thumbnail || ''}" onerror="this.style.display='none'" />
      <div class="media-info">
        <div class="media-title">${escHtml(info.title)}</div>
        <div class="media-meta">
          <span class="meta-item">👤 ${escHtml(info.uploader || "")}</span>
          <span class="meta-item">⏱ ${dur}</span>
          ${views ? `<span class="meta-item">${views}</span>` : ""}
          ${info.is_playlist ? `<span class="meta-item">📋 플레이리스트 ${info.playlist_count || ""}개 항목</span>` : ""}
        </div>
        <div class="flex gap-2 flex-wrap">
          <span style="font-size:11px;color:var(--text-muted);">${escHtml(info.url)}</span>
        </div>
      </div>
    `;
  }

  function renderPresets(info, url) {
    presetsEl.innerHTML = "";
    PRESETS.forEach(preset => {
      const btn = document.createElement("button");
      btn.className = preset.audio_only ? "btn btn-success" : "btn btn-primary";
      btn.textContent = preset.label;
      btn.onclick = () => startDownload(url, preset);
      presetsEl.appendChild(btn);
    });
  }

  async function startDownload(url, preset) {
    try {
      const resp = await window.$api.post("/api/download", {
        url,
        format_id: preset.format,
        container: preset.container,
        audio_only: preset.audio_only || false,
        audio_format: preset.audio_format || "mp3"
      });
      window.$toast(`✅ 다운로드 시작! (${resp.task_id})`, "success");

      // Switch to queue tab
      document.querySelector('[data-tab="queue"]')?.click();
    } catch (e) {
      window.$toast(`다운로드 실패: ${e.message}`, "error");
    }
  }

  function escHtml(str) {
    return String(str || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }

  // WebSocket log updates
  window.$ws.on("log", (msg) => {
    logEl.textContent += msg.message + "\n";
    logEl.scrollTop = logEl.scrollHeight;
  });
}
