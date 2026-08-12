"""
Tropical Downloader - File Service
Disk space monitoring, file listing, node_modules emergency cleanup.
"""

import os
import shutil
import concurrent.futures
from typing import Dict, Any, List, Tuple


class FileService:
    def get_free_space(self, path: str) -> int:
        try:
            os.makedirs(path, exist_ok=True)
            usage = shutil.disk_usage(path)
            return usage.free
        except Exception:
            return 10 * 1024 * 1024 * 1024  # 10GB fallback

    def has_sufficient_space(
        self, target_path: str, estimated_bytes: int, safety_margin: float = 0.10
    ) -> Tuple[bool, int, int]:
        free_b = self.get_free_space(target_path)
        req_b = int(estimated_bytes * (1.0 + safety_margin))
        return (free_b >= req_b), free_b, req_b

    def list_files(self, directory: str) -> List[Dict[str, Any]]:
        if not os.path.exists(directory):
            return []
        
        items = []
        try:
            for fname in os.listdir(directory):
                fpath = os.path.join(directory, fname)
                if os.path.isfile(fpath):
                    stat = os.stat(fpath)
                    items.append({
                        "name": fname,
                        "path": fpath,
                        "size": stat.st_size,
                        "modified": stat.st_mtime
                    })
        except Exception as e:
            print(f"[FileService] List files error: {e}")
        return items

    def delete_file(self, filepath: str) -> bool:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception as e:
            print(f"[FileService] Delete file error: {e}")
        return False

    def purge_node_modules(self, root_dirs: List[str] = None, log_callback=None) -> int:
        if root_dirs is None:
            home = os.path.expanduser("~")
            root_dirs = [
                os.path.join(home, "Desktop"),
                os.path.join(home, "Documents"),
                os.path.join(home, "Downloads"),
                os.path.join(home, "Projects"),
                "D:\\", "C:\\Users"
            ]

        targets = []
        for root in root_dirs:
            if not os.path.exists(root):
                continue
            try:
                for dirpath, dirnames, _ in os.walk(root):
                    if "node_modules" in dirnames:
                        full_path = os.path.join(dirpath, "node_modules")
                        targets.append(full_path)
                        dirnames.remove("node_modules")
                    if len(targets) >= 30:
                        break
            except Exception:
                pass

        freed_bytes = 0

        def remove_folder(path):
            nonlocal freed_bytes
            try:
                size = 0
                for dirpath, _, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if os.path.exists(fp):
                            size += os.path.getsize(fp)
                shutil.rmtree(path, ignore_errors=True)
                freed_bytes += size
                if log_callback:
                    log_callback(f"[Purge] Removed: {path} ({size / 1048576:.1f} MB freed)")
            except Exception as e:
                if log_callback:
                    log_callback(f"[Purge Error] {path}: {e}")

        if targets:
            if log_callback:
                log_callback(f"[Purge] Found {len(targets)} node_modules folders. Purging...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                executor.map(remove_folder, targets)

        return freed_bytes


file_service = FileService()
