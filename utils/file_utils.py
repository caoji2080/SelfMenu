"""
文件处理工具函数
"""
import json
import csv
import os
from typing import List, Dict, Optional
from pathlib import Path
from app_config import EXPORT_DIR, IMPORT_DIR

class FileUtils:
    """文件处理工具类"""

    @staticmethod
    def ensure_dirs():
        """确保目录存在"""
        for directory in [EXPORT_DIR, IMPORT_DIR]:
            directory.mkdir(exist_ok=True, parents=True)

    @staticmethod
    def export_to_json(data: List[Dict], filename: str) -> bool:
        """导出数据为 JSON 文件"""
        try:
            FileUtils.ensure_dirs()
            filepath = EXPORT_DIR / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"导出 JSON 失败：{e}")
            return False

    @staticmethod
    def import_from_json(filename: str) -> Optional[List[Dict]]:
        """从 JSON 文件导入数据"""
        try:
            FileUtils.ensure_dirs()
            filepath = IMPORT_DIR / filename
            if not filepath.exists():
                return None
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if isinstance(data, list) else None
        except Exception as e:
            print(f"导入 JSON 失败：{e}")
            return None

    @staticmethod
    def export_to_csv(data: List[Dict], filename: str, fieldnames: List[str]) -> bool:
        """导出数据为 CSV 文件"""
        try:
            FileUtils.ensure_dirs()
            filepath = EXPORT_DIR / filename
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"导出 CSV 失败：{e}")
            return False

    @staticmethod
    def import_from_csv(filename: str) -> Optional[List[Dict]]:
        """从 CSV 文件导入数据"""
        try:
            FileUtils.ensure_dirs()
            filepath = IMPORT_DIR / filename
            if not filepath.exists():
                return None
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            return data
        except Exception as e:
            print(f"导入 CSV 失败：{e}")
            return None

    @staticmethod
    def get_export_files(extension: str = '') -> List[str]:
        """获取导出目录中的所有文件"""
        FileUtils.ensure_dirs()
        files = []
        for f in EXPORT_DIR.iterdir():
            if f.is_file():
                if not extension or f.suffix == extension:
                    files.append(f.name)
        return sorted(files)

    @staticmethod
    def get_import_files(extension: str = '') -> List[str]:
        """获取导入目录中的所有文件"""
        FileUtils.ensure_dirs()
        files = []
        for f in IMPORT_DIR.iterdir():
            if f.is_file():
                if not extension or f.suffix == extension:
                    files.append(f.name)
        return sorted(files)

    @staticmethod
    def delete_file(directory: str, filename: str) -> bool:
        """删除指定文件"""
        try:
            if directory == 'export':
                filepath = EXPORT_DIR / filename
            else:
                filepath = IMPORT_DIR / filename

            if filepath.exists():
                filepath.unlink()
                return True
            return False
        except Exception as e:
            print(f"删除文件失败：{e}")
            return False

    @staticmethod
    def file_exists(directory: str, filename: str) -> bool:
        """检查文件是否存在"""
        if directory == 'export':
            return (EXPORT_DIR / filename).exists()
        else:
            return (IMPORT_DIR / filename).exists()
