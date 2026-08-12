/**
 * Download Queue Tab
 * Real-time download monitoring via WebSocket.
 * Pause, Resume, Cancel, Retry, Open File/Folder controls.
 */

export function mount(root) {
  root.innerHTML = `
    <div style="max-width:900px;margin:0 auto;">
      <div class="flex items-center justify-between mb-4">
        <h2 style="font-size:16px;font-weight:700;color:var(--col-ocean);">📥 다운로드 큐</h2>
        <button class="btn btn-ghost btn-sm" id="q-refresh">🔄 새로고침</button>
      </div>
      <div id="q-list">
        <div style="text-align:center;padding:60px;color:var(--text-muted);">
          <div style="font-size:36px;margin-bottom:12px;">📭</div>
          <div>활성 다운로드가 없습니다.</div>
        </div>
      </div>
    </div>
  `;

  const listEl = root.querySelector("#q-list");
  const refreshBtn = root.querySelector("#q-refresh");

  const tasks = {};

  refreshBtn.onclick = loadTasks;

  async function loadTasks() {
    try {
      const resp = await window.$api.get("/api/tasks");
      const list = resp.data || [];
      if (list.length === 0) {
        listEl.innerHTML = `
          <div style="text-align:center;padding:60px;color:var(--text-muted);">
            <div style="font-size:36px;margin-bottom:12px;">📭</div>
            <div>활성 다운로드가 없습니다.</div>
          </div>`;
        return;
      }
      list.forEach(t => { tasks[t.task_id] = t; });
      renderAll();
    } catch (e) {
      listEl.innerHTML = `<div style="color:var(--col-coral);padding:20px;">로드 실패: ${e.message}</div>`;
    }
  }

  function renderAll() {
    const taskList = Object.values(tasks).sort((a, b) =>
      ["downloading","pending","paused"].includes(a.status) ? -1 : 1);

    if (taskList.length === 0) {
      listEl.innerHTML = `<div style="text-align:center;padding:60px;color:var(--text-muted);">📭 활성 다운로드 없음</div>`;
      return;
    }

    listEl.innerHTML = taskList.map(t => renderTask(t)).join("");
    // Bind events
    taskList.forEach(t => bindTaskEvents(t.task_id));
  }

  function renderTask(t) {
    const pct = t.progress_percent || 0;
    const isActive = ["downloading","pending"].includes(t.status);
    const isPaused = t.status === "paused";
    const isDone   = t.status === "finished";
    const isError  = t.status === "error";

    return `
    <div class="dl-item" id="task-${t.task_id}">
      <div class="dl-header">
        <div class="dl-title">${escHtml(t.title || t.url)}</div>
        <span class="dl-status status-${t.status}">${statusLabel(t.status)}</span>
      </div>

      <div class="progress-track" style="margin-bottom:6px;">
        <div class="progress-fill" style="width:${pct}%;${isDone ? 'animation:none;' : ''}"></div>
      </div>

      <div class="dl-meta-row">
        <span>⚡ ${t.speed_str || "--"}</span>
        <span>⏱ ${t.eta_str || "--"}</span>
        <span>${pct.toFixed(1)}%</span>
        ${t.filename ? `<span>📄 ${escHtml(t.filename)}</span>` : ""}
      </div>

      ${t.error_msg ? `<div style="color:var(--col-coral);font-size:12px;margin-top:4px;">❌ ${escHtml(t.error_msg)}</div>` : ""}

      <div class="dl-actions">
        ${isActive ? `<button class="btn btn-warning btn-sm" data-action="pause" data-id="${t.task_id}">⏸ 일시정지</button>` : ""}
        ${isPaused ? `<button class="btn btn-primary btn-sm" data-action="resume" data-id="${t.task_id}">▶ 재개</button>` : ""}
        ${(isActive || isPaused) ? `<button class="btn btn-danger btn-sm" data-action="cancel" data-id="${t.task_id}">✕ 취소</button>` : ""}
        ${isError ? `<button class="btn btn-primary btn-sm" data-action="retry" data-id="${t.task_id}">🔄 재시도</button>` : ""}
        ${isDone && t.filepath ? `
          <button class="btn btn-ghost btn-sm" data-action="open-file" data-id="${t.task_id}" data-path="${escHtml(t.filepath)}">📂 파일 열기</button>
          <button class="btn btn-ghost btn-sm" data-action="open-folder" data-id="${t.task_id}" data-path="${escHtml(t.filepath)}">📁 폴더 열기</button>
        ` : ""}
      </div>
    </div>`;
  }

  function bindTaskEvents(taskId) {
    const el = document.getElementById(`task-${taskId}`);
    if (!el) return;
    el.querySelectorAll("[data-action]").forEach(btn => {
      btn.onclick = () => handleAction(btn.dataset.action, taskId, btn.dataset.path);
    });
  }

  async function handleAction(action, taskId, extraPath) {
    try {
      switch (action) {
        case "pause":
          await window.$api.post(`/api/download/${taskId}/pause`);
          tasks[taskId] && (tasks[taskId].status = "paused");
          updateTask(taskId);
          break;
        case "resume":
          await window.$api.post(`/api/download/${taskId}/resume`);
          tasks[taskId] && (tasks[taskId].status = "downloading");
          updateTask(taskId);
          break;
        case "cancel":
          await window.$api.post(`/api/download/${taskId}/cancel`);
          tasks[taskId] && (tasks[taskId].status = "canceled");
          updateTask(taskId);
          break;
        case "retry":
          const r = await window.$api.post(`/api/download/${taskId}/retry`);
          window.$toast(`재시도 시작: ${r.task_id}`, "info");
          loadTasks();
          break;
        case "open-file":
          if (window.api) window.api.openFile(extraPath);
          break;
        case "open-folder":
          if (window.api) {
            const folder = extraPath.replace(/[/\\][^/\\]+$/, "");
            window.api.openPath(folder);
          }
          break;
      }
    } catch (e) {
      window.$toast(`작업 실패: ${e.message}`, "error");
    }
  }

  function updateTask(taskId) {
    const el = document.getElementById(`task-${taskId}`);
    if (el && tasks[taskId]) {
      el.outerHTML = renderTask(tasks[taskId]);
      bindTaskEvents(taskId);
    }
  }

  // WebSocket real-time updates
  window.$ws.on("progress", (msg) => {
    if (!tasks[msg.task_id]) {
      tasks[msg.task_id] = { task_id: msg.task_id, url: "", title: "" };
    }
    Object.assign(tasks[msg.task_id], {
      status: msg.status || "downloading",
      progress_percent: msg.percent,
      speed_str: msg.speed,
      eta_str: msg.eta,
      downloaded_bytes: msg.downloaded,
      total_bytes: msg.total
    });
    updateTask(msg.task_id);
  });

  window.$ws.on("task_complete", (msg) => {
    if (tasks[msg.task_id]) {
      Object.assign(tasks[msg.task_id], {
        status: "finished",
        progress_percent: 100,
        title: msg.title,
        filepath: msg.filepath,
        filename: (msg.filepath || "").split(/[/\\]/).pop()
      });
      updateTask(msg.task_id);
      window.$toast(`✅ 다운로드 완료: ${msg.title}`, "success");
      if (window.api) window.api.showNotification("다운로드 완료 🌴", msg.title);
    }
  });

  window.$ws.on("task_error", (msg) => {
    if (tasks[msg.task_id]) {
      tasks[msg.task_id].status = "error";
      tasks[msg.task_id].error_msg = msg.error;
      updateTask(msg.task_id);
    }
    window.$toast(`❌ 오류: ${msg.error}`, "error");
  });

  function statusLabel(s) {
    return { downloading:"다운로드 중", pending:"대기 중", paused:"일시정지", finished:"완료", error:"오류", canceled:"취소됨" }[s] || s;
  }

  function escHtml(str) {
    return String(str || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }

  // Initial load
  loadTasks();

  // Auto-refresh every 5s while tab is visible
  setInterval(() => {
    if (root.classList.contains("active")) loadTasks();
  }, 5000);
}
