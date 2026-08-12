/**
 * History & Logs Tab
 */

export function mount(root) {
  root.innerHTML = `
    <div style="max-width:900px;margin:0 auto;">
      <div class="flex items-center justify-between mb-4">
        <h2 style="font-size:16px;font-weight:700;color:var(--col-ocean);">📜 다운로드 기록</h2>
        <div class="flex gap-2">
          <input id="h-search" class="input" style="width:220px;" placeholder="🔍 검색..." />
          <button id="h-clear" class="btn btn-danger btn-sm">🗑 전체 삭제</button>
        </div>
      </div>
      <div id="h-list"></div>

      <div class="divider"></div>
      <div class="section-title">실시간 로그</div>
      <div class="log-output" id="h-log" style="height:200px;"></div>
    </div>
  `;

  const listEl   = root.querySelector("#h-list");
  const searchEl = root.querySelector("#h-search");
  const clearBtn = root.querySelector("#h-clear");
  const logEl    = root.querySelector("#h-log");

  loadHistory();

  searchEl.addEventListener("input", () => loadHistory(searchEl.value.trim()));

  clearBtn.onclick = async () => {
    if (!confirm("히스토리를 모두 삭제하시겠습니까?")) return;
    try {
      await window.$api.delete("/api/history");
      loadHistory();
      window.$toast("히스토리 삭제 완료", "success");
    } catch (e) {
      window.$toast(`삭제 실패: ${e.message}`, "error");
    }
  };

  async function loadHistory(q = "") {
    try {
      const path = q ? `/api/history?q=${encodeURIComponent(q)}` : "/api/history";
      const resp = await window.$api.get(path);
      const items = resp.data || [];
      if (items.length === 0) {
        listEl.innerHTML = `<div style="text-align:center;padding:40px;color:var(--text-muted);">📭 다운로드 기록이 없습니다.</div>`;
        return;
      }
      listEl.innerHTML = items.map(item => `
        <div class="dl-item">
          <div class="dl-header">
            <div class="dl-title">${escHtml(item.title || item.url)}</div>
            <span class="dl-status status-${item.status || 'finished'}">${item.status || "완료"}</span>
          </div>
          <div class="dl-meta-row">
            <span>📅 ${item.timestamp || ""}</span>
            <span>💾 ${fmtSize(item.filesize || 0)}</span>
          </div>
          <div style="font-size:11px;color:var(--text-muted);margin-bottom:6px;">${escHtml(item.url || "")}</div>
          <div class="dl-actions">
            ${item.filepath ? `<button class="btn btn-ghost btn-sm" onclick="openHistFile('${escAttr(item.filepath)}')">📂 파일 열기</button>` : ""}
            ${item.filepath ? `<button class="btn btn-ghost btn-sm" onclick="openHistFolder('${escAttr(item.filepath)}')">📁 폴더 열기</button>` : ""}
          </div>
        </div>`).join("");
    } catch (e) {
      listEl.innerHTML = `<div style="color:var(--col-coral);padding:20px;">로드 실패: ${e.message}</div>`;
    }
  }

  window.openHistFile = (path) => { if (window.api) window.api.openFile(path); };
  window.openHistFolder = (path) => {
    if (window.api) {
      const folder = path.replace(/[/\\][^/\\]+$/, "");
      window.api.openPath(folder);
    }
  };

  // Real-time log from WebSocket
  window.$ws.on("log", (msg) => {
    logEl.textContent += msg.message + "\n";
    if (logEl.textContent.split("\n").length > 200) {
      logEl.textContent = logEl.textContent.split("\n").slice(-150).join("\n");
    }
    logEl.scrollTop = logEl.scrollHeight;
  });

  function fmtSize(bytes) {
    if (!bytes) return "?";
    if (bytes > 1024**3) return (bytes/1024**3).toFixed(1) + " GB";
    if (bytes > 1024**2) return (bytes/1024**2).toFixed(1) + " MB";
    return (bytes/1024).toFixed(0) + " KB";
  }

  function escHtml(str) {
    return String(str || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }
  function escAttr(str) {
    return String(str || "").replace(/'/g, "\\'");
  }
}
