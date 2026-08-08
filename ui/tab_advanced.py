"""
Tropical Downloader - Advanced yt-dlp Options Tab
Every major yt-dlp option exposed with a clean, grouped layout.
Direct CLI pass-through covers anything not explicitly listed.
"""
import shlex
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QCheckBox, QGroupBox, QPushButton, QFileDialog, QScrollArea,
    QFrame, QGridLayout, QSpinBox, QSizePolicy
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from assets.icons import get_icon
from core.config import config_manager
from core.cookie_manager import SUPPORTED_BROWSERS


def _row(label_text: str, widget, hint: str = "") -> QHBoxLayout:
    """Helper: label + widget in a horizontal row."""
    row = QHBoxLayout()
    row.setSpacing(8)
    lbl = QLabel(label_text)
    lbl.setFixedWidth(160)
    lbl.setStyleSheet("color: #334155; font-size: 12px;")
    row.addWidget(lbl)
    row.addWidget(widget, stretch=1)
    if hint:
        h = QLabel(hint)
        h.setStyleSheet("color: #94A3B8; font-size: 11px;")
        row.addWidget(h)
    return row


class AdvancedTab(QWidget):
    settings_saved = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Scroll area ──────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # ────────────────────────────────────────────────────────────
        # 1. 출력 / 저장 설정
        # ────────────────────────────────────────────────────────────
        grp_out = QGroupBox("출력 / 저장")
        g = QVBoxLayout(grp_out)

        self.txt_output_tmpl = QLineEdit(config_manager.get(
            "output_template", "%(uploader)s/%(title)s.%(ext)s"))
        self.txt_output_tmpl.setPlaceholderText("%(title)s.%(ext)s")
        g.addLayout(_row("파일명 템플릿:", self.txt_output_tmpl,
                         "yt-dlp -o 와 동일"))

        self.combo_merge_fmt = QComboBox()
        for fmt in ["mkv", "mp4", "webm", "ogg", "opus", "flac", "mp3", "m4a"]:
            self.combo_merge_fmt.addItem(fmt, fmt)
        saved_merge = config_manager.get("merge_output_format", "mkv")
        self.combo_merge_fmt.setCurrentText(saved_merge)
        g.addLayout(_row("병합 컨테이너:", self.combo_merge_fmt))

        self.chk_restrict_filenames = QCheckBox("특수문자 제거 (--restrict-filenames)")
        self.chk_restrict_filenames.setChecked(config_manager.get("restrict_filenames", False))
        self.chk_no_overwrites = QCheckBox("이미 있으면 건너뜀 (--no-overwrites)")
        self.chk_no_overwrites.setChecked(config_manager.get("no_overwrites", True))
        self.chk_write_desc = QCheckBox("설명 파일 저장 (--write-description)")
        self.chk_write_desc.setChecked(config_manager.get("write_description", False))
        self.chk_write_info = QCheckBox("info.json 저장 (--write-info-json)")
        self.chk_write_info.setChecked(config_manager.get("write_info_json", False))
        self.chk_write_comments = QCheckBox("댓글 저장 (--write-comments)")
        self.chk_write_comments.setChecked(config_manager.get("write_comments", False))

        for chk in [self.chk_restrict_filenames, self.chk_no_overwrites,
                    self.chk_write_desc, self.chk_write_info, self.chk_write_comments]:
            g.addWidget(chk)

        layout.addWidget(grp_out)

        # ────────────────────────────────────────────────────────────
        # 2. 비디오 / 오디오 포스트프로세싱
        # ────────────────────────────────────────────────────────────
        grp_pp = QGroupBox("포스트프로세싱 (FFmpeg)")
        g2 = QVBoxLayout(grp_pp)

        self.chk_embed_thumb = QCheckBox("썸네일 임베딩 (--embed-thumbnail)")
        self.chk_embed_thumb.setChecked(config_manager.get("embed_thumbnail", True))
        self.chk_embed_meta = QCheckBox("메타데이터 임베딩 (--add-metadata)")
        self.chk_embed_meta.setChecked(config_manager.get("embed_metadata", True))
        self.chk_embed_chapters = QCheckBox("챕터 마커 임베딩 (--embed-chapters)")
        self.chk_embed_chapters.setChecked(config_manager.get("embed_chapters", False))
        self.chk_remux_video = QCheckBox("리먹스만 (재인코딩 없음, --remux-video)")
        self.chk_remux_video.setChecked(config_manager.get("remux_video", False))

        self.combo_recode_video = QComboBox()
        for c in ["없음", "mp4", "mkv", "webm", "avi", "flv"]:
            self.combo_recode_video.addItem(c)
        self.combo_recode_video.setCurrentText(config_manager.get("recode_video", "없음"))

        for chk in [self.chk_embed_thumb, self.chk_embed_meta,
                    self.chk_embed_chapters, self.chk_remux_video]:
            g2.addWidget(chk)
        g2.addLayout(_row("비디오 재인코딩 (--recode-video):", self.combo_recode_video))

        layout.addWidget(grp_pp)

        # ────────────────────────────────────────────────────────────
        # 3. 자막
        # ────────────────────────────────────────────────────────────
        grp_sub = QGroupBox("자막")
        g3 = QVBoxLayout(grp_sub)

        self.chk_embed_subs = QCheckBox("자막 임베딩 (--embed-subs)")
        self.chk_embed_subs.setChecked(config_manager.get("embed_subs", False))
        self.chk_write_subs = QCheckBox("자막 파일 저장 (--write-subs)")
        self.chk_write_subs.setChecked(config_manager.get("write_subs", False))
        self.chk_auto_subs = QCheckBox("자동 생성 자막 포함 (--write-auto-subs)")
        self.chk_auto_subs.setChecked(config_manager.get("write_auto_subs", False))

        self.txt_sub_langs = QLineEdit(config_manager.get("sub_langs", "ko,en.*"))
        self.txt_sub_langs.setPlaceholderText("ko,en.* (쉼표로 구분)")
        self.combo_sub_fmt = QComboBox()
        for sf in ["srt", "vtt", "ass", "lrc", "json3"]:
            self.combo_sub_fmt.addItem(sf)
        self.combo_sub_fmt.setCurrentText(config_manager.get("sub_format", "srt"))

        for chk in [self.chk_embed_subs, self.chk_write_subs, self.chk_auto_subs]:
            g3.addWidget(chk)
        g3.addLayout(_row("자막 언어 코드:", self.txt_sub_langs))
        g3.addLayout(_row("자막 형식:", self.combo_sub_fmt))

        layout.addWidget(grp_sub)

        # ────────────────────────────────────────────────────────────
        # 4. 재생목록 / 범위
        # ────────────────────────────────────────────────────────────
        grp_pl = QGroupBox("재생목록 / 범위 (플레이리스트 탭과 연동)")
        g4 = QVBoxLayout(grp_pl)

        self.spin_playlist_start = QSpinBox()
        self.spin_playlist_start.setMinimum(1); self.spin_playlist_start.setMaximum(9999)
        self.spin_playlist_start.setValue(config_manager.get("playlist_start", 1))
        self.spin_playlist_end = QSpinBox()
        self.spin_playlist_end.setMinimum(0); self.spin_playlist_end.setMaximum(9999)
        self.spin_playlist_end.setValue(config_manager.get("playlist_end", 0))
        self.spin_playlist_end.setSpecialValueText("끝까지")

        self.txt_playlist_items = QLineEdit(config_manager.get("playlist_items", ""))
        self.txt_playlist_items.setPlaceholderText("1,3,5-10  (비워두면 전체)")

        self.spin_concurrent = QSpinBox()
        self.spin_concurrent.setMinimum(1); self.spin_concurrent.setMaximum(16)
        self.spin_concurrent.setValue(config_manager.get("concurrent_fragments", 4))

        g4.addLayout(_row("시작 항목 (--playlist-start):", self.spin_playlist_start))
        g4.addLayout(_row("종료 항목 (--playlist-end):", self.spin_playlist_end))
        g4.addLayout(_row("항목 지정 (--playlist-items):", self.txt_playlist_items))
        g4.addLayout(_row("동시 프래그먼트 수 (--concurrent-fragments):", self.spin_concurrent,
                          "HLS/DASH 고속화"))

        layout.addWidget(grp_pl)

        # ────────────────────────────────────────────────────────────
        # 5. SponsorBlock
        # ────────────────────────────────────────────────────────────
        grp_sb = QGroupBox("SponsorBlock (YouTube 전용)")
        g5 = QVBoxLayout(grp_sb)

        self.chk_sponsorblock = QCheckBox("SponsorBlock 사용 (--sponsorblock-remove all)")
        self.chk_sponsorblock.setChecked(config_manager.get("sponsorblock", False))

        self.txt_sponsorblock_cats = QLineEdit(config_manager.get(
            "sponsorblock_categories", "sponsor,intro,outro,selfpromo"))
        self.txt_sponsorblock_cats.setPlaceholderText("sponsor,intro,outro,selfpromo,interaction")

        g5.addWidget(self.chk_sponsorblock)
        g5.addLayout(_row("제거 카테고리:", self.txt_sponsorblock_cats))
        layout.addWidget(grp_sb)

        # ────────────────────────────────────────────────────────────
        # 6. 쿠키 / 인증
        # ────────────────────────────────────────────────────────────
        grp_auth = QGroupBox("쿠키 / 인증")
        g6 = QVBoxLayout(grp_auth)

        self.combo_browser = QComboBox()
        for name, code in SUPPORTED_BROWSERS:
            self.combo_browser.addItem(name, code)
        cur_b = config_manager.get("cookie_browser", "")
        idx = self.combo_browser.findData(cur_b)
        if idx >= 0:
            self.combo_browser.setCurrentIndex(idx)
        g6.addLayout(_row("브라우저 쿠키 연동:", self.combo_browser))

        cookie_row = QHBoxLayout()
        cookie_row.setSpacing(8)
        cookie_row.addWidget(QLabel("쿠키 파일 (cookies.txt):"))
        self.txt_cookie_file = QLineEdit(config_manager.get("cookies_file", ""))
        self.txt_cookie_file.setPlaceholderText("선택 사항")
        btn_browse_cookie = QPushButton("...")
        btn_browse_cookie.setFixedWidth(36)
        btn_browse_cookie.clicked.connect(self._browse_cookie)
        cookie_row.addWidget(self.txt_cookie_file, stretch=1)
        cookie_row.addWidget(btn_browse_cookie)
        g6.addLayout(cookie_row)

        self.txt_username = QLineEdit(config_manager.get("username", ""))
        self.txt_username.setPlaceholderText("사이트 계정 아이디")
        self.txt_password = QLineEdit(config_manager.get("password", ""))
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setPlaceholderText("사이트 계정 비밀번호")

        self.txt_netrc = QLineEdit(config_manager.get("netrc_location", ""))
        self.txt_netrc.setPlaceholderText(".netrc 파일 경로 (선택)")

        self.chk_ap_mso = QCheckBox("Adobe Pass / TV Everywhere 인증 사용")
        self.chk_ap_mso.setChecked(config_manager.get("ap_mso", False))

        g6.addLayout(_row("사용자 이름 (-u):", self.txt_username))
        g6.addLayout(_row("비밀번호 (-p):", self.txt_password))
        g6.addLayout(_row("netrc 위치:", self.txt_netrc))
        g6.addWidget(self.chk_ap_mso)

        layout.addWidget(grp_auth)

        # ────────────────────────────────────────────────────────────
        # 7. 네트워크
        # ────────────────────────────────────────────────────────────
        grp_net = QGroupBox("네트워크")
        g7 = QVBoxLayout(grp_net)

        self.txt_proxy = QLineEdit(config_manager.get("proxy", ""))
        self.txt_proxy.setPlaceholderText("http://127.0.0.1:8080 또는 socks5://...")
        self.txt_rate_limit = QLineEdit(config_manager.get("rate_limit", ""))
        self.txt_rate_limit.setPlaceholderText("예: 5M, 500k  (비우면 제한 없음)")
        self.txt_source_address = QLineEdit(config_manager.get("source_address", ""))
        self.txt_source_address.setPlaceholderText("바인딩할 로컬 IP (선택)")

        self.chk_force_ipv4 = QCheckBox("IPv4 강제 사용 (--force-ipv4)")
        self.chk_force_ipv4.setChecked(config_manager.get("force_ipv4", False))
        self.chk_force_ipv6 = QCheckBox("IPv6 강제 사용 (--force-ipv6)")
        self.chk_force_ipv6.setChecked(config_manager.get("force_ipv6", False))

        self.spin_retries = QSpinBox()
        self.spin_retries.setMinimum(0); self.spin_retries.setMaximum(100)
        self.spin_retries.setValue(config_manager.get("retries", 10))

        self.spin_socket_timeout = QSpinBox()
        self.spin_socket_timeout.setMinimum(5); self.spin_socket_timeout.setMaximum(300)
        self.spin_socket_timeout.setValue(config_manager.get("socket_timeout", 30))

        g7.addLayout(_row("프록시:", self.txt_proxy))
        g7.addLayout(_row("속도 제한:", self.txt_rate_limit))
        g7.addLayout(_row("소스 주소:", self.txt_source_address))
        g7.addLayout(_row("재시도 횟수:", self.spin_retries))
        g7.addLayout(_row("소켓 타임아웃 (초):", self.spin_socket_timeout))
        g7.addWidget(self.chk_force_ipv4)
        g7.addWidget(self.chk_force_ipv6)

        layout.addWidget(grp_net)

        # ────────────────────────────────────────────────────────────
        # 8. 지역 우회 / 기타
        # ────────────────────────────────────────────────────────────
        grp_misc = QGroupBox("지역 우회 / 기타")
        g8 = QVBoxLayout(grp_misc)

        self.chk_geo_bypass = QCheckBox("지역 제한 우회 시도 (--geo-bypass)")
        self.chk_geo_bypass.setChecked(config_manager.get("geo_bypass", False))
        self.txt_geo_country = QLineEdit(config_manager.get("geo_bypass_country", ""))
        self.txt_geo_country.setPlaceholderText("예: US, KR (비우면 자동)")
        self.chk_age_limit = QCheckBox("연령 제한 건너뜀 (--age-limit 99)")
        self.chk_age_limit.setChecked(config_manager.get("bypass_age_limit", False))
        self.txt_download_archive = QLineEdit(config_manager.get("download_archive", ""))
        self.txt_download_archive.setPlaceholderText("archive.txt 경로 — 이미 다운로드한 항목 건너뜀")
        btn_archive = QPushButton("...")
        btn_archive.setFixedWidth(36)
        btn_archive.clicked.connect(self._browse_archive)

        arch_row = QHBoxLayout()
        arch_row.addWidget(QLabel("다운로드 아카이브:"))
        arch_row.addWidget(self.txt_download_archive, stretch=1)
        arch_row.addWidget(btn_archive)

        self.chk_no_playlist = QCheckBox("URL이 재생목록이어도 단일 항목만 다운로드 (--no-playlist)")
        self.chk_no_playlist.setChecked(config_manager.get("no_playlist", False))

        g8.addWidget(self.chk_geo_bypass)
        g8.addLayout(_row("우회 국가 코드:", self.txt_geo_country))
        g8.addWidget(self.chk_age_limit)
        g8.addLayout(arch_row)
        g8.addWidget(self.chk_no_playlist)

        layout.addWidget(grp_misc)

        # ────────────────────────────────────────────────────────────
        # 9. Custom CLI (100% yt-dlp pass-through)
        # ────────────────────────────────────────────────────────────
        grp_cli = QGroupBox("사용자 정의 CLI 인자 — yt-dlp의 모든 기능 지원")
        g9 = QVBoxLayout(grp_cli)

        hint = QLabel(
            "위 옵션으로 제공되지 않는 yt-dlp 인자를 직접 입력하세요.\n"
            "예:  --write-comments --compat-options filename  --extractor-args \"youtube:skip=dash\""
        )
        hint.setStyleSheet("color: #475569; font-size: 11px;")
        hint.setWordWrap(True)
        g9.addWidget(hint)

        self.txt_custom_cli = QLineEdit(config_manager.get("custom_cli_args", ""))
        self.txt_custom_cli.setPlaceholderText("--option value --flag ...")
        g9.addWidget(self.txt_custom_cli)

        layout.addWidget(grp_cli)

        # ────────────────────────────────────────────────────────────
        # Save button (sticky bottom)
        # ────────────────────────────────────────────────────────────
        layout.addStretch()
        scroll.setWidget(container)
        outer.addWidget(scroll, stretch=1)

        # Bottom save bar
        bar = QFrame()
        bar.setStyleSheet("background:#FFFFFF; border-top:1px solid #BAE6FD;")
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(16, 8, 16, 8)
        bar_layout.addStretch()
        self.btn_save = QPushButton("설정 저장")
        self.btn_save.setObjectName("btn_primary")
        self.btn_save.setIcon(get_icon("check", 18))
        self.btn_save.setFixedHeight(38)
        self.btn_save.setMinimumWidth(120)
        self.btn_save.clicked.connect(self.save_settings)
        bar_layout.addWidget(self.btn_save)
        outer.addWidget(bar)

    # ── Helpers ──────────────────────────────────────────────────────
    def _browse_cookie(self):
        p, _ = QFileDialog.getOpenFileName(self, "쿠키 파일", "", "Text (*.txt);;All (*)")
        if p:
            self.txt_cookie_file.setText(p)

    def _browse_archive(self):
        p, _ = QFileDialog.getSaveFileName(self, "아카이브 파일", "archive.txt",
                                           "Text (*.txt);;All (*)")
        if p:
            self.txt_download_archive.setText(p)

    def save_settings(self):
        cfg = config_manager
        cfg.set("output_template", self.txt_output_tmpl.text().strip())
        cfg.set("merge_output_format", self.combo_merge_fmt.currentData())
        cfg.set("restrict_filenames", self.chk_restrict_filenames.isChecked())
        cfg.set("no_overwrites", self.chk_no_overwrites.isChecked())
        cfg.set("write_description", self.chk_write_desc.isChecked())
        cfg.set("write_info_json", self.chk_write_info.isChecked())
        cfg.set("write_comments", self.chk_write_comments.isChecked())
        cfg.set("embed_thumbnail", self.chk_embed_thumb.isChecked())
        cfg.set("embed_metadata", self.chk_embed_meta.isChecked())
        cfg.set("embed_chapters", self.chk_embed_chapters.isChecked())
        cfg.set("remux_video", self.chk_remux_video.isChecked())
        cfg.set("recode_video", self.combo_recode_video.currentText())
        cfg.set("embed_subs", self.chk_embed_subs.isChecked())
        cfg.set("write_subs", self.chk_write_subs.isChecked())
        cfg.set("write_auto_subs", self.chk_auto_subs.isChecked())
        cfg.set("sub_langs", self.txt_sub_langs.text().strip())
        cfg.set("sub_format", self.combo_sub_fmt.currentText())
        cfg.set("playlist_start", self.spin_playlist_start.value())
        cfg.set("playlist_end", self.spin_playlist_end.value())
        cfg.set("playlist_items", self.txt_playlist_items.text().strip())
        cfg.set("concurrent_fragments", self.spin_concurrent.value())
        cfg.set("sponsorblock", self.chk_sponsorblock.isChecked())
        cfg.set("sponsorblock_categories", self.txt_sponsorblock_cats.text().strip())
        cfg.set("cookie_browser", self.combo_browser.currentData())
        cfg.set("cookies_file", self.txt_cookie_file.text().strip())
        cfg.set("username", self.txt_username.text().strip())
        cfg.set("password", self.txt_password.text())
        cfg.set("netrc_location", self.txt_netrc.text().strip())
        cfg.set("ap_mso", self.chk_ap_mso.isChecked())
        cfg.set("proxy", self.txt_proxy.text().strip())
        cfg.set("rate_limit", self.txt_rate_limit.text().strip())
        cfg.set("source_address", self.txt_source_address.text().strip())
        cfg.set("force_ipv4", self.chk_force_ipv4.isChecked())
        cfg.set("force_ipv6", self.chk_force_ipv6.isChecked())
        cfg.set("retries", self.spin_retries.value())
        cfg.set("socket_timeout", self.spin_socket_timeout.value())
        cfg.set("geo_bypass", self.chk_geo_bypass.isChecked())
        cfg.set("geo_bypass_country", self.txt_geo_country.text().strip())
        cfg.set("bypass_age_limit", self.chk_age_limit.isChecked())
        cfg.set("download_archive", self.txt_download_archive.text().strip())
        cfg.set("no_playlist", self.chk_no_playlist.isChecked())
        cfg.set("custom_cli_args", self.txt_custom_cli.text().strip())
        self.settings_saved.emit()

    def get_custom_args(self) -> str:
        return self.txt_custom_cli.text().strip()

    def get_ydl_opts(self) -> dict:
        """Returns a yt-dlp options dict from all UI settings (used by DownloadWorker)."""
        cfg = config_manager
        opts = {}

        def g(k, d=None):
            return cfg.get(k, d)

        if g("restrict_filenames"):   opts["restrictfilenames"] = True
        if g("no_overwrites"):        opts["nooverwrites"] = True
        if g("write_description"):    opts["writedescription"] = True
        if g("write_info_json"):      opts["writeinfojson"] = True
        if g("write_comments"):       opts["getcomments"] = True

        if g("embed_thumbnail"):      opts["embedthumbnail"] = True
        if g("embed_metadata"):       opts["addmetadata"] = True
        if g("embed_chapters"):       opts["embedchapters"] = True

        recode = g("recode_video", "없음")
        if recode and recode != "없음":
            opts["recodevideo"] = recode

        if g("embed_subs"):           opts["embedsubtitles"] = True
        if g("write_subs"):           opts["writesubtitles"] = True
        if g("write_auto_subs"):      opts["writeautomaticsub"] = True
        sub_langs = g("sub_langs", "")
        if sub_langs:                 opts["subtitleslangs"] = sub_langs.split(",")
        opts["subtitlesformat"] = g("sub_format", "srt")

        if g("sponsorblock"):
            cats = g("sponsorblock_categories", "sponsor,intro,outro,selfpromo")
            opts["sponsorblock_remove"] = cats.split(",")

        if g("cookies_file"):         opts["cookiefile"] = g("cookies_file")
        if g("cookie_browser"):       opts["cookiesfrombrowser"] = (g("cookie_browser"),)
        if g("username"):             opts["username"] = g("username")
        if g("password"):             opts["password"] = g("password")
        if g("netrc_location"):       opts["netrc_location"] = g("netrc_location")

        if g("proxy"):                opts["proxy"] = g("proxy")
        if g("rate_limit"):           opts["ratelimit"] = g("rate_limit")
        if g("source_address"):       opts["source_address"] = g("source_address")
        if g("force_ipv4"):           opts["force_ipv4"] = True
        elif g("force_ipv6"):         opts["force_ipv6"] = True
        opts["retries"] = g("retries", 10)
        opts["socket_timeout"] = g("socket_timeout", 30)

        if g("geo_bypass"):
            opts["geo_bypass"] = True
            country = g("geo_bypass_country", "")
            if country:
                opts["geo_bypass_country"] = country
        if g("bypass_age_limit"):     opts["age_limit"] = 99
        if g("download_archive"):     opts["download_archive"] = g("download_archive")
        if g("no_playlist"):          opts["noplaylist"] = True

        merge_fmt = g("merge_output_format", "mkv")
        if merge_fmt:                 opts["merge_output_format"] = merge_fmt

        pl_start = g("playlist_start", 1)
        pl_end   = g("playlist_end", 0)
        pl_items = g("playlist_items", "")
        if pl_items:
            opts["playlist_items"] = pl_items
        else:
            if pl_start > 1:          opts["playliststart"] = pl_start
            if pl_end:                opts["playlistend"] = pl_end

        opts["concurrent_fragment_downloads"] = g("concurrent_fragments", 4)

        tmpl = g("output_template", "%(title)s.%(ext)s")
        if tmpl:                      opts["outtmpl"] = tmpl

        return opts
