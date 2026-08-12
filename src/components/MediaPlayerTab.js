/**
 * Media Player Tab
 * Built-in HTML5 video/audio player with downloaded files browser.
 */

export function mount(root) {
  root.innerHTML = `
    <div style="display:grid;grid-template-columns:280px 1fr;gap:16px;height:calc(100vh - 140px);">
      <!-- File List -->
      <div class="glass" style="padding:16px;overflow-y:auto;">
        <div class="section-title">📁 다운로드 파일</div>
        <div id="mp-filelist"></div>
      </div>

      <!-- Player -->
      <div style="display:flex;flex-direction:column;gap:12px;">
        <div class="glass-card" style="flex:1;display:flex;align-items:center;justify-content:center;min-height:0;">
          <video id="mp-video" controls style="max-width:100%;max-height:100%;border-radius:8px;display:none;"></video>
          <audio id="mp-audio" controls style="width:100%;display:none;"></audio>
          <div id="mp-placeholder" style="text-align:center;color:var(--text-muted);">
            <div style="font-size:48px;margin-bottom:12px;">▶</div>
            <div>왼쪽에서 파일을 선택하세요</div>
          </div>
        </div>

        <div class="glass-card" style="padding:12px;">
          <div style="font-size:13px;font-weight:600;color:var(--text-secondary);margin-bottom:8px;" id="mp-title">—</div>
          <div class="flex gap-2 items-center">
            <span style="font-size:12px;color:var(--text-muted);">배속:</span>
            <select id="mp-rate" class="select" style="width:90px;">
              <option value="0.5">0.5x</option>
              <option value="1" selected>1.0x</option>
              <option value="1.25">1.25x</option>
              <option value="1.5">1.5x</option>
              <option value="2">2.0x</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  `;

  const fileList  = root.querySelector("#mp-filelist");
  const video     = root.querySelector("#mp-video");
  const audio     = root.querySelector("#mp-audio");
  const placeholder = root.querySelector("#mp-placeholder");
  const titleEl   = root.querySelector("#mp-title");
  const rateEl    = root.querySelector("#mp-rate");

  rateEl.onchange = () => {
    video.playbackRate = parseFloat(rateEl.value);
    audio.playbackRate = parseFloat(rateEl.value);
  };

  loadFiles();

  async function loadFiles() {
    try {
      const resp = await window.$api.get("/api/files");
      const files = (resp.data || []).filter(f =>
        /\.(mp4|mkv|webm|mp3|m4a|flac|wav|ogg|avi|mov)$/i.test(f.name)
      );

      if (files.length === 0) {
        fileList.innerHTML = `<div style="color:var(--text-muted);font-size:12px;padding:12px 0;">다운로드된 파일 없음</div>`;
        return;
      }

      fileList.innerHTML = files.map(f => `
        <div class="glass-card" style="padding:10px;margin-bottom:8px;cursor:pointer;" onclick="playFile('${escAttr(f.path)}', '${escAttr(f.name)}')">
          <div style="font-size:12px;font-weight:600;color:var(--text-secondary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${escHtml(f.name)}</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:2px;">${fmtSize(f.size)}</div>
        </div>`).join("");
    } catch (e) {
      fileList.innerHTML = `<div style="color:var(--col-coral);font-size:12px;">로드 실패: ${e.message}</div>`;
    }
  }

  window.playFile = (path, name) => {
    const isAudio = /\.(mp3|m4a|flac|wav|ogg)$/i.test(name);
    placeholder.style.display = "none";

    if (isAudio) {
      video.style.display = "none";
      audio.style.display = "block";
      audio.src = `file://${path}`;
      audio.play().catch(() => {});
    } else {
      audio.style.display = "none";
      video.style.display = "block";
      video.src = `file://${path}`;
      video.play().catch(() => {});
    }
    titleEl.textContent = name;
  };

  function fmtSize(bytes) {
    if (!bytes) return "";
    if (bytes > 1024**3) return (bytes/1024**3).toFixed(1) + " GB";
    if (bytes > 1024**2) return (bytes/1024**2).toFixed(1) + " MB";
    return (bytes/1024).toFixed(0) + " KB";
  }
  function escHtml(str) { return String(str || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
  function escAttr(str) { return String(str || "").replace(/'/g, "\\'"); }
}
