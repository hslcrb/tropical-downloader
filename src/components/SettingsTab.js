/**
 * Settings Tab
 */

export function mount(root) {
  root.innerHTML = `
    <div style="max-width:680px;margin:0 auto;">
      <h2 style="font-size:16px;font-weight:700;color:var(--col-ocean);margin-bottom:16px;">🔧 설정</h2>

      <div class="glass-card mb-4">
        <div class="section-title">📁 다운로드 폴더</div>
        <div class="flex gap-2">
          <input id="s-dlpath" class="input" placeholder="~/Downloads/Tropical" />
          <button id="s-dlpath-browse" class="btn btn-ghost btn-sm">📂 선택</button>
        </div>
      </div>

      <div class="glass-card mb-4">
        <div class="section-title">🎬 FFmpeg 경로 (선택)</div>
        <input id="s-ffmpeg" class="input" placeholder="ffmpeg 실행 파일 경로 (비어 있으면 시스템 PATH 사용)" />
      </div>

      <div class="glass-card mb-4">
        <div class="section-title">📝 파일명 템플릿</div>
        <input id="s-template" class="input" value="%(title)s [%(id)s].%(ext)s" />
        <div style="font-size:11px;color:var(--text-muted);margin-top:6px;">yt-dlp 템플릿 변수: %(title)s, %(id)s, %(uploader)s, %(upload_date)s, %(ext)s</div>
      </div>

      <div class="glass-card mb-4">
        <div class="section-title">💾 저장공간 관리</div>
        <label class="checkbox-label mb-2">
          <input type="checkbox" id="s-purge" checked /> 저장공간 부족 시 node_modules 자동 삭제
        </label>
      </div>

      <div class="glass-card mb-4">
        <div class="section-title">💽 현재 디스크 공간</div>
        <div id="s-diskspace" style="color:var(--text-muted);font-size:13px;">로드 중...</div>
      </div>

      <button id="s-save" class="btn btn-success btn-lg w-full">💾 설정 저장</button>
    </div>
  `;

  const dlPathInput = root.querySelector("#s-dlpath");
  const dlPathBtn   = root.querySelector("#s-dlpath-browse");
  const ffmpegInput = root.querySelector("#s-ffmpeg");
  const templateInput = root.querySelector("#s-template");
  const purgeCheck  = root.querySelector("#s-purge");
  const diskEl      = root.querySelector("#s-diskspace");
  const saveBtn     = root.querySelector("#s-save");

  // Load current config
  window.$api.get("/api/config").then(resp => {
    const cfg = resp.data || {};
    if (cfg.download_path) dlPathInput.value = cfg.download_path;
    if (cfg.ffmpeg_path) ffmpegInput.value = cfg.ffmpeg_path;
    if (cfg.filename_template) templateInput.value = cfg.filename_template;
    purgeCheck.checked = cfg.auto_purge_node_modules !== false;
  }).catch(() => {});

  // Load disk space
  window.$api.get("/api/disk-space").then(resp => {
    const d = resp.data;
    const pct = Math.round((d.used / d.total) * 100);
    const freeGB = d.free_gb;
    diskEl.innerHTML = `
      <div style="margin-bottom:8px;">여유 공간: <strong style="color:${freeGB < 5 ? 'var(--col-coral)' : 'var(--col-teal)'};">${freeGB} GB</strong> / ${(d.total/1024**3).toFixed(1)} GB</div>
      <div class="progress-track">
        <div class="progress-fill" style="width:${pct}%;${pct > 85 ? 'background:linear-gradient(90deg,var(--col-coral),#ff4444);' : ''}"></div>
      </div>`;
  }).catch(() => { diskEl.textContent = "디스크 정보를 가져올 수 없습니다."; });

  // Folder picker (Electron IPC)
  dlPathBtn.onclick = async () => {
    if (window.api) {
      const folder = await window.api.selectFolder();
      if (folder) dlPathInput.value = folder;
    }
  };

  saveBtn.onclick = async () => {
    const updates = {
      download_path: dlPathInput.value.trim(),
      ffmpeg_path: ffmpegInput.value.trim(),
      filename_template: templateInput.value.trim(),
      auto_purge_node_modules: purgeCheck.checked,
    };
    try {
      await window.$api.put("/api/config", updates);
      window.$toast("✅ 설정 저장 완료", "success");
    } catch (e) {
      window.$toast(`저장 실패: ${e.message}`, "error");
    }
  };
}
