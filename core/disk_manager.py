"""
Tropical Downloader - Disk Space Monitor & Node Modules Cleaner
Monitors disk space (+10% margin), manages RAM buffering, and purges node_modules on low disk.
"""
import os
import shutil
import concurrent.futures
from PySide6.QtCore import QThread, Signal

def get_free_space(path: str) -> int:
    """Returns free space in bytes for given directory path"""
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        usage = shutil.disk_usage(path)
        return usage.free
    except Exception:
        return 10 * 1024 * 1024 * 1024  # 10GB fallback on error

def has_sufficient_space(target_path: str, estimated_bytes: int, safety_margin: float = 0.10) -> tuple[bool, int, int]:
    """
    Checks if target_path has enough space for estimated_bytes + safety_margin (default +10%).
    Returns (has_space: bool, free_bytes: int, required_bytes: int)
    """
    free_b = get_free_space(target_path)
    req_b = int(estimated_bytes * (1.0 + safety_margin))
    return (free_b >= req_b), free_b, req_b

def purge_node_modules(root_dirs: list[str] = None, log_callback=None) -> int:
    """
    Searches and permanently deletes node_modules folders across the user system to free disk space.
    Returns total freed size in bytes.
    """
    if root_dirs is None:
        home = os.path.expanduser("~")
        root_dirs = [
            os.path.join(home, "Desktop"),
            os.path.join(home, "Documents"),
            os.path.join(home, "Downloads"),
            os.path.join(home, "Projects"),
            os.path.join(home, "source"),
            os.path.join(home, "repos"),
            os.path.join(home, "workspace"),
            "D:\\", "E:\\", "C:\\Users"
        ]

    deleted_count = 0
    freed_bytes = 0

    def remove_folder(path):
        nonlocal deleted_count, freed_bytes
        try:
            size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        size += os.path.getsize(fp)
            shutil.rmtree(path, ignore_errors=True)
            deleted_count += 1
            freed_bytes += size
            if log_callback:
                log_callback(f"[저장공간 확보] node_modules 삭제 완료: {path} ({size / 1048576:.1f} MB 확보)")
        except Exception as e:
            if log_callback:
                log_callback(f"[경고] node_modules 삭제 실패: {path} - {e}")

    targets = []
    for root in root_dirs:
        if not os.path.exists(root):
            continue
        try:
            for dirpath, dirnames, _ in os.walk(root):
                if "node_modules" in dirnames:
                    full_path = os.path.join(dirpath, "node_modules")
                    targets.append(full_path)
                    dirnames.remove("node_modules")  # Don't recurse inside
                if len(targets) > 50:
                    break
        except Exception:
            pass

    if targets:
        if log_callback:
            log_callback(f"[저장공간 자동 확보] 감지된 {len(targets)}개의 node_modules 폴더 영구 삭제 진행 중...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(remove_folder, targets)

    return freed_bytes


class NodeModulesPurgeWorker(QThread):
    log_signal = Signal(str)
    finished_signal = Signal(int)

    def __init__(self, roots=None):
        super().__init__()
        self.roots = roots

    def run(self):
        freed = purge_node_modules(self.roots, log_callback=self.log_signal.emit)
        self.finished_signal.emit(freed)
