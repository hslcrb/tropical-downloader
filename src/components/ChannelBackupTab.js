/**
 * Channel Backup Tab
 * Full YouTube Channel & Account Archive for information preservation.
 */

export function mount(root) {
  root.innerHTML = `
    <div style="max-width:780px;margin:0 auto;">
      <div class="glass-card mb-4" style="border-color:rgba(6,214,160,0.3);">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
          <span style="font-size:24px;">🛡</span>
          <div>
            <div style="font-size:15px;font-weight:700;color:var(--col-teal);">채널 완전 백업 — 정보 보전 사명</div>
            <div style="font-size:12px;color:var(--text-muted);">검열과 탄압에 맞서 채널 전체를 영구 아카이브합니다. 자유와 진실을 지킵니다. 🌴</div>
          </div>
        </div>

        <div class="section-title">채널 / 계정 URL</div>
        <div class="flex gap-2 mb-3">
          <input id="cb-url" class="input" placeholder="https://www.youtube.com/@channel 또는 채널 URL" />
          <button id="cb-analyze" class="btn btn-success">🔍 분석</button>
        </div>
        <div id="cb-channel-info" style="display:none;" class="glass-card mb-3" style="padding:12px;"></div>
      </div>

      <div class="glass-card mb-4">
        <div class="section-title">백업 옵션</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;">
          <label class="checkbox-label">
            <input type="checkbox" id="cb-videos" checked /> 영상 다운로드
          </label>
          <label class="checkbox-label">
            <input type="checkbox" id="cb-shorts" checked /> 숏츠 포함
          </label>
          <label class="checkbox-label">
            <input type="checkbox" id="cb-subs" checked /> 자막 저장
          </label>
          <label class="checkbox-label">
            <input type="checkbox" id="cb-thumbs" checked /> 썸네일 저장
          </label>
          <label class="checkbox-label">
            <input type="checkbox" id="cb-metadata" checked /> 메타데이터 JSON 저장
          </label>
          <label class="checkbox-label">
            <input type="checkbox" id="cb-comments" /> 댓글 저장 (느림)
          </label>
          <label class="checkbox-label">
            <input type="checkbox" id="cb-audioonly" /> 오디오 전용 (MP3)
          </label>
        </div>

        <div class="mb-3">
          <div class="section-title" style="margin-bottom:6px;">저장 경로 (선택)</div>
          <div class="flex gap-2">
            <input id="cb-path" class="input" placeholder="기본값 사용 (~/Downloads/Tropical/ChannelBackup/)" />
            <button id="cb-select-path" class="btn btn-ghost btn-sm">📁 선택</button>
          </div>
        </div>

        <button id="cb-start" class="btn btn-success btn-lg w-full">
          🛡 채널 완전 백업 시작
        </button>
      </div>

      <!-- Active Backups -->
      <div id="cb-active-list"></div>
    </div>
  `;

  const urlInput     = root.querySelector("#cb-url");
  const analyzeBtn   = root.querySelector("#cb-analyze");
  const channelInfo  = root.querySelector("#cb-channel-info");
  const startBtn     = root.querySelector("#cb-start");
  const selectPath   = root.querySelector("#cb-select-path");
  const pathInput    = root.querySelector("#cb-path");
  const activeList   = root.querySelector("#cb-active-list");

  const activeTasks = {};

  // Folder selection (Electron IPC)
  selectPath.onclick = async () => {
    if (window.api) {
      const folder = await window.api.selectFolder();
      if (folder) pathInput.value = folder;
    }
  };

  analyzeBtn.onclick = async () => {
    const url = urlInput.value.trim();
    if (!url) return;
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "분석 중...";
    try {
      const resp = await window.$api.post("/api/analyze", { url });
      const info = resp.data;
      channelInfo.style.display = "block";
      channelInfo.innerHTML = `
        <div style="display:flex;gap:12px;align-items:center;">
          <img src="${info.thumbnail || ''}" style="width:80px;height:45px;object-fit:cover;border-radius:6px;border:1px solid var(--glass-border);" onerror="this.style.display='none'"/>
          <div>
            <div style="font-weight:700;color:var(--col-teal);">${escHtml(info.title)}</div>
            <div style="font-size:12px;color:var(--text-muted);">👤 ${escHtml(info.uploader || "")} &nbsp;·&nbsp; 📋 ${info.playlist_count || "?"}개 항목</div>
          </div>
        </div>`;
    } catch (e) {
      window.$toast(`분석 실패: ${e.message}`, "error");
    } finally {
      analyzeBtn.disabled = false;
      analyzeBtn.textContent = "🔍 분석";
    }
  };

  startBtn.onclick = async () => {
    const url = urlInput.value.trim();
    if (!url) { window.$toast("채널 URL을 입력하세요", "error"); return; }

    const opts = {
      channel_url: url,
      download_videos:      root.querySelector("#cb-videos").checked,
      download_shorts:      root.querySelector("#cb-shorts").checked,
      download_subtitles:   root.querySelector("#cb-subs").checked,
      download_thumbnails:  root.querySelector("#cb-thumbs").checked,
      download_metadata_json: root.querySelector("#cb-metadata").checked,
      download_comments:    root.querySelector("#cb-comments").checked,
      download_audio_only:  root.querySelector("#cb-audioonly").checked,
    };
    if (pathInput.value.trim()) opts.backup_path = pathInput.value.trim();

    try {
      const resp = await window.$api.post("/api/channel-backup", opts);
      const backupId = resp.backup_id;
      activeTasks[backupId] = { backup_id: backupId, channel_url: url, status: "pending", completed_items: 0, total_items: 0, current_title: "" };
      renderActiveTasks();
      window.$toast(`✅ 채널 백업 시작! (${backupId})`, "success");
    } catch (e) {
      window.$toast(`백업 시작 실패: ${e.message}`, "error");
    }
  };

  function renderActiveTasks() {
    if (Object.keys(activeTasks).length === 0) {
      activeList.innerHTML = "";
      return;
    }
    activeList.innerHTML = Object.values(activeTasks).map(t => `
      <div class="dl-item" id="backup-${t.backup_id}">
        <div class="dl-header">
          <div class="dl-title">🛡 ${escHtml(t.channel_url)}</div>
          <span class="dl-status status-${t.status}">${t.status}</span>
        </div>
        <div class="progress-track" style="margin-bottom:6px;">
          <div class="progress-fill" style="width:${t.total_items ? Math.round(t.completed_items/t.total_items*100) : 0}%;"></div>
        </div>
        <div class="dl-meta-row">
          <span>📹 ${t.completed_items} / ${t.total_items || "?"} 영상</span>
          ${t.current_title ? `<span>현재: ${escHtml(t.current_title)}</span>` : ""}
        </div>
        <div class="dl-actions">
          <button class="btn btn-danger btn-sm" onclick="cancelBackup('${t.backup_id}')">✕ 취소</button>
        </div>
      </div>
    `).join("");
  }

  window.cancelBackup = async (backupId) => {
    try {
      await window.$api.post(`/api/channel-backup/${backupId}/cancel`);
      if (activeTasks[backupId]) activeTasks[backupId].status = "canceled";
      renderActiveTasks();
    } catch (e) {
      window.$toast(`취소 실패: ${e.message}`, "error");
    }
  };

  // WebSocket channel progress
  window.$ws.on("channel_progress", (msg) => {
    if (activeTasks[msg.backup_id]) {
      Object.assign(activeTasks[msg.backup_id], {
        status: "downloading",
        completed_items: msg.current,
        total_items: msg.total,
        current_title: msg.title
      });
      if (msg.current >= msg.total) {
        activeTasks[msg.backup_id].status = "finished";
        window.$toast(`✅ 채널 백업 완료!`, "success");
      }
      renderActiveTasks();
    }
  });

  function escHtml(str) {
    return String(str || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }
}
