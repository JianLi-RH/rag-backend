# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
from typing import List, Dict, Optional

from enums import EmbedStatus

def format_bytes(bytes_size: int) -> str:
    """���ֽ���ת��Ϊ����ɶ��ĸ�ʽ��"""
    if bytes_size == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index = 0
    
    while bytes_size >= 1024.0 and unit_index < len(units) - 1:
        bytes_size /= 1024.0
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(bytes_size)} {units[unit_index]}"
    else:
        return f"{bytes_size:.2f} {units[unit_index]}"
    
class FileStatusManager:
    def __init__(self, status_file: str = "file-status.json"):
        self.status_file = status_file
        self._ensure_status_file_exists()

    def _ensure_status_file_exists(self):
        """Create status file if it doesn't exist."""
        if not os.path.exists(self.status_file):
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump({"files": []}, f, ensure_ascii=False, indent=2)

    def get_all_files(self) -> List[Dict]:
        """Get all files from status file."""

        if not os.path.exists(self.status_file):
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump({"files": []}, f, ensure_ascii=False, indent=4)
            return []

        with open(self.status_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("files", [])

    def _normalize_path(self, path: str) -> str:
        """Normalize path for comparison."""
        return os.path.normpath(path).replace('\\', '/')

    def get_file_status(self, file_path: str) -> Optional[Dict]:
        """Get status for a specific file."""
        files = self.get_all_files()
        normalized_path = self._normalize_path(file_path)
        for file_info in files:
            if self._normalize_path(file_info.get('path', '')) == normalized_path:
                return file_info
        return None

    def add_file(self, file_name: str, file_path: str, embeded: str = EmbedStatus.not_started.name) -> Dict:
        """Add a new file to status."""
        size = format_bytes(os.stat(file_path).st_size)
        files = self.get_all_files()
        normalized_path = self._normalize_path(file_path)

        for file_info in files:
            if self._normalize_path(file_info.get('path', '')) == normalized_path:
                return file_info

        new_file = {
            "name": file_name,
            "path": file_path,
            "embeded": embeded,
            "size": size,
            "upload_time": datetime.now().isoformat()
        }

        files.append(new_file)
        self._save_status(files)
        return new_file

    def update_file_status(self, file_path: str, **updates) -> Optional[Dict]:
        """Update status for a file."""
        files = self.get_all_files()
        updated = False
        normalized_path = self._normalize_path(file_path)
        
        updates['last_update'] = datetime.now().isoformat()

        for file_info in files:
            if self._normalize_path(file_info.get('path', '')) == normalized_path:
                file_info.update(updates)
                updated = True
                break

        if updated:
            self._save_status(files)
            return file_info
        return None

    def update_vectorized_status(self, file_path: str, embeded: str) -> Optional[Dict]:
        """Update vectorization status for a file."""
        updates = {
            'embeded': embeded
        }
        if embeded == EmbedStatus.completed.name:
            updates['vectorized_time'] = datetime.now().isoformat()
        else:
            updates['vectorized_time'] = None

        return self.update_file_status(file_path, **updates)

    def _save_status(self, files: List[Dict]):
        """Save status to file."""
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump({"files": files}, f, ensure_ascii=False, indent=2)

    def get_relative_path(self, absolute_path: str, base_dir: str = ".") -> str:
        """Get relative path from base directory."""
        return os.path.relpath(absolute_path, base_dir)

    def get_absolute_path(self, relative_path: str, base_dir: str = ".") -> str:
        """Get absolute path from relative path."""
        return os.path.abspath(os.path.join(base_dir, relative_path))
    
    def get_file_name(self, file_path: str) -> str:
        """Get file name for a file."""
        return os.path.basename(self.get_relative_path(file_path))

