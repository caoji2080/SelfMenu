"""
分享视图 - 负责菜谱分享功能的界面展示
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable
import json
import os


class ShareView:
    """分享视图"""

    def __init__(self, parent, callbacks: dict):
        self.parent = parent
        self.callbacks = callbacks

    def create_share_dialog(self, recipe_id: int, recipe_title: str):
        """创建分享对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"📤 分享菜谱 - {recipe_title}")
        dialog.geometry("500x400")
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        ttk.Label(frame, text="选择分享方式",
                 font=('Arial', 14, 'bold')).pack(pady=10)

        # 分享方式选择
        share_frame = ttk.LabelFrame(frame, text="分享渠道", padding=15)
        share_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        share_methods = ['微信', 'QQ', '邮件', '复制链接', '导出 JSON', '导出 CSV']

        for i, method in enumerate(share_methods):
            btn_text = f"📱 {method}" if method in ['微信', 'QQ'] else \
                      f"✉️ {method}" if method == '邮件' else \
                      f"🔗 {method}" if method == '复制链接' else \
                      f"📄 {method}"

            btn = ttk.Button(share_frame, text=btn_text,
                           command=lambda m=method: self._handle_share(m, recipe_id, dialog))
            btn.pack(fill=tk.X, pady=5)

        # 关闭按钮
        ttk.Button(frame, text="关闭",
                  command=dialog.destroy).pack(pady=10)

        return dialog

    def _handle_share(self, method: str, recipe_id: int, dialog: tk.Toplevel):
        """处理分享操作"""
        if method in ['微信', 'QQ']:
            messagebox.showinfo("提示", f"已复制到剪贴板，请在{method}中粘贴分享")
        elif method == '邮件':
            messagebox.showinfo("提示", "邮件分享功能开发中...")
        elif method == '复制链接':
            link = f"recipe://{recipe_id}"
            dialog.clipboard_clear()
            dialog.clipboard_append(link)
            messagebox.showinfo("成功", "链接已复制到剪贴板")
        elif method.startswith('导出'):
            file_format = 'json' if 'JSON' in method else 'csv'
            self.export_recipe(recipe_id, file_format)

        dialog.destroy()

    def export_recipe(self, recipe_id: int, format: str = 'json'):
        """导出菜谱"""
        if self.callbacks.get('on_export'):
            filepath = filedialog.asksaveasfilename(
                defaultextension=f".{format}",
                filetypes=[(f"{format.upper()} files", f"*.{format}")],
                title="导出菜谱"
            )
            if filepath:
                self.callbacks.get('on_export')(recipe_id, format, filepath)
                messagebox.showinfo("成功", f"菜谱已导出到：{filepath}")
