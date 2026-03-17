import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, Dict, Any, List



class BaseView:
    """基础视图类，提供通用 UI 功能"""

    def __init__(self, parent: tk.Tk = None):
        self.parent = parent or tk.Tk()
        self.style = ttk.Style()
        self._setup_style()

    def _setup_style(self):
        """设置样式"""
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Arial', 12))
        self.style.configure('Card.TFrame', background='white', relief='raised', borderwidth=1)

    def show_info(self, message: str, title: str = "提示"):
        CommonDialog.show_info(message, title)

    def show_error(self, message: str, title: str = "错误"):
        CommonDialog.show_error(message, title)

    def show_warning(self, message: str, title: str = "警告"):
        CommonDialog.show_warning(message, title)

    def show_confirm(self, message: str, title: str = "确认") -> bool:
        return CommonDialog.show_confirm(message, title)
