/**
 * Format Inspector Tab
 * Detailed stream format table, video/audio selection, container choice, download.
 */

export function mount(root) {
  root.innerHTML = `
    <div style="max-width:900px;margin:0 auto;">
      <div class="glass-card mb-4">
        <div class="section-title">URL 분석</div>
        <div class="flex gap-2 mb-2">
          <input id="fi-url" class="input" placeholder="YouTube URL..." />
          <button id="fi-analyze" class="btn btn-primary">🔍 분석</button>
        </div>
      </div>

      <div id="fi-loading" style="display:none;text-align:center;padding:40px;">
        <div class="spinner" style="margin:0 auto 12px;width:32px;height:32px;"></div>
        <div style="color:var(--text-muted);">스트림 정보 분석 중...</div>
      </div>

      <div id="fi-result" style="display:none;">
        <div id="fi-media-card" class="media-card mb-4"></div>

        <div class="glass-card mb-4">
          <div class="section-title">비디오 스트림</div>
          <div style="overflow-x:auto;">
            <table class="format-table" id="fi-video-table">
              <thead><tr>
                <th>선택</th><th>ID</th><th>해상도</th><th>코덱</th><th>FPS</th><th>비트레이트</th><th>크기</th>
              </tr></thead>
              <tbody></tbody>
            </table>
          </div>
        </div>

        <div class="glass-card mb-4">
          <div class="section-title">오디오 스트림</div>
          <div style="overflow-x:auto;">
            <table class="format-table" id="fi-audio-table">
              <thead><tr>
                <th>선택</th><th>ID</th><th>코덱</th><th>비트레이트</th><th>크기</th>
              </tr></thead>
              <tbody></tbody>
            </table>
          </div>
        </div>

        <div class="glass-card mb-4">
          <div class="section-title">출력 옵션</div>
          <div class="flex gap-3 flex-wrap mb-3">
            <label class="checkbox-label">
              <input type="checkbox" id="fi-embed-subs" checked /> 자막 임베딩
            </label>
            <label class="checkbox-label">
              <input type="checkbox" id="fi-embed-thumb" checked /> 썸네일 임베딩
            </label>
          </div>
          <div class="flex gap-2 items-center mb-3">
            <span style="color:var(--text-muted);font-size:13px;">컨테이너:</span>
            <select id="fi-container" class="select" style="width:120px;">
              <option value="mp4">MP4</option>
              <option value="mkv">MKV</option>
              <option value="webm">WEBM</option>
            </select>
          </div>
          <button id="fi-download" class="btn btn-primary btn-lg">⬇ 선택된 포맷으로 다운로드</button>
        </div>
      </div>
    </div>
  `;

  const urlInput   = root.querySelector("#fi-url");
  const analyzeBtn = root.querySelector("#fi-analyze");
  const loadingEl  = root.querySelector("#fi-loading");
  const resultEl   = root.querySelector("#fi-result");
  const cardEl     = root.querySelector("#fi-media-card");
  const dlBtn      = root.querySelector("#fi-download");

  let currentInfo = null;
  let selectedVideo = null;
  let selectedAudio = null;

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
      renderMediaCard(currentInfo);
      renderFormats(currentInfo.formats || []);
      loadingEl.style.display = "none";
      resultEl.style.display = "block";
    } catch (e) {
      loadingEl.style.display = "none";
      window.$toast(`분석 실패: ${e.message}`, "error");
    }
  }

  function renderMediaCard(info) {
    cardEl.innerHTML = `
      <img class="media-thumb" src="${info.thumbnail || ''}" onerror="this.style.display='none'" />
      <div class="media-info">
        <div class="media-title">${escHtml(info.title)}</div>
        <div class="media-meta">
          <span class="meta-item">👤 ${escHtml(info.uploader || "")}</span>
          <span class="meta-item">⏱ ${info.duration_string}</span>
        </div>
      </div>`;
  }

  function fmtSize(bytes) {
    if (!bytes) return "?";
    if (bytes > 1024**3) return (bytes/1024**3).toFixed(1) + " GB";
    if (bytes > 1024**2) return (bytes/1024**2).toFixed(1) + " MB";
    return (bytes/1024).toFixed(0) + " KB";
  }

  function renderFormats(formats) {
    const videos = formats.filter(f => f.vcodec !== "none" && f.vcodec);
    const audios  = formats.filter(f => f.vcodec === "none" && f.acodec !== "none");

    const videoTbody = root.querySelector("#fi-video-table tbody");
    videoTbody.innerHTML = videos.map((f, i) => `
      <tr class="${i === 0 ? 'selected' : ''}" data-fid="${f.format_id}" data-type="video" style="cursor:pointer;">
        <td><input type="radio" name="vid" ${i === 0 ? "checked" : ""} /></td>
        <td>${f.format_id}</td>
        <td>${f.resolution}</td>
        <td>${f.vcodec}</td>
        <td>${f.fps || "?"}</td>
        <td>${f.tbr ? f.tbr.toFixed(0) + " kbps" : "?"}</td>
        <td>${fmtSize(f.filesize_approx)}</td>
      </tr>`).join("");

    const audioTbody = root.querySelector("#fi-audio-table tbody");
    audioTbody.innerHTML = audios.map((f, i) => `
      <tr class="${i === 0 ? 'selected' : ''}" data-fid="${f.format_id}" data-type="audio" style="cursor:pointer;">
        <td><input type="radio" name="aud" ${i === 0 ? "checked" : ""} /></td>
        <td>${f.format_id}</td>
        <td>${f.acodec}</td>
        <td>${f.tbr ? f.tbr.toFixed(0) + " kbps" : "?"}</td>
        <td>${fmtSize(f.filesize_approx)}</td>
      </tr>`).join("");

    if (videos.length > 0) selectedVideo = videos[0].format_id;
    if (audios.length > 0) selectedAudio  = audios[0].format_id;

    [videoTbody, audioTbody].forEach(tbody => {
      tbody.querySelectorAll("tr").forEach(row => {
        row.onclick = () => {
          const type = row.dataset.type;
          tbody.querySelectorAll("tr").forEach(r => r.classList.remove("selected"));
          row.classList.add("selected");
          row.querySelector("input[type=radio]").checked = true;
          if (type === "video") selectedVideo = row.dataset.fid;
          else selectedAudio = row.dataset.fid;
        };
      });
    });
  }

  dlBtn.onclick = async () => {
    if (!currentInfo) return;
    const container = root.querySelector("#fi-container").value;
    const embedSubs = root.querySelector("#fi-embed-subs").checked;
    const embedThumb = root.querySelector("#fi-embed-thumb").checked;

    let format = "bestvideo+bestaudio/best";
    if (selectedVideo && selectedAudio) format = `${selectedVideo}+${selectedAudio}`;
    else if (selectedVideo) format = selectedVideo;

    try {
      const resp = await window.$api.post("/api/download", {
        url: currentInfo.url,
        format_id: format,
        container,
        embed_subtitles: embedSubs,
        embed_thumbnail: embedThumb
      });
      window.$toast(`✅ 다운로드 시작! (${resp.task_id})`, "success");
      document.querySelector('[data-tab="queue"]')?.click();
    } catch (e) {
      window.$toast(`다운로드 실패: ${e.message}`, "error");
    }
  };

  function escHtml(str) {
    return String(str || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }
}
