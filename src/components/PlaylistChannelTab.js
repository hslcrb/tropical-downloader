/**
 * Playlist Tab - Batch playlist download with range selection.
 */

export function mount(root) {
  root.innerHTML = `
    <div style="max-width:780px;margin:0 auto;">
      <div class="glass-card mb-4">
        <div class="section-title">플레이리스트 URL</div>
        <div class="flex gap-2 mb-2">
          <input id="pl-url" class="input" placeholder="YouTube 플레이리스트 URL..." />
          <button id="pl-analyze" class="btn btn-primary">🔍 분석</button>
        </div>
      </div>

      <div id="pl-loading" style="display:none;text-align:center;padding:40px;">
        <div class="spinner" style="margin:0 auto 12px;width:32px;height:32px;"></div>
        <div style="color:var(--text-muted);">플레이리스트 분석 중...</div>
      </div>

      <div id="pl-result" style="display:none;">
        <div id="pl-info" class="glass-card mb-4"></div>

        <div class="glass-card mb-4">
          <div class="section-title">다운로드 범위</div>
          <div class="flex gap-3 items-center mb-3">
            <input id="pl-range" class="input" style="width:200px;" placeholder="예: 1-20, 1,3,5, all" value="all" />
            <span style="font-size:12px;color:var(--text-muted);">"all"은 전체, "1-20"은 1번~20번 항목</span>
          </div>

          <div class="section-title">파일명 템플릿</div>
          <input id="pl-template" class="input mb-3" value="%(playlist_index)s - %(title)s.%(ext)s" />

          <div class="section-title">포맷</div>
          <div class="flex gap-2 mb-3 flex-wrap">
            <button class="btn btn-primary btn-sm preset-dl" data-fmt="bestvideo+bestaudio/best" data-audio="false">🎬 최고 화질</button>
            <button class="btn btn-primary btn-sm preset-dl" data-fmt="bestvideo[height<=1080]+bestaudio/best" data-audio="false">🖥 1080p</button>
            <button class="btn btn-success btn-sm preset-dl" data-fmt="bestaudio/best" data-audio="true" data-afmt="mp3">🎵 MP3</button>
            <button class="btn btn-success btn-sm preset-dl" data-fmt="bestaudio/best" data-audio="true" data-afmt="flac">🎶 FLAC</button>
          </div>
        </div>

        <div class="glass-card mb-4" style="max-height:400px;overflow-y:auto;">
          <div class="flex items-center justify-between mb-3">
            <div class="section-title" style="margin-bottom:0;">항목 목록</div>
            <span id="pl-count" style="font-size:12px;color:var(--text-muted);"></span>
          </div>
          <div id="pl-items"></div>
        </div>
      </div>
    </div>
  `;

  const urlInput  = root.querySelector("#pl-url");
  const analyzeBtn = root.querySelector("#pl-analyze");
  const loadingEl = root.querySelector("#pl-loading");
  const resultEl  = root.querySelector("#pl-result");
  const infoEl    = root.querySelector("#pl-info");
  const itemsEl   = root.querySelector("#pl-items");
  const countEl   = root.querySelector("#pl-count");

  let currentInfo = null;

  analyzeBtn.onclick = doAnalyze;
  urlInput.addEventListener("keydown", (e) => { if (e.key === "Enter") doAnalyze(); });

  async function doAnalyze() {
    const url = urlInput.value.trim();
    if (!url) return;
    resultEl.style.display = "none";
    loadingEl.style.display = "block";
    try {
      const resp = await window.$api.post("/api/analyze", { url });
      currentInfo = resp.data;
      renderInfo(currentInfo);
      renderItems(currentInfo.playlist_items || []);
      loadingEl.style.display = "none";
      resultEl.style.display = "block";
    } catch (e) {
      loadingEl.style.display = "none";
      window.$toast(`분석 실패: ${e.message}`, "error");
    }
  }

  function renderInfo(info) {
    infoEl.innerHTML = `
      <div style="display:flex;gap:12px;align-items:center;">
        <img src="${info.thumbnail || ''}" style="width:100px;height:56px;object-fit:cover;border-radius:6px;border:1px solid var(--glass-border);" onerror="this.style.display='none'"/>
        <div>
          <div style="font-size:15px;font-weight:700;margin-bottom:4px;">${escHtml(info.title)}</div>
          <div style="font-size:12px;color:var(--text-muted);">👤 ${escHtml(info.uploader || "")} &nbsp;·&nbsp; 📋 ${info.playlist_count || (info.playlist_items||[]).length}개 항목</div>
        </div>
      </div>`;
  }

  function renderItems(items) {
    countEl.textContent = `총 ${items.length}개`;
    itemsEl.innerHTML = items.map((item, i) => `
      <div class="flex items-center gap-2" style="padding:7px 0;border-bottom:1px solid rgba(0,180,255,0.06);">
        <span style="color:var(--text-muted);font-size:12px;min-width:28px;">${item.index || i+1}</span>
        <span style="flex:1;font-size:13px;color:var(--text-secondary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
          ${escHtml(item.title)}
        </span>
        <span style="font-size:11px;color:var(--text-muted);">${fmtDur(item.duration)}</span>
      </div>`).join("");
  }

  root.querySelectorAll(".preset-dl").forEach(btn => {
    btn.onclick = async () => {
      if (!currentInfo) return;
      const url = urlInput.value.trim();
      const range = root.querySelector("#pl-range").value.trim();
      const template = root.querySelector("#pl-template").value.trim();
      const isAudio = btn.dataset.audio === "true";
      const afmt = btn.dataset.afmt;
      try {
        const resp = await window.$api.post("/api/playlist/download", {
          url,
          range_str: range || "all",
          format_id: btn.dataset.fmt,
          audio_only: isAudio,
          audio_format: afmt,
          filename_template: template
        });
        window.$toast(`✅ 플레이리스트 다운로드 시작! (${resp.task_id})`, "success");
        document.querySelector('[data-tab="queue"]')?.click();
      } catch (e) {
        window.$toast(`다운로드 실패: ${e.message}`, "error");
      }
    };
  });

  function fmtDur(secs) {
    if (!secs) return "";
    const m = Math.floor(secs / 60), s = secs % 60;
    return `${m}:${String(s).padStart(2, "0")}`;
  }

  function escHtml(str) {
    return String(str || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }
}
