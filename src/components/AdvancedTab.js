/**
 * Advanced Options Tab
 * Browser cookies, SponsorBlock, proxy, speed limit, subtitle languages, custom CLI args.
 */

export function mount(root) {
  root.innerHTML = `
    <div style="max-width:720px;margin:0 auto;">
      <h2 style="font-size:16px;font-weight:700;color:var(--col-ocean);margin-bottom:16px;">⚙ 고급 yt-dlp 옵션</h2>

      <div class="glass-card mb-4">
        <div class="section-title">🍪 브라우저 쿠키 (인증 필요 콘텐츠)</div>
        <select id="adv-browser" class="select mb-2"></select>
        <input id="adv-cookie-file" class="input mb-2" placeholder="쿠키 파일 직접 지정 (선택 사항)" />
        <button id="adv-cookie-browse" class="btn btn-ghost btn-sm">📁 파일 선택</button>
      </div>

      <div class="glass-card mb-4">
        <div class="section-title">🚫 SponsorBlock</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
          <label class="checkbox-label"><input type="checkbox" id="sb-sponsor" /> 스폰서 광고 건너뜀</label>
          <label class="checkbox-label"><input type="checkbox" id="sb-intro" /> 인트로 건너뜀</label>
          <label class="checkbox-label"><input type="checkbox" id="sb-outro" /> 아웃트로 건너뜀</label>
          <label class="checkbox-label"><input type="checkbox" id="sb-selfpromo" /> 자기 홍보 건너뜀</label>
        </div>
      </div>

      <div class="glass-card mb-4">
        <div class="section-title">🌐 네트워크</div>
        <div class="mb-3">
          <div style="font-size:12px;color:var(--text-muted);margin-bottom:4px;">프록시 주소</div>
          <input id="adv-proxy" class="input" placeholder="예: socks5://127.0.0.1:1080 또는 http://proxy:8080" />
        </div>
        <div>
          <div style="font-size:12px;color:var(--text-muted);margin-bottom:4px;">속도 제한</div>
          <input id="adv-ratelimit" class="input" placeholder="예: 5M (5MB/s), 500K (500KB/s)" />
        </div>
      </div>

      <div class="glass-card mb-4">
        <div class="section-title">🔠 자막 언어</div>
        <input id="adv-sub-langs" class="input" placeholder="예: ko,en,ja (쉼표로 구분)" value="ko,en" />
      </div>

      <div class="glass-card mb-4">
        <div class="section-title">🔧 사용자 정의 yt-dlp CLI 인수 (고급)</div>
        <textarea id="adv-cli" class="textarea" placeholder="예: --geo-bypass --no-overwrites --no-playlist"></textarea>
        <div style="font-size:11px;color:var(--text-muted);margin-top:6px;">yt-dlp의 모든 옵션을 직접 전달합니다. 다운로드 시 자동으로 적용됩니다.</div>
      </div>

      <button id="adv-save" class="btn btn-success btn-lg w-full">💾 설정 저장</button>
    </div>
  `;

  const browserSel   = root.querySelector("#adv-browser");
  const cookieFile   = root.querySelector("#adv-cookie-file");
  const cookieBrowse = root.querySelector("#adv-cookie-browse");
  const proxyInput   = root.querySelector("#adv-proxy");
  const rateInput    = root.querySelector("#adv-ratelimit");
  const subLangs     = root.querySelector("#adv-sub-langs");
  const cliInput     = root.querySelector("#adv-cli");
  const saveBtn      = root.querySelector("#adv-save");

  // Load browsers
  window.$api.get("/api/browsers").then(resp => {
    const browsers = resp.data || [];
    browserSel.innerHTML = browsers
      .filter(b => b.installed)
      .map(b => `<option value="${b.key}">${b.name}</option>`)
      .join("");
  }).catch(() => {});

  // Load current config
  window.$api.get("/api/config").then(resp => {
    const cfg = resp.data || {};
    if (cfg.browser_cookies) browserSel.value = cfg.browser_cookies;
    if (cfg.proxy) proxyInput.value = cfg.proxy;
    if (cfg.rate_limit) rateInput.value = cfg.rate_limit;
    if (cfg.custom_cli_args) cliInput.value = cfg.custom_cli_args;
  }).catch(() => {});

  // Cookie file browser (Electron IPC)
  cookieBrowse.onclick = async () => {
    if (window.api) {
      const result = await window.api.selectFolder();
      if (result) cookieFile.value = result;
    }
  };

  saveBtn.onclick = async () => {
    const sbRemove = [];
    if (root.querySelector("#sb-sponsor").checked) sbRemove.push("sponsor");
    if (root.querySelector("#sb-intro").checked) sbRemove.push("intro");
    if (root.querySelector("#sb-outro").checked) sbRemove.push("outro");
    if (root.querySelector("#sb-selfpromo").checked) sbRemove.push("selfpromo");

    const updates = {
      browser_cookies: browserSel.value,
      proxy: proxyInput.value.trim(),
      rate_limit: rateInput.value.trim(),
      sub_langs: subLangs.value.trim(),
      custom_cli_args: cliInput.value.trim(),
      sponsorblock: sbRemove.length > 0,
    };

    try {
      await window.$api.put("/api/config", updates);
      window.$toast("✅ 고급 옵션 저장 완료", "success");
    } catch (e) {
      window.$toast(`저장 실패: ${e.message}`, "error");
    }
  };
}
