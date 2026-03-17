"""
导入导出视图 - 负责菜谱导入导出功能的界面展示
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable
import os


class ImportExportView:
    """导入导出视图"""

    def __init__(self, parent, callbacks: dict):
        self.parent = parent
        self.callbacks = callbacks

    def create_import_export_dialog(self):
        """创建导入导出对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("📥📤 导入导出管理")
        dialog.geometry("600x400")
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        ttk.Label(frame, text="导入导出管理",
                 font=('Arial', 16, 'bold')).pack(pady=10)

        # 选项卡
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # 导出选项卡
        export_frame = ttk.Frame(notebook, padding=10)
        notebook.add(export_frame, text="📤 导出")
        self._create_export_tab(export_frame, dialog)

        # 导入选项卡
        import_frame = ttk.Frame(notebook, padding=10)
        notebook.add(import_frame, text="📥 导入")
        self._create_import_tab(import_frame, dialog)

        return dialog

    def _create_export_tab(self, parent, dialog):
        """创建导出选项卡"""
        # 导出格式选择
        format_frame = ttk.LabelFrame(parent, text="导出格式", padding=10)
        format_frame.pack(fill=tk.X, pady=10)

        self.export_format_var = tk.StringVar(value='json')
        formats = [
            ('JSON 格式', 'json'),
            ('CSV 格式', 'csv'),
            ('TXT 文本', 'txt')
        ]

        for text, value in formats:
            ttk.Radiobutton(format_frame, text=text,
                          variable=self.export_format_var,
                          value=value).pack(anchor=tk.W, pady=2)

        # 导出范围
        range_frame = ttk.LabelFrame(parent, text="导出范围", padding=10)
        range_frame.pack(fill=tk.X, pady=10)

        self.export_range_var = tk.StringVar(value='all')
        ranges = [
            ('全部菜谱', 'all'),
            ('已发布菜谱', 'published'),
            ('草稿菜谱', 'draft'),
            ('指定类别', 'category')
        ]

        for text, value in ranges:
            ttk.Radiobutton(range_frame, text=text,
                          variable=self.export_range_var,
                          value=value).pack(anchor=tk.W, pady=2)

        # 类别选择（当选择"指定类别"时启用）
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(range_frame, textvariable=self.category_var, width=47)
        category_combo.pack(anchor=tk.W, pady=5)
        category_combo['state'] = 'disabled'

        # 监听类别选项
        def on_range_change():
            if self.export_range_var.get() == 'category':
                category_combo['state'] = 'readonly'
            else:
                category_combo['state'] = 'disabled'

        self.export_range_var.trace('w', lambda *args: on_range_change())

        # 导出按钮
        ttk.Button(parent, text="📤 导出",
                  command=lambda: self._do_export(dialog)).pack(pady=10)

    def _create_import_tab(self, parent, dialog):
        """创建导入选项卡"""
        # 文件选择
        file_frame = ttk.LabelFrame(parent, text="选择文件", padding=10)
        file_frame.pack(fill=tk.X, pady=10)

        self.import_file_path = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.import_file_path, width=50)
        file_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(file_frame, text="浏览...",
                  command=self._browse_file).pack(side=tk.LEFT)

        # 导入选项
        option_frame = ttk.LabelFrame(parent, text="导入选项", padding=10)
        option_frame.pack(fill=tk.X, pady=10)

        self.skip_duplicate_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(option_frame, text="跳过重复的菜谱",
                       variable=self.skip_duplicate_var).pack(anchor=tk.W, pady=2)

        self.update_existing_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(option_frame, text="更新已存在的菜谱",
                       variable=self.update_existing_var).pack(anchor=tk.W, pady=2)

        # 导入按钮
        ttk.Button(parent, text="📥 导入",
                  command=lambda: self._do_import(dialog)).pack(pady=10)

    def _browse_file(self):
        """浏览选择文件"""
        filepath = filedialog.askopenfilename(
            title="选择导入文件",
            filetypes=[
                ("JSON 文件", "*.json"),
                ("CSV 文件", "*.csv"),
                ("所有文件", "*.*")
            ]
        )
        if filepath:
            self.import_file_path.set(filepath)

    def _do_export(self, dialog):
        """执行导出"""
        if self.callbacks.get('on_export'):
            filepath = filedialog.asksaveasfilename(
                defaultextension=f".{self.export_format_var.get()}",
                filetypes=[(f"{self.export_format_var.get().upper()} 文件",
                           f"*.{self.export_format_var.get()}")],
                title="导出菜谱"
            )
            if filepath:
                options = {
                    'format': self.export_format_var.get(),
                    'range': self.export_range_var.get(),
                    'category': self.category_var.get() if self.export_range_var.get() == 'category' else None
                }
                count = self.callbacks.get('on_export')(filepath, options)
                messagebox.showinfo("成功", f"已导出 {count} 个菜谱到：\n{filepath}")
                dialog.destroy()

    def _do_import(self, dialog):
        """执行导入"""
        if not self.import_file_path.get():
            messagebox.showwarning("警告", "请先选择要导入的文件")
            return

        if self.callbacks.get('on_import'):
            filepath = self.import_file_path.get()
            options = {
                'skip_duplicate': self.skip_duplicate_var.get(),
                'update_existing': self.update_existing_var.get()
            }

            try:
                result = self.callbacks.get('on_import')(filepath, options)
                messagebox.showinfo("成功",
                                  f"导入完成！\n成功：{result.get('success', 0)}\n失败：{result.get('failed', 0)}")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"导入失败：{str(e)}")
